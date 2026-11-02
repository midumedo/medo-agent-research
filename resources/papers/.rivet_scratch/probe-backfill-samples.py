"""打印指定行的回填试算明细（修正后复跑）。"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")))
import pdf_repair as R

root = Path(r"d:\workspace\memory\resources\papers")
text = (root / "md" / "arxiv-2504.19413v1.Project.Mem0.md").read_text(encoding="utf-8")
result = R.backfill_preview(text, root / "pdf" / "arxiv-2504.19413v1.Project.Mem0.pdf", limit=99)
print(json.dumps(result["stats"], ensure_ascii=False, indent=2))
for item in result["items"]:
    if item["line"] not in (25, 28, 38, 44, 161):
        continue
    print("=" * 30, "L", item["line"], item["status"])
    for seg in item["segments"]:
        print("  span", seg["span"], "score", seg["score"], "status", seg["status"])
        print("  before:", seg["before"][:260])
        print("  sentence:", (seg["sentence"] or "")[:260])
        print("  replace:", seg["replacement"])
        print("  delta:", seg["delta"], "gates", seg["gates"], "intact", seg["intact_kept"],
              "reasons", seg["reasons"])
        if seg.get("orig_span"):
            print("  orig_span", seg["orig_span"], "plain", repr(seg.get("plain_before")))
