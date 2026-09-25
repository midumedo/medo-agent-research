"""交付门：账本自洽 + 反追踪生效。

账本自洽（`repos.validate`）：每行 `id` 唯一；`kind`/`completeness` 落在封闭集内；有本地目录的
行必须有 `snapshot` 或 `snapshot-unknown` 标记；没有本地目录的行必须有 `no-local-snapshot` 标记。

反追踪生效：`git ls-files sources/repos` 只允许列出元数据层那几类；任何一个第三方
checkout 的文件出现在索引里就算失败。

Usage:
    status.py            # 人读的报告
    status.py --check    # 任一项不满足即非零退出
    status.py --sync     # 幂等：补齐两处 .gitignore 里缺的条目
"""

import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import repos  # noqa: E402

ROOT = os.path.dirname(repos.BASE)          # 仓库根（sources/ 的上一级）
REPO_ROOT = os.path.dirname(ROOT)
TRACKED_PREFIXES = ("sources/repos/.gitignore", "sources/repos/index.csv",
                    "sources/repos/_commits.json", "sources/repos/CHANGELOG.md",
                    "sources/repos/AGENTS.md", "sources/repos/_scripts/")

ROOT_IGNORE_WANTED = "/sources/repos/*"
INNER_IGNORE_WANTED = ["!index.csv", "!_commits.json", "!CHANGELOG.md", "!AGENTS.md",
                       "!_scripts/", "!_scripts/**", "__pycache__/"]


def tracked_files():
    """git 索引里的 sources/repos 路径；git 不可用时返回 None。"""
    try:
        result = subprocess.run(["git", "ls-files", "--", "sources/repos"],
                                cwd=REPO_ROOT, capture_output=True, text=True, check=True)
    except Exception:
        return None
    return [line for line in result.stdout.splitlines() if line.strip()]


def anti_tracking_problems():
    tracked = tracked_files()
    if tracked is None:
        return None
    stray = [p for p in tracked if not p.startswith(TRACKED_PREFIXES)]
    return stray


def ensure_lines(path, wanted):
    """幂等：把缺的行补到 `path` 末尾。返回补了哪些。"""
    text = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    lines = text.splitlines()
    added = [w for w in wanted if w not in lines]
    if added:
        if text and not text.endswith("\n"):
            lines.append("")
        lines.extend(added)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(lines) + "\n")
    return added


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="任一项不满足则非零退出")
    ap.add_argument("--sync", action="store_true", help="幂等补齐两处 .gitignore")
    args = ap.parse_args()

    problems = []

    rows = repos.read_index()
    if not rows:
        problems.append("index.csv 不存在或为空——先跑 build_index.py")
    problems.extend(repos.validate(rows))

    dirs = set(repos.scan_dirs())
    # 逐目录比对**完整目录名**：历史快照的目录名就是 `<id>@<sha12>`，账本里也有一行同名。
    # 早先这里把行 id 压成 base 再比，于是每个历史快照目录都被误报成「账本里没有行」。
    row_ids = {row["id"] for row in rows}
    for missing in sorted(dirs - row_ids):
        problems.append(f"{missing}: 磁盘上有 checkout，账本里没有行")
    for row in rows:
        ident = row["id"]
        if ident in dirs or repos.has_marker(row, repos.NO_SNAPSHOT):
            continue
        problems.append(f"{ident}: 账本里有行，磁盘上没有对应目录，也没有 {repos.NO_SNAPSHOT} 标记")

    stray = anti_tracking_problems()
    if stray is None:
        problems.append("问不到 git 索引（不是 checkout？）")
    elif stray:
        problems.append(f"{len(stray)} 个第三方文件被跟踪了（例 {stray[0]}）")

    for problem in problems:
        print(f"✗ {problem}")
    if not problems:
        print(f"✓ {len(rows)} 行账本自洽；{len(dirs)} 个 checkout 在盘；反追踪生效（"
              f"{len(tracked_files() or [])} 个文件在索引里，全部属元数据层）")

    if args.sync:
        for path, wanted in ((os.path.join(REPO_ROOT, ".gitignore"), [ROOT_IGNORE_WANTED]),
                             (os.path.join(repos.BASE, ".gitignore"), INNER_IGNORE_WANTED)):
            for line in ensure_lines(path, wanted):
                print(f"+ {os.path.relpath(path, REPO_ROOT)}: {line}")
        print("--sync 完成")

    if args.check and problems:
        raise SystemExit(f"有 {len(problems)} 项不满足")


if __name__ == "__main__":
    main()
