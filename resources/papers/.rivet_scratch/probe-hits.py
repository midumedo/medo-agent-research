import sys
from pathlib import Path
sys.path.insert(0, str(Path(r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")))
import pdf_repair as R

md = Path(r"d:\workspace\memory\resources\papers\md\arxiv-2504.19413v1.Project.Mem0.md")
text = md.read_text(encoding="utf-8")
pdf = Path(r"d:\workspace\memory\resources\papers\pdf\arxiv-2504.19413v1.Project.Mem0.pdf")
index = R._pdf_index(pdf)

# word stream with line index
stream, owner = [], []
for li, line in enumerate(index["lines"]):
    for w in line["words"]:
        stream.append(w)
        owner.append(li)
print("pdf words", len(stream), "pdf lines", len(index["lines"]))

starts, pos = {}, {}
for li in range(len(index["lines"])):
    pos[li] = sum(len(l["words"]) for l in index["lines"][:li])

def occurrences(words, size=8):
    key = tuple(words[:size])
    hits = []
    n = size
    for i in range(len(stream) - n + 1):
        if tuple(stream[i:i+n]) == key:
            hits.append(owner[i])
    return hits

prev = -10
for n, line in enumerate(text.split("\n"), 1):
    plain = R._merge_tags(line)
    wc = len(R._words(plain))
    if wc < 3:
        continue
    words = R._words(plain)
    hits = occurrences(words)
    if n in (34, 49, 120, 122, 124, 128, 134, 151, 157, 161, 167, 371, 373, 377, 379):
        print(f"L{n} wc={wc} prev={prev} hits8={hits[:6]} count={len(hits)}")
    # advance using best hit now
    a = R._anchor(plain, index, prev)
    if a is not None:
        prev = a
