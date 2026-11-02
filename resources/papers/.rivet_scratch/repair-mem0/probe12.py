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
line_patches = [p for p in patches if p["line"] == 371]
delta = 0
print("n patches", len(line_patches))
for p in sorted(line_patches, key=lambda x: x["start"]):
    rs = p["start"] - delta
    print(p["start"], p["end"], repr(p["before"]), "->", repr(p["after"]), "repaired_at", rs)
    delta += (p["end"] - p["start"]) - len(p["after"])
    if p["start"] > 950:
        break
print("delta total", delta)
print("repaired L371 around 930:", repr(repaired.split("\n")[370][900:1000]))
print("original L371 around 900:", repr(text.split("\n")[370][900:1000]))
