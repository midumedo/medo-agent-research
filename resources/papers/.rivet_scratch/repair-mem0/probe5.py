import sys
import re
import pathlib

sys.path.insert(0, r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")
import pdf_repair as R

md = pathlib.Path(r"d:\workspace\memory\resources\papers\md\arxiv-2504.19413v1.Project.Mem0.md")
pdf = r"d:\workspace\memory\resources\papers\pdf\arxiv-2504.19413v1.Project.Mem0.pdf"
text = md.read_text(encoding="utf-8")
index = R._pdf_index(pdf)
spans = R.masked_spans(text)
starts = R._line_starts(text)
lines = text.split("\n")
masked_lines = R._masked_text(text, spans).split("\n")

previous = -10
stats = {"win": 0, "nowin": 0, "overlap_tokens": 0}
for number, line in enumerate(lines, 1):
    if not R.TAG_RE.search(line):
        continue
    plain = R._merge_tags(masked_lines[number - 1])
    wc = len(R._words(plain))
    anchor = R._anchor(plain, index, previous) if wc >= 3 else None
    if anchor is None:
        stats["nowin"] += 1
        window = None
    else:
        previous = anchor
        stats["win"] += 1
        window = R._window(index, anchor, wc)
    overlap = sum(1 for s, e, t in R._tokens(line)
                  if R._overlaps(starts[number - 1] + s, starts[number - 1] + e, spans))
    stats["overlap_tokens"] += overlap
    if number in (19, 21, 25, 28, 30, 157, 161, 167):
        print("\nL", number, "page", window["page"] if window else None,
              "win?", bool(window), "tokens", len(R._tokens(line)), "overlap", overlap)
        print("  plain:", plain[:140])
        if window:
            print("  win  :", window["text"][:140])
        for s, e, t in R._tokens(line)[:6]:
            if not R.TAG_RE.search(t):
                continue
            merged = R._merge_tags(t)
            core = merged.strip(R.PUNCTUATION)
            print("   token", repr(t[:40]), "->", repr(core), "found", R._found(window, core))
print("\nsummary", stats)
