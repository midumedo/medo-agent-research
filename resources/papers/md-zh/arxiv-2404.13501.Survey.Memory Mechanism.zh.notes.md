# 译法摘记：arxiv-2404.13501

## 1 术语定译表

关键术语一律保留英文原形，中文只承担叙述、连接与论证。

| 英文 | 定译 | 备选 | 理由 |
| :--- | :--- | :--- | :--- |
| memory | memory（保留） | 记忆 | 全文 460 次，译中文会与“存储、回忆、经验”混同 |
| agent / LLM-based agent | agent（保留） | 智能体 | 与 memory、prompt 并置时保持术语链完整 |
| trial / step | trial、step（保留） | 试次 / 步 | 层级词，译中文后 inside-trial 等派生词无法统一 |
| inside-trial / cross-trial | 保留 | 试次内 / 跨试次 | 与 trial 同源，须一并保留 |
| token | token（保留） | 词元 | 原文与 embedding、sequence 并置 |
| parametric / textual | 保留 | 参数化 / 文本 | 两种 memory form 的对称标签 |
| latent space | latent space（保留） | 隐空间 | 与 continuous／discrete space 对照 |
| context / context window | context（保留） | 上下文 | 与 prompt、memory 构成三层概念 |
| prompt | prompt（保留） | 提示词 | 与 context 刻意区分 |
| retrieval / retrieve | retrieval（名词）、retrieve（动词） | 检索 | 名词、动词形态随原文，不强行统一 |
| RAG | RAG（保留） | 检索增强生成 | 首次出现处保留全称 retrieval-augmented generation（RAG） |
| embedding | embedding（保留） | 嵌入 | 与向量索引语境绑定 |
| consolidation | consolidation（保留） | 合并 | 与 reflection、forgetting 并列的三类 management 操作 |
| forgetting | forgetting（保留） | 遗忘 | 同上；亦用于 catastrophic forgetting |
| working / long-term / short-term memory | 保留 | 工作 / 长期 / 短期记忆 | 认知心理学术语，保留原形避免与中文译名冲突 |
| episodic / semantic / procedural memory | 保留 | 情节 / 语义 / 程序记忆 | 本文实际只出现 episode memory |
| KV cache | 保留（本文未出现） | 键值缓存 | 规则要求保留；源文无此词 |
| attention | attention（保留） | 注意力 | 与 quadratic complexity 语境绑定 |
| fine-tuning | fine-tuning（保留）；SFT 首次给全称 | 微调 | 与 training、editing 并列 |
| LoRA | LoRA（保留） | 低秩适配 | 方法名 |
| distillation | 保留（本文未出现） | 蒸馏 | 规则要求保留 |
| benchmark | benchmark（保留） | 基准 | 与 ground truth 同属评估词 |
| ground truth | ground truth（保留） | 标准答案 | 评估语境固定 |
| session / episode | session、episode memory（保留） | 会话 / 情节 | 与 trial 区分 |
| recall / precision | recall、precision（保留） | 召回率 / 精确率 | 与 F1 公式一致 |
| harness | 保留（本文未出现） | 治理框架 | 规则要求保留 |
| self-evolution / self-evolving | 保留 | 自演化 | 与 agent 的演化能力绑定 |

不属于强制清单、仍用中文的词：observation → 观测；coherence → 连贯性；consistency → 一致性；engagement → 参与度；knowledge editing → 知识编辑；reference accuracy → 参考准确率；ability level → 能力水平。

## 2 信达雅句例

1. 原文：Large language model (LLM) based agents have recently attracted much attention from the research and industry communities.  
   译文：基于 LLM 的 agent 近来受到研究与产业界的广泛关注。  
   取舍：`LLM-based` 拆为“基于 LLM 的”，保留 LLM 与 agent 原形，避免“大模型智能体”再造术语。

2. 原文：The key component to support agent-environment interactions is the memory of the agents.  
   译文：支撑 agent-environment interaction 的关键组件是 agent 的 memory。  
   取舍：保留复合名词原形，让“组件—交互—memory”的关系在读英文文献时不需回译。

3. 原文：The complete agent-environment interaction process is called a trial, and each interaction turn is called a step.  
   译文：完整的一次 agent-environment interaction 过程称为一个 trial，每一次交互轮次称为一个 step。  
   取舍：trial／step 不译，直接以原词建立层级，后文 inside-trial、cross-trial 才不会断裂。

4. 原文：This operation aims to project the raw observations into the actually stored memory contents, which are more informative [7] and concise [6].  
   译文：该操作旨在将原始观测投影为实际存储的 memory content，这些内容更具信息量 [7] 且更简洁 [6]。  
   取舍：project 取“投影”而非“投射”，保留函数映射的技术含义；observations 用中文“观测”，因它是接口层动作而非术语标签。

5. 原文：Textual form is currently the mainstream method to represent the memory contents, which is featured in better interpretability, easier implementation, and faster read-write efficiency.  
   译文：文本形式目前是表示 memory content 的主流方法，其特点是可解释性更好、实现更容易、读写效率更高。  
   取舍：三个比较级并列保留，不合并为“易用高效”，以免丢失原文的三项论证。

6. 原文：Caching the memory according to recency is an effective way to enhance memory efficiency, and it enables agents to focus more on the recent information.  
   译文：按近期性对 memory 做 cache 是提升 memory efficiency 的有效方式，它使 agent 能够更多关注近期信息。  
   取舍：cache 作动词时中文无对应单字，补“做”使句子成立，同时保留 cache 的技术含义。

7. 原文：The retrieval methods considerably depend on the accuracy and efficiency of obtaining expected information.  
   译文：retrieval 方法在很大程度上依赖获取预期信息的准确性与效率。  
   取舍：considerably 译“在很大程度上”，比“极大依赖”更贴原语气；expected information 不作“期望信息”，避免统计歧义。

8. 原文：Essentially, parametric memory boasts a higher information density, expressing semantics through continuous real-number vectors in a latent space, whereas textual memory employs a combination of tokens in a discrete space for semantic expression.  
   译文：本质上，parametric memory 具有更高的信息密度，通过 latent space 中的连续实值向量表达语义，而 textual memory 使用离散空间中的 token 组合进行语义表达。  
   取舍：boasts 不译“吹嘘”，取“具有”以保持学术中性；continuous real-number vectors 逐项保留。

9. 原文：The intuition behind this type of approaches is that if the agent can successfully complete a task that highly depends on memory, it suggests that the designed memory module is effective.  
   译文：这类方法背后的直觉是：若 agent 能够成功完成高度依赖 memory 的任务，则说明所设计的 memory module 有效。  
   取舍：intuition 译“直觉”而非“思路”，保留方法论意味；用“若……则……”显式呈现推理链。

10. 原文：For human beings, memory information is constantly processed and abstracted in the brains.  
    译文：对人类而言，memory information 在大脑中不断被处理与抽象。  
    取舍：全句只有“处理与抽象”是动作，其余保留原形，避免把 memory 拆成“记忆信息”后失去术语连续性。

11. 原文：We separate the entire procedure of memory into three operations: memory writing, memory management, and memory reading.  
    译文：我们将 memory 的整体流程分为三种操作：memory writing、memory management 与 memory reading。  
    取舍：三个操作名整体保留，使 5.3 各小节标题与正文严格对齐。

12. 原文：Without memory, there is no culture. Without memory, there would be no civilization, no society, no future.  
    译文：没有记忆，就没有文化。没有记忆，就没有文明、没有社会、没有未来。  
    取舍：唯一保留中文“记忆”的位置；引语属修辞而非术语，且中文已有通行译法，保留排比节奏。

13. 原文：The memory of an agent is key to achieving lifelong learning, as it needs to learn to store and apply the past observations.  
    译文：agent 的 memory 是实现终身学习的关键，因为它需要学会存储并应用过去的观测。  
    取舍：key 译“关键”而非“钥匙”，避免比喻；it 明确指 memory，故补“它”。

## 3 存疑译法

- “记忆”仅存于开篇 Elie Wiesel 引语（第 81 行）。此处 memory 是修辞义，译中文更顺；与全文技术义分开处理。
- “知识编辑”（knowledge editing）：不在强制清单，且中文文献通用，故未保留英文。位置 5.2.2、5.2.2 讨论段。
- “连贯性／一致性／参与度”：coherence、consistency、engagement 三者需在中文语感上区分，保留英文反而增加负担。位置 6.1.1、6.2.1。
- “观测”（observation）：指环境返回给 agent 的反馈，中文 RL 文献常用“观测”；保留 observation 会使“原始观测投影”一句过长。
- “memory 功能”（memory function）：此处 function 是叙述词而非术语，译“功能”以断开与 memory module 的重复。位置 5.3、7。
- “按近期性对 memory 做 cache”：为动词顺口加了“做”；严格对应原文 caching 分词结构时略松。位置 5.2.1。
- “从 memory 中 recall 时”：recall 作动词保留，若译“回忆”会引入心理学色彩。位置 7.2。
- “episode memory”：源文为 episode memories / episode memory，未写成 episodic memory；已按原词统一。位置 7.1。
- “空间任务”（spacial tasks）：源文拼写疑为 spatial，按原义译“空间”，未擅改。位置 6.2.4。
- 第 460 行一段内集中出现 memory、episode memory、context、prompt、SFT、retrieval，中文连接词被压缩，可读性低于其余段落。
- “数字生命卡”（digital life card）：源文比喻直译，中文读者需借同句“可插拔的 parametric memory”才能理解。位置 8.1。
- “参考准确率”（reference accuracy）：取“参考”而非“引用”，因该指标比对的是检索到的 memory 与预置 ground truth，而非文献引用。位置 6.1.2。
