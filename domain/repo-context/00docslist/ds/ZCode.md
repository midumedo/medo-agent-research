# ZCode · 根目录文档实测

> 快照 `29628c9acdb8` · 取证 2026-09-25 · 来源 `sources/repos/ZCode/`
> 状态：verified ｜ 覆盖范围：仓库根目录直接子文件 + `.agents/skills/` + `architecture-policy.yaml`
> **注意**：`sources/repos/index.csv` 对本仓的 `completeness` 是 `source-partial`（`.gitignore` 排除了 `bundled-agents/`、`bundled-tools/`、`prebuilds/`）。

## 1. 根目录清单一览

| 文件 | 字节 | kind | 角色(D) | 一句话 |
|---|---|---|---|---|
| `AGENTS.md` | 6387 | agent-entry | D09 | **无 H1**，首节 `## 核心原则`；**中文正文** |
| `CONTEXT.md` | 4316 | semantic | D14 | 领域词汇表，范围限定为「插件商店」：首行 `# ZCode 插件商店（Plugin Store）` |
| `DESIGN.md` | 29663 | semantic | — | 设计系统；首行即自述受众：`This file is meant for coding agents.` |
| `NOTICE.md` | 27721 | legal | D06 | **混体**：既有 AI 风险声明，又有第三方组件声明 |
| `THIRD-PARTY-NOTICES.md` | 1978939 | legal | D06 | **1.9MB**，由 `node scripts/licenses.mjs notices` 生成 |
| `README.md` | 10808 | facade | D01 | 中文门面 |
| `README.en.md` | 12149 | facade | D01 | 英文门面 |
| `architecture-policy.yaml` | 1681 | machine | — | **机器可判定的架构约束**（本样本唯一） |

## 2. 逐文件分析

### 2.1 `AGENTS.md`（6387 字节）—— 中文正文 + 无 H1

- **取到的原文**：首行 `## 核心原则`；首条 `- 新增或修改行为前，先更新对应 spec；目录不存在时按需创建。先明确产品规则、状态所有者、接口和验收场景，再实现`。
- **三个与众不同**：
  1. **无 H1**（与 `cline` 同为「首行不是 H1」，但那份至少是英文散文）。
  2. **中文正文**（本样本 18 仓里唯一）。
  3. **第一条规则是 order-of-work**：*先写 spec 再实现*，且允许按需创建目录——把「spec-first」当成首要硬约束。

### 2.2 `architecture-policy.yaml`（1681 字节）—— 把架构约束变成机器可判定的数据

实测内容结构：

```yaml
version: 1
# 存量模块先标记为 legacy；新模块或完成迁移的模块设置 managed: true。
modules:
  - id: storage
    roots: [packages/services/src/storage]
    managed: true
    requires: [shared, rpc, services]
    publicEntrypoints: [packages/services/src/storage/contract.ts]
    layers: { domain: domain, app: app, adapters: adapters }
    layerOrder: [domain, app, adapters]
    owner: desktop-settings
  - id: rpc
    roots: [packages/rpc/src]
    managed: false          # ← 存量，未迁移
  …
global:
  maxFileLines: 400
  maxContractLines: 300
  maxPublicMethods: 12
```

**它为什么重要**：本样本其余 17 仓的架构约束**都在散文里**（`docs/architecture.md`、`AGENTS.md` 段落）。ZCode 把「谁依赖谁、公开入口是哪个、分层顺序、文件行数上限」写成 yaml——**可被 linter/CI 直接判定**。

**它同时回答了「为什么需要 managed 标志」**：存量模块标 `managed: false`，新模块或完成迁移的标 `true`。这是一条**渐进迁移**的机制，而不是一次性重写。

### 2.3 `NOTICE.md`（27721 字节）—— 法务件与风险声明的**混体**

首行 `# ZCode 相关功能说明与第三方组件声明`，次行：*「本声明适用于本仓库公开的源码及其构建产物。各运行形态的功能、权限、存储位置和网络行为不同，不能将其中一种形式…」*，第一节标题是 `## 一、AI 输出、执行权限与自动化风险`。

**形态判据**：`NOTICE` 通常是纯法务声明（对比 `codex/NOTICE` 242B、`EverOS/NOTICE` 2634B）。ZCode 把**AI 风险声明**（面向用户的能力/权限说明）与**第三方组件声明**合进同一份 27KB 文档。

**与 `THIRD-PARTY-NOTICES.md`（1.9MB）并存**：两份都在根目录、都叫 NOTICE 类，但一个是人手写的风险+组件混合说明，另一个是脚本生成的完整许可证文本。**同名族里职责不同、体量差 70 倍**。

### 2.4 `DESIGN.md`（29663 字节）—— 受众是 agent 的设计系统

首行 `# ZCode Design System`，次两行：*"Portable design system for AI-assisted UI work in this repository."* / *"This file is meant for coding agents. When generating or editing UI in this repo, follow this file before inventing new visual rules."*

**判据**：`DESIGN` 这个名字在 `02docsdefine` 里没有对应条目。它既不是 `ARCHITECTURE`（不讲模块/数据流），也不是 `STYLE`（不是代码风格）。它是**给 agent 的前端规范**——把「设计系统的约束」前置到模型生成 UI 之前。属本阶段新发现的一族。

## 3. Agent 面（vibe coding 相关文件管理）

### 3.1 指令分级：根 + `apps/zcode-cli/` + **skill 目录内**

```
AGENTS.md
apps/zcode-cli/AGENTS.md
.agents/skills/react-best-practices/AGENTS.md     ← 见下
```

**第三个是异常**：`.agents/skills/react-best-practices/AGENTS.md` —— `AGENTS.md` 出现在 **skill 目录内部**。若按「`AGENTS.md` 只按子树辖域分级」的模型去扫，这一份会被误读成「react-best-practices 子树的仓库约定」，而它实际是**某个 skill 自带的说明文件**。→ 枚举 `AGENTS.md` 时必须检查其所在路径是否属于 skill/示例/fixture。

### 3.2 Skills：11 份，三处

| 位置 | 数量 | 性质 |
|---|---|---|
| `.agents/skills/` | 8 | 仓库自用工作流（`architecture-governance`、`dep-refs`、`dogfood`、`feature-boundary-planner`、`react-best-practices`、`agent-browser`、`ai-elements`、`electron`） |
| `apps/zcode-cli/packages/browser-use-plugin/skills/` | 2 | 插件能力（`control-browser`、`web-gui-tester`） |
| `apps/zcode-cli/packages/bundled-skills/skills/` | 1 | 随 CLI 分发（`dynamic-workflows`） |

`architecture-governance` 与根级 `architecture-policy.yaml` 显然配套——**skill 负责「怎么做」，yaml 负责「规则是什么」**，机器判定的那部分不靠模型自觉。

### 3.3 根级 dotdir 2 个

`.agents`、`.vscode`。**无 `.claude/`、无 `.cursor/`、无 `.github/`** —— 在 18 仓里属于最少的一档（对比 `cline` 的 12 个）。

## 4. 与既有结论的冲突（反证）

| 既有结论 | 本轮实测 | 判定 |
|---|---|---|
| D09 形态「单文件（可分级到 `docs\AGENTS.md`、`packages\AGENTS.md`）」 | 本仓有 `apps/zcode-cli/AGENTS.md`，另有 `.agents/skills/react-best-practices/AGENTS.md` | **分级模型需补一条排除规则**：skill/示例/fixture 目录下的同名文件不是辖域分级 |
| 根级目录清单里没有 `architecture-policy.yaml` 这类条目 | 本仓存在，且是仅此一家的机器可判定架构策略 | **新增命名与形态**，`02docsdefine` 无覆盖 |
| V5 边界：`CONVENTIONS`/`STYLE`「已被 `AGENTS.md` + linter 配置取代」 | 本仓把规则写成 **yaml 策略文件**（`architecture-policy.yaml`）而非 linter 配置 | **需补第三种去向**：不是 AGENTS、不是 linter，而是**独立的机器可读策略文件** |
| D14：`CONTEXT.md` 是「领域语言正典」 | 本仓 `CONTEXT.md` **限定到单个功能域**（插件商店），而非整仓 | **形态需补**：`CONTEXT` 可整仓一份，也可**每域一份** |

## 5. 空白与未取证

- **未读** `AGENTS.md` 全文（只取首 2 行）、`DESIGN.md`（29KB，只取首 3 行）、`NOTICE.md`（27KB，只取首 3 行）。
- **未核对** `README.md` 与 `README.en.md` 是否内容对齐（10808 vs 12149 字节，差 12%）。
- **未验证** `architecture-policy.yaml` 是否有配套的执行器（CI 是否真的按它判定）。
- **未确认** `.gitignore` 排除的三个目录（`bundled-agents/`、`bundled-tools/`、`prebuilds/`）对 skill/agent 计数的实际影响。
- 以上均属「在本次检索范围内未查」。
