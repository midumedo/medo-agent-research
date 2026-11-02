import json
from pathlib import Path

d = Path(r"d:\workspace\memory\resources\papers\.rivet_scratch\repair-mem0")
payload = json.loads((d / "patches.json").read_text(encoding="utf-8"))
patches = payload["patches"]
lines = Path(payload["md"]).read_text(encoding="utf-8").split("\n")

wanted = [
    (19, "<sub>g</sub>"), (19, "2<sup>6</sup>"), (74, "<sup>b</sup>"),
    (157, "propose"), (161, "<sub>e average</sub>"), (161, "grap"),
    (25, "afoundation"), (19, "ofer"), (128, "mu<sup>l</sup>"),
    (25, "<sub>ers</sub>i<sub>s</sub>t"), (32, "i<sub>nsu</sub>"),
]
shown = set()
for line, needle in wanted:
    for p in patches:
        if p["line"] != line:
            continue
        if needle not in lines[line - 1][p["start"]:p["end"] + 1] and needle not in p["before"]:
            continue
        key = (line, p["start"])
        if key in shown:
            continue
        shown.add(key)
        start = max(0, p["start"] - 34)
        stop = p["end"] + 34
        print(f"{p['rule']} L{line} {p['before']!r} -> {p['after']!r}")
        print("   ", lines[line - 1][start:p["start"]] + "【" + p["before"] + "】" + lines[line - 1][p["end"]:stop])
        break
