# 译法摘记 · arxiv-2512.13564.Survey.Age of Agent Memory

## 1. 术语定译表

| 英文 | 定译 | 备选 | 一句话理由 |
| :--- | :--- | :--- | :--- |
| memory | 保留英文 | 记忆 | 中文「记忆」兼指记忆动作与所记内容，本文指可读写、可演化的表示，用原词避免歧义 |
| agent memory | 保留英文 | 智能体记忆 | 译名易被读成「agent 的记忆能力」，而本文指的是一个可被设计的系统 |
| long / short-term memory | 保留英文 | 长期／短期记忆 | 本文用它做对照坐标，中文译名会掩盖它与 episode 边界的对应关系 |
| working memory | 保留英文 | 工作记忆 | 认知科学既有译名易被读成「临时缓存」 |
| factual / experiential memory | 保留英文 | 事实／经验记忆 | 与 LLM memory 对比时才显出功能差异，译名会丢失这层对照 |
| episodic / semantic / procedural memory | 保留英文 | 情节／语义／程序性记忆 | 三分法在本文中是类型标签而非修辞，保留原形便于与其他文献对齐 |
| token | 保留英文 | 词元、令牌 | 本文的 token 是可写可读的表示单元，不是分词单位 |
| parametric | 保留英文 | 参数化 | 与「参数内化」是两件事，译成中文后容易混同 |
| latent | 保留英文 | 潜在、隐 | 中文「潜在」另有 potential 义，见第 3 节 |
| context / context window | 保留英文 | 上下文／上下文窗口 | context 兼指窗口内容与情境，中文译名会锁定为前者 |
| prompt | 保留英文 | 提示词 | 与 context engineering 并列出现时须区分层级 |
| harness | 保留英文 | 框架、脚手架 | harness 特指包裹模型的运行装置，译「框架」会与 framework 混同 |
| retrieval | 保留英文 | 检索 | 与 RAG 的 retrieve 同源，译「检索」遮蔽了二者是同一动作 |
| RAG | 保留缩写 | 检索增强生成 | 社区通名，展开成中文反而增加噪声 |
| embedding | 保留英文 | 嵌入 | 中文「嵌入」兼作动词，名词场合一律用原词 |
| consolidation | 保留英文 | 巩固 | 对应 memory consolidation 的实验语境，不与「整合」混用 |
| forgetting | 保留英文 | 遗忘 | 与 consolidation 成对出现，须保持同一套词形 |
| attention | 保留英文 | 注意力 | 本文兼指 attention 机制与研究关注度，中文无法区分 |
| KV cache | 保留英文 | 键值缓存 | 通用缩写，展开后反而不好检索 |
| LoRA / fine-tuning / distillation | 保留英文 | 低秩适配／微调／蒸馏 | 均为 LoRA 生态内的固定词形，混译会破坏一致性 |
| benchmark | 保留英文 | 基准 | 中文「基准」另有 baseline 义 |
| ground truth | 保留英文 | 真值 | 避免与「标准答案」这类口语混淆 |
| session / episode | 保留英文 | 会话／回合 | 本文用二者区分交互容器与任务单元，中文常混用 |
| experience | 保留英文 | 经验 | 与 experiential memory 是同一词根，须一起保留 |

## 2. 信达雅句例

**1.** 原文：Memory has emerged, and will continue to remain, a core capability of foundation model based agents.
译文：memory 已经成为、并将继续作为 foundation model 驱动的 agent 的核心能力。
取舍：原文用完成时加将来时的双重断言，中文用「已经、并将继续」保留这种时间张力，不合并为「一直是」。

**2.** 原文：Rather than treating memory as a static repository to be queried, memory generation emphasizes the agent's ability to actively synthesize new memory representations on demand.
译文：memory generation 不把 memory 当作待查询的静态仓库，而强调 agent 按需主动综合新 memory 表示的能力。
取舍：rather than 结构前置为否定小句，让「被查」与「被生成」的对比落在同一句的同一层级。

**3.** 原文：Experiential memory encapsulates the mechanism by which agents encode historical trajectories, distilled strategies, and interaction outcomes into durable, retrievable representations.
译文：experiential memory 概括 agent 将历史 trajectory、distillation 后的 strategy 与交互结果编码为持久、可 retrieval 表示的机制。
取舍：encapsulates 译「概括」而非「封装」，因为此处说的是概念范围而非实现细节；三个并列宾语保持原序。

**4.** 原文：Unlike working memory, which manages transient context, experiential memory focuses on the long-term accumulation and transfer of knowledge across distinct episodes.
译文：与负责瞬时 context 的 working memory 不同，experiential memory 关注知识在不同 episode 之间的长期积累与迁移。
取舍：把插入语改为前置定语，中文更顺；accumulation 与 transfer 译为「积累与迁移」，保留它们各自的时间含义。

**5.** 原文：This implementation difference grants agents a unique capability absent in biological counterparts: the ability to introspect, edit, and reason over their own procedural knowledge.
译文：这一实现差异赋予 agent 生物对应物所不具备的独特能力：对自身 procedural knowledge 进行内省、编辑与推理。
取舍：biological counterparts 译「生物对应物」而非「生物体」，因为比较对象是机制而非物种。

**6.** 原文：The central objective is to furnish an updatable, retrievable, and governable external fact layer, providing a stable reference across sessions and stages.
译文：其核心目标是提供一个可更新、可 retrieval、可治理的外部事实层，在 cross-session 与跨阶段提供稳定参照。
取舍：三个 -able 形容词保持同构；复数 sessions 用 cross-session 表达，避免「跨会话」与 session 术语脱节。

**7.** 原文：This mechanism ensures that individual agents directly benefit from collective knowledge, thereby suppressing contradictory conclusions and enhancing overall system efficiency.
译文：这一机制确保个体 agent 直接从集体知识中获益，从而抑制矛盾结论并提升整体系统效率。
取舍：suppressing 译「抑制」而非「消除」，因为原文说的是降低出现概率，不是杜绝。

**8.** 原文：By maintaining a centralized repository of past queries and responses, frameworks such as Memory Sharing enable agents to access and build on peers' accumulated insights asynchronously.
译文：Memory Sharing 等框架维护过往查询与响应的集中式仓库，使 agent 能够异步访问并基于同伴积累的洞见继续工作。
取舍：build on 译「继续工作」会丢失「在其上叠加」，故译为「基于……继续工作」，保留支撑关系。

**9.** 原文：In the conceptual landscape, agent memory and RAG share substantial overlap: both construct, organize, and leverage auxiliary information stores to extend the capabilities of LLMs/agents beyond their native parametric knowledge.
译文：在概念层面，agent memory 与 RAG 存在大量重叠：两种系统都构建、组织并利用辅助信息库，以将 LLM/agent 的能力扩展到其原生 parametric knowledge 之外。
取舍：landscape 不译「图景」而译「层面」，因为本段讨论的是概念范围；三个动词保持并列以对应原文节奏。

**10.** 原文：Strategy-based Memory distills transferable reasoning patterns, workflows, and high-level insights from past trajectories to guide planning across diverse scenarios.
译文：Strategy-based Memory 从过往 trajectory 中 distillation 可迁移的 reasoning 模式、workflow 与高层洞见，以指导多样场景下的 planning。
取舍：distill 用名词派生形式嵌进中文动词位，避免造出「蒸馏出」这种半术语化的说法；三个宾语按抽象层级由低到高排列。

**11.** 原文：Biological systems rely on distributed neural circuits for implicit skill acquisition.
译文：生物系统依赖分布式神经回路实现隐式技能习得。
取舍：acquisition 译「习得」而非「获取」，固定搭配上更贴近认知科学用法。

**12.** 原文：Crucially, experiential memory serves as a foundation for continual learning and self-evolution in the era of experience.
译文：关键在于，experiential memory 是 experience 时代持续学习与自我演化的基础。
取舍：era of experience 是原文自带的论断，不译作「经验时代」，以免与 experiential memory 的「经验」混为一个概念。

## 3. 存疑译法

- **potential 与 latent 同形**：`潜在` 在 2.2、4.1.2、5.1.3、5.3 等处作「potential（可能的）」用，一律保留中文，未改为 latent；只有「潜在 token／内容／摘要／KV」等明确指向表示空间的场合改了。位置：§2.2 末段、§4.1 末段、§5.1.3、§5.3.1、§7.4。
- **attention 与「关注」同形**：§7.1.2、§7.4 的「注意力转向／自然扩展到」指研究关注，保留中文，未改为 attention；其余指 attention 机制处已改。位置：§7.1.2 第二段、§7.4 首段。
- **`memory attention KV`**：表 3 中 FOT 一行原表该格文本不明（源文为机器转换产物），译文强行作 `memory attention KV`，未能确定原意。位置：§3.3.2 表 3。
- **表 4 MemVerse 行错位**：源表该行 Cell 列被填入 `√`，其余列内容错位到表 1 的字段，译文按源表原样照录，未纠正，也未猜测。位置：§4.1 表 4。
- **表 1 表头**：源文表头作 `Memory Structure`，据正文分类应为 `Memory Form`；译文保留源文字面，避免与正文不符的静默更正。位置：§3.1 表 1。
- **表 8 结构异常**：`SWE-Bench Verified` 行后缺 `</tr>`，译文连同表格 HTML 一并照录，仅在视觉上不影响渲染。位置：§6.1.1 表 8。
- **分页截断**：源文第 117–119 行一句被分页切开（`a capability fundamentally` / `grounded in agent memory.`），译文按跨行合并为一句，未加连接词。位置：§1 引言末段。
- **`Summary` 等小标题**：源文用粗体充当小节标签（`Summary`、`Knowledge Persistence`、`Shared Access`），译文保留粗体标签加英文原词，未另立中文小标题。位置：§3.1.1、§4.1.2、§4.2。
- **行数差异**：译文较源文少 19 行，源于合并源文的分页断句与多处标题前的空行差异，非删节；章节数、图数、表数、参考文献条目数与源文一致。
