import json
import sys
import time
from pathlib import Path

ROOT = Path(r"d:\workspace\memory")
sys.path.insert(0, str(ROOT / ".agents/skills/pdf-manager/scripts"))
import pdf_repair as R

md = ROOT / "resources/papers/md/arxiv-2504.19413v1.Project.Mem0.md"
pdf = ROOT / "resources/papers/pdf/arxiv-2504.19413v1.Project.Mem0.pdf"
text = md.read_text(encoding="utf-8")

spans = R.masked_spans(text)
masked_chars = sum(e - s for s, e in spans)
print("spans", len(spans), "masked chars", masked_chars, "/", len(text))

t0 = time.perf_counter()
plan = R.build_plan(text, pdf, whitelist=R.DEFAULT_WHITELIST)
elapsed = time.perf_counter() - t0
print("elapsed", round(elapsed, 2))
print("stats", json.dumps(plan["stats"], ensure_ascii=False))
print("checks", plan["checks"])

for line in (25, 157, 161, 19, 21):
    rows = [p for p in plan["patches"] if p["line"] == line]
    print(f"\n=== L{line} patches={len(rows)}")
    for p in rows[:12]:
        print(p["rule"], p["start"], p["end"], repr(p["before"]), "->", repr(p["after"]))

print("\n=== first 10 patches")
for p in plan["patches"][:10]:
    print(p["line"], p["rule"], repr(p["before"]), "->", repr(p["after"]), p["reason"])

print("\n=== AI items", plan["stats"]["ai_items"], "packs", plan["stats"]["ai_packs"])
for item in plan["ai_items"][:6]:
    print("L", item["line"], item["reason"], repr(item["fragment"][:160]))
