import sys
import pathlib

sys.path.insert(0, r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")
import pdf_repair as R

md = pathlib.Path(r"d:\workspace\memory\resources\papers\md\arxiv-2504.19413v1.Project.Mem0.md")
pdf = r"d:\workspace\memory\resources\papers\pdf\arxiv-2504.19413v1.Project.Mem0.pdf"
text = md.read_text(encoding="utf-8")
index = R._pdf_index(pdf)
print("pdf lines", len(index["lines"]), "shingles", len(index["shingles"]), "vocab", len(index["vocab"]))

spans = R.masked_spans(text)
starts = R._line_starts(text)
previous = -10
none_lines, ok_lines = [], []
for number, line in enumerate(text.split("\n"), 1):
    line_start = starts[number - 1]
    if any(s <= line_start < e for s, e in spans):
        continue
    if not R.TAG_RE.search(line):
        continue
    plain = R.TAG_RE.sub("", line)
    words = R._words(plain)
    anchor = R._anchor(plain, index, previous) if len(words) >= 3 else None
    if anchor is None:
        none_lines.append(number)
        continue
    previous = anchor
    window = R._window(index, anchor, len(words))
    ok_lines.append(number)
    if number in (122, 161, 167, 179):
        print("\nL", number, "anchor", anchor, "page", window["page"])
        print("plain ", plain[:200])
        print("window", window["text"][:200])

print("\ntagged lines anchored", len(ok_lines), "anchor failed", len(none_lines))
print("failed lines", none_lines[:30])
