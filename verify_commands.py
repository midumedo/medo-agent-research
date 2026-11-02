#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_commands.py -- 保鲜校验器：把上下文文件里的可执行断言抽出来真跑一遍。

这是交付到你仓库里的脚本，不是技能的内部零件
  技能只负责把它复制进来、交付当天跑一次，并给一段 CI 接线文本。
  之后它归你维护，技能不改它。你可以直接删掉它。

它做什么
  读目标文件里 info string 含 agents-verify 的围栏代码块，把块内每个非空、
  非 # 开头的行当作一条命令，在仓库根下顺序执行，报告通过 / 失败。

它不做什么
  不持有命令清单。命令只存在于目标文件里——若把命令抄进脚本，就等于给文件造了
  第二份真相源，两者必然漂移，那样它不是保鲜器，而是新的腐化源。
  不写任何文件、不改目标文件、不联网、不装依赖。

判定（重要）
  抽到 0 条命令 -> exit 2 并明说"没有可执行断言：这不是通过，是没测"。
  一个会静默通过的保鲜脚本，比没有保鲜脚本更糟：它把"没人测"伪装成"测过了"。

退出码
  0  全部通过（且至少跑了 1 条断言）
  1  有命令失败
  2  用法错，或抽到 0 条断言
  3  环境缺失（shell 不可用、目标文件读不到、--file 不存在）

跨平台
  Windows 上 shell=True 走 cmd.exe：`&&`、`||`、`%VAR%` 可用，`$(...)`、`export`、
  `&&` 之外的 POSIX 语法大多不可用；POSIX-only 的命令在这里会失败并按 1 报出，
  不会假装通过。macOS / Linux 上走 /bin/sh 语义。
  因此 agents-verify 块里的命令最好只用你的项目实际运行环境支持的那一套。

用法
  python verify_commands.py                 # 在仓库根跑，默认读 AGENTS.md
  python verify_commands.py -C . --file CLAUDE.md
  python verify_commands.py --list-only     # 只列命令不执行
  python verify_commands.py --json          # 机器可读
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

FENCE_TAG = "agents-verify"
EXIT_OK = 0
EXIT_FAILED = 1
EXIT_USAGE = 2
EXIT_ENV = 3


def extract_commands(text):
    """从 info string 含 agents-verify 的围栏块里抽命令，保持文件顺序。"""
    cmds = []
    inside = False
    for raw in text.split("\n"):
        line = raw.rstrip()
        stripped = line.strip()
        if stripped.startswith("```"):
            if inside:
                inside = False
                continue
            info = stripped[3:].strip()
            inside = FENCE_TAG in info
            continue
        if not inside:
            continue
        if not stripped or stripped.startswith("#"):
            continue
        cmds.append(stripped)
    return cmds


def shell_available():
    if os.name == "nt":
        return bool(os.environ.get("ComSpec") or shutil.which("cmd"))
    return bool(shutil.which("sh") or os.path.exists("/bin/sh"))


def git_dirty_count(repo):
    """返回 (count, error)。git 不可用 / 非仓库 -> (None, 原因)。"""
    git = shutil.which("git")
    if not git:
        return None, "git 不可用，未检查工作区"
    try:
        out = subprocess.run([git, "-C", str(repo), "status", "--porcelain"],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
    except Exception as exc:
        return None, "git 调用失败，未检查工作区: %s" % exc
    if out.returncode != 0:
        return None, "不是 git 仓库，未检查工作区"
    return len([ln for ln in out.stdout.decode("utf-8", "replace").split("\n") if ln.strip()]), None


def run_one(cmd, repo, timeout):
    started = time.monotonic()
    try:
        proc = subprocess.run(cmd, shell=True, cwd=str(repo), timeout=timeout,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        code = proc.returncode
        output = proc.stdout.decode("utf-8", "replace")
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        code = -1
        out = exc.output or b""
        output = out.decode("utf-8", "replace") if isinstance(out, bytes) else str(out)
        timed_out = True
    except Exception as exc:
        code = -1
        output = "执行失败：%s" % exc
        timed_out = False
    duration = time.monotonic() - started
    return {
        "command": cmd,
        "exit": code,
        "duration_s": round(duration, 2),
        "timed_out": timed_out,
        "tail": output.strip().split("\n")[-20:],
    }


def main(argv):
    ap = argparse.ArgumentParser(
        prog="verify_commands.py",
        description=("从目标文件的 agents-verify 围栏里抽命令并真跑。"
                     "0 条断言不是通过，是没测（exit 2）。"
                     "退出码：0 全过 / 1 有失败 / 2 用法错或 0 断言 / 3 环境缺失。"))
    ap.add_argument("-C", "--repo", default=".", help="命令的工作目录（默认当前目录）")
    ap.add_argument("--file", default="AGENTS.md", help="含 agents-verify 围栏的目标文件")
    ap.add_argument("--timeout", type=float, default=600.0, help="单条命令超时秒数")
    ap.add_argument("--fail-fast", action="store_true", dest="fail_fast")
    ap.add_argument("--list-only", action="store_true", dest="list_only")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if sys.version_info < (3, 9):
        sys.stderr.write("需要 Python 3.9+（本脚本用了 pathlib 与 subprocess.run 的 "
                         "3.9 语义），当前 %s。\n修法：升级解释器，或换用仓库里其它"
                         "已安装的 python3。\n" % sys.version.split()[0])
        return EXIT_ENV

    repo = Path(args.repo).expanduser().resolve()
    if not repo.is_dir():
        sys.stderr.write("仓库目录不存在：%s\n修法：用 -C 指定仓库根目录。\n" % repo.as_posix())
        return EXIT_ENV
    target = Path(args.file)
    if not target.is_absolute():
        target = repo / target
    target = target.resolve()
    if not target.is_file():
        sys.stderr.write("目标文件不存在：%s\n修法：用 --file 指定含 agents-verify 围栏的文件。\n"
                         % target.as_posix())
        return EXIT_ENV
    try:
        text = target.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError) as exc:
        sys.stderr.write("读不到目标文件：%s\n修法：确认文件是 UTF-8 且有读权限。\n" % exc)
        return EXIT_ENV

    cmds = extract_commands(text)
    if not cmds:
        sys.stderr.write(
            "没有可执行断言：这不是通过，是没测。\n"
            "目标文件 %s 里找不到 info string 含 %s 的围栏块。\n"
            "修法：在验证节写一个 ```%s 代码块，一行一条可执行命令，"
            "# 开头为注释。\n" % (target.name, FENCE_TAG, FENCE_TAG))
        return EXIT_USAGE

    if args.list_only:
        if args.json:
            sys.stdout.write(json.dumps({"assertions": len(cmds), "commands": cmds},
                                        ensure_ascii=False, indent=2) + "\n")
        else:
            sys.stdout.write("共 %d 条断言（--list-only，未执行）：\n" % len(cmds))
            for c in cmds:
                sys.stdout.write("  " + c + "\n")
        return EXIT_OK

    if not shell_available():
        sys.stderr.write("找不到可用 shell（Windows 需 ComSpec/cmd，其他平台需 sh）。\n"
                         "修法：在能起 shell 的环境里跑，或先修 PATH。\n")
        return EXIT_ENV

    dirty_before, dirty_note = git_dirty_count(repo)
    results = []
    failed = 0
    for cmd in cmds:
        r = run_one(cmd, repo, args.timeout)
        results.append(r)
        if r["exit"] != 0:
            failed += 1
            if args.fail_fast:
                break
    dirty_after, _note = git_dirty_count(repo)
    changed = (dirty_before is not None and dirty_after is not None and dirty_after != dirty_before)

    if args.json:
        sys.stdout.write(json.dumps({
            "assertions": len(cmds),
            "executed": len(results),
            "failed": failed,
            "workspace_changed": changed,
            "workspace_note": dirty_note,
            "results": results,
        }, ensure_ascii=False, indent=2) + "\n")
    else:
        for r in results:
            mark = "PASS" if r["exit"] == 0 else "FAIL"
            sys.stdout.write("[%s] exit=%s %5.2fs %s\n"
                             % (mark, r["exit"], r["duration_s"], r["command"]))
            if r["exit"] != 0:
                for ln in r["tail"]:
                    sys.stdout.write("    | " + ln + "\n")
        sys.stdout.write("\n%d/%d 通过" % (len(results) - failed, len(results)))
        if len(results) < len(cmds):
            sys.stdout.write("（--fail-fast 提前停止，剩余 %d 条未跑）" % (len(cmds) - len(results)))
        sys.stdout.write("\n")
        if changed:
            sys.stdout.write("注意：本次执行改动了工作区（git status 行数 %s -> %s）。"
                             "建议在干净分支上跑。\n" % (dirty_before, dirty_after))
        elif dirty_note:
            sys.stdout.write("提示：%s。\n" % dirty_note)
        sys.stdout.write("覆盖范围：只覆盖文件里的可执行断言，不覆盖描述性规则。\n")

    return EXIT_OK if failed == 0 else EXIT_FAILED


# ------------------------------------------------------------------ selftest --

SELFTEST_WITH_ASSERT = """# AGENTS.md

## 验证

```agents-verify
echo verify-ok
# 这是注释，不算断言
```

其他命令块不算断言：

```bash
echo not-an-assertion
```
"""

SELFTEST_NO_ASSERT = """# AGENTS.md

只有描述，没有可执行断言。

```bash
echo not-an-assertion
```
"""


def _quiet(argv):
    import contextlib
    import io as _io

    buf_out, buf_err = _io.StringIO(), _io.StringIO()
    with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
        code = main(argv)
    return code, buf_out.getvalue() + buf_err.getvalue()


def selftest():
    fails = []

    def want(cond, msg):
        if not cond:
            fails.append(msg)

    with tempfile.TemporaryDirectory() as td:
        repo = Path(td)
        ok_file = repo / "AGENTS.md"
        ok_file.write_text(SELFTEST_WITH_ASSERT, encoding="utf-8")
        no_file = repo / "CLAUDE.md"
        no_file.write_text(SELFTEST_NO_ASSERT, encoding="utf-8")

        cmds = extract_commands(SELFTEST_WITH_ASSERT)
        want(cmds == ["echo verify-ok"], "只应抽出 1 条断言，实际 %s" % cmds)
        want(extract_commands(SELFTEST_NO_ASSERT) == [], "无 agents-verify 块应抽到 0 条")

        listing, _out = _quiet(["-C", str(repo), "--list-only"])
        want(listing == EXIT_OK, "--list-only 应 exit 0")
        lst, out = _quiet(["-C", str(repo), "--list-only", "--json"])
        want('"assertions": 1' in out, "--list-only --json 应报 1 条断言")

        code, out = _quiet(["-C", str(repo), "--file", "AGENTS.md"])
        want(code == EXIT_OK, "有 1 条通过的断言应 exit 0，实际 %d" % code)
        want("[PASS]" in out, "人读输出应有 [PASS] 行")

        code, out = _quiet(["-C", str(repo), "--file", "CLAUDE.md"])
        want(code == EXIT_USAGE, "0 断言应 exit 2，实际 %d" % code)
        want("这不是通过，是没测" in out, "0 断言时必须明说这不是通过")

        code, out = _quiet(["-C", str(repo), "--file", "nope.md"])
        want(code == EXIT_ENV, "目标文件不存在应 exit 3，实际 %d" % code)

        # 失败命令必须按 1 报出，不假装通过
        bad = repo / "BAD.md"
        bad.write_text("# x\n\n```agents-verify\nexit 7\n```\n", encoding="utf-8")
        code, out = _quiet(["-C", str(repo), "--file", "BAD.md"])
        want(code == EXIT_FAILED, "失败命令应 exit 1，实际 %d" % code)
        want("[FAIL]" in out, "失败时应输出 [FAIL]")

        # 脚本自身不改目标文件
        before = ok_file.read_text(encoding="utf-8")
        _quiet(["-C", str(repo), "--file", "AGENTS.md"])
        want(ok_file.read_text(encoding="utf-8") == before, "脚本不应改动目标文件")

    if fails:
        for m in fails:
            sys.stderr.write("SELFTEST FAIL: " + m + "\n")
        return 1
    sys.stdout.write("verify_commands selftest: OK (12 项断言：抽取 / 0 断言 exit 2 / "
                     "通过 exit 0 / 失败 exit 1 / 缺文件 exit 3 / 不改目标文件)\n")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(errors="replace")  # type: ignore[attr-defined]
    except Exception:
        pass
    sys.exit(main(sys.argv[1:]))
