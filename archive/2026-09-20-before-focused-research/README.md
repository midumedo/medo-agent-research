# Memory 与上下文工程

面向已了解 LLM 与 Agent 的进阶读者，逐步理解 Agent、Context 与 Memory，形成可审查、可纠错的认知体系，再编写教材与多视图手册。

**当前先积累认识。** 项目结构和教材顺序尚未锁定，可以先深拆一些项目或论文，搞清它们实际上怎样运行、怎样论证，再发现问题、比较方案和修订领域模型。

## 两个研究入口

- [deepdive/](deepdive/README.md)：从对象开始。忠实拆清一个项目或论文，保留结构、路径、推理、局部评价与未知；无需预先命中主线。
- [analysis/](analysis/README.md)：从问题开始。围绕具体问题开展解释、比较、综合与检验；可以只研究一个系统。

两者会相互推动，不要求先后完成整个阶段。现有 H1/H2/H3 是工作假设，不是准入条件。研究结果可以是更清楚的对象模型、新问题、条件性判断或负结果；不要求每篇都有普遍结论。

## 职责结构

| 位置 | 主要回答 |
|---|---|
| [sources/](sources/README.md) | 外部原件和所用版本是什么？ |
| [deepdive/](deepdive/README.md) | 这个项目或论文实际是什么，如何运作，依据到哪？ |
| [analysis/](analysis/README.md) | 这个问题怎样解释、比较或检验？ |
| [notes/](notes/README.md) | 本项目决定怎么做，为什么？ |
| [domain/](domain/index.md) | 我们当前怎样理解这个领域？ |
| `entries/`（后期） | 怎样保留条件和依据，提炼成可组装的单元？ |
| `output/`（后期） | 怎样按读者的学习或使用目的呈现？ |

以上目录均在根级。`deepdive/`、`analysis/` 与 `notes/` 在存放上并列；Notes 记录项目决定，不是知识必须经过的阶段。配套的 `evidence/` 支撑具体主张，`dialogue/` 保存交流，`archive/` 保存旧版。

后期采用 `output/book/` 与 `output/manual/<视图>/`。目前 `entries/`、`output/` 只确定职责，不提前建立空目录。认知可以被修正，未来条目和产物随来源变更而更新。

## 怎么读

- [ARCHITECTURE.md](ARCHITECTURE.md)：完整职责设计，两种研究入口如何形成认知。
- [deepdive/README.md](deepdive/README.md)：当前直接拆源码、读论文的工作方式。
- [domain/index.md](domain/index.md)：已有概念与机制，暂定解释可被新的对象认识改写。
- [THESIS.md](THESIS.md)：已有工作假设；[研究议程](analysis/research-agenda.md) 保留可选分析与实验。
- [项目深度审查](analysis/project-review-2026-09-20.md)：此前为何修正证据越界、不可撤回认知与来源混杂。
- [本次职责调整](notes/2026-09-20-deepdive-and-research-roles.md)：为何增加探索入口，并修正上一版过早要求问题驱动的约束。

## 目前有哪些积累

认知层已有工作定义、竞争解释与一篇上下文留存机制；分析层有两篇修订过的 Claude Code 策略与成本文章、综述导航和历史调研。它们均注明来源与推断边界。

Deepdive 目前有工作入口，还没有完整对象稿。下一次可以选择真实项目或论文开始，不需要先定教材章节。既有分析也不会仅因名字像“拆解”就被搬过去，冒充已完成源码审查。

本地已核对部分论文段落，但没有完成全库内容复核或成对模型行为实验；厂商行为、来源版本仍存在明确待核实项。具体对象的已知范围见 [研究对象](domain/systems.md)。

## 维护

AI 每轮读 [AGENTS.md](AGENTS.md)、领域入口与当前主线；动手时按需读维护 skill。归属规则见 [CONVENTIONS.md](CONVENTIONS.md)，表述见 [STYLE.md](STYLE.md)，后期产物取舍见 [TRADEOFFS.md](TRADEOFFS.md)。

当前根目录没有 Git 版本历史。两次结构调整均保留涉及文件的快照：[架构审查前](archive/2026-09-20-architecture-review-before/SNAPSHOT.md)、[增加 Deepdive 前](archive/2026-09-20-before-deepdive/SNAPSHOT.md)。它们用于恢复对应文件，不代表项目全量备份。
