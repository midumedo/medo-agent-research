"""编排：把六步串成两条常用路径，不重复实现任何一步。

    pipeline.py --check     重建比对 + 交付门（交付前跑这个）
    pipeline.py --all       按账本更新全部快照，然后重建账本
    pipeline.py --new <owner/name>   抓一个新仓库，并把它并进账本

每一步都是独立可跑的脚本，这里只负责顺序与失败即停——所以任何一步都能单独调试。
"""

import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def run(script, *args):
    cmd = [sys.executable, os.path.join(HERE, script), *args]
    print(f"\n$ {' '.join(['python', os.path.join('sources/repos/_scripts', script), *args])}")
    return subprocess.run(cmd).returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--new", metavar="OWNER/NAME")
    args = ap.parse_args()

    if args.check:
        code = run("build_index.py", "--check")
        code |= run("status.py", "--check")
        raise SystemExit(code)

    if args.all:
        if run("fetch.py", "--all", "--no-changelog") != 0:
            raise SystemExit("抓取有失败项，未继续")
        run("build_index.py")

    if args.new:
        if run("fetch.py", args.new) != 0:
            raise SystemExit("抓取失败，未并进账本")
        run("build_index.py")

    if not (args.check or args.all or args.new):
        ap.error("选一个：--check / --all / --new")


if __name__ == "__main__":
    main()
