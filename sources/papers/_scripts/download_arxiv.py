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


from stem import load_meta, load_provenance, native_id, pdf_path, registry, save_meta, \
    save_provenance, to_stem

WATCHLIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "watchlist.txt")
UA = "MemoryResearch/1.0 (local paper archive)"


def resolve_version(aid):
    """Resolve the current arXiv version through the official API.

    arXiv changed the abs page so that citation_pdf_url may omit the version
    suffix. The API still reports the identity with version, so it remains an
    explicit-version source rather than a guess.
    """
    base = re.sub(r"v\d+$", "", aid)
    try:
        req = urllib.request.Request(ARXIV_API.format(base), headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as response:
            root = ET.fromstring(response.read())
    except Exception:
        return None
    for entry in root.findall(ATOM + "entry"):
        raw = entry.findtext(ATOM + "id", "").rsplit("/", 1)[-1]
        if re.fullmatch(r"\d{4}\.\d{4,5}v\d+", raw):
            return raw
    return None


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


def download_one(token, meta, provenance):
    try:
        stem = to_stem(token)
    except ValueError as error:
        return f"[{token}] {error}"
    aid = native_id(stem)
    if registry(stem) != "arxiv" or not re.fullmatch(r"\d{4}\.\d{4,5}(?:v[1-9]\d*)?", aid):
        return f"[{stem}] 本脚本只处理 arXiv 来源；非 arXiv 来源请手工放入 pdf/ 并按 AGENTS.md 定词干"
    dest = pdf_path(stem)
    if os.path.exists(dest):
        # Do not fetch latest metadata for a legacy/cached PDF.
        return f"[{stem}] cached PDF and metadata preserved; version: {provenance.get(stem, {}).get('version') or 'unknown'}"

    candidate = fetch_meta(aid)
    if not candidate.get("exists"):
        return f"[{stem}] metadata unavailable; existing records preserved"
    versioned_id = candidate.get("versioned_id")
    if not versioned_id:
        # Fall back to the API; the abs page alone no longer guarantees a versioned identity.
        versioned_id = resolve_version(aid)
    if not versioned_id:
        return f"[{stem}] version unresolved; unchanged. Retry with an explicit version after checking the intended version."
    if aid != versioned_id:
        candidate = fetch_meta(versioned_id)
        if not candidate.get("exists"):
            return f"[{stem}] versioned metadata unavailable; existing records preserved"
    try:
        data = fetch_pdf(versioned_id)
    except Exception as error:
        return f"[{stem}] PDF unavailable ({error}); existing records preserved"

    os.makedirs(os.path.dirname(dest), exist_ok=True)
    temporary = dest + ".tmp"
    with open(temporary, "wb") as f:
        f.write(data)
    os.replace(temporary, dest)
    candidate["id"] = stem
    candidate["native_id"] = aid
    candidate["registry"] = "arxiv"
    candidate["versioned_id"] = versioned_id
    meta[stem] = candidate
    provenance[stem] = {
        "source_url": f"https://arxiv.org/abs/{versioned_id}",
        "pdf_url": f"https://arxiv.org/pdf/{versioned_id}",
        "version": versioned_id,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "pdf_path": f"pdf/{stem}.pdf",
        "pdf_sha256": hashlib.sha256(data).hexdigest(),
        "metadata_pdf_pairing": "same explicit arXiv version requested for both downloads",
    }
    # Save after each successful pair. Failed attempts never replace valid data.
    save_provenance(provenance)
    save_meta(meta)
    return f"[{stem}] saved {versioned_id} ({len(data) // 1024} KB)"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--all" in sys.argv[1:] or not args:
        if os.path.exists(WATCHLIST):
            with open(WATCHLIST, encoding="utf-8") as f:
                args = [line.strip() for line in f if line.strip() and not line.lstrip().startswith("#")]
    if not args:
        print("no ids given")
        return
    meta, provenance = load_meta(), load_provenance()
    for aid in args:
        print(download_one(aid, meta, provenance))
        if len(args) > 1:
            time.sleep(1.5)


if __name__ == "__main__":
    main()
