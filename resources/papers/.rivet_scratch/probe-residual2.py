import sys
from bisect import bisect_left
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

def anchor_words(plain):
    return R._words(R.DOLLAR_BLOCK_RE.sub(" ", R.INLINE_DOLLAR_RE.sub(" ", plain)))

def anchor(plain_line, index, previous):
    words = anchor_words(plain_line)
    floor = previous - 40
    best = None
    for size in (8, 7, 6, 5):
        table = index[f"{size}gram"]
        for offset in range(len(words) - size + 1):
            hits = table.get(tuple(words[offset:offset + size]))
            if not hits:
                continue
            cursor = bisect_left(hits, floor)
            if cursor == len(hits):
                continue
            key = (offset, -size)
            if best is None or key < best[0]:
                best = (key, hits[cursor])
    return None if best is None else best[1]
R._anchor = anchor

plan = R.build_plan(text, pdf)
fixed = R.apply_patches(text, plan["patches"])
rows = [(len(R.TAG_RE.findall(l)), n, l) for n, l in enumerate(fixed.split("\n"), 1)]
rows = [r for r in rows if r[0]]
rows.sort(reverse=True)
print("residual", sum(r[0] for r in rows), "lines", len(rows))
for t, n, l in rows[:20]:
    print(f"\nL{n} tags={t}")
    print("  ", l[:200])
print("\nkept", plan["stats"]["kept"])
print("ai items", len(plan["ai_items"]), "packs", len(plan["packs"]))
