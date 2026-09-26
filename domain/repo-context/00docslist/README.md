# 00 · docslist —— `sources/repos/` 根目录文档实测账本

> 属于 `domain\repo-context\` 研究，阶段 **00docslist**
> 产出者：ds（AI 生成，见 `domain\AGENTS.md` 的命名约定）
> 上游：`domain\repo-context\docslist.md`（人手写的候选名字清单）、`domain\repo-context\初步研究计划.md`
> 下游：`01docsclassify`（分类法）、`02docsdefine`（文档类型定义与重判）、`03docscompare`（相似文档对比）

## 这一阶段回答什么

两个问题，分开回答，不互相顶替：

- **Q1 纵向**：`sources/repos/` 里**某一个仓库**的根目录文档治理究竟长什么样？→ 读 `ds\{id}.md`（一仓一份）。
- **Q2 横向**：18 个仓库之间，**哪些命名是活的、哪些是纸面的**？→ 过滤 `index.csv`。

本阶段**只做实测与枚举**：登记真实存在的文件、它们的字节数与角色、以及每条断言的取证方式。分类法归 `01`，类型定义归 `02`，相似文档的取舍归 `03`。本阶段对它们唯一的贡献是**可机械核对的实例账本**。

`docslist.md` 是**意图**（用户想到过哪些名字），不是结论；`具体md文件的初步分析-by-ai.md` 是**历史草稿**（自述含幻觉风险）。两者的实测归宿都在本目录的 `index.csv` 与 `ds\`。

---

## 方法边界（本轮实测，不是推测）

`sources/repos/` 被 `.gitignore` 的 `/sources/repos/` 排除，这决定了每个工具能用还是不能用。下表全部来自本轮实测：

| 通道 | 状态 | 证据 |
|---|---|---|
| `bash`（find / wc / cmp / grep -r） | **可用** | `find sources/repos -maxdepth 1 -type f` 正常返回 |
| `repo_map` | 可用（plan 阶段唯一能递归枚举的通道） | `repo_map({path:"sources/repos/Raven", depth:0})` 完整列出 26 个根文件 |
| `read_file` | **不可用** | `Error: File is gitignored`（`sources/repos/AGENTS.md`、`sources/repos/deepseek-harness/AGENTS.md` 两次独立命中） |
| `glob` | **静默返回空** | `glob("sources/repos/*")` → 未找到匹配；`glob("sources/**/*.md")` 结果不含 `repos/` 下任何文件 |
| `grep`（显式文件路径） | 可用 | `grep(path:"sources/repos/Raven/AGENTS.md")` 正常返回行与行哈希 |
| `grep`（目录） | **只覆盖该目录的直接子文件，不递归** | 见下方「假阴性陷阱」 |
| `web_fetch` / `web_search` | 本环境外域被 DNS 层拦截 | 见 `domain\repo-context\04how-agent-read-file\README.md` 的取证边界表 |

### 假阴性陷阱（本阶段确立的纪律）

本环境 `grep` 的**目录**检索不递归，只命中该目录的直接子文件。三处交叉实测：

1. `grep(path="sources/repos", glob="*.md", pattern="^# ")` 只返回 `sources/repos/AGENTS.md`、`sources/repos/CHANGELOG.md`，未返回任何子目录文件。
2. `grep(path="sources/repos/deepseek-harness", pattern="Alternatives considered")` → 未找到匹配；而该串确实存在于 `sources/repos/deepseek-harness/.agents/notes/README.md`。
3. `grep(path="sources/repos/Tianshu-harness/docs", pattern="rivet/plans")` → 未找到匹配；而该串确实存在于 `sources/repos/Tianshu-harness/docs/README.md:53`。

**纪律一**：枚举只能用 `bash find` 或 `repo_map`，不得用 `grep` 做目录检索。
**纪律二**：负向结论一律标 `absent`（在什么检索范围内未命中），不写「不存在」。
（本项目历史上已因此吃过一次假阴性：用上述方式搜 `llms.txt` / `.copilot-instructions` 得到「未找到匹配」，实测 `sources/repos/goose/.github/copilot-instructions.md` 与 `sources/repos/goose/documentation/static/llms.txt` 都存在。）

---

## `index.csv` 字段口径

一行一个文件。**不重复** `sources/repos/index.csv` 已有的字段（`repo` / `kind` / `completeness` / `snapshot`）——那是同一事实的第二个出处。本表用 `id` 做外键，其余 join 得到。

| 列 | 含义 | 取值 |
|---|---|---|
| `id` | 仓库目录名，外键到 `sources/repos/index.csv` | `Raven` |
| `path` | 该仓根相对路径 | `AGENTS.md`、`.agents/notes/README.md` |
| `kind` | 文件类别 | 见下表封闭集 |
| `bytes` | 实测字节数 | `22349` |
| `role` | 对应的 `02docsdefine\ds.md` D 编号；无对应留空 | `D09` |
| `evidence` | 取证方式（+ 已细读过的补行哈希前 8 位） | `find;L1=204aa1e7` |
| `status` | `verified` / `absent` / `unverified` | `verified` |
| `checked_at` | 取证日期 | `2026-09-25` |

**收录范围**：根目录的 `*.md`，加上治理型非 md（`NOTICE`、`LICENSE.txt`、`architecture-policy.yaml`、`marketplace.json`）。构建/CI 配置（`package.json`、`tsconfig.json`、`pnpm-workspace.yaml`、`.pre-commit-config.yaml`、`pnpm-lock.yaml` 等）**不收**——它们不属于文档治理面。

**`kind` 封闭集**（8 值）：

| kind | 含义 |
|---|---|
| `agent-entry` | `AGENTS.md` / `CLAUDE.md` / `GEMINI.md` |
| `facade` | `README*` |
| `legal` | `LICENSE*` / `NOTICE*` / `CITATION` / `CONTRIBUTORS` / `ACKNOWLEDGMENTS` / `THIRD-PARTY-NOTICES` |
| `collab-rule` | `CONTRIBUTING` / `CODE_OF_CONDUCT` / `GOVERNANCE` / `SECURITY` / `MAINTAINERS` |
| `record` | `CHANGELOG` / `RELEASING` / `RELEASE*` / `EXTERNAL-PRS` |
| `semantic` | `CONTEXT*` / `DESIGN` / `star.md` / `QUICKSTART` |
| `topic-manual` | 项目自造的主题手册（`LLM` / `ERRORS` / `SDK` / `BENCHMARK` / `BRAND_GUIDELINES` / `I18N` / `CUSTOM_DISTROS` / `BUILDING_*` / `RISCV_SETUP` / `MERGE_FIXES` / `ROADMAP`） |
| `machine` | 机读治理件（`architecture-policy.yaml`、`marketplace.json`、`*.i18n.yaml`） |

> ⚠ `kind` 是**本阶段的临时归类，不是分类法结论**。它只为让 `awk` 能过滤，不声称理论地位；归并权在 `01docsclassify`。

**重新生成**：`python domain/repo-context/00docslist/_scripts/build_index.py`（脚本从磁盘现读字节数，`role` 由脚本内的显式映射表给出，不手改 CSV）。

**快照纪律**：`bytes` 只在 `sources/repos/index.csv` 的 `snapshot` 未变时有效。快照刷新后重跑脚本即可，不要手改数字。

---

## 索引（18 仓）

| id | 一句话 | 根级 agent 入口 | 明细 |
|---|---|---|---|
| `deepseek-harness` | 全插件 Cordis agent harness，文档分级与 i18n sidecar 最完备 | `AGENTS.md`（+`CLAUDE.md` 逐字节复制） | [ds\deepseek-harness.md](ds/deepseek-harness.md) |
| `Raven` | Python agent runtime，plans / specs 双目录 + CONTEXT 正典 | `AGENTS.md`（+`CLAUDE.md` 逐字节复制） | [ds\Raven.md](ds/Raven.md) |
| `Tianshu-harness` | 终端 coding agent，`docs/` 有受控 type 枚举与生成式索引 | `AGENTS.md`（Architecture Map）+ 独立的 `CLAUDE.md` | [ds\Tianshu-harness.md](ds/Tianshu-harness.md) |
| `codex` | OpenAI Codex CLI，Rust workspace + 分层 skill 加载 | `AGENTS.md` | [ds\codex.md](ds/codex.md) |
| `gemini-cli` | Google 终端 agent，`GEMINI.md` 按 package 分级 8 份 | `GEMINI.md` | [ds\gemini-cli.md](ds/gemini-cli.md) |
| `qwen-code` | Qwen 终端 agent，`CLAUDE.md` 为散文指针 | `AGENTS.md`（+350B `CLAUDE.md` 指针） | [ds\qwen-code.md](ds/qwen-code.md) |
| `cline` | Cline monorepo，唯一同时有 `.clinerules` 与 copilot 指令 | `AGENTS.md` + `.clinerules` | [ds\cline.md](ds/cline.md) |
| `goose` | Rust agent 框架，根目录手册最多（16 份），含 llms.txt | `AGENTS.md`（+11B `CLAUDE.md` import 指针） | [ds\goose.md](ds/goose.md) |
| `OpenHands` | Agent Canvas 前端，最小根文档集（4 份） | `AGENTS.md` | [ds\OpenHands.md](ds/OpenHands.md) |
| `ZCode` | 插件化 harness，机器可判定的 `architecture-policy.yaml` | `AGENTS.md` | [ds\ZCode.md](ds/ZCode.md) |
| `minimax-cli` | 能力型 CLI（非 harness），根目录带 SDK/ERRORS 手册 | `AGENTS.md` | [ds\minimax-cli.md](ds/minimax-cli.md) |
| `mem0` | 记忆层，56 份 SKILL.md + 4 个 harness 插件目录 | `AGENTS.md`（+`CLAUDE.md` 逐字节复制） | [ds\mem0.md](ds/mem0.md) |
| `memU` | 记忆框架，两份根级 skill 描述符（无 H1，带 frontmatter） | `AGENTS.md` | [ds\memU.md](ds/memU.md) |
| `MemOS` | 记忆操作系统，明写 AGENTS 为正本、CLAUDE 只管运行时适配 | `AGENTS.md`（+1.2KB `CLAUDE.md` 分工件） | [ds\MemOS.md](ds/MemOS.md) |
| `EverOS` | md-first 记忆抽取框架，**有 `CLAUDE.md` 无 `AGENTS.md`** | `CLAUDE.md` | [ds\EverOS.md](ds/EverOS.md) |
| `MemoryBear` | 记忆产品，根目录只有 3 份文档 | **无** | [ds\MemoryBear.md](ds/MemoryBear.md) |
| `ReFind` | 检索型记忆项目，根目录只有 `README.md` | **无** | [ds\ReFind.md](ds/ReFind.md) |
| `claude-code` | Anthropic 官方客户端，**无本地 checkout**（`completeness=binary`） | — | [ds\claude-code.md](ds/claude-code.md) |

> 明细一律为**单文件**：18 份合计 1721 行，最长 125 行（`deepseek-harness`），单次读取足够。没有再分层的判据成立，故 `ds\` 保持扁平。

---

## 与相邻阶段的关系

本阶段的**综合层**在三层产物之外单列一份：[研究报告.md](研究报告.md)——它不复述账本事实，只做跨仓关系的归纳（7 条规律 / 5 个分歧点 / 一个分层模型 / 10 条反例）。

- **给 `01docsclassify`**：`index.csv` 的 `kind` 列是一份**未经理论加工的原始分类**，可直接当分类法的输入样本，也可被推翻。
- **给 `02docsdefine`**：`role` 列填了 D 编号的行，能机械列出「因样本从 11 仓扩到 18 仓而需要重判」的条目（例：`ROADMAP.md` 在 `sources/repos/gemini-cli/ROADMAP.md` 真实存在，而 D26 状态仍是 `○`）。
- **给 `03docscompare`**：同角色多命名的候选对（如 `CONTEXT.md` ↔ `GLOSSARY.md`、`DECISIONS.md` ↔ `decisions\`）在 `ds\*.md` 的「逐文件分析」里已各自带出处，可直接取用。

本目录不改动 `01`–`04` 任何文件，也不改动 `sources/repos/` 的任何 checkout 内容。
