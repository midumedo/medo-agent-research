"""Rebuild papers/index.csv from the pdf/ and md/ file names plus the md front matter.

index.csv is a pointer table: `id, name, keywords, revised`. `keywords` is a
judgement column — it is carried over from the previous index.csv (or read from
an md front matter when the index does not exist yet) and is never overwritten
by a rebuild. Titles and abstracts live in the md front matter on purpose.

Usage: build_index.py [--check]
"""

import argparse
import csv
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stem


def front_fields(path):
    """Read the md front matter block, turning `[a, b]` into a list."""
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


def split_multi(value):
    if isinstance(value, list):
        return [v for v in value if v]
    return [v for v in re.split(r"[;,]", value or "") if v]



def render_index(papers):
    """The exact text write_index() produces, for --check comparison."""
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=stem.INDEX_FIELDS, lineterminator="\n")
    writer.writeheader()
    for record in sorted(papers, key=stem.stem_of):
        row = {key: record.get(key) for key in stem.INDEX_FIELDS}
        row["keywords"] = ";".join(record.get("keywords") or [])
        writer.writerow(row)
    return buf.getvalue()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="fail if index.csv differs from a fresh build")
    ap.add_argument("--prune", action="store_true",
                    help="删除索引里磁盘上已不存在的行（默认只增不删）")
    args = ap.parse_args()

    # index.csv 是账本，不是磁盘的投影：md/ 与 pdf/ 都不在本地时它必须原样不动。
    # 行以 `id` 为键、永不以文件名为键——名称允许改，改名不该丢关键词。
    rows = {r["id"]: dict(r) for r in stem.read_index() if r.get("id")}

    stems = {os.path.splitext(f)[0] for d in (stem.pdf_dir(), stem.md_dir())
             if os.path.isdir(d)
             for f in os.listdir(d) if os.path.splitext(f)[1] in {".pdf", ".md"}}

    seen = set()
    for entry_stem in sorted(stems):
        fields = front_fields(stem.md_path(entry_stem))
        ident = fields.get("id") or entry_stem
        seen.add(ident)
        old = rows.get(ident) or {}
        rows[ident] = {
            "id": ident,
            # 文件名是 `<id>.<name>`，名称可以直接从文件名校回。
            "name": (stem.name_from_stem(entry_stem, ident) or old.get("name") or ""),
            # keywords 写在 md 登记块；磁盘上没有 md 时保留账本里的判断。
            "keywords": split_multi(fields.get("keywords")) or old.get("keywords") or [],
            "revised": (stem.normalize_date(fields.get("revised")) or old.get("revised") or ""),
        }

    if args.prune:
        for ident in [i for i in rows if i not in seen]:
            del rows[ident]

    papers = list(rows.values())

    if args.check:
        current = (open(stem.index_path(), encoding="utf-8").read()
                   if os.path.exists(stem.index_path()) else "")
        fresh = render_index(papers)
        if current != fresh:
            raise SystemExit("index.csv 与当前文件状态不一致；运行 build_index.py 重新生成。")
        print(f"index.csv up to date ({len(papers)} 篇)")
        return

    stem.write_index(papers)
    print(f"index.csv: {len(papers)} 篇")


if __name__ == "__main__":
    main()
