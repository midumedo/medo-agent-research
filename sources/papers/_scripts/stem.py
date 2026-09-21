"""Shared stem helpers for the papers/ scripts.

Naming (see papers/AGENTS.md):
  file stem = slug of the paper title, frozen at ingest
  identity  = `<registry>-<native-id>`, kept in index.json and in the md front
              matter as `id`, never derived from the filename again

The stem routes `pdf/<stem>.pdf`, `md/<stem>.md`, `json/<stem>.json` and
`assets/<stem>/`. Paths resolve through functions so tests can move the
library by patching `stem.BASE` alone.
"""

import hashlib
import json
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SLUG_LIMIT = 96
REGISTRIES = ("arxiv", "openreview", "acl", "doi", "web", "repo")
ARXIV_RE = re.compile(r"^\d{4}\.\d{4,5}(?:v[1-9]\d*)?$")
ID_RE = re.compile(r"^(?:%s)-[a-z0-9][a-z0-9.-]*$" % "|".join(REGISTRIES))


def base():
    return BASE


def pdf_dir():
    return os.path.join(BASE, "pdf")


def md_dir():
    return os.path.join(BASE, "md")


def json_dir():
    return os.path.join(BASE, "json")


def assets_dir(stem):
    return os.path.join(BASE, "assets", stem)


def index_path():
    return os.path.join(BASE, "index.json")


def meta_path():
    return os.path.join(BASE, "meta.json")


def provenance_path():
    return os.path.join(BASE, "provenance.json")


def pdf_path(stem):
    return os.path.join(pdf_dir(), f"{stem}.pdf")


def md_path(stem):
    return os.path.join(md_dir(), f"{stem}.md")


def json_path(stem):
    return os.path.join(json_dir(), f"{stem}.json")


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


def load_index():
    return load_json(index_path())


def save_index(data):
    save_json(index_path(), data)


def records():
    return load_index().get("papers", [])


def find(token):
    """Resolve a stem, an id, a native id, or a title to an index record."""
    token = (token or "").strip()
    if not token:
        return None
    for record in records():
        if token in (record.get("stem"), record.get("id"), record.get("native_id")):
            return record
    slug = slugify(token)
    for record in records():
        if record.get("stem") == slug:
            return record
    return None


def to_stem(token):
    """Stem for a CLI argument: a known stem/id/title, or the slug of a new title."""
    token = (token or "").strip()
    record = find(token)
    if record:
        return record["stem"]
    if token.startswith("arxiv-") or ARXIV_RE.match(token):
        raise ValueError(f"[{token}] 尚未入库，无法解析为词干；先下载或用标题运行")
    return slugify(token)


def native_for(token, record=None):
    """arXiv native id behind a token, for scripts that must hit the arXiv API."""
    if ARXIV_RE.match(token):
        return token
    if token.startswith("arxiv-"):
        return token.split("-", 1)[1]
    if record:
        return record.get("native_id")
    return None


def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def yaml_quote(value):
    text = "" if value is None else str(value)
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


BARE = {"stem", "id", "registry", "native_id", "pdf", "parser"}


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
        fields[key.strip()] = value.strip().strip('"')
    return fields


def front_matter(stem, meta=None, index_record=None, prov=None, kind=None):
    """YAML block: identity comes from index.json, never from the filename."""
    meta = meta or {}
    index_record = index_record or {}
    prov = prov or {}
    conversion = prov.get("conversion") or {}
    existing = read_front_matter(stem)

    def missing(value):
        return value is None or (isinstance(value, str) and value.strip().lower() in ("", "null", "none"))

    def pick(key, *values):
        for value in values:
            if not missing(value):
                return value
        return None if missing(existing.get(key)) else existing.get(key)

    kinds = kind or index_record.get("kinds") or ([existing["kind"].strip("[]")] if existing.get("kind") else [])
    fields = [
        ("stem", stem),
        ("id", pick("id", index_record.get("id"), meta.get("id"))),
        ("title", pick("title", index_record.get("title"), meta.get("title"))),
        ("registry", pick("registry", index_record.get("registry"), meta.get("registry"))),
        ("native_id", pick("native_id", index_record.get("native_id"), meta.get("native_id"))),
        ("version", pick("version", index_record.get("version"), prov.get("version"))),
        ("kinds", "[%s]" % ", ".join(kinds) if kinds else "[]"),
        ("pdf", f"pdf/{stem}.pdf"),
        ("pdf_sha256", pick("pdf_sha256", prov.get("pdf_sha256"), index_record.get("pdf_sha256"))),
        ("parser", conversion.get("parser")),
        ("converted_at", conversion.get("converted_at")),
    ]
    lines = ["---"]
    for key, value in fields:
        if value is None:
            lines.append(f"{key}: null")
        elif key in BARE or key == "kinds":
            lines.append(f"{key}: {value}")
        else:
            lines.append(f"{key}: {yaml_quote(value)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def body_after_front_matter(text):
    match = re.match(r"^---\n.*?\n---\n", text, re.S)
    return text[match.end():] if match else text
