"""Observable library operations; fixtures live only in temporary directories."""

import contextlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import quote
import zipfile

SKILL_SCRIPTS = Path(__file__).resolve().parents[1] / "pdf2md/scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))
import pdf_library as storage
import pdf2md as cli


def archive():
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as bundle:
        bundle.writestr("full.md", "# Source title\n\n## Abstract\nA source abstract.\n\n## 1 Introduction\n![](images/plot.jpg)")
        bundle.writestr("doc_content_list.json", json.dumps([
            {"type": "image", "img_path": "images/plot.jpg", "image_caption": ["Figure 1: A plot"]},
            {"type": "table", "img_path": "images/table.jpg", "table_caption": ["Table 2: Results"]},
        ]))
        bundle.writestr("images/plot.jpg", b"plot")
        bundle.writestr("images/table.jpg", b"table")
    return buffer.getvalue()


class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="pdf2md-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "资料 空间"
        self.lib = storage.Library(self.root)

    def doc(self, name="Report.中文 旧名称", ident=None):
        document = storage.Document(self.root, name)
        storage.atomic_bytes(document.pdf, b"%PDF-1.4\nfixture\n%%EOF")
        prefix = ident or name
        front = {"stem": name, "id": ident, "abstract": 'An abstract with "quotes" and \\alpha.', "keywords": ["human-choice"]}
        body = (f"# Title\n\n![figure](../assets/{quote(prefix + '-fig1.jpg', safe='-._~')})\n"
                f'<img src="../assets/{quote(prefix + "-chart1.jpg", safe="-._~")}">\n'
                f"[plate]: ../assets/{quote(prefix + '-img1.jpg', safe='-._~')}\n")
        storage.atomic_text(document.md, storage.render_markdown(front, body))
        for kind in ("fig1", "chart1", "table1", "img1"):
            storage.atomic_bytes(self.root / "assets" / f"{prefix}-{kind}.jpg", kind.encode())
        return document

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = cli.main(list(args))
        return code, out.getvalue(), err.getvalue()

    def test_no_index_needed_and_path_infers_root(self):
        doc = self.doc()
        resolved, _ = storage.resolve_document(str(doc.pdf))
        self.assertEqual(resolved.root, self.root)
        self.assertTrue(storage.check_document(resolved)["complete"])
        self.assertFalse(self.lib.index.exists())

    def test_generic_rename_updates_all_assets_and_optional_index(self):
        doc = self.doc()
        self.lib.write_index(self.lib.rebuilt_index())
        renamed = storage.rename_document(doc, "Report.中文 新名称")
        self.assertTrue(storage.check_document(renamed)["complete"])
        self.assertFalse(doc.pdf.exists())
        self.assertFalse(doc.md.exists())
        self.assertTrue((self.root / "assets" / "Report.中文 新名称-table1.jpg").exists())
        self.assertFalse((self.root / "assets" / (doc.stem + "-table1.jpg")).exists())
        rows = self.lib.read_index()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["id"], "")
        self.assertEqual(rows[0]["name"], renamed.stem)
        self.assertEqual(rows[0]["keywords"], ["human-choice"])

    def test_official_id_and_asset_names_stay_fixed_on_rename(self):
        ident = "arxiv-2504.19413v1"
        doc = self.doc(ident + ".Project.Old", ident)
        self.lib.write_index([{ "id": ident, "name": "Project.Old", "keywords": ["curated"], "revised": "2025-04-28"},
                              {"id": "arxiv-2401.00001v1", "name": "Survey.Offline", "keywords": [], "revised": ""}])
        renamed = storage.rename_document(doc, ident + ".Project.New")
        self.assertTrue(storage.check_document(renamed)["complete"])
        self.assertTrue((self.root / "assets" / f"{ident}-table1.jpg").exists())
        self.assertEqual(len(self.lib.read_index()), 2)
        self.assertEqual(renamed.record["keywords"], ["curated"])
        with self.assertRaises(storage.LibraryError):
            storage.rename_document(renamed, "arxiv-2504.19413v2.Project.New")

    def test_collision_preflight_leaves_every_source_unchanged(self):
        doc = self.doc()
        before = doc.md.read_bytes()
        storage.atomic_bytes(self.root / "assets" / "Report.New-table1.jpg", b"another paper")
        with self.assertRaises(storage.LibraryError):
            storage.rename_document(doc, "Report.New")
        self.assertEqual(doc.md.read_bytes(), before)
        self.assertTrue(doc.pdf.exists())
        self.assertFalse((self.root / "pdf" / "Report.New.pdf").exists())

    def test_conversion_validates_missing_asset_before_overwriting_md(self):
        doc = self.doc()
        before = doc.md.read_bytes()
        parsed = {"body": "![](../assets/missing.jpg)", "assets": {}, "parser": "mineru-cloud vlm"}
        with self.assertRaises(storage.LibraryError):
            storage.write_conversion(doc, parsed)
        self.assertEqual(before, doc.md.read_bytes())

    def test_partial_document_rename_cannot_pair_with_another_document(self):
        for source_kind, target_kind in (("md", "pdf"), ("pdf", "md")):
            with self.subTest(source_kind=source_kind):
                source = storage.Document(self.root, "Source.only-" + source_kind)
                target = storage.Document(self.root, "Target.only-" + target_kind)
                source_file = source.file(source_kind)
                target_file = target.file(target_kind)
                storage.atomic_bytes(source_file, b"source document")
                storage.atomic_bytes(target_file, b"different document")
                with self.assertRaises(storage.LibraryError):
                    storage.rename_document(source, target.stem)
                self.assertEqual(source_file.read_bytes(), b"source document")
                self.assertEqual(target_file.read_bytes(), b"different document")
                self.assertFalse(target.file(source_kind).exists())

    def test_index_without_identity_keeps_rows_and_explicit_keyword_clear(self):
        doc = self.doc()
        self.assertEqual(self.run_cli("index", "--root", str(self.root))[0], 0)
        self.assertEqual(self.run_cli("index", "--root", str(self.root), "--set-keywords", doc.stem, "")[0], 0)
        self.assertEqual(self.lib.read_index()[0]["keywords"], [])
        self.assertEqual(doc.front["keywords"], [])
        self.assertEqual(self.run_cli("index", "--root", str(self.root), "--check")[0], 0)

    def test_index_queries_read_saved_rows_without_collecting_unregistered_files(self):
        self.doc("Unregistered.Alias", "arxiv-2501.13956v1")
        code, output, _ = self.run_cli("index", "--root", str(self.root), "--list")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output), [])
        self.assertFalse(self.lib.index.exists())
        saved = [
            {"id": "", "name": "Offline.MissingKeywords", "keywords": [], "revised": "2025-01-23"},
            {"id": "", "name": "Offline.Curated", "keywords": ["selected"], "revised": ""},
        ]
        self.lib.write_index(saved)
        before = self.lib.index.read_bytes()
        code, output, _ = self.run_cli("index", "--root", str(self.root), "--list")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output), self.lib.read_index())
        code, output, _ = self.run_cli("index", "--root", str(self.root), "--missing-keywords")
        self.assertEqual(code, 0)
        missing = json.loads(output)
        self.assertEqual([row["name"] for row in missing], ["Offline.MissingKeywords"])
        self.assertIsNone(missing[0]["abstract"])
        self.assertEqual(self.lib.index.read_bytes(), before)

    def test_index_keyword_update_only_collects_target_and_preserves_other_rows(self):
        target = self.doc("Report.Target")
        unrelated = self.doc("Unregistered.Alias", "arxiv-2501.13956v1")
        self.doc("Report.OtherLocal")
        offline = {"id": "", "name": "Offline.Candidate", "keywords": ["keep"], "revised": "2025-01-23"}
        self.lib.write_index([{"id": "", "name": target.stem, "keywords": ["old"], "revised": ""}, offline])
        before = unrelated.md.read_bytes()
        code, _, _ = self.run_cli("index", "--root", str(self.root), "--set-keywords", target.stem, "memory;agent")
        self.assertEqual(code, 0)
        rows = {row["name"]: row for row in self.lib.read_index()}
        self.assertEqual(set(rows), {target.stem, offline["name"]})
        self.assertEqual(rows[target.stem]["keywords"], ["memory", "agent"])
        self.assertEqual(target.front["keywords"], ["memory", "agent"])
        self.assertEqual(rows[offline["name"]], offline)
        self.assertEqual(unrelated.md.read_bytes(), before)

    def test_index_check_compares_records_without_reformatting_saved_csv(self):
        self.doc("Report.One")
        self.doc("Report.Two")
        saved = ('\ufeffid,name,keywords,revised\r\n'
                 '"","Report.Two","human-choice",""\r\n'
                 '"","Offline.Candidate","keep","2025-01-23"\r\n'
                 '"","Report.One","human-choice",""\r\n')
        storage.atomic_text(self.lib.index, saved)
        before = self.lib.index.read_bytes()
        self.assertEqual(self.run_cli("index", "--root", str(self.root), "--check")[0], 0)
        self.assertEqual(self.lib.index.read_bytes(), before)
        self.doc("Report.New")
        self.assertEqual(self.run_cli("index", "--root", str(self.root), "--check")[0], 1)
        self.assertEqual(self.lib.index.read_bytes(), before)

    def test_index_rebuild_rejects_duplicate_saved_identity_without_rewriting(self):
        ident = "arxiv-2501.13956v1"
        rows = [{"id": ident, "name": "Project.One", "keywords": ["one"], "revised": ""},
                {"id": ident, "name": "Project.Two", "keywords": ["two"], "revised": ""}]
        storage.atomic_text(self.lib.index, self.lib.render_index(rows))
        before = self.lib.index.read_bytes()
        self.assertEqual(self.run_cli("index", "--root", str(self.root))[0], 1)
        self.assertEqual(self.lib.index.read_bytes(), before)

    def test_index_rebuild_allows_versions_but_rejects_two_local_names_for_one_identity(self):
        first_id = "arxiv-2501.13956v1"
        second_id = "arxiv-2501.13956v2"
        self.doc(first_id + ".Project.Zep", first_id)
        self.doc(second_id + ".Project.Zep", second_id)
        self.assertEqual({row["id"] for row in self.lib.rebuilt_index()}, {first_id, second_id})
        self.doc(first_id + ".Project.Other", first_id)
        self.assertEqual(self.run_cli("index", "--root", str(self.root))[0], 1)
        self.assertFalse(self.lib.index.exists())

    def test_index_identity_completion_replaces_name_only_row_and_keeps_curated_fields(self):
        ident = "arxiv-2501.13956v1"
        doc = self.doc(ident + ".Project.Zep")
        self.lib.write_index([{"id": "", "name": doc.stem, "keywords": ["curated"], "revised": "2025-01-23"}])
        self.assertEqual(self.run_cli("index", "--root", str(self.root))[0], 0)
        self.assertEqual(self.lib.read_index(), [{"id": ident, "name": "Project.Zep",
                                                 "keywords": ["curated"], "revised": "2025-01-23"}])

    def test_index_rebuild_rejects_two_saved_rows_for_same_file(self):
        ident = "arxiv-2501.13956v1"
        doc = self.doc(ident + ".Project.Zep", ident)
        rows = [{"id": "", "name": doc.stem, "keywords": ["one"], "revised": ""},
                {"id": ident, "name": "Project.Zep", "keywords": ["two"], "revised": ""}]
        for ordering in (rows, rows[::-1]):
            with self.subTest(ordering=ordering):
                storage.atomic_text(self.lib.index, self.lib.render_index(ordering))
                before = self.lib.index.read_bytes()
                self.assertEqual(self.run_cli("index", "--root", str(self.root))[0], 1)
                self.assertEqual(self.lib.index.read_bytes(), before)

    def test_index_rebuild_preserves_curated_fields_and_offline_rows_until_pruned(self):
        ident = "arxiv-2501.13956v1"
        doc = self.doc(ident + ".Project.Zep", ident)
        front, body = storage.read_markdown(doc.md)
        front["revised"] = "2025-01-01"
        storage.atomic_text(doc.md, storage.render_markdown(front, body))
        local = {"id": ident, "name": "Project.Zep", "keywords": ["curated"], "revised": "2025-01-23"}
        offline = {"id": "arxiv-2401.00001v1", "name": "Survey.Candidate", "keywords": ["keep"], "revised": ""}
        self.lib.write_index([local, offline])
        before = doc.md.read_bytes()
        self.assertEqual(self.run_cli("index", "--root", str(self.root))[0], 0)
        rows = {row["id"]: row for row in self.lib.read_index()}
        self.assertEqual(rows, {ident: local, offline["id"]: offline})
        self.assertEqual(doc.md.read_bytes(), before)
        self.assertEqual(self.run_cli("index", "--root", str(self.root), "--prune")[0], 0)
        self.assertEqual(self.lib.read_index(), [local])

    def test_download_only_fills_missing_index_revision_without_overwriting_curated_date(self):
        ident = "arxiv-2501.13956v1"
        fetched_date = "2025-01-23"
        for label, previous_date in (("missing", ""), ("curated", "2025-01-20")):
            with self.subTest(previous_date=previous_date):
                root = self.root / label
                library = storage.Library(root)
                library.write_index([{"id": ident, "name": "Project.Zep", "keywords": ["keep"], "revised": previous_date}])
                info = {"id": ident, "title": "Zep", "source": "https://arxiv.org/abs/2501.13956v1",
                        "pdf_url": "https://arxiv.org/pdf/2501.13956v1", "revised": fetched_date}
                with patch.object(cli.pdf_sources, "fetch_metadata", return_value=info), \
                     patch.object(cli.pdf_sources, "download_pdf", return_value=b"%PDF-1.4\n%%EOF"):
                    doc, _ = cli.download_one(ident, root, "Project.Zep")
                self.assertTrue(doc.pdf.is_file())
                self.assertFalse(doc.md.exists())
                self.assertEqual(library.read_index(), [{"id": ident, "name": "Project.Zep",
                                                        "keywords": ["keep"], "revised": previous_date or fetched_date}])

    def test_rename_adds_previously_unregistered_document_to_existing_index(self):
        doc = self.doc("Report.Unregistered")
        offline = {"id": "", "name": "Offline.Candidate", "keywords": ["keep"], "revised": "2025-01-23"}
        self.lib.write_index([offline])
        renamed = storage.rename_document(doc, "Report.Renamed")
        rows = {row["name"]: row for row in self.lib.read_index()}
        self.assertEqual(set(rows), {renamed.stem, offline["name"]})
        self.assertEqual(rows[offline["name"]], offline)
        self.assertEqual(rows[renamed.stem]["keywords"], ["human-choice"])
        self.assertTrue(storage.check_document(renamed)["complete"])

    def test_check_only_selected_document_and_metadata_is_complete(self):
        doc = self.doc()
        self.lib.write_index(self.lib.rebuilt_index() + [{"id": "arxiv-2401.00001v1", "name": "Survey.Missing", "keywords": [], "revised": ""}])
        self.assertEqual(self.run_cli("check", str(doc.pdf))[0], 0)
        self.assertEqual(self.run_cli("check", "--root", str(self.root), "--all")[0], 1)
        code, text, _ = self.run_cli("metadata", str(doc.pdf))
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(text)["abstract"], doc.front["abstract"])

    def test_unversioned_cached_pdf_does_not_fetch_latest_metadata(self):
        doc = self.doc("arxiv-2404.13501.Survey.Existing", "arxiv-2404.13501")
        with patch.object(cli.pdf_sources, "fetch_metadata", side_effect=AssertionError("must not resolve latest")):
            info = cli.metadata_for(str(doc.pdf))
        self.assertIsNone(info["version"])

    def test_download_convert_and_idempotent_rerun_without_index(self):
        def converted(jobs, **kwargs):
            for job in jobs:
                yield {"data_id": job["data_id"], "file_name": job["name"], "state": "done", "zip_bytes": archive(), "batch_id": "test"}
        info = {"id": None, "source": "https://example.org/paper.pdf", "pdf_url": "https://example.org/paper.pdf", "filename": "paper.pdf", "abstract": None}
        with patch.object(cli.pdf_sources, "fetch_metadata", return_value=info), \
             patch.object(cli.pdf_sources, "download_pdf", return_value=b"%PDF-1.4\n%%EOF"), \
             patch.object(cli.mineru_backend, "convert_files", side_effect=converted) as cloud:
            code, _, err = self.run_cli("download", info["pdf_url"], "--root", str(self.root), "--name", "Report.中文 名称", "--convert")
            self.assertEqual(code, 0, err)
            doc = storage.Document(self.root, "Report.中文 名称")
            self.assertTrue(storage.check_document(doc)["complete"])
            self.assertEqual(doc.front["abstract"], "A source abstract.")
            self.assertEqual(doc.front["source"], info["source"])
            self.assertTrue((self.root / "assets" / "Report.中文 名称-table2.jpg").exists())
            self.assertFalse(self.lib.index.exists())
            self.assertEqual(self.run_cli("convert", str(doc.pdf))[0], 0)
            self.assertEqual(cloud.call_count, 1)

    def test_download_pinned_missing_ledger_item_keeps_exact_version(self):
        ident = "arxiv-2504.19413v1"
        self.lib.write_index([{"id": ident, "name": "Project.Mem0", "keywords": [], "revised": "2025-04-28"}])
        with patch.object(cli.pdf_sources, "fetch_metadata", return_value={"id": ident, "pdf_url": "https://arxiv.org/pdf/2504.19413v1"}) as metadata, \
             patch.object(cli.pdf_sources, "download_pdf", return_value=b"%PDF-1.4\n%%EOF"):
            doc, _ = cli.download_one(ident + ".Project.Mem0", self.root)
        metadata.assert_called_once_with(ident)
        self.assertEqual(doc.stem, ident + ".Project.Mem0")

    def test_rename_generic_document_to_known_id_uses_stable_asset_prefix(self):
        doc = self.doc()
        ident = "arxiv-2504.19413v1"
        renamed = storage.rename_document(doc, ident + ".Project.Mem0")
        self.assertEqual(renamed.front["id"], ident)
        self.assertTrue((self.root / "assets" / f"{ident}-fig1.jpg").exists())
        again = storage.rename_document(renamed, ident + ".Project.Other")
        self.assertTrue(storage.check_document(again)["complete"])

    def test_no_index_resolves_existing_id_and_download_reuses_same_name(self):
        ident = "arxiv-2501.13956v1"
        doc = self.doc(ident + ".Project.Zep", ident)
        self.assertEqual(self.lib.resolve("2501.13956v1").stem, doc.stem)
        with patch.object(cli.pdf_sources, "fetch_metadata", side_effect=AssertionError("cached source must not refetch")):
            cached, info = cli.download_one("https://arxiv.org/pdf/2501.13956v1", self.root, "Project.Zep")
        self.assertEqual(cached.stem, doc.stem)
        self.assertEqual(info["state"], "cached")
        self.assertFalse(self.lib.index.exists())

    def test_encoded_hash_and_letter_duplicate_suffix_survive_rename(self):
        doc = self.doc("Report.C# old")
        special = doc.stem + "-fig3a-2.jpg"
        storage.atomic_bytes(self.root / "assets" / special, b"subfigure")
        fields, body = storage.read_markdown(doc.md)
        body += "\n![](../assets/" + quote(special, safe="-._~") + ")\n"
        storage.atomic_text(doc.md, storage.render_markdown(fields, body))
        self.assertTrue(storage.check_document(doc)["complete"])
        renamed = storage.rename_document(doc, "Report.C# new")
        self.assertTrue(storage.check_document(renamed)["complete"])
        self.assertTrue((self.root / "assets" / "Report.C# new-fig3a-2.jpg").exists())
        self.assertFalse((self.root / "assets" / special).exists())

    def test_legacy_arxiv_id_download_stays_in_flat_directory(self):
        info = {"id": "arxiv-cs-9901001v1", "pdf_url": "https://arxiv.org/pdf/cs/9901001v1", "title": "Old paper"}
        with patch.object(cli.pdf_sources, "fetch_metadata", return_value=info), \
             patch.object(cli.pdf_sources, "download_pdf", return_value=b"%PDF-1.4\n%%EOF"):
            doc, _ = cli.download_one("cs/9901001v1", self.root, "Project.Old")
        self.assertEqual(doc.pdf.parent, self.root / "pdf")
        self.assertEqual(doc.ident, info["id"])
        self.assertEqual(self.lib.resolve("cs/9901001v1").stem, doc.stem)

    def test_register_only_md_is_incomplete_and_is_repaired(self):
        doc = self.doc()
        storage.atomic_text(doc.md, '---\nstem: "' + doc.stem + '"\n---\n')
        state = storage.check_document(doc)
        self.assertFalse(state["complete"])
        self.assertFalse(state["md_body"])
        def converted(jobs, **kwargs):
            for job in jobs:
                yield {"data_id": job["data_id"], "state": "done", "zip_bytes": archive()}
        with patch.object(cli.mineru_backend, "convert_files", side_effect=converted) as cloud:
            code, _, error = self.run_cli("convert", str(doc.pdf))
        self.assertEqual(code, 0, error)
        cloud.assert_called_once()
        self.assertTrue(storage.check_document(doc)["complete"])

    def test_explicit_missing_path_never_selects_same_basename(self):
        doc = self.doc("same")
        missing = str(self.root / "elsewhere" / "same.pdf")
        with self.assertRaises(storage.LibraryError):
            storage.resolve_document(missing, self.root)
        with patch.object(cli.mineru_backend, "convert_files") as cloud:
            code, _, _ = self.run_cli("convert", missing, "--root", str(self.root))
        self.assertEqual(code, 1)
        cloud.assert_not_called()
        code, output, _ = self.run_cli("check", missing, str(doc.pdf), "--root", str(self.root))
        results = json.loads(output)
        self.assertEqual(code, 1)
        self.assertEqual(sum(bool(row["complete"]) for row in results), 1)
        self.assertEqual(len(results), 2)

    def test_code_examples_and_plain_paths_are_not_asset_links(self):
        doc = self.doc()
        literals = '\nPath example: ../assets/not-real.png\n`![](../assets/inline.png)`\n```md\n![](../assets/fenced.png)\n```\n'
        front, body = storage.read_markdown(doc.md)
        storage.atomic_text(doc.md, storage.render_markdown(front, body + literals))
        self.assertTrue(storage.check_document(doc)["complete"])
        renamed = storage.rename_document(doc, "Report.Renamed")
        self.assertIn(literals, renamed.md.read_text(encoding="utf-8"))
        self.assertTrue(storage.check_document(renamed)["complete"])

    def test_metadata_reads_standalone_file_and_retains_partial_batch_results(self):
        standalone = Path(self.temp.name) / "Downloads" / "paper.md"
        storage.atomic_text(standalone, "# Exact title\n\n## Abstract\nAn actual abstract.\n\n## Introduction\nBody.")
        missing = standalone.with_name("absent.md")
        code, output, _ = self.run_cli("metadata", str(standalone), str(missing))
        results = json.loads(output)
        self.assertEqual(code, 1)
        self.assertEqual(results[0]["abstract"], "An actual abstract.")
        self.assertEqual(results[0]["md"], str(standalone))
        self.assertEqual(results[1]["state"], "failed")
        self.assertFalse((standalone.parent / "md").exists())

    def test_nonstandard_local_image_paths_are_checked_and_repaired(self):
        doc = self.doc()
        front, _ = storage.read_markdown(doc.md)
        body = ('# Existing conversion\n'
                '![plot [detail]](images/missing.jpg)\n'
                '<img src="../figures/missing.png">\n'
                '![Chart][chart]\n[chart]: images/missing%20chart.png\n')
        storage.atomic_text(doc.md, storage.render_markdown(front, body))
        state = storage.check_document(doc)
        self.assertFalse(state["complete"])
        self.assertCountEqual(state["missing_images"],
                              ["images/missing.jpg", "../figures/missing.png", "images/missing chart.png"])
        def converted(jobs, **kwargs):
            for job in jobs:
                yield {"data_id": job["data_id"], "state": "done", "zip_bytes": archive()}
        with patch.object(cli.mineru_backend, "convert_files", side_effect=converted) as cloud:
            code, _, error = self.run_cli("convert", str(doc.pdf))
        self.assertEqual(code, 0, error)
        cloud.assert_called_once()
        self.assertTrue(storage.check_document(doc)["complete"])

    def test_existing_local_images_ignore_nonimage_links_and_examples(self):
        doc = self.doc()
        storage.atomic_bytes(doc.md.parent / "images" / "present.png", b"image")
        front, body = storage.read_markdown(doc.md)
        body += ('\n![plot](images/present.png)\n![remote](https://example.org/image.png)\n'
                 '[related](missing-paper.md)\n[reference][paper]\n[paper]: missing.pdf\n'
                 '[unused]: images/missing.png\n`![example](images/missing.png)`\n'
                 '```md\n![example](images/also-missing.png)\n```\n')
        storage.atomic_text(doc.md, storage.render_markdown(front, body))
        self.assertTrue(storage.check_document(doc)["complete"])

    def test_root_scopes_bare_name_even_if_cwd_has_another_same_name(self):
        doc = self.doc("same")
        elsewhere = Path(self.temp.name) / "elsewhere"
        storage.atomic_bytes(elsewhere / "same.pdf", b"%PDF-1.4\nwrong source")
        old_cwd = Path.cwd()
        try:
            os.chdir(elsewhere)
            info = cli.metadata_for("same.pdf", self.root)
        finally:
            os.chdir(old_cwd)
        self.assertEqual(info["pdf"], str(doc.pdf))
        self.assertEqual(info["abstract"], doc.front["abstract"])

    def test_explicit_metadata_path_reads_that_file_not_another_library_copy(self):
        doc = self.doc("same")
        other = Path(self.temp.name) / "other" / "same.md"
        storage.atomic_text(other, "# Other paper\n\n## Abstract\nOther actual abstract.\n\n## Introduction\nText")
        info = cli.metadata_for(str(other), self.root)
        self.assertEqual(info["abstract"], "Other actual abstract.")
        self.assertEqual(info["md"], str(other))
        self.assertIsNone(info["pdf"])

    def test_alias_identity_resolves_actual_file_and_index_rejects_phantom_path(self):
        ident = "arxiv-2501.13956v1"
        doc = self.doc("Alias", ident)
        self.assertEqual(self.lib.resolve(ident).pdf, doc.pdf)
        code, _, _ = self.run_cli("index", "--root", str(self.root))
        self.assertEqual(code, 1)
        self.assertFalse(self.lib.index.exists())
        storage.rename_document(doc, ident + ".Project.Zep")
        self.assertEqual(self.run_cli("index", "--root", str(self.root))[0], 0)

    def test_same_identity_cannot_overwrite_another_documents_assets(self):
        ident = "arxiv-2501.13956v1"
        first = self.doc(ident + ".Project.One", ident)
        self.doc(ident + ".Project.Two", ident)
        before = first.md.read_bytes()
        with patch.object(cli.mineru_backend, "convert_files") as cloud:
            code, _, error = self.run_cli("convert", str(first.pdf), "--force")
        self.assertEqual(code, 1)
        self.assertIn("同一资产前缀", error)
        cloud.assert_not_called()
        self.assertEqual(first.md.read_bytes(), before)

    def test_generic_url_reuses_known_source_without_redownloading(self):
        doc = self.doc()
        front, body = storage.read_markdown(doc.md)
        front["source"] = "https://example.org/report.pdf"
        storage.atomic_text(doc.md, storage.render_markdown(front, body))
        with patch.object(cli.pdf_sources, "fetch_metadata", side_effect=AssertionError("cached")), \
             patch.object(cli.pdf_sources, "download_pdf", side_effect=AssertionError("cached")):
            selected, info = cli.download_one(front["source"], self.root)
        self.assertEqual(selected.stem, doc.stem)
        self.assertEqual(info["state"], "cached")


if __name__ == "__main__":
    unittest.main()
