import sys
import pathlib

sys.path.insert(0, r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")
import pdf_repair as R

md = pathlib.Path(r"d:\workspace\memory\resources\papers\md\arxiv-2504.19413v1.Project.Mem0.md")
pdf = r"d:\workspace\memory\resources\papers\pdf\arxiv-2504.19413v1.Project.Mem0.pdf"
text = md.read_text(encoding="utf-8")
plan = R.build_plan(text, pdf)
fixed = R.apply_patches(text, plan["patches"])
orig = text.split("\n")
new = fixed.split("\n")

for label, line_no, needle in (("L128", 128, "multi-ho"), ("L161", 161, "graph"), ("L25", 25, "foundation"), ("L157", 157, "efficiency"), ("L161b", 161, "construct")):
    o = orig[line_no - 1].find(needle)
    n = new[line_no - 1].find(needle)
    print(f"\n{label} orig:", repr(orig[line_no - 1][max(0, o - 70):o + 90]))
    print(f"{label} new :", repr(new[line_no - 1][max(0, n - 70):n + 90]))

touched = set()
for p in plan["patches"]:
    line = orig[p["line"] - 1]
    for s, e, tok in R._tokens(line):
        if s <= p["start"] < e:
            touched.add((p["line"], s, e))
print("\ndistinct tokens", len(touched))
print("packs", len(plan["ai_packs"]) + 1 if plan["ai_packs"] else 0)
print("pack sizes", [p.count("\n### ") for p in plan["ai_packs"]])
