import sys, time
from bisect import bisect_left, bisect_right
from pathlib import Path
sys.path.insert(0, str(Path(r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")))
import pdf_repair as R

md = Path(r"d:\workspace\memory\resources\papers\md\arxiv-2504.19413v1.Project.Mem0.md")
text = md.read_text(encoding="utf-8")
pdf = Path(r"d:\workspace\memory\resources\papers\pdf\arxiv-2504.19413v1.Project.Mem0.pdf")

index = R._pdf_index(pdf)
lines = index["lines"]
for size in range(3, 9):
    table = {}
    for i, line in enumerate(lines):
        for off in range(len(line["words"]) - size + 1):
            table.setdefault(tuple(line["words"][off:off + size]), []).append(i)
    index[f"{size}gram"] = table
R._pdf_index = lambda path: index

MATH = R.INLINE_DOLLAR_RE

def anchor_words(plain):
    stripped = MATH.sub(" ", plain)
    stripped = R.DOLLAR_BLOCK_RE.sub(" ", stripped)
    return R._words(stripped)

def make_anchor(floor_slack, sizes, prefer="offset"):
    def anchor(plain_line, index, previous):
        words = anchor_words(plain_line)
        floor = previous - floor_slack
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
                key = (offset, -size) if prefer == "offset" else (-size, offset)
                if best is None or key < best[0]:
                    best = (key, hits[cursor])
        return None if best is None else best[1]
    return anchor

for label, slack, sizes in [
    ("A slack80 8..3", 80, (8, 7, 6, 5, 4, 3)),
    ("B slack40 8..5", 40, (8, 7, 6, 5)),
]:
    R._anchor = make_anchor(slack, sizes)
    t0 = time.time()
    plan = R.build_plan(text, pdf)
    fixed = R.apply_patches(text, plan["patches"])
    residual = len(R.TAG_RE.findall(fixed))
    stats = plan["stats"]
    print(label, stats["rules"], "patches", stats["patches"], "ai", stats["ai_items"],
          "residual", residual, "checks", plan["checks"], f"{time.time()-t0:.0f}s")
