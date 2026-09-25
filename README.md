# Memory 与上下文工程

面向已了解 LLM 与 Agent 的进阶读者，研究 Memory、Context 与 Harness，形成能支持工程判断的主题认识，再制作教材与多视图手册。

**当前优先研究 Memory。** 围绕过去信息怎样被保存、找回、修正和复用，先拆清有机制差异的项目与论文，再判断哪些复杂度值得投入。Context 与 Harness 提供必要的使用和控制关系；领域结构与教材顺序可以随证据调整。

## 从任务选择入口

| 想做什么 | 入口 |
|---|---|
| 找外部材料与所用版本 | [Sources](sources/README.md) |
| 拆清一个项目或论文的相关机制 | [Deepdive](deepdive/README.md) |
| 研究概念、解释现象、比较方案或设计检验 | [Analysis](analysis/README.md) |
| 连贯理解一个综合主题 | [Domain](domain/index.md)；已有第一个暂定的整体运行主题 |
| 看 Memory 专题与后续教材路线 | [Output](output/README.md)；当前优先 [Memory 教材设计](output/book-memory/design.md) |
| 追溯项目讨论和重要决定 | [Dialogue](dialogue/README.md) |

Deepdive 与 Analysis 在根级并列，分别按对象和问题组织。Domain 形成更大尺度的主题综合，`output/` 中的教材设计及后续成品直接使用它们及其依据。章节草案不限制研究展开，也不等于已完成教材。

## 现在实际积累了什么

- [Agent 的持续运行](domain/agent-runtime/index.md)：首个主题综合，把 Harness、Context、Memory、反馈、修正与恢复连成整体；附状态、生命周期和失效定位的深入解释。
- [Memory 工程选择](analysis/memory-engineering-selection.md)：区分需求、机制、实现与训练前提，给出当前值得深拆的对象和比较条件。
- [Memory 教材设计](output/book-memory/design.md)：八章主干，加关系与时间、经验复用两条深入路线；含持续研究项目案例。
- [整体运行教材设计](<output/harness book/book-design.md>)：保留原十一章路线，当前作为后续参考。
- [概念与边界草稿](analysis/concepts-and-boundaries.md)：区分 Memory、Context、Harness 及相关观察维度，仍是可修正的研究框架。
- [上下文留存分析](analysis/context-retention.md)：保留、摘要、外部化与组合的条件推演，含逻辑反例和未校准的成本式。
- [问题、假设与检验议程](analysis/research-agenda.md)：候选问题与实验设计，按需使用。
- [Claude Code 策略分析](analysis/claude-code/context-management-offload.md)与[成本分析](analysis/claude-code/context-economics-two-traps.md)：已修正过强推断，产品行为仍有待核实项。
- [综述阅读导航](analysis/surveys/README.md)与[本地核对片段](evidence/domain/reviewed-local-passages.md)：已有局部原文核对，不代表全文复核或实验复现。
- [Memory 框架一手材料](evidence/domain/memory-frameworks-core-2026-09-21.md)与[评估片段核对](evidence/domain/memory-evaluation-passages-2026-09-21.md)：固定版本的文档和局部源码阅读，以及论文比较条件与报告限制。
- [记忆横评对照](analysis/memory-benchmark-crossreview-2026-09.md)：20 个基准的编号与日期经官方接口核验，五份一手横评的具体数字，以及厂商自报分数为何不能互比。
- [记忆分类法](domain/memory-taxonomy/index.md)：第二个主题综合，解释六家分类轴的分歧与三处归属冲突；含[经典分类详解](domain/memory-taxonomy/cognitive-classes.md)（感觉/工作/情景/语义/程序及其映射到 Agent 后的失效处）。
- [论文简介卡片](analysis/paper-digests-2026-09.md)：27 篇入库论文与四个纯源码对象的一句话定位、可引用点、限制，以及过程中未进正文的判断。
- 已完成的[五个记忆系统深拆](deepdive/README.md)：Mem0、memU、EverMemOS、MemoryBear、AML 开源榜前二，均为静态读码，结论区分"代码存在/文档声称/默认启用/未验证"。

目前有初版主题综合与章节提案，尚无完成的对象深拆或成对模型行为实验。主题综合依据已有研究和官方资料形成可修正解释，不能因目录名称被提升成实证定律。候选对象与范围在 [Deepdive 入口](deepdive/README.md#research-map)。

## 项目设计与协作

ARCHITECTURE.md 解释整体设计；[本轮架构研究](analysis/knowledge-architecture-2026-09-20.md) 给出诊断、外部参考与取舍理由。AI 协作入口是 AGENTS.md，按任务读取相关材料，无需每轮遍读假设和历史。

修改文档、表达与成品取舍的规则见 CONVENTIONS.md。

项目已建立 Git 版本历史，后续改动通过提交追溯。[.gitignore](.gitignore) 排除第三方仓库、本地凭据与缓存等；研究正文、论文原件与来源记录正常跟踪。既有 [历史快照](archive/2026-09-20-before-focused-research/SNAPSHOT.md) 保留原用途。
