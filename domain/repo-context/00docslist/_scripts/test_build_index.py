#!/usr/bin/env python3
"""index.csv 不变量检查。

这个账本的全部价值在于「每条断言都能回溯到一次真实取证」。所以本测试不检查
生成逻辑，而是**回到磁盘**核对：脚本写进 CSV 的每个字节数与首行哈希，是否
与当前磁盘上的文件一致。手改过数字、或快照刷新后忘了重跑，都会在这里红。

运行：python -m unittest discover -s domain/repo-context/00docslist/_scripts -p 'test_*.py'
"""
from __future__ import annotations

import csv
import hashlib
import re
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAGE = HERE.parent
INDEX = STAGE / "index.csv"
REPO_ROOT = STAGE.parents[2] / "sources" / "repos"

FIELDS = ["id", "path", "kind", "bytes", "role", "evidence", "status", "checked_at"]
KINDS = {
    "agent-entry", "facade", "legal", "collab-rule",
    "record", "semantic", "topic-manual", "machine", "",
}


def read_rows() -> list[dict[str, str]]:
    with INDEX.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def l1_hash(path: Path) -> str:
    with path.open("rb") as fh:
        return hashlib.sha256(fh.readline().rstrip(b"\r\n")).hexdigest()[:8]


class IndexInvariants(unittest.TestCase):
    def setUp(self) -> None:
        self.rows = read_rows()

    def test_header_matches_documented_fields(self) -> None:
        with INDEX.open(encoding="utf-8", newline="") as fh:
            self.assertEqual(next(csv.reader(fh)), FIELDS)

    def test_covers_every_repo_directory(self) -> None:
        on_disk = {p.name for p in REPO_ROOT.iterdir() if p.is_dir() and p.name != "_scripts"}
        in_ledger = {r["id"] for r in self.rows}
        for missing in sorted(on_disk - in_ledger):
            self.fail(f"仓库目录在账本中缺失：{missing}")
        self.assertIn("claude-code", in_ledger, "无 checkout 的仓应有 absent 占位行")

    def test_exactly_eighteen_repos(self) -> None:
        self.assertEqual(len({r["id"] for r in self.rows}), 18)

    def test_no_duplicate_id_path(self) -> None:
        seen = [(r["id"], r["path"]) for r in self.rows]
        self.assertEqual(len(seen), len(set(seen)))

    def test_verified_rows_are_fully_populated(self) -> None:
        for r in self.rows:
            if r["status"] != "verified":
                continue
            for field in ("path", "kind", "bytes", "evidence", "checked_at"):
                self.assertTrue(r[field], f"{r['id']}/{r['path']} 缺 {field}")

    def test_absent_rows_carry_a_reason(self) -> None:
        for r in self.rows:
            if r["status"] == "absent":
                self.assertTrue(r["evidence"], f"{r['id']} 标 absent 却没说原因")

    def test_bytes_and_l1_hash_match_disk(self) -> None:
        """核心断言：账本里的数字必须能指回磁盘上的真实字节。"""
        for r in self.rows:
            if r["status"] != "verified":
                continue
            path = REPO_ROOT / r["id"] / r["path"]
            self.assertTrue(path.is_file(), f"账本登记了不存在的文件：{r['id']}/{r['path']}")
            self.assertEqual(int(r["bytes"]), path.stat().st_size, f"字节数漂移：{r['id']}/{r['path']}")
            self.assertEqual(r["evidence"], f"find;L1={l1_hash(path)}", f"首行哈希漂移：{r['id']}/{r['path']}")

    def test_kind_is_within_closed_set(self) -> None:
        for r in self.rows:
            self.assertIn(r["kind"], KINDS, f"kind 越界：{r['id']}/{r['path']} = {r['kind']}")

    def test_role_is_a_d_number_or_blank(self) -> None:
        for r in self.rows:
            self.assertTrue(
                r["role"] == "" or re.fullmatch(r"D\d{2}", r["role"]),
                f"role 不是 D 编号：{r['id']}/{r['path']} = {r['role']}",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
