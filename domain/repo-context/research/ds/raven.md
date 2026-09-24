# Raven 文档体系拆解

> 源：`D:\workspace\memory\sources\repos\Raven\`
> 规模实测：`.md` 307 个（其中 `.zh-CN.md` / `.zh.md` 15 个）；`docs\specs\` 54 个、`docs\plans\` 28 个。
> 一句话定位：一套**以"硬约束 + 领域语言表 + 计划/规格双轨"为骨架**的体系——文档数量不大，但三份核心文档（AGENTS / CONTEXT / CONTEXT-MAP）承担了极重的规范职责。

---

## 0. 这是什么项目的文档

Raven 自称 "Raven AI-collaboration spec"（见 `AGENTS.md:3`），是一个 Python Agent runtime（`raven\`，走 `uv`），带 TUI（`ui-tui\`，React/Ink）、Web（`ui-web\`）、WhatsApp 桥（`bridge\`）、evolver、plugins-dist 与 docs-site。文档体系的特征不是"多"，而是**规范密度高、层级引用严**。

---

## 1. 文档拓扑

```
Raven\
├── AGENTS.md              (413 行)  ← 【唯一的规范入口】硬约束 only，§N.M 编号
├── CLAUDE.md              (1 行)    ← 内容就是 "./AGENTS.md"
├── CONTEXT.md             (2646 行) ← 【领域语言表】术语正典 + _Avoid_ 反例
├── CONTEXT-MAP.md         (24 行)   ← 【上下文地图】多 context 导航 + 架构术语路由
├── README.md / README.zh-CN.md      ← 对外门面（zh 后缀用 .zh-CN）
├── CHANGELOG.md  (1015 行)
├── CONTRIBUTING.md (55) / RELEASING.md (94) / SECURITY.md (25) / NOTICES.md (85)
├── CODE_OF_CONDUCT.md / LICENSES\README.md
│
├── docs\                            ← 设计记录 + 开发者参考
│   ├── README.md                    ← 【docs 索引】逐项列出，并声明哪些是"日期记录"
│   ├── dev.md                       ← 本地开发笔记
│   ├── specs\ (54)                  ← 设计记录：YYYY-MM-DD-<slug>-design.md
│   │   └── 另有少量恒久 spec：playbook-spec.md、evolve-bench-contract.md、
│   │       self-evolution-loop-sop.md、self-evolution-loop-raven-mapping.md
│   ├── plans\ (28)                  ← 历史实现计划：YYYY-MM-DD-<slug>.md，明确是 archive
│   ├── sandbox\                     ← BoxLite 沙箱用法/调试
│   ├── examples\                    ← benchmark / runtime 配置样例
│   ├── TRACING_STANDARD_API.md      ← raven ↔ raven-tracing 的 span 契约
│   ├── research-report-quality.md / memory-plugin-architecture.md /
│   │   skill-hub-integration-design.md / everos-memory-e2e-test-plan.md
│   └── Proactivity-Plan.md / -Implementation.md / -Cost-Analysis.md
│
├── ui-tui\CONTEXT.md                ← 【模块级 context】TUI 的领域语言
├── agents\README.md + BUILDING.md   ← "Agents over ACP" 这个 context
├── i18n\messages.json               ← 代码运行时的 zh 消息目录
├── docs-site\                       ← 双语文档站
└── 各子目录 README.md（benchmarks\ / demos\ / docker\ / raven\ / scripts\ / tests\ / evolver\）
```

---

## 2. 三种"真相源"各司其职

Raven 把文档分成**职责不同、互不重述**的三类，这是理解它整个体系的关键：

| 文档 | 回答 | 性质 | 变更频率 |
|---|---|---|---|
| `AGENTS.md` | **必须怎么做、绝不能碰什么**（How / Boundary） | 硬约束，违反即被 revert | 低（`Maintenance` 章明说"越短越好"） |
| `CONTEXT.md` | **某个词在本项目是什么意思**（What it means） | 领域语言正典 | 中（随术语收敛） |
| `docs\specs\` `docs\plans\` | **当时做了什么决策、怎么落地**（What/Why historically） | 带日期的事实记录 | 只增不改（历史冻结） |

`AGENTS.md:7` 自己划了边界：

> Hard constraints only（违规会被 revert / 拒绝）。软建议与风格偏好属于个人笔记或对话，**不属于这里**。新增章节前先读 [Maintenance](#maintenance) 注记——越短越好。

这句话把"AGENTS.md 变成垃圾桶"的常见病直接封死。

---

## 3. CONTEXT 体系：多上下文地图

这是 Raven 最有辨识度的设计——**领域驱动设计的 Bounded Context 映射，落到 Markdown**。

- `CONTEXT-MAP.md`（仅 24 行）是**地图**，列出：

  ```
  ## Contexts
  - [Raven Runtime](./CONTEXT.md) — the Python agent runtime: channels, spine, agent loop, engines, providers
  - [TUI](./ui-tui/CONTEXT.md) — the terminal frontend (`ui-tui/`, React/Ink); talks to the Runtime only via the RPC protocol
  - [Agents over ACP](./agents/README.md) -- the agent-serving vocabulary ...

  ## Relationships
  - **TUI ↔ Runtime**: communicate exclusively over the RPC protocol (`raven/rpc/`); the TUI never imports Runtime internals
  - **UI ↔ Runtime**: `ui-web/` is the served page, over the same protocol via `raven serve`'s WebSocket ...
  - **bridge/ (WhatsApp TS)**: part of the Runtime context's channel boundary, not a separate context

  ## Architecture terms (routing)
  The five-layer vocabulary lives in `CONTEXT.md`; look these up there:
  **Kernel** ... **Paper** ... **Assembly Root** ... **Layer Seats** ...
  ```

- `CONTEXT.md`（2646 行）是**每个 context 内部的术语正典**：分节（如 `### Agent Core`），每条术语给"定义 + 具体路径/不变量 + `_Avoid_:` 反例"。例如 `**Model binding**` 条目不仅定义"模型 id + 提供者凭据作为一个值"，还指出路径 `raven/providers/binding.py`，并声明 `_Avoid_: "the current model" / "the active provider"`——**同时禁止两种模糊说法**。
- `ui-tui\CONTEXT.md`、`agents\README.md` 是各自 context 的词汇表，由 CONTEXT-MAP 统一路由。

**设计意图**：让 Agent 在命名与理解时先查 CONTEXT-MAP → 找到对应 context 的 CONTEXT.md，用**正典术语**，避免"约定俗称与项目人为定义冲突"（正好回应本仓库 `README.md` 中"符合 ai 时代的命名"议题）。`AGENTS.md` §6 也强制："命名前先查 `CONTEXT-MAP.md`，使用正典术语"。

---

## 4. plan / spec 双轨：过程与结论分离

Raven 用两个目录承载"决策"，且**职责严格区分**：

| | `docs\plans\` | `docs\specs\` |
|---|---|---|
| 命名 | `YYYY-MM-DD-<slug>.md` | `YYYY-MM-DD-<slug>-design.md` |
| 回答 | **怎么做**（任务分解、文件清单、约束、checkbox） | **是什么**（设计目标、决策、as-built） |
| 生命周期 | 历史存档，"deliberately not held to today's layout" | 描述"截至其日期的树"，每条带 `Status:` |
| 是否可过期 | 是（带 Superseded 横幅） | 是（明确是 dated record） |

**plan 的典型骨架**（`docs\plans\2026-08-05-session-workspace.md`）：

- 顶部横幅：`> **Superseded — kept as a task record.**` + 说明哪些内容已不成立 + 链接到实际落地的 spec
- `> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development …`（**给执行 Agent 的机器指令**，任务用 `- [ ]` checkbox）
- `**Goal**` / `**Architecture**` / `**Tech Stack**` / `**Spec:**`（链接对应 spec）
- `## Global Constraints`：**逐条引用 `AGENTS.md` 章节号**，例如
  `(AGENTS.md section 4)` `(AGENTS.md section 5.4)` `(AGENTS.md section 2.2)`
- `## File Structure`：`**Created:**` / `**Modified:**` 表格，每行"文件 → 职责"

**spec 的典型骨架**（`docs\specs\2026-08-05-session-workspace-design.md`）：

- 头部：`Date: 2026-08-05 (rewritten 2026-08-07 after the first design was withdrawn)` + `Status: implemented`
- `## Goal` → 问题拆分（"`workspace` 曾同时指两件事，拆开它"）→ 决策与后果（含"对运行中 gateway 的 4 条影响"编号清单）

**这套双轨的价值**：plan 可以被取代、被撤销而不污染"当前是什么"；spec 记录设计意图与落地状态；两者用**相对链接**互指（plan 顶部链到 spec），使"历史计划"与"当前事实"永远能对上。这正是 dsh 的 notes 状态机要解决的同一个问题——**只不过 dsh 用"状态即目录 + 冻结归档"，Raven 用"plan/spec 分目录 + 横幅声明"**。

---

## 5. AGENTS.md：唯一权威 + 可被引用的编号

`AGENTS.md` 是全仓库**唯一**的规范入口，风格高度工程化：

- 开篇声明权威优先级：`When a rule here conflicts with an ad-hoc instruction in conversation, this file wins — unless the user explicitly says "ignore rule X in AGENTS.md"`（`AGENTS.md:5`）。即**文件 > 对话中的临时指令**，除非用户显式豁免。
- 开篇有**总目录表**（`| # | Section | Gist |`）——7 节速览。
- 每节用 `## N. 标题` + `### §N.M` 编号（如 `§1.1` `§3.5`）。
- 大量 **✅ Good / ❌ Bad 对照表**（分支命名、commit message、代码注释）。
- 关键规则附带 **Why** 段（如 §3.1.1 ASCII-only 的 why、§3.5 rebase 的 why）。
- **可被其它文档精确引用**：plan 里写 `(AGENTS.md section 4)`，链回规范——规范与执行文档之间形成稳定的引用契约。

`CLAUDE.md` 只有一行，内容是 `./AGENTS.md`——与 dsh 的 9 字节指针同构，用**内容重定向**让不同 harness 落到同一份规范。

---

## 6. 文档纪律：索引 + dated banner

与 dsh 相反，Raven **有** `docs\README.md` 索引，并在其中做了明确的**性质声明**：

> This directory holds design notes, dated records, and developer references that are too detailed for the main README.
> … Several files below are dated records kept for their history rather than **descriptions of the current tree**; each such file carries a **banner** saying so.

即：索引不只是目录，还是"**这一段到底是不是当前事实**"的诚实标注。具体到每个过期文件，用顶部 banner 自我声明（如 plan 的 `Superseded — kept as a task record.`）。

`docs\README.md` 还逐项说明每类文档的定位，例如把 `specs\` 描述为"dated design records（`YYYY-MM-DD-*.md`）+ self-evolution SOP 与 playbook specs；**each describes the tree as of its date**"，把 `plans\` 描述为"historical implementation plans; an archive, deliberately not held to today's layout"。

---

## 7. 语言边界：English 默认 + 具名豁免区

Raven 对"什么语言写在哪儿"有机器强制的规则（`AGENTS.md §1.3`）：

- 仓库源码**全英文**（注释、字符串常量、prompt、日志、测试夹具、docs）。
- **豁免区（exemption zones）** 是 owner 签名的白名单，CJK 仅在区内、且仅作为特性所需的能力数据出现：
  `plugins-dist/ppt-engine/`、`tests/test_ppt_engine_*`、`plugins-dist/design-engine/`、`tests/test_design_engine_*`、`docs-site/`、`raven/i18n/`、`raven/templates/prompts/zh/`、`tests/test_i18n_*`。
- **Markdown 自我治理**：`*.md` 后缀被门禁整体豁免——所以 `README.zh-CN.md` 与 `docs\` 的中文散文合法；但 `docs\` 下非 markdown 文件**没有**兜底豁免。
- 机器执行：`scripts\check_source_language.py` 逐 PR 检查新增行（`make check-source-language`），与 `make check-large-files`（§7 禁止大文件）同类。
- 翻译资源落在 `i18n\messages.json`（代码运行时目录），文档翻译落在 `docs-site\` 与 `.zh-CN.md` 文件。

对比 dsh：Raven 是**"默认英文 + 具名豁免 + 门禁"**，dsh 是**"全量双语配对 + 行对齐 + sidecar"**。前者的翻译成本低、覆盖面窄；后者的翻译是结构契约、覆盖全文档。

---

## 8. 设计要点提炼

1. **规范单入口**：`AGENTS.md` 是唯一硬约束源，其它文档引用它的章节号，不复制它的规则。
2. **语言正典独立成文**：`CONTEXT.md` + `CONTEXT-MAP.md` 让"术语"与"规则"分离，且支持多 context 的自相似结构（每个模块一份 CONTEXT.md）。
3. **过程与结论分离**：plan（过程，可废弃）vs spec（结论，as-built），互链。
4. **诚实标注时效**：dated banner + docs 索引里的性质声明，让读者一眼知道"这是当前事实还是历史"。
5. **规范密度靠纪律**：`Hard constraints only` + `更短更好` + 引用而非重述，抑制规范臃肿。
6. **语言边界可执行**：豁免区是具名白名单 + 脚本门禁，不靠自觉。

---

## 附：可直接借用的模式

- **CONTEXT-MAP.md → 每 context 一份 CONTEXT.md**：用 DDD 的 bounded context 组织领域语言，`_Avoid_:` 反例是术语收敛的关键杠杆。
- **plan 顶部 `For agentic workers: REQUIRED SUB-SKILL …` + `- [ ]` 任务**：把计划写成可被 Agent 直接执行的工单。
- **plan 的 Global Constraints 逐条引用 `AGENTS.md section N`**：规范与执行之间的稳定引用契约。
- **`Superseded — kept as a task record` 横幅**：一条廉价、诚实的"此文档已过期"提示。
- **CLAUDE.md = `./AGENTS.md`**：多 harness 共享单份规范的零成本重定向。
- **豁免区 + `check_source_language.py`**：语言规则从口头约定升级为可执行门禁。
