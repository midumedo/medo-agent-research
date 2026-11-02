import json
import sys
import pathlib

sys.path.insert(0, r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")
import pdf_repair as R

md = pathlib.Path(r"d:\workspace\memory\resources\papers\md\arxiv-2504.19413v1.Project.Mem0.md")
pdf = r"d:\workspace\memory\resources\papers\pdf\arxiv-2504.19413v1.Project.Mem0.pdf"
text = md.read_text(encoding="utf-8")
plan = R.build_plan(text, pdf)
print(json.dumps(plan["stats"], ensure_ascii=False))
print(json.dumps(plan["checks"], ensure_ascii=False))
print("\nR5:")
for p in plan["patches"]:
    if p["rule"] == "R5":
        print(" L", p["line"], repr(p["before"]), "->", repr(p["after"]))
print("\nkept:")
for k in plan["kept"]:
    print(" ", k)
print("\nAI packs", [len(p.splitlines()) for p in plan["ai_packs"]])
for p in plan["ai_items"][:5]:
    print(" ", p["line"], p["reason"], repr(p["fragment"][:120]))
