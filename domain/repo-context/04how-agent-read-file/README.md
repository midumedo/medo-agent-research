# 04 · harness 的 read 工具与 skill 加载工具

> 属于 `domain\repo-context\` 研究，阶段 **04how-agent-read-file**
> 上游：`domain\repo-context\README.md`（研究纲领末节）、`domain\repo-context\02docsdefine\ds.md`（11 仓命名实测）
> 产出者：ds（AI 生成，见 `domain\repo-context\AGENTS.md` 的命名约定）

## 这一阶段回答什么

纲领末节问的是「终究是落地到 harness 怎么读的」：**harness 到底用什么工具读文件、怎么把 skill 装进上下文**，以及——**这些代码哪些是开源的、开在哪里**。

本目录只做一件事：把「read 工具」与「skill 加载」两个能力的**源码事实**逐对象钉住，并给出一张可增行的索引。不做 token 耗费与模型理解的量化实验（那需要独立实验设计）。

| 文件 | 内容 |
|---|---|
| `README.md`（本文件） | 范围、方法、证据边界、索引字段口径 |
| `ds.md` | 主研究稿：逐对象拆解、横向对照、开源形态判定 |
| `index.csv` | 索引本体：一行一个对象，11 列 |

## 方法：三条取证通道，只有两条能用

| 通道 | 状态 | 说明 |
|---|---|---|
| `grep`（显式路径）/ `ast_grep` | 可用 | `sources/repos/**` 被 `.gitignore` 的 `/sources/repos/` 排除，`read_file` 硬拒、`glob` 静默返回空；这两个工具对**显式路径/子树**仍可读 |
| `bash`（curl / npm / find / grep -r） | 可用 | 与 `web_fetch` 走不同通道，本环境**未被拦**——第三方 checkout 的下载与全树检索都靠它 |
| `web_fetch` / `web_search` | **不可用** | `web_fetch` 对任何外域返回 `Access denied: ... resolves to a private/reserved IP (198.18.x.x)`；`web_search` 返回与查询无关的页面 |

**这条边界决定了本文的行文纪律**：凡是「某 harness 开源了某文件、路径在哪」的断言，只有两种合法来源——本地已有 checkout，或本轮**实际下载**的 checkout；两者都没有的，一律写 `unverified`，不允许用模型记忆或检索摘要填充。

## 索引字段口径（`index.csv`）

| 列 | 含义 |
|---|---|
| `harness` | 本地目录名或产品名 |
| `repo` | 上游仓库标识；闭源写 `—（闭源）` |
| `license` | 只写实际读到的 LICENSE 首行结论；没读到的写 `未记录` |
| `kind` | `coding-harness` / `capability-cli` / `memory-library` / `app-only-repo` / `closed-binary` / `closed-client` |
| `read_tool` | **面向模型**的工具名；没有专用工具写 `（无）` |
| `read_impl` | 实现文件与主入口行号；路径相对该对象自己的仓库根 |
| `read_limits` | 只写源码里读得到的常量与语义，不换算 token |
| `skill_mechanism` | 加载器（哪种发现/注入策略）／仅发布 SKILL.md／无 |
| `skill_impl` | 加载器或 SKILL.md 所在路径 |
| `evidence` | 可复现的定位：file:line、命令、或下载时的 sha＋日期 |
| `status` | **只取三值**，见下 |

`status` 三值（缺一不可的字面区分）：

- `verified`——本轮由我本人用 grep/ast_grep/bash 取得证据。
- `absent`——在**该仓整树**内，7 类关键词（`read_file`、`read_files`、`str_replace_editor`、`view_image`、`SKILL.md`、`load_skill`、`skill_loader`）**零命中**。这是「检索范围内未见」，**不是**「该仓库不存在此能力」。
- `unverified`——没有一手证据（下载失败、闭源且无法访问）。**下游不得引用**。

## 几个容易误读的点

1. **`sources/repos/` 的提交指纹不完整**。`sources/repos/_commits.json` 只记了 7 个记忆框架的 sha；codex、Raven、Tianshu-harness、deepseek-harness、minimax-cli 五个**没有指纹记录**，因此对它们的断言必须带「该 checkout 版本」限定，不能写成产品当前行为。
2. **`sources/repos-sources.md` 里的 `cli/` 行已过期**——磁盘上是 `minimax-cli/`。
3. **`_partial-goose-dl-failed-20260924/` 是废料**：goose 的 tar.gz 在 900s 超时后只解压了一部分，目录内文件齐但不完整。不要引用它，也不要 `git add`（该目录本就在 `.gitignore` 内）。
4. **记忆库不是「与本题无关」**：mem0 发布 56 个 SKILL.md、MemOS 7 个、EverOS 5 个、MemoryBear 自建 `load_skill_tools`。它们扮演的是 skill 的**生产/消费方**，不是 harness。
