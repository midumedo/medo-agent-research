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
- 2026-09-25 · 抓取 · `EverOS` · `EverMind-AI/EverOS`（462ebf9fd59b），旧快照存为 `EverOS@5076683ab88d/`。
- 2026-09-25 · 抓取 · `MemOS` · `MemTensor/MemOS`（a7367d07e55d），旧快照存为 `MemOS@12acdad694d0/`。
- 2026-09-25 · 抓取 · `MemoryBear` · `SuanmoSuanyangTechnology/MemoryBear`（85004dacaf2f），旧快照存为 `MemoryBear@c32b937f1ed0/`。
- 2026-09-25 · 抓取 · `OpenHands` · `All-Hands-AI/OpenHands`（c17fc6538d57），旧快照存为 `OpenHands@unknown-2026-09-25/`。
- 2026-09-25 · 抓取 · `Raven` · `EverMind-AI/Raven`（e17694113b13），旧快照存为 `Raven@unknown-2026-09-25/`。
- 2026-09-25 · 抓取 · `Tianshu-harness` · `huiliyi37/Tianshu-harness`（79c10d30ba4f），旧快照存为 `Tianshu-harness@unknown-2026-09-25/`。
- 2026-09-25 · 抓取 · `codex` · `openai/codex`（75e0e0aad97a），旧快照存为 `codex@unknown-2026-09-25/`。
- 2026-09-25 · 抓取 · `mem0` · `mem0ai/mem0`（989c7da0fc8e），旧快照存为 `mem0@a39a802bbc93/`。
- 2026-09-25 · 抓取 · `memU` · `NevaMind-AI/memU`（2c050bc9681a），旧快照存为 `memU@08e1ed4cdf4c/`。
- 2026-09-25 · 抓取 · `minimax-cli` · `MiniMax-AI/cli`（33453cf12392），旧快照存为 `minimax-cli@unknown-2026-09-25/`。
- 2026-09-25 · 抓取 · `qwen-code` · `QwenLM/qwen-code`（d124dd56cd0a），旧快照存为 `qwen-code@ffea2d024e52/`。
- 2026-09-25 · 抓取 · `deepseek-harness` · `deepseek-ai/deepseek-harness`（477b4f420553），旧快照存为 `deepseek-harness@unknown-2026-09-25/`。
- 2026-09-25 · 全量更新 · 17 个当前快照 · 11 个仓库上游有新提交：`EverOS`（462ebf9fd59b）、`MemOS`（a7367d07e55d）、`MemoryBear`（85004dacaf2f）、`OpenHands`（c17fc6538d57）、`Raven`（e17694113b13）、`Tianshu-harness`（79c10d30ba4f）、`codex`（75e0e0aad97a）、`mem0`（989c7da0fc8e）、`memU`（2c050bc9681a）、`minimax-cli`（33453cf12392）、`qwen-code`（d124dd56cd0a）；`ReFind`、`ZCode`、`cline`、`gemini-cli`、`goose` 未动（sha 未变，脚本直接跳过，没白下）。旧快照全部按规则改名保留为 `<id>@…/`，账本因此新增 11 行历史行——**代价要说清**：11 个仓库的源码引用行号随之位移（如 Tianshu-harness 的 `READ_FILE_TOOL` 从 `:723` 移到 `:711`），`domain/repo-context/04how-agent-read-file/` 里的锚点已逐条重新对齐。
- 2026-09-25 · 修复 · `fetch.py` · 分支名写死 `main`，而 `deepseek-ai/deepseek-harness` 的默认分支不是它——第一次全量更新时 404（旧快照已自动回位，没有留下半新半旧的树）。改为先向 API 问 `default_branch`、取不到才回落 `main`，重抓成功（`477b4f420553`）。
- 2026-09-25 · 修复 · `build_index.py` + `repos.py` · `<id>@unknown-<日期>` 这种「落盘时没记指纹」的历史快照行，`split_id` 因后缀非十六进制而把整串当成 id，于是这些行既进不了历史分支、也拿不到 `snapshot-unknown` 标记，交付门一直报「有本地目录却没有 snapshot」。新增 `repos.base_of()` 只按 `@` 切分，两个问题一起消解。
- 2026-09-25 · 抓取 · `ReFind` · `imlrz/ReFind`（a80175ca0eeb），覆盖原有快照。
- 2026-09-25 · 结构 · 全库 · **取消多版本副本**。删除 12 个历史快照目录（`<id>@…/`，约 2G）与对应账本行（30 → 18 行）。理由：研究不需要同一仓库多版本并存——要「现在这一版是什么」就够，真要比某个历史版本，按引用里的 sha 用 codeload 重现即可，不值得在本地囤一棵旧树。`fetch.py` 同步改为**就地覆盖**（先落 `<id>.incoming/`，确认完整再换上去，失败的下载不会搭进原有那棵树）；`build_index.py` 的历史行分支与 `repos.py` 的 `split_id`/`base_of` 一并拆除，不留死代码。版本记录仍由各行 `snapshot` 的 sha 承担——它是一列字符串，不是一份副本。
