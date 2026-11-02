> 本文为 AI 译文，由 DeepSeek-V4.1-Flash 于 2026-11-02 生成；源文件：`arxiv-2603.07670.Survey.Autonomous Memory.md`。

---
stem: arxiv-2603.07670.Survey.Autonomous Memory
id: arxiv-2603.07670
keywords: [memory, agent, survey, retrieval]
abstract: "LLM 智能体正越来越多地运行在这样一类场景中：单一 context window 远远不足以容纳已经发生了什么、学到了什么，以及不应重复什么。memory——跨交互持久化、组织并选择性召回信息的能力——正是将无状态的文本生成器转变为真正具有自适应能力的智能体的关键。本综述对现代 LLM 智能体中 memory 的设计、实现与评测给出结构化梳理，覆盖 2022 年至 2026 年初的工作。我们将 agent memory 形式化为一个与感知和行动紧密耦合的\emph{write--manage--read} 循环，随后提出一个横跨 temporal scope、representational substrate 与 control policy 的三维分类体系。我们深入考察五个机制族：context-resident compression、retrieval-augmented memory stores、reflective self-improvement、hierarchical virtual context、policy-learned memory management。在评测方面，我们追溯了从静态召回 benchmark 到将 memory 与决策交织在一起的 multi-session 智能体测试的转变，并分析四个近期 benchmark，它们暴露出当前系统中顽固存在的缺口。我们还综述了 memory 成为差异化因素的应用领域——个人助理、编程智能体、开放世界游戏、科学推理与多智能体协作——并讨论 write path 过滤、矛盾处理、延迟预算与 privacy governance 等工程现实。全文以开放挑战收束：continual consolidation、causally grounded retrieval、trustworthy reflection、learned forgetting，以及多模态具身 memory。"
revised: 2026-03-08
source: "https://arxiv.org/abs/2603.07670"
parser: mineru-cloud 3.4.4
---

# 面向自主 LLM 智能体的 memory：机制、评测与新兴前沿

Pengfei Du<sup>1</sup>

<sup>1</sup> Hong Kong Research Institute of Technology, HongKong, China

E-mail: lldpf1234@gmail.com

## 摘要

LLM 智能体正越来越多地运行在这样一类场景中：单一 context window 远远不足以容纳已经发生了什么、学到了什么，以及不应重复什么。memory——跨交互持久化、组织并选择性召回信息的能力——正是将无状态的文本生成器转变为真正具有自适应能力的智能体的关键。本综述对现代 LLM 智能体中 memory 的设计、实现与评测给出结构化梳理，覆盖 2022 年至 2026 年初的工作。我们将 agent memory 形式化为一个与感知和行动紧密耦合的 write–manage–read 循环，随后提出一个横跨 temporal scope、representational substrate 与 control policy 的三维分类体系。我们深入考察五个机制族：context-resident compression、retrieval-augmented memory stores、reflective self-improvement、hierarchical virtual context、policy-learned memory management。在评测方面，我们追溯了从静态召回 benchmark 到将 memory 与决策交织在一起的 multi-session 智能体测试的转变，并分析四个近期 benchmark，它们暴露出当前系统中顽固存在的缺口。我们还综述了 memory 成为差异化因素的应用领域——个人助理、编程智能体、开放世界游戏、科学推理与多智能体协作——并讨论 write path 过滤、矛盾处理、延迟预算与 privacy governance 等工程现实。全文以开放挑战收束：continual consolidation、causally grounded retrieval、trustworthy reflection、learned forgetting，以及多模态具身 memory。

Keywords: large language model agents; agent memory; long-term memory; retrieval-augmented generation; continual adaptation; agent evaluation

## 1 引言

扩展 LLM 解锁了一类新的自主软件智能体——这类系统感知环境、围绕目标推理、运用工具，并在长时间跨度上采取行动 [Brown et al., 2020, Achiam et al., 2023, Touvron et al., 2023]。把这些智能体与普通聊天机器人区分开来的，不仅仅是更大的模型；而是人们对它们从经验中学习的期待。编程助手应当记住某个特定 API 不稳定，游戏智能体应当记得自己已经掌握了哪些合成配方，个人日程助手则绝不应第二次询问用户的生日。所有这些都要求 memory。

## 1.1 没有 memory 时会出什么问题

设想一个调试助手，它在一周的多轮 session 中处理一个大型代码库。没有 memory，每个周一早晨它都要重新发现目录布局、重读同一份 README，而最糟的是——重试那个在周五让构建崩溃的完全相同修复。给同一个智能体配备哪怕一个很小的 memory module，动态就会转变：它到达时已经知道热点所在，跳过死胡同，并逐渐提炼出项目特定的启发式规则。

这不是边际改进，而是质的变化。memory 把无状态的 LLM 转变为能够（i）积累事实知识与用户偏好、（ii）发展以先前经验为基础的行为模式、（iii）避免重复代价高昂的错误、（iv）通过交互持续改进的自我演化智能体 [Zhang et al., 2024a]。

## 1.2 神经 memory 的简史

为神经网络配备外部存储的雄心可以追溯到十多年前。Memory Networks [Weston et al., 2015] 及其端到端变体 [Sukhbaatar et al., 2015] 为问答任务引入了对外部 memory slots 的可微读写访问。Neural Turing Machines [Graves et al., 2014] 与 Differentiable Neural Computers [Graves et al., 2016] 更进一步，支持在 memory matrix 上进行基于内容与基于位置的寻址。Memorizing Transformers [Wu et al., 2022] 与 Recurrent Memory Transformers [Bulatov et al., 2022] 后来又把显式 memory layers 直接集成进 Transformer 主干。

另一条并行脉络聚焦于 retrieval。Retrieval-augmented generation (RAG) [Lewis et al., 2020] 将预训练生成器与稠密文档 retriever 结合，RETRO [Borgeaud et al., 2022] 则表明，在推理时从万亿 token 语料中取用内容，可以以很小的参数量比肩大得多的模型。这些系统证明了一个关键点：外部知识存储可以在生成过程中被动态查询，而无需重新训练。

从 retrieval-augmented 模型到 memory-augmented 智能体的跃迁发生得很快。ReAct [Yao et al., 2022] 将推理轨迹与环境动作交错起来，产生一条既可解释、又可兼作短程 memory 的轨迹。Reflexion [Shinn et al., 2023] 更进一步，在任务尝试之后存储言语化的自我批评——本质上给了智能体一本事后复盘日志。随后是 Generative Agents 论文 [Park et al., 2023]，其模拟小镇中的 25 个角色表明，一个简单的观察—reflection—规划循环就能产生持续数月、连贯一致的社会行为。自 2023 年以来，设计空间急剧扩张：受操作系统启发的分层虚拟 memory [Packer et al., 2024]、Minecraft 中不断增长的技能库 [Wang et al., 2023a]、作为符号 memory 的 SQL 数据库 [Hu et al., 2023]，以及最近——通过 RL 实现的端到端学习式 memory management [Yu et al., 2026]。

## 1.3 为什么还需要另一篇综述？

已经存在若干宽泛的智能体综述 [Xi et al., 2023, Wang et al., 2024a]，Zhang et al. [Zhang et al., 2024a] 也在 2024 年发表了一篇聚焦 memory 的评论。然而，自那以后研究图景已发生相当大的变化。2025–2026 年的一波工作——Agentic Memory [Yu et al., 2026]、MemBench [Tan et al., 2025]、MemoryAgent-Bench [Hu et al., 2025]、MemoryArena [He et al., 2026]——引入了学习式 memory control、更丰富的评测维度，以及把 memory 与行动紧密耦合的智能体 benchmark。

本综述聚焦于 memory module，并提出三个问题：

RQ1 LLM 智能体中的 memory 应当如何分解与形式化？

RQ2 存在哪些机制，它们施加了怎样的权衡？

RQ3 当最终检验是下游智能体表现时，memory 应当如何评测？

贡献。我们在 POMDP 式智能体循环内把 agent memory 形式化为 write–manage–read 循环（第 2 节），提出一个统一各种异构设计的三维分类体系（第 3 节），提供带有具体系统对比的深入机制评述（第 4 节），综述 benchmark 并给出实用的指标栈（第 5 节），勾勒 memory 成为差异化因素的应用（第 6 节），讨论工程现实与架构模式（第 7 节），定位其与既有综述的关系（第 8 节），并描绘开放研究方向（第 9 节）。

## 2 问题形式化与设计目标

## 2.1 透过 memory 看智能体循环

在每个离散步骤 t，智能体接收输入 x<sub>t</sub>——一条用户消息、一次传感器读数或一个工具返回值——并必须产生一个动作 $a _ { t }$。在这两个事件之间，它查询自己积累的 memory。我们写作：

$$
a _ {t} = \pi_ {\theta} \big (x _ {t}, \mathscr {R} (M _ {t}, x _ {t}), g _ {t} \big),\tag{1}
$$

$$
M _ {t + 1} = \mathcal {U} \big (M _ {t}, x _ {t}, a _ {t}, o _ {t}, r _ {t} \big),\tag{2}
$$

其中 $\pi _ { \theta }$ 是策略（通常是一个经提示、或部分 fine-tuned LLM），$\mathcal { R }$ 从 memory 中读取，$\boldsymbol { \mathcal U }$ 向 memory write 并进行管理，$g _ { t }$ 编码当前目标，$o _ { t }$ 是环境反馈，$r _ { t }$ 是任何类似奖励的信号。

有两点值得强调。第一，$\boldsymbol { \mathcal U }$ 不是简单的追加操作。在一个设计良好的系统中，它会总结、去重、评定优先级、消解矛盾，并在适当的时候删除。第二，$\pi _ { \theta }$ 与 $( \mathcal { R } , \mathcal { U } )$ 构成一个反馈回路：智能体的决策决定写入什么，而写入的内容又塑造未来的决策。正是这种递归依赖，使 memory 既强大又脆弱——一次糟糕的写入可能污染存储，并在下游影响许多步骤。

## 2.2 与 POMDP 的联系

正式地说，上述设置是一个 POMDP。memory $M _ { t }$ 扮演智能体信念状态的角色：一个关于历史的内部摘要，用以代替世界不可观测的真实状态。经典的 POMDP 求解器通过贝叶斯滤波更新信念；LLM 智能体则做着类似——尽管更杂乱——的事情：通过自然语言压缩、向量索引或结构化存储。

这一类比澄清了一个要点：agent memory 不仅仅是数据库查询问题。它关乎在严格的计算与存储预算下，为良好的动作选择维护交互历史的一个充分统计量。

## 2.3 五个设计目标及其张力

在我们综述的系统中，memory mechanism 被五条轴线拉扯：

• Utility——memory 是否真正改善任务结果？

• Efficiency——每获得一单位 Utility，付出多少 token、延迟与存储成本？

• Adaptivity——系统能否从交互反馈中增量更新，而无需完整重训？

• Faithfulness——召回的信息是否准确且及时？陈旧或幻觉式召回可能比完全不召回更糟。

• Governance——系统是否尊重隐私、支持删除请求，并遵守组织政策？

这些目标朝相反方向拉扯。最大化 Utility 会诱使你存储一切，这既膨胀存储，又制造 governance 难题。激进压缩提升效率，却会悄无声息地丢弃那条三周后才发现至关重要的罕见事实。任何真实部署都必须有意识地穿越这些权衡，而「正确」的平衡点随应用而移动。一个医疗分诊智能体，遗漏一条过敏记录可能危及生命，其 Faithfulness–Efficiency 前沿与一个随意的食谱推荐器截然不同。理解这些张力不仅是学术问题——正如我们在后续章节所讨论的，它直接塑造架构选择。

## 2.4 memory as a differentiator：经验视角

memory design 的实际重要性，或许最好由近期系统报告的消融结果来说明。在 Generative Agents 实验 [Park et al., 2023] 中，移除 reflection 组件导致智能体行为在 48 个模拟小时内从连贯的多日规划退化为重复、脱离情境的回应。Voyager [Wang et al., 2023a] 若没有技能库，在科技树里程碑速度上损失 15.3×——技能库就是性能本身。而在 MemoryArena [He et al., 2026] 中，把主动 memory 智能体换成仅 long context 的基线，使相互依赖的 multi-session 任务完成率从 80% 以上降至约 45%。

这些数字凸显了一个反复出现的主题：「有 memory」与「没有 memory」之间的差距，往往大于不同 LLM 主干之间的差距。投资 memory architecture 所能带来的回报，可以媲美——甚至超过——模型规模扩展。

## 3 agent memory 的统一分类体系

认知科学家早已区分人脑中的多种 memory system [Atkinson and Shiffrin, 1968, Tulving, 1972, Baddeley, 2000, Squire, 2004]。智能体设计者——常常无意识地——映射了这种结构。我们沿三个正交维度组织这一空间。

## 3.1 temporal scope

working memory。凡是能装进当前 context window 的内容，都构成智能体的 working memory。Baddeley 的中央执行器加缓冲区模型 [Baddeley, 2000] 可以整齐对应：LLM 是执行器，context window 是缓冲区，二者共享同一个瓶颈——容量有限。

episodic memory。具体经验的记录：单次工具调用、对话轮次、环境观察。在 Generative Agents 世界 [Park et al., 2023] 中，每一次观察——「Isabella 在下午 3 点看到 Klaus 在公园里画画」——都会带着时间戳、重要性分数和供后续 retrieval 使用的 embedding，落入 episodic stream。

semantic memory。抽象化、去情境化的知识。一条 episodic fact，如「用户在 1 月 5 日、1 月 12 日和 2 月 1 日都纠正了日期格式」，可以 consolidate 为语义记录「用户偏好 DD/MM/YYYY」。这种 consolidation 很少自动发生；当前大多数系统需要显式提示或启发式触发。

procedural memory。可复用的技能与可执行计划。Voyager 的技能库 [Wang et al., 2023a] 是最清晰的例子：每一条经过验证的 Minecraft 例程都以可运行的 JavaScript 存储，以自然语言描述建立索引，并为新任务即时组合。

在实践中，大多数智能体至少混合其中两种。困难的问题在于转换策略：episodic record 何时「毕业」为语义状态，语义事实又何时被实例化回 working memory 以服务特定任务？

为说明这种交互，考虑一个处理退货的客服智能体。每一次退货请求都构成一条 episodic record。在处理数百个类似请求之后，智能体可能把模式 consolidate 为一条语义规则：「7 天内收到损坏商品的客户有资格获得快速换货。」当新请求到达时，这条语义规则与当前案例的具体情景细节一起载入 working memory。如果智能体还存储了 procedural memory（处理退货的脚本），四种 memory types 便形成一个完整的推理栈：程序说明如何做，semantic memory 说明政策是什么，episodic memory 说明发生了什么，working memory 则承载实时推理 context。

这种四层整合是理想状态；当前大多数系统只把其中两层实现得较好，并通过粗糙的启发式处理层间转换。consolidation step——episodes 转化为 semantic knowledge 之处——尤其欠缺：它通常需要显式的开发者规则或周期性 LLM 驱动的摘要，而这两者都脆弱且难以验证。

## 3.2 representational substrate

memory 如何物理存储，制约着智能体能高效地对它做什么。

context-resident 的文本——摘要、便签、chain-of-thought 轨迹 [Wei et al., 2022]——是最简单的基底。完全透明、零基础设施，但受容量无情限制。

向量索引存储把记录编码为 dense embeddings，并支持近似最近邻搜索 [Karpukhin et al., 2020, Johnson et al., 2021]。它们能平滑扩展到数百万条记录，却丢失结构化关系：你可以问「什么最相似？」，但无法问「什么导致了什么？」

结构化存储——SQL 数据库 [Hu et al., 2023]、键值映射、知识图谱 [Ji et al., 2022]——保留关系结构并支持复杂查询（「过去 7 天内涉及服务 X 的所有 API 失败」），代价是前期模式设计。

可执行仓库——代码库、工具定义、计划模板 [Wang et al., 2023a]——让智能体直接调用已存储技能，绕开重新生成及其引入的错误。

混合存储在真实生产中是常态。例如，MemGPT [Packer et al., 2024] 在 context window「主 memory」之上，叠加可搜索的召回数据库与向量索引档案库——每一层都有不同的访问模式和驱逐规则。

## 3.3 control policy

或许最具后果——也最少被讨论——的维度是：由谁决定存储什么、retrieve 什么、丢弃什么。

启发式控制硬编码规则：top-k retrieval、每 n 轮摘要、使超过 d 天的记录过期。可预测、易调试，但对情境视而不见。

prompted self-control 把 memory operation 暴露为工具调用，让 LLM 决定何时调用它们。MemGPT 的 core\_memory\_append 与 archival\_memory\_search 是典型例子 [Packer et al., 2024]。这里的质量取决于 LLM 的指令遵循能力，以及 memory API 在 system prompt 中的文档化程度。

学习式控制把 memory operation 视为端到端优化的策略动作。Agentic Memory [Yu et al., 2026] 通过一个带有逐步 GRPO 的三阶段 RL 流程，把 store、retrieve、update、summarize 与 discard 训练为可调用工具。收益可观——学习到的策略会发现非显而易见的战术，例如在 context 填满之前抢先摘要——但训练成本同样可观。

## 3.4 代表性系统一览

表 1 在时间轴上标出关键系统与 benchmark。

## 4 核心 memory mechanism

现在我们详细考察每个机制族，把讨论建立在具体系统设计及其经验权衡之上。

## 4.1 context-resident memory 与压缩

给 agent memory 的最直接方式，是把相关信息留在 prompt 中。系统消息、最近的对话轮次、便签——LLM 在每次调用时「看到」的一切，都作为具有窗口内完美召回能力的 working memory 发挥作用。

麻烦始于历史增长超出窗口。已经出现了若干压缩策略：（i）滑动窗口，保留最近 n 轮并丢弃其余部分；（ii）滚动摘要，周期性把较旧的历史浓缩为更短的摘要；（iii）分层摘要，在轮次、session 与主题粒度上运作；（iv）任务条件压缩，由当前查询决定历史的哪些部分保留完整细节。Self-Controlled Memory 系统 [Liang et al., 2023] 把这一决定交给智能体自身，让它选择哪些片段值得逐字保留、哪些应激进浓缩。

context-resident memory 透明且无需基础设施，但它带有一种众所周知的病理：summarization drift。每一轮压缩都会悄无声息地丢弃低频细节。经过足够多轮之后，智能体「记住」的是经过清洗的、泛化的历史版本——恰恰是那种在边缘案例上失效的 memory。把 context window 扩展到 100k+ token [Chen et al., 2023] 会推迟问题，但无法消除它，而且更长的 context 会带来 attention cost 的二次方增长。

把这个说得具体些：考虑一个每天处理 50 次用户交互的智能体。经过一周的滚动摘要，原本 350 轮的原始历史已经至少经历三个摘要周期。来自第一天的一条罕见但关键的指令——比如「切勿直接调用生产数据库」——也许能挺过第一次压缩，但它恰恰属于那种到第三轮就倾向于消失的低频、高重要性细节。智能体随后便去调用生产数据库，后果可想而知。

这不是假设性的失效模式；它映射了已部署的长时运行聊天机器人与编程助手中报告过的问题。含义很清楚：对于任何预期运行超过少数几个 session 的智能体，context-resident memory 应当被补充——不是被替代，而是被补充——以一个能完整保真地保存原始记录的外部存储。

context-resident memory 一个不那么明显、但同样重要的局限是 attentional dilution。即使在足够大的窗口内，LLM 的 attention mechanism 也必须把容量分配到所有 token 上。随着注入的 memory content 增多，模型聚焦于任何单一片段的能力都会退化——这一现象在 lost in the middle 文献中已有经验记录：放在 long context 中间的信息，比放在开头或结尾的信息更难被可靠召回。这表明，单纯把窗口做大并不是完整解决方案；智能体还必须策展进入窗口的内容，这又把我们带回 retrieval 与过滤机制的根本需求。

## 4.2 retrieval-augmented memory stores

RAG [Lewis et al., 2020] 证明，把生成器与 non-parametric retrieval index 配对，可以在知识密集型任务上产生强劲结果。在智能体场景中，存储中填充的不是百科全书条目，而是活的交互记录：工具调用日志、环境观察、用户纠正、部分计划与言语化 reflection。

indexing granularity。细粒度索引（单次工具调用或单句）提供精确召回，却可能把多步推理切碎成无意义的碎片。粗粒度索引（完整 session 或长段落）保留 context，却让信号淹没在噪声中。实用的最佳位置是多粒度索引，由 retriever 自适应地选择正确分辨率。通过习得编码器实现的 dense passage retrieval [Karpukhin et al., 2020]，通常由 FAISS 式近似最近邻搜索 [Johnson et al., 2021] 支撑，仍是默认实现，并常以稀疏 BM25 与元数据过滤器（时间戳、工具类型、任务标签）加以增强。

query formulation。许多系统一带而过的一个微妙之处是：智能体当下的输入 x 往往是一个糟糕的 retrieval query。用户问「刚才为什么崩溃了？」，需要智能体 retrieve 两个 session 之前的崩溃日志，而不是语义上最相似的那句话。策略包括：由 LLM 重构查询、多查询扇出并融合结果，以及把当前子目标用作额外的 retrieval signal。Self-RAG [Asai et al., 2024] 更进一步，教会模型判断是否根本不值得 retrieval——一个简单的门控，能显著削减不必要的延迟。

Scale。RETRO [Borgeaud et al., 2022] 以及后续关于万亿 token 数据存储的工作 [Raad et al., 2024] 表明，retrieval memory 可以在不做架构改动的情况下扩展到数年的交互历史。瓶颈决定性地从存储转向相关性：确保返回的是最有用——而不仅仅是最相似——的记录。

read-write memory。RET-LLM [Sun et al., 2024] 在自由形式 retrieval 与结构化存储之间架起桥梁：智能体在存储时写入结构化三元组，同时通过自然语言查询它们。这是一种务实的折中：写入时用模式，读取时保持灵活。

表 1：LLM 智能体的代表性 memory system 与 benchmark（2020–2026）。

<table><tr><td>系统</td><td>年份</td><td>memory 类别</td><td>区分性特征</td></tr><tr><td>RAG [Lewis et al., 2020]</td><td>2020</td><td>non-parametric retrieval</td><td>在 NeurIPS 2020 上首次将 seq2seq 生成器与稠密文档 retriever 结合。</td></tr><tr><td>RETRO [Borgeaud et al., 2022]</td><td>2022</td><td>scaled retrieval</td><td>从 2 万亿 token 语料中 retrieve 文本块；7.5B 参数模型在 10/16 个 benchmark 上比肩 175B 的 Jurassic-1。</td></tr><tr><td>ReAct [Yao et al., 2022]</td><td>2022</td><td>trajectory record</td><td>推理与行动轨迹兼作短程 working memory；在 ALFWorld 上获得 34% 绝对提升。</td></tr><tr><td>Reflexion [Shinn et al., 2023]</td><td>2023</td><td>reflective episodic memory</td><td>言语化自我批评存储为 episodic memory；HumanEval 上 pass@1 达 91%（GPT-4 基线为 80%）。</td></tr><tr><td>Generative Agents [Park et al., 2023]</td><td>2023</td><td>episodic + reflective</td><td>25 个模拟角色通过观察—reflection—规划循环自主组织一场情人节派对。</td></tr><tr><td>Voyager [Wang et al., 2023a]</td><td>2023</td><td>procedural skill library</td><td>相比此前的 Minecraft 智能体，独特物品多 3.3×，科技树推进快 15.3×。</td></tr><tr><td>LongMem [Wang et al., 2023b]</td><td>2023</td><td>long-form external memory</td><td>冻结主干 + 残差侧网络；memory bank 可扩展至 65k token。</td></tr><tr><td>ChatDB [Hu et al., 2023]</td><td>2023</td><td>structured symbolic memory</td><td>以 SQL 数据库作为 agent memory；支持对交互记录进行精确的 INSERT/SELECT 查询。</td></tr><tr><td>ExpeL [Zhao et al., 2024]</td><td>2024</td><td>experiential learning</td><td>从轨迹对比中系统性地提取成功/失败「经验法则」。</td></tr><tr><td>MemGPT [Packer et al., 2024]</td><td>2024</td><td>hierarchical virtual memory</td><td>受操作系统启发的分页，跨越主 context、召回数据库与档案向量库。</td></tr><tr><td>MemoryBank [Zhong et al., 2024]</td><td>2024</td><td>long-term memory with forgetting</td><td>将 Ebbinghaus curve decay 应用于聊天机器人 memory；发表于 AAAI 2024。</td></tr><tr><td>LoCoMo [Maharana et al., 2024]</td><td>2024</td><td>benchmark</td><td>最多 35 个 session、300+ 轮、每次对话 9k–16k token；人类仍大幅领先。</td></tr><tr><td>MemBench [Tan et al., 2025]</td><td>2025</td><td>benchmark</td><td>区分 factual memory 与 reflective memory；参与模式与观察模式；ACL 2025 Findings。</td></tr><tr><td>MemoryAgentBench [Hu2025 et al., 2025]</td><td>2025</td><td>benchmark</td><td>测试四项认知能力；当前没有系统能掌握全部四项。</td></tr><tr><td>Agentic Memory [Yu et al., 2026]</td><td>2026</td><td>unified STM/LTM policy</td><td>memory operation 经逐步 GRPO 训练为 RL 动作；在五个 benchmark 上优于所有 memory-augmented 基线。</td></tr><tr><td>MemoryArena [He et al., 2026]</td><td>2026</td><td>benchmark</td><td>四个领域中的 multi-session 相互依赖任务；在 LoCoMo 上接近饱和的模型在此降至 40–60%。</td></tr></table>

## 4.3 reflective and self-improving memory

Reflexion [Shinn et al., 2023] 引入了一个看似简单得具有欺骗性的想法：任务失败之后，让智能体写一份自然语言的事后复盘，再把这份复盘前插到下一次尝试的 prompt 中。没有梯度更新，没有奖励模型——只有一个存满自我批评的文本文件。结果令人瞩目：HumanEval 上 pass@1 达 91%，而未做 reflection 的 GPT-4 为 80%。

Generative Agents [Park et al., 2023] 构建了一条更丰富的流水线。原始观察在 episodic stream 中积累。智能体周期性聚类相关观察，并综合出更高阶的 reflection——例如「Klaus 一直独自吃饭，似乎有些封闭。」retrieval 时，memory 按近因性（指数衰减）、embedding similarity 与重要性（一个自评整数）的加权组合评分。这种多信号评分相比单纯的余弦相似度是实质性改进，并在后续设计中持续产生影响。

ExpeL [Zhao et al., 2024] 通过系统性对比成功与失败轨迹，把这一范式推得更远：它提取具有区分力的「经验法则」，并将其存储为可复用的启发式规则。Think-in-Memory [Liu et al., 2024a] 把 retrieval 与推理分开：智能体先召回，再对召回内容执行一个专门的思考步骤，之后才生成回应。

reflective memory 的核心风险是自我强化错误。如果智能体错误地断定「API X 在使用参数 Y 时总是返回错误」，它就会永远避开那条调用路径，也永远不会收集到推翻这一错误信念的证据。过度泛化是它的姊妹风险：在一个情境中学到的教训被盲目套用到另一个情境。质量门控——置信度分数、与其他 memory 的矛盾检查、周期性过期——是必要的，但仍不成熟。

问题在规模化时更加尖锐。在短生命周期智能体中，一条错误的 reflection 造成的损害有限；同一条错误 reflection 若在长期运行的生产智能体中持续存在——数周内可能影响成千上万次下游决策——则可能是灾难性的。reflective memory failure mode 的严重性随智能体寿命增长，这使它在恰恰最需要 memory 的场景中尤其危险。

近期工作探索的一种缓解策略是 reflection grounding：要求智能体为它生成的每一条 reflection 引用具体的 episodic evidence。如果 reflection「API X 不可靠」必须指向三个具体失败实例，智能体就更不可能生成毫无根据的泛化。这并未完全解决问题——被引用的证据本身可能并不具代表性——但它提供了一条可供人类操作者审查的可审计线索。

## 4.4 hierarchical memory and virtual context management

MemGPT [Packer et al., 2024] 借用了一个操作系统设计者几十年前就已完善的想法：虚拟内存。操作系统通过在 RAM 与磁盘之间透明分页，让每个进程产生拥有巨大连续内存的错觉。MemGPT 为 LLM 的 context window 做同样的事：

• 主 context（RAM）：活动窗口，容纳 system prompt、最近消息与当前相关记录。

• 召回存储（磁盘）：一个可搜索的数据库，保存所有过往消息。

• 档案存储（冷存储）：一个向量索引存储，用于文档与长期知识。

智能体通过调用 memory management「函数」——archival\_memory\_search、core\_memory\_append 等——在各层之间移动数据。中断机制在每条用户消息或定时器事件发生时把控制权交给智能体，让它能在回应之前执行多次内部 memory operation。

JARVIS-1 [Wang et al., 2024b] 把分层原则扩展到多模态场景，为视觉观察、文本计划与可执行技能分别设置存储。Cognitive Architectures for Language Agents [Sumers et al., 2024] 提出一个泛化的蓝图：working memory、episodic memory、semantic memory 与 procedural memory 通过一个中央执行器（即 LLM）交互，直接呼应 Baddeley 的模型 [Baddeley, 2000]。

hierarchical memory 的致命弱点是 orchestration。把错误的东西调入会浪费宝贵的 context token；过度激进地归档则会制造 memory blindness——智能体根本不知道那条关键事实存在于冷存储的某个角落。这一张力促成了下一个机制族。

值得注意的是，hierarchical memory 中的 orchestration 失败往往是无声的。与会产生错误信息的崩溃 API 调用不同，一次驱逐了错误记录的分页决策只是导致回应稍微变差——没有异常、没有日志条目、也没有明显信号表明出了问题。随着时间推移，这些无声失败会累积。诊断它们需要详细的 memory operation 日志与回溯分析——这是一项当前很少有系统愿意投入的工程投资，但对生产级部署至关重要。

## 4.5 policy-learned memory management

启发式规则与 prompted self-control 并未针对智能体的最终任务进行优化。k 近邻 retriever 不知道被 retrieve 的记录是否真的有用；固定的摘要日程也不在乎被压缩的材料是否重要。

Agentic Memory（AgeMem）[Yu et al., 2026] 通过把五种 memory operation——store、retrieve、update、summarize、discard——视为智能体策略内的可调用工具，并用 RL 优化整条流水线来解决这一点。训练分三个阶段进行：在 memory 演示上进行监督式预热，以结果奖励进行任务级 RL，最后用步级 GRPO 为单个 memory 动作提供更稠密的信用分配。在五个长时程 benchmark 上，AgeMem 持续优于强基线，而且学习到的策略会浮现出非显而易见的战术：在 context 填满之前主动摘要中间结果，以及选择性丢弃那些与现有记录语义相似但不增加新信息的记录。

未决的担忧依然存在。长时程上的 RL 训练成本高昂。学习到的 forgetting 可能删除安全关键信息。在某一任务分布上训练的策略可能无法迁移。而且很难解释智能体为何选择某个特定的 memory 动作——可解释性落后于能力。

## 4.6 parametric memory and weight-based adaptation

以上所有机制都把 memory 视为模型权重之外的东西。另一族方法通过 fine-tuning 或适配器模块把 memory 嵌入参数之中。Mem-LLM [Modarressi et al., 2024] fine-tune LLM，使其与一个显式的读写 memory module 交互，从而紧密耦合 parametric 与 non-parametric 知识。retrieval 与生成的联合训练 [Zhong et al., 2022] 比冻结 retriever 的基线产生更好的 memory 利用率。

parametric memory 提供无缝集成——模型就是「知道」事情。但它难以审计（用户的生日究竟存储在权重中的哪个位置？），难以从中删除（machine unlearning 仍不成熟），且更新昂贵（每条新事实都需要 fine-tuning）。由于这些原因，大多数已部署的智能体偏好 non-parametric、可检查的存储。

## 5 评测：从召回到智能体 Utility

## 5.1 为何经典 retrieval metrics 不够用

Precision@k 与 nDCG 告诉你正确的文档是否被 retrieve 到。它们对智能体是否正确使用了该文档——或者 retrieval 是否值得付出延迟——一无所知。agent memory evaluation 必须联合评估 memory quality 与决策质量，并纳入经典信息 retrieval（IR）完全忽略的关切：陈旧性、矛盾、forgetting quality 与 governance 合规。

## 5.2 新的 benchmark 图景

四个近期 benchmark 把评测推向互补的方向。

LoCoMo [Maharana et al., 2024] 测试极长期对话 memory：最多 35 个 session、300+ 轮、每次对话 9k–16k token。三项评测任务——事实问答、事件摘要与对话生成——探查不同的 memory requirements。头条结果是：即便经过 RAG 增强的 LLM 也远远落后于人类，尤其是在时间与因果动态方面。

MemBench [Tan et al., 2025] 区分 factual memory 与 reflective memory，并在参与模式与观察模式下分别测试二者。指标横跨三个维度：有效性（准确率）、Efficiency（memory operation count）与 Capacity（memory store 增长时的性能退化）。

MemoryAgentBench [Hu et al., 2025] 把评测建立在认知科学之上，探查四项能力：准确 retrieval、测试时学习、长程理解与 selective forgetting。long context 数据集被重新格式化为增量式多轮交互，以模拟真实的积累过程。当前没有系统能掌握全部四项能力；大多数在 selective forgetting 上明显失败。

MemoryArena [He et al., 2026] 把 memory evaluation 嵌入完整的智能体任务——网页导航、偏好约束规划、渐进式信息搜索与序列形式推理——其中后续子任务依赖智能体从早先子任务中学到的内容。最引人注目的发现是：在 LoCoMo 上得分接近完美的模型，在 MemoryArena 中骤降至 40–60%，暴露出被动召回与主动、决策相关的 memory 使用之间的深层差距。

## 5.3 benchmark 对比

表 2 总结这四个 benchmark 之间的设计差异。

## 5.4 一套实用的指标栈

部署所需的细微程度超过任何单一 benchmark 所能提供。我们提出一个四层评测栈：

第 1 层——任务有效性：成功率、事实正确性、计划完成率。

第 2 层——memory quality：retrieved records 的精确率/召回率、矛盾率、陈旧性分布、任务相关事实的覆盖率。

第 3 层——效率：每次 memory operation 的延迟、memory content 消耗的 prompt token、每步 retrieval calls 次数、存储随时间的增长。

第 4 层——governance：隐私泄漏率、删除合规性、访问范围违规。

消融研究应分别隔离 write strategy、retrieval strategy 与压缩模块，以便把增益归因于具体组件，而非整条流水线。

## 5.5 来自这些 benchmark 的跨领域教训

汇总这四项评测的结果，若干模式格外突出。

long context 不是 memory。尽管 context window 已扩展到 200k token [Chen et al., 2023]，long context 模型在需要 selective retrieval 与主动管理的任务上，始终不如专门构建的 memory system。MemoryArena 把这一点暴露得最清楚：被动召回的高手是糟糕的 memory 智能体。

RAG 有帮助，但与人类的差距仍然很大。基于 RAG 的智能体全面胜过纯 long context 基线，然而首要瓶颈已不再是存储——而是 retrieval quality。智能体经常捞出看似合理但陈旧或跑题的记录 [Maharana et al., 2024]。

没有人把 forgetting 评测好。只有 MemoryAgent-Bench 显式测试 selective forgetting。然而在任何长期运行的部署中，无法丢弃过时信息会逐渐毒化 retrieval precision。

cross-session 连贯性研究不足。大多数 benchmark 衡量 session 内表现。MemoryArena 的 multi-session 设计揭示：在相隔数小时或数天的 session 之间维持一致的知识与行为，是一项独特——且在很大程度上尚未解决——的挑战。

parametric—non-parametric 差距是真实的。拥有 parametric memory（fine-tuned weights）与 non-parametric memory（外部存储）的系统表现出不同的失效轮廓。parametric memory 擅长无缝知识整合，但在定向删除与审计上失败。non-parametric memory 支持检查与 governance，却可能显得「外挂」——智能体有时忽略 retrieve 到的记录，或前后不一致地使用它们。这两种方法之间的最优平衡，以及如何有效结合它们，仍是一个开放的经验问题。

评测必须包含成本。一个准确率高出 5%、但延迟与存储成本增至三倍的 memory system，在实践中未必是改进。当前没有任何 benchmark 系统性地同时报告效率指标与有效性指标，这使得人们难以评估所报告的增益是「免费」的，还是伴随显著运营开销。未来的评测应强制要求：在准确率数字之外，至少报告 token 消耗与延迟开销。

## 6 memory 在何处成就或击垮智能体

memory 并非均匀地重要。一个一次性翻译工具几乎不需要它；一个为期一个月的项目协作者没有它就无法运作。下面我们考察 memory 成为差异化因素的领域。

## 6.1 个人助理与对话智能体

一个忘记你的饮食限制、或每个 session 都重新询问你时区的个人助理，往好里说也只是烦人。MemoryBank [Zhong et al., 2024] 通过 Ebbinghaus forgetting curve [Ebbinghaus, 1885] 建模 memory decay：频繁访问、高重要性的 memory 得到强化，而被忽视的 memory 逐渐淡出。MemGPT [Packer et al., 2024] 展示了具有演化用户模型的 multi-session 聊天。该领域的核心张力是「个性化而不越界」——智能体必须记住足够多的信息以真正有帮助，又不能呈现用户视为私密或已 forget 的信息。

表 2：近期 agent memory benchmark 的功能对比。

<table><tr><td>benchmark</td><td>年份</td><td>multi-session</td><td>多轮</td><td>智能体任务</td><td>forgetting</td><td>多模态</td></tr><tr><td>LoCoMo</td><td>2024</td><td>√</td><td>√</td><td>-</td><td>-</td><td>√</td></tr><tr><td>MemBench</td><td>2025</td><td>-</td><td>√</td><td>-</td><td>-</td><td>-</td></tr><tr><td>MemoryAgentBench</td><td>2025</td><td>-</td><td>√</td><td>-</td><td>√</td><td>-</td></tr><tr><td>MemoryArena</td><td>2026</td><td>√</td><td>√</td><td>√</td><td>-</td><td>-</td></tr></table>

## 6.2 软件工程智能体

编程智能体在可能包含数百万行的代码库中协助生成、调试、评审与项目管理 [Qian et al., 2024, Hong et al., 2024]。memory requirements 很高：保留架构决策、跟踪缺陷报告历史、记住代码风格偏好，并维护一个经过验证的解决方案库。ChatDev [Qian et al., 2024] 为角色扮演智能体（CEO、CTO、程序员、测试员）配备共享 memory，使项目在开发各阶段保持连贯。MetaGPT [Hong et al., 2024] 把这种共享 memory 结构化为标准化文档——PRD、设计规格、代码模块——这些文档持续存在并演化。

这里独特的挑战是结构性规模：memory system 必须索引并 retrieve 可能横跨数千个文件的代码库中的相关部分，而不仅仅是对话。

## 6.3 开放世界游戏智能体

Minecraft 及类似沙盒之所以成为流行测试平台，恰恰因为它们要求长时程规划与组合式技能复用。Voyager [Wang et al., 2023a] 表明，一个不断增长的技能库能够实现终身学习：相比此前的智能体，独特物品多 3.3×，里程碑推进快 15.3×。JARVIS-1 [Wang et al., 2024b] 以跨越视觉观察与文本计划的多模态 memory 对此加以扩展。Ghost in the Minecraft [Zhu et al., 2023] 使用基于文本的知识与 memory，构建具有通用能力的开放世界智能体。

关键挑战是组合式技能复用：智能体不仅要召回单个技能，还必须创造性地把它们串联起来，以解决新问题。

## 6.4 科学推理与发现

科学智能体必须跟踪假设、记录实验结果、消化文献，并在证据积累时修正信念。这里的 memory 充当假设台账与证据累积器。其独特挑战是不确定性感知 memory：智能体不仅必须维护事实，还必须维护置信水平，并在新数据到达时正确更新它们——这是大多数当前 memory system 处理得很差、或根本不处理的事情。

## 6.5 多智能体协作

当多个智能体共同工作时，memory 成为一种协调机制。AutoGen [Wu et al., 2023] 让智能体通过共享 context 在他人的贡献之上继续构建。CAMEL [Li et al., 2024] 探索角色感知的交流智能体，它们必须记住先前的约定与协作历史。ProAgent [Zhang et al., 2024b] 构建主动型队友，基于对过往交互的 memory 预判需求。

两个挑战占据主导：共享 memory 与私有 memory 的边界——什么应对谁可见？——以及并发写入下的一致性——当两个智能体同时更新共享 memory 时会发生什么？当前多智能体框架以两种方式之一处理共享 memory：要么所有 memory 都共享（简单，但泄漏私有信息），要么每个智能体维护自己的存储、没有跨智能体访问（隔离，但阻止知识迁移）。两种极端都不令人满意。有原则的中间方案会在共享 memory 基底上定义基于角色的访问控制，允许项目经理智能体查看开发者智能体的高层摘要，而不访问原始代码差异。为自然语言记录改造的数据库式访问控制列表，是一种自然但尚未被探索的解决方案。

## 6.6 工具使用与 API orchestration

使用工具的智能体 [Schick et al., 2024] 与 API、数据库和网络服务交互。memory 必须跟踪哪些工具存在、如何调用它们、上次哪些参数有效，以及哪些调用序列已经过验证。AgentBench [Liu et al., 2023] 在八个环境中评测智能体；丢失命令历史记录的智能体在多步任务中表现出急剧的性能下降。DERA [Nair et al., 2023] 使用对话轮次 memory 来迭代改进工具使用策略。

这一场景特有的一个实际风险是 schema drift：当 API 更新接口时，已存储的使用模式会失效。对已存储的工具使用记录进行版本跟踪与模式验证至关重要，却很少被实现。在快速变化的 API 生态系统中，一个不处理 schema drift 的工具使用 memory system 会积累越来越大比例的无效率记录，逐步削弱智能体复用过往经验的能力。

这里更广泛的一点是：工具使用 memory 不仅仅关乎存储「什么曾经有效」；它关乎维护一份活的、带版本的工具能力目录，并随外部世界的变化而优雅降级。这与软件工程中的依赖管理概念相呼应：正如构建系统必须跟踪库版本，使用工具的智能体也必须在 memory store 中跟踪 API 版本。

## 6.7 跨域 memory transfer

一个新兴方向是跨域迁移 memory——例如，把在 Python 中学到的调试启发式复用于 Java，或把一个用户的时间管理策略应用于另一个用户。Tree of Thoughts [Yao et al., 2024] 提供了一个审慎问题求解框架，可能受益于跨域 procedural memory。开放问题是：如何识别哪些 memory 可以泛化，哪些则无可救药地特定于情境。

## 6.8 小结：不同 memory types 各自最要紧之处

应用综述揭示出一个清晰模式：不同领域强调不同的 memory types。个人助理最依赖 semantic memory（用户偏好与画像）。软件工程智能体大量依赖 procedural memory（经过验证的代码模式与架构决策）。游戏智能体需要 episodic memory 与 procedural memory 的紧密整合（发生了什么 + 对此该做什么）。科学智能体需要带有显式不确定性跟踪的 semantic memory。多智能体系统则增加了一个协调层，而当前没有任何单 agent memory design 能很好地处理它。

没有任何现有系统能同时为所有这些画像提供强有力支持，这暗示 agent memory 的下一次跃迁，可能来自更模块化、可插拔的架构：memory components 可按部署组合与配置，而不是被固化在一体化设计之中。

## 7 工程现实

## 7.1 write path

逐字存储每一次交互很诱人，却几乎总是错误的。噪声——闲聊、冗余确认、重复问候——会降低 retrieval precision。设计良好的 write path 包括：过滤以拒绝低信号记录，规范化以统一日期、名称与数量，去重以合并重叠条目，优先级评分以按任务相关性与新颖性排列记录，以及元数据打标（时间戳、来源、任务标签、置信度）以支持下游结构化查询。

最优过滤阈值因应用而异。医疗智能体承受不起漏报（遗漏一次药物过敏提及）；休闲聊天助手则可以容忍漏报。在这两个极端之间是一个谱系：企业客服机器人通常对合同承诺优先保证高召回，但接受对休闲偏好的较低召回；财务顾问智能体则要求对监管披露近乎完美的召回，却可以承受 forget 非正式闲谈。write path 设计应基于风险分析：把 memory failure mode 映射到目标领域中的下游后果。

## 7.2 read path

并非每一步都需要 retrieval，也并非每次 retrieval 都需要完整流水线。实用的 read path 优化包括：two-stage retrieval（快速 BM25 或元数据过滤 → 较慢的交叉编码器重排序器）、是否 retrieve 的门控 [Asai et al., 2024]、在 memory 与当前任务之间动态分配 context space 的 token 预算，以及针对用户偏好等高频记录的缓存层。

## 7.3 陈旧性、矛盾与漂移

一个把生日贺卡寄到用户前伴侣旧地址的个人助理，不只是帮倒忙——它是有害的。长期存活的 memory store 会累积陈旧记录，如果没有显式机制，智能体无法区分 2024 年的地址与 2022 年的地址。

健壮的系统需要时间版本化（偏好最新记录）、来源归因（用户陈述 > 智能体推断）、矛盾检测（标记冲突以供解决），以及 periodic consolidation（定期扫描，合并重复项并退役过时条目）。

## 7.4 延迟与成本

用户期望简单查询在亚秒级得到回应。retrieval pipeline 很容易增加 200–500ms。常见缓解措施包括：异步写入（把存储推迟到回应之后）、progressive retrieval（retrieval 并行运行时就开始生成），以及动态路由（对直接了当的请求跳过 retrieval，只在歧义较高时启用完整流水线）。

Xu et al. [Xu et al., 2024] 表明，把少量高度相关的段落 retrieve 到一个中等长度的 context 中，往往同时胜过纯 long context 与纯 retrieval methods——这是调节延迟—质量权衡的一条有用准则。

## 7.5 隐私、合规与删除

agent memory 可能藏有敏感数据：健康细节、财务记录、私人对话。部署必须提供静态与传输中加密、按用户划分的访问范围、自动化的 PII 脱敏、可配置的保留策略，以及可审计的删除——从每一层移除数据，包括向量索引条目与备份快照。

当 memory 已经渗入 fine-tuned weights 时，外部删除是不够的。machine unlearning [Bourtoule et al., 2021, Liu et al., 2024b] 是唯一的路径，而它仍远未达到生产就绪。agent memory governance 与 machine unlearning 的交叉是一个紧迫的开放问题。

## 7.6 三种架构模式

在实践中，agent memory system 聚成三种反复出现的模式：

模式 A：一体化 context。所有 memory 都活在 prompt 内。零基础设施、完全透明，但容量受限，且易发生 summarization drift。适合短生命周期智能体或快速原型开发。

模式 B：context + retrieval store。working memory 在 context window 内；长期记录在外部向量或结构化存储中。retrieval pipeline 在每一步注入相关记录。这是当今大多数生产智能体背后的主力模式：编程助手、客服机器人、企业副驾驶。工程负担可控；主要挑战是 retrieval quality。

模式 C：带学习式控制的 hierarchical memory。多层——context、结构化数据库、向量存储、冷档案——由 learned 或 prompted controller 管理。MemGPT [Packer et al., 2024] 与 AgeMem [Yu et al., 2026] 是范例。这一模式提供最大的提升空间，但也要求最复杂的工程与训练。

我们的建议：从模式 B 开始，对它进行充分埋点，只有当经验数据表明学习式控制能实质性改善你的目标工作负载时，才升级到模式 C。

## 7.7 可观测性与调试

memory system 以难以调试著称。当智能体给出错误答案时，问题究竟出在 retrieval（浮现了错误记录）、write path（相关信息从未被存储）、压缩（摘要在过程中丢失了细节），还是 LLM 对正确 retrieval 内容的推理？

生产部署受益于全面的 memory operation 日志：每一次写入、读取、更新与删除都应记录时间戳、触发情境与涉及的记录。让开发者用修改后的 memory content 重放失败交互的重放工具，对根因分析极为宝贵。一些团队发现，一个简单的「memory diff」——展示两次对话轮次之间 memory store 发生了什么变化——比传统日志分析提供更大的诊断价值。

这种可观测性基础设施在研究论文中很少被讨论，但它的缺失正是许多令人印象深刻的演示阶段 memory system 无法过渡到可靠生产部署的主要原因之一。

除调试之外，memory observability 还支持持续改进。通过分析 memory operation 中的模式——哪些类型的记录最常被 retrieve、哪些被写入却从未被读取、哪些 retrieval query 持续返回空结果——团队可以识别瓶颈，并随时间校准 memory system。这一反馈回路在数据库工程中是标准做法（查询性能监控、索引优化），但在 agent memory 实践中几乎完全缺席。借用这些技术，即便以简化形式，也会显著提升已部署 memory-augmented 智能体的可靠性。

一个相关关切是 memory behavior 的回归测试。当 memory system 更新时——比如为向量存储部署了一个新的 embedding model——对 retrieval quality 的影响是不可预测的，而且可能很微妙。如果没有一套在代表性场景上验证预期 memory behavior 的回归测试，对 memory subsystem 的改动就会成为未跟踪风险的来源。构建这样的测试套件需要「哪些 memory 应为哪些查询被 retrieve」的 ground truth 标注，这项投资会在系统稳定性上带来回报。

## 8 相对于既有综述的定位

Xi et al. [Xi et al., 2023] 与 Wang et al. [Wang et al., 2024a] 提供了宽泛的智能体综述，其中 memory 只是众多模块之一。Zhang et al. [Zhang et al., 2024a] 专门聚焦 memory，并围绕 write–manage–read 操作组织其评述；我们的工作用 2025–2026 年的系统（AgeMem、MemBench、MemoryAgentBench、MemoryArena）更新了他们的覆盖范围，增加了以 POMDP 为基础的形式化，并把讨论扩展到应用、工程模式与 governance。

Gao et al. [Gao et al., 2024] 全面综述了 RAG，但其范围是 retrieval—生成流水线，而非智能体特有的 memory requirements。Sumers et al. [Sumers et al., 2024] 提出语言智能体的认知架构蓝图；我们的分类体系与之互补，共享认知科学术语，但把分析扩展到 representational substrate 与 control policy。

一个常被提出的问题是：不断扩展的 context window——从早期 GPT 模型的 4k 到今天的 200k+ [Chen et al., 2023]——是否使外部 memory 变得过时。证据表明并非如此。更长的 context 扩大了 working memory，却不提供持久的 cross-session 存储、结构化知识组织、从数月历史中进行 selective retrieval，或删除与访问控制之类的 governance 机制。此外，推理成本随 context 长度呈二次方增长，而 Xu et al. [Xu et al., 2024] 的经验研究表明，在适度 context 上加以 targeted retrieval，在许多任务上胜过蛮力 long context。

## 9 开放挑战

## 9.1 有原则的 consolidation

当前系统在囤积（存储一切，淹没于噪声）与失忆（激进压缩，丢失罕见但至关重要的事实）之间摇摆。神经科学提供了一个有启发性的模型：睡眠期间，海马体重放近期经验，强化重要痕迹并修剪其余部分 [Squire, 2004]。一个类似的「offline consolidation」过程——安排在空闲时段——可以提供有原则的平衡。开放问题包括：如何在没有先见之明的情况下估计 memory importance、如何检测何时需要 consolidation，以及如何保证安全关键记录在这一过程中存活。

一个值得探索的具体方法是 dual-buffer consolidation：新形成的 memory 在考察期内驻留于「热」缓冲区，只有在通过质量检查——再验证、去重与重要性评分——之后才晋升为长期存储。这映射了在生物 memory 中观察到的海马体到新皮层的迁移 [Squire, 2004]：新 memory 最初依赖海马体，并通过反复再激活逐渐独立。在智能体系统中实现这一点，需要定义考察期、晋升标准，以及热缓冲区在晋升发生之前溢出时的回退行为。

## 9.2 causally grounded retrieval

语义相似度回答「什么看起来像这个？」，却不回答「什么导致了这个？」。当智能体调试系统故障时，相关 memory 可能在时间上遥远、在语义上不同于当前错误消息，却在因果上游。融合语义相似度、时间排序、因果图遍历与反事实相关性的混合 retriever，在很大程度上仍未被探索。构建它们需要把因果发现技术与 memory indexing 结合起来——技术上颇具挑战，但对复杂推理任务可能具有变革性。

一个具体的起点是用轻量级因果元数据层增强标准向量索引。存储 memory 记录时，智能体可以用一个估计的因果父节点——促成该记录的较早记录或事件——对其进行标注。retrieval 时，系统在标准相似度搜索之外遍历这些因果链接，浮现语义上遥远但因果相关的记录。这样的系统无需执行完整因果推断；即便是由 LLM 在写入时生成的近似因果标注，也能在根因分析、反事实规划与多步调试等推理密集型任务中实质性改善 retrieval。

## 9.3 trustworthy reflection

self-reflection 是一种强大的适应机制，却也可能固化错误。如果智能体错误地断定「方法 A 总是失败」，它就再也不会测试方法 A——这是典型的确认偏误。未来系统需要外部验证（在 ground truth 可用时对照检查 reflection）、不确定性量化（在没有确证证据时随时间衰减置信度）、对抗式探查（周期性用反例挑战已存储的信念），以及过期策略（在设定时段后退役未经验证的 reflection）。

## 9.4 Learning to forget

forgetting 不是缺陷，而是特性——对健壮性、隐私与效率都必不可少。然而当前系统对它的处理很粗糙：基于时间的硬过期、存储上限驱逐，或者干脆什么都不做。研究问题是在安全与合规约束下，学习能最大化长期 Utility 的 selective forgetting 策略。当 memory 已通过 in-context learning 或 fine-tuning 影响模型行为时，与 machine unlearning [Bourtoule et al., 2021, Liu et al., 2024b] 的联系至关重要。

## 9.5 多模态与具身 memory

随着智能体进入机器人与混合现实领域，memory 必须融合文本、视觉、音频、本体感觉与工具状态。JARVIS-1 [Wang et al., 2024b] 在 Minecraft 中提供了一个早期例子，但真实世界的具身场景增加了空间 memory、实时延迟约束，以及 cross-modal retrieval 这一棘手问题——通过文本查询找到视觉 memory，或反之。

## 9.6 multi-agent memory governance

多智能体系统提出了单 agent memory 从未遇到的问题：共享存储上的访问控制、并发写入的共识协议，以及不同专长智能体之间的知识迁移机制。当前方法依赖共享对话日志或文档存储；更复杂的设计——带合并语义的分布式 memory、带每智能体缓存的分层共享 memory——仍完全开放。

## 9.7 走向 memory 高效的架构

memory-augmented 智能体成本高昂：大 context window、每步多次 retrieval calls、不断增长的存储。sparse retrieval（每步只激活存储的一小部分）、压缩的 session 向量、像 recurrent memory Transformer [Bulatov et al., 2022] 这样的 memory 原生架构，以及通过适配器实现的无 retrieval 注入 [Modarressi et al., 2024]，都指向更便宜的替代方案，尽管尚无一种展示出强劲的智能体级性能。

## 9.8 更深层的神经科学整合

当前 agent memory 借用认知科学标签；更深层的参与可能产生更好的机制。spreading activation [Anderson, 1983]——访问一条 memory 会为其相关 memory 预热——可以改善超越直接相似度的 retrieval。memory reconsolidation 理论——retrieval 使 memory 变得不稳定并可能被修改——可以为更新机制提供启示。Ebbinghaus forgetting curve [Ebbinghaus, 1885] 已在 MemoryBank [Zhong et al., 2024] 中使用，可以结合间隔重复来优化强化时机。

## 9.9 用于 memory management 的 foundation model

一个更长期的愿景：一个 memory control foundation model，在多样化的智能体任务上训练，以通用能力执行写入、retrieval、摘要、forgetting 与 consolidation 操作——正如指令 fine-tuned LLM [Ouyang et al., 2022] 提供通用语言能力。AgeMem [Yu et al., 2026] 通过学习把 memory management 作为策略，迈出了第一步，但一个真正任务无关的 memory controller 的愿景仍未实现。

这样的 foundation model 需要处理多样分布的 memory 挑战：短期对话跟踪、长期用户画像、高频工具使用日志、罕见但安全关键的信息保留，以及存储预算耗尽时的优雅降级。训练数据需求令人生畏——模型需要接触横跨数十个领域的数千条智能体轨迹，并带有 memory operation 质量的 ground truth 标签。合成生成这些训练数据——或许让先进 LLM 回溯性地标注历史轨迹中哪些 memory operation 有帮助、哪些有害——可以为这一过程提供启动数据。

## 9.10 标准化评测

该领域仍缺乏社区统一的 harness。每个 benchmark 都使用自己的数据集、指标与协议，使跨论文比较不可靠。一个 GLUE 式的 agent memory 共享排行榜——横跨对话、智能体与 multi-session 赛道，并采用我们四层指标栈中的标准化指标——将实质性加速进展并减少重复劳动。

## 10 结论

memory 已从边缘附加组件，转变为 LLM 智能体的核心工程与研究挑战。该领域快速连续地走过了三代：prompt 级压缩、retrieval-augmented 的外部存储，以及端到端学习式 memory 策略。评测也同步演进——从静态召回测试，到 multi-session 智能体 benchmark，后者暴露出「记住一条事实」与「真正使用它」之间的差距。

本综述提供了以 POMDP 为基础的形式化、三轴分类体系、对五个机制族的深入剖析、结构化的 benchmark 对比、应用层分析，以及一份实用的工程手册。但最困难的问题仍在前面：如何 consolidate 而不造成灾难性损失，如何按因果而非相似度 retrieve，如何 reflect 而不固化错误，以及如何安全地 forget。解决这些问题，将决定下一代智能体仅仅是令人印象深刻，还是真正可靠。

如果要从本综述中带走一条结论，那就是：memory 值得与 LLM 本身同等水平的工程投资。模型选择会得到数月的仔细 benchmark 测试；memory architecture 却常常只得到一个下午。本文综述的证据表明，翻转这一优先级——把 memory 视为值得专门设计、测试与优化的一等系统组件——可能是当今智能体构建者所能获得的、单一杠杆率最高的干预。

## 致谢

本手稿面向 Advanced Intelligent Systems。作者、资助与伦理元数据应在投稿前最终确定。

## 利益冲突

作者声明无利益冲突。

## 数据可用性声明

本研究未生成任何原始数据。所有被引用的工作均如所引公开可得。

## 参考文献

Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D. Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot learners. Advances in Neural Information Processing Systems (NeurIPS), 2020.

Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. GPT-4 technical report. arXiv preprint arXiv:2303.08774, 2023.

Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, et al. LLaMA: Open and efficient foundation language models. arXiv preprint arXiv:2302.13971, 2023.

Zeyu Zhang, Xiaohe Bo, Chen Ma, Rui Li, Xu Chen, Quanyu Dai, Jieming Zhu, Zhenhua Dong, and Ji-Rong Wen. A survey on the memory mechanism of large language model based agents. arXiv preprint arXiv:2404.13501, 2024a.

Jason Weston, Sumit Chopra, and Antoine Bordes. Memory networks. arXiv preprint arXiv:1410.3916, 2015.

Sainbayar Sukhbaatar, Arthur Szlam, Jason Weston, and Rob Fergus. End-to-end memory networks. Advances in Neural Information Processing Systems (NeurIPS), 2015.

Alex Graves, Greg Wayne, and Ivo Danihelka. Neural turing machines. arXiv preprint arXiv:1410.5401, 2014.

Alex Graves, Greg Wayne, Malcolm Reynolds, Tim Harley, Ivo Danihelka, Agnieszka Grabska-Barwinska,´ Sergio Gómez Colmenarejo, Edward Grefenstette, Tiago Ramalho, John Agapiou, et al. Hybrid computing using a neural network with dynamic external memory. Nature, 538:471–476, 2016.

Yuhuai Wu, Markus N. Rabe, DeLesley Hutchins, and Christian Szegedy. Memorizing transformers. arXiv preprint arXiv:2203.08913, 2022.

Aydar Bulatov, Yuri Kuratov, and Mikhail Burtsev. Recurrent memory transformer. Advances in Neural Information Processing Systems (NeurIPS), 2022.

Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen tau Yih, Tim Rocktäschel, Sebastian Riedel, and Douwe Kiela. Retrieval-augmented generation for knowledge-intensive NLP tasks. In Advances in Neural Information Processing Systems (NeurIPS), 2020.

Sebastian Borgeaud, Arthur Mensch, Jordan Hoffmann, Trevor Cai, Eliza Rutherford, Katie Millican, George van den Driessche, Jean-Baptiste Lespiau, Bogdan Damoc, Aidan Clark, Diego de Las Casas, et al. Improving language models by retrieving from trillions of tokens. In Proceedings of the 39th International Conference on Machine Learning (ICML), 2022.

Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. ReAct: Synergizing reasoning and acting in language models. arXiv preprint arXiv:2210.03629, 2022.

Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflexion: Language agents with verbal reinforcement learning. arXiv preprint arXiv:2303.11366, 2023.

Joon Sung Park, Joseph C. O’Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, and Michael S. Bernstein. Generative agents: Interactive simulacra of human behavior. In Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology (UIST), 2023.

Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, and Joseph E. Gonzalez. MemGPT: Towards LLMs as operating systems. arXiv preprint arXiv:2310.08560, 2024.

Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and Anima Anandkumar. Voyager: An open-ended embodied agent with large language models. arXiv preprint arXiv:2305.16291, 2023a.

Chenxu Hu, Jie Fu, Chenzhuang Du, Simian Luo, Junbo Zhao, and Hang Zhao. ChatDB: Augmenting LLMs with databases as their symbolic memory. arXiv preprint arXiv:2306.03901, 2023.

Yi Yu, Liuyi Yao, Yuexiang Xie, Qingquan Tan, Jiaqi Feng, Yaliang Li, and Libing Wu. Agentic memory: Learning unified long-term and short-term memory management for large language model agents. arXiv preprint arXiv:2601.01885, 2026.

Zhiheng Xi, Wenxiang Chen, Xin Guo, Wei He, Yiwen Ding, Boyang Hong, Ming Zhang, Junzhe Wang, Senjie Jin, Enyu Zhou, et al. The rise and potential of large language model based agents: A survey. arXiv preprint arXiv:2309.07864, 2023.

Lei Wang, Chen Ma, Xueyang Feng, Zeyu Zhang, Hao Yang, Jingsen Zhang, Zhiyuan Chen, Jiakai Tang, Xu Chen, Yankai Lin, Wayne Xin Zhao, Zhewei Wei, and Ji-Rong Wen. A survey on large language model based autonomous agents. Frontiers of Computer Science, 18 (6):186345, 2024a.

Haoran Tan, Zeyu Zhang, Chen Ma, Xu Chen, Quanyu Dai, and Zhenhua Dong. MemBench: Towards more comprehensive evaluation on the memory of LLM-based agents. arXiv preprint arXiv:2506.21605, 2025.

Yuanzhe Hu, Yu Wang, and Julian McAuley. Evaluating memory in LLM agents via incremental multi-turn interactions. arXiv preprint arXiv:2507.05257, 2025.

Zexue He, Yu Wang, Churan Zhi, Yuanzhe Hu, Tzu-Ping Chen, Lang Yin, Ze Chen, Tong Arthur Wu, Siru Ouyang, Zihan Wang, Jiaxin Pei, Julian McAuley, Yejin Choi, and Alex Pentland. MemoryArena: Benchmarking agent memory in interdependent multi-session agentic tasks. arXiv preprint arXiv:2602.16313, 2026.

Richard C. Atkinson and Richard M. Shiffrin. Human memory: A proposed system and its control processes. Psychology ofLearning and Motivation, 2:89–195, 1968.

Endel Tulving. Episodic and semantic memory. Organization ofMemory, pages 381–403, 1972.

Alan Baddeley. The episodic buffer: A new component of working memory? Trends in Cognitive Sciences, 4(11): 417–423, 2000.

Larry R. Squire. Memory systems of the brain: A brief history and current perspective. Neurobiology of Learning and Memory, 82(3):171–177, 2004.

Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc V. Le, and Denny Zhou. Chain-of-thought prompting elicits reasoning in large language models. Advances in Neural Information Processing Systems (NeurIPS), 2022.

Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick˘ Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, and Wen tau Yih. Dense passage retrieval for open-domain question answering. arXiv preprint arXiv:2004.04906, 2020.

Jeff Johnson, Matthijs Douze, and Hervé Jégou. Billionscale similarity search with GPUs. IEEE Transactions on Big Data, 7(3):535–547, 2021.

Shaoxiong Ji, Shirui Pan, Erik Cambria, Pekka Marttinen, and Philip S. Yu. A survey on knowledge graphs: Representation, acquisition, and applications. IEEE Transactions on Neural Networks and Learning Systems, 33(2): 494–514, 2022.

Weizhi Wang, Li Dong, Hao Cheng, Xiaodong Liu, Xifeng Yan, Jianfeng Gao, and Furu Wei. Augmenting language models with long-term memory. In Advances in Neural Information Processing Systems (NeurIPS), 2023b.

Andrew Zhao, Daniel Huang, Quentin Xu, Matthieu Lin, Yong-Jin Liu, and Gao Huang. ExpeL: LLM agents are experiential learners. Proceedings of the AAAI Conference on Artificial Intelligence, 38, 2024.

Wanjun Zhong, Lianghong Guo, Qiqi Gao, He Ye, and Yanlin Wang. MemoryBank: Enhancing large language models with long-term memory. Proceedings of the AAAI Conference on Artificial Intelligence, 38, 2024.

Adyasha Maharana, Dong-Ho Lee, Sergey Tulyakov, Mohit Bansal, Francesco Barbieri, and Yuwei Fang. Evaluating very long-term conversational memory of LLM agents. arXiv preprint arXiv:2402.17753, 2024.

Xinnian Liang, Bing Wang, Hui Huang, Shuangzhi Wu, Peihao Wu, Lu Lu, Zejun Ma, and Zhoujun Li. Unleashing infinite-length input capacity for large-scale language models with self-controlled memory system. arXiv preprint arXiv:2304.13343, 2023.

Shouyuan Chen, Sherman Wong, Liangjian Chen, and Yuandong Tian. Extending context window of large language models via positional interpolation. arXiv preprint arXiv:2306.15595

Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, and Hannaneh Hajishirzi. Self-RAG: Learning to retrieve, generate, and critique through self-reflection. arXiv preprint arXiv:2310.11511, 2024.

Jad Raad, Xian Li, Peter West, and Yejin Choi. Scaling retrieval-based language models with a trillion-token datastore. arXiv preprint arXiv:2407.12854, 2024.

Jianlv Sun, Zihao Shi, Simeng Han, Chuang Gan, and Yilun Du. RET-LLM: Towards a general read-write memory for large language models. arXiv preprint arXiv:2305.14322, 2024.

Lei Liu, Xiaoyan Yang, Yue Shen, Binbin Hu, Zhiqiang Zhang, Jinjie Gu, and Jun Zhou. Think-in-memory: Recalling and post-thinking enable LLMs with long-term memory. arXiv preprint arXiv:2311.08719, 2024a.

Zihao Wang, Shaofei Cai, Anji Liu, Yonggang Jin, Jinbing Hou, Bowei Zhang, Haowei Lin, Zhaofeng He, Zilong Zheng, Yaodong Yang, Xiaojian Ma, and Yitao Liang. JARVIS-1: Open-world multi-task agents with memoryaugmented multimodal language models. arXiv preprint arXiv:2311.05997, 2024b.

Theodore R. Sumers, Shunyu Yao, Karthik Narasimhan, and Thomas L. Griffiths. Cognitive architectures for language agents. Transactions on Machine Learning Research, 2024.

Ali Modarressi, Aber Rizvi, Mehdi Rezagholizadeh, and Pascal Poupart. MemLLM: Finetuning LLMs to use an explicit read-write memory. arXiv preprint arXiv:2404.11672, 2024.

Wanjun Zhong, Lianghong Guo, Qiqi Gao, He Ye, and Yanlin Wang. Training language models with memory augmentation. arXiv preprint arXiv:2205.12674, 2022.

Hermann Ebbinghaus. Über das gedächtnis: Untersuchungen zur experimentellen psychologie. Leipzig: Duncker & Humblot, 1885.

Chen Qian, Xin Cong, Cheng Yang, Weize Chen, Yusheng Su, Juyuan Xu, Zhiyuan Liu, and Maosong Sun. Chat-Dev: Communicative agents for software development. arXiv preprint arXiv:2307.07924, 2024.

Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng Cheng, Ceyao Zhang, Jinlin Wang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, et al. MetaGPT: Meta programming for a multi-agent collaborative framework. arXiv preprint arXiv:2308.00352, 2024.

Xizhou Zhu, Yuntao Chen, Hao Tian, Chenxin Tao, Weijie Su, Chenyu Yang, Gao Huang, Bin Li, Lewei Lu, Xiaogang Wang, Yu Qiao, Zhaoxiang Zhang, and Jifeng Dai. Ghost in the minecraft: Generally capable agents for open-world environments via large language models with text-based knowledge and memory. arXiv preprint arXiv:2305.17144, 2023.

Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun Zhang, Shaokun Zhang, Jiale Liu, et al. AutoGen: Enabling next-gen LLM applications via multi-agent conversation. arXiv preprint arXiv:2308.08155, 2023.

Guohao Li, Hasan Abed Al Kader Hammoud, Hani Itani, Dmitrii Khizbullin, and Bernard Ghanem. CAMEL: Communicative agents for “mind” exploration of large language model society. Advances in Neural Information Processing Systems (NeurIPS), 2024.

Ceyao Zhang, Kaijie Yang, Siyi Du, Xuewei Guo, Yulin Chen, Yao Huang, Haonan Li, Kunlun Zhu, Zhe Zheng, Haoqi Fan, Jiaqi Li, Yu Song, Yiwen Sun, and Sirui Hong. ProAgent: Building proactive cooperative agents with large language models. Proceedings of the AAAI Conference on Artificial Intelligence, 38, 2024b.

Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicola Cancedda, and Thomas Scialom. Toolformer: Language models can teach themselves to use tools. Advances in Neural Information Processing Systems (NeurIPS), 2024.

Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, Hangliang Ding, Kaiwen Men, Kejuan Yang, et al. AgentBench: Evaluating LLMs as agents. arXiv preprint arXiv:2308.03688, 2023.

Varun Nair, Elliot Schumacher, Geoffrey Tso, and Anitha Kannan. DERA: Enhancing large language model completions with dialog-enabled resolving agents. arXiv preprint arXiv:2303.17071, 2023.

Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao, and Karthik Narasimhan. Tree of thoughts: Deliberate problem solving with large language models. Advances in Neural Information Processing Systems (NeurIPS), 2024.

Peng Xu, Wei Ping, Xianchao Wu, Lawrence McAfee, Chen Zhu, Zihan Liu, Sandeep Subramanian, Evelina Bakhturina, Mohammad Shoeybi, and Bryan Catanzaro. Retrieval meets long context large language models. arXiv preprint arXiv:2310.03025, 2024.

Lucas Bourtoule, Varun Chandrasekaran, Christopher A. Choquette-Choo, Henning Brendel, Milad Nasr, Matthew Hoover, Barbara Fung, Dimitris Papadopoulos, Chiyuan Zhang, Adelin Travers, et al. Machine unlearning. IEEE Symposium on Security and Privacy, 2021.

Zheyuan Liu, Guangyao Dou, Zhaoxuan Tan, Yijun Tian, and Meng Jiang. Towards safer large language models through machine unlearning. arXiv preprint arXiv:2402.10058, 2024b.

Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Jinliu Pan, Yuxi Bi, Yi Dai, Jiawei Sun, and Haofen Wang. Retrieval-augmented generation for large language models: A survey. arXiv preprint arXiv:2312.10997, 2024.

John R. Anderson. A spreading activation theory of memory. Journal ofVerbal Learning and Verbal Behavior, 22 (3):261–295, 1983.

Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. Training language models to follow instructions with human feedback. Advances in Neural Information Processing Systems (NeurIPS), 2022.
