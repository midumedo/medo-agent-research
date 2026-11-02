import re, sys, json, hashlib
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")))
import pdf_repair as R

cur = Path(r"d:\workspace\memory\resources\papers\md\arxiv-2504.19413v1.Project.Mem0.md").read_text(encoding="utf-8")
bak = Path(r"d:\workspace\memory\resources\papers\.rivet_scratch\backup\20261103T014427-12f3511e6689cd0c-arxiv-2504.19413v1.Project.Mem0.md").read_text(encoding="utf-8")

def spans(text):
    out = {
        "front": [text[:m.end()] for m in [R.FRONT_RE.match(text)] if m],
        "tables": [m.group(0) for m in R.TABLE_RE.finditer(text)],
        "algo": [m.group(0) for m in R.ALGO_RE.finditer(text)],
        "fences": [m.group(0) for m in R.FENCE_RE.finditer(text)],
        "dollars": [m.group(0) for m in R.DOLLAR_BLOCK_RE.finditer(text)],
        "inline": [m.group(0) for m in R.INLINE_DOLLAR_RE.finditer(text)],
        "images": [m.group(0) for m in R.IMAGE_LINE_RE.finditer(text)],
    }
    return out

a, b = spans(bak), spans(cur)
print("lines", bak.count("\n"), cur.count("\n"))
print("bytes", len(bak.encode()), len(cur.encode()), "sha", hashlib.sha256(cur.encode()).hexdigest()[:16])
for key in a:
    same = a[key] == b[key]
    print(f"{key:8s} before={len(a[key])} after={len(b[key])} identical={same}")
    if not same:
        for x, y in zip(a[key], b[key]):
            if x != y:
                print("  first diff:", x[:60], "|", y[:60]); break
print("front matter md5", hashlib.md5(a["front"][0].encode()).hexdigest()[:12],
      hashlib.md5(b["front"][0].encode()).hexdigest()[:12])
