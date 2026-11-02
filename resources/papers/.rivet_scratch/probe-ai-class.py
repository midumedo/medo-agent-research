import re, sys
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")))
import pdf_repair as R

md = Path(r"d:\workspace\memory\resources\papers\md\arxiv-2504.19413v1.Project.Mem0.md").read_text(encoding="utf-8")
spans = R.masked_spans(md)
starts = R._line_starts(md)
lines = md.split("\n")

tags = Counter()
tag_class = Counter()
samples = defaultdict(list)
for match in R.TAG_RE.finditer(md):
    if R._overlaps(match.start(), match.end(), spans):
        continue
    li = R._line_at(starts, match.start())
    col = match.start() - starts[li]
    left = lines[li][col - 1] if col else ""
    end = col + len(match.group(0))
    right = lines[li][end] if end < len(lines[li]) else ""
    content = match.group("content")
    tags[match.group("kind").lower()] += 1
    if left in ("'", "’") and len(content) <= 2 and content.isalnum():
        cls = "撇号后缀"
    elif re.fullmatch(r"[A-Za-z]+", content) and not left.isalnum() and not right.isalnum():
        cls = "整词包裹"
    elif any(ch.isspace() for ch in content):
        cls = "跨词畸形"
    elif any(not ch.isalnum() for ch in content) and not any(ch.isalpha() for ch in content):
        cls = "标点"
    else:
        cls = "错位切分/丢字符"
    tag_class[cls] += 1
    samples[cls].append((li + 1, lines[li][max(0, col - 45):end + 45]))

print("tags", dict(tags), "total", sum(tags.values()))
print("classes", dict(tag_class), "sum", sum(tag_class.values()))

# item-level: parse packs
pack_dir = Path(r"d:\workspace\memory\resources\papers\.rivet_scratch\repair-mem0\ai-packs")
items = []
for pack in sorted(pack_dir.glob("p*.md")):
    body = pack.read_text(encoding="utf-8")
    for chunk in re.split(r"\n## ", body)[1:]:
        header, _, rest = chunk.partition("\n")
        number = int(header.split(".")[0])
        frag = rest.split("MinerU：`", 1)[1].split("`", 1)[0] if "MinerU：`" in rest else rest
        items.append({"pack": pack.name, "n": number, "line": int(re.search(r"第 (\d+) 行", header).group(1)),
                      "fragment": frag})
print("items", len(items))

item_class = Counter()
for item in items:
    counts = Counter()
    for m in R.TAG_RE.finditer(item["fragment"]):
        content = m.group("content")
        cstart = m.start()
        left = item["fragment"][cstart - 1] if cstart else ""
        cend = cstart + len(m.group(0))
        right = item["fragment"][cend] if cend < len(item["fragment"]) else ""
        if left in ("'", "’") and len(content) <= 2 and content.isalnum():
            counts["撇号后缀"] += 1
        elif re.fullmatch(r"[A-Za-z]+", content) and not left.isalnum() and not right.isalnum():
            counts["整词包裹"] += 1
        elif any(ch.isspace() for ch in content):
            counts["跨词畸形"] += 1
        elif any(not ch.isalnum() for ch in content) and not any(ch.isalpha() for ch in content):
            counts["标点"] += 1
        else:
            counts["错位切分/丢字符"] += 1
    item["counts"] = dict(counts)
    item_class[max(counts, key=counts.get)] += 1
print("item dominant", dict(item_class))
for cls, chunk in samples.items():
    print("\n###", cls, tag_class[cls])
    for x in chunk[:4]:
        print(" L", x[0], "|", x[1])
print("\n### item samples 撇号后缀")
for item in items:
    if item["counts"].get("撇号后缀"):
        print(" p", item["pack"], "L", item["line"], "|", item["fragment"][:160])
        break
