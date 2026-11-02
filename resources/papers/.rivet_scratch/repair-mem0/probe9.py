import sys
import pathlib

sys.path.insert(0, r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")
import pdf_repair as R

md = pathlib.Path(r"d:\workspace\memory\resources\papers\md\arxiv-2504.19413v1.Project.Mem0.md")
pdf = r"d:\workspace\memory\resources\papers\pdf\arxiv-2504.19413v1.Project.Mem0.pdf"
text = md.read_text(encoding="utf-8")
plan = R.build_plan(text, pdf, checks=False)
repaired = R.apply_patches(text, plan["patches"])
orig = text.split("\n")
new = repaired.split("\n")
for needle in ("encodin", "realworld", "uestions,"):
    for n, line in enumerate(new, 1):
        pos = line.find(needle)
        if pos >= 0:
            print("\n", needle, "L", n, repr(line[max(0, pos - 70):pos + 40]))
            patches = [p for p in plan["patches"] if p["line"] == n]
            for p in patches:
                if p["start"] > pos + 40 and p["start"] < pos + 200:
                    continue
                print("   ", p["start"], p["end"], repr(p["before"]), "->", repr(p["after"]))
            print("  orig:", repr(orig[n - 1][:150]))
