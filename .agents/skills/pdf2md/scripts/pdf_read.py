# /// script
# requires-python = ">=3.10"
# dependencies = ["pymupdf==1.28.2"]
# ///
"""Read PDF evidence for an agent: page text, phrase locations, and page images."""

import argparse
import json
from pathlib import Path

import pymupdf


def page_text(page: pymupdf.Page) -> str:
    return page.get_textpage(flags=pymupdf.TEXTFLAGS_TEXT).extractText()


def page_numbers(spec, total):
    """One-based PDF page positions, including comma-separated ranges."""
    if not spec:
        return list(range(1, total + 1))
    pages = []
    for part in spec.split(","):
        bounds = [int(value) for value in part.split("-")]
        start, end = bounds[0], bounds[-1]
        if len(bounds) > 2 or not 1 <= start <= end <= total:
            raise ValueError(f"页码超出范围或倒序：{part}；PDF 共 {total} 页")
        pages.extend(range(start, end + 1))
    return list(dict.fromkeys(pages))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--pages", help="PDF 文件中的页序号，从 1 开始，如 2,4-6；省略则全文")
    parser.add_argument("--find", help="在文本层定位短语，忽略大小写和空白差异，输出命中页与片段")
    parser.add_argument("--render", type=Path, metavar="DIR", help="将所选页渲染为 PNG，供视觉核对")
    args = parser.parse_args(argv)
    if args.render and not args.pages:
        parser.error("渲染时请用 --pages 指定页码")
    if args.render and args.find is not None:
        parser.error("先 --find 定位，再 --pages 配合 --render 查看对应页")

    with pymupdf.open(args.pdf) as document:
        pages = page_numbers(args.pages, len(document))
        if args.render:
            args.render.mkdir(parents=True, exist_ok=True)
            for number in pages:
                image = args.render / f"{args.pdf.stem}-page-{number}.png"
                document[number - 1].get_pixmap(dpi=144).save(image)
                print(image.resolve())
        elif args.find is not None:
            query = " ".join(args.find.casefold().split())
            if not query:
                parser.error("--find 需要非空短语")
            hits = []
            for number in pages:
                text = " ".join(page_text(document[number - 1]).split())
                at = text.casefold().find(query)
                if at >= 0:
                    hits.append({"page": number, "excerpt": text[max(0, at - 120):at + len(query) + 240]})
            print(json.dumps(hits, ensure_ascii=False, indent=2))
        else:
            for number in pages:
                print(f"\n--- PDF page {number} ---\n")
                print(page_text(document[number - 1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
