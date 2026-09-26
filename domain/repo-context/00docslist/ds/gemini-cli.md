# gemini-cli · 根目录文档实测

> 快照 `bedef96ef429` · 取证 2026-09-25 · 来源 `sources/repos/gemini-cli/`
> 状态：verified ｜ 覆盖范围：仓库根目录直接子文件 + `GEMINI.md` 分级 + `.gemini/skills/`

## 1. 根目录清单一览

| 文件 | 字节 | kind | 角色(D) | 一句话 |
|---|---|---|---|---|
| `GEMINI.md` | 4610 | agent-entry | D10 | 首行 `# Gemini CLI Project Context`，agent 入口 |
| `README.md` | 13489 | facade | D01 | 门面（含 CI badge 墙） |
| `ROADMAP.md` | 5748 | topic-manual | **D26** | **首行 `# Gemini CLI Roadmap`，正文指向官方 GitHub Projects 板** |
| `CONTRIBUTING.md` | 20400 | collab-rule | D03 | 20KB，本样本最大的 CONTRIBUTING |
| `SECURITY.md` | 423 | collab-rule | D04 | 极短：指向 `https://g.co/vulnz` 统一入口 |

无 `AGENTS.md`、无 `CLAUDE.md`、无 `CODE_OF_CONDUCT.md`、无 `CHANGELOG.md`。

## 2. 逐文件分析

### 2.1 `GEMINI.md`（4610 字节）—— 别名家族里唯一「本尊即别名」的形态

- **取到的原文**：L1 `# Gemini CLI Project Context`；L3–L5 `Gemini CLI is an open-source AI agent that brings the power of Gemini directly into the terminal. It is designed to be a terminal-first, extensible, and …`
- **与 `CLAUDE.md` 的关键差异**：`CLAUDE.md` 在其它样本里总是**别名**（复制 / 指针 / 分工件），都指向 `AGENTS.md` 这个正本。gemini-cli **没有** `AGENTS.md`——`GEMINI.md` 自己就是正本。
- **含义**：`AGENTS.md` 不必然是正本。判断「谁是正本」只能看**谁没有被声明为副本**，不能靠文件名的通用性。

### 2.2 `ROADMAP.md`（5748 字节）—— 推翻 D26 的「零命中」

- **声称**：`02docsdefine\ds.md` D26 `ROADMAP.md` 状态 `○`（仅草案，样本零命中）。
- **实测**：`sources/repos/gemini-cli/ROADMAP.md` 存在，5748 字节，首行 `# Gemini CLI Roadmap`。
- **原因**：D26 的样本集是 11 仓，不含 gemini-cli；本阶段样本扩到 18 仓才命中。
- **这条正是 `role` 列的价值**：`index.csv` 里 `role=D26` 的行能机械地把「因扩样而需重判」的条目列出来，不需要改 `02docsdefine` 的任何一行。

### 2.3 `SECURITY.md` 只有 423 字节

对照：`Tianshu-harness/SECURITY.md` 3048B、`Raven/SECURITY.md` 662B、`mem0/SECURITY.md` 2280B。gemini-cli 那份只写「用 g.co/vulnz 上报」——**组织级统一入口**取代了仓内政策文本。同类型文档的体量差异来自**主体不同**（项目 vs 组织）。

## 3. Agent 面（vibe coding 相关文件管理）

### 3.1 `GEMINI.md` 分级：8 份，本样本**最彻底**的别名分级

```
GEMINI.md                              ← 根：项目上下文
packages/core/GEMINI.md                ← 首行 `# Gemini CLI Core (@google/gemini-cli-core)`
packages/cli/GEMINI.md
packages/a2a-server/GEMINI.md
packages/devtools/GEMINI.md
packages/sdk/GEMINI.md
packages/test-utils/GEMINI.md
packages/vscode-ide-companion/GEMINI.md
```

**与 DSH 的差别**：DSH 用 `AGENTS.md`（通用名）+ 少量 `CLAUDE.md` 副本；gemini-cli 用**单一别名 `GEMINI.md` 铺满所有 package**。

`packages/core/GEMINI.md` 首 6 行显示子树文件的写法：H1 带**包名与 npm scope**，然后一句职责（`Backend logic for Gemini CLI: API orchestration, prompt construction, tool execution, and agent management.`），再进 `## Architecture`。→ 子树级入口文件是**该 package 的定位卡**，不是全局规范的复读。

### 3.2 Skills：25 份，三处不同性质

| 位置 | 数量 | 性质 |
|---|---|---|
| `.gemini/skills/` | 13 | **仓库自用工作流**（`agent-tui`、`code-reviewer`、`docs-writer`、`pr-creator`、`tui-tester` …） |
| `packages/core/src/skills/builtin/` | 2 | 内置能力（`antigravity-support`、`skill-creator`） |
| `tools/{caretaker-agent,gemini-cli-bot}/**/.gemini/skills/` | 7 | **子工具的独立 agent 配置**（triage-worker 4 份、gemini-cli-bot 4 份 —— 含各自的 memory/critique/metrics/prs） |
| `packages/cli/src/commands/extensions/examples/skills/`、`packages/sdk/test-data/skills/` | 3 | 示例/测试夹具 |

**判据**：`tools/` 下的 7 份是**独立 bot 的 skill 配置**，不服务主仓开发——与 `codex-rs/skills/src/assets/samples/`（产品资产）、`.gemini/skills/`（仓库工作流）构成第三种性质。统计「有多少 skill」时必须带上这个区分。

### 3.3 工具目录

根级 dotdir：`.allstar`、`.gcp`、`.gemini`、`.github`、`.husky`、`.vscode`——**6 个**，是「按工具/组织配置文件分置」的典型。无 `.cursor/`、无 `.claude/`。

## 4. 与既有结论的冲突（反证）

| 既有结论 | 本轮实测 | 判定 |
|---|---|---|
| D26 `ROADMAP.md` 状态 `○`（零命中） | `sources/repos/gemini-cli/ROADMAP.md` 存在，5748B | **需重判为 `●`（实证）**。样本扩到 18 仓后命中 |
| D10 边界：`CLAUDE.md` 与 `AGENTS.md` 同源，分歧时 AGENTS 是正本；同族 `GEMINI.md` | 本仓 **无 `AGENTS.md`**，`GEMINI.md` 4610B 即正本 | **「AGENTS 是正本」不成立为通则**。D10 需改成「同族文件里哪个是正本，取决于本仓有没有 `AGENTS.md`」 |
| D05 边界：`QUICKSTART` 是 README 的最短路径切片 | 本仓无 `QUICKSTART.md` | 无冲突 |

## 5. 空白与未取证

- **未读** `GEMINI.md`（4610B）全文，只取了首 5 行。
- **未核对** `packages/*/GEMINI.md` 六份的正文差异（是否只是定位卡）。
- **未验证** `.gemini/skills/` 的加载机制与 `packages/core/src/skills/` 是否同一套。
- **未确认** `docs/` 目录（远端 repo_map 提示存在）的内部结构与根级文档的分工。
- **未取证** `ROADMAP.md` 正文是否只是外链（首 3 行显示指向 GitHub Projects 板，但未读完）。
- 以上均属「在本次检索范围内未查」。
