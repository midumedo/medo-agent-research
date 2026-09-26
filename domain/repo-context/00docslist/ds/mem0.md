# mem0 · 根目录文档实测

> 快照 `a39a802bbc93` · 取证 2026-09-25 · 来源 `sources/repos/mem0/`
> 状态：verified ｜ 覆盖范围：仓库根目录直接子文件 + 11 组 `AGENTS.md`/`CLAUDE.md` 对 + 9 个 plugin 的 skill 矩阵

## 1. 根目录清单一览

| 文件 | 字节 | kind | 角色(D) | 一句话 |
|---|---|---|---|---|
| `AGENTS.md` | 11997 | agent-entry | D09 | 首行 `# AGENTS.md`；次行 `Context for AI coding assistants (Claude Code, Cursor, Copilot, Codex) working in the Mem0 repository.` |
| `CLAUDE.md` | 11997 | agent-entry | D10 | **与 `AGENTS.md` 逐字节相同**（`cmp` 退出 0） |
| `README.md` | 11914 | facade | D01 | 门面（banner + badge） |
| `CONTRIBUTING.md` | 11543 | collab-rule | D03 | 贡献流程 |
| `CODE_OF_CONDUCT.md` | 8437 | collab-rule | D03 | Contributor Covenant |
| `SECURITY.md` | 2280 | collab-rule | D04 | 漏洞披露 |
| `LLM.md` | 37334 | topic-manual | D36 | 面向 LLM 的产品说明（37KB，本样本最大的 topic 手册） |
| `marketplace.json` | 436 | machine | — | 插件市场清单 |

## 2. 逐文件分析

### 2.1 `AGENTS.md`（11997 字节）—— 面向**四家** harness 的单一正本

- **取到的原文**（逐字）：L2 `Context for AI coding assistants (Claude Code, Cursor, Copilot, Codex) working in the Mem0 repository.`；L3 `**Mem0** ("mem-zero") is a memory layer for AI agents: persistent, personalized memory through a hosted platform API and self-hosted open-source SDKs. Apache-2.`
- **判据**：第二行就**点名四个消费者**。这是「一份正本供多 harness」的显式声明——与本仓同时维护 `CLAUDE.md` 逐字节副本、`.claude-plugin/`、`.codex-plugin/`、`.cursor-plugin/`、`.kimi-plugin/` 四个插件目录形成对照：**规范只认一份，适配件按 harness 各备一套。**

### 2.2 `CLAUDE.md`（11997 字节）

`cmp -s AGENTS.md CLAUDE.md` → 逐字节相同。与 `deepseek-harness`、`Raven` 同型。见 §4。

### 2.3 `LLM.md`（37334 字节）—— 名字即受众

本样本里唯一以 `LLM` 命名的根级文档。`02docsdefine` D36 已收录。命名特点：**受众写在文件名里**（`LLM`），而其它仓的同类内容叫 `README` 或进 `docs/`。

**判据**：这个名字对 LLM 本身**没有任何先验含义**——不像 `README`/`AGENTS` 有强先验。因此它必须**在别处被显式介绍**，否则模型不会主动去读。

### 2.4 `marketplace.json`（436 字节）

插件市场清单。与 9 个 `integrations/*-plugin/` 目录配套。

## 3. Agent 面（vibe coding 相关文件管理）

### 3.1 指令分级：**11 组成对副本**——本样本最系统化的复制模式

`find` 实测 22 份文件（11 个 `AGENTS.md` + 11 个 `CLAUDE.md`），**每一对都逐字节相同**：

| 目录 | 字节 | 判定 |
|---|---|---|
| `.`（根） | 11997 | SAME |
| `.github/` | 19893 | SAME |
| `cli/node/` | 1228 | SAME |
| `cli/python/` | 1456 | SAME |
| `docs/` | 1877 | SAME |
| `integrations/` | 7809 | SAME |
| `mem0-ts/` | 2072 | SAME |
| `mem0/` | 4600 | SAME |
| `server/` | 1113 | SAME |
| `skills/` | 4674 | SAME |
| `tests/` | 1007 | SAME |

（字节为 `AGENTS.md` 侧实测；`cmp -s` 对每对均退出 0。全部 11 行逐条实测，无省略。）

→ **硬结论**：mem0 把「一份正本 + 一份别名副本」的分级模式推到了 monorepo 的**每一个子包**：11 个包各 2 份 = 22 个文件维护**11 份不同的规范**，其中**一半是纯副本**。这是本样本里「副本维护成本」的最高点。

### 3.2 多 harness 插件：4 个 dotdir + 9 个 plugin 目录

根级 dotdir：`.agents`、`.claude-plugin`、`.codex-plugin`、`.cursor-plugin`、`.github`、`.kimi-plugin` —— **4 个 harness 插件目录**。

`integrations/` 下 9 个 plugin，各自带 skills：

| plugin | skills |
|---|---|
| `antigravity-plugin` | forget / pause / remember / resume / search / status |
| `claude-code-plugin` | 同上 6 个 |
| `codex-plugin` | 同上 6 个 |
| `cursor-plugin` | 同上 6 个 |
| `kimi-plugin` | 同上 6 个 |
| `mem0-agent-plugin` | 同上 6 个 |
| `pi-agent-plugin` | forget / remember / search / status / tour / context-loader |
| `opencode-plugin` | mem0-{context-loader,forget,remember,scope,search,status,tour} |
| `openclaw` | memory-triage |

再加根级 `skills/` 6 个（`mem0`、`mem0-cli`、`mem0-integrate`、`mem0-oss-to-platform`、`mem0-test-integration`、`mem0-vercel-ai-sdk`）。

**合计 56 份 `SKILL.md`** —— 本样本最多。

**判据（关键）**：这 6 个同名的 skill（forget/pause/remember/resume/search/status）在 **6 个 plugin 里各出现一次**。它们是**同一套能力在 6 个 harness 上的适配件**，不是 6 套不同的能力。任何「本仓有 56 个 skill」的计数都会**高估 9 倍**。这与 `cline` 的「一个 skill 复制 3 份」是同一类现象的不同规模（`cline` 3×，`mem0` 6×）。

### 3.3 `docs/llms.txt` 存在

与 `goose/documentation/static/llms.txt` 同型：放在**文档目录**下，服务站点/外部消费者，而非仓内 agent。

## 4. 与既有结论的冲突（反证）

| 既有结论 | 本轮实测 | 判定 |
|---|---|---|
| D10：`CLAUDE.md` 最佳实现是指针，「避免同一规范维护两份」 | 本仓 `CLAUDE.md` 与 `AGENTS.md` **逐字节相同**（11997B），且这一模式在 11 个子包**全部复制** | **D10 的规范主张在本样本里被广泛违反**（DSH、Raven、mem0 三家复制；goose、qwen-code 两家指针）。D10 应从「最佳实现是指针」改述为「**实测存在多种实现，指针是其中维护成本最低的一种**」 |
| D12：`SKILL.md` 落点 | 本仓 56 份横跨 `integrations/<harness>-plugin/skills/`、`integrations/opencode-plugin/opencode-skills/`（**目录名又不叫 skills**）、根级 `skills/` | **落点命名未收敛**，同一仓内三种 |
| `sources/repos/index.csv` 关键词 `56-skills-published;claude-code-plugin;antigravity-plugin` | `find -name SKILL.md` 计数 56，四个 plugin dotdir 存在 | 一致 |
| D36 `LLM.md` 归入「主题专章」 | 实测确认，37KB 最大 | 一致 |

## 5. 空白与未取证

- **未读** `AGENTS.md` 全文（12KB，只取首 3 行）；11 份分级 `AGENTS.md` 的**内容差异未比对**（只 `cmp` 了同名对，未比较不同包之间的差异）。
- **未比对** 6 个 plugin 里同名的 `forget`/`remember`/`search` 等 skill 是否也逐字节相同（`cline` 的同类现象已证实相同，mem0 未验证）。
- **未读** `marketplace.json` 内容。
- **未核对** `.github/AGENTS.md`（19893B，比根级 11997B 更大）为何体量大于根级。
- **未确认** `mem0/` 与 `mem0-ts/` 两个子目录与根级 `mem0` 的关系（顶层目录列表实测出现 `mem0 mem0 mem0-ts`，疑有重名）。
- 以上均属「在本次检索范围内未查」。
