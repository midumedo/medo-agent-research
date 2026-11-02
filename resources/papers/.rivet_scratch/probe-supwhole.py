"""定位整词包裹里的 sup 实例，确认不是真上标。"""
import re, sys
from pathlib import Path

sys.path.insert(0, str(Path(r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")))
import pdf_repair as R

text = Path(r"d:\workspace\memory\resources\papers\md\arxiv-2504.19413v1.Project.Mem0.md").read_text(encoding="utf-8")
spans = R.masked_spans(text)
starts = R._line_starts(text)
lines = text.split("\n")
for match in R.TAG_RE.finditer(text):
    if R._overlaps(match.start(), match.end(), spans):
        continue
    if match.group("kind").lower() != "sup":
        continue
    content = match.group("content")
    if not re.fullmatch(r"[A-Za-z]{2,}", content):
        continue
    li = R._line_at(starts, match.start())
    col = match.start() - starts[li]
    left = lines[li][col - 1] if col else ""
    end = col + len(match.group(0))
    right = lines[li][end] if end < len(lines[li]) else ""
    print("L", li + 1, repr(content), "left", repr(left), "right", repr(right), "|",
          lines[li][max(0, col - 90):end + 60])
