"""步骤⑥ 反追踪状态 + 完整性对账。

每篇检查 `pdf/md/assets` 是否齐，并检查派生目录是否已被 `.gitignore` 覆盖、
是否还留在 git 索引里。`--check` 任一项不满足就非零退出（交付门）；`--sync`
幂等地把 `.gitignore` 与 git 索引对齐（`git rm --cached`，只动索引、不动磁盘），
让「取消追踪」从一次性手工动作变成一个可重复的状态更新。

Usage:
    status.py            # 报告（人读）
    status.py --check    # 缺料或反追踪未生效 → 非零退出
    status.py --sync     # 幂等：补 .gitignore 条目 + 把派生文件移出索引
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import stem  # noqa: E402
import pipeline  # noqa: E402

DERIVED = ("pdf", "md", "assets", "logs")


def repo_root():
    """The repository root, derived from stem.BASE so tests can move the library."""
    return Path(stem.BASE).resolve().parents[1]


def derived_paths():
    return [f"sources/papers/{name}" for name in DERIVED]


def ignore_lines():
    return [f"/sources/papers/{name}/" for name in DERIVED]


def tracked_derived():
    """Files still tracked under the derived dirs; [] means untracking is in effect.

    Returns None when git cannot be asked at all (not a checkout, no git).
    """
    try:
        result = subprocess.run(["git", "ls-files", "--"] + derived_paths(),
                                cwd=str(repo_root()), capture_output=True, text=True, check=True)
    except Exception:
        return None
    return [line for line in result.stdout.splitlines() if line.strip()]


def ensure_gitignore():
    """Add any missing `/sources/papers/<derived>/` line. Returns the lines added."""
    path = repo_root() / ".gitignore"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    lines = text.splitlines()
    added = []
    for line in ignore_lines():
        if line not in lines:
            lines.append(line)
            added.append(line)
    if added:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return added


def untrack():
    """`git rm --cached` the derived dirs; index only, disk untouched."""
    result = subprocess.run(["git", "rm", "-r", "--cached", "--quiet", "--"] + derived_paths(),
                            cwd=str(repo_root()), capture_output=True, text=True)
    message = (result.stdout + result.stderr).strip()
    return result.returncode, message


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="缺料或反追踪未生效则非零退出")
    ap.add_argument("--sync", action="store_true", help="幂等地更新 .gitignore 与 git 索引")
    args = ap.parse_args()

    rows = stem.read_index()
    problems = []
    for row in rows:
        name = stem.stem_of(row)
        if not os.path.exists(stem.pdf_path(name)):
            problems.append(f"{row['id']}: 缺 PDF")
        absent = pipeline.missing_images(name)
        if absent is None:
            problems.append(f"{row['id']}: 缺 md")
        elif absent:
            problems.append(f"{row['id']}: 缺 {len(absent)} 张图")

    tracked = tracked_derived()
    if tracked:
        problems.append(f"{len(tracked)} 个派生文件仍在 git 索引里（例 {tracked[0]}）")

    for problem in problems:
        print(f"✗ {problem}")
    if not problems:
        print(f"✓ {len(rows)} 篇齐备，派生目录均未被跟踪")

    if args.sync:
        for line in ensure_gitignore():
            print(f"+ .gitignore: {line}")
        code, message = untrack()
        if code != 0 and "did not match" not in message and "pathspec" not in message:
            print(f"⚠ git rm --cached 返回 {code}：{message}")
        print("--sync 完成（反追踪状态已更新）")

    if args.check and problems:
        raise SystemExit(f"有 {len(problems)} 项不满足")


if __name__ == "__main__":
    main()
