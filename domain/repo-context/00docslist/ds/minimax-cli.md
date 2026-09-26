# minimax-cli · 根目录文档实测

> 快照 `33453cf12392` · 取证 2026-09-25 · 来源 `sources/repos/minimax-cli/`
> 状态：verified ｜ 覆盖范围：仓库根目录直接子文件 + `skill/` + `docs/`
> **注意**：`sources/repos/index.csv` 对本仓的 `kind` 是 `tooling`，`keywords` 含 `capability-cli;not-a-harness` —— **它不是 agent harness，是能力型 CLI**。样本里唯一一个。

## 1. 根目录清单一览

| 文件 | 字节 | kind | 角色(D) | 一句话 |
|---|---|---|---|---|
| `AGENTS.md` | 5952 | agent-entry | D09 | 首行 `# AGENTS.md - Agent Coding Guidelines`，含 `## Project Overview` |
| `README.md` | 9793 | facade | D01 | 英文门面（含能力大图） |
| `README_CN.md` | 8632 | facade | D01 | 中文门面。**命名用下划线 `_CN`**，与 `README.zh-CN.md`（点号）不同 |
| `ERRORS.md` | 10631 | topic-manual | D36 | 错误码/错误文案参考手册 |
| `SDK.md` | 4457 | topic-manual | D36 | TypeScript SDK 用法 |

无 `CLAUDE.md`、无 `CONTRIBUTING.md`、无 `SECURITY.md`、无 `CODE_OF_CONDUCT.md`、无 `CHANGELOG.md`。

## 2. 逐文件分析

### 2.1 `AGENTS.md`（5952 字节）

- **取到的原文**：L1 `# AGENTS.md - Agent Coding Guidelines`（**标题即说明用途**，不是裸 `# AGENTS.md`）；L3 `This document provides guidelines for agents operating in this repository.`；L5 `## Project Overview`。
- **与众不同的格式**：H1 里带**破折号副标题**，把「这是什么文件」直接写进标题。对照：`Raven`/`DSH`/`qwen-code` 用裸 `# AGENTS.md`，`OpenHands` 用 `# Repository Notes`，`cline`/`ZCode` 干脆无 H1。**五种 H1 策略并存。**

### 2.2 `ERRORS.md`（10631 字节）—— 面向用户的错误文案手册

- **取到的原文**：L1 `# MiniMax CLI Error Reference`；L3 `This document lists all error scenarios and the messages users will see.`；L5 `## Auth Commands`。
- **判据**：它登记的是**用户会看到的确切文本**，不是内部异常类型。`02docsdefine` D36 把 `ERRORS` 归入「主题专章」是对的，但没记它**面向用户可见文案**这一性质。

### 2.3 `SDK.md`（4457 字节）

首行 `# MiniMax SDK`，次行 `TypeScript SDK for the [MiniMax](https://www.minimaxi.com) AI platform.`——**CLI 仓里带 SDK 手册**，说明该仓是「平台能力出口」而非单一产品。

### 2.4 `README_CN.md` —— 命名变体

本样本里语言变体后缀至少有 6 种写法：

| 写法 | 出现仓 |
|---|---|
| `README.zh-CN.md` | `EverOS`、`Raven` |
| `README.zh.md` | `deepseek-harness` |
| `README_ZH.md` | `MemOS` |
| `README_CN.md` | `MemoryBear`、`minimax-cli` |
| `README.en.md` / `.ja.md` / `.ko.md` | `Tianshu-harness` |
| `README.ja.md` | `Tianshu-harness` |

**点号 vs 下划线、`zh` vs `zh-CN` vs `CN`** —— 同一个语义，六种拼写。任何「按文件名匹配语言变体」的脚本都必须把这六种都覆盖。

## 3. Agent 面（vibe coding 相关文件管理）

### 3.1 指令分级：只有 1 份

全仓仅根级 `AGENTS.md`。无 `CLAUDE.md`、无 `GEMINI.md`、无子树 `AGENTS.md`。

### 3.2 Skills：2 份，落在 **`skill/`**（单数，且非 dotdir）

```
skill/SKILL.md          (13KB)
skill/h3-video/SKILL.md
```

**形态异常之处**：
- 目录名是 **`skill/` 单数**，不是 `skills/` 复数，也不是 `.agents/skills/`；
- **不在任何 dotdir 下**——它是仓库的**一级正常目录**，与 `src/`、`docs/`、`test/` 并列；
- `skill/SKILL.md` 直接放在目录根（不是 `<name>/SKILL.md` 约定）。

→ 与 `memU/SKILL.md`（仓库根）合起来说明：**`SKILL.md` 的落点没有收敛**。至少 4 种：`skills/<name>/`、`.<tool>/skills/<name>/`、`<任意目录>/SKILL.md`、仓库根 `SKILL.md`。

### 3.3 Skills 的**分发**性质

`keywords` 记 `publishes-skill-md`。本仓 skill 不是给「维护本仓的 agent」用的——它随 CLI 分发给用户，让**用户的 agent** 学会用这个 CLI。这是 `codex`（产品资产）、`gemini-cli`（子 bot 配置）、`cline`（多工具副本）之外的**第五种 skill 性质**。

### 3.4 根级 dotdir 只有 `.github`

## 4. 与既有结论的冲突（反证）

| 既有结论 | 本轮实测 | 判定 |
|---|---|---|
| D01 语言变体实测：「TS `README.en.md`/`.ja.md`/`.ko.md`、DSH `README.zh.md`、Raven `README.zh-CN.md`、MemOS `README_ZH.md`、MemOS/MemoryBear `README_CN.md`」 | 逐仓实测：`EverOS`=`README.zh-CN.md`、`MemOS`=`README_ZH.md`、`MemoryBear`=`README_CN.md`、`Raven`=`README.zh-CN.md`、`DSH`=`README.zh.md`、`Tianshu-harness`=`README.{en,ja,ko}.md`、`minimax-cli`=`README_CN.md`、`OpenHands`=`README.windows.md` | **D01 的归属写错了**：它把 `README_CN.md` 记在「MemOS/MemoryBear」名下，但 **MemOS 用的是 `README_ZH.md`，没有 `_CN`**。D01 需修正归属 |
| D36：`ERRORS.md` 是「主题专章」 | 实测确认，并补一条：它登记的是**用户可见文本** | 一致，可补性质 |
| D12 `SKILL.md` 位置清单 | 本仓 `skill/SKILL.md` 是**第四种落点**（非 dotdir、单数目录名、无 `<name>/` 层） | **需扩充** |
| `index.csv` 关键词 `not-a-harness` | 根级无 `CLAUDE.md`/`GEMINI.md`，指令面只有 1 份 `AGENTS.md` | 一致 |

## 5. 空白与未取证

- **未读** `AGENTS.md` 全文（只取首 5 行）、`ERRORS.md` 正文（只取首 5 行）、`SDK.md` 正文。
- **未核对** `docs/` 目录（`docs/cli-design.md`、`docs/releasing.md`）与根级手册的分工。
- **未确认** `skill/SKILL.md` 与 `skill/h3-video/SKILL.md` 的关系（后者是否被前者引用）。
- **未验证** `publishes-skill-md` 的分发形态（npm 包内路径）。
- 以上均属「在本次检索范围内未查」。
