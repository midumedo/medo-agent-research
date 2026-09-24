"""Download an arXiv PDF and metadata from the same explicit version.

Usage: download_arxiv.py [stem ...] or download_arxiv.py --all
A stem is `arxiv-<id>` (bare arXiv ids still work). The PDF is written to
`pdf/<stem>.pdf` and all records are keyed by the stem. Existing PDFs are
preserved together with their existing metadata. To fetch a different version,
pass a versioned id (e.g. arxiv-2512.13564v2); it gets its own file.
"""

import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV_API = "http://export.arxiv.org/api/query?id_list={}&max_results=1"


from stem import find, native_for, pdf_path, slugify, stem_of

UA = "MemoryResearch/1.0 (local paper archive)"


def resolve_meta(aid):
    """(versioned_id, published, updated) from the official API, or (None, None, None).

    `updated` is when the current version was posted — the date that belongs with
    the `vN` in the id. `published` is v1; it is kept as a separate fact.
    """
    base = re.sub(r"v\d+$", "", aid)
    try:
        req = urllib.request.Request(ARXIV_API.format(base), headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as response:
            root = ET.fromstring(response.read())
    except Exception:
        return None, None, None
    for entry in root.findall(ATOM + "entry"):
        raw = entry.findtext(ATOM + "id", "").rsplit("/", 1)[-1]
        published = (entry.findtext(ATOM + "published", "") or "").strip() or None
        updated = (entry.findtext(ATOM + "updated", "") or "").strip() or None
        if re.fullmatch(r"\d{4}\.\d{4,5}v\d+", raw):
            return raw, published, updated
    return None, None, None


def get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.status, response.read()


def fetch_meta(aid):
    url = f"https://arxiv.org/abs/{aid}"
    try:
        _, data = get(url)
    except Exception as error:
        return {"id": aid, "error": f"abs fetch failed: {error}"}
    txt = data.decode("utf-8", "replace")

    def grab(name):
        match = re.search(rf'<meta name="{name}" content="(.*?)"', txt, re.S)
        return html.unescape(match.group(1).strip()) if match else None

    title = grab("citation_title")
    base = re.sub(r"v\d+$", "", aid)
    version = aid if re.search(r"v[1-9]\d*$", aid) else None
    if not version:
        pdf_url = grab("citation_pdf_url") or ""
        match = re.search(rf"/pdf/({re.escape(base)}v[1-9]\d*)(?:\.pdf)?$", pdf_url)
        if not match:
            # Only use the displayed arXiv identity, not dates or history order.
            identity = re.search(r'<span class="arxivid">(.*?)</span>', txt, re.S)
            match = re.search(rf"arXiv:\s*({re.escape(base)}v[1-9]\d*)\b", identity.group(1)) if identity else None
        version = match.group(1) if match else None
    abstract_match = re.search(r'<blockquote class="abstract[^"]*">(.*?)</blockquote>', txt, re.S)
    abstract = None
    if abstract_match:
        abstract = html.unescape(re.sub(r"<.*?>", " ", abstract_match.group(1)))
        abstract = re.sub(r"\s+", " ", abstract).replace("Abstract:", "").strip()
    return {
        "id": aid,
        "title": title,
        "authors": [html.unescape(a.strip()) for a in re.findall(r'<meta name="citation_author" content="(.*?)"', txt, re.S)],
        "date": grab("citation_date"),
        "abstract": abstract,
        "exists": bool(title),
        "url": url,
        "versioned_id": version,
    }


def fetch_pdf(versioned_id):
    if not re.fullmatch(r"\d{4}\.\d{4,5}v[1-9]\d*", versioned_id):
        raise ValueError("PDF download requires an explicit arXiv version")
    _, data = get(f"https://arxiv.org/pdf/{versioned_id}")
    if len(data) < 20000 or not data.startswith(b"%PDF"):
        raise ValueError("response is not a plausible PDF")
    return data


def download_one(token, meta=None, provenance=None):
    record = find(token)
    aid = native_for(token, record)
    stem = stem_of(record) if record else None
    if stem and os.path.exists(pdf_path(stem)):
        # Do not fetch latest metadata for a legacy/cached PDF.
        return f"[{stem}] cached PDF preserved; version lives in its filename"
    if not aid or not re.fullmatch(r"\d{4}\.\d{4,5}(?:v[1-9]\d*)?", aid):
        return f"[{token}] 只有 arXiv 来源能自动下载：给出 arXiv 编号或已入库的标识／标题；非 arXiv 请手工放入 pdf/ 再跑 mineru_cloud.py"

    candidate = fetch_meta(aid)
    if not candidate.get("exists"):
        return f"[{token}] metadata unavailable; existing records preserved"
    versioned_id = candidate.get("versioned_id")
    published_at = revised = None
    if not versioned_id:
        # Fall back to the API; the abs page alone no longer guarantees a versioned identity.
        versioned_id, published_at, revised = resolve_meta(aid)
    if not versioned_id:
        return f"[{token}] version unresolved; unchanged. Retry with an explicit version after checking the intended version."
    if aid != versioned_id:
        candidate = fetch_meta(versioned_id)
        if not candidate.get("exists"):
            return f"[{token}] versioned metadata unavailable; existing records preserved"
    try:
        data = fetch_pdf(versioned_id)
    except Exception as error:
        return f"[{token}] PDF unavailable ({error}); existing records preserved"

    stem = stem or slugify(candidate.get("title") or "")
    if not stem:
        return f"[{token}] 元数据没有标题，无法定文件名；未写入"
    dest = pdf_path(stem)
    if os.path.exists(dest) and not record:
        return f"[{stem}] 同名文件已存在，未覆盖；先确认是不是同一篇"
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    temporary = dest + ".tmp"
    with open(temporary, "wb") as f:
        f.write(data)
    os.replace(temporary, dest)
    candidate["id"] = stem
    candidate["native_id"] = aid
    candidate["registry"] = "arxiv"
    candidate["versioned_id"] = versioned_id
    if published_at:
        candidate["published_at"] = published_at
    if revised:
        candidate["revised"] = revised[:10]
    # 元数据不再另存一份：转换后由人／agent 现查写入 md 的登记块。
    # 需要时可随时重取，留一份快照只会随时间腐坏。
    return f"[{stem}] saved {versioned_id} ({len(data) // 1024} KB)"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--all" in sys.argv[1:] or not args:
        # 不再读一份单独的清单：pdf/ 里现有篇目就是范围，index.csv 的 id 列是权威。
        args = [r["id"] for r in stem.records()]
    if not args:
        print("no ids given")
        return
    for aid in args:
        print(download_one(aid))
        if len(args) > 1:
            time.sleep(1.5)


if __name__ == "__main__":
    main()
