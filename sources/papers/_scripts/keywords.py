"""步骤⑤ 打词：只由 abstract 判词，结果回写 index.csv。

脚本**不自动生成**关键词——它只负责搬运：`--missing` 把「缺关键词」的篇目导成
`id \t name \t abstract`，模型只读这一行就够，不必读全文（省 token）；模型选完词
后用 `--set` 回写。摘要不在时回退标题，仍不足就留空，**绝不推测**。

Usage:
    keywords.py --missing            # 导出缺词的篇目（id / name / abstract）
    keywords.py --set <id> a;b;c     # 回写 keywords（只改命中行）
    keywords.py --list               # 列出全库的 id 与现有 keywords
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stem  # noqa: E402


def abstract_of(record):
    """The md register's abstract, or None. Never invents one."""
    fields = stem.read_front_matter(stem.stem_of(record))
    return fields.get("abstract") or None


def split_words(value):
    return [w.strip() for w in re.split(r"[;,]", value or "") if w.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--missing", action="store_true", help="导出缺关键词的篇目")
    ap.add_argument("--list", action="store_true", help="列出全库 id 与 keywords")
    ap.add_argument("--set", nargs=2, metavar=("ID", "WORDS"),
                    help="回写某篇的 keywords，如 --set arxiv-1v1 memory;agent")
    args = ap.parse_args()

    rows = stem.read_index()

    if args.set:
        ident, words = args.set
        wanted = split_words(words)
        hit = False
        for row in rows:
            if row["id"] == ident:
                row["keywords"] = wanted
                hit = True
        if not hit:
            raise SystemExit(f"[{ident}] 不在 index.csv 里，未改动任何行。")
        stem.write_index(rows)
        print(f"[{ident}] keywords = {';'.join(wanted)}")
        return

    if args.list:
        for row in rows:
            print(f"{row['id']}\t{row['name']}\t{';'.join(row['keywords']) or '-'}")
        return

    # 默认即 --missing：缺词的篇目 + 判词素材（摘要，或回退标题）
    for row in rows:
        if row["keywords"]:
            continue
        abstract = abstract_of(row)
        if abstract:
            print(f"{row['id']}\t{row['name']}\t{abstract}")
        else:
            print(f"{row['id']}\t{row['name']}\t(无摘要，回退标题：{row['name']})")


if __name__ == "__main__":
    main()
