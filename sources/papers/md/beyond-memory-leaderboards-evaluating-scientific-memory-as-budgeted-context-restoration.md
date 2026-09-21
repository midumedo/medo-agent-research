---
stem: beyond-memory-leaderboards-evaluating-scientific-memory-as-budgeted-context-restoration
id: arxiv-2607.16848
title: "Beyond Memory Leaderboards: Evaluating Scientific Memory as Budgeted Context Restoration"
registry: arxiv
native_id: 2607.16848
version: null
kinds: [survey]
pdf: pdf/beyond-memory-leaderboards-evaluating-scientific-memory-as-budgeted-context-restoration.pdf
pdf_sha256: "09dd5520b628bbce492110aa73efd70d40d7e48eba379ab24dc6bda2cad68069"
parser: pymupdf4llm (recorded by legacy script)
converted_at: null
---

# Beyond Memory Leaderboards: Evaluating Scientific Memory as Budgeted Context Restoration

- arXiv: [2607.16848](https://arxiv.org/abs/2607.16848)
- 作者: Sheverev, Maksim, Finkelstein, David, Nikolenko, Sergey
- 发表日期: 2026/07/18

> 本文件是 PDF 的机器转换文本，转换成功不等于已对 PDF 做视觉核验。
> 上方元数据沿用历史抓取记录；其与当前 PDF 是否同版尚未核实。来源版本、获取时间及原转换环境缺失，不推测。
> 本地 PDF SHA256: `09dd5520b628bbce492110aa73efd70d40d7e48eba379ab24dc6bda2cad68069`。文件身份与转换信息见 [provenance.json](../provenance.json)。
> 下方分隔线之后为既有转换正文；本次只移除我方导航，不重新解析。

---

# Beyond Memory Leaderboards: Evaluating Scientific Memory as Budgeted Context Restoration 

Maksim Sheverev David Finkelstein _Quantellence Research Quantellence Research_ 

Sergey Nikolenko 

_St. Petersburg Department of the Steklov Institute of Mathematics, St. Petersburg, Russia St. Petersburg State University, St. Petersburg, Russia_ `sergey@logic.pdmi.ras.ru` 

July 21, 2026 

##### **Abstract** 

Long-term memory is becoming a core component of LLM agents, but most memory benchmarks evaluate conversations or compact summaries, while research agents need to restore evidence from full scientific papers. We introduce two full-text scientific-memory benchmarks, Public AI Memory (Paim; 81 papers, 66 audited questions) and Public Transformers (PTr; 252 papers, 98 audited questions). We evaluate eight memory/retrieval systems, including our own proposed system _Theoria_ , plus a no-retrieval baseline under a shared context-restoration protocol. Our results show that memory leaderboards are not interpretable without the full protocol: ingestion granularity, raw-text preservation, retrieval budget, retrieval modality, rubric audit, and judge choice all affect the outcome. For example, on Paim Graphiti wins convincingly but uses 2.6M characters of retrieved context per query, and after controlling for retrieval budget the lead disappears. On PTr, for the systems where BM25 retrieval can be added cleanly, the sparse–dense hybrid is the single most significant intervention: hybrid variants of Simple RAG, Mem0, and Theoria tie for the lead within 0.03 points. Multi-judge and human side-by-side calibration show that LLM-as-a-judge rankings are consistent across frontier judges and agree with human evaluation, with an effective resolution of roughly one point on a ten-point scale. We argue that scientific memory should be evaluated as _budgeted, modality-aware context restoration_ rather than as an unconstrained architecture leaderboard, and we release the datasets, harness, raw outputs, judgments, and scripts to reproduce our results and serve as tools for such evaluation. Our code is available at `https://gitlab.com/ quantellence/research/scientific-recall-bench` , and the datasets are available at `https://huggingface.co/datasets/quantellence/srb-data` . 

1 

## **1 Introduction** 

LLM agents increasingly rely on long-term memory mechanisms: vector stores, knowledge graphs, episodic logs, extracted facts, and hybrid retrieval pipelines. The current approaches to evaluating agent memory are largely inherited from conversational settings, with multi-session dialogues, user preferences, and fact updating; they usually treat memory as a _store-and-recall_ module to be ranked on benchmarks such as LongMemEval [43], LoCoMo [27], or BEAM [39]. 

**Why memory at all?** Before discussing how to evaluate memory, let us recall why agents need an explicit memory subsystem when context windows already reach one or two million tokens and retrieval-augmented generation (RAG) can fill them. There are at least four reasons, all of which recur throughout the systems we survey in Section 2. 

- (1) _Long contexts degrade._ The _lost-in-the-middle_ effect [26] shows that models attend well to the beginning and end of a long context but lose information in the middle, and interference grows with context length; a million-token window may be a poor substitute for curated memory. 

- (2) _Long contexts are expensive_ , both in money and in latency, because re-reading the entire history on every turn scales super-linearly with input size. 

- (3) _There is a benchmark-to-deployment gap._ Systems that score near-perfectly on conversational recall benchmarks can drop to 40–60% when the same facts must be _used_ inside a downstream task such as web navigation or constrained planning [12]; passive recall and active use are not the same skill. 

- (4) _Memory must update._ If an agent learned months ago that a user lives in Berlin and the user has since moved to Lisbon, the system has to decide whether to forget, overwrite, or version the stale fact. A useful memory is therefore not a log or a database but a system that answers a family of questions: what to store, how to store it, how to update it, what to return at query time, how to fuse evidence, how to flag contradictions, and when to forget. 

**Scientific memory is context restoration.** In our opinion, the standard conversational framing does not transfer cleanly to _research_ agents. When an agent reads a research paper, the relevant unit of memory is rarely a single fact: it is a conditional claim, the evidence behind it, the regimes in which it holds, the methods used to obtain it, and how it relates to other papers. The agent’s task is not to remember a user preference but to reconstruct, on demand, an interconnected body of literature relevant to a research question. We call this task _context restoration_ : the memory must return enough grounded evidence for a downstream model to compose a faithful answer. A scientific memory system is therefore valuable not only because it stores facts but because it can restore the right context for a downstream reasoning process, at the right granularity and within a realistic budget. 

In this work we present two new full-text question answering (QA) benchmarks on research papers and show experimentally that the distinction between recall and 

2 

<!-- Start of picture text -->
Ingest unit Memory store Retrieval Synthesis<br>Full Results<br>(chunk / paper / (vectors / facts / (budget / modality (LLM processing<br>papers and eval<br>episode) graph / theories) constraints) retrieved context)<br><!-- End of picture text -->

**Figure 1:** The context-restoration protocol. A memory system can differ at every stage: how full papers are split into ingestion units, how those units are represented in the store, how much and what kind of context is returned at retrieval time (the budget _𝐵_ and modality _𝑀_ ), and whether the final answer is synthesized internally by the system or externally by a shared model. 

context restoration has empirical consequences large enough to invert standard memory leaderboards in some settings. Our datasets consist of recent research papers on a given topic together with questions of varying difficulty that require either precise search or broad synthesis across several papers; we release Public AI Memory (Paim) on AI agent memory and Public Transformers (PTr) on recent Transformer architectures. We also present _Theoria_ , our own approach to memory for AI research agents, which is competitive with the strongest baselines under matched retrieval and wins on specific difficulty tiers. 

Figure 1 shows the evaluation protocol. We focus on the _retrieval budget_ ( _𝐵_ , characters returned per query) and the _retrieval modality_ ( _𝑀_ , dense vs. dense+lexical), and we compare memory approaches under the _same_ synthesis model. Our evaluation yields three main findings. 

First, comparisons can be dominated by the sheer volume of retrieved context. Graphiti [33] wins on Paim largely because it returns the raw text of matched episodes, up to 2.6M characters per query, and when the retrieval budget is constrained it drops to the bottom of the leaderboard. In a fair comparison with fixed budget _𝐵_ ≈ 30K characters, Simple RAG (7 _._ 25) ≈ Theoria (7 _._ 19) _>_ Mem0 (6 _._ 97) _>_ Hindsight (6 _._ 53) _>_ Cognee (5 _._ 28) ≈ Graphiti’s knowledge-graph output (5 _._ 27), so the original win was entirely due to context volume. 

Second, corpus structure and retrieval modality matter. On Paim we see a dense top cluster with Simple RAG, Theoria, and Mem0, whereas on PTr, whose named entities (model names, kernel names, hyperparameters) are lexically distinctive, structured memories (Theoria, Mem0) pull ahead of Simple RAG under dense retrieval. Interestingly, adding lexical BM25 retrieval to the dense embeddings and thus producing a sparse–dense hybrid was the single largest intervention we measured, significantly improving the scores for many memory systems. 

Third, we find LLM-as-a-judge evaluation to be quite reliable, especially on rank. A subset re-evaluation across three judges (Gemini 3.1 Pro, Sonnet 4.6, GPT-5.4) on Paim gives rank Spearman _𝜌_ ∈[0 _._ 90 _,_ 0 _._ 97]; on PTr, DeepSeek V4 Pro rankings correlate with Gemini at Pearson _𝑟_ = 0 _._ 93 over _𝑛_ = 946 valid paired cells even though DeepSeek is systematically more critical. A human study with 112 blinded side-by-side (SxS) votes shows high agreement with the LLM judge, scaling cleanly with the score gap. 

**Contributions.** (1) Two full-text scientific-memory benchmarks with audited rubrics, Paim and PTr. (2) A unified experimental harness covering eight memory/retrieval systems and a no-memory baseline, with hybrid BM25 variants for three of them and 

3 

a budget-and-modality retrieval protocol. (3) Multi-judge LLM calibration and 112 blinded human SxS votes that establish the resolution of the LLM judge (∼1 point on a 0–10 scale) and underwrite our experimental claims. (4) _Theoria_ , our own three-layer scientific-memory system, with an ablation ( _Prism_ ) that isolates its community/theory layers. We release the full datasets, experimental results, and scripts so that every figure and table in this paper can be reproduced: the `scibench` evaluation harness, per-system adapters, raw outputs, judgments, and analysis scripts are available on GitLab,<sup>1</sup> and both benchmark corpora with their audited rubrics are hosted on Hugging Face.<sup>2</sup> 

The remainder of the paper is organized as follows. Section 2 surveys agent-memory systems and benchmarks and positions our work; Section 3 describes the eight evaluated systems; Section 4 introduces the two benchmarks and the rubric audit; and Section 5 presents _Theoria_ . Section 6 presents our experimental evaluation, including the setup, Paim and PTr budget-and-modality sweeps, statistical significance, and judge calibration, while Section 7 analyzes representative answers qualitatively (including how a single system’s answer shifts with the retrieval budget). Section 8 discusses implications and limitations and draws lessons for the evaluation infrastructure, and Section 9 concludes the paper. Appendix A collects several more sample questions and answers. 

## **2 Related work** 

Agent memory has grown into a large and fast-moving field; a useful heuristic is that when a problem has twenty competing solutions, none of them works decisively well yet. This section surveys the landscape we benchmark against. We organize it by idea rather than chronology, and then we discuss in Section 3 the specific systems that we evaluate in this work. For broader treatments we refer to four recent surveys, each taking a different cut. 

### **2.1 Surveys and taxonomies** 

There are three main recent surveys of memory for LLM-based agents. _Memory in the Age of AI Agents_ [16] organizes memory along three orthogonal axes— _forms_ (token-level / parametric / latent), _functions_ (factual / experiential / working), and _dynamics_ (formation / evolution / retrieval)—and adds dedicated sections on benchmarks, open-source frameworks, and frontier directions. _CoALA_ [38] ports Tulving’s working/episodic/semantic/procedural split from cognitive psychology to LLM agents; this approach has become a default reference taxonomy. Jiang et al. [18] survey eleven architectural patterns and document _benchmark saturation_ and evaluation fragility, that is, sensitivity to the judge model and to the backbone LLM. They explain why reported numbers are often inflated even without any intent to mislead. In addition, Zhang et al. [50] provide an earlier systematic review that is useful mainly for the history of the problem. 

It is helpful to keep these three complementary taxonomies in mind. The _neuropsychological_ taxonomy (CoALA) classifies memory by what it stores: working memory 

> 1 `https://gitlab.com/quantellence/research/scientific-recall-bench` 

> 2 `https://huggingface.co/datasets/quantellence/srb-data` 

4 

(what is in context now), episodic memory (timestamped past events), semantic memory (facts about the world), and procedural memory (learned skills and behaviors). The _operational_ taxonomy classifies memory by the atomic operations a system must support; almost all modern systems implement three, called _formation / management / retrieval_ in academic surveys and _retain / recall / reflect_ in the Hindsight framing. The surveys agree that retrieval is comparatively well understood, both via classical information retrieval and with the extensively developed RAG tools, while the hardest, least-solved problems remain in management: conflict resolution, temporal reasoning, selective forgetting, and knowledge updating. Finally, the _methodological_ taxonomy classifies systems by their dominant mechanism, which is the organization we use below: store-first vector search, extract-and-update, OS-like hierarchies, temporal knowledge graphs, self-editing notes, verbal reinforcement learning, RL-trained memory management, multi-strategy parallel retrieval with fusion, graph-based associative recall, and bio-inspired consolidation. 

### **2.2 Three foundational systems** 

_Generative Agents_ [32] introduced the _memory stream_ : an append-only log of naturallanguage observations, each scored at retrieval time by a linear combination of three normalized signals, 

score = _𝛼_ rec recency + _𝛼_ imp importance + _𝛼_ rel relevance _,_ 

where recency is an exponential decay, importance is an LLM-assigned 1–10 “poignancy” rating, and relevance is embedding cosine similarity. In the released implementation all three weights are simply 1, yet the scheme works well enough that most retrieval-based memories still use it. Generative Agents also introduced _reflection_ : periodically the agent poses high-level questions about recent experience, retrieves relevant memories, and synthesizes higher-level insights that are written back into the stream, growing a tree where meaning is supposed to crystallize out of raw observations. Almost everything since is either a refinement of one component of this formula or a replacement of one component by something more sophisticated. 

_MemGPT_ [31], now productionized as _Letta_ [23], treats memory as an operating system: a fixed-size main context (system instructions, a read/write working block, and a FIFO queue with recursive summarization of the evicted tail) backed by external recall and archival stores, with explicit tool calls ( `core_memory_append` , `archival_memory_search` , . . . ) and _memory-pressure warnings_ analogous to page faults. Its lasting contribution is the principle that _the agent manages its own memory_ , which has since been reproduced in many different forms, including the `CLAUDE.md` -style memory files used by modern coding agents. 

_Reflexion_ [37] replaces parameter updates with verbal self-critique: an actor produces a trajectory, an evaluator scores it, and a self-reflection module writes a natural-language post-mortem that is appended to the next attempt’s prompt. The authors describe the text feedback as a _semantic gradient_ , a specific improvement direction expressed in tokens rather than numbers, and observe, somewhat counter-intuitively, that more reflections are not better: the buffer is capped at 1–3 entries because larger buffers drown the agent in contradictory advice. Compression of memory is often more important than its accumulation, and this is a theme we will return to. 

5 

**Table 1:** The surveyed agent-memory systems ranked across three axes; • marks a primary, defining property, ◦ a secondary one. 

|**System**|**Year**|**Mechanism**|**CoALA**<br>**W E S P **|**R**|**O**<br>**t **|**per.**<br> **Rc Rf Key idea / signature**|
|---|---|---|---|---|---|---|
|_Memory stream_|_s, OS hi_|_erarchies, and verba_|_l reinforce_|_me_|_n_|<br>_t_|
|Generative<br>Agents [32]|2023|Weighted memory<br>stream|• ◦|||• • Recency–importance–relevance scoring of an observation<br>stream; reflection synthesizes higher-level insights|
|MemGPT /<br>Letta [31,23]<br>Reflexion [37]|2023<br>2023|Tiered OS<br>memory+paging<br>Verbal-RL<br>critique buffer|• ◦◦<br>•<br>•|•||◦◦Memory as a virtual OS; the agent self-manages tiers via<br>tool calls, with memory-pressure “page faults”<br>◦• Verbal self-critique as a “semantic gradient” appended to<br>the next attempt; capped1–3-entry buffer|
|_Graph-based a_|_nd temp_|_oral memory_|||||
|HippoRAG<br>1/2 [10,11]|2024 /<br>2025|KG+PPR|•|◦||•<br>One Personalized-PageRank pass over a schemaless KG<br>replaces multi-hop LLM traversal; v2 fixes the factoid<br>regression|
|Zep / Graphiti<br>[33]<br>MAGMA [17]|2025<br>2026|Bi-temporal<br>knowledge graph<br>Multi-graph+<br>temporal engine|◦•<br>• •|•<br>•|<br>|• ◦Facts carry`valid_at`/`invalid_at`timestamps;<br>embedding+BM25+graph search with async indexing<br> •<br>Multi-relational entity/episodic/temporal/semantic<br>subgraphs plus a temporal inference engine that<br>normalizes time|
|_Mutable, learne_|_d, and_|_bio-inspired memory_|||||
|A-MEM [46]|2025|Self-editing<br>Zettelkasten notes|◦•|◦||◦• Atomic linked notes; adding a note rewrites the<br>descriptions and tags of the old notes it links to (“memory<br>evolution”)|
|Memory-R1<br>[48]|2025|RL-trained policy|•|•||• An RL policy learns ADD/UPDATE/DELETE/NOOP<br>from downstream answer reward; only∼152training<br>pairs needed|
|LightMem [8]|2025|Sleep-time<br>consolidation|•<br>◦|◦||<br>• Atkinson–Shiffrin stages; consolidation moved off the<br>inference path into a background “sleep” phase|
|SleepGate<br>[45]|2026|KV-cache<br>consolidation|•|||• Sleep-inspired consolidation applied to the KV-cache<br>itself, targeting proactive interference from stale<br>memories|
|EverMemOS<br>[13]|2026|MemCell /<br>MemScene store|• •|•||• ◦Heterogeneous items become_MemCells_aggregated into<br>_MemScenes_for structured long-horizon retrieval|
|Nemori [29]|2025|Surprise-gated<br>admission|• ◦|•||◦A free-energy / predictive-coding rule admits an episode<br>only when it is a “surprise” vs. current knowledge|
|_Production fram_|_eworks_|_and multi-strategy r_|_etrieval_||||
|Mem0 [4]|2025|Extract-and-<br>update facts|•|•||• ◦One-line`add()`extracts atomic facts, deduplicates, and<br>ADD/UPDATEs on conflict; vector+optional graph/KV|
|Cognee [40]|2024|<br>ECL typed-KG<br>completion|•|•||l <br> •<br>An Extract–Cognify–Load pipeline builds a typed-schema<br>KG and answers via internal graph completion|
|MemPalace<br>[19]|2026|Spatial hierarchy,<br>0-LLM write|◦•|•||◦<br>Wings/rooms/halls “palace” with a deterministic<br>zero-LLM write path; headline recall was a vector-store<br>confound|
|Hindsight<br>[21]|2025|4 networks+<br>multi-strategy<br>RRF|• •|◦||• • Four epistemic networks<br>(world/experience/observation/opinion); TEMPR fuses<br>semantic+BM25+graph+time by RRF; dispositions|
|Framework<br>memories<sup>†</sup>|2023–<br>2025|Built-in<br>framework<br>memory|◦<br>◦•|◦||<br>• ◦LangMem (procedural self-prompt rewriting);<br>LlamaIndex (composable memory blocks+token<br>budget); CrewAI (shared weighted memory)|
|_Structured sciei_|_ntific me_|_i mory (this work)_|||||
|Theoria_(this_<br>_work)_|2026|Evidence+<br>community+<br>theory stack|•|•||• ◦Three-layer evidence+community+theory store:<br>multi-aspect claim extraction over a RAPTOR tree,<br>Leiden community-routed retrieval, typed<br>supports/contradicts links, and confidence-rated theory<br>statements|

6 

Table 1 gives a general overview of influential memory systems for AI agents that we detail below. It ranks systems by three axes: rows are grouped by _dominant mechanism_ (methodological taxonomy), CoALA memory type columns are the neuropsychological taxonomy ( **W** orking / **E** pisodic / **S** emantic / **P** rocedural), and operation emphasis columns represent the operational taxonomy ( **Rt** = retain/formation, **Rc** = recall/retrieval, **Rf** = reflect/management). 

### **2.3 Graphs and neuroscience** 

A parallel line of work treats memory as a graph. _HippoRAG_ [10] maps neocortex / parahippocampus / hippocampus onto an LLM doing open information extraction, a retrieval encoder that adds synonymy edges above a similarity threshold, and a schemaless knowledge graph; at query time it runs Personalized PageRank seeded by query entities instead of multi-hop LLM traversal, which is both cheaper and more accurate than one-shot RAG. _HippoRAG 2_ [11] fixes the first version’s weakness on simple factoid questions (where graph diffusion blurred easy cases) with a more careful integration of retrieved passages. The lesson is that such systems work exactly as well as their open information extraction does: many errors now come from entity extraction rather than from the graph search itself. 

_Zep / Graphiti_ [33] brings this idea to production with a _bi-temporal knowledge graph_ : every fact stores both _𝑡_ valid (when it became true) and _𝑡_ invalid (when it ceased to be true), so a “where did the user live in February?” query returns the right answer even after the user moves. Graphiti combines embedding search, BM25, and graph traversal, with asynchronous background extraction and indexing; it is one of the most developed graph memories for temporal recall. _MAGMA_ [17] couples multi-relational subgraphs (entity / episodic / temporal / semantic) with a temporal inference engine that normalizes temporal expressions into a chronological representation. 

### **2.4 Mutable, learned, and bio-inspired memory** 

Most of the systems above only _add_ elements, but human memory is continually re-consolidated. _A-MEM_ [46] casts each memory as a Zettelkasten note (raw content, timestamp, LLM-extracted keywords and tags, a generated contextual description, an embedding, and links); when a new note is added, the system links it to its nearest neighbors and, crucially, rewrites the descriptions and tags of the _old_ linked notes in light of the new one—a mechanism the authors call _memory evolution_ . 

_Memory-R1_ [48] takes the further step of _learning_ the memory-management policy: instead of hand-coded heuristics, an RL-trained agent chooses an operation (ADD/UPDATE/DELETE/NOOP) for each new item, rewarded by downstream answer correctness (PPO and GRPO converge to similar points). In their experiments, ∼152 QA pairs sufficed to beat strong prior systems; this is, in our view, one of the most promising directions in the area, even if the best ready-to-use systems today are not yet RL-trained. 

Several recent systems borrow explicitly from models of human memory. _LightMem_ [8] implements Atkinson–Shiffrin-style sleep-time consolidation, separating background consolidation from inference to speed up queries. _SleepGate_ [45] addresses _proactive interference_ —the degradation of retrieval as stale information accumulates—by 

7 

updating the KV-cache rather than an abstract store. _EverMemOS_ [13] introduces _MemCells_ that aggregate heterogeneous items into _MemScenes_ for retrieval, and _Nemori_ [29] applies a free-energy / predictive-coding principle, admitting a new episode into memory only when it is a _surprise_ relative to what the existing knowledge predicts. 

### **2.5 Open-source frameworks** 

In practice most developers use a ready-made framework. _Mem0_ [4] is among the most popular: a one-line `add()` extracts facts and preferences with an LLM, deduplicates, and updates on conflict, while `search()` ranks by relevance/importance/recency over a vector store with optional graph and key-value backends; it remains an easy and strong baseline. _Cognee_ [40] ships a standalone “Extract → Cognify → Load” (ECL) pipeline that builds a typed knowledge graph and answers via graph completion. Agent frameworks bundle their own memory: LangChain’s LangMem implements procedural memory by letting the agent rewrite its own system prompt,<sup>3</sup> LlamaIndex offers composable memory blocks with a priority token budget,<sup>4</sup> and CrewAI provides a shared multi-agent memory with explicit recency/similarity/importance weights.<sup>5</sup> During 2025 all three major providers (OpenAI, Anthropic, Google) added persistent, importable/exportable memory, with philosophically different defaults—transparent automatic memory versus memory loaded only through explicit, user-visible tool calls.<sup>6</sup> 

The recent _MemPalace_ [19] framework is an instructive cautionary tale for exactly the evaluation problems this paper studies. It organizes memory as a spatial hierarchy (a “memory palace” of wings, rooms, halls, tunnels, closets, and drawers) with a zero-LLM write path and aggressive regex-based compression, which is an elegant, human-interpretable design. However, independent analysis showed that its headline result (96 _._ 6% Recall@5 on LongMemEval, claimed as the highest published) was obtained in a mode that stores documents verbatim in a vector database and uses its default embedding search, with none of the “palace” machinery in the retrieval path; enabling the palace structure _lowered_ the numbers. In this work, we aim for a controlled leaderboard that makes all parameters explicit and can distinguish between the contributions of different components. 

### **2.6 A modern example: Hindsight** 

As a detailed example of a strong contemporary system we use _Hindsight_ [21], which partitions memory into four epistemically distinct networks: 

- _world_ network of objective facts, 

- _experience_ network of first-person agent experience, 

- _observation_ network of synthesized entity profiles, and 

> 3 `https://langchain-ai.github.io/langmem/` 

> 4 `https://www.llamaindex.ai/` 

> 5 `https://github.com/crewAIInc/crewAI` 

> 6 `https://code.claude.com/docs/en/memory` 

8 

• _opinion_ network of subjective beliefs with confidence scores and timestamps. 

In this approach, “what I _know_ about _𝑋_ ” can be queried separately from “what I _think_ about _𝑋_ .” 

The Hindsight architecture has several components. The retrieval component of Hindsight, TEMPR, runs four strategies in parallel (semantic, BM25 keyword, graph activation, and temporal-graph parsing), fuses them with reciprocal rank fusion [5] RRF( _𝑓_ ) =<sup>�</sup> _𝑖_<sup>1/(</sup><sup>_𝑘_+ rank</sup> _𝑖_<sup>(</sup><sup>_𝑓_)),andappliesacross-encoderreranker.Itsreflection</sup> component, CARA, processes memory in priority order (opinions and observations before raw facts) and writes new beliefs back into the opinion network, closing a learning loop. 

Hindsight also exposes tunable _disposition parameters_ (skepticism, literalism, empathy) that shape how aggressively the agent commits to evidence during reflection. It reports large margins on conversational memory benchmarks; e.g., on LongMemEval S it surpasses full-context GPT-4o by more than 23 points using a 20B open model, and it tops the BEAM 10M-token benchmark at 64 _._ 1% versus 40 _._ 6% for the next system. Hu et al. [16] rank it first on their aggregate Agent Memory Benchmark, and we include Hindsight as one of our evaluated systems. 

### **2.7 Memory and scientific-QA benchmarks** 

The most common memory benchmarks remain LongMemEval [43], LoCoMo [27], BEAM [39], and MemoryArena [12], all of which target conversation. LoCoMo uses very long multi-session dialogues (∼300 turns, 35 sessions) with five question types; since long-context models can partly solve it by ingesting the whole dialogue, scores depend heavily on the backbone LLM. LongMemEval (500 questions) evaluates information extraction, multi-session reasoning, temporal reasoning, knowledge updates, and abstention, and is harder to solve by brute-force context. BEAM scales to 10M tokens and 2 _,_ 000 validated questions over ten abilities including contradiction resolution. MemoryArena and its relative Mem2ActBench [36] measure retrieval- _to-action_ grounding inside agentic tasks and expose the benchmark-to-deployment gap that we discussed above. HaluMem [3] measures hallucinations during memory formation, which matters because an LLM-fabricated fact written at storage time can persist in memory storage forever. 

Scientific QA benchmarks are closer to our setting but evaluate a different object. QASA [22] and PeerQA [2] focus on article- or document-level scientific QA, while OpenScholar/ScholarQABench [1] and ResearchQA [49] evaluate multi-paper literature synthesis and long-form scholarly answering. Our benchmark instead treats the evaluated object as a persistent _memory system_ : papers are ingested into a memory store, systems retrieve under explicit budget and modality constraints, and the same synthesizer and judge are held fixed across memory representations. We are not aware of a prior benchmark that uses full-paper scientific corpora across two domains, varies retrieval budget and modality while holding the synthesizer fixed, audits rubrics against full cited-paper text, and cross-validates LLM-as-judge with a second frontier model and human side-by-side votes. 

9 

**Table 2:** Memory systems evaluated in this work. “Native chars” is the mean retrieved-context size per query in the uncapped run on Paim; per-system implementation details are given below. 

|**System**|**Representation / ingest unit**|**Native chars**|**Design**|
|---|---|---|---|
|Simple RAG|raw chunks / 1K-char chunks|20_,_635|cosine top-_𝑘_baseline|
|Theoria|evidence + theories / full paper|28_,_857|community-routed, the-<br>ory layer|
|Mem0|atomic facts / 6K-char chunks|6_,_222|extract-and-update|
|Hindsight|narrative facts / full paper item|19_,_078|4-network temporal RRF|
|Cognee|typed KG / full paper|281_,_524|ECL pipeline, KG com-<br>pletion|
|Graphiti / Zep|temporal graph + episodes / full<br>paper episode|2_,_596_,_250|bi-temporal, label propa-<br>gation|
|Prism|claims + RAPTOR + links / full<br>paper|—|multi-aspect typed claims|
|Direct Read|raw papers + filler / full corpus|1_,_956_,_298|oracle-anchor diagnostic|

## **3 Systems evaluated in this work** 

We evaluate eight memory/retrieval systems plus a no-retrieval base model, chosen to span the methodological families of Section 2. Table 2 summarizes them; the “Native chars” column reports the mean retrieved-context size per query in the uncapped run on Paim and already foreshadows one of our central points: these volumes differ by more than two orders of magnitude, so any comparison that does not control for them is comparing budgets as much as architectures. 

We group the eight systems by what they preserve and how they retrieve. We mostly used the out-of-the-box configurations that a developer would use by default (except when controlling for variables such as token budgets); each system is integrated through a thin adapter in the released `scibench` harness<sup>7</sup> that exposes a uniform `ingest` / `retrieve` interface and translates per-system hyperparameters ( `top_k` , episode budgets, edge/node limits, RRF’s _𝑘_ ) into the harness’s per-query budget target. 

1. **Simple RAG** [24], a chunk-RAG baseline. It ingests 1K-character overlapping chunks and returns the cosine top- _𝑘_ to an external synthesizer. It preserves raw text but no structure, and it is our null hypothesis: any memory architecture is theoretically supposed to beat it under a matched budget. 

2. **Mem0** [4], an extract-and-update memory. An LLM extracts atomic facts from ∼6K-character chunks under an ADD/UPDATE/DELETE/NOOP policy (the 6K window is forced by an 8K-token embedding cap), and an optional BM25 hybrid (the `fastembed` backend) is fused at retrieval time. Its native context is the smallest of all systems (∼6K chars). 

3. **Hindsight** [21], a narrative/temporal memory. It ingests each paper as an item into four parallel networks (world / experience / observation / opinion), retrieves with 

> 7Released as part of our _Scientific Recall Bench_ repository, `https://gitlab.com/quantellence/ research/scientific-recall-bench` . 

10 

reciprocal rank fusion [5] of semantic + BM25 + graph + temporal channels, and applies a cross-encoder reranker. The server-side recall caps its return at ∼19K characters regardless of the requested `n` , so it does not really honor the budget parameter; it also expects conversation exchanges rather than 20K-token papers, and its ∼300KB ingest cap rejected three papers. 

4. **Cognee** [40], a knowledge-graph memory. Its Extract–Cognify–Load (ECL) pipeline builds a typed Pydantic-schema KG and answers via `GRAPH_COMPLETION` (internal synthesis). Its chunks are coarse (∼19K characters each), so the budget grid collapses to a coarse 1/2/3-chunk grid. 

5. **Graphiti / Zep** [33], a bi-temporal graph memory. It ingests each paper as one `EpisodeType.text` episode and returns edges (LLM-extracted fact strings, ∼200 chars each) and nodes (∼500 chars each) plus, in the native run, the matched episode body, that is, a full ∼20K-token paper, which is why its native context reaches 2 _._ 6M characters per query. The “KG-only” mode used in the budget sweep sets `include_episodes=false` to isolate the graph from the raw-episode channel, and `top_k` is applied per modality rather than globally. 

6. **Theoria** and its ablation **Prism** (our systems, Section 5). Theoria ingests at the paper level, runs five LLM passes per chunk for multi-aspect evidence extraction, builds a RAPTOR collapsed tree, performs Leiden community detection, and produces theory statements; its BM25 sparse vectors are stored as SQLite BLOBs alongside the evidence and theory tables. Prism keeps the multi-aspect extraction and a single RAPTOR tree with typed cross-document links but answers via internal synthesis, so it isolates “extraction + RAPTOR” from “community routing + theory aggregation.” 

7. **Direct Read Anchored** , a long-context oracle. It concatenates the gold-source papers plus random filler up to a 500K-token budget and runs no LLM at retrieval time. It is a diagnostic anchor (run on a 15-question subset), not a fair competitor. 

8. **Base model** has no retrieval mechanism, sees no retrieved context, and answers from parametric knowledge alone. It serves as a floor and, since the corpora are public arXiv papers, as a contamination probe. 

Per-system ingest cost, wall-clock, and configuration files are released in the artifact. 

## **4 Datasets** 

We release two full-text scientific QA datasets.<sup>8</sup> Both use open-access, markdownconverted papers, an 8 question-type × 3 difficulty-tier schema, and auditable rubrics grounded in the papers. The two corpora differ in domain and lexical character, which lets us separate effects of memory architectures from effects of a specific subject domain. 

**Public AI Memory (Paim).** 81 full-text papers (1 _._ 10M words; 2 _._ 15M tokens after MinerU markdown extraction [30]) on LLM agent memory, RAG, scientific agents, 

> 8Both datasets, including the paper corpora, structured notes, questions, and audited rubrics, are available at `https://huggingface.co/datasets/quantellence/srb-data` . 

11 

long-context, and adjacent retrieval and cognitive-architecture work; in part, it is the literature surveyed in Section 2. We also include 103 structured paper notes (under a 10-section schema); 22 production frameworks without an arXiv mirror (e.g., Letta, Cognee, MemPalace, and the CrewAI/LlamaIndex/LangChain memory subsystems, plus a pair of foundational psychology papers) are notes-only. The QA part comprises 66 main questions across three difficulty tiers (9 L1, 39 L2, 18 L3) plus a 10-question holdout set. Question types include factual, mechanistic, quantitative, enumeration, conditional, cross-document, negative, and synthesis; most questions combine two or more types. 

**Public Transformers (PTr).** 252 full-text papers (arXiv 2507.* through 2604.*) on attention mechanisms, positional encodings, mixture-of-experts, long-context KV management, training, multimodality, and reasoning, organized into 15 thematic clusters. PTr includes 98 audited questions (34 L1, 41 L2, 23 L3), designed to cover ∼48% of the corpus by source-note references and to probe the full paper-ID range. Compared to Paim, its named entities—model names, kernel names, and hyperparameters—are denser and more lexically distinctive, a property that turns out to matter a great deal for retrieval modality (Section 6.3). 

**Question schema.** The three difficulty tiers capture how much of the corpus an answer must touch. L1 questions are answerable from a single span in a single paper (e.g., a reported score); L2 questions require a mechanism, a multi-part enumeration, or a comparison within one or two papers; L3 questions require synthesizing evidence across several papers (e.g., comparing thresholds reported by three different systems). The question types are orthogonal to the tiers: factual and quantitative questions probe precise recall, mechanistic and conditional questions check whether qualifiers survive ingestion, enumeration and cross-document questions target coverage, negative questions probe calibrated abstention, and synthesis questions are intended for cross-paper aggregation. This design deliberately stresses the parts of context restoration that compact summaries tend to discard. 

**Rubric audit.** Each question has a gold answer decomposed into _must-have facts_ , each supported by a span in the corpus. We additionally ran a 6-dimension audit by parallel reading agents, asking: 

(1) is every must-have fact verifiable in the cited paper? 

- (2) do the rubric’s source pointers exist in the corpus? 

- (3) is the answer stable (pinned to the paper, not to volatile repository state)? 

- (4) can a frontier LLM answer it from parametric knowledge alone? 

- (5) is the difficulty label still right? 

- (6) does the rubric require precision that the cited paper does not actually claim? 

On Paim, the audit found that 35 questions in the first version had at least one defect (Table 3); these questions were rewritten and re-audited. The same procedure was applied to PTr, and we release only successfully audited questions. This audit is itself part of the contribution: benchmark errors that are invisible at the leaderboard level (a 

12 

**Table 3:** Audit-class statistics on the first version of Paim (76 audited questions). Defective questions were rewritten and re-audited (36/37 clean on the first re-pass, 1 patched again). 

|**Class**|**Defect**|**#**|
|---|---|---|
|A|rubric fact not verifiable in the cited paper|11|
|B|dependency on internal (non-corpus) data|5|
|C|volatile value (repository state, stars, README)|3|
|D|rubric over-specifies precision the paper does not claim|12|
|E|answerable from parametric knowledge alone (kept, flagged)|5|
|Multi-c|lass (two classes simultaneously)|6|
|**Total q**|**uestions rewritten**|**37**|

must-have fact that lives only outside the corpus, or a rubric that demands more precision than the paper offers) can silently penalize systems that answer honestly. 

**Why full text matters.** The same systems behave very differently on full papers than on a smaller summary corpus we previously tried. Structured-notes ingestion sees a pre-extracted, high-density abstract; full-paper ingestion must contend with introductions, related-work sections, numbers dispersed across tables, redundant restatements, and inconsistent OCR around equations introduced by the open-source MinerU PDF-tomarkdown pipeline [30] we use for extraction. Compact representations tend to lose qualifiers and conditions, which are exactly what L2 and L3 questions ask about. We provide full details of our data collection and auditing pipeline, following the W3C PROV-O `prov:wasGeneratedBy` pattern, in the release; Section 3 documents per-system ingestion, and Table 3 summarizes the audit findings. 

**Two examples.** To illustrate the question style, below we show two representative questions with their gold rubrics; we follow each one through the systems’ answers in Section 7. 

**PQ40** (Paim, L2; enumeration + cross-document). 

**Q:** “MemoryAgentBench evaluates four core competencies essential for memory agents. List them. Which of the four is most often neglected by prior benchmarks like LoCoMo and LongMemEval?” 

**Gold:** the four competencies are _accurate retrieval_ , _test-time learning_ , _longrange understanding_ , and _selective forgetting_ ; selective forgetting is the most neglected—LoCoMo and LongMemEval test recall under accumulation but do not stress-test invalidation of stale information. **Sources:** [15], [27], [43] 

**TX17** (PTr, L2; quantitative + cross-document synthesis). 

**Q:** “Several papers argue that sparse/linear attention only pays off above a context-length threshold. Compare the thresholds reported by at least three of FSA, SALS, Ring-flash-linear-2.0, HSA-UltraLong, and Kimi Linear, and identify the most aggressive throughput claim at 1M+ tokens.” **Gold:** Kimi Linear is the most aggressive (6× decoding throughput at 1M tokens); FSA reports up to 1 _._ 25× training / 1 _._ 36× prefill speedup, SALS 

13 

||GET /theories<br>Cold-start bootstrap|POST /retrieve<br>Evidence retrieval|POST /observe<br>Insert + theoryupdate|
|---|---|---|---|
|**Theory layer**|Belief statements + confidence +<br>supports / contradicts|Community-scoped<br>theory matching|Deduplication check<br>(cosine > 0.80)|
|**Community layer**|Two-resolution<br>Leiden clustering|Sparse top-5 membership<br>per evidence item|Community graph<br>(bridge expansion)|
|**Evidence layer**|Multi-aspect extraction(numbers,<br>mechanisms, failures, conditions, tables)|RAPTOR<br>collapsed tree|Typed cross-doc links (supports /<br>contradicts / extends / depends)|

**Figure 2:** The architecture of _Theoria_ . The three-layer evidence + community + theory stack shares the same store with three agent endpoints: `GET /theories` for cold-start bootstrap, `POST /retrieve` for community-routed evidence retrieval, and `POST /observe` for inserting new findings (which can update or contradict existing theories). 

6 _._ 4× KV compression at 4K, Ring-flash-linear-2.0 advantages pronounced beyond 8K, and HSA-UltraLong _>_ 90% retrieval at 16M tokens. **Sources:** [47], [28], [25], [14], [20] 

## **5 Theoria: a three-layer scientific-memory system** 

We introduce _Theoria_ , our structured scientific-memory system and one of the systems evaluated below. Theoria is built around the hypothesis that scientific memory needs both fine-grained evidence retrieval (table values, precise conditions, failure modes) and coarse-grained structure for cross-paper synthesis (which papers belong together, where their claims disagree). Most production systems pick one: chunk RAG [24] preserves text but not structure, while knowledge-graph completion in Cognee [40] imposes structure but loses raw-text fidelity. 

We therefore view Theoria both as a systems contribution and as a test subject for the evaluation protocol: if structure helps, it should show up under matched retrieval budgets. Theoria stacks three layers so that evidence retrieval and theory-level cross-paper aggregation share the same store but expose distinct interfaces (Fig. 2). 

**Evidence layer.** Theoria performs multi-aspect extraction over section-aware ∼6Kchar chunks, with five LLM passes that extract numbers, mechanisms, failures, conditions, and tables as self-contained claims. A RAPTOR collapsed tree [35] builds one summary level above the leaves via Ward agglomerative clustering. Typed cross-document links (supports / contradicts / extends / depends-on) are discovered by filtering: each new claim’s top-5 embedding-nearest existing claims are passed to an LLM disambiguator, and typed relations become rows of a `links` table. After ingesting Paim, Theoria holds 26 _,_ 782 evidence items plus RAPTOR summary nodes and 1 _,_ 275 typed cross-document links. 

**Community layer.** We run two-resolution Leiden clustering [41] on the evidence graph (with edges between embedding-near items) and assign items to fine communities, weighted by cosine similarity to community centroids. Community-to-community edges drive expansion at retrieval time. On Paim, this yields ∼70 coarse and ∼470 fine communities, with average degree ∼12. The intuition is that a research question rarely lands on a single isolated fact; routing through communities lets retrieval pull in the cluster of related evidence that a synthesis answer needs. 

14 

**Theory layer.** “Theories” are natural-language statements anchored to a community, carried at low / medium / high confidence, promoted by supporting-evidence count and demoted by contradiction count. When a new finding arrives, only theories anchored to its top-5 communities (plus their direct graph neighbors) are considered as candidates, narrowing the comparison from all theories to typically 10–40. Cosine similarity above 0 _._ 25 counts as a match; on no match (and below the deduplication threshold of 0 _._ 80) the finding seeds a new theory. On Paim this produces ∼637 theories. 

These layers support three agent endpoints (Fig. 2): 

- (i) `GET /theories` returns the theory table filtered by confidence and grouped by community—an agent’s cold-start bootstrap (“what does this corpus believe?”); 

- (ii) `POST /retrieve` embeds the query, picks the top-5 fine communities, optionally expands to neighbors, scores by entropy-weighted cosine across RAPTOR levels, and returns the top- _𝑘_ deduplicated items plus their one-hop linked items; 

- (iii) `POST /observe` ingests a new finding: extract evidence, assign communities, and update existing theories or seed new beliefs. 

Below, we evaluate only Theoria’s `POST /retrieve` endpoint under matched-budget single-shot QA. This is a deliberately conservative evaluation: it tests whether communityrouted evidence and theory-linked retrieval improve answer quality, but it does not use the full agentic loop. The cold-start `GET /theories` endpoint and the iterative `POST /observe` loop— the parts of Theoria most unlike RAG, and the ones that have proven most useful in our internal use—are _not_ exercised by one-shot QA; evaluating them properly requires a sequential research-agent benchmark, which we leave to future work. 

**Prism (ablation).** Our second system, _Prism_ , shares Theoria’s multi-aspect extraction but replaces the community and theory layers with a single RAPTOR tree and typed links, returning answers via internal synthesis rather than external retrieval. Prism therefore isolates “multi-aspect extraction + RAPTOR” from “community routing + theory aggregation.” Because internal synthesis has no measurable retrieved-context volume, Prism does not participate in the budget sweeps. 

## **6 Experimental evaluation** 

### **6.1 Experimental setup** 

We run all memory systems on Paim (81 papers, 66 questions) and on PTr (252 papers, 98 questions). External-synthesis systems use gpt-4.1-mini at temperature 0 as the shared synthesizer; internal-synthesis systems (Cognee, Prism) return their own answer using whatever model they invoke internally. The primary judge is Gemini 3.1 Pro, scoring each answer against the gold rubric on five dimensions: accuracy, completeness, specificity, hallucination avoidance, and retrieval quality. We report the _no-retrieval composite_ , the mean of the first four dimensions on a 0–10 scale, so that internal- and external-synthesis systems are scored on the same footing, and we use the audited rubrics of Section 4 throughout. 

15 

**Table 4:** Experimental results on Paim (Gemini 3.1 Pro judge, 0–10 scale). 

|||**Na**|**tive (66 qu**|**estions)**||_𝐵_≈|10K|_𝐵_≈|30K|_𝐵_≈5|0K|
|---|---|---|---|---|---|---|---|---|---|---|---|
|**System**|**Avg**|**L1**(9q)|**L2**(39q)|**L3**(18q)|**chars**|**score**|**chars**|**score**|**chars**|**score**|**chars**|
|Theoria|6_._82|8_._14|6_._64|6_._54|29K|6_._32|16K|7_._19|41K|7_._60|60K|
|+BM25 hybrid|6_._97|8_._09|6_._51|**7**_._**22**|28K|**6**_._**70**|16K|**7**_._**41**|40K|7_._34|57K|
|Mem0|5_._65|8_._44|5_._35|4_._90|6K|6_._43|11K|6_._97|32K|7_._40|53K|
|+BM25 hybrid|5_._98|8_._33|5_._54|5_._74|6K|6_._54|11K|7_._13|33K|7_._48|54K|
|Simple RAG|**7**_._**22**|8_._28|**7**_._**14**|6_._86|21K|6_._27|11K|7_._25|31K|7_._58|52K|
|+BM25 hybrid|7_._15|**8**_._**47**|6_._77|7_._03|21K|6_._64|10K|7_._30|32K|**7**_._**77**|53K|
|Hindsight|6_._81|7_._86|6_._44|7_._10|19K|6_._63|19K|6_._53|19K|6_._72|19K|
|Cognee|6_._20|7_._14|6_._13|5_._89|282K|5_._16|19K|5_._28|37K|5_._45|56K|
|Graphiti|8_._04|8_._49|7_._84|8_._24|2_,_552K|5_._05|21K|5_._27|59K|5_._19|96K|
|Direct Read (on 15q)|6_._67|6_._30|6_._15|7_._55|1_,_968K|Oracle|anchor;|budgets|exceede|d||
|Prism (ablation)|6_._20|8_._14|5_._92|5_._83|—|Interna|l synthes|is (no re|trieval v|olume)||
|Base model|2_._64|1_._50|2_._51|3_._49|0|2_._64|0|2_._64|0|2_._64|0|

**Native and budget-targeted configurations.** There are two configurations. In the _native_ configuration retrieval is uncapped and each system returns whatever it would out of the box. In the _budget-targeted_ configuration we re-query the already-ingested memory at three character targets _𝐵_ ∈{10K _,_ 30K _,_ 50K} by changing only retrieval settings ( `top_k` or its equivalent); the corpus, the stored representation, and the synthesis pipeline are unchanged. This separation is deliberate: the native track measures out-ofthe-box product behavior, while the budget-targeted track measures evidence-selection efficiency at a fixed context cost. We calibrate the retrieval settings from each system’s mean characters per retrieved unit on the native run (Theoria 1 _,_ 151, Hindsight 432, Mem0 292, Cognee 18 _,_ 768, Graphiti edges+nodes 223, Simple RAG 999). 

**Two ablation variants.** For Graphiti, the budgeted runs additionally disable episode retrieval ( `include_episodes=false` ); the system then returns only edges (LLM-extracted fact strings, ∼200 chars each) and nodes (∼500 chars each), because each episode is a ∼20K-token full-text paper that would by itself blow any budget. This “KG-only” Graphiti is an ablation that isolates the graph representation from the raw-episode channel. Rows marked “+ BM25” are the sparse–dense hybrids: BM25 fused with the existing dense retrievers by reciprocal rank fusion at _𝑘_ = 60, computed without re-ingesting the corpus. 

Three systems cannot take part in the budget sweep: Prism (internal synthesis, no measurable retrieved-context volume), Direct Read (an oracle anchor at ∼2M chars/query that exceeds every budget, run on its 15-question subset), and the base model (no retrieval). 

### **6.2 Results on Paim: native and budget-targeted retrieval** 

Tables 4 and 5 report the full results on Paim and PTr; Figure 3 shows the Paim results graphically, and Figure 4 plots the budget sweeps. We find three patterns in Table 4. 

First, _L1 is largely saturated._ Every retrieval-augmented system other than Direct Read reaches ≥ 7 _._ 7 on L1 in the native run, with little spread; systems separate only from L2 downward. Basic factual recall is therefore no longer a useful discriminator among memory architectures—it mainly verifies that ingestion and retrieval are wired 

16 

<!-- Start of picture text -->
9 Simple RAG Hindsight Cognee<br>Theoria Direct Read Prism<br>8<br>7<br>6<br>5<br>4<br>3<br>L1 (n=9) L2 (n=39) L3 (n=18)<br>Composite score (Gemini)<br><!-- End of picture text -->

**Figure 3:** Native Paim scores by difficulty tier (Gemini judge, audited rubrics). L1 is largely saturated; L2 fans the systems out; on L3 the long-context Direct Read anchor (∼2M chars/query) leads, followed by Hindsight and Simple RAG. These are the “Native” columns of Table 4. 

up at all. 

Second, _native L3 is dominated by raw context volume._ The two highest native L3 scores belong to the two highest volume systems. Graphiti (native, 8 _._ 24 on L3) returns ∼2 _._ 55M chars/query because it ingests each paper as one episode, so every matched episode adds the whole ∼20K-token paper into synthesis; Direct Read (7 _._ 55) is a diagnostic with ∼2M chars/query of gold sources plus random filler. Without budget control, neither gain can be attributed to architecture: a system that hands the synthesizer two million characters of relevant raw text is, in effect, a semantically filtered long-context reader, not evidence that temporal-graph memory is intrinsically better. 

Third, _under budget control, the architectural premium over chunk RAG is small or negative on Paim._ At the fair-comparison anchor _𝐵_ ≈ 30K (the natural volume of several systems), Simple RAG 7 _._ 25 ≈ Theoria 7 _._ 19 _>_ Mem0 6 _._ 97 _>_ Hindsight 6 _._ 53 _>_ Cognee 5 _._ 28 ≈ Graphiti (KG) 5 _._ 27. The KG-only Graphiti row lands at the bottom: its native wins were entirely due to the raw episode bodies, not the graph. Simple RAG, Theoria, and Mem0 form a tight upper cluster that scales monotonically with budget (∼6 _._ 3 at 10K, ∼7 _._ 2 at 30K, ∼7 _._ 6 at 50K), staying within 0 _._ 3 points of one another. Hindsight saturates at ∼19K chars regardless of `n` because its server caps recall, so its three budget columns are nearly identical; Cognee’s chunks are ∼19K each, mapping the budget grid onto `top_k` = 1/2/3, too coarse for a real curve. 

Figure 3 visualizes per-tier scores for external synthesis systems: L1 is saturated, L2 distinguishes between the systems, and on L3 the long-context Direct Read anchor leads, followed by Hindsight and Simple RAG, which is again a volume effect rather than an architecture effect. 

**BM25 hybrid on Paim.** For Mem0, Simple RAG, and Theoria we additionally evaluate a BM25-over-RRF hybrid [5, 34] that fuses the sparse and dense retrievers ( _𝑘_ = 60) without re-ingesting the corpus; these are the rows marked “+ BM25 hybrid” in Table 4. On Paim the lift is uneven. In the native run it is small (+0 _._ 15 for Theoria, +0 _._ 33 for Mem0, −0 _._ 07 for Simple RAG); under budget control BM25 is most useful at low and mid budgets (+0 _._ 4 at 10K, +0 _._ 1 to +0 _._ 2 at 30K) and turns slightly negative at 50K for Theoria (−0 _._ 26). The picture on Paim is that retrieval modality is not decisive 

17 

**Table 5:** Experimental results on PTr (Gemini 3.1 Pro judge, 0–10 scale). 

|||**Nati**|**ve (98 ques**|**tions)**||_𝐵_≈|10K|_𝐵_≈|30K|_𝐵_≈|50K|
|---|---|---|---|---|---|---|---|---|---|---|---|
|**System**|**Avg**|**L1**(34q)|**L2**(41q)|**L3**(23q)|**chars**|**score**|**chars**|**score**|**chars**|**score**|**chars**|
|Theoria+BM25|8_._67|9_._75|**8**_._**77**|7_._09|26K|8_._21|15K|**8**_._**96**|36K|9_._21|50K|
|Mem0+BM25|8_._10|9_._54|7_._83|6_._22|7K|**8**_._**42**|11K|8_._88|34K|**9**_._**24**|57K|
|Simple RAG+BM25|**8**_._**74**|**9**_._**79**|8_._70|**7**_._**37**|21K|7_._94|11K|8_._88|32K|9_._22|53K|
|Theoria (dense)|8_._23|9_._70|8_._23|6_._22|28K|7_._92|16K|8_._54|39K|8_._96|55K|
|Mem0 (dense)|7_._73|9_._60|7_._16|5_._72|7K|8_._21|11K|8_._74|33K|8_._95|55K|
|Simple RAG (dense)|8_._31|9_._66|8_._07|6_._64|21K|7_._83|10K|8_._45|31K|8_._72|52K|
|Base model|1_._78|1_._76|1_._66|2_._06|—|1_._89|0|1_._81|0|1_._70|0|

**Table 6:** Experimental results on the 80-paper subset of PTr (48q, Gemini 3.1 Pro judge). 

|||**Headline (4**|**8 questions)**|,_𝐵_=50K||_𝐵_≈|10K|_𝐵_≈|30K|_𝐵_≈|50K|
|---|---|---|---|---|---|---|---|---|---|---|---|
|**System**|**Overall**|**L1**(16q)|**L2**(20q)|**L3**(12q)|**chars**|**score**|**chars**|**score**|**chars**|**score**|**chars**|
|Mem0+BM25|8_._60|9_._67|8_._05|8_._08|55K|**8**_._**02**|11K|**8**_._**56**|33K|8_._60|55K|
|Theoria|8_._45|9_._88|**8**_._**24**|6_._92|54K|7_._27|16K|8_._36|38K|8_._45|54K|
|Mem0|**8**_._**72**|**9**_._**97**|8_._04|**8**_._**19**|53K|6_._56|10K|8_._33|32K|**8**_._**72**|53K|
|Simple RAG|8_._17|9_._64|7_._86|6_._73|52K|7_._33|10K|8_._02|31K|8_._17|52K|
|Hindsight|7_._07|9_._05|6_._39|5_._56|18K|7_._23|18K|7_._22|18K|7_._07|18K|
|Cognee|5_._97|8_._25|5_._62|3_._50|51K|5_._27|16K|5_._70|33K|5_._97|51K|
|Graphiti (KG)|7_._99|8_._50|7_._67|7_._83|96K|7_._61|21K|7_._87|58K|7_._99|96K|
|Base model|1_._99|1_._78|1_._82|2_._56|0|1_._99|0|1_._99|0|1_._99|0|

and architecture matters less than context budget. As we show next, PTr tells a very different story about modality. 

**Granularity caveats.** Three integrations diverge from their intended granularity (Section 3): Hindsight is fed whole papers rather than conversation exchanges, and its server cap rejects the largest three, Mem0 chunks at an arbitrary 6K window, and Graphiti’s episode is meant for short snippets rather than whole papers. We treat these as evaluation facts rather than defects, since they are the out-of-the-box choices a developer actually faces: a system has a specific granularity, size and semantic coherence of a unit it expects at ingestion, and violating their default parameters can change both quality and cost. Qualitative examples follow in Section 7; we present more in Appendix A. 

### **6.3 Results on PTr: a different domain and the BM25 hybrid effect** 

PTr has 252 full-text papers and 98 audited questions on the modern Transformer / long-context / multimodal literature; as noted, its named entities are denser and more lexically distinctive than Paim’s. Due to budget constraints we first compared all systems on a subset of PTr size-matched to Paim (Table 6), then evaluated the three strongest systems—Theoria, Mem0, and Simple RAG—and their three BM25 hybrid variants on the full corpus. Table 5 reports the full-corpus results, and the middle panel of Fig. 4 shows the budget curves. 

Again we make three observations. 

First, _dense retrieval is tighter, but architectural advantages persist._ At _𝐵_ ≈ 50K, 

18 

<!-- Start of picture text -->
8.0 9.50 9.0<br>7.5 Graphiti+ep. native (2.6M) 9.25 8.5<br>9.00 8.0<br>7.0<br>Simple RAGTheoria 8.75 7.5<br>6.5 Mem0 Hindsight 8.50 7.0<br>6.0 CogneeGraphiti (KG) 8.25 6.5<br>5.5 8.00 6.0 Mem0 + BM25 Hindsight<br>Mem0 + BM25 Mem0 Theoria Cognee<br>5.0 7.75 Simple RAG + BM25 Theoria + BM25 Simple RAG Theoria 5.5 Mem0 Simple RAG Graphiti (KG)<br>7.50 5.0<br>10K 30K 50K 100K 10K 30K 50K 10K 30K 50K 100K<br>Retrieved chars / query Retrieved chars / query Retrieved chars / query<br>(a)  Paim (66 questions) (b)  PTr (98 questions) (c)  PTr 80-paper subset (48q)<br>Composite score (Gemini)<br><!-- End of picture text -->

**Figure 4:** Budget sweeps: composite score vs. mean retrieved characters per query (log _𝑥_ -axis). _(a) Paim_ : Simple RAG, Theoria, and Mem0 form a tight upper cluster that scales monotonically with budget; Hindsight is a single point repeated because its server ignores the budget knob; Cognee and Graphiti’s KG output are flat and low. The dotted line marks Graphiti’s native score with episodes (2 _._ 6M chars). _(b) PTr_ (252 papers, 98 questions): filled markers / solid lines are hybrid retrieval (BM25+dense, RRF _𝑘_ = 60); open markers / dashed lines are dense-only. _(c) PTr 80-paper subset_ (size-matched to Paim, 48 questions; Table 6): the same six dense systems as in (a), plus the Mem0+BM25 variant. 

Theoria 8 _._ 96 ≈ Mem0 8 _._ 95 _>_ Simple RAG 8 _._ 72: structured and extracted memories pull ahead of chunk RAG, though the spread is small. Unlike Paim, the gap does not vanish under dense retrieval. 

Second, _BM25 lifts every evaluated system, and the three hybrids converge._ Adding BM25 over dense retrieval gives +0 _._ 50 for Simple RAG at 50K, +0 _._ 29 for Mem0, and +0 _._ 25 for Theoria; the lift is largest where the dense-only L3 score was lowest, suggesting that BM25 recovers exactly what dense cosine retrieval misses. At 50K the three hybrids are essentially tied (Mem0+BM25 9 _._ 24, Simple RAG+BM25 9 _._ 22, Theoria+BM25 9 _._ 21), even though their ingest costs differ by orders of magnitude (Theoria: ∼$30 of LLM extraction + ∼10h wall-clock; Mem0: hours of fact extraction; Simple RAG: ∼1 _._ 5 minutes of embedding). The convergence is on _average_ overall score only; tier-level behavior, latency, cost, provenance, and agentic interfaces all still differ. 

Third, _we find tier-level specialization._ At _𝐵_ ≈ 50K, Theoria+BM25 wins L1 (9 _._ 96) and ties Simple RAG+BM25 on L2 (9 _._ 21), but Mem0+BM25 wins L3 (8 _._ 63), so a question-conditioned ensemble of memory systems could in principle raise the ceiling further; we quantify both this headroom and the difficulty of realizing it in Section 8. The dense rows show the same but weaker pattern, with Theoria leading on L1/L2 and Mem0 on L3. 

Why does BM25 help so much more here than on Paim? We believe the key is PTr’s lexical structure: named methods, kernel names, and model identifiers, often phrased exactly as in the paper. Dense embeddings collapse synonyms but also conflate near-neighbors (e.g., different attention variants), whereas BM25 preserves the surface form and can pull the exact rare phrase a question hinges on. Table 6 shows the size-matched 80-paper / 48-question subset, which we ran before the full corpus to compare domains at the same scale as Paim and to choose systems for the full run. The subset was selected greedily so that its token count matches Paim (∼2 _._ 17M tokens) and 

19 

**Table 7:** Paired bootstrap 95% confidence intervals for the main contrasts (Gemini composite, _𝐵_ = 10 _,_ 000 resamples over questions). Δ is the mean per-question score difference, _𝑛_ is the number of common questions,<sup>∗</sup> marks an interval that excludes 0. 

|**Contrast**|Δ|95%**CI**||_𝑛_|
|---|---|---|---|---|
|_Paim, budget-targeted @_30_K (the fair-co_|_mparison_|_anchor)_|||
|Simple RAG−Theoria|+0_._01|[−0_._52_,_|+0_._53]|65|
|Theoria−Mem0|+0_._22|[−0_._28_,_|+0_._74]|65|
|Simple RAG−Mem0|+0_._28|[−0_._18_,_|+0_._76]|66|
|Simple RAG−Hindsight|+0_._72|[+0_._18_,_|+1_._30]<sup>∗</sup>|66|
|Simple RAG−Cognee|+1_._97|[+1_._29_,_|+2_._65]<sup>∗</sup>|66|
|Simple RAG−Graphiti (KG)|+1_._98|[+1_._16_,_|+2_._84]<sup>∗</sup>|66|
|_PTr (98 q) @_50_K: BM25 lift (hybrid_−|_dense)_||||
|Theoria+BM25−Theoria|+0_._20|[−0_._02_,_|+0_._44]|95|
|Mem0+BM25−Mem0|+0_._29|[+0_._11_,_|+0_._48]<sup>∗</sup>|98|
|Simple RAG+BM25−Simple RAG|+0_._50|[+0_._24_,_|+0_._79]<sup>∗</sup>|98|
|_PTr (98 q) @_50_K: among the three hybr_|_ids_||||
|Mem0+BM25−Simple RAG+BM25|+0_._03|[−0_._16_,_|+0_._22]|98|
|Mem0+BM25−Theoria+BM25|+0_._06|[−0_._20_,_|+0_._34]|97|
|Simple RAG+BM25−Theoria+BM25|+0_._01|[−0_._21_,_|+0_._24]|97|

the source notes of the 48 baseline questions are covered. At the 30K fair-comparison anchor we observed Theoria 8 _._ 36, Mem0 8 _._ 33, Simple RAG 8 _._ 02, Graphiti (KG) 7 _._ 87, Hindsight 7 _._ 22, and Cognee 5 _._ 70: the qualitative picture from Paim replicates, except that here the architectural systems (Theoria, Mem0) edge ahead of Simple RAG by 0 _._ 3–0 _._ 5 points instead of tying, which is why those three were chosen for the full run. 

The subset also tells a more nuanced story about scaling the corpus: comparing the same 48 baseline questions on the 80-paper subset vs. the full 252-paper corpus (same questions, more papers), dense-only Theoria moves 8 _._ 45 → 8 _._ 71 (+0 _._ 26), Mem0 8 _._ 72 → 8 _._ 52 (−0 _._ 20), and Simple RAG 8 _._ 17 → 8 _._ 08 (−0 _._ 09). This directional pattern is consistent with candidate pool dilution that pre-aggregation absorbs but atomic fact extraction does not; the combined 98-question numbers in Table 5 therefore mix this scale effect with the difficulty of the 50 expansion questions, so we report both views and avoid attributing the leaderboard change to corpus growth alone. Qualitative examples follow in Section 7; more are in Appendix A. 

### **6.4 Statistical significance of our main results** 

Since the question counts are modest, we quantify the uncertainty of the main differences with a paired bootstrap over questions: we resample question ids with replacement ( _𝐵_ = 10 _,_ 000), recompute the mean per-question score difference each time, and report the percentile 95% confidence interval. Pairing is over the common question set since every system answers the same questions; scores are the Gemini composite used throughout. This analysis re-aggregates the same judge scores reported elsewhere and involves no new inference. Table 7 shows the results. 

The conclusions agree with the claims we make from the point estimates. First, the Paim top cluster is a genuine statistical tie: the Simple RAG / Theoria / Mem0 

20 

<!-- Start of picture text -->
9.50<br>8 Gemini 3.1 ProSonnet 4.6 9.25 Theoria Mem0 Simple RAG 9.21 9.24 9.22<br>7 GPT-5.4<br>9.00 8.96 8.95<br>6<br>8.75 8.72 8.72<br>5<br>8.50 8.45<br>4<br>8.25 8.17<br>3<br>8.00<br>2<br>PTr subset PTr PTr<br>(80 pp, 48 q, dense) (252 pp, 98 q, dense) (252 pp, 98 q, +BM25)<br>(a)  Paim multi-judge (shared 6q subset) (b)  PTr corpus + modality at  𝐵 = 50K<br>Graphiti DRHindsight RAG Mem0Theoria PrismCognee Base<br>Mean overall (no-ret.) Score @ 50K (Gemini)<br><!-- End of picture text -->

**Figure 5:** _(a)_ Paim mean overall by system across three judges on the shared 6-question subset, so absolute levels are directly comparable; the bar heights track each other closely and rank Spearman is _𝜌_ ∈[0 _._ 90 _,_ 0 _._ 97]. _(b)_ PTr corpus+modality progression at a 50K retrieval budget: the 80-paper / 48-question size-matched subset (dense) → PTr dense (252 papers, 98 questions) → PTr hybrid (the same, + BM25). The full-corpus step expands both papers and questions over the subset. 

differences at 30K all have intervals that include 0, whereas Simple RAG’s margins over Hindsight, Cognee, and the KG-only Graphiti are all significant. Thus, our claim that bonuses from architecture vanish under budget control is about the top cluster, not about the weak systems, which really are beaten. 

Second, the BM25 lift on PTr is significant for Mem0 (+0 _._ 29) and Simple RAG (+0 _._ 50) but only a positive trend for Theoria (+0 _._ 20, interval marginally including 0). Third, the three hybrids are statistically indistinguishable at 50K (all pairwise intervals include 0 and sit within ±0 _._ 35), which is why we do not read the 0 _._ 03-point ordering among them as a real ranking. The bootstrap script is released in the artifact. 

### **6.5 Judge calibration: multi-judge LLM and human ranking** 

The scores in our benchmark come from an LLM judge, so the reliability of that judge is itself part of the contribution. We therefore compare four LLM judges and add blinded human pairwise comparisons. As a result, we find that both system-level ranks and per-question scores correlate well across judges. There is non-trivial cell-level disagreement on close calls, so single-judge rankings are reliable for large score gaps but unstable for near-ties, which is exactly what one would expect from a 10-point scale. 

**Paim multi-judge subset.** Gemini judged the full 66-question × 9-protocol Paim grid (594 cells); Sonnet 4.6 and GPT-5.4 re-judged a stratified 6-question subset (PQ5, PQ7, PQ13, PQ24, PQ50, PQ58) across all 9 protocols (53 cells per judge, owing to a missing Graphiti cell on GPT-5.4). Computed on this shared subset, system-rank Spearman correlations are high: Gemini–Sonnet _𝜌_ = 0 _._ 90, Gemini–GPT-5.4 _𝜌_ = 0 _._ 97, Sonnet–GPT-5.4 _𝜌_ = 0 _._ 93 (Fig. 5a). Per-cell agreement within 1 point is 90 _._ 6% for Sonnet vs. GPT-5.4, 69 _._ 8% for Gemini vs. GPT-5.4, and 57 _._ 4% for Gemini vs. Sonnet; Gemini is systematically more generous in absolute level, but the induced ranking is essentially the same. 

**PTr cross-judge experiment.** We used a 50-question subset of PTr (7 systems × 50 questions × 3 budgets, 1 _,_ 050 design cells) to test _DeepSeek V4 Pro_ as a cross-judge 

21 

**Table 8:** Per-system mean overall on the 50-question PTr expansion subset at 50K budget under Gemini 3.1 Pro vs. DeepSeek V4 Pro, plus the average Δ across all three budgets. Per-cell Pearson _𝑟_ = 0 _._ 93 over _𝑛_ = 946 valid paired cells; DeepSeek is uniformly ∼0 _._ 4–0 _._ 6 more critical except on the (near-floor) base model. 

<!-- Start of picture text -->
System Gemini @ 50K DeepSeek @ 50K Δ  at 50K Avg.  Δ  (all)<br>Theoria 9 . 14 8 . 61 −0 . 53 −0 . 58<br>Theoria + BM25 9 . 48 9 . 14 −0 . 34 −0 . 49<br>Mem0 (dense) 9 . 39 9 . 11 −0 . 28 −0 . 38<br>Mem0 + BM25 9 . 41 8 . 91 −0 . 49 −0 . 40<br>Simple RAG 9 . 32 8 . 87 −0 . 44 −0 . 44<br>Simple RAG + BM25 9 . 53 8 . 95 −0 . 58 −0 . 55<br>Base model 1 . 79 2 . 18 +0 . 39 +0 . 30<br>10 Pearson  n  = 946 r  = 0.934 80 Tie-tolerance sweep ( ττ =0=1.5: 63%  : 76%   τ =0.5 τ =2: 72%  : 72% n =111 τ =1):: 77% agreedisagree<br>8 human ties<br>60 7/11=64%<br>[35%,85%]<br>6<br>40 29/29=100%<br>4 [88%,100%]<br>9/10=90%<br>2 20 [35%,85%] 7/11=64% [60%,98%]<br>fit y = 0.97x-0.20<br>0 0<br>0 2 4 6 8 10 0-1 1-2 2-4 4+<br>Gemini per-cell score |Gemini gap| between compared systems<br> PTr cross-judge: DeepSeek V4 Pro vs. Gemini ( 𝑛 = 946) (b)  Human SxS vs. Gemini ( 𝑛 = 112)<br>Human votes () n<br>DeepSeek V4 Pro per-cell score<br><!-- End of picture text -->

<!-- Start of picture text -->
(a)  PTr cross-judge: DeepSeek V4 Pro vs. Gemini ( 𝑛 = 946)<br><!-- End of picture text -->

**Figure 6:** Judge calibration. _(a)_ Per-cell scores, DeepSeek V4 Pro ( _𝑦_ ) vs. Gemini 3.1 Pro ( _𝑥_ ) on the PTr 50-question subset (7 systems × 50 questions × 3 budgets); Pearson _𝑟_ = 0 _._ 93, _𝑛_ = 946, best fit _𝑦_ = 0 _._ 97 _𝑥_ − 0 _._ 20. _(b)_ Human SxS vs. Gemini, 112 blinded votes. Stacked bars count votes per |Gemini gap| bucket, split into “Gemini agrees with the human winner”, “Gemini disagrees”, and “human tie”; annotations are agreement rate among decisive humans with Wilson 95% CIs. The inset reports overall agreement at five tie-tolerance thresholds _𝜏_ ; agreement peaks at _𝜏_ = 1 (77%), confirming that a ∼1-point gap is the effective resolution of the judge. 

against _Gemini 3.1 Pro_ (total cost $11). After excluding cells where either judge failed to produce a valid judgment (mostly DeepSeek timeouts on the base-model 50K column and a handful of memory-system answers), the paired comparison contains _𝑛_ = 946 system/question/budget combinations. Per-cell Pearson score correlation is _𝑟_ = 0 _._ 93 (Fig. 6a); the best-fit slope is 0 _._ 97 and the intercept −0 _._ 20, so DeepSeek is slightly more critical, and the critical bias concentrates at L3 (the DeepSeek-minus-Gemini gap is −0 _._ 30 at L1, −0 _._ 34 at L2, and −0 _._ 74 at L3). The two judges disagree about which hybrid is in the first place—under DeepSeek it is Theoria+BM25 (9 _._ 14), under Gemini it is Simple RAG+BM25 (9 _._ 53)—but under both judges the three hybrids fall within ∼0 _._ 3 of each other and beat their dense counterparts. We therefore do not treat the top ordering within the hybrid cluster as meaningful, and our headline result that hybrids _>_ dense with a three-way tie at the top holds under both judges. Per-system numbers are shown in Table 8. 

**Blinded human side-by-side study.** Human assessors, blinded to system identity 

22 

and to Gemini’s scores, voted on 112 randomly sampled A/B answer pairs, choosing “A”, “B”, or “tie” (system identities and Gemini scores were revealed only _after_ each vote, so they could not influence it). Fig. 6b shows that agreement scales cleanly with the Gemini gap: among decisive human votes, the judge agrees with the human winner 11/22 (50%) when the gap is 0–2 points, 9/10 (90%) at 2–4 points, and 29/29 (100%) at 4+ points. Allowing a tie tolerance recovers most of the disagreement: declaring a Gemini “tie” whenever |gap| ≤ _𝜏_ lifts overall agreement from 63% at _𝜏_ = 0 to 77% at _𝜏_ = 1, and the rate stays ≥ 72% for _𝜏_ ∈[0 _._ 5 _,_ 2]. In short, a 1-point Gemini gap on a 10-point scale should not be read as a real ranking difference, while a ≥ 2-point gap nearly always agrees with the human verdict. The full per-system win/loss/tie counts (with Wilson 95% CIs) are released in the artifact. 

**Recommendation.** On scientific QA at this scale, no single judge should be treated as the ground truth, but with a sensible tie tolerance Gemini agrees with a human rater on 77% of blinded pairwise comparisons and correlates strongly with DeepSeek V4 Pro, Sonnet 4.6, and GPT-5.4. We therefore recommend that scientific-memory benchmarks: 

- (i) report per-cell agreement with a second frontier judge on a stratified subset, plus per-question Pearson/Spearman; 

- (ii) avoid claiming system-rank differences within 1–2 points on a 10-point scale; 

- (iii) validate cell-level reliability with at least a small blinded human SxS study. 

## **7 Qualitative analysis** 

Aggregate scores are important but cannot tell us _why_ systems differ. We first follow the two questions introduced in Section 4 through the systems’ answers and then discuss how the same system’s answer to the same question changes as retrieval budget grows. All excerpts and scores are from the released run artifacts (Gemini judge, audited rubrics); several more examples, one per tier per corpus, are given in Appendix A. 

### **7.1 The same question across systems** 

**PQ40** (Paim, L2; enumeration + cross-document). The gold answer is the four MemoryAgentBench competencies and that _selective forgetting_ is the most neglected (Section 4; sources [15], [27], [43]). The spread is driven entirely by whether a system’s retrieval surfaces the canonical four-item list. 

23 

|**System**|**Score **|**Answer (excerpt)**|
|---|---|---|
|Simple RAG|10_._0|“MemoryAgentBench evaluates: (1) Accurate Retrieval, (2) Test-Time<br>Learning, (3) Long-Range Understanding, (4) Selective Forgetting.<br>Selective Forgetting is the most often neglected by LoCoMo and<br>LongMemEval.”|
|Theoria|9_._0|“Four competencies: Accurate Retrieval (AR), Test-Time Learning<br>(TTL), Long-Range Understanding (LRU), Selective Forgetting (SF).<br>Prior benchmarks such as LoCoMo and LongMemEval most often<br>neglect Long-Range Understanding (LRU) and Selective Forgetting<br>(SF). . . ” [partially correct – adds LRU, which is not in the gold.]|
|Hindsight|6_._0|“Four core competencies: Accurate Retrieval (AR), Test-Time Learning<br>(TTL), Long-Range Understanding (LRU), Selective Forgetting (SF).<br>Prior benchmarks such as LoCoMo and LongMemEval primarily focus<br>on aspects like long-term interaction. . . ”|
|Graphiti (KG)|0_._5|“MemoryAgentBench evaluates memory agents focusing on their<br>memory capabilities but does not evaluate agentic actions or<br>environment feedback. . . The exact four core competencies are not<br>explicitly listed in the evidence, we can infer. . . ”|

Simple RAG pulls the source enumeration cell verbatim; Theoria and Hindsight retrieve the list but append a non-gold item (LRU) and lose a point or more; the KG-only Graphiti, whose edges/nodes never surfaced the list, can only hedge (0 _._ 5). In this case, it is mostly not about reasoning but simply about whether the exact list reached the synthesizer. 

**TX17** (PTr, L2; quantitative + cross-document). Here the gold answer spans five papers and hinges on rare surface forms (“Kimi Linear 6× at 1M”); sources [47], [28], [25], [14], [20]. This is where retrieval _modality_ becomes important. 

|**System**|**Score **|**Answer (excerpt)**|
|---|---|---|
|Theoria|10_._0|“FSA: improvements primarily at ≥64K, up to3_._5×kernel speedup;<br>SALS: useful from4K with6_._4×KV compression; Kimi Linear: 6×<br>decoding throughput at 1M context (most<br>aggressive). . . Ring-flash-linear-2.0: linear-attention pronounced<br>beyond 8K. . . ”|
|Theoria+BM25|10_._0|“FSA:∼8K–16K crossover; SALS: efficient from 4K, scales to<br>RULER-128K; Kimi Linear: 6×decoding at 1M (most aggressive);<br>Ring-flash-linear-2.0: pronounced beyond 8K; HSA-UltraLong:<br>_>_ 90% retrieval at 16M tokens.”|
|Simple RAG+BM25|10_._0|“Comprehensive comparison across FSA, SALS, Kimi Linear,<br>Ring-flash-linear-2.0, HSA-UltraLong. . . Kimi Linear gives the most<br>aggressive throughput claim at 1M+tokens with 6×decoding<br>throughput.”|
|Simple RAG|5_._0|“FSA becomes beneficial beyond∼8K–16K tokens. At shorter<br>sequences. . . ” [retrieval pulled relevant FSA paragraphs but missed<br>Kimi Linear’s 1M-context claim, giving an incomplete answer.]|

Dense Simple RAG retrieves the FSA discussion but never the rare “Kimi Linear 6×” phrase, and scores 5 _._ 0; adding BM25 surfaces that exact string and lifts the same system to 10 _._ 0. This is a representative example of the PTr modality story of Section 6.3. 

### **7.2 The same system across budgets** 

A larger token budget usually helps on average, but per question the effect is sharper and not always monotone. We show two representative cases. 

24 

#### **Budget unlocks a correct answer (Simple RAG, PQ9).** 

**PQ9** (Paim, L2; mechanistic + quantitative). 

**Q:** “Why does RAPTOR’s collapsed-tree retrieval outperform tree traversal, and by how much? What does the paper identify as the mechanism, and how does the benefit change with model strength?” 

**Gold:** collapsed-tree retrieval outperforms tree traversal by 2–4 _._ 5 points; flattening all levels lets every leaf and summary compete by cosine similarity, avoiding the routing errors that top-down traversal accumulates; weaker reader models benefit more from the tree structure. **Sources:** [35] 

At 10K the top- _𝑘_ surfaces a passage _describing_ tree traversal and the synthesizer confidently asserts the wrong winner; more budget surfaces the actual comparison, and the answer becomes correct and stays correct. 

###### **Budget Score Answer (excerpt) and judge verdict** 

10K 0 _._ 0 “. . . The paper reports **tree traversal** as the consistently better-performing retrieval strategy. . . ” _Judge:_ “completely fails by claiming tree traversal is the winner instead of collapsed-tree retrieval, . . . invents mechanisms to support this incorrect claim.” 30K 10 _._ 0 “. . . The **collapsed tree retrieval** strategy consistently outperforms the tree traversal method across experiments. . . supported by results on QASPER (Figure 3). . . ” _Judge:_ “perfectly identifies collapsed-tree retrieval as the winner and accurately explains the mechanism.” 50K 10 _._ 0 “. . . the **collapsed tree retrieval** strategy consistently outperforms the tree traversal method across experiments. . . ” _Judge:_ “perfectly captures the required facts. . . without triggering any penalties.” 

Under-budgeted retrieval here does not merely truncate the answer; it shows a plausiblebut-wrong passage and yields a confident 0 _._ 0. 

#### **Higher budget introduces a distractor (Theoria, PQ44).** 

**PQ44** (Paim, L2; mechanistic + cross-document). **Q:** “HaluMem decomposes memory hallucinations into three stage-specific error categories. Name each stage and explain why extract-and-update systems like Mem0 and Memory-R1 are structurally more vulnerable than verbatim-storage systems like MemMachine.” 

**Gold:** the three stages are _extraction_ , _updating_ , and _memory-QA_ ; extractand-update systems write hallucinated facts permanently (and later retrieve them as if true), whereas verbatim-storage systems such as MemMachine extract only at read time, so errors do not compound in the store. **Sources:** [3], [4], [48], [42] 

At 10–30K Theoria answers correctly; at 50K its community-routed retrieval pulls in a neighboring paper (EverMemOS), and the synthesizer conflates the two, substituting EverMemOS’s memory stages for HaluMem’s. 

25 

|**Budget **|**Score **|**Answer (excerpt) and judge verdict**|
|---|---|---|
|10K|9_._25|“. . . three distinct, stage-specific error categories. . . Extraction. . . Update. . . ”<br>_Judge:_ “accurately identifies the three stages and the structural<br>vulnerabilities, though the retrieved sources completely missed the<br>HaluMem paper.”|
|30K|9_._5|“. . . three distinct, stage-specific error categories: (1) Extraction Errors,<br>(2) Update Errors, (3) [Memory-QA]. . . ” _Judge:_ “accurately identifies the<br>three stages. . . slightly misses the explicit nuance that hallucinated facts<br>become permanently written.”|
|50K|4_._5|“. . . three distinct stages. . . (1)**Episodic Trace Formation**. . . ” _Judge:_<br>“failed to retrieve the HaluMem paper and incorrectly substituted<br>EverMemOS’s memory stages for HaluMem’s, missing the core argument.”|

This is the candidate-pool dilution of Section 6.3 in miniature: the extra ∼20K characters at 50K were not neutral filler but a semantically adjacent distractor that displaced the correct source. This example shows that “more retrieval” is not uniformly better, and that the budget–quality curve can be non-monotone for an individual question even when it rises on average (Appendix A gives a third, oscillating case). 

## **8 Discussion and limitations** 

### **8.1 Conclusions from the evaluation study** 

Our experiments show that there is no definitive architecture-only leaderboard for scientific agentic memory. On Paim, native results are dominated by raw-context volume (Graphiti’s 8 _._ 04 native overall comes with 2 _._ 55M chars per query; its KG-only ablation drops to 5 _._ 27 at 30K), and dense budget-targeted retrieval leaves Simple RAG, Theoria, and Mem0 within 0 _._ 3 of one another. On PTr, which has clearer named entities, architecture lineages, and quantitative technical claims, structured and extracted memories (Theoria, Mem0) edge ahead of Simple RAG by 0 _._ 2–0 _._ 3 under dense retrieval at the same budget. Adding BM25 to the three evaluated systems on PTr produces the largest measured improvement and makes their overall scores converge within 0 _._ 03 at 50K. Budget control is thus _necessary but not sufficient_ : modality, corpus structure, and representation density all matter, and benchmarks should report all of them. 

**What this says about Theoria.** Theoria does not win the overall hybrid leaderboard, but this is not a negative result. Under dense retrieval it is competitive with Simple RAG on Paim and stronger on PTr, especially at high budget; with BM25 it joins the same top cluster as Mem0 and Simple RAG. This suggests that theory/community structure can improve budgeted evidence selection in some corpora, but that retrieval modality is a larger lever for the single-shot QA protocol studied here. The parts of Theoria most unlike RAG— `/theories` as a cold-start literature map and `/observe` as an incremental theory-update loop—remain untested by one-shot QA and motivate future sequential research-agent benchmarks. 

**Compression versus evidence preservation.** The budgeted results refine the usual intuition that extraction loses information. Mem0’s atomic facts are competitive once retrieval is matched, so aggressive extraction is not inherently bad; what fails is discarding the answer-critical details (quantities, conditions, table values) that L2/L3 questions 

26 

require. The KG-only Graphiti row, which keeps structure but throws away raw episode text, is the clearest illustration: it is competitive on some L3 synthesis but collapses on L1 factual recall, because the exact numbers are in the episode bodies that it no longer returns. 

**How much can routing help?** The tier-shaped specialization in Tables 4–5 (Theoria+BM25 wins L1, Mem0+BM25 wins L3) suggests a question-conditioned ensemble. Because we already have every system’s answer and judge score on every question, we can measure the ceiling without any new inference, as a pure re-aggregation of existing scores. 

On PTr (98 questions) at 50K, an _oracle_ router that picks the best-scoring of the three hybrids per question reaches 9 _._ 68, a +0 _._ 40 gain over the best single hybrid; over all six dense and hybrid systems the oracle reaches 9 _._ 73 (+0 _._ 46). On Paim at 50K the dense top-cluster oracle is 8 _._ 39 vs. 7 _._ 61 for the best single system (+0 _._ 77). The headroom is therefore real and significant. 

The catch is that a tier-level router that knows only the difficulty tier does not capture it: a leave-one-question-out, tier-conditioned router scores 9 _._ 22 on PTr and 7 _._ 12 on Paim, which is no better than (even slightly below) simply always using the best single system. The oracle’s advantage comes from per-question variation that the tier label (and, in additional checks, the question type label) does not predict. So in principle, a router conditioned on the question could add another ∼0 _._ 4–0 _._ 8 points, but realizing that gain is an open problem that requires a per-question routing signal, most probably a separate LLM run. 

**Recommendations.** Based on our results we make the following recommendations for future scientific-memory benchmarks. 

1. Report mean retrieved characters per query alongside scores. 

2. Report retrieval modality (dense, lexical, hybrid). 

3. Always include Simple RAG _and_ Simple RAG+BM25 as null hypotheses; denseonly RAG alone is too weak a null. 

4. Run a budget-targeted track in addition to the native track, and report achieved characters rather than nominal budgets. 

5. Audit rubrics against full paper text before reporting rankings (we caught many errors in the original data). 

6. Cross-validate judges and report Spearman _𝜌_ on a shared question subset rather than treating any single LLM as ground truth; calibrate cell-level reliability with at least a small human SxS study. 

7. Document granularity contracts and any deviations from them. 

### **8.2 Limitations** 

We also note the following limitations of our study. 

27 

1. _Modest question count_ (66 / 98); within-cluster differences smaller than ∼0 _._ 3 should be treated as noise. 

2. _Sparse PTr coverage_ : the 98 questions reach only ∼48% of the 252-paper corpus, leaving 132 papers uncovered. 

3. _Approximate budget control_ : three systems do not honor a clean character cap (Hindsight ignores `n` ; Cognee’s chunks are coarse; Graphiti’s `top_k` is permodality), so reported volumes are close but not exactly equal across systems. 

4. _Synthesis model fixed_ (gpt-4.1-mini, _𝑇_ =0); a comparison across synthesis models is interesting future work. 

5. _Single run per (system, budget)_ due to cost; smaller deltas (±0 _._ 05) would benefit from multi-seed reruns. 

6. _Human SxS sample is relatively small_ ; although the agreement curve is convincing as far as it goes, broader human evaluation would strengthen it. 

7. _Public-paper contamination_ : because the corpora are public arXiv papers, the no-retrieval base model is not a pure zero-information baseline, and markdown conversion can introduce noise around tables and equations. 

These limitations are, to a large degree, precisely why memory-system evaluation needs the kind of explicit, budget-aware protocol we propose. 

### **8.3 Lessons for memory evaluation infrastructure** 

Several integration patterns silently produced misleading numbers during our experiments, and they motivate a pre-run “doctoring” phase that probes each system with a known query before any evaluation begins. We report them because they are the kind of failures that an uncontrolled leaderboard might absorb without warning. 

1. A Qdrant collection symlink on Paim pointed to an empty directory after a working-directory change; `mem.search()` then returned 0 characters on most queries with no exception raised. 

2. A “ `fastembed` not installed” warning at ingest time silently disabled BM25 hybrid retrieval for an entire phase; only re-installation revealed that Mem0 had been running dense-only the whole time. 

3. A Qdrant local-mode SDK crashed with an out-of-memory error at 38 _,_ 330 points (the SDK warns it is “not recommended above 20 _,_ 000”); the failure surfaced only when a later query died at load time. 

We recommend a six-line checklist before any memory-system run: 

(1) a known good query returns nonzero retrieved context; 

(2) the retrieved character count matches the expected budget within a tolerance; 

28 

- (3) lexical and dense modalities are actually enabled; 

- (4) the stored-unit count matches the ingest logs; 

- (5) the source-document count matches the corpus manifest; 

- (6) the `top_k` knob actually changes output size on a probe query. 

## **9 Conclusion** 

We argue that scientific memory should be evaluated as budgeted, modality-aware _context restoration_ rather than as an unconstrained architecture leaderboard, and we built the artifacts to do so. We release 

- (i) _two full-text scientific-memory benchmarks_ , Paim (81 papers, 66 audited questions) on AI agent memory and PTr (252 papers, 98 questions) on modern transformer literature; 

- (ii) _a context-restoration evaluation harness_ that explicitly varies retrieval budget and modality while holding the synthesis model fixed, applied to eight memory systems plus a no-retrieval baseline, with BM25 hybrid variants for three of them; 

- (iii) _Theoria_ , a three-layer evidence + community + theory memory system, also evaluated as a participant; and 

- (iv) _an LLM-as-judge protocol_ verified against human votes and cross-validated across frontier LLMs. 

All of these artifacts are public: the harness, adapters, raw outputs, judgments, and analysis scripts at `https://gitlab.com/quantellence/research/scientificrecall-bench` , and the Paim and PTr corpora with their audited rubrics at `https: //huggingface.co/datasets/quantellence/srb-data` . 

We found that native leaderboards conflate architecture with retrieved evidence volume: Graphiti’s lead on Paim comes with 2 _._ 55M characters per query, and once retrieval is constrained the lead over Simple RAG vanishes on Paim and is small (0 _._ 2–0 _._ 3 points) on PTr. Budget control is necessary but not sufficient: adding BM25 hybrid retrieval to the systems where it can be wired up cleanly is the single largest intervention we measured, and the three resulting hybrids on PTr tie within 0 _._ 03 points at 50K characters despite ingest costs that span four orders of magnitude. Multi-judge and human SxS calibration further show that a Gemini score gap below ∼1 point is below the noise floor of the protocol; with a _𝜏_ =1 tolerance, the LLM judge agrees with a blinded human rater on 77% of 112 pairs, and the agreement curve scales cleanly with the gap. 

We note several directions for future work. First, we considered only one-shot, single-question retrieval; the parts of _Theoria_ most unlike chunk RAG, namely the cold-start `GET /theories` endpoint and the iterative `POST /observe` loop, have not been evaluated at all. The tier specialization we observed (Theoria+BM25 wins L1, Mem0+BM25 wins L3) points to an ensemble opportunity: a per-question oracle over our systems would add 0 _._ 4–0 _._ 8 points (Section 8), but a tier-only router does not realize 

29 

it, so a per-question routing signal is the open problem. PTr questions reach only ∼48% of the corpus, so expanding question coverage, as well as adding scientific domains beyond AI memory and Transformers, would test how far the corpus structure / retrieval modality story generalizes. Finally, and most consequentially in our view, the field needs a _sequential_ research-agent benchmark rather than one-shot QA. We see scientific memory as a research-agent infrastructure problem rather than a static leaderboard, and we hope this protocol and its artifacts make that infrastructure progressively more measurable. 

## **References** 

- [1] Akari Asai, Jacqueline He, Rulin Shao, Weijia Shi, Amanpreet Singh, Joseph Chee Chang, Kyle Lo, Luca Soldaini, Sergey Feldman, Mike D’arcy, David Wadden, Matt Latzke, Minyang Tian, Pan Ji, Shengyan Liu, Hao Tong, Bohao Wu, Yanyu Xiong, Luke Zettlemoyer, Dan Weld, Graham Neubig, Doug Downey, Wentau Yih, Pang Wei Koh, and Hannaneh Hajishirzi. OpenScholar: Synthesizing scientific literature with retrieval-augmented language models. _arXiv_ , 2024. URL `https://arxiv.org/abs/2411.14199` . 

- [2] Tim Baumgärtner, Ted Briscoe, and Iryna Gurevych. PeerQA: A scientific question answering dataset from peer reviews. In _Proceedings of the 2025 Conference of the North American Chapter of the Association for Computational Linguistics (NAACL)_ , 2025. URL `https://arxiv.org/abs/2502.13668` . arXiv:2502.13668. 

- [3] Ding Chen, Simin Niu, Kehang Li, Peng Liu, Xiangping Zheng, Bo Tang, Xinchi Li, Feiyu Xiong, and Zhiyu Li. HaluMem: Evaluating hallucinations in memory systems of agents. _arXiv preprint arXiv:2511.03506_ , 2025. URL `https://arxiv.org/abs/2511.03506` . 

- [4] Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh, and Deshraj Yadav. Mem0: Building production-ready AI agents with scalable long-term memory. _arXiv preprint arXiv:2504.19413_ , 2025. URL `https://arxiv.org/abs/2504. 19413` . 

- [5] Gordon V. Cormack, Charles L. A. Clarke, and Stefan Buettcher. Reciprocal rank fusion outperforms Condorcet and individual rank learning methods. In _Proceedings of the 32nd International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR)_ , pages 758–759, 2009. doi: 10.1145/1571941.1572114. 

- [6] DeepSeek-AI. DeepSeek-V3.2: Pushing the frontier of open large language models. _arXiv preprint arXiv:2512.02556_ , 2025. URL `https://arxiv.org/abs/2512. 02556` . Introduces DeepSeek Sparse Attention (DSA). 

- [7] Darren Edge, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva Mody, Steven Truitt, Dasha Metropolitansky, Robert Osazuwa Ness, and Jonathan Larson. From local to global: A graph RAG approach to query-focused summarization. 

30 

_arXiv preprint arXiv:2404.16130_ , 2024. URL `https://arxiv.org/abs/2404. 16130` . 

- [8] Jizhan Fang, Xinle Deng, Haoming Xu, Ziyan Jiang, Yuqi Tang, Ziwen Xu, Shumin Deng, Yunzhi Yao, Mengru Wang, Shuofei Qiao, Huajun Chen, and Ningyu Zhang. LightMem: Lightweight and efficient memory-augmented generation. _arXiv preprint arXiv:2510.18866_ , 2025. URL `https://arxiv.org/abs/2510. 18866` . 

- [9] Zirui Guo, Lianghao Xia, Yanhua Yu, Tu Ao, and Chao Huang. LightRAG: Simple and fast retrieval-augmented generation. _arXiv preprint arXiv:2410.05779_ , 2024. URL `https://arxiv.org/abs/2410.05779` . 

- [10] Bernal Jiménez Gutiérrez, Yiheng Shu, Yu Gu, Michihiro Yasunaga, and Yu Su. HippoRAG: Neurobiologically inspired long-term memory for large language models. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2024. URL `https://arxiv.org/abs/2405.14831` . arXiv:2405.14831. 

- [11] Bernal Jiménez Gutiérrez, Yiheng Shu, Weijian Qi, Sizhe Zhou, and Yu Su. From RAG to memory: Non-parametric continual learning for large language models. In _Proceedings of the 42nd International Conference on Machine Learning (ICML)_ , 2025. URL `https://arxiv.org/abs/2502.14802` . arXiv:2502.14802. 

- [12] Zexue He, Yu Wang, Churan Zhi, Yuanzhe Hu, Tzu-Ping Chen, Lang Yin, Ze Chen, Tong Arthur Wu, Siru Ouyang, Zihan Wang, Jiaxin Pei, Julian McAuley, Yejin Choi, and Alex Pentland. MemoryArena: Benchmarking agent memory in interdependent multi-session agentic tasks. _arXiv preprint arXiv:2602.16313_ , 2026. URL `https://arxiv.org/abs/2602.16313` . 

- [13] Chuanrui Hu, Xingze Gao, Zuyi Zhou, Dannong Xu, Yi Bai, Xintong Li, Hui Zhang, Tong Li, Chong Zhang, Lidong Bing, and Yafeng Deng. EverMemOS: A self-organizing memory operating system for structured long-horizon reasoning. _arXiv preprint arXiv:2601.02163_ , 2026. URL `https://arxiv.org/abs/2601. 02163` . 

- [14] Xiang Hu, Zhanchao Zhou, Ruiqi Liang, Zehuan Li, Wei Wu, and Jianguo Li. Every token counts: Generalizing 16M ultra-long context in large language models. _arXiv preprint arXiv:2511.23319_ , 2025. URL `https://arxiv.org/abs/2511.23319` . HSA-UltraLong. 

- [15] Yuanzhe Hu, Yu Wang, and Julian McAuley. Evaluating memory in LLM agents via incremental multi-turn interactions. _arXiv preprint arXiv:2507.05257_ , 2025. URL `https://arxiv.org/abs/2507.05257` . Introduces the MemoryAgentBench benchmark. 

- [16] Yuyang Hu et al. Memory in the age of AI agents. _arXiv preprint arXiv:2512.13564_ , 2025. URL `https://arxiv.org/abs/2512.13564` . 

31 

- [17] Dongming Jiang, Yi Li, Guanpeng Li, and Bingzhe Li. MAGMA: A multi-graph based agentic memory architecture for AI agents. _arXiv preprint arXiv:2601.03236_ , 2026. URL `https://arxiv.org/abs/2601.03236` . 

- [18] Dongming Jiang, Yi Li, Songtao Wei, Jinxin Yang, Ayushi Kishore, Alysa Zhao, Dingyi Kang, Xu Hu, Feng Chen, Qiannan Li, and Bingzhe Li. Anatomy of agentic memory: Taxonomy and empirical analysis of evaluation and system limitations. _arXiv preprint arXiv:2602.19320_ , 2026. URL `https://arxiv.org/abs/2602. 19320` . 

- [19] Milla Jovovich and Ben Sigman. MemPalace: An open-source AI memory system. GitHub repository, `https://github.com/milla-jovovich/mempalace` , 2026. 

- [20] Kimi Team. Kimi Linear: An expressive, efficient attention architecture. _arXiv preprint arXiv:2510.26692_ , 2025. URL `https://arxiv.org/abs/2510. 26692` . 

- [21] Chris Latimer, Nicolò Boschi, Andrew Neeser, Chris Bartholomew, Gaurav Srivastava, Xuan Wang, and Naren Ramakrishnan. Hindsight is 20/20: Building agent memory that retains, recalls, and reflects. _arXiv preprint arXiv:2512.12818_ , 2025. URL `https://arxiv.org/abs/2512.12818` . 

- [22] Yoonjoo Lee, Kyungjae Lee, Sunghyun Park, Dasol Hwang, Jaehyeon Kim, HongIn Lee, and Moontae Lee. QASA: Advanced question answering on scientific articles. In _Proceedings of the 40th International Conference on Machine Learning (ICML)_ , 2023. URL `https://proceedings.mlr.press/v202/lee23n.html` . 

- [23] Letta AI. Letta: The stateful agents framework with memory, reasoning, and context management. GitHub repository, `https://github.com/letta-ai/ letta` , 2024. Formerly the MemGPT open-source project. 

- [24] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, and Douwe Kiela. Retrieval-augmented generation for knowledge-intensive NLP tasks. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2020. URL `https://arxiv.org/abs/2005.11401` . arXiv:2005.11401. 

- [25] Ling Team. Every attention matters: An efficient hybrid architecture for longcontext reasoning. _arXiv preprint arXiv:2510.19338_ , 2025. URL `https://arxiv. org/abs/2510.19338` . Ring-flash-linear-2.0. 

- [26] Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. Lost in the middle: How language models use long contexts. _Transactions of the Association for Computational Linguistics_ , 12:157– 173, 2024. URL `https://arxiv.org/abs/2307.03172` . arXiv:2307.03172. 

32 

- [27] Adyasha Maharana, Dong-Ho Lee, Sergey Tulyakov, Mohit Bansal, Francesco Barbieri, and Yuwei Fang. Evaluating very long-term conversational memory of LLM agents. In _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (ACL)_ , 2024. URL `https://arxiv.org/abs/2402. 17753` . arXiv:2402.17753. 

- [28] Junlin Mu, Hantao Huang, Jihang Zhang, Minghui Yu, Tao Wang, and Yidong Li. SALS: Sparse attention in latent space for KV cache compression. _arXiv preprint arXiv:2510.24273_ , 2025. URL `https://arxiv.org/abs/2510.24273` . 

- [29] Jiayan Nan, Wenquan Ma, Wenlong Wu, and Yize Chen. Nemori: Self-organizing agent memory inspired by cognitive science. _arXiv preprint arXiv:2508.03341_ , 2025. URL `https://arxiv.org/abs/2508.03341` . 

- [30] OpenDataLab. MinerU: A one-stop, high-quality open-source pdf extraction tool. GitHub repository, `https://github.com/opendatalab/MinerU` , 2024. 

- [31] Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, and Joseph E. Gonzalez. MemGPT: Towards LLMs as operating systems. _arXiv preprint arXiv:2310.08560_ , 2023. URL `https://arxiv.org/abs/2310. 08560` . 

- [32] Joon Sung Park, Joseph C. O’Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, and Michael S. Bernstein. Generative agents: Interactive simulacra of human behavior. In _Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology (UIST)_ , 2023. URL `https://arxiv.org/ abs/2304.03442` . arXiv:2304.03442. 

- [33] Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais, Jack Ryan, and Daniel Chalef. Zep: A temporal knowledge graph architecture for agent memory. _arXiv preprint arXiv:2501.13956_ , 2025. URL `https://arxiv.org/abs/2501.13956` . 

- [34] Stephen Robertson and Hugo Zaragoza. The probabilistic relevance framework: BM25 and beyond. _Foundations and Trends in Information Retrieval_ , 3(4):333–389, 2009. doi: 10.1561/1500000019. 

- [35] Parth Sarthi, Salman Abdullah, Aditi Tuli, Shubh Khanna, Anna Goldie, and Christopher D. Manning. RAPTOR: Recursive abstractive processing for treeorganized retrieval. In _International Conference on Learning Representations (ICLR)_ , 2024. URL `https://arxiv.org/abs/2401.18059` . arXiv:2401.18059. 

- [36] Yiting Shen, Kun Li, Wei Zhou, and Songlin Hu. Mem2ActBench: A benchmark for evaluating long-term memory utilization in task-oriented autonomous agents. _arXiv preprint arXiv:2601.19935_ , 2026. URL `https://arxiv.org/abs/2601. 19935` . 

- [37] Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflexion: Language agents with verbal reinforcement learning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2023. URL `https://arxiv.org/abs/2303.11366` . arXiv:2303.11366. 

33 

- [38] Theodore R. Sumers, Shunyu Yao, Karthik Narasimhan, and Thomas L. Griffiths. Cognitive architectures for language agents. _Transactions on Machine Learning Research_ , 2024. URL `https://arxiv.org/abs/2309.02427` . arXiv:2309.02427. 

- [39] Mohammad Tavakoli, Alireza Salemi, Carrie Ye, Mohamed Abdalla, Hamed Zamani, and J. Ross Mitchell. Beyond a million tokens: Benchmarking and enhancing long-term memory in LLMs. In _International Conference on Learning Representations (ICLR)_ , 2026. URL `https://arxiv.org/abs/2510.27246` . arXiv:2510.27246. 

- [40] Topoteretes. Cognee: Knowledge engine for AI agent memory in 6 lines of code. GitHub repository, `https://github.com/topoteretes/cognee` , 2024. 

- [41] V. A. Traag, L. Waltman, and N. J. van Eck. From Louvain to Leiden: Guaranteeing well-connected communities. _Scientific Reports_ , 9(1):5233, 2019. doi: 10.1038/ s41598-019-41695-z. 

- [42] Shu Wang, Edwin Yu, Oscar Love, Tom Zhang, Tom Wong, Steve Scargall, and Charles Fan. MemMachine: A ground-truth-preserving memory system for personalized AI agents. _arXiv preprint arXiv:2604.04853_ , 2026. URL `https: //arxiv.org/abs/2604.04853` . 

- [43] Di Wu, Hongwei Wang, Wenhao Yu, Yuwei Zhang, Kai-Wei Chang, and Dong Yu. LongMemEval: Benchmarking chat assistants on long-term interactive memory. In _International Conference on Learning Representations (ICLR)_ , 2025. URL `https://arxiv.org/abs/2410.10813` . arXiv:2410.10813. 

- [44] Zhishang Xiang, Chuanjie Wu, Qinggang Zhang, Shengyuan Chen, Zijin Hong, Xiao Huang, and Jinsong Su. When to use graphs in RAG: A comprehensive analysis for graph retrieval-augmented generation. _arXiv preprint arXiv:2506.05690_ , 2025. URL `https://arxiv.org/abs/2506.05690` . Introduces the GraphRAG-Bench benchmark. 

- [45] Ying Xie. Learning to forget: Sleep-inspired memory consolidation for resolving proactive interference in large language models, 2026. URL `https://arxiv. org/abs/2603.14517` . 

- [46] Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, and Yongfeng Zhang. A-MEM: Agentic memory for LLM agents. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2025. URL `https://arxiv.org/abs/2502. 12110` . arXiv:2502.12110. 

- [47] Ran Yan, Youhe Jiang, Zhuoming Chen, Haohui Mai, Beidi Chen, and Binhang Yuan. FSA: An alternative efficient implementation of native sparse attention kernel. _arXiv preprint arXiv:2508.18224_ , 2025. URL `https://arxiv.org/ abs/2508.18224` . 

- [48] Sikuan Yan, Xiufeng Yang, Zuchao Huang, Ercong Nie, Zifeng Ding, Zonggen Li, Xiaowen Ma, Jinhe Bi, Kristian Kersting, Jeff Z. Pan, Hinrich Schütze, Volker Tresp, 

34 

and Yunpu Ma. Memory-R1: Enhancing large language model agents to manage and utilize memories via reinforcement learning. _arXiv preprint arXiv:2508.19828_ , 2025. URL `https://arxiv.org/abs/2508.19828` . 

- [49] Li S. Yifei, Allen Chang, Chaitanya Malaviya, and Mark Yatskar. ResearchQA: Evaluating scholarly question answering at scale across 75 fields with surveymined questions and rubrics. _Transactions of the Association for Computational Linguistics_ , 2026. URL `https://arxiv.org/abs/2509.00496` . To appear; arXiv:2509.00496. 

- [50] Zeyu Zhang, Xiaohe Bo, Chen Ma, Rui Li, Xu Chen, Quanyu Dai, Jieming Zhu, Zhenhua Dong, and Ji-Rong Wen. A survey on the memory mechanism of large language model based agents. _ACM Transactions on Information Systems_ , 2025. URL `https://arxiv.org/abs/2404.13501` . arXiv:2404.13501 (2024). 

- [51] Luyao Zhuang, Shengyuan Chen, Yilin Xiao, Huachi Zhou, Yujing Zhang, Hao Chen, Qinggang Zhang, and Xiao Huang. LinearRAG: Linear graph retrievalaugmented generation on large-scale corpora. _arXiv preprint arXiv:2510.10114_ , 2025. URL `https://arxiv.org/abs/2510.10114` . 

## **A Qualitative answer examples** 

This appendix collects additional per-tier examples beyond the cases considered in Section 7 (PQ40, TX17, and the two budget-sensitivity cases). Each is chosen for cross-system disagreement (high standard deviation of judge scores across systems); we show the question, a one-line gold-answer summary, and three to four representative system answers, each with the Gemini judge’s overall score for that cell. Answers are abbreviated to the first ∼3 sentences for readability; the full answers are in the released artifact ( `synthesized.jsonl` ). The final subsection adds a third budget-sensitivity example to complement Section 7.2. 

### **PQ4 – saturation with integration failures** 

**PQ4** (Paim, L1; factual + quantitative). 

**Q:** “What Judge score does MAGMA report on LoCoMo, and by what margin does it beat prior systems according to the paper?” **Gold:** MAGMA achieves an LLM-as-a-Judge score of 0 _._ 700 on LoCoMo, beating Full Context (0 _._ 481), A-MEM (0 _._ 580), MemoryOS (0 _._ 553), and Nemori (0 _._ 590) by 18 _._ 6%–45 _._ 5% relative. **Sources:** [17], [27] 

35 

|**System**|**Score **|**Answer (excerpt)**|
|---|---|---|
|Theoria|10_._0|“MAGMA reports an overall LLM-as-a-Judge score of 0_._700 on<br>LoCoMo. This score significantly outperforms prior systems, beating<br>Full Context (0_._481) by45_._5%, A-MEM (0_._580) by18_._6%, MemoryOS<br>(0_._553) by∼26_._6%, and Nemori (0_._590) by∼18_._6%.”|
|Simple RAG|10_._0|“MAGMA reports an overall LLM-as-a-Judge score of 0_._7 on the<br>LoCoMo benchmark, with relative improvements of18_._6%–45_._5%over<br>Full Context (0_._481), A-MEM (0_._58), MemoryOS (0_._553) and Nemori<br>(0_._59).”|
|Mem0|10_._0|“MAGMA reports an overall LLM-as-a-Judge score of 0_._7 (70%) on<br>LoCoMo, substantially outperforming Full Context, A-MEM,<br>MemoryOS, and Nemori by relative margins of 18_._6% to 45_._5%.”|
|Graphiti (KG)|4_._0|“The provided evidence does not specify the exact LLM-as-a-Judge<br>score MAGMA achieves on LoCoMo, nor the precise margins.<br>MAGMA is described as a multi-graph agentic memory architecture. . . ”<br>[the relevant numbers were in the episode body that the KG-only mode<br>does not return.]|

_Reading._ The dense top systems all return the same correct numbers; the spread is driven entirely by systems whose retrieval scope does not surface the relevant rubric facts. 

### **PQ28 – multi-paper density argument** 

**PQ28** (Paim, L3; quantitative + conditional + cross-document). **Q:** “GraphRAG-Bench argues that graph density predicts performance more than architectural sophistication. State the specific average-degree and edges-per-10K-tokens numbers for HippoRAG 2 and MS-GraphRAG, and describe what this implies for systems whose graphs fall below the density threshold.” 

**Gold:** HippoRAG 2 avg degree 8 _._ 75 (novel) / 13 _._ 31 (medical), ∼2 _,_ 310 edges per 10K tokens (novel); MS-GraphRAG avg degree 1 _._ 48 / 1 _._ 82, ∼273 edges per 10K tokens. Sparser graphs underperform regardless of architecture. 

**Sources:** [44], [10], [11], [7] 

36 

|**System**|**Score **|**Answer (excerpt)**|
|---|---|---|
|Simple RAG|10_._0|“HippoRAG 2 average node degree: novel 8_._75, medical 13_._31.<br>MS-GraphRAG: novel 1_._48, medical 1_._82. HippoRAG 2 produces<br>∼2_,_310 edges on the novel dataset, vs. much sparser graphs from<br>MS-GraphRAG. . . Systems whose graphs fall below this density<br>threshold consistently underperform.”|
|Cognee|10_._0|“[GraphRAG-Bench] Average node degree: HippoRAG 28_._75/13_._31vs.<br>MS-GraphRAG 1_._48/1_._82; edges per 10K tokens∼2_,_310 for<br>HippoRAG 2 (novel) vs.∼273for MS-GraphRAG. . . Systems below the<br>density threshold (e.g. MS-GraphRAG) lose answer accuracy<br>proportionally.”|
|Theoria|7_._8|“HippoRAG 2: novel 8_._75, medical 13_._31. . . edges-per-10K-tokens for<br>HippoRAG 2 is not explicitly stated, we can infer from the data that<br>HippoRAG 2 generates significantly denser graphs with2_,_310edges on<br>the novel dataset.”|
|Mem0|6_._0|“HippoRAG 2: novel 8_._75, medical 13_._31. Exact average degrees for<br>MS-GraphRAG are not explicitly stated in the excerpts. . . ”|
|Graphiti (KG)|2_._0|“The provided evidence does not include explicit numerical<br>values. . . HippoRAG 2 is evaluated on GraphRAG-Bench and shows<br>improved QA performance compared to GraphRAG and other<br>baselines.”|

_Reading._ This synthesis question rewards systems whose retrieval scope returns multiple paragraphs from a single source: Cognee’s coarse ∼19K chunks are well matched here (and in fact tie Simple RAG); Theoria and Mem0 surface part of the evidence but miss the second paper’s numbers; Graphiti (KG) loses everything that lived in the episode body (which native Graphiti would place in its huge retrieved context). 

### **TX4 – BM25 closes a small gap** 

**TX4** (PTr, L1; factual + enumeration). 

**Q:** “What two components make up DeepSeek Sparse Attention (DSA) layered on top of MLA, and what context length does DeepSeek-V3.2 target?” 

**Gold:** DSA = lightning indexer + fine-grained (top- _𝑘_ ) token selection mechanism, instantiated under MLA; DeepSeek-V3.2 targets 128K context (not 1M). 

**Sources:** [6] 

37 

|**System**|**Score **|**Answer (excerpt)**|
|---|---|---|
|Simple RAG|10_._0|“DSA primarily consists of two components: (1) Lightning Indexer,<br>which computes an index score_𝐼𝑡,𝑠_between query and preceding<br>tokens; (2) Fine-Grained Token Selection<br>Mechanism. . . DeepSeek-V3.2 targets 128K context.”|
|Theoria+BM25|10_._0|“DSA components: (1) Lightning Indexer (low-precision FP8<br>attention indexer); (2) Fine-Grained Token Selection Mechanism<br>(top-_𝑘_KV per query token). Layered under MLA. DeepSeek-V3.2<br>targets a 128K context length.”|
|Theoria|7_._2|“DSA consists of two main components: Lightning Indexer (FP8<br>small-head attention indexer. . . ) and Fine-Grained Token Selection<br>Mechanism. . . ” [missing the explicit “128K context” fact in the cell<br>the judge scored.]|
|Mem0|7_._2|“DSA: Lightning Indexer+Fine-Grained Token Selection Mechanism.<br>DSA is instantiated on top of masked multi-head<br>attention. . . DeepSeek-V3.2 targets 128_,_000 tokens.” [the “masked<br>multi-head attention” phrasing is judged a partial mismatch with the<br>gold “MLA”.]|

_Reading._ BM25 closes a small but real gap by surfacing the exact fact strings (e.g., the “128K” value in a context paragraph) that dense retrieval ranked below the cut. 

### **TX37 – five trends** × **flagship models** 

**TX37** (PTr, L3; synthesis + cross-document). 

**Q:** “Synthesize the five converging trends in the corpus’s closing sections (sparse/linear hybrids, ultra-sparse trillion MoE, test-time compute, sub-4bit training and KV-quantization, native multimodal). For each trend, name two flagship models and cite specific benchmark numbers for at least one trend.” 

**Gold:** Sparse/linear: Kimi Linear (75% KV reduction, 6× decoding at 1M), DeepSeek-V3.2 (DSA on MLA). Ultra-sparse trillion MoE: Kimi K2 (1T/32B), Ring-1T (1T/∼50B). Test-time compute: TRM (7M params, 45% ARC-AGI-1), Ouro (2 _._ 6B looped matches 12B). Sub-4-bit: NVFP4 (12B×10T tokens), KVTC (up to 20× KV compression). Native multimodal: Emu3.5, Qwen3-VL. 

**Sources:** corpus-wide synthesis; cited flagship models include [20] and [6]. 

38 

|**System**|**Score **|**Answer (excerpt)**|
|---|---|---|
|Mem0+BM25|10_._0|“(a) Sparse/linear hybrids: Kimi Linear (75% KV reduction, 6×at<br>1M), DeepSeek-V3.2 (DSA over MLA); (b) ultra-sparse trillion MoE:<br>Kimi K2, Ring-1T; (c) test-time compute: TRM (7M, 45%<br>ARC-AGI-1), Ouro (2_._6B); (d) sub-4-bit + KV: NVFP4, KVTC;<br>(e) native multimodal: Emu3.5, Qwen3-VL.”|
|Simple RAG+BM25|5_._8|“(a) Sparse/linear hybrids: hybrid architectures combining sparse or<br>linear attention with full attention. . . ” [structurally correct but mostly<br>summary prose with few specific model names per trend.]|
|Theoria|5_._5|“(a) Sparse/Linear Attention Hybrids: hybrids that combine sparse,<br>linear, and dense attention. . . ” [similar issue: trend descriptions<br>strong, flagship-model coverage thin.]|
|Theoria+BM25|4_._0|“Sparse/linear hybrids: hybrid attention architectures combining<br>sparse, linear, and full quadratic attention. . . ” [BM25 surface match<br>retrieved a different cluster of paragraphs and the synthesis lost<br>specificity.]|

_Reading._ A synthesis question at this scope rewards a single retrieval pass that returns specific numerical claims from many papers; only Mem0+BM25 happened to produce that mix here. This supports the routing-ensemble argument of Section 6.3: different hybrids win different L3 questions, and a question-conditioned routing layer would raise the ceiling further. 

### **PQ52 – sparse-graph failure modes (budget-sensitive)** 

**PQ52** (Paim, L2; conditional + negative + cross-document). 

**Q:** “GraphRAG-Bench identifies that graph-based memory systems fail when graph density falls below a threshold. Which specific systems in the corpus are at risk under this criterion? Cite at least one paper (LinearRAG, LightRAG, or MS-GraphRAG) where density metrics or F1 catastrophes are reported.” 

**Gold:** a density threshold near average degree 2 _._ 0; at-risk systems include MS-GraphRAG (average degree 1 _._ 48) and LightRAG (F1 = 6 _._ 6 catastrophe), while LinearRAG reports 89 _._ 08% recall and HippoRAG 2 is safe (average degree 8 _._ 75). 

**Sources:** [44], [9], [51], [10], [11] 

Simple RAG’s score is _non-monotone_ in the budget—it dips sharply at 30K before recovering at 50K—complementing the monotone PQ9 and the over-budget collapse of PQ44 in Section 7.2. 

39 

|**Budget **|**Score **|**Answer (excerpt) and judge verdict**|
|---|---|---|
|10K|6_._0|“. . . graph-based memory systems fail when graph density falls below a<br>certain threshold. . . ” _Judge:_ “correctly identifies the systems at risk and the<br>general relationship, but fails to provide the specific density metrics or F1<br>scores due to poor retrieval.”|
|30K|2_._5|“. . . graph density—measured by metrics such as average degree—governs<br>performance. . . ” _Judge:_ “triggers a direct penalty by claiming LightRAG is<br>fundamentally sound and avoids pitfalls, completely misses the F1<br>catastrophe, and hallucinates LinearRAG’s failure.”|
|50K|8_._25|“. . . low graph density leads to fragmented or sparse evidence. . . ” _Judge:_<br>“correctly identifies MS-GraphRAG and LightRAG as at-risk systems and<br>cites LinearRAG regarding F1 catastrophes, fulfilling the core requirements,<br>though it misses the specific gold metrics.”|

_Reading._ The 30K retrieval happened to surface a passage that led the synthesizer to a penalized claim (LightRAG “fundamentally sound”); the larger 50K pool diluted that distractor and recovered most of the answer. As in PQ44, budget and answer quality are not monotonically related for an individual question, even though the per-tier averages rise smoothly with budget. 

40
