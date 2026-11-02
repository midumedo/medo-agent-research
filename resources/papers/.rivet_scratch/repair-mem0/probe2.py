import sys
import pathlib

sys.path.insert(0, r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")
import pdf_repair as R

p = pathlib.Path(r"d:\workspace\memory\resources\papers\md\arxiv-2504.19413v1.Project.Mem0.md")
t = p.read_text(encoding="utf-8")
body = R.split_body(t)
off = t[: len(t) - len(body)].count("\n")
bl = body.split("\n")
spans = R.masked_spans(t)
starts = R._line_starts(t)
for ln in (47, 61, 65, 65, 113, 140):
    file_line = ln + off
    line_start = starts[file_line - 1]
    masked_line = any(s <= line_start < e for s, e in spans)
    print("body", ln, "file", file_line, "masked", masked_line, repr(bl[ln - 1][:90]))
