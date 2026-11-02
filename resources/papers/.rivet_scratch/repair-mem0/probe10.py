import sys
import pathlib

sys.path.insert(0, r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")
import pdf_repair as R

md = pathlib.Path(r"d:\workspace\memory\resources\papers\md\arxiv-2504.19413v1.Project.Mem0.md")
pdf = r"d:\workspace\memory\resources\papers\pdf\arxiv-2504.19413v1.Project.Mem0.pdf"
text = md.read_text(encoding="utf-8")
index = R._pdf_index(pdf)
base = R._plan_core(text, index, R.DEFAULT_WHITELIST, 20)
patches = base["patches"]
repaired = R.apply_patches(text, patches)
extra = R._plan_core(repaired, index, R.DEFAULT_WHITELIST, 20)["patches"]
print("extra", len(extra))
grouped = {}
for p in patches:
    grouped.setdefault(p["line"], []).append(p)
for p in extra:
    try:
        R._remap_line(p["start"], p["end"], grouped.get(p["line"], []))
    except R.RepairError:
        print("CONFLICT", p)
        for q in grouped.get(p["line"], []):
            if q["start"] <= p["start"] <= q["end"] or abs(q["start"] - p["start"]) < 20:
                print("   near", q)
        print("   repaired:", repr(repaired.split("\n")[p["line"] - 1][max(0, p["start"] - 60):p["start"] + 60]))
        print("   original:", repr(text.split("\n")[p["line"] - 1][:120]))
        break
