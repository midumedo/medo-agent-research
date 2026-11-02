"""Construct download_one where no local document matches; it must not crash."""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(r"d:\workspace\memory\.agents\skills\pdf-manager\scripts")))
import pdf_manager
import pdf_sources

url = "https://example.org/paper.pdf"
info = {"id": "arxiv-2504.99999v1", "title": "Some Paper", "pdf_url": url}
pdf_sources.fetch_metadata = lambda value: dict(info)
pdf_sources.download_pdf = lambda target: b"%PDF-1.4\n%%EOF\n"

with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    doc, payload = pdf_manager.download_one(url, root)
    print("CASE-A no cache, ident ->", doc.stem, doc.pdf.is_file(), payload["state"])

with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    doc, payload = pdf_manager.download_one(url, root, name="custom name")
    print("CASE-B no cache, name ->", doc.stem, doc.pdf.is_file())

with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    info_no_id = {"title": "Untitled", "pdf_url": url, "filename": "fallback.pdf"}
    pdf_sources.fetch_metadata = lambda value: dict(info_no_id)
    doc, payload = pdf_manager.download_one(url, root)
    print("CASE-C no cache, no id ->", doc.stem, doc.pdf.is_file())
