"""枚举当前 Mem0 正文里符合 R6-lite 两类的标签，核对边界。"""
import re, sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")))
import pdf_repair as R

md_path = Path(r"d:\workspace\memory\resources\papers\md\arxiv-2504.19413v1.Project.Mem0.md")
text = md_path.read_text(encoding="utf-8")
spans = R.masked_spans(text)
starts = R._line_starts(text)
lines = text.split("\n")

whole, apo, other_standalone = [], [], []
kinds = Counter()
for match in R.TAG_RE.finditer(text):
    if R._overlaps(match.start(), match.end(), spans):
        kinds["protected"] += 1
        continue
    li = R._line_at(starts, match.start())
    col = match.start() - starts[li]
    left = lines[li][col - 1] if col else ""
    end = col + len(match.group(0))
    right = lines[li][end] if end < len(lines[li]) else ""
    content = match.group("content")
    kind = match.group("kind").lower()
    if left in ("'", "’") and len(content) <= 2 and content.isalnum():
        apo.append((li + 1, kind, content, lines[li][max(0, col - 40):end + 25]))
    elif re.fullmatch(r"[A-Za-z]{2,}", content) and not left.isalnum() and not right.isalnum():
        whole.append((li + 1, kind, content, lines[li][max(0, col - 40):end + 25]))
    elif not left.isalnum() and not right.isalnum():
        other_standalone.append((li + 1, kind, content, lines[li][max(0, col - 40):end + 25]))

print("protected tags", kinds["protected"])
print("whole-word", len(whole), Counter(k for _, k, _, _ in whole))
print("apostrophe", len(apo), Counter(k for _, k, _, _ in apo))
print("other standalone", len(other_standalone), Counter(k for _, k, _, _ in other_standalone))
print("contents", Counter(c for _, _, c, _ in whole).most_common())
print("\n-- apostrophe")
for row in apo:
    print(" L", row[0], row[1], "|", row[3])
print("\n-- other standalone (first 25)")
for row in other_standalone[:25]:
    print(" L", row[0], row[1], repr(row[2]), "|", row[3])
print("\n-- whole-word (first 12)")
for row in whole[:12]:
    print(" L", row[0], row[1], repr(row[2]), "|", row[3])
