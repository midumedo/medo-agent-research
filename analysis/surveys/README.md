# 综述阅读与比较

这里存放**我方的阅读判断**，不是论文原文。现有七篇材料的全文覆盖、实验和版本尚未完成统一复核；以下入口用于选择下一步阅读，不代表已经核实的领域全景。

## 本轮已核对与已撤回

下列三点针对 `2512.13564` 做了局部检查，依据是本地转换正文与元数据，未重新联网确认版本，也未做 PDF 视觉核验：

- 作者数组有 **47** 人，转换文件的作者头部也写 47（作者数现查 arXiv abs 页即可，不再另存元数据快照）。旧导航中的“48 位作者”已更正。
- [正文 §4.2.3 Skill-based Memory](../../sources/papers/md/memory-in-the-age-of-ai-agents.md#423-skill-based-memory) 明确讨论 **Code Snippets、Functions and Scripts、APIs、MCPs**，并在 MCP 段落提到按需加载与降低上下文开销。因此撤回“程序性记忆只在 taxonomy 表里出现”的旧判断。
- 这段原文只足以纠正上述缺席断言；它没有自动证明某个工程方案有效，也不能代替对整篇论文及其余六篇材料的复核。

本次还核对了控制策略、记忆范围、技能外部化与评测协议的局部原文，见 [可引用摘录](../../evidence/domain/reviewed-local-passages.md)。这些文本核对不等于全文评审或实验复现。

旧版导航中的“七篇集体没解决”“全库唯一”“完全没有”等强断言不再作为当前结论。旧稿见 [重建前阅读入口](../../archive/2026-09-20-architecture-review-before/sources/papers/surveys/README.md)。

## 按问题选阅读入口

除已明确标注的局部核对，其余定位沿用初步阅读记录，章节与覆盖程度仍需在使用时核对。

| 想调查的问题 | 可先检查的材料 |
|---|---|
| 不同论文如何划分 memory、RAG 与 context engineering？ | [2512.13564](../../sources/papers/md/memory-in-the-age-of-ai-agents.md) §2.3；比较定义，不预设边界已统一 |
| 技能记忆有哪些表示和执行方式？ | [2512.13564](../../sources/papers/md/memory-in-the-age-of-ai-agents.md#423-skill-based-memory) §4.2.3；再对照 [2602.06052](../../sources/papers/md/a-survey-of-agent-memory-in-the-second-half-towards-self-evolving-and-long-horizon-agents.md) 的 procedural 与 learning policy 部分 |
| 写入、管理和读取能解释哪些机制？ | [2603.07670](../../sources/papers/md/memory-for-autonomous-llm-agents-mechanisms-evaluation-and-emerging-frontiers.md) 的问题形式化与分类；[2505.00675](../../sources/papers/md/rethinking-memory-in-llm-based-agents-representations-operations-and-emerging-topics.md) 的记忆操作 |
| 构建、检索和生成的代价怎样分布？ | [2606.06448](../../sources/papers/md/agent-memory-characterization-and-system-implications-of-stateful-long-horizon-workloads.md) 的 workload、profiling 与实验部分；使用数字前补齐配置与分母 |
| 协议与预算怎样影响系统比较？ | [2607.16848](../../sources/papers/md/beyond-memory-leaderboards-evaluating-scientific-memory-as-budgeted-context-restoration.md)；先核对任务、输入、检索预算与评分方式 |
| 早期分类与当前定义有什么差异？ | [2404.13501](../../sources/papers/md/a-survey-on-the-memory-mechanism-of-large-language-model-based-agents.md)；先确定所读版本，不能只凭初次发布日期推定覆盖范围 |

逐篇阅读提示仅维护在 [nav.json](nav.json)。它保留初步分类与章节线索，把覆盖判断改为待检查问题；不再嵌入来源正文，也不需要为更新导航而重新解析 PDF。

## 待调查的问题

这些是我方的研究问题，不是已经证明的文献空白：

1. 现有材料如何处理 prefix caching、前缀变动、缓存写读价格与总成本？要区分提示缓存与论文讨论的 KV 状态复用。
2. harness 的持久状态、上下文选择、压缩和委托，在现有分类中有什么位置？产品未被点名，不代表机制未被讨论。
3. 常驻内容的容量、有效期与访问频率分别怎样影响选择？现有数值需要核对版本和适用对象。
4. 技能记忆的形成、验证、更新与执行如何连起来？已知存在技能章节，问题应转向其适用条件和未解决约束。
5. 记忆的修订、冲突和回滚分别有哪些方案？没有出现某个产品名，不足以断言没有相关思路。
6. 评测对照如何控制预算、任务和评分偏差？需要具体实验及独立复核，不能用“榜单都不可信”结束调查。

所有外部引用返回 [来源库](../../sources/papers/README.md)。新结论须保留准确原文位置与适用条件；阅读建议不直接晋升为领域事实。
