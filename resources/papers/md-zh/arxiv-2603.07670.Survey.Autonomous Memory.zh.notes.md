# 译法摘记：arxiv-2603.07670.Survey.Autonomous Memory

## 1 保留英文原形的术语清单

| 英文原形 | 说明 |
| :--- | :--- |
| memory / agent memory / long-term memory / working memory / episodic memory / semantic memory / procedural memory | 一律保留英文；不写「记忆」「智能体记忆」，也不加中文括注。复合词按英文搭配：memory system、memory module、memory operation、memory governance。 |
| token | 全文保留 token；不使用「词元」。 |
| parametric / non-parametric | 保留；不写「参数化 / 非参数化」。 |
| latent | 源文未出现，无对应替换。 |
| context / context window | 保留；long context、in-context learning、context-resident 同。 |
| prompt / system prompt | 保留；prompted self-control 同。 |
| harness | 保留；对应先前「评测框架」，仅 9.10 出现一次。 |
| retrieval / retrieval-augmented / retriever / RAG | 保留；名词用 retrieval，动词用 retrieve。RAG 首次展开为 Retrieval-augmented generation (RAG)。 |
| embedding | 保留；dense embeddings、embedding model、embedding similarity 同。 |
| consolidation | 保留；动词用 consolidate，不写「巩固」。 |
| forgetting | 保留；动词用 forget，不写「遗忘」；machine unlearning 单列。 |
| KV cache / LoRA / distillation | 源文未出现，无对应替换。 |
| attention | 保留；attentional dilution 同。 |
| fine-tuning | 保留；fine-tuned、fine-tune 同。 |
| benchmark | 保留；不写「基准」。 |
| ground truth | 保留；不写「真值」。 |
| session | 保留；multi-session、cross-session 同。 |
| episode / episodic | 保留；episodic memory、episodic stream、episodic record、episodic evidence 同。 |
| temporal scope / representational substrate / control policy | 保留；对应第 3 节三条分类轴。 |
| reflection / governance / schema drift / machine unlearning | 保留；trustworthy reflection、self-reflection、privacy governance 同。 |
| utility / write path / read path / write–manage–read | 保留；Utility 作为设计目标名首字母大写。 |
| memory blindness / summarization drift / attentional dilution / spreading activation / indexing granularity / query formulation / read-write memory / causally grounded retrieval | 保留英文原形，不再附中文译名。 |

例外：仅「嵌入」在两处保留中文，因原句是动词（把 memory 嵌入参数、把 evaluation 嵌入任务），不是 embedding 这一名词术语；见第 3 节。

## 2 信达雅句例

1. 原文：Memory—the ability to persist, organize, and selectively recall information across interactions—is what turns a stateless text generator into a genuinely adaptive agent.
   译文：记忆——跨交互持久化、组织并选择性召回信息的能力——正是将无状态的文本生成器转变为真正具有自适应能力的智能体的关键。
   取舍：保留双破折号插入语；genuinely 译「真正」而非「较为」，不削弱定义句的断言力度。

2. 原文：It is about maintaining a sufficient statistic of the interaction history for good action selection, subject to hard computational and storage budgets.
   译文：它关乎在严格的计算与存储预算下，为良好的动作选择维护交互历史的一个充分统计量。
   取舍：sufficient statistic 是统计学固定术语「充分统计量」；subject to 提前为状语，符合中文语序。

3. 原文：In a well-designed system it summarizes, deduplicates, scores priority, resolves contradictions, and—when appropriate—deletes.
   译文：在一个设计良好的系统中，它会总结、去重、评定优先级、消解矛盾，并在适当的时候删除。
   取舍：五个动词保持并列短促节奏；scores priority 不直译「给优先级打分」，用「评定优先级」。

4. 原文：The hard question is the transition policy: when does an episodic record graduate to semantic status, and when does a semantic fact get instantiated back into working memory for a specific task?
   译文：困难的问题在于转换策略：情景记录何时「毕业」为语义状态，语义事实又何时被实例化回工作记忆以服务特定任务？
   取舍：graduate 的引号保留为「毕业」，因为它在原文中就是机制隐喻；instantiate 用「实例化」而非「具体化」。

5. 原文：After enough passes, the agent "remembers" a sanitized, generic version of history—precisely the kind of memory that fails on edge cases.
   译文：经过足够多轮之后，智能体「记住」的是经过清洗的、泛化的历史版本——恰恰是那种在边缘案例上失效的记忆。
   取舍：sanitized 译「清洗」，保留去掉细节与异常值的处理含义；precisely 用「恰恰」承接判断语气。

6. 原文：Long context is not memory.
   译文：长上下文不是记忆。
   取舍：保留原文短句断言的力度，不扩写为「长上下文并不等同于记忆」。

7. 原文：Nobody evaluates forgetting well.
   译文：没有人把遗忘评测好。
   取舍：保留口语化的绝对判断；若译「遗忘评测尚不完善」，会削弱原文的批评锋芒。

8. 原文：A personal assistant that sends a birthday card to a user's expartner at the old address is not just unhelpful—it is harmful.
   译文：一个把生日贺卡寄到用户前伴侣旧地址的个人助理，不只是帮倒忙——它是有害的。
   取舍：expartner 是源文粘连拼写，按语义拆为「前伴侣」；not just...it is 保留递进结构。

9. 原文：The Achilles' heel of hierarchical memory is orchestration.
   译文：分层记忆的致命弱点是编排（orchestration）。
   取舍：不直译「阿喀琉斯之踵」，避免生活化比喻；保留英文原词，便于与机制名对照。

10. 原文：Forgetting is not a bug; it is a feature—essential for robustness, privacy, and efficiency.
    译文：遗忘不是缺陷，而是特性——对健壮性、隐私与效率都必不可少。
    取舍：bug/feature 用「缺陷/特性」保持对照；补「都」使三项列举在中文里完整。

11. 原文：Model selection gets months of careful benchmarking; memory architecture often gets an afternoon.
    译文：模型选择会得到数月的仔细基准测试；记忆架构却常常只得到一个下午。
    取舍：用「却」显化对比；gets an afternoon 直译，保留原文的讽刺力度，不补「草草了事」。

12. 原文：The evidence reviewed here suggests that flipping this priority—treating memory as a first-class system component worthy of dedicated design, testing, and optimization—may be the single highest-leverage intervention available to agent builders today.
    译文：本文综述的证据表明，翻转这一优先级——把记忆视为值得专门设计、测试与优化的一等系统组件——可能是当今智能体构建者所能获得的、单一杠杆率最高的干预。
    取舍：first-class 译「一等」而非「头等」，保留系统设计语义；highest-leverage 用「杠杆率最高」，贴近原文隐喻且不口语化。

## 3 存疑译法

- L125「表示基底」：substrate 也可译「表示载体」；选「基底」是直译，但与「基质」易混。
- L199「反思接地」、L407「因果接地」：grounding 统一译「接地」，读感偏硬；备选「锚定于证据」「因果锚定」。
- L161「更短的摘要」：precis 有「提要」的体裁感，此处为与全文 summarization 术语统一而牺牲。
- L215「编排」：orchestration 在操作系统与智能体语境均可，但中文「编排」偏工作流，可能弱化「调度分层存储」的含义。
- L353「来源归因」：attribution 在数据治理中常译「溯源」；选「归因」以保留「判断来源可信度」的含义。
- L31「很小的记忆模块」：modest 含「不大但够用」，译「很小」只取了体积义。
- L351「前伴侣」：源文 expartner 为粘连拼写，按语义拆分，非原词形态。
- L445「评测框架」：harness 也可译「测试台」；此处取「框架」，强调协议与指标集合。
- L453「一个下午」：直译时间量，中文读者未必感到夸张；备选「一个下午的功夫」。
