# cline · 根目录文档实测

> 快照 `dd2e190e5c55` · 取证 2026-09-25 · 来源 `sources/repos/cline/`
> 状态：verified ｜ 覆盖范围：仓库根目录直接子文件 + 12 个 dotdir + `.clinerules/` + 三份 skill 副本

## 1. 根目录清单一览

| 文件 | 字节 | kind | 角色(D) | 一句话 |
|---|---|---|---|---|
| `AGENTS.md` | 5279 | agent-entry | D09 | **无 H1**，首行即正文 `This is the **Cline** monorepo. Toolchain is **Bun 1.3.13** …` |
| `README.md` | 9237 | facade | D01 | 门面 |
| `CHANGELOG.md` | 137910 | record | D02 | 138KB，最高版本节 `## [4.1.21]` |
| `CONTRIBUTING.md` | 8764 | collab-rule | D03 | 贡献流程 + bug 上报 |
| `CODE_OF_CONDUCT.md` | 3373 | collab-rule | D03 | Contributor Covenant（截取版） |
| `SECURITY.md` | 952 | collab-rule | D04 | 只补最近一个 minor 版本 |

## 2. 逐文件分析

### 2.1 `AGENTS.md`（5279 字节）

- **取到的原文**：L1（首行即正文）`This is the **Cline** monorepo. Toolchain is **Bun 1.3.13** (package manager + task runner) with **Node >=22** as the runtime. Do not use npm/yarn/pnpm.`；L2 `## Cloud Agent Instructions`；L3 `### Cline CLI`。
- **格式漂移**：本样本里唯一**首行不是 H1** 的 `AGENTS.md`（`Raven`/`DSH`/`qwen-code` 都是 `# AGENTS.md`，`Tianshu-harness` 是 `# 天枢 … — Architecture Map`）。任何按「首行是 `# AGENTS.md`」做的机械识别会漏掉它。
- **内容取向**：开篇即**工具链硬约束**（Bun，禁 npm/yarn/pnpm），并直接进入 `## Cloud Agent Instructions`——面向云端 agent 的操作说明而非人。

### 2.2 `.clinerules/`（**目录**）——本样本唯一的第三方规则目录

```
.clinerules/bun-and-node.md
.clinerules/cline-overview.md
.clinerules/debug-harness.md
.clinerules/general.md
.clinerules/network.md
.clinerules/protobuf-development.md
.clinerules/sdk-migration.md
.clinerules/storage.md
.clinerules/hooks/README.md
.clinerules/workflows/{address-pr-comments,find-pr-reviewers,git-branch-analysis,hotfix-release,pr-review,release,writing-documentation}.md
```

**特征**：8 份**主题分片**（按子系统切：网络 / 存储 / protobuf / SDK 迁移 …）+ 7 份**工作流分片**（按任务切）+ `hooks/`。

**判据**：这是「**一份 AGENTS.md 还是多份**」这个问题的**第三种答案**——不是单文件、也不是 `AGENTS.md` 分级（子树同名文件），而是**同层多文件按主题切分**。它对应的是 cline 自己的规则加载器约定。

### 2.3 `.github/copilot-instructions.md` 存在

**这是「AGENTS.md 已被全行业收敛」这一说法的一个反例**：同一仓里同时有 `AGENTS.md`（根 + `sdk/` + `sdk/packages/llms/`）与 `.github/copilot-instructions.md`。

## 3. Agent 面（vibe coding 相关文件管理）

### 3.1 指令分级：根 + sdk + sdk/packages/llms（三层）

```
AGENTS.md
sdk/AGENTS.md
sdk/packages/llms/AGENTS.md
```

无 `CLAUDE.md`、无 `GEMINI.md`。

### 3.2 Skills：18 份 `SKILL.md`，但只有 7 个**不同**的 skill —— 三倍副本

| skill | `.agents/skills/` | `.claude/skills/` | `.cline/skills/` |
|---|---|---|---|
| `tuistory` | 5647B | 5647B | 5647B |
| `publish-cli` | 13677B | 13677B | 13677B |
| `publish-desktop` | 18019B | 18019B | 18019B |
| `publish-extension` | 19380B | 19380B | 19380B |
| `opentui` | 7789B | 7789B | — |
| `cline-sdk` | 8790B | 8790B | — |
| `create-pull-request` | ✓ | — | — |
| `publish-ui` | — | — | ✓ |

**逐字节实测**（`cmp -s`，本轮）：`opentui`、`tuistory`、`publish-cli`、`publish-desktop`、`publish-extension` 在 `.agents/` 与 `.claude/` 下**完全相同**；`tuistory`、`publish-cli`、`publish-desktop`、`publish-extension` 在三个目录下**全都相同**。

→ **硬结论**：本仓用「同一 skill 在 3 个工具目录各存一份」来适配多 harness。代价是**修改一处要同步三处**，且没有任何 sidecar 或生成标记来保证同步（对比 `deepseek-harness` 的 `.i18n.yaml`）。这是「agent 面重复」的**可量化样本**。

### 3.3 12 个根级 dotdir——本样本最多

```
.agents .changeset .claude .cline .clinerules .codex .github .greptile .husky .kanban .vscode
```

**判据**：「按工具分置」推到极致时，仓库根会变成**工具目录的集合**。其中 `.changeset`（发版）、`.greptile`（代码审查 bot）、`.kanban`（任务板）已超出「AI 编码」范畴，属于**开发流程工具面**。

## 4. 与既有结论的冲突（反证）

| 既有结论 | 本轮实测 | 判定 |
|---|---|---|
| D09 实测写 `AGENTS.md`「根；可分级到 `docs\AGENTS.md`、`packages\AGENTS.md`」 | 本仓分级路径是 `sdk/AGENTS.md`、`sdk/packages/llms/AGENTS.md`；且根级 `AGENTS.md` **无 H1** | 分级机制一致；**格式边界需补**「首行不必然是 H1」 |
| D12 `SKILL.md` 位置「`skills\<name>\SKILL.md`（也可在包内）；memU 直接放根级」 | 本仓三处落点：`.agents/skills/`、`.claude/skills/`、`.cline/skills/`，**内容逐字节相同** | **需补第三种落点：工具名前缀目录**，并补一条「同一 skill 在多工具目录重复」的形态 |
| `sources/repos/index.csv` 关键词含 `skill-dirs` | 实测确认 | 一致 |

## 5. 空白与未取证

- **未读** `.clinerules/*.md` 任何一份的正文（只在 §3.2 列了文件名）。
- **未核对** `.github/copilot-instructions.md` 与 `AGENTS.md` 的内容重叠度。
- **未确认** `create-pull-request` 为何只在 `.agents/` 下、`publish-ui` 为何只在 `.cline/` 下（可能是增量漂移的证据，也可能是设计）。
- **未统计** `docs/`、`evals/` 目录结构。
- 以上均属「在本次检索范围内未查」。
