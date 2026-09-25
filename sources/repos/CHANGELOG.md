# CHANGELOG · 第三方仓库快照

只追加，不删改；最新在下。它记「什么时候抓了什么、改了什么」，不重复 `index.csv` 里的数据。
抓取日期属于**事件**，只在这里；账本里对应的是 `snapshot` 的 sha（版本身份）。

- 2026-09-20 · 入库 · 5 个 · `Raven`、`Tianshu-harness`、`minimax-cli`（当时台账记作 `cli/`）、`codex`、`deepseek-harness` 落盘。**落盘时未记提交指纹**，这五个的 `snapshot` 至今为空，账本以 `snapshot-unknown` 标记。
- 2026-09-20 · 入库 · 1 个 · `EverOS`（`5076683ab88d`）。
- 2026-09-21 · 入库 · 6 个 · `mem0`（`a39a802bbc93`）、`memU`（`08e1ed4cdf4c`）、`MemoryBear`（`c32b937f1ed0`）、`vanilla-rag-memory`（`31ab7bf9cfa3`）、`ReFind`（`a80175ca0eeb`）、`MemOS`（`12acdad694d0`）。
- 2026-09-24 · 入库 · 4 个 · `gemini-cli`（`bedef96ef429`）、`qwen-code`（`ffea2d024e52`）、`cline`（`dd2e190e5c55`）、`OpenHands`（sha 未取到——GitHub API 限流）。抓取路径：`codeload.github.com` 的 tar.gz，解压用 `--strip-components=1`。
- 2026-09-24 · 失败 · `goose` · `block/goose` 的 tar.gz 在 900s 超时后只解压了一部分，目录内文件齐但不完整。隔离为 `_partial-goose-dl-failed-20260924/`，**不建账本行**，`scan.py` 跳过它。
- 2026-09-24 · 更正 · `minimax-cli` · 台账原记 `cli/`（"编码 Agent CLI，来源待补"），实为 `MiniMax-AI/cli`（MIT，MiniMax 平台能力 CLI，非 harness）。
- 2026-09-25 · 结构 · `.gitignore` · 根规则由 `/sources/repos/` 改为 `/sources/repos/*`。前者把目录本身排除，git 不会下降进来，内层 `.gitignore` 的否定规则全部失效——`git check-ignore -v sources/repos/index.csv` 曾报告 `.gitignore:2:/sources/repos/`。改后只跟踪 `.gitignore`、`index.csv`、`_commits.json`、`CHANGELOG.md`、`AGENTS.md`、`_scripts/**`；`_scripts/**` 之外另加 `__pycache__/` 收回规则，避免字节缓存入库。
- 2026-09-25 · 立账 · 全库 · 新建 `index.csv`（六列：`id`/`repo`/`kind`/`keywords`/`completeness`/`snapshot`）与 `_scripts/`（六步：`repos`/`fetch`/`scan`/`build_index`/`status`/`pipeline`）。`_commits.json` 由 11 条补到 16 条——补上那 5 个目录的 `slug`，`sha` 仍为空（没有指纹就是没有，不拿今天的 main 冒充落盘版本）。
- 2026-09-25 · 退役 · `sources/repos-sources.md` · 手工台账删除。清单进 `index.csv`、事件进本文件、使用规则与逐仓说明进 `AGENTS.md`。理由：它的清单与账本重复、日期与本文件重复，而两份来源不一致时以谁为准没有规定——它确实已经腐坏过一次（`cli/`）。
- 2026-09-25 · 抓取 · `ZCode` · `zai-org/ZCode`（29628c9acdb8）。
- 2026-09-25 · 抓取 · `vanilla-rag-memory` · `wenxiaof345-ctrl/vanilla-rag-memory`（31ab7bf9cfa3），旧快照存为 `vanilla-rag-memory@31ab7bf9cfa3/`。
- 2026-09-25 · 抓取 · `goose` · `aaif-goose/goose`（61830521ad31）。
- 2026-09-25 · 迁移 · `goose` · 上游由 `block/goose` 迁到 `aaif-goose/goose`，按新地址重抓（`61830521ad31`，349MB）。9-24 那次 900s 超时留下的 `_partial-goose-dl-failed-20260924/` 随之删除——它的存在只在本文里留痕，不再占磁盘。
- 2026-09-25 · 移除 · `vanilla-rag-memory` · 按用户判断（项目过冷门、不值得占样本位）连同历史快照一起删除：目录两处、账本两行（含 `vanilla-rag-memory@31ab7bf9cfa3`）、`_commits.json` 一条同时清掉。9-21 的入库记录保留在上方，不抹掉曾经收过它这件事。
- 2026-09-25 · 修复 · `_commits.json` · `fetch.py` 是「读-改-写」：下载动辄几分钟，这段时间里对账本的其它修改会在它落盘时被静默覆盖。实测——删掉的 `vanilla-rag-memory` 被 goose 那次抓取写了回来。这是并发写同一账本的结构缺口，尚未在代码里加锁，使用时避免「一边抓取一边改账本」。
