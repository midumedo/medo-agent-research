"""Offline regression checks for source preservation and version pairing.

Run with any Python 3.13 (the toolchain is stdlib-only):
    python -B test_pipeline.py
All downloads are mocked; conversion uses a tiny PDF created in a temp folder.
"""

import hashlib
import io
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

import stem  # noqa: E402
import meta  # noqa: E402
import pdf  # noqa: E402
import convert  # noqa: E402
import build_index  # noqa: E402
import pipeline  # noqa: E402
import keywords  # noqa: E402
import status  # noqa: E402

STEM = "arxiv-2512.13564.Memory in the Age of AI Agents"
AID = "2512.13564"
ID = "arxiv-2512.13564"
NAME = "Memory in the Age of AI Agents"


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
        self.aid = AID
        self.meta = {STEM: {"title": "Existing title", "exists": True, "native_id": AID,
                            "id": ID, "registry": "arxiv"}}
        stem.save_index({"papers": [{"id": ID, "name": NAME,
                                     "keywords": [], "revised": ""}]})

    def test_cached_pdf_never_fetches_or_replaces_metadata(self):
        cached = self.base / "pdf" / (STEM + ".pdf")
        cached.write_bytes(b"legacy PDF bytes")
        with patch.object(meta, "get", side_effect=AssertionError("network forbidden")):
            message = pdf.download_one(STEM)
        self.assertIn("preserved", message)
        self.assertEqual(cached.read_bytes(), b"legacy PDF bytes")

    def test_metadata_failure_preserves_previous_records(self):
        with patch.object(meta, "get", side_effect=OSError("offline")):
            message = pdf.download_one(STEM)
        self.assertIn("preserved", message)
        self.assertFalse(list((self.base / "pdf").iterdir()))

    def test_pdf_failure_does_not_commit_new_metadata(self):
        candidate = {"exists": True, "title": "New title", "versioned_id": self.aid + "v2"}
        with patch.object(meta, "fetch_meta", return_value=candidate), \
             patch.object(pdf, "fetch_pdf", side_effect=OSError("offline")):
            message = pdf.download_one(STEM)
        self.assertIn("preserved", message)

    def test_unknown_version_is_not_guessed(self):
        with patch.object(meta, "fetch_meta", return_value={"exists": True, "versioned_id": None}), \
             patch.object(meta, "resolve_meta", return_value=(None, None, None)), \
             patch.object(pdf, "fetch_pdf", side_effect=AssertionError("must not download")):
            message = pdf.download_one(STEM)
        self.assertIn("version unresolved", message)

    def test_refuses_a_source_it_cannot_resolve(self):
        message = pdf.download_one("some-unknown-title")
        self.assertIn("只有 arXiv 来源能自动下载", message)

    def test_download_refetches_metadata_for_same_pinned_version(self):
        version = self.aid + "v2"
        calls = []
        payload = b"%PDF-1.7\n" + b"x" * 20001

        def get(url):
            calls.append(url)
            if "/pdf/" in url:
                self.assertTrue(url.endswith(version))
                return 200, payload
            title = "Latest metadata" if url.endswith(self.aid) else "Pinned metadata"
            return 200, (f'<meta name="citation_title" content="{title}">'
                         f'<meta name="citation_pdf_url" content="https://arxiv.org/pdf/{version}">').encode()

        with patch.object(meta, "get", side_effect=get):
            pdf.download_one(STEM)
        self.assertEqual(calls, [f"https://arxiv.org/abs/{self.aid}",
                                 f"https://arxiv.org/abs/{version}", f"https://arxiv.org/pdf/{version}"])
        # 元数据不再另存：这里只保证按固定版本取回了 PDF。
        self.assertEqual((self.base / "pdf" / (STEM + ".pdf")).read_bytes(), payload)
        self.assertFalse((self.base / "meta.json").exists())
        self.assertFalse((self.base / "provenance.json").exists())

    def test_non_pdf_response_is_rejected(self):
        with patch.object(meta, "get", return_value=(200, b"<html>" + b"x" * 21000)):
            with self.assertRaises(ValueError):
                pdf.fetch_pdf(self.aid + "v2")

class VisualNamingTests(unittest.TestCase):
    """图注解析、命名映射与引用改写：纯函数，不联网、不建 zip。"""

    ITEMS = [
        {"type": "text", "text": "Intro", "text_level": 1, "page_idx": 0},
        {"type": "image", "img_path": "images/aaaa.jpg",
         "image_caption": ["Figure 1: Overview of the architecture."], "page_idx": 2},
        {"type": "image", "img_path": "images/bbbb.jpg", "page_idx": 3},
        {"type": "image", "img_path": "images/cccc.jpg", "page_idx": 4},
        {"type": "table", "img_path": "images/dddd.jpg",
         "table_caption": ["Table 2: Main results."], "page_idx": 5},
    ]

    def test_control_characters_are_stripped(self):
        """MinerU 偶尔在公式里吐出控制字节；NUL 会让 grep 把 md 当二进制。"""
        raw = "E -ℓ\x00h, (x, y)\x03 end\ttab\nnext\r\n"
        out = convert.sanitize_text(raw)
        self.assertNotIn("\x00", out)
        self.assertNotIn("\x03", out)
        self.assertIn("\ttab", out)
        self.assertIn("next\r\n", out)

    def test_orphan_images_named_eq_when_all_equations(self):
        """无 img_path 的条目全是 equation 时，孤儿图可以确证是公式。"""
        items = [{"img_path": "images/a.jpg", "kind": "image", "number": "1",
                  "caption": None, "page": 0},
                 {"img_path": "", "kind": "equation", "number": None,
                  "caption": None, "page": 1},
                 {"img_path": "", "kind": "equation", "number": None,
                  "caption": None, "page": 2}]
        m = convert.name_map(items, "arxiv-1v1",
                            ["images/a.jpg", "images/b.jpg", "images/c.jpg"])
        self.assertEqual(m["images/a.jpg"], "arxiv-1v1-fig1.jpg")
        self.assertEqual(m["images/b.jpg"], "arxiv-1v1-eq1.jpg")
        self.assertEqual(m["images/c.jpg"], "arxiv-1v1-eq2.jpg")

    def test_orphan_images_are_img_when_kinds_mix(self):
        """混了 table 就无法确证哪张是公式，归 others 用 img。"""
        items = [{"img_path": "", "kind": "equation", "number": None, "caption": None, "page": 1},
                 {"img_path": "", "kind": "table", "number": None, "caption": None, "page": 2}]
        m = convert.name_map(items, "arxiv-1v1", ["images/b.jpg", "images/c.jpg"])
        self.assertTrue(all("-img" in v for v in m.values()), m)

    def test_orphan_images_are_img_when_content_list_says_nothing(self):
        """content_list 完全没提的图，不能说它们是公式。"""
        m = convert.name_map([], "arxiv-1v1", ["images/b.jpg"])
        self.assertEqual(m["images/b.jpg"], "arxiv-1v1-img1.jpg")

    def test_chart_caption_is_read(self):
        """chart 的图注在 `chart_caption`，不是 `image_caption`——拿错就是空的。"""
        items = [{"type": "chart", "img_path": "images/x.jpg",
                  "chart_caption": ["Figure 4: Latency comparison."],
                  "page_idx": 1}]
        out = convert.parse_visual(items)
        self.assertEqual(out[0]["caption"], "Figure 4: Latency comparison.")
        self.assertEqual(out[0]["number"], "4")

    def test_figure_number_from_caption(self):
        mapping = convert.name_map(convert.parse_visual(self.ITEMS), "arxiv-2504.19413v1")
        self.assertEqual(mapping["images/aaaa.jpg"], "arxiv-2504.19413v1-fig1.jpg")

    def test_numberless_image_falls_back_to_seq(self):
        mapping = convert.name_map(convert.parse_visual(self.ITEMS), "arxiv-2504.19413v1")
        self.assertEqual(mapping["images/bbbb.jpg"], "arxiv-2504.19413v1-fig2.jpg")
        self.assertEqual(mapping["images/cccc.jpg"], "arxiv-2504.19413v1-fig3.jpg")

    def test_table_uses_table_caption(self):
        mapping = convert.name_map(convert.parse_visual(self.ITEMS), "arxiv-2504.19413v1")
        self.assertEqual(mapping["images/dddd.jpg"], "arxiv-2504.19413v1-table2.jpg")

    def test_duplicate_number_gets_suffix(self):
        dup = [{"type": "image", "img_path": "images/p.jpg",
                "image_caption": ["Figure 3: First part."], "page_idx": 1},
               {"type": "image", "img_path": "images/q.jpg",
                "image_caption": ["Figure 3: Second part."], "page_idx": 2}]
        mapping = convert.name_map(convert.parse_visual(dup), "arxiv-1v1")
        self.assertEqual(mapping["images/p.jpg"], "arxiv-1v1-fig3.jpg")
        self.assertEqual(mapping["images/q.jpg"], "arxiv-1v1-fig3-2.jpg")

    def test_rewrite_refs_maps_names(self):
        mapping = {"aaaa.jpg": "arxiv-1v1-fig1.jpg"}
        out = convert.rewrite_image_refs(
            'see ![](images/aaaa.jpg) and <img src="images/aaaa.jpg">\n', mapping)
        self.assertIn("](../assets/arxiv-1v1-fig1.jpg)", out)
        self.assertIn('src="../assets/arxiv-1v1-fig1.jpg"', out)
        self.assertNotIn("images/aaaa.jpg", out)


class IndexCsvTests(unittest.TestCase):
    """index.csv 四列往返 + md front matter 七字段。"""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        active = patch.object(stem, "BASE", self.temp.name)
        active.start()
        self.addCleanup(active.stop)

    def test_index_csv_roundtrip(self):
        stem.write_index([{"id": "arxiv-1v1", "name": "A-Mem",
                           "keywords": ["memory", "context"], "revised": "2025-10-08"}])
        back = stem.read_index()
        self.assertEqual(len(back), 1)
        self.assertEqual(back[0]["id"], "arxiv-1v1")
        self.assertEqual(back[0]["name"], "A-Mem")
        self.assertEqual(back[0]["keywords"], ["memory", "context"])
        self.assertEqual(back[0]["revised"], "2025-10-08")
        self.assertNotIn("date", back[0], "date 已由 revised 取代")

    def test_front_matter_fields(self):
        text = stem.front_matter("a-v1", {"id": "arxiv-1v1"},
                                 source="https://arxiv.org/abs/xv1",
                                 keywords=["memory"], abstract="abs", revised="2025-10-08",
                                 parser="mineru-cloud")
        for key in ("stem:", "id:", "keywords:", "abstract:", "revised:", "source:",
                    "parser:"):
            self.assertIn(key, text)
        self.assertIn("https://arxiv.org/abs/xv1", text)
        self.assertNotIn("converted_at", text, "转换时间由 git 承载，不进登记块")
        self.assertNotIn("\ndate:", text, "date 字段已由 revised 取代")
        self.assertNotIn("registry:", text)
        self.assertNotIn("native_id:", text)
        self.assertNotIn("pdf_sha256:", text)

    def test_version_suffix(self):
        self.assertEqual(stem.version_suffix("2504.19413v11"), "v11")
        self.assertEqual(stem.version_suffix(None), "")
        self.assertEqual(stem.version_suffix("unknown"), "")


def fake_zip(entries):
    """A real in-memory zip, so the asset pipeline is exercised without a network."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for name, payload in entries.items():
            zf.writestr(name, payload)
    buf.seek(0)
    return zipfile.ZipFile(buf)


class NamesAndAssetsTests(unittest.TestCase):
    """文件名拼装、非法字符替换、图片全覆盖命名、manifest 取消。"""

    TYPE_TOKENS = ("Survey", "Bench", "Project", "Model", "Method", "Analysis")

    def test_every_name_carries_a_type_prefix(self):
        """名字一律是 `<类型>.<领域或名字>`，类型首字母大写、取自封闭小集。"""
        rows = stem.read_index()
        self.assertTrue(rows, "索引为空，无法校验命名规则")
        for row in rows:
            name = row.get("name") or ""
            token, sep, rest = name.partition(".")
            self.assertEqual(sep, ".", f"{row['id']}: 类型与名称之间要用 `.` 连接")
            self.assertIn(token, self.TYPE_TOKENS,
                          f"{row['id']}: 类型前缀 {token!r} 不在词表内")
            self.assertTrue(rest.strip(), f"{row['id']}: 类型后没有领域或名字")

    def test_stem_of_composes_filename(self):
        self.assertEqual(stem.stem_of({"id": "arxiv-1v1", "name": "A-Mem"}),
                         "arxiv-1v1.A-Mem")

    def test_sanitize_name_replaces_illegal(self):
        self.assertEqual(stem.sanitize_name("A-Mem: Agentic Memory"),
                         "A-Mem. Agentic Memory")

    def test_sanitize_name_keeps_case(self):
        self.assertEqual(stem.sanitize_name("Mem0: Building X"), "Mem0. Building X")

    def test_name_map_covers_every_zip_image(self):
        items = [{"img_path": "images/a.jpg", "kind": "image", "number": "1",
                  "caption": "Figure 1: x", "page": 0}]
        mapping = convert.name_map(items, "arxiv-1v1",
                                  ["images/a.jpg", "images/b.jpg", "images/c.jpg"])
        self.assertEqual(mapping["images/a.jpg"], "arxiv-1v1-fig1.jpg")
        for path in ("images/b.jpg", "images/c.jpg"):
            self.assertIn(path, mapping)
            self.assertFalse(re.fullmatch(r"[0-9a-f]{64}\.[a-z]+", mapping[path]),
                             "没有 content_list 记录的图不得保留 hash 名")
        self.assertEqual(len(set(mapping.values())), 3, "三个名字必须互不相同")

    def test_mineru_version_read_from_layout(self):
        """版本只在 zip 的 layout.json 里，API 响应从不给。"""
        zf = fake_zip({"layout.json":
                       '{"pdf_info": [], "_backend": "hybrid", "_effort": "medium",'
                       ' "_ocr_enable": false, "_version_name": "3.4.4"}'})
        version, backend = convert.mineru_version(zf)
        self.assertEqual(version, "3.4.4")
        self.assertEqual(backend, "hybrid")

    def test_mineru_version_absent_is_not_invented(self):
        version, backend = convert.mineru_version(fake_zip({"layout.json": '{"pdf_info": []}'}))
        self.assertIsNone(version)
        self.assertIsNone(backend)

    def test_parser_label_prefers_the_reported_version(self):
        self.assertEqual(convert.parser_label({}, "vlm", "3.4.4"), "mineru-cloud 3.4.4")
        self.assertEqual(convert.parser_label({}, "vlm", None), "mineru-cloud vlm")

    def test_front_matter_has_no_converted_at(self):
        """converted_at 由 revised 与 git 覆盖，不再进登记块。"""
        text = stem.front_matter("a-v1", {"id": "arxiv-1v1"},
                                 keywords=["memory"], parser="mineru-cloud 3.4.4")
        self.assertNotIn("converted_at", text)

    def test_write_assets_writes_no_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(stem, "BASE", tmp):
                zf = fake_zip({"images/a.jpg": b"a" * 10, "images/b.jpg": b"b" * 20})
                items = [{"img_path": "images/a.jpg", "kind": "image", "number": "1",
                          "caption": "Figure 1: x", "page": 0}]
                mapping = convert.name_map(items, "arxiv-1v1",
                                          ["images/a.jpg", "images/b.jpg"])
                info = convert.write_assets(zf, "arxiv-1v1.A-Mem", "arxiv-1v1",
                                           items, mapping, True)
                files = sorted(os.listdir(os.path.join(tmp, "assets")))
                self.assertEqual(files, ["arxiv-1v1-fig1.jpg", "arxiv-1v1-img1.jpg"])
                self.assertNotIn("manifest", info)


class DocumentWriteTests(unittest.TestCase):
    """写 md 的单一入口：文本先构建、后开文件，登记块只有 front matter 一个。"""

    def test_write_document_preserves_register_fields(self):
        """重转不得洗掉 abstract/revised/source。

        `open(path, "w")` 一调用就截断；`front_matter` 却靠读旧文件来保留这三个
        字段。若读发生在句柄打开之后，读到的是空文件，三个字段全变 null —— 这是
        实测过的真实事故（一次 --force 探针把一篇的 abstract/revised/source 洗空）。
        """
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(stem, "BASE", tmp):
                os.makedirs(os.path.join(tmp, "md"))
                stem_name = "arxiv-1v1.A-Mem"
                with open(stem.md_path(stem_name), "w", encoding="utf-8", newline="\n") as f:
                    f.write(stem.front_matter(stem_name, {"id": "arxiv-1v1"},
                                              keywords=["memory"], abstract="keep me",
                                              revised="2025-01-01",
                                              source="https://arxiv.org/abs/1v1")
                            + "old body\n")
                convert.write_document(stem_name, {"id": "arxiv-1v1"}, "arxiv-1v1",
                                      "mineru-cloud 3.4.4", "# new body")
                got = stem.read_front_matter(stem_name)
                self.assertEqual(got["abstract"], "keep me")
                self.assertEqual(got["revised"], "2025-01-01")
                self.assertEqual(got["source"], "https://arxiv.org/abs/1v1")
                self.assertEqual(got["parser"], "mineru-cloud 3.4.4")
                text = open(stem.md_path(stem_name), encoding="utf-8").read()
                self.assertTrue(text.endswith("# new body\n"))
                for marker in ("- 解析器:", "- 转换时间:", "- 本地 PDF SHA256:", "- 图片:"):
                    self.assertNotIn(marker, text, "正文里不该再有第二个登记块")
                self.assertEqual(text.count("\n---\n"), 1, "只允许 front matter 那一对分隔线")


class LedgerTests(unittest.TestCase):
    """index.csv 是账本：磁盘缺料不能把它清空，删行只能显式 --prune。"""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        active = patch.object(stem, "BASE", self.temp.name)
        active.start()
        self.addCleanup(active.stop)

    def test_build_index_keeps_the_ledger_when_disk_is_empty(self):
        stem.write_index([{"id": "arxiv-1v1", "name": "Project.A",
                           "keywords": ["memory"], "revised": "2025-01-01"},
                          {"id": "arxiv-2v1", "name": "Bench.B",
                           "keywords": [], "revised": ""}])
        before = open(stem.index_path(), encoding="utf-8").read()
        with patch.object(sys, "argv", ["build_index.py"]):
            build_index.main()
        after = open(stem.index_path(), encoding="utf-8").read()
        self.assertEqual(before, after, "磁盘上没有 pdf/md 时不得清空索引")

    def test_build_index_check_passes_on_an_empty_disk(self):
        stem.write_index([{"id": "arxiv-1v1", "name": "Project.A",
                           "keywords": [], "revised": ""}])
        with patch.object(sys, "argv", ["build_index.py", "--check"]):
            build_index.main()          # 不抛 SystemExit 即通过

    def test_prune_is_the_only_way_to_drop_a_row(self):
        stem.write_index([{"id": "arxiv-1v1", "name": "Project.A",
                           "keywords": [], "revised": ""}])
        with patch.object(sys, "argv", ["build_index.py", "--prune"]):
            build_index.main()
        self.assertEqual(stem.read_index(), [])


class AbstractChainTests(unittest.TestCase):
    """摘要提取链：API summary → abs 页 → 人工判读；取不到就 None，绝不编造。"""

    ATOM_FEED = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<feed xmlns="http://www.w3.org/2005/Atom"><entry>'
        '<id>http://arxiv.org/abs/2504.19413v2</id>'
        '<updated>2025-04-28T01:49:46Z</updated>'
        '<published>2025-04-10T00:00:00Z</published>'
        '<title>Mem0:  Building   Production-Ready Agents</title>'
        '<summary>Abstract:  We  introduce  Mem0. </summary>'
        '</entry></feed>')

    def test_normalize_abstract_flattens_and_strips_label(self):
        self.assertEqual(meta.normalize_abstract("Abstract:  a  b "), "a b")
        self.assertIsNone(meta.normalize_abstract(""))
        self.assertIsNone(meta.normalize_abstract(None))

    def test_api_entry_reads_the_summary(self):
        with patch.object(meta, "get", return_value=(200, self.ATOM_FEED.encode())):
            entry = meta.api_entry("2504.19413")
        self.assertEqual(entry["versioned_id"], "2504.19413v2")
        self.assertEqual(entry["abstract"], "We introduce Mem0.")
        self.assertEqual(entry["updated"], "2025-04-28T01:49:46Z")

    def test_arxiv_meta_prefers_the_summary(self):
        def fake_get(url):
            if "export.arxiv.org" in url:
                return 200, self.ATOM_FEED.encode()
            return 200, b'<html><meta name="citation_title" content="Mem0"></html>'

        with patch.object(meta, "get", side_effect=fake_get):
            info = meta.arxiv_meta("2504.19413")
        self.assertEqual(info["abstract"], "We introduce Mem0.")
        self.assertEqual(info["revised"], "2025-04-28")
        self.assertEqual(info["versioned_id"], "2504.19413v2")
        self.assertEqual(info["source"], "https://arxiv.org/abs/2504.19413v2")

    def test_arxiv_meta_is_none_when_nothing_is_reachable(self):
        with patch.object(meta, "get", side_effect=OSError("offline")):
            self.assertIsNone(meta.arxiv_meta("2504.19413"))

    def test_convert_fills_the_register_from_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(stem, "BASE", tmp):
                stem_name = "arxiv-1v1.Project.A"
                convert.write_document(stem_name, {"id": "arxiv-1v1"}, "arxiv-1v1",
                                       "mineru-cloud 3.4.4", "# body",
                                       abstract="the abstract", revised="2025-01-01",
                                       source="https://arxiv.org/abs/1v1")
                got = stem.read_front_matter(stem_name)
                self.assertEqual(got["abstract"], "the abstract")
                self.assertEqual(got["revised"], "2025-01-01")
                self.assertEqual(got["source"], "https://arxiv.org/abs/1v1")


class MaterialCheckTests(unittest.TestCase):
    """编排的完整性终检：缺 md 也算不齐，不再假绿。"""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        active = patch.object(stem, "BASE", self.temp.name)
        active.start()
        self.addCleanup(active.stop)
        stem.write_index([{"id": "arxiv-1v1", "name": "Project.A",
                           "keywords": [], "revised": ""}])

    def test_check_fails_when_md_is_absent(self):
        with patch.object(sys, "argv", ["pipeline.py", "--check"]):
            with self.assertRaises(SystemExit):
                pipeline.main()

    def test_check_passes_when_md_and_its_images_are_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(stem, "BASE", tmp):
                os.makedirs(os.path.join(tmp, "md"))
                os.makedirs(os.path.join(tmp, "assets"))
                with open(os.path.join(tmp, "assets", "arxiv-1v1-fig1.jpg"), "wb") as f:
                    f.write(b"x")
                name = "arxiv-1v1.Project.A"
                with open(stem.md_path(name), "w", encoding="utf-8", newline="\n") as f:
                    f.write("![](../assets/arxiv-1v1-fig1.jpg)\n")
                stem.write_index([{"id": "arxiv-1v1", "name": "Project.A",
                                   "keywords": [], "revised": ""}])
                with patch.object(sys, "argv", ["pipeline.py", "--check"]):
                    pipeline.main()      # 不抛即通过


class KeywordsTests(unittest.TestCase):
    """打词只搬运不生成：--set 只改命中行，--missing 只列缺词的行并带上摘要。"""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        active = patch.object(stem, "BASE", self.temp.name)
        active.start()
        self.addCleanup(active.stop)
        os.makedirs(os.path.join(self.temp.name, "md"))
        stem.write_index([{"id": "arxiv-1v1", "name": "Project.A",
                           "keywords": ["memory"], "revised": ""},
                          {"id": "arxiv-2v1", "name": "Bench.B",
                           "keywords": [], "revised": ""}])

    def test_set_touches_only_the_target_row(self):
        with patch.object(sys, "argv", ["keywords.py", "--set", "arxiv-2v1", "memory;benchmark"]):
            keywords.main()
        rows = {r["id"]: r for r in stem.read_index()}
        self.assertEqual(rows["arxiv-2v1"]["keywords"], ["memory", "benchmark"])
        self.assertEqual(rows["arxiv-1v1"]["keywords"], ["memory"], "其余行不得改动")

    def test_set_refuses_an_unknown_id(self):
        with patch.object(sys, "argv", ["keywords.py", "--set", "arxiv-9v9", "x"]):
            with self.assertRaises(SystemExit):
                keywords.main()

    def test_missing_lists_the_abstract_of_untagged_rows(self):
        name = "arxiv-2v1.Bench.B"
        with open(stem.md_path(name), "w", encoding="utf-8", newline="\n") as f:
            f.write(stem.front_matter(name, {"id": "arxiv-2v1"}, abstract="an abstract") + "body\n")
        buf = io.StringIO()
        with patch.object(sys, "argv", ["keywords.py", "--missing"]), redirect_stdout(buf):
            keywords.main()
        out = buf.getvalue()
        self.assertIn("arxiv-2v1", out)
        self.assertIn("an abstract", out)
        self.assertNotIn("arxiv-1v1", out, "已有关键词的行不再列出")


class StatusTests(unittest.TestCase):
    """反追踪状态：缺料要报，--sync 幂等地把派生目录移出索引。"""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.base = self.root / "sources" / "papers"
        self.base.mkdir(parents=True)
        active = patch.object(stem, "BASE", str(self.base))
        active.start()
        self.addCleanup(active.stop)
        stem.write_index([{"id": "arxiv-1v1", "name": "Project.A",
                           "keywords": [], "revised": ""}])

    def test_check_fails_when_md_is_absent(self):
        with patch.object(sys, "argv", ["status.py", "--check"]):
            with self.assertRaises(SystemExit):
                status.main()

    def test_sync_adds_every_derived_ignore_line(self):
        with patch.object(sys, "argv", ["status.py", "--sync"]):
            status.main()
        text = (self.root / ".gitignore").read_text(encoding="utf-8")
        for name in status.DERIVED:
            self.assertIn(f"/sources/papers/{name}/", text)

    def test_sync_is_idempotent(self):
        with patch.object(sys, "argv", ["status.py", "--sync"]):
            status.main()
        once = (self.root / ".gitignore").read_text(encoding="utf-8")
        with patch.object(sys, "argv", ["status.py", "--sync"]):
            status.main()
        twice = (self.root / ".gitignore").read_text(encoding="utf-8")
        self.assertEqual(once, twice)


if __name__ == "__main__":
    unittest.main()
