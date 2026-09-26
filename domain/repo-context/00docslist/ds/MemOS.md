# MemOS · 根目录文档实测

> 快照 `12acdad694d0` · 取证 2026-09-25 · 来源 `sources/repos/MemOS/`
> 状态：verified ｜ 覆盖范围：仓库根目录直接子文件 + `.claude/`、`.codex/` + 7 份 SKILL.md

## 1. 根目录清单一览（5 份，本样本最少之一）

| 文件 | 字节 | kind | 角色(D) | 一句话 |
|---|---|---|---|---|
| `AGENTS.md` | 10155 | agent-entry | D09 | 首行 `# AGENTS.md`；L2–L3 是本样本**最明确的单一正本声明** |
| `CLAUDE.md` | 1200 | agent-entry | D10 | **互补分工件**：自述只管 Claude Code 运行时适配 |
| `README.md` | 17535 | facade | D01 | 门面（居中标题 + 徽章） |
| `README_ZH.md` | 17161 | facade | D01 | 中文门面。**下划线式 `_ZH`** |
| `CONTRIBUTING.md` | 16551 | collab-rule | D03 | 贡献指南（16.5KB，本样本第二大） |

无 `SECURITY.md`、无 `CODE_OF_CONDUCT.md`、无 `CHANGELOG.md`、无 `LICENSE`（根目录）。

## 2. 逐文件分析

### 2.1 `AGENTS.md`（10155 字节）—— 把「谁是正本」写进第二行

- **取到的原文（逐字）**：
  - L1 `# AGENTS.md`
  - L2 `> Single source of truth for the project across AI runtimes. Claude Code, Codex, Cursor, Copilot, etc. all defer to this file.`
  - L3 `> Runtime-specific adaptation belongs in each runtime's own file (Claude reads \`CLAUDE.md\`); do not mix it in here.`
- **这两行为什么值得单列**：它同时定了三件事——
  1. **正本唯一**（`single source of truth`）；
  2. **消费者名单**（Claude Code / Codex / Cursor / Copilot——与 `mem0` 的 L2 同型）；
  3. **反向边界**（`do not mix it in here`）——**运行时适配不许写进正本**。
- **对照**：`Raven` 用一句 *"this file wins"* 定优先级，`MemOS` 用**分区**（正本 vs 运行时适配）定边界。同一问题两种解法。

### 2.2 `CLAUDE.md`（1200 字节）—— 四类别名策略里唯一的「互补分工」

- **取到的原文**：
  - L1 `# CLAUDE.md`
  - L3 `## Claude Code Entry`
  - L5 `Project facts live in \`AGENTS.md\`. This file only covers Claude Code runtime adaptation.`
  - L7 `## Sub-agents`
- **它在四类里最省也最难维护**：不是复制（会漂移）、不是指针（不承载内容），而是**分工**——`AGENTS.md` 管项目事实，`CLAUDE.md` 管 Claude 专属运行时（如子 agent 配置）。**分工边界靠人守**，因为没有机械检查能判断「这条内容属于项目事实还是运行时适配」。

### 2.3 命名变体：`README_ZH.md`

下划线式。实测本样本 6 种写法（见 `ds\minimax-cli.md` §2.4）：`.zh-CN` / `.zh` / `_ZH` / `_CN` / `.en|.ja|.ko` / `.windows`。

## 3. Agent 面（vibe coding 相关文件管理）

### 3.1 指令分级：根 2 份 + 子应用 1 份

```
AGENTS.md
CLAUDE.md
apps/openwork-memos-integration/CLAUDE.md     ← 子应用内的 Claude 专属件
```

注意第三份是 **`CLAUDE.md` 而非 `AGENTS.md`**——子树的 Claude 适配件是独立的一份，不与根级 `CLAUDE.md` 同内容（未比对，见 §5）。

### 3.2 Skills：7 份，落在两个**应用**目录下

```
apps/memos-local-openclaw/skill/browserwing-admin/SKILL.md
apps/memos-local-openclaw/skill/browserwing-executor/SKILL.md
apps/memos-local-openclaw/skill/memos-memory-guide/SKILL.md
apps/memos-local-openclaw/site/public/SKILL.md          ← 静态站公开目录
apps/openwork-memos-integration/apps/desktop/skills/{ask-user-question,dev-browser,safe-file-deletion}/SKILL.md
```

**判据**：全部落在 `apps/` 下，**没有一份属于「维护 MemOS 主仓」的工作流**。本仓把 skill 当作**产品能力**（`memos-memory-guide` 教 agent 怎么用 MemOS 记忆），而非开发流程。→ 与 `minimax-cli` 的「skill 是分发物」同型，与 `qwen-code`/`codex` 的「skill 是开发工作流」相反。

`site/public/SKILL.md` 落在**站点静态目录**，属分发物而非仓内工具。

### 3.3 3 个根级 dotdir：`.claude`、`.codex`、`.github`

**`.claude/` 与 `.codex/` 并存**——两个 harness 各有自己的运行时目录，而规范只有根级 `AGENTS.md` 一份（+ `CLAUDE.md` 分工件）。→ 「多 harness = 多目录，但规范只一份」是可行组合。

## 4. 与既有结论的冲突（反证）

| 既有结论 | 本轮实测 | 判定 |
|---|---|---|
| D10 边界：「与 AGENTS.md **同源**；分歧时 AGENTS.md 是正本」 | 本仓 `CLAUDE.md` **不同源**（1200B vs 10155B），自述「只覆盖运行时适配」 | **「同源」不是通则**。D10 应改述为「同源（复制/指针）**或** 分工（互补），取决于本仓约定」 |
| D01 语言变体：把 `README_CN.md` 记在「MemOS/MemoryBear」名下 | MemOS 用 `README_ZH.md`，**没有 `README_CN.md`** | **D01 归属有误**，需修正（同 `ds\minimax-cli.md` 的反证） |
| D12 `SKILL.md` 落点 | 本仓 7 份全在 `apps/` 下，含 `site/public/` | 落点再增一例；且**判据应改为「谁用」**（产品能力 vs 开发工作流） |

## 5. 空白与未取证

- **未读** `AGENTS.md` 全文（只取前 7 行）、`CLAUDE.md` 全文（只取前 7 行）。
- **未比对** 根级 `CLAUDE.md` 与 `apps/openwork-memos-integration/CLAUDE.md` 的差异。
- **未确认** 根目录为何无 `LICENSE`（可能在 `LICENSES/` 或未截图）。
- **未核对** `docs/`（顶层存在）与根级文档的分工。
- **未验证** `.claude/`、`.codex/` 内各自的文件清单。
- 以上均属「在本次检索范围内未查」。
