# Raven · 根目录文档实测

> 快照 `e17694113b13` · 取证 2026-09-25 · 来源 `sources/repos/Raven/`
> 状态：verified ｜ 覆盖范围：仓库根目录直接子文件 + agent 面（`docs/`、`AGENTS.md` 分级、skills）

## 1. 根目录清单一览

| 文件 | 字节 | kind | 角色(D) | 一句话 |
|---|---|---|---|---|
| `AGENTS.md` | 22349 | agent-entry | D09 | AI 协作规范（硬约束），含 §N.M 编号与章节速查表 |
| `CLAUDE.md` | 22349 | agent-entry | D10 | **与 `AGENTS.md` 逐字节相同**（见 §4） |
| `CONTEXT.md` | 194587 | semantic | D14 | PyAgent runtime 的领域语言正典，**190KB**，本样本最大单文档之一 |
| `CONTEXT-MAP.md` | 1565 | semantic | D16 | 多上下文地图：本仓有几个 context、各自术语表在哪 |
| `README.md` | 28307 | facade | D01 | 门面 |
| `README.zh-CN.md` | 27936 | facade | D01 | 中文对照 |
| `CHANGELOG.md` | 85170 | record | D02 | 变更流水，首节 `## Unreleased` |
| `RELEASING.md` | 4123 | record | D05 | 发版步骤，首节 `## Versioning` |
| `CONTRIBUTING.md` | 1519 | collab-rule | D03 | 极短（1.5KB）：要求小 PR、绑需求 |
| `CODE_OF_CONDUCT.md` | 648 | collab-rule | D03 | 本仓自定版，非 Contributor Covenant 全文（648B） |
| `SECURITY.md` | 662 | collab-rule | D04 | 漏洞上报 |
| `NOTICES.md` | 4706 | legal | D06 | 第三方声明（Apache-2.0 本仓 + 若干 MIT 组件） |

## 2. 逐文件分析

### 2.1 `AGENTS.md`（22349 字节）

- **取到的原文**：L1 `# AGENTS.md`（`L1=204aa1e7`）；L3 `Raven AI-collaboration spec. **Read this file before making any code change in this repo.**`
- **L5 定范围**：`Scope: Codex / Claude Code / Claude API / any AI-assisted work. When a rule here conflicts with an ad-hoc instruction in conversation, **this file wins** — unless the user *explicitly* says "ignore rule X in AGENTS.md".`
- **L7 定边界（本样本最锋利的一句）**：`Hard constraints only (violations get reverted / rejected). Soft suggestions and style preferences belong in personal notes or conversation, not here. See the [Maintenance](#maintenance) note before adding sections — shorter is better.`
  → 直接回答「AGENTS.md 该不该塞一切」：**不塞**。风格偏好去个人笔记或对话，这里只留会被 revert 的硬约束。
- **L9–L12 是一张速查表**（`| # | Section | Gist |`），把 §1 代码注释、§2 分支命名、§3 提交规范…压成一句话索引。
- **它是「被读」还是「被 grep」**：编号 `§N.M` + 章节表，使得 `docs/plans/**` 能逐条回引（如「见 AGENTS.md §3.4」），把规范变成可寻址对象。

### 2.2 `CLAUDE.md`（22349 字节）

- **判定**：**整份复制**。`cmp -s AGENTS.md CLAUDE.md` → 逐字节相同；L1 哈希同为 `204aa1e7`，L3/L5/L7 亦逐行相同。
- **含义**：与 DSH 同型。Raven 的 `AGENTS.md` 里写着 *"this file wins"*，但它有两份逐字节相同的物理副本——**「哪个文件赢」这件事在文件系统层面没有强制机制**。

### 2.3 `CONTEXT.md`（194587 字节）与 `CONTEXT-MAP.md`（1565 字节）

- **CONTEXT.md**：首行 `# Raven Runtime`，自述 *"The Python agent runtime: receives messages from chat channels, runs the agent loop against LLM providers, and hosts the feature engines (context, memory, proactive, eval)"*。190KB 的术语正典，条目带 `_Avoid_:` 反例（`02docsdefine` D14 已记录）。
- **CONTEXT-MAP.md**：`## Contexts` 下逐条列出各 context 及其正典文件（如 `[Raven Runtime](./CONTEXT.md)`）。
- **分工判据**：MAP 是**路由**（去哪查），CONTEXT 是**内容**。190KB 的单文件正典与 1.5KB 的路由文件拆开，正是「回答不同问题 / 读取场合不同」的教科书级例子。

### 2.4 `CONTRIBUTING.md` 只有 1519 字节

与 `goose/CONTRIBUTING.md`（16647B）、`qwen-code/CONTRIBUTING.md`（12173B）相比极短。**同一类型在不同仓的体量差一个数量级**——「CONTRIBUTING」这个名字不承诺内容规模。

## 3. Agent 面（vibe coding 相关文件管理）

### 3.1 指令分级：只有 3 份非夹具的 `AGENTS.md`

```
AGENTS.md                              ← 根：AI 协作规范
raven/templates/AGENTS.md              ← 子树：模板目录专属
plugins-dist/ppt-engine/raven_ppt/prompts/AGENTS.md
tests/fixtures/vendored_fork/raven-ppt/.../raven/templates/AGENTS.md   ← 夹具里的第二份，重复
```

`tests/fixtures/vendored_fork/` 下那份是**vendored 拷贝**，与研究对象的治理无关。分级规模（根 + 1）远小于 DSH（22）与 gemini-cli（8）。

### 3.2 `docs/` —— 「记录」与「现况」分家的显式声明

`docs/README.md` 全文 37 行，是**本样本里对「records 与 docs 职责」回答得最直白的一份**：

- L3–L4：*"This directory holds design notes, dated records, and developer references that are too detailed for the main README."*
- L7–L9（关键）：*"Several files below are dated records kept for their history rather than descriptions of the current tree; **each such file carries a banner saying so**."*
  → 时态不是靠目录位置区分的，而是靠**文件自带的横幅**声明。
- L24–L27：
  - `specs/` — *"dated design records (`YYYY-MM-DD-*.md`) … each describes **the tree as of its date**"*
  - `plans/` — *"historical implementation plans; **an archive, deliberately not held to today's layout**"*
  → plan 与 spec 是两个**互不承担「当前状态」义务**的归档目录；当前状态归 `CONTEXT.md` 与源码。

实测规模：`docs/plans/` 34 篇（7KB–127KB），`docs/specs/` 40+ 篇（`*-design.md`，最大 105KB）。`docs/` 另有 `examples/`、`sandbox/` 两个子目录与 11 份顶层文档（`dev.md`、`browser-and-desktop.md`、`TRACING_STANDARD_API.md`、`memory-plugin-architecture.md`、`Proactivity-{Plan,Implementation,Cost-Analysis}.md` …）。

### 3.3 Skills：22 份，但绝大多数属于**产品资产**而非开发工作流

分布：

| 位置 | 数量级 | 性质 |
|---|---|---|
| `plugins-dist/design-engine/raven_design/skills/` | 17 | **随产品分发的设计能力**（`build-interactive-explainers`、`design-typefaces-and-lettering` …） |
| `agents/raven-design/skills/deck-to-pptx` | 1 | 内置 agent 的 skill |
| `raven/memory_engine/skills/{subagent-dag-orchestration,weather}` | 2 | 运行时 skill |
| `demos/skill_retrieval/skills/image-gen` | 1 | 演示夹具 |

**推论**：把「有 22 个 SKILL.md」直接读成「这个仓的开发工作流很丰富」是错的。同一目录名 `skills/` 在 `plugins-dist/` 下是**产物**，在 `.agents/` 下才是**工作流**。分类时必须带路径前缀。

### 3.4 工具目录

根级 dotdir 只有 `.github/`。**无 `.agents/`、无 `.claude/`、无 `.cursor/`**——但存在根级 `CLAUDE.md`，说明「Claude 入口」不必然伴随 `.claude/` 目录。

## 4. 与既有结论的冲突（反证）

| 既有结论 | 本轮实测 | 判定 |
|---|---|---|
| `02docsdefine\ds.md` D10：Raven `CLAUDE.md` = 一行 `./AGENTS.md`（指针） | `cmp -s` 退出 0；两文件均 **22349 字节**；L1/L3/L5/L7 哈希逐行相同 | **D10 已失效**。当前快照是**整份复制**，不是指针 |
| D14：Raven `CONTEXT.md`=2646 行 | 字节数实测 194587；**行数本轮未测** | 待补（不据字节数反推行数） |
| D28：`docs/plans/` 带 `Superseded` 横幅 + `For agentic workers` 子技能 | 本轮只实测到 34 篇文件与 `docs/README.md:26` 的归档声明 | 部分一致；横幅与子技能**本轮未逐篇核对** |

## 5. 空白与未取证

- **未逐份读** `docs/plans/**` 与 `docs/specs/**` 的正文；只据 `docs/README.md` 的声明与文件尺寸定性。
- **未核对** `CONTEXT.md` 的 `_Avoid_:` 反例条目数与行数。
- **未确认** `plugins-dist/` 是否在 `.gitignore` 内（若被排除，则那 17 个 skill 不得计入「仓内资产」）。
- **未取证** `docs-site/mkdocs.yml` 与 `docs/` 的发布关系。
- 以上均属「在本次检索范围内未查」。
