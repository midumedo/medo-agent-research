"""步骤① 元数据：按 id 取 arXiv 元数据（标题、版本标识、修订日期、摘要、来源）。

这一层只回答「一篇论文是什么」。它不下载 PDF（那是 ② `pdf.py`），也不转换正文
（那是 ③ `convert.py`）。

摘要按稳到宽排成一条链，取不到就留空、**绝不编造**：
  1. `api_entry()` 走官方 Atom API（export.arxiv.org）——`<summary>` 就是摘要；
  2. `fetch_meta()` 抓 abs 页面——`<blockquote class="abstract">` 是摘要；
  3. 两处都拿不到时，把 md 正文里 abstract 附近的窗口交给人／模型判读
     （`--dump-abstract-context`），判完用 `--set-abstract` 写回 md 表头，
     并在 `abstract_trace.md` 追加一行——这就是「提取 abstract 的专用 trace」。

Usage:
    meta.py show <id 或 文件名 ...>
    meta.py --dump-abstract-context <token>     # 打印摘要附近的窗口，供判读
    meta.py --set-abstract <token> <文本>        # 判读结果写回 md 表头 + 记录 trace
"""

import html
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stem  # noqa: E402

ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV_API = "http://export.arxiv.org/api/query?id_list={}&max_results=1"
UA = "MemoryResearch/1.0 (local paper archive)"
TRACE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "abstract_trace.md")


def get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.status, response.read()


def normalize_abstract(text):
    """Flatten whitespace and drop the leading 'Abstract:' label. None when empty."""
    if not text:
        return None
    flat = re.sub(r"<[^>]+>", " ", text)
    flat = html.unescape(flat)
    flat = re.sub(r"\s+", " ", flat).strip()
    flat = re.sub(r"^abstract[:\s]+", "", flat, flags=re.I).strip()
    return flat or None


def api_entry(aid):
    """One Atom API lookup -> dict(versioned_id, published, updated, abstract, title).

    Empty dict when the network or the response fails; the caller treats that as
    "no data", never as "no abstract".
    """
    base = re.sub(r"v\d+$", "", aid)
    try:
        _, data = get(ARXIV_API.format(base))
        root = ET.fromstring(data)
    except Exception:
        return {}
    for entry in root.findall(ATOM + "entry"):
        raw = entry.findtext(ATOM + "id", "").rsplit("/", 1)[-1]
        if not re.fullmatch(r"\d{4}\.\d{4,5}v\d+", raw):
            continue
        return {
            "versioned_id": raw,
            "published": (entry.findtext(ATOM + "published", "") or "").strip() or None,
            "updated": (entry.findtext(ATOM + "updated", "") or "").strip() or None,
            "title": " ".join((entry.findtext(ATOM + "title", "") or "").split()) or None,
            "abstract": normalize_abstract(entry.findtext(ATOM + "summary", "")),
        }
    return {}


def resolve_meta(aid):
    """(versioned_id, published, updated) from the official API, or (None, None, None).

    `updated` is when the current version was posted — the date that belongs with
    the `vN` in the id. `published` is v1; it is kept as a separate fact.
    """
    entry = api_entry(aid)
    return entry.get("versioned_id"), entry.get("published"), entry.get("updated")


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
    abstract = normalize_abstract(abstract_match.group(1)) if abstract_match else None
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


def arxiv_meta(aid):
    """The one dict ③ needs: versioned_id / title / abstract / revised / source.

    Reads the Atom API and the abs page; a field neither carries stays None.
    Returns None only when the paper cannot be found at all.
    """
    entry = api_entry(aid)
    page = fetch_meta(aid)
    if not entry and not page.get("exists"):
        return None
    vid = page.get("versioned_id") or entry.get("versioned_id")
    return {
        "native_id": aid,
        "versioned_id": vid,
        "title": page.get("title") or entry.get("title"),
        "abstract": page.get("abstract") or entry.get("abstract"),
        # `revised` 要的是「当前版本」的日期：API 的 `updated` 才对；abs 页的
        # `citation_date` 是 v1 的投递日，只在 API 取不到时兜底。
        "revised": (entry.get("updated") or "")[:10] or stem.normalize_date(page.get("date")) or None,
        "source": f"https://arxiv.org/abs/{vid or aid}",
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


def dump_abstract_context(token, window=2400):
    """The md body's opening window — where the paper's own abstract sits.

    Used when neither the API nor the abs page yields an abstract: a human or a
    model reads this window and writes the answer back with `set_abstract`.
    Returns None when the md is not on disk yet (convert it first).
    """
    record = stem.find(token)
    if not record:
        return None
    path = stem.md_path(stem.stem_of(record))
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        text = f.read()
    body = stem.body_after_front_matter(text)
    return body[:window].strip()


def trace(line):
    """Append one line to the abstract-extraction trace (created on first use)."""
    if not os.path.exists(TRACE_PATH):
        with open(TRACE_PATH, "w", encoding="utf-8", newline="\n") as f:
            f.write("# abstract_trace · 摘要提取的困难与解法\n\n"
                    "只追加。每次走到人工／模型判读这一级，就记一行："
                    "日期 · id · 为什么自动链失败 · 判定结果。\n\n")
    with open(TRACE_PATH, "a", encoding="utf-8", newline="\n") as f:
        f.write(f"- {date.today().isoformat()} · {line}\n")


def set_abstract(token, text):
    """Write a judged abstract back into the md front matter, and record it.

    The register field's home is the md header; this is the only writer for the
    human-judged case. Builds the whole text before opening the file.
    """
    record = stem.find(token)
    if not record:
        return f"[{token}] 不在 index.csv 里，无法定位 md。"
    name = stem.stem_of(record)
    path = stem.md_path(name)
    if not os.path.exists(path):
        return f"[{name}] 还没有 md，先跑 convert.py 再写摘要。"
    with open(path, encoding="utf-8") as f:
        existing = f.read()
    body = stem.body_after_front_matter(existing)
    head = stem.front_matter(name, record, abstract=text)
    new_text = head + body
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_text)
    trace(f"{record.get('id')} · 自动链（API summary + abs 页）均无摘要，人工／模型判读后写下 {len(text)} 字")
    return f"[{name}] abstract 已写入表头（{len(text)} 字），并记入 abstract_trace.md"


def main():
    argv = sys.argv[1:]
    if not argv:
        print("用法：meta.py show <id ...> | --dump-abstract-context <token> | --set-abstract <token> <文本>")
        return
    if argv[0] == "--dump-abstract-context":
        for token in argv[1:]:
            window = dump_abstract_context(token)
            if window is None:
                print(f"[{token}] 没有可读的 md；先跑 convert.py，再回来判读摘要。")
            else:
                print(f"===== {token} · abstract 附近 =====\n{window}\n")
        return
    if argv[0] == "--set-abstract":
        if len(argv) < 3:
            print("用法：meta.py --set-abstract <token> <文本>")
            return
        print(set_abstract(argv[1], " ".join(argv[2:])))
        return
    tokens = [a for a in argv if a != "show"]
    for token in tokens:
        aid = native_id(token)
        if not aid:
            print(f"[{token}] 不是 arXiv 来源，无法取元数据；非 arXiv 请手工登记。")
            continue
        info = arxiv_meta(aid)
        if not info:
            print(f"[{token}] 取不到元数据（网络或编号问题），未写入任何猜测。")
            continue
        state = "有" if info.get("abstract") else "无（需人工／模型判读）"
        print(f"[{token}] versioned_id={info.get('versioned_id')} "
              f"revised={info.get('revised')} abstract={state} title={info.get('title')}")


if __name__ == "__main__":
    main()
