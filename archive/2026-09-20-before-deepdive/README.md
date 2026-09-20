# Memory 与上下文工程

面向已了解 LLM 与 Agent 的进阶读者，研究 Agent 如何把过去的信息变成未来可用、可更新、可追责的决策依据。

**当前核心资产是认知体系，教材与手册是后期产物。** 我们希望积累的不是产品功能清单，而是有依据的工程判断：什么条件下选什么、为什么、什么时候会坏，以及怎样发现选错了。

## 从哪里开始

- **了解当前设计**：[ARCHITECTURE.md](ARCHITECTURE.md)。项目如何组织研究、证据、纠错与未来产物。
- **看这次深度审查**：[项目审查](analysis/project-review-2026-09-20.md)。旧设计的具体问题、反证与处理。
- **进入领域研究**：[domain/index.md](domain/index.md)。工作定义、机制、研究对象与未决问题。
- **看接下来要检验什么**：[THESIS.md](THESIS.md) 与 [研究议程](analysis/research-agenda.md)。

2026-09-20 的重建修正了“认知只增不推翻”、来源与我方解释混杂、若干全称断言和规则漂移。已依据本地原文纠正部分事实；产品行为仍有待核实项，**尚未完成成对模型行为实验**。

## 项目覆盖什么

重点是任务内与跨任务的信息保持、上下文组装、外部记忆、程序性记忆，以及这些机制的更新、恢复与评价。Harness 只研究与信息状态和决策有关的部分；不扩成全部 Agent 工程的百科。

Memory、Context、Harness 是不同类型的对象，工作定义见 [领域基础](domain/foundations.md)。已有术语与分类用来解释问题，不能强迫所有系统具有同一种模块结构。

后期教材按学习路径组织；手册按决策、产品或症状提供多个视图。两者从认知层分别派生，目前不提前写。

## 材料如何分工

| 位置 | 用途 |
|---|---|
| [domain/](domain/index.md) | 当前领域解释，包含推理、边界与反例 |
| [analysis/](analysis/README.md) | 调查、比较、系统分析和检验设计 |
| [sources/](sources/README.md) | 外部原件、转换件及来源元数据 |
| `evidence/` | 已引用的原文片段、代码定位与观测记录 |
| `notes/` | 设计决定与修订理由 |
| `dialogue/` | 历史交流与研究过程 |
| `archive/` | 旧稿与可恢复快照 |

单篇分析不是已证实事实，官方文档也不自动证明策略优越。阅读时先看来源、条件和作者的推断边界。

## 当前最值得研究的选择

第一项是保留原文、摘要和按需恢复如何组合；第二项是更正、冲突与删除能否传播到后续决策；第三项是如何分开内容效果与缓存费用。具体比较、基线和会改变判断的结果已写入 [研究议程](analysis/research-agenda.md)。

已有两篇 Claude Code 分析已经修订为有边界的论证，并明确旧产品事实的来源缺口。论文导航和早期调研属于我方分析，入口在 [analysis/README.md](analysis/README.md)，不能当作外部原文的权威摘要。

研究系统按问题选择，不按清单逐一凑齐。原始关注对象保留在 [历史目标](archive/2026-09-20-architecture-review-before/BRIEF.md)，它是候选池，不是完成度清单。

## 维护入口

AI 每轮读 [AGENTS.md](AGENTS.md)、领域入口和当前主线；修改时按需读维护 skill。目录归属见 [CONVENTIONS.md](CONVENTIONS.md)，表述与术语见 [STYLE.md](STYLE.md)，未来产物取舍见 [TRADEOFFS.md](TRADEOFFS.md)。

本次修改前已保存 [快照与校验清单](archive/2026-09-20-architecture-review-before/SNAPSHOT.md)。当前根目录没有 Git 版本历史，快照只能恢复本次涉及文件，不替代完整备份系统。
