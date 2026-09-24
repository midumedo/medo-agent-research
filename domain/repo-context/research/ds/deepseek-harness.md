# deepseek-harness 文档体系拆解

> 源：`D:\workspace\memory\sources\repos\deepseek-harness\`
> 规模实测：`.md` 3668 个，其中 `.zh.md` 1646 个、`.i18n.yaml` 1643 个；`.agents\notes\` 下 2206 个。
> 一句话定位：一套**把文档当工程产物管理**的体系——每篇文档有 kind、有模板、有生命周期状态、有双语配对、有字数预算、有 CI 门禁。

---

## 0. 这是什么项目的文档

deepseek-harness（简称 dsh）是 pnpm monorepo（`pnpm-workspace.yaml`、多份 `vitest.*.config.ts`），核心是 Cordis 插件框架（`docs\cordis-primer.md`、`docs\cordis-api\`、`docs\cordis-tutorial\01..07`）。它自带一个 CLI（`dsh`）与 Web 端，文档量级远超普通项目——**文档本身就是产品的一部分**（`website\` 是把仓库 Markdown 投影成的文档站）。

因此它的文档体系不是"写几个 md 说明一下"，而是三条正交分类轴 + 三套生命周期 + 一整套自动化门禁。

---

## 1. 文档拓扑：三个分区 + 一个包契约层

```
deepseek-harness\
├── README.md / README.zh.md            ← 对外门面（+ .i18n.yaml sidecar）
├── AGENTS.md                           ← 工作流与自检约束（179 行，Agent 每次任务必读）
├── CLAUDE.md                           ← 9 字节指针文件，内容仅 "AGENTS.md"
├── CONTRIBUTING.md / .zh.md            ← 协作规范
├── SAFETY.md / .zh.md                  ← 安全边界
├── BRAND_GUIDELINES.md / .zh.md        ← 品牌规范
├── BENCHMARK.md / THIRD_PARTY_NOTICES.md
│
├── docs\                               ← 人类文档（跨包知识）
│   ├── AGENTS.md                       ← 【文档标准本身】层级 + 字数预算 + slop 清单
│   ├── architecture.md / glossary.md / module-graph.md / graph-atlas.md
│   ├── capability-seams.md / event-producer-consumer.md / defensive-patterns.md
│   ├── agent-lifecycle.md / config-catalog.md / persistence-catalog.md
│   ├── cookbook\                       ← 教程（adding-a-tool / adding-an-llm-adapter …）
│   ├── cordis-tutorial\                ← 编号教程 01..07 + index
│   ├── cordis-api\                     ← API 参考（context / events / fiber / registry / service）
│   ├── i18n\                           ← 翻译规范（translation-rules / terminology / style-samples）
│   ├── persistence-changes\            ← 持久化格式变更记录，每条配 .schema.json
│   │   ├── 2026-09-11-initial.md (+ .zh.md + .i18n.yaml + .schema.json)
│   │   ├── historical-formats\         ← v0/v1/v2 历史格式快照
│   │   └── releases\                   ← 每个 RC 版本一份（dsh-v0.0.1-rc.1..3）
│   ├── postmortem\ / subsystems\ / user\
│   └── testing.md / development.md / dependency-catalog.json
│
├── .agents\                            ← Agent 体系（只读规范 + 决策记录）
│   ├── notes\                          ← 【Agent Notes】决策/提案的生命周期树
│   │   ├── README.md / README.zh.md    ← 【定义】生命周期、分类、格式
│   │   ├── AGENTS.md
│   │   ├── proposed\{class}\
│   │   ├── implemented\{class}\
│   │   ├── rejected\{class}\
│   │   └── archived\{class}\           ← 冻结，门禁跳过
│   └── skills\                         ← Skill 化的工作流
│       ├── dsh-doc\                    ← 【文档标准执行器】SKILL + templates\ + references\
│       ├── dsh-archive-agent-notes\    ← 归档 workflow
│       ├── dsh-translate-docs\         ← 翻译 workflow
│       ├── dsh-prose-standard\         ← 句级写作规范
│       ├── dsh-trim-cot-leakage\       ← 清理推理转录泄漏
│       └── dsh-pre-push-checks\ / dsh-code-review\ / …
│
├── packages\<pkg>\README.md            ← 包契约，就近放在代码旁
└── website\                            ← docs\ 的投影站点（.generated\ 是产物，不可手改）
```

---

## 2. 三条正交分类轴

dsh 的设计核心是：**一篇文档同时被三个维度定位**。

| 轴 | 取值 | 编码位置 | 决定什么 |
|---|---|---|---|
| **① 读者 / 职责**（kind） | `package-group` `package-reference` `package-library` `package-bundle` `persistence-change` `persistence-release` `persistence-format` … | frontmatter `kind:` | 选哪个模板、允许哪些章节 |
| **② 生命周期**（lifecycle） | `proposed` → `implemented` →（`rejected` / `archived`） | 目录第一层 | 文档处于提案/已落地/被否/冻结 |
| **③ 决策类别**（class） | `feature` `bug-fix` `simplification` `architecture` `process` `testing` | 目录第二层 | 这条决策的性质 |

轴 ②③ 只作用于 Agent Notes（`.agents\notes\`）；轴 ① 作用于人类文档与包 README。

关键约束：**class 是封闭集合**，由 `scripts\agent-note-tree.ts` 定义，分类门禁拒绝其它目录名；新增一个 class 必须同步改"规范集合 + notes\README 章节"。`refactor` 被**故意排除**——它与 `simplification` 重叠，后者的判别式"可观察行为是否变化"已经覆盖。

---

## 3. kind 系统：frontmatter 驱动模板映射

`kind` 字段与模板是**一一对应**的（在 `dsh-doc` skill 中定义）：

- `package-group` → `templates\package-group.md`：族群地图（`packages\README.md`、`packages\<group>\README.md`）
- `package-reference` → 插件/服务包的 README：挂载配置 + 配置表 + 折叠实现 + Model Experience + Known Limitations
- `package-library` → 无插件面的库：消费者入口，**没有** profile 安装路径
- `package-bundle` → 声明 `dsh.bundle.patch` 的包：经核验的 `dsh plugin` 安装路径
- `persistence-change` / `persistence-release` / `persistence-format` → 持久化三类记录

规则很硬：**每个 kind 恰好对应一个模板文件，每个模板恰好反哺一个 kind**；"新增 kind"必须同时带来一个新模板文件、一个文档化的仓库位置（或声明的 owner）、以及一个把文档映射到该 kind 的聚焦检查。这堵死了"随手新增一种文档类型"的路。

---

## 4. Agent Notes：状态机 + 路径编码

`.agents\notes\README.md` 给出的定义值得完整引用：

> 一个 **Agent Note** 记录一个影响本代码库的决策或提案——*为什么*与*我们放弃了什么*，即代码和文档无法承载的部分。

**路径即元数据**：`{lifecycle}/{class}/yyyy-mm-dd-topic-title.md`

- 日期是**该主题首次被提出**的时间（依 git 历史），不是修改时间。
- 文档在生命周期目录间**移动**（状态即位置），不是原地改状态。
- 交叉引用**必须用相对 markdown 链接**（`[topic](../../implemented/architecture/2026-…-….md)`），禁止裸写编号或散文——这样链接可被机器校验，且移动后仍成立。

**统一文件格式**（由 `pnpm run verify-agent-note-format` 强制，属 `doc-sync`）：

```
# Agent Note: <title>
                     ← 空行
Status: <status>     ← 三选一，且必须与所在生命周期目录一致（门禁交叉校验）
```

`Status` 三种形式：`proposed` / `implemented` / `rejected — <一句话原因>`。状态行**不带日期、不带括号**；"以修正形式通过"之类是正文内容。被拒 note 是唯一带内容的 status，因为"为什么被否"正是读者要的事实。

**各类生命周期正文骨架**（`## Problem` 必为首段，且要写到"脱离解决方案也能独立成立"）：

| 生命周期 | 骨架 |
|---|---|
| `proposed\` | Problem → Proposal → …自由章节… → Alternatives considered → Acceptance criteria → Risks |
| `implemented\` | 记录已落地决策 + 被否方案，且**必须随实际发布同步更新**（路径、包名、key、默认值），但决策本身不改 |
| `rejected\` | 仅在"其理由能阻止一个诱人且实质的错误"时保留，否则**三件套（英/中/sidecar）一起删除** |
| `archived\` | 冻结历史。归档只允许：移动完整三件套、保留 `Status: implemented`、在两份语言文件中插入同一行 `Archived: YYYY-MM-DD`、重录 sidecar、修复或删除入链 |

**归档是不可逆的分界**：一旦封存，永久冻结——不得编辑、翻译、重排、更新、移动、删除，也不得当作当前行为的权威。文件路径 `archived/{class}/…` **故意不含 `implemented`**，因为只有 implemented 能进入归档。存储策略由标定的 `dsh-archive-agent-notes` 工作流决定，而不是看字数、年龄或配额。

**合并不允许偷懒**：被完全取代的 implemented note 可合并进当前 owner 后删除，但删除前必须保全每一条独有理由、备选、后果、必需验证与命名的覆盖缺口，并修复全部入链；**部分取代不合格**。

---

## 5. 双语机制：行对齐 + sidecar

dsh 的翻译不是"另存一份中文"，而是**结构上锁死的配对**：

- 成对文件：`foo.md` + `foo.zh.md` + `foo.i18n.yaml`（sidecar 记录配对确认状态）。
- 要求**标题、列表、表格、代码、链接、frontmatter 布局、物理行数全部对齐**。
- 每次成对编辑后必须 `pnpm run verify-translation-pairing --write <pair>` **重录** sidecar。
- 翻译规范集中在 `docs\i18n\`（`translation-rules.md`、`terminology.md`、`translation-prompt.md`、`style-samples.md`）。
- 翻译由 `dsh-translate-docs` skill 承载，不是靠人记。

**为何值得**：行数对齐让"英文改了哪一行"可以用 diff 机械定位；sidecar 让"这份翻译还确认有效吗"变成可查询状态。代价是**每次编辑都欠一份对侧更新**——因此规范明确把"配对文档"列为成本项。

---

## 6. 门禁：文档是被 CI 约束的产物

dsh 的独特之处在于**几乎所有文档规则都有对应脚本**：

| 命令 | 作用 |
|---|---|
| `pnpm run test:docs` | 快速全量文档检查（配对 / 换行 / 链接 / README 门禁 / 预算 / skill 元数据 / Agent Note 门禁） |
| `pnpm run doc-sync` | 完整同步校验（含 Agent Note 格式） |
| `pnpm run verify-doc-budgets` | 按 `scripts\doc-budgets.manifest.json` 校验字数上限 |
| `pnpm run verify-translation-pairing --write <pair>` | 重录双语配对 sidecar |
| `scripts\verify-archived-agent-notes.ts` | 校验归档树的封闭 class、完整三件套、归档元数据、sidecar 哈希、只增冻结清单 |
| `scripts\verify-md-links.ts` | 本地链接目标存在性 |
| `scripts\verify-repository-references.ts` | 拒绝维护文件中的真实 commit 标识与不允许的组织 URL |

**字数预算**是 guardrail 而非削减目标：命中或低于目标时保留至少 5% 余量；超限则冻结上限，按"迁移 → 压缩 → 提额"的有序策略处理，提额必须在 PR 里论证 manifest diff。目标示例：root `AGENTS.md` ≤ 1950、`architecture.md` ≤ 2400、子树 `AGENTS.md` ≤ 600、`docs\AGENTS.md` ≤ 1320。

**slop 清单**（`docs\AGENTS.md`，`dsh-doc` 把它当审计项跑）：重复规则、越层历史、正文里的实现状态标注（"implemented!" "future: …"——状态会腐烂）、手抄目录/JSDoc/inventory、推理转录（推导路径残留）、兄弟方法旁重复理由、段落墙、强调通胀、implemented note 里的 spec-speak（"should"、迁移计划、验收清单）。

**网站是投影不是副本**：`website\docs.ts` 是显式公开 allowlist，`scripts\project-doc-site.ts` 把 canonical `docs\` 源改写成一次性的 `website\.generated\` 树，VitePress 再构建。规矩：仓库 Markdown 永远是唯一可编辑源；翻译永远是同级配对（`foo.md` / `foo.zh.md` / `foo.i18n.yaml`），**不用 locale 目录**；`website\.generated\` / `.cache\` / `.dist\` 永不手改；移动或删除必须原子地同步源 + manifest 条目 + 入链。

---

## 7. 索引哲学：没有 INDEX.md

dsh **明确禁止**集中式索引。`.agents\notes\README.md` 写道：

> 活跃的生命周期树就是工作面清单：浏览它的 lifecycle/class 文件夹或搜索仓库。**不要**新增集中式 `INDEX.md`；[no-index Agent Note](implemented\process\2026-07-19-remove-generated-agent-note-index.md) 拥有这条理由。

理由由一条**独立 Agent Note** 承载（自指：用体系本身记录体系的规则）。替代导航手段：路径编码本身就是索引（lifecycle/class/date 即查询维度）+ 全文搜索 + 分级 AGENTS.md。这与本仓库 `domain\repo-context\README.md` 里"index 总不能指向具体文件吧？"的疑问正好呼应——dsh 给出的答案是不做 index，让路径和搜索承担。

---

## 8. 文档层级与 CLAUDE.md 指针

dsh 的 AGENTS.md 是**分级**的：

- root `AGENTS.md`（≤1950 字）：常读的 standing orders
- `docs\AGENTS.md`（≤1320 字）：文档层级、教程/参考形态、taxonomy、预算、slop 清单
- 子树 `AGENTS.md`（≤600 字，`packages\AGENTS.md` ≤750）
- `packages\<pkg>\README.md`（≤994 字）

**CLAUDE.md 是一个 9 字节的指针文件**——`ls -la` 显示 9 字节，`file` 报 `ASCII text, with no line terminators`，内容就是字符串 `AGENTS.md`（无换行）。即：Claude Code 读 `CLAUDE.md` 与其它 harness 读 `AGENTS.md`，落到同一份内容，靠**内容重定向**而非符号链接（跨平台、进 git、无链接语义问题）。

---

## 9. 设计要点提炼

1. **一份事实一个 owner**：源码、测试、生成目录、包 README、指南、Agent Notes、scratch 各自持有自己那类真相；禁止在别处重述（这正是 slop 清单的第一条）。
2. **状态即位置**：生命周期用目录表达，移动即状态转移，门禁交叉校验目录与 `Status:` 行，杜绝"文件说 approved 但目录在 proposed"的漂移。
3. **可机械校验优先**：能让脚本判的绝不靠人记——链接、配对、行数、预算、格式、归档哈希。
4. **历史分冻结区**：`archived\` 一旦封存即不可变且门禁跳过，当前文档不会因历史而腐烂，历史也不会被后人"顺手更正"而失真。
5. **模板与 kind 一一锁死**：新增文档类型有准入门槛（模板 + 位置 + 检查三件套），抑制文档类型膨胀。
6. **诚实的成本标注**：配对文档、字数预算都被显式写为成本与 guardrail，而不是假装零成本。

---

## 附：可直接借用的模式

- **CLAUDE.md 指针文件**（9 字节，指向 AGENTS.md）：零成本让多 harness 共享同一份规范。
- **frontmatter `kind` → 模板一一映射**：把"这文档该怎么写"从人的记忆变成机器查表。
- **`{lifecycle}/{class}/date-topic.md` 路径编码**：一条路径同时编码状态、类别、时间、主题。
- **双语行对齐 + sidecar 重录**：翻译从"另一份文件"变成"可校验的配对"。
- **无 INDEX.md 的论证**（用 Agent Note 记录）：索引决策本身也要有 owner 和理由。
