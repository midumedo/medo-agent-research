#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""measure_read_cost.py — 同一份文档的 PDF 版本与 HTML 版本，各读取管线的确定性成本测量。

只测可确定量：文件字节、字符、结构元素计数、按透明假设的 token 估算。
不调用任何模型，不测「理解质量」——模型在环的行为比较见 README「待执行」一节。

依赖策略与本项目一致（pyproject 声明零第三方运行时依赖）：
  HTML 侧只用标准库 html.parser；PDF 侧的标准库无法完成（需解压内容流并处理
  字体 ToUnicode 映射），因此 PyMuPDF 是**可选**依赖——缺失时脚本仍产出全部
  HTML 侧结果，PDF 侧标记为 unavailable 并以明确消息提示，不静默降级。

三条测量线：
  1. 体积      raw / 去样式 / 可见文本 / 结构化文本，各自 chars·bytes·est_tokens
  2. 结构      标题、表格、代码块在读取后是否可恢复（HTML 用标签计数，PDF 用字体/字号信号）
  3. 噪声      朴素读取引入的非内容开销（HTML 标签与 CSS；PDF 页眉页脚与断行碎片）

用法（从仓库根运行）：
    python domain/repo-context/05read-pdf-vs-html/measure_read_cost.py \
        --out domain/repo-context/05read-pdf-vs-html/results/2026-09-26
"""
from __future__ import annotations

import argparse
import collections
import datetime as _dt
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
from html.parser import HTMLParser

try:  # PDF 侧唯一可选项；不需要它也能跑完 HTML 侧全部测量
    import pymupdf as _fitz
except Exception:  # pragma: no cover
    try:
        import fitz as _fitz
    except Exception:
        _fitz = None

HEAD_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
BLOCK_TAGS = {
    "p", "div", "section", "article", "blockquote", "table", "ul", "ol",
    "br", "hr", "body", "html", "dl", "dt", "dd", "figure", "figcaption",
}
SKIP_TAGS = {"script", "style", "head", "title", "meta", "link", "noscript"}
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
    # SVG 自闭合元素，避免污染标签栈
    "path", "rect", "circle", "line", "ellipse", "polygon", "polyline", "stop", "use",
}


# ────────────────────────────────────────────────────────────── token 估算
def est_tokens(text: str) -> dict:
    """按字符构成估算 token 区间——透明假设，不是实测分词。

    CJK 取 1.0–1.5 tok/字，ASCII 取 0.25 tok/字，其余取 0.5–1.0。
    这是不同 BPE 词表的经验区间；结论只应依赖同一估算器下的相对比较。
    """
    cjk = ascii_ = other = 0
    for ch in text:
        o = ord(ch)
        if "\u4e00" <= ch <= "\u9fff" or "\u3000" <= ch <= "\u303f" or "\uff00" <= ch <= "\uffef":
            cjk += 1
        elif o < 128:
            ascii_ += 1
        else:
            other += 1
    low = cjk * 1.0 + ascii_ / 4.0 + other * 0.5
    high = cjk * 1.5 + ascii_ / 4.0 + other * 1.0
    return {
        "cjk": cjk, "ascii": ascii_, "other": other,
        "tokens_low": round(low), "tokens_high": round(high),
    }


def measure(text: str, **extra) -> dict:
    d = {"chars": len(text), "bytes_utf8": len(text.encode("utf-8"))}
    d.update(est_tokens(text))
    d.update(extra)
    return d


# ────────────────────────────────────────────────────────────── 标准库 DOM
class Node:
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag=None, attrs=None, parent=None):
        self.tag = tag
        self.attrs = attrs or {}
        self.children = []           # 元素为 Node，文本为 str
        self.parent = parent

    def text_content(self) -> str:
        out = []
        for c in self.children:
            out.append(c if isinstance(c, str) else c.text_content())
        return "".join(out)


class TreeBuilder(HTMLParser):
    """只建够用的树：标签计数、可见文本、结构化渲染。程序生成的 HTML 上足够稳。"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#document")
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        n = Node(tag, dict(attrs), self.stack[-1])
        self.stack[-1].children.append(n)
        if tag not in VOID_TAGS:
            self.stack.append(n)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(Node(tag, dict(attrs), self.stack[-1]))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def build_tree(html: str) -> Node:
    tb = TreeBuilder()
    tb.feed(html)
    tb.close()
    return tb.root


def iter_nodes(root: Node):
    for c in root.children:
        if isinstance(c, Node):
            yield c
            yield from iter_nodes(c)


def visible_text(root: Node) -> str:
    parts = []

    def rec(n):
        if isinstance(n, str):
            parts.append(n)
            return
        if n.tag in SKIP_TAGS:
            return
        for c in n.children:
            rec(c)

    rec(root)
    return "".join(parts)


def html_markdown(root: Node) -> str:
    """DOM → 结构化文本。保留全部可见文本，块级元素成行，表格成行，代码加标记。

    转换后由 coverage 断言检查是否漏文本——不允许用丢内容的转换充当「更省」。
    """
    out: list[str] = []

    def rec_children(n: Node):
        for c in n.children:
            if isinstance(c, str):
                out.append(c)
            else:
                rec(c)

    def rec(n: Node):
        tag = n.tag
        if tag in SKIP_TAGS:
            return
        if tag in HEAD_TAGS:
            out.append("\n" + "#" * int(tag[1]) + " ")
            rec_children(n)
            out.append("\n")
            return
        if tag == "pre":
            out.append("\n```\n")
            rec_children(n)
            out.append("\n```\n")
            return
        if tag == "code":
            out.append("`")
            rec_children(n)
            out.append("`")
            return
        if tag == "li":
            out.append("\n- ")
            rec_children(n)
            out.append("\n")
            return
        if tag == "tr":
            cells = [
                (c.text_content() or "").strip().replace("\n", " ")
                for c in n.children
                if isinstance(c, Node) and c.tag in ("td", "th")
            ]
            if any(cells):
                out.append("\n| " + " | ".join(cells) + " |")
            return
        if tag in BLOCK_TAGS:
            out.append("\n")
            rec_children(n)
            out.append("\n")
            return
        rec_children(n)

    for c in root.children:
        if isinstance(c, str):
            out.append(c)
        else:
            rec(c)
    s = "".join(out)
    s = re.sub(r"[ \t\u00a0]+", " ", s)
    s = re.sub(r"\n\s*\n\s*\n+", "\n\n", s)
    return s.strip()


def core_counter(s: str) -> collections.Counter:
    return collections.Counter(ch for ch in s if not ch.isspace())


def serialize(root: Node, skip: set) -> str:
    """从树上重新序列化标记文本，用于度量「剥离样式后的 HTML」还剩多少字符。"""
    from html import escape

    buf: list[str] = []

    def rec(n: Node):
        if n.tag in skip:
            return
        buf.append("<" + n.tag)
        for k, v in n.attrs.items():
            buf.append(f' {k}="{escape(v, quote=True)}"' if v is not None else f" {k}")
        buf.append(">")
        for c in n.children:
            if isinstance(c, str):
                buf.append(escape(c, quote=False))
            else:
                rec(c)
        if n.tag not in VOID_TAGS:
            buf.append(f"</{n.tag}>")

    for c in root.children:
        if isinstance(c, str):
            buf.append(escape(c, quote=False))
        else:
            rec(c)
    return "".join(buf)


# ────────────────────────────────────────────────────────────── HTML 读取管线
def load_html(path: str) -> dict:
    raw = open(path, encoding="utf-8").read()
    root = build_tree(raw)

    visible = re.sub(r"\s+", " ", visible_text(root)).strip()
    md = html_markdown(root)

    # 覆盖率自检：结构化文本必须承载可见文本的绝大部分字符
    ct, cm = core_counter(visible), core_counter(md)
    missing = sum(max(0, ct[c] - cm[c]) for c in ct)
    coverage = 1.0 - missing / max(1, sum(ct.values()))
    assert coverage >= 0.98, f"markdown 转换漏掉 {1-coverage:.1%} 的可见文本"

    tags = collections.Counter(n.tag for n in iter_nodes(root))
    struct = {
        "headings": sum(tags[t] for t in HEAD_TAGS),
        "tables": tags["table"], "rows": tags["tr"],
        "cells": tags["td"] + tags["th"],
        "code_elements": tags["code"], "pre_elements": tags["pre"],
        "list_items": tags["li"], "links": tags["a"], "images": tags["img"],
        "total_tags": sum(tags.values()),
    }
    code_chars = sum(
        len(n.text_content()) for n in iter_nodes(root) if n.tag in ("code", "pre")
    )
    # 去样式后的 HTML：从树上重新序列化，移除 head/style/script 子树
    stripped = serialize(root, skip={"head", "style", "script"})

    return {
        "path": path,
        "raw": measure(raw),
        "no_style_script": measure(stripped, note="标准库重新序列化，与原件字节不等"),
        "visible_text": measure(visible),
        "markdown": measure(md, coverage_ok=round(coverage, 4)),
        "structure": struct,
        "code_text_chars": code_chars,
        "style_script_chars": len(raw) - len(stripped),
        "markup_overhead_chars": len(raw) - len(visible),
        "markup_overhead_ratio": round((len(raw) - len(visible)) / len(raw), 4),
    }


# ────────────────────────────────────────────────────────────── PDF 读取管线
def load_pdf(path: str) -> dict:
    if _fitz is None:
        return {
            "path": path, "available": False,
            "file": {"bytes": os.path.getsize(path)},
            "reason": "未安装 PyMuPDF：PDF 侧需解压内容流并处理字体映射，标准库无法完成。"
                      " 安装后用同一命令复跑：python -m pip install pymupdf",
        }

    doc = _fitz.open(path)
    pages = [p.get_text() for p in doc]
    full = "".join(pages)

    # 页眉页脚噪声：Chrome 打印会写入源文件路径与「页码/总页数」
    noise_lines = noise_chars = url_lines = 0
    for t in pages:
        for line in t.split("\n"):
            ls = line.strip()
            if not ls:
                continue
            if re.fullmatch(r"\d+\s*/\s*\d+", ls) or ls.startswith("file://"):
                noise_lines += 1
                noise_chars += len(ls)
                if ls.startswith("file://"):
                    url_lines += 1

    # 字体/字号信号：判断结构能否从 PDF 原生信息恢复
    fonts: collections.Counter = collections.Counter()
    sizes: collections.Counter = collections.Counter()
    spans = span_chars = bold_spans = mono_spans = mono_chars = 0
    ink_area = page_area = 0.0
    for p in doc:
        page_area += abs(p.rect.width * p.rect.height)
        for b in p.get_text("dict")["blocks"]:
            for line in b.get("lines", []):
                for s in line.get("spans", []):
                    t = s["text"]
                    spans += 1
                    span_chars += len(t)
                    f = s["font"]
                    fonts[f] += len(t)
                    sizes[round(s["size"], 1)] += len(t)
                    x0, y0, x1, y1 = s["bbox"]
                    ink_area += max(0.0, x1 - x0) * max(0.0, y1 - y0)
                    if s["flags"] & 2 ** 4:
                        bold_spans += 1
                    if "mono" in f.lower() or "consol" in f.lower() or "courier" in f.lower():
                        mono_spans += 1
                        mono_chars += len(t)

    # 断行碎片：表格单元格与版式断行会把内容切成极短行
    lines = [l for l in full.split("\n") if l.strip()]
    frag = sum(1 for l in lines if len(l.strip()) <= 3)

    # 视觉路径：PDF 逐页渲染为位图后按像素计费。
    # tokens ≈ w*h/750 取自 Anthropic 图像文档的公开口径——本轮未能联网核实，可能随版本变化。
    r = doc[0].rect
    main_size = sizes.most_common(1)[0][0] if sizes else 0.0
    visual = {
        "formula": "tokens_per_page ≈ round(w*h/750)；只算像素项，未含可能叠加的文本层",
        "main_font_pt": main_size,
        "zooms": {},
    }
    for zoom in (1.0, 2.0, 3.0):
        w, h = round(r.width * zoom), round(r.height * zoom)
        per_page = round(w * h / 750)
        visual["zooms"][f"{zoom:g}x"] = {
            "page_px": [w, h], "tokens_per_page": per_page,
            "tokens_total": per_page * doc.page_count,
            "main_glyph_px": round(main_size * zoom, 1),
        }

    # 图像路径还要付传输/存储体积（与 token 计费口径不同，仅作量级比较）
    idxs = sorted({0, doc.page_count // 2, doc.page_count - 1})
    png_sizes = [
        len(doc[i].get_pixmap(matrix=_fitz.Matrix(2, 2)).tobytes("png")) for i in idxs
    ]
    render = {
        "sampled_pages": [i + 1 for i in idxs],
        "mean_png_bytes_at_2x": round(sum(png_sizes) / len(png_sizes)),
        "estimated_total_png_bytes_at_2x": round(
            sum(png_sizes) / len(png_sizes) * doc.page_count),
        "text_extract_bytes": len(full.encode("utf-8")),
    }

    return {
        "path": path, "available": True,
        "pages": doc.page_count,
        "producer": doc.metadata.get("producer"),
        "file": {"bytes": os.path.getsize(path)},
        "text_extract": measure(full, lines=len(lines), short_lines_le3=frag,
                                short_line_ratio=round(frag / max(1, len(lines)), 4)),
        "noise": {"header_footer_lines": noise_lines, "noise_chars": noise_chars,
                  "source_url_lines": url_lines},
        "ink": {
            "span_bbox_area_sum": round(ink_area), "page_area_sum": round(page_area),
            "coverage": round(ink_area / page_area, 4) if page_area else None,
            "note": "文字 bbox 面积和 ÷ 页面面积和；重叠会略高估，作为视觉路径「按页付费」的无效面积下界",
        },
        "signals": {
            "spans": spans, "span_chars": span_chars,
            "distinct_fonts": len(fonts),
            "type3_fonts": sum(1 for f in fonts if f.lower().startswith("type3")),
            "bold_spans": bold_spans, "mono_spans": mono_spans, "mono_chars": mono_chars,
            "top_sizes": sizes.most_common(6),
        },
        "visual_estimate": visual,
        "render": render,
        "note": "tokens ≈ w*h/750 为像素计费粗估，随供应商与分辨率变化；仅用于量级比较",
    }


# ────────────────────────────────────────────────────────────── 组装
def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_head() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return "(not a git repo)"


def locate(root: str) -> tuple[str, str]:
    pdfs = glob.glob(os.path.join(root, "sources/books/*/*.pdf"))
    htmls = glob.glob(os.path.join(root, "sources/books/*/*.html"))
    if len(pdfs) != 1 or len(htmls) != 1:
        sys.exit(f"期望恰好一对同名 PDF/HTML，实际 PDF={pdfs} HTML={htmls}")
    return pdfs[0], htmls[0]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="仓库根（默认当前目录）")
    ap.add_argument("--out", default=None, help="输出 JSON 前缀（不含扩展名）；省略则只打印")
    args = ap.parse_args()

    pdf_path, html_path = locate(args.root)
    h = load_html(html_path)
    p = load_pdf(pdf_path)
    if not p.get("available", True):
        print("⚠ " + p["reason"], file=sys.stderr)

    # 内容等价性自检：两种格式承载的 CJK 字符量应同量级，否则不是同一文档
    if p.get("available", True):
        hc, pc = h["visible_text"]["cjk"], p["text_extract"]["cjk"]
        assert 0.85 <= hc / max(1, pc) <= 1.15, \
            f"CJK 字符量差异过大（html={hc} pdf={pc}），非同源文档？"

    result = {
        "generated": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "git_head": git_head(),
        "python": sys.version.split()[0],
        "parser": {"html": "stdlib html.parser", "pdf": "pymupdf" if _fitz else None},
        "inputs": {
            "sha256": {"pdf": sha256(pdf_path), "html": sha256(html_path)},
            "pdf": {"path": pdf_path, "bytes": os.path.getsize(pdf_path)},
            "html": {"path": html_path, "bytes": os.path.getsize(html_path)},
        },
        "html": h,
        "pdf": p,
        "assumptions": [
            "token 为按字符构成的估算区间，非实测分词；只做同一估算器下的相对比较",
            "HTML 由标准库 html.parser 建树，「结构化文本」已用 98% 覆盖率断言保证不丢可见文本",
            "PDF「文本抽取」用 PyMuPDF get_text，等价于 harness 最常见的 pdf→text 路径",
            "PDF「视觉」按每页位图像素计费粗估，未含文本层叠加与多次采样",
        ],
    }

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        json.dump(result, open(args.out + ".json", "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)

    # 摘要表：同一估算器下的横向比较
    rows = [
        ("html.raw", h["raw"]), ("html.no_style_script", h["no_style_script"]),
        ("html.visible_text", h["visible_text"]), ("html.markdown", h["markdown"]),
    ]
    if p.get("available", True):
        rows.append(("pdf.text_extract", p["text_extract"]))
    print(f"{'pipeline':24}{'chars':>9}{'bytes':>10}{'tok_low':>9}{'tok_high':>9}")
    for name, m in rows:
        print(f"{name:24}{m['chars']:>9}{m['bytes_utf8']:>10}{m['tokens_low']:>9}{m['tokens_high']:>9}")
    for z, v in p.get("visual_estimate", {}).get("zooms", {}).items():
        print(f"{'pdf.visual ' + z:24}{'-':>9}{'-':>10}{v['tokens_total']:>9}"
              f"{('  glyph≈%.1fpx' % v['main_glyph_px']):>16}")
    if p.get("available", True):
        print(f"\nPDF pages={p['pages']}  header/footer noise lines={p['noise']['header_footer_lines']} "
              f"chars={p['noise']['noise_chars']}  short(<=3) lines={p['text_extract']['short_lines_le3']}"
              f" ({p['text_extract']['short_line_ratio']:.1%})")
        print(f"PDF ink coverage={p['ink']['coverage']:.1%} (文字 bbox 面积 ÷ 页面面积)"
              f"  main font={p['visual_estimate']['main_font_pt']}pt")
        print(f"PDF render@2x mean PNG={p['render']['mean_png_bytes_at_2x']:,} B/page"
              f" → est total={p['render']['estimated_total_png_bytes_at_2x']:,} B"
              f"  vs text_extract={p['render']['text_extract_bytes']:,} B")
    print(f"HTML structure={h['structure']}  markup overhead={h['markup_overhead_ratio']:.1%}")
    print(f"HTML markdown coverage check = {h['markdown']['coverage_ok']}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
