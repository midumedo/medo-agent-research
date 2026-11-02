import json, sys, re
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")))
import pdf_repair as R

d = Path(r"d:\workspace\memory\resources\papers\.rivet_scratch\repair-mem0")
payload = json.loads((d / "patches.json").read_text(encoding="utf-8"))
text = Path(payload["md"]).read_text(encoding="utf-8")
fixed = R.apply_patches(text, payload["patches"])
spans = R.masked_spans(fixed)
starts = R._line_starts(fixed)
rows = fixed.split("\n")
counter = Counter()
examples = {}
for match in R.TAG_RE.finditer(fixed):
    li = R._line_at(starts, match.start())
    col = match.start() - starts[li]
    left = rows[li][col - 1] if col else ""
    end = col + len(match.group(0))
    right = rows[li][end] if end < len(rows[li]) else ""
    if R._overlaps(match.start(), match.end(), spans):
        key = "protected"
    elif left.isalnum() or right.isalnum():
        key = "adjacent"
    elif left in ("'", "’") and len(match.group("content")) <= 2:
        key = "apostrophe suffix"
    elif re.fullmatch(r"[A-Za-z]+", match.group("content")):
        key = "wrapped word"
    else:
        key = "other standalone"
    counter[key] += 1
    if key in ("apostrophe suffix", "other standalone"):
        examples.setdefault(key, []).append((li + 1, rows[li][max(0, col - 30): end + 30]))
print(counter, "total", sum(counter.values()))
for key in ("apostrophe suffix", "other standalone"):
    print("\n###", key)
    for line, chunk in examples.get(key, [])[:10]:
        print(" L", line, "|", chunk)
