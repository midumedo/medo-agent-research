"""MinerU v4 transport and in-memory conversion of its result archive.

This module owns no library paths. It consumes the returned Markdown and media
relations, and returns ready-to-write text and image bytes to the caller.
"""

from __future__ import annotations

import html
import http.client
import io
import ipaddress
import json
import os
from pathlib import Path
import posixpath
import re
import socket
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile

from pdf_markdown import rewrite_links as _rewrite_references


API = "https://mineru.net/api/v4"
USER_AGENT = "PDFManager/1.0 (MinerU cloud client)"
BATCH_SIZE = 50
POLL_INTERVAL = 3
CDN_HOSTS = {"cdn-mineru.openxlab.org.cn"}
DOH_RESOLVERS = ("https://dns.alidns.com/resolve", "https://cloudflare-dns.com/dns-query")
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".jp2"}
KINDS = {"image": "fig", "chart": "chart", "table": "table", "equation": "eq",
         "equation_interline": "eq"}
CAPTION_KEYS = {"image": "image_caption", "chart": "chart_caption", "table": "table_caption"}
NUMBER_RE = re.compile(r"(?:figure|fig\.?|图|table|tab\.?|表|chart)\s*([0-9]+[a-z]?)", re.I)
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


class MinerUError(RuntimeError):
    """An actionable API, upload, or returned-archive failure."""


def api_key():
    value = os.environ.get("MINERU_APIKEY", "").strip()
    if value:
        return value
    if sys.platform == "win32":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
                value = str(winreg.QueryValueEx(key, "MINERU_APIKEY")[0]).strip()
            if value:
                return value
        except (OSError, ImportError):
            pass
    raise MinerUError("没有取到 MINERU_APIKEY；请设置环境变量后重试。")


def _request_json(route, key, data=None):
    headers = {"User-Agent": USER_AGENT, "Authorization": "Bearer " + key}
    encoded = None
    if data is not None:
        headers["Content-Type"] = "application/json"
        encoded = json.dumps(data, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(API + route, data=encoded, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        raise MinerUError(f"MinerU 请求失败：HTTP {error.code}") from error
    except (urllib.error.URLError, OSError) as error:
        raise MinerUError("无法连接 MinerU，请稍后重试。") from error
    except (ValueError, UnicodeError) as error:
        raise MinerUError("MinerU 返回了无法读取的 JSON。") from error
    if not isinstance(result, dict):
        raise MinerUError("MinerU 返回格式错误：应为 JSON 对象。")
    if result.get("code") != 0:
        raise MinerUError(f"MinerU 错误 {result.get('code')}：{result.get('msg', '未知错误')}")
    data = result.get("data") or {}
    if not isinstance(data, dict):
        raise MinerUError("MinerU 返回格式错误：data 应为 JSON 对象。")
    return data


def _upload_file(url, path):
    """Signed PUT must not acquire urllib's implicit Content-Type header."""
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in {"http", "https"}:
        raise MinerUError("MinerU 上传地址不是 HTTP(S)。")
    connection_type = http.client.HTTPSConnection if parts.scheme == "https" else http.client.HTTPConnection
    connection = connection_type(parts.netloc, timeout=600)
    try:
        payload = Path(path).read_bytes()
        target = parts.path + (("?" + parts.query) if parts.query else "")
        connection.request("PUT", target, body=payload,
                           headers={"User-Agent": USER_AGENT, "Content-Length": str(len(payload))})
        response = connection.getresponse()
        response.read()
        if not 200 <= response.status < 300:
            raise MinerUError(f"文件上传失败：HTTP {response.status}")
    except (OSError, http.client.HTTPException) as error:
        raise MinerUError(f"无法上传本地文件 {Path(path).name}") from error
    finally:
        connection.close()


def _doh_addresses(host, resolver):
    """Resolve only the public CDN hostname, never its signed URL or API token."""
    query = urllib.parse.urlencode({"name": host, "type": "A"})
    request = urllib.request.Request(resolver + "?" + query,
                                     headers={"Accept": "application/dns-json", "User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=12) as response:
        result = json.loads(response.read().decode("utf-8"))
    if not isinstance(result, dict) or result.get("Status") != 0:
        return []
    addresses = []
    for answer in result.get("Answer") or []:
        if not isinstance(answer, dict) or answer.get("type") != 1:
            continue
        try:
            address = ipaddress.ip_address(answer.get("data", ""))
        except ValueError:
            continue
        if address.version == 4 and address.is_global and str(address) not in addresses:
            addresses.append(str(address))
    return addresses[:2]


class _HTTPSAtAddress(http.client.HTTPSConnection):
    """Use a fresh DNS address while authenticating the original HTTPS host."""

    def __init__(self, host, address, timeout=30):
        super().__init__(host, timeout=timeout, context=ssl.create_default_context())
        self.address = address

    def connect(self):
        raw = socket.create_connection((self.address, self.port), timeout=self.timeout)
        try:
            # Host and certificate/SNI identity remain the original CDN domain.
            self.sock = self._context.wrap_socket(raw, server_hostname=self.host)
        except Exception:
            raw.close()
            raise


def _download_at_address(url, address):
    parts = urllib.parse.urlsplit(url)
    connection = _HTTPSAtAddress(parts.hostname, address)
    try:
        connection.connect()
        connection.sock.settimeout(600)
        target = parts.path or "/"
        if parts.query:
            target += "?" + parts.query
        # http.client generates Host from connection.host, not the socket IP.
        connection.request("GET", target, headers={"User-Agent": USER_AGENT})
        response = connection.getresponse()
        if response.status != 200:
            raise urllib.error.HTTPError(url, response.status, "CDN download failed", response.headers, None)
        return response.read()
    finally:
        connection.close()


def _cdn_fallback(url):
    host = urllib.parse.urlsplit(url).hostname
    seen = set()
    for resolver in DOH_RESOLVERS:
        try:
            addresses = _doh_addresses(host, resolver)
        except (OSError, ValueError, http.client.HTTPException):
            continue
        for address in addresses:
            if address in seen:
                continue
            seen.add(address)
            try:
                return _download_at_address(url, address)
            except urllib.error.HTTPError as error:
                # A real HTTP denial/expired object is not a DNS or TLS failure.
                raise MinerUError(f"MinerU 结果下载返回 HTTP {error.code}；请使用批次编号重新查询。") from error
            except (OSError, http.client.HTTPException):
                continue
    raise MinerUError("MinerU CDN 常规连接与实时 DNS 地址重试均失败；可使用批次编号继续查询。")


def _download_zip(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=600) as response:
            payload = response.read()
    except urllib.error.HTTPError as error:
        raise MinerUError(f"MinerU 结果下载返回 HTTP {error.code}；请使用批次编号重新查询。") from error
    except (OSError, http.client.HTTPException) as error:
        parts = urllib.parse.urlsplit(url)
        if parts.scheme != "https" or parts.hostname not in CDN_HOSTS or parts.port not in (None, 443):
            reason = type(getattr(error, "reason", error)).__name__
            raise MinerUError(f"MinerU 结果 ZIP 下载失败（{reason}）；可使用批次编号继续查询。") from error
        print("MinerU CDN 常规连接失败，尝试实时 DNS 地址（保留 HTTPS 证书校验）。", file=sys.stderr, flush=True)
        payload = _cdn_fallback(url)
    if not zipfile.is_zipfile(io.BytesIO(payload)):
        raise MinerUError("MinerU 结果不是有效 ZIP。")
    return payload


def _match_results(jobs, records):
    by_id = {str(r.get("data_id")): r for r in records if isinstance(r, dict) and r.get("data_id")}
    by_name = {r.get("file_name"): r for r in records if isinstance(r, dict) and r.get("file_name")}
    return {job["data_id"]: by_id.get(str(job["data_id"])) or by_name.get(job["name"])
            for job in jobs}


def _poll_batch(batch_id, jobs, key, timeout):
    deadline = time.monotonic() + max(0, timeout)
    matched = {job["data_id"]: None for job in jobs}
    while True:
        data = _request_json("/extract-results/batch/" + urllib.parse.quote(batch_id, safe=""), key)
        records = data.get("extract_result") or []
        if not isinstance(records, list):
            raise MinerUError("MinerU 批次结果格式错误：extract_result 应为列表。")
        current = _match_results(jobs, records)
        # Retain already reported terminal entries if the service sends a partial snapshot.
        for ident, record in current.items():
            if record:
                matched[ident] = record
        if all(record and record.get("state") in {"done", "failed"} for record in matched.values()):
            return matched
        if time.monotonic() >= deadline:
            return matched
        time.sleep(min(POLL_INTERVAL, max(0, deadline - time.monotonic())))


def _batch_results(batch_id, jobs, key, timeout):
    try:
        records = _poll_batch(batch_id, jobs, key, timeout)
    except MinerUError as error:
        for job in jobs:
            yield {"data_id": job["data_id"], "file_name": job["name"], "state": "pending",
                   "batch_id": batch_id, "error": f"查询中断：{error}；可继续查询，无需重新提交。"}
        return
    for job in jobs:
        record = records.get(job["data_id"]) or {}
        state = record.get("state") or "pending"
        result = {"data_id": job["data_id"], "file_name": job["name"],
                  "state": state, "batch_id": batch_id}
        if state == "done":
            url = record.get("full_zip_url")
            if not url:
                result.update(state="failed", error="任务已完成，但结果没有 full_zip_url。")
            else:
                try:
                    result["zip_bytes"] = _download_zip(url)
                except MinerUError as error:
                    result.update(state="failed", error=str(error))
        elif state == "failed":
            result["error"] = record.get("err_msg") or "MinerU 解析失败。"
        else:
            result["error"] = f"等待超时；批次 {batch_id} 的该文件仍为 {state}，可继续查询。"
        yield result


def convert_files(jobs, *, model_version="vlm", language="ch", enable_formula=True,
                  enable_table=True, is_ocr=False, timeout=1800, batch_id=None):
    """Yield one result per job; resuming a batch never uploads or submits again."""
    jobs = [dict(job) for job in jobs]
    if not jobs:
        return
    names = [job.get("name") for job in jobs]
    identifiers = [job.get("data_id") for job in jobs]
    if any(not value for value in names + identifiers):
        raise MinerUError("每个转换文件都需要 name 和 data_id。")
    if len(set(names)) != len(names) or len(set(identifiers)) != len(identifiers):
        raise MinerUError("同次转换中的文件名和 data_id 必须各自唯一。")
    key = api_key()
    if batch_id:
        yield from _batch_results(batch_id, jobs, key, timeout)
        return
    for start in range(0, len(jobs), BATCH_SIZE):
        chunk = jobs[start:start + BATCH_SIZE]
        data = _request_json("/file-urls/batch", key, {
            "files": [{"name": job["name"], "data_id": job["data_id"], "is_ocr": bool(is_ocr)}
                      for job in chunk],
            "model_version": model_version, "language": language,
            "enable_formula": bool(enable_formula), "enable_table": bool(enable_table),
        })
        current_batch = data.get("batch_id")
        urls = data.get("file_urls")
        if not current_batch or not isinstance(urls, list) or len(urls) != len(chunk):
            raise MinerUError("MinerU 返回的批次编号或上传链接数量与请求不符，未上传。")
        print(f"MinerU batch_id={current_batch}；{len(chunk)} 个文件", file=sys.stderr, flush=True)
        submitted = []
        for job, url in zip(chunk, urls):
            try:
                _upload_file(url, job["path"])
                submitted.append(job)
            except MinerUError as error:
                yield {"data_id": job["data_id"], "file_name": job["name"], "state": "failed",
                       "batch_id": current_batch, "error": str(error)}
        if submitted:
            yield from _batch_results(current_batch, submitted, key, timeout)


def _plain(value):
    if isinstance(value, str):
        return html.unescape(re.sub(r"<[^>]+>", "", value))
    if isinstance(value, list):
        return " ".join(_plain(item) for item in value)
    if isinstance(value, dict):
        return _plain(value.get("content", value.get("text", "")))
    return ""


def _visual_records(value, v2=False):
    if isinstance(value, list):
        for item in value:
            yield from _visual_records(item, v2)
    elif isinstance(value, dict):
        kind = value.get("type")
        if kind in KINDS:
            content = value.get("content") if v2 else value
            if not isinstance(content, dict):
                return
            source = content.get("image_source") or {}
            path = source.get("path") if v2 and isinstance(source, dict) else content.get("img_path")
            caption = content.get(CAPTION_KEYS.get(kind, "caption"))
            if not caption:
                caption = content.get("caption") or content.get("img_caption")
            if path:
                yield str(path), KINDS[kind], _plain(caption)
        else:
            for key in ("content_list", "pages", "items"):
                if key in value:
                    yield from _visual_records(value[key], v2)


def _member_path(path):
    return posixpath.normpath(str(path).replace("\\", "/"))


def _resolve_media(path, candidates, markdown_name):
    path = html.unescape(str(path)).strip()
    parsed = urllib.parse.urlsplit(path)
    if parsed.scheme or parsed.netloc:
        return None
    raw = urllib.parse.unquote(parsed.path)
    raw = re.sub(r"\\([\\ ()])", r"\1", raw).replace("\\", "/")
    for candidate in (_member_path(posixpath.join(posixpath.dirname(markdown_name), raw)), _member_path(raw)):
        if candidate in candidates:
            return candidate
    same_name = [name for name in candidates if posixpath.basename(name) == posixpath.basename(raw)]
    return same_name[0] if len(same_name) == 1 else None



def parse_archive(payload, prefix, requested_model="vlm"):
    """Return body, named media bytes, parser label and nonfatal format notices."""
    prefix = re.sub(r'[<>:"/\\|?*\x00-\x1f]', ".", str(prefix)).strip(". ")
    if not prefix:
        raise MinerUError("资产前缀不能为空。")
    warnings = []
    try:
        archive = zipfile.ZipFile(io.BytesIO(payload))
    except (zipfile.BadZipFile, OSError) as error:
        raise MinerUError("MinerU 结果不是有效 ZIP。") from error
    with archive:
        members = {_member_path(name): name for name in archive.namelist() if not name.endswith("/")}
        full = [name for name in members if posixpath.basename(name).lower() == "full.md"]
        markdown = full or [name for name in members if name.lower().endswith(".md")]
        if len(markdown) != 1:
            raise MinerUError("结果 ZIP 需要包含唯一的 full.md 或 Markdown 正文。")
        markdown_name = markdown[0]
        body = archive.read(members[markdown_name]).decode("utf-8-sig", "replace")

        def read_json(suffix):
            names = [name for name in members if name.lower().endswith(suffix)]
            preferred = [name for name in names if posixpath.dirname(name) == posixpath.dirname(markdown_name)]
            selected = preferred or names
            if not selected:
                return []
            if len(selected) != 1:
                warnings.append(f"存在多份 {suffix}，未据此推断图片类型。")
                return []
            try:
                return json.loads(archive.read(members[selected[0]]).decode("utf-8-sig"))
            except (ValueError, UnicodeError):
                warnings.append(f"无法读取 {suffix}，相关图片使用其他可用关系或 img 分类。")
                return []

        v1 = list(_visual_records(read_json("content_list.json")))
        v2 = list(_visual_records(read_json("content_list_v2.json"), True))
        image_members = {name for name in members if posixpath.splitext(name)[1].lower() in IMAGE_EXTENSIONS}
        images = {name for name in image_members if "images" in name.split("/")[:-1]}
        if not images:
            images = set(image_members)
        for path, _, _ in v1 + v2:
            resolved = _resolve_media(path, image_members, markdown_name)
            if resolved:
                images.add(resolved)

        mapping, sequences, used = {}, {}, set()

        def assign(path, kind, caption=""):
            if path in mapping:
                return
            sequences[kind] = sequences.get(kind, 0) + 1
            number = NUMBER_RE.search(caption)
            number = number.group(1) if number else str(sequences[kind])
            extension = posixpath.splitext(path)[1].lower()
            base = f"{prefix}-{kind}{number}"
            filename = base + extension
            duplicate = 1
            while filename.casefold() in used:
                duplicate += 1
                filename = f"{base}-{duplicate}{extension}"
            used.add(filename.casefold())
            mapping[path] = filename

        for path, kind, caption in v1 + v2:
            resolved = _resolve_media(path, images, markdown_name)
            if resolved:
                assign(resolved, kind, caption)
        for path in sorted(images):
            assign(path, "img")

        def replacement(path):
            resolved = _resolve_media(path, images, markdown_name)
            if resolved:
                return "../assets/" + urllib.parse.quote(mapping[resolved], safe="-._~")
            parsed = urllib.parse.urlsplit(html.unescape(str(path)))
            if not parsed.scheme and not parsed.netloc and posixpath.splitext(urllib.parse.unquote(parsed.path))[1].lower() in IMAGE_EXTENSIONS:
                raise MinerUError("Markdown 引用的本地图片不在结果包中：" + parsed.path)
            return None

        body = CONTROL_RE.sub("", _rewrite_references(body, replacement)).strip() + "\n"
        if not body.strip():
            raise MinerUError("MinerU 返回的 Markdown 正文为空，未生成转换件。")
        assets = {mapping[name]: archive.read(members[name]) for name in sorted(images)}
        version = None
        layouts = [name for name in members if posixpath.basename(name).lower() == "layout.json"]
        if not layouts:
            layouts = [name for name in members if name.lower().endswith("_middle.json")]
        if len(layouts) == 1:
            raw = archive.read(members[layouts[0]]).decode("utf-8", "replace")
            found = re.search(r'"_version_name"\s*:\s*"([^"]+)"', raw)
            if found:
                version = found.group(1)
        return {"body": body, "assets": assets,
                "parser": "mineru-cloud " + (version or requested_model), "warnings": warnings}
