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
line_patches = sorted([p for p in patches if p["line"] == 371], key=lambda x: x["start"])
delta = 0
for p in line_patches:
    rs = p["start"] - delta
    re = rs + len(p["after"])
    if 920 <= rs <= 950 or 920 <= re <= 950:
        print("orig", p["start"], p["end"], "rep", rs, re, repr(p["before"]), "->", repr(p["after"]))
    delta += (p["end"] - p["start"]) - len(p["after"])
print("original 1340..1400:", repr(text.split("\n")[370][1340:1400]))
print("repaired 920..950:", repr(repaired.split("\n")[370][920:950]))
