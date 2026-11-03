"""只核对撇号后缀 token 的 PDF 守卫（按 token 合并，不按整行）。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")))
import pdf_repair as R

md_path = Path(r"d:\workspace\memory\resources\papers\md\arxiv-2504.19413v1.Project.Mem0.md")
pdf_path = Path(r"d:\workspace\memory\resources\papers\pdf\arxiv-2504.19413v1.Project.Mem0.pdf")
text = md_path.read_text(encoding="utf-8")
index = R._pdf_index(pdf_path)
spans = R.masked_spans(text)
starts = R._line_starts(text)
lines = text.split("\n")

previous = -10
windows = {}
for number, line in enumerate(lines, 1):
    plain = R._merge_tags(R._masked_text(text, spans).split("\n")[number - 1])
    wc = len(R._words(plain))
    if wc >= 3:
        anchor = R._anchor(plain, index, previous)
        if anchor is not None:
            previous = anchor
            windows[number] = R._window(index, anchor, wc)

for number, line in enumerate(lines, 1):
    for token_start, token_end, token in R._tokens(line):
        matches = [(m, token_start + m.start(), token_start + m.end(), m.group("content"))
                   for m in R.TAG_RE.finditer(token)]
        if not matches:
            continue
        if not any(token[start - token_start - 1:start - token_start] in ("'", "’")
                   and len(content) <= 2 for _, start, _, content in matches):
            continue
        merged = R._apply_merge(token, token_start, matches)
        core = merged.strip(R.PUNCTUATION)
        print(f"L{number}", repr(token), "->", repr(core), "found", R._found(windows.get(number), core))
