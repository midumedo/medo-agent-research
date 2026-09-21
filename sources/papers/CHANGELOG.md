# CHANGELOG · 论文库

只追加，不删改；最新在下。它记「什么时候多了什么、改了什么」，不重复 index.json 里的数据。

- 2026-09-20 · 入库 · 7 篇 · 首批综述材料，PDF 与机器转换文本写入 `pdf/` 与当时的分类目录；来源版本与获取时间缺失，记为 unknown。
- 2026-09-21 · 入库 · 20 篇 · 10 篇基准 + 10 篇框架，编号与日期经 arXiv 官方接口核对（脚本 `_scripts/check_arxiv.py`）。
- 2026-09-22 · 结构 · 全库 · 取消 `surveys/`、`benchmarks/`、`frameworks/` 三级分类目录，改为按表示形式分 `pdf/`、`md/`、`json/`；类型从目录迁入索引，可多值、可复核后改写。
- 2026-09-22 · 换行 · 7 篇 · 首批七份原以 CRLF 入库，随迁移归一为 LF；逐字节比对确认内容未变，`.gitattributes` 中对应的 `-text` 规则一并移除。
- 2026-09-22 · 记录 · 全库 · 每份 md 追加 YAML front matter；正文未改动。
- 2026-09-22 · 命名 · 全库 · 由「`<registry>-<native-id>` 作文件名」改为**标题 slug 作文件名**，`<registry>-<native-id>` 退为 index.json 与 front matter 里的 `id`。27 份材料全部改名，`id` 不变。这是对本日早先「不按标题命名」决定的推翻，理由见 [决定记录](../../dialogue/2026-09-22-papers-layout-and-naming.md)。
- 2026-09-22 · 索引 · 全库 · 清单从 INDEX.md 迁出：新增 `index.json` 作为唯一事实来源，`INDEX.md` 改为字段说明与查询方式，日志独立为 `CHANGELOG.md`。新增 `_scripts/build_index.py` 与 `_scripts/index_query.py`（内存 SQLite，`--emit` 可导出 `.sql`）。
- 2026-09-22 · 图片 · 约定 · 转换图片默认只写 `assets/<词干>/manifest.json`（文件名、字节数、SHA256 + 图注），字节需 `--keep-images` 才落盘；md 内的 `images/` 引用改写为 `../assets/<词干>/`。
