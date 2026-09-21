"""Rebuild papers/index.json from the files, meta.json, provenance.json and md front matter.

index.json is the single source of truth for identity and semantics in the
library. Everything else (INDEX.md, SQL views) is derived from it.

Usage: build_index.py [--check]
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stem

EMPTY = {
    "stem": None,
    "id": None,
    "registry": None,
    "native_id": None,
    "alt_ids": [],
    "title": None,
    "slug_year": None,
    "authors": [],
    "kinds": [],
    "tags": [],
    "source_url": None,
    "version": None,
    "added": None,
    "has_pdf": False,
    "has_md": False,
    "has_json": False,
    "has_assets": False,
    "pdf_sha256": None,
    "parser": None,
    "converted_at": None,
    "retrieved_at": None,
    "visual_verification": False,
    "note": "",
}


def year_of(value):
    match = re.search(r"(\d{4})", value or "")
    return int(match.group(1)) if match else None


def front_fields(path):
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


def kinds_of(fields):
    raw = fields.get("kind", "")
    items = [k for k in re.split(r"[,\s\[\]]+", raw) if k]
    return [k.rstrip("?") for k in items]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="fail if index.json differs from a fresh build")
    args = ap.parse_args()

    meta = stem.load_meta()
    prov = stem.load_provenance()
    previous = {}
    if os.path.exists(stem.index_path()):
        previous = {r["id"]: r for r in stem.load_index().get("papers", []) if r.get("id")}

    stems = {os.path.splitext(f)[0] for d in (stem.pdf_dir(), stem.md_dir(), stem.json_dir())
             if os.path.isdir(d)
             for f in os.listdir(d) if os.path.splitext(f)[1] in {".pdf", ".md", ".json"}}

    papers = []
    for name in stems:
        record = dict(EMPTY)
        fields = front_fields(stem.md_path(name))
        old = previous.get(fields.get("id")) or {}
        pid = fields.get("id") or old.get("id") or name
        meta_entry = meta.get(name) or meta.get(pid) or {}
        prov_entry = prov.get(name) or prov.get(pid) or {}
        conversion = prov_entry.get("conversion") or {}

        record["stem"] = name
        record["id"] = pid
        record["registry"] = fields.get("registry") or old.get("registry") or meta_entry.get("registry")
        record["native_id"] = fields.get("native_id") or old.get("native_id") or meta_entry.get("native_id")
        record["title"] = meta_entry.get("title") or fields.get("title") or old.get("title")
        record["slug_year"] = year_of(meta_entry.get("date") or "")
        record["authors"] = meta_entry.get("authors") or old.get("authors") or []
        record["kinds"] = kinds_of(fields) or old.get("kinds") or []
        record["tags"] = old.get("tags") or []
        record["source_url"] = prov_entry.get("source_url")
        record["version"] = prov_entry.get("version")
        record["added"] = old.get("added") or (prov_entry.get("retrieved_at") or "")[:10] or None
        record["has_pdf"] = os.path.exists(stem.pdf_path(name))
        record["has_md"] = os.path.exists(stem.md_path(name))
        record["has_json"] = os.path.exists(stem.json_path(name))
        record["has_assets"] = os.path.isdir(os.path.join(stem.base(), "assets", name))
        record["pdf_sha256"] = prov_entry.get("pdf_sha256")
        record["parser"] = conversion.get("parser")
        record["converted_at"] = conversion.get("converted_at")
        record["retrieved_at"] = prov_entry.get("retrieved_at")
        record["visual_verification"] = bool(conversion.get("visual_verification"))
        record["note"] = old.get("note") or ""
        papers.append(record)

    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(papers),
        "papers": sorted(papers, key=lambda r: (r["stem"] or "")),
    }
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"

    if args.check:
        current = open(stem.index_path(), encoding="utf-8").read() if os.path.exists(stem.index_path()) else ""
        current = re.sub(r'"generated_at": "[^"]*"', '"generated_at": ""', current)
        fresh = re.sub(r'"generated_at": "[^"]*"', '"generated_at": ""', text)
        if current != fresh:
            raise SystemExit("index.json 与当前文件状态不一致；运行 build_index.py 重新生成。")
        print(f"index.json up to date ({len(papers)} 篇)")
        return

    with open(stem.index_path(), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"index.json: {len(papers)} 篇")


if __name__ == "__main__":
    main()
