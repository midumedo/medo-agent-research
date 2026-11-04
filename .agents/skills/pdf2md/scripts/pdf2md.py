#!/usr/bin/env python3
"""Manage a portable pdf/, md/, assets/ collection. Standard library only."""

from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from pathlib import Path

from pdf_library import (Document, Library, LibraryError, atomic_bytes, atomic_text,
                         check_document, clean_name, name_stem, read_markdown,
                         rename_document, render_markdown, resolve_document,
                         split_keywords, stem_of, write_conversion, identity_from_name)
import pdf_sources
import mineru_backend


def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2), flush=True)


def local_metadata(doc: Document, source: Path | None = None) -> dict:
    path = source if source and source.suffix.lower() == ".md" else doc.md
    fields, body = read_markdown(path)
    pdf = source if source and source.suffix.lower() == ".pdf" else doc.pdf
    return metadata_view(doc.stem, fields, body, pdf, path, doc.record)


def metadata_view(stem, fields, body, pdf, markdown, row=None):
    row = row or {}
    extracted = pdf_sources.extract_document_metadata(body) if body else {}
    ident = fields.get("id") or row.get("id") or identity_from_name(stem)
    version = re.search(r"v[1-9]\d*$", ident or "")
    return {
        "stem": stem,
        "id": ident,
        "version": version.group(0) if version else None,
        "title": fields.get("title") or extracted.get("title"),
        "abstract": fields.get("abstract") or extracted.get("abstract"),
        "revised": row.get("revised") or fields.get("revised"),
        "source": fields.get("source"),
        "keywords": row.get("keywords", fields.get("keywords", [])),
        "parser": fields.get("parser"),
        "pdf": str(pdf) if pdf is not None else None,
        "md": str(markdown) if markdown is not None else None,
        "needs_conversion": bool(pdf and pdf.is_file() and not body.strip()),
    }


def metadata_for(value: str, root=None) -> dict:
    path = Path(value).expanduser()
    explicit_path = path.is_absolute() or "/" in value or "\\" in value
    if (root is None or explicit_path) and path.is_file() and path.suffix.lower() in (".pdf", ".md"):
        source = path.resolve()
        if source.parent.name.lower() in ("pdf", "md"):
            doc = Document(source.parent.parent, source.stem)
            return complete_metadata(local_metadata(doc, source))
        markdown = source if source.suffix.lower() == ".md" else source.with_suffix(".md")
        front, body = read_markdown(markdown)
        pdf = source if source.suffix.lower() == ".pdf" else source.with_suffix(".pdf")
        info = metadata_view(source.stem, front, body, pdf if pdf.is_file() else None,
                             markdown if markdown.is_file() else None)
        return complete_metadata(info)
    if path.is_file() or (root and not value.startswith(("http://", "https://"))):
        doc, source = resolve_document(value, root)
        if doc.pdf.exists() or doc.md.exists() or source or doc.record:
            return complete_metadata(local_metadata(doc, source))
    elif explicit_path and not value.startswith(("http://", "https://")) and not pdf_sources.arxiv_id(value):
        raise LibraryError(f"文件不存在：{value}")
    return pdf_sources.fetch_metadata(value)


def complete_metadata(info: dict) -> dict:
    native = pdf_sources.arxiv_id(info.get("id") or "")
    if native and info.get("version") and (not info.get("abstract") or not info.get("title")):
        try:
            fetched = pdf_sources.fetch_metadata(native)
            return {**fetched, **{k: v for k, v in info.items() if v is not None and v != ""}}
        except pdf_sources.SourceError as error:
            info["warnings"] = [str(error)]
    return info


def collect_documents(inputs, root=None, all_files=False, import_pdf=False) -> list[Document]:
    if all_files:
        if not root:
            raise LibraryError("--all 需要 --root。")
        if inputs:
            raise LibraryError("指定资料和 --all 请选择一种范围。")
        return Library(root).documents()
    if not inputs:
        raise LibraryError("请指定资料，或用 --root DIR --all 选择整个资料目录。")
    documents = []
    for value in inputs:
        doc, source = resolve_document(value, root)
        if import_pdf and source and source.suffix.lower() == ".pdf" and source != doc.pdf:
            if doc.pdf.exists():
                if not source.samefile(doc.pdf):
                    raise LibraryError(f"导入目标已存在，未覆盖：{doc.pdf}")
            else:
                payload = source.read_bytes()
                if not payload.startswith(b"%PDF-"):
                    raise LibraryError(f"输入不是 PDF：{source}")
                atomic_bytes(doc.pdf, payload)
        if (doc.root, doc.stem) not in {(d.root, d.stem) for d in documents}:
            documents.append(doc)
    return documents


def select_documents(inputs, root=None, all_files=False, import_pdf=False):
    """Keep independent input failures from hiding or blocking valid papers."""
    if all_files or not inputs:
        return collect_documents(inputs, root, all_files, import_pdf), []
    documents, failures, seen = [], [], set()
    for value in inputs:
        try:
            for doc in collect_documents([value], root, import_pdf=import_pdf):
                key = (doc.root, doc.stem)
                if key not in seen:
                    documents.append(doc)
                    seen.add(key)
        except (LibraryError, OSError) as error:
            failures.append({"input": value, "state": "failed", "error": str(error), "complete": False})
    return documents, failures


def check_download_name(doc, name=None):
    if name:
        requested = clean_name(name_stem(name))
        ident = doc.ident
        if requested != doc.stem and ident and doc.stem.startswith(ident + ".") and not requested.startswith(ident + "."):
            requested = ident + "." + requested
        if requested != doc.stem:
            raise LibraryError("资料已存在；需要改名请使用 rename。")


def cached_download(doc, name=None):
    check_download_name(doc, name)
    return doc, {**local_metadata(doc), "state": "cached"}


def confirm_download_source(doc, info):
    """A missing PDF may join existing material only with matching source evidence."""
    front, row = doc.front, doc.record
    requested = pdf_sources.arxiv_id(info.get("id") or "")
    identities = [front.get("id"), row.get("id"), identity_from_name(doc.stem)]
    known = [pdf_sources.arxiv_id(value) for value in identities if value]
    known = [value for value in known if value]
    source = front.get("source")
    if source:
        source_id = pdf_sources.arxiv_id(source)
        if source_id:
            known.append(source_id)
        elif source not in (info.get("source"), info.get("pdf_url")):
            raise LibraryError(f"已有资料的来源与下载来源冲突，未补取：{doc.stem}")
    if known and (not requested or any(value != requested for value in known)):
        raise LibraryError(f"已有资料的来源编号与下载来源冲突，未补取：{doc.stem}")
    if not known and not (source and source in (info.get("source"), info.get("pdf_url"))):
        raise LibraryError(f"无法确认已有资料与下载来源相同，未补取：{doc.stem}")


def download_one(value: str, root, name=None) -> tuple[Document, dict]:
    lib = Library(root)
    native = pdf_sources.arxiv_id(value)
    if native or not value.startswith(("http://", "https://")):
        lookup = "arxiv-" + native.replace("/", "-") if native else value
        existing = lib.resolve(lookup)
        if existing.pdf.is_file():
            return cached_download(existing, name)
        row = existing.record
        if existing.md.is_file() or row:
            check_download_name(existing, name)
            # An unversioned lookup may select an existing pinned revision.
            # Recover that PDF rather than silently pairing its MD with latest.
            if not native or not re.search(r"v[1-9]\d*$", native):
                value = existing.ident or existing.front.get("source") or value
    else:
        existing, row = None, {}
        cached = [doc for doc in lib.documents(include_ledger=False)
                  if doc.front.get("source") == value]
        if name and len(cached) > 1:
            cached = [doc for doc in cached if doc.stem == clean_name(name_stem(name))]
        if len(cached) > 1:
            raise LibraryError("该来源对应多份本地资料，请用 --name 指定名称或直接操作已有 PDF。")
        if cached:
            existing = cached[0]
            check_download_name(existing, name)
            if existing.pdf.is_file():
                return cached_download(existing, name)
            row = existing.record
    info = pdf_sources.fetch_metadata(value)
    url = info.get("pdf_url")
    if not url:
        raise LibraryError(f"没有明确的 PDF 下载地址：{value}")
    ident = info.get("id")
    partial = existing if existing and (existing.md.is_file() or row) else None
    if partial:
        confirm_download_source(partial, info)
        filename = partial.stem
    elif name:
        filename = clean_name(name_stem(name))
        if ident and filename != ident and not filename.startswith(ident + "."):
            filename = ident + "." + filename
    elif ident:
        title = info.get("title")
        filename = ident + ("." + clean_name(title) if title else "")
    else:
        filename = clean_name(name_stem(info.get("filename") or "document.pdf"))
    doc = Document(lib.root, filename)
    if doc.pdf.exists() or (doc.md.exists() and not partial):
        raise LibraryError(f"同名资料已存在，未覆盖：{filename}；请使用明确名称或现有资料标识。")
    payload = pdf_sources.download_pdf(url)
    atomic_bytes(doc.pdf, payload)
    # Metadata is returned to the Agent; a combined download/convert retains it
    # in memory until it can be written into the MD. No permanent sidecar.
    lib.update_existing_index(doc, revised=info.get("revised"))
    return doc, {**info, "stem": doc.stem, "pdf": str(doc.pdf), "state": "downloaded"}


def convert_documents(documents, args, known_metadata=None) -> int:
    groups = {}
    errors = 0
    for doc in documents:
        if not doc.pdf.is_file():
            print(f"[{doc.stem}] 缺 PDF：{doc.pdf}", file=sys.stderr)
            errors += 1
        elif not args.force and check_document(doc)["complete"]:
            print(f"[{doc.stem}] 已齐备，跳过（--force 可重转）")
        else:
            try:
                Library(doc.root).validate_conversion(doc)
            except LibraryError as error:
                print(f"[{doc.stem}] {error}", file=sys.stderr)
                errors += 1
                continue
            groups.setdefault(doc.root, []).append(doc)
    if args.batch_id and len(groups) > 1:
        raise LibraryError("继续一个 batch_id 时请只指定一个资料目录。")
    for root, selected in groups.items():
        jobs, by_id, by_name = [], {}, {}
        for doc in selected:
            job = {"path": str(doc.pdf), "name": doc.pdf.name, "data_id": uuid.uuid4().hex}
            jobs.append(job)
            by_id[job["data_id"]] = doc
            by_name[job["name"]] = doc
        seen = set()
        try:
            results = mineru_backend.convert_files(
                jobs, model_version=args.model_version, language=args.lang,
                enable_formula=not args.no_formula, enable_table=not args.no_table,
                is_ocr=args.ocr, timeout=args.timeout, batch_id=args.batch_id,
            )
            for result in results:
                doc = by_id.get(result.get("data_id")) or by_name.get(result.get("file_name"))
                if not doc:
                    print("收到无法匹配到所选文件的任务结果。", file=sys.stderr)
                    errors += 1
                    continue
                seen.add(doc.stem)
                if result.get("state") != "done":
                    errors += 1
                    print(f"[{doc.stem}] {result.get('state')}: {result.get('error') or '尚未完成'}；"
                          f"batch_id={result.get('batch_id')}", file=sys.stderr)
                    continue
                try:
                    parsed = mineru_backend.parse_archive(result["zip_bytes"], doc.prefix,
                                                         requested_model=args.model_version)
                    info = (known_metadata or {}).get((doc.root, doc.stem)) or local_metadata(doc)
                    native = pdf_sources.arxiv_id(doc.ident or "")
                    if native and re.search(r"v[1-9]\d*$", native) and (not info.get("abstract") or not info.get("source")):
                        try:
                            fetched = pdf_sources.fetch_metadata(native)
                            info = {**fetched, **{k: v for k, v in info.items() if v is not None and v != ""}}
                        except pdf_sources.SourceError as error:
                            print(f"[{doc.stem}] 元数据未补齐：{error}", file=sys.stderr)
                    extracted = pdf_sources.extract_document_metadata(parsed["body"])
                    for key in ("title", "abstract"):
                        if not info.get(key) and extracted.get(key):
                            info[key] = extracted[key]
                    write_conversion(doc, parsed, info)
                    for warning in parsed.get("warnings", []):
                        print(f"[{doc.stem}] {warning}", file=sys.stderr)
                    print(f"[{doc.stem}] -> {doc.md}；{len(parsed['assets'])} 张分类资产；{parsed['parser']}")
                except (LibraryError, mineru_backend.MinerUError, OSError, ValueError) as error:
                    errors += 1
                    print(f"[{doc.stem}] 结果处理失败：{error}", file=sys.stderr)
        except (mineru_backend.MinerUError, OSError, ValueError) as error:
            print(str(error), file=sys.stderr)
            errors += 1
        unseen = [doc.stem for doc in selected if doc.stem not in seen]
        if unseen:
            errors += len(unseen)
            print("未取得完整结果：" + ", ".join(unseen), file=sys.stderr)
    return 1 if errors else 0


def add_conversion_options(parser):
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--model-version", choices=("vlm", "pipeline"), default="vlm")
    parser.add_argument("--lang", default="ch", help="MinerU language；英文论文可用 en")
    parser.add_argument("--timeout", type=int, default=1800, help="批次轮询等待秒数，不是整个命令的总时限")
    parser.add_argument("--batch-id", help="继续已有批次，只查询、不重新提交；仍提供原输入文件")
    parser.add_argument("--ocr", action="store_true", help="启用云端 OCR（pipeline / vlm）")
    parser.add_argument("--no-formula", action="store_true", help="关闭公式识别；vlm 仅关闭行内公式识别")
    parser.add_argument("--no-table", action="store_true", help="关闭表格识别（pipeline / vlm）")



def make_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    metadata = sub.add_parser("metadata", help="输出完整来源信息和摘要，供 Agent 命名")
    metadata.add_argument("inputs", nargs="+")
    metadata.add_argument("--root")
    download = sub.add_parser("download", help="下载明确来源；不会搜索论文")
    download.add_argument("inputs", nargs="+")
    download.add_argument("--root", required=True)
    download.add_argument("--name", help="单篇目标名称；arXiv 名称可省略官方编号前缀")
    download.add_argument("--convert", action="store_true")
    add_conversion_options(download)
    convert = sub.add_parser("convert", help="MinerU 转 MD 并提取分类资产")
    convert.add_argument("inputs", nargs="*")
    convert.add_argument("--root")
    convert.add_argument("--all", action="store_true")
    add_conversion_options(convert)
    rename = sub.add_parser("rename", help="联动改名；保持来源编号与版本")
    rename.add_argument("input")
    rename.add_argument("new_name", help="完整文件 stem，含已有来源编号前缀")
    rename.add_argument("--root")
    index = sub.add_parser("index", help="维护四列 index.csv；默认合并本地资料并保留离线记录",
                           description="不带操作参数时创建或更新 index.csv；读取、关键词修改和对账分别按指定范围执行。")
    index.add_argument("--root", required=True)
    action = index.add_mutually_exclusive_group()
    action.add_argument("--set-keywords", nargs=2, metavar=("TARGET", "WORDS"),
                        help="替换单篇关键词并同步已有 MD；分号分隔，空字符串清空")
    action.add_argument("--missing-keywords", action="store_true", help="只读已登记且缺关键词的记录，附本地标题与摘要")
    action.add_argument("--check", action="store_true", help="只检查索引是否需要对账；不检查 PDF/MD 齐备性")
    action.add_argument("--list", action="store_true", help="只读已保存的索引，不扫描或收录本地文件")
    index.add_argument("--prune", action="store_true", help="对账时删除 PDF 和 MD 均不在本地的记录，包括待下载资料")
    check = sub.add_parser("check", help="检查 PDF、MD 及 MD 引用的本地图片")
    check.add_argument("inputs", nargs="*")
    check.add_argument("--root")
    check.add_argument("--all", action="store_true")
    return parser


def index_command(args):
    lib = Library(args.root)
    if args.prune and (args.check or args.missing_keywords or args.list or args.set_keywords):
        raise LibraryError("--prune 仅与索引重建一起使用。")
    if args.list:
        emit(lib.read_index())
        return 0
    if args.missing_keywords:
        result = []
        for row in lib.read_index():
            if not row.get("keywords"):
                info = local_metadata(Document(lib.root, stem_of(row)))
                result.append({**row, "title": info.get("title"), "abstract": info.get("abstract")})
        emit(result)
        return 0
    if args.set_keywords:
        token, words = args.set_keywords
        doc = lib.resolve(token)
        if not (doc.pdf.is_file() or doc.md.is_file() or doc.record):
            raise LibraryError(f"找不到关键词目标：{token}")
        rows = lib.rebuilt_index([doc])
        row = next(r for r in rows if stem_of(r) == doc.stem)
        row["keywords"] = split_keywords(words)
        if doc.md.is_file():
            front, body = read_markdown(doc.md)
            front["keywords"] = row["keywords"]
            atomic_text(doc.md, render_markdown(front, body))
    else:
        rows = lib.rebuilt_index(prune=args.prune)
        if args.check:
            if not lib.index.is_file() or lib.render_index(lib.read_index()) != lib.render_index(rows):
                print("index.csv 需要对账；未写入。", file=sys.stderr)
                return 1
            print(f"index.csv 一致：{len(rows)} 条")
            return 0
    lib.write_index(rows)
    print(f"index.csv：{len(rows)} 条")
    return 0


def main(argv=None):
    args = make_parser().parse_args(argv)
    try:
        if args.command == "metadata":
            values, failures = [], 0
            for value in args.inputs:
                try:
                    values.append(metadata_for(value, args.root))
                except (LibraryError, pdf_sources.SourceError, OSError, ValueError) as error:
                    values.append({"input": value, "state": "failed", "error": str(error)})
                    failures += 1
            emit(values[0] if len(values) == 1 else values)
            return 1 if failures else 0
        if args.command == "download":
            if args.name and len(args.inputs) != 1:
                raise LibraryError("--name 仅用于单篇下载。")
            documents, results, known, failures = [], [], {}, 0
            for value in args.inputs:
                try:
                    doc, info = download_one(value, args.root, args.name)
                    documents.append(doc)
                    results.append(info)
                    known[(doc.root, doc.stem)] = info
                except (LibraryError, pdf_sources.SourceError, OSError) as error:
                    failures += 1
                    results.append({"input": value, "state": "failed", "error": str(error)})
            emit(results[0] if len(results) == 1 else results)
            if args.convert and documents:
                failures += convert_documents(documents, args, known)
            return 1 if failures else 0
        if args.command == "convert":
            documents, failures = select_documents(args.inputs, args.root, args.all, import_pdf=True)
            for failure in failures:
                print(f"[{failure['input']}] {failure['error']}", file=sys.stderr)
            code = convert_documents(documents, args)
            return 1 if failures or code else 0
        if args.command == "rename":
            doc, source = resolve_document(args.input, args.root)
            if source and source not in (doc.pdf, doc.md):
                raise LibraryError("先将资料导入指定根目录，再使用 rename。")
            renamed = rename_document(doc, args.new_name)
            emit({"old": doc.stem, "new": renamed.stem, "root": str(doc.root)})
            return 0
        if args.command == "index":
            return index_command(args)
        if args.command == "check":
            documents, failures = select_documents(args.inputs, args.root, args.all or (not args.inputs and bool(args.root)))
            results = [check_document(doc)
                       for doc in documents] + failures
            emit(results)
            return 0 if all(row["complete"] for row in results) else 1
    except (LibraryError, pdf_sources.SourceError, mineru_backend.MinerUError, OSError, ValueError) as error:
        print(f"错误：{error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
