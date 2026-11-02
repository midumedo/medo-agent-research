"""Quality audit and read-only repair planning for MinerU Markdown.

`audit` stays on the standard library. `build_plan` needs a PDF text layer for
anchoring and imports PyMuPDF lazily, so a missing engine fails loudly instead
of silently degrading.
"""

from __future__ import annotations

import difflib
import hashlib
import io
import re
from bisect import bisect_left, bisect_right
from pathlib import Path

# A tag pair, non-greedy, may span a line break inside the content.
TAG_RE = re.compile(r"<(?P<kind>sub|sup)>(?P<content>.*?)</(?P=kind)>", re.I | re.S)
TABLE_RE = re.compile(r"<table\b.*?</table>", re.I | re.S)
FRONT_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", re.S)
# The token immediately left of a tag, so "Zexue He <sup>1</sup>" has no base.
BASE_RE = re.compile(r"([A-Za-z0-9][A-Za-z0-9._-]*)\Z")
PARAGRAPH_RE = re.compile(r"[^\n]+(?:\n(?!\n)[^\n]+)*")

# Protected regions. Order matters: block structures first, then line-local.
ALGO_RE = re.compile(r'<div class="mineru-algorithm"[^>]*>.*?</div>', re.I | re.S)
FENCE_RE = re.compile(r"^[ \t]*```[^\n]*\n.*?^[ \t]*```[ \t]*$", re.M | re.S)
DOLLAR_BLOCK_RE = re.compile(r"\$\$.*?\$\$", re.S)
INLINE_DOLLAR_RE = re.compile(r"(?<![\\$])\$[^$\n]+?\$")
IMAGE_LINE_RE = re.compile(r"^[ \t]*(?:!\[[^\]]*\]\([^)]*\)|<img\b[^>]*>)[ \t]*$", re.M | re.I)

RAW_WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’\-]*")
PUNCTUATION = " \t\r\n.,;:!?()[]{}\"'“”‘’"
WHOLE_WORD_RE = re.compile(r"[A-Za-z]{2,}")

# Block-level trigger. Every clean paper in the corpus sits at or below 0.84
# tags per 1000 chars overall, so 2.0 is a 2.4x margin. The tag floor keeps a
# one-tag heading out; the noise floor keeps a long, otherwise clean paragraph
# from being flagged by a handful of stray tags.
BLOCK_PER_KCHARS = 2.0
BLOCK_TOKEN_FLOOR = 5
BLOCK_TAG_FLOOR = 3

DEFAULT_WHITELIST = ()


def split_body(text: str) -> str:
    """Return the body after the YAML front matter (register, not prose)."""
    match = FRONT_RE.match(text)
    return text[match.end():] if match else text


def _blank(text: str) -> str:
    """Same length, same line breaks, but every tag inside a table disappears."""
    return "".join("\n" if char == "\n" else " " for char in text)


def mask_tables(body: str) -> tuple[str, int]:
    """Return (body without table content, table character count)."""
    removed = 0
    parts = []
    cursor = 0
    for match in TABLE_RE.finditer(body):
        parts.append(body[cursor:match.start()])
        chunk = match.group(0)
        removed += len(chunk)
        parts.append(_blank(chunk))
        cursor = match.end()
    parts.append(body[cursor:])
    return "".join(parts), removed


def _line_starts(text: str) -> list[int]:
    return [0] + [index + 1 for index, char in enumerate(text) if char == "\n"]


def _line_at(starts: list[int], offset: int) -> int:
    return bisect_right(starts, offset) - 1


def _true_super(content: str, before: str, after: str, whitelist=()) -> bool:
    """A real superscript at a word end: one letter/digit on a name or entity.

    Conservative by design, and it has to be, because audit has no PDF to
    confirm against. It rejects marks separated by whitespace (author-unit
    marks such as ``Zexue He <sup>1</sup>``), marks followed by a letter
    (``LLM-<sup>b</sup>ase``), and numeric bases (``3.<sup>6</sup>7``).
    What survives is an alphanumeric identifier such as ``Mem0<sup>g</sup>``
    or ``Neo4j<sup>1</sup>``, an all-capital acronym at a word end, or an
    explicit whitelist entry. Callers should confirm via ``true_sups``.
    """
    value = content.strip()
    if not value or len(value) > 3:
        return False
    if not (value.isdigit() or (len(value) == 1 and value.isalpha())):
        return False
    base = BASE_RE.search(before)
    if not base:
        return False
    token = base.group(1)
    if any(token == mark or token.endswith(mark) for mark in whitelist):
        return True
    if len(token) >= 2 and token[0].isalpha() and any(char.isdigit() for char in token):
        # Alphanumeric identifiers (Mem0, Neo4j, GPT4) keep their superscript
        # even when a broken word follows immediately: Mem0<sup>g</sup>rema.
        return True
    if after and after.isalnum():
        return False
    return len(token) >= 2 and token.isupper()


def audit_body(body: str, *, whitelist=DEFAULT_WHITELIST) -> dict:
    """Describe tag noise in one MinerU body without touching disk."""
    masked, table_chars = mask_tables(body)
    chars = len(body) - table_chars
    starts = _line_starts(masked)
    lines = masked.split("\n")

    tags = {"sub": 0, "sup": 0}
    noise = 0
    internal = 0
    cross_word = 0
    true_sups = []
    for match in TAG_RE.finditer(masked):
        kind = match.group("kind").lower()
        tags[kind] += 1
        line = _line_at(starts, match.start())
        left = match.start() - starts[line]
        row = lines[line]
        end = left + len(match.group(0))
        left_ok = left > 0 and row[left - 1].isalnum()
        right_ok = end < len(row) and row[end].isalnum()
        if left_ok or right_ok:
            noise += 1
        if left_ok and right_ok:
            internal += 1
        if any(char.isspace() for char in match.group("content")):
            cross_word += 1
        after = row[end] if end < len(row) else ""
        if kind == "sup" and _true_super(match.group("content"), row[:left], after, whitelist):
            true_sups.append({"line": line + 1, "text": match.group(0).strip(),
                              "internal": left_ok and right_ok})
    total = tags["sub"] + tags["sup"]
    density = round(total * 1000 / chars, 2) if chars > 0 else 0.0
    internal_density = round(internal * 1000 / chars, 2) if chars > 0 else 0.0

    # Structural estimate for R1: a tag inside a word that merges back into one
    # all-letter word. True superscripts are subtracted; R6 shapes keep angle
    # brackets and never reach here, so this is an upper bound, not a promise.
    auto = internal - sum(1 for item in true_sups if item["internal"])

    blocks = 0
    worst = None
    for match in PARAGRAPH_RE.finditer(masked):
        block = match.group(0)
        block_tags = list(TAG_RE.finditer(block))
        if len(block_tags) < BLOCK_TAG_FLOOR:
            continue
        noisy = 0
        for item in block_tags:
            index = item.start() - (block.rfind("\n", 0, item.start()) + 1)
            if _adjacent_line(block, index, index + len(item.group(0))):
                noisy += 1
        per_kchars = noisy * 1000 / max(1, len(block))
        if noisy >= BLOCK_TOKEN_FLOOR or per_kchars >= BLOCK_PER_KCHARS:
            blocks += 1
            if worst is None or per_kchars > worst["per_kchars"]:
                worst = {"line": _line_at(starts, match.start()) + 1,
                         "per_kchars": round(per_kchars, 1), "noise_tags": noisy}

    return {
        "chars": chars,
        "table_chars": table_chars,
        "tags": {**tags, "total": total},
        "density": density,
        "noise_tags": noise,
        "word_internal_tags": internal,
        "word_internal_density": internal_density,
        "cross_word_tags": cross_word,
        "words_with_tags": sum(1 for token in masked.split()
                               if "<sub>" in token.lower() or "<sup>" in token.lower()),
        "true_sup_count": len(true_sups),
        "true_sups": [{"line": item["line"], "text": item["text"]} for item in true_sups],
        "auto_fixable": auto,
        "blocks_over_threshold": blocks,
        "worst_block": worst,
        "suggest_repair": blocks > 0 and internal_density >= BLOCK_PER_KCHARS,
        "threshold": {"block_per_kchars": BLOCK_PER_KCHARS,
                      "block_token_floor": BLOCK_TOKEN_FLOOR,
                      "block_tag_floor": BLOCK_TAG_FLOOR},
    }


def _adjacent_line(text: str, start: int, end: int) -> bool:
    left = text[start - 1] if start > 0 else ""
    right = text[end] if end < len(text) else ""
    return left.isalnum() or right.isalnum()


def audit_text(text: str, *, whitelist=DEFAULT_WHITELIST) -> dict:
    return audit_body(split_body(text), whitelist=whitelist)


def summarize(quality: dict) -> str:
    """One line meant for conversion logs; stable enough for a human to diff."""
    if not quality:
        return "体检：不可用"
    if quality.get("error"):
        return f"体检：失败（{quality['error']}）"
    verdict = "建议 repair" if quality["suggest_repair"] else "无需 repair"
    return (f"体检：表格外 sub+sup {quality['density']}/千字"
            f" · 跨词标签 {quality['cross_word_tags']}"
            f" · 真上标 {quality['true_sup_count']}"
            f" · 可自动修 {quality['auto_fixable']} 词"
            f" · {verdict}")


# --------------------------------------------------------------------------
# Stage one: plan only. Nothing below is allowed to write the document itself.


class RepairError(RuntimeError):
    """An unsafe plan request, a failed self-check, or an unusable output path."""


class DependencyError(RepairError):
    """PyMuPDF is required for anchoring; callers turn this into exit code 2."""


def _merge_spans(spans) -> list[tuple[int, int]]:
    merged = []
    for start, end in sorted(spans):
        if start >= end:
            continue
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
        else:
            merged.append((start, end))
    return merged


def _overlaps(start: int, end: int, spans) -> bool:
    return any(start < other_end and other_start < end for other_start, other_end in spans)


def masked_spans(text: str) -> list[tuple[int, int]]:
    """Explicit structural markers, as half-open character spans."""
    spans = []
    front = FRONT_RE.match(text)
    if front:
        spans.append((0, front.end()))
    spans.extend(match.span() for match in TABLE_RE.finditer(text))
    spans.extend(match.span() for match in ALGO_RE.finditer(text))
    spans.extend(match.span() for match in FENCE_RE.finditer(text))
    spans.extend(match.span() for match in DOLLAR_BLOCK_RE.finditer(text))
    spans.extend(match.span() for match in IMAGE_LINE_RE.finditer(text))
    spans = _merge_spans(spans)
    for match in INLINE_DOLLAR_RE.finditer(text):
        if not _overlaps(match.start(), match.end(), spans):
            spans.append(match.span())
    return _merge_spans(spans)


def _masked_text(text: str, spans) -> str:
    chars = list(text)
    for start, end in spans:
        for index in range(start, end):
            if chars[index] != "\n":
                chars[index] = " "
    return "".join(chars)


def _protected_bytes(text: str, spans) -> bytearray:
    flags = bytearray(len(text))
    for start, end in spans:
        flags[start:end] = b"\x01" * (end - start)
    return flags


def _tokens(line: str) -> list[tuple[int, int, str]]:
    """Whitespace tokens where a tag, including its content, stays one token."""
    tokens = []
    index, length = 0, len(line)
    while index < length:
        if line[index].isspace():
            index += 1
            continue
        start = index
        while index < length:
            tag = TAG_RE.match(line, index)
            if tag:
                index = tag.end()
                continue
            if line[index].isspace():
                break
            index += 1
        tokens.append((start, index, line[start:index]))
    return tokens


def _norm(text: str) -> str:
    return "".join(char for char in text.lower() if char.isalnum())


def _flat(text: str) -> str:
    """Words normalized the same way as `_norm`, joined by single spaces."""
    words = (_norm(match.group(0)) for match in RAW_WORD_RE.finditer(text.lower()))
    return " ".join(word for word in words if word)


def _words(text: str) -> list[str]:
    return [match.group(0).lower() for match in RAW_WORD_RE.finditer(text)]


def _load_pymupdf():
    try:
        import pymupdf
    except ImportError as error:
        raise DependencyError("缺少 PyMuPDF；请先安装：python -m pip install pymupdf") from error
    return pymupdf


SHINGLE_SIZES = (8, 7, 6, 5)
MATH_RE = re.compile(r"\$\$.*?\$\$|(?<![\\$])\$[^$\n]+?\$", re.S)


def _paragraph_words(text: str) -> list[str]:
    """Words for anchoring, with dollar-delimited math taken out.

    A line whose opening is ``$\\mathtt{MemO}^{g}$`` never matches the PDF
    text layer, which prints the glyphs separately; dropping the formula lets
    the prose after it do the anchoring.
    """
    return _words(MATH_RE.sub(" ", text))


def _pdf_index(path) -> dict:
    """Text layers only: words per line, 5–8 word line index, global vocabulary."""
    pymupdf = _load_pymupdf()
    document = pymupdf.open(str(path))
    try:
        lines = []
        for page_number, page in enumerate(document, 1):
            for text in page.get_text("text").splitlines():
                text = text.strip()
                words = _words(text)
                if text and words:
                    lines.append({"page": page_number, "text": text, "words": words})
    finally:
        document.close()
    shingles, vocabulary = {}, set()
    for index, line in enumerate(lines):
        for size in SHINGLE_SIZES:
            table = shingles.setdefault(size, {})
            for offset in range(len(line["words"]) - size + 1):
                table.setdefault(tuple(line["words"][offset:offset + size]), []).append(index)
        vocabulary.update(line["words"])
    return {"lines": lines, "shingles": shingles, "vocab": vocabulary}


def _anchor(plain_line: str, index: dict, previous: int) -> int | None:
    """PDF line holding the line's opening words, searched forward-only.

    MinerU paragraphs are long, so a line routinely starts before where the
    previous line ended; the 40-line lookback absorbs that overlap. There is no
    upper bound on purpose: the appendix sits hundreds of lines past the body
    text, and an earlier ceiling made every later line anchor to a short n-gram
    near the last hit, which silently starved their windows. Longest-first,
    earliest-offset-first: a sentence opening beats a rare fragment deeper in
    the line.
    """
    words = _paragraph_words(plain_line)
    floor = previous - 40
    best = None
    for size in SHINGLE_SIZES:
        table = index["shingles"][size]
        for offset in range(len(words) - size + 1):
            hits = table.get(tuple(words[offset:offset + size]))
            if not hits:
                continue
            cursor = bisect_left(hits, floor)
            if cursor == len(hits):
                continue
            key = (offset, -size)
            if best is None or key < best[0]:
                best = (key, hits[cursor])
    return None if best is None else best[1]


def _window(index: dict, anchor: int, word_count: int) -> dict:
    """Whole PDF stretch a long MinerU paragraph can occupy, tail included."""
    lines = index["lines"]
    start = max(0, anchor - 2)
    end = min(len(lines), anchor + 1)
    total = sum(len(line["words"]) for line in lines[start:end])
    while end < len(lines) and total < word_count + 20 and end - start < 200:
        total += len(lines[end]["words"])
        end += 1
    text = " ".join(line["text"] for line in lines[start:end])
    words = [match.group(0) for match in RAW_WORD_RE.finditer(text)]
    return {"page": lines[anchor]["page"], "text": text, "words": words,
            "norm": {_norm(word) for word in words}, "flat": _flat(text)}


def _found(window: dict | None, value: str) -> bool:
    """Verbatim hit: the merged fragment as it would read on the PDF page.

    A single word must match a PDF word, so ``afoundation`` cannot pass as
    "a foundation" before R5 gets a look at it. A fragment carrying spaces or
    punctuation is matched on word boundaries, so "tracks causall" cannot pass
    by being a prefix of "tracks causally".
    """
    if not window:
        return False
    target = _flat(value)
    if not target:
        return False
    if " " not in target:
        return target in window["norm"]
    return f" {target} " in f" {window['flat']} "


def _merge_tags(text: str) -> str:
    """Drop only the markup; the tag content is the duplicated fragment."""
    return TAG_RE.sub(lambda match: match.group("content"), text)


def _apply_merge(token: str, token_start: int, tags) -> str:
    """Merge selected tags inside one whitespace token, keeping the rest."""
    parts, cursor = [], 0
    for _, start, end, content in sorted(tags, key=lambda item: item[1]):
        left, right = start - token_start, end - token_start
        parts.append(token[cursor:left])
        parts.append(content)
        cursor = right
    parts.append(token[cursor:])
    return "".join(parts)


def _candidate(core: str, window: dict | None, threshold: float) -> str | None:
    """A PDF word or word pair that explains a damaged token, or None."""
    if not window:
        return None
    target = _norm(core)
    words = window["words"]
    for first, second in zip(words, words[1:]):
        if _norm(first) + _norm(second) != target:
            continue
        if not (_norm(first).isalpha() and _norm(second).isalpha()):
            continue
        # A hyphen or apostrophe at the end of the first word is the PDF's own
        # join, so the pair reads back as it was printed.
        if first.endswith(("-", "'", "’")):
            return first + second
        return f"{first} {second}"
    scored = []
    for word in words:
        normal = _norm(word)
        if not normal.isalpha() or len(normal) < 4 or abs(len(normal) - len(target)) > 3:
            continue
        ratio = difflib.SequenceMatcher(None, target, normal, autojunk=False).ratio()
        if ratio >= threshold:
            scored.append((ratio, word, normal))
    scored.sort(key=lambda item: item[0], reverse=True)
    if not scored:
        return None
    if len(scored) > 1 and scored[0][0] - scored[1][0] < 0.02:
        return None
    return scored[0][1]


def _line_rel(line: str, span_start: int) -> tuple[bool, bool]:
    left = span_start > 0 and line[span_start - 1].isalnum()
    tag = TAG_RE.match(line, span_start)
    end = tag.end() if tag else span_start
    right = end < len(line) and line[end].isalnum()
    return left, right


def _isolated_tag(token: str, start: int, end: int) -> bool:
    """The token is this one tag, surrounded by punctuation and nothing else."""
    rest = token[:start] + token[end:]
    return not any(char.isalnum() or char in "<>/" for char in rest)


def _apostrophe_suffix(token: str, start: int, end: int, content: str) -> bool:
    """``system’<sub>s</sub>``: the mark only completes a possessive."""
    if not (content.isalnum() and 1 <= len(content) <= 2):
        return False
    before, after = token[:start], token[end:]
    if any(char in "<>/" for char in before + after):
        return False
    head = before.lstrip(PUNCTUATION)
    return bool(head) and head.endswith(("'", "’")) and not after.strip(PUNCTUATION)


def _pack_blocks(items: list[dict], max_items: int, max_chars: int) -> list[list[dict]]:
    chunks, current, size = [], [], 0
    for item in items:
        rendered = _render_ai_item(item)
        if current and (len(current) >= max_items or size + len(rendered) > max_chars):
            chunks.append(current)
            current, size = [], 0
        current.append(item)
        size += len(rendered)
    if current:
        chunks.append(current)
    return chunks


def _render_ai_item(item: dict, number: int | None = None) -> str:
    label = f"{number}. " if number else ""
    offsets = ", ".join(f"{start}-{end}" for start, end in item["offsets"][:8])
    fragment = item["fragment"].replace("`", "'")
    neighbor = (item["pdf_neighbor"] or "（无 PDF 锚点）").replace("`", "'")
    return (f"## {label}第 {item['line']} 行（列 {offsets}）\n"
            f"MinerU：`{fragment}`\n"
            f"PDF 邻文：`{neighbor}`\n"
            f"原因：{item['reason']}\n")


def _render_pack(items: list[dict], number: int, total: int) -> str:
    body = "".join(_render_ai_item(item, index + 1) for index, item in enumerate(items))
    return f"# AI 裁决包 {number}/{total}\n\n{body}"


def _fragment(line: str, first: int, last: int, pad: int = 60) -> str:
    """A readable excerpt that never starts or ends inside a tag."""
    start, stop = 0, len(line)
    for token_start, token_end, _ in _tokens(line):
        if token_end >= first - pad:
            start = token_start
            break
    for token_start, token_end, _ in _tokens(line):
        if token_start >= last + pad:
            stop = token_start
            break
        stop = token_end
    return line[start:stop]


def _plan_core(text: str, index: dict, whitelist, max_pack_items: int) -> dict:
    spans = masked_spans(text)
    protected = _protected_bytes(text, spans)
    masked = _masked_text(text, spans)
    starts = _line_starts(text)
    lines = text.split("\n")
    masked_lines = masked.split("\n")
    patches, kept, ai_lines = [], [], {}
    previous = -10

    def add_patch(line_number, start, end, after, rule, reason, page):
        before = lines[line_number - 1][start:end]
        if not before or "\n" in before or "\n" in after:
            return
        line_start = starts[line_number - 1]
        if any(protected[line_start + start:line_start + end]):
            return
        patches.append({"id": f"L{line_number}-{start}-{end}", "line": line_number,
                        "start": start, "end": end, "before": before, "after": after,
                        "rule": rule, "reason": reason, "page": page})

    for number, line in enumerate(lines, 1):
        line_start = starts[number - 1]
        plain = _merge_tags(masked_lines[number - 1])
        word_count = len(_words(plain))
        window = None
        if word_count >= 3:
            anchor = _anchor(plain, index, previous)
            if anchor is not None:
                previous = anchor
                window = _window(index, anchor, word_count)
        page = window["page"] if window else None
        unresolved, reasons = [], set()

        for token_start, token_end, token in _tokens(line):
            if _overlaps(line_start + token_start, line_start + token_end, spans):
                continue
            tags = [(match, token_start + match.start(), token_start + match.end(), match.group("content"))
                    for match in TAG_RE.finditer(token)]
            if not tags:
                core = token.strip(PUNCTUATION)
                if len(core) < 6 or not core.isalpha() or not core.islower():
                    continue
                if _norm(core) in index["vocab"] or _found(window, core):
                    continue
                candidate = _candidate(core, window, 0.92)
                if not candidate:
                    continue
                lead = token[:len(token) - len(token.lstrip(PUNCTUATION))]
                trail = token[len(token.rstrip(PUNCTUATION)):]
                add_patch(number, token_start, token_end, lead + candidate + trail, "R5",
                          "无标签的词在 PDF 同窗内有唯一近邻", page)
                continue

            supers = []
            for match, start, end, content in tags:
                after = line[end] if end < len(line) else ""
                if (match.group("kind").lower() == "sup"
                        and _true_super(content, line[:start], after, whitelist)):
                    supers.append((match, start, end, content))
            others = [item for item in tags if item not in supers]
            if supers:
                kept.extend({"line": number, "text": match.group(0)} for match, _, _, _ in supers)
            if not others:
                continue

            merged = _apply_merge(token, token_start, others)
            core = merged.strip(PUNCTUATION)
            single = bool(re.fullmatch(r"[A-Za-z][A-Za-z'’\-]*", core or ""))
            points = all(not any(char.isalnum() for char in content)
                         for _, _, _, content in others)
            if core and _found(window, core):
                for match, start, end, content in others:
                    left, right = _line_rel(line, start)
                    rel_start, rel_end = start - token_start, end - token_start
                    if not (left or right):
                        # R6-lite only unwraps a tag that stands alone. The
                        # merged reading still has to be a verbatim PDF hit;
                        # shape alone is never enough to patch.
                        if (WHOLE_WORD_RE.fullmatch(content)
                                and _isolated_tag(token, rel_start, rel_end)
                                and _found(window, content)):
                            add_patch(number, start, end, content, "R6-lite",
                                      "整词包裹：删标记后该词在 PDF 同窗内逐字命中", page)
                            continue
                        if (_apostrophe_suffix(token, rel_start, rel_end, content)
                                and _found(window, core)):
                            add_patch(number, start, end, content, "R6-lite",
                                      "撇号后缀：合并结果在 PDF 同窗内逐字命中", page)
                            continue
                        unresolved.append((start, end))
                        reasons.add("独立标记，需人工/PDF 核查")
                        continue
                    if points:
                        rule, reason = "R4", "标签内容为标点，合并后字符序列与 PDF 一致"
                    else:
                        rule = "R1" if left and right else "R2"
                        reason = "合并词在 PDF 同窗内逐字命中"
                    add_patch(number, start, end, content, rule, reason, page)
                continue

            if single and window:
                candidate = _candidate(core, window, 0.90)
                if candidate and _norm(core) not in index["vocab"]:
                    lead = merged[:len(merged) - len(merged.lstrip(PUNCTUATION))]
                    trail = merged[len(merged.rstrip(PUNCTUATION)):]
                    add_patch(number, token_start, token_end, lead + candidate + trail, "R5",
                              f"合并词不在 PDF 同窗，取唯一近邻（{core} -> {candidate}）", page)
                    continue
            unresolved.extend((start, end) for _, start, end, _ in others)
            reasons.add("跨词或畸形片段" if not single else "合并词不在 PDF 同窗内")

        if unresolved:
            first = min(start for start, _ in unresolved)
            last = max(end for _, end in unresolved)
            fragment = _fragment(line, first, last)
            ai_lines[number] = {"line": number, "offsets": sorted(set(unresolved)),
                                "fragment": fragment,
                                "pdf_neighbor": window["text"][:700] if window else "",
                                "reason": "、".join(sorted(reasons)) or "未判定"}

    ai_items = [ai_lines[key] for key in sorted(ai_lines)]
    chunks = _pack_blocks(ai_items, max_pack_items, 12000)
    packs = [_render_pack(chunk, index + 1, len(chunks)) for index, chunk in enumerate(chunks)]
    touched = {patch["line"] for patch in patches}
    rules = {rule: sum(1 for patch in patches if patch["rule"] == rule)
             for rule in ("R1", "R2", "R4", "R5", "R6-lite")}
    return {
        "patches": sorted(patches, key=lambda item: (item["line"], item["start"])),
        "kept": kept,
        "ai_items": ai_items,
        "ai_packs": packs,
        "stats": {"rules": rules, "patches": len(patches), "lines_touched": len(touched),
                  "kept_whitelist": len(kept), "ai_items": len(ai_items),
                  "ai_packs": len(packs)},
    }


def apply_patches(text: str, patches) -> str:
    """Apply the plan to a copy; every `before` must still match exactly."""
    starts = _line_starts(text)
    edits = []
    for patch in patches:
        begin = starts[patch["line"] - 1] + patch["start"]
        finish = starts[patch["line"] - 1] + patch["end"]
        if text[begin:finish] != patch["before"]:
            raise RepairError(f"补丁与原文不一致：{patch['id']}")
        if "\n" in patch["after"]:
            raise RepairError(f"补丁会改变行数：{patch['id']}")
        edits.append((begin, finish, patch["after"]))
    edits.sort(reverse=True)
    previous = len(text)
    for begin, finish, after in edits:
        if finish > previous:
            raise RepairError("补丁区间重叠")
        previous = begin
        text = text[:begin] + after + text[finish:]
    return text


def render_diff(text: str, patches) -> str:
    lines = text.split("\n")
    grouped = {}
    for patch in patches:
        grouped.setdefault(patch["line"], []).append(patch)
    blocks = []
    for number in sorted(grouped):
        original = lines[number - 1]
        repaired = original
        for patch in sorted(grouped[number], key=lambda item: item["start"], reverse=True):
            repaired = repaired[:patch["start"]] + patch["after"] + repaired[patch["end"]:]
        blocks.append(f"L{number}\n- {original}\n+ {repaired}\n")
    return "\n".join(blocks)


def _protected_digest(text: str) -> str:
    spans = masked_spans(text)
    payload = "\x00".join(text[start:end] for start, end in spans)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _remap_line(start: int, end: int, patches_on_line) -> tuple[int, int]:
    """Translate a span in repaired text back to the original offsets."""
    delta = 0
    for patch in sorted(patches_on_line, key=lambda item: item["start"]):
        repaired_start = patch["start"] - delta
        repaired_end = repaired_start + len(patch["after"])
        if repaired_end <= start:
            delta += (patch["end"] - patch["start"]) - len(patch["after"])
        elif repaired_start >= end:
            break
        else:
            raise RepairError("区间落在已改动区段，无法映射回原文")
    return start + delta, end + delta


def _fold_patches(text: str, patches, extra) -> list:
    """Fold a later-round patch back into the original coordinates."""
    lines = text.split("\n")
    grouped = {}
    for patch in patches:
        grouped.setdefault(patch["line"], []).append(patch)
    seen = {(patch["line"], patch["start"], patch["end"]) for patch in patches}
    merged = list(patches)
    for patch in extra:
        start, end = _remap_line(patch["start"], patch["end"], grouped.get(patch["line"], []))
        if lines[patch["line"] - 1][start:end] != patch["before"]:
            raise RepairError(f"第二轮补丁无法映射回原文：{patch['id']}")
        if (patch["line"], start, end) in seen:
            continue
        seen.add((patch["line"], start, end))
        merged.append({**patch, "id": f"L{patch['line']}-{start}-{end}",
                       "start": start, "end": end})
    return merged


def _original_ai(items, text: str, patches) -> list:
    """Bring residual spans back to the MinerU line so the pack reads original."""
    lines = text.split("\n")
    grouped = {}
    for patch in patches:
        grouped.setdefault(patch["line"], []).append(patch)
    result = []
    for item in items:
        spans = []
        try:
            spans = [_remap_line(start, end, grouped.get(item["line"], []))
                     for start, end in item["offsets"]]
        except RepairError:
            result.append(item)
            continue
        line = lines[item["line"] - 1]
        first = min(start for start, _ in spans)
        last = max(end for _, end in spans)
        result.append({**item, "offsets": spans,
                       "fragment": _fragment(line, first, last)})
    return result


def build_plan(text: str, pdf_path, *, whitelist=(), checks: bool = True,
               max_pack_items: int = 20) -> dict:
    """Build a stage-one plan that is already a fixed point of application."""
    index = _pdf_index(pdf_path)
    base = _plan_core(text, index, whitelist, max_pack_items)
    patches = base["patches"]
    for _ in range(4):
        repaired = apply_patches(text, patches)
        extra = _plan_core(repaired, index, whitelist, max_pack_items)["patches"]
        if not extra:
            break
        patches = _fold_patches(text, patches, extra)
    else:
        raise RepairError("补丁计划四轮未收敛")

    repaired = apply_patches(text, patches)
    residual = _plan_core(repaired, index, whitelist, max_pack_items)
    ai_items = _original_ai(residual["ai_items"], text, patches)
    chunks = _pack_blocks(ai_items, max_pack_items, 12000)
    packs = [_render_pack(chunk, position + 1, len(chunks))
             for position, chunk in enumerate(chunks)]
    touched = {patch["line"] for patch in patches}
    rules = {rule: sum(1 for patch in patches if patch["rule"] == rule)
             for rule in ("R1", "R2", "R4", "R5", "R6-lite")}
    plan = {
        "patches": sorted(patches, key=lambda item: (item["line"], item["start"])),
        "kept": base["kept"],
        "ai_items": ai_items,
        "ai_packs": packs,
        "diff": render_diff(text, patches),
        "stats": {"rules": rules, "patches": len(patches), "lines_touched": len(touched),
                  "kept_whitelist": len(base["kept"]), "ai_items": len(ai_items),
                  "ai_packs": len(packs)},
    }
    if checks:
        before = audit_body(split_body(text))
        after = audit_body(split_body(repaired))
        verdicts = {
            "line_count": text.count("\n") == repaired.count("\n"),
            "protected_sha": _protected_digest(text) == _protected_digest(repaired),
            "whitelist_preserved": before["true_sup_count"] == after["true_sup_count"],
            "idempotent": not residual["patches"],
        }
        plan["checks"] = verdicts
        failed = [name for name, passed in verdicts.items() if not passed]
        if failed:
            raise RepairError("自检未通过：" + "、".join(failed))
    return plan


AUTO_RULES = ("R1", "R2", "R4", "R5", "R6-lite")


def apply_plan(text: str, patches, pdf_path, *, whitelist=(), max_pack_items: int = 20) -> dict:
    """Apply the automatic rules and re-run every stage-one assertion.

    `before` must still sit at its offset; text that already reads `after` is
    counted as applied-before, anything else is a conflict and aborts the whole
    write. Only R1/R2/R4/R5/R6-lite are applied — AI items stay untouched.
    """
    lines = text.split("\n")
    applied, already, conflicts = [], [], []
    grouped = {}
    for patch in patches:
        if patch["rule"] in AUTO_RULES:
            grouped.setdefault(patch["line"], []).append(patch)
    repaired_lines = []
    for number, line in enumerate(lines, 1):
        delta = 0
        for patch in sorted(grouped.get(number, []), key=lambda item: item["start"]):
            expected, replacement = patch["before"], patch["after"]
            if "\n" in replacement:
                conflicts.append({"id": patch["id"], "expected": expected, "found": "越界"})
                continue
            begin = patch["start"] + delta
            starts_before = line.startswith(expected, begin)
            starts_after = line.startswith(replacement, begin)
            if starts_before and not (starts_after and replacement.startswith(expected)):
                line = line[:begin] + replacement + line[begin + len(expected):]
                applied.append(patch["id"])
                delta += len(replacement) - len(expected)
            elif starts_after:
                already.append(patch["id"])
                delta += len(replacement) - len(expected)
            else:
                conflicts.append({"id": patch["id"], "expected": expected,
                                  "found": line[begin:begin + len(expected)][:80]})
        repaired_lines.append(line)
    if conflicts:
        first = conflicts[0]
        raise RepairError(f"{len(conflicts)} 条补丁与原文不一致（首条 {first['id']}："
                          f"期望 {first['expected']!r}，实际 {first['found']!r}），未写入")
    repaired = "\n".join(repaired_lines)

    before_quality = audit_body(split_body(text))
    after_quality = audit_body(split_body(repaired))
    residual = _plan_core(repaired, _pdf_index(pdf_path), whitelist, max_pack_items)
    verdicts = {
        "line_count": text.count("\n") == repaired.count("\n"),
        "protected_sha": _protected_digest(text) == _protected_digest(repaired),
        "whitelist_preserved": before_quality["true_sup_count"] == after_quality["true_sup_count"],
        "idempotent": not residual["patches"],
    }
    failed = [name for name, passed in verdicts.items() if not passed]
    if failed:
        raise RepairError("应用后自检未通过：" + "、".join(failed))
    return {"text": repaired, "applied": applied, "already_applied": already,
            "conflicts": conflicts, "checks": verdicts,
            "tags": {"before": before_quality["tags"], "after": after_quality["tags"],
                     "true_sup_before": before_quality["true_sup_count"],
                     "true_sup_after": after_quality["true_sup_count"],
                     "ai_lines": len(residual["ai_items"])}}


def guard_output(out, library_root) -> Path:
    """Refuse content directories, symlinked escapes, and non-directory targets."""
    root = Path(library_root).resolve()
    target = Path(out)
    if target.exists() and target.is_symlink():
        raise RepairError(f"输出路径是软链，拒绝写入：{target}")
    resolved = target.resolve()
    for name in ("md", "assets", "pdf"):
        blocked = (root / name).resolve()
        if resolved == blocked or blocked in resolved.parents:
            raise RepairError(f"拒绝写入资料库内容目录：{resolved}")
    for parent in [target, *target.parents]:
        if parent.exists() and parent.is_symlink():
            landing = parent.resolve()
            if not landing.is_relative_to(root) and landing != root:
                raise RepairError(f"输出路径经过库外软链：{parent}")
    if resolved.exists() and not resolved.is_dir():
        raise RepairError(f"输出路径不是目录：{resolved}")
    return resolved

