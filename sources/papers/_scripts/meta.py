"""步骤① 元数据：按 id 取 arXiv 元数据（标题、版本标识、修订日期、摘要、来源）。

这一层只回答「一篇论文是什么」。它不下载 PDF（那是 ② `pdf.py`），也不转换正文
（那是 ③ `convert.py`）。

两条取法，从稳到宽：
  1. `resolve_meta()` 走官方 Atom API（export.arxiv.org）——返回当前版本号与修订日；
  2. `fetch_meta()` 抓 abs 页面——给出标题、作者、日期与摘要。

Usage:
    meta.py <arXiv 编号 | 已入库的 id | 文件名 | 标题 ...>
"""

import html
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stem  # noqa: E402

ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV_API = "http://export.arxiv.org/api/query?id_list={}&max_results=1"
UA = "MemoryResearch/1.0 (local paper archive)"


def get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.status, response.read()


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


def fetch_meta(aid):
    """The abs page as a dict: title, authors, date, abstract, versioned_id, exists.

    `abstract` is read from the page's `<blockquote class="abstract">`; when the
    page has no such block the field is None — never filled in from a guess.
    """
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
        abstract = re.sub(r"\s+", " ", abstract).replace("Abstract:", "").strip() or None
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


def native_id(token):
    """arXiv 编号 for a CLI token: a bare number, or the id behind a library row."""
    if re.fullmatch(r"\d{4}\.\d{4,5}(?:v[1-9]\d*)?", token or ""):
        return token
    record = stem.find(token)
    if record:
        return stem.native_from_id(record.get("id")) or None
    match = re.fullmatch(r"arxiv-(\d{4}\.\d{4,5}(?:v[1-9]\d*)?)", (token or "").strip())
    return match.group(1) if match else None


def main():
    tokens = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not tokens:
        print("用法：meta.py <arXiv 编号 | id | 文件名 | 标题>")
        return
    for token in tokens:
        aid = native_id(token)
        if not aid:
            print(f"[{token}] 不是 arXiv 来源，无法取元数据；非 arXiv 请手工登记。")
            continue
        info = fetch_meta(aid)
        print(f"[{token}] versioned_id={info.get('versioned_id')} "
              f"revised={info.get('date')} title={info.get('title')} "
              f"abstract={'有' if info.get('abstract') else '无'}")


if __name__ == "__main__":
    main()
