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


def module(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + ".py"))
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


download = module("download_arxiv")
convert = module("pdf2md")


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        (self.base / "pdf").mkdir()
        for value in (download, convert):
            active = patch.multiple(value, BASE=str(self.base), PDF_DIR=str(self.base / "pdf"),
                                    META_PATH=str(self.base / "meta.json"),
                                    PROVENANCE_PATH=str(self.base / "provenance.json"))
            active.start()
            self.addCleanup(active.stop)
        self.aid = "2512.13564"
        self.meta = {self.aid: {"title": "Existing title", "exists": True}}
        self.provenance = {self.aid: {"version": None}}
        download.save_json(download.META_PATH, self.meta)
        download.save_json(download.PROVENANCE_PATH, self.provenance)
        self.original_meta = (self.base / "meta.json").read_bytes()

    def test_cached_pdf_never_fetches_or_replaces_metadata(self):
        pdf = self.base / "pdf" / (self.aid + ".pdf")
        pdf.write_bytes(b"legacy PDF bytes")
        with patch.object(download, "get", side_effect=AssertionError("network forbidden")):
            message = download.download_one(self.aid, self.meta, self.provenance)
        self.assertIn("preserved", message)
        self.assertEqual(pdf.read_bytes(), b"legacy PDF bytes")
        self.assertEqual((self.base / "meta.json").read_bytes(), self.original_meta)

    def test_metadata_failure_preserves_previous_records(self):
        with patch.object(download, "get", side_effect=OSError("offline")):
            message = download.download_one(self.aid, self.meta, self.provenance)
        self.assertIn("preserved", message)
        self.assertEqual((self.base / "meta.json").read_bytes(), self.original_meta)
        self.assertFalse(list((self.base / "pdf").iterdir()))

    def test_pdf_failure_does_not_commit_new_metadata(self):
        candidate = {"exists": True, "title": "New title", "versioned_id": self.aid + "v2"}
        with patch.object(download, "fetch_meta", return_value=candidate), \
             patch.object(download, "fetch_pdf", side_effect=OSError("offline")):
            message = download.download_one(self.aid, self.meta, self.provenance)
        self.assertIn("preserved", message)
        self.assertEqual((self.base / "meta.json").read_bytes(), self.original_meta)

    def test_unknown_version_is_not_guessed(self):
        with patch.object(download, "fetch_meta", return_value={"exists": True, "versioned_id": None}), \
             patch.object(download, "fetch_pdf", side_effect=AssertionError("must not download")):
            message = download.download_one(self.aid, self.meta, self.provenance)
        self.assertIn("version unresolved", message)
        self.assertEqual((self.base / "meta.json").read_bytes(), self.original_meta)

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
            download.download_one(self.aid, self.meta, self.provenance)
        self.assertEqual(calls, [f"https://arxiv.org/abs/{self.aid}",
                                 f"https://arxiv.org/abs/{version}", f"https://arxiv.org/pdf/{version}"])
        self.assertEqual(self.meta[self.aid]["title"], "Pinned metadata")
        self.assertEqual(self.provenance[self.aid]["pdf_sha256"], hashlib.sha256(pdf).hexdigest())
        self.assertEqual(self.provenance[self.aid]["version"], version)

    def test_non_pdf_response_is_rejected(self):
        with patch.object(download, "get", return_value=(200, b"<html>" + b"x" * 21000)):
            with self.assertRaises(ValueError):
                download.fetch_pdf(self.aid + "v2")

    def test_existing_conversion_is_preserved_without_parser(self):
        (self.base / "pdf" / (self.aid + ".pdf")).write_bytes(b"existing PDF")
        out = self.base / "surveys" / (self.aid + ".md")
        out.parent.mkdir()
        out.write_bytes(b"existing conversion")
        convert.convert(self.aid, self.meta, "surveys")
        self.assertEqual(out.read_bytes(), b"existing conversion")

    def test_conversion_records_real_parser_and_rejects_changed_pdf(self):
        import pymupdf
        pdf_path = self.base / "pdf" / (self.aid + ".pdf")
        doc = pymupdf.open()
        page = doc.new_page()
        page.insert_text((72, 72), "Memory pipeline source preservation check.")
        doc.save(pdf_path)
        doc.close()
        convert.convert(self.aid, self.meta, "surveys")
        out = self.base / "surveys" / (self.aid + ".md")
        raw = out.read_bytes()
        header, body = raw.split(b"\n---\n\n", 1)
        self.assertIn(b"Memory pipeline source preservation check.", body)
        self.assertNotIn("导航卡".encode(), header)
        record = json.loads((self.base / "provenance.json").read_text(encoding="utf-8"))[self.aid]
        self.assertEqual(record["conversion"]["body_sha256"], hashlib.sha256(body).hexdigest())
        self.assertTrue(record["conversion"]["parser_version"])
        self.assertFalse(record["conversion"]["visual_verification"])
        with pdf_path.open("ab") as stream:
            stream.write(b"changed")
        with self.assertRaisesRegex(ValueError, "SHA256"):
            convert.convert(self.aid, self.meta, "surveys", force=True)
        self.assertEqual(out.read_bytes(), raw)


if __name__ == "__main__":
    unittest.main()
