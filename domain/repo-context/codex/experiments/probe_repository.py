#!/usr/bin/env python3
"""Read-only repo-context measurements; Python standard library only.

The results are byte/structure observations, not LLM performance or token tests.
Run from any directory; --root selects another compatible repository.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import platform
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def fingerprint(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def csv_text(rows: list[dict[str, str]], fields: list[str]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows({key: row[key] for key in fields} for row in rows)
    return stream.getvalue()


def measurements(text: str) -> dict[str, int]:
    return {"utf8_bytes": len(text.encode("utf-8")), "unicode_codepoints": len(text),
            "physical_lines": len(text.splitlines())}


def quoted_csv_case() -> dict:
    rows = [{"id": "x", "note": 'comma, quote " and\nsecond line', "scope": "local"}]
    text = csv_text(rows, ["id", "note", "scope"])
    parsed = list(csv.DictReader(io.StringIO(text, newline="")))
    assert parsed == rows
    naive_fields = text.splitlines()[1].split(",")
    assert naive_fields != [rows[0][key] for key in ["id", "note", "scope"]]
    return {"input_csv": text, "expected_records": rows, "csv_round_trip": True,
            "naive_first_physical_line_fields": naive_fields,
            "interpretation": "Physical lines and comma splitting are not general CSV records/fields."}


def probe(root: Path) -> dict:
    ledger_path = root / "domain/repo-context/00docslist/index.csv"
    index_path = root / "sources/repos/index.csv"
    commits_path = root / "sources/repos/_commits.json"
    ledger = read_csv(ledger_path)
    repos = read_csv(index_path)
    commits = json.loads(commits_path.read_text(encoding="utf-8-sig"))
    fields = list(ledger[0])
    selected = [row for row in ledger if row["kind"] == "agent-entry" and row["status"] == "verified"]
    projected_fields = ["id", "path"]
    projected = [{field: row[field] for field in projected_fields} for row in selected]
    full = csv_text(ledger, fields)
    filtered = csv_text(selected, fields)
    projected_csv = csv_text(projected, projected_fields)
    assert list(csv.DictReader(io.StringIO(full, newline=""))) == ledger
    assert list(csv.DictReader(io.StringIO(projected_csv, newline=""))) == projected
    # This sample has no Markdown metacharacters; refuse a lossy format comparison.
    assert all(not any(char in value for char in "|\n\r") for row in projected for value in row.values())
    markdown = "| id | path |\n| --- | --- |\n" + "".join(
        f"| {row['id']} | {row['path']} |\n" for row in projected)
    compact_json = json.dumps(projected, ensure_ascii=False, separators=(",", ":")) + "\n"
    jsonl = "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in projected)
    assert json.loads(compact_json) == projected
    assert [json.loads(line) for line in jsonl.splitlines()] == projected
    versions = []
    for row in repos:
        entry = commits.get(row["id"], {})
        sha = entry.get("sha", "")
        recorded = row.get("snapshot", "")
        if sha and recorded and not sha.startswith(recorded):
            versions.append({"id": row["id"], "index_snapshot": recorded, "capture_sha": sha})
    file_checks = []
    for row in ledger:
        if row["status"] != "verified":
            continue
        path = root / "sources/repos" / row["id"] / row["path"]
        exists = path.is_file()
        actual = path.stat().st_size if exists else None
        expected = int(row["bytes"])
        file_checks.append({"id": row["id"], "path": row["path"], "exists": exists,
                            "recorded_bytes": expected, "actual_bytes": actual,
                            "bytes_match": actual == expected,
                            "sha256": fingerprint(path) if exists else None})
    git_head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True,
                              capture_output=True, text=True).stdout.strip()
    return {
        "schema": "repo-context-local-probe-v1",
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_head_at_measurement": git_head,
        "python": platform.python_version(),
        "scope": "Local ledger rows and bytes, not representative repositories or model behavior.",
        "inputs": [{"path": str(path.relative_to(root)).replace("\\", "/"),
                    "sha256": fingerprint(path)} for path in [ledger_path, index_path, commits_path]],
        "ledger": {"rows": len(ledger), "repository_ids": len({row['id'] for row in ledger}),
                   "status_counts": dict(Counter(row["status"] for row in ledger)),
                   "kind_counts": dict(Counter(row["kind"] for row in ledger))},
        "projection": {"predicate": "kind == agent-entry and status == verified",
                       "selected_records": projected, "selected_rows": len(selected),
                       "full_csv": measurements(full), "filtered_csv": measurements(filtered),
                       "projected_csv": measurements(projected_csv)},
        "same_content_formats": {name: measurements(value) for name, value in {
            "csv": projected_csv, "markdown_table": markdown,
            "compact_json_array": compact_json, "jsonl": jsonl}.items()},
        "version_metadata_mismatches": versions,
        "file_checks": file_checks,
        "quoted_csv_fixture": quoted_csv_case(),
        "unit_fixture": {"ascii_1000": measurements("a" * 1000),
                         "chinese_1000": measurements("中" * 1000)},
        "not_measured": ["token_count", "API_cost", "latency", "model_correctness", "upstream_HEAD"]
    }


def render(result: dict) -> str:
    projection = result["projection"]
    lines = ["# 本地测量结果", "", f"> Codex / GPT-6 · 观测时间（UTC）：{result['observed_at_utc']} · 由 probe_repository.py 生成。",
             "", "这是本地文件/字节观测，不是 Agent 效果实验。完整输入指纹和逐文件结果见同名 JSON。", "",
             f"- 输入基线 Git：`{result['git_head_at_measurement']}`",
             f"- Python：`{result['python']}`",
             f"- 账本：{result['ledger']['rows']} 条数据、{result['ledger']['repository_ids']} 个仓库 ID。",
             f"- 状态分布：`{json.dumps(result['ledger']['status_counts'], ensure_ascii=False)}`", "",
             "## 查询减少输出的两个步骤", "",
             "筛选条件：`kind == agent-entry and status == verified`；投影字段：`id,path`。",
             "序列化统一采用 UTF-8、LF、有表头的 CSV；数值不等于原文件物理大小。", "",
             "| 输出 | 行记录数 | UTF-8 字节 |", "| --- | ---: | ---: |",
             f"| 全账本 | {result['ledger']['rows']} | {projection['full_csv']['utf8_bytes']} |",
             f"| 仅筛选 | {projection['selected_rows']} | {projection['filtered_csv']['utf8_bytes']} |",
             f"| 筛选后投影 | {projection['selected_rows']} | {projection['projected_csv']['utf8_bytes']} |", "",
             "## 相同记录与字段的不同表示", "",
             "这里的记录已无多行、竖线等 Markdown 特殊值；没有把该结果推广到嵌套文本或模型理解。", "",
             "| 表示 | UTF-8 字节 | Unicode 码点 | 物理行 |", "| --- | ---: | ---: | ---: |"]
    for name, values in result["same_content_formats"].items():
        lines.append(f"| {name} | {values['utf8_bytes']} | {values['unicode_codepoints']} | {values['physical_lines']} |")
    lines.extend(["", "## 来源账本冲突", "",
                  "此处只比较两个本地元数据文件；任何一方都不自动证明磁盘源码与该提交一致。", "",
                  "| 对象 | index.csv snapshot | _commits.json sha |", "| --- | --- | --- |"])
    for item in result["version_metadata_mismatches"]:
        lines.append(f"| {item['id']} | `{item['index_snapshot']}` | `{item['capture_sha']}` |")
    missing = [item for item in result["file_checks"] if not item["exists"]]
    changed = [item for item in result["file_checks"] if item["exists"] and not item["bytes_match"]]
    lines.extend(["", f"逐文件复核：{len(result['file_checks'])} 条 verified 记录中，缺文件 {len(missing)} 条、字节数不同 {len(changed)} 条。",
                  "字节相同不能证明内容相同；JSON 另存本次全文件 SHA-256。", "",
                  "## 两个构造反例", "",
                  "CSV 中包含逗号、引号和换行时，标准库解析往返成功，按逗号与物理行切分不能恢复原记录。",
                  "同为 1000 个 Unicode 码点，ASCII 示例占 1000 UTF-8 字节，中文示例占 3000 字节。",
                  "这些是脚本实际执行的确定性示例；不代表任何客户端的具体截断结果，也不是 token 测量。", "",
                  "## 解释边界", "",
                  "已观测：查询可以减少需要输出的行与列；这推翻了“没有专用列投影工具就一定要全文读表”的绝对命题。",
                  "尚未知：Agent 能否自行选对查询、工具包装后的总输入、重复读取、缓存费用和任务正确率。",
                  "没有安装 tokenizer 或调用付费模型；字节不能换算成可靠 token 或费用。", ""])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[4])
    parser.add_argument("--output", type=Path, required=True,
                        help="New output prefix, e.g. experiments/results/2026-09-26")
    args = parser.parse_args()
    result = probe(args.root.resolve())
    outputs = [args.output.with_suffix(".json"), args.output.with_suffix(".md")]
    if any(path.exists() for path in outputs):
        parser.error("Output exists; use a new prefix to preserve prior observations.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    outputs[0].write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    outputs[1].write_text(render(result), encoding="utf-8")
    print(json.dumps({"outputs": [str(path) for path in outputs],
                      "rows": result["ledger"]["rows"],
                      "metadata_mismatches": len(result["version_metadata_mismatches"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
