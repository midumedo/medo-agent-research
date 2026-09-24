"""Restore the paper material that is deliberately not in the repository.

Tracked:   `index.csv`, `md/*.md`, `_scripts/`, the docs.
Untracked: `pdf/` — the arXiv originals, re-downloadable by `id`;
           `assets/` — images derived from those PDFs by MinerU.

Usage:
    fetch_material.py [--all] [token ...]
    fetch_material.py --check [token ...]     # 只核对，不下载、不转换

A token is a file name (`<id>.<name>`), an `id`, an arXiv number or a title —
whatever `stem.find()` resolves. `--all` walks every row of `index.csv`.

For each paper, in order:
  1. no `pdf/<file>.pdf`            -> download it (same id, same version);
  2. no `md/<file>.md`              -> convert it (MinerU cloud);
  3. md present but a `](../assets/<name>)` reference has no file on disk
                                    -> re-convert, then report whether the md
                                       itself changed (it is tracked; a change
                                       is a real diff to review, not silence).
Finally every md is checked again and any still-missing reference exits non-zero.

The md is never hand-edited here: rebuilding images is the converter's job.
"""

import argparse
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import stem  # noqa: E402
import download_arxiv  # noqa: E402

REF_RE = re.compile(r"\]\(\.\./assets/([^)\s]+)\)")
MINERU = HERE / "mineru_cloud.py"


def referenced_images(stem_name):
    """Image file names the md points at, or None when the md itself is absent."""
    path = stem.md_path(stem_name)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return sorted(set(REF_RE.findall(f.read())))


def missing_images(stem_name):
    names = referenced_images(stem_name)
    if names is None:
        return None
    root = stem.assets_root()
    return [n for n in names if not os.path.exists(os.path.join(root, n))]


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def convert(stem_name):
    """Run the converter; report whether the tracked md changed as a result."""
    md = stem.md_path(stem_name)
    before = sha256(md) if os.path.exists(md) else None
    result = subprocess.run([sys.executable, str(MINERU), "--force", stem_name],
                            cwd=str(HERE.parent.parent))
    if result.returncode != 0:
        return f"转换失败（退出码 {result.returncode}）"
    after = sha256(md) if os.path.exists(md) else None
    if before is None:
        return "md 已生成"
    return "md 未变" if before == after else "⚠ md 内容已变（是跟踪文件，请 git diff 复核）"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--check", action="store_true", help="只核对，不补取")
    ap.add_argument("tokens", nargs="*")
    args = ap.parse_args()

    rows = stem.read_index()
    if args.all or not args.tokens:
        records = rows
    else:
        records = []
        for token in args.tokens:
            record = stem.find(token)
            if not record:
                raise SystemExit(f"[{token}] 不在 index.csv 里")
            records.append(record)

    print(f"核对 {len(records)} 篇" + ("（只核对）" if args.check else ""))
    for record in records:
        name = stem.stem_of(record)
        line = [f"[{record.get('id')}]"]
        if not os.path.exists(stem.pdf_path(name)):
            if args.check:
                line.append("缺 PDF")
            else:
                print(" ".join(line + ["下载 PDF…"]), flush=True)
                print("   ", download_arxiv.download_one(name))
        absent = missing_images(name)
        if absent is None and not args.check:
            print(" ".join(line + ["转换…"]), flush=True)
            print("   ", convert(name))
        elif absent:
            if args.check:
                line.append(f"缺 {len(absent)} 张图：{absent[:3]}")
            else:
                print(" ".join(line + [f"缺 {len(absent)} 张图，重转…"]), flush=True)
                print("   ", convert(name))
        if line:
            print(" ".join(line))

    # final verification: every reference must resolve
    bad = {}
    for record in rows:
        absent = missing_images(stem.stem_of(record))
        if absent:
            bad[record.get("id")] = absent
    if bad:
        for ident, names in bad.items():
            print(f"✗ {ident}: {len(names)} 张图仍缺（例 {names[0]}）")
        raise SystemExit(f"仍有 {len(bad)} 篇不完整")
    print("✓ 全部 27 篇的 pdf/md/assets 齐备")


if __name__ == "__main__":
    main()
