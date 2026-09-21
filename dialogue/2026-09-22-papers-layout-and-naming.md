# 2026-09-22：论文库扁平化、词干命名与两层 AGENTS

本轮由用户对 `sources/` 结构的四点意见发起：MinerU 可直接用云端 API（`MINERU_APIKEY` 已在用户环境变量）、论文命名的取舍、取消 `papers/` 下的类型分级目录、以及给 `sources/` 与 `sources/papers/` 各写一份 AGENTS.md。记录选择理由，不重复规则正文。

## 做了什么

1. **取消类型分级目录**。`surveys/`、`benchmarks/`、`frameworks/` 三个目录合并进 `md/`；`pdf/` 保留，新增 `json/` 与按需的 `assets/`。类型不再是目录，改记在 [INDEX.md](../sources/papers/INDEX.md) 的「类型」列与 md 的 front matter，可多值、可在复核后改写。
2. **文件名改为词干 `<registry>-<native-id>`**。27 份材料由裸编号 `2504.19413` 改为 `arxiv-2504.19413`；版本不进文件名。
3. **新增 [sources/papers/INDEX.md](../sources/papers/INDEX.md)**：上半是当前清单（标识、标题、类型、版本、各表示形式是否齐备、入库日期），下半是只追加的入库与修订日志。
4. **新增 [sources/AGENTS.md](../sources/AGENTS.md) 与 [sources/papers/AGENTS.md](../sources/papers/AGENTS.md)**，并把 `papers/README.md` 压缩成人看的入口说明。
5. **脚本改为词干驱动**：新增 `_scripts/stem.py` 作为唯一标识与路径来源；`download_arxiv.py`、`pdf2md.py`、`mineru_client.py` 全部接受词干并写入新目录；新增 `_scripts/mineru_cloud.py` 走 MinerU 云端 API。
6. 全项目 10 个文件里的旧路径链接已改；`_scripts/test_pipeline.py` 同步更新，9 项回归检查通过。

## 命名：为什么是编号，为什么不带标题

文件名在这个库里同时是**跨目录的路由键**和**被 `analysis/`、`deepdive/`、`domain/` 引用的锚点**，所以它的优化目标是稳定与可推导，不是好看。

- **不用标题**：标题是论文最容易变的字段。标题进文件名后，每次 arXiv 修订都变成一次改名，会静默打断所有指向它的链接；标题还长、会撞名、带标点与大小写，slug 化必然有损，两个人收录同一篇会得到两个文件。
- **不用裸编号**：这个领域的材料不都有 arXiv 号，只发在自己官网的那批没有号可用；裸编号也不说明该去哪个登记处核验。
- **不用「编号+标题」**：两种成本都付，好处一个没有——标题那半从不参与路由却最先腐烂，而且它让文件名不可推导。**不可推导的方案不是命名规则，只是命名习惯**，这是它被否掉的决定性理由。
- **标题放在哪**：INDEX.md 的标题列 + md 的 front matter。认不出某个标识是哪篇就查 INDEX，不靠猜也不改名。
- **版本不进文件名**：版本是文件的状态，不是论文的身份。版本进文件名会让每次修订凭空造出第二个身份，并把已写的阅读笔记分裂成两份。需要并存对比时放 `variants/`，不进 `pdf/`、`md/`。
- **registry 前缀**：`arxiv` / `openreview` / `acl` / `doi` / `web` / `repo` 是封闭集合。没有登记号、只发在自己官网的论文用 `web-<年>-<机构>-<短 slug>`，slug 在收录那一刻冻结——以后发现官方标题不同也不改文件名。

## 目录：为什么按表示形式分，而不是合并

用户先提出「反正有后缀能区分，不如合并」，随后自己决定分开。分开的实质理由不是整洁：

- **一层目录只表达一件事**。`pdf|md|json` 是表示形式；语义全部交给 INDEX 与 front matter。类型目录会把一个可改、可多值的判断写死进路径——一篇论文既是基准又提出框架时，目录逼你二选一。
- 分开后可以按格式区别处理（二进制与文本的 git 属性不同），也能用 `pdf/` 与 `md/` 的差集直接看出哪些还没转换。
- 同名词干路由在两种布局下都成立，所以这个选择纯粹是操作层面的，而操作层面分开更划算。

MinerU 云端返回的是 zip（`full.md` + `*_content_list.json` + `images/`），所以拆包规则也写进了 AGENTS.md：`full.md` → `md/`，content_list → `json/`，图片只在当次任务真的需要时才落进 `assets/`（默认不落，避免几百张图进版本库）。

## INDEX.md 放在 `papers/` 而不是 `sources/`

`repos/` 不进版本库，所以它的索引只能放在 `sources/` 这一层；`papers/` 是受版本控制的，索引放在它自己里面更符合「索引紧邻被索引的数据」。嵌套 AGENTS.md 也按子目录加载，`papers/AGENTS.md` 与 `papers/INDEX.md` 同级，进入子树即可见。

## MinerU：云端为主，本地为备

云端（`/api/v4/file-urls/batch` 上传 + `/api/v4/extract-results/batch/{batch_id}` 轮询）不用装模型，每天有免费页数额度。因为还有**每日任务数**上限（错误码 `-60018`），`mineru_cloud.py` 把一次给出的多个词干合成**一个**批量请求提交。`MINERU_APIKEY` 取不到时会回退读 Windows 用户环境变量的注册表值——用户变量对设置之前启动的进程不可见，这是最常踩的坑。本地服务版本 `mineru_client.py` 保留为备选。

## 顺带处理的三件事

- 首批七份 md 原以 CRLF 入库，`.gitattributes` 里有一条 `sources/papers/surveys/*.md -text` 专门保留。迁移后路径失效，且这七份与其余二十份换行不一致会妨碍后续处理，于是归一为 LF 并移除该规则；逐字节比对确认内容未变（差异只在 `\r`）。provenance 里的正文指纹在写入前计算，与文件换行无关。
- `pdf2md.py` 的 `--out surveys|benchmarks|frameworks` 是「把类型写进命令」的残留，已删除，输出固定在 `md/`；类型改由 `--kind` 写进 front matter。
- 托管 Python 环境缺 `pymupdf4llm`，已装；不装则 `pdf2md.py` 与一项回归检查无法运行。

## 未完成

- `json/` 目前只有占位文件：现有 27 份都是 `pymupdf4llm` 转换的，没有结构化输出。需要表格或公式定位时，对具体某篇跑一次 `mineru_cloud.py` 即可补齐。
- 首批七份的来源版本与获取时间仍为 unknown，INDEX 里如实记着；补齐需要对每篇单独核对 PDF 与 arXiv 版本。
