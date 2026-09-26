# Tianshu-harness · 根目录文档实测

> 快照 `79c10d30ba4f` · 取证 2026-09-25 · 来源 `sources/repos/Tianshu-harness/`
> 状态：verified ｜ 覆盖范围：仓库根目录直接子文件 + `docs/` 总纲与目录地图 + `AGENTS.md` 分级 + `.rivet/`

## 1. 根目录清单一览

| 文件 | 字节 | kind | 角色(D) | 一句话 |
|---|---|---|---|---|
| `AGENTS.md` | 14896 | agent-entry | D09 | 首行 `# 天枢 (Tiānshū) — Architecture Map`，**是架构地图不是操作守则** |
| `CLAUDE.md` | 17418 | agent-entry | D10 | 与 `AGENTS.md` **不同**的两份文档（见 §2.2） |
| `star.md` | 85689 | semantic | D17 | 项目立论 / 思想文档（星域公理），**85KB** |
| `README.md` | 26771 | facade | D01 | 门面正本（中文） |
| `README.en.md` | 81089 | facade | D01 | 英文 |
| `README.ja.md` | 115798 | facade | D01 | 日文 |
| `README.ko.md` | 104222 | facade | D01 | 韩文 |
| `CHANGELOG.md` | 60769 | record | D02 | 按日期分段的变更流水（`## 2026-09-13 — …`） |
| `CONTRIBUTING.md` | 7738 | collab-rule | D03 | 明说哪些可自由贡献、哪些需特别处理 |
| `CODE_OF_CONDUCT.md` | 1408 | collab-rule | D03 | 采用 Contributor Covenant 2.1（引用，非全文） |
| `SECURITY.md` | 3048 | collab-rule | D04 | 中英双语同文件 |
| `CONTRIBUTORS.md` | 16096 | legal | D06 | 贡献者名单 |
| `CREDITS.md` | 18178 | legal | D06 | **署名台账**，自述「本文件是公开仓那份台账的初始骨架」 |
| `EXTERNAL-PRS.md` | 3278 | collab-rule | — | 外部 PR 处置说明：公开仓是 dev 仓的投影，外部 PR 从不直接合并 |
| `.rivet.md` | 4359 | machine | — | 本 harness 自己的项目级配置，落在仓库根 |

## 2. 逐文件分析

### 2.1 `AGENTS.md`（14896 字节）—— 命名与职责的漂移

- **取到的原文**：L1 `# 天枢 (Tiānshū) — Architecture Map`（`L1=fcb4b680`）；L3 `> v2.19.6 · 顶层目录索引 + 能力全景。文件级细节用工具 \`repo_map\` / \`repo_graph\` 按需获取。`
- **冲突点**：`02docsdefine\ds.md` D09 的边界写「AGENTS.md **不解释『系统是什么』**（→ARCHITECTURE/CONTEXT），只规定『怎么执行』」。本仓 `AGENTS.md` 恰恰**就是**系统地图，含「项目定位 / 能力全景 / 内置星域 / 顶层目录 / Runtime Data Layout / 缓存排查指南 / 相关源码」。
- **它为什么可以这样**：L3 那句给了机制——**地图只到目录级，文件级交给工具现查**。所以它不是「架构文档搬进了 AGENTS」，而是「AGENTS 只保留够用的定位信息 + 把细节外包给 `repo_map`」。
- **与之配对**：L4 指向 `docs/architecture-overview.md`（架构总览）与 `star.md`（星图叙事）。

### 2.2 `CLAUDE.md`（17418 字节）—— 互补分工，不是复制

- **取到的原文**：L1 `# 天枢 (Tianshu) / Rivet`（`L1=9ace2df1`）；L3 项目定位（Node.js 24 / TypeScript strict / 纯 ANSI 终端 UI / `desktop/` 闭源 / `vscode-extension/` 开源）；L5 `顶层索引与运行时排查：[\`AGENTS.md\`](./AGENTS.md)。架构总览：[\`docs/architecture-overview.md\`](./docs/architecture-overview.md)。`；随后是 `## Build & Test` 与命令。
- **判定**：`cmp -s` 退出 1（14896 vs 17418 字节），哈希不同 → **两份不同文档**。
- **分工**：`CLAUDE.md` 承载**可执行命令面**（`npm install && npm run build`、`npm test`、`npm run typecheck` 及其坑位说明），并把 `AGENTS.md` 称作「顶层索引」。二者是「索引 ↔ 命令手册」，不是正本 ↔ 副本。

### 2.3 `star.md`（85689 字节）—— 草案里 `THESIS.md` 的现实对应物

首行 `# 天枢（Tianshu Harness）`，自述 `面向 Foundation Model Agent 的认知运行时（CVM）——稳定交付、证据门禁、不虚报完成`，含 `## 起源` 等章节。`02docsdefine` D17 已记为「唯一实例」。

### 2.4 语言变体：`README.md` + `.en` + `.ja` + `.ko`（共 328KB）

四份**体量差 3–4 倍**（26KB / 81KB / 116KB / 104KB）。同类型文档的多语言变体**不做内容对齐声明**，也没有 sidecar（对比 `deepseek-harness` 的 `.i18n.yaml`）。

## 3. Agent 面（vibe coding 相关文件管理）

### 3.1 指令分级：根级 2 份，子树 0 份

```
AGENTS.md    ← Architecture Map
CLAUDE.md    ← 命令手册 + 指向 AGENTS.md
```

全仓仅此两份（`find -name AGENTS.md -o -name CLAUDE.md` 实测无第三份）。与 DSH（22+4）、gemini-cli（8）形成三个量级。

### 3.2 `docs/` —— 本样本里**唯一**「受控类型枚举 + 生成式索引」的完整实现

`docs/README.md`（总纲，自述「文档类型、目录地图、命名规范、frontmatter 标准、索引用法」）给出 12 个受控 `type` 与各自的落点/命名：

| type | 职责 | 落点 | 命名 |
|---|---|---|---|
| `plan` | 执行计划：任务分解 + checkbox 追踪 | `plans/` | `YYYY-MM-DD-主题.md` |
| `spec` | 事前规格：做什么/为什么 | `specs/` | `YYYY-MM-DD-主题.md` |
| `design` | 事前权衡：怎么做（trade-off + 备选） | `design/` | `YYYY-MM-DD-主题.md` |
| `decision` | 决策记录（ADR 五段式） | `decisions/` | `NNNN-标题.md`（单调递增、**绝不复用**） |
| `analysis` | 事后归因 / 复盘 / handoff | `analysis/` | `YYYY-MM-DD-主题.md` |
| `research` | 外部调研 | `research/` | `YYYY-MM-DD-主题.md` |
| `changelog` | 变更记录 | `changelog/` | `YYYY-MM-DD-主题.md` |
| `issue` | 单点问题追踪 | `known-issues/` | `YYYY-MM-DD-主题.md` |
| `release` | 版本发布说明 | `releases/` | `v2.x.y.md`（语义命名） |
| `guide` | 手册指南 | `guides/` | 语义命名，无日期前缀 |
| `reference` | 架构参考 / 长期有效资料 | `reference/` | 语义命名，无日期前缀 |

**这张表直接回答了「records 与 docs 怎么划」**（`05docs文件夹\AGENTS.md` 里那个困惑）：

- 边界判据（总纲 L29–L34）：*「要不要做、做成什么样」→ `spec`；「怎么实现、为什么这么实现」→ `design`；「下一步谁做什么」→ `plan`；「为什么选了 A 不选 B」的单点决策 → `decision`（不从属任何 feature，长期有效）；「发生了什么、根因是什么」→ `analysis`；「改了哪些东西」→ `changelog`。*
- `docs/decisions/README.md` 补三条纪律：编号 `NNNN-标题.md` **单调递增、绝不复用**；被推翻的决策**不删档**（状态改 `superseded`，替代者 frontmatter 写 `supersedes`）；模板 `docs/_templates/_decision.md`。

**索引由脚本生成，不手维护**（总纲 L3–L4、L89）：`INDEX.md`（人读，按 type 分组、日期倒序、含状态列）/ `docs.json`（机读，供脚本消费）/ `MINDMAP.md`（结构图），三者全由 `scripts/docs-index.ts` 产出。理念自述：*「元数据内嵌、索引生成——元数据写在每篇文档头部的 frontmatter 里，索引是构建产物，可随时重建（借 KEP/PEP 范式）。**手维护的总索引必然腐烂**。」*

**模板**：`docs/_templates/` 下 7 个（`_analysis` / `_changelog` / `_decision` / `_design` / `_plan` / `_research` / `_spec`），对应上表各类型。

**工具草稿区与晋升路径**（总纲 L53，逐字）：*「工具草稿区（\`.rivet/plans/\`、\`.cursor/plans/\`、\`.zcode/plans/\`）是各 agent 工具的运行时产物，**不改其行为**；定稿后的晋升路径：按命名规范移入对应 docs 类型目录 + 补 frontmatter。」*
→ 显式划出「工具自留地」与「受控文档区」，并规定**单向晋升**。这是本样本独有的机制。

**兼容策略**（总纲 L81）：索引生成器三级兜底——frontmatter 优先；无 frontmatter 时用文件名日期前缀 + blockquote 元信息头 + 首个 H1。存量文档不强制补。

### 3.3 Skills：8 份，三分天下

| 位置 | 性质 |
|---|---|
| `docs/skills/optional/agent-harness-testing` | 开发工作流 |
| `plugins/{design,office-docx,office-excel,office-pdf,office-ppt}/skills/` | 随插件分发的能力 |
| `runtime-assets/bundled-skills/{brainstorming,visual-acceptance}` | 运行时内置 |

### 3.4 根级 `.rivet/`

仓内就有一个 `.rivet/` 目录（本 harness 的运行时数据布局）。加上根级 `.rivet.md`，构成「配置在根级明文、运行时数据在 `.rivet/` 内」的一对。

## 4. 与既有结论的冲突（反证）

| 既有结论 | 本轮实测 | 判定 |
|---|---|---|
| D09 边界：「AGENTS.md 不解释『系统是什么』」 | 本仓 `AGENTS.md` L1 即 `— Architecture Map`，含项目定位/能力全景/目录索引 | **反例成立**。D09 需要补一条「AGENTS.md 可承载**目录级**系统地图，细节外包给工具」的边界说明，否则会把本仓判为违规 |
| D19 INDEX：「TS `docs\INDEX.md`」，并记为路线分裂三方之一（做 / 不做 / 变形） | 总纲明写 INDEX.md / docs.json / MINDMAP.md **均由脚本生成** | **信息不足**：`02docsdefine` 只记了「有 INDEX.md」，未记「索引不手维护、且有机器可读的 docs.json」。这是 D19 三方对比里最有分歧价值的一条，当前记录不足以支撑对比 |
| D26 ROADMAP：根级零命中 | 本仓确实无 `ROADMAP.md` | 一致 |

## 5. 空白与未取证

- **未逐份读** `README.en/ja/ko.md`——只测了字节数与首行（`<p align="center">`，四份皆同）。
- **未验证** `scripts/docs-index.ts` 的实际行为（是否存在、是否可真跑）：本轮只读了总纲的自述。**这是典型「文档声称 vs 实现」的待验证点。**
- **未统计** `docs/` 下各类型目录的实际文件数（`superpowers/` 自述含 plans 339 / specs 212，未核）。
- **未取证** `docs/{stars,brand,dev,prompt-changelog,prompt-versions,cache-baseline,teamtask}/` 各自的内容形态。
- **未确认** 根目录下那个同名 `Tianshu-harness/` 子目录是什么（疑为构建产物）。
- 以上均属「在本次检索范围内未查」。
