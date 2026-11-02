import json
import pathlib

p = pathlib.Path(r"d:\workspace\memory\resources\papers\.rivet_scratch\repair-mem0")
d = json.loads((p / "patches.json").read_text(encoding="utf-8"))
text = pathlib.Path(d["md"]).read_text(encoding="utf-8")
lines = text.split("\n")


def render(number, start, end):
    old = lines[number - 1]
    rows = sorted([q for q in d["patches"] if q["line"] == number], key=lambda q: q["start"])
    parts, cursor = [], start
    for q in rows:
        if q["end"] <= start:
            continue
        if q["start"] >= end:
            break
        parts.append(old[cursor:q["start"]])
        parts.append(q["after"])
        cursor = q["end"]
    parts.append(old[cursor:end])
    return old[start:end], "".join(parts)


cases = [
    ("afoundation → 补空格", 25, "afoundation", -10, 40),
    ("eficienc<sub>y</sub> → efficiency", 157, "eficienc", -20, 40),
    ("graph construction completes", 161, "ra <sup>h</sup>", -20, 180),
    ("行首连续标签", 19, "Lar<sub>g</sub>e", 0, 90),
    ("2<sup>6</sup>% → 26%", 19, "2<sup>6</sup>%", -30, 30),
    ("multi-hop + questions", 128, "mu<sup>l</sup>", -35, 60),
    ("trade-offs", 90, "t<sub>ra</sub>d", -20, 50),
    ("LLM-based", 74, "LLM-<sup>b</sup>", -20, 40),
    ("参考文献作者", 179, "A<sub>n</sub>th", -10, 80),
    ("真上标保留", 122, "Mem0<sup>g</sup>", -25, 60),
]
for label, number, needle, back, ahead in cases:
    old = lines[number - 1]
    i = old.find(needle)
    if i < 0:
        print(f"**[{label}] L{number}: 未找到 {needle!r}**")
        continue
    start, end = max(0, i + back), min(len(old), i + len(needle) + ahead)
    before, after = render(number, start, end)
    print(f"\n**[{label}] L{number}**")
    print("before:", before)
    print("after :", after)
