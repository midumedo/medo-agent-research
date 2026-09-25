"""sources/repos/ 账本与抓取脚本的共享库。

两层分工（详见 sources/repos/AGENTS.md）：

  `_commits.json`  抓取事实——机器写。一个目录一条，记上游 slug 与落盘时的提交 sha。
  `index.csv`      研究视图——身份列（`repo`、`snapshot`）派生自 `_commits.json` 与磁盘；
                   判断列（`kind`、`keywords`、`completeness`）由人或模型写定，
                   重建时**永不覆盖**。

所以 `index.csv` 不能手改身份列：改上游就重抓（`fetch.py`），改目录就重跑
`build_index.py`。判断列随手改没关系，重建会保留。

目录名即身份：`<id>/` 就是该仓库当前快照，一个仓库只有一个目录。**不留多版本副本**——
要特定版本就按引用里的上游 sha 用 `fetch.py` 重现，不在本地囤旧树（见 fetch.py 的更新语义）。
"""

import csv
import io
import json
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INDEX_FIELDS = ["id", "repo", "kind", "keywords", "completeness", "snapshot"]
# 重建时从旧行原样搬过来的列——它们是判断，不是可从磁盘推导的事实。
JUDGEMENT_FIELDS = ("kind", "keywords", "completeness")
MULTI_FIELDS = ("keywords",)  # `;` 分隔，与 sources/papers/index.csv 同约定

KINDS = {"harness", "model", "memory", "paper", "docs", "tooling"}
COMPLETENESS = {"source", "source-partial", "binary", "app-only", "docs-only", "unknown"}

# 没有本地快照的行必须在 keywords 里带这个标记。否则「账本里有一行」会被下游误读成
# 「本地有一份可读的代码」——这正是本层要防的错误。
NO_SNAPSHOT = "no-local-snapshot"

# 有本地目录、但落盘时的提交 sha 没能记录（更早轮次抓取时未记指纹，或 API 限流）。
# 空 `snapshot` 必须配这个标记：留空而不说明，下游会以为「sha 就是空」，读不出「没记」。
SNAPSHOT_UNKNOWN = "snapshot-unknown"

# 目录里不是第三方 checkout 的条目：元数据层自身，以及 _commits.json 这类账本文件。
NON_CHECKOUT = {
    ".gitignore", "index.csv", "AGENTS.md", "CHANGELOG.md", "README.md",
    "_commits.json", "_scripts", "__pycache__", "logs", "assets",
}
# 抓取失败留下的残缺目录。它们**不建账本行**，只在 CHANGELOG.md 里记一条事件。
PARTIAL_PREFIX = "_partial-"

_ID_RE = re.compile(r"^([^@]+)(?:@([0-9a-f]{4,40}))?$")


def index_path():
    return os.path.join(BASE, "index.csv")


def commits_path():
    return os.path.join(BASE, "_commits.json")


def scan_dirs():
    """磁盘上真正的第三方 checkout 目录名（不含元数据层与抓取残缺目录）。"""
    if not os.path.isdir(BASE):
        return []
    out = []
    for name in os.listdir(BASE):
        if name in NON_CHECKOUT or name.startswith(PARTIAL_PREFIX):
            continue
        if name.startswith(".") or not os.path.isdir(os.path.join(BASE, name)):
            continue
        out.append(name)
    return sorted(out)


def read_commits():
    """`_commits.json`：`{id: {slug, sha, date, msg}}`；文件不存在时给空字典。"""
    if not os.path.exists(commits_path()):
        return {}
    with open(commits_path(), encoding="utf-8") as f:
        return json.load(f)


def write_commits(data):
    with open(commits_path(), "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def read_index():
    """账本行；`keywords` 取回为列表。"""
    if not os.path.exists(index_path()):
        return []
    with open(index_path(), encoding="utf-8", newline="") as f:
        raw = list(csv.DictReader(f))
    rows = []
    for item in raw:
        row = {key: (item.get(key) or "").strip() for key in INDEX_FIELDS}
        row["keywords"] = [w for w in row["keywords"].split(";") if w]
        rows.append(row)
    return rows


def has_marker(row, marker):
    return marker in (row.get("keywords") or [])


def render_index(rows):
    """写出 `write_index()` 会产生的确切文本，供 `--check` 逐字节比对。"""
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=INDEX_FIELDS, lineterminator="\n")
    writer.writeheader()
    for row in sorted(rows, key=lambda r: r.get("id") or ""):
        out = {key: row.get(key) or "" for key in INDEX_FIELDS}
        out["keywords"] = ";".join(row.get("keywords") or [])
        writer.writerow(out)
    return buf.getvalue()


def write_index(rows):
    with open(index_path(), "w", encoding="utf-8", newline="") as f:
        f.write(render_index(rows))


def find(token):
    """按 `id`／目录名／上游 slug 解析回账本行；找不到返回 None。"""
    token = (token or "").strip()
    if not token:
        return None
    rows = read_index()
    for row in rows:
        if token in (row.get("id"), row.get("repo")):
            return row
    for row in rows:
        if (row.get("repo") or "").split("/")[-1] == token:
            return row
    return None


def validate(rows):
    """返回不合规项的文字描述列表；空列表表示账本自洽。"""
    problems = []
    seen = set()
    for row in rows:
        ident = row.get("id") or ""
        if not ident:
            problems.append("有一行 id 为空")
            continue
        if ident in seen:
            problems.append(f"{ident}: id 重复")
        seen.add(ident)
        kind = row.get("kind") or ""
        if kind and kind not in KINDS:
            problems.append(f"{ident}: kind={kind} 不在封闭集内")
        comp = row.get("completeness") or ""
        if comp and comp not in COMPLETENESS:
            problems.append(f"{ident}: completeness={comp} 不在封闭集内")
        base = ident
        has_dir = ident in scan_dirs()
        if has_dir:
            if not row.get("snapshot") and not has_marker(row, SNAPSHOT_UNKNOWN):
                problems.append(
                    f"{ident}: 有本地目录却没有 snapshot——取不到指纹时要加 `{SNAPSHOT_UNKNOWN}` 标记"
                )
            if has_marker(row, NO_SNAPSHOT):
                problems.append(
                    f"{ident}: 有本地目录却带着 `{NO_SNAPSHOT}` 标记——抓到了就要把这个标记摘掉"
                )
        elif not has_marker(row, NO_SNAPSHOT):
            problems.append(f"{ident}: 没有本地目录，但 keywords 缺 `{NO_SNAPSHOT}` 标记")
    return problems
