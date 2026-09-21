"""Shared stem (paper identifier) helpers for the papers/ scripts.

A stem is `<registry>-<native-id>`, lowercase ASCII, and is the routing key that
ties `pdf/<stem>.pdf`, `md/<stem>.md` and `json/<stem>.json` together. Stems are
never renamed; see papers/AGENTS.md for the rule and its rationale.

Paths are resolved through functions so tests can redirect the whole library by
patching `stem.BASE` alone.
"""

import hashlib
import json
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REGISTRIES = ("arxiv", "openreview", "acl", "doi", "web", "repo")
STEM_RE = re.compile(r"^(?:%s)-[a-z0-9][a-z0-9.-]*$" % "|".join(REGISTRIES))
ARXIV_RE = re.compile(r"^\d{4}\.\d{4,5}(?:v[1-9]\d*)?$")


def base():
    return BASE


def pdf_dir():
    return os.path.join(BASE, "pdf")


def md_dir():
    return os.path.join(BASE, "md")


def json_dir():
    return os.path.join(BASE, "json")


def meta_path():
    return os.path.join(BASE, "meta.json")


def provenance_path():
    return os.path.join(BASE, "provenance.json")


def to_stem(value):
    """Normalize user input into a stem. Bare arXiv ids stay supported."""
    text = (value or "").strip()
    if STEM_RE.match(text):
        return text
    if ARXIV_RE.match(text):
        return "arxiv-" + text
    raise ValueError(f"不是合法词干（<registry>-<native-id>）或 arXiv 编号：{value}")


def registry(stem):
    return stem.split("-", 1)[0]


def native_id(stem):
    return stem.split("-", 1)[1]


def pdf_path(stem):
    return os.path.join(pdf_dir(), f"{stem}.pdf")


def md_path(stem):
    return os.path.join(md_dir(), f"{stem}.md")


def json_path(stem):
    return os.path.join(json_dir(), f"{stem}.json")


def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


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


def yaml_quote(value):
    text = "" if value is None else str(value)
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def read_front_matter(stem):
    """Existing front-matter fields, so a re-conversion keeps curated values."""
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


BARE = {"id", "registry", "native_id", "pdf", "parser"}  # simple slugs; no quoting needed


def front_matter(stem, meta=None, record=None, kind=None):
    """YAML block identifying the file even when INDEX.md is stale."""
    meta = meta or {}
    record = record or {}
    conversion = record.get("conversion") or {}
    existing = read_front_matter(stem)
    pick = lambda key, value: value if value not in (None, "") else existing.get(key)
    fields = {
        "id": stem,
        "title": pick("title", meta.get("title")),
        "registry": registry(stem),
        "native_id": native_id(stem),
        "version": pick("version", record.get("version")),
        "kind": kind or existing.get("kind") or "[unclassified]",
        "pdf": f"pdf/{stem}.pdf",
        "pdf_sha256": record.get("pdf_sha256"),
        "parser": conversion.get("parser"),
        "converted_at": conversion.get("converted_at"),
    }
    lines = ["---"]
    for key, value in fields.items():
        if value is None:
            lines.append(f"{key}: null")
        elif key == "kind":
            lines.append(f"kind: {value}")
        elif key in BARE:
            lines.append(f"{key}: {value}")
        else:
            lines.append(f"{key}: {yaml_quote(value)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def body_after_front_matter(text):
    """Drop an existing front-matter block; the remainder is the file proper."""
    match = re.match(r"^---\n.*?\n---\n", text, re.S)
    return text[match.end():] if match else text
