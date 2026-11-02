import sys, re, json
from pathlib import Path
sys.path.insert(0, str(Path(r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")))
import pdf_repair as R

md = Path(r"d:\workspace\memory\resources\papers\md\arxiv-2504.19413v1.Project.Mem0.md")
text = md.read_text(encoding="utf-8")
pdf = Path(r"d:\workspace\memory\resources\papers\pdf\arxiv-2504.19413v1.Project.Mem0.pdf")
plan = R.build_plan(text, pdf)
fixed = R.apply_patches(text, plan["patches"])
rows = []
for n, line in enumerate(fixed.split("\n"), 1):
    tags = len(R.TAG_RE.findall(line))
    if tags:
        rows.append((tags, n))
rows.sort(reverse=True)
print("residual total", sum(t for t, _ in rows), "lines", len(rows))
for t, n in rows[:20]:
    print(t, n)

index = R._pdf_index(pdf)
prev = -10
print("\nanchor sample")
for n, line in enumerate(text.split("\n"), 1):
    plain = R._merge_tags(line)
    wc = len(R._words(plain))
    if wc < 3:
        continue
    a = R._anchor(plain, index, prev)
    if a is not None:
        prev = a
    if n in (19, 25, 34, 49, 122, 124, 157, 161):
        w = R._window(index, a, wc) if a is not None else None
        print(n, "wc", wc, "anchor", a, "page", w["page"] if w else None)
        print("   plain:", plain[:80])
        if w:
            print("   win  :", w["text"][:80], "|", w["text"][-60:])
