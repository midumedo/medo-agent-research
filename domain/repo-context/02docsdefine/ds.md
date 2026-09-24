# 01 · Define —— 文档类型定义

> 属于 `domain\repo-context\` 研究，阶段 **01docsdefine**
> 目的：为研究中涉及的每一种 `.md` 给出一条**明确、可引用、可锁定**的定义。
> 上游：`README.md`（研究纲领）、`drafts\`（**草案，非教条**）、`具体md文件的初步分析.md`（**草案**）
> 下游：`02docsclassify\`、`03docscompare\`
>
> ⚠ **对草案的立场**：`drafts\总览.md`、`具体md文件的初步分析.md`，以及其它 AI 的产出（如 `02docsclassify\glm.md`）**都是草稿**——可能有幻觉、错误、内部矛盾，**不构成基线**。本文只把"能在样本仓库实测"的部分当证据；仅见于草案的框架一律标注为**待验证假设**。特别是下面"坐标"字段所用的 `时态 / 层级 / 契约对象` 三轴，来源是 `drafts\总览.md` 草案，**未经实证**，且已被 `02docsclassify\ds.md` 判定为需要改造。

---

## 0. 这份定义怎么用

**定义的对象是"类型"，不是文件。** `README.md` 在样本里有 11 份实例，但只对应 1 个类型。

每条定义有**稳定编号**（D01…）与稳定标题，便于在别处引用（例："见 `01docsdefine\ds.md` D07"）。

每条定义带一枚**状态**，取值三种：

| 标记 | 含义 | 证据要求 |
|---|---|---|
| `●` | **实证** | 在本次研究的 11 个样本仓库里找到真实文件实例（列出路径） |
| `◐` | **业界常见** | 业界/文档惯例中存在，但 11 个样本里**未见**实例——属待验证假设 |
| `○` | **仅草案** | 目前只出现在本研究的草案（`drafts\`、`具体md文件的初步分析.md`）里，样本**零命中** |

**锁定机制**：一条定义只有"定义 / 边界 / 实测"三项都无待办，才可追加 `[LOCKED]`；锁定后需要修改时，**新增一行变更记录**（日期 + 改了什么 + 理由），不覆盖旧定义。

### 样本仓库（11 个）

`deepseek-harness`（DSH）· `Raven` · `Tianshu-harness`（TS）· `codex` · `mem0` · `memU` · `MemOS` · `MemoryBear` · `EverOS` · `minimax-cli` · `vanilla-rag-memory`

---

## 1. 定义模板（schema）

每条定义固定填以下字段，缺项写 `—`，不省略：

- **定义**：它是什么（1–3 句，说清"是什么"而非"举例"）
- **回答**：它回答的那**一个问题**（一句话，这是区分近义文档最有效的判据）
- **坐标**：`读者 / 时态 / 层级 / 契约对象 / 形态`（枚举见下）
- **位置**：典型落点（根 / `docs\` / 子目录 / 目录型）
- **边界**：与最易混邻居如何区分（对比句）
- **实测**：样本实例路径，或"零命中"
- **状态**：`●` / `◐` / `○`

**坐标枚举**（⚠ 取自 `drafts\总览.md` 草案，**属待验证假设**，非既定框架——分类法改造见 `02docsclassify\ds.md`）

- 读者：`AI Agent` / `新用户` / `外部贡献者` / `维护者` / `未来自己` / `法务合规`
- 时态：`事前`(选项·计划) / `事中`(过程·流水) / `事后`(结果·快照·记录) / `永恒`(原则·契约)
- 层级：`公理层`(宪法级原则) / `架构层`(跨模块决策) / `模块层`(单模块设计) / `操作层`(命令·规范·流程)
- 契约对象：`人`(共识) / `工具`(机器读) / `人+工具`
- 形态：`单文件` / `目录` / `单文件+目录`

---

## 2. 实测命名矩阵（先看现实，再谈定义）

这是本阶段最硬的一块证据：**用户清单里大量"约定俗成"的名字，在真实仓库里并不存在。**

| 名称 | DSH | Raven | TS | 其它样本 | 结论 |
|---|---|---|---|---|---|
| `README` | ✓ | ✓ | ✓(+en/ja/ko) | 全部 11 个 | **强实证** |
| `AGENTS` | ✓ | ✓ | ✓ | codex/mem0/memU/minimax/MemOS | **强实证** |
| `CLAUDE` | ✓ | ✓ | ✓ | MemOS/EverOS | **强实证** |
| `CHANGELOG` | 无根级 | ✓ | ✓ | EverOS/codex/memU | 实证 |
| `CONTRIBUTING` | ✓ | ✓ | ✓ | 多家 | **强实证** |
| `SECURITY` | ✓ | ✓ | ✓ | mem0/codex/EverOS | **强实证** |
| `LICENSE` | ✓ | ✓ | ✓ | 多家 | **强实证** |
| `CONTEXT` | 无 | ✓(2646) | 无 | — | 实证（单家） |
| `CONTEXT-MAP` | 无 | ✓(24) | 无 | — | 实证（唯一） |
| `star.md` | 无 | 无 | ✓(915) | — | 实证（唯一） |
| `INDEX` | **明令禁止** | 用 docs\README 代 | ✓ docs\INDEX.md | — | **实证但路线分裂** |
| `MINDMAP` | 无 | 无 | ✓ | — | 实证（唯一） |
| `docs\decisions\` | 无 | 无 | ✓ | — | 实证（唯一） |
| `docs\known-issues\` | 无 | 无 | ✓ | — | 实证（唯一） |
| `docs\plans\` | 无 | ✓ | ✓ | — | 实证 |
| `docs\specs\` | 无 | ✓ | 无 | — | 实证（单家） |
| `.agents\notes\` | ✓(2206) | 无 | 无 | — | 实证（唯一） |
| `docs\glossary` | ✓ | 用 CONTEXT 代 | 无 | — | 实证（单家） |
| `SAFETY` | ✓ | 用 SECURITY 代 | 无 | — | 实证（唯一） |
| `BENCHMARK` | ✓ | 无 | 无 | — | 实证（唯一） |
| `BRAND_GUIDELINES` | ✓ | 无 | 无 | — | 实证（唯一） |
| `SKILL.md` | ✓(skills\) | ✓(skills\) | ✓(skills\) | memU(根级) | 实证 |
| `THESIS` | — | — | — | — | **零命中**（TS 用 star.md） ○ |
| `TRADEOFFS` | — | — | — | — | **零命中** ○ |
| `DECISIONS`(文件) | — | — | — | — | **零命中**（TS 用 decisions\ 目录） ○ |
| `ADR` | — | — | — | — | **零命中** ○ |
| `EXPERIMENTS` | — | — | — | — | **零命中** ○ |
| `PROBLEMS` | — | — | — | — | **零命中**（TS 用 known-issues\） ○ |
| `ROADMAP` | — | — | — | — | **零命中** ○ |
| `THISIS` | — | — | — | — | **零命中** ○ |
| `BRIEF`(根级) | — | — | — | — | **零命中** ○ |
| `TREE`(根级) | — | — | — | — | **零命中**（TS 用 MINDMAP/codebase-index） ○ |
| `CONVENTIONS` | — | — | — | — | **零命中**（并入 AGENTS） ○ |
| `STYLE` | — | — | — | — | **零命中** ○ |
| `LIMITATIONS`(根级) | — | — | — | — | **零命中**（DSH 有 README 内 gate） ○ |
| `registry`(根级) | — | — | — | — | **零命中**（仅 DSH docs\cordis-api\ 内 API 名） ○ |
| `outline`(根级) | — | — | — | — | **零命中** ○ |
| `dialogue\` | — | — | — | — | **零命中** ○ |

**读法**：上半区是"活的命名"（有人真的这么用），下半区是"纸面命名"（草案里想到、现实没人这么命名）。这个分界本身就是研究结论的一部分。

---

## 3. 定义正文

### 3.1 门面与对外文档

#### D01 `README.md` — 项目门面
- **定义**：仓库的第一入口，对外介绍项目"是什么、能干什么、怎么跑起来"。
- **回答**：这个项目是什么，我怎么开始用？
- **坐标**：读者=新用户+外部贡献者 · 时态=现状 · 层级=操作层 · 契约=人 · 形态=单文件(+语言变体)
- **位置**：根
- **边界**：README 教"怎么用"；`AGENTS` 教"怎么改"；`CONTEXT` 讲"词是什么意思"。
- **实测**：全部 11 个样本根级均有。语言变体：TS `README.en.md`/`.ja.md`/`.ko.md`、DSH `README.zh.md`、Raven `README.zh-CN.md`、MemOS `README_ZH.md`、MemOS/MemoryBear `README_CN.md`。
- **状态**：`●`（变体的后缀命名不统一——留给 04 对比）

#### D02 `CHANGELOG.md` — 版本变更记录
- **定义**：面向使用者的、按版本组织的变更流水（Keep a Changelog 惯例）。
- **回答**：这个版本对外可感知地改了什么？
- **坐标**：读者=新用户+维护者 · 时态=事后 · 层级=操作层 · 契约=人 · 形态=单文件（+目录变体）
- **位置**：根
- **边界**：CHANGELOG 记"对外变化"；`decisions\`/notes 记"内部为什么这么选"。
- **实测**：Raven(1015 行)、TS、EverOS、codex、memU。**DSH 根级无 CHANGELOG**，改写 `docs\persistence-changes\releases\`（按版本判持久化格式兼容）。TS 另有 `docs\changelog\`（41 篇日期文件，是"CHANGELOG 目录化"实例）。
- **状态**：`●`

#### D03 `CONTRIBUTING.md` / `CODE_OF_CONDUCT.md` — 协作规则
- **定义**：前者规定"外部贡献者怎么提 PR/遵守什么流程"；后者规定社区行为准则。
- **回答**：（CONTRIBUTING）我怎么贡献？／（COC）在这里如何待人？
- **坐标**：读者=外部贡献者 · 时态=永恒（规则） · 层级=操作层 · 契约=人 · 形态=单文件
- **位置**：根
- **边界**：CONTRIBUTING 面向"仓库外的人"；`AGENTS` 面向"仓库内的 AI Agent"。
- **实测**：CONTRIBUTING — DSH/Raven/TS/EverOS/MemOS/MemoryBear/mem0/memU/minimax/codex 均有；CODE_OF_CONDUCT — Raven/TS/EverOS/mem0。
- **状态**：`●`

#### D04 `SECURITY.md` — 安全策略
- **定义**：漏洞上报渠道与安全承诺（旧时代 GitHub 标配，AI 时代扩展为"工具调用沙箱/越权风险"说明）。
- **回答**：发现安全问题我该怎么报、项目承诺什么？
- **坐标**：读者=外部贡献者+法务合规 · 时态=永恒 · 层级=操作层 · 契约=人 · 形态=单文件
- **位置**：根
- **边界**：SECURITY 面向"外部报告漏洞"；DSH 的 `SAFETY.md` 面向"Agent 运行安全边界"——**两者不同**（见 D25）。
- **实测**：DSH/Raven/TS/codex/mem0/EverOS 均有。
- **状态**：`●`

#### D05 `RELEASING.md` / `QUICKSTART.md` / `INSTALL-LATEST.md` — 流程与上手
- **定义**：RELEASING＝维护者发版步骤；QUICKSTART＝最短上手路径；INSTALL-LATEST＝安装最新版的专门指引。
- **回答**：怎么发一个版本？／怎么最快跑起来？
- **坐标**：读者=维护者(RELEASING)/新用户(QUICKSTART,INSTALL) · 时态=现状 · 层级=操作层 · 契约=人 · 形态=单文件
- **位置**：根（QUICKSTART 可进 `docs\`）
- **边界**：QUICKSTART 是 README 的"只保留最短路径"切片，不重复完整 README。
- **实测**：Raven `RELEASING.md`(94 行)；EverOS `QUICKSTART.md`；memU `INSTALL-LATEST.md`。
- **状态**：`●`（各为单样本）

#### D06 `LICENSE` / `NOTICES.md` / `THIRD_PARTY_NOTICES.md` / `CITATION.md` / `ACKNOWLEDGMENTS.md` / `CONTRIBUTORS.md` — 法务与致谢
- **定义**：许可协议、第三方依赖声明、引用方式、致谢名单、贡献者名单。
- **回答**：我能怎么用这份代码？用了谁的代码？该引谁？
- **坐标**：读者=法务合规+外部贡献者 · 时态=事后（记录） · 层级=操作层 · 契约=人 · 形态=单文件
- **位置**：根
- **边界**：NOTICES（本仓声明）vs THIRD_PARTY_NOTICES（他人版权）；CONTRIBUTORS（人）vs ACKNOWLEDGMENTS（致谢）。
- **实测**：DSH `THIRD_PARTY_NOTICES.md`；Raven `NOTICES.md` + `LICENSES\README.md`；EverOS `CITATION.md`+`ACKNOWLEDGMENTS.md`；TS `CONTRIBUTORS.md`。
- **状态**：`●`

#### D07 `BRIEF.md` — 电梯演讲
- **定义**：半页以内讲清"项目到底解决什么问题、核心定位"，不写安装步骤。
- **回答**：一句话，这项目是干什么的？
- **坐标**：读者=维护者+快速外部预览 · 时态=永恒（定位） · 层级=公理层偏架构层 · 契约=人 · 形态=单文件
- **位置**：根（或内部 wiki 首页）
- **边界**：BRIEF 极短且不教怎么跑；README 长且以"跑起来"为目标。草案提醒：很多项目把 BRIEF 复制进 README 头部后 BRIEF 就废弃了。
- **实测**：**零命中**（`Raven\plugins-dist\design-engine\...\design-brief.md` 是设计产物，不是项目 BRIEF）。
- **状态**：`○` 仅草案

#### D08 `THISIS.md` — 项目自我介绍
- **定义**：草案提出的"介绍本项目"的短文档，与 README/BRIEF 同族。
- **回答**：这个仓库是什么？
- **坐标**：读者=新用户 · 时态=现状 · 层级=操作层 · 契约=人 · 形态=单文件
- **边界**：与 BRIEF/README 高度重叠，草案自身也没给出清晰分工——**建议合并，不单列**。
- **实测**：**零命中**。
- **状态**：`○` 仅草案（且与 D01/D07 重叠，标为"疑似冗余"）

---

### 3.2 Agent 指令

#### D09 `AGENTS.md` — Agent 操作守则（最高频的 AI 时代文档）
- **定义**：写给 AI Agent 的硬约束与执行契约——"作为执行者必须怎么做、如何自检、绝不能碰什么"。
- **回答**：作为 Agent，在这个仓库里我必须遵守什么？
- **坐标**：读者=AI Agent（首要）+维护者 · 时态=永恒（约束） · 层级=操作层 · 契约=人+工具 · 形态=单文件（**可分级**）
- **位置**：根；可分级到 `docs\AGENTS.md`、`packages\AGENTS.md`（DSH 明确限定各级字数）
- **边界**：**不解释"系统是什么"**（→ARCHITECTURE/CONTEXT），只规定"怎么执行"。Raven `AGENTS.md:7` 原文："Hard constraints only … 软建议与风格偏好属于个人笔记或对话，不属于这里。"
- **实测**：DSH `AGENTS.md`(179 行) · Raven `AGENTS.md`(413 行，§N.M 编号) · TS `AGENTS.md` · codex/mem0/memU/minimax-cli/MemOS 均有。
- **状态**：`●`

#### D10 `CLAUDE.md` — harness 别名（指针文件）
- **定义**：Claude 系工具只读这个文件名，因此它是 `AGENTS.md` 的**开关**。最佳实现是**指针**（内容指向 AGENTS.md），避免同一规范维护两份。
- **回答**：Claude 系 harness 该读哪份规范？
- **坐标**：读者=特定 AI harness · 时态=永恒 · 层级=操作层 · 契约=工具 · 形态=单文件（极短）
- **位置**：根
- **边界**：与 AGENTS.md **同源**；分歧时 AGENTS.md 是正本。同族：`GEMINI.md`、`.cursorrules`。
- **实测**：DSH `CLAUDE.md` = **9 字节**，内容 `AGENTS.md`（`file` 报 `ASCII text, with no line terminators`）；Raven `CLAUDE.md` = 一行 `./AGENTS.md`；TS、MemOS、EverOS 均有。
- **状态**：`●`（两种指针写法：裸名 vs `./` 前缀——留给 04 对比）

#### D11 `AGENTS.local.md` — 本机临时变体
- **定义**：开发者本机的临时笔记/实验 agent 定义，**不进版本库**（写进 `.gitignore`）。
- **回答**：我这台机器上临时要遵守/试验什么？
- **坐标**：读者=单个开发者 · 时态=事中 · 层级=操作层 · 契约=人 · 形态=单文件
- **位置**：根（但被忽略）
- **边界**：靠 `.local` 后缀区分"不入库"。
- **实测**：**零命中**。
- **状态**：`○` 仅草案（惯例描述见 `具体md文件的初步分析.md`）

#### D12 `SKILL.md` — 可加载的工作流
- **定义**：skill 的入口文件，定义一段可被 Agent 按需加载的完整工作流（含 references/templates）。
- **回答**：这件事的标准做法是什么？
- **坐标**：读者=AI Agent · 时态=永恒 · 层级=操作层 · 契约=人+工具 · 形态=单文件（+ 同目录 `references\`、`templates\`）
- **位置**：`skills\<name>\SKILL.md`（也可在包内）；memU 直接放根级
- **边界**：SKILL 是"可按需加载的流程"；AGENTS 是"常驻的约束"。
- **实测**：DSH `.agents\skills\dsh-doc\SKILL.md`（含 `templates\`+`references\`）· Raven `plugins-dist\...\skills\...`· TS `docs\skills\`· memU 根级 `SKILL.md`。
- **状态**：`●`

---

### 3.3 架构与认知

#### D13 `ARCHITECTURE.md` — 系统结构说明
- **定义**：描述"系统长什么样"——模块划分、数据流、组件关系，不含决策过程。
- **回答**：系统由哪些部分构成、它们如何协作？
- **坐标**：读者=维护者+AI Agent · 时态=现状 · 层级=架构层 · 契约=人+工具 · 形态=单文件
- **位置**：`docs\`（DSH `docs\architecture.md`、TS `docs\architecture-overview.md`）
- **边界**：ARCHITECTURE 说"是什么"；`star.md`/THESIS 说"为什么"；`decisions\` 说"当时怎么选的"。
- **实测**：DSH `docs\architecture.md` · TS `docs\architecture-overview.md` + `architecture-subagent.md`。**Raven 无独立 ARCHITECTURE**（靠 `CONTEXT.md` + `specs\`）。
- **状态**：`●`

#### D14 `CONTEXT.md` — 领域语言正典
- **定义**：本项目每个术语的权威定义 + 反例（`_Avoid_:`），让 Agent 与人在同一套词汇上对齐。
- **回答**：这个词在本项目里确切是什么意思？
- **坐标**：读者=AI Agent+维护者 · 时态=永恒（术语） · 层级=架构层 · 契约=人+工具 · 形态=单文件（**每个上下文一份**）
- **位置**：根 或 各模块目录（Raven `CONTEXT.md` + `ui-tui\CONTEXT.md`）
- **边界**：与 `GLOSSARY` **同义**（D15）；与 ARCHITECTURE 区别——CONTEXT 管"词义"，ARCHITECTURE 管"结构"。
- **实测**：Raven `CONTEXT.md`(2646 行，`_Avoid_` 反例逐条) + `ui-tui\CONTEXT.md` + `agents\README.md`。
- **状态**：`●`（单家）

#### D15 `GLOSSARY.md` — 术语表（= D14 的别名）
- **定义**：与 CONTEXT 同角色的命名——"名词 → 定义"的清单。
- **回答**：这个词是什么意思？
- **坐标**：同 D14
- **边界**：若项目同时有 CONTEXT 与 GLOSSARY，需明确分工（通常是 CONTEXT 含反例/上下文，GLOSSARY 纯名词表）——**样本中无同时出现的案例**。
- **实测**：DSH `docs\glossary.md`（+`.zh.md`）。
- **状态**：`●`（单家）；与 D14 是**同一角色的两个名字**

#### D16 `CONTEXT-MAP.md` — 多上下文地图
- **定义**：列出仓库由哪几个"上下文"构成、各自术语表在哪、彼此如何通信、架构术语去哪个文件查。
- **回答**：这个仓库有哪几个上下文？术语分散在哪里？
- **坐标**：读者=AI Agent+维护者 · 时态=永恒 · 层级=架构层 · 契约=人+工具 · 形态=单文件（短）
- **位置**：根
- **边界**：MAP 是**路由**（去哪查），CONTEXT 是**内容**。
- **实测**：Raven `CONTEXT-MAP.md`(24 行，列 3 个 context + Relationships + Architecture terms routing)。
- **状态**：`●`（唯一实例）——**最有研究价值的命名**：它把 DDD 的 bounded-context 落成了 Markdown

#### D17 `star.md` — 项目立论/思想文档
- **定义**：写底层公理、设计立场、哲学主张。承担业界常说的 THESIS/ manifesto 角色，但用项目自造命名。
- **回答**：我们为什么这样构建？我们信奉什么？
- **坐标**：读者=维护者+未来自己 · 时态=永恒（原则） · 层级=公理层 · 契约=人 · 形态=单文件
- **位置**：根
- **边界**：比 ARCHITECTURE 更"为什么"；比 README 更"内部"。
- **实测**：TS `star.md`(915 行，含"星域公理"四条 + 伙伴星印记)。
- **状态**：`●`（唯一实例）；**是草案中 `THESIS.md` 的现实对应物**

#### D18 `THESIS.md` — 项目立论（草案命名）
- **定义**：草案提出的思想文档——底层假设、哲学立场、要证明的命题。
- **回答**：这套架构为什么可行？
- **坐标**：读者=维护者 · 时态=永恒 · 层级=公理层 · 契约=人 · 形态=单文件
- **边界**：与 ARCHITECTURE 的区别（草案原文）：THESIS 是 **why**（立场/假设），ARCHITECTURE 是 **what/how**（模块/数据流）。
- **实测**：**零命中**（TS 用 `star.md`，见 D17）。
- **状态**：`○` 仅草案——**存在现实对应物，但现实没用这个名字**

#### D19 `INDEX.md` — 文档索引
- **定义**：文档的总目录/导航入口。
- **回答**：文档都在哪？
- **坐标**：读者=AI Agent+维护者 · 时态=现状 · 层级=操作层 · 契约=人+工具 · 形态=单文件
- **位置**：根 或 `docs\`
- **边界**：INDEX 只导航；README 还讲怎么用；目录树是自动的、INDEX 是语义化的。
- **实测**：TS `docs\INDEX.md`；Raven 用 `docs\README.md` 充当；**DSH 明令禁止**——`.agents\notes\README.md` 原文："Do not add a centralized `INDEX.md`"，并由一条独立 Agent Note 承载理由。
- **状态**：`●` **路线分裂**（做 / 不做 / 变形）——正是 `03docscompare` 的核心议题

#### D20 `MINDMAP.md` / `TREE` / `codebase-index` — 结构可视化
- **定义**：用树/脑图/索引表达项目结构或文件布局。
- **回答**：项目的整体形状是什么样？
- **坐标**：读者=AI Agent+维护者 · 时态=现状 · 层级=架构层 · 契约=人+工具 · 形态=单文件
- **边界**：与 INDEX 区别——MINDMAP/TREE 表达**结构关系**，INDEX 表达**清单导航**。
- **实测**：TS `docs\MINDMAP.md`、`docs\codebase-index.md`。草案的 `TREE.md` 零命中。
- **状态**：`●`（TS 实证）；`TREE.md` 本身 `○`

#### D21 `registry` / `outline` — 登记表与大纲
- **定义**：草案提出的"登记表"（如组件/能力注册清单）与"大纲"（文档/内容结构）。
- **回答**：有哪些已登记项？内容的大纲是什么？
- **坐标**：读者=维护者 · 时态=现状/事前 · 层级=模块层 · 契约=工具偏多 · 形态=单文件
- **边界**：registry 偏"机器可读的清单"（草案设想用 csv/json 更好，因为频繁 add）——见研究纲领"各种文档格式该如何选择"。
- **实测**：**零命中**（DSH `docs\cordis-api\registry.md` 是 API 方法名，不是此角色）。
- **状态**：`○` 仅草案

---

### 3.4 决策与记录

> 这一簇是"研究纲领"里争议最大的部分：**记录型的文档该用文件还是目录、该用什么时态**。

#### D22 `DECISIONS.md` / `decisions\` / `ADR` — 架构决策记录
- **定义**：一条条正式的设计决策记录（ADR：Architecture Decision Record），记"当时选了什么、为什么、放弃了什么"。
- **回答**：这个设计为什么是现在这样？
- **坐标**：读者=维护者+未来自己 · 时态=事后 · 层级=架构层 · 契约=人 · 形态=**单文件**(小项目) 或 **目录**(大项目)
- **位置**：根 `DECISIONS.md` 或 `docs\decisions\` / `adr\`
- **边界**：**ADR ≠ TRADEOFFS**（草案原文）：TRADEOFFS 偏"权衡清单"，ADR 是"一条条正式决策记录"，常用 `adr\0001-xxx.md` 编号。
- **实测**：TS `docs\decisions\`（目录型 ✓）。**根级 `DECISIONS.md` 零命中，`ADR` 零命中。**
- **状态**：`●`（目录型，TS 唯一）；文件型 `○`

#### D23 `TRADEOFFS.md` — 权衡取舍记录
- **定义**：记录每个重要决策的利弊，**把放弃的方案也写下来**。
- **回答**：当初为什么没选另一个方案？
- **坐标**：读者=维护者+未来自己 · 时态=事后 · 层级=架构层 · 契约=人 · 形态=单文件
- **边界**：与 D22 区别见上；与 EXPERIMENTS 区别——TRADEOFFS 是决策时的利弊，EXPERIMENTS 是原型实验结果。
- **实测**：**零命中**。
- **状态**：`○` 仅草案（草案称"普通业务项目很少维护，但 Agent 框架强烈建议"——属**待验证假设**）

#### D24 `EXPERIMENTS.md` — 实验记录
- **定义**：开发中做过的废弃实验、试过的方向、实验结论。
- **回答**：我们试过什么、结果如何？
- **坐标**：读者=维护者 · 时态=事后 · 层级=模块层 · 契约=人 · 形态=单文件
- **边界**：与 TRADEOFFS 重叠，更偏原型结果。
- **实测**：**零命中**。
- **状态**：`○` 仅草案

#### D25 `PROBLEMS.md` / `known-issues\` — 已知问题/技术债
- **定义**：当前架构的已知缺陷、待解决痛点、技术债。
- **回答**：现在哪里有坑？
- **坐标**：读者=维护者 · 时态=现状（未解决） · 层级=架构层偏模块层 · 契约=人 · 形态=单文件 或 目录
- **边界**：与 GitHub Issues 区别——这里放**高层**结构性问题，不放在 issue 里。
- **实测**：TS `docs\known-issues\`（目录型 ✓，含 `win-orphan-descendants-repro` 子目录）。**根级 `PROBLEMS.md` 零命中。**
- **状态**：`●`（目录型，TS 唯一）；文件型 `○`

#### D26 `ROADMAP.md` — 路线图
- **定义**：短期/中期/长期的版本与能力规划。
- **回答**：接下来要做什么？
- **坐标**：读者=维护者+新用户 · 时态=**事前** · 层级=架构层 · 契约=人 · 形态=单文件
- **边界**：ROADMAP 是"未来"；CHANGELOG 是"过去"；PROBLEMS 是"现在"。
- **实测**：**零命中**。
- **状态**：`○` 仅草案（研究纲领自己也在问："ROADMAP、PROBLEMS 这种未来的该怎么管理呢"）

#### D27 `LIMITATIONS.md` — 项目局限
- **定义**：明写框架固有的局限、哪些问题**不打算**解决，避免使用者产生不切实际的预期。
- **回答**：这东西做不到什么？
- **坐标**：读者=新用户+外部贡献者 · 时态=永恒偏现状 · 层级=架构层 · 契约=人 · 形态=单文件
- **边界**：PROBLEMS＝"缺陷待修"；LIMITATIONS＝"设计上不做"。二者语义相反，**不可合并**。
- **实测**：**根级零命中**。DSH 把"Known Limitations"做成了**包 README 的必需章节 + 门禁**（`.agents\notes\archived\process\2026-07-10-readme-known-limitations-gate.md`）。
- **状态**：`○`（文件型）；其**内容**在 DSH 以章节形式 `●` 实证

#### D28 `plans\` — 实现计划（目录）
- **定义**：带日期的实现计划——"怎么做"的任务分解（文件清单、约束、可勾选步骤）。
- **回答**：当时打算怎么实现它？
- **坐标**：读者=维护者+AI Agent · 时态=**事前**（事后转为历史存档） · 层级=模块层 · 契约=人+工具 · 形态=**目录**
- **位置**：`docs\plans\`
- **边界**：plan 是"过程"（可废弃）；spec 是"结论"（as-built）。
- **实测**：Raven `docs\plans\`(28 篇，`YYYY-MM-DD-slug.md`，顶部 `Superseded` 横幅 + `For agentic workers` 子技能指令 + 逐条引用 `AGENTS.md section N`）· TS `docs\plans\`。
- **状态**：`●`

#### D29 `specs\` — 设计规格（目录）
- **定义**：带日期的设计记录/契约——"是什么"，描述"截至其日期的系统"。
- **回答**：它被设计成了什么样？
- **坐标**：读者=维护者 · 时态=事后（as-built） · 层级=模块层 · 契约=人 · 形态=**目录**
- **位置**：`docs\specs\`
- **边界**：与 plan 互链（plan 顶部链接对应 spec）；`Status:` 字段标明实现状态。
- **实测**：Raven `docs\specs\`(54 篇，`YYYY-MM-DD-slug-design.md`，头部 `Date:` + `Status: implemented`）。
- **状态**：`●`（单家）

#### D30 `notes\` — 决策/提案笔记（目录，状态机）
- **定义**：以**生命周期状态**组织的一类设计文档——提案→落地→否决→归档。
- **回答**：这条决策处于什么状态、为什么？
- **坐标**：读者=维护者+AI Agent · 时态=跨事前/事后 · 层级=架构层 · 契约=人 · 形态=**目录**（路径编码状态）
- **位置**：`.agents\notes\{lifecycle}\{class}\`
- **边界**：与 plans/specs 区别——notes 用**目录表达状态**（proposed/implemented/rejected/archived），plans/specs 用**头部字段 + 横幅**表达。
- **实测**：DSH `.agents\notes\`(2206 篇)——`{lifecycle}/{class}/yyyy-mm-dd-topic.md`，强制头部三行 `# Agent Note: <title>` / 空行 / `Status: <status>`，`archived\` 冻结不可变。
- **状态**：`●`（单家，但设计最完备）

#### D31 `changelog\` — 变更记录（目录化）
- **定义**：把"变更记录"从单文件展开成目录，每条变更一个日期文件。
- **回答**：某次具体变更是什么？
- **坐标**：读者=维护者 · 时态=事后 · 层级=模块层 · 契约=人 · 形态=**目录**
- **边界**：根级 `CHANGELOG.md` 面向使用者、聚合；`changelog\` 面向维护者、细粒度。
- **实测**：TS `docs\changelog\`(41 篇，`YYYY-MM-DD-slug.md`，中英混合命名）。
- **状态**：`●`（唯一实例）

#### D32 `postmortem\` — 事故复盘
- **定义**：故障后的复盘记录，沉淀根因与教训。
- **回答**：这次事故的根因是什么、如何避免？
- **坐标**：读者=维护者 · 时态=事后 · 层级=模块层 · 契约=人 · 形态=目录
- **实测**：DSH `docs\postmortem\` ✓（目录存在）。单一 `POSTMORTEM.md` 零命中。
- **状态**：`●`（目录型，DSH 实证）

---

### 3.5 规范与约束

#### D33 `CONVENTIONS.md` — 开发规约
- **定义**：代码风格、命名、prompt 管理、日志规范等"本项目内部开发手册"。
- **回答**：写代码时我要遵守哪些约定？
- **坐标**：读者=维护者+AI Agent · 时态=永恒 · 层级=操作层 · 契约=人+工具 · 形态=单文件
- **边界**：与 AGENTS 高度重叠——**样本中此项几乎全被 `AGENTS.md` 吸收**。
- **实测**：**零命中**（Raven 的代码注释/命名/提交规范全在 `AGENTS.md` 的 §1–§7；DSH 在 `AGENTS.md` + `docs\AGENTS.md`）。
- **状态**：`○` 仅草案——**现实中被 AGENTS.md 取代**

#### D34 `STYLE.md` — 风格指南
- **定义**：写作/代码风格细则。
- **回答**：风格上该怎么写？
- **坐标**：读者=维护者 · 时态=永恒 · 层级=语法层 · 契约=人+工具 · 形态=单文件
- **边界**：多数样本把它交给 linter 配置（`.prettierrc`/`.oxlintrc.json`/`ruff.toml`），而非 md。
- **实测**：**零命中**（无通用 `STYLE.md`）。相近但非同类：DSH `docs\i18n\style-samples.md`（翻译风格样例）、codex `codex-rs\tui\styles.md`（TUI 样式技术文档）。
- **状态**：`○` 仅草案

#### D35 `SAFETY.md` — Agent 运行安全
- **定义**：面向 Agent 的运行安全边界（沙箱、权限、越权风险）。
- **回答**：Agent 运行时哪些红线不能碰？
- **坐标**：读者=AI Agent+维护者 · 时态=永恒 · 层级=操作层 · 契约=人+工具 · 形态=单文件
- **边界**：**与 SECURITY.md 不同**——SECURITY 是"漏洞上报政策"，SAFETY 是"Agent 行为安全边界"。
- **实测**：DSH `SAFETY.md` + `SAFETY.zh.md`。
- **状态**：`●`（唯一实例）

#### D36 `BRAND_GUIDELINES.md` / `BENCHMARK.md` / `ERRORS.md` / `SDK.md` / `LLM.md` — 主题专章
- **定义**：项目自定的单一主题手册——品牌规范 / 基准测试 / 错误码 / SDK 用法 / LLM 集成。
- **回答**：关于 <主题> 的规范是什么？
- **坐标**：读者=使用者+维护者 · 时态=现状 · 层级=模块层 · 契约=人 · 形态=单文件
- **边界**：命名是**项目自造**，不是通用惯例——正因如此，LLM 无法从名字推断内容，必须在别处显式介绍。
- **实测**：DSH `BRAND_GUIDELINES.md`+`.zh.md`、`BENCHMARK.md`；minimax-cli `ERRORS.md`、`SDK.md`；mem0 `LLM.md`。
- **状态**：`●`（各为单样本）——**命名研究的富矿**

---

### 3.6 主体与机制

#### D37 `MEMORY.md` — 项目记忆
- **定义**：项目层面的"记忆"——跨会话需要保留的信息（含 Agent 记忆机制说明或记忆内容）。
- **回答**：关于这个项目，需要长期记住什么？
- **坐标**：读者=AI Agent+维护者 · 时态=跨时态 · 层级=架构层 · 契约=人+工具 · 形态=单文件
- **边界**：与 `USER.md` 相对——MEMORY 是"项目事实"，USER 是"用户模型"。本仓库（memory 研究）的 `.workbuddy\memory\MEMORY.md` 即此角色实例。
- **实测**：样本 repo 内**零命中**；本工作区 `.workbuddy\memory\MEMORY.md` 存在（同类实例）。
- **状态**：`◐` 业界常见（样本未见）

#### D38 `USER.md` — 用户模型
- **定义**：站在用户视角的模型——用户偏好、状态、权限、约束，以及 Agent 如何感知用户。
- **回答**：我们服务的用户是什么样的？
- **坐标**：读者=AI Agent · 时态=现状 · 层级=架构层 · 契约=人+工具 · 形态=单文件
- **实测**：样本 repo 内**零命中**（Raven 据其 `CONTEXT.md` 描述，用户信息存于 `user_memory\profile\user.md`，属运行时产物、非仓库文档）。
- **状态**：`○`/`◐` 草案提出、样本未见

#### D39 `dialogue\` — 对话记录
- **定义**：保存与 AI 的对话/协作记录。
- **回答**：当时是怎么讨论出这个决定的？
- **坐标**：读者=维护者 · 时态=事中 · 层级=— · 契约=人 · 形态=目录
- **实测**：**零命中**。近似物：本研究的 `02docsclassify\`、`03docscompare\` 目录（按 AI 命名，如 `glm.md`）。
- **状态**：`○` 仅草案

---

### 3.7 过程与教程

#### D40 `cookbook\` / `guides\` / `tutorial\` — 教程（目录）
- **定义**：按任务组织的操作教程（如"如何新增一个 tool"）。
- **回答**：怎么做这件具体的事？
- **坐标**：读者=新用户+外部贡献者 · 时态=现状 · 层级=操作层 · 契约=人 · 形态=**目录**
- **边界**：tutorial 是**循序渐进**（按前置依赖排序），cookbook 是**按任务查阅**（可跳读）。
- **实测**：DSH `docs\cookbook\`（adding-a-tool / adding-an-llm-adapter …）、`docs\cordis-tutorial\`（编号 01–07）；TS `docs\guides\`。
- **状态**：`●`

#### D41 `dev.md` / `development.md` / `reference\` — 开发者参考
- **定义**：本地开发环境搭建与命令速查；`reference\` 放精确 API/字段参考。
- **回答**：怎么把开发环境跑起来？这个接口的确切签名是什么？
- **坐标**：读者=外部贡献者+维护者 · 时态=现状 · 层级=操作层 · 契约=人+工具 · 形态=单文件/目录
- **实测**：Raven `docs\dev.md`；DSH `docs\development.md`；TS `docs\dev\`、`docs\reference\`。
- **状态**：`●`

#### D42 `_templates\` — 文档模板（目录）
- **定义**：存放各类文档的骨架模板，供新建时复制。
- **回答**：这类文档该长什么样？
- **坐标**：读者=维护者 · 时态=永恒 · 层级=操作层 · 契约=工具 · 形态=**目录**
- **边界**：模板让"格式"可机械复制，是文档治理从"靠人记"转向"靠结构"的标志。
- **实测**：TS `docs\_templates\` ✓；DSH `.agents\skills\dsh-doc\templates\`（7 个 kind 模板）。
- **状态**：`●`

---

## 4. 一页总表

| ID | 名称 | 回答的问题 | 读者 | 时态 | 层级 | 形态 | 状态 |
|---|---|---|---|---|---|---|---|
| D01 | `README.md` | 这是什么、怎么开始用 | 新用户 | 现状 | 操作层 | 单文件 | `●` |
| D02 | `CHANGELOG.md` | 这版改了什么 | 新用户 | 事后 | 操作层 | 单文件(+目录) | `●` |
| D03 | `CONTRIBUTING.md`/`CODE_OF_CONDUCT.md` | 我怎么贡献/如何待人 | 外部贡献者 | 永恒 | 操作层 | 单文件 | `●` |
| D04 | `SECURITY.md` | 漏洞怎么报 | 外部贡献者 | 永恒 | 操作层 | 单文件 | `●` |
| D05 | `RELEASING`/`QUICKSTART`/`INSTALL-LATEST` | 怎么发版/最快上手 | 维护者/新用户 | 现状 | 操作层 | 单文件 | `●` |
| D06 | `LICENSE`/`NOTICES`/`CITATION`/`ACKNOWLEDGMENTS`/`CONTRIBUTORS` | 能怎么用/引谁/谢谁 | 法务合规 | 事后 | 操作层 | 单文件 | `●` |
| D07 | `BRIEF.md` | 一句话这是什么 | 维护者 | 永恒 | 公理层 | 单文件 | `○` |
| D08 | `THISIS.md` | 这个仓库是什么 | 新用户 | 现状 | 操作层 | 单文件 | `○` |
| D09 | `AGENTS.md` | Agent 必须遵守什么 | **AI Agent** | 永恒 | 操作层 | 单文件(可分级) | `●` |
| D10 | `CLAUDE.md` | Claude 读哪份规范 | AI harness | 永恒 | 操作层 | 单文件(指针) | `●` |
| D11 | `AGENTS.local.md` | 本机临时遵守什么 | 单个开发者 | 事中 | 操作层 | 单文件 | `○` |
| D12 | `SKILL.md` | 这件事的标准做法 | AI Agent | 永恒 | 操作层 | 单文件(+目录) | `●` |
| D13 | `ARCHITECTURE.md` | 系统由什么构成 | 维护者 | 现状 | 架构层 | 单文件 | `●` |
| D14 | `CONTEXT.md` | 这个词什么意思 | AI Agent | 永恒 | 架构层 | 单文件(可多份) | `●` |
| D15 | `GLOSSARY.md` | 这个词什么意思 | AI Agent | 永恒 | 架构层 | 单文件 | `●` |
| D16 | `CONTEXT-MAP.md` | 有哪几个上下文 | AI Agent | 永恒 | 架构层 | 单文件 | `●` |
| D17 | `star.md` | 为什么这样构建 | 维护者 | 永恒 | 公理层 | 单文件 | `●` |
| D18 | `THESIS.md` | 这套架构为何可行 | 维护者 | 永恒 | 公理层 | 单文件 | `○` |
| D19 | `INDEX.md` | 文档都在哪 | AI Agent | 现状 | 操作层 | 单文件 | `●`(分裂) |
| D20 | `MINDMAP`/`TREE`/`codebase-index` | 项目整体形状 | AI Agent | 现状 | 架构层 | 单文件 | `●`/`○` |
| D21 | `registry`/`outline` | 有哪些登记项/大纲 | 维护者 | 现状 | 模块层 | 单文件 | `○` |
| D22 | `DECISIONS`/`decisions\`/`ADR` | 为什么是现在这样 | 未来自己 | 事后 | 架构层 | 单文件/目录 | `●`(目录) |
| D23 | `TRADEOFFS.md` | 为什么没选另一个 | 未来自己 | 事后 | 架构层 | 单文件 | `○` |
| D24 | `EXPERIMENTS.md` | 试过什么、结果如何 | 维护者 | 事后 | 模块层 | 单文件 | `○` |
| D25 | `PROBLEMS`/`known-issues\` | 现在哪里有坑 | 维护者 | 现状 | 架构层 | 单文件/目录 | `●`(目录) |
| D26 | `ROADMAP.md` | 接下来做什么 | 维护者 | 事前 | 架构层 | 单文件 | `○` |
| D27 | `LIMITATIONS.md` | 做不到什么 | 新用户 | 永恒 | 架构层 | 单文件 | `○` |
| D28 | `plans\` | 当时打算怎么做 | 维护者 | 事前 | 模块层 | 目录 | `●` |
| D29 | `specs\` | 被设计成什么样 | 维护者 | 事后 | 模块层 | 目录 | `●` |
| D30 | `notes\` | 决策处于什么状态 | 维护者 | 跨时态 | 架构层 | 目录 | `●` |
| D31 | `changelog\` | 某次变更是什么 | 维护者 | 事后 | 模块层 | 目录 | `●` |
| D32 | `postmortem\` | 事故根因是什么 | 维护者 | 事后 | 模块层 | 目录 | `●` |
| D33 | `CONVENTIONS.md` | 写代码遵守什么 | AI Agent | 永恒 | 操作层 | 单文件 | `○` |
| D34 | `STYLE.md` | 风格怎么写 | 维护者 | 永恒 | 语法层 | 单文件 | `○` |
| D35 | `SAFETY.md` | Agent 哪些红线不能碰 | AI Agent | 永恒 | 操作层 | 单文件 | `●` |
| D36 | `BRAND_GUIDELINES`/`BENCHMARK`/`ERRORS`/`SDK`/`LLM` | <主题>规范是什么 | 使用者 | 现状 | 模块层 | 单文件 | `●` |
| D37 | `MEMORY.md` | 需长期记住什么 | AI Agent | 跨时态 | 架构层 | 单文件 | `◐` |
| D38 | `USER.md` | 用户是什么样的 | AI Agent | 现状 | 架构层 | 单文件 | `○` |
| D39 | `dialogue\` | 当时怎么讨论的 | 维护者 | 事中 | — | 目录 | `○` |
| D40 | `cookbook\`/`guides\`/`tutorial\` | 这件具体事怎么做 | 新用户 | 现状 | 操作层 | 目录 | `●` |
| D41 | `dev.md`/`reference\` | 环境怎么搭/接口签名 | 贡献者 | 现状 | 操作层 | 单文件/目录 | `●` |
| D42 | `_templates\` | 这类文档该长什么样 | 维护者 | 永恒 | 操作层 | 目录 | `●` |

---

## 5. 锁定台账

**已锁定（定义/边界/实测三项无待办）**：D01 · D02 · D04 · D06 · D09 · D10 · D12 · D13 · D14 · D16 · D17 · D19 · D28 · D29 · D30 · D31 · D35 · D40 · D41 · D42

**待论证（状态为 `○`/`◐`，需继续找实例或裁决是否废弃）**：D07 BRIEF · D08 THISIS（疑似与 D01/D07 冗余）· D11 AGENTS.local · D15 GLOSSARY（与 D14 是否应合一）· D18 THESIS · D21 registry/outline · D23 TRADEOFFS · D24 EXPERIMENTS · D26 ROADMAP · D27 LIMITATIONS · D33 CONVENTIONS · D34 STYLE · D37 MEMORY · D38 USER · D39 dialogue

**待裁决的路线分裂**：
- **D19 INDEX**：做（TS）/ 不做（DSH，有专门论证）/ 变形为 docs\README（Raven）——三选一需在 `03docscompare` 定夺。
- **D14 vs D15**：`CONTEXT` 与 `GLOSSARY` 是同一角色的两个名字，还是应各司其职？
- **D33/D34**：`CONVENTIONS`/`STYLE` 是否已被 `AGENTS.md` + linter 配置彻底取代？
- **决策记录形态**：单文件 `DECISIONS.md` 还是目录 `decisions\`？D22/D25 的实证都指向**目录型**。

**下一步（阶段 03/04 的输入）**：
1. 用第 2 节的实测矩阵，把"纸面命名"与"活的命名"分开表述——避免研究被草案里的想象命名带偏。
2. 把 D14/D15、D18/D17、D33/D09 这三组"同角色多名字"交给 `02docsclassify` 做归并。
3. 用第 4 节总表的五个坐标轴，检验分类法是否能**唯一**定位每一个类型。

---

> 证据说明：第 2 节矩阵与各条"实测"字段均来自对 `sources\repos\` 下 11 个仓库的文件实测（`find`/`ls`/`wc -l`/文件字节数），未对运行时行为作断言。"零命中"指在本次 `find` 覆盖范围内未见同名文件——若后续扩大样本或发现遗漏，应更新对应条目并记录变更。
