"""把 papers/pdf/*.pdf 解析为 papers/<分类>/<编号>.md，并把 nav.json 的导航卡写进文件头。

用法:
    python pdf2md.py                      # 转换全部（已存在且非空的会跳过）
    python pdf2md.py --force              # 强制重转
    python pdf2md.py 2512.13564           # 只转指定编号（可多个）
    python pdf2md.py --out engineering    # 输出到 papers/engineering/（默认 papers/surveys/）

依赖: pymupdf4llm（装在隔离 venv）
运行: C:\\Users\\37071\\.workbuddy\\binaries\\python\\envs\\default\\Scripts\\python.exe pdf2md.py
"""

import json
import os
import re
import sys

import pymupdf4llm

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_DIR = os.path.join(BASE, "pdf")
META_PATH = os.path.join(BASE, "meta.json")
NAV_PATH = os.path.join(BASE, "nav.json")


def load_json(path):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def clean(md: str) -> str:
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r"(?m)^\s*-\s*\d+\s*-\s*$", "", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n"


def nav_block(aid, nav):
    n = nav.get(aid)
    if not n:
        return ""
    rows = [
        ("一句话定位", n.get("one_liner")),
        ("分类轴", n.get("axis")),
        ("必读", n.get("must_read")),
        ("可跳过", n.get("skip")),
        ("盲区", n.get("blind_spot")),
        ("回答什么问题", n.get("answers")),
    ]
    out = ["", "", "## 导航卡", ""]
    for k, v in rows:
        if v:
            out.append(f"- **{k}**: {v}")
    out.append("")
    return "\n".join(out)


def header(aid, meta, nav):
    m = meta.get(aid, {})
    title = m.get("title") or "(标题待补)"
    authors = m.get("authors") or []
    a = (", ".join(authors[:6]) + f" 等 {len(authors)} 人") if len(authors) > 6 else (", ".join(authors) or "—")
    lines = [
        f"# {title}",
        "",
        f"- arXiv: [{aid}](https://arxiv.org/abs/{aid})",
        f"- 作者: {a}",
        f"- 发表日期: {m.get('date') or '—'}",
    ]
    return "\n".join(lines) + nav_block(aid, nav) + "\n---\n\n"


def convert(aid, meta, nav, out_dir, force=False):
    src = os.path.join(PDF_DIR, f"{aid}.pdf")
    md_dir = os.path.join(BASE, out_dir)
    os.makedirs(md_dir, exist_ok=True)
    dst = os.path.join(md_dir, f"{aid}.md")
    if not os.path.exists(src):
        return f"[{aid}] 缺少 PDF，跳过"
    if os.path.exists(dst) and os.path.getsize(dst) > 2000 and not force:
        return f"[{aid}] 已存在，跳过（--force 可重转）"

    md = clean(pymupdf4llm.to_markdown(src, write_images=False, show_progress=False))
    out = header(aid, meta, nav) + md
    with open(dst, "w", encoding="utf-8") as f:
        f.write(out)
    return f"[{aid}] -> {dst}  ({len(out)//1024} KB, {len(md.splitlines())} 行)"


def main():
    args, out_dir, force = [], "surveys", False
    it = iter(sys.argv[1:])
    for a in it:
        if a == "--force":
            force = True
        elif a == "--out":
            out_dir = next(it, "surveys")
        elif not a.startswith("--"):
            args.append(a)

    meta, nav = load_json(META_PATH), load_json(NAV_PATH)
    if not args:
        args = sorted(f[:-4] for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")) if os.path.isdir(PDF_DIR) else []
    if not args:
        print("没有可转换的 PDF。先用 download_arxiv.py 下载。")
        return
    for aid in args:
        print(convert(aid, meta, nav, out_dir, force))


if __name__ == "__main__":
    main()
