import hashlib
import re
from pathlib import Path

md = Path(r"d:\workspace\memory\resources\papers\md\arxiv-2504.19413v1.Project.Mem0.md")
bak = Path(r"d:\workspace\memory\resources\papers\.rivet_scratch\backup\20261103T014427-12f3511e6689cd0c-arxiv-2504.19413v1.Project.Mem0.md")
print("current sha", hashlib.sha256(md.read_bytes()).hexdigest())
print("backup  sha", hashlib.sha256(bak.read_bytes()).hexdigest())
lines = md.read_text(encoding="utf-8").split("\n")
TAG = re.compile(r"</?su[bp]>")


def show(n, start, length):
    line = lines[n - 1]
    i = line.find(start)
    part = line[i:i + length]
    print(f"\n[L{n}] remaining tags in window: {len(TAG.findall(part))}")
    print(part)


show(19, "Large Language Models", 300)
show(25, "Human memory is", 300)
show(161, "In stark contrast", 300)
show(161, "Mem0 encodes complete", 260)
