"""Convert local PDFs to Markdown without adding our reading judgments.

Usage: pdf2md.py [--force] [--out surveys] [arxiv_id ...]
Existing nonempty outputs are preserved unless --force is supplied.
"""

import hashlib
import importlib.metadata
import json
import os
import re
import sys
from datetime import datetime, timezone


BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_DIR = os.path.join(BASE, "pdf")
META_PATH = os.path.join(BASE, "meta.json")
PROVENANCE_PATH = os.path.join(BASE, "provenance.json")


def load_json(path):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_json(path, data):
    temporary = path + ".tmp"
    with open(temporary, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(temporary, path)


def clean(md):
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r"(?m)^\s*-\s*\d+\s*-\s*$", "", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n"


def header(aid, meta, pdf_hash, record):
    m = meta.get(aid, {})
    authors = m.get("authors") or []
    names = (", ".join(authors[:6]) + f" 等 {len(authors)} 人") if len(authors) > 6 else (", ".join(authors) or "—")
    return "\n".join([
        f"# {m.get('title') or '(标题待补)'}", "",
        f"- arXiv: [{aid}]({record.get('source_url') or 'https://arxiv.org/abs/' + aid})",
        f"- 作者: {names}",
        f"- 发表日期: {m.get('date') or '—'}",
        f"- 来源版本: {record.get('version') or 'unknown（缺失，不推测）'}",
        f"- 本地 PDF SHA256: `{pdf_hash}`", "",
        "> 本文件是 PDF 的机器转换文本，转换成功不等于已对 PDF 做视觉核验。",
        "> 元数据与 PDF 的配对状态、转换时间及解析器版本见 papers/provenance.json；历史版本缺失时不能假定同版。",
        "> 下方分隔线之后为转换正文，不含本项目的阅读建议。", "", "---", "",
    ]) + "\n"


def convert(aid, meta, out_dir, force=False):
    if not re.fullmatch(r"\d{4}\.\d{4,5}(?:v[1-9]\d*)?", aid):
        raise ValueError(f"invalid arXiv id: {aid}")
    src = os.path.join(PDF_DIR, f"{aid}.pdf")
    md_dir = os.path.abspath(os.path.join(BASE, out_dir))
    if os.path.commonpath([BASE, md_dir]) != BASE or md_dir == BASE:
        raise ValueError("--out must be a subdirectory of papers/")
    dst = os.path.join(md_dir, f"{aid}.md")
    if not os.path.exists(src):
        return f"[{aid}] 缺少 PDF，跳过"
    if os.path.exists(dst) and os.path.getsize(dst) > 0 and not force:
        return f"[{aid}] 已存在，未重解析（--force 可重转）"

    with open(src, "rb") as f:
        pdf_hash = hashlib.sha256(f.read()).hexdigest()
    provenance = load_json(PROVENANCE_PATH)
    record = provenance.setdefault(aid, {})
    if record.get("pdf_sha256") and record["pdf_sha256"] != pdf_hash:
        raise ValueError(f"[{aid}] PDF 与已记录的 SHA256 不一致，请先调查来源变化")

    # Lazy import allows metadata inspection and no-op runs without the parser.
    import pymupdf4llm

    md = clean(pymupdf4llm.to_markdown(src, write_images=False, show_progress=False))
    record.setdefault("version", None)
    record.setdefault("retrieved_at", None)
    record.setdefault("metadata_pdf_pairing", "unknown")
    record["pdf_sha256"] = pdf_hash
    record["pdf_path"] = os.path.relpath(src, BASE).replace(os.sep, "/")
    out = header(aid, meta, pdf_hash, record) + md
    os.makedirs(md_dir, exist_ok=True)
    temporary = dst + ".tmp"
    with open(temporary, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    os.replace(temporary, dst)
    record["conversion"] = {
        "path": os.path.relpath(dst, BASE).replace(os.sep, "/"),
        "parser": "pymupdf4llm",
        "parser_version": importlib.metadata.version("pymupdf4llm"),
        "converted_at": datetime.now(timezone.utc).isoformat(),
        "pdf_sha256": pdf_hash,
        "body_sha256": hashlib.sha256(md.encode("utf-8")).hexdigest(),
        "options": {"write_images": False, "show_progress": False},
        "postprocess": "clean(): normalize blank lines and remove dash-number-dash lines",
        "visual_verification": False,
    }
    save_json(PROVENANCE_PATH, provenance)
    return f"[{aid}] -> {dst} ({len(md.splitlines())} 行；已记录来源与转换信息)"


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
    meta = load_json(META_PATH)
    if not args:
        args = sorted(f[:-4] for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")) if os.path.isdir(PDF_DIR) else []
    if not args:
        print("没有可转换的 PDF。先用 download_arxiv.py 下载。")
        return
    for aid in args:
        print(convert(aid, meta, out_dir, force))


if __name__ == "__main__":
    main()
