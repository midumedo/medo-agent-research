---
id: arxiv-2510.27246
title: "Beyond a Million Tokens: Benchmarking and Enhancing Long-Term Memory in LLMs"
registry: arxiv
native_id: 2510.27246
version: "2510.27246v2"
kind: [benchmark]
pdf: pdf/arxiv-2510.27246.pdf
pdf_sha256: "8ae85b00eb0f93f0717edb082f5471716f6c757670d7157dc5ba94df01fbb303"
parser: pymupdf4llm
converted_at: "2026-09-21T02:37:58.414418+00:00"
---

# Beyond a Million Tokens: Benchmarking and Enhancing Long-Term Memory in LLMs

- arXiv: [2510.27246](https://arxiv.org/abs/2510.27246v2)
- 作者: Tavakoli, Mohammad, Salemi, Alireza, Ye, Carrie, Abdalla, Mohamed, Zamani, Hamed, Mitchell, J Ross
- 发表日期: 2025/10/31
- 来源版本: 2510.27246v2
- 本地 PDF SHA256: `8ae85b00eb0f93f0717edb082f5471716f6c757670d7157dc5ba94df01fbb303`

> 本文件是 PDF 的机器转换文本，转换成功不等于已对 PDF 做视觉核验。
> 元数据与 PDF 的配对状态、转换时间及解析器版本见 papers/provenance.json；历史版本缺失时不能假定同版。
> 下方分隔线之后为转换正文，不含本项目的阅读建议。

---

Published as a conference paper at ICLR 2026 

# BEYOND A MILLION TOKENS: BENCHMARKING AND ENHANCING LONG-TERM MEMORY IN LLMS 

**Mohammad Tavakoli**<sup>1</sup> **, Alireza Salemi**<sup>2</sup> **, Carrie Ye**<sup>1</sup> **, Mohamed Abdalla**<sup>1</sup> **, Hamed Zamani**<sup>2</sup> **, J. Ross Mitchell**<sup>1</sup> 

1University of Alberta 2University of Massachusetts Amherst 

_{_ tavakol5, cye, mabdall2, jmitche2 _}_ @ualberta.ca 

_{_ asalemi, zamani _}_ @cs.umass.edu 

## ABSTRACT 

Evaluating the abilities of large language models (LLMs) for tasks that require long-term memory and thus long-context reasoning, for example in conversational settings, is hampered by the existing benchmarks, which often lack narrative coherence, cover narrow domains, and only test simple recall-oriented tasks. This paper introduces a comprehensive solution to these challenges. First, we present a novel framework for automatically generating long (up to 10M tokens), coherent, and topically diverse conversations, accompanied by probing questions targeting a wide range of memory abilities. From this, we construct BEAM, a new benchmark comprising 100 conversations and 2,000 validated questions. Second, to enhance model performance, we propose LIGHT–a framework inspired by human cognition that equips LLMs with three complementary memory systems: a long-term episodic memory, a short-term working memory, and a scratchpad for accumulating salient facts. Our experiments on BEAM reveal that even LLMs with 1M token context windows (with and without retrieval-augmentation) struggle as dialogues lengthen. In contrast, LIGHT consistently improves performance across various models, achieving an average improvement of 3.5%–12.69% over the strongest baselines, depending on the backbone LLM. An ablation study further confirms the contribution of each memory component. 

## 1 INTRODUCTION 

Large language models (LLMs) have been deployed across diverse applications, including opendomain conversational agents (Laban et al., 2025; Chen et al., 2025), retrieval-augmented generation (RAG) for open-domain question answering and fact checking (Lewis et al., 2020; Salemi et al., 2025; Salemi & Zamani, 2025; Kim et al., 2024b), long-document and code analysis (Li et al., 2025; Jelodar et al., 2025; Fang et al., 2024), and scientific or legal research (Rueda et al., 2025; Nguyen et al., 2025). Many of these tasks demand models capable of processing long inputs, motivating LLMs such as Gemini (DeepMind, 2025) with input windows of up to 1M tokens. Among these domains, conversational systems present an intuitive and critical need for extended context, as users often engage in protracted, multi-session dialogues that require consistent memory across lengthy interactions (Zhong et al., 2024; Xu et al., 2022; Du et al., 2024; Tan et al., 2025). This highlights the importance of evaluating how well LLMs can reason over and utilize long conversational histories. 

While there are many prior efforts on studying and evaluating long-term memory of LLMs (Kim et al., 2024a; Xu et al., 2021; Maharana et al., 2024; Zhong et al., 2024; Xu et al., 2022; Du et al., 2024; Tan et al., 2025), existing benchmarks have fundamental limitations. Most extend conversation length by artificially concatenating short sessions of different users, producing dialogues with abrupt topic shifts and weak narrative coherence. Such a construction artificially simplifies evaluation because distinct segments are easily separable, reducing the need for true long-range reasoning. Furthermore, these datasets typically target narrow domains—often limited to personal-life scenarios—leaving many real-world application areas underrepresented. Finally, they emphasize simple context recall, overlooking other critical memory abilities such as contradiction resolution, recognizing evolving information, and instruction following. 

1 

Published as a conference paper at ICLR 2026 

<!-- Start of picture text -->
1 Theme, Subtopic}{Domain, Title, 2 Conversation PlanSubplan 1.. 3 User_turnAssistantQuestionLLM Conversation Plan}{Memory Ability,LLM 4 {Probing Questions,Ideal Answer,Source ids} 5<br>Narrative Generator Subplan n Detection Question AssistantLLM ValidationHuman Invalid<br>Candidates Bullets<br>Subplan t<br>Conversation PlanGenerator Yes & δ< 3 Question?Has  No or δ>= 3 User LLM Provenance Dialogue Valid        Discard<br>Batch 1        ...       Batch K Finder<br>Next<br>No L == 10M Yes GeneratorQuestion GeneratorQuestion User LLM  Follow-upCheck Question LLM Pairs MessagesUser Assistant QuestionsProbingPool<br>Plan Plan10 I Questions    ...    I Questions AssistantLLM follow-up?Need {Probing Questions,Ideal Answer,Source ids} Nuggets<br>Yes & δ< 3 No or δ >= 3<br><!-- End of picture text -->

Figure 1: Overview of BEAM generation process. In the first stage, conversation plans are created for each chat seed. In the second stage, user utterances are generated from the conversation plans. In the third stage, assistant responses are produced. In the fourth stage, probing questions are generated based on the targeted memory abilities and corresponding conversation plans. In the final stage, invalid probing questions are filtered out, and nuggets are created for the validated set. 

To address these limitations, this paper presents a framework for automatically generating long coherent conversations between a user and an AI assistant—scaling up to 10M tokens on diverse domains—with a set of probing questions designed to evaluate diverse memory abilities of any LLM on the generated dialogues. An overview of the data generation framework is shown in Figure 1. This framework begins by defining a high-level conversation plan—a narrative for a particular domain and a simulated user with generated attributes—that outlines the overall flow of the dialogue. This plan is recursively decomposed into finer sub-plans that specify the storyline and its progression. From these sub-plans we generate chronologically ordered user turns, which are then expanded with corresponding assistant responses. To increase realism, the system injects follow-up questions and clarifications from both sides. Finally, we automatically create a set of probing questions that target ten distinct memory dimensions, with a focus on complicated and multi-hop reasoning, which are then validated by human annotators to ensure high quality. Using this pipeline, we construct the BEAM dataset: 100 diverse conversations ranging from 100 K to 10 M tokens each, accompanied by 2000 probing questions to evaluate the memory capabilities of LLMs. 

To improve LLM performance on probing questions, we introduce the LIGHT framework (Figure 2), which is applicable to both open-source and proprietary LLMs, inspired by research in human cognitive science and human’s memorization and recall process (Sridhar et al., 2023; Binder & Desai, 2011). This framework integrates three complementary memories: (1) episodic memory, a longterm index of the full conversation used for retrieval; (2) working memory, capturing the most recent user–assistant turns; and (3) a scratchpad, where after each turn the model reasons over the dialogue and records salient facts for future use. At inference, the LLM draws jointly on retrieved episodic content, the working memory, and the accumulated scratchpad to generate accurate answers. 

To evaluate LLM memory capabilities and the effectiveness of our method, we conduct experiments on the constructed dataset, BEAM, using both open-source and proprietary models. Results show that even LLMs with long context windows perform substantially worse as conversation length increases. Our method improves the LLM’s performance in answering the probing questions by 3.5%–12.69% on average over the best-performing baseline, depending on the backbone model and conversation length. An ablation study further reveals the contribution of each LIGHT component on the performance. To support future work, we release all code, data, and evaluation scripts.<sup>1</sup> 

## 2 BEAM: BENCHMARKING MEMORY CAPABILITIES OF LLMS 

### 2.1 PROBLEM FORMULATION 

> Let _D_ = _{Ti}_<sup>_|D|_</sup> _i_ =1<sup>denote a collection of</sup><sup>_|D|_conversations between users and a conversational agent</sup> _π_ . Each conversation is represented as _T_ = _{ti}_<sup>_|T |_</sup> _i_ =1<sup>, where</sup><sup>_ti∈T_corresponds to the</sup><sup>_i_thutterance</sup> 

> 1Available at: https://github.com/mohammadtavakoli78/BEAM 

2 

Published as a conference paper at ICLR 2026 

(turn) in the dialogue. The objective of this work is to systematically evaluate a predefined set of memory abilities _M_ exhibited by _π_ across conversations. For each memory ability _m ∈M_ , we construct a probing dataset of size _N_ , denoted as _Qm_ = _{_ ( _xi, yi_ ) _}_<sup>_N_</sup> _i_ =1<sup>,where</sup><sup>_xi_isaprobing</sup> question and _yi_ is the corresponding ground-truth answer set. Each probing question ( _x, y_ ) _∈Qm_ is appended as the ( _|T |_ +1)<sup>th</sup> turn in the dialogue, and the system generates a response ˆ _y_ = _π_ ( _x_ ; _T_ ) based on the conversation. The generated response is then evaluated using an ability-specific scoring function _µm_ , producing a performance score _s_ = _µm_ ( _x, y,_ ˆ _y_ ). The goal of this work is to quantify the performance of conversational systems on each memory ability in _M_ . 

### 2.2 BENCHMARK CREATION 

Our goal is to evaluate how well LLMs can answer questions that depend on long-term conversational memory. We measure performance across ten complementary abilities, seven drawn from prior benchmarks and three newly introduced here— _Instruction Following_ , _Event Ordering_ , and _Contradiction Resolution_ (see Table 2 in Appendix B.1). _Abstention_ evaluates whether a model withholds answers when evidence is missing. _Contradiction Resolution_ tests the capacity to detect and reconcile inconsistent statements across widely separated turns, maintaining global coherence. _Event Ordering_ assesses whether a model can recognize and reconstruct the sequence of evolving information in the dialogue. _Information Extraction_ measures recall of entities and factual details in long histories. _Instruction Following_ examines sustained adherence to user-specified constraints over long contexts. _Information Update_ evaluates revising stored facts as new ones appear. _Multi-hop Reasoning_ probes inference that integrates evidence across multiple, non-adjacent dialogue segments. _Preference Following_ captures personalized responses that adapt to evolving preferences. _Summarization_ assesses the ability to abstract and compress dialogue content, while _Temporal Reasoning_ tests reasoning about explicit and implicit time relations. Together, these abilities evaluate a system’s capacity to maintain, update, and manipulate information throughout extended conversations (see Appendix B.6 for examples of each ability). Given these abilities and the formulation in Section 2.1, the benchmark requires three components: 1) a user–assistant conversation, 2) probing questions targeting key memory abilities, and 3) an evaluation methodology to assess the model’s responses. The overall statistics of the constructed benchmark are summarized in Table 3 in Appendix B.1. The rest of this section details the process used to construct these components. 

**Overview:** The overview of our framework for creating conversations, probing questions, and the evaluation strategy is illustrated in Figure 1. The process begins by generating a simulated conversation between a user and an assistant. Structured conversation plans are first produced to guide the flow of the synthetic interactions. Each plan specifies sufficient information to generate both user and assistant turns, ensuring a coherent and natural conversational trajectory. While a typical exchange consists of a user question followed by an assistant response, realistic dialogues often involve follow-ups for clarification, elaboration, or related subtopics. To capture this, we incorporate two interaction-control modules. The question-detection module identifies whether an assistant response includes a query that requires a user reply; if triggered, the system generates the corresponding user response. The follow-up detection module determines when the user would naturally pose a clarifying or elaborative question; if triggered, it produces an additional user query for the assistant. Together, these mechanisms produce conversations that exhibit interactive, bidirectional behavior beyond simple turn-taking. After the conversation is generated, an automated procedure constructs a candidate set of probing questions, each tailored to the specific memory abilities in the benchmark. These candidates are then reviewed by a human evaluator, who selects valid questions and formulates the associated evaluation rubrics used for subsequent benchmarking. A case study and an example of the different generated components of a conversation is provided in Appendix E. 

### 2.2.1 CONVERSATION PLAN GENERATION 

A _conversation plan_ serves as the scaffold for each dialogue, providing a coherent storyline that unfolds chronologically. Each plan is generated using an LLM based on seed information, including: the conversation _domain_ ; a _title and theme_ ; _subtopics_ outlining specific topics; a set of _narratives_ defining evolving aspects (e.g., career progression, goals); a _user profile_ with attributes such as name, age, gender, location, profession, and personality traits sampled from the Myers–Briggs Type Indicator (MBTI); a _relationship graph_ linking the user to family, friends, and acquaintances, constrained for realism (e.g., age gaps); and an explicit _timeline_ specifying the span of the conversation. 

3 

Published as a conference paper at ICLR 2026 

To generate candidate titles and themes, human annotators specify target domains, then GPT-4.1 (OpenAI, 2025a) generates candidate titles, themes, and subtopics using Listing 22. Human reviewers refine outputs for topical diversity. For each conversation, we generate 15-20 narratives using the open-source LLaMA-3.3 70B model (AI, 2024) with the prompt in Listing 23 (Appendix H). Given the conversation seed, this model produces narrative elements capturing the evolving storyline, forming the backbone of a coherent conversation. 

Conversation plans consist of _N sub-plans_ , each representing a distinct stage in the conversation. Each sub-plan contains _M bullet points_ , defined by a _narrative_ , a descriptive statement of its role in the storyline, and a _time anchor_ . For conversations of 128K, 500K, and 1M tokens, a single plan is generated (line 4 in Algorithm 1, Appendix B.3.5) by conditioning the LLM on the conversation seed, profile, relationship graph, timeline, and specified counts of sub-plans, bullet points, and narratives (prompt in Listing 24, Appendix H). The number of sub-plans varies with domain and target length to meet the token requirement; e.g., coding domains generally require fewer turns than broader domains. For 10M-token conversations, one plan cannot capture the scope, so we create ten interlocking plans forming a coherent longer narrative. The process begins with a global seed defining the overall topic and theme, but a single seed is insufficient; instead, we derive ten distinct seeds—one per plan—so the narrative can evolve across stages. We propose two strategies: 

- **Sequential Expansion:** The global seed defines the initial point in the conversation’s chronology. Subsequent seeds represent successive events (e.g., a trip, job search, later milestones). Using the prompt in Listing 28 (Appendix H), each new seed is generated from the main seed, profile, and timeline. Plans are then produced sequentially (line 12 in Algorithm 1, Appendix B.3.5), with each plan conditioned on its predecessor to maintain continuity. Core relationships (e.g., parents) remain fixed, while new acquaintances are gradually introduced to reflect the evolving context. 

- **Hierarchical Decomposition:** The main seed is decomposed into ten sub-seeds, each representing a distinct topical and temporal segment. Together, these sub-seeds span the full storyline (e.g., an international trip: first three for preparation, next five for trip events, final two for reflections). Similar to sequential expansion, the user’s core relationships remain constant, while new acquaintances are introduced to reflect the evolving context. These ten sub-seeds are generated using the prompt in Listing 29 (Appendix H), conditioned on the main seed, profile, and timeline. 

Each conversation plan is assigned explicit topical and temporal boundaries—encoded in the seed—to avoid redundancy and ensure sub-themes appear in the right narrative stage. For coherence, the LLM conditions on summaries of prior plans and future seeds when producing a new plan, allowing anticipation of upcoming events (e.g., reserving tickets for travel dates). This procedure is implemented in line 20 of Algorithm 1 (Appendix B.3.5). Plans are generated using the prompt in Listing 31 (Appendix H), conditioned on the main seed, current sub-seed, number of subplans, narrative set, user profile, core and new relationships, preceding and subsequent sub-seeds, previous plan, a summary of earlier plans, current sub-seed index, and a binary flag for the first plan (triggering user introduction). Since initial plans may not sufficiently test three key memory abilities— _contradiction resolution_ , _information update_ , and _instruction following_ —we apply a twostage augmentation: first generate the base plan, then use GPT-4.1 (Listing 27) to augment each sub-plan with three targeted bullet points. Performing augmentation separately improves coverage and fidelity. The refinement follows the prompt in Listing 27 (Appendix H), which takes plan as input and outputs the revised version. This stage corresponds to the first module in Figure 1, which forms the first step of the overall data-generation pipeline. The detailed process for plan generation is reported in Appendix B.3.2. 

### 2.2.2 USER UTTERANCE GENERATION 

Once conversation plans are constructed, user utterances are synthesized from the sub-plans. Each sub-plan contains _M_ bullet points, which are divided sequentially into _K_ contiguous batches of equal size. Batching narrows the LLM’s focus, reducing repetition and low-quality outputs that can occur when conditioning on the entire sub-plan. For each batch, the LLM generates _I_ user questions (line 6 in Algorithm 2 in Appendix B.3.5) using the prompt in Listing 32 (Appendix H), conditioned on the conversation seed, the current batch, preceding batches, and context from earlier sub-plans. Each generated user question constitutes a user turn in the dialogue, ensuring coherence and continuity across extended conversations. Values of _K_ and _I_ are manually specified based on domain and target conversation length to meet the token budget, with configurations reported in 

4 

Published as a conference paper at ICLR 2026 

Table 6 (Appendix B). This provides fine-grained control over user interaction density, preventing under-generation or redundancy. To balance quality and cost, question generation uses the opensource LLaMA-3.3 70B model (AI, 2024), which produces high-quality outputs efficiently as the backbone LLM. This user-utterance construction aligns with the second stage in Figure 1. The details of this procedure for user utterance generation are provided in Appendix B.3.3. 

### 2.2.3 ASSISTANT UTTERANCE GENERATION 

Assistant-side responses are generated iteratively in a role-playing setup, where one LLM assumes the _assistant role_ and another the _user role_ . For each sub-plan, the assistant LLM is conditioned on the conversation seed (Section 2.2.1), prior sub-plans, a summary of the last _M_ turns, and a compressed summary of earlier ones (using the prompt in Listing 37 in Appendix B); for 10Mtoken conversations, additional summaries of prior plans are provided. The assistant first generates a response to the user’s most recent question (line 9 in Algorithm 3 in Appendix B.3.5), which is analyzed by a _question-detection module_ (line 11 in Algorithm 3 in Appendix B.3.5, using the prompt in Listing 35 Appendix B) to determine the presence of a counter-question. If detected, the response is passed to the user LLM, which generates a contextually consistent reply based on the current and prior sub-plans, relevant history, and conversation summaries (using the prompt in Listing 38 in Appendix B, line 14 in Algorithm 3 in Appendix B.3.5). This loop continues until no further assistant questions are detected or the threshold _δ_ 1 = 2 is reached, balancing realism and avoiding infinite cycles. In addition, a _follow-up detection module_ (line 21 in Algorithm 3 in Appendix B.3.5, using the prompt in Listing 36 in Appendix B) evaluates whether a clarifying or elaborative user followup is warranted, based on factors such as subject complexity, ambiguity, or incomplete responses. When required, the module generates a follow-up query conditioned on the seed, current and prior sub-plans, the most recent _M_ turns, and earlier summaries (using the prompt in Listing 39 in Appendix B), which is then passed back to the assistant LLM. The number of follow-up exchanges is limited by a threshold _δ_ 2 = 2, analogous to _δ_ 1. Together, these modules yield dialogues with bidirectional dynamics, contextual referencing, and realistic clarifications, approximating human–AI interactions. This assistant-side generation maps to the third module in Figure 1. The details of this procedure are provided in Appendix B.3.4. 

### 2.3 PROBING QUESTIONS GENERATION 

After constructing conversations, we generate probing questions to evaluate memory abilities. The pipeline combines automated synthesis with human validation: an LLM first produces candidate probes, which annotators review to select valid ones. Probes are derived from both the conversation plan and chat to ensure each targets a specific ability, is grounded in dialogue turns, and includes explicit provenance. The process begins by passing the plan to GPT-4.1-mini (OpenAI, 2025b), which selects candidate bullet points conditioned on the ability under evaluation. For example, knowledge-update probes require bullet pairs encoding an initial fact and its later revision, while summarization and event-ordering probes span multiple bullets. Each bullet is linked to its corresponding user and assistant turns through indices introduced during user-assistant turn generation, enabling retrieval of the precise dialogue segments in which the content was created. Candidate bullet selection is performed using prompts 1–9, one per memory ability. For abstention, candidate selection is unnecessary; probes are created directly from the plan using the prompt shown in Listing 14 (Appendix H). 

Given the selected bullet points and aligned dialogue snippets, GPT-4.1-mini generates the probing question, a candidate answer, and source identifiers citing the specific messages containing the answer. For 10M-token dialogues, candidate selection and synthesis are performed with a sliding window across the ten interlocking plans, processing a limited number at a time to preserve topical locality and scalability. Probe generation uses prompts 10–19 for each memory ability, mapping candidate bullet points and contexts into fully formed questions. Finally, a human evaluator reviews the generated candidates and selects those that are valid and consistent with the conversation. Samples of probing questions are provided in Appendix D, items 1–10. 

### 2.4 EVALUATION 

We evaluate LLMs on the probing questions using nugget evaluation, a common approach for longform text assessment (Pradeep et al., 2024; 2025). Each probing question is manually validated: 

5 

Published as a conference paper at ICLR 2026 

<!-- Start of picture text -->
User-assistant chat Key-Values Vector database<br>Key-Value   Embedding  Episodic<br>Extractor Model memory<br>Turn M-1 Scratchpad Buffer Buffer<br>Last pairs N } + Scratchpad Generator 1 N Summarizer Semantic memory<br>Add to<br>Last pair  buffer If<br>} Turn M total tokens > T<br>Working<br>memory<br>Retriver<br>Model<br>Scratchpad<br>Keep<br>relevant<br>Query + Filtering Noise parts + Working memory LLM Response<br>}<br><!-- End of picture text -->

Figure 2: Overview of the LIGHT framework. The system combines (i) **episodic retrieval** , (ii) a **scratchpad** and (iii) a **working memory buffer** . At inference, relevant items from the index and scratchpad, together with the full working memory, are integrated to generate the final response. 

invalid or unsupported questions are discarded, and minor inconsistencies are corrected. From the validated set, two questions per memory ability are chosen for each conversation, yielding 20 probing questions per conversation. Rubric nuggets are then derived for each question. A nugget is an atomic, self-contained criterion that a system response must satisfy. Annotators decompose the ideal reference answer into minimal semantic units, ensuring each nugget is both atomic and self-contained. System responses are scored against these nuggets by an LLM judge (Listing 20, Appendix H), which assigns 0 (unsatisfied), 0.5 (partially satisfied), or 1 (fully satisfied). Scores are averaged across nuggets to produce ability-level metrics. This nugget-based procedure applies to nine memory abilities; the exception is event ordering, where quality depends on both recall and correct sequence. We evaluate event ordering using the Kendall tau-b coefficient (Kendall, 1945), which considers both order and presence. To apply this metric, an LLM equivalence detector (using the prompt in Listing 21 in Appendix H) aligns events in system responses with nuggets, outputting yes if two snippets denote the same event/topic and no otherwise. Kendall tau-b is then computed over the aligned sequences, capturing both recall and ordering fidelity. Examples of nugget construction for each memory ability are provided in Appendix D. 

## 3 LIGHT: IMPROVING MEMORY CAPABILITIES OF LLMS 

Inspired by research in human cognitive science (Sridhar et al., 2023; Binder & Desai, 2011), humans employ two primary mechanisms for remembering and using knowledge: _episodic memory_ , the ability to recall specific personal experiences along with their context, and _working memory_ , the capacity to retain and manipulate information about recent events over short periods. In addition, maintaining notes on a _scratchpad_ provides an external record that supports long-term recall and later retrieval. Since answering questions in long-context conversations similarly requires integrating past experiences and accumulated knowledge, we introduce a method that emulates these strategies by combining episodic recall, short-term working memory, and an external scratch-pad mechanism. 

**Overview:** An overview of our method is shown in Figure 2. Given a question _x_ about a conversation _T_ = _{ti}_<sup>_|T |_</sup> _i_ =1<sup>,where</sup><sup>_|T |_isthetotalnumberofturns,theframeworkfirstqueriesare-</sup> trieval model _R_ to obtain _k_ relevant segments from _T_ , simulating recall from episodic memory: _E_ = _R_ ( _x, k, T_ ). Next, the most recent _z_ dialogue pairs of the conversation are selected to form the working memory, _W_ = _{t|T |−i}_<sup>_z_</sup> _i_ =0<sup>. In parallel, a pre-constructed scratchpad</sup><sup>_S|T |_contains up to</sup><sup>_m_</sup> 

6 

Published as a conference paper at ICLR 2026 

salient notes. A filtering function _f_ retains only the items pertinent to _x_ , yielding _Sx_ = _f_ ( _S|T |, x_ ). Finally, the LLM _π_ generates the answer by conditioning on the question and these three memory components, _y_ = _π_ ( _x, E, W, Sx_ ) using the prompt shown in Listing 44 in Appendix H. The remainder of this section details the construction and logic of each component in this pipeline. 

### 3.1 RETRIEVAL FROM THE CONVERSATION 

**Indexing the Conversation:** After each user–assistant turn (Figure 2, top), we apply Qwen2.532B-AWQ (Team, 2024) with the prompt in Listing 40 (Appendix H) to extract key–value pairs and a summary of the interaction. Keys represent entities and values capture attributes or descriptive details, providing fine-grained, event-level indices analogous to hippocampal memory traces (Teyler & DiScenna, 1986). These key–value pairs and summaries are embedded using the BAAI/bgesmall-en-v1.5 embedding model (of Artificial Intelligence, 2023) and stored in a vector database as keys, while the original dialogue segments are kept as values to ensure faithful grounding. 

**Retrieval from the Index:** To retrieve information from the conversation as episodic memory, we embed the question _x_ using the same embedding model and compare it against the stored keys in the index, and the original dialogue segments corresponding to the top _k_ nearest neighbors are returned. 

### 3.2 SCRATCHPAD FORMATION AND UTILIZATION 

**Construction:** In addition to episodic memory (Figure 2, middle pathway), we build a higher-level representation that preserves information beyond individual dialogue events. It integrates semantic knowledge (facts and concepts), autobiographical details (life events), prospective memory (future intentions), and contextual metadata (time, place, acquisition context) (Binder & Desai, 2011). For each dialogue pair, we use Qwen2.5-32B-AWQ with the prompt in Listing 41 (Appendix H) to reason over the current and preceding turn and extract salient content. The resulting “scratchpad” is iteratively merged with earlier versions; once content exceeds a 30K-token threshold—substantially shorter than the raw conversation—it is compressed into a 15K-token summary by GPT-4.1-nano using the prompt in Listing 42. This process maintains efficiency and long-term coherence, analogous to the gradual abstraction of semantic memory in humans. Unlike the episodic index, the scratchpad is not stored in a retrieval database but is provided directly as contextual input during inference. 

**Filtering Scratchpad (function** _f_ **):** During inference, the scratchpad is selectively filtered with respect to the question. It is first divided into semantically coherent chunks using _semantic chunking_ . 2 Each chunk is evaluated by Qwen2.5-32B-AWQ with the prompt in Listing 43 (Appendix H), which assigns a binary relevance label (yes/no). Only the chunks judged relevant are retained, producing a condensed representation of scratchpad that is passed to the response generator. 

## 4 EXPERIMENTS 

### 4.1 EXPERIMENTAL SETUP 

**Baselines:** We evaluate our approach against two types of baselines: long-context LLMs and a RAG method. For long-context LLMs, the entire conversation history is provided, followed by the probing question. We include two proprietary LLMs ( _GPT-4.1-nano_ , _Gemini-2.0-flash_ , both 1M context). and two open-source models ( _Qwen2.5-32B-AWQ_ , _Llama-4-Maverick-fp8_ ). For longcontext experiments, _Qwen2.5-32B-AWQ_ is evaluated with a 128K context length, while for the RAG baseline and our proposed method a 32K context length is used. At the 10M-token, since none of the four models support this length, they are evaluated on the largest recent dialogue segment fitting their window.<sup>3</sup> For RAG baselines, each user–assistant turn pair is treated as a document, embedded and stored in a vector database. At inference, the top five most similar documents are retrieved and passed to the LLM using the prompt in Listing 44 (Appendix H). 

> 2SemanticChunker in LangChain is used, which segments text into variable-length passages based on semantic rather than fixed token windows. 

> 3Among available models, only _Llama-4-Scout_ supports 10M-token context windows; however, due to its extreme computational requirements, we were unable to include it in our experiments. 

7 

Published as a conference paper at ICLR 2026 

Table 1: Comparison of different LLMs and methods across conversation lengths and memory abilities using the created benchmark. Methods with the best performance per evaluation are bolded. 

|Lth|Memory||Qwen 2.5||Lla|ma Mave|rick|G|emini 2 Fl|ash|G|PT-4.1-na|no|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|eng|Ability|Vanilla|RAG|Ours|Vanilla|RAG|Ours|Vanilla|RAG|Ours|Vanilla|RAG|Ours|
||Abstention|0.300|**0.650**|0.475|0.200|**0.800**|0.600|**0.800**|0.800|0.675|0.475|**0.800**|0.575|
||Contradiction Resolution|0.031|0.025|**0.037**|0.025|0.031|**0.031**|0.006|**0.050**|0.018|0.012|0.018|**0.031**|
||Event Ordering|0.192|0.201|**0.205**|**0.190**|0.162|0.166|0.181|**0.191**|0.166|**0.181**|0.169|0.177|
||Information Extraction|0.425|0.338|**0.479**|0.510|0.392|**0.518**|0.333|0.341|**0.464**|0.273|0.362|**0.538**|
||Instruction Following|**0.400**|0.375|0.362|0.412|0.375|**0.412**|0.275|0.287|**0.362**|**0.425**|0.350|0.400|
|100K|<br>Knowledge Update|**0.437**|0.275|0.362|0.300|0.350|**0.450**|0.125|**0.325**|0.300|0.275|0.375|**0.375**|
||Multi-Hop Reasoning|0.222|0.203|**0.281**|0.152|0.225|**0.353**|0.200|0.148|**0.225**|0.178|0.263|**0.365**|
||Preference Following|0.554|0.379|**0.566**|0.450|0.512|**0.625**|0.300|0.416|**0.462**|0.437|0.550|**0.625**|
||Summarization|0.128|0.074|**0.232**|0.065|0.111|**0.238**|0.018|0.093|**0.139**|0.028|0.083|**0.202**|
||Temporal Reasoning|0.112|**0.162**|0.112|0.100|**0.275**|0.187|**0.187**|0.150|0.125|0.112|0.125|**0.162**|
||Average|0.280|0.269|**0.311**|0.240|0.323|**0.358**|0.242|0.280|**0.294**|0.239|0.309|**0.345**|
||Abstention|0.314|**0.728**|0.571|0.185|**0.785**|0.628|0.714|**0.800**|0.685|0.557|**0.828**|0.600|
||Contradiction Resolution|**0.053**|0.017|0.017|0.035|0.028|**0.042**|0.010|0.021|**0.021**|0.017|0.025|**0.035**|
||Event Ordering|0.185|0.221|**0.244**|**0.209**|0.186|0.197|**0.215**|0.189|0.200|0.188|0.180|**0.204**|
||Information Extraction|0.166|0.400|**0.506**|**0.608**|0.402|0.535|0.469|0.343|**0.478**|0.142|0.382|**0.491**|
||Instruction Following|0.304|**0.350**|0.295|0.403|**0.447**|0.390|0.133|**0.334**|0.280|0.244|0.286|**0.342**|
|500K|Knowledge Update|0.111|0.226|**0.278**|0.276|**0.338**|0.264|0.171|0.180|**0.223**|0.107|**0.288**|0.240|
||Multi-Hop Reasoning|0.125|0.187|**0.214**|0.219|0.313|**0.350**|**0.198**|0.135|0.157|0.070|0.233|**0.266**|
||<br>Preference Following|0.567|0.477|**0.571**|0.560|0.525|**0.623**|0.379|0.427|**0.532**|0.450|0.577|**0.684**|
||<br>Summarization|0.137|0.187|**0.344**|0.266|0.197|**0.373**|0.136|0.165|**0.250**|0.109|0.184|**0.334**|
||Temporal Reasoning|0.035|0.114|**0.121**|0.064|0.078|**0.190**|**0.150**|0.078|0.092|0.057|**0.161**|0.154|
||Average|0.200|0.291|**0.316**|0.283|0.330|**0.359**|0.257|0.267|**0.292**|0.194|0.314|**0.335**|
||Abstention|0.342|**0.650**|0.500|0.221|**0.742**|0.435|0.642|**0.750**|0.735|0.492|**0.778**|0.678|
||Contradiction Resolution|**0.035**|0.035|0.021|**0.046**|0.028|0.042|0.010|**0.028**|0.007|**0.050**|0.028|0.021|
||Event Ordering|0.183|0.195|**0.200**|**0.214**|0.179|0.193|0.190|**0.198**|0.185|0.191|0.179|**0.211**|
||Information Extraction|0.138|**0.407**|0.366|**0.489**|0.431|0.474|0.374|**0.380**|0.341|0.153|0.399|**0.410**|
||Instruction Following|0.383|0.300|**0.419**|**0.440**|0.338|0.433|0.120|0.290|**0.380**|0.226|0.271|**0.394**|
|1M|<br>Knowledge Update|0.064|**0.378**|0.357|0.164|0.342|**0.414**|0.107|**0.278**|0.264|0.150|0.342|**0.392**|
||Multi-Hop Reasoning|0.102|0.163|**0.209**|0.174|0.245|**0.270**|0.083|0.134|**0.147**|0.091|**0.293**|0.278|
||<br>Preference Following|0.486|0.491|**0.551**|0.535|0.514|**0.610**|0.273|0.470|**0.472**|0.435|0.513|**0.576**|
||Summarization|0.122|0.157|**0.316**|0.207|0.145|**0.315**|0.091|0.125|**0.224**|0.060|0.152|**0.290**|
||Temporal Reasoning|0.073|0.078|**0.154**|0.097|0.107|**0.176**|**0.104**|0.057|0.085|0.061|0.064|**0.107**|
||Average|0.193|0.285|**0.309**|0.259|0.307|**0.336**|0.199|0.271|**0.284**|0.191|0.302|**0.336**|
||Abstention|0.250|**0.600**|0.550|0.050|**0.700**|0.450|**0.750**|0.650|0.650|0.450|**0.650**|0.400|
||Contradiction Resolution|**0.050**|0.000|0.012|**0.025**|0.000|0.000|0.000|**0.025**|0.000|0.000|0.012|**0.025**|
||Event Ordering|0.180|**0.221**|0.197|0.190|**0.220**|0.176|0.220|**0.266**|0.193|**0.215**|0.201|0.173|
||Information Extraction|0.100|0.350|**0.350**|0.075|**0.375**|0.300|0.075|**0.275**|0.150|0.050|0.300|**0.350**|
||Instruction Following|0.175|0.200|**0.350**|0.250|0.350|**0.500**|0.025|0.125|**0.250**|0.075|0.175|**0.250**|
|10M|<br>Knowledge Update|0.100|**0.300**|0.275|0.100|**0.375**|0.325|0.050|**0.325**|0.200|0.050|**0.325**|0.300|
||<br>Multi-Hop Reasoning|0.125|0.050|**0.125**|0.000|0.075|**0.125**|0.000|0.125|**0.125**|0.012|0.091|**0.135**|
||<br>Preference Following|0.241|0.291|**0.308**|0.291|0.316|**0.483**|0.075|**0.300**|0.150|0.175|0.366|**0.425**|
||<br>Summarization|0.114|0.106|**0.220**|0.065|0.053|**0.277**|0.000|0.045|**0.136**|0.020|0.063|**0.179**|
||Temporal Reasoning|0.000|0.000|0.000|0.000|0.025|**0.025**|0.025|0.025|**0.075**|**0.050**|0.000|0.025|
||Average|0.133|0.211|**0.238**|0.104|0.249|**0.266**|0.122|**0.216**|0.192|0.109|0.218|**0.226**|

**Inference Setup:** For inference, we use Nucleus (Holtzman et al., 2020) with temperature 0, except for conversation plan, user-turn, and assistant-turn generation, where temperature is 0.1 to encourage diversity. All open-source LLMs are served via VLLM for efficient inference. For Llama3.3-70B, we set the maximum output length to 6K tokens during user-turn generation, while for other LLMs we adopt their default maximum output length. For experiments involving both the RAG baseline and our proposed method, we employ FAISS as the vector database (Douze et al., 2024). For dense retrieval, we use the embedding model _BAAI/bge-small-en-v1.5_ (Xiao et al., 2023). 

### 4.2 EMPIRICAL FINDINGS 

**Main Results:** Across all four conversation lengths (100K–10M tokens), our method consistently outperforms both long-context LLMs and RAG baselines (Table 1). At shorter contexts (100K), we observe strong gains, such as +49.1% for Llama-4-Maverick and +44.3% for GPT-4.1-nano over long-context baselines, showing that structured memory helps even when full history can be processed. The benefits grow with context length: at 1M tokens, improvements reach +75.9% for GPT-4.1-nano and +60.1% for Qwen2.5-32B. At 10M tokens—where no baseline natively supports the full context—our method achieves dramatic improvements, including +155.7% for Llama-4Maverick and +107.3% for GPT-4.1-nano. The only exception is Gemini-2.0-flash at 10M, where our method surpasses the long-context baseline (+57.3%) but slightly trails RAG, likely due to model-specific retrieval behavior. Overall, these findings underscore the scalability and robustness of our framework across diverse architectures and extreme context lengths. 

When evaluated across the ten memory abilities, our method shows the largest relative gains in summarization (+160.6%), multi-hop reasoning (+27.2%), and preference following (+76.5%). Strong improvements are also observed in information extraction (+56.7%), instruction following (+39.5%), and temporal reasoning (+56.3%). These results highlight that our method is particularly 

8 

Published as a conference paper at ICLR 2026 

Figure 3: Ablation study illustrating the contribution of each component in LIGHT (retrieval, scratchpad, working memory, and noise filtering) across different conversation lengths. 

effective for tasks requiring long-range recall and integration of dispersed information. In contrast, all methods—including ours—perform strongest in abstention and weakest in contradiction resolution, indicating that contradiction detection remains a challenging open problem. 

**Ablation:** We conduct an ablation to assess the role of each component— _episodic memory_ , _scratchpad_ , _working memory_ , and _noise filtering_ —across conversation lengths (Figure 3). At 100K, removing retrieval does not change performance and it remains steady, since the scratchpad alone suffices, while removing scratchpad or noise filtering reduces performance (–1.1%, –2.2%). Working memory also degrades results here (–1.6%). At 500K, removing any component reduces performance except working memory, where removal enhances performance very slightly. At 1M, retrieval, scratchpad, and noise filtering remain beneficial, but removing working memory slightly improves performance, again reflecting its limited usefulness when few questions depend on the most recent turns. By 10M, all components are essential, with removals leading to large drops (–8.5% for retrieval, –3.7% for scratchpad, –5.7% for working memory, –8.3% for noise filtering). Overall, the ablations show that each module contributes increasingly as context length grows, and the full architecture consistently achieves the best performance. Detailed results across all memory abilities are provided in Table 8. 

**Effect of Retrieval Budget:** We examine the effect of retrieval budget ( _K_ ), testing 5, 10, 15, and 20 documents (Figure 4). Performance consistently improves when increasing _K_ from 5 to 15, with the best results at _K_ =15 (+7.39%, +10.75%, +6.79%, and +6.3% at 100K, 500K, 1M, and 10M). Increasing further to _K_ =20 slightly degrades performance, likely due to noisy context. Results at _K_ =10 are mixed—helpful at 100K, 500K and 1M but harmful at 10M—indicating additional documents sometimes add noisy information. Full results across memory abilities are shown in Table 9. We also conducted complementary experiments analyzing the effect of retriever choice, where we observed that at 100K, 500K, and 1M token 

Figure 4: Effect of varying retrieval budget ( _K_ ) on performance. The plot shows how the number of retrieved documents shapes the balance between recall and noise, highlighting different behaviors at short and long conversation lengths. 

lengths, using a sparse retriever improves performance, whereas at 10M tokens, the dense retriever achieves better results. The full results and discussion are provided in Appendix C.2. 

**Case Study** A case study demonstrating the usefulness of the scratchpad is provided in Appendix F. 

9 

Published as a conference paper at ICLR 2026 

Additional analyses on embedding choice, indexing setup, and a supplementary baseline are provided in Appendix C.3–C.5. 

**Human Evaluation:** We conducted a human evaluation to assess the quality of the generated conversations. Three dimensions were considered: _Coherence and Flow_ , _Realism_ , and _Complexity and Depth_ , each rated on a 5-point Likert scale (1 = lowest, 5 = highest). The average scores across all conversations were 4.53, 4.57, and 4.64, respectively, indicating consistently high quality. Details of the annotation protocol and inter-annotator agreement are provided in Appendix B.2. We further present a qualitative error analysis characterizing LIGHT ’s failure modes across memory abilities in Appendix G. 

## 5 RELATED WORK 

The detailed related work is provided in Appendix A; here we present a concise summary. 

Context windows of LLMs have expanded dramatically, from early limits of 512–2K tokens (GPT2/3; (Radford et al., 2019; Brown et al., 2020)) to 128K–1M (Claude-3, GPT-4-Turbo, Gemini 2.0; (DeepMind, 2025; Anthropic, 2025; OpenAI, 2025a)) and even 10M (Llama 4; (Meta-AI, 2025)). This growth is driven by advances in efficient attention (sparse, linear, memory-optimized kernels; (Beltagy et al., 2020; Wang et al., 2020; Dao et al., 2022)), improved positional encodings (relative, rotary with scaling, ALiBi; (Dai et al., 2019; Peng et al., 2023b)), long-context training strategies (continued-training, curriculum learning; (Xiong et al., 2023; Ding et al., 2024)), and inference optimizations such as paged attention, KV-cache compression, and distributed attention (Kwon et al., 2023; Zhang et al., 2023; Li et al., 2024; Liu et al., 2023). Such capabilities are especially valuable for applications involving conversational histories, the main focus of our work. 

Beyond expanding context windows, models incorporate additional mechanisms for persistent memory. These include recurrence and compression (Transformer-XL, Compressive Transformer; (Dai et al., 2019; Rae et al., 2019)), state-space architectures (RWKV, Mamba, Hyena; (Peng et al., 2023a; Gu & Dao, 2023; Poli et al., 2023)), external memory modules (Memformer, RETRO, RMT; (Wu et al., 2020; Borgeaud et al., 2022; Fan et al., 2024)), context summarization (AutoCompressor; (Chevalier et al., 2023)), and retrieval-augmented generation (REALM, RAG, HippoRAG; (Guu et al., 2020; Lewis et al., 2020; Jimenez Gutierrez et al., 2024)). These approaches complement larger windows by enabling scalable and persistent long-term reasoning. 

Existing benchmarks such as DialSim, MSC, LoCoMo, MemoryBank, DuLeMon, PerLTQA, LongMemEval, and MemBench (Kim et al., 2024a; Xu et al., 2021; Maharana et al., 2024; Zhong et al., 2024; Xu et al., 2022; Du et al., 2024; Tan et al., 2025) evaluate recall, temporal reasoning, and multi-session reasoning, but typically span narrow domains, exhibit shallow dependencies, and concatenate separate user sessions to simulate long context, reducing realism. Recent work such as MemoryCode (Rakotonirina et al., 2025) generates multi-session dialogues from template-driven instruction seeds to assess long-context reasoning, but focuses on a single domain. Our benchmark instead scales to 10M tokens across diverse topics and introduces new tasks such as contradiction resolution, event ordering, and instruction following, generating coherent, single-user conversations that preserve narrative continuity for a more faithful assessment of long-term conversational memory. 

## 6 CONCLUSION 

This paper addresses the shortcomings of existing benchmarks for evaluating long-term memory in conversational systems. We introduce a scalable framework to generate BEAM, a new benchmark with long, coherent dialogues (up to 10M tokens) and diverse memory probes. To improve LLMs performance, we develop LIGHT, a cognitive-inspired framework combining episodic, working, and scratchpad memories. Our experiments show that while standard LLMs’ performance degrades over long contexts, LIGHT provides substantial improvements, boosting memory performance by an average of 3.5%-12.69%. By offering a more robust evaluation and an effective memory enhancement technique, this work helps the development of more reliable long-context conversational systems. 

10 

Published as a conference paper at ICLR 2026 

## ACKNOWLEDGMENTS 

Ross Mitchell is the Alberta Health Services Chair in Artificial Intelligence in Health and is supported by CIFAR, the University Hospital Foundation, the Alberta Machine Intelligence Institute (Amii), and the Canada Foundation for Innovation. Mohamed Abdalla is supported by a CIFAR AI Chair. This research is supported by the Canadian Institutes of Health Research (FRF 196047). Carrie Ye is supported by the CRAF (CIORA)–Arthritis Society Canada Clinician Investigator Award (CI-24-0013). This research is supported in part by the Center for Intelligent Information Retrieval, in part by NSF grant #2143434, in part by the Office of Naval Research contract #N000142412612, and with support from Google.org. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect those of the sponsors. 

11 

Published as a conference paper at ICLR 2026 

## REFERENCES 

- Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 

- Meta AI. Llama 3.3 — model cards and prompt formats. https://www.llama.com/docs/ model-cards-and-prompt-formats/llama3_3/, 2024. 

- Anthropic. Claude 3 model card. Technical report, Anthropic PBC, 2024. URL https:// www-cdn.anthropic.com/de8ba9b01c9ab7cbabf5c33b80b7bbc618857627/ Model_Card_Claude_3.pdf. 

- Anthropic. Claude 4 model card (claude opus 4 & sonnet 4). Technical report, Anthropic PBC, May 2025. 

- Iz Beltagy, Matthew E Peters, and Arman Cohan. Longformer: The long-document transformer. _arXiv preprint arXiv:2004.05150_ , 2020. 

- Jeffrey R Binder and Rutvik H Desai. The neurobiology of semantic memory. _Trends in cognitive sciences_ , 15(11):527–536, 2011. 

- Sebastian Borgeaud, Arthur Mensch, Jordan Hoffmann, Trevor Cai, Eliza Rutherford, Katie Millican, George Bm Van Den Driessche, Jean-Baptiste Lespiau, Bogdan Damoc, Aidan Clark, et al. Improving language models by retrieving from trillions of tokens. In _International conference on machine learning_ , pp. 2206–2240. PMLR, 2022. 

- Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot learners. _Advances in neural information processing systems_ , 33:1877–1901, 2020. 

- Zhiliang Chen, Xinyuan Niu, Chuan-Sheng Foo, and Bryan Kian Hsiang Low. Broaden your SCOPE! efficient multi-turn conversation planning for LLMs with semantic space. In _The Thirteenth International Conference on Learning Representations_ , 2025. URL https:// openreview.net/forum?id=3cgMU3TyyE. 

- Alexis Chevalier, Alexander Wettig, Anirudh Ajith, and Danqi Chen. Adapting language models to compress contexts. _arXiv preprint arXiv:2305.14788_ , 2023. 

- Krzysztof Choromanski, Valerii Likhosherstov, David Dohan, Xingyou Song, Andreea Gane, Tamas Sarlos, Peter Hawkins, Jared Davis, Afroz Mohiuddin, Lukasz Kaiser, et al. Rethinking attention with performers. _arXiv preprint arXiv:2009.14794_ , 2020. 

- Zihang Dai, Zhilin Yang, Yiming Yang, Jaime Carbonell, Quoc V Le, and Ruslan Salakhutdinov. Transformer-xl: Attentive language models beyond a fixed-length context. _arXiv preprint arXiv:1901.02860_ , 2019. 

- Tri Dao, Dan Fu, Stefano Ermon, Atri Rudra, and Christopher R´e. Flashattention: Fast and memoryefficient exact attention with io-awareness. _Advances in neural information processing systems_ , 35:16344–16359, 2022. 

- Google DeepMind. Gemini 2.0 flash: A multimodal model with 1 million token context window. https://cloud.google.com/vertex-ai/generative-ai/docs/ models/gemini/2-0-flash, 2025. 

- Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. Bert: Pre-training of deep bidirectional transformers for language understanding. In _Proceedings of the 2019 conference of the North American chapter of the association for computational linguistics: human language technologies, volume 1 (long and short papers)_ , pp. 4171–4186, 2019. 

- Yiran Ding, Li Lyna Zhang, Chengruidong Zhang, Yuanyuan Xu, Ning Shang, Jiahang Xu, Fan Yang, and Mao Yang. Longrope: Extending llm context window beyond 2 million tokens. _arXiv preprint arXiv:2402.13753_ , 2024. 

12 

Published as a conference paper at ICLR 2026 

- Matthijs Douze, Alexandr Guzhva, Chengqi Deng, Jeff Johnson, Gergely Szilvasy, PierreEmmanuel Mazar´e, Maria Lomeli, Lucas Hosseini, and Herv´e J´egou. The faiss library. _arXiv preprint arXiv:2401.08281_ , 2024. 

- Yiming Du, Hongru Wang, Zhengyi Zhao, Bin Liang, Baojun Wang, Wanjun Zhong, Zezhong Wang, and Kam-Fai Wong. Perltqa: A personal long-term memory dataset for memory classification, retrieval, and fusion in question answering. In _Proceedings of the 10th SIGHAN Workshop on Chinese Language Processing (SIGHAN-10)_ , pp. 152–164, 2024. 

- Qihang Fan, Huaibo Huang, Mingrui Chen, Hongmin Liu, and Ran He. Rmt: Retentive networks meet vision transformers. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 5641–5651, 2024. 

- Chongzhou Fang, Ning Miao, Shaurya Srivastav, Jialin Liu, Ruoyu Zhang, Ruijie Fang, Asmita, Ryan Tsang, Najmeh Nazari, Han Wang, and Houman Homayoun. Large language models for code analysis: do llms really do their job? In _Proceedings of the 33rd USENIX Conference on Security Symposium_ , SEC ’24, USA, 2024. USENIX Association. ISBN 978-1-939133-44-1. 

- Thibault Formal, Carlos Lassance, Benjamin Piwowarski, and St´ephane Clinchant. Splade v2: Sparse lexical and expansion model for information retrieval. In _Proceedings of the 45th International ACM SIGIR Conference on Research and Development in Information Retrieval_ , pp. 127–137, 2022. 

- Albert Gu and Tri Dao. Mamba: Linear-time sequence modeling with selective state spaces. _arXiv preprint arXiv:2312.00752_ , 2023. 

- Kelvin Guu, Kenton Lee, Zora Tung, Panupong Pasupat, and Mingwei Chang. Retrieval augmented language model pre-training. In _International conference on machine learning_ , pp. 3929–3938. PMLR, 2020. 

- Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes, and Yejin Choi. The curious case of neural text degeneration. In _International Conference on Learning Representations_ , 2020. URL https: //openreview.net/forum?id=rygGQyrFvH. 

- Hamed Jelodar, Mohammad Meymani, and Roozbeh Razavi-Far. Large language models (llms) for source code analysis: applications, models and datasets, 2025. URL https://arxiv.org/ abs/2503.17502. 

- Bernal Jimenez Gutierrez, Yiheng Shu, Yu Gu, Michihiro Yasunaga, and Yu Su. Hipporag: Neurobiologically inspired long-term memory for large language models. _Advances in Neural Information Processing Systems_ , 37:59532–59569, 2024. 

- Adam Tauman Kalai, Ofir Nachum, Santosh S Vempala, and Edwin Zhang. Why language models hallucinate. _arXiv preprint arXiv:2509.04664_ , 2025. 

- Maurice G Kendall. The treatment of ties in ranking problems. _Biometrika_ , 33(3):239–251, 1945. 

- Jiho Kim, Woosog Chay, Hyeonji Hwang, Daeun Kyung, Hyunseung Chung, Eunbyeol Cho, Yohan Jo, and Edward Choi. Dialsim: A real-time simulator for evaluating long-term dialogue understanding of conversational agents. _arXiv e-prints_ , pp. arXiv–2406, 2024a. 

- To Eun Kim, Alireza Salemi, Andrew Drozdov, Fernando Diaz, and Hamed Zamani. Retrievalenhanced machine learning: Synthesis and opportunities, 2024b. URL https://arxiv.org/ abs/2407.12982. 

- Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph Gonzalez, Hao Zhang, and Ion Stoica. Efficient memory management for large language model serving with pagedattention. In _Proceedings of the 29th symposium on operating systems principles_ , pp. 611–626, 2023. 

- Philippe Laban, Hiroaki Hayashi, Yingbo Zhou, and Jennifer Neville. Llms get lost in multi-turn conversation, 2025. URL https://arxiv.org/abs/2505.06120. 

13 

Published as a conference paper at ICLR 2026 

- Kuang-Huei Lee, Xinyun Chen, Hiroki Furuta, John Canny, and Ian Fischer. A human-inspired reading agent with gist memory of very long contexts. _arXiv preprint arXiv:2402.09727_ , 2024. 

- Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich K¨uttler, Mike Lewis, Wen-tau Yih, Tim Rockt¨aschel, et al. Retrieval-augmented generation for knowledge-intensive nlp tasks. _Advances in neural information processing systems_ , 33: 9459–9474, 2020. 

- Minghan Li, Miyang Luo, Tianrui Lv, Yishuai Zhang, Siqi Zhao, Ercong Nie, and Guodong Zhou. A survey of long-document retrieval in the plm and llm era, 2025. URL https://arxiv. org/abs/2509.07759. 

- Yuhong Li, Yingbing Huang, Bowen Yang, Bharat Venkitesh, Acyr Locatelli, Hanchen Ye, Tianle Cai, Patrick Lewis, and Deming Chen. Snapkv: Llm knows what you are looking for before generation. _Advances in Neural Information Processing Systems_ , 37:22947–22970, 2024. 

- Hao Liu, Matei Zaharia, and Pieter Abbeel. Ring attention with blockwise transformers for nearinfinite context. _arXiv preprint arXiv:2310.01889_ , 2023. 

- Adyasha Maharana, Dong-Ho Lee, Sergey Tulyakov, Mohit Bansal, Francesco Barbieri, and Yuwei Fang. Evaluating very long-term conversational memory of llm agents. _arXiv preprint arXiv:2402.17753_ , 2024. 

- Meta-AI. The llama 4 herd: The beginning of a new era of natively multimodal ai innovation. Meta AI Blog, April 2025. URL https://ai.meta.com/blog/ llama-4-multimodal-intelligence/. 

- Ha Thanh Nguyen, Wachara Fungwacharakorn, May Myo Zin, Randy Goebel, Francesca Toni, Kostas Stathis, and Ken Satoh. Llms for legal reasoning: A unified framework and future perspectives. _Computer Law & Security Review_ , 58:106165, 2025. ISSN 2212-473X. doi: https://doi.org/10.1016/j.clsr.2025.106165. URL https://www.sciencedirect.com/ science/article/pii/S2212473X25000380. 

- Beijing Academy of Artificial Intelligence. Baai/bge-small-en-v1.5. Hugging Face model, 2023. URL https://huggingface.co/BAAI/bge-small-en-v1.5. MIT License; embedding model. 

- OpenAI. Introducing gpt-4.1 in the api. https://openai.com/index/gpt-4-1/, 2025a. 

- OpenAI. Gpt-4.1-mini model card. https://platform.openai.com/docs/models# gpt-4-1-mini, 2025b. Accessed: 2025-09-11. 

- Bo Peng, Eric Alcaide, Quentin Anthony, Alon Albalak, Samuel Arcadinho, Stella Biderman, Huanqi Cao, Xin Cheng, Michael Chung, Matteo Grella, et al. Rwkv: Reinventing rnns for the transformer era. _arXiv preprint arXiv:2305.13048_ , 2023a. 

- Bowen Peng, Jeffrey Quesnelle, Honglu Fan, and Enrico Shippole. Yarn: Efficient context window extension of large language models. _arXiv preprint arXiv:2309.00071_ , 2023b. 

- Michael Poli, Stefano Massaroli, Eric Nguyen, Daniel Y Fu, Tri Dao, Stephen Baccus, Yoshua Bengio, Stefano Ermon, and Christopher R´e. Hyena hierarchy: Towards larger convolutional language models. In _International Conference on Machine Learning_ , pp. 28043–28078. PMLR, 2023. 

- Ronak Pradeep, Nandan Thakur, Shivani Upadhyay, Daniel Campos, Nick Craswell, and Jimmy Lin. Initial nugget evaluation results for the trec 2024 rag track with the autonuggetizer framework. _arXiv preprint arXiv:2411.09607_ , 2024. 

- Ronak Pradeep, Nandan Thakur, Shivani Upadhyay, Daniel Campos, Nick Craswell, Ian Soboroff, Hoa Trang Dang, and Jimmy Lin. The great nugget recall: Automating fact extraction and rag evaluation with large language models. In _Proceedings of the 48th International ACM SIGIR Conference on Research and Development in Information Retrieval_ , pp. 180–190, 2025. 

14 

Published as a conference paper at ICLR 2026 

- Ofir Press, Noah A Smith, and Mike Lewis. Train short, test long: Attention with linear biases enables input length extrapolation. _arXiv preprint arXiv:2108.12409_ , 2021. 

- Alec Radford, Karthik Narasimhan, Tim Salimans, Ilya Sutskever, et al. Improving language understanding by generative pre-training. 2018. 

- Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, Ilya Sutskever, et al. Language models are unsupervised multitask learners. _OpenAI blog_ , 1(8):9, 2019. 

- Jack W Rae, Anna Potapenko, Siddhant M Jayakumar, and Timothy P Lillicrap. Compressive transformers for long-range sequence modelling. _arXiv preprint arXiv:1911.05507_ , 2019. 

- Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and Peter J Liu. Exploring the limits of transfer learning with a unified text-to-text transformer. _Journal of machine learning research_ , 21(140):1–67, 2020. 

- Nathana¨el Carraz Rakotonirina, Mohammed Hamdy, Jon Ander Campos, Lucas Weber, Alberto Testoni, Marzieh Fadaee, Sandro Pezzelle, and Marco Del Tredici. From tools to teammates: Evaluating llms in multi-session coding interactions. _arXiv preprint arXiv:2502.13791_ , 2025. 

- Alice Rueda, Mohammed S. Hassan, Argyrios Perivolaris, Bazen G. Teferra, Reza Samavi, Sirisha Rambhatla, Yuqi Wu, Yanbo Zhang, Bo Cao, Divya Sharma, Sridhar Krishnan, and Venkat Bhat. Understanding llm scientific reasoning through promptings and model’s explanation on the answers, 2025. URL https://arxiv.org/abs/2505.01482. 

- Alireza Salemi and Hamed Zamani. Learning to rank for multiple retrieval-augmented models through iterative utility maximization. In _Proceedings of the 2025 International ACM SIGIR Conference on Innovative Concepts and Theories in Information Retrieval (ICTIR)_ , ICTIR ’25, pp. 183–193, New York, NY, USA, 2025. Association for Computing Machinery. ISBN 9798400718618. doi: 10.1145/3731120.3744584. URL https://doi.org/10.1145/ 3731120.3744584. 

- Alireza Salemi, Chris Samarinas, and Hamed Zamani. Plan-and-refine: Diverse and comprehensive retrieval-augmented generation, 2025. URL https://arxiv.org/abs/2504.07794. 

- Sruthi Sridhar, Abdulrahman Khamaj, and Manish Kumar Asthana. Cognitive neuroscience perspective on memory: overview and summary. _Frontiers in human neuroscience_ , 17:1217093, 2023. 

- Jianlin Su, Murtadha Ahmed, Yu Lu, Shengfeng Pan, Wen Bo, and Yunfeng Liu. Roformer: Enhanced transformer with rotary position embedding. _Neurocomputing_ , 568:127063, 2024. 

- Haoran Tan, Zeyu Zhang, Chen Ma, Xu Chen, Quanyu Dai, and Zhenhua Dong. Membench: Towards more comprehensive evaluation on the memory of llm-based agents. _arXiv preprint arXiv:2506.21605_ , 2025. 

- Gemini Team, Petko Georgiev, Ving Ian Lei, Ryan Burnell, Libin Bai, Anmol Gulati, Garrett Tanzer, Damien Vincent, Zhufeng Pan, Shibo Wang, et al. Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context. _arXiv preprint arXiv:2403.05530_ , 2024. 

- Qwen Team. Qwen2.5: A party of foundation models, September 2024. URL https://qwenlm. github.io/blog/qwen2.5/. 

- Timothy J Teyler and Pascal DiScenna. The hippocampal memory indexing theory. _Behavioral neuroscience_ , 100(2):147, 1986. 

- Sinong Wang, Belinda Z Li, Madian Khabsa, Han Fang, and Hao Ma. Linformer: Self-attention with linear complexity. _arXiv preprint arXiv:2006.04768_ , 2020. 

- Di Wu, Hongwei Wang, Wenhao Yu, Yuwei Zhang, Kai-Wei Chang, and Dong Yu. Longmemeval: Benchmarking chat assistants on long-term interactive memory. _arXiv preprint arXiv:2410.10813_ , 2024. 

15 

Published as a conference paper at ICLR 2026 

- Qingyang Wu, Zhenzhong Lan, Kun Qian, Jing Gu, Alborz Geramifard, and Zhou Yu. Memformer: A memory-augmented transformer for sequence modeling. _arXiv preprint arXiv:2010.06891_ , 2020. 

- Shitao Xiao, Zheng Liu, Peitian Zhang, and Niklas Muennighoff. C-pack: Packaged resources to advance general chinese embedding, 2023. 

- Wenhan Xiong, Jingyu Liu, Igor Molybog, Hejia Zhang, Prajjwal Bhargava, Rui Hou, Louis Martin, Rashi Rungta, Karthik Abinav Sankararaman, Barlas Oguz, et al. Effective long-context scaling of foundation models. _arXiv preprint arXiv:2309.16039_ , 2023. 

- Jing Xu, Arthur Szlam, and Jason Weston. Beyond goldfish memory: Long-term open-domain conversation. _arXiv preprint arXiv:2107.07567_ , 2021. 

- Xinchao Xu, Zhibin Gou, Wenquan Wu, Zheng-Yu Niu, Hua Wu, Haifeng Wang, and Shihang Wang. Long time no see! open-domain conversation with long-term persona memory. _arXiv preprint arXiv:2203.05797_ , 2022. 

- Manzil Zaheer, Guru Guruganesh, Kumar Avinava Dubey, Joshua Ainslie, Chris Alberti, Santiago Ontanon, Philip Pham, Anirudh Ravula, Qifan Wang, Li Yang, et al. Big bird: Transformers for longer sequences. _Advances in neural information processing systems_ , 33:17283–17297, 2020. 

- Zhenyu Zhang, Ying Sheng, Tianyi Zhou, Tianlong Chen, Lianmin Zheng, Ruisi Cai, Zhao Song, Yuandong Tian, Christopher R´e, Clark Barrett, et al. H2o: Heavy-hitter oracle for efficient generative inference of large language models. _Advances in Neural Information Processing Systems_ , 36:34661–34710, 2023. 

- Wanjun Zhong, Lianghong Guo, Qiqi Gao, He Ye, and Yanlin Wang. Memorybank: Enhancing large language models with long-term memory. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 38, pp. 19724–19731, 2024. 

16 

Published as a conference paper at ICLR 2026 

## A DETAILED RELATED WORK 

**Long-Context Large Language Models.** The context window of LLMs has expanded from 512–2,048 tokens in early models (GPT-1/2/3, BERT, T5; (Radford et al., 2018; 2019; Brown et al., 2020; Devlin et al., 2019; Raffel et al., 2020)) to 128K–1M tokens in recent systems (Claude-3, GPT-4-Turbo, Gemini 1.5 Pro, Gemini 2.0 Flash, Claude-4, GPT-4.1; (Anthropic, 2024; Achiam et al., 2023; Team et al., 2024; DeepMind, 2025; Anthropic, 2025; OpenAI, 2025a)), with some reaching 10M tokens (Llama 4 Scout; (Meta-AI, 2025)). This growth has been enabled by innovations that address the quadratic cost of self-attention, including sparse mechanisms (Longformer, BigBird; (Beltagy et al., 2020; Zaheer et al., 2020)), linear approximations (Linformer, Performer; (Wang et al., 2020; Choromanski et al., 2020)) and memory-efficient kernels (FlashAttention; (Dao et al., 2022)). Advances in positional encoding, such as relative encodings (Transformer-XL; (Dai et al., 2019)), rotary embeddings (RoPE; (Su et al., 2024)) with scaling methods (YaRN, NTK; (Peng et al., 2023b)), and linear biases (ALiBi; (Press et al., 2021)), have extended usable context lengths. Training strategies like continued pre-training and curriculum learning (e.g., LLaMA-2Long (Xiong et al., 2023), LongRoPE (Ding et al., 2024)) further expand capabilities, while inference optimizations such as PagedAttention (Kwon et al., 2023), KV-cache compression (H2O, SnapKV; (Zhang et al., 2023; Li et al., 2024)) and distributed approaches (Ring Attention; (Liu et al., 2023)) enable practical deployment at scale. 

**Long-Term Memory Methods.** Researchers have developed approaches to enhance longterm memory beyond simply extending context windows. Architectural modifications include Transformer-XL (Dai et al., 2019), which introduced segment-level recurrence, and Compressive Transformer (Rae et al., 2019), which stored both recent states and compressed older information. State-space models such as RWKV (Peng et al., 2023a), Mamba (Gu & Dao, 2023), and Hyena (Poli et al., 2023) replace attention with recurrent dynamics, allowing linear scaling and theoretically unbounded memory. Memory-augmented transformers such as Memformer (Wu et al., 2020), RETRO (Borgeaud et al., 2022) and RMT (Fan et al., 2024) add external memory slots for explicit storage and recall. Context compression offers an orthogonal strategy by summarizing past information rather than storing it verbatim, as in AutoCompressor (Chevalier et al., 2023), which learns compact, information-preserving representations to reduce token usage. Retrieval-augmented generation (RAG) scales further by maintaining external knowledge stores: REALM (Guu et al., 2020) and RAG (Lewis et al., 2020) pioneered dense retrieval, RETRO (Borgeaud et al., 2022) integrated retrieval into transformers, and HippoRAG (Jimenez Gutierrez et al., 2024) incorporated structured knowledge graphs. 

Building on these foundations, we propose a novel retrieval-augmented method that shows substantial improvements over baselines in long-memory evaluation. 

**Long-Term Memory Benchmarks.** Several benchmarks have emerged to evaluate long-term memory capabilities in LLMs. DialSim (Kim et al., 2024a) derives evaluation data from multiparty television scripts, producing dialogues extending to 350K tokens with naturalistic patterns but limited topical diversity. MSC (Xu et al., 2021) introduces multisession human-assistant conversations testing memory across session boundaries, though with brief sessions and shallow dependencies. LoCoMo (Maharana et al., 2024) presents 50 conversations averaging 9K tokens in 35 sessions, while MemoryBank (Zhong et al., 2024) provides 300 sessions with 194 probing questions evaluating recall and temporal reasoning. DuLeMon (Xu et al., 2022) focuses on dialogue-level memory and forgetting curves, PerLTQA (Du et al., 2024) targets memory classification and retrieval, and LongMemEval (Wu et al., 2024) constructs multisession evaluations with 500 questions testing information extraction and temporal reasoning. More recently, MemBench (Tan et al., 2025) evaluates the memory of LLM-based agents by assessing their performance on information extraction, multihop reasoning, knowledge updating, preference following, and temporal reasoning. Recent work such as MemoryCode (Rakotonirina et al., 2025) generates multi-session dialogues from templatedriven instruction seeds to assess long-context reasoning, but focuses on a single domain. 

As summarized in Table 2, the existing benchmarks are largely based on concatenated short sessions with limited coherence, narrow personal and casual domains, and few memory abilities. They also lack realistic bidirectional interactivity. In contrast, our benchmark spans diverse domains, scales up to 10M tokens, and introduces three additional dimensions—contradiction resolution, event order- 

17 

Published as a conference paper at ICLR 2026 

Table 2: Comparison of our benchmark with existing long-term memory benchmarks. Memory abilities: IE = Information Extraction, MR = Multi-hop Reasoning, KU = Knowledge Update, TR = Temporal Reasoning, ABS = Abstention, CR = Contradiction Resolution, EO = Event Ordering, IF = Instruction Following, PF = Preference Following, SUM = Summarization. 

|**Benchmark**|**Domain**|**Chat Length**||||**Me**|**mory**|**Abilit**|**ies**||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||IE|MR|KU|TR|ABS|CR|EO|IF|PF|SUM|
|MSC (Xu et al., 2021)|Casual|_∼_1K|✗|✗|✗|✗|✗|✗|✗|✗|✗|✗|
|DuLeMon (Xu et al., 2022)|Casual|_∼_1K|✗|✗|✗|✗|✗|✗|✗|✗|✗|✗|
|MemoryBank (Zhong et al., 2024)|Personal life|_∼_5K|✓|✗|✗|✓|✗|✗|✗|✗|✗|✗|
|PerLTQA (Du et al., 2024)|Personal life|N/A|✓|✗|✗|✗|✓|✗|✗|✗|✗|✗|
|LoCoMo (Maharana et al., 2024)|Personal life|_∼_10K|✓|✓|✗|✓|✓|✗|✗|✗|✗|✓|
|DialSim (Kim et al., 2024a)|TV/Film scripts|_∼_350K|✓|✓|✗|✓|✓|✗|✗|✗|✗|✗|
|LongMemEval (Wu et al., 2024)|Personal life|115K, 1M|✓|✓|✓|✓|✓|✗|✗|✗|✓|✗|
|MemBench (Tan et al., 2025)|Personal life|_∼_100K|✓|✓|✓|✓|✗|✗|✗|✗|✓|✗|
|**BEAM (This work)**|**Multi-domain:**<br>Coding, Math,<br>Health, Finance,<br>Personal life, ...|**128K, 500K,**<br>**1M, 10M**|✓|✓|✓|✓|✓|✓|✓|✓|✓|✓|

ing, and instruction following—yielding a more comprehensive framework for evaluating long-term memory in conversational systems. 

## B BENCHMARK DESIGN 

### B.1 DATASET STATISTICS 

Table 3 summarizes the statistics of the generated dataset, including averages of user messages, assistant messages, assistant and user follow-up questions, and dialogue turns across different chat sizes. 

Table 3: Statistics of the dataset. Reported values are averages per chat in each chat size. # User Messages and # Assistant Messages denote the average number of utterances from the user and assistant, respectively. # Answer Assistant Questions is the number of times the assistant posed a question that the user answered. # Followup Questions is the number of follow-up questions asked by the user. # Turns refers to the total number of dialogue turns. 

|**Chat Size**|**# User Messages**|**# Assistant Messages**|**# Answer Assistant**<br>**Questions**|**# Followup**<br>**Questions**|**# turns**|
|---|---|---|---|---|---|
|128K|144|144|27|216|107|
|500K|544|544|79|51|416|
|1M|1067|1067|105|120|842|
|10M|10435|10435|1151|1528|7757|

B.2 BENCHMARK QUALITY EVALUATION 

To evaluate the quality of the generated conversations, we conducted a human assessment across all conversations. Two annotators rated each conversation on three dimensions using a 5-point Likert scale (1 = lowest, 5 = highest): _Coherence and Flow_ , _Dialogue Realism_ , and _Complexity and Depth_ . 

**Annotation Setup and Procedure.** We used an internal system for the annotators. The annotations were completed by two annotators with a computer science background. Human involvement are as follows: 

- **Probing Question Validation.** The annotators were first provided with guidelines and instructions on how to perform the task, and a training session was held. They went through 

18 

Published as a conference paper at ICLR 2026 

a calibration set together, completed multiple examples, and discussed their opinions on each example. 

- **Rubric Design.** The annotators were given guidelines on how to design rubrics along with examples and templates to make the task easier and more unified. A training and calibration session was then held, during which annotators reviewed many samples together, asked questions, and received clarification on ambiguous and edge cases. 

- **Conversation Quality Evaluation.** For this task, the annotators were again provided with guidelines on how to evaluate the generated conversations and assign scores. Because the conversations are very long and it is impractical to read them in full, annotators were instructed to read the initial 25 dialogue turns to understand what the conversation is about and to become familiar with the theme and flow of the chat. They were instructed to check the follow-up questions proposed by both the user and the assistant, the adherence of the conversation to the conversation plan and user utterances, and whether any hallucinations or unexpected behaviors occur. After that, they were asked to read several random turns between the initial 25 turns and the middle of the conversation to assess whether the conversation is progressing according to the conversation plan. They then had to read 25 dialogue turns in the middle of the conversation, followed by additional random turns between the middle and the end, and finally 25 dialogue turns near the end of the conversation. In this way, annotators read different parts of each conversation and ensured good coverage. 

For every conversation, annotators rated the three quality dimensions described below using a 5- point Likert scale. 

- **Coherence and Flow** : Conversation continuity (each turn follows naturally from the previous one), smooth transitions across topics and responses, and thread consistency without abrupt or jarring shifts. 

- **Dialogue Realism** : Naturalness of user queries (messages sound authentic), realistic progression of topics over time, human-like interactions (appropriate clarifications, follow-ups, etc.), and believability of scenarios. 

- **Complexity and Depth** : Handling of multi-layered, interconnected topics, progressive increase in difficulty, and demonstration of domain expertise when required. 

**Inter-Annotator Agreement.** Before performing the full evaluation, annotators independently assessed a set of 20 conversations. Agreement was measured using Cohen’s Kappa. The observed agreement levels were: 

- **Coherence and Flow:** _κ_ = 0 _._ 7044 

- **Dialogue Realism:** _κ_ = 0 _._ 7391 

- **Complexity and Depth:** _κ_ = 0 _._ 7849 

The aggregated evaluation results are reported in Table 4. 

Table 4: Conversation quality human evaluation results (1–5 scale). Higher is better. 

|**Chat Size**|**Coherence and Flow**|**Dialogue Realism**|**Complexity and Depth**|
|---|---|---|---|
|128K|4.4|4.55|4.35|
|500K|4.49|4.4|4.63|
|1M|4.66|4.54|4.6|
|10M|4.6|4.8|5|
|**Average**|4.53|4.57|4.64|

B.3 BENCHMARK CREATION DETAILS 

### B.3.1 DOMAIN COVERAGE OF THE DATASET 

To ensure broad coverage and realism, our dataset spans a diverse set of domains. The collection includes both technical and non-technical conversations, ranging from specialized domains such as coding, mathematics, financial investment and health to personal and social domains such as therapy, 

19 

Published as a conference paper at ICLR 2026 

lifestyle, and trip planning. In total, we designed 100 multi-turn chats distributed across 19 domains, each represented by a set of distinct titles that capture the thematic scope of the dialogues. The full list of domains and their associated chat titles is provided in Table 5. 

Table 5: Domains and associated chat titles in our dataset (100 total chats). 

|**Domain**|**Chat Titles**|
|---|---|
|Coding|Designing a Large-Scale Retrieval-Augmented Generation (RAG) Sys-<br>tem for Enterprise Search_•_Creating a Self-Driving Car Simulation En-<br>vironment_•_Developing a Multi-Agent AI Research Platform_•_Build-<br>ing a Multi-Language AI Chatbot with Contextual Memory_•_Develop-<br>ing a Personalized News Aggregator with AI Summarization_•_Creating<br>an Autonomous Stock Trading Bot _•_ Implementing a Custom Image<br>Captioning Model _•_ Building a Multiplayer Online Game with Real-<br>Time Physics _•_ Building a Real-Time Chat Application with Node.js<br>and Socket.io_•_Creating an AI-Powered Resume Analyzer with Python<br>and NLP _•_ Developing a Computer Vision App for Real-Time Ob-<br>ject Detection_•_Creating a Restaurant Recommendation System_•_Au-<br>tomating Social Media Posts with Python_•_Building a Personal Budget<br>Tracker Web App in Python and Flask _•_ Creating a Command-Line<br>To-Do List Manager in Go _•_ Developing a Weather Forecast App in<br>JavaScript with OpenWeather API _•_ Training a Spam Email Classi-<br>fier Using Python and Scikit-learn_•_Building a Portfolio Website with<br>HTML, CSS, and Bootstrap|
|Math|Partial Differential Equations (PDEs) in Depth _•_ Functional Analysis<br>and Infinite-Dimensional Spaces_•_Solving Ordinary Differential Equa-<br>tions (ODEs)_•_Deep Dive into Number Theory_•_Advanced Probability<br>and Combinatorics _•_ Exploring Non-Euclidean Geometry _•_ Studying<br>Multivariable Calculus_•_Diving into Analytic Geometry_•_Developing<br>Skills in Mathematical Induction_•_Exploring Conic Sections in Depth<br>_•_ Understanding Sequences and Series _•_ Mastering Basic Differential<br>Calculus _•_ Exploring the Geometry of Triangles _•_ Understanding the<br>Basics of Probability _•_ Mastering Algebraic Equations for Everyday<br>Problem Solving _•_ Learning the Foundations of Trigonometry _•_ Mas-<br>tering Fractions, Decimals, and Percentages|
|Writing Assistant &<br>Learning|Building a Portfolio-Ready Resume that Passes Any Applicant Track-<br>ing System_•_Mastering the Art of Persuasive Academic Essay Writing<br>_•_Crafting a Standout Cover Letter for Competitive Job Markets_•_De-<br>signing a Multi-Purpose Personal Statement for Global Opportunities_•_<br>Developing a Self-Editing System for Lifelong Writing Improvement|
|Therapy<br>&<br>Emo-<br>tional Support|Recovering from Workplace Burnout and Chronic Stress_•_Healing Af-<br>ter the Loss of a Loved One_•_Overcoming Childhood Trauma and Re-<br>building Self-Trust _•_ Coping with Post-Breakup Emotional Pain and<br>Relationship Trauma|
|Career<br>&<br>Profes-<br>sional Development|Advancing from Mid-Level to Senior Leadership Roles _•_ Building a<br>Powerful Professional Network from Scratch_•_Landing Your Next Job:<br>From Resume to Job Offer_•_Designing a 5-Year Career Growth Plan_•_<br>Positioning Yourself for a Promotion|
|Financial Investment|Building a Long-Term Stock Market Investment Strategy _•_ Getting<br>Started in Real Estate Investing _•_ Navigating the World of Cryptocur-<br>rency_•_Creating a Balanced Investment Portfolio|
|Health & Wellness|Creating a Personalized Nutrition and Meal Planning System_•_Design-<br>ing a Sustainable Fitness Routine_•_Improving Sleep Quality for Better<br>Health _•_ Understanding and Managing Chronic Illness _•_ Recognizing<br>Symptoms and Seeking Medical Help Early|

20 

Published as a conference paper at ICLR 2026 

|**Domain**<br>Relationship & Fam-<br>ily|**Chat Titles**<br>Strengthening Communication in Romantic Relationships _•_ Parenting<br>Through Different Life Stages_•_Navigating In-Law and Extended Fam-<br>ily Relationships_•_Rebuilding Relationships After Trust Has Been Bro-<br>ken|
|---|---|
|Education & Learn-<br>ing|Learning to Play a Musical Instrument from Scratch_•_Mastering a New<br>Language for Real-World Communication _•_ Becoming a Skilled Pho-<br>tographer_•_Exploring Performing Arts: Acting, Theater, and Dance|
|Home & Real Estate|Buying Your First Home with Confidence_•_Renting a Home or Apart-<br>ment Without Stress_•_Selling Your Home for Maximum Value_•_DIY<br>Home Improvement and Repairs_•_Making Your Home More Comfort-<br>able and Functional|
|Lifestyle|Designing a Daily Routine That Boosts Productivity and Well-Being_•_<br>Building Healthy and Sustainable Lifestyle Habits _•_ Balancing Social<br>Life and Personal Time|
|Cooking|Mastering Quick and Healthy Weeknight Dinners_•_Baking Like a Pro<br>at Home_•_Exploring Global Cuisines from Your Kitchen_•_Cooking for<br>Special Diets and Allergies_•_Meal Prepping for the Week Ahead|
|Business<br>&<br>En-<br>trepreneurship|Starting a Business from Scratch _•_ Growing and Scaling Your Small<br>Business_•_Building a Successful Startup|
|Trip Planning|Preparing for a Week-Long Hiking and Camping Adventure in Patago-<br>nia_•_Organizing a Cross-Country USA Road Trip_•_Planning a Cultural<br>Immersion Trip to Japan_•_Planning a Budget Backpacking Trip Across<br>Southeast Asia_•_Arranging a Luxury Honeymoon in the Maldives|
|Sport|Soccer – Playing, Watching, and Supporting the World’s Most Popular<br>Game _•_ Basketball – From Street Courts to the NBA _•_ Volleyball –<br>Indoor, Beach, and Competitive Play_•_Hockey – Ice, Field, and Global<br>Competitions_•_Tennis – From Local Courts to Grand Slams|
|Event Planning|Planning a Surprise 30th Birthday Party for a Close Friend_•_Coordinat-<br>ing a Destination Beach Wedding for 100 Guests_•_Organizing a Week-<br>end Community Food and Music Festival_•_Planning a Cozy Christmas<br>Eve Dinner for Extended Family|
|Asking Recommen-<br>dation|Finding the Perfect Smartphone for Photography and Gaming_•_Choos-<br>ing a Lightweight Laptop for Work, Travel, and Entertainment_•_Select-<br>ing a Must-Read Fiction Series for Winter Evenings_•_Finding the Best<br>Streaming Movies for a Family Weekend_•_Choosing Comfortable and<br>Stylish Sneakers for Daily Wear|
|Legal & Administra-<br>tive|Filing for a Marriage-Based Green Card in the United States_•_Creating<br>a Legally Valid Will and Estate Plan_•_Applying for a Patent to Protect<br>a New Invention|
|Philosophical & Eth-<br>ical Discussion|Deciding Whether to Use AI to Automate Hiring in My Company _•_<br>Considering Whether to Believe in and Live by the Idea of Free Will|

21 

Published as a conference paper at ICLR 2026 

### B.3.2 CONVERSATION PLAN GENERATION 

A _conversation plan_ serves as the central scaffold of each conversation, providing a coherent storyline that evolves chronologically. The process of constructing conversation plans is anchored by a _seed_ that specifies the _domain_ of the dialogue (e.g., sports, finance, programming, mathematics), a _title_ representing the high-level topic, and a _theme_ that provides a more detailed instantiation of the title. The seed also includes a set of _subtopics_ , which enumerate finer-grained subtopics and details to ensure topical diversity. However, a title, theme, and subtopics alone are insufficient to support detailed and information-rich conversations. To enrich the narrative, we introduce _narratives set_ that define the evolving aspects of a conversation (e.g., career progression, goals, relationships). Each narrative is paired with descriptive details that specify its scope and trajectory. 

In addition to the seed and narrative set, each conversation incorporates a _user profile_ , a _relationship graph_ , and an explicit _timeline_ . The user profile includes attributes such as name, age, gender, location, profession, and personality traits. To avoid redundancy, personality traits are grounded in the Myers–Briggs Type Indicator (MBTI). Specifically, we randomly select six MBTI types, provide their descriptions, and instruct an LLM to synthesize a composite trait profile, enabling the creation of 8,008 unique user profiles. Relationship graphs are then constructed, linking the main user to family members (parents, partner, children), friends, and acquaintances, subject to constraints (e.g., plausible age gaps) to preserve realism. The timeline specifies the temporal span of the conversation, defining the range between its beginning and end. 

In order to generate titles and themes of the chats, target domains are first specified by human. Given these domains, GPT-4.1 (OpenAI, 2025a) is prompted using the prompt shown in Listing 22 in Appendix H, to produce candidate titles, themes, and subtopics. These candidates are refined by human to ensure topical diversity by removing the similar chat titles and selecting diverse chat titles. Finally, for each conversation, we generate 15–20 narratives using open-source LLaMA-3.3 70B (AI, 2024) with the prompt shown in Listing 23 to save cost. In this prompt, given the conversation seed as input, the LLM produces narratives that capture evolving aspects of the storyline, providing the backbone for constructing coherent conversation plans. 

Conversation plans are structured as a sequence of _N sub-plans_ , where each sub-plan corresponds to a distinct stage of the conversation. Each sub-plan contains a fixed number of _M bullet-points_ , and each bullet-point is defined by a _narrative_ and a descriptive statement specifying how that narrative unfolds in the storyline. To maintain temporal coherence, each sub-plan also includes a _time anchor_ specifying a concrete date or period. 

For conversations of sizes 128K, 500K, and 1M tokens, a single conversation plan is generated, as shown in line 4 of Algorithm 1 in Appendix B.3.5. The plan is produced by conditioning the LLM on the conversation seed, user profile, relationship graph, timeline, the number of sub-plans, the number of bullet points within each sub-plan and narrative set, using the prompt shown in Listing 24 in Appendix H. The number of sub-plans is not fixed but varies with both the domain and the target conversation length, in order to adhere to the length budget. For instance, domains such as coding typically require fewer dialogue turns to reach the same token budget compared to more general domains. 

For 10M-token conversations, a single plan cannot adequately capture the scope and continuity required at this scale. To address this, we construct ten distinct yet interlocking conversation plans that together produce a coherent long-term narrative. While the process begins with a main seed that defines the global topic and theme of the conversation, a single seed is insufficient for producing ten plans. Instead, we generate ten distinct conversation seeds—one for each plan—so that the narrative can unfold across multiple stages. The procedure for deriving these seeds—and the plans that follow—differs depending on the strategy. We propose two strategies for constructing them: 

- **Sequential Expansion:** The conversation seed is used as the first seed in the sequence. The remaining seeds are generated to represent successive stages of the user’s life, extending the storyline chronologically. For instance, if the main seed concerns an international trip, the first plan covers the trip itself, the second covers the period after returning (e.g., job search), and subsequent seeds correspond to later milestones. We generate these seeds using the prompt shown in Listing 28, which conditions on the main seed, user profile, and timeline to produce a sequence of temporally aligned seeds. Each conversation plan is then generated sequentially, with every plan conditioned on its predecessor to maintain continuity, as specified in line 12 of Algorithm 1 

22 

Published as a conference paper at ICLR 2026 

in Appendix B.3.5. The plans are generated using the prompt shown in Listing 30, yielding a temporally ordered series of interconnected narrative arcs. To maintain realism, the user’s core relationships (e.g., parents, children, partner) remain fixed across plans, while new acquaintances are gradually introduced. 

- **Hierarchical Decomposition:** Instead of extending the seed chronologically, the main seed is decomposed into ten sub-seeds, each corresponding to a distinct topical or temporal slice of the overall storyline. Together, these seeds span the full narrative. For example, if the main seed concerns an international trip, the first three seeds may cover preparation steps (e.g., reservations, document gathering), the next five capture events during the trip, and the final two represent post-trip activities (e.g., reflections, recounting experiences). Like in Sequential Expansion, the user’s core relationships (e.g., parents, children, partner) remain fixed across plans, while new acquaintances are gradually introduced. We generate these ten sub-seeds using the prompt shown in Listing 29, which takes the main seed, user profile, and timeline, and outputs ten derived seeds. 

Each plan is assigned explicit topical and temporal boundaries to prevent redundancy or thematic overlap, ensuring that sub-themes unfold in the correct stage of the narrative. These boundaries are encoded in the conversation seed itself. For coherence, summaries of all prior plans are provided to the LLM when generating a new plan, allowing contextual references to past events. Moreover, when generating each plan, future seeds are also supplied, encoding their own topical and temporal boundaries. This design allows earlier plans to anticipate upcoming events with consistent references (e.g., booking tickets for the correct travel dates before the trip actually occurs). This strategy is implemented in line 20 of Algorithm 1 in Appendix B.3.5. Conversation plans are generated using the prompt shown in Listing 31, which takes as input the main seed, the current sub-seed, the number of sub-plans, the narrative set, the user profile, core and newly introduced relationships, the preceding and subsequent sub-seeds, the previous plan, the summary of all previous plans, the index of the current sub-seed, and a binary indicator specifying whether the plan is the first in the sequence (in which case the introduction of the user is included). The output is a fully specified conversation plan. 

After the conversation plan is constructed, it is expanded into user-turn questions and subsequently assistant responses, yielding complete dialogues that can be used to evaluate memory abilities. However, in its initial form, the plan may not include sufficient information to evaluate three critical memory abilities: _contradiction resolution_ , _knowledge update_ , and _instruction following_ . To address this, after the initial plan generation, we pass the plan to GPT-4.1 to generate high-quality plans and augment each sub-plan with additional bullet points specifically designed to enable evaluation of these abilities. Importantly, this augmentation is performed in a second stage rather than during the initial plan generation, since incorporating such information directly in a single-pass generation leads to lower quality and less reliable coverage of these abilities. The augmentation is implemented using the prompt shown in Listing 27, which takes an existing conversation plan as input and outputs a revised version where each sub-plan includes three additional bullet points targeting these abilities. 

### B.3.3 USER UTTERANCE GENERATION 

Once conversation plans are constructed, user turns are synthesized directly from them. Each subplan within a conversation plan consists of _M_ bullet-points, which are partitioned into _K_ contiguous batches of equal size. Partitioning is performed sequentially, such that each batch corresponds to a consecutive segment of the sub-plan. Partitioning is necessary because conditioning the LLM on an entire sub-plan at once tends to yield repetitive or low-quality questions; batching mitigates this by narrowing the focus of generation. For each batch, the LLM produces _I_ user questions (line 6 of Algorithm 2 in Appendix B.3.5) using the prompt presented in Listing 32. The model is conditioned on the conversation seed, the current batch specification, preceding batches within the same sub-plan, and contextual information from earlier sub-plans. This setup ensures that generated questions remain grounded in prior context, yielding conversations that are coherent and continuous over extended spans. 

The values of _K_ and _I_ vary depending on the domain and the target conversation length, in order to adhere to the overall length budget. We specify the values for _K_ and _I_ manually. The specific configurations of _K_ and _I_ across domains and conversation sizes are reported in Table 6. This provides fine-grained control over the density of user interactions and helps prevent both under- 

23 

Published as a conference paper at ICLR 2026 

generation and excessive redundancy. Additonally, to better capture domain-specific conversational patterns, we incorporate domain-specific features during question generation: 

- **Programming:** To reflect realistic developer–assistant interactions, we incorporate questions that involve sharing code snippets. These include (i) buggy code requiring debugging assistance, (ii) correct code seeking optimization, and (iii) natural language descriptions of desired functionality for which code is requested. We use the prompt shown in Listing 33 to generate questions specific to the programming domain. 

- **Mathematics.** To capture authentic problem-solving dynamics, we incorporate questions that involve sharing mathematical work, requesting corrections, asking for the next logical step in a solution, or introducing problems to be solved. We use the prompt shown in Listing 34 to generate questions specific to the mathematics domain. 

To reduce computational cost while maintaining generation quality, question generation is performed using the open-source LLaMA-3.3 70B model (AI, 2024), which produces high-quality questions. 

### B.3.4 ASSISTANT UTTERANCE GENERATION 

After generating user-side questions, assistant-side responses are generated in an iterative, roleplaying framework where one LLM assumes the _assistant role_ and another assumes the _user role_ . For each sub-plan, the assistant LLM is conditioned on the seed as explained in Section 2.2.1, prior sub-plans of the conversation plan, a summary of the most recent _M_ dialogue turns, and a compressed summary of older turns (generated using the prompt shown in Listing 37). For 10Mtoken conversations, additional summaries of prior plans are also provided. 

The response generation process unfolds as an iterative interaction between the assistant and user roles. First, the assistant LLM produces an answer to the user’s most recent question (line 9). This output is then analyzed by a _question-detection module_ , which determines whether the assistant’s response contains a counter-question directed at the user (line 11), using the prompt shown in Listing 35 that takes the assistant response as input and outputs yes if a question is present and no otherwise. If such a counter-question is detected, the response—together with the current and previous sub-plans, relevant past context, and conversation summaries—is passed to the user LLM, which generates a realistic reply that reflects the storyline and contextual details using the prompt shown in Listing 38 (line 14). This new user reply is subsequently passed back to the assistant LLM, continuing the conversation. This loop repeats until no further assistant questions are detected or the predefined threshold _δ_ 1 (which is set to two) is reached, preventing infinite cycles. For _δ_ 1 we tested values 2, 3 and 5 which we selected 2 as it produces more realistic dialogues. 

Beyond direct question–answer exchanges, a _follow-up detection module_ (line 21) evaluates whether, in a realistic setting, the user would naturally ask a clarifying or elaborative follow-up. The need for a follow-up is determined using the prompt shown in Listing 36, which takes as input the seed, dialogue history, and the assistant’s most recent response, and outputs yes or no. This decision is guided by factors such as subject complexity, ambiguity in the assistant’s answer, or incompleteness of the response. When a follow-up is required, the module conditions on the seed, the current and prior sub-plans, the most recent _M_ turns, and summaries of earlier turns to generate the follow-up query using the prompt shown in Listing 39. The generated query is then passed back to the assistant LLM for resolution. As with the assistant-question loop, a strict threshold _δ_ 2 (which is set to two like _δ_ 1) limits the number of follow-up exchanges, preventing unbounded cycles. 

Through the interaction of these two threshold-controlled modules, the system produces conversations that exhibit naturalistic bidirectional dynamics, rich contextual references, and realistic clarification behaviors characteristic of human–AI dialogues. 

24 

Published as a conference paper at ICLR 2026 

**Algorithm 1** Conversation plan generation. 

**Input:** domain _c_ , length budget _L_ , title _θ_ , theme _τ_ , subtopics Σ, user profile _u_ , user relationships _ρ_ , timeline Γ, number of conversation sub-plans _N_ , number of bullet-points in each conversation sub-plan _M_ , generator _G_ **Output:** Conversation plan set _p_ 1: _S ←_ ( _c, θ, τ,_ Σ) _▷_ Initialize seed 2: **if** _L ∈{_ 128 _K,_ 500 _K,_ 1 _M }_ **then** 3: Λ _← G_ ( _S_ ) _▷_ Generate narratives using Listing 23 4: _P ← G_ ( _S, u, ρ,_ Γ _, N, M,_ Λ) _▷_ Generate a single conversation plan with Listing 24 5: **else if** _L_ = 10 _M_ **then** 6: _P ←{} ▷_ Initialize set of plans 7: **if** _σ_ = Sequential Expansion **then** 8: _S_<sup>_′_</sup> _← G_ seeds( _S,_ Γ) _▷_ Generate sequential sub-seeds with Listing 28 9: **for** each _s_<sup>_′_</sup> _i_<sup>_∈S′_</sup><sup>**do**</sup> 10: Λ _i ← G_ ( _s_<sup>_′_</sup> _i_<sup>)</sup> _▷_ Generate narratives for sub-seed 11: _b ←_ **1** [ _i_ = 0] _▷_ Binary indicator: 1 if first plan, else 0 12: _Pi ← G_ ( _s_<sup>_′_</sup> _i_<sup>_,_Γ</sup><sup>_i, N,_Λ</sup><sup>_i, u, ρ, Pi−_1</sup><sup>_, i, b_)</sup> _▷_ Generate plan with Listing 30 13: _P ← P ∪{Pi}_ 14: **end for** 15: **else if** _σ_ = Hierarchical Decomposition **then** 16: _S_<sup>_′_</sup> _← G_ decompose( _S,_ Γ) _▷_ Decompose seed with Listing 29 17: **for** each _s_<sup>_′_</sup> _i_<sup>_∈S′_</sup><sup>**do**</sup> 18: Λ _i ← G_ ( _s_<sup>_′_</sup> _i_<sup>)</sup> _▷_ Generate narratives for sub-seed 19: _b ←_ **1** [ _i_ = 0] 20: _Pi ← G_ ( _S, S_<sup>_′_</sup> _, s_<sup>_′_</sup> _i_<sup>_,_Γ</sup><sup>_i, N,_Λ</sup><sup>_i, u, ρ, Pi−_1</sup><sup>_,_</sup> _P_ 0 _,...,i−_ 1 _, i, b_ ) _▷_ Generate plan with Listing 31 21: _P ← P ∪{Pi}_ 22: **end for** 23: **end if** 24: **end if** 25: **return** _P_ 

**Algorithm 2** User questions generation. 

**Input:** seed _S_ , conversation plan _p_ , number of questions per iteration _I_ , generator _G_ **Output:** Question set _Q_ 

1: _p ←{p_ 1 _, . . . , pN } ▷_ Conversation plan with _N_ sub-plans 2: _Q ←{} ▷_ Initialize empty question set 

3: **for** each _pi ∈ P_ **do** 4: _pi_ = _{pi_ 1 _, . . . , piK}_ 5: **for** each _pij ∈ pi_ **do** 6: _Qij ← G_ ( _S, pij, {pi_ 1 _, . . . , pi_ ( _j−_ 1) _}, {p_ 1 _, . . . , pi−_ 1 _},_ I) _▷_ Generate _I_ questions using Listing 32 7: _Q ← Q ∪{Qij} ▷_ Append generated questions to the question set 8: **end for** 

9: **end for** 

10: **return** _Q_ 

25 

Published as a conference paper at ICLR 2026 

### B.3.5 ALGORITHMS 

**Algorithm 3** Answer generation. 

**Input:** question set _Q_ = _{Q_ 1 _, . . . , QN }_ , seed _S_ , conversation plan set _P_ , thresholds _δ_ 1 _, δ_ 2, assistant-question detector _ϕ_ , follow-up detector _ψ_ , generator _G_ **Output:** conversation list _T_ 1: _T ←{} ▷_ Initialize empty conversation list 2: **for** each _Qi ∈ Q_ **do** 3: _Qi_ = _{q_ 1 _, . . . , qJ } ▷_ Questions in sub-plan _i_ 4: **for** each _qj ∈ Qi_ **do** 5: _t ←{} ▷_ Initialize turn sequence 6: _Ht_<sup>(</sup><sup>_M_)</sup> _←_ recent- _M_ turn window at turn _t_ 7: _H t ←_ summary of turns prior to _Ht_<sup>(</sup><sup>_M_)</sup> 8: _P_ ~~(~~ _<p_ ) _←_ summaries of conversation plans preceding _p_ 9: _aij ← G_ assistant( _S, p_ 1:( _i−_ 1) _, Ht_<sup>(</sup><sup>_M_)</sup> _, H t, P_ ~~(~~ _<p_ )) _▷_ Generate assistant response with Listing 37 10: _t ← t ∪{aij} ▷_ Add assistant’s response to current dialogues turn 11: _isQ ← ϕ_ ( _aij, Ht_<sup>(</sup><sup>_M_)</sup> _, H t_ ) _▷_ Checks if assistant response contains question from user with Listing 35 12: _count ←_ 0 13: **while** _isQ_ **and** _count < δ_ 1 **do** 14: _uij ← G_ user( _S, pi, p_ 1:( _i−_ 1) _, P_ ~~(~~ _<p_ ) _, Ht_ ( _M_ ) _, H t, aij_ ) _▷_ Generate user’s response to assistant question with Listing 38 15: _t ← t ∪{uij} ▷_ Add user’s response to current dialogues turn 16: _aij ← G_ assistant( _S, p_ 1:( _i−_ 1) _, Ht_<sup>(</sup><sup>_M_)</sup> _, H t, P_ ~~(~~ _<p_ )) _▷_ Generate assistant’s response 17: _t ← t ∪{aij} ▷_ Add assistant’s response to current dialogues turn 18: _count ← count_ + 1 19: _isQ ← ϕ_ ( _aij, Ht_<sup>(</sup><sup>_M_)</sup> _, H t_ ) 20: **end while** 21: _needFU ← ψ_ ( _aij, Ht_<sup>(</sup><sup>_M_)</sup> _, H t, S_ ) _▷_ Checks if user need to ask followup question with Listing 36 22: _fu_ _~~c~~ ount ←_ 0 23: **while** _needFU_ **and** _fu_ _~~c~~ ount < δ_ 2 **do** 24: _uij ← G_ user( _S, pi, p_ 1:( _i−_ 1) _, P_ ~~(~~ _<p_ ) _, Ht_ ( _M_ ) _, H t, aij_ ) _▷_ Generate user’s followup question with Listing 39 25: _t ← t ∪{uij}_ 26: _aij ← G_ assistant( _S, p_ 1:( _i−_ 1) _, Ht_<sup>(</sup><sup>_M_)</sup> _, H t, P_ ~~(~~ _<p_ )) _▷_ Generate assistant’s response to user’s followup question 27: _t ← t ∪{aij}_ 28: _fu_ _~~c~~ ount ← fu_ _~~c~~ ount_ + 1 29: _needFU ← ψ_ ( _aij, Ht_<sup>(</sup><sup>_M_)</sup> _, H t, S_ ) 30: **end while** 31: _T ←T ∪{t}_ 32: **end for** 33: **end for** 

34: **return** _T_ 

26 

Published as a conference paper at ICLR 2026 

### B.4 USER UTTERANCE GENERATION HYPERPARAMETERS 

Table 6: Batching configuration by chat size and domain category for user-turn question generation. NUM ~~S~~ UBPLANS denotes the number of conversation sub-plans, _K_ the number of batches per sub-plan, and _I_ the number of questions generated per batch. 

|**Chat Size**|**Category**|**NUM**<br>**~~S~~UBPLANS**|**K**|**I**|
|---|---|---|---|---|
||General|5|10|2|
|128K|Coding|3|23|1|
||Math|3|25|1|
||General|10|10|4|
|500K|Coding|10|10|3|
||Math|10|10|4|
||General|10|10|9|
|1M|Coding|10|10|6|
||Math|10|10|6|
||General|10|10|9|
|10M|Coding|10|10|6|
||Math|10|10|6|

### B.5 CREATED PROBING QUESTIONS DISTRIBUTION 

We measure which parts of the dialogue contain the information required to answer the probing questions. To this end, each conversation is divided into ten equal segments, and we record the segment(s) where the supporting evidence for each probing question resides. The detailed methodology for aligning probing questions with dialogue segments is described in Section 2.3. The resulting distributions across conversation lengths are reported in Table 7. 

Table 7: Percentage distribution of created probing questions across ten equal chat segments (deciles) for different chat sizes. Each row corresponds to a segment of the dialogue, moving from the beginning (Segment 1) to the end (Segment 10). 

|**Chat Segment(Decile)**|**100K**|**500K**|**1M**|**10M**|
|---|---|---|---|---|
|1|0.00%|0.65%|0.19%|0.00%|
|2|11.05%|23.70%|21.60%|10.24%|
|3|14.83%|15.91%|20.11%|16.27%|
|4|12.79%|14.45%|15.83%|15.06%|
|5|13.08%|7.95%|9.50%|14.46%|
|6|13.37%|9.09%|8.01%|9.64%|
|7|11.92%|6.33%|5.96%|10.24%|
|8|8.14%|5.52%|5.21%|13.25%|
|9|9.59%|4.55%|4.47%|8.43%|
|10|5.23%|11.85%|9.12%|2.41%|

27 

Published as a conference paper at ICLR 2026 

### B.6 MEMORY ABILITIES EXAMPLES 

To illustrate how our benchmark evaluates different aspects of long-term conversational memory, we provide representative probing questions and their ideal answers for each of the ten memory abilities. These examples demonstrate how each ability is operationalized in practice. 

### 1. **Abstention (withholding answers when information is missing)** 

**Probing Question:** What specific advice did Manuel give about property management companies during the March 5 Investors Meetup? **Ideal Answer:** Based on the provided chat, there is no information related to the specific advice Manuel gave about property management companies. 

2. **Contradiction Resolution (detecting and reconciling inconsistencies)** 

**Probing Question:** Have I ever attended any real estate webinars or investor meetups? **Ideal Answer:** I notice you’ve mentioned contradictory information about this. You said you have never attended any real estate webinars or investor meetups, but you also mentioned attending a webinar about Turkey’s rising demand for multi-family rentals. Which statement is correct? 

3. **Event Ordering (reasoning about chronological sequence)** 

**Probing Question:** How did my focus on different aspects of property investment and management develop throughout our conversations in order? Mention ONLY and ONLY ten items. 

**Ideal Answer:** Your focus developed in this sequence: 1) Agent interaction and preparation, 2) Financial evaluation, 3) Financing and mortgage, 4) Contractor management, 5) Zoning and permits, 6) Renovation planning, 7) Viewing preparation, 8) Negotiation and cash flow, 9) Renovation completion, 10) Commercial property considerations. 

4. **Information Extraction (recalling factual details)** 

**Probing Question:** What amount did I say I had set aside as my initial capital for investing? **Ideal Answer:** You said you had set aside $50,000 as your initial capital. 

5. **Instruction Following (adhering to explicit user constraints)** 

**Probing Question:** How should I allocate my funds for the upcoming quarter? **Ideal Answer:** The response should include an itemized list of costs, category-bycategory breakdown, and detailed cost analysis, reflecting the instruction to always provide detailed financial breakdowns when budgeting. 

6. **Information Update (revising prior facts when updated)** 

**Probing Question:** How much initial capital have I allocated for real estate investing? **Ideal Answer:** $60,000 

7. **Multi-hop Reasoning (integrating evidence across turns)** 

**Probing Question:** How many different banks did I consider for my mortgage options across my conversations? **Ideal Answer:** Two banks: Halkbank and Ziraat Bank. 

8. **Preference Following (adapting to evolving user preferences)** 

28 

Published as a conference paper at ICLR 2026 

**Probing Question:** I’m looking at several properties and want to understand how to approach comparing them effectively. What steps would you suggest I take? **Ideal Answer:** A structured, step-by-step process that emphasizes data collection and analysis, breaking comparisons into measurable factors, reflecting the user’s preference for methodical, data-driven decisions. 

9. **Summarization (abstraction and compression of content)** 

**Probing Question:** Can you give me a comprehensive summary of my journey and decision-making process around investing in rental properties, including how my budget, property choices, management considerations, and financing plans have developed over time? 

**Ideal Answer:** Your journey began with an initial capital of $50,000, followed by exploration of market conditions, renovation planning, property type tradeoffs, financing through Halkbank and Ziraat Bank, and a structured plan for purchase and management. 

10. **Temporal Reasoning (reasoning about durations and timelines)** 

**Probing Question:** How many days are there between my first property viewing with Mehmet Yilmaz and the last one I scheduled? **Ideal Answer:** There are 2 days between the first property viewing on March 25 and the last one on March 27. 

29 

Published as a conference paper at ICLR 2026 

## C DETAILED EXPERIMENTS 

### C.1 ABLATION STUDY 

In this section, we present the complete results of our ablation experiments. All ablations are conducted using Qwen2.5-32B-AWQ as the base model. We evaluate the contribution of individual components in our proposed module as shown in table 8. 

Table 8: Ablation study showing the impact of removing key memory components (retrieval, scratchpad, working memory, and noise filtering) on performance across various conversation lengths (100K–10M). 

|Length|MemoryAbility|Base|w/o Retrieval from Index|w/o Scratchpad|w/o WorkingMemory|w/o Noise Filtering|
|---|---|---|---|---|---|---|
||Abstention|0.475|0.725|0.600|0.575|0.700|
||Contradiction Resolution|0.037|0.043|0.012|0.043|0.018|
||Event Ordering<br>|0.205<br>|0.190<br>|0.194<br>|0.220<br>|0.200<br>|
||Information Extraction|0.479|0.329|0.510|0.451|0.485|
||Instruction Following|0.362|0.375|0.287|0.387|0.312|
|100K|Knowledge Update<br>|0.362<br>|0.237<br>|0.350<br>|0.362<br>|0.312<br>|
||Multi-Hop Reasoning|0.281|0.201|0.248|0.303|0.181|
||Preference Following|0.566|0.675|0.533|0.579|0.491|
||Summarization|0.232|0.232|0.143|0.223|0.103|
||Temporal Reasoning|0.112|0.075|0.125|0.125|0.087|
||Average|0.311|0.311|0.300|**0.327**|0.289|
||Abstention|0.571|0.571|0.585|0.657|0.585|
||Contradiction Resolution|0.017|0.007|0.014|0.017|0.014|
||Event Ordering|0.244|0.222|0.266|0.262|0.229|
||Information Extraction|0.506|0.254|0.466|0.485|0.464|
||Instruction Following|0.295|0.307|0.316|0.334|0.286|
|500K|Knowledge Update|0.278|0.192|0.285|0.235|0.314|
||Multi-Hop Reasoning|0.214|0.104|0.227|0.192|0.247|
||Preference Following|0.571|0.553|0.450|0.547|0.465|
||Summarization|0.344|0.312|0.225|0.353|0.203|
||Temporal Reasoning|0.121|0.042|0.116|0.114|0.130|
||Average|0.316|0.256|0.295|**0.320**|0.294|
||Abstention|0.500|0.664|0.600|0.557|0.507|
||Contradiction Resolution|0.021|0.021|0.035|0.042|0.032|
||Event Ordering|0.200|0.215|0.221|0.227|0.199|
||Information Extraction|0.366|0.246|0.391|0.397|0.366|
||Instruction Following|0.419|0.427|0.335|0.384|0.351|
|1M|Knowledge Update|0.357|0.185|0.321|0.400|0.285|
||Multi-Hop Reasoning|0.209|0.129|0.227|0.221|0.169|
||Preference Following|0.551|0.602|0.536|0.597|0.540|
||Summarization|0.316|0.310|0.169|0.330|0.128|
||Temporal Reasoning|0.154|0.050|0.111|0.121|0.111|
||Average|0.309|0.285|0.295|**0.328**|0.269|
||Abstention|0.550|0.800|0.650|0.650|0.600|
||Contradiction Resolution|0.012|0.000|0.012|0.000|0.000|
||Event Ordering|0.197|0.199|0.199|0.209|0.181|
||Information Extraction|0.350|0.000|0.200|0.150|0.200|
||Instruction Following|0.350|0.175|0.175|0.175|0.050|
|10M|<br>Knowledge Update|0.275|0.050|0.300|0.150|0.225|
||Multi-Hop Reasoning|0.125|0.000|0.125|0.125|0.075|
||Preference Following|0.308|0.191|0.241|0.200|0.175|
||<br>Summarization|0.220|0.119|0.068|0.008|0.050|
||Temporal Reasoning|0.000|0.000|0.050|0.075|0.000|
||Average|**0.238**|0.153|0.202|0.181|0.155|

### C.2 RETRIEVAL BUDGET 

We investigate the impact of the retrieval budget through two sets of experiments: (i) varying the retrieval depth by setting the number of retrieved documents _K ∈{_ 5 _,_ 10 _,_ 15 _,_ 20 _}_ , and (ii) comparing a dense retriever against a sparse retriever (SPLADE). 

The full results examining the effect of different retrieval depths (number of retrieved documents) are presented in Table 9. 

30 

Published as a conference paper at ICLR 2026 

Table 9: Effect of retrieval depth on performance across conversation lengths (100K–10M) and memory abilities. Results are shown for different numbers of retrieved documents ( _K ∈ {_ 5 _,_ 10 _,_ 15 _,_ 20 _}_ ). 

|Length|MemoryAbility|K=5|K=10|K=15|K=20|
|---|---|---|---|---|---|
||Abstention|0.475|0.500|0.625|0.625|
||Contradiction Resolution|0.037|0.025|0.025|0.031|
||Event Ordering|0.205|0.191|0.218|0.210|
||Information Extraction|0.479|0.450|0.412|0.391|
||Instruction Following|0.362|0.362|0.475|0.462|
|100K|Knowledge Update<br>|0.362<br>|0.375<br>|0.350<br>|0.300<br>|
||Multi-Hop Reasoning|0.281|0.322|0.321|0.309|
||Preference Following|0.566|0.591|0.562|0.575|
||Summarization|0.232|0.231|0.218|0.213|
||Temporal Reasoning|0.112|0.162|0.137|0.137|
||Average|0.311|0.321|**0.334**|0.325|
||Abstention|0.571|0.514|0.614|0.642|
||Contradiction Resolution|0.017|0.021|0.071|0.071|
||Event Ordering|0.244|0.229|0.238|0.247|
||Information Extraction|0.506|0.531|0.503|0.507|
||Instruction Following<br>|0.295<br>|0.341<br>|0.390<br>|0.373<br>|
|500K|Knowledge Update|0.278|0.307|0.326|0.326|
||Multi-Hop Reasoning|0.214|0.188|0.234|0.213|
||Preference Following|0.571|0.597|0.628|0.607|
||Summarization<br>|0.344<br>|0.354<br>|0.375<br>|0.376<br>|
||Temporal Reasoning|0.121|0.128|0.121|0.135|
||Average|0.316|0.321|**0.350**|0.350|
||Abstention|0.500|0.521|0.600|0.585|
||Contradiction Resolution|0.021|0.021|0.057|0.053|
||Event Ordering<br>|0.200<br>|0.224<br>|0.240<br>|0.242<br>|
||Information Extraction|0.366|0.398|0.377|0.391|
||Instruction Following|0.419|0.476|0.439|0.446|
|1M|Knowledge Update|0.357|0.350|0.400|0.407|
||Multi-Hop Reasoning|0.209|0.189|0.209|0.190|
||Preference Following<br>|0.551<br>|0.596<br>|0.535<br>|0.514<br>|
||Summarization|0.316|0.317|0.325|0.351|
||Temporal Reasoning|0.154|0.154|0.119|0.199|
||Average|0.309|0.325|**0.330**|0.330|
||Abstention|0.550|0.600|0.650|0.600|
||Contradiction Resolution|0.012|0.012|0.025|0.025|
||Event Ordering|0.197|0.210|0.213|0.236|
||Information Extraction|0.350|0.150|0.300|0.300|
||Instruction Following|0.350|0.150|0.450|0.400|
|10M|<br>Knowledge Update|0.275|0.200|0.300|0.300|
||<br>Multi-Hop Reasoning|0.125|0.100|0.125|0.150|
||Preference Following|0.308|0.175|0.275|0.275|
||Summarization|0.220|0.089|0.196|0.164|
||Temporal Reasoning|0.000|0.025|0.000|0.000|
||Average|0.238|0.171|**0.253**|0.245|

In a complementary experiment, we analyzed the impact of retriever choice. Our base architecture employs a dense retriever, which we compare against the sparse SPLADE-V2 retriever (Formal et al., 2022). As shown in Figure 5 in Appendix C.2, SPLADE yields performance gains of 1.7% at 100K tokens, 0.7% at 500K, and 0.8% at 1M, but results in a slight performance drop of 0.7% at 10M. On average, the sparse retriever provides a modest improvement across conversation lengths. Complete results comparing the dense retriever with SPLADE are presented in Table 10. 

31 

Published as a conference paper at ICLR 2026 

Figure 5: Performance comparison between dense retrieval and sparse retrieval (SPLADE) in LIGHT. 

Table 10: Comparison of dense and sparse retrieval strategies across conversation lengths (100K–10M) and ten memory abilities. The table reports performance when using the default dense retriever versus a sparse retriever (SPLADE). 

|Length|MemoryAbility|Base(Dense retriever)|Sparse retriever(SPLADE)|
|---|---|---|---|
||Abstention|0.475|0.525|
||Contradiction Resolution|0.037|0.43|
||Event Ordering|0.205|0.181|
||Information Extraction|0.479|0.596|
||Instruction Following|0.362|0.400|
|100K|Knowledge Update|0.362|0.350|
||Multi-Hop Reasoning|0.281|0.267|
||Preference Following|0.566|0.562|
||Summarization|0.232|0.230|
||Temporal Reasoning|0.112|0.125|
||Average|0.311|**0.328**|
||Abstention|0.571|0.557|
||Contradiction Resolution|0.017|0.025|
||Event Ordering|0.244|0.226|
||Information Extraction|0.506|0.559|
||Instruction Following|0.295|0.345|
|500K|Knowledge Update|0.278|0.307|
||Multi-Hop Reasoning|0.214|0.212|
||Preference Following|0.571|0.565|
||Summarization|0.344|0.330|
||Temporal Reasoning|0.121|0.107|
||Average|0.316|0.**323**|
||Abstention|0.500|0.564|
||Contradiction Resolution|0.021|0.028|
||Event Ordering|0.200|0.196|
||Information Extraction|0.366|0.392|
||Instruction Following|0.419|0.401|
|1M|Knowledge Update|0.357|0.371|
||Multi-Hop Reasoning|0.209|0.193|
||Preference Following|0.551|0.595|
||Summarization|0.316|0.300|
||Temporal Reasoning|0.154|0.133|
||Average|0.309|**0.317**|
||Abstention|0.550|0.700|
||Contradiction Resolution|0.012|0.000|
||Event Ordering|0.197|0.202|
||Information Extraction|0.350|0.350|
||Instruction Following|0.350|0.250|
|10M|<br>Knowledge Update|0.275|0.375|
||<br>Multi-Hop Reasoning|0.125|0.125|
||Preference Following|0.308|0.200|
||<br>Summarization|0.220<br>32|0.090|
||Temporal Reasoning|0.000|0.025|
||Average|**0.238**|0.231|

Published as a conference paper at ICLR 2026 

### C.3 EFFECT OF EMBEDDING MODEL CHOICE 

We also examined how the choice of embedding model affects the performance of both the RAG baseline and the episodic memory component of LIGHT. In the primary experiments, we used the _BAAI/bge-small-en-v1.5_ embedding model. To assess robustness, we re-ran all experiments using the larger _BAAI/bge-large-en-v1.5_ model while keeping the LLM reader fixed to _GPT-4.1-nano_ . As shown in Table 11, LIGHT consistently outperforms the RAG baseline under both embedding configurations. Moreover, LIGHT exhibits larger gains when switching to the higher-capacity embedding model, achieving an additional 2.08% improvement at the 1M-token setting and 16.37% at the 10M-token setting. These results indicate that LIGHT is robust to changes in embedding quality and can effectively leverage stronger embedding models to enhance long-term memory abilities. 

Table 11: Effect of the embedding model on performance across conversation lengths (100K–10M) and ten memory abilities. Results are shown for the RAG baseline and LIGHT using two different embedding models. 

|Length|MemoryAbility|RAG(bge-small)|Ours(bge-small)|RAG(bge-large)|Ours(bge-large)|
|---|---|---|---|---|---|
||Abstention|0.800|0.575|0.825|0.600|
||Contradiction Resolution<br>Event Ordering|0.018<br>0.169|0.031<br>0.177|0.012<br>0.185|0.031<br>0.171|
||Information Extraction|0.362|0.538|0.404|0.562|
||Instruction Following|0.350|0.400|0.337|0.462|
|100K|Knowledge Update<br>|0.375<br>|0.375<br>|0.325<br>|0.375<br>|
||Multi-Hop Reasoning|0.263|0.365|0.224|0.341|
||Preference Following|0.550|0.625|0.537|0.562|
||Summarization|0.083|0.202|0.089|0.148|
||Temporal Reasoning|0.125|0.162|0.112|0.162|
||Average|0.309|**0.345**|0.305|0.341|
||Abstention|0.828|0.600|0.814|0.571|
||Contradiction Resolution|0.025|0.035|0.028|0.032|
||Event Ordering|0.180|0.204|0.178|0.202|
||Information Extraction|0.382|0.491|0.345|0.454|
||Instruction Following|0.286|0.342|0.303|0.363|
|500K|Knowledge Update|0.288|0.240|0.380|0.321|
||Multi-Hop Reasoning|0.233|0.266|0.272|0.282|
||Preference Following|0.577|0.684|0.571|0.650|
||Summarization|0.184|0.334|0.153|0.316|
||Temporal Reasoning|0.161|0.154|0.126|0.126|
||Average|0.314|**0.335**|0.317|0.331|
||Abstention|0.778|0.678|0.771|0.657|
||Contradiction Resolution|0.028|0.021|0.021|0.025|
||Event Ordering|0.179|0.211|0.194|0.211|
||Information Extraction|0.399|0.410|0.360|0.439|
||Instruction Following|0.271|0.394|0.269|0.421|
|1M|Knowledge Update|0.342|0.392|0.371|0.378|
||Multi-Hop Reasoning|0.293|0.278|0.204|0.254|
||Preference Following|0.513|0.576|0.497|0.598|
||Summarization<br>|0.152<br>|0.290<br>|0.116<br>|0.296<br>|
||Temporal Reasoning|0.064|0.107|0.119|0.150|
||Average|0.302|0.336|0.292|**0.343**|
||Abstention|0.650|0.400|0.800|0.550|
||Contradiction Resolution|0.012|0.025|0.025|0.037|
||Event Ordering|0.201|0.173|0.203|0.171|
||Information Extraction|0.300|0.350|0.300|0.450|
||Instruction Following|0.175|0.250|0.175|0.275|
|10M|<br>Knowledge Update|0.325|0.300|0.325|0.300|
||<br>Multi-Hop Reasoning|0.091|0.135|0.066|0.075|
||<br>Preference Following|0.366|0.425|0.316|0.525|
||<br>Summarization|0.063|0.179|0.100|0.224|
||Temporal Reasoning|0.000|0.025|0.000|0.025|
||Average|0.218|0.226|0.231|**0.263**|

C.4 EFFECT OF INDEXING SETUP 

We also investigated the effect of the vector database indexing setup on the performance of LIGHT. In the primary experiments, we used _IndexFlatIP_ , and in the experiments below, we examined the 

33 

Published as a conference paper at ICLR 2026 

effect of switching the indexing setup to _IndexHNSWFlat_ . For this experiment, the reader LLM was GPT-4.1-nano. The results are shown in Table 12. 

Table 12: Effect of vector database indexing setup on performance across conversation lengths (100K–10M) and ten memory abilities. Results are reported for LIGHT under two different indexing configurations. 

|Length|MemoryAbility|Ours(IndexFlatIP)|Ours(IndexHNSWFlat)|
|---|---|---|---|
||Abstention|0.575|0.600|
||Contradiction Resolution|0.031|0.031|
||Event Ordering<br>|0.177<br>|0.173<br>|
||Information Extraction<br>|0.538<br>|0.565<br>|
||Instruction Following<br>|0.400<br>|0.375<br>|
|100K|Knowledge Update|0.375|0.400|
||Multi-Hop Reasoning|0.365|0.285|
||Preference Following|0.625|0.662|
||Summarization|0.202|0.217|
||Temporal Reasoning|0.162|0.162|
||Average|0.345|**0.347**|
||Abstention|0.600|0.528|
||Contradiction Resolution|0.035|0.032|
||Event Ordering|0.204|0.207|
||Information Extraction<br>|0.491<br>|0.503<br>|
||Instruction Following<br>|0.342<br>|0.332<br>|
|500K|Knowledge Update|0.240|0.226|
||Multi-Hop Reasoning|0.266|0.269|
||Preference Following|0.684|0.666|
||Summarization|0.334|0.317|
||Temporal Reasoning|0.154|0.176|
||Average|**0.335**|0.325|
||Abstention|0.678|0.578|
||Contradiction Resolution|0.021|0.025|
||Event Ordering<br>|0.211<br>|0.211<br>|
||Information Extraction|0.410|0.420|
||Instruction Following|0.394|0.386|
|1M|Knowledge Update|0.392|0.385|
||Multi-Hop Reasoning|0.278|0.278|
||Preference Following|0.576|0.567|
||Summarization|0.290|0.257|
||Temporal Reasoning|0.107|0.128|
||Average|**0.336**|0.324|
||Abstention|0.400|0.600|
||Contradiction Resolution<br>|0.025<br>|0.025<br>|
||Event Ordering|0.173|0.168|
||Information Extraction|0.350|0.350|
||Instruction Following|0.250|0.300|
|10M|<br>Knowledge Update|0.300|0.225|
||<br>Multi-Hop Reasoning|0.135|0.075|
||Preference Following|0.425|0.433|
||Summarization|0.179|0.194|
||Temporal Reasoning|0.025|0.000|
||Average|0.226|**0.237**|

### C.5 SUPPLEMENTARY BASELINE EVALUATION 

Alongside long-context LLMs and RAG, we also evaluated ReadAgent (Lee et al., 2024), another method designed to enhance long-term memory in LLMs, on BEAM and compared it with LIGHT. The results demonstrate that LIGHT consistently outperforms ReadAgent across all four conversation lengths (100K, 500K, 1M, and 10M). The full results are shown in Table 13. 

34 

Published as a conference paper at ICLR 2026 

Table 13: Comparing LIGHT with ReadAgent across conversation lengths (100K–10M) and ten memory abilities. 

|Length|MemoryAbility|ReadAgent|Ours(LIGHT)|
|---|---|---|---|
||Abstention|0.850|0.475|
||Contradiction Resolution|0.000|0.037|
||Event Ordering|0.200|0.205|
||Information Extraction|0.066|0.479|
||Instruction Following|0.237|0.362|
|100K|Knowledge Update<br>|0.150<br>|0.362<br>|
||Multi-Hop Reasoning|0.095|0.281|
||Preference Following|0.425|0.566|
||Summarization|0.045|0.232|
||Temporal Reasoning|0.000|0.112|
||Average|0.206|**0.311**|
||Abstention|0.928|0.571|
||Contradiction Resolution|0.007|0.017|
||Event Ordering|0.237|0.244|
||Information Extraction<br>|0.047<br>|0.506<br>|
||Instruction Following|0.166|0.295|
|500K|Knowledge Update|0.014|0.278|
||Multi-Hop Reasoning|0.022|0.214|
||<br>Preference Following|0.386|0.571|
||Summarization|0.069|0.344|
||Temporal Reasoning|0.028|0.121<br>|
||Average|0.191|**0.316**|
||Abstention|0.792|0.500|
||Contradiction Resolution|0.003|0.021|
||Event Ordering|0.211|0.200|
||Information Extraction|0.106|0.366|
||Instruction Following|0.166|0.419|
|1M|Knowledge Update|0.014|0.357|
||Multi-Hop Reasoning|0.105|0.209|
||Preference Following|0.391|0.551|
||Summarization|0.041|0.316|
||Temporal Reasoning|0.033|0.154|
||Average|0.186|**0.309**|
||Abstention|0.750|0.550|
||Contradiction Resolution|0.000|0.012|
||Event Ordering|0.205|0.197|
||Information Extraction|0.000|0.350|
||Instruction Following|0.300|0.350|
|10M|Knowledge Update|0.000|0.275|
||<br>Multi-Hop Reasoning|0.000|0.125|
||<br>Preference Following|0.166|0.308|
||<br>Summarization|0.061|0.220|
||Temporal Reasoning|0.000|0.000|
||Average|0.148|**0.238**|

35 

Published as a conference paper at ICLR 2026 

## D NUGGET DESIGN 

In this section, we provide illustrative examples for each memory ability, demonstrating how nuggets are derived from the corresponding probing questions. 

### 1. **Abstention** 

**Objective:** The correct behavior is to acknowledge that the requested information is not present in the provided conversation. **Rubric pattern:** Each atomic unit should be in this format: _States that, based on the provided chat, there is no information about <target topic>_ **Example JSON:** 

{ "question": "What specific advice did Manuel give about property management companies during the March 5 Investors Meetup?", "ideal_response": "Based on the provided chat, there is no information related to the specific advice Manuel gave about property management companies.", "source_chat_ids": {}, "rubric": [ "Based on the provided chat, there is no information related to the specific advice Manuel gave about property management companies." ] } 

### 2. **Contradiction Resolution** 

**Objective:** Correct behavior is that the LLM should detect the contradiction and state both contradictory information while requesting clarification. **Rubric pattern:** 

- States there is contradictory information. 

- Mentions claim <A> 

- Mentions claim <B> 

• Requests clarification about which statement is correct **Example JSON:** { "question": "Have I ever attended any real estate webinars or investor meetups?" , "ideal_answer": "I notice you’ve mentioned contradictory information about this. You said you have never attended any real estate webinars or investor meetups, but you also mentioned attending a webinar about Turkey’s rising demand for multi-family rentals. Which statement is correct?", "source_chat_ids": { "first_statement": [ ], "second_statement": [ ] }, "rubric": [ "LLM response should state: there is contradictory information", "LLM response should mention: You said you have never attended any real estate webinars or investor meetups", "LLM response should mention: you also mentioned attending a webinar about Turkey\u2019s rising demand for multi-family rentals", "LLM response should mention: which statement is correct?" ] } 

### 3. **Event Ordering** 

**Objective:** Correct behavior is the model lists a sequence of events/topics in the correct chronological order. **Rubric pattern:** 

- LLM response should mention: <event 1> 

• ... 

36 

Published as a conference paper at ICLR 2026 

- LLM response should mention: <event N> 

- **Example JSON:** 

{ "question": "How did my focus on different aspects of property investment and management develop throughout our conversations in order? Mention ONLY and ONLY ten items.", "answer": "Your focus on property investment and management developed in this sequence: 1) Initial engagement with the local agent and preparation for property viewings, 2) Evaluation of property financials including ROI and rental income potential, 3) Exploration of financing options and mortgage concerns, 4) Handling contractor performance and repair negotiations, 5) Understanding zoning regulations and permit requirements for property conversions, 6) Planning and prioritizing renovations and investment risks for multi-family properties, 7) Detailed preparation for property viewings involving both agent and contractor, 8) Negotiation strategies and cash flow implications related to repair costs, 9) Final renovation project completion steps and portfolio diversification strategies, 10) Consideration of commercial property types and location factors for longterm investment.", "ordering_tested": [ "1st: Agent interaction and viewing preparation", "2nd: Property financial evaluation", "3rd: Financing and mortgage concerns", "4th: Contractor management", "5th: Zoning and permits", "6th: Renovation planning and investment risks", "7th: Viewing preparation with agent and contractor", "8th: Repair cost negotiation and cash flow", "9th: Renovation completion and portfolio diversification", "10th: Commercial property and location considerations" ], "source_chat_ids": [], "rubric": [ "LLM response should mention: Agent interaction and viewing preparation", "LLM response should mention: Property financial evaluation", "LLM response should mention: Financing and mortgage concerns", "LLM response should mention: Contractor management", "LLM response should mention: Zoning and permits", "LLM response should mention: Renovation planning and investment risks", "LLM response should mention: Viewing preparation with agent and contractor" , "LLM response should mention: Repair cost negotiation and cash flow", "LLM response should mention: Renovation completion and portfolio diversification", "LLM response should mention: Commercial property and location considerations", "Presents the events in the correct chronological order" ] } 

4. **Information Extraction** 

**Objective:** LLM should answer the questioned facts correctly. 

**Rubric pattern:** 

• Instantiate one criterion per fact directly from the ideal answer, using the stem “LLM response should state/mention:” **Example JSON:** 

{ "question": "What amount did I say I had set aside as my initial capital for investing?", "ideal_answer": "You said you had set aside $50,000 as your initial capital.", "source_chat_ids": [], "rubric": [ "LLM response should state: $50,000" ] } 

5. **Instruction Following** 

37 

Published as a conference paper at ICLR 2026 

**Objective:** LLM should adhere to format and/or content priorities stated in the conversation. **Rubric pattern:** • Use instruction ~~b~~ eing ~~t~~ ested (the explicit instruction) and decompose expected ~~c~~ ompliance into atomic criteria **Example JSON:** 

{ "question": "How should I allocate my funds for the upcoming quarter?", "instruction_being_tested": "Always provide detailed financial breakdowns when I ask about budgeting decisions.", "expected_compliance": "Response should include itemized costs, specific amounts for different categories, and detailed breakdown rather than just a total estimate", "source_chat_ids": [], "rubric": [ "LLM response should contain: itemized list of costs", "LLM response should contain: category-by-category breakdown", "LLM response should contain: detailed cost analysis" ] } 

### 6. **Knowledge Update** 

**Objective:** LLM must reflect updated values when prior values have changed over time. **Rubric pattern:** • Derive criteria from the ideal answer, using the stem “LLM response should state/mention:” for the updated value(s). **Example JSON:** { "question": "How much initial capital have I allocated for real estate investing ?", "answer": "$60,000", "source_chat_ids": { "original_info": [ ], "updated_info": [ ] }, "rubric": [ "LLM response should state: $60,000" ] } 

7. **Multi-hop Reasoning** 

**Objective:** LLM must aggregate or compare information spanning multiple sessions. **Rubric pattern:** • Instantiate criteria from the ideal answer for each required intermediate or aggregated fact. **Example JSON:** { "question": "How many different banks did I consider for my mortgage options across my conversations?", "answer": "Two banks: Halkbank and Ziraat Bank.", "source_chat_ids": [], "rubric": [ "LLM response should state: Two banks", "LLM response should state: Halkbank", "LLM response should state: Ziraat Bank" ] } 

8. **Preference Following** 

38 

Published as a conference paper at ICLR 2026 

**Objective:** LLM must generate content consistent with user-specified preferences. **Rubric pattern:** 

- Use preference ~~b~~ eing ~~t~~ ested (the user’s stated preference) and decompose expected ~~c~~ ompliance into atomic criteria. 

- **Example JSON:** 

{ "question": "I’m looking at several properties and want to understand how to approach comparing them effectively. What steps would you suggest I take?", "preference_being_tested": "I prefer methodical, data-driven decisions over impulsive purchases, reflecting my analytical nature.", "expected_compliance": "Response should outline a structured, step-by-step approach that involves gathering and analyzing relevant data before making a choice, rather than suggesting quick or impulsive actions.", "source_chat_ids": [], "rubric": [ "LLM response should contain: provides a clear, logical process", "LLM response should contain: emphasizes data collection and analysis", "LLM response should contain: breaks down comparison into measurable factors " ] } 

### 9. **Summarization** 

**Objective:** LLM must provide a comprehensive summary covering required content elements. **Rubric pattern:** 

- Decompose ideal ~~s~~ ummary into atomic content units; use the stem “LLM response should contain:”. 

- **Example JSON:** 

{ "question": "Can you give me a comprehensive summary of my journey and decisionmaking process around investing in rental properties, including how my budget, property choices, management considerations, and financing plans have developed over time?", 

"ideal_summary": "Your journey toward investing in rental properties began with an initial capital of $50,000, which you questioned as potentially insufficient for purchasing a property within 12 months. Early discussions highlighted the need to research local market conditions, down payment requirements, and additional costs like closing fees and renovations, revealing that typical investments might exceed your initial capital. You explored identifying good fixer-upper properties by learning to recognize signs such as structural issues and outdated features, emphasizing the importance of cost-benefit analysis for renovations. As your plans progressed, you weighed the pros and cons of investing close to your location versus elsewhere, balancing ease of management against market diversity and growth potential. You also considered the choice between single-family homes and multi-family units, analyzing factors like rental yield, management complexity, and investment scale, with examples showing similar yields but differing capital needs. Financing options were carefully compared, particularly between Halkbank and Ziraat Bank mortgages , focusing on interest rates, fees, and service quality to optimize costs. Throughout, you developed a step-by-step plan for purchasing your first rental property, including market research, budgeting, inspections, financing, and tenant management, with timelines to reduce anxiety and ensure readiness. This comprehensive process reflects a thoughtful evolution from initial capital concerns to detailed investment strategies, property evaluation, financing decisions, and management planning, all aimed at making informed, balanced real estate investment choices.", "source_chat_ids": [], "rubric": [ "LLM response should contain: investing in rental properties began with an initial capital of $50,000", "LLM response should contain: Early discussions highlighted the need to research local market conditions, down payment requirements, and additional costs like closing fees", "LLM response should contain: You explored identifying good fixer-upper properties by learning to recognize signs such as structural issues and outdated features", 

39 

Published as a conference paper at ICLR 2026 

"LLM response should contain: you weighed the pros and cons of investing close to your location versus elsewhere, balancing ease of management against market diversity and growth potential", "LLM response should contain: You also considered the choice between singlefamily homes and multi-family units, analyzing factors like rental yield, management complexity, and investment scale", "LLM response should contain: Financing options were carefully compared, particularly between Halkbank and Ziraat Bank mortgages, focusing on interest rates, fees, and service quality to optimize costs", "LLM response should contain: you developed a step-by-step plan for purchasing your first rental property, including market research, budgeting, inspections, financing, and tenant management" ] } 

### 10. **Temporal Reasoning** 

**Objective:** LLM must compute or restate durations and timeline relations correctly. **Rubric pattern:** • Derive criteria from the ideal answer, using the stem “LLM response should state:”. **Example JSON:** { "question": "How many days are there between my first property viewing with Mehmet Yilmaz and the last one I scheduled?", "answer": "There are 2 days between the first property viewing on March 25 and the last one on March 27.", "calculation_required": "March 27 - March 25 = 2 days", "source_chat_ids": { "first_event": [], "second_event": [] }, "rubric": [ "LLM response should state: 2 days", "LLM response should state: from March 25, 2024 till March 27, 2024" ] } 

40 

Published as a conference paper at ICLR 2026 

## E EXAMPLES FROM DIFFERENT COMPONENTS OF BEAM 

In this section, we provide illustrative examples of generating a chat in the _coding_ domain. Specifically, we include a representative _chat seed_ with its domain, title, theme, and subtopics, followed by the corresponding _narratives_ , where only a truncated set is shown for brevity. We then present the _user profile_ and the user’s social _relationships_ . Next, we provide excerpts from the _conversation plans_ , showing only a subset of bullet points from each sub-plan while preserving their full descriptions to maintain clarity. Finally, we provide samples of the _generated chat_ , highlighting exchanges where the user shares or requests code, and including follow-up turns to demonstrate the naturalistic back-and-forth flow. Together, these examples illustrate how different components of BEAM interact to form coherent, long-context dialogues. 

### Chat Seed 

**Domain:** Coding **Title:** Automating Social Media Posts with Python **Theme:** Scheduling and posting content across multiple platforms **Subtopics:** _· ·_ • Twitter API integration Facebook Graph API usage Instagram automation tools 

- Scheduling with cron jobs / APScheduler 

- Image and caption management; hashtag generation 

- Error handling for failed posts; tracking engagement metrics 

### Narratives (Truncated) 

**Technical Problem-Solving:** Debugging Twitter OAuth/403/429; fixing hashtag validation; profiling scheduler bottlenecks. 

**Learning & Knowledge:** API docs comprehension (Twitter v2, Facebook Graph v12–15); best practices for Instagram automation; mastering cron/APScheduler. **Progress & Development:** Setting up Twitter/Facebook integrations; building Instagram tools; designing scheduling algorithms. **Implementation:** Feature implementation and refactoring for efficiency; async migration; retry and backoff strategies. **Framework & Technology:** Python libraries (Tweepy, facebook-sdk, requests); APScheduler/cron; Redis; asyncio. **Testing & QA:** Unit/integration/E2E tests (pytest, Selenium); TDD for schedulers and hashtag rules. **DevOps & Deployment:** CI/CD (GitHub Actions), containerization (Docker), EC2 deployment, blue–green releases. 

**Data:** PostgreSQL schemas, indices, ETL for engagement metrics, Redis caching. **Integration & APIs:** Webhooks, message queues (RabbitMQ), API Gateway, SNS/Lambda. **Performance:** Caching, load balancing (HAProxy), CPU/memory targets, throughput goals. **Security/Compliance:** OAuth, token rotation, TLS, GDPR. **PM & Workflow:** Sprints, reviews, documentation standards. 

User Profile 

**Name:** John Brooks **Age:** 52 **Gender:** Male **Location:** Port Charles, Luxembourg **Profession:** Secretary/Administrator 

**Personality:** He is a pillar of his community, always ready to lend a helping hand and offer guidance when needed. With a strong sense of tradition and order, he values honesty and dedication, often taking on a mentorship role to help others. His diligent and efficient approach to planning and organization makes him a reliable asset to those around him. He has a warm and welcoming demeanor, always willing to open his heart and home to friends, loved ones, and neighbors. Despite his strong convictions, he believes in the power of hospitality and good manners, often going out of his way to make others feel supported and cared for. 

41 

Published as a conference paper at ICLR 2026 

With a dry sense of humor and a quick wit, he can be entertaining to be around, but he’s not afraid to speak his mind and challenge the status quo when necessary. His practical and responsible nature makes him a respected member of his community, and his ability to stay grounded and logical in stressful situations is a valuable asset to those around him. 

Relationships 

**Parents:** Elizabeth (74), Robert (76) **Partner:** Shannon (48) **Close Friends:** Taylor (51), Teresa (62), Thomas (44), Charles (56), Patricia (46) **Acquaintances/Colleagues:** Wesley (26), Jason (59), Claudia (15), Janice (13), Dana (55) 

Conversation Plan (Only a few representative bullets from each sub-plan) 

### **Subplan 1 — March 1, 2024** 

- **Project Initialization:** I’m setting up a Python 3.10 environment with Tweepy v4.10.1 and Facebook SDK v3.1.0 for API integrations. 

- **Security & Compliance Labels: Authentication for Twitter API Integration:** Implemented OAuth 1.0a with environment variables TWITTER ~~A~~ PI ~~K~~ EY and TWITTER ~~A~~ PI SECRET securely stored. 

- **Database & Data Management Labels: Database Design for Social Media Posting:** Designed PostgreSQL 14 schema with tables for posts, platforms, and scheduling metadata. 

- **User Instruction:** Always include exact API version numbers when I ask about integration details. 

- **Logical Contradiction:** I have never registered a Twitter Developer account or created any Twitter app. 

### **Subplan 2 — March 20, 2024** 

- **Technical Problem-Solving Labels: Debugging Twitter API Integration:** Fixed “403 Forbidden” error caused by missing media upload step before tweet creation. 

- **Implementation & Development Labels: Code Refactoring for Performance:** Refactored twitter ~~p~~ ost.py to async functions using asyncio, improved throughput by 30%. 

- **Security & Compliance Labels: Authorization for Facebook Graph API:** Implemented OAuth 2.0 flow with refresh tokens stored encrypted using Fernet symmetric encryption. 

- **Information Update:** The Instagram automation prototype sprint deadline was adjusted to April 5, 2024, to allow additional testing of media upload features. 

### **Subplan 3 — April 5, 2024** 

- **Implementation & Development Labels: Implementing Error Handling:** Added retry logic with exponential backoff for Instagram API 429 Too Many Requests errors. 

- **Performance & Optimization Labels: Caching Strategies for Image and Caption Management:** Implemented Redis caching for resized images, reducing image processing time from 800ms to 200ms. 

- **Debugging & Troubleshooting Labels: Incident Response for Social Media Automation:** Responded to March 30, 2024, outage caused by expired Instagram tokens, implemented alerting via Slack webhook. 

### **Subplan 4 — April 20, 2024** 

- **Implementation & Development Labels: Algorithm Optimization for Scheduling:** Rewrote scheduling algorithm to use async priority queues, reducing average job dispatch latency from 500ms to 150ms. 

42 

Published as a conference paper at ICLR 2026 

- **Framework & Technology Labels: Integrating Twitter API with Python:** Upgraded Tweepy from v4.10.1 to v4.12.1 to leverage new media upload endpoints. 

- **Security & Compliance Labels: Authentication for Twitter API Integration:** Rotated Twitter API keys on April 15, 2024, updated environment variables TWITTER ~~A~~ PI ~~K~~ EY and TWITTER ~~A~~ PI SECRET. 

### **Subplan 5 — May 5, 2024** 

- **Progress & Development Labels: Building Hashtag Generation Tools:** Developed hashtag generator supporting dynamic keyword extraction using spaCy v3.5.0 NLP library. 

- **Database & Data Management Labels: Data Warehousing for Engagement Metrics:** Designed PostgreSQL 14 schema for engagement ~~m~~ etrics with partitioning by month for scalability. 

- **Debugging & Troubleshooting Labels: Log Analysis for Facebook Graph API:** Detected “OAuthException: Error validating access token” on May 1, 2024, resolved by token refresh automation. 

### **Subplan 6 — May 20, 2024** 

- **Implementation & Development Labels: Implementing Error Handling:** Added centralized error handler middleware in posting API, logging errors with Sentry v1.12.0. 

- **Debugging & Troubleshooting Labels: Error Diagnosis for Twitter API Integration:** Fixed intermittent “ConnectionResetError” during media upload by adding retry with jitter. 

- **DevOps & Deployment Labels: Containerization for Instagram Automation:** Updated Dockerfile to use multi-stage builds, reduced image size from 120MB to 85MB. 

### **Subplan 7 — June 5, 2024** 

- **DevOps & Deployment Labels: Deploying Social Media Automation Tools:** Deployed v1.0.0 release on AWS EC2 t3.medium with 99.9% uptime SLA. 

- **Integration & API Labels: Event-Driven Architecture for Social Media Automation:** Implemented AWS SNS topics for post status updates, integrated with Lambda v3.2.1 functions. 

- **User Experience & Interface Labels: Mobile App Design for Social Media Automation:** Released beta version of React Native app on Android with basic scheduling and metrics display. 

### **Subplan 8 — June 20, 2024** 

- **Progress & Development Labels: Developing Instagram Automation Tools:** Implemented batch media uploads for Instagram, supporting up to 10 images per carousel post. 

- **User Experience & Interface Labels: Responsive Design for Scheduling:** Enhanced React 18.2 dashboard for scheduling with drag-and-drop post reordering, tested on Chrome and Safari. 

- **Security & Compliance Labels: Encryption for Instagram Automation:** Migrated token storage to AWS KMS encrypted S3 bucket, access controlled via IAM roles. 

### **Subplan 9 — July 5, 2024** 

- **Security & Compliance Labels: Authentication for Twitter API Integration:** Implemented OAuth 2.0 PKCE flow for enhanced security, tested with Postman v10.15.0. 

- **Performance & Optimization Labels: Code Optimization for Twitter API Integration:** Reduced memory usage by 20% by optimizing data serialization and connection pooling. 

- **Debugging & Troubleshooting Labels: Error Diagnosis for Twitter API Integration:** Fixed “TimeoutError” during high load by increasing HTTP client timeout from 10s to 30s. 

43 

Published as a conference paper at ICLR 2026 

### **Subplan 10 — July 20, 2024** 

- **DevOps & Deployment Labels: Deploying Social Media Automation Tools:** Completed production rollout on July 18, 2024, with zero downtime and 99.95% uptime in first 48 hours. 

- **Integration & API Labels: Event-Driven Architecture for Social Media Automation:** Fully implemented AWS SNS event bus with Lambda v3.2.1 for asynchronous post status updates. 

- **Testing & Quality Assurance Labels: End-to-End Testing for Instagram Automation:** Verified Instagram automation stability with 1000+ posts over 7 days, no failures reported. 

Generated Dialogues (Exemplars, Truncated) 

Turn 1 (Mar 1, 2024) 

**User:** I’m trying to set up a Python 3.10 environment for automating social media posts, and I’ve chosen Tweepy v4.10.1 and Facebook SDK v3.1.0 for API integrations, but I’m not sure how to structure my project for better outreach. Can you help me plan this out in terms of scheduling and deadlines? 

### **Assistant:** 

Certainly! Setting up an automated posting system with Tweepy and Facebook SDK is a great start. 

Project Structure: 

1. Project Setup (Mar 1–7) [Truncated ...] 

2. Content Creation (Mar 8–14) [Truncated ...] 

3. Automation Development (Mar 15–21) [Truncated ...] 

4. Deployment and Monitoring (Mar 22–28) [Truncated ...] 

### **User (Follow-up)** 

That sounds like a great plan! One thing though—could we add a step for testing posts on a smaller scale before full deployment? Just to make sure everything looks good and functions as expected. 

### **Assistant** 

Absolutely, adding a step for testing the posts on a smaller scale is a great idea to ensure everything looks good and functions as expected before full deployment. Here’s how you can incorporate that into the existing plan: ### Updated Project Structure #### 1. **Project Setup [Trunicated ...] #### 4. **Testing Phase (March 22 - March 24, 2024)** - **Days 22-23:** Conduct a small-scale test. - Post a few test messages to a limited audience or a test account. - Verify that the posts look good and function as expected. - **Day 24:** Review the test results. - Address any issues found during the test phase. 

- Make final adjustments to the automation script and content. 

[Trunicated ...] 

### **User (Mid-turn) -> Code Sharing** 

I’m trying to implement a feature to collect engagement metrics for Instagram posts, but I’m not sure how to integrate it with the existing PostgreSQL schema. I’ve designed a table for instagram ~~p~~ osts with foreign key to posts table, but I’m not sure how to handle the data migration. Can you help me with that? Here’s my code: 

import psycopg2 conn = psycopg2.connect(dbname=\"engagement_metrics\", 

user=\"username\", 

44 

Published as a conference paper at ICLR 2026 

password=\"password\", host=\"localhost\", port=\"5432\") cur = conn.cursor() cur.execute(\"\"\" CREATE TABLE instagram_posts (id SERIAL PRIMARY KEY, post_id INTEGER REFERENCES posts(id), engagement_metrics JSONB); \"\"\")\n\nconn.commit() cur.close() conn.close() 

**Assistant -> Code Review** Your approach is good! Consider adding NOT NULL, timestamps, and indexes for performance ... 

CREATE TABLE IF NOT EXISTS instagram_posts ( id SERIAL PRIMARY KEY, post_id INTEGER NOT NULL REFERENCES posts(id), engagement_metrics JSONB, created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ); CREATE INDEX IF NOT EXISTS idx_instagram_posts_post_id ON instagram_posts(post_id); 

[Truncated ...] plus safe migration with INSERT SELECT to backfill existing posts. 

**User -> Deployment** I’m trying to deploy my updated posting services to an AWS EC2 t3.medium instance with 2 vCPUs and 4GB RAM, but I’m running into some issues with the deployment process. Can you help me figure out how to properly deploy my application to this instance, considering the DevOps and deployment aspects? I’ve been using Docker to containerize my application, and I’m not sure what changes I need to make to ensure a smooth deployment. Here’s a snippet of my current Dockerfile: 

FROM python:3.10-slim WORKDIR /app COPY requirements.txt . RUN pip install -r requirements.txt COPY . . CMD ["python", "app.py"] 

**Assistant -> Deployment Guidance** Install Docker on EC2, push image to registry, pull with pinned tag, and run with --restart=always [Truncated ...] add healthchecks and a minimal systemd unit [Truncated ...] **User (Follow-up)** hmm, what’s the best way to automate the pulling and running of the Docker container? **Assistant -> CI/CD Automation** Use GitHub Actions with SSH deploy step [Truncated ...] 

name: Deploy on: { push: { branches: [main] } } jobs: deploy: runs-on: ubuntu-latest steps: - uses: actions/checkout@v4 - run: | ssh -i id_rsa ec2-user@EC2_DNS \ "docker stop socauto || true && docker rm socauto || true && docker pull username/your-app:sha-${GITHUB_SHA} && docker run -d --restart=always -p 80:80 username/your-app:sha-${GITHUB_SHA}" 

**User (Follow-up)** hmm, what’s the best way to handle environment variables for different stages like dev and prod? 

45 

Published as a conference paper at ICLR 2026 

**Assistant -> Env Vars** 

Use separate .env.dev / .env.prod files locally. In production, prefer AWS SSM Parameter St46ore or Secrets Manager [Truncated ...] inject via --env-file or systemd environment exports. 

## F CASE STUDY 

The scratchpad serves as a persistent, iteratively compressed semantic layer that (i) consolidates scattered entities and facts (improving _Information Extraction_ ), (ii) preserves user-level metainstructions alongside task context (improving _Instruction Following_ ), (iii) records state changes and overrides (improving _Information Update_ ), and (iv) normalizes timeline cues into explicit anchors (improving _Temporal Reasoning_ ). Out of the ten memory abilities in our benchmark, we present case studies from these four; however, the scratchpad provides similar benefits for the remaining six abilities as well. Below we contrast “LIGHT with all components” versus “LIGHT w/o scratchpad” on representative probes, and show the exact scratchpad cue that enabled the correct answer. 

### Information Extraction 

**(1) Question:** Which versions of the tools did I say I was using to start my project? **Correct Answer:** Python 3.10, spaCy v3.5, Flask 2.2, PyMuPDF 1.22.0 **LIGHT with all components:** Python 3.10, spaCy v3.5, Flask 2.2, PyMuPDF 1.22.0 **LIGHT wo scratchpad:** Based solely on the provided context, there is no direct answer to this question **Scratchpad cue (excerpt):** **KEY ENTITIES & RELATIONSHIPS:** ...... [trunecated] - Technologies: Python 3.10, spaCy v3.5, Flask 2.2/2.2.3, PyMuPDF 1.22.0, scikit-learn v1.2.2, Redis, RabbitMQ, Docker ...... [trunecated] 

**(2) Question:** Can you remind me of the city and country I said I live in, along with my age? **Correct Answer:** New Gary, Saint Helena; 26 **LIGHT with all components:** New Gary, Saint Helena; 26 **LIGHT wo scratchpad:** No information provided about your city, country, or age in the given context **Scratchpad cue (excerpt):** **KEY ENTITIES & RELATIONSHIPS:** - **Primary individuals:** User and partner Wendy (both turning 26 on March 3, 2024) - **Friends and collaborators:** Joe (writer, 35), Stacy ...... [trunecated] - **Locations:** New Gary, Saint Helena; Island Art Gallery; Saint Helena Book Fair; Saint Helena Community Center; GreenLeaf Nursery; Island Finds thrift store; Saint Helena Charity; The Lighthouse Bistro 

### Instruction Following 

**Question:** Can you tell me about the mentoring activities I’ve been involved in recently? 

**User instruction:** Always provide the number of team members involved when I ask about mentoring activities. **Correct Answer:** Mentions number of team members **LIGHT with all components:** Mentoring 3 junior editors **LIGHT wo scratchpad:** No recent mentoring activities noted in the provided context **Scratchpad cue (excerpt):** ...... [trunecated] The user requested to always include the number of team members when discussing mentoring activities. ...... [trunecated] *Mentoring & Crisis Management:* 

46 

Published as a conference paper at ICLR 2026 

- Mentoring 3 junior editors; balancing mentoring with crisis management. ...... [trunecated] 

### Knowledge Update 

**(1) Question:** What is the typical memory usage per session for batch resume processing? **Correct Answer:** Around 140MB per session **LIGHT with all components:** ˜140MB **LIGHT wo scratchpad:** The typical memory usage per session for batch resume processing can vary widely depending on the complexity of the resumes and the system’s available memory, but optimizing with batch sizes and efficient data handling can keep it under 100MB per resume. **Scratchpad cue (excerpt):** ...... [trunecated] - Memory optimization: - Reduce peak memory usage from 250MB to 140MB per batch. ...... [trunecated] 

**(2) Question:** What is the deadline for completing the Instagram automation prototype sprint? **Correct Answer:** April 5, 2024 **LIGHT with all components:** April 5, 2024 **LIGHT wo scratchpad:** April 1, 2024 **Scratchpad cue (excerpt):** **PROCESSES & WORKFLOWS:** 1. **Project Planning & Sprint Management:** ...... [trunecated] 

- Instagram automation sprint extended to April 5, 2024. 

### Temporal Reasoning 

**(1) Question:** How many days passed between when I met my mom at home and when I completed my first successful batch of Miche’s sourdough? **Correct Answer:** Jan 6 – Jan 1 = 5 days **LIGHT with all components:** 5 days **LIGHT wo scratchpad:** 37 days **Scratchpad cue (excerpt):** **IMPORTANT DATES:** - **January 1, 2024:** Met mother Brittney at home. - **January 5-6, 2024:** Completed first batch of Michele’s sourdough. ...... [trunecated] 

**(2) Question:** How many days do I have between finalizing my survey plans at Caf´e Soleil and attending the Raymondburgh Startup Meetup to prepare effectively? **Correct Answer:** Mar 28 – Mar 10 = 18 days **LIGHT with all components:** 18 days **LIGHT wo scratchpad:** 28 days **Scratchpad cue (excerpt):** **IMPORTANT DATES:** - **March 10, 2024**: Paper-based customer survey at Cafe Soleil. - **March 28, 2024**: Raymondburgh Startup Meetup. ...... [trunecated] 

**Takeaways.** Across abilities, removing the scratchpad consistently causes failures that the full model avoids. In _Information Extraction_ , the scratchpad aggregates dispersed entity/version mentions so the model can recover exact tool versions and bios (city/age). For _Instruction Following_ , it retains user meta-preferences (e.g., “always include team count”), ensuring style/format compliance even many turns later. For _Knowledge Update_ , it encodes overrides (e.g., extended deadline; reduced memory), preventing stale answers. For _Temporal Reasoning_ , it surfaces normalized date anchors, enabling simple, correct day-difference calculations. These examples show that the scratchpad provides a high-utility semantic scaffold that complements working (recency) and episodic (retrieval) memory, yielding robust long-context behavior. 

47 

Published as a conference paper at ICLR 2026 

## G QUALITATIVE ERROR ANALYSIS 

We conduct a qualitative analysis of failure cases across the ten memory abilities in our benchmark to better characterize the limitations of LIGHT and identify systematic patterns. For each ability, we manually inspected probing questions that LIGHT answered incorrectly and analyzed the underlying reasons. Below, we summarize the dominant error modes observed for each ability. 

**Abstention** In this ability, the LLM should abstain from answering because the answer to the probing question is not present in the conversation. Therefore, the context that LIGHT provides to the LLM does not contain the required information. One failure mode occurs when the context contains nothing relevant to the question, yet the LLM hallucinates and generates an answer. This is because these LLMs are usually trained to always provide an answer, regardless of actually having this knowledge (Kalai et al., 2025). Another hallucination pattern occurs when the LLM produces an answer entirely unrelated to the question, which stems from the long-context nature of the task and the inability of the LLM to understand the context correctly. The main failure mode, however, arises when the context contains information about entities, dates, or concepts that are similar to, but not the same as, the information requested by the question. In these cases, the LLM uses these similar details and generates an answer instead of abstaining. This pattern is the primary failure mode for abstention. 

**Contradiction Resolution** For this ability, the LLM should identify the contradiction, state both sides, and request clarification. One common failure mode occurs when the context contains only one side of the contradiction, leading the LLM to answer based solely on that information. Since the model does not have access to the other side of the story, it cannot detect the conflict. Another common failure occurs when both sides of the contradiction are present in the context, but the LLM still overweighs one side of the contradiction due to position and frequency bias for that side in the context. 

**Event Ordering** In this ability, the LLM should recognize and reconstruct the sequence of evolving information in the conversation. A common failure occurs when the context contains items from the sequence but the LLM does not include them in the response. Another failure mode occurs when the model includes the items but presents them in the wrong order. This happens because the retrieval model retrieves based on similarity, which does not necessarily preserve temporal order, leaving the LLM without clues about the correct sequence of events. Also, in many cases, the retriever does not retrieve all the events related to the question. 

**Information Extraction** In this ability, one failure mode arises when the context does not contain the answer to the question; thus, the LLM cannot extract the answer from the retrieved context. Another occurs when the answer is present, but the LLM produces an incorrect answer because it becomes confused by details in the context that are similar to the answer. A third failure happens when the answer is present but the LLM provides an incomplete answer. 

**Instruction Following** For this ability, the LLM should adhere to user-specified instructions. Failures occur either when the user instruction is present in the context, but the LLM does not follow it, or when the instruction is missing from the context, and the LLM cannot answer the question without it. 

**Knowledge Update** Here, the LLM should answer the question using the updated version of the facts. One failure mode occurs when the context contains only the old value and does not include the updated value, causing the LLM to respond using outdated information, because the retrieval model retrieves based on similarity, which does not necessarily preserve temporal order. A more common failure mode occurs when the context contains both the old and updated values, but the LLM still bases its answer on the old value, because the retrieved documents are not necessarily presented in the correct temporal order, again due to the retriever. 

**Multi-Hop Reasoning** For this ability, the LLM often fails when the context contains the necessary pieces of information but the model does not use them to answer the question. Another failure 

48 

Published as a conference paper at ICLR 2026 

occurs when the context is missing some components required for the multi-hop reasoning chain, making it impossible for the LLM to answer correctly. 

**Preference Following** In this ability, the LLM should incorporate user-stated preferences into its answer. Failures occur when the context does not contain the user’s preference and the model therefore answers without considering it, or when the preference is present but the LLM does not use it when generating the response. 

**Summarization** For this ability, one failure mode occurs when the context contains some components of the correct answer but the LLM fails to include them in the summary. Another failure arises when the context is missing some parts of the answer, which leads the LLM to omit those details as well. 

**Temporal Reasoning** In this ability, the LLM should reason about explicit and implicit temporal relations. A common failure mode occurs when the context contains the required dates, but the LLM becomes confused by another date (or dates) in the context and answers incorrectly. Another failure occurs when the context contains both dates but the LLM performs the arithmetic incorrectly, producing an answer with a numerical error. A third failure mode occurs when the context does not contain one of the necessary dates, causing the LLM to incorrectly substitute another date when answering. 

49 

Published as a conference paper at ICLR 2026 

## H PROMPTS 

Here we provide the prompts used in different stages of our framework. 

<!-- Start of picture text -->
This is a plan that contains detailed bullet points about a topic. This plan is used to generate realistic<br>chat conversations between a user and an AI assistant, which are then used to evaluate the long-term<br>memory capabilities of LLMs.<br>Your task is to analyze this plan and select bullet points that would be most effective for testing<br>information extraction abilities when incorporated into chat conversations.<br>Analyze this plan and identify bullet points that contain specific factual information ideal for testing<br>precise recall and information extraction capabilities.<br>## INPUT DATA<br>- **PLAN**: <plan><br>## CRITICAL REQUIREMENT: EARLY BATCH PRIORITIZATION<br>** SELECTION PRIORITY ORDER: **<br>1. **Batch 1-3 (HIGHEST PRIORITY)**: Select 70-80% of your choices from these early batches<br>2. **Batch 4-6 (MEDIUM PRIORITY)**: Select 10-20% of your choices from these middle batches<br>3. **Batch 7+ (LOW PRIORITY)**: Select only 5-10% of your choices from later batches<br>Focus on bullet points with:<br>- **Specific numbers, quantities, measurements, prices, percentages**<br>- **Proper names of people, organizations, brands, locations**<br>- **Exact dates, times, schedules, or deadlines**<br>- **Contact details such as addresses, phone numbers, email IDs**<br>- **Technical or detailed descriptions (model names, product codes, ratings, specifications)**<br>- **Distinctive events, awards, or milestones**<br>- **Direct quotes, messages, or instructions with exact wording**<br>- **Precise parameters, formulas, or datasets in technical and academic contexts**<br>- **Mathematical expressions, theorems, proofs**<br>Prioritize information that:<br>- Appears early in the timeline<br>- Contains multiple distinct factual details in one bullet point<br>- Includes uncommon names, technical terms, or culturally specific references<br>- Has precise numerical values or measurements that could be easily confused<br>- Could be misremembered if details are swapped, rounded, or reworded<br>- Requires high accuracy to preserve meaning (e.g., formulas, addresses, step-by-step processes)<br>Return your analysis in this exact JSON format:<br>[{"capability": "information_extraction", "batch_numbers": 1, "bullet_numbers": 3,<br>"bullet_points": "• **Personal Introduction:** I am Sherry Rodriguez, 34, licensed conveyancer in<br>Hollyborough, Bahrain, earning approximately $68,000 annually."}<br>]<br>Important formatting notes:<br>- The "batch_numbers" and "bullet_numbers" correspond to each other positionally<br>- "1" and "3" means: Batch 1 Bullet 3<br>Select ONLY <bullet_number> bullet points total that would generate the highest quality information extraction<br>questions.<br>NOTE: Only output the list without any explanation before or after the list.<br><!-- End of picture text -->

Listing 1: Candidate selection information extraction prompt 

<!-- Start of picture text -->
This is a plan that contains detailed bullet points about a topic. This plan is used to generate realistic<br>chat conversations between a user and an AI assistant, which are then used to evaluate the long-term<br>memory capabilities of LLMs.<br>Your task is to analyze this plan and select GROUPS of related bullet points that would be most effective for<br>testing multi-session reasoning abilities when incorporated into chat conversations.<br>Analyze this project plan and identify GROUPS of bullet points that enable testing of aggregation, comparison,<br>and synthesis across multiple batches/sessions. Each group should contain 2-6 related bullet points<br>that together enable complex multi-hop reasoning questions.<br>## INPUT DATA<br>- **PLAN**: <plan><br>## CRITICAL REQUIREMENT: EARLY BATCH PRIORITIZATION<br>** SELECTION PRIORITY ORDER: **<br>1. **Groups starting in Batches 1-3 (HIGHEST PRIORITY)**: Select 70-80% of your groups with primary content<br>from early batches<br>2. **Groups spanning early to middle batches (MEDIUM PRIORITY)**: Select 10-20% of groups that bridge early-to<br>-middle timeline<br>3. **Groups from later batches only (LOW PRIORITY)**: Select only 5-10% from purely later batches<br>Focus on bullet point groups that involve:<br>- **Aggregation opportunities**: Multiple costs that need to be summed, events that need counting,<br>measurements to be totaled<br>- **Comparison patterns**: Same categories appearing in different batches (budget changes, progress updates,<br>relationship interactions)<br>- **Evolution tracking**: How preferences, decisions, or situations change over time across multiple bullet<br>points<br>- **Cross-reference relationships**: Information that connects between different people, events, or decisions<br>across batches<br>Prioritize bullet point groups that:<br>- Are part of recurring themes across multiple batches (budget tracking, progress monitoring, relationship<br>dynamics)<br><!-- End of picture text -->

50 

Published as a conference paper at ICLR 2026 

<!-- Start of picture text -->
- Enable mathematical aggregation across multiple entries (total costs, time durations, quantity counting)<br>- Allow before/after comparisons of the same entities across different batches<br>- Require synthesis of information from 3+ different batches<br>- Create opportunities for complex multi-hop reasoning questions<br>Return your analysis in this exact JSON format where each object contains multiple related bullet points:<br>[{"capability": "multi_session_reasoning", "batch_numbers": "1, 2, 3, 5", "bullet_numbers": "10, 4, 7, 7",<br>"bullet_points": "Financial & Budget:Cost Estimation: Initial budget set at $12,500, including<br>materials and labor for decoupled framing and MLV. | Financial & Budget:Expense Tracking: Paid<br>$2,200 deposit to QuietFlow Bahrain for HVAC silencing on March 14 via bank transfer. |<br>Financial & Budget:Expense Tracking: Total spent $9,300 by April 1 on materials, labor, and<br>consultant fees. | Financial & Budget:Expense Tracking: Total project spending $12,000 as of May<br>1, within original $12,500 budget."}<br>]<br>Important formatting notes:<br>- The "batch_numbers" and "bullet_numbers" correspond to each other positionally<br>- "1, 2, 3, 5" and "10, 4, 7, 7" means: Batch 1 Bullet 10, Batch 2 Bullet 4, Batch 3 Bullet 7, Batch 5 Bullet<br>7<br>- Use comma-separated values for batch_number and bullet_number<br>- Separate multiple bullet_point entries with " | "<br>- Each group should contain 2-6 related bullet points<br>- Focus on groups that enable the most sophisticated multi-hop aggregation and comparison questions<br>Select 8-12 groups of bullet points that would enable the most sophisticated multi-session reasoning questions<br>.<br>NOTE: Only output the list without any explanation before or after the list.<br><!-- End of picture text -->

Listing 2: Candidate selection multi-hop reasoning prompt 

<!-- Start of picture text -->
This is a plan that contains detailed bullet points about a topic. This plan is used to generate realistic<br>chat conversations between a user and an AI assistant, which are then used to evaluate the long-term<br>memory capabilities of LLMs.<br>Your task is to analyze this plan and select PAIRS of related bullet points that would be most effective for<br>testing knowledge update abilities when incorporated into chat conversations.<br>Analyze this plan and identify bullet points labeled as "Information Update" and match them with their<br>corresponding original facts from earlier in the plan.<br>## INPUT DATA<br>- **PLAN**: <plan><br>## CRITICAL REQUIREMENT: SPECIAL UPDATE BULLETS WITH ORIGINAL FACTS<br>Focus on bullet points that:<br>- **Are labeled "Information Update"**: Look specifically for bullet points with this exact label<br>- **Have corresponding original facts**: Find the earlier bullet point that contains the original information<br>being updated<br>- **Show clear before/after relationships**: Original information paired with its explicit update or<br>correction<br>For each "Information Update" bullet point you find:<br>1. **Locate the original fact** in an earlier bullet point that this update refers to<br>2. **Create a pair** with the original bullet point first, then the "Information Update" bullet point second<br>3. **Ensure clear connection** between the original fact and its update<br>Look specifically for "Information Update" bullet points that contain:<br>- Clear update language ("updated," "changed," "revised," "rescheduled," "increased," "decreased")<br>- References to modifications of previously mentioned information<br>- Corrections or adjustments to earlier facts<br>- Timeline or specification changes<br>Then match each update with its original fact from earlier bullet points.<br>Return your analysis in this exact JSON format where each object contains exactly TWO related bullet points (<br>original + Information Update):<br>[{"capability": "knowledge_update", "batch_numbers": "1, 3", "bullet_numbers": "9, 31",<br>"bullet_points": "• **Financial & Budget:Cost Estimation:** Initial budget set at $12,500, including<br>materials and labor for decoupled framing and MLV. | Information Update: The initial framing<br>materials purchase included an additional 10% surplus to accommodate unexpected cuts and errors<br>."}<br>]<br>Important formatting notes:<br>- The "batch_numbers" and "bullet_numbers" correspond to each other positionally<br>- "1, 3" and "9, 31" means: Batch 1 Bullet 9 (original), Batch 3 Bullet 31 (Information Update)<br>- Each object must contain exactly 2 bullet points separated by " | "<br>- Use comma-separated values for batch_number and bullet_number<br>- First bullet point should represent the original information<br>- Second bullet point should be the "Information Update" labeled bullet<br>- Focus on pairs that enable questions like "How did the original plan change when you got the update?"<br>Select all "Information Update" bullet points and pair them with their corresponding original facts (<br>approximately 10 pairs total).<br>NOTE: Only output the list without any explanation before or after the list.<br><!-- End of picture text -->

Listing 3: Candidate selection knowledge update prompt 

<mark>This is a plan that contains detailed bullet points about a topic. This plan is used to generate realistic chat conversations between a user and an AI assistant, which are then used to evaluate the long-term memory capabilities of LLMs.</mark> 

51 

Published as a conference paper at ICLR 2026 

<mark>Your task is to analyze this plan and select PAIRS of related bullet points that would be most effective for testing temporal reasoning abilities when incorporated into chat conversations. Analyze this project plan and identify PAIRS of bullet points that enable testing duration calculations and sequence understanding between two events. Each pair should enable questions about time duration, sequence, or temporal relationships between two events. ## INPUT DATA - **PLAN**: <plan> ## CRITICAL REQUIREMENT: BALANCED BATCH DISTRIBUTION **</mark><sup><mark>SELECTIONPRIORITYORDER:</mark></sup> <mark>** 1. **Pairs starting in Batches 1-3 (MEDIUM-HIGH PRIORITY)**: Select 40-50% of your pairs with at least one bullet from early batches 2. **Far-distance pairs (HIGH PRIORITY)**: Select 30-40% of pairs that span large batch distances (e.g., Batch 1 & Batch 6, Batch 2 & Batch 8, Batch 1 & Batch 7, etc.) to test long-term temporal reasoning 3. **Pairs spanning early to middle batches (MEDIUM PRIORITY)**: Select 10-15% of pairs that bridge early-tomiddle timeline 4. **Pairs from later batches only (LOW PRIORITY)**: Select only 5-10% from purely later batches Focus on bullet point pairs that: - Enable duration calculations between two time points - Show sequence relationships between events - Allow comparison of timing across different batches - Demonstrate temporal progression or changes over time - Include scheduling, deadlines, or milestone comparisons ## EXPLICIT TIME MENTION REQUIREMENTS **</mark><sup><mark>ONLYabsolutedatescountasexplicittimementions:</mark></sup> <mark>** [Examples] **</mark><sup><mark>THESEDONOTCOUNTasexplicittimementions:</mark></sup> <mark>** - Specific times - Calendar references - Specific weekdays - Relative durations - Time periods - Vague references - Duration spans ## IMPORTANT TIME ANCHOR RULES: 1. If BOTH bullet points contain explicit absolute dates, use them as-is 2. If ONE bullet point lacks explicit absolute dates, prepend that bullet point with its batch’s Time Anchor 3. If BOTH bullet points lack explicit absolute dates, prepend both with their respective Time Anchors FORMAT EXAMPLES: Case 1 - Both have time mentions (no Time Anchor needed): [Example] Case 2 - Second bullet point lacks explicit absolute dates (add Time Anchor to second): [Example] Case 3 - Both bullet points lack explicit absolute dates (add Time Anchors to both): [Example] Return your analysis in this exact JSON format where each object contains exactly TWO related bullet points: [{"capability": "temporal_reasoning", "batch_numbers": "1, 2", "bullet_numbers": "17, 9", "bullet_points": "Bullet Description: ... | Bullet Description: ..."} ] Important formatting notes: - The "batch_numbers" and "bullet_numbers" correspond to each other positionally - "1, 2" and "17, 9" means: Batch 1 Bullet 17, Batch 2 Bullet 9 - Each object must contain exactly 2 bullet points separated by " | " - Use comma-separated values for batch_number and bullet_number - Add Time Anchors before bullet points that lack explicit time mentions - Focus on pairs that enable duration calculation questions like "How many days between X and Y?" Select 8-10 pairs of bullet points that would enable the most sophisticated temporal reasoning and duration calculation questions. NOTE: Only output the list without any explanation before or after the list.</mark> 

Listing 4: Candidate selection temporal reasoning prompt 

<mark>This is a plan that contains detailed bullet points about a topic. This plan is used to generate realistic chat conversations between a user and an AI assistant, which are then used to evaluate the long-term memory capabilities of LLMs. Your task is to analyze this plan and select bullet points that would be most effective for testing preference following abilities when incorporated into chat conversations. Analyze this plan and identify bullet points labeled as "Preference Statement" and select all. ## INPUT DATA - **PLAN**: <plan> Focus on bullet points with: - **Explicit preference statements**: "I prefer", "I like", "I choose", "I favor" - **Decision choices**: Selections between options with stated reasoning - **Personal preferences**: Style, approach, method, or format preferences - **Avoidance statements**: "I don’t like", "I avoid", "I prefer not to" - **Priority preferences**: What user values most or considers important Prioritize preferences that: - Are clearly stated with specific reasoning - Involve choices between multiple options - Contain detailed preference explanations - Include comparative preferences (X over Y) - Express strong preferences or dislikes - Relate to recurring decisions or situations NOTE: ONLY CONSIDER ’’PREFERENCE’’ NOT INSTRUCTION.</mark> 

52 

Published as a conference paper at ICLR 2026 

<!-- Start of picture text -->
Return your analysis in this exact JSON format:<br>[{"capability": "preference_following", "batch_numbers": 1,"bullet_numbers": 17,<br>"bullet_points": "**Preference Statement:** I prefer materials that balance cost and performance;<br>chose 3.5 lb/ft$ ˆ 2$ MLV despite 20% higher price."}<br>]<br>Important formatting notes:<br>- The "batch_numbers" and "bullet_numbers" correspond to each other positionally<br>- "1" and "17" means: Batch 1 Bullet 17<br>Select ONLY <bullet_number> bullet points total that would generate the highest quality preference following<br>questions.<br>NOTE: Only output the list without any explanation before or after the list.<br><!-- End of picture text -->

Listing 5: Candidate selection preference following prompt 

<!-- Start of picture text -->
This is a plan that contains detailed bullet points about a topic. This plan is used to generate realistic<br>chat conversations between a user and an AI assistant, which are then used to evaluate the long-term<br>memory capabilities of LLMs.<br>Your task is to analyze this plan and select GROUPS of related bullet points that would be most effective for<br>testing event ordering abilities when incorporated into chat conversations.<br>Event ordering tests whether the LLM can recall the chronological order in which events or topics were<br>MENTIONED in the conversation, regardless of when the actual events occurred in real life.<br>Analyze this plan and identify GROUPS of 8-12 or more related bullet points that represent the same topic/<br>theme mentioned across different batches, enabling testing of mention-order recall and conversation<br>sequence understanding.<br>## INPUT DATA<br>- **PLAN**: <plan><br>## CRITICAL REQUIREMENT: EARLY BATCH PRIORITIZATION<br>** SELECTION PRIORITY ORDER: **<br>1. **Groups starting in Batches 1-3 (HIGHEST PRIORITY)**: Select 70-80% of your groups with first mention in<br>early batches<br>2. **Groups spanning early to middle batches (MEDIUM PRIORITY)**: Select 10-20% of groups that bridge early-to<br>-middle timeline<br>3. **Groups from later batches only (LOW PRIORITY)**: Select only 5-10% from purely later batches<br>Focus on bullet point groups that show:<br>- **Same person mentioned multiple times**: Different interactions or mentions of the same person across<br>batches<br>- **Same component/process discussed repeatedly**: Multiple mentions of the same equipment, material, or<br>process<br>- **Same location/venue referenced**: Multiple mentions of the same place or address<br>- **Same decision/topic revisited**: The same subject brought up in different conversation sessions<br>- **Same problem/solution mentioned**: Multiple references to the same issue across different times<br>- **Same financial item tracked**: Multiple mentions of the same cost, budget item, or expense<br>Prioritize bullet point groups that:<br>- Contain 8-12 mentions of the same topic across different batches<br>- Enable questions about "In what order events X,Y,Z,... happen?" Or ...<br>- Allow testing of conversation chronology rather than real-world event chronology<br>- Test recall of mention sequence: "Which did I talk about first, second, third?"<br>- Focus on the order topics appeared in conversation, not when events actually happened<br>- Create opportunities to test conversational memory rather than factual timeline memory<br>Return your analysis in this exact JSON format where each object contains 3+ bullet points about the same<br>topic across different batches:<br>[{"capability": "event_ordering", "batch_numbers": "1, 3, 5, 7", "bullet_numbers": "22, 18, 11, 27",<br>"bullet_points": "• **Character & Relationship:Acoustic Consultant:** Met Rami Al-Hassan at Bahrain<br>Acoustic Expo on Feb 20; he recommended HVAC silencing at $2,200. | • **Character & Relationship<br>:Acoustic Consultant:** Rami conducted mid-project site visit April 3, advised on bass trap<br>repositioning to improve 5 dB absorption. | • **Character & Relationship:Acoustic Consultant:**<br>Rami praised progress in May 1 email; suggested minor EQ tweaks. | • **Character & Relationship:<br>Acoustic Consultant:** Rami praised final results August 20; recommended ongoing maintenance and<br>periodic EQ checks."}<br>]<br>Important formatting notes:<br>- The "batch_numbers" and "bullet_numbers" correspond to each other positionally<br>- "1, 2, 3, 5, 7" and "22, 18, 11, 27" means: Batch 1 Bullet 22, Batch 3 Bullet 18, Batch 5 Bullet 11, Batch 7<br>Bullet 27<br>- Each object must contain 8-12 related bullet points separated by " | "<br>- Use comma-separated values for batch_number and bullet_number<br>- All bullet points must reference the same topic/person/component/theme<br>- Focus on groups that enable mention-order questions<br>- Test conversational chronology, not real-world event chronology<br>Select 8-10 groups of bullet points that would enable the most sophisticated mention-order and conversation<br>sequence questions.<br>CRITICAL NOTE: DO NOT consider bulletpoint names for selecting the bullets. ONLY consider the bullets contents<br>.<br>NOTE: Only output the list without any explanation before or after the list.<br><!-- End of picture text -->

Listing 6: Candidate selection event ordering prompt 

53 

Published as a conference paper at ICLR 2026 

<mark>This is a plan that contains detailed bullet points about a topic. This plan is used to generate realistic chat conversations between a user and an AI assistant, which are then used to evaluate the long-term memory capabilities of LLMs. Your task is to analyze this plan and select PAIRS of bullet points that would be most effective for testing contradiction resolution abilities when incorporated into chat conversations. Contradiction resolution tests whether the LLM can detect and appropriately handle impossible contradictions - statements that logically cannot both be true simultaneously. Analyze this project plan and identify PAIRS of bullet points where one completely contradicts the other with impossible contradictions. Each pair should contain statements that are logically incompatible and cannot both be true. ## INPUT DATA - **PLAN**: <plan> Focus on bullet point pairs that show: - **Never-Statement Violations**: One bullet says "never" did something, another shows they did it - **Always-Statement Violations**: One bullet claims "always" pattern, another breaks that pattern - **Only-Statement Conflicts**: One bullet claims exclusivity ("only"), another contradicts it - **Impossible Reversals**: Age going backward, timeline impossibilities, logical reversals - **Dead-Alive Contradictions**: References to deceased people being active - **Mutually Exclusive States**: Being in two places simultaneously, having contradictory capabilities - **Absolute Negations**: Claiming something is impossible then showing it happened **</mark><sup><mark>TypesofImpossibleContradictionstolookfor:</mark></sup> <mark>** 1. **Never-Statement Violations**: "Never attended X" vs "Attended X event" 2. **Always-Statement Violations**: "Always lived in Y" vs "Moved from Z to Y" 3. **Only-Statement Conflicts**: "Only child" vs "Has siblings" 4. **Timeline Impossibilities**: Events happening in wrong chronological order 5. **Capability Contradictions**: "Cannot do X" vs "Successfully did X" 6. **Location Impossibilities**: Being in two places at once 7. **Relationship Contradictions**: "Never met person" vs "Long friendship with person" Prioritize bullet point pairs that: - Contain completely impossible contradictions that cannot be resolved or explained - Use absolute language ("never," "always," "only," "impossible," "cannot") - Create clear logical impossibilities rather than simple inconsistencies - Enable questions about detecting fundamental contradictions - Test whether the AI can identify when statements are mutually exclusive - Focus on contradictions that are objectively impossible, not subjective differences Return your analysis in this exact JSON format where each object contains exactly TWO contradicting bullet points: [{"capability": "contradiction_resolution", "batch_numbers": "1, 8", "bullet_numbers": "30, 29", "bullet_points": "• **Logical Contradiction:** Jeremiah has never attended any Bahrain Jazz Festival events. | • **Character & Relationship:Close Friend:** Jeremiah, 37, met at Bahrain Jazz Festival 2015, recommended an acoustic consultant."} ] Important formatting notes: - The "batch_numbers" and "bullet_numbers" correspond to each other positionally - "1, 8" and "30, 29" means: Batch 1 Bullet 30, Batch 8 Bullet 29 - Each object must contain exactly 2 bullet points separated by " | " - Use comma-separated values for batch_number and bullet_number - First bullet point can be the contradiction marker or the contradicted statement - Second bullet point should directly contradict the first with impossible logic - Focus on pairs that test detection of fundamental logical impossibilities Select <bullet_number> pairs of bullet points that demonstrate the clearest impossible contradictions for testing contradiction resolution abilities. NOTE: Only output the list without any explanation before or after the list.</mark> 

Listing 7: Candidate selection contradiction resolution prompt 

<mark>This is a plan that contains detailed bullet points about a topic. This plan is used to generate realistic chat conversations between a user and an AI assistant, which are then used to evaluate the long-term memory capabilities of LLMs. Your task is to analyze this plan and select GROUPS of bullet points that would be most effective for testing summarization abilities when incorporated into chat conversations. Summarization tests whether the LLM can synthesize and condense information from across multiple conversation sessions into coherent, comprehensive summaries. Analyze this plan and identify GROUPS of 8-12 related bullet points that represent topics suitable for summarization testing. Groups can vary in size depending on the richness and complexity of the topic. ## INPUT DATA - **PLAN**: <plan> ## CRITICAL REQUIREMENT: EARLY BATCH PRIORITIZATION **</mark><sup><mark>SELECTIONPRIORITYORDER:</mark></sup> <mark>** 1. **Groups starting in Batches 1-3 (HIGHEST PRIORITY)**: Select 60-70% of your groups with foundational content from early batches 2. **Groups spanning early to middle batches (MEDIUM PRIORITY)**: Select 20-30% of groups that bridge early-to -middle timeline 3. **Groups from later batches only (LOW PRIORITY)**: Select only 10-20% from purely later batches ## CRITICAL REQUIREMENT: CONTENT-BASED ANALYSIS **</mark><sup><mark>ANALYZEBULLETCONTENT,NOTCATEGORYNAMES:</mark></sup> <mark>** - Read the actual bullet point text to identify mentions of entities (people, places, items, topics, amounts, processes) - The same entity might appear in different category types - include mentions across all categories</mark> 

<mark>- The same process might appear in different category types - include mentions across all categories</mark> 

54 

Published as a conference paper at ICLR 2026 

- <mark>The same project might appear in different category types - include mentions across all categories</mark> 

- <mark>**</mark><sup><mark>SEARCHMETHODOLOGY:</mark></sup> <mark>** 1. **Identify key entities** in bullet content: names, places, amounts, equipment, topics, processes 2. **Search ALL batches** for any mention of these entities in ANY category 3. **Group by content similarity**, not category similarity 4. **Include 8-12 mentions** regardless of how they’re categorized Focus on complete topic clusters that enable summarization of: - **Entity or Relationship Histories**: interactions, developments, or changes related to a specific person, organization, group, or other identifiable entity across the entire plan (complete relationship or entity arc)</mark> 

- <mark>- **End-to-End Processes**: steps, stages, or phases of a specific process, workflow, or methodology from initiation to conclusion across the entire plan (no missing steps)</mark> 

- <mark>- **Resource or Asset Lifecycles**: mentions of acquisition, allocation, usage, modification, and outcomes for a specific resource, asset, or material across the entire plan</mark> 

- <mark>- **Decision and Strategy Journeys**: details of decision-making, planning, and strategy development from problem identification through implementation across the entire plan</mark> 

- <mark>- **Problem/Challenge Resolution Narratives**: instances of identifying, analyzing, addressing, and resolving a particular issue or challenge across the entire plan</mark> 

- <mark>- **Timeline-Driven Developments**: events and updates showing chronological evolution of a specific project, initiative, or topic across the entire plan</mark> 

- <mark>- **Knowledge or Skill Development Sequences**: progress updates, milestones, and learning activities related to acquiring or improving a specific skill or knowledge area across the entire plan</mark> 

- <mark>- **Discussion and Agreement Processes**: discussions, debates, negotiations, and agreements related to a specific matter across the entire plan</mark> 

- <mark>Prioritize bullet point groups that: - Contain rich, interconnected information suitable for synthesis - Enable questions like "Can you summarize my interactions with X?" or "Summarize the [X] process" - Include both factual/quantitative details and qualitative/narrative elements for well-rounded summaries - Have varying complexity levels (simple single-topic vs. complex multi-faceted stories) - Allow testing of information condensation across multiple conversation sessions - Include both factual details and narrative elements for comprehensive summarization - Create opportunities to test synthesis of scattered information into coherent narratives Return your analysis in this exact JSON format where each object contains 8-12 related bullet points: [{"capability": "summarization", "batch_numbers": "1, 1, 2, 3, 4, 5", "bullet_numbers": "5, 22, 18, 19, 23, 31", "bullet_points": "• **Character & Relationship:Close Friend:** Jeremiah, 37, met at festival, recommended consultant. | • **Conflict & Resolution:Relationship Boundaries:** Jeremiah requested exclusive studio access; agreed to 3 hours only. | • **Character & Relationship:Close Friend:** Jeremiah helped install MLV, bringing snacks from bakery. | • **Character & Relationship:Close Friend:** Jeremiah invited me to music club to test prototype. | • ** Character & Relationship:Close Friend:** Jeremiah brought dinner during late work session. | • **</mark><sup><mark>Goals&Progress:MilestoneCelebration:</mark></sup> <mark>**</mark><sup><mark>HostedlisteningpartywithJeremiah,Jon,andTonya</mark></sup> <mark>."}</mark> 

- <mark>] Important formatting notes: - The "batch_numbers" and "bullet_numbers" correspond to each other positionally - "1, 1, 2, 3, 4, 5" and "5, 22, 18, 19, 23, 31" means: Batch 1 Bullet 5, Batch 1 Bullet 22, Batch 2 Bullet 18, Batch 3 Bullet 19, Batch 4 Bullet 23, Batch 5 Bullet 31</mark> 

- <mark>- Each bullet point separated by " | " - Use comma-separated values for batch_number and bullet_number - Vary group sizes based on topic complexity and richness - Focus on groups that enable comprehensive summarization questions - Include both simple single-topic and complex multi-topic groups - **NO LIMIT on number of bullet points** - include as many as needed for complete coverage CRITICAL NOTES: - **ANALYZE BULLET CONTENT, NOT CATEGORY NAMES**: Search for mentions of entities in the actual text - **IGNORE CATEGORY LABELS**: The same entity mentioned in different category types should all be grouped together</mark> 

- <mark>- **COMPREHENSIVE ENTITY SEARCH**: For each entity/topic/process, scan ALL batches and ALL categories for any mention</mark> 

- <mark>- Include 8-12 mentions regardless of bullet point category if they reference the same entity/topic in the content</mark> 

- <mark>Select 7-9 groups of bullet points with COMPLETE mention coverage that would enable the most sophisticated and comprehensive summarization questions across different complexity levels.</mark> 

- <mark>NOTE: Only output the list without any explanation before or after the list.</mark> 

Listing 8: Candidate selection summarization prompt 

<mark>This is a plan that contains detailed bullet points about a topic. This plan is used to generate realistic chat conversations between a user and an AI assistant, which are then used to evaluate the long-term memory capabilities of LLMs. Your task is to analyze this plan and select bullet points that would be most effective for testing instruction following abilities when incorporated into chat conversations. Analyze this plan and identify bullet points that contain user instructions ideal for testing whether the LLM remembers and follows user-given instructions. ## INPUT DATA - **PLAN**: <plan> Focus on bullet points with: - **User Instruction** category/label - **Explicit instruction statements**: "Always", "Never", "When I ask about X, do Y" - **Behavioral directives**: How the AI should respond or behave</mark> 

55 

Published as a conference paper at ICLR 2026 

<mark>- **Format instructions**: Specific response formats or structures requested - **Content instructions**: What to include or exclude in responses - **Process instructions**: How to handle specific types of requests Look specifically for bullet points labeled as "User Instruction" that contain: - Clear directive language ("Always provide", "Never include", "When I ask") - Specific behavioral expectations for the AI assistant - Conditional instructions ("When I ask about X, do Y") - Response formatting requirements - Content inclusion/exclusion rules Return your analysis in this exact JSON format: [{"capability": "instruction_following", "batch_numbers": 1,"bullet_numbers": 32, "bullet_points": "User Instruction: Always provide detailed cost breakdowns when I ask about budget estimates."} ] Important formatting notes: - The "batch_numbers" and "bullet_numbers" correspond to each other positionally - "1" and "32" means: Batch 1 Bullet 32 - Include the full bullet point text as it appears in the plan - Focus specifically on "User Instruction" labeled bullet points Select all bullet points labeled as "User Instruction" from each batch (approximately 10 total). NOTE: Only output the list without any explanation before or after the list.</mark> 

Listing 9: Candidate selection instruction following prompt 

<mark>You are tasked with generating a probing question to test information extraction capabilities of LLMs. You will be given a bullet point and the corresponding multi-turn dialog between a user and assistant that incorporates this bullet point information. Your task is to create ONE question that tests whether an LLM can precisely extract and recall specific factual details from the conversation through indirect questioning that requires synthesizing multiple details from different parts of the conversation. ## INPUT DATA - **BULLET POINT**: <bullet_point> - **CONVERSATION TURNS**: <conversation_turns> ## CRITICAL REQUIREMENT: INFORMATION EXTRACTION - The question MUST NOT directly ask for the information being tested - Ask about related topics/contexts that require the LLM to synthesize multiple details from different conversation parts - Force the LLM to extract and combine information scattered across different conversation turns - Make the LLM demonstrate knowledge of facts without being directly asked for them - Require connecting and integrating information from multiple different conversation elements - Remove ALL specific details from the question that would give away the answer ## FORBIDDEN QUESTION ELEMENTS - Do NOT repeat specific names, numbers, or details being tested - Do NOT mention key characteristics or attributes being extracted - Do NOT include descriptive words that hint at the answer - Do NOT reference specific categories or types being tested - Do NOT use qualifying details that narrow down the answer ## QUESTION LANGUAGE REQUIREMENTS - Write questions as if the USER is asking them naturally - Questions MUST ONLY BE from USER language not ASSISTANT - **If testing information from USER messages**: Use first person ("I", "my", "me") in question -> Answer uses ("you", "your") - Example: "How did I decide on the location?" -> "You decided on the location because..." - **If testing information from ASSISTANT messages**: Use second person ("you", "your") in question -> Answer uses ("I", "my") - Example: "What steps did you suggest for handling this?" -> "I suggested doing..." - Avoid phrases like "according to the conversation", "based on what was discussed", "from our chat history" - Make questions sound conversational and natural - Questions should flow naturally as if continuing the conversation - Ask about context, or relationships rather than direct facts ## INDIRECT QUESTIONING STRATEGIES ### 1. **Context-Based Recall** Ask about the surrounding circumstances instead of the exact fact [Example] ### 2. **Comparison Questions** Encourage differentiation between similar elements [Example] ### 3. **Timeline Integration** Link facts to their sequence in time [Example] ### 4. **Problem-Solution Context** Frame questions around issues and how they were addressed: [Example] ### 5. **Discovery and Learning Process** Focus on the origin of knowledge or awareness [Example] ### 6. **Relationship and Connection Context** Test understanding of associations [Example] ## FORBIDDEN DIRECT QUESTIONS [Examples] ## CHAT ID TRACKING REQUIREMENT - You MUST identify which specific chat_id(s) contain the information being tested - List ALL chat_ids where the answer appears</mark> 

56 

Published as a conference paper at ICLR 2026 

- <mark>NOTE: If the answer is spread out between multiple chat_ids, group them in one list - NOTE: DO NOT INCLUDE chat_ids in the answer</mark> 

- <mark>- If answer spans multiple chats, include all relevant chat_ids - Use the exact chat_id numbers from the conversation turns</mark> 

- <mark>## DIFFICULTY LEVEL: HARD - **Hard**: Requires synthesizing multiple details from different parts of conversation - Force integration of information scattered across multiple conversation turns - Test ability to connect related facts from different conversation contexts - Require deep understanding and synthesis rather than simple recall ## OUTPUT FORMAT Return your analysis in this exact JSON format: { "question": [], "answer": [], "difficulty": "hard", "question_type": # one of: [] "conversation_reference ": "", "key_facts_tested": "",</mark> 

- <mark>"extraction_challenge": "", "source_chat_ids": [X, Y, ...]</mark> 

- <mark>} ## IMPORTANT REQUIREMENTS 1. **Indirect questioning**: Ask about context rather than direct facts 2. **Question source flexibility**: Questions can be based on information from EITHER user messages OR assistant messages</mark> 

- <mark>3. **Perspective matching**: Question perspective must match the source of information: - **User info** -> "I/my/me" question -> "you/your" answer - **Assistant info** -> "you/your" question -> "I/my" answer</mark> 

- <mark>4. **Assistant information questions**: When testing assistant advice/suggestions, use "What did you suggest/ recommend/advise..." format</mark> 

- <mark>5. **Multi-detail synthesis**: Question should require combining information from different conversation parts 6. **Cross-turn integration**: Force LLM to connect scattered information across multiple turns 7. **Complex reasoning**: Require understanding of relationships and synthesis of multiple elements 8. **Challenging extraction**: Force LLM to demonstrate knowledge through indirect demonstration Generate ONE high-quality indirect information extraction question that tests recall of specific factual details through contextual questioning requiring synthesis of multiple details from different parts of the conversation.</mark> 

- <mark>NOTE: Only output the JSON object without any explanation before or after.</mark> 

Listing 10: Information extraction probing question generation prompt 

- <mark>You are tasked with generating a probing question to test multi-session reasoning capabilities of LLMs. You will be given multiple related bullet points and the corresponding multi-turn dialogs between a user and assistant that incorporate this information across different conversation sessions.</mark> 

- <mark>Your task is to create ONE question that tests whether an LLM can perform complex multi-hop reasoning, synthesis, and analysis across 4+ conversation sessions.</mark> 

- <mark>## INPUT DATA - **BULLET POINTS**: <bullet_points> - **CONVERSATION TURNS**: <conversation_turns> ## CRITICAL REQUIREMENT: HARD MULTI-SESSION REASONING - The question MUST NOT include any explicit number, dates, times, duration, or temporal references - Focus on complex synthesis requiring multi-hop reasoning across 4+ sessions - Test sophisticated analysis that requires connecting multiple data points - Ask for complex calculations, patterns, or insights that need advanced reasoning ## QUESTION GENERATION GUIDELINES Focus on creating questions that require: - **Complex Aggregation** - **Advanced Synthesis** - **Multi-hop Reasoning**</mark> 

- <mark>- **Pattern Recognition** - **Performance Evaluation** - **Comparative Analysis** - **Predictive Reasoning** ## QUESTION TYPES TO GENERATE (HARD LEVEL) 1. **Complex Multi-hop Calculation** 2. **Performance Evaluation** 3. **Multi-variable Comparison** 4. ** Complex Evolution Analysis**</mark> 

- <mark>## REASONING COMPLEXITY LEVEL: HARD - **Hard**: Requires complex multi-hop reasoning, synthesis, and analysis across 4+ sessions - Focus on sophisticated calculations or insights requiring advanced reasoning - Test ability to identify complex patterns, correlations, or relationships - Include deep analytical thinking and synthesis of multiple data points ## QUESTION LANGUAGE REQUIREMENTS - Write questions as if the USER is asking them naturally - **If testing information from USER messages**: Use first person ("I", "my", "me") in question -> Answer uses ("you", "your")</mark> 

- <mark>- Example: "How did I decide on the location?" -> "You decided on the location because..."</mark> 

- <mark>- **If testing information from ASSISTANT messages**: Use second person ("you", "your") in question -> Answer uses ("I", "my")</mark> 

- <mark>- Example: "What steps did you suggest for handling this?" -> "I suggested doing..."</mark> 

- <mark>- Avoid phrases like "according to the conversation", "based on what was discussed", "from our chat history" - Make questions sound conversational and natural - Questions should flow naturally as if continuing the conversation ## CHAT ID TRACKING REQUIREMENT - You MUST identify which specific chat_id(s) contain the information needed for reasoning - List ALL chat_ids where relevant information appears across the reasoning chain - NOTE: If the answer is spread out between multiple chat_ids, group them in one list - NOTE: DO NOT INCLUDE chat_ids in the answer</mark> 

- <mark>If reasoning spans multiple chats, include all relevant chat_ids</mark> 

57 

Published as a conference paper at ICLR 2026 

|- Use the exact chat_id numbers from the conversation turns|
|---|
|## OUTPUT FORMAT<br>You will output exactly ONE JSON object matching this schema:<br>{|
|"question": string, "answer": string, "difficulty": "hard", "reasoning_type": [Some categories]|
|"sessions_required": integer, "conversation_references": [string,...], "reasoning_steps": [string,...], "|
|source_chat_ids": [integer,...]<br>}|
|## IMPORTANT REQUIREMENTS|
|1. **Complex multi-session dependency**: Question must require sophisticated information synthesis from 4+<br>conversation sessions|
|2. **Question source**: The question and answer to it MUST BE based on information from USER messages in|
|CONVERSATION TURNS. You MUST NOT generate questions about assistant responses or suggestions.|
|3. **User information only**: Only create questions that test details the user provided, not assistant advice|
|or recommendations.|
|5. **Advanced reasoning path**: Provide complex reasoning steps that require multi-hop thinking|
|6. **Precise answer**: Give exact answer that demonstrates complex analysis|
|7. **Session references**: Note which sessions contain relevant information|
|8. **High complexity**: Ensure question requires advanced multi-session reasoning and sophisticated synthesis|
|Generate ONE high-quality hard multi-session reasoning question.|
|NOTE: Only output the JSON object without any explanation before or after.|

Listing 11: Multi-hop reasoning probing question generation prompt 

- <mark>You are tasked with generating a probing question to test knowledge update capabilities of LLMs. You will be given two related bullet points (original information and updated information) and the corresponding multi-turn dialogs between a user and assistant that incorporate both pieces of information across different conversation sessions.</mark> 

- <mark>Your task is to create ONE question that asks about the current/updated state of information, testing whether the LLM correctly recalls the most recent version rather than outdated information.</mark> 

- <mark>## INPUT DATA - **BULLET POINTS**: <bullet_points> - **CONVERSATION TURNS**: <conversation_turns> ## CRITICAL REQUIREMENT: NO SPECIFIC CONTEXT HINTS - MUST NOT GIVE ANY INFORMATION RELATED TO OLD AND UPDATED INFORMATION/FACTS OR ANY HINTS THAT THERE IS UPDATE AT ALL</mark> 

- <mark>_ DO NOT use words like: currently, now, ... that shows update of information - The question MUST NOT include specific dates, times, locations, or detailed circumstances - Do NOT reference specific events, phases, or instances that would hint at which version to recall - Ask about the general current state, not specific occurrences ## FACTUAL UPDATE IDENTIFICATION Before creating the question: 1. Identify the EXACT fact that was updated in the "Information Update" bullet 2. Determine what the original fact was vs. the updated fact 3. Create a question that tests recall of the updated fact specifically 4. Ensure question asks for the factual detail, not procedures or implications ## QUESTION GENERATION GUIDELINES Focus on creating questions that: - **Ask about current state**: Question the most recent/updated version of information - **Test update retention**: Whether LLM remembers the latest information, not the original - **Avoid mentioning changes**: Don’t explicitly ask "how did X change" - just ask about current state - **Target updated facts**: Focus on information that was specifically updated/changed ## QUESTION TYPES TO GENERATE 1. **Current State Query** 2. **Latest Status** 3. **Updated Decision** 4. **Final Information** 5. **Recent Details**</mark> 

- <mark>## QUESTION LANGUAGE REQUIREMENTS - Write questions as if the USER is asking them naturally - **If testing information from USER messages**: Use first person ("I", "my", "me") in question -> Answer uses ("you", "your")</mark> 

- <mark>- Example: "How did I decide on the location?" -> "You decided on the location because..."</mark> 

- <mark>- **If testing information from ASSISTANT messages**: Use second person ("you", "your") in question -> Answer uses ("I", "my")</mark> 

- <mark>- Example: "What steps did you suggest for handling this?" -> "I suggested doing..."</mark> 

- <mark>- Avoid phrases like "according to the conversation", "based on what was discussed", "from our chat history" - Make questions sound conversational and natural - Questions should flow naturally as if continuing the conversation ## CHAT ID TRACKING REQUIREMENT - You MUST identify which specific chat_id(s) contain the original and updated information - List the chat_id with the original information and the chat_id with the updated information - NOTE: If the answer is spread out between multiple chat_ids, group them in one list - NOTE: DO NOT INCLUDE chat_ids in the answer - Use the exact chat_id numbers from the conversation turns ## OUTPUT FORMAT Return your analysis in this exact JSON format: { "question": "", "answer": "", "difficulty": "moderate", "update_type": "", "tests_retention_of": "", " conversation_references": "",</mark> 

- <mark>"potential_confusion": "", "source_chat_ids": {"original_info": [, ], "updated_info": [, ]}</mark> 

58 

Published as a conference paper at ICLR 2026 

|}<br>## IMPORTANT REQUIREMENTS|
|---|
|1. Do not mention how or when the value changed.Question text must not contain words like ‘‘after,’’‘‘negotiated|
|,’’‘‘updated,’’‘‘revised,’’ or any mention of a change process.|
|2. **Current state focus**: Question must ask about the updated/current information only|
|3. **No change language**: Avoid words like "changed," "updated," "revised" in the question|
|4. **Updated answer**: Answer must reflect the most recent version of the information|
|5. **Confusion potential**: Note what outdated information the LLM might incorrectly recall|
|6. **Natural phrasing**: Question should sound like asking for current facts, not testing memory updates|
|7. ‘‘Include at least **two** entries in ‘conversation_references‘: one for the original fact session and one<br>for the updated fact session.’’|
|Generate ONE knowledge update question that tests whether the LLM correctly recalls the updated information<br>rather than the original outdated version.|
|CRITICAL NOTE: Do not mention how or when the value changed.Question text must not contain words like ‘‘after,’’<br>‘‘negotiated,’’‘‘updated,’’‘‘revised,’’ or any mention of a change process.|
|NOTE: Only output the JSON object without any explanation before or after.|

Listing 12: Knowledge update probing question generation prompt 

<mark>You are tasked with generating a probing question to test temporal reasoning capabilities of LLMs. You will be given two related bullet points with temporal information and the corresponding multi-turn dialogs between a user and assistant that incorporate both time points across different conversation sessions. Your task is to create ONE question that tests whether an LLM can perform complex multi-step temporal reasoning, advanced calculations, pattern analysis, or synthesis of multiple temporal relationships. ## INPUT DATA - **BULLET POINTS**: <bullet_points> - **CONVERSATION TURNS**: <conversation_turns> ## CRITICAL REQUIREMENTS: CHALLENGING TEMPORAL REASONING - The question MUST NOT include any explicit dates, times, or temporal references - Use only event descriptions that require the LLM to recall temporal information - Create questions that require complex temporal reasoning, not simple lookups - Test sophisticated temporal understanding across multiple conversation sessions ## ADVANCED QUESTION GENERATION GUIDELINES Focus on creating questions that test: - **Complex duration calculations** - **Relative temporal positioning** - **Cross-session temporal synthesis** - **Temporal pattern recognition** - **Conditional temporal logic** - **Temporal inference** ## SOPHISTICATED QUESTION TYPES ### **Duration & Calculation Questions** 1. **Multi-hop Duration** [Other examples] ### **Sequence & Ordering Questions** 6. **Complex Sequencing** [Other examples] ### **Comparative & Analytical Questions** 10. **Timeline Comparison** [Other examples] ### **Inferential & Complex Questions** 15. **Causal Temporal** [Other examples] ### **Between-Time Information Extraction**: 21. "What/Who/Where/How much/When [specific query] between [ starting point] and [ending point]?" ## FORBIDDEN QUESTION ELEMENTS - Do NOT mention specific dates, times, or numbers in the question - Do NOT use phrases like "on [specific date]" or "after [X] days/weeks/months" [Other examples] ## GOOD VS BAD EXAMPLES [Examples] ## TEMPORAL COMPLEXITY LEVEL: HARD - **Hard**: Requires multi-step temporal reasoning across 3+ conversation sessions, complex calculations, pattern analysis, temporal inference, or synthesis of multiple temporal relationships ## QUESTION LANGUAGE REQUIREMENTS - Write questions as if the USER is asking them naturally - **If testing information from USER messages**: Use first person ("I", "my", "me") in question -> Answer uses ("you", "your") - Example: "How did I decide on the location?" -> "You decided on the location because..." - **If testing information from ASSISTANT messages**: Use second person ("you", "your") in question -> Answer uses ("I", "my") - Example: "What steps did you suggest for handling this?" -> "I suggested doing..." - Avoid phrases like "according to the conversation", "based on what was discussed" - Make questions sound conversational and natural - Questions should require deep temporal reasoning to answer ## CHAT ID TRACKING REQUIREMENT - You MUST identify which specific chat_id(s) contain the temporal information for both events - List the chat_id for the first temporal event and the chat_id for the second temporal event - NOTE: If the answer is spread out between multiple chat_ids, group them in one list - NOTE: DO NOT INCLUDE chat_ids in the answer - Use the exact chat_id numbers from the conversation turns ## OUTPUT FORMAT Return your analysis in this exact JSON format:</mark> 

59 

Published as a conference paper at ICLR 2026 

<mark>{ "question": "", "answer": "", "difficulty": "hard", "temporal_type": "", "time_points": "", " conversation_references": "", "calculation_required": "", "complexity_factors": "", "source_chat_ids": { "first_event": [12, 15], " second_event": [28, 31]} } ## IMPORTANT REQUIREMENTS 1. **No temporal hints**: Question must NOT include dates, times, or temporal references 2. **Complex reasoning**: Require multi-step temporal analysis, not simple lookup 3. **Cross-session dependency**: Events should span multiple conversation sessions 4. **Advanced difficulty**: Always use "hard" difficulty level 5. **Sophisticated types**: Use advanced question types that test complex temporal reasoning 6. **Pattern recognition**: Include questions that test temporal patterns and relationships Generate ONE high-quality, challenging temporal reasoning question that requires sophisticated temporal analysis between the provided bullet points. NOTE: Only output the JSON object without any explanation before or after.</mark> 

Listing 13: Temporal reasoning probing question generation prompt 

<!-- Start of picture text -->
You are tasked with generating multiple probing questions to test abstention capabilities of LLMs. You will be<br>given a plan containing bullet points that will be used to generate conversations between a user and AI<br>assistant.<br>Your task is to create questions that test whether an LLM can appropriately respond with "I don’t know" or "<br>Based on the provided chat, there is no information related to [topic]" when asked about information<br>that is missing or unavailable from the plan.<br>## INPUT DATA<br>- **PLAN**: <plan><br>## CRITICAL REQUIREMENT: EARLY BATCH PRIORITIZATION<br>** SELECTION PRIORITY ORDER: **<br>1. **Batch 1-3 (HIGHEST PRIORITY)**: Select 70-80% of your questions from these early batches<br>2. **Batch 4-6 (MEDIUM PRIORITY)**: Select 10-20% of your questions from these middle batches<br>3. **Batch 7+ (LOW PRIORITY)**: Select only 5-10% of your questions from later batches<br>## CRITICAL REQUIREMENT: CONTEXT-BASED HARD QUESTIONS<br>- Questions MUST be related to the plan’s context and domain<br>- Ask about plausible information that SEEMS like it should be available but isn’t<br>- Use names, places, events, and topics mentioned in the plan<br>- Ask for specific details about mentioned entities that aren’t actually provided<br>- Create questions that would be natural follow-ups but can’t be answered<br>## QUESTION GENERATION GUIDELINES<br>Focus on creating questions that test appropriate abstention for:<br>### 1. Missing Details About Mentioned People/Entities [Exmaples]<br>### 2. Unavailable Specifics About Mentioned Events/Activities [Examples]<br>### 3. Missing Information About Referenced Sources/Materials [Examples]<br>### 4. Unavailable Details About Mentioned Processes/Procedures [Examples]<br>### 5. Missing Context About Mentioned Decisions/Choices [Examples]<br>### 6. Unavailable Quantitative/Measurement Details [Examples]<br>### 7. Missing Emotional/Subjective Information [Examples]<br>### 8. Unavailable Technical/Specialized Details [Examples]<br>### 9. Unavailable Future/Predictive Information [Examples]<br>## ABSTENTION QUESTION TYPES<br>Only generate these two types: 1. **Unavailable Information Questions**: Ask about topics, people, events, or<br>details that are completely absent from the plan<br>2. **Missing Detail Questions**: Ask for specific details about topics that may be mentioned generally but<br>lack the requested specifics<br>## DIFFICULTY LEVELS<br>Generate questions of varying abstention difficulty:<br>- **Easy**: Ask for details about mentioned entities that seem like they should be available<br>- **Medium**: Ask for specific information about mentioned processes/events that weren’t detailed<br>- **Hard**: Ask for nuanced details that are plausible but not provided<br>## QUESTION LANGUAGE REQUIREMENTS<br>- Write questions as if the USER is asking them naturally<br>- **If testing information from USER messages**: Use first person ("I", my", "me") in question -> Answer uses<br>("you", "your")<br>- Example: "How did I decide on the location?" -> "You decided on the location because..."<br>- **If testing information from ASSISTANT messages**: Use second person ("you", "your") in question -> Answer<br>uses ("I", "my")<br>- Example: "What steps did you suggest for handling this?" -> "I suggested doing..."<br>- Avoid phrases like "according to the conversation", "based on what was discussed", "from our chat history"<br>- Make questions sound conversational and natural<br>- Questions should flow naturally as if continuing the conversation<br>## OUTPUT FORMAT<br>Return your analysis in this exact JSON format:<br>[{"question": "", "ideal_response": "", "difficulty": "easy", "abstention_type": "", "why_unanswerable": "",<br>"plan_reference": ""},<br>]<br>## IMPORTANT REQUIREMENTS<br>1. **Context-based questions**: Questions must relate to plan content and use mentioned entities<br>2. **Plausible but unavailable**: Ask for information that seems reasonable but isn’t provided<br><!-- End of picture text -->

60 

Published as a conference paper at ICLR 2026 

<mark>3. **Natural follow-ups**: Questions should sound like logical next questions about mentioned topics 4. **Challenging abstention**: Make it harder for LLM to recognize information is missing 5. **Domain consistency**: Questions should fit naturally within the plan’s subject matter Generate 8-15 abstention questions that test the LLM’s ability to appropriately say "Based on the provided chat, there is no information related to [topic]" when information is missing or unavailable in the plan .</mark> 

<mark>NOTE: Only output the JSON array without any explanation before or after the list.</mark> 

Listing 14: Abstention probing question generation prompt 

<mark>You are tasked with generating a probing question to test preference following capabilities of LLMs. You will be given a bullet point containing a user preference and corresponding conversation turns where this preference was mentioned. Your task is to create ONE question that tests whether an LLM remembers and respects the user’s stated preference when making recommendations or providing advice. ## INPUT DATA - **BULLET POINT**: <bullet_point> - **CONVERSATION TURNS**: <conversation_turns> ## CRITICAL REQUIREMENT: COMPLETELY NEUTRAL QUESTION - The question MUST BE COMPLETELY NEUTRAL with NO hints about any preference - The question MUST NOT contain ANY words that suggest evaluation criteria - The question should be so neutral it could test ANY type of preference in that domain - The LLM should only know about the preference from previous conversation history ## MANDATORY PREFERENCE ANALYSIS STEP BEFORE writing the question, you MUST: 1. **Extract ALL preference-related words** from the bullet point 2. **List ALL forbidden terms** including synonyms and related concepts 3. **Verify your question contains NONE of these terms** ## FORBIDDEN QUESTION ELEMENTS [Examples] ## QUESTION LANGUAGE REQUIREMENTS - Write questions as if the USER is asking them naturally - Use first person ("I", "my", "me") when referring to the user - Use second person ("you") when addressing the assistant - Avoid phrases like "according to the conversation", "based on what was discussed", "from our chat history" - Make questions sound conversational and natural - Questions should flow naturally as if continuing the conversation - NEVER mention the preference, decision criteria, or reasoning from the bullet point ## CHAT ID TRACKING REQUIREMENT - You MUST identify which specific chat_id(s) contain the preference information - List ALL chat_ids where the preference was mentioned or demonstrated - NOTE: If the answer is spread out between multiple chat_ids, group them in one list - NOTE: DO NOT INCLUDE chat_ids in the answer - Use the exact chat_id numbers from the conversation turns ## OUTPUT FORMAT Return your analysis in this exact JSON format: { "question": "", "preference_being_tested": "", "expected_compliance": "", "compliance_indicators": [], " non_compliance_signs": [], "difficulty": "medium", "preference_type": "","source_chat_ids": [] } ## IMPORTANT REQUIREMENTS 1. **Preference-triggering question**: Question must create a situation where the stated preference should guide the response 2. **Clear compliance expectations**: Define what respecting the preference looks like 3. **Measurable indicators**: Provide specific signs of following vs. ignoring the preference 4. **Natural question phrasing**: Question should sound realistic and conversational 5. **Preference relevance**: Question must relate to the same domain/context as the stated preference Generate ONE preference following question that tests whether the LLM remembers and applies the user’s stated preference when providing recommendations or advice.</mark> 

<mark>NOTE: Only output the JSON object without any explanation before or after.</mark> 

Listing 15: Preference following probing question generation prompt 

<mark>You are tasked with generating a probing question to test event ordering capabilities of LLMs. You will be given multiple related bullet points about the same topic/theme and the corresponding multi-turn dialogs between a user and assistant that incorporate these mentions across different conversation sessions. Your task is to create ONE question that tests whether an LLM can recall the chronological order in which topics were MENTIONED in the conversation, regardless of when the actual events occurred in real life. ## INPUT DATA - **BULLET POINTS**: <bullet_points> - **CONVERSATION TURNS**: <conversation_turns></mark> 

<mark>## CRITICAL REQUIREMENTS: NO SPOILERS OR TIME HINTS - The question MUST NOT list, mention, or hint at the specific events/mentions being tested</mark> 

61 

Published as a conference paper at ICLR 2026 

<mark>- The question should only specify the general topic/theme, not the individual events - Do NOT include any time references, dates, or temporal hints in the question - The LLM must recall and order the mentions entirely from memory without any hints ## ADVANCED QUESTION TYPES FOR EVENT ORDERING ### **Sequential Ordering Questions** 1. **General Mention Order** [Other types] ### **Comparative Ordering Questions** 4. **Priority Sequencing** [Other types] ### **Pattern Recognition Questions** 7. **Mention Pattern**: [Other types] ### **Analytical Ordering Questions** 10. **Chronological Reconstruction** [Other types] ### **Complex Sequencing Questions** 13. **Multi-faceted Ordering** [Other types] ## FORBIDDEN QUESTION ELEMENTS - Do NOT list specific events like "including X, Y, and Z" - Do NOT mention specific details, dates, times, or temporal references - Do NOT provide hints about what mentions to look for - Do NOT reference specific timeframes (e.g., "in February", "during spring", "early in project") - Do NOT use temporal words like "first", "then", "after", "before" in the question ## GOOD VS BAD EXAMPLES [Examples] ## ORDERING COMPLEXITY LEVEL: HARD - **Hard**: Either 8-10 mentions requiring chronological reconstruction or 8-10 mentions with complex conversational patterns or 8+ mentions requiring sophisticated sequence analysis - Focus on advanced sequence reconstruction with sophisticated analysis - Test ability to track complex mention patterns across multiple sessions - Include scenarios requiring expert-level sequence analysis and pattern recognition ## QUESTION LANGUAGE REQUIREMENTS - Write questions as if the USER is asking them naturally - Use first person ("I", "my", "me") when referring to the user - Use second person ("you") when addressing the assistant - Avoid phrases like "according to the conversation", "based on what was discussed", "from our chat history" - Make questions sound conversational and natural - Questions should flow naturally as if continuing the conversation - NEVER include temporal references or time-related words ## MANDATORY QUESTION ENDING REQUIREMENT - ALL questions MUST end with the phrase "in order" if previously didn’t mention the order - The order should mention ONLY ONCE - This signals to the LLM that a sequential, ordered response is expected ## CHAT ID TRACKING REQUIREMENT [ONLY for source_chat_ids filed in JSON object] - You MUST identify which specific chat_id(s) contain each mention in the ordering sequence - List ALL chat_ids for each mention in chronological order in source_chat_ids field - NOTE: If the answer is spread out between multiple chat_ids, group them in one list - NOTE: DO NOT INCLUDE chat_ids in the answer - Use the exact chat_id numbers from the conversation turns - Map each mention to its source chat_id ## OUTPUT FORMAT Return your analysis in this exact JSON format: { "question": "", "answer": "", "difficulty": "hard", "ordering_type": "", "total_mentions": , " conversation_references": [], "ordering_tested": [], "complexity_factors": [], "source_chat_ids": [] } ## IMPORTANT REQUIREMENTS 1. **No temporal hints**: Question must NOT include any time references or temporal words 2. **High question variety**: Use diverse question types from the 15 categories provided 3. **Complex reasoning**: Require sophisticated mention-order analysis 4. **Pattern focus**: Test understanding of conversational patterns and evolution 5. **Advanced difficulty**: Always use "hard" difficulty level 6. **General topic focus**: Ask about broad themes, not specific events 7. **Sophisticated analysis**: Test expert-level sequence reconstruction and pattern recognition Generate ONE high-quality, challenging event ordering question that tests sophisticated mention-sequence analysis without providing any hints about the specific events or timing.</mark> 

<mark>NOTE: Only output the JSON object without any explanation before or after.</mark> 

Listing 16: Event ordering probing question generation prompt 

<mark>You are tasked with generating a probing question to test contradiction resolution capabilities of LLMs. You will be given two contradictory bullet points and the corresponding multi-turn dialogs between a user and assistant that incorporate both contradictory statements across different conversation sessions. Your task is to create ONE question that asks about the contradicted topic as if seeking factual information, testing whether the LLM will detect the contradiction and ask for clarification rather than giving a definitive answer. ## INPUT DATA - **BULLET POINTS**: <bullet_points> - **CONVERSATION TURNS**: <conversation_turns> ## QUESTION GENERATION GUIDELINES Focus on creating questions that: - **Ask about the contradicted fact**: Question the topic that has contradictory information - **Sound like normal fact-seeking**: Don’t hint that there’s a contradiction - **Test contradiction detection**: Whether LLM notices conflicting information</mark> 

62 

Published as a conference paper at ICLR 2026 

<mark>- **Expect clarification request**: LLM should ask which contradictory statement is correct - **Avoid revealing the contradiction**: Question should seem like routine information request ## CRITICAL REQUIREMENT: - The question MUST be general and broad about the contradicted topic - Do NOT include specific dates, times, locations, or detailed circumstances - Do NOT reference specific events or instances that would narrow down the contradiction - Ask about the general pattern/behavior, not specific occurrences - This tests whether the LLM can detect contradictions across all related mentions ## QUESTION LANGUAGE REQUIREMENTS - Write questions as if the USER is asking them naturally - Use first person ("I", "my", "me") when referring to the user - Use second person ("you") when addressing the assistant - Avoid phrases like "according to the conversation", "based on what was discussed", "from our chat history" - Make questions sound conversational and natural - Questions should flow naturally as if continuing the conversation ## QUESTION FORMAT Generate questions that ask about the contradicted topic directly: [Examples] ## EXPECTED LLM BEHAVIOR The ideal LLM response should: [Example] ## CHAT ID TRACKING REQUIREMENT - You MUST identify which specific chat_id(s) contain each contradictory statement - List the chat_id for the first contradictory statement and the chat_id for the second contradictory statement - NOTE: If the answer is spread out between multiple chat_ids, group them in one list - NOTE: DO NOT INCLUDE chat_ids in the answer - Use the exact chat_id numbers from the conversation turns ## OUTPUT FORMAT Return your analysis in this exact JSON format: { "question": "", "ideal_answer": "", "difficulty": "", "contradiction_type": "", "topic_questioned": "", " conversation_references": [], "tests_for": "", "source_chat_ids": {"first_statement": [, ], "second_statement": [, ]} } ## IMPORTANT REQUIREMENTS 1. **Natural question phrasing**: Question should sound like normal fact-seeking, not contradiction testing 2. **Topic focus**: Ask directly about the contradicted subject 3. **Contradiction detection expectation**: LLM should notice and ask for clarification 4. **No hint giving**: Don’t reveal that there’s a contradiction in the question 5. **Clarification seeking**: Ideal response should ask which statement is correct Generate ONE contradiction resolution question that tests whether the LLM will detect the contradiction and appropriately request clarification when asked about the contradicted topic. CRITICAL NOTE: Do NOT include specific dates, times, locations, or detailed circumstances in the question that make the question easy. NOTE: Only output the JSON object without any explanation before or after.</mark> 

Listing 17: Contradiction resolution probing question generation prompt 

<mark>You are tasked with generating a probing question to test advanced summarization capabilities of LLMs. You will be given 6-8 related bullet points about the same topic/theme and the corresponding multi-turn dialogs between a user and assistant that incorporate this information across different conversation sessions. Your task is to create ONE question that tests whether an LLM can synthesize and condense complex, multifaceted information from across 4+ conversation sessions into sophisticated, comprehensive summaries. ## INPUT DATA - **BULLET POINTS**: <bullet_points> - **CONVERSATION TURNS**: <conversation_turns> ## CRITICAL REQUIREMENT: HARD SUMMARIZATION - Focus on complex information synthesis from 8-10 bullet points - Test comprehensive synthesis requiring sophisticated analysis - Require advanced narrative construction with multiple threads - Ask for summaries that demonstrate deep understanding and integration ## CRITICAL REQUIREMENT: NEUTRAL SUMMARIZATION TESTING - The question MUST NOT reveal what should be included in the summary - The question MUST mention *only* the overarching topic-no specific bullet-point details, subtopics, phases, or technical terms may appear. - The question MUST NOT hint at the structure or content of the expected answer - The question should be maximally generic, forcing the LLM to identify and synthesize all relevant information independently ## QUESTION GENERATION GUIDELINES Focus on creating questions that test: - **Complex information synthesis** - **Advanced cross-session condensation** - **Comprehensive overview** - **Sophisticated narrative coherence** - **Strategic detail prioritization** ## QUESTION TYPES TO GENERATE (HARD LEVEL) 1. **Complex Relationship & Interaction Summary** 2. **Complete Sequence & Event Analysis** 3. **Resource, Effort, & Timeline Evolution** 4. **Multi-factor Decision Process Review** 5. **Problem-to-Resolution Journey** 6. **Chronological Development Overview** 7. **Knowledge & Insight Integration Summary** 8. **Complex Negotiation or Agreement Path**</mark> 

63 

Published as a conference paper at ICLR 2026 

<mark>## SUMMARIZATION COMPLEXITY LEVEL: HARD - **Hard**: 8-10 bullet points requiring comprehensive synthesis with detailed progression - Focus on sophisticated analysis requiring understanding of complex relationships and patterns - Test ability to synthesize multiple narrative threads and extensive information - Include advanced narrative elements with multi-layered connections and sophisticated causation ## QUESTION LANGUAGE REQUIREMENTS - Write questions as if the USER is asking them naturally - Use first person ("I", "my", "me") when referring to the user - Use second person ("you") when addressing the assistant - Avoid phrases like "according to the conversation", "based on what was discussed", "from our chat history" - Make questions sound conversational and natural - Questions should flow naturally as if continuing the conversation ## CHAT ID TRACKING REQUIREMENT - You MUST identify which specific chat_id(s) contain the information needed for the summary - List ALL chat_ids where relevant summary information appears - NOTE: If the answer is spread out between multiple chat_ids, group them in one list - NOTE: DO NOT INCLUDE chat_ids in the answer - Use the exact chat_id numbers from the conversation turns ## OUTPUT FORMAT Return your analysis in this exact JSON format: { "question": "", "ideal_summary": "", "difficulty": "hard", "summarization_type": "", "bullet_points_covered": , "conversation_sessions": , "key_elements_tested": [], "synthesis_required": "", "source_chat_ids": [, , ...] } ## IMPORTANT REQUIREMENTS 1. **Comprehensive coverage**: Summary should integrate all key information from 8-10 bullet points 2. **Sophisticated coherence**: Create complex narrative with multiple threads and advanced logical structure 3. **Advanced multi-session synthesis**: Combine information from 4+ conversation sessions 4. **Strategic condensation**: Include extensive important details while maintaining sophisticated narrative structure 5. **Complex question phrasing**: Question should request comprehensive, sophisticated summaries Generate ONE advanced summarization question that tests the LLM’s ability to synthesize 8-10 bullet points into a sophisticated, comprehensive summary. NOTE: Only output the JSON object without any explanation before or after.</mark> 

Listing 18: Summarization probing question generation prompt 

<mark>This is a plan that contains detailed bullet points about a topic. This plan is used to generate realistic chat conversations between a user and an AI assistant, which are then used to evaluate the long-term memory capabilities of LLMs. Your task is to analyze this plan and select bullet points that would be most effective for testing instruction following abilities when incorporated into chat conversations. Analyze this plan and identify bullet points that contain user instructions ideal for testing whether the LLM remembers and follows user-given instructions. ## INPUT DATA - **PLAN**: <plan> Focus on bullet points with: - **User Instruction** category/label - **Explicit instruction statements**: "Always", "Never", "When I ask about X, do Y" - **Behavioral directives**: How the AI should respond or behave - **Format instructions**: Specific response formats or structures requested - **Content instructions**: What to include or exclude in responses - **Process instructions**: How to handle specific types of requests Look specifically for bullet points labeled as "User Instruction" that contain: - Clear directive language ("Always provide", "Never include", "When I ask") - Specific behavioral expectations for the AI assistant - Conditional instructions ("When I ask about X, do Y") - Response formatting requirements - Content inclusion/exclusion rules Return your analysis in this exact JSON format: [{"capability": "instruction_following", "batch_numbers": 1,"bullet_numbers": 32, "bullet_points": "User Instruction: Always provide detailed cost breakdowns when I ask about budget estimates."} ] Important formatting notes: - The "batch_numbers" and "bullet_numbers" correspond to each other positionally - "1" and "32" means: Batch 1 Bullet 32 - Include the full bullet point text as it appears in the plan - Focus specifically on "User Instruction" labeled bullet points Select all bullet points labeled as "User Instruction" from each batch (approximately 10 total). NOTE: Only output the list without any explanation before or after the list.</mark> 

Listing 19: Instruction following probing question generation prompt 

64 

Published as a conference paper at ICLR 2026 

- <mark>You are an expert evaluator tasked with judging whether the LLM’s response demonstrates compliance with the specified RUBRIC CRITERION.</mark> 

- <mark>## EVALUATION INPUTS - QUESTION (what the user asked): <question> - RUBRIC CRITERION (what to check): <rubric_item> - RESPONSE TO EVALUATE: <llm_response></mark> 

- <mark>## EVALUATION RUBRIC: The rubric defines a specific requirement, constraint, or expected behavior that the LLM response should demonstrate.</mark> 

- <mark>**</mark><sup><mark>IMPORTANT</mark></sup> <mark>**</mark><sup><mark>:Paycarefulattentiontowhethertherubricspecifies:</mark></sup> <mark>- **Positive requirements** (things the response SHOULD include/do) - **Negative constraints** (things the response SHOULD NOT include/do, often indicated by "no", "not", "avoid ", "absent")</mark> 

- <mark>## RESPONSIVENESS REQUIREMENT (anchored to the QUESTION) A compliant response must be **on-topic with respect to the QUESTION** and attempt to answer it. - If the response does not address the QUESTION, score **0.0** and stop. - For negative constraints, both must hold: (a) the response is responsive to the QUESTION, and (b) the prohibited element is absent.</mark> 

- <mark>## SEMANTIC TOLERANCE RULES: Judge by meaning, not exact wording. - Accept **paraphrases** and **synonyms** that preserve intent. - **Case/punctuation/whitespace** differences must be ignored. - **Numbers/currencies/dates** may appear in equivalent forms (e.g., ‘‘$68,000’’, ‘‘68k’’, ‘‘68,000 USD’’, or ‘‘sixty -eight thousand dollars’’). Treat them as equal when numerically equivalent.</mark> 

- <mark>- If the rubric expects a number or duration, prefer **normalized comparison** (extract and compare values) over string matching.</mark> 

- <mark>## STYLE NEUTRALITY (prevents style contamination): Ignore tone, politeness, length, and flourish unless the rubric explicitly requires a format/structure (e.g., ‘‘itemized list’’, ‘‘no citations’’, ‘‘one sentence’’).</mark> 

- <mark>- Do **not** penalize hedging, voice, or verbosity if content satisfies the rubric. - Only evaluate format when the rubric **explicitly** mandates it. ## SCORING SCALE: - **1.0 (Complete Compliance)**: Fully complies with the rubric criterion. - Positive: required element present, accurate, properly executed (allowing semantic equivalents). - Negative: prohibited element **absent** AND response is **responsive**.</mark> 

- <mark>- **0.5 (Partial Compliance)**: Partially complies. - Positive: element present but minor inaccuracies/incomplete execution. - Negative: generally responsive and mostly avoids the prohibited element but with minor/edge violations.</mark> 

- <mark>- **0.0 (No Compliance)**: Fails to comply. - Positive: required element missing or incorrect. - Negative: prohibited element present **or** response is non-responsive/evasive even if the element is absent.</mark> 

- <mark>## EVALUATION INSTRUCTIONS: 1. **Understand the Requirement**: Determine if the rubric is asking for something to be present (positive) or absent (negative/constraint).</mark> 

- <mark>2. **Parse Compound Statements**: If the rubric contains multiple elements connected by "and" or commas, evaluate whether:</mark> 

- <mark>- **All elements** must be present for full compliance (1.0) - **Some elements** present indicates partial compliance (0.5) - **No elements** present indicates no compliance (0.0)</mark> 

- <mark>3. **Check Compliance**: - For positive requirements: Look for the presence and quality of the required element - For negative constraints: Look for the absence of the prohibited element</mark> 

- <mark>4. **Assign Score**: Based on compliance with the specific rubric criterion according to the scoring scale above.</mark> 

- <mark>5. **Provide Reasoning**: Explain whether the rubric criterion was satisfied and justify the score. ## OUTPUT FORMAT: Return your evaluation in JSON format with two fields: { "score": [your score: 1.0, 0.5, or 0.0], "reason": "[detailed explanation of whether the rubric criterion was satisfied and why this justified the assigned score]"</mark> 

- <mark>} NOTE: ONLY output the json object, without any explanation before or after that</mark> 

Listing 20: Rubric scoring for nugget satisfaction prompt 

<mark>You are a binary classifier. If the TWO snippets describe the SAME event/fact, reply **YES** Otherwise reply **NO**. No extra words. DO NOT provide any explanation. First snippet: {first_paragraph}</mark> 

65 

Published as a conference paper at ICLR 2026 

<mark>Second snippet: {second_paragraph}</mark> 

### Listing 21: Fact equivalence detection prompt 

<mark>I want {chat_number} chat titles, themes, and subtopics for the category {chat_category}, in the format below: {"id": 1, "category": "Trip Planning", "title": "Designing a Year-Long Round-the-World Itinerary on a Shoestring", "theme": "Sequencing flights, overland legs, and visas across five continents in 12 months", "subtopics": ["Round-the-world tickets", "Back-to-back visa rules", "Seasonal climate mapping", "Open-jaw routing", "Long-term travel insurance", "Budget forecasting", "Digital-nomad logistics"] } NOTE: Generate the most common ones.</mark> 

Listing 22: Chat titles generation prompt 

<mark>You are a conversation framework specialist tasked with identifying the most relevant section label categories for a specific chat scenario. INPUT PARAMETERS: DOMAIN: {} TITLE: {} THEME: {} SUBTOPICS: {} CORE OBJECTIVE: Analyze the given DOMAIN, TITLE, THEME, SUBTOPICS to determine which section label categories would be most relevant and natural for this specific scenario. Generate 15-20 section label categories that best fit this particular context. LABEL CATEGORIES SELECTION: Here are some examples: **</mark><sup><mark>UNIVERSALCATEGORIES(AlwaysInclude2-3):</mark></sup> <mark>** - **Character & Relationship Labels** (relationships are always relevant) - **Personal & Emotional Labels** (human element always present) - **Decision & Change Labels** (conversations involve decisions) **</mark><sup><mark>TOPIC-SPECIFICCATEGORIES(Select9-13basedonrelevance):</mark></sup> <mark>** **</mark><sup><mark>Planning&LogisticsLabels</mark></sup> <mark>**</mark><sup><mark>-Usewhenscenarioinvolves:</mark></sup> <mark>- Travel, events, projects, moves, construction, organizing - Resource management, scheduling, coordination - Physical planning or systematic approaches [More examples] ELECTION CRITERIA: **</mark><sup><mark>MustIncludeIfRelevant:</mark></sup> <mark>** - Categories directly related to the main topic - Categories that would naturally generate diverse conversations - Categories that allow for progression and development over time - Categories that create authentic human concerns and interests **</mark><sup><mark>AvoidIncluding:</mark></sup> <mark>** - Categories that don’t naturally fit the scenario - Too many similar categories that would overlap - Categories that wouldn’t generate meaningful conversation - Generic categories that don’t add specific value OUTPUT FORMAT: Generate exactly 15-20 section label categories in this format: **</mark><sup><mark>[CategoryName]Labels:</mark></sup> <mark>** - Brief explanation of why this category is relevant to the DOMAIN/TITLE/THEME/SUBTOPICS - 3-5 specific label examples that would be used within this category Example: **</mark><sup><mark>Planning&LogisticsLabels:</mark></sup> <mark>** - Essential for travel scenarios involving coordination, scheduling, and resource management - Budget Planning, Transportation Strategy, Accommodation Research, Itinerary Adjustment, Packing Organization QUALITY STANDARDS: Each selected category must: - Be directly relevant to the specific DOMAIN, TITLE and THEME - Generate natural, varied conversation opportunities - Allow for progression and development across multiple batches - Feel authentic to what a real person would discuss in this scenario - Provide enough depth for 15-20 bullet points across the conversation - Just ouput the labels, without explanation at the first Focus on categories that would create the most natural, engaging, and realistic chat conversations for this specific scenario.</mark> 

Listing 23: Narrative generation prompt 

66 

Published as a conference paper at ICLR 2026 

<mark>You are a long-form narrative planning specialist creating a COHERENT STORY PLANSET for natural conversational flow. Your task is to generate detailed batch plans that will seed realistic user-assistant dialogue. ## INPUT DATA - **DOMAIN:** <domain> - **TITLE:** <title> - **THEME:** <theme> - **SUBTOPICS:** <subtopics> - **TIMELINE:** <timeline> - **NUM_BATCHES:** <num_batches> batches - **LABELS:** <provided_labels> - **USER PROFILE:** <user_profile> - **USER RELATIONSHIPS:** <user_relationships> =============== CORE OBJECTIVE =============== Generate <num_batches> distinct, non-repetitive batch plans that form a coherent narrative arc where a real person naturally converses with an AI assistant. Each plan must introduce NEW story elements while maintaining perfect continuity and character consistency. =============== CRITICAL DETAIL REQUIREMENTS =============== **</mark><sup><mark>MANDATORYSPECIFICDETAILS:</mark></sup> <mark>** Every batch MUST include numerous concrete details that enable factual answers: **</mark><sup><mark>RequiredDetailCategories(minimum5-7perbatch):</mark></sup> <mark>** - **Exact Numbers:** prices ($X), quantities, percentages, measurements, distances - **Specific Dates/Times:** For example: "Month x yth", "x:y PM/AM", "next [week day]", "in x weeks", ... - **Named Locations:** restaurants, stores, streets, buildings, parks, venues - **Brand/Product Names:** specific items, services, companies, tools, software - **Yes/No Situations:** decisions made, preferences stated, conflicts resolved - **Event Outcomes:** what happened, who won/lost, what was chosen/rejected - **Specific Preferences:** favorite foods, colors, activities, music, books - **Quantifiable Results:** test scores, rankings, ratings, completion times **</mark><sup><mark>DetailDistributionRules:</mark></sup> <mark>** - Each bullet must contain AT LEAST one verifiable detail - Avoid vague statements like "discussed options" - specify WHAT options - Instead of "considering choices" use "choosing between X, Y, and Z" =============== STRUCTURE REQUIREMENTS =============== **</mark><sup><mark>1.OUTPUTFORMAT:</mark></sup> <mark>** - Generate exactly <num_batches> plans - Format: ‘BATCH X PLAN‘ headers - Each plan contains exactly <num_bullets> bullets - Each bullet: "• **[LABEL CATEGORY]:[LABEL DESCRIPTION]:** [content]" (<=25 words) - NOTE: Each label consists of category and description. Use both for each bullet point. - Use only the provided LABELS - no custom categories - CRITICAL: Add one time anchor bulletpoint at the begining of each batch with this format: Month Day, Year. **</mark><sup><mark>NOTE</mark></sup> <mark>**</mark><sup><mark>:Timeanchormustcorrelatedwithotherdatesinthebatchandthetimeanchorsamongbatchesshould</mark></sup> <mark>be increasing and time anchor in each batch should be before the dates mentioned in the batches. **</mark><sup><mark>2.STORYPROGRESSIONARCHITECTURE:</mark></sup> <mark>** **</mark><sup><mark>BATCH1(StoryFoundation):</mark></sup> <mark>** - First bullet MUST be: "• **Time Anchor:**" - Second bullet MUST be: "• **Personal Introduction:**" [Must be from user language (I ...)] - MUST HAVE one bullet (titled personality trait) from personality_traits in USER PROFILE - Establish initial context with SPECIFIC details (age, location, job title, salary range) - Introduce all relationships with CONCRETE contexts (how long known, where met) - Set up measurable goals, deadlines, and quantifiable challenges **</mark><sup><mark>BATCHES2-<num_batches>(StoryEvolution):</mark></sup> <mark>** - Reference user as "I/my/me" (never repeat the full name) - Each batch advances the timeline chronologically - Build upon ALL previously established elements - Show MEASURABLE progression (promotions, relationship milestones, achievement metrics) **</mark><sup><mark>3.RELATIONSHIPCONTINUITYSYSTEM:</mark></sup> <mark>**</mark><sup><mark>[OtherdetailsifdomainisCodingorMath]</mark></sup> <mark>**</mark><sup><mark>RelationshipEvolutionMandate:</mark></sup> <mark>** Every relationship mention MUST include specific interaction details: **</mark><sup><mark>EvolutionStageswithRequiredDetails:</mark></sup> <mark>** - **Introduction:** "Met [Name] at [specific place] on [date/time]" - **Development:** "[Name] suggested [specific action] which resulted in [outcome]" - **Deepening:** "[Name] revealed [specific information] during [specific event]" - **Maturation:** "After [X months/years], [Name] and I [specific change]" **</mark><sup><mark>InteractionVariety(rotate-neverrepeatwithinbatches):</mark></sup> <mark>** - Collaborative, Supportive, Conflictual, Social, Professional, Personal, Transactional, Serendipitous **</mark><sup><mark>CharacterConsistencyRules:</mark></sup> <mark>** - Track specific preferences for each character (favorite restaurant, hobby, pet peeve) - Reference past specific events and their measurable consequences - Include 2-3 relationship bullets per batch with concrete details =============== CONFLICT & RESOLUTION TRACKING =============== **</mark><sup><mark>ConflictElements:</mark></sup> <mark>** Each batch must include situations with: - **Binary Decisions:** - **Measurable Outcomes:** - **Specific Disagreements:**</mark> 

<mark>**</mark><sup><mark>ConflictTypestoRotate:</mark></sup> <mark>**</mark> 

67 

Published as a conference paper at ICLR 2026 

<mark>- Financial decisions with specific amounts - Time management with exact deadlines - Relationship boundaries with specific incidents - Professional choices with concrete options - Personal values with specific scenarios =============== ANTI-REPETITION VERIFICATION =============== **</mark><sup><mark>BeforewritingANYbullet,verify:</mark></sup> <mark>** - Have I included at least one specific, verifiable detail? - Can this generate a question with a one-word answer? - Does this show MEASURABLE progression from previous mentions? - Are the numbers, dates, names, and locations specific? - Is this a NEW piece of information with NEW details? =============== CONTENT DISTRIBUTION STRATEGY =============== **</mark><sup><mark>PerBatchRequirements:</mark></sup> <mark>** - 2-3 bullets: Relationship developments with specific incidents - 2-4 bullets: Current situation with measurable metrics - 1 bullet: Exact temporal anchor (specific date/time) - 5-7 bullets: Events with verifiable outcomes - 3-4 bullets: Decisions/preferences with specific choices - 1 bullet: **Preference Statement**: implicitly showing user preferences - Rest: Using remaining labels with concrete details =============== SPECIAL BULLET REQUIREMENTS =============== **</mark><sup><mark>1.PREFERENCESTATEMENT(rotateeachbatch):</mark></sup> <mark>** Must show preference through action/decision **</mark><sup><mark>RotateTheseTypesEachBatch:</mark></sup> <mark>** - Choice actions - Method implementations - Quality decisions - Timing patterns - Style approaches - Priority demonstrations **</mark><sup><mark>StoryProgressionPatterns:</mark></sup> <mark>** - **Early Batches (1-3):** Establish baselines (current salary, relationship status, living situation) - **Middle Batches:** Track changes from baselines with specific metrics - **Later Batches:** Show cumulative results with before/after comparisons =============== QUALITY STANDARDS =============== **</mark><sup><mark>SpecificityChecklist:</mark></sup> <mark>** - Every person has a full name and defined relationship - Every event has a date, time, or specific temporal reference - Every location has a name or address - Every decision has concrete options with specific details - Every outcome is measurable or verifiable **</mark><sup><mark>NarrativeDepth:</mark></sup> <mark>** - Include prices, percentages, distances, durations - Show cause-and-effect with specific triggers and results - Maintain factual consistency (don’t change established numbers/dates) - Reference past specific events by name and date =============== EXECUTION NOTES =============== - Prioritize concrete details over abstract descriptions - Every bullet should enable at least 2-3 factual questions - Include cultural, financial, and geographic specificity - Ensure details are realistic and internally consistent - End immediately after ‘BATCH <num_batches> PLAN‘ Begin generation now.</mark> 

Listing 24: General domain conversation plan generation prompt 

<mark>=========== CRITICAL DETAIL REQUIREMENTS =========== **</mark><sup><mark>MANDATORYSPECIFICDETAILS:</mark></sup> <mark>** Every batch MUST include numerous concrete, verifiable technical details that enable single-word or short factual answers: **</mark><sup><mark>RequiredDetailCategories(minimum5-7perbatch):</mark></sup> <mark>** - **Exact Numbers:** version numbers (v2.3.1), port numbers (3000), response times (250ms), file sizes (2.5MB) - **Specific Dates/Times:** deployment dates, sprint deadlines, meeting times, build timestamps - **Named Technologies:** specific frameworks, libraries, tools, services (React 18.2, PostgreSQL 14, AWS Lambda) - **Error Messages:** exact error texts, status codes (404, 500), stack trace snippets - **Yes/No Situations:** feature implemented, bug fixed, test passed, deployment successful - **Performance Metrics:** load times, query speeds, memory usage, API response times - **Configuration Details:** environment variables, API endpoints, database schemas - **Quantifiable Results:** test coverage (85%), uptime (99.9%), user count (1,000+), bug count **</mark><sup><mark>DetailDistributionRules:</mark></sup> <mark>** - Each bullet must contain AT LEAST one verifiable technical detail - Avoid vague statements like "worked on feature" - specify WHAT feature and HOW - Replace "had a bug" with "encountered ’undefined is not a function’ error in UserAuth.js line 42" - Instead of "improved performance" use "reduced API response time from 800ms to 200ms" =========== STRUCTURE REQUIREMENTS =========== TECHNICAL CONTINUITY SYSTEM:** **</mark><sup><mark>DevelopmentPhaseEvolution:</mark></sup> <mark>**</mark> 

68 

Published as a conference paper at ICLR 2026 

<mark>Every technical element MUST show progression from previous batches: **</mark><sup><mark>NaturalDevelopmentProgressionExamples:</mark></sup> <mark>** - **Planning Phase:** "I need to design the authentication system..." [More examples] **</mark><sup><mark>TechnicalComplexityProgression:</mark></sup> <mark>** - Early batches: Basic implementation, simple features - Middle batches: Integration challenges, debugging complex issues - Later batches: Performance optimization, advanced features, production concerns =========== CONFLICT & RESOLUTION TRACKING =========== **</mark><sup><mark>MandatoryTechnicalConflictElements:</mark></sup> <mark>** Each batch must include at least 2-3 technical challenges with: - **Clear Stakes:** what’s at risk (deployment deadline, performance SLA, budget constraint) - **Binary Decisions:** chose Framework A over B, implemented Solution X vs Y, fixed vs workaround - **Measurable Outcomes:** reduced latency by Xms, saved $X in hosting, improved performance by X% - **Specific Trade-offs:** what was sacrificed for what gain (memory for speed, complexity for features) **</mark><sup><mark>TechnicalConflictTypestoRotate:</mark></sup> <mark>** - Performance bottlenecks with specific metrics - Architecture decisions with concrete alternatives - Integration challenges with external systems - Security vulnerabilities with severity levels - Scalability issues with user load numbers - Technical debt vs new features =========== CONTENT DISTRIBUTION STRATEGY =========== **</mark><sup><mark>PerBatchRequirements:</mark></sup> <mark>** - 2-3 bullets: Technical implementation details with specific code elements - 2-4 bullets: Current development status with measurable metrics - 1 bullet: Exact temporal anchor (specific date/time) - 5-7 bullets: Development activities with verifiable outcomes - 3-4 bullets: Technical decisions with specific alternatives considered - 1 bullet: **Preference Statement**: implicitly showing developer preferences - Rest: Using remaining labels with concrete technical details **</mark><sup><mark>AdaptiveBatchPlanning:</mark></sup> <mark>** Each batch should organically focus on what makes sense for that development phase: **</mark><sup><mark>Implementation-HeavyBatch:</mark></sup> <mark>** - Multiple implementation requests - Architecture decisions - Code structure planning - Framework/library selection [More examples] =========== NATURAL CODING CONVERSATION FLOW =========== Each bullet should represent realistic developer-AI interactions: **</mark><sup><mark>ImplementationRequests:</mark></sup> <mark>** [Examples] **</mark><sup><mark>DebuggingHelp:</mark></sup> <mark>** [Examples] **</mark><sup><mark>CodeReview/Optimization:</mark></sup> <mark>** [Examples] =========== EXECUTION NOTES =========== - Use plain, technical language throughout - Include realistic technical specificity: version numbers, error messages, configuration details - Make every bullet contribute to the overarching development story - Ensure uniform technical detail quality across ALL batches - Vary batch focus organically based on development phase (implementation vs debugging vs optimization) - Prioritize concrete technical details over abstract descriptions - Every bullet should enable at least 2-3 factual technical questions - End immediately after ‘BATCH <num_batches> PLAN‘</mark> 

Listing 25: Coding domain conversation plan generation prompt 

<mark>=========== CRITICAL DETAIL REQUIREMENTS =========== **</mark><sup><mark>MANDATORYSPECIFICDETAILS:</mark></sup> <mark>** Every batch MUST include numerous concrete, verifiable mathematical details that enable single-word or short factual answers: **</mark><sup><mark>RequiredDetailCategories(minimum5-7perbatch):</mark></sup> <mark>** - **Exact Numbers:** specific values (x = 3.14), coefficients ($2x</mark> ˆ <mark>2 + 5x - 3$), dimensions ($5\times7$ matrix ) - **Specific Problems:** complete equations ($x</mark> ˆ <mark>2 - 4x + 3 = 0$), specific integrals ($\int_0</mark> ˆ <mark>5 (2x+1)\,dx$) - **Named Concepts:** theorem names (Pythagorean Theorem), method names (Gaussian elimination), formulas ( quadratic formula) - **Calculation Results:** exact answers ($x = 4$), decimal results ($\pi \approx 3.14159$), fractions ($\ tfrac{3}{4}$) - **Yes/No Situations:** problem solved correctly, method applicable, theorem satisfied, solution exists - **Score/Grade Metrics:** test scores (85%), homework grades (18/20), quiz results (9/10 correct) - **Time/Duration:** study hours (3 hours), problem completion time (15 minutes), exam duration (2 hours) - **Mathematical Properties:** function characteristics (continuous, differentiable), matrix properties ( invertible, symmetric)</mark> 

69 

Published as a conference paper at ICLR 2026 

<mark>**</mark><sup><mark>DetailDistributionRules:</mark></sup> <mark>** - Each bullet must contain AT LEAST one verifiable mathematical detail - Avoid vague statements like "worked on problems" - specify WHICH problems and results - Replace "studied math" with "completed 5 quadratic equation problems, solved 4 correctly" - Instead of "improved understanding" use "increased quiz score from 70% to 85%" =============== STRUCTURE REQUIREMENTS =============== **</mark><sup><mark>3.MATHEMATICALCONTINUITYSYSTEM:</mark></sup> <mark>** **</mark><sup><mark>LearningPhaseEvolution:</mark></sup> <mark>** Every mathematical element MUST show progression from previous batches: **</mark><sup><mark>NaturalLearningProgressionExamples:</mark></sup> <mark>** - **Conceptual Phase:** "I need to understand what derivatives mean..." [More examples] =============== CONFLICT & RESOLUTION TRACKING =============== **</mark><sup><mark>MandatoryMathematicalConflictElements:</mark></sup> <mark>** Each batch must include at least 2-3 mathematical challenges with: - **Clear Stakes:** what’s at risk (exam grade, assignment deadline, course prerequisite) - **Binary Decisions:** chose Method A over B, applied Theorem X vs Y, used algebraic vs geometric approach - **Measurable Outcomes:** improved accuracy by X%, reduced solution time by Y minutes, raised grade from B to A - **Specific Struggles:** which step caused confusion, what concept was misunderstood, where calculation went wrong **</mark><sup><mark>MathematicalConflictTypestoRotate:</mark></sup> <mark>** - Conceptual misunderstandings with specific confusion points - Calculation errors with exact mistake locations - Method selection dilemmas with pros/cons - Time pressure challenges with specific deadlines - Prerequisite knowledge gaps with missing concepts - Application difficulties with real-world connections =============== CONTENT DISTRIBUTION STRATEGY =============== **</mark><sup><mark>PerBatchRequirements:</mark></sup> <mark>** - 2-3 bullets: Problem-solving activities with specific equations/solutions - 1-2 bullets: Current learning status with measurable metrics - 1 bullet: Exact temporal anchor (specific date/time) - 4-6 bullets: Mathematical activities with verifiable outcomes - 2-3 bullets: Learning decisions with specific alternatives considered - 1 bullet: **Preference Statement**: implicitly showing learning preferences - Rest: Using remaining labels with concrete mathematical details **</mark><sup><mark>AdaptiveBatchPlanning:</mark></sup> <mark>** Each batch should organically focus on what makes sense for that learning phase: [More examples] =============== NATURAL MATH CONVERSATION FLOW =============== Each bullet should represent realistic user-AI interactions: **</mark><sup><mark>Problem-SolvingRequests:</mark></sup> <mark>** [examples] **</mark><sup><mark>ConceptClarification:</mark></sup> <mark>** [examples] **</mark><sup><mark>SolutionVerification:</mark></sup> <mark>** [examples] **</mark><sup><mark>MethodExplanation:</mark></sup> <mark>** [examples] =============== QUALITY STANDARDS =============== **</mark><sup><mark>ChronologicalConsistency:</mark></sup> <mark>** - Batch 1 = learning beginning/foundation phase - Batch <num_batches> = evolved understanding with clear mathematical progression - Each batch logically follows the previous learning timeline **</mark><sup><mark>MathematicalAuthenticity:</mark></sup> <mark>** - Include specific mathematical details: equation types, theorem names, calculation methods [More examples] **</mark><sup><mark>UserAuthenticity:</mark></sup> <mark>** - Keep user personality consistent with provided profile [More examples] **</mark><sup><mark>LearningRealism:</mark></sup> <mark>** - Follow realistic mathematical learning patterns [More examples] **</mark><sup><mark>SpecificityChecklist:</mark></sup> <mark>** - Every equation has specific coefficients and variables [More examples] =============== EXECUTION NOTES =============== - Use plain, mathematical language throughout - Include realistic mathematical specificity: complete equations, exact values, specific theorems - Make every bullet contribute to the overarching mathematical story</mark> 

- <mark>Ensure uniform mathematical detail quality across ALL batches</mark> 

70 

Published as a conference paper at ICLR 2026 

<mark>- Vary batch focus organically based on learning phase (understanding vs solving vs applying) - Prioritize concrete mathematical details over abstract descriptions - Every bullet should enable at least 2-3 factual mathematical questions - End immediately after ‘BATCH <num_batches> PLAN‘ Begin generation now.</mark> 

Listing 26: Math domain conversation plan generation prompt 

<mark>You are a specialized editor that adds three specific test bullets to existing batch plans for synthetic conversation generation. ## INPUT & TASK - **PLAN:** <plan> - For EACH batch: Keep ALL <num_bullets> original bullets unchanged, ADD exactly 3 bullets at positions < num_bullets>+1, <num_bullets>+2, <num_bullets>+3 ## MANDATORY OUTPUT STRUCTURE Each batch MUST have EXACTLY <num_bullets>+3 bullets: - Bullets 1-<num_bullets>: Original bullets (unchanged) - Bullet <num_bullets>+1: Information Update - Bullet <num_bullets>+2: User Instruction - Bullet <num_bullets>+3: Logical Contradiction ## THE THREE SPECIAL BULLETS ### 1. INFORMATION UPDATE (Bullet <num_bullets>+1) **</mark><sup><mark>Format:</mark></sup> <mark>**</mark><sup><mark>‘•</mark></sup> <mark>**</mark><sup><mark>InformationUpdate:</mark></sup> <mark>**</mark><sup><mark>[Naturalnarrativecontainingupdate]‘</mark></sup> <mark>**</mark><sup><mark>MANDATORYPRE-CHECK:</mark></sup> <mark>** 1. SCAN bullets 1-<num_bullets>-2 for EXPLICIT numerical/measurable data 2. IDENTIFY exact number, time, date, or measurement 3. VERIFY value is clearly stated in original text 4. ONLY THEN create update changing that exact value EXAMPLES: [Some examples] **</mark><sup><mark>CRITICAL:</mark></sup> <mark>**</mark><sup><mark>MakeupdateIMPLICIT-embednewvalueinnaturalnarrative,don’tstate"XisnowY"</mark></sup> <mark>**</mark><sup><mark>UpdateCategories(rotatethroughall):</mark></sup> <mark>** 1. Numerical shifts (prices, quantities, measurements) 2. Status changes (employment, relationships, health) 3. Location changes (addresses, venues, destinations) 4. Relationship progressions (social connections) [Some other categories] **</mark><sup><mark>VERIFICATION:</mark></sup> <mark>**</mark><sup><mark>STOPifnomatchingfactexistsinbullets1-<num_bullets>-2.</mark></sup> <mark>### 2. USER INSTRUCTION (Bullet <num_bullets>+2) **</mark><sup><mark>Format:</mark></sup> <mark>**</mark><sup><mark>‘•</mark></sup> <mark>**</mark><sup><mark>UserInstruction:</mark></sup> <mark>**</mark><sup><mark>Always[action]whenIaskabout[condition]‘</mark></sup> <mark>**</mark><sup><mark>MANDATORYFORMAT:</mark></sup> <mark>**</mark><sup><mark>Mustinclude"whenIaskabout"-thismakesittestable.</mark></sup> <mark>**</mark><sup><mark>InstructionTypes(rotatethroughall):</mark></sup> <mark>** 1. Output formatting rules 2. Content restrictions 3. Personal preferences 4. Conditional responses 5. Time-based rules [Some other categories] **</mark><sup><mark>EXAMPLES:</mark></sup> <mark>** [Some examples] ### 3. LOGICAL CONTRADICTION (Bullet <num_bullets>+3) **</mark><sup><mark>Format:</mark></sup> <mark>**</mark><sup><mark>‘•</mark></sup> <mark>**</mark><sup><mark>LogicalContradiction:</mark></sup> <mark>**</mark><sup><mark>[Contradictingfactonly]‘</mark></sup> <mark>**</mark><sup><mark>CRITICALPRE-CHECK:</mark></sup> <mark>** 1. SCAN bullets 1-<num_bullets>-2 for COMPLETED ACTIONS or PERMANENT STATES: - Past tense actions: "visited", "ate", "traveled", "lived" - Permanent conditions: "born in", "raised as", "died in" - Absolute statements: "never did X", "always was Y" 2. FIND exactly ONE target fact to contradict 3. IF NO COMPLETED ACTIONS EXIST: CREATE setup bullet with completed action, insert between bullets 5-< num_bullets>-2, THEN contradict in bullet <num_bullets>+4 FORBIDDEN WORDS/PHRASES (NEVER USE): "Before this batch", "In this batch", [Other examples] **</mark><sup><mark>RULE:</mark></sup> <mark>**</mark><sup><mark>OnlycontradictCOMPLETEDACTIONS,neverplans/intentions.</mark></sup> <mark>TEMPORAL QUALIFIER PROBLEM: [Some examples] FORBIDDEN WORDS/PHRASES (NEVER USE): "Before this batch", "In this batch", "Previously", [Other examples] **</mark><sup><mark>CRITICAL:</mark></sup> <mark>**</mark><sup><mark>Contradictionmustmakethe</mark></sup> <mark>**</mark><sup><mark>sameoriginalevent/factIMPOSSIBLE</mark></sup> <mark>**</mark><sup><mark>,notdescribeadifferent</mark></sup> <mark>event with different outcomes.</mark> 

71 

Published as a conference paper at ICLR 2026 

<mark>**</mark><sup><mark>ContradictionTypes(usevariety):</mark></sup> <mark>** 1. Age/Time Reversal: Age going backward 2. Death Resurrection: Dead people doing activities 3. Never-Statement Violations: Contradicting "never" claims 4. Location Impossibilities: Being in two places simultaneously 5. Only-Statement Conflicts: Contradicting exclusivity **</mark><sup><mark>VERIFICATION:</mark></sup> <mark>** Original is COMPLETED ACTION (past tense)? Contradiction makes original IMPOSSIBLE, not just different? Reads like normal, natural statement with NO hint words? Avoided ALL forbidden words that suggest conflict? ## CRITICAL VERIFICATION STEPS **</mark><sup><mark>InformationUpdate:</mark></sup> <mark>** - Can you point to EXACT number/time/date from bullets 1-<num_bullets>-2? - Changing ONLY that specific value? **</mark><sup><mark>LogicalContradiction:</mark></sup> <mark>** - Can you point to EXACT bullet (1-<num_bullets>-2) being contradicted? - Original fact is COMPLETED ACTION, not plan? - Contradiction is IMPOSSIBLE, not just different? - NOT using FORBIDDEN WORDS/PHRASES mentioned in LOGICAL CONTRADICTION section ## COMMON ERRORS TO AVOID Don’t place special bullets anywhere except <num_bullets>+1, <num_bullets>+2, <num_bullets>+3 Don’t modify original <num_bullets> bullets Don’t skip any of the three special bullets Don’t use other labels for special bullets ## OUTPUT FORMAT Return COMPLETE plan where each batch has ALL original bullets unchanged + exactly 3 additional bullets at the end. When setup fact is created, insert between bullets 5-<num_bullets>-2, renumber, and add special bullets as <num_bullets>+2, <num_bullets>+3, <num_bullets>+4. Begin processing the plan now.</mark> 

Listing 27: Adding special bulletpoints to conversation plan prompt 

<mark>You are a narrative coherence specialist creating CHRONOLOGICALLY SEQUENCED topic clusters for realistic conversational AI dataset generation. Your task is to generate 10 interconnected topics that form a natural life progression. ## INPUT DATA - **SEED TOPIC**: <seed_topic> - **SEED THEME**: <seed_theme> - **SEED SUBTOPICS**: <seed_subtopics> - **USER PROFILE**: <user_profile> - **TIMELINE**: <timeline> ## CORE OBJECTIVE Generate a JSON object containing 10 topics (including the provided seed topic as Topic 0) that form a CHRONOLOGICALLY COHERENT narrative where each topic naturally follows the previous one in realistic time progression. ## CRITICAL REQUIREMENTS ### 1. CHRONOLOGICAL COHERENCE & TOPIC INDEPENDENCE **</mark><sup><mark>TOPICPROGRESSIONRULES:</mark></sup> <mark>** - **Topic 0**: Use the provided seed topic EXACTLY as given - **Topics 1-9**: Each must be a COMPLETELY DIFFERENT life domain/category - **NO EXTENDED NARRATIVES**: Topics 1-9 should NOT continue the seed topic’s story - **LIFE PROGRESSION**: Each topic represents what naturally happens AFTER completing the previous life experience **</mark><sup><mark>TOPICINDEPENDENCEMANDATE:</mark></sup> <mark>** - Each topic must address a DIFFERENT life area (career, relationships, health, education, finances, etc.) - Topics should show how one life experience leads to growth in OTHER areas - NO topic should be "Part 2" of a previous topic ### 2. NATURAL LIFE FLOW REQUIREMENTS **</mark><sup><mark>CAUSALRELATIONSHIPSWITHOUTCONTINUATION:</mark></sup> <mark>** - Topic N+1 is INFLUENCED BY Topic N but addresses a DIFFERENT life domain - Show how growth in one area catalyzes change in another area - Example: Travel experience (Topic 0) -> Career reassessment (Topic 1) -> Relationship priorities (Topic 2) [Examples] ### 3. USER PROFILE ALIGNMENT - **Demographic Consistency**: All topics must align with user’s age, education, career level, and life stage - **Financial Realism**: Topics must reflect user’s actual financial capacity and constraints - **Geographic Logic**: Topics must consider user’s location and mobility constraints - **Value Alignment**: Topics must reflect user’s stated priorities, interests, and life goals ### 4. TOPIC BREADTH REQUIREMENTS Each topic must include a realistic timeline that: - **Sequential Timing**: Topics must not overlap and should follow logical temporal progression - **Duration Realism**: Each topic should span 1-2 months for authentic decision-making and implementation - **Natural Gaps**: Include realistic time gaps between major life transitions - **Seasonal Considerations**: Account for natural timing (job searches, moving seasons, academic calendars) - **Timeline Format**: Use "Month X, Year Y - Month X’, Year Y’" format</mark> 

<mark>Each topic must be sufficiently BROAD to generate 2000+ authentic conversations by including:</mark> 

72 

Published as a conference paper at ICLR 2026 

<mark>- **Multiple Decision Points**: 15-20 major decisions per topic - **Complex Subtopics**: 9-10 substantial subtopics that each require extensive discussion - **Ongoing Processes**: Topics involving multi-month planning, execution, and adjustment phases - **Cross-Domain Impact**: Topics affecting multiple life areas ### 5. NARRATIVE REALISM - **Natural Timing**: Realistic time gaps between major life decisions - **Emotional Progression**: Topics should reflect natural emotional and psychological development - **Practical Constraints**: Topics must acknowledge real-world limitations (money, time, responsibilities) ## OUTPUT FORMAT REQUIREMENTS Generate a single JSON object with this EXACT structure: ‘‘‘json {"topics": [{"id": 0,"category": "[Provided Category]","title": "[Provided Title]", "theme": "[Provided Theme ]","subtopics": [/* Provided Subtopics Array */],"timeline": "[Start Month, Year - End Month, Year]"}, {"id": 1,"category": "[New Category]","title": "[Descriptive Title]","theme": "[Character-focused theme describing the challenge/opportunity]", "subtopics": ["[Subtopic 1]", "[Subtopic 2]", "[Subtopic 3]", "[Subtopic 4]", "[Subtopic 5]", "[Subtopic 6]", "[Subtopic 7]", "[Subtopic 8]", "[Subtopic 9]", "[Subtopic 10]"],"timeline": "[Start Month, Year - End Month, Year]"}, // ... topics 2-9 following same structure]} ‘‘‘ ## CRITICAL TIMELINE REQUIREMENTS ### MANDATORY NON-OVERLAPPING TIMELINE RULES **</mark><sup><mark>ABSOLUTERULE</mark></sup> <mark>**</mark><sup><mark>:Eachtopic’stimelineMUSTstartATLEASTonemonthAFTERtheprevioustopicends.</mark></sup> <mark>**</mark><sup><mark>TIMELINECALCULATIONPROTOCOL:</mark></sup> <mark>** 1. Topic 0: Uses provided timeline exactly 2. Topic N+1 start = Topic N end + AT LEAST 1 month gap 3. NO overlapping months between any topics 4. Each topic duration: 1-2 months [Examples] **</mark><sup><mark>TIMELINEVERIFICATIONSTEPS:</mark></sup> <mark>** Before finalizing each topic: 1. Identify previous topic’s END month 2. Add AT LEAST 1 month to get earliest possible START 3. Verify NO month appears in multiple topics 4. Confirm realistic gaps for life transitions **</mark><sup><mark>GAPJUSTIFICATION:</mark></sup> <mark>** The 1+ month gaps represent: - Processing and integration time after major experiences - Natural life rhythms and decision-making periods - Realistic pacing of significant life changes - Time for consequences of previous decisions to manifest ## TOPIC PROGRESSION GUIDELINES ### Phase 1: Post-Seed Topic Reality (Topics 1-2) - **Topic 1**: How the seed topic experience changes perspective on ANOTHER life area - **Topic 2**: Ripple effects creating needs in YET ANOTHER domain ### Phase 2: Multi-Domain Growth (Topics 3-5) - **Topics 3-5**: Leveraging cumulative growth to address diverse life challenges ### Phase 3: Integration Across Life (Topics 6-8) - **Topics 6-8**: Synthesizing learnings to optimize different life areas ### Phase 4: Holistic Vision (Topic 9) - **Topic 9**: Long-term life design incorporating all previous growth **</mark><sup><mark>CRITICALQUESTIONFOREACHTOPIC:</mark></sup> <mark>** "After completing [previous topic], what DIFFERENT area of life would this person naturally need to address next?" ## QUALITY VALIDATION CHECKLIST [Examples] ## EXAMPLE PROGRESSION LOGIC [Example] ## FORBIDDEN ELEMENTS - **Non-sequential topics**: Topics that could happen in any order - **Profile contradictions**: Topics that contradict user’s established circumstances - **Unrealistic jumps**: Major life changes without proper foundation/motivation - **Narrow topics**: Topics that couldn’t generate extensive conversation - **Template responses**: Generic topics that don’t reflect unique user circumstances ## EXECUTION NOTES - Generate all 10 topics in a single coherent response - Ensure seamless narrative flow from Topic 0 through Topic 9 - Prioritize realism and character consistency over dramatic storylines - Focus on authentic life progressions that real people experience - End output immediately after closing the JSON structure **</mark><sup><mark>CRITICAL</mark></sup> <mark>**</mark><sup><mark>:OutputyourresponseinJSONformatonly.Donotincludeanyexplanatorytext,markdown</mark></sup> <mark>formatting, or additional commentary. Provide only the raw JSON object. Generate the complete topic cluster now.</mark> 

Listing 28: Ten million sequential seed generation prompt 

73 

Published as a conference paper at ICLR 2026 

<!-- Start of picture text -->
You are creating a CHRONOLOGICAL SUBTOPIC FRAMEWORK that breaks down a main topic into 10 diverse, non-<br>repetitive phases with strict timeline boundaries.<br>## INPUT DATA<br>- **MAIN TOPIC:** <main_topic><br>- **MAIN THEME:** <main_theme><br>- **MAIN SUBTOPICS:** <main_subtopics><br>- **USER PROFILE:** <user_profile><br>- **TOTAL TIMELINE:** <total_timeline><br>## TIMELINE EXTRACTION (MANDATORY FIRST)<br>1. **Extract Core Action**:<br>- Duration from main topic (e.g., "x-day doing Y" = x days)<br>- Action type (trip/project/course/challenge/etc.)<br>- Total timeline span in months<br>2. **Calculate Key Dates**:<br>- MAIN_ACTION_START: When core action begins<br>- MAIN_ACTION_END: When core action ends<br>- Allocate realistic prep/integration time around core action<br>## SUBTOPIC GENERATION RULES<br>### Phase Distribution (10 Topics)<br>- **Topics 0-2**: PREPARATION (before action starts)<br>- **Topics 3-6**: CORE ACTION (during main action period)<br>- **Topics 7-9**: INTEGRATION (after action ends)<br>### MANDATORY DIVERSITY REQUIREMENTS<br>** EACH SUBTOPIC MUST BE UNIQUE: **<br>- No recycling of themes between subtopics<br>- Each explores DIFFERENT aspects/challenges<br>- Progressive complexity within each phase<br>- Distinct focus areas that don’t overlap<br>** PREPARATION DIVERSITY (Topics 0-2): **<br>- Topic 0: Discovery/Research/Initial Planning<br>- Topic 1: Decision-Making/Resource Gathering/Skill Building<br>- Topic 2: Final Preparations/Confirmations/Pre-Launch<br>** CORE ACTION DIVERSITY (Topics 3-6): **<br>- Topic 3: Launch/Beginning/Initial Experiences<br>- Topic 4: Early Challenges/Adaptations/Progress<br>- Topic 5: Peak Performance/Deep Engagement/Mastery<br>- Topic 6: Final Push/Completion/Transition<br>** INTEGRATION DIVERSITY (Topics 7-9): **<br>- Topic 7: Immediate Reflection/Initial Processing<br>- Topic 8: Application/Transformation/Sharing<br>- Topic 9: Long-term Impact/Future Planning/Legacy<br>### Required Structure Per Subtopic<br>‘‘‘json {"id": [0-9],"category": "[Phase name]","title": "[Unique descriptive title - NO REPETITION]","theme":<br>"[Distinct challenge/opportunity - MUST BE DIFFERENT]","subtopics": ["10 DIVERSE sub-elements - NO<br>OVERLAP with other topics"],"timeline": "[Date range]","phase_type": "[preparation/core_action/<br>integration]",<br>"action_dates": {"main_action_type": "[type]","main_action_starts": "[date]","main_action_ends": "[date]","<br>main_action_duration": "[duration]","current_phase_relation": "[before/during/after]"},<br>"phase_boundaries": {"can_mention": ["Allowed activities"],"cannot_mention": ["Forbidden activities"],"<br>tense_for_main_action": "[future/present/past]"},<br>"key_milestones": ["3 unique milestones"],"future_references": ["Setup for continuity"],"continuity_hooks":<br>["Links to next topic"]}<br>DIVERSITY ENFORCEMENT CHECKLIST<br>[Examples]<br>MAIN SUBTOPIC DISTRIBUTION<br>Spread the provided main_subtopics across topics you generate strategically:<br>Show evolution: basic -> intermediate -> advanced -> mastery<br>Different angles in each phase (planning vs doing vs reflecting)<br>OUTPUT FORMAT<br>Generate ONLY this JSON structure:<br>json{"main_topic": "[Input]","main_theme": "[Input]","main_subtopics": ["Input array"],"total_timeline": "[<br>Input]",<br>"master_timeline": {"timeline_start": "[Date]","timeline_end": "[Date]","main_action_starts": "[Date]","<br>main_action_ends": "[Date]","main_action_duration": "[Duration]",<br>"preparation_phase": {"start": "[Date]","end": "[Date]","topics": [0, 1, 2]},<br>"core_action_phase": {"start": "[Date]","end": "[Date]","duration": "[Duration]","topics": [3, 4, 5, 6]},<br>"integration_phase": {"start": "[Date]","end": "[Date]","topics": [7, 8, 9]},<br>"subtopics": [/* 10 UNIQUE subtopic objects */]}<br>CRITICAL:<br>Each subtopic explores DIFFERENT aspects<br>NO thematic repetition across topics<br>Progressive narrative arc<br>Diverse conversation opportunities<br>Output ONLY the JSON. No explanations<br><!-- End of picture text -->

Listing 29: Ten million hierarchical seed generation prompt 

74 

Published as a conference paper at ICLR 2026 

- <mark>You are a long-form narrative planning specialist creating a COHERENT STORY PLANSET for natural conversational flow. Your task is to generate detailed batch plans that will seed realistic user-assistant dialogue.</mark> 

- <mark>## INPUT DATA - **DOMAIN:** <domain> - **TITLE:** <title> - **THEME:** <theme> - **SUBTOPICS:** <subtopics> - **TIMELINE:** <timeline> - **NUM_BATCHES:** <num_batches> batches - **LABELS:** <provided_labels> - **USER PROFILE:** <user_profile> - **CORE RELATIONSHIPS:** <core_relationships> - **NEW RELATIONSHIPS:** <new_relationships> - **PREVIOUS PLAN:** <previous_plan> - **INCLUDE_INTRODUCTION:** <YES/NO> =============== CORE OBJECTIVE =============== Generate <num_batches> distinct, non-repetitive batch plans that form a coherent narrative arc where a real person naturally converses with an AI assistant. Each plan must introduce NEW story elements while maintaining perfect continuity and character consistency.</mark> 

- <mark>=============== CRITICAL NARRATIVE PERSPECTIVE =============== **</mark><sup><mark>MANDATORYFIRST-PERSONPERSPECTIVE:</mark></sup> <mark>**</mark><sup><mark>-ALLcontentmustbewrittenfromtheUSER’sperspective(first-</mark></sup> <mark>person)</mark> 

- <mark>- Use first-person perspective throughout but VARY sentence structures - Natural narrative flow - avoid starting every bullet with "I"</mark> 

- <mark>- Mix active and passive voice while maintaining first-person perspective =============== CONTINUITY REQUIREMENTS =============== **</mark><sup><mark>CRITICAL</mark></sup> <mark>**</mark><sup><mark>:IfPREVIOUSPLANisprovided,youMUST:</mark></sup> <mark>- **Reference Previous Events** **Maintain Core Character Consistency** **Integrate New Relationships** **Show Temporal Progression**</mark> 

- <mark>**</mark><sup><mark>BuildUponPreviousDecisions</mark></sup> <mark>** **</mark><sup><mark>PreserveEstablishedFacts</mark></sup> <mark>** **</mark><sup><mark>ContinueRelationshipArcs</mark></sup> <mark>** =============== STRICT TIMELINE ENFORCEMENT =============== **</mark><sup><mark>CRITICALTIMELINEPARSING(MANDATORYFIRSTSTEP):</mark></sup> <mark>** Before generating ANY content, you MUST internally calculate timeline boundaries. **</mark><sup><mark>STEP1:ExtractandWriteTimelineBoundaries</mark></sup> <mark>** **</mark><sup><mark>CALCULATEYOURPARSEDDATES:</mark></sup> <mark>** **</mark><sup><mark>STEP2:CreateBatchDateAssignments</mark></sup> <mark>** Divide timeline into <num_batches> segments: Days per batch = TOTAL DAYS / <num_batches> **</mark><sup><mark>ABSOLUTETIMELINERULES:</mark></sup> <mark>**</mark><sup><mark>1.</mark></sup> <mark>**</mark><sup><mark>EVERYdatementionedMUSTbebetweenSTARTandENDdates</mark></sup> <mark>**</mark><sup><mark>2.</mark></sup> <mark>**</mark><sup><mark>NOfuture</mark></sup> <mark>references beyond TIMELINE END** (no "next month" if timeline ends this month)</mark> 

- <mark>3. **NO past references before TIMELINE START** 4. **Temporal anchors MUST progress chronologically within boundaries** 5. **Final batch MUST conclude naturally before or on END DATE**</mark> 

- <mark>**</mark><sup><mark>TEMPORALANCHORREQUIREMENTS:</mark></sup> <mark>** - First bullet of EACH batch MUST be temporal anchor - Format: "• **Temporal Anchor:** [Month] [Day], [year], [event description]" - Each temporal anchor date MUST be within that batch’s assigned date range - Dates must progress: Batch 2’s date > Batch 1’s date, etc. **</mark><sup><mark>TIMELINEVIOLATIONEXAMPLES(FORBIDDEN):</mark></sup> <mark>** [Examples] **</mark><sup><mark>PRE-GENERATIONCHECKLIST:</mark></sup> <mark>** [Examples] =============== CRITICAL DETAIL REQUIREMENTS =============== **</mark><sup><mark>MANDATORYSPECIFICDETAILS:</mark></sup> <mark>** Every batch MUST include numerous concrete, verifiable details that enable single-word or short factual answers:</mark> 

- <mark>**</mark><sup><mark>RequiredDetailCategories(minimum5-7perbatch):</mark></sup> <mark>** - **Exact Numbers:** prices ($X), quantities, percentages, measurements, distances [Some categories examples] **</mark><sup><mark>DetailDistributionRules:</mark></sup> <mark>** - Each bullet must contain AT LEAST one verifiable detail - Avoid vague statements =============== STRUCTURE REQUIREMENTS =============== **</mark><sup><mark>1.OUTPUTFORMAT:</mark></sup> <mark>** - Generate exactly <num_batches> plans - Format: ‘BATCH X PLAN‘ headers - Each plan contains exactly 30 bullets - Each bullet: "• **[LABEL CATEGORY]:[LABEL DESCRIPTION]:** [content]" (<=25 words) - NOTE: Each label consists of category and description. Use both for each bullet point. - Use only the provided LABELS - no custom categories - **MANDATORY**: First bullet MUST be Temporal Anchor with the ONLY date reference in the batch **</mark><sup><mark>2.STORYPROGRESSIONARCHITECTURE:</mark></sup> <mark>** **</mark><sup><mark>IFINCLUDE_INTRODUCTION=YES:</mark></sup> <mark>** **</mark><sup><mark>BATCH1(StoryFoundation):</mark></sup> <mark>** - First bullet MUST be: "• **Personal Introduction:**" Establish initial context with SPECIFIC details Introduce all relationships with CONCRETE contexts Set up measurable goals, deadlines, and quantifiable challenges</mark> 

<mark>**</mark><sup><mark>IFINCLUDE_INTRODUCTION=NO:</mark></sup> <mark>**</mark> 

75 

Published as a conference paper at ICLR 2026 

<!-- Start of picture text -->
** BATCH 1 (Continuation): ** NO personal introduction bullets Begin directly with current topic-related content<br>Reference established character details from PREVIOUS PLAN<br>** BATCHES 2-<num_batches> (Story Evolution): **<br>- Reference user as "I/my/me" (never repeat the full name) Each batch advances the timeline chronologically<br>Build upon ALL previously established elements<br>Show MEASURABLE progression (promotions, relationship milestones, achievement metrics)<br>** 3. RELATIONSHIP CONTINUITY SYSTEM: **<br>** Core vs. New Relationship Management: **<br>- **CORE RELATIONSHIPS**: Must remain consistent across all plans - same names, established details, ongoing<br>dynamics<br>- **NEW RELATIONSHIPS**: Introduce naturally based on current topic and life phase **Relationship Integration<br>**<br>** Relationship Evolution Mandate: **<br>Every relationship mention MUST include specific interaction details:<br>** Evolution Stages with Required Details: **<br>[Examples]<br>=============== CONFLICT & RESOLUTION TRACKING ===============<br>** Mandatory Conflict Elements: **<br>Each batch must include at least 2-3 situations with:<br>- **Clear Stakes:** what’s at risk (money amount, deadline, relationship status)<br>[Examples]<br>** Conflict Types to Rotate: ** Financial decisions with specific amounts Time management with exact deadlines<br>Relationship boundaries with specific incidents<br>Professional choices with concrete options Personal values with specific scenarios<br>=============== ANTI-REPETITION VERIFICATION ===============<br>[Examples]<br>=============== CONTENT DISTRIBUTION STRATEGY ===============<br>** Per Batch Requirements: **<br>- 2-3 bullets: Relationship developments with specific incidents (mix of core and new relationships)<br>- 2-4 bullets: Current situation with measurable metrics<br>- 1 bullet: Exact temporal anchor (specific date/time)<br>- 5-7 bullets: Events with verifiable outcomes<br>- 3-4 bullets: Decisions/preferences with specific choices<br>- Rest: Using remaining labels with concrete details<br>** Story Progression Patterns: **<br>- **Early Batches (1-3):** Establish baselines (current salary, relationship status, living situation) **<br>Middle Batches:** Track changes from baselines with specific metrics<br>** Later Batches: ** Show cumulative results with before/after comparisons<br>=============== NATURAL CONVERSATION FLOW ===============<br>These plans generate conversations where users seek AI assistance for SPECIFIC situations:<br>[Example]<br>=============== QUALITY STANDARDS ===============<br>** Specificity Checklist: **<br>- Every person has a full name and defined relationship<br>[Other exmaples]<br>** Narrative Depth: **<br>- Include prices, percentages, distances, durations<br>- Show cause-and-effect with specific triggers and results<br>- Maintain factual consistency (don’t change established numbers/dates)<br>- Reference past specific events by name and date<br>=============== EXECUTION NOTES ===============<br>- Prioritize concrete details over abstract descriptions<br>- Every bullet should enable at least 2-3 factual questions<br>- Include cultural, financial, and geographic specificity<br>- Ensure details are realistic and internally consistent<br>- If PREVIOUS PLAN provided, include 3-5 specific references to previous events per batch<br>- End immediately after ‘BATCH <num_batches> PLAN‘<br>** FINAL TIMELINE REMINDER: **<br>- Parse TIMELINE boundaries FIRST<br>- EVERY date must fall within those boundaries<br>- NO exceptions to timeline limits<br>- Verify each batch respects the timeline<br>Output ONLY the batch plans. No explanations or additional text.<br>Begin generation now.<br><!-- End of picture text -->

Listing 30: Ten million sequential conversation plan generation prompt 

<mark>You are a precision narrative architect generating TEMPORALLY COHERENT BATCH PLANS with absolute timeline integrity and phase-appropriate content. ## INPUTS MAIN_TITLE:<main_title> | MAIN_THEME:<main_theme> | TITLE:<title> | THEME:<theme> | TIMELINE:<timeline> | NUM_BATCHES:<num_batches> | LABELS:<provided_labels> | USER_PROFILE:<user_profile> | CORE_RELATIONSHIPS :<core_relationships> | NEW_RELATIONSHIPS:<new_relationships> | ALL_SUBTOPIC_PLANS:<all_subtopic_plans> | PREVIOUS_PLANS_SUMMARY:<previous_plans_summary> | PREVIOUS_PLAN:<previous_plan> |</mark> 

76 

Published as a conference paper at ICLR 2026 

<mark>CURRENT_SUBTOPIC_DATA:<current_subtopic_data> | CURRENT_SUBTOPIC_ID:<current_subtopic_id> | INCLUDE_INTRODUCTION:<YES/NO> ## OBJECTIVE Generate <num_batches> distinct, non-repetitive batch plans forming coherent narrative where user naturally converses with AI. Each plan introduces NEW elements while maintaining continuity. ## STRUCTURE [MANDATORY] - Format: ‘BATCH X PLAN‘ headers - Exactly 30 bullets per batch - Bullet format: "**[LABEL CATEGORY]:[LABEL DESCRIPTION]:** [content]" (<=30 words) - First bullet ALWAYS: "• **Temporal Anchor:** [Date], [context]" - NO other dates in batch except temporal anchor</mark> 

- <mark>ALL content in FIRST-PERSON ("I/my/me")</mark> 

- <mark>Vary sentence structures, avoid starting every bullet with "I"</mark> 

<mark>## DETAIL REQUIREMENTS [8-10 per batch minimum] - Exact Numbers: prices($X), quantities, percentages, measurements - Specific Dates/Times: "Month x yth", "x:y PM/AM" [Some other examples] Replace vague with specific: [Examples] ## FACT TRACKING SYSTEM [MAINTAIN THROUGHOUT] Track per batch: 1. Purchases: [Item, Price, Store, Date] [Examples] Before EVERY bullet: - Check if fact exists in registry If similar exists, ADD NEW DIMENSION (consequence/complication/perspective/ progression) ## PROGRESSION PATTERNS **</mark><sup><mark>Batches1-3:</mark></sup> <mark>**</mark><sup><mark>Establishbaselines,initialdecisions,relationshipintros</mark></sup> <mark>**</mark><sup><mark>Batches4-6:</mark></sup> <mark>**</mark><sup><mark>Show</mark></sup> <mark>consequences, complications, deepen relationships **</mark><sup><mark>Batches7-8:</mark></sup> <mark>**</mark><sup><mark>Unexpecteddevelopments,secondaryeffects,evolution</mark></sup> <mark>**</mark><sup><mark>Batches9-10:</mark></sup> <mark>**</mark><sup><mark>Long-termimpacts,</mark></sup> <mark>synthesis, maturity, future implications Recurring element progression: 1. First: Basic establishment 2. Second: Add complication 3. Third: Show resolution 4. Fourth: Reveal impact 5. Fifth+: FORBIDDEN unless dramatic change ## LABEL ROTATION RULES Track usage: Label+Focus combination FORBIDDEN across all batches [Examples] ## RELATIONSHIP RULES **</mark><sup><mark>IFINCLUDE_INTRODUCTION=YES:</mark></sup> <mark>**</mark><sup><mark>Batch1firstbullet:"•</mark></sup> <mark>**</mark><sup><mark>PersonalIntroduction:</mark></sup> <mark>**</mark><sup><mark>"Establishcontextwith</mark></sup> <mark>SPECIFICS (age, location, job, salary) Introduce relationships with context (how long known, where met) **</mark><sup><mark>NEW_RELATIONSHIPSfirstappearance:</mark></sup> <mark>**</mark><sup><mark>Includerelationshiptouser+age+contextAfterintroduction,refer</mark></sup> <mark>naturally Every relationship mention needs specific interaction: Introduction Development Deepening Maturation ## BATCH REQUIREMENTS - 1 temporal anchor (specific date) - 2-3 relationship developments - 3-4 current situation with metrics - 5-6 events with outcomes - 4-5 decisions with choices - Rest: remaining labels with details ## ANTI-REPETITION PROTOCOL **</mark><sup><mark>THREE-PASSREVIEW:</mark></sup> <mark>**</mark><sup><mark>1.</mark></sup> <mark>**</mark><sup><mark>FactUniqueness:</mark></sup> <mark>**</mark><sup><mark>2.</mark></sup> <mark>**</mark><sup><mark>InformationAdvancement:</mark></sup> <mark>**</mark><sup><mark>3.</mark></sup> <mark>**</mark><sup><mark>Cross-Batch:</mark></sup> <mark>** [Examples] ## DATE EXTRACTION Extract from CURRENT_SUBTOPIC_DATA ## TEMPORAL BOUNDARIES **</mark><sup><mark>preparationphase:</mark></sup> <mark>**</mark><sup><mark>[Example]</mark></sup> <mark>**</mark><sup><mark>core_actionphase:</mark></sup> <mark>**</mark><sup><mark>[Example]</mark></sup> <mark>**</mark><sup><mark>integrationphase:</mark></sup> <mark>**</mark><sup><mark>[Example]</mark></sup> <mark>**</mark><sup><mark>ABSOLUTE:</mark></sup> <mark>**</mark><sup><mark>Nodatesoutside[START_DATE,END_DATE]fromTIMELINE</mark></sup> <mark>## CONTENT BOUNDARIES Extract from CURRENT_SUBTOPIC_DATA **</mark><sup><mark>Rules:</mark></sup> <mark>**</mark><sup><mark>ONLYgeneratefromcan_mentionNEVERgeneratefromcannot_mentionONLYreferencecurrentsubtopic</mark></sup> <mark>activities Use specified tense for main action **</mark><sup><mark>PhaseContent:</mark></sup> <mark>** **</mark><sup><mark>Preparation:</mark></sup> <mark>**</mark><sup><mark>[Example]</mark></sup> <mark>**</mark><sup><mark>CoreAction:</mark></sup> <mark>**</mark><sup><mark>[Example]</mark></sup> <mark>**</mark><sup><mark>Integration:</mark></sup> <mark>**</mark><sup><mark>[Example]</mark></sup> <mark>## TIMELINE DISTRIBUTION 1. Calculate: Total Days = END - START + 1 2. IF Days >= <num_batches>: Sequential dates 3. IF Days < < num_batches>: Group batches per day **</mark><sup><mark>Same-daydifferentiation:</mark></sup> <mark>**</mark><sup><mark>Timeprogression(morning->evening)ActivityfocusshiftsPerspectivechanges</mark></sup> <mark>Depth layers</mark> 

77 

Published as a conference paper at ICLR 2026 

<mark>## CONTEXT INTEGRATION 1. Review previous plans summary for established facts 2. Continue from previous plan if exists 3. IF INCLUDE_INTRODUCTION=YES: Introduce naturally 4. IF NO: Continue without re-introduction 5. Reference prior facts consistently 6. Show progression from previous ending ## VALIDATION GATES [Examples] ## EXECUTION 1. Extract/verify dates 2. Write FIRST-PERSON 3. Date ONLY in anchor 4. Maximum detail density 5. Exactly 30 bullets 6. Validate boundaries Output ONLY batch plans. End after ‘BATCH <num_batches> PLAN‘</mark> 

Listing 31: Ten million hierarchical conversation plan generation prompt 

<mark>You are generating realistic questions that a USER would ask an AI ASSISTANT. Create questions based ONLY on the specific details in the current bullet points. ## DOMAIN: <domain> ## TITLE: <title> ## CURRENT FOCUS AREAS (ONLY SOURCE FOR QUESTIONS): <FOCUSED_BULLETS> ## AVOID (ALREADY COVERED): <BATCH_HISTORY> ## CONTEXT REFERENCE (FOR UNDERSTANDING ONLY): <PREVIOUS_SUB_BATCH_PLANS> <PREVIOUS_BATCH_PLANS> ## CRITICAL RULES: ### 1. MANDATORY DETAIL COVERAGE & TRACKING **</mark><sup><mark>BEFOREGENERATING:</mark></sup> <mark>**</mark><sup><mark>ListeverydetailfromCURRENTFOCUSAREAS:</mark></sup> <mark>- Names: [extract all names] - Ages/Numbers: [extract all numbers] - Locations: [extract all places] - Facts/Situations: [extract all specific facts] **</mark><sup><mark>USAGETRACKING:</mark></sup> <mark>**</mark><sup><mark>Markeachdetailasusedtopreventrepetitionwithincurrentquestions.</mark></sup> <mark>### 2. ABSOLUTE SOURCE RESTRICTION **</mark><sup><mark>ONLYALLOWEDSOURCE:</mark></sup> <mark>**</mark><sup><mark>DetailsexplicitlywritteninCURRENTFOCUSAREASbulletpoints</mark></sup> <mark>**</mark><sup><mark>COMPLETELYFORBIDDEN:</mark></sup> <mark>** - ANY names, places, facts, or details from CONTEXT REFERENCE sections - ANY topics or content from BATCH_HISTORY **</mark><sup><mark>CONTEXTREFERENCERULE:</mark></sup> <mark>**</mark><sup><mark>UseCONTEXTREFERENCEonlytounderstandWHOpeopleareorWHATthingsmeanwhen</mark></sup> <mark>they appear in CURRENT FOCUS AREAS. NEVER generate questions about CONTEXT REFERENCE content. ### 3. ZERO REPETITION ENFORCEMENT **</mark><sup><mark>ABSOLUTEREQUIREMENT:</mark></sup> <mark>**</mark><sup><mark>EachspecificdetailcanONLYbementionedONCEacrossallquestions.</mark></sup> <mark>**</mark><sup><mark>ABSOLUTEPROHIBITIONS:</mark></sup> <mark>** - Using ANY detail more than once in current questions - Mentioning ANY topic/detail from BATCH_HISTORY - Referencing ANY content from CONTEXT REFERENCE sections - Asking about broader topics not in current bullets **</mark><sup><mark>VERIFICATION:</mark></sup> <mark>**</mark><sup><mark>Beforeeachquestion,confirmitdoesn’trepeatpreviouscontent.</mark></sup> <mark>### 4. ANTI-REPETITION SYSTEM **</mark><sup><mark>DETAILUSAGEPATTERN:</mark></sup> <mark>** - First mention: Use full specific detail from bullet point - Subsequent references: Use pronouns ("he", "she", "it", "that", "my choice") **</mark><sup><mark>VERIFICATION:</mark></sup> <mark>**</mark><sup><mark>Checkeachquestiondoesn’trepeat:</mark></sup> <mark>- Specific names/numbers already used - Topics from BATCH_HISTORY - Any details or content from reference sections (CONTEXT REFERENCE) ### 5. REALISTIC CONVERSATION STYLE **</mark><sup><mark>NATURALLANGUAGE:</mark></sup> <mark>** - Contractions: "I’m", "don’t", "can’t" - Casual words: "kinda", "sorta", "gonna" - Fillers: "like", "um", "you know" - Informal: "...", "??", "!!" ### 6. QUESTION VARIETY **</mark><sup><mark>AVOIDREPETITIVEPATTERNS:</mark></sup> <mark>** - Don’t start multiple questions the same way - Vary question length and complexity ### 7. QUESTION GENERATION STRATEGY - **Normal question** - **Seek advice** - **Ask for help** - **Request clarification** - **Get guidance** - **Express emotions** - **Validate decisions** - **Process thoughts** - **Explore options** **</mark><sup><mark>QUESTIONCLUSTERING:</mark></sup> <mark>** - Some bullets get 1 question, others get 2-3 - Deep dive into complex situations - Quick questions for simple details - User introducing himself/herself should be first question ## OUTPUT REQUIREMENTS:</mark> 

78 

Published as a conference paper at ICLR 2026 

<mark>Generate exactly <SUB_BATCH_SIZE> questions that: 1. **USE EVERY DETAIL** from current bullet points exactly once 2. Sound like genuine human requests for AI help 3. Focus on specific personal situations mentioned 4. Avoid all repetition from previous batches 5. Show realistic emotional responses to bullet situations 6. Follow natural conversation flow 7. **NEVER repeat specific details within current questions** 8. **NO repetitive "and" chains** in any message **</mark><sup><mark>SUCCESSCRITERIA:</mark></sup> <mark>** - Every name, age, location, fact from bullets MUST appear and appear ONLY ONCE - No repetition of BATCH_HISTORY topics - Questions sound like real people texting for advice - All questions trace back to specific bullet details - Subsequent references use pronouns/generic terms only - ZERO content from CONTEXT REFERENCE sections **</mark><sup><mark>OUTPUTFORMAT:</mark></sup> <mark>** For each question, use this exact format: [question text] ->-> [bullet_number] **</mark><sup><mark>CRITICAL:</mark></sup> <mark>** - Each question MUST end with "->-> [number]" where [number] is the bullet point it’s based on - Use bullet numbers 1, 2, 3, etc. as they appear in CURRENT FOCUS AREAS - If a question combines details from multiple bullets, use the primary bullet number - If the question is not generated from any bulletpoints, put N/A - Generate exactly <SUB_BATCH_SIZE> questions **</mark><sup><mark>Format:</mark></sup> <mark>**</mark><sup><mark>Onequestionperline,naturallength,nonumberingorextratext.</mark></sup> 

Listing 32: Question generation general domain prompt 

<mark>You are generating realistic coding questions that a DEVELOPER would ask an AI ASSISTANT. Create questions based ONLY on the specific details in CURRENT FOCUS AREAS. ## CURRENT FOCUS AREAS (STRICT SCOPE - ONLY SOURCE FOR QUESTIONS): <FOCUSED_BULLETS> ## QUESTIONS ALREADY COVERED IN THIS BATCH (AVOID THESE): <BATCH_HISTORY> ## CONTEXT REFERENCE (FOR UNDERSTANDING ONLY - DO NOT GENERATE QUESTIONS ABOUT THIS): <PREVIOUS_SUB_BATCH_PLANS> <PREVIOUS_BATCH_PLANS> ## BULLET TYPE DETECTION **</mark><sup><mark>MANDATORYFIRSTSTEP-CHECKEACHBULLET:</mark></sup> <mark>** - If bullet contains "**Time Anchor:**" -> ABSOLUTELY NO CODE, ONLY project/scheduling questions - If bullet contains "**Personal Introduction:**" -> ABSOLUTELY NO CODE, ONLY career/personal questions - Otherwise -> Technical bullet, GENERATE CODE ### 1. CURRENT FOCUS AREAS BULLET TYPE IDENTIFICATION - CHECK FIRST **</mark><sup><mark>BEFOREDOINGANYTHING:</mark></sup> <mark>**</mark><sup><mark>IdentifythebullettypeinCURRENTFOCUSAREAS:</mark></sup> <mark>- **Time Anchor:** bullets (contain "Time Anchor:" in title) -> NO CODE GENERATION - **Personal Introduction:** bullets (contain "Personal Introduction:" in title) -> NO CODE GENERATION - **Technical bullets:** (all others) -> CODE GENERATION REQUIRED ### 2. MANDATORY DETAIL COVERAGE & TRACKING **</mark><sup><mark>STEP1-MANDATORYEXTRACTION:</mark></sup> <mark>**</mark><sup><mark>BeforewritingANYquestions,youMUSTextractandlistEVERYSINGLEdetail</mark></sup> <mark>from CURRENT FOCUS AREAS: **</mark><sup><mark>ExtractALLofthesecategories:</mark></sup> <mark>** - **Names:** [list EVERY name - developer names, company names, project names, client names] - **Numbers/Versions:** [list EVERY version number, date, time, quantity, port, ID, measurement] [Other categories examples] **</mark><sup><mark>STEP2-VERIFICATION:</mark></sup> <mark>**</mark><sup><mark>Counttotalextracteddetails.YouMUSTuse100%ofthem.</mark></sup> <mark>**</mark><sup><mark>STEP3-TRACKING:</mark></sup> <mark>**</mark><sup><mark>Asyouwriteeachquestion,markwhichspecificdetailsituses.</mark></sup> <mark>**</mark><sup><mark>STEP4-FINALCHECK:</mark></sup> <mark>**</mark><sup><mark>Beforesubmitting,verifyEVERYextracteddetailappearsinatleastonequestion.</mark></sup> <mark>**</mark><sup><mark>ABSOLUTEREQUIREMENT:</mark></sup> <mark>**</mark><sup><mark>EverysingleextracteddetailMUSTappearinatleastonequestionacrossthebatch.</mark></sup> <mark>NO EXCEPTIONS. ### 3. ABSOLUTE SOURCE RESTRICTION **</mark><sup><mark>ONLYALLOWED:</mark></sup> <mark>**</mark><sup><mark>DetailsexplicitlywritteninCURRENTFOCUSAREASbulletpoints</mark></sup> <mark>**</mark><sup><mark>COMPLETELYFORBIDDEN:</mark></sup> <mark>** - ANY content from BATCH_HISTORY - ANY content from CONTEXT REFERENCE sections - Generic programming questions - Details not explicitly mentioned in current bullets **</mark><sup><mark>CONTEXTREFERENCERULE:</mark></sup> <mark>**</mark><sup><mark>UseonlytounderstandWHATtechnologies/componentsmeanwhentheyappearin</mark></sup> <mark>CURRENT FOCUS AREAS. ### 4. DETAIL USAGE PATTERN (ANTI-REPETITION) - **First mention:** Use full specific detail from bullet point (exact names, versions, error messages) - **Subsequent references:** Use pronouns ("it", "that", "my React app", "the API") - **VERIFICATION:** Each specific detail appears ONLY ONCE across all questions ### 5. MANDATORY COMPLEX CODE GENERATION **</mark><sup><mark>CRITICAL:85%ofquestionsMUSTincludesubstantialcodesnippets(20-60+lines)</mark></sup> <mark>** ONLY IF bullet’s title in CURRENT FOCUS AREAS is not time anchor or personal introduction</mark> 

79 

Published as a conference paper at ICLR 2026 

<mark>**</mark><sup><mark>ABSOLUTEEXCEPTIONS-NOCODEGENERATION:</mark></sup> <mark>** - **Time Anchor:** bullets - NEVER EVER generate any code, programming solutions, or technical implementations - **Personal Introduction:** bullets - NEVER EVER generate any code, programming solutions, or technical implementations - **FOR PERSONAL INTRODUCTION BULLETS:** Generate questions FROM the perspective of the person introducing themselves The person in the bullet is the USER asking the questions These are contextual/personal details, NOT technical coding scenarios **</mark><sup><mark>STOPANDVERIFY:Ifthebulletcontains"TimeAnchor:"or"PersonalIntroduction:"inthetitle,youMUST</mark></sup> <mark>NOT generate ANY code blocks, programming solutions, scripts, or technical implementations. Period.** **</mark><sup><mark>FORTIMEANCHOR/PERSONALINTRODUCTIONBULLETS:</mark></sup> <mark>** - Focus on project management, scheduling, personal goals - Ask about deadlines, meeting coordination, project planning - NO code blocks, NO programming solutions, NO technical implementations - Use natural conversation about timing, goals, and context **</mark><sup><mark>CODECOMPLEXITYREQUIREMENTS(forallotherbullets):</mark></sup> <mark>** - **Minimum 20-60+ lines per code block** - **Multiple functions/methods/classes (4-6 minimum)** - **Realistic imports and dependencies (3-5 minimum)** - **Proper error handling, validation, edge cases** - **Complex business logic, database operations, API calls** - **Production-level structure and realistic variable names** **</mark><sup><mark>REQUIREDPATTERNS(forcodingbulletsonly):</mark></sup> <mark>** - **Debugging (40%):** Generate buggy code with realistic, hard-to-spot errors - **Code Review (25%):** Generate working but suboptimal code needing improvements - **Implementation (20%):** Generate partial implementations with detailed TODOs - **Optimization (15%):** Generate slow/inefficient but functional code **</mark><sup><mark>NEVERusesimpleexamplesortutorial-stylecode-alwaysproduction-levelcomplexity</mark></sup> <mark>** ### 6. AUTHENTIC DEVELOPER STYLE **</mark><sup><mark>Language:</mark></sup> <mark>**</mark><sup><mark>Usecontractions("I’m","don’t"),devslang("lol","btw"),fillers("like","um"),informal</mark></sup> <mark>punctuation ("...", "??", "!!") **</mark><sup><mark>Emotion:</mark></sup> <mark>**</mark><sup><mark>Showgenuinefeelings-frustrationwithbugs,excitementaboutfeatures</mark></sup> <mark>**</mark><sup><mark>NaturalFlow:</mark></sup> <mark>**</mark><sup><mark>Mixquestionlengths,includerambling,thinkingoutloud</mark></sup> <mark>**</mark><sup><mark>TechnicalAuthenticity:</mark></sup> <mark>**</mark><sup><mark>Includeactualerrormessages,filenames,versionnumbersfrombullets</mark></sup> <mark>### 7. CHRONOLOGICAL ORDER Process bullet points in exact order provided. Earlier bullet details appear in earlier questions. ### 8. CODING QUESTION STRATEGY - **Implementation:** "Help me build [specific feature from bullet]" - **Debugging:** "I’m getting this error: [specific error]. How do I fix it?" - **Code Review:** "Can you review this [specific code] and suggest improvements?" - **Optimization:** "How can I make [specific implementation] faster?" ## OUTPUT REQUIREMENTS: Generate exactly <SUB_BATCH_SIZE> questions that: 1. **MANDATORY:** Use EVERY SINGLE detail from FOCUSED_BULLETS at least once (names, versions, errors, files, specs, etc.) 2. **85% MUST include substantial code snippets (20-60+ lines) with production-level complexity** 3. Sound like genuine developer requests with realistic technical scenarios 4. Follow chronological order of bullet points 5. **ALWAYS include complete, complex code - NEVER use simple examples** 6. Match one of the four coding patterns with appropriate complexity 7. Stay strictly within bullet point scope 8. **MANDATORY VERIFICATION:** Before submitting, confirm every extracted detail appears in the questions **</mark><sup><mark>OUTPUTFORMAT:</mark></sup> <mark>** - **CRITICAL: Generate ONLY the developer messages, nothing else** - Do NOT include question numbers, headers, or organizational text - **MANDATORY: Separate each complete message with "---MESSAGE_SEPARATOR---"** - Each message can span multiple lines and include code blocks - **CRITICAL: Each message MUST end with "->-> [number]" where [number] is the bullet point it’s based on** - **MANDATORY: End with "### COMPLETE ###"** **</mark><sup><mark>REQUIREDFORMATPATTERN:</mark></sup> <mark>** [Output format example] **</mark><sup><mark>CRITICALFORMATTINGRULES:</mark></sup> <mark>** [Output formatting rules] **</mark><sup><mark>CRITICALVERIFICATION:</mark></sup> <mark>**</mark><sup><mark>Beforeeachquestion:</mark></sup> <mark>1. **MANDATORY FIRST CHECK: What type of bullet is this?** - Time Anchor bullet -> Generate project management/scheduling questions, ABSOLUTELY NO CODE - Personal Introduction bullet -> Generate career/personal questions FROM their perspective, ABSOLUTELY NO CODE - Technical bullet -> Generate coding questions WITH substantial code 2. Does this use a specific detail from current bullets? 3. Have I included substantial, complex code (not simple examples) for technical bullets? 4. Does this sound like a real developer asking for help? 5. Am I following one of the four coding patterns correctly for technical bullets? **</mark><sup><mark>FINALVERIFICATIONBEFORESUBMITTING:</mark></sup> <mark>** Count how many extracted details appear in your questions. It MUST be 100% of all details from CURRENT FOCUS AREAS.</mark> 

80 

Published as a conference paper at ICLR 2026 

<mark>**</mark><sup><mark>Generateexactly<SUB_BATCH_SIZE>questionsintheformatabove.</mark></sup> <mark>**</mark> 

### Listing 33: Question generation coding domain prompt 

<mark>You are generating realistic math questions that a USER would ask an AI ASSISTANT. Create questions based ONLY on the specific details in CURRENT FOCUS AREAS. ## CURRENT FOCUS AREAS (STRICT SCOPE - ONLY SOURCE FOR QUESTIONS): <FOCUSED_BULLETS> ## QUESTIONS ALREADY COVERED IN THIS BATCH (AVOID THESE): <BATCH_HISTORY> ## CONTEXT REFERENCE (FOR UNDERSTANDING ONLY - DO NOT GENERATE QUESTIONS ABOUT THIS): <PREVIOUS_SUB_BATCH_PLANS> <PREVIOUS_BATCH_PLANS> ## CRITICAL RULES: ### 1. CURRENT FOCUS AREAS BULLET TYPE IDENTIFICATION - CHECK FIRST **</mark><sup><mark>BEFOREDOINGANYTHING:</mark></sup> <mark>**</mark><sup><mark>IdentifythebullettypeinCURRENTFOCUSAREAS:</mark></sup> <mark>- **Time Anchor:** bullets (contain "Time Anchor:" in title) -> NO MATHEMATICAL WORK GENERATION - **Personal Introduction:** bullets (contain "Personal Introduction:" in title) -> NO MATHEMATICAL WORK GENERATION - **Mathematical bullets: (all others) -> MATHEMATICAL WORK GENERATION REQUIRED ### 2. MANDATORY DETAIL COVERAGE & TRACKING **</mark><sup><mark>STEP1-MANDATORYEXTRACTION:</mark></sup> <mark>**</mark><sup><mark>BeforewritingANYquestions,youMUSTextractandlistEVERYSINGLEdetail</mark></sup> <mark>from CURRENT FOCUS AREAS: **</mark><sup><mark>ExtractALLofthesecategories:</mark></sup> <mark>** - **Names:** [list EVERY name mentioned - people, places, institutions, etc.] - **Numbers:** [list EVERY number, age, percentage, score, quantity, measurement] [Other categories example] **</mark><sup><mark>STEP2-VERIFICATION:</mark></sup> <mark>**</mark><sup><mark>Counttotalextracteddetails.YouMUSTuse100%ofthem.</mark></sup> <mark>**</mark><sup><mark>STEP3-TRACKING:</mark></sup> <mark>**</mark><sup><mark>Asyouwriteeachquestion,markwhichspecificdetailsituses.</mark></sup> <mark>**</mark><sup><mark>STEP4-FINALCHECK:</mark></sup> <mark>**</mark><sup><mark>Beforesubmitting,verifyEVERYextracteddetailappearsinatleastonequestion.</mark></sup> <mark>**</mark><sup><mark>ABSOLUTEREQUIREMENT:</mark></sup> <mark>**</mark><sup><mark>EverysingleextracteddetailMUSTappearinatleastonequestionacrossthebatch.</mark></sup> <mark>NO EXCEPTIONS. ### 3. ABSOLUTE SOURCE RESTRICTION **</mark><sup><mark>ONLYALLOWED:</mark></sup> <mark>**</mark><sup><mark>DetailsexplicitlywritteninCURRENTFOCUSAREASbulletpoints</mark></sup> <mark>**</mark><sup><mark>COMPLETELYFORBIDDEN:</mark></sup> <mark>** - ANY content from BATCH_HISTORY - ANY content from CONTEXT REFERENCE sections - Generic questions about mathematical fields - Details not explicitly mentioned in current bullets **</mark><sup><mark>CONTEXTREFERENCERULE:</mark></sup> <mark>**</mark><sup><mark>UseonlytounderstandWHO/WHATthingsmeanwhentheyappearinCURRENTFOCUS</mark></sup> <mark>AREAS. ### 4. DETAIL USAGE PATTERN (ANTI-REPETITION) - **First mention:** Use full specific detail from bullet point - **Subsequent references:** Use pronouns ("it", "that", "my homework") - **VERIFICATION:** Each specific detail appears ONLY ONCE across all questions ### 5. MANDATORY MATHEMATICAL WORK INCLUSION **</mark><sup><mark>CRITICAL:</mark></sup> <mark>**</mark><sup><mark>Whenreferencingproblems,equations,ormathematicalworkthatisn’texplicitlyprovidedin</mark></sup> <mark>bullets, you MUST generate and include the complete mathematical content. **</mark><sup><mark>ABSOLUTEEXCEPTIONS-NOMATHEMATICALWORKGENERATION:</mark></sup> <mark>** - **Time Anchor:** bullets - Generate questions about scheduling, deadlines, timing without any MATHEMATICAL WORK - **Personal Introduction:** bullets - Generate questions FROM the person introducing themselves about their background, career, goals without any MATHEMATICAL WORK - **FOR PERSONAL INTRODUCTION BULLETS:** Generate questions FROM the perspective of the person introducing themselves The person in the bullet is the USER asking the questions These are contextual/personal details, NOT MATHEMATICAL WORK scenarios **</mark><sup><mark>FORTIMEANCHOR/PERSONALINTRODUCTIONBULLETS:</mark></sup> <mark>** - Focus on study scheduling, academic deadlines, learning goals - Ask about exam preparation, study coordination, academic planning</mark> 

- <mark>NO mathematical equations, NO problem-solving, NO calculations</mark> 

- <mark>Use natural conversation about timing, goals, and academic context</mark> 

- <mark>**</mark><sup><mark>REQUIREDPATTERNS:</mark></sup> <mark>** - **Completely Stuck (40%):** NO work shown, just describe what you’re trying to solve - **Partially Stuck (30%):** Show ONLY initial 2-4 steps where you got stuck - **Need Verification (20%):** Show ONLY final answer/result - **Conceptual Confusion (10%):** NO calculations, concept-focused questions **</mark><sup><mark>WORKGENERATIONREQUIREMENTS:</mark></sup> <mark>** - Match mathematical level mentioned in bullet points - Include specific numbers, variables, expressions - Create realistic problems users would encounter - **NEVER use placeholders like "... (insert work)" - ALWAYS generate actual mathematical work** ### 6. AUTHENTIC USER STYLE</mark> 

81 

Published as a conference paper at ICLR 2026 

<!-- Start of picture text -->
** Language: ** Use contractions ("I’m", "don’t"), casual slang ("lol", "btw"), fillers ("like", "um"), informal<br>punctuation ("...", "??", "!!")<br>** Emotion: ** Show genuine feelings - confusion, frustration, excitement<br>** Natural Flow: ** Mix question lengths, include rambling, thinking out loud<br>### 7. CHRONOLOGICAL ORDER<br>Process bullet points in exact order provided. Earlier bullet details appear in earlier questions.<br>### 8. QUESTION GENERATION STRATEGY<br>- **Problem-Solving:** "Help me solve [specific problem]"<br>- **Concept Clarification:** "I don’t understand [specific concept]"<br>- **Solution Verification:** "Can you check if my solution is correct?"<br>- **Method Explanation:** "Why does [specific method] work?"<br>## OUTPUT REQUIREMENTS:<br>Generate exactly <SUB_BATCH_SIZE> questions that:<br>1. **MANDATORY:** Use EVERY SINGLE detail from FOCUSED_BULLETS at least once (names, ages, dates, traits,<br>goals, timeframes, etc.)<br>2. **80% MUST include substantial mathematical work** (equations, calculations, solution attempts)<br>3. Sound like genuine user requests with realistic mathematical content<br>4. Follow chronological order of bullet points<br>5. **ALWAYS include complete mathematical problems/equations - NEVER use placeholders**<br>6. Match one of the four behavioral patterns with appropriate work shown<br>7. Stay strictly within bullet point scope<br>8. **MANDATORY VERIFICATION:** Before submitting, confirm every extracted detail appears in the questions<br>** OUTPUT FORMAT: **<br>- **CRITICAL: Generate ONLY the user messages, nothing else**<br>- Do NOT include question numbers, headers, or organizational text<br>- **MANDATORY: Separate each complete message with "---MESSAGE_SEPARATOR---"**<br>- Each message can span multiple lines and include mathematical expressions<br>- **CRITICAL: Each message MUST end with "->-> [number]" where [number] is the bullet point it’s based on**<br>** REQUIRED FORMAT PATTERN: **<br>[Output format example]<br>** CRITICAL FORMATTING RULES: **<br>[Output formatting rules]<br>** CRITICAL VERIFICATION: ** Before each question:<br>1. Does this use a specific detail from current bullets?<br>2. **Is this a Time Anchor or Personal Introduction bullet? If YES, do NOT include any mathematical work**<br>3. **For Personal Introduction: Am I generating questions FROM the person’s perspective (they are the user)?**<br>4. Have I included actual mathematical work (not placeholders) for mathematical bullets?<br>5. Does this sound like a real user asking for help?<br>6. Am I following one of the four behavioral patterns correctly for mathematical bullets?<br>** FINAL VERIFICATION BEFORE SUBMITTING: **<br>Count how many extracted details appear in your questions. It MUST be 100% of all details from CURRENT FOCUS<br>AREAS.<br>** Generate exactly <SUB_BATCH_SIZE> questions in the format above. **<br><!-- End of picture text -->

Listing 34: Question generation math domain prompt 

<mark>You will receive an AI assistant’s reply. Determine whether it contains a **direct, specific question** that the user must answer next by providing new information, preferences, or a decision. - **YES** if, and only if, the assistant’s reply asks for a concrete user response (e.g. "What’s your budget for this trip?", "Which option would you prefer?"). - **NO** for generic or rhetorical prompts (e.g. "Any questions?", "Would you like to dive deeper?", "Consider your budget") that do not demand an immediate, specific answer. AI ASSISTANT RESPONSE: <assistant_response> CRITICAL NOTE: Respond only in English. Do not include any Chinese. Output exactly **YES** or **NO**, nothing else.</mark> 

Listing 35: Check assistant’s response include question prompt 

<mark>You are simulating a typical user in conversation. Decide if you would ask a follow-up question after the AI’s response. **</mark><sup><mark>CONVERSATIONCONTEXT:</mark></sup> <mark>** - DOMAIN: <domain> - TITLE: <title> - THEME: <theme> - SUBTOPICS: <subtopics> - Recent History: <formatted_history> - AI’s Last Response: <assistant_response> **</mark><sup><mark>ASKFOLLOW-UP("yes")WHEN:</mark></sup> <mark>** 1. **Missing Info**: The response lacks details you genuinely need to proceed - Specific steps for a process you’re trying to follow - Key parameters (dates, amounts, requirements) for a decision you’re making - Clarification on which option applies to your specific situation 2. **Genuine Confusion**: Something is unclear or contradictory</mark> 

82 

Published as a conference paper at ICLR 2026 

<mark>- Technical terms used without explanation that block understanding - Conflicting information that affects your next action - Ambiguous instructions where the wrong interpretation has consequences 3. **Incomplete Practical Guidance**: You asked "how to" but can’t actually do it yet - Missing steps in a procedure - Lacks specifics needed for implementation - Assumes knowledge you don’t have **</mark><sup><mark>NOFOLLOW-UP("no")WHEN:</mark></sup> <mark>** 1. **Good Enough to Proceed**: You have what you need **</mark><sup><mark>OUTPUT:</mark></sup> <mark>**</mark><sup><mark>Only"yes"or"no"</mark></sup> 

Listing 36: Check need for followup prompt 

<mark>You must respond only in English. Never switch to Chinese or any other language mid-sentence. All responses should be entirely in English. Respond to the user’s message by either: • Fully answering their question . Provide a comprehensive answer • Answering plus asking at most ONE follow-up question if you need more detail Always honor these rules: 1. Do NOT ask questions the user already answered. 2. Only ask a question if you genuinely need context to provide a complete, actionable answer. 3. Keep your main answer clear and comprehensive before you ask. 4. Use the following system inputs: DOMAIN: <domain> TITLE: <title> THEME: <theme> SUBTOPICS: <subtopics> PREVIOUS PLANS SUMMARY: <previous_plans_summary> PREVIOUS BATCHES OF THIS PLAN: <previous_batches> CURRENT HISTORY: <current_batch_messages> CRITICAL NOTE: Respond only in English. Do not include any Chinese. **</mark><sup><mark>Output</mark></sup> <mark>** Return exactly what you’d say to the user---no tags, no internal notes.</mark> 

Listing 37: Assistant LLM answer generation prompt 

<mark>You are role-playing as a real user having an authentic conversation with an AI chat assistant. The AI assistant has just asked you a question, and you need to provide a natural, human-like response. #### Input Context You’ll Receive: - **Current Batch Message History**: The conversation flow leading to the AI’s question - **Domain, Title, Theme & Subtopics**: The main subject of this conversation - **Previous Plans**: Summary of earlier conversation contexts for continuity - **Current Plan**: The overarching narrative direction for this conversation batch - **AI’s Question**: The specific question the assistant asked that requires your response #### INPUTS: **</mark><sup><mark>CurrentBatchMessageHistory</mark></sup> <mark>**</mark><sup><mark>:<current_batch_messages></mark></sup> <mark>**</mark><sup><mark>DOMAIN:<domain></mark></sup> <mark>**</mark><sup><mark>TITLE:<title></mark></sup> <mark>**</mark><sup><mark>THEME:<theme></mark></sup> <mark>**</mark><sup><mark>SUBTOPICS:<subtopics></mark></sup> <mark>**</mark><sup><mark>PreviousPlansSummary</mark></sup> <mark>**</mark><sup><mark>:<previous_plans_summary></mark></sup> <mark>**</mark><sup><mark>PreviousBatchesofThisPlan</mark></sup> <mark>**</mark><sup><mark>:<previous_batches></mark></sup> <mark>**</mark><sup><mark>CurrentPlan</mark></sup> <mark>**</mark><sup><mark>:<current_plan></mark></sup> <mark>**</mark><sup><mark>AI’sQuestion</mark></sup> <mark>**</mark><sup><mark>:<ai_last_message></mark></sup> <mark>#### CRITICAL: Keep Responses SHORT and Natural **</mark><sup><mark>Realusersgivebrief,to-the-pointanswerstoAIquestions</mark></sup> <mark>** #### Your Role & Behavior: You are a real human user with: - Personal experiences, opinions, and emotions - Natural speech patterns and conversational habits - Realistic knowledge limitations and curiosity - Consistent personality traits across the conversation **</mark><sup><mark>LanguageAuthenticity:</mark></sup> <mark>** - Use lots of contractions: "I’m", "don’t", "can’t", "it’s", "that’s" - Include casual slang: "lol", "btw", "tbh", "kinda", "sorta", "gonna", "wanna" - Add filler words: "like", "um", "you know", "I mean", "so", "well" - Use informal punctuation: multiple periods "...", question marks "??", exclamation points "!!" **</mark><sup><mark>ImperfectNaturalSpeech:</mark></sup> <mark>** - Include minor typos and informal grammar - Add rambling elements: "I mean, ..." - Include thinking out loud: "hmm", "actually", "oh", "maybe" **</mark><sup><mark>EmotionalAuthenticity:</mark></sup> <mark>** - Show genuine feelings: excitement, frustration, uncertainty, hope - Use emotional language - Add personal reactions: "ugh", "omg", "yay", "oof", "blah"</mark> 

83 

Published as a conference paper at ICLR 2026 

<mark>#### Response Guidelines: **</mark><sup><mark>STEP1-CheckPlansforExistingInformation</mark></sup> <mark>**</mark><sup><mark>:</mark></sup> <mark>- **First**, carefully review the Current Plan and Previous Plans for any information that answers the AI’s question - **If found in plans**: Base your response on that established information to maintain story continuity - **If not found in plans**: Create a new answer that aligns with the topic, theme, and existing storyline **</mark><sup><mark>STEP2-AnswertheAI’sQuestionDirectly</mark></sup> <mark>**</mark><sup><mark>:</mark></sup> <mark>- Keep your reply focused on answering; do **not** introduce new questions. - Give a direct answer to what the AI asked - Don’t over-explain or provide unnecessary details - Answer like you would in a real text conversation - Include personal context or examples when natural - **CRITICAL**: Ensure your answer doesn’t contradict anything established in previous or current plans **</mark><sup><mark>StayConsistentwithContext</mark></sup> <mark>**</mark><sup><mark>:</mark></sup> <mark>- Maintain the same personality and circumstances throughout - Keep your responses aligned with the current topic and theme **</mark><sup><mark>ResponseCharacteristics</mark></sup> <mark>**</mark><sup><mark>:</mark></sup> <mark>- **Tone**: Match the conversation’s emotional tone and your established personality - **Authenticity**: Sound like a real person, not an AI trying to sound human #### Critical Instructions: - **Be concise** - Real people don’t write long in chat - Keep your reply focused on answering; do **not** introduce new questions. - **ALWAYS check plans first** - Look for any information that answers the AI’s question before creating new details - **Maintain consistency** - Never contradict information established in current or previous plans - **Fill gaps naturally** - If plans don’t have the answer, create responses that fit the established storyline - ONLY provide your response as the user - no meta-commentary - Stay in character as a human user throughout - Answer the question but don’t feel obligated to ask a question back (the AI asked YOU)</mark> 

Listing 38: User LLM answer generation prompt 

<mark>You must respond **only in English**. Do not include any Chinese characters or phrases in your response. You are a real person having a conversation with an AI assistant. Based on the conversation history and the AI ’s last response, ask ONE natural follow-up question. ## CONTEXT: **</mark><sup><mark>CurrentBatchMessageHistory</mark></sup> <mark>**</mark><sup><mark>:<current_batch_messages></mark></sup> <mark>**</mark><sup><mark>DOMAIN:<domain></mark></sup> <mark>**</mark><sup><mark>TITLE:<title></mark></sup> <mark>**</mark><sup><mark>THEME:<theme></mark></sup> <mark>**</mark><sup><mark>SUBTOPICS:<subtopics></mark></sup> <mark>**</mark><sup><mark>PreviousPlansSummary</mark></sup> <mark>**</mark><sup><mark>:<previous_plans_summary></mark></sup> <mark>**</mark><sup><mark>PreviousBatchesofThisPlan</mark></sup> <mark>**</mark><sup><mark>:<previous_batches></mark></sup> <mark>**</mark><sup><mark>CurrentPlan</mark></sup> <mark>**</mark><sup><mark>:<current_plan></mark></sup> <mark>**</mark><sup><mark>AI’sResponse</mark></sup> <mark>**</mark><sup><mark>:<ai_last_message></mark></sup> <mark>## YOUR TASK Ask a follow-up question (10-20 words) that a real person would naturally ask after receiving the AI’s response.</mark> 

<mark>## CRITICAL RULES TO PREVENT REPETITION Before generating your question: 1. **Scan the Current Batch Message History** for all topics already discussed 2. **Check Previous Batches** for questions already asked 3. **Never ask about something already covered** If you notice your question seeks information already provided in the conversation history, STOP and generate a completely different question. ## HOW REAL PEOPLE ASK FOLLOW-UPS ### Natural conversation starters: - "oh wait..." / "hmm..." / "actually..." / "btw..." / "ok but..." - "that’s cool but..." / "makes sense, though..." / "yeah but what about..." ### Authentic reaction patterns: **</mark><sup><mark>Buildingonthelastairesponse:</mark></sup> <mark>** - Ask about a specific topic not yet covered - Connect it to your personal situation from the Current Plan **</mark><sup><mark>Showinggenuinereactions:</mark></sup> <mark>** - If AI gave good news -> "nice! but does that mean..." [Other examples] ### Question types that feel natural: - **Practical concerns**: "how long does that usually take?" [Other types] ## NATURAL SPEECH PATTERNS Include these elements to sound human: - Contractions: "don’t", "can’t", "won’t", "that’s" - Casual words: "kinda", "sorta", "gonna", "like" - Emotional reactions: "ugh", "hmm", "oh", "yikes" - Informal punctuation: "..." or "??" or "!"</mark> 

84 

Published as a conference paper at ICLR 2026 

<mark>## CONVERSATION FLOW AWARENESS Based on where you are in the Current Batch Message History: Ask broader exploratory questions Ask for specific details or comparisons Ask about implementation or next steps ## AUTHENTICITY CHECKLIST [Some examples] CRITICAL NOTE: Respond only in English. Do not include any Chinese. ## YOUR RESPONSE: [Generate only the follow-up question, nothing else]</mark> 

Listing 39: User LLM ask followup question prompt 

<mark>I provide you with a text. Your task it to identify all the details stated in the text, and output that in key: value format. E.g.: Key 1: Value 1, Key 2: Value 2, Key 3: Value 3, .... Also at the end, I want you to provide a brief summary of what this text was about in this format: Summary: ’ summarized text’ Note: only output key-values and the summary. DO NOT provide any explanation before or after that. Note: Do not output Key 1, Key 2, ... **</mark><sup><mark>PreviousContext:</mark></sup> <mark>** {history} text: {text}</mark> 

Listing 40: Key-value extraction prompt 

<mark>You are a highly analytical AI assistant. Your task is to analyze the latest conversation exchange and produce a structured summary of key information and insights. **</mark><sup><mark>YourInternalProcess:</mark></sup> <mark>** To ensure maximum accuracy, you must first think step-by-step. 1. **</mark><sup><mark>Analyze:</mark></sup> <mark>**</mark><sup><mark>Breakdowntheuser’slatestmessage.</mark></sup> <mark>2. **</mark><sup><mark>Identify:</mark></sup> <mark>**</mark><sup><mark>Pinpointallfacts,instructions,andupdates.</mark></sup> <mark>3. **</mark><sup><mark>Deduce:</mark></sup> <mark>**</mark><sup><mark>Reasonabouttheimplicationsofthenewinformationinthecontextoftheconversation</mark></sup> <mark>history. What is the user’s underlying goal or state? 4. **</mark><sup><mark>Format:</mark></sup> <mark>**</mark><sup><mark>Aftercompletingyourinternalanalysis,formattheconclusionsintothe‘ExtractedFacts‘</mark></sup> <mark>structure. **</mark><sup><mark>CrucialInstruction:</mark></sup> <mark>**</mark><sup><mark>Yourfinaloutputmust</mark></sup> <mark>**</mark><sup><mark>ONLY</mark></sup> <mark>**</mark><sup><mark>bethe‘ExtractedFacts‘block.</mark></sup> <mark>**</mark><sup><mark>DONOT</mark></sup> <mark>**</mark><sup><mark>include</mark></sup> <mark>your step-by-step reasoning or any other text in your response. Strictly follow the format shown in the example’s output. --**</mark><sup><mark>EXAMPLE</mark></sup> <mark>** **</mark><sup><mark>ConversationContext:</mark></sup> <mark>** * **</mark><sup><mark>RecentConversationHistory:</mark></sup> <mark>** USER: Hey, I need some help with the "Project Phoenix" launch plan. ASSISTANT: Of course. What do you need? USER: The launch date is set for September 15th, 2025. I’m responsible for the marketing materials. * **</mark><sup><mark>LatestExchangetoAnalyze:</mark></sup> <mark>** USER: Okay, the final budget for the social media campaign is $7,500. The client, Innovate Corp, just approved it. Please find me three case studies of successful B2B SaaS launches by tomorrow, August 28th. And don’t include any of our direct competitors in the examples. ASSISTANT: Understood. I will find three case studies of successful B2B SaaS launches, excluding competitors, and have them for you by tomorrow, August 28th. The approved budget of $7,500 for the social media campaign has been noted. **</mark><sup><mark>ExampleofCorrectFinalOutput:</mark></sup> <mark>** *</mark><sup><mark>Theclient’snameis"InnovateCorp".</mark></sup> <mark>*</mark><sup><mark>Theprojectisrelatedtoa"B2BSaaSlaunch".</mark></sup> <mark>*</mark><sup><mark>Thefinalbudgetforthesocialmediacampaignis\$7,500.</mark></sup> <mark>*</mark><sup><mark>Adeadlineissetfor"tomorrow,August28th".</mark></sup> <mark>*</mark><sup><mark>Userintendstoreviewthreecasestudiesfortheproject.</mark></sup> <mark>*</mark><sup><mark>Instruction:Findthreecasestudies.</mark></sup> <mark>*</mark><sup><mark>Constraint:Donotincludedirectcompetitorsintheexamples.</mark></sup> <mark>*</mark><sup><mark>Thebudgetforthesocialmediacampaignhasbeenapprovedbytheclient.</mark></sup> 

- <sup><mark>Theuserisunderadeadlineandneedsthecasestudiesurgentlytoinformtheirworkonthemarketing</mark></sup> <mark>materials.</mark> 

<mark>**</mark><sup><mark>ACTUALTASK</mark></sup> <mark>** **</mark><sup><mark>RecentConversationHistory:</mark></sup> <mark>** {history} **</mark><sup><mark>LatestExchangetoAnalyze:</mark></sup> <mark>** USER: {latest_user_message}</mark> 

<mark>ASSISTANT: {latest_assistant_message}</mark> 

85 

Published as a conference paper at ICLR 2026 

<mark>**</mark><sup><mark>ExtractedFacts:</mark></sup> <mark>**</mark> 

### Listing 41: Scratchpad creation prompt 

<mark>You are tasked with summarizing and compressing scratch pad content to fit within a specific token limit. **</mark><sup><mark>InputContent:</mark></sup> <mark>** {content} **</mark><sup><mark>TargetLength:</mark></sup> <mark>**</mark><sup><mark>{tokens_limit}tokens</mark></sup> <mark>**</mark><sup><mark>YourTask:</mark></sup> <mark>** Compress this content by clustering related information, removing redundancy, and prioritizing the most important details. **</mark><sup><mark>Process:</mark></sup> <mark>** 1. **Cluster**: Group related information by topic, entity, or theme 2. **Deduplicate**: Remove redundant or repetitive information 3. **Prioritize**: Keep the most important and contextually relevant details 4. **Compress**: Condense while maintaining essential meaning and context **</mark><sup><mark>OutputFormat:</mark></sup> <mark>** Return ONLY the compressed content organized as: **</mark><sup><mark>KEYENTITIES&RELATIONSHIPS:</mark></sup> <mark>** - [Most important people, organizations, systems mentioned] **</mark><sup><mark>COREDECISIONS&PREFERENCES:</mark></sup> <mark>** - [Critical decision points, requirements, constraints] **</mark><sup><mark>PROCESSES&WORKFLOWS:</mark></sup> <mark>** - [Essential procedural information and methodologies] **</mark><sup><mark>USERPREFERENCES:</mark></sup> <mark>** - [User’s stated likes, dislikes, preferred methods, settings, choices] **</mark><sup><mark>USERINSTRUCTIONS:</mark></sup> <mark>** - [Specific directions, commands, or guidance provided by the user] **</mark><sup><mark>IMPORTANTDATES:</mark></sup> <mark>** - [Deadlines, milestones, scheduled events, time-sensitive information] **</mark><sup><mark>CRITICALCONTEXT:</mark></sup> <mark>** - [Background information necessary for understanding] **</mark><sup><mark>ACTIONABLEITEMS:</mark></sup> <mark>** - [Next steps, pending actions, deadlines] **</mark><sup><mark>IMPORTANTDEVELOPMENTS:</mark></sup> <mark>** - [Significant events, changes, milestones] **</mark><sup><mark>Requirements:</mark></sup> <mark>** - Stay within {tokens_limit} tokens - Eliminate redundancy while preserving essential information - Eliminate older values when there is newer and updated value for a thing - Maintain chronological context where important - Prioritize information with ongoing relevance" **</mark><sup><mark>CRITICALLENGTHREQUIREMENT:</mark></sup> <mark>** - Your response should be approximately {tokens_limit} tokens - If your draft is significantly shorter than {tokens_limit} tokens, ADD MORE DETAIL</mark> 

Listing 42: Scratchpad summarization prompt 

<mark>I provide you with a user query and a text chunk. You need to decide if the text chunk is nesseccery for answering user question. If we need the text chunk to answer the user question, or if the text chunk is part of the answer to user question return ’yes’ If the text chunk is noise and not relevant to user question, return ’no’. Output format: Return only ’yes’ or ’no’, without any explantion before or after that. User query: {query} \n\n Text chunk: {doc_text}</mark> 

Listing 43: Scratchpad noise filtering prompt 

<mark>You are an assistant that MUST answer questions using ONLY the information provided in the context below. STRICT INSTRUCTIONS: 1. Answer ONLY based on the provided context 2. Do NOT use your internal knowledge CONTEXT: <context> QUESTION: <question></mark> 

86 

Published as a conference paper at ICLR 2026 

<mark>ANSWER REQUIREMENTS: - Be direct and concise - Only output the answer to the question without any explanation RESPONSE:</mark> 

Listing 44: Answer generation with RAG prompt 

87
