# Memory 工程比较：两篇本地论文的片段与限制

核对日期：2026-09-21。读取的是本地机器转换文本，未对照 PDF 图表、未复现实验，也未核实原始 arXiv 版本。短引文用于定位作者所述，后面的判断是我方分析。来源记录见 [provenance.json](../../sources/papers/provenance.json)。

## 2606.06448：构建、使用和维护要在同一使用期里考察

来源：[Agent Memory: Characterization and System Implications of Stateful Long-Horizon Workloads](../../sources/papers/md/arxiv-2606.06448.md)。

### 原文支持哪些研究问题

§3.1 说明主要系统刻画使用五份历史，每份约 360K token，每份 60 个问题，总计 300 个问题。检索默认限制为十个 memory entries，但局部模型溢出时改为五条，Letta 另使用 512-token 摄入块；部分系统还调整了提示词、解析格式或工具调用上限。这是具体工作负载和适配条件，不是所有系统开箱行为的完全同预算比较。

§4.2：

> “The per-query latency advantage in Fig. 2 is conditional on memory having already been constructed.”

§4.5：

> “High-volume query workloads against stable histories favor agent memory systems that move work into construction”

这支持把初始构建、持续写入和重复读取放在一起考察；不能把该配置下的构建开销占比推广成所有个人任务的常数。

§4.4 固定 QA 模型为 GPT-4o-mini、embedding 为 text-embedding-3-small，只改变构建 LLM。作者讨论模型无法稳定完成抽取和工具调用时，记忆质量可能在回答之前已经损坏：

> “a model that cannot reliably satisfy these contracts produces a corrupted store”

这支持分别检查构建模型与回答模型的能力，不支持推出一个通用参数量门槛。尤其不能把模型大小、结构化输出适配与记忆机制的影响混成同一个变量。

### 不直接采用的报告内容

- §4.6 正文与图 8 说同步等待暴露构建延迟、异步可能读取尚未完成写入的记忆，但 Insight 6 又将同步和陈旧并列，进而要求异步。该句与前文不一致，本项目采用“等待与新鲜度之间的取舍”这一有限解释，不照抄必须异步的结论。
- §4.2 的 “Energy is invariant” 不能被扩写为能耗对调度和批处理不敏感。可采用的判断只是：把构建放在后台，并不会使构建工作自动消失。
- 表 3 的 MIRIX 为 144,629 J/correct，随后正文却写 197 kJ；BM25 的正文与表格也有小幅差异。在 PDF 与原实验输出核对之前，不引用这些精确数字作为选型依据。
- §4.5 本身限制了 BM25 聚合优势的外推，指出部分任务偏重准确召回和精确匹配。不能将该结果写成复杂 Memory 普遍无用。

## 2607.16848：返回更多材料与采用更好结构不是同一件事

来源：[Beyond Memory Leaderboards: Evaluating Scientific Memory as Budgeted Context Restoration](../../sources/papers/md/arxiv-2607.16848.md)。这篇研究包含作者自己的 Theoria 系统，不能作为独立第三方复现使用。

### 原文支持哪些研究问题

§6.1 表中的平均返回单元大小差异很大，文中实际采用的是**字符预算**，不是已严格统一的 token 预算。§8.2 承认预算控制近似。相同 `top_k` 或返回条数不能自动代表相同实际输入量。

§5 对 Theoria 的范围有明确限制：

> “evaluate only Theoria’s `POST /retrieve` endpoint”

`/theories` 的冷启动和 `/observe` 的迭代更新没有进入测试。静态文献问答可以研究证据恢复，不能由此证明持续任务的更新、经验形成和行为改善。部分系统还使用内部综合，不能笼统声称所有候选具有相同回答模型。

### Graphiti 消融不能支持的因果结论

§6.1 同时改变了返回预算和可用表示：

> “disable episode retrieval ( `include_episodes=false` )”

这使部分比较从完整论文 episode 变成仅图节点与边。作者随后将优势归为 “entirely due to context volume” 或原始 episode，是过强归因：同时移除原文与改变体积，无法区分表示内容和数量的影响。

可采用的较弱结论是：较大的原生返回量不能单独证明图结构的价值；该科学问答配置中的纯图表示可能丢失重要细节。要辨别图的贡献，应在保留原文通道与明确预算的条件下进一步比较，而非据此宣布图方法无效。

### 其他外推边界

作者列出 66／98 题、部分论文覆盖、每配置一次运行、公开材料可能已进入模型训练等限制。三个 PTr hybrid 在 50K 字符配置下的两两差值置信区间均包含零，不适合拿微小分差作确定名次。表 4 的 Graphiti L3 分数也高于 Direct Read，但部分文字称 Direct Read 在 native L3 领先；需要限定比较子集或进一步核对图表，当前不复述该排名。

## 本项目采用什么

采用两篇提出的比较问题：写入是否值得摊销、构建模型是否可靠、检索实际返回多少、保留了什么表示、测试是否覆盖真正要用的能力。相关推理与当前对象选择见 [Memory 工程选择](../../analysis/memory-engineering-selection.md)。

不采用其榜单作为今日产品排序，不把作者报告写成本项目复现，也不因发现局部报告问题而否定全部方法。后续若需要使用具体性能结论，再核对明确版本、PDF 和可复现配置。
