---
name: pdf2md
description: 将搜索发现的论文、给定链接或本地 PDF 保存为可直接阅读和检索的 Markdown，保留原始 PDF 与图表。需要深入阅读论文全文、核查方法与实验、收藏研究材料，或继续阅读和校对本地论文时使用。
---

# pdf2md：从论文发现到本地全文

让值得研究的论文成为可阅读、可核对、可复用的本地材料。Agent 负责选文、阅读与判断，脚本负责获取、转换和维护文件关系。

## 取得材料，尽早开始读

只有主题或标题时，用可用的搜索工具定位论文与原文来源；已有搜索结果时承接编号或 PDF 链接。依据标题、摘要和研究问题选择需要读或保存的论文。资料库有 `index.csv` 时先按名称和关键词筛选，再用 `metadata` 读取候选摘要，按问题继续读正文。查明本地是否已有同一论文及所需版本，有可读材料就复用。

`<skill>` 替换为本 skill 的绝对路径，`<资料库>` 使用项目已有或任务指定的论文目录。下面用一篇 arXiv 论文示例：

```text
python "<skill>/scripts/pdf2md.py" metadata 2501.13956v1
python "<skill>/scripts/pdf2md.py" download 2501.13956v1 --root "<资料库>" --name "Project.Zep"
python "<skill>/scripts/pdf2md.py" convert "<资料库>/pdf/arxiv-2501.13956v1.Project.Zep.pdf" --lang en
```

`metadata` 获取来源标题与摘要，供筛选和命名。`download` 保存 PDF，加 `--convert` 可接着转换。仅保存原文时下载即可；导入已有外部 PDF 时用 `convert "<PDF 路径>" --root "<资料库>"`，原件保留。

下载后即可读 PDF，不必等待转换。命令工具支持持续运行时，让转换继续，同时阅读 PDF、同版本原文 HTML 或其他材料；Markdown 就绪后接着读。转换命令会轮询云端结果，保留运行会话和输出的 `batch_id`。等待超时或结果下载失败时，用原 PDF 和 `convert --batch-id "<批次>"` 续取；`--timeout` 仅限制轮询等待。按需查 [批次续取与网络诊断](references/mineru-network.md)。

普通 PDF 链接若分步下载、转换，保留下载输出中的来源 URL，并在转换后补入 MD 顶部的 `source` 字段；同次 `download --convert` 会传递这份来源信息。只保存 PDF 时，把来源随本次研究记录保存。

## 围绕问题阅读与核对

用文件读取和 `rg` 定位 Markdown 中的方法、实验、附录或待核查表述，再读相邻上下文。根据研究问题决定阅读范围，区分论文表述、实验依据与自己的推断。

```text
rg -n '^#{1,3} |ablation|limitations' "<资料库>/md/<论文名>.md"
uv run --script "<skill>/scripts/pdf_read.py" "<资料库>/pdf/<论文名>.pdf" --find "附近一段完整短语"
uv run --script "<skill>/scripts/pdf_read.py" "<资料库>/pdf/<论文名>.pdf" --pages 2-3
uv run --script "<skill>/scripts/pdf_read.py" "<资料库>/pdf/<论文名>.pdf" --pages 3 --render "<临时目录>"
```

PDF 页码按文件位置从 1 开始。短语未命中时换附近文字或查看页面；具体数字、公式、表格、图示及转换疑点按需回 PDF 核对，文本层不能确认的内容看渲染页。

确认转换错误后直接编辑 MD，保留来源含义与表格、公式、代码、图片结构。重复且含义一致的问题可以批量替换，再核对差异。需要校对时读 [转换疑点核对](references/conversion-checks.md)。

## 保存与维护

- 新名称依据来源标题与完整摘要，默认 `<来源编号及版本>.<类型>.<简称>`，如 `arxiv-2501.13956v1.Project.Zep`。类型按贡献选 Survey、Bench、Project、Model、Method 等，简称优先作者自称。用户命名优先，已有材料沿用现名，按任务需要改名。
- 已知来源与版本随材料保留；缺失信息留空，Agent 概括不能填成来源摘要。
- 目录为同名 `pdf/<论文名>.pdf`、`md/<论文名>.md` 与平铺 `assets/`，MD 引用 `../assets/...`。保留转换返回的全部内容图片，包括正文未引用的裁图；资产以前缀区分归属，有来源编号时用编号，否则用文件名。
- `rename` 联动 PDF、MD、资产和已有索引，**新名称必须包含已有来源编号**；只有下载时的 `--name` 会补 arXiv 编号。外部研究文稿中的引用由 Agent 按任务范围更新。
- 已有 MD 仅缺 PDF 时，确认同一来源与版本后补下载。完整转换件默认跳过，确需重转才用 `--force`；部分失败只处理失败项，整库转换用 `--root "<资料库>" --all`。

```text
python "<skill>/scripts/pdf2md.py" rename "<资料库>/md/arxiv-2501.13956v1.Project.Zep.md" "arxiv-2501.13956v1.Project.ZepMemory"
python "<skill>/scripts/pdf2md.py" check "<资料库>/md/<论文名>.md"
```

`check` 检查原件、正文和正文引用的本地图片；它不能确认未引用裁图是否缺失，也不判断论文内容正确性。

## 索引管理

`index.csv` 保存选定资料的身份、名称与检索线索，包含尚未下载的候选。单篇阅读无需建索引；持续积累资料时使用。全文摘要保留在 MD 顶部，阅读判断写研究笔记。

| 字段 | 含义与维护 |
|---|---|
| `id` | 来源编号及已知版本；未知留空，不推断成线上最新版 |
| `name` | 有 `id` 时为类型与简称，无 `id` 时为完整文件名主体；二者组成 PDF/MD 的同名文件名 |
| `keywords` | Agent 根据来源摘要和研究关注点选择的检索词，沿用库内一致用词，以 `;` 分隔 |
| `revised` | 所用论文版本的来源修订日，格式 `YYYY-MM-DD`；未知留空，不填下载日或本地修改日 |

已有索引时，新增下载、实际转换和改名会维护本次资料的记录。缓存命中或完整转换件跳过时不补录；首次创建或扫描补录本地文件，显式运行不带操作参数的 `index --root`。待下载候选可直接在 CSV 补一行；已有本地文件的名称通过 `rename` 修改。

对账保留已有关键词（包括空值）与非空修订日，只从 MD 登记块补缺失日期、为新记录取得字段。下载时已获得的来源修订日也会补入空日期。关键词以 CSV 中的选择为准；用 `--set-keywords` **替换整组**并同步对应 MD，空字符串表示清空。修正已登记的日期时依据来源编辑 CSV，并同步已有 MD 的 `revised`。

```text
python "<skill>/scripts/pdf2md.py" index --root "<资料库>" --list
python "<skill>/scripts/pdf2md.py" index --root "<资料库>"
python "<skill>/scripts/pdf2md.py" index --root "<资料库>" --missing-keywords
python "<skill>/scripts/pdf2md.py" index --root "<资料库>" --set-keywords "<编号或名称>" "memory;agent"
python "<skill>/scripts/pdf2md.py" index --root "<资料库>" --check
```

`--list` 和 `--missing-keywords` 只读已保存的索引，没有索引时返回空列表。后者附本地标题与摘要，供 Agent 判断关键词；缺摘要时再定向取得来源，暂不凭名称猜词。单篇关键词修改只登记目标资料，不顺带收录其他文件。

默认对账保留本地缺文件的记录。同一来源与版本出现多个名称时，核对重复材料后再整理，脚本不替 Agent 选一份。只有任务明确要求移除所有离线记录时才用 `--prune`：它删除 PDF、MD 均不在本地的行，也会删除待下载候选。

`index --check` 只读检查登记是否需要对账，忽略行顺序等格式差异；离线记录可以通过。核对资料齐备性用 `check`，是否读过或结论可靠由实际研究记录说明。

## 运行与交付

下载与转换脚本只用 Python 3.10+ 标准库；PDF 读取脚本在头部声明 PyMuPDF，`uv run --script` 为它准备依赖，已有带 PyMuPDF 的解释器也可直接运行。资料相对路径按当前工作目录解析。

MinerU 凭据为 `MINERU_APIKEY`：先读进程变量，未设置时 Windows 可读用户环境变量，显式空值禁用回退。脚本不自动读取 `.env`。转换默认使用 `vlm`；本地参数看子命令 `--help`，服务端参数、额度与错误码查 [官方 API 文档](https://mineru.net/apiManage/docs)。

原文与转换件放资料库，研究判断写入任务对应的笔记。页图、临时片段和一次性查询使用系统临时目录；需要长期引用的证据随研究保存。

完成后给出论文身份、本地材料位置和读到的具体内容，并说明保存、转换、阅读与核对的实际进度。
