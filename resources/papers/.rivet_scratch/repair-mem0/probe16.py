import json
import pathlib

p = pathlib.Path(r"d:\workspace\memory\resources\papers\.rivet_scratch\repair-mem0")
payload = json.loads((p / "patches.json").read_text(encoding="utf-8"))
md = pathlib.Path(payload["md"])
text = md.read_text(encoding="utf-8")
lines = text.split("\n")

names = [
    ("afoundation", 25), ("efficiency", 157), ("construction", 161),
    ("numbers", 19), ("reference", 179), ("appendix", 373),
]
for label, number in names:
    rows = [q for q in payload["patches"] if q["line"] == number]
    print(f"\n== {label} L{number} patches={len(rows)}")
    for q in rows[:4]:
        print(" ", q["rule"], q["start"], q["end"], repr(q["before"]), "->", repr(q["after"]), q["page"])

print("\nR5 all:")
for q in payload["patches"]:
    if q["rule"] == "R5":
        print(" L", q["line"], repr(q["before"]), "->", repr(q["after"]))

print("\nAI item for L161:")
for item in payload["patches"]:
    pass
import re
pack = (p / "ai-packs").glob("*.md")
for path in sorted(pack):
    content = path.read_text(encoding="utf-8")
    if "第 161 行" in content:
        print(path.name)
        idx = content.find("## 第 161 行")
        print(content[idx:idx + 500])
