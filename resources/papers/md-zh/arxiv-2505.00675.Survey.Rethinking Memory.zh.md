> 本文为 AI 译文，由 DeepSeek-V4.1-Flash 于 2026-11-02 生成；源文件：`arxiv-2505.00675.Survey.Rethinking Memory.md`。

---
stem: arxiv-2505.00675.Survey.Rethinking Memory
id: arxiv-2505.00675
keywords: [memory, survey, long-term-memory, retrieval]
abstract: "memory 是基于大语言模型（LLM）的 agent 的基础，但现有综述强调应用层面的使用（例如个性化对话），而忽视了支配 memory dynamics 的原子操作。本工作将 memory 分为 parametric（隐式存在于模型权重中）与 contextual（显式外部数据，结构化/非结构化）两种形式，并定义六种核心操作：consolidation、updating、indexing、forgetting、retrieval 与 condensation。将这些维度映射后，可得到四个关键研究主题：long-term memory、long-context、parametric 修改与 multi-source memory。该分类体系为 memory-related 研究、benchmark 与工具提供了结构化视角，阐明了基于 LLM 的 agent 中各功能的相互作用，并为未来进展提供指引。数据集、论文与工具已在 https://github.com/Elvin-Yiming-Du/Survey_Memory_in_AI 公开。"
revised: 2025-12-24
source: "https://arxiv.org/abs/2505.00675"
parser: mineru-cloud 3.4.4
---

# 重思基于 LLM 的 agent 中的 memory：表示、操作与新兴主题

YIMING DU<sup>∗</sup>, The Chinese University of Hong Kong, China and The University of Edinburgh, UK

WENYU HUANG<sup>∗</sup>, The University of Edinburgh, UK

DANNA ZHENG<sup>∗</sup>, The University of Edinburgh, UK

ZHAOWEI WANG, The Hong Kong University of Science and Technology, China

SEBASTIEN MONTELLA, Huawei Technologies Research & Development (UK) Limited, UK

MIRELLA LAPATA, The University of Edinburgh, UK

KAM-FAI WONG, The Chinese University of Hong Kong, China

JEFF Z. PAN, The University of Edinburgh, UK and Huawei Technologies Research & Development (UK) Limited, UK

摘要：memory 是基于大语言模型（Large Language Model, LLM）的 agent 的基础，但现有综述强调应用层面的使用（例如个性化对话），而忽视了支配 memory dynamics 的原子操作。本工作将 memory 分为 parametric（隐式存在于模型权重中）与 contextual（显式外部数据，结构化/非结构化）两种形式，并定义六种核心操作：consolidation、updating、indexing、forgetting、retrieval 与 condensation。将这些维度映射后，可得到四个关键研究主题：long-term memory、long-context、parametric 修改与 multi-source memory。该分类体系为 memory-related 研究、benchmark 与工具提供了结构化视角，阐明了基于 LLM 的 agent 中各功能的相互作用，并为未来进展提供指引。数据集、论文与工具已在 https://github.com/Elvin-Yiming-Du/Survey\_Memory\_in\_AI 公开。

## 1 引言

memory 是基于大语言模型（LLM）的 agent 的核心组件 [301]，也是迈向通用人工智能（AGI）的关键一步 [228]，它支撑持久交互 [196, 375]、推理 [78]、多模态理解 [189]、个性化 [153] 以及多 agent 协作 [298]。尽管近期研究探索了 memory sources [65, 207]、操作 [23, 281, 350, 375] 与应用 [97, 189, 202, 255]，但仍然缺乏一个用于组织和演进 agent memory 的统一而系统化的框架。

现有的 agent memory 综述采用基于类型与受认知科学启发的视角，提供了有价值的概览，但缺少统一的、可操作的形式化；多数综述聚焦于子主题，例如 long-context 建模 [108]、long-term memory [94, 126]、个性化 [177] 或 knowledge editing [297]，而未统一核心操作。Zhang 等 [367] 仅涵盖写作、管理、阅读等高层操作，遗漏了 indexing 等操作。更广泛地说，很少有综述界定 memory research 的范围、分析技术实现，或提供 benchmark 与工具等实践基础。

为填补这些空白，我们将 memory 分为 parametric 与 contextual 两类。parametric memory 将知识隐式编码于模型参数中 [289]，而 contextual memory 存储显式外部信息，或为结构化（例如图、表、轨迹 [239]），或为非结构化（例如文本 [375]、向量、音频、视频 [189]）。在时间维度上，memory 既跨越长期（例如多轮对话、外部观察 [153]），也跨越短期 context（例如 KV cache、当前对话历史 [226]）。基于这些类型，我们定义六种 memory operations，并进一步将其归入三类：memory encoding、memory evolving 与 memory adapting。memory encoding 包含 consolidation（将新知识纳入持久 memory [73]）与 indexing（为 retrieval 而组织 memory [314]）。

memory evolution 包含 updating（修改既有 memory 以纳入近期更新 [32]）与 forgetting（移除过时或错误的内容 [277]）。memory adaptation 涵盖 retrieval（访问相关 memory [84]）与 condensation（在保留关键信息的同时缩减规模 [32]）。

除这一结构分类体系外，memory 的功能视角为理解 LLM 系统提供了互补的透镜。episodic memory 根植于认知心理学 [279]，存储以时间为锚点的经验——例如对话历史与事件序列——并支撑动态环境中的推理与适配 [74, 207]。semantic memory 编码结构化、可泛化的知识，通常形式化为可查询的 knowledge graph 或表，补充 parametric memory 以增强推理与 retrieval-augmented generation（RAG）。procedural memory 捕获任务执行模式与习得轨迹，通常通过大规模训练或结合 chain-of-thought 数据的强化学习形成，并驱动任务导向 agent 中高效的工具使用与问题求解。working memory 作为一种动态控制机制，整合短期缓存与已激活的长期知识，支撑实时推理、规划与决策。这些功能类型凸显了 memory 在支撑 LLM 能力时所扮演的多样角色，并为我们提出的操作框架提供依据。

为给操作框架提供实证基础，我们开展了一项先导研究，并定义四个核心主题。这些主题覆盖 memory research 的互补维度，代表了发展能力强的 AI agent 的关键前沿：

• long-term memory（时间维度）：聚焦 multi-session 对话系统 [196, 327]、RAG、个性化 agent [153] 与问答 [314, 375] 中的 memory management、利用与个性化。

• long-context memory（context 维度）：在处理扩展序列时，同时关注 parametric 效率（例如「KV cache eviction」[368]）与 context 利用有效性（例如 long-context compression [36, 125]）。

• parametric memory modification（模型内部维度）：涵盖 model editing [70, 204, 289]、machine unlearning [197] 与 continual learning [301]，以适配内部知识表示。

• multi-source memory（跨来源维度）：强调跨异构文本来源的整合 [102]，同时也包括多模态输入 [281]，以进一步支撑鲁棒且具备场景感知的推理。

## 1.1 研究方法

为提供系统且全面的 memory research 图景，我们首先分析了 37 篇被广泛认为构成 memory—LLM 文献基础或具有代表性的种子论文。通过专家标注与迭代讨论，这些论文被用于界定我们的 memory types 与核心操作分类体系，并人工识别四个主要研究主题：long-term memory、long-context memory、parametric memory modification 与 multi-source memory。之所以选择这些主题，是因为它们 1）代表了以 memory 为中心的 LLM 系统中最密切相关且研究最活跃的领域，2）反映了四个互补维度上的不同操作挑战，包括时间维度（例如长期使用中的持久性与个性化）、context 维度（例如长序列的高效处理与 compression）、模型内部维度（例如更新或编辑 parametric 表示中的知识）以及模态与 integration 维度（例如跨异构或多模态来源的对齐与推理），并共同覆盖了从对话 agent 到 retrieval-augmented 推理系统的最新发展广度。

在此框架基础上，我们收集了 2022 至 2025 年间发表于 NeurIPS、ICLR、ICML、ACL、EMNLP 与 NAACL 等顶级 NLP 与 ML 会议的大规模语料，超过 30,000 篇论文；这一时期以大型语言模型的快速涌现与演进为标志。每篇论文摘要均通过基于 GPT 的相关性评分流水线评估。兼顾成本与有效性，我们选择 GPT-4o-mini，因其具备较强的零样本推理能力与效率。按照与分类体系对齐的任务定义，得分 ≥ 8（满分 10）的论文被保留，最终得到 3,923 篇高相关论文的精选集合。为确保可靠性，我们对随机抽样子集进行了人工验证与召回检查，确认阈值 8 在精确率与召回率之间取得了平衡。

为凸显有影响力的工作并缓解发表年份偏差，我们引入相对引用指数（Relative Citation Index, RCI），这是一种基于双对数回归、按时间归一化的指标，改编自 RCR 框架 [110]。RCI 依据发表年龄调整原始引用数，使跨论文与跨年份的比较更为公平。实证结果显示，双对数回归模型取得最佳拟合 $\left( R ^ { 2 } = 0 . 9 7 \right)$，并产生直观结果：新近发表论文的期望引用数收敛于零。通过结合语义相关性过滤与基于 RCI 的影响力评估，我们为分析四个核心领域的研究进展、趋势与主题特定的影响力动态，建立了平衡且可复现的基础。

## 1.2 贡献与结构

本综述通过提供关于 AI agent memory 的全面且结构化的视角，同时服务于研究界与工业界。对研究界而言，我们的综述建立了全面的概念基础：不仅系统化地组织 memory representation、类型与核心操作，还以 memory 生命周期为透镜来框定前沿主题，阐明 memory 在 AI agent 中如何被编码、演进与适配。对工业界而言，它提供了关于工具、产品与 benchmark 的广泛概览，并分析其功能与部署场景。因此，本综述可作为设计与实现具备 memory capabilities 的应用的实践参考。此外，本综述综合了新兴趋势与突出挑战，勾勒出这一快速演进领域中未来研究与开发的有前景路径。

本文其余部分组织如下。第 2 节帮助读者全面理解 memory representation、memory types、功能性 memory 类别与核心 memory operations，为研究 agent 中的 memory 奠定坚实基础。第 3 节将高影响力主题映射到该基础，并总结关键方法与数据集。第 4 节概述用于构建具备 memory capabilities 的 AI 系统的真实应用、产品与实践工具。第 5 节比较人类与 agent memory 系统，突出操作层面的相似与差异。第 6 节以以 memory 为中心的 agent 的未来方向作结（总体概览见图 1）。

## 2 memory 基础

agent 中的 memory 可通过四个互补维度理解：表示、时间尺度、功能类型与操作。这些视角共同描述 memory 是什么、持续多久、承担何种角色以及如何演进。表示界定所存知识的结构形式，时间尺度刻画其时间持久性，功能类型捕获所存内容的认知或计算角色，操作则描述支配编码、演进与适配的动态过程。它们共同提供了一个整合框架，将人类认知与人工智能中 memory 的结构、功能与动态联系起来。这些维度共同构成分析 agent memory 机制的核心维度。

![](../assets/arxiv-2505.00675-fig1.jpg) 
图 1. memory 的统一框架：基于 LLM 的 agent 中的分类体系、核心操作与应用。

## 2.1 memory representation

从 memory representation 的角度，我们将 memory 划分为 parametric memory 与 contextual memory，其中后者包含非结构化与结构化两种形式。

parametric memory 指隐式存储于模型内部参数中的知识 [21, 233, 289]。它在预训练或后训练期间获得，嵌入模型权重中，并在推理时通过前馈计算访问。它作为一种长期且持久的 memory，使事实性与常识性知识能够快速、无需 context 地 retrieval。然而，它缺乏透明性，且难以针对新经验或任务特定 context 进行选择性更新。

contextual memory 指显式外部信息，用于补充模型参数，并分为非结构化与结构化形式。contextual unstructured memory 指一种显式且动态演进的 memory system，以非结构化格式存储、检索并更新情境信息，例如文本 [375]、图像 [281]、音频 [189]、视频 [305, 352] 或 embedding，来源于用户、系统与环境。它无需预定义模式即可捕获 context 的时间 [78]、情感 [340]、procedural [71] 与 semantic 方面，从而实现跨交互的自适应推理与连续性。contextual unstructured memory 的短期形式包括拼接的 prompt 与 key-value（KV）cache [336]，后者在推理期间保留 token 级表示，以维持局部连贯性并高效复用 context。相比之下，其长期形式扩展至 memory 缓冲 [226]、retrieval 数据库 [295] 或 episodic 存储 [103]，随时间存储并精炼 context 信号，以支撑个性化与终身学习 [153]。同时，contextual structured memory 指以预定义、可解释格式或模式组织的显式 memory，例如 knowledge graph [221, 308]、关系表 [190]、经验 [225] 或本体 [235]，其始终保持易查询性。这些结构支撑符号推理与精确查询，通常补充预训练语言模型（pre-trained language model, PLM）的联想能力。结构化 memory 虽通常用作 long-term memory，也可作为 short-term memory：在推理时构建以支持局部推理，或作为 long-term memory 在 session 间存储精炼知识。

## 2.2 memory 时间尺度

除表示之外，时间尺度是另一个关键维度。依据信息的时间持久性，memory 通常分为 long-term memory 与 short-term memory。

long-term memory 指一种容量几乎不受限的认知系统，可在从数小时到整个生命周期的延长时间段内存储信息 [261]。在 LLM agent 中，它指在与扩展环境进行长期交互的过程中持久地存储、管理与利用信息的能力。这一能力对于 multi-session agent [78]、RAG [234]、个性化助手 [65, 375] 与长期规划 agent [329] 等真实应用中的连续性、个性化与 knowledge grounding 至关重要。它既包含 contextual memory（例如对话历史 [103] 与用户特定偏好 [202, 358]），也包含 parametric memory（编码于模型参数中的知识 [23]）。同时，它与功能视角密切相关，包括 semantic [295]、episodic [183, 307]、procedural [71] memory，这些将在后续章节介绍。

short-term memory 指为即时使用而临时存储信息 [192]。在基于 LLM 的 agent 中，它通常指 KV cache [336] 或当前 context window [226]，保存任务相关信息以支撑实时推理与决策。与人类认知类似，这种 short-term memory 可通过摘要 [190] 以及存储到外部数据库或模型参数等过程整合为 long-term memory。在实践中，short-term memory 在 long-context 场景中尤为关键，有助于缓解幻觉、应对超长 context 中的「中间迷失（lost in the middle）」问题 [180][350]、减少多轮交互中的误差累积 [381]，并提升多轮工具使用的可靠性 [192]。

## 2.3 memory 功能类型

除时间持久性外，memory 还可依据其在支撑 agentic 智能中的功能角色来刻画。借鉴认知科学，我们进一步将 memory 区分为 episodic memory、semantic memory、procedural memory 与 working memory。

episodic memory 是源自认知心理学的核心 long-term memory 类型 [279]，指存储与时间线索、事件、对话历史及空间 context 相关联的过往经验，并随环境变化动态演进。它被广泛视为一种 long-term memory [74]，在现代 agent 系统中常作为外部 memory module [232]，补充 parametric 知识。近期 agent 研究 [207] 日益探索如何更新 episodic memory [47, 155]、执行时间推理 [78]，以及检索并利用相关经验 [207]，以增强动态环境中的适应性与决策 [333]。

semantic memory 是另一种基本 long-term memory 形式，指关于世界的事实与概念的 memory [279]。在计算系统中，它常被形式化为显式、可查询的结构，例如 knowledge graph [239]、关系表 [102] 或隐式模型参数 [226]。在模型参数内，语义知识以分布式表示编码，捕获预训练期间学到的一般世界事实与概念。与依赖 context 的 episodic memory 不同，semantic memory 相对稳定、可泛化，并从累积经验中抽象而来。在 LLM 中，semantic memory 与 episodic memory 的边界常常模糊，parametric 表示可能将事实知识与 context 联想交织在一起。这种隐式与显式 semantic memory 的 integration，为现代 agent 中的 memory-augmented 推理与自适应知识使用提供了基础 [381]。

procedural memory 同样被归类为 long-term memory 的一种形式，指支撑习得技能与动作序列执行的 memory，且无需对先前经验有意识觉察 [71, 225, 377]。在 agent 中，procedural memory 通常以两种方式形成：显式存储于外部技能库以供复用 [377]，或通过大规模训练隐式编码 [171]。在轨迹与 CoT 推理等执行数据上训练，可促成稳定的任务表现，尤其在工具增强 [192] 与基于 RL 的系统 [350] 中。procedural memory 支撑任务导向行为的自动化与泛化。

working memory 是 short-term memory 的功能性延伸，作为一种动态控制机制运行，不仅临时存储信息，还主动操纵并更新信息以支撑进行中的认知 [239, 294]。其主要功能是主动选择并整合来自多样来源的信息，例如短期 context（如对话历史）、已激活的 long-term memory（如检索到的知识或 parametric 输出）以及 KV cache [31, 255] 等瞬态计算缓冲。在实践中，working memory 充当 agent context window 的控制层 [168]，动态组装必要输入，包括检索到的推理经验 [225]、工具输出 [192] 与用户数据 [281]，以支撑复杂推理、规划与目标导向行为。

## 2.4 memory operations

为使 memory 超越静态存储而具备动态性，现代 agent 需要支配信息生命周期、并支撑其在与外部环境交互期间有效使用的操作。这些操作可分为三个功能类别：memory encoding、memory evolving 与 memory adapting。

2.4.1 memory encoding。memory encoding 支配信息如何转化为可存储表示并为后续 retrieval 建立链接。它主要涉及两个互补过程：consolidation 与 indexing。这些操作自然纳入了 memory 的时间属性，即信息随时间演进。

consolidation [258] 指将 $t$ 到 $t + \Delta_{t}$ 之间的短期经验 $\mathcal { E } [ t , t + \Delta t ] = ( \epsilon _ { 1 } , \epsilon _ { 2 } , . . . , \epsilon _ { m } )$ 转化为持久 memory $\mathcal { M } _ { t + \Delta_ { t } }$。它将交互历史（例如对话、轨迹）编码为持久形式，例如模型参数 [301]、图 [372] 或知识库 [190]。它对于 continual learning [73]、个性化 [358]、外部 memory 库（Memory Bank）构建 [375] 与 knowledge graph 构建 [331] 至关重要。

$$
\mathcal {M} _ {t + \Delta_ {t}} = \mathrm{Consolidate} (\mathcal {M} _ {t}, \mathcal {E} _ {[ t, t + \Delta_ {t} ]})\tag{1}
$$

indexing [195] 构造辅助编码 $\phi$，例如实体、属性或基于内容的表示 [314]，作为访问已存 memory 的入口。除访问之外，indexing 还编码 memory 之间的时间 [196] 与关系结构 [200]，通过可遍历的 indexing 路径实现高效且连贯的 retrieval。它进一步支撑跨符号、神经与混合 memory system 的可扩展 retrieval。

$$
\mathcal {I} _ {t} = \operatorname{Index} (\mathcal {M} _ {t}, \phi)\tag{2}
$$

2.4.2 memory evolution。memory evolution 描述已存信息如何通过两个互补过程随时间动态变化：memory updating 与 memory forgetting。

updating [136] 重新激活 $\boldsymbol { \mathcal { M } } _ { t }$ 中的既有 memory representation，并用新知识 $\mathcal { K } _ { t + \Delta _ { t } }$ 临时修改它们。updating parametric memory 通常涉及定位—编辑（locate-and-edit）机制 [70]，以特定模型组件为目标。同时，contextual memory 更新涉及摘要 [375]、剪枝或精炼 [13]，以重组或替换过时内容。这些更新操作支撑持续适配，同时维持 memory consistency。

$$
\mathcal {M} _ {t + \Delta_ {t}} = \mathrm{Update} (\mathcal {M} _ {t}, \mathcal {K} _ {t + \Delta_ {t}})\tag{3}
$$

forgetting [49, 285] 指从 $\mathcal { M } _ { t }$ 中选择性抑制可能过时、无关或有害的 memory content $\mathcal { F }$ 的能力。在 parametric memory 中，它通常通过 machine unlearning 技术 [119, 157] 实现，即修改模型参数以抹除特定知识。在 contextual memory 中，forgetting 涉及基于时间的删除 [375] 或语义过滤 [296]，以丢弃不再相关的内容。这些操作有助于维持 memory 效率并减少干扰。

$$
\mathcal {M} _ {t + \Delta_ {t}} = \operatorname{Forget} (\mathcal {M} _ {t}, \mathcal {F})\tag{4}
$$

然而，这些操作也带来固有风险与局限。攻击者可利用漏洞篡改或投毒 memory content。memory 片段一旦被污染，可能未被察觉地持续存在，并在之后触发恶意行为。正如第 6 节所讨论，此类威胁要求采用鲁棒方法，不仅处理 memory operations，还要覆盖整个 memory 生命周期。

2.4.3 memory adaptation。memory adaptation 指在推理期间如何检索并使用已存 memory，包含两种操作：retrieval 与 compression。

retrieval 是响应输入、从 memory 中识别并访问相关信息的过程，旨在支撑响应生成、视觉定位或意图预测等下游任务。输入 Q 可以是简单查询 [65]，也可以是复杂的多轮对话 context [281]；可以是纯文本输入，也可以是视觉内容 [378] 乃至更多模态。memory 片段通常用函数 sim() 评分，高于阈值 $\tau$ 者被视为相关。retrieval 目标包括来自多来源 [268]、多模态 [281]，乃至模型内部 parametric 表示 [193] 的 memory。

$$
\begin{array}{c} \text { Retrieve } (\mathcal {M} _ {t}, Q) = m _ {Q} \in \mathcal {M} _ {t} \\ \text { with } \text { sim } (Q, m _ {Q}) \geq \tau \end{array}\tag{5}
$$

condensation 通过在输入模型之前保留显著信息、丢弃冗余内容（compression 比为 $\alpha$），在有限 context window 下实现高效 context 使用。它可大致分为输入前 compression 与 retrieval 后 compression。输入前 compression 适用于无 retrieval 的 long-context 模型，此时对完整 context 输入进行评分、过滤或摘要，以满足 context 约束 [41, 351]。retrieval 后 compression 在 memory 访问之后运行，可通过模型推理前的 context compression [325]，或通过将检索知识整合进模型参数的 parametric compression [244]，来缩减 retrieval 内容。与在 memory 构建期间摘要信息的 memory consolidation [375] 不同，compression 聚焦于在推理时缩减 memory [149]。

$$
\mathcal {M} _ {t} ^ {c o m p} = \operatorname{Compress} (\mathcal {M} _ {t}, \alpha)\tag{6}
$$

## 3 从操作到关键研究主题

本节分析真实系统如何通过核心操作管理与利用 memory。我们依据图 1 的框架，考察第 1 节引入的四个关键研究主题，并使用相对引用指数（RCI）——一种按发表年龄归一化引用数、以突出有影响力工作的时间调整指标。

![](../assets/arxiv-2505.00675-fig2.jpg) 
图 2. AI agent 中操作驱动的关键研究主题，将核心 memory operations 映射到四个关键研究主题。

RCI 揭示 memory research 中的新兴趋势与持久贡献。图 2 展示了这些主题的架构图景。

## 3.1 long-term memory

long-term memory 作为一个研究主题，考察 agent 如何在长期交互中保存并利用信息，以实现连续性、个性化与累积学习。本节将 contextual long-term memory 讨论为一种整合结构化与非结构化形式的功能系统，突出其在支撑复杂推理与时间连贯性方面的核心操作：memory encoding、memory evolving 与 memory adapting。

3.1.1 memory encoding。memory encoding 是将原始输入——例如对话历史或 agent 观察——转化为适合长期存储的持久表示的基础过程。这一过程通过两个关键且互补的操作实现：memory consolidation 与 memory indexing。

memory consolidation 通过将短期 context 稳定为持久表示，在塑造 long-term memory 中发挥核心作用。在基于 LLM 的 agent 中，consolidation 在多个层级展开：（1）对话摘要或结构化将交互历史转化为可供检索的痕迹 [100, 190, 293, 375]；（2）推理经验 consolidation 编码成功的工具使用轨迹与问题求解策略 [71, 225]；（3）parametric consolidation 通过持续预训练 [126]、supervised fine-tuning [39] 或强化学习 [303, 333] 等方法，将稳定知识直接嵌入模型参数；（4）事件级 consolidation 将 episodic 信息组织为结构化事件图 [372]；（5）知识级 consolidation 用事实三元组填充 knowledge graph，以支持符号推理 [239]。这些过程共同扩展 agent 的时间 memory 视界，使 contextual、episodic 与 semantic memory 能够在与外部环境的长期交互中持久保留。然而，鲁棒的长期 consolidation 仍然具有挑战性——需要在稳定性与可适应性之间取得平衡，缓解过度 compression 导致的 context 丢失，并在持续更新下保持相关性 [361]。这凸显了在复杂、演进中的 memory system 内采用动态 consolidation 策略的迫切需求。

memory indexing 为 long-term memory 提供基础结构，将大量经验集合转化为可搜索仓库，从而实现高效且准确的 retrieval。近期工作将 memory indexing 归为三种范式：以 HippoRAG [84] 为代表的图式 indexing，构建轻量 knowledge graph 以显式映射 memory 片段之间的关系结构；信号增强 indexing，如 LongMemEval [314] 等系统用时间戳或摘要等元数据丰富 memory 键，以提升 retrieval 准确性；以及时间线式 indexing，如 Theanine [222] 所示，沿时间与因果链组织 memory，以实现基于时间顺序的 retrieval。这些策略凸显了整合结构、retrieval 信号与时间动态对于有效 long-term memory 管理的必要性。这些范式标志着从简单语义相似度向关系结构、元数据信号与时间动态的关键综合转变，使可扩展且具备 context-aware 的 memory system 得以发展。

3.1.2 memory evolution。memory evolution 涉及 forgetting 与 updating 等操作。在此，memory 通过纳入新知识、纠正过时或错误内容、选择性移除低价值信息而被动态精炼。这些过程确保 memory 保持准确、高效且与 context 相关，使 agent 能够适应演进中的任务与环境。

memory updating 是通过持续创建新表示 [32]、将其与既有知识整合，并剪除过时或无关信息 [13]，以维持 long-term memory 内部一致性与准确性的动态过程。近期研究大致可分为 intrinsic 与 extrinsic。intrinsic updating 通过自包含过程精炼知识库：选择性编辑 [13] 通过选择性删除过时信息来改进 memory；递归摘要 [292] 通过迭代摘要压缩对话历史；memory 混合将过去与当前表示合并，形成演进后的洞见 [139]；自我反思式演进通过将 memory 与 retrieval 证据核验，增强事实一致性 [262]。外在更新依赖外部信号，例如将用户的直接纠正纳入 memory，从而实现系统的持续改进 [45]。归根结底，任何 memory updating 的成功取决于其能否在不破坏关键既有知识、不违反事实与风格一致性的前提下整合新信息。

![](../assets/arxiv-2505.00675-chart1.jpg) 
图 3. long-term memory 部分所讨论高亮论文（RCI > 1）的发表统计。

memory forgetting 涉及移除先前已整合的 long-term memory 表示。与认知心理学研究的被动衰退不同，LLM agent 中的 forgetting 是对已整合信息进行主动、有针对性的「machine unlearning」，其驱动因素是需要清除敏感、有害或私密内容以满足外部约束 [32, 212]。因此，面向安全、隐私与合规的鲁棒 machine unlearning 能力已成为关键研究焦点 [69, 118, 157, 185, 187]。首要挑战是在不损害其余有效知识的完整性与性能的前提下，实现对目标数据的精确且完整移除。

3.1.3 memory adaptation。memory adaptation 聚焦于从已存 long-term memory 中检索并压缩相关信息，以支撑推理、决策与生成。它弥合了大量被动的已存知识仓库与有效推理和生成所需的即时 context 之间的鸿沟。memory retrieval 选择相关信息，而 memory condensation 则将这些信息转化为模型可用的结构化、紧凑 context。这些操作的最终成功，以其支撑 memory-grounded generation 最后阶段的能力来衡量。

memory retrieval 聚焦于为给定查询选择最相关的 memory 条目。retrieval 方法可分为三种主要范式：（1）查询中心 retrieval，精炼查询本身以提高搜索准确性，如 FLARE [129] 与 IterCQR [116]；（2）memory 中心 retrieval，通过增强 indexing [314] 或重排序 [65] 改进已存信息的组织与排序；（3）事件中心 retrieval，利用时间与因果结构进行 context-aware 选择，如 LoCoMo [196] 与 MSC [327] 所探索的那样。多跳图遍历等技术进一步丰富了这一过程 [84]，但核心挑战仍在于开发自适应 retrieval 策略，能够动态适应 memory 库本身不断演进的结构与相关性。

memory condensation 是推理时过程，将原始、已检索的 long-term memory 转化为供 LLM 使用的结构化、紧凑 context。integration 可能跨越多个 memory sources（例如长期对话历史、外部知识库）与模态（例如文本、图像或视频），从而实现更丰富、contextually grounded 的生成。近期 memory consolidation 工作大致可分为两种策略。静态 context integration 方法，如 EWE [31] 与 Optimus-1 [169]，聚焦于在推理时检索并组合静态 memory 条目，以丰富 context 并提升推理一致性。相比之下，动态 memory evolution 方法，以 A-MEM [100]、Synapse [374]、R2I [247] 与 SCM [282] 为代表，强调让 memory 在交互过程中生长、适配与重构，或通过动态链接，或通过受控 memory updating。静态 integration 增强即时的 context grounding，而近期工作已将 condensation 转变为更具 agentic 的范式——agentic context engineering（ACE）[361]，其中自主 agent 主动精炼、排序并重构检索到的 context，以最大化推理效率。这种由 agent 驱动的 memory condensation 演进，是构建自适应、自我改进与终身学习 agent 的关键一步。

memory-grounded generation 可依据 memory 影响生成的方式大致分为三类。自我反思推理（Self-Reflective Reasoning）利用先前思维过程的 memory 来引导中间推理步骤，例如 MoT [160] 与 StructRAG [165]。反馈引导纠正（Feedback-Guided Correction）利用过去错误或用户反馈的知识来约束解码并防止其重复 [234, 270]；context 对齐的长期生成（Contextually-Aligned Long-Term Generation）整合远期历史摘要，以在整个长对话或文档中保持连贯性 [32, 190]。所有这些方法面临的主要挑战，是缓解早期 retrieval 操作带来的噪声或不准确信息的影响，确保最终输出既可靠又有事实依据。

3.1.4 个性化。个性化对 long-term memory 至关重要，但受数据稀疏、隐私与用户偏好变化所限。当前方法大致可分为两条路线：model-level adaptation 与 external memory augmentation。

model-level adaptation 通过 fine-tuning 或轻量更新将用户偏好编码进模型参数。一种策略是将用户特征嵌入潜在空间，其中 CLV 等方法使用对比学习对人物形象表示进行聚类，以引导生成 [272]。更普遍的策略采用参数高效技术；例如 RECAP 通过前缀编码器注入用户历史 [182]，而 Per-Pes 组装反映用户行为的模块化适配器 [269]。在专门领域，MaLP [358] 引入双过程 memory，用于建模医疗对话中的短期与长期个性化。这一范式的核心挑战是管理个性化—泛化权衡：在不损害模型广泛预训练能力的前提下，有效地将模型专门化到个体。

external memory augmentation 通过在推理时从外部仓库检索用户特定信息来个性化响应。该方法随 memory 格式而异：结构化 memory（如用户画像或 knowledge graph）用于在 LaMP [246] 中构建个性化 prompt；非结构化 memory（如对话历史）在 LAPDOG [105] 等系统中提供丰富的 context 数据以进行对齐；而 SiliconFriend [375] 等混合系统维护持久的 cross-session memory storage。这些方法虽可良好扩展，但往往将 long-term memory 视为被动缓冲，其用于主动规划与决策的潜力大多未被开发。

3.1.5 讨论。long-term memory 评估仍受静态假设制约。当前 benchmark 主要遵循两种范式：基于知识的问答（QA）与多轮对话。QA 任务测试模型检索并推理事实知识的能力，同时利用 parametric memory [21, 51, 336] 与非结构化 contextual memory [132, 245]。自演进对齐 [364] 与 salient memory distillation [147, 190] 等技术增强 factual grounding。然而，这些 benchmark 往往假设静态 memory，忽视 updating、选择性保留与时间连续性等动态操作 [196, 314]。相比之下，多轮对话 benchmark（例如 LoCoMo [196]、LongMemEval [314]）跨越 20–30 轮，并支持对 cross-session retrieval、更新与事件推理的分析，因而更好地反映真实世界的 memory 使用。但多数仍将对话历史视为静态 context，狭隘地聚焦 QA 准确性，而忽视 indexing、consolidation、forgetting 与用户适配等操作。这种静态透镜限制了对 memory 如何随时间演进的理解，尤其是在需要时间适配的交互场景中。近期工作已开始通过基于 agent 的系统 [329] 应对这些挑战，将 long-term memory 整合进多轮规划与生成。

memory retrieval 与 memory-grounded generation 之间的失配揭示了 context engineering 的瓶颈。我们分析了近期研究所报告的 retrieval—generation 性能差距 [84, 196, 314, 375]。如图 4 所示，最先进模型在 2Wiki 与 MemoryBank 上取得超过 90 的 Recall@5 [84, 375]，但生成指标（例如，F1）落后超过 30 个百分点。这表明高 retrieval 率并不保证有效生成。多种因素造成这一现象：紧凑 memory 格式（例如对话轮次或任务级观察）比冗长条目更能支撑生成；memory 与查询之间的时间距离越长，如 MemInsight 在 LoCoMo 上的表现 [245]，即便 retrieval 准确，生成也会退化，凸显时间推理是 memory-grounded generation 的关键瓶颈。近期 TREMU [78] 等工作试图通过 chain-of-thought 监督加以解决，但实证收益仍然有限，进一步表明 long-horizon agent 将日益遭遇这一约束；retrieval 更多条目会引入噪声并损害解码；多语言环境则揭示出持续的语言差距，英语优于中文。这些发现表明，当前系统虽能检索相关 memory，但在为下游生成而结构化并利用这些 memory 方面仍然受限。

![](../assets/arxiv-2505.00675-chart2.jpg) 
(a) benchmark

![](../assets/arxiv-2505.00675-chart3.jpg) 
(b) LoCoMo 上的任务

![](../assets/arxiv-2505.00675-chart4.jpg) 
(c) MemInsight 上的任务

![](../assets/arxiv-2505.00675-chart5.jpg) 
(d) 格式

![](../assets/arxiv-2505.00675-chart6.jpg) 
(e) TopK

![](../assets/arxiv-2505.00675-chart7.jpg) 
(f) 语言与模型 
图 4. 用于评估 long-term memory 的 benchmark。$^ { * } M 0 ^ { * }$ 表示模态。「Ops」表示可操作性。「DS Type」表示数据集类型（QA——问答，MS——multi-session 对话）。「Per」与「TR」表示是否存在人物形象与时间推理。

memory operations 在当前 benchmark 中仍未被充分评估。尽管对 memory-augmented 模型的兴趣日增，当前评估主要聚焦 retrieval 准确性（例如 Recall@k、Hit@k、NDCG）与 retrieval 后生成质量（例如 F1、BLEU、ROUGE-L），如 LoCoMo 与 LongMemEval 所示。虽然部分研究纳入了对 memorability、连贯性与正确性的人工评估，但这些努力在很大程度上忽视了 memory 使用的过程性方面——例如 consolidation、updating、forgetting 与选择性保留。近期一些工作，如 MemoryBank 与 ChMapData-test [313]，开始处理 memory updating 与长期规划的某些方面，但仍孤立且范围狭窄。当前迫切需要覆盖 parametric、context 非结构化与结构化 memory 的综合 benchmark，以及超越静态 QA 准确性的动态评估协议，以评估 memory 可靠性、时间推理与 multi-session 对话一致性。

![](../assets/arxiv-2505.00675-fig3.jpg)

![](../assets/arxiv-2505.00675-fig4.jpg)

![](../assets/arxiv-2505.00675-fig5.jpg)

![](../assets/arxiv-2505.00675-chart8.jpg)

![](../assets/arxiv-2505.00675-chart9.jpg) 
图 5. long-term memory 部分所讨论高亮论文（RCI > 1）的发表统计。

![](../assets/arxiv-2505.00675-chart10.jpg) 
图 6. 基于 compression 的方法在 LongBench [15] 上的性能与 compression ratio 对比。数据取自 Yuan 等 [353]。

发表趋势。如图 3 所示，retrieval 与生成主导近期文献，尤其在 NLP 领域。consolidation 与 indexing 等核心操作在 ML 领域获得更多关注，而 forgetting 仍未被充分探索。个性化因实际应用需求而主要局限于 NLP。就引用影响力而言，consolidation、retrieval 与 integration 发挥关键作用——这由 memory 感知 fine-tuning、摘要、RAG 与 prompt fusion 的进展所驱动。

将评估从孤立的 memory operations 转向对 memory encoding、memory evolving 与 memory adapting 的系统性评估。

![](../assets/arxiv-2505.00675-fig6.jpg)

超越对话的有效 long-horizon 时间推理方法仍然缺乏。

解决 retrieval—生成脱节需要优先考虑简洁、可靠 memory condensation 的 context engineering 策略。

通过超越 memory storage、转向 cross-session memory 的自适应复用与个性化，推进个性化 agent。

## 3.2 long-context memory

在对话式搜索中管理大量多来源外部 memory（short-term memory），对 long-context 语言理解构成重大挑战。尽管模型设计与 long-context 训练的进展已使 LLM 能够处理数百万输入 token [56, 58]，但在如此广泛 context 中有效管理 memory 仍是一个复杂问题。就 memory operations 而言，这些挑战大致可分为两个方面：1）memory compression，聚焦于压缩 context token 或 KV cache 的 short-term memory，以实现高效 long-context 解码；以及 memory retrieval，优化 contextual memory 的选择，以实现有效的 long-context 处理。本节系统回顾应对这些挑战的努力。

3.2.1 memory compression。为管理大量多来源外部 memory，LLM 必须被优化以高效处理 long-context。本节讨论高效处理 long-context short-term memory 的方法，重点在 memory compression。具体而言，我们同时讨论 context token（例如文档、对话历史）的 memory operations 与 KV cache（即 working memory）的 memory operations。

context compression 利用 memory compression 操作优化 contextual memory utilization，通常涉及两类主要方法：软 prompt compression 与硬 prompt compression [167]。软 prompt compression 聚焦于在推理阶段将输入 token 块压缩为连续向量（例如 AutoCompressors [37]、xRAG [36]、CEPE [345]），或在训练阶段将任务特定 long-context（例如数据库模式）编码进 fine-tuning 模型的 parametric memory（例如 YORO [142]），以缩短输入序列长度。

硬 prompt compression 则直接将长输入块压缩为更短的自然语言块。基于 eviction 的方法从 context 中选择性剪除无信息量的 token（例如 Selective Context [162]、Adaptively Sparse Attention [7]、HOMER [257]）或块（例如 Semantic Compression [72]），以缩短输入。基于摘要的方法（例如 RECOMP [325]、CompAct [347]、Nano-Capsulator [40]、LLMLingua 系列 [124, 125, 227]）则通过抽象关键信息来压缩长输入。混合方法（例如 TCRA-LLM [176]）结合对无信息 token 的 eviction 与 context 块抽象的特征，以增强 context compression。借助 soft prompt 与 hard prompt，LLM 可以通过 memory compression 更有效地利用 context。

除静态 compression 外，近期出现了基于 RL 的主动管理（Active Management），将 context 利用视为动态决策过程。AgentFold [344] 与 FoldGRPO [264] 等方法利用可验证奖励强化学习（Reinforcement Learning from Verifiable Rewards, RLVR）训练 LLM agent，在任务执行期间主动管理与压缩 long-context 信息。与传统摘要或剪枝不同，这些方法让 agent 通过针对任务特定奖励的优化，学习 memory 保留的最优策略。从静态软 compression 与硬 compression 转向 RL 驱动的主动管理，使 LLM 能够超越简单的 token 缩减，面向 long-context memory 处理实现任务感知的 memory 优化。

KV cache eviction。在 long-context 处理中，KV cache（working memory）通过将过去的 key-value 对存储为外部 parametric memory，力求最小化不必要的 key-value 计算。然而，随着 context 长度增加，存储这些 memory 所需的内存呈二次增长，使其在极长 context 下不可行。KV cache eviction 旨在通过消除不必要的 KV cache 来缩减缓存规模。静态 eviction 方法以固定模式选择不必要的缓存。例如，StreamingLLM [323] 与 LM-Infinite [86] 使用 Λ 形稀疏模式，LCKV [315] 仅保留顶层的 KV cache，而 LaCache [251] 使用梯形 eviction 模式以保留长程依赖。相比之下，动态 eviction 方法更灵活，依据查询（例如 H<sub>2</sub>O [368]、FastGen [77]、Keyformer [2]、Radar [88]、NACL [35]）或推理期间的模型行为（attention 权重）（例如 SnapKV [163]、HeadKV [76]、Scissorhands [184]、PyramidInfer [334]、$\mathrm { L } _ { 2 }$ Norm [53]、SirLLM [342]、D-LLM [127]、CateKV [123]、RocketKV [19]）决定要消除的 KV cache。考虑到丢弃 KV cache 可能造成信息损失，基于合并的方法（例如 MiniCache [172]、InfiniPot [138]、CHAI [3]）合并相似 KV cache，或用特殊 token 存储 KV cache（Activation Beacon [360]），而非直接丢弃，以减少信息损失。

KV cache storing optimization。作为压缩 KV cache 的另一种方式，KV cache storing optimization 考虑移除较不重要元素时可能的信息损失，并聚焦于如何在更小占用下保留整个 KV cache。例如，LESS [59]、Eigen [249] 与 ShadowKV [263] 将 KV cache 条目压缩为低秩表示，而 FlexGen [250]、Atom [371]、KVQuant [98]、ZipCache [93]、KIVI [188] 对 KV cache 进行动态量化以减少内存分配。更近期，Kelle [322] 等动态方法提出软硬件协同设计解决方案，以降低存储 KV cache 的成本。与 KV cache eviction 方法相比，这些方法的性能下降较小，但因内存增长的二次特性而仍受限制。未来工作应继续关注更小内存成本与更小性能下降之间的权衡。

3.2.2 memory retrieval。除压缩 contextual memory 以减轻 long-context 处理负担外，优化 long-context 中的 memory retrieval 提出了另一重要挑战，即从噪声 context 中有效识别关键信息。考虑到 contextual memory 的类型，这些努力可归纳为 context retrieval 与 KV cache selection。

context retrieval 旨在增强 LLM 从 contextual memory 中识别并定位关键信息的能力。基于图的方法，如 CGSN [219] 与 GraphReader [158]，将文档分解为图结构以进行有效 context 选择。token 级 context 选择方法（例如 TRAMS [351]、Selection-p [41]、PASTA [362]）剪枝和/或选择被认为最重要的 token。相比之下，NBCE [259]、FragRel [354] 与 Sparse RAG [382] 等方法在片段级执行 context 选择，依据 context 片段对特定任务的重要性选择相关片段。此外，Ziya-Reader [91] 与 FILM [6] 等基于训练的方法用专门数据训练 LLM，以帮助提升其 context 选择能力。MemGPT [226]、Neurocache [244] 与 AWESOME [24] 等其他方法保留外部向量 memory 缓存，先将外部 memory encoding 进向量空间，再有效地存储与 retrieval；这一外部向量 memory 可被有效更新或 retrieval，从而实现 long-term memory 利用。与这些方法一起，LLM 能够通过 memory retrieval 更好地识别 context 中的关键信息。

KV cache selection 选择性加载必要的 KV cache 以加速推理，聚焦于高效 memory retrieval。QUEST [271]、TokenSelect [316] 与 Selective Attention [151] 应用查询感知的 KV cache selection，识别关键缓存以加快推理。类似地，RetrievalAttention [174] 采用近似最近邻（Approximate Nearest Neighbor, ANN）搜索来定位重要缓存。通过将 KV cache 在外部存储并在推理时 retrieval，Memorizing Transformers [318]、LongLLaMA [280]、ReKV [54] 与 ArkVale [33] 高效处理 long-context。这些方法避免了 KV cache eviction，并与存储优化技术集成，从而提供灵活性（例如 Tang 等 [271] 表明 QUEST 与 Atom [371] 兼容）。

## 3.2.3 讨论。

lost in the context。尽管有主张称 context 长度可扩展至数百万 token，但 long-context LLM 在问答与 key-value retrieval 等任务中已被发现会遗漏 context 中部的关键信息 [179, 241]。在管理大量外部 memory 时，这种「中间迷失（lost in the middle）」问题尤为关键，因为关键信息可能位于 long-context 的不同位置。此类局限也延伸至多模态 context；正如 MMLongBench [311] 所示，long-context 视觉语言模型（Long-Context Vision Language Models, LCVLM）在处理冗长的交错文本—图像文档时，也表现出类似的「中间迷失」现象。此外，在需要基于 contextual memory 进行推理的更复杂场景中，LLM 也无法有效聚合 context 不同部分的 memory [106]。进一步而言，尽管更大的 retrieval 集可获得更高召回，但无关信息会误导 LLM 并损害生成质量 [131, 252]。有效 context 利用成为应对这些局限的关键挑战，涵盖 memory operations 中的 context retrieval 与 context compression。

compression ratio 与性能下降之间的权衡。compression 作为 long-context memory 涉及的主要 memory operations 之一，被广泛用于压缩 parametric memory（KV cache）与 contextual memory（Context），以平衡效率（compression ratio）与有效性（性能下降）。不同基于 compression 的策略各有优劣。例如，KV cache eviction 方法通常达到更高 compression ratio，但导致更大信息损失，从而造成更显著性能下降。Yuan 等 [353] 针对这些不同策略提出通用 benchmark，并定性展示各策略的优劣。如图 6 所示，总体而言，KV cache storing optimization 方法（以 'x' 标记）在有效性与效率之间取得最佳权衡。相比之下，KV cache eviction 方法（以 ∇ 标记）更灵活，可完全定制 compression ratio，但有效性较低。另一方面，压缩 contextual memory（以 Δ 标记）相比压缩 parametric memory 有效性更低，LLMLingua2 相对较差的表现即为佐证。

发表趋势。图 5 总结了 long-context 方面的发表趋势。NLP 社区更关注 contextual memory 的利用，而 ML 社区在 parametric memory 的效率上投入更多。从 RCI 视角看，KV cache storing optimization 主导 long-context 主题的讨论。这种主导不仅源于效率与有效性的平衡，也源于其与其他 long-context 方法的兼容性。比较两种 memory operations，retrieval 方法通常获得较少关注。原因之一是 context retrieval 与 long-term memory、multi-source memory 等其他主题存在重叠，导致其在图 5 中被一定程度低估。此外，理解 RAG 与 long-context 之间的关系 [131, 166] 对基于 memory 的 LLM agent 发展至关重要。然而，关于复杂环境中 context 利用的有影响力工作仍然缺乏。填补这一空白是有价值的未来方向。

在 KV cache 优化中平衡更低的 memory 占用与最小化的性能退化，是未来研究的一个令人兴奋的方向。

复杂环境（例如 multi-source memory）中的 context 利用，是推进 agent 发展的关键研究方向。

## 3.3 parametric memory modification

修改 parametric memory——即编码在 LLM 参数中的知识——对于动态适配已存 memory 至关重要。parametric memory modification 方法大致可分为三类：（1）editing 是对模型参数的局部修改，无需完整重训练；（2）machine unlearning 选择性移除不需要或敏感的信息；（3）continual learning 增量纳入新知识，同时缓解 catastrophic forgetting。本节系统回顾这些类别的最新研究，后续小节提供详细分析与比较。

3.3.1 editing。parametric memory editing 更新 parametric memory 中存储的特定知识，而无需完整重训练。一条重要工作路线涉及直接修改模型权重。主流策略是定位—编辑方法 [52, 70, 83, 107, 201, 203, 205]，利用归因或追踪找到事实存储位置，然后直接修改已识别的 memory。另一种方法是元学习 [50, 83, 159, 211, 267, 365]，其中编辑器网络学习预测目标权重变化，以实现快速且鲁棒的纠正。一些方法完全避免改动原始权重。基于 prompt 的方法 [373, 376] 使用 ICL 等精心构造的 prompt 间接引导输出。附加参数方法 [48, 60, 212, 289, 300] 添加外部 parametric memory 模块以调整行为，而不触碰模型权重。这些方法在效率与可扩展性上各异，但多数聚焦实体级编辑。

3.3.2 machine unlearning。parametric memory unlearning 通过移除特定 memory 而保留无关 memory，实现选择性 forgetting。近期工作探索了若干策略。附加参数方法添加 logit 差异模块 [118] 或 unlearning 层 [30] 等组件，在不重训练整个模型的情况下调整 memory。基于 prompt 的方法操纵输入 [173] 或使用 ICL [231]，从外部触发 forgetting。locating-then-unlearning 方法 [119, 277, 317] 先识别负责的 parametric memory，再施加针对性更新或停用。基于训练目标的方法 [120, 185, 304, 343] 显式修改训练损失函数或优化策略以促成 memory forgetting。这些方法旨在给定显式 forgetting 目标时抹除 memory，同时保留非目标知识，并平衡效率与精确性。

3.3.3 continual learning。continual learning [287] 通过缓解模型参数中的 catastrophic forgetting，实现 long-term memory 的持久性。两类主要方法是基于正则化与基于回放的方法。正则化约束对重要权重的更新，保护关键 parametric memory；TaSL [73]、SELF-PARAM [302]、EWC [141] 与 POCL [319] 等方法应用此类约束，在无需回放的情况下 embedding 知识。相比之下，基于回放的方法通过重新引入过往样本强化 memory，尤其适合在训练期间纳入检索到的外部知识或历史经验。例如，DSI++ [200] 利用生成式 memory 以伪查询补充学习，在无需完整重训练的情况下维持 retrieval 性能。除这些范式外，LifeSpan Cognitive System（LSCS）[301] 等基于 agent 的工作将 continual learning 扩展至交互式情境，使 agent 通过实时经验增量获取并整合 memory。LSCS 为外部 memory 如何持续编码进模型参数提供了有价值的洞见。

## 3.3.4 讨论。

SOTA 方案分析。我们选取不同类别中的近期 SOTA 方法，并在图 10 中报告其在 memory editing（CounterFact [203] 与 ZsRE [152]）与 memory unlearning（ToFU [197]）最常用数据集上的性能。我们通过使用一致的基座模型与适当的评估指标，力求公平比较。具体而言，对于 CounterFact 与 ZsRE，我们遵循 Meng 等 [203]，从数据集中随机选取 2,000 个样本进行更新，每次编辑 100 个样本。CounterFact 上的所有方法均使用 GPT-J 作为基座模型；对于 ZsRE，多数使用 GPT-2，MELO 除外，其使用 T5-small。对于 ToFU benchmark，所有方法均在 10% forgetting 设置下使用 LLaMA2-7B-chat。基于 prompt 的方法在所有 benchmark 上取得较强的总体表现，而元学习方法通常逊于其他方法。我们观察到，同一批方法在 ZsRE 上的表现往往比在 CounterFact 上更差。这一下降主要源于 ZsRE 上的特异性得分显著较低，进而拉低总体得分。这凸显了实现精确、针对性编辑的挑战，并表明提升特异性仍是有前景的研究方向。此外，我们发现多数当前 SOTA 方法在 ToFU benchmark 上取得高分，表明该 benchmark 可能挑战性不足，需要新的 machine unlearning benchmark。

扩展性挑战。图 8 展示了不同方法支持的最大连续编辑次数。除 MemoryLLM 支持多达 65 万次编辑外，多数方法仅测试 1,000 至 5,000 次编辑。我们还注意到，连续 machine unlearning 研究仍然稀少，是未来探索的开放领域。图 9 展示了不同方法所使用的模型规模分布。在编辑与 machine unlearning 中，非 prompt 方法通常应用于中、小模型（≤ 20B）。相比之下，基于 prompt 的方法更常在较大模型上评估，这可能因其依赖更强的指令遵循与 in-context learning 能力。另一方面，非 prompt 方法常因较高计算成本而面临可扩展性挑战，难以应用于大模型。这凸显了进一步研究如何平衡模型规模与编辑或 machine unlearning 有效性及效率的必要性。

![](../assets/arxiv-2505.00675-fig7.jpg)

![](../assets/arxiv-2505.00675-chart11.jpg)

![](../assets/arxiv-2505.00675-chart12.jpg) 
图 7. 本节所讨论高亮论文（RCI > 1）的发表统计。

![](../assets/arxiv-2505.00675-chart13.jpg) 
图 8. 不同 model editing 方法支持的最大连续编辑次数。

![](../assets/arxiv-2505.00675-chart14.jpg)

![](../assets/arxiv-2505.00675-chart15.jpg) 
图 9. memory 编辑与 machine unlearning 中的模型规模分布。

![](../assets/arxiv-2505.00675-chart16.jpg)

![](../assets/arxiv-2505.00675-chart17.jpg) 
图 10. 不同类别方法在 CounterFact（编辑）、ZsRE（编辑）与 TOFU（machine unlearning）benchmark 上的 SOTA 方案。

发表趋势。图 7 展示了编辑、machine unlearning 与终身学习中 RCI > 1 论文的发表统计。编辑最受关注，尤其是定位—编辑与附加参数方法。NLP 会议更关注编辑，而 ML 工作在三个领域分布更均匀。定位—编辑的 RCI 方差也最高，反映出若干高影响力研究。machine unlearning 虽占比较小，但在基于目标与基于参数的类别中展现出强大潜力。相比之下，终身学习仍相对未被充分探索。

当前编辑方法往往缺乏特异性，而 TOFU 等 machine unlearning benchmark 可能过于简单，无法揭示真实局限。

agent 应利用 continual learning，通过与环境的持续交互实现自我演进，同时不覆盖稳定的 parametric memory。

![](../assets/arxiv-2505.00675-chart18.jpg)

![](../assets/arxiv-2505.00675-chart19.jpg) 
图 11. multi-source memory 部分所讨论高亮论文（RCI > 1）的发表统计。

![](../assets/arxiv-2505.00675-chart20.jpg) 
图 12. 跨文本推理趋势：memory sources 与推理策略。

## 3.4 multi-source memory

multi-source memory 对真实世界的 AI 部署至关重要，系统必须同时推理内部参数与外部知识库，覆盖结构化数据（例如 knowledge graph、表）与非结构化多模态内容（例如文本、音频、图像、视频）。本节从两个维度考察关键挑战：cross-textual integration 与多模态协调。

3.4.1 cross-textual integration。cross-textual integration 使 AI agent 能够从多个文本来源执行更深层推理并解决冲突，以支撑更具 context grounding 的响应。

reasoning 聚焦于整合多格式 memory，以生成事实与语义一致的响应。一条研究路线考察跨不同领域 memory 的推理，尤其是通过精确操纵结构化符号 memory，如 ChatDB [102] 与 Neurosymbolic [295] 所示。其他工作 [220, 320] 探索领域特定 parametric memory 的动态 consolidation，以实现更灵活的推理。跨多样文档来源的 multi-source 推理也已得到研究，如 DelTA [306] 与 dynamic-MT [63]。此外，若干研究 [148, 165, 331, 369] 通过从结构化与非结构化来源检索信息，考察异构知识整合。尽管这些努力在结合 parametric 与外部 memory 进行推理方面取得实质进展，但实现异构、multi-source memory 的统一推理仍是一大开放挑战。特别而言，需要更多工作来有效整合 parametric memory 与结构化及非结构化外部知识来源。

multi-source memory 中的 conflict 指在检索并推理异构 memory representation 时出现的事实或语义不一致。这些冲突常在整合 parametric 与 contextual memory，或结合结构化与非结构化知识（如三元组、表与自由文本）时出现 [328]。先前工作聚焦于识别并定位此类不一致。例如，RKC-LLM [299] 提出评估框架，以评估模型检测 context 矛盾的能力；BGC-KC [268] 则指出模型倾向于偏好内部知识而非 retrieval 内容，从而推动来源归因与信任校准。这些方法为理解 memory conflict 提供了重要基础，但许多仍局限于静态场景或单源推理。

3.4.2 多模态协调。随着 memory-augmented 系统向多模态设置演进，关键挑战在于对文本、图像、音频与视频等异构模态进行 fusion 与 retrieval。

![](../assets/arxiv-2505.00675-chart21.jpg) 
图 13. 各年份 memory operations 支持的演进。

![](../assets/arxiv-2505.00675-chart22.jpg) 
图 14. 多模态协调中时间建模、fusion 策略与 retrieval 方法的分析。

fusion 指对不同模态的检索信息进行对齐。从 memory 视角看，fusion 是随时间整合跨模态信息的关键机制。现有方法大致可分为两条路线。第一条聚焦统一语义投影，UniTransSeR [194]、MultiInstruct [332]、PaLM-E [62] 与 NExT-Chat [355] 等模型将异构输入嵌入共享表示空间，以供复用与查询。第二条强调长期跨模态 memory consolidation。例如，LifelongMemory [305] 引入带持久 memory 的 Transformer，在患者记录间累积视觉—文本知识。类似地，MA-LMM [90] 维护多模态 memory 库，以扩展长视频中的时间理解。当前 fusion 方法虽能有效对齐模态，但往往难以支撑长期多模态 memory management。关键挑战包括动态 memory updating 以及维持异构来源间的一致性。

多模态系统中的 retrieval 使跨文本、图像与视频等模态访问已存知识成为可能。多数现有方法依赖基于 embedding 的相似度计算，其基础是 QwenVL [14]、CLIP [237] 或其他多模态模型 [164] 等视觉—语言模型。这些模型将异构输入投影到共享语义空间，从而支持跨模态 retrieval。例如，VISTA [378] 通过视觉 token 表示增强 retrieval，而 UniVL-DR [186] 通过统一双编码器整合视频与语言。更近期，IGSR [281] 通过引入意图感知贴纸 retrieval，将 retrieval 扩展至 multi-session 对话，但仍以相似度 retrieval 为基础。MMLongBench [311] 凸显了此类方法的局限：即便最先进的大型视觉—语言模型（Large Vision-Language Model, LVLM）也难以进行跨模态 retrieval。因此，这些方法往往缺乏推理驱动 retrieval 的能力，并忽视具身交互所需的音频与感觉运动信号等关键模态。为弥合这些差距，M3 [189] 面向开放式 agent 引入多模态 memory 建模框架，统一跨音频与感觉运动信号等多样数据类型的存储与推理。通过支持动态更新与推理驱动 retrieval，M3 超越浅层对齐，确保鲁棒的 long-term memory 管理。

## 3.4.3 讨论。

multi-source memory integration 的趋势。近期研究 [256, 281] 显示，multi-source memory 的组织、retrieval 与推理方式正在稳步演进。尽管针对 cross-textual integration 与多模态协调已提出多样方法，但细察代表性模型（图 12、13、14）可发现共同挑战与新兴趋势。这些发展反映出从静态 retrieval 流水线向动态、context 敏感 memory system 的更广泛转变，此类系统能够跨任务与 session 支撑基于时间的、跨来源的推理。

cross-textual integration 涉及两个关键设计轴：来源类型与推理机制。早期模型如 ChatDB [102] 与 EMAT [320] 使用通过显式查询访问的符号 memory（例如数据库、表），提供透明性，但在开放域场景中可扩展性有限。更近期的系统如 StructRAG [165]、DelTA [306] 与 Chain-of-Knowledge [161] 采用非结构化 memory 与神经 retrieval，结合基于 attention 的 fusion 与 chain-of-thought 推理。然而，多数仍将 memory 视为静态，与实时推理脱节。MATTER [148]、GoG [331] 与 ZCoT [208] 等更新模型迈向推理感知 memory，使用 retrieval—生成循环与协作 agent 动态演进 memory。尽管有此转变，解决异构来源间的冲突仍是一大挑战。retrieval 内容与 parametric 内容常被合并，却未进行一致性检查或来源归因，导致幻觉与事实漂移 [268, 379]。多步冲突解决 [299] 与认知校准 [328] 等初步方案具有前景，但缺乏可扩展性。未来工作应追求集成的、冲突感知的 memory system，能够在不确定性与来源歧义下进行动态推理。

多模态 memory 协调已在三个关键维度上取得进展：fusion、retrieval 与时间建模。如图 14 所示，常见策略包括联合 embedding [90, 194, 281, 311, 378] 与 prompt 级 fusion [82, 305]，而基于标识符的 memory [164] 与跨模态图融合 [218] 等近期方法实现了更具选择性、任务自适应的 integration。retrieval 已从静态相似度演进为时间 context 化方法，包括时间图与时间感知 attention [324]，促进对长期交互的推理。值得注意的是，60% 的受调查模型编码时间信息，凸显时间在 long-horizon 任务中的重要性。除 retrieval 与融合外，操作控制——例如 memory updating、indexing 与 compression——正日益重要。早期系统（2022–2023）主要聚焦 retrieval，而 E-Agent [80] 与 WorldMem [324] 等较新 agent 采用自维护架构，随时间持续精炼 memory content。例如，WorldMem 压缩多模态日志，而 E-Agent 动态更新内部 memory 以支撑 long-horizon 规划。这些系统凸显了从被动 memory 查询向主动、操作丰富的架构的转变。

发表趋势。如图 11 所示，跨文本推理主导发表数量，反映其在 multi-source integration 中的基础性作用。fusion 研究，尤其是 CLIP [237] 驱动的工作，展现出最高的引用影响力与对多模态学习的影响。相比之下，动态 retrieval 与冲突解决仍未被充分探索。总体而言，这些趋势表明该领域正从表层 integration 转向更深层、操作感知且时间结构化的 memory architecture。

设计冲突感知的 memory mechanism，显式检测、归因并解决演进中的 memory 与异构表示之间的不一致。

开发自维护 memory architecture，内置 indexing、updating、compression 与一致性检查，以支持长期、cross-session 使用。

通过整合多模态 long-context 理解与多轮对话推理，推进 long-horizon 推理——这是真实世界 agent 的核心需求。

表 1. 产品 memory 设计的权衡。比较代表性产品，以突出 memory system 中反复出现的设计选择与局限。

<table><tr><td>产品</td><td>领域</td><td>主导 memory</td><td>优先操作</td><td>用户体验</td><td>局限</td></tr><tr><td>ChatGPT [223]</td><td>通用</td><td>parametric</td><td>consolidation、retrieval、condensation</td><td>一致性 / 准确性 / 通用性</td><td>幻觉；个性化与模态 memory management 有限。</td></tr><tr><td>Replika [191]</td><td>个人</td><td>contextual</td><td>updating、retrieval</td><td>共情 / 适配</td><td>隐私风险；memory 漂移；cross-session 连续性有限；基于简单槽位的 memory management。</td></tr><tr><td>GitHub Copilot [79]</td><td>任务导向</td><td>parametric</td><td>condensation</td><td>效率 / 可靠性</td><td>无 cross-session 任务连续性；无用户级个性化；无持久 long-term memory。</td></tr><tr><td>Doubao [22]</td><td>多模态</td><td>parametric</td><td>consolidation、retrieval、condensation</td><td>通用 / 风格化 / 低延迟</td><td>幻觉；模态鸿沟；受 session 约束。</td></tr></table>

## 4 实践中的 memory

memory-augmented agent 通过产品、开发工具与基础设施这一相互依赖的层级体系，将理论 memory 概念付诸实践。助手与副驾驶等产品利用 parametric 与 contextual memory 来支撑个性化与 long-horizon 推理。开发工具将实际需求转化为管理存储、retrieval 与适配的框架。基础设施提供在规模上支撑 memory operations 的计算骨干。这些层级之间的互动是双向的：产品需求驱动开发工具设计，工具约束基础设施实现，而基础设施进步又赋能更丰富的产品能力。理解并弥合它们之间的差距，有助于厘清 agent memory 机制的技术与概念前沿。

## 4.1 产品

agent 产品可依据其主导 memory types 与应用焦点大致分类。ChatGPT [223]、Gemini [81]、Claude [8]、Grok [321] 与 DeepSeek [171] 等通用 agent 主要依赖大规模 parametric memory，将广泛的跨领域知识编码进模型权重，并支撑稳定的推理与事实泛化。有限的用户 contextual memory 被叠加其上，以改进 retrieval 与 grounding。个人 agent 主要利用 contextual memory 来捕获用户偏好、交互历史与情感线索，从而实现个性化且自适应的响应 [97, 153, 236]，例如 Replika [191]、Character.AI [27]、Me.bot、Tencent ima.copilot [276] 与 Doubao [22]。这些 agent 实现长期个性化与社会性连贯，代价则是隐私管理与 memory 漂移。任务导向 agent 依赖 contextual memory 与特定领域知识来执行多步推理并维持 session 连续性，如 GitHub Copilot [79]、Cursor [111]、Coze [44]、DeepResearcher [275]、WebSearcher [275] 与 CodeBuddy [370]。对这些 agent 而言，高任务成功率仍是用户满意度与实际有效性的首要考量。多模态 agent 代表一种更整合的范式，在语言、视觉与动作模态上统一 parametric 与 contextual memory。代表性示例包括移动助手（Doubao [22]、Siri [11]、Xiaoyi [109]）与具身 agent，它们将 memory 从文本扩展到感知与具身，标志着迈向通用、long-horizon agent 的一步。

表 2. memory 开发工具的权衡。比较代表性开发工具，以突出其特殊设计与潜在局限。

<table><tr><td>工具</td><td>类别</td><td>memory types</td><td>优先操作</td><td>关键特性</td><td>局限</td></tr><tr><td>EasyEdit [291]</td><td>parametric 编辑</td><td>parametric</td><td>updating</td><td>直接修改 LLM 权重（WISE [289]）</td><td>涟漪效应：编辑事实可能损害通用推理；计算成本高。</td></tr><tr><td>Zep [239]</td><td>时间 memory 构建</td><td>contextual</td><td>consolidation、updating</td><td>时间 knowledge graph；增量摘要；鲁棒时间推理。</td><td>可控性；信息损失。</td></tr><tr><td>Mem0 [255]</td><td>个性化 memory 层</td><td>contextual</td><td>consolidation、indexing、updating</td><td>cross-session 的用户级个性化；混合搜索（向量 + 图）；开发者友好 API。</td><td>有损 condensation；以用户为中心的个性化，而非复杂任务或世界状态 memory。</td></tr><tr><td>MemOS [168]</td><td>memory 调度与层次化管理</td><td>contextual</td><td>updating、retrieval</td><td>操作系统式层次调度（短期/长期/working memory），优化 context window 与 memory management。</td><td>控制开销；延迟。</td></tr><tr><td>Graphiti [92]</td><td>图 memory 构建</td><td>contextual</td><td>indexing、updating、retrieval</td><td>从非结构化流动态构建 knowledge graph；语义关系追踪。</td><td>严格类型化的图可能脆弱，图构建的 token 消耗高。</td></tr></table>

尽管这些产品已部分整合 memory-related 功能，其 memory 范围与模态在不同领域差异显著。ChatGPT 与 Doubao 通过大模型骨干支撑长程与 cross-session 适配，但其 memory management 仍相对简单，易产生幻觉。其多模态 memory 功能局限于基本的 image-grounded retrieval，而非整合式跨模态推理。Replika 作为面向个性化的陪伴系统，严重依赖透明且由用户驱动的 memory updating。然而，其存储内容完全取决于用户输入，缺乏自主管理并引发隐私担忧，而更高层的 session memory 仍未发展。相比之下，GitHub Copilot 受编程任务复杂性制约，主要在短期 working memory 窗口内运行，没有持久的任务级或项目级 memory 协调，也缺乏个性化的代码适配。总体而言，这些系统仍处于 memory consolidation 的早期阶段，memory operations 在很大程度上基于 prompt，而非动态管理。这一差距凸显了对更先进开发工具的需求，以在跨产品与领域间支撑可扩展、透明且自适应的 memory mechanism。

## 4.2 开发工具

框架。在核心基础设施之上，框架为 memory-related 操作提供模块化接口。示例包括 Graphiti [92]、LlamaIndex [175]、LangChain [28]、LangGraph [112]、EasyEdit [291]、CrewAI [66]、MemU [217] 与 Letta [226]。这些框架将复杂的 memory 过程抽象为可配置流水线，使开发者能够构建与 LLM agent 交互的多模态、持久且可更新的 memory module。memory 层系统。这些系统将 memory 作为服务层付诸实践，提供编排、持久化与生命周期管理。Mem0 [255]、Zep [239]、Memary [140]、MemOS [168] 与 Memobase [140] 等工具聚焦于维持时间一致性、按 session 或主题对 memory 建立 index，并确保高效召回。这些平台常结合符号与亚符号 memory representation，并提供内部 API 以随时间访问与操纵 memory。

## 4.3 基础设施

memory tools 依赖鲁棒的基础设施来实践 memory 的存储、retrieval 与演进。该基础设施以持久存储系统为锚点，例如 Neo4j [216] 等图数据库与向量存储 [61]，它们与从稀疏 BM25 [243] 到稠密 embedding retrieval [113, 224] 的 retrieval 机制协同工作，以确保精确访问。复杂 memory 生命周期操作——包括动态 updating 与针对性 forgetting——的执行，依赖 LLM 在优化 prompt engineering 引导下的推理能力 [1, 171]。关键在于，为支撑这些工具所需的高吞吐与可扩展性，底层计算层纳入了 FlashAttention [46]、序列并行与高效 KV cache 管理策略 [146] 等加速技术，均旨在有效处理超长 context 与海量交互历史。

## 5 生物 memory 与 agent memory 之间的认知鸿沟

人类 memory 并非单一存储，而是感觉、短期与长期系统之间复杂的层级互动 [12]。agent 虽旨在模拟这些功能以支撑推理，但其底层机制不同于生物认知架构。如表 3 所总结，当前 agentic 实现仍聚焦于静态持久性，在 memory encoding、memory evolving 与 memory adapting 方面缺乏生物 memory 的动态精巧性。

encoding：从逐字记录到建构式图式化。人类编码本质上是建构性的；我们并不记录快照，而是通过当下认知重构过去，以适配内部图式。相比之下，agent 通常执行逐字记录（存入数据库）或静态 parametric（存入权重），导致碎片化痕迹的累积，而非综合的自我模型。这种对「原始」数据的依赖，使 agent 无法在入口处剪除噪声。尽管当前训练（例如预训练/后训练 [171]）尝试内化，但它仍是一个离散过程，未能弥合静态「知其然（knowing that）」与过滤环境复杂性所需的自适应认知结构之间的鸿沟。

evolving：从摘要到内化。人类的 memory evolution 依赖睡眠相关的再巩固，其中 episodic traces 被 distillation 为一般世界知识的语义结构。这种主动综合剪除噪声并提取因果模式，以防止对即时现实的过拟合。相比之下，agent memory 演进依赖摘要或硬删除等显式操作来模拟 memory dynamics。ACE [361] 等框架虽利用摘要进行短期缓冲 condensation，但其主要解决即时任务完成，而非长期认知成长。反过来，G-Memory [356] 等系统虽通过层级图构建长期档案，但这仍是一种符号式演进路径。这些机制将 memory 视为需要归档的静态图书馆，而人类 memory 更像肌肉。agent 虽能摘要一本书（短暂经验），却无法将该知识转化为自然执行任务所需的直觉性技能（程序性智慧）。因此，当代 agent 仍是受人工 compression 历史所限的反应式记录者，缺乏长生命周期演进的能力，或构建一致自我表征的能力。

<table><tr><td>方面</td><td>人类 memory</td><td>agent memory</td></tr><tr><td>存储</td><td>跨脑区的分布式、互联神经系统</td><td>模型参数、模块化且依赖 context</td></tr><tr><td>所有权</td><td>个体且私密。</td><td>可共享、可复制、可广播。</td></tr><tr><td>容量</td><td>受生物学限制</td><td>可扩展，仅受存储与算力限制</td></tr><tr><td>memory encoding</td><td>缓慢、生物驱动、被动</td><td>快速、显式、策略驱动且选择性</td></tr><tr><td>memory evolution</td><td>间接、基于再巩固、易出错</td><td>精确、可编程、支持回滚/machine unlearning</td></tr><tr><td>memory adaptation</td><td>隐式，受显著性与频率偏置</td><td>显式、可定制（例如量化、摘要）</td></tr></table>

表 3. 人类 memory 与 agent memory 的关键差异。

adapting：从 retrieval 到意义建构。人类 memory utilization 是由稳态需求与自我一致性驱动的动态重构过程 [12]。相比之下，当前 agent 主要依赖 RAG 与极长 context window。context window 的扩展虽提供更大缓冲，却代表一种绕过语义内化必要性的暴力式架构扩展。这种「long-context」依赖导致信噪比递减与高昂计算成本。如「中间迷失」现象 [179] 所示，缺乏推理时再巩固的 retrieval——其特征是像 AgentFold [344] 与 FoldGRPO [264] 那样主动重写历史痕迹——难以形成连贯的因果表示。下一个前沿是超越被动 retrieval，转向主动思考者，实时重构内部状态以适应环境动态。

存储、所有权与容量。生物 memory 与 agent memory 的分歧，根植于其物理与系统基底的基本属性，主要体现在存储、数据所有权与资源可扩展性上。就存储而言，人类 memory 以生物整体互联为特征，支持全脑范围的联想回忆。相反，agent 依赖异构表示——将数据分割为文档、图与 vector embeddings 等不连通格式——这优先局部模式匹配而非全局语义连贯。这一系统性差距延伸至数据所有权：人类 memory 天然私密且以个体为界，而 agent memory 可复制、可广播，赋能集体智能，却挑战「right to be forgotten」的伦理。最后，人脑以极端的代谢节俭（约 20W）[17] 实现复杂 memory evolution，而 agent memory 仍受硅基扩展的计算与环境成本制约，需要转向以语义密度优先于原始数据量的生物启发式效率。

## 6 开放挑战与未来方向

本节概述核心 memory 主题中的开放挑战，并提出未来研究方向。随后，我们探讨更广泛的视角，包括生物启发模型、终身学习、多 agent memory 与统一 memory representation，这些进一步扩展 memory system 的能力与理论根基。这些讨论共同构成推进 AI 中可靠、可解释且自适应 memory 的路线图。

## 6.1 主题特定方向

设计以 memory 为中心的 AI 需要应对核心局限与新兴需求。在 RCI 分析与趋势的指引下，我们概述塑造未来 memory research 的关键挑战。

需要统一评估，以应对 long-term memory 中的一致性、个性化与时间推理。现有 benchmark 很少评估动态、multi-session 设置中的 consolidation、updating、retrieval 与 forgetting 等核心操作。这一空白造成 retrieval—生成失配：由于 memory 维护不佳，retrieval 内容往往过时、无关或失配。解决这些问题需要时间推理、结构感知生成与 retrieval 鲁棒性，以及支持 cross-session 个性化复用与自适应 memory management 的系统。

long-context 处理：效率与表达力。扩展 memory 长度会加剧计算成本与建模保真度之间的权衡。KV cache compression 与循环 memory 复用等技术提供效率，却伴随信息损失或不稳定风险。同时，对复杂环境（尤其 multi-source 或多模态设置）的推理，需要选择性 context integration、来源区分与 attention 调制。为弥合这些需求，平衡 context 带宽与任务相关性及稳定性的机制，正日益指向使用基于 RL 的框架来学习主动最优 context 管理与折叠策略。

尽管前景可观，parametric memory modification 仍需进一步研究以改进控制、擦除与可扩展性。当前编辑方法往往缺乏特异性，而 TOFU 等 machine unlearning benchmark 可能过于简单，无法暴露真实局限。多数方法无法扩展到数千次编辑以上，或支持超过 20B 参数的模型。终身学习虽有潜力，但仍未被充分探索。未来工作应开发更真实的 benchmark、提升效率，并将编辑、machine unlearning 与 continual learning 统一为连贯框架。

multi-source integration：一致性、compression 与协调。现代 agent 依赖由结构化知识、非结构化历史与多模态信号构成的异构 memory，却面临冗余、不一致与歧义。这些问题源于时间范围错位、语义冲突与跨模态归因缺失。解决它们需要冲突解决、temporal grounding 与溯源追踪。高效 indexing 与 compression 对 multi-session 设置中的可扩展性与可解释性至关重要。

## 6.2 更广泛的视角

除上述核心主题外，一系列更广泛的视角正在涌现，进一步丰富以 memory 为中心的 agent 图景。

procedural 工具 memory 与技能习得。随着 agent 更偏向行动，memory 需要从静态事实存储演进为 procedural 工具 memory：工具使用被内化为可复用技能，而非在长期交互中反复查询工具 API。ReAct [341] 等框架已通过将推理与动作轨迹耦合而暗示这一转变，使 agent 从执行反馈中学习，而非将工具视为无状态调用。包括 MCP [9] 服务器在内的近期基础设施进一步支撑这一演进，将工具框定为持久服务，允许跨交互累积经验。BFCL v4 [229] 等 benchmark 明确暴露了对 memory 执行轨迹、错误恢复策略与工具链组合的需求，而非依赖临时 prompt。工业系统已开始实践这一理念，例如 Anthropic 在 Claude 中引入技能（skills）[10]，将工具使用视为一种 procedural memory，以提升可靠性并降低推理成本。

parametric 共享：memory 作为动态权重。文本 memory（例如 RAG）虽提供透明性，却不可避免地在 compression 与自然语言转换过程中遭受信息损失。我们提出 parametric sharing，即 memory 以模型原生表示 [21]——例如动态适配器或专用 memory 层——直接在潜在空间 [383] 中交换。该方法保留高维语义细微差别，并通过绕过显式文本的「瓶颈」增强 fusion 系统的集体推理。未来工作应探索标准化神经 memory 协议与跨模型权重对齐，使异构 agent 能够将内化经验合并为协作式参数智能。

终身学习。未来研究应从离散任务学习转向管理实时环境流 [361]，聚焦于缓解 catastrophic forgetting 的同时维持快速适配 [73]。在极端数据稀疏条件下，agent 必须利用元学习优化「memory 价值函数」，从而自主决定选择性 memory 内化的「固化价值」[277]。关键在于，个性化表示必须超越基座模型预训练分布的 restrictive inductive bias（限制性归纳偏置），后者常压制独特个体特质。通过将结构化 [239] 与非结构化 memory [13] 整合进动态个性化参数空间（例如演化式 LoRA 或 embedding），agent 可将个人痕迹与一般知识解耦。这确保跨无限视界的因果一致性，使 agent 从任务导向工具演进为纵向的、习惯感知的伙伴。

多 agent 系统中的 memory。在多 agent 系统中，memory 不仅是个体的，也是分布的。agent 必须在管理自身内部 memory 的同时，与他人交互并向其学习 [298]。这带来独特挑战，例如 memory 共享、对齐、冲突解决与跨 agent 一致性。有效的多 agent memory 系统应同时支持个性化经验的局部保留，以及通过共享 memory 空间或通信协议实现的全局协调。未来工作可探索去中心化 memory architecture、跨 agent memory 同步与集体 memory consolidation，以实现协作规划、推理与长期协调。

多模态 memory。多模态 memory 本质上反映人类如何感知真实世界。M3-agent [189] 与 GUI-agent [97] 等进展虽已探索多模态 memory 处理能力，该领域仍处初步阶段。在统一语义空间中对齐多模态 memory，并实现有效 retrieval 与推理，仍存在重大挑战。具体而言，当前系统在多轮交互中推理能力薄弱且存在数据错位，这凸显了未来研究的关键方向。

memory 设计的生物学启发。生物系统中的 memory 为构建更具韧性与自适应性的 AI memory architecture 提供了关键洞见。大脑通过互补学习系统管理稳定性—可塑性困境：海马体编码快速变化的 episodic 经验，而皮层缓慢整合稳定的 long-term memory [144, 199]。受此启发，AI 模型日益采用双 memory architecture、突触 consolidation 与经验回放以缓解 forgetting [242, 284]。memory 再巩固 [67]、有界 memory capacity [43] 与分区化知识 [75] 等认知概念，进一步为更新感知回忆、高效存储与 context 敏感泛化等策略提供启示。

同时，K-Line 理论 [210] 指出，层级 memory 结构是生物认知的基础。这些结构使人类能够在不同抽象层次上高效组织 memory，例如婴儿将「苹果」与「香蕉」等具体物体归入「水果」与「食物」等更广泛类别。以层级结构组织 agent memory 以提升可扩展性与效率，为 memory research 提出新挑战 [87, 310] 与未来方向 [96, 308]。

parametric memory retrieval。尽管近期 knowledge editing 方法 [70, 289] 声称能够定位并修改特定表示，但使模型能够从自身参数中选择性检索知识仍是一个开放挑战。潜 memory（latent memory）的高效 retrieval 与 consolidation，可显著增强 memory utilization 并减少对外部 indexing 与 memory management 的依赖。

spatio-temporal memory 不仅捕获信息之间的结构关系，还捕获其时间演进，使 agent [150] 能够在保留历史 context 的同时自适应更新知识 [372]。例如，agent 可记录用户曾不喜欢西兰花，但随后依据近期购买模式调整其 memory。通过同时维护对历史与当前状态的访问，spatio-temporal memory 支撑基于时间的推理与细致个性化。然而，高效管理与推理长期 spatio-temporal memory 仍是一大关键挑战。

统一 memory representation。parametric memory [335] 提供紧凑且隐式的知识存储，外部 memory [375] 提供显式且可解释的信息；统一它们的表示空间并建立联合 indexing 机制，对有效 memory consolidation 与 retrieval 至关重要。未来工作可聚焦于开发统一 memory representation 框架，支持跨模态与知识形式的共享 indexing、混合存储与 memory operations。

memory 威胁与安全。memory 虽通过支持最新且个性化响应显著增强 LLM 的效用，其管理仍是一个关键安全问题。memory 常存储敏感与机密数据，使添加或移除信息等操作远非平凡。近期研究已暴露 memory 处理中的严重漏洞，尤其是在旨在选择性擦除数据的 machine unlearning 技术中。多项研究 [18, 187] 表明这些方法易受恶意攻击，这强化了对更安全、可靠 memory operations 的需求。

## 7 结论

本综述全面概述 agent memory，将其分为 parametric 与 contextual 类型，并将操作映射到 memory encoding、memory evolving 与 memory adapting。辅以 episodic、semantic、procedural 与 working memory 等功能视角，该框架阐明了 memory 如何支撑推理、个性化与协作。通过分析 long-term memory、long-context memory、parametric memory modification 与 multi-source memory 四个关键主题，我们突出了进展、挑战与未来工作路径，同时为工业界提供实践 benchmark 与工具指引。

## 参考文献

[1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. 2023. Gpt-4 technical report. arXiv preprint arXiv:2303.08774 (2023).

[2] Muhammad Adnan, Akhil Arunkumar, Gaurav Jain, Prashant J. Nair, Ilya Soloveychik, and Purushotham Kamath. 2024. Keyformer: KV Cache reduction through key tokens selection for Eficient Generative Inference. In Proceedings ofMachine Learning and Systems. https://proceedings. mlsys.org/paper\_files/paper/2024/file/48fecef47b19fe501d27d338b6d52582-Paper-Conference.pdf

[3] Saurabh Agarwal, Bilge Acun, and Basil et al. Hosmer. 2024. CHAI: Clustered Head Attention for Eficient LLM Inference. In ICML. https: //proceedings.mlr.press/v235/agarwal24a.html

[4] Qingyao Ai, Yichen Tang, Changyue Wang, Jianming Long, Weihang Su, and Yiqun Liu. 2025. MemoryBench: A Benchmark for Memory and Continual Learning in LLM Systems. arXiv preprint arXiv:2510.17281 (2025).

[5] Chenxin An, Shansan Gong, Ming Zhong, Xingjian Zhao, Mukai Li, Jun Zhang, Lingpeng Kong, and Xipeng Qiu. 2024. L-Eval: Instituting Standardized Evaluation for Long Context Language Models. In Proceedings ofthe 62nd Annual Meeting ofthe Association for Computational

Linguistics (Volume 1: Long Papers). doi:10.18653/v1/2024.acl-long.776

[6] Shengnan An, Zexiong Ma, Zeqi Lin, Nanning Zheng, Jian-Guang Lou, and Weizhu Chen. 2024. Make Your LLM Fully Utilize the Context. In Advances in Neural Information Processing Systems. https://proceedings.neurips.cc/paper\_files/paper/2024/file/71c3451f6cd6a4f82bb822db25cea4fd-Paper-Conference.pdf

[7] Sotiris Anagnostidis, Dario Pavllo, and Luca et al. Biggio. 2023. Dynamic Context Pruning for Eficient and Interpretable Autoregressive Transformers. In NeurIPS. https://proceedings.neurips.cc/paper\_files/paper/2023/file/cdaac2a02c4fdcae77ba083b110efcc3-Paper-Conference.pdf

[8] Anthropic. 2023. Claude: AI Thinking Partner. https://www.claude.com/. Accessed: 2025-11-01.

[9] Anthropic. 2024. Introducing the Model Context Protocol. https://www.anthropic.com/news/model-context-protocol. Model Context Protocol (MCP) Specification.

[10] Anthropic. 2025. Equipping agents for the real world with Agent Skills. https://claude.com/blog/skills. Accessed: 2025-12-21.

[11] Apple Inc. 2025. Siri: Apple’s Intelligent Voice Assistant. https://www.apple.com/siri/ Accessed: 2025-11-01.

[12] Alan Baddeley. 1988. Cognitive Psychology and Human Memory. Trends in Neurosciences 11, 4 (1988), 176–181.

[13] Sanghwan Bae, Donghyun Kwak, Soyoung Kang, Min Young Lee, Sungdong Kim, Yuin Jeong, Hyeri Kim, Sang-Woo Lee, Woomyoung Park, and Nako Sung. 2022. Keep Me Updated! Memory Management in Long-term Conversations. In Findings ofthe Association for Computational Linguistics: EMNLP 2022. doi:10.18653/v1/2022.findings-emnlp.276

[14] Jinze Bai, Shuai Bai, Shusheng Yang, Shijie Wang, Sinan Tan, Peng Wang, Junyang Lin, Chang Zhou, and Jingren Zhou. 2023. Qwen-VL: A Versatile Vision-Language Model for Understanding, Localization, Text Reading, and Beyond. arXiv (2023). https://arxiv.org/abs/2308.12966

[15] Yushi Bai, Xin Lv, Jiajie Zhang, Hongchang Lyu, Jiankai Tang, Zhidian Huang, Zhengxiao Du, Xiao Liu, Aohan Zeng, Lei Hou, Yuxiao Dong, Jie Tang, and Juanzi Li. 2024. LongBench: A Bilingual, Multitask Benchmark for Long Context Understanding. In Proceedings ofthe 62nd Annual Meeting ofthe Association for Computational Linguistics (Volume 1: Long Papers). doi:10.18653/v1/2024.acl-long.172

[16] Yushi Bai, Shangqing Tu, Jiajie Zhang, Hao Peng, Xiaozhi Wang, Xin Lv, Shulin Cao, Jiazheng Xu, Lei Hou, Yuxiao Dong, Jie Tang, and Juanzi Li. 2025. LongBench v2: Towards Deeper Understanding and Reasoning on Realistic Long-context Multitasks. https://arxiv.org/abs/2412.15204

[17] Vijay Balasubramanian. 2021. Brain power. Proceedings ofthe National Academy ofSciences 118, 32 (2021), e2107022118.

[18] Fazl Barez, Tingchen Fu, Ameya Prabhu, Stephen Casper, Amartya Sanyal, Adel Bibi, Aidan O’Gara, Robert Kirk, Ben Bucknall, Tim Fist, Luke Ong, Philip Torr, Kwok-Yan Lam, Robert Trager, David Krueger, Sören Mindermann, José Hernandez-Orallo, Mor Geva, and Yarin Gal. 2025. Open Problems in Machine Unlearning for AI Safety. https://arxiv.org/abs/2501.04952

[19] Payman Behnam, Yaosheng Fu, Ritchie Zhao, Po-An Tsai, Zhiding Yu, and Alexey Tumanov. 2025. RocketKV: Accelerating Long-Context LLM Inference via Two-Stage KV Cache Compression. In Forty-second International Conference on Machine Learning. https://openreview.net/forum?id= RyOpooIxDF

[20] Ali Behrouz, Peilin Zhong, and Vahab Mirrokni. 2024. Titans: Learning to memorize at test time. arXiv (2024). https://arxiv.org/abs/2501.0066

[21] Vincent-Pierre Berges, Barlas Oğuz, Daniel Haziza, Wen-tau Yih, Luke Zettlemoyer, and Gargi Ghosh. 2024. Memory Layers at Scale. doi:10.48550 arXiv.2412.09764

[22] ByteDance Seed Team. 2025. Doubao-1.5-pro: A High-Eficiency Sparse MoE Multimodal AI Model. https://seed.bytedance.com/en/special/doubao 1\_5\_pro Accessed: 2025-11-01.

[23] Jiaqi Cao, Jiarui Wang, Rubin Wei, Qipeng Guo, Kai Chen, Bowen Zhou, and Zhouhan Lin. 2025. Memory Decoder: A Pretrained, Plug-and-Play Memory for Large Language Models. arXiv preprint arXiv:2508.09874 (2025).

[24] Shuyang Cao and Lu Wang. 2024. AWESOME: GPU Memory-constrained Long Document Summarization using Memory Mechanism and Global Salient Content. In Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers). doi:10.18653/v1/2024.naacl-long.330

[25] Zhiwei Cao, Qian Cao, Yu Lu, Ningxin Peng, Luyang Huang, Shanbo Cheng, and Jinsong Su. 2024. Retaining Key Information under High Compression Ratios: Query-Guided Compressor for LLMs. In Proceedings ofthe ACL. doi:10.18653/v1/2024.acl-long.68

[26] Sungmin Cha, Sungjun Cho, Dasol Hwang, and Moontae Lee. 2025. Towards Robust and Parameter-Eficient Knowledge Unlearning for LLMs. In The Thirteenth International Conference on Learning Representations. https://openreview.net/forum?id=1ExfUpmIW4

[27] Character Technologies, Inc. 2023. Character.AI: A Platform for Creating and Interacting with AI Characters. https://character.ai Accessed: 2025-11-01.

[28] Harrison Chase. 2022. LangChain. https://www.langchain.com

[29] Ding Chen, Simin Niu, Kehang Li, Peng Liu, Xiangping Zheng, Bo Tang, Xinchi Li, Feiyu Xiong, and Zhiyu Li. 2025. HaluMem: Evaluating Hallucinations in Memory Systems of Agents. arXiv preprint arXiv:2511.03506 (2025)

[30] Jiaao Chen and Diyi Yang. 2023. Unlearn What You Want to Forget: Eficient Unlearning for LLMs. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing. 12041–12052

[31] Mingda Chen, Yang Li, Karthik Padthe, et al. 2024. Improving Factuality with Explicit Working Memory. arXiv preprint arXiv:2412.18069 (2024)

[32] Nuo Chen, Hongguang Li, Juhua Huang, Baoyuan Wang, and Jia Li. 2024. Compress to impress: Unleashing the potential of compressive memory in real-world long-term conversations. arXiv preprint arXiv:2402.11975 (2024).

[33] Renze Chen, Zhuofeng Wang, and Beiquan et al. Cao. 2024. ArkVale: Eficient Generative LLM Inference with Recallable Key-Value Eviction. In NeurIPS. https://proceedings.neurips.cc/paper\_files/paper/2024/file/cd4b49379efac6e84186a3fce108c37-Paper-Conference.pdf

[34] Wenhu Chen, Zhihao He, Yu Su, Yunyao Yu, William Wang, and Xifeng Yan. 2021. HybridQA: A Dataset of Multi-Hop Question Answering over Tabular and Textual Data. In Proceedings ofthe International Conference on Learning Representations (ICLR).

[35] Yilong Chen, Guoxia Wang, Junyuan Shang, Shiyao Cui, Zhenyu Zhang, Tingwen Liu, Shuohuan Wang, Yu Sun, Dianhai Yu, and Hua Wu. 2024. NACL: A General and Efective KV Cache Eviction Framework for LLM at Inference Time. In Proceedings ofthe ACL. doi:10.18653/v1/2024.acl long.428

[36] Xin Cheng, Xun Wang, Xingxing Zhang, Tao Ge, Si-Qing Chen, Furu Wei, Huishuai Zhang, and Dongyan Zhao. 2024. xrag: Extreme context compression for retrieval-augmented generation with one token. arXiv preprint arXiv:2405.13792 (2024)

[37] Alexis Chevalier, Alexander Wettig, Anirudh Ajith, and Danqi Chen. 2023. Adapting Language Models to Compress Contexts. In Proceedings of the EMNLP. doi:10.18653/v1/2023.emnlp-main.232

[38] Somnath Basu Roy Chowdhury, Krzysztof Marcin Choromanski, Arijit Sehanobish, Kumar Avinava Dubey, and Snigdha Chaturvedi. 2025. Towards Scalable Exact Machine Unlearning Using Parameter-Eficient Fine-Tuning. In The Thirteenth International Conference on Learning Representations. https://openreview.net/forum?id=oe51Q5Uo37

[39] Tianzhe Chu, Yuexiang Zhai, Jihan Yang, Shengbang Tong, Saining Xie, Dale Schuurmans, Quoc V Le, Sergey Levine, and Yi Ma. 2025. Sft memorizes, rl generalizes: A comparative study of foundation model post-training. arXiv preprint arXiv:2501.17161 (2025).

[40] Yu-Neng Chuang, Tianwei Xing, Chia-Yuan Chang, Zirui Liu, Xun Chen, and Xia Hu. 2024. Learning to Compress Prompt in Natural Language Formats. In Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers). doi:10.18653/v1/2024.naacl-long.429

[41] Tsz Ting Chung, Leyang Cui, Lemao Liu, Xinting Huang, Shuming Shi, and Dit-Yan Yeung. 2024. Selection-p: Self-Supervised Task-Agnostic Prompt Compression for Faithfulness and Transferability. In Findings ofthe Association for Computational Linguistics: EMNLP 2024. doi:10.18653 v1/2024.findings-emnlp.646

[42] Codebuddy AI Inc. 2025. CodeBuddy: AI-Powered Coding Assistant. https://codebuddy.ca/ Accessed: 2025-05-23.

[43] Nelson Cowan. 2001. The magical number 4 in short-term memory: A reconsideration of mental storage capacity. Behavioral and Brain Sciences (2001).

[44] Coze. 2024. Coze: Build your own AI agent. https://www.coze.cn/. Accessed: 2025-04-19.

[45] Bhavana Dalvi Mishra, Oyvind Tafjord, and Peter Clark. 2022. Towards Teachable Reasoning Systems: Using a Dynamic Memory of User Feedback for Continual System Improvement. In Proceedings ofthe 2022 Conference on Empirical Methods in Natural Language Processing. https: //aclanthology.org/2022.emnlp-main.644/

[46] Tri Dao. 2024. FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning. In The Twelfth International Conference on Learning Representations. https://openreview.net/forum?id=mZn2Xyh9Ec

[47] Payel Das, Subhajit Chaudhury, Elliot Nelson, Igor Melnyk, Sarathkrishna Swaminathan, Sihui Dai, Aurélie Lozano, Georgios Kollias, Viji Chenthamarakshan, Jiří Navrátil, Soham Dan, and Pin-Yu Chen. 2024. Larimar: Large Language Models with Episodic Memory Control. In International Conference on Machine Learning. https://arxiv.org/abs/2403.1190

[48] Payel Das, Subhajit Chaudhury, Elliot Nelson, Igor Melnyk, Sarathkrishna Swaminathan, Sihui Dai, Aurélie C. Lozano, Georgios Kollias, Vijil Chenthamarakshan, Jirí Navrátil, Soham Dan, and Pin-Yu Chen. 2024. Larimar: Large Language Models with Episodic Memory Control. In ICML. https://openreview.net/forum?id=t8mt4YrPsq

[49] Ronald L Davis and Yi Zhong. 2017. The biology of forgetting—a perspective. Neuron (2017).

[50] Nicola De Cao, Wilker Aziz, and Ivan Titov. 2021. Editing Factual Knowledge in Language Models. In Proceedings ofthe 2021 Conference on Empirical Methods in Natural Language Processing.

[51] Cyprien de Masson D’Autume, Sebastian Ruder, Lingpeng Kong, et al. 2019. Episodic Memory in Lifelong Language Learning. Advances in Neural Information Processing Systems 32 (2019).

[52] Jingcheng Deng, Zihao Wei, Liang Pang, Hanxing Ding, Huawei Shen, and Xueqi Cheng. 2025. Everything is Editable: Extend Knowledge Editing to Unstructured Data in Large Language Models. In The Thirteenth International Conference on Learning Representations. https://openreview.net/ forum?id=X5rO5VyTgB

[53] Alessio Devoto, Yu Zhao, Simone Scardapane, and Pasquale Minervini. 2024. A Simple and Efective �<sub>2</sub> Norm-Based Strategy for KV Cache Compression. In EMNLP. doi:10.18653/v1/2024.emnlp-main.1027

[54] Shangzhe Di, Zhelun Yu, and Guanghao et al. Zhang. 2025. Streaming Video Question-Answering with In-context Video KV-Cache Retrieval. In ICLR. https://openreview.net/forum?id=8g9fs6mdEG

[55] Chenlu Ding, Jiancan Wu, Yancheng Yuan, Jinda Lu, Kai Zhang, Alex Su, Xiang Wang, and Xiangnan He. 2025. Unified Parameter-Eficien Unlearning for LLMs. In The Thirteenth International Conference on Learning Representations. https://openreview.net/forum?id=zONMuIVCAT

[56] Jiayu Ding, Shuming Ma, Li Dong, Xingxing Zhang, Shaohan Huang, Wenhui Wang, Nanning Zheng, and Furu Wei. 2023. LongNet: Scaling Transformers to 1,000,000,000 Tokens. arXiv preprint arXiv:2307.02486 (2023). https://arxiv.org/abs/2307.02486

[57] Xuanwen Ding, Jie Zhou, Liang Dou, Qin Chen, Yuanbin Wu, Arlene Chen, and Liang He. 2024. Boosting Large Language Models with Continual Learning for Aspect-based Sentiment Analysis. In Findings ofthe EMNLP. doi:10.18653/v1/2024.findings-emnlp.252

[58] Yiran Ding, Li Lyna Zhang, Chengruidong Zhang, Yuanyuan Xu, Ning Shang, Jiahang Xu, Fan Yang, and Mao Yang. 2024. LongRoPE: Extending LLM Context Window Beyond 2 Million Tokens. arXiv preprint arXiv:2402.13753 (2024). https://arxiv.org/abs/2402.13753

[59] Harry Dong, Xinyu Yang, Zhenyu Zhang, Zhangyang Wang, Yuejie Chi, and Beidi Chen. 2024. Get More with LESS: Synthesizing Recurrence with KV Cache Compression for Eficient LLM Inference. In Proceedings of the 41st International Conference on Machine Learning. https: //proceedings.mlr.press/v235/dong24f.html

[60] Qingxiu Dong, Damai Dai, Yifan Song, Jingjing Xu, Zhifang Sui, and Lei Li. 2022. Calibrating Factual Knowledge in Pretrained Language Models In Findings ofthe Association for Computational Linguistics: EMNLP 2022. 5937–5947

[61] Matthijs Douze, Alexandr Guzhva, Chengqi Deng, JefJohnson, Gergely Szilvasy, Pierre-Emmanuel Mazar’e, Maria Lomeli, Lucas Hosseini, and Herv’e J’egou. 2024. The faiss library. arXiv preprint arXiv:2401.08281 (2024).

[62] Danny Driess, Fei Xia, Mehdi SM Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, et al. 2023. PaLM-E: An Embodied Multimodal Language Model. arXiv preprint arXiv:2303.03378 (2023).

[63] Xinya Du, Sha Li, and Heng Ji. 2022. Dynamic Global Memory for Document-level Argument Extraction. In Proceedings ofthe ACL. doi:10.18653 v1/2022.acl-long.361

[64] Yiming Du, Bingbing Wang, Yang He, Bin Liang, Baojun Wang, Zhongyang Li, Lin Gui, Jef Z. Pan, Ruifeng Xu, and Kam-Fai Wong. 2025. MemGuide Intent-Driven Memory Selection for Goal-Oriented Multi-Session LLM Agents. arXiv preprint. doi:10.48550/arXiv.2505.20231 arXiv:2505.20231.

[65] Yiming Du, Hongru Wang, Zhengyi Zhao, et al. 2024. PerLTQA: A Personal Long-term Memory Dataset for Memory Classification, Retrieval, and Synthesis in QA. arXiv preprint arXiv:2402.16288 (2024)

[66] Zhihua Duan and Jialin Wang. 2024. Exploration of LLM Multi-Agent Application Implementation Based on LangGraph+ CrewAI. arXiv preprint arXiv:2411.18241 (2024)

[67] Yadin Dudai, Avi Karni, and Jan Born. 2015. The consolidation and transformation of memory. Neuron (2015).

[68] Ritam Dutt, Kasturi Bhattacharjee, Rashmi Gangadharaiah, Dan Roth, and Carolyn Rose. 2022. PerKGQA: Question answering over personalized knowledge graphs. In Findings ofthe Association for Computational Linguistics: NAACL 2022.

[69] Ronen Eldan and Mark Russinovich. 2024. Who’s Harry Potter? Approximate Unlearning for LLMs. https://openreview.net/forum?id=PDct7vrcvT

[70] Junfeng Fang, Houcheng Jiang, Kun Wang, Yunshan Ma, Jie Shi, Xiang Wang, Xiangnan He, and Tat-Seng Chua. 2025. AlphaEdit: Null-Space Constrained Model Editing for Language Models. In The Thirteenth International Conference on Learning Representations. https://openreview.net/ forum?id=HvSytvg3Jh

[71] Runnan Fang, Yuan Liang, Xiaobin Wang, Jialong Wu, Shuofei Qiao, Pengjun Xie, Fei Huang, Huajun Chen, and Ningyu Zhang. 2025. Memp: Exploring Agent Procedural Memory. arXiv preprint arXiv:2508.06433 (2025)

[72] Weizhi Fei, Xueyan Niu, and Pingyi et al. Zhou. 2024. Extending Context Window of Large Language Models via Semantic Compression. In ACL Findings. doi:10.18653/v1/2024.findings-acl.306

[73] Yujie Feng, Xu Chu, Yongxin Xu, et al. 2024. TaSL: Continual Dialog State Tracking via Task Skill Localization and Consolidation. In Proceedings of the 62nd Annual Meeting ofthe Association for Computational Linguistics. doi:10.18653/v1/2024.acl-long.69

[74] Zafeirios Fountas, Martin A Benfeghoul, Adnan Oomerjee, Fenia Christopoulou, Gerasimos Lampouras, Haitham Bou-Ammar, and Jun Wang. 2024. Human-like Episodic Memory for Infinite Context LLMs. arXiv preprint arXiv:2407.09450 (2024).

[75] Nicholas T Franklin, Kenneth A Norman, Charan Ranganath, Jefrey M Zacks, and Samuel J Gershman. 2020. Structured event memory: A neuro-symbolic model of event cognition. Psychological Review (2020).

[76] Yu Fu, Zefan Cai, Abedelkadir Asi, Wayne Xiong, Yue Dong, and Wen Xiao. 2025. Not All Heads Matter: A Head-Level KV Cache Compression Method with Integrated Retrieval and Reasoning. In International Conference on Learning Representations. https://openreview.net/forum?id=FJFVmeXusW

[77] Suyu Ge, Yunan Zhang, Liyuan Liu, Minjia Zhang, Jiawei Han, and Jianfeng Gao. 2024. Model Tells You What to Discard: Adaptive KV Cache Compression for LLMs. In The Twelfth International Conference on Learning Representations. https://openreview.net/forum?id=uNrFpDPMyo

[78] Yubin Ge, Salvatore Romeo, Jason Cai, Raphael Shu, Monica Sunkara, Yassine Benajiba, and Yi Zhang. 2025. Tremu: Towards Neuro-Symbolic Temporal Reasoning for LLM-Agents with Memory in Multi-Session Dialogues. arXiv preprint arXiv:2502.01630 (2025).

[79] GitHub and OpenAI. 2021. GitHub Copilot: Your AI pair programmer. https://github.com/features/copilot. Accessed May 2025

[80] Marc Glocker, Peter Hönig, Matthias Hirschmanner, and Markus Vincze. 2025. LLM-Empowered Embodied Agent for Memory-Augmented Task Planning in Household Robotics. arXiv preprint arXiv:2504.21716 (2025).

[81] Google AI / DeepMind. 2024. Gemini: Multimodal AI Assistant. https://gemini.google/. Accessed: 2025-11-01.

[82] Xudong Guo, Kaixuan Huang, and Jiale et al. Liu. 2024. Embodied LLM Agents Learn to Cooperate in Organized Teams. arXiv preprint arXiv:2403.12482 (2024)

[83] Yaming Guo, Siyang Guo, Hengshu Zhu, and Ying Sun. 2025. Towards Lifelong Model Editing via Simulating Ideal Editor. In Forty-second International Conference on Machine Learning. https://openreview.net/forum?id=VdEG08ZJCH

[84] Bernal Jiménez Gutiérrez, Yiheng Shu, Yu Gu, et al. 2024. HippoRAG: Neurobiologically Inspired Long-term Memory for Large Language Models. In NeurIPS.

[85] Bernal Jiménez Gutiérrez, Yiheng Shu, Weijian Qi, Sizhe Zhou, and Yu Su. 2025. From RAG to Memory: Non-Parametric Continual Learning for Large Language Models. arXiv preprint arXiv:2502.14802 (2025).

[86] Chi Han, Qifan Wang, Hao Peng, Wenhan Xiong, Yu Chen, Heng Ji, and Sinong Wang. 2024. LM-Infinite: Zero-Shot Extreme Length Generalization for Large Language Models. In Proceedings ofthe NAACL-HLT. doi:10.18653/v1/2024.naacl-long.222

[87] Kaiqiao Han, Tianqing Fang, Zhaowei Wang, Yangqiu Song, and Mark Steedman. [n. d.]. Concept-Reversed Winograd Schema Challenge: Evaluating and Improving Robust Reasoning in Large Language Models via Abstraction. In Proceedings of the 2025 Conference of the Nations of the Americas

Chapter ofthe Association for Computational Linguistics: Human Language Technologies (Volume 2: Short Papers). Association for Computational Linguistics.

[88] Yongchang Hao, Mengyao Zhai, Hossein Hajimirsadeghi, Sepidehsadat Hosseini, and Frederick Tung. 2025. Radar: Fast Long-Context Decoding for Any Transformer. In The Thirteenth International Conference on Learning Representations. https://openreview.net/forum?id=ZTpWOwMrzQ

[89] Shirley Anugrah Hayati, Dongyeop Kang, Qingxiaoyang Zhu, Weiyan Shi, and Zhou Yu. 2020. INSPIRED: Toward Sociable Recommendation Dialog Systems. In Proceedings ofthe EMNLP. doi:10.18653/v1/2020.emnlp-main.654

[90] Bo He, Hengduo Li, Young Kyun Jang, Menglin Jia, Xuefei Cao, Ashish Shah, Abhinav Shrivastava, and Ser-Nam Lim. 2024. Ma-lmm: Memoryaugmented large multimodal model for long-term video understanding. In Proceedings ofthe IEEE/CVF Conference on Computer Vision and Pattern Recognition. 13504–13514.

[91] Junqing He, Kunhao Pan, Xiaoqun Dong, Zhuoyang Song, LiuYiBo LiuYiBo, Qianguosun Qianguosun, Yuxin Liang, Hao Wang, Enming Zhang, and Jiaxing Zhang. 2024. Never Lost in the Middle: Mastering Long-Context Question Answering with Position-Agnostic Decompositional Training. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers). doi:10.18653/v1/2024.acl-long.736

[92] Yang He, Ruijie Fang, Isil Dillig, and Yuepeng Wang. 2025. Graphiti: Bridging Graph and Relational Database Queries. arXiv preprint arXiv:2504.03182 (2025).

[93] Yefei He, Luoming Zhang, and Weijia et al. Wu. 2024. ZipCache: Accurate and Eficient KV Cache Quantization with Salient Token Identification. In NeurIPS. https://proceedings.neurips.cc/paper\_files/paper/2024/file/7e57131fdeb815764434b65162c88895-Paper-Conference.pdf

[94] Zihong He, Weizhe Lin, Hao Zheng, Fan Zhang, Matt W. Jones, Laurence Aitchison, Xuhai Xu, Miao Liu, Per Ola Kristensson, and Junxiao Shen. 2024. Human-inspired Perspectives: A Survey on AI Long-term Memory. arXiv (2024). https://arxiv.org/abs/2411.00489

[95] Xanh Ho, Anh-Khoa Nguyen Duong, Saku Sugawara, and Akiko Aizawa. 2020. Constructing a multi-hop qa dataset for comprehensive evaluation of reasoning steps. arXiv preprint arXiv:2011.01060 (2020)

[96] Ruixin Hong, Hongming Zhang, Xiaoman Pan, Dong Yu, and Changshui Zhang. 2024. Abstraction-of-Thought Makes Language Models Better Reasoners. In Findings of the Association for Computational Linguistics: EMNLP 2024. Association for Computational Linguistics. doi:10.18653/v1 2024.findings-emnlp.110

[97] Wenyi Hong, Weihan Wang, Qingsong Lv, Jiazheng Xu, Wenmeng Yu, Junhui Ji, Yan Wang, Zihan Wang, Yuxuan Zhang, Juanzi Li, Bin Xu, Yuxiao Dong, Ming Ding, and Jie Tang. 2023. CogAgent: A Visual Language Model for GUI Agents. arXiv preprint arXiv:2312.08914 (2023). https://arxiv.org/abs/2312.08914

[98] Coleman Hooper, Sehoon Kim, Hiva Mohammadzadeh, Michael W. Mahoney, Yakun Sophia Shao, Kurt Keutzer, and Amir Gholami. 2024. KVQuant: Towards 10 Million Context Length LLM Inference with KV Cache Quantization. In Advances in Neural Information Processing Systems.

[99] Lishuai Hou, Zixiong Wang, Gaoyang Liu, Chen Wang, Wei Liu, and Kai Peng. 2025. Decoupling Memories, Muting Neurons: Towards Practical Machine Unlearning for Large Language Models. In Findings ofthe Association for Computational Linguistics: ACL 2025, Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and Mohammad Taher Pilehvar (Eds.). Association for Computational Linguistics, Vienna, Austria, 13978–13999. doi:10.18653/v1/2025.findings-acl.719

[100] Yuki Hou, Haruki Tamoto, and Homei Miyashita. 2024. "My agent understands me better": Integrating Dynamic Human-like Memory Recall and Consolidation in LLM-Based Agents. In CHI Extended Abstracts. doi:10.1145/3613905.3650839

[101] Zhijian Hou, Lei Ji, Difei Gao, Wanjun Zhong, Kun Yan, Chao Li, Wing-Kwong Chan, Chong-Wah Ngo, Nan Duan, and Mike Zheng Shou. 2023. Groundnlq@ ego4d natural language queries challenge 2023. arXiv (2023). https://arxiv.org/abs/2306.15255

[102] Chenxu Hu, Jie Fu, Chenzhuang Du, Simian Luo, Junbo Zhao, and Hang Zhao. 2023. ChatDB: Augmenting LLMs with Databases as Their Symboli Memory. https://arxiv.org/abs/2306.0390

[103] Yuanzhe Hu, Yu Wang, and Julian McAuley. 2025. Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions. arXiv preprint arXiv:2507.05257 (2025).

[104] Luyang Huang, Shuyang Cao, Nikolaus Parulian, Heng Ji, and Lu Wang. 2021. Eficient Attentions for Long Document Summarization. In Proceedings ofthe 2021 Conference ofthe North American Chapter ofthe Association for Computational Linguistics: Human Language Technologies. doi:10.18653/v1/2021.naacl-main.112

[105] Qiushi Huang, Shuai Fu, Xubo Liu, Wenwu Wang, Tom Ko, Yu Zhang, and Lilian Tang. 2023. Learning Retrieval Augmentation for Personalized Dialogue Generation. In Proceedings ofthe 2023 Conference on Empirical Methods in Natural Language Processing. doi:10.18653/v1/2023.emnlpmain.154

[106] Wenyu Huang, Pavlos Vougiouklis, Mirella Lapata, and Jef Z. Pan. 2025. Masking in Multi-hop QA: An Analysis of How Language Models Perform with Context Permutation. arXiv:2505.11754 [cs.CL] https://arxiv.org/abs/2505.11754

[107] Xiusheng Huang, Yequan Wang, Jun Zhao, and Kang Liu. 2024. Commonsense Knowledge Editing Based on Free-Text in LLMs. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing. 14870–14880.

[108] Yunpeng Huang, Jingwei Xu, Junyu Lai, Zixu Jiang, Taolue Chen, Zenan Li, Yuan Yao, Xiaoxing Ma, Lijuan Yang, Hao Chen, et al. 2023. Advancing transformer architecture in long-context large language models: A comprehensive survey. arXiv preprint arXiv:2311.12351 (2023).

[109] Huawei Technologies Co., Ltd. 2025. Xiaoyi: Huawei’s AI Smart Assistant. https://xiaoyi.huawei.com/chat/ Accessed: 2025-11-01.

[110] B. Ian Hutchins, Xin Yuan, and James M. et al. Anderson. 2016. Relative Citation Ratio (RCR): A New Metric That Uses Citation Rates to Measure Influence at the Article Level. PLOS Biology (2016). doi:10.1371/journal.pbio.1002541

[111] Anysphere Inc. 2024. Cursor: An AI-Powered Code Editor. https://www.cursor.sh Version 0.x, Accessed: 2025-11-01.

[112] LangChain Inc. 2025. LangGraph: Build Resilient Language Agents as Graphs. https://github.com/langchain-ai/langgraph

[113] Gautier Izacard, Mathilde Caron, Lucas Hosseini, Sebastian Riedel, Piotr Bojanowski, Armand Joulin, and Edouard Grave. 2021. Unsupervised dense information retrieval with contrastive learning. arXiv (2021). https://arxiv.org/abs/2112.09118

[114] Jihyoung Jang, Minseong Boo, and Hyounghun Kim. 2023. Conversation Chronicles: Towards Diverse Temporal and Relational Dynamics in Multi-session Conversations. arXiv preprint arXiv:2310.13420 (2023).

[115] Joel Jang, Dongkeun Yoon, Sohee Yang, Sungmin Cha, Moontae Lee, Lajanugen Logeswaran, and Minjoon Seo. 2023. Knowledge Unlearning for Mitigating Privacy Risks in Language Models. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), Anna Rogers, Jordan Boyd-Graber, and Naoaki Okazaki (Eds.). Association for Computational Linguistics, Toronto, Canada, 14389–14408. doi:10.18653/v1/2023.acl-long.805

[116] Yunah Jang, Kang-il Lee, Hyunkyung Bae, Hwanhee Lee, and Kyomin Jung. 2024. IterCQR: Iterative Conversational Query Reformulation with Retrieval Guidance. In Proceedings ofthe 2024 Conference ofthe North American Chapter ofthe Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers). doi:10.18653/v1/2024.naacl-long.449

[117] Wonje Jeung, Sangyeon Yoon, and Albert No. 2025. SEPS: A Separability Measure for Robust Unlearning in LLMs. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing, Christos Christodoulopoulos, Tanmoy Chakraborty, Carolyn Rose, and Violet Peng (Eds.). Association for Computational Linguistics, Suzhou, China, 5556–5587. doi:10.18653/v1/2025.emnlp-main.283

[118] Jiabao Ji, Yujian Liu, Yang Zhang, et al. 2024. Reversing the Forget-Retain Objectives: An Eficient LLM Unlearning Framework from Logit Diference. Advances in Neural Information Processing Systems 37 (2024).

[119] Jinghan Jia, Jiancheng Liu, Yihua Zhang, Parikshit Ram, Nathalie Baracaldo, and Sijia Liu. 2024. WAGLE: Strategic Weight Attribution for Efective and Modular Unlearning in Large Language Models. In NeurIPS

[120] Jinghan Jia, Yihua Zhang, Yimeng Zhang, et al. 2024. SOUL: Unlocking the Power of Second-Order Optimization for LLM Unlearning. In Proceedings ofthe 2024 Conference on Empirical Methods in Natural Language Processing. doi:10.18653/v1/2024.emnlp-main.245

[121] Bowen Jiang, Yuan Yuan, Maohao Shen, Zhuoqun Hao, Zhangchen Xu, Zichen Chen, Zijun Liu, Anirudh Ravi Vijjini, Jiaming He, et al. 2025 PersonaMem-v2: Towards Personalized Intelligence via Learning Implicit User Personas and Agentic Memory. arXiv preprint arXiv:2512.06688 (2025).

[122] Houcheng Jiang, Junfeng Fang, Ningyu Zhang, Mingyang Wan, Guojun Ma, Xiang Wang, Xiangnan He, and Tat-Seng Chua. 2025. AnyEdit: Edit Any Knowledge Encoded in Language Models. In Forty-second International Conference on Machine Learning. https://openreview.net/forum?id= aJIoBur0Ef

[123] Haoyun Jiang, Haolin li, jianwei zhang, Fei Huang, Qiang Hu, Minmin Sun, Shuai Xiao, Yong Li, Junyang Lin, and Jiangchao Yao. 2025. CateKV: On Sequential Consistency for Long-Context LLM Inference Acceleration. In Forty-second International Conference on Machine Learning. https: //openreview.net/forum?id=u7dlwgKstN

[124] Huiqiang Jiang, Qianhui Wu, Chin-Yew Lin, Yuqing Yang, and Lili Qiu. 2023. LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing. doi:10.18653/v1/2023.emnlp-main.825

[125] Huiqiang Jiang, Qianhui Wu, Xufang Luo, Dongsheng Li, Chin-Yew Lin, Yuqing Yang, and Lili Qiu. 2024. LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers). doi:10.18653/v1/2024.acl-long.91

[126] Xun Jiang, Feng Li, Han Zhao, Jiaying Wang, Jun Shao, Shihao Xu, Shu Zhang, Weiling Chen, Xavier Tang, Yize Chen, Mengyue Wu, Weizhi Ma Mengdi Wang, and Tianqiao Chen. 2024. Long Term Memory: The Foundation of AI Self-Evolution. arXiv (2024). https://arxiv.org/abs/2410.15665

[127] Yikun Jiang, Huanyu Wang, and Lei et al. Xie. 2024. D-LLM: A Token Adaptive Computing Resource Allocation Strategy for Large Language Models. In NeurIPS. https://proceedings.neurips.cc/paper\_files/paper/2024/file/03469b1a66e351b18272be23baf3b809-Paper-Conference.pdf

[128] Yuxin Jiang, Yufei Wang, Chuhan Wu, Wanjun Zhong, Xingshan Zeng, Jiahui Gao, Liangyou Li, Xin Jiang, Lifeng Shang, Ruiming Tang, Qun Liu, and Wei Wang. 2024. Learning to Edit: Aligning LLMs with Knowledge Editing. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), Lun-Wei Ku, Andre Martins, and Vivek Srikumar (Eds.). Association for Computational Linguistics, Bangkok, Thailand, 4689–4705. doi:10.18653/v1/2024.acl-long.258

[129] ZhengbaoJiang, Frank Xu, Luyu Gao, Zhiqing Sun, Qian Liu,Jane Dwivedi-Yu, Yiming Yang,Jamie Callan, and Graham Neubig. 2023. Active Retrieval Augmented Generation. In Proceedings ofthe 2023 Conference on Empirical Methods in Natural Language Processing. doi:10.18653/v1/2023.emnlp main.495

[130] Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik R Narasimhan. 2024. SWE-bench: Can Language Models Resolve Real-world GitHub Issues?. In ICLR. https://openreview.net/forum?id=VTF8yNQM66

[131] Bowen Jin, Jinsung Yoon, Jiawei Han, and Sercan O Arik. 2025. Long-Context LLMs Meet RAG: Overcoming Challenges for Long Inputs in RAG. In The Thirteenth International Conference on Learning Representations. https://openreview.net/forum?id=oU3tpaR8fm

[132] Mingyu Jin, Weidi Luo, and Sitao et al. Cheng. 2024. Disentangling Memory and Reasoning Ability in Large Language Models. arXiv preprint arXiv:2411.13504 (2024)

[133] Zhuoran Jin, Pengfei Cao, Chenhao Wang, Zhitao He, Hongbang Yuan, Jiachun Li, Yubo Chen, Kang Liu, and Jun Zhao. 2024. RWKU: Benchmarking Real-World Knowledge Unlearning for Large Language Models. In NeurIPS Datasets and Benchmarks Track. https://openreview.net/forum?id= wOmtZ5FgMH

[134] Mandar Joshi, Eunsol Choi, Daniel Weld, and Luke Zettlemoyer. 2017. TriviaQA: A Large Scale Distantly Supervised Challenge Dataset for Reading Comprehension. In Proceedings ofthe 55th Annual Meeting ofthe Association for Computational Linguistics (Volume 1: Long Papers) doi:10.18653/v1/P17-1147

[135] Gregory Kamradt. 2023. Needle In A Haystack - Pressure Testing LLMs. https://github.com/gkamradt/LLMTest\_NeedleInAHaystack

[136] Christopher Kiley and Colleen M Parks. 2022. Mechanisms of memory updating: State dependency vs. reconsolidation. Journal of cognition (2022).

[137] Jiho Kim, Woosog Chay, Hyeonji Hwang, Daeun Kyung, Hyunseung Chung, Eunbyeol Cho, Yohan Jo, and Edward Choi. 2024. DialSim: A Real-Tim Simulator for Evaluating Long-Term Multi-Party Dialogue Understanding of Conversational Agents. arXiv preprint arXiv:2406.13144 (2024)

[138] Minsoo Kim, Kyuhong Shim, Jungwook Choi, and Simyung Chang. 2024. InfiniPot: Infinite Context Processing on Memory-Constrained LLMs. In EMNLP. doi:10.18653/v1/2024.emnlp-main.897

[139] Seo Hyun Kim, Keummin Ka, Yohan Jo, Seung-won Hwang, Dongha Lee, and Jinyoung Yeo. 2024. Ever-Evolving Memory by Blending and Refining the Past. arXiv (2024). https://arxiv.org/abs/2403.04787

[140] kingjulio8238. 2025. Memary. https://github.com/kingjulio8238/Memary

[141] James Kirkpatrick, Razvan Pascanu, Neil Rabinowitz, et al. 2017. Overcoming Catastrophic Forgetting in Neural Networks. Proceedings ofthe National Academy ofSciences 114, 13 (2017)

[142] Hideo Kobayashi, Wuwei Lan, Peng Shi, Shuaichen Chang, Jiang Guo, Henghui Zhu, Zhiguo Wang, and Patrick Ng. 2025. You Only Read Once (YORO): Learning to Internalize Database Knowledge for Text-to-SQL. In Proceedings ofNAACL-HLT (Long Papers). 1889–1901. https: //aclanthology.org/2025.naacl-long.94

[143] Tom’aš Kočisk’y, Jonathan Schwarz, Phil Blunsom, Chris Dyer, Karl Moritz Hermann, G’abor Melis, and Edward Grefenstette. 2018. The NarrativeQA Reading Comprehension Challenge. Transactions ofthe Association for Computational Linguistics (2018). doi:10.1162/tacl\_a\_00023

[144] Dharshan Kumaran, Demis Hassabis, and James L McClelland. 2016. What learning systems do intelligent agents need? Complementary learning systems theory updated. Trends in Cognitive Sciences (2016).

[145] Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh, Chris Alberti, Danielle Epstein, Illia Polosukhin, Jacob Devlin, Kenton Lee, et al. 2019. Natural questions: a benchmark for question answering research. Transactions ofthe Association for Computational Linguistics (2019).

[146] Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E. Gonzalez, Hao Zhang, and Ion Stoica. 2023. Eficient Memory Management for Large Language Model Serving with PagedAttention. In Proceedings ofthe ACM SIGOPS 29th Symposium on Operating Systems Principles.

[147] Jack Lanchantin, Shubham Toshniwal, and Jason et al. Weston. 2023. Learning to Reason and Memorize with Self-Notes. NeurIPS (2023).

[148] Dongkyu Lee, Chandana Satya Prakash, Jack FitzGerald, and Jens Lehmann. 2024. MATTER: Memory-Augmented Transformer Using Heterogeneous Knowledge Sources. In Findings ofthe ACL. https://aclanthology.org/2024.findings-acl.953

[149] Kuang-Huei Lee, Xinyun Chen, Hiroki Furuta, John Canny, and Ian Fischer. 2024. A Human-Inspired Reading Agent with Gist Memory of Very Long Contexts. In Proceedings ofthe 41st International Conference on Machine Learning. https://proceedings.mlr.press/v235/lee24c.htm

[150] Mingcong Lei, Yiming Zhao, Ge Wang, Zhixin Mai, Shuguang Cui, Yatong Han, and Jinke Ren. 2025. STMA: A Spatio-Temporal Memory Agent for Long-Horizon Embodied Task Planning. arXiv (2025)

[151] Yaniv Leviathan, Matan Kalman, and Yossi Matias. 2025. Selective Attention Improves Transformer. In ICLR. https://openreview.net/forum?id= v0FzmPCd1e

[152] Omer Levy, Minjoon Seo, Eunsol Choi, et al. 2017. Zero-shot Relation Extraction via Reading Comprehension. In Proceedings ofCoNLL.

[153] Hao Li, Chenghao Yang, An Zhang, Yang Deng, Xiang Wang, and Tat-Seng Chua. 2024. Hello again! llm-powered personalized agent for long-term dialogue. arXiv preprint arXiv:2406.05925 (2024).

[154] Jiaqi Li, Mengmeng Wang, Zilong Zheng, and Muhan Zhang. 2024. LooGLE: Can Long-Context Language Models Understand Long Contexts?. In ACL. 16304–16333. doi:10.18653/v1/2024.acl-long.859

[155] Ji-An Li, Corey Zhou, Marcus Benna, and Marcelo G Mattar. 2024. Linking In-Context Learning in Transformers to Human Episodic Memory. Advances in Neural Information Processing Systems 37 (2024), 6180–6212.

[156] Nathaniel Li, Alexander Pan, Anjali Gopal, Summer Yue, Daniel Berrios, Alice Gatti, Justin D Li, Ann-Kathrin Dombrowski, Shashwat Goel, Gabriel Mukobi, et al. 2024. The WMDP benchmark: measuring and reducing malicious use with unlearning. In Proceedings ofthe 41st International Conference on Machine Learning. 28525–28550.

[157] Na Li, Chunyi Zhou, Yansong Gao, Hui Chen, Zhi Zhang, Boyu Kuang, and Anmin Fu. 2025. Machine Unlearning: Taxonomy, Metrics, Applications, Challenges, and Prospects. IEEE Transactions on Neural Networks and Learning Systems (2025). doi:10.1109/TNNLS.2025.3530988

[158] Shilong Li, Yancheng He, Hangyu Guo, Xingyuan Bu, Ge Bai, Jie Liu, Jiaheng Liu, Xingwei Qu, Yangguang Li, Wanli Ouyang, Wenbo Su, and Bo Zheng. 2024. GraphReader: Building Graph-based Agent to Enhance Long-Context Abilities of Large Language Models. In Findings ofthe Association for Computational Linguistics: EMNLP 2024. doi:10.18653/v1/2024.findings-emnlp.746

[159] Xiaopeng Li, Shasha Li, Shezheng Song, Jing Yang, Jun Ma, and Jie Yu. 2024. Pmet: Precise model editing in a transformer. In Proceedings ofthe AAAI Conference on Artificial Intelligence, Vol. 38. 18564–18572.

[160] Xiaonan Li and Xipeng Qiu. 2023. MoT: Memory-of-Thought Enables ChatGPT to Self-Improve. In Proceedings ofthe 2023 Conference on Empirical Methods in Natural Language Processing. doi:10.18653/v1/2023.emnlp-main.392

[161] Xingxuan Li, Ruochen Zhao, Yew Ken Chia, Bosheng Ding, Shafiq Joty, Soujanya Poria, and Lidong Bing. 2024. Chain-of-Knowledge: Grounding Large Language Models via Dynamic Knowledge Adapting over Heterogeneous Sources. In International Conference on Learning Representations. https://arxiv.org/abs/2305.13269

[162] Yucheng Li, Bo Dong, and Frank et al. Guerin. 2023. Compressing Context to Enhance Inference Eficiency of Large Language Models. In EMNLP. doi:10.18653/v1/2023.emnlp-main.391

[163] Yuhong Li, Yingbing Huang, Bowen Yang, Bharat Venkitesh, Acyr Locatelli, Hanchen Ye, Tianle Cai, Patrick Lewis, and Deming Chen. 2024. SnapKV: LLM Knows What You are Looking for Before Generation. In Advances in Neural Information Processing Systems, Vol. 37. 22947–22970. https://proceedings.neurips.cc/paper\_files/paper/2024/file/28ab418242603e0f7323e54185d19bde-Paper-Conference.pdf

[164] Yongqi Li, Wenjie Wang, Leigang Qu, Liqiang Nie, Wenjie Li, and Tat-Seng Chua. 2024. Generative Cross-Modal Retrieval: Memorizing Images in Multimodal Language Models for Retrieval and Beyond. In Proceedings of the ACL. doi:10.18653/v1/2024.acl-long.639

[165] Zhuoqun Li, Xuanang Chen, Haiyang Yu, Hongyu Lin, Yaojie Lu, Qiaoyu Tang, Fei Huang, Xianpei Han, Le Sun, and Yongbin Li. 2024. Structrag: Boosting knowledge intensive reasoning of LLMs via inference-time hybrid information structurization. In The Thirteenth International Conference on Learning Representations.

[166] Zhuowan Li, Cheng Li, Mingyang Zhang, Qiaozhu Mei, and Michael Bendersky. 2024. Retrieval Augmented Generation or Long-Context LLMs? A Comprehensive Study and Hybrid Approach. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing: Industry Track. doi:10.18653/v1/2024.emnlp-industry.66

[167] Zongqian Li, Yinhong Liu, Yixuan Su, and Nigel Collier. 2024. Prompt compression for large language models: A survey. arXiv preprint arXiv:2410.12388 (2024).

[168] Zhiyu Li, Shichao Song, Hanyu Wang, Simin Niu, Ding Chen, Jiawei Yang, Chenyang Xi, Huayi Lai, Jihao Zhao, Yezhaohui Wang, et al. 2025. MemOS: An Operating System for Memory-Augmented Generation (MAG) in Large Language Models. arXiv preprint arXiv:2505.22101 (2025).

[169] Zaijing Li, Yuquan Xie, Rui Shao, et al. 2024. Optimus-1: Hybrid Multimodal Memory Empowered Agents Excel in Long-horizon Tasks. arXiv preprint arXiv:2408.03615 (2024).

[170] Greg Linden, Brent Smith, and Jeremy York. 2003. Amazon.com Recommendations: Item-to-Item Collaborative Filtering. IEEE Internet Computing 7, 1 (2003), 76–80.

[171] Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, et al. 2024. Deepseek-v3 technical report. arXiv preprint arXiv:2412.19437 (2024).

[172] Akide Liu, Jing Liu, and Zizheng et al. Pan. 2024. MiniCache: KV Cache Compression in Depth Dimension for Large Language Models. In NeurIPS. https://proceedings.neurips.cc/paper\_files/paper/2024/file/fd0705710bf01b88a60a3d479ea341d9-Paper-Conference.pdf

[173] Chris Liu, Yaxuan Wang, Jefrey Flanigan, et al. 2024. Large Language Model Unlearning via Embedding-corrupted Prompts. Advances in Neural Information Processing Systems 37 (2024)

[174] Di Liu, Meng Chen, Baotong Lu, Huiqiang Jiang, Zhenhua Han, Qianxi Zhang, Qi Chen, Chengruidong Zhang, Bailu Ding, Kai Zhang, Chen Chen, Fan Yang, Yuqing Yang, and Lili Qiu. 2024. RetrievalAttention: Accelerating Long-Context LLM Inference via Vector Retrieval. https: //arxiv.org/abs/2409.10516

[175] Jerry Liu. 2022. LlamaIndex. https://www.llamaindex.ai

[176] Junyi Liu, Liangzhi Li, and Tong et al. Xiang. 2023. TCRA-LLM: Token Compression Retrieval Augmented Large Language Model for Inference Cost Reduction. In EMNLP Findings. doi:10.18653/v1/2023.findings-emnlp.655

[177] Jiahong Liu, Zexuan Qiu, Zhongyang Li, Quanyu Dai, Jieming Zhu, Minda Hu, Menglin Yang, and Irwin King. 2025. A Survey of Personalized Large Language Models: Progress and Future Directions. arXiv preprint arXiv:2502.11528 (2025).

[178] Minqian Liu, Shiyu Chang, and Lifu Huang. 2022. Incremental prompting: Episodic memory prompt for lifelong event detection. arXiv (2022) https://arxiv.org/abs/2204.07275

[179] Nelson F Liu, Kevin Lin, John Hewitt, et al. 2024. Lost in the Middle: How Language Models Use Long Contexts. Transactions of the Association for Computational Linguistics 12 (2024)

[180] Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. 2024. Lost in the Middle: How Language Models Use Long Contexts. Transactions ofthe Association for Computational Linguistics (2024). doi:10.1162/tacl\_a\_00638

[181] Shuai Liu, Hyundong Cho, Marjorie Freedman, Xuezhe Ma, and Jonathan May. 2023. RECAP: Retrieval-Enhanced Context-Aware Prefix Encoder for Personalized Dialogue Response Generation. In Proceedings ofthe 61st Annual Meeting ofthe Association for Computational Linguistics (Volume 1: Long Papers). doi:10.18653/v1/2023.acl-long.468

[182] Shuai Liu, Hyundong J Cho, Marjorie Freedman, Xuezhe Ma, and Jonathan May. 2023. RECAP: retrieval-enhanced context-aware prefix encoder for personalized dialogue response generation. arXiv preprint arXiv:2306.07206 (2023)

[183] WenTao Liu, Ruohua Zhang, and Aimin et al. Zhou. 2025. Echo: A Large Language Model with Temporal Episodic Memory. arXiv preprint arXiv:2502.16090 (2025)

[184] Zichang Liu, Aditya Desai, Fangshuo Liao, Weitao Wang, Victor Xie, Zhaozhuo Xu, Anastasios Kyrillidis, and Anshumali Shrivastava. 2023. Scissorhands: Exploiting the Persistence of Importance Hypothesis for LLM KV Cache Compression at Test Time. In NeurIPS. https://openreview. net/forum?id=JZfg6wGi6g

[185] Zheyuan Liu, Guangyao Dou, Zhaoxuan Tan, Yijun Tian, and Meng Jiang. 2024. Towards Safer Large Language Models through Machine Unlearning In Findings ofthe Association for Computational Linguistics: ACL 2024. 1817–1829.

[186] Zhenghao Liu, Chenyan Xiong, Yuanhuiyi Lv, Zhiyuan Liu, and Ge Yu. 2023. Universal Vision-Language Dense Retrieval: Learning A Unified Representation Space for Multi-Modal Retrieval. In Proceedings ofICLR.

[187] Ziyao Liu, Huanyi Ye, Chen Chen, Yongsen Zheng, and Kwok-Yan Lam. 2025. Threats, Attacks, and Defenses in Machine Unlearning: A Survey. IEEE Open Journal ofthe Computer Society (2025). doi:10.1109/OJCS.2025.3543483

[188] Zirui Liu, Jiayi Yuan, Hongye Jin, Shaochen Zhong, Zhaozhuo Xu, Vladimir Braverman, Beidi Chen, and Xia Hu. 2024. KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache. In International Conference on Machine Learning. https://proceedings.mlr.press/v235/liu24bz.html

[189] Lin Long, Yichen He, Wentao Ye, Yiyuan Pan, Yuan Lin, Hang Li, Junbo Zhao, and Wei Li. 2025. Seeing, Listening, Remembering, and Reasoning: A Multimodal Agent with Long-Term Memory. arXiv:2508.09736 [cs.CV] https://arxiv.org/abs/2508.09736

[190] Junru Lu, Siyu An, and Mingbao et al. Lin. 2023. Memochat: Tuning LLMs to Use Memos for Consistent Long-range Open-domain Conversation. arXiv preprint arXiv:2308.08239 (2023).

[191] Luka, Inc. 2025. Replika: The AI companion who cares. https://replika.com/. Accessed: 2025-05-14.

[192] Elias Lumer, Anmol Gulati, Vamse Kumar Subbiah, Pradeep Honaganahalli Basavaraju, and James A Burke. 2025. MemTool: Optimizing Short-Term Memory Management for Dynamic Tool Calling in LLM Agent Multi-Turn Conversations. arXiv preprint arXiv:2507.21428 (2025).

[193] Kun Luo, Zheng Liu, Shitao Xiao, Tong Zhou, Yubo Chen, Jun Zhao, and Kang Liu. 2024. Landmark Embedding: A Chunking-Free Embedding Method For Retrieval Augmented Long-Context Large Language Models. In Proceedings ofthe 62nd Annual Meeting ofthe Association for Computational Linguistics (Volume 1: Long Papers). doi:10.18653/v1/2024.acl-long.180

[194] Zhiyuan Ma, Jianjun Li, Guohui Li, and Yongjing Cheng. 2022. UniTranSeR: A Unified Transformer Semantic Representation Framework for Multimodal Task-Oriented Dialog System. In Proceedings ofthe 60th Annual Meeting ofthe Association for Computational Linguistics (Volume 1: Long Papers). doi:10.18653/v1/2022.acl-long.9

[195] Aru Maekawa, Hidetaka Kamigaito, Kotaro Funakoshi, and Manabu Okumura. 2023. Generative replay inspired by hippocampal memory indexing for continual language learning. In Proceedings ofthe 17th Conference ofthe European Chapter ofthe Association for Computational Linguistics.

[196] Adyasha Maharana, Dong-Ho Lee, Sergey Tulyakov, et al. 2024. Evaluating Very Long-term Conversational Memory of LLM Agents. arXiv preprint arXiv:2402.17753 (2024).

[197] Pratyush Maini, Zhili Feng, Avi Schwarzschild, Zachary Chase Lipton, and J Zico Kolter. 2024. TOFU: A Task of Fictitious Unlearning for LLMs. In First Conference on Language Modeling. https://openreview.net/forum?id=B41hNBoWLo

[198] Karttikeya Mangalam, Raiymbek Akshulakov, and Jitendra Malik. 2023. EgoSchema: A Diagnostic Benchmark for Very Long-form Video Language Understanding. In Advances in Neural Information Processing Systems (NeurIPS).

[199] James L McClelland, Bruce L McNaughton, and Randall C O’Reilly. 1995. Why there are complementary learning systems in the hippocampus and neocortex: Insights from the successes and failures of connectionist models of learning and memory. Psychological Review (1995).

[200] Sanket Vaibhav Mehta, Jai Gupta, Yi Tay, Mostafa Dehghani, Vinh Q Tran, Jinfeng Rao, Marc Najork, Emma Strubell, and Donald Metzler. 2022. DSI++: Updating transformer memory with new documents. arXiv preprint arXiv:2212.09744 (2022)

[201] Daniel Mela, Aitor González-Agirre, Javier Hernando, and Marta Villegas. 2024. Mass-Editing Memory with Attention in Transformers: A cross-lingual exploration of knowledge. In Findings ofthe Association for Computational Linguistics: ACL 2024. 5831–5847.

[202] memodb io. 2025. Memobase: Profile-Based Long-Term Memory for AI Applications. https://github.com/memodb-io/memobase

[203] Kevin Meng, David Bau, Alex Andonian, et al. 2022. Locating and Editing Factual Associations in GPT. Advances in Neural Information Processing Systems 35 (2022)

[204] Kevin Meng, Arnab Sen Sharma, Alex Andonian, et al. 2022. Mass-editing Memory in a Transformer. arXiv preprint arXiv:2210.07229 (2022)

[205] Kevin Meng, Arnab Sen Sharma, Alex J Andonian, Yonatan Belinkov, and David Bau. 2023. Mass-Editing Memory in a Transformer. In The Eleventh International Conference on Learning Representations. https://openreview.net/forum?id=MkbcAHIYgyS

[206] Stephen Merity, Caiming Xiong, James Bradbury, and Richard Socher. 2017. Pointer Sentinel Mixture Models. In International Conference on Learning Representations. https://openreview.net/forum?id=Byj72udxe

[207] Xin Miao, Yongqi Li, Shen Zhou, and Tieyun Qian. 2024. Episodic Memory Retrieval from LLMs: A Neuromorphic Mechanism to Generate Commonsense Counterfactuals for Relation Extraction. In Findings ofACL. 2489–2511

[208] Julie Michelman, Nasrin Baratalipour, and Matthew Abueg. 2025. Enhancing Reasoning with Collaboration and Memory. arXiv preprint arXiv:2503.05944 (2025).

[209] Mindverse AI. 2025. Me.bot: Your AI Second Brain. https://www.me.bot/ Accessed: 2025-05-23.

[210] Marvin Minsky. 1980. K-Lines: A theory of memory. Cognitive Science (1980). doi:10.1016/S0364-0213(80)80014-0

[211] Eric Mitchell, Charles Lin, Antoine Bosselut, Chelsea Finn, and Christopher D Manning. 2022. Fast Model Editing at Scale. In International Conference on Learning Representations. https://openreview.net/forum?id=0DcZxeWfOP

[212] Eric Mitchell, Charles Lin, Antoine Bosselut, Christopher D Manning, and Chelsea Finn. 2022. Memory-based model editing at scale. In International Conference on Machine Learning. PMLR, 15817–15831.

[213] Andrei Ioan Muresanu, Anvith Thudi, Michael R. Zhang, and Nicolas Papernot. 2025. Fast Exact Unlearning for In-Context Learning Data for LLMs. In Forty-second International Conference on Machine Learning. https://openreview.net/forum?id=TzNVZEsqTi

[214] Mahmud Wasif Nafee, Maiqi Jiang, Haipeng Chen, and Yanfu Zhang. 2025. Dynamic Retriever for In-Context Knowledge Editing via Policy Optimization. In Proceedings ofthe 2025 Conference on Empirical Methods in Natural Language Processing, Christos Christodoulopoulos, Tanmoy Chakraborty, Carolyn Rose, and Violet Peng (Eds.). Association for Computational Linguistics, Suzhou, China, 16755–16768. doi:10.18653/v1/2025.

emnlp-main.848

[215] Ramesh Nallapati, Bowen Zhou, Cicero dos Santos, Çağlar Gu¤lçehre, and Bing Xiang. 2016. Abstractive Text Summarization using Sequence-tosequence RNNs and Beyond. In Proceedings ofthe 20th SIGNLL Conference on Computational Natural Language Learning. doi:10.18653/v1/K16-1028 [216] Neo4j. 2012. Neo4j - The World’s Leading Graph Database. https://neo4j.com/

[217] NevaMind-AI. 2025. MemU: An open-source memory framework for AI companions. https://github.com/NevaMind-AI/memU. Accessed: October 29, 2025.

[218] Cam-Van Thi Nguyen, Anh-Tuan Mai, and The-Son et al. Le. 2023. Conversation Understanding using Relational Temporal Graph Neural Networks with Auxiliary Cross-Modality Interaction. In EMNLP. doi:10.18653/v1/2023.emnlp-main.937

[219] Yuxiang Nie, Heyan Huang, Wei Wei, and Xian-Ling Mao. 2022. Capturing Global Structural Information in Long Document Question Answering with Compressive Graph Selector Network. In Proceedings ofthe 2022 Conference on Empirical Methods in Natural Language Processing. doi:10. 18653/v1/2022.emnlp-main.336

[220] Cicero Nogueira dos Santos, James Lee-Thorp, Isaac Noble, Chung-Ching Chang, and David Uthus. 2024. Memory Augmented Language Models through Mixture of Word Experts. In Proceedings ofthe NAACL-HLT. doi:10.18653/v1/2024.naacl-long.249

[221] Barlas Oguz, Xilun Chen, Vladimir Karpukhin, Stan Peshterliev, Dmytro Okhonko, Michael Schlichtkrull, Sonal Gupta, Yashar Mehdad, and Scott Yih. 2022. UniK-QA: Unified Representations of Structured and Unstructured Knowledge for Open-Domain Question Answering. In Findings ofthe Association for Computational Linguistics: NAACL 2022. doi:10.18653/v1/2022.findings-naacl.115

[222] Kai Tzu-iunn Ong, Namyoung Kim, Minju Gwak, Hyungjoo Chae, Taeyoon Kwon, Yohan Jo, Seung-won Hwang, Dongha Lee, and Jinyoung Yeo. 2025. Towards Lifelong Dialogue Agents via Timeline-based Memory Management. In Proceedings of the 2025 NAACL-HLT. https: //arxiv.org/abs/2406.10996

[223] OpenAI. 2022. Chatgpt: Optimizing language models for dialogue. https://openai.com/blog/chatgpt

[224] OpenAI. 2025. OpenAI Platform Documentation: Embeddings Guide. https://platform.openai.com/docs/guides/embeddings

[225] Siru Ouyang, Jun Yan, I-Hung Hsu, Yanfei Chen, Ke Jiang, Zifeng Wang, Rujun Han, Long T. Le, Samira Daruki, Xiangru Tang, Vishy Tirumalashetty George Lee, Mahsan Rofouei, Hangfei Lin, Jiawei Han, Chen-Yu Lee, and Tomas Pfister. 2025. ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory. arXiv preprint arXiv:2509.25140 (2025). https://arxiv.org/abs/2509.25140

[226] Charles Packer, Vivian Fang, Shishir G Patil, et al. 2023. MemGPT: Towards LLMs as Operating Systems. arXiv preprint arXiv:2310.00000 (2023)

[227] Zhuoshi Pan, Qianhui Wu, Huiqiang Jiang, Menglin Xia, Xufang Luo, Jue Zhang, Qingwei Lin, Victor Rühle, Yuqing Yang, Chin-Yew Lin, H. Vicky Zhao, Lili Qiu, and Dongmei Zhang. 2024. LLMLingua-2: Data Distillation for Eficient and Faithful Task-Agnostic Prompt Compression. In Findings ofthe ACL. doi:10.18653/v1/2024.findings-acl.57

[228] Joon Sung Park, Joseph O’Brien, Carrie Jun Cai, Meredith Ringel Morris, Percy Liang, and Michael S Bernstein. 2023. Generative Agents: Interactive Simulacra of Human Behavior. In Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology. 1–22.

[229] Shishir G. Patil, Fanjia Yan, Tianjun Zhang, Siddharth Jha, Pranav Gade, and Joseph E. Gonzalez. 2024. The Berkeley Function Calling Leaderboard: From Tool Use to Agentic Evaluation of Large Language Models. In The Thirty-eighth Annual Conference on Neural Information Processing Systems (NeurIPS). https://openreview.net/forum?id=2GmDdhBdDk

[230] Martin Pawelczyk, Seth Neel, and Himabindu Lakkaraju. 2023. In-context Unlearning: Language Models as Few-shot Unlearners. arXiv preprint arXiv:2310.07579 (2023).

[231] Martin Pawelczyk, Seth Neel, and Himabindu Lakkaraju. 2024. In-Context Unlearning: Language Models as Few-Shot Unlearners. In International Conference on Machine Learning. PMLR, 40034–40050.

[232] Mathis Pink, Qinyuan Wu, Vy Ai Vo, Javier Turek, Jianing Mu, Alexander Huth, and Mariya Toneva. 2025. Position: Episodic Memory is the Missing Piece for Long-Term LLM Agents. arXiv preprint arXiv:2502.06975 (2025)

[233] USVSN Sai Prashanth, Alvin Deng, Kyle O’Brien, et al. 2024. Recite, Reconstruct, Recollect: Memorization in LMs as a Multifaceted Phenomenon. arXiv preprint arXiv:2406.17746 (2024).

[234] Hongjin Qian, Peitian Zhang, Zheng Liu, Kelong Mao, and Zhicheng Dou. 2024. Memorag: Moving towards next-gen rag via memory-inspired knowledge discovery. arXiv preprint arXiv:2409.05591 (2024).

[235] Zhangcheng Qiang, Weiqing Wang, and Kerry Taylor. 2023. Agent-OM: Leveraging LLM Agents for Ontology Matching. arXiv preprint arXiv:2312.00326 (2023)

[236] Yujia Qin, Yining Ye, Junjie Fang, Haoming Wang, Shihao Liang, Shizuo Tian, Junda Zhang, Jiahao Li, Yunxin Li, Shijue Huang, Wanjun Zhong, Kuanye Li, Jiale Yang, Yu Miao, Woyu Lin, Longxiang Liu, Xu Jiang, Qianli Ma, Jingyu Li, Xiaojun Xiao, Kai Cai, Chuang Li, Yaowei Zheng, Chaolin Jin, Chen Li, Xiao Zhou, Minchao Wang, Haoli Chen, Zhaojian Li, Haihua Yang, Haifeng Liu, Feng Lin, Tao Peng, Xin Liu, and Guang Shi. 2025. UI-TARS: Pioneering Automated GUI Interaction with Native Agents. arXiv preprint arXiv:2501.12326 (2025). https://arxiv.org/abs/2501.12326

[237] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, Gretchen Krueger, and Ilya Sutskever. 2021. Learning Transferable Visual Models From Natural Language Supervision. In International Conference on Machine Learning. https://proceedings.mlr.press/v139/radford21a.htm

[238] Jack W. Rae, Anna Potapenko, Siddhant M. Jayakumar, Chloe Hillier, and Timothy P. Lillicrap. 2020. Compressive Transformers for Long-Range Sequence Modelling. In International Conference on Learning Representations. https://openreview.net/forum?id=SylKikSYDH

[239] Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais, Jack Ryan, and Daniel Chalef. 2025. Zep: A Temporal Knowledge Graph Architecture for Agent Memory. arXiv preprint arXiv:2501.13956 (2025).

[240] Abhinav Rastogi, Xiaoxue Zang, Srinivas Sunkara, Raghav Gupta, and Pranav Khaitan. 2020. Towards scalable multi-domain conversational agents: The schema-guided dialogue dataset. In AAAI Conference on Artificial Intelligence

[241] Mathieu Ravaut, Aixin Sun, Nancy Chen, and Shafiq Joty. 2024. On Context Utilization in Summarization with Large Language Models. In Proceedings ofthe 62nd Annual Meeting ofthe Association for Computational Linguistics (Volume 1: Long Papers). doi:10.18653/v1/2024.acl-long.153

[242] Steven Ritter, Jane X Wang, Zeb Kurth-Nelson, Siddhant Jayakumar, Charles Blundell, and Timothy Lillicrap. 2018. Meta-learning through Hebbian plasticity in random networks. In Advances in Neural Information Processing Systems (NeurIPS).

[243] Stephen E Robertson, Steve Walker, Susan Jones, Micheline M Hancock-Beaulieu, Mike Gatford, et al. 1995. Okapi at TREC-3. Nist Special Publication Sp (1995).

[244] Ali Safaya and Deniz Yuret. 2024. Neurocache: Eficient Vector Retrieval for Long-range Language Modeling. In Proceedings ofthe 2024 Conference ofthe North American Chapter ofthe Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers). doi:10.18653/ v1/2024.naacl-long.50

[245] Rana Salama, Jason Cai, and Michelle et al. Yuan. 2025. MemInsight: Autonomous Memory Augmentation for LLM Agents. arXiv preprint arXiv:2503.21760 (2025).

[246] Alireza Salemi, Sheshera Mysore, Michael Bendersky, and Hamed Zamani. 2023. Lamp: When large language models meet personalization. arXiv preprint arXiv:2304.11406 (2023).

[247] Mohammad Reza Samsami, Artem Zholus, Janarthanan Rajendran, and Sarath Chandar. 2024. Mastering Memory Tasks with World Models. In International Conference on Learning Representations. https://openreview.net/forum?id=1vDArHJ68h

[248] Gabriel Sarch, Lawrence Jang, Michael Tarr, William W Cohen, Kenneth Marino, and Katerina Fragkiadaki. 2024. Vlm agents generate their own memories: Distilling experience into embodied programs of thought. Advances in Neural Information Processing Systems (2024)

[249] Utkarsh Saxena, Gobinda Saha, Sakshi Choudhary, and Kaushik Roy. 2024. Eigen Attention: Attention in Low-Rank Space for KV Cache Compression. In Findings ofEMNLP. 15332–15344. doi:10.18653/v1/2024.findings-emnlp.899

[250] Ying Sheng, Lianmin Zheng, Binhang Yuan, Zhuohan Li, Max Ryabinin, Beidi Chen, Percy Liang, Christopher Ré, Ion Stoica, and Ce Zhang. 2023. FlexGen: high-throughput generative inference of large language models with a single GPU. In International Conference on Machine Learning. https://github.com/FMInference/FlexGen

[251] Dachuan Shi, Yonggan Fu, Xiangchi Yuan, Zhongzhi Yu, Haoran You, Sixu Li, Xin Dong, Jan Kautz, Pavlo Molchanov, and Yingyan Celine Lin. 2025. LaCache: Ladder-Shaped KV Caching for Eficient Long-Context Modeling of Large Language Models. In Forty-second International Conference on Machine Learning. https://openreview.net/forum?id=SDjZtxDo35

[252] Freda Shi, Xinyun Chen, Kanishka Misra, Nathan Scales, David Dohan, Ed H. Chi, Nathanael Schärli, and Denny Zhou. 2023. Large Language Models Can Be Easily Distracted by Irrelevant Context. In International Conference on Machine Learning. https://proceedings.mlr.press/v202/shi23a.html

[253] Haizhou Shi and Hao Wang. 2023. A unified approach to domain incremental learning with memory: Theory and algorithm. Advances in Neural Information Processing Systems (2023).

[254] Weijia Shi, Jaechan Lee, Yangsibo Huang, et al. 2024. MUSE: Machine Unlearning Six-way Evaluation for Language Models. arXiv preprint arXiv:2407.06460 (2024).

[255] Taranjeet Singh and Deshraj Yadav. 2024. Mem0: The Memory Layer for your AI agents. https://github.com/mem0ai/mem0

[256] Enxin Song, Wenhao Chai, Guanhong Wang, Yucheng Zhang, Haoyang Zhou, Feiyang Wu, Haozhe Chi, Xun Guo, Tian Ye, Yanting Zhang, et al. 2024. MovieChat: From Dense Token to Sparse Memory for Long Video Understanding. In CVPR. 18221–18232

[257] Woomin Song, Seunghyuk Oh, and Sangwoo et al. Mo. 2024. Hierarchical Context Merging: Better Long Context Understanding for Pre-trained LLMs. In ICLR. https://openreview.net/forum?id=ulaUJFd96G

[258] Larry R Squire, Lisa Genzel, John T Wixted, and Richard G Morris. 2015. Memory consolidation. Cold Spring Harbor perspectives in biology (2015).

[259] Jianlin Su, Murtadha Ahmed, Bo Wen, Luo Ao, Mingren Zhu, and Yunfeng Liu. 2024. Naive Bayes-based Context Extension for Large Language Models. In Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers), Kevin Duh, Helena Gomez, and Steven Bethard (Eds.). Association for Computational Linguistics, Mexico City, Mexico, 7791–7807. doi:10.18653/v1/2024.naacl-long.43

[260] Xin Su, Tiep Le, Steven Bethard, and Phillip Howard. 2023. Semi-structured chain-of-thought: Integrating multiple sources of knowledge for improved language model reasoning. arXiv preprint arXiv:2311.08505 (2023).

[261] Theodore Sumers, Shunyu Yao, Karthik Narasimhan, and Thomas Grifiths. 2024. Cognitive Architectures for Language Agents. Transactions on Machine Learning Research (2024). https://openreview.net/forum?id=1i6ZCvflQJ Survey Certification

[262] Hao Sun, Hengyi Cai, Bo Wang, Yingyan Hou, Xiaochi Wei, Shuaiqiang Wang, Yan Zhang, and Dawei Yin. 2024. Towards Verifiable Text Generation with Evolving Memory and Self-Reflection. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing. https://aclanthology.org/2024.emnlp-main.469

[263] Hanshi Sun, Li-Wen Chang, Wenlei Bao, Size Zheng, Ningxin Zheng, Xin Liu, Harry Dong, Yuejie Chi, and Beidi Chen. 2025. ShadowKV: KV Cache in Shadows for High-Throughput Long-Context LLM Inference. In Forty-second International Conference on Machine Learning. https: //openreview.net/forum?id=oa7MYAO6h6

[264] Weiwei Sun, Miao Lu, Zhan Ling, Kang Liu, Xuesong Yao, Yiming Yang, andJiecao Chen. 2025. Scaling Long-Horizon LLM Agent via Context-Folding. arXiv:2510.11967 [cs.CL] https://arxiv.org/abs/2510.1196

[265] Alon Talmor and Jonathan Berant. 2018. The Web as a Knowledge-base for Answering Complex Questions. In Proceedings ofthe 2018 Conference of the North American Chapter ofthe Association for Computational Linguistics: Human Language Technologies.

[266] Alon Talmor, Jonathan Herzig, Nicholas Lourie, and Jonathan Berant. 2019. CommonsenseQA: A Question Answering Challenge Targeting Commonsense Knowledge. In Proceedings ofthe 2019 Conference ofthe North American Chapter ofthe Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers). doi:10.18653/v1/N19-1421

[267] Chenmien Tan, Ge Zhang, and Jie Fu. 2024. Massive Editing for Large Language Models via Meta Learning. In The Twelfth International Conference on Learning Representations. https://openreview.net/forum?id=L6L1CJQ2PE

[268] Hexiang Tan, Fei Sun, and Wanli et al. Yang. 2024. Blinded by Generated Contexts: How Language Models Merge Generated and Retrieved Contexts When Knowledge Conflicts?. In ACL. doi:10.18653/v1/2024.acl-long.337

[269] Zhaoxuan Tan, Zheyuan Liu, and Meng Jiang. 2024. Personalized Pieces: Eficient Personalized Large Language Models through Collaborative Eforts. In Proceedings ofthe 2024 Conference on Empirical Methods in Natural Language Processing. doi:10.18653/v1/2024.emnlp-main.371

[270] Niket Tandon, Aman Madaan, Peter Clark, and Yiming Yang. 2021. Learning to repair: Repairing model output errors after deployment using a dynamic memory of feedback. arXiv (2021). https://arxiv.org/abs/2112.09737

[271] Jiaming Tang, Yilong Zhao, Kan Zhu, Guangxuan Xiao, Baris Kasikci, and Song Han. 2024. QUEST: Query-Aware Sparsity for Eficient Long-Context LLM Inference. In Proceedings ofthe 41st International Conference on Machine Learning. https://proceedings.mlr.press/v235/tang24l.html

[272] Yihong Tang, Bo Wang, Miao Fang, Dongming Zhao, Kun Huang, Ruifang He, and Yuexian Hou. 2023. Enhancing Personalized Dialogue Generation with Contrastive Latent Variables: Combining Sparse and Dense Persona. In Proceedings ofthe 61st Annual Meeting ofthe Association for Computational Linguistics (Volume 1: Long Papers), Anna Rogers, Jordan Boyd-Graber, and Naoaki Okazaki (Eds.). Association for Computational Linguistics, Toronto, Canada, 5456–5468. doi:10.18653/v1/2023.acl-long.299

[273] Yihong Tang, Bo Wang, Miao Fang, Dongming Zhao, Kun Huang, Ruifang He, and Yuexian Hou. 2023. Enhancing Personalized Dialogue Generation with Contrastive Latent Variables: Combining Sparse and Dense Persona. In Proceedings ofthe 61st Annual Meeting ofthe Association for Computational Linguistics (Volume 1: Long Papers). doi:10.18653/v1/2023.acl-long.299

[274] Yi Tay, Mostafa Dehghani, Samira Abnar, Yikang Shen, Dara Bahri, Philip Pham, Jinfeng Rao, Liu Yang, Sebastian Ruder, and Donald Metzler. 2021. Long Range Arena : A Benchmark for Eficient Transformers. In International Conference on Learning Representations. https://openreview.net/ forum?id=qVyeW-grC2k

[275] Tongyi DeepResearch Team. 2025. Tongyi DeepResearch: A New Era of Open-Source AI Researchers. https://github.com/Alibaba-NLP DeepResearch.

[276] Tencent. 2025. ima.copilot: Intelligent Workbench Powered by Tencent’s Hunyuan Model. https://ima.qq.com/ Accessed: 2025-05-23.

[277] Bozhong Tian, Xiaozhuan Liang, Siyuan Cheng, Qingbin Liu, Mengru Wang, Dianbo Sui, Xi Chen, Huajun Chen, and Ningyu Zhang. 2024. To Forget or Not? Towards Practical Knowledge Unlearning for Large Language Models. In Findings ofthe Association for Computational Linguistics: EMNLP 2024. 1524–1537.

[278] Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, and Ashish Sabharwal. 2022. MuSiQue: Multihop Questions via Single-hop Question Composition Transactions of the Association for Computational Linguistics (2022) doi:10 1162/tacl a 0047

[279] Endel Tulving et al. 1972. Episodic and Semantic Memory. Organization of Memory 1, 381-403 (1972), 1.

[280] Szymon Tworkowski, Konrad Staniszewski, and Mikołaj et al. Pacek. 2023. Focused Transformer: Contrastive Training for Context Scaling. In NeurIPS. https://proceedings.neurips.cc/paper\_files/paper/2023/file/8511d06d5590f4bda24d42087802cc81-Paper-Conference.pdf

[281] Bingbing Wang, Yiming Du, Bin Liang, Zhixin Bai, Min Yang, Baojun Wang, Kam-Fai Wong, and Ruifeng Xu. 2025. A New Formula for Sticker Retrieval: Reply with Stickers in Multi-Modal and Multi-Session Conversation. In Proceedings of the AAAI Conference on Artificial Intelligence.

[282] Bing Wang, Xinnian Liang, Jian Yang, Hui Huang, Shuangzhi Wu, Peihao Wu, Lu Lu, Zejun Ma, and Zhoujun Li. 2024. Enhancing Large Language Model with Self-Controlled Memory Framework. https://arxiv.org/abs/2304.13343

[283] Changyue Wang, Weihang Su, Qingyao Ai, Yichen Tang, and Yiqun Liu. 2025. Knowledge Editing through Chain-of-Thought. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing, Christos Christodoulopoulos, Tanmoy Chakraborty, Carolyn Rose, and Violet Peng (Eds.). Association for Computational Linguistics, Suzhou, China, 10684–10704. doi:10.18653/v1/2025.emnlp-main.540

[284] Jane X Wang, Zeb Kurth-Nelson, Dharshan Kumaran, Dhruva Tirumala, Hubert Soyer, Joel Z Leibo, Demis Hassabis, and Matthew Botvinick. 2021. Dual-system episodic control: Integrating episodic memory and reinforcement learning. Nature Human Behaviour (2021).

[285] Kewen Wang, Zhe Wang, Rodney Topor, et al. 2009. Concept and Role Forgetting in ALC Ontologies. In Proceedings of the 8th International Semantic Web Conference (ISWC)

[286] Lingzhi Wang, Tong Chen, Wei Yuan, et al. 2023. KGA: A General Machine Unlearning Framework Based on Knowledge Gap Alignment. arXiv preprint arXiv:2305.06535 (2023).

[287] Liyuan Wang, Xingxing Zhang, Hang Su, and Jun Zhu. 2024. A comprehensive survey of continual learning: Theory, method and application. IEEE Transactions on Pattern Analysis and Machine Intelligence (2024)

[288] Liyuan Wang, Xingxing Zhang, Kuo Yang, Longhui Yu, Chongxuan Li, Lanqing Hong, Shifeng Zhang, Zhenguo Li, Yi Zhong, and Jun Zhu. 2022 Memory replay with data compression for continual learning. arXiv (2022). https://arxiv.org/abs/2202.06592

[289] Peng Wang, Zexi Li, Ningyu Zhang, Ziwen Xu, Yunzhi Yao, Yong Jiang, Pengjun Xie, Fei Huang, and Huajun Chen. 2024. Wise: Rethinking the knowledge memory for lifelong model editing of large language models. Advances in Neural Information Processing Systems (2024)

[290] Piaohong Wang, Motong Tian, Jiaxian Li, Yuan Liang, Yuqing Wang, Qianben Chen, Tiannan Wang, Zhicong Lu, Jiawei Ma, Yuchen Eleanor Jiang, and Wangchunshu Zhou. 2025. O-Mem: Omni Memory System for Personalized, Long Horizon, Self-Evolving Agents. arXiv preprint arXiv:2511.13593 (2025).

[291] Peng Wang, Ningyu Zhang, Bozhong Tian, Zekun Xi, Yunzhi Yao, Ziwen Xu, Mengru Wang, Shengyu Mao, Xiaohan Wang, Siyuan Cheng, Kangwei Liu, Yuansheng Ni, Guozhou Zheng, and Huajun Chen. 2024. EasyEdit: An Easy-to-use Knowledge Editing Framework for Large Language Models. In Proceedings ofthe 62nd Annual Meeting ofthe Association for Computational Linguistics (Volume 3: System Demonstrations). doi:10.18653/v1/2024.acl-demos.9

[292] Qingyue Wang, Yanan Fu, Yanan Cao, Shi Wang, Zhiliang Tian, and Liang Ding. 2025. Recursively Summarizing Enables Long-Term Dialogue Memory in Large Language Models. Neurocomputing (2025). doi:10.1016/j.neucom.2025.130193

[293] Qingyue Wang, Yanhe Fu, Yanan Cao, Shuai Wang, Zhiliang Tian, and Liang Ding. 2025. Recursively summarizing enables long-term dialogue memory in large language models. Neurocomputing (2025). doi:10.1016/j.neucom.2025.130193

[294] Rongzheng Wang, Qizhi Chen, Yihong Huang, Yizhuo Ma, Muquan Li, Jiakai Li, Ke Qin, Guangchun Luo, and Shuang Liang. 2025. GraphCogent: Overcoming LLMs’ Working Memory Constraints via Multi-Agent Collaboration in Complex Graph Understanding. arXiv preprint arXiv:2508.12379 (2025).

[295] Siyuan Wang, Zhongyu Wei, Yejin Choi, et al. 2024. Symbolic Working Memory Enhances Language Models for Complex Rule Application. arXiv preprint arXiv:2408.13654 (2024).

[296] Shang Wang, Tianqing Zhu, Dayong Ye, and Wanlei Zhou. 2024. When Machine Unlearning Meets Retrieval-Augmented Generation (RAG): Keep Secret or Forget Knowledge? arXiv preprint arXiv:2410.15267 (2024).

[297] Song Wang, Yaochen Zhu, Haochen Liu, Zaiyi Zheng, Chen Chen, and Jundong Li. 2024. Knowledge editing for large language models: A survey. Comput. Surveys 57, 3 (2024), 1–37.

[298] Yu Wang and Xi Chen. 2025. Mirix: Multi-agent memory system for llm-based agents. arXiv preprint arXiv:2507.07957 (2025)

[299] Yike Wang, Shangbin Feng, Heng Wang, Weijia Shi, Vidhisha Balachandran, Tianxing He, and Yulia Tsvetkov. 2023. Resolving knowledge conflicts in large language models. arXiv preprint arXiv:2310.00935 (2023)

[300] Yu Wang, Yifan Gao, Xiusi Chen, Haoming Jiang, Shiyang Li, Jingfeng Yang, Qingyu Yin, Zheng Li, Xian Li, Bing Yin, et al. 2024. MEMORYLLM: towards self-updatable large language models. In International Conference on Machine Learning.

[301] Yu Wang, Chi Han, Tongtong Wu, Xiaoxin He, Wangchunshu Zhou, Nafis Sadeq, Xiusi Chen, Zexue He, Wei Wang, Gholamreza Hafari, et al. 2024. Towards lifespan cognitive systems. arXiv preprint arXiv:2409.13265 (2024)

[302] Yu Wang, Xinshuang Liu, Xiusi Chen, Sean O’Brien, Junda Wu, and Julian McAuley. 2024. Self-Updatable Large Language Models by Integrating Context into Model Parameters. In The Thirteenth International Conference on Learning Representations.

[303] Yu Wang, Ryuichi Takanobu, Zhiqi Liang, Yuzhen Mao, Yuanzhe Hu, Julian McAuley, and Xiaojian Wu. 2025. Mem-{\alpha}: Learning Memory Construction via Reinforcement Learning. arXiv preprint arXiv:2509.25911 (2025).

[304] Yaxuan Wang, Jiaheng Wei, Chris Yuhao Liu, Jinlong Pang, Quan Liu, Ankit Shah, Yujia Bao, Yang Liu, and Wei Wei. 2025. LLM Unlearning via Loss Adjustment with Only Forget Data. In The Thirteenth International Conference on Learning Representations. https://openreview.net/forum?id= 6ESRicalFE

[305] Ying Wang, Yanlai Yang, and Mengye Ren. 2023. LifelongMemory: Leveraging LLMs for Answering Queries in Long-form Egocentric Videos. arXiv preprint arXiv:2312.05269 (2023).

[306] Yutong Wang, Jiali Zeng, Xuebo Liu, Derek F. Wong, Fandong Meng, Jie Zhou, and Min Zhang. 2025. DelTA: An Online Document-Level Translation Agent Based on Multi-Level Memory. In International Conference on Learning Representations. https://openreview.net/forum?id=hoYFLRNbhc

[307] Yun Wang, Long Zhang, Jingren Liu, Jiaqi Yan, Zhanjie Zhang, Jiahao Zheng, Xun Yang, Dapeng Wu, Xiangyu Chen, and Xuelong Li. 2025. Episodi Memory Representation for Long-form Video Understanding. arXiv preprint arXiv:2508.09486 (2025)

[308] Zhaowei Wang, Wei Fan, Qing Zong, Hongming Zhang, Sehyun Choi, Tianqing Fang, Xin Liu, Yangqiu Song, Ginny Wong, and Simon See. 2024. AbsInstruct: Eliciting Abstraction Ability from LLMs through Explanation Tuning with Plausibility Estimation. In Proceedings ofthe 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers). Association for Computational Linguistics. doi:10.18653/v1/2024.acl long.55

[309] Zheng Wang, Zhongyang Li, Zeren Jiang, Dandan Tu, and Wei Shi. 2024. Crafting Personalized Agents through Retrieval-Augmented Generation on Editable Memory Graphs. In Proceedings ofthe 2024 Conference on Empirical Methods in Natural Language Processing. doi:10.18653/v1/2024.emnlp main.281

[310] Zhaowei Wang, Haochen Shi, Weiqi Wang, Tianqing Fang, Hongming Zhang, Sehyun Choi, Xin Liu, and Yangqiu Song. 2024. AbsPyramid: Benchmarking the Abstraction Ability of Language Models with a Unified Entailment Graph. In Findings ofthe Association for Computational Linguistics: NAACL 2024. Association for Computational Linguistics. doi:10.18653/v1/2024.findings-naacl.252

[311] Zhaowei Wang, Wenhao Yu, Xiyu Ren, Jipeng Zhang, Yu Zhao, Rohit Saxena, Liang Cheng, Ginny Wong, Simon See, Pasquale Minervini, et al. 2025. MMLongBench: Benchmarking Long-Context Vision-Language Models Efectively and Thoroughly. arXiv preprint arXiv:2505.10610 (2025)

[312] Rubin Wei, Jiaqi Cao, Jiarui Wang, Jushi Kai, Qipeng Guo, Bowen Zhou, and Zhouhan Lin. 2025. MLP Memory: Language Modeling with Retriever-pretrained External Memory. arXiv preprint arXiv:2508.01832 (2025)

[313] Bowen Wu, Wenqing Wang, and Haoran et al. Li. 2025. Interpersonal Memory Matters: A New Task for Proactive Dialogue Utilizing Conversationa History. arXiv preprint arXiv:2503.05150 (2025).

[314] Di Wu, Hongwei Wang, Wenhao Yu, et al. 2024. LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory. arXiv preprint arXiv:2410.10813 (2024).

[315] Haoyi Wu and Kewei Tu. 2024. Layer-Condensed KV Cache for Eficient Inference of Large Language Models. In ACL. doi:10.18653/v1/2024.acl long.602

[316] Wei Wu, Zhuoshi Pan, Chao Wang, Liyi Chen, Yunchu Bai, Tianfu Wang, Kun Fu, Zheng Wang, and Hui Xiong. 2025. TokenSelect: Eficient Long-Context Inference and Length Extrapolation for LLMs via Dynamic Token-Level KV Cache Selection. https://arxiv.org/abs/2411.02886

[317] Xinwei Wu, Junzhuo Li, Minghui Xu, Weilong Dong, Shuangzhi Wu, Chao Bian, and Deyi Xiong. 2023. DEPN: Detecting and Editing Privacy Neurons in Pretrained Language Models. In Proceedings ofthe 2023 Conference on Empirical Methods in Natural Language Processing. 2875–2886.

[318] Yuhuai Wu, Markus N Rabe, DeLesley Hutchins, et al. 2022. Memorizing Transformers. arXiv preprint arXiv:2203.08913 (2022).

[319] Yichen Wu, Hong Wang, Peilin Zhao, et al. 2024. Mitigating Catastrophic Forgetting in Online Continual Learning via Pareto Optimization. In International Conference on Machine Learning

[320] Yuxiang Wu, Yu Zhao, Baotian Hu, Pasquale Minervini, Pontus Stenetorp, and Sebastian Riedel. 2022. An Eficient Memory-Augmented Transformer for Knowledge-Intensive NLP Tasks. In Proceedings ofthe EMNLP. doi:10.18653/v1/2022.emnlp-main.346

[321] xAI. 2023. Grok. https://grok.com. Accessed: 2025-04-19.

[322] Tianhua Xia and Sai Qian Zhang. 2025. Kelle: Co-design KV Caching and eDRAM for Eficient LLM Serving in Edge Computing. arXiv:2510.16040 [cs.AR] https://arxiv.org/abs/2510.1604

[323] Guangxuan Xiao, Yuandong Tian, Beidi Chen, Song Han, and Mike Lewis. 2024. Eficient Streaming Language Models with Attention Sinks. In International Conference on Learning Representations. https://openreview.net/forum?id=NG7sS51zVF

[324] Zeqi Xiao, Yushi Lan, and Yifan et al. Zhou. 2025. WORLDMEM: Long-term Consistent World Simulation with Memory. arXiv preprint arXiv:2504.12369 (2025)

[325] Fangyuan Xu, Weijia Shi, and Eunsol Choi. 2024. RECOMP: Improving Retrieval-Augmented LMs with Context Compression and Selective Augmentation. In The Twelfth International Conference on Learning Representations. https://openreview.net/forum?id=mlJLVigNH

[326] Haoming Xu, Ningyuan Zhao, Liming Yang, Sendong Zhao, Shumin Deng, Mengru Wang, Bryan Hooi, Nay Oo, Huajun Chen, and Ningyu Zhang 2025. ReLearn: Unlearning via Learning for Large Language Models. In Proceedings ofthe 63rd Annual Meeting ofthe Association for Computational Linguistics (Volume 1: Long Papers), Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and Mohammad Taher Pilehvar (Eds.). Association for Computational Linguistics, Vienna, Austria, 5967–5987. doi:10.18653/v1/2025.acl-long.297

[327] Jing Xu, Arthur Szlam, and Jason Weston. 2021. Beyond Goldfish Memory: Long-term Open-domain Conversation. arXiv preprint arXiv:2107.07567 (2021).

[328] Rongwu Xu, Zehan Qi, Zhijiang Guo, Cunxiang Wang, Hongru Wang, Yue Zhang, and Wei Xu. 2024. Knowledge conflicts for llms: A survey. arXiv preprint arXiv:2403.08319 (2024).

[329] Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, and Yongfeng Zhang. 2025. A-MEM: Agentic Memory for LLM Agents. arXiv (2025). https://arxiv.org/abs/2502.12110

[330] Xinchao Xu, Zhibin Gou, Wenquan Wu, et al. 2022. Long Time No See! Open-domain Conversation with Long-term Persona Memory. arXiv preprint arXiv:2203.05797 (2022)

[331] Yao Xu, Shizhu He, Jiabei Chen, Zihao Wang, Yangqiu Song, Hanghang Tong, Guang Liu, Kang Liu, and Jun Zhao. 2024. Generate-on-graph: Treat llm as both agent and kg in incomplete knowledge graph question answering. arXiv preprint arXiv:2404.14741 (2024)

[332] Zhiyang Xu, Ying Shen, and Lifu Huang. 2023. MultiInstruct: Improving Multi-Modal Zero-Shot Learning via Instruction Tuning. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers). doi:10.18653/v1/2023.acl-long.64

[333] Sikuan Yan, Xiufeng Yang, Zuchao Huang, Ercong Nie, Zifeng Ding, Zonggen Li, Xiaowen Ma, Hinrich Schütze, Volker Tresp, and Yunpu Ma. 2025 Memory-r1: Enhancing large language model agents to manage and utilize memories via reinforcement learning. arXiv preprint arXiv:2508.19828 (2025).

[334] Dongjie Yang, Xiaodong Han, and Yan et al. Gao. 2024. PyramidInfer: Pyramid KV Cache Compression for High-throughput LLM Inference. In ACL Findings. doi:10.18653/v1/2024.findings-acl.195

[335] Hongkang Yang, Zehao Lin, Wenjin Wang, Hao Wu, Zhiyu Li, Bo Tang, Wenqiang Wei, Jinbo Wang, Zeyun Tang, Shichao Song, et al. 2024. ������<sup>3</sup>: Language Modeling with Explicit Memory. arXiv preprint arXiv:2407.01178 (2024).

[336] Hongkang Yang, Zehao Lin, and Wenjin et al. Wang. 2024. Memory3: Language Modeling with Explicit Memory. arXiv preprint arXiv:2407.01178 (2024).

[337] John Yang, Carlos E Jimenez, Alex L Zhang, Kilian Lieret, Joyce Yang, Xindi Wu, Ori Press, Niklas Muennighof, Gabriel Synnaeve, Karthik R Narasimhan, Diyi Yang, Sida Wang, and Ofir Press. 2025. SWE-bench Multimodal: Do AI Systems Generalize to Visual Software Domains?. In ICLR. https://openreview.net/forum?id=riTiq3i21b

[338] Yijun Yang, Zeyu Huang, Wenhao Zhu, Zihan Qiu, Fei Yuan, Jef Z. Pan, and Ivan Titov. 2025. A Controllable Examination for Long-Context Language Models. In The Thirty-ninth Annual Conference on Neural Information Processing Systems Datasets and Benchmarks Track. https: //openreview.net/forum?id=atjpGqjG73

[339] Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W Cohen, Ruslan Salakhutdinov, and Christopher D Manning. 2018. HotpotQA: A dataset for diverse, explainable multi-hop question answering. arXiv preprint arXiv:1809.09600 (2018).

[340] Zhou Yang, Zhaochun Ren, Wang Yufeng, Haizhou Sun, Chao Chen, Xiaofei Zhu, and Xiangwen Liao. 2024. An Iterative Associative Memory Model for Empathetic Response Generation. In Proceedings ofthe 62nd Annual Meeting ofthe Association for Computational Linguistics (Volume 1: Long Papers). doi:10.18653/v1/2024.acl-long.170

[341] Shunyu Yao, Jefrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. 2023. ReAct: Synergizing Reasoning and Acting in Language Models. In The Eleventh International Conference on Learning Representations (ICLR). https://openreview.net/forum?id=WE\_vluYpwdu

[342] Yao Yao, Zuchao Li, and Hai Zhao. 2024. SirLLM: Streaming Infinite Retentive LLM. In Proceedings ofthe 62nd Annual Meeting ofthe Association for Computational Linguistics. doi:10.18653/v1/2024.acl-long.143

[343] Yuanshun Yao, Xiaojun Xu, and Yang Liu. 2024. Large language model unlearning. Advances in Neural Information Processing Systems 37 (2024), 105425–105475

[344] Rui Ye, Zhongwang Zhang, Kuan Li, Huifeng Yin, Zhengwei Tao, Yida Zhao, Liangcai Su, Liwen Zhang, Zile Qiao, Xinyu Wang, Pengjun Xie, Fei Huang, Siheng Chen, Jingren Zhou, and Yong Jiang. 2025. AgentFold: Long-Horizon Web Agents with Proactive Context Management. arXiv:2510.24699 [cs.CL] https://arxiv.org/abs/2510.24699

[345] Howard Yen, Tianyu Gao, and Danqi Chen. 2024. Long-Context Language Modeling with Parallel Context Encoding. In Proceedings ofthe 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers). doi:10.18653/v1/2024.acl-long.142

[346] Wen-tau Yih, Ming-Wei Chang, Xiaodong He, and Jianfeng Gao. 2016. The Value of Semantic Parse Labeling for Knowledge Base Question Answering. In Proceedings ofthe 54th Annual Meeting ofthe Association for Computational Linguistics (Volume 1: Long Papers).

[347] Chanwoong Yoon, Taewhoo Lee, and Hyeon et al. Hwang. 2024. CompAct: Compressing Retrieved Documents Actively for Question Answering. In EMNLP. doi:10.18653/v1/2024.emnlp-main.1194

[348] Peter Young, Alice Lai, Micah Hodosh, and Julia Hockenmaier. 2014. From image descriptions to visual denotations: New similarity metrics for semantic inference over event descriptions. Transactions ofthe Association for Computational Linguistics (2014)

[349] Paul Youssef, Zhixue Zhao, Jörg Schlötterer, and Christin Seifert. 2025. How to Make LLMs Forget: On Reversing In-Context Knowledge Edits In Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers), Luis Chiruzzo, Alan Ritter, and Lu Wang (Eds.). Association for Computational Linguistics, Albuquerque, New Mexico, 12656–12669. doi:10.18653/v1/2025.naacl-long.630

[350] Hongli Yu, Tinghong Chen, Jiangtao Feng, Jiangjie Chen, Weinan Dai, Qiying Yu, Ya-Qin Zhang, Wei-Ying Ma, Jingjing Liu, Mingxuan Wang, et al. 2025. MemAgent: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent. arXiv preprint arXiv:2507.02259 (2025).

[351] Haofei Yu, Cunxiang Wang, Yue Zhang, and Wei Bi. 2023. TRAMS: Training-free Memory Selection for Long-range Language Modeling. In Finding ofthe Association for Computational Linguistics: EMNLP 2023. doi:10.18653/v1/2023.findings-emnlp.331

[352] Jiwen Yu, Jianhong Bai, Yiran Qin, Quande Liu, Xintao Wang, Pengfei Wan, Di Zhang, and Xihui Liu. 2025. Context as memory: Scene-consistent interactive long video generation with memory retrieval. arXiv preprint arXiv:2506.03141 (2025).

[353] Jiayi Yuan, Hongyi Liu, Shaochen Zhong, Yu-Neng Chuang, Songchen Li, Guanchu Wang, Duy Le, Hongye Jin, Vipin Chaudhary, Zhaozhuo Xu, Zirui Liu, and Xia Hu. 2024. KV Cache Compression, But What Must We Give in Return? A Comprehensive Benchmark of Long Context Capable Approaches. In Findings of EMNLP. 4623–4648. doi:10.18653/v1/2024.findings-emnlp.266

[354] Xihang Yue, Linchao Zhu, and Yi Yang. 2024. FragRel: Exploiting Fragment-level Relations in the External Memory of Large Language Models In Findings ofthe Association for Computational Linguistics: ACL 2024, Lun-Wei Ku, Andre Martins, and Vivek Srikumar (Eds.). Association for Computational Linguistics, Bangkok, Thailand, 16348–16361. doi:10.18653/v1/2024.findings-acl.968

[355] Ao Zhang, Yuan Yao, Wei Ji, Zhiyuan Liu, and Tat-Seng Chua. 2023. NExT-Chat: An LMM for Chat, Detection and Segmentation. arXiv preprint arXiv:2311.04498 (2023).

[356] Guibin Zhang, Muxin Fu, Guancheng Wan, Miao Yu, Kun Wang, and Shuicheng Yan. 2025. G-Memory: Tracing Hierarchical Memory for Multi-Agent Systems. arXiv preprint arXiv:2506.07398 (2025).

[357] Kai Zhang, Xiangchao Chen, Bo Liu, Tianci Xue, Zeyi Liao, Zhihan Liu, Xiyao Wang, Yuting Ning, Zhaorun Chen, Xiaohan Fu, et al. 2025. Agent learning via early experience. arXiv preprint arXiv:2510.08558 (2025)

[358] Kai Zhang, Yangyang Kang, Fubang Zhao, and Xiaozhong Liu. 2024. LLM-based Medical Assistant Personalization with Short- and Long-Term Memory Coordination. In Proceedings ofthe 2024 Conference ofthe North American Chapter ofthe Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers). doi:10.18653/v1/2024.naacl-long.132

[359] Ningyu Zhang, Yunzhi Yao, Bozhong Tian, et al. 2024. A Comprehensive Study of Knowledge Editing for Large Language Models. arXiv preprint arXiv:2401.01286 (2024).

[360] Peitian Zhang, Zheng Liu, and Shitao et al. Xiao. 2025. Long Context Compression with Activation Beacon. In ICLR. https://openreview.net/ forum?id=1eQT9OzfNQ

[361] Qizheng Zhang, Changran Hu, Shubhangi Upasani, Boyuan Ma, Fenglu Hong, Vamsidhar Kamanuru, Jay Rainton, Chen Wu, Mengmeng Ji, Hanchen Li, et al. 2025. Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models. arXiv preprint arXiv:2510.04618 (2025).

[362] Qingru Zhang, Chandan Singh, and Liyuan et al. Liu. 2024. Tell Your Model Where to Attend: Post-hoc Attention Steering for LLMs. In ICLR. https://openreview.net/forum?id=xZDWO0oejD

[363] Qingyang Zhang, Ningyu Zhang, et al. 2025. LightMem: Lightweight and Eficient Memory-Augmented Generation. arXiv preprint arXiv:2510.18866 (2025).

[364] Siyuan Zhang, Yichi Zhang, and Yinpeng et al. Dong. 2025. Self-Memory Alignment: Mitigating Factual Hallucinations with Generalized Improvement. arXiv preprint arXiv:2502.19127 (2025).

[365] Taolin Zhang, Qizhou Chen, Dongyang Li, Chengyu Wang, Xiaofeng He, Longtao Huang, Jun Huang, et al. 2024. DAFNet: Dynamic Auxiliary Fusion for Sequential Model Editing in Large Language Models. In Findings of the Association for Computational Linguistics: ACL 2024. 1588–1602.

[366] Xinrong Zhang, Yingfa Chen, Shengding Hu, Zihang Xu, Junhao Chen, Moo Hao, Xu Han, Zhen Thai, Shuo Wang, Zhiyuan Liu, and Maosong Sun. 2024. ∞Bench: Extending Long Context Evaluation Beyond 100K Tokens. In ACL. 15262–15277. doi:10.18653/v1/2024.acl-long.814

[367] Zeyu Zhang, Xiaohe Bo, Chen Ma, Rui Li, Xu Chen, Quanyu Dai, Jieming Zhu, Zhenhua Dong, and Ji-Rong Wen. 2024. A survey on the memory mechanism of large language model based agents. arXiv preprint arXiv:2404.13501 (2024).

[368] Zhenyu Zhang, Ying Sheng, Tianyi Zhou, Tianlong Chen, Lianmin Zheng, Ruisi Cai, Zhao Song, Yuandong Tian, Christopher Re, Clark Barrett, Zhangyang Wang, and Beidi Chen. 2023. H2O: Heavy-Hitter Oracle for Eficient Generative Inference of Large Language Models. In Thirty-seventh Conference on Neural Information Processing Systems. https://openreview.net/forum?id=RkRrPp7GKO

[369] Wenting Zhao, Ye Liu, Tong Niu, Yao Wan, Philip S. Yu, Shafiq Joty, Yingbo Zhou, and Semih Yavuz. 2024. DIVKNOWQA: Assessing the Reasoning Ability of LLMs via Open-Domain Question Answering over Knowledge Base and Text. In Findings ofthe Association for Computational Linguistics: NAACL 2024. doi:10.18653/v1/2024.findings-naacl.5

[370] Wayne Xin Zhao, Yusheng Wang, Yujia Yuan, Qitian Xiao, Yichong He, Jingyuan Zhang, and Ji-Rong Wen. 2024. CodeBuddy: Teaching Large Language Models to Write Better Code via Self-Improvement Feedback. In ACL. https://arxiv.org/abs/2403.09161 arXiv preprint arXiv:2403.09161.

[371] Yilong Zhao, Chien-Yu Lin, Kan Zhu, Zihao Ye, Lequn Chen, Size Zheng, Luis Ceze, Arvind Krishnamurthy, Tianqi Chen, and Baris Kasikci. 2024. Atom: Low-Bit Quantization for Eficient and Accurate LLM Serving. In MLSys. https://proceedings.mlsys.org/paper\_files/paper/2024/hash 5edb57c05c81d04beb716ef1d542fe9e-Abstract-Conference.html

[372] Zhengyi Zhao, Shubo Zhang, Yiming Du, Bin Liang, Baojun Wang, Zhongyang Li, Binyang Li, and Kam-Fai Wong. 2025. EventWeave: A Dynamic Framework for Capturing Core and Supporting Events in Dialogue Systems. arXiv preprint arXiv:2503.23078 (2025)

[373] Ce Zheng, Lei Li, Qingxiu Dong, Yuxuan Fan, Zhiyong Wu, Jingjing Xu, and Baobao Chang. 2023. Can We Edit Factual Knowledge by In-Context Learning?. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing. 4862–4876.

[374] Longtao Zheng, Rundong Wang, Xinrun Wang, and Bo An. 2024. Synapse: Trajectory-as-Exemplar Prompting with Memory for Computer Control. In International Conference on Learning Representations. https://arxiv.org/abs/2306.07863

[375] Wanjun Zhong, Lianghong Guo, Qiqi Gao, et al. 2024. MemoryBank: Enhancing Large Language Models with Long-term Memory. In Proceedings ofthe AAAI Conference on Artificial Intelligence

[376] Zexuan Zhong, Zhengxuan Wu, Christopher D Manning, Christopher Potts, and Danqi Chen. 2023. MQuAKE: Assessing Knowledge Editing in Language Models via Multi-Hop Questions. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing. 15686–15702.

[377] Huichi Zhou, Yihang Chen, Siyuan Guo, Xue Yan, Kin Hei Lee, Zihan Wang, Ka Yiu Lee, Guchun Zhang, Kun Shao, Linyi Yang, et al. 2025. AgentFly: Fine-tuning LLM Agents without Fine-tuning LLMs. arXiv preprint arXiv:2508.16153 (2025).

[378] Junjie Zhou, Zheng Liu, Shitao Xiao, Bo Zhao, and Yongping Xiong. 2024. VISTA: Visualized Text Embedding For Universal Multi-Modal Retrieval. In Proceedings ofthe 62nd Annual Meeting ofthe Association for Computational Linguistics (Volume 1: Long Papers).

[379] Wenxuan Zhou, Sheng Zhang, Hoifung Poon, and Muhao Chen. 2023. Context-faithful Prompting for Large Language Models. In Findings of EMNLP. doi:10.18653/v1/2023.findings-emnlp.968

[380] Yang Zhou, Pengfei Cao, Yubo Chen, Qingbin Liu, Dianbo Sui, Xi Chen, Kang Liu, and Jun Zhao. 2025. M2Edit: Locate and Edit Multi-Granularity Knowledge in Multimodal Large Language Model. In Proceedings ofthe 2025 Conference on Empirical Methods in Natural Language Processing Christos Christodoulopoulos, Tanmoy Chakraborty, Carolyn Rose, and Violet Peng (Eds.). Association for Computational Linguistics, Suzhou, China, 29017–29030. doi:10.18653/v1/2025.emnlp-main.1478

[381] Zijian Zhou, Ao Qu, Zhaoxuan Wu, Sunghwan Kim, Alok Prakash, Daniela Rus, Jinhua Zhao, Bryan Kian Hsiang Low, and Paul Pu Liang. 2025 MEM1: Learning to Synergize Memory and Reasoning for Eficient Long-Horizon Agents. arXiv preprint arXiv:2506.15841 (2025).

[382] Yun Zhu, Jia-Chen Gu, Caitlin Sikora, Ho Ko, Yinxiao Liu, Chu-Cheng Lin, Lei Shu, Liangchen Luo, Lei Meng, Bang Liu, and Jindong Chen. 2025. Accelerating Inference of Retrieval-Augmented Generation via Sparse Context Selection. In The Thirteenth International Conference on Learning Representations. https://openreview.net/forum?id=HE6pJoNnFp

[383] Jiaru Zou, Xiyuan Yang, Ruizhong Qiu, Gaotang Li, Katherine Tieu, Pan Lu, Ke Shen, Hanghang Tong, Yejin Choi, Jingrui He, James Zou, Mengdi Wang, and Ling Yang. 2025. Latent Collaboration in Multi-Agent Systems. arXiv:arXiv:2511.20639 [cs.CL] https://arxiv.org/abs/2511.20639

## 附录

## A 基于 GPT 的流水线筛选

为促进与我们的分类体系对齐的大规模相关性过滤，我们设计了一个基于 GPT 的评分流水线，用于评估论文摘要与预定义任务定义（表 4）之间的对齐程度。每篇摘要与相应任务定义配对，由模型按 1–10 分评分，并以 ≥ 8 为阈值保留高相关论文以供进一步分析。我们采用 GPT-4o-mini 作为评分骨干，因其在性能与效率之间取得良好权衡。尽管架构相对轻量，GPT-4o-mini 展现出较强的零样本推理能力，使其成为在超过 30,000 篇论文的语料上进行摘要级主题相关性估计时兼具成本效益与足够精度的选择。该评估过程所用精确 prompt 格式见附图 18。

## B 相对引用指数

本工作通过相对引用指数（RCI）识别有影响力的工作，该指标受 RCR 指标 [110] 启发，依据发表年龄估计期望引用数，以防止不同发表日期原始引用数之间的偏差。论文 $\mathscr { p } _ { i }$ 的年龄 $A _ { i }$ 计算如下：

$$
A = T - Y e a r _ {i}\tag{7}
$$

其中 $T$ 为引用采集日期（2025 年 4 月 20 日），$Year_{i}$ 为论文 $i$ 首次发表的年份。由此，我们可以用三种不同方式建模论文 $\mathcal { P } i$ 的引用数 $C _ { i }$ 与年龄 $A _ { i }$ 之间的关系，即线性模型：

$$
C _ {i} = \beta + \alpha A _ {i}\tag{8}
$$

指数模型：

$$
C _ {i} = \exp (\beta + \alpha A _ {i})\tag{9}
$$

双对数回归模型：

$$
\log (C _ {i} + 1) = \beta + \alpha \log A _ {i} + \epsilon_ {i}\tag{10}
$$

我们从过去 3 年（2022 至 2025）的顶级 NLP 与 ML 会议（即 ACL、NAACL、EMNLP、NeurIPS、ICML、ICLR）收集论文。为减少不同研究领域带来的偏差，我们使用 GPT 并借助图 18 所示 prompt，对论文与本文所讨论四个主题的相关性进行评分。我们选取所有得分等于或高于 8 的论文，并从 Semantic Scholar API<sup>1</sup> 收集其发表日期与引用数。对于缺少发表日期字段的论文，我们以会议首日作为发表日期。处理后共收集 3,932 篇有效论文，并据此计算估计的 $\hat { \beta }$ 与 $\hat { \alpha }$<sup>2</sup>。图 15 展示了估计的年龄—引用模型，可以发现双对数回归模型对数据拟合最佳，几乎完美地拟合了引用数随发表年龄的中位数关系。此外，双对数回归模型保证论文刚发表时期望引用数为 0，符合直觉。因此，我们选择双对数回归模型计算下一步的期望引用数<sup>3</sup>，并能够得到论文 $\mathcal { P } i$ 的期望引用数 $\hat { C } _ { i }$。

![](../assets/arxiv-2505.00675-chart23.jpg) 
图 15. 3,932 篇论文引用分布随年龄变化的箱线图，红色曲线为期望引用数 $\hat { C } _ { i }$。一般而言，$R C I > = 1$ 表示该论文在其年龄组中高于引用中位数，而更高的 RCI 表示更高的研究影响力。

其与年龄 $A _ { i }$ 的关系为：

$$
\hat {C} _ {i} = \exp (\hat {\beta}) A _ {i} ^ {\hat {\alpha}}\tag{11}
$$

然后我们计算论文 $\mathcal { P } i$ 的相对引用指数 $RCI_i$ 如下：

$$
R C I _ {i} = \frac {C _ {i}}{\hat {C} _ {i}}\tag{12}
$$

当 $R C I _ { i } > = 1$ 时，我们认为该论文的引用高于其期望值，反之亦然。本文聚焦于 $R C I > = 1$ 的论文，我们认为这些论文具有更大影响力。

## C 主题影响力的 RCI 驱动分析

本研究同时利用 RCI 与发表数量趋势，以更清晰地理解各类 memory-related 研究主题的发展与影响。如图 16 所示，箱线图展示了各主题按年份划分的中位相对引用指数（RCI）分布。值得注意的是，2023 年成为大型语言模型（LLM）出现后的关键年份，long-context 与 parametric memory 相关发表的数量与质量均激增，表明这些领域直接受到 LLM 进展的塑造。相比之下，long-term memory 与 multi-source memory 保持了相对稳定的平均影响水平，表明其持续活跃，但该时期未出现颠覆性或界定领域的工作。

图 17 可视化了各主题发表数量与中位 RCI 的时间趋势。所有主题的发表数量均显著增长，其中 long-context 尤其从 2022 年前代表性最弱的主题之一，扩展为 2024 年最突出的主题——这很大程度上由 LLM 的兴起驱动。此外，long-term memory 的 RCI 稳步上升，反映出该领域有价值工作的增加。相比之下，其他主题在 2023 年后中位 RCI 明显下降，尽管其影响水平仍与 2022 年前相当。这些模式共同凸显大型模型在催化 memory-related 研究进展方面的实质影响，尤其是在 long-context 与 parametric memory 领域。

![](../assets/arxiv-2505.00675-chart24.jpg) 
图 16. 各主题与年份的中位 RCI 总体分布。

![](../assets/arxiv-2505.00675-chart25.jpg) 
图 17. 各主题发表数量与中位 RCI 的总体时间趋势。

## D memory types、操作、主题与会议场所之间互动的和弦分析

我们从两个视角呈现 memory research 的和弦分析：（1）memory types、操作与主题之间的互动；（2）它们在主要 ML 与 NLP 会议场所中的分布。

## D.1 跨类型、操作与主题的 memory 互动

为直观分析 memory types、操作与研究主题之间联系的强度，我们考察 132 篇 $\mathrm { R C I } \geq 1$ 的方法类论文，并基于分析生成最终和弦图（如附图 19 所示）。

从 memory types 看，研究主要聚焦 parametric memory 与 contextual unstructured memory，多数工作集中于 compression、retrieval、forgetting 与 updating。相比之下，contextual structured memory 相对未被充分探索，这可能因为 LLM 针对序列文本优化，在结构化输入上表现较弱。

从操作视角看，compression 与 retrieval 最常被研究，而 indexing 获得相对较少关注。这在很大程度上是因为多数现有工作聚焦 memory 的使用，而 retrieval 与 compression 是两种基础操作。就 consolidation 而言，多数研究指将知识存储于模型参数（通过在非结构化文本上训练），或将其转化为固定外部 memory 格式。

updating 与 forgetting 主要与 knowledge editing 和 machine unlearning 相关，通常位于 parametric memory 内。这些方向旨在依据外部输入增量修改模型参数。然而，由于模型内部的不透明性，此类 memory operations 仍处于主动探索的早期阶段。相比之下，面向 LLM 的 memory indexing 机制获得有限关注。

从主题视角看，parametric 修改研究大多以 parametric memory 为中心，尽管一些工作尝试通过非结构化文本上的 continual learning 进行参数适配。long-context 主题下的研究主要聚焦非结构化 memory 中的 compression 与 retrieval，部分利用 KV cache 等 parametric 形式。在 long-term memory 研究中，重点也在非结构化 memory，尤其是 consolidation、compression 与 retrieval 方面。multi-source memory 相关研究仍然有限，通常涉及整合结构化与非结构化信息。

总之，对 contextual structured memory 的有限探索，凸显了通过将其与非结构化 memory 整合来发展更全面 memory operations 的机会。其次，multi-source memory 研究仍然稀少，尽管其带来重大挑战——尤其是异构来源引起的 memory conflict。因此，为 multi-source memory integration 设计鲁棒且一致的策略是有前景的方向。最后，indexing 虽在传统数据库系统中得到广泛研究，但在基于 LLM 的 agent 中仍未被充分探索。memory types 的复杂性以及向量化或稀疏 retrieval 方法的需求，呼唤专门为 LLM 中的推理与交互量身定制的新 indexing 方法。

## D.2 跨会议场所的 memory 互动

除主要论文收集之外，我们还分析了主要会议中 81 篇 RCI ≥ 1 的方法类论文。如图 20 所示，从操作视角看，compression、forgetting 与 updating 在 ML 会议（ICLR、ICML、NeurIPS）中出现更频繁，而 retrieval 与 consolidation 在 NLP 会议（ACL、EMNLP、NAACL）中更常见。这一分布表明，前一组操作仍处于理论探索阶段，而后者更扎根于实际应用。因此，compression、forgetting 与 updating 仍具有转化为真实世界系统的巨大潜力。

indexing 在 ML 与 NLP 会议中均代表性不足。部分原因可能是其常与 retrieval 共现，部分原因是当前基于向量的 indexing 方法相对统一，少有新颖替代方案。

从主题视角看，long-term memory 在 NLP 会议中更常被讨论，而 long-context 主题在 ML 场所更常见——这很可能反映这些社区不同的应用导向与理论导向。parametric modification 在 ML 会议中出现更频繁，而 multi-source memory 在 NLP 会议中更普遍，凸显 multi-source memory 挑战常出现在真实应用与系统集成过程中。

<table><tr><td>主题名称</td><td>prompt 中的定义</td></tr><tr><td>long-term memory</td><td>定义：创建系统，确保过去交互中的知识在新任务出现时仍可访问，维持多轮对话中的连续性。特征：memory 保留、retrieval 与归因——访问 memory 并将其 context 化，以支撑连贯交互。</td></tr><tr><td>long-context</td><td>定义：高效处理、解释并利用极长输入序列而不发生性能退化。特征：优化 attention、context compression，以及缓解「中间迷失」问题。</td></tr><tr><td>parametric memory modification</td><td>定义：管理与更新内部参数，以在不完整重训练的情况下保持准确性、隐私与可适应性。特征：选择性 machine unlearning、精确 model editing、distillation 与终身学习。</td></tr><tr><td>multi-source</td><td>定义：将多样数据类型整合并协调进统一框架，同时解决不一致。特征：多模态 fusion、语义一致性、冲突解决与冗余移除。</td></tr><tr><td>个性化*</td><td>定义：构建以用户为中心的 memory system，在适配个体偏好与历史的同时保护隐私。特征：隐私感知画像、一致的个性化与长期连续性。</td></tr><tr><td colspan="2">表 4. 五个以 memory 为中心的评估主题的定义与特征。*个性化被视为 long-term memory 的一种专门形式，聚焦 cross-session 的用户中心适配。</td></tr></table>

![](../assets/arxiv-2505.00675-fig18.jpg) 
图 18. 用于评估文章与特定任务定义相关性的 prompt。

![](../assets/arxiv-2505.00675-chart26.jpg)

图 19. 跨 memory 主题、操作与类型的互动和弦图。 
![](../assets/arxiv-2505.00675-chart27.jpg) 
图 20. 跨 memory 主题与会议场所的互动和弦图。

<table><tr><td>数据集</td><td>模态</td><td>操作</td><td>数据集类型</td><td>人物</td><td>时间推理</td><td>指标</td><td>用途</td><td>年份</td></tr><tr><td>PersonaMem-v2 [121]</td><td>文本</td><td>updating、retrieval</td><td>MS</td><td>✓</td><td>✓</td><td>准确率、人物得分</td><td>用于评测 long-context 中隐式用户人物学习与 agentic memory updating 的 benchmark。</td><td>2025</td></tr><tr><td>MemoryBench [4]</td><td>文本</td><td>updating、retrieval、forgetting</td><td>QA</td><td>✘</td><td>✓</td><td>准确率、保持率</td><td>面向 memory 正确性、持久性与 continual learning 的综合 benchmark。</td><td>2025</td></tr><tr><td>HaluMem [29]</td><td>文本</td><td>retrieval</td><td>QA</td><td>✘</td><td>✘</td><td>准确率、幻觉率、遗漏率</td><td>评估 memory 抽取、更新与 retrieval 中的幻觉。</td><td>2025</td></tr><tr><td>BFCL V4 [229]</td><td>文本（API/代码）</td><td>updating、retrieval、reasoning</td><td>QA（API）</td><td>✘</td><td>✘</td><td>AST 准确率、执行成功率</td><td>评测函数调用能力，并设有专门的 memory 类别用于 CRUD 风格的工具使用。</td><td>2025</td></tr><tr><td>LongMemEval [314]</td><td>文本</td><td>indexing、retrieval、compression</td><td>MS</td><td>✘</td><td>✓</td><td>Recall@K、NDCG@K、准确率</td><td>评测聊天助手 long-term memory 能力（含时间推理）的 benchmark。</td><td>2024</td></tr><tr><td>LoCoMo [196]</td><td>文本 + 图像</td><td>indexing、retrieval、compression</td><td>MS</td><td>✘</td><td>✓</td><td>准确率、ROUGE、精确率、召回率、F1</td><td>在问答、事件摘要与多模态对话任务中评估 LLM 的 long-term memory。</td><td>2024</td></tr><tr><td>MemoryBank [375]</td><td>文本</td><td>updating、retrieval</td><td>MS</td><td>✓</td><td>✘</td><td rowspan="2">准确率、人工评估 MAP、召回率、精确率、F1；准确率、GPT-4 得分</td><td>为 LLM 增强 long-term memory，适配用户人物设定与演进中的 context。</td><td>2024</td></tr><tr><td>PerLTQA [65]</td><td>文本</td><td>retrieval</td><td>MS</td><td>✓</td><td>✘</td><td>评估个性化 long-term memory 的问答能力。</td><td>2024</td></tr><tr><td>MALP [358]</td><td>文本</td><td>retrieval、compression</td><td>QA</td><td>✓</td><td>✘</td><td>ROUGE、准确率、胜率</td><td>偏好条件化的对话生成；支持 PEFT 定制。</td><td>2024</td></tr><tr><td>DialSim [137]</td><td>文本</td><td>retrieval</td><td>MS</td><td>✓</td><td>✘</td><td>准确率</td><td>在真实、实时、long-context 的多方对话条件下评估对话系统。</td><td>2024</td></tr><tr><td>CC [114]</td><td>文本</td><td>retrieval</td><td>MS</td><td>✘</td><td>✓</td><td>BLEU、ROUGE</td><td>对包含时间与关系 context 的长期对话进行建模。</td><td>2023</td></tr><tr><td>LAMP [246]</td><td>文本</td><td>consolidation、retrieval、compression</td><td>MS</td><td>✓</td><td>✓</td><td>准确率、F1、ROUGE</td><td>提供基于用户与基于时间的划分，用于评估短期与长期个性化。</td><td>2023</td></tr><tr><td>MSC [327]</td><td>文本</td><td>consolidation、retrieval、compression</td><td>MS</td><td>✓</td><td>✘</td><td>PPL</td><td>用于评估演进中的共享知识的 multi-session 人—人对话。</td><td>2022</td></tr><tr><td>DuLeMon [330]</td><td>文本</td><td>consolidation、updating、retrieval、compression</td><td>MS</td><td>✓</td><td>✘</td><td>准确率、F1、召回率、精确率、PPL、BLEU、DISTINCT</td><td>支持动态人物追踪与一致的长程人—机器人交互。</td><td>2022</td></tr><tr><td>2WikiMultiHopQA [95]</td><td>表格 + 知识库 + 文本</td><td>indexing、retrieval、compression</td><td>QA</td><td>✘</td><td>✘</td><td>EM、F1</td><td>结合结构化与非结构化数据并带推理路径的多跳问答。</td><td>2020</td></tr><tr><td>NQ [145]</td><td>文本</td><td>retrieval、compression</td><td>QA</td><td>✘</td><td>✘</td><td>EM、F1</td><td>基于真实 Google 搜索查询的开放域问答。</td><td>2019</td></tr><tr><td>HotpotQA [339]</td><td>文本</td><td>retrieval、compression</td><td>QA</td><td>✘</td><td>✘</td><td>EM、F1</td><td>带可解释推理与句子级支撑事实的多跳问答。</td><td>2018</td></tr></table>

表 5. 用于评估 long-term memory 的数据集。“Mo” = 模态（modality）；“Ops” = 支持的操作；“DS Type” = 数据集类型（QA – 问答，MS – multi-session 对话）；“Per” 与 “TR” = 是否含人物设定（persona）与时间推理（temporal reasoning）。

<table><tr><td>数据集</td><td>模态</td><td>操作</td><td>指标</td><td>用途</td><td>年份</td></tr><tr><td>LongBioBench [338]</td><td>文本</td><td>retrieval</td><td>EM</td><td>面向 LLM 的可控 long-context 多跳检验</td><td>2025</td></tr><tr><td>LongBench v2 [16]</td><td>文本 + 表格 + KG</td><td>compression、retrieval</td><td>准确率</td><td>LongBench 的更新版本，更长且更具挑战性，采用统一的多项选择格式以便可靠评估。</td><td>2024</td></tr><tr><td>SWE-bench Multimodal [337]</td><td>文本 + 图像</td><td>compression、retrieval</td><td>解决率、推理成本</td><td>将 SWE-bench 扩展至多模态任务（517 个实例），以测试带图像的推理。</td><td>2024</td></tr><tr><td>∞Bench [366]</td><td>文本</td><td>compression、retrieval</td><td>F1、准确率、ROUGE-L-Sum</td><td>含 12 个任务、面向极端 long-context（平均 &gt;100K token）的 benchmark。</td><td>2024</td></tr><tr><td>L-Eval [5]</td><td>文本</td><td>compression、retrieval</td><td>ROUGE-L、F1、GPT-4</td><td>从多个视角评估 long-context LLM 的 20 个任务。</td><td>2023</td></tr><tr><td>LongBench [15]</td><td>文本</td><td>compression、retrieval</td><td>F1、ROUGE-L、准确率、EM、Edit Sim</td><td>含 14 个英文任务、5 个中文任务与 2 个代码任务，用于系统的 long-context 评估。</td><td>2023</td></tr><tr><td>SWE-bench [130]</td><td>文本</td><td>compression、retrieval</td><td>解决率（% Resolved）</td><td>在解决 GitHub issue（2,294 个实例）上测试 LLM，要求对大型代码库进行推理。</td><td>2023</td></tr><tr><td>NIAH [135]</td><td>文本</td><td>retrieval</td><td>召回准确率</td><td>评估 LLM 在 long-context（haystack）中查找特定数据（needle）的能力。</td><td>2023</td></tr><tr><td>LooGLE [154]</td><td>文本</td><td>compression、retrieval</td><td rowspan="2">BLEU-1、BLEU-4、ROUGE-1、ROUGE-4、ROUGE-L、Meteor、Bert、GPT-4 分数；ROUGE-1、ROUGE-2、ROUGE-L、Bert 分数</td><td>含 7 个任务、面向极端 long-context（每篇文档 &gt;24K token）的 benchmark。</td><td>2023</td></tr><tr><td>GovReport [104]</td><td>文本</td><td>compression</td><td>用于评估长文档摘要的政府研究报告。</td><td>2021</td></tr><tr><td>MusiQue [278]</td><td>文本</td><td>retrieval</td><td>F1</td><td>面向推理与 long-context 问答任务的多跳问答 benchmark。</td><td>2021</td></tr><tr><td>LRA [274]</td><td>文本 + 图像</td><td>compression、retrieval</td><td>准确率</td><td>用于评估高效 long-context 模型的 6 个任务。</td><td>2020</td></tr><tr><td>NaturalQuestions [145]</td><td>文本</td><td>retrieval</td><td>EM、F1</td><td>用于 long-context retrieval 与推理任务的问答数据集。</td><td>2019</td></tr><tr><td>PG-19 [238]</td><td>文本</td><td>compression</td><td>PPL</td><td>来自 Project Gutenberg 的书籍语料，用于 long-context 语言建模。</td><td>2019</td></tr><tr><td>TriviaQA [134]</td><td>文本</td><td>retrieval</td><td>EM、F1</td><td>适合测试 long-context 理解与推理的问答数据集。</td><td>2017</td></tr><tr><td>NarrativeQA [143]</td><td>文本</td><td>retrieval</td><td>BLEU-1、BLEU-4、Meteor、ROUGE-L、MRR</td><td>面向 long-context 叙事文本理解的问答数据集。</td><td>2017</td></tr><tr><td>CNN/DailyMail [215]</td><td>文本</td><td>compression</td><td>ROUGE-1、ROUGE-2、ROUGE-L</td><td>用于摘要任务的新闻文章，适合 long-context 评估。</td><td>2016</td></tr><tr><td>WikiText-103 [206]</td><td>文本</td><td>compression</td><td>PPL</td><td>基于 Wikipedia 的 1 亿 token 语料，用于 long-context 语言建模。</td><td>2016</td></tr><tr><td>数据集</td><td>模态</td><td>操作</td><td>指标</td><td>用途</td><td>年份</td></tr><tr><td>KnowEdit[359]</td><td>文本</td><td>updating</td><td>编辑成功率、可移植性、局部性、流畅度</td><td>提供六个数据集的综合 benchmark，用于评估知识插入、修改与擦除。</td><td>2024</td></tr><tr><td>MUSE[254]</td><td>文本</td><td>forgetting</td><td>VerbMem、KnowMem、PrivLeak</td><td>面向机器 machine unlearning（machine unlearning）的 benchmark，评估 forgetting 后模型的六项关键属性。</td><td>2024</td></tr><tr><td>KnowUnDo[277]</td><td>文本</td><td>forgetting</td><td>forgetting 成功率、保留成功率、困惑度、ROUGE-L</td><td>在含版权内容与用户隐私的领域评估 machine unlearning，检查关键知识是否被意外擦除。</td><td>2024</td></tr><tr><td>RWKU[133]</td><td>文本</td><td>forgetting</td><td>ROUGE-L</td><td>在无语料条件下测试真实世界 machine unlearning，并含对抗性评估。</td><td>2024</td></tr><tr><td>WMDP[156]</td><td>文本</td><td>forgetting</td><td>问答准确率</td><td>面向生物安全、网络安全与化学安全的有害知识检测与 machine unlearning benchmark。</td><td>2024</td></tr><tr><td>TOFU[197]</td><td>文本</td><td>forgetting</td><td>概率、ROUGE、真值比</td><td>含 200 位虚构作者事实的数据集，用于 machine unlearning 研究。</td><td>2024</td></tr><tr><td>ABSA[57]</td><td>文本</td><td>consolidation</td><td>F1</td><td>用于方面级情感分析，以在 continual learning 任务中评估 LLM。</td><td>2024</td></tr><tr><td>MQUAKE-CF[376]</td><td>文本</td><td>updating</td><td>单编辑成功率、实例级准确率、多跳准确率</td><td>评估反事实知识经多跳推理（最多 4 跳）的传播。</td><td>2023</td></tr><tr><td>MQUAKE-T[376]</td><td>文本</td><td>updating</td><td>单编辑成功率、实例级准确率、多跳准确率</td><td>评估时间性知识经多跳推理链的传播，每条链含一次编辑。</td><td>2023</td></tr><tr><td>Counterfact[203]</td><td>文本</td><td>updating</td><td>有效性得分、有效性幅度、改写得分、邻域得分</td><td>评估超出表层编辑的重大且不合理的事实变更。</td><td>2022</td></tr><tr><td>zsRE[50]</td><td>文本</td><td>updating</td><td>成功率、保留准确率、等价准确率、性能退化</td><td>最早的用于评估 knowledge editing 的数据集之一。</td><td>2021</td></tr><tr><td>SGD[240]</td><td>文本</td><td>consolidation</td><td>JGA、FWT、BWT</td><td>面向用户意图演进与模式（schema）持续更新的多轮任务导向对话。</td><td>2020</td></tr><tr><td>INSPIRED[89]</td><td>文本</td><td>consolidation</td><td>JGA、FWT、BWT</td><td>支持任务导向设定下意图增量变化的对话数据集。</td><td>2020</td></tr><tr><td>Natural Questions[145]</td><td>文本</td><td>consolidation</td><td>indexing 准确率、Hits@1</td><td>带 index 文档的多用途问答数据集，用于动态 continual learning。</td><td>2019</td></tr></table>

表 6. 用于 long-context memory 评估的数据集，按由新到旧排序。

表 7. 用于 parametric memory 评估的数据集，按年份由新到旧排序。

<table><tr><td>数据集</td><td>模态</td><td>操作</td><td>来源数</td><td>模态数</td><td>任务</td><td>指标</td><td>用途</td><td>年份</td></tr><tr><td>MultiChat [281]</td><td>文本 + 图像</td><td>retrieval</td><td>2</td><td>2</td><td>retrieval</td><td>精确率、mAP、GPT-4</td><td>带 cross-session 图文对话 context 的image-grounded sticker retrieval。</td><td>2025</td></tr><tr><td>MovieChat-1K [256]</td><td>文本 + 视频</td><td>retrieval</td><td>2</td><td>2</td><td>QA</td><td>准确率</td><td>面向大型多模态模型的长期视频理解，用于视频问答与描述任务。</td><td>2025</td></tr><tr><td>Context-conflicting [268]</td><td>文本</td><td>compression</td><td>2</td><td>1</td><td>冲突</td><td>DiffGR、EM、相似度</td><td>评估模型处理跨来源冲突证据的能力。</td><td>2024</td></tr><tr><td>EgoSchema [198]</td><td>视频 + 文本</td><td>retrieval、compression</td><td>3</td><td>2</td><td>fusion</td><td>准确率</td><td>结合 episodic 视频 memory、社会图式与对话，用于长期问答。</td><td>2023</td></tr><tr><td>Ego4D NLQ [101]</td><td>视频 + 文本</td><td>retrieval、compression</td><td>2</td><td>2</td><td>fusion</td><td>Recall@K</td><td>以自然语言查询对带时间 memory 的第一人称视频进行问答。</td><td>2022</td></tr><tr><td>2WikiMultihopQA [95]</td><td>文本</td><td>indexing、retrieval、compression</td><td>2</td><td>1</td><td colspan="2">推理；EM、F1</td><td>需跨两段 Wikipedia 文本并利用句子级证据进行推理的多跳问答。</td><td>2020</td></tr><tr><td>HybridQA [34]</td><td>文本</td><td>retrieval、compression</td><td>2</td><td>1</td><td colspan="2">推理；EM、F1</td><td>需跨结构化表格与非结构化文本进行推理的问答。</td><td>2020</td></tr><tr><td>CommonsenseVQA [266]</td><td>文本 + 图像</td><td>retrieval、compression</td><td>2</td><td>2</td><td>fusion</td><td>准确率</td><td>需视觉—文本 fusion 的视觉场景常识问答。</td><td>2019</td></tr><tr><td>NaturalQuestions [145]</td><td>文本</td><td>retrieval、compression</td><td>&gt;1*</td><td>1</td><td>冲突</td><td>EM、F1</td><td>基于 Google 搜索片段的真实世界问答；亦用于矛盾分析。</td><td>2019</td></tr><tr><td>ComplexWebQuestions [265]</td><td>文本</td><td>retrieval、compression</td><td>&gt;1*</td><td>1</td><td colspan="2">推理；EM、F1</td><td>需跨网页片段进行多步推理的组合型问答。</td><td>2018</td></tr><tr><td>HotpotQA [339]</td><td>文本</td><td>retrieval、compression</td><td>2</td><td>1</td><td>冲突</td><td>EM、F1、支撑事实准确率</td><td>带段落级来源与句子级支撑事实的多跳问答。</td><td>2018</td></tr><tr><td>TriviaQA [134]</td><td>文本</td><td>retrieval、compression</td><td>≥6</td><td>1</td><td>冲突</td><td>EM、F1</td><td>含噪声网页来源的冷知识问答；用于来源分歧研究。</td><td>2017</td></tr><tr><td>WebQuestionsSP [346]</td><td>文本</td><td>indexing、retrieval、compression</td><td>&gt;1*</td><td>1</td><td colspan="2">推理；F1、准确率</td><td>带结构化推理链的增强版 WebQuestions。</td><td>2016</td></tr><tr><td>Flickr30K [348]</td><td>文本 + 图像</td><td>retrieval、compression</td><td>2</td><td>2</td><td>retrieval</td><td>相似度</td><td>广泛用于跨模态 retrieval 与对齐任务的图文对。</td><td>2014</td></tr></table>

表 8. 用于评估 multi-source memory 的数据集。“Mo” 表示数据模态。“Ops” 表示操作。“Src#” = 每个实例的信息来源数量；“Mod#” = 模态数量；“Task” = retrieval、fusion、reasoning 或 conflict resolution。

<table><tr><td>方法</td><td>类型</td><td>TF</td><td>RE</td><td>DS</td><td>输入</td><td>输出</td><td>语言模型</td><td>操作</td><td>特性</td><td>年份</td></tr><tr><td>EWE[31]</td><td>memory-grounded generation</td><td>✓</td><td>✓</td><td>✓</td><td>context</td><td>响应</td><td>Llama-3.1-70B, 8B</td><td>updating、retrieval</td><td>显式 working memory、在线事实核查反馈、事实性长文生成</td><td>2025</td></tr><tr><td>ICAL[248]</td><td>生成</td><td>✓</td><td>✓</td><td>✓</td><td>示例 + 任务指令</td><td>轨迹 + 思维</td><td>GPT4V, Qwen2VL</td><td>updating</td><td>轨迹抽象 memory、多模态、迭代式推理修正</td><td>2025</td></tr><tr><td>MEMORAG [234]</td><td>memory-grounded generation</td><td>✓</td><td>✓</td><td>✓</td><td>context + 查询</td><td>响应</td><td>Mistral7B-Instruct, Phi-3-mini-128K-instruct, GPT-4o</td><td>retrieval、compression</td><td>全局 memory retrieval、KV memory compression、反馈引导生成</td><td>2024</td></tr><tr><td>ReadAgent[149]</td><td>生成</td><td>✓</td><td>✓</td><td>✓</td><td>context + 查询</td><td>检索到的段落/摘要</td><td>PaLM 2</td><td>updating、retrieval</td><td>episodic gist memory、动态 memory retrieval、扩展 context window</td><td>2024</td></tr><tr><td>FLOW-RAG[296]</td><td>updating</td><td>✓</td><td>✓</td><td>✓</td><td>知识库 + 查询</td><td>响应</td><td>GPT4o, Gemini, llama2-7B-chat</td><td>forgetting</td><td>基于 RAG 的 machine unlearning</td><td>2024</td></tr><tr><td>HippoRAG[84]</td><td>retrieval</td><td>✓</td><td>✓</td><td>✓</td><td>context + 查询</td><td>响应</td><td>ColBERTv2, GPT-3.5-turbo, Llama-3.1-8B, 70B</td><td>indexing</td><td>类海马体 retrieval、多跳问答、knowledge graph consolidation</td><td>2024</td></tr><tr><td>IterCQR[116]</td><td>retrieval</td><td>✓</td><td>✓</td><td>✓</td><td>对话历史 + 查询</td><td>retrieval 结果</td><td>Transformer++</td><td>retrieval</td><td>迭代式查询重构、context-aware 查询重写</td><td>2024</td></tr><tr><td>MemoryBank[375]</td><td>consolidation</td><td>✓</td><td>✓</td><td>✓</td><td>retrieval 结果与 context + 查询</td><td>响应</td><td>ChatGLM-6B, BELLE-7B, gpt-3.5-turbo</td><td>consolidation、updating、forgetting、retrieval</td><td>fine-tuning、RAG、Ebbinghaus forgetting</td><td>2024</td></tr><tr><td>FLARE[129]</td><td>retrieval</td><td>✓</td><td>✓</td><td>✓</td><td>数据库 + 查询</td><td>响应</td><td>WebGPT, WebCPM</td><td>retrieval</td><td>生成过程中的主动 retrieval、前瞻式查询预测</td><td>2023</td></tr><tr><td>MemoChat[190]</td><td>consolidation</td><td>✓</td><td>✓</td><td>✓</td><td>对话历史 + 查询</td><td>响应</td><td>GPT4, ChatGPT, Vicuna-7B, 13B, 33B, T5</td><td>consolidation、retrieval</td><td>结构化备忘、memory-driven 对话、memory—retrieval—响应循环</td><td>2023</td></tr><tr><td>NLI-Transfer[13]</td><td>updating</td><td>✓</td><td>✓</td><td>✓</td><td>memory + 对话历史</td><td>响应</td><td>T5</td><td>consolidation、updating、retrieval</td><td>session-level memory 追踪、演进式对话系统</td><td>2022</td></tr></table>

表 9. memory management 与利用中的 long-term memory 方法概览。“TF”（Training Free）表示该方法是否无需额外的基于梯度的更新即可运行；“RE”（Retrieval Module）表示该方法是否使用 retrieval；“DS”（Dialogue System）表示该方法是否为对话任务设计。

<table><tr><td>方法</td><td>类型</td><td>TF</td><td>RE</td><td>输入</td><td>输出</td><td>语言模型</td><td>操作</td><td>特性</td><td>年份</td></tr><tr><td>LD-Agent[153]</td><td>增强</td><td>√</td><td>√</td><td>retrieval 结果与 context + 查询</td><td>响应</td><td>ChatGLM, BlenderBot, ChatGPT</td><td>consolidation、updating、retrieval</td><td>长期对话建模、事件与人物 memory、模块化 agent 架构</td><td>2025</td></tr><tr><td>SiliconFriend[375]</td><td>增强</td><td>✗</td><td>√</td><td>retrieval 结果与 context + 查询</td><td>响应</td><td>ChatGLM-6B, BELLE-7B, gpt-3.5-turbo</td><td>consolidation、updating、forgetting、retrieval</td><td>fine-tuning、RAG、Ebbinghaus forgetting</td><td>2024</td></tr><tr><td>MALP[358]</td><td>适配</td><td>✗</td><td>√</td><td>retrieval 结果与 context + 查询</td><td>响应</td><td>GPT3.5, LLaMA-7B, LLaMA-13B</td><td>consolidation、retrieval</td><td>memory 协调、计算仿生 memory mechanism、患者画像、自聊</td><td>2024</td></tr><tr><td>PERPCS[269]</td><td>适配</td><td>✗</td><td>✗</td><td>用户历史</td><td>/</td><td>Llama-2-7B</td><td>consolidation</td><td>模块化 PEFT 共享、协同个性化、用户历史组装</td><td>2024</td></tr><tr><td>LAPDOG[105]</td><td>增强</td><td>√</td><td>√</td><td>retrieval 结果与 context + 查询</td><td>响应</td><td>T5</td><td>consolidation、updating、retrieval</td><td>基于故事的人物 retrieval、retriever—生成器联合训练</td><td>2024</td></tr><tr><td>RECAP[181]</td><td>增强</td><td>✗</td><td>√</td><td>retrieval 结果与 context + 查询</td><td>响应</td><td>Transformers</td><td>retrieval</td><td>层次化 Transformer retriever、context-aware 前缀编码器</td><td>2023</td></tr><tr><td>CLV[273]</td><td>适配</td><td>✗</td><td>✗</td><td>人物设定 + 查询</td><td>响应</td><td>GPT-2</td><td>consolidation</td><td>对比学习、聚类稠密人物、对话生成</td><td>2023</td></tr><tr><td>PERKGQA[68]</td><td>增强</td><td>√</td><td>√</td><td>retrieval 结果与 knowledge graph + 查询</td><td>响应</td><td>RoBERTa</td><td>retrieval</td><td>长期对话建模、事件与人物 memory、模块化 agent 架构</td><td>2022</td></tr></table>

表 10. 个性化中的 long-term memory 方法概览。"TF"（Training Free）表示该方法是否无需额外的基于梯度的更新即可运行。"RE"（Retrieval Module）表示该方法是否需要 retrieval。

<table><tr><td>方法</td><td>类型</td><td>TF</td><td>FC</td><td>操作</td><td>语言模型</td><td>特性</td><td>年份</td></tr><tr><td>FoldGRPO[264]</td><td>context compression</td><td>✗</td><td>✗</td><td>compression</td><td>Seed-OSS-36B</td><td>训练 agent 将详细历史主动折叠为简洁摘要的强化学习框架</td><td>2025</td></tr><tr><td>RECOMP[325]</td><td>context compression</td><td>✗</td><td>✗</td><td>compression</td><td>GPT-2, GPT2-XL, GPT-J, Flan-UL2</td><td>采用抽取式与生成式策略的硬 prompt compression</td><td>2024</td></tr><tr><td>LongLLMLingua[125]</td><td>context compression</td><td>√</td><td>✗</td><td>compression</td><td>GPT-3.5-Turbo-06136, LongChat-13B-16k</td><td>用于高效输入表示的硬 prompt compression</td><td>2024</td></tr><tr><td>LLMLingua-2[227]</td><td>context compression</td><td>✗</td><td>✗</td><td>compression</td><td>XLM-RoBERTa-Large, Multilingual-BERT</td><td>面向多语言 context、含数据 distillation 的硬 prompt compression</td><td>2024</td></tr><tr><td>QGC[25]</td><td>context compression</td><td>✗</td><td>✗</td><td>compression</td><td>LongChat-13B-16K, LLaMA-2-7B</td><td>查询引导的动态 context compression</td><td>2024</td></tr><tr><td>xRAG[36]</td><td>context compression</td><td>✗</td><td>✗</td><td>compression</td><td>Mistral-7B, Mixtral-8x7B</td><td>用于 parametric consolidation 的软 prompt compression</td><td>2024</td></tr><tr><td>AutoCompressor[37]</td><td>context compression</td><td>✗</td><td>√</td><td>compression</td><td>OPT-1.3B, OPT-2.7B, LLaMA-2-7B</td><td>面向通用效率的软 prompt compression</td><td>2023</td></tr><tr><td>StreamingLLM[323]</td><td>KV cache eviction</td><td>√</td><td>✗</td><td>compression</td><td>Llama-2, MPT, PyThia, Falcon</td><td>静态 KV cache eviction、初始 token 中的 attention sink</td><td>2024</td></tr><tr><td>FastGen[77]</td><td>KV cache eviction</td><td>√</td><td>✗</td><td>compression</td><td>Llama-1 7B/13B/30B/65B</td><td>基于自适应剖析（profiling）的 KV cache eviction</td><td>2024</td></tr><tr><td>SnapKV[163]</td><td>KV cache eviction</td><td>√</td><td>✗</td><td>compression</td><td>LWM-Text-Chat-1M, LongChat-7b-v1.5-32k, Mistral-7B-Instruct-v0.2, Mixtral-8x7B-Instruct-v0.1</td><td>按 attention head 进行的 KV cache eviction、attention head 行为</td><td>2024</td></tr><tr><td>LESS[59]</td><td>KV cache storing optimization</td><td>✗</td><td>√</td><td>compression</td><td>Llama-2 13B, Falcon 7B</td><td>低秩 KV cache 存储，支持查询全部 token</td><td>2024</td></tr><tr><td>KIVI[188]</td><td>KV cache storing optimization</td><td>√</td><td>√</td><td>compression</td><td>Llama-2 7B/13B, Llama-3 8B, Falcon 7B, Mistral-7B</td><td>非对称 KV cache 量化</td><td>2024</td></tr><tr><td>KVQuant[98]</td><td>KV cache storing optimization</td><td>√</td><td>√</td><td>compression</td><td>LLaMA-7B/13B/30B/65B, Llama-2-7B/13B/70B, Llama-3-8B/70B, Mistral-7B</td><td>KV cache 量化</td><td>2024</td></tr><tr><td> $H_2O$ [368]</td><td>KV cache eviction</td><td>√</td><td>✗</td><td>compression</td><td>OPT, Llama-1, GPT-NeoX</td><td>动态 KV cache eviction，保留 Heavy Hitter token</td><td>2023</td></tr><tr><td>Scissorhands[184]</td><td>KV cache eviction</td><td>√</td><td>✗</td><td>compression</td><td>OPT 6.7B, 13B, 30B, 66B</td><td>动态 KV cache eviction、重要性持久性假设</td><td>2023</td></tr><tr><td>ShadowKV[263]</td><td>KV cache storing optimization</td><td>√</td><td>√</td><td>compression</td><td>Llama-3.1-8B, Llama-3-8B-1M, GLM-4-9B-1M, Yi-9B-200K, Phi-3-Mini-128K, and Qwen2-7B-128K</td><td>将键的 compression 影子版本保留在 GPU 上、把完整数据卸载到 CPU，以降低 GPU 显存占用</td><td>2025</td></tr><tr><td>FlexGen[250]</td><td>KV cache storing optimization</td><td>√</td><td>√</td><td>compression</td><td>OPT 6.7B to 175B</td><td>KV cache 量化与卸载</td><td>2023</td></tr></table>

表 11. long-context memory compression 方法概览。“TF”（Training Free）表示无需额外的基于梯度的更新。“FC”（Full Context）表示该方法保留对全部 context token 的访问。

<table><tr><td>方法</td><td>类型</td><td>TF</td><td>FC</td><td>操作</td><td>语言模型</td><td>特性</td><td>年份</td></tr><tr><td>Sparse RAG [382]</td><td>context 选择</td><td>✕</td><td>✕</td><td>retrieval</td><td>Gemini</td><td>稀疏 context 选择，减少解码时涉及的文档数量</td><td>2025</td></tr><tr><td>GraphReader [158]</td><td>context 选择</td><td>√</td><td>✕</td><td>retrieval</td><td>GPT-4-128k</td><td>基于图的 agent；将 long-context 结构化为图</td><td>2024</td></tr><tr><td>Ziya-Reader [91]</td><td>context 选择</td><td>✕</td><td>√</td><td>retrieval</td><td>Ziya2-13B-Base (LLaMA-2-13B)</td><td>supervised fine-tuning；位置无关的多步问答</td><td>2024</td></tr><tr><td>FILM [6]</td><td>context 选择</td><td>✕</td><td>√</td><td>retrieval</td><td>FILM-7B (Mistral 7B)</td><td>数据驱动方法；缓解「中间迷失」问题</td><td>2024</td></tr><tr><td>TokenSelect [316]</td><td>KV cache selection</td><td>√</td><td>√</td><td>retrieval</td><td>Qwen2 7B, Llama-3 8B, Yi-1.5-6B</td><td>动态 token 级 KV cache selection</td><td>2025</td></tr><tr><td>QUEST [271]</td><td>KV cache selection</td><td>√</td><td>√</td><td>retrieval</td><td>LongChat-7B-v1.5-32K, Yarn-Llama2-7B-128K</td><td>查询感知的 KV cache selection</td><td>2024</td></tr><tr><td>Memorizing Transformers [318]</td><td>KV cache selection</td><td>✕</td><td>√</td><td>retrieval</td><td>Transformers</td><td>用于增强召回的外部 KV cache memory</td><td>2022</td></tr></table>

表 12. long-context memory retrieval 方法概览。“TF”（Training Free）表示无需额外的基于梯度的更新。“FC”（Full Context）表示该方法保留对全部 context token 的访问。

<table><tr><td>方法</td><td>类型</td><td>PR</td><td>TF</td><td>BES</td><td>SEO</td><td>语言模型</td><td>主要改进</td><td>年份</td></tr><tr><td>AlphaEdit [70]</td><td>先定位后编辑</td><td>✕</td><td>√</td><td>√</td><td>√</td><td>gpt2-xl-1.5b,gpt-j-6b,llama3-8b</td><td>通过将扰动投影到零空间并添加正则项来保护被保留的知识，以支持顺序编辑。</td><td>2024</td></tr><tr><td>MEMAT [201]</td><td>先定位后编辑</td><td>✕</td><td>√</td><td>√</td><td>✕</td><td>aguila-7b</td><td>MEMIT 的扩展，引入 attention head 修正以支持跨语言编辑。</td><td>2024</td></tr><tr><td>DEM [107]</td><td>先定位后编辑</td><td>✕</td><td>√</td><td>√</td><td>✕</td><td>gpt-j-6b,llama2-7b</td><td rowspan="2">使用动态感知模块选择编辑层，面向自由文本中的常识 knowledge editing；通过 Intra-editing Attention Flow（事实内）与 Inter-editing Attention Flow（事实间）支持顺序编辑。</td><td>2024</td></tr><tr><td>DAFNET [365]</td><td>元学习</td><td>✕</td><td>✕</td><td>✕</td><td>√</td><td>gpt-j-6b,llama2-7b</td><td>2024</td></tr><tr><td>Larimar [48]</td><td>附加参数</td><td>√</td><td>√</td><td>√</td><td>√</td><td>gpt2-xl,gpt-j-6b</td><td>引入解耦的潜在 memory module，在测试时以条件化方式调节 LLM 解码器而无需更新参数。</td><td>2024</td></tr><tr><td>MEMORYLLM [300]</td><td>附加参数</td><td>√</td><td>✕</td><td>√</td><td>√</td><td>llama2-7b</td><td>在冻结的 LLM 中引入固定大小的 memory 池，并以增量、选择性的方式更新。</td><td>2024</td></tr><tr><td>WISE [289]</td><td>附加参数</td><td>√</td><td>✕</td><td>√</td><td>√</td><td>llama2-7b,mistral-7b,gpt-j-6b</td><td>通过 Side Memory Design 与 Knowledge Sharding and Merging 支持顺序编辑。</td><td>2024</td></tr><tr><td>PMET [159]</td><td>先定位后编辑</td><td>✕</td><td>√</td><td>√</td><td>✕</td><td>gpt-j-6b,gpt-neox-20bgpt-j-6b,gpt2-xl-1.5b,gpt-neo,gpt-neox,opt-175b</td><td>联合优化 attention head 与 FFN，仅更新 FFN 权重。</td><td>2023</td></tr><tr><td>IKE [373]</td><td>prompt</td><td>√</td><td>√</td><td>-</td><td>-</td><td>gpt2-xl-1.5b,gpt-neo,gpt-neox,opt-175b</td><td>首个使用 in-context learning（ICL）进行 LLM 编辑的方法。</td><td>2023</td></tr><tr><td>MeLLo [376]</td><td>prompt</td><td>√</td><td>√</td><td>-</td><td>-</td><td rowspan="2">vicuna-7b,gpt-j-6bbert-base,gpt-2,t5-xl,gpt-j-6b</td><td>结合问题分解与自检进行编辑。</td><td>2023</td></tr><tr><td>MALMEN [267]</td><td>元学习</td><td>✕</td><td>✕</td><td>√</td><td>✕</td><td>使用最小二乘可靠地合并编辑，并解耦网络以节省内存，支持大规模批量编辑。</td><td>2023</td></tr><tr><td>MEMIT [205]</td><td>先定位后编辑</td><td>✕</td><td>√</td><td>√</td><td>✕</td><td>gpt-j-6b,gpt-neox-20b</td><td>优化松弛的最小二乘目标，为大规模批量编辑提供闭式解。</td><td>2022</td></tr><tr><td>ROME [203]</td><td>先定位后编辑</td><td>✕</td><td>√</td><td>✕</td><td>✕</td><td>gpt2-xl-1.5b</td><td>经典的先定位后编辑方法，在单个 MLP 层上执行秩一更新。</td><td>2022</td></tr><tr><td>CaliNET [60]</td><td>附加参数</td><td>√</td><td>✕</td><td>√</td><td>✕</td><td>t5-base,t5-large</td><td>添加类 FFN 的校准层以高效修改输出。</td><td>2022</td></tr><tr><td>SERAC [212]</td><td>附加参数</td><td>√</td><td>✕</td><td>√</td><td>√</td><td>t5-large,bert-base,blenderbot-90m</td><td>结合 Scope Classifier 与 Counterfactual Model，支持顺序或同时编辑并保持结果一致。</td><td>2022</td></tr><tr><td>GRACE [212]</td><td>附加参数</td><td>√</td><td>✕</td><td>✕</td><td>√</td><td rowspan="2">t5-small,bert-base,gpt2-xl-1.5bgpt-neo,gpt-j-6b,t5-xl,t5-xxl,bert-base,bart-base</td><td>使用带延迟机制（deferral mechanism）的码本（codebook）支持顺序编辑。</td><td>2022</td></tr><tr><td>MEND [211]</td><td>元学习</td><td>✕</td><td>✕</td><td>√</td><td>✕</td><td>将梯度更新分解为秩一外积，以实现可扩展、快速的编辑。</td><td>2021</td></tr><tr><td>KE [50]</td><td>元学习</td><td>✕</td><td>✕</td><td>√</td><td>✕</td><td>bert-base,bart-base</td><td>首个使用超网络将句子 embedding 投影为秩 1 梯度掩码的方法。</td><td>2021</td></tr></table>

表 13. 编辑中的 parametric memory 优化方法概览。"PR"（Parametric Reserving）表示模型权重是否保持不变。"TF"（Training-Free）表示是否无需迭代优化即可完成编辑。"BES"（Batch Editing Support）标示批量编辑能力。"SEO"（Sequential Editing Optimization）表示针对顺序编辑的专门机制。"LMs" 列出实验所用的语言模型。

<table><tr><td>方法</td><td>类型</td><td>PR</td><td>TF</td><td>BUS</td><td>SUO</td><td>语言模型</td><td>主要改进</td><td>年份</td></tr><tr><td>ULD[118]</td><td>附加参数</td><td>√</td><td>✗</td><td>√</td><td>✗</td><td>llama2-chat-7b, mistral-7b-instruct</td><td>通过计算目标模型与助手模型之间的 logit 差异，得到 forgetting 后的 LLM。</td><td>2024</td></tr><tr><td>ECO[173]</td><td>prompt</td><td>√</td><td>✗</td><td>√</td><td>✗</td><td>68 LLMs ranging from 0.5B to 236B</td><td>通过破坏由分类器检测到的 prompt embedding 来执行 forgetting，而不改变模型权重。</td><td>2024</td></tr><tr><td>WAGLE[119]</td><td>先 locate-then-unlearn</td><td>✗</td><td>✗</td><td>√</td><td>✗</td><td>llama2-7b-chat, zephyr-7b-beta, llama2-7b</td><td>使用双层优化计算权重归因分数，以选择性 fine-tuning 实现高效、模块化的 forgetting。</td><td>2024</td></tr><tr><td>SOUL[120]</td><td>训练目标</td><td>✗</td><td>✗</td><td>√</td><td>√</td><td>opt-1.3b, llama2-7b</td><td>利用二阶优化器实现更有效的 LLM forgetting。</td><td>2024</td></tr><tr><td>SKU[185]</td><td>训练目标</td><td>✗</td><td>✗</td><td>√</td><td>√</td><td>opt-2.7b, llama2-7b, llama2-13b</td><td>在两阶段框架中结合有害知识学习与任务向量取反，实现鲁棒 forgetting。</td><td>2024</td></tr><tr><td>EUL[30]</td><td>附加参数</td><td>√</td><td>✗</td><td>√</td><td>√</td><td>t5-base, t5-3b</td><td>引入 unlearning 层以遗忘特定数据，并通过融合机制合并多个层以支持顺序 forgetting。</td><td>2023</td></tr><tr><td>ICUL[231]</td><td>prompt</td><td>√</td><td>√</td><td>-</td><td>-</td><td>bloom-560m, bloom-1.1b, bloom-3b, llama2-7b</td><td>首个利用 in-context learning（ICL）在语言模型中进行 forgetting 的方法。</td><td>2023</td></tr><tr><td>GA+Mismatch[343]</td><td>训练目标</td><td>✗</td><td>✗</td><td>√</td><td>✗</td><td>opt-1.3b, opt-2.7b, llama2-7b</td><td>开创 LLM forgetting，混合 forgetting、随机失配与基于 KL 的保留目标。</td><td>2023</td></tr><tr><td>KGA[286]</td><td>训练目标</td><td>✗</td><td>✗</td><td>√</td><td>✗</td><td>bart-base, distil-bert, lstm</td><td>通过分布散度最小化对齐保留模型与 forgetting 模型之间的知识差距，以模拟 forgetting。</td><td>2023</td></tr><tr><td>DEPN[317]</td><td>先 locate-then-unlearn</td><td>√</td><td>√</td><td>√</td><td>✗</td><td>bert-base</td><td>检测并禁用与隐私相关的神经元，以减少语言模型中的敏感数据泄漏。</td><td>2023</td></tr></table>

表 14. machine unlearning 中的 parametric memory 优化方法概览。"PR"（Parametric Reserving）表示该方法是否避免直接修改内部权重。"TF"（Training-Free）表示该方法是否无需迭代优化即可运行。"BUS"（Batch Unlearning Support）标示对同时多次编辑的支持。"SUO"（Sequential Unlearning Optimization）表示顺序 forgetting 能力。"LMs" 列出实验所用的语言模型。

<table><tr><td>方法</td><td>类型</td><td>TF</td><td>TB</td><td>TS</td><td>领域</td><td>语言模型</td><td>主要改进</td><td>年份</td></tr><tr><td>HippoRAG 2[85]</td><td></td><td>✗</td><td>✗</td><td>无任务</td><td>问答</td><td></td><td>采用一个训练目标，最小化原始模型与目标模型预测之间的 Kullback-Leibler（KL）散度。增强个性化</td><td>2025</td></tr><tr><td>SELF-PARAM[302]</td><td>基于正则化的学习</td><td>√</td><td>√</td><td>无任务</td><td>问答</td><td>Llama-3.3-70B-Instruct</td><td>基于 PageRank 的 retrieval，配合更深的段落 consolidation 与在线 LLM 使用，在事实性、联想性与意义建构类 memory 任务上取得更优表现。</td><td>2025</td></tr><tr><td>MBPA++[301]</td><td>基于回放</td><td>✗</td><td>✗</td><td>CIL</td><td>无</td><td>REPLAY, MBPA</td><td>在 memory 中保留一小部分（低至 1%）随机选择的过往样本，以达到与更大 memory 规模相当的性能。</td><td>2025</td></tr><tr><td>LSCS[301]</td><td>交互式学习</td><td>✗</td><td>✗</td><td>CIL</td><td>抽象/合并/retrieval</td><td>/</td><td>整合多种存储机制，以实现抽象、经验合并与带准确召回的长期保持。</td><td>2025</td></tr><tr><td>TaSL[73]</td><td>基于正则化的学习</td><td>✗</td><td>✗</td><td>TIL</td><td>对话系统</td><td>T5, Llama-7B</td><td>参数级的任务技能定位与 consolidation，使知识可在无 memory 回放的情况下迁移。</td><td>2024</td></tr><tr><td>EMP[178]</td><td>基于回放</td><td>✗</td><td>✗</td><td>CLI</td><td>事件检测</td><td rowspan="2">BERT-ED, KCnoEWC, SI, LwF,A-GEM,CLS-ER, ESM,etc.</td><td>设计与各事件类型关联的连续 prompt。引入自适应系数</td><td>2023</td></tr><tr><td>UDIL[253]</td><td>交互式学习</td><td>✗</td><td>√</td><td>DLI</td><td>事件检测</td><td>训练中优化，以实现更紧的泛化误差界与跨领域性能改进。</td><td>2023</td></tr><tr><td>DSI++[200]</td><td>基于回放</td><td>✗</td><td>√</td><td>TIL</td><td>信息 retrieval</td><td>T5</td><td rowspan="2">支持持续文档 indexing，同时保留对旧数据与新数据的查询性能。通过压缩数据增强 memory 回放，平衡样本质量与数量以支持 continual learning。</td><td>2022</td></tr><tr><td>MRDC[288]</td><td>基于回放</td><td>✗</td><td>√</td><td>CIL</td><td>目标检测</td><td>LUCIR,PODNet</td><td>2022</td></tr></table>

表 15. continual learning 中的 parametric memory modification 方法概览。"TB" 表示是否存在任务边界。"TS" 表示任务设定，包括 TIL（Task Incremental Learning，任务增量学习）、CIL（Class Incremental Learning，类增量学习）、DIL（Domain Incremental Learning，领域增量学习）与无任务（Task-Free）。

<table><tr><td>方法</td><td>类型</td><td>TF</td><td>来源类型</td><td>来源数据集</td><td>输入</td><td>输出</td><td>语言模型</td><td>操作</td><td>特性</td><td>年份</td></tr><tr><td>GoG[331]</td><td>reasoning</td><td>√</td><td>KG + 文本</td><td>WebQSP, CWQ</td><td>KG + prompt + 查询</td><td>答案</td><td>GPT-3.5, GPT-4, Qwen-1.5-72B-Chat, LLaMA3-70B-Instruct</td><td>retrieval、compression</td><td>整合内部与外部知识</td><td>2024</td></tr><tr><td>RKC-LLM[299]</td><td>冲突</td><td>√</td><td>模型 + 文本</td><td>prompt + context</td><td>实体</td><td>答案</td><td>ChatGPT</td><td>compression</td><td>冲突片段定位、指令引导的冲突处理</td><td>2024</td></tr><tr><td>BGC-KC[268]</td><td>冲突</td><td>√</td><td>模型 + 文本</td><td>AIG, AIR</td><td>文档 + 查询</td><td>答案</td><td>GPT-4, GPT-3.5, Llama2-13b, Llama2-7b</td><td>retrieval、compression</td><td>归因追踪框架、评估 LLM 偏差</td><td>2024</td></tr><tr><td>Sem-CoT[260]</td><td>reasoning</td><td>✗</td><td>knowledge graph + 文本 + 模型</td><td>Wikidata, 2Wiki, MuSiQue, TKB</td><td>CoT prompt + 查询</td><td>答案</td><td>LLaMA2-7B, 13B, 70B, 65B</td><td>retrieval、compression</td><td>面向 multi-source 输入 fusion 的半结构化 prompt</td><td>2023</td></tr><tr><td>CoK[161]</td><td>reasoning</td><td>✗</td><td>数据库 + 表格 + 文本</td><td>Wikidata, Wikipedia, Wikitables, Flashcard, UpToDate, ScienceQA, CK-12</td><td>CoT prompt + 查询</td><td>答案</td><td>GPT-3.5-turbo</td><td>retrieval、compression</td><td>异构知识整合、动态知识 retrieval、跨格式自适应查询生成</td><td>2023</td></tr><tr><td>DIVKNOWQA[369]</td><td>reasoning</td><td>✗</td><td>知识库 + 文本</td><td>Wikidata, DIVKNOWQA</td><td>CoT prompt + 查询</td><td>答案</td><td>GPT-3.5-turbo</td><td>retrieval、compression</td><td>两跳推理、面向结构化数据的符号查询生成</td><td>2023</td></tr><tr><td>StructRAG[165]</td><td>reasoning</td><td>✗</td><td>KG + 表格 + 文本</td><td>Loong, Podcast Transcripts</td><td>文档 + 查询</td><td>答案</td><td>Qwen2-7B, 72B</td><td>retrieval、compression</td><td>认知启发的结构化、动态结构选择</td><td>2023</td></tr></table>

表 16. cross-textual integration 中的 multi-source memory 方法概览。"TF"（Training Free）表示该方法是否无需额外的基于梯度的更新即可运行。"STs" 表示来源类型。"SNs" 表示来源数据集名称。

<table><tr><td>方法</td><td>类型</td><td>TF</td><td>来源类型</td><td>来源数据集</td><td>输入</td><td>输出</td><td>语言模型</td><td>操作</td><td>特性</td><td>年份</td></tr><tr><td>GoG[331]</td><td>reasoning</td><td>√</td><td>KG + 文本</td><td>WebQSP, CWQ</td><td>KG + prompt + 查询</td><td>答案</td><td>GPT-3.5, GPT-4, Qwen-1.5-72B-Chat, LLaMA3-70B-Instruct</td><td>retrieval、compression</td><td>整合内部与外部知识</td><td>2024</td></tr><tr><td>RKC-LLM[299]</td><td>冲突</td><td>√</td><td>模型 + 文本</td><td>prompt + context</td><td>实体</td><td>答案</td><td>ChatGPT</td><td>compression</td><td>冲突片段定位、指令引导的冲突处理</td><td>2024</td></tr><tr><td>BGC-KC[268]</td><td>冲突</td><td>√</td><td>模型 + 文本</td><td>AIG, AIR</td><td>文档 + 查询</td><td>答案</td><td>GPT-4, GPT-3.5, Llama2-13b, Llama2-7b</td><td>retrieval、compression</td><td>归因追踪框架、评估 LLM 偏差</td><td>2024</td></tr><tr><td>Sem-CoT[260]</td><td>reasoning</td><td>✗</td><td>knowledge graph + 文本 + 模型</td><td>Wikidata, 2Wiki, MuSiQue, TKB</td><td>CoT prompt + 查询</td><td>答案</td><td>LLaMA2-7B, 13B, 70B, 65B</td><td>retrieval、compression</td><td>面向 multi-source 输入 fusion 的半结构化 prompt</td><td>2023</td></tr><tr><td>CoK[161]</td><td>reasoning</td><td>✗</td><td>数据库 + 表格 + 文本</td><td>Wikidata, Wikipedia, Wikitables, Flashcard, UpToDate, ScienceQA, CK-12</td><td>CoT prompt + 查询</td><td>答案</td><td>GPT-3.5-turbo</td><td>retrieval、compression</td><td>异构知识整合、动态知识 retrieval、跨格式自适应查询生成</td><td>2023</td></tr><tr><td>DIVKNOWQA[369]</td><td>reasoning</td><td>✗</td><td>知识库 + 文本</td><td>Wikidata, DIVKNOWQA</td><td>CoT prompt + 查询</td><td>答案</td><td>GPT-3.5-turbo</td><td>retrieval、compression</td><td>两跳推理、面向结构化数据的符号查询生成</td><td>2023</td></tr><tr><td>StructRAG[165]</td><td>reasoning</td><td>✗</td><td>KG + 表格 + 文本</td><td>Loong, Podcast Transcripts</td><td>文档 + 查询</td><td>答案</td><td>Qwen2-7B, 72B</td><td>retrieval、compression</td><td>认知启发的结构化、动态结构选择</td><td>2023</td></tr></table>

表 17. cross-textual integration 中的 multi-source memory 方法概览。"TF"（Training Free）表示该方法是否无需额外的基于梯度的更新即可运行。"STs" 表示来源类型。"SNs" 表示来源数据集名称

<table><tr><td>memory tools</td><td>层级</td><td>分类</td><td>操作</td><td>功能</td><td>输入/输出</td><td>示例用途</td><td>来源类型</td></tr><tr><td>FAISS [61]</td><td>组件</td><td>contextual-unstructured</td><td>consolidation、indexing、retrieval</td><td>用于高维向量快速存储、indexing 与 retrieval 的库</td><td>向量/indexing，相关性分数</td><td>向量数据库——对大量 text embeddings 构建 index，并在 RAG 系统中为查询 retrieval 最相关的文档。</td><td>open</td></tr><tr><td>Neo4j [216]</td><td>组件</td><td>contextual-structured</td><td>consolidation、indexing、updating、retrieval</td><td>支持 ACID 事务与 Cypher 查询语言的原生图数据库</td><td>带属性的节点与关系 / 通过 Cypher 查询的结果</td><td>图数据库——为欺诈检测与推荐引擎等任务建模并 retrieval 复杂关系数据。</td><td>conditional open</td></tr><tr><td>BM25 [243]</td><td>组件</td><td>contextual-unstructured</td><td>retrieval</td><td rowspan="2">一种用于信息 retrieval 的概率排序函数，用于估计文档与给定查询的相关性。一种以对比学习训练的无监督稠密 retriever，可跨语言 retrieval 语义相似的文档。</td><td>文本查询 / 排序后的文档列表</td><td>改进搜索引擎结果与文档 retrieval 系统。</td><td>open</td></tr><tr><td>Contriever [113]</td><td>组件</td><td>contextual-unstructured</td><td>retrieval</td><td>查询文本 / 相似文档列表</td><td>多语言问答系统中的高召回 retrieval 任务。</td><td>open</td></tr><tr><td>Embedding Models (e.g., OpenAI embeddings [224])</td><td>组件</td><td>context</td><td>consolidation、retrieval</td><td>将文本、图像或音频转换为捕获语义的稠密向量表示的技术。</td><td>原始数据 / vector embeddings</td><td>文本相似度计算、推荐系统与聚类任务。</td><td>open</td></tr></table>

表 18. memory management 与利用的组件级工具。

<table><tr><td>memory tools</td><td>层级</td><td>分类</td><td>操作</td><td>功能</td><td>输入/输出</td><td>示例用途</td><td>来源类型</td></tr><tr><td>Graphiti [92]</td><td>框架</td><td>contextual-structured</td><td>consolidation、indexing、updating、retrieval</td><td>用于构建与查询面向动态环境中 AI agent 的时间感知 knowledge graph 的框架。</td><td>multi-source 数据 / 可查询的 knowledge graph</td><td>构建实时 knowledge graph 以增强 AI agent memory。</td><td>open</td></tr><tr><td>LLamaIndex [175]</td><td>框架</td><td>context</td><td>consolidation、indexing、retrieval</td><td>用于构建连接企业数据的 LLM 知识助手的灵活框架。</td><td>文本 / context 增强的响应</td><td>开发处理复杂数据格式的知识助手。</td><td>open</td></tr><tr><td>LangChain [28]</td><td>框架</td><td>context</td><td>consolidation、indexing、updating、forgetting、retrieval</td><td>通过将 LLM 与外部数据源连接，提供构建 context-aware 推理应用的框架。</td><td>输入 prompt / 多步推理输出</td><td>创建问答系统与聊天机器人等复杂 LLM 应用。</td><td>open</td></tr><tr><td>LangGraph [112]</td><td>框架</td><td>contextual-structured</td><td>consolidation、indexing、updating、forgetting、retrieval</td><td>构建支持 long-term memory 与人在回路（human-in-the-loop）多 agent 系统的可控 agent 架构。</td><td>图状态 / 状态更新</td><td>用多个 AI agent 构建复杂任务工作流。</td><td>open</td></tr><tr><td>EasyEdit [291]</td><td>框架</td><td>parametric</td><td>updating</td><td>面向 LLM 的易用 knowledge editing 框架，可在特定领域内高效修改行为。</td><td>编辑指令 / 更新后的模型行为</td><td>修改 LLM 在特定领域的知识，例如更新事实信息。</td><td>open</td></tr><tr><td>CrewAI [66]</td><td>框架</td><td>context</td><td>consolidation、indexing、retrieval</td><td>用于构建与部署多 agent 系统的平台，支持使用任意 LLM 与云平台的自动化工作流。</td><td>多 agent 任务 / 协作结果</td><td>在项目管理与内容生成等 agent 之间自动化工作流。</td><td>open</td></tr><tr><td>Letta [226]</td><td>框架</td><td>contextual-unstructured</td><td>consolidation、retrieval</td><td>在可视化环境中构建具有 long-term memory、高级推理与自定义工具的有状态 agent。</td><td>用户交互 / 改进后的响应</td><td>开发随时间学习与改进的 AI agent。</td><td>open</td></tr></table>

表 19. memory management 与利用的框架级工具。

<table><tr><td>memory tools</td><td>层级</td><td>分类</td><td>操作</td><td>功能</td><td>输入/输出</td><td>示例用途</td><td>来源类型</td></tr><tr><td>MemOS [168]</td><td>应用层</td><td>contextual-structured</td><td>consolidation、updating、retrieval</td><td>类操作系统架构，管理分层 memory（工作、短期、长期）以优化 memory-augmented 生成。</td><td>agent 查询、复杂 context / 分层 memory 块</td><td>为处理多步推理与 long-horizon 任务的 agent 管理复杂 memory 资源。</td><td>open</td></tr><tr><td>O-Mem [290]</td><td>应用层</td><td>contextual-unstructured</td><td>consolidation、updating、retrieval</td><td>全 memory system，通过递归 memory consolidation 使 agent 自我演进并保持 long-horizon 一致性。</td><td>长期交互日志 / 演进后的 memory 状态</td><td>创建随时间适应用户成长的自演进个人 AI 助手。</td><td>open</td></tr><tr><td>Mem0 [255]</td><td>应用层</td><td>contextual-unstructured</td><td>consolidation、indexing、updating、retrieval</td><td>为 LLM 提供智能 memory 层，支持在模型中直接添加、更新与搜索 memory。</td><td>用户交互 / 个性化响应</td><td>为客户支持与个性化推荐增强带持久 context 的 AI 系统。</td><td>open</td></tr><tr><td>Zep [239]</td><td>应用层</td><td>contextual-structured</td><td>consolidation、indexing、updating、retrieval</td><td>将聊天消息整合进 knowledge graph，提供准确、相关的用户信息。</td><td>聊天日志、业务数据 / knowledge graph 查询结果</td><td>通过从用户交互中 continual learning，为 AI agent 增强知识。</td><td>open</td></tr><tr><td>Memory [140]</td><td>应用层</td><td>context</td><td>consolidation、indexing、updating、retrieval</td><td>开放 memory 层，模拟人类 memory 以帮助 AI agent 有效管理与利用信息。</td><td>agent 任务 / memory management 与利用</td><td>构建具有类人 memory 特征的 AI agent。</td><td>open</td></tr><tr><td>Memobase [202]</td><td>应用层</td><td>context</td><td>consolidation、indexing、updating、retrieval</td><td>基于用户画像的 long-term memory 系统，旨在为生成式 AI 应用提供个性化体验。</td><td>用户交互 / 个性化响应</td><td>实现虚拟助手、教育工具与个性化 AI 伴侣。</td><td>open</td></tr><tr><td>Me.bot [209]</td><td>产品</td><td>context</td><td>consolidation、indexing、updating、retrieval</td><td>AI 驱动的个人助理，组织笔记、任务与 memory，提供情感支持与生产力工具。</td><td>用户输入（文本、语音）/ 组织后的笔记、提醒、摘要</td><td>个人生产力提升、情感支持、想法组织。</td><td>closed</td></tr><tr><td>ima.copilot [276]</td><td>产品</td><td>context</td><td>consolidation、indexing、updating、retrieval</td><td>由腾讯的 Mix Huang 模型驱动的智能工作台，为学习与工作场景构建个人知识库。</td><td>用户查询 / 定制化响应、知识 retrieval</td><td>提升学习效率、工作效率、知识管理。</td><td>closed</td></tr><tr><td>Coze [44]</td><td>产品</td><td>context</td><td>consolidation</td><td>支持跨多种平台的多 agent 协作。</td><td rowspan="2">用户自定义工作流 / 响应；查询 / 信息性答案、生成图像</td><td>已部署的聊天机器人、AI agent</td><td>closed</td></tr><tr><td>Grok [321]</td><td>产品</td><td>context</td><td>retrieval、compression</td><td>由 xAI 开发的 AI 助手，旨在提供真实、有用且好奇的响应，具备实时数据访问与图像生成能力。</td><td>回答问题、生成图像、提供洞见。</td><td>closed</td></tr><tr><td>ChatGPT [223]</td><td>产品</td><td>context</td><td>consolidation、retrieval</td><td>OpenAI 开发的 session 式 AI，可根据 prompt 理解并生成类人文本。</td><td>用户 prompt / 生成的文本响应</td><td>回答问题、生成图像、提供洞见。</td><td>closed</td></tr><tr><td>Replika [191]</td><td>产品</td><td>context</td><td>consolidation、updating、retrieval</td><td>维持纵向交互历史以实现情感连续性的 AI 伴侣。</td><td>文本输入 / 情感响应式对话</td><td>情感支持、心理健康、模拟陪伴。</td><td>closed</td></tr><tr><td>Amazon Recommender [170]</td><td>产品</td><td>context</td><td>consolidation、retrieval、indexing</td><td>使用行为 memory 痕迹的个性化推荐引擎。</td><td>用户行为日志 / 排序后的商品推荐</td><td>电商个性化、客户画像、定向营销。</td><td>closed</td></tr><tr><td>GitHub Copilot [79]</td><td>产品</td><td>context</td><td>retrieval、compression</td><td>基于编码历史与文件 context 提供建议的代码助手。</td><td>代码编辑器 context / 代码补全、代码片段</td><td>编程辅助、自动补全、context 理解。</td><td>closed</td></tr><tr><td>CodeBuddy [42]</td><td>产品</td><td>context</td><td>retrieval、compression</td><td>AI 代码助手。</td><td>代码与编辑 / 个性化编码建议</td><td>习惯感知的代码生成、交互式开发支持。</td><td>closed</td></tr><tr><td>Doubao [22]</td><td>产品</td><td>context</td><td>consolidation、retrieval</td><td>高效多模态 AI 助手，能处理 long-context 交互与多样日常任务。</td><td>文本、语音、图像输入 / 答案、创意内容</td><td>日常对话、写作辅助、编码支持与角色扮演。</td><td>closed</td></tr><tr><td>Siri [11]</td><td>产品</td><td>context</td><td>consolidation、retrieval</td><td>利用设备端个人 semantic memory 实现 context-aware 与跨应用操作的智能语音助手。</td><td>语音命令 / 动作执行、个人信息 retrieval</td><td>设备控制、retrieval 个人 context（例如航班日程）与跨应用任务。</td><td>closed</td></tr><tr><td>Xiaoyi [109]</td><td>产品</td><td>context</td><td>consolidation、retrieval</td><td>集成于 HarmonyOS 的智能助手，利用生态级 memory 提供主动服务与文档理解。</td><td>语音、文本、文档 / 摘要、建议、IoT 控制</td><td>文档摘要、智能家居控制与个性化出行规划。</td><td>closed</td></tr></table>

表 20. memory management 与利用的应用层级工具。

表 21. memory utilization 的产品级工具。
