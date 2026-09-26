# qwen-code · 根目录文档实测

> 快照 `ffea2d024e52` · 取证 2026-09-25 · 来源 `sources/repos/qwen-code/`
> 状态：verified ｜ 覆盖范围：仓库根目录直接子文件 + `.qwen/` agent 面 + skills

## 1. 根目录清单一览

| 文件 | 字节 | kind | 角色(D) | 一句话 |
|---|---|---|---|---|
| `AGENTS.md` | 17255 | agent-entry | D09 | 正本：首行 `# AGENTS.md`，次节 `## Working Principles` → `### Simplicity First` |
| `CLAUDE.md` | 350 | agent-entry | D10 | **散文指针**，无实质规范内容（见 §2.2） |
| `README.md` | 13274 | facade | D01 | 门面（badge 墙 + 中英导航） |
| `CHANGELOG.md` | 908017 | record | D02 | **908KB**，本样本最大的单文档 |
| `CONTRIBUTING.md` | 12173 | collab-rule | D03 | 贡献流程 |
| `SECURITY.md` | 535 | collab-rule | D04 | 指向云盾上报门户 |

无 `GEMINI.md`、无 `CODE_OF_CONDUCT.md`（根级）。

## 2. 逐文件分析

### 2.1 `AGENTS.md`（17255 字节）

- **取到的原文**：L1 `# AGENTS.md`；L3 `## Working Principles`；L5 `### Simplicity First`。
- **写法**：以**工作原则**（`Simplicity First`）开篇，而不是目录索引或命令表——与 `Tianshu-harness`（Architecture Map）和 `Raven`（硬约束清单）构成三种截然不同的开头策略。

### 2.2 `CLAUDE.md`（350 字节）—— 本样本最明确的「单一正本」声明

全文 5 行，核心一句：

```
**Read [`AGENTS.md`](AGENTS.md) — it is the single source of truth for all coding conventions,
build/test commands, code style, commit conventions, PR workflow, and review guidelines.
All rules in AGENTS.md apply to Claude Code.**
```

- **形态**：**散文指针**——不是 `goose` 式的 `@AGENTS.md` 单行 import（11B），也不是 `deepseek-harness`/`Raven` 式的整份复制（17–22KB），也不是 `MemOS` 式的互补分工（1.2KB 只管运行时适配）。
- **对照表（`CLAUDE.md` 的四种处理法）**：

| 仓 | 字节 | 与 `AGENTS.md` 的关系 |
|---|---|---|
| `deepseek-harness` | 17805 | **逐字节复制**（`cmp` 退出 0） |
| `Raven` | 22349 | **逐字节复制**（`cmp` 退出 0） |
| `mem0` | 11997 | **逐字节复制**（`cmp` 退出 0） |
| `Tianshu-harness` | 17418 / 14896 | 两份**不同**文档（互补分工） |
| `MemOS` | 1200 | **互补分工**（自述只管运行时适配） |
| `qwen-code` | 350 | **散文指针** |
| `goose` | 11 | **import 指针**（`@AGENTS.md`） |
| `EverOS` | 4297 | **单向存在**（无 `AGENTS.md`） |

### 2.3 `CHANGELOG.md`（908017 字节）

**888KB**。对照 `Tianshu-harness/CHANGELOG.md` 60769B、`cline/CHANGELOG.md` 137910B、`codex/CHANGELOG.md` 330B。

- **机制问题**：同一命名下体量跨越 4 个数量级（330B → 888KB）。
- **推论**：单文件 `CHANGELOG.md` 在长周期项目里会**线性膨胀到不可读**，这正是 `Tianshu-harness` 把 changelog 目录化（`docs/changelog/` 41 篇日期文件）与 `codex` 改成指针（正文进 Releases）的动因。**三个样本给出三种应对，值得放进 `03docscompare`。**

## 3. Agent 面（vibe coding 相关文件管理）

### 3.1 指令分级：根级 2 份，子树 0 份

```
AGENTS.md    ← 单一正本（明写 single source of truth）
CLAUDE.md    ← 350B 指针
```

全仓无第三份 `AGENTS.md`/`CLAUDE.md`/`GEMINI.md`。

### 3.2 `.qwen/` —— 工具自留地承载四类资产

根级 dotdir：`.github`、`.husky`、`.qwen`、`.vscode`。`.qwen/` 内实测：

```
agents/            ← agent 定义
skills/            ← 22 个 SKILL.md
specs/             ← 规格
e2e-tests/
review-context.json
```

**判据**：`.qwen/` 已不只是「配置」，而是**装 agent、skill、spec 三类资产的目录**——与本项目的 `.rivet/`、`Tianshu-harness` 的 `.rivet/` 同型，都是 harness 自带的、在仓库根建立的一级目录。

### 3.3 Skills：43 份，三处性质

| 位置 | 数量 | 性质 |
|---|---|---|
| `.qwen/skills/` | 22 | **仓库自用工作流**（`autofix`、`bugfix`、`codegraph`、`deflake`、`docs-audit-and-refresh`、`memory-leak-debug`、`prevent-*`、`triage`、`verify-pr` …） |
| `packages/core/src/skills/bundled/` | 20 | **随产品分发的内置能力**（`agent-delegation`、`browser-use`、`computer-use`、`dataviz`、`goal-draft`、`loop`、`new-app`、`review`、`simplify`、`stuck`、`workflow-authoring` …） |
| `packages/cli/src/commands/extensions/examples/`、`packages/cua-driver/rust/Skills/`、`packages/desktop-shell/.agents/skills/` | 4 | 示例 / 驱动 / 桌面壳 |

**`.qwen/skills/` 是 18 仓里人数最多的一处开发工作流集合**（22），且命名是**问题导向**（`deflake`、`memory-leak-debug`、`stuck`、`triage`），而非 `codex` 的**审查维度导向**（`code-review-*`）。

## 4. 与既有结论的冲突（反证）

| 既有结论 | 本轮实测 | 判定 |
|---|---|---|
| D10 最佳实现是**指针**，避免同一规范维护两份 | 本仓 `CLAUDE.md` 350B 明确声明 `AGENTS.md` 是 `single source of truth` | **一致**，且这是「指针」写法里**信息量最大**的一种：不仅指向，还**逐项列出** AGENTS.md 覆盖哪些领域 |
| D02 `CHANGELOG.md` 形态「单文件（+目录变体）」 | 本仓单文件 888KB | 形态清单需补「**膨胀后的应对**」：目录化（TS）/ 指针化（codex）/ 截断策略 |
| D12 `SKILL.md` 位置「`skills/<name>/`（也可在包内）；memU 直接放根级」 | 本仓 `.qwen/skills/`（22）+ `packages/core/src/skills/bundled/`（20） | **位置清单不全**：`.qwen/` 这类**工具名前缀目录**是第三种落点，且在本样本中出现于 5 个仓（`.qwen/`、`.codex/`、`.gemini/`、`.claude/`、`.agents/`） |

## 5. 空白与未取证

- **未读** `AGENTS.md` 全文（17KB），只取了首 5 行。
- **未比对** `CHANGELOG.md` 888KB 的首尾结构（是否已按版本分段、是否有截断策略）。
- **未读** `.qwen/specs/`、`.qwen/agents/` 的内容形态。
- **未验证** `.qwen/` 与 `packages/core/src/skills/bundled/` 的加载优先级。
- **未确认** 根级无 `CODE_OF_CONDUCT.md` 是设计还是遗漏（`.github/` 下可能有）。
- 以上均属「在本次检索范围内未查」。
