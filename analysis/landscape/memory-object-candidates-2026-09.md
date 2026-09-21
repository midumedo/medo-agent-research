# 候选对象与记忆框架清单

> **用户提供的研究输入笔记，正文逐字保留。** 2026-09-21 从 `sources/以前的/pass.md` 迁入分析层；同时移除了 `.gitignore` 中把它当作私人文件排除的规则——本轮确认它是研究者输入的候选清单，不是外部来源，也不是私人文件。
>
> 下列项目、版本号、星级与基准分数**尚未逐项核实**，写入时间也不统一。引用任何具体主张前须回到外部原文。本文件的分类轴（按数据模型分组）独立于 [Memory 工程选择](../memory-engineering-selection.md) 与[记忆横评对照](../memory-benchmark-crossreview-2026-09.md) 的判断，后两者不继承这里的主张。
>
> 原文正文从下方标题起至文件末尾，与迁移前的文件逐字节一致（SHA256 900295cfb244 …）。

---

# 重点研究方向

harness engineering，congtext engineering，memory

# agent参考项目

## coding agent

主要：codex，claude code（无源码，只有之前泄露的），tianshu-harness(https://github.com/huiliyi37/Tianshu-harness)

补充：minimax（https://github.com/MiniMax-AI/cli），kimi-code（https://github.com/MoonshotAI/kimi-code），gimini（https://github.com/google-gemini/gemini-cli），zcode（据说未来会开源），workbuddy 

## ai projects

openclaw，hermes，prime agent，raven（https://github.com/EverMind-AI/Raven）

补充：manus

## 框架

langchain系列（langchain，langgraph，langmem），pi

openviking那个不知道该不该放进这里

deepseek harness（https://github.com/deepseek-ai/deepseek-harness，太开放了，还是先放这里吧）

# 纯记忆框架

以下是按**数据模型**分类的完整清单（这是我认为比按名气排序更有讲授价值的分类轴）：

**A. 提取-更新派（extract & update）** — 先 LLM 抽取原子事实，再治理
- **mem0**：混合存储（向量 + 图 + KV）；双 LLM 架构（一个抽取、一个更新/冲突检测）；五维 scope（user_id / agent_id / app_id / run_id / org）；四层记忆（conversation / session / user / organizational）；时序权重衰减。LoCoMo 92.5、LongMemEval 94.4（官方口径）。
  - ⚠️ **注意版本口径冲突**：较新官方文档描述为 **single-pass ADD-only 流水线**——新旧事实都保留，靠检索时的 recency/relevance 排序让新事实浮上来，而非写入时删除。这与其他文档描述的 "UPDATE / DELETE 失效标记" 是**两种不同的演进阶段**。教材引用时必须注明版本。
- **Memobase**：强制 **Topic-SubTopic-Memo** 三级结构；5 阶段流水线（话题提取 → 合并冲突 → 事件记录 → 资料整理 → 再总结）；多语言 prompt（en/zh/ja）；Docker 化。
- **Memary**：Memory Stream（实体 + 时间戳，衡量知识**广度**）+ Entity Knowledge Store（引用频率与最近性，衡量知识**深度**）；递归检索构建最大深度 2 的子图；FalkorDB 多图切换管理不同 Agent 的记忆上下文。

**B. 时序图派（temporal knowledge graph）**
- **Zep / Graphiti**：**双时间模型**（valid time 事件真实发生时间 + transaction time 系统记录时间）；三层子图（Episode 无损原始 → Semantic Entity → Community 标签传播聚类）；**时序边失效**（矛盾时打 `invalid_at`，不删除）；混合检索（cosine + BM25 + BFS 图遍历）+ RRF/MMR/节点距离/episode 提及频率/cross-encoder 重排。115K → 1,600 token。企业版 Graphzilla 用 "context lake" 管大量中等规模图 + 热图内存管理。

**C. 文件系统 / 上下文数据库派**
- **OpenViking**（字节火山引擎，23K★）：`viking://` 虚拟文件系统统一管理记忆/资源/技能；**L0(~100 tok 摘要) / L1(~2000 tok 要点) / L2(全量原文)** 三层按需加载；**目录递归检索**（意图分析 → 多查询 → 定位高分目录 → 目录内二次检索 → 递归下降 → 热度加权）；`session.commit()` 触发 8 类记忆自动提取（profile / cases / preferences / patterns / entities / tools / events / skills），其中 events、cases 只追加，patterns、tools 可合并；检索轨迹完整留存可观测。号称比 OpenClaw 原生记忆省 91% 输入 token。
- **MemU**：结构化记忆树（根/枝/叶自动分类，权重检索）；面向 24/7 主动 Agent。
- **MemPalace**：记忆宫殿五层空间隐喻（Wings→Halls→Rooms→Tunnels→Drawers），**逐字存储不做摘要**，ChromaDB + SQLite，纯本地零 API 成本。⚠️ 其 LongMemEval 96.6% / LoCoMo 100% 的说法有争议（见 §6），教材引用要谨慎。

**D. 操作系统 / 认知架构派**
- **Letta（原 MemGPT）**：核心记忆（常驻块，Agent 用工具自编辑）/ 召回记忆（可检索对话史）/ 归档记忆（向量冷存）；上下文将满时收到"你快没上下文了"的系统消息，由 Agent 决策换页；sleep-time compute；Context Repositories（git 版本化记忆）。
  - ⚠️ **重要变更**：`letta-ai/letta` 主分支在 **2026-08-15 移除了 V1 API server（约 36.7 万行）**，当前开发在 `letta-code`。教材若要讲代码，必须指向正确的仓库，否则会失效。
- **MemOS**：MemCube 统一管理**明文记忆 / 激活记忆（KV）/ 参数记忆**三种形态——它是极少数真正覆盖"参数化记忆"的工程实现。
- **EverMemOS**：见 2.2。
- **Cognee**：模块化 **ECL 管道**（Extract 提取 → Cognify 认知 → Load 加载），向量 + 图双写，38+ 数据格式。

**E. 框架内嵌派**
- **LangMem**（LangChain）：三类记忆 **semantic（事实）/ episodic（经历）/ procedural（系统提示词自我改写）**；两种集成模式（热路径工具 vs 后台 memory manager）；namespace 隔离（user_id / team_id / app_id）；后台 consolidation 防膨胀。
  - **procedural memory 是它最独特的能力**：Agent 根据反馈改自己的 system prompt。这是教材"程序性记忆"章节的必引案例。
  - ⚠️ 有评测称其 p95 检索延迟约 59.82 秒——这个数字大概率是特定基准配置下的结果，**教材引用必须标注前提**，否则会误导读者以为 LangMem 慢到不可用。
- **memg-core**：MEMG 的确定性 schema 驱动引擎，YAML 定义记忆类型，Qdrant（向量）+ Kuzu（图）双后端，带审计日志与自管理记忆循环。

**F. 其他值得提一句的**
- Supermemory（Memory+RAG 双引擎，sub-300ms 召回）、SimpleMem（三步式终身记忆）、TencentDB Agent Memory（团队级记忆中枢）、Hindsight、agentmemory（12 hooks + MCP 的 Claude Code 插件形态）。

- MemoryBear 应该是属于时序图？

- memgit请删掉。无需关注


# 另一个集合
MemU, OpenViking, Cognee, Supermemory, Hindsight, Letta, LangMem, Memopalace, agentmemory, MemoraX, InvMem, ReFind, ActiveMemoryIndex, Maximem Synap, AgentOS, Memori (2603.19935?), Tencent Cloud Agent Memory, NTES-MEMORY-SMART, Redis Agent Memory Server, Mastra (observational memory), HippoRAG2, GraphRAG, MemoRAG, MemAgent, MEM1, Nemori, MemoryBearNow let me also read the local papers2512.13564's benchmark table (line ~1638-1730) and framework table — these give me the survey's curated list. Let me read those lines.