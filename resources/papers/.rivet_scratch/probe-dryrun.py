"""在副本上 dry-run R6-lite：统计命中、降级、样例与残留构成。"""
import re, sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")))
import pdf_repair as R

root = Path(r"d:\workspace\memory\resources\papers")
live = root / "md" / "arxiv-2504.19413v1.Project.Mem0.md"
pdf = root / "pdf" / "arxiv-2504.19413v1.Project.Mem0.pdf"
copy = root / ".rivet_scratch" / "dryrun-r6lite.md"
copy.write_text(live.read_text(encoding="utf-8"), encoding="utf-8")
text = copy.read_text(encoding="utf-8")

spans = R.masked_spans(text)
starts = R._line_starts(text)
lines = text.split("\n")


def classify(current: str):
    """沿用诊断脚本的分类口径，统计正文标签。"""
    spans = R.masked_spans(current)
    starts = R._line_starts(current)
    lines = current.split("\n")
    result = Counter()
    for match in R.TAG_RE.finditer(current):
        if R._overlaps(match.start(), match.end(), spans):
            continue
        li = R._line_at(starts, match.start())
        col = match.start() - starts[li]
        left = lines[li][col - 1] if col else ""
        end = col + len(match.group(0))
        right = lines[li][end] if end < len(lines[li]) else ""
        content = match.group("content")
        if left in ("'", "’") and len(content) <= 2 and content.isalnum():
            result["撇号后缀"] += 1
        elif re.fullmatch(r"[A-Za-z]+", content) and not left.isalnum() and not right.isalnum():
            result["整词包裹"] += 1
        elif any(ch.isspace() for ch in content):
            result["跨词畸形"] += 1
        elif not any(ch.isalnum() for ch in content):
            result["标点"] += 1
        else:
            result["错位切分/丢字符"] += 1
    return result


plan = R.build_plan(text, pdf)
patches = plan["patches"]
r6 = [p for p in patches if p["rule"] == "R6-lite"]
whole = [p for p in r6 if p["before"].lstrip("<sub><sup>").rstrip("</sub></sup>") and
         R.WHOLE_WORD_RE.fullmatch(re.sub(r"</?(?:sub|sup)>", "", p["before"]))]
apo = [p for p in r6 if "</sub>" in p["before"] and p["before"].startswith(("<sub>s</sub>", "<sub>es</sub>"))]

print("patches", len(patches), "rules", plan["stats"]["rules"])
print("R6-lite", len(r6), "whole-word", len(whole), "apostrophe", len(apo))
print("kept", plan["stats"]["kept_whitelist"], "ai_items", plan["stats"]["ai_items"],
      "ai_packs", plan["stats"]["ai_packs"], "checks", plan["checks"])

fixed = R.apply_patches(text, patches)
before_tags = Counter(m.group("kind").lower() for m in R.TAG_RE.finditer(R.mask_tables(R.split_body(text))[0]))
after_tags = Counter(m.group("kind").lower() for m in R.TAG_RE.finditer(R.mask_tables(R.split_body(fixed))[0]))
print("tags before", dict(before_tags), "after", dict(after_tags))
print("class before", dict(classify(text)))
print("class after", dict(classify(fixed)))
print("lines", plan["stats"]["lines_touched"])

print("\n-- R6-lite examples")
for p in r6[:8]:
    print(f"L{p['line']} [{p['rule']}] {p['before']!r} -> {p['after']!r} | {p['reason']} | page {p['page']}")
print("\n-- R6-lite per line")
for line, count in sorted(Counter(p["line"] for p in r6).items()):
    print(line, count)

# 候选但未修的（整词/撇号形状），用于核对降级去向
print("\n-- candidates rejected")
rej = []
for match in R.TAG_RE.finditer(text):
    if R._overlaps(match.start(), match.end(), spans):
        continue
    li = R._line_at(starts, match.start())
    col = match.start() - starts[li]
    left = lines[li][col - 1] if col else ""
    end = col + len(match.group(0))
    right = lines[li][end] if end < len(lines[li]) else ""
    content = match.group("content")
    shaped = (left in ("'", "’") and len(content) <= 2 and content.isalnum()) or \
             (re.fullmatch(r"[A-Za-z]{2,}", content) and not left.isalnum() and not right.isalnum())
    if shaped and not any(p["line"] == li + 1 and p["start"] == col for p in r6):
        rej.append((li + 1, match.group(0), lines[li][max(0, col - 45):end + 30]))
print(len(rej))
for row in rej:
    print(" L", row[0], row[1], "|", row[2])
