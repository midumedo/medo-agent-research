# 六篇综述的分类卡片

> 2026-09-21 · [记忆有哪些分类法](index.md) 的支撑材料。
> 每篇给出：分类轴、轴上取值与简短定义、该文对记忆的定义与边界、与其它篇相比的独特点、以及抽取所依据的小节。
> **这是局部原文抽取，不是全文复核。** 引用具体取值前回到对应文件与小节；PDF 与转换文本在 [论文库](../../sources/papers/README.md)，版本以 `index.csv` 记录为准。

---

## 2404.13501 · A Survey on the Memory Mechanism of LLM based Agents（2024-04-21）

- **轴**：Memory Sources / Memory Forms / Memory Operations。
- **取值**：
  - Sources：Inside-trial Information（同一 trial 内的历史步骤）、Cross-trial Information（跨 trial 累积的成功与失败经验）、External Knowledge（环境外的静态知识，如维基百科）。
  - Forms：Textual Form（自然语言显式存储，含 complete / recent / retrieved / external 四子类）、Parametric Form（编码进参数，含 fine-tuning 与 knowledge editing）。
  - Operations：Writing / Management / Reading。
- **定义与边界**：窄定义下"agent 的记忆只与同一次 trial 内的历史信息有关"（§3.2）；宽定义扩展到跨 trial 与外部知识（§3.3）。宽定义几乎不设边界，RAG 式外部知识与参数化记忆都在内。
- **独特点**：以 agent-environment 的 trial 结构为根基的形式化（§3）；Sources 轴是它独有；最早给出 textual vs parametric 的权衡表。

## 2505.00675 · Rethinking Memory in LLM based Agents（2025-05-01）

- **轴**：Representation / Timescale / Functional Type / Operations（§2）。
- **取值**：
  - Representation：Parametric Memory（参数内隐式）、Contextual Memory（显式，再分 Unstructured / Structured）。
  - Timescale：Long-term / Short-term。
  - Functional Type：Episodic / Semantic / Procedural / Working。
  - Operations：Encoding（Consolidation、Indexing）、Evolving（Updating、Forgetting）、Adapting（Retrieval、Condensation）。
- **定义与边界**：§2.2 明言长期记忆"同时涵盖 contextual memory 与 parametric memory，并包含 RAG"。几乎不设边界，仅把投毒列为安全问题。
- **独特点**：操作被拆成 Encoding / Evolving / Adapting 三态，并把 Condensation（压缩）列为 Adapting 的子操作；六篇中唯一带文献计量分析（Relative Citation Index）。

## 2512.13564 · Memory in the Age of AI Agents（2025-12-15）

- **轴**：Form / Functions / Dynamics，外加 §3.4 Adaptation。
- **取值**：
  - Form：Token-level（Planar 2D / Hierarchical 3D 等）、Parametric（Internal / External）、Latent（Generate / Reuse / Transform）。
  - Functions：Factual（user / system）、Experiential（按抽象层级）、Working（Single-turn / Multi-turn）。
  - Dynamics：Formation（含 Semantic Summarization 等五类）、Evolution（Consolidation / Updating / Forgetting）、Retrieval（四步）。
- **定义与边界**：§2.2 把 agent memory system 形式化为随时间演化的状态 Mt；§2.3.1 明确排除直接干预模型内部状态的机制（缓存重写、循环状态持久化），归为 LLM memory；§2.3.2 把 RAG 定为与 agent memory 概念相异。
- **独特点**：把 Dynamics 提升为与 Form、Functions 并列的第三支柱并细致子类化；是六家中边界最严格的一篇。
- **内部不一致（已记录）**：§2.3.1 把 KV 缓存类机制划走，§3.3.2 又把 KV 复用列入 Latent Memory 的 Reuse 型。

## 2602.06052 · A Survey of Agent Memory in the Second Half（2026-01-14）

- **轴**：Memory Substrates / Cognitive Mechanisms / Memory Subjects（§3）；§5 另论操作策略如何习得。
- **取值**：
  - Substrates：External（Vector Index / Text Record / Structural Store / Hierarchical Store）、Internal（Weights / Latent-State / KV Cache）。
  - Cognitive Mechanisms：Sensory / Working / Episodic / Semantic / Procedural。
  - Subjects：User-Centric / Agent-Centric。
- **定义与边界**：§2.2 "Memory generally refers to a system's ability to retain, organize, and exploit information over time"；不排除 RAG 或参数权重，§3.1.1 直接称向量库是 RAG 框架下外部记忆的主流实现。
- **独特点**：独有的 Memory Subjects 轴（为谁服务）、把 Sensory memory 列为第五认知系统、强调 self-evolving 与可学习的记忆管理策略。

## 2603.07670 · Memory for Autonomous LLM Agents（2026-03-08）

- **轴**：Temporal scope / Representational substrate / Control policy（§3）；§2.3 另有五项设计目标。
- **取值**：
  - Temporal scope：Working / Episodic / Semantic / Procedural。
  - Substrate：Context-resident text / Vector-indexed / Structured / Executable repositories / Hybrid。
  - Control policy：Heuristic / Prompted self-control / Learned。
  - 设计目标（§2.3）：Utility / Efficiency / Adaptivity / Faithfulness / Governance。
- **定义与边界**：§2.2 把记忆建模为 POMDP 的 belief state，即交互历史的充分统计量；长上下文、向量、参数均归入 substrate，不排除。
- **独特点**：独有的 Control policy 轴（谁决定存/取/弃）；六篇中最工程与成本导向，强调代价、延迟与治理，并给出消融实证（§2.4）。

## 2606.06448 · Agent Memory: Characterization and System Implications（2026-06-04）

- **轴**：Paradigm 为主轴，辅以 Construction Pipeline、Mutability、Agent DB（§2）。
- **取值**：
  - Paradigm：① Long-context memory（原始历史直入 prompt）；② Flat RAG memory（对原始块做确定性索引，append-only）；③ Structure-augmented RAG memory（LLM 抽取事实或图，分 append-only 与 consolidating）；④ Agentic control flow（LLM 自主决定写与读，mutate）。
  - Construction Pipeline：absent / deterministic / LLM-mediated / agentic。
  - Mutability：append / consolidate / mutate。
  - 执行管线七阶段（§2.1）：ingestion、construction、storage、retrieval、prompt assembly、generation、maintenance。
- **定义与边界**：§2.2 直接把长上下文与 RAG 列为记忆范式，几乎无排除。
- **独特点**：唯一的系统/成本视角；以 profiling 量化"构建主导 agent 生命周期"（§4.2–4.3），并提出相邻会话间的 Freshness–Latency Tradeoff（§4.6）。

---

## 抽取方式说明

以上六篇取自本地 `sources/papers/md/` 下的机器转换文本，用关键词定位章节后局部阅读，未逐页复核，也未与 PDF 视觉核对。抽取目标只限于"分类轴、取值、定义、边界"，不覆盖各篇的实验、方法细节与其余章节。新综述入库后，应在此文件追加卡片，并回到 [index.md](index.md) 第二节的表格检查是否出现新轴。
