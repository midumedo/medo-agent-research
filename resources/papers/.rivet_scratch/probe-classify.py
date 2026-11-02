import sys
from collections import Counter
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
spans = R.masked_spans(fixed)
starts = R._line_starts(fixed)
counter = Counter()
samples = {}
for match in R.TAG_RE.finditer(fixed):
    line = R._line_at(starts, match.start())
    row = fixed[starts[line]: match.start()]
    left = match.start() - starts[line]
    line_text = fixed.split("\n")[line]
    protected = R._overlaps(match.start(), match.end(), spans)
    content = match.group("content")
    l_ok = left > 0 and line_text[left - 1].isalnum()
    r_end = left + len(match.group(0))
    r_ok = r_end < len(line_text) and line_text[r_end].isalnum()
    if protected:
        key = "protected"
    elif any(c.isspace() for c in content):
        key = "content has space"
    elif not l_ok and not r_ok:
        key = "standalone word tag"
    elif not l_ok or not r_ok:
        key = "one-sided"
    else:
        key = "internal"
    counter[key] += 1
    samples.setdefault(key, []).append((line + 1, line_text[max(0, left - 40): r_end + 40]))
print(counter, "total", sum(counter.values()))
for key, rows in samples.items():
    print("\n###", key)
    for line, snippet in rows[:6]:
        print(" L", line, "|", snippet.replace("\n", " "))
