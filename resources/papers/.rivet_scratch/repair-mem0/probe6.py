import sys
import pathlib
from collections import Counter

sys.path.insert(0, r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")
import pdf_repair as R

md = pathlib.Path(r"d:\workspace\memory\resources\papers\md\arxiv-2504.19413v1.Project.Mem0.md")
pdf = r"d:\workspace\memory\resources\papers\pdf\arxiv-2504.19413v1.Project.Mem0.pdf"
text = md.read_text(encoding="utf-8")
plan = R.build_plan(text, pdf, checks=False)
counts = Counter(p["line"] for p in plan["patches"])
print(sorted(counts.items()))
print("ai lines", len(plan["ai_items"]))
print("ai no anchor", sum(1 for i in plan["ai_items"] if not i["pdf_neighbor"]))
print("L30 patches", [p for p in plan["patches"] if p["line"] == 30][:5])
print("L157 patches", [p for p in plan["patches"] if p["line"] == 157][:5])
idx = {i["line"]: i for i in plan["ai_items"]}
for ln in (30, 157, 161):
    print("\nL", ln, "AI:", idx.get(ln))
