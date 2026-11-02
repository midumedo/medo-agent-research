import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")))
import pdf_repair as R

d = Path(r"d:\workspace\memory\resources\papers\.rivet_scratch\repair-mem0")
payload = json.loads((d / "patches.json").read_text(encoding="utf-8"))
text = Path(payload["md"]).read_text(encoding="utf-8")
fixed = R.apply_patches(text, payload["patches"])
orig = text.split("\n")
new = fixed.split("\n")
for n in (19, 25, 44, 90, 161):
    for needle in ("persist", "efficient", "ffering", "inherently", "ficiency"):
        oi = orig[n - 1].find("<sub") if needle in ("persist",) else -1
    print(f"=== L{n} orig")
    print(orig[n - 1][:260])
    print(f"=== L{n} fixed")
    print(new[n - 1][:260])
    print()
