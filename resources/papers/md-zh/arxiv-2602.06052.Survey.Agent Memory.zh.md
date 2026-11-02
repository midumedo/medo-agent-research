> 本文为 AI 译文，由 DeepSeek-V4.1-Flash 于 2026-11-02 翻译自源文件 `arxiv-2602.06052.Survey.Agent Memory.md`。

---
stem: arxiv-2602.06052.Survey.Agent Memory
id: arxiv-2602.06052
keywords: [memory, agent, survey, personalization]
abstract: "人工智能研究正从以模型创新与 benchmark 分数为优先，转向强调问题定义与严谨的真实世界评估。随着该领域进入“下半场”，核心挑战变成了在 long-horizon、动态且依赖用户的场景中实现真实效用，例如 agentic coding、deep research 与 computer use；在这些场景中，基于 LLM 的 agent 面临超出固定 context window 的 context explosion，必须跨扩展交互持续积累、管理并选择性复用大量信息。因此，memory——2025 年有数百篇相关论文发表——成为填补这一 utility gap 的关键解决方案。除了作为被动存储，memory 日益成为 agent 借以 self-evolving 的 substrate：short-term memory 在执行过程中对哪些经验被感知、选择和抽象进行门控，而 long-term memory 则积累这些经验，并经 consolidation 转化为可复用的知识与技能，形成 agent 从自身经验中改进并维持 continual learning 的回路。在本综述中，我们从三个维度给出 foundation agent memory 的统一视图：memory substrate（内部 parametric state 与外部 retrieval-augmented 存储）、cognitive mechanism（sensory、working、episodic、semantic 与 procedural memory）以及 memory subject（user-centric 的个性化与 agent-centric 的经验）。随后，我们分析 memory 在 single-agent 与 multi-agent 拓扑下如何被操作，并重点讨论 memory operation 之上的学习策略，展示 memory management 本身如何正在成为一项可训练的、self-evolving 的能力，涵盖 RL 驱动的 context curation、决策时的 experience consolidation，以及经由 agent harness、context engineering 与标准化工具中介协议浮现出来的显式、可移植、可共享的 agent 技能这一新兴生态。最后，我们回顾用于评估 memory utility 的 evaluation benchmark 与指标，并概述各类开放挑战与未来方向。"
revised: 2026-08-04
source: "https://arxiv.org/abs/2602.06052"
parser: mineru-cloud 3.4.4
---

# 下半场中的 Agent Memory 综述：迈向 Self-Evolving 与 Long-Horizon Agents

Wei-Chieh Huang<sup>1,†</sup>, Weizhi Zhang<sup>1,†,‡</sup>, Yueqing Liang<sup>2,†</sup>, Yuanchen Bei<sup>3,∗</sup>, Yankai Chen<sup>1,18,∗</sup>, Tao Feng<sup>3,∗</sup>, Xinyu Pan<sup>4,∗</sup>, Zhen Tan<sup>5,∗</sup>, Yu Wang<sup>14,∗</sup>, Tianxin Wei<sup>3,∗</sup>, Shanglin Wu<sup>6,∗</sup>, Ruiyao Xu<sup>7,∗</sup>, Liangwei Yang<sup>22,∗</sup>, Rui Yang<sup>3,∗</sup>, Wooseong Yang<sup>1,∗</sup>, Chin-Yuan Yeh<sup>1,∗</sup>, Hanrong Zhang<sup>1,∗</sup>, Haozhen Zhang<sup>8,∗</sup>, Siqi Zhu<sup>3,∗</sup>, Henry Peng Zou<sup>1</sup>, Wanjia Zhao<sup>21</sup>, Song Wang<sup>9</sup>, Wujiang Xu<sup>10</sup>, Zixuan Ke<sup>22</sup>, Zheng Hui<sup>11</sup>, Dawei Li<sup>5</sup>, Yaozu Wu<sup>13</sup>, Langzhou He<sup>1</sup>, Chen Wang<sup>1</sup>, Xiongxiao Xu<sup>2</sup>, Baixiang Huang<sup>6</sup>, Juntao Tan<sup>22</sup>, Shelby Heinecke<sup>22</sup>, Huan Wang<sup>22</sup>, Caiming Xiong<sup>22</sup>, Ahmed A. Metwally<sup>23</sup>, Jun Yan<sup>23</sup>, Chen-Yu Lee<sup>23</sup>, Hanqing Zeng<sup>24</sup>, Yinglong Xia<sup>24</sup>, Xiaokai Wei<sup>25</sup>, Ali Payani<sup>26</sup>, Yu Wang<sup>27</sup>, Haitong Ma<sup>12</sup>, Wenya Wang<sup>8</sup>, Chenguang Wang<sup>15</sup>, Yu Zhang<sup>16</sup>, Xin Eric Wang<sup>17</sup>, Yongfeng Zhang<sup>10</sup>, Jiaxuan You<sup>3</sup>, Hanghang Tong<sup>3</sup>, Xiao Luo<sup>4</sup>, Xue Liu<sup>18,19</sup>, Yizhou Sun<sup>20</sup>, Wei Wang<sup>20</sup>, Julian McAuley<sup>14</sup>, James Zou<sup>21</sup>, Jiawei Han<sup>3</sup>, Philip S. Yu<sup>1,¶</sup>, Kai Shu<sup>6,¶</sup>

<sup>†</sup>共同第一作者 <sup>∗</sup>核心贡献者（按字母顺序排列） <sup>‡</sup>项目组织者 <sup>¶</sup>核心导师

<sup>1</sup> UIC <sup>2</sup> IIT <sup>3</sup> UIUC <sup>4</sup> UW–Madison <sup>5</sup> ASU <sup>6</sup> Emory <sup>7</sup> Northwestern <sup>8</sup> NTU <sup>9</sup> UCF <sup>10</sup> Rutgers <sup>11</sup> Cambridge <sup>12</sup> Harvard <sup>13</sup> UTokyo <sup>14</sup> UCSD <sup>15</sup> UCSC <sup>16</sup> TAMU <sup>17</sup> UCSB <sup>18</sup> MBZUAI <sup>19</sup> McGill <sup>20</sup> UCLA <sup>21</sup> Stanford <sup>22</sup> Salesforce <sup>23</sup> Google <sup>24</sup> Meta <sup>25</sup> Roblox <sup>26</sup> Cisco <sup>27</sup> Capital One

Reviewed on OpenReview: https: //openreview. net/forum?id=XycbogUAeJ

## AgentMemoryWorld/Awesome-Agent-Memory

![](../assets/arxiv-2602.06052-fig1.jpg)  
图 1：foundation agent memory 路线图。该时间线展示了 2023 至 2025 年间发布的 foundation agent memory 框架的趋势，并沿三个分类维度中的两个进行归类：memory substrate（内部、外部或混合）与 memory subject（user-centric 或 agent-centric）。

## 目录

1 引言 3
2 背景 6
2.1 LLM 与 Foundation Agents 6
2.2 Memory 7
3 Foundation Agents 中的 Memory 分类 8
3.1 Memory Substrates 8
3.2 Memory Cognitive Mechanisms 14
3.3 Memory Subjects 20
4 Memory Operation Mechanism 24
4.1 Single-Agent Systems 的 Memory Operations 24
4.2 Multi-Agent Systems 的 Memory Operations 27
5 Memory Evolution 与 Optimization Policies 30
5.1 Prompt-Driven Memory Evolution 与 Optimization 31
5.2 Parameterized Memory Policies 的 Fine-Tuning 32
5.3 Memory Policies 的 Reinforcement Learning 33
6 Evolving 与 Scaling：Memory、Contexts 与 Environments 34
6.1 Context-Limited Simple Environments 34
6.2 Context-Exploded Real-World Environments 35
7 Evaluation 37
7.1 Metrics 39
7.2 Benchmarks 40
8 应用 44
9 未来方向 49
9.1 Memory for Continual Learning 与 Self-Evolving Agents 49
9.2 Multi-Human-Agent Memory Organization 50
9.3 Memory Infrastructure 与 Efficiency 51
9.4 Lifelong Personalization 与 Trustworthy Memory 51
9.5 Memory for Multimodal、Embodied 与 World-Model Agents 52
9.6 Real-World Benchmarking 与 Evaluations 53
10 结论 53

## 摘要

人工智能研究正在经历一次范式转变：从优先考虑模型创新与 benchmark 分数，转向强调问题定义与严谨的真实世界评估。随着该领域进入“下半场”，核心挑战变成了在 long-horizon、动态且依赖用户的场景中实现真实效用，例如 agentic coding、深度研究与计算机使用；在这些场景中，基于 LLM 的 agent 面临超出固定 context window 的 context explosion，必须跨扩展交互持续积累、管理并选择性复用大量信息。因此，memory——2025 年有数百篇相关论文发表——成为填补这一 utility gap 的关键解决方案。除了作为被动存储，memory 日益成为 agent 借以 self-evolving 的 substrate：short-term memory 在执行过程中对哪些经验被感知、选择和抽象进行门控，而 long-term memory 则积累这些经验，并经 consolidation 转化为可复用的知识与技能，形成 agent 从自身经验中改进并维持 continual learning 的回路。在本综述中，我们从三个维度给出 foundation agent memory 的统一视图：memory substrate（内部 parametric state 与外部 retrieval-augmented 存储）、cognitive mechanism（sensory、working、episodic、semantic 与 procedural memory）以及 memory subject（user-centric 的个性化与 agent-centric 的经验）。随后，我们分析 memory 在 single-agent 与 multi-agent 拓扑下如何被操作，并重点讨论 memory operation 之上的学习策略，展示 memory management 本身如何正在成为一项可训练的、self-evolving 的能力，涵盖 RL 驱动的 context curation、决策时的 experience consolidation，以及经由 agent harness、context engineering 与标准化工具中介协议浮现出来的显式、可移植、可共享的 agent 技能这一新兴生态。最后，我们回顾用于评估 memory utility 的 evaluation benchmark 与指标，并概述各类开放挑战与未来方向。

## 1 引言

AI 的格局如今已经经历了一次根本性的范式转变：从优先考虑基础模型架构与简化的 benchmark 表现，转向强调问题定义与严谨的真实世界评估。这标志着 AI 发展“上半场”的结束——在这一阶段，进展主要由训练方法（Liu et al., 2024a）、规模扩展（He et al., 2016; Achiam et al., 2023; Gu et al., 2025）与模型架构（Vaswani et al., 2017）驱动，它们不断在标准化 benchmark 上推高分数（Wang et al., 2024m; Krizhevsky et al., 2012）。在此期间，该领域收敛到一种以数据与模型规模扩展为主导的范式。该范式遵循一条通用配方：先进行大规模预训练（Minaee et al., 2024），随后进行后训练过程（Ouyang et al., 2022），从而以惊人的准确率解决传统 benchmark 问题。在定义良好的训练流程下，LLM 与 agent 可以在 MMLU（Hendrycks et al., 2021b）或 MATH（Hendrycks et al., 2021c）等 benchmark 上达到 90% 以上的准确率。因此，LLM 与 agent 已迅速从静态预测器（如传统机器学习模型）演化为通用 agent，能够在各类任务与环境中进行复杂推理（Wu et al., 2025f）、规划（Li et al., 2025i）与工具使用（Huang et al., 2025a; Zou et al., 2025b）。在本综述中，我们将 foundation agent 定义为由基础模型（如 LLM、VLM 或世界模型）驱动，并辅以感知、推理、规划、工具使用与 memory management 的自主或半自主系统（更多细节见第 2 节）。

尽管在标准 benchmark 上展现了令人印象深刻的能力，但所报告的性能与许多真实世界任务和环境中的效用之间仍存在显著差距（Yu et al., 2024b）。大多数评估协议在很大程度上简化了实验假设，并设计了静态、预定义的规则，任务设置相对短小且孤立（Cobbe et al., 2021; Chen et al., 2021; Budzianowski et al., 2018）。特别是，近期大多数 agent 评估 benchmark 都与较短的 agent 执行时间相绑定，缺乏多轮、长期交互（Wang et al., 2024j; Lu et al., 2025a）。因此，这些评估不再能反映 foundation agent 在现实中的能力——现实中的交互本质上具有 long-horizon、long-context 以及深度依赖用户的高复杂度特征。随着该领域转向更真实的设置，例如具身 agent（Li et al., 2024b）、GUI 自动化（Ye et al., 2025a）、agentic coding 与计算机使用、深度研究（Huang et al., 2025c）、个人健康护理（Zhan et al., 2024）以及人—agent 协作（Feng et al., 2024; Zou et al., 2025c），运行环境的复杂度急剧膨胀，使 agent 暴露在异常庞大且动态的 context 之中。在此类环境中，静态的、一次性的能力已不足以应对。相反，agent 必须跨交互积累、保留并选择性复用信息。因此，memory 成为弥合理想化 benchmark 性能与真实世界实现及环境之间差距的关键且自然的解决方案（Zhang et al., 2025q）。不同于固定任务的 AI 系统——其 memory 主要优化效率与成本——foundation agent 要求 memory 能够支持持续积累、选择性复用、跨 session 保留以及在动态、long-horizon 环境中的用户适应。

![](../assets/arxiv-2602.06052-fig2.jpg)  
图 2：foundation agent memory 的分类。对 foundation agent 而言，memory substrate（以何种形式表示）包括 internal memory 与 external memory（§3.1），其中 internal memory 涵盖权重、latent state 与 KV cache（§3.1.2），external memory 涵盖 vector index、text record 与结构化/hierarchical storage（§3.1.1）。在 memory cognitive mechanism（memory 如何发挥作用）视角下，memory 被分为 sensory memory、working memory、episodic memory、semantic memory 与 procedural memory（§3.2；各类型见 §3.2.1–§3.2.5）。基于 memory subject（为谁提供支持），memory 被刻画为 user-centric 的视角与 agent-centric 的视角（§3.3）。

随着该领域进入 AI 发展的“下半场”，焦点从改进训练配方转向解决现实中的关键效用问题（Bell et al., 2025; Yao et al., 2025）。如何设计 benchmark 以在真实环境中评估 agent，已成为最重要的挑战之一（Xu et al., 2025c），尤其是当 agent 努力沿两个主要经验维度进行适应时：面向用户的个性化（Cai et al., 2025; Zhang et al., 2025o; Wu et al., 2025e）与面向任务的专门化（Ling et al., 2025; Zhang et al., 2025i）。在这两个维度上，特定用户长期历史的交互 context，或编码（Islam et al., 2024）与网络搜索（He et al., 2024a）这类垂直任务的交互 context，都远远超出了仅靠基于 prompt 的机制所能容纳的范围。随着日常交互的 multi-session 数据或项目工作积累的 context 呈指数增长，依赖静态 memory mechanism 已不足够。因此，memory architecture 从静态、预定义且简单的机制（Hao et al., 2023; Hu et al., 2023）演化为自适应、self-evolving 且灵活的单元（Liu et al., 2025g;f），以智能地存储、加载、总结、遗忘与精炼 memory，从而为下游任务保留有信息量的经验。

这一转变在 memory 层级上形成了一个闭环：working memory 门控哪些内容进入并留在活动 context 中，而其策展策略越来越多地通过 RL 端到端训练，而非手工设计的启发式规则（Zhang et al., 2025p; Yuan et al., 2025a; Zhou et al., 2025c; Yu et al., 2025b）；被保留的经验积累为 episodic record，反思与 consolidation 将其经 distillation 形成语义事实与程序技能（Yang et al., 2025a; Liu et al., 2025b; Ouyang et al., 2025），这些内容进一步被外化为显式、可组合且可共享的技能，由 agent 自主归纳、修订与维护，并由现代 agent harness 通过 context engineering 与标准化工具中介协议加以暴露（Wang et al., 2025c; Anthropic, 2025; Belikova et al., 2026; Song et al., 2026; Zhang et al., 2026a）。因此，memory 不仅是 agent 历史的接口，更是 agent self-evolving 本身的 substrate（Gao et al., 2025a），这条线索贯穿 cognitive mechanism（第 3.2 节）、memory operation（第 4 节）与学习策略（第 5 节）。

尽管 foundation agent memory 研究的快速增长已产生若干综述，但在从系统设计视角分析真实世界 agent 效用设置中的 agent memory 方面，仍存在重要空白。此类 memory design 已从短小、孤立的 prompt 转向 long-horizon 交互，agent 必须在爆炸式增长的 context window、multi-session 工作流以及持续的真实世界用户关系之上运行。早期工作往往主要按任务应用或管理策略来组织 memory（Zhang et al., 2025q; Du et al., 2025），或采用受神经科学启发的视角，通过功能类比与 memory 生命周期将 AI memory 投射到人类 memory 上（Wu et al., 2025g; Liang et al., 2025）。这些方法虽然提供了有用的概念基础，但并未系统刻画底层 memory substrate，也未显式建模 memory 在 agent system 中所服务的 subject，而后者在 context 超出基础模型限制时尤为重要。因此，它们未能区分 agent memory 的优化目标，也忽视了在真实世界应用中设计与部署自主 agent system 所必需的、跨互补维度的联系。较新的工作开始拓宽这一概念图景。特别是 Hu et al. (2025d) 沿形式、功能与时间动态来组织 agent memory。尽管提供了有价值的 memory consolidation，但它在很大程度上仍不完整，主要关注 memory 在 agent-centric 的任务中如何发挥作用，而非 memory 应如何为用户设计、优化与部署。本综述的动机源于当前文献在 retrieval-augmented generation（RAG）系统、long-context 建模、认知 memory architecture、个性化、continual learning、反思与 agent 评估等方面的碎片化，使研究者难以理解不同 memory mechanism 之间如何关联，以及如何为真实部署设计 memory system。我们的综述通过三项贡献填补这一空白：(1) 一个连接 substrate、mechanism 与 subject 的三维分类体系——这些维度在以往综述中往往被分开讨论；(2) 对 memory 如何在 single-agent 与 multi-agent 拓扑中被实例化、操作与评估的系统设计分析；(3) 将 memory 定位为 AI 发展“下半场”中真实世界效用以及 agent self-evolving 与 self-improvement 的核心机制，并提出六项开放挑战以指导未来研究。为此，我们从三个主要的互补视角分析数百篇论文中的 foundation agent memory，将 memory 与日益复杂环境中的系统级设计选择联系起来。

具体而言，我们引入一个围绕三个核心设计维度组织的统一分类体系：memory substrate、cognitive mechanism 与 memory subject，如图 2 所示。我们按 substrate 将现有的 foundation agent memory 工作分为外部与内部，按 cognitive mechanism 分为 sensory、working、episodic、semantic 与 procedural memory 等功能类别，按 subject 分为 user-centric 与 agent-centric 的 subject。从系统视角出发，我们进一步分析这些 foundation agent memory 系统在不同 agent 拓扑下如何被操作，区分单 agent system 中的基本 memory operation 与 multi-agent 设置中的 memory routing。此外，我们强调学习策略日益增长的作用，展示 agent 如何越来越多地被训练以掌握 memory management 本身，从而从其交互历史中学习并随时间 self-evolving。这些学得的策略闭合了短期选择与 long-term consolidation 之间的环路，将 memory 从被动管理的资源转变为主动演化的能力。为反映环境变化对 foundation agent memory 设计的影响，我们讨论跨交互时程、环境复杂度以及交互 agent 与系统数量方面的可扩展性问题，并回顾用于衡量 memory 性能与效用的评估方法与指标。最后，我们概述 foundation agent memory 中的六项开放挑战，以指导下一代 foundation agent memory 设计。

![](../assets/arxiv-2602.06052-chart1.jpg)

![](../assets/arxiv-2602.06052-chart2.jpg)

![](../assets/arxiv-2602.06052-chart3.jpg)  
图 3：LLM agent 中 memory 相关研究的累计发表趋势（2023 年第一季度至 2025 年第四季度）。图中展示了所收集的 218 篇论文在三个关键维度上的分布：memory substrate（左）、memory cognitive mechanism（中）与 memory subject（右）。阴影区域突出显示了 2025 年研究产出的迅速加速。在左图中，外部与内部各自指存储在模型之外（§3.1.1）的 memory 与保存在模型权重及推理时状态中的 memory（§3.1.2）。中图与右图分别对应 cognitive mechanism（§3.2）与 memory subject（§3.3）。单篇论文可能体现多种 cognitive mechanism，因此中图的总和超过所收集的 218 篇论文，而左图与右图则对其进行了划分。

## 2 背景

## 2.1 LLM 与 Foundation Agents

近期的进展已将 LLM 超越一次性问答，推进到 foundation agent（Park et al., 2023; Xi et al., 2025a; Luo et al., 2025; Liu et al., 2025a）：这类系统能够感知环境、围绕复杂目标进行推理，并执行动作以实现被赋予的目标。与传统“一次性”聊天机器人不同，agent 在一个完整回路中运行：它解读指令、选择动作、观察结果，并更新其内部状态或 memory。这种迭代交互使 agent 特别适合 long-horizon、动态的问题求解。这一趋势已在新兴的 agent 产品中可见，例如 Deep Research 与 Manus，它们强调多步执行与工具增强的决策，而非单轮响应（Zhang et al., 2025l）。

foundation agent 通常是一个自主或半自主系统，它以基础模型（如 LLM）作为核心决策模块，并辅以状态估计、动作执行与 memory management 机制。在本综述中，我们用“foundation agent”一词指代其核心决策由通用基础模型（包括 LLM、VLM 或学得的世界模型）驱动的 AI agent。核心能力通常包括面向任务分解与决策的规划（Yao et al., 2023; Huang et al., 2024b）、通过外部函数或模型的工具使用（Wu et al., 2025c; Yuan et al., 2025c; Lu et al., 2025a）、多模态感知（Liu et al., 2023a;

Bai et al., 2025），以及同时覆盖短期 context 与更 long-horizon 的 memory（Lumer et al., 2025; Wang et al., 2025t）。memory（Zhang et al., 2025q; Xiong et al., 2025d）变得尤为重要，因为 context window 有限且环境随时间演化；因此，许 multi-agent 依赖外部 memory storage，并结合总结（Lu et al., 2025b）、反思（Renze & Guven, 2024）或将经验压缩为可复用知识的 consolidation 流程（Kang et al., 2025c; Yu et al., 2025b）。越来越多的工作进一步将 foundation agent 框定为 self-evolving 系统，它们在部署时从自身的执行经验中改进，而非仅通过离线训练改进（Gao et al., 2025a），并且新兴 benchmark 已开始直接评估这种在 self-evolving memory 之上、由经验驱动的测试时学习（Wei et al., 2025d）。memory 是使这种 self-evolving 成为可能的 substrate：若没有记录、整合与复用经验的机制，每个 episode 都不会给 agent 带来任何改变，long-horizon 交互便退化为一系列孤立的一次性任务。多 agent system（Talebirad & Nadiri, 2023; Wu et al., 2024b）通过为多个通信与协调的 agent 分配专门角色与 memory，扩展了这一范式（Lan et al., 2024; Estornell et al., 2025）。

foundation agent 目前正被探索用于不同的真实世界应用，例如工作流自动化（Xiong et al., 2025c）、辅导（Wang et al., 2025l）、网页与 GUI 交互（He et al., 2024a; Wang et al., 2025e）、模拟或真实环境中的具身控制（Fan et al., 2022; Yang et al., 2025c），以及 agentic 科学辅助的早期形态（Ren et al., 2025; Pantiukhin et al., 2025; Zheng et al., 2025d）。尽管取得了这些进展，若干基础性挑战仍然存在。第一，long-horizon 可靠性（Huang et al., 2024b; Xi et al., 2025b）要求防止误差累积、行为循环与不可靠的重规划。第二，评估（Yehudai et al., 2025）应从静态问答转向衡量动态、交互式能力的 benchmark，例如工具使用、多步决策与 long-horizon 反馈。第三，对齐与安全（Hua et al., 2024; Yuan et al., 2024a; Tian et al., 2023; Zhang et al., 2024d）随着自主性与工具访问的扩展而日益重要，要求对可控性提供更强的保证。解决这些挑战，最终可能将当今的工具使用型助手转变为能力足以解决更复杂任务、且可信到能在真实世界部署中保持可预测与可控的 agent。

## 2.2 Memory

memory 一般指系统随时间保留、组织与利用信息的能力。在基于 LLM 的 foundation agent 语境中，memory 被用来解释 agent 如何超越单轮 context，以支持长期交互、行为一致性与经验积累（Luo et al., 2025）。虽然生物学研究常将 memory 刻画为持续的、经验驱动的神经变化（例如突触可塑性与 consolidation（Hebb, 2005; Bliss & Lømo, 1973; Tonegawa et al., 2015）），但对 agent system 而言，更相关的洞见在于 memory 如何被设计、实现与在实践中使用，以支持不同的功能、表示与目标。

在人类认知模型中，memory 通常被理解为一组跨不同时间尺度组织的、相互作用的子系统。short-term memory 支持在持续处理过程中对信息进行临时保留与操作。sensory memory 短暂缓冲原始感知输入，使下游处理成为可能（Sperling, 1960），而 working memory 在严格容量约束下运行，支持在线信息操作、推理与控制（Baddeley, 2020; 2000）。long-term memory 支持信息在较长时间段内的保留，并由多个功能上不同的系统组成。episodic memory storage 定位于特定时间与 context 的具体经验，semantic memory 积累抽象事实与概念知识（Tulving, 1972; 1985），procedural memory 则捕捉技能、习惯与动作策略，它们通常通过表现而非显式回忆被隐式表达（Cohen & Squire, 1980; Squire, 1992）。至关重要的是，这些子系统并非孤立运行。短期系统决定在持续处理过程中哪些经验被感知、选择与抽象，而长期系统积累这些经验，并经 consolidation 转化为稳定的知识与技能；它们的相互作用——而非任何单个存储——构成了行为随经验改进的回路（Gao et al., 2025a）。我们对 foundation agent 同样采用这种系统观：agent memory 被视为一个整合的层级结构，其操作——从选择与保留到 consolidation 与技能形成——本身可以被设计、优化，并日益从 agent 自身的交互中学习。在生物系统中，memory 的功能区分最终植根于 physical substrate，例如突触可塑性（Hebb, 2005; Bliss & Lømo, 1973; Martin et al., 2000）以及产生持久 memory trace 或 engram 的回路级变化（Tonegawa et al., 2015; Josselyn & Tonegawa, 2020）。虽然这些认知与生物学视角提供了必要的基础，但 foundation agent memory 系统引入了额外的设计考量，包括显式区分 memory 被设计用来捕捉与支持谁的信息、memory 实现于何种 physical substrate、以及 memory 扮演何种认知角色——这三个问题构成了本分类体系的骨架，此外还包括其操作策略如何获得（第 5 节）。

## 3 Foundation Agents 中的 Memory 分类

我们通过以 memory 相关关键词（例如 agent memory、long-term memory、context management、personalization memory）查询 Google Scholar，并人工审阅主要计算机科学会议与期刊（包括顶级 NLP、ML、IR 与 AI 会议）的论文集，进行了系统的文献收集。从最初数百篇论文的候选池出发，我们通过迭代筛选挑选出最相关的贡献，最终选定 2023 年第一季度至 2025 年第四季度间发表的 218 篇关键文章。由此得到的结果趋势见图 3，显示出研究活动的急剧升级；图 1 则沿时间线放置了代表性框架。最值得注意的是，累计发表量在 2025 年全年大幅上升，其中第四季度增长最陡。这些趋势表明，人们日益需要更智能的 memory design，使 agent 能够在日益复杂的环境中完成 long-horizon、long-context 任务。

为更好地区分 memory design，我们沿三个正交视角对 foundation agent 中的 memory 进行分类，如图 2 所示：(1) Memory Substrates，亦称存储格式，描述 memory 在不同设置中以何种形式表示，见第 3.1 节；(2) Memory Cognitive Mechanisms，描述 memory 在流水线或工作流中承担的功能角色，见第 3.2 节；(3) Memory Subjects，即 memory 被设计用来捕捉与支持谁的信息，详见第 3.3 节。此外，我们在图 4 中给出该分类体系。随后，我们讨论 single-agent 与多 agent system 中的 memory operation 与管理（第 4 节）、学习策略（第 5 节）、扩展（第 6 节）、评估（第 7 节）、应用（第 8 节）与开放挑战（第 9 节）。

## 3.1 Memory Substrates

memory substrate 是保留 foundation agent 与人类在各种任务与环境交互过程中所产生的历史知识的必要机制。基于当前研究的框架、存储介质与持久化机制，我们将这些 substrate 分为 external memory 与 internal memory。这两类的定义与实现分别在第 3.1.1 节与第 3.1.2 节详述。

## 3.1.1 External Memory

## External Memory

external memory 指任何将知识、信息与过往经验存储在 agent 模型参数或状态之外的 memory substrate。agent 可以通过 retrieval 与更新操作显式地读写 external memory，从而实现可扩展、易更新、跨 session 保留的知识与交互历史。

external memory 表示以 vector index、text record、structured storage 与 hierarchical storage 来保存信息的存储系统（Lewis et al., 2020; Zhang et al., 2023a）。它独立于神经网络中由梯度更新的权重运行。其特征是计算与知识的清晰分离：计算在 LLM 内部参数中执行，知识存储在外部数据库或 memory module 中（Mallen et al., 2023; Zhong et al., 2024）。这种计算与 retrieval 分离的设计使 agent 无需对基础模型进行昂贵的重新训练，即可访问大量且持续更新的信息（Omidi et al., 2025; Aratchige & Ilmini, 2025）。此外，external memory 既可扩展又灵活。只需少量改动，它便可轻松加入、替换或插入大多数框架。而且，与 internal memory（Saha et al., 2021）不同——在 internal memory 中，知识可能因新经验的权重更新而被覆盖或调整——external memory 能以原始形式保存过往信息，通过额外的存储模块帮助减少幻觉或知识截断（Castrillo et al., 2025）。

![](../assets/arxiv-2602.06052-fig4.jpg)  
图 4：foundation agent memory 系统的分类

然而，这一设计也有缺点与权衡。通常，推理会耗时更长，因为 agent 必须从外部存储中 retrieval 信息。当 agent 在多轮迭代或复杂环境中运行时，这一问题更为严重。此外，retrieval 可能不可靠。如果相似度或排序算法不够完善，它们可能给出与当前任务无关或无帮助的结果。这些无关信息会引入噪声，可能降低 agent 的效用（Xu et al., 2025a）。随着系统运行时间更长、轮次更多，且 memory 不断增长，存储与索引成本的攀升可能进一步削弱效率与性能（Chen et al., 2025e）。因此，构建良好的 external memory 通常需要健全的流程来调控 memory 的规模与质量，包括总结、选择性保留、forgetting、去重以及定期修剪低价值或过时条目（Du et al., 2025; He et al., 2024b）。

vector index。vector index 的实现方式是将 memory entry 或查询嵌入共享向量空间，运行近似最近邻搜索以获取前 k 个条目，并将这些片段附加到 prompt 中作为 grounding context（Lewis et al., 2020; Zou et al., 2025a）。当前 agent 或 LLM 工作中 external memory 的主导实现是向量数据库，在 RAG 框架内使用（Quinn et al., 2025; Li et al., 2025i; Zhang et al., 2025l）。该方法将 memory 作为一个几何问题来操作。通过把文本或多模态信息嵌入高维向量，它将每个 memory entry 表示为连续空间中的一个点。新查询也以相同的 embedding 机制转换为向量，agent 则搜索最近的点，即代表最接近语义信息的数据。现有技术，例如分层可导航小世界（hierarchical navigable small-world，HNSW）（Liu et al., 2025h）、倒排文件（inverted file，IVF）（Rege et al., 2023）或乘积量化（product quantization，PQ）（Huang & Huang, 2024）索引，被开发并优化用于在高维 embedding 空间中高效地找到语义最相似的文档或过往交互。这种近似最近邻搜索 retrieval 出一小部分 context 片段，将其映射回原始形式并输入 agent 或 LLM，使其响应与相关的、此前未见的信息整合（Guu et al., 2020）。

text record。text record 型 memory 将 agent 的 long-term memory 视为一组显式文本文档，而非 embedding 或图（Zhang et al., 2025q）。它实现为持久的人类可读文本产物（例如持续维护的“核心摘要”加 episodic log），这些产物被定期总结或编辑，并在生成下一次响应时被选择性地复制到 prompt 中。一种常见实现保留持久的核心摘要，并用语义列表与 episodic list 加以扩充。语义列表存储离散事实，可通过插入、更新与删除操作修改。相比之下，episodic list 是按时间戳记录事件与交互的时间顺序账本。在 memory update 期间，agent 修改这些结构（Zhu et al., 2025c; Wang & Chen, 2025）。在响应生成期间，它提取有限数量的相关信息与实例，然后将其与主摘要一起重新整合到 prompt 中。该架构通过将 memory 组织为人类可读的摘要与列表，促进了透明性与快速集成（Yue et al., 2025; Park et al., 2023）。然而，它需要细致的总结与修剪，以维持简洁的核心摘要与可控规模的列表。

structured storage。structured storage 的实现方式是将 memory 存入显式 schema，并通过符号查询或遍历进行 retrieval，再将返回的记录格式化为 LLM 的 context。基于拓扑设计的structured memory architecture（Jia et al., 2025a; Bei et al., 2025）可划分为关系表、基于图的 memory 或基于树的 memory。关系表使用 SQL 从表中 retrieval 行记录。它们可以将事实与偏好存储为结构化记录，将短期事务与长期事件分离到不同表中，并使用连接与索引在不同表之间高效 retrieval（Wang et al., 2024d）。基于图的 memory 将 episode 或信息片段表示为 knowledge graph 中的节点与边（Anokhin et al., 2024）。knowledge graph 本质上是一个语义网络。它通常将信息组织为带实体的节点以及捕捉其间关系的边。当新信息到来时，系统将 semantic embedding 与关键词搜索同遍历相结合，以检测边变化、解决冲突并维护有效的图结构（Jiang et al., 2025c）。基于树的 memory 以层次化方式组织知识，树中每个节点存储文本内容的聚合摘要及相应的 semantic embedding，更深的枝叶表示更具体的细节（Sarthi et al., 2024）。当新信息到来时，系统遍历树，并根据 embedding 相似度更新或创建节点，以决定信息存储的位置。这种动态机制支持多级抽象与高效 retrieval，以支撑长对话任务（Rezazadeh et al., 2025b）。structured memory 凭借其不同类型的形式，能够捕捉顺序历史与关系，并支持多级抽象。这一技术为 agent 提供了对 memory 如何存储、更新与查询的灵活性与控制。

hierarchical storage。层次化 memory 将 memory 分离为多个存储单元，每个单元有自己的模式与存储策略。agent 不再把所有内容放在一个扁平档案中，而是维护专门的 memory module（Rezazadeh et al., 2025b; Zhai et al., 2025）。例如，agent 可维护用于持久人设与用户事实的核心 memory、用于时间敏感事件的 episodic memory、用于抽象概念的 semantic memory、用于分步指令的 procedural memory、用于文档与媒体的资源 memory，以及用于敏感或私有信息的知识库（Yang et al., 2025a; Wang et al., 2025q）。每个模块采用适合其内容的数据结构。例如，episodic memory 可能存储带有 event\_type、summary、details 与 timestamp 的记录；semantic memory 可能按 type、summary 与 source 组织条目；procedural memory 将工作流编码为 JSON 序列；知识库则施加严格的访问控制以保护凭据与 API 密钥。元 memory management 器（meta-memory manager）（Wang & Chen, 2025; Zhang et al., 2024a）协调这些模块，将查询导向正确的存储，并为每个存储单元使用专门的 retrieval 方法（例如 embedding 相似度（Xu et al., 2025d）、BM25 匹配（Hu et al., 2025c）、字符串匹配（Alla et al., 2025））。这种多存储 substrate 具有模块化、关注点分离与可扩展性等优势，使其更容易设计专门的模式与 retrieval 路径，同时支持长期交互中细致的个性化。然而，协调多个 memory module 增加了系统的架构复杂度。在查询多个存储时，它可能带来延迟与额外资源成本，并且需要设计良好的机制来维持数据一致性，并在 long-horizon 任务的不同轮次之间同步更新（Sun & Zeng, 2025; Li et al., 2025k; Maragheh & Deldjoo, 2025）。

## 3.1.2 Internal Memory

## Internal Memory

internal memory 指直接存储在模型架构内部的信息，既包括嵌入其参数中的持久知识（即 parametric memory），也包括推理过程中使用的工作状态。


**Weights.** weight memory 通过将 memory write 参数来实现，使模型之后无需 retrieval 外部 context 即可回忆信息。知识或经验通过预训练、后训练或有针对性的参数编辑（Wang et al., 2025r; Ampel et al., 2025; Wang et al., 2024h）直接嵌入神经网络的参数中（Mallen et al., 2023）。由于这些知识是内部的，此类模型能高效且稳健地回忆事实与过往事件，而无需与外部存储通信。然而，维护与更新内部权重颇具挑战。因此，近期研究将权重更新分为三种主要策略：continual learning、模型编辑与 distillation。continual learning 方法用新信息增量更新模型权重，同时尝试避免灾难性 forgetting（De Lange et al., 2021）。诸如对变化施加正则化以防止覆盖重要权重、以及应用软掩码以选择性更新参数的方法，可以在识别新信息的同时在很大程度上保留先前的领域知识（Serra et al., 2018）。模型编辑策略将特定事实关联视为局部 memory 并调整相应参数：一类工作定位决定性中层权重并施加秩一更新以改变单个事实关联，另一类则将这一思想扩展为在多个层上施加小幅更新，从而更新数千条 memory（Meng et al., 2022; 2023）。例如，一些方法表明，用增强数据对模型进行细致 fine-tuning 可以达到可比的编辑性能。另一种方法插入少量新神经元以顺序纠正错误，而不影响无关行为。还有一种方法增加校准 memory 槽（calibration memory slots），在不改变原始参数的情况下存储被纠正的事实（Chhetri et al., 2025; Luo & Specia, 2024）。distillation 技术将 context 知识压缩进参数本身。它们可以通过训练一个学生模型复现被 prompt 的教师模型的输出（例如 prompt-to-weights 或 context 内 distillation），将依赖 prompt 或 context 的行为内化到模型参数中。具体而言，一些方法优化模型，使其在推理时表现得如同某个固定 prompt 被隐式地存在（Cao et al., 2025a; Padmanabhan et al., 2023）。虽然这种基于参数的 memorization 可使推理时的回忆更高效，但修改权重在计算上代价高昂，并可能引入干扰、覆盖或扭曲先前学到的知识（Meng et al., 2023）。

**Latent-State.** latent state memory 通过跨步骤或跨片段携带并复用中间隐藏状态来实现。即使原始 token 已不再位于窗口内，较早的激活仍可直接影响后续计算。中间激活或隐藏状态张量是在前向传播过程中信息流经各层时产生的（Ibanez-Lissen et al., 2025）。这些隐藏状态是逐层表示，将固定的已学参数与当前 prompt 相结合，形成驱动下一 token 预测的模型工作状态。与基于权重的 memory 不同，state memory 并不持久。它通常在运行时激活中产生、被使用，并通常在请求结束时被丢弃或重置。因此，它支持 session 内的连贯性与推理，但除非被导出到外部，否则不会跨 session 持久化知识。关键权衡在于资源成本。环境不仅必须在内存中保存参数，还必须保存中间状态，而这一激活值随模型深度、批大小与精度而变化。高效且优化的 latent state 管理可降低推理延迟与内存成本。一个代表性方向是跨层重建隐藏表示，以可控成本强化较早的 context（Dillon et al., 2025）。与重建相对，另一些工作跨片段缓存隐藏状态向量或 memory token 的一个紧凑子集，从而在降低内存与计算成本的同时，将有效 context length 延伸到固定窗口之外（Dai et al., 2019）。除了复用现有状态，latent state memory 也可以被生成。memory 触发器（memory trigger）与 memory 编织器（memory weaver）合成机器原生的 latent token，并将其反馈给模型以丰富下游推理（Zhang et al., 2025d）。同时，对隐藏状态转移的结构化调制可维持与先前 context 对齐的 latent trajectory，从而减少长序列中的语义漂移（Carson & Reisizadeh, 2025）。此外，一些架构将压缩后的 memory 经 consolidation 融入 attention 机制，以存储并复用先前片段的键值对，从而在有界内存下处理超长输入（Munkhdalai et al., 2024）。其他策略将隐藏状态视为快速权重（fast-weight），在推理期间通过小型优化步骤更新，以在扩展 context 中精炼内部表示（Zhu et al., 2025b）。

**KV Cache.** 在基于 Transformer 的 LLM 中，KV cache 是一种瞬态的推理时 memory，用于加速自回归解码（Kwon et al., 2023; Liu et al., 2023c）。其实现方式是在解码期间缓存先前 token 的逐层注意力键与值，并在后续 token 中复用。在自注意力中，每个 token 被投影为键与值（Ge et al., 2023; Pope et al., 2023）。若不使用 KV cache，这些矩阵会在每一步对所有先前 token 重新计算，导致不必要的资源浪费，并拖慢长序列生成（Cai et al., 2024; Feng et al., 2025b）。KV cache 保存较早 token 的键与值，并在每个新步骤中只对新生成的 token 计算它们，其余从缓存中取回。该机制显著加速推理，尤其是在长输出或大型深层模型上，但代价是更高的内存占用与实现复杂度（Pope et al., 2023; Kwon et al., 2023）。近期研究提出了若干高影响力的 KV cache compression 方法。一种方法认识到少数 token 对注意力分数的贡献最大，并动态驱逐其余 token，在“重击者”（heavy hitters）与近期生成的 token 之间取得平衡。该方法在大幅提升吞吐量的同时仅保留一小部分缓存（Zhang et al., 2023b）。另一项技术识别 prompt 观察窗口内一致的注意力模式，并对重要特征进行聚类，从而在长输入序列上实现可观的加速与内存节省（Li et al., 2024d）。还有一种方法观察到不同层真正需要的键值向量数量不同，于是不再给每层相同的缓存大小，而是按重要性对向量排序，并使用二分搜索在全局预算下决定每层保留多少，从而只保留最具信息量的向量（Wang et al., 2024a）。这些近期研究表明，KV cache 可以被高效地用于显著提升模型性能。

## 3.1.3 Memory Substrates 之间的权衡

不同 memory substrate 可能有不同的优点与缺点。它们在访问速度、可扩展性、适应性与可靠性方面存在权衡，这些权衡在 long-horizon 任务中会迅速显现。在实践中，选择往往归结为快速、精确的内部状态与可扩展但随增长而变得嘈杂的外部存储之间的取舍。表 1 从八个操作维度总结了这些权衡：retrieval 延迟（访问存储信息的时间成本）、存储成本（所需内存占用）、更新灵活性（修改存储内容的难易程度）、context window 开销（对 context window 的额外负担）、跨 session 持久性（信息能否跨 session 存续）、可扩展性（容纳不断增长的 memory 的能力）、forgetting 风险（修改时知识退化的易感性）以及 retrieval 精度（定位相关存储信息的准确性）。

表 1：memory substrate 在八个操作维度上的权衡对比分析。

<table><tr><td>维度</td><td>internal memory（§3.1.2）</td><td>external memory（§3.1.1）</td></tr><tr><td>retrieval 延迟</td><td>低；通过前向传播或驻留 GPU 的缓存访问</td><td>可变；取决于索引结构、语料规模与 retrieval 算法</td></tr><tr><td>存储成本</td><td>高；随模型深度与序列长度增长</td><td>中等；随存储条目增长，与模型架构无关</td></tr><tr><td>更新灵活性</td><td>低；需要 fine-tuning、模型编辑或 distillation</td><td>高；支持显式插入、更新与删除，而无需修改参数</td></tr><tr><td>context window 开销</td><td>对 latent state 与 KV cache substrate 而言显著</td><td>中等；retrieval 到的条目必须序列化进 prompt</td></tr><tr><td>跨 session 持久性</td><td>部分；权重持久，但 latent state 与 KV cache 被丢弃</td><td>永久；条目跨 session 维护</td></tr><tr><td>可扩展性</td><td>受限；参数容量在训练时固定</td><td>高；存储增长与模型架构无关</td></tr><tr><td>forgetting 风险</td><td>parametric substrate 高（灾难性 forgetting）；KV cache 缺乏持久性</td><td>可忽略；原始条目除非被显式修改否则得以保留</td></tr><tr><td>retrieval 精度</td><td>由学得的关联隐式决定；KV cache 在 session 内较高</td><td>可变；对 embedding 质量与排序算法敏感</td></tr><tr><td>代表性工作</td><td>MemoryLLM、WISE、SELF-PARAM（parametric）；vLLMPA、Titans、ChunkKV、EpiCache（latent state/KV）</td><td>Mem0、Zep、A-Mem、HippoRAG2、MIRIX、MemTree</td></tr></table>

internal memory，包括编码在模型权重中的 parametric memory，通常提供高速访问并与推理紧密集成。然而，它更新代价高昂，且可能因频繁修改而遭受灾难性 forgetting。因此，它更适合稳定的通用知识，而非快速变化或用户特定的信息。latent substrate（如隐藏激活或 KV cache）快速且短暂，因而非常适合 session 内状态。然而，其短暂性以及与序列长度成线性关系的扩展限制了容量，使其不适合跨 session 保留。此外，latent state 与 KV cache substrate 直接占用 context 预算，带来显著的 context window 开销，且其存储成本随模型深度、批大小与精度增长。

external memory 由向量数据库或存储组成，随经验自然扩展，并支持无需重新训练的灵活编辑。然而，retrieval 会引入延迟，并使性能对索引与 retrieval 质量敏感。先前工作表明，存储过多或低质量的条目会注入噪声，并增加定位有信息量条目的难度，从而降低紧耦合的决策质量（Liu et al., 2024b）。retrieval 精度进一步取决于 embedding 质量、相似度度量与排序算法，这使其成为外部 memory system 的关键设计考量。为更好地应对该问题，剪枝、总结与层次化组织等显式 memory management 机制是必需且必要的。

总体而言，没有任何单一 substrate 在所有设置与环境中占优，表 1 所总结的互补优势与局限说明了这一点。有效的系统设计日益采用混合 memory architecture：用内部或 parametric memory 承载固有知识或事实，用 latent memory 支持快速短期推理，用 external memory 实现可扩展的经验存储。这一模式反映了更广泛的转变：从静态或持久、定义明确的知识存储机制，转向能够处理真实世界任务复杂性的更动态、更自适应的方法。

## 3.2 Memory Cognitive Mechanisms

人类 memory 为分析基于 LLM 的 agent 中的 memory 提供了概念脚手架（Kim et al., 2023b; Li & Li, 2024; Sumers et al., 2023）。认知心理学区分了多个相互作用的系统，用以解释信息如何被感知、保持与复用（Baddeley, 2020; Tulving, 1972）。尽管文献中提出了广泛的认知 memory 类型，我们聚焦于五类对基于 LLM 的 agent 尤为相关的原子认知 memory system：sensory memory、working memory、episodic memory、semantic memory 与 procedural memory。表 2 通过将这五类 memory system 的核心功能角色映射到代表性研究方向与示例性 agent 级实现来总结它们。这五类系统构成认知 memory 的一个最小且架构上完整的分解，而其他 memory 构念（如自传体 memory（Conway & Pleydell-Pearce, 2000）或前瞻 memory（Einstein & McDaniel, 1990））可被理解为在其之上构建的组合或功能抽象。相应地，我们的分类体系围绕这五种原子 memory 类型组织，它们覆盖了当前 agent 架构中通常以显式或隐式方式实现的短期与长期 memory mechanism。除了各自的功能，这五类系统在 agent self-evolving 中扮演互补角色：短期系统（sensory memory 与 working memory）在执行过程中对哪些经验被感知、选择与抽象进行门控，而长期系统（episodic、semantic 与 procedural memory）积累这些经验，并经 consolidation 转化为可复用的知识与技能，共同形成 agent 从自身经验中改进的回路（Gao et al., 2025a）。

## 3.2.1 Sensory Memory

## Sensory Memory

sensory memory 指对传入感知信号的临时保留，使注意与选择机制能够在更高层处理发生之前运作，其方式是短暂保持原始输入，时间足以让系统决定下一步关注什么。

在当前的 foundation agent 中，sensory memory 通常未被显式建模。这在很大程度上源于文本输入的高度抽象性质：感知处理已被折叠为符号或语言表示。与编码稳定知识的 memory system 不同，sensory memory 作为感知与认知之间的瞬态接口，在极短时间尺度上跨多种感知模态运作（Atkinson & Shifrin, 1968）。然而，在多模态或具身 agent 中，类似机制以短时感知缓冲（short-lived perceptual buffer）的形式出现，例如视觉、听觉或交互 embedding 的缓存。这些缓冲充当感觉阶段，在经最小处理的观察被过滤、总结或路由到 working memory 以供下游推理与控制之前，对其加以临时保留。

只有有限数量的 LLM agent 工作在其 memory architecture 中将 sensory memory 显式实例化为一个独立阶段。HMT（He et al., 2025c）、LightMem（Fang et al., 2025a）与 M2PA（Zhou et al., 2025b）等层次化与多阶段设计将 sensory memory 建模为一个初始缓冲，在选择、压缩或整合进下游 memory 组件之前保留近期的、经最小处理的输入。除这些显式表述之外，隐式的 sensory memory 实现更常见于流式与具身 agent。SAM2（Ravi et al., 2024）与 ReSurgSAM2（Liu et al., 2025d）等系统对近期视频帧维护短期感知队列，而 ReKV（Di et al., 2025）与 V-Rex（Kim et al., 2025a）则依赖流式 KV cache 或 memory 队列，在在线推理期间保留近期 token 或视觉表示。尽管这些机制很少被标注为 sensory memory，但它们通过缓冲近期观察以支持感知连续性与计算效率，发挥着类似功能，并且通常与 working memory 和 semantic memory 紧密耦合，而非作为独立的认知模块实现。

表 2：将五类认知 memory system 映射到其在 foundation agent 中的功能角色与相应 memory design 方向，并附示例性 agent 级案例。

<table><tr><td>认知类型</td><td>功能角色</td><td>LLM agent 中的核心研究焦点（代表性工作）</td><td>实现</td></tr><tr><td colspan="4">short-term memory</td></tr><tr><td>sensory memory</td><td>感知到什么。在进一步处理之前对近期视觉、听觉或其他感觉输入的短暂保留。</td><td>面向多模态流的感知缓冲与轻量缓存，例如短时 embedding 队列与感知状态缓冲（He et al., 2025c; Fang et al., 2025a; Zhou et al., 2025b; Di et al., 2025）。时间门控与选择机制，用于稳定嘈杂或高带宽的观察，以供下游推理与控制（Mon-Williams et al., 2025; Bjorck et al., 2025; Black et al., 2025; Ravi et al., 2024; Liu et al., 2025d）。</td><td>对最近 2–5 秒音频与视频帧（或近期 sensor embedding）的短滚动缓冲，用于平滑感知并处理短暂遮挡。</td></tr><tr><td>working memory</td><td>当前处理什么。对当前信息的临时保持与操作。</td><td>写入前的表示塑形，以减少必须进入活动 context 的内容，包括 compression、折叠与抽象感知表示（Labate et al., 2025; Kang et al., 2025c; Wu et al., 2025d; Sun et al., 2025b; Ye et al., 2025b）。固定预算下的在线状态维护与 self-evolving 策展，包括对 context 与 KV 状态的更新、驱逐与运行时控制，且策展策略日益从 agent 自身经验中学得（Zhang et al., 2025p; Yuan et al., 2025a; Zhou et al., 2025c; Yu et al., 2025b; Zhang et al., 2025j; Kim et al., 2025b; Liu et al., 2025j; Kwon et al., 2023; Ni et al., 2025）。</td><td>进行中的推理状态（思维链）：“目标：精炼综述；前面章节设定了框架；下一次修订应保持框架一致性。”</td></tr><tr><td colspan="4">long-term memory</td></tr><tr><td>episodic memory</td><td>发生了什么。对具体经验的 context 记录。</td><td>episodic record 与结构化，包括写什么、如何组织事件与轨迹、以及多尺度 episode formation（Rajesh et al., 2025; Yeo et al., 2025a;b; Anokhin et al., 2024）。决策时的 retrieval、反思与 experience consolidation，包括自适应触发、episode selection、保留策略，以及将 episode 经 distillation 形成可复用知识以支持 self-evolving（Yeo et al., 2025b; Latimer et al., 2025; Li et al., 2025f; Sarin et al., 2025; Alqithami, 2025; Yang et al., 2025a; Liu et al., 2025b）。</td><td>过往交互日志：“上次你偏好 2 页摘要；上一个计划因缺少 API 密钥而失败”，并连同其时间与情境 context 一起存储。</td></tr><tr><td>semantic memory</td><td>知道什么。关于世界的概念性知识与事实性知识。</td><td>知识归纳与组织为可复用表示，包括 memory 图、模式与紧凑神经表示（Zhao et al., 2025a; Jia et al., 2025a; Li et al., 2025d; Rasmussen et al., 2025; Behrouz et al., 2024; Wang et al., 2024l; Pouransari et al., 2025）。推理期间的知识访问与可靠性控制，包括分布偏移下的选择性激活、验证与持续修订（Jimenez Gutierrez et al., 2024; Wang et al., 2025m; Rezazadeh et al., 2025b; Yan et al., 2025b; Wang et al., 2024f; Alqithami, 2025）。</td><td>知识库：通过查询 retrieval 并检查可靠性的实体或事实（例如项目信息、偏好、定义）。</td></tr><tr><td>procedural memory</td><td>如何行动。技能与动作模式。</td><td>技能归纳与打包，从经验、工具或交互轨迹中学习可复用流程，并日益外化为可移植、可共享的技能（Hong et al., 2024; Fang et al., 2025b; Han et al., 2025; Zhang et al., 2025d; Xia et al., 2025; Wang et al., 2025c; Anthropic, 2025; Xu &amp; Yan, 2026）。技能执行、组合与适应，在 long-horizon 中于变化的情境下调用与精炼流程，包括技能库的 self-evolving 维护（Ouyang et al., 2025; Li et al., 2025h; Tablan et al., 2025; Terranova et al., 2025; Wang &amp; Chen, 2025; Belikova et al., 2026; Song et al., 2026）。</td><td>可复用工作流或工具技能：“搜索 → 阅读 → 提取 → 引用”，或“用 sanitizer 调试”，作为例程被调用。</td></tr></table>

尽管在当前 LLM agent 研究中得到的显式处理有限，但随着 agent 被部署到多模态、具身与机器人环境中，sensory memory 很可能日益重要。在此类环境中，agent 必须在实时与内存约束下处理持续、高带宽的感知流，例如视频帧、音频信号与本体感觉（Black et al., 2025; Bjorck et al., 2025; Mon-Williams et al., 2025）。在这些具身应用中，sensory memory 常通过感觉级缓冲与门控机制实例化，例如短时 perceptual embedding 缓冲、注意力驱动的过滤与 temporal integration，而非被明确标注为认知模块。这些设计减少冗余计算、稳定部分可观测环境，并支持从原始感觉输入到 working memory 与 episodic memory 的原则性整合。因此，对 sensory memory 更显式的建模可能成为可扩展具身与机器人 foundation agent 的关键设计考量。

## 3.2.2 Working Memory

## Working Memory

working memory 指一种短期 memory mechanism，支持对推理、理解与学习等复杂任务所需信息的临时存储与主动操作，使信息能够在持续操作期间被主动保持。

在基于 LLM 的 agent 设置中，working memory（Baddeley, 2020）的核心目标是在严格的在线容量约束下维持并操作任务相关状态，使多步推理与行动能够不中断地进行。由于 LLM 本质上无状态，working memory 提供了在交互步骤之间显式携带与更新此类状态的机制。除了充当被动缓冲，工作 memory management 本身日益被视为 agent 的一种自适应能力：近期的 agent 不再仅依赖手工设计的截断或总结启发式，而是从自身交互经验中学习如何策展进入并留在活动 context 中的内容，使 working memory 成为 agent self-evolving 的直接对象（Gao et al., 2025a）。

foundation agent 中的 working memory 最常见地通过活动 context 实例化，包括 prompt context、中间推理轨迹、工具输出，以及推理期间可访问的 KV cache 等运行时状态。在这一实例化中，现有方法在干预执行的位置上有所不同。一类工作关注任务相关状态在写入活动 context 之前或写入之时如何被表示。通过 compression（Kang et al., 2025c; Wu et al., 2025d）、重构（Sun et al., 2025b; Ye et al., 2025b）或抽象交互历史（Labate et al., 2025），这些方法旨在从源头延迟或避免 context 饱和。具体而言，Labate et al. (2025) 用轻量引用替代大型中间输出，而 Kang et al. (2025c); Wu et al. (2025d); Sun et al. (2025b); Ye et al. (2025b) 则定期总结或折叠已完成的推理片段，以维持紧凑的工作 context。第二类工作在状态已经积累之后处理该问题。这些方法研究在执行过程中，如何在固定的在线预算下持续维持、更新或驱逐任务相关状态。在系统层面，运行时机制管理 KV cache 与调度等状态（Kim et al., 2025b; Liu et al., 2025j; Kwon et al., 2023; Ni et al., 2025）。在 agent 层面，越来越多的工作超越固定启发式，转向 self-evolving 的工作 memory management：其中策展策略本身从 agent 自身经验中学得，agent 通常通过 RL 端到端训练，以决定保留、整合或丢弃什么，并将其作为推理回路不可分割的一部分（Zhang et al., 2025p; Yuan et al., 2025a; Zhou et al., 2025c; Yu et al., 2025b）。一个互补方向将工作 context 本身视为可跨任务改进的可演化 substrate：或是通过将执行经验持续经 distillation 形成结构化、可复用的 context（Zhang et al., 2025j; Suzgun et al., 2025），或是通过向 agent 暴露运行时 memory 状态，使其能够在执行期间自主归档并恢复自身 context（Xu et al., 2026）。

总之，foundation agent 中的 working memory 充当 agent 的在线工作区，通过活动 context 在严格容量约束下实现。现有工作表明，维持连贯的 long-horizon 推理并不取决于把 context window 变得更长当作唯一解法，而取决于在执行期间选择性保留与操作任务相关状态。这一转变将 working memory 从被动的 context 缓冲重新定义为自我管理的工作区：与 agent memory 从静态、预定义机制向自适应、self-evolving 设计的更广泛演进相呼应，支配 working memory 的策略日益从 agent 自身经验中学得与精炼，而非预先固定。working memory 进一步充当这一 self-evolving 回路的门户，因为短期状态必须先经过它，才能被整合进 episodic、semantic 或 procedural memory，而在此阶段进行的选择与抽象决定了 agent 之后能从哪些经验中学习（第 5 节）。随着 agent 扩展到更长的时程与更复杂的交互设置，working memory 的进展将取决于有原则且日益 self-evolving 的状态选择与变换，而非无界的 context 扩展。

## 3.2.3 Episodic Memory

## Episodic Memory


episodic memory 指一种 long-term memory 形式，专用于跨 session 持久存储 agent 的交互经验。它记录定位于特定时间与环境 context 中的具体事件，通常组织为交互轨迹、动作序列与相关反馈。

episodic memory 在 foundation agent 中的主要作用是在较长时间范围内保留历史交互 context 与结果，使 agent 能够在与当前交互或决策相关时引用过往经验（Tulving, 1983; 2002）。通过维持对具体过往经验的访问，episodic memory 在动态环境中支持背景重建与跨 session 连续性。这使 agent 能够将其行为锚定在先前观察到的情况上，在重复交互中保持一致性，并恢复那些否则会在 session 之间丢失的相关 context。

foundation agent 中的 episodic memory 最常实例化为一个显式经验库，它跨 session 积累交互历史，并可在需要时被 agent 访问。从方法论角度，现有 foundation agentepisodic memory 工作按其首要关注点可分为两条主导研究路线。一类工作聚焦于 episodic record，即跨 session 的历史交互如何被组织为连贯的 episodic record，以保留事件结构与情境 context。对于跨 session 交互历史，Rajesh et al. (2025) 强调选择性 episodic write 与过往交互的结构化组织，使“存储什么”与“如何组织 episode 内容”变得显式。对于长视频理解，Yeo et al. (2025a) 通过将事件与其时间和因果关系一起组织来构建 episodic record，从而实现长时视觉经验的连贯 episode-level 表示。更广泛地，Yeo et al. (2025b) 在多个时间尺度上表示 episodic event，使 episode formation 与访问能够适应不同粒度。Anokhin et al. (2024) 将 episodic observation 与语义锚点连接起来，使规划期间能够进行 episodic recall。第二类工作聚焦于 retrieval 与反思，即已存储的 episode 在决策时如何被触发、选择与利用。Yeo et al. (2025b) 将 episode retrieval 表述为一个自适应过程，它以查询与 retrieval 历史为条件，迭代地选择 memory 来源与时间尺度。Latimer et al. (2025) 定义了显式回忆与反思操作，根据 episode 与当前推理 context 的相关性检索 episode，并用其指导后续行为。在工具使用设置中，Li et al. (2025f) 通过将当前执行状态与从过往轨迹归纳出的结构化表示进行匹配来检索 episode 经验。对于 multi-session 对话，Sarin et al. (2025) 使用 session 级 context 与用户状态线索触发 episode retrieval，以跨 session 回忆相关的 episodic summary。最后，Alqithami (2025) 表明，固定 memory 预算下的保留策略直接决定了哪些 episode 在 long-horizon 中仍可被 retrieval。

总体而言，foundation agent 中的 episodic memory 研究集中于跨 session 保留具体交互经验，并在决策时实现对这些经验的选择性访问。现有工作主要处理两个方法论问题：episodic record 与 episode retrieval 或反思。从 self-evolving 视角看，episodic memory 进一步充当 agent 能力生长的经验 substrate：积累的 episode 不仅被 retrieval 以指导单个决策，还通过反思与 consolidation 被经 distillation 形成语义事实与程序技能，使 agent 能够从自身执行历史中持续改进（Yang et al., 2025a; Liu et al., 2025b; Ouyang et al.,

2025）。开放问题包括 agent 应如何定义 episode boundary、如何调控推理期间 episodic recall 的影响，以及随着 episodic memory 规模扩大如何管理长期保留。

## 3.2.4 Semantic Memory

## Semantic Memory

semantic memory 指一种 long-term memory 形式，专用于存储抽象事实、一般概念与结构化知识。它为 agent 提供去语境化的信息，这些信息随时间保持稳定，并可跨不同情境与目标复用。

在 foundation agent 架构中，semantic memory 充当稳定的知识库，支持 knowing-what 的事实性推理（Tulving, 1972）。其内容通常通过对 episodic memory 中积累的反复出现事实进行 distillation 与去语境化而获得。当 agent 在多个任务中遇到相似的知识模式时，来自单个经验的碎片化事实信息会通过总结机制被整合为通用概念、实体关系或属性摘要。这一语义化过程赋予 agent 一种类似于百科全书或技术手册的知识 substrate。通过使 agent 能够直接访问经核实的概念知识，而非重复 retrieval 原始交互日志，semantic memory 为复杂推理与决策提供了连贯且可靠的事实基础。重要的是，在 long-horizon agent 设置中，semantic memory 并非静态，而是随着新信息积累而持续经历访问、修订与控制。

现有 semantic memory 方法主要差异在于抽象知识如何被构建与稳定化，以及当 agent 在 long-horizon 上推理时，知识如何被选择、验证与维护。一类工作聚焦于知识归纳与组织，研究稳定的、去语境化的知识如何从交互、文档或外部证据中被 distillation 出来，并以 agent 可可靠复用的形式存储。代表性方法使用层次化模式（Zhao et al., 2025a; Jia et al., 2025a）、memory 图（Rasmussen et al., 2025; Wang et al., 2024n）或以条目为中心的语义结构（Xu et al., 2025e; Li et al., 2025d）来组织语义知识，支持长期维护与推理期间的结构化访问。其他方法将语义知识编码进神经 memory module（Behrouz et al., 2024; Wang et al., 2024l）或辅助参数（Wang et al., 2025p; Pouransari et al., 2025），强调紧凑表示与快速复用，而不依赖显式外部结构。第二类工作聚焦于当新证据积累时，语义知识在 agent 推理期间如何被激活、验证与更新。代表性方法将语义访问视为决策时的控制过程：抽象知识被选择性挑选、检查适用性，并应用于当前推理状态，而非通过固定的相似度查找来 retrieval（Jimenez Gutierrez et al., 2024; Wang et al., 2025m; Rezazadeh et al., 2025b; Yan et al., 2025b）。其他工作通过引入偏好漂移检测（Sun et al., 2025a）、保留或 forgetting 策略（Alqithami, 2025）以及持续知识编辑（Wang et al., 2024f）等机制来强调长期语义可靠性，以防止过时或不一致的知识降低 agent 行为质量。

总之，semantic memory 通过提供稳定但可修订的知识 substrate，补充了 working memory 与 episodic memory。它作为将碎片化经验经 distillation 形成稳定、可复用规律与事实的主要场所。通过从具体 episode 中剥离出通用知识本体，它为 agent 提供了跨领域任务所需的常识基础。随着研究推进，semantic memory 正从简单的文档存储演化为 self-evolving 的语义网络，确保 agent 在长期运行中维持准确且一致的知识体系。

## 3.2.5 Procedural Memory

## Procedural Memory

procedural memory 指一种 long-term memory 形式，专用于“如何执行任务”。它编码面向特定场景的操作技能、执行策略与自动化例程。与存储事实性知识的 memory 不同，它将复杂动作序列抽象为可复用模式，使 agent 能够高效且连贯地完成任务。

在 foundation agent 架构中，procedural memory 通常体现在执行层，其中重复的动作序列、决策规则或工作流塑造高层决策的执行方式。此类知识并非绑定于单一 memory substrate，它可以从先前执行中 distillation、通过优化学习，或在 agent 之间共享。随着执行经验积累，短时动作状态可被整合为可复用的技能或例程，使 agent 在较长交互时程中更一致地执行任务（Fang et al., 2025b）。

procedural memory 的实例化呈现出从显式非参数模板到隐式 parametric 神经策略的演化，其机制多样。经验 distillation 与元认知控制涉及将历史轨迹转化为可复用方案；例如，From Experience to Strategy 将交互经 distillation 形成结构化策略（Xia et al., 2025），而 Adapting Like Humans 聚焦于测试时纠错的元认知例程（Li et al., 2025h）。学习优化与策略精炼强调将技能内化到 parametric 权重中；例如，Retroformer 采用策略梯度优化来精炼 agent 动作（Yao et al., 2024），BREW 通过持续训练与精炼增强任务处理能力（Kirtania et al., 2025）。multi-agent 协调与共享实践在协作环境中建立共同操作规范，Smarter Together、MetaGPT 与 MIRIX 对此进行了探索（Tablan et al., 2025; Hong et al., 2024; Wang & Chen, 2025）。工作流外化与自动化将复杂操作转化为显式自动化模板，Agent Workflow Memory 与 LEGOMem 即为示例（Wang et al., 2025v; Han et al., 2025）。此外，MemGen 与 ReasoningBank 等工作中的 self-evolving 机制促进推理轨迹的积累，以支持长期程序演化（Zhang et al., 2025d; Ouyang et al., 2025），而 CoEvoSkills 让技能生成器与代理验证器共同演化，使技能包无需访问真实测试即可被精炼（Zhang et al., 2026a）。最后，尽管 Evaluating Long-Term Memory 等工作表明评估日益受到关注（Terranova et al., 2025），程序 memory evaluation 正开始围绕专门 benchmark 走向标准化，这些 benchmark 既衡量程序知识的任务级效用，也衡量其跨任务、角色与模型的迁移（Li et al., 2026; Belikova et al., 2026）。

近期一项显著发展将 procedural memory 重新定义为显式、可共享的技能。Voyager 等早期技能库表明，agent 可以积累经过验证的可复用程序，形成不断增长的行为库（Wang et al., 2025c）；这一思想此后成熟为更广泛的生态：技能被打包为指令、代码与资源的可组合束，由 agent 按需加载（Anthropic, 2025; Xu & Yan, 2026; Wang et al., 2025u）。这种外化将 procedural memory 从私有的 agent 状态转变为可移植、人类可读且可版本化的基础设施，可被检查、共享并跨 agent 与模型复用。从 self-evolving 视角看，技能库本身随后成为演化对象：agent 通过迭代的诊断—修订循环，从自身执行轨迹中修订技能（Belikova et al., 2026），通过合并、修复或退役技能来自主维护库的健康，以控制积累的技能级技术债（Song et al., 2026），并学习在 long-horizon 中应归纳与演化哪些 memory 技能（Zhang et al., 2026b）。有两点保留意见使这一趋势有所降温。经验上，自生成技能仍不如人工策展的技能，这表明完全自主的技能归纳对 self-evolving agent 仍是一个开放挑战（Li et al., 2026）；而且，随着技能作为共享产物流通，它们引入了新的安全与治理风险，相当一部分社区贡献的技能被发现含有漏洞（Liu et al., 2026）。

总之，procedural memory 通过提供可复用的动作抽象，补充了 semantic memory 与 episodic memory。它目前正经历一次关键转变：从显式非参数指令 retrieval 转向隐式 parametric 神经策略。这一演化不仅支持技能获取，也确保在 long-horizon 自主 agent 中稳定且高效地实现复杂决策。与此同时，agent 技能生态的迅速崛起凸显出一个互补的反向趋势：程序知识被外化为显式、可移植且可共享的产物；使 agent 能够自主归纳、演化并安全治理此类技能，而非依赖人工策展，仍是 self-evolving agent 的核心挑战。

![](../assets/arxiv-2602.06052-fig5.jpg)  
图 5：memory cognitive mechanism 与 memory subject 之间的联系。该图以网格组织：列对应五种 cognitive mechanism（§3.2）——sensory、working、semantic、episodic 与 procedural，两行对应 agent-centric（上；§3.3.2）与 user-centric（下；§3.3.1）的 memory subject。每个点代表一篇论文，沿横轴按发表时间（2023 至 2025 年）定位。聚类面积与每个单元格中的论文数量成正比。

## 3.3 Memory Subjects

从 self-evolving 与 long-horizon 视角看，memory subject 刻画 memory 主要建模并服务谁。该维度与 memory substrate 和 cognitive mechanism 正交，对于理解 foundation agent 中 memory 的优化目标至关重要。图 5 展示了这种 subject 级区分如何与认知 memory mechanism 相联系。working memory、procedural memory 与 sensory memory 主要面向 agent，反映它们在支持许多真实世界下游任务中的角色。semantic memory 与 episodic memory 则同时出现在 user-centric 与 agent-centric 的设置中。对用户而言，它们编码纵向交互历史与演化中的偏好；而在 agent-centric 的 memory 中，它们支持世界建模、long-horizon 任务执行与持续经验积累。总体来看，我们或许会发现 memory subject 与认知类别相互交织，为组织 memory 研究提供了超越以往综述中单一分类（Zhang et al., 2025q; Du et al., 2025）的互补视角。我们注意到，user-centric 的 memory 与 agent-centric 的 memory 是概念取向，而非互斥类别。在实践中，单个系统可以在维护可复用任务策略的同时维护用户特定偏好。例如，编码助手可以同时维护 user-centric 的用户特定编码风格偏好与 agent-centric 的跨用户可复用调试策略。MemSkill（Zhang et al., 2026b）等近期工作在两种取向上评估 memory。然而，当前 benchmark 很少同时要求两者，这自然导致现有研究强调其中之一。

## 3.3.1 User-Centric Memory

## User-Centric Memory

user-centric 的 memory 指对用户特定事实与偏好的抽象，包括生平数据、历史交互与已表达偏好，这些内容可跨 session 与跨领域演化，以与用户对齐并实现连贯交互与助手任务执行。

user-centric 的 memory 构成 LLM agent 执行用户相关任务的基础组件，尤其是长期个性化（Liu et al., 2025e; Chen et al., 2024b; Zhang et al., 2025o）。除了仅告知临时任务执行状态的通用指令 prompt 之外，user-centric 的 memory 通过将 agent 的行动与响应锚定在用户身份以及短期交互与长期历史中不断演化的 context 上，为其提供支撑（Tan et al., 2025c）。该组件在包括但不限于咨询（Litam et al., 2021）、推荐（Chen et al., 2018; Zhang et al., 2025m; Shao et al., 2026）与个人医疗保健（Velliangiri et al., 2022; Zhang et al., 2026c）等领域尤为关键，在这些领域中，agent 必须同时对用户不断演化的偏好、意图与行为特征表现出即时与纵向的感知。下面，我们并不强加严格分类，而是强调准确且持久的 user-centric 的 memory 所服务的关键目标，使 agent 能够在长交互时程中持续精炼对用户的理解并维持个性化对齐。

**long-horizon 对话中的 memory management。** 对话系统是用户—agent 交互最流行的真实世界应用场景之一（Chen et al., 2017; Xu et al., 2025e）。在 LLM 有限的 context window 内，现有对话系统通常只能在有限的 session context 中处理多轮对话（Li et al., 2025a）。将先前对话中的所有细节 prompt 给 LLM agent 在计算上不可行，且常因噪声累积与话题漂移而适得其反。因此，有效的用户 memory 需要针对相关对话 context 的 retrieval（Maharana et al., 2024）、更新（Xu et al., 2025e）、总结（Chhikara et al., 2025; Salama et al., 2025）与 forgetting（Zhong et al., 2024）的原则性机制。MemGPT（Packer et al., 2023）等近期真实世界 memory system 显式形式化了 memory 层级，以管理长期对话状态。与此同时，OpenAI 的 ChatGPT memory 功能实现了一种持久 memory mechanism，保留用户相关细节，同时让用户对存储或 forgetting 什么拥有显式控制（OpenAI, 2025）。这些发展说明了对话 memory management 中的一个核心挑战：确定在 long-horizon 用户—agent 交互中积累的哪些信息应被保留、更新或 forgetting，以支持未来对话。此类信息可能包括持久偏好、演化中的目标、重大生活事件与敏感约束。因此，memory management 不仅是保存过往对话，而是一个持续过程，agent 通过该过程随时间维持对用户的连贯但可适应的表示。

**持久用户模拟。** 高保真用户模拟器对真实的交互式在线平台至关重要，因为它们提供可扩展、可复现且受控的训练与评估环境，而无需访问大量真实用户数据，从而尊重隐私并降低与实时用户研究和在线 A/B 测试相关的成本（Park et al., 2023; Zhu et al., 2024; Samuel et al., 2024; Zhang et al., 2025s）。在推荐系统（Zhu et al., 2025a）与社交网络（Gao et al., 2023）等在线数字平台中，模拟器帮助近似长期用户行为与偏好，使策略优化、排序策略与干预影响的评估能够在动态条件下进行，而非依赖静态测试集（Jin et al., 2013; Zhang et al., 2025k）。在此类场景中，user-centric 的 memory 同时支持纵向一致性与细粒度偏好演化，因为模拟器需要在扩展时程上维护个性化画像与自适应交互模式。memory augmentation 的模拟器不应复现固定人设，而应建模用户状态、偏好与行为如何随积累的经验和 agent 干预而演化。

**长期个性化。** 与主要面向群体或平台级收益的用户模拟、以及主要捕捉用户—agent 对话 context 中已表达偏好的对话系统（Zhang et al., 2025n）不同，长期个性化聚焦于在跨越数天、数月甚至数年的扩展时程上优化特定用户的体验。通过跨 session 维护显式用户画像或持久个人知识库（Zhang et al., 2026d），agent 可以调整语言风格、决策与行为，以随时间持续支持同一用户的需求与偏好。重要的是，这种个性化不应将用户画像视为静态记录。相反，agent 必须持续将历史证据与新观察到的交互相协调，区分持久偏好与临时状态，并在用户目标或行为变化时修订 memory。这一过程实现 self-evolving 的偏好对齐，agent 在保持纵向连贯性的同时逐步调整其理解与行为。长期个性化的早期工作（Salemi et al., 2024）通过 episodic memory construction 生成 context 相关的响应。后续研究（Tan et al., 2024a）进一步探索将个人 memory 编码进参数高效模块，例如基于 LoRA 的参数（Hu et al., 2022）。然而，这些方法要么难以充分利用丰富的个人用户数据，要么产生可观的计算开销。因此，较新的框架强调高效 memory mechanism，能够将新观察到的行为与现有 memory structure 相协调以实现个性化对齐（Cai et al., 2025; Zhang et al., 2025o）。这一方向将个性化从一次性画像构建转向贯穿用户—agent 关系的持续、memory 驱动的适应。

**隐私保护 memory。** 持久用户 memory 在隐私、安全与数据治理方面提出了大量要求，因为敏感属性可能通过 memory augmentation agent 的训练时 memorization 与推理时 context 泄漏而被存储、retrieval 并意外暴露（Mireshghallah & Li, 2025）。近期工作已系统性地证明，LLM agent 中的 memory module 易受定向提取攻击（Wang et al., 2025a），在黑盒威胁模型下，人们可以轻松恢复存储在 agent memory 中的私有用户数据。在 multi-agent 设置中，异构 agent 角色与动态协作进一步加剧隐私风险，这使在交互 memory store 之间执行一致的隐私协议变得复杂（Shi et al., 2025b）。对 self-evolving agent 而言，这些风险尤为重要，因为持续个性化要求 memory 在长期运行交互中被反复 retrieval、更新、整合并可能共享。为确保安全部署，agent 必须支持选择性 memory 保留、安全存储、用户控制的删除，以及对记住或 forgetting 何种信息进行透明审计。它们还应让用户对如何推断与更新其演化画像拥有控制权，而非仅允许控制单个存储记录。在实践中，这些保障措施常与差分隐私机制（尤其是在个性化或联邦式适应中）、通过私有向量数据库的加密存储与 retrieval，以及显式保留或访问控制策略相结合，以降低来自存储内容与 embedding 两方面的泄漏风险（Tran et al., 2025; Shi et al., 2025b）。

## 3.3.2 Agent-Centric Memory

## Agent-Centric Memory

agent-centric 的 memory 指 agent 通过自身任务执行历史或环境交互所积累的 distillation 知识、技能与操作性任务先验。它支持跨真实世界环境的 long-context、long-horizon 与长运行任务。

与主要保留关于相应用户的个性化信息的 user-centric 的 memory 不同，agent-centric 的 memory 编码从 agent 自身解决并交互真实世界任务的历史中得出的更通用教训与经验（Luo et al., 2025; Shinn et al., 2023; Wang et al., 2025c; Zhang et al., 2025i）。该 memory 捕捉普遍适用的教训，而不绑定于任何单一用户。本质上，它表示 agent 如何“从经验与环境学习”，保留通过先前经验获得的重要事实、策略与世界知识，以提升未来表现（Wei et al., 2025e;d; Zhang et al., 2025i）。与优化特定用户满意度的 user-centric 的 memory 不同，agent-centric 的 memory 处理更广泛真实世界问题，其中经验与解决方案预期可在不同任务、环境或用户之间保持有用。这对 long-horizon 自主性至关重要：处理复杂多步任务或终身学习（Zheng et al., 2025c;b）的 agent 必须能够记住并基于先前遇到的内容继续构建。除了保留经验，agent-centric 的 memory 还为 self-evolving 提供基础：agent 可以将成功与失败的轨迹经 distillation 形成领域知识、操作策略与可执行技能；通过后续交互精炼它们；

并将可复用的抽象迁移到此前未见过的任务。下面，我们概述需要 agent-centric memory 方法的关键动机与场景。

**long-horizon 任务执行。** LLM agent 经常参与需要数百或数千个推理与动作步骤的任务，例如编码（Jimenez et al., 2024）、网页导航（Zhang et al., 2025l; Zhou et al., 2024）、复杂多轮决策（Shani et al., 2024）或顺序工具使用（Qin et al., 2024）。在这些设置中，即时 working memory 很容易被累积的观察与中间推理淹没。agent-centric 的 memory 提供一种外化机制，用于存储与 retrieval 关键中间状态，使 agent 能够在原生 context window 之外运行。此类 memory 通过保留子目标、动作结果、环境状态、未解决的失败以及时间上相隔较远步骤之间的依赖关系，直接支持进行中任务的执行。因此，它使 agent 能够恢复被中断的工作流、修订较早的决策，并在长运行交互中保持连贯进展。例如，MEM1（Zhou et al., 2025c）引入端到端 RL 框架，维护紧凑内部状态，使 agent 能够整合相关信息并丢弃冗余 context，从而在任意长的多轮交互中以接近恒定的内存使用运行。作为对 MEM1 的补充，MemAgent（Yu et al., 2025b）提出一种面向长文本处理的基于 RL 的 memory agent。它分块读取长输入，并使用固定长度、可覆写的 memory 进行增量更新。这一设计使 LLM agent 能够以线性复杂度扩展到极 long-context，且性能退化最小。较新的方法包括层次化 memory module（Hu et al., 2025b）、context 折叠方案（Sun et al., 2025b）与学得的 memory 控制器（Zhang et al., 2025p），后者决定存储什么以及何时压缩或丢弃过时信息。总体而言，这些方法将 memory 从被动 context 保留扩展到主动状态管理，以支持持续 agent 执行。

**领域特定的长尾解决方案迭代。** 许多真实世界问题呈现长尾现象（Zhang et al., 2021; Kandpal et al., 2023; Park & Tuzhilin, 2008），即罕见但重要的模式、错误案例或领域特定启发式在训练数据中不常出现。agent-centric 的经验 memory 支持保留这些罕见洞见与知识，使 agent 在未来出现相似或相关案例时能够高效复用（Li et al., 2024a）。通过在领域内反复交互，agent 可以逐步将一次性解决方案整合为领域特定知识，并根据观察到的成功、失败与环境反馈精炼策略。这实现了超越预训练期间最初获得的知识与行为的 self-evolving。例如，在软件调试中（Jimenez et al., 2024），大多数错误遵循常见模式，但真实世界系统常因高度特定的配置问题、依赖冲突或环境相关缺陷而失败。类似地，在科学研究中（Ghafarollahi & Buehler, 2025），虽然通用推理模式与实验流程往往在同一学科内共享，但许多子领域特定的实验设置（例如无线通信中的专用信道编码配置）或高度依赖领域的故障排查实践（例如考古学中的领域特定协议）很少在不同研究者之间遇到，因此不太可能在预训练数据中得到充分表示。类似的长尾动态也出现在复杂信息搜索（Wei et al., 2025a）与专业工作流自动化（Zhang et al., 2025g）中，agent 必须处理范围狭窄、依赖 context 的问题，而存储定制的一次性解决方案并随时间重复应用会带来收益（Yang et al., 2025a）。随着这些经验积累，memory 使 agent 能够更新领域特定启发式、纠正无效策略，并在长操作时程中发展日益专门化的能力。

**跨任务技能泛化。** long-term memory 使 agent 能够跨任务与 episode 积累持久知识，支持无灾难性 forgetting 的持续改进（Hatalis et al., 2023）。在高层面上，跨任务技能泛化关注 agent 如何从多样交互轨迹中抽象并保留可复用知识与技能，从而实现跨异构任务、领域与环境的泛化，而非仅改进单一设置或环境内的执行。例如，Agent KB（Tang et al., 2025b）构建跨领域经验框架，将从异构 agent 轨迹中 distillation 的高层策略与执行教训聚合到共享知识库，使 agent 在面对跨不同领域的新任务时能够 retrieval 并复用可迁移的问题求解知识。与特定轨迹回放不同，跨任务 memory 的目标是将交互经验经 distillation 形成任务无关的抽象与可复用技能原语，使其跨环境与目标泛化。另一个代表性例子是 ReAct（Yao et al., 2023）中跨 WebShop（Yao et al., 2022）与 ALFWorld（Shridhar et al., 2021）使用的动作—思维模式。此类抽象还包括可复用的工具使用模式，例如 Toolformer（Schick et al., 2023）与 ToolLLM（Qin et al., 2024）中稳定的工具使用策略，以及通过反复失败积累的避错执行启发式（Shinn et al., 2023）。agent 不必 memory 完整解决方案，而可以识别反复出现的子问题、提取不变的动作模式，并重组先前学到的技能以解决新任务。这使 LLM agent 能够逐步演化为更有能力、更高效的问题求解者，表现出类似人类在多样任务中随时间发展专长的行为。

**持续策略与技能演化。** 作为跨任务泛化的补充，持续策略与技能演化关注以环境为根基的 procedural memory 如何通过反复执行被创建、精炼、组合与维护。这些 memory 编码在特定交互体制（例如网页界面、GUI 系统或物理环境）内如何高效执行多步动作。例如，WebArena（Zhou et al., 2024）等环境中的网页 agent（Wei et al., 2025e）学会复用与精炼成功的多步浏览策略，而非从头重新探索界面。对 GUI agent 而言，此类程序 memory storage 界面特定的动作序列，包括在桌面或移动环境约束下的菜单遍历、控件操作与错误恢复策略（Qin et al., 2025; Wang et al., 2025e）。在具身 agent 中，procedural memory 表现为遵循物理动力学与动作前置条件的可执行技能与控制策略（Fung et al., 2025; Yang et al., 2025c）。这些存储的经验可作为模板、示范或先验被复用以更高效地解决任务。然而，self-evolving agent 必须超越单纯存储成功轨迹：它们需要从经验中归纳技能、评估其有效性、在环境变化时更新它们、在不同抽象层级分解或组合它们，并移除过时或冲突的技能。因此，基于 memory 的技能学习使 agent 能够在反复 episode 中精炼有效行为，并在动作—结果规律层面内化世界模型。随着时间推移，由此产生的技能库充当不断演化的程序 substrate，既支持在熟悉领域内日益高效的执行，也支持对新任务的自适应泛化。这一能力是 long-horizon 自主性的核心，并构成终身学习（Zheng et al., 2025c）与长运行 agent（Yang et al., 2025a）新兴研究的基础。

## 4 Memory Operation Mechanism


除了 memory 如何被表示以及它扮演何种认知角色，memory system 还由作用于其上的操作来定义。图 6 总结了 single-agent 与 multi-agent 设置中的这些操作。第 4.1 节涵盖 single-agent 的五项核心操作，第 4.2 节将它们扩展到多 agent system——在那里，架构、路由与隔离支配经验如何在 agent 之间共享并保持一致性。

## 4.1 Single-Agent Systems 的 Memory Operations

在单 agent system 中，memory operation mechanism 定义 foundation agent 在 long-horizon 交互与任务执行中如何主动构建、更新、控制与利用 memory。现代 agent 不把 memory 当作静态仓库，而是通过一系列操作来操纵 memory，包括索引、retrieval、更新、compression、总结、forgetting 与修剪。除了管理信息，self-evolving agent 还进一步整合交互轨迹、反思执行结果，并将反复出现的经验经 distillation 形成可复用知识、策略与技能。这些操作共同调控过往经验如何被纳入进行中的推理与未来决策，构成单 agent memory 系统的操作骨架。它们共同建立一个持续适应回路：agent retrieval 相关经验以指导当前执行，评估由此产生的成功与失败，随后修订其 memory 与技能库。该回路使 agent 能够在长运行任务中维持连贯状态，同时跨任务与交互 episode 逐步改进。

![](../assets/arxiv-2602.06052-fig6.jpg)  
图 6：foundation agent memory 系统的操作机制。该图展示了 foundation agent memory 系统的完整操作机制。对单 agent system，它定义了五项核心操作：存储与索引、加载与 retrieval、更新与刷新、Compression 与 Summarization、forgetting 与 retention，这些操作支配历史信息如何被保存与访问以支持下游工作。对多 agent system，该框架进一步通过 memory architecture 定义、路由协议以及隔离与冲突解决策略来应对协调挑战，确保分布式 agent 之间的数据一致性与高效协作。

## 4.1.1 Storage 与 Index

随着 agent memory 随时间增长，信息如何存储与组织对于确保相关信息在需要时能被高效且可靠地 retrieval 变得至关重要。在单 agent system 中，memory 通常在写入时建立索引，将每个条目与 semantic embedding 及辅助元数据（如时间戳、任务标识符、实体或工具使用）关联（Lewis et al., 2020; Zhang et al., 2023a; Rezazadeh et al., 2025b）。基于向量的存储仍是非参数 agent memory 的主导范式，使 retrieval-augmented agent 能够对 episode 或 semantic memory 进行高效的近似最近邻搜索（Guu et al., 2020; Quinn et al., 2025）。除扁平 vector index 之外，agent 日益采用 structured storage 格式，包括关系表、基于图的 memory 与层次化树表示，从而实现与任务结构对齐的关系查询、多级抽象与模式感知访问（Anokhin et al., 2024; Sarthi et al., 2024; Rezazadeh et al., 2025b）。同时，一些系统维护 text record 型 memory，存储显式、人类可读的摘要与时间顺序日志，依赖关键词匹配或轻量字符串 retrieval 以优先保证透明性与可控性（Park et al., 2023; Zhang et al., 2025q）。最后，存储并不限于外部 memory module：embedding 模型权重的 parametric memory、context window 中的瞬态 working memory，以及 KV cache 等推理时内部状态，共同充当隐式存储 substrate，影响 retrieval 行为与推理动态（Mallen et al., 2023; Kwon et al., 2023; Pope et al., 2023）。随着 memory 在更 long-horizon 上扩展，存储格式与索引策略的选择会直接影响 retrieval 精度、计算开销与下游推理可靠性。

## 4.1.2 Loading 与 Retrieval

为了在进行中的推理与决策中利用存储的经验，agent 依赖 retrieval 任务相关 memory，同时限制无关或过时信息的影响。在单 agent system 中，该过程通常始于轻量加载操作：根据近来性、任务范围或 memory 类型等元数据过滤或预选 memory entry，随后对向量化表示进行基于相似度的 retrieval（Lewis et al., 2020; Mallen et al., 2023; Zhang et al., 2025q）。加载后的 memory 随后通过语义相似度、启发式约束或预算感知的选择策略进行排序或精炼，再注入模型的 prompt 或工作 context，形成 external memory 与 LLM 推理过程之间的主要接口（Park et al., 2023; Wang et al., 2025q）。先前研究表明，retrieval 质量对 agent 性能有实质性影响。retrieval 过多 memory 可能引入噪声与 context 过载，而过于严格的 retrieval 可能阻止访问关键历史信息（Xu et al., 2025e; Hu et al., 2025c）。因此，有效的加载与 retrieval 机制旨在平衡相关性、多样性与 context 预算，以支持连贯的 long-horizon 行为。

## 4.1.3 Update 与 Refresh

随着 agent 在扩展时程上与环境交互，先前存储的 memory 可能变得不完整、过时或与新观察到的信息不一致，使静态或仅追加式的 memory 表示不再足够。更新机制使 single-agent 能够根据新观察、外部反馈或反思性推理修订现有 memory entry，使 memory content 得以演化，而非仅仅累积。在实践中，更新常在任务完成、评估信号或检测到不一致之后触发，可能涉及重写语义摘要、合并重叠的 episodic record 或调整存储信息的重要性（Park et al., 2023; Tan et al., 2025c; Wang et al., 2023a）。同时，刷新操作聚焦于在不改变核心内容的情况下调整 memory 的相对显著度与可访问性，例如重新排序显著条目、重新生成压缩摘要，或强化频繁访问的 memory 以保持其对未来推理的影响。近期 agent system 进一步表明，反思或自我评估过程可以自主触发更新与刷新动作，从而改善长期连贯性与任务表现（Shinn et al., 2023; Ouyang et al., 2025）。这些机制共同使 memory 表示能够动态演化，支持在非平稳环境中的适应，同时减轻过时或误导性信息的积累。

## 4.1.4 Compression 与 Summarization

long-horizon agent memory 系统需要机制来调控增长，同时保留对未来推理与决策至关重要的信息。Compression 与 Summarization 通过将细粒度 episodic record 转换为更紧凑、更抽象的表示，减少冗余并提升 memory efficiency，从而满足这一需求。在实践中，许多 agent system 定期或在任务完成后执行总结，将交互历史整合为适合长期存储的 semantic memory 或层次化 memory（Wang et al., 2025j; Chen et al., 2025d）。hierarchical consolidation进一步将压缩后的 memory 组织为多级或树状结构表示，实现跨不同抽象层级的可扩展 retrieval（Sarthi et al., 2024; Rezazadeh et al., 2025b）。Dynamic Cheatsheet 进一步实例化了这一思想：维护一个紧凑、任务自适应的摘要，持续更新以仅呈现进行中推理最显著的信息，减少推理时重复的大规模 retrieval 与 context 扩展（Suzgun et al., 2025）。尽管这些机制提升了 context 利用与可扩展性，先前工作强调了抽象保真度与长期回忆之间的内在权衡，使总结策略成为单 agent memory 系统中的关键设计考量（Lee et al., 2024; Wu et al., 2025d）。

## 4.1.5 Forgetting 与 Retention

在 agent system 中，随着任务目标变化与环境变为非平稳，memory 相关性随时间演化，使不加区分的 memory 积累日益与有效的长期推理相错位。forgetting 机制通过显式移除或抑制不再与 agent 进行中目标一致的 memory entry，降低过时或低效用信息的影响，以应对这一挑战。在实践中，forgetting 常通过近来性衰减或重要性阈值等启发式策略实现，也通过显式资源或效率约束下优化 memory 移除的学得策略实现（Alla et al., 2025; Wang et al., 2025q）。相反，保留机制决定哪些 memory 应在扩展交互时程中被保存并优先考虑，确保任务相关知识在 memory 持续增长时仍可访问。近期工作强调自适应保留策略，agent 根据任务 context、反馈信号或长期性能目标动态调整保存优先级，从而在非平稳环境中实现稳健行为（Yan et al., 2025b; Zheng et al., 2025a）。

## 4.2 Multi-Agent Systems 的 Memory Operations

在多 agent system 中，memory operation mechanism 描述若干 agent 在协作期间如何共同构建与复用 memory：每个 agent 可以保有自己的私有 memory，它们也可以通过共享工作区共享经验。与单 agent system 一样，该机制仍包括索引、retrieval、更新、compression、总结、forgetting 与修剪等基本操作。它还可能额外支持将多个 agent 贡献的经验聚合与经 distillation 形成共享知识与技能库，使某个 agent 发现的有用策略惠及其他 agent 或未来协作。除这些基本操作之外，multi-agent 设置中更重要的是跨 agent 读写规则：在每个任务中，系统需要为不同角色的 agent 选择合适的 memory。此类规则不仅决定每个 agent 能访问哪些 memory，还决定角色特定经验、专门技能与执行反馈如何在 agent 之间转移。此外，系统通常需要额外操作来消除冗余、解决冲突并保持 memory 一致。这些操作必须考虑异构 agent 所生成 memory 的来源、可靠性与兼容性，尤其是当它们的观察或学得策略发生冲突时。通过选择性共享、验证、整合与修订，多 agent memory 可以支持集体 self-evolving，同时保留专门能力与连贯的 long-horizon 协作。

## 4.2.1 Memory Architecture

在多 agent system 中，memory 可以按不同方式组织，差异在于它存储在哪一层、跨 agent 的读写权限如何定义，以及系统是否引入控制器。这些设计选择决定路由能否构建高效的 memory 视图，以及是否会产生信息泄漏等系统性问题。

**Private-only.** 在仅私有架构中，每个 agent 拥有独立 memory，其读写权限仅在该 agent 的 memory 内生效。在 multi-agent 协作中，agent 只能依赖自身 memory 与当前任务 context 工作。这种设置提供强隔离，使系统更易于检查。然而，相同 memory 往往在多个私有空间中被重复创建，可能浪费资源。代表性例子包括 RecAgent（Wang et al., 2025h），它为每个用户实例化一个 agent 并保留私有 memory，以避免混合不同用户的历史，从而更好地保护隐私；TradingGPT（Li et al., 2023b）中，每个交易 agent 维护自己的 memory，以遵循一致的风险偏好与板块关注，协作主要通过交换选定观点而非共享完整 memory；MetaAgents（Li et al., 2025j）为每个角色配备关于其过往思考与决策的隔离 memory，使角色保持稳定一致，而从对话中获得的信息则写回本地。

**Shared-workspace.** 与仅私有 memory 不同，共享工作区设计使用一个所有 agent 都可读写的公共池。agent 通过这一共享状态共享中间结果，因而无需大量点对点消息传递，降低了通信成本。然而，共享池可能迅速变得嘈杂，因此需要过滤机制，以及在多个 agent 更新同一信息时避免冲突的协调策略。作为代表性共享工作区设计，MetaGPT（Hong et al., 2024）使用一个简单共享池发布角色 agent 的中间产物，每个 agent 应用其角色画像过滤该池，仅把相关 memory 拉入 context。InteRecAgent（Huang et al., 2025b）通过建立 Candidate Bus 使共享状态更具任务特定性：工具反复读取当前候选集并写回过滤后的候选，使集合逐步收窄，从而避免 prompt 长度溢出。MAICC（Jiang et al., 2025d）进一步将工作区扩展为包含离线数据与在线回放缓冲的共享经验池，agent 用当前子轨迹查询，并 retrieval 前 k 条相似轨迹以在 context 内复用。

**Hybrid.** 这种设置同时保留私有层与共享层。它使用策略决定新信息写入私有空间还是共享空间。每次调用时，它为 agent 构建权限受限的 memory 视图，使 agent 只看到被允许看到的内容。这在最大化 memory reuse 与保持敏感信息隔离之间取得平衡。例如，在 Collaborative Memory（Rezazadeh et al., 2025a）中，系统将所有 memory snippet 分离为私有 memory 与共享 memory。写入时，写策略判断信息是普遍有用还是用户特定，然后将其写入共享层或私有层。读取时，读策略使用系统提供的访问图，为当前调用构建权限受限的 memory 视图。类似地，在 MirrorMind（Zeng et al., 2025）中，每个 Author Agent 维护与其研究兴趣对应的私有 memory，同时通过公共 memory sharing 基础学科知识。这种混合设计构成了一个 AI Scientist 的结构。

**Orchestrated.** 前三类主要在 memory 位于何处以及谁能看到它方面存在差异。相比之下，编排设计引入一个显式控制器，在层次化工作流中协调 agent 并中介 memory 访问。具体而言，控制器分解任务、将子任务分配给角色 agent，并决定每个 agent 能读写什么。这种集中协调非常适合多阶段工作流与强约束设置，但也可能引入瓶颈与额外的系统复杂度。ChatDev（Qian et al., 2024a）通过在预定义 ChatChain（设计、编码、测试）下运行角色 agent 来示例这一模式，其中各阶段输出作为结构化交接，以减少跨阶段 context 过载。MIRIX（Wang & Chen, 2025）同样编排 memory 维护：Meta Memory Manager 将更新/retrieval 路由到专门的 Memory Manager，并将其结果聚合为统一响应。值得注意的是，这一控制层与存储布局正交，可与仅私有、共享工作区或混合 memory storage 组合。例如，MGA（Cheng et al., 2025）将 GUI 交互组织为 observe、plan 与 ground agent 流水线。Planner 充当控制器，而底层 agent 可在共享工作区提交中间状态，由 Planner 选择每一步检索并注入哪些历史。类似地，AgentFlow 也将编排与共享工作区结合：planner 控制所有模块，并将关键中间结果写入共享 memory 以供后续 retrieval（Li et al., 2025l）。

## 4.2.2 Memory Routing

给定一种架构，路由描述一组 memory 分配与访问规则。当新任务到来时，系统需要为不同角色的 agent 构建单独的 memory 视图：它决定应 retrieval 哪些过往 memory，以及如何将它们注入每个 agent 的 context。我们按路由决策作出位置对路由方法分组：中央编排器、单个 agent，或通过 retrieval 与匹配的 memory storage 本身。

**基于编排器的路由。** 这指由中央编排器以统一方式作出路由决策的设置。它维护全局任务状态与协作进度，将复杂目标分解为子任务，然后根据角色与能力将子任务分配给不同工作 agent，同时分发所需 memory 并决定执行顺序。这些决策可随任务状态变化而动态更新。该方法强调集中式全局工作流，但代价是编排器可能成为性能与稳健性的瓶颈，形成单点负载与故障风险。例如，在 LEGOMem（Han et al., 2025）中，编排器维护全局状态、生成下一个子任务、选择 agent 执行它，并用该 agent 的摘要更新状态；memory 也以同样方式调度，任务 memory 注入编排器以供规划，子任务 memory routing 给所选 agent 以供执行。GameGPT（Chen et al., 2023）将焦点转向工作流路由：管理器定义多阶段流水线，并要求每个阶段将关键中间输出写入共享工作区，使后续阶段能够继承与复用它们。最后，Westhäußer et al. (2025) 将编排扩展到 memory 源路由，其中编排器使用 MCP 选择调用哪些 memory 源并注入最相关片段；若注入证据不足，Self-Validator 会请求更多 retrieval 并更新 context，从而实现集中式 memory 控制。

**agent 发起式路由。** 与基于编排器的路由相比，该方法中的路由决策不由中央编排器分配。相反，每个 agent 根据其角色与任务在本地发起路由。信息通常先发布到共享 memory 池，然后 agent 使用约束机制选择所需 memory，形成自己的 memory 视图。该方法通常更灵活，但也更依赖良好的过滤设计，以避免共享池中的噪声、冲突或遗漏重要信息。在 SRMT（Sagirova et al., 2025）中，每个 agent 保有个人 memory 向量，并在本地决定从共享 memory read 多少：每一步它在自身 memory 上使用交叉注意力，从共享 memory 序列中选择，并更新个人 memory。S<sup>3</sup>（Gao et al., 2023）走更显式的过滤路线，将共享 memory 视为平台级消息流，根据 forgetting、相关性与来源可信度等因素对条目评分，仅保留一小部分作为 agent 自身的 memory 视图。在 Talker-Reasoner 设置（Christakopoulou et al., 2024）中，共享存储（mem）由 Reasoner 写入、由 Talker 读取，Talker 可以选择读取什么，或在回复前等待最新更新，这表明 agent 可以决定何时从 memory read。

**memory 驱动式路由。** 与前两种不同，这里的路由主要由从 memory storage 中的 retrieval 完成。系统将当前任务表示为查询，然后在 memory storage 中执行“retrieval、评分与重排序、选择”，以获取最相关的 memory 子集并注入 context。有时它还可以利用 memory 之间的结构化链接（如图扩展），将 retrieval 结果扩展为更完整的经验片段集合。作为 memory 驱动路由的一种典型形式，G-Memory（Zhang et al., 2025c）将 multi-agent 历史组织为层次化图，为新任务检索相关节点，通过邻域链接扩展它们，并将结果压缩为核心子图，再修剪为角色特定的 memory 视图。CRMWeaver（Lai et al., 2025）则在可复用指南层面路由：它从过往成功轨迹中 retrieval 最相关的工作流指南并注入当前 context，并在不存在匹配时写回新指南。最后，在 Spark（Tablan et al., 2025）中，每个编码问题被当作查询，retrieval agent 分析意图，并从共享存储中选择最相关的文档与过往经验轨迹。

## 4.2.3 Memory Isolation 与 Conflicts

在 multi-agent 架构与 memory routing 的基础上，memory isolation 非常重要，因为 memory 由多个 agent 读写，而非在单一、顺序回路中更新。多个 agent 可能并行产生结论，且其可访问资源与权限常随时间变化。如果系统将所有信息写入同一共享池而不作任何分离，并使其对每个 agent 可见，就可能出现一致性冲突：不同 agent 可能写入相互矛盾的事实，过时信息可能未被移除并在之后仍被 retrieval，从而误导推理。Agents Thinking Fast and Slow（Christakopoulou et al., 2024）报告称，Talker 可能因在 Reasoner 更新之前读取过时的信念状态而产生错误或仓促的回答。这里，memory conflict 主要通过两种方式处理：在写入时控制，或通过迭代回路逐步提升一致性。

**面向 memory isolation 的写控制。** 一种直接策略是在 memory write 与更新阶段强制隔离。在每个交互轮次中，agent 先将新提取的候选事实与现有 memory 状态比较，并通过受控评估机制选择性更新 memory，而非盲目追加新信息。在 Memory-R1（Yan et al., 2025b）中，memory management 器 agent 是唯一被允许改变 memory 的 agent。这包括四种离散编辑动作，即 ADD、UPDATE、DELETE 与 NOOP。ADD 写入新条目；UPDATE 重写或合并现有条目（尤其是当新信息是对旧信息的精炼或纠正时，系统倾向于保留信息更多的版本）；DELETE 移除被新证据明确否定或已过时的条目；NOOP 表示信息已被覆盖或对 long-term memory 不重要，因此不作更新。对每个用户查询，memory management 器观察当前 memory 状态，并决定操作哪些具体 memory 槽。因此，无关的 memory entry 保持不被触碰。WebCoach（Liu et al., 2025b）采用了相关的写入时隔离形式：memory storage 仅在 episode 完成后更新，因此部分轨迹永远不会被写入 long-term memory，从而隔离 episode 并防止 memory conflict。

**带反馈回路的 memory 一致性。** 与写控制相对，这类工作将 memory conflict 视为一致性的迭代优化过程。通常，多 agent memory 系统在稳定的约束 memory 中执行任务硬性要求，供后续迭代查阅，并维护一个不断增长的反馈 memory，记录先前轮次的失败以支持后续迭代中的学习。EvoMem（Fan et al., 2025b）是一个代表性例子。其验证器将每个候选与存储的约束 memory 比较并输出分数。仅当分数达到一百时，系统才接受解决方案。

![](../assets/arxiv-2602.06052-fig7.jpg)  
图 7：foundation agent memory 系统的 memory evolution 与优化策略。我们展示学习策略如何引导 agent 决定存储什么、何时存储、如何表示，以及何时何处 retrieval 或丢弃 memory。该图总结了三种常见方法，包括 prompt、fine-tuning 与 RL，它们使 memory 决策从不精确的 memory management 逐步改进为有效且准确的 memory management。

## 5 Memory Evolution 与 Optimization Policies

本节考察 agent 如何获得策略，以通过读取、写入、更新、整合、抽象、遗忘与修剪等操作来演化和优化 memory。这些策略不依赖硬编码启发式，而是决定何时记住什么、积累的经验应如何转化为结构化知识与可复用技能，以及现有 memory 应如何根据后续交互与反馈修订。我们按主要优化机制将这些策略分为三种范式：prompt、fine-tuning 与 RL，如图 7 所示。

这些范式在不同层面实现 memory evolution 与优化。prompt 在推理期间直接重组与精炼 external memory；fine-tuning 将 memory operation 策略内化到模型参数中；RL 则根据 memory 决策对 agent 执行与任务结果的长期影响来优化这些决策。

## 5.1 Prompt-Driven Memory Evolution 与 Optimization


prompt-driven 的 memory 优化指在推理时使用 prompt、反思或总结来管理 memory、而不修改模型参数的策略，以区别于 fine-tuning（§5.2）与 RL（§5.3）。该范式将 memory policyparametric 为自然语言 prompt。agent 执行这些 prompt，以决定何时访问、修改或修剪 memory。这种方法的主要优势包括无需昂贵的模型 fine-tuning，以及策略具有高可解释性。我们进一步将该范式分为静态 prompt 控制（§5.1.1）与动态 prompt 控制（§5.1.2）。

## 5.1.1 Static Prompt-based Control

基于静态 prompt 的控制将 memory policy 编码为固定的、人工设计的规则，这些规则在执行期间保持不变。memory 决策在设计时通过 prompt 模板或预定义模式指定，提供强可解释性与可预测行为，但缺乏根据交互反馈或分布偏移进行适应的能力。

现有基于静态 prompt 的 memory 控制工作可分为三个设计目标：静态 memory operation 系统与组织，即把 memory 视为具有固定形式的结构化容器或操作系统，通过层次化划分、索引、总结或基于模式的表示加以实施，以缓解 long-horizon context 退化（例如 SCM（Wang et al., 2023a）、MemGPT（Packer et al., 2023）、LiCoMemory（Huang et al., 2025e）、MemoChat（Lu et al., 2023）、A-Mem（Xu et al., 2025e）、D-SMART（Lei et al., 2025）、MemWeaver（Yu et al., 2025d）与 Zep（Rasmussen et al., 2025））；single-agent 设置中的静态 memory 控制，即访问与保留由 prompt 中编码的人设身份或领域特定先验约束，而非由学得的相关性信号决定（例如 RoleLLM（Wang et al., 2024e）、ChatHaruhi（Li et al., 2023a）、Mem-PAL（Huang et al., 2025d）、WarAgent（Hua et al., 2023）、MemoTime（Tan et al., 2025b）、FinMem（Yu et al., 2025e）、TradingGPT（Li et al., 2023b）与 MemoCRS（Xi et al., 2024））；以及多 agent system 中的静态 memory 分配与协调，即通过预定义角色、模块化分解与结构化通信协议在 agent 之间分配 memory，而不使用基于学习的协调（例如 MIRIX（Wang & Chen, 2025）、LEGOMem（Han et al., 2025）、G-Memory（Zhang et al., 2025c）、MADRA（Wang et al., 2025g）、GameGPT（Chen et al., 2023）与 ChatDev（Qian et al., 2024a））。

## 5.1.2 Dynamic Prompt-based Control

基于动态 prompt 的控制探索以自然语言 prompt 编码的 memory policy 能否在测试时根据经验与反馈进行适配，而不更新模型参数。该范式不在设计时固定 memory 行为，而是将 memory 控制视为一个由语言中介且可持续修订的过程。

该领域的现有工作围绕一组紧密相关的研究问题展开。一类工作追问 memory 使用策略能否通过反思过往结果而被纠正，促使 agent 分析失败或成功，并将这些洞见转化为指导未来行为的修订后 memory 指令（例如 Reflexion（Shinn et al., 2023）、ReasoningBank（Ouyang et al., 2025）、WebCoach（Liu et al., 2025b）与 QuantAgent（Wang et al., 2024g））。另一类研究探究 memory 表示本身能否被动态优化，以在有限 context 预算下提升信息效率，将 compression、去噪与结构重组视为自适应的、prompt-driven 的过程（例如 ACON（Kan et al., 2025c）、ACE（Zhang et al., 2025j）、SeCom（Pan et al., 2025）、Nemori（Nan et al., 2025）、CAM（Li et al., 2025d）、EvoMem（Fan et al., 2025b）与 ViLoMem（Bo et al., 2025））。还有一个问题关注动态 prompt 能否将积累的经验经 distillation 形成可复用的程序知识，例如推理模板、执行脚本或超越 episodic recall 的工具使用策略（例如 BoT（Yang et al., 2024b）、Memp（Fang et al., 2025b）与 ToolMem（Xiao et al., 2025））。尽管具有适应性，这些方法本质上仍由语言中介，且缺乏显式的 credit assignment，与 fine-tuning 和基于 RL 的方法相比，限制了其长期策略优化的能力。

## 5.2 Parameterized Memory Policies 的 Fine-Tuning

除基于 prompt 的适应之外，SFT 将 memory policy 内化到模型参数中，从而实现更稳定、更可复用的 memory 行为。从策略学习视角看，基于 SFT 的方法研究 memory policy 一旦 embedding 模型权重，如何被内化、稳定化与高效执行。

## 5.2.1 Policy Internalization into Parameters

基于 SFT 的 memory 控制的一个决定性特征是 memory policy 被内化到模型参数中，将 memory 从外部 context 操作问题转变为 parametric policy 表示。这些方法不依赖推理时的 prompt 或显式缓冲，而是将 memory 相关行为直接嵌入权重空间，从而实现跨任务稳定且可复用的 memory 使用。

在该范式内，现有工作探索若干紧密相关的研究问题：memory 控制策略如何 embedding 模型参数，以及这种内化应如何组织。一些方法聚焦于内化 memory content 本身，将短期 context 信息经 distillation 形成长期 parametric 表示（Wang et al., 2024l; 2025p）。其他方法强调内化 memory 访问与 retrieval 行为，通过学习 parametric 接口或轻量模块来中介与外部或structured memory storage 的交互，而非将原始内容吸收进权重（例如 Memory3（Yang et al., 2024a）与 MLP Memory（Wei et al., 2025c））。一条相关工作研究此类 parametric memory policy 如何被层次化组织，从而实现大型 memory 组件的可扩展调用，同时将长尾知识与核心推理能力解耦（Pouransari et al., 2025）。尽管存在差异，这些方法共享同一目标：将 memory 控制从 prompt 级操作转向通过监督学得的 parametric 决策规则。

## 5.2.2 Parameterized Policy 的稳定化与边界控制

除内化之外，SFT 还通过学得关于应写入、纠正或抑制什么的显式边界，在 memory 控制嵌入参数后实现 memory policy 的稳定化。这些方法不仅旨在扩展 memory 容量，还旨在防止长期使用下的误差累积、概念漂移与人设不一致。

这些工作的一个共同主题是利用监督来正则化 memory update 并执行边界约束。一些方法训练模型在将信息提交到 memory 之前执行反思或自我分析，鼓励存储与任务意图对齐的高层、抗噪表示（Liu et al., 2023b; Zhang et al., 2025r; Chen et al., 2025d）。其他方法强调通过纠正信号、验证器反馈或路由机制，学习何时应修订或覆盖现有知识，以识别并修复错误或过时 memory（例如 WISE（Wang et al., 2024f）、SuperIntelliAgent（Lin et al., 2025）与 CRMWeaver（Lai et al., 2025））。在 long-horizon 交互设置中，防御性边界控制通过限制哪些经验可被保留或复用来进一步约束 memory update，以保持角色或身份一致性（例如 Character-LLM（Shao et al., 2023））。总体而言，这些方法不把反思与自我纠正视为孤立的 prompt 级技术，而是将其视为通过监督学习稳定且有界 memory policy 的机制。

## 5.2.3 Parameterized Policy 的效率与 Retrieval Refinement

除学习存储什么以及如何稳定 memory 之外，SFT 还用于精炼 parametric memory policy 在推理时的执行方式，尤其是在 memory read 与 retrieval 期间。这些方法不依赖穷举式 context 访问，而是将 retrieval 本身视为一种学习策略，并优化查询如何被构造、迭代精炼并应用于压缩的 memory 表示。通过监督训练，模型学会生成精确的 retrieval 线索以实现定向 memory 访问（Qian et al., 2025b），执行多跳或渐进式 retrieval 以跨推理步骤精炼查询（Ko et al., 2024），并通过内化或可逆地精炼 memory 表示来优化 compression-aware retrieval（Cao et al., 2025b; Wang et al., 2025m），从而在降低推理时开销的同时提升推理稳健性。尽管有这些收益，所得的 retrieval 策略在训练后仍然固定，且未能在扩展决策时程上纳入显式 credit assignment。

## 5.3 Memory Policies 的 Reinforcement Learning

RL（He et al., 2026）通过使 memory policy 能够经由交互与奖励反馈进行优化，引入了一种根本不同的 memory 控制范式。与基于 prompt 或监督的方法不同，RL 允许下游任务结果影响较早的 memory 相关决策，使 memory construction 本身成为一种可学习策略。现有工作可被理解为逐步扩展强化信号塑造 memory 行为的时间范围。

## 5.3.1 Step-Level Memory Decisions

在最短时间范围内，RL 通过将 memory management 视为一系列步骤级决策，应用于 memory 控制。在此设置中，memory operation 被建模为由学习策略选择的动作，并依据其对任务奖励的即时或短时程影响进行优化。

一类工作研究 memory 编辑如何被形式化为显式动作空间。Memory-R1（Yan et al., 2025b）定义添加、更新、删除或跳过条目等原子 memory operation，并学习一种 memory policy，根据任务级奖励在这些动作之间选择。MemAct（Zhang et al., 2025p）扩展这一表述，将修剪与总结等更细粒度的编辑动作直接纳入 agent 的统一策略空间。一个紧密相关的问题涉及显式容量约束下的步骤级 memory 决策。MemAgent（Yu et al., 2025b）与 RMM（Tan et al., 2025c）通过交互驱动的反馈学习在处理极 long-context 时哪些信息应被写入固定大小的 memory 缓冲，以应对该设置。Mem-α（Wang et al., 2025q）推广这一范式，将 memory construction 本身表述为顺序决策问题：agent 通过 RL 学习如何填充与更新结构化的多组件 memory（例如核心 memory、semantic memory 与 episodic memory），以最大化 long-horizon 任务表现。这些方法共同将步骤级 memory 控制框定为通过强化信号优化局部 memory 动作，而未显式建模 memory 状态构建的长期影响

## 5.3.2 Trajectory-Level Memory Representation

随着任务扩展到更 long-horizon，memory 决策的价值往往只有通过其对未来推理与动作选择的累积影响才显现。RL 通过允许延迟的任务结果塑造学习策略如何构建、更新与维护轨迹级 memory 状态，支持这一设置。

在此范围内，现有工作研究当交互历史不再能逐步评估时，如何学习紧凑、决策充分的 memory 表示。这些方法不把 memory 视为瞬态缓冲，而是将轨迹级 memory 视为 agent 马尔可夫状态的一部分，其质量通过下游决策表现来评估（Chen et al., 2025c; Wu et al., 2025d）。一个紧密相关的问题关注长交互历史应如何被抽象为这样的表示。若干研究将总结、折叠或 compression 视为策略决策，其有效性只能通过从未来结果传播的强化信号来评估（Lu et al., 2025b; Sun et al., 2025b; Li et al., 2025g）。轨迹级 memory 还引出 memory 状态应如何随新交互展开而随时间演化的问题。MemSearcher（Yuan et al., 2025a）通过维护迭代更新的紧凑 memory 状态并跨 context 传播优势来精炼 memory 表示，以应对该问题。这些工作共同将轨迹级 memory 刻画为一种学得的状态表示，其效用由其在 RL 下对决策的长期贡献来定义。

## 5.3.3 Cross-Episode 与 Multi-Agent Memory

当 memory scaling 到单个轨迹之外，它不再仅服务于即时推理，而是积累经验，其价值在反复 episode 或交互中显现。在这一范围上，RL 变得尤为重要，因为长期与 cross-episode 奖励信号为哪些 memory 应被 memory policy 保留、适应或修订提供了显式 credit assignment。

这一层面的研究关注当 memory 跨越多个 episode 或 agent 时，经验应如何被表示、复用与协调。跨 episodic memory 不保留原始交互历史，而旨在 distillation 更高层、与决策相关的知识，例如可复用策略、自我纠正规则或抽象行为模式，其效用通过反复强化信号评估。这一视角支撑了 MCTR（Li et al., 2025h）与基于图的经验抽象（Xia et al., 2025）等方法，它们将经验编码为通过交互学得的可迁移决策知识。至关重要的是，此类经验以受 RL 支配的、依赖 context 的方式被 retrieval 与应用，Retroformer（Yao et al., 2024）与 Memento（Zhou et al., 2025a）中的反思性 retrieval 策略即为例证。随着 memory 进一步跨越 agent 或表示空间，RL 使反馈能够传播到单个轨迹之外。这包括 MemGen（Zhang et al., 2025d）等latent 或非文本 memory 表示、ReMemR1（Shi et al., 2025a）中的 retrieval 路径优化与回调机制，以及 MAICC（Jiang et al., 2025d）与 SRMT（Sagirova et al., 2025）等多 agent system 中的共享或去中心化 memory policy。这些研究将 cross-episode 与多 agent memory 框定为基于 RL 的 memory 控制的最广范围，其中 memory policy 通过积累的交互与奖励反馈演化，而非依赖预定义规则或一次性监督。

## 6 Evolving 与 Scaling：Memory、Contexts 与 Environments

随着 LLM 与 agent 被部署到日益真实的设置中，其运行期间积累的经验与 context 信息沿开放世界环境中的三个扩展轴迅速增长：交互时程、环境复杂度，以及交互环境、工具与 agent 的数量。传统评估往往依赖静态、context-limited 的设置，忽视环境动态；而真实世界效用要求 agent 在扩展时间框架与异构数据结构上积累、保留、整合与更新知识。仅仅扩展 context window 并不足够，因为长运行交互会引入冗余、过时、冲突且日益异构的经验，必须被选择性组织与变换。本节探讨 memory 如何成为应对这一扩展挑战的必要架构方案，从简单交互日志转变为管理不断增长的经验并支持 agent 持续演化的自适应 substrate。通过选择性保留任务相关状态、将轨迹抽象为可复用知识与技能、跟踪演化中的用户偏好，以及跨 agent 协调经验，可扩展 memory 使开放世界环境中的 long-horizon 执行、持久个性化与集体适应成为可能。


## 6.1 Context-Limited Simple Environments

当今大多数 LLM 与 agent benchmark 仍配置在 context-limited 的简单环境中：agent 被置于紧凑且封闭的世界中，仅在一个短时程任务实例上交互（Hendrycks et al., 2021b），或与合成的非真实用户交互（Maharana et al., 2024）。此类设置虽然便于可复现性与实验比较，却在很大程度上低估了真实世界 agent 所面对的 memory 需求。因此，强 benchmark 表现往往反映的是 context 内模式匹配或短期推理的熟练度，而非在扩展交互以及不断演化的用户偏好与 context 中积累、保留与复用知识的能力。这种错配导致了显著的效用差距：在现有 benchmark 上取得高分的 agent，常常无法在开放式动态环境中表现出长期适应、用户个性化或任务特定技能复用。

现有 LLM 与 agent 评估的很大一部分仍局限于静态、context-limited 的环境。经典通用问答 benchmark，包括 SQuAD（Rajpurkar et al., 2018）、HotpotQA（Yang et al., 2018）与 KILT（Petroni et al., 2021），运行在冻结的 Wikipedia 快照上；而 MS MARCO（Craswell et al., 2021）、Natural Questions（Kwiatkowski et al., 2019）、SearchQA（Dunn et al., 2017）与 TriviaQA（Joshi et al., 2017）则用预先收集的查询与段落替代实时信息访问。这些设计产生稳定、有界且控制良好的信息源，现代系统在此类信息源上达到近乎饱和的性能。然而，retrieval 与推理严格是 episodic 且实例隔离的：agent 既不维护跨查询状态，也不面对时间漂移、来源不一致或演化中的知识。因此，此类 benchmark 对持久 memory 的要求极低，主要测试短期 retrieval 与 context 内推理，而非长期知识积累或自适应 context 管理。类似的局限也延伸到工具使用与网页交互 benchmark。ToolBench（Qin et al., 2024）、WebShop（Yao et al., 2022）与 WorkArena（Drouin et al., 2024）等框架依赖固定 API 或自托管环境，将认证、故障恢复以及长期用户或任务状态抽象掉。即便是与实时网页交互的系统，包括 WebGPT（Nakano et al., 2021）与 WebVoyager（He et al., 2024a），也仍受限于受限浏览界面、精选站点列表与严格交互预算。ScienceWorld（Wang et al., 2022）、ALFWorld（Shridhar et al., 2021）、TextWorld（Côté et al., 2018）与 Jericho（Hausknecht et al., 2020）等顺序与交互式环境，以及 APPS（Hendrycks et al., 2021a）、SWE-bench（Jimenez et al., 2024）、SWE-Bench Pro（Deng et al., 2025）与 SWE-Lancer（Miserendino et al., 2025）等编程 benchmark，提高了任务复杂度，但仍以 episodic、重置为中心且由评估驱动。因此，这些 benchmark 系统性地未能评估 cross-episode 的知识积累与 long-horizon 一致性，从而掩盖了 memory 对稳健真实世界 agent 部署的关键作用。

## 6.2 Context-Exploded Real-World Environments

与研究设置中 context-limited 的 benchmark 评估不同，真实世界部署让 agent 面对 context 沿多个轴扩展的环境。它随长交互时程累积，因结构化且异构的环境状态而日益复杂，并跨越多个环境、agent 与工具。此外，真实世界 context 不仅在体量上增加：它持续变化，因为用户修订偏好、环境演化、工具产生新观察，agent 也获得新知识与技能。因此，可扩展 memory 必须同时支持对不断增长的 long-context 的 compression，以及 agent 所保留状态的持续演化。

## 6.2.1 随 Long-Horizon Interactions 演化

**扩展交互时程上的用户 memory evolution。** 在持久用户—agent 交互中，agent 需要在扩展对话时程上维持与用户一致的连贯行为与决策一致性。与短小、自包含的对话不同，早期轮次引入的信息——例如用户偏好、身份属性或隐式任务约束——可能不会立即影响响应，但往往在交互的后期阶段变得决定性。因此，交互历史与其说是静态输入，不如说是用户状态的演化表示，必须随时间被选择性维护与修订。这种信息持久性要求源于：某些用户属性相对稳定，而偏好与目标跨不同轮次逐渐演化（Li et al., 2016）；涉及规划或持续目标的对话任务具有长期结构；以及身份与目标一致性对用户信任与可用性的重要性（Zhang et al., 2018）。

因此，long-horizon 个性化必须平衡一致性与适应：agent 应保留持久的用户特征，同时识别近期交互何时提供了充分证据，以更新先前推断的偏好或约束。然而，在固定 context window 约束下，long-horizon 对话系统常表现出失败模式，例如早期 contextforgetting 以及随交互长度增加而逐步出现的 context 漂移（Liu et al., 2024b; Xu et al., 2022a）。这些失败并非孤立的推理错误，而是长期 context 管理不当的累积后果。它们可能使 agent 要么忘记持久偏好，要么固守过时信息，两者都会破坏持续的偏好对齐。

现有缓解策略，例如滑动 context window、启发式截断与基于摘要的 memory mechanism（Park et al., 2023），以及用户画像或人设 memory 等显式长期结构（Xu et al., 2022a），提升了可扩展性，但往往降低回忆可靠性。在实践中，看似边缘的信息可能尽管具有未来相关性，却被不可逆地丢弃，暴露出 context 预算控制与长期信息可访问性之间的根本权衡（Liu et al., 2024b）。因此，挑战不在于简单地保留更多交互历史，而在于持续判断哪些信息仍然稳定、哪些已经过时、哪些应修改 agent 当前对用户的表示。

**多轮工具使用的累积执行 memory。** 在依赖多轮工具使用与推理架构的 agent 中，context explosion 可能加剧。除对话历史之外，基于工具的 agent 还必须保留工具输入、执行输出与中间状态，其中许多会在后续推理步骤中被反复引用（Schick et al., 2023）。在 ReAct（Yao et al., 2023）与 Planner–Executor 架构（Wang et al., 2023b）等框架中，这种累积尤为严重：规划轨迹、工具反馈与反思性推理被显式保留，以维持连贯性与决策一致性（Shinn et al., 2023）。因此，context 规模可能随交互长度以及工具调用数量或复杂度迅速增长。

在 ReAct 式 agent 中，显式推理轨迹本身成为 context 的一部分，实现了可解释性与复杂推理，但同时引入大量且持续存在的 context 负担。此外，对许多真实世界应用而言，大型或异构的工具输出，例如网络搜索结果（Wei et al., 2025e）与数据库查询结果（Jing et al., 2025），也会急剧累积。天真地移除或压缩这些轨迹，可能破坏推理与动作步骤之间的因果依赖，并损害后续决策（Yao et al., 2023）。有效的 memory 必须转而保留任务关键状态、未解决的依赖、先前的工具效果与执行失败，同时压缩冗余观察与推理轨迹。

因此，尽管多轮工具使用大幅增强 agent 能力，它也在有限 context window 上暴露了可扩展性限制，凸显了 long-horizon agent 设计的核心挑战（Liu et al., 2024b）。除维持进行中任务的状态之外，agent 还应将反复出现的工具使用 experience consolidation 为可复用流程与技能，使未来任务能够受益于先前执行，而非重现相同的长推理轨迹。

## 6.2.2 随 Environmental Complexity 演化

随着环境复杂度扩展，agent 的 context 必须容纳异构数据模态、异步工具交互，以及受协议或权限约束的外部状态。在此类设置中，context 不再能被当作附加到 prompt 上的线性交互轨迹。真实世界部署要求对结构化产物进行推理，例如 API 响应、文件、数据库、日志与配置状态，其语义取决于模式、来源、更新规则与时间有效性。天真地将这些产物扁平化为 token 序列，既低效又在结构上有损，损害可解释性、精确 retrieval 与定向更新（Modarressi et al., 2024）。因此，环境复杂度的提升使 memory 从 prompt 累积的隐式副产物转变为显式的系统级组件，负责结构化 context 管理。memory 挑战由此从仅仅保留过往信息，转变为在多样来源与生命周期上维持连贯、可查询且可更新的环境状态表示。对 self-evolving agent 而言，这些表示还必须随模式、接口、权限与环境动态变化而进一步适应，同时保持先前获得的知识与技能的有效性与来源可追溯性。

近期 agent system 通过将 memory 外化到 prompt 之外，并暴露显式读写接口，使存储与推理解耦，以应对这一挑战（cauri, 2025）。外化 memory 支持模式感知 retrieval、版本化、定向编辑与访问控制——这些操作在仅基于 prompt 的 context 中难以或无法实现（Yakobi & Sadon, 2025）。Model Context Protocol（Anthropic, 2024）等基于协议的接口标准化 agent 访问外部工具与 context 资源的方式，而 Claude Agent Skills（Anthropic, 2025）等面向技能的抽象将程序性指令、可执行资源与领域特定工作流打包为可复用单元。这些抽象共同将持久状态、环境访问与可复用技能同瞬态推理 context 分离，从而提升模块化、可审计性与行为安全性（Keen, 2025）。

随着环境复杂度提高，持久化变得不可避免：用户模型、系统配置与任务产物代表必须在 session 之间保持一致、同时遵守隐私、权限与回滚等治理约束的持久状态（Sarin et al., 2025; Wu & Shu, 2025）。这些需求带来额外挑战，包括模式漂移、并发更新与路径依赖评估，凸显了对原则性抽象的需要——将 memory 视为复杂开放世界环境中 context 管理的一流基础设施。因此，memory 必须在内容与结构两个层面演化：它应更新环境事实与任务状态，在模式变化时重组表示，并在先前学到的技能所依赖的接口或动作前置条件不再有效时修订这些技能。

## 6.2.3 跨 Multiple Environments 与 Agents 演化

**作为跨工具环境接口的 memory。** 在开放世界设置中，context 复杂性不仅来自单一环境内的长时间交互，也来自跨多个异构工具环境运行的需要，每个环境由不同状态表示、动作空间与访问协议定义。例如，个人具身助手可能在物理家庭环境（在那里它执行以感知反馈为根基的 long-horizon 行为）与数字网页环境（在那里它通过浏览器交互 retrieval 天气预报等信息）之间交替。支持此类行为需要 memory mechanism 能够跨多样动作与观察模态保留、区分并协调环境特定状态（Glocker et al., 2025; Hong et al., 2025）。在 OSWorld（Xie et al., 2024）中，GUI agent 可能在浏览器中发出搜索查询、从新闻应用 retrieval 结果，并在文件查看器中查阅文档，每次交互都会产生环境特定的观察与状态转移。工具使每个环境内的局部交互成为可能，而 memory 提供跨环境边界持久、组织并 context 化信息的接口功能。因此，memory system 不仅需要记录过往工具调用，还需要维持结构化且分离的环境状态表示，以支持不超出 context window 的 long-horizon 推理（Burtsev et al., 2020; Rae et al., 2019）。

**多人类—agent system 中的 memory。** 随着 agent system 扩展到包含多个 agent 与人类参与者，有效协调日益依赖结构化通信与共享 memory mechanism，而非朴素的 context 共享——后者在有限 context window 下会迅速碎片化（Chen et al., 2025f）。近期方法引入 agent 对齐或半共享的 memory 抽象，在长交互时程上编码关系历史、agent 间依赖与任务相关状态。例如，Intrinsic Memory Agents 为 agent 配备角色特定的 memory 模板，在保留专门视角的同时支持整合进共享 context substrate，显著提升 long-horizon 规划的稳定性（Yuen et al., 2025）。除 memory 之外，结构化通信协议在协调中发挥核心作用：层次化与角色感知的对话方案减少 agent 间交流中的噪声与偏差（Wang et al., 2025s），而认知自适应编排框架根据推断的协作者状态动态调整通信模式（Zhang et al., 2025h）。在涉及多个人类与 agent 的开放世界部署中，协调进一步扩展到对齐、冲突解决与分歧下的集体决策。经验研究表明，基于辩论的协议以及共识或多数投票等决策规则，会显著影响推理与知识任务上的表现（Kaesberg et al., 2025; Samanta et al., 2025），包括多模态抽取设置——在那里少数几轮辩论即可可测量地提升准确率（Huang & Caragea, 2026）；而自适应且无需共识的辩论机制则平衡计算成本、稳健性与从众效应（Fan et al., 2025a; Cui et al., 2025b）。随着这些系统扩展，显式的图结构表示日益支撑编排与通信，将关系依赖组织为可优化的通信拓扑，并将 context 管理重新表述为开放世界系统中分布式 memory、协调与对齐的问题（Qian et al., 2025a; Zhang et al., 2025f;e）。

## 7 Evaluation

评估 foundation agent memory，根本上是衡量在 long-horizon 交互下，所存储的信息与经验是否准确、有用、可靠且可高效访问。下面，我们在第 7.1 节中按三个基本类别总结常用指标，包括基于准确率、基于相似度与 LLM 作为评判者（LLM-as-a-judge）。此外，我们在第 7.2 节中汇总用于评估 foundation agent 表现的常用 benchmark。

表 3：foundation agent memory 评估中使用的指标。

<table><tr><td>指标</td><td>简要说明</td><td>代表性 benchmark</td></tr><tr><td colspan="3">基于准确率的指标</td></tr><tr><td>准确率 / memory 准确率</td><td>正确回答的实例比例，按 benchmark 粒度（例如问题级、轮次级、session 级或任务级）计算。</td><td>HotpotQA (Yang et al., 2018), PerLTQA (Du et al., 2024), MemoryBank (Zhong et al., 2024)</td></tr><tr><td>F1 分数</td><td>精确率与召回率的调和平均，按 token 级计算，并可选择聚合到问题、轮次或 session 级。</td><td>MuSiQue (Trivedi et al., 2022), MSC (Xu et al., 2022a), PerLTQA (Du et al., 2024)</td></tr><tr><td>Recall@K</td><td>通过检查相关证据是否出现在前 K 个结果中来评估 retrieval 成功率。</td><td>LongMemEval (Wu et al., 2025b), PerLTQA (Du et al., 2024)</td></tr><tr><td>平均精度均值（MAP）</td><td>对相关条目所在排名的精确率取平均，再跨查询取平均。</td><td>PerLTQA (Du et al., 2024), PMR (Kohar &amp; Krishnan, 2025)</td></tr><tr><td>NDCG@K</td><td>在截断 K 处衡量排序相关性，优先考虑靠前位置。</td><td>LongMemEval (Wu et al., 2025b), PMR (Kohar &amp; Krishnan, 2025)</td></tr><tr><td>成功率（SR）/ 目标完成率（GC）</td><td>在环境定义的成功检查器下完成的交互任务比例，通常在任务或 episode-level 衡量。</td><td>WebArena (Zhou et al., 2024), OSWorld (Xie et al., 2024), MineDojo (Fan et al., 2022)</td></tr><tr><td>Pass@K / 解决率（RR）</td><td>在 K 次采样尝试中至少出现一个正确解的概率（Pass@K），或端到端解决的问题比例（RR）。</td><td>HumanEval (Chen et al., 2021), SWE-Bench (Jimenez et al., 2024)</td></tr><tr><td>memory 完整性（MI）</td><td>memory 抽取的完整性，通过 memory 点上的覆盖率或召回率衡量。</td><td>HaluMem (Chen et al., 2025a)</td></tr><tr><td>虚假 memory 率（FMR）</td><td>引入幻觉 memory 的比率，包括捏造或错误的更新。</td><td>HaluMem (Chen et al., 2025a)</td></tr><tr><td colspan="3">基于相似度的指标</td></tr><tr><td>ROUGE</td><td>衡量生成文本与参考文本之间的 n-gram 与最长公共子序列重叠。广泛用于摘要。</td><td>LoCoMo (Maharana et al., 2024), MemoryBench (Ai et al., 2025)</td></tr><tr><td>BLEU</td><td>与参考文本的 n-gram 精确率重叠。常用于对话生成。</td><td>DuLeMon (Xu et al., 2022b), LoCoMo (Maharana et al., 2024)</td></tr><tr><td>Distinct-n</td><td>计算唯一 n-gram 的比例，以衡量词汇多样性与抑制重复。</td><td>DuLeMon (Xu et al., 2022b), MADial-Bench (He et al., 2025a)</td></tr><tr><td>BERTScore</td><td>候选文本与参考文本之间基于 embedding 的语义相似度。</td><td>LoCoMo (Maharana et al., 2024), MADial-Bench (He et al., 2025a)</td></tr><tr><td>FactScore</td><td>事实级忠实度：抽取原子主张并衡量被 retrieval 证据支持的比例。</td><td>LoCoMo (Maharana et al., 2024), Face4Rag (Xu et al., 2024b)</td></tr><tr><td>困惑度（Perplexity）</td><td>预测参考文本的似然指标，通常按 token 级计算并跨 session 聚合。</td><td>MSC (Xu et al., 2022a), DuLeMon (Xu et al., 2022b)</td></tr><tr><td colspan="3">LLM 作为评判者的指标（JUDGE）</td></tr><tr><td>响应正确性</td><td>由强 LLM 评判响应是否回答了查询或满足约束。</td><td>LongMemEval (Wu et al., 2025b), MemTrack (Deshpande et al., 2025)</td></tr><tr><td>忠实度 / grounding</td><td>评判者检查响应主张是否以 retrieval context 或 memory 为据，或检查引用是否支持主张。</td><td>SeekBench (Shao et al., 2025), LiveResearchBench (Wang et al., 2025f)</td></tr><tr><td>偏好遵循</td><td>评判者通过检查输出是否满足用户陈述的偏好或约束来评估偏好遵循。</td><td>PrefEval (Zhao et al., 2025c), BEAM (Tavakoli et al., 2025), ConvoMem (Pakhomov et al., 2025)</td></tr></table>


## 7.1 Metrics

表 3 总结了 foundation agent memory 评估中最常用的指标。评估 foundation agent 及其 memory module 表现有多个维度。有些任务有明确的 ground truth，可用精确正确性评分（Du et al., 2024; Dunn et al., 2017），而另一些任务是开放式的（对话（Budzianowski et al., 2018）、摘要（Maharana et al., 2024）、偏好遵循（Zhao et al., 2025c）），其中多个输出都可接受，基于参考的评分并不可靠。因此，现有工作通常将结果级正确性与面向 retrieval 的评估以及基于评判者的评分细则相结合，具体取决于 benchmark 是否暴露 memory module、是否使用 long-context prompt，或是否评估在特定环境、场景或任务中行动的 agent（Patlan et al., 2025; Yadav et al., 2025）。

**基于准确率的指标。** 当任务有清晰客观结果时，使用基于准确率的指标。对于回答关于长历史的问题，准确率或 memory 准确率直接评估最终响应与 ground truth 的对齐程度（Yang et al., 2018; Zhong et al., 2024; Du et al., 2024）。F1 通过为 token 级部分重叠给分，放宽了精确匹配标准。这在响应不完全匹配但存在一定差异时尤为常见（Trivedi et al., 2022; Deng et al., 2023）。当 benchmark 评估显式 memory module 时，Recall@K、平均精度均值（MAP）与归一化折损累计增益（NDCG）@K 成为核心，因为它们将“系统是否 retrieval 到正确证据”与“生成器是否把答案表述得好”区分开来。Recall@K 衡量相关条目出现在前 K 个 retrieval 结果中的比例（Wu et al., 2025b）。MAP 与 NDCG@K 则还考虑排序质量，对把相关 memory 排在前面的系统给出更高分数（Kohar & Krishnan, 2025）。对交互式 agent 而言，正确性改由环境评估器定义，因此成功率（SR）或目标完成率（GC）表示 agent 是否端到端完成任务（Zhou et al., 2024; Zheng et al., 2025a）。对具身 agent，还常用路径长度加权成功率（SPL）、导航效率与交互成功率等额外指标，以捕捉二元完成之外的执行质量。对代码与工具使用设置，Pass@K 与解决率（RR）衡量 K 次采样尝试中是否至少有一次解决任务或解决问题（Yao et al., 2025; Jimenez et al., 2024）。此外，以 memory 为中心的 benchmark 日益增加仅靠端到端任务准确率难以捕捉的失败模式评估。memory 完整性量化抽取的 memory 是否覆盖所需 memory 点，虚假 memory 率衡量系统在存储、更新或使用期间引入捏造或错误 memory 的频率（Chen et al., 2025a）。

**基于相似度的指标。** 基于相似度的指标最常见于对话生成与摘要，这些任务输出自由形式，正确性无法完全由准确率或 F1 分数检查（Chen et al., 2024d）。BLEU、ROUGE 与 ROUGE-L 衡量与参考文本的词汇重叠，适合跟踪表层相似性，但可能低估有效的改写，并高估流畅却无据的响应（Gehrmann et al., 2023; Ai et al., 2025）。Distinct-n 通过衡量词汇多样性补充重叠指标，抑制可能抬高相似度分数却不提升忠实度的重复生成（He et al., 2025a）。当词汇重叠过于严格时，BERTScore 提供基于 embedding 的语义相似度近似（Maharana et al., 2024），FactScore 则通过在原子事实主张层面检查一致性来评估 memory 忠实度（Min et al., 2023），这在摘要被用作 long-history compression 机制时尤为相关（Saxena et al., 2025）。困惑度也被一些长对话 benchmark 用作跨 session 生成质量的似然指标（Xu et al., 2022a），但它仍是 memory 表现的间接指标，因为它并不验证模型内容是否以正确的历史证据为据（Durmus et al., 2022）。

**LLM 作为评判者的指标。** 当 ground truth 或参考不完整、多个响应可接受，或评估需要难以编码为字符串匹配的评分细则时，使用 LLM 作为评判者的指标（Yu et al., 2025a）。响应正确性让强模型判断答案是否满足用户查询（Deshpande et al., 2025），这对开放式响应很方便，但引入评判者依赖与对 prompt 的敏感性。忠实度或 grounding 使用评判者验证主张是否由 retrieval context 或 memory 支持（在某些设置中，还检查所提供的引用是否支持响应）（Shao et al., 2025; Wang et al., 2025f），这有助于将有帮助但幻觉的答案与有证据支持的答案区分开。偏好遵循使用评判者判断输出是否尊重显式用户约束或陈述偏好（Zhao et al., 2025c; Tavakoli et al., 2025; Pakhomov et al., 2025），这对以用户对齐而非单一事实标签定义正确性的个性化 benchmark 至关重要（Wang et al., 2024b）。

在这些指标中，一个实践含义是：当 benchmark 能将 retrieval 或选择与生成分离时，评估就更可归因于 memory mechanism（Chen et al., 2025a）。retrieval 与排序指标（Recall@K/MAP/NDCG@K）评估 memory 接口是否呈现正确条目，而完整性与面向幻觉的指标（MI/FMR）揭示那些在累积到一定程度之前可能不会改变端到端准确率的失败模式（Zhang et al., 2025a）。相比之下，基于相似度的指标仍有助于跟踪流畅度与摘要质量，但应与 grounding 检查（FactScore 或基于评判者的忠实度）配对，以避免奖励无据的改写（Aralikatte et al., 2021）。此外，一些 benchmark 还强调成本与可行性（例如容量与效率）（Tan et al., 2025a），从而促使报告不仅说明 agent 记住了什么，还说明达到该性能所需的计算与存储权衡。

## 7.2 Benchmarks

为评估 memory 在多样场景中对 foundation agent 任务的改进，我们将现有 benchmark 分为两个主要领域：user-centric 的 benchmark 与 agent-centric 的 benchmark。user-centric 的 benchmark，例如 MSC（Xu et al., 2022a）与 MemoryBank（Zhong et al., 2024），主要评估对话一致性，衡量 agent 在 multi-session 或多轮对话中保留人设信息、回忆用户偏好并维持连贯交互的能力。另一方面，agent-centric 的 benchmark，包括 OSWorld（Xie et al., 2024）与 WebArena（Zhou et al., 2024），聚焦 memory 在复杂问题求解中的功能性应用，衡量需要多跳推理与工具使用的任务成功率。我们分别在第 7.2.1 节与第 7.2.2 节介绍常用的 user-centric 与 agent-centric 的 benchmark。

## 7.2.1 User-Centric Evaluation Benchmarks

user-centric 的 benchmark 在个性化对话中评估 foundation agent，其目标是长期与特定用户不断演化的画像及共享交互历史保持一致。与评估指标在很大程度上与用户无关的 agent-centric 任务（Mo et al., 2025）相比，user-centric 的设置本质上依赖用户（Zhao et al., 2025d）。agent 必须决定从对话中存储什么、在需要时 retrieval 相关信息、在用户改变偏好时修订它，并在证据缺失时保持校准（Terranova et al., 2025）。表 4 总结了代表性 benchmark 的交互规模（#session 数、#问题数、最大 context length）、数据资源（REAL/SIM/MIX），以及使用 ✓/✓/✗ 表示的 memory capability 与评估覆盖。

我们定义十项 user-centric 的 memory capability，以刻画 agent 在 long-horizon 交互中必须记住并使用什么（Wu et al., 2025b; Pakhomov et al., 2025）：事实抽取（FE）是从对话中识别并存储可复用事实（例如用户属性、约束、关键事件）以便日后回忆的能力；multi-session 推理（MR）要求整合分布在多个 session 与轮次中、而非包含在单一 session 中的证据；时间推理（TR）涵盖对时间序列（顺序、时间戳、近来性）的推理，以及在信息变化时选择正确状态；更新与刷新（UR）捕捉在新证据与旧内容矛盾时显式修订 memory（覆盖过时事实并在冲突下遵循最新状态）；Compression 与 Summarization（CS）是将长交互历史浓缩为仍保持忠实且可用的紧凑 memory 表示的能力；forgetting 与 retention（FR）反映在维持长程信息的同时选择性 forgetting 过时或无关内容以减少干扰；用户事实与偏好（UP）聚焦 user-centric 的 memory subject（人设、偏好、关系、反复出现的习惯或事件）及其演化；助手事实（AS）跟踪助手自身先前的陈述、建议或承诺，使 agent 与先前所言保持连贯；隐式推断与连接（IC）衡量 agent 能否连接零散线索并执行多跳或隐式推断（例如在未被提醒的情况下将先前提到的限制应用于新建议）；以及弃答与边界处理（AB）

表 4：user-centric 的 memory benchmark 概览。memory capability——FE：事实抽取；MR：multi-session 推理；TR：时间推理；UR：更新与刷新；CS：Compression 与 Summarization；FR：forgetting 与 retention；UP：用户事实与偏好；AS：助手事实；IC：隐式推断与连接；AB：弃答与边界处理。标记——✓：显式覆盖。benchmark 将该能力定义为目标，配有专门任务类型或标注，并直接评估；✓：部分或间接覆盖。该能力可能在某些实例中被要求或由设置隐含，但缺乏专门标注或能力特定评估，因此覆盖较弱或无法清晰归因；✗：未覆盖。不存在相应任务、标注或评分细则，评估既不要求也不衡量该能力。资源——REAL（人工撰写或真实世界对话）、SIM（完全合成或模拟）、MIX（真实与合成混合）。评估指标——AR：准确 retrieval；TTL：测试时学习；LRU：长程理解；SF：选择性 forgetting；MM-R：多消息相关性；RC：响应正确性；CC：context 连贯性；MA：memory 准确率；MI：memory 完整性；FMR：虚假 memory 率；MRS：memory 保留分数；JUDGE：LLM 作为评判者。

<table><tr><td>名称</td><td>#session</td><td>#问题</td><td>最大 Token</td><td>FE</td><td>MR</td><td>TR</td><td>UR</td><td>CS</td><td>FR</td><td>UP</td><td>AS</td><td>IC</td><td>AB</td><td>资源</td><td>链接</td><td>评估</td></tr><tr><td>MSC</td><td>5K</td><td>-</td><td>1K</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>✗</td><td>√</td><td>√</td><td>√</td><td>✗</td><td>REAL</td><td></td><td>Perplexity</td></tr><tr><td>DuLeMon</td><td>27,501</td><td>-</td><td>1K</td><td>√</td><td>√</td><td>✗</td><td>√</td><td>√</td><td>✗</td><td>√</td><td>√</td><td>√</td><td>✗</td><td>REAL</td><td></td><td>F1, Recall@K, BLEU, Distinct-n</td></tr><tr><td>MemoryBank</td><td>300</td><td>194</td><td>5K</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>✗</td><td>SIM</td><td></td><td>Retrieval Accuracy, RC, CC</td></tr><tr><td>PerLTQA</td><td>3,409</td><td>8,593</td><td>1M</td><td>✗</td><td>√</td><td>✗</td><td>✗</td><td>✗</td><td>✗</td><td>√</td><td>√</td><td>√</td><td>✗</td><td>SIM</td><td></td><td>Accuracy, F1, Recall@K, MAP</td></tr><tr><td>LoCoMo</td><td>1K</td><td>7,512</td><td>10K</td><td>√</td><td>√</td><td>√</td><td>✗</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>MIX</td><td></td><td>F1, ROUGE, BLEU, MM-R</td></tr><tr><td>DialSim</td><td>~1,300</td><td>1M</td><td>367K</td><td>✗</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>MIX</td><td></td><td>Accuracy</td></tr><tr><td>LOCCO</td><td>3,080</td><td>2,981</td><td>-</td><td>√</td><td>✗</td><td>√</td><td>✗</td><td>✗</td><td>√</td><td>√</td><td>✗</td><td>✗</td><td>✗</td><td>SIM</td><td></td><td>Accuracy, MRS</td></tr><tr><td>MemoryAgentBench</td><td>130</td><td>207</td><td>1.44M</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>✗</td><td>√</td><td>√</td><td>SIM</td><td></td><td>Accuracy, F1, AR, TTL, LRU, SF</td></tr><tr><td>LongMemEval</td><td>50K</td><td>500</td><td>1.5M</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>MIX</td><td></td><td>JUDGE, Recall@K, NDCG@K</td></tr><tr><td>HaluMem</td><td>1,387</td><td>3,467</td><td>1M</td><td>√</td><td>√</td><td>√</td><td>√</td><td>✗</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>MIX</td><td></td><td>MA, MI, FMR</td></tr><tr><td>PersonaMem</td><td>60</td><td>~6K</td><td>1M</td><td>√</td><td>√</td><td>√</td><td>✗</td><td>√</td><td>√</td><td>√</td><td>✗</td><td>√</td><td>✗</td><td>SIM</td><td></td><td>Accuracy</td></tr><tr><td>PrefEval</td><td>-</td><td>3,000</td><td>100K</td><td>√</td><td>√</td><td>√</td><td>√</td><td>✗</td><td>√</td><td>√</td><td>✗</td><td>√</td><td>√</td><td>MIX</td><td></td><td>JUDGE, Accuracy</td></tr><tr><td>MemBench</td><td>65K</td><td>53K</td><td>100K</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>✗</td><td>MIX</td><td></td><td>Accuracy, Capacity, Efficiency</td></tr><tr><td>MemoryBench</td><td>20K</td><td>-</td><td>-</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>✗</td><td>√</td><td>√</td><td>MIX</td><td></td><td>Accuracy, F1, JUDGE</td></tr><tr><td>ConvoMem</td><td>300</td><td>75,335</td><td>3M</td><td>√</td><td>√</td><td>√</td><td>√</td><td>✗</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>SIM</td><td></td><td>Accuracy</td></tr></table>

衡量识别未知或不可回答问题、冲突或虚假前提，并通过在所需信息从未被陈述时明确说“我不知道”等方式避免捏造。

表 4 中的一个关键模式是，MR 与 UP 是覆盖最一致的能力，反映以用户 memory 为主导的框架：从长对话中 retrieval 用户相关事实并在之后使用。相比之下，操作性能力的定义远不那么统一。MSC（Xu et al., 2022a）与 DuLeMon（Xu et al., 2022b）等早期长对话 benchmark 强调 multi-session 连贯性与人设使用，但其评估严重依赖基于相似度或基于生成的指标（例如 BLEU、Distinct-n、Perplexity、ROUGE），对 memory 的隔离较弱。流畅性与通用有帮助性可能掩盖错误的回忆，使 FE、UR 与 FR 难以归因。较新的 benchmark 日益转向通过定义特定任务类型或评估来实现机制可归因的评估。MemoryBank（Zhong et al., 2024）与 HaluMem（Chen et al., 2025a）引入显式 memory record 与操作级搜索，将抽取、更新与 memory 完整性失败转化为可测量目标。LongMemEval（Wu et al., 2025b）通过按 memory capability 显式分类问题类型，进一步加强归因，使失败能够更清晰地定位到时间推理、更新或弃答行为。然而，CS 与 FR 在当前 benchmark 设计中仍相对评估不足、系统性较弱。compression 仅在少数 benchmark 中被显式处理（Hu et al., 2025c），选择性 forgetting 或保留（Jia et al., 2025b）常常是部分的或缺失的，尽管它们对在有限 memory 预算与不断演化的用户状态下运行的 long-horizon 助手至关重要。AB 的要求也不一致（Ai et al., 2025; Jiang et al., 2025a）。只有少数 benchmark 明确奖励在证据缺失时弃答，留下了评估安全 memory 行为的空白——此类行为可防止自信的幻觉。

表 4 中的评估遵循几个主要方面，反映 benchmark 所提供的评估程度。第一，许多 benchmark 将评估简化为对 ground truth 问题的答案级正确性，报告准确率与 F1（例如 PerLTQA（Du et al., 2024）、LoCoMo（Maharana et al., 2024）、DialSim（Kim et al., 2024a）、PersonaMem（Jiang et al., 2025a）、MemoryAgentBench（Hu et al., 2025c）），并在任务被明确框定为选择支撑 memory 而非生成自由文本时，使用 Recall@K 或排序相关性指标（MAP/NDCG@K）等 retrieval 式评分（例如 PerLTQA（Du et al., 2024）、LongMemEval（Wu et al., 2025b））。第二，若干 user-centric 的 benchmark 引入超越最终答案、直接评估 memory system 行为的 memory 特定评估。HaluMem 报告 memory 准确率与完整性以及虚假 memory 率，以量化幻觉或错误 memory operation（Chen et al., 2025a），LOCCO（Jia et al., 2025b）报告 memory 保留（MRS），MemBench（Tan et al., 2025a）显式衡量容量与效率，以捕捉固定 memory 预算下的性能与成本权衡。第三，当输出开放式或参考答案不足时，benchmark 日益依赖 LLM 作为评判者来评分响应正确性或偏好遵循（例如 LongMemEval（Wu et al., 2025b）、PrefEval（Zhao et al., 2025c）与 MemoryBench（Ai et al., 2025））。与精确匹配评分相比，基于评判者的评估将覆盖扩展到现实助手行为，但对评估者模型与评分细则更敏感。

## 7.2.2 Agent-Centric Evaluation Benchmarks

agent-centric 的 benchmark 将基础模型作为半自主 agent 来评估，它必须在环境中执行多步动作以达成明确指定的目标，而非仅对静态 prompt 产生响应。这些 benchmark 通常提供任务规范（例如带约束的初始状态）以及客观成功检查器，并用端到端指标总结表现，例如文本问答任务的 Accuracy/F1 或交互环境的成功率（SR）。由于正确性由环境状态定义，目标结果在很大程度上与用户无关：在相同任务设置下，不同用户发出相同请求应获得相同的完成信号，即使 agent 遵循不同轨迹（Trivedi et al., 2024; Zhou et al., 2024）。

我们在表 5 中总结常用的 agent-centric benchmark。除了按 Env 与 Interact 标注每个 benchmark 之外，我们进一步标注 (i) 资源类型，表示任务世界与证据是用真实世界数据还是模拟数据、或两者混合构建；(ii) benchmark 最直接考察的核心 agent 能力（Abilities）。我们定义一组常用于刻画 agent 与 memory benchmark 的核心能力标签：TEMP（对事件顺序与时间依赖的时间/序列推理）、STATE（跨多步交互跟踪并更新环境/任务状态）、GROUND（将自然语言指令落地为具体环境目标/动作）、PLAN（规划并重规划通向目标的多步动作）、TOOL（选择并正确调用工具/API 以解决子任务）、MHOP（组合多条证据的多跳推理）、DIAL（目标导向的对话管理，例如澄清与跨轮一致性）、DEBUG、CODEGEN 与 PATCH（在软件工程环境中诊断失败、生成新代码与修复现有代码）；可选地，TTL 表示测试时学习，即 agent 通过在 memory 积累经验而非更新参数来改进后续表现。在这些工作中，memory 被视为用于跨 session 知识转移与经验共享的工具与模块，使 agent 能够在 long-horizon 与有限 context window 中保存中间发现、工具输出与状态更新，以提升下游任务完成能力。

跨环境而言，agent-centric 的评估覆盖 TEXT/WEB 信息查找（Yang et al., 2018; Trivedi et al., 2022; Deng et al., 2023; Yao et al., 2022; Mialon et al., 2024; Wei et al., 2025a）、OS/APP 计算机使用（Xie et al., 2024; Trivedi et al., 2024; Yao et al., 2025; Barres et al., 2025）、CODE 软件工程（Chen et al., 2021; Qiu et al., 2025b）、具身 ROBOT/GAME 控制（Shridhar et al., 2020; 2021; Fan et al., 2022）以及长格式 VIDEO/PAPER 工作流（Mangalam et al., 2023; Fu et al., 2025; Wu et al., 2024a; Starace et al., 2025）。这些环境引出不同的 memory 压力。文本与多跳问答强调对中间事实的证据跟踪与状态记账（Ho et al., 2020; Trivedi et al., 2022）。网页、桌面与应用设置强调 episodic 动作 memory。foundation agent 必须记住访问过的页面、填写过的字段、下载的文件、先前的工具输出、交互期间发现的约束，并避免冗余探索（Deng et al., 2023; Zhou et al., 2024; Yao et al., 2022）。代码与论文工作流需要 working memory，例如文件、补丁、假设与实验日志，以支持跨阶段连续性（Starace et al., 2025; Miao et al., 2025）。这些要求使 compression、选择与 retrieval 保真度对完成任务至关重要（Jimenez et al., 2024; Qiu et al., 2025a）。视频 benchmark 还测试长片段上的 sensory memory，其中关键线索可能在提问之前很久就出现（Fu et al., 2025; Wu et al., 2024a）。随着 benchmark 变得更真实、更 long-horizon，foundation agent 无法在 prompt 中保留所有任务相关 context，而必须通过显式 memory operation 外化状态，以随时间保存与 retrieval 关键信息。

表 5：agent-centric 的任务 benchmark 概览（§7.2.2）。每个 benchmark 按 Env、Interact、Resource、Abilities 与 Evaluation 标注。Env——TEXT：文本/文档；WEB：网页；OS：操作系统/桌面；APP：应用/以 API 为中心；CODE：代码/软件工程；ROBOT：具身机器人；GAME：游戏/模拟；VIDEO：视频（长格式）；PAPER：科学论文/研究。Interact——QA：问答；MT：多轮；GUI：图形界面；API：工具/API 调用；EXEC：基于执行；MM：多模态；ACT：动作/控制。Resource——REAL：真实世界；SIM：模拟/合成；MIX：真实与模拟混合。Abilities——MHOP：多跳推理；PLAN：规划/行动；STATE：状态跟踪；GROUND：落地；TOOL：工具使用；DEBUG：调试；CODEGEN：代码生成；PATCH：补丁/修复；TEMP：时间推理；DIAL：对话管理；TTL：测试时学习。Evaluation——SR：成功率/解决率；PR：通过率；GC：目标完成；RR：解决率；LCCS：最长连续正确序列。

<table><tr><td>名称</td><td>#数据</td><td>环境</td><td>交互</td><td>资源</td><td>核心能力</td><td>链接</td><td>评估</td></tr><tr><td>HotpotQA</td><td>113K</td><td>TEXT</td><td>QA</td><td>REAL</td><td>MHOP, STATE</td><td>Github</td><td>Accuracy, F1</td></tr><tr><td>2WikiMultiHopQA</td><td>193K</td><td>TEXT</td><td>QA</td><td>REAL</td><td>MHOP, STATE</td><td>Github</td><td>Accuracy, F1</td></tr><tr><td>MuSiQue</td><td>25K</td><td>TEXT</td><td>QA</td><td>REAL</td><td>MHOP, STATE</td><td>Github</td><td>F1</td></tr><tr><td>HLE</td><td>2.5K</td><td>TEXT</td><td>QA</td><td>REAL</td><td>MHOP, STATE</td><td>Website</td><td>Accuracy, RMSE</td></tr><tr><td>BrowseComp</td><td>1,266</td><td>WEB</td><td>QA, GUI</td><td>REAL</td><td>PLAN, TOOL, MHOP, STATE</td><td>Website</td><td>Accuracy, PR</td></tr><tr><td>Mind2Web</td><td>2.35K</td><td>WEB</td><td>GUI</td><td>REAL</td><td>GROUND, PLAN, STATE</td><td>Website</td><td>Accuracy, F1, SR</td></tr><tr><td>WebArena</td><td>812</td><td>WEB</td><td>GUI</td><td>SIM</td><td>GROUND, PLAN, STATE</td><td>Website</td><td>SR</td></tr><tr><td>WebShop</td><td>12.1K</td><td>WEB</td><td>GUI</td><td>MIX</td><td>GROUND, PLAN, STATE</td><td>Github</td><td>Task Score, SR</td></tr><tr><td>GAIA</td><td>466</td><td>WEB</td><td>QA, GUI</td><td>REAL</td><td>TOOL, MHOP, PLAN, STATE</td><td>Website</td><td>Accuracy, SR</td></tr><tr><td>OSWorld</td><td>369</td><td>OS</td><td>GUI, MM</td><td>REAL</td><td>GROUND, PLAN, STATE</td><td>Website</td><td>SR</td></tr><tr><td>AppWorld</td><td>750</td><td>APP</td><td>API, MT</td><td>SIM</td><td>TOOL, CODEGEN, PLAN, STATE</td><td>Website</td><td>SR</td></tr><tr><td>τ-Bench</td><td>165</td><td>APP</td><td>API, MT</td><td>SIM</td><td>TOOL, PLAN, STATE, DIAL</td><td>Github</td><td>Pass^1, Pass^k</td></tr><tr><td>τ-Bench2</td><td>2.3K</td><td>APP</td><td>API, MT</td><td>SIM</td><td>TOOL, PLAN, STATE, DIAL</td><td>Github</td><td>Pass^1, Pass^k</td></tr><tr><td>HumanEval</td><td>164</td><td>CODE</td><td>EXEC</td><td>REAL</td><td>CODEGEN, DEBUG</td><td>Github</td><td>Pass@1</td></tr><tr><td>SWE-Bench</td><td>2.3K</td><td>CODE</td><td>EXEC</td><td>REAL</td><td>PATCH, DEBUG, STATE</td><td>Website</td><td>RR</td></tr><tr><td>LoCoBench</td><td>8K</td><td>CODE</td><td>EXEC</td><td>SIM</td><td>CODEGEN, PATCH, DEBUG, STATE</td><td>Github</td><td>Multi-metric</td></tr><tr><td>LoCoBench-Agent</td><td>8K</td><td>CODE</td><td>EXEC</td><td>SIM</td><td>TOOL, PLAN, CODEGEN, PATCH, DEBUG, STATE</td><td>Github</td><td>Multi-metric</td></tr><tr><td>PaperBench</td><td>20</td><td>PAPER</td><td>EXEC, MT</td><td>REAL</td><td>TOOL, PLAN, CODEGEN, DEBUG, STATE</td><td>Website</td><td>Replication Score</td></tr><tr><td>RECODE-H</td><td>102</td><td>PAPER</td><td>EXEC, MT</td><td>REAL</td><td>CODEGEN, PATCH, DEBUG, DIAL, STATE</td><td>Github</td><td>Recall, PR</td></tr><tr><td>ALFRED</td><td>25.7K</td><td>ROBOT</td><td>ACT, MM</td><td>SIM</td><td>GROUND, PLAN, STATE</td><td>Website</td><td>SR, GC</td></tr><tr><td>ALFWorld</td><td>3.8K</td><td>ROBOT</td><td>ACT, MT</td><td>SIM</td><td>PLAN, STATE, GROUND</td><td>Website</td><td>SR</td></tr><tr><td>MineDojo</td><td>3.1K</td><td>GAME</td><td>ACT, MM</td><td>MIX</td><td>PLAN, STATE, GROUND</td><td>Website</td><td>SR</td></tr><tr><td>EgoSchema</td><td>5,031</td><td>VIDEO</td><td>QA, MM</td><td>REAL</td><td>TEMP</td><td>Website</td><td>Accuracy</td></tr><tr><td>Video-MME</td><td>2,700</td><td>VIDEO</td><td>QA, MM</td><td>REAL</td><td>TEMP</td><td>Website</td><td>Accuracy</td></tr><tr><td>LongVideoBench</td><td>6.7K</td><td>VIDEO</td><td>QA, MM</td><td>REAL</td><td>TEMP</td><td>Website</td><td>Accuracy</td></tr><tr><td>MT-Mind2Web</td><td>720</td><td>WEB</td><td>GUI, MT</td><td>REAL</td><td>GROUND, PLAN, STATE, DIAL</td><td>Github</td><td>Accuracy, F1, SR</td></tr><tr><td>MPR</td><td>10.8K</td><td>TEXT</td><td>QA</td><td>SIM</td><td>MHOP, STATE</td><td>Github</td><td>Accuracy</td></tr><tr><td>StoryBench</td><td>397</td><td>GAME</td><td>MT, ACT</td><td>SIM</td><td>PLAN, STATE, TEMP</td><td>-</td><td>Accuracy, LCCS</td></tr><tr><td>Evo-Memory</td><td>~3,700</td><td>TEXT</td><td>QA, MT</td><td>MIX</td><td>TTL, PLAN, STATE</td><td>-</td><td>Accuracy, SR</td></tr><tr><td>LifelongAgentBench</td><td>1,396</td><td>APP, OS</td><td>API, MT</td><td>SIM</td><td>TTL, TOOL, PLAN, STATE</td><td>Website</td><td>SR</td></tr><tr><td>OdysseyBench</td><td>602</td><td>APP</td><td>GUI, MT</td><td>MIX</td><td>PLAN, TOOL, STATE, TEMP</td><td>Github</td><td>PR</td></tr></table>

表 5 中 benchmark 的评估方法主要分为几类。TEXT 的答案级 Accuracy/F1（Trivedi et al., 2022; Phan et al., 2025），交互式 WEB/OS/APP/ROBOT/GAME 的基于目标 SR、GC（Xie et al., 2024; Trivedi et al., 2024; Shridhar et al., 2020; 2021; Fan et al., 2022），以及 CODE 的以执行为中心的指标（例如 Pass@1、RR）（Jimenez et al., 2024; Qiu et al., 2025a）。对以 memory 为中心的分析，另有两个维度至关重要：(1) 依赖距离——所需信息与其后续使用之间相隔多远，例如轮内、跨轮或跨 session；(2) 交互下的 memory 正确性——随着环境演化，存储条目是否保持忠实、不矛盾且策略一致。这促使我们用 memory 敏感的度量补充端到端成功，例如：(i) 对所需事实或工具输出的 retrieval 忠实度与覆盖；(ii) 状态跟踪中的错误模式（漂移、遗漏、矛盾）；(iii) 中断下的持久性（长间隔后恢复）；(iv) 效率权衡（memory 大小、更新频率与 retrieval 成本）。我们预期下一代 benchmark 将超越单一端到端准确率或成功率，转而纳入 memory 相关指标，使评估也能归因于 memory mechanism，而非短时程 prompt 或偶然启发式。

## 8 应用

memory 将 LLM 转变为动态、持久的 agent，代表了近期研究中的根本转变。当在复杂真实世界场景中实现时，agent memory 已不仅作为存储工具出现，而是作为支持连续性、学习与个性化的认知 substrate，将 agent 的过往经验与未来行动连接起来。近期工作广泛研究了 LLM agent 中 memory 赋能的能力，其存储、操作与管理 memory 的方式差异显著。为提供 memory design 改进如何提升进一步能力的洞见，本节讨论并总结教育、科学研究、游戏与模拟、机器人、医疗保健、对话系统、工作流自动化、软件工程、在线流媒体与推荐、信息搜索、金融与会计以及法律与咨询领域的近期代表性工作。应用领域如图 8 所示，总结见表 6。

**教育。** 教育 agent 需要跨越长时间段的持续、个性化交互，使 memory 对于跟踪学习者进度、调整教学并维持教学连贯性至关重要（Chu et al., 2025）。没有 memory，agent 将每次交互视为孤立事件，无法基于学生先前知识继续构建，也无法维持教学一致性。近期模型展示了向更精细 memory module 的转变。例如，LOOM（Cui et al., 2025a）利用学习者 memory 图，将教育概念与先决依赖关系映射起来，以促进个性化课程生成。Agent4Edu（Gao et al., 2025b）显式复现艾宾浩斯 forgetting 曲线，以模拟教师培训中的知识衰减。WebCoach（Liu et al., 2025b）使用持久跨 session memory 实现 self-evolving 的教学指导。这些系统表明，在教育领域，memory 与其说是历史日志，不如说是学生的认知数字孪生（Zheng et al., 2022）。未来工作应走向可互操作的 memory 协议，使学习者的认知画像能够跨不同教育平台持久存在，有效创建其智力发展的演化记录。

**科学研究。** 科学研究代表一个前沿领域，其过程漫长且昂贵，要求 agent 综合大量文献、管理来源并跨多阶段工作维持推理连续性。在近期研究中，General Agentic Memory（GAM）（Yan et al., 2025a）采用专门的 researcher agent，在通用页面存储上进行深度研究，为复杂多跳推理实现动态 context 重建。IterResearch（Chen et al., 2025c）维护一个工作区，仅保留演化中的报告与即时结果，以防止 context 窒息。MirrorMind（Zeng et al., 2025）通过层次化架构模拟集体智能，retrieval 特定认知风格与知识库。AISAC（Bhattacharya & Som, 2025）实现混合 memory，将语义 retrieval 与结构化 SQLite 日志相结合以支持可复现性。这些研究 agent 体现了一种范式转变：memory 作为研究过程的验证层，维持结论如何达成的透明谱系。未来系统将从孤立的研究助手演化为实验室规模的集体智能，多个 agent 共享某一科学领域统一且不断演化的 knowledge graph，并在新论文发表与综合时实时更新。

表 6：代表性 agent memory 应用总结。

<table><tr><td>应用</td><td>memory utilization</td><td>工作</td></tr><tr><td>教育</td><td>跟踪学习者进度并模拟知识衰减，以提供个性化教学指导。</td><td>LOOM (Cui et al., 2025a), Agent4Edu (Gao et al., 2025b), WebCoach (Liu et al., 2025b), CAM (Li et al., 2025d), Classroom Simulacra (Xu et al., 2025b), TeachTune (Jin et al., 2025a), EduAgent (Xu et al., 2024a), EvaAI (Lagakis &amp; Demetriadis, 2024), OATutor (Pardos et al., 2023), MEDCO (Wei et al., 2024)</td></tr><tr><td>科学研究</td><td>综合大量文献，并在多阶段发现过程中维持推理来源。</td><td>IterResearch (Chen et al., 2025c), GAM (Yan et al., 2025a), MirrorMind (Zeng et al., 2025), AISAC (Bhattacharya &amp; Som, 2025), Lee et al. (2024), ChemDFM (Zhao et al., 2025e), AI-coscientist (Got-tweis et al., 2025), SciAgents (Ghafarollahi &amp; Buehler, 2025), Agent Laboratory (Schmidgall et al., 2025), NovelSeek (Team et al., 2025)</td></tr><tr><td>游戏与模拟</td><td>通过 episodic memory 实现自下而上的技能获取与复杂社会动态的涌现。</td><td>Voyager (Wang et al., 2025c), GITM (Zhu et al., 2023), Generative Agents (Park et al., 2023), GameGPT (Chen et al., 2023), M2PA (Zhou et al., 2025b), Jiang et al. (2025d), WarAgent (Hua et al., 2023), S3 (Gao et al., 2023), AvalonBench (Light et al., 2023), Mosaic (Liu et al., 2025c)</td></tr><tr><td>机器人</td><td>通过维护空间图与轨迹摘要，将高层推理与底层控制连接起来。</td><td>Memo (Gupta et al., 2025), MG-Nav (Wang et al., 2025b), JARVIS-1 (Wang et al., 2024p), KARMA (Wang et al., 2025t), VIPeR (Ming et al., 2025), SAM 2 (Ravi et al., 2024), LRLL (Tziafas &amp; Kasaei, 2024), VideoAgent (Fan et al., 2024), Kim et al. (2023a), RAP (Kagaya et al., 2024), GridMM (Wang et al., 2023d)</td></tr><tr><td>医疗保健</td><td>维护生理趋势与情绪状态的纵向记录，以建立用户信任与依从性。</td><td>TheraMind (Hu et al., 2025a), DAM (Lu &amp; Li, 2025), Mem-PAL (Huang et al., 2025d), ReSurgSAM2 (Liu et al., 2025d), CARE-AD (Li et al., 2025e), AgentMD (Jin et al., 2025b), MedConMA (Wang et al., 2025k), MDAgents (Kim et al., 2024b), MedAgents (Tang et al., 2024), ChatCAD (Tang et al., 2025a)</td></tr><tr><td>对话系统</td><td>管理 context window 约束与人设一致性，以模拟持久的人类式关系。</td><td>A-Mem (Xu et al., 2025e), MemGPT (Packer et al., 2023), O-Mem (Wang et al., 2025i), MemoChat (Lu et al., 2023), Mem0 (Chhikara et al., 2025), SEAL (Wang et al., 2025d), LiCoMemory (Huang et al., 2025e), Lu &amp; Li (2025), Terranova et al. (2025), LightMem (Fang et al., 2025a), RGMem (Tian et al., 2025)</td></tr><tr><td>工作流自动化</td><td>归纳可复用工作流模板，并从成功执行历史中学习工具使用模式。</td><td>AWM (Wang et al., 2025v), ToolMem (Xiao et al., 2025), Synapse (Zheng et al., 2024), WebArena (Zhou et al., 2024), Wheeler &amp; Jeunen (2025), Wang et al. (2025u), WALT (Prabhu et al., 2025), Mobile-agent-v2 (Wang et al., 2024c), AutoAgents (Chen et al., 2024a), SIT-Graph (Li et al., 2025f)</td></tr><tr><td>软件工程</td><td>维护全局代码 context 并回忆失败轨迹，以改进多文件调试与开发。</td><td>MetaGPT (Hong et al., 2024), ChatDev (Qian et al., 2024a), SWE-bench (Jimenez et al., 2024), SWE-Effi (Fan et al., 2025c), TroVE (Wang et al., 2024o), Self-organized agents (Ishibashi &amp; Nishimura, 2024), Openhands (Wang et al., 2025n), Masai (Arora et al., 2024), DeepCode (Li et al., 2025m)</td></tr><tr><td>在线流媒体与推荐</td><td>将高吞吐多模态信息流经 distillation 形成持久表示，以识别长程时间模式。</td><td>WorldMM (Yeo et al., 2025b), GCAgent (Yeo et al., 2025a), XMem++ (Bekuzarov et al., 2023), VideoScan (Li et al., 2025c), Xiong et al. (2025b), Qian et al. (2024b), VideoLLM-online (Chen et al., 2024c), VideoLLM-MoD (Wu et al., 2024c), Di et al. (2025)</td></tr><tr><td>信息搜索</td><td>将静态 retrieval 转变为主动工作区，用于综合冲突报告并跟踪搜索来源。</td><td>AgentFold (Ye et al., 2025b), MemSearcher (Yuan et al., 2025a), MoM (Zhao et al., 2025a), ReSum (Wu et al., 2025d), Memento (Zhou et al., 2025a), MLP Memory (Wei et al., 2025c), MemAgent (Yu et al., 2025b), Wang et al. (2025p), MemoryLLM (Wang et al., 2024l)</td></tr><tr><td>金融与会计</td><td>在波动市场周期中维持战略一致性，并平衡定量信号与定性历史先例。</td><td>FinCon (Yu et al., 2024a), FinMem (Yu et al., 2025e), QuantAgent (Wang et al., 2024g), FLAG-Trader (Xiong et al., 2025a), Investor-Bench (Li et al., 2025b), TradingAgents (Xiao et al., 2024), Trading-GPT (Li et al., 2023b), Open-FinLLMs (Huang et al., 2024a)</td></tr><tr><td>法律与咨询</td><td>管理多文档来源，并在长期案件历史中将冲突法规综合为连贯建议。</td><td>MALR (Yuan et al., 2024b), StaffPro (Maritan, 2025), Blair-Stanek et al. (2025), LegalMind (Vara et al., 2025), CaseGPT (Yang, 2024), Dallma (Westermann, 2024), AgentCourt (Chen et al., 2025b), Legal-GPT (Shi et al., 2024), Feat (Shen et al., 2025)</td></tr></table>

![](../assets/arxiv-2602.06052-fig8.jpg)  
图 8：foundation agent memory 系统的应用。该图介绍 foundation agent memory 系统的一般应用领域，包括教育、科学研究、游戏与模拟、机器人、对话系统、医疗保健、工作流自动化、软件工程、在线流媒体与推荐、信息搜索、金融与会计以及法律与咨询。


**游戏与模拟。** 在开放式游戏环境与模拟中，memory 支持技能获取、空间探索与复杂社会动态的涌现。agent 必须利用 procedural memory 保留已学技能，并利用 episodic memory 维持可信的社会历史。例如，Voyager（Wang et al., 2025c）将成功动作作为可执行代码存储在技能库中，以实现能力的复利增长。GITM（Zhu et al., 2023）采用层次化文本 memory，其中规划器记录结构化子目标摘要。Generative Agents（Park et al., 2023）使用 memory 流，agent 通过反思将高层洞见综合为关系与计划。GameGPT（Chen et al., 2023）将 memory 用作 multi-agent 游戏开发的共享状态，管理版本控制与冲突解决。在这些工作中，memory module 使行为从经验积累中自下而上涌现，而非自上而下编程。该领域的下一个前沿可能是社会对齐与 forgetting 机制的发展。随着模拟长时间运行，agent 应模仿类人的 memory 衰减，确保人设有机演化，而不被无穷琐碎历史数据的噪声所瘫痪。

**机器人。** 在物理世界中运行的具身 agent 面临部分可观测性挑战（Fung et al., 2025），需要 memory 将视觉输入与语义概念连接起来，并随时间维持空间表示。memory 必须被压缩，同时细节足够丰富，以支持非静态环境中的导航与操作。Memo（Gupta et al., 2025）引入周期性总结 token，压缩轨迹以支持 long-horizon 导航。MG-Nav（Wang et al., 2025b）构建带地标区域的空间 memory 图，而非稠密点云，模仿人类导航。JARVIS-1（Wang et al., 2024p）以多模态 memory scaling 具身能动性，根据视觉与语义相似度检索经验。这些应用表明，memory 是高层推理与底层控制之间的桥梁。未来研究应聚焦多模态 memory consolidation，使 agent 能够基于 procedural memory 中存储的过往成功与失败，模拟物理 affordance。

**医疗保健。** 在医疗保健领域，memory 使 agent 能够跟踪纵向健康趋势、情绪轨迹与干预效果。TheraMind（Hu et al., 2025a）引入双回路架构，将即时响应与战略性跨 session memory update 分离，以调整治疗策略。DAM（Lu & Li, 2025）将 memory 单元视为情感极性上的置信分布，以实现稳定的概率情绪建模。Mem-PAL（Huang et al., 2025d）采用 H2Memory 架构，区分客观生理日志与主观对话，以推断健康指标相关性。agent memory 的部署表明，情感连续性与临床准确性同样关键，可测量地提升用户信任与依从性。然而，该领域面临隐私与伦理挑战。未来架构应通过设计机制实现隐私保护 memory，在长期 memory utility 与患者保密义务之间取得平衡。

**对话系统。** 对通用助手而言，memory 营造出持续个性化关系的印象，在管理 context window 的同时提供对话历史。该领域聚焦于主动管理保留与 context window 约束之间的权衡。MemGPT（Packer et al., 2023）引入 context 管理系统，显式地在主 context 与外部 context 之间移动数据，以支持更长对话。O-Mem（Wang et al., 2025i）使用三分量 memory 抽取并更新整体用户画像，以实现对齐响应。MemoChat（Lu et al., 2023）采用指令 fine-tuning 训练模型撰写结构化备忘录，以改善长程一致性。这些对话架构展示了向操作系统级 memory management 的转变，agent 充当管理自身资源的内核。对话系统的未来在于自我优化 memory。下一代 agent 将不再依赖固定启发式规则决定记住什么，而很可能学习个性化 memory policy。

**工作流自动化。** LLM agent 也作为助手，通过工作流自动化提升生产力。自动化 agent 主要编排多步流程、协调工具使用，并根据执行反馈调整流程。memory mechanism 使 agent 能够积累程序知识、优化工作流，并在复杂自动化流水线中维持任务 context。AWM（Wang et al., 2025v）从成功轨迹中归纳可复用工作流模板，作为 parametricprocedural memory。ToolMem（Xiao et al., 2025）实现工具使用模式的 semantic memory，学习适用于特定任务类型的有效工具。在 WebArena（Zhou et al., 2024）上，保留网页交互序列 episodic memory 的 agent 显著优于无 memory 基线。Synapse（Zheng et al., 2024）引入轨迹作为范例的 prompt（trajectory-as-exemplar prompting），将成功控制序列存储为 episodic memory 以支持类比推理。在这些工作中，memory 的 consolidation 促进了从僵硬脚本执行向自适应程序学习的转变，大幅提升稳健性与效率。未来系统将不仅遵循人类定义的操作流程，还应基于长期执行日志主动重写自身指令，从简单任务执行者演化为流程架构师，自主精炼企业工作流以实现最大效率。

**软件工程。** 在软件工程中，agent 在复杂代码库中运行，需要 long-horizon 推理、多文件协调与累积调试经验。memory 使这些 agent 能够维持代码 context、从实现尝试中学习，并在大规模仓库中导航。MetaGPT（Hong et al., 2024）为开发工作流实现 procedural memory，同时维护项目规范的共享 semantic memory。ChatDev（Qian et al., 2024a）以开发迭代的 episodic memory scaling 这一做法，从调试 session 中学习。SWE-bench（Jimenez et al., 2024）上的评估报告称，memory mechanism 通过在多文件编辑中维持 context 并利用先前调试经验，提升问题解决率。关键的是，有效的编码 agent 不仅生成代码，还回忆先前失败与修复的轨迹，以在通过单元测试上取得更高成功率。该领域的未来应用很可能从本地项目 memory 走向共享、匿名的知识仓库，分布式编码 agent 向通用算法解决方案与错误补丁池贡献并查询，加速自动化软件开发的全球步伐。

**在线流媒体与推荐。** 在在线流媒体与推荐系统时代，agent 处理高吞吐多模态输入，其中信息相关性随时间动态变化。memory 使 agent 能够维持时间一致性，并识别跨视频帧与用户交互的长程模式。例如，WorldMM（Yeo et al., 2025b）利用动态多模态 memory storage 视觉—语言特征，以对长时视频流进行复杂推理。GCAgent（Yeo et al., 2025a）引入双结构 episodic memory，将图示性知识与叙事序列分离，以实现结构化视频理解。类似地，Xiong et al. (2025b) 实现 memory augmentation 的知识缓冲，支持带保留 context 的多轮交互。这些应用表明，在流式语境中，memory 充当时间过滤器，将瞬态数据经 distillation 形成持久表示。未来研究应聚焦 forgetting 感知的推荐 memory，能够区分用户短暂兴趣与长期偏好，在实时信息流中优化新颖性与相关性之间的平衡。

**信息搜索。** 除简单 retrieval 之外，信息搜索 agent 必须综合冲突报告、跟踪演化中的报道，并在不丢失推理深度的情况下管理庞大文档空间。memory 作为组织框架，将静态搜索结果转变为知识综合的主动工作区。AgentFold（Ye et al., 2025b）通过主动 context 管理应对 long-horizon 网页导航，折叠无关轨迹以防止溢出，同时保留关键发现。MemSearcher（Yuan et al., 2025a）采用 RL 进行联合搜索与 memory management。MoM（Zhao et al., 2025a）利用场景感知 memory，将查询动态路由到专门 memory store。此外，Rajesh et al. (2025) 将 RAG 与 episodic memory 连接起来，维护搜索过程本身的仓库。这些系统表明，有效的搜索不仅是找到数据，更是管理搜索轨迹的认知负荷。下一代信息搜索 agent 很可能演化为协作 memory structure，其中多个 agent 核实事实，并响应突发新闻周期更新 agent 之间的共享信念图。

**金融与会计。** 金融领域的特征是高频波动、定量数据与定性新闻的混合，以及对长期战略一致性的关键需求。memory 在这里至关重要，因为交易与会计要求 agent 处理实时信号、回忆历史市场状态，并维持持久的交易性格以避免反复无常的决策。近期工作为此引入了专门架构。FinMem（Yu et al., 2025e）实现分层 memory system，将即时市场观察与长期投资经验分离，使 agent 能够随时间精炼其人设与风险画像。FinCon（Yu et al., 2024a）利用 multi-agent 设置，其中 memory 充当概念性言语强化的仓库，使系统能够通过反思性反馈回路从过往金融决策中学习。QuantAgent（Wang et al., 2024g）进一步通过 self-improvement 机制寻求投资“圣杯”，将成功轨迹存储为 procedural memory 以供未来策略精炼。尽管有这些收益，主要挑战仍是金融 memory 中的信噪比。agent 必须学会区分短暂市场波动与根本性转变。未来研究应探索 forgetting 感知的金融 agent，能够修剪过时经济假设，同时保留核心风险管理原则。

**法律与咨询。** 在法律与咨询服务中，agent 必须处理大量异构文档，其中每项主张的精确来源都是强制要求。memory 是使这些 agent 能够对长期案件进行多步推理的认知 substrate，确保建议与先前引用的法规或客户历史保持一致。例如，MALR（Yuan et al., 2024b）利用 multi-agent 框架，通过维护模拟法律专家协作辩论的交互历史来改善复杂法律推理。StafPro（Maritan, 2025）聚焦咨询侧，使用 memory 随时间刻画员工与项目需求，通过过往绩效数据的反馈回路实现动态人员配置。Blair-Stanek et al. (2025) 展示了 memory 在发现新颖税务最小化策略方面的力量：将数千页演化中的法规与判例法综合为持久推理图。该领域的核心挑战是幻觉 memory 的高风险。一个被记错的条款可能导致法律责任。未来方向很可能聚焦可验证 memory architecture，将每项 retrieval 洞见链接回经密码学签名的来源文档，确保最高级别的职业诚信与问责。

![](../assets/arxiv-2602.06052-fig9.jpg)  
图 9：foundation agent memory 的未来方向与挑战。该图突出未来 agent memory 工作的关键机会，包括面向 continual learning 与 self-evolving agent 的 memory、多人类—agent memory 组织、memory 基础设施与效率、终身个性化与可信 memory、面向多模态、具身与世界模型 agent 的 memory，以及真实世界 benchmark 与评估。每个方向都将一项挑战与一条有前景的研究路径配对。

## 9 未来方向

在前述分析的基础上，我们突出六项我们认为对 foundation agent memory 最具影响的开放挑战。图 9 将它们与我们认为每个方向最有前景的路径一起总结。

## 9.1 Memory for Continual Learning 与 Self-Evolving Agents

memory 赋能的 self-evolving agent 中的一个根本挑战在于管理跨任务内与跨任务时间尺度的 memory 动态。在任务内层面，agent 必须在严格 context window 约束下，持续决定从异构流（如工具输出、搜索结果、反馈信号与中间推理轨迹）中保留、压缩或丢弃哪些信息（Gao et al., 2025a）。现有系统在很大程度上依赖启发式 memory 控制器，使 memory evolution 与推理行为之间的内部耦合仍鲜有理解。在跨任务层面，agent 被期望 cross-episode 与任务分布积累经验（Wei et al., 2025d），但当前方法主要强调推理时复用，而非原则性整合与泛化。相比之下，经典 continual learning 方法聚焦于通过回放、正则化或参数隔离防止灾难性 forgetting（Rebufi et al., 2017; Lopez-Paz & Ranzato, 2017; Shin et al., 2017; Kemker & Kanan, 2018），但它们通常将 memory 视为知识保留的静态机制。这一框架对基于 agent 的系统并不足够，因为 memory 还必须跟踪演化中的交互状态、用户特定信息与程序行为。此外，从积累经验进行稳定的后训练适应仍探索不足，存在负迁移、失控漂移与语义不一致等未解决风险（Ke et al., 2025b）。

因此，未来研究应围绕更丰富、agent-centric 的 memory 概念重构 continual learning，整合 semantic、episodic 与 procedural 组件（Ke et al., 2025a; Sumers et al., 2023）。除显式文本日志之外，latent 与structured memory 表示为可扩展且高效的适应提供了有前景的方向，实现紧凑存储的同时保留因果与行为抽象。进展很可能需要从推理时启发式转向原则性后训练范式，利用积累的 agent 经验实现持续改进。这包括设计 consolidation 机制，选择性 distillation 长期知识、使演化中的 memory 与模型参数对齐，并在不牺牲可塑性的情况下减轻 forgetting。相应地，需要新 benchmark，不仅评估任务级保留，还评估持续适应、相关性感知 memory management，以及在非平稳目标与环境下的行为稳定性（Ke et al., 2024）。建立一个连接经典 continual learning 目标与structured memory design 的统一框架，仍是 self-evolvingfoundation agent 的关键开放方向。

## 9.2 Multi-Human-Agent Memory Organization

近期 multi-agent LLM 框架，例如 AutoGen（Wu et al., 2024b）与 AgentLite（Liu et al., 2024c），通过结构化消息传递与 prompt-driven 控制实现任务分解与基于角色的协调。在实践中，此类系统日益在人—agent 协作设置中运行，人工 agent 不仅与其他 agent 交互，还通过迭代反馈、纠正与委派与人类用户或监督者交互（Lu et al., 2025c; Zou et al., 2025b;c），benchmark 也开始在可配置的人类参与以及显式角色与权限结构下评估此类系统（Wu et al., 2026）。然而，尽管复杂性不断增长，协调在很大程度上仍是 episodic 且短暂的：交互被限定在单个任务实例内，任务完成后很少保留经验（Suzgun et al., 2025）。因此，agent—agent 与 human-agent 协作都被反复从头重建，限制了系统在重复任务或部署中适应交互策略、个性化行为或提升协作质量的能力。

实现交互实体（包括 foundation agent 与人类）之间持久且自适应的协作将引出长期研究问题（Han et al., 2024; Li et al., 2024c）。一个重要方向是协作（社会）memory，agent 保留关于协作者的经验，例如沟通偏好、领域专长、反馈模式或历史交互结果，使其能够随时间调整信号策略、校准信任并降低协调开销。同时，agent 可受益于角色特定工作流与 procedural memory，积累关于自身反复出现工作流的经验（Wang et al., 2025v），包括任务分解模式、执行策略与常见失败模式，使承担稳定功能角色的 agent 能够通过经验驱动的专门化逐步精炼行为。在此类多实体设置中引入持久 memory 还带来 memory 治理与协调挑战，包括所有权、访问、责任问题，以及如何处理分歧观点或人类纠正。解决这些问题对于防止失控的错误传播、以及在多 agent system 规模、异构性与任务复杂度扩展时维持可靠协作至关重要。

## 9.3 Memory Infrastructure 与 Efficiency

随着 foundation agent 日益部署于 long-horizon、交互式与开放式环境，memory 基础设施已成为核心效率瓶颈（Chhikara et al., 2025; Qiu et al., 2025b）。大多数现有 agent memory 设计仍以文本为中心，将 memory 视为不断增长的过往交互、摘要或 episodic log 集合，并将其检索并注入 prompt（Xu et al., 2025e; Zhong et al., 2024）。该策略虽可提升任务表现，却引入大量 token 开销，memory context 常扩展到数千 token，并表现出边际收益递减（Chhikara et al., 2025）。memory 成本的这种线性增长（Kwon et al., 2023）直接转化为更高的推理延迟与降低的可扩展性，尤其是在多轮或终身设置中。更根本地，当前方法将 memory 容量与 prompt 长度混为一谈，隐含假设更多 context 意味着更好推理。这一假设忽视了选择性保留、结构化访问与 experience consolidation 的需要。此外，memory 常通过总结或截断等启发式在外部管理，而非整合进 agent 的推理与学习过程。这些局限凸显一个核心挑战：如何设计 memory system，使 agent 能够在严格资源约束下高效保留、抽象与复用经验，而不依赖无界 context 扩展。

未来关于 memory 基础设施与效率的研究可被视为朝向日益抽象与整合的经验表示演进的过程。近期而言，一个有前景的方向是有组织的文本 memory，其中文本 memory 被显式结构化以实现高效访问，而非最大覆盖。近期工作探索了基于模式或图结构的 memory 表示（Edge et al., 2024; Chhikara et al., 2025），但这些努力主要面向推理准确率而非效率。一个开放机会是设计结构感知存储与面向精度的 retrieval 机制，仅暴露推理关键片段，最小化不必要的 context 注入。除文本组织之外，效率收益还可通过压缩 latent memory 实现：将 episodic、semantic 或 procedural 经验编码为紧凑向量表示，使其作为持久 memory 单元而非仅仅是相似度索引。在更深层的整合上，内化或 parametric memory 提供了通向恒定大小 memory 的路径，将长期经验吸收进内部状态或模型参数。MEM1（Zhou et al., 2025c）与 Mem-α（Wang et al., 2025q）等框架示例了这一转变：通过 RL 训练 agent 将 memory 的 consolidation、更新与丢弃作为推理过程本身的一部分，从而即便在 long-horizon 任务中也能实现有界 memory。实现这些方向还需要稳健的环境基础设施，能够支持受控多步交互与可扩展评估。NeMo Gym（NVIDIA, 2025）等平台将环境逻辑与训练解耦，并提供模块化奖励与验证服务，是该生态的必要组件。这些进展共同指向一个未来：memory 不再是外部 prompt 管理产物，而是与 agent 推理和决策共同演化的核心、学得子系统，通过整合 memory architecture 实现——结合结构化 latent representation（例如带可微读写接口的层次化向量表）、通过端到端 RL 或元学习目标对 memory 与策略的联合优化，以及根据任务相关性、不确定性估计与长期效用动态分配、压缩与退役 memory 单元的自适应 memory 控制器。

## 9.4 Lifelong Personalization 与 Trustworthy Memory

终身个性化旨在使 foundation agent 具备跨 session、任务与扩展时间范围持续适应单个用户的能力（Wang et al., 2024i）。与依赖静态用户画像或瞬态 context 信号的传统个性化方法不同，该设置要求 agent 维护演化中的用户表示，捕捉渐进偏好变化、长期目标与行为规律。尽管近期关于持久 memory 与动态用户建模的努力已取得初步进展（Zhong et al., 2024; Tan et al., 2025c; Zhang et al., 2025o），现有系统在很大程度上依赖交互历史的启发式聚合或非structured memory retrieval，限制了其 distillation 可靠、可解释且具因果根基的用户知识的能力（Pink et al., 2025）。此外，long-horizon 个性化在 memory 陈旧、概念漂移与 credit assignment 方面引入不小挑战：agent 必须决定哪些过往交互仍然相关、如何随时间协调冲突信号，以及如何防止过时偏好主导当前行为。这些问题还因可扩展性约束而加剧，因为天真地保留或回放长交互历史会导致过高的存储、retrieval 与推理成本，尤其是在真实世界常驻助手设置中部署时。

一个关键研究方向是设计可扩展且动态的 memory system，能够增量更新用户建模，同时在细粒度 episodic trace 与更高层抽象（如偏好、习惯或长期意图）之间架桥。有前景的方法包括：将短期 episodic buffer 与 distillation 语义用户画像分离的层次化 memory architecture（Tan et al., 2025c）、调节何时写入、压缩或覆盖用户信息的学得 memory 控制器（Zhang et al., 2025o），以及减轻分布偏移下 forgetting 的持续表示学习技术（De Lange et al., 2021; Parisi et al., 2019）。同时，该领域需要针对终身个性化的新评估 benchmark，从单轮准确率转向评估长期一致性、对偏好变化的适应性以及扩展交互下的稳健性（Xu et al., 2025e）。同样重要的是可信 memory 基础设施的发展。持久用户 memory 带来实质风险，包括隐私泄漏（Wang et al., 2025a）、memory 投毒（Tan et al., 2024b）与对抗性操纵（Dong et al., 2025），这些风险可能随时间静默累积。近期关于安全且可审计 memory module 的工作（Wei et al., 2025b; Wang et al., 2025a）强调需要用户可控机制，支持对存储 memory 的检查、编辑与撤销，并防御未授权访问与恶意写入。最终，在设计并评估终身个性化 foundation agent 时，稳健性、透明性与安全性应被视同一流目标，与适应性同等重要（Yu et al., 2025c）。

## 9.5 Memory for Multimodal、Embodied 与 World-Model Agents

下一代 foundation agent 的一个核心挑战在于设计 memory system，能够将异构感知流（包括视觉、音频、语言、触觉反馈与本体感觉信号）忠实表示、对齐并抽象为连贯内部状态（Bei et al., 2026）。尽管文本 memory mechanism 在 long-horizon 推理与个性化方面已取得显著成功（Xu et al., 2025e），现有方法在很大程度上假设单模态或以语言为主的表示。多模态 agent memory 的早期努力（Long et al., 2025; Bo et al., 2025; Liu et al., 2025g）揭示，天真地将基于文本的 memory scaling 到高维感知输入会导致严重低效、跨模态语义错位与脆弱的 retrieval 行为。这些挑战在具身设置中进一步放大，agent 在闭环环境中运行，必须对时间上延展的感知—动作—结果轨迹进行推理。在此类场景中，memory 必须超越存储 episodic observation，转而编码关于动力学、affordance 与物理约束的具身知识（Wang et al., 2025t）。然而，当前系统缺乏原则性机制来实现动作条件下的 memory update、跨模态抽象，以及 cross-episode、语义与 procedural memory 层的一致性维护。因此，具身 agent 常受困于技能碎片化、long-horizon 规划失败，以及由错位或陈旧 memory 导致的误差累积。

展望未来，一个有前景的研究方向是将 agent memory 提升为显式、预测性的世界模型，把 memory 视为随时间演化的可控内部状态，而非被动日志。基于世界模型的表述（Hafner et al., 2023; Ha & Schmidhuber, 2018）提供统一视角，其中 memory update 可被建模为以感知与动作为条件的 latent state 转移。这为主动 memory 规划打开大门：agent 在提交更新之前模拟存储、压缩或遗忘信息的长期后果（Schrittwieser et al., 2020; Silver et al., 2017）。在这一框架内，memory operation 成为与外部决策共同优化的内部动作，使 agent 能够平衡即时效用与长期一致性和任务表现。此外，将多模态 memory 与结构化世界表示（如空间地图、以对象为中心的图（Singh et al., 2023）或技能图（Wang et al., 2025c; Feng et al., 2025a））整合，可支持跨时间与模态的抽象，同时提升 retrieval 效率。最后，memory 与世界模型应在相互强化的回路中共同训练：稳定、结构化的 memory 可提供长期状态线索以改善世界模型预测，而世界模型可正则化 memory evolution 以防止身份漂移、目标不一致与行为不稳定（Savinov et al., 2019）。推进这一协同是构建可扩展、可靠的多模态与具身 agent、使其能在复杂真实世界环境中实现 long-horizon 自主的关键。

## 9.6 Real-World Benchmarking 与 Evaluations

memory 赋能 foundation agent 的真实世界 benchmark 中的一个核心挑战，在于研究级 benchmark 抽象与真实世界部署复杂性之间的持续错配，这对 user-centric 与 agent-centric 的 memory 都成立。在用户侧，大多数现有 benchmark 将长期个性化简化为合成事实回忆，agent 从 long-context 或脚本化交互历史中检索以 embedding 形式存在的静态用户属性（例如人设事实、偏好或对话）。此类设置虽便于受控评估，却未能捕捉真实用户满意度——后者取决于偏好漂移、冲突信号、部分可观测性以及数周或数月的延迟反馈。LoCoMo（Maharana et al., 2024）等 benchmark 强调 long-context retrieval 准确率，却隐含假设用户意图平稳且 ground truth 无歧义，忽视了陈旧偏好复用、长期用户状态被错误覆盖或敏感信息不安全保留等关键失败模式。即便是显式面向演化偏好的 PersonaMem（Jiang et al., 2025a），也在完全模拟的 session 上评估它们，且不评估 memory update 或刷新。在 agent 侧，包括 WebArena（Zhou et al., 2024）与 OSWorld（Xie et al., 2024）在内的交互式 benchmark 通过基于执行的评估提升真实感，但仍受限于精选环境、以重置为中心的任务设计与短评估时程。近期扩展开始放宽其中第一项：InterruptBench 通过任务中途添加、修订与撤回用户目标来增强 WebArena-Lite，并报告称即便是强骨干模型处理这些情况仍然困难（Zou et al., 2026）。这些约束掩盖了 agent 能否 cross-episode 积累、修订并安全利用经验，尤其是在非平稳工具、策略或环境下。因此，agent 可能优化短时程成功，却在 memory 关键能力（如来源跟踪、矛盾解决与长期策略一致性）上静默失败。直接探测隐藏用户状态使这一差距可测量：即便对无 memory 基线，任务完成也已饱和，而用户演化状态的恢复仍属中等，并在 top-K retrieval 下进一步退化（Ma et al., 2026）。这一差距与 GAIA（Mialon et al., 2024）等通用助手 benchmark 中的观察相呼应：失败往往并非来自孤立推理错误，而是来自多模态与工具中介交互中的脆弱状态转移与错误 memory update。

未来研究应走向闭环、纵向且以执行为根基的评估范式，在真实约束下显式施压持久 memory，对用户与 agent 均是如此。对 user-centric 的 memory，benchmark 应纳入带受控偏好漂移、模糊反馈与真实用户奖励的反复交互，从而直接测量与满意度对齐的 memory 行为，例如 compression、选择性 forgetting 与安全覆盖，而非静态回忆准确率（例如用数月偏好演化或反事实反馈扩展用户历史）。对 agent-centric 的 memory，评估应从模拟重置走向部分开放或持续演化的环境，其中经验积累具有真实后果，例如金融交易沙箱、长运行网络服务或带延迟回报的竞争性控制任务，从而在相同条件下比较 memory augmentation agent 与无 memory 基线。OSWorld（Xie et al., 2024）等基于执行的框架可扩展 memory 敏感不变量，要求 agent 对持久状态进行版本化、审计与回滚，并为存储知识附上来源元数据。同时，标准化工具中介层（例如 MCP 风格接口）可实现可复现日志、权限执行与回放，支持在真实约束下对 memory—策略交互进行细粒度评估。最后，benchmark 应显式量化资源—效用权衡，将 memory 质量测量为 token 预算、存储成本与延迟的函数，反映真实部署的有界 memory 条件。总体而言，这些方向将 benchmark 从 episodic 任务完成重新表述为对 memory 作为一流能力的系统级评估，共同塑造演化环境中的用户信任、agent 自主性与长期效用。

## 10 结论

memory 正成为 foundation agent 在 long-horizon、context explosion 且依赖用户的环境（如 agentic coding、深度研究与计算机使用）中运行的关键组件。在本综述中，我们沿三个维度统一设计，包括 memory substrate（内部与外部）、cognitive mechanism（sensory、working、episodic、semantic 与 procedural）与 memory subject（user-centric 的个性化与 agent-centric 的经验），并分析 memory 在 single-agent 与多 agent system 中如何被操作，以及它如何日益被基于 prompt、fine-tuning 与 RL 的演化与优化策略所塑造。此外，我们总结了用于评估 foundation agent 表现的指标与 benchmark，并将当前工作归类到代表性应用领域。贯穿始终，memory 从被动存储转向 agent self-evolving 的 substrate，我们以六项关键挑战收尾，指向可靠、可扩展且可信的 memory 基础设施。

## 参考文献

Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. arXiv preprint arXiv:2303.08774, 2023.

Qingyao Ai, Yichen Tang, Changyue Wang, Jianming Long, Weihang Su, and Yiqun Liu. Memorybench: A benchmark for memory and continual learning in llm systems. arXiv preprint arXiv:2510.17281, 2025.

Chandra Vamsi Krishna Alla, Harish Naidu Gaddam, and Manohar Kommi. Budgetmem: Learning selective memory policies for cost-eficient long-context processing in language models. arXiv preprint arXiv:2511.04919, 2025.

Saad Alqithami. Forgetful but faithful: A cognitive memory architecture and benchmark for privacy-aware generative agents. arXiv preprint arXiv:2512.12856, 2025.

Benjamin Ampel, Chi-Heng Yang, James Hu, and Hsinchun Chen. Large language models for conducting advanced text analytics information systems research. ACM Transactions on Management Information Systems, 16(1):1–27, 2025.

Petr Anokhin, Nikita Semenov, Artyom Sorokin, Dmitry Evseev, Andrey Kravchenko, Mikhail Burtsev, and Evgeny Burnaev. Arigraph: Learning knowledge graph world models with episodic memory for llm agents. arXiv preprint arXiv:2407.04363, 2024.

Anthropic. Model context protocol. https://github.com/modelcontextprotocol, 2024. GitHub repository, an open protocol for connecting LLMs with external data sources and tools

Anthropic. Claude agent skills. https://github.com/anthropics/skills, 2025. GitHub repository.

Rahul Aralikatte, Shashi Narayan, Joshua Maynez, Sascha Rothe, and Ryan McDonald. Focus attention: Promoting faithfulness and diversity in summarization. In Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers), pp. 6078–6095, 2021.

RM Aratchige and WMKS Ilmini. Llms working in harmony: A survey on the technological aspects of building efective llm-based multi agent systems. arXiv preprint arXiv:2504.01963, 2025.

Daman Arora, Atharv Sonwane, Nalin Wadhwa, Abhav Mehrotra, Saiteja Utpala, Ramakrishna Bairi, Aditya Kanade, and Nagarajan Natarajan. Masai: Modular architecture for software-engineering ai agents. arXiv preprint arXiv:2406.11638, 2024.

Richard C Atkinson and Richard M Shifrin. Human memory: A proposed system and its control processes. In Psychology of learning and motivation, volume 2, pp. 89–195. Elsevier, 1968.

Alan Baddeley. The episodic bufer: a new component of working memory? Trends in cognitive sciences, 4 (11):417–423, 2000.

Alan Baddeley. Working memory. Memory, pp. 71–111, 2020.

Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, et al. Qwen2. 5-vl technical report. arXiv preprint arXiv:2502.13923, 2025.

Victor Barres, Honghua Dong, Soham Ray, Xujie Si, and Karthik Narasimhan. τ<sup>2</sup>-bench: Evaluating conversational agents in a dual-control environment. arXiv preprint arXiv:2506.07982, 2025.

Ali Behrouz, Peilin Zhong, and Vahab Mirrokni. Titans: Learning to memorize at test time. arXiv preprint arXiv:2501.00663, 2024.

Yuanchen Bei, Weizhi Zhang, Siwen Wang, Weizhi Chen, Sheng Zhou, Hao Chen, Yong Li, Jiajun Bu, Shirui Pan, Yizhou Yu, et al. Graphs meet ai agents: Taxonomy, progress, and future opportunities. arXiv preprint arXiv:2506.18019, 2025.

Yuanchen Bei, Tianxin Wei, Xuying Ning, Yanjun Zhao, Zhining Liu, Xiao Lin, Yada Zhu, Hendrik Hamann, Jingrui He, and Hanghang Tong. Mem-gallery: Benchmarking multimodal long-term conversational memory for mllm agents. arXiv preprint arXiv:2601.03515, 2026.

Maksym Bekuzarov, Ariana Bermudez, Joon-Young Lee, and Hao Li. Xmem++: Production-level video segmentation from few annotated frames. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pp. 635–644, 2023.

Julia Belikova, Rauf Parchiev, Evgeny Egorov, Grigorii Davydenko, Gleb Gusev, Andrey Savchenko, and Maksim Makarenko. Managing procedural memory in llm agents: Control, adaptation, and evaluation. arXiv preprint arXiv:2606.23127, 2026.

Jack Bell, Luigi Quarantiello, Eric Nuertey Coleman, Lanpei Li, Malio Li, Mauro Madeddu, Elia Piccoli, and Vincenzo Lomonaco. The future of continual learning in the era of foundation models: Three ke directions. arXiv preprint arXiv:2506.03320, 2025.

Chandrachur Bhattacharya and Sibendu Som. Aisac: An integrated multi-agent system for transparent, retrieval-grounded scientific assistance. arXiv preprint arXiv:2511.14043, 2025.

Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. arXiv preprint arXiv:2503.14734, 2025.

Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Robert Equi, Chelsea Finn, Niccolo Fusai, Manuel Y Galliker, et al. π<sub>0.5</sub>: a vision-language-action model with open-world generalization. In Proceedings of The 9th Conference on Robot Learning, volume 305, pp. 17–40. PMLR, 2025.

Andrew Blair-Stanek, Nils Holzenberger, and Benjamin Van Durme. Can llms identify tax abuse? arXiv preprint arXiv:2508.20097, 2025.

Tim VP Bliss and Terje Lømo. Long-lasting potentiation of synaptic transmission in the dentate area of the anaesthetized rabbit following stimulation of the perforant path. The Journal of physiology, 232(2): 331–356, 1973.

Weihao Bo, Shan Zhang, Yanpeng Sun, Jingjing Wu, Qunyi Xie, Xiao Tan, Kunbin Chen, Wei He, Xiaofan Li, Na Zhao, et al. Agentic learner with grow-and-refine multimodal semantic memory. arXiv preprint arXiv:2511.21678, 2025.

Paweł Budzianowski, Tsung-Hsien Wen, Bo-Hsiang Tseng, Iñigo Casanueva, Stefan Ultes, Osman Ramadan, and Milica Gasic. Multiwoz-a large-scale multi-domain wizard-of-oz dataset for task-oriented dialogue modelling. In Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing, pp. 5016–5026, 2018.

Mikhail S Burtsev, Yuri Kuratov, Anton Peganov, and Grigory V Sapunov. Memory transformer. arXiv preprint arXiv:2006.11527, 2020.

Hongru Cai, Yongqi Li, Wenjie Wang, Fengbin Zhu, Xiaoyu Shen, Wenjie Li, and Tat-Seng Chua. Large language models empowered personalized web agents. In Proceedings of the ACM on Web Conference 2025, pp. 198–215, 2025.

Zefan Cai, Yichi Zhang, Bofei Gao, Yuliang Liu, Yucheng Li, Tianyu Liu, Keming Lu, Wayne Xiong, Yue Dong, Junjie Hu, et al. Pyramidkv: Dynamic kv cache compression based on pyramidal information funneling. arXiv preprint arXiv:2406.02069, 2024.

Bowen Cao, Deng Cai, and Wai Lam. Infiniteicl: Breaking the limit of context window size via long short-term memory transformation. arXiv preprint arXiv:2504.01707, 2025a.

Jiaqi Cao, Jiarui Wang, Rubin Wei, Qipeng Guo, Kai Chen, Bowen Zhou, and Zhouhan Lin. Memory decoder: A pretrained, plug-and-play memory for large language models. arXiv preprint arXiv:2508.09874, 2025b.

Jack David Carson and Amir Reisizadeh. A statistical physics of language model reasoning. arXiv preprint arXiv:2506.04374, 2025.

Victor de Lamo Castrillo, Habtom Kahsay Gidey, Alexander Lenz, and Alois Knoll. Fundamentals of building autonomous llm agents. arXiv preprint arXiv:2510.09244, 2025.

cauri. Memory in multi-agent systems: Technical implementations. https://artium.ai/insights/ memory-in-multi-agent-systems-technical-implementations, 2025. Artium.ai Insights article.

Dake Chen, Hanbin Wang, Yunhao Huo, Yuzhao Li, and Haoyang Zhang. Gamegpt: Multi-agent collaborative framework for game development. arXiv preprint arXiv:2310.08067, 2023.

Ding Chen, Simin Niu, Kehang Li, Peng Liu, Xiangping Zheng, Bo Tang, Xinchi Li, Feiyu Xiong, and Zhiyu Li. Halumem: Evaluating hallucinations in memory systems of agents. arXiv preprint arXiv:2511.03506, 2025a.

Guangyao Chen, Siwei Dong, Yu Shu, Ge Zhang, Jaward Sesay, Börje Karlsson, Jie Fu, and Yemin Shi. Autoagents: a framework for automatic agent generation. In Proceedings of the Thirty-Third International Joint Conference on Artificial Intelligence, pp. 22–30, 2024a.

Guhong Chen, Liyang Fan, Zihan Gong, Nan Xie, Zixuan Li, Ziqiang Liu, Chengming Li, Qiang Qu, Hamid Alinejad-Rokny, Shiwen Ni, et al. Agentcourt: Simulating court with adversarial evolvable lawyer agents. In Findings of the Association for Computational Linguistics: ACL 2025, pp. 5850–5865, 2025b.

Guoxin Chen, Zile Qiao, Xuanzhong Chen, Donglei Yu, Haotian Xu, Wayne Xin Zhao, Ruihua Song, Wenbiao Yin, Huifeng Yin, Liwen Zhang, et al. Iterresearch: Rethinking long-horizon agents via markovian state reconstruction. arXiv preprint arXiv:2511.07327, 2025c.

Hongshen Chen, Xiaorui Liu, Dawei Yin, and Jiliang Tang. A survey on dialogue systems: Recent advances and new frontiers. Acm Sigkdd Explorations Newsletter, 19(2):25–35, 2017.

Jiangjie Chen, Xintao Wang, Rui Xu, Siyu Yuan, Yikai Zhang, Wei Shi, Jian Xie, Shuang Li, Ruihan Yang, Tinghui Zhu, et al. From persona to personalization: A survey on role-playing language agents. arXiv preprint arXiv:2404.18231, 2024b.

Joya Chen, Zhaoyang Lv, Shiwei Wu, Kevin Qinghong Lin, Chenan Song, Difei Gao, Jia-Wei Liu, Ziteng Gao, Dongxing Mao, and Mike Zheng Shou. Videollm-online: Online video large language model for streaming video. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pp. 18407–18418, 2024c.

Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Josh Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba. Evaluating large language models trained on code. arXiv preprint arXiv:2107.03374, 2021.

Nuo Chen, Hongguang Li, Jianhui Chang, Juhua Huang, Baoyuan Wang, and Jia Li. Compress to impress: Unleashing the potential of compressive memory in real-world long-term conversations. In Proceedings of the 31st International Conference on Computational Linguistics, pp. 755–773, 2025d.

Xu Chen, Hongteng Xu, Yongfeng Zhang, Jiaxi Tang, Yixin Cao, Zheng Qin, and Hongyuan Zha. Sequential recommendation with user memory networks. In Proceedings of the eleventh ACM international conference on web search and data mining, pp. 108–116, 2018.

Yaoqi Chen, Jinkai Zhang, Baotong Lu, Qianxi Zhang, Chengruidong Zhang, Jingjia Luo, Di Liu, Huiqiang Jiang, Qi Chen, Jing Liu, et al. Retroinfer: A vector-storage approach for scalable long-context llm inference. arXiv preprint arXiv:2505.02922, 2025e.

Yi-Pei Chen, Noriki Nishida, Hideki Nakayama, and Yuji Matsumoto. Recent trends in personalized dialogue generation: A review of datasets, methodologies, and evaluations. arXiv preprint arXiv:2405.17974, 2024d.

Yixing Chen, Yiding Wang, Siqi Zhu, Haofei Yu, Tao Feng, Muhan Zhang, Mostofa Patwary, and Jiaxuan You. Multi-agent evolve: Llm self-improve through co-evolution. arXiv preprint arXiv:2510.23595, 2025f.

Weihua Cheng, Ersheng Ni, Wenlong Wang, Yifei Sun, Junming Liu, Wangyu Shen, Yirong Chen, Botian Shi, and Ding Wang. Mga: Memory-driven gui agent for observation-centric interaction. arXiv preprint arXiv:2510.24168, 2025.

Vinaik Chhetri, AB Siddique, and Umar Farooq. Understanding robustness of model editing in code llms: An empirical study. arXiv preprint arXiv:2511.03182, 2025.

Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh, and Deshraj Yadav. Mem0: Building productionready ai agents with scalable long-term memory. arXiv preprint arXiv:2504.19413, 2025.

Konstantina Christakopoulou, Shibl Mourad, and Maja Matarić. Agents thinking fast and slow: A talkerreasoner architecture. arXiv preprint arXiv:2410.08328, 2024.

Zhendong Chu, Shen Wang, Jian Xie, Tinghui Zhu, Yibo Yan, Jingheng Ye, Aoxiao Zhong, Xuming Hu, Jing Liang, Philip S. Yu, and Qingsong Wen. LLM agents for education: Advances and applications. In Christos Christodoulopoulos, Tanmoy Chakraborty, Carolyn Rose, and Violet Peng (eds.), Findings of the Association for Computational Linguistics: EMNLP 2025, pp. 13782–13810, Suzhou, China, November 2025. Association for Computational Linguistics.

Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, et al. Training verifiers to solve math word problems. arXiv preprint arXiv:2110.14168, 2021.

Neal J Cohen and Larry R Squire. Preserved learning and retention of pattern-analyzing skill in amnesia: Dissociation of knowing how and knowing that. Science, 210(4466):207–210, 1980.

Martin A. Conway and Christopher W. Pleydell-Pearce. The construction of autobiographical memories in the self-memory system. Psychological Review, 107(2):261–288, 2000.

Marc-Alexandre Côté, Akos Kádár, Xingdi Yuan, Ben Kybartas, Tavian Barnes, Emery Fine, James Moore, Matthew Hausknecht, Layla El Asri, Mahmoud Adada, et al. Textworld: A learning environment for text-based games. In Workshop on Computer Games, pp. 41–75. Springer, 2018.

Nick Craswell, Bhaskar Mitra, Emine Yilmaz, Daniel Campos, and Jimmy Lin. Ms marco: Benchmarking ranking models in the large-data regime. In Proceedings of the 44th international ACM SIGIR conference on research and development in information retrieval, pp. 1566–1576, 2021.

Justin Cui, Kevin Pu, and Tovi Grossman. Loom: Personalized learning informed by daily llm conversations toward long-term mastery via a dynamic learner memory graph. arXiv preprint arXiv:2511.21037, 2025a.

Yu Cui, Hang Fu, Haibin Zhang, Licheng Wang, and Cong Zuo. Free-mad: Consensus-free multi-agent debate. arXiv preprint arXiv:2509.11035, 2025b.

Zihang Dai, Zhilin Yang, Yiming Yang, Jaime G Carbonell, Quoc Le, and Ruslan Salakhutdinov. Transformerxl: Attentive language models beyond a fixed-length context. In Proceedings of the 57th annual meeting of the association for computational linguistics, pp. 2978–2988, 2019.

Matthias De Lange, Rahaf Aljundi, Marc Masana, Sarah Parisot, Xu Jia, Aleš Leonardis, Gregory Slabaugh, and Tinne Tuytelaars. A continual learning survey: Defying forgetting in classification tasks. IEEE transactions on pattern analysis and machine intelligence, 44(7):3366–3385, 2021.

Xiang Deng, Yu Gu, Boyuan Zheng, Shijie Chen, Sam Stevens, Boshi Wang, Huan Sun, and Yu Su. Mind2web: Towards a generalist agent for the web. Advances in Neural Information Processing Systems, 36:28091–28114, 2023.

Xiang Deng, Jef Da, Edwin Pan, Yannis Yiming He, Charles Ide, Kanak Garg, Niklas Laufer, Andrew Park, Nitin Pasari, Chetan Rane, et al. Swe-bench pro: Can ai agents solve long-horizon software engineering tasks? arXiv preprint arXiv:2509.16941, 2025.

Darshan Deshpande, Varun Gangal, Hersh Mehta, Anand Kannappan, Rebecca Qian, and Peng Wang. Memtrack: Evaluating long-term memory and state tracking in multi-platform dynamic agent environments. arXiv preprint arXiv:2510.01353, 2025.

Shangzhe Di, Zhelun Yu, Guanghao Zhang, Haoyuan Li, Tao Zhong, Hao Cheng, Bolin Li, Wanggui He, Fangxun Shu, and Hao Jiang. Streaming video question-answering with in-context video kv-cache retrieval. arXiv preprint arXiv:2503.00540, 2025.

Frederick Dillon, Gregor Halvorsen, Simon Tattershall, Magnus Rowntree, and Gareth Vanderpool. Contextual memory reweaving in large language models using layered latent state reconstruction. arXiv preprint arXiv:2502.02046, 2025.

Shen Dong, Shaochen Xu, Pengfei He, Yige Li, Jiliang Tang, Tianming Liu, Hui Liu, and Zhen Xiang. A practical memory injection attack against llm agents. arXiv preprint arXiv:2503.03704, 2025.

Alexandre Drouin, Maxime Gasse, Massimo Caccia, Issam H Laradji, Manuel Del Verme, Tom Marty, David Vazquez, Nicolas Chapados, and Alexandre Lacoste. Workarena: how capable are web agents at solving common knowledge work tasks? In Proceedings of the 41st International Conference on Machine Learning, pp. 11642–11662, 2024.

Yiming Du, Hongru Wang, Zhengyi Zhao, Bin Liang, Baojun Wang, Wanjun Zhong, Zezhong Wang, and Kam-Fai Wong. Perltqa: A personal long-term memory dataset for memory classification, retrieval, and fusion in question answering. In Proceedings of the 10th SIGHAN Workshop on Chinese Language Processing (SIGHAN-10), pp. 152–164, 2024.

Yiming Du, Wenyu Huang, Danna Zheng, Zhaowei Wang, Sebastien Montella, Mirella Lapata, Kam-Fai Wong, and Jef Z Pan. Rethinking memory in ai: Taxonomy, operations, topics, and future directions. arXiv preprint arXiv:2505.00675, 2025.

Matthew Dunn, Levent Sagun, Mike Higgins, V Ugur Guney, Volkan Cirik, and Kyunghyun Cho. Searchqa: A new q&a dataset augmented with context from a search engine. arXiv preprint arXiv:1704.05179, 2017.

Esin Durmus, Faisal Ladhak, and Tatsunori B Hashimoto. Spurious correlations in reference-free evaluation of text generation. In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 1443–1454, 2022.

Darren Edge, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva Mody, Steven Truitt, Dasha Metropolitansky, Robert Osazuwa Ness, and Jonathan Larson. From local to global: A graph rag approach to query-focused summarization. arXiv preprint arXiv:2404.16130, 2024.

Gilles O Einstein and Mark A McDaniel. Normal aging and prospective memory. Journal of Experimental Psychology: Learning, memory, and cognition, 16(4):717, 1990.

Andrew Estornell, Jean-Francois Ton, Yuanshun Yao, and Yang Liu. ACC-collab: An actor-critic approach to multi-agent LLM collaboration. In The Thirteenth International Conference on Learning Representations, 2025.

Linxi Fan, Guanzhi Wang, Yunfan Jiang, Ajay Mandlekar, Yuncong Yang, Haoyi Zhu, Andrew Tang, De-An Huang, Yuke Zhu, and Anima Anandkumar. Minedojo: Building open-ended embodied agents with internet-scale knowledge. Advances in Neural Information Processing Systems, 35:18343–18362, 2022.

Wei Fan, JinYi Yoon, and Bo Ji. imad: Intelligent multi-agent debate for eficient and accurate llm inference. arXiv preprint arXiv:2511.11306, 2025a.

Wenzhe Fan, Ning Yan, and Masood Mortazavi. Evomem: Improving multi-agent planning with dual-evolving memory. arXiv preprint arXiv:2511.01912, 2025b.

Yue Fan, Xiaojian Ma, Rujie Wu, Yuntao Du, Jiaqi Li, Zhi Gao, and Qing Li. Videoagent: A memoryaugmented multimodal agent for video understanding. In European Conference on Computer Vision, pp. 75–92. Springer, 2024.

Zhiyu Fan, Kirill Vasilevski, Dayi Lin, Boyuan Chen, Yihao Chen, Zhiqing Zhong, Jie M Zhang, Pinjia He, and Ahmed E Hassan. Swe-efi: Re-evaluating software ai agent system efectiveness under resource constraints. arXiv preprint arXiv:2509.09853, 2025c.

Jizhan Fang, Xinle Deng, Haoming Xu, Ziyan Jiang, Yuqi Tang, Ziwen Xu, Shumin Deng, Yunzhi Yao, Mengru Wang, Shuofei Qiao, et al. Lightmem: Lightweight and eficient memory-augmented generation. arXiv preprint arXiv:2510.18866, 2025a

Runnan Fang, Yuan Liang, Xiaobin Wang, Jialong Wu, Shuofei Qiao, Pengjun Xie, Fei Huang, Huajun Chen, and Ningyu Zhang. Memp: Exploring agent procedural memory. arXiv preprint arXiv:2508.06433, 2025b.

Tao Feng, Yexin Wu, Guanyu Lin, and Jiaxuan You. Graph world model. arXiv preprint arXiv:2507.10539, 2025a.

Xueyang Feng, Zhi-Yuan Chen, Yujia Qin, Yankai Lin, Xu Chen, Zhiyuan Liu, and Ji-Rong Wen. Large language model-based human-agent collaboration for complex task solving. In Findings of the Association for Computational Linguistics: EMNLP 2024, pp. 1336–1357, 2024.

Yuan Feng, Junlin Lv, Yukun Cao, Xike Xie, and S Kevin Zhou. Identify critical kv cache in llm inference from an output perturbation perspective. arXiv preprint arXiv:2502.03805, 2025b.

Sandro Rama Fiorini, Leonardo G Azevedo, Raphael M Thiago, Valesca M de Sousa, Anton B Labate, and Viviane Torres da Silva. Episodic memory in agentic frameworks: Suggesting next tasks. arXiv preprint arXiv:2511.17775, 2025.

Chaoyou Fu, Yuhan Dai, Yongdong Luo, Lei Li, Shuhuai Ren, Renrui Zhang, Zihan Wang, Chenyu Zhou, Yunhang Shen, Mengdan Zhang, et al. Video-mme: The first-ever comprehensive evaluation benchmark of multi-modal llms in video analysis. In Proceedings of the Computer Vision and Pattern Recognition Conference, pp. 24108–24118, 2025.

Pascale Fung, Yoram Bachrach, Asli Celikyilmaz, Kamalika Chaudhuri, Delong Chen, Willy Chung, Emmanuel Dupoux, Hongyu Gong, Hervé Jégou, Alessandro Lazaric, et al. Embodied ai agents: Modeling the world. arXiv preprint arXiv:2506.22355, 2025.

Chen Gao, Xiaochong Lan, Zhihong Lu, Jinzhu Mao, Jinghua Piao, Huandong Wang, Depeng Jin, and Yong Li. S3: Social-network simulation system with large language model-empowered agents. arXiv preprint arXiv:2307.14984, 2023.

Huan-ang Gao, Jiayi Geng, Wenyue Hua, Mengkang Hu, Xinzhe Juan, Hongzhang Liu, Shilong Liu, Jiahao Qiu, Xuan Qi, Yiran Wu, et al. A survey of self-evolving agents: On path to artificial super intelligence. arXiv preprint arXiv:2507.21046, 2025a.

Weibo Gao, Qi Liu, Linan Yue, Fangzhou Yao, Rui Lv, Zheng Zhang, Hao Wang, and Zhenya Huang. Agent4edu: Generating learner response data by generative agents for intelligent education systems. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, pp. 23923–23932, 2025b.

Suyu Ge, Yunan Zhang, Liyuan Liu, Minjia Zhang, Jiawei Han, and Jianfeng Gao. Model tells you what to discard: Adaptive kv cache compression for llms. arXiv preprint arXiv:2310.01801, 2023.

Sebastian Gehrmann, Elizabeth Clark, and Thibault Sellam. Repairing the cracked foundation: A survey of obstacles in evaluation practices for generated text. Journal of Artificial Intelligence Research, 77:103–166, 2023.

Alireza Ghafarollahi and Markus J Buehler. Sciagents: automating scientific discovery through bioinspired multi-agent intelligent graph reasoning. Advanced Materials, 37(22):2413523, 2025.

Marc Glocker, Peter Hönig, Matthias Hirschmanner, and Markus Vincze. Llm-empowered embodied agent for memory-augmented task planning in household robotics. arXiv preprint arXiv:2504.21716, 2025.

Juraj Gottweis, Wei-Hung Weng, Alexander Daryin, Tao Tu, Anil Palepu, Petar Sirkovic, Artiom Myaskovsky, Felix Weissenberger, Keran Rong, Ryutaro Tanno, et al. Towards an ai co-scientist. arXiv preprint arXiv:2502.18864, 2025.

Zhengyao Gu, Henry Peng Zou, Yankai Chen, Aiwei Liu, Weizhi Zhang, and Philip S Yu. Scaling laws for many-shot in-context learning with self-generated annotations. arXiv preprint arXiv:2503.03062, 2025.

Gunshi Gupta, Karmesh Yadav, Zsolt Kira, Yarin Gal, and Rahaf Aljundi. Memo: Training memory-eficient embodied agents with reinforcement learning. arXiv preprint arXiv:2510.19732, 2025.

Bernal Jiménez Gutiérrez, Yiheng Shu, Weijian Qi, Sizhe Zhou, and Yu Su. From rag to memory: Nonparametric continual learning for large language models. arXiv preprint arXiv:2502.14802, 2025.

Kelvin Guu, Kenton Lee, Zora Tung, Panupong Pasupat, and Mingwei Chang. Retrieval augmented language model pre-training. In International conference on machine learning, pp. 3929–3938. PMLR, 2020.

David Ha and Jürgen Schmidhuber. World models. arXiv preprint arXiv:1803.10122, 2(3), 2018.

Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. arXiv preprint arXiv:2301.04104, 2023.

Dongge Han, Camille Couturier, Daniel Madrigal Diaz, Xuchao Zhang, Victor Rühle, and Saravan Rajmohan. Legomem: Modular procedural memory for multi-agent llm systems for workflow automation. arXiv preprint arXiv:2510.04851, 2025.

Shanshan Han, Qifan Zhang, Yuhang Yao, Weizhao Jin, and Zhaozhuo Xu. Llm multi-agent systems: Challenges and open problems. arXiv preprint arXiv:2402.03578, 2024.

Shibo Hao, Yi Gu, Haodi Ma, Joshua Hong, Zhen Wang, Daisy Wang, and Zhiting Hu. Reasoning with language model is planning with world model. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pp. 8154–8173, 2023.

Kostas Hatalis, Despina Christou, Joshua Myers, Steven Jones, Keith Lambert, Adam Amos-Binks, Zohreh Dannenhauer, and Dustin Dannenhauer. Memory matters: The need to improve long-term memory in llm-agents. In Proceedings of the AAAI Symposium Series, volume 2, pp. 277–280, 2023.

Matthew Hausknecht, Prithviraj Ammanabrolu, Marc-Alexandre Côté, and Xingdi Yuan. Interactive fiction games: A colossal adventure. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 34, pp. 7903–7910, 2020.

Hongliang He, Wenlin Yao, Kaixin Ma, Wenhao Yu, Yong Dai, Hongming Zhang, Zhenzhong Lan, and Dong Yu. Webvoyager: Building an end-to-end web agent with large multimodal models. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 6864–6890, 2024a.

Junqing He, Liang Zhu, Rui Wang, Xi Wang, Gholamreza Hafari, and Jiaxing Zhang. Madial-bench: Towards real-world evaluation of memory-augmented dialogue generation. In Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers), pp. 9902–9921, 2025a.

Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. In Proceedings of the IEEE conference on computer vision and pattern recognition, pp. 770–778, 2016.

Langzhou He, Junyou Zhu, Yue Zhou, Zhengyao Gu, Junhua Liu, Wei-Chieh Huang, Henry Peng Zou, David Wipf, Philip S Yu, and Qitian Wu. Resolving action bottleneck: Agentic reinforcement learning informed by token-level energy. arXiv preprint arXiv:2605.14558, 2026.

Shiqi He, Yue Cui, Xinyu Ma, Yaliang Li, Bolin Ding, and Mosharaf Chowdhury. Branch-and-browse: Eficient and controllable web exploration with tree-structured reasoning and action memory. arXiv preprint arXiv:2510.19838, 2025b.

Zifan He, Yingqi Cao, Zongyue Qin, Neha Prakriya, Yizhou Sun, and Jason Cong. Hmt: Hierarchical memory transformer for eficient long context language processing. In Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers), pp. 8068–8089, 2025c.

Zihong He, Weizhe Lin, Hao Zheng, Fan Zhang, Matt W Jones, Laurence Aitchison, Xuhai Xu, Miao Liu, Per Ola Kristensson, and Junxiao Shen. Human-inspired perspectives: A survey on ai long-term memory. arXiv preprint arXiv:2411.00489, 2024b

Donald Olding Hebb. The organization of behavior: A neuropsychological theory. Psychology press, 2005.

Dan Hendrycks, Steven Basart, Saurav Kadavath, Mantas Mazeika, Akul Arora, Ethan Guo, Collin Burns, Samir Puranik, Horace He, Dawn Song, and Jacob Steinhardt. Measuring coding challenge competence with APPS. In Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2), 2021a.

Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, and Jacob Steinhardt. Measuring massive multitask language understanding. In International Conference on Learning Representations, 2021b.

Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and Jacob Steinhardt. Measuring mathematical problem solving with the math dataset. In Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track, 2021c.

Xanh Ho, Anh-Khoa Duong Nguyen, Saku Sugawara, and Akiko Aizawa. Constructing a multi-hop qa dataset for comprehensive evaluation of reasoning steps. In Proceedings of the 28th International Conference on Computational Linguistics, pp. 6609–6625, 2020.

Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng Cheng, Jinlin Wang, Ceyao Zhang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, et al. Metagpt: Meta programming for a multi-agent collaborative framework. In The Twelfth International Conference on Learning Representations, 2024.

Yining Hong, Rui Sun, Bingxuan Li, Xingcheng Yao, Maxine Wu, Alexander Chien, Da Yin, Ying Nian Wu, Zhecan James Wang, and Kai-Wei Chang. Embodied web agents: Bridging physical-digital realms for integrated agent intelligence. arXiv preprint arXiv:2506.15677, 2025.

Yuki Hou, Haruki Tamoto, and Homei Miyashita. " my agent understands me better": Integrating dynamic human-like memory recall and consolidation in llm-based agents. In Extended Abstracts of the CHI Conference on Human Factors in Computing Systems, pp. 1–7, 2024.

Chenxu Hu, Jie Fu, Chenzhuang Du, Simian Luo, Junbo Zhao, and Hang Zhao. Chatdb: Augmenting llms with databases as their symbolic memory. arXiv preprint arXiv:2306.03901, 2023.

Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, et al. Lora: Low-rank adaptation of large language models. ICLR, 1(2):3, 2022.

He Hu, Yucheng Zhou, Chiyuan Ma, Qianning Wang, Zheng Zhang, Fei Ma, Laizhong Cui, and Qi Tian. Theramind: A strategic and adaptive agent for longitudinal psychological counseling. arXiv preprint arXiv:2510.25758, 2025a.

Mengkang Hu, Tianxing Chen, Qiguang Chen, Yao Mu, Wenqi Shao, and Ping Luo. Hiagent: Hierarchical working memory management for solving long-horizon agent tasks with large language model. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 32779–32798, 2025b.

Yuanzhe Hu, Yu Wang, and Julian McAuley. Evaluating memory in llm agents via incremental multi-turn interactions. arXiv preprint arXiv:2507.05257, 2025c.

Yuyang Hu, Shichun Liu, Yanwei Yue, Guibin Zhang, Boyang Liu, Fangyi Zhu, Jiahang Lin, Honglin Guo, Shihan Dou, Zhiheng Xi, et al. Memory in the age of ai agents. arXiv preprint arXiv:2512.13564, 2025d.

Wenyue Hua, Lizhou Fan, Lingyao Li, Kai Mei, Jianchao Ji, Yingqiang Ge, Libby Hemphill, and Yongfeng Zhang. War and peace (waragent): Large language model-based multi-agent simulation of world wars. arXiv preprint arXiv:2311.17227, 2023.

Wenyue Hua, Xianjun Yang, Mingyu Jin, Zelong Li, Wei Cheng, Ruixiang Tang, and Yongfeng Zhang. Trustagent: Towards safe and trustworthy llm-based agents through agent constitution. In Trustworthy Multi-modal Foundation Models and AI Agents (TiFA), 2024.

Jimin Huang, Mengxi Xiao, Dong Li, Zihao Jiang, Yuzhe Yang, Yifei Zhang, Lingfei Qian, Yan Wang, Xueqing Peng, Yang Ren, et al. Open-finllms: Open multimodal large language models for financial applications. arXiv preprint arXiv:2408.11878, 2024a.

Wei-Chieh Huang and Cornelia Caragea. MADIAVE: Multi-agent debate for implicit attribute value extraction. In Findings of the Association for Computational Linguistics: EACL 2026, 2026.

Wei-Chieh Huang, Henry Peng Zou, Yaozu Wu, Dongyuan Li, Yankai Chen, Weizhi Zhang, Yangning Li, Angelo Zangari, Jizhou Guo, Chunyu Miao, et al. Deepresearchguard: Deep research with open-domain evaluation and multi-stage guardrails for safety. arXiv preprint arXiv:2510.10994, 2025a.

Xu Huang, Weiwen Liu, Xiaolong Chen, Xingmei Wang, Hao Wang, Defu Lian, Yasheng Wang, Ruiming Tang, and Enhong Chen. Understanding the planning of llm agents: A survey. arXiv preprint arXiv:2402.02716, 2024b.

Xu Huang, Jianxun Lian, Yuxuan Lei, Jing Yao, Defu Lian, and Xing Xie. Recommender ai agent: Integrating large language models for interactive recommendations. ACM Transactions on Information Systems, 43(4): 1–33, 2025b.

Yizheng Huang and Jimmy Huang. A survey on retrieval-augmented text generation for large language models. arXiv preprint arXiv:2404.10981, 2024.

Yuxuan Huang, Yihang Chen, Haozheng Zhang, Kang Li, Huichi Zhou, Meng Fang, Linyi Yang, Xiaoguang Li, Lifeng Shang, Songcen Xu, et al. Deep research agents: A systematic examination and roadmap. arXiv preprint arXiv:2506.18096, 2025c.

Zhaopei Huang, Qifeng Dai, Guozheng Wu, Xiaopeng Wu, Kehan Chen, Chuan Yu, Xubin Li, Tiezheng Ge, Wenxuan Wang, and Qin Jin. Mem-pal: Towards memory-based personalized dialogue assistants for long-term user-agent interaction. arXiv preprint arXiv:2511.13410, 2025d.

Zhengjun Huang, Zhoujin Tian, Qintian Guo, Fangyuan Zhang, Yingli Zhou, Di Jiang, and Xiaofang Zhou. Licomemory: Lightweight and cognitive agentic memory for eficient long-term reasoning. arXiv preprint arXiv:2511.01448, 2025e.

Luis Ibanez-Lissen, Lorena Gonzalez-Manzano, Jose Maria de Fuentes, Nicolas Anciaux, and Joaquin Garcia-Alfaro. Lumia: Linear probing for unimodal and multimodal membership inference attacks leveraging internal llm states. In European Symposium on Research in Computer Security, pp. 186–206. Springer, 2025.

Yoichi Ishibashi and Yoshimasa Nishimura. Self-organized agents: A llm multi-agent framework toward ultra large-scale code generation and optimization. arXiv preprint arXiv:2404.02183, 2024.

Md Ashraful Islam, Mohammed Eunus Ali, and Md Rizwan Parvez. Mapcoder: Multi-agent code generation for competitive problem solving. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 4912–4944, 2024.

Shian Jia, Ziyang Huang, Xinbo Wang, Haofei Zhang, and Mingli Song. Pisa: A pragmatic psych-inspired unified memory system for enhanced ai agency. arXiv preprint arXiv:2510.15966, 2025a.

Zixi Jia, Qinghua Liu, Hexiao Li, Yuyan Chen, and Jiqiang Liu. Evaluating the long-term memory of large language models. In Findings of the Association for Computational Linguistics: ACL 2025, pp. 19759–19777, 2025b.

Bowen Jiang, Zhuoqun Hao, Young-Min Cho, Bryan Li, Yuan Yuan, Sihao Chen, Lyle Ungar, Camillo J Taylor, and Dan Roth. Know me, respond to me: Benchmarking llms for dynamic user profiling and personalized responses at scale. arXiv preprint arXiv:2504.14225, 2025a.

Bowen Jiang, Yuan Yuan, Maohao Shen, Zhuoqun Hao, Zhangchen Xu, Zichen Chen, Ziyi Liu, Anvesh Rao Vijjini, Jiashu He, Hanchao Yu, et al. Personamem-v2: Towards personalized intelligence via learning implicit user personas and agentic memory. arXiv preprint arXiv:2512.06688, 2025b.

Jinhao Jiang, Kun Zhou, Wayne Xin Zhao, Yang Song, Chen Zhu, Hengshu Zhu, and Ji-Rong Wen. Kg-agent: An eficient autonomous agent framework for complex reasoning over knowledge graph. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 9505–9523, 2025c.

Tao Jiang, Zichuan Lin, Lihe Li, Yi-Chen Li, Cong Guan, Lei Yuan, Zongzhang Zhang, Yang Yu, and Deheng Ye. Multi-agent in-context coordination via decentralized memory retrieval. arXiv preprint arXiv:2511.10030, 2025d.

Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik R Narasimhan. Swe-bench: Can language models resolve real-world github issues? In The Twelfth International Conference on Learning Representations, 2024.

Bernal Jimenez Gutierrez, Yiheng Shu, Yu Gu, Michihiro Yasunaga, and Yu Su. Hipporag: Neurobiologically inspired long-term memory for large language models. Advances in Neural Information Processing Systems, 37:59532–59569, 2024.

Hyoungwook Jin, Minju Yoo, Jeongeon Park, Yokyung Lee, Xu Wang, and Juho Kim. Teachtune: Reviewing pedagogical agents against diverse student profiles with simulated students. In Proceedings of the 2025 CHI Conference on Human Factors in Computing Systems, pp. 1–28, 2025a.

Long Jin, Yang Chen, Tianyi Wang, Pan Hui, and Athanasios V Vasilakos. Understanding user behavior in online social networks: A survey. IEEE communications magazine, 51(9):144–150, 2013.

Qiao Jin, Zhizheng Wang, Yifan Yang, Qingqing Zhu, Donald Wright, Thomas Huang, Nikhil Khandekar, Nicholas Wan, Xuguang Ai, W John Wilbur, et al. Agentmd: Empowering language agents for risk prediction with large-scale clinical tool learning. Nature Communications, 16(1):9377, 2025b.

Zhi Jing, Yongye Su, and Yikun Han. When large language models meet vector databases: A survey. In 2025 Conference on Artificial Intelligence x Multimedia (AIxMM), pp. 7–13. IEEE, 2025.

Mandar Joshi, Eunsol Choi, Daniel S Weld, and Luke Zettlemoyer. Triviaqa: A large scale distantly supervised challenge dataset for reading comprehension. In Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 1601–1611, 2017.

Sheena A Josselyn and Susumu Tonegawa. Memory engrams: Recalling the past and imagining the future. Science, 367(6473):eaaw4325, 2020.

Lars Benedikt Kaesberg, Jonas Becker, Jan Philip Wahle, Terry Ruas, and Bela Gipp. Voting or consensus? decision-making in multi-agent debate. In Findings of the Association for Computational Linguistics: ACL 2025, pp. 11640–11671. Association for Computational Linguistics, 2025. doi: 10.18653/v1/2025. findings-acl.606.

Tomoyuki Kagaya, Thong Jing Yuan, Yuxuan Lou, Jayashree Karlekar, Sugiri Pranata, Akira Kinose, Koki Oguri, Felix Wick, and Yang You. Rap: Retrieval-augmented planning with contextual memory fo multimodal llm agents. arXiv preprint arXiv:2402.03610, 2024.

Tomoyuki Kagaya, Subramanian Lakshmi, Anbang Ye, Thong Jing Yuan, Jayashree Karlekar, Sugiri Pranata, Natsuki Murakami, Akira Kinose, and Yang You. Vireskill: Vision-grounded replanning with skill memory for llm-based planning in lifelong robot learning. arXiv preprint arXiv:2509.24219, 2025.

Nikhil Kandpal, Haikang Deng, Adam Roberts, Eric Wallace, and Colin Rafel. Large language models struggle to learn long-tail knowledge. In International conference on machine learning, pp. 15696–15707. PMLR, 2023.

Jiazheng Kang, Mingming Ji, Zhe Zhao, and Ting Bai. Memory os of ai agent. arXiv preprint arXiv:2506.06326, 2025a.

Jikun Kang, Wenqi Wu, Filippos Christianos, Alex James Chan, Fraser David Greenlee, George Thomas, Marvin Purtorab, and Andrew Toulis. Lm2: Large memory models for long context reasoning. In Workshop on Reasoning and Planning for Large Language Models, 2025b.

Minki Kang, Wei-Ning Chen, Dongge Han, Huseyin A Inan, Lukas Wutschitz, Yanzhi Chen, Robert Sim, and Saravan Rajmohan. Acon: Optimizing context compression for long-horizon llm agents. arXiv preprint arXiv:2510.00615, 2025c.

Zixuan Ke, Weize Kong, Cheng Li, Mingyang Zhang, Qiaozhu Mei, and Michael Bendersky. Bridging the preference gap between retrievers and LLMs. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 10438–10451, Bangkok, Thailand, August 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.acl-long.562.

Zixuan Ke, Fangkai Jiao, Yifei Ming, Xuan-Phi Nguyen, Austin Xu, Do Xuan Long, Minzhi Li, Chengwei Qin, PeiFeng Wang, silvio savarese, Caiming Xiong, and Shafiq Joty. A survey of frontiers in LLM reasoning: Inference scaling, learning to reason, and agentic systems. Transactions on Machine Learning Research, 2025a. ISSN 2835-8856. Survey Certification.

Zixuan Ke, Yifei Ming, Xuan-Phi Nguyen, Caiming Xiong, and Shafiq Joty. Demystifying domain-adaptive post-training for financial LLMs. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing. Association for Computational Linguistics, 2025b. ISBN 979-8-89176-332-6. doi: 10.18653/v1/2025.emnlp-main.1579.

Sam Keen. Implicit memory systems for llms. https://deepengineering.substack.com/p/ implicit-memory-systems-for-llms, 2025. Deep Engineering (Substack) article.

Ronald Kemker and Christopher Kanan. FearNet: Brain-Inspired Model for Incremental Learning. In ICLR, 2018.

Byeonghwi Kim, Jinyeon Kim, Yuyeong Kim, Cheolhong Min, and Jonghyun Choi. Context-aware planning and environment-aware memory for instruction following embodied agents. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pp. 10936–10946, 2023a.

Donghyuk Kim, Sejeong Yang, Wonjin Shin, and Joo-Young Kim. V-rex: Real-time streaming video llm acceleration via dynamic kv cache retrieval. arXiv preprint arXiv:2512.12284, 2025a.

Jiho Kim, Woosog Chay, Hyeonji Hwang, Daeun Kyung, Hyunseung Chung, Eunbyeol Cho, Yohan Jo, and Edward Choi. Dialsim: A real-time simulator for evaluating long-term multi-party dialogue understanding of conversation systems. arXiv preprint arXiv:2406.13144, 2024a.

Minsoo Kim, Arnav Kundu, Han-Byul Kim, Richa Dixit, and Minsik Cho. Epicache: Episodic kv cache management for long conversational question answering. arXiv preprint arXiv:2509.17396, 2025b.

Taewoon Kim, Michael Cochez, Vincent François-Lavet, Mark Neerincx, and Piek Vossen. A machine with short-term, episodic, and semantic memory systems. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 37, pp. 48–56, 2023b.

Yubin Kim, Chanwoo Park, Hyewon Jeong, Yik S Chan, Xuhai Xu, Daniel McDuf, Hyeonhoon Lee, Marzyeh Ghassemi, Cynthia Breazeal, and Hae W Park. Mdagents: An adaptive collaboration of llms for medical decision-making. Advances in Neural Information Processing Systems, 37:79410–79452, 2024b.

Shashank Kirtania, Param Biyani, Priyanshu Gupta, Yasharth Bajpai, Roshni Iyer, Sumit Gulwani, and Gustavo Soares. Improving language agents through brew. arXiv preprint arXiv:2511.20297, 2025.

Ching-Yun Ko, Sihui Dai, Payel Das, Georgios Kollias, Subhajit Chaudhury, and Aurelie Lozano. Memreasoner: A memory-augmented llm architecture for multi-hop reasoning. In The First Workshop on System-2 Reasoning at Scale, NeurIPS’24, 2024.

Ishant Kohar and Aswanth Krishnan. A benchmark for procedural memory retrieval in language agents. arXiv preprint arXiv:2511.21730, 2025.

Alex Krizhevsky, Ilya Sutskever, and Geofrey E Hinton. Imagenet classification with deep convolutional neural networks. Advances in neural information processing systems, 25, 2012.

Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh, Chris Alberti, Danielle Epstein, Illia Polosukhin, Jacob Devlin, Kenton Lee, et al. Natural questions: a benchmark for question answering research. Transactions of the Association for Computational Linguistics, 7:453–466, 2019.

Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph Gonzalez, Hao Zhang, and Ion Stoica. Eficient memory management for large language model serving with pagedattention. In Proceedings of the 29th symposium on operating systems principles, pp. 611–626, 2023.

Anton Bulle Labate, Valesca Moura de Sousa, Sandro Rama Fiorini, Leonardo Guerreiro Azevedo, Raphael Melo Thiago, and Viviane Torres da Silva. Solving context window overflow in ai agents. arXiv preprint arXiv:2511.22729, 2025.

Paraskevas Lagakis and Stavros Demetriadis. Evaai: a multi-agent framework leveraging large language models for enhanced automated grading. In International Conference on Intelligent Tutoring Systems, pp. 378–385. Springer, 2024.

Yilong Lai, Yipin Yang, Jialong Wu, Fengran Mo, Zhenglin Wang, Ting Liang, Jianguo Lin, and Keping Yang. Crmweaver: Building powerful business agent via agentic rl and shared memories. arXiv preprint arXiv:2510.25333, 2025.

Tian Lan, Wenwei Zhang, Chengqi Lyu, Shuaibin Li, Chen Xu, Heyan Huang, Dahua Lin, Xian-Ling Mao, and Kai Chen. Training language models to critique with multi-agent feedback. arXiv preprint arXiv:2410.15287, 2024.

Chris Latimer, Nicoló Boschi, Andrew Neeser, Chris Bartholomew, Gaurav Srivastava, Xuan Wang, and Naren Ramakrishnan. Hindsight is 20/20: Building agent memory that retains, recalls, and reflects. arXiv preprint arXiv:2512.12818, 2025.

Gibbeum Lee, Volker Hartmann, Jongho Park, Dimitris Papailiopoulos, and Kangwook Lee. Prompted llms as chatbot modules for long open-domain conversation. In Findings of the Association for Computational Linguistics: ACL 2023, pp. 4536–4554, 2023.

Kuang-Huei Lee, Xinyun Chen, Hiroki Furuta, John Canny, and Ian Fischer. A human-inspired reading agent with gist memory of very long contexts. In International Conference on Machine Learning, pp. 26396–26415. PMLR, 2024.

Xiang Lei, Qin Li, and Min Zhang. D-smart: Enhancing llm dialogue consistency via dynamic structured memory and reasoning tree. arXiv preprint arXiv:2510.13363, 2025.

Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, et al. Retrieval-augmented generation for knowledge intensive nlp tasks. Advances in neural information processing systems, 33:9459–9474, 2020.

Cheng Li, Ziang Leng, Chenxi Yan, Junyi Shen, Hao Wang, Weishi Mi, Yaying Fei, Xiaoyang Feng, Song Yan, HaoSheng Wang, et al. Chatharuhi: Reviving anime character in reality via large language model. arXiv preprint arXiv:2308.09597, 2023a.

Hao Li, Chenghao Yang, An Zhang, Yang Deng, Xiang Wang, and Tat-Seng Chua. Hello again! llm-powered personalized agent for long-term dialogue. In Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers), pp. 5259–5276, 2025a.

Haohang Li, Yupeng Cao, Yangyang Yu, Shashidhar Reddy Javaji, Zhiyang Deng, Yueru He, Yuechen Jiang, Zining Zhu, Kp Subbalakshmi, Jimin Huang, et al. Investorbench: A benchmark for financial decision-making tasks with llm-based agent. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 2509–2525, 2025b.

Huihan Li, Yuting Ning, Zeyi Liao, Siyuan Wang, Xiang Lorraine Li, Ximing Lu, Wenting Zhao, Faeze Brahman, Yejin Choi, and Xiang Ren. In search of the long-tail: Systematic generation of long-tail inferential knowledge via logical rule guided search. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, pp. 2348–2370, 2024a.

Jitang Li and Jinzheng Li. Memory, consciousness and large language model. arXiv preprint arXiv:2401.02509, 2024.

Jiwei Li, Michel Galley, Chris Brockett, Georgios Spithourakis, Jianfeng Gao, and William B Dolan. A persona-based neural conversation model. In Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 994–1003, 2016.

Manling Li, Shiyu Zhao, Qineng Wang, Kangrui Wang, Yu Zhou, Sanjana Srivastava, Cem Gokmen, Tony Lee, Erran Li Li, Ruohan Zhang, et al. Embodied agent interface: Benchmarking llms for embodied decision making. Advances in Neural Information Processing Systems, 37:100428–100534, 2024b.

Ruanjun Li, Yuedong Tan, Yuanming Shi, and Jiawei Shao. Videoscan: Enabling eficient streaming video understanding via frame-level semantic carriers. arXiv preprint arXiv:2503.09387, 2025c.

Rui Li, Zeyu Zhang, Xiaohe Bo, Zihang Tian, Xu Chen, Quanyu Dai, Zhenhua Dong, and Ruiming Tang. Cam: A constructivist view of agentic memory for llm-based reading comprehension. arXiv preprint arXiv:2510.05520, 2025d.

Rumeng Li, Xun Wang, Dan Berlowitz, Jesse Mez, Honghuang Lin, and Hong Yu. Care-ad: a multi-agent large language model framework for alzheimer’s disease prediction using longitudinal clinical notes. npj Digital Medicine, 8(1):541, 2025e.

Sijia Li, Yuchen Huang, Zifan Liu, Zijian Li, Lei Song, Jiang Bian, Jun Zhang, Rui Wang, et al. Sit-graph: State integrated tool graph for multi-turn agents. arXiv preprint arXiv:2512.07287, 2025f.

Xiangyi Li et al. Skillsbench: Benchmarking how well agent skills work across diverse tasks. arXiv preprint arXiv:2602.12670, 2026.

Xiaoxi Li, Wenxiang Jiao, Jiarui Jin, Guanting Dong, Jiajie Jin, Yinuo Wang, Hao Wang, Yutao Zhu, Ji-Rong Wen, Yuan Lu, et al. Deepagent: A general reasoning agent with scalable toolsets. arXiv preprint arXiv:2510.21618, 2025g.

Xinyi Li, Sai Wang, Siqi Zeng, Yu Wu, and Yi Yang. A survey on llm-based multi-agent systems: workflow, infrastructure, and challenges. Vicinagearth, 1(1):9, 2024c.

Yang Li, Yangyang Yu, Haohang Li, Zhi Chen, and Khaldoun Khashanah. Tradinggpt: Multi-agent system with layered memory and distinct characters for enhanced financial trading performance. arXiv preprint arXiv:2309.03736, 2023b.

Yang Li, Zhiyuan He, Yuxuan Huang, Zhuhanling Xiao, Chao Yu, Meng Fang, Kun Shao, and Jun Wang. Adapting like humans: A metacognitive agent with test-time reasoning. arXiv preprint arXiv:2511.23262, 2025h.

Yangning Li, Weizhi Zhang, Yuyao Yang, Wei-Chieh Huang, Yaozu Wu, Junyu Luo, Yuanchen Bei, Henry Peng Zou, Xiao Luo, Yusheng Zhao, et al. Towards agentic rag with deep reasoning: A survey of rag-reasoning systems in llms. In Findings of the Association for Computational Linguistics: EMNLP 2025, pp. 12120– 12145, 2025i.

Yuan Li, Lichao Sun, and Yixuan Zhang. Metaagents: Large language model based agents for decision-making on teaming. Proceedings of the ACM on Human-Computer Interaction, 9(2):1–27, 2025j.

Yuhong Li, Yingbing Huang, Bowen Yang, Bharat Venkitesh, Acyr Locatelli, Hanchen Ye, Tianle Cai, Patrick Lewis, and Deming Chen. Snapkv: Llm knows what you are looking for before generation. Advances in Neural Information Processing Systems, 37:22947–22970, 2024d.

Zhiyu Li, Shichao Song, Chenyang Xi, Hanyu Wang, Chen Tang, Simin Niu, Ding Chen, Jiawei Yang, Chunyu Li, Qingchen Yu, et al. Memos: A memory os for ai system. arXiv preprint arXiv:2507.03724, 2025k.

Zhuofeng Li, Haoxiang Zhang, Seungju Han, Sheng Liu, Jianwen Xie, Yu Zhang, Yejin Choi, James Zou, and Pan Lu. In-the-flow agentic system optimization for efective planning and tool use. arXiv preprint arXiv:2510.05592, 2025l.

Zongwei Li, Zhonghang Li, Zirui Guo, Xubin Ren, and Chao Huang. Deepcode: Open agentic coding. arXiv preprint arXiv:2512.07921, 2025m.

Jiafeng Liang, Hao Li, Chang Li, Jiaqi Zhou, Shixin Jiang, Zekun Wang, Changkai Ji, Zhihao Zhu, Runxuan Liu, Tao Ren, et al. Ai meets brain: Memory systems from cognitive neuroscience to autonomous agents. arXiv preprint arXiv:2512.23343, 2025.

Jonathan Light, Min Cai, Sheng Shen, and Ziniu Hu. Avalonbench: Evaluating llms playing the game of avalon. arXiv preprint arXiv:2310.05036, 2023.

Jianzhe Lin, Zeyu Pan, Yun Zhu, Ruiqi Song, and Jining Yang. Towards continuous intelligence growth: Selftraining, continual learning, and dual-scale memory in superintelliagent. arXiv preprint arXiv:2511.23436, 2025.

Chen Ling, Xujiang Zhao, Jiaying Lu, Chengyuan Deng, Can Zheng, Junxiang Wang, Tanmoy Chowdhury, Yun Li, Hejie Cui, Xuchao Zhang, et al. Domain specialization as the key to make large language models disruptive: A comprehensive survey. ACM Computing Surveys, 58(3):1–39, 2025.

Stacey Diane Arañez Litam, Clark D Ausloos, and John JS Harrichand. Stress and resilience among professional counselors during the covid-19 pandemic. Journal of Counseling & Development, 99(4):384–395, 2021.

Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, et al. Deepseek-v3 technical report. arXiv preprint arXiv:2412.19437, 2024a.

Bang Liu, Xinfeng Li, Jiayi Zhang, Jinlin Wang, Tanjin He, Sirui Hong, Hongzhang Liu, Shaokun Zhang, Kaitao Song, Kunlun Zhu, et al. Advances and challenges in foundation agents: From brain-inspired intelligence to evolutionary, collaborative, and safe systems. arXiv preprint arXiv:2504.01990, 2025a.

Genglin Liu, Shijie Geng, Sha Li, Hejie Cui, Sarah Zhang, Xin Liu, and Tianyi Liu. Webcoach: Self-evolving web agents with cross-session memory guidance. arXiv preprint arXiv:2511.12997, 2025b.

Genglin Liu, Vivian T Le, Salman Rahman, Elisa Kreiss, Marzyeh Ghassemi, and Saadia Gabriel. Mosaic: Modeling social ai for content dissemination and regulation in multi-agent simulations. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing, pp. 6401–6428, 2025c.

Haofeng Liu, Mingqi Gao, Xuxiao Luo, Ziyue Wang, Guanyi Qin, Junde Wu, and Yueming Jin. Resurgsam2: Referring segment anything in surgical video via credible long-term tracking. In International Conference on Medical Image Computing and Computer-Assisted Intervention, pp. 435–445. Springer, 2025d.

Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. Advances in neural information processing systems, 36:34892–34916, 2023a.

Jiahong Liu, Zexuan Qiu, Zhongyang Li, Quanyu Dai, Wenhao Yu, Jieming Zhu, Minda Hu, Menglin Yang, Tat-Seng Chua, and Irwin King. A survey of personalized large language models: Progress and future directions. arXiv preprint arXiv:2502.11528, 2025e.

Jiarun Liu, Shiyue Xu, Yang Li, Shangkun Liu, Yongli Yu, and Peng Cao. Unifying dynamic tool creation and cross-task experience sharing through cognitive memory architecture. arXiv preprint arXiv:2512.11303, 2025f.

Junming Liu, Yifei Sun, Weihua Cheng, Haodong Lei, Yirong Chen, Licheng Wen, Xuemeng Yang, Daocheng Fu, Pinlong Cai, Nianchen Deng, et al. Memverse: Multimodal memory for lifelong learning agents. arXiv preprint arXiv:2512.03627, 2025g.

Lei Liu, Xiaoyan Yang, Yue Shen, Binbin Hu, Zhiqiang Zhang, Jinjie Gu, and Guannan Zhang. Think-inmemory: Recalling and post-thinking enable llms with long-term memory. arXiv preprint arXiv:2311.08719, 2023b.

Mugeng Liu, Siqi Zhong, Qi Yang, Yudong Han, Xuanzhe Liu, and Yun Ma. Webanns: Fast and eficient approximate nearest neighbor search in web browsers. In Proceedings of the 48th International ACM SIGIR Conference on Research and Development in Information Retrieval, pp. 2483–2492, 2025h.

Nelson F Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. Lost in the middle: How language models use long contexts. Transactions of the Association for Computational Linguistics, 12:157–173, 2024b.

WenTao Liu, Ruohua Zhang, Aimin Zhou, Feng Gao, and JiaLi Liu. Echo: A large language model with temporal episodic memory. arXiv preprint arXiv:2502.16090, 2025i.

Xiang Liu, Zhenheng Tang, Peijie Dong, Zeyu Li, Yue Liu, Bo Li, Xuming Hu, and Xiaowen Chu. Chunkkv: Semantic-preserving kv cache compression for eficient long-context llm inference. arXiv preprint arXiv:2502.00299, 2025j.

Yi Liu, Weizhe Wang, Ruitao Feng, Yao Zhang, Guangquan Xu, Gelei Deng, Yuekang Li, and Leo Zhang. Agent skills in the wild: An empirical study of security vulnerabilities at scale. arXiv preprint arXiv:2601.10338, 2026.

Zhiwei Liu, Weiran Yao, Jianguo Zhang, Liangwei Yang, Zuxin Liu, Juntao Tan, Prafulla K Choubey, Tian Lan, Jason Wu, Huan Wang, et al. Agentlite: A lightweight library for building and advancing task-oriented llm agent system. arXiv preprint arXiv:2402.15538, 2024c.

Zichang Liu, Aditya Desai, Fangshuo Liao, Weitao Wang, Victor Xie, Zhaozhuo Xu, Anastasios Kyrillidis, and Anshumali Shrivastava. Scissorhands: Exploiting the persistence of importance hypothesis for llm kv cache compression at test time. Advances in Neural Information Processing Systems, 36:52342–52364, 2023c.

Lin Long, Yichen He, Wentao Ye, Yiyuan Pan, Yuan Lin, Hang Li, Junbo Zhao, and Wei Li. Seeing, listening, remembering, and reasoning: A multimodal agent with long-term memory. arXiv preprint arXiv:2508.09736, 2025.

David Lopez-Paz and Marc’Aurelio Ranzato. Gradient episodic memory for continual learning. In NIPS, 2017.

Jiarui Lu, Thomas Holleis, Yizhe Zhang, Bernhard Aumayer, Feng Nan, Haoping Bai, Shuang Ma, Shen Ma, Mengyu Li, Guoli Yin, et al. Toolsandbox: A stateful, conversational, interactive evaluation benchmark for llm tool use capabilities. In Findings of the Association for Computational Linguistics: NAACL 2025, pp. 1160–1183, 2025a.

Junfeng Lu and Yueyan Li. Dynamic afective memory management for personalized llm agents. arXiv preprint arXiv:2510.27418, 2025.

Junru Lu, Siyu An, Mingbao Lin, Gabriele Pergola, Yulan He, Di Yin, Xing Sun, and Yunsheng Wu. Memochat: Tuning llms to use memos for consistent long-range open-domain conversation. arXiv preprint arXiv:2308.08239, 2023.

Miao Lu, Weiwei Sun, Weihua Du, Zhan Ling, Xuesong Yao, Kang Liu, and Jiecao Chen. Scaling llm multi-turn rl with end-to-end summarization-based context management. arXiv preprint arXiv:2510.06727, 2025b.

Yaxi Lu, Shenzhi Yang, Cheng Qian, Guirong Chen, Qinyu Luo, Yesai Wu, Huadong Wang, Xin Cong, Zhong Zhang, Yankai Lin, Weiwen Liu, Yasheng Wang, Zhiyuan Liu, Fangming Liu, and Maosong Sun. Proactive agent: Shifting LLM agents from reactive responses to active assistance. In The Thirteenth International Conference on Learning Representations, 2025c.

Elias Lumer, Anmol Gulati, Vamse Kumar Subbiah, Pradeep Honaganahalli Basavaraju, and James A Burke. Memtool: Optimizing short-term memory management for dynamic tool calling in llm agent multi-turn conversations. arXiv preprint arXiv:2507.21428, 2025.

Haoyan Luo and Lucia Specia. From understanding to utilization: A survey on explainability for large language models. arXiv preprint arXiv:2401.12874, 2024.

Junyu Luo, Weizhi Zhang, Ye Yuan, Yusheng Zhao, Junwei Yang, Yiyang Gu, Bohan Wu, Binqi Chen, Ziyue Qiao, Qingqing Long, et al. Large language model agent: A survey on methodology, applications and challenges. arXiv preprint arXiv:2503.21460, 2025.

Enze Ma, Yufan Zhou, Wei-Chieh Huang, Jie Yang, Huanhuan Ma, Zixuan Wang, Chengze Li, Chunyu Miao, Philip S. Yu, and Zhen Wang. Memprobe: Probing long-term agent memory via hidden user-state recovery. arXiv preprint arXiv:2606.24595, 2026.

Adyasha Maharana, Dong-Ho Lee, Sergey Tulyakov, Mohit Bansal, Francesco Barbieri, and Yuwei Fang. Evaluating very long-term conversational memory of llm agents. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 13851–13870, 2024.

Alex Mallen, Akari Asai, Victor Zhong, Rajarshi Das, Daniel Khashabi, and Hannaneh Hajishirzi. When not to trust language models: Investigating efectiveness of parametric and non-parametric memories. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 9802–9822, 2023.

Karttikeya Mangalam, Raiymbek Akshulakov, and Jitendra Malik. Egoschema: A diagnostic benchmark for very long-form video language understanding. Advances in Neural Information Processing Systems, 36: 46212–46244, 2023.

Reza Yousefi Maragheh and Yashar Deldjoo. The future is agentic: Definitions, perspectives, and open challenges of multi-agent recommender systems. arXiv preprint arXiv:2507.02097, 2025.

Alessio Maritan. Stafpro: an llm agent for joint stafing and profiling. arXiv preprint arXiv:2507.21636, 2025.

Vasilije Markovic, Lazar Obradovic, Laszlo Hajdu, and Jovan Pavlovic. Optimizing the interface between knowledge graphs and llms for complex reasoning. arXiv preprint arXiv:2505.24478, 2025.

Stephen J Martin, Paul D Grimwood, and Richard GM Morris. Synaptic plasticity and memory: an evaluation of the hypothesis. Annual review of neuroscience, 23(1):649–711, 2000.

Kevin Meng, David Bau, Alex Andonian, and Yonatan Belinkov. Locating and editing factual associations in gpt. Advances in neural information processing systems, 35:17359–17372, 2022.

Kevin Meng, Arnab Sen Sharma, Alex J Andonian, Yonatan Belinkov, and David Bau. Mass-editing memory in a transformer. In The Eleventh International Conference on Learning Representations, 2023.

Grégoire Mialon, Clémentine Fourrier, Thomas Wolf, Yann LeCun, and Thomas Scialom. Gaia: a benchmark for general ai assistants. In The Twelfth International Conference on Learning Representations, 2024.

Chunyu Miao, Henry Peng Zou, Yangning Li, Yankai Chen, Yibo Wang, Fangxin Wang, Yifan Li, Wooseong Yang, Bowei He, Xinni Zhang, et al. Recode-h: A benchmark for research code development with interactive human feedback. arXiv preprint arXiv:2510.06186, 2025.

Julie Michelman, Nasrin Baratalipour, and Matthew Abueg. Enhancing reasoning with collaboration and memory. arXiv preprint arXiv:2503.05944, 2025.

Sewon Min, Kalpesh Krishna, Xinxi Lyu, Mike Lewis, Wen-tau Yih, Pang Koh, Mohit Iyyer, Luke Zettlemoyer, and Hannaneh Hajishirzi. Factscore: Fine-grained atomic evaluation of factual precision in long form text generation. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pp. 12076–12100, 2023.

Shervin Minaee, Tomas Mikolov, Narjes Nikzad, Meysam Chenaghlu, Richard Socher, Xavier Amatriain, and Jianfeng Gao. Large language models: A survey. arXiv preprint arXiv:2402.06196, 2024.

Yuhang Ming, Minyang Xu, Xingrui Yang, Weicai Ye, Weihan Wang, Yong Peng, Weichen Dai, and Wanzeng Kong. Viper: Visual incremental place recognition with adaptive mining and continual learning. IEEE Robotics and Automation Letters, 2025.

Niloofar Mireshghallah and Tianshi Li. Position: Privacy is not just memorization! arXiv preprint arXiv:2510.01645, 2025.

Samuel Miserendino, Michele Wang, Tejal Patwardhan, and Johannes Heidecke. SWE-lancer: Can frontier LLMs earn \$1 million from real-world freelance software engineering? In Forty-second International Conference on Machine Learning, 2025.

Fengran Mo, Kelong Mao, Ziliang Zhao, Hongjin Qian, Haonan Chen, Yiruo Cheng, Xiaoxi Li, Yutao Zhu, Zhicheng Dou, and Jian-Yun Nie. A survey of conversational search. ACM Transactions on Information Systems, 43(6):1–50, 2025.

Ali Modarressi, Ayyoob Imani, Mohsen Fayyaz, and Hinrich Schütze. Ret-llm: Towards a general read-write memory for large language models. arXiv preprint arXiv:2305.14322, 2023.

Ali Modarressi, Abdullatif Köksal, Ayyoob Imani, Mohsen Fayyaz, and Hinrich Schütze. Memllm: Finetuning llms to use an explicit read-write memory. arXiv preprint arXiv:2404.11672, 2024.

Ruaridh Mon-Williams, Gen Li, Ran Long, Wenqian Du, and Christopher G Lucas. Embodied large language models enable robots to complete complex tasks in unpredictable environments. Nature Machine Intelligence, pp. 1–10, 2025.

Tsendsuren Munkhdalai, Manaal Faruqui, and Siddharth Gopal. Leave no context behind: Eficient infinite context transformers with infini-attention. arXiv preprint arXiv:2404.07143, 101, 2024.

Reiichiro Nakano, Jacob Hilton, Suchir Balaji, Jef Wu, Long Ouyang, Christina Kim, Christopher Hesse, Shantanu Jain, Vineet Kosaraju, William Saunders, et al. Webgpt: Browser-assisted question-answering with human feedback. arXiv preprint arXiv:2112.09332, 2021.

Jiayan Nan, Wenquan Ma, Wenlong Wu, and Yize Chen. Nemori: Self-organizing agent memory inspired by cognitive science. arXiv preprint arXiv:2508.03341, 2025.

Hongqiu Ni, Jiabao Zhang, Guopeng Li, Zilong Wang, Ruiqi Wu, Chi Zhang, and Haisheng Tan. Astraea: A state-aware scheduling engine for llm-powered agents. arXiv preprint arXiv:2512.14142, 2025.

NVIDIA. Nemo gym: An open source library for scaling reinforcement learning environments for llm. https://github.com/NVIDIA-NeMo/Gym, 2025. GitHub repository.

Parsa Omidi, Xingshuai Huang, Axel Laborieux, Bahareh Nikpour, Tianyu Shi, and Armaghan Eshaghi. Memory-augmented transformers: A systematic review from neuroscience principles to enhanced model architectures. arXiv preprint arXiv:2508.10824, 2025.

OpenAI. Memory and new controls for chatgpt, April 2025. URL https://openai.com/index/ memory-and-new-controls-for-chatgpt/.

Long Ouyang, Jefrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. Training language models to follow instructions with human feedback. Advances in neural information processing systems, 35:27730–27744, 2022.

Siru Ouyang, Jun Yan, I Hsu, Yanfei Chen, Ke Jiang, Zifeng Wang, Rujun Han, Long T Le, Samira Daruki, Xiangru Tang, et al. Reasoningbank: Scaling agent self-evolving with reasoning memory. arXiv preprint arXiv:2509.25140, 2025.

Charles Packer, Vivian Fang, Shishir G. Patil, Kevin Lin, Sarah Wooders, and Joseph\_E Gonzalez. Memgpt: Towards llms as operating systems. arXiv preprint arXiv:2310.08560, 2023.

Shankar Padmanabhan, Yasumasa Onoe, Michael Zhang, Greg Durrett, and Eunsol Choi. Propagating knowledge updates to lms through distillation. Advances in Neural Information Processing Systems, 36: 47124–47142, 2023.

Egor Pakhomov, Erik Nijkamp, and Caiming Xiong. Convomem benchmark: Why your first 150 conversations don’t need rag. arXiv preprint arXiv:2511.10523, 2025.

Zhuoshi Pan, Qianhui Wu, Huiqiang Jiang, Xufang Luo, Hao Cheng, Dongsheng Li, Yuqing Yang, Chin-Yew Lin, H Vicky Zhao, Lili Qiu, et al. Secom: On memory construction and retrieval for personalized conversational agents. In The Thirteenth International Conference on Learning Representations, 2025.

Dmitrii Pantiukhin, Boris Shapkin, Antonia Anna Jost, Ivan Kuznetsov, and Nikolay V Koldunov. Accelerating earth science discovery via multi-agent llm systems. Frontiers in Artificial Intelligence, 8:1674927, 2025.

Zachary A Pardos, Matthew Tang, Ioannis Anastasopoulos, Shreya K Sheel, and Ethan Zhang. Oatutor: An open-source adaptive tutoring system and curated content library for learning sciences research. In Proceedings of the 2023 chi conference on human factors in computing systems, pp. 1–17, 2023.

German I Parisi, Ronald Kemker, Jose L Part, Christopher Kanan, and Stefan Wermter. Continual lifelong learning with neural networks: A review. Neural networks, 113:54–71, 2019.

Joon Sung Park, Joseph O’Brien, Carrie Jun Cai, Meredith Ringel Morris, Percy Liang, and Michael S Bernstein. Generative agents: Interactive simulacra of human behavior. In Proceedings of the 36th annual acm symposium on user interface software and technology, pp. 1–22, 2023.

Yoon-Joo Park and Alexander Tuzhilin. The long tail of recommender systems and how to leverage it. In Proceedings of the 2008 ACM conference on Recommender systems, pp. 11–18, 2008.

Atharv Singh Patlan, Peiyao Sheng, S Ashwin Hebbar, Prateek Mittal, and Pramod Viswanath. Real ai agents with fake memories: Fatal context manipulation attacks on web3 agents. arXiv preprint arXiv:2503.16248, 2025.

Fabio Petroni, Aleksandra Piktus, Angela Fan, Patrick Lewis, Majid Yazdani, Nicola De Cao, James Thorne, Yacine Jernite, Vladimir Karpukhin, Jean Maillard, et al. Kilt: a benchmark for knowledge intensive language tasks. In Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, pp. 2523–2544, 2021.

Long Phan, Alice Gatti, Ziwen Han, Nathaniel Li, Josephina Hu, Hugh Zhang, Chen Bo Calvin Zhang, Mohamed Shaaban, John Ling, Sean Shi, et al. Humanity’s last exam. arXiv preprint arXiv:2501.14249, 2025.

Mathis Pink, Qinyuan Wu, Vy Ai Vo, Javier Turek, Jianing Mu, Alexander Huth, and Mariya Toneva. Position: Episodic memory is the missing piece for long-term llm agents. arXiv preprint arXiv:2502.06975, 2025.

Reiner Pope, Sholto Douglas, Aakanksha Chowdhery, Jacob Devlin, James Bradbury, Jonathan Heek, Kefan Xiao, Shivani Agrawal, and Jef Dean. Eficiently scaling transformer inference. Proceedings of machine learning and systems, 5:606–624, 2023.

Hadi Pouransari, David Grangier, C Thomas, Michael Kirchhof, and Oncel Tuzel. Pretraining with hierarchical memories: separating long-tail and common knowledge. arXiv preprint arXiv:2510.02375, 2025.

Viraj Prabhu, Yutong Dai, Matthew Fernandez, Jing Gu, Krithika Ramakrishnan, Yanqi Luo, Silvio Savarese, Caiming Xiong, Junnan Li, Zeyuan Chen, et al. Walt: Web agents that learn tools. arXiv preprint arXiv:2510.01524, 2025.

Chen Qian, Wei Liu, Hongzhang Liu, Nuo Chen, Yufan Dang, Jiahao Li, Cheng Yang, Weize Chen, Yusheng Su, Xin Cong, et al. Chatdev: Communicative agents for software development. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 15174–15186, 2024a.

Chen Qian, Zihao Xie, YiFei Wang, Wei Liu, Kunlun Zhu, Hanchen Xia, Yufan Dang, Zhuoyun Du, Weize Chen, Cheng Yang, et al. Scaling large language model-based multi-agent collaboration. In The Thirteenth International Conference on Learning Representations, 2025a.

Hongjin Qian, Zheng Liu, Peitian Zhang, Kelong Mao, Defu Lian, Zhicheng Dou, and Tiejun Huang. Memorag: Boosting long context processing with global memory-enhanced retrieval augmentation. In Proceedings of the ACM on Web Conference 2025, pp. 2366–2377, 2025b.

Rui Qian, Xiaoyi Dong, Pan Zhang, Yuhang Zang, Shuangrui Ding, Dahua Lin, and Jiaqi Wang. Streaming long video understanding with large language models. Advances in Neural Information Processing Systems, 37:119336–119360, 2024b.

Yujia Qin, Shihao Liang, Yining Ye, Kunlun Zhu, Lan Yan, Yaxi Lu, Yankai Lin, Xin Cong, Xiangru Tang, Bill Qian, et al. Toolllm: Facilitating large language models to master 16000+ real-world apis. In The Twelfth International Conference on Learning Representations, 2024.

Yujia Qin, Yining Ye, Junjie Fang, Haoming Wang, Shihao Liang, Shizuo Tian, Junda Zhang, Jiahao Li, Yunxin Li, Shijue Huang, et al. Ui-tars: Pioneering automated gui interaction with native agents. arXiv preprint arXiv:2501.12326, 2025.

Jielin Qiu, Zuxin Liu, Zhiwei Liu, Rithesh Murthy, Jianguo Zhang, Haolin Chen, Shiyu Wang, Ming Zhu, Liangwei Yang, Juntao Tan, et al. Locobench: A benchmark for long-context large language models in complex software engineering. arXiv preprint arXiv:2509.09614, 2025a.

Jielin Qiu, Zuxin Liu, Zhiwei Liu, Rithesh Murthy, Jianguo Zhang, Haolin Chen, Shiyu Wang, Ming Zhu, Liangwei Yang, Juntao Tan, et al. Locobench-agent: An interactive benchmark for llm agents in long-context software engineering. arXiv preprint arXiv:2511.13998, 2025b.

Derrick Quinn, Mohammad Nouri, Neel Patel, John Salihu, Alireza Salemi, Sukhan Lee, Hamed Zamani, and Mohammad Alian. Accelerating retrieval-augmented generation. In Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, Volume 1, pp. 15–32, 2025.

Jack W Rae, Anna Potapenko, Siddhant M Jayakumar, and Timothy P Lillicrap. Compressive transformers for long-range sequence modelling. arXiv preprint arXiv:1911.05507, 2019.

Shreyas Rajesh, Pavan Holur, Chenda Duan, David Chong, and Vwani Roychowdhury. Beyond fact retrieval: Episodic memory for rag with generative semantic workspaces. arXiv preprint arXiv:2511.07587, 2025.

Pranav Rajpurkar, Robin Jia, and Percy Liang. Know what you don’t know: Unanswerable questions for squad. In Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers), pp. 784–789, 2018.

Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais, Jack Ryan, and Daniel Chalef. Zep: a temporal knowledge graph architecture for agent memory. arXiv preprint arXiv:2501.13956, 2025.

Nikhila Ravi, Valentin Gabeur, Yuan-Ting Hu, Ronghang Hu, Chaitanya Ryali, Tengyu Ma, Haitham Khedr, Roman Rädle, Chloe Rolland, Laura Gustafson, et al. Sam 2: Segment anything in images and videos. arXiv preprint arXiv:2408.00714, 2024.

Sylvestre-Alvise Rebufi, Alexander Kolesnikov, Georg Sperl, and Christoph H. Lampert. icarl: Incremental classifier and representation learning. In CVPR, 2017.

Aniket Rege, Aditya Kusupati, Alan Fan, Qingqing Cao, Sham Kakade, Prateek Jain, Ali Farhadi, et al. Adanns: A framework for adaptive semantic search. Advances in Neural Information Processing Systems, 36:76311–76335, 2023.

Shuo Ren, Pu Jian, Zhenjiang Ren, Chunlin Leng, Can Xie, and Jiajun Zhang. Towards scientific intelligence: A survey of llm-based scientific agents. arXiv preprint arXiv:2503.24047, 2025.

Matthew Renze and Erhan Guven. Self-reflection in llm agents: Efects on problem-solving performance. arXiv preprint arXiv:2405.06682, 2024.

Alireza Rezazadeh, Zichao Li, Ange Lou, Yuying Zhao, Wei Wei, and Yujia Bao. Collaborative memory: Multi-user memory sharing in llm agents with dynamic access control. arXiv preprint arXiv:2505.18279, 2025a.

Alireza Rezazadeh, Zichao Li, Wei Wei, and Yujia Bao. From isolated conversations to hierarchical schemas: Dynamic tree memory representation for llms. In The Thirteenth International Conference on Learning Representations, 2025b.

Alsu Sagirova, Yuri Kuratov, and Mikhail Burtsev. Srmt: shared memory for multi-agent lifelong pathfinding. arXiv preprint arXiv:2501.13200, 2025.

Gobinda Saha, Isha Garg, and Kaushik Roy. Gradient projection memory for continual learning. In International Conference on Learning Representations, 2021.

Rana Salama, Jason Cai, Michelle Yuan, Anna Currey, Monica Sunkara, Yi Zhang, and Yassine Benajiba. Meminsight: Autonomous memory augmentation for llm agents. arXiv preprint arXiv:2503.21760, 2025.

Alireza Salemi, Sheshera Mysore, Michael Bendersky, and Hamed Zamani. Lamp: When large language models meet personalization. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 7370–7392, 2024.

Ankur Samanta, Akshayaa Magesh, Youliang Yu, Runzhe Wu, Ayush Jain, Daniel Jiang, Boris Vidolov, Paul Sajda, Yonathan Efroni, and Kaveh Hassani. Internalizing self-consistency in language models: Multi-agent consensus alignment. arXiv preprint arXiv:2509.15172, 2025.

Vinay Samuel, Henry Peng Zou, Yue Zhou, Shreyas Chaudhari, Ashwin Kalyan, Tanmay Rajpurohit, Ameet Deshpande, Karthik Narasimhan, and Vishvak Murahari. Personagym: Evaluating persona agents and llms. arXiv preprint arXiv:2407.18416, 2024.

Samarth Sarin, Lovepreet Singh, Bhaskarjit Sarmah, and Dhagash Mehta. Memoria: A scalable agentic memory framework for personalized conversational ai. arXiv preprint arXiv:2512.12686, 2025.

Parth Sarthi, Salman Abdullah, Aditi Tuli, Shubh Khanna, Anna Goldie, and Christopher D Manning. Raptor: Recursive abstractive processing for tree-organized retrieval. In The Twelfth International Conference on Learning Representations, 2024.

Nikolay Savinov, Anton Raichuk, Damien Vincent, Raphael Marinier, Marc Pollefeys, Timothy Lillicrap, and Sylvain Gelly. Episodic curiosity through reachability. In International Conference on Learning Representations, 2019.

Rohit Saxena, Hao Tang, and Frank Keller. End-to-end long document summarization using gradient caching. Transactions of the Association for Computational Linguistics, 13:1271–1297, 2025.

Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Eric Hambro, Luke Zettlemoyer, Nicola Cancedda, and Thomas Scialom. Toolformer: Language models can teach themselves to use tools. Advances in Neural Information Processing Systems, 36:68539–68551, 2023.

Samuel Schmidgall, Yusheng Su, Ze Wang, Ximeng Sun, Jialian Wu, Xiaodong Yu, Jiang Liu, Zicheng Liu, and Emad Barsoum. Agent laboratory: Using llm agents as research assistants. arXiv preprint arXiv:2501.04227, 2025.

Julian Schrittwieser, Ioannis Antonoglou, Thomas Hubert, Karen Simonyan, Laurent Sifre, Simon Schmitt, Arthur Guez, Edward Lockhart, Demis Hassabis, Thore Graepel, et al. Mastering atari, go, chess and shogi by planning with a learned model. Nature, 588(7839):604–609, 2020.

Joan Serra, Didac Suris, Marius Miron, and Alexandros Karatzoglou. Overcoming catastrophic forgetting with hard attention to the task. In International conference on machine learning, pp. 4548–4557. PMLR, 2018.

Lior Shani, Aviv Rosenberg, Asaf Cassel, Oran Lang, Daniele Calandriello, Avital Zipori, Hila Noga, Orgad Keller, Bilal Piot, Idan Szpektor, et al. Multi-turn reinforcement learning with preference human feedback. Advances in Neural Information Processing Systems, 37:118953–118993, 2024.

Jiaqi Shao, Yuxiang Lin, Munish Prasad Lohani, Yufeng Miao, and Bing Luo. Do llm agents know how to ground, recover, and assess? a benchmark for epistemic competence in information-seeking agents. arXiv preprint arXiv:2509.22391, 2025.

Yifan Shao, Peilin Zhou, Shoujin Wang, Weizhi Zhang, Sunghun Kim, and Xu Cai. Dtrec: Learning dynamic reasoning trajectories for sequential recommendation. In Proceedings of the ACM Web Conference 2026, pp. 8549–8552, 2026.

Yunfan Shao, Linyang Li, Junqi Dai, and Xipeng Qiu. Character-llm: A trainable agent for role-playing. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pp. 13153–13187, 2023.

Chen Shen, Wanqing Zhang, Kehan Li, Erwen Huang, Haitao Bi, Aiying Fan, Yiwen Shen, Hongmei Dong, Ji Zhang, Yuming Shao, et al. Feat: A multi-agent forensic ai system with domain-adapted large language model for automated cause-of-death analysis. arXiv preprint arXiv:2508.07950, 2025.

Juanming Shi, Qinglang Guo, Yong Liao, and Shenglin Liang. Legalgpt: legal chain of thought for the legal large language model multi-agent framework. In International Conference on Intelligent Computing, pp. 25–37. Springer, 2024.

Yaorui Shi, Yuxin Chen, Siyuan Wang, Sihang Li, Hengxing Cai, Qi Gu, Xiang Wang, and An Zhang. Look back to reason forward: Revisitable memory for long-context llm agents. arXiv preprint arXiv:2509.23040, 2025a.

Zitong Shi, Guancheng Wan, Wenke Huang, Guibin Zhang, Jiawei Shao, Mang Ye, and Carl Yang. Privacyenhancing paradigms within federated multi-agent systems. In ICML 2025 Workshop on Collaborative and Federated Agentic Workflows, 2025b.

Hanul Shin, Jung Kwon Lee, Jaehong Kim, and Jiwon Kim. Continual learning with deep generative replay. In NIPS, 2017.

Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflexion: Language agents with verbal reinforcement learning. Advances in Neural Information Processing Systems, 36:8634– 8652, 2023.

Mohit Shridhar, Jesse Thomason, Daniel Gordon, Yonatan Bisk, Winson Han, Roozbeh Mottaghi, Luke Zettlemoyer, and Dieter Fox. Alfred: A benchmark for interpreting grounded instructions for everyday tasks. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pp. 10740–10749, 2020.

Mohit Shridhar, Xingdi Yuan, Marc-Alexandre Cote, Yonatan Bisk, Adam Trischler, and Matthew Hausknecht. Alfworld: Aligning text and embodied environments for interactive learning. In International Conference on Learning Representations, 2021.

David Silver, Hado Hasselt, Matteo Hessel, Tom Schaul, Arthur Guez, Tim Harley, Gabriel Dulac-Arnold, David Reichert, Neil Rabinowitz, Andre Barreto, et al. The predictron: End-to-end learning and planning. In International Conference on Machine Learning, pp. 3191–3199. PMLR, 2017.

Kunal Pratap Singh, Jordi Salvador, Luca Weihs, and Aniruddha Kembhavi. Scene graph contrastive learning for embodied navigation. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pp. 10884–10894, 2023.

Xinyuan Song, Hongji Pu, and Liang Zhao. Skillops: Managing llm agent skill libraries as self-maintaining software ecosystems. arXiv preprint arXiv:2605.13716, 2026.

George Sperling. The information available in brief visual presentations. Psychological monographs: General and applied, 74(11):1, 1960.

Larry R Squire. Memory and the hippocampus: a synthesis from findings with rats, monkeys, and humans. Psychological review, 99(2):195, 1992.

Giulio Starace, Oliver Jafe, Dane Sherburn, James Aung, Jun Shern Chan, Leon Maksin, Rachel Dias, Evan Mays, Benjamin Kinsella, Wyatt Thompson, et al. Paperbench: Evaluating ai’s ability to replicate ai research. In Forty-second International Conference on Machine Learning, 2025.

Theodore Sumers, Shunyu Yao, Karthik Narasimhan, and Thomas Grifiths. Cognitive architectures for language agents. Transactions on Machine Learning Research, 2023.

Haoran Sun and Shaoning Zeng. Hierarchical memory for high-eficiency long-term reasoning in llm agents. arXiv preprint arXiv:2507.22925, 2025.

Haoran Sun, Zekun Zhang, and Shaoning Zeng. Preference-aware memory update for long-term llm agents. arXiv preprint arXiv:2510.09720, 2025a.

Weiwei Sun, Miao Lu, Zhan Ling, Kang Liu, Xuesong Yao, Yiming Yang, and Jiecao Chen. Scaling long-horizon llm agent via context-folding. arXiv preprint arXiv:2510.11967, 2025b.

Mirac Suzgun, Mert Yuksekgonul, Federico Bianchi, Dan Jurafsky, and James Zou. Dynamic cheatsheet: Test-time learning with adaptive memory. arXiv preprint arXiv:2504.07952, 2025.

Valentin Tablan, Scott Taylor, Gabriel Hurtado, Kristofer Bernhem, Anders Uhrenholt, Gabriele Farei, and Karo Moilanen. Smarter together: Creating agentic communities of practice through shared experiential learning. arXiv preprint arXiv:2511.08301, 2025.

Jihoon Tack, Jaehyung Kim, Eric Mitchell, Jinwoo Shin, Yee Whye Teh, and Jonathan Richard Schwarz. Online adaptation of language models with a memory of amortized contexts. Advances in Neural Information Processing Systems, 37:130109–130135, 2024.

Yashar Talebirad and Amirhossein Nadiri. Multi-agent collaboration: Harnessing the power of intelligent llm agents. arXiv preprint arXiv:2306.03314, 2023.

Haoran Tan, Zeyu Zhang, Chen Ma, Xu Chen, Quanyu Dai, and Zhenhua Dong. Membench: Towards more comprehensive evaluation on the memory of llm-based agents. arXiv preprint arXiv:2506.21605, 2025a.

Xingyu Tan, Xiaoyang Wang, Qing Liu, Xiwei Xu, Xin Yuan, Liming Zhu, and Wenjie Zhang. Memotime: Memory-augmented temporal knowledge graph enhanced large language model reasoning. arXiv preprint arXiv:2510.13614, 2025b.

Zhaoxuan Tan, Qingkai Zeng, Yijun Tian, Zheyuan Liu, Bing Yin, and Meng Jiang. Democratizing large language models via personalized parameter-eficient fine-tuning. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, pp. 6476–6491, 2024a.

Zhen Tan, Chengshuai Zhao, Raha Morafah, Yifan Li, Song Wang, Jundong Li, Tianlong Chen, and Huan Liu. Glue pizza and eat rocks-exploiting vulnerabilities in retrieval-augmented generative models. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, pp. 1610–1626, 2024b.

Zhen Tan, Jun Yan, I-Hung Hsu, Rujun Han, Zifeng Wang, Long Le, Yiwen Song, Yanfei Chen, Hamid Palangi, George Lee, et al. In prospect and retrospect: Reflective memory management for long-term personalized dialogue agents. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 8416–8439, 2025c.

Jing Tang, Hongru Xiao, Xiang Li, Wei Wang, and Zeyu Gong. Chatcad: An mllm-guided framework for zero-shot cad drawing restoration. In ICASSP 2025-2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pp. 1–5. IEEE, 2025a.

Xiangru Tang, Anni Zou, Zhuosheng Zhang, Ziming Li, Yilun Zhao, Xingyao Zhang, Arman Cohan, and Mark Gerstein. Medagents: Large language models as collaborators for zero-shot medical reasoning. In Findings of the Association for Computational Linguistics: ACL 2024, pp. 599–621, 2024.

Xiangru Tang, Tianrui Qin, Tianhao Peng, Ziyang Zhou, Daniel Shao, Tingting Du, Xinming Wei, Peng Xia, Fang Wu, He Zhu, et al. Agent kb: Leveraging cross-domain experience for agentic problem solving. arXiv preprint arXiv:2507.06229, 2025b.

Mohammad Tavakoli, Alireza Salemi, Carrie Ye, Mohamed Abdalla, Hamed Zamani, and J Ross Mitchell. Beyond a million tokens: Benchmarking and enhancing long-term memory in llms. arXiv preprint arXiv:2510.27246, 2025.

NovelSeek Team, Bo Zhang, Shiyang Feng, Xiangchao Yan, Jiakang Yuan, Zhiyin Yu, Xiaohan He, Songtao Huang, Shaowei Hou, Zheng Nie, et al. Novelseek: When agent becomes the scientist–building closed-loop system from hypothesis to verification. arXiv preprint arXiv:2505.16938, 2025.

Alessandra Terranova, Björn Ross, and Alexandra Birch. Evaluating long-term memory for long-context question answering. arXiv preprint arXiv:2510.23730, 2025.

Ao Tian, Yunfeng Lu, Xinxin Fan, Changhao Wang, Lanzhi Zhou, Yeyao Zhang, and Yanfang Liu. Rgmem: Renormalization group-based memory evolution for language agent user profile. arXiv preprint arXiv:2510.16392, 2025.

Yu Tian, Xiao Yang, Jingyuan Zhang, Yinpeng Dong, and Hang Su. Evil geniuses: Delving into the safety of llm-based agents. arXiv preprint arXiv:2311.11855, 2023.

Susumu Tonegawa, Michele Pignatelli, Dheeraj S Roy, and Tomás J Ryan. Memory engram storage and retrieval. Current opinion in neurobiology, 35:101–109, 2015.

Linh Tran, Wei Sun, Stacy Patterson, and Ana Milanova. Privacy-preserving personalized federated prompt learning for multimodal large language models. In International Conference on Learning Representations, 2025.

Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, and Ashish Sabharwal. Musique: Multihop questions via single-hop question composition. Transactions of the Association for Computational Linguistics, 10: 539–554, 2022.

Harsh Trivedi, Tushar Khot, Mareike Hartmann, Ruskin Manku, Vinty Dong, Edward Li, Shashank Gupta, Ashish Sabharwal, and Niranjan Balasubramanian. Appworld: A controllable world of apps and people for benchmarking interactive coding agents. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 16022–16076, 2024.

Endel Tulving. Episodic and semantic memory. In Endel Tulving and Wayne Donaldson (eds.), Organization of Memory, pp. 381–403. Academic Press, 1972.

Endel Tulving. Elements of episodic memory. Oxford University Press, 1983.

Endel Tulving. Memory and consciousness. Canadian Psychology/Psychologie canadienne, 26(1):1, 1985.

Endel Tulving. Episodic memory: From mind to brain. Annual review of psychology, 53(1):1–25, 2002.

Szymon Tworkowski, Konrad Staniszewski, Mikołaj Pacek, Yuhuai Wu, Henryk Michalewski, and Piotr Miłoś. Focused transformer: Contrastive training for context scaling. Advances in neural information processing systems, 36:42661–42688, 2023.

Georgios Tziafas and Hamidreza Kasaei. Lifelong robot library learning: Bootstrapping composable and generalizable skills for embodied control with language models. In 2024 IEEE International Conference on Robotics and Automation (ICRA), pp. 515–522. IEEE, 2024.

Nidadavolu Venkat Durga Sai Siva Vara, Prasad Raju, Nuruzzaman Faruqui, Nikhil Patel, Olivia-Roxana Alecsoiu, Priyabrata Thatoi, Salem A Alyami, and AKM Azad. Legalmind: Agentic ai-driven process optimization and cost reduction in legal services using deepseek. IEEE Access, 2025.

Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. Advances in neural information processing systems, 30, 2017.

S Velliangiri, V Anbarasu, P Karthikeyan, and SP Anandaraj. Intelligent personal health monitoring and guidance using long short-term memory. Journal of Mobile Multimedia, 18(2):349–371, 2022.

Ao Wang, Hui Chen, Jiaxin Li, Jianchao Tan, Kefeng Zhang, Xunliang Cai, Zijia Lin, Jungong Han, and Guiguang Ding. Prefixkv: Adaptive prefix kv cache is what vision instruction-following models need for eficient generation. arXiv preprint arXiv:2412.03409, 2024a.

Bing Wang, Xinnian Liang, Jian Yang, Hui Huang, Shuangzhi Wu, Peihao Wu, Lu Lu, Zejun Ma, and Zhoujun Li. Scm: Enhancing large language model with self-controlled memory framework. arXiv e-prints, pp. arXiv–2304, 2023a.

Bo Wang, Weiyi He, Shenglai Zeng, Zhen Xiang, Yue Xing, Jiliang Tang, and Pengfei He. Unveiling privacy risks in llm agent memory. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 25241–25260, 2025a.

Bo Wang, Jiehong Lin, Chenzhi Liu, Xinting Hu, Yifei Yu, Tianjia Liu, Zhongrui Wang, and Xiaojuan Qi. Mg-nav: Dual-scale visual navigation via sparse spatial memory. arXiv preprint arXiv:2511.22609, 2025b.

Danqing Wang, Kevin Yang, Hanlin Zhu, Xiaomeng Yang, Andrew Cohen, Lei Li, and Yuandong Tian. Learning personalized alignment for evaluating open-ended text generation. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, pp. 13274–13292, 2024b.

Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and Anima Anandkumar. Voyager: An open-ended embodied agent with large language models. Transactions on Machine Learning Research, 2025c.

Hao Wang, Jialun Zhong, Changcheng Wang, Zhujun Nie, Zheng Li, Shunyu Yao, Yanzeng Li, and Xinchi Li. Seal: Self-evolving agentic learning for conversational question answering over knowledge graphs. arXiv preprint arXiv:2512.04868, 2025d.

Haoming Wang, Haoyang Zou, Huatong Song, Jiazhan Feng, Junjie Fang, Junting Lu, Longxiang Liu, Qinyu Luo, Shihao Liang, Shijue Huang, et al. Ui-tars-2 technical report: Advancing gui agent with multi-turn reinforcement learning. arXiv preprint arXiv:2509.02544, 2025e.

Jiayu Wang, Yifei Ming, Riya Dulepet, Qinglin Chen, Austin Xu, Zixuan Ke, Frederic Sala, Aws Albarghouthi, Caiming Xiong, and Shafiq Joty. Liveresearchbench: A live benchmark for user-centric deep research in the wild. arXiv preprint arXiv:2510.14240, 2025f.

Junjian Wang, Lidan Zhao, and Xi Sheryl Zhang. Madra: Multi-agent debate for risk-aware embodied planning. arXiv preprint arXiv:2511.21460, 2025g.

Junyang Wang, Haiyang Xu, Haitao Jia, Xi Zhang, Ming Yan, Weizhou Shen, Ji Zhang, Fei Huang, and Jitao Sang. Mobile-agent-v2: Mobile device operation assistant with efective navigation via multi-agent collaboration. Advances in Neural Information Processing Systems, 37:2686–2710, 2024c.

Lei Wang, Wanyu Xu, Yihuai Lan, Zhiqiang Hu, Yunshi Lan, Roy Ka-Wei Lee, and Ee-Peng Lim. Plan-and solve prompting: Improving zero-shot chain-of-thought reasoning by large language models. arXiv preprint arXiv:2305.04091, 2023b.

Lei Wang, Chen Ma, Xueyang Feng, Zeyu Zhang, Hao Yang, Jingsen Zhang, Zhiyuan Chen, Jiakai Tang, Xu Chen, Yankai Lin, et al. A survey on large language model based autonomous agents. Frontiers of Computer Science, 18(6):186345, 2024d.

Lei Wang, Jingsen Zhang, Hao Yang, Zhi-Yuan Chen, Jiakai Tang, Zeyu Zhang, Xu Chen, Yankai Lin, Hao Sun, Ruihua Song, et al. User behavior simulation with large language model-based agents. ACM Transactions on Information Systems, 43(2):1–37, 2025h.

Noah Wang, Zy Peng, Haoran Que, Jiaheng Liu, Wangchunshu Zhou, Yuhan Wu, Hongcheng Guo, Ruitong Gan, Zehao Ni, Jian Yang, et al. Rolellm: Benchmarking, eliciting, and enhancing role-playing abilities of large language models. In Findings of the Association for Computational Linguistics: ACL 2024, pp. 14743–14777, 2024e.

Peng Wang, Zexi Li, Ningyu Zhang, Ziwen Xu, Yunzhi Yao, Yong Jiang, Pengjun Xie, Fei Huang, and Huajun Chen. Wise: Rethinking the knowledge memory for lifelong model editing of large language models. Advances in Neural Information Processing Systems, 37:53764–53797, 2024f.

Piaohong Wang, Motong Tian, Jiaxian Li, Yuan Liang, Yuqing Wang, Qianben Chen, Tiannan Wang, Zhicong Lu, Jiawei Ma, Yuchen Eleanor Jiang, et al. O-mem: Omni memory system for personalized, long horizon, self-evolving agents. arXiv e-prints, pp. arXiv–2511, 2025i.

Qingyue Wang, Yanhe Fu, Yanan Cao, Shuai Wang, Zhiliang Tian, and Liang Ding. Recursively summarizing enables long-term dialogue memory in large language models. Neurocomputing, 639:130193, 2025j.

Rui Wang, Yonghe Chen, Weiyu Zhang, Jiasheng Si, Hongjiao Guan, Xueping Peng, and Wenpeng Lu. Medconma: A confidence-driven multi-agent framework for medical q&a. In Pacific-Asia Conference on Knowledge Discovery and Data Mining, pp. 421–433. Springer, 2025k.

Ruoyao Wang, Peter Jansen, Marc-Alexandre Côté, and Prithviraj Ammanabrolu. Scienceworld: Is your agent smarter than a 5th grader? In Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing, pp. 11279–11298, 2022.

Saizhuo Wang, Hang Yuan, Lionel M Ni, and Jian Guo. Quantagent: Seeking holy grail in trading by self-improving large language model. arXiv preprint arXiv:2402.03755, 2024g.

Song Wang, Yaochen Zhu, Haochen Liu, Zaiyi Zheng, Chen Chen, and Jundong Li. Knowledge editing for large language models: A survey. ACM Computing Surveys, 57(3):1–37, 2024h.

Tianfu Wang, Yi Zhan, Jianxun Lian, Zhengyu Hu, Nicholas Jing Yuan, Qi Zhang, Xing Xie, and Hui Xiong. Llm-powered multi-agent framework for goal-oriented learning in intelligent tutoring system. In Companion Proceedings of the ACM on Web Conference 2025, pp. 510–519, 2025l.

Tiannan Wang, Meiling Tao, Ruoyu Fang, Huilin Wang, Shuai Wang, Yuchen Eleanor Jiang, and Wangchunshu Zhou. Ai persona: Towards life-long personalization of llms. arXiv preprint arXiv:2412.13103, 2024i.

Weizhi Wang, Li Dong, Hao Cheng, Xiaodong Liu, Xifeng Yan, Jianfeng Gao, and Furu Wei. Augmenting language models with long-term memory. Advances in Neural Information Processing Systems, 36:74530– 74543, 2023c.

Xiaoqiang Wang, Suyuchen Wang, and Yun Zhu. R<sup>3</sup>Mem: Bridging memory retention and retrieval via reversible compression. In Findings of the Association for Computational Linguistics: ACL 2025, pp. 4541– 4557, Vienna, Austria, July 2025m. Association for Computational Linguistics. ISBN 979-8-89176-256-5. doi: 10.18653/v1/2025.findings-acl.235.

Xingyao Wang, Zihan Wang, Jiateng Liu, Yangyi Chen, Lifan Yuan, Hao Peng, and Heng Ji. MINT: Evaluating LLMs in multi-turn interaction with tools and language feedback. In The Twelfth International Conference on Learning Representations, 2024j.

Xingyao Wang, Boxuan Li, Yufan Song, Frank F Xu, Xiangru Tang, Mingchen Zhuge, Jiayi Pan, Yueqi Song, Bowen Li, Jaskirat Singh, et al. Openhands: An open platform for ai software developers as generalist agents. In The Thirteenth International Conference on Learning Representations, 2025n.

Yancheng Wang, Ziyan Jiang, Zheng Chen, Fan Yang, Yingxue Zhou, Eunah Cho, Xing Fan, Yanbin Lu, Xiaojiang Huang, and Yingzhen Yang. Recmind: Large language model powered agent for recommendation. In Findings of the Association for Computational Linguistics: NAACL 2024, pp. 4351–4364, 2024k.

Yu Wang and Xi Chen. Mirix: Multi-agent memory system for llm-based agents. arXiv preprint arXiv:2507.07957, 2025.

Yu Wang, Yifan Gao, Xiusi Chen, Haoming Jiang, Shiyang Li, Jingfeng Yang, Qingyu Yin, Zheng Li, Xian Li, Bing Yin, et al. Memoryllm: towards self-updatable large language models. In Proceedings of the 41st International Conference on Machine Learning, pp. 50453–50466, 2024l.

Yu Wang, Dmitry Krotov, Yuanzhe Hu, Yifan Gao, Wangchunshu Zhou, Julian McAuley, Dan Gutfreund, Rogerio Feris, and Zexue He. M+: Extending memoryllm with scalable long-term memory. arXiv preprint arXiv:2502.00592, 2025o.

Yu Wang, Xinshuang Liu, Xiusi Chen, Sean O’Brien, Junda Wu, and Julian McAuley. Self-updatable large language models by integrating context into model parameters. In The Thirteenth International Conference on Learning Representations, 2025p.

Yu Wang, Ryuichi Takanobu, Zhiqi Liang, Yuzhen Mao, Yuanzhe Hu, Julian McAuley, and Xiaojian Wu. Mem-α: Learning memory construction via reinforcement learning. arXiv preprint arXiv:2509.25911, 2025q.

Yu Wang, Ruihan Wu, Zexue He, Xiusi Chen, and Julian McAuley. Large scale knowledge washing. In The Thirteenth International Conference on Learning Representations, 2025r.

Yubo Wang, Xueguang Ma, Ge Zhang, Yuansheng Ni, Abhranil Chandra, Shiguang Guo, Weiming Ren, Aaran Arulraj, Xuan He, Ziyan Jiang, et al. Mmlu-pro: A more robust and challenging multi-task language understanding benchmark. Advances in Neural Information Processing Systems, 37:95266–95290, 2024m.

Zhao Wang, Sota Moriyama, Wei-Yao Wang, Briti Gangopadhyay, and Shingo Takamatsu. Talk structurally, act hierarchically: A collaborative framework for llm multi-agent systems. arXiv preprint arXiv:2502.11098, 2025s.

Zheng Wang, Zhongyang Li, Zeren Jiang, Dandan Tu, and Wei Shi. Crafting personalized agents through retrieval-augmented generation on editable memory graphs. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, pp. 4891–4906, 2024n.

Zhiruo Wang, Daniel Fried, and Graham Neubig. Trove: Inducing verifiable and eficient toolboxes for solving programmatic tasks. arXiv preprint arXiv:2401.12869, 2024o.

Zihan Wang, Xiangyang Li, Jiahao Yang, Yeqi Liu, and Shuqiang Jiang. Gridmm: Grid memory map for vision-and-language navigation. In Proceedings of the IEEE/CVF International conference on computer vision, pp. 15625–15636, 2023d.

Zihao Wang, Shaofei Cai, Anji Liu, Yonggang Jin, Jinbing Hou, Bowei Zhang, Haowei Lin, Zhaofeng He, Zilong Zheng, Yaodong Yang, et al. Jarvis-1: Open-world multi-task agents with memory-augmented multimodal language models. IEEE Transactions on Pattern Analysis and Machine Intelligence, 2024p.

Zixuan Wang, Bo Yu, Junzhe Zhao, Wenhao Sun, Sai Hou, Shuai Liang, Xing Hu, Yinhe Han, and Yiming Gan. Karma: Augmenting embodied ai agents with long-and-short term memory systems. In 2025 IEEE International Conference on Robotics and Automation (ICRA), pp. 1–8. IEEE, 2025t.

Zora Zhiruo Wang, Apurva Gandhi, Graham Neubig, and Daniel Fried. Inducing programmatic skills for agentic tasks. arXiv preprint arXiv:2504.06821, 2025u.

Zora Zhiruo Wang, Jiayuan Mao, Daniel Fried, and Graham Neubig. Agent workflow memory. In Forty-second International Conference on Machine Learning, 2025v.

Hao Wei, Jianing Qiu, Haibao Yu, and Wu Yuan. Medco: Medical education copilots based on a multi-agent framework. In European Conference on Computer Vision, pp. 119–135. Springer, 2024.

Jason Wei, Zhiqing Sun, Spencer Papay, Scott McKinney, Jefrey Han, Isa Fulford, Hyung Won Chung, Alex Tachard Passos, William Fedus, and Amelia Glaese. Browsecomp: A simple yet challenging benchmark for browsing agents. arXiv preprint arXiv:2504.12516, 2025a.

Qianshan Wei, Tengchao Yang, Yaochen Wang, Xinfeng Li, Lijun Li, Zhenfei Yin, Yi Zhan, Thorsten Holz, Zhiqiang Lin, and XiaoFeng Wang. A-memguard: A proactive defense framework for llm-based agent memory. arXiv preprint arXiv:2510.02373, 2025b.

Rubin Wei, Jiaqi Cao, Jiarui Wang, Jushi Kai, Qipeng Guo, Bowen Zhou, and Zhouhan Lin. Mlp memory: A retriever-pretrained memory for large language models. arXiv preprint arXiv:2508.01832, 2025c.

Tianxin Wei, Noveen Sachdeva, Benjamin Coleman, Zhankui He, Yuanchen Bei, Xuying Ning, Mengting Ai, Yunzhe Li, Jingrui He, Ed H Chi, et al. Evo-memory: Benchmarking llm agent test-time learning with self-evolving memory. arXiv preprint arXiv:2511.20857, 2025d.

Zhepei Wei, Wenlin Yao, Yao Liu, Weizhi Zhang, Qin Lu, Liang Qiu, Changlong Yu, Puyang Xu, Chao Zhang, Bing Yin, et al. Webagent-r1: Training web agents via end-to-end multi-turn reinforcement learning. arXiv preprint arXiv:2505.16421, 2025e.

Hannes Westermann. Dallma: Semi-structured legal reasoning and drafting with large language models. In 2nd Workshop on Generative AI and Law, 2024.

Rebecca Westhäußer, Wolfgang Minker, and Sebatian Zepf. Enabling personalized long-term interactions in llm-based agents through persistent memory and user profiles. arXiv preprint arXiv:2510.07925, 2025.

Schaun Wheeler and Olivier Jeunen. Procedural memory is not all you need: Bridging cognitive gaps in llm-based agents. In Adjunct Proceedings of the 33rd ACM Conference on User Modeling, Adaptation and Personalization, pp. 360–364, 2025.

Bowen Wu, Wenqing Wang, Lihaoran Lihaoran, Yunhan Deng, Ying Li, Jingsong Yu, and Baoxun Wang. Interpersonal memory matters: A new task for proactive dialogue utilizing conversational history. In Proceedings of the 29th Conference on Computational Natural Language Learning, pp. 47–67, 2025a.

Di Wu, Hongwei Wang, Wenhao Yu, Yuwei Zhang, Kai-Wei Chang, and Dong Yu. Longmemeval: Bench marking chat assistants on long-term interactive memory. In The Thirteenth International Conference on Learning Representations, 2025b.

Haoning Wu, Dongxu Li, Bei Chen, and Junnan Li. Longvideobench: A benchmark for long-context interleaved video-language understanding. Advances in Neural Information Processing Systems, 37:28828–28857, 2024a.

Junde Wu, Jiayuan Zhu, Yuyuan Liu, Min Xu, and Yueming Jin. Agentic reasoning: A streamlined framework for enhancing llm reasoning with agentic tools. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 28489–28503, 2025c.

Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun Zhang, Shaokun Zhang, Jiale Liu, et al. Autogen: Enabling next-gen llm applications via multi-agent conversations. In First Conference on Language Modeling, 2024b.

Shanglin Wu and Kai Shu. Memory in llm-based multi-agent systems: Mechanisms, challenges, and collective intelligence. Authorea Preprints, 2025.

Shiwei Wu, Joya Chen, Kevin Qinghong Lin, Qimeng Wang, Yan Gao, Qianli Xu, Tong Xu, Yao Hu, Enhong Chen, and Mike Zheng Shou. Videollm-mod: Eficient video-language streaming with mixture-of-depths vision computation. Advances in Neural Information Processing Systems, 37:109922–109947, 2024c.

Xixi Wu, Kuan Li, Yida Zhao, Liwen Zhang, Litu Ou, Huifeng Yin, Zhongwang Zhang, Xinmiao Yu, Dingchu Zhang, Yong Jiang, et al. Resum: Unlocking long-horizon search intelligence via context summarization. arXiv preprint arXiv:2509.13313, 2025d.

Yaozu Wu, Jizhou Guo, Dongyuan Li, Henry Peng Zou, Wei-Chieh Huang, Yankai Chen, Zhen Wang, Weizhi Zhang, Yangning Li, Meng Zhang, et al. Psg-agent: Personality-aware safety guardrail for llm-based agents. arXiv preprint arXiv:2509.23614, 2025e.

Yaozu Wu, Dongyuan Li, Yankai Chen, Renhe Jiang, Henry Peng Zou, Wei-Chieh Huang, Yangning Li, Liancheng Fang, Zhen Wang, and Philip S Yu. Multi-agent autonomous driving systems with large language models: A survey of recent advances, resources, and future directions. Findings of the Association for Computational Linguistics: EMNLP, 2025, 2025f.

Yaozu Wu, Wei-Chieh Huang, Jizhou Guo, Dongyuan Li, Renhe Jiang, Henry Peng Zou, Chunyu Miao, Shanghao Li, Weizhi Zhang, WeiWei Ye, et al. Has-bench: Evaluating llm-based human-agent systems under configurable human participation. arXiv preprint arXiv:2607.04329, 2026.

Yaxiong Wu, Sheng Liang, Chen Zhang, Yichao Wang, Yongyue Zhang, Huifeng Guo, Ruiming Tang, and Yong Liu. From human memory to ai memory: A survey on memory mechanisms in the era of llms. arXiv preprint arXiv:2504.15965, 2025g.

Yunjia Xi, Weiwen Liu, Jianghao Lin, Bo Chen, Ruiming Tang, Weinan Zhang, and Yong Yu. Memocrs: Memory-enhanced sequential conversational recommender systems with large language models. In Proceedings of the 33rd ACM International Conference on Information and Knowledge Management, pp. 2585–2595, 2024.

Zhiheng Xi, Wenxiang Chen, Xin Guo, Wei He, Yiwen Ding, Boyang Hong, Ming Zhang, Junzhe Wang, Senjie Jin, Enyu Zhou, et al. The rise and potential of large language model based agents: A survey. Science China Information Sciences, 68(2):121101, 2025a.

Zhiheng Xi, Jixuan Huang, Chenyang Liao, Baodai Huang, Honglin Guo, Jiaqi Liu, Rui Zheng, Junjie Ye, Jiazheng Zhang, Wenxiang Chen, et al. Agentgym-rl: Training llm agents for long-horizon decision making through multi-turn reinforcement learning. arXiv preprint arXiv:2509.08755, 2025b.

Siyu Xia, Zekun Xu, Jiajun Chai, Wentian Fan, Yan Song, Xiaohan Wang, Guojun Yin, Wei Lin, Haifeng Zhang, and Jun Wang. From experience to strategy: Empowering llm agents with trainable graph memory. arXiv preprint arXiv:2511.07800, 2025.

Yijia Xiao, Edward Sun, Di Luo, and Wei Wang. Tradingagents: Multi-agents llm financial trading framework. arXiv preprint arXiv:2412.20138, 2024.

Yunzhong Xiao, Yangmin Li, Hewei Wang, Yunlong Tang, and Zora Zhiruo Wang. Toolmem: Enhancing multimodal agents with learnable tool capability memory. arXiv preprint arXiv:2510.06664, 2025.

Tianbao Xie, Danyang Zhang, Jixuan Chen, Xiaochuan Li, Siheng Zhao, Ruisheng Cao, Toh J Hua, Zhoujun Cheng, Dongchan Shin, Fangyu Lei, et al. Osworld: Benchmarking multimodal agents for open-ended tasks in real computer environments. Advances in Neural Information Processing Systems, 37:52040–52094, 2024.

Guojun Xiong, Zhiyang Deng, Keyi Wang, Yupeng Cao, Haohang Li, Yangyang Yu, Xueqing Peng, Mingquan Lin, Kaleb E Smith, Xiao-Yang Liu, et al. Flag-trader: Fusion llm-agent with gradient-based reinforcement learning for financial trading. arXiv preprint arXiv:2502.11433, 2025a.

Haomiao Xiong, Zongxin Yang, Jiazuo Yu, Yunzhi Zhuge, Lu Zhang, Jiawen Zhu, and Huchuan Lu. Streaming video understanding and multi-round interaction with memory-enhanced knowledge. arXiv preprint arXiv:2501.13468, 2025b.

Yiming Xiong, Jian Wang, Bing Li, Yuhan Zhu, and Yuqi Zhao. Self-organizing agent network for llm-based workflow automation. arXiv preprint arXiv:2508.13732, 2025c.

Zidi Xiong, Yuping Lin, Wenya Xie, Pengfei He, Zirui Liu, Jiliang Tang, Himabindu Lakkaraju, and Zhen Xiang. How memory management impacts llm agents: An empirical study of experience-following behavior. arXiv preprint arXiv:2505.16067, 2025d.

Binyan Xu, Haitao Li, and Kehuan Zhang. Llm agents are latent context managers: Eliciting self-managed context via a proprioceptive dashboard. arXiv preprint arXiv:2606.30005, 2026.

Haoran Xu, Jiacong Hu, Ke Zhang, Lei Yu, Yuxin Tang, Xinyuan Song, Yiqun Duan, Lynn Ai, and Bill Shi. Sedm: Scalable self-evolving distributed memory for agents. arXiv preprint arXiv:2509.09498, 2025a.

Jing Xu, Arthur Szlam, and Jason Weston. Beyond goldfish memory: Long-term open-domain conversation. In Proceedings of the 60th annual meeting of the association for computational linguistics (volume 1: long papers), pp. 5180–5197, 2022a.

Renjun Xu and Yang Yan. Agent skills for large language models: Architecture, acquisition, security, and the path forward. arXiv preprint arXiv:2602.12430, 2026.

Songlin Xu, Xinyu Zhang, and Lianhui Qin. Eduagent: Generative student agents in learning. arXiv preprint arXiv:2404.07963, 2024a.

Songlin Xu, Hao-Ning Wen, Hongyi Pan, Dallas Dominguez, Dongyin Hu, and Xinyu Zhang. Classroom simulacra: Building contextual student generative agents in online education for learning behavioral simulation. In Proceedings of the 2025 CHI Conference on Human Factors in Computing Systems, pp. 1–26, 2025b.

Tianqi Xu, Linyao Chen, Dai-Jie Wu, Yanjun Chen, Zecheng Zhang, Xiang Yao, Zhiqiang Xie, Yongchao Chen, Shilong Liu, Bochen Qian, et al. Crab: Cross-environment agent benchmark for multimodal language model agents. In Findings of the Association for Computational Linguistics: ACL 2025, pp. 21607–21647, 2025c.

Tianyang Xu, Hongqiu Wu, Weiqi Wu, and Hai Zhao. Open-theatre: An open-source toolkit for llm-based interactive drama. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing: System Demonstrations, pp. 453–460, 2025d.

Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, and Yongfeng Zhang. A-mem: Agentic memory for llm agents. arXiv preprint arXiv:2502.12110, 2025e.

Xinchao Xu, Zhibin Gou, Wenquan Wu, Zheng-Yu Niu, Hua Wu, Haifeng Wang, and Shihang Wang. Long time no see! open-domain conversation with long-term persona memory. In Findings of the Association for Computational Linguistics: ACL 2022, pp. 2639–2650, 2022b.

Yunqi Xu, Tianchi Cai, Jiyan Jiang, and Xierui Song. Face4rag: Factual consistency evaluation for retrieval augmented generation in chinese. In Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, pp. 6083–6094, 2024b.

Karmesh Yadav, Yusuf Ali, Gunshi Gupta, Yarin Gal, and Zsolt Kira. Findingdory: A benchmark to evaluate memory in embodied agents. arXiv preprint arXiv:2506.15635, 2025.

Ofir Yakobi and Shir Sadon. Bringing memory to ai: Mcp, a2a & agent context protocols. https: //orca.security/resources/blog/bringing-memory-to-ai-mcp-a2a-agent-context-protocols/, 2025. Orca Security blog.

BY Yan, Chaofan Li, Hongjin Qian, Shuqi Lu, and Zheng Liu. General agentic memory via deep research. arXiv preprint arXiv:2511.18423, 2025a.

Sikuan Yan, Xiufeng Yang, Zuchao Huang, Ercong Nie, Zifeng Ding, Zonggen Li, Xiaowen Ma, Kristian Kersting, Jef Z Pan, Hinrich Schütze, et al. Memory-r1: Enhancing large language model agents to manage and utilize memories via reinforcement learning. arXiv preprint arXiv:2508.19828, 2025b.

Cheng Yang, Xuemeng Yang, Licheng Wen, Daocheng Fu, Jianbiao Mei, Rong Wu, Pinlong Cai, Yufan Shen, Nianchen Deng, Botian Shi, et al. Learning on the job: An experience-driven self-evolving agent for long-horizon tasks. arXiv preprint arXiv:2510.08002, 2025a.

Hongkang Yang, Zehao Lin, Wenjin Wang, Hao Wu, Zhiyu Li, Bo Tang, Wenqiang Wei, Jinbo Wang, Zeyun Tang, Shichao Song, et al. Memory3: Language modeling with explicit memory. arXiv preprint arXiv:2407.01178, 2024a.

Jingkang Yang, Shuai Liu, Hongming Guo, Yuhao Dong, Xiamengwei Zhang, Sicheng Zhang, Pengyun Wang, Zitang Zhou, Binzhu Xie, Ziyue Wang, et al. Egolife: Towards egocentric life assistant. In Proceedings of the Computer Vision and Pattern Recognition Conference, pp. 28885–28900, 2025b.

Ling Yang, Zhaochen Yu, Tianjun Zhang, Shiyi Cao, Minkai Xu, Wentao Zhang, Joseph E Gonzalez, and Bin Cui. Bufer of thoughts: Thought-augmented reasoning with large language models. Advances in Neural Information Processing Systems, 37:113519–113544, 2024b.

Rui Yang. Casegpt: a case reasoning framework based on language models and retrieval-augmented generation. arXiv preprint arXiv:2407.07913, 2024.

Rui Yang, Hanyang Chen, Junyu Zhang, Mark Zhao, Cheng Qian, Kangrui Wang, Qineng Wang, Teja Venkat Koripella, Marziyeh Movahedi, Manling Li, et al. Embodiedbench: Comprehensive benchmarking multi modal large language models for vision-driven embodied agents. arXiv preprint arXiv:2502.09560, 2025c.

Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William Cohen, Ruslan Salakhutdinov, and Christopher D Manning. Hotpotqa: A dataset for diverse, explainable multi-hop question answering. In Proceedings of the 2018 conference on empirical methods in natural language processing, pp. 2369–2380, 2018.

Shunyu Yao, Howard Chen, John Yang, and Karthik Narasimhan. Webshop: Towards scalable real-world web interaction with grounded language agents. Advances in Neural Information Processing Systems, 35: 20744–20757, 2022.

Shunyu Yao, Jefrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R Narasimhan, and Yuan Cao. React: Synergizing reasoning and acting in language models. In The eleventh international conference on learning representations, 2023.

Shunyu Yao, Noah Shinn, Pedram Razavi, and Karthik R. Narasimhan. τ-bench: A benchmark for Tool-Agent-User interaction in real-world domains. In The Thirteenth International Conference on Learning Representations, 2025.

Weiran Yao, Shelby Heinecke, Juan Carlos Niebles, Zhiwei Liu, Yihao Feng, Le Xue, Rithesh RN, Zeyuan Chen, Jianguo Zhang, Devansh Arpit, et al. Retroformer: Retrospective large language agents with policy gradient optimization. In The Twelfth International Conference on Learning Representations, 2024.

Jiabo Ye, Xi Zhang, Haiyang Xu, Haowei Liu, Junyang Wang, Zhaoqing Zhu, Ziwei Zheng, Feiyu Gao, Junjie Cao, Zhengxi Lu, et al. Mobile-agent-v3: Fundamental agents for gui automation. arXiv preprint arXiv:2508.15144, 2025a.

Rui Ye, Zhongwang Zhang, Kuan Li, Huifeng Yin, Zhengwei Tao, Yida Zhao, Liangcai Su, Liwen Zhang, Zile Qiao, Xinyu Wang, et al. Agentfold: Long-horizon web agents with proactive context management. arXiv preprint arXiv:2510.24699, 2025b.

Asaf Yehudai, Lilach Eden, Alan Li, Guy Uziel, Yilun Zhao, Roy Bar-Haim, Arman Cohan, and Michal Shmueli-Scheuer. Survey on evaluation of llm-based agents. arXiv preprint arXiv:2503.16416, 2025.

Ryan Yen and Jian Zhao. Memolet: Reifying the reuse of user-ai conversational memories. In Proceedings of the 37th Annual ACM Symposium on User Interface Software and Technology, pp. 1–22, 2024.

Jeong Hun Yeo, Sangyun Chung, Sungjune Park, Dae Hoe Kim, Jinyoung Moon, and Yong Man Ro. Gcagent: Long-video understanding via schematic and narrative episodic memory. arXiv preprint arXiv:2511.12027, 2025a.

Woongyeong Yeo, Kangsan Kim, Jaehong Yoon, and Sung Ju Hwang. Worldmm: Dynamic multimodal memory agent for long video reasoning. arXiv preprint arXiv:2512.02425, 2025b.

Fangyi Yu, Nabeel Seedat, Drahomira Herrmannova, Frank Schilder, and Jonathan Richard Schwarz. Beyond pointwise scores: Decomposed criteria-based evaluation of llm responses. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing: Industry Track, pp. 1931–1954, 2025a.

Hongli Yu, Tinghong Chen, Jiangtao Feng, Jiangjie Chen, Weinan Dai, Qiying Yu, Ya-Qin Zhang, Wei-Ying Ma, Jingjing Liu, Mingxuan Wang, et al. Memagent: Reshaping long-context llm with multi-conv rl-based memory agent. arXiv preprint arXiv:2507.02259, 2025b.

Miao Yu, Fanci Meng, Xinyun Zhou, Shilong Wang, Junyuan Mao, Linsey Pan, Tianlong Chen, Kun Wang, Xinfeng Li, Yongfeng Zhang, et al. A survey on trustworthy llm agents: Threats and countermeasures. In Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V. 2, pp. 6216–6226, 2025c.

Shuo Yu, Mingyue Cheng, Daoyu Wang, Qi Liu, Zirui Liu, Ze Guo, and Xiaoyu Tao. Memweaver: A hierarchical memory from textual interactive behaviors for personalized generation. arXiv preprint arXiv:2510.07713, 2025d.

Yangyang Yu, Zhiyuan Yao, Haohang Li, Zhiyang Deng, Yuechen Jiang, Yupeng Cao, Zhi Chen, Jordan Suchow, Zhenyu Cui, Rong Liu, et al. Fincon: A synthesized llm multi-agent system with conceptual verbal reinforcement for enhanced financial decision making. Advances in Neural Information Processing Systems, 37:137010–137045, 2024a.

Yangyang Yu, Haohang Li, Zhi Chen, Yuechen Jiang, Yang Li, Jordan W Suchow, Denghui Zhang, and Khaldoun Khashanah. Finmem: A performance-enhanced llm trading agent with layered memory and character design. IEEE Transactions on Big Data, 2025e.

Zhuohao Yu, Chang Gao, Wenjin Yao, Yidong Wang, Wei Ye, Jindong Wang, Xing Xie, Yue Zhang, and Shikun Zhang. Kieval: A knowledge-grounded interactive evaluation framework for large language models. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 5967–5985, 2024b.

Qianhao Yuan, Jie Lou, Zichao Li, Jiawei Chen, Yaojie Lu, Hongyu Lin, Le Sun, Debing Zhang, and Xianpei Han. Memsearcher: Training llms to reason, search and manage memory via end-to-end reinforcement learning. arXiv preprint arXiv:2511.02805, 2025a.

Ruifeng Yuan, Shichao Sun, Yongqi Li, Zili Wang, Ziqiang Cao, and Wenjie Li. Personalized large language model assistant with evolving conditional memory. In Proceedings of the 31st International Conference on Computational Linguistics, pp. 3764–3777, 2025b.

Siyu Yuan, Kaitao Song, Jiangjie Chen, Xu Tan, Yongliang Shen, Kan Ren, Dongsheng Li, and Deqing Yang. Easytool: Enhancing llm-based agents with concise tool instruction. In Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers), pp. 951–972, 2025c.

Tongxin Yuan, Zhiwei He, Lingzhong Dong, Yiming Wang, Ruijie Zhao, Tian Xia, Lizhen Xu, Binglin Zhou, Fangqi Li, Zhuosheng Zhang, et al. R-judge: Benchmarking safety risk awareness for llm agents. In Findings of the Association for Computational Linguistics: EMNLP 2024, pp. 1467–1490, 2024a.

Weikang Yuan, Junjie Cao, Zhuoren Jiang, Yangyang Kang, Jun Lin, Kaisong Song, Tianqianjin Lin, Pengwei Yan, Changlong Sun, and Xiaozhong Liu. Can large language models grasp legal theories? enhance legal reasoning with insights from multi-agent collaboration. In Findings of the association for computational linguistics: EMNLP 2024, pp. 7577–7597, 2024b.

Murong Yue, Zhiwei Liu, Liangwei Yang, Jianguo Zhang, Zuxin Liu, Haolin Chen, Ziyu Yao, Silvio Savarese, Caiming Xiong, Shelby Heinecke, et al. Toollibgen: Scalable automatic tool creation and aggregation for llm reasoning. arXiv preprint arXiv:2510.07768, 2025.

Sizhe Yuen, Francisco Gomez Medina, Ting Su, Yali Du, and Adam J Sobey. Intrinsic memory agents: Heterogeneous multi-agent llm systems through structured contextual memory. arXiv preprint arXiv:2508.08997, 2025.

Qingbin Zeng, Bingbing Fan, Zhiyu Chen, Sijian Ren, Zhilun Zhou, Xuhua Zhang, Yuanyi Zhen, Fengli Xu, Yong Li, and Tie-Yan Liu. Mirrormind: Empowering omniscientist with the expert perspectives and collective knowledge of human scientists. arXiv preprint arXiv:2511.16997, 2025.

Mingliang Zhai, Zhi Gao, Yuwei Wu, and Yunde Jia. Memory-centric embodied question answer. arXiv preprint arXiv:2505.13948, 2025.

Xiao Zhan, Noura Abdi, William Seymour, and Jose Such. Healthcare voice ai assistants: factors influencing trust and intention to use. Proceedings of the ACM on Human-Computer Interaction, 8(CSCW1):1–37, 2024.

Dianxing Zhang, Wendong Li, Kani Song, Jiaye Lu, Gang Li, Liuchun Yang, and Sheng Li. Memory in large language models: Mechanisms, evaluation and evolution. arXiv preprint arXiv:2509.18868, 2025a.

Gaoke Zhang, Bo Wang, Yunlong Ma, Dongming Zhao, and Zifei Yu. Multiple memory systems for enhancing the long-term memory of agent. arXiv preprint arXiv:2508.15294, 2025b.

Guibin Zhang, Muxin Fu, Guancheng Wan, Miao Yu, Kun Wang, and Shuicheng Yan. G-memory: Tracing hierarchical memory for multi-agent systems. arXiv preprint arXiv:2506.07398, 2025c.

Guibin Zhang, Muxin Fu, and Shuicheng Yan. Memgen: Weaving generative latent memory for self-evolving agents. arXiv preprint arXiv:2509.24704, 2025d.

Guibin Zhang, Yanwei Yue, Zhixun Li, Sukwon Yun, Guancheng Wan, Kun Wang, Dawei Cheng, Jefrey Xu Yu, and Tianlong Chen. Cut the crap: An economical communication pipeline for LLM-based multi-agent systems. In The Thirteenth International Conference on Learning Representations, 2025e.

Guibin Zhang, Yanwei Yue, Xiangguo Sun, Guancheng Wan, Miao Yu, Junfeng Fang, Kun Wang, Tianlong Chen, and Dawei Cheng. G-designer: Architecting multi-agent communication topologies via graph neural networks. In Forty-second International Conference on Machine Learning, 2025f.

Hanrong Zhang, Shicheng Fan, Henry Peng Zou, Yankai Chen, Zhenting Wang, Jiayu Zhou, Chengze Li, Wei Chieh Huang, Yifei Yao, Kening Zheng, Xue Liu, Xiaoxiao Li, and Philip S. Yu. Coevoskills: Self-evolving agent skills via co-evolutionary verification. arXiv preprint arXiv:2604.01687, 2026a.

Haozhen Zhang, Quanyu Long, Jianzhu Bao, Tao Feng, Weizhi Zhang, Haodong Yue, and Wenya Wang. Memskill: Learning and evolving memory skills for self-evolving agents. arXiv preprint arXiv:2602.02474, 2026b.

Hongxin Zhang, Weihua Du, Jiaming Shan, Qinhong Zhou, Yilun Du, Joshua B Tenenbaum, Tianmin Shu, and Chuang Gan. Building cooperative embodied agents modularly with large language models. In The Twelfth International Conference on Learning Representations, 2024a.

Jiayi Zhang, Jinyu Xiang, Zhaoyang Yu, Fengwei Teng, Xiong-Hui Chen, Jiaqi Chen, Mingchen Zhuge, Xin Cheng, Sirui Hong, Jinlin Wang, et al. Aflow: Automating agentic workflow generation. In The Thirteenth International Conference on Learning Representations, 2025g.

Junjie Zhang, Yupeng Hou, Ruobing Xie, Wenqi Sun, Julian McAuley, Wayne Xin Zhao, Leyu Lin, and Ji-Rong Wen. Agentcf: Collaborative learning with autonomous language agents for recommender systems. In Proceedings of the ACM Web Conference 2024, pp. 3679–3689, 2024b.

Jusheng Zhang, Yijia Fan, Kaitong Cai, Xiaofei Sun, and Keze Wang. OSC: Cognitive orchestration through dynamic knowledge alignment in multi-agent LLM collaboration. In Findings of the Association for Computational Linguistics: EMNLP 2025, pp. 6320–6337. Association for Computational Linguistics, November 2025h.

Kai Zhang, Xiangchao Chen, Bo Liu, Tianci Xue, Zeyi Liao, Zhihan Liu, Xiyao Wang, Yuting Ning, Zhaorun Chen, Xiaohan Fu, et al. Agent learning via early experience. arXiv preprint arXiv:2510.08558, 2025i.

Qizheng Zhang, Changran Hu, Shubhangi Upasani, Boyuan Ma, Fenglu Hong, Vamsidhar Kamanuru, Jay Rainton, Chen Wu, Mengmeng Ji, Hanchen Li, et al. Agentic context engineering: Evolving contexts for self-improving language models. arXiv preprint arXiv:2510.04618, 2025j.

Saizheng Zhang, Emily Dinan, Jack Urbanek, Arthur Szlam, Douwe Kiela, and Jason Weston. Personalizing dialogue agents: I have a dog, do you have pets too? arXiv preprint arXiv:1801.07243, 2018.

Songyang Zhang, Zeming Li, Shipeng Yan, Xuming He, and Jian Sun. Distribution alignment: A unified framework for long-tail visual recognition. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pp. 2361–2370, 2021.

Weizhi Zhang, Yuanchen Bei, Liangwei Yang, Henry Peng Zou, Peilin Zhou, Aiwei Liu, Yinghui Li, Hao Chen, Jianling Wang, Yu Wang, et al. Cold-start recommendation towards the era of large language models (llms): A comprehensive survey and roadmap. arXiv preprint arXiv:2501.01945, 2025k.

Weizhi Zhang, Yangning Li, Yuanchen Bei, Junyu Luo, Guancheng Wan, Liangwei Yang, Chenxuan Xie, Yuyao Yang, Wei-Chieh Huang, Chunyu Miao, et al. From web search towards agentic deep research: Incentivizing search with reasoning agents. arXiv preprint arXiv:2506.18959, 2025l.

Weizhi Zhang, Liangwei Yang, Wooseong Yang, Henry Peng Zou, Yuqing Liu, Ke Xu, Sourav Medya, and Philip S Yu. Llminit: A free lunch from large language models for selective initialization of recommendation. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing: Industry Track, pp. 2016–2024, 2025m.

Weizhi Zhang, Wooseong Yang, Yuxin Cui, Zhaohui Guo, Hins Hu, Liangwei Yang, Henry Peng Zou, Qifei Wang, Hanqing Zeng, Jiayi Liu, et al. Toward user preference alignment in llm recommendation via explicit context feedback. In 2025 IEEE 7th International Conference on Cognitive Machine Intelligence (CogMI), pp. 381–388. IEEE, 2025n.

Weizhi Zhang, Xinyang Zhang, Chenwei Zhang, Liangwei Yang, Jingbo Shang, Zhepei Wei, Henry Peng Zou, Zijie Huang, Zhengyang Wang, Yifan Gao, et al. Personaagent: When large language model agents meet personalization at test time. arXiv preprint arXiv:2506.06254, 2025o.

Weizhi Zhang, Zechen Li, Hamid Palangi, Ben Graef, A Ali Heydari, Simon A Lee, Salman Rahman, Ray Luo, Zeinab Esmaeilpour, Erik Schenck, et al. Rubricstree: Scalable and evolving open-ended evaluation of personal health agents across health memory and medical skills. arXiv preprint arXiv:2606.18203, 2026c.

Weizhi Zhang, Xiaokai Wei, Wei-Chieh Huang, Zheng Hui, Chen Wang, Michelle Gong, and Philip S Yu. Memorycd: Benchmarking long-context user memory of llm agents for lifelong cross-domain personalization. arXiv preprint arXiv:2603.25973, 2026d.

Yi Zhang, Zhongyang Yu, Wanqi Jiang, Yufeng Shen, and Jin Li. Long-term memory for large language models through topic-based vector database. In 2023 International Conference on Asian Language Processing (IALP), pp. 258–264. IEEE, 2023a.

Yuxiang Zhang, Jiangming Shu, Ye Ma, Xueyuan Lin, Shangxi Wu, and Jitao Sang. Memory as action: Autonomous context curation for long-horizon agentic tasks. arXiv preprint arXiv:2510.12635, 2025p.

Zeyu Zhang, Quanyu Dai, Luyu Chen, Zeren Jiang, Rui Li, Jieming Zhu, Xu Chen, Yi Xie, Zhenhua Dong, and Ji-Rong Wen. Memsim: A bayesian simulator for evaluating memory of llm-based personal assistants. arXiv preprint arXiv:2409.20163, 2024c.

Zeyu Zhang, Quanyu Dai, Xiaohe Bo, Chen Ma, Rui Li, Xu Chen, Jieming Zhu, Zhenhua Dong, and Ji-Rong Wen. A survey on the memory mechanism of large language model-based agents. ACM Transactions on Information Systems, 43(6):1–47, 2025q.

Zeyu Zhang, Quanyu Dai, Rui Li, Xiaohe Bo, Xu Chen, and Zhenhua Dong. Learn to memorize: Optimizing llm-based agents with adaptive memory framework. arXiv preprint arXiv:2508.16629, 2025r.

Zhenyu Zhang, Ying Sheng, Tianyi Zhou, Tianlong Chen, Lianmin Zheng, Ruisi Cai, Zhao Song, Yuandong Tian, Christopher Ré, Clark Barrett, et al. H2o: Heavy-hitter oracle for eficient generative inference of large language models. Advances in Neural Information Processing Systems, 36:34661–34710, 2023b.

Zhexin Zhang, Shiyao Cui, Yida Lu, Jingzhuo Zhou, Junxiao Yang, Hongning Wang, and Minlie Huang. Agent-safetybench: Evaluating the safety of llm agents. arXiv preprint arXiv:2412.14470, 2024d.

Zijian Zhang, Shuchang Liu, Ziru Liu, Rui Zhong, Qingpeng Cai, Xiangyu Zhao, Chunxu Zhang, Qidong Liu, and Peng Jiang. Llm-powered user simulator for recommender system. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, pp. 13339–13347, 2025s.

Jihao Zhao, Zhiyuan Ji, Simin Niu, Hanyu Wang, Feiyu Xiong, and Zhiyu Li. Mom: Mixtures of scenarioaware document memories for retrieval-augmented generation systems. arXiv preprint arXiv:2510.14252, 2025a.

Linxi Zhao, Sofian Zalouk, Christian K Belardi, Justin Lovelace, Jin Peng Zhou, Kilian Q Weinberger, Yoav Artzi, and Jennifer J Sun. Pre-training large memory language models with internal and external knowledge. arXiv preprint arXiv:2505.15962, 2025b.

Siyan Zhao, Mingyi Hong, Yang Liu, Devamanyu Hazarika, and Kaixiang Lin. Do llms recognize your preferences? evaluating personalized preference following in llms. In The Thirteenth International Conference on Learning Representations, 2025c.

Zheng Zhao, Clara Vania, Subhradeep Kayal, Naila Khan, Shay B Cohen, and Emine Yilmaz. Personalens: A benchmark for personalization evaluation in conversational ai assistants. arXiv preprint arXiv:2506.09902, 2025d.

Zihan Zhao, Da Ma, Lu Chen, Liangtai Sun, Zihao Li, Yi Xia, Bo Chen, Hongshen Xu, Zichen Zhu, Su Zhu, et al. Developing chemdfm as a large language foundation model for chemistry. Cell Reports Physical Science, 6(4), 2025e.

Junhao Zheng, Xidi Cai, Qiuke Li, Duzhen Zhang, ZhongZhi Li, Yingying Zhang, Le Song, and Qianli Ma. Lifelongagentbench: Evaluating llm agents as lifelong learners. arXiv preprint arXiv:2505.11942, 2025a.

Junhao Zheng, Shengjie Qiu, Chengming Shi, and Qianli Ma. Towards lifelong learning of large language models: A survey. ACM Computing Surveys, 57(8):1–35, 2025b.

Junhao Zheng, Chengming Shi, Xidi Cai, Qiuke Li, Duzhen Zhang, Chenxing Li, Dong Yu, and Qianli Ma. Lifelong learning of large language model based agents: A roadmap. arXiv preprint arXiv:2501.07278, 2025c.

Longtao Zheng, Rundong Wang, Xinrun Wang, and Bo An. Synapse: Trajectory-as-exemplar prompting with memory for computer control. In The Twelfth International Conference on Learning Representations, 2024.

Tianshi Zheng, Kelvin Kiu-Wai Tam, Newt Hue-Nam K Nguyen, Baixuan Xu, Zhaowei Wang, Jiayang Cheng, Hong Ting Tsang, Weiqi Wang, Jiaxin Bai, Tianqing Fang, et al. Newtonbench: Benchmarking generalizable scientific law discovery in llm agents. arXiv preprint arXiv:2510.07172, 2025d.

Xiaochen Zheng, Jinzhi Lu, and Dimitris Kiritsis. The emergence of cognitive digital twin: vision, challenges and opportunities. International Journal of Production Research, 60(24):7610–7632, 2022.

Wanjun Zhong, Lianghong Guo, Qiqi Gao, He Ye, and Yanlin Wang. Memorybank: Enhancing large language models with long-term memory. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, pp. 19724–19731, 2024.

Huichi Zhou, Yihang Chen, Siyuan Guo, Xue Yan, Kin Hei Lee, Zihan Wang, Ka Yiu Lee, Guchun Zhang, Kun Shao, Linyi Yang, et al. Memento: Fine-tuning llm agents without fine-tuning llms. arXiv preprint arXiv:2508.16153, 2025a.

Shuyan Zhou, Frank F Xu, Hao Zhu, Xuhui Zhou, Robert Lo, Abishek Sridhar, Xianyi Cheng, Tianyue Ou, Yonatan Bisk, Daniel Fried, et al. Webarena: A realistic web environment for building autonomous agents. In The Twelfth International Conference on Learning Representations, 2024.

Yanfang Zhou, Xiaodong Li, Yuntao Liu, Yongqiang Zhao, Xintong Wang, Zhenyu Li, Jinlong Tian, and Xinhai Xu. M2pa: A multi-memory planning agent for open worlds inspired by cognitive theory. In Findings of the Association for Computational Linguistics: ACL 2025, pp. 23204–23220, 2025b.

Zijian Zhou, Ao Qu, Zhaoxuan Wu, Sunghwan Kim, Alok Prakash, Daniela Rus, Jinhua Zhao, Bryan Kian Hsiang Low, and Paul Pu Liang. Mem1: Learning to synergize memory and reasoning for eficient long-horizon agents. arXiv preprint arXiv:2506.15841, 2025c.

Lixi Zhu, Xiaowen Huang, and Jitao Sang. How reliable is your simulator? analysis on the limitations of current llm-based user simulators for conversational recommendation. In Companion Proceedings of the ACM Web Conference 2024, pp. 1726–1732, 2024.

Lixi Zhu, Xiaowen Huang, and Jitao Sang. A llm-based controllable, scalable, human-involved user simulator framework for conversational recommender systems. In Proceedings of the ACM on Web Conference 2025, pp. 4653–4661, 2025a.

Rui-Jie Zhu, Tianhao Peng, Tianhao Cheng, Xingwei Qu, Jinfa Huang, Dawei Zhu, Hao Wang, Kaiwen Xue, Xuanliang Zhang, Yong Shan, et al. A survey on latent reasoning. arXiv preprint arXiv:2507.06203, 2025b.

Xizhou Zhu, Yuntao Chen, Hao Tian, Chenxin Tao, Weijie Su, Chenyu Yang, Gao Huang, Bin Li, Lewei Lu, Xiaogang Wang, et al. Ghost in the minecraft: Generally capable agents for open-world environments via large language models with text-based knowledge and memory. arXiv preprint arXiv:2305.17144, 2023.

Yuanjie Zhu, Liangwei Yang, Ke Xu, Weizhi Zhang, Zihe Song, Jindong Wang, and Philip S Yu. Llmmemcluster: Empowering large language models with dynamic memory for text clustering. arXiv preprint arXiv:2511.15424, 2025c.

Henry Peng Zou, Zhengyao Gu, Yue Zhou, Yankai Chen, Weizhi Zhang, Liancheng Fang, Yibo Wang, Yangning Li, Kay Liu, and Philip S Yu. Testnuc: Enhancing test-time computing approaches and scaling through neighboring unlabeled data consistency. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 30750–30762, 2025a.

Henry Peng Zou, Wei-Chieh Huang, Yaozu Wu, Yankai Chen, Chunyu Miao, Hoang Nguyen, Yue Zhou, Weizhi Zhang, Liancheng Fang, Langzhou He, et al. A survey on large language model based human-agent systems. Authorea Preprints, 2025b.

Henry Peng Zou, Wei-Chieh Huang, Yaozu Wu, Chunyu Miao, Dongyuan Li, Aiwei Liu, Yue Zhou, Yankai Chen, Weizhi Zhang, Yangning Li, et al. A call for collaborative intelligence: Why human-agent systems should precede ai autonomy. arXiv preprint arXiv:2506.09420, 2025c.

Henry Peng Zou, Chunyu Miao, Wei-Chieh Huang, Yankai Chen, Yue Zhou, Hanrong Zhang, Yaozu Wu, Liancheng Fang, Zhengyao Gu, Zhen Zhang, Kening Zheng, Fangxin Wang, Yi Nian, Shanghao Li, Wenzhe Fan, Langzhou He, Weizhi Zhang, Xue Liu, and Philip S. Yu. When users change their mind: Evaluating interruptible agents in long-horizon web navigation. arXiv preprint arXiv:2604.00892, 2026.
