"""步骤② 原件：按 id 把 arXiv PDF 取回 `pdf/<文件名>.pdf`。

只管「原件在不在、下没下来」。元数据由 ① `meta.py` 提供。已存在的 PDF 一律保留，
不因为元数据更新而覆盖——版本写在文件名里（`<id>` 含 `vN`），换版本就换文件名。

Usage:
    pdf.py [文件名 | id | arXiv 编号 | 标题 ...]
    pdf.py --all        # 按 index.csv 的 id 列逐篇核对／下载
"""

import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import meta  # noqa: E402
import stem  # noqa: E402
from stem import find, native_for, pdf_path, slugify, stem_of  # noqa: E402


def fetch_pdf(versioned_id):
    """The PDF bytes for an explicitly versioned arXiv id."""
    if not re.fullmatch(r"\d{4}\.\d{4,5}v[1-9]\d*", versioned_id):
        raise ValueError("PDF download requires an explicit arXiv version")
    _, data = meta.get(f"https://arxiv.org/pdf/{versioned_id}")
    if len(data) < 20000 or not data.startswith(b"%PDF"):
        raise ValueError("response is not a plausible PDF")
    return data


def download_one(token):
    """Fetch one PDF by id. A cached PDF is never refetched or replaced."""
    record = find(token)
    aid = native_for(token, record)
    stem_name = stem_of(record) if record else None
    if stem_name and os.path.exists(pdf_path(stem_name)):
        # Do not fetch latest metadata for a legacy/cached PDF.
        return f"[{stem_name}] cached PDF preserved; version lives in its filename"
    if not aid or not re.fullmatch(r"\d{4}\.\d{4,5}(?:v[1-9]\d*)?", aid):
        return f"[{token}] 只有 arXiv 来源能自动下载：给出 arXiv 编号或已入库的标识／标题；非 arXiv 请手工放入 pdf/ 再跑 convert.py"

    candidate = meta.fetch_meta(aid)
    if not candidate.get("exists"):
        return f"[{token}] metadata unavailable; existing records preserved"
    versioned_id = candidate.get("versioned_id")
    published_at = revised = None
    if not versioned_id:
        # Fall back to the API; the abs page alone no longer guarantees a versioned identity.
        versioned_id, published_at, revised = meta.resolve_meta(aid)
    if not versioned_id:
        return f"[{token}] version unresolved; unchanged. Retry with an explicit version after checking the intended version."
    if aid != versioned_id:
        candidate = meta.fetch_meta(versioned_id)
        if not candidate.get("exists"):
            return f"[{token}] versioned metadata unavailable; existing records preserved"
    try:
        data = fetch_pdf(versioned_id)
    except Exception as error:
        return f"[{token}] PDF unavailable ({error}); existing records preserved"

    stem_name = stem_name or slugify(candidate.get("title") or "")
    if not stem_name:
        return f"[{token}] 元数据没有标题，无法定文件名；未写入"
    dest = pdf_path(stem_name)
    if os.path.exists(dest) and not record:
        return f"[{stem_name}] 同名文件已存在，未覆盖；先确认是不是同一篇"
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    temporary = dest + ".tmp"
    with open(temporary, "wb") as f:
        f.write(data)
    os.replace(temporary, dest)
    candidate["id"] = stem_name
    candidate["native_id"] = aid
    candidate["registry"] = "arxiv"
    candidate["versioned_id"] = versioned_id
    if published_at:
        candidate["published_at"] = published_at
    if revised:
        candidate["revised"] = revised[:10]
    # 元数据不再另存一份：登记块由 ③ convert.py 写入 md，缺的信息随取随用。
    return f"[{stem_name}] saved {versioned_id} ({len(data) // 1024} KB)"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--all" in sys.argv[1:] or not args:
        # 不读单独的清单：index.csv 的 id 列是范围。
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
