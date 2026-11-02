import json
from pathlib import Path

d = Path(r"d:\workspace\memory\resources\papers\.rivet_scratch\repair-mem0")
payload = json.loads((d / "patches.json").read_text(encoding="utf-8"))
patches = payload["patches"]
lines = Path(payload["md"]).read_text(encoding="utf-8").split("\n")

targets = ["afoundation", "ra <sup>h</sup>", "construct<sup>i</sup>on", "graph construction",
           "eficienc", "Lar<sub>g</sub>", "2<sup>6</sup>", "LLM-<sup>b</sup>", "multi-hop"]
seen = set()
for needle in targets:
    for p in patches:
        if needle in p["before"] or needle in p["after"] or needle in lines[p["line"] - 1]:
            key = (p["line"], p["start"])
            if key in seen:
                continue
            seen.add(key)
            span = lines[p["line"] - 1][max(0, p["start"] - 30): p["end"] + 30]
            print(f"{p['rule']} L{p['line']} [{p['start']}..{p['end']}] before={p['before']!r} after={p['after']!r}")
            print(f"   ctx: {span}")
            break

print("\nR5 samples")
for p in [x for x in patches if x["rule"] == "R5"][:8]:
    print(f"L{p['line']} {p['before']!r} -> {p['after']!r} | {p['reason']}")

print("\nR4 samples")
for p in [x for x in patches if x["rule"] == "R4"][:5]:
    print(f"L{p['line']} {p['before']!r} -> {p['after']!r}")

print("\nline counts")
from collections import Counter
print(Counter(p["rule"] for p in patches))
print("patches per line max", max(Counter(p["line"] for p in patches).values()))

print("\npack head")
pack = (d / "ai-packs" / "p01.md").read_text(encoding="utf-8")
print(pack[:900])
