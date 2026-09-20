# Memory 与上下文工程

面向已了解 LLM 与 Agent 的进阶读者，研究 Memory、Context 与 Harness，形成能支持工程判断的主题认识，再制作教材与多视图手册。

**当前先理解具体项目与论文。** 领域结构和教材顺序尚未定型，可以先拆对象，再提出问题；研究必须允许改变早期定义和假设。

## 从任务选择入口

| 想做什么 | 入口 |
|---|---|
| 找外部材料与所用版本 | [Sources](sources/README.md) |
| 拆清一个项目或论文的相关机制 | [Deepdive](deepdive/README.md) |
| 研究概念、解释现象、比较方案或设计检验 | [Analysis](analysis/README.md) |
| 连贯理解一个综合主题 | [Domain](domain/index.md)；已有第一个暂定的整体运行主题 |
| 追溯项目讨论和重要决定 | [Dialogue](dialogue/README.md) |

Deepdive 与 Analysis 在根级并列，分别按对象和问题组织。Domain 形成更大尺度的主题综合，后期 `output/book/`、`output/manual/<视图>/` 直接使用它们及其依据。`output/refs/` 已有教材参考记录；实际成品制作时再展开教材与手册目录。

## 现在实际积累了什么

- [Agent 的持续运行](domain/agent-runtime/index.md)：首个主题综合，把 Harness、Context、Memory、反馈、修正与恢复连成整体；附状态、生命周期和失效定位的深入解释。
- [教材章节设计](analysis/book-design.md)：沿持续任务提出十一章的暂定学习路线，说明概念如何交叉、各章怎样分工。
- [概念与边界草稿](analysis/concepts-and-boundaries.md)：区分 Memory、Context、Harness 及相关观察维度，仍是可修正的研究框架。
- [上下文留存分析](analysis/context-retention.md)：保留、摘要、外部化与组合的条件推演，含逻辑反例和未校准的成本式。
- [问题、假设与检验议程](analysis/research-agenda.md)：候选问题与实验设计，按需使用。
- [Claude Code 策略分析](analysis/claude-code/context-management-offload.md)与[成本分析](analysis/claude-code/context-economics-two-traps.md)：已修正过强推断，产品行为仍有待核实项。
- [综述阅读导航](analysis/surveys/README.md)与[本地核对片段](evidence/domain/reviewed-local-passages.md)：已有局部原文核对，不代表全文复核或实验复现。

目前有初版主题综合与章节提案，尚无完成的对象深拆或成对模型行为实验。主题综合依据已有研究和官方资料形成可修正解释，不能因目录名称被提升成实证定律。候选对象与范围在 [Deepdive 入口](deepdive/README.md#research-map)。

## 项目设计与协作

[ARCHITECTURE.md](ARCHITECTURE.md) 解释整体设计；[本轮架构研究](analysis/knowledge-architecture-2026-09-20.md) 给出诊断、外部参考与取舍理由。AI 协作入口是 [AGENTS.md](AGENTS.md)，按任务读取相关材料，无需每轮遍读假设和历史。

修改文档参考 [CONVENTIONS.md](CONVENTIONS.md)，表达与证据参考 [STYLE.md](STYLE.md)，后期成品的内容选择参考 [TRADEOFFS.md](TRADEOFFS.md)。

项目已建立 Git 版本历史，后续改动通过提交追溯，不再逐轮复制快照。[.gitignore](.gitignore) 排除第三方仓库、本地凭据与缓存等；研究正文、论文原件与来源记录正常跟踪。既有 [历史快照](archive/2026-09-20-before-focused-research/SNAPSHOT.md) 保留原用途。
