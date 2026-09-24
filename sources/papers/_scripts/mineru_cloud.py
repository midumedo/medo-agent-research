"""Convert local PDFs through the MinerU cloud API (https://mineru.net).

Preferred over the local service: no models to install, and the account has a
daily free page quota. The token comes from the MINERU_APIKEY environment
variable (falling back to the Windows user environment).

Usage:
    mineru_cloud.py [--model-version vlm|pipeline] [--lang en]
                    [--no-images] [--force] [--timeout 1800] [stem ...]

Writes md/<stem>.md and flat images under assets/, named by id and figure
number (e.g. arxiv-2504.19413v1-fig3.png). No json/ output: the content list is
read from the result zip only to recover figure captions, then discarded.
Existing nonempty md/ is preserved unless --force is given. The API is used as
documented; this script never falls back to another parser, so a failure cannot
be mistaken for a conversion.
"""

import argparse
import hashlib
import http.client
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from datetime import datetime, timezone

from stem import (assets_root, find, front_matter, md_path, pdf_dir, pdf_path,
                  read_front_matter, slugify, stem_of)

API = "https://mineru.net/api/v4"
UA = "MemoryResearch/1.0 (mineru cloud client)"
DONE = "done"
FAILED = "failed"
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"}

# Content List V1 field names. The official name is `image_caption`; the older
# spellings stay as fallbacks in case a server revision differs.
CAPTION_KEY = {"image": "image_caption", "table": "table_caption",
               "chart": "chart_caption", "equation": None}
CAPTION_FALLBACKS = ("image_caption", "table_caption", "chart_caption",
                     "code_caption", "caption", "img_caption")
KIND_TOKEN = {"image": "fig", "table": "table", "chart": "chart", "equation": "eq"}
NUM_RE = re.compile(r"(?:figure|fig\.?|图|table|tab\.?|表)\s*([0-9]+[a-z]?)", re.I)
TAG_RE = re.compile(r"<[^>]+>")
STATE_ORDER = ["downloaded", "converted", "imaged", "abstracted", "keyworded", "reviewed"]


def merge_state(existing, steps):
    """Union of what is already recorded and what just happened.

    Re-running the converter must not erase steps that came after it — the
    abstract and keywords are written outside this script.
    """
    keep = existing if isinstance(existing, list) else ([existing] if existing else [])
    merged = {str(s).strip() for s in list(keep) + list(steps) if str(s).strip()}
    return sorted(merged, key=lambda s: (STATE_ORDER.index(s) if s in STATE_ORDER
                                         else len(STATE_ORDER), s))


CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def sanitize_text(text):
    """Drop C0 control bytes that MinerU occasionally emits inside formulas.

    A single NUL is enough for grep and diff to treat the whole .md as binary,
    which hides the file from ordinary searching. Tab, newline and carriage
    return are kept: they are the text's own structure.
    """
    return CONTROL_RE.sub("", text)


def clean_caption(text):
    """Captions arrive with <sup>/<sub> markup wrapped around single glyphs
    (`Wit<sup>h</sup>out`); strip the tags rather than storing them as text."""
    return re.sub(r"\s+", " ", TAG_RE.sub("", text or "")).strip()


def token():
    value = os.environ.get("MINERU_APIKEY")
    if value:
        return value.strip()
    # Windows user variables are not visible to processes started before they
    # were set; read them from the registry instead of failing outright.
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            return winreg.QueryValueEx(key, "MINERU_APIKEY")[0].strip()
    except OSError:
        raise SystemExit(
            "没有取到 MINERU_APIKEY。它在用户环境变量里；当前会话看不到时重开终端，"
            "或临时用 $env:MINERU_APIKEY 设置后再运行。"
        )


def request(url, data=None, headers=None, method=None, timeout=120):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": UA, **(headers or {})}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", "replace")[:400]
        raise SystemExit(f"MinerU 返回 HTTP {error.code}：{body}")
    except urllib.error.URLError as error:
        raise SystemExit(f"无法连接 MinerU（{url}）：{error}")
    except ValueError:
        raise SystemExit("MinerU 返回的不是 JSON，请检查接口版本。")


def auth():
    return {"Content-Type": "application/json", "Authorization": "Bearer " + token()}


def apply_upload_urls(stems, model_version):
    payload = {"files": [{"name": f"{stem}.pdf", "data_id": stem} for stem in stems],
               "model_version": model_version}
    response = request(API + "/file-urls/batch", data=json.dumps(payload).encode("utf-8"), headers=auth())
    if response.get("code") != 0:
        raise SystemExit(f"申请上传链接失败：{response.get('msg')} / {response.get('trace_id')}")
    data = response.get("data") or {}
    urls = data.get("file_urls") or []
    if len(urls) != len(stems):
        raise SystemExit(f"上传链接数量（{len(urls)}）与请求数量（{len(stems)}）不一致，未上传。")
    return data.get("batch_id"), urls


def upload(url, path):
    """PUT the PDF straight to the signed URL.

    http.client rather than urllib: urllib injects a default Content-Type on any
    request carrying a body, and the object-storage signature covers that field,
    so the upload is rejected with 403. The response body is surfaced on failure
    instead of being swallowed.
    """
    parts = urllib.parse.urlsplit(url)
    connection_cls = http.client.HTTPSConnection if parts.scheme == "https" else http.client.HTTPConnection
    connection = connection_cls(parts.netloc, timeout=600)
    try:
        with open(path, "rb") as f:
            payload = f.read()
        target = parts.path + (("?" + parts.query) if parts.query else "")
        connection.request("PUT", target, body=payload,
                           headers={"User-Agent": UA, "Content-Length": str(len(payload))})
        response = connection.getresponse()
        body = response.read().decode("utf-8", "replace")[:300]
        if response.status >= 300:
            raise SystemExit(f"上传失败 HTTP {response.status}：{body}")
        return response.status
    finally:
        connection.close()


def poll(batch_id, stems, timeout):
    deadline = time.time() + timeout
    last = ""
    while time.time() < deadline:
        response = request(API + f"/extract-results/batch/{batch_id}", headers=auth())
        if response.get("code") != 0:
            raise SystemExit(f"查询结果失败：{response.get('msg')} / {response.get('trace_id')}")
        results = (response.get("data") or {}).get("extract_result") or []
        if not getattr(poll, "dumped", False):
            poll.dumped = True
        if not isinstance(results, list) or not results:
            time.sleep(5)
            continue
        states = {r.get("file_name", ""): r for r in results}
        summary = " ".join(f"{k}={v.get('state')}" for k, v in sorted(states.items()))
        if summary != last:
            print(f"  ... {summary}")
            last = summary
        if all(v.get("state") in (DONE, FAILED) for v in states.values()):
            return states
        time.sleep(5)
    raise SystemExit(f"等待超时（{timeout}s）；任务可能仍在队列里，稍后可用 batch_id {batch_id} 再查。")


def open_zip(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=600) as resp:
        payload = resp.read()
    if not zipfile.is_zipfile(io.BytesIO(payload)):
        raise SystemExit("结果不是 zip，无法解包。")
    return zipfile.ZipFile(io.BytesIO(payload))


def pick(zf, suffix, prefer=None):
    names = [n for n in zf.namelist() if n.lower().endswith(suffix)]
    if not names:
        return None
    if prefer:
        for name in names:
            if prefer in os.path.basename(name).lower():
                return name
    return sorted(names)[0]


def image_entries(zf):
    return [n for n in zf.namelist()
            if os.path.splitext(n)[1].lower() in IMAGE_EXT and not n.endswith("/")]


def load_content_list(zf, json_name):
    if not json_name:
        return []
    try:
        items = json.loads(zf.read(json_name).decode("utf-8", "replace"))
    except ValueError:
        return []
    if isinstance(items, dict):
        items = items.get("content_list") or []
    return items or []


def parse_visual(items):
    """content_list items -> [{img_path, kind, number, caption, page}], in order.

    The number comes from the caption text (e.g. "Figure 3" -> 3); items whose
    caption carries no number keep `number = None` so the caller can fall back to
    a running sequence instead of inventing a figure number.
    """
    out = []
    for item in items:
        if not isinstance(item, dict):
            continue
        kind = item.get("type")
        if kind not in KIND_TOKEN:
            continue
        preferred = CAPTION_KEY.get(kind)
        candidates = ([preferred] if preferred else []) + [
            c for c in CAPTION_FALLBACKS if c != preferred]
        caption = ""
        for candidate in candidates:
            value = item.get(candidate)
            if not value:
                continue
            parts = value if isinstance(value, list) else [value]
            caption = clean_caption(" ".join(str(p) for p in parts if p))
            if caption:
                break
        match = NUM_RE.search(caption)
        out.append({"img_path": item.get("img_path") or "",
                    "kind": kind,
                    "number": match.group(1) if match else None,
                    "caption": caption or None,
                    "page": item.get("page_idx")})
    return out


def name_map(items, ident, zip_names=()):
    """img_path -> `<ident>-<token><n>.<ext>`; **every** zip image gets a name.

    Figure numbers come from captions. Images content_list never recorded (the
    inline formulas MinerU also cuts out) are numbered `<ident>-img<N>`, so no
    file is left carrying the parser's hash as its name.
    """
    used, seq, dup = {}, {}, {}

    def unique(base, ext):
        name = base + ext
        while name in used.values():
            dup[base] = dup.get(base, 1) + 1
            name = f"{base}-{dup[base]}{ext}"
        return name

    for item in items:
        path = item["img_path"]
        if not path:
            continue
        kind_token = KIND_TOKEN[item["kind"]]
        seq[kind_token] = seq.get(kind_token, 0) + 1
        ext = os.path.splitext(path)[1].lower() or ".png"
        used[path] = unique(f"{ident}-{kind_token}{item['number'] or seq[kind_token]}", ext)

    # Items content_list knows but has no image for: `equation` blocks (and, in
    # a few papers, `table` ones). When every such item is an equation the orphan
    # images can be called what they are; once the kinds mix there is no way to
    # tell which file is which, so they fall back to the neutral `img`.
    nameless = {item["kind"] for item in items if not item["img_path"]}
    token = "eq" if nameless and nameless <= {"equation"} else "img"

    orphan = 0
    for name in zip_names:
        if name in used:
            continue
        orphan += 1
        ext = os.path.splitext(name)[1].lower() or ".png"
        used[name] = unique(f"{ident}-{token}{orphan}", ext)
    return used


def rewrite_image_refs(md_text, mapping):
    """MinerU writes ![](images/x.jpg); point it at ../assets/<renamed file>.

    The reference is resolved through the rename map, so the link and the file on
    disk can never drift apart.
    """
    def rel(path):
        name = os.path.basename(path)
        return "../assets/" + mapping.get(path, mapping.get(name, name))

    md_text = re.sub(r'\]\(images/([^)\s]+)[^)]*\)',
                     lambda m: "](" + rel("images/" + m.group(1)) + ")", md_text)
    return re.sub(r'src="images/([^"]+)"',
                  lambda m: 'src="' + rel("images/" + m.group(1)) + '"', md_text)


def write_assets(zf, stem, ident, items, mapping, keep_images):
    """Images land flat in assets/, each under its mapped name. No manifest.

    The bytes are versioned, the figure numbers are in the file names, and the
    captions sit right next to the image references in the md — a manifest would
    be a third copy of what already exists.
    """
    directory = assets_root()
    entries = sorted(image_entries(zf))
    images = []
    if entries:
        os.makedirs(directory, exist_ok=True)
    for name in entries:
        payload = zf.read(name)
        target = mapping.get(name) or os.path.basename(name)
        if keep_images:
            with open(os.path.join(directory, target), "wb") as f:
                f.write(payload)
        images.append({"file": target, "bytes": len(payload),
                       "sha256": hashlib.sha256(payload).hexdigest()})
    return {"count": len(images),
            "bytes": sum(i["bytes"] for i in images),
            "kept": bool(keep_images and images)}


def mineru_version(zf):
    """MinerU's own version, which only the zip knows.

    The API responses never mention it, and the model output does not either —
    it sits at the end of `layout.json` (the MiddleJson) as `_version_name`,
    next to `_backend`. Returns (version, backend), both None when absent: the
    caller falls back to the tier it asked for rather than inventing a number.
    """
    name = pick(zf, "layout.json")
    if not name:
        return None, None
    try:
        raw = zf.read(name).decode("utf-8", "replace")
    except Exception:
        return None, None
    found = re.search(r'"_version_name"\s*:\s*"([^"]+)"', raw)
    backend = re.search(r'"_backend"\s*:\s*"([^"]+)"', raw)
    return (found.group(1) if found else None,
            backend.group(1) if backend else None)


def parser_label(result, model_version, version=None):
    """`mineru-cloud <version>` when the server told us; the requested tier otherwise.

    Never issue an extra request just to learn a version number.
    """
    if version:
        return f"mineru-cloud {version}"
    for key in ("version", "parser_version", "model_version"):
        value = str((result or {}).get(key) or "").strip()
        if value:
            return f"mineru-cloud {value}"
    return f"mineru-cloud {model_version}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-version", default="vlm")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--no-images", action="store_true",
                    help="只写清单，不把图片字节写入 assets/")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("tokens", nargs="*")
    args = ap.parse_args()
    keep_images = not args.no_images

    stems = []
    for raw in args.tokens:
        record = find(raw)
        stems.append(stem_of(record) if record else slugify(raw))
    if not stems:
        stems = sorted(os.path.splitext(f)[0] for f in os.listdir(pdf_dir()) if f.lower().endswith(".pdf"))
    stems = [s for s in stems if os.path.exists(pdf_path(s))]
    if not stems:
        print("没有可转换的 PDF。")
        return

    todo = []
    for stem in stems:
        if os.path.exists(md_path(stem)) and os.path.getsize(md_path(stem)) > 0 and not args.force:
            print(f"[{stem}] 已存在，未重新转换（--force 可重转）")
            continue
        todo.append(stem)
    if not todo:
        return

    print(f"提交 {len(todo)} 个文件到 MinerU（model_version={args.model_version}）")
    batch_id, urls = apply_upload_urls(todo, args.model_version)
    for stem, url in zip(todo, urls):
        print(f"[{stem}] 上传 -> {upload(url, pdf_path(stem))}")
    print(f"batch_id={batch_id}，等待解析…")
    states = poll(batch_id, todo, args.timeout)

    for stem in todo:
        result = states.get(f"{stem}.pdf") or {}
        if result.get("state") != DONE:
            print(f"[{stem}] 未成功：state={result.get('state')} err={result.get('err_msg')}")
            continue
        with open_zip(result["full_zip_url"]) as zf:
            md_name = pick(zf, ".md", prefer="full")
            if not md_name:
                print(f"[{stem}] zip 里没有 .md，跳过")
                continue
            # 身份只有一份，记在 md 的登记块里；已入库的篇目可以从索引取到。
            ident = (find(stem) or {}).get("id") or stem
            items = parse_visual(load_content_list(zf, pick(zf, "_content_list.json")))
            mapping = name_map(items, ident, image_entries(zf))
            md_text = sanitize_text(rewrite_image_refs(zf.read(md_name).decode("utf-8", "replace"), mapping))
            assets = write_assets(zf, stem, ident, items, mapping, keep_images)

            stamp = datetime.now(timezone.utc).isoformat()
            version, backend = mineru_version(zf)
            label = parser_label(result, args.model_version, version)
            state = merge_state(read_front_matter(stem).get("state"),
                                ["downloaded", "converted"] + (["imaged"] if assets["count"] else []))
            os.makedirs(os.path.dirname(md_path(stem)), exist_ok=True)
            with open(md_path(stem), "w", encoding="utf-8", newline="\n") as f:
                f.write(front_matter(stem, find(stem), ident=ident,
                                     parser=label, state=state))
                f.write("\n".join([
                    f"- 解析器: {label}（语言 {args.lang}）",
                    f"- 转换时间: {stamp}",
                    f"- 图片: {assets['count']} 个，{assets['bytes'] // 1024} KB；"
                    + ("字节已写入 assets/" if assets["kept"] else "字节未保留，只写清单"),
                    "",
                    "> 本文件由 MinerU 云端接口转换，转换成功不等于已对 PDF 做视觉核验。",
                    "> 表格、公式与图像仍需在使用时核对；引用具体数字请回 pdf/ 定位原文。",
                    "> 分隔线之后为转换正文，上方 front matter 是本项目的登记信息。", "", "---", "",
                ]) + "\n")
                f.write(md_text.strip() + "\n")
            print(f"[{stem}] -> {md_path(stem)}（{len(md_text.splitlines())} 行，"
                  f"图 {assets['count']} 个{'，字节已落盘' if assets['kept'] else '，仅清单'}）")
    print("转换完成；运行 _scripts/build_index.py 刷新 index.csv。")


if __name__ == "__main__":
    main()
