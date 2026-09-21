"""Convert local PDFs to Markdown without adding our reading judgments.

Usage: pdf2md.py [--force] [--kind survey] [stem ...]
Output always goes to md/<stem>.md. Existing nonempty outputs are preserved
unless --force is supplied.
"""

import hashlib
import importlib.metadata
import os
import re
import sys
from datetime import datetime, timezone

from stem import (base, find, front_matter, load_meta, load_provenance, md_path,
                  pdf_dir, pdf_path, save_provenance, to_stem)


def clean(md):
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r"(?m)^\s*-\s*\d+\s*-\s*$", "", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n"


def human_header(name, meta, pdf_hash, record):
    """Human-readable block below the front matter; identity fields live above it."""
    m = meta.get(name, {})
    info = find(name) or {}
    registry = info.get("registry") or m.get("registry") or "unknown"
    native_id = info.get("native_id") or m.get("native_id") or "unknown"
    authors = m.get("authors") or info.get("authors") or []
    names = (", ".join(authors[:6]) + f" 等 {len(authors)} 人") if len(authors) > 6 else (", ".join(authors) or "—")
    if registry == "arxiv":
        source = f"arXiv: [{native_id}]({record.get('source_url') or 'https://arxiv.org/abs/' + native_id})"
    else:
        source = f"{registry}: [{native_id}]({record.get('source_url') or ''})"
    return "\n".join([
        f"# {m.get('title') or '(标题待补)'}", "",
        f"- {source}",
        f"- 作者: {names}",
        f"- 发表日期: {m.get('date') or '—'}",
        f"- 来源版本: {record.get('version') or 'unknown（缺失，不推测）'}",
        f"- 本地 PDF SHA256: `{pdf_hash}`", "",
        "> 本文件是 PDF 的机器转换文本，转换成功不等于已对 PDF 做视觉核验。",
        "> 元数据与 PDF 的配对状态、转换时间及解析器版本见 papers/provenance.json；历史版本缺失时不能假定同版。",
        "> 下方分隔线之后为转换正文，不含本项目的阅读建议。", "", "---", "",
    ]) + "\n"


def convert(token, meta, force=False, kind=None):
    try:
        stem = to_stem(token)
    except ValueError as error:
        return f"[{token}] {error}"
    src = pdf_path(stem)
    dst = md_path(stem)
    if not os.path.exists(src):
        return f"[{stem}] 缺少 PDF，跳过"
    if os.path.exists(dst) and os.path.getsize(dst) > 0 and not force:
        return f"[{stem}] 已存在，未重解析（--force 可重转）"

    with open(src, "rb") as f:
        pdf_hash = hashlib.sha256(f.read()).hexdigest()
    provenance = load_provenance()
    record = provenance.setdefault(stem, {})
    if record.get("pdf_sha256") and record["pdf_sha256"] != pdf_hash:
        raise ValueError(f"[{stem}] PDF 与已记录的 SHA256 不一致，请先调查来源变化")

    # Lazy import allows metadata inspection and no-op runs without the parser.
    import pymupdf4llm

    md = clean(pymupdf4llm.to_markdown(src, write_images=False, show_progress=False))
    record.setdefault("version", None)
    record.setdefault("retrieved_at", None)
    record.setdefault("metadata_pdf_pairing", "unknown")
    record["pdf_sha256"] = pdf_hash
    record["pdf_path"] = os.path.relpath(src, base()).replace(os.sep, "/")
    out = front_matter(stem, meta.get(stem, {}), find(stem), record, kind) + human_header(stem, meta, pdf_hash, record) + md
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    temporary = dst + ".tmp"
    with open(temporary, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    os.replace(temporary, dst)
    record["conversion"] = {
        "path": os.path.relpath(dst, base()).replace(os.sep, "/"),
        "parser": "pymupdf4llm",
        "parser_version": importlib.metadata.version("pymupdf4llm"),
        "converted_at": datetime.now(timezone.utc).isoformat(),
        "pdf_sha256": pdf_hash,
        "body_sha256": hashlib.sha256(md.encode("utf-8")).hexdigest(),
        "options": {"write_images": False, "show_progress": False},
        "postprocess": "clean(): normalize blank lines and remove dash-number-dash lines",
        "visual_verification": False,
    }
    save_provenance(provenance)
    return f"[{stem}] -> {dst}（{len(md.splitlines())} 行；已记录来源与转换信息）"


def main():
    args, force, kind = [], False, None
    it = iter(sys.argv[1:])
    for a in it:
        if a == "--force":
            force = True
        elif a == "--kind":
            kind = "[" + next(it, "unclassified") + "]"
        elif not a.startswith("--"):
            args.append(a)
    meta = load_meta()
    if not args:
        args = sorted(f[:-4] for f in os.listdir(pdf_dir()) if f.lower().endswith(".pdf")) if os.path.isdir(pdf_dir()) else []
    if not args:
        print("没有可转换的 PDF。先用 download_arxiv.py 下载。")
        return
    for token in args:
        print(convert(token, meta, force, kind))


if __name__ == "__main__":
    main()
