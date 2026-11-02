"""打印样本行的 PDF 窗口与切句，核对回填可行性。"""
import re, sys
from pathlib import Path

sys.path.insert(0, str(Path(r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")))
import pdf_repair as R

root = Path(r"d:\workspace\memory\resources\papers")
text = (root / "md" / "arxiv-2504.19413v1.Project.Mem0.md").read_text(encoding="utf-8")
index = R._pdf_index(root / "pdf" / "arxiv-2504.19413v1.Project.Mem0.pdf")
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

for n in (161, 25, 38, 28, 44):
    w = windows[n]
    print("=" * 20, "L", n, "page", w["page"], "words", len(w["words"]))
    print(w["text"][:2400])
    print()
