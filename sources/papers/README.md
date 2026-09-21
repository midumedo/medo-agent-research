# 论文来源库

现有二十七份 PDF 和对应的机器转换文本。**文件在本地不代表已经完成内容核实或 PDF 视觉核验。** 阅读建议、比较和待调查问题见 [我方综述阅读入口](../../analysis/surveys/README.md)；本轮横评用到的基准与框架编号见 [记忆横评对照](../../analysis/memory-benchmark-crossreview-2026-09.md)。

| 路径 | 内容与限制 |
|---|---|
| [surveys/](surveys/README.md) | 第一批七份的机器转换 Markdown；头部是元数据与转换声明，分隔线之后是转换正文。其中 2606.06448 与 2607.16848 不是综述，因既有引用较多而保留在此 |
| `benchmarks/` | 2026-09-21 入库的十份基准论文转换文本（LoCoMo、LongMemEval、MemoryAgentBench、BEAM、AMA-Bench、LongMemEval-V2、MemBench、MemoryBench、PersonaMem、MemoryArena） |
| `frameworks/` | 2026-09-21 入库的十份记忆框架论文转换文本（Zep、Mem0、MemOS、EverMemOS、MemoryOS、MIRIX、A-MEM、SimpleMem、AtomMem、AgeMem） |
| `pdf/` | 既有 PDF 文件，保留原样 |
| [meta.json](meta.json) | 历史抓取的标题、作者、日期与摘要；尚未核对与现有 PDF 是否同版 |
| [provenance.json](provenance.json) | 当前本地 PDF SHA256、版本与获取信息、转换记录；缺失字段为 `null` |
| `_scripts/` | 本项目的下载与转换工具，不属于外部证据 |
| `logs/` | 历史运行记录，路径按运行时语境保留 |

2026-09-20 将 `nav.json` 移至 [analysis/surveys/nav.json](../../analysis/surveys/nav.json)，不再在来源库维护重复导航。七份 Markdown 只移除了我方导航并补充转换声明，分隔线后的正文与 [重建前快照](../../archive/2026-09-20-architecture-review-before/sources/papers/surveys/README.md) 中对应文件逐字节一致。本轮没有重下载或重新解析这些论文。

现有 PDF 的 arXiv 版本、原获取时间和实际转换环境缺失，明确记为 unknown / `null`；当前文件指纹不是来源真实性证明，也不是旧 PDF 与旧元数据同版的证明。

## 编号与日期的核验

2026-09-21 新增的 20 份材料的 arXiv 编号、首次与最新修订日期、以及 venue 线索，均用官方接口核对过，脚本为 [_scripts/check_arxiv.py](_scripts/check_arxiv.py)。它只读取并返回接口字段，核验不到的项输出 `NOT-FOUND` 或 `ERROR`，不推测。同批下载还修复了 [download_arxiv.py](_scripts/download_arxiv.py)：arXiv 的 abs 页改版后 `citation_pdf_url` 不再带版本号，脚本会走到"版本未解析"分支；现在解析失败时改从官方接口取得显式版本，再按该版本分别取元数据与 PDF。

## 继续下载与转换

在本目录运行，`<python>` 替换为本机 Python；执行转换需要安装 `pymupdf4llm` 的环境。

```text
<python> _scripts\download_arxiv.py --all
<python> _scripts\download_arxiv.py 2512.13564v2
<python> _scripts\pdf2md.py
<python> _scripts\pdf2md.py --out engineering 2512.13564v2
```

下载工具遇到已有 PDF 时同时保留旧元数据，不拿新元数据拼旧 PDF。下载新文件时先确定一个明确版本，再从该版本分别取得元数据与 PDF；无法确定版本或任一步失败，就保留现有记录。要下载不同版本，核对目标后使用带 `vN` 的编号，得到独立文件；工具不自动回退到 `v1`。

转换工具保留现有非空文件，只有显式 `--force` 才重转。新转换记录 PDF SHA256、解析器版本、转换时间和正文指纹；检测到 PDF 与已记录指纹不一致时停止，先调查来源变化。转换不会加入我方阅读卡片。PDF 的表格、公式、图像和关键摘录仍需在使用时核对。
