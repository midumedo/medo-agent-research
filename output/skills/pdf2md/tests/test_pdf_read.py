"""Check the three evidence operations against a small real PDF."""

import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

SKILL_SCRIPTS = Path(__file__).resolve().parents[1] / "pdf2md/scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))
import pdf_read


class PdfReadTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.pdf = self.root / "两页 example.pdf"
        with pdf_read.pymupdf.open() as document:
            for text in ("Large Language Models\nFirst page.", "Large Language Models\nSecond page."):
                document.new_page().insert_text((72, 72), text)
            document.save(self.pdf)

    def run_cli(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(pdf_read.main([str(self.pdf), *args]), 0)
        return output.getvalue()

    def test_text_uses_pdf_page_positions_and_preserves_source(self):
        original = self.pdf.read_bytes()
        text = self.run_cli("--pages", "2")
        self.assertIn("Second page.", text)
        self.assertNotIn("First page.", text)
        self.assertEqual(self.pdf.read_bytes(), original)

    def test_find_returns_all_matching_pages_without_fuzzy_guesses(self):
        hits = json.loads(self.run_cli("--find", "large   language models"))
        self.assertEqual([hit["page"] for hit in hits], [1, 2])
        self.assertEqual(json.loads(self.run_cli("--find", "large memory models")), [])

    def test_render_writes_only_selected_page(self):
        folder = self.root / "页面"
        self.run_cli("--pages", "2", "--render", str(folder))
        files = list(folder.iterdir())
        self.assertEqual([path.name for path in files], ["两页 example-page-2.png"])
        self.assertTrue(files[0].read_bytes().startswith(b"\x89PNG\r\n\x1a\n"))


if __name__ == "__main__":
    unittest.main()
