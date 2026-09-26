# OpenHands · 根目录文档实测

> 快照 `c17fc6538d57` · 取证 2026-09-25 · 来源 `sources/repos/OpenHands/`
> 状态：verified ｜ 覆盖范围：仓库根目录直接子文件 + `.agents/skills/`
> **注意**：`sources/repos/index.csv` 对本仓的 `completeness` 是 `app-only`（只有前端应用，无 agent core），`keywords` 含 `no-agent-core;no-root-pyproject`。

## 1. 根目录清单一览（4 份，本样本最少之一）

| 文件 | 字节 | kind | 角色(D) | 一句话 |
|---|---|---|---|---|
| `AGENTS.md` | 6277 | agent-entry | D09 | 首行 `# Repository Notes`——**标题与文件名不一致** |
| `README.md` | 10162 | facade | D01 | 门面 |
| `README.windows.md` | 1134 | facade | D01 | Windows 专属快速上手，自述「主安装选项见 README.md」 |
| `CHANGELOG.md` | 1093 | record | D02 | 1KB，Keep a Changelog 格式 |

无 `CONTRIBUTING.md`、无 `SECURITY.md`、无 `CODE_OF_CONDUCT.md`。

## 2. 逐文件分析

### 2.1 `AGENTS.md`（6277 字节）—— 四个小节都在回答「代码该放哪、谁不能碰什么」

首行不是 `# AGENTS.md` 而是 `# Repository Notes`。四个小节：

**(a) `## General`** —— 命令与硬约束。含三条可直接核验的规则：

- 验证命令：`npm run lint`、`npm test`、`npm run build`、`npm run build:lib`（这就是 D09 说的「工具链 Runbook」）
- 依赖**精确锁定**：`Use the committed package-lock.json with npm ci, and update package.json and package-lock.json together through npm.`
- **反向禁止**：`Default working-directory behavior must reuse DEFAULT_WORKING_DIR from src/api/agent-server-config.ts rather than hardcoding /workspace/project.`

**(b) `## Repository Ownership`** —— 一张表，列出**四个兄弟仓各拥有什么**（`OpenHands/OpenHands`、`software-agent-sdk`、`extensions`、`automation`），并给出判断列「Add code there when…」。

收尾一句是**依赖方向**：`The normal dependency direction is Agent Server contract → TypeScript client → Agent Canvas. Do not reimplement Agent Server endpoints or contracts in Canvas.`

→ 这是本样本里**唯一**一份把「跨仓边界」写进 agent 指令的文件。它解决的问题不是「怎么写代码」，而是**「这个改动根本不该落在这个仓」**。

**(c) `## Shared Frontend Change Checklist`** —— 改共享适配器前的三条前置动作（升 `compatibility.minimumAgentServer`、枚举跨 Local/Cloud × 各 agent 类型的消费路径、给持久化状态定唯一 owner）。

**(d) `## PR Description Human Check`** —— 逐字：*"The `HUMAN:` section in PR descriptions is reserved for human contributors only. **AI agents must not add to, edit, move, or remove it.** If validation fails because it is missing or empty, stop and ask the human user to update it in their own words."*

→ 罕见的「**给 AI 划一条人机分界线**」的成文规则：给人类留一个 AI 不可触碰的字段，且明确「校验失败时停下问人，不要代替人写」。

### 2.2 `README.windows.md`（1134 字节）—— 平台变体

自述：*"This doc contains **Windows-specific** command syntax for running Agent Canvas with the **Docker sandbox**. For the main install options and overall context, see README.md."*

**与语言变体的区别**：`Tianshu-harness` 的 `README.{en,ja,ko}.md` 是**翻译**（同内容不同语言），`OpenHands` 的 `README.windows.md` 是**平台分化**（不同内容、同一语言）。两者共用 `.xxx.md` 后缀形式，语义完全不同——`01docsclassify` 若按后缀归类会把它们混为一谈。

## 3. Agent 面（vibe coding 相关文件管理）

### 3.1 指令分级：只有 1 份

全仓仅根级 `AGENTS.md`（`find -name 'AGENTS.md'` 实测）。无 `CLAUDE.md`、无 `GEMINI.md`。

### 3.2 Skills：7 份，且**有配套的评审指南文件**

```
.agents/skills/{desktop-electron, e2e-testing, frontend-api-contracts,
                frontend-development, local-stack-runtime, pr-design-doc, telemetry-analytics}
```

`AGENTS.md` 对这套机制的说明值得逐字记：

- *"Public skills come from `@openhands/extensions`; **project-specific contributor guidance lives under `.agents/skills/`**."*
  → 明确区分「公共 skill（外部包）」与「本仓贡献者指引（`.agents/skills/`）」。
- *"All pull requests must comply with [`.agents/skills/custom-codereview-guide.md`](...), in addition to the general contribution requirements and CI checks."*
  → **`.agents/skills/` 里存在非 `SKILL.md` 的 `.md` 文件**（`custom-codereview-guide.md`），且被 PR 规则引用。这打破了「`.agents/skills/` 下只有 `<name>/SKILL.md`」的形态假设。
- `## Functionality-Specific Skills` 自述：*"Detailed contributor knowledge is split into skills **so it loads only for relevant work**. Invoke every applicable skill before changing that area; cross-cutting changes may require several skills."*
  → 这就是 skill 机制存在的**理由陈述**：**按需加载**，避免常驻上下文。本样本里对这个问题说得最直白的一份。

### 3.3 5 个根级 dotdir

`.agents`、`.github`、`.husky`、`.openhands`、`.screenshots`。其中 `.openhands` 是产品自己的运行时目录、`.screenshots` 是测试产物目录——**都不是文档面**。

## 4. 与既有结论的冲突（反证）

| 既有结论 | 本轮实测 | 判定 |
|---|---|---|
| D09 边界：「AGENTS 不解释『系统是什么』，只规定怎么执行」 | 本仓 `AGENTS.md` 的 (b) 节整节在解释**四个仓各自是什么** | 一致但需补充：**「跨仓责任边界」属于「怎么执行」**，可以在 AGENTS 里；它约束的是「改动该不该做」，不是「系统长什么样」 |
| D12 形态：「单文件（+ 同目录 `references\`、`templates\`）」 | 本仓 `.agents/skills/` 下**混放** `custom-codereview-guide.md` 这类非 SKILL 文件，且被 AGENTS 引用 | **形态需补**：`.agents/skills/` 是**目录约定**，其内不必然只有 `<name>/SKILL.md` |
| D01 语言变体：「`README.en.md`/`.ja.md`/`.ko.md`」 | 本仓 `README.windows.md` 是**平台**变体而非语言变体，后缀形式相同 | **需新增维度**：`.xxx.md` 后缀可表示语言，也可表示平台 |
| `index.csv` 关键词 `no-agent-core;app-only` | 实测根目录确有 `src/`、`electron/`、`public/`，无 Python 后端 | 一致 |

## 5. 空白与未取证

- **未读** `AGENTS.md` 的 `.agents/skills/custom-codereview-guide.md`（被 AGENTS 引用但本轮未打开）。
- **未读** `CHANGELOG.md`(1093B) 与 `README.md`(10162B) 正文。
- **未核对** `specs/`、`docs/` 两个子目录的结构（顶层目录列表里存在）。
- **未验证** `@openhands/extensions` 这个外部公共 skill 包的仓库形态。
- 以上均属「在本次检索范围内未查」。
