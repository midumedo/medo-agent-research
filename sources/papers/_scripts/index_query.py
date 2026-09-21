"""Query papers/index.json with SQL.

The library keeps JSON as the versioned source of truth (diffable, greppable);
this script loads it into an in-memory SQLite database so you can ask real
questions without hand-writing jq. Use --emit to materialise a .sql file.

Usage:
    index_query.py                                   # summary
    index_query.py --sql "SELECT stem, title FROM papers WHERE has_json = 0"
    index_query.py --sql "SELECT p.stem FROM papers p JOIN paper_kinds k
                          ON p.stem = k.stem WHERE k.kind = 'benchmark'"
    index_query.py --emit index.sql
"""

import argparse
import json
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stem

COLUMNS = [
    "stem", "id", "registry", "native_id", "title", "slug_year", "version",
    "kinds_csv", "tags_csv", "source_url", "added",
    "has_pdf", "has_md", "has_json", "has_assets",
    "pdf_sha256", "parser", "converted_at", "visual_verification", "note",
]

SCHEMA = """CREATE TABLE papers (
  stem TEXT PRIMARY KEY,
  id TEXT UNIQUE,
  registry TEXT,
  native_id TEXT,
  title TEXT,
  slug_year INTEGER,
  version TEXT,
  kinds_csv TEXT,
  tags_csv TEXT,
  source_url TEXT,
  added TEXT,
  has_pdf INTEGER,
  has_md INTEGER,
  has_json INTEGER,
  has_assets INTEGER,
  pdf_sha256 TEXT,
  parser TEXT,
  converted_at TEXT,
  visual_verification INTEGER,
  note TEXT
);
CREATE TABLE paper_kinds (stem TEXT, kind TEXT);
CREATE TABLE paper_tags (stem TEXT, tag TEXT);
"""


def rows():
    out = []
    for record in stem.records():
        row = {key: record.get(key) for key in COLUMNS}
        row["kinds_csv"] = ",".join(record.get("kinds") or [])
        row["tags_csv"] = ",".join(record.get("tags") or [])
        row["has_pdf"] = int(bool(record.get("has_pdf")))
        row["has_md"] = int(bool(record.get("has_md")))
        row["has_json"] = int(bool(record.get("has_json")))
        row["has_assets"] = int(bool(record.get("has_assets")))
        row["visual_verification"] = int(bool(record.get("visual_verification")))
        out.append(row)
    return out


def connect():
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.executescript(SCHEMA)
    data = rows()
    connection.executemany(
        "INSERT INTO papers VALUES (%s)" % ",".join(":" + c for c in COLUMNS), data)
    connection.executemany(
        "INSERT INTO paper_kinds VALUES (?, ?)",
        [(r["stem"], k) for r in data for k in (r["kinds_csv"].split(",") if r["kinds_csv"] else [])])
    connection.executemany(
        "INSERT INTO paper_tags VALUES (?, ?)",
        [(r["stem"], t) for r in data for t in (r["tags_csv"].split(",") if r["tags_csv"] else [])])
    return connection


def summary(connection):
    total = connection.execute("SELECT COUNT(*) FROM papers").fetchone()[0]
    print(f"papers: {total}")
    for kind, count in connection.execute(
            "SELECT kind, COUNT(*) c FROM paper_kinds GROUP BY kind ORDER BY c DESC"):
        print(f"  {kind}: {count}")
    for label, sql in (
            ("缺 md", "SELECT COUNT(*) FROM papers WHERE has_md = 0"),
            ("缺 json", "SELECT COUNT(*) FROM papers WHERE has_json = 0"),
            ("版本未知", "SELECT COUNT(*) FROM papers WHERE version IS NULL"),
            ("未经视觉核验", "SELECT COUNT(*) FROM papers WHERE visual_verification = 0"),
    ):
        print(f"  {label}: {connection.execute(sql).fetchone()[0]}")


def emit(path):
    data = rows()
    lines = [SCHEMA]
    for row in data:
        values = ",".join("NULL" if row[c] is None else "'%s'" % str(row[c]).replace("'", "''")
                          for c in COLUMNS)
        lines.append("INSERT INTO papers VALUES (%s);" % values)
    for row in data:
        for kind in (row["kinds_csv"].split(",") if row["kinds_csv"] else []):
            lines.append(f"INSERT INTO paper_kinds VALUES ('{row['stem']}', '{kind}');")
        for tag in (row["tags_csv"].split(",") if row["tags_csv"] else []):
            lines.append(f"INSERT INTO paper_tags VALUES ('{row['stem']}', '{tag}');")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print(f"{path}: {len(data)} 篇")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sql", default=None)
    ap.add_argument("--emit", default=None, metavar="FILE")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    connection = connect()
    if args.emit:
        emit(args.emit)
        return
    if not args.sql:
        summary(connection)
        return
    cursor = connection.execute(args.sql)
    records = [dict(r) for r in cursor.fetchall()]
    if args.json:
        print(json.dumps(records, ensure_ascii=False, indent=2))
        return
    if not records:
        print("(no rows)")
        return
    widths = [max(len(str(k)) for k in r) for r in zip(*[[str(v) for v in row] for row in records])]
    keys = list(records[0])
    widths = [max(len(k), w) for k, w in zip(keys, widths)]
    print(" | ".join(k.ljust(w) for k, w in zip(keys, widths)))
    print("-+-".join("-" * w for w in widths))
    for row in records:
        print(" | ".join(str(row[k]).ljust(w) for k, w in zip(keys, widths)))


if __name__ == "__main__":
    main()
