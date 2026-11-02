import sys
import pathlib
from collections import Counter

sys.path.insert(0, r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")
import pdf_repair as R

md = pathlib.Path(r"d:\workspace\memory\resources\papers\md\arxiv-2504.19413v1.Project.Mem0.md")
pdf = r"d:\workspace\memory\resources\papers\pdf\arxiv-2504.19413v1.Project.Mem0.pdf"
text = md.read_text(encoding="utf-8")
plan = R.build_plan(text, pdf, checks=False)
print("stats", plan["stats"])
repaired = R.apply_patches(text, plan["patches"])
again = R._plan_core(repaired, R._pdf_index(pdf), R.DEFAULT_WHITELIST, 20)
print("second", again["stats"])
print(Counter(p["rule"] for p in again["patches"]))
for p in again["patches"][:20]:
    print(p["line"], p["rule"], repr(p["before"]), "->", repr(p["after"]), p["reason"])
