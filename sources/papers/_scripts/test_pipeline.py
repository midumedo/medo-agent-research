"""Offline regression checks for source preservation and version pairing.

Run with a Python environment containing pymupdf4llm and pymupdf:
    python -B test_pipeline.py
All downloads are mocked; conversion uses a tiny PDF created in a temp folder.
"""

import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))


def module(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + ".py"))
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


import stem

download = module("download_arxiv")
convert = module("pdf2md")

STEM = "arxiv-2512.13564"


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        (self.base / "pdf").mkdir()
        # Everything resolves through stem.BASE, so patching it moves the library.
        active = patch.object(stem, "BASE", str(self.base))
        active.start()
        self.addCleanup(active.stop)
        self.aid = STEM.split("-", 1)[1]
        self.meta = {STEM: {"title": "Existing title", "exists": True, "native_id": self.aid}}
        self.provenance = {STEM: {"version": None}}
        stem.save_meta(self.meta)
        stem.save_provenance(self.provenance)
        self.original_meta = (self.base / "meta.json").read_bytes()

    def test_cached_pdf_never_fetches_or_replaces_metadata(self):
        pdf = self.base / "pdf" / (STEM + ".pdf")
        pdf.write_bytes(b"legacy PDF bytes")
        with patch.object(download, "get", side_effect=AssertionError("network forbidden")):
            message = download.download_one(STEM, self.meta, self.provenance)
        self.assertIn("preserved", message)
        self.assertEqual(pdf.read_bytes(), b"legacy PDF bytes")
        self.assertEqual((self.base / "meta.json").read_bytes(), self.original_meta)

    def test_metadata_failure_preserves_previous_records(self):
        with patch.object(download, "get", side_effect=OSError("offline")):
            message = download.download_one(STEM, self.meta, self.provenance)
        self.assertIn("preserved", message)
        self.assertEqual((self.base / "meta.json").read_bytes(), self.original_meta)
        self.assertFalse(list((self.base / "pdf").iterdir()))

    def test_pdf_failure_does_not_commit_new_metadata(self):
        candidate = {"exists": True, "title": "New title", "versioned_id": self.aid + "v2"}
        with patch.object(download, "fetch_meta", return_value=candidate), \
             patch.object(download, "fetch_pdf", side_effect=OSError("offline")):
            message = download.download_one(STEM, self.meta, self.provenance)
        self.assertIn("preserved", message)
        self.assertEqual((self.base / "meta.json").read_bytes(), self.original_meta)

    def test_unknown_version_is_not_guessed(self):
        with patch.object(download, "fetch_meta", return_value={"exists": True, "versioned_id": None}), \
             patch.object(download, "resolve_version", return_value=None), \
             patch.object(download, "fetch_pdf", side_effect=AssertionError("must not download")):
            message = download.download_one(STEM, self.meta, self.provenance)
        self.assertIn("version unresolved", message)
        self.assertEqual((self.base / "meta.json").read_bytes(), self.original_meta)

    def test_rejects_a_registry_it_cannot_fetch(self):
        message = download.download_one("web-2025-example-paper", self.meta, self.provenance)
        self.assertIn("本脚本只处理 arXiv", message)

    def test_download_refetches_metadata_for_same_pinned_version(self):
        version = self.aid + "v2"
        calls = []
        pdf = b"%PDF-1.7\n" + b"x" * 20001

        def get(url):
            calls.append(url)
            if "/pdf/" in url:
                self.assertTrue(url.endswith(version))
                return 200, pdf
            title = "Latest metadata" if url.endswith(self.aid) else "Pinned metadata"
            return 200, (f'<meta name="citation_title" content="{title}">'
                         f'<meta name="citation_pdf_url" content="https://arxiv.org/pdf/{version}">').encode()

        with patch.object(download, "get", side_effect=get):
            download.download_one(STEM, self.meta, self.provenance)
        self.assertEqual(calls, [f"https://arxiv.org/abs/{self.aid}",
                                 f"https://arxiv.org/abs/{version}", f"https://arxiv.org/pdf/{version}"])
        self.assertEqual(self.meta[STEM]["title"], "Pinned metadata")
        self.assertEqual(self.provenance[STEM]["pdf_sha256"], hashlib.sha256(pdf).hexdigest())
        self.assertEqual(self.provenance[STEM]["version"], version)
        self.assertEqual(self.meta[STEM]["native_id"], self.aid)
        self.assertEqual(self.meta[STEM]["registry"], "arxiv")

    def test_non_pdf_response_is_rejected(self):
        with patch.object(download, "get", return_value=(200, b"<html>" + b"x" * 21000)):
            with self.assertRaises(ValueError):
                download.fetch_pdf(self.aid + "v2")

    def test_existing_conversion_is_preserved_without_parser(self):
        (self.base / "pdf" / (STEM + ".pdf")).write_bytes(b"existing PDF")
        out = self.base / "md" / (STEM + ".md")
        out.parent.mkdir()
        out.write_bytes(b"existing conversion")
        convert.convert(STEM, self.meta)
        self.assertEqual(out.read_bytes(), b"existing conversion")

    def test_conversion_records_real_parser_and_rejects_changed_pdf(self):
        import pymupdf
        pdf_path = self.base / "pdf" / (STEM + ".pdf")
        doc = pymupdf.open()
        page = doc.new_page()
        page.insert_text((72, 72), "Memory pipeline source preservation check.")
        doc.save(pdf_path)
        doc.close()
        convert.convert(STEM, self.meta)
        out = self.base / "md" / (STEM + ".md")
        raw = out.read_bytes()
        front, rest = raw.split(b"\n---\n\n", 1)
        header, body = rest.split(b"\n---\n\n", 1)
        self.assertIn(b"Memory pipeline source preservation check.", body)
        self.assertIn(b"id: " + STEM.encode(), front)
        self.assertNotIn("导航卡".encode(), header)
        record = json.loads((self.base / "provenance.json").read_text(encoding="utf-8"))[STEM]
        self.assertEqual(record["conversion"]["body_sha256"], hashlib.sha256(body).hexdigest())
        self.assertTrue(record["conversion"]["parser_version"])
        self.assertFalse(record["conversion"]["visual_verification"])
        with pdf_path.open("ab") as stream:
            stream.write(b"changed")
        with self.assertRaisesRegex(ValueError, "SHA256"):
            convert.convert(STEM, self.meta, force=True)
        self.assertEqual(out.read_bytes(), raw)


if __name__ == "__main__":
    unittest.main()
