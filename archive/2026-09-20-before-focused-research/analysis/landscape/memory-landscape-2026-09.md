> **历史我方调查稿，待逐项复核。** 本文是本项目在 2026-09-19 的调查与推断，不是外部来源，也不代表当前认知。下方旧稿原文完整保留，其中产品能力、数字、来源配对和概念关系尚未逐项复核；引用具体主张前须回到外部原文。
> 2026-09-20 从 sources/reports/ 迁入分析层。项目当前定义见 [领域基础](../../domain/foundations.md)，旧稿备份见 [重建前版本](../../archive/2026-09-20-architecture-review-before/sources/reports/memory-landscape-2026-09.md)。

---

# 《Memory 与上下文工程》教材立项：目标文件深度调研与分析

> 分析对象：`D:\workspace\memory\目标.md`
> 调研时间：2026-09-19
> 方法：对目标文件中列出的全部实体逐项核实 + 对"记忆框架还需要补充"做定向补漏 + 交叉验证理论层与评测层
> 复用：本工作区已有的 22 个来源 / 62 个引用点的前一轮调研（`20260919-201314-e52b6696/`），本轮对其中的错误结论做了修正

---

## 〇、一句话结论

你的目标文件其实已经把教材的**骨架**写对了（"先找共性、把核心思路讲好，再各点深入"），但清单里有 **1 处事实性错误、3 处需要澄清的歧义、1 个结构性缺口**（缺程序性记忆这条线）。这轮调研的价值主要在：

1. **纠错**：`memgit` 不是"找不到"，它是一个真实存在且设计相当完整的独立项目，而且和上一轮调研猜测的 "Letta Context Repositories 别称" 完全不是一回事。
2. **补齐**：纯记忆框架从你列的 6 个扩到 **18 个可讲授的实体**，并按"数据模型"而非"名气"分类。
3. **提炼共性**：把所有系统（含 Claude Code / Pi / Hermes 这类 harness）压到同一套 **"写入—治理—召回—注入—压缩—隔离"六段循环**上，这是教材第一章就该立起来的东西。
4. **挖出教材最硬的一章**：程序性记忆（技能库）是被学术 taxonomy 点名"最高价值、最少工程实现"的一层，而恰恰是 Hermes / Pi / Letta 已经在做的一层——这是你能写出别人写不出来的差异化内容。

---

## 一、目标解读：把 19 行目标拆成 4 个决策

你的目标文件信息密度很高，但隐含了 4 个必须显式拍板的问题，否则写到第三章一定会返工。

| 目标原文 | 解读 | 必须拍板的问题 |
|---|---|---|
| 重点研究方向：harness 工程、上下文工程、memory | 三条线，且是**包含关系**不是并列关系 | 谁是上位概念？建议：**Harness ⊃ Context Engineering ⊃ Memory**。教材主线应该是"从 Harness 视角看上下文，从上下文视角看记忆" |
| 纯记忆框架：mem0 / zep / everOS / memgit？<br>框架的：langchain 及 langmem、openviking 记忆库 | 你已经自觉分了两类：<br>**独立记忆层**（standalone memory layer）vs **框架内嵌记忆**（framework-embedded） | 这个二分是对的，建议直接作为教材第 4 章的分类轴。但还需要第三类：**harness 自带记忆**（Claude Code / OpenClaw / Hermes…），它们在工程上是另一套哲学 |
| 项目自带：codex / claude code / gemini / openclaw / hernes / kimi code / zcode / minimax code / tianshu / pi agent | 10 个编码 Agent，你要的是**它们各自的上下文/记忆机制** | 这些产品的公开资料深度差异极大：Claude Code 有源码级逆向，Pi / Hermes / OpenClaw 有完整设计文档，而 ZCode / MiniMax Code / Kimi Code 只有产品级描述。**教材不能按同一深度写**，需要分"可深挖"与"只做横评"两档 |
| 目标：面向了解 LLM 及 Agent 的进阶教材，重点工程化 + 记忆的深度讲解；先找共性，再各点深入 | 受众锚定清晰（已懂 LLM/Agent）、教学法主张清晰 | 缺一个：**是否要包含可运行代码**。进阶教材 + 工程化定位，强烈建议每章配一个"最小可运行实现"（60~150 行），否则会退化成产品说明书合集 |

**额外提醒一个坑**：你说"面向了解 LLM 及 Agent 的"。这类读者的真实痛点是——他能跑通 RAG，但不知道**记忆和 RAG 的边界在哪**。所以第一章最该回答的不是"记忆是什么"，而是 **"记忆不是什么"**（不是长上下文、不是 RAG、不是向量库）。这一节决定了读者会不会继续读。

---

## 二、清单核实：纠错、澄清、补漏

### 2.1 【纠错】memgit 是真实存在的独立项目，且设计完整度超出预期

上一轮调研的结论是"未找到名为 MemGit 的独立开源记忆框架，最可能是 Letta Context Repositories 的别称"——**这个结论是错的**。

真实情况是"memgit"这个名字下至少有三个不同的东西，其中 **memgit.dev** 才是你大概率听说的那个：

| 项目 | 是什么 | 与教材的关系 |
|---|---|---|
| **memgit.dev**（github.com/code4161/memgit） | 定位 "Git for AI Memory"。本地优先、MIT 开源、SHA-256 内容寻址、自研 TOON 明文格式、`.memgit/objects/`、MCP server + CLI + VS Code 扩展 | **重点讲**。它的设计完整度接近 mem0，且哲学完全不同 |
| xbasset/memgit | 学术向探索：用 Git 管理 LLM 调用的 short-term / working memory，Markdown "episodes" 存于 git tree | 可作为"Git 作为记忆后端"的思路来源提一句 |
| subho004/mem-git-agent | 无状态 LLM→Agent runtime，core-memory 每次编辑记为 reversible diff，支持 `/memory/revert` | 可作为"记忆可回滚"的最小示例 |
| Letta Context Repositories | Letta 生态的 git 版本化记忆，2026-02 发布 | 归到 Letta 条目下，不要和 memgit 混 |

**memgit.dev 值得单独成节的四个设计**（这些在别的框架里都没有）：

1. **类型化记忆 + 优先级**：`fb=feedback / us=user / pj=project / rf=reference / cn=convention / lx=lesson / co=core(项目操作指南) / tr=tracker(实体实时状态)`，优先级 `3=critical(常驻) / 2=default / 1=low`。**这是把"哪些记忆该常驻"从启发式变成了显式 schema**——非常适合进教材。
2. **supersede 而非覆盖**：记忆错了不是改，是存一条 `supersedes=[old-slug]` 的新记忆；被取代的自动停止出现在 search/resume 中，但 `memgit list` 仍可见。**更正即新增版本**，这是冲突消解的一种干净实现。
3. **checkpoint 语义**：`memgit commit -m "what changed and why"` 明确要求"写给未来的 agent 能执行的话"。跨会话历史 = checkpoint 序列。
4. **自我维护闭环**：`core seed` 从项目 skills/rules 蒸馏操作指南并写进各 AI host 的规则文件（`.claude/rules/memgit.md`、`AGENTS.md` 的 marker 块）；`core sync` / `core heal`；sidecar usage ledger 记录哪些记忆真被召回，高频的自动提升为指针，且带预算上限与衰减；`memgit eval` 用冻结集做 recall / 稳定性测量。**"用召回反馈驱动记忆排序"是记忆系统里少见的自我量化机制。**

另外它有一句设计立场非常适合当教材引文：*"不是靠人记得去跑命令的备份不会发生"* → 0.9.0 起会话结束自动备份到已存在的云同步目录，网络出口划为安全边界，绝不自建 remote。**这体现了记忆系统的一个真实工程约束：持久化的敌人是人的惰性。**

### 2.2 【澄清 1】"everOS" = EverMemOS，不是另一个项目

- 官方域名 **evermind.ai**，2025-09-30 首次曝光、2025-11 中旬开源。
- 核心抽象 **MemCell**，形式化为一个四元组 `M = (E, A, F, T)`：
  - `E` Episode：一段叙事摘要（发生了什么）
  - `A` Atomic Facts：离散可验证陈述（便于精确查询）
  - `F` Foresight：**前瞻性推断 + 有效期区间**（"用户明天飞巴黎" → 记录"用户将在巴黎"，带 valid_after / valid_until）
  - `T` Metadata：时间戳、来源、置信度、情绪效价
- 类型体系：MemCell / Episode / Profile / GroupProfile / EventLog / Foresight（从原始到抽象分层，对应人脑工作记忆→情景记忆→他人模型→事实记忆→前瞻记忆）。
- 四条设计支柱：① 分类记忆提取 ② MemCell 原子化存储 ③ **事件边界按主题跨会话切分**（不按 session / token 硬切）④ 多重召回（简单请求快速召回、复杂请求多跳深度召回，类比前额叶+海马体协作）。
- LoCoMo 官方 92.3%，第三方横评可复现 92.32%，是横评中**唯一综合得分超过 LLM Full-context** 的系统，且 token 显著更低。

> `Foresight` 这一维是 EverMemOS 独有的，也是教材里讲"记忆不只是回顾"的最佳例子。**建议在教材中把它单列为"前瞻记忆"类型**，因为主流分类（CoALA 四分法）里根本没有它。

### 2.3 【澄清 2】"tianshu harness" 是社区项目，不是 DeepSeek 官方

- 项目：`github.com/huiliyi37/Tianshu-harness`（天枢），TypeScript，初代号 **Rivet**（CLI 命令名仍叫 `rivet`），TUI + Tauri 桌面端共内核。
- 三大支柱：
  - **CVM（认知虚拟机）**：72 个运行时 hook 横跨 5 大阶段（preTurn / afterPerception / postTool / postTurn / postSession），默认会话激活约 18+。在模型输出与真实动作之间插入可观测、可纠偏的一层，专门拦截服从性漂移、注意力衰减、Doom Loop。
  - **Stigmergy（信息素）自衰减记忆**：**不是 MEMORY.md 那种静态文件，而是把行为足迹和认知标记映射到代码文件上并随时间衰减**——AI 在频繁修改的文件上"越用越熟"。这是非常独特的一招。
  - **前缀缓存引擎**：冻结前缀 + 增量 appendix + Read-ref 去重 + resume 缓存继承，DeepSeek V4 长会话稳态命中率 95–99%。
- 另有：任务契约（TaskContract）钉住全局目标、交付门禁（"完成"必须带运行时证据）、收敛检测、16 个"星域"（认知纪律可切换）。
- **务必与"DeepSeek 官方 Harness（dsh）"区分**：后者是 DeepSeek 内部团队 2026-05 组建、2026-08 开源、MIT、Cordis 微内核"一切皆插件"、230+ workspace 成员。教材里两者都应出现但不该混淆。

### 2.4 【澄清 3】"hernes" = Hermes（Nous Research）

四层记忆（数字以官方文档为准）：

| 层 | 内容 | 加载策略 | 预算 |
|---|---|---|---|
| L1 提示词记忆 | MEMORY.md（项目上下文/踩坑/约定）+ USER.md（用户画像） | 会话开始**冻结快照**注入 system prompt，**修改下次会话才生效** | 两文件合计 **~3,575 字符**硬上限 |
| L2 会话检索 | 全会话写入 SQLite + **FTS5** 全文索引 | Agent 判断需要时才查，命中后先 LLM 摘要再注入 | 10k+ 文档约 10ms |
| L3 技能库 | `~/.hermes/skills/*.md`，含触发条件/步骤/已知坑/验证步骤 | **渐进式披露**：默认只加载名字+简介 | 与技能数量基本无关 |
| L4 用户模型 | Honcho（可选，被动累积偏好） | 可选接入 | — |

- **nudge 机制**：会话中周期性触发，让 Agent 自己回看刚才发生了什么并决定"值不值得持久化"。官方说法很到位：*"记忆不是对话转储，是 Agent 对自己执行的编辑行为"*。
- 压缩：独立 sentinel 触发，辅助模型把值得留的压进字符预算，SQLite 里保留 lineage chain 做溯源。
- 实测对照：12 个历史会话 + 技能，朴素"全量加载" 42.4K/64.0K tokens，**Hermes（检索+摘要）5.5K/64.0K**。
- 代价：技能生成与自我改进带来约 **15–25% 额外 token 开销**（NxCode 独立分析）。

### 2.5 编码 Agent 侧：核实结果汇总

| 项目 | 指令文件 | 压缩 | 隔离 | 记忆/持久化 | 资料深度 |
|---|---|---|---|---|---|
| **Claude Code** | CLAUDE.md 四层作用域（managed policy / user / project / local，~200 行推荐，@path 导入最多 4 跳）；**2.1.277 起支持 AGENTS.md** | **五级梯度**：Snip → MicroCompact（~2000 行截断）→ ApiMicroCompact（Haiku 摘要 + hash 缓存）→ AutoCompact（剩余 <13K 触发，200K 窗口阈值 167K）→ Full Compact（`/compact`，压后重置 50K 预算）。九段式摘要 prompt，熔断 3 次 | Subagent 独立 context window | Session memory（后台增量笔记，实验特性默认关）；压缩后回注最近 5 个文件（各 ≤5K token） | ★★★★★ 源码级 |
| **Codex CLI** | AGENTS.md（**32 KiB 硬上限**，git 根→cwd 每目录一个）；多层级就近优先 | `model_auto_compact_token_limit`（1M 场景配 900000） | Subagents `.codex/agents/*.toml` | **Memories 是独立一层**（v0.119.0 引入，`$CODEX_HOME/memories/`）；`[memory]` 段含 diff_based_forgetting、recency_half_life_days、max_memories_injected、per_project_memory；Chronicle 屏幕记忆（截图→markdown，未加密） | ★★★★☆ |
| **Gemini CLI** | GEMINI.md（可配置为 AGENTS.md）；三层：全局 → 项目（cwd 向上到 .git）→ 子目录 JIT；`@file.md` 导入；`/memory show|reload|add` | 有压缩机制，公开细节少于前两者 | — | 追加到 `~/.gemini/GEMINI.md` | ★★★☆☆ |
| **OpenClaw** | AGENTS.md / SOUL.md / IDENTITY.md / USER.md / TOOLS.md / MEMORY.md / `memory/YYYY-MM-DD.md` / DREAMS.md | Memory Flush：压缩前强制写入（默认 4000 token 或 2MB 触发）；另有 **contextPruning.mode: cache-ttl**（剪枝是临时无损、压缩是永久有损） | **子 Agent 只收到 AGENTS.md + TOOLS.md**，SOUL.md/USER.md 被过滤 | 混合检索（BM25 + 向量）；MEMORY.md 截断上限 20,000 字符；Dreaming 后台提炼；FSRS 保留窗口后归档而非删除 | ★★★★☆ |
| **Hermes** | AGENTS.md（cwd）；prompt 分 stable / context / volatile 三段 | 历史过半即压缩；**压缩后重建前缀以保持缓存温热**；压缩 = 关闭会话 + 开子会话（保留 lineage） | Subagents，父死子死 | 见 2.4 | ★★★★☆ |
| **Pi** | AGENTS.md（global→parents→cwd）；SYSTEM.md 可替换系统提示 | **可替换策略**：默认保留最近约 20,000 token 原文，其余摘要 | 无内置 subagent（需扩展） | **本身不内置长期记忆**，靠 Extension API 实现 | ★★★★☆ |
| **Kimi Code** | AGENTS.md（项目根/子目录/全局 `~/.kimi-code/`，就近优先） | 有会话管理与上下文压缩（细节未公开） | Sub-agents 独立上下文；Agent Swarm（管理器模式，100 Agent 并行，分布式锁/原子操作/异步信号量，双流架构语义流+运行时流） | — | ★★☆☆☆ |
| **ZCode**（智谱，2026-07，1M 上下文） | 支持 `injectAgentsMd` 字段控制子 Agent 是否注入 AGENTS.md | — | 通用型 + 只读 Explore 子 Agent | **Memory：自动提取项目偏好与团队约定，后续会话自动带入**；可编辑历史对话/撤销改动 | ★★☆☆☆ |
| **MiniMax Code** | — | — | — | Session 保存任务可续跑；TUI / Headless(`mcode exec`) / ACP 三模式；BYOK | ★☆☆☆☆（2026-09-18 刚开源 v0.4.12 MIT） |
| **Tianshu** | 统一项目记忆写 `.rivet/knowledge/memory.jsonl`，**自动注入只带治理/约束类，旧问题走显式 recall** | 冻结前缀 + 增量 appendix + 边界压缩 | /scout 只读侦察、/team 并行、/council 多席会诊、/galaxy 多维攻坚 | Stigmergy 信息素自衰减记忆 | ★★★☆☆（README 极详细） |

**一个重要的新发现**：Pi 目前 GitHub **10万+ star，被 OpenClaw 和 MiniMax Code 作为底层 SDK 使用**。这意味着你的清单里 "openclaw / minimax code / pi agent" 不是三个平行产品，而是**有依赖关系的两层**——教材里画架构图时应该体现这一点（Pi 是 harness 内核层，OpenClaw/MiniMax Code 是产品层）。

### 2.6 纯记忆框架：从 6 个补到 18 个

你标注"记忆框架还需要补充"，以下是按**数据模型**分类的完整清单（这是我认为比按名气排序更有讲授价值的分类轴）：

**A. 提取-更新派（extract & update）** — 先 LLM 抽取原子事实，再治理
- **mem0**：混合存储（向量 + 图 + KV）；双 LLM 架构（一个抽取、一个更新/冲突检测）；五维 scope（user_id / agent_id / app_id / run_id / org）；四层记忆（conversation / session / user / organizational）；时序权重衰减。LoCoMo 92.5、LongMemEval 94.4（官方口径）。
  - ⚠️ **注意版本口径冲突**：较新官方文档描述为 **single-pass ADD-only 流水线**——新旧事实都保留，靠检索时的 recency/relevance 排序让新事实浮上来，而非写入时删除。这与其他文档描述的 "UPDATE / DELETE 失效标记" 是**两种不同的演进阶段**。教材引用时必须注明版本。
- **Memobase**：强制 **Topic-SubTopic-Memo** 三级结构；5 阶段流水线（话题提取 → 合并冲突 → 事件记录 → 资料整理 → 再总结）；多语言 prompt（en/zh/ja）；Docker 化。
- **Memary**：Memory Stream（实体 + 时间戳，衡量知识**广度**）+ Entity Knowledge Store（引用频率与最近性，衡量知识**深度**）；递归检索构建最大深度 2 的子图；FalkorDB 多图切换管理不同 Agent 的记忆上下文。

**B. 时序图派（temporal knowledge graph）**
- **Zep / Graphiti**：**双时间模型**（valid time 事件真实发生时间 + transaction time 系统记录时间）；三层子图（Episode 无损原始 → Semantic Entity → Community 标签传播聚类）；**时序边失效**（矛盾时打 `invalid_at`，不删除）；混合检索（cosine + BM25 + BFS 图遍历）+ RRF/MMR/节点距离/episode 提及频率/cross-encoder 重排。115K → 1,600 token。企业版 Graphzilla 用 "context lake" 管大量中等规模图 + 热图内存管理。

**C. 文件系统 / 上下文数据库派**
- **OpenViking**（字节火山引擎，23K★）：`viking://` 虚拟文件系统统一管理记忆/资源/技能；**L0(~100 tok 摘要) / L1(~2000 tok 要点) / L2(全量原文)** 三层按需加载；**目录递归检索**（意图分析 → 多查询 → 定位高分目录 → 目录内二次检索 → 递归下降 → 热度加权）；`session.commit()` 触发 8 类记忆自动提取（profile / cases / preferences / patterns / entities / tools / events / skills），其中 events、cases 只追加，patterns、tools 可合并；检索轨迹完整留存可观测。号称比 OpenClaw 原生记忆省 91% 输入 token。
- **memgit**（见 2.1）：git 语义 + 内容寻址。
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

---

## 三、共性骨架：所有系统其实在解同一道题

这是教材第一章的核心。我建议把它叫做 **"上下文预算模型"**，一句话：

> **模型的能力是固定的，Harness 决定它每一轮看到什么。记忆系统的全部工作，是在一个固定大小的 token 预算里，做一场关于"留下什么"的持续决策。**

### 3.1 第一原理：Context 是预算，不是仓库

支撑这个判断的三个事实：

1. **上下文越长，效果越差**：相关研究显示相关信息被埋在长上下文中时准确率可下降约 24.2%（"lost in the middle"依然存在）。EverMemOS 的横评结论更直接——**精准提取+召回的系统能打败 Full-context**，因为过多上下文引入噪声、稀释注意力。
2. **长上下文不经济**：分层记忆方案 vs 把 80 万 token 历史塞进上下文，推理成本差约 4 倍（即使有 prefix caching）。mem0 数据：全量注入 25,000+ token/查询 vs 分层检索约 6,956。Zep：115K → 1,600。Hermes：42.4K → 5.5K。
3. **注意力预算是有限的**：transformer 每个 token 与所有 token 互算，训练序列长度远短于生产 Agent 实际长度。

**教材表达建议**：开篇不要从"记忆分类"讲起，先给读者看上面三组数字，让他自己得出"必须取舍"的结论，然后再引出取舍的框架。

### 3.2 六段循环：所有记忆系统的最小公分母

无论 mem0 还是 Claude Code，都在跑同一条循环。我建议教材用这个统一模型，然后每个框架只讲"它在哪一段做了什么特别的事"：

```
        ┌─────────────────────────────────────────────┐
        │                                             │
   ① 产生 ──► ② 写入 WRITE ──► ③ 治理 MANAGE ──► ④ 召回 READ ──► ⑤ 注入 INJECT
   (交互/工具结果)   (该不该记?      (去重/冲突/      (向量?BM25?     (常驻?按需?
                     记成什么粒度?    衰减/压缩/归档)   图?目录递归?)     L0/L1/L2?)
                          │                                              │
                          └──────────► ⑥ 侧路：COMPRESS 压缩 / ISOLATE 隔离
```

| 段 | 核心问题 | 代表性实现 |
|---|---|---|
| ① 产生 | 什么算"经验" | 对话、工具结果、文件修改、用户反馈、屏幕（Codex Chronicle） |
| ② 写入 | 值不值得记？记成什么？ | mem0 双 LLM 抽取；EverMemOS MemCell(E,A,F,T)；OpenViking session.commit 提 8 类；memgit 类型+优先级 schema；Memobase 三级结构 |
| ③ 治理 | 重复了？矛盾了？过期了？ | 相似度 >0.95 丢弃、0.7–0.95 交 LLM 判断；Graphiti 时序边失效（`invalid_at`）；memgit supersede；TTL 分层 |
| ④ 召回 | 怎么找到它？ | cosine + BM25 + BFS 三路 + RRF/MMR 重排；OpenViking 目录递归；Hermes SQLite FTS5 |
| ⑤ 注入 | 怎么呈现给模型？ | 常驻冻结快照（Hermes 3,575 字符）；L0/L1/L2（OpenViking）；分层回注（Claude Code 压后回注 5 文件） |
| ⑥ 侧路 | 装不下/怕污染怎么办 | 压缩五级梯度（Claude Code）；subagent 独立窗口；沙箱；namespace 隔离 |

### 3.3 分层：所有系统都是一个"金字塔"，差别只在搬运工

把 mem0、Zep、Letta、Hermes、OpenClaw、Claude Code、OpenViking 摆在一起看，它们的层几乎一一对应：

| 抽象层 | 记忆框架侧 | Harness 侧 | 加载时机 | 典型预算 |
|---|---|---|---|---|
| **常驻层**（永远在 prompt 里） | Letta core memory / Mem0 user memory（部分） | MEMORY.md+USER.md（Hermes）、SOUL/USER/AGENTS/IDENTITY/TOOLS（OpenClaw）、AGENTS.md（Codex） | 每轮强制 | 几百~几千 token，通常有硬上限 |
| **热层**（当前任务） | session / working memory | 当前 messages[] + 最近工具结果 | 每轮 | 窗口的主要部分 |
| **温层**（按需检索） | 向量库 / 图 / FTS5 档案 | memory_search、recall、会话归档检索 | Agent 判断需要时 | 命中后通常先摘要再注入 |
| **冷层**（归档） | 原始事件流水、归档记忆 | 每日日志 `memory/YYYY-MM-DD.md`、session checkpoint、git history | 几乎不主动加载 | 不限 |

**关键洞察（这是教材的点睛之笔）**：

> **决定一个记忆系统好坏的，不是它存了多少，而是"谁来决定什么在常驻层"。**

- mem0 / Zep：**系统决定**（检索排序 + 范围 scope）
- Letta / OpenClaw：**Agent 决定**（工具调用自编辑 / 文件读写）
- Hermes：**Agent 决定，但被字符预算逼着精简**（3,575 字符上限）
- memgit：**人/Agent 用显式优先级决定**（3=critical 常驻）
- Claude Code：**系统决定，但用后台笔记把"摘要"摊到平时**（session memory）

这条对比维度是我建议贯穿全书的**主线之一**，因为它把"记忆框架"和"编码 Agent harness"这两条看似无关的线缝合在了一起。

### 3.4 三大数据模型 × 三种控制策略

数据模型（记忆长什么样）：
- **文本块**（Markdown / JSONL）— 可审计、可 diff、人可读，检索弱
- **向量** — 语义召回强，无关系、无时间
- **图 / 时序图** — 多跳推理 + 时间推理，构建贵

控制策略（谁决定）：
- **启发式**（top-k、固定摘要节奏）
- **提示式自控制**（记忆操作作为工具暴露给模型，MemGPT 开创）
- **学习式**（把 store/retrieve/update/summarize/discard 训成可调用工具，如 AgeMem，三阶段 + step-wise GRPO）

学术层面的共识：**retrieval 相对已经解决，最难、最少解的在 management**（冲突消解、时序推理、选择性遗忘、知识更新）。这句话可以直接作为教材重难点分布的依据。

---

## 四、逐点深入：教材各章应该讲到什么深度

### 4.1 记忆分类学（第 2 章）

给读者两套分类，并说明它们正交：

**A. 认知科学四分法（CoALA 移植）**

| 类型 | Agent 对应 | 存储形态 | 例子 |
|---|---|---|---|
| 工作记忆 Working | 上下文窗口 | 原始 token / 注意力 | 当前对话活跃信息 |
| 情景记忆 Episodic | 对话历史 / 执行轨迹 | 时间索引事件 | 某次具体会话、工具调用记录 |
| 语义记忆 Semantic | 偏好 / 规范 / 提炼事实 | 与时间无关的知识 | "用户偏好 Python" |
| 程序性记忆 Procedural | 工具使用 / 执行模式 | prompt / 策略 / 代码 / 技能文件 | 固化下来的 Skill |

**动态规律必须讲**：情景记忆会随时间**巩固（consolidate）**为语义记忆——一条脱离原始上下文仍有用的事实会从"某次对话"升格为"稳定知识"，原始情景淡出。**这个"层间迁移策略（transition policy）"被综述点名为最关键的架构决策，同时也是工程上最脆弱的一环**（通常只是开发者规则或周期性 LLM 摘要）。

**B. 三轴 taxonomy**（47 位作者《Memory in the Age of AI Agents》，arXiv:2512.13564）

- **Forms 形态**：token-level（上下文里的原始文本）/ parametric（权重里，需重训）/ latent（embedding、hidden state、KV cache）
- **Functions 功能**：factual（稳定知识）/ experiential（发生过什么）/ working（当前任务状态）
- **Dynamics 动态**：formation（形成）/ evolution（演化：更新、巩固、衰减）/ retrieval（检索）

这个 taxonomy 最有价值的产出是**一张覆盖率表**：factual 成熟、experiential 在改善、working 新兴、**procedural 几乎是空白**——"基准影响最大、生产工具最少"的一层。

> **这就是你教材的差异化机会**：程序性记忆在学术界被点名缺失，而 Hermes 的技能库、Pi 的 Skills、Letta 的 skill learning（Terminal-Bench +21.1% / +36.8%）、Codex 的 Skills 层、OpenViking 的 skills 类记忆，全都已经在工程上做了。**你可以写出目前没人系统写过的"程序性记忆工程"一章。**

另外还有两条正交轴要讲：**显式 vs 隐式**（可声明的事实 vs 肌肉记忆式行为模式，多数框架只覆盖显式）、**参数化 vs 非参数化**（MemOS 的 MemCube 是极少见的同时覆盖三种形态的实现）。

### 4.2 写入（第 5 章）

- **决策闸门**：不是所有对话都值得记。生产级做法是 LLM 打分（<5 丢弃 / 5–7 存摘要 / >7 存原文）。
- **操作集合**：ADD / UPDATE / DELETE / NO_OP 四元判定（mem0 single-pass）。
- **粒度**：chunk（MemPalace 逐字）→ 原子事实（mem0 / Memobase）→ 结构化元组（EverMemOS MemCell）→ 事件+前瞻（EverMemOS Foresight）。
- **写前必做**：PII 脱敏（向量可被反演攻击还原，研究显示 32-token chunk 能还原约 90%）。
- **写入时机**：同步（阻塞，体验差）vs 异步后台（推荐）vs **flush 钩子**（OpenClaw Memory Flush：压缩前强制存盘，否则关键指令随压缩丢失）。
- **反面案例（非常适合当教材习题）**：某公司把每轮对话全文 embedding 直灌向量库，3 个月从 10 万条膨胀到 10 亿条，HNSW 索引变深，P99 延迟破 2 秒。

### 4.3 治理（第 6–7 章）

**冲突消解三法**：
1. 相似度阈值：>0.95 直接丢弃，0.7–0.95 交 LLM 判断
2. LLM 合并："喜欢科幻片" + "不太喜欢太空题材" → "喜欢科幻片但不太喜欢太空题材"
3. **版本化 / 双时间**：Graphiti 每条关系带 `valid_at` / `invalid_at`；memgit supersede

**矛盾的四型**：否定矛盾（不用 AWS vs 用 AWS）、时间替代（在 B 公司替代在 A 公司）、值冲突（截止 3/15 vs 2/28）、反义（要详细 vs 要简洁）。

**遗忘五档**（按执行顺序）：原始日志归档 → TTL 过期删除 → 重要性衰减扫描 → 冲突检测与合并 → 容量触发压缩 → 用户发起删除。

**分层 TTL（2026 最佳实践）**：

| 类型 | TTL |
|---|---|
| 不可变事实（过敏、身份） | 无限 |
| 长期偏好（语言、回复风格） | 1 年 |
| 上下文事实（当前项目、近期行程） | 7–30 天 |
| 纯闲聊 | 会话级 |

**时间衰减公式**：`score = sim × exp(-λ × age)`；更进一步的 **Ebbinghaus 曲线**：每次成功召回"强化"记忆延长寿命，不被召回的逐渐淘汰。

**一个反直觉结论要写进去**：激进遗忘能提升整体效果（上下文纯净度提高、注意力集中），代价是极端长程记忆测试分数下降。**"精准的遗忘和精准的记一样重要"**（EverMemOS 横评结论）。

### 4.4 检索（第 8 章）

- 纯语义不够（3 个月前"住北京" vs 2 天前"搬上海"，纯相似可能召回旧的）
- 混合三路：cosine + BM25 + 图 BFS
- 融合：RRF（倒数排名融合）、MMR（多样性）、cross-encoder、节点距离、episode 提及频率
- 时间衰减加权：`final = sim × α + recency × β`（经验值 α=0.7 / β=0.3）
- **非平坦检索**：OpenViking 目录递归——先定位高分目录再精细下钻，解决"平坦向量池"丢失语境的问题
- **索引粒度**：多粒度索引是实用折中
- **查询改写**：原始输入 `x_t` 常常是个糟糕的检索 query
- **检索-否门控**：Self-RAG 式的"要不要检索"判断

### 4.5 注入与呈现（第 9 章）

- **L0/L1/L2 三段式**（OpenViking）：L0 ~100 token 一句话 / L1 ~2000 token 要点 / L2 全量。效果类比：Agent 可以"知道" 1000 件事（L0 全量才 100K token），但只"深入了解"其中几件。
- **字符预算即机制**：Hermes 3,575 字符上限不是限制，是逼迫精选的机制——*"上限不是要绕开的限制，而是让 Agent 工作记忆保持锋利的机制"*。
- **冻结快照**：Hermes 的 MEMORY.md/USER.md 在首条消息前注入，**会话中修改下次才生效**（避免热更新破坏前缀缓存）。
- **压缩后回注**：Claude Code Full Compact 后重新注入最近 5 个文件（各 ≤5K token）、当前任务计划、相关工具 schema——防止压完立刻去重读。
- **只注入治理/约束类**：Tianshu 的自动注入策略，旧问题走显式 recall，不劫持新任务。**这是一条很聪明的原则：常驻层放规则，不放事实。**

### 4.6 压缩（第 10 章）

这是教材最该"深挖"的一章，因为 Claude Code 的五级梯度是目前公开资料里最完整的工程样本：

| 级别 | 机制 | 触发 | 是否调模型 | 是否有损 |
|---|---|---|---|---|
| Snip | 从头部删最旧若干轮 | 兜底 | 否 | 严重有损 |
| MicroCompact | 工具输出超 ~2000 行截断，追加 `[Output truncated: X lines omitted]` | 每轮 / 时间或条数 | 否 | 轻度（日志类可接受） |
| ApiMicroCompact | 超大输出交 Haiku 摘要，磁盘缓存（key=内容 hash） | 复用命中 | 是（一次） | 中度 |
| AutoCompact | Haiku 生成 ≤20K token 九段式结构化摘要替换旧历史 | 剩余 <13K（200K 窗口 → 阈值 167K） | 是 | 中度 |
| Full Compact | 全量压缩 + 回注 | `/compact` 或 ContextCollapse | 是 | — |

**必须讲的几个"只有读过源码才知道"的细节**（这些是教材的价值密度所在）：

1. **阈值不是百分比，是两道减法**：`有效窗口 = 上下文窗口 − min(最大输出, 20000)`；`阈值 = 有效窗口 − 13000`。200K 模型阈值 167K（占有效窗口 ~92.8%，占完整窗口 ~83.5%）；1M 窗口的 Sonnet 5 阈值 967K（~96.7%）。**流传的"92%"说法的分母是有效窗口不是完整窗口**。
2. **cache_edits：热缓存下不能改本地消息**。Anthropic 提示词缓存是前缀缓存，从中间删一块会导致删除点之后全部失效、下轮全价重算。解法是客户端不改本地 prefix，而是发 `cache_reference` + 一组 `cache_edits` 删除指令，由服务端在自己缓存副本上执行，保住九折折扣。代价是删除指令要 pin 在原位每轮重发。
3. **冷/热两条路径**：缓存凉了（时间间隔触发）→ 直接改写本地消息整块替换为 `[Old tool result content cleared]`；缓存还热（条数触发）→ 走 cache_edits 只发删除指令。
4. **只清幂等可重取的工具**：FileRead / Bash / Grep / Glob / WebSearch / WebFetch / FileEdit / FileWrite。Agent 工具与 MCP 工具结果一律不碰（无法判断是否可重取）。
5. **只在主线程执行**：fork 出去的 subagent 与主线共享前缀，主线先擦会导致 subagent cache break，要等汇合后统一清理。
6. **think block 也砍**：历史轮次的 extended thinking 只留最近一轮（单块几千 token 且不享受缓存折扣，结论已写在同轮正文里）。
7. **session memory：把摘要摊到后台**。对话每涨约 5,000 token 或跑 3 次工具调用，就 fork 一个严格受限的模型子调用，把新增段归纳进固定栏目的 Markdown 笔记（标题/当前进展/任务说明/涉及文件函数/常用命令/错误与纠正/系统组件/经验/关键结果/工作流水），总量约 1.2 万 token、每栏约 2,000 token。**压缩那一刻零 LLM**——直接拿笔记 + 游标之后的近期消息拼接。目前仍是实验特性、默认关闭。
8. **切割点不能随意**：保留区里若有 tool_result，必须连其 tool_use 一起保留；共享同一 message.id 的 thinking 片段不能切掉。
9. **三道闸**：熔断（连续失败 3 次停手，源码注释提到曾有 1,279 个会话连续失败 50+ 次，全球每天浪费约 25 万次 API 调用）、递归守卫（压缩里不再压缩）、静默失败（失败只返回 `wasCompacted: false`，不打断操作）。
10. **九段式摘要 prompt**：主要诉求与意图 / 关键技术概念 / 文件与代码片段 / 报错与修复 / 问题排查 / **所有非工具结果的用户消息（逐字保留）** / 待办任务 / 当前工作 / 可选下一步（附逐字引用防意图漂移）。

**对照组**（让教材有横向参照）：
- **DeepSeek Harness**：两级压缩——一级单工具结果截断（不调模型），二级对话摘要在 80% 触发或错误补救触发，**最近 16% 不动**；只追加会话日志为唯一真源；300K–400K token 主动结束会话。
- **Hermes**：历史过半即压缩，**压缩后重建前缀保持缓存温热**，压缩 = 关会话 + 开子会话（保留 lineage 而非重写成一个 blob）。
- **Pi**：保留最近约 20,000 token 原文，其余摘要；**压缩是可替换策略**（可自己实现）。
- **OpenClaw**：区分**剪枝（临时、无损，隐藏旧工具结果）** 与 **压缩（永久、有损，重写历史）**，用 `contextPruning.mode: cache-ttl` 让剪枝先顶上，尽量不让压缩触发。这个二分法本身就很值得讲。

### 4.7 隔离（第 11 章）

- Subagent 独立窗口，父只拿 1,000–2,000 token 摘要（Anthropic 多 Agent researcher：子 Agent 消耗约 15 倍 token，但只回传 1–2K 摘要）
- **OpenClaw 的过滤器是个好例子**：子 Agent 只收到 AGENTS.md + TOOLS.md，SOUL.md / USER.md 被过滤掉 → **硬规则必须写在 AGENTS.md 里才能触达子 Agent**
- 沙箱：Pi 提供 Gondolin 扩展（内置工具路由到微 VM）/ Plain Docker / OpenShell 三种
- Namespace 隔离失效 = 安全事故（某投顾 Agent 因共用 vector collection 把 A 的偏好写成 B 的）——**记忆串用户是安全事故，不是 bug**
- 多 Agent 记忆共享三态：private / shared / federated，规模上 federated + 显式请求更稳

### 4.8 程序性记忆（第 12 章 —— 差异化章节）

- **为什么重要**：Voyager 有技能库 vs 无技能库，tech-tree 里程碑速度差 **15.3 倍**；Reflexion 用语言化自我批评记忆，HumanEval pass@1 从 80% → 91%；Letta 技能学习带来 Terminal-Bench +21.1% / +36.8%。
- **工程形态**：Hermes `~/.hermes/skills/*.md`（触发条件/步骤/已知坑/验证步骤，渐进式披露，200 个技能与 40 个技能的上下文开销差不多）；Pi Skills；OpenViking 的 skills 类记忆；Codex 七层扩展点里的 Skills。
- **代价**：技能生成与自我改进带来约 15–25% 额外 token 开销；Hermes 明确不是权重微调——*"在任务层面说'自我改进'是准确的，在模型层面就是误导"*。这句话应该原样放进教材。
- **风险**：自我强化错误——一个错误结论（"API X 用参数 Y 必然失败"）会永久阻断证据收集，危害随 Agent 生命周期放大。缓解手段是 **reflection grounding**：要求引用到具体情景证据，提供可审计性（但不保证代表性）。

### 4.9 缓存友好（第 13 章 —— 另一个差异化章节）

这是"工程化"定位下最实在的一章，而且几乎没人系统写：

- Pi + DeepSeek V4 Flash：近 10 亿输入 token，**缓存命中率 99.93%**，花费 $2.65；不走缓存同量预估 $132（**约 50 倍**）。10 亿 token 走缓存约 $19 vs 不走 $900+。
- Composio 横评：同一模型下换 harness，**单成功任务成本差最高 7 倍**（Pi $0.028 vs Claude Code $0.195）。
- Tianshu：冻结前缀 + 增量 appendix + Read-ref 去重 + resume 缓存继承，稳态 95–99%。
- **缓存友好的设计纪律**（可从上面反推出来，是很好的教材产出）：
  1. 系统提示词与工具定义**冻结**，极少变动
  2. 内容**只向后追加**，不回头改前缀
  3. 工具集**默认最小**（Pi 4 个工具，system prompt + 工具定义 <1000 token）
  4. 动态信息放**尾部**（volatile 段：memory 快照、profile、时间戳）
  5. 压缩后**重建前缀**使其尽快重新温热（Hermes）
  6. 需要删除时用 **cache_edits** 而非改写本地消息（Claude Code）
- **权衡要说清楚**：缓存友好要求"稳定"，上下文新鲜要求"动态"，二者天然冲突。Pi 的解法是把控制权交出去；Claude Code 的解法是用 cache_edits 精确手术。

---

## 五、教材大纲建议（可直接用的目录）

```
序章：为什么 2026 年 Agent 的瓶颈是记忆，不是模型
  · 三组数字：成本（4×/7×/25K vs 7K）、效果（lost in the middle 24.2%）、延迟（115K→1.6K）
  · 记忆不是什么：不是长上下文、不是 RAG、不是向量库

第一篇  第一原理（共性）
  1. 上下文预算模型：Context is a budget, not a warehouse
  2. 记忆分类学：CoALA 四分法 / 三轴 taxonomy / 参数化 vs 非参数化
  3. 六段循环：产生—写入—治理—召回—注入—（压缩/隔离）
  4. 分层金字塔：常驻/热/温/冷，以及"谁来搬运"这条主线

第二篇  逐点深入：记忆的六个环节
  5. 写入 Formation
  6. 治理 Evolution（上）：去重与冲突消解
  7. 治理 Evolution（下）：遗忘、衰减、TTL
  8. 检索 Retrieval：混合检索与融合排序
  9. 注入 Injection：L0/L1/L2 与常驻预算
  10. 压缩 Compression：五级梯度与源码级拆解
  11. 隔离 Isolation：subagent、沙箱、namespace

第三篇  两种实现路线
  12. 独立记忆层：mem0 / Zep·Graphiti / EverMemOS / Letta / Cognee / Memobase / OpenViking / memgit
  13. 框架内嵌记忆：LangMem 三类记忆与 procedural 自我改写
  14. Harness 自带记忆：Claude Code / Codex / Gemini CLI / OpenClaw / Hermes / Pi / Tianshu / Kimi / ZCode
  15. 程序性记忆：技能库——被学术界点名缺失、被工程界悄悄做掉的一层
  16. 缓存友好设计：把 50 倍成本差拆成 6 条纪律

第四篇  工程落地
  17. 从零搭一个记忆层：四表最小架构（events / memory_items / checkpoints / retrieval_index）
  18. 记忆的失败模式与可观测性
  19. 合规与安全：PII 脱敏、被遗忘权、namespace 隔离
  20. 评测：LongMemEval / LoCoMo / BEAM 怎么读，以及为什么不该信

第五篇  前沿
  21. 层间迁移策略（transition policy）：情景 → 语义 → 程序性
  22. 学习式记忆管理（RL 训 store/retrieve/update/discard）
  23. 参数化记忆与 MemCube 三形态统一
  24. 多 Agent 记忆：private / shared / federated
```

**每章固定三件套**（建议）：① 机制讲解 ② 一个真实系统的源码/文档级剖析 ③ 一个 60–150 行的最小可运行实现或"如果你来设计会怎么做"的决策练习。

---

## 六、必须写进教材的一章：评测为什么不可信

这一章会让你的教材显得有判断力，而不是资料汇编。目前公开基准的问题已经被相当系统地揭露：

1. **Ground truth 有错**：Penfield Labs 审计 LoCoMo 发现 1,540 题中有 99 处会污染分数的错误（6.4%），**理论上限制定了约 93.6%**——高于这个数的分数在没有"错答案错得刚好"的情况下数学上不可能。
2. **Judge 太宽松**：标准 LoCoMo judge（GPT-4o-mini + 原 prompt）在压力测试中接受了 **62.81%** 的"故意答错但主题沾边"的答案。而这恰恰是弱检索的典型失败模式，基准在奖励它。
3. **厂商各自跑自己的管线**：Mem0 vs Zep 公开吵架——Zep 发文称反超 Mem0 24%，被 Mem0 CTO 抓出算术错误（分子含 Category 5、分母不含）后悄悄改为 10%（75.14% vs ~68%）。Letta 随后用**纯文件系统 + grep、根本不用记忆系统**报了 74.0%，把两边都打了。
4. **提示词调优痕迹可查**：有第三方审计指出 mem0 的 benchmark prompt 文件里含 **14 条与具体 question_id 一一对应的等价规则**、隐藏 CoT 块（judge 只看清洗后的答案）、judge prompt 里的 "lean toward yes" 指令，以及只在判 WRONG 时才有 5 步关卡的不对称设计。同一系统同一数据，厂商口径 93.4%，第三方标准化复现 73.8%（且承认 4/14 更新后确实从 57.5% 涨到 73.8%，是真实进步）。
5. **基准太短**：LoCoMo / LongMemEval 的规模**能舒服地塞进前沿模型的上下文窗口**，所以它们测的到底是"记忆系统"还是"长窗口 needle-in-haystack"一直有争议。
6. **病毒式项目**：MemPalace 首发宣称 LoCoMo 100%、LongMemEval 首个满分，48 小时 23K star；在 19–32 条的池子上设 `top_k=50` 不构成有效检索测试，后被社区压力修正；独立评测称开 AAAK 压缩后真实准确率降到 84.2%。

**给读者的可操作建议**（这一节的产出）：忽略公开分数，用自己的数据跑三个基线——**Full-context 基线、文件系统搜索基线、目标记忆系统**；审计 ground truth；要求多种子；要求公开 judge prompt。*"不肯公开 judge prompt 和 eval harness 的分数，在任何意义上都不存在。"*

**基准的正确读法**（可作为教材的方法论输出）：
- **成对读**：准确率配 token 成本；单会话分配多会话；上下文探针配记忆评测
- **新一代基准已经在改**：LoCoMo-Refined（1,382 题，修订 337 题，官方 judge Qwen3-14B，人类一致率从 43.67% → 86.33%，原则"包含且不矛盾、完整且不越界"）；LongMemEval-V2（451 题，多模态 web-agent 轨迹，最多 500 条轨迹、最大 1.15 亿 token，**准确率与延迟联合评分 LAFS**，测静态状态召回/动态状态追踪/工作流知识/环境陷阱/前提意识五项，其中四项关乎累积经验而非一次性查找）；BEAM（1M / 10M token 规模，十项能力，设计上就是不让任何现有架构饱和——最强系统在 BEAM-1M 只有 64.1、BEAM-10M 48.6）。

---

## 七、风险与不确定性（写作时必须标注）

| 项 | 风险 | 处理建议 |
|---|---|---|
| 所有基准分数 | 系统性不可信（见 §6） | 教材中引用一律标注"厂商口径 / 第三方复现 / 评测配置"，并给出不可信清单 |
| mem0 架构描述 | 官方文档前后不一致（ADD-only vs UPDATE/DELETE） | 注明版本号，或两者都讲并标注为"两个演进阶段" |
| LangMem p95 延迟 59.82s | 疑似特定基准配置，非通用表现 | 不引用，或明确标注前提 |
| Letta 仓库 | 主分支 2026-08-15 移除 V1 server，代码在 `letta-code` | 代码引用指向 `letta-code` |
| ZCode / MiniMax Code / Kimi Code | 只有产品级公开资料，无源码级机制 | 教材中降级为"横评表一行"，不要伪造成深度剖析 |
| MiniMax Code | 2026-09-18 刚开源 v0.4.12，变化会很快 | 标注"截至 2026-09" |
| Pi star 数 | 不同来源 8.6 万 / 10 万+ | 写"~10 万（2026 年中）"并注明来源分歧 |
| 二手中文源 | 部分细节（如某些字符上限）来自中文技术博客转述 | 涉及数字的关键结论尽量回到官方 README / 源码 |
| 领域速度 | 这一领域按月变化 | **教材重心放在"机制层"而非"产品层"**——机制（预算模型、六段循环、治理动作）三年内不会过时，产品名会 |

---

## 八、建议的下一步（按优先级）

1. **先写第 1 章（上下文预算模型）+ 第 10 章（压缩）**——这两章最能验证你的教材定位是否成立，也最能体现"工程化"与市面上已有资料的差异。
2. **建立一手核实清单**：把 mem0 / Zep / EverMemOS / OpenViking / memgit / Letta-code / Pi / Hermes / Tianshu 的官方 README 与关键源码文件拉下来存档（这轮调研已经覆盖了大部分，但需要落到本地作为写作时的事实底座）。
3. **补两个空白**：Kimi Code / ZCode / MiniMax Code 的上下文机制（目前只能靠产品文档）；以及 DeepSeek 官方 harness（dsh）的源码级机制——这两块如果要写深，需要额外的动手验证。
4. **确定"最小可运行实现"的技术栈**：建议 TypeScript（Pi / Tianshu 生态，且你列的项目里 TS 占多数）或 Python（mem0 / LangMem 生态）。这决定了每章的配套代码。
5. **程序性记忆那一章尽早动手**——这是唯一的空白带，拖延会被别人填上。

---

## 附：本轮调研主要来源

**官方文档 / 源码**
- memgit: memgit.dev、github.com/code4161/memgit
- EverMemOS: docs.evermind.ai/cloud/concepts/memcell
- OpenViking: volcengine.com/docs/84313/2374478、github.com/volcengine/OpenViking
- Tianshu-harness: github.com/huiliyi37/Tianshu-harness
- Graphiti: github.com/getzep/graphiti、Zep 451Research 报告
- LangMem: blog.langchain.com/langmem-sdk-launch
- mem0: mem0.ai/blog、mem0.ai/research
- Letta: letta.com、agent-memory-atlas（源码级，含 2026-08-15 主分支变更记录）

**源码级逆向 / 深度剖析**
- claude-wiki.com/auto-compact.html、deepwiki 的 Compact System 四层架构
- threadnavigator.com（Pi 与 Hermes 的 loop 对比）
- neoneye.github.io/agent-memory-atlas（Letta / mem0 等逐仓库机制标注）

**理论与评测**
- 《Memory in the Age of AI Agents》（arXiv:2512.13564，47 作者 taxonomy）
- 《Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers》（arXiv 2603.07670，write-manage-read 循环 + 3D taxonomy）
- ar5iv.org/html/2607.16848（Beyond Memory Leaderboards，含 Generative Agents / MemGPT / 十种机制家族综述）
- LoCoMo_refined: github.com/mem-eval-suite/LoCoMo_refined
- maximem.ai/blog/state-of-ai-memory-2026-claimed-vs-observed（厂商口径 vs 复现）
- essays.bloo-mind.ai（Benchmark Theatre）
- mem0.ai/blog/ai-memory-benchmarks-in-2026（LoCoMo / LongMemEval / BEAM 对照）

**中文技术社区（二手，用于交叉验证）**
- 腾讯云开发者社区多篇（上下文工程简史、Harness 六大组件、DeepSeek Harness）
- 掘金 / 微信公众号多篇（Claude Code 压缩机制、Hermes 记忆架构、OpenClaw 记忆系统）
- 51CTO / CSDN 多篇（记忆分层与落地实践、写入/遗忘策略）
