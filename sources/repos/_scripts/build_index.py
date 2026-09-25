"""以 index.csv 为账本重建它：身份列派生，判断列原样保留。

账本语义（与 `sources/papers/_scripts/build_index.py` 一致）：
行以 `id` 为键，**只增不删**。一个 checkout 被移走，那一行仍然留着——它记的是
「我们曾在某个 sha 上看过这个仓库」，不是「磁盘现在有什么」。`--prune` 才删除，
而且带 `no-local-snapshot` 标记的行（本来就声明没有本地快照：Claude Code 的 npm 产物、
抓取失败的 goose、尚未抓到的 ZCode）永远不删。

身份列的来源优先级：旧账本 > `_commits.json` > 空。判断列（kind/keywords/completeness）
只从旧账本搬，**永不**由本脚本生成。

Usage:
    build_index.py            # 重建 index.csv
    build_index.py --check    # 与重建结果逐字节比对，不一致则非零退出
    build_index.py --prune    # 一并删除磁盘上已消失的行
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import repos  # noqa: E402


def derive(rows, commits):
    """以旧账本为底，用磁盘与 `_commits.json` 补齐身份列。"""
    by_id = {row["id"]: dict(row) for row in rows if row.get("id")}
    dirs = set(repos.scan_dirs())

    for entry in sorted(dirs):
        old = by_id.get(entry) or {}
        meta = commits.get(entry) or {}
        by_id[entry] = {
            "id": entry,
            # `repo` 是身份列，以抓取台账为准：仓库搬家时（如 block/goose → aaif-goose/goose）
            # 上游 slug 会变，旧行里那份只是缓存。台账里没有该条时（非 git 快照对象）才用旧值。
            "repo": meta.get("slug") or old.get("repo") or "",
            "keywords": list(old.get("keywords") or []),
            "kind": old.get("kind") or "",
            "completeness": old.get("completeness") or "",
            # 有指纹就用，没有就留空——由 `snapshot-unknown` 标记说明「没记」，不猜当前 sha。
            # 无论来自旧行还是 `_commits.json`，账本一律只存前 12 位：完整 sha 留在
            # `_commits.json`，账本要的是能一眼认出的版本号。
            "snapshot": (old.get("snapshot") or meta.get("sha") or "")[:12],
        }

    # 历史快照行（`<id>@<sha12>`）与非 checkout 行：原样保留，只把 repo/snapshot/判断列补全。
    for ident, row in by_id.items():
        base, sha = repos.split_id(ident)
        if ident == base and base in dirs:
            continue
        if not row.get("repo"):
            row["repo"] = (commits.get(base) or {}).get("slug") or ""
        if not row.get("snapshot") and sha:
            row["snapshot"] = sha
        # 历史快照是新行、没有旧行可继承，判断列从当前快照继承——同一个仓库的开放度
        # 不会因为「这是旧的哪一份」而改变。
        current = by_id.get(base)
        if current:
            for field in repos.JUDGEMENT_FIELDS:
                if not row.get(field):
                    row[field] = current.get(field) or row.get(field)
    return list(by_id.values())


def prune(rows):
    """删掉磁盘上已消失、且没有声明「本来就没有本地快照」的行。"""
    dirs = set(repos.scan_dirs())
    kept, dropped = [], []
    for row in rows:
        base, _ = repos.split_id(row.get("id") or "")
        if base in dirs or repos.has_marker(row, repos.NO_SNAPSHOT):
            kept.append(row)
        else:
            dropped.append(row["id"])
    return kept, dropped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="与重建结果逐字节比对，不一致则非零退出")
    ap.add_argument("--prune", action="store_true",
                    help="删除磁盘上已消失的行（带 no-local-snapshot 的永不删）")
    ap.add_argument("--drop", action="append", default=[], metavar="ID",
                    help="显式删除某一行（例：待抓对象抓到了，占位的 unknown 行该退场）")
    args = ap.parse_args()

    rows = derive(repos.read_index(), repos.read_commits())
    dropped = []
    if args.drop:
        wanted = set(args.drop)
        dropped = [r["id"] for r in rows if r["id"] in wanted]
        rows = [r for r in rows if r["id"] not in wanted]
    if args.prune:
        rows, dropped = prune(rows)

    if args.check:
        current = (open(repos.index_path(), encoding="utf-8").read()
                   if os.path.exists(repos.index_path()) else "")
        if current != repos.render_index(rows):
            raise SystemExit("index.csv 与当前账本状态不一致；运行 build_index.py 重建。")
        print(f"index.csv up to date ({len(rows)} 行)")
        return

    repos.write_index(rows)
    for ident in dropped:
        print(f"- 删除行 {ident}")
    problems = repos.validate(rows)
    for problem in problems:
        print(f"⚠ {problem}")
    print(f"index.csv: {len(rows)} 行" + (f"，{len(problems)} 项待修" if problems else "，自洽"))


if __name__ == "__main__":
    main()
