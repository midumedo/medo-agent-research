"""导出每个 checkout 的开放度证据——**只导证据，不判定**。

`completeness` 是人或模型的判断，不是脚本的输出。脚本做的是把判据摆出来（构建清单在哪一层、
有没有预编译二进制、有多少 `SKILL.md`、树有多大），再由判定者落值。这与
`sources/papers/_scripts/keywords.py` 的分工一致：脚本不自动生成判断，只导出料。

判据必须落在**变的 native 维度**上：数的是「构建清单在第几层」「二进制文件数」「SKILL.md 个数」
「文件数」，不是字节数。

Usage:
    scan.py                 # 全部有本地目录的行
    scan.py codex gemini-cli
    scan.py --set codex --kind harness --completeness source --keywords a;b;c
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import repos  # noqa: E402

MANIFESTS = ("pyproject.toml", "package.json", "Cargo.toml", "go.mod", "setup.py",
             "pom.xml", "build.gradle", "CMakeLists.txt")
BINARY_EXT = (".exe", ".node", ".dll", ".so", ".dylib", ".wasm")
NOISE_DIRS = {"node_modules", ".git", "__pycache__", ".venv", "dist", "build", ".next"}
MAX_DEPTH = 4


def _walk(base):
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in NOISE_DIRS]
        depth = root[len(base):].count(os.sep)
        if depth >= MAX_DEPTH:
            dirs[:] = []
        for name in files:
            yield root, name


def probe(ident):
    """一个 checkout 的可观测证据。目录不存在时返回 None。"""
    base = os.path.join(repos.BASE, ident)
    if not os.path.isdir(base):
        return None

    root_manifests = [m for m in MANIFESTS if os.path.isfile(os.path.join(base, m))]
    nested = set()
    binaries = 0
    skills = 0
    files = 0
    for root, name in _walk(base):
        files += 1
        rel = os.path.relpath(root, base)
        if name in MANIFESTS and rel != ".":
            nested.add(name)
        if name.lower().endswith(BINARY_EXT):
            binaries += 1
        if name == "SKILL.md":
            skills += 1

    return {
        "id": ident,
        "root_manifests": root_manifests,
        "nested_manifests": sorted(nested),
        "binaries": binaries,
        "skill_md": skills,
        "files": files,
        "top_level": sorted(e for e in os.listdir(base) if not e.startswith("."))[:12],
    }


def show(rows):
    for row in rows:
        print(f"{row['id']}")
        print(f"  根清单     : {'、'.join(row['root_manifests']) or '（无）'}")
        print(f"  深层清单   : {'、'.join(row['nested_manifests']) or '（无）'}")
        print(f"  预编译二进制: {row['binaries']}     SKILL.md: {row['skill_md']}     文件数: {row['files']}")
        print(f"  顶层       : {'、'.join(row['top_level'])}")


def set_values(ident, kind, completeness, keywords):
    rows = repos.read_index()
    target = None
    for row in rows:
        if row["id"] == ident:
            target = row
            break
    if target is None:
        raise SystemExit(f"{ident}: 账本里没有这一行；先 fetch 再 build_index")
    if kind:
        if kind not in repos.KINDS:
            raise SystemExit(f"kind={kind} 不在封闭集 {'/'.join(sorted(repos.KINDS))}")
        target["kind"] = kind
    if completeness:
        if completeness not in repos.COMPLETENESS:
            raise SystemExit(f"completeness={completeness} 不在封闭集 {'/'.join(sorted(repos.COMPLETENESS))}")
        target["completeness"] = completeness
    if keywords:
        words = [w.strip() for w in re.split(r"[;,]", keywords) if w.strip()]
        # 标记类关键词不能被 --set 抹掉：它们是账本自洽的判据，不是普通标签。
        # 但要不要保留要看它现在是否还成立——`no-local-snapshot` 描述的是「没有本地目录」，
        # 抓取成功之后这个标记必须消失，否则账本会声称一份它其实有了的快照不存在。
        for marker in (repos.NO_SNAPSHOT, repos.SNAPSHOT_UNKNOWN):
            if not repos.has_marker(target, marker) or marker in words:
                continue
            if marker == repos.NO_SNAPSHOT and ident in repos.scan_dirs():
                continue
            words.append(marker)
        target["keywords"] = words
    repos.write_index(rows)
    print(f"✓ {ident}: kind={target['kind'] or '-'} completeness={target['completeness'] or '-'} "
          f"keywords={';'.join(target['keywords']) or '-'}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*", help="目录名；省略则扫全部有本地目录的行")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--set", dest="set_id", help="把判定写回 index.csv")
    ap.add_argument("--kind")
    ap.add_argument("--completeness")
    ap.add_argument("--keywords")
    args = ap.parse_args()

    if args.set_id:
        set_values(args.set_id, args.kind, args.completeness, args.keywords)
        return

    ids = args.ids or ([row["id"] for row in repos.read_index()
                        if row["id"] in repos.scan_dirs()] if (args.all or not args.ids) else [])
    rows = [row for row in (probe(i) for i in ids) if row]
    missing = [i for i in ids if not probe(i)]
    show(rows)
    if missing:
        print(f"\n（没有本地目录，跳过：{'、'.join(missing)}）")


if __name__ == "__main__":
    main()
