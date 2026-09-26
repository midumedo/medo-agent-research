#!/usr/bin/env python3
"""生成 domain/repo-context/00docslist/index.csv。

口径见同目录 README.md「index.csv 字段口径」。要点：
- 一行一个根目录文件，不重复 sources/repos/index.csv 已有字段（repo/kind/completeness/snapshot）。
- 收录范围：根目录 *.md + *.i18n.yaml + 治理型非 md（NOTICE / LICENSE.txt / architecture-policy.yaml / marketplace.json）。
  构建与 CI 配置（package.json、tsconfig.json、pnpm-workspace.yaml、.pre-commit-config.yaml、*-lock.* 等）不收。
- bytes 与 L1 哈希都从磁盘现读，不手填；快照刷新后重跑本脚本即可。
- role 是显式映射表（pattern -> D 编号），映射依据 domain/repo-context/02docsdefine/ds.md；
  没有对应 D 编号的一律留空，不猜。
"""
from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4] / "sources" / "repos"
OUT = Path(__file__).resolve().parents[1] / "index.csv"
CHECKED_AT = "2026-09-25"

# 收录：根目录 *.md + *.i18n.yaml + 下列治理型非 md
EXTRA_FILES = {"NOTICE", "LICENSE.txt", "architecture-policy.yaml", "marketplace.json"}

# 语言变体归一：README.zh-CN.md / README_ZH.md / CONTRIBUTING.zh.md 与正本同类
_README = re.compile(r"^README([_.].*)?\.md$")
_LANG = re.compile(r"\.(zh-CN|zh|en|ja|ko|CN|ZH)(?=\.md$)")


def normalize(name: str) -> str:
    if _README.match(name):
        return "README.md"
    return _LANG.sub("", name)


# kind 封闭集（8 值）
KIND_RULES: list[tuple[str, str]] = [
    (r"^(AGENTS|CLAUDE|GEMINI)\.md$", "agent-entry"),
    (r"^README\.md$", "facade"),
    (r"^(LICENSE.*|NOTICE.*|THIRD[-_]PARTY[-_]NOTICES\.md|CITATION\.md|CONTRIBUTORS\.md|CREDITS\.md|ACKNOWLEDGMENTS\.md)$", "legal"),
    (r"^(CONTRIBUTING\.md|CODE_OF_CONDUCT\.md|GOVERNANCE\.md|SECURITY\.md|MAINTAINERS\.md|EXTERNAL-PRS\.md)$", "collab-rule"),
    (r"^(CHANGELOG\.md|RELEASING\.md|RELEASE.*\.md)$", "record"),
    (r"^(CONTEXT\.md|CONTEXT-MAP\.md|DESIGN\.md|star\.md|QUICKSTART\.md)$", "semantic"),
    (r"^(.*\.i18n\.yaml|marketplace\.json|architecture-policy\.yaml|\.rivet\.md)$", "machine"),
    (
        r"^(BENCHMARK\.md|BRAND_GUIDELINES\.md|ERRORS\.md|SDK\.md|LLM\.md|I18N\.md|SAFETY\.md|"
        r"CUSTOM_DISTROS\.md|MERGE_FIXES\.md|RISCV_SETUP\.md|ROADMAP\.md|BUILDING_.*\.md|"
        r"INSTALL-LATEST\.md|SKILL\.md)$",
        "topic-manual",
    ),
]

# role：文件名 -> 02docsdefine 的 D 编号。无对应则留空。
ROLE_RULES: list[tuple[str, str]] = [
    (r"^README\.md$", "D01"),
    (r"^CHANGELOG\.md$", "D02"),
    (r"^(CONTRIBUTING\.md|CODE_OF_CONDUCT\.md)$", "D03"),
    (r"^SECURITY\.md$", "D04"),
    (r"^(RELEASING\.md|RELEASE.*\.md|QUICKSTART\.md|INSTALL-LATEST\.md)$", "D05"),
    (r"^(LICENSE.*|NOTICE.*|THIRD[-_]PARTY[-_]NOTICES\.md|CITATION\.md|CONTRIBUTORS\.md|CREDITS\.md|ACKNOWLEDGMENTS\.md)$", "D06"),
    (r"^AGENTS\.md$", "D09"),
    (r"^(CLAUDE|GEMINI)\.md$", "D10"),
    (r"^SKILL\.md$", "D12"),
    (r"^CONTEXT\.md$", "D14"),
    (r"^CONTEXT-MAP\.md$", "D16"),
    (r"^star\.md$", "D17"),
    (r"^ROADMAP\.md$", "D26"),
    (r"^SAFETY\.md$", "D35"),
    (
        r"^(BENCHMARK\.md|BRAND_GUIDELINES\.md|ERRORS\.md|SDK\.md|LLM\.md|I18N\.md|"
        r"CUSTOM_DISTROS\.md|MERGE_FIXES\.md|RISCV_SETUP\.md|BUILDING_.*\.md)$",
        "D36",
    ),
]


def classify(key: str, rules: list[tuple[str, str]]) -> str:
    for pattern, value in rules:
        if re.match(pattern, key):
            return value
    return ""


def first_line_hash(path: Path) -> str:
    with path.open("rb") as fh:
        raw = fh.readline()
    return hashlib.sha256(raw.rstrip(b"\r\n")).hexdigest()[:8]


def main() -> None:
    rows: list[dict[str, str]] = []
    for repo_dir in sorted(p for p in REPO_ROOT.iterdir() if p.is_dir() and p.name != "_scripts"):
        for path in sorted(p for p in repo_dir.iterdir() if p.is_file()):
            name = path.name
            if not (name.endswith(".md") or name.endswith(".i18n.yaml") or name in EXTRA_FILES):
                continue
            key = normalize(name)
            rows.append(
                {
                    "id": repo_dir.name,
                    "path": name,
                    "kind": classify(key, KIND_RULES),
                    "bytes": str(path.stat().st_size),
                    "role": classify(key, ROLE_RULES),
                    "evidence": f"find;L1={first_line_hash(path)}",
                    "status": "verified",
                    "checked_at": CHECKED_AT,
                }
            )

    # 无本地 checkout 的仓：显式占位，避免被读成「忘了收」
    rows.append(
        {
            "id": "claude-code",
            "path": "",
            "kind": "",
            "bytes": "",
            "role": "",
            "evidence": "no-local-checkout (index.csv completeness=binary; snapshot empty)",
            "status": "absent",
            "checked_at": CHECKED_AT,
        }
    )

    fields = ["id", "path", "kind", "bytes", "role", "evidence", "status", "checked_at"]
    with OUT.open("w", encoding="utf-8", newline="\n") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {OUT} rows={len(rows)}")


if __name__ == "__main__":
    main()
