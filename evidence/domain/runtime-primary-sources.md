# Agent 运行主题的一手资料记录

访问日期：2026-09-20。以下页面均已实际读取；记录短摘录、来源位置及本主题采用的解释范围。官方文档描述接口或工程实践，本项目未据此声称完成源码深拆、验证部署默认值或复现实验。网页可继续变化，访问日期不等于固定产品版本。

<a id="anthropic-context"></a>

## Anthropic：Context 选择与执行中的检索

来源：[Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)，页面标注 2025-09-29；位置为开头、Context engineering vs. prompt engineering、Context retrieval and agentic search、Structured note-taking。

> “Context refers to the set of tokens included when sampling from a large-language model (LLM).”

> “the curation phase happens each time we decide what to pass to the model.”

> “agents built with the ‘just in time’ approach maintain lightweight identifiers (file paths, stored queries, web links, etc.) and use these references to dynamically load data into context at runtime using tools.”

> “the agent regularly writes notes persisted to memory outside of the context window. These notes get pulled back into the context window at later times.”

支持：Context 与每次采样的信息选择相关；检索可以发生在执行中；外部笔记需要之后重新进入输入才能沿这条路径影响模型。指针不等于内容已被读取，笔记不等于总会正确使用。文章属于厂商的工程解释，不把注意力预算等比喻直接当作统一性能定律或固定长度阈值。

<a id="anthropic-agents"></a>

## Anthropic：工作流、动态控制与环境反馈

来源：[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)，页面标注 2024-12-19；当前页面已提示工具生态变化，读取的是当前正文。位置为 What are agents?、Agents、Combining and customizing these patterns。

> “Workflows are systems where LLMs and tools are orchestrated through predefined code paths.”

> “Agents, on the other hand, are systems where LLMs dynamically direct their own processes and tool usage”

> “Agents can then pause for human feedback at checkpoints or when encountering blockers.”

> “These building blocks aren't prescriptive. They're common patterns that developers can shape and combine to fit different use cases.”

该文还强调以工具结果、代码执行等环境反馈评估进展。支持：控制可以固定、动态或组合，暂停与继续属于运行行为。来源用 ground truth 描述环境反馈；本项目采用更有限的“观测”，因为工具也可能失败或只覆盖局部。文中的 agent/workflow 区分不是行业唯一命名，也不证明多 Agent 普遍更优。

<a id="langchain-memory"></a>

## LangChain：任务状态、记忆范围与写入时机

来源：[Memory overview](https://docs.langchain.com/oss/python/concepts/memory)，实际读取 [Markdown](https://docs.langchain.com/oss/python/concepts/memory.md)。位置为 Short-term memory、Long-term memory、Writing memories、In the background。

> “This state can normally include the conversation history along with other stateful data, such as uploaded files, retrieved documents, or generated artifacts.”

> “Unlike short-term memory, which is thread-scoped, long-term memory is saved within custom ‘namespaces.’”

> “There are two primary methods for agents to write memories: ‘in the hot path’ and ‘in the background’.”

> “infrequent updates may leave other threads without new context.”

支持：消息历史可为应用状态的一部分，状态范围可能更大；按线程划分和按写入时机划分是不同维度。主路径和后台形成各有可见性与开销问题。此处短期／长期是该框架的定义，不推广成统一时间阈值；后台写入移出关键路径，不等于没有系统成本。

<a id="langgraph-persistence"></a>

## LangGraph：检查点与跨线程数据

来源：[Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)，实际读取 [Markdown](https://docs.langchain.com/oss/python/langgraph/persistence.md)。访问旧 durable-execution.md 时已重定向到此页面。位置为开头、Checkpointer vs. store、MemorySaver does not persist between restarts。

> “Checkpointers persist a thread's graph state as checkpoints.”

> “Stores persist application-defined data outside the graph state.”

> “MemorySaver and InMemorySaver store checkpoints in RAM. When the process restarts, all checkpoints are lost.”

支持：执行恢复状态与跨任务复用信息可以有不同保存机制，接口名不保证后端持久化。该文是具体框架说明，不要求所有系统实现同名模块，也不证明外部世界包含在图状态内。

<a id="langgraph-checkpointers"></a>

## LangGraph：恢复、重放与修订

来源：[Checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers)，实际读取 [Markdown](https://docs.langchain.com/oss/python/langgraph/checkpointers.md)。位置为开头、StateSnapshot fields、Replay、Update state、Durability modes。

> “A checkpointer saves a snapshot of graph state at each super-step, organized into threads.”

> “Nodes after the checkpoint re-execute, including any LLM calls, API requests, or interrupts — which are always re-triggered during replay.”

> “This creates a new checkpoint with the updated values — it does not modify the original checkpoint.”

页面中的 StateSnapshot 还含 values、next、metadata、tasks 等字段，durability 有不同保存时机。支持：状态包含控制位置，重放有明确执行语义，修订不必覆盖原记录。由此作出的工程推断是：恢复图状态不能单独保证外部动作回滚。重放与故障恢复需区分，不能说每次恢复都会重做全部工具。

<a id="openai-tools"></a>

## OpenAI：模型的工具请求与应用执行

来源：[Function calling](https://developers.openai.com/api/docs/guides/function-calling)，位置为 The tool calling flow。

> “Tool calling is a multi-step conversation between your application and a model via the OpenAI API.”

页面列出的相关步骤包括：

> “Receive a tool call from the model”
> “Execute code on the application side with input from the tool call”
> “Make a second request to the model with the tool output”
> “Receive a final response from the model (or more tool calls)”

支持：对这里的应用函数调用，模型请求、应用执行、返回结果和后续采样是不同事件。工具输出需要对应调用标识；具体协议也可能含必须续传的非文本项。本主题不据此假定所有工具都在本地客户端执行；托管工具仍需区分请求、执行和结果。

<a id="openai-state"></a>

## OpenAI：请求载荷与会话状态

来源：[Conversation state](https://developers.openai.com/api/docs/guides/conversation-state)，位置为 Conversations API、Passing context from the previous response、Managing the context window。

> “Conversations store items, which can be messages, tool calls, tool outputs, and other data.”

> “Another way to manage conversation state is to share context across generated responses with the previous_response_id parameter.”

页面还展示应用自行维护历史，并说明上下文窗口的容量口径涉及输入、输出及相应模型的推理 token。支持：请求体可使用续接标识，客户端省去重复传输不等于历史没有参与后续请求；Conversation、实际输入与窗口容量要区分。当前主题不复述具体型号价格、限额或默认保留时长，也没有核验实际请求轨迹。
