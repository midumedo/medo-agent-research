# 本地第三方仓库与来源版本

> 2026-09-21 建立，2026-09-24 增补。`sources/repos/` 下的第三方 checkout **不进入版本库**（`.gitignore` 排除），因此在这里记录每个仓库的来源标识，避免"本地有一份代码"被当成"已核对过版本"。
> 记录的是获取当日的仓库默认分支最新提交；之后上游会继续变化，引用具体代码前请重新核对。

## 获取方式

GitHub 的 git 协议在本环境很慢，这里改用打包下载（`codeload.github.com` 的 tar.gz），因此本地 checkout **不含 `.git` 历史**。提交指纹由 GitHub API 单独取得，与落盘代码的对应关系以"获取当日默认分支最新提交"为准，不保证逐文件一致。

2026-09-24 增补的四个仓库走同一条路径：`curl -sL https://codeload.github.com/<owner>/<repo>/tar.gz/refs/heads/main`，解压用 `--strip-components=1`；逐条指纹另记在 `sources/repos/_commits.json`。

## 清单

| 本地目录 | 仓库 | 分支 | 提交（前 12 位） | 提交日期 | 获取日期 |
|---|---|---|---|---|---|
| `mem0/` | mem0ai/mem0 | main | a39a802bbc93 | 2026-09-18 | 2026-09-21 |
| `memU/` | NevaMind-AI/memU | main | 08e1ed4cdf4c | 2026-09-10 | 2026-09-21 |
| `MemoryBear/` | SuanmoSuanyangTechnology/MemoryBear | main | c32b937f1ed0 | 2026-09-16 | 2026-09-21 |
| `vanilla-rag-memory/` | wenxiaof345-ctrl/vanilla-rag-memory | main | 31ab7bf9cfa3 | 2026-08-11 | 2026-09-21 |
| `ReFind/` | imlrz/ReFind | main | a80175ca0eeb | 2026-08-14 | 2026-09-21 |
| `MemOS/` | MemTensor/MemOS | main | 12acdad694d0 | 2026-09-21 | 2026-09-21 |
| `EverOS/` | EverMind-AI/EverOS | main | 5076683ab88d | 2026-09-08 | 2026-09-20 |
| `Raven/` | EverMind-AI/Raven | — | 未记录 | — | 2026-09-20 |
| `Tianshu-harness/` | huiliyi37/Tianshu-harness | — | 未记录 | — | 2026-09-20 |
| `minimax-cli/` | MiniMax-AI/cli | — | 未记录 | — | 2026-09-20 |
| `codex/` | openai/codex | — | 未记录 | — | 2026-09-20 |
| `deepseek-harness/` | deepseek-ai/deepseek-harness | — | 未记录 | — | 2026-09-20 |
| `gemini-cli/` | google-gemini/gemini-cli | main | bedef96ef429 | 2026-09-24 | 2026-09-24 |
| `qwen-code/` | QwenLM/qwen-code | main | ffea2d024e52 | 2026-09-24 | 2026-09-24 |
| `cline/` | cline/cline | main | dd2e190e5c55 | 2026-09-24 | 2026-09-24 |
| `OpenHands/` | All-Hands-AI/OpenHands | main | 未取得（API 限流） | — | 2026-09-24 |

`Raven/`、`Tianshu-harness/`、`minimax-cli/`、`codex/`、`deepseek-harness/` 是更早轮次获取，提交指纹当时未记录；使用它们时先补上来源标识，不要凭目录名假定版本——引用其代码行为时必须写成"该 checkout 版本如此"。

2026-09-24 更正：清单此前记的 `cli/`（"编码 Agent CLI，来源待补"）在磁盘上实际是 `minimax-cli/`，即 `MiniMax-AI/cli`（MIT，MiniMax 平台能力 CLI，`README.md:4`）。

## 未完成的获取

- `goose/`（`block/goose`）：2026-09-24 尝试下载，tar.gz 在 900s 超时后仅部分解压。**该目录是废料，不得引用**，已隔离为 `_partial-goose-dl-failed-20260924/`。

## 使用规则

- 引用代码行为时写 **commit + 文件路径 + 函数/类**，不写"mem0 会……"这类没有定位的说法。
- 区分四种状态：代码里确实存在、文档或 README 声称、默认是否启用、本项目是否实际验证。
- 打包下载不含历史，无法用 `git log`/`git blame` 追溯；需要历史时另行 clone。
- 外部依赖（如 EverOS 依赖的 PyPI 包 `everalgo`）不在本地，其算法实现不可读——这类缺口要明说，不能当作已核对。
- `sources/repos/` 被 `.gitignore` 排除，`read_file`/`glob` 对其一律拒读；取证只能用 `grep`（显式路径）、`ast_grep` 或 `bash`。
