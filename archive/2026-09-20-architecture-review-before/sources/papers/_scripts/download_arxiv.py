"""从 arXiv 下载论文 PDF 到 refs/pdf/，并抓取 abs 页的标题/作者/日期写入 refs/meta.json。

用法:
    python download_arxiv.py 2512.13564 2602.06052 ...
    python download_arxiv.py --all        # 下载 refs/watchlist.txt 里的全部编号
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # papers/
PDF_DIR = os.path.join(BASE, "pdf")
META_PATH = os.path.join(BASE, "meta.json")
WATCHLIST = os.path.join(BASE, "watchlist.txt")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()


def fetch_meta(aid):
    """抓 abs 页，解析 citation_title / citation_author / citation_date。"""
    try:
        _, html = get(f"https://arxiv.org/abs/{aid}")
    except Exception as e:
        return {"id": aid, "error": f"abs fetch failed: {e}"}
    txt = html.decode("utf-8", "ignore")

    def grab(name):
        m = re.search(rf'<meta name="{name}" content="(.*?)"', txt, re.S)
        return m.group(1).strip() if m else None

    title = grab("citation_title")
    date = grab("citation_date")
    authors = re.findall(r'<meta name="citation_author" content="(.*?)"', txt, re.S)
    abstract = None
    m = re.search(r'<blockquote class="abstract[^"]*">(.*?)</blockquote>', txt, re.S)
    if m:
        abstract = re.sub(r"<.*?>", " ", m.group(1))
        abstract = re.sub(r"\s+", " ", abstract).replace("Abstract:", "").strip()
    # 判断是否真的存在这篇论文
    not_found = ("not found" in txt.lower() and title is None) or title is None
    return {
        "id": aid,
        "title": title,
        "authors": [a.strip() for a in authors],
        "date": date,
        "abstract": abstract,
        "exists": not not_found,
        "url": f"https://arxiv.org/abs/{aid}",
    }


def fetch_pdf(aid):
    os.makedirs(PDF_DIR, exist_ok=True)
    dest = os.path.join(PDF_DIR, f"{aid}.pdf")
    if os.path.exists(dest) and os.path.getsize(dest) > 20000:
        return dest, "cached"
    for url in (f"https://arxiv.org/pdf/{aid}", f"https://arxiv.org/pdf/{aid}v1"):
        try:
            _, data = get(url)
        except Exception:
            continue
        if len(data) < 20000 or not data[:5].startswith(b"%PDF"):
            continue
        with open(dest, "wb") as f:
            f.write(data)
        return dest, f"ok ({len(data)//1024} KB)"
    return None, "failed"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--all" in sys.argv[1:] or not args:
        if os.path.exists(WATCHLIST):
            with open(WATCHLIST, encoding="utf-8") as f:
                args = [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]
    if not args:
        print("no ids given")
        return

    meta = {}
    if os.path.exists(META_PATH):
        with open(META_PATH, encoding="utf-8") as f:
            meta = json.load(f)

    for aid in args:
        m = fetch_meta(aid)
        meta[aid] = m
        status = "NOT FOUND" if not m.get("exists") else m.get("title", "")[:70]
        print(f"[{aid}] meta: {status}")
        time.sleep(1.5)
        path, st = fetch_pdf(aid)
        print(f"[{aid}] pdf : {st} -> {path}")
        time.sleep(1.5)

    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"\nmeta written -> {META_PATH}")


if __name__ == "__main__":
    main()
