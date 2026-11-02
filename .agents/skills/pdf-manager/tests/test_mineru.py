"""Offline checks of archive consumption and the MinerU API contract."""

import io
import json
from pathlib import Path
import sys
import tempfile
import ssl
import urllib.error
import unittest
from unittest.mock import Mock, patch
import zipfile

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import mineru_backend as backend


def archive(entries):
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w") as zf:
        for name, value in entries.items():
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            zf.writestr(name, value)
    return output.getvalue()


class ArchiveTests(unittest.TestCase):
    def test_bundled_real_v1_excerpt_supplies_actual_caption_and_path_fields(self):
        sample_path = Path(__file__).resolve().parents[1] / "references" / "samples" / "content_list.sample.json"
        sample = json.loads(sample_path.read_text(encoding="utf-8"))
        visuals = [sample["examples"][kind] for kind in ("image", "chart", "table")]
        # The entries are a real, truncated excerpt; this ZIP is a synthetic
        # test container, not another recorded cloud response.
        entries = {"full.md": "![](" + visuals[0]["img_path"] + ")", "sample_content_list.json": visuals}
        for item in visuals:
            entries[item["img_path"]] = b"fixture image bytes"
        result = backend.parse_archive(archive(entries), "sample")
        self.assertEqual(set(result["assets"]), {"sample-fig1.jpg", "sample-chart1.jpg", "sample-table1.jpg"})
        self.assertIn("../assets/sample-fig1.jpg", result["body"])

    def test_types_captions_duplicates_and_unreferenced_table(self):
        entries = {
            "full.md": "# Paper\n\n![](images/a.jpg)\nFigure 1: retained.\n\n<table><tr><td>3</td></tr></table>\n",
            "paper_content_list.json": [
                {"type": "image", "img_path": "images/a.jpg", "image_caption": ["Figure 1: A"]},
                {"type": "image", "img_path": "images/a.jpg", "image_caption": ["Figure 7: A reused"]},
                {"type": "image", "img_path": "images/b.jpg", "image_caption": ["Figure 1: B"]},
                {"type": "chart", "img_path": "images/c.jpg", "chart_caption": ["Figure 4: Chart"]},
                {"type": "table", "img_path": "images/t.jpg", "table_caption": ["Table 2: Results"]},
                {"type": "equation", "img_path": "images/e.jpg", "text": "x=y"},
            ],
            "images/a.jpg": b"a", "images/b.jpg": b"b", "images/c.jpg": b"c",
            "images/t.jpg": b"t", "images/e.jpg": b"e", "images/orphan.png": b"o",
            "layout.json": {"_version_name": "3.4.4", "_backend": "hybrid"},
        }
        result = backend.parse_archive(archive(entries), "arxiv-1v1")
        self.assertEqual(set(result["assets"]), {
            "arxiv-1v1-fig1.jpg", "arxiv-1v1-fig1-2.jpg", "arxiv-1v1-chart4.jpg",
            "arxiv-1v1-table2.jpg", "arxiv-1v1-eq1.jpg", "arxiv-1v1-img1.png"})
        self.assertIn("![](../assets/arxiv-1v1-fig1.jpg)", result["body"])
        self.assertEqual(result["body"].count("Figure 1: retained."), 1)
        self.assertIn("<table>", result["body"])
        self.assertNotIn("table2.jpg", result["body"])
        self.assertEqual(result["assets"]["arxiv-1v1-table2.jpg"], b"t")
        self.assertEqual(result["parser"], "mineru-cloud 3.4.4")

    def test_v2_only_supplements_v1_with_direct_formula_relation(self):
        result = backend.parse_archive(archive({
            "full.md": "$$x=y$$\n![](images/formula.png)",
            "paper_content_list.json": [
                {"type": "equation", "text": "x=y"},
                {"type": "image", "img_path": "images/fig.jpg", "image_caption": ["Fig. 3"]},
            ],
            "paper_content_list_v2.json": [[
                {"type": "equation_interline", "content": {"math_content": "x=y",
                    "image_source": {"path": "images/formula.png"}}},
                {"type": "chart", "content": {"image_source": {"path": "images/fig.jpg"},
                    "chart_caption": [{"type": "text", "content": "Figure 8"}]}},
            ]],
            "images/formula.png": b"eq", "images/fig.jpg": b"fig", "images/unknown.png": b"unknown",
        }), "paper")
        self.assertEqual(set(result["assets"]), {"paper-eq1.png", "paper-fig3.jpg", "paper-img1.png"})
        self.assertIn("$$x=y$$", result["body"])

    def test_nameless_equation_does_not_classify_arbitrary_orphan(self):
        result = backend.parse_archive(archive({
            "full.md": "text", "paper_content_list.json": [{"type": "equation", "text": "x=y"}],
            "images/orphan.jpg": b"not proven formula",
        }), "paper")
        self.assertEqual(list(result["assets"]), ["paper-img1.jpg"])

    def test_nested_zip_encoded_paths_html_and_reference_links(self):
        result = backend.parse_archive(archive({
            "result/full.md": "\x00# Paper\n![](<images/a (1).jpg> \"Caption\")\n"
                "<img src='images/a%20%281%29.jpg'>\n<img src=\"images/a (1).jpg\">\n"
                "![Figure][visual]\n[visual]: <images/a (1).jpg> 'title'\n",
            "result/document_content_list.json": [{"type": "image", "img_path": "images/a (1).jpg"}],
            "result/images/a (1).jpg": b"image", "result/debug.png": b"diagnostic",
        }), "中文 名称")
        self.assertEqual(len(result["assets"]), 1)
        destination = "../assets/%E4%B8%AD%E6%96%87%20%E5%90%8D%E7%A7%B0-fig1.jpg"
        self.assertEqual(result["body"].count(destination), 4)
        self.assertIn('"Caption"', result["body"])
        self.assertIn("'title'", result["body"])
        self.assertNotIn("\x00", result["body"])

    def test_unquoted_parentheses_and_markdown_title_are_preserved(self):
        result = backend.parse_archive(archive({
            "full.md": '![](images/a(1).jpg "description")',
            "images/a(1).jpg": b"image",
        }), "p")
        self.assertIn('![](../assets/p-img1.jpg "description")', result["body"])

    def test_optional_malformed_content_list_still_keeps_images(self):
        result = backend.parse_archive(archive({
            "full.md": "![](images/a.jpg)", "a_content_list.json": "{broken",
            "images/a.jpg": b"a",
        }), "p", requested_model="pipeline")
        self.assertEqual(result["parser"], "mineru-cloud pipeline")
        self.assertEqual(list(result["assets"]), ["p-img1.jpg"])
        self.assertTrue(result["warnings"])

    def test_invalid_or_ambiguous_archive_does_not_pass(self):
        for payload in (b"not zip", archive({"images/a.jpg": b"a"}),
                        archive({"a/full.md": "a", "b/full.md": "b"})):
            with self.subTest(payload=payload[:10]), self.assertRaises(backend.MinerUError):
                backend.parse_archive(payload, "p")

    def test_missing_local_image_cannot_remain_a_silent_broken_link(self):
        with self.assertRaises(backend.MinerUError):
            backend.parse_archive(archive({"full.md": '![](images/missing.jpg "caption")'}), "p")

    def test_empty_body_does_not_become_a_successful_conversion(self):
        with self.assertRaises(backend.MinerUError):
            backend.parse_archive(archive({"full.md": "\x00 \n"}), "p")

    def test_literal_image_examples_are_not_rewritten_or_reported_missing(self):
        body = '# Paper\n\n```md\n![](images/example.jpg)\n```\n\n`![](images/inline.png)`\n\n![](images/actual.png)\n'
        result = backend.parse_archive(archive({"full.md": body, "images/actual.png": b"image"}), "p")
        self.assertIn("![](images/example.jpg)", result["body"])
        self.assertIn("`![](images/inline.png)`", result["body"])
        self.assertIn("![](../assets/p-img1.png)", result["body"])


class TransportTests(unittest.TestCase):
    def setUp(self):
        self.key_patch = patch.object(backend, "api_key", return_value="secret")
        self.key_patch.start()
        self.addCleanup(self.key_patch.stop)

    @staticmethod
    def jobs(count=2):
        return [{"path": f"/pdf/paper{i}.pdf", "name": f"paper{i}.pdf", "data_id": f"source-{i}"}
                for i in range(count)]

    def test_all_expected_files_must_finish_and_options_are_sent(self):
        jobs = self.jobs()
        responses = [
            {"batch_id": "batch", "file_urls": ["upload-a", "upload-b"]},
            {"extract_result": [{"file_name": "paper0.pdf", "state": "done", "full_zip_url": "zip-a"}]},
            {"extract_result": [{"file_name": "paper0.pdf", "state": "done", "full_zip_url": "zip-a"},
                                {"file_name": "paper1.pdf", "state": "failed", "err_msg": "invalid PDF"}]},
        ]
        with patch.object(backend, "_request_json", side_effect=responses) as request, \
             patch.object(backend, "_upload_file") as upload, \
             patch.object(backend, "_download_zip", return_value=b"zip") as download, \
             patch.object(backend.time, "sleep"):
            results = list(backend.convert_files(jobs, model_version="pipeline", language="en",
                                                is_ocr=True, enable_formula=False, enable_table=True))
        self.assertEqual([result["state"] for result in results], ["done", "failed"])
        self.assertEqual(results[0]["zip_bytes"], b"zip")
        self.assertEqual(results[1]["error"], "invalid PDF")
        self.assertEqual(request.call_count, 3)
        payload = request.call_args_list[0].args[2]
        self.assertEqual(payload["language"], "en")
        self.assertFalse(payload["enable_formula"])
        self.assertTrue(payload["enable_table"])
        self.assertTrue(all(item["is_ocr"] for item in payload["files"]))
        self.assertEqual(upload.call_count, 2)
        download.assert_called_once_with("zip-a")

    def test_resume_uses_names_when_new_data_ids_differ_and_never_uploads(self):
        jobs = self.jobs(1)
        with patch.object(backend, "_request_json", return_value={"extract_result": [{
                 "data_id": "previous-id", "file_name": "paper0.pdf", "state": "done", "full_zip_url": "zip"}]}) as request, \
             patch.object(backend, "_upload_file") as upload, \
             patch.object(backend, "_download_zip", return_value=b"zip"):
            result = list(backend.convert_files(jobs, batch_id="existing"))[0]
        self.assertEqual(result["state"], "done")
        self.assertEqual(result["batch_id"], "existing")
        self.assertEqual(request.call_count, 1)
        self.assertEqual(request.call_args.args[0], "/extract-results/batch/existing")
        upload.assert_not_called()

    def test_timeout_returns_missing_files_with_batch_identifier(self):
        with patch.object(backend, "_request_json", return_value={"extract_result": []}), \
             patch.object(backend, "_upload_file") as upload:
            results = list(backend.convert_files(self.jobs(), batch_id="resume-me", timeout=0))
        self.assertEqual(len(results), 2)
        self.assertTrue(all(result["state"] == "pending" and result["batch_id"] == "resume-me"
                            and "超时" in result["error"] for result in results))
        upload.assert_not_called()

    def test_poll_connection_failure_retains_batch_for_resume(self):
        with patch.object(backend, "_request_json", side_effect=backend.MinerUError("connection failed")):
            results = list(backend.convert_files(self.jobs(), batch_id="keep-this-batch"))
        self.assertEqual(len(results), 2)
        self.assertTrue(all(r["state"] == "pending" and r["batch_id"] == "keep-this-batch" for r in results))

    def test_batches_are_capped_at_fifty(self):
        def request(route, key, data=None):
            self.assertEqual(route, "/file-urls/batch")
            return {"batch_id": str(len(data["files"])), "file_urls": ["upload"] * len(data["files"])}
        def results(batch, jobs, key, timeout):
            for job in jobs:
                yield {"data_id": job["data_id"], "file_name": job["name"], "state": "failed", "batch_id": batch}
        with patch.object(backend, "_request_json", side_effect=request) as requests, \
             patch.object(backend, "_upload_file"), patch.object(backend, "_batch_results", side_effect=results):
            output = list(backend.convert_files(self.jobs(101)))
        self.assertEqual([len(call.args[2]["files"]) for call in requests.call_args_list], [50, 50, 1])
        self.assertEqual(len(output), 101)

    def test_upload_failure_does_not_drop_other_jobs(self):
        with patch.object(backend, "_request_json", return_value={"batch_id": "b", "file_urls": ["a", "b"]}), \
             patch.object(backend, "_upload_file", side_effect=[backend.MinerUError("upload failed"), None]), \
             patch.object(backend, "_batch_results", return_value=iter([{"data_id": "source-1", "state": "done"}])) as poll:
            results = list(backend.convert_files(self.jobs()))
        self.assertEqual([r["state"] for r in results], ["failed", "done"])
        self.assertEqual(len(poll.call_args.args[1]), 1)

    def test_signed_put_does_not_set_content_type(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "test.pdf"
            path.write_bytes(b"%PDF-test")
            connection = Mock()
            connection.getresponse.return_value.status = 200
            with patch.object(backend.http.client, "HTTPSConnection", return_value=connection):
                backend._upload_file("https://storage.example/upload?signature=private", path)
        method, target = connection.request.call_args.args
        self.assertEqual((method, target), ("PUT", "/upload?signature=private"))
        self.assertNotIn("Content-Type", connection.request.call_args.kwargs["headers"])

    def test_missing_credential_is_clear_on_non_windows(self):
        self.key_patch.stop()
        with patch.dict(backend.os.environ, {}, clear=True), patch.object(backend.sys, "platform", "linux"):
            with self.assertRaisesRegex(backend.MinerUError, "MINERU_APIKEY"):
                backend.api_key()


class CdnDownloadTests(unittest.TestCase):
    URL = "https://cdn-mineru.openxlab.org.cn/pdf/result.zip?signature=example"

    def test_normal_download_does_not_bypass_system_routing(self):
        response = Mock()
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        payload = archive({"full.md": "text"})
        response.read.return_value = payload
        with patch.object(backend.urllib.request, "urlopen", return_value=response), \
             patch.object(backend, "_cdn_fallback") as fallback:
            self.assertEqual(backend._download_zip(self.URL), payload)
        fallback.assert_not_called()

    def test_cdn_tls_failure_uses_fallback_without_new_parse_task(self):
        payload = archive({"full.md": "text"})
        with patch.object(backend.urllib.request, "urlopen", side_effect=urllib.error.URLError(ssl.SSLEOFError("EOF"))), \
             patch.object(backend, "_cdn_fallback", return_value=payload) as fallback:
            self.assertEqual(backend._download_zip(self.URL), payload)
        fallback.assert_called_once_with(self.URL)

    def test_http_denial_and_unrelated_hosts_do_not_trigger_bypass(self):
        denial = urllib.error.HTTPError(self.URL, 403, "denied", {}, None)
        with patch.object(backend.urllib.request, "urlopen", side_effect=denial), \
             patch.object(backend, "_cdn_fallback") as fallback:
            with self.assertRaisesRegex(backend.MinerUError, "HTTP 403"):
                backend._download_zip(self.URL)
        fallback.assert_not_called()
        with patch.object(backend.urllib.request, "urlopen", side_effect=urllib.error.URLError("offline")), \
             patch.object(backend, "_cdn_fallback") as fallback:
            with self.assertRaises(backend.MinerUError):
                backend._download_zip("https://other.example/result.zip")
        fallback.assert_not_called()

    def test_dns_request_contains_only_hostname_and_rejects_fake_or_local_ips(self):
        response = Mock()
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        response.read.return_value = json.dumps({"Status": 0, "Answer": [
            {"type": 1, "data": value} for value in ("198.18.0.214", "127.0.0.1", "10.0.0.1", "8.8.8.8", "1.1.1.1", "9.9.9.9")
        ]}).encode()
        with patch.object(backend.urllib.request, "urlopen", return_value=response) as request:
            result = backend._doh_addresses("cdn-mineru.openxlab.org.cn", backend.DOH_RESOLVERS[0])
        self.assertEqual(result, ["8.8.8.8", "1.1.1.1"])
        query = backend.urllib.parse.parse_qs(backend.urllib.parse.urlsplit(request.call_args.args[0].full_url).query)
        self.assertEqual(query, {"name": ["cdn-mineru.openxlab.org.cn"], "type": ["A"]})

    def test_fallback_tries_current_addresses_then_another_resolver(self):
        with patch.object(backend, "_doh_addresses", side_effect=[["8.8.8.8", "1.1.1.1"], ["9.9.9.9"]]) as dns, \
             patch.object(backend, "_download_at_address", side_effect=[OSError("first"), OSError("second"), b"zip"]) as download:
            self.assertEqual(backend._cdn_fallback(self.URL), b"zip")
        self.assertEqual(dns.call_count, 2)
        self.assertEqual([call.args[1] for call in download.call_args_list], ["8.8.8.8", "1.1.1.1", "9.9.9.9"])

    def test_direct_address_keeps_certificate_validation_sni_and_http_host(self):
        context = ssl.create_default_context()
        self.assertTrue(context.check_hostname)
        self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
        raw, tls = Mock(), Mock()
        tls.makefile.return_value = io.BytesIO(b"HTTP/1.1 200 OK\r\nContent-Length: 3\r\n\r\nzip")
        with patch.object(backend.ssl, "create_default_context", return_value=context), \
             patch.object(context, "wrap_socket", return_value=tls) as wrap, \
             patch.object(backend.socket, "create_connection", return_value=raw) as connect:
            self.assertEqual(backend._download_at_address(self.URL, "8.8.8.8"), b"zip")
        connect.assert_called_once_with(("8.8.8.8", 443), timeout=30)
        wrap.assert_called_once_with(raw, server_hostname="cdn-mineru.openxlab.org.cn")
        request = b"".join(call.args[0] for call in tls.sendall.call_args_list)
        self.assertIn(b"Host: cdn-mineru.openxlab.org.cn\r\n", request)
        self.assertIn(b"GET /pdf/result.zip?signature=example HTTP/1.1", request)
        self.assertTrue(context.check_hostname)
        self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)


if __name__ == "__main__":
    unittest.main()
