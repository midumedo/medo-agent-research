# 译法摘记：arxiv-2602.06052.Survey.Agent Memory

对应译本：`arxiv-2602.06052.Survey.Agent Memory.zh.md`。术语策略为「关键术语保留英文原形，中文承担叙述与连接」，下表只收反复出现或易译错的词。

## 1. 术语定译表

| 英文 | 定译 | 备选 | 一句话理由 |
| :--- | :--- | :--- | :--- |
| memory | memory（保留） | 记忆 | 核心术语；全篇统一，复合词沿用原形 |
| agent / foundation agent | agent / foundation agent | 智能体 / 基础智能体 | 与 agent memory、agentic 术语链一致 |
| memory substrate | memory substrate | 记忆基质 | 三维分类维度名，需与原文一一对应 |
| memory subject | memory subject | 记忆主体 | 同上 |
| cognitive mechanism | cognitive mechanism | 认知机制 | 同上 |
| memory operation | memory operation | 记忆操作 | §4 节名与操作链同形 |
| memory policy | memory policy | 记忆策略 | §5 全节统一 |
| parametric | parametric | 参数化 | parametric memory/state/policy 同形 |
| latent state / latent token | 保留 | 潜状态 / 潜 token | 与 latent representation 等系列一致 |
| KV cache | KV cache | 键值缓存 | 原文即缩写；译「缓存」会与 buffer 混淆 |
| context / context window | 保留 | 上下文 / 上下文窗口 | context 含义宽，中译易窄化 |
| prompt | prompt | 提示 | prompt-driven、prompt engineering 保持同形 |
| harness | harness | 运行框架 | agent harness 为固定说法 |
| retrieval | retrieval | 检索 | retrieval-augmented、RAG 同形 |
| embedding | embedding（名词） | 嵌入 | 动词义仍用「嵌入」 |
| consolidation | consolidation（名词） | 整合 | 动词义仍用「整合」 |
| forgetting | forgetting（名词） | 遗忘 | 动词义仍用「遗忘」 |
| benchmark | benchmark | 基准 | 与 evaluation 区分，避免「基准」泛化 |
| ground truth | ground truth | 标准答案 / 真值 | 避免与逻辑「真值」混淆 |
| session / episode | 保留 | 会话 / 情景 | multi-session、cross-episode 同形 |
| long-horizon | long-horizon | 长时程 | 与标题、§6 一致 |
| self-evolving | self-evolving | 自我演化 | 与 self-evolution 区分词性 |
| token | token | 词元 | 保留原词，避免「词元」歧义 |
| fine-tuning / distillation | 保留 | 微调 / 蒸馏 | 方法名保持原形 |
| attention | attention | 注意力 | 与 KV cache、attention score 一致 |

## 2. 信达雅句例

**例 1（摘要，utility gap）**
原文：Memory, with hundreds of papers released in 2025, therefore emerges as the critical solution to fill the utility gap.
译文：因此，memory——2025 年有数百篇相关论文发表——成为填补这一 utility gap 的关键解决方案。
取舍：保留破折号插入语；utility gap 不译「效用缺口」，避免生造名词。

**例 2（摘要，working memory 的门控）**
原文：short-term memory gates which experiences are perceived, selected, and abstracted during execution.
译文：short-term memory 在执行过程中对哪些经验被感知、选择和抽象进行门控。
取舍：gate 译「门控」而非「控制」，保留其筛选机制的技术含义；从句语序按中文调整。

**例 3（§1，foundation agent 定义）**
原文：we define a foundation agent as an autonomous or semi-autonomous system driven by a foundation model, augmented with perception, reasoning, planning, tool use, and memory management.
译文：我们将 foundation agent 定义为由基础模型……驱动，并辅以感知、推理、规划、工具使用与 memory management 的自主或半自主系统。
取舍：augmented with 译「辅以」，不用「增强」，以免与 memory augmentation 撞词。

**例 4（§2.2，memory 的定义句）**
原文：Memory generally refers to a system's capacity to retain, organize, and utilize information over time.
译文：memory 一般指系统随时间保留、组织与利用信息的能力。
取舍：三个动词按「保留—组织—利用」递进排列，与后文 memory operation 的分类呼应。

**例 5（§3.1.1，external memory 定义）**
原文：External memory refers to any memory substrate that stores knowledge, information, and past experience outside the agent's model parameters or state.
译文：external memory 指任何将知识、信息与过往经验存储在 agent 模型参数或状态之外的 memory substrate。
取舍：「outside」后置为「在……之外」，保证定义的可判定性；memory substrate 不译，维持分类维度名。

**例 6（§3.1.1，计算与知识分离）**
原文：It operates independently of the gradient-updated weights in a neural network.
译文：它独立于神经网络中由梯度更新的权重运行。
取舍：把 independently of 拆成「独立于……运行」，避免「独立运行于」的歧义。

**例 7（§3.1.2，weight memory）**
原文：Weight memory is implemented by making memory writes parametric, so that the model can later recall information without retrieving external context.
译文：weight memory 通过将 memory write 参数来实现，使模型之后无需 retrieval 外部 context 即可回忆信息。
取舍：保留 memory write 的原形，避免「记忆写入」与 memory write 反复切换；recall 译「回忆」以区别 retrieval。

**例 8（§3.2.2，working memory 的容量约束）**
原文：working memory operates under strict capacity constraints, supporting online manipulation, reasoning, and control of information.
译文：working memory 在严格容量约束下运行，支持在线信息操作、推理与控制。
取舍：「online」译「在线」而非「实时」，与认知心理学中的 online processing 对齐。

**例 9（§3.1.3，无单一基质占优）**
原文：Overall, no single substrate dominates across all settings and environments.
译文：总体而言，没有任何单一 substrate 在所有设置与环境中占优。
取舍：dominates 译「占优」而非「主导」，保留比较级含义；substrate 以单数形式承接前文的类指。

**例 10（§4.1.4，压缩与总结的机制）**
原文：Compression and summarization reduce redundancy and improve memory efficiency by converting fine-grained episodic records into more compact, more abstract representations.
译文：Compression 与 Summarization 通过将细粒度 episodic record 转换为更紧凑、更抽象的表示，减少冗余并提升 memory efficiency，从而满足这一需求。
取舍：两个动名词并列保留英文；把 by converting 前置为手段状语，符合中文因果顺序。

**例 11（摘要/结论，memory 作为自我演化的基质）**
原文：Beyond serving as passive storage, memory is increasingly the substrate through which agents self-evolve.
译文：除了作为被动存储，memory 日益成为 agent 借以 self-evolving 的 substrate。
取舍：把 through which 译为「借以」，保留「基质—经由—演化」的因果链；self-evolving 保留原形以对应 self-evolution。

## 3. 存疑译法

- **操作动词仍为中文**（§3.2.2、§4.1.4、§4.1.5）：整合、压缩、嵌入、检索、遗忘、修剪作谓语时未替换为英文名词。原因：英文名词无法直接带中文宾语，硬换会产生「consolidation 为」「retrieval 出」一类病句。
- **summarization 未统一**（§4.1.4、§7.2）：标题用 Summarization，正文多作「总结」。为保动词流畅牺牲了词形一致。
- **标题混合式**（全部小节标题）：采用「英文术语 + 中文虚词」，如「4.1 Single-Agent Systems 的 Memory Operations」。全英文标题会与「翻译」定位冲突，故折中。
- **weight memory / state memory**（§3.1.2，约 145–147 行）：原文为 weight-based / state-based memory，译文保留「weight/state + memory」的混合形。
- **memory trace 或 engram**（§2.2，约 105 行）：原文 "memory traces or memory engrams"，合并后只各保留一次，弱化了「痕迹/印迹」的原措辞。
- **substrate 不标单复数**（§3.1.3、§4.2 等）：按英文 mass-noun 习惯处理，中文语境下无法区分单复数。
- **scene 与 episode 的边界**（§4.1.1、§6.2）：episode 义项统一为 episode，泛称「场景」仍用中文「场景」，依赖上下文判断。
- **subject 级区分**（§3.3，约 243 行）：原为 subject-level distinction，直译后略生硬，未找到更自然的等价表达。
- **benchmark 之外**（§7.2，约 501 行）：源译此处原有残字「确」，已修正；整句仍是长定语，读起来偏绕。
- **表格列名仍为中文**（表 1、表 5）：如「维度」「代表性工作」「任务环境」等列名保留中文，未按术语规则英文化。
- **structured / hierarchical memory**（§3.1.1）：修饰语仍为「结构化/层次化」，仅 memory 保留英文，形成半混合形式。
