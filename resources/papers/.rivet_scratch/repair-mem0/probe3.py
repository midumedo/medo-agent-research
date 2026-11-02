import sys
import pathlib

sys.path.insert(0, r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")
import pdf_repair as R

p = pathlib.Path(r"d:\workspace\memory\resources\papers\md\arxiv-2504.19413v1.Project.Mem0.md")
t = p.read_text(encoding="utf-8")
plan = R.build_plan(t, r"d:\workspace\memory\resources\papers\pdf\arxiv-2504.19413v1.Project.Mem0.pdf", checks=False)
print(plan["kept"])
lines = t.split("\n")
for ln in (122, 149):
    line = lines[ln - 1]
    for m in R.TAG_RE.finditer(line):
        if m.group("content") == "g":
            start = m.start()
            print(ln, start, repr(line[max(0, start - 25):start + 30]), R._true_super("g", line[:start], line[m.end()] if m.end() < len(line) else "", ()))
