---
stem: arxiv-2404.13501.Survey.Memory Mechanism
id: arxiv-2404.13501
keywords: [memory, agent, survey]
abstract: "基于 LLM 的 agent 近来受到研究与产业界的广泛关注。与原始 LLM 相比，LLM-based agent 以 self-evolving 能力为特征，而这一能力是解决需要长期、复杂 agent-environment interaction 的现实问题的基础。支撑 agent-environment interaction 的关键组件是 agent 的 memory。尽管已有研究提出了许多有前景的 memory mechanism，但它们散落在不同论文中，缺乏从整体视角对这些工作进行系统梳理与比较的综述，因而未能抽象出可启发后续研究的共性、有效设计模式。为弥补这一空白，本文对 LLM-based agent 的 memory mechanism 进行了全面综述。具体而言，我们首先讨论 LLM-based agent 中 memory“是什么”以及“为什么需要”。随后，我们系统回顾关于如何设计与评估 memory module 的已有研究。此外，我们还介绍许多 memory module 发挥重要作用的 agent application。最后，我们分析现有工作的局限并提出重要的未来方向。为跟进该领域的最新进展，我们建立了仓库：https://github.com/nuster1128/LLM_Agent_Memory_Survey。"
revised: 2024-04-21
source: "https://arxiv.org/abs/2404.13501"
parser: mineru-cloud 3.4.4
---

> 本文为 AI 译文。翻译模型：DeepSeek-V4.1-Flash；翻译日期：2026-11-02；源文件：arxiv-2404.13501.Survey.Memory Mechanism.md。

# A Survey on the Memory Mechanism of Large Language Model based Agents

Zeyu Zhang<sup>1</sup>, Xiaohe Bo<sup>1</sup>, Chen Ma<sup>1</sup>, Rui Li<sup>1</sup>, Xu Chen<sup>1</sup>, Quanyu Dai<sup>2</sup>, Jieming Zhu<sup>2</sup>, Zhenhua Dong<sup>2</sup>, Ji-Rong Wen<sup>1</sup>

<sup>1</sup>Gaoling School of Artificial Intelligence, Renmin University of China, Beijing, China <sup>2</sup>Huawei Noah’s Ark Lab, China zeyuzhang@ruc.edu.cn, xu.chen@ruc.edu.cn

## 摘要

基于 LLM 的 agent 近来受到研究与产业界的广泛关注。与原始 LLM 相比，LLM-based agent 以 self-evolving 能力为特征，而这一能力是解决需要长期、复杂 agent-environment interaction 的现实问题的基础。支撑 agent-environment interaction 的关键组件是 agent 的 memory。尽管已有研究提出了许多有前景的 memory mechanism，但它们散落在不同论文中，缺乏从整体视角对这些工作进行系统梳理与比较的综述，因而未能抽象出可启发后续研究的共性、有效设计模式。为弥补这一空白，本文对 LLM-based agent 的 memory mechanism 进行了全面综述。具体而言，我们首先讨论 LLM-based agent 中 memory“是什么”以及“为什么需要”。随后，我们系统回顾关于如何设计与评估 memory module 的已有研究。此外，我们还介绍许多 memory module 发挥重要作用的 agent application。最后，我们分析现有工作的局限并提出重要的未来方向。为跟进该领域的最新进展，我们建立了仓库：https://github.com/nuster1128/LLM_Agent_Memory_Survey。

![](../assets/arxiv-2404.13501-fig1.jpg)  
图 1：memory module 在 LLM-based agent 中的重要性。

## 目录

1 Introduction 4
2 Related Surveys 5
2.1 Surveys on Large Language Models 5
2.2 Surveys on Large Language Model-based Agents 7
3 What is the Memory of LLM-based Agent 7
3.1 Basic Knowledge 7
3.2 Narrow Definition of the Agent Memory 9
3.3 Broad Definition of the Agent Memory 9
3.4 Memory-assisted Agent-Environment Interaction 9
4 Why We Need the Memory in LLM-based Agent 10
4.1 Perspective of Cognitive Psychology 10
4.2 Perspective of Self-Evolution 11
4.3 Perspective of Agent Applications 11
5 How to Implement the Memory of LLM-based Agent 11
5.1 Memory Sources 11
5.1.1 Inside-trial Information 12
5.1.2 Cross-trial Information 13
5.1.3 External Knowledge 13
5.2 Memory Forms 13
5.2.1 Memory in Textual Form 14
5.2.2 Memory in Parametric Form 16
5.2.3 Advantages and Disadvantages of Textual and Parametric Memory 17
5.3 Memory Operations 18
5.3.1 Memory Writing 18
5.3.2 Memory Management 18
5.3.3 Memory Reading 19
6 How to Evaluate the Memory in LLM-based Agent 20
6.1 Direct Evaluation 20
6.1.1 Subjective Evaluation 20
6.1.2 Objective Evaluation 21
6.2 Indirect Evaluation 22
6.2.1 Conversation 22
6.2.2 Multi-source Question-answering 22
6.2.3 Long-context Applications 22
6.2.4 Other Tasks 23
6.3 Discussions 23
7 Memory-enhanced Agent Applications 23
7.1 Role-playing and Social Simulation 23
7.2 Personal Assistant 25
7.3 Open-world Game 25
7.4 Code Generation 25
7.5 Recommendation 26
7.6 Expert System in Specific Domains 26
7.7 Other Applications 26
8 Limitations & Future Directions 27
8.1 More Advances in Parametric Memory 27
8.2 Memory in LLM-based Multi-agent Applications 27
8.3 Memory-based Lifelong Learning 28
8.4 Memory in Humanoid Agent 28
9 Conclusion 28

## 1 Introduction

没有记忆，就没有文化。没有记忆，就没有文明、没有社会、没有未来。

Elie Wiesel，1928—2016

近来，large language models（LLMs）在从人工智能、软件工程到教育与社会科学的众多领域取得了显著成功 [1–3]。原始 LLM 通常在不与环境交互的情况下完成不同任务。然而，要实现通用人工智能（AGI）的最终目标，智能机器应能够通过自主探索真实世界并从中学习来改进自身。例如，若一个旅行规划 agent 打算预订机票，它应向票务网站发送订单请求，并在采取下一动作前观察响应。personal assistant agent 应根据用户反馈调整其行为，提供个性化回复以提升用户满意度。为进一步把 LLM 的边界推向 AGI，近年来出现了大量关于 LLM-based agent 的研究 [3, 4]，其关键是给 LLM 配备额外模块，以增强其在真实环境中的 self-evolving 能力。

在所有新增模块中，memory 是使 agent 区别于原始 LLM、使 agent 真正成为 agent 的关键组件（见图 1）。它在决定 agent 如何积累知识、处理历史经验、retrieve 有用知识以支持其动作等方面发挥着极其重要的作用。围绕 memory module，人们已投入大量精力设计其信息来源、存储形式与操作机制。例如，Shinn 等人 [5] 同时纳入 inside-trial 与 cross-trial information 来构建 memory module，以增强 agent 的推理能力。Zhong 等人 [6] 以自然语言形式存储 memory information，这种形式可解释且对用户友好。Modarressi 等人 [7] 设计了 memory reading 与 memory writing 操作，以与环境交互来求解任务。

尽管已有研究设计了许多有前景的 memory module，但仍缺乏从整体视角审视 memory module 的系统性研究。为弥补这一空白，本文全面回顾已有研究，给出清晰分类体系以及设计与评估 memory module 的关键原则。具体而言，我们讨论三个关键问题：（1）LLM-based agent 的 memory 是什么？（2）为什么 LLM-based agent 需要 memory？（3）如何实现与评估 LLM-based agent 中的 memory？首先，我们详述 LLM-based agent 中 memory 的概念，给出狭义与广义两种定义。然后，我们分析 memory 在 LLM-based agent 中的必要性，从认知心理学、self-evolution 与 agent application 三个视角说明其重要性。在“是什么”与“为什么”的基础上，我们介绍设计与评估 memory module 的常用策略。在 memory 设计方面，我们从 memory source、memory form 与 memory operation 三个维度讨论已有工作。在 memory evaluation 方面，我们介绍两种广泛使用的方法，包括直接评估与通过特定 agent 任务进行的间接评估。随后，我们讨论角色扮演、社会模拟、个人助理、开放世界游戏、代码生成、推荐与专家系统等 agent application，以展示 memory module 在实际场景中的重要性。最后，我们分析现有工作的局限并指出重要的未来方向。

本文的主要贡献可概括如下：（1）我们形式化定义了 memory module，并全面分析其对 LLM-based agent 的必要性。（2）我们系统总结 LLM-based agent 中 memory module 的设计与评估研究，给出清晰的分类体系与直观洞见。（3）我们给出典型的 agent application，以展示 memory module 在不同场景中的重要性。（4）我们分析现有 memory module 的关键局限，并提出可启发后续研究的潜在解决方案。据我们所知，这是首篇关于 LLM-based agent memory mechanism 的综述。

本文其余部分组织如下。首先，第 2 节对 LLM 与 LLM-based agent 领域进行系统性的元综述，对不同类型的综述进行分类并总结其主要贡献。然后，第 3 至 6 节讨论 LLM-based agent 中 memory module 的“是什么”“为什么需要”以及“如何实现与评估”问题。接着，第 7 节展示 memory-enhanced agent 的应用。关于现有工作局限与未来方向的讨论最后见于第 8 节与第 9 节。

## 2 Related Surveys

过去两年，LLM 受到学术界与产业界的广泛关注。为系统总结该领域的研究，研究者撰写了大量综述论文。本节简要回顾这些综述（总体见图 2），突出其主要关注点与贡献，以便更好地定位本文研究。

## 2.1 Surveys on Large Language Models

在 LLM 领域，Zhao 等人 [70] 给出了首篇全面综述，总结了 LLM 的背景、演进路径、模型架构、训练方法与评估策略。Hadi 等人 [71] 与 Min 等人 [72] 也从整体视角开展了 LLM 综述，但它们给出了不同的分类体系与理解。沿着这些综述，人们深入 LLM 的特定方面，回顾相应的里程碑研究与关键技术。这些方面可分为四类，包括 LLM 的基础问题、评估、应用与挑战。

基础问题。这一类的综述旨在总结可用于解决 LLM 基础问题的技术。具体而言，Zhang 等人 [8] 对 supervised fine-tuning 方法进行了全面综述，这是更好地训练 LLM 的关键技术。Shen 等人 [9]、Wang 等人 [10] 与 Liu 等人 [11] 综述了 LLM 的对齐，这是 LLM 产生与人类价值观一致输出的关键要求。Gao 等人 [12] 综述了 LLM 的 retrieval-augmented generation（RAG）能力，这是为 LLM 提供事实性与最新知识、消除幻觉的关键。Qin 等人 [18] 总结了使 LLM 利用外部工具的最新方法，这对于 LLM 在需要专门知识的领域扩展能力至关重要。Wang 等人 [13]、Yao 等人 [14]、Wang 等人 [15]、Feng 等人 [16] 与 Zhang 等人 [17] 综述了 LLM 知识编辑方向，这对于定制 LLM 以满足特定需求十分重要。Huang 等人 [19]、Wang 等人 [20] 与 Pawar 等人 [21] 关注 LLM 的 long-context 能力，这对于 LLM 每次处理更多信息、增强其应用场景至关重要。Wu 等人 [22]、Song 等人 [23]、Caffagni 等人 [24] 与 Yin 等人 [25] 总结了多模态 LLM，这使 LLM 的能力从文本扩展到视觉及其他模态。上述综述主要关注 LLM 的有效性。LLM 的另一个重要方面是训练与推理效率。为总结这一方面的研究，Zhu 等人 [30]、Xu 与 McAuley [31]、Wang 等人 [32] 与 Park 等人 [33] 系统回顾了模型压缩技术。Ding 等人 [81] 与 Xu 等人 [29] 分析并总结了 parameter-efficient fine-tuning 研究。Bai 等人 [26]、Wan 等人 [27]、Miao 等人 [28] 与 Ding 等人 [81] 更关注一般意义上的资源利用效率。

评估。这一类的综述关注如何评估 LLM 的能力。具体而言，Chang 等人 [34] 从总体视角全面总结了评估方法，涵盖不同的评估任务、方法与 benchmark，这些是评估 LLM 表现的关键部分。Guo 等人 [35] 更关注评估目标，描述如何评估 LLM 的知识、对齐与安全控制能力，补充了性能之外的评估指标。

应用。这一类的综述旨在总结利用 LLM 改进不同应用的模型。更具体地说，Zhu 等人 [37] 关注 information retrieval（IR）领域，总结了基于 LLM 的查询过程研究。Xu 等人 [38] 更关注 information extraction（IE），为该领域基于 LLM 的模型提供了全面分类。Li 等人 [50]、Lin 等人 [51] 与 Wang 等人 [52] 讨论 LLM 在推荐系统领域的应用，其中利用 agent 生成数据并提供推荐。Fan 等人 [39]、Wang 等人 [40] 与 Zheng 等人 [41] 关注 LLM 如何在软件设计、开发与测试方面促进 software engineering（SE）。Zeng 等人 [42] 总结了机器人领域的基于 LLM 的方法。Cui 等人 [43] 与 Yang 等人 [44] 关注自动驾驶应用，并从不同视角总结了该领域基于 LLM 的模型。除上述人工智能领域外，LLM 也被用于自然科学与社会科学。He 等人 [45]、Zhou 等人 [46] 与 Wang 等人 [47] 总结了 LLM 在医学中的应用。Li 等人 [48] 关注 LLM 在金融中的应用。He 等人 [49] 回顾了利用 LLM 促进心理学发展的模型。

![](../assets/arxiv-2404.13501-fig2.jpg)  
图 2：LLM 与 LLM-based agent 相关综述的组织结构。

挑战。这一类的综述关注 LLM 中的可信性问题，如幻觉、偏见、不公平、可解释性、安全与隐私。LLM 中的幻觉指 LLM 可能生成错误观念或捏造内容，影响其在下游应用中的可靠性。Zhang 等人 [53]、Huang 等人 [54]、Rawte 等人 [55]、Ye 等人 [56]、Ji 等人 [57]、Tonmoy 等人 [58] 与 Jiang 等人 [59] 总结了缓解 LLM 幻觉问题的主流模型。偏见与不公平问题指 LLM 可能不平等地对待不同人或目标，从而导致社会刻板印象与歧视的传播。Gallegos 等人 [60]、Kotek 等人 [61] 与 Li 等人 [62] 全面讨论了这些挑战，并总结了现有缓解方法。可解释性问题意味着 LLM 的内部工作机制仍不清楚。Zhao 等人 [63] 系统讨论了这一问题，并总结了以往提升 LLM 可解释性的努力。安全与隐私同样是具有挑战性的问题，Yao 等人 [64]、Shayegani 等人 [65]、Neel 与 Chang [66]、Smith 等人 [67]、Dong 等人 [68] 与 Das 等人 [69] 已对此进行了全面综述。

## 2.2 Surveys on Large Language Model-based Agents

基于 LLM 的能力，人们开展了大量构建 LLM-based agent 的研究，这些 agent 能够自主感知环境、采取动作、积累知识并演化自身。在该领域，Wang 等人 [3] 给出了首篇系统总结 LLM-based agent 的综述论文，从 agent construction、agent application 与 agent evaluation 三个视角展开。Xi 等人 [4]、Zhao 等人 [77]、Cheng 等人 [78] 与 Ge 等人 [80] 也从整体视角总结了 LLM-based agent 研究，但关注点与分类体系不同，提供了对该领域更多样的理解。除这些整体综述外，还出现了若干回顾 LLM-based agent 特定方面的论文。对于基础问题，Durante 等人 [79] 总结了多模态 agent 研究。Huang 等人 [74] 关注 LLM-based agent 的规划能力。Guo 等人 [75] 更关注 multi-agent 交互场景。对于应用，Li 等人 [76] 总结了作为个人助理使用的 LLM-based agent。

本文定位。我们的综述总结 LLM-based agent 的一个基础问题，即 agent 的 memory mechanism。据我们所知，这是该方向的首篇综述。我们希望它不仅能启发未来更先进的 memory architecture，也能为新手提供全面的入门材料。

## 3 What is the Memory of LLM-based Agent

与环境交互并从中学习是 LLM-based agent 的基本要求。在 agent-environment interaction 过程中有三个关键阶段，即（1）agent 从环境中感知信息，并将其存入 memory；（2）agent 处理已存储的信息，使其更可用；（3）agent 基于处理后的 memory information 采取下一动作。在所有这些阶段中，memory 都发挥着极其重要的作用。下文首先从狭义与广义两个视角定义 agent 的 memory，然后基于 memory module 详述上述三个阶段的执行过程。

## 3.1 Basic Knowledge

为清晰呈现，我们首先介绍如下若干重要背景知识：

定义 1（Task）。任务是 agent 需要达成的最终目标，例如为 Alice 预订机票、为 Bob 推荐餐厅等。形式上，我们用 T 表示一个任务，并在后文用下标标注不同任务。

定义 2（Environment）。狭义上，环境是 agent 为完成任务而需要与之交互的对象。对于定义 1 中的例子，环境就是 Alice 与 Bob，他们对 agent 的动作给出反馈。更广泛地说，环境可以是任何影响 agent decision-making 的 context 因素，例如预订机票时的天气、推荐餐厅时的时间与地点等。

定义 3（Trial and Step）。为完成任务，agent 需要与环境交互。通常，agent 先采取一个动作，然后环境对该动作作出响应。最后，agent 基于响应采取下一动作。这一过程迭代进行，直到任务完成。完整的一次 agent-environment interaction 过程称为一个 trial，每一次交互轮次称为一个 step。对于每个 trial，agent 可以采取多个 step，形成一个对任务的潜在解。对于每个任务，agent 可以探索多个 trial 来完成任务 [5]。形式上，在第 t 个 step，我们用 a<sub>t</sub> 与 o<sub>t</sub> 分别表示 agent 的 action 与观测到的环境响应。于是，一个长度为 T 的 trial 可表示为 $\xi _ { T } = \{ a _ { 1 } , o _ { 1 } , a _ { 2 } , o _ { 2 } , . . . , o _ { T } , a _ { T } \}$。

任务 A：为 Alice 制定在北京的旅行计划  
![](../assets/arxiv-2404.13501-fig3.jpg)  
图 3：（a）agent-environment interaction 过程中潜在 trial 的示例。（b）memory reading、memory writing 与 memory management 过程的图示，其中虚线表示 cross-trial information 可被纳入 memory module。

在上述定义中，任务与环境是最粗粒度的概念，而 step 是最细粒度的概念。它们共同描述了完整的 agent-environment interaction 过程。

一个简单示例。基于上述定义，我们给出一个简单示例，并在全文使用它来提供更多直观理解。在该示例中，agent 有两个任务：（A）为 Alice 制定从 2024 年 5 月 1 日至 2024 年 5 月 3 日在北京的旅行计划，其中 agent 必须（i）购买往返机票，（ii）根据 Alice 的偏好确定若干景点，（iii）安排这些景点的参观顺序。（B）在 2024 年 5 月 10 日为 Alice 推荐一部电影，其中 agent 必须（i）确定 Alice 有空看电影的时间，（ii）根据 Alice 的观影偏好选择一部电影。对于每个任务，我们在下文给出一个潜在 trial（也在图 3（a）中展示）。对于任务（A），trial 为：

[Step 1] agent：我需要通过在线票务网站预订 2024 年 5 月 1 日从上海到北京、以及 2024 年 5 月 3 日从北京到上海的机票。环境（在线票务网站）：订单已确认。去程航班于上午 9:00 起飞，票号为 EK240501SX9021。返程航班于下午 4:30 起飞，票号为 LG240503FN6317。请准时到达机场乘机。

[Step 2] agent：我已从杂志《北京景点》获取外部知识。杂志显示，长城、故宫与颐和园很有名。根据 Alice 的偏好，我认为她更喜欢古建筑，因此我确定故宫与颐和园为目的地。环境（Alice）：做得好！

[Step 3] agent：现在，我需要为 Alice 安排参观顺序。根据上述信息，我建议她到达北京后先参观颐和园，因为那里适合花一整个下午并观看日落。然后，她可以在第二天去故宫，这样时间会很充裕。最后，她可以在第三天返回上海并休息。环境（Alice）：我很喜欢这个计划。谢谢！

对于任务（B），trial 为：

[Step 1] agent：根据我以往为 Alice 推荐电影的经验，她更喜欢在晚上 9:00 开始看电影，因为那时她已经下班。我应询问 Alice 那个时间是否有空。环境（Alice）：当然，那是个不错的时间！

[Step 2] agent：现在，我需要找一些 Alice 在 Netflix 上标记为“想看”的电影。环境（Netflix）：Alice 的想看列表：Interstellar、Planet Terror 与 Candle in the Tomb。

[Step 3] agent：由于 Alice 从不在晚上看恐怖片，Interstellar 会更适合她。现在，我需要就这部电影与 Alice 确认。环境（Alice）：太好了！我喜欢！

## 3.2 Narrow Definition of the Agent Memory

狭义上，agent 的 memory 只与同一 trial 内的历史信息相关。形式上，对于给定任务，第 t 个 step 之前该 trial 的历史信息为 $\xi _ { t } = \{ a _ { 1 } , o _ { 1 } , a _ { 2 } , o _ { 2 } , . . . , a _ { t - 1 } , o _ { t - 1 } \}$，memory 便基于 $\xi _ { t }$ 导出。在上述简单示例中，对于任务（A），agent 在 [Step 3] 需要为 Alice 安排参观顺序；此时其 memory 包含 [Step 1] 与 [Step 2] 中关于所选景点与到达时间的信息。对于任务（B），agent 必须在 [Step 3] 为 Alice 选择一部电影；此时其 memory 包含已安排的观影时间。

## 3.3 Broad Definition of the Agent Memory

广义上，agent 的 memory 可以来自更广泛的来源，例如跨不同 trial 的信息，以及 agent-environment interaction 之外的外部知识。形式上，给定一系列顺序任务 $\{ \mathcal { T } _ { 1 } , \mathcal { T } _ { 2 } , . . . , \mathcal { T } _ { K } \}$，对于任务 $\mathcal { T } _ { k }$，第 t 个 step 的 memory information 来自三个来源：（1）同一 trial 内的历史信息，即 $\xi _ { t } ^ { k } = \{ a _ { 1 } ^ { k } , o _ { 1 } ^ { k } , . . . , a _ { t - 1 } ^ { k } , o _ { t - 1 } ^ { k } \}$，其中我们加上标 k 来标注任务索引。（2）跨不同 trial 的历史信息，即 $\Xi ^ { k } = \{ \xi ^ { 1 } , \xi ^ { 2 } , . . . , \xi ^ { k - 1 } , \xi ^ { k ^ { \prime } } \}$，其中 $\xi ^ { j } \left( j \in \left\{ 1 , . . . , k - 1 \right\} \right)$ 表示任务 j 的 trial，$\xi ^ { k ^ { \prime } }$ 表示任务 $\mathcal { T } _ { k }$ 先前探索过的 trial。（3）外部知识，由 $D _ { t } ^ { k }$ 表示。agent 的 memory 基于 $( \xi _ { t } ^ { k } , \Xi ^ { k } , D _ { t } ^ { k } )$ 导出。在上述简单示例中，对于任务（A），若存在若干 failed trial，即 Alice 的反馈为负面，则这些 trial 可被纳入 agent 的 memory，以避免将来出现类似错误（对应 $\xi ^ { k ^ { \prime } }$）。此外，对于任务（B），agent 可以推荐与 Alice 在任务（A）中参观过的景点相关的电影，以捕捉其近期偏好（对应 $\{ \xi ^ { 1 } , \xi ^ { 2 } , . . . , \xi ^ { k - 1 } \}$）。在 agent decision-making 过程中，它还参考了杂志《北京景点》来制定旅行计划，这就是当前任务 $\mathcal { T } _ { k }$ 的外部知识（对应 $D _ { t } ^ { k }$）。

## 3.4 Memory-assisted Agent-Environment Interaction

如第 3 节开头所述，agent-environment interaction 过程有三个关键阶段。agent 的 memory module 通过三种操作实现这些阶段，包括 memory writing、memory management 与 memory reading。

memory writing。该操作旨在将原始观测投影为实际存储的 memory content，这些内容更具信息量 [7] 且更简洁 [6]。它对应 agent-environment interaction 过程的第一个阶段。给定任务 $\mathcal { T } _ { k }$，若 agent 在第 t 个 step 采取动作 $a _ { t } ^ { k }$，且环境给出观测 $o _ { t } ^ { k }$，则 memory writing 操作可形式化表示为：

$$
m _ {t} ^ {k} = W (\{a _ {t} ^ {k}, o _ {t} ^ {k} \}),
$$

其中 W 是投影函数。$m _ { t } ^ { k }$ 是最终存储的 memory content，可以是自然语言或 parametric 表示。在上述简单示例中，对于任务（A），agent 应在 [Step 2] 之后记住航班安排与景点决策。对于任务（B），agent 应在 [Step 1] 之后记住 Alice 希望在晚上 9:00 看电影这一事实。

memory management。该操作旨在处理已存储的 memory information，使其更有效，例如总结高层概念以使 agent 更具泛化性 [6]，对相似信息做 consolidation 以减少冗余 [7]，以及 forgetting 不重要或不相关的信息以消除其负面影响。该操作对应 agent-environment interaction 过程的第二个阶段。设 $M _ { t - 1 } ^ { k }$ 为任务 k 在第 t 个 step 之前的 memory content，并假设 $m _ { t } ^ { k }$ 是第 t 个 step 基于上述 memory writing 操作存储的信息，则 memory management 操作可表示为：

$$
M _ {t} ^ {k} = P (M _ {t - 1} ^ {k}, m _ {t} ^ {k}),
$$

其中 P 是迭代处理已存储 memory information 的函数。对于狭义的 memory 定义，迭代只发生在同一 trial 内，trial 结束时 memory 被清空。对于广义的 memory 定义，迭代发生在不同 trial 甚至不同任务之间，并且包括外部知识的整合。对于上述简单示例中的任务（B），agent 可以得出 Alice 喜欢在晚上看科幻电影，这可以作为默认规则用于将来为 Alice 提供推荐。

memory reading。该操作旨在从 memory 中获取重要信息，以支持 agent 的下一动作。它对应 agent-environment interaction 过程的第三个阶段。假设 $\hat { M } _ { t } ^ { k }$ 是任务 k 在第 t 个 step 的 memory content，$c _ { t + 1 } ^ { k }$ 是下一动作的 context，则 memory reading 操作可表示为：

$$
\hat {M} _ {t} ^ {k} = R (M _ {t} ^ {k}, c _ {t + 1} ^ {k}),
$$

其中 R 通常通过计算 $M _ { t } ^ { k }$ 与 $c _ { t + 1 } ^ { k }$ 之间的相似度实现 [82]。$\hat { M } _ { t } ^ { k }$ 作为最终 prompt 的一部分，用于驱动 agent 的下一动作。对于上述简单示例中的任务（B），当 agent 在 [Step 3] 决定最终推荐电影时，它应关注 [Step 2] 中的“想看”列表，并从中选择一部。

基于上述操作，我们可以导出从 $\{ a _ { t } ^ { k } , o _ { t } ^ { k } \}$ 到 $a _ { t + 1 } ^ { k }$ 的演化过程的统一函数，即：

$$
a _ {t + 1} ^ {k} = \operatorname{LLM} \left\{R \left(P \left(M _ {t - 1} ^ {k}, W \left(\left\{a _ {t} ^ {k}, o _ {t} ^ {k} \right\}\right)\right), c _ {t + 1} ^ {k}\right) \right\},
$$

其中 LLM 指 large language model。通过迭代展开该函数，可以容易地得到完整的 agent-environment interaction 过程（直观图示见图 3（b））。注。该函数给出了 agent memory 过程的一般形式化描述。已有工作可能采用不同具体设定。例如，在 [5] 中，R 与 P 被设为相同函数，且 P 仅在 trial 结束时生效。在 Park 等人 [83] 中，R 基于相似度、时间间隔与重要性三个准则实现，$P$ 通过 reflection 过程实现，以获得更抽象的想法。本节关注 agent memory 操作的整体框架。W、P 与 R 更具体的实现推迟到第 5 节讨论。

## 4 Why We Need the Memory in LLM-based Agent

上文介绍了 LLM-based agent 的 memory 是什么。在全面介绍如何实现之前，本节简要说明为什么构建 LLM-based agent 需要 memory，并从认知心理学、self-evolution 与 agent application 三个视角展开讨论。

## 4.1 Perspective of Cognitive Psychology

认知心理学是对人类心理过程的科学研究，这些过程包括注意、语言使用、memory、感知、问题解决、创造性与推理<sup>2</sup>。在这些过程中，memory 被广泛认为是一个极其重要的过程 [84]。它对于人类通过学习积累重要信息并抽象高层概念来获取知识 [85]、通过记住文化价值与个体经验来形成社会规范 [86]、通过想象潜在的正负后果来采取合理行为 [87] 等方面具有基础性作用。

LLM-based agent 的一个主要目标是替代人类完成不同任务。为使 agent 表现得像人类，遵循人类的工作机制来设计 agent 是一种自然且必要的选择 [88]。既然 memory 对人类很重要，设计 memory module 对 agent 也同样重要。此外，认知心理学已被研究很长时间，积累了许多有效的 human memory 理论与架构，可支持 agent 更高级的能力 [89]。

![](../assets/arxiv-2404.13501-fig4.jpg)  
图 4：LLM-based agent 中 memory 的来源、形式与操作概览。

## 4.2 Perspective of Self-Evolution

为完成不同的实际任务，agent 必须在动态环境中 self-evolve [90]。在 agent-environment interaction 过程中，memory 对以下方面至关重要：（1）经验积累。memory 的一个重要功能是记住过去的错误规划、不当行为或失败经验，从而使 agent 在未来处理类似任务时更有效 [91]。这对于提升 agent 在 self-evolution 过程中的学习效率极其重要。（2）环境探索。为在环境中自主演化，agent 必须探索不同动作并从反馈中学习 [92]。通过记住历史信息，memory 可以帮助更好地决定何时以及如何进行探索，例如更多地关注先前失败的 trial 或探索频率较低的动作 [93]。（3）知识抽象。memory 的另一个重要功能是从原始观测中总结与抽象高层信息，这是 agent 对未见环境更具适应性与泛化性的基础 [82]。总之，self-evolution 是 LLM-based agent 的基本特征，而 memory 对 self-evolution 至关重要。

## 4.3 Perspective of Agent Applications

在许多应用中，memory 是 agent 不可或缺的组件。例如，在 conversational agent 中，memory 存储历史对话信息，这是 agent 生成下一回复所必需的。没有 memory，agent 就不知道 context，无法继续对话 [94]。在 simulation agent 中，memory 对于使 agent 始终遵循角色设定极其重要。没有 memory，agent 在模拟过程中很容易脱离角色 [95]。上述两个例子都表明，memory 不是可选组件，而是 agent 完成给定任务所必需的。

在上述三个视角中，第一个视角揭示了 memory 为 agent 建立认知基础。第二个与第三个视角表明 memory 对 agent 的演化原则与应用是必要的，这为设计具有 memory mechanism 的 agent 提供了洞见。

## 5 How to Implement the Memory of LLM-based Agent

本节从三个视角讨论 memory module 的实现：memory source、memory form 与 memory operation。memory source 指 memory content 来自何处。memory form 关注如何表示 memory content。memory operation 旨在处理 memory content。这三个视角给出 memory implementation 方法的全面回顾，有助于未来研究。为更好展示，我们在图 4 中给出实现方法概览。

## 5.1 Memory Sources

在已有工作中，memory content 可能来自不同来源。基于第 3 节的表述，这些来源可分为三类，即一个 trial 内的信息、跨不同 trial 的信息与外部知识。前两者是在 agent-environment interaction 过程中动态生成的（例如任务内部信息），后者则是循环之外的静态信息（例如任务外部信息）。我们在表 1 中总结了关于 memory source 的已有工作。

表 1：Memory Sources 汇总。我们用 ✓ 与 × 标注模型中是否采用相应来源。

<table><tr><td>Model</td><td>Inside-trial Information</td><td>Cross-trial Information</td><td>External Knowledge</td></tr><tr><td>MemoryBank [6]</td><td>✓</td><td>×</td><td>×</td></tr><tr><td>RET-LLM [7]</td><td>✓</td><td>×</td><td>✓</td></tr><tr><td>ChatDB [96]</td><td>✓</td><td>×</td><td>✓</td></tr><tr><td>TiM [97]</td><td>✓</td><td>×</td><td>×</td></tr><tr><td>SCM [98]</td><td>✓</td><td>×</td><td>×</td></tr><tr><td>Voyager [99]</td><td>✓</td><td>×</td><td>×</td></tr><tr><td>MemGPT [100]</td><td>✓</td><td>×</td><td>×</td></tr><tr><td>MemoChat [94]</td><td>✓</td><td>×</td><td>×</td></tr><tr><td>MPC [101]</td><td>✓</td><td>×</td><td>×</td></tr><tr><td>Generative Agents [83]</td><td>✓</td><td>×</td><td>×</td></tr><tr><td>RecMind [102]</td><td>✓</td><td>×</td><td>✓</td></tr><tr><td>Retroformer [103]</td><td>✓</td><td>✓</td><td>✓</td></tr><tr><td>ExpeL [82]</td><td>✓</td><td>✓</td><td>✓</td></tr><tr><td>Synapse [91]</td><td>✓</td><td>✓</td><td>×</td></tr><tr><td>GITM [93]</td><td>✓</td><td>✓</td><td>✓</td></tr><tr><td>ReAct [104]</td><td>✓</td><td>×</td><td>✓</td></tr><tr><td>Reflexion [5]</td><td>✓</td><td>✓</td><td>✓</td></tr><tr><td>RecAgent [95]</td><td>✓</td><td>×</td><td>×</td></tr><tr><td>Character-LLM [105]</td><td>✓</td><td>×</td><td>✓</td></tr><tr><td>MAC [106]</td><td>✓</td><td>×</td><td>×</td></tr><tr><td>Huatuo [107]</td><td>✓</td><td>×</td><td>✓</td></tr><tr><td>ChatDev [1]</td><td>✓</td><td>×</td><td>×</td></tr><tr><td>InteRecAgent [108]</td><td>✓</td><td>×</td><td>✓</td></tr><tr><td>MetaAgents [109]</td><td>✓</td><td>×</td><td>×</td></tr><tr><td>TPTU [110, 111]</td><td>✓</td><td>×</td><td>✓</td></tr><tr><td>MetaGPT [112]</td><td>✓</td><td>✓</td><td>×</td></tr><tr><td> $S^3$ [2]</td><td>✓</td><td>×</td><td>×</td></tr><tr><td>InvestLM [113]</td><td>✓</td><td>×</td><td>✓</td></tr></table>

## 5.1.1 Inside-trial Information

在 agent-environment interaction 过程中，一个 trial 内的历史步骤通常是支持 agent 未来动作最相关、最具信息量的信号。几乎所有已有工作都使用这一信息作为 memory source 的一部分。

代表性研究。Generative Agents [83] 旨在使用 LLM-based agent 模拟人类的日常行为。agent 的 memory 由为实现目标而产生的历史行为导出，例如研究特定主题时收集的相关论文。MemoChat [94] 旨在与人类聊天，其中 agent 的 memory 基于一次对话 session 的对话历史导出。TiM [97] 旨在通过在完成任务后自生成多个想法来增强 agent 的推理能力，这些想法被用作 memory 以提供更具泛化性的信息。Voyager [99] 关注基于 Minecraft 构建游戏 agent，其中 memory 包含用于完成任务的预备动作与基本动作的可执行代码。需要注意的是，inside-trial information 不仅包含 agent-environment interaction，还包含交互 context，例如时间与地点信息。

讨论。inside-trial information 是最明显、最直观的 memory construction 来源，因为它与 agent 当前必须完成的任务高度相关。然而，仅依赖 inside-trial information 可能使 agent 无法从各种任务中积累有价值的知识并学习更具泛化性的信息。因此，许多研究还探索如何有效利用跨不同任务的信息来构建 memory module，详见后续章节。

## 5.1.2 Cross-trial Information

对于 LLM-based agent，在环境中跨多个 trial 积累的信息也是 memory 的关键部分，通常包括成功与失败的动作及其洞见，例如失败原因、成功的常见动作模式等。

代表性研究。最突出的研究之一是 Reflexion [5]，它提出了面向 LLM-based agent 的 verbal reinforcement learning。它以言语形式从过去 trial 中导出经验，并将其应用于后续 trial，以提升同一任务的表现。此外，Retroformer [103] 对 reflection 模型进行 fine-tuning，使 agent 能够更有效地从过去 trial 中提取 cross-trial information。在 Synapse [91] 中，agent 专注于求解计算机控制任务。其 memory 可通过成功范例记录 cross-trial information，这些范例可用作类似 trial 的参考。在 ExpeL [82] 中，agent 需要在环境中求解一组复杂交互任务。它们存储并组织已完成的轨迹，并为新任务 recall 相似轨迹。在 recalled 的轨迹中，成功案例将与失败案例进行比较，以识别成功的模式。

讨论。根据积累的 cross-trial information memory，agent 能够积累经验，这对它们的演化很重要。基于过去经验，agent 可以根据整个过程的总体反馈调整动作。inside-trial 观测充当 short-term memory，而 trial experience 可被视为 long-term memory。它利用来自不同 trial 的反馈来支持范围更广的 agent trial，为 agent 提供更持久的经验支持。然而，其局限在于 inside-trial information 与 cross-trial information 都要求 agent 亲自参与 agent-environment interaction，不包含外部经验与知识。

## 5.1.3 External Knowledge

LLM-based agent 的一个重要特征是可以用自然语言直接与之交流和控制。因此，LLM-based agent 可以容易地纳入文本形式的外部知识（例如维基百科<sup>3</sup>），以辅助其决策。

代表性研究。在 ReAct [104] 中，agent 需要通过多个推理步骤回答常识问题。若在这些步骤中缺乏信息，它们可以利用维基百科 API 获取外部知识。GITM [93] 旨在设计 Minecraft 中的 agent，使其能在复杂且稀疏奖励的环境中探索。agent 从在线 Minecraft Wiki 与合成配方中获取知识，为其导航提供无限的知识来源。CodeAgent [114] 关注仓库级代码生成任务，这通常需要复杂依赖与大量文档。它设计了网络搜索策略来获取相关外部知识。ChatDoctor [115] 将 LLM-based agent 适配到医学领域。它对一个获取过程进行 fine-tuning，从维基百科与医学数据库 retrieve 外部知识。

讨论。外部知识可从私有与公开来源获得。它为 LLM-based agent 提供了远超其内部环境的知识，而这些知识可能是 agent 通过 agent-environment interaction 难以或甚至无法获得的。此外，大多数外部知识可根据任务需求，通过实时动态访问各种工具的 API 获得，从而缓解知识过时的问题。将外部知识整合进 LLM-based agent 的 memory，显著扩展了其知识边界，为决策提供无限、最新且有充分依据的知识。

## 5.2 Memory Forms

一般而言，表示 memory content 有两种形式：文本形式与 parametric 形式。在文本形式中，信息以自然语言显式保留与 recall。在 parametric 形式中，memory information 被编码进参数，并隐式影响 agent 的动作。我们在表 2 中总结了关于 memory form 及其实现的已有工作。

表 2：Memory Forms 汇总。我们用 ✓ 与 × 标注模型中是否采用相应 memory form。

<table><tr><td rowspan="2">Model</td><td colspan="4">Textual Form</td><td colspan="2">Parametric Form</td></tr><tr><td>Full</td><td>Recent</td><td>Retrieval</td><td>External</td><td>Fine-tuning</td><td>Editing</td></tr><tr><td>MemoryBank [6]</td><td>×</td><td>×</td><td>√</td><td>×</td><td>×</td><td>×</td></tr><tr><td>RET-LLM [7]</td><td>×</td><td>×</td><td>√</td><td>×</td><td>×</td><td>×</td></tr><tr><td>ChatDB [96]</td><td>×</td><td>×</td><td>√</td><td>×</td><td>×</td><td>×</td></tr><tr><td>TiM [97]</td><td>×</td><td>×</td><td>√</td><td>×</td><td>×</td><td>×</td></tr><tr><td>SCM [98]</td><td>×</td><td>√</td><td>√</td><td>×</td><td>×</td><td>×</td></tr><tr><td>Voyager [99]</td><td>×</td><td>×</td><td>√</td><td>×</td><td>×</td><td>×</td></tr><tr><td>MemGPT [100]</td><td>×</td><td>√</td><td>√</td><td>×</td><td>×</td><td>×</td></tr><tr><td>MemoChat [94]</td><td>×</td><td>×</td><td>√</td><td>×</td><td>×</td><td>×</td></tr><tr><td>MPC [101]</td><td>×</td><td>×</td><td>√</td><td>×</td><td>×</td><td>×</td></tr><tr><td>Generative Agents [83]</td><td>×</td><td>×</td><td>√</td><td>×</td><td>×</td><td>×</td></tr><tr><td>RecMind [102]</td><td>√</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td></tr><tr><td>Retroformer [103]</td><td>√</td><td>×</td><td>×</td><td>√</td><td>√</td><td>×</td></tr><tr><td>ExpeL [82]</td><td>√</td><td>×</td><td>√</td><td>√</td><td>×</td><td>×</td></tr><tr><td>Synapse [91]</td><td>×</td><td>×</td><td>√</td><td>×</td><td>×</td><td>×</td></tr><tr><td>GITM [93]</td><td>√</td><td>×</td><td>√</td><td>√</td><td>×</td><td>×</td></tr><tr><td>ReAct [104]</td><td>√</td><td>×</td><td>×</td><td>√</td><td>×</td><td>×</td></tr><tr><td>Reflexion [5]</td><td>√</td><td>×</td><td>×</td><td>√</td><td>×</td><td>×</td></tr><tr><td>RecAgent [95]</td><td>×</td><td>√</td><td>√</td><td>×</td><td>×</td><td>×</td></tr><tr><td>Character-LLM [105]</td><td>×</td><td>√</td><td>×</td><td>×</td><td>√</td><td>×</td></tr><tr><td>MAC [106]</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td><td>√</td></tr><tr><td>Huatuo [107]</td><td>√</td><td>×</td><td>×</td><td>×</td><td>√</td><td>×</td></tr><tr><td>ChatDev [1]</td><td>√</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td></tr><tr><td>InteRecAgent [108]</td><td>×</td><td>√</td><td>√</td><td>√</td><td>×</td><td>×</td></tr><tr><td>MetaAgents [109]</td><td>×</td><td>×</td><td>√</td><td>×</td><td>×</td><td>×</td></tr><tr><td>TPTU [110, 111]</td><td>√</td><td>×</td><td>×</td><td>√</td><td>×</td><td>×</td></tr><tr><td>MetaGPT [112]</td><td>√</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td></tr><tr><td> $S^3$ [2]</td><td>×</td><td>×</td><td>√</td><td>×</td><td>×</td><td>×</td></tr><tr><td>InvestLM [113]</td><td>√</td><td>×</td><td>×</td><td>×</td><td>√</td><td>×</td></tr></table>

## 5.2.1 Memory in Textual Form

文本形式目前是表示 memory content 的主流方法，其特点是可解释性更好、实现更容易、读写效率更高。具体而言，文本形式既可以是原始自然语言这类非结构化表示，也可以是元组、数据库等结构化信息。一般而言，已有研究使用 textual memory 存储四类信息，包括（1）完整的 agent-environment interaction，（2）近期的 agent-environment interaction，（3）retrieved agent-environment interaction，以及（4）外部知识。前三种方法利用自然语言描述 agent-environment interaction 循环内的信息。前三种类型记录该循环内的信息，而最后一种类型利用自然语言存储该循环之外的信息。

完整交互。该方法基于 long-context 策略 [116] 存储 agent-environment interaction 历史的全部信息。对于第 3.1 节的例子，任务（A）中 agent 在第 2 个 step 之后的 memory 可以通过拼接第 2 个 step 之前的所有信息来实现，最终的 textual memory 为：“你的 memory 是 [Step 1]（agent）……（在线票务网站）……[Step 2]……请基于你的 memory 进行推断”。

在已有工作中，不同模型使用不同策略存储 memory information。例如，在 LongChat [116] 中，agent 关注 long-context 场景下的自然语言理解。它对基础模型进行 fine-tuning，以更好地适应完整的 interaction memory。Memory Sandbox [117] 旨在缓解对话中无关 memory 的影响。它设计了一种透明、可交互的方法来管理 agent memory，在将 memory 拼接为 prompt 之前移除无关 memory。此外，还有一些工作致力于增强 LLM 处理更 long-context 的能力 [118, 119]。

存储全部 agent-environment interaction 可以保留完整信息，但在计算成本、推理时间与推理鲁棒性方面存在明显局限。首先，实践中快速增长的 long-context memory 会导致 LLM 推理期间的高计算成本，因为 attention 计算的时间复杂度随序列长度呈二次增长。因此，它需要更多计算资源并显著增加推理延迟，阻碍实际部署。其次，随着 memory 快速增长，memory length 很容易超过 LLM 预训练时的序列长度上界，因而必须对 memory 进行截断。这会导致 agent memory 不完整，从而造成信息损失。最后，它可能导致 LLM 推理中的偏差与不鲁棒性。具体而言，已有研究 [120] 表明，long-context 中文本片段的位置会极大影响其被利用的程度，因此 long-context prompt 中的 memory 不能被平等、稳定地对待。所有这些缺点表明，需要为 LLM-based agent 设计额外的 memory module，而不是简单地把所有信息拼接进 prompt。

近期交互。该方法使用自然语言存储并维护最近获得的 memory，从而依据局部性原理（Principle of Locality）[121] 提升 memory information 利用效率。在第 3.1 节例子的任务（B）中，我们可以只记住 Alice 近三年的偏好，截断更久远的部分，其中近三年可视为 memory window 大小。

在已有研究中，存储近期 textual memory 有多种策略。例如，SCM [98] 提出一种基于 cache 机制的闪存（flash memory），保留最近 t − 1 个 time step 的观测，旨在增强信息的时效性。MemGPT [100] 将 agent 视为操作系统，可通过自然接口与用户动态交互。它设计 working context 来保存近期历史，作为虚拟 context 管理的一部分。在 RecAgent [95] 中，agent 被设计为模拟电影推荐中的用户行为。它将一些时间信息存储在 short-term memory 中作为中间 cache，这可以模拟人类大脑的 memory mechanism [122, 123]。这些代表性方法可以基于近期交互动态更新 memory，并更多关注对当前阶段重要的近期 context。

按近期性对 memory 做 cache 是提升 memory efficiency 的有效方式，它使 agent 能够更多关注近期信息。然而，在长期任务中，该方法无法访问久远 memory 中的关键信息。它可能导致不在当前 cache 窗口内、但潜在关键的信息丢失。换言之，强调近期性会天然地忽略较早但关键的信息，从而在需要全面理解过去事件的场景中带来挑战。

retrieved interaction。与上述按时间截断 memory 的方法不同，该方法通常基于相关性、重要性与主题选择 memory content。它确保久远但关键的 memory 被纳入决策过程，从而解决只记住近期信息的局限。在第 3.1 节例子的任务（A）中，Alice 的偏好已在此任务之前存入 memory。在 [Step 2]，agent 将根据查询关键词“旅行”从 memory 中 retrieve Alice 偏好中最相关的方面，得到 Alice 对古建筑类景点的偏好。一般而言，retrieval 方法会在 memory writing 期间为 memory entry 生成 embedding 作为索引，同时记录辅助信息以协助 retrieval。在 memory reading 期间，为每个 memory entry 计算匹配分数，前 K 个条目将用于 agent 的决策过程。

在现有研究中，大多数 agent 利用 retrieval 方法处理 memory information。例如，Park 等人 [83] 首先通过余弦相似度计算当前 context 与 memory entry 的相关性，并根据辅助信息获得重要性与近期性。MemoryBank [6] 采用双塔 dense retrieval 模型从过去对话中寻找相关信息。每个 memory entry 被编码为 embedding，随后由 FAISS [124] 建立索引，以提升 retrieval 效率。读取 memory 时，当前 context 将被编码为表示，以获得最相关的 memory。此外，RET-LLM [7] 旨在设计一个通用写读 memory module。它利用局部敏感哈希（LSH）从数据库中 retrieve 具有相关条目的元组，以提供更多信息。另外，ChatDB [96] 设计利用符号 memory，并提出生成 SQL 语句从数据库 retrieve 已存储信息。

retrieval 方法在很大程度上依赖获取预期信息的准确性与效率。不准确的 retrieval 策略可能获取无关信息，对 agent 推理毫无帮助。而沉重的 retrieval 系统会导致大量计算成本与长时间延迟，尤其是在处理海量信息时。此外，retrieval 方法通常存储环境内的同质信息，即所有信息形式一致。对于环境外的异质信息，很难直接应用相同方法进行 memory storage。

外部知识。为获取更多信息，一些 agent 通过调用工具获取外部知识，目的是把额外的相关知识转化为自身 memory 以用于决策。例如，通过应用程序编程接口（API）访问外部知识是一种常见做法 [104, 5]。如今，大量公开信息（如维基百科与 OpenWeatherMap<sup>4</sup>）可在网上获取（免费或付费），并可通过 API 调用方便地访问。例如，在第 3.1 节例子的任务（A）的 [Step 2] 中，来自数字杂志的外部知识就是通过工具方法获得的。

在现有模型中，Toolformer [125] 提出教 LLM 使用工具，从而获取外部知识以更好地求解任务。此外，ToolLLM [126] 赋予 Llama [127] 利用 RapidAPI<sup>5</sup> 中更多 API 的能力，并支持多工具使用，为扩展 agent 能力提供了通用接口。在 TPTU [110] 中，agent 被纳入任务规划与工具使用，以处理复杂问题。后续工作 [111] 进一步在 retrieval 等方面广泛提升其能力。在 ToRA [128] 中，agent 需要求解数学问题。它们利用模仿学习提升使用基于程序的工具的能力。

上述方法允许 agent 从多样来源访问外部最新真实世界信息，从而显著提升 agent 能力。然而，由于潜在的不准确与偏差，这些信息的可靠性可能存疑 [18]。此外，将工具集成到 agent 中需要全面理解，以在各种 context 中解释 retrieved 信息，这可能带来更高计算成本，并使外部数据与内部决策过程对齐变得复杂。另外，使用外部 API 会引发隐私、数据安全与使用政策合规方面的担忧，需要严格管理与监督 [18]。

## 5.2.2 Memory in Parametric Form

另一类方法是把 memory 表示为 parametric 形式。它们不占用 prompt 中额外的 context 长度，因此不受 LLM context 长度限制的约束。然而，parametric memory 形式仍研究不足，我们将已有工作分为两类：fine-tuning 方法与 memory editing 方法。

fine-tuning 方法。将外部知识整合进 agent memory，有利于在其通用知识之上丰富领域特定知识。为把领域知识注入 LLM，supervised fine-tuning 是一种常见方法，它赋予 agent 领域专家的 memory，显著提升 agent 完成领域特定任务的能力。在第 3.1 节例子的任务（A）中，来自杂志的景点外部知识可以在该任务之前通过 fine-tuning 注入 LLM 参数。

在已有工作中，Character-LLM [105] 关注角色扮演情境。它利用角色相关数据（例如经历）进行 supervised fine-tuning，赋予 agent 角色的特定特质与特征。Huatuo [107] 旨在赋予 agent 生物医学领域的专业能力。它尝试在中文医学知识库上对 Llama 进行 fine-tuning [127]。此外，为创建人工医生，DoctorGLM [129] 使用 LoRA [131] 对 ChatGLM 进行 fine-tuning [130]，Radiology-GPT [132] 通过在标注的放射学数据集上进行 supervised fine-tuning，提升放射学分析领域的知识。此外，InvestLM [113] 收集投资数据并进行 fine-tuning，以提升金融投资领域的特定能力。

fine-tuning 方法可以有效弥合通用 agent 与专用 agent 之间的差距。它提升 agent 在需要对领域特定信息保持高准确性与可靠性的任务上的能力。然而，为特定领域对 LLM 进行 fine-tuning 可能导致过拟合，还引发 catastrophic forgetting 的担忧，即 LLM 可能因更新参数而忘记原有知识。fine-tuning 的另一个局限在于计算成本与时间消耗，以及大量数据需求。因此，大多数 fine-tuning 方法应用于离线场景，很少能处理在线场景，例如利用 agent 观测与 trial experience 进行 fine-tuning。由于 agent-environment interaction 频繁，对在线动态交互的每个 step 进行反向传播 fine-tuning 在成本上无法承受。

memory editing 方法。除 fine-tuning 方法外，另一类将 memory 注入模型参数的方法是知识编辑 [133, 134]。与从特定数据集抽取模式的 fine-tuning 方法不同，知识编辑方法专门定位并只调整需要改变的事实。它确保无关知识不受影响。知识编辑方法更适合小规模 memory 调整。一般而言，它们计算成本更低，因而更适合在线场景。在任务（B）的例子中，agent memory 显示 Alice 总在晚上 9:00 看电影，但她可能最近换了工作，晚上 9:00 没空。若是如此，相关 memory（例如晚上 9:00 的作息）应被编辑，这可通过知识编辑方法实现。

在已有研究中，MAC [106] 旨在为在线场景设计有效且高效的 memory adaptation 框架。它利用元学习替代优化步骤。PersonalityEdit [135] 关注编辑 LLM 与 agent 的人格，基于大五人格等理论改变其特质。MEND [134] 利用元学习思想训练一个轻量模型，该模型能够为预训练语言模型的参数生成修改。APP [136] 研究添加新事实是否会导致对现有事实的 catastrophic forgetting，重点关注邻居扰动对 memory 添加的影响。此外，KnowledgeEditor [133] 训练一个超网络，在基于“学习如何更新”的问题表述注入 memory 时，预测模型参数的修改。Wang 等人 [137] 提出一个新的优化目标来改变 LLM 的有害知识，同时保持通用性能。对于 LLM-based agent，agent 可以通过知识编辑改变不良 memory，这可视为一种 forgetting mechanism。

知识编辑方法提供了一种创新方式来更新 LLM 参数中存储的信息。通过专门定位与调整事实，这些方法可以确保更新期间非目标知识不受影响，从而缓解 catastrophic forgetting 问题。此外，定向调整机制允许更高效、资源消耗更少的更新，使知识编辑成为高精度、实时修改的有吸引力选择。然而，尽管这些进展有前景，元训练的计算成本与无关 memory 的保留仍是显著挑战。

## 5.2.3 Advantages and Disadvantages of Textual and Parametric Memory

textual memory 与 parametric memory 各有优势与弱点，因而适用于不同 memory content 与应用场景。本节从多个方面讨论这两种 memory form 的优缺点。

有效性。textual memory 存储 agent-environment interaction 的原始信息，更全面、更详细。然而，它受 LLM 的 prompt token 数量上限的约束，使 agent 难以存储大量信息。相比之下，parametric memory 不受 prompt 长度限制，但在把文本转化为参数时可能遭受信息损失，且复杂的 memory 训练会带来额外挑战。

效率。对于 textual memory，每次 LLM 推理都需要把 memory 整合进 context prompt，导致更高成本与更长处理时间。相比之下，对于 parametric memory，信息可被整合进 LLM 参数，消除这些 context 的额外成本。然而，parametric memory 在写入过程中需要额外成本，而 textual memory 更易写入，尤其是小量数据。简言之，textual memory 在写入上更高效，而 parametric memory 在读取上更高效。

可解释性。textual memory 通常比 parametric memory 更可解释，因为自然语言是人类理解的最自然、最直接的策略，而 parametric memory 通常表示在 latent space 中。然而，这种可解释性是以信息密度为代价换来的。这是因为 textual memory 中的词序列表示在离散空间中，不如 parametric memory 的连续空间稠密。

总之，这两类 memory 之间的权衡使它们适用于不同应用。例如，对于需要回忆近期交互的任务，如对话与 context-specific 任务，textual memory 似乎更有效。对于需要大量 memory 或成熟知识的任务，parametric memory 可能是更好的选择。

## 5.3 Memory Operations

我们将 memory 的整体流程分为三种操作：memory writing、memory management 与 memory reading。这三种操作通常协同实现 memory 的功能，为 LLM 推理提供信息。我们在表 3 中总结了关于 memory operation 的已有工作。

## 5.3.1 Memory Writing

agent 感知信息后，其中一部分将通过 memory writing 操作被 agent 存储以供后续使用，识别哪些信息是必须存储的至关重要。许多研究选择存储原始信息，另一些研究则把原始信息的摘要也放入 memory module。

代表性研究。在 TiM [97] 中，原始信息将被抽取为两个实体之间的关系，并存入结构化数据库。写入数据库时，相似内容将被存储在同一组中。在 SCM [98] 中，它设计了一个 memory controller 来决定何时执行操作。该控制器充当整个 memory module 的向导。在 MemGPT [100] 中，memory writing 完全由 agent 自主主导。agent 可以基于 context 自主更新 memory。在 MemoChat [94] 中，agent 通过抽象主要讨论的主题来总结每个对话片段，并将其存储为索引 memory segment 的键。

讨论。已有研究指出，在 memory writing 操作中设计信息抽取策略至关重要 [94]。这是因为原始信息通常冗长且含噪。此外，不同环境可能提供不同形式的反馈，如何抽取信息并将其表示为 memory，对 memory writing 也同样重要。

## 5.3.2 Memory Management

对人类而言，memory information 在大脑中不断被处理与抽象。agent 中的 memory 也可以通过 reflection 生成更高层 memory、对冗余 memory entry 做 consolidation，以及通过 forgetting 不重要、早期的 memory 来管理。

代表性研究。在 MemoryBank [6] 中，agent 把对话处理并提炼为对日常事件的高层总结，类似于人类回忆经历的关键方面。通过长期交互，它们不断评估与精炼知识，生成对人格特质的日常洞见。在 Voyager [99] 中，agent 能够基于环境反馈精炼 memory。在 Generative Agents [83] 中，agent 可以通过 reflection 获得更高层信息，即从 agent 生成抽象想法。当积累的事件足以处理时，reflection 过程将被激活。对于 GITM [93]，为建立适用于各种情境的通用参考计划，多个计划中的关键动作会在 memory module 中被进一步总结。

讨论。大多数 memory management 操作受人类大脑工作机制启发。借助 LLM 模拟人类心智的强大能力，这些操作可以帮助 agent 更好地生成高层信息并与环境交互。

表 3：Memory Operations 汇总。若模型未对 memory operation 作特殊设计，我们用 ◦ 标注；否则用 ✓ 标注。× 表示论文未讨论该 memory operation。

<table><tr><td rowspan="2">Model</td><td rowspan="2">Writing</td><td colspan="3">Management</td><td rowspan="2">Reading</td></tr><tr><td>Consolidation</td><td>Reflection</td><td>Forgetting</td></tr><tr><td>MemoryBank [6]</td><td>✓</td><td>✓</td><td>✓</td><td>✓</td><td>✓</td></tr><tr><td>RET-LLM [7]</td><td>✓</td><td>×</td><td>×</td><td>×</td><td>✓</td></tr><tr><td>ChatDB [96]</td><td>✓</td><td>×</td><td>✓</td><td>×</td><td>✓</td></tr><tr><td>TiM [97]</td><td>✓</td><td>✓</td><td>×</td><td>✓</td><td>✓</td></tr><tr><td>SCM [98]</td><td>✓</td><td>✓</td><td>×</td><td>×</td><td>✓</td></tr><tr><td>Voyager [99]</td><td>✓</td><td>×</td><td>✓</td><td>×</td><td>✓</td></tr><tr><td>MemGPT [100]</td><td>✓</td><td>×</td><td>✓</td><td>×</td><td>✓</td></tr><tr><td>MemoChat [94]</td><td>✓</td><td>×</td><td>×</td><td>×</td><td>✓</td></tr><tr><td>MPC [101]</td><td>✓</td><td>×</td><td>×</td><td>×</td><td>✓</td></tr><tr><td>Generative Agents [83]</td><td>✓</td><td>×</td><td>✓</td><td>✓</td><td>✓</td></tr><tr><td>RecMind [102]</td><td>○</td><td>×</td><td>×</td><td>×</td><td>✓</td></tr><tr><td>Retroformer [103]</td><td>✓</td><td>✓</td><td>✓</td><td>×</td><td>○</td></tr><tr><td>ExpeL [82]</td><td>✓</td><td>✓</td><td>✓</td><td>×</td><td>○</td></tr><tr><td>Synapse [91]</td><td>✓</td><td>×</td><td>×</td><td>×</td><td>✓</td></tr><tr><td>GITM [93]</td><td>○</td><td>✓</td><td>✓</td><td>×</td><td>✓</td></tr><tr><td>ReAct [104]</td><td>○</td><td>×</td><td>×</td><td>×</td><td>○</td></tr><tr><td>Reflexion [5]</td><td>✓</td><td>✓</td><td>✓</td><td>×</td><td>○</td></tr><tr><td>RecAgent [95]</td><td>✓</td><td>✓</td><td>✓</td><td>✓</td><td>✓</td></tr><tr><td>Character-LLM [105]</td><td>✓</td><td>×</td><td>×</td><td>×</td><td>○</td></tr><tr><td>MAC [106]</td><td>✓</td><td>✓</td><td>✓</td><td>×</td><td>✓</td></tr><tr><td>Huatuo [107]</td><td>✓</td><td>×</td><td>×</td><td>×</td><td>○</td></tr><tr><td>ChatDev [1]</td><td>✓</td><td>×</td><td>✓</td><td>×</td><td>✓</td></tr><tr><td>InteRecAgent [108]</td><td>✓</td><td>✓</td><td>✓</td><td>×</td><td>✓</td></tr><tr><td>MetaAgents [109]</td><td>✓</td><td>×</td><td>✓</td><td>×</td><td>✓</td></tr><tr><td>TPTU [110, 111]</td><td>○</td><td>×</td><td>✓</td><td>×</td><td>✓</td></tr><tr><td>MetaGPT [112]</td><td>✓</td><td>×</td><td>✓</td><td>×</td><td>✓</td></tr><tr><td> $S^3$ [2]</td><td>✓</td><td>×</td><td>✓</td><td>✓</td><td>✓</td></tr><tr><td>InvestLM [113]</td><td>✓</td><td>×</td><td>×</td><td>×</td><td>○</td></tr></table>

## 5.3.3 Memory Reading

当 agent 需要信息进行推理与决策时，memory reading 操作将从 memory 中抽取相关信息以供使用。因此，如何为当前状态访问相关信息十分重要。由于 memory entity 数量巨大，且并非全部与当前状态相关，需要精心设计，以基于相关性及其他面向任务的因素抽取有用信息。

代表性研究。在 ChatDB [96] 中，memory reading 操作由 SQL 语句执行。这些语句将由 agent 预先作为一系列 memory chain（Chain-of-Memory）生成。在 MPC [101] 中，agent 可以从 memory pool 中 retrieve 相关 memory。该方法还提出提供思维链（Chain-of-Thought）示例，以忽略某些 memory。ExpeL [82] 利用 Faiss [124] 向量存储作为 memory pool，并获得与当前任务相似度分数最高的前 K 条成功轨迹。

讨论。在某种程度上，memory reading 与 memory writing 操作是协同的，memory writing 的形式会极大影响 memory reading 的方法。对于 textual memory 形式，大多数已有工作使用文本相似度及其他辅助信息进行读取。对于 parametric memory 形式，现有模型可能仅利用更新后的参数进行推理，这可视为一种隐式读取过程。

![](../assets/arxiv-2404.13501-fig5.jpg)  
图 5：memory module 评估方法概览。

## 6 How to Evaluate the Memory in LLM-based Agent

如何有效评估 memory module 仍是一个开放问题，已有工作根据不同应用提出了多样化的评估策略。为清晰展示不同评估方法的共同思想，本节总结一个通用框架，包含两种宽泛的评估策略（概览见图 5），即（1）直接评估，独立测量 memory module 的能力；（2）间接评估，通过端到端 agent 任务评估 memory module。若这些任务能被有效完成，则表明 memory module 有用。

## 6.1 Direct Evaluation

这类方法把 agent 的 memory 视为独立组件，并独立评估其有效性。已有研究可分为两类：主观评估与客观评估。主观评估旨在基于人类判断衡量 memory 有效性，可广泛用于缺乏客观 ground truth 的场景。客观评估基于数值指标评估 memory 有效性，便于比较不同 memory module。

## 6.1.1 Subjective Evaluation

在主观评估中，有两个关键问题，即（1）应评估哪些方面，以及（2）如何开展评估过程。首先，以下两个方面是评估 memory module 最常用的视角。

连贯性。该方面指 recalled memory 是否自然且适合当前 context。例如，若 agent 正在为 Alice 的旅行制定计划，memory 应与其旅行偏好相关，而不是工作偏好。在已有工作中，Modarressi 等人 [7] 研究 memory module 能否在不断变化的知识中提供恰当参考。Liang 等人 [98] 给出一些示例，展示当前查询与历史 memory 之间的关系。Zhong 等人 [6] 与 Liu 等人 [97] 通过评分标签评估整合 context 与 retrieved memory 的回复连贯性。Lee 等人 [101] 关注 recalled memory 与 context 之间的矛盾。

合理性。该方面旨在评估 recalled memory 是否合理。例如，若 agent 被要求回答“颐和园在哪里”，recalled memory 应是“颐和园在北京”，而不是“颐和园在月球上”。在已有工作中，Lee 等人 [101] 要求众包工作者直接为 retrieved memory 的合理性打分。Zhong 等人 [6] 与 Liu 等人 [97] 招募人类评估者，检查 memory 是否包含当前问题的合理答案。

至于如何开展评估过程，有两个重要问题。第一个是如何选择人类评估者。一般而言，评估者应熟悉评估任务，以确保标注结果可信可靠。此外，评估者的背景应多样化，以消除特定人群的主观偏差。第二个问题是如何标注 memory module 的输出。通常，可以直接为结果打分 [6]，也可以在两个候选之间进行比较 [95]。前者可以获得绝对、定量的评估结果，后者可以在独立为每个候选打分时消除标注噪声。此外，评分粒度也应仔细设计。过粗的评分可能无法有效区分不同 memory module 的能力，而过细的评分可能给工作者带来更多判断负担。

一般而言，主观评估可用于广泛场景，只需定义评估方面，并让招募的工作者作出判断。该方法通常更可解释，因为工作者可以提供判断理由。然而，主观评估因需要雇佣人类评估者而成本高昂。此外，不同评估者群体可能存在不同偏差，使结果难以复现与比较。

## 6.1.2 Objective Evaluation

在客观评估中，已有工作通常定义数值指标来评估 memory module 的有效性与效率。

结果正确性。该指标衡量 agent 能否直接基于 memory module 成功回答预定义问题。例如，问题可以是“Alice 今天去了哪里？”，两个选项为“A：颐和园”与“B：长城”。然后，agent 应基于问题及其 memory 选择正确答案。agent 生成的答案将与 ground truth 进行比较。形式上，准确率可计算为

$$
\text { Correctness } = \frac {1} {N} \sum_ {i = 1} ^ {N} \mathbb {I} \left[ a _ {i} = \hat {a} _ {i} \right],
$$

其中 N 是问题数量，$a _ { i }$ 表示第 i 个问题的 ground truth，$\hat { a } _ { i }$ 表示 agent 给出的答案，$\mathbb{I}[ a _ { i } = \hat { a } _ { i } ]$ 是匹配函数，通常表示为

$$
\mathbb {I} \left[ a _ {i} = \hat {a} _ {i} \right] = \left\{ \begin{array}{l l} 1 & \text {if} a _ {i} = \hat {a} _ {i}, \\ 0 & \text {if} a _ {i} \neq \hat {a} _ {i}. \end{array} \right.
$$

在已有工作中，Hu 等人 [96] 从带有标注 ground truth 的过去历史中构造问题，并计算 recalled memory 能否匹配正确答案的准确率。类似地，Packer 等人 [100] 生成只能从过去 session 中推导的问题与答案，并将 agent 的回复与 ground truth 比较以计算准确率。

参考准确率。该指标评估 agent 能否发现相关 memory content 来回答问题。与上述关注最终结果的指标不同，参考准确率更关注支持 agent 最终决策的中间信息。具体而言，它将 retrieved memory 与预先准备的 ground truth 进行比较。对于上述“Alice 今天去了哪里？”的问题，若 memory content 包括（A）“Alice 今天在王府井与朋友吃午饭”与（B）“Alice 午饭吃了烤鸭”，则更好的 memory module 应选择（A）作为回答问题的参考。通常，研究者利用 F1 分数评估参考准确率，其计算为

$$
\mathrm{F1} = 2 \cdot \frac {\text { Precision } \cdot \text { Recall }}{\text { Precision } + \text { Recall }},
$$

其中 precision 与 recall 计算为 Precision $= \textstyle { \frac { \mathrm { T P } } { \mathrm { T P } + \mathrm { F P } } }$ 与 $\begin{array} { r } { \mathrm { R e c a l l } = \frac { \mathrm { T P } } { \mathrm { T P } + \mathrm { F N } } } \end{array}$。TP 表示真正例 memory content 的数量，FP 表示假正例 memory content 的数量，FN 表示假负例 memory content 的数量。在已有工作中，Lu 等人 [94] 利用 F1 分数评估 memory retrieval process，Zhong 等人 [6] 关注评估相关 memory 的 retrieval 是否成功。

结果正确性与参考准确率都用于评估 memory module 的有效性。除有效性外，效率也是一个重要方面，尤其对于真实世界应用。因此，我们如下描述效率评估。

时间与硬件成本。总时间成本包括用于 memory adaptation 与推理的时间。适配时间指 memory writing 与 memory management 的时间，推理时间指 memory reading 的时间延迟。具体而言，从 memory operation 开始到结束的时间差可视为时间消耗。形式上，每类操作的平均时间消耗可表示为

$$
\Delta \text { time } = \frac {1} {M} \sum_ {i = 1} ^ {M} t _ {i} ^ {\text { end }} - t _ {i} ^ {\text { start }},
$$

其中 M 表示这些操作的数量，$t _ { i } ^ { \mathrm { e n d } }$ 表示第 i 次操作的结束时间，$t _ { i } ^ { \mathrm { s t a r t } }$ 表示该操作的开始时间。至于计算开销，可以通过峰值 GPU 内存分配来评估。在已有工作中，Tack 等人 [106] 利用峰值内存分配与适配时间来评估 memory operation 的效率。

客观评估提供了比较不同 memory 方法的数值策略，这对该领域建立 benchmark 并推动未来发展很重要。

## 6.2 Indirect Evaluation

除上述直接评估 memory module 的方法外，通过任务完成情况进行评估也是一种流行的评估策略。这类方法背后的直觉是：若 agent 能够成功完成高度依赖 memory 的任务，则说明所设计的 memory module 有效。下文介绍若干代表性的、用于间接评估 memory module 的任务。

## 6.2.1 Conversation

与人类进行对话是 agent 最重要的应用之一，memory 在该过程中起关键作用。通过把 context 信息存储在 memory 中，agent 让用户体验个性化对话，从而提升用户满意度。因此，当 agent 的其他部分确定时，对话任务的性能可以反映不同 memory module 的有效性。

在对话语境中，一致性与参与度是评估 agent memory 有效性的两种常用方法。一致性指 agent 的回复与 context 的一致程度，因为对话过程中应避免剧烈变化。例如，Lu 等人 [94] 在交互对话上评估 agent 的一致性，使用 GPT-4 为 agent 的回复打分。参与度指用户被吸引继续对话的程度。它反映 agent 回复的质量与吸引力，以及 agent 为当前对话塑造人设的能力。例如，Lee 等人 [101] 通过 SCE-p 分数评估回复的参与度，Packer 等人 [100] 利用 CSIM 分数评估 memory 对提升用户参与度的效果。

## 6.2.2 Multi-source Question-answering

多源问答可以全面评估来自多个来源的 memory information，包括 inside-trial information、cross-trial information 与外部知识。它关注来自不同内容与来源的 memory 利用与整合。

在已有工作中，Yao 等人 [104] 评估整合任务 trial 信息与维基百科外部知识的 memory。然后，Shinn 等人 [5] 与 Yao 等人 [103] 进一步纳入同一任务的 cross-trial information，允许 memory 从先前 failed trial 中获得更多经验。此外，Packer 等人 [100] 允许 agent 利用多文档信息中的 memory 进行问答。

通过评估多源问答任务，可以考察 agent memory 从多种来源整合内容的能力。它还揭示了多信息源导致的 memory conflict 问题，以及知识更新的问题，这些问题可能影响 memory module 的性能。

## 6.2.3 Long-context Applications

除上述一般应用外，在许多场景中，LLM-based agent 必须基于极长的 prompt 作出决策。在这些场景中，长 prompt 通常被视为 memory content，在驱动 agent 行为方面发挥重要作用。

在已有工作中，Huang 等人 [19] 组织了一篇关于 long-context LLM 的全面综述，总结了 long-context 场景的评估指标。此外，Shaham 等人 [138] 提出一个零样本 benchmark，用于评估 agent 对 long-context 自然语言的理解。至于具体的 long-context 任务，long-context passage retrieval 是评估 agent long-context 能力的重要任务之一。它要求 agent 在 long-context 中找到与给定问题或描述对应的正确段落 [139]。long-context 摘要生成是另一个代表性任务。它要求 agent 形成对整个 context 的全局理解，并根据描述进行总结，其中可以利用 ROUGE 等匹配分数指标将结果与 ground truth 进行比较。

long-context 应用的评估提供了更广泛的方法来评估 memory 在 agent 中的功能，关注实际下游场景。综合 benchmark [138, 140] 也为 long-context 理解能力提供了客观评估。

## 6.2.4 Other Tasks

除上述三类用于间接评估的主要任务外，一般任务中还有一些其他指标可以揭示 memory module 的有效性。

成功率指 agent 能够成功解决的任务比例。对于 Yao 等人 [104]、Shinn 等人 [5] 与 Zhao 等人 [82]，他们评估在 AlfWorld [141] 中通过推理与 memory 能够正确完成多少空间任务。在 Zhu 等人 [93] 中，他们评估在 Minecraft 中产出不同物品的成功率，以展示 memory 的效果。此外，Shinn 等人 [5] 衡量生成代码通过问题的成功率，Zheng 等人 [91] 计算计算机控制的成功率与元素选择准确率，以展示轨迹作为范例的 memory 的功能。探索程度通常出现在探索类游戏中，反映 agent 能够探索环境的程度。例如，Wang 等人 [99] 比较在 Minecraft 中探索到的不同物品数量，以反映 memory 中的技能学习。

事实上，几乎所有配备 memory 的 agent 都可以通过消融研究，比较有／无 memory module 时的性能，以评估 memory 的效果。对特定场景的评估可以更实际地反映 memory 对下游应用的重要性。

## 6.3 Discussions

与直接评估相比，通过特定任务进行间接评估更容易实施，因为已有许多公开 benchmark。然而，任务性能可归因于多种因素，memory 只是其中之一，这可能使评估结果存在偏差。通过直接评估，可以独立评估 memory module 的有效性，从而提高评估结果的可靠性。然而，据我们所知，目前还没有专门针对 LLM-based agent 中 memory module 的开源 benchmark。

## 7 Memory-enhanced Agent Applications

近来，LLM-based agent 已在广泛场景中得到研究，推动了社会进步。一般而言，大多数 LLM-based agent 都配备 memory module。然而，这些 memory 组件所承担的具体作用、它们存储的特定信息以及所采用的实现方法，在不同应用中各不相同。为给 LLM-based agent 中 memory 功能的设计提供洞见，本节回顾并总结 memory mechanism 在各种应用场景的 LLM-based agent 中如何体现。具体而言，我们将其分为若干类别：角色扮演与社会模拟、个人助理、开放世界游戏、代码生成、推荐、特定领域的专家系统以及其他应用。总结见表 4。

## 7.1 Role-playing and Social Simulation

角色扮演是 LLM-based agent 的经典应用，memory 在 agent 内部起关键作用。它赋予角色鲜明特征，使角色彼此区分。许多已有研究探索了构建角色 memory 的方法 [105, 143, 145–147]。Shao 等人 [105] 通过经验上传构建角色 memory，利用 supervised fine-tuning（SFT）把 memory 注入模型参数。Li 等人 [143] 通过改进的 prompt 与从剧本中抽取的角色 memory 增强 LLM 的角色扮演能力，其中用户查询与聊天机器人的回复被拼接为序列作为 memory。Wang 等人 [145] 把角色特定知识与 episode memory 注入 LLM-based agent，其中 context 问答对被拼接为 episode memory。Zhao 等人 [146] 旨在生成类人回复，以从叙事中抽取的人格特质为引导，这些特质可按相关性与重要性进行存储与 retrieval。Zhou 等人 [147] 为不同角色生成基于角色的对话，并通过 SFT 赋予 LLM-based agent 相应风格。

表 4：Memory-enhanced Agent Applications 汇总。

<table><tr><td>Application</td><td>Model</td></tr><tr><td>Role-playing</td><td>Character-LLM [105]<br>ChatHaruhi [143]<br>RoleLLM [145]<br>NarrativePlay [146]<br>CharacterGLM [147]</td></tr><tr><td>Social simulation</td><td>Generative Agents [83]<br>Lyfe Agents [148]<br> $S^3$ [2]<br>MetaAgents [109]<br>WarAgent [150]</td></tr><tr><td>Personal assistant</td><td>MemoryBank [6]<br>RET-LLM [7]<br>MemoChat [94]<br>MemGPT [100]<br>MPC [101]<br>AutoGen [153]<br>ChatDB [96]<br>TiM [97]<br>SCM [98]</td></tr><tr><td>Game</td><td>Voyager [99]<br>GITM [93]<br>JARVIS [159]<br>LARP [161]</td></tr><tr><td>Code generation</td><td>RTLFixer [142]<br>GameGPT [144]<br>ChatDev [1]<br>MetaGPT [109]<br>CodeAgent [114]</td></tr><tr><td>Recommendation</td><td>RecAgent [95]<br>InteRecAgent [108]<br>RecMind [102]<br>AgentCF [149]</td></tr><tr><td>Medicine</td><td>Huatuo [107]<br>DoctorGLM [129]<br>Radiology-GPT [132]<br>Wang et al. [151]<br>EHRAgent [152]<br>ChatDoctor [115]</td></tr><tr><td>Finance</td><td>InvestLM [113]<br>TradingGPT [154]<br>QuantAgent [155]<br>FinMem [156]<br>Koa et al. [157]</td></tr><tr><td>Science</td><td>Chemist-X [158]<br>ChemDFM [160]<br>MatChat [162]</td></tr></table>

社会模拟基本上是角色扮演的延伸，更关注 multi-agent 建模。memory module 是此类应用的重要组成部分，有助于准确模拟人类的动态行为。在已有研究中，Kaiya 等人 [148] 提出一种“Summarize-and-Forget” memory mechanism，以便在社会场景中更好地自我监控。Gao 等人 [2] 关注社交网络模拟系统。系统中的每个 agent 都有一个 memory pool，由来自在线平台的多样用户消息组成，用于识别用户。Li 等人 [163] 维护对话 context，涵盖经济环境与前几个月的 agent decision-making，以模拟广泛宏观经济趋势对 agent decision-making 的影响，并使 agent 把握市场动态。Li 等人 [109] 模拟人类社会中的求职场景，其中 agent 的 memory 最初包含档案与目标，并进一步用对话与个人 reflection 等其他信息丰富。Hua 等人 [150] 模拟战争参与国的决策与后果，其中 agent 的对话被持续维护进 memory。

为角色扮演与社会模拟设计 agent memory 有若干洞见。第一，memory 应与角色特征一致，可用于识别每个角色并将其与其他角色区分。这对提升角色扮演的真实性与社会模拟的多样性至关重要。第二，memory 应适当影响 agent 的后续动作，以确保其行为的一致性与合理性。此外，对于 humanoid agent，其 memory mechanism 应与 human memory 的特征一致，例如 forgetting 与 long-term／short-term memory，并应参考认知心理学理论。

## 7.2 Personal Assistant

LLM-based agent 非常适合创建个人助理，例如能够与用户进行长期对话的 agent [94, 101, 153]，以及负责自动查找信息的 agent [164]。这些 agent 通常需要记住先前对话以保持一致性，并记住关键风格与事件以生成更个性化、更相关的回复。Lu 等人 [94] 通过保存对话内容与信息来维持对话的 context 一致性，这有助于通过 retrieval 找到恰当的相关信息。Lee 等人 [101] 总结对话以抽取重要信息、存储信息，并为未来推理 retrieve 信息。Pan 等人 [164] 关注信息查找任务，设计 memory module 存储用户 context 信息，并借助工具使用增强外部知识。Wu 等人 [153] 保留重要 context 作为 memory，以维持对话一致性。

总之，个人助理的大多数 memory implementation 采用文本形式的 retrieval 方法，因为它们更擅长从对话片段中找到相关信息。对于 memory storage，agent 应记住用户—agent 交互中的事实信息，以及用户的个人风格，以生成针对用户情境量身定制的回复。此外，在从 memory 中 recall 时，agent 应识别并 retrieve 与当前查询和 context 相关的 memory。这一原则可使 agent 正确理解用户需求，并保持对话的一致性。

## 7.3 Open-world Game

对于游戏与开放世界探索，LLM-based agent 通常把过往观测维护为任务 context，并把先前成功 trial 中的经验存储起来。通过利用过去经验，agent 可以避免反复犯同样的错误，并形成对环境的更高层理解，从而更有效地探索。其中一些 agent 可以获取外部数据库或 API 来获得通用知识 [99, 93, 159, 161]。Wang 等人 [99] 把获得的技能存入 memory，以便在 Minecraft 中后续使用。Zhu 等人 [93] 存储并 retrieve 成功轨迹作为类似任务的示例，并通过 API 调用利用外部 Minecraft Wiki。Wang 等人 [159] 构建多模态 memory 作为知识库，并通过 retrieve 交互经验为 prompt 提供示例。Yan 等人 [161] 维护用于决策的 working memory，保存并 retrieve 相关过去经验，并实现外部数据集以获取通用知识。

总之，无论 inside-trial information 还是 cross-trial information，memory 的关键都在于对过去的交互进行 reflection，并提炼可应用于后续探索的经验。除通过亲自参与的 trial 积累经验外，吸收外部知识作为 agent memory 的一部分，也是增强 agent 探索能力的重要方式。

## 7.4 Code Generation

在代码生成场景中，LLM-based agent 可以从 memory 中搜索相关信息，从而获得更多开发知识。它们可以为未来问题保存先前经验，也可以在对话式开发界面中维护 context [142, 144, 1, 109]。Tsai 等人 [142] 构建一个外部非 parametric memory 数据库，存储编译器错误与人类专家指令，用于自动修复语法错误。在 [144] 中，个人信息将被存储在 memory 中，有助于为决策保留 context 与知识。Qian 等人 [1] 采用 multi-agent 开发软件，其中每个角色维护一个 memory，存储与其他角色的过去对话。Li 等人 [109] 也关注软件开发，当出现错误时，agent 可以 retrieve 保留在 memory 中的历史记录。Zhang 等人 [114] 在代码生成遇到问题时可以搜索相关信息。

通过利用外部资源，agent 可以从代码相关知识中学习并存入 memory，从而增强代码生成能力。此外，memory 可以改善代码生成的连续性与一致性。通过整合 context memory，agent 可以更好地理解软件开发需求，从而增强生成代码的连贯性。此外，memory 对代码的迭代优化也至关重要，因为它可以基于历史识别开发者的目标。

## 7.5 Recommendation

在推荐领域，一些已有工作关注在推荐系统中模拟用户 [95, 108]，其中 memory 可以表示真实世界中的用户画像与历史。另一些工作尝试提升推荐性能，或提供其他形式的推荐接口 [149, 102]。Wang 等人 [95] 在推荐场景中模拟用户行为，为推荐系统生成数据，agent 把过往观测与洞见存入分层 memory。在 Huang 等人 [108] 中，LLM-based agent 中的 memory 可以归档用户长期的对话历史，并捕捉与当前 prompt 相关的最新对话，以模拟交互式推荐系统。它还使用 actor-critic reflection 来提升 agent 的鲁棒性。[149] 中的 item agent 与 user agent 配备不同 memory，其中 item agent 被赋予动态 memory module，用于捕捉并保留与其内在属性及采用者倾向相关的信息。对于 user agent，自适应 memory update 机制在使 agent 操作与用户行为和偏好对齐方面起关键作用。Wang 等人 [102] 把个性化用户信息存入 memory，如对物品的评论或评分，并通过网络搜索工具获取领域特定知识与实时信息。

无论是模拟推荐系统中的用户还是捕捉其偏好，通过 memory 保留个性化信息都必不可少。一个关键挑战在于如何把个性化信息与反馈和 LLM 对齐，并存入 agent memory。这也是弥合传统推荐模型与 LLM 之间差距的重要任务。

## 7.6 Expert System in Specific Domains

医学领域。在医学领域，大多数已有工作把外部知识注入 LLM-based agent 的 memory 中 [107, 129, 132, 151, 115]。Wang 等人 [107] 以问答形式用医学知识图谱 CMeKG [165] 对 LLaMA 进行 fine-tuning [127]，以增强其医学领域知识。Xiong 等人 [129] 采用 LoRA [131] 在医疗基础模型上进行高效 fine-tuning。Wang 等人 [151] 赋予 LLM-based agent 获取基于文本的外部知识作为推理参考。此外，Shi 等人 [152] 基于过去经验中最相关的成功案例构建 memory，并使用相似度指标 retrieve 医学领域的相关问题。

金融领域。一些已有工作也把 LLM-based agent 应用于金融领域，其 memory 可以存储金融知识 [113]、市场信息 [154, 156] 与成功经验 [157, 155]。Yang 等人 [113] 构建金融投资数据集，并对 LLaMA 进行 fine-tuning [127]，以赋予投资知识。Li 等人 [154] 设计分层 memory 结构来存储不同类型的市场信息。Wang 等人 [155] 记录交易与信息等持续交互，以确保回复一致，并把先前输出记录为经验，用于 retrieve 相关示例，为 agent 提供多样化的学习 context。Koa 等人 [157] 存储过去价格走势与解释，并对 previous trial 生成 reflection。Yu 等人 [156] 采用分层 memory mechanism 为推理提供丰富信息。

科学。在科学领域，一些现有工作设计在 memory 中存储大量知识的 LLM-based agent 来解决问题 [158, 160, 162]。Chen 等人 [158] 把分子数据库与在线文献作为 LLM-based agent memory 中的外部知识，并在需要相关信息时 retrieve。Zhao 等人 [160] 与 Chen 等人 [162] 分别通过化学与结构化材料领域的 fine-tuning 赋予领域知识。

要基于 agent 在特定垂直领域构建专家系统，必须在其 memory 中保留领域特定知识。然而，存在若干挑战。第一，领域知识专业性强、准确度要求高，导致 memory storage 的构建困难。第二，领域知识往往具有时效性，未来可能过时。因此，当部分知识过时时，memory 需要部分更新。此外，领域知识体量庞大，难以基于当前查询从 memory 中 recall。

## 7.7 Other Applications

LLM-based agent 中还有一些其他 memory application。Wang 等人 [166] 关注云根因分析任务，使用 memory 存储框架规则、任务需求、工具文档、少样本示例与 agent 观测。Qiang 等人 [167] 求解本体匹配问题。agent 保存对话，并构建一个数据库以 retrieve 外部知识。Wen 等人 [168] 研究自动驾驶，其 memory module 由向量数据库构建，包含过去驾驶场景的经验。Wang 等人 [169] 提出改进用户验收测试，采用自我 reflection 机制。每次 trial 后，operation agent 总结对话并更新 memory pool，直到当前步骤的目标完成。

对于不同应用，memory 的重点各不相同，因为它本质上服务于下游任务。因此，设计还应考虑任务需求。

## 8 Limitations & Future Directions

## 8.1 More Advances in Parametric Memory

目前，LLM-based agent 的 memory 主要以文本形式为主，尤其是观测记录、trial experience 与文本知识库等 context 知识。尽管 textual memory 具有可解释、易扩展与易编辑的优点，但它也意味着相对 parametric memory 在效率上的牺牲。本质上，parametric memory 具有更高的信息密度，通过 latent space 中的连续实值向量表达语义，而 textual memory 使用离散空间中的 token 组合进行语义表达。因此，parametric memory 提供更丰富的表达空间，其软编码相比 token 序列的硬编码形式更鲁棒。此外，parametric memory 更节省存储，不需要显式存储大量文本，类似一个知识压缩过程。至于 memory management，如 consolidation 与 reflection，parametric memory 不一定像 textual memory 那样设计人工规则，而可以采用优化方法隐式学习这些过程。此外，可插拔的 parametric memory 类似一张数字生命卡，能够赋予 agent 所需特征。例如，Huatuo [107] 旨在通过在中文医学知识库上对 Llama [127] 模型进行 fine-tuning，为 agent 增强生物医学领域专业知识。MAC [106] 旨在创建适用于在线环境的 parametric memory 适配框架，采用元学习技术替代传统优化阶段。

尽管 parametric memory 前景广阔，但目前面临诸多挑战。其中最首要的是效率问题：如何有效地把文本信息转化为参数或参数修改，是一个关键问题。目前，研究者可以通过 SFT 把大量领域知识迁移到 LLM 参数中。然而，这耗时且需要大量文本语料，因而不适合情境性知识。一种可行方法是采用元学习，让模型学会 memory。例如，MEND [134] 利用元学习方法训练一个紧凑模型，该模型能够为预训练语言模型的参数生成调整。此外，parametric memory 缺乏可解释性也可能成为障碍，尤其是在医学等需要高度信任的领域。因此，提升 parametric memory 的可信度与可解释性是一个亟待解决的问题。

## 8.2 Memory in LLM-based Multi-agent Applications

LLM 中 memory mechanism 的探索已蓬勃发展为一个动态的 multi-agent systems（MAS）领域，在同步、通信与信息不对称管理方面取得显著进展。合作场景中出现的一个关键方面是 agent 之间的 memory synchronization。该过程是建立统一知识库、确保不同 agent decision-making 一致的基础。例如，Chen 等人 [170] 强调为多机器人协作整合同步 memory module 的重要性。另一个重要方面是 agent 之间的通信，这严重依赖 memory 来维护 context 与解释消息。例如，Mandi 等人 [171] 说明了 memory 驱动的通信框架，促进 agent 之间的共同理解。除合作场景外，一些研究还关注竞争场景，信息不对称成为关键问题 [172]。

展望未来，基于 LLM 的 MAS 中 memory 的发展正处于技术创新与策略应用的交汇点。它呼唤探索新的 memory module，以进一步增强 agent 同步、实现更有效的通信，并在信息丰富的环境中提供策略优势。此类 memory 模型的发展不仅需要应对当前的 memory integration 与 management 挑战，还需要探索 memory 在促进更鲁棒、更智能、更具适应性的 MAS 方面的未开发潜力。正如开创性研究所表明的，基于 LLM 的 MAS 不断演进的图景为 memory utilization 与 management 的未来创新奠定了有前景的基础。这一探索有望揭示 memory integration 的新维度，拓展当前可实现能力的边界，并在 MAS 领域确立新的 benchmark。

## 8.3 Memory-based Lifelong Learning

终身学习是人工智能中的一个高级主题，将 agent 的学习能力扩展到其整个生命周期 [173]。agent 可以持续与环境交互、持久观察环境并获取外部知识，从而实现类似人类的增强模式。agent 的 memory 是实现终身学习的关键，因为它需要学会存储并应用过去的观测。LLM-based agent 中的终身学习具有显著实用价值，例如在长期社会模拟与个人助理中。然而，它也面临若干挑战。第一，终身学习具有时间性，要求 agent memory 捕捉时间性。这种时间性可能导致 memory 之间的交互，例如 memory overlap。此外，由于终身学习周期很长，需要存储大量 memory 并在需要时 retrieve 这些 memory，可能还需要纳入某种 forgetting mechanism。

## 8.4 Memory in Humanoid Agent

humanoid agent 指被设计为表现出与人类一致行为的 agent，从而促进社会模拟、人类行为研究与角色扮演中的应用。与通常偏好更强能力的任务型 agent 不同，humanoid agent 的能力水平应贴近模仿人类。因此，humanoid agent 的 memory 应与人类认知过程一致，遵循 memory distortion 与 forgetting 等心理学原则。此外，humanoid agent 应具备知识边界，即其知识应对应于其所复现实体的知识。例如，在角色扮演场景中，扮演儿童的 agent 不应具备超出该年龄典型水平的进阶数学概念或其他复杂知识 [174]。

## 9 Conclusion

在本综述中，我们对 LLM-based agent 的 memory mechanism 进行了系统回顾，重点关注三个关键问题，包括 LLM-based agent 中 memory module 的“是什么”“为什么需要”以及“如何设计与评估”。为展示 agent memory 的重要性，我们还介绍了许多 memory module 发挥重要作用的典型应用。我们相信本综述可为该领域的新手提供有价值的参考，也希望它能启发更先进的 memory mechanism，以增强 LLM-based agent。

## Acknowledgement

我们感谢 Lei Wang 对本文的校对与宝贵建议。

## References

[1] Chen Qian, Xin Cong, Cheng Yang, Weize Chen, Yusheng Su, Juyuan Xu, Zhiyuan Liu, and Maosong Sun. Communicative agents for software development. arXiv preprint arXiv:2307.07924, 2023.

[2] Chen Gao, Xiaochong Lan, Zhihong Lu, Jinzhu Mao, Jinghua Piao, Huandong Wang, Depeng Jin, and Yong Li. S<sup>3</sup>: Social-network simulation system with large language model-empowered agents. arXiv preprint arXiv:2307.14984, 2023.

[3] Lei Wang, Chen Ma, Xueyang Feng, Zeyu Zhang, Hao Yang, Jingsen Zhang, Zhiyuan Chen, Jiakai Tang, Xu Chen, Yankai Lin, et al. A survey on large language model based autonomous agents. arXiv preprint arXiv:2308.11432, 2023.

[4] Zhiheng Xi, Wenxiang Chen, Xin Guo, Wei He, Yiwen Ding, Boyang Hong, Ming Zhang, Junzhe Wang, Senjie Jin, Enyu Zhou, et al. The rise and potential of large language model based agents: A survey. arXiv preprint arXiv:2309.07864, 2023.

[5] Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik R Narasimhan, and Shunyu Yao. Reflexion: Language agents with verbal reinforcement learning. In Thirty-seventh Conference on Neural Information Processing Systems, 2023.

[6] Wanjun Zhong, Lianghong Guo, Qiqi Gao, and Yanlin Wang. Memorybank: Enhancing large language models with long-term memory. arXiv preprint arXiv:2305.10250, 2023.

[7] Ali Modarressi, Ayyoob Imani, Mohsen Fayyaz, and Hinrich Schütze. Ret-llm: Towards a general read-write memory for large language models. arXiv preprint arXiv:2305.14322, 2023.

[8] Shengyu Zhang, Linfeng Dong, Xiaoya Li, Sen Zhang, Xiaofei Sun, Shuhe Wang, Jiwei Li, Runyi Hu, Tianwei Zhang, Fei Wu, et al. Instruction tuning for large language models: A survey. arXiv preprint arXiv:2308.10792, 2023.

[9] Tianhao Shen, Renren Jin, Yufei Huang, Chuang Liu, Weilong Dong, Zishan Guo, Xinwei Wu, Yan Liu, and Deyi Xiong. Large language model alignment: A survey. arXiv preprint arXiv:2309.15025, 2023.

[10] Yufei Wang, Wanjun Zhong, Liangyou Li, Fei Mi, Xingshan Zeng, Wenyong Huang, Lifeng Shang, Xin Jiang, and Qun Liu. Aligning large language models with human: A survey. arXiv preprint arXiv:2307.12966, 2023.

[11] Yang Liu, Yuanshun Yao, Jean-Francois Ton, Xiaoying Zhang, Ruocheng Guo Hao Cheng, Yegor Klochkov, Muhammad Faaiz Taufiq, and Hang Li. Trustworthy llms: a survey and guideline for evaluating large language models’ alignment. arXiv preprint arXiv:2308.05374, 2023.

[12] Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Jinliu Pan, Yuxi Bi, Yi Dai, Jiawei Sun, and Haofen Wang. Retrieval-augmented generation for large language models: A survey. arXiv preprint arXiv:2312.10997, 2023.

[13] Song Wang, Yaochen Zhu, Haochen Liu, Zaiyi Zheng, Chen Chen, et al. Knowledge editing for large language models: A survey. arXiv preprint arXiv:2310.16218, 2023.

[14] Yunzhi Yao, Peng Wang, Bozhong Tian, Siyuan Cheng, Zhoubo Li, Shumin Deng, Huajun Chen, and Ningyu Zhang. Editing large language models: Problems, methods, and opportuni ties. arXiv preprint arXiv:2305.13172, 2023.

[15] Peng Wang, Ningyu Zhang, Xin Xie, Yunzhi Yao, Bozhong Tian, Mengru Wang, Zekun Xi, Siyuan Cheng, Kangwei Liu, Guozhou Zheng, et al. Easyedit: An easy-to-use knowledge editing framework for large language models. arXiv preprint arXiv:2308.07269, 2023.

[16] Zhangyin Feng, Weitao Ma, Weijiang Yu, Lei Huang, Haotian Wang, Qianglong Chen, Weihua Peng, Xiaocheng Feng, Bing Qin, et al. Trends in integration of knowledge and large language models: A survey and taxonomy of methods, benchmarks, and applications. arXiv preprint arXiv:2311.05876, 2023.

[17] Ningyu Zhang, Yunzhi Yao, Bozhong Tian, Peng Wang, Shumin Deng, Mengru Wang, Zekun Xi, Shengyu Mao, Jintian Zhang, Yuansheng Ni, et al. A comprehensive study of knowledge editing for large language models. arXiv preprint arXiv:2401.01286, 2024.

[18] Yujia Qin, Shengding Hu, Yankai Lin, Weize Chen, Ning Ding, Ganqu Cui, Zheni Zeng, Yufei Huang, Chaojun Xiao, Chi Han, et al. Tool learning with foundation models. arXiv preprint arXiv:2304.08354, 2023.

[19] Yunpeng Huang, Jingwei Xu, Zixu Jiang, Junyu Lai, Zenan Li, Yuan Yao, Taolue Chen, Lijuan Yang, Zhou Xin, and Xiaoxing Ma. Advancing transformer architecture in long-context large language models: A comprehensive survey. arXiv preprint arXiv:2311.12351, 2023.

[20] Xindi Wang, Mahsa Salmani, Parsa Omidi, Xiangyu Ren, Mehdi Rezagholizadeh, and Armaghan Eshaghi. Beyond the limits: A survey of techniques to extend the context length in large language models. arXiv preprint arXiv:2402.02244, 2024.

[21] Saurav Pawar, SM Tonmoy, SM Zaman, Vinija Jain, Aman Chadha, and Amitava Das. The what, why, and how of context length extension techniques in large language models–a detailed survey. arXiv preprint arXiv:2401.07872, 2024.

[22] Jiayang Wu, Wensheng Gan, Zefeng Chen, Shicheng Wan, and S Yu Philip. Multimodal large language models: A survey. In 2023 IEEE International Conference on Big Data (BigData), pages 2247–2256. IEEE, 2023.

[23] Shezheng Song, Xiaopeng Li, and Shasha Li. How to bridge the gap between modalities: A comprehensive survey on multimodal large language model. arXiv preprint arXiv:2311.07594, 2023.

[24] Davide Caffagni, Federico Cocchi, Luca Barsellotti, Nicholas Moratelli, Sara Sarto, Lorenzo Baraldi, Marcella Cornia, and Rita Cucchiara. The (r) evolution of multimodal large language models: A survey. arXiv preprint arXiv:2402.12451, 2024.

[25] Shukang Yin, Chaoyou Fu, Sirui Zhao, Ke Li, Xing Sun, Tong Xu, and Enhong Chen. A survey on multimodal large language models. arXiv preprint arXiv:2306.13549, 2023.

[26] Guangji Bai, Zheng Chai, Chen Ling, Shiyu Wang, Jiaying Lu, Nan Zhang, Tingwei Shi, Ziyang Yu, Mengdan Zhu, Yifei Zhang, et al. Beyond efficiency: A systematic survey of resource-efficient large language models. arXiv preprint arXiv:2401.00625, 2024.

[27] Zhongwei Wan, Xin Wang, Che Liu, Samiul Alam, Yu Zheng, Zhongnan Qu, Shen Yan, Yi Zhu, Quanlu Zhang, Mosharaf Chowdhury, et al. Efficient large language models: A survey. arXiv preprint arXiv:2312.03863, 1, 2023.

[28] Xupeng Miao, Gabriele Oliaro, Zhihao Zhang, Xinhao Cheng, Hongyi Jin, Tianqi Chen, and Zhihao Jia. Towards efficient generative large language model serving: A survey from algorithms to systems. arXiv preprint arXiv:2312.15234, 2023.

[29] Lingling Xu, Haoran Xie, Si-Zhao Joe Qin, Xiaohui Tao, and Fu Lee Wang. Parameter-efficient fine-tuning methods for pretrained language models: A critical review and assessment. arXiv preprint arXiv:2312.12148, 2023.

[30] Xunyu Zhu, Jian Li, Yong Liu, Can Ma, and Weiping Wang. A survey on model compression for large language models. arXiv preprint arXiv:2308.07633, 2023.

[31] Canwen Xu and Julian McAuley. A survey on model compression and acceleration for pretrained language models. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 37, pages 10566–10575, 2023.

[32] Wenxiao Wang, Wei Chen, Yicong Luo, Yongliu Long, Zhengkai Lin, Liye Zhang, Binbin Lin, Deng Cai, and Xiaofei He. Model compression and efficient inference for large language models: A survey. arXiv preprint arXiv:2402.09748, 2024.

[33] Seungcheol Park, Jaehyeon Choi, Sojin Lee, and U Kang. A comprehensive survey of compression algorithms for language models. arXiv preprint arXiv:2401.15347, 2024.

[34] Yupeng Chang, Xu Wang, Jindong Wang, Yuan Wu, Linyi Yang, Kaijie Zhu, Hao Chen, Xiaoyuan Yi, Cunxiang Wang, Yidong Wang, et al. A survey on evaluation of large language models. ACM Transactions on Intelligent Systems and Technology, 2023.

[35] Zishan Guo, Renren Jin, Chuang Liu, Yufei Huang, Dan Shi, Linhao Yu, Yan Liu, Jiaxuan Li, Bojian Xiong, Deyi Xiong, et al. Evaluating large language models: A comprehensive survey. arXiv preprint arXiv:2310.19736, 2023.

[36] Jingfeng Yang, Hongye Jin, Ruixiang Tang, Xiaotian Han, Qizhang Feng, Haoming Jiang, Bing Yin, and Xia Hu. Harnessing the power of llms in practice: A survey on chatgpt and beyond. arXiv preprint arXiv:2304.13712, 2023.

[37] Yutao Zhu, Huaying Yuan, Shuting Wang, Jiongnan Liu, Wenhan Liu, Chenlong Deng, Zhicheng Dou, and Ji-Rong Wen. Large language models for information retrieval: A survey. arXiv preprint arXiv:2308.07107, 2023.

[38] Derong Xu, Wei Chen, Wenjun Peng, Chao Zhang, Tong Xu, Xiangyu Zhao, Xian Wu, Yefeng Zheng, and Enhong Chen. Large language models for generative information extraction: A survey. arXiv preprint arXiv:2312.17617, 2023.

[39] Angela Fan, Beliz Gokkaya, Mark Harman, Mitya Lyubarskiy, Shubho Sengupta, Shin Yoo, and Jie M Zhang. Large language models for software engineering: Survey and open problems. arXiv preprint arXiv:2310.03533, 2023.

[40] Junjie Wang, Yuchao Huang, Chunyang Chen, Zhe Liu, Song Wang, and Qing Wang. Software testing with large language models: Survey, landscape, and vision. IEEE Transactions on Software Engineering, 2024.

[41] Zibin Zheng, Kaiwen Ning, Yanlin Wang, Jingwen Zhang, Dewu Zheng, Mingxi Ye, and Jiachi Chen. A survey of large language models for code: Evolution, benchmarking, and future trends. arXiv preprint arXiv:2311.10372, 2023.

[42] Fanlong Zeng, Wensheng Gan, Yongheng Wang, Ning Liu, and Philip S Yu. Large language models for robotics: A survey. arXiv preprint arXiv:2311.07226, 2023.

[43] Can Cui, Yunsheng Ma, Xu Cao, Wenqian Ye, Yang Zhou, Kaizhao Liang, Jintai Chen, Juanwu Lu, Zichong Yang, Kuei-Da Liao, et al. A survey on multimodal large language models for autonomous driving. In Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision, pages 958–979, 2024.

[44] Zhenjie Yang, Xiaosong Jia, Hongyang Li, and Junchi Yan. A survey of large language models for autonomous driving. arXiv preprint arXiv:2311.01043, 2023.

[45] Kai He, Rui Mao, Qika Lin, Yucheng Ruan, Xiang Lan, Mengling Feng, and Erik Cambria. A survey of large language models for healthcare: from data, technology, and applications to accountability and ethics. arXiv preprint arXiv:2310.05694, 2023.

[46] Hongjian Zhou, Boyang Gu, Xinyu Zou, Yiru Li, Sam S Chen, Peilin Zhou, Junling Liu, Yining Hua, Chengfeng Mao, Xian Wu, et al. A survey of large language models in medicine: Progress, application, and challenge. arXiv preprint arXiv:2311.05112, 2023.

[47] Benyou Wang, Qianqian Xie, Jiahuan Pei, Zhihong Chen, Prayag Tiwari, Zhao Li, and Jie Fu. Pre-trained language models in biomedical domain: A systematic survey. ACM Computing Surveys, 56(3):1–52, 2023.

[48] Yinheng Li, Shaofei Wang, Han Ding, and Hang Chen. Large language models in finance: A survey. In Proceedings of the Fourth ACM International Conference on AI in Finance, pages 374–382, 2023.

[49] Tianyu He, Guanghui Fu, Yijing Yu, Fan Wang, Jianqiang Li, Qing Zhao, Changwei Song, Hongzhi Qi, Dan Luo, Huijing Zou, et al. Towards a psychological generalist ai: A survey of current applications of large language models and future prospects. arXiv preprint arXiv:2312.04578, 2023.

[50] Lei Li, Yongfeng Zhang, Dugang Liu, and Li Chen. Large language models for generative recommendation: A survey and visionary discussions. arXiv preprint arXiv:2309.01157, 2023.

[51] Jianghao Lin, Xinyi Dai, Yunjia Xi, Weiwen Liu, Bo Chen, Xiangyang Li, Chenxu Zhu, Huifeng Guo, Yong Yu, Ruiming Tang, et al. How can recommender systems benefit from large language models: A survey. arXiv preprint arXiv:2306.05817, 2023.

[52] Wenjie Wang, Xinyu Lin, Fuli Feng, Xiangnan He, and Tat-Seng Chua. Generative recommendation: Towards next-generation recommender paradigm. arXiv preprint arXiv:2304.03516, 2023.

[53] Yue Zhang, Yafu Li, Leyang Cui, Deng Cai, Lemao Liu, Tingchen Fu, Xinting Huang, Enbo Zhao, Yu Zhang, Yulong Chen, et al. Siren’s song in the ai ocean: a survey on hallucination in large language models. arXiv preprint arXiv:2309.01219, 2023.

[54] Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong, Zhangyin Feng, Haotian Wang, Qianglong Chen, Weihua Peng, Xiaocheng Feng, Bing Qin, et al. A survey on hallucination in large language models: Principles, taxonomy, challenges, and open questions. arXiv preprint arXiv:2311.05232, 2023.

[55] Vipula Rawte, Amit Sheth, and Amitava Das. A survey of hallucination in large foundation models. arXiv preprint arXiv:2309.05922, 2023.

[56] Hongbin Ye, Tong Liu, Aijia Zhang, Wei Hua, and Weiqiang Jia. Cognitive mirage: A review of hallucinations in large language models. arXiv preprint arXiv:2309.06794, 2023.

[57] Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu, Etsuko Ishii, Ye Jin Bang, Andrea Madotto, and Pascale Fung. Survey of hallucination in natural language generation. ACM Computing Surveys, 55(12):1–38, 2023.

[58] SM Tonmoy, SM Zaman, Vinija Jain, Anku Rani, Vipula Rawte, Aman Chadha, and Amitava Das. A comprehensive survey of hallucination mitigation techniques in large language models. arXiv preprint arXiv:2401.01313, 2024.

[59] Xuhui Jiang, Yuxing Tian, Fengrui Hua, Chengjin Xu, Yuanzhuo Wang, and Jian Guo. A survey on large language model hallucination via a creativity perspective. arXiv preprint arXiv:2402.06647, 2024.

[60] Isabel O Gallegos, Ryan A Rossi, Joe Barrow, Md Mehrab Tanjim, Sungchul Kim, Franck Dernoncourt, Tong Yu, Ruiyi Zhang, and Nesreen K Ahmed. Bias and fairness in large language models: A survey. arXiv preprint arXiv:2309.00770, 2023.

[61] Hadas Kotek, Rikker Dockum, and David Sun. Gender bias and stereotypes in large language models. In Proceedings ofThe ACM Collective Intelligence Conference, pages 12–24, 2023.

[62] Yingji Li, Mengnan Du, Rui Song, Xin Wang, and Ying Wang. A survey on fairness in large language models. arXiv preprint arXiv:2308.10149, 2023.

[63] Haiyan Zhao, Hanjie Chen, Fan Yang, Ninghao Liu, Huiqi Deng, Hengyi Cai, Shuaiqiang Wang, Dawei Yin, and Mengnan Du. Explainability for large language models: A survey. ACM Transactions on Intelligent Systems and Technology, 2023.

[64] Yifan Yao, Jinhao Duan, Kaidi Xu, Yuanfang Cai, Eric Sun, and Yue Zhang. A survey on large language model (llm) security and privacy: The good, the bad, and the ugly. arXiv preprint arXiv:2312.02003, 1, 2023.

[65] Erfan Shayegani, Md Abdullah Al Mamun, Yu Fu, Pedram Zaree, Yue Dong, and Nael Abu-Ghazaleh. Survey of vulnerabilities in large language models revealed by adversarial attacks. arXiv preprint arXiv:2310.10844, 2023.

[66] Seth Neel and Peter Chang. Privacy issues in large language models: A survey. arXiv preprint arXiv:2312.06717, 2023.

[67] Victoria Smith, Ali Shahin Shamsabadi, Carolyn Ashurst, and Adrian Weller. Identifying and mitigating privacy risks stemming from language models: A survey. arXiv preprint arXiv:2310.01424, 2023.

[68] Zhichen Dong, Zhanhui Zhou, Chao Yang, Jing Shao, and Yu Qiao. Attacks, defenses and evaluations for llm conversation safety: A survey. arXiv preprint arXiv:2402.09283, 2024.

[69] Badhan Chandra Das, M Hadi Amini, and Yanzhao Wu. Security and privacy challenges of large language models: A survey. arXiv preprint arXiv:2402.00888, 2024.

[70] Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yupeng Hou, Yingqian Min, Beichen Zhang, Junjie Zhang, Zican Dong, et al. A survey of large language models. arXiv preprint arXiv:2303.18223, 2023.

[71] Muhammad Usman Hadi, Rizwan Qureshi, Abbas Shah, Muhammad Irfan, Anas Zafar, Muhammad Bilal Shaikh, Naveed Akhtar, Jia Wu, Seyedali Mirjalili, et al. A survey on large language models: Applications, challenges, limitations, and practical usage. Authorea Preprints, 2023.

[72] Bonan Min, Hayley Ross, Elior Sulem, Amir Pouran Ben Veyseh, Thien Huu Nguyen, Oscar Sainz, Eneko Agirre, Ilana Heintz, and Dan Roth. Recent advances in natural language processing via large pre-trained language models: A survey. ACM Computing Surveys, 56(2): 1–40, 2023.

[73] Grégoire Mialon, Roberto Dessì, Maria Lomeli, Christoforos Nalmpantis, Ram Pasunuru, Roberta Raileanu, Baptiste Rozière, Timo Schick, Jane Dwivedi-Yu, Asli Celikyilmaz, et al. Augmented language models: a survey. arXiv preprint arXiv:2302.07842, 2023.

[74] Xu Huang, Weiwen Liu, Xiaolong Chen, Xingmei Wang, Hao Wang, Defu Lian, Yasheng Wang, Ruiming Tang, and Enhong Chen. Understanding the planning of llm agents: A survey. arXiv preprint arXiv:2402.02716, 2024.

[75] Taicheng Guo, Xiuying Chen, Yaqi Wang, Ruidi Chang, Shichao Pei, Nitesh V Chawla, Olaf Wiest, and Xiangliang Zhang. Large language model based multi-agents: A survey of progress and challenges. arXiv preprint arXiv:2402.01680, 2024.

[76] Yuanchun Li, Hao Wen, Weijun Wang, Xiangyu Li, Yizhen Yuan, Guohong Liu, Jiacheng Liu, Wenxing Xu, Xiang Wang, Yi Sun, et al. Personal llm agents: Insights and survey about the capability, efficiency and security. arXiv preprint arXiv:2401.05459, 2024.

[77] Pengyu Zhao, Zijian Jin, and Ning Cheng. An in-depth survey of large language model-based artificial intelligence agents. arXiv preprint arXiv:2309.14365, 2023.

[78] Yuheng Cheng, Ceyao Zhang, Zhengwen Zhang, Xiangrui Meng, Sirui Hong, Wenhao Li, Zihao Wang, Zekai Wang, Feng Yin, Junhua Zhao, et al. Exploring large language model based intelligent agents: Definitions, methods, and prospects. arXiv preprint arXiv:2401.03428, 2024.

[79] Zane Durante, Qiuyuan Huang, Naoki Wake, Ran Gong, Jae Sung Park, Bidipta Sarkar, Rohan Taori, Yusuke Noda, Demetri Terzopoulos, Yejin Choi, et al. Agent ai: Surveying the horizons of multimodal interaction. arXiv preprint arXiv:2401.03568, 2024.

[80] Yingqiang Ge, Yujie Ren, Wenyue Hua, Shuyuan Xu, Juntao Tan, and Yongfeng Zhang. Llm as os (llmao), agents as apps: Envisioning aios, agents and the aios-agent ecosystem. arXiv preprint arXiv:2312.03815, 2023.

[81] Ning Ding, Yujia Qin, Guang Yang, Fuchao Wei, Zonghan Yang, Yusheng Su, Shengding Hu, Yulin Chen, Chi-Min Chan, Weize Chen, et al. Delta tuning: A comprehensive study of parameter efficient methods for pre-trained language models. arXiv preprint arXiv:2203.06904, 2022.

[82] Andrew Zhao, Daniel Huang, Quentin Xu, Matthieu Lin, Yong-Jin Liu, and Gao Huang. Expel: Llm agents are experiential learners. arXiv preprint arXiv:2308.10144, 2023.

[83] Joon Sung Park, Joseph O’Brien, Carrie Jun Cai, Meredith Ringel Morris, Percy Liang, and Michael S Bernstein. Generative agents: Interactive simulacra of human behavior. In Proceedings ofthe 36th Annual ACM Symposium on User Interface Software and Technology, pages 1–22, 2023.

[84] Robert L Solso and Jerome Kagan. Cognitive psychology. Houghton Mifflin Harcourt P, 1979.

[85] Fergus IM Craik and Robert S Lockhart. Levels of processing: A framework for memory research. Journal ofverbal learning and verbal behavior, 11(6):671–684, 1972.

[86] Selma Leydesdorff. Memory cultures: Memory, subjectivity and recognition. Routledge, 2017.

[87] Philip Nicholas Johnson-Laird. Mental models: Towards a cognitive science of language, inference, and consciousness. Number 6. Harvard University Press, 1983.

[88] John E Laird. The Soar cognitive architecture. MIT press, 2019.

[89] Ron Sun. Duality of the mind: A bottom-up approach toward cognition. Psychology Press, 2001.

[90] Richard S Sutton and Andrew G Barto. Reinforcement learning: An introduction. MIT press, 2018.

[91] Longtao Zheng, Rundong Wang, Xinrun Wang, and Bo An. Synapse: Trajectory-as-exemplar prompting with memory for computer control. In NeurIPS 2023 Foundation Models for Decision Making Workshop, 2023.

[92] Ali Montazeralghaem, Hamed Zamani, and James Allan. A reinforcement learning framework for relevance feedback. In Proceedings of the 43rd international acm sigir conference on research and development in information retrieval, pages 59–68, 2020.

[93] Xizhou Zhu, Yuntao Chen, Hao Tian, Chenxin Tao, Weijie Su, Chenyu Yang, Gao Huang, Bin Li, Lewei Lu, Xiaogang Wang, et al. Ghost in the minecraft: Generally capable agents for open-world enviroments via large language models with text-based knowledge and memory. arXiv preprint arXiv:2305.17144, 2023.

[94] Junru Lu, Siyu An, Mingbao Lin, Gabriele Pergola, Yulan He, Di Yin, Xing Sun, and Yunsheng Wu. Memochat: Tuning llms to use memos for consistent long-range open-domain conversation. arXiv preprint arXiv:2308.08239, 2023.

[95] Lei Wang, Jingsen Zhang, Hao Yang, Zhiyuan Chen, Jiakai Tang, Zeyu Zhang, Xu Chen, Yankai Lin, Ruihua Song, Wayne Xin Zhao, Jun Xu, Zhicheng Dou, Jun Wang, and Ji-Rong Wen. When large language model based agent meets user behavior analysis: A novel user simulation paradigm, 2023.

[96] Chenxu Hu, Jie Fu, Chenzhuang Du, Simian Luo, Junbo Zhao, and Hang Zhao. Chatdb: Augmenting llms with databases as their symbolic memory. arXiv preprint arXiv:2306.03901, 2023.

[97] Lei Liu, Xiaoyan Yang, Yue Shen, Binbin Hu, Zhiqiang Zhang, Jinjie Gu, and Guannan Zhang. Think-in-memory: Recalling and post-thinking enable llms with long-term memory. arXiv preprint arXiv:2311.08719, 2023.

[98] Xinnian Liang, Bing Wang, Hui Huang, Shuangzhi Wu, Peihao Wu, Lu Lu, Zejun Ma, and Zhoujun Li. Unleashing infinite-length input capacity for large-scale language models with self-controlled memory system. arXiv preprint arXiv:2304.13343, 2023.

[99] Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and Anima Anandkumar. Voyager: An open-ended embodied agent with large language models. arXiv preprint arXiv:2305.16291, 2023.

[100] Charles Packer, Vivian Fang, Shishir G Patil, Kevin Lin, Sarah Wooders, and Joseph E Gonzalez. Memgpt: Towards llms as operating systems. arXiv preprint arXiv:2310.08560, 2023.

[101] Gibbeum Lee, Volker Hartmann, Jongho Park, Dimitris Papailiopoulos, and Kangwook Lee. Prompted llms as chatbot modules for long open-domain conversation. arXiv preprint arXiv:2305.04533, 2023.

[102] Yancheng Wang, Ziyan Jiang, Zheng Chen, Fan Yang, Yingxue Zhou, Eunah Cho, Xing Fan, Xiaojiang Huang, Yanbin Lu, and Yingzhen Yang. Recmind: Large language model powered agent for recommendation. arXiv preprint arXiv:2308.14296, 2023.

[103] Weiran Yao, Shelby Heinecke, Juan Carlos Niebles, Zhiwei Liu, Yihao Feng, Le Xue, Rithesh Murthy, Zeyuan Chen, Jianguo Zhang, Devansh Arpit, et al. Retroformer: Retrospective large language agents with policy gradient optimization. arXiv preprint arXiv:2308.02151, 2023.

[104] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. React: Synergizing reasoning and acting in language models. arXiv preprint arXiv:2210.03629, 2022.

[105] Yunfan Shao, Linyang Li, Junqi Dai, and Xipeng Qiu. Character-llm: A trainable agent for role-playing. arXiv preprint arXiv:2310.10158, 2023.

[106] Jihoon Tack, Jaehyung Kim, Eric Mitchell, Jinwoo Shin, Yee Whye Teh, and Jonathan Richard Schwarz. Online adaptation of language models with a memory of amortized contexts. arXiv preprint arXiv:2403.04317, 2024.

[107] Haochun Wang, Chi Liu, Nuwa Xi, Zewen Qiang, Sendong Zhao, Bing Qin, and Ting Liu. Huatuo: Tuning llama model with chinese medical knowledge. arXiv preprint arXiv:2304.06975, 2023.

[108] Xu Huang, Jianxun Lian, Yuxuan Lei, Jing Yao, Defu Lian, and Xing Xie. Recommender ai agent: Integrating large language models for interactive recommendations. arXiv preprint arXiv:2308.16505, 2023.

[109] Yuan Li, Yixuan Zhang, and Lichao Sun. Metaagents: Simulating interactions of human behaviors for llm-based task-oriented coordination via collaborative generative agents. arXiv preprint arXiv:2310.06500, 2023.

[110] Jingqing Ruan, Yihong Chen, Bin Zhang, Zhiwei Xu, Tianpeng Bao, Guoqing Du, Shiwei Shi, Hangyu Mao, Xingyu Zeng, and Rui Zhao. Tptu: Task planning and tool usage of large language model-based ai agents. arXiv preprint arXiv:2308.03427, 2023.

[111] Yilun Kong, Jingqing Ruan, Yihong Chen, Bin Zhang, Tianpeng Bao, Shiwei Shi, Guoqing Du, Xiaoru Hu, Hangyu Mao, Ziyue Li, et al. Tptu-v2: Boosting task planning and tool usage of large language model-based agents in real-world systems. arXiv preprint arXiv:2311.11315, 2023.

[112] Sirui Hong, Xiawu Zheng, Jonathan Chen, Yuheng Cheng, Jinlin Wang, Ceyao Zhang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, Liyang Zhou, et al. Metagpt: Meta programming for multi-agent collaborative framework. arXiv preprint arXiv:2308.00352, 2023.

[113] Yi Yang, Yixuan Tang, and Kar Yan Tam. Investlm: A large language model for investment using financial domain instruction tuning. arXiv preprint arXiv:2309.13064, 2023.

[114] Kechi Zhang, Jia Li, Ge Li, Xianjie Shi, and Zhi Jin. Codeagent: Enhancing code generation with tool-integrated agent systems for real-world repo-level coding challenges. arXiv preprint arXiv:2401.07339, 2024.

[115] Li Yunxiang, Li Zihan, Zhang Kai, Dan Ruilong, and Zhang You. Chatdoctor: A medical chat model fine-tuned on llama model using medical domain knowledge. arXiv preprint arXiv:2303.14070, 2023.

[116] Dacheng Li, Rulin Shao, Anze Xie, Ying Sheng, Lianmin Zheng, Joseph Gonzalez, Ion Stoica, Xuezhe Ma, and Hao Zhang. How long can context length of open-source llms truly promise? In NeurIPS 2023 Workshop on Instruction Tuning and Instruction Following, 2023.

[117] Ziheng Huang, Sebastian Gutierrez, Hemanth Kamana, and Stephen MacNeil. Memory sandbox: Transparent and interactive memory management for conversational agents. In Adjunct Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology, pages 1–3, 2023.

[118] Arka Pal, Deep Karkhanis, Manley Roberts, Samuel Dooley, Arvind Sundararajan, and Siddartha Naidu. Giraffe: Adventures in expanding context lengths in llms. arXiv preprint arXiv:2308.10882, 2023.

[119] Szymon Tworkowski, Konrad Staniszewski, Mikołaj Pacek, Yuhuai Wu, Henryk Michalewski, and Piotr Miłos. Focused transformer: Contrastive training for context scaling, 2023.´

[120] Nelson F Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. Lost in the middle: How language models use long contexts. arXiv preprint arXiv:2307.03172, 2023.

[121] Peter J Denning. The locality principle. Communications of the ACM, 48(7):19–24, 2005.

[122] Hermann Ebbinghaus. Memory: A contribution to experimental psychology, trans. HA Ruger & CE Bussenius. Teachers College.[rWvH], 1885.

[123] Jaap MJ Murre and Joeri Dros. Replication and analysis of ebbinghaus’ forgetting curve. PloS one, 10(7):e0120644, 2015.

[124] Jeff Johnson, Matthijs Douze, and Hervé Jégou. Billion-scale similarity search with gpus. IEEE Transactions on Big Data, 7(3):535–547, 2019.

[125] Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Luke Zettle moyer, Nicola Cancedda, and Thomas Scialom. Toolformer: Language models can teach themselves to use tools. arXiv preprint arXiv:2302.04761, 2023.

[126] Yujia Qin, Shihao Liang, Yining Ye, Kunlun Zhu, Lan Yan, Yaxi Lu, Yankai Lin, Xin Cong, Xiangru Tang, Bill Qian, et al. Toolllm: Facilitating large language models to master 16000+ real-world apis. arXiv preprint arXiv:2307.16789, 2023.

[127] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, et al. Llama: Open and efficient foundation language models. arXiv preprint arXiv:2302.13971, 2023.

[128] Zhibin Gou, Zhihong Shao, Yeyun Gong, Yujiu Yang, Minlie Huang, Nan Duan, Weizhu Chen, et al. Tora: A tool-integrated reasoning agent for mathematical problem solving. arXiv preprint arXiv:2309.17452, 2023.

[129] Honglin Xiong, Sheng Wang, Yitao Zhu, Zihao Zhao, Yuxiao Liu, Qian Wang, and Dinggang Shen. Doctorglm: Fine-tuning your chinese doctor is not a herculean task. arXiv preprint arXiv:2304.01097, 2023.

[130] Aohan Zeng, Xiao Liu, Zhengxiao Du, Zihan Wang, Hanyu Lai, Ming Ding, Zhuoyi Yang, Yifan Xu, Wendi Zheng, Xiao Xia, et al. Glm-130b: An open bilingual pre-trained model. arXiv preprint arXiv:2210.02414, 2022.

[131] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. Lora: Low-rank adaptation of large language models. arXiv preprint arXiv:2106.09685, 2021.

[132] Zhengliang Liu, Aoxiao Zhong, Yiwei Li, Longtao Yang, Chao Ju, Zihao Wu, Chong Ma, Peng Shu, Cheng Chen, Sekeun Kim, et al. Radiology-gpt: A large language model for radiology. arXiv preprint arXiv:2306.08666, 2023.

[133] Nicola De Cao, Wilker Aziz, and Ivan Titov. Editing factual knowledge in language models. arXiv preprint arXiv:2104.08164, 2021.

[134] Eric Mitchell, Charles Lin, Antoine Bosselut, Chelsea Finn, and Christopher D Manning. Fast model editing at scale. arXiv preprint arXiv:2110.11309, 2021.

[135] Shengyu Mao, Ningyu Zhang, Xiaohan Wang, Mengru Wang, Yunzhi Yao, Yong Jiang, Pengjun Xie, Fei Huang, and Huajun Chen. Editing personality for large language models. 2023.

[136] Jun-Yu Ma, Jia-Chen Gu, Ningyu Zhang, and Zhen-Hua Ling. Neighboring perturbations of knowledge editing on large language models. arXiv preprint arXiv:2401.17623, 2024.

[137] Mengru Wang, Ningyu Zhang, Ziwen Xu, Zekun Xi, Shumin Deng, Yunzhi Yao, Qishen Zhang, Linyi Yang, Jindong Wang, and Huajun Chen. Detoxifying large language models via knowledge editing. arXiv preprint arXiv:2403.14472, 2024.

[138] Uri Shaham, Maor Ivgi, Avia Efrat, Jonathan Berant, and Omer Levy. Zeroscrolls: A zero-shot benchmark for long text understanding. arXiv preprint arXiv:2305.14196, 2023.

[139] Yushi Bai, Xin Lv, Jiajie Zhang, Hongchang Lyu, Jiankai Tang, Zhidian Huang, Zhengxiao Du, Xiao Liu, Aohan Zeng, Lei Hou, et al. Longbench: A bilingual, multitask benchmark for long context understanding. arXiv preprint arXiv:2308.14508, 2023.

[140] Dacheng Li, Rulin Shao, Anze Xie, Ying Sheng, Lianmin Zheng, Joseph Gonzalez, Ion Stoica, Xuezhe Ma, and Hao Zhang. How long can context length of open-source llms truly promise? In NeurIPS 2023 Workshop on Instruction Tuning and Instruction Following, 2023.

[141] Mohit Shridhar, Xingdi Yuan, Marc-Alexandre Côté, Yonatan Bisk, Adam Trischler, and Matthew Hausknecht. Alfworld: Aligning text and embodied environments for interactive learning. arXiv preprint arXiv:2010.03768, 2020.

[142] YunDa Tsai, Mingjie Liu, and Haoxing Ren. Rtlfixer: Automatically fixing rtl syntax errors with large language models. arXiv preprint arXiv:2311.16543, 2023.

[143] Cheng Li, Ziang Leng, Chenxi Yan, Junyi Shen, Hao Wang, Weishi Mi, Yaying Fei, Xiaoyang Feng, Song Yan, HaoSheng Wang, et al. Chatharuhi: Reviving anime character in reality via large language model. arXiv preprint arXiv:2308.09597, 2023.

[144] Dake Chen, Hanbin Wang, Yunhao Huo, Yuzhao Li, and Haoyang Zhang. Gamegpt: Multiagent collaborative framework for game development. arXiv preprint arXiv:2310.08067, 2023.

[145] Zekun Moore Wang, Zhongyuan Peng, Haoran Que, Jiaheng Liu, Wangchunshu Zhou, Yuhan Wu, Hongcheng Guo, Ruitong Gan, Zehao Ni, Man Zhang, et al. Rolellm: Benchmarking, eliciting, and enhancing role-playing abilities of large language models. arXiv preprint arXiv:2310.00746, 2023.

[146] Runcong Zhao, Wenjia Zhang, Jiazheng Li, Lixing Zhu, Yanran Li, Yulan He, and Lin Gui. Narrativeplay: Interactive narrative understanding. arXiv preprint arXiv:2310.01459, 2023.

[147] Jinfeng Zhou, Zhuang Chen, Dazhen Wan, Bosi Wen, Yi Song, Jifan Yu, Yongkang Huang, Libiao Peng, Jiaming Yang, Xiyao Xiao, et al. Characterglm: Customizing chinese conversational ai characters with large language models. arXiv preprint arXiv:2311.16832, 2023.

[148] Zhao Kaiya, Michelangelo Naim, Jovana Kondic, Manuel Cortes, Jiaxin Ge, Shuying Luo, Guangyu Robert Yang, and Andrew Ahn. Lyfe agents: Generative agents for low-cost real-time social interactions. arXiv preprint arXiv:2310.02172, 2023.

[149] Junjie Zhang, Yupeng Hou, Ruobing Xie, Wenqi Sun, Julian McAuley, Wayne Xin Zhao, Leyu Lin, and Ji-Rong Wen. Agentcf: Collaborative learning with autonomous language agents for recommender systems. arXiv preprint arXiv:2310.09233, 2023.

[150] Wenyue Hua, Lizhou Fan, Lingyao Li, Kai Mei, Jianchao Ji, Yingqiang Ge, Libby Hemphill, and Yongfeng Zhang. War and peace (waragent): Large language model-based multi-agent simulation of world wars. arXiv preprint arXiv:2311.17227, 2023.

[151] Haochun Wang, Sendong Zhao, Zewen Qiang, Zijian Li, Nuwa Xi, Yanrui Du, MuZhen Cai, Haoqiang Guo, Yuhan Chen, Haoming Xu, et al. Knowledge-tuning large language models with structured medical knowledge bases for reliable response generation in chinese. arXiv preprint arXiv:2309.04175, 2023.

[152] Wenqi Shi, Ran Xu, Yuchen Zhuang, Yue Yu, Jieyu Zhang, Hang Wu, Yuanda Zhu, Joyce Ho, Carl Yang, and May D Wang. Ehragent: Code empowers large language models for complex tabular reasoning on electronic health records. arXiv preprint arXiv:2401.07128, 2024.

[153] Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Shaokun Zhang, Erkang Zhu, Beibin Li, Li Jiang, Xiaoyun Zhang, and Chi Wang. Autogen: Enabling next-gen llm applications via multi-agent conversation framework. arXiv preprint arXiv:2308.08155, 2023.

[154] Yang Li, Yangyang Yu, Haohang Li, Zhi Chen, and Khaldoun Khashanah. Tradinggpt: Multi agent system with layered memory and distinct characters for enhanced financial trading performance. arXiv preprint arXiv:2309.03736, 2023.

[155] Saizhuo Wang, Hang Yuan, Lionel M Ni, and Jian Guo. Quantagent: Seeking holy grail in trading by self-improving large language model. arXiv preprint arXiv:2402.03755, 2024.

[156] Yangyang Yu, Haohang Li, Zhi Chen, Yuechen Jiang, Yang Li, Denghui Zhang, Rong Liu, Jordan W Suchow, and Khaldoun Khashanah. Finmem: A performance-enhanced llm trading agent with layered memory and character design. arXiv e-prints, pages arXiv–2311, 2023.

[157] Kelvin JL Koa, Yunshan Ma, Ritchie Ng, and Tat-Seng Chua. Learning to generate explainable stock predictions using self-reflective large language models. arXiv preprint arXiv:2402.03659, 2024.

[158] Kexin Chen, Junyou Li, Kunyi Wang, Yuyang Du, Jiahui Yu, Jiamin Lu, Lanqing Li, Jiezhong Qiu, Jianzhang Pan, Yi Huang, Qun Fang, Pheng Ann Heng, and Guangyong Chen. Chemist-x: Large language model-empowered agent for reaction condition recommendation in chemical synthesis, 2024.

[159] Zihao Wang, Shaofei Cai, Anji Liu, Yonggang Jin, Jinbing Hou, Bowei Zhang, Haowei Lin, Zhaofeng He, Zilong Zheng, Yaodong Yang, et al. Jarvis-1: Open-world multi-task agents with memory-augmented multimodal language models. arXiv preprint arXiv:2311.05997, 2023.

[160] Zihan Zhao, Da Ma, Lu Chen, Liangtai Sun, Zihao Li, Hongshen Xu, Zichen Zhu, Su Zhu, Shuai Fan, Guodong Shen, et al. Chemdfm: Dialogue foundation model for chemistry. arXiv preprint arXiv:2401.14818, 2024.

[161] Ming Yan, Ruihao Li, Hao Zhang, Hao Wang, Zhilan Yang, and Ji Yan. Larp: Language-agent role play for open-world games. arXiv preprint arXiv:2312.17653, 2023.

[162] Zi-Yi Chen, Fan-Kai Xie, Meng Wan, Yang Yuan, Miao Liu, Zong-Guo Wang, Sheng Meng, and Yan-Gang Wang. Matchat: A large language model and application service platform for materials science. Chinese Physics B, 32(11):118104, 2023.

[163] Nian Li, Chen Gao, Yong Li, and Qingmin Liao. Large language model-empowered agents for simulating macroeconomic activities. arXiv preprint arXiv:2310.10436, 2023.

[164] Haojie Pan, Zepeng Zhai, Hao Yuan, Yaojia Lv, Ruiji Fu, Ming Liu, Zhongyuan Wang, and Bing Qin. Kwaiagents: Generalized information-seeking agent system with large language models. arXiv preprint arXiv:2312.04889, 2023.

[165] Odma Byambasuren, Yunfei Yang, Zhifang Sui, Damai Dai, Baobao Chang, Sujian Li, and Hongying Zan. Preliminary study on the construction of chinese medical knowledge graph. Journal ofChinese Information Processing, 33(10):1–9, 2019.

[166] Zefan Wang, Zichuan Liu, Yingying Zhang, Aoxiao Zhong, Lunting Fan, Lingfei Wu, and Qingsong Wen. Rcagent: Cloud root cause analysis by autonomous agents with tool-augmented large language models. arXiv preprint arXiv:2310.16340, 2023.

[167] Zhangcheng Qiang, Weiqing Wang, and Kerry Taylor. Agent-om: Leveraging large language models for ontology matching. arXiv preprint arXiv:2312.00326, 2023.

[168] Licheng Wen, Daocheng Fu, Xin Li, Xinyu Cai, Tao Ma, Pinlong Cai, Min Dou, Botian Shi, Liang He, and Yu Qiao. Dilu: A knowledge-driven approach to autonomous driving with large language models. arXiv preprint arXiv:2309.16292, 2023.

[169] Zhitao Wang, Wei Wang, Zirao Li, Long Wang, Can Yi, Xinjie Xu, Luyang Cao, Hanjing Su, Shouzhi Chen, and Jun Zhou. Xuat-copilot: Multi-agent collaborative system for automated user acceptance testing with large language model. arXiv preprint arXiv:2401.02705, 2024.

[170] Yongchao Chen, Jacob Arkin, Yang Zhang, Nicholas Roy, and Chuchu Fan. Scalable multirobot collaboration with large language models: Centralized or decentralized systems? arXiv preprint arXiv:2309.15943, 2023.

[171] Zhao Mandi, Shreeya Jain, and Shuran Song. Roco: Dialectic multi-robot collaboration with large language models. arXiv preprint arXiv:2307.04738, 2023.

[172] Jonathan Light, Min Cai, Sheng Shen, and Ziniu Hu. From text to tactic: Evaluating llms playing the game of avalon. arXiv preprint arXiv:2310.05036, 2023.

[173] Bing Liu. Lifelong machine learning: a paradigm for continuous learning. Frontiers of Computer Science, 11:359–361, 2017.

[174] Gati V Aher, Rosa I Arriaga, and Adam Tauman Kalai. Using large language models to simulate multiple humans and replicate human subject studies. In International Conference on Machine Learning, pages 337–371. PMLR, 2023.
