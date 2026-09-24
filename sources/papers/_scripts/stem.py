"""Shared stem helpers for the papers/ scripts.

Naming (see papers/AGENTS.md):
  file stem = slug of the paper title plus its version, e.g. `mem0-...-memory-v1`
  identity  = `<registry>-<native-id><vN>`, kept in index.csv and in the md
              front matter as `id`, never derived from the filename again

The stem routes `pdf/<stem>.pdf` and `md/<stem>.md`. Images live flat under
`assets/` and are named by `id`, not by stem. Paths resolve through functions so
tests can move the library by patching `stem.BASE` alone.
"""

import csv
import hashlib
import json
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SLUG_LIMIT = 96
REGISTRIES = ("arxiv", "openreview", "acl", "doi", "web", "repo")
ARXIV_RE = re.compile(r"^\d{4}\.\d{4,5}(?:v[1-9]\d*)?$")
ID_RE = re.compile(r"^(?:%s)-[a-z0-9][a-z0-9.-]*$" % "|".join(REGISTRIES))
VERSION_RE = re.compile(r"v[1-9]\d*$")

# index.csv is a pointer table: enough to locate a paper, nothing more.
INDEX_FIELDS = ["id", "name", "keywords", "revised"]
# md front matter is the per-paper register: 8 fields, no duplicates of index.csv.
FRONT_FIELDS = ["stem", "id", "keywords", "abstract", "revised", "source",
                "parser", "state"]


def base():
    return BASE


def pdf_dir():
    return os.path.join(BASE, "pdf")


def md_dir():
    return os.path.join(BASE, "md")


def assets_root():
    return os.path.join(BASE, "assets")


def index_path():
    return os.path.join(BASE, "index.csv")


def meta_path():
    return os.path.join(BASE, "meta.json")


def provenance_path():
    return os.path.join(BASE, "provenance.json")


def pdf_path(stem):
    return os.path.join(pdf_dir(), f"{stem}.pdf")


def md_path(stem):
    return os.path.join(md_dir(), f"{stem}.md")


def version_suffix(version):
    """`2504.19413v11` -> `v11`. Missing or unknown versions get no suffix.

    Inventing a version into a filename would invent an identity.
    """
    match = VERSION_RE.search((version or "").strip())
    return match.group(0) if match else ""


def with_version(slug, version):
    """Attach the version suffix to a slug, unless it already carries it."""
    suffix = version_suffix(version)
    if not suffix or slug.endswith("-" + suffix):
        return slug
    return f"{slug}-{suffix}"


def normalize_date(value):
    """`2025/04/28` or `2025-04-28T01:49:46Z` -> `2025-04-28`; else None."""
    match = re.match(r"(\d{4})[/-](\d{2})[/-](\d{2})", (value or "").strip())
    return f"{match.group(1)}-{match.group(2)}-{match.group(3)}" if match else None


def native_from_id(value):
    """`arxiv-2504.19413v1` -> `2504.19413`."""
    text = VERSION_RE.sub("", (value or "").strip())
    return text.split("-", 1)[1] if "-" in text else ""


def identity(meta, prov=None):
    """`<registry>-<native-id><vN>`, derived from the raw metadata.

    The filename never contributes: it is a label, this is the identity.
    """
    meta = meta or {}
    prov = prov or {}
    native = meta.get("native_id") or ""
    if not native:
        return ""
    suffix = version_suffix(prov.get("version") or meta.get("versioned_id") or "")
    return f"{meta.get('registry') or 'arxiv'}-{native}{suffix}"


ILLEGAL_NAME_CHARS = re.compile(r'[<>:"/\\|?*]')


def sanitize_name(text):
    """Replace the characters Windows forbids in a filename with `.`.

    Case is preserved on purpose: the name is what a person reads, and `A-Mem`
    is the paper's name while `a-mem` is not.
    """
    cleaned = ILLEGAL_NAME_CHARS.sub(".", (text or "").strip())
    cleaned = re.sub(r"\.{2,}", ".", cleaned)
    return cleaned.strip(". ")


def stem_of(record):
    """The filename stem: `<id>.<name>`. One rule, applied in one place."""
    record = record or {}
    return f"{record.get('id') or ''}.{record.get('name') or ''}"


def name_from_stem(stem, ident):
    """Recover `<name>` from `<id>.<name>`; '' when the stem does not start with that id."""
    prefix = f"{ident or ''}."
    if not ident or not stem.startswith(prefix):
        return ""
    return stem[len(prefix):]


def slugify(title, limit=SLUG_LIMIT):
    """Deterministic filename slug: lowercase, ASCII alphanumerics and CJK kept,
    everything else becomes a separator, cut on a word boundary at `limit`."""
    text = (title or "").lower()
    chars = []
    for ch in text:
        if ch.isascii() and ch.isalnum():
            chars.append(ch)
        elif "一" <= ch <= "鿿":
            chars.append(ch)
        else:
            chars.append("-")
    slug = re.sub(r"-+", "-", "".join(chars)).strip("-")
    if len(slug) > limit:
        cut = slug[:limit]
        if "-" in cut:
            cut = cut[:cut.rindex("-")]
        slug = cut.strip("-")
    return slug


def load_json(path):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    temporary = path + ".tmp"
    with open(temporary, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(temporary, path)


def load_meta():
    return load_json(meta_path())


def save_meta(data):
    save_json(meta_path(), data)


def load_provenance():
    return load_json(provenance_path())


def save_provenance(data):
    save_json(provenance_path(), data)


def read_index():
    """Rows of index.csv; `keywords` comes back as a list."""
    if not os.path.exists(index_path()):
        return []
    with open(index_path(), encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    out = []
    for row in rows:
        record = {key: (row.get(key) or "") for key in INDEX_FIELDS}
        record["keywords"] = [w for w in record["keywords"].split(";") if w]
        out.append(record)
    return out


def write_index(papers):
    os.makedirs(os.path.dirname(index_path()), exist_ok=True)
    with open(index_path(), "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=INDEX_FIELDS, lineterminator="\n")
        writer.writeheader()
        for record in sorted(papers, key=stem_of):
            row = {key: record.get(key) for key in INDEX_FIELDS}
            row["keywords"] = ";".join(record.get("keywords") or [])
            writer.writerow(row)


def load_index():
    return {"papers": read_index()}


def save_index(data):
    write_index(data.get("papers", []))


def records():
    return read_index()


def find(token):
    """Resolve a stem, an id, a name, or the bare native id to an index record."""
    token = (token or "").strip()
    if not token:
        return None
    for record in records():
        if token in (stem_of(record), record.get("id"), record.get("name")):
            return record
        if token == native_from_id(record.get("id")):
            return record
    slug = slugify(token)
    for record in records():
        if slugify(stem_of(record)) == slug:
            return record
    return None


def to_stem(token):
    """Filename stem for a CLI argument: a known stem/id/name, or a new title's slug."""
    token = (token or "").strip()
    record = find(token)
    if record:
        return stem_of(record)
    if ARXIV_RE.match(token) or re.fullmatch(r"arxiv-\d{4}\.\d{4,5}(?:v[1-9]\d*)?", token):
        raise ValueError(f"[{token}] 尚未入库，无法解析为词干；先下载或用标题运行")
    return slugify(token)


def native_for(token, record=None):
    """arXiv native id behind a token, for scripts that must hit the arXiv API.

    A filename stem now starts with `arxiv-` too, so the bare-id form is matched
    in full; a prefix test would swallow `arxiv-2512.13564.Memory in the Age…`.
    """
    if ARXIV_RE.match(token):
        return token
    match = re.fullmatch(r"arxiv-(\d{4}\.\d{4,5}(?:v[1-9]\d*)?)", (token or "").strip())
    if match:
        return match.group(1)
    if record:
        return native_from_id(record.get("id")) or None
    return None


def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def yaml_quote(value):
    text = "" if value is None else str(value)
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


LIST_KEYS = ("keywords", "state")
BARE = {"stem", "id", "parser", "revised"}
EMPTY_TOKENS = ("", "null", "none")


def _clean_list(value):
    """Drop empty and literal `null` tokens; a blocked field must not become a word."""
    raw = value if isinstance(value, list) else [value]
    return [str(v).strip() for v in raw
            if str(v).strip().lower() not in EMPTY_TOKENS]


def read_front_matter(stem):
    path = md_path(stem)
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        head = f.read(8192)
    match = re.match(r"^---\n(.*?)\n---\n", head, re.S)
    if not match:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            fields[key] = [v.strip().strip('"') for v in value[1:-1].split(",") if v.strip()]
        else:
            plain = value.strip('"')
            fields[key] = "" if plain.lower() in ("null", "none") else plain
    return fields


def front_matter(stem, meta=None, index_record=None, prov=None, kind=None,
                 keywords=None, abstract=None, revised=None, source=None,
                 parser=None, state=None, ident=None):
    """The eight-field register block above the parser output.

    Everything after the closing `---` is the untouched parser text; this block
    is the only place the project writes its own judgement.
    """
    meta = meta or {}
    index_record = index_record or {}
    prov = prov or {}
    conversion = prov.get("conversion") or {}
    existing = read_front_matter(stem)

    def missing(value):
        if value is None:
            return True
        if isinstance(value, str):
            return value.strip().lower() in ("", "null", "none")
        if isinstance(value, list):
            return not _clean_list(value)
        return False

    def pick(key, *values):
        for value in values:
            if not missing(value):
                return value
        fallback = existing.get(key)
        return None if missing(fallback) else fallback

    fields = [
        ("stem", stem),
        ("id", ident or pick("id", index_record.get("id")) or identity(meta, prov)),
        ("keywords", keywords or pick("keywords", index_record.get("keywords"))),
        ("abstract", abstract or pick("abstract", meta.get("abstract"))),
        ("revised", revised or pick("revised", normalize_date(meta.get("revised")))),
        ("source", source or pick("source", prov.get("source_url"), meta.get("url"))),
        ("parser", parser or pick("parser", conversion.get("parser"))),
        ("state", state or pick("state", prov.get("state"))),
    ]
    lines = ["---"]
    for key, value in fields:
        if value is None:
            lines.append(f"{key}: null")
        elif key in LIST_KEYS:
            lines.append("%s: [%s]" % (key, ", ".join(_clean_list(value))))
        elif key in BARE:
            lines.append(f"{key}: {value}")
        else:
            lines.append(f"{key}: {yaml_quote(value)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def body_after_front_matter(text):
    match = re.match(r"^---\n.*?\n---\n", text, re.S)
    return text[match.end():] if match else text
