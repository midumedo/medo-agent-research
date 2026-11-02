import sys, time
from bisect import bisect_left
from pathlib import Path
sys.path.insert(0, str(Path(r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")))
import pdf_repair as R

md = Path(r"d:\workspace\memory\resources\papers\md\arxiv-2504.19413v1.Project.Mem0.md")
text = md.read_text(encoding="utf-8")
pdf = Path(r"d:\workspace\memory\resources\papers\pdf\arxiv-2504.19413v1.Project.Mem0.pdf")

index = R._pdf_index(pdf)
for size in range(3, 9):
    table = {}
    for i, line in enumerate(index["lines"]):
        for off in range(len(line["words"]) - size + 1):
            table.setdefault(tuple(line["words"][off:off + size]), []).append(i)
    index[f"{size}gram"] = table
R._pdf_index = lambda path: index

def anchor_words(plain):
    return R._words(R.DOLLAR_BLOCK_RE.sub(" ", R.INLINE_DOLLAR_RE.sub(" ", plain)))

def maker(slack, sizes, offset_first=True):
    def anchor(plain_line, index, previous):
        words = anchor_words(plain_line)
        floor = previous - slack
        best = None
        for size in sizes:
            table = index[f"{size}gram"]
            for offset in range(len(words) - size + 1):
                hits = table.get(tuple(words[offset:offset + size]))
                if not hits:
                    continue
                cursor = bisect_left(hits, floor)
                if cursor == len(hits):
                    continue
                key = (offset, -size) if offset_first else (-size, offset)
                if best is None or key < best[0]:
                    best = (key, hits[cursor])
        return None if best is None else best[1]
    return anchor

for label, slack, sizes, of in [
    ("8-5 s40", 40, (8, 7, 6, 5), True),
    ("8-4 s40", 40, (8, 7, 6, 5, 4), True),
    ("8-3 s40", 40, (8, 7, 6, 5, 4, 3), True),
    ("8-5 s80", 80, (8, 7, 6, 5), True),
    ("8-5 s20", 20, (8, 7, 6, 5), True),
    ("len-first 8-5 s40", 40, (8, 7, 6, 5), False),
]:
    R._anchor = maker(slack, sizes, of)
    t0 = time.time()
    plan = R.build_plan(text, pdf)
    fixed = R.apply_patches(text, plan["patches"])
    outside = R._masked_text(fixed, R.masked_spans(fixed))
    residual = len(R.TAG_RE.findall(outside))
    print(label, plan["stats"]["rules"], "patches", plan["stats"]["patches"],
          "ai", plan["stats"]["ai_items"], "outer-residual", residual,
          "checks", all(plan["checks"].values()), f"{time.time()-t0:.0f}s")
