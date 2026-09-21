"""Convert local PDFs through the MinerU cloud API (https://mineru.net).

Preferred over the local service: no models to install, and the account has a
daily free page quota. The token comes from the MINERU_APIKEY environment
variable (falling back to the Windows user environment).

Usage:
    mineru_cloud.py [--model-version vlm|pipeline] [--lang en]
                    [--keep-images] [--force] [--timeout 1800] [stem ...]

Writes md/<stem>.md and json/<stem>.json, optionally assets/<stem>/.
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

from stem import (assets_dir, base, find, front_matter, json_path, load_meta,
                  load_provenance, md_path, pdf_dir, pdf_path, save_provenance, slugify)

API = "https://mineru.net/api/v4"
UA = "MemoryResearch/1.0 (mineru cloud client)"
DONE = "done"
FAILED = "failed"
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"}


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


def rewrite_image_refs(md_text, stem):
    """MinerU writes ![](images/x.jpg); point it at ../assets/<stem>/ instead so
    the reference stays valid wherever md/ is read from."""
    target = f"../assets/{stem}/"
    md_text = re.sub(r"\]\(images/", "](" + target, md_text)
    md_text = re.sub(r'(src=)"images/', r'\1"' + target, md_text)
    return md_text


def image_entries(zf):
    return [n for n in zf.namelist()
            if os.path.splitext(n)[1].lower() in IMAGE_EXT and not n.endswith("/")]


def figure_captions(zf, json_name):
    """Captions from content_list let you find a figure by text without opening it."""
    if not json_name:
        return []
    try:
        items = json.loads(zf.read(json_name).decode("utf-8", "replace"))
    except ValueError:
        return []
    if isinstance(items, dict):
        items = items.get("content_list") or []
    out = []
    for item in items or []:
        if not isinstance(item, dict) or item.get("type") != "image":
            continue
        caption = " ".join(str(item.get(k) or "") for k in ("caption", "img_caption", "text")).strip()
        out.append({"n": len(out) + 1, "page": item.get("page_idx"),
                    "caption": caption or None,
                    "file": os.path.basename(str(item.get("img_path") or "")) or None})
    return out


def write_assets(zf, stem, keep_images, figures):
    """Images are derived: bytes are optional, the manifest is always written."""
    names = sorted(image_entries(zf))
    directory = assets_dir(stem)
    images = []
    for name in names:
        payload = zf.read(name)
        images.append({"file": os.path.basename(name), "bytes": len(payload),
                       "sha256": hashlib.sha256(payload).hexdigest()})
    if images:
        os.makedirs(directory, exist_ok=True)
        if keep_images:
            for name in names:
                with open(os.path.join(directory, os.path.basename(name)), "wb") as f:
                    f.write(zf.read(name))
        with open(os.path.join(directory, "manifest.json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump({"stem": stem, "generated_by": "mineru-cloud",
                       "images": images, "figures": figures}, f, ensure_ascii=False, indent=2)
            f.write("\n")
    return {"count": len(images), "bytes": sum(i["bytes"] for i in images),
            "kept": bool(keep_images and images),
            "manifest": f"assets/{stem}/manifest.json" if images else None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-version", default="vlm")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--keep-images", action="store_true", help="把图片字节写入 assets/（默认只写清单）")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("tokens", nargs="*")
    args = ap.parse_args()

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
            md_text = rewrite_image_refs(zf.read(md_name).decode("utf-8", "replace"), stem)
            json_name = pick(zf, "_content_list.json")
            if json_name:
                os.makedirs(os.path.dirname(json_path(stem)), exist_ok=True)
                with open(json_path(stem), "wb") as f:
                    f.write(zf.read(json_name))
            assets = write_assets(zf, stem, args.keep_images, figure_captions(zf, json_name))

            stamp = datetime.now(timezone.utc).isoformat()
            record = provenance[stem]
            os.makedirs(os.path.dirname(md_path(stem)), exist_ok=True)
            with open(md_path(stem), "w", encoding="utf-8", newline="\n") as f:
                f.write(front_matter(stem, meta.get(stem, {}), find(stem), record))
                f.write("\n".join([
                    f"# {meta.get(stem, {}).get('title') or stem}（MinerU 云端转换）", "",
                    f"- 解析器: MinerU cloud（model_version {args.model_version}；语言 {args.lang}）",
                    f"- 转换时间: {stamp}",
                    f"- 本地 PDF SHA256: `{record['pdf_sha256']}`",
                    f"- 图片: {assets['count']} 个，{assets['bytes'] // 1024} KB；"
                    + ("字节已写入 assets/" + stem if assets["kept"]
                       else "字节未保留，只写清单（--keep-images 可取回）"), "",
                    "> 本文件由 MinerU 云端接口转换，**转换成功不等于已对 PDF 做视觉核验**。",
                    "> 表格、公式与图像仍需在使用时核对；结构化输出见 json/ 下的同名文件。",
                    "> 下方分隔线之后为转换正文，不含本项目的阅读建议。", "", "---", "",
                ]) + "\n")
                f.write(md_text.strip() + "\n")
            record["conversion"] = {
                "path": os.path.relpath(md_path(stem), base()).replace(os.sep, "/"),
                "parser": "mineru-cloud",
                "api": API,
                "model_version": args.model_version,
                "lang": args.lang,
                "batch_id": batch_id,
                "task_id": result.get("task_id"),
                "full_zip_url": result.get("full_zip_url"),
                "converted_at": stamp,
                "pdf_sha256": record["pdf_sha256"],
                "body_sha256": hashlib.sha256(md_text.encode("utf-8")).hexdigest(),
                "structured_path": (os.path.relpath(json_path(stem), base()).replace(os.sep, "/")
                                    if json_name else None),
                "images": assets,
                "options": {"model_version": args.model_version, "lang": args.lang},
                "visual_verification": False,
            }
            save_provenance(provenance)
            print(f"[{stem}] -> {md_path(stem)}（{len(md_text.splitlines())} 行，"
                  f"图 {assets['count']} 个{'，已保留字节' if assets['kept'] else '，仅清单'}）")
    print("转换完成；运行 _scripts/build_index.py 刷新 index.json。")


if __name__ == "__main__":
    main()
