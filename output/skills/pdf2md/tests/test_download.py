"""Recover missing originals without changing or mispairing existing material."""

from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

SKILL_SCRIPTS = Path(__file__).resolve().parents[1] / "pdf2md/scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))
import pdf_library as storage
import pdf2md as cli


class DownloadRepairTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="pdf-download-repair-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.ident = "arxiv-2501.13956v1"
        self.info = {"id": self.ident, "title": "Fetched title",
                     "source": "https://arxiv.org/abs/2501.13956v1",
                     "pdf_url": "https://arxiv.org/pdf/2501.13956v1"}
        fetch_patch = patch.object(cli.pdf_sources, "fetch_metadata", return_value=self.info)
        download_patch = patch.object(cli.pdf_sources, "download_pdf", return_value=b"%PDF-1.4\noriginal")
        self.fetch = fetch_patch.start()
        self.download = download_patch.start()
        self.addCleanup(fetch_patch.stop)
        self.addCleanup(download_patch.stop)

    def markdown(self, stem, fields):
        doc = storage.Document(self.root, stem)
        storage.atomic_text(doc.md, storage.render_markdown(fields, "# Existing body\n"))
        return doc

    def test_arxiv_repair_preserves_markdown_name_and_optional_index(self):
        for indexed in (False, True):
            with self.subTest(indexed=indexed), tempfile.TemporaryDirectory(dir=self.root) as folder:
                root = Path(folder)
                doc = storage.Document(root, self.ident + ".Project.Existing")
                storage.atomic_text(doc.md, storage.render_markdown(
                    {"id": self.ident, "title": "Existing title", "keywords": ["chosen"]}, "# Existing body\n"))
                original_md = doc.md.read_bytes()
                library = storage.Library(root)
                if indexed:
                    library.write_index([{"id": self.ident, "name": "Project.Existing",
                                          "keywords": ["chosen"], "revised": "2025-01-23"}])
                original_index = library.index.read_bytes() if indexed else None
                selected, result = cli.download_one("2501.13956v1", root)
                self.assertEqual(selected.stem, doc.stem)
                self.assertEqual(result["state"], "downloaded")
                self.assertEqual(doc.pdf.read_bytes(), b"%PDF-1.4\noriginal")
                self.assertEqual(doc.md.read_bytes(), original_md)
                self.assertEqual(library.index.read_bytes() if indexed else None, original_index)
                self.assertEqual(library.index.exists(), indexed)

    def test_unversioned_repair_pins_existing_revision(self):
        doc = self.markdown(self.ident + ".Project.Existing", {"id": self.ident})
        selected, _ = cli.download_one("2501.13956", self.root)
        self.fetch.assert_called_once_with(self.ident)
        self.assertEqual(selected.stem, doc.stem)

    def test_explicit_different_name_requires_rename_for_md_only_material(self):
        doc = self.markdown(self.ident + ".Project.Existing", {"id": self.ident})
        with self.assertRaisesRegex(storage.LibraryError, "rename"):
            cli.download_one("2501.13956v1", self.root, "Project.Other")
        self.fetch.assert_not_called()
        self.download.assert_not_called()
        self.assertFalse(doc.pdf.exists())

    def test_plain_url_repair_uses_exact_recorded_source(self):
        url = "https://example.org/report.pdf"
        self.fetch.return_value = {"source": url, "pdf_url": url, "filename": "report.pdf"}
        doc = self.markdown("Report.Existing", {"source": url})
        original_md = doc.md.read_bytes()
        selected, _ = cli.download_one(url, self.root)
        self.assertEqual(selected.stem, doc.stem)
        self.assertTrue(doc.pdf.is_file())
        self.assertEqual(doc.md.read_bytes(), original_md)
        self.assertFalse(storage.Library(self.root).index.exists())

    def test_same_name_without_source_evidence_or_with_other_source_is_refused(self):
        url = "https://example.org/report.pdf"
        self.fetch.return_value = {"source": url, "pdf_url": url, "filename": "report.pdf"}
        for fields in ({}, {"source": "https://other.org/report.pdf"}):
            with self.subTest(fields=fields), tempfile.TemporaryDirectory(dir=self.root) as folder:
                root = Path(folder)
                doc = storage.Document(root, "Report.Existing")
                storage.atomic_text(doc.md, storage.render_markdown(fields, "# Existing\n"))
                before = doc.md.read_bytes()
                with self.assertRaises(storage.LibraryError):
                    cli.download_one(url, root, "Report.Existing")
                self.assertFalse(doc.pdf.exists())
                self.assertEqual(doc.md.read_bytes(), before)
        self.download.assert_not_called()

    def test_conflicting_arxiv_identity_or_source_is_refused(self):
        for fields in ({"id": "arxiv-2501.13956v2"},
                       {"id": self.ident, "source": "https://arxiv.org/abs/2501.13956v2"}):
            with self.subTest(fields=fields), tempfile.TemporaryDirectory(dir=self.root) as folder:
                root = Path(folder)
                doc = storage.Document(root, self.ident + ".Project.Existing")
                storage.atomic_text(doc.md, storage.render_markdown(fields, "# Existing\n"))
                storage.Library(root).write_index([{"id": self.ident, "name": "Project.Existing"}])
                before = doc.md.read_bytes()
                with self.assertRaisesRegex(storage.LibraryError, "冲突"):
                    cli.download_one("2501.13956v1", root)
                self.assertFalse(doc.pdf.exists())
                self.assertEqual(doc.md.read_bytes(), before)
        self.download.assert_not_called()

    def test_metadata_cannot_replace_existing_pinned_revision(self):
        doc = self.markdown(self.ident + ".Project.Existing", {"id": self.ident})
        self.fetch.return_value = {"id": "arxiv-2501.13956v2",
                                   "pdf_url": "https://arxiv.org/pdf/2501.13956v2"}
        with self.assertRaisesRegex(storage.LibraryError, "冲突"):
            cli.download_one("2501.13956v1", self.root)
        self.download.assert_not_called()
        self.assertFalse(doc.pdf.exists())


if __name__ == "__main__":
    unittest.main()
