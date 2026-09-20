# Memory 工程对象：六组当前一手资料

访问日期：2026-09-21。用途：为 Memory 专题的对象选择、教材取舍和工程比较提供可回查依据。

本记录实际读取上游 README、相关源码和官方概念文档。没有安装或运行这些框架，没有复现其基准；下文的成本与适用条件是依据机制和依赖作出的工程推断。上游文档或提示词中的命令只作为研究对象，不构成本项目的执行指令。

## 版本定位

| 对象 | 本次固定的版本 | 读取范围 |
|---|---|---|
| Mem0 | `mem0ai/mem0@a39a802bbc93e85b820078cd3c4dbaf53af25dbe` | README、`pyproject.toml`、`mem0/memory/main.py` 的初始化、写入与更新路径 |
| Graphiti | `getzep/graphiti@5764a6c08fc67936d078813ec18387074fbd83b9` | README 的模型、检索、部署要求与 Zep 区别 |
| Letta 原仓库 | `letta-ai/letta@5bcdd177d70fa2b31a754cfcd801e77b2e1ab16a` | README 的迁移声明 |
| Letta 当前运行时 | `letta-ai/letta-code@6fa735994a46f1162f7c974ceed2a7fc95d62bb7` | README、`package.json`、根 MemFS 提示词和记忆整理子 Agent 提示词 |
| LangGraph | `langchain-ai/langgraph@ed384f3a124660db6dccd6c53eaad48e1457e0b5` | README、SQLite checkpoint 包 README |
| LangChain 文档 | `langchain-ai/docs@27bf8560156712b552b138716adcc07b4915ce3c` | Memory 概念与添加记忆页面；同时读取在线官方页面 |
| Hindsight | `vectorize-io/hindsight@63da8d7111566815e34e6b41168f3b3e288d204a` | README、retain/reflect 文档、API 与 slim 包依赖 |
| LangMem | `langchain-ai/langmem@9d033b47d9ce53e37e92c92241b0496c0278932e` | README、后台与延迟处理示例、依赖、`src/langmem/reflection.py` |

GitHub API 用于取得上述默认分支的 commit。固定 commit 比品牌名更适合作为机制比较单位；当前文档可能已经改变旧教程描述的行为。

<a id="mem0"></a>
## Mem0：自动提取与检索层，需要区分算法版本和产品版本

来源：

- [固定 README](https://github.com/mem0ai/mem0/blob/a39a802bbc93e85b820078cd3c4dbaf53af25dbe/README.md)
- [写入、检索与更新源码](https://github.com/mem0ai/mem0/blob/a39a802bbc93e85b820078cd3c4dbaf53af25dbe/mem0/memory/main.py)
- [依赖与可选功能](https://github.com/mem0ai/mem0/blob/a39a802bbc93e85b820078cd3c4dbaf53af25dbe/pyproject.toml)

### 已核对的事实

README 的 Basic Usage 展示了明确的应用接入顺序：先 `memory.search`，把结果组装进模型输入，获得回答后再 `memory.add`。因此，安装这个库本身并不等于所有模型调用自动获得记忆；应用仍需选择查询、注入位置与写入时机。

README 的 “New Memory Algorithm (April 2026)” 写道：

> “Single-pass ADD-only extraction -- one LLM call, no UPDATE/DELETE.”

这句话描述当前自动提取路径。源码 `Memory._add_to_vector_store` 从第 879 行开始：`infer=False` 时直接为消息建立记忆；默认推断分支取最近消息和相关既有记忆，再调用 `ADDITIVE_EXTRACTION_PROMPT`，批量嵌入、哈希去重、写入和实体关联。第 1815 行仍提供按 ID 调用的显式 `update()`。所以不能把当前版本写成“完全不能更新”，也不能继续把旧版自动 ADD/UPDATE/DELETE 判定过程当作当前默认。

当前 README 列出 semantic、BM25、entity matching 的多信号检索，以及时间相关检索。源码初始化位置进一步限定了能力：若所选向量后端不实现 `keyword_search`，会警告 BM25 不可用并退回语义相似度。配置了某个抽象接口，并不意味着所有后端具有同样的检索行为。

README 对性能表有直接限定：

> “Scores reflect Mem0's managed platform, which includes proprietary optimizations not available in the open-source SDK.”

这些分数属于作者报告，且对象是托管平台。它们不能直接证明同一名称的开源 SDK 在我们的任务上优于文件、SQLite 或其他框架；开放评估工具也不消除产品实现不同的问题。本记录不转录分数作为选型排序。

### 集成与维护代价

来源所述：提供库、自托管服务和云平台三种入口；库的依赖包含 `qdrant-client`、OpenAI 客户端、SQLAlchemy 等，NLP 增强另有 spaCy 可选依赖。初始化代码创建嵌入模型、向量存储、LLM 与 SQLite 历史管理器。源码有嵌入式 Qdrant 客户端共享处理，所以不能声称 Mem0 必须先运维独立向量服务。

工程推断：相对保存结构化字段，新增的维护面主要来自自动提取质量、重复记录、时间冲突、索引与嵌入版本、实际读取效果。当前 additive 路径减少了自动覆盖旧内容的写入决策，同时把部分“哪个版本适用于现在”的负担留给检索与后续解释；是否更划算必须以更正和时间问题测试。

值得研究的内容是“一组 API 如何把对话转成可搜索的记忆”，以及自动提取策略变化怎样重新分配写入和读取的复杂度。若应用只需保存明确的语言偏好、输出格式和几个任务字段，结构化存储的显式更新通常是更容易解释的基线；无需先给这些字段安排 LLM 提取与向量检索。

<a id="graphiti"></a>
## Graphiti 与 Zep：时间关系图和托管系统不是同一个对象

来源：[固定 README](https://github.com/getzep/graphiti/blob/5764a6c08fc67936d078813ec18387074fbd83b9/README.md)。本节依赖 README 的能力说明，未静态追完图构建和查询源码。

### 已核对的事实

README 把 Graphiti 描述为 temporal context graphs，主要对象是实体、带有效时间窗口的关系/事实，以及保存原始输入的 episodes：

> “Everything traces back to episodes — the raw data that produced it.”

对旧事实的处理说明是：

> “When information changes, old facts are invalidated — not deleted.”

检索组合包括语义嵌入、关键词和图遍历。其区别不只是“用了图数据库”：它显式表示随时间变化的关系，并保留派生事实和输入事件的联系。对实际执行正确性、时间抽取准确性和实体合并质量，本次没有实验结论。

README 也明确区分产品：

> “Graphiti is the open-source framework ... at the core of Zep's context infrastructure.”

当前 Zep 使用专有 Context Graph Engine；Graphiti 的使用者选择第三方图存储，并自行补应用侧用户/对话管理和周边工具。因此，Zep 的托管性能、控制台与使用体验不能自动归到 Graphiti 本身。

### 支持的设置与工程代价

来源所述：README 列出 Python 3.10+、Neo4j、FalkorDB、Amazon Neptune 等后端；Kuzu 驱动当前标记 deprecated。也提供 `falkordblite` 嵌入式可选包，需要 Python 3.12+。这里记录的是上游支持说明，不代表本项目验证了安装组合；不能把“支持图存储”简化成一律需要额外部署重型服务。

README 强调抽取、去重需要可靠的结构化输出，小模型和部分兼容服务可能出现 schema 错误和摄入失败；并提供摄入并发限制。这些是值得纳入研究的实际约束，比只看最终问答分数更接近维护工作。

工程推断：对“谁在什么时候属于哪个项目”“某关系何时生效、何时被取代”“答案需要连通多个人、事件与组织”的任务，图和时间语义有明确的价值假设。代价包含实体消歧、关系抽取、有效时间解释、图维护以及出错后的纠正。

如果关系已经来自可靠业务表，SQL join 与时间字段可以直接回答；如果任务只是按关键词找一条历史记录，带日期的事件表加全文检索也应先进入对照。图的收益需要由真实关系查询支撑，不能由“知识更有结构”这句话替代。

<a id="letta"></a>
## Letta / MemGPT：当前对象已经包含可编辑记忆文件与运行时

来源：

- [旧仓库迁移声明](https://github.com/letta-ai/letta/blob/5bcdd177d70fa2b31a754cfcd801e77b2e1ab16a/README.md)
- [当前 Letta Code README](https://github.com/letta-ai/letta-code/blob/6fa735994a46f1162f7c974ceed2a7fc95d62bb7/README.md)
- [包与运行时要求](https://github.com/letta-ai/letta-code/blob/6fa735994a46f1162f7c974ceed2a7fc95d62bb7/package.json)
- [根 MemFS 提示词样本](https://github.com/letta-ai/letta-code/blob/6fa735994a46f1162f7c974ceed2a7fc95d62bb7/src/agent/prompts/letta_root_memfs.md)
- [记忆整理子 Agent 提示词样本](https://github.com/letta-ai/letta-code/blob/6fa735994a46f1162f7c974ceed2a7fc95d62bb7/src/agent/subagents/builtin/memory-v2.md)

### 先纠正研究对象的版本

旧仓库 README 明确写道：

> “The current source code lives in letta-ai/letta-code.”

并指出 `archive` 分支保存 retired Letta V1 API server。若根据旧教程安排 PostgreSQL 服务端、旧 SDK 和旧记忆 API，再把结果称作“当前 Letta”，会研究错版本。MemGPT 论文、旧 V1 服务端、当前 Letta Code 应分别引用；本次没有读取 MemGPT 论文正文，不以它证明当前实现。

当前 README 描述 Letta Code 为 stateful agent harness，公开入口含 CLI、桌面、App Server、渠道和 SDK。核心可研究机制包括：

- Memory blocks / system prompt learning：通过改写记忆改变后续输入。
- MemFS：把包括 memory blocks 的 context 置于 Git 跟踪之下。
- Message search：查询自己的或其他 Agent 的历史消息。
- Dreaming / sleeptime：周期性处理经验与整理记忆。
- Skills：把程序性知识作为按需使用的材料。

这是上游功能说明，不是对“它能持续改善任务表现”的独立验证。

### 一份提示词样本揭示了什么，不能证明什么

根 MemFS 提示词把 root Markdown 描述为编入 system prompt 的 core memory，把子目录及 skills 等作为外部材料；自动保存的消息历史另作为 recall memory。它还明确写道：

> “Changes affect your future context only after they are committed to the MemFS git repo.”

> “Editing memory does NOT change your behavior in the current turn.”

这支持一个具体的研究点：文件编辑、版本提交、输入重新编译与后续模型行为是不同步骤。提示词还要求保留索引，通过搜索恢复历史，后台子 Agent 可整理记忆。

边界：提示词是可用行为协议的源码证据。本次没有追踪配置选择、完整上下文编译和实际运行轨迹，因此不能声称每个 Letta Agent 默认都运行这份提示词，也不能把提示词要求直接当作已经发生的行为。

### 部署与学习价值

来源所述：当前包名为 `@letta-ai/letta-code`，检查版本为 `0.32.14`，包要求 Node `>=22.19.0`；README 说明通过 npm 安装，`letta server` 支持本地或自托管运行。Letta Cloud 保存代理记忆、身份与对话，并连接不同机器上的 Harness。源码采用 Apache-2.0；Cloud 是另一种服务形态，不能因为客户端开源就声称整个托管系统可完全复刻。

工程推断：Letta 对“Agent 如何主动维护自身记忆、何时整理、如何使改动进入未来输入”的研究价值较高。其集成面是完整代理运行时，和只添加一个记忆搜索库的替换成本不同。值得先拆机制，再决定是否采用整套运行时。

当前材料也直接反驳“文件记忆天然落后于专门框架”的分类方式：这个专门系统本身就在使用可编辑文件、索引和 Git。真正需要比较的是谁维护、如何检索、何时编入输入以及能否改善行为；存储文件与采用框架不是互斥选择。

<a id="langgraph"></a>
## LangGraph Memory：提供状态和存储原语，策略仍需应用设计

来源：

- [框架 README](https://github.com/langchain-ai/langgraph/blob/ed384f3a124660db6dccd6c53eaad48e1457e0b5/README.md)
- [Memory 概念文档固定版](https://github.com/langchain-ai/docs/blob/27bf8560156712b552b138716adcc07b4915ce3c/src/oss/concepts/memory.mdx)，[本次读取的官方页面](https://docs.langchain.com/oss/python/langgraph/memory)
- [添加记忆固定版](https://github.com/langchain-ai/docs/blob/27bf8560156712b552b138716adcc07b4915ce3c/src/oss/langgraph/add-memory.mdx)，[本次读取的官方页面](https://docs.langchain.com/oss/python/langgraph/add-memory)
- [SQLite checkpoint 包](https://github.com/langchain-ai/langgraph/blob/ed384f3a124660db6dccd6c53eaad48e1457e0b5/libs/checkpoint-sqlite/README.md)

### 已核对的事实

概念文档按 recall scope 区分两类：线程内短期记忆属于 graph state，由 checkpointer 持久化；跨线程长期记忆由 store 保存，按自定义 namespace 和 key 组织 JSON 文档。关键短引文是：

> “State is persisted to a database using a checkpointer so the thread can be resumed at any time.”

> “LangGraph stores long-term memories as JSON documents in a store.”

Store 提供内容过滤和可配置语义检索。文档分别讨论单份 profile 与 collection、前台写入与后台写入，示例中由应用代码读取旧指令、生成新指令、调用 `store.put`。所以持久化能力不能等同于已经具有自动提取、冲突处理、失效和经验学习策略。

SQLite checkpoint 包说明：

> “Use it when you want LangGraph state persistence backed by SQLite for local development, testing, or lightweight deployments.”

因此，本地或轻量部署并不天然需要 PostgreSQL 和托管平台。`InMemorySaver` / `InMemoryStore` 的示例也不能被误读为进程重启后的持久化保证；需要依据具体后端判断。

### 学习价值与成本

工程推断：它适合帮助教材拆清“任务恢复”和“跨任务复用”这两个问题。已经采用 graph 执行模型的项目，可以复用 state/checkpointer/store；没有采用该执行模型的简单应用，则没有必要为了保存几个偏好字段先引入完整图编排。

LangGraph 开源框架与 LangSmith 的开发、观测和部署平台应分别评估。README 允许 LangGraph standalone，也说明可不使用 LangChain。这里没有比较托管平台价格或服务质量。

<a id="hindsight"></a>
## Hindsight：事实、后台整理与按需推理需要分开检查

来源：

- [固定 README](https://github.com/vectorize-io/hindsight/blob/63da8d7111566815e34e6b41168f3b3e288d204a/README.md)
- [Retain 机制说明](https://github.com/vectorize-io/hindsight/blob/63da8d7111566815e34e6b41168f3b3e288d204a/hindsight-docs/docs/developer/retain.md)与 [Retain API](https://github.com/vectorize-io/hindsight/blob/63da8d7111566815e34e6b41168f3b3e288d204a/hindsight-docs/docs/developer/api/retain.mdx)
- [Reflect 机制说明](https://github.com/vectorize-io/hindsight/blob/63da8d7111566815e34e6b41168f3b3e288d204a/hindsight-docs/docs/developer/reflect.mdx)
- [API 包](https://github.com/vectorize-io/hindsight/blob/63da8d7111566815e34e6b41168f3b3e288d204a/hindsight-api/pyproject.toml)与 [slim 包依赖](https://github.com/vectorize-io/hindsight/blob/63da8d7111566815e34e6b41168f3b3e288d204a/hindsight-api-slim/pyproject.toml)

### 已核对的接口与派生材料

README 中的三种调用有不同职责：`retain` 通过 LLM 抽取事实、时间、实体和关系，形成规范化表示与索引；`recall` 组合 semantic、keyword、graph、temporal 四路检索，再融合、重排并控制结果 token；`reflect` 根据问题使用记忆推理、返回回答及引用。Reflect 文档明确写道：

> “When you call reflect(), Hindsight runs an agentic loop.”

它可以查询 mental models、observations、事实并补充上下文。这说明 `reflect()` 是按请求组织的推理过程，不能仅凭名字写成“每次后台反思并持久化新记忆”。

后台整理是另一条已文档化路径：retain 完成后异步 consolidation 将事实综合成 observations，保留支持关系。README 的 mental models 则是针对预先定义问题保存的答案，可在后台刷新；读取已经生成的答案是数据库读取，但生成与刷新仍有计算成本。上述均为当前文档所述，未追完执行源码或验证其效果。

Retain API 还区分同步处理与显式异步摄入：

> “When async: true, the call returns immediately with an operation_id.”

这不同于 retain 完成后发生的 observation consolidation。至少应区分请求被接受、事实处理完成、派生认识更新完成三个时点；若只看到请求成功就立即测试长期认识是否更新，可能测到后台进度差异。

一个尤其值得研究的边界来自 Retain 文档：收窄 `retain_mission` 可能使输入不产生任何事实，虽然原文仍被存储，但 recall/reflect 搜索的是 memories，该文档便不能通过这两种操作找到。这里存在“原文保存了，但记忆接口不能找回”的具体例子；后续深拆应核对其来源访问和补救路径。

### 依赖和使用成本

来源所述：MIT 开源，同时提供 Hindsight Cloud。README 提供 Docker、pip、外部 PostgreSQL、嵌入式 pg0 和 Python 封装入口；因此不宜声称试用时必须独立搭建远程数据库。所谓 Python embedded 示例仍启动 `HindsightServer` 并通过客户端访问，只是封装了生命周期，不等于简单的无服务文件读写。

所读包版本 `0.10.0` 要求 Python 3.11+。`hindsight-api` 依赖 `hindsight-api-slim[all]`；slim 的基础依赖包含 FastAPI、数据库驱动、pgvector、多家模型客户端等，`all` 又纳入本地模型、ONNX 与嵌入数据库相关可选包。README 还列出 Oracle AI Database 后端；本次没有验证不同存储与系统组合。

工程推断：它值得作为“较重写入和后台整理，换取不同粒度的未来读取”的案例。应分别测原始事实、observations 和 mental models 的新鲜度、证据损失、写入与刷新代价。若只需重读少量历史或获取精确字段，直接事件表和状态字段仍应作为对照；不能把三 API 的易用性当作背后计算与维护很少的依据。

<a id="langmem"></a>
## LangMem：记忆处理组件与执行器，仍需明确存储和进程边界

来源：

- [固定 README](https://github.com/langchain-ai/langmem/blob/9d033b47d9ce53e37e92c92241b0496c0278932e/README.md)
- [后台处理示例](https://github.com/langchain-ai/langmem/blob/9d033b47d9ce53e37e92c92241b0496c0278932e/docs/docs/background_quickstart.md)
- [延迟处理与执行器](https://github.com/langchain-ai/langmem/blob/9d033b47d9ce53e37e92c92241b0496c0278932e/docs/docs/guides/delayed_processing.md)
- [执行器源码](https://github.com/langchain-ai/langmem/blob/9d033b47d9ce53e37e92c92241b0496c0278932e/src/langmem/reflection.py)
- [包依赖](https://github.com/langchain-ai/langmem/blob/9d033b47d9ce53e37e92c92241b0496c0278932e/pyproject.toml)

### 组件究竟负责什么

README 的直接表述是：

> “functional primitives you can use with any storage system and native integration with LangGraph's storage layer.”

它提供重要信息提取、prompt refinement、记忆管理/搜索工具和后台 memory manager。README 示例把 `create_manage_memory_tool`、`create_search_memory_tool` 交给 Agent，再传入 LangGraph store；Agent 可决定何时使用工具。所谓可接不同存储是功能层的组合能力，不能写成此 Python 包没有 LangGraph 依赖：所读 `pyproject.toml` 中 `langgraph>=0.6.0,<2`、LangChain、Trustcall 和模型客户端均在依赖列表。

文档对示例中的内存存储明确提醒：

> “InMemoryStore keeps memories in process memory—they'll be lost on restart.”

因此，“已接入记忆工具”和“跨进程持久化”需要不同的配置证据。

### 后台处理并非只有一种运行方式

后台 quickstart 的基本示例实际 `await memory_manager.ainvoke(...)` 后才返回回答；该示例不能支持“记忆处理不增加返回延迟”的结论。延迟处理文档另展示 `ReflectionExecutor(...).submit(..., after_seconds=...)`，按线程取消旧任务并推迟处理。

静态读取 `src/langmem/reflection.py` 确认：`LocalReflectionExecutor` 用进程内 `PriorityQueue`、pending tasks 和工作线程；`RemoteReflectionExecutor` 通过 LangGraph 客户端 `runs.create` 提交远程运行。因此 LangMem 确实提供调度辅助，不宜笼统写成“调度完全需要自己从零实现”；但本地执行器也不是跨进程持久任务队列，进程结束后能否继续要依据部署方式判断。

文档对 serverless 场景直接说明本地线程在调用间终止，并给出远程执行器入口。这是具体运行边界，不应扩写成所有项目必须使用托管平台。本次未验证远程服务的恢复语义。

### 研究价值

所读版本为 `0.0.30`，Python 3.10+、MIT。对已经使用 LangGraph 的应用，它有利于分别研究模型主导写入、应用侧后台抽取、延迟合并以及持久化 store 的组合。对尚未使用该技术栈的简单应用，安装一个库也会带入相应依赖和调用模型，需要与几段显式写读代码比较总复杂度。

它适合作为组件组合案例，重点是“谁调用、给哪些历史、产物存哪里、何时能看到”，而不是再增加一种与 Mem0、Letta 完全同层的框架名称。

<a id="selection-implications"></a>
## 对对象选择与教材取舍的有限结论

这是基于以上一手资料的研究判断，不是实测排名。

| 需要解释的问题 | 优先研究的对象或基线 | 要避免的误读 |
|---|---|---|
| 明确字段怎样跨会话延续 | JSON / SQLite 的显式读写 | 有持久化就有自动学习 |
| 大量对话怎样变成可查询记忆 | Mem0 的提取、索引与检索路径 | 托管分数等于 OSS 效果；旧版自动更新等于当前默认 |
| 变化的关系怎样支持历史查询 | Graphiti 的 episode、entity、fact 和时间窗口 | 图数据库本身保证关系与时间正确 |
| Agent 怎样主动改写长期认识与程序性材料 | 固定版本 Letta Code 的 MemFS 与后台整理 | 一份提示词就是全部默认行为；论文与现版软件同构 |
| 任务怎样恢复，跨线程数据怎样保存 | LangGraph state/checkpointer/store | 数据库存储替开发者完成了记忆策略 |
| 预先整理怎样改变未来读取和推理 | Hindsight 的 facts、observations、mental models 与 reflect | reflect 调用等于后台持久化；请求成功等于所有派生材料已更新 |
| 记忆处理怎样组合到已有执行流程 | LangMem tools、manager、local/remote executor 与 store | 内存示例可跨重启；功能可接不同存储等于包没有框架依赖 |

这些对象不是同层替代品，不能排成一个总榜：Mem0 更接近接入层，Graphiti 是时间关系建模与检索框架，Letta 当前包含有记忆的执行环境，LangGraph 提供状态和执行原语，Hindsight 把摄入、综合与读取推理做成系统，LangMem 提供记忆处理和执行辅助组件。一个应用甚至可以组合其中部分机制。

个人初期项目可以从一份显式状态文档、事件日志和可搜索原始历史开始。只有在明确失败上，才增加自动提取、向量索引、时间图或后台整理：例如原文搜索找不到表达不同的相关事件，才有语义检索的需求；多次关系变化无法正确回答“当时是什么”，才有时间建模的需求。这个顺序是为了让新增机制的价值可辨认，不是断言简单方案永远足够。

下一阶段若要形成工程推荐，应分别固定版本、模型、写入范围、检索预算与任务集；至少包含明确更正、时间变化、没有相关记忆和无需记忆也能完成的对照。应同时记录写入成本、读取延迟、维护工作和最终行为变化。本记录尚不足以给出通用胜者。
