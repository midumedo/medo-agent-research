"""应用后四项断言 + 残留构成，对照 R6-lite 之前的备份。"""
import re, sys, hashlib
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")))
import pdf_repair as R

root = Path(r"d:\workspace\memory\resources\papers")
cur_path = root / "md" / "arxiv-2504.19413v1.Project.Mem0.md"
bak_path = root / ".rivet_scratch" / "backup" / "20261103T020351-c850b545d197146f-arxiv-2504.19413v1.Project.Mem0.md"
pdf = root / "pdf" / "arxiv-2504.19413v1.Project.Mem0.pdf"
cur = cur_path.read_text(encoding="utf-8")
bak = bak_path.read_text(encoding="utf-8")

before_q = R.audit_body(R.split_body(bak))
after_q = R.audit_body(R.split_body(cur))
residual = R.build_plan(cur, pdf)
verdicts = {
    "line_count": bak.count("\n") == cur.count("\n"),
    "protected_sha": R._protected_digest(bak) == R._protected_digest(cur),
    "whitelist_preserved": before_q["true_sup_count"] == after_q["true_sup_count"],
    "idempotent": not residual["patches"],
}
print("checks", verdicts)
print("lines", bak.count("\n"), "->", cur.count("\n"))
print("bytes", len(bak.encode()), "->", len(cur.encode()))
print("sha256", hashlib.sha256(cur.encode()).hexdigest())
print("tags", before_q["tags"], "->", after_q["tags"])
print("true_sup", before_q["true_sup_count"], "->", after_q["true_sup_count"],
      [x["text"] for x in after_q["true_sups"]])
print("density", before_q["density"], "->", after_q["density"])
print("ai_items now", len(residual["ai_items"]), "packs", len(residual["ai_packs"]))


def classify(current):
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


print("class before", dict(classify(bak)))
print("class after", dict(classify(cur)))
print("protected objects")
for name, pattern in (("tables", R.TABLE_RE), ("algo", R.ALGO_RE), ("fences", R.FENCE_RE),
                      ("dollar", R.DOLLAR_BLOCK_RE), ("inline", R.INLINE_DOLLAR_RE),
                      ("images", R.IMAGE_LINE_RE)):
    a = [m.group(0) for m in pattern.finditer(bak)]
    b = [m.group(0) for m in pattern.finditer(cur)]
    print(f"  {name:7s} {len(a)} -> {len(b)} identical={a == b}")
front_a = bak[:R.FRONT_RE.match(bak).end()]
front_b = cur[:R.FRONT_RE.match(cur).end()]
print("front matter identical", front_a == front_b,
      hashlib.md5(front_a.encode()).hexdigest()[:12], hashlib.md5(front_b.encode()).hexdigest()[:12])

for needle in ("Large Language Models", "memory representations", "if slight", "model’s ability"):
    idx = cur.find(needle)
    print("\n[{}]".format(needle), cur[max(0, idx - 60):idx + len(needle) + 60].replace("\n", " / ") if idx >= 0 else "NOT FOUND")
