---
stem: arxiv-2512.13564.Survey.Age of Agent Memory
id: arxiv-2512.13564
keywords: [memory, agent, survey, rag]
abstract: "Memory 已经成为、并将继续作为 foundation model 驱动的 agent 的核心能力。它支撑 long-horizon reasoning、continual adaptation，以及与复杂环境的有效交互。随着 agent memory 研究迅速扩展并吸引前所未有的关注，这一领域也日益碎片化。归入 agent memory 这一伞形概念之下的既有工作，在动机、实现、假设与评测协议上往往差异巨大；而定义松散的 memory 术语不断增殖，进一步遮蔽了概念清晰性。长/短期 memory 等传统分类法已被证明不足以刻画当代 agent memory 系统的多样性与动态性。本综述旨在给出当前 agent memory 研究的最新且全面的全景。我们首先明确界定 agent memory 的范围，并将其与 LLM memory、RAG 与 context engineering 等相关概念区分开来。随后，我们从 forms、functions 与 dynamics 这三个统一视角考察 agent memory。从 forms 的视角，我们识别 agent memory 的三种主导实现，即 token-level、parametric 与 latent memory。从 functions 的视角，我们不再停留于粗粒度的时序分类，而提出更细粒度的分类法，依据其在知识保持、能力累积与任务级 reasoning 中的作用区分 factual、experiential 与 working memory。从 dynamics 的视角，我们分析 memory 在 agent 与环境交互过程中如何随时间形成、演化与 retrieval。为支撑实证研究与工程实践，我们汇总代表性 benchmark 与开源 memory framework 的全面概览。除整合之外，我们还就若干新兴研究前沿提出前瞻性观点，包括面向自动化的 memory 设计、reinforcement learning 与 memory 系统的深度集成、multimodal memory、multi-agent 系统中的 shared memory，以及 trustworthiness 问题。我们希望本综述不仅作为既有工作的参考，也成为重新思考 memory——将其视为未来 agentic intelligence 设计中的 first-class primitive——的概念基础。"
revised: 2026-01-13
source: "https://arxiv.org/abs/2512.13564"
parser: mineru-cloud 3.4.4
---

> 本文为 AI 译文，由 DeepSeek-V4.1-Flash 于 2026-11-02 翻译；源文件：arxiv-2512.13564.Survey.Age of Agent Memory.md。

# Memory in the Age of AI Agents: A Survey

Forms, Functions and Dynamics

Yuyang Hu<sup>†</sup>, Shichun Liu<sup>†</sup>, Yanwei Yue<sup>†</sup>, Guibin Zhang<sup>†ò</sup>, Boyang Liu, Fangyi Zhu, Jiahang Lin, Honglin Guo, Shihan Dou, Zhiheng Xi, Senjie Jin, Jiejun Tan, Yanbin Yin, Jiongnan Liu, Zeyu Zhang, Zhongxiang Sun, Yutao Zhu, Hao Sun, Boci Peng, Zhenrong Cheng, Xuanbo Fan, Jiaxin Guo, Xinlei Yu, Zhenhong Zhou, Zewen Hu, Jiahao Huo, Junhao Wang, Yuwei Niu, Yu Wang, Zhenfei Yin, Xiaobin Hu, Yue Liao, Qiankun Li, Kun Wang, Wangchunshu Zhou, Yixin Liu, Dawei Cheng, Qi Zhang, Tao Gui<sup>‡</sup>, Shirui Pan, Yan Zhang<sup>‡</sup>, Philip Torr, Zhicheng Dou<sup>‡</sup>, Ji-Rong Wen, Xuanjing Huang<sup>‡</sup>, Yu-Gang Jiang, Shuicheng Yan<sup>‡</sup>

<sup>†</sup>核心贡献者，按姓名字母顺序排列。ò 项目组织者。<sup>‡</sup>核心指导者。

所属机构：National University of Singapore, Renmin University of China, Fudan University, Peking University, Nanyang Technological University, Tongji University, University of California San Diego, Hong Kong University of Science and Technology (Guangzhou), Grifith University, Georgia Institute of Technology, OPPO, Oxford University

Memory 已经成为、并将继续作为 foundation model 驱动的 agent 的核心能力。它支撑 long-horizon reasoning、continual adaptation，以及与复杂环境的有效交互。随着 agent memory 研究迅速扩展并吸引前所未有的关注，这一领域也日益碎片化。归入 agent memory 这一伞形概念之下的既有工作，在动机、实现、假设与评测协议上往往差异巨大；而定义松散的 memory 术语不断增殖，进一步遮蔽了概念清晰性。长/短期 memory 等传统分类法已被证明不足以刻画当代 agent memory 系统的多样性与动态性。本综述旨在给出当前 agent memory 研究的最新且全面的全景。我们首先明确界定 agent memory 的范围，并将其与 LLM memory、RAG 与 context engineering 等相关概念区分开来。随后，我们从 forms、functions 与 dynamics 这三个统一视角考察 agent memory。从 forms 的视角，我们识别 agent memory 的三种主导实现，即 token-level、parametric 与 latent memory。从 functions 的视角，我们不再停留于粗粒度的时序分类，而提出更细粒度的分类法，依据其在知识保持、能力累积与任务级 reasoning 中的作用区分 factual、experiential 与 working memory。从 dynamics 的视角，我们分析 memory 在 agent 与环境交互过程中如何随时间形成、演化与 retrieval。为支撑实证研究与工程实践，我们汇总代表性 benchmark 与开源 memory framework 的全面概览。除整合之外，我们还就若干新兴研究前沿提出前瞻性观点，包括面向自动化的 memory 设计、reinforcement learning 与 memory 系统的深度集成、multimodal memory、multi-agent 系统中的 shared memory，以及 trustworthiness 问题。我们希望本综述不仅作为既有工作的参考，也成为重新思考 memory——将其视为未来 agentic intelligence 设计中的 first-class primitive——的概念基础。

\# 主要联系人：guibinz@u.nus.edu, yuyang.hu@ruc.edu.cn, liusc24@m.fudan.edu.cn, ywyue25@stu.pku.edu.cn Github：https://github.com/Shichun-Liu/Agent-Memory-Paper-List

## Contents

1 Introduction 4
2 Preliminaries: Formalizing Agents and Memory 6
2.1 LLM-based Agent Systems 6
2.2 Agent Memory Systems 7
2.3 Comparing Agent Memory with Other Key Concepts 8
2.3.1 Agent Memory vs. LLM Memory 9
2.3.2 Agent Memory vs. RAG 10
2.3.3 Agent Memory vs. Context Engineering 11
3 Form: What Carries Memory? 12
3.1 Token-level Memory 13
3.1.1 Flat Memory (1D) 15
3.1.2 Planar Memory (2D) 20
3.1.3 Hierarchical Memory (3D) 21
3.2 Parametric Memory 22
3.2.1 Internal Parametric Memory 22
3.2.2 External Parametric Memory 24
3.3 Latent Memory 26
3.3.1 Generate 26
3.3.2 Reuse 28
3.3.3 Transform 28
3.4 Adaptation 30
4 Functions: Why Agents Need Memory? 31
4.1 Factual Memory 32
4.1.1 User factual memory 35
4.1.2 Environment factual memory 36
4.2 Experiential Memory 37
4.2.1 Case-based Memory 39
4.2.2 Strategy-based Memory 40
4.2.3 Skill-based Memory 41
4.2.4 Hybrid memory 42
4.3 Working Memory 42
4.3.1 Single-turn Working Memory 43
4.3.2 Multi-turn Working Memory 45
5 Dynamics: How Memory Operates and Evolves? 46
5.1 Memory Formation 48
5.1.1 Semantic Summarization 48
5.1.2 Knowledge Distillation 50
5.1.3 Structured Construction 51
5.1.4 Latent Representation 53
5.1.5 Parametric Internalization 54
5.2 Memory Evolution 55
5.2.1 Consolidation 55
5.2.2 Updating 57
5.2.3 Forgetting 58
5.3 Memory Retrieval 59
5.3.1 Retrieval Timing and Intent 60
5.3.2 Query Construction 62
5.3.3 Retrieval Strategies 62
5.3.4 Post-Retrieval Processing 64

6 Resources and Frameworks 65   
6.1 Benchmarks and Datasets . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 65   
6.1.1 Benchmarks for Memory / Lifelong / Self-Evolving Agents 65   
6.1.2 Other Related Benchmarks 67   
6.2 Open-Source Frameworks 68   
7 Positions and Frontiers 69   
7.1 Memory Retrieval vs. Memory Generation 69   
7.1.1 Look Back: From Memory Retrieval to Memory Generation 69   
7.1.2 Future Perspective 69   
7.2 Automated Memory Management 70   
7.2.1 Look-Back: From Hand-crafted to Automatically Constructed Memory Systems. 70   
7.2.2 Future Perspective 70   
7.3 Reinforcement Learning Meets Agent Memory 71   
7.3.1 Look-Back: RL is Internalizing Memory Management Abilities for Agents. 71   
7.3.2 Future Perspective 72   
7.4 Multimodal Memory 72   
7.4.1 Look-Back 72   
7.4.2 Future Perspective 73   
7.5 Shared Memory in Multi-Agent Systems 73   
7.5.1 Look-Back: From Isolated Memories to Shared Cognitive Substrates 73   
7.5.2 Future Perspective 73   
7.6 Memory for World Model 74   
7.6.1 Look-Back 74   
7.6.2 Future Perspective 74   
7.7 Trustworthy Memory 75   
7.7.1 Look-Back: From Trustworthy RAG to Trustworthy Memory 75   
7.7.2 Future Perspective 75   
7.8 Human-Cognitive Connections 76   
7.8.1 Look Back 76   
7.8.2 Future Perspective 76

## 8 Conclusion

![](../assets/arxiv-2512.13564-fig1.jpg)  
Figure 1 按 forms（第 3 节）、functions（第 4 节）与 dynamics（第 5 节）的统一分类法组织的 agent memory 概览。该图按主导 form 与主要 function 对 memory 产物进行定位，并进一步将代表性系统映射到这一分类法之中，以提供整合后的全景。

## 1 Introduction

过去两年间，能力不断增强的 LLM 以前所未有的态势演化为强大的 AI agent（Matarazzo and Torlone, 2025; Minaee et al., 2025; Luo et al., 2025a）。这些以 foundation model 为动力的 agent 在深度研究（Xu and Peng, 2025; Zhang et al., 2025p）、软件工程（Wang et al., 2024i）与科学发现（Wei et al., 2025c）等多样化领域展现出显著进展，持续推动通向 artificial general intelligence（AGI）的进程（Fang et al., 2025a; Durante et al., 2024）。尽管早期对“agent”的构想高度异质，社区内部此后逐渐形成共识：除纯粹的 LLM backbone 之外，agent 通常还配备 reasoning、planning、perception、memory 与 tool use 等能力。其中 reasoning 与 tool use 等能力，已通过 reinforcement learning 在很大程度上内化到模型参数之中（Wang et al., 2025m; Qu et al., 2025b），而另一些能力仍高度依赖外部的 agentic scaffold。这些组件共同将 LLM 从静态的条件生成器转变为可学习的 policy，使其能够与多样化的外部环境交互并随时间自适应演化（Zhang et al., 2025f; Liu et al., 2025a）。

在这些 agent 能力之中，memory 尤为突出，堪称基石：它明确地使静态的 LLM——其参数无法被快速更新——转变为能够通过环境交互持续适应的自适应 agent（Zhang et al., 2025s; Wu et al., 2025g）。从应用角度看，众多领域要求 agent 主动管理 memory，而非表现出短暂、易忘的行为：个性化聊天机器人（Chhikara et al., 2025; Li et al., 2025b）、推荐系统（Liu et al., 2025c）、社会模拟（Park et al., 2023; Yang et al., 2025）以及金融调查（Zhang et al., 2024），都依赖 agent 处理、存储与管理历史信息的能力。从发展角度看，AGI 研究的一项根本诉求，是赋予 agent 通过环境交互持续演化的能力（Hendrycks et al., 2025），而这种能力从根本上

植根于 agent memory。

**agent memory 需要一种新的分类法** 鉴于 agent memory 系统日益增长的重要性与所受的社区关注，为当代 agent memory 研究提供一种更新的视角，既适时又必要。提出新分类法并撰写本综述的动机有二：❶ 既有分类法的局限：尽管近期若干综述已对 agent memory 给出了有价值且全面的概览（Zhang et al., 2025s; Wu et al., 2025g），其分类法是在此后一系列快速的方法进展之前形成的，因而未能充分反映当前研究图景的广度与复杂度。例如，2025 年出现的新兴方向——从过往经验中 distillation 可复用工具的 memory 框架（Qiu et al., 2025a,c; Zhao et al., 2025c），或 memory 增强的 test-time scaling 方法（Zhang et al., 2025g; Suzgun et al., 2025）——在早先的分类体系中仍代表性不足。❷ 概念碎片化：随着 memory 相关研究的爆炸式增长，这一概念本身日益扩张且碎片化。研究者常发现，声称研究“agent memory”的论文在实现、目标与基本假设上差异巨大。诸如 declarative memory、episodic memory、semantic memory、parametric memory 等术语的增殖，进一步遮蔽了概念清晰性，凸显出亟需一种能够统一这些新兴概念的连贯分类法。

因此，本文力图建立一个系统框架，以调和既有定义、衔接新兴趋势，并阐明 agent 系统中 memory 的基础原理。具体而言，本综述旨在回答以下关键问题：

## Key Questions

❶ agent memory 如何定义，它与 LLM memory、RAG 与 context engineering 等相关概念有何关系？

❷ Forms：agent memory 可以采取哪些架构形式或表示形式？

❸ Functions：agent 为何需要 memory，它承担哪些角色或目的？

❹ Dynamics：agent memory 如何随时间运作、适应与演化？

❺ 推进 agent memory 研究的前沿方向有哪些？

为回答问题 ❶，我们首先在第 2 节给出基于 LLM 的 agent 与 agent memory 系统的形式化定义，并详细比较 agent memory 与 LLM memory、RAG、context engineering 等相关概念。随后沿“forms—functions—dynamics”三角，给出 agent memory 的结构化概览。问题 ❷ 考察 memory 的架构形式，我们在第 3 节讨论，重点阐述三种主流实现：token-level、parametric 与 latent memory。问题 ❸ 关注 memory 的功能角色，在第 4 节处理，我们区分三类 memory：factual memory，记录 agent 与用户及环境交互中获得的知识；experiential memory，通过任务执行逐步增强 agent 的问题求解能力；working memory，在单个任务实例期间管理工作区信息。问题 ❹ 聚焦 agent memory 的生命周期与运作动态，我们按 memory 的形成、retrieval 与演化的顺序依次呈现。

在以“forms—functions—dynamics”为透镜考察既有研究之后，我们进一步给出对 agent memory 研究的观点与洞见。为便于知识共享与未来发展，我们首先在第 6 节汇总关键 benchmark 与 framework 资源。在此基础上，我们通过在第 7 节探讨若干新兴但尚未充分发展的研究前沿来回答问题 ❺，包括面向自动化的 memory 设计、reinforcement learning（RL）的集成、multimodal memory、multi-agent 系统的 shared memory 以及 trustworthiness 问题。

贡献 本综述的贡献可概括如下：(1) 我们从“forms—functions—dynamics”的视角，给出 agent memory 的最新且多维度的分类法，提供一个结构化透镜以理解该领域的当前发展。(2) 我们深入讨论不同 memory form 与 function 目的的适配性及其相互作用，给出关于如何将各类 memory 与不同 agent 目标有效对齐的洞见。(3) 我们考察 agent memory 中新兴且有前景的研究方向，从而勾勒未来机遇并指出推进路径。(4) 我们汇编全面的资源集合，包括 benchmark 与开源 framework，以支撑研究者与实践者进一步探索 agent memory 系统。

综述结构 本综述其余部分组织如下。第 2 节形式化基于 LLM 的 agent 与 agent memory 系统，并澄清它们与相关概念的关系。第 3 节、第 4 节与第 5 节分别考察 agent memory 的 forms、functions 与 dynamics。第 6 节汇总代表性 benchmark 与 framework 资源。第 7 节讨论新兴研究前沿与未来方向。最后，我们在第 8 节以关键洞见的总结收束全篇。

## 2 Preliminaries: Formalizing Agents and Memory

LLM agent 日益充当交互式系统的决策核心，这些系统随时间持续运行、操作外部工具，并与人类或其他 agent 协同。为研究此类情境中的 memory，我们首先以同时涵盖 single-agent 与 multi-agent 配置的方式，形式化基于 LLM 的 agent 系统。随后，我们形式化通过与 agent 决策过程以读/写交互耦合的 memory 系统，从而对任务之内（within-episode / short-term memory）与跨任务（cross-episode / long-term memory）出现的 memory 现象作统一处理。

## 2.1 LLM-based Agent Systems

**agent 与环境** 令 $\mathcal { I } = \{ 1 , \ldots , N \}$ 表示 agent 的索引集合，其中 $N = 1$ 对应 single-agent 情形（例如 ReAct），$N > 1$ 表示 multi-agent 设置，如辩论（Li et al., 2024c）或 planner–executor 架构（Wan et al., 2025）。环境由状态空间 S 刻画。在每个时间步 t，环境按受控随机转移模型演化

$$
s _ {t + 1} \sim \Psi (s _ {t + 1} \mid s _ {t}, a _ {t}),
$$

其中 $a _ { t }$ 表示在时间 t 执行的动作。在 multi-agent 系统中，这一抽象既允许顺序决策（每个时间步仅一个 agent 行动），也允许通过环境中介效应实现的隐式协调。每个 agent $i \in \mathcal { T }$ 接收一个观测

$$
o _ {t} ^ {i} = O _ {i} (s _ {t}, h _ {t} ^ {i}, \mathcal {Q}),
$$

其中 $h _ { t } ^ { i }$ 表示 agent i 可见的那部分交互历史。视系统设计而定，该历史可包含先前的消息、中间工具输出、部分 reasoning trace、shared workspace 状态或其他 agent 的贡献。Q 表示任务规范（task specification），例如用户指令、目标描述或外部约束；除非另有说明，任务之内将其视为固定不变。

**动作空间** 基于 LLM 的 agent 的一个显著特征是其动作空间的异质性。动作并不限于纯文本生成，agent 可以在 multimodal 且语义结构化的动作空间上操作，包括：

• 自然语言生成，例如产生中间 reasoning、解释、回复或指令（Li et al., 2023b; Wu et al., 2024b; Hong et al., 2024; Qian et al., 2024）。

• 工具调用动作，即调用外部 API、搜索引擎、计算器、数据库、模拟器或代码执行环境（Qin et al., 2025; Li et al., 2025h; Zhou et al., 2023c, 2024c）。

• planning 动作，即显式输出任务分解、执行计划或子目标规范，以指导后续行为（CAMEL-AI, 2025; Liu et al., 2025g; Pan et al., 2024）。

• 环境控制动作，即 agent 直接操纵外部环境（例如在具身设置中导航（Shridhar et al., 2021; Wang et al., 2022a）、编辑软件仓库（Jimenez et al., 2024; Aleithan et al., 2024），或修改 shared memory buffer）。

• 通信动作，即通过结构化消息与其他 agent 协作或协商（Marro et al., 2024）。

这些动作虽然在语义上多样，但都由同一个事实统一起来：它们经由以情境输入为条件的自回归 LLM backbone 产生。形式上，每个 agent i 遵循 policy

$$
a _ {t} = \pi_ {i} (o _ {t} ^ {i}, m _ {t} ^ {i}, \mathcal {Q}),
$$

其中 $m _ { t } ^ { i }$ 是第 2.2 节所定义的、由 memory 导出的信号。该 policy 可在输出可执行动作之前，在内部生成多步 reasoning chain、latent deliberation 或 scratchpad 计算；此类内部过程被抽象掉，不显式建模。

**交互过程与 trajectory** 系统的一次完整执行会诱导一条 trajectory

$$
\tau = (s _ {0}, o _ {0}, a _ {0}, s _ {1}, o _ {1}, a _ {1}, \ldots , s _ {T}),
$$

其中 T 由任务终止条件或系统特定的停止准则决定。在每一步，trajectory 反映了以下环节的交织：(i) 环境观测，(ii) 可选的 memory retrieval，(iii) 基于 LLM 的计算，以及 (iv) 驱动下一状态转移的动作执行。

这一形式化刻画了广泛的一类 agent 系统，从借助工具增强求解 reasoning 任务的单个 agent，到由角色专用 agent 组成的团队协同开发软件（Qian et al., 2024; Wang et al., 2025l）或开展科学探究（Weng et al., 2025）。接下来，我们形式化集成到这一 agent 循环中的 memory 系统。

## 2.2 Agent Memory Systems

当基于 LLM 的 agent 与环境交互时，其瞬时观测 $o _ { t } ^ { i }$ 往往不足以支撑有效决策。因此，agent 依赖从先前交互中导出的额外信息，这些信息既来自当前任务之内，也来自此前已完成的任务。我们通过一个统一的 agent memory 系统来形式化这一能力，该系统表示为不断演化的 memory state

$$
\mathcal {M} _ {t} \in \mathbb {M},
$$

其中 M 表示可容许 memory 配置的空间。不对 $\mathcal { M } _ { t }$ 施加特定的内部结构；它可以采取文本 buffer、键值 store、向量数据库、图结构或任意混合表示的形式。在任务开始时，$\mathcal { M } _ { t }$ 可能已包含从先前 trajectory 中 distillation 出的信息（cross-episode memory）。在任务执行期间，新信息不断累积，并充当短期的、任务特定的 memory。两种角色都由同一个 memory 容器支持，其时序区分源自使用模式，而非架构上的分离。

**memory 生命周期：formation、evolution 与 retrieval** memory 系统的动态由三个概念性算子刻画。

**memory formation** 在时间步 t，agent 产生信息性产物 $\phi _ { t }$，其中可包含工具输出、reasoning trace、部分计划、自我评估或环境反馈。一个 formation 算子

$$
\mathcal {M} _ {t + 1} ^ {\mathrm{form}} = F (\mathcal {M} _ {t}, \phi_ {t})
$$

有选择地将这些产物转化为 memory 候选，提取具有潜在未来用途的信息，而非逐字存储整个交互历史。

**memory evolution** 形成的 memory 候选通过一个 evolution 算子被整合进既有 memory bank

$$
\mathcal {M} _ {t + 1} = E (\mathcal {M} _ {t + 1} ^ {\mathrm{form}}),
$$

该算子可合并冗余条目（Zhao et al., 2024）、消解冲突（Rasmussen et al., 2025; Li et al., 2025l）、丢弃低价值信息（Wang et al., 2025r），或为高效 retrieval 而重构 memory。由此得到的 memory state 会在后续决策步骤与任务之间持续存在。

**memory retrieval** 在选择动作时，agent i retrieval 一个依赖情境的 memory 信号

$$
m _ {t} ^ {i} = R (\mathcal {M} _ {t}, o _ {t} ^ {i}, \mathcal {Q}),
$$

其中 R 表示 retrieval 算子，它构造一个任务感知的查询并返回相关 memory 内容。retrieval 到的信号 $m _ { t } ^ { i }$ 被格式化为可由 LLM policy 直接消费的形式，例如一系列文本片段或结构化摘要。

**agent 循环中的时序角色** 尽管 memory 被表示为统一状态 $\mathcal { M } _ { t }$，三个生命周期算子（formation $F$、evolution E 与 retrieval $R$）并不需要在每个时间步都被调用。相反，不同的 memory 效应源自不同的时序调用模式。例如，某些系统仅在任务初始化时执行一次 retrieval，

$$
m _ {t} ^ {i} = \left\{ \begin{array}{l l} R (\mathcal {M} _ {0}, o _ {0} ^ {i}, \mathcal {Q}), & t = 0, \\ \bot , & t > 0, \end{array} \right.
$$

其中 ⊥ 表示空 retrieval 策略。另一些系统则可能基于情境触发条件间歇或持续地 retrieval memory。类似地，memory formation 既可以是原始观测的最小累积，

$$
\mathcal {M} _ {t + 1} ^ {\mathrm{form}} = \mathcal {M} _ {t} \cup \{o _ {t} ^ {i} \},
$$

也可以是可复用模式或抽象的高级抽取与精炼。因此，在任务之内，short-term memory 效应可能来自轻量级日志记录，正如 Yao et al. (2023b); Chen et al. (2023a) 所做，也可能来自更精细的迭代精炼（Hu et al., 2025a）；在跨任务层面，long-term memory 可以在任务边界处按 episode 更新，也可以在运行过程中持续更新。由此可见，short-term 与 long-term memory 现象并非源自离散的架构模块，而是源自 formation、evolution 与 retrieval 被启用时所呈现的时序模式。

**memory–agent 耦合** memory 与 agent 决策过程之间的交互同样灵活。一般而言，agent policy 写作

$$
a _ {t} = \pi_ {i} (o _ {t} ^ {i}, m _ {t} ^ {i}, \mathcal {Q}),
$$

其中 retrieval 到的 memory 信号 $m _ { t } ^ { i }$ 是否存在取决于 retrieval 调度。当某一步禁用 retrieval 时，$m _ { t } ^ { i }$ 可视为一个被特别标记的空输入。

因此，整体 agent 循环由以下环节构成：观测环境，可选地 retrieval memory，计算动作，接收反馈，并可选地通过 formation 与 evolution 更新 memory。不同的 agent 实现会以不同的时间频率实例化这些操作的不同子集，从而产生从被动 buffer 到主动演化知识库的各种 memory 系统。

## 2.3 Comparing Agent Memory with Other Key Concepts

尽管人们对具备 memory 的 agent 系统兴趣日增，社区对“什么构成 agent memory”的理解仍支离破碎。在实践中，研究者与从业者常将 agent memory 与 LLM memory（Wu et al., 2025g）、RAG（Gao et al., 2024）与 context engineering（Mei et al., 2025）等相关构念混为一谈。尽管这些概念因都涉及 LLM 驱动系统中信息如何被管理与利用而内在地相互关联，但它们在范围、时序特征与功能角色上各有不同。

这些相互重叠却有区别的概念，导致文献与实践中的含混。为厘清这些区分并将 agent memory 置于这一更大的图景之中，我们在随后的小节中考察 agent memory 如何与 LLM memory、RAG 及 context engineering 相关联、又如何与之相区别。图 2 通过 Venn diagram 直观展示这些领域的共性与区别。
![](../assets/arxiv-2512.13564-fig2.jpg)  
图 2 agent memory 与 LLM memory、RAG 及 context engineering 的概念比较。该图展示了共享的技术实现（例如 KV 复用、图 retrieval），同时凸显根本区别：不同于 LLM memory 的架构优化、RAG 的静态知识访问或 context engineering 的瞬时资源管理，agent memory 的独特之处在于，它专注于维护一个持久且自演化的认知状态，该状态整合了事实知识与经验。所列类别与示例用于说明问题，并非严格平行，仅作为代表性参照点以澄清概念关系，而非定义一套僵化的分类法。

## 2.3.1 agent memory vs. LLM memory

在高层面上，agent memory 几乎完全涵盖了传统上所称的 LLM memory。自 2023 年以来，许多自称"LLM memory 机制"的工作（Zhong et al., 2024; Packer et al., 2023a; Wang et al., 2023b），按当代术语更恰当的理解，其实是 agent memory 的早期实例。这种重新解释源于"LLM agent"这一概念本身的历史含混。在 2023—2024 年间，社区尚无稳定或连贯的定义：某些情形下，提示 LLM 调用计算器便足以使系统被认定为 agent（Wu et al., 2024c）；另一些情形下，agent 性（agency）要求远为丰富的能力，如显式规划、工具使用、memory 与反思性推理（Ruan et al., 2023）。直到近期，才出现更统一、更有结构的定义（例如 Zhang et al. (2025f) 所讨论的：基于 LLM 的 agent = LLM + 推理 + 规划 + memory + 工具使用 + 自我改进 + 多轮交互 + 感知），但即便这一表述也并非普遍适用。在这一历史背景下，MemoryBank（Zhong et al., 2024）与 MemGPT（Packer et al., 2023a）等早期系统将其贡献表述为提供 LLM memory。然而它们从根本上处理的却是经典的 agent 挑战，例如使基于 LLM 的 session agent 能够追踪用户偏好、维护对话状态信息，并在多轮交互中积累经验。若按现代且更成熟的 agent 性理解，此类系统自然应归类为 agent memory 的实例。

话虽如此，这种涵盖关系并非绝对。另有一条研究路线确实关注 LLM 内部 memory：管理 Transformer 的 KV cache（key–value, KV cache）、设计长 context 处理机制，或修改模型架构（例如 RWKV（Peng et al., 2023）、Mamba（Gu and Dao, 2024; Lieber et al., 2024）、基于扩散（diffusion）的语言模型（Nie et al., 2025）），以便在序列长度增长时更好地保留信息。这些工作聚焦于模型内在动态，通常处理不需要 agent 行为的任务，因此应被视为超出 agent memory 的范围。

**重叠** 在我们的分类法中，历史上被称为"LLM memory"的大部分内容，对应 agent memory 的各种形式。少样本提示（few-shot prompting）（Prabhumoye et al., 2022; Ma et al., 2023a）等技术可视为 long-term memory 的一种形式：过往示例或 distillation 出的任务摘要作为可复用知识，通过 retrieval 或 context 注入被纳入。自我反思与迭代精炼方法（Madaan et al., 2023; Mousavi et al., 2023; Han et al., 2025c）自然对应短期的、试验内 memory，因为 agent 在同一任务内反复利用先前尝试的中间推理轨迹或结果。甚至 KV 压缩与 context window 管理（Yoon et al., 2024; Jiang et al., 2023），当用于在单个任务过程中保留显著信息时，也在 agent 意义上充当 short-term memory 机制。这些技术都支持 agent 在任务执行全过程累积、变换与复用信息的能力。

**区别** 相比之下，直接干预模型内部状态的 memory 机制——例如为获得更长有效 context 而作的架构修改、缓存重写策略、循环状态持久化、attention sparsification 机制，或外置 KV 存储扩展——更宜归类为 LLM memory 而非 agent memory。其目标是扩展或重组底层模型的表示能力，而非为决策 agent 提供一个不断演化的外部 memory 库。它们通常不支持跨任务持久化、环境驱动的适应或刻意的 memory 操作（例如形成、演化、retrieval），因此位于本综述所定义的 agent memory 运作范围之外。

## 2.3.2 agent memory vs. RAG

在概念层面，agent memory 与 RAG 存在大量重叠：两种系统都构建、组织并利用辅助信息库，以将 LLM/agent 的能力扩展到其原生 parametric knowledge 之外。例如，知识图谱与索引策略等结构化表示同时出现在两个社区的方法中；agentic RAG 的近期发展表明，自主 retrieval 机制可以以类似 agent memory 架构的方式与动态数据库交互（Singh et al., 2025）。事实上，许多 RAG 与 agent memory 系统所依赖的工程栈共享相同的构件，包括向量索引、语义搜索与 context 扩展模块。

尽管存在这些技术趋同，两种范式在历史上主要通过其应用情境而相互区分。经典 RAG 技术主要使 LLM 能够访问静态知识源，无论是扁平文档库、结构化知识库，还是为按需 retrieval 而在外部建立索引的大型语料（Zhang et al., 2025q; Han et al., 2025b）。这些系统旨在将生成锚定于最新事实、缓解幻觉，并提升知识密集型任务的准确性，但它们一般不维护关于过往交互的内部、演化中的 memory。相比之下，agent memory 系统在 agent 与环境的持续交互中被实例化，将 agent 自身动作与环境反馈所产生的新信息持续纳入一个持久的 memory 库（Wang et al., 2024m; Zhao et al., 2024; Sun et al., 2025e）。

在早期表述中，RAG 与 agent memory 的区分相对清晰：RAG 为单次任务调用从外部维护的知识中 retrieval，而 agent memory 在多轮、多任务交互中演化。然而，随着 retrieval 系统本身日益动态，这一边界已越来越模糊。例如，某些 retrieval 任务在迭代查询过程中持续更新相关 context（例如多跳问答设置中逐步加入相关 context）。有趣的是，HippoRAG/HippoRAG2（Gutierrez et al., 2024; Gutiérrez et al., 2025）等系统同时被 RAG 与 memory 两个社区解读为在解决 LLM 的 long-term memory 挑战。因此，更实用（尽管无法完全分离）的区分在于任务领域。RAG 主要应用于为单次推理任务补充大型外部来源 context，其典型代表是 HotpotQA（Yang et al., 2018）、2WikiMQA（Ho et al., 2020）与 MuSiQue（Trivedi et al., 2022）等经典多跳与知识密集型 benchmark。相比之下，agent memory 系统通常在需要持续多轮交互、时间依赖或环境驱动适应的设置中接受评测。代表性 benchmark 包括 LoCoMo（Maharana et al., 2024）与 LongMemEval（Wu et al., 2025a）等长 context 对话评测，GAIA（Mialon et al., 2023）、XBench（Chen et al., 2025c）与 BrowseComp（Wei et al., 2025b）等复杂问题求解与深度研究 benchmark，SWE-bench Verified（Jimenez et al., 2024）等以代码为中心的 agent 任务，以及 StreamBench（Wu et al., 2024a）等终身学习 benchmark。我们在第 6.1 节给出 memory 相关 benchmark 的全面汇总。

然而，即便这种基于领域的区分也包含大量灰色地带。许多自称 agent memory 系统的工作是在 HotpotQA（Wang et al., 2025g,p）等长文档问答任务下评测的；而许多被标为 RAG 系统的论文，实际上实现了某种 agent 式自我改进，随时间持续 distillation 并精炼知识或技能。因此，标题、方法论与实证评测常常模糊了两类范式之间的概念边界。为进一步澄清这些关系，以下三段借鉴（Me et al., 2025）中既有的 RAG 分类法：模块化 RAG（Modular RAG）、图 RAG（Graph RAG）与 agent 式 RAG（Agentic RAG），并考察各谱系的核心技术如何在 RAG 与 agent memory 系统中分别显现。

**模块化 RAG** 模块化 RAG 指将 retrieval 流水线分解为明确规定的组件（如索引、候选 retrieval、重排序、过滤与 context 组装）的架构，这些组件以基本静态、流水线式的方式运行（Singh et al., 2025）。此类系统将 retrieval 视为置于 LLM 之外、经过良好工程化的模块化子系统，主要设计用于在推理期间将相关知识注入模型的 context window。在 agent memory 视角下，相应技术通常出现在 retrieval 阶段，memory 访问通过向量搜索、语义相似度匹配或基于规则的过滤来实现，正如 Memary（Memary, 2025）、MemOS（Li et al., 2025l）与 Mem0（Chhikara et al., 2025）等流行的 agent memory 框架所示。

**图 RAG** 图 RAG 系统将知识库结构化为图，从知识图谱到概念图或文档—实体关系不等，并利用图遍历或基于图的排序算法 retrieval context（Peng et al., 2024）。这种表示支持多跳关系推理，已被证明对知识密集型任务有效（Edge et al., 2025; Han et al., 2025b; Dong et al., 2025a）。在 agent memory 的语境中，当 agent 随时间积累关系性洞见时——例如关联概念、追踪子任务间的依赖，或记录通过交互推断出的因果关系——图结构 memory 便自然出现。若干成熟实践包括 Mem0<sup>g</sup>（Chhikara et al., 2025）、A-MEM（Xu et al., 2025c）、Zep（Rasmussen et al., 2025）与 G-memory（Zhang et al., 2025c）。值得注意的是，基于图的 agent memory 系统可以在 agent 运行全程构建、扩展或重组其内部图。因此，基于图的 retrieval 构成两类范式的结构骨架，但只有 agent memory 将图视为经验的活的、演化中的表示。我们在第 3.1.2 节进一步分析基于图的 memory 形式，并请读者参阅相关综述（Liu et al., 2025h）。

**agent 式 RAG** agent 式 RAG 将 retrieval 整合进自主决策循环，由 LLM agent 主动控制何时 retrieval、如何 retrieval 与 retrieval 什么（Singh et al., 2025; Sun et al., 2025e）。此类系统常采用迭代查询、多步规划或自主搜索流程，使 agent 能够通过刻意推理精炼其信息需求，正如 PlanRAG（Lee et al., 2024b）与 Self-RAG（Asai et al., 2023）所实现的那样。关于 agent 式 RAG 的更详细理解，请读者参阅 Singh et al. (2025)。从 agent memory 视角看，agent 式 RAG 占据最接近的概念空间：两种系统都涉及与外部信息库的自主交互，都支持多步精炼，都可能将 retrieval 到的洞见纳入后续推理。关键区别在于，经典的 agent 式 RAG 通常在外部、且往往是任务特定的数据库上运作，而 agent memory 维护一个内部的、持久的、自演化的 memory 库，跨任务积累知识（Yan et al., 2025b; Xu et al., 2025c）。

## 2.3.3 agent memory vs. context engineering

agent memory 与 context engineering 之间的关系，最好理解为两种不同运作范式的交集，而非层级上的涵盖关系。context engineering 是一种系统化设计方法论，将 context window 视为受限的计算资源。它严格优化信息载荷（包括指令、知识、状态与 memory），以缓解海量输入容量与模型生成能力之间的不对称（Mei et al., 2025）。agent memory 关注的是一个具有演化身份的持久实体的认知建模，而 context engineering 则在资源管理范式下运作。从 context engineering 的视角看，agent memory 只是 context 组装函数中的一个变量，需要被高效调度以最大化推理效能。反过来，从 agent 的视角看，context engineering 是实现层，确保认知连续性保持在底层模型的物理极限之内。

**重叠** 两个领域在 long-horizon 交互中 working memory 的技术实现上高度趋同，且常采用功能上相同的机制来应对有限 context window 带来的约束（Hu et al., 2025a; Zhang et al., 2025r; Kang et al., 2025c; Yu et al., 2025a）。两类范式都依赖先进的信息压缩（Zhou et al., 2025b; Wu et al., 2025f）、组织（Xu et al., 2025c; Zhang et al., 2025c; Anokhin et al., 2024）与选择（Zhang et al., 2025r）技术，以在延长的交互序列中保持运作连续性。例如，作为 context engineering 框架核心的 token 剪枝与基于重要性的选择方法（Jiang et al., 2023; Li et al., 2023c），在 agent memory 系统中通过过滤噪声、保留显著信息而发挥基础性作用。类似地，滚动摘要（rolling summary）技术充当共享的基础原语，同时作为缓冲区管理策略与瞬时 episodic memory 机制发挥作用（Yu et al., 2025a; Lu et al., 2025b）。在实践中，对此类情境而言，工程化 context 与维护 agent short-term memory 之间的边界实际上已消融，因为两者都依赖相同的底层摘要、动态信息 retrieval 与递归状态更新（Tang et al., 2025b; Yoon et al., 2024）。

**区别** 当从短期文本处理转向长生命周期 agent 这一更广范围时，区别最为明显。context engineering 主要处理 LLM 与其运行环境之间交互接口的结构化组织，包括优化工具集成推理与选择流水线（Qin et al., 2024a; Schick et al., 2023; Jia and Li, 2025），以及标准化通信协议，如 MCP（Qiu et al., 2025c）。这些方法着眼于确保指令、工具调用与中间状态在 context window 约束下格式正确、调度高效且可执行。因此，context engineering 在资源分配与接口正确性的层面上运作，强调语法有效性与执行效率。

相比之下，agent memory 界定了远为宽广的认知范围。除瞬时 context 组装之外，它还包括事实知识的持久存储（Zhong et al., 2024）、经验痕迹的积累与演化（Zhao et al., 2024; Tang et al., 2025d; Zhang et al., 2025d），并在某些情形下包括将 memory 内化到模型参数之中（Wang et al., 2025o）。agent memory 管理的不是推理时信息如何呈现给模型，而是 agent 知道什么、经历过什么，以及这些要素如何随时间演化。这包括将重复交互 consolidation 为知识（Tan et al., 2025c）、从过往成败中抽象出程序性知识（Ouyang et al., 2025），以及跨任务与情节维持连贯身份（Wang et al., 2024f）。

从这个视角看，context engineering 构建的是使感知与行动在资源约束下得以发生的外部脚手架（scaffolding），而 agent memory 构成的是支撑学习、适应与自主性的内部基底（substrate）。前者优化 agent 与模型之间的瞬时接口，后者则维持超越任何单一 context window 的持久认知状态。

## 3 形式：什么承载 memory？

作为组织既有工作的起点，我们首先考察构建 agent memory 的最基本表示单元。我们首先尝试回答：agent memory 可以采取哪些架构形式或表示形式？

在多样化的 agent 系统中，memory 并非通过单一、统一的结构实现。相反，不同任务设置需要不同的存储形式，每种形式各有其结构性质。这些架构赋予 memory 不同的能力，塑造 agent 如何在交互中积累信息、如何保持行为一致性。它们最终使 memory 能够在各类任务场景中履行其预期角色。

依据 memory 存放于何处、以何种形式表示，我们将这些 memory 组织为三类：

## 三大 memory 形式

1. token 级 memory（第 3.1 节）：memory 被组织为显式、离散的单元，可被单独访问、修改与重建。这些单元在外部可见，并可随时间以结构化形式存储。

2. parametric memory（第 3.2 节）：memory 存储于模型参数之中，信息通过参数空间的统计模式进行编码，并前向计算过程中被隐式访问。

3. latent memory（第 3.3 节）：memory 表示于模型的内部隐藏状态、连续表示或演化中的 latent structure 之中。它可以在推理期间或跨交互周期持续存在并更新，捕获依赖情境的内部状态。

上述三种 memory 形式为理解"什么承载 memory"确立了核心结构框架。每种形式都以自己的方式组织、存储与更新信息，产生不同的表示模式与运作行为。有了这一结构分类法，我们便能更系统地考察 agent 为何需要 memory（第 4 节），以及 memory 如何在持续交互中演化、适应并塑造 agent 行为（第 5 节）。这一分类为后续讨论提供了概念基础。

## 3.1 token 级 memory

## token 级 memory 的定义

token 级 memory 将信息存储为持久的、离散的单元，这些单元可在外部访问与检视。这里的 token 是一个宽泛的表示概念：除文本 token 之外，它还包括视觉 token、音频帧——任何可被写入、retrieval、重组与修订的离散元素，且位于模型参数之外。

由于这些单元是显式的，token 级 memory 通常透明、易于编辑且便于解释，这使其成为 retrieval、路由、冲突处理以及与 parametric memory 和 latent memory 协调的自然层次。token 级 memory 也是最常见的 memory 形式，拥有最庞大的既有工作体量。

尽管所有 token 级 memory 都具有"以离散单元存储"这一性质，但它们在单元的组织方式上差异显著。存储 token 的结构组织，在决定 agent 搜索、更新或推理过往信息的效率方面起着核心作用。为描述这些差异，我们按单元间的结构组织对 token 级 memory 分类，从无显式拓扑到多层拓扑：

## token 级 memory 的三大类型

1. 扁平 memory（1D）：无显式的单元间拓扑。memory 作为单元的序列或集合累积（例如片段、轨迹、块）

2. 平面 memory（2D）：在单一平面内进行有结构但单层的组织：单元之间通过图、树、表等相互关联，没有跨层关系。结构是显式的，但不分层。

3. 层级 memory（3D）：跨多个层结构化并具有层间链接，形成体状或分层 memory

![](../assets/arxiv-2512.13564-fig3.jpg)

![](../assets/arxiv-2512.13564-fig4.jpg)

![](../assets/arxiv-2512.13564-fig5.jpg)

(a) 扁平 memory（1D）  
![](../assets/arxiv-2512.13564-fig6.jpg)  
(b) 平面 memory（2D）

![](../assets/arxiv-2512.13564-fig3-2.jpg)  
(c) 层级 memory（3D）  
图 3 按拓扑复杂度与维度组织的 token 级 memory 分类法：(a) 扁平 memory（1D）将信息存储为线性序列或独立簇，无显式的单元间拓扑，常用于块集合、对话日志与经验池。(b) 平面 memory（2D）引入单层结构化布局，单元通过树或图结构相连以捕获关系依赖，支持图像与聊天记录等多样节点类型。(c) 层级 memory（3D）采用多层形式，如金字塔或多层图，以促进垂直抽象以及不同数据粒度（如原始文档与合成问答）之间的跨层推理。

token 级 memory 的三种类型在图 3 中已有清晰展示。从无拓扑的扁平 memory，到具有单层结构组织的平面 memory，再到具有多层互联结构的层级 memory，这一组织谱系不仅决定了 token 级 memory 如何支持搜索、更新与推理，也决定了 memory 本身如何被结构化以及它能提供哪些能力。在随后的小节中，我们按优势与局限、典型用例与代表性工作介绍每种组织形式。代表性 token 级 memory 方法的总结与比较见表 1。

值得注意的是，沿着 ReAct（Yao et al., 2023b）所引入的思路，一系列研究开始关注 long-horizon 交互任务（Song et al., 2025a; Jin et al., 2025; Li et al., 2025h,e,j; Wu et al., 2025b）。其中许多任务引入了显式的 memory 概念，而由于 memory 通常以明文形式存储，它们属于 token 级 memory 的范围。它们大多强调如何压缩或折叠累积的交互轨迹，使 agent 能够在不超出 context 限制的情况下处理长序列（Zhou et al., 2025b; Zhang et al., 2025r; Wu et al., 2025f; Sun et al., 2025b; Li et al., 2025i; Chen et al., 2025b）。关于 working memory 的更详细讨论见第 4.3 节。

## 3.1.1 扁平 memory（1D）

## 扁平（1D）memory 的定义

扁平 memory 将信息存储为离散单元的累积，不显式建模它们之间的语义或关系依赖。这些单元可包括文本块、用户画像、经验轨迹、其对应的向量表示或 multimodal 条目。单元之间的关系不被直接编码在 memory 之中。

为便于清晰连贯的呈现，我们按主要设计目标与技术侧重对先前的扁平 memory 工作进行分组。此种分组服务于组织目的，并不意味着所得类别严格平行或互斥。在实践中，某些方法可能适用于多个类别，而一些涉及 multimodal 信息的方法，若 multimodal 并非其核心焦点，可能会在其他小节讨论。这样的组织使我们能够系统综述文献，同时在解释上保持灵活性。

表 1 代表性 token 级 memory 方法的比较。我们依据拓扑复杂度将既有工作分为三组：扁平 memory（1D）用于线性或独立记录，平面 memory（2D）用于结构化单层图/树，层级 memory（3D）用于多层架构。方法沿四个维度刻画：(1) Multi 表示 multimodal 能力，其中 ✔ 表示支持文本之外的模态（例如视觉），✗ 表示仅文本；(2) Type 标识 memory 的具体功能类别（例如 Fact 表示 factual memory，Exp 表示经验 memory，Work 表示 working memory）；(3) Memory Form 详述所存储单元的内容；(4) Task 列出主要应用领域。
<table><tr><td>Method</td><td>multimodal</td><td>Type</td><td>memory 形式</td><td>Task</td></tr><tr><td colspan="5">扁平 memory 模型</td></tr><tr><td>Reflexion (Shinn et al., 2023b)</td><td>✕</td><td>E&amp;W</td><td>轨迹作为 short-term memory，反馈作为 long-term memory</td><td>QA、推理、编程</td></tr><tr><td>Memento (Zhou et al., 2025a)</td><td>✕</td><td>Exp</td><td>轨迹案例（成功/失败）</td><td>推理</td></tr><tr><td>JARVIS-1 (Wang et al., 2025q)</td><td>✕</td><td>Exp</td><td>规划—环境配对</td><td>游戏</td></tr><tr><td>Expel (Zhao et al., 2024)</td><td>✕</td><td>Exp</td><td>洞见与少样本示例</td><td>推理</td></tr><tr><td>Buffer of Thoughts (Yang et al., 2024b)</td><td>✕</td><td>Exp</td><td>高层思维模板</td><td>游戏、推理、编程</td></tr><tr><td>SAGE (Liang et al., 2025)</td><td>✕</td><td>Exp</td><td>带 forgetting 机制的双存储</td><td>游戏、推理、编程</td></tr><tr><td>ChemAgent (Tang et al., 2025c)</td><td>✕</td><td>Exp</td><td>结构化子任务与原理</td><td>化学</td></tr><tr><td>AgentKB (Tang et al., 2025d)</td><td>✕</td><td>Exp</td><td>5 元组经验节点</td><td>编程、推理</td></tr><tr><td>H2R (Ye et al., 2025b)</td><td>✕</td><td>Exp</td><td>规划层与执行层</td><td>游戏、具身模拟</td></tr><tr><td>AWM (Wang et al., 2024m)</td><td>✕</td><td>Exp</td><td>抽象化的通用工作流</td><td>Web</td></tr><tr><td>PRINCIPLES (Kim et al., 2025a)</td><td>✕</td><td>Exp</td><td>自对弈产生的规则模板</td><td>情感陪伴</td></tr><tr><td>ReasoningBank (Ouyang et al., 2025)</td><td>✕</td><td>Exp</td><td>可迁移的推理策略条目</td><td>Web</td></tr><tr><td>Voyager (Wang et al., 2024b)</td><td>✕</td><td>Exp</td><td>可执行技能代码库</td><td>游戏</td></tr><tr><td>DGM (Zhang et al., 2025i)</td><td>✕</td><td>Exp</td><td>递归自修改代码库</td><td>编程</td></tr><tr><td>Memp (Fang et al., 2025d)</td><td>✕</td><td>Exp</td><td>指令与抽象脚本</td><td>具身模拟、旅行规划</td></tr><tr><td>UFO2 (Zhang et al., 2025a)</td><td>✕</td><td>Exp</td><td>系统文档与交互记录</td><td>Windows OS</td></tr><tr><td>LEGOMem (Han et al., 2025a)</td><td>✕</td><td>Exp</td><td>向量化任务轨迹</td><td>办公</td></tr><tr><td>ToolMem (Xiao et al., 2025b)</td><td>✕</td><td>Exp</td><td>工具能力</td><td>工具调用</td></tr><tr><td>SCM (Wang et al., 2025a)</td><td>✕</td><td>Fact</td><td>memory 流与向量数据库</td><td>长 context</td></tr><tr><td>MemoryBank (Zhong et al., 2024)</td><td>✕</td><td>Fact</td><td>历史与用户画像</td><td>情感陪伴</td></tr><tr><td>MPC (Lee et al., 2023)</td><td>✕</td><td>Fact</td><td>人格与摘要向量池</td><td>QA</td></tr><tr><td>RecMind (Wang et al., 2024h)</td><td>✕</td><td>Fact</td><td>用户元数据与外部知识</td><td>推荐</td></tr><tr><td>InteRecAgent (Huang et al., 2025d)</td><td>✕</td><td>Fact</td><td>用户画像与候选条目</td><td>推荐</td></tr><tr><td>Ego-LLaVA (Shen et al., 2024)</td><td>✕</td><td>Fact</td><td>语言编码的 chunk embedding</td><td>multimodal QA</td></tr><tr><td>ChatHaruhi (Li et al., 2023a)</td><td>✕</td><td>Fact</td><td>来自媒体的对话数据库</td><td>角色扮演</td></tr><tr><td>Memochat (Lu et al., 2023)</td><td>✕</td><td>Fact</td><td>备忘录与分类对话历史</td><td>长对话 QA</td></tr><tr><td>RecursiveSum (Wang et al., 2025h)</td><td>✕</td><td>Fact</td><td>短对话的递归摘要</td><td>长对话 QA</td></tr><tr><td>MemGPT (Packer et al., 2023a)</td><td>✕</td><td>Fact</td><td>虚拟内存（主 context/外部 context）</td><td>长对话 QA、文档 QA</td></tr><tr><td>Method</td><td>multimodal</td><td>Type</td><td>memory 结构</td><td>Task</td></tr><tr><td>RoleLLM (Wang et al., 2024d)</td><td>✕</td><td>Fact</td><td>角色特定问答对</td><td>角色扮演</td></tr><tr><td>Think-in-memory (Liu et al., 2023a)</td><td>✕</td><td>Fact</td><td>归纳性思考的哈希表</td><td>长对话 QA</td></tr><tr><td>PLA (Yuan et al., 2025b)</td><td>✕</td><td>Fact</td><td>历史与摘要的演化记录</td><td>QA、人类反馈</td></tr><tr><td>COMEDY (Chen et al., 2025d)</td><td>✕</td><td>Fact</td><td>单模型压缩 memory 格式</td><td>摘要、压缩、QA</td></tr><tr><td>Memoro (Zulfikar et al., 2024)</td><td>√</td><td>Fact</td><td>语音转文本 vector embedding</td><td>用户研究</td></tr><tr><td>Memory Sharing (Gao and Zhang, 2024a)</td><td>✕</td><td>Fact</td><td>查询—回复对 retrieval</td><td>文学创作、逻辑、计划生成</td></tr><tr><td>Conv Agent(Alonso et al., 2024)</td><td>✕</td><td>Fact</td><td>表链与向量条目</td><td>QA</td></tr><tr><td>EM-LLM (Fountas et al., 2025)</td><td>✕</td><td>Fact</td><td>带贝叶斯边界的情节事件</td><td>长 context</td></tr><tr><td>Memocrs (Xi et al., 2024a)</td><td>✕</td><td>Fact</td><td>用户元数据与知识</td><td>推荐</td></tr><tr><td>SECOM (Pan et al., 2025)</td><td>✕</td><td>Fact</td><td>段落级分块</td><td>长对话 QA</td></tr><tr><td>Mem0 (Chhikara et al., 2025)</td><td>✕</td><td>Fact</td><td>摘要与原始对话</td><td>长对话 QA</td></tr><tr><td>RMM (Tan et al., 2025c)</td><td>✕</td><td>Fact</td><td>反思组织的扁平条目</td><td>个性化</td></tr><tr><td>MEMENTO (Kwon et al., 2025)</td><td>√</td><td>Fact</td><td>交互历史条目</td><td>个性化</td></tr><tr><td>MemGuide (Du et al., 2025b)</td><td>✕</td><td>Fact</td><td>对话导出的问答对</td><td>长对话 QA</td></tr><tr><td>MIRIX (Wang and Chen, 2025)</td><td>√</td><td>Fact</td><td>六种优化的扁平 memory 类型</td><td>长对话 QA</td></tr><tr><td>SemanticAnchor (Chatterjee and Agarwal, 2025)</td><td>✕</td><td>Fact</td><td>句法 5 元组结构</td><td>长对话 QA</td></tr><tr><td>MMS (Zhang et al., 2025b)</td><td>✕</td><td>Fact</td><td>双 retrieval 与 context 单元</td><td>长对话 QA</td></tr><tr><td>Memory-R1 (Yan et al., 2025c)</td><td>✕</td><td>Fact</td><td>RL 管理的 mem0 架构</td><td>长对话 QA</td></tr><tr><td>ComoRAG (Wang et al., 2025f)</td><td>✕</td><td>Fact</td><td>事实/语义/情节单元与探针</td><td>叙事 QA</td></tr><tr><td>Nemori (Nan et al., 2025)</td><td>✕</td><td>Fact</td><td>预测校准存储</td><td>长对话 QA</td></tr><tr><td>Livia (Xi and Wang, 2025)</td><td>√</td><td>Fact</td><td>剪枝后的交互历史</td><td>情感陪伴</td></tr><tr><td>MOOM (Chen et al., 2025e)</td><td>✕</td><td>Fact</td><td>解耦的情节与角色存储</td><td>角色扮演</td></tr><tr><td>Mem-α (Wang et al., 2025p)</td><td>✕</td><td>Fact</td><td>核心、语义与 episodic memory</td><td>memory 管理</td></tr><tr><td>Personalized Long term Interaction (Westhäußer et al., 2025)</td><td>✕</td><td>Fact</td><td>层级历史与摘要</td><td>个性化</td></tr><tr><td>LightMem (Fang et al., 2025b)</td><td>✕</td><td>Fact</td><td>优化的长/短期存储</td><td>长对话 QA</td></tr><tr><td>MEXTRA (Wang et al., 2025b)</td><td>✕</td><td>Fact</td><td>抽取的原始对话数据</td><td>隐私攻击</td></tr><tr><td>MovieChat (Song et al., 2024)</td><td>√</td><td>Fact</td><td>短期特征与长期持久化</td><td>视频理解</td></tr><tr><td>MA-LMM (He et al., 2024)</td><td>√</td><td>Fact</td><td>视觉与查询 memory 库</td><td>视频理解</td></tr><tr><td>VideoAgent (Wang et al., 2024g)</td><td>√</td><td>Fact</td><td>时间文本描述与对象追踪</td><td>视频理解</td></tr><tr><td>Video-RAG (Luo et al., 2025b)</td><td>√</td><td>Fact</td><td>视觉对齐信息</td><td>视频理解</td></tr><tr><td>KARMA (Wang et al., 2025r)</td><td>√</td><td>Fact</td><td>3D 场景图与动态对象状态</td><td>具身任务</td></tr><tr><td>Embodied VideoAgent (Fan et al., 2025)</td><td>√</td><td>Fact</td><td>持久对象与传感器存储</td><td>multimodal</td></tr><tr><td>Mem2Ego (Zhang et al., 2025m)</td><td>√</td><td>Fact</td><td>地图、地标与访问地点存储</td><td>具身导航</td></tr><tr><td>Context-as-Memory (Yu et al., 2025b)</td><td>√</td><td>Fact</td><td>生成的 context 帧</td><td>视频生成</td></tr><tr><td>RCR-Router (Liu et al., 2025d)</td><td>✕</td><td>Fact</td><td>预算感知的语义子集</td><td>QA</td></tr><tr><td>ELL (Cai et al., 2025a)</td><td>✕</td><td>Fact</td><td>终身 memory 与技能</td><td>终身学习</td></tr><tr><td>MemRL (Zhang et al., 2026)</td><td>✕</td><td>Exp</td><td>用于 memory 管理的 RL</td><td>Web</td></tr><tr><td>ReMe (Cao et al., 2025b)</td><td>✕</td><td>Exp</td><td>步骤级经验与洞见</td><td>Web</td></tr><tr><td>MMAG (Zeppieri, 2025)</td><td>✕</td><td>Fact</td><td>五个交互 memory 层</td><td>用户研究</td></tr><tr><td>Hindsight (Latimer et al., 2025)</td><td>✕</td><td>Fact</td><td>保留、回忆与反思</td><td>长对话 QA</td></tr><tr><td>GAM (Yan et al., 2025a)</td><td>✕</td><td>Fact</td><td>简单 memory 但 retrieval 受引导</td><td>长对话 QA</td></tr><tr><td colspan="5">平面 memory 模型</td></tr><tr><td>D-SMART (Lei et al., 2025)</td><td>✕</td><td>Fact</td><td>带推理树的结构化 memory</td><td>长对话 QA</td></tr><tr><td>Reflexion (Shinn et al., 2023b)</td><td>✕</td><td>Work</td><td>来自经验的反思文本缓冲区</td><td>QA、推理、编程</td></tr><tr><td colspan="4"></td><td>下页续</td></tr><tr><td>PREMem (Kim et al., 2025b)</td><td>✕</td><td>Fact</td><td>动态 cross-session 链接三元组</td><td>长对话 QA</td></tr><tr><td>Query Reconstruct (Xu et al., 2025b)</td><td>✕</td><td>Exp</td><td>由知识库构建的逻辑图</td><td>知识图谱 QA</td></tr><tr><td>KGT (Sun et al., 2024)</td><td>✕</td><td>Fact</td><td>来自查询与反馈的知识图谱节点</td><td>QA</td></tr><tr><td>Optimus-1 (Li et al., 2024d)</td><td>✓</td><td>F&amp;E</td><td>知识图谱与经验池</td><td>游戏</td></tr><tr><td>SALI (Pan et al., 2024)</td><td>✓</td><td>Exp</td><td>带空间节点的拓扑图</td><td>导航</td></tr><tr><td>HAT (A et al., 2024)</td><td>✕</td><td>Fact</td><td>层级聚合树</td><td>长对话 QA</td></tr><tr><td>MemTree (Rezazadeh et al., 2025c)</td><td>✕</td><td>Fact</td><td>动态层级对话树</td><td>长对话 QA</td></tr><tr><td>TeaFarm (iunn Ong et al., 2025)</td><td>✕</td><td>Fact</td><td>连接 memory 的因果边</td><td>长对话 QA</td></tr><tr><td>COMET (Kim et al., 2024b)</td><td>✕</td><td>Fact</td><td>通过图实现的情境感知 memory</td><td>长对话 QA</td></tr><tr><td>Intrinsic Memory (Yuen et al., 2025)</td><td>✕</td><td>Fact</td><td>私有内部 memory 与共享外部 memory</td><td>规划</td></tr><tr><td>A-MEM (Xu et al., 2025c)</td><td>✕</td><td>Fact</td><td>基于卡片的连接 memory</td><td>长对话 QA</td></tr><tr><td>Ret-LLM (Modarressi et al., 2023)</td><td>✕</td><td>Fact</td><td>三元组表与 LSH 向量</td><td>QA</td></tr><tr><td>HuaTuo (Wang et al., 2023a)</td><td>✕</td><td>Fact</td><td>医学知识图谱</td><td>医学 QA</td></tr><tr><td>M3-Agent (Long et al., 2025)</td><td>✓</td><td>Fact</td><td>图结构中的 multimodal 节点</td><td>具身 QA</td></tr><tr><td>EMem (Zhou and Han, 2025a)</td><td>✕</td><td>Fact</td><td>以事件为中心、带 pagerank 的替代方案</td><td>长对话 QA</td></tr><tr><td>WorldMM (Yeo et al., 2025)</td><td>✓</td><td>Fact</td><td>多个互补 memory</td><td>视频理解</td></tr><tr><td>Memoria (Sarin et al., 2025)</td><td>✕</td><td>Fact</td><td>知识图谱画像与摘要</td><td>长对话 QA</td></tr><tr><td>LingoEDU (Zhou et al., 2026)</td><td>✕</td><td>Fact</td><td>基本话语单元的关系树</td><td>长对话 QA</td></tr><tr><td colspan="5">层级 memory 模型</td></tr><tr><td>GraphRAG (Edge et al., 2025)</td><td>✕</td><td>Fact</td><td>多层社区图索引</td><td>QA、摘要</td></tr><tr><td>H-Mem (Sun and Zeng, 2025)</td><td>✕</td><td>Fact</td><td>解耦的索引层与内容层</td><td>长对话 QA</td></tr><tr><td>EMG-RAG (Wang et al., 2024l)</td><td>✕</td><td>Fact</td><td>三层 memory 图</td><td>QA</td></tr><tr><td>G-Memory (Zhang et al., 2025c)</td><td>✕</td><td>Exp</td><td>以查询为中心的三层图结构</td><td>QA、游戏、具身任务</td></tr><tr><td>Zep (Rasmussen et al., 2025)</td><td>✕</td><td>Fact</td><td>时间知识图谱</td><td>长对话 QA</td></tr><tr><td>SGMem (Wu et al., 2025h)</td><td>✕</td><td>Fact</td><td>块图与句图</td><td>长对话 QA</td></tr><tr><td>HippoRAG (Gutierrez et al., 2024)</td><td>✕</td><td>Fact</td><td>带查询节点的知识</td><td>QA</td></tr><tr><td>HippoRAG 2 (Gutiérrez et al., 2025)</td><td>✕</td><td>Fact</td><td>带短语与段落的 KG</td><td>QA</td></tr>
<tr><td>AriGraph (Anokhin et al., 2024)</td><td>✕</td><td>Fact</td><td>语义与 episodic memory 图</td><td>游戏</td></tr><tr><td>Lyfe Agents (Kaiya et al., 2023)</td><td>✕</td><td>Fact</td><td>工作、短期与长期层</td><td>社会模拟</td></tr><tr><td>CAM (Li et al., 2025g)</td><td>✕</td><td>Fact</td><td>带主题的多层图</td><td>文档 QA</td></tr><tr><td>HiAgent (Hu et al., 2025a)</td><td>✕</td><td>E&amp;W</td><td>带递归聚类的目标图</td><td>agent 任务</td></tr><tr><td>ILM-TR (Tang et al., 2024)</td><td>✕</td><td>Fact</td><td>层级 memory 树</td><td>长 context</td></tr><tr><td>CompassMem (Hu et al., 2026b)</td><td>✕</td><td>Fact</td><td>以事件为中心的层级 memory</td><td>QA</td></tr><tr><td>MAGMA (Jiang et al., 2026)</td><td>✕</td><td>Fact</td><td>语义、时间、因果、实体图</td><td>长对话 QA</td></tr><tr><td>EverMemOS (Hu et al., 2026a)</td><td>✕</td><td>Fact</td><td>覆盖多类型的可复用 memory</td><td>长对话 QA</td></tr><tr><td>RGMem (Tian et al., 2025a)</td><td>✕</td><td>Fact</td><td>基于重整化群的 memory</td><td>长对话 QA</td></tr><tr><td>MemVerse (Liu et al., 2025e)</td><td>✓</td><td>Fact</td><td>multimodal 层级知识图谱</td><td>推理、QA</td></tr></table>
**对话** 部分扁平 memory 工作专注于存储与管理对话内容。早期方法主要着眼于通过存储原始对话历史或生成递归摘要来扩展 context window，以防 forgetting（Wang et al., 2025a; Lu et al., 2023; Wang et al., 2025h; Yuan et al., 2025b）。MemGPT（Packer et al., 2023a）引入操作系统隐喻与层级管理，启发后续工作（Li et al., 2025l; Kang et al., 2025a）将活跃 context 与外部存储解耦，以实现无限 context 管理。

为提升 retrieval 精度，memory 单元的粒度与结构日益多样，并与认知对齐。COMEDY（Chen et al., 2025d）、Memory Sharing（Gao and Zhang, 2024a）与 MemGuide（Du et al., 2025b）等工作将信息压缩为紧凑的语义表示或查询—回复对，以便直接查找；而 Alonso et al. (2024) 与 MIRIX（Wang and Chen, 2025）等则采用从向量—表组合到多功能 memory 类型的混合结构。此外，研究已开始依据认知心理学界定 memory 边界，通过句法元组（Chatterjee and Agarwal, 2025）组织信息，或基于贝叶斯惊奇（Bayesian surprise）与段落结构切分事件（Fountas et al., 2025; Pan et al., 2025），从而匹配类人的认知切分。

随着对话深度增加，memory 演化为存储高层认知过程与叙事复杂性。Think-in-Memory（Liu et al., 2023a）与 RMM（Tan et al., 2025c）等系统不再只记录事实，而存储归纳性思考与回溯性反思以指导未来推理。在角色扮演或长篇叙事等复杂场景中，ComoRAG（Wang et al., 2025f）与 MOOM（Chen et al., 2025e）等方法将 memory 分解为事实、情节层与角色层组件，确保 agent 在延长的交互中保持连贯人格与理解。

memory 已从静态存储转向自主且自适应的优化。Mem0（Chhikara et al., 2025）为 memory 维护建立了标准化操作，为智能控制奠定基础。近期进展引入 reinforcement learning 以优化 memory 构建（Yan et al., 2025c; Wang et al., 2025p），而其他机制则关注动态校准与效率，例如预测缺失信息（Nan et al., 2025）、在多 agent 系统中管理 token 预算（Liu et al., 2025d），以及减少长期存储中的冗余（Fang et al., 2025b）。

**偏好** 部分 memory 系统专注于建模用户不断演化的品味、兴趣与决策模式，尤其在偏好理解处于核心的推荐场景中。与侧重维持对话连贯性的对话中心 memory 不同，偏好 memory 的核心在于识别用户的品味与倾向。RecMind（Wang et al., 2024h）等早期努力通过同时存储事实性用户属性与条目元数据，将用户特定信息与外部领域知识分离。InteRecAgent（Huang et al., 2025d）将 memory 折入推荐工作流，但更关注当前候选集，保留用户画像与活跃条目池以支持情境感知推荐。MR.Rec（Huang et al., 2025b）构建 memory 索引，归档完整交互过程，存储原始条目信息与按类别的偏好摘要。在 session 场景中，Memocrs（Xi et al., 2024a）提出更结构化的设计：用户特定 memory 追踪实体与用户态度，通用 memory 聚合跨用户知识。

**画像** 一部分扁平 memory 系统专注于存储与维护稳定的用户画像、角色属性或长期身份信息，使 agent 能够跨轮次、跨任务保持一致行为。MemoryBank（Zhong et al., 2024）是该方向最早的框架之一：它按时间戳组织对话历史与事件摘要，逐步构建用户画像，支持对身份相关信息的准确 retrieval。AI Persona（Wang et al., 2024f）使 memory 系统不仅处理对话语境中呈现的信息，还处理多维人机交互维度中的信息。MPC（Lee et al., 2023）扩展了这一思路，将实时人格信息与对话摘要存入 memory 池，使对话行为在长期交互中与一致人格保持对齐。Westhäußer et al. (2025) 提出更全面的画像维护机制，结合长期与 short-term memory，并在每轮之后自动生成摘要以形成中期 context，使用户画像能够通过交互持续演化。

在虚拟角色扮演场景中，ChatHaruhi（Li et al., 2023a）从小说与电视剧本中抽取对话，使模型能够通过 retrievalmemory 保持角色一致的行为。RoleLLM（Wang et al., 2024d）采取更结构化的方式，构建问答对以捕获角色特定知识。

**经验** experiential memory 不同于静态的通用知识，它源于 agent 在实际交互任务中的动态积累，涵盖具体观测、思维链、动作轨迹与环境反馈。需要注意的是，本节仅从 token 级存储的角度简要概述 experiential memory；关于该领域的更全面分析与详细讨论见第 4.2 节。

experiential memory 最基本的形式是直接归档历史行为轨迹。这一范式使 agent 能够通过 retrieval 与复用过往实例（包括成功与失败案例）来指导当前决策（Zhou et al., 2025a; Wang et al., 2025q）。

为解决原始轨迹固有的泛化能力局限，大量研究聚焦于将具体交互抽象为更高层、更泛化的经验。作为最早且最具影响力的方法之一，Reflexion（Shinn et al., 2023b）将 short-term memory 界定为轨迹历史，将 long-term memory 界定为自我反思模型产生的反馈。某些研究将复杂交互历史压缩为通用工作流、规则模板或高层"思维模板"，以促进跨问题迁移与复用（Wang et al., 2024m; Kim et al., 2025a; Yang et al., 2024b）。其他工作强调 memory 的结构化组织与动态维护。这些方法通过构建领域特定的结构化知识库、采用层级"规划—执行"memory 架构，或引入类人的 forgetting 与反思机制，确保存储的洞见仍能适应新任务并被高效更新（Tang et al., 2025c,d; Ouyang et al., 2025; Ye et al., 2025b; Zhao et al., 2024; Liang et al., 2025）。

在涉及编程或特定工具使用的语境中，experiential memory 演化为可执行技能。在这一范式下，agent 将探索经验 consolidation 为代码库、程序性脚本或工具使用条目。借助环境反馈，这些系统迭代精炼代码质量，甚至动态修改底层逻辑以实现自我演化（Wang et al., 2024a; Yin et al., 2025; Fang et al., 2025d; Xiao et al., 2025b）。此外，针对操作系统等复杂环境，一些研究将成功执行记录 distillation 为可复用范例或向量化表示，从而促进从离线构建到在线分配的高效流水线（Zhang et al., 2025a; Han et al., 2025a）。

**multimodal** multimodalmemory 系统以从原始 multimodal 数据（如图像、视频帧、音频片段与文本）中抽取的离散 token 级单元形式存储信息，使 agent 能够跨通道、跨 long-horizon 经验捕获、压缩与 retrieval 知识。在可穿戴与自我中心（egocentric）设置中，Ego-LLaVA（Shen et al., 2024）等早期工作捕获第一人称视频并转换为轻量语言描述。Memoro（Zulfikar et al., 2024）遵循类似理念，但使用语音转文本形成 embedding-based memory 块。沿此方向，Livia（Xi and Wang, 2025）将长期用户 memory 纳入具备情感感知的 AR 系统，并应用 forgetting 曲线与剪枝策略。

对于视频理解，重点转向将瞬时的视觉线索与持久的 context 信息分离。MovieChat（Song et al., 2024）采用短期/长期拆分，存储近期帧特征。MA-LMM（He et al., 2024）以双库设计进一步推进——一个存储原始视觉特征，另一个保留 query embedding。VideoAgent（Wang et al., 2024g）采用更语义化的组织方式，维护文本片段描述的时间 memory，以及跨帧追踪实体的对象级 memory。在交互式视频生成中，Context-as-Memory（Yu et al., 2025b）表明，仅将先前生成的帧作为 memory 存储也可能非常有效。WorldMM（Yeo et al., 2025）构建多个相互强化的 memory 模块，在文本与视觉两种模态中捕获信息。

在具身场景中，memory 与空间结构及持续交互内在绑定。KARMA（Wang et al., 2025r）引入双层 memory 系统：long-term memory 在 3D 场景图中存储静态对象，short-term memory 追踪对象位置与状态变化。Embodied VideoAgent（Fan et al., 2025）同样构建持久对象 memory，但将其与第一人称视频及额外的具身传感器融合。Mem2Ego（Zhang et al., 2025m）将这一思路扩展到导航，把全局地图、地标描述与访问历史分离为三个不同的 memory 存储。作为对上述任务驱动设计的补充，MEMENTO（Kwon et al., 2025）提供一个评测框架，将 multimodal 交互历史视为 agent 的 memory，从而系统评估具身系统利用累积感知经验的程度。

**讨论** 扁平 memory 的主要优势在于简单性与可扩展性：memory 可以以极小成本追加或剪枝，相似度搜索等 retrieval 方法允许灵活访问而无需预定义结构。这使其适用于广泛召回、情节积累与快速变化的交互历史。然而，缺乏显式关系组织意味着连贯性与相关性高度依赖 retrieval 质量。随着 memory 增长，冗余与噪声会累积，模型可能 retrieval 到相关单元却不理解它们如何关联，从而限制组合推理、long-horizon 规划与抽象形成。因此，无拓扑集合擅长广泛覆盖与轻量更新，但在需要结构化推断或稳定知识组织的任务中受到约束。

## 3.1.2 平面 memory（2D）

## 平面（2D）memory 的定义
平面 memory 在 memory 单元之间引入显式的组织拓扑，但仅限单一结构层，简称 2D。该拓扑可以是图、树、表、隐式连接结构等，其中邻接、父子次序或语义分组等关系编码于同一平面之内，不涉及层级或跨层引用。

平面 memory 形式的核心在于突破单一存储池，建立显式关联机制，实现从单纯"存储"到"组织"的跃迁。

**树** 树结构以层级方式组织信息，可处理不同层次的抽象。HAT（A et al., 2024）通过切分长交互并逐步聚合，构建层级聚合树（Hierarchical Aggregate Tree）。这种多层结构支持由粗到细的 retrieval，在长 context 问答中优于扁平向量索引。为减少对话碎片化，MemTree（Rezazadeh et al., 2025c）引入动态表示，从孤立对话日志中推断层级模式（schema）。它逐步将具体事件摘要为更高层概念，使 agent 既能使用细粒度 memory，也能使用抽象知识。

**图** 由于能够捕获复杂关联、因果性与时间动态，图结构主导了 2D memory 的图景。Ret-LLM（Modarressi et al., 2023）等基础性工作将外部存储抽象为可寻址的、基于三元组的单元，使 LLM 能够与一个类轻量知识图谱的关系中心表交互。在医学领域，HuaTuo（Wang et al., 2023a）通过整合中文医学知识图谱与临床文本的结构化语料并 fine-tuning 基础模型，注入专业知识。KGT（Sun et al., 2024）引入实时个性化机制，将用户偏好与反馈编码为用户特定知识图谱中的节点与边。对于推理密集型任务，PREMem（Kim et al., 2025b）将部分推断负担转移到 memory 构建阶段，从原始对话中导出结构化 memory 条目及其演化关系。类似地，memory 增强的查询重构（Memory-augmented Query Reconstruction）（Xu et al., 2025b）维护专用的查询 memory，记录过往 KG 查询与推理步骤，并利用 retrieval 到的记录重构更准确的查询。从时间线视角出发，TeaFarm（iunn Ong et al., 2025）沿分段的时间线组织对话历史，并应用结构化压缩以管理终身 context。COMET（Kim et al., 2024b）利用外部常识库解析对话，并用推断出的隐藏属性动态更新情境感知的人格图，从而进一步精炼 session memory。A-Mem（Xu et al., 2025c）将知识标准化为卡片式单元，按相关性组织，并将相关 memory 放入同一盒子，从而构建完整的 memory 网络。Intrinsic Memory Agents（Yuen et al., 2025）采用分区架构，各子 agent 维护各自的角色特定私有 memory，同时协作读写共享 memory。扩展到 multimodalagent，M3-Agent（Long et al., 2025）将图像、音频与文本统一为以实体为中心的 memory 图。SALI（Pan et al., 2024）构建"现实—想象"混合 memory（Reality–Imagination Hybrid Memory），将真实观测与想象的未来场景统一为一致的导航图。

**混合** 复杂任务常需混合架构，将不同认知功能分区，同时共享同一 memory 基底。Optimus-1（Li et al., 2024d）将静态知识显式分离为用于规划的层级有向知识图谱，将动态交互分离为用于反思与自我改进的抽象 multimodal 经验池。D-SMART（Lei et al., 2025）将结构化 factual memory（实现为持续更新的知识图谱）与基于遍历的推理树相结合。

**讨论** 平面 memory 通过在节点之间有效建立链接，使 memory 能够发挥集体协同效应，从而编码更全面的情境知识。此外，它支持超越简单迭代的 retrieval 机制，包括结构化键值查找与沿图边的关系遍历。这些能力使该形式在 memory 的存储、组织与管理方面表现强劲。然而，它也存在一个关键局限：缺少层级存储机制，所有 memory 都必须被整合进单一、整体式的模块。随着任务场景复杂度与多样性上升，这种冗余且扁平化的设计越来越不足以支撑稳健性能。更重要的是，高昂的构建与搜索成本显著阻碍其实际部署。

## 3.1.3 层级 memory（3D）

## 层级（3D）memory 的定义

层级 memory 跨层组织信息，利用层间连接将 memory 塑造成体状的结构化空间。

这种层级支持不同抽象程度的表示——从原始观测，到紧凑的事件摘要，再到更高层的主题模式。跨层连接进一步产生一个体状 memory 空间，系统在其中不仅可以在单元之间横向导航，还可以跨抽象层级纵向导航。

层级 memory 超越了简单的分层，旨在构建具备深度抽象能力与动态演化机制的复杂系统。此类工作通常采用多级图结构或受神经科学启发的机制，构建更接近人类的体状 memory 空间，其中信息更丰富，memory 单元之间的连接更清晰、更显式。

**金字塔** 这一类将 memory 构建为多级金字塔，信息被逐步组织到更高层抽象，并以由粗到细的方式查询。HiAgent（Hu et al., 2025a）通过以子目标为中心的层级 working memory 管理 long-horizon 任务：为当前活跃子目标保留详细轨迹，同时将已完成子目标压缩为更高层摘要，以便在需要时选择性 retrieval。GraphRAG（Edge et al., 2025）通过社区检测构建多层图索引，递归地将实体级子图聚合为社区级摘要。作为聚类 memory 节点思路的扩展，Zep（Rasmussen et al., 2025）将 agent memory 形式化为时间知识图谱（Temporal Knowledge Graph），并同样执行社区划分。ILM-TR（Tang et al., 2024）采用树状金字塔索引并结合内循环（Inner Loop）机制，反复查询不同抽象层的摘要并更新 short-term memory 缓冲区，直至 retrieval 到的证据与生成的答案趋于稳定。为确保可控的个性化，EMG-RAG（Wang et al., 2024l）将可编辑 memory 图（Editable Memory Graph）组织为三层，其中树状的类型与子类索引（L1、L2）位于实体级 memory 图（L3）之上。在多 agent 系统中，G-Memory（Zhang et al., 2025c）用洞见图、查询图与交互图的三层图层级来组织共享经验。这一设计使以查询为中心的遍历能够在高层跨试验洞见与具体协作的紧凑轨迹之间垂直移动。

**多层** 这些形式转而强调分层专门化，将 memory 组织为聚焦特定信息类型或功能的不同模块或层次。Lyfe Agents（Kaiya et al., 2023）将显著的长期记录与低价值瞬时细节分离，使系统维持一个紧凑、对行为重要的 memory 层。H-Mem（Sun and Zeng, 2025）将长期对话 memory 显式安排为按语义抽象排序的多级层级，较低层存储细粒度交互片段，较高层存储日益压缩的摘要。HippoRAG（Gutierrez et al., 2024）等受生物学启发的架构将 memory 分解为联想索引组件（实现为开放知识图谱）与底层段落存储，并用图层编排对存储内容的多跳 retrieval。其后续 HippoRAG 2（Gutiérrez et al., 2025）将这一设计扩展到非 parametric 持续学习设置，通过更深的段落整合与在线 LLM 过滤来丰富索引层。AriGraph（Anokhin et al., 2024）在统一图内按信息类型分离 memory，将编码环境结构的语义知识图谱世界模型，与将具体观测链接回语义骨架的事件级组件相结合。类似地，SGMem（Wu et al., 2025h）在原始对话之上增加句图（sentence graph）memory 层，将历史表示为分块单元内的句级图。CAM（Li et al., 2025g）对阅读过程本身分层，将重叠的语义图逐步聚类为层级模式结构。近期，CompassMem（Hu et al., 2026b）与 MAGMA（Jiang et al., 2026）等方法开始探索富含逻辑关系的层级组合策略，旨在使 memory 的 retrieval 与利用更高效、更全面，使 memory 能为模型提供超越纯语义信息的收益。

**讨论** 通过将 memory 节点置于层级与关系维度的交汇处，层级 memory 允许不同 memory 相互作用并形成多维协同。这一设计帮助系统编码更整体、更深层情境化的知识。该形式也支持强大的 retrieval：它使复杂、多路径的查询得以在各层内的关系网络与层间的抽象层级间穿行。这种能力使系统能够高精度地 retrieval 任务相关 memory，从而获得强劲的任务表现。然而，结构的复杂性及其稠密的信息组织，对 retrieval 效率与整体有效性都构成挑战。特别是，确保所有存储 memory 保持语义有意义，以及设计系统最优的三维布局，仍是困难而关键的问题。

## 3.2 parametric memory

与以可见、可编辑的离散单元存储信息的 token 级 memory 相反，parametric memory 将信息直接存储在模型参数之中。本节考察将 memory 嵌入可学习参数空间的方法，使模型能够在不访问外部存储的情况下内化并回忆信息。

依据 memory 相对于核心模型参数的存储位置，我们区分两种主要的 parametric memory 形式：

## parametric memory 的两大类型

1. 内部 parametric memory：memory 编码在模型原有参数（例如权重、偏置）之中。这些方法直接调整基础模型以纳入新知识或新行为。

2. 外部 parametric memory：memory 存储在附加或辅助参数集之中，例如适配器（adapter）、LoRA 模块或轻量代理模型。这些方法引入新参数来承载 memory，而不修改原模型权重。

这一区分反映了一个关键设计选择：memory 是完全被吸收进基础模型，还是以模块化方式附着其旁。在随后的小节中，我们针对每种形式概述实现方法、分析其优势与局限，并列出代表性系统或工作。表 2 给出代表性 parametric memory 方法的概览。

## 3.2.1 内部 parametric memory

内部参数 memory 将下游任务所需的领域知识、个性化知识或先验注入模型。我们也将增强模型的长 context 能力视为注入一种先验。

表 2 parametric memory 方法的分类。我们依据相对于核心模型的存储位置对既有工作分类：内部 parametric memory 将知识直接嵌入原始权重，外部 parametric memory 则将信息隔离在辅助参数集之中。依据训练阶段，我们对文献作了二次分类。方法沿三个技术维度比较：(1) Type 界定 memory 的性质，(2) Task 指明目标下游应用，(3) Optimization 表示优化策略，例如 SFT、FT（fine-tuning）与 PE（提示工程）。
<table><tr><td>Method</td><td>Type</td><td>Task</td><td>优化</td></tr><tr><td colspan="4">I. 内部 parametric memory</td></tr><tr><td colspan="4">(a) 预训练阶段</td></tr><tr><td>TNL (Qin et al., 2024b)</td><td>working memory</td><td>QA、推理</td><td>SFT</td></tr><tr><td>StreamingLLM (Xiao et al., 2024)</td><td>working memory</td><td>QA、推理</td><td>SFT</td></tr><tr><td>LMLM (Zhao et al., 2025b)</td><td>factual memory</td><td>QA、事实生成</td><td>SFT</td></tr><tr><td>HierMemLM (Pouransari et al., 2025)</td><td>factual memory</td><td>QA、语言建模</td><td>SFT</td></tr><tr><td>Function Token (Zhang et al., 2025o)</td><td>factual memory</td><td>语言建模</td><td>预训练</td></tr><tr><td colspan="4">(b) 中期训练阶段</td></tr><tr><td>Agent-Founder (Su et al., 2025)</td><td>experiential memory</td><td>工具调用、深度研究</td><td>SFT</td></tr><tr><td>Early Experience (Zhang et al., 2025k)</td><td>experiential memory</td><td>工具调用、具身模拟、推理、Web</td><td>SFT</td></tr><tr><td colspan="4">(c) 后训练阶段</td></tr><tr><td>Character-LM (Shao et al., 2023)</td><td>factual memory</td><td>角色扮演</td><td>SFT</td></tr><tr><td>CharacterGLM (Zhou et al., 2024a)</td><td>factual memory</td><td>角色扮演</td><td>SFT</td></tr><tr><td>SELF-PARAM (Wang et al., 2025o)</td><td>factual memory</td><td>QA、推荐</td><td>KL 调优</td></tr><tr><td>Room (Kim et al., 2023b)</td><td>experiential memory</td><td>具身任务</td><td>RL</td></tr><tr><td>KnowledgeEditor (Cao et al., 2021)</td><td>factual memory</td><td>QA、事实核查</td><td>FT</td></tr><tr><td>Mend (Mitchell et al., 2022)</td><td>factual memory</td><td>QA、事实核查、模型编辑</td><td>FT</td></tr><tr><td>PersonalityEdit Mao et al. (2024)</td><td>factual memory</td><td>QA、模型编辑</td><td>FT、PE</td></tr><tr><td>APP (Ma et al., 2024)</td><td>factual memory</td><td>QA</td><td>FT</td></tr><tr><td>DINM (Wang et al., 2024c)</td><td>experiential memory</td><td>QA、去毒化</td><td>FT</td></tr><tr><td>AlphaEdit (Fang et al., 2025c)</td><td>factual memory</td><td>QA</td><td>FT</td></tr><tr><td colspan="4">II. 外部 parametric memory</td></tr><tr><td colspan="4">(a) 基于适配器的模块</td></tr><tr><td>MLP-Memory (Wei et al., 2025d)</td><td>factual memory</td><td>QA、分类、文本蕴含</td><td>SFT</td></tr><tr><td>K-Adapter (Wang et al., 2021)</td><td>factual memory</td><td>QA、实体类型标注、分类</td><td>SFT</td></tr><tr><td>WISE (Wang et al., 2024e)</td><td>factual memory</td><td>QA、幻觉检测</td><td>SFT</td></tr><tr><td>ELDER (Li et al., 2025d)</td><td>factual memory</td><td>模型编辑</td><td>SFT</td></tr><tr><td>T-Patcher (Huang et al., 2023)</td><td>factual memory</td><td>QA</td><td>FT</td></tr><tr><td>Sparse Memory FT (Lin et al., 2025a)</td><td>factual memory</td><td>QA</td><td>SFT</td></tr><tr><td>Memory Decoder (Cao et al., 2025a)</td><td>factual memory</td><td>QA、语言建模</td><td>SFT</td></tr><tr><td>MemLoRA (Bini et al., 2025)</td><td>factual memory</td><td>QA</td><td>SFT</td></tr><tr><td colspan="4">(b) 基于辅助语言模型的模块</td></tr><tr><td>MAC (Tack et al., 2024)</td><td>factual memory</td><td>QA</td><td>SFT</td></tr><tr><td>Retroformer (Yao et al., 2024a)</td><td>experiential memory</td><td>QA、网页导航</td><td>RL</td></tr></table>
memory 注入的时机可以是预训练阶段、持续预训练阶段、中期训练阶段或后训练阶段。存储于内部参数中的 memory 不会增加额外参数或附加模块。

**预训练** 一些工作在预训练阶段引入 memory 机制，旨在解决长尾世界知识难以压缩进有限模型参数的问题。LMLM（Zhao et al., 2025b）与 HierMemLM（Pouransari et al., 2025）在预训练阶段将用于知识 retrieval 的 memory 存入模型，同时将知识本身存放在外部知识库。也有工作优化 attention computation efficiency 以增强长窗口 memory 能力（Xiao et al., 2024; Qin et al., 2024b,c; Dao, 2024; Shah et al., 2024）。

**中期训练** 在持续预训练阶段，一些工作纳入来自下游任务的通用经验。例如 Su et al. (2025) 与 Zhang et al. (2025k) 整合 agent 经验。还有工作在中期训练阶段提升 LLM 的长窗口性能或效率，使模型在 memory 辅助任务中能以更长窗口维持更多 short-term memory（Zaheer et al., 2020; Chen et al., 2024a）。

**后训练** 其他工作在后训练阶段纳入 memory 以适配下游任务。一些工作使 LLM 记住个性化的用户历史或风格；一些工作使 LLM 从过往相似任务执行的成功或失败中学习。Character-LM（Shao et al., 2023）与 CharacterGLM（Zhou et al., 2024a）将 LLM fine-tuning 为不同性格特征。在后训练阶段，SELF-PARAM（Wang et al., 2025o）通过 KL 散度 distillation 注入额外知识，而无需额外参数。Room（Kim et al., 2023b）将知识存储于外部，同时将经验保存于内部。KnowledgeEditor（Cao et al., 2021）修改内部参数，目标仅改变需要编辑的知识。MEND（Mitchell et al., 2022）利用小网络修改大模型的梯度，实现快速知识编辑。PersonalityEdit（Mao et al., 2024）基于心理学中的人格理论提出一个 LLM 人格编辑数据集。APP（Ma et al., 2024）采用多个训练目标，确保知识编辑过程中相邻知识受到的扰动最小。DINM（Wang et al., 2024c）提出一种模型编辑方法，使模型学会拒绝此类危险请求，而不影响其正常功能。

**讨论** 内部参数的优势在于结构简单，不会给原始模型增加额外推理开销或部署成本。其缺点在于内部参数难以更新：存储新 memory 需要重新训练，代价高昂且容易 forgetting 旧 memory。因此，内部参数 memory 更适合大规模存储领域知识或任务先验，而非片段式的个性化 memory 或 working memory。

## 3.2.2 外部 parametric memory

将 memory 以 token 形式存储在 LLM 之外，会导致模型对输入窗口中 token 形式 memory 内容的理解不足。同时，将 memory 存储在 LLM 参数中也有问题，例如难以更新、与预训练知识冲突。一些工作采取折衷方案，通过外部参数引入 memory，而不改动 LLM 的原始参数。

**适配器** 外部 parametric memory 的一条常见路线依赖附着于冻结基础模型的模块。MLP-Memory（Wei et al., 2025d）通过 MLP 将 RAG 知识与 Transformer 解码器整合。K-Adapter（Wang et al., 2021）在保持原始主干不变的情况下，训练任务特定适配器模块以注入新知识，实现知识的持续扩展而不干扰预训练表示。WISE（Wang et al., 2024e）进一步引入双参数 memory 设置——将预训练知识与编辑知识分离——以及一个路由机制，在推理时动态选择使用哪个参数 memory，从而缓解终身编辑过程中的冲突。ELDER（Li et al., 2025d）通过维护多个 LoRA 模块并学习一个路由函数来推进这一方向，该函数依据输入语义自适应地选择或混合这些模块，提升了长期编辑场景中的稳健性与可扩展性。总体而言，这些方法利用附加参数子空间以模块化、可逆的方式存储与 retrievalmemory，避免直接修改核心模型权重所带来的灾难性干扰风险。

![](../assets/arxiv-2512.13564-fig4-2.jpg)  
图 4 LLM agent 中 latent memory 集成的概览。与显式文本存储不同，latent memory 在模型内部表示空间中运作。该框架按 latent state 的来源分类：(a) 生成，由辅助模型 synthesized embedding 以干扰或增强 LLM 的前向传递；(b) 复用，直接传播先前的计算状态，如 KV 缓存或 intermediate embedding；(c) 变换，通过 token 选择、合并或投影压缩内部状态，以维持高效 context。

**辅助语言模型** 除基于适配器的存储之外，另一条工作路线采用架构上更解耦的外部 parametric memory 形式，将 memory 存储在独立模型或外部知识模块中。MAC（Tack et al., 2024）通过摊销网络（amortization network）将新文档的信息压缩为紧凑调制，并存入 memory 库。Retroformer（Yao et al., 2024a）提出一种学习范式，用于 memory 过往任务执行中成功或失败的经验。

**讨论** 这种外部 parametric memory 方法在可适应性与模型稳定性之间提供平衡。由于 memory 被编码进附加参数模块，它可以被添加、移除或替换，而不干扰基础模型的预训练表示空间。这支持模块化更新、任务特定个性化与可控回滚，同时避免全模型 fine-tuning 中可能出现的灾难性 forgetting 或全局权重畸变。

然而，这一方法也有局限。外部参数模块仍必须与模型内部表示流整合，这意味着其影响是间接的，并通过模型的 attention 与计算通路中介。因此，memory 注入的有效性取决于外部参数与内部 parametric 知识的对接程度。

## 3.3 latent memory

## latent memory 的定义

latent memory 指隐式承载于模型内部表示（例如 KV 缓存、激活、隐藏状态、latent embedding）之中的 memory，而非以显式、人类可读的 token 或专用参数集存储。

latent 避免以明文暴露 memory，带来实际上更低的推理延迟，同时可能通过在模型自身表示空间内保留细粒度 context 信号而获得更好的性能增益。

如图 4 所示，我们按 latent memory 的来源——即 latent state 如何形成并引入 agent——组织既有工作。我们在本部分于表 3 中总结相关工作。

## latent memory 的三大类型

1. 生成：latent memory 由独立模型或模块产生，随后作为可复用的内部表示提供给 agent。
2. 复用：latent memory 直接从先前计算中承继，最典型的是 KV 缓存复用（轮内或跨轮），以及传播隐藏状态的循环控制器（recurrent controller）或有状态控制器（stateful controller）。

3. 变换：既有 latent state 被变换为新的表示（例如 distillation、池化或压缩），使 agent 能够保留要点，同时降低延迟与 context 占用。

## 3.3.1 生成

一条主要工作路线通过生成新的 latent representation 来构建 memory，而非复用或变换既有激活。在这一范式中，模型或辅助编码器创建紧凑的连续状态。这些状态可以作为序列中的特殊 token 出现，也可以作为独立向量出现。它们概括来自长 context、任务轨迹或 multimodal 输入的关键信息。生成的 latent summary 随后被存储、插入，或用作后续推理与决策的条件。这使系统能够超越其原生 context 长度运行、维持任务特定的中间状态，并在不重访原始输入的情况下跨情节保留知识。尽管具体形式因研究而异，其底层思想是一致的：memory 通过学习到的编码或压缩被显式地产生，所得的 latent state 作为可复用的 memory 单元支撑未来推理。

这一设计选择也可能与 parametric memory 产生潜在含混，尤其是许多方法依赖单独训练的模型来生成 latent representation。然而，本章的分类立足于 memory 的形式，而非学习机制。关键在于，尽管这些方法通过学习到的编码生成 memory，所产生的 latent representation 仍被显式实例化为独立 memory 单元并加以复用，而不是直接嵌入模型参数或前向传播激活之中。在详细讨论各个方法时，我们将回到这一区分。

**单模态** 在单模态设置中，一大类方法聚焦于长 context 处理与语言建模，模型生成一小组内部表示以替代较长的原始输入（Mu et al., 2023; Luo et al., 2024; Xu et al., 2025d; Chevalier et al., 2023; Qian et al., 2025; Wang et al., 2024j, 2025n）。典型策略是将长序列压缩为少量内部 token 或连续向量，以便在后续推理中复用。例如，Gist（Mu et al., 2023）训练语言模型在处理长提示后产生一组要点 token（gist token）。Luo et al. (2024) 在每个块边界引入特殊的哨兵 token（sentinel token），并鼓励模型将局部语义聚合到该 token 中。SoftCoT（Xu et al., 2025d）沿类似方向，从最后隐藏状态生成实例特定的软 token（soft token）。

表 3 latent memory 方法的分类。我们依据 latent state 的来源对既有工作分类：生成（Generate）通过辅助模块合成 memory，复用（Reuse）传播内部计算状态，变换（Transform）压缩、修改或重构既有 latent state。方法沿三个技术维度比较：(1) Form 指明 latent memory 的具体数据类型，(2) Type 界定所记录内容的性质（例如 Working、Factual 与 Experiential），(3) Task 表示目标下游应用。
<table><tr><td>Method</td><td>Form</td><td>Type</td><td>Task</td></tr><tr><td colspan="4">I. 生成</td></tr><tr><td colspan="4">(a) 单模态</td></tr><tr><td>Gist (Mu et al., 2023)</td><td>要点 token</td><td>Working</td><td>长 context 压缩</td></tr><tr><td>Taking a Deep Breath (Luo et al., 2024)</td><td>哨兵 token</td><td>Working</td><td>长 context QA</td></tr><tr><td>SoftCoT (Xu et al., 2025d)</td><td>软 token</td><td>Working</td><td>推理</td></tr><tr><td>CARE (Choi et al., 2025)</td><td>memory token</td><td>Working</td><td>QA、事实核查</td></tr><tr><td>AutoCompressor (Chevalier et al., 2023)</td><td>摘要向量</td><td>Working</td><td>QA、压缩</td></tr><tr><td>MemoRAG (Qian et al., 2025)</td><td>全局语义状态</td><td>Working</td><td>QA、摘要</td></tr><tr><td>MemoryLLM (Wang et al., 2024j)</td><td>持久 token</td><td>Fact</td><td>长对话 QA、模型编辑</td></tr><tr><td>M+ (Wang et al., 2025n)</td><td>跨层 token 池</td><td>Fact</td><td>QA</td></tr><tr><td>LM2 (Kang et al., 2025b)</td><td>矩阵槽</td><td>Working</td><td>QA、推理</td></tr><tr><td>Titans (Behrouz et al., 2025b)</td><td>神经权重（MLP）</td><td>Working</td><td>QA、语言建模</td></tr><tr><td>MemGen (Zhang et al., 2025d)</td><td>LoRA 片段</td><td>Working, Experiential</td><td>QA、数学、代码、具身任务、推理</td></tr><tr><td>EMU (Na et al., 2024)</td><td>reward-conditioned embedding</td><td>Fact</td><td>游戏</td></tr><tr><td>TokMem (Wu et al., 2025j)</td><td>memory token</td><td>Experiential</td><td>函数调用</td></tr><tr><td>Nested Learning (Behrouz et al., 2025a)</td><td>嵌套优化</td><td>Fact</td><td>语言建模</td></tr><tr><td>Memoria (Park and Bak, 2024)</td><td>带 memory 痕迹（engram）的三层 memory</td><td>Fact</td><td>语言建模</td></tr><tr><td colspan="4">(b) multimodal</td></tr><tr><td>CoMem (Wu et al., 2025d)</td><td>multimodal embedding</td><td>Fact</td><td>multimodal QA</td></tr><tr><td>ACM (Wu et al., 2025e)</td><td>trajectory embedding</td><td>Working</td><td>Web</td></tr><tr><td>Time-VLM (Zhong et al., 2025)</td><td>patch embedding</td><td>Working</td><td>视频理解</td></tr><tr><td>Mem Augmented RL (Mezghani et al., 2022)</td><td>新颖性状态编码器</td><td>Working</td><td>视觉导航</td></tr><tr><td>MemoryVLA (Shi et al., 2025a)</td><td>感知状态</td><td>Fact, Working</td><td>具身任务</td></tr><tr><td>XMem (Cheng and Schwing, 2022)</td><td>key-value embedding</td><td>Working</td><td>视频分割</td></tr><tr><td colspan="4">II. 复用</td></tr><tr><td>Memorizing Transformers (Wu et al., 2022)</td><td>外部 KV 缓存</td><td>Working</td><td>语言建模</td></tr><tr><td>SirLLM (Yao et al., 2024b)</td><td>熵选择的 KV</td><td>Fact</td><td>长对话 QA</td></tr><tr><td> $Memory^3$ (Yang et al., 2024a)</td><td>关键 KV 对</td><td>Fact</td><td>QA</td></tr><tr><td>FOT (Tworkowski et al., 2023)</td><td>memory attention KV</td><td>Working</td><td>QA、少样本学习、语言建模</td></tr><tr><td>LONGMEM (Wang et al., 2023b)</td><td>残差 SideNet KV</td><td>Working</td><td>语言建模与理解</td></tr><tr><td colspan="4">III. 变换</td></tr><tr><td>Scissorhands (Liu et al., 2023b)</td><td>剪枝 KV</td><td>Working</td><td>图像分类与生成</td></tr><tr><td>SnapKV (Li et al., 2024b)</td><td>聚合前缀 KV</td><td>Working</td><td>语言建模</td></tr><tr><td>PyramidKV (Cai et al., 2024)</td><td>逐层预算</td><td>Working</td><td>语言建模</td></tr><tr><td>RazorAttention (Tang et al., 2025a)</td><td>补偿窗口</td><td>Working</td><td>语言建模</td></tr><tr><td>H2O (Zhang et al., 2023)</td><td>重击者 token（heavy hitter token）</td><td>Working</td><td>QA、语言建模</td></tr><tr><td> $R^3Mem$ (Wang et al., 2025k)</td><td>带可逆压缩的虚拟 memory token</td><td>Working</td><td>QA、语言建模</td></tr></table>
CARE（Choi et al., 2025）通过训练一个 context 评估器，将 retrieval 到的 RAG 文档压缩为紧凑的 memory token，进一步扩展了 latent token 的用法。

AutoCompressor（Chevalier et al., 2023）与 MemoRAG（Qian et al., 2025）等工作强调向量化或独立的 latent representation。AutoCompressor（Chevalier et al., 2023）将整篇长文档编码为少量摘要向量，充当软提示；而 MemoRAG（Qian et al., 2025）使用 LLM 产生紧凑的隐藏状态 memory，以捕获全局语义结构。这些方法不仅从原始文本中抽象出来，还将 retrieval 到或情境化的信息变换为为复用而优化的新 latent memory 单元。为支持更持久的 memory，MemoryLLM（Wang et al., 2024j）在模型 latent space 中嵌入一组专用 memory token。M+（Wang et al., 2025n）将这一思路扩展为跨层 long-term memory 架构。LM2（Kang et al., 2025b）沿相关但结构不同的方向，在每一层引入矩阵形 latent memory 槽。

另一支工作将 latent memory 的生成内化于模型的参数动态之中。尽管这些工作依赖 parametric 模块，其运作性 memory 单元仍是 latent representation，因而仍稳稳属于本类别。Titans（Behrouz et al., 2025b）将长程信息压缩为在线更新的 MLP 权重，在推理时产生 latent vector。MemGen（Zhang et al., 2025d）在解码期间动态生成 latent memory：两个 LoRA 适配器决定在何处插入 memory 片段以及插入什么 latent content。EMU（Na et al., 2024）训练状态编码器，以产生标注了回报与合意性（desirability）的 latent embedding。

**multimodal** 在 multimodal 设置中，生成式 latent memory 扩展到图像、音频与视频，将它们编码为紧凑的 latent representation。CoMem（Wu et al., 2025d）使用 VLM 将 multimodal 知识压缩为 a set of embeddings，充当即插即用的 memory。类似地，Wu et al. (2025e) 将整个 GUI 交互轨迹压缩为 fixed-length embedding，并注入 VLM 的输入空间。对于时间建模，Time-VLM（Zhong et al., 2025）将视频或交互流切分为图块，并为每个图块生成一个 latent embedding。

在基于视觉的导航中，Mezghani et al. (2022) 学习一个状态编码器，将视觉观测映射到 latent space，并构建只包含新颖观测的 episodic memory。MemoryVLA（Shi et al., 2025a）维护一个感知—认知 memory 库（Perceptual–Cognitive Memory Bank），以 Transformer 隐藏状态存储感知细节与高层语义。在长视频对象分割中，XMem（Cheng and Schwing, 2022）将每一帧编码为键值 latent embedding，并将其组织为包含感知、工作与长期组件的多阶段 memory。

**讨论** 这些单模态与 multimodal 方法共享同一基本原理：先生成紧凑的 latent representation，再将其作为 memory 条目加以维护与 retrieval。模型可以主动构建高度信息密集、契合任务的表示，以最小的存储成本捕获关键动态、长程依赖或跨模态关系。这也避免了对完整 context 的反复处理，使跨延长交互的推理更高效。

然而，其缺陷同样明显。生成过程本身可能引入信息损失或偏差，且状态在多次读写循环后可能漂移或累积误差。此外，训练专用模块来生成 latent representation 会带来额外计算开销、数据需求与工程复杂性。

## 3.3.2 复用

与生成新 latent representation 的方法相反，另一条工作路线直接复用模型的内部激活（主要是键值（KV）缓存）作为 latent memory。这些方法不改换（修改、压缩）已存储的 KV 对，而将前向传递的原始激活视为可复用的 memory 条目。主要挑战在于确定保留哪些 KV 对、如何索引它们，以及如何在长 context 或持续处理需求下高效 retrieval 它们。

从认知视角看，Gershman et al. (2025) 提供了概念基础，将生物 memory 框定为键值系统：键充当 retrieval 地址，值编码存储内容——这一抽象与现代 LLM 中基于 KV 的 memory 高度一致。Memorizing Transformers（Wu et al., 2022）显式存储过去的 KV 对，并在推理时通过 K 近邻搜索 retrieval 它们。FOT（Tworkowski et al., 2023）通过引入 memory attention layer 扩展了这一路线，在推理时对额外的 KV memory 执行基于 KNN 的 retrieval。LONGMEM（Wang et al., 2023b）同样增强了长程 retrieval，采用轻量残差 SideNet 将历史 KV embedding 视为持久 memory 库。这些系统展示了：对 latent KV 状态进行 retrieval 感知的组织，能够大幅增强对遥远信息的访问。

**讨论** 复用型 latent memory 方法凸显了直接利用模型自身内部激活作为 memory 的有效性，表明经过精心整理的 KV 表示可以作为长程 retrieval 与推理的强大而高效的基底。

其最大优势在于保留模型内部激活的完整保真度，确保信息不会因剪枝或压缩而丢失。这使其概念上简单、易于集成到既有形式，并且高度忠实于模型的原始计算。然而，原始 KV 缓存随 context 长度快速增长，增加了内存消耗，并可能使 retrieval 效率下降。因此，复用的有效性在很大程度上取决于索引策略。

## 3.3.3 变换

变换型 latent memory 方法专注于修改、压缩或重构既有 latent state，而非生成全新的 latent state 或直接复用原始 KV 缓存。这些方法将 KV 缓存与隐藏激活视为可塑的 memory 单元，通过选择、聚合或结构变换对其重塑。由此，它们处于生成型与复用型 memory 之间的概念中间地带：模型既不创建全新的 latent representation，也不只是简单重放已存储的 KV 对。

![](../assets/arxiv-2512.13564-fig5-2.jpg)  
图 5 LLM agent 三种互补 memory 范式的概览。token 级 memory、parametric memory 与 latent memory 在表示形式、更新动态、可解释性与效率上各有不同，因而在 long-horizon 与交互式 agent 系统中形成不同的优势、局限与应用领域。

一条主要工作路线聚焦于在保留关键语义的同时压缩 KV 缓存。一些方法通过只保留最具影响力的 token 来降低内存占用。Scissorhands（Liu et al., 2023b）在缓存容量超限时依据 attention scores 剪枝 token；而 SnapKV（Li et al., 2024b）通过逐头投票机制聚合高重要性的前缀 KV 表示。PyramidKV（Cai et al., 2024）在层间重新分配 KV 预算。SirLLM（Yao et al., 2024b）在这一视角上更进一步，用 token 熵准则估计 token 重要性，并仅选择性保留有信息量的 KV 条目。Memory<sup>3</sup>（Yang et al., 2024a）只存储最关键的 attention key-value pairs，显著缩减存储需求。RazorAttention（Tang et al., 2025a）引入更显式的压缩方案：计算每个头的有效 attention span，仅保留有限的局部窗口，并使用补偿 token 保留来自被丢弃条目的信息。从更偏效率的视角看，H2O（Zhang et al., 2023）采用更简单的驱逐策略，仅保留最近的 token 以及特殊的 H2 token，以降低内存足迹。

**讨论** 这些方法展示了 latent memory 如何通过选择、retrieval 增强或压缩重编码，被变换为更有效的 memory 表示，使 LLM 能够在不依赖原始缓存复用的情况下扩展可用 context 长度并提升推理性能。

其主要优势在于产生更紧凑、信息更密集的 memory 表示，从而降低存储成本并支持长 context 上的高效 retrieval。通过重塑 latent state，这些方法使模型能够访问 distillation 后的语义信号，这些信号可能比原始激活更有用。然而，变换带来信息损失的风险，与直接复用的 KV 缓存相比，压缩后的状态可能更难解释或验证。剪枝、聚合或重编码所需的额外计算也增加了系统复杂性。

## 3.4 适配

如上所示，已有大量工作聚焦于 agent memory，清晰表明 memory 机制对 agent 系统不可或缺（Zhang et al., 2025s）。agent 系统中 memory 类型的选择，反映了设计者期望 agent 在给定任务中如何行为。设计者不仅是在要求 agent 记住某些信息，也在隐式表达他们希望这些信息如何塑造 agent 的行为。因此，为任务选择正确的 memory 类型远非简单的组合选择。

本节从各 memory 类型的特征出发，讨论在理想设置下它们最适合哪些任务与场景，如图 5 所示。我们希望这一讨论能为实际选择提供有用的思路与指导。示例仅说明这些理想化设置中 memory 的一种可能形式，并不意味着其他 memory 类型在同一场景中缺乏独特优势。

**token 级 memory** token 级 memory 仍是符号化、可寻址且透明的，因此特别适合需要显式推理、可控性与可问责性的场景。这类 memory 在实时、高频更新的设置中表现出色：agent 必须持续追踪与修订信息，且知识本身呈现可被显式建模的清晰结构。其可外化性使 memory 易于检视、审计、迁移或修订，因而尤其适合需要精确增/删/改操作的领域。高度的可解释性进一步确保 agent 的决策过程可追溯至具体 memory 单元，这在高风险应用中是一项关键属性。此外，token 级 memory 提供长期稳定性并避免灾难性 forgetting，使 agent 能够在延长的时程中积累可靠知识。另一个实际优势是，token 级 memory 通常实现为即插即用模块，可随时与最新的闭源或开源基础模型集成，而无需修改其内部参数。

## 可能场景：

• 聊天机器人与多轮对话系统。（Zhong et al., 2024; Lu et al., 2023; Chhikara et al., 2025）

• 需要稳定 memory 的 long-horizon 或终身 agent。（Wang et al., 2024f; Westhäußer et al., 2025）

• 用户特定的个性化画像。（Wang et al., 2024f; Lee et al., 2023）

• 推荐系统。（Wang et al., 2024h; Huang et al., 2025d; Xi et al., 2024a）

• 企业或组织知识库。

• 法律、合规及其他需要可验证来源的高风险领域。
**parametric memory** 与符号 memory 相比，parametric memory 是隐式的、抽象的且可泛化的，因而天然适合需要概念理解与广泛模式归纳的任务。当 agent 必须依赖适用于多样情境的通用知识或规则时，它尤其有效，因为此类规律可作为分布式表示被内化，而无需显式外部查找。这种内化支撑流畅的推理与端到端处理，使模型能够系统地泛化到未见任务或问题变体。因此，parametric memory 更契合要求结构性洞见、稳健抽象以及深度内化的行为或风格模式的任务。

## 可能场景：

• 角色扮演或人格一致的行为。（Shao et al., 2023; Zhou et al., 2024a）

• 数学推理、编程、游戏与结构化问题求解。

• 人类对齐与规范性的行为先验。

• 风格化、专业化或领域专家式回复。

**latent memory** 与 token 级 memory 或 parametric memory 不同，latent memory 位于显式数据与固定模型权重之间，实现灵活性与效率的独特平衡。其低可读性提供内在的隐私保护，使 latent representation 适合处理敏感信息。同时，其高表达能力允许以最小的信息损失进行丰富的语义编码，使 agent 能够捕获跨模态或跨任务的细微关联。latent memory 还支持高效的推理时 retrieval 与整合，使 agent 能够注入大量紧凑知识。因此，这一 memory 类型优先考虑性能与可扩展性，而非可解释性，实现高知识密度与高压缩比，非常适合受限或高度动态的环境。

## 可能场景：

• multimodal 或完全集成的 agent 架构。（Shi et al., 2025a; Cheng and Schwing, 2022; Wu et al., 2025d）

• 设备端或边缘部署以及云端服务环境。

• 加密或隐私敏感的应用领域。

## 4 功能：agent 为何需要 memory？

从作为通用、无状态文本处理器的大语言模型，转向自主、目标导向的 agent，并非渐进式的一步，而是根本性的范式转变。这一转变暴露了无状态性的关键局限。按定义，agent 必须随时间持续存在、适应并连贯交互。实现这一点不仅依赖大的 context window，更根本地依赖 memory 能力。本节讨论 agent memory 的功能，即其根本目的，优先回答它为何不可或缺，而非如何实现。我们认为，agent memory 并非单一组件，而是一组不同的功能能力，每项能力在支撑持久、智能的行为中都服务于独特目标。

为提供系统分析，本节围绕一个直接映射 agent 核心需求的功能分类法来组织 memory 的"为什么"。在最高层，我们区分两个时间类别：long-term memory，作为累积知识的持久、cross-session 存储；short-term memory，作为活跃推理的瞬时、intra-session 工作区。这一高层时间划分进一步分解为三大功能支柱，构成本节分析的结构。该分类法的概览见图 6。

## 三大 memory 功能

1. factual memory（第 4.1 节）：agent 的陈述性知识库，旨在通过回忆显式事实、用户偏好与环境状态，确保一致性、连贯性与适应性。该系统回答："agent 知道什么？"

2. experiential memory（第 4.2 节）：agent 的程序性与策略性知识，通过从过往轨迹、失败与成功中抽象而积累，以实现持续学习与自我演化。该系统回答："agent 如何改进？"

3. working memory（第 4.3 节）：agent 在单个任务或 session 期间用于活跃 context 管理的、容量受限且动态受控的草稿本。该系统回答："agent 此刻在想什么？"

这三种 memory 系统并非孤立，而是构成一个动态、互联的架构，界定 agent 的认知循环。循环始于编码：agent 交互的结果，例如新获得的事实或失败计划的结果，通过摘要、反思或抽象被 consolidation 进 long-term memory。随后在处理阶段，working memory 作为即时推理的活跃工作区发挥作用。为支撑这一推理，系统依靠 retrieval，从 factual memory 与 experiential memory 的持久存储中提取相关 context 与技能以填充工作区。这一"编码—处理—retrieval"序列构成核心架构模式，使 agent 能够同时从过去学习并在当下推理。

![](../assets/arxiv-2512.13564-fig6-2.jpg)  
图 6 agent memory 的功能分类法。我们依据功能（目的）将 memory 能力组织为横跨两个时间领域的三大支柱：(1) factual memory 作为持久的陈述性知识库，确保交互的一致性、连贯性与适应性；(2) experiential memory 封装程序性知识，以支持跨情节的持续学习与自我演化；(3) working memory 提供对瞬时 context 进行主动管理的机制。

## 4.1 factual memory

factual memory 指 agent 存储与 retrieval 关于过往事件、用户特定信息以及外部环境状态的显式、陈述性事实的能力。这类信息涵盖广泛内容，包括对话历史、用户偏好与外部世界的相关属性。通过允许 agent 在解释当前输入时利用历史信息，factual memory 成为情境感知、个性化回复与扩展任务规划的基石。

为理解 agent memory 的结构组成，我们借鉴认知科学中的陈述性 memory（declarative memory）框架（Riedel and Blokland, 2015）。在神经科学中，陈述性 memory 指可被意识访问的信息的长期存储，通常按两大成分分析：episodic memory 与 semantic memory（Squire, 2004）。episodic memory 存储与特定时间、空间情境相关联的个人经历事件——一个情节的"什么、何处、何时"（Tulving, 1972, 2002）。其核心特征是能够在心理上重新体验过往事件。semantic memory 保留一般性事实知识、概念与词义，独立于获得它们的特定场合（Squire, 2004）。尽管人脑中的陈述性系统是单一的整体，这些成分代表着不同的抽象层次。

在 agent 系统中，这种生物学区分并非作为僵化的二分法，而是作为处理连续体被操作化。系统通常以记录具体交互历史（如对话轮次、用户动作与环境状态）作为情节痕迹来启动这一过程（Zhong et al., 2024; Wang et al., 2024h; Chhikara et al., 2025）。后续处理阶段应用摘要（Wang et al., 2025h; Chen et al., 2025d）、反思（Tan et al., 2025c; Park et al., 2023; Wang et al., 2025h）、实体抽取（Gutierrez et al., 2024）与事实归纳（Rasmussen et al., 2025）。所得抽象被存入向量数据库（Zhong et al., 2024）、键值存储或知识图谱（Rasmussen et al., 2025; Sun et al., 2024）等结构，并受去重与一致性检查程序约束。通过这一序列，原始事件流逐步转变为可复用的语义事实库。

在功能上，这一架构确保 agent 在交互中展现三项基本属性：一致性、连贯性与适应性。

• 一致性意味着随时间保持稳定的行为与自我呈现。通过维护关于用户特定事实与自身承诺的持久内部状态，agent 避免矛盾与立场的任意改变。

• 连贯性体现在稳健的情境感知上。agent 能够回忆并整合相关交互历史、引用过往用户输入、保持话题连续性，确保回复构成逻辑上相连的对话，而非孤立的语句。

• 适应性展现基于已存储用户画像与历史反馈来个性化行为的能力。因此，回复风格与决策会逐步贴合用户的具体需求与特征。

为便于阐述，我们进一步按 factual memory 所指的主要实体进行组织。这一以实体为中心的分类法，连同代表性方法及其技术设计选择，在第 4.1 小节系统总结。这一视角突出两个核心应用领域：

## factual memory 的两大类型

• 用户 factual memory（第 4.1.1 节）指维持人机交互一致性的事实，包括身份、稳定偏好、任务约束与历史承诺。

• 环境 factual memory（第 4.1.2 节）指维持与外部世界一致性的事实，例如文档状态、资源可用性以及其他 agent 的能力。

表 4 factual memory 方法的分类。我们依据主要目标实体对既有工作分类：用户 factual memory 聚焦于维持交互一致性，环境 factual memory 确保与外部世界一致。方法沿三个技术维度比较：(1) Carrier（第 3 节）标识存储介质，(2) Structure 沿用 token 级 memory 的分类法（第 3.1 节），(3) Optimization 表示整合策略，其中 PE 涵盖无需参数更新的提示工程与推理时技术，区别于 SFT 与 RL 等基于梯度的方法。
<table><tr><td>Method</td><td>Carrier</td><td>结构</td><td>Task</td><td>优化</td></tr><tr><td colspan="5">I. 用户 factual memory</td></tr><tr><td colspan="5">(a) 对话连贯性</td></tr><tr><td>MemGPT (Packer et al., 2023b)</td><td>token 级</td><td>1D</td><td>长期对话</td><td>PE</td></tr><tr><td>TiM (Liu et al., 2023a)</td><td>token 级</td><td>2D</td><td>QA</td><td>PE</td></tr><tr><td>MemoryBank (Zhong et al., 2024)</td><td>token 级</td><td>1D</td><td>情感陪伴</td><td>PE</td></tr><tr><td>AI Persona (Wang et al., 2024f)</td><td>token 级</td><td>1D</td><td>情感陪伴</td><td>PE</td></tr><tr><td>Encode-Store-Retrieve (Shen et al., 2024)</td><td>token 级</td><td>1D</td><td>multimodal QA</td><td>PE</td></tr><tr><td>Method</td><td>Carrier</td><td>Form</td><td>Task</td><td>优化</td></tr><tr><td>Livia (Xi and Wang, 2025)</td><td>token 级</td><td>1D</td><td>情感陪伴</td><td>PE</td></tr><tr><td>mem0 (Chhikara et al., 2025)</td><td>token 级</td><td>1D</td><td>长期对话、QA</td><td>PE</td></tr><tr><td>RMM (Tan et al., 2025c)</td><td>token 级</td><td>2D</td><td>个性化</td><td>PE、RL</td></tr><tr><td>D-SMART (Lei et al., 2025)</td><td>token 级</td><td>2D</td><td>推理</td><td>PE</td></tr><tr><td>Comedy (Chen et al., 2025d)</td><td>token 级</td><td>1D</td><td>摘要、压缩、QA</td><td>PE</td></tr><tr><td>MEMENTO (Kwon et al., 2025)</td><td>token 级</td><td>1D</td><td>具身、个性化</td><td>PE</td></tr><tr><td>O-Mem (Wang et al., 2025g)</td><td>token 级</td><td>3D</td><td>个性化对话</td><td>PE</td></tr><tr><td>DAM-LLM (Lu and Li, 2025)</td><td>token 级</td><td>1D</td><td>情感陪伴</td><td>PE</td></tr><tr><td>MemInsight (Salama et al., 2025)</td><td>token 级</td><td>1D</td><td>个性化对话</td><td>PE</td></tr><tr><td>EMem (Zhou and Han, 2025a)</td><td>token 级</td><td>1D</td><td>个性化对话</td><td>PE</td></tr><tr><td>RGMem (Tian et al., 2025a)</td><td>token 级</td><td>1D</td><td>长对话 QA</td><td>PE</td></tr><tr><td>Memoria (Sarin et al., 2025)</td><td>token 级</td><td>1D</td><td>长对话 QA</td><td>PE</td></tr><tr><td>MemVerse (Liu et al., 2025e)</td><td>√</td><td>Fact</td><td>multimodal 层级知识图谱。</td><td>推理、QA</td></tr><tr><td colspan="5">(b) 目标一致性</td></tr><tr><td>RecurrentGPT (Zhou et al., 2023b)</td><td>token 级</td><td>1D</td><td>长 context 生成、个性化互动小说</td><td>PE</td></tr><tr><td>Memolet (Yen and Zhao, 2024)</td><td>token 级</td><td>2D</td><td>QA、文档推理</td><td>PE</td></tr><tr><td>MemGuide (Du et al., 2025b)</td><td>token 级</td><td>1D</td><td>长对话 QA</td><td>PE、SFT</td></tr><tr><td>SGMem (Wu et al., 2025h)</td><td>token 级</td><td>2D</td><td>长 context</td><td>PE</td></tr><tr><td>A-Mem (Xu et al., 2025c)</td><td>token 级</td><td>2D</td><td>QA、推理</td><td>PE</td></tr><tr><td>M3-agent (Long et al., 2025)</td><td>token 级</td><td>2D</td><td>multimodal QA</td><td>PE、SFT</td></tr><tr><td>WorldMM (Yeo et al., 2025)</td><td>token 级</td><td>1D</td><td>multimodal QA</td><td>PE</td></tr><tr><td>EverMemOS (Hu et al., 2026a)</td><td>token 级</td><td>1D</td><td>长对话 QA</td><td>PE</td></tr><tr><td colspan="5">II. 环境 factual memory</td></tr><tr><td colspan="5">(a) 知识持久化</td></tr><tr><td>MemGPT (Packer et al., 2023b)</td><td>token 级</td><td>1D</td><td>文档 QA</td><td>PE</td></tr><tr><td>CALYPSO (Zhu et al., 2023)</td><td>token 级</td><td>1D</td><td>桌面游戏</td><td>PE</td></tr><tr><td>AriGraph (Anokhin et al., 2024)</td><td>token 级</td><td>3D</td><td>游戏、多操作 QA</td><td>PE</td></tr><tr><td>HippoRAG (Gutierrez et al., 2024)</td><td>token 级</td><td>3D</td><td>QA</td><td>PE</td></tr><tr><td>WISE (Wang et al., 2024e)</td><td>parametric</td><td>/</td><td>文档推理、QA</td><td>SFT</td></tr><tr><td>MemoryLLM (Wang et al., 2024j)</td><td>parametric</td><td>/</td><td>文档推理</td><td>SFT</td></tr><tr><td>Memoria (Park and Bak, 2024)</td><td>latent</td><td>/</td><td>语言建模</td><td>PE</td></tr><tr><td>Zep (Rasmussen et al., 2025)</td><td>token 级</td><td>3D</td><td>文档分析</td><td>PE</td></tr><tr><td>MemTree (Rezazadeh et al., 2025c)</td><td>token 级</td><td>2D</td><td>文档推理、对话</td><td>PE</td></tr><tr><td>LMLM (Zhao et al., 2025b)</td><td>token 级</td><td>1D</td><td>QA</td><td>SFT</td></tr><tr><td>M+ (Wang et al., 2025n)</td><td>latent</td><td>/</td><td>文档推理、QA</td><td>SFT</td></tr><tr><td>CAM (Li et al., 2025g)</td><td>token 级</td><td>3D</td><td>多跳 QA</td><td>SFT、RFT</td></tr><tr><td>MemAct (Zhang et al., 2025r)</td><td>token 级</td><td>1D</td><td>多目标 QA</td><td>RL</td></tr><tr><td>Mem-α (Wang et al., 2025p)</td><td>token 级</td><td>1D</td><td>文档推理</td><td>RL</td></tr><tr><td>WebWeaver (Li et al., 2025m)</td><td>token 级</td><td>1D</td><td>深度研究</td><td>SFT</td></tr><tr><td>MemLoRA (Bini et al., 2025)</td><td>parametric</td><td>/</td><td>QA</td><td>SFT</td></tr><tr><td>Memory Decoder (Cao et al., 2025a)</td><td>parametric</td><td>/</td><td>QA、语言建模</td><td>SFT</td></tr><tr><td colspan="5">(b) 共享访问</td></tr><tr><td>GameGPT (Chen et al., 2023b)</td><td>token 级</td><td>1D</td><td>游戏开发</td><td>PE</td></tr><tr><td>Generative Agent (Park et al., 2023)</td><td>token 级</td><td>2D</td><td>社会模拟</td><td>PE</td></tr><tr><td> $S^3$ (Gao et al., 2023a)</td><td>token 级</td><td>1D</td><td>社会模拟</td><td>PE</td></tr><tr><td>Memory Sharing (Gao and Zhang, 2024a)</td><td>token 级</td><td>1D</td><td>文档推理</td><td>PE</td></tr><tr><td>MetaGPT (Hong et al., 2024)</td><td>token 级</td><td>1D</td><td>软件开发</td><td>PE</td></tr><tr><td>G-Memory (Zhang et al., 2025e)</td><td>token 级</td><td>3D</td><td>QA</td><td>PE</td></tr><tr><td>OASIS (Yang et al., 2025)</td><td>token 级、parametric</td><td>1D</td><td>社会模拟</td><td>PE</td></tr></table>

## 4.1.1 用户 factual memory

用户 factual memory cross-session、跨任务持久保存关于特定用户的可验证事实，包括身份、偏好、习惯、历史承诺与显著事件。

其主要功能是防止无状态交互的典型失败模式，例如指代漂移、重复问询与矛盾回复，从而减少对 long-horizon 目标的打断（Tan et al., 2025c; Zhong et al., 2024）。工程实践通常包括选择与压缩、结构化组织、retrieval 与复用以及一致性治理，目标是在有界访问成本下维持长程的对话与行为连贯性。

**对话连贯性** 对话连贯性要求 agent 在较长时期内保留对话语境、用户特定事实与稳定人格。这确保后续轮次仍对早先的披露与情感线索保持敏感，而不是退化为重复澄清或不一致回复。为此，现代系统通过两种互补策略实现用户 factual memory：启发式选择与语义抽象

为高效应对有限 context window，一项主要策略是选择性保留并对交互历史排序。系统并不保留所有原始日志，而是维护过去交互的结构化存储，按相关性、近因性、重要性或独特性等指标对条目排序（Xi and Wang, 2025; Zhong et al., 2024; Park et al., 2023; Lei et al., 2025）。通过基于这些分数过滤 retrieval，高价值条目得以保留，并周期性浓缩为更高层摘要，从而使后续回复保持连续性，而不会压垮 agent 的 working memory。

除单纯选择之外，先进框架强调将原始对话片段变换并抽象为更高层语义表示。Think in Memory（Liu et al., 2023a）与 Reflective Memory Management（Tan et al., 2025c）等方法通过迭代更新操作，将原始交互痕迹转化为思考表示或反思。这使 agent 能够查询稳定的 semantic memory，使后续回复在话题上保持一致且更少重复。类似地，COMEDY（Chen et al., 2025d）使用单一语言模型生成、压缩与复用 memory，同时更新紧凑的用户画像。这些方法通过将 memory 存储与原始 token 表层形式解耦，有效稳定了长对话历史中的人格与偏好表达。

**目标一致性** 目标一致性要求 agent 随时间维护并精炼显式的任务表示。这确保澄清性问题、信息请求与动作严格对齐首要目标，将意图漂移最小化。

为缓解此类漂移，系统利用 factual memory 动态追踪并更新任务状态。RecurrentGPT（Zhou et al., 2023b）、Memolet（Yen and Zhao, 2024）与 MemGuide（Du et al., 2025b）等方法保留已确认信息，同时突出未解决要素。通过基于任务意图引导 retrieval，这些方法帮助 agent 补足缺失约束，并 cross-session 保持专注。

对于复杂的 long-horizon 任务，memory 形式常被结构化以促进围绕活跃目标的局部化 retrieval（Wu et al., 2025h）。例如，A-Mem（Xu et al., 2025c）将 memory 组织为相互连接的笔记图，而 H-Mem（Limbacher and Legenstein, 2020）采用联想机制，在后续步骤依赖先前观测时回忆前提事实。

在具身场景中，factual memory 将 agent 行为锚定于用户特定习惯与环境语境。M3-Agent（Long et al., 2025）与 MEMENTO（Kwon et al., 2025）等系统持久保存家庭成员、物体位置与日常作息等数据，复用这些信息以最小化冗余探索与重复指令。类似地，Encode-Store-Retrieve（Shen et al., 2024）将自我中心视觉流处理为可文本寻址的条目，使 agent 能够基于过往视觉经验回答问题，而无需用户重复。

**小结** 总体而言，这些机制将短暂的交互痕迹转化为持久的认知基底。通过将基于 retrieval 的排序与生成式抽象相结合，用户 factual memory 将系统从简单的相似度匹配升级为对显式目标与约束的主动维护。这一基础带来双重收益：一方面通过长期行为连贯性培养熟悉感与信任，另一方面通过提高任务成功率、减少冗余、降低错误恢复开销来提升运作效率。

## 4.1.2 环境 factual memory

环境 factual memory 涉及用户之外的实体与状态，涵盖长文档、代码库、工具与交互痕迹。

这一 memory 范式应对事实回忆不完整与来源不可验证的问题，最小化多 agent 协作中的矛盾与冗余，并在异构环境中稳定 long-horizon 任务。其核心目标是提供一个可更新、可 retrieval、可治理的外部事实层，在 cross-session 与跨阶段提供稳定参照。具体而言，我们沿两个互补维度对既有实现分类：知识持久化与多 agent 共享访问。

**Knowledge Persistence** knowledge memory 指世界知识与领域特定知识的持久表示，用以支撑长文档分析、事实性问答、multi-hop reasoning，以及代码与数据资源的可靠 retrieval。

在知识组织方面，既有研究聚焦于将外部数据结构化以增强 reasoning 能力。例如，HippoRAG（Gutierrez et al., 2024）利用知识图谱促进证据传播，MemTree（Rezazadeh et al., 2025c）采用动态层级结构，以优化不断增长的语料中的聚合与定向访问。在存储形式方面，LMLM（Zhao et al., 2025b）明确将事实性知识与模型权重解耦，将其外置到数据库中，从而无需重新训练即可直接编辑知识并核验来源。在叙事领域，CALYPSO（Zhu et al., 2023）将冗长的游戏 context distillation 为精炼散文，保留关键故事状态的可访问性。

在需要持续知识更新的场景中，以参数为中心的方法将持久性直接整合进模型架构。MEMORYLLM（Wang et al., 2024j）、M+（Wang et al., 2025n）与 WISE（Wang et al., 2024e）等方法引入可训练的 memory pool 或 side network 以吸收新信息。这些设计并非仅依赖静态的外部 retrieval，而是聚焦于模型编辑问题，使 agent 能够适应动态环境、纠正过时事实，同时保持预训练 backbone 的稳定性。

**Shared Access** shared memory 为 multi-agent 协作建立可见且可管理的共同事实基础，用于对齐目标、承载中间产物并消除重复工作。Memory Sharing（Gao and Zhang, 2024b）等框架维护过往查询与响应的集中式仓库，使 agent 能够异步访问并基于同伴积累的洞见继续工作。这一机制确保个体 agent 直接从集体知识中获益，从而抑制矛盾结论并提升整体系统效率。

对于复杂项目协调，MetaGPT（Hong et al., 2024）与 GameGPT（Chen et al., 2023b）等系统将共享消息池用作发布计划与部分结果的中央工作区。类似地，G-Memory（Zhang et al., 2025e）采用层级 memory 图作为统一协调媒介。这些架构有助于围绕当前项目状态维持一致性，降低通信开销，并支持从历史协作中抽取可复用的 workflow。

在社会模拟领域，Generative Agents（Park et al., 2023）与 S<sup>3</sup>（Gao et al., 2023a）等平台，以及 OASIS（Yang et al., 2025）与 AgentSociety（Piao et al., 2025）等大规模模拟器，将全局环境与公共交互日志建模为 shared memory substrate。该 substrate 由群体逐步更新与观测，使信息在 agent 之间自然扩散，并在规模上支撑连贯、具历史感知的社会动态。

**Summary** environment factual memory 提供了一个可持续更新、可审计、可复用的外部事实层。在知识轴上，它通过结构化组织与 long-term memory 模块提升事实回忆的完整性、可解释性与可编辑性。在协作轴上，它通过 shared access 与治理维持跨 agent、跨阶段的一致性，从而在 long horizon、多主体与多源信息条件下支撑稳健的决策与执行。

![](../assets/arxiv-2512.13564-fig7.jpg)  
Figure 7 experiential memory 范式的分类法。我们依据所存知识的抽象层级对方法分类：(1) Case-based Memory 将原始 trajectory 与 solution 保留为具体范例；(2) Strategy-based Memory 将经验抽象为高层 strategy、template 或 workflow；(3) Skill-based Memory 将 procedural knowledge distillation 为可执行函数与 API；(4) Hybrid Memory 整合多种表示。这些系统共同映射人类的 procedural memory，以实现持续学习与自我演化。本图受 Gao et al. (2025) 启发。

## 4.2 Experiential Memory

experiential memory 概括 agent 将历史 trajectory、distillation 后的 strategy 与交互结果编码为持久、可 retrieval 表示的机制。与负责瞬时 context 的 working memory 不同，experiential memory 关注知识在不同 episode 之间的长期积累与迁移。

该范式在理论上植根于认知科学，与人类的 nondeclarative memory（尤其是程序性与习惯系统）相平行（Squire, 2004; Seger and Spiering, 2011）。生物系统依赖分布式神经回路实现隐式技能习得（Reber, 2013）。相比之下，agentic experiential memory 通常采用显式数据结构，如向量数据库或符号日志。这一实现差异赋予 agent 生物对应物所不具备的独特能力：对自身 procedural knowledge 进行内省、编辑与推理。

关键在于，experiential memory 是 experience 时代持续学习与自我演化的基础（Sutton, 2025; Gao et al., 2025）。通过维护结构化经验的仓库，agent 获得一条非参数的适应路径，避免频繁 parametric 更新的高昂成本。该机制通过将交互反馈转化为可复用知识，有效闭合学习回路。在此过程中，agent 纠正过往错误、抽象可泛化的启发式，并将常规行为编译化。因此，这种适应能最小化冗余计算，并随时间精炼决策（Zhao et al., 2024; Shinn et al., 2023b）。

为系统分析既有文献，我们依据所存信息的抽象层级对 experiential memory 分类。这一基于抽象的分类法概览与代表性范式见图 7。该分类法下的代表性方法，连同其存储载体、表示形式与优化策略，汇总于表 5。

## Three Types of Experiential Memory

• Case-based Memory（第 4.2.1 节）存储历史 episode 的最小加工记录，优先保证高信息保真度，以支持直接重放与模仿。通过保留情境与结果之间的原始对齐，它充当具体、可验证证据的仓库，可作为 in-context exemplar 用于证据驱动学习。

• Strategy-based Memory（第 4.2.2 节）从过往 trajectory 中 distillation 可迁移的 reasoning 模式、workflow 与高层洞见，以指导多样场景下的 planning。它充当认知脚手架（scaffold），将决策逻辑与特定 context 解耦，从而增强跨任务泛化并约束复杂 reasoning 的搜索空间。

• Skill-based Memory（第 4.2.3 节）封装可执行的程序性能力，从原子级代码片段到标准化 API 协议，将抽象 strategy 操作化为可验证动作。该类别充当 agent 的主动执行 substrate，支持能力的模块化扩展与工具使用环境的高效处理。

表 5 experiential memory 方法的分类。我们依据所存知识的抽象层级对既有工作分类：Case-based Memory 保留原始记录以供直接重放，Strategy-based Memory distillation 抽象启发式以支持 planning，Skill-based Memory 将可执行能力编译化以付诸行动。方法沿三个技术维度比较：(1) Carrier（第 3 节）标识存储介质，(2) Form 指明经验的表示格式，(3) Optimization 表示整合策略，其中 PE 涵盖 prompt engineering 与不涉及参数更新的推理时技术，区别于 SFT 与 RL 等基于梯度的方法。
<table><tr><td>Method</td><td>Carrier</td><td>Form</td><td>Task</td><td>Optimization</td></tr><tr><td colspan="5">I. Case-based Memory</td></tr><tr><td>Expel (Zhao et al., 2024)</td><td>Token-level</td><td>Solution</td><td>推理</td><td>PE</td></tr><tr><td>Synapse (Zheng et al., 2024a)</td><td>Token-level</td><td>Solution</td><td>Web 交互、指令引导的 Web 任务</td><td>PE</td></tr><tr><td>Fincon (Yu et al., 2024)</td><td>Token-level</td><td>Solution</td><td>金融</td><td>PE</td></tr><tr><td>MapCoder (Islam et al., 2024)</td><td>Token-level</td><td>Solution</td><td>编程</td><td>PE</td></tr><tr><td>Memento (Zhou et al., 2025a)</td><td>Token-level</td><td>Trajectory</td><td>推理</td><td>RL</td></tr><tr><td>COLA (Zhao et al., 2025a)</td><td>Token-level</td><td>Trajectory</td><td>GUI、Web 导航、推理</td><td>PE</td></tr><tr><td>Continuous Memory (Wu et al., 2025e)</td><td>Latent</td><td>Trajectory</td><td>GUI</td><td>SFT</td></tr><tr><td>JARVIS-1 (Wang et al., 2025q)</td><td>Token-level</td><td>Trajectory</td><td>游戏、GUI 交互</td><td>PE</td></tr><tr><td>MemGen (Zhang et al., 2025d)</td><td>Latent</td><td>Trajectory</td><td>Web 搜索、具身模拟、推理、数学、代码</td><td>RL、SFT</td></tr><tr><td>Early Experience (Zhang et al., 2025k)</td><td>Parametric</td><td>Trajectory</td><td>具身模拟、推理、Web 导航</td><td>SFT</td></tr><tr><td>DreamGym (Chen et al., 2025f)</td><td>Token-level</td><td>Trajectory</td><td>Web 交互、具身模拟、购物</td><td>RL</td></tr><tr><td>MemRL (Zhang et al., 2026)</td><td>Token-level</td><td>Trajectory</td><td>编程、具身模拟、推理</td><td>RL</td></tr><tr><td colspan="5">II. Strategy-based Memory</td></tr><tr><td>Reflexion (Shinn et al., 2023a)</td><td>Token-level</td><td>Insight</td><td>具身模拟、推理、编程</td><td>PE</td></tr><tr><td>Buffer of Thoughts (Yang et al., 2024b)</td><td>Token-level</td><td>Pattern</td><td>游戏、推理、编程</td><td>PE</td></tr><tr><td>AWM (Wang et al., 2024m)</td><td>Token-level</td><td>Workflow</td><td>Web 交互、指令引导的 Web 任务</td><td>PE</td></tr><tr><td>RecMind (Wang et al., 2024h)</td><td>Token-level</td><td>Pattern</td><td>推荐</td><td>PE</td></tr><tr><td> $H^2R$  (Ye et al., 2025b)</td><td>Token-level</td><td>Insight</td><td>游戏、具身模拟</td><td>PE</td></tr><tr><td>ReasoningBank (Ouyang et al., 2025)</td><td>Token-level</td><td>Insight</td><td>Web 交互、指令引导的 Web 任务</td><td>PE</td></tr><tr><td>R2D2 (Huang et al., 2025c)</td><td>Token-level</td><td>Insight</td><td>Web 交互</td><td>PE</td></tr><tr><td>BrowserAgent (Yu et al., 2025d)</td><td>Token-level</td><td>Insight</td><td>通用 QA、Web 搜索</td><td>RL、SFT</td></tr><tr><td>Agent KB (Tang et al., 2025d)</td><td>Token-level</td><td>Workflow</td><td>代码、推理</td><td>PE</td></tr><tr><td>ToolMem (Xiao et al., 2025b)</td><td>Token-level</td><td>Insight</td><td>推理、图像生成</td><td>PE</td></tr><tr><td>PRINCIPLES (Kim et al., 2025a)</td><td>Token-level</td><td>Pattern</td><td>情感陪伴</td><td>PE</td></tr><tr><td>SE-Agent (Sun et al., 2025c)</td><td>Token-level</td><td>Insight</td><td>编程</td><td>PE</td></tr><tr><td>ACE (Zhang et al., 2025n)</td><td>Token-level</td><td>Insight</td><td>编程、工具调用、金融</td><td>PE</td></tr><tr><td>Flex (Cai et al., 2025c)</td><td>Token-level</td><td>Insight</td><td>数学、化学、生物</td><td>PE</td></tr><tr><td>AgentEvolver (Zhai et al., 2025)</td><td>Parametric</td><td>Pattern</td><td>工具增强任务</td><td>RL</td></tr><tr><td>Dynamic Cheatsheet (Suzgun et al., 2025)</td><td>Token-level</td><td>Insight</td><td>数学、推理、游戏</td><td>PE</td></tr><tr><td>Training-Free GRPO (Cai et al., 2025b)</td><td>Token-level</td><td>Insight</td><td>数学、推理、Web 搜索</td><td>PE</td></tr><tr><td>MemEvolve (Zhang et al., 2025h)</td><td>Token-level</td><td>Solution,Insight</td><td>Web 搜索、推理</td><td>PE</td></tr><tr><td colspan="5">III. Skill-based Memory</td></tr><tr><td>CREATOR (Qian et al., 2023)</td><td>Token-level</td><td>Function and Script</td><td>推理、数学</td><td>PE</td></tr><tr><td>Gorilla (Patil et al., 2024)</td><td>Token-level</td><td>API</td><td>工具调用</td><td>SFT</td></tr><tr><td>ToolRerank (Zheng et al., 2024b)</td><td>Token-level</td><td>API</td><td>工具调用</td><td>PE</td></tr><tr><td>Voyager (Wang et al., 2024b)</td><td>Token-level</td><td>Code Snippet</td><td>游戏</td><td>PE</td></tr><tr><td>RepairAgent (Bouzenia et al., 2024)</td><td>Token-level</td><td>Function and Script</td><td>编程</td><td>PE</td></tr><tr><td>COLT (Qu et al., 2024)</td><td>Token-level</td><td>API</td><td>工具调用</td><td>SFT</td></tr><tr><td>ToolLLM (Qin et al., 2024a)</td><td>Token-level</td><td>API</td><td>工具调用</td><td>SFT</td></tr><tr><td>LEGOMem (Han et al., 2025a)</td><td>Token-level</td><td>Function and Script</td><td>办公</td><td>PE</td></tr><tr><td>Darwin Gödel Machine (Zhang et al., 2025i)</td><td>Token-level</td><td>Code Snippet</td><td>代码</td><td>PE</td></tr><tr><td>Huxley-Gödel Machine (Wang et al., 2025j)</td><td>Token-level</td><td>Code Snippet</td><td>代码</td><td>PE</td></tr><tr><td>MempP (Fang et al., 2025d)</td><td>Token-level</td><td>Function and Script</td><td>具身模拟、旅行规划</td><td>PE</td></tr><tr><td>SkillWeaver (Zheng et al., 2025a)</td><td>Token-level</td><td>Function and Script</td><td>Web 交互、指令引导的 Web 任务</td><td>PE</td></tr><tr><td>Alita (Qiu et al., 2025c)</td><td>Token-level</td><td>MCP</td><td>数学、推理、VQA</td><td>PE</td></tr><tr><td>Alita-G (Qiu et al., 2025b)</td><td>Token-level</td><td>MCP</td><td>数学、推理、VQA</td><td>PE</td></tr><tr><td>LearnAct (Liu et al., 2025b)</td><td>Token-level</td><td>Function and Script</td><td>移动 GUI</td><td>PE</td></tr><tr><td>ToolGen (Wang et al., 2025i)</td><td>Parametric</td><td>API</td><td>工具调用</td><td>SFT</td></tr><tr><td>MemTool (Lumer et al., 2025)</td><td>Token-level</td><td>MCP</td><td>工具调用</td><td>SFT</td></tr><tr><td>ToolRet (Shi et al., 2025c)</td><td>Token-level</td><td>API</td><td>Web、代码、工具 retrieval</td><td>SFT</td></tr><tr><td>DRAFT (Qu et al., 2025a)</td><td>Token-level</td><td>API</td><td>工具调用</td><td>PE</td></tr><tr><td>ASI (Wang et al., 2025s)</td><td>Token-level</td><td>Functions and Scripts</td><td>Web 交互</td><td>PE</td></tr></table>

## 4.2.1 Case-based Memory

Case-based memory 存储对历史事件最小化处理的记录，优先保真度，以确保 episode 能够被重放或作为 in-context exemplar 复用。与 strategy 模板或 skill 模块不同，case 避免大规模抽象，从而保留情境与解法之间的原始对齐。

**Trajectories** 这一类保留交互序列，以支持重放与证据驱动学习。为优化文本环境中的 retrieval，Memento（Zhou et al., 2025a）采用 soft Q-learning 动态精炼选择高价值过往 trajectory 的概率。在 multimodal 设置中，JARVIS-1（Wang et al., 2025q）、EvoVLA（Liu et al., 2025i）与 Auto-scaling Continuous Memory（Wu et al., 2025e）保留视觉 context，前者在 Minecraft 中存储生存经验，后者将 GUI 历史压缩为连续 embedding。此外，early experience 范式（Zhang et al., 2025k）构建无奖励、由 agent 生成的交互 trace，并通过 mid-training 将其整合进模型参数以增强泛化。

**Solutions** 这一类将 memory 视为已验证解法的仓库。ExpeL（Zhao et al., 2024）通过试错自主收集经验，将成功 trajectory 作为 exemplar 存储，同时抽取文本 insight 以指导未来动作。Synapse（Zheng et al., 2024a）类似地注入抽象化的 state-action episode 作为 context 示例，以对齐问题求解模式。在程序合成中，MapCoder（Islam et al., 2024）保留相关示例代码作为 playbook 式 case，多 agent pipeline retrieval 并适配它，以提高复杂任务的可靠性。在金融领域，FinCon（Yu et al., 2024）维护关于过往动作、PnL trajectory 与信念更新的 episodic memory，以促进稳健的跨轮决策。

**Summary** Case-based memory 提供高信息保真度，并为模仿提供可验证证据。然而，对原始数据的依赖在 retrieval 效率与 context window 消耗方面带来挑战。与可执行 skill 或抽象 strategy 不同，case 不包含编排逻辑或函数接口。相反，它们作为事实基底，供更高层 reasoning 在其上运作。

## 4.2.2 Strategy-based Memory

与保留"发生了什么"的 case 库不同，strategy-based memory 抽取关于"如何行动"的可迁移知识，涵盖可复用的 reasoning pattern、任务分解、insight、抽象与跨情境 workflow。它将经验提升为可编辑、可审计、可组合的高层知识，从而减少对冗长 trajectory 重放的依赖，提升跨任务泛化与效率。本节聚焦非代码或弱代码化的 template 与 workflow，而可执行函数、API、MCP 协议与代码片段归入第 4.2.3 节。依据所保留知识的粒度与结构复杂度，我们将 strategy-based memory 分为三种类型：原子化的 Insights、序列化的 Workflows 与图式化的 Patterns。

**Insights** 这一类方法聚焦于从过往 trajectory 中 distillation 离散知识片段，例如细粒度决策规则与反思性启发式。H<sup>2</sup>R（Ye et al., 2025b）显式解耦 planning 层与 execution 层 memory，使高层 planning insight 与低层操作规则可分别 retrieval，以支持多任务场景中的细粒度迁移。R2D2（Huang et al., 2025c）将 remembering、reflecting 与动态决策整合用于 web navigation，从失败与成功案例中导出纠正性 insight 以指导后续 episode。对于 long-horizon web 自动化，BrowserAgent（Yu et al., 2025d）将关键结论持久化为显式 memory，以稳定延长的 reasoning 链并缓解 context drift。

**Workflows** 与原子化、静态的 insight 不同，workflow 将 strategy 封装为结构化的动作序列——从先前 trajectory 抽象出的可执行例程，用于在推理时引导多步执行。Agent Workflow Memory（AWM）（Wang et al., 2024m）在 Mind2Web（Deng et al., 2023）与 WebArena（Zhou et al., 2023a）上归纳可复用 workflow，并将其作为高层 scaffold 引导后续生成，在不更新基础模型权重的情况下提高成功率、减少步数。这表明 strategy template 可作为顶层控制器，与 case 级证据互补。Agent KB（Tang et al., 2025d）建立统一知识库，将 workflow 视为可迁移的程序性知识。它采用层级 retrieval，先访问 workflow 以组织策略路径，并使问题求解逻辑能在多样 agent 架构间复用。

**Patterns** 在更高抽象层，reasoning pattern 作为认知模板，封装问题求解的结构，使 agent 能够通过实例化这些可泛化骨架来处理复杂 reasoning 任务。Buffer of Thoughts（Yang et al., 2024b）维护 thought template 的元缓冲区，retrieval 并实例化以求解新问题。类似地，ReasoningBank（Ouyang et al., 2025）将成功与失败都抽象为可复用 reasoning 单元，促进 test-time 扩展与稳健学习。RecMind 的自启发 planning 算法（Wang et al., 2024h）生成中间 self-guidance，以组织后续 planning 与工具使用。在对话 agent 领域，PRINCIPLES（Kim et al., 2025a）通过离线 self-play 构建合成 strategy memory，在推理时引导 strategy planning，从而无需额外训练。这些进展表明，从描述性规则向可移植 reasoning 结构的范式转变。

**Summary** Strategy-based memory 涵盖 insight、workflow 与 pattern，充当引导生成式 reasoning 的高层 scaffold。与依赖 retrieval 具体、原始 trajectory（可能噪声大或依赖 context）的 case-based memory 不同，这一 memory 形式 distillation 可泛化 schema，以有效约束搜索空间并提升未见任务上的稳健性。然而，一个关键区别在于，这些 strategy 充当结构性指南而非可执行动作；它们指导 planning 过程，但不直接与环境交互。这一局限使得下一节讨论的 skill-based memory 成为必要，后者存储可调用能力与工具。最终，稳健的 agent 通常协同这些组件：strategy 提供抽象 planning 逻辑，skill 负责落地执行。

## 4.2.3 Skill-based Memory

Skill memory 捕获 agent 的程序性能力，并将抽象 strategy 操作化为可验证动作。它编码 agent 能做什么，补充关于 agent 知道什么的陈述性知识，并通过提供可调用、可测试、可组合的可执行体，锚定 perception–reasoning–action 循环。近期证据表明，语言模型能够学习何时以及如何调用工具，并随工具库规模可靠扩展，从而将 skill memory 确立为现代 agent 的执行基底。

Skill memory 横跨从内部细粒度代码到外化标准化接口的连续谱。统一标准很直接：skill 必须可被 agent 调用，其结果必须可验证以支撑学习，且必须能与其他 skill 组合成更大例程。

**Code Snippets** 以可复用片段形式存储的可执行代码，提供从经验到能力的最快路径。在开放式任务中，agent 将成功的子 trajectory distillation 为可解释程序，并跨环境复用。Voyager（Wang et al., 2024b）以不断增长的 skill 库 exemplify 这一模式；Darwin Gödel Machine（Zhang et al., 2025i）更进一步，在经验验证下安全重写自身代码，产生自指且能力逐步增强的 skill 集合。

**Functions and Scripts** 将复杂行为抽象为模块化函数或脚本，可提升可复用性与泛化能力。近期进展使 agent 能够自主创建专用工具以求解问题（Qian et al., 2023; Yuan et al., 2024a），并通过演示与环境反馈在移动 GUI、web navigation 与软件工程等多样领域精炼工具使用能力（Fang et al., 2025d; Zheng et al., 2025a; Bouzenia et al., 2024）。此外，新兴的程序性 memory 机制使 agent 能将执行 trajectory distillation 为可 retrieval 脚本，促进对新场景的高效泛化（Liu et al., 2025b; Han et al., 2025a）。

**APIs** API 充当封装 skill 的通用接口。早期工作聚焦于 fine-tuning 模型以正确调用工具（Schick et al., 2023; Patil et al., 2024），而 API 库的指数增长已将主要瓶颈转移到 retrieval。标准信息 retrieval 方法往往无法捕获工具的功能语义（Shi et al., 2025c）。因此，近期方法转向基于学习的 retrieval 与 reranking 策略，考虑工具文档质量、层级关系与协作使用模式，以弥合用户意图与可执行函数之间的差距（Zheng et al., 2024b; Gao and Zhang, 2024c; Qu et al., 2024, 2025a）。

**MCPs** 为减少基于 API 的生态中的协议碎片化，Model Context Protocol 提供了一个开放标准，统一 agent 发现与使用工具和数据的方式，包括按需加载工具、削减 context 开销的代码执行模式（Qiu et al., 2025c,b）。广泛的平台支持表明正在向共同接口层收敛。

在标准可执行体之外，研究还探索工具能力的可学习 memory 以处理不确定的神经工具、将工具符号嵌入以统一 retrieval 与调用的 parametric 集成，以及把专门化 agent 视为模块化设计空间中可调用模块的 architecture-as-skill 视角（Xiao et al., 2025b; Wang et al., 2025i; Zhao et al., 2025a）。总体而言，这些线索将 skill memory 重构为可学习、可演化、可编排的能力层。

**Summary** 总之，skill-based memory 构成 agent 的主动执行基底，从静态代码片段与模块化脚本，演进到标准化 API 与可学习架构。它通过将 case-based 与 strategy-based memory 中的 insight 操作化为可验证程序，弥合抽象 planning 与环境交互之间的差距。随着工具创建、retrieval 与互操作机制（例如 MCP）成熟，skill memory 超越简单存储，形成能力合成、精炼与执行的持续循环，驱动开放式 agent 演化。

## 4.2.4 Hybrid memory

先进 agent 架构日益采用混合设计，整合多种 experiential memory 形式，以在落地证据与可泛化逻辑之间取得平衡。通过维护横跨原始 episode、distillation 规则与可执行 skill 的知识谱系，这些系统动态选择最合适的 memory 格式，确保 retrieval 精度与跨 context 的广泛泛化。

一个显著方向是将 case-based 与 strategy-based memory 耦合，以促进互补 reasoning。例如，ExpeL（Zhao et al., 2024）将具体 trajectory 与抽象文本 insight 协同，使 agent 既能回忆具体解法，又能应用通用启发式。Agent KB（Tang et al., 2025d）采用层级结构，高层 workflow 指导 planning，具体解法路径提供执行细节。类似地，R2D2（Huang et al., 2025c）将历史 trace 的回放缓冲区与反思机制整合，从过往错误中精炼决策 strategy，有效桥接 case retrieval 与 strategy 抽象。与之互补，Dynamic Cheatsheet（Suzgun et al., 2025）通过存储累积 strategy 与问题求解 insight 以供推理时即时复用，避免冗余计算。

此外，近期框架力图统一 memory 生命周期，纳入 skill-based 组件或建立综合认知架构（Sun et al., 2025a; Cai et al., 2025a）。在科学 reasoning 中，ChemAgent（Tang et al., 2025c）构建自更新库，将执行 case 与可分解 skill 模块配对，使模型能够通过累积经验精炼化学 reasoning。采取整体视角，LARP（Yan et al., 2023）为开放世界游戏建立认知架构，协调用于世界知识的 semantic memory、用于交互 case 的 episodic memory 与用于可学习 skill 的 procedural memory，确保一致的角色扮演与稳健决策。最后，G-Memory（Zhang et al., 2025c）与 Memp（Fang et al., 2025d）等演化系统实现动态跃迁：重复的成功 case 逐步被编译为高效 skill，自动化地从重 retrieval 转向快速执行。近期努力 MemVerse（Liu et al., 2025e）则结合 parametric memory 与 token-level procedural memory。

## 4.3 Working Memory

在认知科学中，working memory 被定义为一种容量受限、动态受控的机制，通过在当下选择、维持与变换任务相关信息来支撑高阶认知（Baddeley, 2012）。它不止于临时存储，还意味着资源约束下的主动控制。这一视角植根于多成分模型与 embedded-processes 解释等框架，二者都强调 attentional focus、干扰控制与有界容量（Cowan, 2014）。

迁移到 LLM 时，标准 context window 主要充当被动的只读缓冲区。模型在 inference 期间虽可消费窗口内容，却缺乏选择、维持或动态变换当前工作区的显式机制。近期行为证据表明，当前模型并不具备类人的 working memory 特征，凸显出显式工程化、可操作的 working memory 机制的必要性（Huang et al., 2025a）。

本节将 working memory 定义为在单个 episode 内主动管理与操作 context 的一组机制（Zhang et al., 2025r）。目标是让 context window 从被动缓冲区转变为可控、可更新、抗干扰的工作区。这一转变带来直接收益：在固定 attention 预算下提高任务相关信息的密度，抑制冗余与噪声，并允许重写或压缩表示以维持连贯的思维链。我们依据交互动态对这些机制分类。

表 6 系统汇总了这一基于交互的分类下的代表性 working memory 方法，以及它们的存储载体、任务领域与优化策略。

## Two Types of Working Memory

• Single-turn Working Memory（4.3.1 节）聚焦输入凝缩与抽象。在此设定下，系统必须在单次前向传播中处理海量即时输入，例如长文档或高维 multimodal 流。目标是动态过滤并重写证据，以构造有界的计算 scratchpad，从而最大化每个 token 的有效信息载荷。

• Multi-turn Working Memory（4.3.2 节）处理时间性状态维持。在顺序交互中，挑战在于防止历史累积压垮 attention 机制。这涉及通过读取、执行与更新的连续循环来维持任务状态、目标与约束，确保中间产物跨轮次被折叠并 consolidated。

总之，面向 LLM 的 working memory 代表一种范式转向：走向主动的、episode 内的 context 管理。通过与主动操作的认知要求对齐，它抑制干扰，并为长 context inference 的工程约束提供可行解法。

## 4.3.1 Single-turn Working Memory

Single-turn working memory 应对在单次前向传播内处理海量即时输入的挑战，包括长文档（Chevalier et al., 2023）与高维 multimodal 流（Wang et al., 2024g）。其目标不是被动消费整个 context，而是主动构造可写工作区。这涉及过滤并变换原始信息，以在固定 attention 与 memory 预算下提高密度与可操作性（Jiang et al., 2023, 2024）。我们将这些机制分为 input condensation 与 observation abstraction：前者减少物理 token 数量，后者将数据变换为结构化语义表示。

Input Condensation Input condensation 技术旨在预处理 context，在保留关键信息的同时最小化 token 使用（Jiang et al., 2023）。这些方法大体分为三种范式：hard、soft 与 hybrid condensation（Liao et al., 2025a）。

Hard condensation 依据重要性度量离散地选择 token。LLMLingua（Jiang et al., 2023）与 LongLLMLingua（Jiang et al., 2024）等方法估计 token 困惑度，以丢弃可预测或与任务无关的内容，而 CompAct（Yoon et al., 2024）采用迭代策略保留使信息增益最大的片段。尽管高效，hard selection 有切断句法或语义依赖的风险。Soft condensation 将变长 context 编码为稠密 latent 向量（memory slots）。Gist（Mu et al., 2023）、In-Context Autoencoder（ICAE）（Ge et al., 2024）与 AutoCompressors（Chevalier et al., 2023）等方法训练模型将 prompt 压缩为有效 summary token 或独立 memory embedding。这实现了高压缩比，但需要额外训练，且可能遮蔽细粒度细节。HyCo2（Liao et al., 2025a）等 hybrid 方法试图结合全局语义 adapter（soft）与 token 级保留概率（hard），以调和这些取舍。

Observation Abstraction 凝缩聚焦于削减，observation abstraction 则旨在将原始观察变换为便于 reasoning 的结构化格式。该机制把动态、高维的观察空间映射为固定大小的 memory state，防止 agent 被原始数据淹没。

在复杂交互环境中，抽象将冗长输入转换为简洁状态描述。Synapse（Zheng et al., 2024a）将非结构化 HTML DOM 树重写为任务相关状态摘要，以指导 GUI 自动化。类似地，在 multimodal 设定中，逐帧处理视频流在计算上不可行。working memory 机制通过抽取语义结构来应对：Context as Memory（Yu et al., 2025b）依据视野重叠过滤帧，VideoAgent（Wang et al.,

Table 6 Taxonomy of working memory methods. We categorize approaches into Single-turn and Multi-turn settings based on interaction dynamics. Methods are compared across three technical dimensions: (1) Carrier (Section 3) identifies the storage medium, (2) Task specifies the evaluation domain or application scenario, and (3) Optimization denotes the integration strategy, where PE encompasses prompt engineering and inference-time techniques without parameter updates, distinct from gradient-based methods like SFT and RL.
<table><tr><td>Method</td><td>Carrier</td><td>Task</td><td>Optimization</td></tr><tr><td colspan="4">I. Single-turn Working Memory</td></tr><tr><td colspan="4">(a) Input Condensation</td></tr><tr><td>Gist (Mu et al., 2023)</td><td>Latent</td><td>指令 fine-tuning</td><td>SFT</td></tr><tr><td>ICAE (Ge et al., 2024)</td><td>Latent</td><td>语言建模、指令 fine-tuning</td><td>Pretrain, LoRA</td></tr><tr><td>AutoCompressors (Chevalier et al., 2023)</td><td>Latent</td><td>语言建模</td><td>SFT</td></tr><tr><td>LLMLingua (Jiang et al., 2023)</td><td>Token-level</td><td>Reasoning、对话、摘要</td><td>PE</td></tr><tr><td>LongLLMLingua (Jiang et al., 2024)</td><td>Token-level</td><td>多文档 QA、长 context、多跳 QA</td><td>PE</td></tr><tr><td>CompAct (Yoon et al., 2024)</td><td>Token-level</td><td>文档 QA</td><td>SFT</td></tr><tr><td>HyCo2 (Liao et al., 2025a)</td><td>Hybrid</td><td>摘要、开放域 QA、多跳 QA</td><td>SFT</td></tr><tr><td>Sentence-Anchor (Tarasov et al., 2025)</td><td>Latent</td><td>文档 QA</td><td>SFT</td></tr><tr><td>MELODI (Chen et al., 2024c)</td><td>Hybrid</td><td>预训练</td><td>Pretrain</td></tr><tr><td>R3Mem (Wang et al., 2025k)</td><td>Latent</td><td>文档 QA、语言建模</td><td>PEFT</td></tr><tr><td colspan="4">(b) Observation Abstraction</td></tr><tr><td>Synapse (Zheng et al., 2024a)</td><td>Token-level</td><td>计算机控制、Web 导航</td><td>PE</td></tr><tr><td>VideoAgent (Wang et al., 2024g)</td><td>Token-level</td><td>长时视频理解</td><td>PE</td></tr><tr><td>MA-LMM (He et al., 2024)</td><td>Latent</td><td>长时视频理解</td><td>SFT</td></tr><tr><td>Context as Memory (Yu et al., 2025b)</td><td>Token-level</td><td>长时视频生成</td><td>PE</td></tr><tr><td colspan="4">II. Multi-turn Working Memory</td></tr><tr><td colspan="4">(c) State Consolidation</td></tr><tr><td>MEM1 (Zhou et al., 2025b)</td><td>Latent</td><td>Retrieval、开放域 QA、购物</td><td>RL</td></tr><tr><td>MemGen (Zhang et al., 2025d)</td><td>Latent</td><td>Reasoning、具身动作、Web 搜索、编码</td><td>RL</td></tr><tr><td>MemAgent (Yu et al., 2025a)</td><td>Token-level</td><td>长文档 QA</td><td>RL</td></tr><tr><td>ReMemAgent (Shi et al., 2025b)</td><td>Token-level</td><td>长文档 QA</td><td>RL</td></tr><tr><td>ReSum (Wu et al., 2025f)</td><td>Token-level</td><td>long-horizon Web 搜索</td><td>RL</td></tr><tr><td>MemSearcher (Yuan et al., 2025a)</td><td>Token-level</td><td>多跳 QA</td><td>SFT, RL</td></tr><tr><td>ACON (Kang et al., 2025c)</td><td>Token-level</td><td>App 使用、多目标 QA</td><td>PE</td></tr><tr><td>IterResearch (Chen et al., 2025b)</td><td>Token-level</td><td>Reasoning、Web 导航、long-horizon QA</td><td>RL</td></tr><tr><td>SUPO (Lu et al., 2025a)</td><td>Token-level</td><td>long-horizon 任务</td><td>RL</td></tr><tr><td>AgentDiet (Xiao et al., 2025a)</td><td>Token-level</td><td>long-horizon 任务</td><td>PE</td></tr><tr><td>SUMER (Zheng et al., 2025c)</td><td>Token-level</td><td>QA</td><td>RL</td></tr><tr><td>Sculptor (Li et al., 2025f)</td><td>Token-level</td><td>多针 QA</td><td>PE,RL</td></tr><tr><td>AgeMem (Yu et al., 2026)</td><td>Token-level</td><td>QA、具身动作</td><td>PE,RL</td></tr><tr><td colspan="4">(d) Hierarchical Folding</td></tr><tr><td>HiAgent (Hu et al., 2025a)</td><td>Token-level</td><td>long-horizon agent 任务</td><td>PE</td></tr><tr><td>Context-Folding (Sun et al., 2025b)</td><td>Token-level</td><td>深度研究、SWE</td><td>RL</td></tr><tr><td>AgentFold (Ye et al., 2025a)</td><td>Token-level</td><td>Web 搜索</td><td>SFT</td></tr><tr><td>DeepAgent (Li et al., 2025i)</td><td>Token-level</td><td>工具使用、购物、Reasoning</td><td>RL</td></tr><tr><td colspan="4">(e) Cognitive Planning</td></tr><tr><td>SayPlan (Rana et al., 2023)</td><td>Token-level</td><td>3D 场景图、机器人</td><td>PE</td></tr><tr><td>KARMA (Wang et al., 2025r)</td><td>Token-level</td><td>家庭环境</td><td>PE</td></tr><tr><td>Agent-S (Agashe et al., 2025)</td><td>Token-level</td><td>计算机使用</td><td>PE</td></tr><tr><td>PRIME (Tran et al., 2025)</td><td>Token-level</td><td>多跳 QA、知识密集 reasoning</td><td>PE</td></tr></table>
2024g）将流转换为时间事件描述，MA-LMM（He et al., 2024）维护视觉特征库。这些方法有效地将高维、冗余的流重写为低维、语义丰富的表示，使其可在有限 context window 内操作，从而实现高效处理。

Summary Single-turn working memory 充当主动压缩层，为即时 reasoning 最大化 context window 的效用。通过 input condensation 与 observation abstraction，这些机制有效提高了操作工作区的信息密度，确保在容量约束下仍保留关键证据。然而，这种优化严格限于 turn 内；它应对的是静态输入的广度与复杂度，而非动态交互的时间连续性。

## 4.3.2 Multi-turn Working Memory

Multi-turn working memory 处理的问题空间与 single-turn 设定根本不同。在 long-horizon 交互中，主要瓶颈从瞬时 context 容量转向任务状态与历史相关性的持续维持。即便拥有扩展的 context window，历史的累积仍不可避免地饱和 attention 预算、增加延迟并引发目标漂移（Lu et al., 2025b）。为缓解这一点，multi-turn 设定下的 working memory 充当外化的状态载体，组织读取、评估与写入的连续循环。目标是在有界资源预算内保持关键状态信息可访问且一致。我们按其状态管理策略将这些机制分为：state consolidation、hierarchical folding 与 cognitive planning。

State Consolidation 在连续交互流中，state consolidation 通过动态更新将不断增长的 trajectory 映射到固定大小的状态空间。将交互视为流式环境，MemAgent（Yu et al., 2025a）与 MemSearcher（Yuan et al., 2025a）采用循环机制更新固定预算的 memory 并丢弃冗余，从紧凑、演化的状态回答查询。ReSum（Wu et al., 2025f）扩展了这一做法，周期性将历史 distillation 为 reasoning state，并利用 reinforcement learning 优化以 summary 为条件的行为，以支持无限探索。

在启发式摘要之外，ACON（Kang et al., 2025c）将 state consolidation 构造为优化问题，将环境观察与交互历史联合压缩为有界凝缩，并从失败案例中迭代精炼压缩准则。IterResearch（Chen et al., 2025b）进一步采用受 MDP 启发的表述与迭代工作区重建，其中演化的报告充当持久 memory，周期性综合缓解 long-horizon 研究中的 context suffocation 与噪声污染。

在状态表示方面，各方法为确保恒定大小的足迹而有所不同。MEM1（Zhou et al., 2025b）维护共享内部状态，将新观察与先前 memory 合并。MemGen（Zhang et al., 2025d）区别于显式文本，将 latent memory token 直接注入 reasoning 流。

Hierarchical Folding 对于复杂、long-horizon 任务，状态维持需要超出线性摘要的结构。Hierarchical folding 依据子目标分解任务 trajectory，仅在子任务活跃时保留细粒度 trace，并在完成时将已完成的子 trajectory 折叠为简洁摘要。

这种先分解再 consolidated 的策略使 working memory 能够动态扩张与收缩。HiAgent（Hu et al., 2025a）以子目标为 memory 单元实例化该策略，仅保留活跃的 action–observation 对，并在子目标完成后写回摘要。Context-Folding（Sun et al., 2025b）与 AgentFold（Ye et al., 2025a）通过将折叠操作变为可学习策略来扩展此做法，训练 agent 自主决定何时分支进入子 trajectory，以及如何将其抽象为高层状态。DeepAgent（Li et al., 2025i）进一步将其应用于工具使用 reasoning，把交互压缩为结构化 episodic memory 与 working memory，以支持细粒度信用分配。通过用稳定的高层抽象替换已完成的子 trajectory，这些方法在保持活跃窗口较小的同时保留了必要 context。

Cognitive Planning 在最高抽象层级上，working memory 创建并维护外化的 plan 或 world model。状态不仅充当对过去的摘要，还作为指导未来行动的前瞻性结构。

PRIME（Tran et al., 2025）将 retrieval 直接整合进 planning 循环，确保 memory 更新主动支撑复杂的 reasoning 步骤。在具身与 agentic 环境中，将语言模型视为高层 planner 使 plan 上升为 working memory 的核心。SayPlan 等方法采用 3D 场景图作为可查询的环境 memory，以将 planning 扩展到大型空间（Rana et al., 2023）。在 GUI 与家庭任务中，Agent-S（Agashe et al., 2025）与 KARMA（Wang et al., 2025r）等系统通过将 reasoning 锚定在层级 plan 上、并利用 memory-augmented retrieval 桥接长期知识与短期执行，来稳定 long-horizon 性能。

通过使 plan 与结构化环境表示成为 working memory 可读写的核心，agent 能够维持目标一致性，并在感知失败时稳健地修订策略（Song et al., 2023）。

Summary Multi-turn working memory 的关键在于构造可操作的状态载体，而非保留原始历史。通过整合 state consolidation 以压缩连续流、hierarchical folding 以结构化子 trajectory、cognitive planning 以锚定未来行动，这些机制有效使 reasoning 性能与交互长度解耦。这一范式使 agent 能在严格遵守计算与 memory 约束的同时，在无限时程上维持时间连贯性与目标对齐。

## 5 Dynamics: How Memory Operates and Evolves?

前几节介绍了 memory 的架构形式（第 3 节）与功能角色（第 4 节），勾勒出 agent memory 相对静态的概念框架。然而，这种静态视角忽视了根本上刻画 agentic memory 的内在动态性。不同于静态编码在模型参数或固定数据库中的知识，agentic memory 系统能够动态构造与更新其 memory store，并针对不同查询执行定制化 retrieval。这种自适应能力对于 agent 自我演化与终身学习至关重要。

据此，本节考察从静态存储到动态 memory 管理与利用的范式转变。这一范式转变体现了 agentic memory 相对静态数据库方法的基础性操作优势。在实践中，agentic memory 系统可基于 reasoning trace 与环境反馈自主抽取精炼、可泛化的知识。通过将新抽取的知识与既有 memory base 动态融合并更新，系统确保持续适应演化环境并缓解认知冲突。在已构造的 memory base 之上，系统在精确时刻从指定 memory 模块执行定向 retrieval，从而有效增强 reasoning。为系统分析 memory 系统“如何”运作与演化，我们将完整 memory 生命周期分解为三个基本过程加以考察。图 8 对这一动态 memory 生命周期作了整体刻画，突出 memory formation、evolution 与 retrieval 如何相互作用以支撑自适应、自演化的 agent 行为。
![](../assets/arxiv-2512.13564-fig8.jpg)  
Figure 8 agent memory 的操作动态。我们将完整 memory 生命周期解耦为三个驱动系统适应性与自我演化的基本过程：(1) Memory Formation 通过有选择地识别具有长期效用的模式，将原始交互经验转化为信息稠密的知识单元；(2) Memory Evolution 通过 consolidation、updating 与 forgetting 机制将新 memory 动态整合进既有仓库，确保知识库保持连贯与高效；(3) Memory Retrieval 执行 context-aware 查询以访问特定 memory 模块，从而以精确的信息支撑优化 reasoning 性能。字母序表示 memory 系统内部的操作顺序。

## Three Fundamental Process in Memory Systems

1. Memory Formation（5.1 节）：该过程聚焦于将原始经验转化为信息稠密的知识。memory 系统不是被动记录全部交互历史，而是有选择地识别具有长期效用的信息，例如成功的 reasoning 模式或环境约束。本部分回答的问题是：“如何抽取 memory？”。

2. Memory Evolution（5.2 节）：该过程代表 memory 系统的动态演化。它聚焦于将新形成的 memory 与既有 memory base 整合。通过相关条目的 consolidation、冲突消解与自适应剪枝等机制，系统确保 memory 在持续变化的环境中保持可泛化、连贯且高效。本部分回答的问题是：“如何精炼 memory？”。

3. Memory Retrieval（5.3 节）：该过程决定被 retrieval memory 的质量。以 context 为条件，系统构造任务感知的查询，并使用精心设计的 retrieval 策略访问合适的 memory bank。因此，被 retrieval 的 memory 既在语义上相关，又在功能上对 reasoning 至关重要。本部分回答的问题是：“如何利用 memory？”。

这三个过程并非独立；它们构成相互连接的循环，驱动 memory 系统的动态演化与运作。memory formation 阶段抽取的 memory 在 memory evolution 阶段被整合并更新进既有 memory base。借助前两个阶段构造的 memory base，memory retrieval 阶段实现定向访问以优化 reasoning。反过来，reasoning 结果与环境反馈又回流到 memory formation 以抽取新 insight，并回流到 memory evolution 以精炼 memory base。总体而言，这些组件使 LLM 从静态的条件生成器转变为持续学习并响应变化环境的动态系统。

## 5.1 Memory Formation

我们将 memory formation 定义为将原始 context（例如对话或图像）编码为紧凑知识的过程。memory formation 的必要性源自处理冗长、含噪且高度冗余的原始 context 所固有的扩展性限制。全 context prompting 常常遇到计算开销、难以承受的 memory 足迹，以及在分布外输入长度上的 reasoning 性能退化。为缓解这些问题，近期 memory 系统将关键信息 distillation 为可高效存储、可精确 retrieval 的表示，从而实现更高效、更有效的 inference。

memory formation 并非独立于前几节。依任务类型不同，memory formation 过程有选择地抽取第 3 节所述的不同架构 memory，以实现第 4 节所述相应功能。基于信息压缩的粒度与编码逻辑，我们将 memory formation 过程分为五种不同类型。表 7 汇总了各类别下的代表性方法，比较其子类型、表示形式与关键机制。

Five Categories of Memory Formation Operations

• Semantic Summarization（5.1.1 节）将冗长原始数据变换为紧凑摘要，在过滤冗余的同时保留全局、高层语义信息，以降低 context 开销。

• Knowledge Distillation（5.1.2 节）抽取特定认知资产，范围从事实细节到经验性 planning 策略。

• Structured Construction（5.1.3 节）将无定形源数据组织为显式拓扑表示，例如知识图谱或层级树，以增强 memory 的可解释性并支撑多跳 reasoning。

• Latent Representation（5.1.4 节）将原始经验直接编码为机器原生格式（例如向量 embedding 或 KV state），置于连续 latent 空间之中。

• Parametric Internalization（5.1.5 节）通过参数更新将外部 memory 直接 consolidated 进模型权重空间，有效地将可 retrieval 信息转化为 agent 的内在能力与本能。

尽管我们将这些方法分为五类，我们认为这些 memory formation 策略并不互斥。单一算法可以整合多种 memory formation 策略，并在不同表示之间转换知识（Li et al., 2025l）。
Table 7 memory formation 方法的分类。我们依据 memory formation 操作对方法分类。方法在三个技术维度上分析：(1) Sub-Type 标识具体变体或范围，(2) Representation Form 指定输出格式，(3) Key Mechanism 表示核心算法策略。

<table><tr><td>Method</td><td>Sub-Type</td><td>Representation Form</td><td>Key Mechanism</td></tr><tr><td colspan="4">I. Semantic Summarization</td></tr><tr><td>MemGPT (Packer et al., 2023a)</td><td>Incremental</td><td>Textual Summary</td><td>将新 chunk 合并进工作 context</td></tr><tr><td>Mem0 (Chhikara et al., 2025)</td><td>Incremental</td><td>Textual Summary</td><td>LLM 驱动的摘要</td></tr><tr><td>Mem1 (Zhou et al., 2025b)</td><td>Incremental</td><td>Textual Summary</td><td>RL 优化的摘要（PPO）</td></tr><tr><td>MemAgent (Yu et al., 2025a)</td><td>Incremental</td><td>Textual Summary</td><td>RL 优化的摘要（GRPO）</td></tr><tr><td>MemoryBank (Zhong et al., 2024)</td><td>Partitioned</td><td>Textual Summary</td><td>按日/session 分段</td></tr><tr><td>ReadAgent (Lee et al., 2024a)</td><td>Partitioned</td><td>Textual Summary</td><td>摘要前进行语义聚类</td></tr><tr><td>LightMem (Fang et al., 2025b)</td><td>Partitioned</td><td>Textual Summary</td><td>按主题聚类的摘要</td></tr><tr><td>DeepSeek-OCR (Wei et al., 2025a)</td><td>Partitioned</td><td>Visual Token Mapping</td><td>光学 2D 映射压缩</td></tr><tr><td>FDVS (You et al., 2024)</td><td>Partitioned</td><td>Multimodal Summary</td><td>多源信号整合（字幕/对象）</td></tr><tr><td>LangRepo (Kahatapitiya et al., 2025)</td><td>Partitioned</td><td>Multimodal Summary</td><td>层级式视频片段聚合</td></tr><tr><td colspan="4">II. Knowledge Distillation</td></tr><tr><td>TiM (Liu et al., 2023a)</td><td>Factual</td><td>Textual Insight</td><td>将对话抽象为 thoughts</td></tr><tr><td>RMM (Tan et al., 2025b)</td><td>Factual</td><td>Topic Insight</td><td>将对话抽象为主题化 memory</td></tr><tr><td>MemGuide (Du et al., 2025b)</td><td>Factual</td><td>User Intent</td><td>捕获高层用户意图</td></tr><tr><td>M3-Agent (Long et al., 2025)</td><td>Factual</td><td>Text-addressable Facts</td><td>压缩自我中心视觉观察</td></tr><tr><td>AWM (Wang et al., 2024m)</td><td>Experiential</td><td>Workflow Patterns</td><td>从成功 trajectory 抽取 workflow</td></tr><tr><td> $Mem^p$  (Fang et al., 2025d)</td><td>Experiential</td><td>Procedural Knowledge</td><td>将 gold trajectory distillation 为抽象过程</td></tr><tr><td>ExpeL (Zhao et al., 2024)</td><td>Experiential</td><td>Experience Insight</td><td>对比式反思与成功实践</td></tr><tr><td>R2D2 (Huang et al., 2025c)</td><td>Experiential</td><td>Reflective Insight</td><td>对照 ground truth 反思 reasoning trace</td></tr><tr><td> $H^2R$  (Ye et al., 2025b)</td><td>Experiential</td><td>Hierarchical Insight</td><td>双层反思（Plan 与 Subgoal）</td></tr><tr><td>Memory-R1 (Yan et al., 2025c)</td><td>Experiential</td><td>Textual Knowledge</td><td>RL 训练的 LLMExtract 模块</td></tr><tr><td>Mem-α (Wang et al., 2025p)</td><td>Experiential</td><td>Textual Insight</td><td>可学习的 insight 抽取策略</td></tr><tr><td colspan="4">III. Structured Construction</td></tr><tr><td>KGT (Sun et al., 2024)</td><td>Entity-Level</td><td>User Graph</td><td>将用户偏好编码为节点/边</td></tr><tr><td> $Mem0^q$  (Chhikara et al., 2025)</td><td>Entity-Level</td><td>Knowledge Graph</td><td>基于 LLM 的实体与三元组抽取</td></tr><tr><td>D-SMART (Lei et al., 2025)</td><td>Entity-Level</td><td>Dynamic Memory Graph</td><td>构造符合 OWL 的图</td></tr><tr><td>GraphRAG (Edge et al., 2025)</td><td>Entity-Level</td><td>Hierarchical KG</td><td>社区发现与迭代摘要</td></tr><tr><td>AriGraph (Anokhin et al., 2024)</td><td>Entity-Level</td><td>Semantic+Episodic Graph</td><td>双层（Semantic 节点 + Episodic 链接）</td></tr><tr><td>Zep (Rasmussen et al., 2025)</td><td>Entity-Level</td><td>Temporal KG</td><td>三层图（Episodic、Semantic、Community）</td></tr><tr><td>RAPTOR (Sarthi et al., 2024)</td><td>Chunk-Level</td><td>Tree Structure</td><td>递归 GMM 聚类与摘要</td></tr><tr><td>MemTree (Rezazadeh et al., 2025c)</td><td>Chunk-Level</td><td>Tree Structure</td><td>自底向上插入与摘要更新</td></tr><tr><td>H-MEM (Sun and Zeng, 2025)</td><td>Chunk-Level</td><td>Hierarchical JSON</td><td>自顶向下四级层级组织</td></tr><tr><td>A-MEM (Xu et al., 2025c)</td><td>Chunk-Level</td><td>Networked Notes</td><td>带语义链接的离散 note</td></tr><tr><td>PREMem (Kim et al., 2025b)</td><td>Chunk-Level</td><td>Reasoning Patterns</td><td>跨 session 的 reasoning 模式聚类</td></tr><tr><td>CAM (Li et al., 2025g)</td><td>Chunk-Level</td><td>Hierarchical Graph</td><td>通过复制解耦重叠簇</td></tr><tr><td>G-Memory (Zhang et al., 2025c)</td><td>Chunk-Level</td><td>Hierarchical Graph</td><td>三层图（interaction、query、insight）</td></tr><tr><td colspan="4">IV. Latent Representation</td></tr><tr><td>MemoryLLM (Wang et al., 2024j)</td><td>Textual</td><td>Latent Vector</td><td>可自我更新的 latent embedding</td></tr><tr><td>M+ (Wang et al., 2025n)</td><td>Textual</td><td>Latent Vector</td><td>跨层 long-term memory token</td></tr><tr><td>MemGen (Zhang et al., 2025d)</td><td>Textual</td><td>Latent Token</td><td>latent memory trigger 与 weaver</td></tr><tr><td>ESR (Shen et al., 2024)</td><td>Multimodal</td><td>Latent Vector</td><td>Video-to-Language-to-Vector 编码</td></tr><tr><td>CoMEM (Wu et al., 2025d)</td><td>Multimodal</td><td>Continuous Embedding</td><td>通过 Q-Former 进行视觉-语言压缩</td></tr><tr><td>Mem2Ego (Zhang et al., 2025m)</td><td>Multimodal</td><td>Multimodal Embedding</td><td>将地标语义 embedding 为 latent memory</td></tr><tr><td>KARMA (Wang et al., 2025r)</td><td>Multimodal</td><td>Multimodal Embedding</td><td>混合 long/short-term memory 编码</td></tr><tr><td colspan="4">V. Parametric Internalization</td></tr><tr><td>MEND (Mitchell et al., 2022)</td><td>Knowledge</td><td>Gradient Decomposition</td><td>用于快速编辑的辅助网络</td></tr><tr><td>ROME (Meng et al., 2022)</td><td>Knowledge</td><td>Model Parameters</td><td>因果追踪与秩一更新</td></tr><tr><td>MEMIT (Meng et al., 2023)</td><td>Knowledge</td><td>Model Parameters</td><td>通过残差分布进行批量编辑</td></tr><tr><td>CoLoR (Wistuba et al., 2023)</td><td>Knowledge</td><td>LoRA Parameters</td><td>低秩 adapter 训练</td></tr><tr><td>ToolFormer (Schick et al., 2023)</td><td>Capability</td><td>Model Parameters</td><td>对 API 调用做监督 fine-tuning</td></tr></table>

## 5.1.1 Semantic Summarization

Semantic summarization 将原始观察数据变换为紧凑且语义丰富的摘要。所得摘要捕获原始数据的全局、高层信息，而非具体的事实或经验细节（Zhao et al., 2024; Anokhin et al., 2024）。此类摘要的典型示例包括文档的整体叙事（Kim and Kim, 2025; Yu et al., 2025a）、任务的程序性流程（Ye et al., 2025a; Zhang et al., 2025r），或用户的历史画像（Zhang, 2024; Westhäußer et al., 2025）。通过过滤冗余内容并保留任务相关的全局语义，semantic summarization 为后续 reasoning 提供高层指导蓝图，且不引入过多 context 开销。为实现这些效果，压缩过程可以两种主要方式实现：incremental 与 partitioned semantic summarization。

Incremental Semantic Summarization 这一范式采用时间整合机制，将新观察到的信息持续融合进既有摘要，产生全局语义的演化表示。这种逐 chunk 的范式支持增量学习（McCloskey and Cohen, 1989），规避全序列处理的 $O ( n ^ { 2 } )$ 计算负担（Yu et al., 2025a），并促进向全局语义的逐步收敛（Chen et al., 2024b）。MemGPT（Packer et al., 2023a）与 Mem0（Chhikara et al., 2025）等早期实现直接在适当时刻将新 chunk 与既有摘要合并，仅依赖 LLM 固有的摘要能力。然而，这种做法受模型有限容量的制约，常导致不一致或语义漂移。为缓解这些问题，Chen et al.（2024b）与 Wu et al.（2025i）引入外部评估器过滤冗余或不连贯内容，分别使用基于卷积的判别器做一致性验证，以及使用 DeBERTa（He et al., 2020）过滤琐碎内容。后续方法如 Mem1（Zhou et al., 2025b）与 MemAgent（Yu et al., 2025a）不再依赖辅助网络，而是通过带 PPO（Schulman et al., 2017）与 GRPO（Shao et al., 2024）的 reinforcement learning 增强 LLM 自身的摘要能力。

随着 incremental summarization 从启发式融合推进到过滤式整合、再到基于学习的优化，摘要能力日益内化于模型之中，从而减少跨迭代的累积误差。尽管如此，串行更新的性质仍带来计算瓶颈（Fang et al., 2025b）与潜在的信息 forgetting，这促使 partitioned semantic summarization 方法的发展。

Partitioned Semantic Summarization 这一范式采用空间分解机制，将信息划分为不同语义分区，并为每个分区生成单独摘要。早期研究通常采用启发式分区策略处理长 context。MemoryBank（Zhong et al., 2024）与 COMEDY（Chen et al., 2025d）以每一天或每个 session 为基本单位，对长期对话进行摘要与聚合。沿结构维度，Wu et al.（2021）与 Bailly et al.（2025）通过将长文档切分为章节或段落，生成“摘要的摘要”。这类方法虽直观，却常受分区之间语义不连续的困扰。为解决该问题，ReadAgent（Lee et al., 2024a）与 LightMem（Fang et al., 2025b）等方法在摘要前引入语义或主题聚类，从而增强 chunk 间连贯性。超越文本压缩，DeepSeek-OCR（Wei et al., 2025a）开创了通过光学 2D 映射压缩长 context 的思路，在 multimodal 场景中实现更高压缩比。在视频 memory 领域，FDVS（You et al., 2024）与 LangRepo（Kahatapitiya et al., 2025）将长视频切分为片段，通过整合字幕、目标检测与场景描述等多源信号生成文本摘要，再层级式聚合为全局长视频故事。

与 incremental summarization 相比，partitioned 方法提供更优效率并捕获更细粒度语义。然而，其对每个子 chunk 的独立处理可能导致跨分区语义依赖的丢失。

Summary Semantic summarization 作为一种有损压缩机制运作，旨在从冗长交互日志中 distillation 出要点。与逐字存储不同，它优先考虑全局语义连贯性而非局部事实精度，将线性流转为紧凑叙事块。semantic summarization 的主要优势是效率：它大幅缩短 context 长度，因而适合长期对话。然而，代价是分辨率损失：具体细节或细微线索可能被抹平，限制其在证据关键任务中的效用。

## 5.1.2 Knowledge Distillation

Semantic summarization 在宏观层面捕获原始数据的全局语义，knowledge distillation 则在更细粒度上运作，从交互 trajectory 或文档中抽取可复用知识。广义上，知识指第 4 节所述各种形式的事实 memory 与经验 memory，取决于任务的基础功能。

Distilling Factual Memory 该过程聚焦于将原始交互与文档转化为关于用户与环境状态的显式陈述性知识。该过程通过保留可验证事实而非瞬时 context，确保 agent 维持一致性与适应性。在用户建模领域，TiM（Liu et al., 2023a）、RMM（Tan et al., 2025c）与 EMem（Zhou and Han, 2025b）等系统采用抽象机制，将对话轮次转化为高层 thoughts 或丰富的基本话语单元，从而保持长期人格连贯性。在用户客观建模方面，MemGuide（Du et al., 2025b）等方法从对话中抽取用户意图描述。在 reasoning 期间，它捕获并更新目标状态，将已确认约束与未决意图分离，以缓解目标漂移。此外，这种 distillation 扩展到 multimodal 环境：ESR（Shen et al., 2024）与 M3-Agent（Long et al., 2025）等 agent 将自我中心视觉观察压缩为关于物体位置与用户日常的文本可寻址事实。进一步地，通过赋予 agent multimodal 理解能力，Video-RAG（Luo et al., 2025b）将视频中的音频、字幕与物体转化为文本笔记，即 factual memory，以增强长视频理解。

Distilling Experiential Memory 该过程聚焦于从历史 trajectory 中抽取任务执行背后的策略。通过从成功 rollout 中提炼 planning 原则、从失败中提炼纠正信号，这一范式增强 agent 在特定任务上的问题求解能力。通过抽象与泛化，它进一步支撑跨任务知识迁移。因此，经验泛化使 agent 能持续精炼能力并迈向终身学习。

这一研究方向旨在从成功与失败 trajectory 中提炼高层 planning 策略与关键 insight。部分方法聚焦基于成功的 distillation：AgentRR（Feng et al., 2025）与 AWM（Wang et al., 2024m）等系统从成功案例中总结整体任务 plan。Mem<sup>p</sup>（Fang et al., 2025d）分析并总结训练集中的 gold trajectory，将其 distillation 为抽象程序性知识。另一些方法采用失败驱动的反思，例如 Matrix（Liu et al., 2024）、SAGE（Liang et al., 2025）与 R2D2（Huang et al., 2025c），将 reasoning trace 与 ground-truth 答案对照，以定位错误来源并抽取反思性 insight。结合两者，ExpeL（Zhao et al., 2024）、From Experience to Strategy（Xia et al., 2025）与 ReMe（Cao et al., 2025b）对比成功与失败经验，以揭示整体 planning insight。

然而，先前工作主要聚焦于总结任务级 planning 知识，缺乏细粒度、步骤级 insight。为补足这一空白，H<sup>2</sup>R（Ye et al., 2025b）引入双层反思机制：它沿用 ExpeL 构造高层 planning insight 池，同时进一步按子目标序列切分 trajectory，以提炼步骤级执行 insight。

早期方法依赖固定 prompt 进行 insight 抽取，使其性能对 prompt 设计与底层 LLM 能力敏感。近来，可训练的 distillation 方法日益流行。Learn-to-Memorize（Zhang et al., 2025u）为不同 agent 优化任务特定 prompt。另一方面，Memory-R1（Yan et al., 2025c）使用 LLMExtract 模块获取经验与事实知识，而仅训练后续融合组件以将这些输出整合进 memory bank。尽管这些方法采用端到端框架，它们在增强 LLM 自身 distillation insight 的内在能力方面仍显不足。为克服这一限制，Mem-α（Wang et al., 2025p）显式训练 LLM 抽取何种 insight 以及如何保存它们。

Summary 本部分聚焦于从原始 context 中抽取功能特定的知识，而不涉及 memory 存储的结构。每条知识可视为一个 flat memory 单元。仅仅将多个单元存入无结构表格，会忽略其间的语义与层级关系。为此，memory formation 过程可应用结构化规则提炼 insight，并将其存入层级架构。简单但基础，此处介绍的单一 knowledge distillation 方法构成更复杂、更结构化 memory formation 机制的基础组件。

## 5.1.3 Structured Construction

Semantic Summarization（5.1.1 节）与 Knowledge Distillation（5.1.2 节）虽在不同粒度层级有效压缩摘要与知识，却常将 memory 视为孤立单元。相比之下，Structured Construction 将无定形数据转化为有组织的拓扑表示。该过程不只是存储格式的改变，而是决定信息如何连接与分层的主动结构操作。不同于非结构化纯文本摘要，结构化抽取显著增强可解释性与 retrieval 效率。关键在于，这种结构先验擅长捕获多跳 reasoning 任务中的复杂逻辑与依赖，相较传统 retrieval-augmented 方法具显著优势。

依据底层结构推导的操作粒度，我们将现有方法分为两种范式：Entity-Level Construction 通过将文本原子化为实体与关系来构建底层拓扑；Chunk-Level Construction 通过组织完整文本片段或 memory 项来构建结构。

Entity-Level Construction 该范式的基础结构源自关系三元组抽取，将原始 context 分解为最细粒度的语义原子实体与关系。传统方法将 memory 建模为平面知识图谱。例如，KGT（Sun et al., 2024）引入实时个性化机制，将用户偏好与反馈直接编码为用户专属知识图谱中的节点与边。类似地，Mem0<sup>g</sup>（Chhikara et al., 2025）在抽取阶段利用 LLM 将对话消息直接转化为实体与关系三元组。

然而，这些直接抽取方法常受 LLM 固有能力限制，可能引入噪声或结构错误。为提升所构造图的质量，D-SMART（Lei et al., 2025）采用精炼方案：先用 LLM 将核心语义内容 distillation 为简洁、断言式自然语言陈述，再通过神经符号 pipeline 抽取符合 OWL 的知识图谱片段。此外，Ret-LLM（Modarressi et al., 2023）对 LLM 应用监督 fine-tuning，使其能与关系图进行更稳健的读写交互。

上述方法聚焦平面结构，近期进展则转向构造层级 memory 以捕获高层抽象。例如，GraphRAG（Edge et al., 2025）从源文档推导实体知识图谱，并应用社区发现算法抽取图社区并迭代生成社区摘要。这种层级方法识别实体间更高层簇关联，从而抽取泛化 insight，并支持不同粒度上的灵活 retrieval。

为更好地反映原始数据的内部连贯性与时间信息，一些工作通过引入 episodic graph 扩展语义知识图谱。AriGraph（Anokhin et al., 2024）与 HippoRAG（Gutierrez et al., 2024）建立由 semantic graph 与 episodic graph 构成的双层结构。它们从对话中抽取语义三元组，同时连接同时出现的节点或建立节点–段落索引。Zep（Rasmussen et al., 2025）进一步将其形式化为三层时间图架构：episodic 子图（G ）通过双时间模型记录原始消息的发生与处理时间，semantic 子图（G ）记录实体与有时间边界的事实，community 子图（G ）对实体进行高层聚类与摘要。

Chunk-Level Construction 该范式将连续文本跨度或离散 memory 项视为节点，在保留局部语义完整性的同时将其组织为拓扑结构。该领域的演进从对固定语料的静态、平面（2D）抽取，推进到随传入 trajectory 的动态适应，最终走向层级（3D）架构。

早期方法聚焦将固定文本库组织为静态平面结构。HAT（A et al., 2024）通过切分长文本并逐步聚合摘要来构造层级树。类似地，RAPTOR（Sarthi et al., 2024）使用 UMAP 降维与高斯混合模型软聚类递归聚类文本 chunk，并迭代摘要这些簇以形成树。然而，这些静态方法缺乏处理流式数据的灵活性，除非付出高昂的重构成本。

为此，动态平面方法在新 trajectory 到达时增量构建 memory 结构，其差异在于基础元素。基于原始文本的方法包括 MemTree（Rezazadeh et al., 2025c）与 H-MEM（Sun and Zeng, 2025）。MemTree 采用自底向上方式：新文本片段 retrieval 最相似节点，并作为子节点插入或迭代插入子树，触发所有父节点自底向上的摘要更新。相反，H-MEM 采用自顶向下策略，prompt LLM 将数据组织为四级 JSON 层级，涵盖 domain、category、memory trace 与 episode 层。另一种思路是，A-MEM（Xu et al., 2025c）与 PREMem（Kim et al., 2025b）聚焦于重组已抽取的 memory 项。A-MEM 将知识总结为离散 note，并链接相关 note 以构造网络化 memory。PREMem 对抽取的事实、经验与主观 memory 聚类，以识别并存储更高维的跨 session reasoning 模式。

近期进展越过平面布局以构造层级结构，提供更丰富的语义深度。SGMem（Wu et al., 2025h）使用 NLTK 将文本切分为句子，在所有句子节点上形成 KNN 图，随后调用 LLM 抽取每段对话对应的摘要、事实与 insight，从而构造层级。为支持流式数据到达时的层级结构增量构建，CAM（Li et al., 2025g）依据语义相关性与叙事连贯性在文本块之间建立边。它迭代摘要 ego graph，并通过节点复制显式解耦重叠簇来处理新 memory 插入。在多 agent 场景中，G-memory（Zhang et al., 2025c）通过维护三张不同图来扩展这一动态 3D 方法：用于原始聊天历史的 interaction graph、用于特定任务的 query graph，以及 insight graph。该结构使每个 agent 能获得不同粒度层级的定制 memory。

Summary Structured construction 的主要优势是可解释性与处理复杂关系查询的能力。此类方法捕获 memory 元素间错综的语义与层级关系，支撑多步依赖上的 reasoning，并便于与符号或基于图的 reasoning 框架整合。然而，其劣势是 schema 刚性：预定义结构可能无法表示细微或歧义信息，且抽取与维护成本通常很高。

## 5.1.4 Latent Representation

前几章聚焦于如何构建 token-level memory；本部分聚焦于将 memory 编码为机器原生的 latent 表示。Latent representation 将原始经验编码为驻留于 latent 空间的 embedding。不同于 semantic compression 与 structured extraction 在 embedding 为向量之前先摘要经验，latent encoding 本身就将经验存储于 latent 空间，从而减少摘要与文本 embedding 过程中的信息损失。此外，latent encoding 更利于机器认知，可实现跨不同模态的统一表示，并确保 memory 表示的密度与语义丰富性。

Textual Latent Representation KV cache 最初虽为加速 inference 而设计，在 memory 语境中也可视为一种 latent 表示（Li et al., 2025c; Jiang et al., 2025b）。它利用额外 memory 存储过往信息，从而避免冗余计算。MEMORYLLM（Wang et al., 2024j）与 M+（Wang et al., 2025n）将 memory 表示为可自我更新的 latent embedding，在 inference 期间注入 transformer 层。此外，MemGen（Zhang et al., 2025d）引入 memory trigger 以监控 agent 的 reasoning 状态并决定何时显式调用 memory，以及 memory waiver，利用 agent 当前状态构造 latent token 序列。该序列充当机器原生 memory，增强 agent 的 reasoning 能力。

Multimodal Latent Representation 在 multimodal memory 研究中，CoMEM（Wu et al., 2025d）通过 Q-Former 将视觉-语言输入压缩为固定长度 token，实现稠密、连续的 memory，并支持无限 context 长度的即插即用。Encode-Store-Retrieve（Shen et al., 2024）使用 Ego-LLaVA 将自我中心视频帧转换为语言编码，随后通过 embedding 模型转化为向量表示。尽管采用 embedding 模型以确保语义对齐，这些方法常面临压缩损失与计算开销之间的取舍，尤其是在处理长 context 序列中的梯度流时。

与具身智能整合时，multimodal latent memory 可融合来自多个传感器的数据。例如，Mem2Ego（Zhang et al., 2025m）动态地将全局 context 信息与局部感知对齐，将地标语义 embedding 为 latent memory，以增强 long-horizon 任务中的空间 reasoning 与决策。KARMA（Wang et al., 2025r）采用混合 long-term 与 short-term memory 形式，将物体信息编码为 multimodal embedding，在即时响应性与一致表示之间取得平衡。这些探索凸显了 latent encoding 在跨模态提供统一且语义丰富表示方面的优势。

Summary Latent representation 绕过人类可读格式，将经验直接编码为机器原生向量或 KV-cache。这种高密度格式保留了可能在文本解码中丢失的丰富语义信号，实现与模型内部计算更顺畅的整合，并天然支持 multimodal 对齐。然而，它受不透明性困扰。latent memory 是黑箱，使人类难以调试、编辑或验证其存储的知识。

## 5.1.5 Parametric Internalization

随着 LLM 越来越多地纳入 memory 系统以支持长期适应，一个核心研究问题是这些外部 memory 应如何 consolidated 为 parametric 形式。上文讨论的 latent representation 方法将 memory parametric 于模型外部，parametric internalization 则直接调整模型内部参数。它利用模型通过所学参数空间编码与泛化信息的能力。这一范式从根本上增强模型的内在能力，消除外部存储与 retrieval 的开销，并无缝支持持续更新。如第 4 节所述，并非所有 memory 内容承担相同功能：一些条目提供陈述性知识，另一些编码塑造 agent reasoning 与行为的程序性策略。这一区分促使对 memory internalization 采取更细粒度的视角，将其分为 knowledge internalization 与 capability internalization。

Knowledge Internalization 该策略将外部存储的事实 memory（例如概念定义或领域知识）转化为模型参数空间。通过这一过程，模型可直接回忆并利用这些事实，而无需依赖显式 retrieval 或外部 memory 模块。在实践中，knowledge internalization 通常通过模型编辑实现（Sinitsin et al., 2020; De Cao et al., 2021）。早期工作 MEND（Mitchell et al., 2022）引入辅助网络，通过分解 fine-tuning 梯度实现快速单步编辑，从而最小化对无关知识的干扰。沿此路线，ROME（Meng et al., 2022）精炼编辑过程，使用因果追踪精确定位存储特定事实的 MLP 层，并应用秩一更新以更高精度与更好泛化注入新信息。MEMIT（Meng et al., 2023）进一步支持批量编辑，通过多层残差分布与批量公式同时更新数千条事实，大幅提升可扩展性。随着 LoRA（Hu et al., 2022）等参数高效范式的兴起，knowledge internalization 可通过轻量 adapter 而非直接修改参数完成。例如，CoLoR（Wistuba et al., 2023）冻结预训练 Transformer 参数，仅训练小型 LoRA adapter 以内化新知识，避免全参数 fine-tuning 的高成本。尽管有这些进展，这些方法仍可能产生 of-target 效应（De Cao et al., 2021），并在持续学习场景中易受灾难性 forgetting 影响。

Capability Internalization 该策略寻求将经验性知识（例如程序性专长或策略启发）embedding 进模型参数空间。该范式在广义上代表一种 memory formation 操作，从获取事实知识转向内化经验能力。具体而言，这些能力包括领域特定解法 schema、策略性 planning，以及 agentic skill 的有效部署等。技术上，capability internalization 通过从 reasoning trace 学习来实现，可采用监督 fine-tuning（Wei et al., 2022; Zelikman et al., 2022; Schick et al., 2023; Mukherjee et al., 2023）或偏好引导的优化方法，如 DPO（Rafailov et al., 2023; Tunstall et al., 2023; Yuan et al., 2024c; Grattafiori et al., 2024）与 GRPO（Shao et al., 2024; DeepSeek-AI et al., 2025）。作为整合外部 RAG 与 parametric 训练的尝试，Memory Decoder（Cao et al., 2025a）是一种即插即用方法：它像外部 RAG 一样不修改基础模型，却通过消除外部 retrieval 开销达到参数内化的 inference 速度。此类即插即用的 parametric memory 可能具有广泛潜力。

Summary Parametric internalization 代表 memory 的终极 consolidation：外部知识经由梯度融合进模型权重。这将范式从 retrieval 信息转向拥有能力，类似生物学的 long-term potentiation。当知识变得如同本能，访问是零延迟的，模型可立即响应而无需查询外部 memory。然而，该方法面临若干挑战，包括灾难性 forgetting 与高更新成本。与外部 memory 不同，parametric 内化难以精确修改或移除而不产生意外副作用，限制了灵活性与适应性。

## 5.2 Memory Evolution

5.1 节介绍的 Memory Formation 从原始数据抽取 memory。下一个重要步骤是将新抽取的 memory 与既有 memory 仓库整合，使 memory 系统得以动态演化。朴素策略是简单地将新条目追加到既有 memory bank。然而，这忽视了 memory 条目间的语义依赖与潜在矛盾，也忽略了信息的时间有效性。为应对这些局限，我们引入 Memory Evolution。该机制将新 memory 与既有 memory consolidated，以综合高层 insight、消解逻辑冲突并剪除过时数据。通过确保长期知识的紧凑性、一致性与相关性，该方法使 memory 系统能够随环境与任务演化而调整其认知过程与 context 理解。

依据 memory evolution 的目标，我们将其分为以下机制：

Three Mechanisms of Memory Evolution

• Memory Consolidation（5.2.1 节）合并新 memory 与既有 memory 并执行反思性整合，形成更泛化的 insight。这确保学习是累积的而非孤立的。

• Memory Updating（5.2.2 节）消解新 memory 与既有 memory 间的冲突，修正并补充仓库以维持准确性与相关性。它使 agent 能适应环境或任务需求的变化。

• Memory Forgetting（5.2.3 节）移除过时或冗余信息，释放容量并提升效率。这防止知识过载导致性能退化，并确保 memory 仓库聚焦于可行动且当前的知识。

这些机制共同维持 memory 仓库的泛化性、准确性与时效性。通过主动管理 memory evolution，这些机制凸显 memory 系统的 agentic 能力，促进持续学习与自主自我改进。图 9 提供这些 memory evolution 机制的统一视图，说明其在共享 memory 数据库中的运作角色与代表性框架。

## 5.2.1 Consolidation

Memory consolidation 旨在将新获得的短期 trace 转化为结构化、可泛化的长期知识。其核心机制是识别新 memory 与既有 memory 间的语义关系，并将其整合为更高层抽象或 insight。该过程有两个主要目的。第一，它将碎片化信息重组为连贯结构，防止短期保持期间关键细节丢失，并促成稳定知识 schema 的形成。第二，通过对经验数据抽象、压缩与泛化，consolidation 从具体事件中提炼可复用模式，产生支持跨任务泛化的 insight。

一个核心挑战是确定新 memory 应与既有 memory 在何种粒度上匹配与合并。先前工作覆盖从局部内容合并到簇级融合、再到全局整合的一系列 consolidation 策略。

Local Consolidation 该操作聚焦涉及高度相似 memory 片段的细粒度更新。在 RMM（Tan et al., 2025c）中，每条新主题 memory retrieval top-K 最相似候选，由 LLM 判定合并是否合适，从而降低错误泛化风险。在 multimodal 设定中，VLN（Song et al., 2025b）在容量饱和时触发池化机制。它识别最相似或冗余的 memory 对，并将其压缩为更高层抽象。这些方法精炼细节知识，同时保留 memory store 的全局结构，提升精度与存储效率。然而，它们无法完全捕获簇级关系，或跨语义相关 memory 涌现的高阶依赖。
![](../assets/arxiv-2512.13564-fig9.jpg)  
Figure 9 Memory Evolution 机制的图景。我们将演化过程分为三个分支，共同维护中心 Memory Database：(a) Consolidation 通过 local consolidation、cluster fusion 与 global integration 处理原材料以综合 insight；(b) Updating 通过对外部数据库执行冲突消解、对内部模型应用参数更新来确保准确性与一致性；(c) Forgetting 依据特定准则剪枝数据以优化效率：时间过期、低访问频率与低信息价值。外环展示与每种演化机制相关的代表性框架与 agent。

Cluster-level Fusion 随着 memory 增长，采用簇级融合对于捕获跨实例规律至关重要。跨簇方面，PREMem（Kim et al., 2025b）将新 memory 簇与相似既有簇对齐，并应用泛化与精炼等融合模式形成高阶 reasoning 单元，显著提升可解释性与 reasoning 深度。EverMemOS（Hu et al., 2026a）计算新生成的 MemCell 与所有 MemScene 质心的相似度，并将其合并进足够相似的 MemScene。簇内方面，TiM（Liu et al., 2023a）周期性调用 LLM 检查共享同一哈希桶的 memory，并合并语义冗余条目。CAM（Li et al., 2025g）将目标簇内所有节点合并为代表摘要，产生更高层且一致的跨样本表示。这些方法在更广尺度上重组 memory 结构，标志着迈向结构化知识的重要一步。

Global Integration 该操作执行整体 consolidation，以维持全局连贯性，并从累积经验中 distillation 出系统级 insight。与 5.1.1 节相比，semantic summarization 聚焦从既有 context 推导全局摘要，可视为摘要的初始构造。相反，本段强调随额外数据到达，新信息如何整合进既有摘要。对于用户 factual memory，MOOM（Chen et al., 2025e）通过规则处理、embedding 方法与 LLM 驱动抽象，将临时角色快照与历史 trace 整合，构造稳定的角色画像。对于经验 memory，Matrix（Liu et al., 2024）执行迭代优化，将执行 trajectory 与反思性 insight 同全局 memory 结合，distillation 出支持跨场景复用的任务无关原则。随着单步 reasoning context 与环境反馈变长，AgentFold（Ye et al., 2025a）与 Context Folding（Zhang et al., 2025r）等方法内化压缩 working memory 的能力。在包括 web navigation 的多步交互中，这些方法在每一步后自动总结并凝缩全局 context，支撑高效且有效的 reasoning。Global integration 从完整经验历史 consolidated 出高层结构化知识，提供可靠的 context 基础，同时提升泛化性、reasoning 准确性与个性化决策。

Summary Consolidation 是将碎片化短期 trace 重组为连贯长期 schema 的认知过程。它超越简单存储，综合孤立条目间的联系，形成结构化世界观。它增强泛化并减少存储冗余。然而，它存在信息抹平风险：离群事件或独特例外在抽象过程中丢失，可能降低 agent 对异常与特定事件的敏感度。

## 5.2.2 Updating

Memory Update 指 agent 在出现冲突或获得新信息时修订或替换既有 memory 的过程。目标是维持事实一致性与持续适应，而无需完整重训模型。不同于 5.2.1 节所述聚焦抽象与泛化的 memory consolidation，memory update 强调局部修正与同步，使 agent 与演化中的环境保持对齐。

通过持续更新，agentic memory 系统保持知识的准确性与时效性，防止过时信息偏置 reasoning。因此，它是实现终身学习与自我演化的核心机制。依据 memory 驻留位置，更新分为两类：(1) External Memory Update：对外部 memory store 的更新；(2) Model Editing：参数空间内的模型内部编辑。

External Memory Update 向量数据库或知识图谱中的条目在出现矛盾或新事实时被修订。该方法不改动模型权重，而是通过动态修改外部存储维持事实对齐。静态 memory 不可避免地累积过时或冲突条目，导致逻辑不一致与 reasoning 错误。更新外部 memory 可实现轻量修正，同时避免完整重训或重建索引的成本。

External memory update 机制的发展沿一条轨迹推进：从基于规则的纠正，到时间感知的软删除，再到延迟一致性策略，最终到完全学习的更新策略。MemGPT（Packer et al., 2023a）、D-SMART（Lei et al., 2025）与 Mem0<sup>g</sup>（Chhikara et al., 2025）等早期系统采用直接 pipeline：LLM 检测新信息间的冲突，然后调用 replace 或 delete 操作更新 memory。这些系统对基本事实修复有效，却依赖破坏性替换，抹除有价值的历史 context 并破坏时间连续性。为解决该问题，Zep（Rasmussen et al., 2025）引入时间标注，用无效时间戳标记冲突事实而非删除，从而同时保留语义一致性与时间完整性。这标志着从硬替换转向软性的、时间感知的更新。然而，在高频交互下，实时更新造成显著计算与 I/O 负担。因此，MOOM（Chen et al., 2025e）与 LightMem（Fang et al.,

2025b）引入双阶段更新：先进行软性在线更新以保证实时响应，随后进入离线反思性 consolidation 阶段，在其中合并相似条目并通过 LLM reasoning 消解冲突。这一最终一致性范式平衡了延迟与连贯性。随着 agentic reinforcement learning 成熟，通过 reinforcement learning 增强 LLM 内在的 memory 更新决策成为可能。Mem-α（Wang et al., 2025p）将 memory 更新表述为策略学习问题，使 LLM 学习何时、如何以及是否更新，从而在稳定性与新鲜度之间实现动态权衡。

总体而言，外部 memory 更新已从手动触发的纠正转向自我调节、时间感知的学习过程，通过 LLM 驱动的 retrieval、冲突检测与修订来维持事实一致性与结构稳定性。

Model Editing 模型编辑在模型参数空间内执行直接修改，以在不完整重训的情况下纠正或注入知识，代表隐式知识更新。重训成本高且易导致灾难性 forgetting。模型编辑可实现精确、低成本修正，增强适应性与内部知识保持。

模型编辑方法分为两大类。(1) 显式定位与修改：ROME（Tan et al., 2025b）通过梯度追踪识别编码特定知识的参数区域，并执行定向权重更新；Model Editor Networks（Tang et al., 2025c）训练辅助元编辑器网络以预测最优参数调整。(2) latent 空间自我更新：MEMORYLLM（Xu et al., 2025c）在 Transformer 层内嵌 memory pool，周期性替换 memory token 以整合新知识；M+（Wang et al., 2025n）维护双层 memory，丢弃过时短期条目并将关键信息压缩进长期存储。
ChemAgent（Tang et al., 2025c）等混合方法进一步将外部 memory 更新与内部模型编辑结合，同步事实与表示变化，以实现快速跨域适应。

Summary 从实现角度看，memory updating 聚焦于新 memory 到达所触发的冲突消解与知识修订，而 memory consolidation 强调新知识与既有知识的整合与抽象。上文讨论的两种 memory updating 策略建立双路径机制：外部数据库中的冲突消解与模型内的参数编辑，使 agent 能执行持续自我纠正并支撑长期演化。关键挑战是稳定性–可塑性困境：判定何时覆盖既有知识、何时将新信息视为噪声。错误更新可能覆盖关键信息，导致知识退化与 reasoning 故障。

## 5.2.3 Forgetting

Memory forgetting 指有意移除过时、冗余或低价值信息，以释放容量并保持对显著知识的聚焦。不同于消解 memory 间冲突的 update 机制，forgetting 优先消除过时信息以确保效率与相关性。随着时间推移，无界 memory 累积导致噪声增加、retrieval 延迟以及过时知识的干扰。受控 forgetting 有助于缓解过载并维持认知聚焦。然而，过度激进的剪枝有抹除罕见但关键知识的风险，损害长 context 中 reasoning 的连续性。

Forgetting 机制可分为 Time-based Forgetting、Frequency-based Forgetting 与 Importance-driven Forgetting，分别对应创建时间、retrieval 活动与综合语义估值。

Time-based Forgetting 时间驱动的 forgetting 仅考虑 memory 的创建时间，随时间逐渐衰减其强度，以模拟人类 memory 的消退。MemGPT（Packer et al., 2023a）在 context 溢出时驱逐最早消息。Xu et al.（2025c）与 Wang et al.（2025n）采用随机 token 替换，替换比例为 K/N，以模拟人类认知中的指数 forgetting；一旦 pool 超过容量，即丢弃最旧条目。不同于显式删除旧 memory，MAICC（Jiang et al., 2025c）通过随时间逐渐衰减 memory 权重实现软 forgetting。该过程映射自然 forgetting，确保持续适应而无历史过载。

Frequency-based Forgetting 频率驱动的 forgetting 依据 retrieval 行为对 memory 排序，保留频繁访问条目而丢弃不活跃条目。XMem（Cheng and Schwing, 2022）采用 LFU 策略移除低频条目；KARMA（Wang et al., 2025r）使用计数 Bloom filter 追踪访问频率；MemOS（Li et al., 2025l）应用 LRU 策略，移除长期未使用项并归档高活跃项。这确保高效的 retrieval 与存储均衡。通过区分创建时间与 retrieval 频率，这两个轴形成更正交的分类：基于时间的衰减捕获自然时间老化，基于频率的 forgetting 反映使用动态，共同维持系统效率与新鲜度。

Importance-driven Forgetting 重要性驱动的 forgetting 整合时间、频率与语义信号，以保留高价值知识并剪除冗余。Zhong et al.（2024）与 Chen et al.（2025e）等早期工作通过时间衰减与访问频率的复合分数量化重要性，实现基于数值的选择性 forgetting。后续方法转向语义级评估：VLN（Song et al., 2025b）通过相似度聚类池化语义冗余 memory，Livia（Xi and Wang, 2025）纳入情绪显著性与 context 相关性，以建模情绪驱动的选择性 forgetting。随着 LLM 判断能力日益强大，TiM（Liu et al., 2023a）与 MemTool（Lumer et al., 2025）利用 LLM 评估 memory 重要性并显式剪除或忘记较不重要的 memory。这一转变反映了从静态数值评分到语义智能的过渡。agent 现在可执行有意识 forgetting，并依据任务 context、语义与情感线索选择性保留最相关的 memory。

Summary 基于时间的衰减反映 memory 的自然时间消退，基于频率的 forgetting 确保对常用 memory 的高效访问，而重要性驱动的 forgetting 引入语义辨别。这三种 forgetting 机制共同治理 agentic memory 如何保持及时、可高效访问且语义相关。然而，LRU 等启发式 forgetting 机制可能消除长尾知识：这些知识很少被访问，却对正确决策至关重要。因此，当存储成本并非关键约束时，许多 memory 系统避免直接删除某些 memory。

上述讨论描述了先前工作如何在不同阶段手工设计 memory 架构，使 agent 的 memory 内容可在线演化。更近期，MemEvolve（Zhang et al., 2025h）提出元演化框架，联合演化 agent 的经验知识与底层 memory 架构，使 memory 框架本身能够持续学习与适应。

## 5.3 Memory Retrieval

在 5.1 节与 5.2 节建立的 memory bank 之上，下一个关键步骤是在 reasoning 期间如何 retrieval 与利用 memory。我们将 memory retrieval 定义为在恰当时刻从特定 memory 仓库 retrieval 相关且简洁的知识片段，以支撑当前 reasoning 任务的过程。关键挑战在于在大规模 memory store 中高效、准确地定位所需知识片段。为此，许多算法采用启发式策略或可学习模型来优化 retrieval 过程的各个阶段。依据 retrieval 的执行顺序，该过程可分解为四个方面。图 10 提供这一 retrieval pipeline 的结构化概览，依据现有方法在各 retrieval 阶段中的角色加以组织。

## Four Steps of Memory Retrieval

• Retrieval Timing and Intent（5.3.1 节）决定 memory retrieval 的具体时刻与目标，从被动、指令驱动的触发转向自主、自我调节的决策。

• Query Construction（5.3.2 节）通过将查询分解或重写为有效 retrieval 信号，弥合用户原始输入与所存 memory 索引之间的语义鸿沟。

• Retrieval Strategies（5.3.3 节）在 memory 仓库上执行搜索，采用从稀疏词汇匹配到稠密语义 embedding、再到结构感知图遍历的多种范式。

• Post-Retrieval Processing（5.3.4 节）通过 re-ranking、过滤与聚合精炼 retrieval 到的原始片段，确保提供给模型的最终 context 简洁且连贯。

这些机制共同将 memory retrieval 从静态搜索操作转变为动态认知过程。retrieval timing 与 intent 决定何时、何处 retrieval。接着，query construction 指定 retrieval 什么，retrieval strategies 聚焦如何执行 retrieval。最后，post-retrieval processing 决定 retrieval 到的信息如何被整合与使用。稳健的 agentic 系统通常将这些组件编排进统一 pipeline，使 agent 能逼近类人的联想 memory 激活，以实现高效知识访问。

## 5.3.1 Retrieval Timing and Intent

retrieval intent 与 timing 决定何时触发 retrieval 机制以及查询哪个 memory store。现有 memory 系统在此采用不同设计选择，从常开 retrieval 到由显式指令或内部信号触发的 retrieval（Zhao et al., 2024; Wang et al., 2025p; Fang et al., 2025b）。例如，MIRIX（Wang and Chen, 2025）对每个查询从全部六个 memory 数据库执行 retrieval 并拼接 retrieval 内容，反映优先全面 memory 访问的设计。其他方法则力求更有选择性地触发 retrieval，允许模型决定 memory 访问的时机与范围，从而更定向、更高效地利用 memory 资源。本小节从两个互补视角回顾文献：自动 retrieval timing 与自动 retrieval intent。

Automated Retrieval Timing 该术语指模型在 reasoning 期间自主决定何时触发 memory retrieval 操作的能力。最简单策略是把决策委托给 LLM 或外部控制器，使其仅凭查询判断 retrieval 是否必要。例如，MemGPT（Packer et al., 2023a）与 MemTool（Lumer et al., 2025）允许 LLM 自身调用 retrieval 函数，在类操作系统框架内高效访问外部 memory。然而，这些方法依赖仅凭查询的静态判断，忽视模型 reasoning 期间动态演化的认知状态。

为补足这一局限，近期工作将快–慢思考机制整合进 retrieval timing。例如，ComoRAG（Wang et al., 2025f）与 PRIME（Tran et al., 2025）先生成快速响应，再让 agent 评估其充分性。若初始 reasoning 被视为不足，系统基于失败反馈触发更深的 retrieval 与 reasoning。MemGen（Zhang et al., 2025d）进一步精炼触发机制，将显式 agent 级决策转化为 latent、可训练的过程。它引入 memory trigger，从 latent rollout 状态检测关键 retrieval 时刻，从而在保持端到端可微性的同时提升 retrieval timing 的精度。

Automated Retrieval Intent 该方面涉及模型在层级存储形式内自主决定访问哪个 memory 源的能力。例如，AgentRR（Feng et al., 2025）依据环境反馈在低层程序模板与高层经验抽象之间动态切换。然而，其依赖显式反馈，限制了在开放式 reasoning 设定中的适用性。

![](../assets/arxiv-2512.13564-fig10.jpg)  
Figure 10 agentic 系统中 memory retrieval 方法学的分类。该思维导图将现有文献组织为 retrieval pipeline 的四个不同阶段：Timing and Intent，治理过程的启动；Query Construction，涵盖查询分解与重写技术；Retrieval Strategies，将搜索范式分为词汇、语义、基于图与混合方法；Post-Retrieval Processing，聚焦通过 re-ranking、过滤与聚合精炼输出。

为克服这一约束，MemOS（Li et al., 2025l）采用 MemScheduler，基于用户级、任务级或组织级 context 在 parametric、activation 与 plaintext memory 之间动态选择。然而，这种扁平选择方案忽视 memory 系统的层级结构。H-MEM（Sun and Zeng, 2025）通过引入基于索引的路由机制来应对：执行由粗到细的 retrieval，从 domain 层移动到 episode 层，逐步将搜索空间收窄至最相关子 memory。这种层级路由不仅提升 retrieval 精度，也缓解信息过载。

Summary 自主 timing 与 intent 有助于降低计算开销并抑制不必要噪声，但也带来潜在脆弱性。当 agent 高估其内部知识、在需要时未能启动 retrieval，系统可能陷入静默失败模式：知识空白可能导致幻觉输出。因此，需要取得平衡：在恰当时刻向 agent 提供必要信息，同时避免引入噪声的过度 retrieval。

## 5.3.2 Query Construction

启动 retrieval 过程后，下一个挑战在于将原始查询转化为与 memory 索引对齐的有效 retrieval 信号。Query construction 充当用户表层话语与 memory latent 存储之间的翻译层。传统方法通常直接基于用户查询执行 retrieval，简单却无法使查询语义与 memory 索引语义对齐。为弥合这一鸿沟，agentic memory 系统主动执行 query decomposition 或 query rewriting，生成更匹配 memory latent 结构的中间 retrieval 信号。

Query Decomposition 该方法将复杂查询分解为更简单的子查询，使系统能 retrieval 更细粒度、更相关的信息。这种分解通过对中间结果进行模块化 retrieval 与 reasoning，缓解一次性 retrieval 的瓶颈。例如，Visconde（Pereira et al., 2023）与 ChemAgent（Tang et al., 2025c）利用 LLM 将原问题分解为子问题，从 memory 为每个子问题 retrieval 候选结果，最后聚合为连贯答案。然而，这些方法缺乏全局 planning。为此，PRIME（Tran et al., 2025）与 MA-RAG（Nguyen et al., 2025）受 ReAct（Yao et al., 2023b）范式启发引入 Planner Agent，先制定全局 retrieval plan，再分解为子查询。但这些方法主要依赖问题驱动的分解，因而无法显式识别模型缺失何种具体知识。为使子查询更有针对性，Agent KB（Tang et al., 2025d）采用两阶段 retrieval：教师模型观察学生模型的失败，并据此生成细粒度子查询。这种定向分解提升 retrieval 精度并减少无关结果，在知识密集任务中尤为明显。

Query Rewriting 该策略不进行分解，而是在 retrieval 前重写原始查询或生成假设文档以精炼其语义。此类重写缓解用户意图与 memory 索引之间的错配。例如，HyDE（Gao et al., 2023b）指示 LLM 以零样本方式生成假设文档，并使用其语义 embedding 执行 retrieval。生成的文档封装了期望语义，有效桥接用户查询与目标 memory。MemoRAG（Qian et al., 2025）扩展这一思路，将全局 memory 纳入假设文档生成。它先压缩全局 memory，再以查询与压缩 memory 为条件生成草稿答案；该草稿随后用作重写查询。由于草稿可访问全局 memory context，它更忠实地捕获用户意图并揭示隐式信息需求。类似地，MemGuide（Du et al., 2025b）利用对话 context prompt LLM 生成简洁、命令式短语，作为 retrieval 的高层意图描述。除了直接 prompt LLM 重写查询，Rewrite-Retrieve-Read（Ma et al., 2023b）通过 reinforcement learning 训练小型语言模型作为专用 rewriter，而 ToC（Kim et al., 2023a）采用 Tree of Clarifications 逐步精炼并明确用户的 retrieval 目标。

Summary 分解与重写这两种范式并不互斥。Auto-RAG（Kim et al., 2024a）在相同 retrieval 条件下评估 HyDE 与 Visconde，再选择给定任务表现最佳的策略，从而整合两者。该工作结果表明，memory-retrieval 查询的质量对 reasoning 性能有实质影响。与早期主要聚焦设计精巧 memory 架构的研究不同，近期研究（Yan et al., 2025b）日益重视 retrieval 构造过程，将 memory 的角色转向服务于 retrieval。以何种内容进行 retrieval，毫不意外地成为该过程的关键组件。

## 5.3.3 Retrieval Strategies

厘清 retrieval 目标后，我们获得一个意图明确的查询。下一个核心挑战在于利用该查询，从大型复杂 memory 仓库中高效、准确地 retrieval 真正相关的知识。Retrieval strategies 充当查询与 memory base 之间的桥梁，其设计直接决定 retrieval 效率与结果质量。本节系统回顾各种 retrieval 范式并分析其优势、局限与应用场景——从基于关键词匹配的传统稀疏 retrieval，到使用语义 embedding 的现代稠密 retrieval，到面向结构化知识的基于图的 retrieval，到新兴的生成式 retrieval 方法，最后到整合多种范式的混合 retrieval 技术。

Lexical Retrieval 该策略依赖关键词匹配定位相关文档，代表性方法包括 TF-IDF（SPARCK JONES, 1972）与 BM25（Robertson and Zaragoza, 2009）。TF-IDF 依据词频与逆文档频率衡量关键词重要性，实现快速且可解释的 retrieval。BM25 通过引入词频饱和与文档长度归一化进一步精炼该方法。此类方法常用于精度导向的 retrieval 场景，其中结果的准确性与相关性优先于召回（Tang et al., 2025d; Wang et al., 2025p; Pan et al., 2025）。然而，纯词汇匹配难以捕获语义变化与 context 关系，对语言表达差异高度敏感，因而在开放域知识或 multimodal memory 设定中效果较差。

Semantic Retrieval 该策略将查询与 memory 条目编码到共享 embedding 空间，并基于语义相似度而非词汇重叠进行匹配。代表性方法采用语义编码器，包括 Sentence-BERT（Reimers and Gurevych, 2019）与 CLIP（Radford et al., 2021）。在 memory 系统中，该方法更好地捕获任务 context，并支持语义泛化与模糊匹配，成为多数 agentic memory 框架的默认选择（Lewis et al., 2020; Wang et al., 2024b; Yang et al., 2024a; Xu et al., 2025c; Tan et al., 2025c; Nguyen et al., 2025; Qian et al., 2025; Hassell et al., 2025; Huang et al., 2025c）。然而，语义漂移与强制 top-K retrieval 常引入 retrieval 噪声与虚假召回。为此，近期系统纳入动态 retrieval 策略、reranking 模块与混合 retrieval 方案。

Graph Retrieval 该策略不仅利用语义信号，还利用图的显式拓扑结构，使 retrieval 本质上更精确且结构感知。通过直接访问结构路径，这些方法展现更强的多跳 reasoning 能力，并能更有效地探索长程依赖。此外，将关系结构视为 inference 路径上的约束，天然支持由精确规则与符号约束治理的 retrieval。AriGraph（Anokhin et al., 2024）、EMG-RAG（Wang et al., 2024l）、Mem0<sup>g</sup>（Chhikara et al., 2025）与 SGMem（Wu et al., 2025h）等代表性方法先识别最相关节点或三元组，再扩展到其语义相关的 K-hop 邻居以构造 ego-graph。HippoRAG（Gutierrez et al., 2024）在 retrieval 到的节点上执行个性化 PageRank（Page et al., 1999），并按与这些种子节点的接近度对图中其余部分排序，从而实现有效的多跳 retrieval。超越固定扩展规则，CAM（Li et al., 2025g）与 D-SMART（Lei et al., 2025）采用 LLM 引导子图探索：CAM 使用 LLM 为中心节点选择信息丰富的邻居与子节点进行联想探索，D-SMART 则将 LLM 视为 planner，在 KG memory 上执行 beam search，以 retrieval 目标实体的一跳邻居以及连接给定实体对的关系。对于时间图，Zep（Rasmussen et al., 2025）与 MemoTime（Tan et al., 2025b）进一步支持显式时间约束下的实体-子图构造与关系 retrieval，确保返回结果满足所需时间规则。

Generative Retrieval 该策略以直接生成相关文档标识符的模型取代词汇或语义 retrieval（Tay et al., 2022; Wang et al., 2022b）。通过将 retrieval 表述为条件生成任务，模型将候选文档隐式存储于参数中，并在解码期间执行深度查询–文档交互（Li et al., 2025k）。借助预训练语言模型的语义能力，该范式常优于传统 retrieval 方法，尤其在小规模设定中（Zeng et al., 2024）。然而，生成式 retrieval 需要额外训练以内化所有候选文档的语义，当语料演化时可扩展性受限（Yuan et al., 2024b）。因此，agentic memory 系统对这一范式关注相对较少，尽管其生成与 retrieval 的紧耦合暗示着尚未发掘的潜力。

Hybrid Retrieval 该策略整合多种 retrieval 范式的优势。Agent KB（Tang et al., 2025d）与 MIRIX（Wang and Chen, 2025）等系统结合词汇与语义 retrieval，在精确术语或工具匹配与更广语义对齐之间取得平衡。类似地，Semantic

Anchoring（Chatterjee and Agarwal, 2025）在语义 embedding 与符号倒排索引上执行并行搜索，以实现互补覆盖。另一些方法结合多种评估信号来引导 retrieval。例如，Generative Agents（Kaiya et al., 2023）通过累加新近性、重要性与相关性的评分方案，展示这种多因素方法。MAICC（Jiang et al., 2025c）采用混合效用评分函数，将相似度与全局回报及预测个体回报整合。在基于图的设定中，retrieval 通常分两阶段进行：语义 retrieval 先识别相关节点或三元组，随后利用图拓扑扩展搜索空间（Anokhin et al., 2024; Wang et al., 2024l; Gutierrez et al., 2024; Li et al., 2025g）。

在数据库基础设施层面，MemoriesDB（Ward, 2025）引入面向长期 agent memory 的时间–语义–关系数据库，提供将这些维度整合进统一存储与访问框架的混合 retrieval 架构。

通过融合异构 retrieval 信号，混合方法在保留关键词匹配精度的同时纳入语义方法的 context 理解，最终产生更全面、更相关的结果。

## 5.3.4 Post-Retrieval Processing

初次 retrieval 常返回冗余、含噪或语义不一致的片段。将这些结果直接注入 prompt 可能导致 context 过长、信息冲突，以及被无关内容分散的 reasoning。因此，post-retrieval processing 对确保 prompt 质量至关重要。其目标是将 retrieval 结果 distillation 为简洁、准确且语义连贯的 context。实践中，两个组件居核心：(1) Re-ranking and Filtering：执行细粒度相关性估计，移除无关或过时 memory 并重排剩余片段，从而减少噪声与冗余。(2) Aggregation and Compression：将 retrieval 到的 memory 与原始查询整合，消除重复、合并语义相似信息，并重建紧凑连贯的最终 context。

Re-ranking and Filtering 为维持简洁连贯的 context，初始 retrieval 结果被重排与过滤，通过移除低相关项来确保 context 简洁连贯。早期方法依赖启发式准则评估语义一致性。例如，Semantic Anchoring（Chatterjee and Agarwal, 2025）将向量相似度与实体级、话语级对齐整合，而 RCR-Router（Liu et al., 2025d）结合多种手工信号，包括角色相关性、任务阶段优先级与新近性。然而，这些方法常需大量超参数调优以平衡异构重要性分数。为减轻这一负担，learn-to-memorize（Zhang et al., 2025u）将分数聚合表述为 reinforcement-learning 问题，使模型学习 retrieval 信号上的最优权重。这些技术主要优化语义连贯性，而要求严格时间 reasoning 的场景需要额外约束：Rasmussen et al.（2025）与 Tan et al.（2025b）依据时间戳与有效窗口过滤 memory，以满足复杂时间依赖。

随着 LLM 能力增强，近期方法利用其内在语言理解直接评估 memory 质量。Memory-R1（Yan et al., 2025c）与 Westhäußer et al.（2025）都引入基于 LLM 的评估器（Answer Agent 或 Self-Validator Agent），在生成最终响应前过滤 retrieval 内容。然而，基于 prompt 的过滤仍受 LLM 固有容量以及 prompt 语义与下游使用错配的限制。因此，许多系统训练辅助模型以更稳健地估计 memory 重要性（Tan et al., 2025c）。Memento（Zhou et al., 2025a）使用 Q-learning（Watkins and Dayan, 1992）预测 retrieval 项对正确答案有贡献的概率，MemGuide（Du et al., 2025b）fine-tune LLaMA-8B（Grattafiori et al., 2024）以边际 slot-completion 增益对候选重排。总体而言，这些 re-ranking 与过滤策略在不修改底层 retriever 的情况下精炼 retrieval 结果，兼容任何预训练 retrieval 模型，同时支持任务特定优化。

Aggregation and Compression 通过 post-retrieval processing 提升下游 reasoning 质量与效率的另一途径是 aggregation and compression。该过程将 retrieval 到的证据与查询整合，形成连贯紧凑的 context。不同于主要处理噪声与优先级的 filtering 与 re-ranking，该阶段聚焦于将多个碎片化 memory 项合并为更高层、distillation 后的知识表示，并在需要任务特定适配时精炼这些表示。ComoRAG（Wang et al., 2025f）通过其 Integration Agent 说明这一思路：识别与查询语义对齐的历史信号，并将其合并为提供广域 context 基础的抽象全局摘要。MA-RAG（Nguyen et al., 2025）中的 Extractor Agent 对 retrieval 文档执行细粒度内容选择，仅保留与当前子查询强相关的关键信息，生成适配局部 reasoning 需求的简洁片段。

此外，G-Memory（Zhang et al., 2025c）将 aggregation and compression 扩展到多 agent 系统的个性化。它 consolidated retrieval 到的高层 insight 与稀疏化 trajectory，然后使用 LLM 依据 agent 角色定制这些凝缩经验。该过程将通用知识精炼为角色特定 prompt，填充 agent 的个性化 memory。

Summary 总之，post-retrieval processing 充当关键的中间步骤，将含噪、碎片化的 retrieval 结果转化为精确连贯的 reasoning context。通过上述机制，post-retrieval processing 不仅提升提供给模型的 memory 密度与保真度，也使信息与任务需求和 agent 特性对齐。

## 6 Resources and Frameworks

## 6.1 Benchmarks and Datasets

本节综述已被（或可被）用于评估 LLM-based agent 的 memory、long-term、continual-learning 或 long-context 能力的代表性 benchmark 与数据集。我们将这些 benchmark 分为两大类：(1) 明确为 memory / lifelong learning / self-evolving agent 设计的 benchmark；(2) 最初为其他目的（例如工具使用能力、web 搜索、具身动作）开发，但因 long-horizon、多任务或顺序性质而与 memory 评估相关的 benchmark。

## 6.1.1 Benchmarks for Memory / Lifelong / Self-Evolving Agents

Memory 导向的 benchmark 主要关注 agent 构造、维持与利用关于过往交互或世界事实的显式 memory 的能力。此类任务通常探查跨多轮对话、用户特定 session 或长合成叙事的信息保持与 retrieval，有时包含 multimodal 信号。

表 8 提供这些 benchmark 的汇总概览，包括其 memory 焦点、环境类型、模态与评估规模，可作为比较其设计目标与评估设定的结构化参考。MemBench（Tan et al., 2025a）、LoCoMo（Maharana et al., 2024）、WebChoreArena（Miyai et al., 2025）、MT-Mind2Web（Deng et al., 2024）、PersonaMem（Jiang et al., 2025a）、PerLTQA（Du et al., 2024）、MPR（Zhang et al., 2025v）、PrefEval（Zhao et al., 2025d）、LOCCO（Jia et al., 2025）、StoryBench（Wan and Ma, 2025）、Madial-Bench（He et al., 2025）、DialSim（Zheng et al., 2025b）、LongBench（Bai et al., 2024）、LongBench v2（Bai et al., 2025）、RULER（Hsieh et al., 2024）、BALILong（Kuratov et al., 2024）、MM-Needle（Wang et al., 2025e）与 HaluMem（Chen et al., 2025a）等代表性示例强调用户建模、偏好追踪与对话级一致性，且常在可精确控制 ground-truth memory 的模拟设定下进行。

Lifelong-learning benchmark 超越孤立 memory retrieval，考察 agent 如何在 long-horizon 与演化任务分布上持续获取、consolidated 与更新知识。LongMemEval（Wu et al., 2025a）、MemoryBank（Zhong et al., 2024）、MemoryBench（Ai et al., 2025）、LifelongAgentBench（Zheng et al., 2025b）与 StreamBench（Wu et al., 2024a）等 benchmark 围绕任务或 episode 序列设计，其中新信息逐步到达，早期信息可能过时或冲突。这些设定强调灾难性 forgetting、前向与后向迁移以及测试时适应等现象，适合研究 memory 机制如何与 continual-learning 目标交互。许多情况下，性能不仅在当前任务上追踪，也在适应新用户、领域或交互模式期间追踪。

Table 8 与 LLM agent memory、long-term、lifelong learning 及 self-evolving 评估相关的 benchmark 概览。该表覆盖两类 benchmark：(i) 明确为 memory、lifelong learning 或 self-evolving agent 评估设计的 benchmark；(ii) 通过顺序、多步或多任务交互隐式施压 long-horizon memory 的其他 agent 导向 benchmark。Fac. 与 Exp. 分别表示 benchmark 是否评估 factual memory 或 experiential（交互衍生）memory。MM. 表示是否存在 multimodal 输入，Env. 表示 benchmark 在模拟还是真实环境中进行。Feature 概括被评估的主要能力，Scale 以样本数（s.）或任务数（t.）报告 benchmark 的大致规模。PDDL 表示常用的基于 PDDL 的 planning 子集。
<table><tr><td>Name</td><td>Link</td><td>Fac.</td><td>Exp.</td><td>MM.</td><td>Env.</td><td>Feature</td><td>Scale</td></tr><tr><td colspan="8">Memory/Lifelong-learning/Self-evolving-oriented Benchmarks</td></tr><tr><td>MemBench</td><td>GitHub</td><td>√</td><td>√</td><td>✕</td><td>模拟</td><td>交互式场景</td><td>53,000 s.</td></tr><tr><td>MemoryAgentBench</td><td>GitHub</td><td>√</td><td>√</td><td>✕</td><td>模拟</td><td>多轮交互</td><td>4 t.</td></tr><tr><td>LoCoMo</td><td>Website</td><td>√</td><td>✕</td><td>√</td><td>真实</td><td>对话 memory</td><td>300 s.</td></tr><tr><td>WebChoreArena</td><td>GitHub</td><td>√</td><td>√</td><td>√</td><td>真实</td><td>繁琐 web 浏览</td><td>4 t./532 s.</td></tr><tr><td>MT-Mind2Web</td><td>GitHub</td><td>√</td><td>√</td><td>✕</td><td>真实</td><td>对话式 web 导航</td><td>720 s.</td></tr><tr><td>PersonaMem</td><td>Website</td><td>√</td><td>✕</td><td>✕</td><td>模拟</td><td>动态用户画像</td><td>15 t./180 s.</td></tr><tr><td>LongMemEval</td><td>GitHub</td><td>√</td><td>✕</td><td>✕</td><td>模拟</td><td>交互式 memory</td><td>5 t./500 s.</td></tr><tr><td>PerLTQA</td><td>Website</td><td>√</td><td>✕</td><td>✕</td><td>模拟</td><td>社交个性化交互</td><td>8,593 s.</td></tr><tr><td>MemoryBank</td><td>Website</td><td>√</td><td>✕</td><td>✕</td><td>模拟</td><td>用户 memory 更新</td><td>194 s.</td></tr><tr><td>MPR</td><td>GitHub</td><td>√</td><td>✕</td><td>✕</td><td>模拟</td><td>用户个性化</td><td>108,000 s.</td></tr><tr><td>PrefEval</td><td>Website</td><td>√</td><td>✕</td><td>✕</td><td>模拟</td><td>个人偏好</td><td>3,000 s.</td></tr><tr><td>LOCCO</td><td>Website</td><td>√</td><td>✕</td><td>✕</td><td>模拟</td><td>时序对话</td><td>3,080 s.</td></tr><tr><td>StoryBench</td><td>Website</td><td>√</td><td>√</td><td>✕</td><td>混合</td><td>交互式虚构游戏</td><td>3 t.</td></tr><tr><td>MemoryBench</td><td>Website</td><td>√</td><td>√</td><td>✕</td><td>模拟</td><td>持续学习</td><td>4 t./~ 20,000 s.</td></tr><tr><td>Madial-Bench</td><td>GitHub</td><td>√</td><td>✕</td><td>✕</td><td>模拟</td><td>memory 回忆</td><td>331 s.</td></tr><tr><td>Evo-Memory</td><td>Website</td><td>√</td><td>√</td><td>✕</td><td>模拟</td><td>测试时学习</td><td>10 t./~ 3,700 s.</td></tr><tr><td>LifelongAgentBench</td><td>Website</td><td>√</td><td>√</td><td>✕</td><td>模拟</td><td>终身学习</td><td>1,396 s.</td></tr><tr><td>StreamBench</td><td>Website</td><td>√</td><td>√</td><td>✕</td><td>模拟</td><td>持续在线学习</td><td>9,702 s.</td></tr><tr><td>DialSim</td><td>Website</td><td>√</td><td>√</td><td>✕</td><td>真实</td><td>多对话理解</td><td>~ 1,300 s.</td></tr><tr><td>LongBench</td><td>Website</td><td>√</td><td>✕</td><td>✕</td><td>混合</td><td>长 context 理解</td><td>21 t./4,750 s.</td></tr><tr><td>LongBench v2</td><td>Website</td><td>√</td><td>✕</td><td>✕</td><td>混合</td><td>长 context 多任务</td><td>20 t./503 s.</td></tr><tr><td>RULER</td><td>GitHub</td><td>√</td><td>✕</td><td>✕</td><td>模拟</td><td>长 context retrieval</td><td>13 t.</td></tr><tr><td>BABILong</td><td>GitHub</td><td>√</td><td>✕</td><td>✕</td><td>模拟</td><td>长 context reasoning</td><td>20 t.</td></tr><tr><td>MM-Needle</td><td>Website</td><td>√</td><td>✕</td><td>√</td><td>模拟</td><td>multimodal 长 context retrieval</td><td>~ 280,000 s.</td></tr><tr><td>HaluMem</td><td>GitHub</td><td>√</td><td>✕</td><td>✕</td><td>模拟</td><td>memory 幻觉</td><td>3,467 s.</td></tr><tr><td>HotpotQA</td><td>Website</td><td>√</td><td>✕</td><td>✕</td><td>模拟</td><td>长 context QA</td><td>113k s.</td></tr><tr><td colspan="8">Other Related Benchmarks</td></tr><tr><td>ALFWorld</td><td>Website</td><td>√</td><td>√</td><td>✕</td><td>模拟</td><td>文本具身环境</td><td>3,353 t.</td></tr><tr><td>ScienceWorld</td><td>GitHub</td><td>√</td><td>√</td><td>✕</td><td>模拟</td><td>交互式具身环境</td><td>10 t./30 t.</td></tr><tr><td>AgentGym</td><td>Website</td><td>✕</td><td>√</td><td>✕</td><td>混合</td><td>多环境</td><td>89 t./20,509 s.</td></tr><tr><td>AgentBoard</td><td>GitHub</td><td>✕</td><td>√</td><td>✕</td><td>混合</td><td>多轮交互</td><td>9 t./1013 s.</td></tr><tr><td>PDDL*</td><td>Website</td><td>✕</td><td>√</td><td>✕</td><td>模拟</td><td>策略游戏</td><td>-</td></tr><tr><td>BabyAI</td><td>Website</td><td>✕</td><td>√</td><td>✕</td><td>模拟</td><td>语言学习</td><td>19 t.</td></tr><tr><td>WebShop</td><td>Website</td><td>✕</td><td>√</td><td>√</td><td>模拟</td><td>电商 web 交互</td><td>12,087 s.</td></tr><tr><td>WebArena</td><td>Website</td><td>✕</td><td>√</td><td>√</td><td>真实</td><td>web 交互</td><td>812 s.</td></tr><tr><td>MMInA</td><td>Website</td><td>√</td><td>√</td><td>√</td><td>真实</td><td>多跳 web 交互</td><td>1,050 s.</td></tr><tr><td>SWE-Bench Verified</td><td>Website</td><td>✕</td><td>√</td><td>✕</td><td>真实</td><td>代码修复</td><td>500 s.</td></tr><tr><td>GAIA</td><td>Website</td><td>✕</td><td>√</td><td>√</td><td>真实</td><td>类人深度研究</td><td>466 s.</td></tr><tr><td>xBench-DS</td><td>Website</td><td>✕</td><td>√</td><td>√</td><td>真实</td><td>深度搜索评估</td><td>100 s.</td></tr><tr><td>ToolBench</td><td>GitHub</td><td>✕</td><td>√</td><td>✕</td><td>真实</td><td>API 工具使用</td><td>126,486 s.</td></tr><tr><td>GenAI-Bench</td><td>Website</td><td>✕</td><td>√</td><td>√</td><td>真实</td><td>视觉生成评估</td><td>~ 40,000 s.</td></tr></table>
先前见过的任务或对话，从而量化 agent 对有用知识的保持程度。

Self-evolving-agent benchmark 更进一步，将 agent 视为开放式系统，可通过交互迭代精炼自身 memory、skill 与 strategy。此处焦点不仅是存储与回忆信息，也包括元层行为，例如自我反思、memory 编辑、工具增强存储，以及跨多个 episode 或游戏改进策略。MemoryAgentBench（Hu et al., 2025c）、Evo-Memory（Wei et al., 2025e）以及其他多 episode 或任务式环境等 benchmark，可通过允许 agent 累积 trajectory、综合更高层抽象、并基于自身过往表现在未来运行中调整行为，被实例化为 self-evolving 设定。从这一视角看，这些 benchmark 提供试验台，用以评估 agent 能否随时间自主 bootstrap 更强能力——将静态任务转变为长期适应、策略精炼与真正自我改进 memory 使用的竞技场。

## 6.1.2 Other Related Benchmarks

除明确为 memory 或 lifelong learning 设计的 benchmark 之外，大量 agent 导向与 long-horizon 评估套件也与研究 LLM-based agent 的 memory 相关能力相关。尽管这些 benchmark 最初用于评估工具使用、具身交互或知识密集 reasoning 等其他方面，其顺序、多步与多任务性质隐含地对长期信息保持、context 管理与状态追踪提出很高要求。

具身与交互环境构成此类 benchmark 的主要类别。ALFWorld（Shridhar et al., 2021）与 ScienceWorld（Wang et al., 2022a）等框架在模拟的文本或部分具身环境中评估 agent，其成功需要在扩展动作序列中记住过往观察、中间目标与环境动态。类似地，BabyAI（Chevalier-Boisvert et al., 2019）聚焦时间延展 episode 上的语言条件指令遵循，隐式测试 agent 在整个交互中维持任务相关状态的能力。这些 benchmark 虽未显式建模外部 memory 模块，其有效表现常取决于 agent 在 long-horizon 上保持与复用信息的能力。

另一显著类别包括基于 web 与工具增强的交互 benchmark。WebShop（Yao et al., 2023a）、WebArena（Zhou et al., 2024b）与 MMInA（Tian et al., 2025b）评估 agent 在真实或半真实 web 环境中运作，涉及多步导航、信息收集与决策。这些设定自然产生长 context trajectory，其中早期动作、retrieval 信息或用户约束必须在后续阶段被回忆并整合。ToolBench（Qin et al., 2024a）进一步扩展该范式，评估 agent 在复杂 workflow 中选取与调用 API 的能力，其中对先前工具输出与工具使用经验的 memory 对连贯执行至关重要。

多任务与通用 agent 评估平台也提供关于 memory 使用的间接但有价值的信号。AgentGym（Xi et al., 2024b）与 AgentBoard（Xi et al., 2024b）将多样环境或任务聚合为统一评估套件，要求 agent 跨任务适应，同时保留任务特定知识与 strategy。agent benchmark 中常用的基于 PDDL 的 planning 环境评估结构化动作空间上的策略性 reasoning，其中 agent 受益于跨 episode 累积与复用经验以提升 long-horizon planning 表现。

最后，若干近期 benchmark 瞄准要求严苛的真实或近真实 reasoning 场景，天然施压长 context 与跨步一致性。SWE-Bench Verified（Jimenez et al., 2024）在真实软件仓库上评估代码修复，agent 必须对长文件与演化代码状态进行 reasoning。GAIA（Mialon et al., 2023）与 xBench（Chen et al., 2025c）评估深度研究与搜索密集任务，需要综合跨多步、多源收集的信息。GenAI-Bench（Li et al., 2024a）虽聚焦 multimodal 生成质量，同样涉及复杂 workflow，其中对先前 prompt、中间输出或视觉约束的 memory 起非平凡作用。

综合来看，这些 benchmark 通过将 LLM-based agent 置于丰富、交互、long-horizon 设定中，显式补充了 memory 导向评估。尽管 memory 并非总是显式测量目标，这些环境中的持续表现隐式取决于 agent 管理长 context、保持相关信息并将过往经验整合进持续决策的能力，使其成为实践中研究 memory 相关行为的宝贵试验台。
Table 9 LLM-based agent 代表性开源 memory 框架概览。该表按所支持的 memory 类型（factual 与 experiential）、multimodal 性、内部 memory 结构与已报告的评估 benchmark 比较广泛使用的框架。Fac. 与 Exp. 分别表示 factual memory 与 experiential memory，MM. 表示 multimodal memory 支持，Structure 概括各框架采用的核心 memory 抽象或组织机制。Evaluation 列出公开报告的用于评估 memory 相关能力的 benchmark（若有）。

<table><tr><td>Framework</td><td>Links</td><td>Fac.</td><td>Exp.</td><td>MM.</td><td>Structure</td><td>Evaluation</td></tr><tr><td>MemGPT</td><td>GitHub Website</td><td>✓</td><td>✓</td><td>✘</td><td>层级（S/LTM）</td><td>LoCoMo</td></tr><tr><td>Mem0</td><td>GitHub Website</td><td>✓</td><td>✓</td><td>✘</td><td>图 + 向量</td><td>LoCoMo</td></tr><tr><td>Memobase</td><td>GitHub Website</td><td>✓</td><td>✓</td><td>✘</td><td>结构化画像</td><td>LoCoMo</td></tr><tr><td>MIRIX</td><td>GitHub Website</td><td>✓</td><td>✓</td><td>✓</td><td>结构化 memory</td><td>LoCoMo, MemoryAgentBench</td></tr><tr><td>MemoryOS</td><td>GitHub Website</td><td>✓</td><td>✓</td><td>✘</td><td>层级（S/M/LTM）</td><td>LoCoMo, MemoryBank</td></tr><tr><td>MemOS</td><td>GitHub Website</td><td>✓</td><td>✓</td><td>✘</td><td>树形 memory + memcube</td><td>LoCoMo, PreFEval, LongMemEval, PersonaMem</td></tr><tr><td>Zep</td><td>GitHub Website</td><td>✓</td><td>✓</td><td>✘</td><td>时间知识图谱</td><td>LongMemEval</td></tr><tr><td>LangMem</td><td>GitHub Website</td><td>✓</td><td>✓</td><td>✘</td><td>核心 API + manager</td><td>-</td></tr><tr><td>SuperMemory</td><td>GitHub Website</td><td>✓</td><td>✓</td><td>✓</td><td>向量 + 语义</td><td>-</td></tr><tr><td>Cognee</td><td>GitHub Website</td><td>✓</td><td>✓</td><td>✓</td><td>知识图谱</td><td>-</td></tr><tr><td>Memory</td><td>GitHub Website</td><td>✓</td><td>✓</td><td>✘</td><td>流 + 实体存储</td><td>-</td></tr><tr><td>Pinecone</td><td>GitHub Website</td><td>✓</td><td>✘</td><td>✘</td><td>向量数据库</td><td>-</td></tr><tr><td>Chroma</td><td>GitHub Website</td><td>✓</td><td>✘</td><td>✓</td><td>向量数据库</td><td>-</td></tr><tr><td>Weaviate</td><td>GitHub Website</td><td>✓</td><td>✘</td><td>✓</td><td>向量 + 图</td><td>-</td></tr><tr><td>Second Me</td><td>GitHub Website</td><td>✓</td><td>✘</td><td>✘</td><td>agent ego</td><td>-</td></tr><tr><td>MemU</td><td>GitHub Website</td><td>✓</td><td>✓</td><td>✓</td><td>层级层</td><td>-</td></tr><tr><td>MemEngine</td><td>GitHub</td><td>✓</td><td>✓</td><td>✓</td><td>模块化空间</td><td>-</td></tr><tr><td>Memori</td><td>GitHub Website</td><td>✓</td><td>✓</td><td>✘</td><td>memory 数据库</td><td>-</td></tr><tr><td>ReMe</td><td>GitHub Website</td><td>✓</td><td>✓</td><td>✘</td><td>memory 管理</td><td>-</td></tr><tr><td>AgentMemory</td><td>GitHub Website</td><td>✓</td><td>✓</td><td>✘</td><td>memory 管理</td><td>-</td></tr><tr><td>MineContext</td><td>GitHub Website</td><td>✓</td><td>✓</td><td>✓</td><td>context engineering</td><td>-</td></tr><tr><td>Acontext</td><td>GitHub</td><td>✓</td><td>✓</td><td>✓</td><td>context engineering + skill learning</td><td>-</td></tr><tr><td>PowerMem</td><td>GitHub</td><td>✓</td><td>✘</td><td>✓</td><td>oceanbase</td><td>-</td></tr><tr><td>ReMe</td><td>GitHub</td><td>✓</td><td>✓</td><td>✘</td><td>agentscope</td><td>BFCL, AppWorld</td></tr><tr><td>HindSight</td><td>GitHub</td><td>✓</td><td>✓</td><td>✘</td><td>并行 retrieval + 反思</td><td>-</td></tr></table>

## 6.2 Open-Source Frameworks

快速成长的开源 memory 框架生态旨在为构建 memory-augmented LLM agent 提供可复用基础设施。表 9 汇总代表性开源 memory 框架的结构化比较，包括其支持的 memory 类型、架构抽象与评估覆盖。多数框架通过向量或结构化 store 支持 factual memory，越来越多的子集也建模经验性 trace，例如对话历史、用户动作与 episodic summary，multimodal memory 则更近期才兴起。面向 LLM agent 的开源 memory 框架横跨一个谱系：从具备丰富层级 memory 抽象的 agent 中心系统，到更通用的 retrieval 或 memory-as-a-service 后端，例如 MemGPT（Packer et al., 2023b）、Mem0（Chhikara et al., 2025）、Memobase、MemoryOS（Kang et al., 2025a）、MemOS（Li et al., 2025l）、Zep（Rasmussen et al., 2025）、LangMem（LangChain, 2025）、SuperMemory（Supermemory, 2025）、Cognee（Cognee, 2025）、Memary（Memary, 2025）、Pinecone、Chroma、Weaviate、Second Me、MemU、MemEngine（Zhang et al., 2025t）、Memori、ReMe（AgentScope, 2025）、AgentMemory 与 MineContext（MineContext, 2025）。其中许多显式分离 short-term 与 long-term store，并提供基于图、基于画像或模块化的 memory 空间，一些已开始在 memory benchmark 上报告结果。其余通常提供可扩展的向量或图数据库、API，以及语义或流式实体层，帮助组织 context，却常将 agent 行为与评估协议留给应用层。总体而言，这些框架在表示灵活性与系统设计上正快速成熟。

## 7 Positions and Frontiers

本节阐述面向 LLM-based agent 的 memory 系统设计中的关键立场与新兴前沿。超越对现有方法的描述性综述，我们聚焦范式级转变，这些转变重新定义 long-horizon agentic 设定下 memory 如何被构造、管理与优化。具体而言，我们考察从以 retrieval 为中心到生成式 memory、从手工工程到自主管理 memory 系统、从启发式 pipeline 到 reinforcement learning 驱动的 memory 控制的转变。我们进一步讨论这些转变如何与 multimodal reasoning、多 agent 协作与可信性交汇，勾勒可能塑造下一代 agent memory 架构的开放挑战与研究方向。

## 7.1 Memory Retrieval vs. Memory Generation

## 7.1.1 Look Back: From Memory Retrieval to Memory Generation

历史上，agent memory 研究的主导范式集中于 memory retrieval。该范式下，主要目标是在给定当前 context 时，从既有 memory store 中识别、过滤并选取最相关 memory 条目。大量先前工作聚焦通过更好的索引策略、相似度度量、reranking 模型或知识图谱等结构化表示来提升 retrieval 精度（Tan et al., 2025c; Memobase, 2025）。实践中，这包括稠密 embedding 的向量相似度搜索、结合词汇与语义信号的混合 retrieval、层级过滤与基于图的遍历等技术。这些方法强调访问已存信息的精度与召回，隐含假设 memory base 本身已良好成形。

然而，近期越来越多注意力转向 memory generation。memory generation 不把 memory 当作待查询的静态仓库，而强调 agent 按需主动综合新 memory 表示的能力。目标不只是 retrieval 并拼接既有片段，而是以适配当前 context 与未来效用的方式整合、压缩并重组信息。这一转变反映一种日益增长的认识：有效的 memory 使用常需要抽象与重组，尤其当已存原始信息含噪、冗余或与即时任务错位时。

现有 memory generation 方法大体分为两个方向。一类工作采用 retrieve then generate 策略，retrieval 到的 memory 项充当重构原材料。在此设定下，agent 先访问相关 memory 子集，再生成更简洁、连贯且 context 特定的精炼 memory 表示，ComoRAG（Wang et al., 2025f）、G-Memory（Zhang et al., 2025c）与 CoMEM（Wu et al., 2025d）即如此实现。该方法保留对历史信息的基础依托，同时支持自适应摘要与重构。第二类工作探索 direct memory generation，即不经过任何显式 retrieval 步骤而生成 memory。agent 直接从当前 context、交互历史或 latent 内部状态生成 memory 表示。MemGen（Zhang et al., 2025d）与 VisMem（Yu et al., 2025e）等系统通过构造适配当前任务的 latent memory token 来例示这一方向，完全绕过显式 memory 查找。

## 7.1.2 Future Perspective

展望未来，我们预计生成式方法将在 agent memory 系统中扮演日益核心的角色。我们强调未来生成式 memory 机制理想上应具备的三项属性。

第一，生成式 memory 应具备 context 适应性。memory 系统不应存储通用摘要，而应生成明确针对 agent 预期未来需求优化的表示。

这包括使 memory 的粒度、抽象层级与语义焦点适配不同任务、问题求解阶段或交互机制。

第二，生成式 memory 应支持跨异构信号的整合。agent 日益在多样模态与信息源上运作，包括文本、代码、工具输出与环境反馈。memory generation 提供自然机制，将这些碎片化信号融合为统一表示，使其比原始拼接或单纯 retrieval 更有益于下游 reasoning。我们假设 latent memory（如 3.3 节所讨论）可能是实现这一目标的有前景技术路径。

第三，生成式 memory 应是可学习且自我优化的。未来系统不应依赖手工指定的生成规则，而应通过优化信号（例如 reinforcement learning 或 long-horizon 任务表现）学习何时以及如何生成 memory。在这一视角下，memory generation 成为 agent policy 的有机组成部分，与 reasoning 和决策共同演化。

## 7.2 Automated Memory Management

## 7.2.1 Look-Back: From Hand-crafted to Automatically Constructed Memory Systems.

现有 agent memory 系统（Xu et al., 2025c; Packer et al., 2023a）通常依赖人工设计的策略来决定存储什么信息、何时使用、以及如何更新或 retrieval。通过以详细指令（Chhikara et al., 2025）、预定义阈值（Kang et al., 2025a）或由人类专家起草的显式手工规则（Xu et al., 2025c）引导固定 LLM，系统设计者可以以相对较低的计算与工程成本将 memory 模块整合进当前 agent 框架，实现快速原型与部署。此外，它们还提供可解释性、可复现性与可控性，使开发者能精确指定 memory 的状态与行为。然而，与其他领域的专家系统类似，这种人工策展方法有显著局限：它们本质上不灵活，常无法泛化到多样、动态的环境。因此，这些系统在长期或开放式交互中往往表现不佳。

近期 agent memory 研究的发展开始通过让 agent 自主管理 memory evolution 与 retrieval 来应对这些局限。例如，CAM（Li et al., 2025g）使 LLM agent 能自动将细粒度 memory 条目聚类为高层抽象单元。Memory-R1（Yan et al., 2025c）引入配备专用“memory manager”工具的辅助 agent 来处理 memory 更新。尽管有这些进展，当前方案仍受约束：许多仍由手工工程规则驱动，或针对狭窄的任务特定学习目标优化，难以泛化到开放式设定。

## 7.2.2 Future Perspective

为支持真正自动化的 memory 管理，一个有前景的方向是通过显式工具调用将 memory construction、evolution 与 retrieval 直接整合进 agent 的决策循环，使 agent 自身对 memory 操作进行 reasoning，而非依赖外部模块或手工 workflow。与将 agent 内部 reasoning 过程与其 memory 管理动作分离的既有设计相比，在这种基于工具的 strategy 中，LLM agent 能精确知道自己执行何种 memory 动作（例如 add/update/delete/retrieval），从而产生更连贯、透明且 context 扎根的 memory 行为。

另一关键前沿在于发展自我优化的 memory 结构，采用受认知系统启发的层级与自适应架构。第一，层级 memory 结构已被证明能提升效率与性能（Kang et al., 2025a）。超越层级，动态链接、索引与重构 memory 条目的自我演化 memory 系统使 memory 存储本身能随时间自组织，支撑更丰富的 reasoning 并减少对手工设计规则的依赖。最终，这种自适应、自组织的 memory 架构为 agent 铺路，使其能够维持稳健、可扩展且真正自主的 memory 管理。
![](../assets/arxiv-2512.13564-fig11.jpg)  
Figure 11 RL-enabled agent memory 系统的演化。一条概念性进展路径：从基于启发式或 prompt 驱动 pipeline 的无 RL memory 系统，到 RL 部分介入、由 reinforcement learning 治理选定 memory 操作的设计，最终到完全 RL 驱动的 memory 系统，其中 memory 架构与控制 policy 被端到端学习。这一演化反映更广的范式转向：从手工工程的 memory pipeline 走向 LLM-based agent 中模型原生、自我优化的 memory 管理。

## 7.3 Reinforcement Learning Meets Agent Memory

## 7.3.1 Look-Back: RL is Internalizing Memory Management Abilities for Agents.

Reinforcement learning 正迅速重塑现代 LLM-based agent 的开发范式。在广泛的 agentic 能力上，包括 planning、reasoning、工具使用，以及在数学 reasoning、深度研究与软件工程等多样任务领域中，RL 已开始扮演驱动 agent 性能的核心角色（Zhang et al., 2025f,l; Feng et al., 2024）。Memory 作为 agentic 能力的基础组件之一，也遵循从基于 pipeline 到模型原生范式的相似趋势（Sang et al., 2025）。agent memory 研究共同体正集体从早期启发式与手工工程设计，转向由 RL 日益治理关键决策的方法。展望未来，完全基于 RL 的 memory 系统最终成为主导方向是合理的预期。在详述这一轨迹之前，我们简要勾勒发展的第一阶段。这一转变——memory 管理通过 reinforcement learning 逐步被内化与优化——在图 11 中示意。

RL-free Memory Systems 前文综述的相当一部分 agent memory 文献可归类为无 RL memory 系统。这些方法通常依赖启发式或手工指定机制，例如受 forgetting 曲线启发的固定阈值规则、MemOS（Li et al., 2025l）、Mem0（Chhikara et al., 2025）与 MemoBase（Memobase, 2025）等框架中的刚性语义搜索 pipeline，或用于存储 memory chunk 的简单拼接 strategy。在一些系统中，LLM 以看似 agentic 的方式参与 memory 管理，但底层行为完全由 prompt 驱动。LLM 被要求生成 memory 条目，却未接受任何专门的有效 memory 控制训练，Dynamic Cheatsheet（Suzgun et al., 2025）、ExpeL（Zhao et al., 2024）、EvolveR（Wu et al., 2025c）与 G-Memory（Zhang et al., 2025c）等系统即如此。这一类方法主导了该领域的早期工作，且因其简单性与实践可及性，可能在一段时间内仍有影响力。

RL-assisted Memory Systems 随着领域推进，许多工作开始将基于 RL 的方法纳入 memory pipeline 的选定组件。该方向早期尝试是 RMM（Tan et al., 2025c），它在基于 BM25 或其他语义相似度度量的初始 retrieval 阶段之后，采用轻量策略梯度学习器对 memory chunk 排序。后续系统探索了雄心更大的设计。例如，Mem-α（Wang et al., 2025p）将整个 memory construction 过程委托给以 RL 训练的 agent，Memory-R1（Yan et al., 2025c）采用相似理念。一条快速扩展的研究线考察 agent 如何在超长多轮任务中自主折叠、压缩与管理 context。这一设定对应 working memory 的管理（Kang et al., 2025c; Ye et al., 2025a）。该领域许多领先系统以 RL 训练，包括但不限于 Context Folding（Sun et al., 2025b）、Memory-as-Action（Zhang et al., 2025r）、MemSearcher（Yuan et al., 2025a）与 IterResearch（Chen et al., 2025b）。这些 RL-assisted 方法已展现强大能力，并指向 RL 在未来 memory 系统设计中日益增强的作用。

## 7.3.2 Future Perspective

展望未来，我们预计完全 RL 驱动的 memory 系统将构成 agent memory 演化的下一个主要阶段。我们强调此类系统理想上应体现的两项属性。

• 第一，由 agent 管理的 memory 架构应尽量减少对人类工程先验的依赖。许多现有框架继承受人类认知启发的设计模式，例如皮层或海马类比（Gutierrez et al., 2024），或预定义层级分类，将 memory 划分为 episodic、semantic 与 core 类别（Wang and Chen, 2025）。这些抽象虽有助于为早期工作奠基，却未必代表在复杂环境中运作的人工 agent 最有效或最自然的结构。完全 RL 驱动的设定为 agent 提供了可能：发明直接源自优化动态、而非人类直觉的新颖且可能更合适的 memory 组织。在这一视角下，agent 被鼓励通过 RL 激励设计新的 memory 格式、存储 schema 或更新规则，使 memory 架构具备自适应性与创造性，而非手工制品。

• 第二，未来 memory 系统应赋予 agent 对 memory 管理所有阶段的完整控制。当前 RL-assisted 方法通常只介入 memory 生命周期的一个子集。例如，Mem-α 自动化 memory 写入的某些方面，却仍依赖人工定义的 retrieval pipeline；MemSearcher（Yuan et al., 2025a）等系统则主要聚焦短期 working memory，未处理长期 consolidation 或 evolution。完全 agentic 的 memory 系统将要求 agent 以整合方式自主处理多粒度 memory formation、memory evolution 与 memory retrieval。实现这一控制水平几乎必然需要端到端 RL 训练，因为启发式或基于 prompt 的方法不足以在 long-horizon 上协调这些组件间的复杂交互。

综合来看，这两个方向指向一个未来：memory 不再只是栓在 LLM agent 上的辅助机制，而是与 agent 通过 RL 共同演化的完全可学习、自组织子系统。此类系统有潜力在人工 agent 中实现真正的持续学习与长期能力。

## 7.4 Multimodal Memory

## 7.4.1 Look-Back

随着基于文本的 memory 研究日益成熟并得到广泛探索，以及同时支持 multimodal 理解与生成的 multimodal 大语言模型与统一模型持续进步，注意力自然扩展到 multimodal memory。这一转变反映更广的认识：许多真实世界 agentic 设定本质上是 multimodal 的，仅限文本的 memory 系统不足以支撑复杂环境中的 long-horizon reasoning 与交互。

现有 multimodal memory 工作大体分为两个互补方向。第一个方向聚焦使 multimodal agent 能够存储、retrieval 与利用源自多样感官输入的 memory（Long et al., 2025; Zuo et al., 2025）。该方向是 agent memory 的自然延伸，因为在真实环境中运作的 agent 不可避免地遇到异构数据源，包括图像、音频、视频与其他非文本信号（Xie et al., 2024）。multimodal memory 的进展程度密切跟随相应模态的成熟度。图像与视频等视觉模态获得最多关注，催生日益增多的视觉与视频 memory 机制研究，支撑视觉 grounding、时间追踪与长期场景一致性等任务（Long et al., 2025; Wang et al., 2024g; Gurukar and Kadav, 2025; Yu et al., 2025e; Bo et al., 2025; Wang et al., 2025q; Li et al., 2024d）。相比之下，面向音频与其他模态的 memory 系统仍相对欠探索（Li et al., 2025a）。

第二个方向将 memory 视为统一模型的使能组件。在此设定中，memory 主要不是用于支撑 agent 决策，而是增强 multimodal 生成与一致性。例如，在图像与视频生成系统中，memory 机制常用于保持实体一致性、跨帧维持世界状态，或确保长生成时程上的连贯性（Yu et al., 2025b）。此处，memory 充当稳定结构，将生成锚定到先前产生的内容，而非作为 agent 经验本身的记录。

## 7.4.2 Future Perspective

展望未来，multimodal memory 很可能成为 agentic 系统不可或缺的组件。随着 agent 日益走向具身与交互设定，其信息源将天然 multimodal，横跨感知、动作与环境反馈。因此，有效的 memory 系统必须以统一方式支持异构信号的存储、整合与 retrieval。

尽管近期有进展，目前尚无 memory 系统提供真正的全模态支持。多数现有方法仍专精于单一模态，或模态间仅松散耦合。一个关键未来挑战在于设计能灵活容纳多样模态、同时保持语义对齐与时间连贯性的 memory 表示与操作。此外，multimodal memory 必须超越被动存储，支持抽象、跨模态 reasoning 与长期适应。应对这些挑战对于使 agent 能在丰富 multimodal 环境中稳健连贯地运作至关重要。

## 7.5 Shared Memory in Multi-Agent Systems

## 7.5.1 Look-Back: From Isolated Memories to Shared Cognitive Substrates

随着 LLM-based 多 agent 系统（MAS）崭露头角，shared memory 已成为实现协调、一致性与集体智能的关键机制。早期多 agent 框架主要依赖隔离的本地 memory 配合显式消息传递，agent 通过对话历史或任务特定通信协议交换信息（Qian et al., 2024; Wu et al., 2024b; Hu et al., 2025b; Zhang et al., 2025j）。这种设计避免了 agent 间直接干扰，却常受冗余、context 碎片化与高通信开销困扰，尤其当团队规模与任务时程增加时。

后续工作引入集中式 shared memory 结构，例如全局向量 store、blackboard 系统或共享文档（Hong et al., 2024），对所有 agent 可访问。这些设计实现某种团队级 memory，支持共同注意、减少重复并促进 long-horizon 协调。代表性系统表明 shared memory 可作为 planning、角色交接与共识构建的持久共同基础（Rezazadeh et al., 2025b; Xu et al., 2025a）。然而，朴素的全局共享也暴露新挑战，包括 memory 杂乱、写竞争，以及缺乏角色或权限感知的访问控制。

## 7.5.2 Future Perspective

展望未来，shared memory 很可能从被动仓库演化为被主动管理且自适应的集体表示。一个重要方向是发展 agent-aware shared memory，其中读写行为以 agent 角色、专长与信任为条件，实现更结构化、可靠的知识聚合。

另一有前景的途径是学习驱动的 shared memory 管理。未来系统不应依赖手工设计的同步、摘要或冲突消解策略，而可训练 agent 基于 long-horizon 团队表现决定何时、贡献什么以及如何贡献到 shared memory。最后，随着 MAS 日益在开放式与 multimodal 环境中运作，shared memory 必须支持跨异构信号的抽象，同时维持时间与语义连贯性，我们认为 latent memory 在此展现出有前景的路径（Wu et al., 2025d）。在这些方向上的推进，对于将 shared memory 从协调辅助扩展为稳健集体智能的基础至关重要。

## 7.6 Memory for World Model

## 7.6.1 Look-Back

World Model 的核心目标是构造能够高保真模拟物理世界的内部环境。此类系统充当下一代人工智能的关键基础设施。world model 的核心属性是生成可无限延展且可实时交互的内容。不同于创建定长片段的传统视频生成，world model 以迭代方式运作：每一步接收动作并预测下一状态，从而提供连续反馈。在这一迭代框架中，memory 机制成为系统的基石。memory 存储并维持来自上一时间步的空间与语义信息或隐藏状态。它确保下一 chunk 的生成在场景布局、物体属性与运动逻辑方面与前序 context 保持长期一致。本质上，memory 机制使 world model 能处理长期时间依赖并实现可信的模拟交互。

此前，memory 建模依赖简化的缓冲方法。Frame Sampling 以少量历史帧为条件生成（Bruce et al., 2024）。该方法虽直观，却导致 context 碎片化与感知漂移，因为早期细节丢失。Sliding Window 方法采用 attention sink 与局部 KV cache 等 LLM 技术（Liu et al., 2025f）。这虽解决了计算瓶颈，却将 memory 限制在固定窗口。一旦物体离开该视野，模型实际上就忘记了它，使 loop closure 等复杂任务无法实现。到 2025 年末，领域从有限 context window 转向结构化状态表示。当前架构遵循三条主要路径：

• State-Space Models（SSM）Long-Context SSM 等架构采用 Mamba 式 backbone（Po et al., 2025; Yu et al., 2025f）。它们将无限历史压缩为固定大小的递归状态，理论上实现无限 memory 容量与恒定 inference 成本。

• Explicit Memory Banks。不同于压缩状态，这些系统维护历史表示的外部存储以支持精确回忆。各方法的结构化逻辑不同：UniWM 采用层级设计，通过基于特征的相似度门控将短期感知与长期历史分离（Dong et al., 2025b）。相反，WorldMem 与 Context-as-Memory（CaM）等基于 retrieval 的方法维护过去 context 的平面 bank，利用几何 retrieval（例如 FOV 重叠）动态选择相关帧以维持 3D 场景一致性（Xiao et al., 2025c; Yu et al., 2025c）。

• Sparse Memory and Retrieval 为在长期遵循与效率之间取得平衡，Genie Envisioner 与 Ctrl-World 采用稀疏 memory 机制（Liao et al., 2025b; Guo et al., 2025）。这些模型通过注入稀疏采样的历史帧或 retrieval 姿态条件 context 来增强当前观察，以在操作任务中锚定预测并防止漂移。

## 7.6.2 Future Perspective

从架构视角看，该领域正经历从聚焦被动保持的 Data Caching 到聚焦主动维持的 State Simulation 的根本转变。这一演化目前正结晶为两种不同范式，旨在解决实时响应性与长期逻辑一致性之间的冲突。

• The Dual-System Architecture。受认知科学启发，world model 可二分为快与慢组件。System 1 代表快速、本能的层，使用 SSM 等高效 backbone 处理即时物理与流畅交互。System 2 代表缓慢、审慎的层，使用大规模 VLM 或显式 memory 数据库处理复杂 reasoning、planning 与世界一致性。

• Active Memory Management。被动机制正被 Active Memory Policies 取代。新模型不再将 memory 视为盲目存储近期历史的固定 buffer，而是设计为 Cognitive Workspaces，基于任务相关性主动策展、摘要并丢弃信息。近期实证研究表明，此类主动 memory 管理在处理功能性无限 context 时显著优于静态 retrieval 方法。这一转变标志着从简单记住最近 N 个 token，转向维持连贯且可查询的世界状态。

## 7.7 Trustworthy Memory

## 7.7.1 Look-Back: From Trustworthy RAG to Trustworthy Memory

如本综述通篇所示，memory 在使能 agentic 行为方面扮演基础角色，支撑持久性、个性化与持续学习。然而，随着 memory 系统更深地嵌入 LLM-based agent，可信性问题变得至关重要。

早期围绕 retrieval-augmented generation（RAG）系统中幻觉与事实性的担忧（Niu et al., 2024; Sun et al., 2025f; Lu et al., 2025c）如今已演化为 memory-augmented agent 更广的信任讨论。与 RAG 类似，使用外部或 long-term memory 的一大动机是通过将模型输出扎根于可 retrieval 的事实内容来减少幻觉（Ru et al., 2024; Wang et al., 2025c）。然而，不同于 RAG，agent memory 常存储用户特定、持久且可能敏感的内容，范围从事实知识到过往交互、偏好或行为 trace。这在隐私、可解释性与安全方面引入额外挑战。

Wang et al.（2025b）近期工作表明，memory 模块可通过间接的基于 prompt 的攻击泄露私有数据，凸显 memory 与过度保留的风险。同时，Wu et al.（2025g）主张 agent memory 系统必须支持访问控制、可验证 forgetting 与可审计更新的显式机制，才能保持可信。值得注意的是，在 memory 跨长时间跨度持久存在的 agent 场景中，此类威胁会被放大。

可解释性也仍是关键瓶颈。显式 memory（例如文本日志或键值 store）提供一定透明度，但用户与开发者仍缺乏工具来追踪哪些 memory 项被 retrieval、它们如何影响生成，或被误用。在这方面，RAGChecker（Ru et al., 2024）等诊断工具与 RAMDocs 配合 MADAM-RAG（Wang et al., 2025d）等冲突消解框架，为在不确定性下追踪 memory 使用与 reasoning 提供启发。

此外，超越个体 memory，Shi et al.（2025d）与 Rezazadeh et al.（2025a）强调共享或联邦 memory 系统中集体隐私的新兴重要性，此类系统可能跨多 agent 部署或组织运作。所有这些发展共同表明，需要将信任提升为 memory 设计中的一等原则。

## 7.7.2 Future Perspective

展望未来，我们认为可信 memory 必须围绕三个相互关联的支柱构建：隐私保护、可解释性与幻觉稳健性——每一项都需要架构与算法创新。

在隐私方面，未来系统应支持细粒度权限化 memory、用户治理的保留策略、加密或设备端存储，以及必要时联邦访问（Wu et al., 2025g; Shi et al., 2025d; Rezazadeh et al., 2025a）。差分隐私、memory redaction 与自适应 forgetting（例如基于衰减的模型或用户擦除接口）等技术可作为防止 memory 与泄露的保障（Chhikara et al., 2025）。

可解释性要求超越可见内容，纳入可追踪的访问路径、自我解释的 retrieval，以及可能的反事实 reasoning（例如，没有该 memory 会改变什么？）（OpenAI, 2024; Zhang et al., 2025v）。memory attention 可视化、memory 影响的因果图，以及面向用户的调试工具，可能成为标准组件。

幻觉缓解将受益于冲突检测、多文档 reasoning 与不确定性感知生成的持续进步。低置信度 retrieval 下的弃答、回退到模型先验（Wang et al., 2025c），或多 agent 交叉检查（Hu et al., 2024）等策略具有前景。除行为层面的保障外，新兴的机制可解释性技术提供互补方向，分析内部表示与 reasoning 回路如何促成幻觉输出。表示级 probing 与 reasoning 路径分解等方法可更细粒度地诊断幻觉来源，并为干预与控制提供有原则的工具（Sun et al., 2025f,d）。

长期而言，我们设想 memory 系统由类 OS 抽象治理：分段（Wang et al., 2024k）、版本受控、可审计，并由 agent 与用户共同管理（Packer et al., 2023b）。构建此类系统需要表示学习、系统设计与策略控制的协同努力。随着 LLM agent 开始在持久、开放式环境中运作，可信 memory 将不仅是一项理想特性，而是真实世界部署的基础要求。

## 7.8 Human-Cognitive Connections

## 7.8.1 Look Back

当代 agent memory 系统的架构已与过去一个世纪确立的人类认知基础模型趋同。主流设计将容量受限的 context window 与海量外部向量数据库耦合，映射 Atkinson-Shifrin 多存储模型（Atkinson and Shifrin, 1968），有效实例化了 working memory 与 long-term memory 区分的人工对应物（Baddeley, 2012）。此外，将 agent memory 划分为交互日志、世界知识与基于代码的 skill，与 Tulving 对 episodic、semantic 与 procedural memory 的分类呈现惊人的结构对齐（Tulving, 1972; Squire, 2004）。当前框架（Zhong et al., 2024; Park et al., 2023; Gutierrez et al., 2024; Li et al., 2025l）将这些生物类别操作化为工程产物，其中 episodic memory 提供自传式连续性，semantic memory 提供泛化世界知识。

尽管存在这些结构平行，retrieval 与维持的动态仍存在根本分歧。人类 memory 作为建构过程运作：大脑基于当前认知状态主动重构过往事件，而非回放精确记录（Schacter and Addis, 2007）。相反，多数现有 agent memory 系统依赖 RAG 等逐字 retrieval 机制，将 memory 视为不可变 token 的仓库，通过语义相似度查询（Packer et al., 2023b; Chhikara et al., 2025）。因此，agent 虽拥有对过去的真实记录，却缺乏人类智能所特有的 memory 扭曲、抽象与历史动态重塑的生物能力。

## 7.8.2 Future Perspective

为弥合静态存储与动态认知之间的鸿沟，下一代 agent 必须超越仅靠在线更新，纳入类似生物睡眠的离线 consolidation 机制（Lin et al., 2025b）。借鉴 Complementary Learning Systems（CLS）理论（Kumaran et al., 2016; McClelland et al., 1995），未来架构很可能引入专门的 consolidation 间隔，使 agent 脱离环境交互，投入 memory 重组与生成式回放（Mattar and Daw, 2018）。在这些离线期间，agent 可自主从原始 episodic trace 中 distillation 出可泛化 schema，执行主动 forgetting 以剪除冗余噪声（Anderson and Hulbert, 2021），并在不受实时处理延迟约束的情况下优化内部索引。

最终，这一演化暗示 memory 形式与功能的范式转变：从显式文本 retrieval 转向生成式重构。未来系统可能采用生成式 memory（Zhang et al., 2025d），由 agent 按需综合 latent memory token，映射大脑的重构本性。通过整合类睡眠 consolidation 循环，agent 将从仅仅归档数据的实体，演化为内化经验的实体，通过周期性将庞大 episodic 流压缩为高效 parametric 直觉，解决稳定性–可塑性困境。

## 8 Conclusion

本综述将 agent memory 作为现代 LLM-based agentic 系统的基础组件加以考察。通过 forms、functions 与 dynamics 的统一视角框定现有研究，我们厘清了 agent memory 的概念图景，并将其置于 agentic 智能更广的演化之中。在 forms 层面，我们识别三种主要实现：token-level、parametric 与 latent memory，每一种近年来都经历了独特而快速的进展，反映在表示、适应性与 agent policy 整合方面根本不同的取舍。在 functions 层面，我们超越先前综述常见的长期/短期二分，转而提出更细粒度且更包容的分类，依据其在知识保持、能力累积与任务级 reasoning 中的作用区分 factual、experiential 与 working memory。综合来看，这些视角揭示 memory 不仅是辅助存储机制，而是 agent 借以实现时间连贯性、持续适应与 long-horizon 能力的本质基底。

除组织先前工作外，我们还识别了指向 agent memory 研究下一阶段的关键挑战与新兴方向。特别是 reinforcement learning 的日益整合、multimodal 与多 agent 设定的兴起，以及从以 retrieval 为中心到生成式 memory 范式的转变，暗示一个 memory 系统变得完全可学习、自适应且自组织的未来。此类系统有潜力将大语言模型从强大却静态的生成器，转变为能够持续交互、自我改进并随时间进行有原则 reasoning 的 agent。

我们希望本综述为未来研究提供连贯基础，并成为研究者与实践者的参考。随着 agentic 系统持续成熟，memory 的设计将始终是核心且开放的问题，并很可能在稳健、通用且持久的人工智能发展中扮演决定性角色。

## References

Aadharsh Aadhithya A, Sachin Kumar S, and Soman K. P. Enhancing long-term memory using hierarchical aggregate tree for retrieval augmented generation, 2024. https://arxiv.org/abs/2406.06124.

Saaket Agashe, Jiuzhou Han, Shuyu Gan, Jiachen Yang, Ang Li, and Xin Eric Wang. Agent S: An Open Agentic Framework that Uses Computers Like a Human. In The Thirteenth International Conference on Learning Representations, ICLR 2025, Singapore, April 24-28, 2025. OpenReview.net, 2025.

AgentScope. GitHub - agentscope-ai/ReMe: ReMe: Memory Management Kit for Agents - Remember Me, Refine Me. github.com. https://github.com/agentscope-ai/ReMe, 2025. [Accessed 14-12-2025].

Qingyao Ai, Yichen Tang, Changyue Wang, Jianming Long, Weihang Su, and Yiqun Liu. Memorybench: A benchmark for memory and continual learning in llm systems. arXiv preprint arXiv:2510.17281, 2025.

Reem Aleithan, Haoran Xue, Mohammad Mahdi Mohajer, Elijah Nnorom, Gias Uddin, and Song Wang. Swe-bench+: Enhanced coding benchmark for llms, 2024. https://arxiv.org/abs/2410.06992.

Nick Alonso, Tomas Figliolia, Anthony Ndirango, and Beren Millidge. Toward conversational agents with context and time sensitive long-term memory. CoRR, abs/2406.00057, 2024. doi: 10.48550/ARXIV.2406.00057. https: //doi.org/10.48550/arXiv.2406.00057.

Michael C. Anderson and Justin C. Hulbert. Active forgetting: Adaptation of memory by prefrontal control. Annual Review of Psychology, 72:1–36, January 2021. ISSN 1545-2085. doi: 10.1146/annurev-psych-072720-094140.

Petr Anokhin, Nikita Semenov, Artyom Sorokin, Dmitry Evseev, Andrey Kravchenko, Mikhail Burtsev, and Evgeny Burnaev. Arigraph: Learning knowledge graph world models with episodic memory for llm agents. arXiv preprint arXiv:2407.04363, 2024.

Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, and Hannaneh Hajishirzi. Self-rag: Learning to retrieve, generate, and critique through self-reflection, 2023. https://arxiv.org/abs/2310.11511.

R. C. Atkinson and R. M. Shifrin. Human memory: A proposed system and its control processes. In The Psychology of Learning and Motivation: II, pages xi, 249–xi, 249. Academic Press, Oxford, England, 1968. doi: 10.1016/ S0079-7421(08)60422-3.

Alan Baddeley. Working Memory: Theories, Models, and Controversies. Annual Review of Psychology, 63(Volume 63, 2012):1–29, January 2012. ISSN 0066-4308, 1545-2085. doi: 10.1146/annurev-psych-120710-100422.

Yushi Bai, Xin Lv, Jiajie Zhang, Hongchang Lyu, Jiankai Tang, Zhidian Huang, Zhengxiao Du, Xiao Liu, Aohan Zeng, Lei Hou, Yuxiao Dong, Jie Tang, and Juanzi Li. LongBench: A bilingual, multitask benchmark for long context understanding. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 3119–3137, Bangkok, Thailand, August 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.acl-long.172. https://aclanthology.org/2024.acl-long.172/.

Yushi Bai, Shangqing Tu, Jiajie Zhang, Hao Peng, Xiaozhi Wang, Xin Lv, Shulin Cao, Jiazheng Xu, Lei Hou, Yuxiao Dong, et al. Longbench v2: Towards deeper understanding and reasoning on realistic long-context multitasks. In

Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 3639–3664, 2025.

Alexandre Bailly, Antoine Saubin, Gabriel Kocevar, and Jonathan Bodin. Divide and summarize: improve slm text summarization. Frontiers in Artificial Intelligence, 8:1604034, 2025.

Ali Behrouz, Meisam Razaviyayn, Peilin Zhong, and Vahab Mirrokni. Nested learning: The illusion of deep learning architectures. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, 2025a. https: //openreview.net/forum?id=nbMeRvNb7A.

Ali Behrouz, Peilin Zhong, and Vahab Mirrokni. Titans: Learning to memorize at test time. CoRR, abs/2501.00663, 2025b. doi: 10.48550/ARXIV.2501.00663. https://doi.org/10.48550/arXiv.2501.00663.

Massimo Bini, Ondrej Bohdal, Umberto Michieli, Zeynep Akata, Mete Ozay, and Taha Ceritli. Memlora: Distilling expert adapters for on-device memory systems, 2025. https://arxiv.org/abs/2512.04763.

Weihao Bo, Shan Zhang, Yanpeng Sun, Jingjing Wu, Qunyi Xie, Xiao Tan, Kunbin Chen, Wei He, Xiaofan Li, Na Zhao, Jingdong Wang, and Zechao Li. Agentic learner with grow-and-refine multimodal semantic memory, 2025. https://arxiv.org/abs/2511.21678.

Islem Bouzenia, Premkumar Devanbu, and Michael Pradel. RepairAgent: An Autonomous, LLM-Based Agent fo Program Repair, October 2024. http://arxiv.org/abs/2403.17134. arXiv:2403.17134 [cs].

Jake Bruce, Michael D Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi, Edward Hughes, Matthew Lai, Aditi Mavalankar, Richie Steigerwald, Chris Apps, et al. Genie: Generative interactive environments. In Forty-firs International Conference on Machine Learning, 2024.

Yuxuan Cai, Yipeng Hao, Jie Zhou, Hang Yan, Zhikai Lei, Rui Zhen, Zhenhua Han, Yutao Yang, Junsong Li, Qianjun Pan, Tianyu Huai, Qin Chen, Xin Li, Kai Chen, Bo Zhang, Xipeng Qiu, and Liang He. Building self-evolving agents via experience-driven lifelong learning: A framework and benchmark. CoRR, abs/2508.19005, 2025a. doi: 10.48550/ARXIV.2508.19005. https://doi.org/10.48550/arXiv.2508.19005.

Yuzheng Cai, Siqi Cai, Yuchen Shi, Zihan Xu, Lichao Chen, Yulei Qin, Xiaoyu Tan, Gang Li, Zongyi Li, Haojia Lin, Yong Mao, Ke Li, and Xing Sun. Training-free group relative policy optimization, 2025b. https://arxiv.org/abs/ 2510.08191.

Zefan Cai, Yichi Zhang, Bofei Gao, Yuliang Liu, Tianyu Liu, Keming Lu, Wayne Xiong, Yue Dong, Baobao Chang, Junjie Hu, and Wen Xiao. Pyramidkv: Dynamic KV cache compression based on pyramidal information funneling. CoRR, abs/2406.02069, 2024. doi: 10.48550/ARXIV.2406.02069. https://doi.org/10.48550/arXiv.2406.02069.

Zhicheng Cai, Xinyuan Guo, Yu Pei, Jiangtao Feng, Jinsong Su, Jiangjie Chen, Ya-Qin Zhang, Wei-Ying Ma, Mingxuan Wang, and Hao Zhou. Flex: Continuous agent evolution via forward learning from experience, 2025c. https://arxiv.org/abs/2511.06449.

CAMEL-AI. Workforce — camel-ai documentation. https://docs.camel-ai.org/key\_modules/workforce, 2025. Accessed: 2025-08-09.

Jiaqi Cao, Jiarui Wang, Rubin Wei, Qipeng Guo, Kai Chen, Bowen Zhou, and Zhouhan Lin. Memory decoder: A pretrained, plug-and-play memory for large language models. CoRR, abs/2508.09874, 2025a. doi: 10.48550/ARXIV. 2508.09874. https://doi.org/10.48550/arXiv.2508.09874.

Nicola De Cao, Wilker Aziz, and Ivan Titov. Editing factual knowledge in language models. In Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, pages 6491–6506, 2021.

Zouying Cao, Jiaji Deng, Li Yu, Weikang Zhou, Zhaoyang Liu, Bolin Ding, and Hai Zhao. Remember me, refine me: A dynamic procedural memory framework for experience-driven agent evolution, 2025b. https://arxiv.org/abs/2512. 10696.

Maitreyi Chatterjee and Devansh Agarwal. Semantic anchoring in agentic memory: Leveraging linguistic structures for persistent conversational context. CoRR, abs/2508.12630, 2025. doi: 10.48550/ARXIV.2508.12630. https: //doi.org/10.48550/arXiv.2508.12630.

Baian Chen, Chang Shu, Ehsan Shareghi, Nigel Collier, Karthik Narasimhan, and Shunyu Yao. Fireact: Toward language agent fine-tuning, 2023a. https://arxiv.org/abs/2310.05915.

Dake Chen, Hanbin Wang, Yunhao Huo, Yuzhao Li, and Haoyang Zhang. GameGPT: Multi-agent Collaborative Framework for Game Development. CoRR, abs/2310.08067, 2023b. doi: 10.48550/ARXIV.2310.08067.

Ding Chen, Simin Niu, Kehang Li, Peng Liu, Xiangping Zheng, Bo Tang, Xinchi Li, Feiyu Xiong, and Zhiyu Li. Halumem: Evaluating hallucinations in memory systems of agents. arXiv preprint arXiv:2511.03506, 2025a.

Guoxin Chen, Zile Qiao, Xuanzhong Chen, Donglei Yu, Haotian Xu, Wayne Xin Zhao, Ruihua Song, Wenbiao Yin, Huifeng Yin, Liwen Zhang, Kuan Li, Minpeng Liao, Yong Jiang, Pengjun Xie, Fei Huang, and Jingren Zhou. Iterresearch: Rethinking long-horizon agents via markovian state reconstruction, 2025b. https://arxiv.org/abs/ 2511.07327.

Kaiyuan Chen, Yixin Ren, Yang Liu, Xiaobo Hu, Haotong Tian, Tianbao Xie, Fangfu Liu, Haoye Zhang, Hongzhang Liu, Yuan Gong, Chen Sun, Han Hou, Hui Yang, James Pan, Jianan Lou, Jiayi Mao, Jizheng Liu, Jinpeng Li, Kangyi Liu, Kenkun Liu, Rui Wang, Run Li, Tong Niu, Wenlong Zhang, Wenqi Yan, Xuanzheng Wang, Yuchen Zhang, Yi-Hsin Hung, Yuan Jiang, Zexuan Liu, Zihan Yin, Zijian Ma, and Zhiwen Mo. xbench: Tracking agents productivity scaling with profession-aligned real-world evaluations, 2025c. https://arxiv.org/abs/2506.13651.

Nuo Chen, Hongguang Li, Jianhui Chang, Juhua Huang, Baoyuan Wang, and Jia Li. Compress to impress: Unleashing the potential of compressive memory in real-world long-term conversations. In Owen Rambow, Leo Wanner, Marianna Apidianaki, Hend Al-Khalifa, Barbara Di Eugenio, and Steven Schockaert, editors, Proceedings of the 31st International Conference on Computational Linguistics, COLING 2025, Abu Dhabi, UAE, January 19-24, 2025, pages 755–773. Association for Computational Linguistics, 2025d. https://aclanthology.org/2025.coling-main.51/.

Qiuhui Chen, Qiang Fu, Hao Bai, and Yi Hong. Longformer: Longitudinal transformer for alzheimer’s disease classification with structural mris. In IEEE/CVF Winter Conference on Applications of Computer Vision, WACV 2024, Waikoloa, HI, USA, January 3-8, 2024, pages 3563–3572. IEEE, 2024a. doi: 10.1109/WACV57701.2024.00354. https://doi.org/10.1109/WACV57701.2024.00354.

Weishu Chen, Jinyi Tang, Zhouhui Hou, Shihao Han, Mingjie Zhan, Zhiyuan Huang, Delong Liu, Jiawei Guo, Zhicheng Zhao, and Fei Su. Moom: Maintenance, organization and optimization of memory in ultra-long role-playing dialogues, 2025e. https://arxiv.org/abs/2509.11860.

Xiuying Chen, Shen Gao, Mingzhe Li, Qingqing Zhu, Xin Gao, and Xiangliang Zhang. Write summary step-by-step: A pilot study of stepwise summarization. IEEE/ACM Transactions on Audio, Speech, and Language Processing, 32: 1406–1415, 2024b.

Yinpeng Chen, DeLesley Hutchins, Aren Jansen, Andrey Zhmoginov, David Racz, and Jesper Andersen. Melodi: Exploring memory compression for long contexts, 2024c. https://arxiv.org/abs/2410.03156.

Zhaorun Chen, Zhuokai Zhao, Kai Zhang, Bo Liu, Qi Qi, Yifan Wu, Tarun Kalluri, Sara Cao, Yuanhao Xiong, Haibo Tong, Huaxiu Yao, Hengduo Li, Jiacheng Zhu, Xian Li, Dawn Song, Bo Li, Jason Weston, and Dat Huynh. Scaling agent learning via experience synthesis, 2025f. https://arxiv.org/abs/2511.03773.

Ho Kei Cheng and Alexander G. Schwing. Xmem: Long-term video object segmentation with an atkinson-shifrin memory model, 2022. https://arxiv.org/abs/2207.07115.

Alexis Chevalier, Alexander Wettig, Anirudh Ajith, and Danqi Chen. Adapting language models to compress contexts. In Houda Bouamor, Juan Pino, and Kalika Bali, editors, Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, EMNLP 2023, Singapore, December 6-10, 2023, pages 3829–3846. Association fo Computational Linguistics, 2023. doi: 10.18653/V1/2023.EMNLP-MAIN.232. https://doi.org/10.18653/v1/2023. emnlp-main.232.

Maxime Chevalier-Boisvert, Dzmitry Bahdanau, Salem Lahlou, Lucas Willems, Chitwan Saharia, Thien Huu Nguyen, and Yoshua Bengio. Babyai: A platform to study the sample eficiency of grounded language learning, 2019. https://arxiv.org/abs/1810.08272.

Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh, and Deshraj Yadav. Mem0: Building production-ready ai agents with scalable long-term memory. arXiv preprint arXiv:2504.19413, 2025.

Eunseong Choi, June Park, Hyeri Lee, and Jongwuk Lee. Conflict-aware soft prompting for retrieval-augmented generation. CoRR, abs/2508.15253, 2025. doi: 10.48550/ARXIV.2508.15253. https://doi.org/10.48550/arXiv.2508. 15253.

Cognee. GitHub - topoteretes/cognee: Memory for AI Agents in 6 lines of code. https://github.com/topoteretes/ cognee, 2025. [Accessed 14-12-2025].

Nelson Cowan. Working Memory Underpins Cognitive Development, Learning, and Education. Educational psychology review, 26(2):197–223, June 2014. ISSN 1040-726X. doi: 10.1007/s10648-013-9246-y.

Tri Dao. Flashattention-2: Faster attention with better parallelism and work partitioning. In The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenReview.net, 2024. https://openreview.net/forum?id=mZn2Xyh9Ec.

Nicola De Cao, Wilker Aziz, and Ivan Titov. Editing factual knowledge in language models. In Marie-Francine Moens, Xuanjing Huang, Lucia Specia, and Scott Wen-tau Yih, editors, Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, pages 6491–6506, Online and Punta Cana, Dominican Republic, November 2021. Association for Computational Linguistics. doi: 10.18653/v1/2021.emnlp-main.522. https://aclanthology.org/2021.emnlp-main.522/.

DeepSeek-AI, Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, Xiaokang Zhang, Xingkai Yu, Yu Wu, Z. F. Wu, Zhibin Gou, Zhihong Shao, Zhuoshu Li, Ziyi Gao, Aixin Liu, Bing Xue, Bingxuan Wang, Bochao Wu, Bei Feng, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, Damai Dai, Deli Chen, Dongjie Ji, Erhang Li, Fangyun Lin, Fucong Dai, Ful Luo, Guangbo Hao, Guanting Chen, Guowei Li, H. Zhang, Han Bao, Hanwei Xu, Haocheng Wang, Honghui Ding, Huajian Xin, Huazuo Gao, Hui Qu, Hui Li, Jianzhong Guo, Jiashi Li, Jiawei Wang, Jingchang Chen, Jingyang Yuan, Junjie Qiu, Junlong Li, J. L. Cai, Jiaqi Ni, Jian Liang, Jin Chen, Kai Dong, Kai Hu, Kaige Gao, Kang Guan, Kexin Huang, Kuai Yu, Lean Wang, Lecong Zhang, Liang Zhao, Litong Wang, Liyue Zhang, Lei Xu, Leyi Xia, Mingchuan Zhang, Minghua Zhang, Minghui Tang, Meng Li, Miaojun Wang, Mingming Li, Ning Tian, Panpan Huang, Peng Zhang, Qiancheng Wang, Qinyu Chen, Qiushi Du, Ruiqi Ge, Ruisong Zhang, Ruizhe Pan, Runji Wang, R. J. Chen, R. L. Jin, Ruyi Chen, Shanghao Lu, Shangyan Zhou, Shanhuang Chen, Shengfeng Ye, Shiyu Wang, Shuiping Yu, Shunfeng Zhou, Shuting Pan, S. S. Li, Shuang Zhou, Shaoqing Wu, Shengfeng Ye, Tao Yun, Tian Pei, Tianyu Sun, T. Wang, Wangding Zeng, Wanjia Zhao, Wen Liu, Wenfeng Liang, Wenjun Gao, Wenqin Yu, Wentao Zhang, W. L. Xiao, Wei An, Xiaodong Liu, Xiaohan Wang, Xiaokang Chen, Xiaotao Nie, Xin Cheng, Xin Liu, Xin Xie, Xingchao Liu, Xinyu Yang, Xinyuan Li, Xuecheng Su, Xuheng Lin, X. Q. Li, Xiangyue Jin, Xiaojin Shen, Xiaosha Chen, Xiaowen Sun, Xiaoxiang Wang, Xinnan Song, Xinyi Zhou, Xianzu Wang, Xinxia Shan, Y. K. Li, Y. Q. Wang, Y. X. Wei, Yang Zhang, Yanhong Xu, Yao Li, Yao Zhao, Yaofeng Sun, Yaohui Wang, Yi Yu, Yichao Zhang, Yifan Shi, Yiliang Xiong, Ying He, Yishi Piao, Yisong Wang, Yixuan Tan, Yiyang Ma, Yiyuan Liu, Yongqiang Guo, Yuan Ou, Yuduan Wang, Yue Gong, Yuheng Zou, Yujia He, Yunfan Xiong, Yuxiang Luo, Yuxiang You, Yuxuan Liu, Yuyang Zhou, Y. X. Zhu, Yanhong Xu, Yanping Huang, Yaohui Li, Yi Zheng, Yuchen Zhu, Yunxian Ma, Ying Tang, Yukun Zha, Yuting Yan, Z. Z. Ren, Zehui Ren, Zhangli Sha, Zhe Fu, Zhean Xu, Zhenda Xie, Zhengyan Zhang, Zhewen Hao, Zhicheng Ma, Zhigang Yan, Zhiyu Wu, Zihui Gu, Zijia Zhu, Zijun Liu, Zilin Li, Ziwei Xie, Ziyang Song, Zizheng Pan, Zhen Huang, Zhipeng Xu, Zhongyu Zhang, and Zhen Zhang. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning, 2025. https://arxiv.org/abs/2501.12948.

Xiang Deng, Yu Gu, Boyuan Zheng, Shijie Chen, Samual Stevens, Boshi Wang, Huan Sun, and Yu Su. Mind2Web: Towards a Generalist Agent for the Web. In Alice Oh, Tristan Naumann, Amir Globerson, Kate Saenko, Moritz Hardt, and Sergey Levine, editors, Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023, 2023. http://papers.nips.cc/paper\_files/paper/2023/hash/ 5950bf290a1570ea401bf98882128160-Abstract-Datasets\_and\_Benchmarks.html.

Yang Deng, Xuan Zhang, Wenxuan Zhang, Yifei Yuan, See-Kiong Ng, and Tat-Seng Chua. On the multi-turn instruction following for conversational web agents. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 8795–8812, Bangkok, Thailand, August 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.acl-long.477. https://aclanthology.org/2024.acl-long.477/.

Junnan Dong, Siyu An, Yifei Yu, Qian-Wen Zhang, Linhao Luo, Xiao Huang, Yunsheng Wu, Di Yin, and Xing Sun. Youtu-graphrag: Vertically unified agents for graph retrieval-augmented complex reasoning, 2025a. https: //arxiv.org/abs/2508.19855.

Yifei Dong, Fengyi Wu, Guangyu Chen, Zhi-Qi Cheng, Qiyu Hu, Yuxuan Zhou, Jingdong Sun, Jun-Yan He, Qi Dai, and Alexander G Hauptmann. Unified world models: Memory-augmented planning and foresight for visual navigation. arXiv preprint arXiv:2510.08713, 2025b.

Yiming Du, Hongru Wang, Zhengyi Zhao, Bin Liang, Baojun Wang, Wanjun Zhong, Zezhong Wang, and Kam-Fai Wong. PerLTQA: A personal long-term memory dataset for memory classification, retrieval, and fusion in question answering. In Proceedings of the 10th SIGHAN Workshop on Chinese Language Processing (SIGHAN-10), pages 152–164, Bangkok, Thailand, August 2024. Association for Computational Linguistics. https://aclanthology.org/ 2024.sighan-1.18/.

Yiming Du, Wenyu Huang, Danna Zheng, Zhaowei Wang, Sebastien Montella, Mirella Lapata, Kam-Fai Wong,

and Jef Z Pan. Rethinking memory in ai: Taxonomy, operations, topics, and future directions. arXiv preprint arXiv:2505.00675, 2025a.

Yiming Du, Bingbing Wang, Yang He, Bin Liang, Baojun Wang, Zhongyang Li, Lin Gui, Jef Z. Pan, Ruifeng Xu, and Kam-Fai Wong. Memguide: Intent-driven memory selection for goal-oriented multi-session llm agents, 2025b. https://arxiv.org/abs/2505.20231.

Zane Durante, Qiuyuan Huang, Naoki Wake, Ran Gong, Jae Sung Park, Bidipta Sarkar, Rohan Taori, Yusuke Noda, Demetri Terzopoulos, Yejin Choi, Katsushi Ikeuchi, Hoi Vo, Li Fei-Fei, and Jianfeng Gao. Agent ai: Surveying the horizons of multimodal interaction, 2024. https://arxiv.org/abs/2401.03568.

Darren Edge, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva Mody, Steven Truitt, Dasha Metropolitansky, Robert Osazuwa Ness, and Jonathan Larson. From local to global: A graph rag approach to query-focused summarization, 2025. https://arxiv.org/abs/2404.16130.

Yue Fan, Xiaojian Ma, Rongpeng Su, Jun Guo, Rujie Wu, Xi Chen, and Qing Li. Embodied videoagent: Persistent memory from egocentric videos and embodied sensors enables dynamic scene understanding. CoRR, abs/2501.00358, 2025. doi: 10.48550/ARXIV.2501.00358. https://doi.org/10.48550/arXiv.2501.00358.

Jinyuan Fang, Yanwen Peng, Xi Zhang, Yingxu Wang, Xinhao Yi, Guibin Zhang, Yi Xu, Bin Wu, Siwei Liu, Zihao Li, Zhaochun Ren, Nikos Aletras, Xi Wang, Han Zhou, and Zaiqiao Meng. A comprehensive survey of self-evolving ai agents: A new paradigm bridging foundation models and lifelong agentic systems, 2025a. https://arxiv.org/abs/2508.07407.

Jizhan Fang, Xinle Deng, Haoming Xu, Ziyan Jiang, Yuqi Tang, Ziwen Xu, Shumin Deng, Yunzhi Yao, Mengru Wang, Shuofei Qiao, et al. Lightmem: Lightweight and eficient memory-augmented generation. arXiv preprint arXiv:2510.18866, 2025b.

Junfeng Fang, Houcheng Jiang, Kun Wang, Yunshan Ma, Shi Jie, Xiang Wang, Xiangnan He, and Tat seng Chua. Alphaedit: Null-space constrained knowledge editing for language models, 2025c. https://arxiv.org/abs/2410.02355.

Runnan Fang, Yuan Liang, Xiaobin Wang, Jialong Wu, Shuofei Qiao, Pengjun Xie, Fei Huang, Huajun Chen, and Ningyu Zhang. Memp: Exploring agent procedural memory, 2025d. https://arxiv.org/abs/2508.06433.

Erhu Feng, Wenbo Zhou, Zibin Liu, Le Chen, Yunpeng Dong, Cheng Zhang, Yisheng Zhao, Dong Du, Zhi-Hua Zhou, Yubin Xia, and Haibo Chen. Get experience from practice: LLM agents with record & replay. CoRR, abs/2505.17716, 2025. doi: 10.48550/ARXIV.2505.17716. https://doi.org/10.48550/arXiv.2505.17716.

Xidong Feng, Ziyu Wan, Mengyue Yang, Ziyan Wang, Girish A. Koushik, Yali Du, Ying Wen, and Jun Wang. Natural language reinforcement learning, 2024. https://arxiv.org/abs/2402.07157.

Zafeirios Fountas, Martin Benfeghoul, Adnan Oomerjee, Fenia Christopoulou, Gerasimos Lampouras, Haitham Bou-Ammar, and Jun Wang. Human-inspired episodic memory for infinite context llms. In The Thirteenth International Conference on Learning Representations, ICLR 2025, Singapore, April 24-28, 2025. OpenReview.net, 2025. https://openreview.net/forum?id=BI2int5SAC.

Chen Gao, Xiaochong Lan, Zhihong Lu, Jinzhu Mao, Jinghua Piao, Huandong Wang, Depeng Jin, and Yong Li. S\(^\mbox3\): Social-network Simulation System with Large Language Model-Empowered Agents. CoRR, abs/2307.14984, 2023a. doi: 10.48550/ARXIV.2307.14984.

Hang Gao and Yongfeng Zhang. Memory sharing for large language model based agents. CoRR, abs/2404.09982, 2024a. doi: 10.48550/ARXIV.2404.09982. https://doi.org/10.48550/arXiv.2404.09982.

Hang Gao and Yongfeng Zhang. Memory Sharing for Large Language Model based Agents. CoRR, abs/2404.09982, 2024b. doi: 10.48550/ARXIV.2404.09982.

Hang Gao and Yongfeng Zhang. PTR: Precision-Driven Tool Recommendation for Large Language Models. CoRR, abs/2411.09613, 2024c. doi: 10.48550/ARXIV.2411.09613. https://doi.org/10.48550/arXiv.2411.09613. arXiv: 2411.09613.

Huan-ang Gao, Jiayi Geng, Wenyue Hua, Mengkang Hu, Xinzhe Juan, Hongzhang Liu, Shilong Liu, Jiahao Qiu, Xuan Qi, Yiran Wu, Hongru Wang, Han Xiao, Yuhang Zhou, Shaokun Zhang, Jiayi Zhang, Jinyu Xiang, Yixiong Fang, Qiwen Zhao, Dongrui Liu, Qihan Ren, Cheng Qian, Zhenhailong Wang, Minda Hu, Huazheng Wang, Qingyun Wu, Heng Ji, and Mengdi Wang. A survey of self-evolving agents: On path to artificial super intelligence, August 2025.

Luyu Gao, Xueguang Ma, Jimmy Lin, and Jamie Callan. Precise zero-shot dense retrieval without relevance labels. In Anna Rogers, Jordan L. Boyd-Graber, and Naoaki Okazaki, editors, Proceedings of the 61st Annual Meeting of

the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2023, Toronto, Canada, July 9-14, 2023, pages 1762–1777. Association for Computational Linguistics, 2023b. doi: 10.18653/V1/2023.ACL-LONG.99. https://doi.org/10.18653/v1/2023.acl-long.99.

Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Jinliu Pan, Yuxi Bi, Yi Dai, Jiawei Sun, Meng Wang, and Haofen Wang. Retrieval-augmented generation for large language models: A survey, 2024. https://arxiv.org/abs/2312.10997.

Tao Ge, Jing Hu, Lei Wang, Xun Wang, Si-Qing Chen, and Furu Wei. In-context Autoencoder for Context Compression in a Large Language Model. In The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenReview.net, 2024.

Samuel J. Gershman, Ila Fiete, and Kazuki Irie. Key-value memory in the brain. CoRR, abs/2501.02950, 2025. doi: 10.48550/ARXIV.2501.02950. https://doi.org/10.48550/arXiv.2501.02950.

Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Alex Vaughan, et al. The llama 3 herd of models. arXiv preprint arXiv:2407.21783, 2024.

Albert Gu and Tri Dao. Mamba: Linear-time sequence modeling with selective state spaces, 2024. https://arxiv.org/ abs/2312.00752.

Yanjiang Guo, Lucy Xiaoyang Shi, Jianyu Chen, and Chelsea Finn. Ctrl-world: A controllable generative world mode for robot manipulation. arXiv preprint arXiv:2510.10125, 2025.

Saket Gurukar and Asim Kadav. Long-vmnet: Accelerating long-form video understanding via fixed memory, 2025. https://arxiv.org/abs/2503.13707.

Bernal Jimenez Gutierrez, Yiheng Shu, Yu Gu, Michihiro Yasunaga, and Yu Su. HippoRAG: Neurobiologically inspired long-term memory for large language models. In Advances in Neural Information Processing Systems, 2024.

Bernal Jiménez Gutiérrez, Yiheng Shu, Weijian Qi, Sizhe Zhou, and Yu Su. From rag to memory: Non-parametric continual learning for large language models, 2025. https://arxiv.org/abs/2502.14802.

Dongge Han, Camille Couturier, Daniel Madrigal Diaz, Xuchao Zhang, Victor Rühle, and Saravan Rajmohan. LEGOMem: Modular Procedural Memory for Multi-agent LLM Systems for Workflow Automation, October 2025a. http://arxiv.org/abs/2510.04851. arXiv:2510.04851 [cs].

Haoyu Han, Yu Wang, Harry Shomer, Kai Guo, Jiayuan Ding, Yongjia Lei, Mahantesh Halappanavar, Ryan A. Rossi, Subhabrata Mukherjee, Xianfeng Tang, Qi He, Zhigang Hua, Bo Long, Tong Zhao, Neil Shah, Amin Javari, Yinglong Xia, and Jiliang Tang. Retrieval-augmented generation with graphs (graphrag), 2025b. https: //arxiv.org/abs/2501.00309.

Jinyi Han, Xinyi Wang, Haiquan Zhao, Tingyun li, Zishang Jiang, Sihang Jiang, Jiaqing Liang, Xin Lin, Weikang Zhou, Zeye Sun, Fei Yu, and Yanghua Xiao. A stitch in time saves nine: Proactive self-refinement for language models, 2025c. https://arxiv.org/abs/2508.12903.

Jackson Hassell, Dan Zhang, Hannah Kim, Tom Mitchell, and Estevam Hruschka. Learning from supervision with semantic and episodic memory: A reflective approach to agent adaptation. arXiv preprint arXiv:2510.19897, 2025.

Bo He, Hengduo Li, Young Kyun Jang, Menglin Jia, Xuefei Cao, Ashish Shah, Abhinav Shrivastava, and Ser-Nam Lim. MA-LMM: Memory-Augmented Large Multimodal Model for Long-Term Video Understanding. In IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2024, Seattle, WA, USA, June 16-22, 2024, pages 13504–13514. IEEE, 2024. doi: 10.1109/CVPR52733.2024.01282.

Junqing He, Liang Zhu, Rui Wang, Xi Wang, Gholamreza Hafari, and Jiaxing Zhang. MADial-bench: Towards real-world evaluation of memory-augmented dialogue generation. In Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers), pages 9902–9921, Albuquerque, New Mexico, April 2025. Association for Computational Linguistics. ISBN 979-8-89176-189-6. doi: 10.18653/v1/2025.naacl-long.499. https://aclanthology.org/2025.naacl-long.499/.

Pengcheng He, Xiaodong Liu, Jianfeng Gao, and Weizhu Chen. Deberta: Decoding-enhanced bert with disentangled attention. arXiv preprint arXiv:2006.03654, 2020.

Dan Hendrycks, Dawn Song, Christian Szegedy, Honglak Lee, Yarin Gal, Erik Brynjolfsson, Sharon Li, Andy Zou, Lionel Levine, Bo Han, et al. A definition of agi. arXiv preprint arXiv:2510.18212, 2025.

Xanh Ho, Anh-Khoa Duong Nguyen, Saku Sugawara, and Akiko Aizawa. Constructing a multi-hop qa dataset for comprehensive evaluation of reasoning steps, 2020. https://arxiv.org/abs/2011.01060.

Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng Cheng, Jinlin Wang, Ceyao Zhang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, Liyang Zhou, Chenyu Ran, Lingfeng Xiao, Chenglin Wu, and Jürgen Schmidhuber. MetaGPT: Meta programming for A multi-agent collaborative framework. In The Twelfth International Conference on Learning Representations, 2024.

Cheng-Ping Hsieh, Simeng Sun, Samuel Kriman, Shantanu Acharya, Dima Rekesh, Fei Jia, Yang Zhang, and Boris Ginsburg. Ruler: What’s the real context size of your long-context language models? arXiv preprint arXiv:2404.06654, 2024.

Chuanrui Hu, Xingze Gao, Zuyi Zhou, Dannong Xu, Yi Bai, Xintong Li, Hui Zhang, Tong Li, Chong Zhang, Lidong Bing, and Yafeng Deng. Evermemos: A self-organizing memory operating system for structured long-horizon reasoning, 2026a. https://arxiv.org/abs/2601.02163.

Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. LoRA: Low-rank adaptation of large language models. In The Tenth International Conference on Learning Representations, 2022.

Mengkang Hu, Tianxing Chen, Qiguang Chen, Yao Mu, Wenqi Shao, and Ping Luo. HiAgent: Hierarchical Working Memory Management for Solving Long-Horizon Agent Tasks with Large Language Model. In Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and Mohammad Taher Pilehvar, editors, Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2025, Vienna, Austria, July 27 - August 1, 2025, pages 32779–32798. Association for Computational Linguistics, 2025a.

Shengran Hu, Cong Lu, and Jef Clune. Automated design of agentic systems. In The Thirteenth International Conference on Learning Representations, 2025b.

Xiangkun Hu, Dongyu Ru, Lin Qiu, Qipeng Guo, Tianhang Zhang, Yang Xu, Yun Luo, Pengfei Liu, Yue Zhang, and Zheng Zhang. Refchecker: Reference-based fine-grained hallucination checker and benchmark for large language models. arXiv preprint arXiv:2405.14486, 2024.

Yuanzhe Hu, Yu Wang, and Julian McAuley. Evaluating memory in llm agents via incremental multi-turn interactions. arXiv preprint arXiv:2507.05257, 2025c.

Yuyang Hu, Jiongnan Liu, Jiejun Tan, Yutao Zhu, and Zhicheng Dou. Memory matters more: Event-centric memory as a logic map for agent searching and reasoning, 2026b. https://arxiv.org/abs/2601.04726.

Jen-tse Huang, Kaiser Sun, Wenxuan Wang, and Mark Dredze. Language Models Do Not Have Human-Like Working Memory, September 2025a.

Jiani Huang, Xingchen Zou, Lianghao Xia, and Qing Li. Mr.rec: Synergizing memory and reasoning for personalized recommendation assistant with llms. CoRR, abs/2510.14629, 2025b. doi: 10.48550/ARXIV.2510.14629. https: //doi.org/10.48550/arXiv.2510.14629.

Tenghao Huang, Kinjal Basu, Ibrahim Abdelaziz, Pavan Kapanipathi, Jonathan May, and Muhao Chen. R2D2: Remembering, Replaying and Dynamic Decision Making with a Reflective Agentic Memory. In Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and Mohammad Taher Pilehvar, editors, Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2025, Vienna, Austria, July 27 - August 1, 2025, pages 30318–30330. Association for Computational Linguistics, 2025c. https://aclanthology.org/ 2025.acl-long.1464/.

Xu Huang, Jianxun Lian, Yuxuan Lei, Jing Yao, Defu Lian, and Xing Xie. Recommender AI agent: Integrating large language models for interactive recommendations. ACM Trans. Inf. Syst., 43(4):96:1–96:33, 2025d. doi: 10.1145/3731446. https://doi.org/10.1145/3731446.

Zeyu Huang, Yikang Shen, Xiaofeng Zhang, Jie Zhou, Wenge Rong, and Zhang Xiong. Transformer-patcher: One mistake worth one neuron, 2023. https://arxiv.org/abs/2301.09785.

Md Ashraful Islam, Mohammed Eunus Ali, and Md Rizwan Parvez. MapCoder: Multi-Agent Code Generation for Competitive Problem Solving. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar, editors, Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2024, Bangkok, Thailand, August 11-16, 2024, pages 4912–4944. Association for Computational Linguistics, 2024. doi: 10.18653/V1/2024.ACL-LONG.269. https://doi.org/10.18653/v1/2024.acl-long.269.

Kai Tzu iunn Ong, Namyoung Kim, Minju Gwak, Hyungjoo Chae, Taeyoon Kwon, Yohan Jo, Seung won Hwang, Dongha Lee, and Jinyoung Yeo. Towards lifelong dialogue agents via timeline-based memory management, 2025. https://arxiv.org/abs/2406.10996.

Jingyi Jia and Qinbin Li. Autotool: Eficient tool selection for large language model agents, November 2025.

Zixi Jia, Qinghua Liu, Hexiao Li, Yuyan Chen, and Jiqiang Liu. Evaluating the long-term memory of large language models. In Findings of the Association for Computational Linguistics: ACL 2025, pages 19759–19777, Vienna, Austria, July 2025. Association for Computational Linguistics. ISBN 979-8-89176-256-5. doi: 10.18653/v1/2025. findings-acl.1014. https://aclanthology.org/2025.findings-acl.1014/.

Bowen Jiang, Zhuoqun Hao, Young-Min Cho, Bryan Li, Yuan Yuan, Sihao Chen, Lyle Ungar, Camillo J Taylor, and Dan Roth. Know me, respond to me: Benchmarking llms for dynamic user profiling and personalized responses at scale. arXiv preprint arXiv:2504.14225, 2025a.

Dongming Jiang, Yi Li, Guanpeng Li, and Bingzhe Li. Magma: A multi-graph based agentic memory architecture fo ai agents, 2026. https://arxiv.org/abs/2601.03236.

Huiqiang Jiang, Qianhui Wu, Chin-Yew Lin, Yuqing Yang, and Lili Qiu. LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models. In Houda Bouamor, Juan Pino, and Kalika Bali, editors, Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, EMNLP 2023, Singapore, December 6-10, 2023, pages 13358–13376. Association for Computational Linguistics, 2023. doi: 10.18653/V1/2023. EMNLP-MAIN.825.

Huiqiang Jiang, Qianhui Wu, Xufang Luo, Dongsheng Li, Chin-Yew Lin, Yuqing Yang, and Lili Qiu. LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar, editors, Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2024, Bangkok, Thailand, August 11-16, 2024, pages 1658–1677. Association for Computational Linguistics, 2024. doi: 10.18653/V1/2024.ACL-LONG.91.

Jiantong Jiang, Peiyu Yang, Rui Zhang, and Feng Liu. Towards eficient large language model serving: A survey on system-aware KV cache optimization. TechRxiv, 2025b. doi: 10.36227/techrxiv.176046306.66521015/v2. http: //dx.doi.org/10.36227/techrxiv.176046306.66521015/v2.

Tao Jiang, Zichuan Lin, Lihe Li, Yi-Chen Li, Cong Guan, Lei Yuan, Zongzhang Zhang, Yang Yu, and Deheng Ye. Multi-agent in-context coordination via decentralized memory retrieval. arXiv preprint arXiv:2511.10030, 2025c.

Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik R. Narasimhan. SWE-bench: Can language models resolve real-world github issues? In The Twelfth International Conference on Learning Representations, 2024.

Bowen Jin, Hansi Zeng, Zhenrui Yue, Dong Wang, Hamed Zamani, and Jiawei Han. Search-r1: Training llms to reason and leverage search engines with reinforcement learning. CoRR, abs/2503.09516, 2025. doi: 10.48550/ARXIV.2503. 09516. https://doi.org/10.48550/arXiv.2503.09516.

Kumara Kahatapitiya, Kanchana Ranasinghe, Jongwoo Park, and Michael S Ryoo. Language repository for long video understanding. In Findings of the Association for Computational Linguistics: ACL 2025, pages 5627–5646, 2025.

Zhao Kaiya, Michelangelo Naim, Jovana Kondic, Manuel Cortes, Jiaxin Ge, Shuying Luo, Guangyu Robert Yang, and Andrew Ahn. Lyfe agents: Generative agents for low-cost real-time social interactions, 2023. https://arxiv.org/abs/ 2310.02172.

Jiazheng Kang, Mingming Ji, Zhe Zhao, and Ting Bai. Memory os of ai agent, 2025a. https://arxiv.org/abs/2506.06326.

Jikun Kang, Wenqi Wu, Filippos Christianos, Alex J. Chan, Fraser Greenlee, George Thomas, Marvin Purtorab, and Andy Toulis. LM2: large memory models. CoRR, abs/2502.06049, 2025b. doi: 10.48550/ARXIV.2502.06049. https://doi.org/10.48550/arXiv.2502.06049.

Minki Kang, Wei-Ning Chen, Dongge Han, Huseyin A. Inan, Lukas Wutschitz, Yanzhi Chen, Robert Sim, and Saravan Rajmohan. Acon: Optimizing context compression for long-horizon llm agents, October 2025c.

Dongkyu Kim, Byoungwook Kim, Donggeon Han, and Matous Eibich. Autorag: Automated framework for optimization of retrieval augmented generation pipeline. CoRR, abs/2410.20878, 2024a. doi: 10.48550/ARXIV.2410.20878. https://doi.org/10.48550/arXiv.2410.20878.

Gangwoo Kim, Sungdong Kim, Byeongguk Jeon, Joonsuk Park, and Jaewoo Kang. Tree of clarifications: Answering ambiguous questions with retrieval-augmented large language models, 2023a. https://arxiv.org/abs/2310.14696.

Hana Kim, Kai Tzu iunn Ong, Seoyeon Kim, Dongha Lee, and Jinyoung Yeo. Commonsense-augmented memory construction and management in long-term conversations via context-aware persona refinement, 2024b. https: //arxiv.org/abs/2401.14215.

Hyuntak Kim and Byung-Hak Kim. Nexussum: Hierarchical llm agents for long-form narrative summarization. arXiv preprint arXiv:2505.24575, 2025.

Namyoung Kim, Kai Tzu-iunn Ong, Yeonjun Hwang, Minseok Kang, Iiseo Jihn, Gayoung Kim, Minju Kim, and Jinyoung Yeo. PRINCIPLES: synthetic strategy memory for proactive dialogue agents. CoRR, abs/2509.17459, 2025a. doi: 10.48550/ARXIV.2509.17459. https://doi.org/10.48550/arXiv.2509.17459.

Sangyeop Kim, Yohan Lee, Sanghwa Kim, Hyunjong Kim, and Sungzoon Cho. Pre-storage reasoning for episodic memory: Shifting inference burden to memory for personalized dialogue. CoRR, abs/2509.10852, 2025b. doi: 10.48550/ARXIV.2509.10852. https://doi.org/10.48550/arXiv.2509.10852.

Taewoon Kim, Michael Cochez, Vincent François-Lavet, Mark A. Neerincx, and Piek Vossen. A machine with short-term, episodic, and semantic memory systems. In Brian Williams, Yiling Chen, and Jennifer Neville, editors, Thirty-Seventh AAAI Conference on Artificial Intelligence, AAAI 2023, Thirty-Fifth Conference on Innovative Applications of Artificial Intelligence, IAAI 2023, Thirteenth Symposium on Educational Advances in Artificial Intelligence, EAAI 2023, Washington, DC, USA, February 7-14, 2023, pages 48–56. AAAI Press, 2023b. doi: 10.1609/AAAI.V37I1.25075. https://doi.org/10.1609/aaai.v37i1.25075.

Dharshan Kumaran, Demis Hassabis, and James L. McClelland. What learning systems do intelligent agents need? complementary learning systems theory updated. Trends in Cognitive Sciences, 20(7):512–534, July 2016. ISSN 1879-307X. doi: 10.1016/j.tics.2016.05.004.

Yuri Kuratov, Aydar Bulatov, Petr Anokhin, Ivan Rodkin, Dmitry Sorokin, Artyom Y. Sorokin, and Mikhail Burtsev. Babilong: Testing the limits of llms with long context reasoning-in-a-haystack. In Amir Globersons, Lester Mackey, Danielle Belgrave, Angela Fan, Ulrich Paquet, Jakub M. Tomczak, and Cheng Zhang, editors, Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, December 10 - 15, 2024, 2024. http://papers.nips.cc/paper\_files/paper/2024/ hash/c0d62e70dbc659cc9bd44cbcf1cb652f-Abstract-Datasets\_and\_Benchmarks\_Track.html.

Taeyoon Kwon, Dongwook Choi, Sunghwan Kim, Hyojun Kim, Seungjun Moon, Beong-woo Kwak, Kuan-Hao Huang, and Jinyoung Yeo. Embodied agents meet personalization: Exploring memory utilization for personalized assistance. CoRR, abs/2505.16348, 2025. doi: 10.48550/ARXIV.2505.16348. https://doi.org/10.48550/arXiv.2505.16348.

LangChain. GitHub - langchain-ai/langmem — github.com. https://github.com/langchain-ai/langmem, 2025. [Ac cessed 14-12-2025].

Chris Latimer, Nicoló Boschi, Andrew Neeser, Chris Bartholomew, Gaurav Srivastava, Xuan Wang, and Naren Ramakrishnan. Hindsight is 20/20: Building agent memory that retains, recalls, and reflects, 2025. https: //arxiv.org/abs/2512.12818.

Gibbeum Lee, Volker Hartmann, Jongho Park, Dimitris Papailiopoulos, and Kangwook Lee. Prompted llms as chatbot modules for long open-domain conversation. In Anna Rogers, Jordan L. Boyd-Graber, and Naoaki Okazaki, editors, Findings of the Association for Computational Linguistics: ACL 2023, Toronto, Canada, July 9-14, 2023, pages 4536–4554. Association for Computational Linguistics, 2023. doi: 10.18653/V1/2023.FINDINGS-ACL.277. https://doi.org/10.18653/v1/2023.findings-acl.277.

Kuang-Huei Lee, Xinyun Chen, Hiroki Furuta, John F. Canny, and Ian Fischer. A human-inspired reading agent with gist memory of very long contexts. In Forty-first International Conference on Machine Learning, 2024a.

Myeonghwa Lee, Seonho An, and Min-Soo Kim. Planrag: A plan-then-retrieval augmented generation for generative large language models as decision makers, 2024b. https://arxiv.org/abs/2406.12430.

Xiang Lei, Qin Li, and Min Zhang. D-smart: Enhancing llm dialogue consistency via dynamic structured memory and reasoning tree. arXiv preprint arXiv:2510.13363, 2025.

Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, and Douwe Kiela. Retrieval-augmented generation for knowledge-intensive NLP tasks. In Hugo Larochelle, Marc’Aurelio Ranzato, Raia Hadsell, Maria-Florina Balcan, and Hsuan-Tien Lin, editors, Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual, 2020. https: //proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html

Baiqi Li, Zhiqiu Lin, Deepak Pathak, Jiayao Li, Yixin Fei, Kewen Wu, Tifany Ling, Xide Xia, Pengchuan Zhang, Graham Neubig, and Deva Ramanan. Genai-bench: Evaluating and improving compositional text-to-visual generation, 2024a. https://arxiv.org/abs/2406.13743.

Caorui Li, Yu Chen, Yiyan Ji, Jin Xu, Zhenyu Cui, Shihao Li, Yuanxing Zhang, Jiafu Tang, Zhenghao Song, Dingling Zhang, Ying He, Haoxiang Liu, Yuxuan Wang, Qiufeng Wang, Zhenhe Wu, Jiehui Luo, Zhiyu Pan, Weihao Xie, Chenchen Zhang, Zhaohui Wang, Jiayi Tian, Yanghai Wang, Zhe Cao, Minxin Dai, Ke Wang, Runzhe Wen, Yinghao Ma, Yaning Pan, Sungkyun Chang, Termeh Taheri, Haiwen Xia, Christos Plachouras, Emmanouil Benetos, Yizhi Li, Ge Zhang, Jian Yang, Tianhao Peng, Zili Wang, Minghao Liu, Junran Peng, Zhaoxiang Zhang, and Jiaheng Liu. Omnivideobench: Towards audio-visual understanding evaluation for omni mllms, 2025a. https://arxiv.org/abs/2510.10689.

Cheng Li, Ziang Leng, Chenxi Yan, Junyi Shen, Hao Wang, Weishi Mi, Yaying Fei, Xiaoyang Feng, Song Yan, HaoSheng Wang, Linkang Zhan, Yaokai Jia, Pingyu Wu, and Haozhen Sun. Chatharuhi: Reviving anime character in reality via large language model. CoRR, abs/2308.09597, 2023a. doi: 10.48550/ARXIV.2308.09597. https: //doi.org/10.48550/arXiv.2308.09597.

Guohao Li, Hasan Abed Al Kader Hammoud, Hani Itani, Dmitrii Khizbullin, and Bernard Ghanem. CAMEL: Communicative agents for ”mind” exploration of large language model society. In Thirty-seventh Conference on Neural Information Processing Systems, 2023b.

Hao Li, Chenghao Yang, An Zhang, Yang Deng, Xiang Wang, and Tat-Seng Chua. Hello again! llm-powered personalized agent for long-term dialogue, 2025b. https://arxiv.org/abs/2406.05925.

Haoyang Li, Yiming Li, Anxin Tian, Tianhao Tang, Zhanchao Xu, Xuejia Chen, Nicole Hu, Wei Dong, Qing Li, and Lei Chen. A survey on large language model acceleration based on KV cache management. Trans. Mach. Learn. Res., 2025, 2025c. https://openreview.net/forum?id=z3JZzu9EA3.

Jiaang Li, Quan Wang, Zhongnan Wang, Yongdong Zhang, and Zhendong Mao. ELDER: enhancing lifelong model editing with mixture-of-lora. In Toby Walsh, Julie Shah, and Zico Kolter, editors, AAAI-25, Sponsored by the Association for the Advancement of Artificial Intelligence, February 25 - March 4, 2025, Philadelphia, PA, USA, pages 24440–24448. AAAI Press, 2025d. doi: 10.1609/AAAI.V39I23.34622. https://doi.org/10.1609/aaai.v39i23.34622.

Kuan Li, Zhongwang Zhang, Huifeng Yin, Liwen Zhang, Litu Ou, Jialong Wu, Wenbiao Yin, Baixuan Li, Zhengwei Tao, Xinyu Wang, Weizhou Shen, Junkai Zhang, Dingchu Zhang, Xixi Wu, Yong Jiang, Ming Yan, Pengjun Xie, Fei Huang, and Jingren Zhou. Websailor: Navigating super-human reasoning for web agent. CoRR, abs/2507.02592, 2025e. doi: 10.48550/ARXIV.2507.02592. https://doi.org/10.48550/arXiv.2507.02592.

Mo Li, L. H. Xu, Qitai Tan, Long Ma, Ting Cao, and Yunxin Liu. Sculptor: Empowering LLMs with Cognitive Agency via Active Context Management, September 2025f.

Rui Li, Zeyu Zhang, Xiaohe Bo, Zihang Tian, Xu Chen, Quanyu Dai, Zhenhua Dong, and Ruiming Tang. Cam: A constructivist view of agentic memory for llm-based reading comprehension, October 2025g.

Xiaoxi Li, Guanting Dong, Jiajie Jin, Yuyao Zhang, Yujia Zhou, Yutao Zhu, Peitian Zhang, and Zhicheng Dou. Search-o1: Agentic search-enhanced large reasoning models. CoRR, abs/2501.05366, 2025h. doi: 10.48550/ARXIV.2501.05366. https://doi.org/10.48550/arXiv.2501.05366.

Xiaoxi Li, Wenxiang Jiao, Jiarui Jin, Guanting Dong, Jiajie Jin, Yinuo Wang, Hao Wang, Yutao Zhu, Ji-Rong Wen, Yuan Lu, and Zhicheng Dou. DeepAgent: A General Reasoning Agent with Scalable Toolsets, October 2025i.

Xiaoxi Li, Jiajie Jin, Guanting Dong, Hongjin Qian, Yutao Zhu, Yongkang Wu, Ji-Rong Wen, and Zhicheng Dou. Webthinker: Empowering large reasoning models with deep research capability. CoRR, abs/2504.21776, 2025j. doi: 10.48550/ARXIV.2504.21776. https://doi.org/10.48550/arXiv.2504.21776.

Xiaoxi Li, Jiajie Jin, Yujia Zhou, Yuyao Zhang, Peitian Zhang, Yutao Zhu, and Zhicheng Dou. From matching to generation: A survey on generative information retrieval. ACM Trans. Inf. Syst., 43(3):83:1–83:62, 2025k. doi: 10.1145/3722552. https://doi.org/10.1145/3722552.

Yucheng Li, Bo Dong, Frank Guerin, and Chenghua Lin. Compressing context to enhance inference eficiency of large language models. In Houda Bouamor, Juan Pino, and Kalika Bali, editors, Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pages 6342–6353, Singapore, December 2023c. Association for Computational Linguistics. doi: 10.18653/v1/2023.emnlp-main.391.

Yuhong Li, Yingbing Huang, Bowen Yang, Bharat Venkitesh, Acyr Locatelli, Hanchen Ye, Tianle Cai, Patrick Lewis, and Deming Chen. Snapkv: LLM knows what you are looking for before generation. In Amir Globersons, Lester Mackey, Danielle Belgrave, Angela Fan, Ulrich Paquet, Jakub M. Tomczak, and Cheng Zhang, editors, Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, December 10 - 15, 2024, 2024b. http://papers.nips.cc/paper\_files/paper 2024/hash/28ab418242603e0f7323e54185d19bde-Abstract-Conference.html.

Yunxuan Li, Yibing Du, Jiageng Zhang, Le Hou, Peter Grabowski, Yeqing Li, and Eugene Ie. Improving multi-agent debate with sparse communication topology. In Yaser Al-Onaizan, Mohit Bansal, and Yun-Nung Chen, editors, Findings of the Association for Computational Linguistics: EMNLP 2024, Miami, Florida, USA, November 12-16, 2024, pages 7281–7294. Association for Computational Linguistics, 2024c. doi: 10.18653/V1/2024.FINDINGS-EMNLP.427. https://doi.org/10.18653/v1/2024.findings-emnlp.427.

Zaijing Li, Yuquan Xie, Rui Shao, Gongwei Chen, Dongmei Jiang, and Liqiang Nie. Optimus-1: Hybrid multimoda memory empowered agents excel in long-horizon tasks, 2024d. https://arxiv.org/abs/2408.03615.

Zhiyu Li, Shichao Song, Hanyu Wang, Simin Niu, Ding Chen, Jiawei Yang, Chenyang Xi, Huayi Lai, Jihao Zhao, Yezhaohui Wang, Junpeng Ren, Zehao Lin, Jiahao Huo, Tianyi Chen, Kai Chen, Kehang Li, Zhiqiang Yin, Qingchen Yu, Bo Tang, Hongkang Yang, Zhi-Qin John Xu, and Feiyu Xiong. Memos: An operating system for memory-augmented generation (mag) in large language models, 2025l. https://arxiv.org/abs/2505.22101.

Zijian Li, Xin Guan, Bo Zhang, Shen Huang, Houquan Zhou, Shaopeng Lai, Ming Yan, Yong Jiang, Pengjun Xie, Fei Huang, Jun Zhang, and Jingren Zhou. Webweaver: Structuring web-scale evidence with dynamic outlines fo open-ended deep research, October 2025m.

Xuechen Liang, Meiling Tao, Yinghui Xia, Jianhui Wang, Kun Li, Yijin Wang, Yangfan He, Jingsong Yang, Tianyu Shi, Yuantao Wang, Miao Zhang, and Xueqian Wang. SAGE: self-evolving agents with reflective and memory-augmented abilities. Neurocomputing, 647:130470, 2025. doi: 10.1016/J.NEUCOM.2025.130470. https://doi.org/10.1016/j. neucom.2025.130470.

Huanxuan Liao, Wen Hu, Yao Xu, Shizhu He, Jun Zhao, and Kang Liu. Beyond Hard and Soft: Hybrid Context Compression for Balancing Local and Global Information Retention. CoRR, abs/2505.15774, 2025a. doi: 10.48550/ ARXIV.2505.15774.

Yue Liao, Pengfei Zhou, Siyuan Huang, Donglin Yang, Shengcong Chen, Yuxin Jiang, Yue Hu, Jingbin Cai, Si Liu, Jianlan Luo, et al. Genie envisioner: A unified world foundation platform for robotic manipulation. arXiv preprint arXiv:2508.05635, 2025b.

Opher Lieber, Barak Lenz, Hofit Bata, Gal Cohen, Jhonathan Osin, Itay Dalmedigos, Erez Safahi, Shaked Meirom, Yonatan Belinkov, Shai Shalev-Shwartz, Omri Abend, Raz Alon, Tomer Asida, Amir Bergman, Roman Glozman, Michael Gokhman, Avashalom Manevich, Nir Ratner, Noam Rozen, Erez Shwartz, Mor Zusman, and Yoav Shoham. Jamba: A hybrid transformer-mamba language model, 2024. https://arxiv.org/abs/2403.19887.

Thomas Limbacher and Robert Legenstein. H-mem: Harnessing synaptic plasticity with hebbian memory networks. In Advances in Neural Information Processing Systems, volume 33, pages 21627–21637. Curran Associates, Inc., 2020.

Jessy Lin, Luke Zettlemoyer, Gargi Ghosh, Wen-Tau Yih, Aram Markosyan, Vincent-Pierre Berges, and Barlas Oğuz. Continual learning via sparse memory finetuning, 2025a. https://arxiv.org/abs/2510.15103.

Kevin Lin, Charlie Snell, Yu Wang, Charles Packer, Sarah Wooders, Ion Stoica, and Joseph E. Gonzalez. Sleep-time Compute: Beyond Inference Scaling at Test-time, April 2025b.

Bang Liu, Xinfeng Li, Jiayi Zhang, Jinlin Wang, Tanjin He, Sirui Hong, Hongzhang Liu, Shaokun Zhang, Kaitao Song, Kunlun Zhu, et al. Advances and challenges in foundation agents: From brain-inspired intelligence to evolutionary, collaborative, and safe systems. arXiv preprint arXiv:2504.01990, 2025a.

Guangyi Liu, Pengxiang Zhao, Liang Liu, Zhiming Chen, Yuxiang Chai, Shuai Ren, Hao Wang, Shibo He, and Wenchao Meng. Learnact: Few-shot mobile GUI agent with a unified demonstration benchmark. CoRR, abs/2504.13805, 2025b. doi: 10.48550/ARXIV.2504.13805. https://doi.org/10.48550/arXiv.2504.13805.

Jiahao Liu, Shengkang Gu, Dongsheng Li, Guangping Zhang, Mingzhe Han, Hansu Gu, Peng Zhang, Tun Lu, Li Shang, and Ning Gu. Agentcf++: Memory-enhanced llm-based agents for popularity-aware cross-domain recommendations, 2025c. https://arxiv.org/abs/2502.13843

Jiale Liu, Yifan Zeng, Malte Højmark-Bertelsen, Marie Normann Gadeberg, Huazheng Wang, and Qingyun Wu. Memory-augmented agent training for business document understanding. CoRR, abs/2412.15274, 2024. doi: 10.48550/ARXIV.2412.15274. https://doi.org/10.48550/arXiv.2412.15274.

Jun Liu, Zhenglun Kong, Changdi Yang, Fan Yang, Tianqi Li, Peiyan Dong, Joannah Nanjekye, Hao Tang, Geng Yuan, Wei Niu, Wenbin Zhang, Pu Zhao, Xue Lin, Dong Huang, and Yanzhi Wang. Rcr-router: Eficient roleaware context routing for multi-agent LLM systems with structured memory. CoRR, abs/2508.04903, 2025d. doi: 10.48550/ARXIV.2508.04903. https://doi.org/10.48550/arXiv.2508.04903.

Junming Liu, Yifei Sun, Weihua Cheng, Haodong Lei, Yirong Chen, Licheng Wen, Xuemeng Yang, Daocheng Fu, Pinlong Cai, Nianchen Deng, Yi Yu, Shuyue Hu, Botian Shi, and Ding Wang. Memverse: Multimodal memory for lifelong learning agents, 2025e. https://arxiv.org/abs/2512.03627.

Kunhao Liu, Wenbo Hu, Jiale Xu, Ying Shan, and Shijian Lu. Rolling forcing: Autoregressive long video difusion in real time. arXiv preprint arXiv:2509.25161, 2025f.

Lei Liu, Xiaoyan Yang, Yue Shen, Binbin Hu, Zhiqiang Zhang, Jinjie Gu, and Guannan Zhang. Think-in-memory: Recalling and post-thinking enable llms with long-term memory. CoRR, abs/2311.08719, 2023a. doi: 10.48550/ ARXIV.2311.08719. https://doi.org/10.48550/arXiv.2311.08719.

Yanming Liu, Xinyue Peng, Jiannan Cao, Shi Bo, Yuwei Zhang, Xuhong Zhang, Sheng Cheng, Xun Wang, Jianwei Yin, and Tianyu Du. Tool-Planner: Task planning with clusters across multiple tools. In The Thirteenth International Conference on Learning Representations, 2025g.

Yixin Liu, Guibin Zhang, Kun Wang, Shiyuan Li, and Shirui Pan. Graph-augmented large language model agents: Current progress and future prospects. arXiv preprint arXiv:2507.21407, 2025h.

Zeting Liu, Zida Yang, Zeyu Zhang, and Hao Tang. Evovla: Self-evolving vision-language-action model, 2025i. https://arxiv.org/abs/2511.16166.

Zichang Liu, Aditya Desai, Fangshuo Liao, Weitao Wang, Victor Xie, Zhaozhuo Xu, Anastasios Kyrillidis, and Anshumali Shrivastava. Scissorhands: Exploiting the persistence of importance hypothesis for LLM KV cache compression at test time. In Alice Oh, Tristan Naumann, Amir Globerson, Kate Saenko, Moritz Hardt, and Sergey Levine, editors, Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023, 2023b. http: //papers.nips.cc/paper\_files/paper/2023/hash/a452a7c6c463e4ae8fbdc614c6e983e6-Abstract-Conference.html.

Lin Long, Yichen He, Wentao Ye, Yiyuan Pan, Yuan Lin, Hang Li, Junbo Zhao, and Wei Li. Seeing, listening, remembering, and reasoning: A multimodal agent with long-term memory. arXiv preprint arXiv:2508.09736, 2025.

Junfeng Lu and Yueyan Li. Dynamic afective memory management for personalized llm agents, 2025. https: //arxiv.org/abs/2510.27418.

Junru Lu, Siyu An, Mingbao Lin, Gabriele Pergola, Yulan He, Di Yin, Xing Sun, and Yunsheng Wu. MemoChat: Tuning LLMs to use memos for consistent long-range open-domain conversation. arXiv preprint arXiv:2308.08239, 2023.

Miao Lu, Weiwei Sun, Weihua Du, Zhan Ling, Xuesong Yao, Kang Liu, and Jiecao Chen. Scaling llm multi-turn rl with end-to-end summarization-based context management, 2025a. https://arxiv.org/abs/2510.06727.

Miao Lu, Weiwei Sun, Weihua Du, Zhan Ling, Xuesong Yao, Kang Liu, and Jiecao Chen. Scaling llm multi-turn rl with end-to-end summarization-based context management, October 2025b.

Pengqian Lu, Jie Lu, Anjin Liu, and Guangquan Zhang. Spad: Seven-source token probability attribution with syntactic aggregation for detecting hallucinations in rag. arXiv preprint arXiv:2512.07515, 2025c.

Elias Lumer, Anmol Gulati, Vamse Kumar Subbiah, Pradeep Honaganahalli Basavaraju, and James A Burke. Memtool: Optimizing short-term memory management for dynamic tool calling in llm agent multi-turn conversations. arXiv preprint arXiv:2507.21428, 2025.

Junyu Luo, Weizhi Zhang, Ye Yuan, Yusheng Zhao, Junwei Yang, Yiyang Gu, Bohan Wu, Binqi Chen, Ziyue Qiao, Qingqing Long, Rongcheng Tu, Xiao Luo, Wei Ju, Zhiping Xiao, Yifan Wang, Meng Xiao, Chenwu Liu, Jingyang Yuan, Shichang Zhang, Yiqiao Jin, Fan Zhang, Xian Wu, Hanqing Zhao, Dacheng Tao, Philip S. Yu, and Ming Zhang. Large language model agent: A survey on methodology, applications and challenges, 2025a. https://arxiv.org/abs/2503.21460.

Weiyao Luo, Suncong Zheng, Heming Xia, Weikang Wang, Yan Lei, Tianyu Liu, Shuang Chen, and Zhifang Sui. Taking a deep breath: Enhancing language modeling of large language models with sentinel tokens. In Yaser Al-Onaizan, Mohit Bansal, and Yun-Nung Chen, editors, Findings of the Association for Computational Linguistics: EMNLP 2024, Miami, Florida, USA, November 12-16, 2024, pages 4034–4040. Association for Computational Linguistics, 2024. doi: 10.18653/V1/2024.FINDINGS-EMNLP.233. https://doi.org/10.18653/v1/2024.findings-emnlp.233.

Yongdong Luo, Xiawu Zheng, Guilin Li, Shukang Yin, Haojia Lin, Chaoyou Fu, Jinfa Huang, Jiayi Ji, Fei Chao, Jiebo Luo, and Rongrong Ji. Video-rag: Visually-aligned retrieval-augmented long video comprehension, 2025b. https://arxiv.org/abs/2411.13093.

Huan Ma, Changqing Zhang, Yatao Bian, Lemao Liu, Zhirui Zhang, Peilin Zhao, Shu Zhang, Huazhu Fu, Qinghua Hu, and Bingzhe Wu. Fairness-guided few-shot prompting for large language models, 2023a. https://arxiv.org/abs/ 2303.13217.

Jun-Yu Ma, Zhen-Hua Ling, Ningyu Zhang, and Jia-Chen Gu. Neighboring perturbations of knowledge editing on large language models. In Forty-first International Conference on Machine Learning, ICML 2024, Vienna, Austria, July 21-27, 2024. OpenReview.net, 2024. https://openreview.net/forum?id=K9NTPRvVRI.

Xinbei Ma, Yeyun Gong, Pengcheng He, Hai Zhao, and Nan Duan. Query rewriting in retrieval-augmented large language models. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pages 5303–5315, 2023b.

Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegrefe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, et al. Self-Refine: Iterative refinement with self-feedback. Advances in Neural Information Processing Systems, pages 46534–46594, 2023.

Adyasha Maharana, Dong-Ho Lee, Sergey Tulyakov, Mohit Bansal, Francesco Barbieri, and Yuwei Fang. Evaluating very long-term conversational memory of LLM agents. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 13851–13870, Bangkok, Thailand, August 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.acl-long.747. https://aclanthology.org/2024. acl-long.747/.

Shengyu Mao, Xiaohan Wang, Mengru Wang, Yong Jiang, Pengjun Xie, Fei Huang, and Ningyu Zhang. Editing personality for large language models. In Derek F. Wong, Zhongyu Wei, and Muyun Yang, editors, Natural Language Processing and Chinese Computing - 13th National CCF Conference, NLPCC 2024, Hangzhou, China, November 1-3, 2024, Proceedings, Part II, volume 15360 of Lecture Notes in Computer Science, pages 241–254. Springer, 2024. doi: 10.1007/978-981-97-9434-8\_19. https://doi.org/10.1007/978-981-97-9434-8\_19.

Samuele Marro, Emanuele La Malfa, Jesse Wright, Guohao Li, Nigel Shadbolt, Michael Wooldridge, and Philip Torr. A scalable communication protocol for networks of large language models, 2024. https://arxiv.org/abs/2410.11905.

Andrea Matarazzo and Riccardo Torlone. A survey on large language models with some insights on their capabilities and limitations, 2025. https://arxiv.org/abs/2501.04040.

Marcelo G. Mattar and Nathaniel D. Daw. Prioritized memory access explains planning and hippocampal replay. Nature Neuroscience, 21(11):1609–1617, November 2018. ISSN 1546-1726. doi: 10.1038/s41593-018-0232-z.

James L. McClelland, Bruce L. McNaughton, and Randall C. O’Reilly. Why there are complementary learning systems in the hippocampus and neocortex: Insights from the successes and failures of connectionist models of learning and memory. Psychological Review, 102(3):419–457, July 1995. ISSN 0033-295X. doi: 10.1037/0033-295X.102.3.419.

Michael McCloskey and Neal J. Cohen. Catastrophic interference in connectionist networks: The sequential learning problem. volume 24 of Psychology of Learning and Motivation, pages 109–165. Academic Press, 1989. doi: https:// doi.org/10.1016/S0079-7421(08)60536-8. https://www.sciencedirect.com/science/article/pii/S0079742108605368.

Lingrui Mei, Jiayu Yao, Yuyao Ge, Yiwei Wang, Baolong Bi, Yujun Cai, Jiazhi Liu, Mingyu Li, Zhong-Zhi Li, Duzhen Zhang, Chenlin Zhou, Jiayi Mao, Tianze Xia, Jiafeng Guo, and Shenghua Liu. A Survey of Context Engineering for Large Language Models, July 2025.

Memary. GitHub - kingjulio8238/Memary: The Open Source Memory Layer For Autonomous Agents — github.com. https://github.com/kingjulio8238/Memary, 2025. [Accessed 14-12-2025].

Memobase. GitHub - memodb-io/memobase: User Profile-Based Long-Term Memory for AI Chatbot Applications. https://github.com/memodb-io/memobase, 2025. [Accessed 12-12-2025].

Kevin Meng, David Bau, Alex Andonian, and Yonatan Belinkov. Locating and editing factual associations in GPT. In Sanmi Koyejo, S. Mohamed, A. Agarwal, Danielle Belgrave, K. Cho, and A. Oh, editors, Advances in Neural Information Processing Systems 35: Annual Conference on Neural Information Processing Systems 2022, NeurIPS 2022, New Orleans, LA, USA, November 28 - December 9, 2022, 2022. http://papers.nips.cc/paper\_files/paper 2022/hash/6f1d43d5a82a37e89b0665b33bf3a182-Abstract-Conference.html.

Kevin Meng, Arnab Sen Sharma, Alex J. Andonian, Yonatan Belinkov, and David Bau. Mass-editing memory in a transformer. In The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023. OpenReview.net, 2023. https://openreview.net/forum?id=MkbcAHIYgyS.

Lina Mezghani, Sainbayar Sukhbaatar, Thibaut Lavril, Oleksandr Maksymets, Dhruv Batra, Piotr Bojanowski, and Karteek Alahari. Memory-augmented reinforcement learning for image-goal navigation. In IEEE/RSJ International

Conference on Intelligent Robots and Systems, IROS 2022, Kyoto, Japan, October 23-27, 2022, pages 3316–3323. IEEE, 2022. doi: 10.1109/IROS47612.2022.9981090. https://doi.org/10.1109/IROS47612.2022.9981090.

Grégoire Mialon, Clémentine Fourrier, Thomas Wolf, Yann LeCun, and Thomas Scialom. GAIA: a benchmark for general ai assistants. In The Twelfth International Conference on Learning Representations, 2023.

Shervin Minaee, Tomas Mikolov, Narjes Nikzad, Meysam Chenaghlu, Richard Socher, Xavier Amatriain, and Jianfeng Gao. Large language models: A survey, 2025. https://arxiv.org/abs/2402.06196.

MineContext. GitHub - volcengine/MineContext: MineContext is your proactive context-aware AI partner (Context-Engineering+ChatGPT Pulse) — github.com. https://github.com/volcengine/MineContext, 2025. [Accessed 14-12-2025].

Eric Mitchell, Charles Lin, Antoine Bosselut, Chelsea Finn, and Christopher D. Manning. Fast model editing at scale. In The Tenth International Conference on Learning Representations, ICLR 2022, Virtual Event, April 25-29, 2022. OpenReview.net, 2022. https://openreview.net/forum?id=0DcZxeWfOPt.

Atsuyuki Miyai, Zaiying Zhao, Kazuki Egashira, Atsuki Sato, Tatsumi Sunada, Shota Onohara, Hiromasa Yamanishi, Mashiro Toyooka, Kunato Nishina, Ryoma Maeda, et al. Webchorearena: Evaluating web browsing agents on realistic tedious web tasks. arXiv preprint arXiv:2506.01952, 2025.

Ali Modarressi, Ayyoob Imani, Mohsen Fayyaz, and Hinrich Schütze. RET-LLM: Towards a general read-write memory for large language models. arXiv preprint arXiv:2305.14322, 2023.

Sajad Mousavi, Ricardo Luna Gutiérrez, Desik Rengarajan, Vineet Gundecha, Ashwin Ramesh Babu, Avisek Naug, Antonio Guillen, and Soumyendu Sarkar. N-critics: Self-refinement of large language models with ensemble of critics, 2023. https://arxiv.org/abs/2310.18679.

Jesse Mu, Xiang Li, and Noah D. Goodman. Learning to compress prompts with gist tokens. In Alice Oh, Tristan Naumann, Amir Globerson, Kate Saenko, Moritz Hardt, and Sergey Levine, editors, Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023, 2023. http://papers.nips.cc/paper\_files/paper/2023/hash 3 77 6 7f143 21 4 7f4 22 68 A C f .

Subhabrata Mukherjee, Arindam Mitra, Ganesh Jawahar, Sahaj Agarwal, Hamid Palangi, and Ahmed Awadallah. Orca: Progressive learning from complex explanation traces of gpt-4, 2023. https://arxiv.org/abs/2306.02707.

Hyungho Na, Yunkyeong Seo, and Il-Chul Moon. Eficient episodic memory utilization of cooperative multi-agen reinforcement learning. In The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenReview.net, 2024. https://openreview.net/forum?id=LjivA1SLZ6.

Jiayan Nan, Wenquan Ma, Wenlong Wu, and Yize Chen. Nemori: Self-organizing agent memory inspired by cognitive science. CoRR, abs/2508.03341, 2025. doi: 10.48550/ARXIV.2508.03341. https://doi.org/10.48550/arXiv.2508. 03341.

Thang Nguyen, Peter Chin, and Yu-Wing Tai. MA-RAG: multi-agent retrieval-augmented generation via collaborative chain-of-thought reasoning. CoRR, abs/2505.20096, 2025. doi: 10.48550/ARXIV.2505.20096. https://doi.org/10. 48550/arXiv.2505.20096.

Shen Nie, Fengqi Zhu, Zebin You, Xiaolu Zhang, Jingyang Ou, Jun Hu, Jun Zhou, Yankai Lin, Ji-Rong Wen, and Chongxuan Li. Large language difusion models, 2025. https://arxiv.org/abs/2502.09992.

Cheng Niu, Yuanhao Wu, Juno Zhu, Siliang Xu, Kashun Shum, Randy Zhong, Juntong Song, and Tong Zhang. Ragtruth: A hallucination corpus for developing trustworthy retrieval-augmented language models. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 10862–10878, 2024.

OpenAI. Memory and new controls for chatgpt, 2024. https://openai.com/index/ memory-and-new-controls-for-chatgpt/.

Siru Ouyang, Jun Yan, I-Hung Hsu, Yanfei Chen, Ke Jiang, Zifeng Wang, Rujun Han, Long T. Le, Samira Daruki, Xiangru Tang, Vishy Tirumalashetty, George Lee, Mahsan Rofouei, Hangfei Lin, Jiawei Han, Chen-Yu Lee, and Tomas Pfister. Reasoningbank: Scaling agent self-evolving with reasoning memory, 2025. https://arxiv.org/abs/2509.25140.

Charles Packer, Vivian Fang, Shishir G. Patil, Kevin Lin, Sarah Wooders, and Joseph E. Gonzalez. MemGPT: Towards LLMs as Operating Systems. CoRR, abs/2310.08560, 2023a. doi: 10.48550/ARXIV.2310.08560.

Charles Packer, Vivian Fang, ShishirG Patil, Kevin Lin, Sarah Wooders, and JosephE Gonzalez. Memgpt: Towards llms as operating systems. arXiv preprint arXiv:2310.08560, 2023b.

Lawrence Page, Sergey Brin, Rajeev Motwani, and Terry Winograd. The pagerank citation ranking : Bringing order to the web. In The Web Conference, 1999. https://api.semanticscholar.org/CorpusID:1508503.

Yiyuan Pan, Yunzhe Xu, Zhe Liu, and Hesheng Wang. Planning from imagination: Episodic simulation and episodic memory for vision-and-language navigation, 2024. https://arxiv.org/abs/2412.01857.

Zhuoshi Pan, Qianhui Wu, Huiqiang Jiang, Xufang Luo, Hao Cheng, Dongsheng Li, Yuqing Yang, Chin-Yew Lin, H. Vicky Zhao, Lili Qiu, and Jianfeng Gao. Secom: On memory construction and retrieval for personalized conversational agents. In The Thirteenth International Conference on Learning Representations, ICLR 2025, Singapore, April 24-28, 2025. OpenReview.net, 2025. https://openreview.net/forum?id=xKDZAW0He3.

Joon Sung Park, Joseph O’Brien, Carrie Jun Cai, Meredith Ringel Morris, Percy Liang, and Michael S Bernstein. Generative agents: Interactive simulacra of human behavior. In Proceedings of the 36th annual acm symposium on user interface software and technology, pages 1–22, 2023.

Sangjun Park and JinYeong Bak. Memoria: Resolving fateful forgetting problem through human-inspired memory architecture. In Forty-first International Conference on Machine Learning, ICML 2024, Vienna, Austria, July 21-27, 2024. OpenReview.net, 2024. https://openreview.net/forum?id=yTz0u4B8ug.

Shishir G. Patil, Tianjun Zhang, Xin Wang, and Joseph E. Gonzalez. Gorilla: Large Language Model Connected with Massive APIs. In Amir Globersons, Lester Mackey, Danielle Belgrave, Angela Fan, Ulrich Paquet, Jakub M. Tomczak, and Cheng Zhang, editors, Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, December 10 - 15, 2024, 2024. http: //papers.nips.cc/paper\_files/paper/2024/hash/e4c61f578f07830f5c37378dd3ecb0d-Abstract-Conference.html

Bo Peng, Eric Alcaide, Quentin Anthony, Alon Albalak, Samuel Arcadinho, Stella Biderman, Huanqi Cao, Xin Cheng, Michael Chung, Matteo Grella, Kranthi Kiran GV, Xuzheng He, Haowen Hou, Jiaju Lin, Przemyslaw Kazienko, Jan Kocon, Jiaming Kong, Bartlomiej Koptyra, Hayden Lau, Krishna Sri Ipsit Mantri, Ferdinand Mom, Atsushi Saito, Guangyu Song, Xiangru Tang, Bolun Wang, Johan S. Wind, Stanislaw Wozniak, Ruichong Zhang, Zhenyuan Zhang, Qihang Zhao, Peng Zhou, Qinghua Zhou, Jian Zhu, and Rui-Jie Zhu. Rwkv: Reinventing rnns for the transforme era, 2023. https://arxiv.org/abs/2305.13048.

Boci Peng, Yun Zhu, Yongchao Liu, Xiaohe Bo, Haizhou Shi, Chuntao Hong, Yan Zhang, and Siliang Tang. Graph retrieval-augmented generation: A survey, 2024. https://arxiv.org/abs/2408.08921.

Jayr Alencar Pereira, Robson do Nascimento Fidalgo, Roberto A. Lotufo, and Rodrigo Nogueira. Visconde: Multidocument QA with GPT-3 and neural reranking. In Jaap Kamps, Lorraine Goeuriot, Fabio Crestani, Maria Maistro, Hideo Joho, Brian Davis, Cathal Gurrin, Udo Kruschwitz, and Annalina Caputo, editors, Advances in Information Retrieval - 45th European Conference on Information Retrieval, ECIR 2023, Dublin, Ireland, April 2-6, 2023, Proceedings, Part II, volume 13981 of Lecture Notes in Computer Science, pages 534–543. Springer, 2023. doi: 10.1007/978-3-031-28238-6\_44. https://doi.org/10.1007/978-3-031-28238-6\_44.

Jinghua Piao, Yuwei Yan, Jun Zhang, Nian Li, Junbo Yan, Xiaochong Lan, Zhihong Lu, Zhiheng Zheng, Jing Yi Wang, Di Zhou, Chen Gao, Fengli Xu, Fang Zhang, Ke Rong, Jun Su, and Yong Li. Agentsociety: Large-scale simulation of llm-driven generative agents advances understanding of human behaviors and society, February 2025.

Ryan Po, Yotam Nitzan, Richard Zhang, Berlin Chen, Tri Dao, Eli Shechtman, Gordon Wetzstein, and Xun Huang. Long-context state-space video world models. arXiv preprint arXiv:2505.20171, 2025.

Hadi Pouransari, David Grangier, C Thomas, Michael Kirchhof, and Oncel Tuzel. Pretraining with hierarchical memories: separating long-tail and common knowledge, 2025. https://arxiv.org/abs/2510.02375.

Shrimai Prabhumoye, Rafal Kocielnik, Mohammad Shoeybi, Anima Anandkumar, and Bryan Catanzaro. Few-sho instruction prompts for pretrained language models to detect social biases, 2022. https://arxiv.org/abs/2112.07868.

Chen Qian, Wei Liu, Hongzhang Liu, Nuo Chen, Yufan Dang, Jiahao Li, Cheng Yang, Weize Chen, Yusheng Su, Xin Cong, Juyuan Xu, Dahai Li, Zhiyuan Liu, and Maosong Sun. ChatDev: Communicative agents for software development. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 15174–15186, 2024.

Cheng Qian, Chi Han, Yi Ren Fung, Yujia Qin, Zhiyuan Liu, and Heng Ji. CREATOR: Tool Creation for Disentangling Abstract and Concrete Reasoning of Large Language Models. In Houda Bouamor, Juan Pino, and Kalika Bali, editors, Findings of the Association for Computational Linguistics: EMNLP 2023, Singapore, December 6-10, 2023,

pages 6922–6939. Association for Computational Linguistics, 2023. doi: 10.18653/V1/2023.FINDINGS-EMNLP.462. https://doi.org/10.18653/v1/2023.findings-emnlp.462.

Hongjin Qian, Zheng Liu, Peitian Zhang, Kelong Mao, Defu Lian, Zhicheng Dou, and Tiejun Huang. Memorag: Boosting long context processing with global memory-enhanced retrieval augmentation. In Guodong Long, Michale Blumestein, Yi Chang, Liane Lewin-Eytan, Zi Helen Huang, and Elad Yom-Tov, editors, Proceedings of the ACM on Web Conference 2025, WWW 2025, Sydney, NSW, Australia, 28 April 2025- 2 May 2025, pages 2366–2377. ACM, 2025. doi: 10.1145/3696410.3714805. https://doi.org/10.1145/3696410.3714805.

Tianrui Qin, Qianben Chen, Sinuo Wang, He Xing, King Zhu, He Zhu, Dingfeng Shi, Xinxin Liu, Ge Zhang, Jiaheng Liu, Yuchen Eleanor Jiang, Xitong Gao, and Wangchunshu Zhou. Flash-searcher: Fast and efective web agents via dag-based parallel execution, 2025. https://arxiv.org/abs/2509.25301.

Yujia Qin, Shihao Liang, Yining Ye, Kunlun Zhu, Lan Yan, Yaxi Lu, Yankai Lin, Xin Cong, Xiangru Tang, Bill Qian, Sihan Zhao, Lauren Hong, Runchu Tian, Ruobing Xie, Jie Zhou, Mark Gerstein, Dahai Li, Zhiyuan Liu, and Maosong Sun. ToolLLM: Facilitating large language models to master 16000+ real-world apis. In The Twelfth International Conference on Learning Representations, 2024a.

Zhen Qin, Weigao Sun, Dong Li, Xuyang Shen, Weixuan Sun, and Yiran Zhong. Various lengths, constant speed: Eficient language modeling with lightning attention. In Forty-first International Conference on Machine Learning, ICML 2024, Vienna, Austria, July 21-27, 2024. OpenReview.net, 2024b. https://openreview.net/forum?id= Lwm6TiUP4X.

Zhen Qin, Weigao Sun, Dong Li, Xuyang Shen, Weixuan Sun, and Yiran Zhong. Lightning attention-2: A free lunch for handling unlimited sequence lengths in large language models. CoRR, abs/2401.04658, 2024c. doi: 10.48550/ARXIV.2401.04658. https://doi.org/10.48550/arXiv.2401.04658.

Jiahao Qiu, Xinzhe Juan, Yimin Wang, Ling Yang, Xuan Qi, Tongcheng Zhang, Jiacheng Guo, Yifu Lu, Zixin Yao, Hongru Wang, Shilong Liu, Xun Jiang, Liu Leqi, and Mengdi Wang. Agentdistill: Training-free agent distillation with generalizable mcp boxes, 2025a. https://arxiv.org/abs/2506.14728.

Jiahao Qiu, Xuan Qi, Hongru Wang, Xinzhe Juan, Yimin Wang, Zelin Zhao, Jiayi Geng, Jiacheng Guo, Peihang Li, Jingzhe Shi, Shilong Liu, and Mengdi Wang. Alita-g: Self-evolving generative agent for agent generation, October 2025b.

Jiahao Qiu, Xuan Qi, Tongcheng Zhang, Xinzhe Juan, Jiacheng Guo, Yifu Lu, Yimin Wang, Zixin Yao, Qihan Ren, Xun Jiang, Xing Zhou, Dongrui Liu, Ling Yang, Yue Wu, Kaixuan Huang, Shilong Liu, Hongru Wang, and Mengdi Wang. Alita: Generalist agent enabling scalable agentic reasoning with minimal predefinition and maximal self-evolution, 2025c. https://arxiv.org/abs/2505.20286.

Changle Qu, Sunhao Dai, Xiaochi Wei, Hengyi Cai, Shuaiqiang Wang, Dawei Yin, Jun Xu, and Ji-Rong Wen. COLT: Towards Completeness-Oriented Tool Retrieval for Large Language Models. CoRR, abs/2405.16089, 2024. doi: 10.48550/ARXIV.2405.16089. https://doi.org/10.48550/arXiv.2405.16089. arXiv: 2405.16089.

Changle Qu, Sunhao Dai, Xiaochi Wei, Hengyi Cai, Shuaiqiang Wang, Dawei Yin, Jun Xu, and Ji-Rong Wen. From exploration to mastery: Enabling llms to master tools via self-driven interactions, February 2025a.

Changle Qu, Sunhao Dai, Xiaochi Wei, Hengyi Cai, Shuaiqiang Wang, Dawei Yin, Jun Xu, and Ji-rong Wen. Tool learning with large language models: a survey. Frontiers of Computer Science, 19(8), January 2025b. ISSN 2095-2236. doi: 10.1007/s11704-024-40678-2. http://dx.doi.org/10.1007/s11704-024-40678-2.

Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, Gretchen Krueger, and Ilya Sutskever. Learning transferable visual models from natural language supervision. In Marina Meila and Tong Zhang, editors, Proceedings of the 38th International Conference on Machine Learning, ICML 2021, 18-24 July 2021, Virtual Event, volume 139 of Proceedings of Machine Learning Research, pages 8748–8763. PMLR, 2021. http://proceedings.mlr.press/v139/radford21a.html.

Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D Manning, Stefano Ermon, and Chelsea Finn. Direct preference optimization: Your language model is secretly a reward model. In Thirty-seventh Conference on Neural Information Processing Systems, 2023.

Krishan Rana, Jesse Haviland, Sourav Garg, Jad Abou-Chakra, Ian D. Reid, and Niko Sünderhauf. SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning. In Jie Tan, Marc Toussaint, and Kourosh Darvish, editors, Conference on Robot Learning, CoRL 2023, 6-9 November 2023, Atlanta, GA, USA, volume 229 of Proceedings of Machine Learning Research, pages 23–72. PMLR, 2023.

Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais, Jack Ryan, and Daniel Chalef. Zep: A temporal knowledge graph architecture for agent memory. CoRR, abs/2501.13956, 2025. doi: 10.48550/ARXIV.2501.13956. https: //doi.org/10.48550/arXiv.2501.13956.

Paul J. Reber. The neural basis of implicit learning and memory: A review of neuropsychological and neuroimaging research. Neuropsychologia, 51(10):2026–2042, August 2013. ISSN 1873-3514. doi: 10.1016/j.neuropsychologia.2013. 06.019.

Nils Reimers and Iryna Gurevych. Sentence-bert: Sentence embeddings using siamese bert-networks. In Kentaro Inui, Jing Jiang, Vincent Ng, and Xiaojun Wan, editors, Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing, EMNLP-IJCNLP 2019, Hong Kong, China, November 3-7, 2019, pages 3980–3990. Association for Computational Linguistics, 2019. doi: 10.18653/V1/D19-1410. https://doi.org/10.18653/v1/D19-1410.

Alireza Rezazadeh, Zichao Li, Ange Lou, Yuying Zhao, Wei Wei, and Yujia Bao. Collaborative memory: Multi-user memory sharing in llm agents with dynamic access control. arXiv preprint arXiv:2505.18279, 2025a.

Alireza Rezazadeh, Zichao Li, Ange Lou, Yuying Zhao, Wei Wei, and Yujia Bao. Collaborative memory: Multi-user memory sharing in llm agents with dynamic access control, 2025b. https://arxiv.org/abs/2505.18279.

Alireza Rezazadeh, Zichao Li, Wei Wei, and Yujia Bao. From Isolated Conversations to Hierarchical Schemas: Dynamic Tree Memory Representation for LLMs. In The Thirteenth International Conference on Learning Representations, ICLR 2025, Singapore, April 24-28, 2025. OpenReview.net, 2025c.

Wim J. Riedel and Arjan Blokland. Declarative memory. Handbook of Experimental Pharmacology, 228:215–236, 2015. ISSN 0171-2004. doi: 10.1007/978-3-319-16522-6\_7.

Stephen E. Robertson and Hugo Zaragoza. The probabilistic relevance framework: BM25 and beyond. Found. Trends Inf. Retr., 3(4):333–389, 2009. doi: 10.1561/1500000019. https://doi.org/10.1561/1500000019.

Dongyu Ru, Lin Qiu, Xiangkun Hu, Tianhang Zhang, Peng Shi, Shuaichen Chang, Cheng Jiayang, Cunxiang Wang, Shichao Sun, Huanyu Li, et al. Ragchecker: A fine-grained framework for diagnosing retrieval-augmented generation. Advances in Neural Information Processing Systems, 37:21999–22027, 2024.

Jingqing Ruan, Yihong Chen, Bin Zhang, Zhiwei Xu, Tianpeng Bao, Guoqing Du, Shiwei Shi, Hangyu Mao, Ziyue Li, Xingyu Zeng, and Rui Zhao. Tptu: Large language model-based ai agents for task planning and tool usage, 2023. https://arxiv.org/abs/2308.03427.

Rana Salama, Jason Cai, Michelle Yuan, Anna Currey, Monica Sunkara, Yi Zhang, and Yassine Benajiba. Meminsight: Autonomous memory augmentation for llm agents, 2025. https://arxiv.org/abs/2503.21760.

Jitao Sang, Jinlin Xiao, Jiarun Han, Jilin Chen, Xiaoyi Chen, Shuyu Wei, Yongjie Sun, and Yuhang Wang. Beyond pipelines: A survey of the paradigm shift toward model-native agentic ai, 2025. https://arxiv.org/abs/2510.16720.

Samarth Sarin, Lovepreet Singh, Bhaskarjit Sarmah, and Dhagash Mehta. Memoria: A scalable agentic memory framework for personalized conversational ai, 2025. https://arxiv.org/abs/2512.12686.

Parth Sarthi, Salman Abdullah, Aditi Tuli, Shubh Khanna, Anna Goldie, and Christopher D. Manning. Raptor: Recursive abstractive processing for tree-organized retrieval. ArXiv, abs/2401.18059, 2024.

Daniel L. Schacter and Donna Rose Addis. Constructive memory: The ghosts of past and future. Nature, 445(7123): 27, January 2007. ISSN 1476-4687. doi: 10.1038/445027a.

Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Eric Hambro, Luke Zettlemoyer, Nicola Cancedda, and Thomas Scialom. ToolFormer: Language models can teach themselves to use tools. Advances in Neural Information Processing Systems, 36:68539–68551, 2023.

John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. arXiv preprint arXiv:1707.06347, 2017.

Carol A. Seger and Brian J. Spiering. A critical review of habit learning and the Basal Ganglia. Frontiers in Systems Neuroscience, 5:66, 2011. ISSN 1662-5137. doi: 10.3389/fnsys.2011.00066.

Jay Shah, Ganesh Bikshandi, Ying Zhang, Vijay Thakkar, Pradeep Ramani, and Tri Dao. Flashattention-3: Fast and accurate attention with asynchrony and low-precision. In Amir Globersons, Lester Mackey, Danielle Belgrave, Angela Fan, Ulrich Paquet, Jakub M. Tomczak, and Cheng Zhang, editors, Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information Processing Systems 2024, NeurIPS 2024,

Vancouver, BC, Canada, December 10 - 15, 2024, 2024. http://papers.nips.cc/paper\_files/paper/2024/hash/ 7ede97c3e082c6df10a8d6103a2eebd2-Abstract-Conference.html.

Yunfan Shao, Linyang Li, Junqi Dai, and Xipeng Qiu. Character-llm: A trainable agent for role-playing. In Houda Bouamor, Juan Pino, and Kalika Bali, editors, Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, EMNLP 2023, Singapore, December 6-10, 2023, pages 13153–13187. Association for Computational Linguistics, 2023. doi: 10.18653/V1/2023.EMNLP-MAIN.814. https://doi.org/10.18653/v1/2023. emnlp-main.814.

Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Yang Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. arXiv preprint arXiv:2402.03300, 2024.

Junxiao Shen, John J. Dudley, and Per Ola Kristensson. Encode-Store-Retrieve: Augmenting Human Memory through Language-Encoded Egocentric Perception. In Ulrich Eck, Misha Sra, Jeanine K. Stefanucci, Maki Sugimoto, Markus Tatzgern, and Ian Williams, editors, IEEE International Symposium on Mixed and Augmented Reality, ISMAR 2024, Bellevue, WA, USA, October 21-25, 2024, pages 923–931. IEEE, 2024. doi: 10.1109/ISMAR62088.2024.00108.

Hao Shi, Bin Xie, Yingfei Liu, Lin Sun, Fengrong Liu, Tiancai Wang, Erjin Zhou, Haoqiang Fan, Xiangyu Zhang, and Gao Huang. Memoryvla: Perceptual-cognitive memory in vision-language-action models for robotic manipulation. CoRR, abs/2508.19236, 2025a. doi: 10.48550/ARXIV.2508.19236. https://doi.org/10.48550/arXiv.2508.19236.

Yaorui Shi, Yuxin Chen, Siyuan Wang, Sihang Li, Hengxing Cai, Qi Gu, Xiang Wang, and An Zhang. Look back to reason forward: Revisitable memory for long-context llm agents, 2025b. https://arxiv.org/abs/2509.23040.

Zhengliang Shi, Yuhan Wang, Lingyong Yan, Pengjie Ren, Shuaiqiang Wang, Dawei Yin, and Zhaochun Ren. Retrieval models aren’t tool-savvy: Benchmarking tool retrieval for large language models, May 2025c.

Zitong Shi, Guancheng Wan, Wenke Huang, Guibin Zhang, Jiawei Shao, Mang Ye, and Carl Yang. Privacy-enhancing paradigms within federated multi-agent systems. arXiv preprint arXiv:2503.08175, 2025d.

Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflexion: Language agents with verbal reinforcement learning. Advances in Neural Information Processing Systems, 36:8634–8652, 2023a.

Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflexion: language agents with verbal reinforcement learning. In Alice Oh, Tristan Naumann, Amir Globerson, Kate Saenko, Moritz Hardt, and Sergey Levine, editors, Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023, 2023b. http:// papers.nips.cc/paper\_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html.

Mohit Shridhar, Xingdi Yuan, Marc-Alexandre Côté, Yonatan Bisk, Adam Trischler, and Matthew J. Hausknecht. Alfworld: Aligning text and embodied environments for interactive learning. In 9th International Conference on Learning Representations, 2021.

Aditi Singh, Abul Ehtesham, Saket Kumar, and Tala Talaei Khoei. Agentic retrieval-augmented generation: A survey on agentic rag, 2025. https://arxiv.org/abs/2501.09136.

Anton Sinitsin, Vsevolod Plokhotnyuk, Dmitry V. Pyrkin, Sergei Popov, and Artem Babenko. Editable neural networks. In 8th International Conference on Learning Representations, ICLR 2020, Addis Ababa, Ethiopia, April 26-30, 2020. OpenReview.net, 2020. https://openreview.net/forum?id=HJedXaEtvS.

Chan Hee Song, Brian M. Sadler, Jiaman Wu, Wei-Lun Chao, Clayton Washington, and Yu Su. LLM-Planner: Few-Shot Grounded Planning for Embodied Agents with Large Language Models. In IEEE/CVF International Conference on Computer Vision, ICCV 2023, Paris, France, October 1-6, 2023, pages 2986–2997. IEEE, 2023. doi: 10.1109/ICCV51070.2023.00280.

Enxin Song, Wenhao Chai, Guanhong Wang, Yucheng Zhang, Haoyang Zhou, Feiyang Wu, Haozhe Chi, Xun Guo, Tian Ye, Yanting Zhang, Yan Lu, Jenq-Neng Hwang, and Gaoang Wang. Moviechat: From dense token to sparse memory for long video understanding. In IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2024, Seattle, WA, USA, June 16-22, 2024, pages 18221–18232. IEEE, 2024. doi: 10.1109/CVPR52733.2024.01725. https://doi.org/10.1109/CVPR52733.2024.01725.

Huatong Song, Jinhao Jiang, Yingqian Min, Jie Chen, Zhipeng Chen, Wayne Xin Zhao, Lei Fang, and Ji-Rong Wen. R1-searcher: Incentivizing the search capability in llms via reinforcement learning. CoRR, abs/2503.05592, 2025a. doi: 10.48550/ARXIV.2503.05592. https://doi.org/10.48550/arXiv.2503.05592.

Xinshuai Song, Weixing Chen, Yang Liu, Weikai Chen, Guanbin Li, and Liang Lin. Towards longhorizon vision-language navigation: Platform, benchmark and method. In IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2025, Nashville, TN, USA, June 11-15, 2025, pages 12078–12088. Computer Vision Foundation / IEEE, 2025b. doi: 10.1109/CVPR52734.2025.01128. https://openaccess.thecvf.com/content/CVPR2025/html/Song\_Towards\_Long-Horizon\_Vision-Language\_ Navigation\_Platform\_Benchmark\_and\_Method\_CVPR\_2025\_paper.html.

KAREN SPARCK JONES. A STATISTICAL INTERPRETATION OF TERM SPECIFICITY AND ITS AP-PLICATION IN RETRIEVAL. Journal of Documentation, 28(1):11–21, January 1972. ISSN 0022-0418. doi: 10.1108/eb026526.

Larry R. Squire. Memory systems of the brain: A brief history and current perspective. Neurobiology of Learning and Memory, 82(3):171–177, November 2004. ISSN 1074-7427. doi: 10.1016/j.nlm.2004.06.005.

Liangcai Su, Zhen Zhang, Guangyu Li, Zhuo Chen, Chenxi Wang, Maojia Song, Xinyu Wang, Kuan Li, Jialong Wu, Xuanzhong Chen, Zile Qiao, Zhongwang Zhang, Huifeng Yin, Shihao Cai, Runnan Fang, Zhengwei Tao, Wenbiao Yin, Chenxiong Qian, Yong Jiang, Pengjun Xie, Fei Huang, and Jingren Zhou. Scaling agents via continual pre-training. CoRR, abs/2509.13310, 2025. doi: 10.48550/ARXIV.2509.13310. https://doi.org/10.48550/arXiv.2509.13310.

Haoran Sun and Shaoning Zeng. Hierarchical memory for high-eficiency long-term reasoning in llm agents. ArXiv, abs/2507.22925, 2025.

Jingwei Sun, Zhixu Du, and Yiran Chen. Knowledge graph tuning: Real-time large language model personalization based on human feedback, 2024. https://arxiv.org/abs/2405.19686.

Mingyang Sun, Feng Hong, and Weinan Zhang. Sophia: A persistent agent framework of artificial life, 2025a. https://arxiv.org/abs/2512.18202.

Weiwei Sun, Miao Lu, Zhan Ling, Kang Liu, Xuesong Yao, Yiming Yang, and Jiecao Chen. Scaling long-horizon LLM agent via context-folding. CoRR, abs/2510.11967, 2025b. doi: 10.48550/ARXIV.2510.11967. https://doi.org/10. 48550/arXiv.2510.11967.

Zeyi Sun, Ziyu Liu, Yuhang Zang, Yuhang Cao, Xiaoyi Dong, Tong Wu, Dahua Lin, and Jiaqi Wang. SEAgent: Self-evolving computer use agent with autonomous learning from experience. arXiv preprint arXiv:2508.04700, 2025c.

Zhongxiang Sun, Zihua Si, Xiaoxue Zang, Kai Zheng, Yang Song, Xiao Zhang, and Jun Xu. Largepig for hallucinationfree query generation: Your large language model is secretly a pointer generator. In Proceedings of the ACM on Web Conference 2025, WWW ’25, page 4766–4779, New York, NY, USA, 2025d. Association for Computing Machinery. ISBN 9798400712746. doi: 10.1145/3696410.3714800. https://doi.org/10.1145/3696410.3714800.

Zhongxiang Sun, Qipeng Wang, Weijie Yu, Xiaoxue Zang, Kai Zheng, Jun Xu, Xiao Zhang, Yang Song, and Han Li. Rearter: Retrieval-augmented reasoning with trustworthy process rewarding. In Proceedings of the 48th International ACM SIGIR Conference on Research and Development in Information Retrieval, pages 1251–1261, 2025e.

ZhongXiang Sun, Xiaoxue Zang, Kai Zheng, Jun Xu, Xiao Zhang, Weijie Yu, Yang Song, and Han Li. Redeep: Detecting hallucination in retrieval-augmented generation via mechanistic interpretability. In The Thirteenth International Conference on Learning Representations, 2025f.

Supermemory. Supermemory — Universal Memory API for AI apps — supermemory.ai. https://supermemory.ai/, 2025. [Accessed 14-12-2025].

David Silver Sutton, Richard S. Welcome to the Era of Experience, April 2025.

Mirac Suzgun, Mert Yuksekgonul, Federico Bianchi, Dan Jurafsky, and James Zou. Dynamic cheatsheet: Test-time learning with adaptive memory, 2025. https://arxiv.org/abs/2504.07952.

Jihoon Tack, Jaehyung Kim, Eric Mitchell, Jinwoo Shin, Yee Whye Teh, and Jonathan Richard Schwarz. Online adaptation of language models with a memory of amortized contexts. In Amir Globersons, Lester Mackey, Danielle Belgrave, Angela Fan, Ulrich Paquet, Jakub M. Tomczak, and Cheng Zhang, editors, Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, December 10 - 15, 2024, 2024. http://papers.nips.cc/paper\_files/paper/2024/ hash/eaf956b52bae51fbf387b8be4cc3ce18-Abstract-Conference.html.

Haoran Tan, Zeyu Zhang, Chen Ma, Xu Chen, Quanyu Dai, and Zhenhua Dong. MemBench: Towards more comprehensive evaluation on the memory of LLM-based agents. In Findings of the Association for Computational

Linguistics: ACL 2025, pages 19336–19352, Vienna, Austria, July 2025a. Association for Computational Linguistics. ISBN 979-8-89176-256-5. doi: 10.18653/v1/2025.findings-acl.989. https://aclanthology.org/2025.findings-acl.989/.

Xingyu Tan, Xiaoyang Wang, Xiwei Xu, Xin Yuan, Liming Zhu, and Wenjie Zhang. Memotime: Memory-augmented temporal knowledge graph enhanced large language model reasoning. arXiv preprint arXiv:2510.13614, 2025b.

Zhen Tan, Jun Yan, I-Hung Hsu, Rujun Han, Zifeng Wang, Long T. Le, Yiwen Song, Yanfei Chen, Hamid Palangi, George Lee, Anand Rajan Iyer, Tianlong Chen, Huan Liu, Chen-Yu Lee, and Tomas Pfister. In prospect and retrospect: Reflective memory management for long-term personalized dialogue agents. In Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and Mohammad Taher Pilehvar, editors, Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2025, Vienna, Austria, July 27 - August 1, 2025, pages 8416–8439. Association for Computational Linguistics, 2025c. https://aclanthology.org/2025.acl-long.413/.

Hanlin Tang, Yang Lin, Jing Lin, Qingsen Han, Danning Ke, Shikuan Hong, Yiwu Yao, and Gongyi Wang. Razorattention: Eficient KV cache compression through retrieval heads. In The Thirteenth International Conference on Learning Representations, ICLR 2025, Singapore, April 24-28, 2025. OpenReview.net, 2025a. https://openreview.net/forum?id=tkiZQlL04w.

Qiaoyu Tang, Hao Xiang, Le Yu, Bowen Yu, Yaojie Lu, Xianpei Han, Le Sun, WenJuan Zhang, Pengbo Wang, Shixuan Liu, Zhenru Zhang, Jianhong Tu, Hongyu Lin, and Junyang Lin. Beyond turn limits: Training deep search agents with dynamic context window, October 2025b.

Xiangru Tang, Tianyu Hu, Muyang Ye, Yanjun Shao, Xunjian Yin, Siru Ouyang, Wangchunshu Zhou, Pan Lu, Zhuosheng Zhang, Yilun Zhao, Arman Cohan, and Mark Gerstein. Chemagent: Self-updating library in large language models improves chemical reasoning, 2025c. https://arxiv.org/abs/2501.06590.

Xiangru Tang, Tianrui Qin, Tianhao Peng, Ziyang Zhou, Daniel Shao, Tingting Du, Xinming Wei, Peng Xia, Fang Wu, He Zhu, Ge Zhang, Jiaheng Liu, Xingyao Wang, Sirui Hong, Chenglin Wu, Hao Cheng, Chi Wang, and Wangchunshu Zhou. Agent kb: Leveraging cross-domain experience for agentic problem solving, 2025d. https://arxiv.org/abs/2507.06229.

Yimin Tang, Yurong Xu, Ning Yan, and Masood Mortazavi. Enhancing long context performance in llms through inner loop query mechanism, 2024. https://arxiv.org/abs/2410.12859.

Dmitrii Tarasov, Elizaveta Goncharova, and Kuznetsov Andrey. Sentence-anchored gist compression for long-context llms, 2025. https://arxiv.org/abs/2511.08128.

Yi Tay, Vinh Tran, Mostafa Dehghani, Jianmo Ni, Dara Bahri, Harsh Mehta, Zhen Qin, Kai Hui, Zhe Zhao, Jai Prakash Gupta, Tal Schuster, William W. Cohen, and Donald Metzler. Transformer memory as a diferentiable search index. In Sanmi Koyejo, S. Mohamed, A. Agarwal, Danielle Belgrave, K. Cho, and A. Oh, editors, Advances in Neural Information Processing Systems 35: Annual Conference on Neural Information Processing Systems 2022, NeurIPS 2022, New Orleans, LA, USA, November 28 - December 9, 2022, 2022. http://papers.nips.cc/paper\_files/paper/ 2022/hash/892840a6123b5ec99ebaab8be1530fba-Abstract-Conference.html.

Ao Tian, Yunfeng Lu, Xinxin Fan, Changhao Wang, Lanzhi Zhou, Yeyao Zhang, and Yanfang Liu. Rgmem: Renormalization group-based memory evolution for language agent user profile. CoRR, abs/2510.16392, 2025a. doi: 10.48550/ARXIV.2510.16392. https://doi.org/10.48550/arXiv.2510.16392.

Shulin Tian, Ziniu Zhang, Liangyu Chen, and Ziwei Liu. Mmina: Benchmarking multihop multimodal internet agents, 2025b. https://arxiv.org/abs/2404.09992.

Hieu Tran, Zonghai Yao, Nguyen Luong Tran, Zhichao Yang, Feiyun Ouyang, Shuo Han, Razieh Rahimi, and Hong Yu. PRIME: planning and retrieval-integrated memory for enhanced reasoning. CoRR, abs/2509.22315, 2025. doi: 10.48550/ARXIV.2509.22315. https://doi.org/10.48550/arXiv.2509.22315.

Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, and Ashish Sabharwal. Musique: Multihop questions via single-hop question composition, 2022. https://arxiv.org/abs/2108.00573.

Endel Tulving. Episodic and semantic memory. In Organization of Memory, pages xiii, 423–xiii, 423. Academic Press, Oxford, England, 1972.

Endel Tulving. Episodic memory: From mind to brain. Annual Review of Psychology, 53:1–25, 2002. ISSN 0066-4308. doi: 10.1146/annurev.psych.53.100901.135114.

Lewis Tunstall, Edward Beeching, Nathan Lambert, Nazneen Rajani, Kashif Rasul, Younes Belkada, Shengyi Huang, Leandro von Werra, Clémentine Fourrier, Nathan Habib, Nathan Sarrazin, Omar Sanseviero, Alexander M. Rush, and Thomas Wolf. Zephyr: Direct distillation of lm alignment, 2023. https://arxiv.org/abs/2310.16944.

Szymon Tworkowski, Konrad Staniszewski, Mikolaj Pacek, Yuhuai Wu, Henryk Michalewski, and Piotr Milos. Focused transformer: Contrastive training for context scaling. In Alice Oh, Tristan Naumann, Amir Globerson, Kate Saenko, Moritz Hardt, and Sergey Levine, editors, Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023, 2023. http://papers.nips.cc/paper\_files/paper/2023/hash/ 8511d06d5590f4bda24d42087802cc81-Abstract-Conference.html.

Luanbo Wan and Weizhi Ma. Storybench: A dynamic benchmark for evaluating long-term memory with multi turns. arXiv preprint arXiv:2506.13356, 2025.

Ziyu Wan, Yunxiang Li, Xiaoyu Wen, Yan Song, Hanjing Wang, Linyi Yang, Mark Schmidt, Jun Wang, Weinan Zhang, Shuyue Hu, and Ying Wen. Rema: Learning to meta-think for llms with multi-agent reinforcement learning, 2025. https://arxiv.org/abs/2503.09501.

Bing Wang, Xinnian Liang, Jian Yang, Hui Huang, Shuangzhi Wu, Peihao Wu, Lu Lu, Zejun Ma, and Zhoujun Li. Scm: Enhancing large language model with self-controlled memory framework, 2025a. https://arxiv.org/abs/2304.13343.

Bo Wang, Weiyi He, Shenglai Zeng, Zhen Xiang, Yue Xing, Jiliang Tang, and Pengfei He. Unveiling privacy risks in llm agent memory, 2025b. https://arxiv.org/abs/2502.13172.

Fei Wang, Xingchen Wan, Ruoxi Sun, Jiefeng Chen, and Sercan O Arik. Astute rag: Overcoming imperfect retrieval augmentation and knowledge conflicts for large language models. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 30553–30571, 2025c.

Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and Anima Anandkumar. Voyager: An open-ended embodied agent with large language models. Trans. Mach. Learn. Res., 2024, 2024a. https://openreview.net/forum?id=ehfRiF0R3a.

Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and Anima Anandkumar. Voyager: An Open-Ended Embodied Agent with Large Language Models. Trans. Mach. Learn. Res., 2024, 2024b. https://openreview.net/forum?id=ehfRiF0R3a.

Han Wang, Archiki Prasad, Elias Stengel-Eskin, and Mohit Bansal. Retrieval-augmented generation with conflicting evidence. arXiv preprint arXiv:2504.13079, 2025d.

Haochun Wang, Chi Liu, Nuwa Xi, Zewen Qiang, Sendong Zhao, Bing Qin, and Ting Liu. Huatuo: Tuning llama model with chinese medical knowledge, 2023a. https://arxiv.org/abs/2304.06975.

Hengyi Wang, Haizhou Shi, Shiwei Tan, Weiyi Qin, Wenyuan Wang, Tunyu Zhang, Akshay Nambi, Tanuja Ganu, and Hao Wang. Multimodal needle in a haystack: Benchmarking long-context capability of multimodal large language models. In Luis Chiruzzo, Alan Ritter, and Lu Wang, editors, Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers), pages 3221–3241, Albuquerque, New Mexico, April 2025e. Association for Computational Linguistics. ISBN 979-8-89176-189-6. doi: 10.18653/v1/2025.naacl-long.166. https://aclanthology.org/2025.naacl-long.166/.

Juyuan Wang, Rongchen Zhao, Wei Wei, Yufeng Wang, Mo Yu, Jie Zhou, Jin Xu, and Liyan Xu. Comorag: A cognitive-inspired memory-organized RAG for stateful long narrative reasoning. CoRR, abs/2508.10419, 2025f. doi: 10.48550/ARXIV.2508.10419. https://doi.org/10.48550/arXiv.2508.10419.

Mengru Wang, Ningyu Zhang, Ziwen Xu, Zekun Xi, Shumin Deng, Yunzhi Yao, Qishen Zhang, Linyi Yang, Jindong Wang, and Huajun Chen. Detoxifying large language models via knowledge editing. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar, editors, Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2024, Bangkok, Thailand, August 11-16, 2024, pages 3093–3118. Association for Computational Linguistics, 2024c. doi: 10.18653/V1/2024.ACL-LONG.171. https://doi.org/10.18653/v1/2024. acl-long.171.

Noah Wang, Zhongyuan Peng, Haoran Que, Jiaheng Liu, Wangchunshu Zhou, Yuhan Wu, Hongcheng Guo, Ruitong Gan, Zehao Ni, Jian Yang, Man Zhang, Zhaoxiang Zhang, Wanli Ouyang, Ke Xu, Wenhao Huang, Jie Fu, and Junran Peng. Rolellm: Benchmarking, eliciting, and enhancing role-playing abilities of large language models. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar, editors, Findings of the Association for Computational Linguistics, ACL 2024, Bangkok, Thailand and virtual meeting, August 11-16, 2024, pages 14743–14777. Association for Computational Linguistics, 2024d. doi: 10.18653/V1/2024.FINDINGS-ACL.878. https://doi.org/10.18653/v1/2024.findings-acl.878.

Peng Wang, Zexi Li, Ningyu Zhang, Ziwen Xu, Yunzhi Yao, Yong Jiang, Pengjun Xie, Fei Huang, and Huajun Chen. WISE: rethinking the knowledge memory for lifelong model editing of large language models. In Amir Globersons, Lester Mackey, Danielle Belgrave, Angela Fan, Ulrich Paquet, Jakub M. Tomczak, and Cheng Zhang, editors,

Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, December 10 - 15, 2024, 2024e. http://papers.nips.cc/ paper\_files/paper/2024/hash/60960ad78868fce5c165295fbd895060-Abstract-Conference.html.

Piaohong Wang, Motong Tian, Jiaxian Li, Yuan Liang, Yuqing Wang, Qianben Chen, Tiannan Wang, Zhicong Lu, Jiawei Ma, Yuchen Eleanor Jiang, and Wangchunshu Zhou. O-mem: Omni memory system for personalized, long horizon, self-evolving agents, 2025g. https://arxiv.org/abs/2511.13593.

Qingyue Wang, Yanhe Fu, Yanan Cao, Shuai Wang, Zhiliang Tian, and Liang Ding. Recursively summarizing enables long-term dialogue memory in large language models. Neurocomputing, 639:130193, 2025h.

Renxi Wang, Xudong Han, Lei Ji, Shu Wang, Timothy Baldwin, and Haonan Li. ToolGen: Unified tool retrieval and calling via generation. In The Thirteenth International Conference on Learning Representations, 2025i.

Ruize Wang, Duyu Tang, Nan Duan, Zhongyu Wei, Xuanjing Huang, Jianshu Ji, Guihong Cao, Daxin Jiang, and Ming Zhou. K-adapter: Infusing knowledge into pre-trained models with adapters. In Chengqing Zong, Fei Xia, Wenjie Li, and Roberto Navigli, editors, Findings of the Association for Computational Linguistics: ACL/IJCNLP 2021, Online Event, August 1-6, 2021, volume ACL/IJCNLP 2021 of Findings of ACL, pages 1405–1418. Association for Computational Linguistics, 2021. doi: 10.18653/V1/2021.FINDINGS-ACL.121. https: //doi.org/10.18653/v1/2021.findings-acl.121.

Ruoyao Wang, Peter Jansen, Marc-Alexandre Côté, and Prithviraj Ammanabrolu. Scienceworld: Is your agent smarter than a 5th grader?, 2022a. https://arxiv.org/abs/2203.07540.

Tiannan Wang, Meiling Tao, Ruoyu Fang, Huilin Wang, Shuai Wang, Yuchen Eleanor Jiang, and Wangchunshu Zhou. Ai persona: Towards life-long personalization of llms, 2024f. https://arxiv.org/abs/2412.13103.

Weizhi Wang, Li Dong, Hao Cheng, Xiaodong Liu, Xifeng Yan, Jianfeng Gao, and Furu Wei. Augmenting language models with long-term memory. In Alice Oh, Tristan Naumann, Amir Globerson, Kate Saenko, Moritz Hardt, and Sergey Levine, editors, Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023, 2023b. http: //papers.nips.cc/paper\_files/paper/2023/hash/ebd82705f44793b6f9ade5a669d0f0bf-Abstract-Conference.html.

Wenyi Wang, Piotr Piękos, Li Nanbo, Firas Laakom, Yimeng Chen, Mateusz Ostaszewski, Mingchen Zhuge, and Jürgen Schmidhuber. Huxley-godel machine: Human-level coding agent development by an approximation of the optimal self-improving machine, 2025j. https://arxiv.org/abs/2510.21614.

Xiaohan Wang, Yuhui Zhang, Orr Zohar, and Serena Yeung-Levy. VideoAgent: Long-Form Video Understanding with Large Language Model as Agent. In Ales Leonardis, Elisa Ricci, Stefan Roth, Olga Russakovsky, Torsten Sattler, and Gül Varol, editors, Computer Vision - ECCV 2024 - 18th European Conference, Milan, Italy, September 29-October 4, 2024, Proceedings, Part LXXX, volume 15138 of Lecture Notes in Computer Science, pages 58–76. Springer, 2024g. doi: 10.1007/978-3-031-72989-8\_4.

Xiaoqiang Wang, Suyuchen Wang, Yun Zhu, and Bang Liu. R<sup>3</sup>mem: Bridging memory retention and retrieval via reversible compression. In Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and Mohammad Taher Pilehvar, editors, Findings of the Association for Computational Linguistics, ACL 2025, Vienna, Austria, July 27 - August 1, 2025, pages 4541–4557. Association for Computational Linguistics, 2025k. https://aclanthology.org/2025.findings-acl. 235/.

Yancheng Wang, Ziyan Jiang, Zheng Chen, Fan Yang, Yingxue Zhou, Eunah Cho, Xing Fan, Yanbin Lu, Xiaojiang Huang, and Yingzhen Yang. RecMind: Large Language Model Powered Agent For Recommendation. In Kevin Duh, Helena Gómez-Adorno, and Steven Bethard, editors, Findings of the Association for Computational Linguistics: NAACL 2024, Mexico City, Mexico, June 16-21, 2024, pages 4351–4364. Association for Computational Linguistics, 2024h. doi: 10.18653/V1/2024.FINDINGS-NAACL.271. https://doi.org/10.18653/v1/2024.findings-naacl.271.

Yanlin Wang, Wanjun Zhong, Yanxian Huang, Ensheng Shi, Min Yang, Jiachi Chen, Hui Li, Yuchi Ma, Qianxiang Wang, and Zibin Zheng. Agents in software engineering: Survey, landscape, and vision, 2024i. https://arxiv.org/ abs/2409.09030.

Yingxu Wang, Siwei Liu, Jinyuan Fang, and Zaiqiao Meng. EvoAgentX: An automated framework for evolving agentic workflows. arXiv preprint arXiv:2507.03616, 2025l.

Yiping Wang, Qing Yang, Zhiyuan Zeng, Liliang Ren, Liyuan Liu, Baolin Peng, Hao Cheng, Xuehai He, Kuan Wang, Jianfeng Gao, Weizhu Chen, Shuohang Wang, Simon Shaolei Du, and Yelong Shen. Reinforcement learning for reasoning in large language models with one training example, 2025m. https://arxiv.org/abs/2504.20571.

Yu Wang and Xi Chen. MIRIX: Multi-agent memory system for llm-based agents. arXiv preprint arXiv:2507.07957, 2025.

Yu Wang, Xiusi Chen, Jingbo Shang, and Julian McAuley. Memoryllm: Towards self-updatable large language models. ArXiv, abs/2402.04624, 2024j. https://api.semanticscholar.org/CorpusID:267523037.

Yu Wang, Chi Han, Tongtong Wu, Xiaoxin He, Wangchunshu Zhou, Nafis Sadeq, Xiusi Chen, Zexue He, Wei Wang, Gholamreza Hafari, et al. Towards lifespan cognitive systems. arXiv preprint arXiv:2409.13265, 2024k.

Yu Wang, Dmitry Krotov, Yuanzhe Hu, Yifan Gao, Wangchunshu Zhou, Julian J. McAuley, Dan Gutfreund, Rogério Feris, and Zexue He. M+: extending memoryllm with scalable long-term memory. CoRR, abs/2502.00592, 2025n. doi: 10.48550/ARXIV.2502.00592. https://doi.org/10.48550/arXiv.2502.00592.

Yu Wang, Xinshuang Liu, Xiusi Chen, Sean O’Brien, Junda Wu, and Julian J. McAuley. Self-updatable large language models by integrating context into model parameters. In The Thirteenth International Conference on Learning Representations, ICLR 2025, Singapore, April 24-28, 2025. OpenReview.net, 2025o. https://openreview.net/forum? id=aCPFCDL9QY.

Yu Wang, Ryuichi Takanobu, Zhiqi Liang, Yuzhen Mao, Yuanzhe Hu, Julian J. McAuley, and Xiaojian Wu. Mem-α: Learning memory construction via reinforcement learning. CoRR, abs/2509.25911, 2025p. doi: 10.48550/ARXIV. 2509.25911. https://doi.org/10.48550/arXiv.2509.25911.

Yujing Wang, Yingyan Hou, Haonan Wang, Ziming Miao, Shibin Wu, Qi Chen, Yuqing Xia, Chengmin Chi, Guoshuai Zhao, Zheng Liu, Xing Xie, Hao Sun, Weiwei Deng, Qi Zhang, and Mao Yang. A neural corpus indexer for document retrieval. In Sanmi Koyejo, S. Mohamed, A. Agarwal, Danielle Belgrave, K. Cho, and A. Oh, editors, Advances in Neural Information Processing Systems 35: Annual Conference on Neural Information Processing Systems 2022, NeurIPS 2022, New Orleans, LA, USA, November 28 - December 9, 2022, 2022b. http://papers.nips.cc/paper\_ files/paper/2022/hash/a46156bd3579c3b268108ea6aca71d13-Abstract-Conference.html.

Zheng Wang, Zhongyang Li, Zeren Jiang, Dandan Tu, and Wei Shi. Crafting personalized agents through retrievalaugmented generation on editable memory graphs, 2024l. https://arxiv.org/abs/2409.19401.

Zihao Wang, Shaofei Cai, Anji Liu, Yonggang Jin, Jinbing Hou, Bowei Zhang, Haowei Lin, Zhaofeng He, Zilong Zheng, Yaodong Yang, Xiaojian Ma, and Yitao Liang. JARVIS-1: open-world multi-task agents with memoryaugmented multimodal language models. IEEE Trans. Pattern Anal. Mach. Intell., 47(3):1894–1907, 2025q. doi: 10.1109/TPAMI.2024.3511593. https://doi.org/10.1109/TPAMI.2024.3511593.

Zixuan Wang, Bo Yu, Junzhe Zhao, Wenhao Sun, Sai Hou, Shuai Liang, Xing Hu, Yinhe Han, and Yiming Gan. KARMA: Augmenting Embodied AI Agents with Long-and-Short Term Memory Systems. In IEEE International Conference on Robotics and Automation, ICRA 2025, Atlanta, GA, USA, May 19-23, 2025, pages 1–8. IEEE, 2025r. doi: 10.1109/ICRA55743.2025.11128047.

Zora Zhiruo Wang, Jiayuan Mao, Daniel Fried, and Graham Neubig. Agent workflow memory. In Forty-second International Conference on Machine Learning, 2024m.

Zora Zhiruo Wang, Apurva Gandhi, Graham Neubig, and Daniel Fried. Inducing programmatic skills for agentic tasks, 2025s. https://arxiv.org/abs/2504.06821.

Joel Ward. Memoriesdb: A temporal-semantic-relational database for long-term agent memory/modeling experience as a graph of temporal-semantic surfaces. arXiv preprint arXiv:2511.06179, 2025.

Christopher Watkins and Peter Dayan. Q-learning. Machine Learning, 8:279–292, 1992. https://api.semanticscholar. org/CorpusID:208910339.

Haoran Wei, Yaofeng Sun, and Yukun Li. Deepseek-ocr: Contexts optical compression. arXiv preprint arXiv:2510.18234, 2025a.

Jason Wei, Maarten Bosma, Vincent Y. Zhao, Kelvin Guu, Adams Wei Yu, Brian Lester, Nan Du, Andrew M. Dai, and Quoc V. Le. Finetuned language models are zero-shot learners, 2022. https://arxiv.org/abs/2109.01652.

Jason Wei, Zhiqing Sun, Spencer Papay, Scott McKinney, Jefrey Han, Isa Fulford, Hyung Won Chung, Alex Tachard Passos, William Fedus, and Amelia Glaese. BrowseComp: A simple yet challenging benchmark for browsing agents. arXiv preprint arXiv:2504.12516, 2025b.

Jiaqi Wei, Yuejin Yang, Xiang Zhang, Yuhan Chen, Xiang Zhuang, Zhangyang Gao, Dongzhan Zhou, Guangshua Wang, Zhiqiang Gao, Juntai Cao, Zijie Qiu, Ming Hu, Chenglong Ma, Shixiang Tang, Junjun He, Chunfeng Song, Xuming He, Qiang Zhang, Chenyu You, Shuangjia Zheng, Ning Ding, Wanli Ouyang, Nanqing Dong, Yu Cheng, Siqi

Sun, Lei Bai, and Bowen Zhou. From ai for science to agentic science: A survey on autonomous scientific discovery, 2025c. https://arxiv.org/abs/2508.14111.

Rubin Wei, Jiaqi Cao, Jiarui Wang, Jushi Kai, Qipeng Guo, Bowen Zhou, and Zhouhan Lin. MLP memory: Language modeling with retriever-pretrained external memory. CoRR, abs/2508.01832, 2025d. doi: 10.48550/ARXIV.2508. 01832. https://doi.org/10.48550/arXiv.2508.01832.

Tianxin Wei, Noveen Sachdeva, Benjamin Coleman, Zhankui He, Yuanchen Bei, Xuying Ning, Mengting Ai, Yunzhe Li, Jingrui He, Ed H Chi, et al. Evo-memory: Benchmarking llm agent test-time learning with self-evolving memory. arXiv preprint arXiv:2511.20857, 2025e.

Yixuan Weng, Minjun Zhu, Qiujie Xie, Qiyao Sun, Zhen Lin, Sifan Liu, and Yue Zhang. Deepscientist: Advancing frontier-pushing scientific findings progressively, 2025. https://arxiv.org/abs/2509.26603.

Rebecca Westhäußer, Wolfgang Minker, and Sebastian Zepf. Enabling personalized long-term interactions in llm-based agents through persistent memory and user profiles. CoRR, abs/2510.07925, 2025. doi: 10.48550/ARXIV.2510.07925. https://doi.org/10.48550/arXiv.2510.07925.

Martin Wistuba, Prabhu Teja Sivaprasad, Lukas Balles, and Giovanni Zappella. Continual learning with low rank adaptation. CoRR, abs/2311.17601, 2023. doi: 10.48550/ARXIV.2311.17601. https://doi.org/10.48550/arXiv.2311. 17601.

Cheng-Kuang Wu, Zhi Rui Tam, Chieh-Yen Lin, Yun-Nung Chen, and Hung-yi Lee. Streambench: Towards benchmarking continuous improvement of language agents. In Amir Globersons, Lester Mackey, Danielle Belgrave, Angela Fan, Ulrich Paquet, Jakub M. Tomczak, and Cheng Zhang, editors, Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, December 10 - 15, 2024, 2024a. http://papers.nips.cc/paper\_files/paper/2024/hash/ c189915371c4474fe9789be3728113fc-Abstract-Datasets\_and\_Benchmarks\_Track.html.

Di Wu, Hongwei Wang, Wenhao Yu, Yuwei Zhang, Kai-Wei Chang, and Dong Yu. Longmemeval: Benchmarking chat assistants on long-term interactive memory. In The Thirteenth International Conference on Learning Representations, ICLR 2025, Singapore, April 24-28, 2025. OpenReview.net, 2025a. https://openreview.net/forum?id=pZiyCaVuti.

Jef Wu, Long Ouyang, Daniel M Ziegler, Nisan Stiennon, Ryan Lowe, Jan Leike, and Paul Christiano. Recursively summarizing books with human feedback. arXiv preprint arXiv:2109.10862, 2021.

Jialong Wu, Baixuan Li, Runnan Fang, Wenbiao Yin, Liwen Zhang, Zhengwei Tao, Dingchu Zhang, Zekun Xi, Yong Jiang, Pengjun Xie, Fei Huang, and Jingren Zhou. Webdancer: Towards autonomous information seeking agency. CoRR, abs/2505.22648, 2025b. doi: 10.48550/ARXIV.2505.22648. https://doi.org/10.48550/arXiv.2505.22648.

Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun Zhang, Shaokun Zhang, Jiale Liu, et al. Autogen: Enabling next-gen llm applications via multi-agent conversations. In First Conference on Language Modeling, 2024b.

Rong Wu, Xiaoman Wang, Jianbiao Mei, Pinlong Cai, Daocheng Fu, Cheng Yang, Licheng Wen, Xuemeng Yang, Yufan Shen, Yuxin Wang, and Botian Shi. Evolver: Self-evolving llm agents through an experience-driven lifecycle, 2025c. https://arxiv.org/abs/2510.16079.

Wenyi Wu, Zixuan Song, Kun Zhou, Yifei Shao, Zhiting Hu, and Biwei Huang. Towards general continuous memory for vision-language models. ArXiv, abs/2505.17670, 2025d.

Wenyi Wu, Kun Zhou, Ruoxin Yuan, Vivian Yu, Stephen Wang, Zhiting Hu, and Biwei Huang. Auto-scaling continuous memory for GUI agent. CoRR, abs/2510.09038, 2025e. doi: 10.48550/ARXIV.2510.09038. https: //doi.org/10.48550/arXiv.2510.09038.

Xixi Wu, Kuan Li, Yida Zhao, Liwen Zhang, Litu Ou, Huifeng Yin, Zhongwang Zhang, Yong Jiang, Pengjun Xie, Fei Huang, Minhao Cheng, Shuai Wang, Hong Cheng, and Jingren Zhou. ReSum: Unlocking Long-Horizon Search Intelligence via Context Summarization. CoRR, abs/2509.13313, 2025f. doi: 10.48550/ARXIV.2509.13313.

Yaxiong Wu, Sheng Liang, Chen Zhang, Yichao Wang, Yongyue Zhang, Huifeng Guo, Ruiming Tang, and Yong Liu. From human memory to ai memory: A survey on memory mechanisms in the era of llms, 2025g. https: //arxiv.org/abs/2504.15965.

Yaxiong Wu, Yongyue Zhang, Sheng Liang, and Yong Liu. Sgmem: Sentence graph memory for long-term conversational agents. ArXiv, abs/2509.21212, 2025h.

Yiran Wu, Feiran Jia, Shaokun Zhang, Hangyu Li, Erkang Zhu, Yue Wang, Yin Tat Lee, Richard Peng, Qingyun Wu, and Chi Wang. Mathchat: Converse to tackle challenging math problems with llm agents, 2024c. https: //arxiv.org/abs/2306.01337.

Yisha Wu, Cen Zhao, Yuanpei Cao, Xiaoqing Xu, Yashar Mehdad, Mindy Ji, and Claire Na Cheng. Incremental summarization for customer support via progressive note-taking and agent feedback. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing: Industry Track, pages 2000–2015, 2025i.

Yuhuai Wu, Markus Norman Rabe, DeLesley Hutchins, and Christian Szegedy. Memorizing transformers. In The Tenth International Conference on Learning Representations, ICLR 2022, Virtual Event, April 25-29, 2022. OpenReview.net, 2022. https://openreview.net/forum?id=TrjbxzRcnf-.

Zijun Wu, Yongchang Hao, and Lili Mou. Tokmem: Tokenized procedural memory for large language models, 2025j. https://arxiv.org/abs/2510.00444.

Rui Xi and Xianghan Wang. Livia: An emotion-aware AR companion powered by modular AI agents and progressive memory compression. CoRR, abs/2509.05298, 2025. doi: 10.48550/ARXIV.2509.05298. https://doi.org/10.48550/ arXiv.2509.05298.

Yunjia Xi, Weiwen Liu, Jianghao Lin, Bo Chen, Ruiming Tang, Weinan Zhang, and Yong Yu. Memocrs: Memoryenhanced sequential conversational recommender systems with large language models. In Edoardo Serra and Francesca Spezzano, editors, Proceedings of the 33rd ACM International Conference on Information and Knowledge Management, CIKM 2024, Boise, ID, USA, October 21-25, 2024, pages 2585–2595. ACM, 2024a. doi: 10.1145 3627673.3679599. https://doi.org/10.1145/3627673.3679599.

Zhiheng Xi, Yiwen Ding, Wenxiang Chen, Boyang Hong, Honglin Guo, Junzhe Wang, Dingwen Yang, Chenyang Liao, Xin Guo, Wei He, Songyang Gao, Lu Chen, Rui Zheng, Yicheng Zou, Tao Gui, Qi Zhang, Xipeng Qiu, Xuanjing Huang, Zuxuan Wu, and Yu-Gang Jiang. Agentgym: Evolving large language model-based agents across diverse environments, 2024b. https://arxiv.org/abs/2406.04151.

Siyu Xia, Zekun Xu, Jiajun Chai, Wentian Fan, Yan Song, Xiaohan Wang, Guojun Yin, Wei Lin, Haifeng Zhang, and Jun Wang. From experience to strategy: Empowering llm agents with trainable graph memory. arXiv preprin arXiv:2511.07800, 2025.

Guangxuan Xiao, Yuandong Tian, Beidi Chen, Song Han, and Mike Lewis. Eficient streaming language models with attention sinks. In The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenReview.net, 2024. https://openreview.net/forum?id=NG7sS51zVF.

Yuan-An Xiao, Pengfei Gao, Chao Peng, and Yingfei Xiong. Improving the eficiency of llm agent systems through trajectory reduction, 2025a. https://arxiv.org/abs/2509.23586.

Yunzhong Xiao, Yangmin Li, Hewei Wang, Yunlong Tang, and Zora Zhiruo Wang. ToolMem: Enhancing Multimodal Agents with Learnable Tool Capability Memory. CoRR, abs/2510.06664, 2025b. doi: 10.48550/ARXIV.2510.06664. https://doi.org/10.48550/arXiv.2510.06664. arXiv: 2510.06664.

Zeqi Xiao, Yushi Lan, Yifan Zhou, Wenqi Ouyang, Shuai Yang, Yanhong Zeng, and Xingang Pan. Worldmem: Long-term consistent world simulation with memory. arXiv preprint arXiv:2504.12369, 2025c.

Junlin Xie, Zhihong Chen, Ruifei Zhang, Xiang Wan, and Guanbin Li. Large multimodal agents: A survey, 2024. https://arxiv.org/abs/2402.15116.

Haoran Xu, Jiacong Hu, Ke Zhang, Lei Yu, Yuxin Tang, Xinyuan Song, Yiqun Duan, Lynn Ai, and Bill Shi. Sedm: Scalable self-evolving distributed memory for agents, 2025a. https://arxiv.org/abs/2509.09498.

Mufan Xu, Gewen Liang, Kehai Chen, Wei Wang, Xun Zhou, Muyun Yang, Tiejun Zhao, and Min Zhang. Memoryaugmented query reconstruction for llm-based knowledge graph reasoning, 2025b. https://arxiv.org/abs/2503.05193.

Renjun Xu and Jingwen Peng. A comprehensive survey of deep research: Systems, methodologies, and applications, 2025. https://arxiv.org/abs/2506.12594.

Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, and Yongfeng Zhang. A-MEM: Agentic Memory for LLM Agents. CoRR, abs/2502.12110, 2025c. doi: 10.48550/ARXIV.2502.12110.

Yige Xu, Xu Guo, Zhiwei Zeng, and Chunyan Miao. Softcot: Soft chain-of-thought for eficient reasoning with llms. In Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and Mohammad Taher Pilehvar, editors, Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2025,

Vienna, Austria, July 27 - August 1, 2025, pages 23336–23351. Association for Computational Linguistics, 2025d. https://aclanthology.org/2025.acl-long.1137/.

B. Y. Yan, Chaofan Li, Hongjin Qian, Shuqi Lu, and Zheng Liu. General agentic memory via deep research, 2025a. https://arxiv.org/abs/2511.18423.

B. Y. Yan, Chaofan Li, Hongjin Qian, Shuqi Lu, and Zheng Liu. General agentic memory via deep research, November 2025b.

Ming Yan, Ruihao Li, Hao Zhang, Hao Wang, Zhilan Yang, and Ji Yan. Larp: Language-agent role play for open-world games, 2023. https://arxiv.org/abs/2312.17653.

Sikuan Yan, Xiufeng Yang, Zuchao Huang, Ercong Nie, Zifeng Ding, Zonggen Li, Xiaowen Ma, Hinrich Schütze, Volker Tresp, and Yunpu Ma. Memory-R1: Enhancing large language model agents to manage and utilize memories via reinforcement learning. arXiv preprint arXiv:2508.19828, 2025c.

Hongkang Yang, Zehao Lin, Wenjin Wang, Hao Wu, Zhiyu Li, Bo Tang, Wenqiang Wei, Jinbo Wang, Zeyun Tang, Shichao Song, Chenyang Xi, Yu Yu, Kai Chen, Feiyu Xiong, Linpeng Tang, and Weinan E. Memory<sup>3</sup>: Language modeling with explicit memory. CoRR, abs/2407.01178, 2024a. doi: 10.48550/ARXIV.2407.01178. https://doi.org/10.48550/arXiv.2407.01178.

Ling Yang, Zhaochen Yu, Tianjun Zhang, Shiyi Cao, Minkai Xu, Wentao Zhang, Joseph E. Gonzalez, and Bin Cui. Bufer of thoughts: Thought-augmented reasoning with large language models. In Amir Globersons, Lester Mackey, Danielle Belgrave, Angela Fan, Ulrich Paquet, Jakub M. Tomczak, and Cheng Zhang, editors, Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, December 10 - 15, 2024, 2024b. http://papers.nips.cc/paper\_files/paper/2024 hash/cde328b7bf6358f5ebb91fe9c539745e-Abstract-Conference.html.

Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W. Cohen, Ruslan Salakhutdinov, and Christopher D. Manning. Hotpotqa: A dataset for diverse, explainable multi-hop question answering, 2018. https://arxiv.org/abs/ 1809.09600.

Ziyi Yang, Zaibin Zhang, Zirui Zheng, Yuxian Jiang, Ziyue Gan, Zhiyu Wang, Zijian Ling, Jinsong Chen, Martz Ma, Bowen Dong, Prateek Gupta, Shuyue Hu, Zhenfei Yin, Guohao Li, Xu Jia, Lijun Wang, Bernard Ghanem, Huchuan Lu, Chaochao Lu, Wanli Ouyang, Yu Qiao, Philip Torr, and Jing Shao. Oasis: Open agent social interaction simulations with one million agents, 2025. https://arxiv.org/abs/2411.11581.

Shunyu Yao, Howard Chen, John Yang, and Karthik Narasimhan. Webshop: Towards scalable real-world web interaction with grounded language agents, 2023a. https://arxiv.org/abs/2207.01206.

Shunyu Yao, Jefrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R Narasimhan, and Yuan Cao. ReAct: Synergizing reasoning and acting in language models. In The Eleventh International Conference on Learning Representations, 2023b.

Weiran Yao, Shelby Heinecke, Juan Carlos Niebles, Zhiwei Liu, Yihao Feng, Le Xue, Rithesh R. N., Zeyuan Chen, Jianguo Zhang, Devansh Arpit, Ran Xu, Phil Mui, Huan Wang, Caiming Xiong, and Silvio Savarese. Retroformer: Retrospective large language agents with policy gradient optimization. In The Twelfth International Conference on Learning Representations, 2024a.

Yao Yao, Zuchao Li, and Hai Zhao. Sirllm: Streaming infinite retentive LLM. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar, editors, Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2024, Bangkok, Thailand, August 11-16, 2024, pages 2611–2624. Association for Computational Linguistics, 2024b. doi: 10.18653/V1/2024.ACL-LONG.143. https://doi.org/10.18653/v1/2024.acl-long.143.

Rui Ye, Zhongwang Zhang, Kuan Li, Huifeng Yin, Zhengwei Tao, Yida Zhao, Liangcai Su, Liwen Zhang, Zile Qiao, Xinyu Wang, et al. Agentfold: Long-horizon web agents with proactive context management. arXiv preprint arXiv:2510.24699, 2025a.

Shicheng Ye, Chao Yu, Kaiqiang Ke, Chengdong Xu, and Yinqi Wei. H<sup>2</sup>r: Hierarchical hindsight reflection for multi-task LLM agents. CoRR, abs/2509.12810, 2025b. doi: 10.48550/ARXIV.2509.12810. https://doi.org/10. 48550/arXiv.2509.12810.

Ryan Yen and Jian Zhao. Memolet: Reifying the Reuse of User-AI Conversational Memories. In Proceedings of the 37th Annual ACM Symposium on User Interface Software and Technology, UIST ’24, pages 1–22, New York, NY, USA, October 2024. Association for Computing Machinery. ISBN 979-8-4007-0628-8. doi: 10.1145/3654777.3676388.

Woongyeong Yeo, Kangsan Kim, Jaehong Yoon, and Sung Ju Hwang. Worldmm: Dynamic multimodal memory agent for long video reasoning, 2025. https://arxiv.org/abs/2512.02425.

Xunjian Yin, Xinyi Wang, Liangming Pan, Li Lin, Xiaojun Wan, and William Yang Wang. Gödel agent: A selfreferential agent framework for recursively self-improvement. In Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and Mohammad Taher Pilehvar, editors, Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2025, Vienna, Austria, July 27 - August 1, 2025, pages 27890–27913. Association for Computational Linguistics, 2025. https://aclanthology.org/2025.acl-long.1354/.

Chanwoong Yoon, Taewhoo Lee, Hyeon Hwang, Minbyul Jeong, and Jaewoo Kang. CompAct: Compressing Retrieved Documents Actively for Question Answering. In Yaser Al-Onaizan, Mohit Bansal, and Yun-Nung Chen, editors, Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, EMNLP 2024, Miami, FL, USA, November 12-16, 2024, pages 21424–21439. Association for Computational Linguistics, 2024. doi: 10.18653/V1/2024.EMNLP-MAIN.1194.

Zeng You, Zhiquan Wen, Yaofo Chen, Xin Li, Runhao Zeng, Yaowei Wang, and Mingkui Tan. Towards long video understanding via fine-detailed video story generation. IEEE Transactions on Circuits and Systems for Video Technology, 2024.

Hongli Yu, Tinghong Chen, Jiangtao Feng, Jiangjie Chen, Weinan Dai, Qiying Yu, Ya-Qin Zhang, Wei-Ying Ma, Jingjing Liu, Mingxuan Wang, et al. Memagent: Reshaping long-context llm with multi-conv rl-based memory agent. arXiv preprint arXiv:2507.02259, 2025a.

Jiwen Yu, Jianhong Bai, Yiran Qin, Quande Liu, Xintao Wang, Pengfei Wan, Di Zhang, and Xihui Liu. Context as memory: Scene-consistent interactive long video generation with memory retrieval. CoRR, abs/2506.03141, 2025b. doi: 10.48550/ARXIV.2506.03141. https://doi.org/10.48550/arXiv.2506.03141.

Jiwen Yu, Jianhong Bai, Yiran Qin, Quande Liu, Xintao Wang, Pengfei Wan, Di Zhang, and Xihui Liu. Context as memory: Scene-consistent interactive long video generation with memory retrieval. arXiv preprint arXiv:2506.03141, 2025c.

Tao Yu, Zhengbo Zhang, Zhiheng Lyu, Junhao Gong, Hongzhu Yi, Xinming Wang, Yuxuan Zhou, Jiabing Yang, Ping Nie, Yan Huang, and Wenhu Chen. BrowserAgent: Building Web Agents with Human-Inspired Web Browsing Actions, October 2025d. http://arxiv.org/abs/2510.10666. arXiv:2510.10666 [cs].

Xinlei Yu, Chengming Xu, Guibin Zhang, Zhangquan Chen, Yudong Zhang, Yongbo He, Peng-Tao Jiang, Jiangning Zhang, Xiaobin Hu, and Shuicheng Yan. Vismem: Latent vision memory unlocks potential of vision-language models. arXiv preprint arXiv:2511.11007, 2025e.

Yangyang Yu, Zhiyuan Yao, Haohang Li, Zhiyang Deng, Yuechen Jiang, Yupeng Cao, Zhi Chen, Jordan Suchow, Zhenyu Cui, Rong Liu, et al. Fincon: A synthesized llm multi-agent system with conceptual verbal reinforcement for enhanced financial decision making. Advances in Neural Information Processing Systems, 37:137010–137045, 2024.

Yi Yu, Liuyi Yao, Yuexiang Xie, Qingquan Tan, Jiaqi Feng, Yaliang Li, and Libing Wu. Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents, January 2026.

Yifei Yu, Xiaoshan Wu, Xinting Hu, Tao Hu, Yangtian Sun, Xiaoyang Lyu, Bo Wang, Lin Ma, Yuewen Ma, Zhongrui Wang, et al. Videossm: Autoregressive long video generation with hybrid state-space memory. arXiv preprint arXiv:2512.04519, 2025f.

Lifan Yuan, Yangyi Chen, Xingyao Wang, Yi Fung, Hao Peng, and Heng Ji. CRAFT: Customizing LLMs by Creating and Retrieving from Specialized Toolsets. In The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenReview.net, 2024a. https://openreview.net/forum?id=G0vdDSt9XM.

Peiwen Yuan, Xinglin Wang, Shaoxiong Feng, Boyuan Pan, Yiwei Li, Heda Wang, Xupeng Miao, and Kan Li. Generative dense retrieval: Memory can be a burden. In Yvette Graham and Matthew Purver, editors, Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics, EACL 2024 - Volume 1: Long Papers, St. Julian’s, Malta, March 17-22, 2024, pages 2835–2845. Association for Computational Linguistics, 2024b. https://aclanthology.org/2024.eacl-long.173.

Qianhao Yuan, Jie Lou, Zichao Li, Jiawei Chen, Yaojie Lu, Hongyu Lin, Le Sun, Debing Zhang, and Xianpei Han. MemSearcher: Training LLMs to Reason, Search and Manage Memory via End-to-End Reinforcement Learning, November 2025a.

Ruifeng Yuan, Shichao Sun, Yongqi Li, Zili Wang, Ziqiang Cao, and Wenjie Li. Personalized large language model assistant with evolving conditional memory. In Owen Rambow, Leo Wanner, Marianna Apidianaki, Hend Al-

Khalifa, Barbara Di Eugenio, and Steven Schockaert, editors, Proceedings of the 31st International Conference on Computational Linguistics, COLING 2025, Abu Dhabi, UAE, January 19-24, 2025, pages 3764–3777. Association for Computational Linguistics, 2025b. https://aclanthology.org/2025.coling-main.254/.

Weizhe Yuan, Richard Yuanzhe Pang, Kyunghyun Cho, Xian Li, Sainbayar Sukhbaatar, Jing Xu, and Jason Weston. Self-rewarding language models. In Forty-first International Conference on Machine Learning, ICML 2024, Vienna, Austria, July 21-27, 2024. OpenReview.net, 2024c. https://openreview.net/forum?id=0NphYCmgua.

Sizhe Yuen, Francisco Gomez Medina, Ting Su, Yali Du, and Adam J. Sobey. Intrinsic memory agents: Heterogeneous multi-agent llm systems through structured contextual memory, 2025. https://arxiv.org/abs/2508.08997.

Manzil Zaheer, Guru Guruganesh, Kumar Avinava Dubey, Joshua Ainslie, Chris Alberti, Santiago Ontañón, Philip Pham, Anirudh Ravula, Qifan Wang, Li Yang, and Amr Ahmed. Big bird: Transformers for longer sequences. In Hugo Larochelle, Marc’Aurelio Ranzato, Raia Hadsell, Maria-Florina Balcan, and Hsuan-Tien Lin, editors, Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual, 2020. https://proceedings.neurips.cc/paper/2020 hash/c8512d142a2d849725f31a9a7a361ab9-Abstract.html.

Eric Zelikman, Yuhuai Wu, Jesse Mu, and Noah Goodman. STaR: Bootstrapping reasoning with reasoning. In Advances in Neural Information Processing Systems, volume 35, pages 15476–15488, 2022.

Hansi Zeng, Chen Luo, Bowen Jin, Sheikh Muhammad Sarwar, Tianxin Wei, and Hamed Zamani. Scalable and efective generative information retrieval. In Tat-Seng Chua, Chong-Wah Ngo, Ravi Kumar, Hady W. Lauw, and Roy Ka-Wei Lee, editors, Proceedings of the ACM on Web Conference 2024, WWW 2024, Singapore, May 13-17, 2024, pages 1441–1452. ACM, 2024. doi: 10.1145/3589334.3645477. https://doi.org/10.1145/3589334.3645477.

Stefano Zeppieri. Mmag: Mixed memory-augmented generation for large language models applications, 2025. https: //arxiv.org/abs/2512.01710.

Yunpeng Zhai, Shuchang Tao, Cheng Chen, Anni Zou, Ziqian Chen, Qingxu Fu, Shinji Mai, Li Yu, Jiaji Deng, Zouying Cao, Zhaoyang Liu, Bolin Ding, and Jingren Zhou. Agentevolver: Towards eficient self-evolving agent system, 2025. https://arxiv.org/abs/2511.10395.

Chaoyun Zhang, He Huang, Chiming Ni, Jian Mu, Si Qin, Shilin He, Lu Wang, Fangkai Yang, Pu Zhao, Chao Du, Liqun Li, Yu Kang, Zhao Jiang, Suzhen Zheng, Rujia Wang, Jiaxu Qian, Minghua Ma, Jian-Guang Lou, Qingwei Lin, Saravan Rajmohan, and Dongmei Zhang. UFO2: the desktop agentos. CoRR, abs/2504.14603, 2025a. doi: 10.48550/ARXIV.2504.14603. https://doi.org/10.48550/arXiv.2504.14603

Gaoke Zhang, Bo Wang, Yunlong Ma, Dongming Zhao, and Zifei Yu. Multiple memory systems for enhancing the long-term memory of agent. CoRR, abs/2508.15294, 2025b. doi: 10.48550/ARXIV.2508.15294. https://doi.org/10. 48550/arXiv.2508.15294.

Gui-Min Zhang, Muxin Fu, Guancheng Wan, Miao Yu, Kun Wang, and Shuicheng Yan. G-memory: Tracing hierarchical memory for multi-agent systems. ArXiv, abs/2506.07398, 2025c.

Gui-Min Zhang, Muxin Fu, and Shuicheng Yan. Memgen: Weaving generative latent memory for self-evolving agents. ArXiv, abs/2509.24704, 2025d.

Guibin Zhang, Muxin Fu, Guancheng Wan, Miao Yu, Kun Wang, and Shuicheng Yan. G-Memory: Tracing hierarchical memory for multi-agent systems. arXiv preprint arXiv:2506.07398, 2025e.

Guibin Zhang, Hejia Geng, Xiaohang Yu, Zhenfei Yin, Zaibin Zhang, Zelin Tan, Heng Zhou, Zhongzhi Li, Xiangyuan Xue, Yijiang Li, Yifan Zhou, Yang Chen, Chen Zhang, Yutao Fan, Zihu Wang, Songtao Huang, Yue Liao, Hongru Wang, Mengyue Yang, Heng Ji, Michael Littman, Jun Wang, Shuicheng Yan, Philip Torr, and Lei Bai. The landscape of agentic reinforcement learning for llms: A survey, 2025f. https://arxiv.org/abs/2509.02547.

Guibin Zhang, Fanci Meng, Guancheng Wan, Zherui Li, Kun Wang, Zhenfei Yin, Lei Bai, and Shuicheng Yan. Latentevolve: Self-evolving test-time scaling in latent space, 2025g. https://arxiv.org/abs/2509.24771.

Guibin Zhang, Haotian Ren, Chong Zhan, Zhenhong Zhou, Junhao Wang, He Zhu, Wangchunshu Zhou, and Shuicheng Yan. Memevolve: Meta-evolution of agent memory systems, 2025h. https://arxiv.org/abs/2512.18746.

Jenny Zhang, Shengran Hu, Cong Lu, Robert T. Lange, and Jef Clune. Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents. CoRR, abs/2505.22954, 2025i. doi: 10.48550/ARXIV.2505.22954. https: //doi.org/10.48550/arXiv.2505.22954. arXiv: 2505.22954.

Jiarui Zhang. Guided profile generation improves personalization with llms. arXiv preprint arXiv:2409.13093, 2024.

Jiayi Zhang, Jinyu Xiang, Zhaoyang Yu, Fengwei Teng, Xiong-Hui Chen, Jiaqi Chen, Mingchen Zhuge, Xin Cheng, Sirui Hong, Jinlin Wang, Bingnan Zheng, Bang Liu, Yuyu Luo, and Chenglin Wu. AFlow: Automating agentic workflow generation. In The Thirteenth International Conference on Learning Representations, 2025j.

Kai Zhang, Xiangchao Chen, Bo Liu, Tianci Xue, Zeyi Liao, Zhihan Liu, Xiyao Wang, Yuting Ning, Zhaorun Chen, Xiaohan Fu, Jian Xie, Yuxuan Sun, Boyu Gou, Qi Qi, Zihang Meng, Jianwei Yang, Ning Zhang, Xian Li, Ashish Shah, Dat Huynh, Hengduo Li, Zi Yang, Sara Cao, Lawrence Jang, Shuyan Zhou, Jiacheng Zhu, Huan Sun, Jason Weston, Yu Su, and Yifan Wu. Agent learning via early experience, 2025k. https://arxiv.org/abs/2510.08558.

Kaiyan Zhang, Yuxin Zuo, Bingxiang He, Youbang Sun, Runze Liu, Che Jiang, Yuchen Fan, Kai Tian, Guoli Jia, Pengfei Li, Yu Fu, Xingtai Lv, Yuchen Zhang, Sihang Zeng, Shang Qu, Haozhan Li, Shijie Wang, Yuru Wang, Xinwei Long, Fangfu Liu, Xiang Xu, Jiaze Ma, Xuekai Zhu, Ermo Hua, Yihao Liu, Zonglin Li, Huayu Chen, Xiaoye Qu, Yafu Li, Weize Chen, Zhenzhao Yuan, Junqi Gao, Dong Li, Zhiyuan Ma, Ganqu Cui, Zhiyuan Liu, Biqing Qi, Ning Ding, and Bowen Zhou. A survey of reinforcement learning for large reasoning models, 2025l. https://arxiv.org/abs/2509.08827.

Lingfeng Zhang, Yuecheng Liu, Zhanguang Zhang, Matin Aghaei, Yaochen Hu, Hongjian Gu, Mohammad Ali Alomrani, David Gamaliel Arcos Bravo, Raika Karimi, Atia Hamidizadeh, Haoping Xu, Guowei Huang, Zhanpeng Zhang, Tongtong Cao, Weichao Qiu, Xingyue Quan, Jianye Hao, Yuzheng Zhuang, and Yingxue Zhang. Mem2ego: Empowering vision-language models with global-to-ego memory for long-horizon embodied navigation. CoRR abs/2502.14254, 2025m. doi: 10.48550/ARXIV.2502.14254. https://doi.org/10.48550/arXiv.2502.14254.

Qizheng Zhang, Changran Hu, Shubhangi Upasani, Boyuan Ma, Fenglu Hong, Vamsidhar Kamanuru, Jay Rainton, Chen Wu, Mengmeng Ji, Hanchen Li, Urmish Thakker, James Zou, and Kunle Olukotun. Agentic context engineering: Evolving contexts for self-improving language models. CoRR, abs/2510.04618, 2025n. doi: 10.48550/ARXIV.2510. 04618. https://doi.org/10.48550/arXiv.2510.04618.

Shaohua Zhang, Yuan Lin, and Hang Li. Memory retrieval and consolidation in large language models through function tokens, 2025o. https://arxiv.org/abs/2510.08203.

Shengtao Zhang, Jiaqian Wang, Ruiwen Zhou, Junwei Liao, Yuchen Feng, Weinan Zhang, Ying Wen, Zhiyu Li, Feiyu Xiong, Yutao Qi, Bo Tang, and Muning Wen. Memrl: Self-evolving agents via runtime reinforcement learning on episodic memory, 2026. https://arxiv.org/abs/2601.03192.

Wenlin Zhang, Xiaopeng Li, Yingyi Zhang, Pengyue Jia, Yichao Wang, Huifeng Guo, Yong Liu, and Xiangyu Zhao. Deep research: A survey of autonomous research agents, 2025p. https://arxiv.org/abs/2508.12752.

Wentao Zhang, Lingxuan Zhao, Haochong Xia, Shuo Sun, Jiaze Sun, Molei Qin, Xinyi Li, Yuqing Zhao, Yilei Zhao, Xinyu Cai, Longtao Zheng, Xinrun Wang, and Bo An. A multimodal foundation agent for financial trading: Tool-augmented, diversified, and generalist, 2024. https://arxiv.org/abs/2402.18485.

Yaoze Zhang, Rong Wu, Pinlong Cai, Xiaoman Wang, Guohang Yan, Song Mao, Ding Wang, and Botian Shi. Leanrag: Knowledge-graph-based generation with semantic aggregation and hierarchical retrieval, 2025q. https: //arxiv.org/abs/2508.10391.

Yuxiang Zhang, Jiangming Shu, Ye Ma, Xueyuan Lin, Shangxi Wu, and Jitao Sang. Memory as action: Autonomous context curation for long-horizon agentic tasks. CoRR, abs/2510.12635, 2025r. doi: 10.48550/ARXIV.2510.12635. https://doi.org/10.48550/arXiv.2510.12635.

Zeyu Zhang, Quanyu Dai, Xiaohe Bo, Chen Ma, Rui Li, Xu Chen, Jieming Zhu, Zhenhua Dong, and Ji-Rong Wen. A survey on the memory mechanism of large language model-based agents. ACM Transactions on Information Systems, 43(6):1–47, 2025s.

Zeyu Zhang, Quanyu Dai, Xu Chen, Rui Li, Zhongyang Li, and Zhenhua Dong. Memengine: A unified and modular library for developing advanced memory of llm-based agents, 2025t. https://arxiv.org/abs/2505.02099.

Zeyu Zhang, Quanyu Dai, Rui Li, Xiaohe Bo, Xu Chen, and Zhenhua Dong. Learn to memorize: Optimizing llm-based agents with adaptive memory framework. CoRR, abs/2508.16629, 2025u. doi: 10.48550/ARXIV.2508.16629. https://doi.org/10.48550/arXiv.2508.16629.

Zeyu Zhang, Yang Zhang, Haoran Tan, Rui Li, and Xu Chen. Explicit vs implicit memory: Exploring multi-hop complex reasoning over personalized information. arXiv preprint arXiv:2508.13250, 2025v.

Zhenyu Zhang, Ying Sheng, Tianyi Zhou, Tianlong Chen, Lianmin Zheng, Ruisi Cai, Zhao Song, Yuandong Tian, Christopher Ré, Clark W. Barrett, Zhangyang Wang, and Beidi Chen. H2O: heavy-hitter oracle for eficient generative inference of large language models. In Alice Oh, Tristan Naumann, Amir Globerson, Kate Saenko, Moritz Hardt,

and Sergey Levine, editors, Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023, 2023. http: //papers.nips.cc/paper\_files/paper/2023/hash/6ceefa7b15572587b78ecfcebb2827f8-Abstract-Conference.html.

Andrew Zhao, Daniel Huang, Quentin Xu, Matthieu Lin, Yong-Jin Liu, and Gao Huang. Expel: LLM agents are experiential learners. In Michael J. Wooldridge, Jennifer G. Dy, and Sriraam Natarajan, editors, Thirty-Eighth AAAI Conference on Artificial Intelligence, AAAI 2024, Thirty-Sixth Conference on Innovative Applications of Artificial Intelligence, IAAI 2024, Fourteenth Symposium on Educational Advances in Artificial Intelligence, EAAI 2014, February 20-27, 2024, Vancouver, Canada, pages 19632–19642. AAAI Press, 2024. doi: 10.1609/AAAI.V38I17.29936. https://doi.org/10.1609/aaai.v38i17.29936.

Di Zhao, Longhui Ma, Siwei Wang, Miao Wang, and Zhao Lv. COLA: A Scalable Multi-Agent Framework For Windows UI Task Automation. CoRR, abs/2503.09263, 2025a. doi: 10.48550/ARXIV.2503.09263. https://doi.org/10.48550/ arXiv.2503.09263. arXiv: 2503.09263.

Linxi Zhao, Sofian Zalouk, Christian K. Belardi, Justin Lovelace, Jin Peng Zhou, Ryan Thomas Noonan, Dongyoung Go, Kilian Q. Weinberger, Yoav Artzi, and Jennifer J. Sun. Pre-training limited memory language models with internal and external knowledge, 2025b. https://arxiv.org/abs/2505.15962.

Shitian Zhao, Haoquan Zhang, Shaoheng Lin, Ming Li, Qilong Wu, Kaipeng Zhang, and Chen Wei. Pyvision: Agentic vision with dynamic tooling, 2025c. https://arxiv.org/abs/2507.07998.

Siyan Zhao, Mingyi Hong, Yang Liu, Devamanyu Hazarika, and Kaixiang Lin. Do llms recognize your preferences? evaluating personalized preference following in llms. In The Thirteenth International Conference on Learning Representations, ICLR 2025, Singapore, April 24-28, 2025. OpenReview.net, 2025d. https://openreview.net/ forum?id=QWunLKbBGF.

Boyuan Zheng, Michael Y. Fatemi, Xiaolong Jin, Zora Zhiruo Wang, Apurva Gandhi, Yueqi Song, Yu Gu, Jayanth Srinivasa, Gaowen Liu, Graham Neubig, and Yu Su. Skillweaver: Web agents can self-improve by discovering and honing skills. CoRR, abs/2504.07079, 2025a. doi: 10.48550/ARXIV.2504.07079. https://doi.org/10.48550/arXiv. 2504.07079.

Junhao Zheng, Xidi Cai, Qiuke Li, Duzhen Zhang, ZhongZhi Li, Yingying Zhang, Le Song, and Qianli Ma. Lifelongagentbench: Evaluating llm agents as lifelong learners. arXiv preprint arXiv:2505.11942, 2025b.

Longtao Zheng, Rundong Wang, Xinrun Wang, and Bo An. Synapse: Trajectory-as-Exemplar Prompting with Memory for Computer Control. In The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenReview.net, 2024a. https://openreview.net/forum?id=Pc8AU1aF5e.

Yicong Zheng, Kevin L. McKee, Thomas Miconi, Zacharie Bugaud, Mick van Gelderen, and Jed McCaleb. Goaldirected search outperforms goal-agnostic memory compression in long-context memory tasks, 2025c. https: //arxiv.org/abs/2511.21726.

Yuanhang Zheng, Peng Li, Wei Liu, Yang Liu, Jian Luan, and Bin Wang. ToolRerank: Adaptive and Hierarchy-Aware Reranking for Tool Retrieval. In Nicoletta Calzolari, Min-Yen Kan, Véronique Hoste, Alessandro Lenci, Sakriani Sakti, and Nianwen Xue, editors, Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation, LREC/COLING 2024, 20-25 May, 2024, Torino, Italy, pages 16263–16273. ELRA and ICCL, 2024b. https://aclanthology.org/2024.lrec-main.1413.

Siru Zhong, Weilin Ruan, Ming Jin, Huan Li, Qingsong Wen, and Yuxuan Liang. Time-vlm: Exploring multimoda vision-language models for augmented time series forecasting. CoRR, abs/2502.04395, 2025. doi: 10.48550/ARXIV. 2502.04395. https://doi.org/10.48550/arXiv.2502.04395.

Wanjun Zhong, Lianghong Guo, Qiqi Gao, He Ye, and Yanlin Wang. Memorybank: Enhancing large language models with long-term memory. In Proceedings of the AAAI Conference on Artificial Intelligence, pages 19724–19731, 2024.

Huichi Zhou, Yihang Chen, Siyuan Guo, Xue Yan, Kin Hei Lee, Zihan Wang, Ka Yiu Lee, Guchun Zhang, Kun Shao, Linyi Yang, and Jun Wang. Memento: Fine-tuning LLM agents without fine-tuning llms. CoRR, abs/2508.16153, 2025a. doi: 10.48550/ARXIV.2508.16153. https://doi.org/10.48550/arXiv.2508.16153.

Jinfeng Zhou, Zhuang Chen, Dazhen Wan, Bosi Wen, Yi Song, Jifan Yu, Yongkang Huang, Pei Ke, Guanqun Bi, Libiao Peng, Jiaming Yang, Xiyao Xiao, Sahand Sabour, Xiaohan Zhang, Wenjing Hou, Yijia Zhang, Yuxiao Dong, Hongning Wang, Jie Tang, and Minlie Huang. Characterglm: Customizing social characters with large language models. In Franck Dernoncourt, Daniel Preotiuc-Pietro, and Anastasia Shimorina, editors, Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing: EMNLP 2024 - Industry Track, Miami,

Florida, USA, November 12-16, 2024, pages 1457–1476. Association for Computational Linguistics, 2024a. doi: 10.18653/V1/2024.EMNLP-INDUSTRY.107. https://doi.org/10.18653/v1/2024.emnlp-industry.107.

Shuyan Zhou, Frank F Xu, Hao Zhu, Xuhui Zhou, Robert Lo, Abishek Sridhar, Xianyi Cheng, Tianyue Ou, Yonatan Bisk, Daniel Fried, et al. Webarena: A realistic web environment for building autonomous agents. arXiv preprint arXiv:2307.13854, 2023a.

Shuyan Zhou, Frank F. Xu, Hao Zhu, Xuhui Zhou, Robert Lo, Abishek Sridhar, Xianyi Cheng, Tianyue Ou, Yonatan Bisk, Daniel Fried, Uri Alon, and Graham Neubig. Webarena: A realistic web environment for building autonomous agents, 2024b. https://arxiv.org/abs/2307.13854.

Sizhe Zhou and Jiawei Han. A simple yet strong baseline for long-term conversational memory of llm agents, 2025a. https://arxiv.org/abs/2511.17208.

Sizhe Zhou and Jiawei Han. A simple yet strong baseline for long-term conversational memory of llm agents, 2025b. https://arxiv.org/abs/2511.17208.

Wangchunshu Zhou, Yuchen Eleanor Jiang, Peng Cui, Tiannan Wang, Zhenxin Xiao, Yifan Hou, Ryan Cotterell, and Mrinmaya Sachan. Recurrentgpt: Interactive generation of (arbitrarily) long text, 2023b. https://arxiv.org/abs/ 2305.13304.

Wangchunshu Zhou, Yuchen Eleanor Jiang, Long Li, Jialong Wu, Tiannan Wang, Shi Qiu, Jintian Zhang, Jing Chen, Ruipu Wu, Shuai Wang, Shiding Zhu, Jiyu Chen, Wentao Zhang, Ningyu Zhang, Huajun Chen, Peng Cui, and Mrinmaya Sachan. Agents: An open-source framework for autonomous language agents. CoRR, abs/2309.07870, 2023c. doi: 10.48550/ARXIV.2309.07870. https://doi.org/10.48550/arXiv.2309.07870.

Wangchunshu Zhou, Yixin Ou, Shengwei Ding, Long Li, Jialong Wu, Tiannan Wang, Jiamin Chen, Shuai Wang, Xiaohua Xu, Ningyu Zhang, Huajun Chen, and Yuchen Eleanor Jiang. Symbolic learning enables self-evolving agents. CoRR, abs/2406.18532, 2024c. doi: 10.48550/ARXIV.2406.18532. https://doi.org/10.48550/arXiv.2406.18532.

Yiqing Zhou, Yu Lei, Shuzheng Si, Qingyan Sun, Wei Wang, Yifei Wu, Hao Wen, Gang Chen, Fanchao Qi, and Maosong Sun. From context to edus: Faithful and structured context compression via elementary discourse unit decomposition, 2026. https://arxiv.org/abs/2512.14244.

Zijian Zhou, Ao Qu, Zhaoxuan Wu, Sunghwan Kim, Alok Prakash, Daniela Rus, Jinhua Zhao, Bryan Kian Hsiang Low, and Paul Pu Liang. MEM1: Learning to synergize memory and reasoning for eficient long-horizon agents. arXiv preprint arXiv:2506.15841, 2025b.

Andrew Zhu, Lara Martin, Andrew Head, and Chris Callison-Burch. CALYPSO: LLMs as dungeon masters’ assistants. In Proceedings of the Nineteenth AAAI Conference on Artificial Intelligence and Interactive Digital Entertainment, volume 19 of AIIDE ’23, pages 380–390, Salt Lake City, October 2023. AAAI Press. ISBN 978-1-57735-883-1. doi: 10.1609/aiide.v19i1.27534.

Wazeer Deen Zulfikar, Samantha W. T. Chan, and Pattie Maes. Memoro: Using large language models to realize a concise interface for real-time memory augmentation. In Florian ’Floyd’ Mueller, Penny Kyburz, Julie R. Williamson, Corina Sas, Max L. Wilson, Phoebe O. Toups Dugas, and Irina Shklovski, editors, Proceedings of the CHI Conference on Human Factors in Computing Systems, CHI 2024, Honolulu, HI, USA, May 11-16, 2024, pages 450:1–450:18. ACM, 2024. doi: 10.1145/3613904.3642450. https://doi.org/10.1145/3613904.3642450.

Jialong Zuo, Yongtai Deng, Lingdong Kong, Jingkang Yang, Rui Jin, Yiwei Zhang, Nong Sang, Liang Pan, Ziwei Liu, and Changxin Gao. Videolucy: Deep memory backtracking for long video understanding, 2025. https: //arxiv.org/abs/2510.12422.
