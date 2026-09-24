"""Convert a local PDF through a MinerU HTTP service.

MinerU itself lives outside this project (heavy models, own environment). This
client only talks to a running service and writes the result into the paper
archive with the same provenance discipline as the cloud client.

Usage:
    mineru_client.py [--service URL] [--backend pipeline|hybrid|vlm]
                     [--lang ch] [--force] [stem ...]

Defaults: service http://127.0.0.1:8000, backend pipeline, lang ch.
Output goes to md/<stem>.md only; no json/ is written.
The service must already be running; this script never starts it and never falls
back to another parser, so a failed conversion cannot be mistaken for success.
"""

import argparse
import hashlib
import io
import json
import os
import re
import sys
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timezone
from uuid import uuid4

from stem import find, front_matter, md_path, pdf_path, to_stem

UA = "MemoryResearch/1.0 (mineru client)"


def request(url, data=None, headers=None, timeout=600):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": UA, **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.URLError as error:
        raise SystemExit(f"无法连接 MinerU 服务 {url}：{error}。请先启动服务再运行本脚本。")


def health(service):
    _, body = request(service.rstrip("/") + "/health", timeout=30)
    try:
        return json.loads(body.decode("utf-8"))
    except ValueError:
        return {}


def multipart(fields, files):
    boundary = "----mineruclient" + uuid4().hex
    buf = io.BytesIO()
    for key, value in fields.items():
        buf.write(('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (boundary, key, value)).encode())
    for name, filename, payload in files:
        buf.write(('--%s\r\nContent-Disposition: form-data; name="%s"; filename="%s"\r\n'
                   'Content-Type: application/pdf\r\n\r\n' % (boundary, name, filename)).encode())
        buf.write(payload)
        buf.write(b"\r\n")
    buf.write(("--%s--\r\n" % boundary).encode())
    return buf.getvalue(), "multipart/form-data; boundary=%s" % boundary


def parse_response(payload):
    """Return (md_text, middle_json_text). Unknown shapes raise instead of guessing."""
    if zipfile.is_zipfile(io.BytesIO(payload)):
        md_parts, json_parts = [], []
        with zipfile.ZipFile(io.BytesIO(payload)) as zf:
            for name in sorted(zf.namelist()):
                lower = name.lower()
                if lower.endswith(".md"):
                    md_parts.append(zf.read(name).decode("utf-8", "replace"))
                elif lower.endswith(".json") and "middle" in lower:
                    json_parts.append(zf.read(name).decode("utf-8", "replace"))
        if md_parts:
            return "\n\n".join(md_parts), (json_parts[0] if json_parts else None)
        raise SystemExit("MinerU 返回了 zip，但里面没有 .md；请检查服务参数。")

    try:
        data = json.loads(payload.decode("utf-8", "replace"))
    except ValueError:
        raise SystemExit("无法识别 MinerU 返回格式（既不是 zip 也不是 JSON）。")

    def walk(node):
        if isinstance(node, dict):
            for key in ("md_content", "markdown", "md"):
                if isinstance(node.get(key), str):
                    return node[key]
            for value in node.values():
                found = walk(value)
                if found:
                    return found
        elif isinstance(node, list):
            for value in node:
                found = walk(value)
                if found:
                    return found
        return None

    md = walk(data)
    if md is None:
        raise SystemExit("MinerU 返回 JSON 但未找到 Markdown 字段；请用 --service 确认服务版本。")
    return md, json.dumps(data, ensure_ascii=False)


def header(stem, record, pdf_hash, info):
    lines = [
        f"# {stem}（MinerU 转换）", "",
        f"- 解析器: MinerU{(' ' + info['parser_version']) if info.get('parser_version') else ''}",
        f"- 服务: {info['service']}（protocol_version {info.get('protocol_version') or 'unknown'}）",
        f"- 后端: {info['backend']}；语言: {info['lang']}",
        f"- 转换时间: {info['converted_at']}",
        f"- 本地 PDF SHA256: `{pdf_hash}`", "",
        "> 本文件由外部 MinerU 服务转换，转换成功不等于已对 PDF 做视觉核验。",
        "> 表格、公式与图像仍需在使用时核对。",
        "> 下方分隔线之后为转换正文，不含本项目的阅读建议。", "", "---", "",
    ]
    return "\n".join(lines)


def convert(token, args, info):
    stem = to_stem(token)
    src = pdf_path(stem)
    if not os.path.exists(src):
        return f"[{stem}] 缺少 PDF，跳过"
    dst = md_path(stem)
    if os.path.exists(dst) and os.path.getsize(dst) > 0 and not args.force:
        return f"[{stem}] 已存在，未重新转换（--force 可重转）"

    with open(src, "rb") as f:
        pdf_bytes = f.read()
    pdf_hash = hashlib.sha256(pdf_bytes).hexdigest()
    fields = {
        "return_md": "true",
        "return_middle_json": "true",
        "response_format_zip": "true",
        "backend": args.backend,
        "lang_list": args.lang,
    }
    body, content_type = multipart(fields, [("files", f"{stem}.pdf", pdf_bytes)])
    _, payload = request(args.service.rstrip("/") + "/file_parse", data=body,
                         headers={"Content-Type": content_type})
    md, middle = parse_response(payload)

    os.makedirs(os.path.dirname(dst), exist_ok=True)
    stamp = datetime.now(timezone.utc).isoformat()
    info["converted_at"] = stamp
    with open(dst, "w", encoding="utf-8", newline="") as f:
        f.write(front_matter(stem, find(stem)))
        f.write(header(stem, {}, pdf_hash, info))
        f.write(md.strip() + "\n")
    return f"[{stem}] -> {dst}（{len(md.splitlines())} 行）"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--service", default=os.environ.get("MINERU_SERVICE", "http://127.0.0.1:8000"))
    ap.add_argument("--backend", default="pipeline")
    ap.add_argument("--lang", default="ch")
    ap.add_argument("--lang", default="ch")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("ids", nargs="*")
    args = ap.parse_args()

    if not args.ids:
        print("没有指定词干。用法见文件头注释。")
        return
    info = health(args.service)
    meta = {
        "service": args.service,
        "backend": args.backend,
        "lang": args.lang,
        "parser_version": args.parser_version,
        "protocol_version": info.get("protocol_version"),
    }
    for token in args.ids:
        try:
            stem = to_stem(token)
        except ValueError as error:
            print(f"[{token}] {error}")
            continue
        print(convert(stem, args, meta))


if __name__ == "__main__":
    main()
