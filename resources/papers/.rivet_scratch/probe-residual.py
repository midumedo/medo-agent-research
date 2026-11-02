import sys, re
from pathlib import Path
sys.path.insert(0, str(Path(r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")))
import pdf_repair as R

md = Path(r"d:\workspace\memory\resources\papers\md\arxiv-2504.19413v1.Project.Mem0.md")
text = md.read_text(encoding="utf-8")
pdf = Path(r"d:\workspace\memory\resources\papers\pdf\arxiv-2504.19413v1.Project.Mem0.pdf")
plan = R.build_plan(text, pdf)
fixed = R.apply_patches(text, plan["patches"])
index = R._pdf_index(pdf)
print("pdf lines", len(index["lines"]))

prev = -10
anchors = {}
for n, line in enumerate(text.split("\n"), 1):
    plain = R._merge_tags(line)
    wc = len(R._words(plain))
    if wc < 3:
        continue
    a = R._anchor(plain, index, prev)
    if a is not None:
        prev = a
    anchors[n] = (a, wc)

rows = []
for n, line in enumerate(fixed.split("\n"), 1):
    tags = len(R.TAG_RE.findall(line))
    if tags:
        rows.append((tags, n))
rows.sort(reverse=True)
for t, n in rows[:12]:
    a, wc = anchors.get(n, (None, 0))
    w = R._window(index, a, wc) if a is not None else None
    print(f"\n=== L{n} tags={t} wc={wc} anchor={a}")
    print("PLAIN:", R._merge_tags(text.split("\n")[n-1])[:120])
    print("FIXED:", line[:120])
    if w:
        print("WIN  :", w["text"][:120])
        print("WINend:", w["text"][-80:])
