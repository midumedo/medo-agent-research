# 译法摘记：Rethinking Memory in LLM based Agents

对应译本：`arxiv-2505.00675.Survey.Rethinking Memory.zh.md`。术语按「英文原形优先」处理，中文只承担叙述、连接与论证；名词性操作保留英文，动词位置用中文。位置编号指译本行号。

## 1 术语处理

| 英文 | 处理 | 备选 | 理由 |
| :--- | :--- | :--- | :--- |
| memory | 保留 memory | 记忆 | 全文核心对象，且需与 biological / human memory 并置区分 |
| agent memory | 保留 agent memory | 智能体记忆 | agent 亦保留原形，组合后不宜半译 |
| long-term memory | 保留 | 长期记忆 | 与 long-context memory 并排时须一眼可辨 |
| short-term memory | 保留 | 短期记忆 | 与 long-term 成对，保持对称 |
| parametric | 保留 parametric | 参数式、参数化 | 指知识存在形式；「参数化」易被读成动作 |
| contextual | 保留 contextual | 上下文式、语境式 | 与 parametric 对举，指载体而非语言学语境 |
| latent | 保留 latent | 潜、潜在 | latent memory 指隐表示，非「潜在记忆」 |
| context / context window | 保留 | 上下文、上下文窗口 | 本文兼指输入文本与模型窗口上限 |
| prompt | 保留 prompt | 提示词、提示 | 兼指输入串、模板与软 prompt |
| harness | 保留 harness | 框架、测试台 | agent harness 指运行脚手架，不译「挽具」 |
| retrieval | 名词保留 retrieval；动词用「检索」 | 召回 | 与指标 Recall 区分；动词化避免「retrieval 检索」叠词 |
| RAG | 保留 RAG | 检索增强生成 | 首次出现给全称，后文一律缩写 |
| embedding | 名词保留 embedding；动词用「嵌入」 | 向量化 | 与 vector、representation 区分 |
| consolidation | 名词保留 consolidation；动词用「整合」 | 巩固、固化 | 强调并入持久 memory，与 updating 的改写相区别 |
| updating | 名词保留 updating；动词用「更新」 | 修改 | 与 model editing 的「编辑」拉开层次 |
| indexing | 名词保留 indexing；动词用「建索引」「索引」 | 索引化 | 六种原子操作之一，名词位置不译 |
| forgetting | 名词保留 forgetting；动词用「遗忘」 | 删除 | 与 machine unlearning 区分：前者是操作，后者是训练范式 |
| condensation | 名词保留 condensation；动词用「凝缩」 | 压缩 | 与 compression 并用，必须分译 |
| compression | 名词保留 compression；动词用「压缩」 | 约简 | 长 context 主题的操作名，与 condensation 分开 |
| integration | 名词保留 integration；动词用「整合」 | 融合 | 与 fusion（模态对齐）区分 |
| episodic / semantic / procedural / working memory | 保留 | 情节／语义／程序／工作记忆 | 认知科学术语，中文译名歧义较大 |
| KV cache | 保留 | 键值缓存 | Key–Value 首次出现括注，后文统一 KV cache |
| KV cache eviction / storing optimization / selection | 保留 | 驱逐／存储优化／选择 | 三类方法名，须与 attention 机制区分 |
| attention | 保留 attention | 注意力 | 与 attention sink、attention 权重连用 |
| LoRA / fine-tuning / distillation | 保留 | 低秩适配／微调／蒸馏 | 均为方法名，中文译名不稳定 |
| benchmark | 保留 benchmark | 基准、评测集 | 与 dataset 区分：前者含协议与指标 |
| ground truth | 保留 | 真值、标准答案 | 与 factual grounding 的 grounding 区分 |
| session | 保留 session | 会话 | 与 multi-session、cross-session 连用 |
| long-context / long-horizon | 保留 | 长上下文／长时程 | long-horizon 指单任务跨度，与 long-term 不同 |
| multi-source | 保留 | 多源 | 与 multi-modal、cross-textual 并置 |
| agentic | 保留 agentic | 智能体式 | agentic context engineering 为专名 |
| fusion / conflict | 小标题与表格操作列保留英文；正文普通名词用「融合／冲突」 | 融合／冲突 | 3.4 节的操作与问题名，正文动词化时用中文更顺 |
| model editing / machine unlearning / continual learning | 保留 | 模型编辑／机器遗忘／持续学习 | 三条技术路线名，缩写与图表一致 |
| persona | 人物形象 | 人格、人设 | 指可检索的用户档案，非性格 |

## 2 句例

1. 原文：Memory is a core component of Large Language Model (LLM) based agents [301] and a critical step towards AGI [228], enabling persistent interactions [196, 375], reasoning [78], multi-modal understanding [189], personalization [153], and multi-agent collaboration [298].
   译文：memory 是基于大语言模型（LLM）的 agent 的核心组件 [301]，也是迈向通用人工智能（AGI）的关键一步 [228]，它支撑持久交互 [196, 375]、推理 [78]、多模态理解 [189]、个性化 [153] 以及多 agent 协作 [298]。
   取舍：enabling 译「支撑」，与后文同类结构统一；五个并列项改为顿号链，引用编号仍紧跟各自项；句首 memory 保留小写原形。

2. 原文：Parametric memory encodes knowledge implicitly in model parameters [289], while contextual memory stores explicit external information, either structured (e.g., graphs, tables, trajectories [239]), or unstructured (e.g., text [375], vectors, audio, video [189]).
   译文：parametric memory 将知识隐式编码于模型参数中 [289]，而 contextual memory 存储显式外部信息，或为结构化（例如图、表、轨迹 [239]），或为非结构化（例如文本 [375]、向量、音频、视频 [189]）。
   取舍：encodes / stores 分译「编码」「存储」，保住隐式—显式的对举；either...or 用「或为……或为……」维持定义句的对称。

3. 原文：Working memory acts as a dynamic control mechanism that integrates short-term caches and activated longterm knowledge, enabling real-time reasoning, planning, and decision-making.
   译文：working memory 作为一种动态控制机制，整合短期缓存与已激活的长期知识，支撑实时推理、规划与决策。
   取舍：acts as 译「作为」而非「充当」；integrated 落在动词位，用「整合」；enabling 沿用例 1 的「支撑」。

4. 原文：Long-Term Memory (temporal), focusing on memory management, utilization, and personalization in multisession dialogue systems [196, 327], retrieval-augmented generation (RAG), personalized agents [153], and question answering [314, 375].
   译文：long-term memory（时间维度）：聚焦 multi-session 对话系统 [196, 327]、RAG、个性化 agent [153] 与问答 [314, 375] 中的 memory management、利用与个性化。
   取舍：temporal 译「时间维度」，与 context、模型内部、跨来源三个维度统一命名；原文列举顺序与引用位置不动。

5. 原文：To highlight impactful work while mitigating publication-age bias, we introduced the Relative Citation Index (RCI), a log-log regression based, time-normalized metric adapted from the RCR framework [110].
   译文：为凸显有影响力的工作并缓解发表年份偏差，我们引入相对引用指数（Relative Citation Index, RCI），这是一种基于双对数回归、按时间归一化的指标，改编自 RCR 框架 [110]。
   取舍：publication-age 译「发表年份」而非「出版年龄」；mitigating 保留「缓解」的程度，不写成「消除」；时间归一化与后文 RCI 公式口径一致。

6. 原文：Similar to human cognition, this short-term memory can be consolidated into long-term memory through processes such as summarization [190] and storage to external databases or model parameters.
   译文：与人类认知类似，这种 short-term memory 可通过摘要 [190] 以及存储到外部数据库或模型参数等过程整合为 long-term memory。
   取舍：consolidated 在动词位译「整合」，与名词 consolidation 的英文原形分工；storage to 拆成「存储到」，避免「存储至外部数据库的存储」这类叠词。

7. 原文：Memory Consolidation plays a central role in shaping long-term memory by stabilizing short-term context into enduring representations.
   译文：memory consolidation 通过将短期 context 稳定为持久表示，在塑造 long-term memory 中发挥核心作用。
   取舍：plays a central role 拆为「在……中发挥核心作用」，避开「扮演核心角色」；enduring 与 persistent 统一译「持久」，不引入「耐久」。

8. 原文：Memory Condensation is the inference-time process of transforming raw, retrieved long-term memories into a structured and compact context for the LLM.
   译文：memory condensation 是推理时过程，将原始、已检索的 long-term memory 转化为供 LLM 使用的结构化、紧凑 context。
   取舍：inference-time 译「推理时」，不译「推断期」；raw 与 retrieved 各留一个限定，不合并为「原始检索结果」。

9. 原文：Long-term memory evaluation remains constrained by static assumptions. Current benchmarks mainly follow two paradigms: knowledge-based question answering (QA) and multi-turn dialogue.
   译文：long-term memory 评估仍受静态假设制约。当前 benchmark 主要遵循两种范式：基于知识的问答（QA）与多轮对话。
   取舍：remains constrained by 译「仍受……制约」，保留「尚未摆脱」的意味；paradigms 译「范式」，保持方法论层级。

10. 原文：Mismatch between memory retrieval and memory-grounded generation reveals context engineering bottlenecks.
    译文：memory retrieval 与 memory-grounded generation 之间的失配揭示了 context engineering 的瓶颈。
    取舍：mismatch 译「失配」，与后文 retrieval—generation 的「差距」错开；bottlenecks 直译「瓶颈」，不改成「短板」。

11. 原文：Memory in biological systems offers key insights for building more resilient and adaptive AI memory architectures. The brain manages the stability–plasticity dilemma through complementary learning systems: the hippocampus encodes fast-changing episodic experiences, while the cortex slowly integrates stable long-term memory [144, 199].
    译文：生物系统中的 memory 为构建更具韧性与自适应性的 AI memory architecture 提供了关键洞见。大脑通过互补学习系统管理稳定性—可塑性困境：海马体编码快速变化的 episodic 经验，而皮层缓慢整合稳定的 long-term memory [144, 199]。
    取舍：stability–plasticity dilemma 译「稳定性—可塑性困境」；hippocampus / cortex 用中文学名「海马体」「皮层」，episodic 仍保留英文；encodes / integrates 分落「编码」「整合」。

12. 原文：This survey provides a comprehensive overview of agent memory, classifying it into parametric and contextual types and mapping operations to encoding, evolving, and adapting.
    译文：本综述全面概述 agent memory，将其分为 parametric 与 contextual 类型，并将操作映射到 memory encoding、memory evolving 与 memory adapting。
    取舍：overview 译「概述」，避免与 survey 的「综述」重复；三个类别补 memory 前缀，与正文 2.4 节术语一致。

## 3 存疑译法

- **integration 与 consolidation 的分层**（译本 L184、L173）：名词写 `integration`，动词写「整合」；名词写 `consolidation`，动词也写「整合」。同句可能出现「integration 可能跨越……整合进……」的双重形态，读者需靠英文原形区分两类操作。
- **「检索」只作动词**（译本 L96、L140、L167 等 20 处）：名词一律 `retrieval`，动词一律「检索」。代价是「retrieval 检索」「检索到的 memory」这类中英混排略生硬，但可避免「检索 retrieval」叠词。
- **「压缩 / 嵌入 / 遗忘」动词化**（译本 L271、L349、L1361）：名词保留 `compression` / `embedding` / `forgetting`，动词用中文。若严格全保留英文，句子会出现「compression parametric memory」「embedding 异构输入」这类不合语法的搭配。
- **「中间迷失（lost in the middle）」**（译本 L90、L269）：保留中文既有现象名并括注原词。严格按新规则应只留 `lost in the middle`；此处为可读性牺牲了形态一致。
- **「更整合的范式」**（译本 L377）：integration 的形容词化未改成 `integration`，否则句子碎裂；属顺口牺牲准确性。
- **「适配」「演进」的普通义**（译本 L233、L353、L383、L433）：指 adapt / evolve 的一般动作，不是 `adapting` / `evolving` 类别名；未改英文，以免与三分类混淆。
- **「个性化」**（全文）：`personalization` 不在保留清单内，统一用中文；与 `persona`（人物形象）分开。
- **「推理经验 consolidation」**（译本 L167）：原文为 reasoning experience consolidation，为可读性补出「经验」二字，未改变结构。
- **「自演进对齐」「显著 memory distillation」**（译本 L194）：前者对应 self-evolution alignment，后者已改为 `salient memory distillation`；「显著」曾误作中文形容词，已回改。
