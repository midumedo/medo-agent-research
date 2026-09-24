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
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timezone

from stem import (assets_root, base, find, front_matter, load_meta,
                  load_provenance, md_path, pdf_dir, pdf_path, save_provenance,
                  slugify, version_suffix)

API = "https://mineru.net/api/v4"
UA = "MemoryResearch/1.0 (mineru cloud client)"
DONE = "done"
FAILED = "failed"
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"}

# Content List V1 field names. The official name is `image_caption`; the older
# spellings stay as fallbacks in case a server revision differs.
CAPTION_KEY = {"image": "image_caption", "table": "table_caption",
               "chart": "image_caption", "equation": None}
CAPTION_FALLBACKS = ("image_caption", "table_caption", "caption", "img_caption")
KIND_TOKEN = {"image": "fig", "table": "table", "chart": "chart", "equation": "eq"}
NUM_RE = re.compile(r"(?:figure|fig\.?|图|table|tab\.?|表)\s*([0-9]+[a-z]?)", re.I)


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
    with open(path, "rb") as f:
        payload = f.read()
    req = urllib.request.Request(url, data=payload, headers={"User-Agent": UA}, method="PUT")
    with urllib.request.urlopen(req, timeout=600) as resp:
        return resp.status


def poll(batch_id, stems, timeout):
    deadline = time.time() + timeout
    last = ""
    while time.time() < deadline:
        response = request(API + f"/extract-results/batch/{batch_id}", headers=auth())
        if response.get("code") != 0:
            raise SystemExit(f"查询结果失败：{response.get('msg')} / {response.get('trace_id')}")
        results = (response.get("data") or {}).get("extract_result") or []
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


def identity_for(stem, meta, prov):
    """The `id` used to prefix image names: `<registry>-<native-id><vN>`."""
    record = find(stem) or {}
    if record.get("id"):
        return record["id"]
    registry = meta.get("registry") or "arxiv"
    native = meta.get("native_id") or ""
    suffix = version_suffix(prov.get("version") or meta.get("versioned_id") or "")
    return f"{registry}-{native}{suffix}" if native else stem


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
            caption = " ".join(str(p) for p in parts if p).strip()
            if caption:
                break
        match = NUM_RE.search(caption)
        out.append({"img_path": item.get("img_path") or "",
                    "kind": kind,
                    "number": match.group(1) if match else None,
                    "caption": caption or None,
                    "page": item.get("page_idx")})
    return out


def name_map(items, ident):
    """img_path -> `<ident>-<token><n>.<ext>`; duplicates get `-2`, `-3`.

    Naming by figure number is what makes a caption findable without opening the
    image; numbers without a caption fall back to that kind's running sequence.
    """
    used, seq, dup = {}, {}, {}
    for item in items:
        path = item["img_path"]
        if not path:
            continue
        kind_token = KIND_TOKEN[item["kind"]]
        seq[kind_token] = seq.get(kind_token, 0) + 1
        stem_name = f"{ident}-{kind_token}{item['number'] or seq[kind_token]}"
        ext = os.path.splitext(path)[1].lower() or ".png"
        name = stem_name + ext
        while name in used.values():
            dup[stem_name] = dup.get(stem_name, 1) + 1
            name = f"{stem_name}-{dup[stem_name]}{ext}"
        used[path] = name
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
    """Images land flat in assets/, renamed by figure number; the manifest always lands."""
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
    figures = [{"n": index + 1, "kind": item["kind"], "number": item["number"],
                "page": item["page"], "caption": item["caption"],
                "file": mapping.get(item["img_path"])}
               for index, item in enumerate(items)]
    manifest = None
    if entries:
        manifest = os.path.join(directory, f"{stem}.manifest.json")
        with open(manifest, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"stem": stem, "id": ident, "images": images, "figures": figures},
                      f, ensure_ascii=False, indent=2)
            f.write("\n")
    return {"count": len(images),
            "bytes": sum(i["bytes"] for i in images),
            "kept": bool(keep_images and images),
            "manifest": f"assets/{stem}.manifest.json" if manifest else None}


def parser_label(result, model_version):
    """Prefer a server-reported version; fall back to the model tier we asked for.

    Never issue an extra request just to learn a version number.
    """
    for key in ("version", "parser_version", "model_version"):
        value = str(result.get(key) or "").strip()
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
        stems.append(record["stem"] if record else slugify(raw))
    if not stems:
        stems = sorted(os.path.splitext(f)[0] for f in os.listdir(pdf_dir()) if f.lower().endswith(".pdf"))
    stems = [s for s in stems if os.path.exists(pdf_path(s))]
    if not stems:
        print("没有可转换的 PDF。")
        return

    provenance = load_provenance()
    meta = load_meta()
    todo = []
    for stem in stems:
        with open(pdf_path(stem), "rb") as f:
            pdf_hash = hashlib.sha256(f.read()).hexdigest()
        record = provenance.setdefault(stem, {})
        if record.get("pdf_sha256") and record["pdf_sha256"] != pdf_hash:
            raise SystemExit(f"[{stem}] PDF 与已记录 SHA256 不一致，请先调查来源变化")
        record["pdf_sha256"] = pdf_hash
        record["pdf_path"] = os.path.relpath(pdf_path(stem), base()).replace(os.sep, "/")
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
            entry_meta = meta.get(stem, {})
            ident = identity_for(stem, entry_meta, provenance[stem])
            items = parse_visual(load_content_list(zf, pick(zf, "_content_list.json")))
            mapping = name_map(items, ident)
            md_text = rewrite_image_refs(zf.read(md_name).decode("utf-8", "replace"), mapping)
            assets = write_assets(zf, stem, ident, items, mapping, keep_images)

            stamp = datetime.now(timezone.utc).isoformat()
            label = parser_label(result, args.model_version)
            state = ["downloaded", "converted"] + (["imaged"] if assets["count"] else [])
            record = provenance[stem]
            record["state"] = state
            os.makedirs(os.path.dirname(md_path(stem)), exist_ok=True)
            with open(md_path(stem), "w", encoding="utf-8", newline="\n") as f:
                f.write(front_matter(stem, entry_meta, find(stem), record,
                                     keywords=None, abstract=None,
                                     date=None, parser=label, state=state))
                f.write("\n".join([
                    f"# {entry_meta.get('title') or stem}（MinerU 云端转换）", "",
                    f"- 解析器: {label}（语言 {args.lang}）",
                    f"- 转换时间: {stamp}",
                    f"- 本地 PDF SHA256: `{record['pdf_sha256']}`",
                    f"- 图片: {assets['count']} 个，{assets['bytes'] // 1024} KB；"
                    + ("字节已写入 assets/" if assets["kept"] else "字节未保留，只写清单"),
                    "",
                    "> 本文件由 MinerU 云端接口转换，转换成功不等于已对 PDF 做视觉核验。",
                    "> 表格、公式与图像仍需在使用时核对；引用具体数字请回 pdf/ 定位原文。",
                    "> 分隔线之后为转换正文，上方 front matter 是本项目的登记信息。", "", "---", "",
                ]) + "\n")
                f.write(md_text.strip() + "\n")
            record["conversion"] = {
                "path": os.path.relpath(md_path(stem), base()).replace(os.sep, "/"),
                "parser": label,
                "api": API,
                "model_version": args.model_version,
                "lang": args.lang,
                "batch_id": batch_id,
                "task_id": result.get("task_id"),
                "full_zip_url": result.get("full_zip_url"),
                "converted_at": stamp,
                "pdf_sha256": record["pdf_sha256"],
                "body_sha256": hashlib.sha256(md_text.encode("utf-8")).hexdigest(),
                "images": assets,
                "options": {"model_version": args.model_version, "lang": args.lang,
                            "keep_images": keep_images},
                "visual_verification": False,
            }
            save_provenance(provenance)
            print(f"[{stem}] -> {md_path(stem)}（{len(md_text.splitlines())} 行，"
                  f"图 {assets['count']} 个{'，字节已落盘' if assets['kept'] else '，仅清单'}）")
    print("转换完成；运行 _scripts/build_index.py 刷新 index.csv。")


if __name__ == "__main__":
    main()
