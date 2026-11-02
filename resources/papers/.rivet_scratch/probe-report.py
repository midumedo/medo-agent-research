import re, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")))
import pdf_repair as R

cur = Path(r"d:\workspace\memory\resources\papers\md\arxiv-2504.19413v1.Project.Mem0.md").read_text(encoding="utf-8")
bak = Path(r"d:\workspace\memory\resources\papers\.rivet_scratch\backup\20261103T014427-12f3511e6689cd0c-arxiv-2504.19413v1.Project.Mem0.md").read_text(encoding="utf-8")
for name, text in (("before", bak), ("after", cur)):
    body = R.split_body(text)
    masked, _ = R.mask_tables(body)
    kinds = Counter(m.group("kind").lower() for m in R.TAG_RE.finditer(masked))
    print(name, dict(kinds), "total", sum(kinds.values()))

# items
pack_dir = Path(r"d:\workspace\memory\resources\papers\.rivet_scratch\repair-mem0\ai-packs")
items = []
for pack in sorted(pack_dir.glob("p*.md")):
    body = pack.read_text(encoding="utf-8")
    for chunk in re.split(r"\n## ", body)[1:]:
        header, _, rest = chunk.partition("\n")
        frag = rest.split("MinerU：`", 1)[1].split("`", 1)[0]
        items.append({"line": int(re.search(r"第 (\d+) 行", header).group(1)), "fragment": frag})

presence = Counter()
for item in items:
    seen = set()
    for m in R.TAG_RE.finditer(item["fragment"]):
        content = m.group("content")
        start = m.start()
        left = item["fragment"][start - 1] if start else ""
        end = start + len(m.group(0))
        right = item["fragment"][end] if end < len(item["fragment"]) else ""
        if left in ("'", "’") and len(content) <= 2 and content.isalnum():
            seen.add("撇号后缀")
        elif re.fullmatch(r"[A-Za-z]+", content) and not left.isalnum() and not right.isalnum():
            seen.add("整词包裹")
        elif any(ch.isspace() for ch in content):
            seen.add("跨词畸形")
        elif not any(ch.isalnum() for ch in content):
            seen.add("标点")
        else:
            seen.add("错位切分/丢字符")
    for key in seen:
        presence[key] += 1
print("items per class", dict(presence), "items", len(items))
print("lines", sorted({i['line'] for i in items}))

idx = R._pdf_index(Path(r"d:\workspace\memory\resources\papers\pdf\arxiv-2504.19413v1.Project.Mem0.pdf"))
print("\n-- excerpts")
for n, needle, width in ((19, "Large Language Models", 320), (25, "Human memory", 520), (161, "Zep", 420), (161, "Mem0", 330)):
    line = cur.split("\n")[n - 1]
    i = line.find(needle)
    print(f"\n[L{n}] {line[max(0, i - 40):i + width]}")
