"""Source lookup tests run offline and do not alter a document library."""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

SKILL_SCRIPTS = Path(__file__).resolve().parents[1] / "pdf2md/scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))
import pdf_sources as sources


def atom(aid="2504.19413v1", abstract="Original $x_1$ abstract.", updated="2025-04-28T00:00:00Z"):
    return f'''<feed xmlns="http://www.w3.org/2005/Atom"><entry>
      <id>http://arxiv.org/abs/{aid}</id><title>The original title</title>
      <summary>{abstract}</summary><published>2025-04-21T00:00:00Z</published>
      <updated>{updated}</updated><author><name>Example Author</name></author>
    </entry></feed>'''.encode()


def page(aid="2504.19413v1", abstract="Version-specific abstract."):
    return f'''<html><head>
      <meta content="Original title" name="citation_title">
      <meta name="citation_pdf_url" content="https://arxiv.org/pdf/{aid}">
      <meta name="citation_author" content="Example Author">
      <meta name="citation_date" content="2025/04/21">
      </head><body><blockquote class="abstract mathjax">
      <span class="descriptor">Abstract:</span>{abstract}</blockquote></body></html>'''.encode()


class ArxivIdentityTests(unittest.TestCase):
    def test_exact_input_forms_keep_requested_version(self):
        for value in ("2504.19413v1", "arxiv-2504.19413v1", "arXiv:2504.19413v1",
                      "https://arxiv.org/abs/2504.19413v1", "https://arxiv.org/pdf/2504.19413v1.pdf"):
            self.assertEqual(sources.arxiv_id(value), "2504.19413v1")

    def test_old_arxiv_ids_are_supported_without_swallowing_filenames(self):
        self.assertEqual(sources.arxiv_id("https://arxiv.org/abs/hep-th/9901001v2"), "hep-th/9901001v2")
        self.assertIsNone(sources.arxiv_id("arxiv-2504.19413v1.Project.Mem0.pdf"))
        self.assertIsNone(sources.arxiv_id("https://notarxiv.org/abs/2504.19413v1"))

    def test_explicit_version_is_sent_to_api_unchanged(self):
        requested = []

        def response(url, **kwargs):
            requested.append(url)
            if "/abs/" in url:
                return page(), url
            return atom(), url

        with patch.object(sources, "_read_url", side_effect=response):
            result = sources.fetch_metadata("2504.19413v1")
        self.assertTrue(any("id_list=2504.19413v1" in url for url in requested))
        self.assertEqual(result["id"], "arxiv-2504.19413v1")
        self.assertEqual(result["version"], "v1")
        self.assertEqual(result["revised"], "2025-04-28")
        self.assertEqual(result["abstract"], "Version-specific abstract.")

    def test_current_api_response_cannot_fill_a_pinned_record(self):
        def response(url, **kwargs):
            if "/abs/" in url:
                return page(abstract="Old version."), url
            return atom("2504.19413v9", "New version.", "2026-10-01T00:00:00Z"), url

        with patch.object(sources, "_read_url", side_effect=response):
            result = sources.fetch_metadata("2504.19413v1")
        self.assertEqual(result["abstract"], "Old version.")
        self.assertIsNone(result["revised"])
        self.assertEqual(result["pdf_url"], "https://arxiv.org/pdf/2504.19413v1")

    def test_page_redirect_to_another_version_is_not_used(self):
        def response(url, **kwargs):
            if "/abs/" in url:
                return page("2504.19413v9", "New version."), "https://arxiv.org/abs/2504.19413v9"
            return atom("2504.19413v9", "New version."), url

        with patch.object(sources, "_read_url", side_effect=response):
            result = sources.fetch_metadata("2504.19413v1")
        self.assertIsNone(result["title"])
        self.assertIsNone(result["abstract"])
        self.assertEqual(result["versioned_id"], "2504.19413v1")

    def test_unversioned_page_is_resolved_then_api_uses_that_version(self):
        requested = []

        def response(url, **kwargs):
            requested.append(url)
            return (page("2504.19413v3"), url) if "/abs/" in url else (atom("2504.19413v3"), url)

        with patch.object(sources, "_read_url", side_effect=response):
            result = sources.fetch_metadata("2504.19413")
        self.assertEqual(result["id"], "arxiv-2504.19413v3")
        self.assertTrue(any("id_list=2504.19413v3" in url for url in requested))

    def test_unknown_version_is_not_guessed(self):
        with patch.object(sources, "_read_url", side_effect=sources.SourceError("Offline")):
            with self.assertRaisesRegex(sources.SourceError, "version unresolved"):
                sources.fetch_metadata("2504.19413")

    def test_explicit_identity_survives_unavailable_metadata(self):
        with patch.object(sources, "_read_url", side_effect=sources.SourceError("Offline")):
            result = sources.fetch_metadata("2504.19413v1")
        self.assertEqual(result["id"], "arxiv-2504.19413v1")
        self.assertIsNone(result["abstract"])
        self.assertIn("warnings", result)

    def test_html_abstract_keeps_mathematical_subscripts(self):
        with patch.object(sources, "_read_url", side_effect=lambda url, **kwargs: (page(abstract="Uses $x_1$ and H<sub>2</sub>O."), url)
                          if "/abs/" in url else (atom(), url)):
            result = sources.fetch_metadata("2504.19413v1")
        self.assertEqual(result["abstract"], "Uses $x_1$ and H<sub>2</sub>O.")


class DownloadTests(unittest.TestCase):
    def test_plain_url_needs_no_search_or_metadata_network_call(self):
        with patch.object(sources, "_read_url", side_effect=AssertionError("must not fetch")):
            result = sources.fetch_metadata("https://example.test/report%20one.pdf?download=1")
        self.assertEqual(result["filename"], "report one.pdf")
        self.assertIsNone(result["id"])
        self.assertIsNone(result["abstract"])

    def test_small_pdf_is_accepted(self):
        payload = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\n%%EOF"
        with patch.object(sources, "_read_url", return_value=(payload, "https://example.test/tiny.pdf")):
            self.assertEqual(sources.download_pdf("https://example.test/tiny.pdf"), payload)

    def test_non_pdf_and_empty_responses_are_rejected(self):
        for payload in (b"", b"<html>Login required</html>"):
            with self.subTest(payload=payload), patch.object(sources, "_read_url", return_value=(payload, "https://example.test/doc")):
                with self.assertRaises(sources.SourceError):
                    sources.download_pdf("https://example.test/doc")


class ConvertedAbstractTests(unittest.TestCase):
    def test_extracts_only_a_labelled_abstract(self):
        text = "# Paper title\n\nAuthors\n\n## Abstract\nUses $x_1$ and H<sub>2</sub>O.\nSecond line.\n\n## 1 Introduction\nMust not enter the abstract."
        self.assertEqual(sources.extract_document_metadata(text), {
            "title": "Paper title", "abstract": "Uses $x_1$ and H<sub>2</sub>O. Second line."})

    def test_absent_abstract_is_not_inferred_from_introduction(self):
        result = sources.extract_document_metadata("# A paper\n\nFirst paragraph.\n\n## Introduction\nMore content.")
        self.assertIsNone(result["abstract"])

    def test_inline_abstract_stops_before_keywords_and_plain_introduction(self):
        for boundary in ("Keywords: memory, agent", "1 Introduction"):
            result = sources.extract_document_metadata("# Title\n\n**Abstract**—Actual source abstract.\n" + boundary + "\nExcluded.")
            self.assertEqual(result["abstract"], "Actual source abstract.")

    def test_existing_front_matter_abstract_takes_precedence(self):
        text = '---\nstem: Report.Name\nabstract: "Source abstract with $x_1$."\n---\n\n# Original title\n\n## Abstract\nDo not replace the registered source abstract.\n'
        self.assertEqual(sources.extract_document_metadata(text), {"title": "Original title", "abstract": "Source abstract with $x_1$."})

    def test_chinese_abstract_is_supported(self):
        result = sources.extract_document_metadata("# 论文题目\n\n摘要：这是来源摘要。\n\n关键词：记忆\n排除。")
        self.assertEqual(result["abstract"], "这是来源摘要。")


if __name__ == "__main__":
    unittest.main()
