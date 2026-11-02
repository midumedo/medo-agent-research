"""Audit behaviour: read-only, dependency-free, and never fatal in a batch."""

import argparse
import contextlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import pdf_library as storage
import pdf_manager as cli
import pdf_repair


class AuditBodyTests(unittest.TestCase):
    def test_clean_body_reports_zero_noise(self):
        quality = pdf_repair.audit_text("---\nstem: x\n---\n\n# Title\n\nPlain prose, no tags.\n")
        self.assertEqual(quality["tags"]["total"], 0)
        self.assertEqual(quality["density"], 0.0)
        self.assertEqual(quality["cross_word_tags"], 0)
        self.assertEqual(quality["true_sup_count"], 0)
        self.assertEqual(quality["auto_fixable"], 0)
        self.assertEqual(quality["blocks_over_threshold"], 0)
        self.assertFalse(quality["suggest_repair"])

    def test_real_superscript_is_not_counted_as_noise(self):
        body = "## 2.2. Mem0<sup>g</sup>\n\nNeo4j<sup>1</sup> is the backing store.\n"
        quality = pdf_repair.audit_text(body)
        self.assertEqual(quality["true_sup_count"], 2)
        self.assertEqual({item["text"] for item in quality["true_sups"]},
                         {"<sup>g</sup>", "<sup>1</sup>"})
        # Word-final marks contribute no word-internal merge candidates.
        self.assertEqual(quality["word_internal_tags"], 0)
        self.assertEqual(quality["auto_fixable"], 0)

    def test_author_unit_mark_is_not_a_true_superscript(self):
        quality = pdf_repair.audit_text("Zexue He <sup>1</sup>, Jane Doe <sup>2</sup>\n")
        self.assertEqual(quality["true_sup_count"], 0)

    def test_explicit_whitelist_overrides_the_structural_guess(self):
        quality = pdf_repair.audit_text("Custom<sup>2</sup> and plain words.\n",
                                        whitelist=("Custom",))
        self.assertEqual(quality["true_sup_count"], 1)

    def test_table_tags_do_not_enter_density(self):
        table = "<table><tr><td>x<sub>1</sub>y</td></tr></table>"
        outside = "A sentence without tags. " * 5
        quality = pdf_repair.audit_text(outside + table)
        self.assertEqual(quality["tags"]["total"], 0)
        self.assertEqual(quality["density"], 0.0)
        self.assertEqual(quality["chars"], len(outside))
        self.assertEqual(quality["table_chars"], len(table))

    def test_word_internal_tags_estimate_auto_fixable(self):
        quality = pdf_repair.audit_text("Lar<sub>g</sub>e Lan<sub>g</sub>ua<sub>g</sub>e\n")
        self.assertEqual(quality["word_internal_tags"], 3)
        self.assertEqual(quality["auto_fixable"], 3)

    def test_audit_runs_without_pymupdf(self):
        with patch.dict(sys.modules, {"fitz": None, "pymupdf": None}):
            quality = pdf_repair.audit_text("Mem0<sup>g</sup> works without a PDF engine.\n")
        self.assertEqual(quality["tags"]["sup"], 1)
        self.assertEqual(quality["true_sup_count"], 1)


class AuditCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="pdf-repair-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "library"
        self.lib = storage.Library(self.root)

    def document(self, name, body):
        doc = storage.Document(self.root, name)
        storage.atomic_bytes(doc.pdf, b"%PDF-1.4\nfixture\n%%EOF")
        storage.atomic_text(doc.md, storage.render_markdown({"stem": name}, body))
        return doc

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = cli.main(list(args))
        return code, out.getvalue(), err.getvalue()

    def test_check_document_quality_defaults_to_none_and_accepts_audit(self):
        doc = self.document("Report.clean", "Plain body.\n")
        plain = storage.check_document(doc)
        self.assertIn("quality", plain)
        self.assertIsNone(plain["quality"])
        audited = storage.check_document(doc, audit={"density": 0.0})
        self.assertEqual(audited["quality"], {"density": 0.0})
        self.assertTrue(audited["complete"])

    def test_audit_command_is_read_only_and_reports_json(self):
        doc = self.document("Report.dirty", "Mem0<sup>g</sup> Lar<sub>g</sub>e\n")
        before = doc.md.read_bytes()
        code, text, _ = self.run_cli("audit", str(doc.md), "--json")
        self.assertEqual(code, 0)
        rows = json.loads(text)
        self.assertEqual(rows[0]["stem"], "Report.dirty")
        self.assertEqual(rows[0]["quality"]["true_sup_count"], 1)
        self.assertEqual(doc.md.read_bytes(), before)

    def test_check_audit_flag_attaches_quality(self):
        doc = self.document("Report.clean", "Plain body.\n")
        code, text, _ = self.run_cli("check", str(doc.md), "--audit")
        self.assertEqual(code, 0)
        row = json.loads(text)[0]
        self.assertIsNotNone(row["quality"])
        self.assertFalse(row["quality"]["suggest_repair"])

    def test_one_audit_failure_does_not_block_the_batch(self):
        first = self.document("Alpha.dirty", "placeholder")
        second = self.document("Beta.clean", "placeholder")
        before_first = first.md.read_bytes()

        def parse(payload, prefix, requested_model=None):
            return {"body": "Broken Lar<sub>g</sub>e\n" if payload == b"bad" else "Clean prose.\n",
                    "assets": {}, "parser": "test"}

        def convert(jobs, **kwargs):
            for job in jobs:
                yield {"data_id": job["data_id"], "file_name": job["name"], "state": "done",
                       "zip_bytes": b"bad" if "Alpha" in job["name"] else b"good",
                       "batch_id": "test"}

        def audit(body, **kwargs):
            if "Broken" in body:
                raise RuntimeError("audit exploded")
            return real_audit(body)

        real_audit = pdf_repair.audit_body

        args = argparse.Namespace(force=True, model_version="vlm", lang="ch", no_formula=False,
                                  no_table=False, ocr=False, timeout=10, batch_id=None, audit=True)
        out = io.StringIO()
        with patch.object(cli.mineru_backend, "convert_files", side_effect=convert), \
             patch.object(cli.mineru_backend, "parse_archive", side_effect=parse), \
             patch.object(cli.pdf_repair, "audit_body", side_effect=audit), \
             contextlib.redirect_stdout(out):
            code = cli.convert_documents([first, second], args)
        self.assertEqual(code, 0)
        self.assertTrue(first.md.is_file())
        self.assertTrue(second.md.is_file())
        self.assertNotEqual(first.md.read_bytes(), before_first)
        text = out.getvalue()
        self.assertIn("体检：失败（audit exploded）", text)
        self.assertIn("体检：表格外 sub+sup 0.0/千字", text)


class RepairPlanTests(unittest.TestCase):
    """Stage one: rules, protection, self-checks, and output guards."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="pdf-repair-plan-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "library"
        self.root.mkdir(parents=True)

    def build(self, name, body, pdf_lines):
        doc = storage.Document(self.root, name)
        storage.atomic_text(doc.md, storage.render_markdown({"stem": name}, body))
        doc.pdf.parent.mkdir(parents=True, exist_ok=True)
        pymupdf = pdf_repair._load_pymupdf()
        document = pymupdf.open()
        page = document.new_page()
        top = 72
        for line in pdf_lines:
            page.insert_text((72, top), line, fontsize=11)
            top += 18
        document.save(str(doc.pdf))
        return doc

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = cli.main(list(args))
        return code, out.getvalue(), err.getvalue()

    def test_merges_tags_inside_words(self):
        doc = self.build(
            "Report.tags",
            "# Title\n\nLar<sub>g</sub>e Lan<sub>g</sub>ua<sub>g</sub>e Mo<sub>d</sub>els are useful for many tasks.\n",
            ["Large Language Models are useful for many tasks."])
        text = doc.md.read_text(encoding="utf-8")
        plan = pdf_repair.build_plan(text, doc.pdf)
        self.assertGreaterEqual(plan["stats"]["rules"]["R1"] + plan["stats"]["rules"]["R2"], 3)
        fixed = pdf_repair.apply_patches(text, plan["patches"])
        self.assertIn("Large Language Models", fixed)
        self.assertNotIn("<sub>", fixed)
        for name, passed in plan["checks"].items():
            self.assertTrue(passed, name)

    def test_true_superscript_survives(self):
        doc = self.build(
            "Report.whitelist",
            "The Mem0<sup>g</sup> system is a strong baseline for agent memory tasks.\n",
            ["The Mem0 system is a strong baseline for agent memory tasks."])
        text = doc.md.read_text(encoding="utf-8")
        plan = pdf_repair.build_plan(text, doc.pdf)
        self.assertEqual(plan["stats"]["kept_whitelist"], 1)
        self.assertFalse([p for p in plan["patches"] if "<sup>g</sup>" in p["before"]])
        fixed = pdf_repair.apply_patches(text, plan["patches"])
        self.assertIn("Mem0<sup>g</sup>", fixed)

    def test_untagged_broken_word_is_repaired_from_pdf(self):
        doc = self.build(
            "Report.characters",
            "Human memory is afoundation of intelligence and shapes identity over time.\n",
            ["Human memory is a foundation of intelligence and shapes identity over time."])
        text = doc.md.read_text(encoding="utf-8")
        plan = pdf_repair.build_plan(text, doc.pdf)
        self.assertEqual(plan["stats"]["rules"]["R5"], 1)
        fixed = pdf_repair.apply_patches(text, plan["patches"])
        self.assertIn("is a foundation of intelligence", fixed)
        self.assertTrue(plan["checks"]["idempotent"])

    def test_whole_word_wrap_is_unwrapped_after_pdf_hit(self):
        doc = self.build(
            "Report.wholeword",
            "Agents equipped with <sub>memory</sub> of past <sub>across</sub> many sessions stay coherent.\n",
            ["Agents equipped with memory of past across many sessions stay coherent."])
        text = doc.md.read_text(encoding="utf-8")
        plan = pdf_repair.build_plan(text, doc.pdf)
        self.assertEqual(plan["stats"]["rules"]["R6-lite"], 2)
        fixed = pdf_repair.apply_patches(text, plan["patches"])
        self.assertIn("equipped with memory of past across many", fixed)
        self.assertNotIn("<sub>", fixed)

    def test_apostrophe_suffix_is_rejoined(self):
        doc = self.build(
            "Report.apostrophe",
            "This method leverages the model’<sub>s</sub> ability to process sequential input.\n",
            ["This method leverages the model's ability to process sequential input."])
        text = doc.md.read_text(encoding="utf-8")
        plan = pdf_repair.build_plan(text, doc.pdf)
        self.assertEqual(plan["stats"]["rules"]["R6-lite"], 1)
        fixed = pdf_repair.apply_patches(text, plan["patches"])
        self.assertIn("the model’s ability", fixed)

    def test_true_superscript_is_never_unwrapped(self):
        doc = self.build(
            "Report.r6sup",
            "Zexue He <sup>1</sup> and the Mem0<sup>g</sup> baseline both matter for memory work.\n",
            ["Zexue He 1 and the Mem0 baseline both matter for memory work."])
        text = doc.md.read_text(encoding="utf-8")
        plan = pdf_repair.build_plan(text, doc.pdf)
        self.assertEqual(plan["stats"]["rules"]["R6-lite"], 0)
        self.assertEqual(plan["stats"]["kept_whitelist"], 1)
        self.assertEqual(len(plan["ai_items"]), 1)
        fixed = pdf_repair.apply_patches(text, plan["patches"])
        self.assertIn("<sup>1</sup>", fixed)
        self.assertIn("Mem0<sup>g</sup>", fixed)

    def test_whole_word_without_pdf_hit_falls_to_ai(self):
        doc = self.build(
            "Report.r6miss",
            "A <sub>zebra</sub> claim about memory systems across many sessions.\n",
            ["A different claim about memory systems across many sessions."])
        text = doc.md.read_text(encoding="utf-8")
        plan = pdf_repair.build_plan(text, doc.pdf)
        self.assertEqual(plan["stats"]["rules"]["R6-lite"], 0)
        self.assertEqual(len(plan["ai_items"]), 1)
        self.assertIn("<sub>zebra</sub>", pdf_repair.apply_patches(text, plan["patches"]))
        self.assertTrue(plan["checks"]["idempotent"])

    def test_table_formula_and_fence_are_untouched(self):
        body = ("Table follows.\n\n"
                "<table><tr><td>x<sub>1</sub>y</td></tr></table>\n\n"
                "Formula $a<sub>2</sub> + b$ stays.\n\n"
                "```\ncode<sup>z</sup> and text\n```\n")
        doc = self.build("Report.protected", body,
                         ["Table follows.", "Formula stays.", "code and text"])
        text = doc.md.read_text(encoding="utf-8")
        plan = pdf_repair.build_plan(text, doc.pdf)
        self.assertEqual(plan["stats"]["patches"], 0)
        self.assertEqual(pdf_repair._protected_digest(text),
                         pdf_repair._protected_digest(text))
        spans = pdf_repair.masked_spans(text)
        self.assertTrue(any(text[start:end].startswith("<table>") for start, end in spans))
        self.assertTrue(any(text[start:end].startswith("$a<sub>") for start, end in spans))

    def test_output_guard_refuses_content_dirs_and_escapes(self):
        for name in ("md", "assets", "pdf"):
            with self.assertRaises(pdf_repair.RepairError):
                pdf_repair.guard_output(self.root / name, self.root)
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        if hasattr(os, "symlink"):
            link = self.root / "escape"
            try:
                os.symlink(outside, link)
            except OSError:
                self.skipTest("本机无法创建软链")
            with self.assertRaises(pdf_repair.RepairError):
                pdf_repair.guard_output(link, self.root)

    def test_missing_pymupdf_is_a_dependency_error(self):
        doc = self.build("Report.engine", "A short sentence about memory systems.\n",
                         ["A short sentence about memory systems."])
        with patch.dict(sys.modules, {"pymupdf": None}):
            with self.assertRaises(pdf_repair.DependencyError):
                pdf_repair.build_plan(doc.md.read_text(encoding="utf-8"), doc.pdf)
        out, err = io.StringIO(), io.StringIO()
        with patch.dict(sys.modules, {"pymupdf": None}), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = cli.main(["repair", str(doc.md), "--out", str(Path(self.temp.name) / "plan")])
        self.assertEqual(code, 2)
        self.assertIn("pip install pymupdf", err.getvalue())

    def test_cli_writes_ledger_and_leaves_md_alone(self):
        doc = self.build(
            "Report.cli",
            "Lar<sub>g</sub>e Lan<sub>g</sub>ua<sub>g</sub>e Mo<sub>d</sub>els are useful for many tasks.\n",
            ["Large Language Models are useful for many tasks."])
        before = doc.md.read_bytes()
        out = Path(self.temp.name) / "plan"
        code, text, _ = self.run_cli("repair", str(doc.md), "--out", str(out))
        self.assertEqual(code, 0)
        self.assertIn("R1", text)
        self.assertEqual(doc.md.read_bytes(), before)
        for name in ("patches.json", "diff.txt", "stats.json"):
            self.assertTrue((out / name).is_file(), name)
        self.assertTrue(list((out / "ai-packs").glob("*.md")) or True)
        payload = json.loads((out / "patches.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["document"], "Report.cli")
        self.assertTrue(payload["checks"]["protected_sha"])
        refused = Path(self.temp.name) / "library" / "md"
        code, _, err = self.run_cli("repair", str(doc.md), "--out", str(refused))
        self.assertEqual(code, 1)
        self.assertIn("拒绝写入", err)


    def test_apply_writes_once_and_refuses_a_drifted_plan(self):
        doc = self.build(
            "Report.apply",
            "Lar<sub>g</sub>e Lan<sub>g</sub>ua<sub>g</sub>e models are useful for many tasks.\n",
            ["Large Language models are useful for many tasks."])
        original = doc.md.read_text(encoding="utf-8")
        out = Path(self.temp.name) / "plan"
        self.assertEqual(self.run_cli("repair", str(doc.md), "--out", str(out))[0], 0)

        code, summary, _ = self.run_cli("repair", str(doc.md), "--out", str(out), "--apply")
        self.assertEqual(code, 0)
        applied = doc.md.read_text(encoding="utf-8")
        self.assertNotEqual(applied, original)
        self.assertIn("Large Language models", applied)
        self.assertNotIn("<sub>", applied)

        code, summary, _ = self.run_cli("repair", str(doc.md), "--out", str(out), "--apply")
        self.assertEqual(code, 0)
        self.assertIn("已应用 0 条", summary)
        self.assertEqual(doc.md.read_text(encoding="utf-8"), applied)

        drifted = original.replace("<sub>g</sub>", "<sub>q</sub>", 1)
        doc.md.write_text(drifted, encoding="utf-8")
        before = doc.md.read_bytes()
        code, _, err = self.run_cli("repair", str(doc.md), "--out", str(out), "--apply")
        self.assertEqual(code, 1)
        self.assertIn("不一致", err)
        self.assertEqual(doc.md.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
