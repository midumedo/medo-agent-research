# EverOS · 根目录文档实测

> 快照 `5076683ab88d` · 取证 2026-09-25 · 来源 `sources/repos/EverOS/`
> 状态：verified ｜ 覆盖范围：仓库根目录直接子文件 + `.claude/skills/`
> **本仓的特殊性：根目录有 `CLAUDE.md`，但没有 `AGENTS.md`。**

## 1. 根目录清单一览

| 文件 | 字节 | kind | 角色(D) | 一句话 |
|---|---|---|---|---|
| `CLAUDE.md` | 4297 | agent-entry | D10 | **全仓唯一的 agent 入口**，首行 `# EverOS — md-first Memory Extraction Framework` |
| `README.md` | 28159 | facade | D01 | 门面（居中 div + banner） |
| `README.zh-CN.md` | 28220 | facade | D01 | 中文门面。**点号 + `zh-CN`** |
| `CHANGELOG.md` | 71214 | record | D02 | 人手写（Keep a Changelog：`All notable changes to **EverOS** are documented in this file.`） |
| `QUICKSTART.md` | 8009 | semantic | D05 | 首行 `# Quickstart`，次两行 `> Five minutes from one OpenRouter API key to durable Markdown memory and keyword recall.` |
| `CONTRIBUTING.md` | 5733 | collab-rule | D03 | 贡献指南 |
| `CODE_OF_CONDUCT.md` | 5478 | collab-rule | D03 | Contributor Covenant（含 `## Our Pledge`） |
| `SECURITY.md` | 2539 | collab-rule | D04 | 只对最新 release 线提供修复 |
| `ACKNOWLEDGMENTS.md` | 3850 | legal | D06 | **带面包屑**：首行 `[Home](README.md) > [Docs](docs/index.md) > Acknowledgments` |
| `CITATION.md` | 1188 | legal | D06 | 同样带面包屑 `[Home](README.md) > [Docs](docs/index.md) > Citation` |
| `NOTICE` | 2634 | legal | D06 | 无扩展名 |

## 2. 逐文件分析

### 2.1 `CLAUDE.md`（4297 字节）—— 「别名」缺位的情形

- **取到的原文**：L1 `# EverOS — md-first Memory Extraction Framework`；L3 `This is a Python framework for md-first memory extraction (lightweight; single-user or small-team).`；L5 `## Quick commands`。
- **它不是什么**：它**不是** `AGENTS.md` 的副本，也**不是**指针——因为本仓**没有** `AGENTS.md`。它是**本仓事实上的通用 agent 入口**，只是用了 Claude 系工具认的文件名。
- **它因此少了一个问题**：没有「正本与副本会不会分叉」的问题（因为只有一份）。但多了一个问题：**只认 `AGENTS.md` 的 harness 在本仓读不到任何指令**。
- **`02docsdefine` D10 实测**把 `EverOS` 列为「有 `CLAUDE.md`」的四家之一，但**没记它没有 `AGENTS.md`**——这正是「有 A 无 B」这种缺失关系的价值。

### 2.2 `ACKNOWLEDGMENTS.md` 与 `CITATION.md` 的面包屑

两份文件首行都是：

```
[Home](README.md) > [Docs](docs/index.md) > Acknowledgments
```

**判据**：本仓的 `docs/` 有自己的 `index.md`，而根级法务/致谢页**主动指向它**。这是一条**根 → docs 的导航线**，反向说明本仓的文档中心在 `docs/`，根目录是**登记页**。

对照 `Tianshu-harness`（根级 `AGENTS.md` 自称 Architecture Map，指向 `docs/architecture-overview.md`）——两种「根做门面、docs 做主体」的实现。

### 2.3 `QUICKSTART.md`（8009 字节）—— 满足 D05 边界的一例

首行 `# Quickstart`，次两行：`> Five minutes from one OpenRouter API key to durable Markdown memory and keyword recall.`

对照 `memU/INSTALL-LATEST.md`（实为 skill 描述符），EverOS 的 `QUICKSTART.md` **符合** D05 的边界：「只保留最短路径」。→ 同一族名字里，一个符合、一个不符合，**只能逐份读首行判断**。

## 3. Agent 面（vibe coding 相关文件管理）

### 3.1 指令分级：0 级分层

全仓仅根级 `CLAUDE.md` 一份（`find` 实测）。无 `AGENTS.md`、无 `GEMINI.md`、无子树同名文件。

### 3.2 Skills：5 份，全在 `.claude/skills/`，且全是**开发工作流**

```
.claude/skills/add-memory-kind/SKILL.md
.claude/skills/commit/SKILL.md
.claude/skills/new-branch/SKILL.md
.claude/skills/pr/SKILL.md
.claude/skills/release/SKILL.md
```

**判据**：这是「**纯开发工作流**」形态的最干净样本——`commit`、`new-branch`、`pr`、`release` 四个直接对应 Git 操作，`add-memory-kind` 对应本项目特有的扩展点。与 `mem0`/`minimax-cli`（skill 是分发物）、`ZCode`（skill 是产品能力）形成对照。

**并且它给出了一个组合**：**`.claude/skills/` + 根级 `CLAUDE.md` + 无 `AGENTS.md`** —— 一个**只面向 Claude 系**的完整 agent 配置。本样本里唯一一家。

### 3.3 2 个根级 dotdir：`.claude`、`.github`

## 4. 与既有结论的冲突（反证）

| 既有结论 | 本轮实测 | 判定 |
|---|---|---|
| D10 实测：「DSH/Raven/TS/MemOS/EverOS 均有 `CLAUDE.md`」 | 属实，但**未记录 EverOS 没有 `AGENTS.md`** | **需补缺失关系**：D10 应区分「有 `CLAUDE.md` 且有 `AGENTS.md`（副本/指针/分工）」与「有 `CLAUDE.md` 但无 `AGENTS.md`（唯一入口）」 |
| D10 边界：`CLAUDE.md` 是「`AGENTS.md` 的**开关**」 | 本仓 `CLAUDE.md` 4297B 承载实体内容，不做任何指向 | **「开关」比喻不成立**于本仓 |
| D06：`ACKNOWLEDGMENTS` = 致谢名单 | 属实，且**带面包屑指向 `docs/index.md`** | 可补一条形态：法务页可作为**文档导航的入口** |
| D02：`CHANGELOG` 记「对外变化」 | 本仓人手写、71KB、Keep a Changelog | 一致（属最简单形态） |

## 5. 空白与未取证

- **未读** `CLAUDE.md` 全文（只取前 5 行）、`README.md`/`README.zh-CN.md`（28KB 各）、`CHANGELOG.md`（71KB）。
- **未展开** `docs/` 目录（顶层存在且有 `index.md`，本轮只由面包屑间接证实其存在）。
- **未核对** `README.md` 与 `README.zh-CN.md` 是否内容对齐（28159 vs 28220，差 61 字节）。
- **未确认** 为什么只提供 `CLAUDE.md` 而无 `AGENTS.md`（设计选择还是疏漏）。
- 以上均属「在本次检索范围内未查」。
