import sys
import pathlib

sys.path.insert(0, r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")
import pdf_repair as R

md = pathlib.Path(r"d:\workspace\memory\resources\papers\md\arxiv-2504.19413v1.Project.Mem0.md")
pdf = r"d:\workspace\memory\resources\papers\pdf\arxiv-2504.19413v1.Project.Mem0.pdf"
text = md.read_text(encoding="utf-8")
index = R._pdf_index(pdf)
spans = R.masked_spans(text)
lines = text.split("\n")
masked_lines = R._masked_text(text, spans).split("\n")

previous = -10
jumps = []
records = []
for number, line in enumerate(lines, 1):
    plain = R._merge_tags(masked_lines[number - 1])
    wc = len(R._words(plain))
    anchor = R._anchor(plain, index, previous) if wc >= 3 else None
    if anchor is not None:
        if anchor < previous:
            jumps.append((number, previous, anchor))
        previous = anchor
    records.append((number, bool(R.TAG_RE.search(line)), anchor))

print("backward jumps", jumps[:20], "count", len(jumps))
for rec in records:
    if rec[1]:
        print(rec)
