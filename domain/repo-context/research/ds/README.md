# ds —— deepseek-harness 与 Raven 的文档体系拆解

本目录拆解 `D:\workspace\memory\sources\repos\` 下两个仓库的 `.md` 文档体系**是如何设计的**：它们各自用什么维度给文档分类、如何编码生命周期、如何选格式与命名、如何（用脚本或纪律）维持一致性。

## 本目录

| 文件 | 内容 |
|---|---|
| `deepseek-harness.md` | DSH 的文档体系拆解——kind 系统、Agent Notes 状态机、双语配对、门禁栈、无索引哲学 |
| `raven.md` | Raven 的文档体系拆解——AGENTS 硬约束、CONTEXT 领域语言地图、plan/spec 双轨、语言豁免区 |
| `README.md`（本文件） | 两套体系的速览与横向对比，及其对本仓库研究议题的回应 |

## 两个样本速览

| | deepseek-harness | Raven |
|---|---|---|
| **规模** | `.md` **3668** 篇（`.zh.md` 1646、`.i18n.yaml` 1643）；`.agents\notes\` 2206 篇 | `.md` **307** 篇（zh 15）；`docs\specs\` 54、`docs\plans\` 28 |
| **核心文档** | `AGENTS.md`(179) / `docs\AGENTS.md`(文档标准) / `.agents\notes\README.md`(生命周期定义) / `.agents\skills\dsh-doc\`(标准执行器) | `AGENTS.md`(413，硬约束) / `CONTEXT.md`(2646，领域语言) / `CONTEXT-MAP.md`(24，上下文地图) |
| **主导哲学** | **工业化**：让机器管文档——kind→模板、门禁→脚本、预算→清单 | **规范密度**：让少数核心文档承载极重规范，靠编号与引用维持一致 |

## 横向对比

### 1. 索引：要不要一个"总目录"

- **DSH：明确禁止 INDEX.md。** `.agents\notes\README.md` 直接写 "Do not add a centralized `INDEX.md`"，并由一条独立 Agent Note（`implemented\process\2026-07-19-remove-generated-agent-note-index.md`）承载理由。替代方案是**路径即索引**（`lifecycle/class/date` 就是查询维度）+ 全文搜索 + 分级 AGENTS.md。
- **Raven：有索引，且索引带性质声明。** `docs\README.md` 逐项列出文档，并明确区分"当前树描述"与"dated records kept for their history"。

> 这正好回答了本仓库 `README.md` 的疑问"index 总不能指向具体文件吧？"——两个样本给出了两种截然不同的答案：要么让路径承载索引，要么让索引承载时效标注。

### 2. 决策记录：怎么存"我们为什么这么选"

| | DSH | Raven |
|---|---|---|
| 载体 | `.agents\notes\` | `docs\plans\` + `docs\specs\` |
| 分类 | 生命周期 × class（两轴路径编码） | 过程(plan) / 结论(spec)（双目录） |
| 命名 | `{lifecycle}/{class}/yyyy-mm-dd-topic.md` | `YYYY-MM-DD-slug.md` / `YYYY-MM-DD-slug-design.md` |
| 状态 | 目录即状态：`proposed`→`implemented`→`rejected`/`archived` | `Status:` 头部字段 + 顶部横幅（如 `Superseded — kept as a task record`） |
| 历史处理 | `archived\` **冻结不可变**，门禁跳过、只增清单校验 | 横幅自我声明时效，"archive, deliberately not held to today's layout" |
| 格式强制 | `verify-agent-note-format` 脚本 + 固定头三行 | 骨架靠约定（Goal/Architecture/Constraints/File Structure），不脚本强制 |

### 3. 双语

- **DSH：全量结构配对。** `foo.md` + `foo.zh.md` + `foo.i18n.yaml` sidecar；标题/列表/表格/代码/链接/**物理行数**全部对齐；每次编辑 `verify-translation-pairing --write` 重录。翻译是**结构契约**。
- **Raven：默认英文 + 具名豁免区。** 源码全英文，CJK 仅在 owner 签名的白名单区（如 `raven/i18n/`、`docs-site/`、`plugins-dist/ppt-engine/`）内合法；`*.md` 后缀被整体豁免；`scripts\check_source_language.py` 逐 PR 强制。翻译是**受控例外**。

### 4. 模板与格式

- **DSH：显式一一映射。** frontmatter 的 `kind` 字段 → `templates\` 下唯一模板；新增 kind 必须同时带来模板文件 + 仓库位置 + 聚焦检查。格式由机器查表决定。
- **Raven：约定式骨架 + 编号规范。** 用 `§N.M` 编号让规则**可被引用**（plan 里写 `(AGENTS.md section 4)`），用 ✅/❌ 对照表传递格式，靠纪律而非脚本。

### 5. 一致性的维持手段

- **DSH：重度门禁。** `test:docs` / `doc-sync` / `verify-doc-budgets` / `verify-md-links` / `verify-repository-references` / `verify-archived-agent-notes` / `verify-translation-pairing`，外加 `doc-budgets.manifest.json` 字数预算与 slop 清单。
- **Raven：轻量门禁 + 高规范密度。** 脚本只覆盖语言边界（`check_source_language.py`）与大文件（`check-large-files`）；一致性主要靠 `AGENTS.md` 的硬约束与"引用而非重述"纪律。

### 6. 一个同构细节：CLAUDE.md 指针

两个仓库都用**内容重定向**让不同 harness 共享同一份规范，而非符号链接：

- DSH：`CLAUDE.md` 是 **9 字节**文件，内容为 `AGENTS.md`（`file` 报 `ASCII text, with no line terminators`）。
- Raven：`CLAUDE.md` 内容为 `./AGENTS.md`。

### 7. 命名约定的分歧

- DSH 中文对后缀：`.zh.md`（如 `README.zh.md`）。
- Raven 中文对后缀：`.zh-CN.md`（如 `README.zh-CN.md`）——根级文档用 locale 全称，代码运行时目录用 `i18n\messages.json`。
- DSH 决策文件：`yyyy-mm-dd-topic-title.md`（小写、连字符）。
- Raven 决策文件：`YYYY-MM-DD-slug.md`（大写日期 + `-design` 后缀区分 spec）。

## 两种哲学，一句话

- **DSH 相信"能被脚本校验的才可靠"**：3668 篇文档不可能靠人守住一致性，于是把分类、模板、生命周期、双语、字数全部编码成机器可查的规则。
- **Raven 相信"规则要少、要能被精确引用"**：307 篇文档用三份核心文件（约束 / 语言 / 地图）撑起规范密度，宁可写清 `§N.M` 让人引用，也不复制规则。

两者不是优劣，而是**规模驱动**：DSH 的文档量级（3668）要求自动化治理，Raven 的量级（307）允许纪律治理。对本仓库 `README.md` 提出的治理议题，它们分别示范了**"大规模机械治理"**与**"小规模规范治理"**两端。

---

> 拆解依据均为仓库内实测（文件清单、`wc -l`、文件字节数、元文档原文），引用处标注了路径；未对任何文档的运行时可验证性做超出静态取证范围的断言。
