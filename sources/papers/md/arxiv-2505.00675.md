---
id: arxiv-2505.00675
title: "Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics"
registry: arxiv
native_id: 2505.00675
version: ""
kind: [survey]
pdf: pdf/arxiv-2505.00675.pdf
pdf_sha256: "23724df6e6a38bdffc97c8bccb132581bf1e21fa534d5c19f84c80d5ab0e741d"
parser: pymupdf4llm (recorded by legacy script)
converted_at: null
---

# Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics

- arXiv: [2505.00675](https://arxiv.org/abs/2505.00675)
- 作者: Du, Yiming, Huang, Wenyu, Zheng, Danna, Wang, Zhaowei, Montella, Sebastien, Lapata, Mirella 等 8 人
- 发表日期: 2025/05/01

> 本文件是 PDF 的机器转换文本，转换成功不等于已对 PDF 做视觉核验。
> 上方元数据沿用历史抓取记录；其与当前 PDF 是否同版尚未核实。来源版本、获取时间及原转换环境缺失，不推测。
> 本地 PDF SHA256: `23724df6e6a38bdffc97c8bccb132581bf1e21fa534d5c19f84c80d5ab0e741d`。文件身份与转换信息见 [provenance.json](../provenance.json)。
> 下方分隔线之后为既有转换正文；本次只移除我方导航，不重新解析。

---

**Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics** 

YIMING DU<sup>∗</sup> , The Chinese University of Hong Kong, China and The University of Edinburgh, UK 

WENYU HUANG<sup>∗</sup> , The University of Edinburgh, UK 

DANNA ZHENG<sup>∗</sup> , The University of Edinburgh, UK ZHAOWEI WANG, The Hong Kong University of Science and Technology, China SEBASTIEN MONTELLA, Huawei Technologies Research & Development (UK) Limited, UK MIRELLA LAPATA, The University of Edinburgh, UK 

KAM-FAI WONG, The Chinese University of Hong Kong, China 

JEFF Z. PAN, The University of Edinburgh, UK and Huawei Technologies Research & Development (UK) Limited, UK 

**Abstract:** Memory is fundamental to large language model (LLM)-based agents, but existing surveys emphasize application-level use (e.g., personalized dialogue), while overlooking the atomic operations governing memory dynamics. This work categorizes memory into parametric (implicit in model weights) and contextual (explicit external data, structured/unstructured) forms, and defines six core operations: Consolidation, Updating, Indexing, Forgetting, Retrieval, and Condensation. Mapping these dimensions reveals four key research topics: long-term, long-context, parametric modification, and multi-source memory. The taxonomy provides a structured view of memory-related research, benchmarks, and tools, clarifying functional interactions in LLM-based agents and guiding future advancements. The datasets, papers, and tools are publicly available at https://github.com/Elvin-Yiming-Du/Survey_Memory_in_AI. 

# **1 Introduction** 

Memory is a core component of Large Language Model (LLM) based agents [301] and a critical step towards AGI [228], enabling persistent interactions [196, 375], reasoning [78], multi-modal understanding [189], personalization [153], and multi-agent collaboration [298]. While recent studies explore memory sources [65, 207], operations [23, 281, 350, 375], and application [97, 189, 202, 255]. A unified and systematic framework for organizing and evolving agent memory remains lacking. 

Existing surveys on agent memory adopt type-based and cognitive-inspired perspectives, offering valuable overviews but a limited unified but lacks operational formalization; most focus on subtopics, such as long-context modeling [108], long-term memory [94, 126], personalization [177], or knowledge editing [297], without unifying core operations. Zhang et al. [367] covers only high-level operations such as writing, management, and reading, and misses some operations like indexing. More broadly, few surveys define the scope of memory research, analyze technical implementations, or provide practical foundations such as benchmarks and tools. 

To address these gaps, we categorize memory into _parametric_ and _contextual_ types. Parametric memory encodes knowledge implicitly in model parameters [289], while contextual memory stores explicit external information, either structured (e.g., graphs, tables, trajectories [239]), or unstructured (e.g., text [375], vectors, audio, video [189]). Temporally, memory spans both long-term (e.g., multi-turn dialogue, external observations [153]) and short-term contexts (e.g., kv-cache, current dialogue history [226]). Based on these types, we define six memory operations, which can be further classified into three categories: _Encoding_ , _Evolving_ , and _Adapting_ . Memory encoding encompasses consolidation (integrating new knowledge into persistent memories [73]) and indexing (organizing memory for retrieval [314]). 

> ∗Both authors contributed equally to this research. 

1 

Du et al. 

2 

Memory evolving includes updating (modifying existing memory to incorporate recent updates [32]) and forgetting (removing outdated or incorrect content [277]). Memory Adapting covers retrieval (accessing relevant memory [84]) and condensation (reducing size while preserving key information [32]). 

Beyond this structural taxonomy, functional perspectives of memory provide a complementary lens for understanding LLM systems. Episodic memory, rooted in cognitive psychology [279], stores temporally anchored experiences—such as dialogue histories and event sequences—and supports reasoning and adapting in dynamic environments [74, 207]. Semantic memory encodes structured and generalizable knowledge, often formalized as queryable knowledge graphs or tables, complementing parametric memory to enhance reasoning and retrieval-augmented generation (RAG). Procedural memory captures task execution patterns and learned trajectories, typically formed through large-scale training or reinforcement learning with chain-of-thought data, and drives efficient tool use and problem-solving in task-oriented agents. Working memory acts as a dynamic control mechanism that integrates short-term caches and activated longterm knowledge, enabling real-time reasoning, planning, and decision-making. These functional types highlight the diverse roles memory can play in supporting LLM capabilities and inform the operational framework we propose. 

To ground our operational framework, we conduct a pilot study and define four core topics. These topics span complementary dimensions of memory research and represent critical frontiers in developing capable AI agents: 

- **Long-Term Memory** (temporal), focusing on memory management, utilization, and personalization in multisession dialogue systems [196, 327], retrieval-augmented generation (RAG), personalized agents [153], and question answering [314, 375]. 

- **Long-Context Memory** (contextual), addressing both parametric efficiency (e.g. "KV cache eviction" [368]) and context utilization effectiveness (e.g., long-context compression [36, 125]) in handling extended sequences. 

- **Parametric Memory Modification** (model-internal), covering model editing [70, 204, 289], unlearning [197], and continual learning [301] for adapting internal knowledge representations. 

- **Multi-Source Memory** (cross-source), emphasizing integration across heterogeneous textual sources [102] but also multi-modal inputs [281] to further support robust and scene-awareness reasoning. 

# **1.1 Research Methodology** 

To provide a systematic and comprehensive view of memory-related research, we first analyzed 37 seed papers that are widely recognized as foundational or representative in the memory-for-LLM literature. Through expert annotation and iterative discussion, these papers were used to define our taxonomy of memory types and core operations and to manually identify four primary research topics: long-term memory, long-context memory, parametric memory modification, and multi-source memory. These topics were selected because they 1) represent the areas most closely related to and actively studied within memory-centric LLM systems, 2) reflect distinct operational challenges across four complementary dimensions including temporal (such as persistence and personalization in long-term usage), 3) contextual (such as efficient handling and compression of long sequences), 4) model-internal (such as updating or editing knowledge within parametric representations), and 5) modality and integration (such as aligning and reasoning across heterogeneous or multi-modal sources), and collectively capture the breadth of recent developments from dialogue agents to retrieval-augmented reasoning systems. 

Building on this framework, we collected a large-scale corpus of over 30,000 papers published in top NLP and ML venues including NeurIPS, ICLR, ICML, ACL, EMNLP, and NAACL between 2022 and 2025, a period marked by the rapid emergence and evolution of large language models. Each paper abstract was evaluated using a GPT-based relevance 

3 

Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

scoring pipeline. Considering both cost and effectiveness, we selected GPT-4o-mini for its strong zero-shot reasoning ability and efficiency. Papers scoring ≥ 8 out of 10 according to our taxonomy-aligned task definitions were retained, yielding a curated set of 3,923 high-relevance papers. To ensure reliability, we conducted **manual validation** and **recall checks** on randomly sampled subsets, confirming that the threshold of 8 provides a balanced trade-off between precision and recall. 

To highlight impactful work while mitigating publication-age bias, we introduced the Relative Citation Index (RCI), a log-log regression based, time-normalized metric adapted from the RCR framework [110]. RCI adjusts raw citation counts according to publication age, enabling fair comparisons across papers and years. Empirical results showed that the log-log regression model achieved the best fit ( _𝑅_<sup>2</sup> = 0 _._ 97) and produced intuitive outcomes, with expected citations converging to zero for newly released papers. By integrating semantic relevance filtering and RCI-based impact assessment, we establish a balanced and reproducible foundation for analyzing research progress, trends, and topic-specific impact dynamics across the four core areas. 

# **1.2 Contribution and Structure** 

This survey contributes to both the research and industrial communities by offering a comprehensive and structured perspective on memory in AI agents. For the research community, our sruvey establishes a comprehensive conceptual foundation. It not only systematically organizes memory representations, types, and core operations, but also frames frontier topics through the lens of the memory lifecycle to elucidate how memory is encoded, evolved, and adapted in AI agents. For the industrial community, it provides an extensive overview of tools, products, and benchmarks, coupled with analyses of their functionalities and deployment scenarios. Thereby, our survey serves as a practical reference for designing and implementing memory-enabled applications. Furthermore, this survey synthesizes emerging trends and outstanding challenges, outlining promising avenues for future research and development in this rapidly evolving domain. 

The remainder of the paper is organized as follows. Section 2 provides readers with a comprehensive understanding of memory representation, memory types, functional memory categories, and core memory operations, forming a solid foundation for studying memory in agents. Section 3 maps high-impact topics to this foundation and summarizes key methods and datasets. Section 4 outlines real-world applications, products, and practical tools for building memoryenabled AI systems. Section 5 compares human and agent memory systems, highlighting operational parallels and differences. Section 6 concludes with future directions for memory-centric agent (see Figure 1 for an overview). 

# **2 Memory Foundations** 

Memory in agents can be understood through four complementary dimensions: **representation** , **timescale** , **functional type** , and **operations** . These perspectives jointly describe _what memory is_ , _how long it persists_ , _what role it serves_ , and _how it evolves_ . Representation defines the structural form of stored knowledge, timescale characterizes its temporal persistence, functional type captures the cognitive or computational role of stored content, and operation describes the dynamic processes that govern encoding, evolving, and adapting. Together, they provide an integrated framework linking the structure, function, and dynamics of memory in both human cognition and artificial intelligence. Together, these dimensions form the core dimensions for analyzing memory mechanisms in agents. 

Du et al. 

4 

<!-- Start of picture text -->
Memory Operations Contextual Memory High-Impact Topic Taxonomy Operations<br>Memory Encoding:<br>Consolidation Indexing Unstructured: …<br>Long Term   Contextual<br>Memory Evolving:<br>Updating Forgetting Structured: …<br>Memory Adapting: Session 2025-05-01T10:15:30Z<br>Retrieval Condensation My sister share with me her favourite photos.  Long Context Contextual, Parametric<br>Parametric Memory<br>Here is the album for you.<br>Parametric<br>Memory Parametric<br>Modification<br>Session 2025-05-10T15:42:10Z<br>Create table of contents for<br>the following files.<br>Contextual,<br>Multi Source Parametric<br>Here is the table for you…<br>…<br><!-- End of picture text -->

Fig. 1. A unified framework of memory: Taxonomy, Core Operations, and Applications in LLM-based agents. 

# **2.1 Memory Representation** 

From the perspective of memory representation, we divide memory into **Parametric Memory** and **Contextual Memory** , where the latter comprises both _Unstructured_ and _Structured_ forms. 

**Parametric Memory** refers to the knowledge implicitly stored within model internal parameters [21, 233, 289]. Acquired during pretraining or post-training, this memory is embedded in the model’s weights and accessed through feedforward computation at inference. It serves as a form of long-term and persistent memory enabling fast, context-free retrieval of factual and commonsense knowledge. However, it lacks transparency and is difficult to update selectively in response to new experiences or task-specific contexts. 

**Contextual Memory** denotes explicit, external information that complements model parameters and is categorized into unstructured and structured forms. **_Contextual Unstructured Memory_** refers to an explicit and dynamically evolving memory system that stores, retrieves, and updates situational information in unstructured formats such as text [375], images [281], audio [189] , videos [305, 352] or embeddings, derived from users, systems, and environments. It captures temporal [78], emotional [340], procedural [71], and semantic aspects of context without predefined schemas, enabling adaptive reasoning and continuity across interactions. The short-term form of Contextual Unstructured Memory includes concatenated prompts and Key–Value (KV) cache [336], which retains token-level representations during inference to maintain local coherence and efficient context reuse. In contrast, its long-term form extends to memory buffers [226], retrieval databases [295], or episodic storage [103] that store and refine contextual signals over time to support personalization and lifelong learning [153]. Meanwhile, **_Contextual Structured Memory_** denotes an explicit memory organized into predefined, interpretable formats or schemata, such as knowledge graphs [221, 308], relational tables [190], experiences [225] or ontologies [235], which remain easily queryable. These structures support symbolic reasoning and precise querying, often complementing the associative capabilities of pretrained language models (PLMs). While usually used as long-term memory, structured memory can be short-term, constructed at inference for local reasoning, or long-term, storing curated knowledge across sessions. 

Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

5 

# **2.2 Memory Timescale** 

Besides the representation, the timescale serves as another critical dimension. Drawing on the temporal persistence of information, memory is typically categorized into long-term and short-term memory. 

**Long-term Memory** refers to a cognitive system with virtually unlimited capacity for storing information over extended periods of time, ranging from hours to an entire lifetime [261]. In LLM agents, it refers to the ability to store, manage, and utilize information persistently across extended interactions with extended environment. This capability is essential for enabling continuity, personalization, and knowledge grounding in real-world applications such as multi-session agents [78], retrieval-augmented generation (RAG) [234], personalized assistants [65, 375], and long-term planning agents [329]. It encompasses both contextual memory (such as dialogue histories [103] and user-specific preferences [202, 358] and parametric memory (knowledge encoded within model parameters [23]). Meanwhile, it is closely aligned with functional perspectives, including semantic [295], episodic [183, 307], procedural [71] memory, which will be introduced in the following sections. 

**Short-term Memory** refers to the temporary storage of information for immediate use [192]. In LLM-based agents, it typically denotes the KV cache [336] or current context window [226], which holds task-relevant information to support real-time reasoning and decision-making. Similar to human cognition, this short-term memory can be consolidated into long-term memory through processes such as summarization [190] and storage in external databases or model parameters. In practice, short-term memory is especially critical in long-context scenarios, where it helps mitigate hallucinations, address the “lost in the middle” problem [180] in ultra-long contexts [350], reduce error accumulation in multi-turn interactions [381], and enhance the reliability of multi-turn tool usage [192]. 

# **2.3 Memory Functional Type** 

Beyond temporal persistence, memory can also be characterized by its functional roles in supporting agentic intelligence. Drawing on cognitive science, we further distinguish memory into episodic, semantic, procedural, and working memory. 

**Episodic memory** , a core type of _long-term memory_ originating from cognitive psychology [279], refers to the storage of past experiences linked to temporal cues, events, dialogue histories, and spatial contexts, and it dynamically evolves as the environment changes. It is widely regarded as a form of long-term memory [74] and, in modern agent systems, often functions as an external memory module [232] that complements parametric knowledge. Recent work on agents [207] increasingly explores how to update episodic memories [47, 155], perform temporal reasoning [78], and retrieve and utilize relevant experiences [207] to enhance adaptability and decision-making in dynamic environments [333]. 

**Semantic memory** another fundamental form of _long-term memory_ , refers to memory for facts concepts about the world [279]. In computational systems, it is often formalized into explicit, queryable structures such as knowledge graphs [239], relational tables [102], or implicit model parameters [226]. Within model parameters, semantic knowledge is encoded in distributed representations that capture general world facts and concepts learned during pretraining. In contrast to context-dependent episodic memory, semantic memory is relatively stable, generalizable, and abstracted from cumulative experiences. While in LLM, the boundary between semantic and episodic memory is often blurred, as parametric representations may intertwine factual knowledge with contextual associations. This integration of implicit and explicit semantic memory provides the foundation for memory-augmented reasoning and adaptive knowledge use in modern agents [381]. 

Du et al. 

6 

**Procedural memory** , also categorized as a form of _long-term memory_ , refers to memory that supports the execution of learned skills and action sequences without conscious awareness of prior experiences [71, 225, 377]. In intelligent agents, procedural memory is typically formed in two ways: stored explicitly in external skill repositories for reuse [377], or encoded implicitly through large-scale training [171]. Training on execution data like trajectories and CoT reasoning fosters consistent task performance, particularly in tool-augmented [192] and RL-based systems [350]. Procedural memory underpins the automation and generalization of task-oriented behaviors. 

**Working Memory** , a functional extension of _short-term memory_ , functions as a _dynamic control mechanism_ that not only temporarily stores information but also actively manipulates and updates it to support ongoing cognition [239, 294]. Its primary function is to actively select and integrate information from diverse sources, such as short-term context (e.g., dialogue history) and activated long-term memory (e.g., retrieved knowledge or parametric outputs) and transient computational buffers like the **Key–Value (KV) cache** [31, 255]. In practice, working memory acts as the control layer [168] for the agent context window, dynamically assembling the necessary inputs, including retrieved reasoning experience [225], tool outputs [192], and user data [281], to support complex reasoning, planning, and goal-directed behavior. 

# **2.4 Memory Operations** 

To enable dynamic memory beyond static storage, modern agents require operations that govern the lifecycle of information and support its effective use during interaction with the external environment. These operations can be grouped into three functional categories: Memory Encoding, Memory Evolving, and Memory Adapting. 

_2.4.1 Memory Encoding._ **Memory encoding** governs how information is transformed into storable representations 

and linked for later retrieval. It primarily involves two complementary processes: Consolidation and Indexing. These operations naturally incorporate the temporal nature of memory, where information evolves over time. 

**Consolidation** [258] refers to transforming _𝑚_ short-term experiences E[ _𝑡,𝑡_ + Δ _𝑡_ ] = ( _𝜖_ 1 _,𝜖_ 2 _, . . . ,𝜖𝑚_ ) between _𝑡_ and _𝑡_ + Δ _𝑡_ into persistent memory M _𝑡_ . It encodes interaction histories (e.g., dialogs, trajectories) into durable forms such as model parameters [301], graphs [372], or knowledge bases [190]. It is essential for continual learning [73], personalization [358], external Memory Bank construction [375], and knowledge graph construction [331]. 

**Indexing** [195] constructs auxiliary codes _𝜙_ such as entities, attributes, or content-based representations [314] that serve as access points to stored memory. Beyond access, indexing encodes temporal [196] and relational structures [200] across memories, enabling efficient and coherent retrieval through traversable index paths. It further supports scalable retrieval across symbolic, neural, and hybrid memory systems. 

_2.4.2 Memory Evolving._ **Memory evolving** describes how stored information dynamically changes over time through two complementary processes: _memory updating_ and _memory forgetting_ . 

**Updating** [136] reactivates existing memory representations in M _𝑡_ and temporarily modify them with new knowledge K _𝑡_ +Δ _𝑡_ . Updating parametric memory typically involves a locate-and-edit mechanism [70] that targets specific model components. Meanwhile, contextual memory updating involves summarization [375], pruning, or refinement [13] to reorganize or replace outdated content. Those updating operations support continual adaptation while maintaining 

7 

Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

memory consistency. 

**Forgetting** [49, 285] is the ability to selectively suppress memory content F from M _𝑡_ that may be outdated, irrelevant, or harmful. In parametric memory, it is commonly implemented through unlearning techniques [119, 157] that modify model parameters to erase specific knowledge. In contextual memory, forgetting involves time-based deletion [375] or semantic filtering [296] to discard content that is no longer relevant. These operations help maintain memory efficiency and reduce interference. 

However, these operations introduce inherent risks and limitations. Attackers can exploit vulnerabilities to alter or poison memory contents. Once corrupted, memory fragments may persist undetected and later trigger malicious actions. As discussed in Section 6, such threats call for robust approaches that address not only the memory operations but also the entire memory lifecycle. 

_2.4.3 Memory Adapting._ Memory adapting refers to how stored memory is retrieved and used during inference, encompassing two operations: retrieval and compression. 

**Retrieval** is the process of identifying and accessing relevant information from memory in response to inputs, aiming to support downstream tasks such as response generation, visual grounding, or intent prediction. Inputs Q can range from a simple query [65] to a complex multi-turn dialogue context [281], and from purely textual inputs to visual content [378] or even more modalities. Memory fragments are typically scored with a function _sim()_ with those above a threshold _𝜏_ deemed relevant. Retrieval targets include memory from multiple sources [268], modalities [281], or even parametric representations [193] within models. 

**Condensation** enables efficient context usage under limited context window by retaining salient information and discarding redundancies with a compression ratio _𝛼_ before feeding it into models. It can be broadly divided into pre-input compression and post-retrieval compression. Pre-input compression applies in long-context models without retrieval, where full-context inputs are scored, filtered, or summarized to fit within context constraints [41, 351]. Post-retrieval compression operates after memory access, reducing retrieved content either through contextual compression before model inference [325] or through parametric compression by integrating retrieved knowledge into model parameters [244]. Unlike memory consolidation, which summarizes information during memory construction [375], compression focuses on reducing memory at inference [149]. 

# **3 From Operations to Key Research Topics** 

This section analyzes how real-world systems manage and utilize memory through core operations. We examine four key research topics introduced in Section 1, guided by the framework in Figure 1, using the Relative Citation Index (RCI)—a time-adjusted metric that normalizes citation counts by publication age to highlight influential work. 

Du et al. 

8 

<!-- Start of picture text -->
Consolidation MyAgent [100], MemoChat [190], MemOS [168], LightMem [363]<br>Encoding<br>Indexing HippoRAG [84], G-Memory [356],LongMemEval [314], GraphCogent[294]<br>Updating Memory-R1 [333], O-Mem [290], NLI-transfer [13], RCSum [292], Mem- 𝛼 [303]<br>Evolving<br>Forgetting FLOW-RAG [296], MemoryBank [375]<br>Retrieval LoCoMo [196], MemoChat [190], MemGuide [64], MemTool [192]<br>Adapting Condensation MoT [160], SCM [282], Optimus-1 [169], A-MEM[329]<br>Generation MEMORAG [234], ReadAgent [149], COMEDY [32]<br>Adaptation PersonaMem-v2 [121], Mem-U [217], MALP [358], Per-Pcs [269]<br>Personalization<br>Augmentation EMG [309], LDAgent [153], PerLTQA [65]<br>Context Compression RECOMP [325], xRAG [36], LongLLMLingua [125], AgentFold [344]<br>Compression KV Cache Eviction H2O [368], StreamingLLM [323], SnapKV [163], RocketKV [19]<br>KV Cache Storing LESS [59], KVQuant [98], KIVI [188], ShadowKV [263]<br>Optimization<br>Context Retrieval GraphReader [92], Ziya-Reader [91],<br>Retrieval<br>KV Cache Selection QUEST [271], RetrievalAttention [174]<br>Locating then ROME [203], MEMIT [204], AlphaEdit[70], AnyEdit[122], M2Edit[380]<br>Editing<br>Meta Learning KE [50], MEND [211], DAFNET [365], MALMEN[267]<br>Editing<br>Prompt IKE [373], MeLLo [376], EditCoT [283], DR-IKE[214], LTE[128]<br>Additional Parameters CaliNET [60] , SERAC [212], Titans [20] , MLP-Memory [312]<br>Locating then DEPN [317], MemFlex [277], WAGLE [119], NeuMuter[99]<br>Unlearning<br>Training Objective FLAT [304], GA+Mismatch [343], SOUL [120], Relearn [326], UL[115]<br>Unlearning<br>Prompt ICUL[230], ECO[173], SEPS[117], ReversingIKE[349], ERASE[213]<br>Additional Parameters ULD[118], EUL[30], LoKU[26], LLMEraser[55], S3T[38]<br>Regularization-based Learning TaSL [73], SELF-PARAM [302]<br>Lifelong<br>(Continual) Replay-Based Learning DSI++ [200], Memento [377], Reasoning Bank [225]<br>Learning<br>Interactive Learning LSCS [301], ACE [361], Early Experience [357]<br>Reasoning Mirix [298], StructRAG [165], ChatDB [102]<br>Cross-Textual<br>Integration<br>Conflict RKC-LLM [299], BGC-KC [268]<br>Multi-modal Fusion LifelongMemory [305], Ma-llm[90],  𝑀 3 [189]<br>Coordination<br>Retrieval VISTA [378], IGSR [281], MMLongBench [311]<br>TermLong<br>ContextLong<br>Memory in AI Agent<br>MotificationParametric<br>Multi-source<br><!-- End of picture text -->

Fig. 2. Operation-driven key research topics in AI agents, mapping core memory operations to four key research topics. 

RCI surfaces emerging trends and enduring contributions across memory research. Figure 2 shows the architectural landscape of these topics. 

# **3.1 Long-term Memory** 

Long-term memory, as a research topic, examines how agents preserve and leverage information across extended interactions to achieve continuity, personalization, and cumulative learning. In this section, we discuss contextual 

Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

9 

long-term memory as a functional system that integrates both structured and unstructured forms, highlighting its core operations of encoding, evolving, and adapting in supporting complex reasoning and temporal coherence. 

_3.1.1 Memory Encoding._ Memory Encoding is the foundational process of transforming raw inputs —such as dialogue histories or agent observations—into durable representations suitable for long-term storage. This process is realized through two critical and complementary operations: Memory Consolidation and Memory Indexing. 

**_Memory Consolidation_** plays a central role in shaping long-term memory by stabilizing short-term context into enduring representations. In LLM-based agents, consolidation unfolds across multiple levels: (1) _dialogue summarization or structuring_ converts interaction histories into retrievable traces [100, 190, 293, 375]; (2) _reasoning experience consolidation_ encodes successful tool-use trajectories and problem-solving strategies [71, 225]; (3) _parametric consolidation_ embeds stable knowledge directly into model parameters through methods such as continual pretraining [126], supervised finetuning [39], or reinforcement learning [303, 333]; (4) _event-level consolidation_ organizes episodic information into structured event graphs [372]; (5) _knowledge-level consolidation_ populates knowledge graphs with factual triples for symbolic reasoning [239]. Collectively, these processes extend the agent’s temporal memory horizon, enabling the persistent retention of contextual, episodic, and semantic memory across extended interaction with the external environment. Nevertheless, robust long-term consolidation remains challenging-requiring the balance between stability and adaptability, mitigating context loss from over-compression, and preserving relevance under continuous updates [361]. This highlights the critical need for dynamic consolidation strategies within complex, evolving memory systems. 

**_Memory Indexing_** provides the foundational structure for long-term memory, transforming vast collections of experiences into a searchable repository that enables efficient and accurate retrieval. Recent work categorizes memory indexing into three paradigms: graph-based indexing, exemplified by HippoRAG [84], constructs lightweight knowledge graphs to explicitly map the relational structure between memory fragments; signal-enhanced indexing, where systems like LongMemEval [314] enrich memory keys with metadata such as timestamps or summaries to refine retrieval accuracy; and timeline-based indexing, as demonstrated in Theanine [222], which organizes memories along temporal and causal chains to enable chronologically-informed retrieval. These strategies highlight the need to integrate structure, retrieval signals, and temporal dynamics for effective long-term memory management. These paradigms signal a shift from simple semantic similarity to a crucial synthesis of relational structure, metadata signals, and temporal dynamics, enabling the development of scalable and contextually aware memory systems. 

_3.1.2 Memory Evolving._ Memory Evolving involves operations such as forgetting and updating. Here, memory is dynamically refined through the incorporation of new knowledge, the correction of outdated or erroneous content, and the selective removal of low-value information. These processes ensure that the memory remains accurate, efficient, and contextually relevant, enabling agents to adapt to evolving tasks and environments. 

**_Memory Updating_** is the dynamic process of maintaining the internal consistency and accuracy of long-term memory by continually creating new representations [32], integrating them with existing knowledge, and pruning outdated or irrelevant information [13]. Recent research are broadly categorized as either intrinsic or extrinsic. _Intrinsic Updating_ operates through self-contained processes to refine its knowledge base: selective editing [13] improves memory by selectively deleting outdated information; recursive summarization [292] compresses dialogue histories through iterative summarization; memory blending merges past and present representations to form evolved insights [139]; and self-reflective evolving enhances factual consistency by verifying memories against retrieved evidence [262]. _Extrinsic Updating_ relies on external signals, such as incorporating direct user corrections into memory to enable 

Du et al. 

10 

Fig. 3. Publication statistic of highlighted papers (RCI > 1) discussed in long-term memory. 

**_Memory Forgetting_** involves the removal of previously consolidated long-term memory representations. Distinct from the passive decay studied in cognitive psychology, forgetting in LLM agents is an active, targeted "unlearning" of consolidated information, driven by the need to expunge sensitive, harmful, or private content to meet external constraints [32, 212]. Consequently, developing robust unlearning capabilities for safety, privacy, and compliance has become a critical research focus [69, 118, 157, 185, 187]. The foremost challenge is to achieve precise and complete removal of targeted data without causing collateral damage to the integrity and performance of the remaining valid knowledge. 

continual system improvement [45]. Ultimately, the success of any memory update hinges on its ability to integrate new information without corrupting critical prior knowledge or violating the factual and stylistic consistency. 

_3.1.3 Memory Adapting._ Memory adapting focuses on retrieving and condensing relevant information from stored long-term memory to support reasoning, decision-making, and generation. It bridges the gap between the vast, passive repository of stored knowledge and the immediate context required for effective reasoning and generation. **Memory Retrieval** selects relevant information, while **Memory Condensation** transforms that information into a structured, compact context for the model to use. The ultimate success of these operations is measured by their ability to support the final stage of **Memory Grounded Generation** . 

**_Memory Retrieval_** focuses on selecting the most relevant memory entries for a given query. Retrieval methods can be categorized into three primary paradigms: (1) _query-centered retrieval_ , which refines the query itself for better search accuracy, as seen in FLARE [129] and IterCQR [116]; (2) _memory-centered retrieval_ , which improves the organization and ranking of stored information through enhanced indexing [314] or reranking [65]; and (3) _event-centered retrieval_ , which leverages temporal and causal structures for context-aware selection, as explored in LoCoMo [196] and MSC [327]. While techniques like multi-hop graph traversal further enrich this process [84], the core challenge remains in developing adaptive retrieval strategies that can dynamically adjust to the evolving structure and relevance of the memory store itself. 

**_Memory Condensation_** is the inference-time process of transforming raw, retrieved long-term memories into a structured and compact context for the LLM. Integration may span multiple memory sources (e.g., long-term dialogue histories, external knowledge bases) and modalities (e.g., text, images, or videos), enabling richer and contextually grounded generation. Recent efforts on memory integration can be broadly categorized into two strategies. **Static contextual integration** approaches, such as EWE [31] and Optimus-1 [169], focus on retrieving and combining static memory entries at inference time to enrich context and improve reasoning consistency. In contrast, **dynamic memory evolving** approaches, exemplified by A-MEM [100], Synapse [374], R2I [247], and SCM [282], emphasize enabling memory to grow, adapt, and restructure over the course of interactions, either through dynamic linking or controlled memory updates. While static integration strengthens immediate contextual grounding, recent work has transformed condensation into a more agentic paradigm, Agentic Context Engineering (ACE) [361], in which an autonomous agent proactively refines, prioritizes, and restructures retrieved contexts to maximize reasoning efficiency. This agent-driven evolution of memory condensation represents a crucial step toward building adaptive, self-improving, and lifelong learning agents. 

Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

11 

**_Memory Grounded Generation_** can be broadly categorized into three types based on how memory influences generation. _Self-Reflective Reasoning_ uses memory of prior thinking processes to guide guide intermediate reasoning steps, such as MoT [160] and StructRAG [165]. _Feedback-Guided Correction_ leverages knowledge of past errors or user feedback to constrain decoding and prevent their repetition [234, 270]; _Contextually-Aligned Long-Term Generation_ integrates summaries of distant history to maintain coherence throughout long dialogues or documents [32, 190]. The primary challenge across all these methods is mitigating the impact of noise or inaccuracies from the earlier retrieval operations, ensuring the final output is both reliable and factually grounded. 

_3.1.4 Personalization._ Personalization is key but challenging for long-term memory, limited by data sparsity, privacy, and changing user preferences. Current methods can be broadly categorized into two lines: model-level adaptation and external memory augmentation. 

**_Model-Level Adaptation_** encodes user preferences into model parameters via fine-tuning or lightweight updates. One strategy involves embedding user traits into a latent space, where methods like CLV use contrastive learning to cluster persona representations that guide generation [272]. A more prevalent strategy employs parameter-efficient techniques; for instance, RECAP injects user histories via a prefix encoder [182], while Per-Pes assembles modular adapters that reflect user behaviors [269]. In specialized domains, MaLP [358] introduces a dual-process memory for modeling short- and long-term personalization in medical dialogues. The central challenge for this paradigm is managing the personalization-generalization trade-off: effectively specializing the model to an individual without compromising its broad, pre-trained capabilities. 

**_External Memory Augmentation_** personalizes responses by retrieving user-specific information from an external repository at inference time. This approach varies by memory format: structured memories like user profiles or knowledge graphs are used to create personalized prompts in LaMP [246]; unstructured memories, such as dialogue histories, provide rich contextual data for alignment in systems like LAPDOG [105]; and hybrid systems like SiliconFriend [375] maintain persistent, cross-session memory stores. While these approaches scale well, they often treat long-term memory as a passive buffer, leaving its potential for proactive planning and decision-making largely untapped. 

_3.1.5 Discussion._ **Long-term memory evaluation remains constrained by static assumptions.** Current bench- 

marks mainly follow two paradigms: knowledge-based question answering (QA) and multi-turn dialogue. QA tasks test a model’s ability to retrieve and reason over factual knowledge, leveraging both parametric memory [21, 51, 336] and unstructured contextual memory [132, 245]. Techniques like self-evolution alignment [364] and salient memory distillation [147, 190] enhance factual grounding. However, these benchmarks often assume static memory and overlook dynamic operations such as updating, selective retention, and temporal continuity [196, 314]. In contrast, multi-turn dialogue benchmarks (e.g., LoCoMo [196], LongMemEval [314]) better capture real-world memory use by spanning 20–30 turns and enabling analyses of cross-session retrieval, updating, and event reasoning. Yet most still treat dialogue history as static context, focusing narrowly on QA accuracy while neglecting operations like indexing, consolidation, forgetting, and user adaptation. This static lens limits understanding of how memory evolves over time, especially in interactive settings requiring temporal adaptation. Recent work has begun addressing these challenges through agent-based systems [329] that integrate long-term memory into multi-turn planning and generation. 

_Mismatch between memory retrieval and memory-grounded generation reveals context engineering bottlenecks._ We analyze retrieval–generation performance gaps reported in recent studies [84, 196, 314, 375]. As shown in Figure 4, state-of-the-art models achieve Recall@5 above 90 on 2Wiki and MemoryBank [84, 375], yet generation metrics (e.g., 

Du et al. 

12 

Fig. 4. Benchmark for evaluating **long-term memory** . “Mo” denotes modality. “Ops” denotes operability. “DS Type” indicates dataset type (QA – question answering, MS – multi-session dialogue). “Per” and “TR” indicate whether persona and temporal reasoning are present. 

F1) lag by over 30 points. This indicates that high retrievability does not guarantee effective generation. Several factors contribute: compact memory formats (e.g., dialogue turns or task-level observations) better support generation than verbose entries; longer temporal distance between memory and query, as in MemInsight on LoCoMo [245], degrades generation even with accurate retrieval, highlighting temporal reasoning as a key bottleneck in memory-grounded generation. Recent efforts such as TREMU [78] attempt to address this via chain-of-thought supervision, yet empirical gains remain limited, further suggesting that long-horizon agents will increasingly encounter this constraint; retrieving more items introduces noise that impairs decoding; and multilingual settings reveal a persistent language gap, with English outperforming Chinese. These findings show that while current systems retrieve relevant memories, they remain limited in structuring and leveraging them for downstream generation. 

_Memory operations remain under-evaluated in current benchmarks._ Despite growing interest in memory-augmented models, current evaluations primarily focus on retrieval accuracy (e.g., Recall@k, Hit@k, NDCG) and post-retrieval generation quality (e.g., F1, BLEU, ROUGE-L), as seen in LoCoMo and LongMemEval. While some studies incorporate human assessments of memorability, coherence, and correctness, these efforts largely overlook procedural aspects of memory use—such as consolidation, updating, forgetting, and selective retention. Some recent efforts, such as MemoryBank and ChMapData-test [313], begin to address aspects of memory updating and long-term planning, but remain isolated and narrow in scope. There remains a pressing need for comprehensive benchmarks that span parametric, contextual unstructured, and structured memory, along with dynamic evaluation protocols that assess memory reliability, temporal reasoning, and multi-session dialogue consistency beyond static QA accuracy. 

Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

13 

Fig. 5. Publication statistic of highlighted papers (RCI > 1) discussed in long-term memory. 

Fig. 6. Compression based method performance vs. compression rate on LongBench [15]. Data borrowed from Yuan et al. [353]. 

_Publication Trend._ As shown in Figure 3, retrieval and generation dominate recent literature, especially in NLP. Core operations like consolidation and indexing receive more attention in ML, while forgetting remains underexplored. Personalization is largely limited to NLP due to practical application needs. In terms of citation impact, consolidation, retrieval, and integration play key roles—driven by advances in memory-aware fine-tuning, summarization, retrievalaugmented generation, and prompt fusion. 

|**Shift evaluation from isolated memory operations toward systematic assessment of memory encoding, evolving,**<br>**and adapting.**|
|---|
|**Effective methods for long-horizon temporal reasoning beyond dialogue are still lacking.**|
|**Addressing the retrieval–generation disconnect requires context engineering strategies that prioritize concise,**|
|**reliable memory condensation.**|
|**Advance personalized agents by moving beyond memory storage toward adaptive reuse and personalization of**|
|**session-spanning memories.**|

# **3.2 Long-context Memory** 

Managing vast quantities of multi-sourced external memory (short-term memory) in conversational search presents significant challenges in long-context language understanding. While advancements in model design and long-context training have enabled LLMs to process millions of input tokens [56, 58], effectively managing memory within such extensive contexts remains a complex issue. These challenges can be broadly categorized into two main aspects with respect to memory operations: 1) **Memory Compression** , which focuses on compressing the short-term memory of the context tokens or KV cache to enable efficient long context decoding and **Memory Retrieval** optimizes the selection of contextual memory for effective long context processing. In this section, we systematically review efforts made in handling these challenges. 

_3.2.1 Memory Compression._ To manage extensive amounts of multi-sourced external memory, LLMs must be optimized to efficiently process lengthy contexts. In this section, we discuss approaches for efficiently processing long-context 

Du et al. 

14 

short-term memory, which focuses on memory compression. Specifically, we discuss both memory operations of context tokens (e.g., documents, dialogue histories), and memory operations of KV cache (i.e., working memory). 

**_Context Compression_** utilizes memory compression operations to optimize contextual memory utilization, which generally involves two major approaches: soft prompt compression and hard prompt compression [167]. Soft prompt compression focuses on compressing chunks of input tokens into the continuous vectors in the inference stage (e.g., AutoCompressors [37], xRAG [36], CEPE [345]), or encoding task-specific long context (e.g., database schema) to parametric memory of finetuned models in the training stage (e.g., YORO [142]), to reduce the input sequence length. 

While hard prompt compression directly compresses long input chunks into shorter natural language chunks. Eviction based methods selectively prune uninformative tokens (e.g., Selective Context [162], Adaptively Sparse Attention [7], HOMER [257]) or chunks (e.g., Semantic Compression [72]) from the context to shorten the input. Summarization based methods (e.g., RECOMP [325], CompAct [347], Nano-Capsulator [40], LLMLingua series [124, 125, 227]) in contrast compress long inputs by abstracting the key information. Hybrid methods (e.g., TCRA-LLM [176]) combine the features of evicting uninformative tokens and abstracting context chunks to empower context compression. With both soft prompts and hard prompts, LLMs are allowed to more effectively utilize the context via memory compression. 

Beyond static compression, RL-based Active Management has recently emerged, treating context utilization as a dynamic decision-making process. Methods such as AgentFold [344] and FoldGRPO [264] utilize Reinforcement Learning from Verifiable Rewards (RLVR) to train LLM agents to actively manage and compress long-context information during task execution. Unlike traditional summarization or pruning, these approaches allow the agent to learn an optimal policy for memory retention by optimizing against task-specific rewards. By transitioning from static soft and hard compression to RL-driven active management, LLMs can move beyond simple token reduction toward task-aware memory optimization for long-context memory processing. 

**_KV Cache Eviction._** In long-context processing, KV cache (working memory) aims to minimize unnecessary keyvalue computations by storing past key-value pairs as external parametric memory. However, as context length increases, the memory requirement for storing these memory grows quadratically, making it infeasible for handling extremely long contexts. KV Cache Eviction aims to reduce cache size by eliminating unnecessary KV cache. Static eviction approaches select unnecessary cache with fixed pattern. For instance, StreamingLLM [323] and LM-Infinite [86] use an Λ-shaped sparse pattern, LCKV [315] only retain the KV cache from top layer, while LaCache [251] use a ladder-shaped eviction pattern to retain long-range dependency. In contrast, dynamic eviction approaches are more flexible, which decide the KV cache to be eliminated with respect to the query (e.g., H2O [368], FastGen [77], Keyformer [2], Radar [88], NACL [35]), or the model behavior (attention weight) during inference (e.g., SnapKV [163], HeadKV [76], Scissorhands [184], PyramidInfer [334], L2 Norm [53], SirLLM [342], D-LLM [127], CateKV [123], RocketKV [19]). Considering the risk of potential information loss when discarding KV cache, merging based approaches (e.g., MiniCache [172], InfiniPot [138], CHAI [3]) merge similar KV cache or storing KV cache with special tokens (Activation Beacon [360]) instead of directly discarding to reduce information loss. 

**_KV Cache Storing Optimization._** In another way of conducting compressing KV cache, KV Cache Storing Optimization considers the potential information loss when removing less important elements, and focus on how to preserve the entire KV cache at a smaller footprint. For instance, LESS [59], Eigen [249] and ShadowKV [263] compress KV cache entries into low-rank representations, while FlexGen [250], Atom [371], KVQuant [98], ZipCache [93], KIVI [188] dynamically quantize KV cache to reduce memory allocation. More recently, dynamic methods (e.g., Kelle [322]) propose software-hardware co-design solution to reduce the cost of storing KV cache. These approaches provide less performance drop compared with KV cache eviction methods but remain limited due to the quadratic nature of 

15 

Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

the growing memory. Future works should continue focusing on the trade-off between less memory cost and less performance drop. 

_3.2.2 Memory Retrieval._ Apart from compressing contextual memory to reduce the load for processing long context, optimizing memory retrieval from long-context raises another important challenge, for effectively identity key information from the noisy context. Considering the type of contextual memory, these efforts can be summarized as contextual retrieval and KV cache selection. 

**_Context Retrieval_** aims to enhance LLM’s ability in identifying and locating key information from the contextual memory. Graph-based approaches such as CGSN [219] and GraphReader [158] decompose documents into graph structures for effective context selection. Token-level context selection approaches (e.g., TRAMS [351], Selection-p [41], PASTA [362]) pruning and (or) selecting tokens deemed most important. In contrast, methods such as NBCE [259], FragRel [354], and Sparse RAG [382] perform context selection at the fragment level, choosing the relevant context fragments based on their importance to the specific task. Furthermore, training-based approaches as Ziya-Reader [91] and FILM [6] train LLMs with specialized data to help improve their context selection ability. Other methods like MemGPT [226], Neurocache [244] and AWESOME [24] preserve an external vector memory cache to effectively store and retrieve first encode external memory into vector space, and this external vector memory can be effectively updated or retrieved to enable long-term memory utilization. Together with these methods, LLMs are allowed to better identify key information in the context via memory retrieval. 

**_KV Cache Selection_** selectively loads essential KV caches to accelerate inference, focusing on efficient memory retrieval. QUEST [271], TokenSelect [316], and Selective Attention [151] apply query-aware KV cache selection to identify critical caches for faster inference. Similarly, RetrievalAttention [174] employs Approximate Nearest Neighbor (ANN) search to locate important caches. By storing KV caches externally and retrieving them during inference, Memorizing Transformers [318], LongLLaMA [280], ReKV [54], and ArkVale [33] efficiently process long contexts. These methods provide flexibility by avoiding KV cache eviction and integrating with storage optimization techniques (e.g., Tang et al. [271] shows QUEST is compatible with Atom [371]). 

_3.2.3 Discussion._ 

_Lost in the Context._ Despite claims that context length can extend to millions of tokens, long-context LLMs have been found to miss crucial information in the middle of the context during tasks such as question answering and key-value retrieval [179, 241]. This “lost in the middle” issue is especially critical when managing vast amounts of external memory, as essential information may be located at various positions within the long context. Such limitations also extend to the multimodal contexts; as demonstrated in MMLongBench [311], Long-Context Vision Language Models (LCVLMs) exhibit a similar “lost-in-the-middle” phenomenon when processing lengthy interleaved text-image documents. In addition, in more complex scenarios requiring reasoning based on contextual memory, LLMs also fail to effectively aggregate memory across different part of the context [106]. Furthermore, though higher recall can be obtained with larger retrieval set, irrelevant information will mislead LLMs and harm the generation quality [131, 252]. Effective contextual utilization become a key challenge in addressing these limitations, encompassing context retrieval and context compression across memory operations. 

_Trade-off between compression rate and performance drop._ Compression, as one of the major memory operations involved in long context memory, is widely used in compressing both parametric memory (KV cache) and contextual memory (Context), to balance the efficiency (compression rate) and effectiveness (performance drop). Different 

Du et al. 

16 

compression-based strategies have their own pros and cons. For example, KV cache eviction methods typically achieve higher compression rates but result in greater information loss and, consequently, a more significant performance drop. Yuan et al. [353] propose an universal benchmarking on these different strategies, qualitatively showcase the pros and cons according to different strategies. As illustrated in Figure 6, generally, KV cache storage optimization methods (with ’x’ marker) achieves best trade-off between effectiveness and efficiency. In contrast, KV cache eviction methods (with ∇ marker) are more flexible, with fully customization compression rate, but less effective. In the other hand, compressing the contextual memory (with Δ marker) are less effective compared with compressing the parametric memory, as evidenced by the comparatively poor performance of LLMLingua2. 

_Publication Trending._ Figure 5 summarizes publication trends on long context. The NLP community focuses more on utilization with contextual memory, while the ML community dedicates more effort to efficiency via parametric memory. From an RCI perspective, KV cache storage optimization dominates discussions on long context topics. This dominance is not only for balancing efficiency and effectiveness, but also due to its compatibility with other long context methods. Comparing the two memory operation, retrieval methods generally get less attention. One reason for this is the overlap between context retrieval and other topics, such as long-term memory and multi-source memory, which leads to context retrieval being somewhat underestimated in Figure 5. Additionally, understanding the relationship between RAG and long-context [131, 166] is crucial for the development of memory-based LLM agent. However, impactful work on contextual utilization in complex environments is still lacking. Addressing this gap is a valuable future direction. 

|**Balancing the trade-off between reduced memory usage and minimized performance degradation in KV cache**<br>**optimization represents an exciting area for future research.**|
|---|
|**Contextual utilization with complex environment (e.g., multi-source memory) is a pivotal research direction for**|
|**advancing the development of intelligent agents.**|

# **3.3 Parametric Memory Modification** 

Modifying parametric memory, which is encoded knowledge within the LLM parameters, is crucial for dynamically adapting stored memory. Methods for parametric memory modification can be broadly categorized into three types: (1) **Editing** is the localized modification of model parameters without requiring full model retraining; (2) **Unlearning** selectively removes unwanted or sensitive information; and (3) **Continual Learning** incrementally incorporates new knowledge while mitigating catastrophic forgetting. This section systematically reviews recent research in these categories, with detailed analyses and comparisons presented in subsequent subsections. 

_3.3.1 Editing._ Parametric memory editing updates specific knowledge stored in the parametric memory without full retraining. One prominent line of work involves directly modifying model weights. A dominant strategy is locatingthen-editing method [52, 70, 83, 107, 201, 203, 205], which uses attribution or tracing to find where facts are stored, then modifies the identified memory directly. Another approach is meta-learning [50, 83, 159, 211, 267, 365], where an editor network learns to predict targeted weight changes for quick and robust corrections. Some methods avoid altering the original weights altogether. Prompt-based methods [373, 376] use crafted prompts like ICL to steer outputs indirectly. Additional-parameter methods [48, 60, 212, 289, 300] add external parametric memory modules to adjust behavior without touching model weights. These approaches vary in efficiency and scalability, though most focus on entity-level edits. 

Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

17 

_3.3.2 Unlearning._ Parametric memory unlearning enables selective forgetting by removing specific memory while retaining unrelated memory. Recent work explores several strategies. Additional-parameter methods add components such as logit difference modules [118] or unlearning layers [30] to adjust memory without retraining the whole model. Prompt-based methods manipulate inputs [173] or use ICL [231] to externally trigger forgetting. Locatingthen-unlearning methods [119, 277, 317] first identify responsible parametric memory, then apply targeted updates or deactivations. Training objective-based methods [120, 185, 304, 343] modify the training loss functions or optimization strategies explicitly to encourage memory forgetting. These approaches aim to erase memory when given explicit forgetting targets, while preserving non-targeted knowledge and balancing efficiency and precision. 

_3.3.3 Continual Learning._ Continual learning [287] enables long-term memory persistence by mitigating catastrophic forgetting in model parameters. Two main approaches are regularization-based and replay-based methods. Regularization constrains updates to important weights, preserving vital parametric memory; methods like TaSL [73], SELF-PARAM [302], EWC [141], and POCL [319] apply such constraints to embed knowledge without replay. In contrast, replay-based methods reinforce memory by reintroducing past samples, particularly suited to incorporating retrieved external knowledge or historical experiences during training. For example, DSI++ [200] leverages generative memory to supplement learning with pseudo queries, maintaining retrieval performance without full retraining. Beyond these paradigms, agent-based work such as LifeSpan Cognitive System (LSCS) [301] extends continual learning into an interactive setting, enabling agents to incrementally acquire and consolidate memory through real-time experience. LSCS provides valuable insights into how external memory can be encoded into model parameters continually. 

_3.3.4 Discussion._ 

_SOTA Solution Analysis._ We select recent SOTA methods across different categories and report their performance in Figure 10 on the most widely used datasets for memory editing (CounterFact [203] and ZsRE [152]) and memory unlearning (ToFU [197]). We aim to ensure a fair comparison by using consistent base models and appropriate evaluation metrics. Specifically, for CounterFact and ZsRE, we follow Meng et al. [203], where 2,000 samples are randomly selected from the dataset for updates, with 100 samples per edit. All methods on CounterFact use GPT-J as the base model; for ZsRE, most use GPT-2, except MELO, which uses T5-small. For the ToFU benchmark, all methods use LLaMA2-7B-chat under the 10% forgetting setting. Prompt-based methods achieve strong overall performance across all benchmarks, while meta-learning methods generally underperform compared to others. We observe that the same methods tend to perform worse on ZsRE than on CounterFact. This drop is primarily due to significantly lower specificity scores on ZsRE, which in turn lowers the overall score. This highlights the challenge of achieving precise, targeted edits and suggests that improving specificity remains a promising research direction. Additionally, we find that most current SOTA methods achieve high scores on the ToFU benchmark, suggesting it may be insufficiently challenging and that new unlearning benchmarks are needed. 

_Scaling Challenges._ Figure 8 shows the maximum number of sequential edits supported by different methods. Except for MemoryLLM, which supports up to 650k updates, most methods only test 1,000 to 5,000 edits. We also note that research on sequential unlearning remains sparse and presents an open area for future exploration. Figure 9 illustrates the distribution of model sizes used across different methods. In both editing and unlearning, non-prompt-based methods are typically applied to medium or small models (≤ 20B). In contrast, prompt-based approaches are more commonly evaluated on larger models, likely due to their reliance on stronger instruction-following and in-context learning capabilities. Non-prompt methods, on the other hand, often face scalability challenges due to higher computational 

Du et al. 

18 

Fig. 7. Publication statistic of highlighted papers (RCI > 1) discussed in this section. 

Fig. 8. Maximum sequential edits supported by different model editing methods 

Fig. 9. Model size distribution in memory editing and unlearning. 

Fig. 10. SOTA solutions across different categories on the CounterFact (editing), ZsRE (editing) and TOFU (unlearning) benchmark. 

costs, making them difficult to apply to large models. This highlights the need to further investigate how to balance model size with editing or unlearning effectiveness and efficiency. 

_Publication Trending._ Figure 7 presents publication statistics of papers with RCI > 1 across editing, unlearning, and lifelong learning. Editing has attracted the most attention, especially locating-then-editing and additional-parameter methods. NLP venues focus more on editing, while ML work is more evenly distributed across the three areas. Locatingthen-editing also shows the highest RCI variance, reflecting several highly influential studies. Although unlearning is less represented, it demonstrates strong potential in objective- and parameter-based categories. Lifelong learning, by contrast, remains relatively underexplored. 

**Current editing methods often lack specificity, while unlearning benchmarks like TOFU may be too simple to reveal real limitations.** 

**Agents should leverage continual learning to self-evolve through sustained interaction with the environment, without overwriting stable parametric memory.** 

Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

19 

Fig. 11. Publication statistic of highlighted papers (RCI > 1) discussed in multi-source memory. 

Fig. 12. Trends in cross-textual reasoning: memory sources and reasoning strategies. 

# **3.4 Multi-source Memory** 

Multi-source memory is essential for real-world AI deployment, where systems must reason over internal parameters and external knowledge bases spanning structured data (e.g., knowledge graphs, tables) and unstructured multi-modal content (e.g., text, audio, images, videos). This section examines key challenges across two dimensions: cross-textual integration and multi-modal coordination. 

_3.4.1 Cross-textual Integration._ Cross-textual integration enables an AI agent to perform deeper reasoning and resolve conflicts from multiple textual sources to support more contextually grounded responses. 

**_Reasoning_** focuses on integrating multi-format memory to generate factually and semantically consistent responses. One line of research investigates reasoning over memories from different domains, particularly through the precise manipulation of structured symbolic memories, as demonstrated by ChatDB [102] and Neurosymbolic [295]. Other works [220, 320] explore the dynamic integration of domain-specific parameterized memories to enable more flexible reasoning. Multi-source reasoning across diverse document sources has also been studied, as seen in DelTA [306] and dynamic-MT [63]. Additionally, several studies [148, 165, 331, 369] have investigated heterogeneous knowledge integration by retrieving information from both structured and unstructured sources. While these efforts have made substantial progress in combining parameterized and external memories for reasoning, achieving unified reasoning over heterogeneous, multi-source memories remains a major open challenge. In particular, more work is needed to effectively integrate parameterized memories with both structured and unstructured external knowledge sources. 

**_Conflict_** in multi-source memory refers to factual or semantic inconsistencies that arise during the retrieval and reasoning over heterogeneous memory representations. These conflicts often emerge when integrating parametric and contextual memories, or combining structured and unstructured knowledge such as triples, tables, and free text [328]. Prior work has focused on identifying and localizing such inconsistencies. For example, RKC-LLM [299] proposes an evaluation framework to assess models’ ability to detect contextual contradictions, while BGC-KC [268] highlights models’ tendency to favor internal knowledge over retrieved content, motivating source attribution and trust calibration. These methods offer important foundations for memory conflict understanding, though many remain limited to static scenarios or single-source reasoning. 

_3.4.2 Multi-Modal Coordination._ As memory-augmented systems evolve toward multi-modal settings, a key challenge lies in fusion and retrieval over heterogeneous modalities such as text, image, audio, and video. 

Du et al. 

20 

Fig. 13. Evolution of memory operation support across Years. 

Fig. 14. Analysis of temporal modeling, fusion strategies, and retrieval methods in multi-modal coordination. 

**_Fusion_** refers to aligning the retrieved information across diverse modalities. From a memory perspective, fusion serves as a key mechanism for integrating cross-modal information over time. Existing approaches can be broadly divided into two lines. The first focuses on **unified semantic projection** , where models such as UniTransSeR [194], MultiInstruct [332], PaLM-E [62], and NExT-Chat [355] embed heterogeneous inputs into a shared representation space for reuse and query. The second line emphasizes long-term cross-modal memory integration. For example, LifelongMemory [305] introduces a transformer with persistent memory to accumulate visual-textual knowledge across patient records. Similarly, MA-LMM [90] maintains a multimodal memory bank to extend temporal understanding in long videos. While effective at aligning modalities, current fusion methods often fall short in supporting long-term multimodal memory management. Key challenges include dynamic memory updates and maintaining consistency across heterogeneous sources. 

**_Retrieval_** in multi-modal systems enables access to stored knowledge across modalities such as text, image, and video. Most existing methods rely on embedding-based similarity computation, grounded in vision-language models like QwenVL [14], CLIP [237] or other multi-modal models [164]. These models project heterogeneous inputs into a shared semantic space, allowing for cross-modal retrieval. For instance, VISTA [378] enhances retrieval via visual token representations, while UniVL-DR [186] integrates video and language through a unified dual encoder. More recently, IGSR [281] extends retrieval to multi-session conversations by introducing intent-aware sticker retrieval, yet it still remains anchored in similarity-based retrieval. The limitations of such approaches are underscored by MMLongBench [311], which reveals that even state-of-the-art Large Vision-Language Models (LVLMs) struggle with cross-modality retrieval. Consequently, these methods often lack the capacity for reasoning-driven retrieval and neglect critical modalities like audio and sensorimotor signals required for embodied interaction. To bridge these gaps, M3 [189] introduces a Multi-modal Memory Modelling framework for open-ended agents that unifies storage and reasoning across diverse data types, including audio and sensorimotor signals. By enabling dynamic updates and reasoning-driven retrieval, M3 moves beyond shallow alignment to ensure robust long-term memory management. 

# _3.4.3 Discussion._ 

_Trends in Multi-Source Memory Integration._ Recent studies [256, 281] reveal a steady evolution in how multi-source memory is organized, retrieved, and reasoned over. While diverse methods have been proposed for **cross-textual integration** and **multi-modal coordination** , a closer look at representative models (Figures 12, 13, 14) highlights shared challenges and emerging trends. These developments reflect a broader shift from static retrieval pipelines toward 

21 

Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

dynamic, context-sensitive memory systems capable of supporting temporally grounded, cross-source reasoning across tasks and sessions. 

**Cross-textual integration** involves two key design axes: source type and reasoning mechanism. Early models such as ChatDB [102] and EMAT [320] use symbolic memory (e.g., databases, tables) accessed via explicit queries, offering transparency but limited scalability in open-domain settings. More recent systems like StructRAG [165], DelTA [306], and Chain-of-Knowledge [161] adopt unstructured memory and neural retrieval, combining attention-based fusion with chain-of-thought reasoning. Yet, most still treat memory as static, disconnected from real-time inference. Newer models such as MATTER [148], GoG [331], and ZCoT [208] move toward inference-aware memory, using retrieval-generation loops and collaborative agents to evolve memory dynamically. Despite this shift, resolving conflicts across heterogeneous sources remains a major challenge. Retrieved and parametric content are often merged without consistency checks or source attribution, leading to hallucinations and factual drift [268, 379]. Preliminary solutions such as multi-step conflict resolution [299] and epistemic calibration [328] are promising but lack scalability. Future work should pursue integrated, conflict-aware memory systems capable of dynamic reasoning under uncertainty and source ambiguity. 

**Multi-modal memory coordination** has advanced across three key dimensions: fusion, retrieval, and temporal modeling. As shown in Figure 14, common strategies include joint embedding [90, 194, 281, 311, 378] and prompt-level fusion [82, 305], while recent methods such as identifier-based memory [164] and cross-modal graph fusion [218] enable more selective, task-adaptive integration. Retrieval has evolved from static similarity toward temporally contextualized approaches, including temporal graphs and time-aware attention [324], facilitating reasoning over extended interactions. Notably, 60% of surveyed models encode temporal information, underscoring the importance of time in long-horizon tasks. Beyond retrieval and fusion, operational control—such as memory updating, indexing, and compression—is becoming increasingly essential. While earlier systems (2022–2023) mainly focused on retrieval, newer agents like E-Agent [80] and WorldMem [324] adopt self-maintaining architectures that continuously refine memory content over time. For example, WorldMem compresses multi-modal logs, while E-Agent dynamically updates internal memory to support long-horizon planning. These systems highlight a shift from passive memory querying to active, operationally rich architectures. 

_Publication Trend._ As shown in Figure 11, cross-textual reasoning dominates publication volume, reflecting its foundational role in multi-source integration. Fusion research, particularly work driven by CLIP [237], demonstrates the highest citation impact and influence on multi-modal learning. In contrast, dynamic retrieval and conflict resolution remain underexplored. Together, these trends suggest a field transitioning from surface-level integration toward deeper, operation-aware, and temporally structured memory architectures. 

**Design conflict-aware memory mechanisms that explicitly detect, attribute, and resolve inconsistencies across evolving memories and heterogeneous representations.** 

**Develop self-maintaining memory architectures with built-in indexing, updating, compression, and consistency checks for long-term, cross-session use.** 

**Advance long-horizon reasoning by integrating multi-modal long-context understanding with multi-turn dialogue reasoning, a core requirement for real-world agents.** 

Du et al. 

22 

Table 1. Product Memory Design Trade-offs. Representative products are compared to highlight recurring design choices and limitations of memory systems. 

|**Products**|**Domain**|**Dominant**<br>**Memory**|**Prioritized**<br>**Operations**|**User**<br>**Experience**|**Limitations**|
|---|---|---|---|---|---|
|**ChatGPT**<br>[223]|General|Parametric|Consolidation<br>Retrieval<br>Condensation|Consistency / Accuracy /<br>General|Hallucination; limited personalization and<br>modal memory management.|
|**Replika**<br>[191]|Personal|Contextual|Updating<br>Retrieval|Empathy / Adaptation|Privacy risks; memory drift; limited cross-<br>session continuity; simple slot-based mem-<br>ory management.|
|**GitHub**<br>**Copilot**<br>[79]|Task-oriented|Parametric|Condensation|Efficiency / Reliability|No cross-session task continuity; no user-<br>level personalization; no persistent long-<br>term memory.|
|**Doubao**<br>[22]|Multi-modal|Parametric|Consolidation<br>Retrieval<br>Condensation|General / Stylization /<br>Low latency|Hallucination; modality gap; session-bound.|

# **4 Memory In Practice** 

Memory augmentation agents operationalize theoretical memory concepts through an interdependent hierarchy of products, development tools, and infrastructure. Products such as assistants and copilots utilize parametric and contextual memory to support personalization and long-horizon reasoning. Development tools translate practical demands into frameworks that manage storage, retrieval, and adaptation. Infrastructure provides the computational backbone that supports memory operations at scale. The interaction among these layers is bidirectional: product requirements drive development tool design, tools constrain infrastructural implementation, and infrastructural advances enable richer product capabilities. Understanding and bridging the gaps among them clarifies both the technical and conceptual frontiers of agent memory mechanisms. 

# **4.1 Products** 

The agent products can be broadly categorized based on their dominant memory types and application focus. **General agents** like ChatGPT [223], Gemini [81], Claude [8], Grok [321], and DeepSeek [171] rely predominantly on large-scale parametric memory to encode broad cross-domain knowledge within model weights and underpin stable reasoning and factual generalization. Limited user contextual memory is layered on top to improve retrieval and situational grounding. **Personal agents** primarily leverage contextual memory to capture user preferences, interaction history, and affective cues, enabling personalized and adaptive responses [97, 153, 236] such as **Replika** [191], **Character.AI [27]** , **Me.bot** , **Tencent ima.copilot** [276] and **Doubao [22]** . These agents achieve long-term personalization and social coherence, though at the cost of privacy management and memory drift. **Task-oriented agents** rely on contextual memory and specific domain knowledge to execute multi-step reasoning and maintain session continuity like GitHub Copilot [79], Cursor [111], Coze [44], DeepResearcher [275], WebSearcher [275] and CodeBuddy [370]. For these agents, achieving a high task success rate remains the primary consideration for user satisfaction and practical effectiveness. **Multi-modal agents** represent a more integrated paradigm that unifies parametric and contextual memory across language, vision, and action modalities. Representative examples such as Mobile assistants (Doubao [22], Siri [11], 

Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

23 

Table 2. Memory Development Tools Trade-offs. Representative development tools are compared to highlight the special design and potential limitations. 

|**Tool**|**Category**|**Memory**<br>**Type**|**Prioritized**<br>**Operations**|**Key Features**|**Limitations**|
|---|---|---|---|---|---|
|**EasyEdit**<br>**[291]**|**Parametric**<br>**Editing**|Parametric|Updating|Directly modifies LLM weights<br>(WISE [289])|Ripple<br>Effects:<br>Editing<br>facts may damage general<br>reasoning; high computa-<br>tional cost.|
|**Zep**<br>**[239]**|**Temporal**<br>Memory<br>Construction|Contextual|Consolidation,<br>Updating|Temporal knowledge graphs;<br>incremental summarization; robust<br>temporal reasoning.|Controllability; Informa-<br>tion loss|
|**Mem0**<br>**[255]**|**Personalized**<br>Memory Layer|Contextual|Consolidation<br>Indexing<br>Updating|User-level personalization across<br>sessions; hybrid search (Vector +<br>Graph); developer-friendly API.|Lossy condensation; user-<br>centric<br>personalization<br>rather than complex task<br>or world-state memory.|
|**MemOS**<br>**[168]**|Memory<br>**Scheduling**&<br>Hierarchical<br>Management|Contextual|Updating<br>Retrieval|Hierarchical OS-style scheduling<br>(Short/Long/Working) for<br>optimized context window and<br>memory management.|Control overhead; latency|
|**Graphiti**<br>**[92]**|**Graph**Memory<br>Construction|Contextual|Indexing<br>Updating<br>Retrieval|Dynamic construction of<br>knowledge graphs from<br>unstructured streams; semantic<br>relationship tracking.|Strictly typed graphs can<br>be brittle with high token<br>consumption for graph<br>construction.|

Xiaoyi [109]) and Embodied Agent extend memory beyond text to perception and embodiment, marking a step toward general, long-horizon agents. 

Although these products have partially integrated memory-related functions, their memory scope and modality differ substantially across domains. ChatGPT and Doubao support long-range and cross-session adaptation through largemodel backbones, but their memory management remains relatively simple and prone to hallucination. Their multimodal memory functions are limited to basic image-grounded retrieval rather than integrated cross-modal reasoning. Replika, as a personalization-oriented companion system, relies heavily on transparent and user-driven memory updates. However, its stored content depends entirely on user input, lacking autonomous management and raising privacy concerns, while higher-level session memory remains undeveloped. In contrast, GitHub Copilot, constrained by the complexity of programming tasks, operates mainly within a short-term working memory window without persistent task-level or project-level memory coordination, and lacks personalized code adaptation. Overall, these systems remain in an early stage of memory integration, where memory operations are largely prompt-based rather than dynamically managed. This gap highlights the need for more advanced development tools to support scalable, transparent, and adaptive memory mechanisms across products and domains. 

# **4.2 Development Tools** 

**Frameworks.** On top of core infrastructure, frameworks offer modular interface for memory-related operations. Examples include **Graphiti** [92], **LlamaIndex** [175], **LangChain** [28], **LangGraph** [112], **EasyEdit** [291], **CrewAI** [66], MemU [217], and **Letta** [226]. These frameworks abstract complex memory processes into configurable pipelines, 

Du et al. 

24 

enabling developers to construct multi-modal, persistent, and updatable memory modules that interact with LLM agents. **Memory Layer Systems.** These systems operationalize memory as a service layer, providing orchestration, persistence, and lifecycle management. Tools like **Mem0** [255], **Zep** [239], **Memary** [140], **MemOS** [168] and **Memobase** [140] focus on maintaining temporal consistency, indexing memory by session or topic, and ensuring efficient recall. These platforms often combine symbolic and sub-symbolic memory representations and provide internal APIs for memory access and manipulation over time. 

# **4.3 Infrastructure** 

Memory tools rely on a robust foundational infrastructure to operationalize the storage, retrieval, and evolution of memory. This infrastructure is anchored by persistent storage systems, such as graph databases like **Neo4j** [216] and vector stores [61], which work in tandem with retrieval mechanisms ranging from sparse **BM25** [243] to dense embedding retrieval [113, 224] to ensure precise access. The execution of complex memory lifecycle operations—including dynamic updating and targeted forgetting—depends on the reasoning capabilities of LLMs [1, 171] guided by optimized prompt engineering. Crucially, to support the high throughput and scalability required by these tools, the underlying computational layer incorporates acceleration technologies such as **FlashAttention** [46], sequence parallelism, and efficient Key-Value (KV) cache management strategies [146], all designed to enable the effective processing of ultra-long contexts and massive interaction histories. 

# **5 The Cognitive Gap between Biological and Agent Memory** 

Human memory is not a monolithic storage but a complex, hierarchical interaction between sensory, short-term, and long-term systems [12]. While agents aim to emulate these functions to support reasoning, their underlying mechanisms are different from biological cognitive architectures. As summarized in Table 3, current agentic implementations remain focused on static persistence, lacking the dynamic sophistication of biological memory in terms of encoding, evolving, and adapting. 

_Encoding: From Verbatim Recording to Constructive Schematization._ Human encoding is inherently _constructive_ ; we do not record snapshots but restructure the past through present cognition to fit internal schemas. In contrast, agents typically perform verbatim recording (in databases) or static parameterization (in weights), leading to an accumulation of fragmented traces rather than a synthesized self-model. This reliance on "raw" data prevents agents from pruning noise at the point of entry. While current training (e.g., pre/post-training [171]) attempts internalization, it remains a discrete process that fails to bridge the gap between static "knowing that" and the adaptive cognitive structures required to filter environmental complexity. 

_Evolving: From Summarization to Internalization._ Memory evolution in humans relies on sleep-dependent reconsolidation, where episodic traces are distilled into semantic structures of general world knowledge. This active synthesis prunes noise and extracts causal patterns to prevent overfitting to immediate reality. In contrast, agent memory evolution depends on explicit operations like summarization or hard deletion to simulate memory dynamics. While frameworks such as ACE [361] utilize summarization for short-term buffer condensation, they primarily address immediate task resolution rather than long-term cognitive growth. Conversely, although systems like G-Memory [356] construct long-term archives via hierarchical graphs, this remains a symbolic approach to evolution. These mechanisms treat memory like a static library that needs filing, whereas human memory is like a muscle. While agents can summarize a book (ephemeral experience), they fail to turn that knowledge into the instinctive skill (procedural wisdom) needed to perform a task 

25 

Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

|**Aspect**|**Human Memory**|**Agent Memory**|
|---|---|---|
|**Storage**|Distributed, interconnected neural systems<br>across brain regions|Model parameter, modular, and context-<br>dependent|
|**Ownership**|Individual and private.|Shareable, replicable, and broadcastable.|
|**Volume**|Biologically limited|Scalable, bounded only by storage and com-<br>pute limits|
|**Memory Encoding**|Slow, biologically driven, passive|Fast, explicit, policy-driven and selective|
|**Memory Evolving**|Indirect, reconsolidation-based, error-prone|Precise, programmable, supports rollback-<br>/unlearning|
|**Memory Adaption**|Implicit, salience- and frequency-biased|Explicit, customizable (e.g., quantization,<br>summarization)|
||Table 3. Key differences between human a|f   nd agent memory.|

naturally. Consequently, contemporary agents remain reactive note-takers limited by artificially compressed histories, lacking the capacity for long-lifecycle evolving or the construction of a consistent self-representation. 

_Adapting: From Retrieval to Meaning Construction._ Human memory utilization is a process of dynamic reconstruction driven by homeostatic needs and self-consistency [12]. In contrast, current agents predominantly rely on RetrievalAugmented Generation (RAG) and extremely long context windows. While expanding the context window provides a larger buffer, it represents a brute-force architectural scaling that bypasses the necessity of semantic internalization. Such "long-context" dependency leads to a diminishing signal-to-noise ratio and prohibitive computational costs. As evidenced by the ’lost-in-the-middle’ phenomenon [179], retrieval without inference-time reconsolidation, characterized by the active rewriting of historical traces like AgentFold [344] and FoldGRPO [264], struggles to develop a coherent causal representation. The next frontier is to move beyond passive retrieval toward active thinkers who reconstruct their internal state in real-time to adapt to environmental dynamics. 

_Storage, Ownership and Volume._ The divergence between biological and agent memory is rooted in the fundamental properties of their physical and systemic substrates, primarily manifested in storage, data ownership, and resource scalability. Regarding **storage** , human memory is characterized by biological **holistic interconnection** , enabling associative recall across the entire brain. Conversely, agents rely on **heterogeneous representations** —segregating data into disconnected formats like documents, graphs, and vector embeddings—which prioritizes local pattern matching over global semantic coherence. This systemic gap extends to **data ownership** : human memory is inherently private and individual-bounded, whereas agent memory is **replicable and broadcastable** , enabling collective intelligence but challenging the ethical "right to be forgotten." Finally, while the human brain achieves complex memory evolving with extreme metabolic frugality (∼20W) [17], agent memory remains constrained by the computational and environmental costs of silicon-based scaling, necessitating a shift toward bio-inspired efficiency that prioritizes semantic density over raw data volume. 

# **6 Open Challenges and Future Directions** 

This section outlines the open challenges in core memory topics and proposes future research directions. We then explore broader perspectives, including biologically inspired models, lifelong learning, multi-agent memory, and unified 

Du et al. 

26 

memory representation, which further extend the capabilities and theoretical grounding of memory systems. Together, these discussions provide a roadmap for advancing reliable, interpretable, and adaptive memory in AI. 

# **6.1 Topic-Specific Directions** 

Designing memory-centric AI requires addressing core limitations and emerging demands. Guided by RCI analysis and trends, we outline key challenges shaping future memory research. 

**Unified evaluation is needed to address consistency, personalization, and temporal reasoning in long-term memory.** Existing benchmarks rarely assess core operations such as consolidation, updating, retrieval, and forgetting in dynamic, multi-session settings. This gap contributes to the retrieval–generation mismatch, where retrieved content is often outdated, irrelevant, or misaligned due to poor memory maintenance. Addressing these issues requires temporal reasoning, structure-aware generation, and retrieval robustness, along with systems supporting personalized reuse and adaptive memory management across sessions. 

**Long-context Processing: Efficiency vs. Expressivity.** Scaling memory length exacerbates trade-offs between computational cost and modeling fidelity. Techniques such as KV cache compression and recurrent memory reuse offer efficiency but risk information loss or instability. Meanwhile, reasoning over complex environments, especially in multi-source or multi-modal settings, requires selective context integration, source differentiation, and attention modulation. Bridging these demands, mechanisms that balance contextual bandwidth with task relevance and stability, increasingly pointing toward the use of RL-based frameworks to learn active optimal context management and folding policies. 

**While promising, parametric memory modification requires further research to improve control, erasure, and scalability.** Current editing methods often lack specificity, while unlearning benchmarks like TOFU may be too simple to expose real limitations. Most approaches fail to scale beyond thousands of edits or support models over 20B parameters. Lifelong learning remains underexplored despite its potential. Future work should develop more realistic benchmarks, improve efficiency, and unify editing, unlearning, and continual learning into a cohesive framework. 

**Multi-source Integration: Consistency, Compression, and Coordination.** Modern agents rely on heterogeneous memory comprising structured knowledge, unstructured histories, and multi-modal signals but face redundancy, inconsistency, and ambiguity. These stem from misaligned temporal scopes, conflicting semantics, and missing attribution across modalities. Resolving them requires conflict resolution, temporal grounding, and provenance tracking. Efficient indexing and compression are essential for scalability and interpretability in multi-session settings. 

# **6.2 Broader Perspectives** 

In addition to the core topics outlined above, a range of broader perspectives is emerging that further enriches the landscape of memory-centric agents. 

**Procedural Tool Memory and Skill Acquisition.** As agents become more action-oriented, memory needs to evolve from static fact storage toward procedural tool memory, where tool use is internalized as reusable skills rather than repeatedly consulting the tool API during extended interactions. Frameworks such as ReAct [341] already hint at this shift by coupling reasoning with action trajectories, enabling agents to learn from execution feedback instead of treating tools as stateless calls. Recent infrastructure, including MCP [9] servers, further supports this evolving by framing tools as persistent services that allow for experience accumulation across interactions. Benchmarks like BFCL v4 [229] explicitly expose the need for memorizing execution traces, error-recovery strategies, and tool-chain compositions, rather than relying on ad hoc prompting. Industrial systems have begun to operationalize this idea, 

Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

27 

exemplified by Anthropic’s introduction of skills [10] in Claude, which treat tool use as a form of procedural memory that improves reliability and reduces inference cost. 

**Parametric Sharing: Memory as Dynamic Weights.** While textual memory (e.g., RAG) provides transparency, it inevitably suffers from information loss during compression and natural language conversion. We propose Parametric Sharing, where memory is exchanged as model-native representations [21]—such as dynamic adapters or specialized memory layers—directly within the latent space [383]. This approach preserves high-dimensional semantic nuances and enhances the collective reasoning of fused systems by bypassing the "bottleneck" of explicit text. Future work should explore standardized neural memory protocols and cross-model weight alignment to enable heterogeneous agents to merge internalized experiences into a collaborative parametric intelligence. 

**Lifelong Learning.** Future research should shift from discrete task-based learning to managing real-time environment streams [361], focusing on mitigating catastrophic forgetting while maintaining rapid adaptation [73]. Under extreme data sparsity, agents must utilize meta-learning to optimize a "memory value function," enabling the autonomous determination of "solidification value" for selective memory internalization [277]. Crucially, personalized representations must transcend the restrictive inductive bias of the base model’s pre-trained distribution, which often suppresses unique individual traits. By integrating structural [239] and unstructured memory [13] into a dynamic personalized parameter space (e.g., evolving LoRA or embeddings), agents can decouple personal traces from general knowledge. This ensures causal consistency across infinite horizons, evolving agents from task-oriented tools into longitudinal, habit-aware companions. 

**Memory in Multi-agent Systems.** In multi-agent systems, memory is not only individual but also distributed. Agents must manage their own internal memories while interacting with and learning from others [298]. This raises unique challenges such as memory sharing, alignment, conflict resolution, and consistency across agents. Effective multiagent memory systems should support both local retention of personalized experiences and global coordination through shared memory spaces or communication protocols. Future work may explore decentralized memory architectures, cross-agent memory synchronization, and collective memory consolidation to enable collaborative planning, reasoning, and long-term coordination. 

**Multi-modal Memory.** Multi-modal memory inherently reflects how humans perceive the real world. While advancements like M3-agent [189] and GUI-agent [97] have explored multi-modal memory processing capabilities, this field remains in its preliminary stages. Significant challenges persist in aligning multi-modal memories within a unified semantic space and enabling effective retrieval and reasoning. Specifically, current systems suffer from weak reasoning during multi-turn interactions and data misalignment, highlighting critical directions for future research. 

**Biological Inspirations for Memory Design.** Memory in biological systems offers key insights for building more resilient and adaptive AI memory architectures. The brain manages the stability–plasticity dilemma through complementary learning systems: the hippocampus encodes fast-changing episodic experiences, while the cortex slowly integrates stable long-term memory [144, 199]. Inspired by this, AI models increasingly adopt dual-memory architectures, synaptic consolidation, and experience replay to mitigate forgetting [242, 284]. Cognitive concepts like memory reconsolidation [67], bounded memory capacity [43], and compartmentalized knowledge [75] further inform strategies for update-aware recall, efficient storage, and context-sensitive generalization. 

Meanwhile, the K-Line Theory [210] points out that hierarchical memory structures are fundamental to biological cognition. These structures enable humans to efficiently organize memory across different levels of abstraction, as seen in how infants group specific objects like "apple" and "banana" into broader categories like "fruit" and "food." Organizing 

Du et al. 

28 

the agent memory with hierarchy structures for scalability and efficiency raises new challenges [87, 310] and future directions [96, 308] for memory research. 

**Parametric Memory Retrieval.** While recent knowledge editing methods [70, 289] claim they can localize and modify specific representations, enabling models to selectively retrieve knowledge from their own parameters remains an open challenge. Efficient retrieval and integration of latent memory could significantly enhance memory utilization and reduce dependence on external indexing and memory management. 

**Spatio-temporal Memory** captures not only the structural relationships among information but also their temporal evolution, enabling agents [150] to adaptively update knowledge while preserving historical context [372]. For example, the agent may record that a user once disliked broccoli but later adjusts its memory based on recent purchase patterns. By maintaining access to both historical and current states, spatio-temporal memory supports temporally informed reasoning and nuanced personalization. However, efficiently managing and reasoning over long-term spatio-temporal memory remains a key challenge. 

**Unified Memory Representation.** While parametric memory [335] provides compact and implicit knowledge storage, and external memory [375] offers explicit and interpretable information, unifying their representational spaces and establishing joint indexing mechanisms is essential for effective memory consolidation and retrieval. Future work could focus on developing unified memory representation frameworks that support shared indexing, hybrid storage, and memory operations across modalities and knowledge forms. 

**Memory Threats & Safety.** While memory significantly enhances the utility of LLMs by enabling up-to-date and personalized responses, its management remains a critical safety concern. Memory often stores sensitive and confidential data, making operations like adding or removing information far from trivial. Recent research has exposed serious vulnerabilities in memory handling, particularly in machine unlearning techniques designed to selectively erase data. Multiple studies [18, 187] have demonstrated that these methods are prone to malicious attacks, which strengthens the need for more secure and reliable memory operations. 

# **7 Conclusions** 

This survey provides a comprehensive overview of agent memory, classifying it into parametric and contextual types and mapping operations to encoding, evolving, and adapting. Complemented by functional perspectives like episodic, semantic, procedural, and working memory, this framework clarifies how memory supports reasoning, personalization, and collaboration. By analyzing four key topics, including long-term memory, long context memory, parametric modification, and multi-source memory, we highlight progress, challenges, and pathways for future work, while offering practical benchmarks and tool guidance for industry. 

# **References** 

- [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. 2023. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ (2023). 

- [2] Muhammad Adnan, Akhil Arunkumar, Gaurav Jain, Prashant J. Nair, Ilya Soloveychik, and Purushotham Kamath. 2024. Keyformer: KV Cache reduction through key tokens selection for Efficient Generative Inference. In _Proceedings of Machine Learning and Systems_ . https://proceedings. mlsys.org/paper_files/paper/2024/file/48fecef47b19fe501d27d338b6d52582-Paper-Conference.pdf 

- [3] Saurabh Agarwal, Bilge Acun, and Basil et al. Hosmer. 2024. CHAI: Clustered Head Attention for Efficient LLM Inference. In _ICML_ . https: //proceedings.mlr.press/v235/agarwal24a.html 

- [4] Qingyao Ai, Yichen Tang, Changyue Wang, Jianming Long, Weihang Su, and Yiqun Liu. 2025. MemoryBench: A Benchmark for Memory and Continual Learning in LLM Systems. _arXiv preprint arXiv:2510.17281_ (2025). 

- [5] Chenxin An, Shansan Gong, Ming Zhong, Xingjian Zhao, Mukai Li, Jun Zhang, Lingpeng Kong, and Xipeng Qiu. 2024. L-Eval: Instituting Standardized Evaluation for Long Context Language Models. In _Proceedings of the 62nd Annual Meeting of the Association for Computational_ 

Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

29 

   - _Linguistics (Volume 1: Long Papers)_ . doi:10.18653/v1/2024.acl-long.776 

- [6] Shengnan An, Zexiong Ma, Zeqi Lin, Nanning Zheng, Jian-Guang Lou, and Weizhu Chen. 2024. Make Your LLM Fully Utilize the Context. In _Advances in Neural Information Processing Systems_ . https://proceedings.neurips.cc/paper_files/paper/2024/file/71c3451f6cd6a4f82bb822db25cea4fdPaper-Conference.pdf 

- [7] Sotiris Anagnostidis, Dario Pavllo, and Luca et al. Biggio. 2023. Dynamic Context Pruning for Efficient and Interpretable Autoregressive Transformers. In _NeurIPS_ . https://proceedings.neurips.cc/paper_files/paper/2023/file/cdaac2a02c4fdcae77ba083b110efcc3-Paper-Conference.pdf 

- [8] Anthropic. 2023. Claude: AI Thinking Partner. https://www.claude.com/. Accessed: 2025-11-01. 

- [9] Anthropic. 2024. Introducing the Model Context Protocol. https://www.anthropic.com/news/model-context-protocol. Model Context Protocol (MCP) Specification. 

- [10] Anthropic. 2025. Equipping agents for the real world with Agent Skills. https://claude.com/blog/skills. Accessed: 2025-12-21. 

- [11] Apple Inc. 2025. _Siri: Apple’s Intelligent Voice Assistant_ . https://www.apple.com/siri/ Accessed: 2025-11-01. 

- [12] Alan Baddeley. 1988. Cognitive Psychology and Human Memory. _Trends in Neurosciences_ 11, 4 (1988), 176–181. 

- [13] Sanghwan Bae, Donghyun Kwak, Soyoung Kang, Min Young Lee, Sungdong Kim, Yuin Jeong, Hyeri Kim, Sang-Woo Lee, Woomyoung Park, and Nako Sung. 2022. Keep Me Updated! Memory Management in Long-term Conversations. In _Findings of the Association for Computational Linguistics: EMNLP 2022_ . doi:10.18653/v1/2022.findings-emnlp.276 

- [14] Jinze Bai, Shuai Bai, Shusheng Yang, Shijie Wang, Sinan Tan, Peng Wang, Junyang Lin, Chang Zhou, and Jingren Zhou. 2023. Qwen-VL: A Versatile Vision-Language Model for Understanding, Localization, Text Reading, and Beyond. _arXiv_ (2023). https://arxiv.org/abs/2308.12966 

- [15] Yushi Bai, Xin Lv, Jiajie Zhang, Hongchang Lyu, Jiankai Tang, Zhidian Huang, Zhengxiao Du, Xiao Liu, Aohan Zeng, Lei Hou, Yuxiao Dong, Jie Tang, and Juanzi Li. 2024. LongBench: A Bilingual, Multitask Benchmark for Long Context Understanding. In _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ . doi:10.18653/v1/2024.acl-long.172 

- [16] Yushi Bai, Shangqing Tu, Jiajie Zhang, Hao Peng, Xiaozhi Wang, Xin Lv, Shulin Cao, Jiazheng Xu, Lei Hou, Yuxiao Dong, Jie Tang, and Juanzi Li. 2025. LongBench v2: Towards Deeper Understanding and Reasoning on Realistic Long-context Multitasks. https://arxiv.org/abs/2412.15204 

- [17] Vijay Balasubramanian. 2021. Brain power. _Proceedings of the National Academy of Sciences_ 118, 32 (2021), e2107022118. 

- [18] Fazl Barez, Tingchen Fu, Ameya Prabhu, Stephen Casper, Amartya Sanyal, Adel Bibi, Aidan O’Gara, Robert Kirk, Ben Bucknall, Tim Fist, Luke Ong, Philip Torr, Kwok-Yan Lam, Robert Trager, David Krueger, Sören Mindermann, José Hernandez-Orallo, Mor Geva, and Yarin Gal. 2025. Open Problems in Machine Unlearning for AI Safety. https://arxiv.org/abs/2501.04952 

- [19] Payman Behnam, Yaosheng Fu, Ritchie Zhao, Po-An Tsai, Zhiding Yu, and Alexey Tumanov. 2025. RocketKV: Accelerating Long-Context LLM Inference via Two-Stage KV Cache Compression. In _Forty-second International Conference on Machine Learning_ . https://openreview.net/forum?id= RyOpooIxDF 

- [20] Ali Behrouz, Peilin Zhong, and Vahab Mirrokni. 2024. Titans: Learning to memorize at test time. _arXiv_ (2024). https://arxiv.org/abs/2501.00663 

- [21] Vincent-Pierre Berges, Barlas Oğuz, Daniel Haziza, Wen-tau Yih, Luke Zettlemoyer, and Gargi Ghosh. 2024. Memory Layers at Scale. doi:10.48550/ arXiv.2412.09764 

- [22] ByteDance Seed Team. 2025. _Doubao-1.5-pro: A High-Efficiency Sparse MoE Multimodal AI Model_ . https://seed.bytedance.com/en/special/doubao_ 1_5_pro Accessed: 2025-11-01. 

- [23] Jiaqi Cao, Jiarui Wang, Rubin Wei, Qipeng Guo, Kai Chen, Bowen Zhou, and Zhouhan Lin. 2025. Memory Decoder: A Pretrained, Plug-and-Play Memory for Large Language Models. _arXiv preprint arXiv:2508.09874_ (2025). 

- [24] Shuyang Cao and Lu Wang. 2024. AWESOME: GPU Memory-constrained Long Document Summarization using Memory Mechanism and Global Salient Content. In _Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)_ . doi:10.18653/v1/2024.naacl-long.330 

- [25] Zhiwei Cao, Qian Cao, Yu Lu, Ningxin Peng, Luyang Huang, Shanbo Cheng, and Jinsong Su. 2024. Retaining Key Information under High Compression Ratios: Query-Guided Compressor for LLMs. In _Proceedings of the ACL_ . doi:10.18653/v1/2024.acl-long.685 

- [26] Sungmin Cha, Sungjun Cho, Dasol Hwang, and Moontae Lee. 2025. Towards Robust and Parameter-Efficient Knowledge Unlearning for LLMs. In _The Thirteenth International Conference on Learning Representations_ . https://openreview.net/forum?id=1ExfUpmIW4 

- [27] Character Technologies, Inc. 2023. _Character.AI: A Platform for Creating and Interacting with AI Characters_ . https://character.ai Accessed: 2025-11-01. 

- [28] Harrison Chase. 2022. LangChain. https://www.langchain.com 

- [29] Ding Chen, Simin Niu, Kehang Li, Peng Liu, Xiangping Zheng, Bo Tang, Xinchi Li, Feiyu Xiong, and Zhiyu Li. 2025. HaluMem: Evaluating Hallucinations in Memory Systems of Agents. _arXiv preprint arXiv:2511.03506_ (2025). 

- [30] Jiaao Chen and Diyi Yang. 2023. Unlearn What You Want to Forget: Efficient Unlearning for LLMs. In _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing_ . 12041–12052. 

- [31] Mingda Chen, Yang Li, Karthik Padthe, et al. 2024. Improving Factuality with Explicit Working Memory. _arXiv preprint arXiv:2412.18069_ (2024). 

- [32] Nuo Chen, Hongguang Li, Juhua Huang, Baoyuan Wang, and Jia Li. 2024. Compress to impress: Unleashing the potential of compressive memory in real-world long-term conversations. _arXiv preprint arXiv:2402.11975_ (2024). 

- [33] Renze Chen, Zhuofeng Wang, and Beiquan et al. Cao. 2024. ArkVale: Efficient Generative LLM Inference with Recallable Key-Value Eviction. In _NeurIPS_ . https://proceedings.neurips.cc/paper_files/paper/2024/file/cd4b49379efac6e84186a3ffce108c37-Paper-Conference.pdf 

Du et al. 

30 

- [34] Wenhu Chen, Zhihao He, Yu Su, Yunyao Yu, William Wang, and Xifeng Yan. 2021. HybridQA: A Dataset of Multi-Hop Question Answering over Tabular and Textual Data. In _Proceedings of the International Conference on Learning Representations (ICLR)_ . 

- [35] Yilong Chen, Guoxia Wang, Junyuan Shang, Shiyao Cui, Zhenyu Zhang, Tingwen Liu, Shuohuan Wang, Yu Sun, Dianhai Yu, and Hua Wu. 2024. NACL: A General and Effective KV Cache Eviction Framework for LLM at Inference Time. In _Proceedings of the ACL_ . doi:10.18653/v1/2024.acllong.428 

- [36] Xin Cheng, Xun Wang, Xingxing Zhang, Tao Ge, Si-Qing Chen, Furu Wei, Huishuai Zhang, and Dongyan Zhao. 2024. xrag: Extreme context compression for retrieval-augmented generation with one token. _arXiv preprint arXiv:2405.13792_ (2024). 

- [37] Alexis Chevalier, Alexander Wettig, Anirudh Ajith, and Danqi Chen. 2023. Adapting Language Models to Compress Contexts. In _Proceedings of the EMNLP_ . doi:10.18653/v1/2023.emnlp-main.232 

- [38] Somnath Basu Roy Chowdhury, Krzysztof Marcin Choromanski, Arijit Sehanobish, Kumar Avinava Dubey, and Snigdha Chaturvedi. 2025. Towards Scalable Exact Machine Unlearning Using Parameter-Efficient Fine-Tuning. In _The Thirteenth International Conference on Learning Representations_ . https://openreview.net/forum?id=oe51Q5Uo37 

- [39] Tianzhe Chu, Yuexiang Zhai, Jihan Yang, Shengbang Tong, Saining Xie, Dale Schuurmans, Quoc V Le, Sergey Levine, and Yi Ma. 2025. Sft memorizes, rl generalizes: A comparative study of foundation model post-training. _arXiv preprint arXiv:2501.17161_ (2025). 

- [40] Yu-Neng Chuang, Tianwei Xing, Chia-Yuan Chang, Zirui Liu, Xun Chen, and Xia Hu. 2024. Learning to Compress Prompt in Natural Language Formats. In _Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)_ . doi:10.18653/v1/2024.naacl-long.429 

- [41] Tsz Ting Chung, Leyang Cui, Lemao Liu, Xinting Huang, Shuming Shi, and Dit-Yan Yeung. 2024. Selection-p: Self-Supervised Task-Agnostic Prompt Compression for Faithfulness and Transferability. In _Findings of the Association for Computational Linguistics: EMNLP 2024_ . doi:10.18653/ v1/2024.findings-emnlp.646 

- [42] Codebuddy AI Inc. 2025. CodeBuddy: AI-Powered Coding Assistant. https://codebuddy.ca/ Accessed: 2025-05-23. 

- [43] Nelson Cowan. 2001. The magical number 4 in short-term memory: A reconsideration of mental storage capacity. _Behavioral and Brain Sciences_ (2001). 

- [44] Coze. 2024. Coze: Build your own AI agent. https://www.coze.cn/. Accessed: 2025-04-19. 

- [45] Bhavana Dalvi Mishra, Oyvind Tafjord, and Peter Clark. 2022. Towards Teachable Reasoning Systems: Using a Dynamic Memory of User Feedback for Continual System Improvement. In _Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing_ . https: //aclanthology.org/2022.emnlp-main.644/ 

- [46] Tri Dao. 2024. FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning. In _The Twelfth International Conference on Learning Representations_ . https://openreview.net/forum?id=mZn2Xyh9Ec 

- [47] Payel Das, Subhajit Chaudhury, Elliot Nelson, Igor Melnyk, Sarathkrishna Swaminathan, Sihui Dai, Aurélie Lozano, Georgios Kollias, Vijil Chenthamarakshan, Jiří Navrátil, Soham Dan, and Pin-Yu Chen. 2024. Larimar: Large Language Models with Episodic Memory Control. In _International Conference on Machine Learning_ . https://arxiv.org/abs/2403.11901 

- [48] Payel Das, Subhajit Chaudhury, Elliot Nelson, Igor Melnyk, Sarathkrishna Swaminathan, Sihui Dai, Aurélie C. Lozano, Georgios Kollias, Vijil Chenthamarakshan, Jirí Navrátil, Soham Dan, and Pin-Yu Chen. 2024. Larimar: Large Language Models with Episodic Memory Control. In _ICML_ . https://openreview.net/forum?id=t8mt4YrPsq 

- [49] Ronald L Davis and Yi Zhong. 2017. The biology of forgetting—a perspective. _Neuron_ (2017). 

- [50] Nicola De Cao, Wilker Aziz, and Ivan Titov. 2021. Editing Factual Knowledge in Language Models. In _Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing_ . 

- [51] Cyprien de Masson D’Autume, Sebastian Ruder, Lingpeng Kong, et al. 2019. Episodic Memory in Lifelong Language Learning. _Advances in Neural Information Processing Systems_ 32 (2019). 

- [52] Jingcheng Deng, Zihao Wei, Liang Pang, Hanxing Ding, Huawei Shen, and Xueqi Cheng. 2025. Everything is Editable: Extend Knowledge Editing to Unstructured Data in Large Language Models. In _The Thirteenth International Conference on Learning Representations_ . https://openreview.net/ forum?id=X5rO5VyTgB 

- [53] Alessio Devoto, Yu Zhao, Simone Scardapane, and Pasquale Minervini. 2024. A Simple and Effective _𝐿_ 2 Norm-Based Strategy for KV Cache Compression. In _EMNLP_ . doi:10.18653/v1/2024.emnlp-main.1027 

- [54] Shangzhe Di, Zhelun Yu, and Guanghao et al. Zhang. 2025. Streaming Video Question-Answering with In-context Video KV-Cache Retrieval. In _ICLR_ . https://openreview.net/forum?id=8g9fs6mdEG 

- [55] Chenlu Ding, Jiancan Wu, Yancheng Yuan, Jinda Lu, Kai Zhang, Alex Su, Xiang Wang, and Xiangnan He. 2025. Unified Parameter-Efficient Unlearning for LLMs. In _The Thirteenth International Conference on Learning Representations_ . https://openreview.net/forum?id=zONMuIVCAT 

- [56] Jiayu Ding, Shuming Ma, Li Dong, Xingxing Zhang, Shaohan Huang, Wenhui Wang, Nanning Zheng, and Furu Wei. 2023. LongNet: Scaling Transformers to 1,000,000,000 Tokens. _arXiv preprint arXiv:2307.02486_ (2023). https://arxiv.org/abs/2307.02486 

- [57] Xuanwen Ding, Jie Zhou, Liang Dou, Qin Chen, Yuanbin Wu, Arlene Chen, and Liang He. 2024. Boosting Large Language Models with Continual Learning for Aspect-based Sentiment Analysis. In _Findings of the EMNLP_ . doi:10.18653/v1/2024.findings-emnlp.252 

- [58] Yiran Ding, Li Lyna Zhang, Chengruidong Zhang, Yuanyuan Xu, Ning Shang, Jiahang Xu, Fan Yang, and Mao Yang. 2024. LongRoPE: Extending LLM Context Window Beyond 2 Million Tokens. _arXiv preprint arXiv:2402.13753_ (2024). https://arxiv.org/abs/2402.13753 

Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

31 

- [59] Harry Dong, Xinyu Yang, Zhenyu Zhang, Zhangyang Wang, Yuejie Chi, and Beidi Chen. 2024. Get More with LESS: Synthesizing Recurrence with KV Cache Compression for Efficient LLM Inference. In _Proceedings of the 41st International Conference on Machine Learning_ . https: //proceedings.mlr.press/v235/dong24f.html 

- [60] Qingxiu Dong, Damai Dai, Yifan Song, Jingjing Xu, Zhifang Sui, and Lei Li. 2022. Calibrating Factual Knowledge in Pretrained Language Models. In _Findings of the Association for Computational Linguistics: EMNLP 2022_ . 5937–5947. 

- [61] Matthijs Douze, Alexandr Guzhva, Chengqi Deng, Jeff Johnson, Gergely Szilvasy, Pierre-Emmanuel Mazar’e, Maria Lomeli, Lucas Hosseini, and Herv’e J’egou. 2024. The faiss library. _arXiv preprint arXiv:2401.08281_ (2024). 

- [62] Danny Driess, Fei Xia, Mehdi SM Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, et al. 2023. PaLM-E: An Embodied Multimodal Language Model. _arXiv preprint arXiv:2303.03378_ (2023). 

- [63] Xinya Du, Sha Li, and Heng Ji. 2022. Dynamic Global Memory for Document-level Argument Extraction. In _Proceedings of the ACL_ . doi:10.18653/ v1/2022.acl-long.361 

- [64] Yiming Du, Bingbing Wang, Yang He, Bin Liang, Baojun Wang, Zhongyang Li, Lin Gui, Jeff Z. Pan, Ruifeng Xu, and Kam-Fai Wong. 2025. MemGuide: Intent-Driven Memory Selection for Goal-Oriented Multi-Session LLM Agents. arXiv preprint. doi:10.48550/arXiv.2505.20231 arXiv:2505.20231. 

- [65] Yiming Du, Hongru Wang, Zhengyi Zhao, et al. 2024. PerLTQA: A Personal Long-term Memory Dataset for Memory Classification, Retrieval, and Synthesis in QA. _arXiv preprint arXiv:2402.16288_ (2024). 

- [66] Zhihua Duan and Jialin Wang. 2024. Exploration of LLM Multi-Agent Application Implementation Based on LangGraph+ CrewAI. _arXiv preprint arXiv:2411.18241_ (2024). 

- [67] Yadin Dudai, Avi Karni, and Jan Born. 2015. The consolidation and transformation of memory. _Neuron_ (2015). 

- [68] Ritam Dutt, Kasturi Bhattacharjee, Rashmi Gangadharaiah, Dan Roth, and Carolyn Rose. 2022. PerKGQA: Question answering over personalized knowledge graphs. In _Findings of the Association for Computational Linguistics: NAACL 2022_ . 

- [69] Ronen Eldan and Mark Russinovich. 2024. Who’s Harry Potter? Approximate Unlearning for LLMs. https://openreview.net/forum?id=PDct7vrcvT 

- [70] Junfeng Fang, Houcheng Jiang, Kun Wang, Yunshan Ma, Jie Shi, Xiang Wang, Xiangnan He, and Tat-Seng Chua. 2025. AlphaEdit: Null-Space Constrained Model Editing for Language Models. In _The Thirteenth International Conference on Learning Representations_ . https://openreview.net/ forum?id=HvSytvg3Jh 

- [71] Runnan Fang, Yuan Liang, Xiaobin Wang, Jialong Wu, Shuofei Qiao, Pengjun Xie, Fei Huang, Huajun Chen, and Ningyu Zhang. 2025. Memp: Exploring Agent Procedural Memory. _arXiv preprint arXiv:2508.06433_ (2025). 

- [72] Weizhi Fei, Xueyan Niu, and Pingyi et al. Zhou. 2024. Extending Context Window of Large Language Models via Semantic Compression. In _ACL Findings_ . doi:10.18653/v1/2024.findings-acl.306 

- [73] Yujie Feng, Xu Chu, Yongxin Xu, et al. 2024. TaSL: Continual Dialog State Tracking via Task Skill Localization and Consolidation. In _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics_ . doi:10.18653/v1/2024.acl-long.69 

- [74] Zafeirios Fountas, Martin A Benfeghoul, Adnan Oomerjee, Fenia Christopoulou, Gerasimos Lampouras, Haitham Bou-Ammar, and Jun Wang. 2024. Human-like Episodic Memory for Infinite Context LLMs. _arXiv preprint arXiv:2407.09450_ (2024). 

- [75] Nicholas T Franklin, Kenneth A Norman, Charan Ranganath, Jeffrey M Zacks, and Samuel J Gershman. 2020. Structured event memory: A neuro-symbolic model of event cognition. _Psychological Review_ (2020). 

- [76] Yu Fu, Zefan Cai, Abedelkadir Asi, Wayne Xiong, Yue Dong, and Wen Xiao. 2025. Not All Heads Matter: A Head-Level KV Cache Compression Method with Integrated Retrieval and Reasoning. In _International Conference on Learning Representations_ . https://openreview.net/forum?id=FJFVmeXusW 

- [77] Suyu Ge, Yunan Zhang, Liyuan Liu, Minjia Zhang, Jiawei Han, and Jianfeng Gao. 2024. Model Tells You What to Discard: Adaptive KV Cache Compression for LLMs. In _The Twelfth International Conference on Learning Representations_ . https://openreview.net/forum?id=uNrFpDPMyo 

- [78] Yubin Ge, Salvatore Romeo, Jason Cai, Raphael Shu, Monica Sunkara, Yassine Benajiba, and Yi Zhang. 2025. Tremu: Towards Neuro-Symbolic Temporal Reasoning for LLM-Agents with Memory in Multi-Session Dialogues. _arXiv preprint arXiv:2502.01630_ (2025). 

- [79] GitHub and OpenAI. 2021. GitHub Copilot: Your AI pair programmer. https://github.com/features/copilot. Accessed May 2025. 

- [80] Marc Glocker, Peter Hönig, Matthias Hirschmanner, and Markus Vincze. 2025. LLM-Empowered Embodied Agent for Memory-Augmented Task Planning in Household Robotics. _arXiv preprint arXiv:2504.21716_ (2025). 

- [81] Google AI / DeepMind. 2024. Gemini: Multimodal AI Assistant. https://gemini.google/. Accessed: 2025-11-01. 

- [82] Xudong Guo, Kaixuan Huang, and Jiale et al. Liu. 2024. Embodied LLM Agents Learn to Cooperate in Organized Teams. _arXiv preprint arXiv:2403.12482_ (2024). 

- [83] Yaming Guo, Siyang Guo, Hengshu Zhu, and Ying Sun. 2025. Towards Lifelong Model Editing via Simulating Ideal Editor. In _Forty-second International Conference on Machine Learning_ . https://openreview.net/forum?id=VdEG08ZJCH 

- [84] Bernal Jiménez Gutiérrez, Yiheng Shu, Yu Gu, et al. 2024. HippoRAG: Neurobiologically Inspired Long-term Memory for Large Language Models. In _NeurIPS_ . 

- [85] Bernal Jiménez Gutiérrez, Yiheng Shu, Weijian Qi, Sizhe Zhou, and Yu Su. 2025. From RAG to Memory: Non-Parametric Continual Learning for Large Language Models. _arXiv preprint arXiv:2502.14802_ (2025). 

- [86] Chi Han, Qifan Wang, Hao Peng, Wenhan Xiong, Yu Chen, Heng Ji, and Sinong Wang. 2024. LM-Infinite: Zero-Shot Extreme Length Generalization for Large Language Models. In _Proceedings of the NAACL-HLT_ . doi:10.18653/v1/2024.naacl-long.222 

- [87] Kaiqiao Han, Tianqing Fang, Zhaowei Wang, Yangqiu Song, and Mark Steedman. [n. d.]. Concept-Reversed Winograd Schema Challenge: Evaluating and Improving Robust Reasoning in Large Language Models via Abstraction. In _Proceedings of the 2025 Conference of the Nations of the Americas_ 

Du et al. 

32 

   - _Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 2: Short Papers)_ . Association for Computational Linguistics. 

- [88] Yongchang Hao, Mengyao Zhai, Hossein Hajimirsadeghi, Sepidehsadat Hosseini, and Frederick Tung. 2025. Radar: Fast Long-Context Decoding for Any Transformer. In _The Thirteenth International Conference on Learning Representations_ . https://openreview.net/forum?id=ZTpWOwMrzQ 

- [89] Shirley Anugrah Hayati, Dongyeop Kang, Qingxiaoyang Zhu, Weiyan Shi, and Zhou Yu. 2020. INSPIRED: Toward Sociable Recommendation Dialog Systems. In _Proceedings of the EMNLP_ . doi:10.18653/v1/2020.emnlp-main.654 

- [90] Bo He, Hengduo Li, Young Kyun Jang, Menglin Jia, Xuefei Cao, Ashish Shah, Abhinav Shrivastava, and Ser-Nam Lim. 2024. Ma-lmm: Memoryaugmented large multimodal model for long-term video understanding. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . 13504–13514. 

- [91] Junqing He, Kunhao Pan, Xiaoqun Dong, Zhuoyang Song, LiuYiBo LiuYiBo, Qianguosun Qianguosun, Yuxin Liang, Hao Wang, Enming Zhang, and Jiaxing Zhang. 2024. Never Lost in the Middle: Mastering Long-Context Question Answering with Position-Agnostic Decompositional Training. In _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ . doi:10.18653/v1/2024.acl-long.736 

- [92] Yang He, Ruijie Fang, Isil Dillig, and Yuepeng Wang. 2025. Graphiti: Bridging Graph and Relational Database Queries. _arXiv preprint arXiv:2504.03182_ (2025). 

- [93] Yefei He, Luoming Zhang, and Weijia et al. Wu. 2024. ZipCache: Accurate and Efficient KV Cache Quantization with Salient Token Identification. In _NeurIPS_ . https://proceedings.neurips.cc/paper_files/paper/2024/file/7e57131fdeb815764434b65162c88895-Paper-Conference.pdf 

- [94] Zihong He, Weizhe Lin, Hao Zheng, Fan Zhang, Matt W. Jones, Laurence Aitchison, Xuhai Xu, Miao Liu, Per Ola Kristensson, and Junxiao Shen. 2024. Human-inspired Perspectives: A Survey on AI Long-term Memory. _arXiv_ (2024). https://arxiv.org/abs/2411.00489 

- [95] Xanh Ho, Anh-Khoa Nguyen Duong, Saku Sugawara, and Akiko Aizawa. 2020. Constructing a multi-hop qa dataset for comprehensive evaluation of reasoning steps. _arXiv preprint arXiv:2011.01060_ (2020). 

- [96] Ruixin Hong, Hongming Zhang, Xiaoman Pan, Dong Yu, and Changshui Zhang. 2024. Abstraction-of-Thought Makes Language Models Better Reasoners. In _Findings of the Association for Computational Linguistics: EMNLP 2024_ . Association for Computational Linguistics. doi:10.18653/v1/ 2024.findings-emnlp.110 

- [97] Wenyi Hong, Weihan Wang, Qingsong Lv, Jiazheng Xu, Wenmeng Yu, Junhui Ji, Yan Wang, Zihan Wang, Yuxuan Zhang, Juanzi Li, Bin Xu, Yuxiao Dong, Ming Ding, and Jie Tang. 2023. CogAgent: A Visual Language Model for GUI Agents. _arXiv preprint arXiv:2312.08914_ (2023). https://arxiv.org/abs/2312.08914 

- [98] Coleman Hooper, Sehoon Kim, Hiva Mohammadzadeh, Michael W. Mahoney, Yakun Sophia Shao, Kurt Keutzer, and Amir Gholami. 2024. KVQuant: Towards 10 Million Context Length LLM Inference with KV Cache Quantization. In _Advances in Neural Information Processing Systems_ . 

- [99] Lishuai Hou, Zixiong Wang, Gaoyang Liu, Chen Wang, Wei Liu, and Kai Peng. 2025. Decoupling Memories, Muting Neurons: Towards Practical Machine Unlearning for Large Language Models. In _Findings of the Association for Computational Linguistics: ACL 2025_ , Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and Mohammad Taher Pilehvar (Eds.). Association for Computational Linguistics, Vienna, Austria, 13978–13999. doi:10.18653/v1/2025.findings-acl.719 

- [100] Yuki Hou, Haruki Tamoto, and Homei Miyashita. 2024. "My agent understands me better": Integrating Dynamic Human-like Memory Recall and Consolidation in LLM-Based Agents. In _CHI Extended Abstracts_ . doi:10.1145/3613905.3650839 

- [101] Zhijian Hou, Lei Ji, Difei Gao, Wanjun Zhong, Kun Yan, Chao Li, Wing-Kwong Chan, Chong-Wah Ngo, Nan Duan, and Mike Zheng Shou. 2023. Groundnlq@ ego4d natural language queries challenge 2023. _arXiv_ (2023). https://arxiv.org/abs/2306.15255 

- [102] Chenxu Hu, Jie Fu, Chenzhuang Du, Simian Luo, Junbo Zhao, and Hang Zhao. 2023. ChatDB: Augmenting LLMs with Databases as Their Symbolic Memory. https://arxiv.org/abs/2306.03901 

- [103] Yuanzhe Hu, Yu Wang, and Julian McAuley. 2025. Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions. _arXiv preprint arXiv:2507.05257_ (2025). 

- [104] Luyang Huang, Shuyang Cao, Nikolaus Parulian, Heng Ji, and Lu Wang. 2021. Efficient Attentions for Long Document Summarization. In _Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies_ . doi:10.18653/v1/2021.naacl-main.112 

- [105] Qiushi Huang, Shuai Fu, Xubo Liu, Wenwu Wang, Tom Ko, Yu Zhang, and Lilian Tang. 2023. Learning Retrieval Augmentation for Personalized Dialogue Generation. In _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing_ . doi:10.18653/v1/2023.emnlpmain.154 

- [106] Wenyu Huang, Pavlos Vougiouklis, Mirella Lapata, and Jeff Z. Pan. 2025. Masking in Multi-hop QA: An Analysis of How Language Models Perform with Context Permutation. arXiv:2505.11754 [cs.CL] https://arxiv.org/abs/2505.11754 

- [107] Xiusheng Huang, Yequan Wang, Jun Zhao, and Kang Liu. 2024. Commonsense Knowledge Editing Based on Free-Text in LLMs. In _Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing_ . 14870–14880. 

- [108] Yunpeng Huang, Jingwei Xu, Junyu Lai, Zixu Jiang, Taolue Chen, Zenan Li, Yuan Yao, Xiaoxing Ma, Lijuan Yang, Hao Chen, et al. 2023. Advancing transformer architecture in long-context large language models: A comprehensive survey. _arXiv preprint arXiv:2311.12351_ (2023). 

- [109] Huawei Technologies Co., Ltd. 2025. _Xiaoyi: Huawei’s AI Smart Assistant_ . https://xiaoyi.huawei.com/chat/ Accessed: 2025-11-01. 

- [110] B. Ian Hutchins, Xin Yuan, and James M. et al. Anderson. 2016. Relative Citation Ratio (RCR): A New Metric That Uses Citation Rates to Measure Influence at the Article Level. _PLOS Biology_ (2016). doi:10.1371/journal.pbio.1002541 

- [111] Anysphere Inc. 2024. _Cursor: An AI-Powered Code Editor_ . https://www.cursor.sh Version 0.x, Accessed: 2025-11-01. 

Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

33 

- [112] LangChain Inc. 2025. LangGraph: Build Resilient Language Agents as Graphs. https://github.com/langchain-ai/langgraph 

- [113] Gautier Izacard, Mathilde Caron, Lucas Hosseini, Sebastian Riedel, Piotr Bojanowski, Armand Joulin, and Edouard Grave. 2021. Unsupervised dense information retrieval with contrastive learning. _arXiv_ (2021). https://arxiv.org/abs/2112.09118 

- [114] Jihyoung Jang, Minseong Boo, and Hyounghun Kim. 2023. Conversation Chronicles: Towards Diverse Temporal and Relational Dynamics in Multi-session Conversations. _arXiv preprint arXiv:2310.13420_ (2023). 

- [115] Joel Jang, Dongkeun Yoon, Sohee Yang, Sungmin Cha, Moontae Lee, Lajanugen Logeswaran, and Minjoon Seo. 2023. Knowledge Unlearning for Mitigating Privacy Risks in Language Models. In _Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , Anna Rogers, Jordan Boyd-Graber, and Naoaki Okazaki (Eds.). Association for Computational Linguistics, Toronto, Canada, 14389–14408. doi:10.18653/v1/2023.acl-long.805 

- [116] Yunah Jang, Kang-il Lee, Hyunkyung Bae, Hwanhee Lee, and Kyomin Jung. 2024. IterCQR: Iterative Conversational Query Reformulation with Retrieval Guidance. In _Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)_ . doi:10.18653/v1/2024.naacl-long.449 

- [117] Wonje Jeung, Sangyeon Yoon, and Albert No. 2025. SEPS: A Separability Measure for Robust Unlearning in LLMs. In _Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing_ , Christos Christodoulopoulos, Tanmoy Chakraborty, Carolyn Rose, and Violet Peng (Eds.). Association for Computational Linguistics, Suzhou, China, 5556–5587. doi:10.18653/v1/2025.emnlp-main.283 

- [118] Jiabao Ji, Yujian Liu, Yang Zhang, et al. 2024. Reversing the Forget-Retain Objectives: An Efficient LLM Unlearning Framework from Logit Difference. _Advances in Neural Information Processing Systems_ 37 (2024). 

- [119] Jinghan Jia, Jiancheng Liu, Yihua Zhang, Parikshit Ram, Nathalie Baracaldo, and Sijia Liu. 2024. WAGLE: Strategic Weight Attribution for Effective and Modular Unlearning in Large Language Models. In _NeurIPS_ . 

- [120] Jinghan Jia, Yihua Zhang, Yimeng Zhang, et al. 2024. SOUL: Unlocking the Power of Second-Order Optimization for LLM Unlearning. In _Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing_ . doi:10.18653/v1/2024.emnlp-main.245 

- [121] Bowen Jiang, Yuan Yuan, Maohao Shen, Zhuoqun Hao, Zhangchen Xu, Zichen Chen, Zijun Liu, Anirudh Ravi Vijjini, Jiaming He, et al. 2025. PersonaMem-v2: Towards Personalized Intelligence via Learning Implicit User Personas and Agentic Memory. _arXiv preprint arXiv:2512.06688_ (2025). 

- [122] Houcheng Jiang, Junfeng Fang, Ningyu Zhang, Mingyang Wan, Guojun Ma, Xiang Wang, Xiangnan He, and Tat-Seng Chua. 2025. AnyEdit: Edit Any Knowledge Encoded in Language Models. In _Forty-second International Conference on Machine Learning_ . https://openreview.net/forum?id= aJIoBur0Ef 

- [123] Haoyun Jiang, Haolin li, jianwei zhang, Fei Huang, Qiang Hu, Minmin Sun, Shuai Xiao, Yong Li, Junyang Lin, and Jiangchao Yao. 2025. CateKV: On Sequential Consistency for Long-Context LLM Inference Acceleration. In _Forty-second International Conference on Machine Learning_ . https: //openreview.net/forum?id=u7dlwgKstN 

- [124] Huiqiang Jiang, Qianhui Wu, Chin-Yew Lin, Yuqing Yang, and Lili Qiu. 2023. LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models. In _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing_ . doi:10.18653/v1/2023.emnlp-main.825 

- [125] Huiqiang Jiang, Qianhui Wu, Xufang Luo, Dongsheng Li, Chin-Yew Lin, Yuqing Yang, and Lili Qiu. 2024. LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression. In _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ . doi:10.18653/v1/2024.acl-long.91 

- [126] Xun Jiang, Feng Li, Han Zhao, Jiaying Wang, Jun Shao, Shihao Xu, Shu Zhang, Weiling Chen, Xavier Tang, Yize Chen, Mengyue Wu, Weizhi Ma, Mengdi Wang, and Tianqiao Chen. 2024. Long Term Memory: The Foundation of AI Self-Evolution. _arXiv_ (2024). https://arxiv.org/abs/2410.15665 

- [127] Yikun Jiang, Huanyu Wang, and Lei et al. Xie. 2024. D-LLM: A Token Adaptive Computing Resource Allocation Strategy for Large Language Models. In _NeurIPS_ . https://proceedings.neurips.cc/paper_files/paper/2024/file/03469b1a66e351b18272be23baf3b809-Paper-Conference.pdf 

- [128] Yuxin Jiang, Yufei Wang, Chuhan Wu, Wanjun Zhong, Xingshan Zeng, Jiahui Gao, Liangyou Li, Xin Jiang, Lifeng Shang, Ruiming Tang, Qun Liu, and Wei Wang. 2024. Learning to Edit: Aligning LLMs with Knowledge Editing. In _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , Lun-Wei Ku, Andre Martins, and Vivek Srikumar (Eds.). Association for Computational Linguistics, Bangkok, Thailand, 4689–4705. doi:10.18653/v1/2024.acl-long.258 

- [129] Zhengbao Jiang, Frank Xu, Luyu Gao, Zhiqing Sun, Qian Liu, Jane Dwivedi-Yu, Yiming Yang, Jamie Callan, and Graham Neubig. 2023. Active Retrieval Augmented Generation. In _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing_ . doi:10.18653/v1/2023.emnlpmain.495 

- [130] Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik R Narasimhan. 2024. SWE-bench: Can Language Models Resolve Real-world GitHub Issues?. In _ICLR_ . https://openreview.net/forum?id=VTF8yNQM66 

- [131] Bowen Jin, Jinsung Yoon, Jiawei Han, and Sercan O Arik. 2025. Long-Context LLMs Meet RAG: Overcoming Challenges for Long Inputs in RAG. In _The Thirteenth International Conference on Learning Representations_ . https://openreview.net/forum?id=oU3tpaR8fm 

- [132] Mingyu Jin, Weidi Luo, and Sitao et al. Cheng. 2024. Disentangling Memory and Reasoning Ability in Large Language Models. _arXiv preprint arXiv:2411.13504_ (2024). 

- [133] Zhuoran Jin, Pengfei Cao, Chenhao Wang, Zhitao He, Hongbang Yuan, Jiachun Li, Yubo Chen, Kang Liu, and Jun Zhao. 2024. RWKU: Benchmarking Real-World Knowledge Unlearning for Large Language Models. In _NeurIPS Datasets and Benchmarks Track_ . https://openreview.net/forum?id= wOmtZ5FgMH 

Du et al. 

34 

- [134] Mandar Joshi, Eunsol Choi, Daniel Weld, and Luke Zettlemoyer. 2017. TriviaQA: A Large Scale Distantly Supervised Challenge Dataset for Reading Comprehension. In _Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ . doi:10.18653/v1/P17-1147 

- [135] Gregory Kamradt. 2023. Needle In A Haystack - Pressure Testing LLMs. https://github.com/gkamradt/LLMTest_NeedleInAHaystack. 

- [136] Christopher Kiley and Colleen M Parks. 2022. Mechanisms of memory updating: State dependency vs. reconsolidation. _Journal of cognition_ (2022). 

- [137] Jiho Kim, Woosog Chay, Hyeonji Hwang, Daeun Kyung, Hyunseung Chung, Eunbyeol Cho, Yohan Jo, and Edward Choi. 2024. DialSim: A Real-Time Simulator for Evaluating Long-Term Multi-Party Dialogue Understanding of Conversational Agents. _arXiv preprint arXiv:2406.13144_ (2024). 

- [138] Minsoo Kim, Kyuhong Shim, Jungwook Choi, and Simyung Chang. 2024. InfiniPot: Infinite Context Processing on Memory-Constrained LLMs. In _EMNLP_ . doi:10.18653/v1/2024.emnlp-main.897 

- [139] Seo Hyun Kim, Keummin Ka, Yohan Jo, Seung-won Hwang, Dongha Lee, and Jinyoung Yeo. 2024. Ever-Evolving Memory by Blending and Refining the Past. _arXiv_ (2024). https://arxiv.org/abs/2403.04787 

- [140] kingjulio8238. 2025. Memary. https://github.com/kingjulio8238/Memary 

- [141] James Kirkpatrick, Razvan Pascanu, Neil Rabinowitz, et al. 2017. Overcoming Catastrophic Forgetting in Neural Networks. _Proceedings of the National Academy of Sciences_ 114, 13 (2017). 

- [142] Hideo Kobayashi, Wuwei Lan, Peng Shi, Shuaichen Chang, Jiang Guo, Henghui Zhu, Zhiguo Wang, and Patrick Ng. 2025. You Only Read Once (YORO): Learning to Internalize Database Knowledge for Text-to-SQL. In _Proceedings of NAACL-HLT (Long Papers)_ . 1889–1901. https: //aclanthology.org/2025.naacl-long.94/ 

- [143] Tom’aš Kočisk’y, Jonathan Schwarz, Phil Blunsom, Chris Dyer, Karl Moritz Hermann, G’abor Melis, and Edward Grefenstette. 2018. The NarrativeQA Reading Comprehension Challenge. _Transactions of the Association for Computational Linguistics_ (2018). doi:10.1162/tacl_a_00023 

- [144] Dharshan Kumaran, Demis Hassabis, and James L McClelland. 2016. What learning systems do intelligent agents need? Complementary learning systems theory updated. _Trends in Cognitive Sciences_ (2016). 

- [145] Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh, Chris Alberti, Danielle Epstein, Illia Polosukhin, Jacob Devlin, Kenton Lee, et al. 2019. Natural questions: a benchmark for question answering research. _Transactions of the Association for Computational Linguistics_ (2019). 

- [146] Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E. Gonzalez, Hao Zhang, and Ion Stoica. 2023. Efficient Memory Management for Large Language Model Serving with PagedAttention. In _Proceedings of the ACM SIGOPS 29th Symposium on Operating Systems Principles_ . 

- [147] Jack Lanchantin, Shubham Toshniwal, and Jason et al. Weston. 2023. Learning to Reason and Memorize with Self-Notes. _NeurIPS_ (2023). 

- [148] Dongkyu Lee, Chandana Satya Prakash, Jack FitzGerald, and Jens Lehmann. 2024. MATTER: Memory-Augmented Transformer Using Heterogeneous Knowledge Sources. In _Findings of the ACL_ . https://aclanthology.org/2024.findings-acl.953 

- [149] Kuang-Huei Lee, Xinyun Chen, Hiroki Furuta, John Canny, and Ian Fischer. 2024. A Human-Inspired Reading Agent with Gist Memory of Very Long Contexts. In _Proceedings of the 41st International Conference on Machine Learning_ . https://proceedings.mlr.press/v235/lee24c.html 

- [150] Mingcong Lei, Yiming Zhao, Ge Wang, Zhixin Mai, Shuguang Cui, Yatong Han, and Jinke Ren. 2025. STMA: A Spatio-Temporal Memory Agent for Long-Horizon Embodied Task Planning. _arXiv_ (2025). 

- [151] Yaniv Leviathan, Matan Kalman, and Yossi Matias. 2025. Selective Attention Improves Transformer. In _ICLR_ . https://openreview.net/forum?id= v0FzmPCd1e 

- [152] Omer Levy, Minjoon Seo, Eunsol Choi, et al. 2017. Zero-shot Relation Extraction via Reading Comprehension. In _Proceedings of CoNLL_ . 

- [153] Hao Li, Chenghao Yang, An Zhang, Yang Deng, Xiang Wang, and Tat-Seng Chua. 2024. Hello again! llm-powered personalized agent for long-term dialogue. _arXiv preprint arXiv:2406.05925_ (2024). 

- [154] Jiaqi Li, Mengmeng Wang, Zilong Zheng, and Muhan Zhang. 2024. LooGLE: Can Long-Context Language Models Understand Long Contexts?. In _ACL_ . 16304–16333. doi:10.18653/v1/2024.acl-long.859 

- [155] Ji-An Li, Corey Zhou, Marcus Benna, and Marcelo G Mattar. 2024. Linking In-Context Learning in Transformers to Human Episodic Memory. _Advances in Neural Information Processing Systems_ 37 (2024), 6180–6212. 

- [156] Nathaniel Li, Alexander Pan, Anjali Gopal, Summer Yue, Daniel Berrios, Alice Gatti, Justin D Li, Ann-Kathrin Dombrowski, Shashwat Goel, Gabriel Mukobi, et al. 2024. The WMDP benchmark: measuring and reducing malicious use with unlearning. In _Proceedings of the 41st International Conference on Machine Learning_ . 28525–28550. 

- [157] Na Li, Chunyi Zhou, Yansong Gao, Hui Chen, Zhi Zhang, Boyu Kuang, and Anmin Fu. 2025. Machine Unlearning: Taxonomy, Metrics, Applications, Challenges, and Prospects. _IEEE Transactions on Neural Networks and Learning Systems_ (2025). doi:10.1109/TNNLS.2025.3530988 

- [158] Shilong Li, Yancheng He, Hangyu Guo, Xingyuan Bu, Ge Bai, Jie Liu, Jiaheng Liu, Xingwei Qu, Yangguang Li, Wanli Ouyang, Wenbo Su, and Bo Zheng. 2024. GraphReader: Building Graph-based Agent to Enhance Long-Context Abilities of Large Language Models. In _Findings of the Association for Computational Linguistics: EMNLP 2024_ . doi:10.18653/v1/2024.findings-emnlp.746 

- [159] Xiaopeng Li, Shasha Li, Shezheng Song, Jing Yang, Jun Ma, and Jie Yu. 2024. Pmet: Precise model editing in a transformer. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , Vol. 38. 18564–18572. 

- [160] Xiaonan Li and Xipeng Qiu. 2023. MoT: Memory-of-Thought Enables ChatGPT to Self-Improve. In _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing_ . doi:10.18653/v1/2023.emnlp-main.392 

Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

35 

- [161] Xingxuan Li, Ruochen Zhao, Yew Ken Chia, Bosheng Ding, Shafiq Joty, Soujanya Poria, and Lidong Bing. 2024. Chain-of-Knowledge: Grounding Large Language Models via Dynamic Knowledge Adapting over Heterogeneous Sources. In _International Conference on Learning Representations_ . https://arxiv.org/abs/2305.13269 

- [162] Yucheng Li, Bo Dong, and Frank et al. Guerin. 2023. Compressing Context to Enhance Inference Efficiency of Large Language Models. In _EMNLP_ . doi:10.18653/v1/2023.emnlp-main.391 

- [163] Yuhong Li, Yingbing Huang, Bowen Yang, Bharat Venkitesh, Acyr Locatelli, Hanchen Ye, Tianle Cai, Patrick Lewis, and Deming Chen. 2024. SnapKV: LLM Knows What You are Looking for Before Generation. In _Advances in Neural Information Processing Systems_ , Vol. 37. 22947–22970. https://proceedings.neurips.cc/paper_files/paper/2024/file/28ab418242603e0f7323e54185d19bde-Paper-Conference.pdf 

- [164] Yongqi Li, Wenjie Wang, Leigang Qu, Liqiang Nie, Wenjie Li, and Tat-Seng Chua. 2024. Generative Cross-Modal Retrieval: Memorizing Images in Multimodal Language Models for Retrieval and Beyond. In _Proceedings of the ACL_ . doi:10.18653/v1/2024.acl-long.639 

- [165] Zhuoqun Li, Xuanang Chen, Haiyang Yu, Hongyu Lin, Yaojie Lu, Qiaoyu Tang, Fei Huang, Xianpei Han, Le Sun, and Yongbin Li. 2024. Structrag: Boosting knowledge intensive reasoning of LLMs via inference-time hybrid information structurization. In _The Thirteenth International Conference on Learning Representations_ . 

- [166] Zhuowan Li, Cheng Li, Mingyang Zhang, Qiaozhu Mei, and Michael Bendersky. 2024. Retrieval Augmented Generation or Long-Context LLMs? A Comprehensive Study and Hybrid Approach. In _Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing: Industry Track_ . doi:10.18653/v1/2024.emnlp-industry.66 

- [167] Zongqian Li, Yinhong Liu, Yixuan Su, and Nigel Collier. 2024. Prompt compression for large language models: A survey. _arXiv preprint arXiv:2410.12388_ (2024). 

- [168] Zhiyu Li, Shichao Song, Hanyu Wang, Simin Niu, Ding Chen, Jiawei Yang, Chenyang Xi, Huayi Lai, Jihao Zhao, Yezhaohui Wang, et al. 2025. MemOS: An Operating System for Memory-Augmented Generation (MAG) in Large Language Models. _arXiv preprint arXiv:2505.22101_ (2025). 

- [169] Zaijing Li, Yuquan Xie, Rui Shao, et al. 2024. Optimus-1: Hybrid Multimodal Memory Empowered Agents Excel in Long-horizon Tasks. _arXiv preprint arXiv:2408.03615_ (2024). 

- [170] Greg Linden, Brent Smith, and Jeremy York. 2003. Amazon.com Recommendations: Item-to-Item Collaborative Filtering. _IEEE Internet Computing_ 7, 1 (2003), 76–80. 

- [171] Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, et al. 2024. Deepseek-v3 technical report. _arXiv preprint arXiv:2412.19437_ (2024). 

- [172] Akide Liu, Jing Liu, and Zizheng et al. Pan. 2024. MiniCache: KV Cache Compression in Depth Dimension for Large Language Models. In _NeurIPS_ . https://proceedings.neurips.cc/paper_files/paper/2024/file/fd0705710bf01b88a60a3d479ea341d9-Paper-Conference.pdf 

- [173] Chris Liu, Yaxuan Wang, Jeffrey Flanigan, et al. 2024. Large Language Model Unlearning via Embedding-corrupted Prompts. _Advances in Neural Information Processing Systems_ 37 (2024). 

- [174] Di Liu, Meng Chen, Baotong Lu, Huiqiang Jiang, Zhenhua Han, Qianxi Zhang, Qi Chen, Chengruidong Zhang, Bailu Ding, Kai Zhang, Chen Chen, Fan Yang, Yuqing Yang, and Lili Qiu. 2024. RetrievalAttention: Accelerating Long-Context LLM Inference via Vector Retrieval. https: //arxiv.org/abs/2409.10516 

- [175] Jerry Liu. 2022. LlamaIndex. https://www.llamaindex.ai 

- [176] Junyi Liu, Liangzhi Li, and Tong et al. Xiang. 2023. TCRA-LLM: Token Compression Retrieval Augmented Large Language Model for Inference Cost Reduction. In _EMNLP Findings_ . doi:10.18653/v1/2023.findings-emnlp.655 

- [177] Jiahong Liu, Zexuan Qiu, Zhongyang Li, Quanyu Dai, Jieming Zhu, Minda Hu, Menglin Yang, and Irwin King. 2025. A Survey of Personalized Large Language Models: Progress and Future Directions. _arXiv preprint arXiv:2502.11528_ (2025). 

- [178] Minqian Liu, Shiyu Chang, and Lifu Huang. 2022. Incremental prompting: Episodic memory prompt for lifelong event detection. _arXiv_ (2022). https://arxiv.org/abs/2204.07275 

- [179] Nelson F Liu, Kevin Lin, John Hewitt, et al. 2024. Lost in the Middle: How Language Models Use Long Contexts. _Transactions of the Association for Computational Linguistics_ 12 (2024). 

- [180] Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. 2024. Lost in the Middle: How Language Models Use Long Contexts. _Transactions of the Association for Computational Linguistics_ (2024). doi:10.1162/tacl_a_00638 

- [181] Shuai Liu, Hyundong Cho, Marjorie Freedman, Xuezhe Ma, and Jonathan May. 2023. RECAP: Retrieval-Enhanced Context-Aware Prefix Encoder for Personalized Dialogue Response Generation. In _Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ . doi:10.18653/v1/2023.acl-long.468 

- [182] Shuai Liu, Hyundong J Cho, Marjorie Freedman, Xuezhe Ma, and Jonathan May. 2023. RECAP: retrieval-enhanced context-aware prefix encoder for personalized dialogue response generation. _arXiv preprint arXiv:2306.07206_ (2023). 

- [183] WenTao Liu, Ruohua Zhang, and Aimin et al. Zhou. 2025. Echo: A Large Language Model with Temporal Episodic Memory. _arXiv preprint arXiv:2502.16090_ (2025). 

- [184] Zichang Liu, Aditya Desai, Fangshuo Liao, Weitao Wang, Victor Xie, Zhaozhuo Xu, Anastasios Kyrillidis, and Anshumali Shrivastava. 2023. Scissorhands: Exploiting the Persistence of Importance Hypothesis for LLM KV Cache Compression at Test Time. In _NeurIPS_ . https://openreview. net/forum?id=JZfg6wGi6g 

- [185] Zheyuan Liu, Guangyao Dou, Zhaoxuan Tan, Yijun Tian, and Meng Jiang. 2024. Towards Safer Large Language Models through Machine Unlearning. In _Findings of the Association for Computational Linguistics: ACL 2024_ . 1817–1829. 

Du et al. 

36 

- [186] Zhenghao Liu, Chenyan Xiong, Yuanhuiyi Lv, Zhiyuan Liu, and Ge Yu. 2023. Universal Vision-Language Dense Retrieval: Learning A Unified Representation Space for Multi-Modal Retrieval. In _Proceedings of ICLR_ . 

- [187] Ziyao Liu, Huanyi Ye, Chen Chen, Yongsen Zheng, and Kwok-Yan Lam. 2025. Threats, Attacks, and Defenses in Machine Unlearning: A Survey. _IEEE Open Journal of the Computer Society_ (2025). doi:10.1109/OJCS.2025.3543483 

- [188] Zirui Liu, Jiayi Yuan, Hongye Jin, Shaochen Zhong, Zhaozhuo Xu, Vladimir Braverman, Beidi Chen, and Xia Hu. 2024. KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache. In _International Conference on Machine Learning_ . https://proceedings.mlr.press/v235/liu24bz.html 

- [189] Lin Long, Yichen He, Wentao Ye, Yiyuan Pan, Yuan Lin, Hang Li, Junbo Zhao, and Wei Li. 2025. Seeing, Listening, Remembering, and Reasoning: A Multimodal Agent with Long-Term Memory. arXiv:2508.09736 [cs.CV] https://arxiv.org/abs/2508.09736 

- [190] Junru Lu, Siyu An, and Mingbao et al. Lin. 2023. Memochat: Tuning LLMs to Use Memos for Consistent Long-range Open-domain Conversation. _arXiv preprint arXiv:2308.08239_ (2023). 

- [191] Luka, Inc. 2025. Replika: The AI companion who cares. https://replika.com/. Accessed: 2025-05-14. 

- [192] Elias Lumer, Anmol Gulati, Vamse Kumar Subbiah, Pradeep Honaganahalli Basavaraju, and James A Burke. 2025. MemTool: Optimizing Short-Term Memory Management for Dynamic Tool Calling in LLM Agent Multi-Turn Conversations. _arXiv preprint arXiv:2507.21428_ (2025). 

- [193] Kun Luo, Zheng Liu, Shitao Xiao, Tong Zhou, Yubo Chen, Jun Zhao, and Kang Liu. 2024. Landmark Embedding: A Chunking-Free Embedding Method For Retrieval Augmented Long-Context Large Language Models. In _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ . doi:10.18653/v1/2024.acl-long.180 

- [194] Zhiyuan Ma, Jianjun Li, Guohui Li, and Yongjing Cheng. 2022. UniTranSeR: A Unified Transformer Semantic Representation Framework for Multimodal Task-Oriented Dialog System. In _Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ . doi:10.18653/v1/2022.acl-long.9 

- [195] Aru Maekawa, Hidetaka Kamigaito, Kotaro Funakoshi, and Manabu Okumura. 2023. Generative replay inspired by hippocampal memory indexing for continual language learning. In _Proceedings of the 17th Conference of the European Chapter of the Association for Computational Linguistics_ . 

- [196] Adyasha Maharana, Dong-Ho Lee, Sergey Tulyakov, et al. 2024. Evaluating Very Long-term Conversational Memory of LLM Agents. _arXiv preprint arXiv:2402.17753_ (2024). 

- [197] Pratyush Maini, Zhili Feng, Avi Schwarzschild, Zachary Chase Lipton, and J Zico Kolter. 2024. TOFU: A Task of Fictitious Unlearning for LLMs. In _First Conference on Language Modeling_ . https://openreview.net/forum?id=B41hNBoWLo 

- [198] Karttikeya Mangalam, Raiymbek Akshulakov, and Jitendra Malik. 2023. EgoSchema: A Diagnostic Benchmark for Very Long-form Video Language Understanding. In _Advances in Neural Information Processing Systems (NeurIPS)_ . 

- [199] James L McClelland, Bruce L McNaughton, and Randall C O’Reilly. 1995. Why there are complementary learning systems in the hippocampus and neocortex: Insights from the successes and failures of connectionist models of learning and memory. _Psychological Review_ (1995). 

- [200] Sanket Vaibhav Mehta, Jai Gupta, Yi Tay, Mostafa Dehghani, Vinh Q Tran, Jinfeng Rao, Marc Najork, Emma Strubell, and Donald Metzler. 2022. DSI++: Updating transformer memory with new documents. _arXiv preprint arXiv:2212.09744_ (2022). 

- [201] Daniel Mela, Aitor González-Agirre, Javier Hernando, and Marta Villegas. 2024. Mass-Editing Memory with Attention in Transformers: A cross-lingual exploration of knowledge. In _Findings of the Association for Computational Linguistics: ACL 2024_ . 5831–5847. 

- [202] memodb io. 2025. Memobase: Profile-Based Long-Term Memory for AI Applications. https://github.com/memodb-io/memobase 

- [203] Kevin Meng, David Bau, Alex Andonian, et al. 2022. Locating and Editing Factual Associations in GPT. _Advances in Neural Information Processing Systems_ 35 (2022). 

- [204] Kevin Meng, Arnab Sen Sharma, Alex Andonian, et al. 2022. Mass-editing Memory in a Transformer. _arXiv preprint arXiv:2210.07229_ (2022). 

- [205] Kevin Meng, Arnab Sen Sharma, Alex J Andonian, Yonatan Belinkov, and David Bau. 2023. Mass-Editing Memory in a Transformer. In _The Eleventh International Conference on Learning Representations_ . https://openreview.net/forum?id=MkbcAHIYgyS 

- [206] Stephen Merity, Caiming Xiong, James Bradbury, and Richard Socher. 2017. Pointer Sentinel Mixture Models. In _International Conference on Learning Representations_ . https://openreview.net/forum?id=Byj72udxe 

- [207] Xin Miao, Yongqi Li, Shen Zhou, and Tieyun Qian. 2024. Episodic Memory Retrieval from LLMs: A Neuromorphic Mechanism to Generate Commonsense Counterfactuals for Relation Extraction. In _Findings of ACL_ . 2489–2511. 

- [208] Julie Michelman, Nasrin Baratalipour, and Matthew Abueg. 2025. Enhancing Reasoning with Collaboration and Memory. _arXiv preprint arXiv:2503.05944_ (2025). 

- [209] Mindverse AI. 2025. Me.bot: Your AI Second Brain. https://www.me.bot/ Accessed: 2025-05-23. 

- [210] Marvin Minsky. 1980. K-Lines: A theory of memory. _Cognitive Science_ (1980). doi:10.1016/S0364-0213(80)80014-0 

- [211] Eric Mitchell, Charles Lin, Antoine Bosselut, Chelsea Finn, and Christopher D Manning. 2022. Fast Model Editing at Scale. In _International Conference on Learning Representations_ . https://openreview.net/forum?id=0DcZxeWfOPt 

- [212] Eric Mitchell, Charles Lin, Antoine Bosselut, Christopher D Manning, and Chelsea Finn. 2022. Memory-based model editing at scale. In _International Conference on Machine Learning_ . PMLR, 15817–15831. 

- [213] Andrei Ioan Muresanu, Anvith Thudi, Michael R. Zhang, and Nicolas Papernot. 2025. Fast Exact Unlearning for In-Context Learning Data for LLMs. In _Forty-second International Conference on Machine Learning_ . https://openreview.net/forum?id=TzNVZEsqTi 

- [214] Mahmud Wasif Nafee, Maiqi Jiang, Haipeng Chen, and Yanfu Zhang. 2025. Dynamic Retriever for In-Context Knowledge Editing via Policy Optimization. In _Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing_ , Christos Christodoulopoulos, Tanmoy Chakraborty, Carolyn Rose, and Violet Peng (Eds.). Association for Computational Linguistics, Suzhou, China, 16755–16768. doi:10.18653/v1/2025. 

37 

# Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

emnlp-main.848 

- [215] Ramesh Nallapati, Bowen Zhou, Cicero dos Santos, Çağlar Gu�lçehre, and Bing Xiang. 2016. Abstractive Text Summarization using Sequence-tosequence RNNs and Beyond. In _Proceedings of the 20th SIGNLL Conference on Computational Natural Language Learning_ . doi:10.18653/v1/K16-1028 

- [216] Neo4j. 2012. Neo4j - The World’s Leading Graph Database. https://neo4j.com/ 

- [217] NevaMind-AI. 2025. MemU: An open-source memory framework for AI companions. https://github.com/NevaMind-AI/memU. Accessed: October 29, 2025. 

- [218] Cam-Van Thi Nguyen, Anh-Tuan Mai, and The-Son et al. Le. 2023. Conversation Understanding using Relational Temporal Graph Neural Networks with Auxiliary Cross-Modality Interaction. In _EMNLP_ . doi:10.18653/v1/2023.emnlp-main.937 

- [219] Yuxiang Nie, Heyan Huang, Wei Wei, and Xian-Ling Mao. 2022. Capturing Global Structural Information in Long Document Question Answering with Compressive Graph Selector Network. In _Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing_ . doi:10. 18653/v1/2022.emnlp-main.336 

- [220] Cicero Nogueira dos Santos, James Lee-Thorp, Isaac Noble, Chung-Ching Chang, and David Uthus. 2024. Memory Augmented Language Models through Mixture of Word Experts. In _Proceedings of the NAACL-HLT_ . doi:10.18653/v1/2024.naacl-long.249 

- [221] Barlas Oguz, Xilun Chen, Vladimir Karpukhin, Stan Peshterliev, Dmytro Okhonko, Michael Schlichtkrull, Sonal Gupta, Yashar Mehdad, and Scott Yih. 2022. UniK-QA: Unified Representations of Structured and Unstructured Knowledge for Open-Domain Question Answering. In _Findings of the Association for Computational Linguistics: NAACL 2022_ . doi:10.18653/v1/2022.findings-naacl.115 

- [222] Kai Tzu-iunn Ong, Namyoung Kim, Minju Gwak, Hyungjoo Chae, Taeyoon Kwon, Yohan Jo, Seung-won Hwang, Dongha Lee, and Jinyoung Yeo. 2025. Towards Lifelong Dialogue Agents via Timeline-based Memory Management. In _Proceedings of the 2025 NAACL-HLT_ . https: //arxiv.org/abs/2406.10996 

- [223] OpenAI. 2022. Chatgpt: Optimizing language models for dialogue. https://openai.com/blog/chatgpt 

- [224] OpenAI. 2025. OpenAI Platform Documentation: Embeddings Guide. https://platform.openai.com/docs/guides/embeddings 

- [225] Siru Ouyang, Jun Yan, I-Hung Hsu, Yanfei Chen, Ke Jiang, Zifeng Wang, Rujun Han, Long T. Le, Samira Daruki, Xiangru Tang, Vishy Tirumalashetty, George Lee, Mahsan Rofouei, Hangfei Lin, Jiawei Han, Chen-Yu Lee, and Tomas Pfister. 2025. ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory. _arXiv preprint_ arXiv:2509.25140 (2025). https://arxiv.org/abs/2509.25140 

- [226] Charles Packer, Vivian Fang, Shishir G Patil, et al. 2023. MemGPT: Towards LLMs as Operating Systems. _arXiv preprint arXiv:2310.00000_ (2023). 

- [227] Zhuoshi Pan, Qianhui Wu, Huiqiang Jiang, Menglin Xia, Xufang Luo, Jue Zhang, Qingwei Lin, Victor Rühle, Yuqing Yang, Chin-Yew Lin, H. Vicky Zhao, Lili Qiu, and Dongmei Zhang. 2024. LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression. In _Findings of the ACL_ . doi:10.18653/v1/2024.findings-acl.57 

- [228] Joon Sung Park, Joseph O’Brien, Carrie Jun Cai, Meredith Ringel Morris, Percy Liang, and Michael S Bernstein. 2023. Generative Agents: Interactive Simulacra of Human Behavior. In _Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology_ . 1–22. 

- [229] Shishir G. Patil, Fanjia Yan, Tianjun Zhang, Siddharth Jha, Pranav Gade, and Joseph E. Gonzalez. 2024. The Berkeley Function Calling Leaderboard: From Tool Use to Agentic Evaluation of Large Language Models. In _The Thirty-eighth Annual Conference on Neural Information Processing Systems (NeurIPS)_ . https://openreview.net/forum?id=2GmDdhBdDk 

- [230] Martin Pawelczyk, Seth Neel, and Himabindu Lakkaraju. 2023. In-context Unlearning: Language Models as Few-shot Unlearners. _arXiv preprint arXiv:2310.07579_ (2023). 

- [231] Martin Pawelczyk, Seth Neel, and Himabindu Lakkaraju. 2024. In-Context Unlearning: Language Models as Few-Shot Unlearners. In _International Conference on Machine Learning_ . PMLR, 40034–40050. 

- [232] Mathis Pink, Qinyuan Wu, Vy Ai Vo, Javier Turek, Jianing Mu, Alexander Huth, and Mariya Toneva. 2025. Position: Episodic Memory is the Missing Piece for Long-Term LLM Agents. _arXiv preprint arXiv:2502.06975_ (2025). 

- [233] USVSN Sai Prashanth, Alvin Deng, Kyle O’Brien, et al. 2024. Recite, Reconstruct, Recollect: Memorization in LMs as a Multifaceted Phenomenon. _arXiv preprint arXiv:2406.17746_ (2024). 

- [234] Hongjin Qian, Peitian Zhang, Zheng Liu, Kelong Mao, and Zhicheng Dou. 2024. Memorag: Moving towards next-gen rag via memory-inspired knowledge discovery. _arXiv preprint arXiv:2409.05591_ (2024). 

- [235] Zhangcheng Qiang, Weiqing Wang, and Kerry Taylor. 2023. Agent-OM: Leveraging LLM Agents for Ontology Matching. _arXiv preprint arXiv:2312.00326_ (2023). 

- [236] Yujia Qin, Yining Ye, Junjie Fang, Haoming Wang, Shihao Liang, Shizuo Tian, Junda Zhang, Jiahao Li, Yunxin Li, Shijue Huang, Wanjun Zhong, Kuanye Li, Jiale Yang, Yu Miao, Woyu Lin, Longxiang Liu, Xu Jiang, Qianli Ma, Jingyu Li, Xiaojun Xiao, Kai Cai, Chuang Li, Yaowei Zheng, Chaolin Jin, Chen Li, Xiao Zhou, Minchao Wang, Haoli Chen, Zhaojian Li, Haihua Yang, Haifeng Liu, Feng Lin, Tao Peng, Xin Liu, and Guang Shi. 2025. UI-TARS: Pioneering Automated GUI Interaction with Native Agents. _arXiv preprint arXiv:2501.12326_ (2025). https://arxiv.org/abs/2501.12326 

- [237] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, Gretchen Krueger, and Ilya Sutskever. 2021. Learning Transferable Visual Models From Natural Language Supervision. In _International Conference on Machine Learning_ . https://proceedings.mlr.press/v139/radford21a.html 

- [238] Jack W. Rae, Anna Potapenko, Siddhant M. Jayakumar, Chloe Hillier, and Timothy P. Lillicrap. 2020. Compressive Transformers for Long-Range Sequence Modelling. In _International Conference on Learning Representations_ . https://openreview.net/forum?id=SylKikSYDH 

- [239] Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais, Jack Ryan, and Daniel Chalef. 2025. Zep: A Temporal Knowledge Graph Architecture for Agent Memory. _arXiv preprint arXiv:2501.13956_ (2025). 

Du et al. 

38 

- [240] Abhinav Rastogi, Xiaoxue Zang, Srinivas Sunkara, Raghav Gupta, and Pranav Khaitan. 2020. Towards scalable multi-domain conversational agents: The schema-guided dialogue dataset. In _AAAI Conference on Artificial Intelligence_ . 

- [241] Mathieu Ravaut, Aixin Sun, Nancy Chen, and Shafiq Joty. 2024. On Context Utilization in Summarization with Large Language Models. In _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ . doi:10.18653/v1/2024.acl-long.153 

- [242] Steven Ritter, Jane X Wang, Zeb Kurth-Nelson, Siddhant Jayakumar, Charles Blundell, and Timothy Lillicrap. 2018. Meta-learning through Hebbian plasticity in random networks. In _Advances in Neural Information Processing Systems (NeurIPS)_ . 

- [243] Stephen E Robertson, Steve Walker, Susan Jones, Micheline M Hancock-Beaulieu, Mike Gatford, et al. 1995. Okapi at TREC-3. _Nist Special Publication Sp_ (1995). 

- [244] Ali Safaya and Deniz Yuret. 2024. Neurocache: Efficient Vector Retrieval for Long-range Language Modeling. In _Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)_ . doi:10.18653/ v1/2024.naacl-long.50 

- [245] Rana Salama, Jason Cai, and Michelle et al. Yuan. 2025. MemInsight: Autonomous Memory Augmentation for LLM Agents. _arXiv preprint arXiv:2503.21760_ (2025). 

- [246] Alireza Salemi, Sheshera Mysore, Michael Bendersky, and Hamed Zamani. 2023. Lamp: When large language models meet personalization. _arXiv preprint arXiv:2304.11406_ (2023). 

- [247] Mohammad Reza Samsami, Artem Zholus, Janarthanan Rajendran, and Sarath Chandar. 2024. Mastering Memory Tasks with World Models. In _International Conference on Learning Representations_ . https://openreview.net/forum?id=1vDArHJ68h 

- [248] Gabriel Sarch, Lawrence Jang, Michael Tarr, William W Cohen, Kenneth Marino, and Katerina Fragkiadaki. 2024. Vlm agents generate their own memories: Distilling experience into embodied programs of thought. _Advances in Neural Information Processing Systems_ (2024). 

- [249] Utkarsh Saxena, Gobinda Saha, Sakshi Choudhary, and Kaushik Roy. 2024. Eigen Attention: Attention in Low-Rank Space for KV Cache Compression. In _Findings of EMNLP_ . 15332–15344. doi:10.18653/v1/2024.findings-emnlp.899 

- [250] Ying Sheng, Lianmin Zheng, Binhang Yuan, Zhuohan Li, Max Ryabinin, Beidi Chen, Percy Liang, Christopher Ré, Ion Stoica, and Ce Zhang. 2023. FlexGen: high-throughput generative inference of large language models with a single GPU. In _International Conference on Machine Learning_ . https://github.com/FMInference/FlexGen 

- [251] Dachuan Shi, Yonggan Fu, Xiangchi Yuan, Zhongzhi Yu, Haoran You, Sixu Li, Xin Dong, Jan Kautz, Pavlo Molchanov, and Yingyan Celine Lin. 2025. LaCache: Ladder-Shaped KV Caching for Efficient Long-Context Modeling of Large Language Models. In _Forty-second International Conference on Machine Learning_ . https://openreview.net/forum?id=SDjZtxDo35 

- [252] Freda Shi, Xinyun Chen, Kanishka Misra, Nathan Scales, David Dohan, Ed H. Chi, Nathanael Schärli, and Denny Zhou. 2023. Large Language Models Can Be Easily Distracted by Irrelevant Context. In _International Conference on Machine Learning_ . https://proceedings.mlr.press/v202/shi23a.html 

- [253] Haizhou Shi and Hao Wang. 2023. A unified approach to domain incremental learning with memory: Theory and algorithm. _Advances in Neural Information Processing Systems_ (2023). 

- [254] Weijia Shi, Jaechan Lee, Yangsibo Huang, et al. 2024. MUSE: Machine Unlearning Six-way Evaluation for Language Models. _arXiv preprint arXiv:2407.06460_ (2024). 

- [255] Taranjeet Singh and Deshraj Yadav. 2024. Mem0: The Memory Layer for your AI agents. https://github.com/mem0ai/mem0 

- [256] Enxin Song, Wenhao Chai, Guanhong Wang, Yucheng Zhang, Haoyang Zhou, Feiyang Wu, Haozhe Chi, Xun Guo, Tian Ye, Yanting Zhang, et al. 2024. MovieChat: From Dense Token to Sparse Memory for Long Video Understanding. In _CVPR_ . 18221–18232. 

- [257] Woomin Song, Seunghyuk Oh, and Sangwoo et al. Mo. 2024. Hierarchical Context Merging: Better Long Context Understanding for Pre-trained LLMs. In _ICLR_ . https://openreview.net/forum?id=ulaUJFd96G 

- [258] Larry R Squire, Lisa Genzel, John T Wixted, and Richard G Morris. 2015. Memory consolidation. _Cold Spring Harbor perspectives in biology_ (2015). 

- [259] Jianlin Su, Murtadha Ahmed, Bo Wen, Luo Ao, Mingren Zhu, and Yunfeng Liu. 2024. Naive Bayes-based Context Extension for Large Language Models. In _Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)_ , Kevin Duh, Helena Gomez, and Steven Bethard (Eds.). Association for Computational Linguistics, Mexico City, Mexico, 7791–7807. doi:10.18653/v1/2024.naacl-long.431 

- [260] Xin Su, Tiep Le, Steven Bethard, and Phillip Howard. 2023. Semi-structured chain-of-thought: Integrating multiple sources of knowledge for improved language model reasoning. _arXiv preprint arXiv:2311.08505_ (2023). 

- [261] Theodore Sumers, Shunyu Yao, Karthik Narasimhan, and Thomas Griffiths. 2024. Cognitive Architectures for Language Agents. _Transactions on Machine Learning Research_ (2024). https://openreview.net/forum?id=1i6ZCvflQJ Survey Certification. 

- [262] Hao Sun, Hengyi Cai, Bo Wang, Yingyan Hou, Xiaochi Wei, Shuaiqiang Wang, Yan Zhang, and Dawei Yin. 2024. Towards Verifiable Text Generation with Evolving Memory and Self-Reflection. In _Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing_ . https://aclanthology.org/2024.emnlp-main.469/ 

- [263] Hanshi Sun, Li-Wen Chang, Wenlei Bao, Size Zheng, Ningxin Zheng, Xin Liu, Harry Dong, Yuejie Chi, and Beidi Chen. 2025. ShadowKV: KV Cache in Shadows for High-Throughput Long-Context LLM Inference. In _Forty-second International Conference on Machine Learning_ . https: //openreview.net/forum?id=oa7MYAO6h6 

- [264] Weiwei Sun, Miao Lu, Zhan Ling, Kang Liu, Xuesong Yao, Yiming Yang, and Jiecao Chen. 2025. Scaling Long-Horizon LLM Agent via Context-Folding. arXiv:2510.11967 [cs.CL] https://arxiv.org/abs/2510.11967 

Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

39 

- [265] Alon Talmor and Jonathan Berant. 2018. The Web as a Knowledge-base for Answering Complex Questions. In _Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies_ . 

- [266] Alon Talmor, Jonathan Herzig, Nicholas Lourie, and Jonathan Berant. 2019. CommonsenseQA: A Question Answering Challenge Targeting Commonsense Knowledge. In _Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)_ . doi:10.18653/v1/N19-1421 

- [267] Chenmien Tan, Ge Zhang, and Jie Fu. 2024. Massive Editing for Large Language Models via Meta Learning. In _The Twelfth International Conference on Learning Representations_ . https://openreview.net/forum?id=L6L1CJQ2PE 

- [268] Hexiang Tan, Fei Sun, and Wanli et al. Yang. 2024. Blinded by Generated Contexts: How Language Models Merge Generated and Retrieved Contexts When Knowledge Conflicts?. In _ACL_ . doi:10.18653/v1/2024.acl-long.337 

- [269] Zhaoxuan Tan, Zheyuan Liu, and Meng Jiang. 2024. Personalized Pieces: Efficient Personalized Large Language Models through Collaborative Efforts. In _Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing_ . doi:10.18653/v1/2024.emnlp-main.371 

- [270] Niket Tandon, Aman Madaan, Peter Clark, and Yiming Yang. 2021. Learning to repair: Repairing model output errors after deployment using a dynamic memory of feedback. _arXiv_ (2021). https://arxiv.org/abs/2112.09737 

- [271] Jiaming Tang, Yilong Zhao, Kan Zhu, Guangxuan Xiao, Baris Kasikci, and Song Han. 2024. QUEST: Query-Aware Sparsity for Efficient Long-Context LLM Inference. In _Proceedings of the 41st International Conference on Machine Learning_ . https://proceedings.mlr.press/v235/tang24l.html 

- [272] Yihong Tang, Bo Wang, Miao Fang, Dongming Zhao, Kun Huang, Ruifang He, and Yuexian Hou. 2023. Enhancing Personalized Dialogue Generation with Contrastive Latent Variables: Combining Sparse and Dense Persona. In _Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , Anna Rogers, Jordan Boyd-Graber, and Naoaki Okazaki (Eds.). Association for Computational Linguistics, Toronto, Canada, 5456–5468. doi:10.18653/v1/2023.acl-long.299 

- [273] Yihong Tang, Bo Wang, Miao Fang, Dongming Zhao, Kun Huang, Ruifang He, and Yuexian Hou. 2023. Enhancing Personalized Dialogue Generation with Contrastive Latent Variables: Combining Sparse and Dense Persona. In _Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ . doi:10.18653/v1/2023.acl-long.299 

- [274] Yi Tay, Mostafa Dehghani, Samira Abnar, Yikang Shen, Dara Bahri, Philip Pham, Jinfeng Rao, Liu Yang, Sebastian Ruder, and Donald Metzler. 2021. Long Range Arena : A Benchmark for Efficient Transformers. In _International Conference on Learning Representations_ . https://openreview.net/ forum?id=qVyeW-grC2k 

- [275] Tongyi DeepResearch Team. 2025. Tongyi DeepResearch: A New Era of Open-Source AI Researchers. https://github.com/Alibaba-NLP/ DeepResearch. 

- [276] Tencent. 2025. ima.copilot: Intelligent Workbench Powered by Tencent’s Hunyuan Model. https://ima.qq.com/ Accessed: 2025-05-23. 

- [277] Bozhong Tian, Xiaozhuan Liang, Siyuan Cheng, Qingbin Liu, Mengru Wang, Dianbo Sui, Xi Chen, Huajun Chen, and Ningyu Zhang. 2024. To Forget or Not? Towards Practical Knowledge Unlearning for Large Language Models. In _Findings of the Association for Computational Linguistics: EMNLP 2024_ . 1524–1537. 

- [278] Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, and Ashish Sabharwal. 2022. MuSiQue: Multihop Questions via Single-hop Question Composition. _Transactions of the Association for Computational Linguistics_ (2022). doi:10.1162/tacl_a_00475 

- [279] Endel Tulving et al. 1972. Episodic and Semantic Memory. _Organization of Memory_ 1, 381-403 (1972), 1. 

- [280] Szymon Tworkowski, Konrad Staniszewski, and Mikołaj et al. Pacek. 2023. Focused Transformer: Contrastive Training for Context Scaling. In _NeurIPS_ . https://proceedings.neurips.cc/paper_files/paper/2023/file/8511d06d5590f4bda24d42087802cc81-Paper-Conference.pdf 

- [281] Bingbing Wang, Yiming Du, Bin Liang, Zhixin Bai, Min Yang, Baojun Wang, Kam-Fai Wong, and Ruifeng Xu. 2025. A New Formula for Sticker Retrieval: Reply with Stickers in Multi-Modal and Multi-Session Conversation. In _Proceedings of the AAAI Conference on Artificial Intelligence_ . 

- [282] Bing Wang, Xinnian Liang, Jian Yang, Hui Huang, Shuangzhi Wu, Peihao Wu, Lu Lu, Zejun Ma, and Zhoujun Li. 2024. Enhancing Large Language Model with Self-Controlled Memory Framework. https://arxiv.org/abs/2304.13343 

- [283] Changyue Wang, Weihang Su, Qingyao Ai, Yichen Tang, and Yiqun Liu. 2025. Knowledge Editing through Chain-of-Thought. In _Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing_ , Christos Christodoulopoulos, Tanmoy Chakraborty, Carolyn Rose, and Violet Peng (Eds.). Association for Computational Linguistics, Suzhou, China, 10684–10704. doi:10.18653/v1/2025.emnlp-main.540 

- [284] Jane X Wang, Zeb Kurth-Nelson, Dharshan Kumaran, Dhruva Tirumala, Hubert Soyer, Joel Z Leibo, Demis Hassabis, and Matthew Botvinick. 2021. Dual-system episodic control: Integrating episodic memory and reinforcement learning. _Nature Human Behaviour_ (2021). 

- [285] Kewen Wang, Zhe Wang, Rodney Topor, et al. 2009. Concept and Role Forgetting in ALC Ontologies. In _Proceedings of the 8th International Semantic Web Conference (ISWC)_ . 

- [286] Lingzhi Wang, Tong Chen, Wei Yuan, et al. 2023. KGA: A General Machine Unlearning Framework Based on Knowledge Gap Alignment. _arXiv preprint arXiv:2305.06535_ (2023). 

- [287] Liyuan Wang, Xingxing Zhang, Hang Su, and Jun Zhu. 2024. A comprehensive survey of continual learning: Theory, method and application. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ (2024). 

- [288] Liyuan Wang, Xingxing Zhang, Kuo Yang, Longhui Yu, Chongxuan Li, Lanqing Hong, Shifeng Zhang, Zhenguo Li, Yi Zhong, and Jun Zhu. 2022. Memory replay with data compression for continual learning. _arXiv_ (2022). https://arxiv.org/abs/2202.06592 

- [289] Peng Wang, Zexi Li, Ningyu Zhang, Ziwen Xu, Yunzhi Yao, Yong Jiang, Pengjun Xie, Fei Huang, and Huajun Chen. 2024. Wise: Rethinking the knowledge memory for lifelong model editing of large language models. _Advances in Neural Information Processing Systems_ (2024). 

Du et al. 

40 

- [290] Piaohong Wang, Motong Tian, Jiaxian Li, Yuan Liang, Yuqing Wang, Qianben Chen, Tiannan Wang, Zhicong Lu, Jiawei Ma, Yuchen Eleanor Jiang, and Wangchunshu Zhou. 2025. O-Mem: Omni Memory System for Personalized, Long Horizon, Self-Evolving Agents. _arXiv preprint arXiv:2511.13593_ (2025). 

- [291] Peng Wang, Ningyu Zhang, Bozhong Tian, Zekun Xi, Yunzhi Yao, Ziwen Xu, Mengru Wang, Shengyu Mao, Xiaohan Wang, Siyuan Cheng, Kangwei Liu, Yuansheng Ni, Guozhou Zheng, and Huajun Chen. 2024. EasyEdit: An Easy-to-use Knowledge Editing Framework for Large Language Models. In _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 3: System Demonstrations)_ . doi:10.18653/v1/2024.acl-demos.9 

- [292] Qingyue Wang, Yanan Fu, Yanan Cao, Shi Wang, Zhiliang Tian, and Liang Ding. 2025. Recursively Summarizing Enables Long-Term Dialogue Memory in Large Language Models. _Neurocomputing_ (2025). doi:10.1016/j.neucom.2025.130193 

- [293] Qingyue Wang, Yanhe Fu, Yanan Cao, Shuai Wang, Zhiliang Tian, and Liang Ding. 2025. Recursively summarizing enables long-term dialogue memory in large language models. _Neurocomputing_ (2025). doi:10.1016/j.neucom.2025.130193 

- [294] Rongzheng Wang, Qizhi Chen, Yihong Huang, Yizhuo Ma, Muquan Li, Jiakai Li, Ke Qin, Guangchun Luo, and Shuang Liang. 2025. GraphCogent: Overcoming LLMs’ Working Memory Constraints via Multi-Agent Collaboration in Complex Graph Understanding. _arXiv preprint arXiv:2508.12379_ (2025). 

- [295] Siyuan Wang, Zhongyu Wei, Yejin Choi, et al. 2024. Symbolic Working Memory Enhances Language Models for Complex Rule Application. _arXiv preprint arXiv:2408.13654_ (2024). 

- [296] Shang Wang, Tianqing Zhu, Dayong Ye, and Wanlei Zhou. 2024. When Machine Unlearning Meets Retrieval-Augmented Generation (RAG): Keep Secret or Forget Knowledge? _arXiv preprint arXiv:2410.15267_ (2024). 

- [297] Song Wang, Yaochen Zhu, Haochen Liu, Zaiyi Zheng, Chen Chen, and Jundong Li. 2024. Knowledge editing for large language models: A survey. _Comput. Surveys_ 57, 3 (2024), 1–37. 

- [298] Yu Wang and Xi Chen. 2025. Mirix: Multi-agent memory system for llm-based agents. _arXiv preprint arXiv:2507.07957_ (2025). 

- [299] Yike Wang, Shangbin Feng, Heng Wang, Weijia Shi, Vidhisha Balachandran, Tianxing He, and Yulia Tsvetkov. 2023. Resolving knowledge conflicts in large language models. _arXiv preprint arXiv:2310.00935_ (2023). 

- [300] Yu Wang, Yifan Gao, Xiusi Chen, Haoming Jiang, Shiyang Li, Jingfeng Yang, Qingyu Yin, Zheng Li, Xian Li, Bing Yin, et al. 2024. MEMORYLLM: towards self-updatable large language models. In _International Conference on Machine Learning_ . 

- [301] Yu Wang, Chi Han, Tongtong Wu, Xiaoxin He, Wangchunshu Zhou, Nafis Sadeq, Xiusi Chen, Zexue He, Wei Wang, Gholamreza Haffari, et al. 2024. Towards lifespan cognitive systems. _arXiv preprint arXiv:2409.13265_ (2024). 

- [302] Yu Wang, Xinshuang Liu, Xiusi Chen, Sean O’Brien, Junda Wu, and Julian McAuley. 2024. Self-Updatable Large Language Models by Integrating Context into Model Parameters. In _The Thirteenth International Conference on Learning Representations_ . 

- [303] Yu Wang, Ryuichi Takanobu, Zhiqi Liang, Yuzhen Mao, Yuanzhe Hu, Julian McAuley, and Xiaojian Wu. 2025. Mem-{\alpha}: Learning Memory Construction via Reinforcement Learning. _arXiv preprint arXiv:2509.25911_ (2025). 

- [304] Yaxuan Wang, Jiaheng Wei, Chris Yuhao Liu, Jinlong Pang, Quan Liu, Ankit Shah, Yujia Bao, Yang Liu, and Wei Wei. 2025. LLM Unlearning via Loss Adjustment with Only Forget Data. In _The Thirteenth International Conference on Learning Representations_ . https://openreview.net/forum?id= 6ESRicalFE 

- [305] Ying Wang, Yanlai Yang, and Mengye Ren. 2023. LifelongMemory: Leveraging LLMs for Answering Queries in Long-form Egocentric Videos. _arXiv preprint arXiv:2312.05269_ (2023). 

- [306] Yutong Wang, Jiali Zeng, Xuebo Liu, Derek F. Wong, Fandong Meng, Jie Zhou, and Min Zhang. 2025. DelTA: An Online Document-Level Translation Agent Based on Multi-Level Memory. In _International Conference on Learning Representations_ . https://openreview.net/forum?id=hoYFLRNbhc 

- [307] Yun Wang, Long Zhang, Jingren Liu, Jiaqi Yan, Zhanjie Zhang, Jiahao Zheng, Xun Yang, Dapeng Wu, Xiangyu Chen, and Xuelong Li. 2025. Episodic Memory Representation for Long-form Video Understanding. _arXiv preprint arXiv:2508.09486_ (2025). 

- [308] Zhaowei Wang, Wei Fan, Qing Zong, Hongming Zhang, Sehyun Choi, Tianqing Fang, Xin Liu, Yangqiu Song, Ginny Wong, and Simon See. 2024. AbsInstruct: Eliciting Abstraction Ability from LLMs through Explanation Tuning with Plausibility Estimation. In _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ . Association for Computational Linguistics. doi:10.18653/v1/2024.acllong.55 

- [309] Zheng Wang, Zhongyang Li, Zeren Jiang, Dandan Tu, and Wei Shi. 2024. Crafting Personalized Agents through Retrieval-Augmented Generation on Editable Memory Graphs. In _Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing_ . doi:10.18653/v1/2024.emnlpmain.281 

- [310] Zhaowei Wang, Haochen Shi, Weiqi Wang, Tianqing Fang, Hongming Zhang, Sehyun Choi, Xin Liu, and Yangqiu Song. 2024. AbsPyramid: Benchmarking the Abstraction Ability of Language Models with a Unified Entailment Graph. In _Findings of the Association for Computational Linguistics: NAACL 2024_ . Association for Computational Linguistics. doi:10.18653/v1/2024.findings-naacl.252 

- [311] Zhaowei Wang, Wenhao Yu, Xiyu Ren, Jipeng Zhang, Yu Zhao, Rohit Saxena, Liang Cheng, Ginny Wong, Simon See, Pasquale Minervini, et al. 2025. MMLongBench: Benchmarking Long-Context Vision-Language Models Effectively and Thoroughly. _arXiv preprint arXiv:2505.10610_ (2025). 

- [312] Rubin Wei, Jiaqi Cao, Jiarui Wang, Jushi Kai, Qipeng Guo, Bowen Zhou, and Zhouhan Lin. 2025. MLP Memory: Language Modeling with Retriever-pretrained External Memory. _arXiv preprint arXiv:2508.01832_ (2025). 

- [313] Bowen Wu, Wenqing Wang, and Haoran et al. Li. 2025. Interpersonal Memory Matters: A New Task for Proactive Dialogue Utilizing Conversational History. _arXiv preprint arXiv:2503.05150_ (2025). 

Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

41 

- [314] Di Wu, Hongwei Wang, Wenhao Yu, et al. 2024. LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory. _arXiv preprint arXiv:2410.10813_ (2024). 

- [315] Haoyi Wu and Kewei Tu. 2024. Layer-Condensed KV Cache for Efficient Inference of Large Language Models. In _ACL_ . doi:10.18653/v1/2024.acllong.602 

- [316] Wei Wu, Zhuoshi Pan, Chao Wang, Liyi Chen, Yunchu Bai, Tianfu Wang, Kun Fu, Zheng Wang, and Hui Xiong. 2025. TokenSelect: Efficient Long-Context Inference and Length Extrapolation for LLMs via Dynamic Token-Level KV Cache Selection. https://arxiv.org/abs/2411.02886 

- [317] Xinwei Wu, Junzhuo Li, Minghui Xu, Weilong Dong, Shuangzhi Wu, Chao Bian, and Deyi Xiong. 2023. DEPN: Detecting and Editing Privacy Neurons in Pretrained Language Models. In _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing_ . 2875–2886. 

- [318] Yuhuai Wu, Markus N Rabe, DeLesley Hutchins, et al. 2022. Memorizing Transformers. _arXiv preprint arXiv:2203.08913_ (2022). [319] Yichen Wu, Hong Wang, Peilin Zhao, et al. 2024. Mitigating Catastrophic Forgetting in Online Continual Learning via Pareto Optimization. In _International Conference on Machine Learning_ . 

- [320] Yuxiang Wu, Yu Zhao, Baotian Hu, Pasquale Minervini, Pontus Stenetorp, and Sebastian Riedel. 2022. An Efficient Memory-Augmented Transformer for Knowledge-Intensive NLP Tasks. In _Proceedings of the EMNLP_ . doi:10.18653/v1/2022.emnlp-main.346 

- [321] xAI. 2023. Grok. https://grok.com. Accessed: 2025-04-19. [322] Tianhua Xia and Sai Qian Zhang. 2025. Kelle: Co-design KV Caching and eDRAM for Efficient LLM Serving in Edge Computing. arXiv:2510.16040 [cs.AR] https://arxiv.org/abs/2510.16040 

- [323] Guangxuan Xiao, Yuandong Tian, Beidi Chen, Song Han, and Mike Lewis. 2024. Efficient Streaming Language Models with Attention Sinks. In _International Conference on Learning Representations_ . https://openreview.net/forum?id=NG7sS51zVF 

- [324] Zeqi Xiao, Yushi Lan, and Yifan et al. Zhou. 2025. WORLDMEM: Long-term Consistent World Simulation with Memory. _arXiv preprint arXiv:2504.12369_ (2025). 

- [325] Fangyuan Xu, Weijia Shi, and Eunsol Choi. 2024. RECOMP: Improving Retrieval-Augmented LMs with Context Compression and Selective Augmentation. In _The Twelfth International Conference on Learning Representations_ . https://openreview.net/forum?id=mlJLVigNHp 

- [326] Haoming Xu, Ningyuan Zhao, Liming Yang, Sendong Zhao, Shumin Deng, Mengru Wang, Bryan Hooi, Nay Oo, Huajun Chen, and Ningyu Zhang. 2025. ReLearn: Unlearning via Learning for Large Language Models. In _Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and Mohammad Taher Pilehvar (Eds.). Association for Computational Linguistics, Vienna, Austria, 5967–5987. doi:10.18653/v1/2025.acl-long.297 

- [327] Jing Xu, Arthur Szlam, and Jason Weston. 2021. Beyond Goldfish Memory: Long-term Open-domain Conversation. _arXiv preprint arXiv:2107.07567_ (2021). 

- [328] Rongwu Xu, Zehan Qi, Zhijiang Guo, Cunxiang Wang, Hongru Wang, Yue Zhang, and Wei Xu. 2024. Knowledge conflicts for llms: A survey. _arXiv preprint arXiv:2403.08319_ (2024). 

- [329] Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, and Yongfeng Zhang. 2025. A-MEM: Agentic Memory for LLM Agents. _arXiv_ (2025). https://arxiv.org/abs/2502.12110 

- [330] Xinchao Xu, Zhibin Gou, Wenquan Wu, et al. 2022. Long Time No See! Open-domain Conversation with Long-term Persona Memory. _arXiv preprint arXiv:2203.05797_ (2022). 

- [331] Yao Xu, Shizhu He, Jiabei Chen, Zihao Wang, Yangqiu Song, Hanghang Tong, Guang Liu, Kang Liu, and Jun Zhao. 2024. Generate-on-graph: Treat llm as both agent and kg in incomplete knowledge graph question answering. _arXiv preprint arXiv:2404.14741_ (2024). 

- [332] Zhiyang Xu, Ying Shen, and Lifu Huang. 2023. MultiInstruct: Improving Multi-Modal Zero-Shot Learning via Instruction Tuning. In _Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ . doi:10.18653/v1/2023.acl-long.641 

- [333] Sikuan Yan, Xiufeng Yang, Zuchao Huang, Ercong Nie, Zifeng Ding, Zonggen Li, Xiaowen Ma, Hinrich Schütze, Volker Tresp, and Yunpu Ma. 2025. Memory-r1: Enhancing large language model agents to manage and utilize memories via reinforcement learning. _arXiv preprint arXiv:2508.19828_ (2025). 

- [334] Dongjie Yang, Xiaodong Han, and Yan et al. Gao. 2024. PyramidInfer: Pyramid KV Cache Compression for High-throughput LLM Inference. In _ACL Findings_ . doi:10.18653/v1/2024.findings-acl.195 

- [335] Hongkang Yang, Zehao Lin, Wenjin Wang, Hao Wu, Zhiyu Li, Bo Tang, Wenqiang Wei, Jinbo Wang, Zeyun Tang, Shichao Song, et al. 2024. _𝑀𝑒𝑚𝑜𝑟𝑦_<sup>3</sup> : Language Modeling with Explicit Memory. _arXiv preprint arXiv:2407.01178_ (2024). 

- [336] Hongkang Yang, Zehao Lin, and Wenjin et al. Wang. 2024. Memory3: Language Modeling with Explicit Memory. _arXiv preprint arXiv:2407.01178_ (2024). 

- [337] John Yang, Carlos E Jimenez, Alex L Zhang, Kilian Lieret, Joyce Yang, Xindi Wu, Ori Press, Niklas Muennighoff, Gabriel Synnaeve, Karthik R Narasimhan, Diyi Yang, Sida Wang, and Ofir Press. 2025. SWE-bench Multimodal: Do AI Systems Generalize to Visual Software Domains?. In _ICLR_ . https://openreview.net/forum?id=riTiq3i21b 

- [338] Yijun Yang, Zeyu Huang, Wenhao Zhu, Zihan Qiu, Fei Yuan, Jeff Z. Pan, and Ivan Titov. 2025. A Controllable Examination for Long-Context Language Models. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems Datasets and Benchmarks Track_ . https: //openreview.net/forum?id=atjpGqjG73 

- [339] Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W Cohen, Ruslan Salakhutdinov, and Christopher D Manning. 2018. HotpotQA: A dataset for diverse, explainable multi-hop question answering. _arXiv preprint arXiv:1809.09600_ (2018). 

Du et al. 

42 

- [340] Zhou Yang, Zhaochun Ren, Wang Yufeng, Haizhou Sun, Chao Chen, Xiaofei Zhu, and Xiangwen Liao. 2024. An Iterative Associative Memory Model for Empathetic Response Generation. In _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ . doi:10.18653/v1/2024.acl-long.170 

- [341] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. 2023. ReAct: Synergizing Reasoning and Acting in Language Models. In _The Eleventh International Conference on Learning Representations (ICLR)_ . https://openreview.net/forum?id=WE_vluYpwdu 

- [342] Yao Yao, Zuchao Li, and Hai Zhao. 2024. SirLLM: Streaming Infinite Retentive LLM. In _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics_ . doi:10.18653/v1/2024.acl-long.143 

- [343] Yuanshun Yao, Xiaojun Xu, and Yang Liu. 2024. Large language model unlearning. _Advances in Neural Information Processing Systems_ 37 (2024), 105425–105475. 

- [344] Rui Ye, Zhongwang Zhang, Kuan Li, Huifeng Yin, Zhengwei Tao, Yida Zhao, Liangcai Su, Liwen Zhang, Zile Qiao, Xinyu Wang, Pengjun Xie, Fei Huang, Siheng Chen, Jingren Zhou, and Yong Jiang. 2025. AgentFold: Long-Horizon Web Agents with Proactive Context Management. arXiv:2510.24699 [cs.CL] https://arxiv.org/abs/2510.24699 

- [345] Howard Yen, Tianyu Gao, and Danqi Chen. 2024. Long-Context Language Modeling with Parallel Context Encoding. In _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ . doi:10.18653/v1/2024.acl-long.142 

- [346] Wen-tau Yih, Ming-Wei Chang, Xiaodong He, and Jianfeng Gao. 2016. The Value of Semantic Parse Labeling for Knowledge Base Question Answering. In _Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ . 

- [347] Chanwoong Yoon, Taewhoo Lee, and Hyeon et al. Hwang. 2024. CompAct: Compressing Retrieved Documents Actively for Question Answering. In _EMNLP_ . doi:10.18653/v1/2024.emnlp-main.1194 

- [348] Peter Young, Alice Lai, Micah Hodosh, and Julia Hockenmaier. 2014. From image descriptions to visual denotations: New similarity metrics for semantic inference over event descriptions. _Transactions of the Association for Computational Linguistics_ (2014). 

- [349] Paul Youssef, Zhixue Zhao, Jörg Schlötterer, and Christin Seifert. 2025. How to Make LLMs Forget: On Reversing In-Context Knowledge Edits. In _Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)_ , Luis Chiruzzo, Alan Ritter, and Lu Wang (Eds.). Association for Computational Linguistics, Albuquerque, New Mexico, 12656–12669. doi:10.18653/v1/2025.naacl-long.630 

- [350] Hongli Yu, Tinghong Chen, Jiangtao Feng, Jiangjie Chen, Weinan Dai, Qiying Yu, Ya-Qin Zhang, Wei-Ying Ma, Jingjing Liu, Mingxuan Wang, et al. 2025. MemAgent: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent. _arXiv preprint arXiv:2507.02259_ (2025). 

- [351] Haofei Yu, Cunxiang Wang, Yue Zhang, and Wei Bi. 2023. TRAMS: Training-free Memory Selection for Long-range Language Modeling. In _Findings of the Association for Computational Linguistics: EMNLP 2023_ . doi:10.18653/v1/2023.findings-emnlp.331 

- [352] Jiwen Yu, Jianhong Bai, Yiran Qin, Quande Liu, Xintao Wang, Pengfei Wan, Di Zhang, and Xihui Liu. 2025. Context as memory: Scene-consistent interactive long video generation with memory retrieval. _arXiv preprint arXiv:2506.03141_ (2025). 

- [353] Jiayi Yuan, Hongyi Liu, Shaochen Zhong, Yu-Neng Chuang, Songchen Li, Guanchu Wang, Duy Le, Hongye Jin, Vipin Chaudhary, Zhaozhuo Xu, Zirui Liu, and Xia Hu. 2024. KV Cache Compression, But What Must We Give in Return? A Comprehensive Benchmark of Long Context Capable Approaches. In _Findings of EMNLP_ . 4623–4648. doi:10.18653/v1/2024.findings-emnlp.266 

- [354] Xihang Yue, Linchao Zhu, and Yi Yang. 2024. FragRel: Exploiting Fragment-level Relations in the External Memory of Large Language Models. In _Findings of the Association for Computational Linguistics: ACL 2024_ , Lun-Wei Ku, Andre Martins, and Vivek Srikumar (Eds.). Association for Computational Linguistics, Bangkok, Thailand, 16348–16361. doi:10.18653/v1/2024.findings-acl.968 

- [355] Ao Zhang, Yuan Yao, Wei Ji, Zhiyuan Liu, and Tat-Seng Chua. 2023. NExT-Chat: An LMM for Chat, Detection and Segmentation. _arXiv preprint arXiv:2311.04498_ (2023). 

- [356] Guibin Zhang, Muxin Fu, Guancheng Wan, Miao Yu, Kun Wang, and Shuicheng Yan. 2025. G-Memory: Tracing Hierarchical Memory for Multi-Agent Systems. _arXiv preprint arXiv:2506.07398_ (2025). 

- [357] Kai Zhang, Xiangchao Chen, Bo Liu, Tianci Xue, Zeyi Liao, Zhihan Liu, Xiyao Wang, Yuting Ning, Zhaorun Chen, Xiaohan Fu, et al. 2025. Agent learning via early experience. _arXiv preprint arXiv:2510.08558_ (2025). 

- [358] Kai Zhang, Yangyang Kang, Fubang Zhao, and Xiaozhong Liu. 2024. LLM-based Medical Assistant Personalization with Short- and Long-Term Memory Coordination. In _Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)_ . doi:10.18653/v1/2024.naacl-long.132 

- [359] Ningyu Zhang, Yunzhi Yao, Bozhong Tian, et al. 2024. A Comprehensive Study of Knowledge Editing for Large Language Models. _arXiv preprint arXiv:2401.01286_ (2024). 

- [360] Peitian Zhang, Zheng Liu, and Shitao et al. Xiao. 2025. Long Context Compression with Activation Beacon. In _ICLR_ . https://openreview.net/ forum?id=1eQT9OzfNQ 

- [361] Qizheng Zhang, Changran Hu, Shubhangi Upasani, Boyuan Ma, Fenglu Hong, Vamsidhar Kamanuru, Jay Rainton, Chen Wu, Mengmeng Ji, Hanchen Li, et al. 2025. Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models. _arXiv preprint arXiv:2510.04618_ (2025). 

- [362] Qingru Zhang, Chandan Singh, and Liyuan et al. Liu. 2024. Tell Your Model Where to Attend: Post-hoc Attention Steering for LLMs. In _ICLR_ . https://openreview.net/forum?id=xZDWO0oejD 

- [363] Qingyang Zhang, Ningyu Zhang, et al. 2025. LightMem: Lightweight and Efficient Memory-Augmented Generation. _arXiv preprint arXiv:2510.18866_ (2025). 

Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

43 

- [364] Siyuan Zhang, Yichi Zhang, and Yinpeng et al. Dong. 2025. Self-Memory Alignment: Mitigating Factual Hallucinations with Generalized Improvement. _arXiv preprint arXiv:2502.19127_ (2025). 

- [365] Taolin Zhang, Qizhou Chen, Dongyang Li, Chengyu Wang, Xiaofeng He, Longtao Huang, Jun Huang, et al. 2024. DAFNet: Dynamic Auxiliary Fusion for Sequential Model Editing in Large Language Models. In _Findings of the Association for Computational Linguistics: ACL 2024_ . 1588–1602. 

- [366] Xinrong Zhang, Yingfa Chen, Shengding Hu, Zihang Xu, Junhao Chen, Moo Hao, Xu Han, Zhen Thai, Shuo Wang, Zhiyuan Liu, and Maosong Sun. 2024. ∞Bench: Extending Long Context Evaluation Beyond 100K Tokens. In _ACL_ . 15262–15277. doi:10.18653/v1/2024.acl-long.814 

- [367] Zeyu Zhang, Xiaohe Bo, Chen Ma, Rui Li, Xu Chen, Quanyu Dai, Jieming Zhu, Zhenhua Dong, and Ji-Rong Wen. 2024. A survey on the memory mechanism of large language model based agents. _arXiv preprint arXiv:2404.13501_ (2024). 

- [368] Zhenyu Zhang, Ying Sheng, Tianyi Zhou, Tianlong Chen, Lianmin Zheng, Ruisi Cai, Zhao Song, Yuandong Tian, Christopher Re, Clark Barrett, Zhangyang Wang, and Beidi Chen. 2023. H2O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Models. In _Thirty-seventh Conference on Neural Information Processing Systems_ . https://openreview.net/forum?id=RkRrPp7GKO 

- [369] Wenting Zhao, Ye Liu, Tong Niu, Yao Wan, Philip S. Yu, Shafiq Joty, Yingbo Zhou, and Semih Yavuz. 2024. DIVKNOWQA: Assessing the Reasoning Ability of LLMs via Open-Domain Question Answering over Knowledge Base and Text. In _Findings of the Association for Computational Linguistics: NAACL 2024_ . doi:10.18653/v1/2024.findings-naacl.5 

- [370] Wayne Xin Zhao, Yusheng Wang, Yujia Yuan, Qitian Xiao, Yichong He, Jingyuan Zhang, and Ji-Rong Wen. 2024. CodeBuddy: Teaching Large Language Models to Write Better Code via Self-Improvement Feedback. In _ACL_ . https://arxiv.org/abs/2403.09161 arXiv preprint arXiv:2403.09161. 

- [371] Yilong Zhao, Chien-Yu Lin, Kan Zhu, Zihao Ye, Lequn Chen, Size Zheng, Luis Ceze, Arvind Krishnamurthy, Tianqi Chen, and Baris Kasikci. 2024. Atom: Low-Bit Quantization for Efficient and Accurate LLM Serving. In _MLSys_ . https://proceedings.mlsys.org/paper_files/paper/2024/hash/ 5edb57c05c81d04beb716ef1d542fe9e-Abstract-Conference.html 

- [372] Zhengyi Zhao, Shubo Zhang, Yiming Du, Bin Liang, Baojun Wang, Zhongyang Li, Binyang Li, and Kam-Fai Wong. 2025. EventWeave: A Dynamic Framework for Capturing Core and Supporting Events in Dialogue Systems. _arXiv preprint arXiv:2503.23078_ (2025). 

- [373] Ce Zheng, Lei Li, Qingxiu Dong, Yuxuan Fan, Zhiyong Wu, Jingjing Xu, and Baobao Chang. 2023. Can We Edit Factual Knowledge by In-Context Learning?. In _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing_ . 4862–4876. 

- [374] Longtao Zheng, Rundong Wang, Xinrun Wang, and Bo An. 2024. Synapse: Trajectory-as-Exemplar Prompting with Memory for Computer Control. In _International Conference on Learning Representations_ . https://arxiv.org/abs/2306.07863 

- [375] Wanjun Zhong, Lianghong Guo, Qiqi Gao, et al. 2024. MemoryBank: Enhancing Large Language Models with Long-term Memory. In _Proceedings of the AAAI Conference on Artificial Intelligence_ . 

- [376] Zexuan Zhong, Zhengxuan Wu, Christopher D Manning, Christopher Potts, and Danqi Chen. 2023. MQuAKE: Assessing Knowledge Editing in Language Models via Multi-Hop Questions. In _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing_ . 15686–15702. 

- [377] Huichi Zhou, Yihang Chen, Siyuan Guo, Xue Yan, Kin Hei Lee, Zihan Wang, Ka Yiu Lee, Guchun Zhang, Kun Shao, Linyi Yang, et al. 2025. AgentFly: Fine-tuning LLM Agents without Fine-tuning LLMs. _arXiv preprint arXiv:2508.16153_ (2025). 

- [378] Junjie Zhou, Zheng Liu, Shitao Xiao, Bo Zhao, and Yongping Xiong. 2024. VISTA: Visualized Text Embedding For Universal Multi-Modal Retrieval. In _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ . 

- [379] Wenxuan Zhou, Sheng Zhang, Hoifung Poon, and Muhao Chen. 2023. Context-faithful Prompting for Large Language Models. In _Findings of EMNLP_ . doi:10.18653/v1/2023.findings-emnlp.968 

- [380] Yang Zhou, Pengfei Cao, Yubo Chen, Qingbin Liu, Dianbo Sui, Xi Chen, Kang Liu, and Jun Zhao. 2025. M2Edit: Locate and Edit Multi-Granularity Knowledge in Multimodal Large Language Model. In _Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing_ , Christos Christodoulopoulos, Tanmoy Chakraborty, Carolyn Rose, and Violet Peng (Eds.). Association for Computational Linguistics, Suzhou, China, 29017–29030. doi:10.18653/v1/2025.emnlp-main.1478 

- [381] Zijian Zhou, Ao Qu, Zhaoxuan Wu, Sunghwan Kim, Alok Prakash, Daniela Rus, Jinhua Zhao, Bryan Kian Hsiang Low, and Paul Pu Liang. 2025. MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents. _arXiv preprint arXiv:2506.15841_ (2025). 

- [382] Yun Zhu, Jia-Chen Gu, Caitlin Sikora, Ho Ko, Yinxiao Liu, Chu-Cheng Lin, Lei Shu, Liangchen Luo, Lei Meng, Bang Liu, and Jindong Chen. 2025. Accelerating Inference of Retrieval-Augmented Generation via Sparse Context Selection. In _The Thirteenth International Conference on Learning Representations_ . https://openreview.net/forum?id=HE6pJoNnFp 

- [383] Jiaru Zou, Xiyuan Yang, Ruizhong Qiu, Gaotang Li, Katherine Tieu, Pan Lu, Ke Shen, Hanghang Tong, Yejin Choi, Jingrui He, James Zou, Mengdi Wang, and Ling Yang. 2025. Latent Collaboration in Multi-Agent Systems. arXiv:arXiv:2511.20639 [cs.CL] https://arxiv.org/abs/2511.20639 

Du et al. 

44 

# **Appendix** 

# **A GPT-based Pipeline Selection** 

To facilitate large-scale relevance filtering aligned with our taxonomy, we design a GPT-based scoring pipeline to evaluate the alignment between paper abstracts and predefined task definitions (Table 4). Each abstract is paired with a corresponding task definition and scored on a 1–10 scale by the model, with a threshold of ≥ 8 used to retain high-relevance papers for further analysis. We adopt **GPT-4o-mini** as the scoring backbone due to its favorable trade-off between performance and efficiency. Despite its relatively lightweight architecture, GPT-4o-mini demonstrates strong zero-shot reasoning capabilities, making it a cost-effective and sufficiently accurate choice for abstract-level topic relevance estimation across a corpus of over 30,000 papers. The exact prompt format used in this evaluation process is illustrated in Figure 18. 

# **B Relative Citation Index** 

In this work, we identify impactful works by Relative Citation Index (RCI) metric inspired by the RCR metrics [110], which estimate the expected citations with respect to publication age to prevent bias between original citations from different publication dates. The age _𝐴𝑖_ of a paper _𝑝𝑖_ is computed as: 

, where _𝑇_ is the date when the citation is collected (20th April 2025) and _𝑌𝑒𝑎𝑟𝑖_ is the year where paper _𝑖_ is first published. Thus, we can model the relation between citation number _𝐶𝑖_ and age _𝐴𝑖_ of paper _𝑝𝑖_ in three different way, which are: 

**exponential model** : 

**log-log regression model** : 

We collect papers from past 3 years (2022 to 2025) from Top NLP and ML conferences (i.e., ACL, NAACL, EMNLP, NeurIPS, ICML, ICLR). To reduce the bias from different research area, we use GPT to score the relevance of a paper with the four topics discussed in the paper, using the prompt shown in Figure 18. We pick all the papers with score equal and higher than 8 and collect their publication date and citation numbers from Semantic Scholar API<sup>1</sup> . For papers without publication date field, we use the first conference day as the publication date. We gather a total number of 3,932 valid papers after the processing and compute the estimated _𝛽_<sup>ˆ</sup> and _𝛼_ ˆ accordingly<sup>2</sup> . Figure 15 shows the estimated age-citation model, where we can find that the log-log regression model best fit the data, which almost perfectly fitting the median citation with respect to publication age. In addition, log-log regression model grantees that the expected citation equals 0 when a paper is freshly released, which follows the intuition. Thus, we pick log-log regression model to compute the expected citation for next step<sup>3</sup> , and we are able to obtain the expected citation number _𝐶_<sup>ˆ</sup> _𝑖_ of paper _𝑝𝑖_ 

> 1https://www.semanticscholar.org/product/api 

> 2Noted that not all papers mentioned in this work are considered in estimating _𝛽_ ˆ and _𝛼_ ˆ, but they will be assigned a RCI score based on the publication age. 

> 3The estimation is: _𝛽_ ˆ = 1 _._ 878, _𝛼_ ˆ = 1 _._ 297 

Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

45 

<!-- Start of picture text -->
250<br>exponential model<br>linear model<br>200 log-log regression model<br>150<br>100<br>50<br>0<br>Age<br>0 0.5 1 1.5 2 2.5 3 3.5 4<br>Citations<br><!-- End of picture text -->

Fig. 15. Boxplot of citation distributions from the 3,932 papers with respect to age, red curve is the expected citations _𝐶_<sup>ˆ</sup> _𝑖_ . Generally _𝑅𝐶𝐼 >_ = 1 indicate the paper is above median citations in its age group, and higher _𝑅𝐶𝐼_ indicate higher research impact. 

with age _𝐴𝑖_ as: 

Then we compute the relative citation index _𝑅𝐶𝐼𝑖_ of paper _𝑝𝑖_ as: 

When _𝑅𝐶𝐼𝑖 >_ = 1, we consider this paper over-cited than its expectations, and vice versa. In this paper, we focus on the paper with _𝑅𝐶𝐼 >_ = 1, for which we believe has more influence. 

# **C RCI-Driven Analysis of Topic Impact** 

In this study, we leverage both RCI and publication volume trends to gain a clearer understanding of the development and influence of various memory-related research topics. As shown in Figure 16, boxplots illustrate the distribution of median Relative Citation Index (RCI) values across topics by year. Notably, 2023 stands out as a pivotal year following the emergence of large language models (LLMs), with a surge in both the quantity and quality of publications related to long-context and parametric memory, suggesting that these areas were directly shaped by the advancement of LLMs. In contrast, long-term memory and multi-source memory maintained relatively stable average impact levels, indicating continued activity without the emergence of disruptive or field-defining work during that period. 

Figure 17 visualizes the temporal trends in publication volume and median RCI for each topic. All topics experienced notable growth in publication counts, with long-context in particular expanding from one of the least represented topics before 2022 to the most prominent by 2024—largely driven by the rise of LLMs. Furthermore, the RCI of long-term memory has shown a steady increase, reflecting a growing body of valuable work in that domain. By contrast, other topics witnessed a noticeable decline in RCI medians after 2023, though their influence levels remained comparable to those seen prior to 2022. These patterns collectively underscore the substantial impact of large models in catalyzing progress across memory-related research, especially in the areas of long-context and parametric memory. 

Du et al. 

46 

Fig. 16. Overall distribution of median RCI across topics and years 

Fig. 17. Overall temporal trends of topic-wise publication volume and median RCI. 

# **D Chord Analysis of Interactions Among Memory Types, Operations, Topics, and Venues** 

We present a chord-based analysis of memory research from two perspectives: (1) the interactions among memory types, operations, and topics, and (2) their distribution across major ML and NLP conference venues. 

# **D.1 Memory Interactions Across Types, Operations, and Topics** 

To intuitively analyze the strength of connections between memory types, operations, and research topics, we examine 132 method-focused papers with an RCI ≥ 1 and generate a final chord diagram (as shown in Figure 19) based on the analysis. 

From the perspective of memory types, research predominantly focuses on parametric memory and contextual unstructured memory, with most work centered on compression, retrieval, forgetting, and updating. In contrast, contextual structured memory is relatively underexplored, likely because LLMs are optimized for sequential text and perform less effectively on structured inputs. 

From the operation perspective, compression and retrieval are the most frequently studied, while indexing receives comparatively less attention. This is largely because most existing works focus on the use of memory, where retrieval and compression are two fundamental operations. In the case of consolidation, most studies refer to storing knowledge either in model parameters via training on unstructured text or transforming it into a fixed external memory format. 

Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

47 

Updating and forgetting are mainly associated with knowledge editing and unlearning, typically within parametric memory. These directions aim to incrementally modify parameters in the model based on external input. However, due to the opaque nature of model internals, such memory operations remain at an early stage of active exploration. In contrast, memory indexing mechanisms for LLMs have received limited attention. 

From the topic perspective, parametric modification studies are mostly centered on parametric memory, though some works attempt parameter adaptation through continual learning over unstructured text. Research under the long-context theme primarily focuses on compression and retrieval within unstructured memory, with some leveraging parameterized forms like key-value caches. In long-term memory studies, the emphasis is also on unstructured memory, particularly in terms of consolidation, compression, and retrieval. Research related to multi-source memory is still limited and typically involves integrating structured and unstructured information. 

In summary, the limited exploration of contextual structured memory highlights an opportunity to develop more comprehensive memory operations by integrating it with unstructured memory. Second, research on multi-source memory remains scarce, despite the substantial challenges it poses—particularly the issue of memory conflicts arising from heterogeneous sources. Designing robust and consistent strategies for multi-source memory integration is thus a promising direction. Finally, although indexing has been extensively studied in traditional database systems, it remains underexplored in the context of LLM-based agents. The complexity of memory types and the need for vectorized or sparse retrieval methods call for new indexing approaches specifically tailored to reasoning and interaction in LLMs. 

# **D.2 Memory Interactions Across Conference Venues** 

In addition to our primary paper collection, we also analyzed 81 method-focused papers with RCI ≥ 1 across major conferences. As shown in Figure 20, from the operation perspective, compression, forgetting, and updating appear more frequently in ML conferences (ICLR, ICML, NeurIPS), while retrieval and consolidation are more commonly featured in NLP conferences (ACL, EMNLP, NAACL). This distribution suggests that the former set of operations is still in the stage of theoretical exploration, whereas the latter is more grounded in practical application. Consequently, compression, forgetting, and updating still hold substantial potential for translation into real-world systems. 

Indexing remains underrepresented in both ML and NLP venues. This may be partly due to its frequent co-occurrence with retrieval, and partly because current vector-based indexing approaches are relatively uniform, with few novel alternatives available. 

From the topic perspective, long-term memory is more frequently addressed in NLP conferences, while long-context topics are more common in ML venues—likely reflecting the differing application- and theory-oriented focuses of these communities. Parameter modification appears more often in ML conferences, whereas multi-source memory is more prevalent in NLP conferences, highlighting the fact that multi-source memory challenges often arise during real-world applications and system integration. 

Du et al. 

48 

|**Topic Name**|**Definition in Prompt**|
|---|---|
|Long-Term Memory|**Definition:**Creating systems that ensure knowledge from past interactions remains accessible as new<br>tasks emerge, maintaining continuity in multi-turn conversations.<br>**Features:**Memory retention, retrieval, and attribution—preserving, accessing, and contextualizing<br>memory to support coherent interaction.|
|Long-Context|**Definition:** Efficiently processing, interpreting, and utilizing very long input sequences without<br>performance degradation.<br>**Features:**Optimized attention, context compression, and mitigation of the “lost-in-the-middle” problem.|
|Parametric Memory Modifica-<br>tion|**Definition:**Managing and updating internal parameters to preserve accuracy, privacy, and adaptability<br>without full retraining.<br>**Features:**Selective unlearning, precise model editing, distillation, and lifelong learning.|
|Multi-Source|**Definition:**Integrating and harmonizing diverse data types into a unified framework while resolving<br>inconsistencies.<br>**Features:**Multi-modal fusion, semantic consistency, conflict resolution, and redundancy removal.|
|Personalization*|**Definition:**Building user-centric memory systems that adapt to individual preferences and history<br>while preserving privacy.<br>**Features:**Privacy-aware profiling, consistent personalization, and long-term continuity.|
|Table 4. Definitions and features<br>long-term memory that focuses o|of the five memory-centric evaluation topics. *Personalization is treated as a specialized form of<br>n user-centric adaptation across sessions.|

# Prompts of the Relevance Evaluation to Task Definitions 

**System Instruction:** Given the task and the abstract, evaluate the relevance of the abstract to the task. **Prompt Template:** """ You are tasked with evaluating the relevance of a given article to a specific task definition. Please read the following task definition, article title, and abstract carefully. Based on the content, rate the relevance on a scale from 1 to 10, where 1 means not relevant at all, and 10 means highly relevant. Task Definition: { _𝑡𝑎𝑠𝑘𝑑𝑒𝑓_ } Article Title: { _𝑡𝑖𝑡𝑙𝑒_ } Abstract: { _𝑎𝑏𝑠𝑡𝑟𝑎𝑐𝑡_ } Please provide your rating in the format [[Rating]]. For example, if the relevance is high, you might respond with [[9]]. """ 

Fig. 18. Prompt for evaluating article relevance to specific task definitions. 

49 

Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

<!-- Start of picture text -->
Dimension<br>Memory Topics<br>Memory Operations<br>e Memory Types<br>n<br>am tric<br>sio<br>Par<br>compres consolidationf<br>Co<br>org<br>nte<br>n etti<br>xtu<br>atio ng<br>al.<br>ind<br>U<br>fic<br>xt n<br>odi exi<br>nte stru<br>−m ng<br>−co ctu<br>tric<br>ng red<br>me<br>lo<br>ret<br>ara rie<br>ep val<br>urc<br>so<br>Co<br>lti− pu<br>nt<br>mu dat<br>etx<br>gin<br>luSatru.<br>erm<br>tg− dtecru<br>lno<br><!-- End of picture text -->

Fig. 19. Chord Map of Interactions Across Memory Topics, Operations, and Types. 

<!-- Start of picture text -->
Dimension<br>Memory Topics<br>Conference Venues<br>trieval Memory Operations<br>ML<br>updating re indexing forgettingconsolid<br>on<br>a<br>ati<br>tion<br>odific<br>c−m<br>xt<br>NL<br>e<br>etri<br>t<br>P<br>on<br>am<br>g−c<br>par<br>lon co<br>e<br>mp<br>urc<br>re<br>so<br>s<br>lti−<br>sion<br>mu<br>erm<br>tg−<br>lon<br><!-- End of picture text -->

Fig. 20. Chord Map of Interactions Across Memory Topics, Operations, and Conference Venues. 

Du et al. 

50 

|**Datasets**|**Mo**|**Operations**|**DS**<br>**Type**|**Per**|**TR**|**Metrics**|**Purpose**|**Year**|
|---|---|---|---|---|---|---|---|---|
|**PersonaMem-v2**<br>[121]|text|Updating,<br>Retrieval<br>|MS|||Accuracy,<br>Persona Score|Benchmarks implicit user persona learning and<br>agentic memory updates over long contexts.|2025|
|**MemoryBench**<br>[4]|text|Updating,<br>Retrieval,<br>Forgetting|QA|||Accuracy,<br>Retention Rate|Comprehensive benchmark for memory correct-<br>ness, persistence, and continual learning.|2025|
|**HaluMem**<br>[29]|text|Retrieval|QA|||Accuracy,<br>Hallucination Rate,<br>Omission Rate|Evaluates hallucinations in memory extraction,<br>updating, and retrieval.|2025|
|**BFCL V4**<br>[229]|text (API/-<br>Code)|Updating,<br>Retrieval,<br>Reasoning|QA<br>(API)|||AST Accuracy,<br>Execution Success|Benchmarks function-calling capabilities, fea-<br>turing a dedicated memory category for CRUD-<br>style tool usage.|2025|
|**LongMemEval**<br>[314]|text|Indexing,<br>Retrieval,<br>Compression|MS|||Recall@K,<br>NDCG@K,<br>Accuracy|Benchmarks chat assistants on long-term mem-<br>ory abilities, including temporal reasoning.|2024|
|**LoCoMo**<br>[196]|text + im-<br>age|Indexing,<br>Retrieval,<br>Compression|MS|||Accuracy, ROUGE,<br>Precision, Recall, F1|Evaluates long-term memory in LLMs across<br>QA, event summarization, and multimodal dia-<br>logue tasks.|2024|
|**MemoryBank**<br>[375]|text|Updating,<br>Retrieval|MS|||Accuracy,<br>Human Eval<br>MAP Recall|<br>Enhances LLMs with long-term memory, adapt-<br>ing to user personalities and evolving contexts.|2024|
|**PerLTQA**<br>[65]|text|Retrieval|MS|||, ,<br>Precision, F1,<br>Accuracy,<br>GPT-4<br>score|Evaluates personalized long-term memory QA<br>capabilities.|2024|
|**MALP**<br>[358]|text|Retrieval,<br>Compression|QA|||ROUGE, Accuracy,<br>Win Rate|Preference-conditioned dialogue generation;<br>supports PEFT customization.<br>|2024|
|**DialSim**<br>[137]|text|Retrieval|MS|||Accuracy|Evaluates dialogue systems under realistic, real-<br>time, and long-context multi-party conversa-<br>tions.|2024|
|**CC**<br>[114]|text|Retrieval<br>|MS|||BLEU, ROUGE|Models long-term dialogues incorporating tem-<br>poral and relationship contexts.|2023|
|**LAMP**<br>[246]|text|Consolidation,<br>Retrieval,<br>Compression<br>|MS|||Accuracy,<br>F1,<br>ROUGE|Provides user- and time-based splits for evalu-<br>ating short- and long-term personalization.|2023|
|**MSC**<br>[327]|text|Consolidation,<br>Retrieval,<br>Compression<br>|MS|||PPL<br>|Multi-session human-human chats for evolving<br>shared knowledge evaluation.|2022|
|||Consolidation,||||Accuracy, F1,|||
|**DuLeMon**<br>[330]|text<br>table +|Updating,<br>Retrieval,<br>Compression<br>Consolidation,|MS|||<br>Recall, Precision,<br>PPL, BLEU,<br>DISTINCT|Supports dynamic persona tracking and consis-<br>tent long-term human-bot interactions.|2022|
|**2WikiMultiHopQA**<br>[95]|knowledge<br>base<br>+<br>text|Indexing,<br>Retrieval,<br>Compression|QA|||EM, F1|Multi-hop QA combining structured and un-<br>structured data with reasoning paths.|2020|
|**NQ**<br>[145]|text|Retrieval,<br>Compression|QA|||EM, F1|Open-domain QA based on real Google search<br>queries.|2019|
|**HotpotQA**<br>[339]|text|Retrieval,<br>Compression|QA|||EM, F1|Multi-hop QA with explainable reasoning and<br>supporting facts at the sentence level.|2018|

Table 5. Datasets used for evaluating **long-term memory** . “Mo” = modality; “Ops” = supported operations; “DS Type” = dataset type (QA – question answering, MS – multi-session dialogue); “Per” and “TR” = presence of persona and temporal reasoning. 

51 

# Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

|**Datasets**|**Modality**|**Operations**|**Metrics**|**Purpose**|**Year**|
|---|---|---|---|---|---|
|**LongBioBench**<br>[338]|text|retrieval|EM|Controllable long-context multi-hop examination<br>for LLMs<br>|2025|
|**LongBench v2**<br>[16]|text + table <br>KG|+<br>compression,<br>retrieval|Accuracy|Updated version of LongBench, longer and more<br>challenging, with a consistent multi-choice format<br>for reliable evaluation.|2024|
|**SWE-bench**<br>**Multimodal**<br>[337]|text + image|compression,<br>retrieval|Resolution rate,<br>Inference cost|Extends SWE-bench with multimodal tasks (517<br>instances) to test reasoning with images.|2024|
|∞**Bench**<br>[366]|text|compression,<br>retrieval|F1,<br>Accuracy,<br>ROUGE-L-Sum|Benchmark with 12 tasks targeting extreme long<br>contexts (average >100K tokens).|2024|
|**L-Eval**<br>[5]|text|compression,<br>retrieval|ROUGE-L, F1,<br>GPT-4<br>|20 tasks designed to evaluate long-context LLMs<br>from various perspectives.|2023|
|**LongBench**<br>[15]|text|compression,<br>retrieval|F1, ROUGE-L,<br>Accuracy, EM,<br>Edit Sim|Includes 14 English tasks, 5 Chinese tasks, and 2<br>code tasks for systematic long-context evaluation.|2023|
|**SWE-bench**<br>[130]|text|compression,<br>retrieval|Resolution rate (%<br>Resolved)|Tests LLMs on solving GitHub issues (2,294 in-<br>stances), requiring reasoning over large codebases.|2023|
|**NIAH**<br>[135]|text|retrieval|Recall Accuracy<br>BLEU-1, BLEU-4,|Evaluating LLMs on finding specific data (needle)<br>in long contexts (haystack).|2023|
|**LooGLE**<br>[154]|text|compression,<br>retrieval|ROUGE-1, ROUGE-<br>4,<br>ROUGE-L, Meteor,<br>Bert, GPT-4 scores<br>ROUGE-1, ROUGE-|Benchmark with 7 tasks for extreme long context<br>(each doc >24K tokens).|2023|
|**GovReport**<br>[104]|text|compression|2,<br>ROUGE-L,<br>Bert<br>|Government research reports for evaluating long-<br>document summarization.|2021|
||||Score|||
|**MusiQue**<br>[278]|text|retrieval|F1|Multi-hop QA benchmark for reasoning and long-<br>context QA tasks.|2021|
|**LRA**<br>[274]|text + image|compression,<br>retrieval|Accuracy|Six tasks designed to evaluate efficient long-context<br>models.|2020|
|**NaturalQuestions**<br>[145]|text|retrieval|EM, F1|QA dataset used for retrieval and reasoning tasks<br>with long contexts.|2019|
|**PG-19**<br>[238]|text|compression|PPL|Book corpus from Project Gutenberg for long-<br>context language modeling.|2019|
|**TriviaQA**<br>[134]|text|retrieval|EM, F1|QA dataset suitable for testing long-context under-<br>standing and reasoning.|2017|
|**NarrativeQA**<br>[143]|text|retrieval|BLEU-1, BLEU-4,<br>Meteor, ROUGE-L,<br>MRR|QA dataset for comprehension over narrative texts<br>with long contexts.|2017|
|**CNN/DailyMail**<br>[215]|text|compression|ROUGE-1, ROUGE-<br>2,<br>ROUGE-L|News articles for summarization tasks, suitable for<br>long-context evaluation.|2016|
|**WikiText-103**<br>[206]|text|compression|PPL|Wikipedia-based corpus of 100M tokens for long-<br>context language modeling.|2016|

Table 6. Datasets for **long-context memory** evaluation, sorted from newest to oldest. 

Du et al. 

52 

|**Dataset**|**Modality**|**Operations**|**Metrics**|**Purpose**|**Year**|
|---|---|---|---|---|---|
|**KnowEdit**<br>[359]|text|updating|Edit Success,<br>Portability, Locality,<br>Fluency|Provides a comprehensive benchmark of **six**<br>**datasets**for evaluating knowledge insertion,<br>modification, and erasure.<br>|2024|
|**MUSE**<br>[254]|text|forgetting|VerbMem, KnowMem,<br>PrivLeak|A benchmark for machine unlearning,<br>assessing**six key properties**for unlearned<br>models.|2024|
|**KnowUnDo**<br>[277]|text|forgetting|Unlearn Success,<br>Retention Success,<br>Perplexity, ROUGE-L|Evaluates unlearning in domains with<br>**copyrighted content and user privacy**,<br>checking if essential knowledge is<br>inadvertently erased.|2024|
|**RWKU**<br>[133]|text|forgetting|ROUGE-L|<br>Tests real-world unlearning under**corpus-free**<br>**conditions**with adversarial assessments.|2024|
|**WMDP**<br>[156]|text|forgetting|QA Accuracy|Benchmarks hazardous knowledge detection<br>and unlearning for**biosecurity,**<br>**cybersecurity, and chemical security**.|2024|
|**TOFU**<br>[197]|text|forgetting|Probability, ROUGE,<br>Truth Ratio|A dataset of facts about 200**fictitious authors**<br>for unlearning research.|2024|
|**ABSA**<br>[57]|text|consolidation|F1<br>|For aspect-based sentiment analysis to assess<br>LLMs in**continual learning**tasks.|2024|
|**MQUAKE-CF**<br>[376]|text|updating|Edit-wise Success Rate,<br>Instance-wise<br>Accuracy, Multi-hop<br>Accuracy|Evaluates**counterfactual knowledge**<br>**propagation**through multi-hop reasoning (up<br>to 4 hops).|2023|
|**MQUAKE-T**<br>[376]|text|updating|Edit-wise Success Rate,<br>Instance-wise<br>Accuracy, Multi-hop<br>Accuracy|Assesses**temporal knowledge propagation**<br>through multi-hop reasoning chains with one<br>edit per chain.|2023|
||||Efficacy Score, Efficacy|||
|**Counterfact**<br>[203]|text|updating|fi  fi<br>Magnitude, Paraphrase<br>Scores, Neighborhood<br>Score<br>Success Rate, Retain|Evaluates**substantial and improbable**<br>**factual changes**beyond superficial edits.|2022|
|**zsRE**<br>[50]|text|updating|Accuracy, Equivalence<br>Accuracy, Performance<br>Deterioration|One of the**earliest datasets**for evaluating<br>knowledge editing.|2021|
|**SGD**<br>[240]|text|consolidation|JGA, FWT, BWT|Multi-turn task-oriented dialogue for evolving<br>user intents and continual schema updates.|2020|
|**INSPIRED**<br>[89]|text|consolidation|JGA, FWT, BWT|Dialogue dataset supporting incremental intent<br>changes in task-oriented settings.|2020|
|**Natural Questions**<br>[145]|text|consolidation|Indexing Accuracy,<br>Hits@1|Multi-purpose QA dataset with indexed<br>documents for**dynamic continual learning**.|2019|

Table 7. Datasets for parametric memory evaluation, sorted by year from newest to oldest. 

53 

# Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

|**Datasets**|**Mo**|**Ops**|**Src#**|**Mod#**|**Task**|**Metrics**|**Purpose**|**Year**|
|---|---|---|---|---|---|---|---|---|
|**MultiChat**<br>[281]|text<br>+<br>image|Retrieval|2|2|Retrieval|<sup>Precision, mAP,</sup><br>GPT-4|Image-grounded sticker retrieval with<br>cross-session image-text dialogue con-<br>text.|2025|
|**MovieChat-1K**<br>[256]|text<br>+<br>video|Retrieval|2|2|QA|Accuracy|Long-term video understanding for<br>large multimodal models in video QA<br>and captioning tasks.|2025|
|**Context-conflicting**<br>[268]|text|Compression|2|1|Conflict|DiffGR,<br>EM,<br>Similarity|<br>Evaluate models’ ability to handle con-<br>flicting evidence across sources.<br>|2024|
|**EgoSchema**<br>[198]|video +<br>text|Retrieval,<br>Compression|3|2|Fusion|Accuracy|Combines episodic video memory, so-<br>cial schema, and conversation for long-<br>term QA.|2023|
|**Ego4D NLQ**<br>[101]|video +<br>text|Retrieval,<br>Compression|2|2|Fusion|Recall@K|QA over egocentric video with tem-<br>poral memory using natural language<br>queries.|2022|
|**2WikiMultihopQA**<br>[95]|text|Indexing,<br>Retrieval,<br>Compression|2|1|Reasonin|gEM, F1|Multi-hop QA requiring reasoning<br>across two Wikipedia passages with<br>sentence-level evidence.|2020|
|**HybridQA**<br>[34]|text|Retrieval,<br>Compression|2|1|Reasonin|gEM, F1|QA requiring reasoning across struc-<br>tured tables and unstructured text.|2020|
|**CommonsenseVQA**<br>[266]|text<br>+<br>image|Retrieval,<br>Compression|2|2|Fusion|Accuracy|Commonsense QA over visual scenes<br>requiring visual-text fusion.<br>|2019|
|**NaturalQuestions**<br>[145]|text|Retrieval,<br>Compression|>1*|1|Conflict|EM, F1|Real-world QA over Google search snip-<br>pets; also used for contradiction analy-<br>sis.|2019|
|**ComplexWebQuestions**<br>[265]|text|Retrieval,<br>Compression|>1*|1|Reasonin|gEM, F1|Compositional QA requiring multi-step<br>reasoning across web snippets.|2018|
|**HotpotQA**<br>[339]|text|Retrieval,<br>Compression|2|1|Conflict|EM,<br>F1,<br>Sup-<br>porting<br>Fact<br>Accuracy|Multi-hop QA with paragraph-level<br>sources and sentence-level supporting<br>facts.|2018|
|**TriviaQA**<br>[134]|text|Retrieval,<br>Compression<br>|≥6|1|Conflict|EM, F1|Trivia-style QA with noisy web sources;<br>used for source disagreement studies.|2017|
|**WebQuestionsSP**<br>[346]|text|Indexing,<br>Retrieval,<br>Compression|>1*|1|Reasonin|gF1, Accuracy|Enhanced WebQuestions with struc-<br>tured reasoning chains.|2016|
|**Flickr30K**<br>[348]|text<br>+<br>image|Retrieval,<br>Compression|2|2|Retrieval|Similarity|Image-caption pairs widely used for<br>cross-modal retrieval and alignment<br>tasks.|2014|

Table 8. Datasets used for evaluating **multi-source memory** . “Mo” denotes data modality. “Ops” indicates operations. “Src#” = number of information sources per instance; “Mod#” = number of modalities; “Task” = retrieval, fusion, reasoning, or conflict resolution. 

Du et al. 

54 

|**Method**|**Type**|**TF**|**RE**|**DS**|**Input**|**Output**|**LMs**|**Ops**|**Features**|**Year**|
|---|---|---|---|---|---|---|---|---|---|---|
|**EWE**<br>[31]|Memory Grounded<br>Generation||||Context<br>|Response|Llama-3.1-70B, 8B|Updating, Retrieval|Explicit working memory,<br>online fact-checking feedback,<br>factual long-form generation<br>|2025|
|**ICAL**|||||Examples +|Trajector|||Trajectory abstraction memory,||
|[248]|Generation||||Task<br>Instruction|y<br>+ Thoughts|GPT4V, Qwen2VL<br>|Updating|multi-modal, iterative<br>reasoning correction<br>|2025|
|**MEMORAG**<br>[234]|Memory Grounded<br>Generation||||Context +<br>Query|Response<br>|Mistral7B-Instruct,<br>Phi-3-mini-128K-<br>instruct, GPT-4o|Retrieval,<br>Compression|Global memory retrieval, KV<br>memory compression,<br>Feedback-guided generation<br>|2024|
|**ReadAgent**<br>[149]|Generation||||Context +<br>Query|Retrieved<br>Passages/-<br>Summary|PaLM 2|Updating, Retrieval|Episodic gist memory, dynamic<br>memory retrieval, extended<br>context window|2024|
|**FLOW-RAG**<br>[296]|Updating||||Knowledge<br>Base + Query|Response|GPT4o, Gemini,<br>llama2-7B-chat<br>|Forgetting|RAG-based unlearning<br>|2024|
|**HippoRAG**<br>[84]|Retrieval||||Context +<br>Query<br>|Response|ColBERTv2,<br>GPT-3.5-turbo,<br>Llama-3.1-8B, 70B|Indexing|Hippocampal-inspired retrieval,<br>multi-hop QA, Knowledge<br>graph integration|2024|
|**IterCQR**<br>[116]|Retrieval||||Dialogue<br>History +<br>Query|Retrieved<br>Results|Transformer++|Retrieval<br>ld|Iterative query reformulation,<br>context-aware query rewriting|2024|
|**MemoryBank**<br>[375]|Consolidation||||Retrieved &<br>Context +<br>Query|Response|ChatGLM-6B,<br>BELLE-7B,<br>gpt-3.5-turbo|Consoiation,<br>Updating,<br>Forgetting,<br>Retrieval|Fine-tuning, RAG, Ebbinghaus<br>Forgetting|2024|
|**FLARE**<br>[129]|Retrieval||||Database +<br>Query|Response|WebGPT, WebCPM|Retrieval|Active retrieval during<br>generation, forward-looking<br>query prediction<br>|2023|
|**MemoChat**<br>[190]|Consolidation||||Dialogue<br>History +<br>Query|Response|GPT4, ChatGPT,<br>Vicuna-7B, 13B,<br>33B, T5|Consolidation,<br>Retrieval|Structured memos,<br>memory-driven dialogue, mem-<br>orization–retrieval–response<br>cycle|2023|
|**NLI-Transfer**<br>[13]|Updating||||Memory +<br>Dialogue<br>History|Response|T5|Consolidation,<br>Updating, Retrieval|Session-level memory tracking,<br>evolving dialogue system|2022|

Table 9. Overview of methods for **long-term memory in memory management and utilization** . “TF” (Training Free) denotes whether the method operates without additional gradient-based updates; “RE” (Retrieval Module) denotes whether the method uses retrieval; “DS” (Dialogue System) denotes whether the method is designed for dialogue tasks. 

|**Method**|**Type**|**TF**|**RE**|**Input**|**Output**|**LMs**|**Ops**|**Features**|**Year**|
|---|---|---|---|---|---|---|---|---|---|
|**LD-Agent**<br>[153]|Augmentation|||Retrieved &<br>Context +<br>Query|Response|ChatGLM,<br>BlenderBot,<br>ChatGPT|Consolidation,<br>Updating,<br>Retrieval<br>|long-term dialogue modeling,<br>event & persona memory,<br>mudular agent architecture|2025|
|**SiliconFriend**<br>[375]|Augmentation|||Retrieved &<br>Context +<br>Query|Response|ChatGLM-6B,<br>BELLE-7B,<br>gpt-3.5-turbo|Consolidation,<br>Updating,<br>Forgetting,<br>Retrieval|fine-tuning,<br>RAG, Ebbinghaus Forgetting|2024|
|||||Retrieved &||||memory coordination,||
|**MALP**<br>[358]|Adaption|||<br>Context +<br>Query|Response|GPT3.5, LLaMA-7B,<br>LLaMA-13B|Consolidation,<br>Retrieval|computational bionic memory<br>mechanism, patient profile,<br>self-chat|2024|
|**PERPCS**||||||||modular PEFT sharing,||
|[269]|Adaption|||User History|/|Llama-2-7B|Consolidation|collaborative personalization,<br>user history assembly|2024|
|**LAPDOG**||||Retrieved &|||Consolidation,|Story-based persona retrieval,||
|[105]|Augmentation|||Context +<br>Query|Response|T5|Updating,<br>Retrieval|joint retriever-generator<br>training|2024|
|**RECAP**||||Retrieved &||||hierarchical transformer||
|[181]|Augmentation|||Context +<br>Query|Response|Transformers|Retrieval|retriever, context-aware prefix<br>encoder<br>|2023|
|**CLV**<br>[273]|Adaption|||Persona +<br>Query|Response|GPT-2|Consolidation|contrastive learning,<br>clustered dense persona,<br>dialogue generation|2023|
|**PERKGA**||||Retrieved &||||long-term dialogue modeling,||
|**Q**<br>[68]|Augmentation|||Knowledge<br>Graph + Query|Response|RoBERTa|Retrieval|event & persona memory,<br>mudular agent architecture|2022|

Table 10. Overview of methods for **long-term memory in personalization** . "TF" (Training Free) denotes whether the method operates without additional gradient-based updates. "RE" (Retrieval Module) denotes whether the method needs Retrieval. 

55 

# Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

|**Method**|**Type**|**TF**|**FC**|**Operations**|**LMs**|**Features**|**Year**|
|---|---|---|---|---|---|---|---|
|**FoldGRPO**<br>[264]|Context<br>Compression|||Compression|Seed-OSS-36B|RL framework training agents to<br>actively fold detailed histories into<br>concise summaries|2025|
|**RECOMP**<br>[325]|Context<br>Compression|||Compression|GPT-2, GPT2-XL, GPT-J,<br>Flan-UL2|Hard prompt compression with<br>extractive and abstractive strategies|2024|
|**LongLLMLingua**<br>[125]|Context<br>Compression|||Compression|GPT-3.5-Turbo-06136,<br>LongChat-13B-16k|Hard prompt compression for efficient<br>input representation|2024|
|**LLMLingua-2**<br>[227]|Context<br>Compression|||Compression|XLM-RoBERTa-Large,<br>Multilingual-BERT|Hard prompt compression with data<br>distillation for multilingual contexts|2024|
|**QGC**|Context|||Ci|LongChat-13B-16K,|Query-guided dynamic context|2024|
|[25]|Compression|||ompresson|LLaMA-2-7B|compression||
|**xRAG**<br>[36]|Context<br>Compression|||Compression|Mistral-7B, Mixtral-8x7B|Soft prompt compression for<br>parametric integration|2024|
|**AutoCompressor**<br>[37]|Context<br>Compression|||Compression|OPT-1.3B, OPT-2.7B,<br>LLaMA-2-7B|Soft prompt compression for<br>general-purpose efficiency|2023|
|**StreamingLLM**<br>[323]|KV Cache<br>Eviction|||Compression|Llama-2, MPT, PyThia, Falcon|Static KV cache eviction, Attention<br>sink in the initial tokens|2024|
|**FastGen**<br>[77]|KV Cache<br>Eviction|||Compression|Llama-1 7B/13B/30B/65B<br>LWM-Text-Chat-1M,|Adaptive profiling-based KV cache<br>eviction|2024|
|**SnapKV**<br>[163]|KV Cache<br>Eviction|||Compression|LongChat-7b-v1.5-32k,<br>Mistral-7B-Instruct-v0.2,<br>Mixtral-8x7B-Instruct-v0.1|Head-wise KV cache eviction,<br>Attention head behavior|2024|
|**LESS**<br>[59]|KV Cache<br>Storing<br>Optimization|||Compression|Llama-2 13B, Falcon 7B|Low-rank KV cache storage enabling<br>querying of all tokens|2024|
|**KIVI**<br>[188]|KV Cache<br>Storing<br>Optimization|||Compression|Llama-2 7B/13B, Llama-3 8B,<br>Falcon 7B, Mistral-7B|Asymmetrical KV cache quantization|2024|
|**KVQuant**<br>[98]|KV Cache<br>Storing<br>Optimization|||Compression|LLaMA-7B/13B/30B/65B,<br>Llama-2-7B/13B/70B,<br>Llama-3-8B/70B, Mistral-7B|KV cache quantization|2024|
|**H**2**O**<br>[368]|KV Cache<br>Eviction|||Compression|OPT, Llama-1, GPT-NeoX|Dynamic KV cache eviction, Retain<br>Heavy Hitter tokens|2023|
|**Scissorhands**<br>[184]|KV Cache<br>Eviction|||Compression|OPT 6.7B, 13B, 30B, 66B<br>|Dynamic KV cache eviction,<br>Persistence of importance hypothesis<br>|2023|
|**ShadowKV**<br>[263]|KV Cache<br>Storing<br>Optimization<br>|||Compression|Llama-3.1-8B, Llama-3-8B-1M,<br>GLM-4-9B-1M, Yi-9B-200K,<br>Phi-3-Mini-128K, and<br>Qwen2-7B-128K|Reduces GPU memory usage by<br>keeping compressed shadow versions<br>of keys on the GPU while offloading<br>full data to the CPU|2025|
|**FlexGen**<br>[250]|KV Cache<br>Storing<br>Optimization|||Compression|OPT 6.7B to 175B|KV cache quantization and offloading|2023|

Table 11. Overview of methods for **long-context memory compression** . “TF” (Training Free) indicates no additional gradient-based updates. “FC” (Full Context) indicates that the method preserves the access to all context tokens. 

Du et al. 

56 

|**Method**|**Type**|**TF**|**FC**|**Operations**|**LMs**|**Features**|**Year**|
|---|---|---|---|---|---|---|---|
|**Sparse RAG**<br>[382]|Context<br>Selection|||Retrieval|Gemini|Sparse context selection, reduces the<br>number of documents involved during<br>decoding|2025|
|**GraphReader**<br>[158]|Context<br>Selection|||Retrieval|GPT-4-128k|Graph-based agent; structures long<br>context into a graph|2024|
|**Ziya-Reader**<br>[91]|Context<br>Selection|||Retrieval|Ziya2-13B-Base (LLaMA-2-13B)|Supervised fine-tuning;<br>position-agnostic multi-step QA|2024|
|**FILM**<br>[6]|Context<br>Selection|||Retrieval|FILM-7B (Mistral 7B)|Data-driven approach; addresses the<br>“lost in the middle” problem|2024|
|**TokenSelect**<br>[316]|KV Cache<br>Selection|||Retrieval|Qwen2 7B, Llama-3 8B,<br>Yi-1.5-6B|Dynamic token-level KV cache<br>selection|2025|
|**QUEST**<br>[271]|KV Cache<br>Selection|||Retrieval|LongChat-7B-v1.5-32K,<br>Yarn-Llama2-7B-128K|Query-aware KV cache selection|2024|
|**Memorizing**<br>**Transformers**<br>[318]|KV Cache<br>Selection|||Retrieval|Transformers|External KV cache memory for<br>enhanced recall|2022|

Table 12. Overview of methods for **long-context memory retrieval** . “TF” (Training Free) indicates no additional gradient-based updates. “FC” (Full Context) indicates that the method preserves the access to all context tokens. 

57 

# Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

|**Method**|**Type**|**PR**|**TF**|**BES**|**SEO**|**LMs**|**Main Advancement**|**Year**|
|---|---|---|---|---|---|---|---|---|
|**AlphaEdit**<br>[70]|locating-then-<br>editing|||||gpt2-xl-1.5b,<br>gpt-j-6b,<br>llama3-8b|Protect preserved knowledge by**projecting**<br>**perturbation onto the null space**and adding<br>a**regularization term**for**sequential**editing.|2024|
|**MEMAT**<br>[201]|locating-then-<br>editing|||||aguila-7b|Extension of MEMIT with**attention head**<br>**corrections**for**cross-lingual**editing.<br>|2024|
|**DEM**<br>[107]|locating-then-<br>editing|||||gpt-j-6b,<br>llama2-7b|Uses a**dynamic aware module**to select<br>editing layers, targeting commonsense<br>knowledge editing in free text.<br>|2024|
|**DAFNET**<br>[365]|meta learning|||||gpt-j-6b,<br>llama2-7b|Supports**sequential editing**via<br>**Intra-editing Attention Flow**(within facts)<br>and**Inter-editing Attention Flow**(across<br>facts).|2024|
|**Larimar**<br>[48]|additional<br>parameters|||||gpt2-xl,<br>gpt-j-6b|Introduces a**decoupled latent memory**<br>**module**that conditions the LLM decoder at<br>test time without parameter updates.|2024|
|**MEMORYLLM**<br>[300]|additional<br>parameters|||||llama2-7b|Introduces a**fixed-size memory pool**that is<br>incrementally and selectively updated in a<br>frozen LLM.|2024|
|**WISE**<br>[289]|additional<br>parameters|||||llama2-7b,<br>mistral-7b,<br>gpt-j-6b|Supports sequential editing through**Side**<br>**Memory Design**and**Knowledge Sharding**<br>**and Merging**.|2024|
|**PMET**<br>[159]|locating-then-<br>editing|||||gpt-j-6b,<br>gpt-neox-20b<br>gpt-j-6b,|<br>**Jointly optimizes attention heads and FFN**,<br>updating only FFN weights.|2023|
|**IKE**<br>[373]|prompt|||-|-|gpt2-xl-1.5b,<br>gpt-neo,<br>gpt-neox,<br>|First method to use**in-context learning (ICL)**<br>for LLM editing.|2023|
|**MeLLo**<br>[376]|prompt|||-|-|opt-175b<br>vicuna-7b,<br>gpt-j-6b<br>|Combines**Question Decomposition + Self**<br>**Check**for editing.|2023|
|**MALMEN**<br>[267]|meta learning|||||bert-base,<br>gpt-2,<br>t5-xl,<br>gpt-j-6b|Uses least squares to merge edits reliably and<br>decouples networks to save memory,<br>supporting**massive batch**editing.|2023|
|**MEMIT**<br>[205]|locating-then-<br>editing|||||gpt-j-6b,<br>gpt-neox-20b|Optimizes a relaxed least-squares objective,<br>enabling a**closed-form solution**for**massive**<br>**batch**editing.|2022|
|**ROME**<br>[203]|locating-then-<br>editing|||||gpt2-xl-1.5b|A**classic locate-then-edit**method<br>performing a**rank-one update**on a single<br>MLP layer.|2022|
|**CaliNET**<br>[60]|additional<br>parameters|||||t5-base,<br>t5-large<br>|<br>Adds**FFN-like calibration layers**to modify<br>outputs efficiently.|2022|
|**SERAC**<br>[212]|additional<br>parameters|||||t5-large,<br>bert-base,<br>blenderbot-<br>90m|Combines**Scope Classifier + Counterfactual**<br>**Model**to support sequential or simultaneous<br>edits with consistent results.|2022|
|**GRACE**<br>[212]|additional<br>parameters|||||t5-small,<br>bert-base,<br>gpt2-xl-1.5b<br>gpt-neo,<br>t-j-6b|Supports sequential editing using a**codebook**<br>**with a deferral mechanism**.|2022|
|**MEND**<br>[211]|meta learning|||||gp,<br>t5-xl,<br>t5-xxl,<br>bert-base,<br>bart-base|Decomposes gradient updates into a rank-one<br>outer product for scalable, fast editing.|2021|
|**KE**<br>[50]|meta learning|||||bert-base,<br>bart-base|First to use a**hypernetwork**to project<br>sentence embeddings into a rank-1 gradient<br>mask.|2021|

Table 13. Overview of methods for **parametric memory optimization in editing** . "PR" (Parametric Reserving) denotes whether model weights remain untouched. "TF" (Training-Free) indicates editing without iterative optimization. "BES" (Batch Editing Support) highlights batch editing capability. "SEO" (Sequential Editing Optimization) shows mechanisms tailored for sequential edits. "LMs" lists the language models used for experiments. 

Du et al. 

58 

|**Method**|**Type**|**PR**|**TF**|**BUS**|**SUO**|**LMs**|**Main Advancement**|**Year**|
|---|---|---|---|---|---|---|---|---|
|**ULD**<br>[118]|additional<br>parameters|||||llama2-chat-7b,<br>mistral-7b-instruct|Derives an unlearned LLM by computing the<br>**logit difference**between the target and<br>assistant models.|2024|
|**ECO**<br>[173]|prompt|||||68 LLMs ranging from<br>0.5B to 236B|Performs unlearning by**corrupting prompt**<br>**embeddings**detected by a classifier, without<br>altering model weights.|2024|
|**WAGLE**<br>[119]|locating-then-<br>unlearning|||||llama2-7b-chat,<br>zephyr-7b-beta,<br>llama2-7b|Uses bi-level optimization to compute weight<br>attribution scores for**selective fine-tuning**to<br>achieve efficient, modular unlearning.|2024|
|**SOUL**<br>[120]|training objective|||||opt-1.3b, llama2-7b|Leverages a**second-order optimizer**for more<br>effective LLM unlearning.|2024|
|**SKU**<br>[185]|training objective|||||opt-2.7b, llama2-7b,<br>llama2-13b|Combines harmful knowledge learning with<br>task vector negation in a two-stage framework<br>for robust unlearning.|2024|
||||||||Introduces**unlearning layers**to forget||
|**EUL**<br>[30]|additional<br>parameters|||||t5-base, t5-3b|specific data, supporting sequential unlearning<br>through a**fusion mechanism**to merge<br>multiple layers.|2023|
|**ICUL**<br>[231]|prompt|||-|-|bloom-560m,<br>bloom-1.1b, bloom-3b,<br>llama2-7b|First method to leverage**in-context learning**<br>**(ICL)**for unlearning in language models.|2023|
|**GA+Mismatch**<br>[343]|training objective|||||opt-1.3b, opt-2.7b,<br>llama2-7b|Pioneered LLM unlearning by blending<br>**forgetting, random mismatch, and**<br>**KL-based preservation**objectives.|2023|
|**KGA**<br>[286]|training objective|||||bart-base, distil-bert,<br>lstm|Simulates forgetting by aligning knowledge<br>gaps between retain and forget models via<br>**distributional divergence minimization**.|2023|
|**DEPN**<br>[317]|locating-then-<br>unlearning|||||bert-base|Detects and disables privacy-related neurons to<br>reduce sensitive data leakage in language<br>models.|2023|

Table 14. Overview of methods for **parametric memory optimization in unlearning** . "PR" (Parametric Reserving) indicates whether the method avoids direct modification of internal weights. "TF" (Training-Free) shows if the method works without iterative optimization. "BUS" (Batch Unlearning Support) marks support for multiple edits simultaneously. "SUO" (Sequential Unlearning Optimization) indicates sequential unlearning capabilities. "LMs" lists language models used for experiments. 

59 

# Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

|**Method**|**Type**|**TF**|**TB**|**TS**|**Domain**|**LMs**|**Main Advancement**|**Year**|
|---|---|---|---|---|---|---|---|---|
|**HippoRAG 2**<br>[85]<br>**SELF-PARAM**<br>[302]|Regularization-<br>based Learning|||Task-<br>Free<br>Task-<br>Free|Question<br>Answering<br>Question<br>Answering|Llama-3.3-70B-<br>Instruct|Employs a training objective that<br>**minimizes the Kullback-Leibler**<br>**(KL) divergence**between the<br>predictions of the original model and<br>target model.<br>Enhances Personalized<br>PageRank-based retrieval with deeper<br>passage integration and online LLM<br>usage, achieving superior performance<br>on factual, associative, and<br>sense-making memory tasks.<br>Maintains a small, randomly selected|2025<br>2025|
|**MBPA++**<br>[301]|Replay-based|||CIL|None|REPLAY, MBPA|subset (as low as 1%) of past examples<br>in memory to achieve performance<br>comparable to larger memory sizes.<br>|2025|
||||||Abi||Integrates**multiple storage**||
|**LSCS**<br>[301]|Interactive<br>Learning|||CIL|stractng/<br>Merging/<br>Retrieval|/|**mechanisms**to achieve abstraction,<br>experience merging, and long-term<br>retention with accurate recall.|2025|
|**TaSL**<br>[73]|Regularization-<br>based Learning|||TIL|Dialogue<br>System|T5, Llama-7B|Parameter-level task skill localization<br>and consolidation enabling knowledge<br>transfer**without memory replay**.|2024|
|**EMP**<br>[178]|Replay-based|||CLI|Event<br>Detection|BERT-ED, KCN<br>oEWC, SI, LwF,|Designs**continuous prompts**<br>associated with each event type.<br>Introduces**adaptive coefficients**|2023|
|**UDIL**<br>[253]|Interactive<br>Learning|||DLI|Event<br>Detection|A-GEM,<br>CLS-ER, ESM,<br>etc.|optimized during training to achieve<br>tighter generalization error bounds and<br>improved performance across domains.|2023|
|**DSI++**<br>[200]|Replay-based|||TIL|Information<br>Retrieval|T5|Enables**continual document**<br>**indexing**while retaining query<br>performance on old and new data.<br>Enhances**memory replay by**|2022|
|**MRDC**<br>[288]|Replay-based|||CIL|Object<br>Detection|LUCIR,<br>PODNet|**compressing data**, balancing sample<br>quality and quantity for continual<br>learning.|2022|

Table 15. Overview of methods for **parametric memory modification in continual learning** . "TB" denotes whether task boundaries exist. "TS" denotes task settings including TIL (Task Incremental Learning), CIL (Class Incremental Learning), DIL (Domain Incremental Learning), and Task-Free. 

Du et al. 

60 

|**Method**|**Type**|**TF**|**STs**|**SNs**|**Input**|**Output**|**LMs**|**Ops**|**Features**|**Year**|
|---|---|---|---|---|---|---|---|---|---|---|
|**GoG**<br>[331]|reasoning||KG + text|WebQSP, CWQ|KG +<br>prompt +<br>query|answer|GPT-3.5,<br>GPT-4,<br>Qwen-1.5-<br>72B-Chat,<br>LLaMA3-<br>70B-<br>Instruct|Retrieval,<br>Compression|Integrate internal and<br>external knowledge|2024|
|**RKC-LLM**<br>[299]|conflict||model +<br>text|prompt + context|entities|answer|ChatGPT|Compression|Conflict span<br>localization,<br>instruction-guided<br>conflict handling|2024|
||||||||GPT-4,||||
|**BGC-KC**<br>[268]|conflict||model +<br>text|AIG, AIR|documents<br>+ query|answer|GPT-3.5,<br>Llama2-13b,<br>Llama2-7b|Retrieval,<br>Compression|Attribution tracing<br>framework, evaluate<br>LLM bias|2024|
||||Knowledge||||LLMA2||Semi-structured||
|**Sem-CoT**<br>[260]|reasoning||Graph +<br>text +<br>Model|Wikidata, 2Wiki,<br>MuSiQue, TKB|CoT prompt<br>+ query|answer|a-<br>7B, 13B,<br>70B, 65B|Retrieval,<br>Compression|prompting for<br>multi-source input<br>fusion|2023|
|||||Wikidata,|||||Heterogeneous||
||||b|Wikipedia,|||||knowledge integration,||
|**CoK**<br>[161]|reasoning||Dataase +<br>Tables +<br>Text|Wikitables,<br>Flashcard,<br>UpToDate,<br>ScienceQA, CK-12|CoT prompt<br>+ query|answer|GPT-3.5-<br>turbo|Retrieval,<br>Compression|dynamic knowledge<br>retrieval, adaptive<br>query generation across<br>formats|2023|
||||||||||Two-hop reasoning,||
|**DIVKNOWQ**<br>[369]|**A**<br>reasoning||Knowledge<br>Base + text|Wikidata,<br>DIVKNOWQA|CoT prompt<br>+ query|answer|GPT-3.5-<br>turbo|Retrieval,<br>Compression|symbolic query<br>generation for<br>structured data<br>Cognitive-inspired|2023|
|**StructRAG**<br>[165]|reasoning||KG + Table<br>+ text|Loong, Podcast<br>Transcripts|documents<br>+ query|answer|Qwen2-7B,<br>72B|Retrieval,<br>Compression|structurization,<br>dynamic structure<br>selection|2023|

Table 16. Overview of methods for **multi-source memory in cross-textual integration** . "TF" (Training Free) denotes whether the method operates without additional gradient-based updates. "STs" denotes the source types. "SNs" denotes the source dataset names. 

61 

Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

|**Method**|**Type**|**TF**|**STs**|**SNs**|**Input**|**Output**|**LMs**|**Ops**|**Features**|**Year**|
|---|---|---|---|---|---|---|---|---|---|---|
|**GoG**<br>[331]<br>**RKC-LLM**<br>[299]|reasoning<br>conflict||KG + text<br>model +<br>text|WebQSP, CWQ<br>prompt + context|KG +<br>prompt +<br>query<br>entities|answer<br>answer|GPT-3.5,<br>GPT-4,<br>Qwen-1.5-<br>72B-Chat,<br>LLaMA3-<br>70B-<br>Instruct<br>ChatGPT|Retrieval,<br>Compression<br>Compression|Integrate internal and<br>external knowledge<br>Conflict span<br>localization,<br>instruction-guided<br>conflict handling|2024<br>2024|
||||||||GPT-4,||||
|**BGC-KC**<br>[268]|conflict||model +<br>text|AIG, AIR|documents<br>+ query|answer|GPT-3.5,<br>Llama2-13b,<br>Llama2-7b|Retrieval,<br>Compression|Attribution tracing<br>framework, evaluate<br>LLM bias|2024|
||||Knowledge||||LLMA2||Semi-structured||
|**Sem-CoT**<br>[260]|reasoning||Graph +<br>text +<br>Model|Wikidata, 2Wiki,<br>MuSiQue, TKB|CoT prompt<br>+ query|answer|a-<br>7B, 13B,<br>70B, 65B|Retrieval,<br>Compression|prompting for<br>multi-source input<br>fusion|2023|
|||||Wikidata,|||||Heterogeneous||
||||Db|Wikipedia,|||||knowledge integration,||
|**CoK**<br>[161]|reasoning||ataase +<br>Tables +<br>Text|Wikitables,<br>Flashcard,<br>UpToDate,<br>ScienceQA, CK-12|CoT prompt<br>+ query|answer|GPT-3.5-<br>turbo|Retrieval,<br>Compression|dynamic knowledge<br>retrieval, adaptive<br>query generation across<br>formats|2023|
||||||||||Two-hop reasoning,||
|**DIVKNOWQ**<br>[369]|**A**<br>reasoning||Knowledge<br>Base + text|Wikidata,<br>DIVKNOWQA|CoT prompt<br>+ query|answer|GPT-3.5-<br>turbo|Retrieval,<br>Compression|symbolic query<br>generation for<br>structured data|2023|
||||||||||Cognitive-inspired||
|**StructRAG**<br>[165]|reasoning||KG + Table<br>+ text|Loong, Podcast<br>Transcripts|documents<br>+ query|answer|Qwen2-7B,<br>72B|Retrieval,<br>Compression|structurization,<br>dynamic structure<br>selection|2023|

Table 17. Overview of methods for **multi-source memory in cross-textual integration** . "TF" (Training Free) denotes whether the method operates without additional gradient-based updates. "STs" denotes the source types. "SNs" denotes the source dataset names. 

Du et al. 

62 

|**Memory**<br>**Tool**|**Level**|**Taxonomy**|**Operation**|**Function**|**Input/Output**|**Example Use**|**Source**<br>**Type**|
|---|---|---|---|---|---|---|---|
|**FAISS**<br>[61]|Components|Contextual-<br>Unstructured|Consolidation,<br>Indexing,<br>Retrieval|Library for fast storage,<br>indexing, and retrieval of<br>high-dimensional vectors|Vectors / Index,<br>relevance scores|Vector database — index a large<br>set of text embeddings and<br>retrieve the most relevant<br>documents for a query in a<br>retrieval-augmented<br>generation (RAG) system.|open|
|**Neo4j**<br>[216]|Components|Contextual-<br>Structured|Consolidation,<br>Indexing,<br>Updating,<br>Retrieval|Native graph database<br>supporting ACID<br>transactions and Cypher<br>query language<br>A probabilistic ranking|Nodes and<br>relationships<br>with properties /<br>Query results via<br>Cypher|Graph database — model and<br>retrieve complex relational data<br>for tasks like fraud detection<br>and recommendation engines.|conditional<br>open|
|**BM25**[243]|Components|Contextual-<br>Unstructured|Retrieval|function for information<br>retrieval to estimate the<br>relevance of documents to<br>a given query.<br>An unsupervised dense<br>retriever trained with|Text queries /<br>Ranked list of<br>documents|Enhancing search engine<br>results and document retrieval<br>systems.|open|
|**Contriever**<br>[113]|Components|Contextual-<br>Unstructured|Retrieval|contrastive learning,<br>capable of retrieving<br>semantically similar<br>documents across|Query text / List<br>of similar<br>documents|High-recall retrieval tasks in<br>multilingual<br>question-answering systems.|open|
|||||languages.||||
|**Embedding**||||Techniques to convert text,||||
|**Models**(e.g.,|||ld|<br>images, or audio into|Raw data /|Text similarity computation,||
|OpenAI<br>embeddings<br>[224])|Components|Contextual|Consoiation,<br>Retrieval|dense vector<br>representations capturing<br>semantic meaning.|Vector<br>embeddings|recommendation systems, and<br>clustering tasks.|open|

Table 18. **Component-Level** Tools for Memory Management and Utilization. 

|**Memory**<br>**Tool**|**Level**|**Taxonomy**|**Operation**|**Function**|**Input/Output**|**Example Use**|**Source**<br>**Type**|
|---|---|---|---|---|---|---|---|
|**Graphiti**<br>[92]<br>**LLamaIndex**<br>[175]<br>**LangChain**<br>[28]|framework<br><br>framework<br>framework|Contextual-<br>Structured<br>Contextual<br>Contextual|Consolidation,<br>Indexing,<br>Updating,<br>Retrieval<br>Consolidation,<br>Indexing,<br>Retrieval<br>Consolidation,<br>Indexing,<br>Updating,<br>Forgetting,<br>Retrieval<br>Consolidation,|Framework for building and<br>querying temporally-aware<br>knowledge graphs tailored for AI<br>agents in dynamic environments.<br>A flexible framework for building<br>knowledge assistants using LLMs<br>connected to enterprise data.<br>Provides a framework for building<br>context-aware, reasoning<br>applications by connecting LLMs<br>with external data sources.<br>Constructs controllable agent|Multi-source<br>data / Queryable<br>knowledge graph<br>Text / Context-<br>augmented<br>responses<br>Input prompts /<br>Multi-step<br>reasoning<br>outputs|Constructing real-time<br>knowledge graphs to<br>enhance AI agent memory.<br>Developing knowledge<br>assistants that process<br>complex data formats.<br>Creating complex LLM<br>applications like<br>question-answering systems<br>and chatbots.|open<br>open<br>open|
|**LangGraph**<br>[112]|framework|Contextual-<br>Structured|Indexing,<br>Updating,<br>Forgetting,<br>Retrieval|architectures supporting<br>long-term memory and<br>human-in-the-loop multi-agent<br>systems.|Graph state /<br>State updates|Building complex task<br>workflows with multiple AI<br>agents.|open|
|**EasyEdit**<br>[291]<br>**CrewAI**<br>[66]|framework<br>framework|Parametric<br>Contextual|Updating<br>Consolidation,<br>Indexing,<br>Retrieval|An easy-to-use knowledge editing<br>framework for LLMs, enabling<br>efficient behavior modification<br>within specific domains.<br>A platform for building and<br>deploying multi-agent systems,<br>supporting automated workflows<br>using any LLM and cloud<br>platform.|Edit instructions<br>/ Updated model<br>behavior<br>Multi-agent<br>tasks /<br>Collaborative<br>results|Modifying LLM knowledge<br>in specific domains, such as<br>updating factual<br>information.<br>Automating workflows<br>across agents like project<br>management and content<br>generation.|open<br>open|
|**Letta**[226]|framework|Contextual-<br>Unstructured|Consolidation,<br>Retrieval|Constructs stateful agents with<br>long-term memory, advanced<br>reasoning, and custom tools<br>within a visual environment.|User interactions<br>/ Improved<br>Response|Developing AI agents that<br>learn and improve over time.|open|

Table 19. **Framework-Level** Tools for Memory Management and Utilization. 

63 

# Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics 

|**Memory**<br>**Tool**|**Level**|**Taxonomy**|**Operation**|**Function**|**Input/Output**|**Example Use**|**Source**<br>**Type**|
|---|---|---|---|---|---|---|---|
|**MemOS**<br>[168]<br>**O-Mem**<br>[290]|Application<br>Layer<br>Application<br>Layer|Contextual-<br>Structured<br>Contextual-<br>Unstructured|Consolidation,<br>Updating,<br>Retrieval<br>Consolidation,<br>Updating,<br>Retrieval|An operating-system-like<br>architecture that manages<br>hierarchical memory (working,<br>short-term, long-term) to optimize<br>memory-augmented generation.<br>An omni-memory system that<br>enables agents to self-evolve and<br>maintain long-horizon consistency<br>through recursive memory<br>consolidation.|Agent queries,<br>complex contexts<br>/ Hierarchical<br>memory blocks<br>Long-term<br>interaction logs /<br>Evolved memory<br>state|Managing complex memory<br>resources for agents<br>handling multi-step<br>reasoning and long-horizon<br>tasks.<br>Creating self-evolving<br>personal AI assistants that<br>adapt to user growth over<br>time.|open<br>open|
|**Mem0**<br>[255]|Application<br>Layer|Contextual-<br>Unstructured|Consolidation,<br>Indexing,<br>Updating,<br>Retrieval|Provides a smart memory layer for<br>LLMs, enabling direct addition,<br>updating, and searching of<br>memories in models.|User interactions<br>/ Personalized<br>responses|Enhancing AI systems with<br>persistent context for<br>customer support and<br>personalized<br>recommendations.|open|
|**Zep**[239]|Application<br>Layer|Contextual-<br>Structured|Consolidation,<br>Indexing,<br>Updating,<br>Retrieval|Integrates chat messages into a<br>knowledge graph, offering<br>accurate and relevant user<br>information.|Chat logs,<br>business data /<br>Knowledge<br>graph query<br>results|Augmenting AI agents with<br>knowledge through<br>continuous learning from<br>user interactions.|open|
||||Consolidation,|An open memory layer that|Agent tasks /|Bildi AI  ih||
|**Memary**<br>[140]<br>**Memobase**<br>[202]|Application<br>Layer<br>Application<br>Layer|Contextual<br>Contextual|Indexing,<br>Updating,<br>Retrieval<br>Consolidation,<br>Indexing,<br>Updating,<br>Retrieval|emulates human memory to help<br>AI agents manage and utilize<br>information effectively.<br>A user profile-based long-term<br>memory system designed to<br>provide personalized experiences<br>in generative AI applications.|Memory<br>management and<br>utilization<br>User interactions<br>/ Personalized<br>responses|ung  agents wt<br>human-like memory<br>characteristics.<br>Implementing virtual<br>assistants, educational tools,<br>and personalized AI<br>companions.|open<br>open|

Table 20. **Application Layer-Level** Tools for Memory Management and Utilization. 

Du et al. 

64 

|**Memory**<br>**Tool**|**Level**|**Taxonomy**|**Operation**|**Function**|**Input/Output**|**Example Use**|**Source**<br>**Type**|
|---|---|---|---|---|---|---|---|
|**Me.bot**[209]|Product|Contextual|Consolidation,<br>Indexing,<br>Updating,<br>Retrieval|AI-powered personal assistant<br>that organizes notes, tasks, and<br>memories, providing emotional<br>support and productivity tools.|User inputs (text,<br>voice) /<br>Organized notes,<br>reminders,<br>summaries|Personal productivity<br>enhancement, emotional<br>support, idea organization.|closed|
|**ima.copilot**<br>[276]|Product|Contextual|Consolidation,<br>Indexing,<br>Updating,<br>Retrieval|Intelligent workstation powered<br>by Tencent’s Mix Huang model,<br>building a personal knowledge<br>base for learning and work<br>scenarios.|User queries /<br>Customized<br>responses,<br>knowledge<br>retrieval|Enhancing learning<br>efficiency, work productivity,<br>knowledge management.|closed|
|**Coze**[44]|Product|Contextual|Consolidation|Enabling multi-agent<br>collaboration across various<br>platforms.<br>AI assistant developed by xAI,|User-defined<br>workflows /<br>Response<br>Query /|Deployed chatbots, AI<br>agents|closed|
|**Grok**[321]|Product|Contextual|Retrieval,<br>Compression|designed to provide truthful,<br>useful, and curious responses,<br>with real-time data access and<br>image generation.<br>|Informative<br>answers,<br>generated<br>images|Answering questions,<br>generating images,<br>providing insights.|closed|
|**ChatGPT**<br>[223]|Product|Contextual|Consolidation,<br>Retrieval|Conversational AI developed by<br>OpenAI, capable of understanding<br>and generating human-like text<br>based on prompts.|User prompts /<br>Generated text<br>responses<br>|Answering questions,<br>generating images,<br>providing insights.|closed|
|**Replika**<br>[191]|Product|Contextual|Consolidation,<br>Updating,<br>Retrieval|AI companion maintaining<br>longitudinal interaction history<br>for emotional continuity.|Text input /<br>Emotionally<br>responsive<br>dialogues|Affective support, mental<br>wellness, simulated<br>companionship.|closed|
|**Amazon**<br>**Recom-**<br>**mender**<br>[170]|Product|Contextual|Consolidation,<br>Retrieval,<br>Indexing|Personalized recommendation<br>engine using behavioral memory<br>traces.|User behavior<br>logs / Ranked<br>product recom-<br>mendations<br>|E-commerce personalization,<br>customer profiling, targeted<br>marketing.|closed|
|**GitHub**<br>**Copilot**[79]|Product|Contextual|Retrieval,<br>Compression|Code assistant that provides<br>suggestions based on coding<br>history and file context.|Code editor<br>context / Code<br>completions,<br>snippets|Programming aid,<br>autocomplete, contextual<br>understanding.|closed|
|**CodeBuddy**<br>[42]|Product|Contextual|Retrieval,<br>Compression|AI code assistant.|Code and edits /<br>Personalized<br>coding<br>suggestions|Habit-aware code<br>generation, interactive<br>development support.|closed|
|**Doubao**[22]|Product|Contextual|Consolidation,<br>Retrieval|High-efficiency multimodal AI<br>assistant capable of handling<br>long-context interactions and<br>diverse everyday tasks.|Text, voice,<br>image inputs /<br>Answers,<br>creative content<br>Voice commands|Daily conversation, writing<br>assistance, coding support,<br>and role-playing.|closed|
|**Siri**[11]|Product|Contextual|Consolidation,<br>Retrieval|Intelligent voice assistant utilizing<br>on-device personal semantic<br>memory for context-aware and<br>cross-application actions.<br>Smart assistant integrated into|/ Action<br>execution,<br>personal<br>information<br>retrieval<br>Voice, text,|Device control, retrieving<br>personal context (e.g., flight<br>schedules), and cross-app<br>tasks.|closed|
|||||HarmonOS leverain|documents /|Document summarization||
|**Xiaoyi**[109]|Product|Contextual|Consolidation,<br>Retrieval|y, gg<br>ecosystem-level memory for<br>proactive services and document<br>understanding.|<br>Summaries,<br>suggestions, IoT<br>control|,<br>smart home control, and<br>personalized travel planning.|closed|

Table 21. **Product-Level** Tools for Memory Utilization.
