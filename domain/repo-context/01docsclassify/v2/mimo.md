按你的决定重排研究顺序：**判据（压缩）→ 角度（降级为参考）→ 模型（核心产物）→ 归类（映射总表）**。命名我做了重新设计。先给结论性的第一性原理论证，因为它决定了后面全部形态。

---

# 〇、第一性原理：什么是"文档类型模型"

周期表的类比要再往下挖一层才成立：

> **Mendeleev 先有元素（观测量），后有坐标（解释量）。坐标解释规律、预测空位，但从不取代元素本身。**

对应过来：

| 周期表 | 文档系统 | 性质 |
|---|---|---|
| 元素 | **文档模型（Model）** | 本体，工程上真正被使用的东西 |
| 坐标（周期/族） | 角度/字段 | 解释量，用于归类新文档、预测治理 |
| 化学性质 | **治理契约** | 由位置预测出来的东西 |
| 同位素 / 化合物 | 修饰符 / 模型迁移 | 不为它们加新轴 |

**模型 = 一簇稳定的坐标取值 + 一份随之而来的治理契约。**

你"决定"里的直觉因此是严格正确的：n1×n2×…×nk 矩阵是伪需求，因为**坐标本身不干活，契约才干活**。工程系统里真正要保证的只有一件事——给一个文件，两个人、两次归类，结果一致（inter-rater agreement），且归类结果能直接抄出治理规则。这两条我称为**可重复判定**与**契约可推导**，取代"正交性"这个数学标准。

由此再得一条第一性原理，它解决你最纠结的单列问题：

> **孤例不进坐标轴，孤例进模型。坐标轴是共享的，模型才是容纳"独一份"的地方。**

氢元素不会因为孤独就该被删掉或单开一族；同样，AGENTS.md 在一个仓库里天然唯一，但它是**纲领模型的模式标本（type specimen）**——一个成员的模型完全合法。

---

# 一、交付物：专用子文件夹

不做原地修改。本专题自成一个 `subject: meta` 的研究区，并且**用自己产出的规则治理自己**（front-matter 示范）：

```
docs/research/doc-models/
├── 00-INDEX.md      ← 图谱：意图→文件的语义路由
├── 01-总览.md        ← 唯一对外入口（最终产物）
├── 02-判据.md        ← 过程产物（判据 + 舍弃记录），主文只留索引
├── 03-角度.md        ← 参考：角度/修饰符/热力矩阵
├── 04-模型.md        ← 核心：10 个模型的一夜契约 ★
├── 05-归类.md        ← 核心：文件→模型 映射总表 ★
├── 06-孤例.md        ← 单列判据 + 嵌合体拆分记录
├── 90-挂起.md        ← 开放问题与跨专题依赖
└── evidence/
    └── 2026-xx-xx-模型法讨论.md   ← 本轮对话留痕（append-only）
```

```yaml
# 04-模型.md 的 front-matter（示例，演示 schema 在自己身上可跑通）
---
role: rule            # 这是本研究的"律条"：新文档必须按此归类
order: meta
subject: doc-system
status: accepted      # 经本轮讨论定稿；修订走议定
origin: handwritten
scope: repo
rank: architecture
treat: instruct
author: mixed
reviewed_by: @human
derived_from: [evidence/2026-xx-xx-模型法讨论.md]
---
```

---

# 二、判据（压缩成 5 行，其余进 02）

你担心"定义太多、过程产物在最终结果里多余"——正解是**分离，不是删除**。判据是验收标准，属于 `02-判据.md`（过程记录，供后人知道为什么这样设计），`01-总览.md` 里只留五句话：

1. **可重复判定**：两人两次归类结果一致（取代"正交性"）
2. **契约可推导**：坐标 → 治理规则能直接抄出来
3. **长尾有泄压阀**：不为边缘案例加轴（见下）
4. **模型数 ≤ 10**：新增模型必须附一页完整契约
5. **孤例进模型，不进轴**（见 06）

**工程化的三个泄压阀**（解决"冗余维度 vs 完备性"的取舍）：

| 长尾情况 | 处置 | 例子 |
|---|---|---|
| 值的组合差异 | **修饰符组合**，不加轴 | 生成件 = 任意模型 + `origin: generated` |
| 时间推移改性质 | **模型迁移**（受治理的状态转换） | plans：草稿→时务→史册 |
| 不属于协作语料 | **域外带**（免分类但不免校验） | LICENSE / CODE_OF_CONDUCT |
| 尚无定论 | **挂起表** | 补偿、skills 读取语义 |

**顺手回答你的四个疑问：**

- "为了概念放弃可读性" → 判据 1 要求的是**判定可重复**，不是坐标漂亮。两轴糊在一起时宁可写成"例外注记"，也不硬拆。
- "规则可推导被其他包含" → 同意，并入判据 2，不单列。
- "工程上不一定能完全正交" → **不要求轴间正交，只要求模型间契约不重叠**。修饰符是可组合的（天然不正交也不碍事），分类轴只剩一根（模型），无从不正交。
- "维度太正交且单轴，但我一维有多值、甚至只是描述" → 你说的其实是**三种东西被一个词"维度"压扁了**：分类轴（partition）、修饰符（可组合标签）、描述性说明（不参与判定）。拆开后各归各位，见 03。

---

# 三、角度（03-角度.md）：三类坐标，一根真轴

## 3.1 三类坐标

| 类型 | 判定性质 | 数量 | 作用 |
|---|---|---|---|
| **分类轴** | 单值、排他、穷尽 | **1 根：模型** | 决定治理契约 |
| **修饰符** | 可组合、可多值 | 7 个 | 在契约上增删条款 |
| **说明性角度** | 不参与判定 | 若干 | 供人理解、供 compare 章使用 |

**修饰符清单**（每个只携带少量规则，可自由组合）：

| 修饰符 | 取值 | 携带的规则 |
|---|---|---|
| `origin` | generated / handwritten | 生成件禁手写；CI freshness；锚定 source |
| `status` | draft / accepted / deprecated | 草稿隔离；`treat:instruct ⇒ accepted` |
| `treat` | instruct / refer / object | 能否被当指令执行 |
| `target` | codebase / harness | 记的是项目还是协作者自己 |
| `subject` | object / meta | **"元"的正确归宿**（见 3.3） |
| `scope` | machine / user / repo / module | 覆盖权 + 隐私 + 检索根 |
| `rank` / `stale_risk` | axiom…operation / mislead·omit | 冲突链 / 复审强度 |

**被降级为"说明"的角度**（你的两个自我否定都是对的，且理由相同）：

- **Mutation（不变/只增/持续更新/过程性）** → 不作分类轴，但它是**模型族的分组依据**（见 3.4）。注意这个反转：你把时间和 mutation 都降级了，但两者命运不同——**时间完全预测不了治理（plans 横跨三态），mutation 几乎完全预测治理（冻结 vs 追加 vs 流转）**。所以时间彻底降为说明，mutation 升为模型族的骨架。
- **时间（过去/现在/未来/元）** → 说明性。你的两条质疑都成立：
  - "元跟时间解耦了吗？" **没有，而且它根本不是时间值**。`元` 描述的是**记述对象**（meta=关于文档系统自身），`INDEX` 描述的是**体裁**（导航）。"元·导航"把两个正交的东西焊在一起了，所以才别扭。拆开后：`subject: meta` 是修饰符，INDEX 是普通模型（图谱），本研究自己也是 `subject: meta` 的普通文档，落在草稿→议定→史册的常规流程里，不需要任何特权。
  - "plans 三个态都占" → 因为 **plan 不是一种文档，是一件文档的三个生命阶段**。解法是"模型迁移"（3.5），不是加轴。

## 3.2 载入：你的四值塌缩成两个参数

你发现的"CONVENTIONS 在开发期默认载入、在规划期却是条件载入"是关键证据——**载入不是文档的属性，是（文档 × 工作阶段）的属性**。所以载入不能是一根单值轴，必须是**热力分布**。

四值 → 两参数的映射：

| 你的四值 | 推送策略 push | 阶段热度 |
|---|---|---|
| 默认载入 | always | 某阶段 ★★★ |
| 条件载入 | on-condition | 命中阶段 ★★★ |
| 可选载入 | on-condition（弱） | ★ |
| 仅供参考 | **never-push**（严禁主动预热） | — |

"都能主动载入"= 基线能力，写进系统规格，不占分类值。

## 3.3 元 → `subject: meta`（已并入修饰符表）

## 3.4 模型族 = 按嬗变分组（四族十型）

| 族 | 嬗变 | 模型 |
|---|---|---|
| **改写型** | 重写覆盖，不留史 | 纲领 / 图谱 / 律条 / 形制 / 规程 |
| **裁决型** | 冻结 + 显式 supersede | 议定 |
| **流转型** | 高频流转 + 清账 + **删除是正常结局** | 时务 / 草稿 |
| **追加型** | 只增不改 | 史册 |
| **随行型** | 持续小改 + 自动沉淀 | 自述 |

## 3.5 模型迁移（受治理的状态转换）

```
草稿 Scratch ──分诊(14天)──▶ 律条/形制/规程/议定/时务/史册（或删除）
时务 Board ──清账──▶ 史册（降级归档）/ 议定（若产生结论）
实验 ──▶ 时务(计划) → 史册(原始日志) → 议定(结论)   ← 一份记录，三次迁移
事故 ──▶ 史册(时间线) → 时务(行动项) → 律条(红线，带 derived_from)
```

**迁移本身是治理事件**：迁移时必须写 `derived_from` 反链，禁止静默搬家。

## 3.6 审查（你把"维护"改成"审查"是本节最锋利的一刀）

分工结论成立：**在 vibe coding 下，生产几乎全由 agent 完成，人的唯一深度介入点是审查**。于是"谁维护"塌缩为"谁审查、审多重"。

你的洞察可以直接写成公式：

> **审查强度 ∝ 该模型的峰值热度 × rank × stale_risk**

即"越容易被参考的文件，越要重点审查"。注意是**峰值**热度不是平均热度——AGENTS 平均读得少（只在开工），但一旦读就全量生效，所以要最重审查。这也解释了你"读少写重"的疑惑：**读少不等于不重要，等于峰值集中**。

| 档位 | 适用模型 | 机制 |
|---|---|---|
| 重 | 纲领 / 图谱 / 律条 / 时务的表头 | 人逐条审 + 每次宪法级改动记议定 |
| 中 | 形制 / 规程 | 季度 + 触发式；规程附加**实操演练** |
| 轻 | 议定（只在写入时审一次） / 自述 | 写入审 + 隐私审 |
| 仅机器 | 史册 / 草稿 / 生成件 | 内容不审，但链接/front-matter/新鲜度校验**永不豁免** |

---

# 四、模型（04-模型.md）：十个模型的一页契约 ★

命名设计原则：**双名制**——中文名表语义（供人记忆），英文 id 表体裁（供文件名/front-matter 使用）。

## M1 纲领 Charter
- **定位**：这份协作的宪法 + 身份证，agent 上电即读
- **成员**：AGENTS、SOUL、README 身份卡、THISIS、公理级红线、VISION/PRINCIPLES
- **嬗变**：极少改写；每次改动 = 宪法修正（人签 + 记议定）
- **热力**：定向 ★★★，其余 ★
- **审查**：最重
- **退役**：不退役，只修正
- **硬规则**：≤200 行；身份卡单一来源（README 首段为 mirror，CI 逐字校验）；只收 ≤10 条红线；**agent 产出永远是 proposed**

## M2 图谱 Atlas
- **定位**：意图→位置的路由表；唯一无法由工具合成的导航件
- **成员**：INDEX、registry、SKILLS 清单；生成件：TREE、BRIEF
- **嬗变**：高频改写（链接漂移是主风险）
- **热力**：定向 ★★★ / 摸底 ★★★
- **审查**：重，但人工只审语义路由，链接交给 CI
- **硬规则**：**条目主键是"你想知道什么"，值才是文件路径**；CI 零死链；每条一句话摘要；有文件工具时 TREE 不生成

## M3 律条 Codex
- **定位**：唯一会被当指令执行的层
- **成员**：CONVENTIONS（含 STYLE）、SECURITY 政策、LIMITATIONS 禁令、用词规范、提交/分支规范、测试要求
- **嬗变**：随政策改写；条目级变更记议定
- **热力**：实施 ★★★ / 设计 ★★ / 收尾 ★★（← 你观察到的阶段依赖在此显形）
- **审查**：重，每条必须可执行
- **硬规则**：每条 must/never + `enforced_by` 与 `review_by` **二选一必填**；机器配置是 source、md 是 mirror；禁用"尽量/应当考虑"类不可判定表述

## M4 形制 Schematic
- **定位**：系统现在长什么样（不含命令、不含理由）
- **成员**：ARCHITECTURE（含"原则与取舍"章）、GLOSSARY、LIMITATIONS 能力边界、DESIGN/SPECS、DATA-MODEL、FAQ、COMPATIBILITY、DIAGRAMS
- **嬗变**：随演进重写，不留史（历史归议定）
- **热力**：摸底 ★★★ / 设计 ★★★ / 实施 ★★
- **审查**：中
- **硬规则**：能生成的不手写（API 文档、依赖表一律 `origin: generated`）；出现"我们选择 X"必须挂 ADR 反链

## M5 规程 Runbook
- **定位**：照着做就能完成一件事
- **成员**：CONTRIBUTING 步骤、RELEASE/DEPLOY/INSTALL/SETUP、DEBUGGING/TROUBLESHOOTING、MIGRATION/UPGRADE、HOWTO/TUTORIAL/EXAMPLES、PLAYBOOK、SECURITY 披露流程
- **嬗变**：随工具链改写；**必须实操验证**
- **热力**：实施 ★★★ / 收尾 ★★★ / 设计 ★★
- **审查**：中 + 演练（dry-run）
- **硬规则**：`last_verified` 是生命线，**过期的 runbook 比没有更危险**；示例必须可执行（CI 跑）；步骤与约束分离，约束条款上缴 M3

## M6 议定 Ledger
- **定位**：为什么变成这样（含"为什么不选那条路"）
- **成员**：ADR/、RFC/、已定稿 PROPOSALS、POSTMORTEM 结论、EXPERIMENTS 结论；生成件：DECISIONS 索引
- **嬗变**：**冻结**，只能被新议定显式 supersede
- **热力**：复盘 ★★★ / 摸底 ★★ / 设计 ★★（query 优先）
- **审查**：写入时一次审到位，此后不再审
- **硬规则**：三相链接——`considered`（事前否选项，**负向知识必须可检索**）+ `derived_from`（事中）+ 被形制反链（事后）；**禁止隐式取代**

## M7 时务 Board
- **定位**：现在卡在哪、接下来做什么（意图 ≠ 授权）
- **成员**：ROADMAP、PROBLEMS、LESSONS、KNOWN_ISSUES、TODO（文档侧）、PLANS、EXPERIMENTS 计划、RETRO 行动项、METRICS/DASHBOARD
- **嬗变**：高流转；条目级 `status/owner/due/derived_from`
- **热力**：设计 ★★★ / 定向 ★★ / 复盘 ★★★
- **审查**：**最频繁**（月度/季度清账），但单条轻
- **硬规则**：不变式 3——**永不构成行动授权**；四选一清账（验收/改期/关闭/降级入史册）；与代码内 TODO 对账、孤儿报警；PROBLEMS 同时是**治理兜底出口**

## M8 史册 Archive
- **定位**：当时到底发生了什么（永不作为指令来源）
- **成员**：dialogue/、incidents/、CHANGELOG、RELEASE-NOTES、experiments 原始数据、BENCHMARKS 结果、MEETING-NOTES、LOGS、PAPERS/sources 原文、POSTMORTEM 时间线
- **嬗变**：只增不改
- **热力**：复盘 ★★★，其余 never-push
- **审查**：无内容审查，机器校验不豁免
- **硬规则**：**严禁主动预热**；与时务/议定建立 `derived_from` 双向链；来源类（papers、第三方 repo 快照）标 `status: immutable`

## M9 草稿 Scratch
- **定位**：工作稿，**happy path 是被分诊或删除**
- **成员**：NOTES/、WIP、未定稿提案、脑图、agent 产出的未审内容、临时 plans
- **嬗变**：高频改写 + 删除是正常结局
- **热力**：仅作者本人（设计/实施 ★★）
- **审查**：无
- **硬规则**：TTL 14 天强制分诊；**永不作 instruct**（只能 `treat: object`）；分诊动作本身留痕；是唯一允许"用完即删"的模型

## M10 自述 Self
- **定位**：协作者的自述与环境，随 agent 走、与 repo 解耦
- **成员**：USER、MEMORY(user 级)、AGENTS.local、PERSONA、本机 config/环境说明、个人 skills 清单
- **嬗变**：持续小改（自动沉淀 + 人工修正）
- **热力**：复盘 ★★★（记忆 agent 的主战场）/ 定向 ★★
- **审查**：轻 + **隐私审查**
- **硬规则**：`scope: user|machine`；不入 repo；含个人信息永不进共享语料；**个人偏好不得上升为团队规范**（必须经议定）

## 域外带（免分类但不免校验）
LICENSE、NOTICE、AUTHORS、CITATION、FUNDING、CODE_OF_CONDUCT、SUPPORT、第三方 VENDOR 条款。契约极简：保持存在、与版本一致、不入 agent 语料、改动需人签。**不为它们建模型**——它们面向法务/社区而非协作回路。

---

# 五、归类（05-归类.md）：映射总表 ★

按你要求覆盖大多数文档（含你清单之外的常见件）。`gen` = `origin: generated`。

| 模型 | 文档（覆盖面尽量广） |
|---|---|
| **M1 纲领** | AGENTS、CLAUDE、GEMINI、.cursorrules、copilot-instructions、SOUL、IDENTITY、THISIS、README(身份卡)、VISION、MISSION、PRINCIPLES、VALUES、公理级红线 |
| **M2 图谱** | INDEX、registry、SKILLS 清单、MANIFEST、CHEATSHEET；gen：TREE、BRIEF、outline |
| **M3 律条** | CONVENTIONS、STYLE、CODING-STANDARDS、LINT 说明、SECURITY(政策)、LIMITATIONS(禁令)、TESTING(要求)、CODE-REVIEW 标准、COMMIT/BRANCH 规范、VERSIONING 政策、GLOSSARY 的 usage 条款 |
| **M4 形制** | ARCHITECTURE、DESIGN、SPECS、GLOSSARY、TRADEOFFS、LIMITATIONS(能力边界)、OVERVIEW、DOMAIN、DATA-MODEL、DIAGRAMS、FAQ、PERFORMANCE(现状)、COMPATIBILITY、MODELS；gen：API/OpenAPI/typedoc |
| **M5 规程** | CONTRIBUTING(步骤)、RELEASE、DEPLOY、INSTALL、SETUP、ONBOARDING、DEBUGGING、TROUBLESHOOTING、MIGRATION、UPGRADE、HOWTO、TUTORIAL、EXAMPLES、PLAYBOOK、RUNBOOK、TESTING(怎么跑)、BENCHMARK(怎么测)、SECURITY-disclosure |
| **M6 议定** | ADR/、RFC/、已定 PROPOSALS/、SPECS(已裁决)、POSTMORTEM(结论)、RETRO(决议)、EXPERIMENTS(结论)；gen：DECISIONS 索引 |
| **M7 时务** | ROADMAP、PROBLEMS、LESSONS、TODO、KNOWN_ISSUES、PLANS、BACKLOG、MILESTONES、RISKS、EXPERIMENTS(计划)、RETRO(行动项)、METRICS、DASHBOARD、当前 sprint/任务板 |
| **M8 史册** | dialogue/、incidents/、CHANGELOG(gen)、RELEASE-NOTES、MEETING-NOTES、STANDUP、LOGS、EXPERIMENTS(原始)、BENCHMARKS(结果)、DATASETS、PAPERS/、sources/、THIRD-PARTY 快照、POSTMORTEM(时间线) |
| **M9 草稿** | NOTES/、WIP、DRAFT、scratch/、未命名笔记、脑图、by-ai 未审提案、临时 plans |
| **M10 自述** | USER、MEMORY(user)、AGENTS.local、PERSONA、LOCAL、ENVIRONMENT、个人 config |
| **域外带** | LICENSE、NOTICE、AUTHORS、CITATION、FUNDING、CODE_OF_CONDUCT、SUPPORT、VENDOR |
| **待定/挂起** | 补偿（无判别依据，黑名单）、CONTEXT（禁用，改名后重归）、outline（并入图谱） |

---

# 六、孤例（06-孤例.md）：你最纠结的那个问题 ★★

**问题原文**："有的文件在维度上需要单开一列，甚至同一个文件在多个维度都是单独成列的，应该单独说明吗？"

**答案：不单独说明。孤例不进轴，进模型。三段判据：**

```
① 只在一条角度上单列
   → 不解释。字段本来就是为此设计的（SOUL 的 target: harness 就是一个字段值）。

② 在多条角度上同时单列 → 跑"一页契约测试"：
   能否为它写出不自相矛盾的一页治理契约？
   ├─ 能，且与现有 10 个模型的契约都不同
   │    → 它是新模型的模式标本，立模型（成员数 = 1 完全合法）
   ├─ 能，但与某模型契约一致
   │    → 归入该模型，单列值降为注解
   │      【实例】SOUL 同时是 harness 单列 + axiom 单列 + user 单列
   │       → 契约是"极少改写 + 最重审查 + instruct" = 纲领 M1
   │       → 归 M1，其余三个单列值写进修饰符字段，不展开说明
   └─ 不能（契约自相矛盾）
        → 它是嵌合体（chimera），拆文件
          【实例】LIMITATIONS = 能力边界(M4) + 行为禁令(M3) → 拆成两份

③ 永不为孤例加新角度——轴是共享坐标，模型才是容纳孤例的容器。
```

**识别嵌合体的信号**：写契约时出现"这个条款在两种情况下相反"（如：能力边界随代码改写、禁令随政策冻结）。**只要一页契约写不顺，就是拆分信号，不是加轴信号。**

**另外三例落点**（顺带清掉）：

| 孤例 | 判定 | 理由 |
|---|---|---|
| AGENTS | M1 模式标本 | 一个仓库天然只有一份，契约独一无二 → 模型代表 |
| CHANGELOG | M8 + `origin: generated` | 不是孤例，是"追加族 + 生成修饰符"的正常组合 |
| 本研究（doc-models/） | 自我归类：M9→M6→M8 | 草稿讨论 → 议定（判词）→ 史册（对话留痕） |

---

# 七、挂起（90-挂起.md）

| 项 | 归属 | 挂起期临时约定 |
|---|---|---|
| read 工具语义 / 加载实现 | how-agent-read-file | 文档侧只承诺三契约：可发现（INDEX 可达）/ 可判定（push 条件机检）/ 可拒载（草稿与留痕可排除） |
| user 目录下 skills 能否被读取 | how-agent-read-file | 原则：**scope 定义检索根**。`~/.{user}/{ai}/skills` 是否可达取决于 harness 的发现规则，文档侧只需声明每级 scope 的根路径，不做承诺 |
| 层级 rank 深度对比 | compare | 沿用 `rank 先于 scope` 的冲突链 |
| 文档—证据分离模式 | 证据分离专题 | 沿用 `derived_from` 双向链 + 模型迁移图（3.5） |
| 补偿 | 待定义 | 黑名单（判别测试：它改变了哪个治理动作？） |
| reader 维护策略 | skill 章 | 二等公民：不入 agent 语料，但不免 source/mirror 校验 |

---

# 八、与你草案的差异清单（便于你复核我改了什么）

| 你的草案 | 本轮处置 | 理由 |
|---|---|---|
| 四判据含"正交性/最少轴数" | 换成"可重复判定 + 模型数≤10" | 工程上要的是判定一致，不是坐标美观 |
| 4 个角度（载入/时间/辖域/受众） | 分类轴降为 1 根（模型），其余拆成修饰符/说明 | 解决"单列"与"正交难"的共同病根 |
| Mutation 仅作说明 | **升为模型族骨架** | 时间预测不了治理，嬗变几乎完全预测 |
| 时间（含元）作方向 | 彻底降为说明；元改 `subject: meta` | 元是记述对象不是时间值；plans 横跨三态 |
| 草稿/受控作"认知姿态" | 拆为 `status` + `treat` 两个修饰符 | 草稿可入上下文（以 object 身份），只是永不作指令 |
| `by{ai}` 文件名后缀 | 否决，改 `author` + 状态机规则 | 文件名是路由主键；**agent 只能产出 proposed** 比标签更硬 |
| developer/agent 的维护维度 | 改为**审查维度** + 强度公式 | vibe coding 下生产归 agent，人只深度介入审查 |
| `assistant` / `default` 命名 | → **自述 Self** / 其余九型 | default 是"没想好"的名字；模型名应携带契约语义 |

---

**下一步建议**（二选一）：
1. 我把 `04-模型.md` 与 `05-归类.md` 展开成可直接落盘的完整正文（含每个模型的完整契约条款与全量映射表）；
2. 或先跑**盲测**：你随便丢 10 个冷门文档名给我，验证"可重复判定"这条判据能不能扛住——扛不住的地方就是模型清单的缺陷所在。