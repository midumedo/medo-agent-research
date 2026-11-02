"""核对 R6-lite 候选的 PDF 守卫与单字母边界。"""
import re, sys
from collections import Counter
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

cands, letters, sup_whole = [], [], []
for match in R.TAG_RE.finditer(text):
    if R._overlaps(match.start(), match.end(), spans):
        continue
    li = R._line_at(starts, match.start())
    col = match.start() - starts[li]
    left = lines[li][col - 1] if col else ""
    end = col + len(match.group(0))
    right = lines[li][end] if end < len(lines[li]) else ""
    content = match.group("content")
    kind = match.group("kind").lower()
    standalone = not left.isalnum() and not right.isalnum()
    if left in ("'", "’") and len(content) <= 2 and content.isalnum():
        cands.append((li + 1, kind, content, R._found(windows.get(li + 1), R._merge_tags(lines[li]).strip(R.PUNCTUATION))))
    elif re.fullmatch(r"[A-Za-z]{2,}", content) and standalone:
        cands.append((li + 1, kind, content, R._found(windows.get(li + 1), content)))
    elif re.fullmatch(r"[A-Za-z]", content) and standalone:
        letters.append((li + 1, kind, content, R._found(windows.get(li + 1), content),
                        lines[li][max(0, col - 40):end + 25]))
    elif re.fullmatch(r"[A-Za-z]+", content) and standalone and kind == "sup":
        sup_whole.append((li + 1, kind, content))

print("candidates", len(cands), "found", sum(1 for c in cands if c[3]), "miss", sum(1 for c in cands if not c[3]))
print("no window lines", sorted({c[0] for c in cands if c[0] not in windows}))
print("misses", [c for c in cands if not c[3]])
print("letter-only", len(letters), Counter((c[1], c[2]) for c in letters))
for row in letters:
    print(" L", row[0], row[1], repr(row[2]), "found", row[3], "|", row[4])
print("sup whole", sup_whole)
