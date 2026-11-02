import sys
import pathlib

sys.path.insert(0, r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")
import pdf_repair as R

md = pathlib.Path(r"d:\workspace\memory\resources\papers\md\arxiv-2504.19413v1.Project.Mem0.md")
pdf = r"d:\workspace\memory\resources\papers\pdf\arxiv-2504.19413v1.Project.Mem0.pdf"
text = md.read_text(encoding="utf-8")
index = R._pdf_index(pdf)
lines = text.split("\n")
line = lines[370]
spans = R.masked_spans(text)
masked_lines = R._masked_text(text, spans).split("\n")

# replicate previous through line 371
previous = -10
for number in range(1, 372):
    plain = R._merge_tags(masked_lines[number - 1])
    wc = len(R._words(plain))
    if wc >= 3:
        a = R._anchor(plain, index, previous)
        if a is not None:
            previous = a
            if number == 371:
                window = R._window(index, a, wc)
                print("anchor", a, "page", window["page"])

for s, e, tok in R._tokens(line):
    if "causa" in tok:
        tags = [(m, s + m.start(), s + m.end(), m.group("content")) for m in R.TAG_RE.finditer(tok)]
        merged = R._apply_merge(tok, s, tags)
        core = merged.strip(R.PUNCTUATION)
        print("token", s, e, repr(tok))
        print("  merged", repr(core), "found", R._found(window, core))
        print("  cand", R._candidate(core, window, 0.90))
