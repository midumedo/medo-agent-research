import json
import pathlib
import sys

sys.path.insert(0, r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")
import pdf_repair as R

p = pathlib.Path(r"d:\workspace\memory\resources\papers\.rivet_scratch\repair-mem0")
d = json.loads((p / "patches.json").read_text(encoding="utf-8"))
text = pathlib.Path(d["md"]).read_text(encoding="utf-8")
fixed = R.apply_patches(text, d["patches"])


def show(tag, number, needle):
    old = text.split("\n")[number - 1]
    new = fixed.split("\n")[number - 1]
    i = old.find(needle)
    if i < 0:
        i = 0
    print(f"\n[{tag}] L{number}")
    print("  before:", old[max(0, i - 60):i + 120])
    print("  after :", new[max(0, i - 60):i + 160])


show("afoundation", 25, "afoundation")
show("efficiency", 157, "eficien")
show("ra-h", 161, "ra <sup>h</sup>")
show("opening", 19, "Lar<sub>g</sub>e")
show("reference", 179, "A<sub>n</sub>th")
show("table-free", 108, "")
show("multi-hop", 128, "mu<sup>l</sup>")
show("trade-offs", 90, "t<sub>ra</sub>d")

print("\nAI L161 offsets:", [i for i in d["patches"] if i["line"] == 161][:0])
