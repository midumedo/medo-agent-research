# **面向自主代码智能体的仓储上下文工程：拓扑架构、生命周期治理与确定性沙箱规范**

## **1\. 执行摘要与理论基石：从人类可读文档到机器可执行上下文拓扑**

随着自主代码智能体（Autonomous Coding Agents，例如 Claude Code、Cursor、Windsurf、Codex 以及 DeepSeek Harness）全面介入工业级软件研发流程，软件工程的人机协作界面正在经历本质性的范式重构1。在传统的研发体系中，软件文档（如 README、设计规范、Wiki、架构图）完全以人类工程师为目标受众，依赖人类大脑强大的模糊联想、宽容上下文容错与隐喻推理能力4。人类在阅读含有轻微过时信息的文档时，能结合代码实现自发纠偏；然而，大型语言模型（LLM）驱动的自主智能体则缺乏此类容错机制4。当非结构化、缺乏生命周期维护的人类自然语言文档直接输入给智能体时，往往会演化为严重的认知干扰源，进而引发指令漂移、幻觉调用与规则冲突4。

仓储上下文工程（Repository Context Engineering）并非单纯的提示词优化（Prompt Engineering），而是将代码库中的领域知识、架构拓扑、操作规范与安全边界，形式化为高度结构化、具备生命周期治理能力与确定性执行语义的机器可执行上下文拓扑5。这一工程范式的核心使命，是在严格的标记（Token）经济学约束下，使模型在注意力容量有限的前提下实现对工程约束的确定性对齐4。

### **注意力稀释与上下文信噪比的数学表征**

在基于 Transformer 架构的自回归大模型中，输入序列的长度扩张直接加剧注意力分配的熵增。大量实证研究证实了“迷失在中间”（Lost-in-the-Middle）现象在复杂长程任务中的普遍存在：模型对位于上下文开头（Primacy Effect）和结尾（Recency Effect）的信息具有较高的召回与遵循精度，而处于长上下文中间地带的指令与事实信息，其注意力检索性能往往呈现出明显的“U 型”下陷11。

在跨会话与多步规划的代码生成场景下，这一现象更加严峻。由于长程代理会话中充斥着编译输出、工具调用结果以及不断追加的文件内容，中间地带的膨胀不仅带来巨额计算开销，更导致核心架构指令的注意力权重被系统性稀释7。将上下文信息空间形式化表征为集合 ![][image1]，其中包含有效可执行语义集合 ![][image2]、冗余无用语义集合 ![][image3] 以及过期失效语义集合 ![][image4]。上下文信噪比（Signal-to-Noise Ratio, SNR）可建立如下数学模型：

![][image5]

其中，![][image6] 表示冗余信息的注意力干扰权重系数，![][image7] 表示过期信息的决策误导惩罚权重系数（通常在代码生成任务中 ![][image8]）8。实证分析表明，前沿基础模型在单次会话中所能稳定维持的高保真指令容量存在硬性上限，通常仅能稳定处理 150 至 200 条细粒度规则4。一旦全局上下文中堆叠的指令数突破该阈值，注意力竞争将导致关键规则的被动忽略率成倍攀升4。

### **语法抽象树/编译器硬约束与自然语言上下文的刚性边界**

导致智能体上下文信噪比崩溃的最直接工程诱因，是开发者将本应由确定性编译器或语法抽象树（AST）工具处置的微观规则，错误地写入了自然语言上下文文件中4。自然语言具有固有的概率性、模糊性与注意力漂移风险，而现代软件构建链路则建立在严格的确定性之上。

必须确立一条不可逾越的工程分界线：凡是能够通过 AST 静态分析工具、格式化工具、类型系统或单元测试以毫秒级离散逻辑判定的规则，绝不可占用宝贵的自然语言上下文配额4。将缩进大小、导入语句排序、分号省略、换行规则等代码风格写入自然语言文件，是对高阶推理计算能力的低效消耗4。此类规则必须强制下沉至代码库的底层工具链，通过非零退出码（Exit Code ![][image9]）形成反馈回路；自然语言上下文仅用于承载系统级不变量、宏观架构依赖、领域业务契约与不可自动化判定的战略设计意图4。

&nbsp;

| 评估维度 | 静态确定性工具链（L0 编译器/AST 级） | 仓储自然语言上下文（L1/L2 语义级） |
| :---- | :---- | :---- |
| **典型执行载体** | Biome, Ruff, ESLint, TypeScript (tsc), Clippy | AGENTS.md, ARCHITECTURE.md, 路径激活规则 (.mdc)1 |
| **治理规约性质** | 代码缩进、导入排序、命名法、废弃 API 拦截、严格空安全 | 模块分层隔离、跨服务事务一致性、领域业务公理4 |
| **执行与反馈机制** | 语法编译器在隔离子进程中运行，返回行号与非零退出码 | 大模型前向推理过程中通过注意力机制对指令进行概率性吸收4 |
| **Token 与计算开销** | **0 Token** 消耗；消耗极低的本地 CPU 静态分析周期 | **持续消耗** 上下文预算，直接参与自注意力矩阵二次方计算4 |
| **约束遵循保证** | **100% 确定性**；不合规即无法通过构建或提交门禁 | **概率性遵循**；受长文本位置偏置与注意力容量影响4 |
| **失败处理模式** | 机械中断；输出确定性诊断错误栈供智能体精准复原 | 隐性偏航；智能体在不知情状态下持续产生逻辑退化7 |

## **2\. 仓储上下文分层记忆架构（L1 / L2 / L3）与新兴引擎解构**

针对单体文档造成的注意力拥塞与推理延迟问题，现代自主代理系统正在从计算机体系结构的层次化存储设计中汲取灵感，全面推行分层记忆拓扑架构17。

### **分层内存模型规范**

分层记忆模型将代码库的全部先验知识解构为三个在响应延迟、Token 开销与生存周期上各不相同的层级：

* **L1 寄存器层（Registers / Passive Pre-load）**： 对应智能体在每次会话启动、上下文重置或调用初始时，无条件全量前置注入的极简信息流1。该层充当智能体在当前代码仓中的“根本宪法”，仅容纳最高抽象级别的架构公理、绝对操作红线、核心命令基线以及可执行的完成定义（DoD）1。L1 内容必须严格控制在极小行数内（工业级标准通常为 80 至 120 行），确保其能以极高的稳定性命中大语言模型服务端的前缀键值缓存（KV Cache），从而大幅度降低首字生成延迟（TTFT）与推理算力成本4。  
* **L2 工作内存层（RAM / Working Context Pointers）**： 对应智能体在遍历文件系统、执行具体模块任务时按需动态挂载与卸载的中短期上下文18。该层以基于路径模式匹配（Glob-scoped matching）的规则文件或显式子目录指令链为主（例如 Cursor 的 .cursor/rules/\*.mdc 或特定子模块的 AGENTS.md）16。当智能体操作触及特定子系统时，运行时通过钩子拦截或元数据检测将 L2 规则局部载入，并在任务上下文切换或执行窗口压缩时将其从活跃视窗中清除，从而避免局部细节对全局决策造成注意力污染15。  
* **L3 外部磁盘层（Cold Disk / On-Demand Retrieval）**： 对应物理持久化于代码仓磁盘中、但对智能体初始会话完全透明的冷存储库17。这一层包含详尽的原子化架构决策记录（ADRs）、完整的接口规范、历史设计讨论以及复杂业务用例8。智能体只有在解析任务遭遇未决争议，或被 L1/L2 中的显式路由指针明确引导时，才会通过终端工具调用（例如 read\_file、专用 MCP 工具或代码符号检索器）以只读切片的方式按需加载特定条目8。

&nbsp;

| 记忆层级 | 物理表现形态 | 注入与装载触发条件 | 典型容量与 Token 预算 | KV 缓存影响评估 | 生命周期与更新频率 |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **L1 寄存器层** | 仓储根目录 AGENTS.md (或兼容的 CLAUDE.md)1 | 会话初始化阶段无条件强制预载1 | ![][image10] Tokens (![][image11] 行)4 | **绝对友好**：长周期静态不变，最大化实现 Prompt 缓存命中21 | 极高稳定性；仅随团队重大架构变革经人工评审后变更22 |
| **L2 工作内存层** | 模块目录 AGENTS.md, .cursor/rules/\*.mdc 16 | 文件系统访问触达深层路径或模式匹配命中16 | 单个模块 ![][image10] Tokens；随执行栈动态调整15 | **局部友好**：作为会话追加块接入，不破坏主干前缀缓存21 | 动态进出；随任务分支或执行压缩被主动替换或回收15 |
| **L3 外部磁盘层** | docs/adr/\*.md, 详细设计规范, 历史变更归档8 | 智能体在具备明确指引后通过工具显式拉取8 | 理论无上限；单次拉取受切片与工具调用上下文限制8 | **中性**：作为动态观察结果返回，在窗口压缩中易被摘要化15 | 追加写入（Append-only）；历史记录永久归档并声明废弃状态9 |

### **新兴系统工程实现深度解构**

在前沿智能体系统与长期运行测试框架（Harness）的代码实现中，分层记忆治理展现出多样化的架构探索：

在 DeepSeek Harness（deepseek-harness 内部的 packages/context/agent-instructions 模块）的实现中，架构师设计了一套针对 KV 缓存高度友好的“基线与动态作用域感知机制”21。系统在首次握手时仅构建由用户全局配置与项目根目录构成的极简基线指令链（\~/.dsh/AGENTS.md 顺次连接至 AGENTS.md），并且对整体字节大小施加硬性上限约束（maxBytes）21。当且仅当智能体的第一方文件系统操作（Read、Write、Edit）触及更深层的代码目录（例如 packages/app/）时，运行框架才会自动检测并追加该作用域下的局部指令文件21。DeepSeek Harness 强制规定新发现的指令必须作为会话消息链的末尾内容追加，并严格执行基于 SHA 摘要的版本比对；只要该路径内容未变，会话便重用既有状态，杜绝由于文件系统探索导致的全局前缀 KV 缓存失效21。此外，其配套的自动化评审沙箱（Auto Review）在执行危险系统调用前，会隔离主智能体的长程聊天记录，仅以只读方式重建五维最小事实投影进行快速裁决，有效阻断了上下文污染26。

在 Prime Agent 的架构体系中，研发团队抛弃了传统的“提示词拼接与工具检索”模型，转而引入递归语言模型（Recursive Language Model, RLM）与持续测试框架（Continual Harness）范式15。Prime Agent 将智能体的持久运行状态形式化为四元组：

![][image12]

其中 ![][image13] 代表基础系统提示词，![][image14] 代表子智能体规格列表，![][image15] 代表技能库，![][image16] 代表记忆库15。Prime Agent 的突破性创新在于，将庞大的代码上下文与多层级说明文档视为运行在持久化 IPython 内核中的可编程内存变量，而非一股脑填入 LLM 的输入流中10。智能体在推理循环中利用生成的 Python 程序对上下文变量执行按需切片、条件过滤与外部委托10。其系统内核集成了自主垃圾回收器（Agentic Garbage Collection），能够主动识别并回收堆栈中过期的中间状态，并且支持通过 /refine 指令在任务推进中动态更新辅助指令层，同时保持根级别 ![][image13] 提示词的绝对不可变性，杜绝了自适应系统常出现的逻辑退化15。

在 Pi Agent 与 Claude Code 的工程实践中，上下文被拆解为互为补充的“双轨制”存储：即人类编写的强制性行为规范（CLAUDE.md / AGENTS.md）与系统自主沉淀的经验追踪库（MEMORY.md / Auto Memory）1。Claude Code 内部硬编码了严格的自限机制：模型自主维护的 MEMORY.md 索引被物理截断在 200 行或 25KB 阈值以内22。一旦会话积累突破此边界，系统静默阻断追加，并在会话结算阶段触发后台异步精炼程序（Auto Dream 机制），将短期情境记忆压缩为结构化事实下沉至外部向量存储或冷文件系统中，从根本上防止了智能体自增记忆对工作上下文的无节制膨胀22。

## **3\. 既有 Markdown 模式解构与消亡机制**

伴随辅助研发工具的野蛮生长，现代软件仓储中往往散落着职责不清、生命周期重叠的 Markdown 文件。对这些历史遗留模式进行拓扑层面的解构，是清理认知负荷、构建高信噪比上下文的必要步骤。

### **历史模式分类学解构**

历史文档模式主要集中在七类形态，它们在人机协同中呈现出不同的效用与损耗特征：

* **不变量与系统边界文件（THESIS.md、AXIOMS.md、ARCHITECTURE.md）**：此类文件旨在声明代码库存在的本体论意义、设计哲学与最核心的模块边界划分。其内容属于高抽象度的架构基石，但在实践中常因夹杂过度形而上学的叙述，导致有效指导代码编写的规则密度过低。  
* **行为规范与操作引导文件（AGENTS.md、CLAUDE.md、.cursorrules、RULES.md）**：此类文件承载智能体的操作权限、构建指令、测试命令、交互契约以及防护栏1。然而，多工具并存导致此类文件碎片化严重，团队往往需要在不同私有格式之间重复粘贴相同的配置5。  
* **语义约定与编码标准文件（CONVENTIONS.md、STYLE.md、STANDARDS.md）**：详细记录变量命名法、文件组织范式、代码书写偏好29。绝大多数此类内容与现代 AST 静态分析工具的职能高度重合，是导致上下文窗口无效占用的主因4。  
* **导航与目录索引文件（INDEX.md、MAP.md、TREE.md）**：人工维护的文件系统拓扑图与代码文件功能描述清单，试图为智能体提供导航定位图谱。  
* **决策与历史记录文件（单体 DECISIONS.md 与原子化 docs/adr/\*.md）**：记录技术选型的演进动机、权衡考量与被否决的备选方案8。单体文件通常按时间线性追加，而原子化文件则独立管理8。  
* **跨会话持久状态文件（MEMORY.md、STATE.md、会话恢复断点日志）**：记录长期任务未完成的待办项、临时环境变量以及会话间沉淀的避坑指南14。此类文件经常混淆了“团队通用经验”与“个人瞬态状态”22。  
* **本地与个性化范围文件（USER.md、.agents.local.md）**：开发者个人开发机环境差异、个人编辑习惯与调试密钥等私有配置19。

### **文档腐化（Doc Rot）的必然性与现代淘汰机制**

传统文档管理模式之所以在代码智能体介入后迅速退化，根源在于其架构违背了“单一事实来源”（Single Source of Truth, SSOT）原则，产生了不可避免的人工维护熵增。

手动维护的代码级 INDEX.md 或 TREE.md 具有必然失效的生命周期缺陷。在敏捷开发与智能体自主编程的高频迭代下，文件的创建、重构、拆分与删除每时每刻都在发生。人类工程师极少同步更新文本索引，而智能体又缺乏对全局文件系统拓扑的无损预知。过时失效的 INDEX.md 比完全没有索引更具杀伤力：大模型会基于文本索引中虚构或已废弃的模块路径发起推理，导致后续的文件读取与写入工具连续爆出 ENOENT 异常，迫使智能体陷入反复试错的死循环。

现代架构彻底废黜人工书写的文件级文本索引。代码文件与符号本身的物理存在，是空间拓扑的唯一事实来源。智能体对代码结构的感知应当全面移交给实时的外部代码制图引擎，例如基于 Tree-sitter 的轻量级 AST 工具（如 repomap、Aider 拓扑检索器）或智能体运行时的原生目录探索原语32。通过在运行时动态提取符号定义与引用图谱，智能体能够以极低的 Token 成本实时重构精准的局部上下文，从根本上消除了静态维护索引带来的文档腐化风险32。

单体 DECISIONS.md 的破产则源于自回归注意力的“扁平化时空陷阱”。在单体文件中，早期的架构决策（如“采用集中式 Redux 状态管理”）与后期经过架构演进所推翻的最新决策（如“迁移至轻量 Zustand 并废除全局单体 Store”）被物理混合在同一个文本流中。对于没有全局强类型时间戳概念的大语言模型而言，这两段文字在语义相似度检索时具有同等的激活权重。实证表明，由于长上下文中的注意力振荡与首因偏置，模型经常将已经被推翻的陈旧选型提取为当前实现的技术依据，进而导致“僵尸决策复活”的严重工程事故8。

现代工程方案通过物理隔离与状态机机制彻底淘汰单体决策文件。所有架构决策必须作为原子化文档下沉至 L3 存储（即 docs/adr/NNNN-\*.md），每个决策必须具备规范的元数据头部，显式声明当前生命周期状态（Proposed、Accepted、Superseded、Deprecated）8。根目录的上下文仅保留指向活动决策的单向索引；任何被取代的决策必须明确声明其继承者编号，使智能体通过工具拉取历史时能够沿着有向无环图（DAG）遍历出唯一的有效决策终态8。

## **4\. 4D 分类模型与物理拓扑映射**

为了消除文档设置的随意性，本报告建立一套四维正交分类体系，将进入仓储的每一条上下文信息进行精确的数学定位与工程定址。

### **四维坐标体系数学表征**

任何代码仓元数据单元 ![][image17] 均可正交解构为一个四元组向量：

![][image18]

* **生命周期与时态稳定性（Temporal Stability, ![][image19]）**：  
  ![][image20]  
  公理不变量在项目生命周期内具有永久的半衰期；渐进演变架构仅在宏观重构时更新；追加式历史遵循只增不改原则；瞬态任务状态则以单次会话或单次指令为生命周期极限15。  
* **抽象层级维度（Abstraction Level, ![][image21]）**：  
  ![][image22]  
  宪法级规则具有全局强制穿透力；操作级规则则高度依赖底层操作系统与具体构建工具1。  
* **认识论方向维度（Epistemology, ![][image23]）**：  
  ![][image24]  
  描述性上下文为智能体构建世界观图景；规范性上下文则为其设定行为沙箱边界与行动序列4。  
* **机器消费模式维度（Machine Consumption Mode, ![][image25]）**：  
  ![][image26]  
  决定了该元数据究竟是通过 Prompt 前缀持续计费，还是通过路径检测动态引入，亦或是完全交由外部工具裁决4。

### **仓储元数据的 4D 坐标映射与定址**

通过将各类工程规范与文档映射至该四维坐标系，可以推导出确定性的物理组织形式与存储拓扑结构：

&nbsp;

| 原始知识载体 | T (稳定性) | A (抽象度) | E (认识论) | M (消费模式) | 最优物理宿主与存放路径 |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **操作红线与安全边界** | Axiom | Constitutional | Prescriptive | L1-Preload | 根目录 AGENTS.md（行为合约区）4 |
| **构建、测试与退出闭环** | Axiom | Operational | Prescriptive | L1-Preload | 根目录 AGENTS.md（DoD 验证区）15 |
| **仓储全局拓扑与核心不变量** | Topology | Architectural | Descriptive | L1-Preload | 根目录 ARCHITECTURE.md（全局拓扑区）4 |
| **业务子域编码规范与模式** | Topology | Semantic | Prescriptive | L2-Routing | .cursor/rules/\*.mdc 或 packages/\*/AGENTS.md 16 |
| **架构演化权衡与决策记录** | History | Architectural | Both | L3-OnDemand | docs/adr/NNNN-\*.md（独立原子文件）8 |
| **深层业务用例与规格说明书** | History | Semantic | Descriptive | L3-OnDemand | docs/specs/\*.md（按需工具读取）9 |
| **代码缩进/格式化/类型安全** | Axiom | Operational | Prescriptive | L0-Compiler | 静态配置：biome.json, tsconfig.json, ruff.toml |
| **静态文件树与符号清单** | Ephemeral | Semantic | Descriptive | L0 / AST | **直接废除**；由实时代码制图工具运行时提供32 |
| **跨会话自增经验与断点** | Ephemeral | Semantic | Both | L2/L3-Auto | 智能体自管目录：\~/.claude/projects/\*/memory/ \[cite: 17, 22\] |
| **个人本地私有开发环境** | Ephemeral | Operational | Prescriptive | L1 (Local) | 本地配置：.agents.local.md（列入 .gitignore）14 |

### **生产级仓储物理拓扑结构**

依据 4D 坐标推导出的最优物理目录拓扑，全面废黜了冗余的文件碎片，形成了清晰的分层治理结构：

* 根目录 AGENTS.md：L1 级常驻上下文，承担行为治理合约、操作红线、基础工具命令与必须强制执行的完成定义（DoD）1。  
* 根目录 ARCHITECTURE.md：L1 级常驻上下文，承担全局系统边界划分、模块依赖流向、不可打破的领域公理与核心活动 ADR 路由索引4。  
* 根目录 .gitignore：显式声明忽略 .agents.local.md、\*.state.json 等会话瞬态文件，防止个人环境污染团队基线14。  
* 目录 .cursor/rules/（或适配其他引擎的路径路由规则）：L2 级动态工作内存，包含按需激发的细粒度规则文件（例如针对 API 层后端的 backend-api.mdc、针对前端界面的 frontend-components.mdc）14。  
* 目录 docs/：L3 级按需只读冷存储库，包含解耦的历史决策记录与长篇规格文档8：  
  * 子目录 docs/adr/：包含如 0001-use-drizzle-orm.md、0002-async-event-bus.md 等严格原子化的架构决策记录8。  
  * 子目录 docs/specs/：包含如 checkout-state-machine.md 等详细的状态机业务规格说明书9。  
* 业务代码目录（如 src/ 或 packages/）：唯一的符号事实来源，由 AST 静态分析器与语言服务器（LSP）负责实时解构32。

## **5\. 整合矩阵：收敛至极简双文件根拓扑与按需归档**

为根绝根目录下文件碎片化导致的上下文膨胀，现代上下文工程主张将根目录常驻上下文高度收敛为两个语义严格正交的入口文件，并辅以规范的 L3 深度归档体系。

### **双文件职责的正交切分**

根目录双文件架构实现了规范性与描述性上下文的彻底分离：

AGENTS.md 定位为纯粹的规范性行为引擎（Prescriptive Engine）。该文件是智能体进入代码仓时签署的“劳动合同与安全准则”。其内容绝不包含对业务逻辑的漫长讲解，而是专注于界定智能体在运行时的权限边界、基础操作环境、负向护栏以及完成任务时必须通过的确定性测试管道4。它是行动的准绳，负责确保智能体的每一次终端调用和代码变更高内聚且安全可控4。

ARCHITECTURE.md 则定位为纯粹的描述性世界观拓扑（Descriptive Topology）。该文件是代码仓的“空间地理简图与物理定律”。其内容不包含日常的安装、格式化或提交指令，而是精确描绘模块之间的物理隔离边界、调用方向性约束、不可破坏的领域公理以及指向 L3 深层决策档案的路由指针4。它是认知的地图，负责确保智能体在规划多文件重构与新增功能时不偏离既定的系统设计架构4。

### **文档收敛与修剪整合矩阵**

通过严格的职责收敛矩阵，原本分散在十余个文件中的信息被系统化提炼并降噪：

&nbsp;

| 历史碎片化模式 | 淘汰与收敛的根本动因 | 归宿目标路径 | 具体转化、提炼与修剪操作 |
| :---- | :---- | :---- | :---- |
| CLAUDE.md, .cursorrules, RULES.md | 厂商方言割裂，内容高度重复，多工具共存时易产生规则版本倾斜5 | **AGENTS.md** | 统一收拢至跨工具标准的 AGENTS.md；针对特定 IDE 的规则由本地适配器编译生成1。 |
| THESIS.md, AXIOMS.md | 哲学化描述过多，包含大量人类团队愿景，对代码生成的 Token 信噪比极低 | **ARCHITECTURE.md** | 剔除所有叙事性修辞，高度浓缩为 3 至 5 条带有一票否决性质的系统不变量（Invariants）。 |
| CONVENTIONS.md, STYLE.md | 超过 90% 的条目属于低级语法风格，自然语言缺乏确定性惩罚机制4 | **编译器 (L0) \+ 路径规则 (L2)** | 机械规则直接编译进 biome.json 或 ruff.toml；领域高阶规范移入按需激发的局部规则14。 |
| INDEX.md, MAP.md, TREE.md | 随代码重构而迅速失效，死路径引发智能体工具链连续异常 | **彻底销毁** | 从版本控制中永久剔除；依靠智能体运行时挂载的 AST 实时符号探针进行按需定位32。 |
| 单体 DECISIONS.md | 线性历史造成上下文污染，极易诱发模型复活早已被推翻的旧技术方案8 | **docs/adr/\*.md** | 拆分为遵循 MADR 规范的原子化文档；在 ARCHITECTURE.md 中仅维护最新生效决策状态表8。 |
| MEMORY.md, STATE.md | 混合了团队通用认知与个人瞬态调试记录，破坏前缀缓存稳定性22 | **智能体私有状态层** | 移出 Git 版本控制；交由智能体运行时的本地存储或专属会话记忆库管理14。 |
| USER.md, .agents.local.md | 容易导致个人绝对路径或私有调试偏好污染代码仓标准基线19 | **本地覆盖文件** | 仅保留对 .agents.local.md 的读取支持，并将其强行固化在 .gitignore 规则中14。 |

## **6\. 智能体操作沙箱与确定性防御机制**

在授予自主智能体执行终端命令与直接修改文件的权限后，纯粹依赖其自发性的“道德约束”是不切实际的1。上下文工程必须构建一套兼具机械退出闭环、负向提示防御与冲突偏序仲裁的认知沙箱体系1。

### **可执行的“完成定义”（Definition of Done, DoD）**

智能体最典型的幻觉表现之一，是在未运行任何验证工具的情况下在会话中宣称“已成功实现需求并修复所有测试”15。上下文工程必须在 AGENTS.md 中构建不可绕过的机器退出闭环（Deterministic Verification Pipeline）15。

DoD 绝对不能采用“请确保代码整洁无错”这类模糊的祈使句，而必须转化为具备强类型退出状态（Exit Code 0）的链式终端验证程序15。智能体在宣告完成并准备生成交付总结前，必须在当前执行上下文中完整产生一组按顺序调用的确定性检查记录：

> 1. 语法与代码风格自动化修复：执行 pnpm biome check \--write（或等效的快速 AST 修复命令），消除语法层面的琐碎偏航。  
> 2. 严格静态类型编译验证：执行 pnpm tsc \--noEmit，确保修改后的抽象契约与参数签名在全局类型拓扑中完全闭合。  
> 3. 影响范围关联测试执行：执行 pnpm vitest run related \--run，仅针对修改涉及的代码依赖节点运行单测，证明未引入回归破坏。  
> 4. 仓储脏状态排查：执行 git status \--porcelain，核验当前工作区是否留存未被跟踪的临时垃圾文件或意外修改的配置文件。

只有当上述四道检验工序全部返回退出状态码零时，智能体的任务执行才被允许终止15。在指令中必须明确警告：任何缺少实际工具执行输出日志的“口头自我验证”，将被底层宿主直接判定为不合格失败任务。

### **负向防护栏（Negative Guardrails）的提示词模式**

自回归模型在处理负向指令时，如果仅接收到单纯的否定词（如“不要破坏代码”），往往因为注意力权重在关键实体上的聚焦，产生逆向执行的概率泄露35。高信噪比的负向护栏必须严格遵循“情境（Context） \+ 明确禁止（Prohibition） \+ 获准替代方案（Approved Alternative）”的三元组范式（即“Instead”模式）36：

在防御破坏性终端指令时，上下文应明确声明：“在任何涉及版本控制、进程管理或文件清理的情境下，严禁执行任何带有强制覆盖、历史重写或不可逆删除的指令（严格禁止包含 git push \--force、git reset \--hard、rm \-rf、DROP TABLE 等操作）。若需要清理未跟踪的文件碎片，必须使用 git clean \-n 进行试运行预览，并将输出呈现给人类工程师以获取明确确认”36。

在防御依赖项劫持（Dependency Hijacking）时，上下文应明确约束：“当面临缺少特定辅助功能的情境时，严禁智能体自行编辑 package.json 或 pyproject.toml 引入任何新的第三方外部依赖包6。必须穷尽当前工程的内置模块以及标准库功能（恪守‘Lazy, not negligent’哲学）37。如果业务实现确有引入依赖的必要，智能体仅被允许在 docs/adr/ 下生成一份技术预研草案，并中断任务以等待人类架构师的批准”6。

在防御未经授权的“过度重构”（Unsolicited Clever Refactoring）时，上下文应构建空间防御：“在修复特定缺陷或实现局部特性的情境下，严禁对超出本次任务影响边界的代码进行顺手格式化、变量重命名、类型抽象提取或无指示的文件拆分6。对于在执行过程中观察到的相邻模块历史遗留缺陷，智能体只能在最终会话报告的建议章节中列出，绝不可私自编辑其源码6。”

### **规则冲突仲裁与偏序优先级体系**

在大型工程的实际演进中，抽象原则之间往往存在内在张力（例如遵循全局 DRY 原则与保持局部代码自包含性之间的矛盾，或者采用新技术规范与保持向下兼容性之间的矛盾）1。如果缺乏清晰的形式化仲裁机制，智能体在遭遇原则冲突时将产生注意力振荡，甚至在多次迭代中来回反转代码实现1。

仓储上下文必须建立并声明全局原则的严格全序关系（Strict Precedence Ordering）：

![][image27]

这套全序关系的工程仲裁逻辑自上而下逐级穿透：

* **安全与数据完整性（Security & Integrity）拥有绝对一票否决权**：任何为了迎合下游原则（如提高吞吐、减少重复代码或简化接口）而削弱参数校验、跳过鉴权守卫或暴露未脱敏数据的行为均被判定为系统级违规30。  
* **正确性与测试闭环（Correctness & DoD）高于演进诉求**：所有实现必须首先满足既定业务逻辑并通过确定性测试链，严禁交付虽然代码结构优雅但破坏了单测的半成品15。  
* **向前/向后兼容性（Compatibility）高于架构重整**：除非任务指令明确声明放弃兼容性，否则所有公有接口、持久化数据 Schema 与序列化协议必须保持向下兼容，严禁在未经版本迁移设计的情况下单方面变更契约6。  
* **架构边界不变量（Architectural Invariants）高于局部优化**：代码必须严格遵守预设的物理分层与依赖流向规则，严禁为了局部实现方便而跨层注入依赖或反向依赖底层组件。  
* **局部简单性（Local Simplicity / KISS）优先于全局去重（DRY）**：当跨模块抽象消除重复代码会导致引入过度泛型、多层间接寻址或紧耦合状态共享时，智能体必须主动放弃抽象，优先保证局部实现的平铺直叙与高内聚性37。  
* **全局代码去重（DRY）处在末位**：仅当上述所有前置约束均完全得到满足、且抽象提取能够带来明确且无副作用的工程收益时，才允许进行跨模块通用逻辑的抽取。

## **7\. 生产级蓝图与优化模板**

### **生产级根目录 AGENTS.md 模板**

该文件作为智能体每次启动时必读的 L1 行为治理引擎，其行数严格压制在 100 行左右，去除了所有低信噪比的人文套话与格式化细则4：

# **Agent Behavioral Contract & Operational Guidelines**

## **1\. Operating Constitution & Negative Guardrails**

* **Minimal Blast Radius**: Touch ONLY files directly required for the immediate task. Never refactor, rename, or restyle code outside the issue scope.  
* **Dependency Freeze**: Do NOT install external packages or modify package manifests without prior approval and an explicit ADR draft.  
* **Destructive Command Ban**: Execution of destructive commands (git push \-f, git reset \--hard, rm \-rf, DROP TABLE) is blocked. Use non-destructive alternatives (e.g., git clean \-n).  
* **Rule Precedence Hierarchy**: Security \> Correctness (DoD) \> Backward Compatibility \> Architectural Invariants \> Local Simplicity \> Global DRY.

## **2\. Tooling Baseline & Environment**

* Runtime: Node.js \>= 22.0.0, pnpm \>= 9.0.0  
* Setup: pnpm install \--frozen-lockfile  
* Auto-fix & Format: pnpm biome check \--write  
* Static Typecheck: pnpm tsc \--noEmit  
* Regression Testing: pnpm vitest run related \--run

## **3\. Mandatory Definition of Done (DoD)**

Before reporting task completion, you MUST execute the following verification chain and achieve clean passes (Exit Code 0):

> 1. pnpm biome check \--write (Ensure format & basic lint rules pass)  
> 2. pnpm tsc \--noEmit (Confirm zero static type errors)  
> 3. pnpm vitest run related \<modified\_files\> (Prove zero regression in affected modules)  
> 4. git status \--porcelain (Confirm no lingering untracked scratch files)  
>    *Self-certification without real execution logs is strictly rejected.*

## **4\. Architectural Pointers & Escalation Protocol**

* Architectural Topology & Data Invariants: Read ARCHITECTURE.md.  
* Historical Context & Technical Decisions: Read individual files in docs/adr/.  
* Ambiguity Protocol: If instructions conflict with existing ADRs or architecture boundaries, HALT immediately, formulate the dilemma, and await human intervention.

### **生产级根目录 ARCHITECTURE.md 模板**

该文件作为描述系统物理边界与逻辑拓扑的世界观蓝图，专注于硬性分层约束与活动决策的快速路由4：

# **System Architecture & Invariant Topography**

## **1\. Core Invariants & Boundary Axioms**

* **Strict Downward Dependencies**: Dependencies flow strictly downward: Presentation (apps/) \-\> Application Services \-\> Domain Core (packages/core) \<- Infrastructure (packages/infra).  
* **Domain Purity**: packages/core has ZERO external dependencies. Importing web frameworks, database clients, or network libraries into the domain core is prohibited.  
* **Explicit Persistence**: Aggregate roots in the domain model must be mutated exclusively through domain methods. Bypassing domain logic via raw database mutations is strictly forbidden.

## **2\. Repository Physical Topology**

* apps/web: Next.js frontend client (App Router). Consumes Application API via typed tRPC.  
* packages/core: Pure business models, domain events, and state-machine transitions.  
* packages/infra: Database connections (Drizzle ORM), payment integrations, message queues.  
* packages/api: Fastify server exposing HTTP routes and bridging network requests to application services.

## **3\. Active Architectural Decisions (ADR Routing)**

When modifying the subsystems listed below, read the corresponding ADR in docs/adr/ before planning changes:

* Primary ORM & Schema Strategy: See docs/adr/0002-drizzle-sqlite-boundary.md  
* Asynchronous Job Processing: See docs/adr/0005-in-memory-queue-worker.md  
* Identity & Token Revocation: See docs/adr/0009-stateless-jwt-with-bloom-filters.md

### **生产级原子化架构决策记录（Atomic ADR）模板**

文件物理定址规范为：docs/adr/NNNN-kebab-case-title.md。其结构遵循轻量级架构决策记录（MADR）范式，包含机器可解析的状态标记与负向范围定义8：

# **ADR-0042: Adoption of Typed Boundary Contracts via Zod**

## **Metadata**

* Status: Accepted (Supersedes: ADR-0012)  
* Date: 2026-03-31  
* Deciders: Core Architecture Group

## **Context & Problem Statement**

External webhook payloads and API request inputs are currently validated using scattered, ad-hoc conditionals across route handlers. This has caused recurrent runtime exceptions and silent data corruption. We require an automated, type-inferred runtime validation schema.

## **Considered Options**

> 1. Zod  
> 2. TypeBox  
> 3. Handcrafted TypeScript Type Guards

## **Decision Outcome**

Chosen Option: "Zod".

### **Positive Consequences**

* Automatic derivation of static TypeScript types from validation schemas.  
* Native integration with our Fastify route definitions.  
* Deterministic and structured error reporting back to API consumers.

### **Negative Consequences & Trade-offs**

* Modest runtime bundle initialization overhead compared to pre-compiled TypeBox schemas.  
* Requires migrating legacy controllers across 12 distinct routes.

## **Negative Guardrails & Scope Boundaries**

* Zod schemas MUST reside strictly within the contracts/ directory of the consuming package.  
* Validation MUST occur at the network input boundary. Never inject Zod schemas into the inner packages/core domain models.

## **8\. 经典反模式与失效分类学（Top 7 Anti-Patterns）**

在工业级工程演化中，缺乏上下文治理的代码库普遍表现出若干典型的上下文工程反模式。这些反模式严重拖累了智能体的规划能力，并直接转化为线上的安全隐患4。

### **反模式深度矩阵分析**

&nbsp;

| 反模式名称与代码表征 | 核心特征表征 | 物理机理与智能体失效机制 | 架构级解毒方案（Mitigation） |
| :---- | :---- | :---- | :---- |
| **1\. 文本倾倒狂热 (Context Dumping)** | 将长达数万字的 PRD、历史背景、整个 Wiki 打包压入根上下文文件4 | 触发“Lost-in-the-Middle”效应；有效注意力预算被历史散文吞噬，核心开发指令遵循度骤降4 | 严格实施 L1/L3 分层存储；常驻上下文施加 120 行上限，细节转入 docs/ 冷存储并由工具调取4 |
| **2\. 静态目录镜像 (The Static Directory Mirror)** | 在文档中人工画出详尽的物理文件树，并注明每个源文件的功用 | 文件结构变更时文档无法实时同步，造成严重“文档腐化”；模型基于死路径发起盲目调用并报错 | 彻底废除文本文件树；指引智能体使用 AST 工具（如 repomap）或实时 Shell 原语动态探测符号32 |
| **3\. 虚愿式规范治理 (Aspirational Governance)** | 通篇充斥“编写健壮的代码”、“尽可能优雅设计”、“注意可维护性”等空洞口号3 | 概率模型的注意力头无法在无锚点的情境下落地空洞词汇；产生大量缺乏功能测试的伪代码3 | 转向硬性可验证指标；以具体命令、严格阈值与确定性退出码（Exit Code 0）替代空泛描述4 |
| **4\. 僵尸决策复活 (Zombie Decisions)** | 维护单体线性追加式 DECISIONS.md，过期、废弃与生效决策混合排列8 | 模型缺乏全局时间状态机意识，倾向于召回文本相似度高但已被废止的早期技术栈方案8 | 实施原子化 ADR 目录结构；强制推行 Status: Deprecated / Superseded 显式单向标记链9 |
| **5\. 编译器重申症 (Linter Redundancy)** | 在 Markdown 中耗费几百行书写缩进、双引号、空行及分号使用规范4 | 严重浪费宝贵的常驻注意力窗口；将高级推理资源消耗在 AST 分析器毫秒级即可解决的问题上4 | 将语法规则下沉至 L0 工具链（Biome / Ruff / ESLint）；Markdown 中仅保留一条执行命令4 |
| **6\. 人格扮演迷思 (Persona Delusion)** | 耗费前置 Token 设定“你是一位拥有 20 年经验、严谨苛刻的硅谷架构专家”4 | 经验证明深层系统指令槽被低效的人格设定挤占，实际任务中的边界控制力反而减弱4 | 移除一切浮夸人设；直入工程主题，以技术规范、输入输出契约与负向护栏构建冰冷的操作沙箱4 |
| **7\. 越界重构狂热 (Scope Bleed)** | 智能体在修复微小 Bug 时，自作主张对数十个外部模块开展重命名与语法现代化6 | 模型缺乏局部修改的经济直觉，在无明确边界约束时倾向于盲目追求全局所谓的代码“一致性”6 | 部署“情境+禁止+替代”的负向护栏；在 DoD 中严密审查 git diff \--stat 的修改文件数量与边界6 |

### **核心失效模式的机理解析**

在上述反模式中，“静态目录镜像”与“僵尸决策复活”最具隐蔽性与杀伤力。

静态目录镜像的破产本质上是软件工程中典型的“缓存失效问题”。当智能体依赖人工书写的静态文件清单时，每一次跨模块重构如果未能百分之百同步更新文档，就会制造知识断层。大模型在推理时往往更倾向于盲信全局 System Prompt 中给出的静态目录，而非重新使用文件列举工具进行核验。这种过度依赖会诱发模型的“反向推演幻觉”，即模型依据错误的旧路径推断文件内容，并在错误的位置生成新的重复逻辑代码，使整个代码库的模块拓扑迅速瓦解。

而僵尸决策复活则暴露了自回归模型处理非结构化时序知识时的固有缺陷8。在传统的单体架构讨论记录中，技术路线往往经历了由方案 A 到方案 B 再到方案 C 的迭代。人类能够凭借对历史事件发生时间的常识，自动抑制方案 A 和 B 的影响力；然而，LLM 依靠的是语义向量的余弦相似度与词法共现。在许多场景下，早期记录（方案 A）由于探讨详尽、关键词丰富，在向量空间中对某个具体开发任务的匹配分值反而高于简短的最终结论（方案 C）。这就不可避免地导致智能体在最新的代码库中，重新引入已经被团队用血泪代价废弃的旧框架或脆弱模式8。

## **9\. 跨平台生态全景与工具化 RFC (ContextSpec)**

当前，各大代码智能体平台在上下文文件的加载策略、边界约定与作用域控制上呈现出高度碎片化的状态5。这种割裂不仅增加了跨工具团队的协作成本，也使得企业级架构治理难以标准化5。

### **主流代码智能体平台上下文机制横向评测**

&nbsp;

| 核心特性 | Claude Code | Cursor | Windsurf | DeepSeek Harness | Prime Agent |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **标准上下文入口** | CLAUDE.md, AGENTS.md \[cite: 1\] | .cursorrules, .cursor/rules/\*.mdc \[cite: 28, 38\] | .windsurfrules, .windsurf/rules/\*.md \[cite: 14, 33\] | AGENTS.md, 嵌套 packages/\*/AGENTS.md 21 | H=(ρ, G, K, M) 全套持续环境四元组15 |
| **初始加载策略** | 会话启动时全局无条件注入1 | 支持全局注入或基于文件路径模式按需激发16 | 级联加载全局与项目级配置3 | 基于基线前缀构建，深层路径按需增量加载21 | 基础提示词常驻，上下文作为变量动态载入内核10 |
| **作用域控制模式** | 单一主配置，支持通过 .claude/rules/ 拆分1 | 基于 YAML Frontmatter 的 Glob 精确匹配16 | 规则划分配合基于 Cascade 的多步工作流14 | 基于文件系统调用的路径深度动态探测21 | 基于 Python REPL 环境的对象引用与函数传递10 |
| **经验与记忆机制** | 双轨制：人工规则与 MEMORY.md 索引截断19 | 基于工作区索引与历史对话向量检索3 | Cascade 自动捕获的非结构化短期事实3 | 基于 Append-only 事件日志与只读沙箱审查26 | 具备 /refine 算子与主动垃圾回收机制15 |
| **核心工程局限** | 全局文件无硬性截断，超长即引发遵循退化1 | 专属 MDC 语法脱离该 IDE 即失去路由语义5 | 长会话摘要压缩容易丢失关键决策论证链8 | 依赖专属宿主，通用轻量编辑器接入成本高2 | 依赖全功能 Python 内核，运行时安全沙箱隔离重24 |

### **开放标准技术规范提案：ContextSpec (v1.0-draft)**

为了终结跨平台配置碎片化的困境，本报告正式提出面向工业界的开放治理规范提案——ContextSpec。其核心设计思想遵循“单一事实来源，全平台分发编译（Single Source of Context, Compile Everywhere）”的范式5。

ContextSpec 将所有上下文文件统一声明为标准的 Markdown 文档，并在文件顶部嵌入严格类型化的 YAML Frontmatter 元数据块：

&nbsp;

&nbsp;

&nbsp;

YAML

\---  
$schema: "https://contextspec.dev/v1/schema.json"  
version: "1.0.0"  
target: "context-rule"  
metadata:  
&nbsp;&nbsp;name: "backend-boundary-contract"  
&nbsp;&nbsp;description: "Enforces domain isolation and prevents direct SQL calls in API handlers."  
spec:  
&nbsp;&nbsp;level: "L2"  
&nbsp;&nbsp;lifecycle: "topology"  
&nbsp;&nbsp;epistemology: "prescriptive"  
&nbsp;&nbsp;scope:  
&nbsp;&nbsp;&nbsp;&nbsp;match:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\- "packages/api/src/\*\*/\*.ts"  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\- "packages/core/src/\*\*/\*.ts"  
&nbsp;&nbsp;&nbsp;&nbsp;exclude:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\- "\*\*/\*.test.ts"  
&nbsp;&nbsp;precedence: 400  
&nbsp;&nbsp;exports:  
&nbsp;&nbsp;&nbsp;&nbsp;cursor: ".cursor/rules/backend-boundary.mdc"  
&nbsp;&nbsp;&nbsp;&nbsp;claude: ".claude/rules/backend-boundary.md"  
&nbsp;&nbsp;&nbsp;&nbsp;windsurf: ".windsurf/rules/backend-boundary.md"  
\---

\# Backend Boundary Engineering Directives

\#\# Invariants  
\- Route handlers must call Application Service interfaces; direct DB access is forbidden.  
\- Domain models in \`packages/core\` must never import Fastify or HTTP context types.

### **上下文工程自动化工具集设计：repo-context CLI**

依托 ContextSpec 规范，工程团队可以通过统一的 CLI 工具链实现仓储上下文的生命周期监控、静态分析与平台代码生成：

* repo-context init：自动化脚手架。扫描当前代码库的技术栈特征（package.json、Cargo.toml、go.mod），提取现有的 Linter 与编译配置，自动在仓储根目录下初始化标准的 AGENTS.md 与 ARCHITECTURE.md 双文件骨架，并构建初始的 docs/adr/ 目录结构。  
* repo-context lint：静态审计引擎。集成至团队 CI 流程或预提交钩子（Pre-commit Hooks）中，针对当前分支的代码与上下文文档进行合规性阻断检查。

#### **repo-context lint 核心算法与指标计算**

repo-context lint 内部实现四套核心分析器，以纯粹的离散分析杜绝上下文层面的腐化：

> 1. **Token 税负审计器（Token Tax Auditor）**： 计算所有 L1 常驻文件（AGENTS.md 与 ARCHITECTURE.md）的 Token 绝对消耗值。通过接入主流分词器（Tokenizer），对根上下文设定严格的预算警戒线（默认上限为 2,500 Tokens）。一旦发现开发者私自向 L1 文件注入长篇文档，立即抛出编译错误中断 CI4。  
> 2. **死指针与悬空引用检测器（Dead Pointer Checker）**： 利用正则表达式与 Markdown AST 解析器，遍历上下文文档中提及的所有相对文件路径、代码符号以及 ADR 编号引用。若发现引用的路径在实际文件树中不存在，或者引用的 ADR 已经处于 Superseded 状态且未声明继承关系，判定为严重上下文腐化并告警8。  
> 3. **AST 规则冗余扫描器（Linter Duplication Detector）**： 自动读取代码仓已激活的静态分析配置（例如 biome.json、ruff.toml、eslint.config.js）。利用词法分析比对 Markdown 文档，一旦检测到文档中包含对现有编译器规则（如单行最大长度、变量命名法则、未导入模块检查）的自然语言描述，发出信噪比优化警告，强制开发者剔除冗余自然语言语句4。  
> 4. **规则冲突有向图检测器（Contradiction Graph Detector）**： 解析各上下文文件中的优先级字段（precedence）与核心指令断言，构建依赖与冲突的有向无环图（DAG）。当不同模块规则之间出现语义正交重叠或断言对立且缺乏优先级定义时，输出确定性的冲突拓扑并要求开发者显式声明优先级全序关系1。

## **10\. 结论与工程演进路线**

自主代码智能体的引入，正在彻底抹平传统软件工程中“开发文档”与“系统运行时”的边界5。文档不再是一堆被动躺在代码仓角落里等待人类翻阅的陈旧文字，而是直接决定了智能体在每一行代码生成中注意力的聚焦深度与边界安全4。

面对未来以长期运行、多智能体协同（Multi-Agent Swarms）与自进化 Harness 为特征的代码研发环境，软件工程团队应当全面重构仓储治理体系，推进三项演进战略5：

第一，**严格践行“最小充分上下文原则”（Principle of Least Sufficient Context）**。将每一次向上下文注入信息都视为对模型注意力与系统计算资源的征税4。坚决摒弃“信息提供越全越好”的盲目直觉，建立编译器硬约束（L0）与自然语言上下文（L1/L2）的绝对隔离壁垒，实现上下文信噪比的工程可控4。

第二，**构建端到端的机器退出闭环**。认识到概率模型的不可控性，彻底淘汰流于形式的人文式规则劝导。在 AGENTS.md 中以确定性的工具链验证（Exit Code 0）构建具有法律效力的“完成定义”，以“情境+禁止+替代”的三元组构建负向操作红线，将自然语言愿景固化为冰冷、确定且无情运行的沙箱门禁15。

第三，**建立统一标准化的 ContextOps 流程**。摆脱单一私有 IDE 规则的绑架，拥抱开放的上下文拓扑规范与自动化 CI 静态审计工具链5。通过在 Git 提交流程中引入上下文防腐审计，确保架构决策记录的原子化与唯一事实源，让工程上下文与业务代码在版本迭代中同频进化，为软件开发走向高度自主化与确定性提供坚实的基础设施支撑5。

#### **引用的著作**

> 1. How Claude remembers your project \- Claude Code Docs, [https://code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)  
> 2. DeepSeek Harness: Why 95,000 GitHub Stars in 2 Days Matters, [https://flowtivity.ai/blog/deepseek-harness-open-source-agent-explained/](https://flowtivity.ai/blog/deepseek-harness-open-source-agent-explained/)  
> 3. Context Management Strategies for Windsurf: A Complete Guide to, [https://iceberglakehouse.com/posts/2026-03-context-windsurf/](https://iceberglakehouse.com/posts/2026-03-context-windsurf/)  
> 4. The Complete Guide to CLAUDE.md: Memory, Rules, Loading, and, [https://medium.com/@bijit211987/the-complete-guide-to-claude-md-memory-rules-loading-and-cross-tool-compression-97cc12ed037b](https://medium.com/@bijit211987/the-complete-guide-to-claude-md-memory-rules-loading-and-cross-tool-compression-97cc12ed037b)  
> 5. Best context engineering tools for AI coding in 2026 \- Packmind, [https://packmind.com/context-engineering-ai-coding/best-context-engineering-tools/](https://packmind.com/context-engineering-ai-coding/best-context-engineering-tools/)  
> 6. Coding Agent, Keep Me in the Loop \- Medium, [https://medium.com/@Farrimoh/coding-agent-keep-me-in-the-loop-2abb1952caf0](https://medium.com/@Farrimoh/coding-agent-keep-me-in-the-loop-2abb1952caf0)  
> 7. A Benchmark for Persona Drift in Long Agentic-Coding Sessions, [https://arxiv.org/html/2605.24279v2](https://arxiv.org/html/2605.24279v2)  
> 8. Why Does Windsurf Forget Architectural Decisions? (Fix 2026), [https://www.memorylake.ai/blogs/windsurf-forgets-architectural-decisions](https://www.memorylake.ai/blogs/windsurf-forgets-architectural-decisions)  
> 9. Archcore CLI — Git-Native Context for AI Coding Agents \- GitHub, [https://github.com/archcore-ai/cli](https://github.com/archcore-ai/cli)  
> 10. Prime Agent in SuperQode: Second RLM based coding harness, [https://medium.com/@shashikant.jagtap/prime-agent-in-superqode-second-rlm-based-coding-harness-after-rlm-code-b903f8839014](https://medium.com/@shashikant.jagtap/prime-agent-in-superqode-second-rlm-based-coding-harness-after-rlm-code-b903f8839014)  
> 11. State-Conditioned Minimal Sufficient Evidence for Coding Agents, [https://arxiv.org/html/2609.20050v1](https://arxiv.org/html/2609.20050v1)  
> 12. Extended Abstract \- CS 224R Deep Reinforcement Learning, [https://cs224r.stanford.edu/projects/pdfs/Leon%20Reilly%20Duy%20Nguyen%20submission\_416241040/CS224R\_Final\_Writeup.pdf](https://cs224r.stanford.edu/projects/pdfs/Leon%20Reilly%20Duy%20Nguyen%20submission_416241040/CS224R_Final_Writeup.pdf)  
> 13. Coding Agents are Effective Long-Context Processors \- alphaXiv, [https://www.alphaxiv.org/abs/2603.20432](https://www.alphaxiv.org/abs/2603.20432)  
> 14. Windsurf Rules & .windsurfrules Guide \- Design.dev, [https://design.dev/guides/windsurf-rules/](https://design.dev/guides/windsurf-rules/)  
> 15. Self-Improving Agentic Harness with Recursive Language Models, [https://www.zenml.io/llmops-database/self-improving-agentic-harness-with-recursive-language-models-and-continual-learning](https://www.zenml.io/llmops-database/self-improving-agentic-harness-with-recursive-language-models-and-continual-learning)  
> 16. Cursor .mdc vs CLAUDE.md vs AGENTS.md | Cursor Workshop, [https://www.cursorworkshop.com/research/agentic-coding-signals-20260311-0855](https://www.cursorworkshop.com/research/agentic-coding-signals-20260311-0855)  
> 17. The Architecture of Persistent Memory for Claude Code, [https://dev.to/suede/the-architecture-of-persistent-memory-for-claude-code-17d](https://dev.to/suede/the-architecture-of-persistent-memory-for-claude-code-17d)  
> 18. Prime Agent: A Self-Improving RLM Harness \- arXiv, [https://arxiv.org/html/2608.23552v1](https://arxiv.org/html/2608.23552v1)  
> 19. claude-howto/02-memory/README.md at main \- GitHub, [https://github.com/luongnv89/claude-howto/blob/main/02-memory/README.md](https://github.com/luongnv89/claude-howto/blob/main/02-memory/README.md)  
> 20. How I Built an AI-Powered Development Lifecycle Inside Windsurf, [https://medium.com/@easwaranvijayakumar/how-i-built-an-ai-powered-development-lifecycle-inside-windsurf-that-thinks-before-it-codes-d63d9a1678ad](https://medium.com/@easwaranvijayakumar/how-i-built-an-ai-powered-development-lifecycle-inside-windsurf-that-thinks-before-it-codes-d63d9a1678ad)  
> 21. README.md \- deepseek-ai/dsh-agent-instructions \- GitHub, [https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/context/agent-instructions/README.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/context/agent-instructions/README.md)  
> 22. How Claude Code Memory Actually Works \- Mem0, [https://mem0.ai/blog/how-memory-works-in-claude-code](https://mem0.ai/blog/how-memory-works-in-claude-code)  
> 23. AGENTS.md \- infocusp-fullstack/ai-coding-handbook \- GitHub, [https://github.com/infocusp-fullstack/ai-coding-handbook/blob/main/02-rules-and-memory/agents-md-standard.md](https://github.com/infocusp-fullstack/ai-coding-handbook/blob/main/02-rules-and-memory/agents-md-standard.md)  
> 24. Prime Agent: Self-Improving RLM Coding Agent (2026) \- explainx.ai, [https://explainx.ai/blog/prime-agent-rlm-continual-harness-primeintellect-august-2026](https://explainx.ai/blog/prime-agent-rlm-continual-harness-primeintellect-august-2026)  
> 25. DeepSeek Harness: Everything is a Plugin. \- GitHub, [https://github.com/deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)  
> 26. deepseek-ai/dsh-experimental-auto-review \- GitHub, [https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/experimental/auto-review/README.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/experimental/auto-review/README.md)  
> 27. Prime Agent: A Self-Improving Coding Harness Where Everything Is, [https://www.developersdigest.tech/blog/prime-agent-rlm-harness](https://www.developersdigest.tech/blog/prime-agent-rlm-harness)  
> 28. One Source of Truth for Your AI Agent Rules: Cursor, Claude Code, [https://pub.towardsai.net/your-ai-agent-rules-one-source-of-truth-for-cursor-claude-code-and-every-tool-youll-adopt-next-cd7f1353dbbc](https://pub.towardsai.net/your-ai-agent-rules-one-source-of-truth-for-cursor-claude-code-and-every-tool-youll-adopt-next-cd7f1353dbbc)  
> 29. Beyond the Prompt: An Empirical Study of Cursor Rules \- arXiv, [https://arxiv.org/html/2512.18925v2](https://arxiv.org/html/2512.18925v2)  
> 30. An Empirical Study of Developer-Provided Context for AI Coding, [https://arxiv.org/html/2512.18925v1](https://arxiv.org/html/2512.18925v1)  
> 31. CLAUDE.md \+ MemClaw: The Complete Context Stack for ... \- Felo AI, [https://felo.ai/blog/claude-md-memclaw-context-stack/](https://felo.ai/blog/claude-md-memclaw-context-stack/)  
> 32. dotcommander/repomap: Token-budgeted repository maps ... \- GitHub, [https://github.com/dotcommander/repomap](https://github.com/dotcommander/repomap)  
> 33. Using Windsurf Rules, Workflows, and Memories, [https://www.paulmduvall.com/using-windsurf-rules-workflows-and-memories/](https://www.paulmduvall.com/using-windsurf-rules-workflows-and-memories/)  
> 34. Windsurf Rules Guide for Reliable Stack Conventions, [https://blog.vibecoder.me/windsurf-rules-configure-your-stack](https://blog.vibecoder.me/windsurf-rules-configure-your-stack)  
> 35. Guardrails Beat Guidance: Rule Design for Coding Agents, [https://agentpatterns.ai/instructions/guardrails-beat-guidance-coding-agents/](https://agentpatterns.ai/instructions/guardrails-beat-guidance-coding-agents/)  
> 36. How to Write the Best Prompt: The Complete Guide to Mastering AI, [https://promptnote.app/blogs/how-to-write-the-best-prompt/](https://promptnote.app/blogs/how-to-write-the-best-prompt/)  
> 37. Context Engineering Suite (Antigravity CLI Edition) \- GitHub, [https://github.com/Apoo711/Context-Engineering](https://github.com/Apoo711/Context-Engineering)  
> 38. Cursor Rules: How to Keep AI Aligned With Your Codebase, [https://www.datacamp.com/tutorial/cursor-rules](https://www.datacamp.com/tutorial/cursor-rules)  
> 39. DeepSeek Harness developer preview: Everything is a plugin, [https://www.deepseek.com/harness/en/](https://www.deepseek.com/harness/en/)  
> 40. pi-agent · GitHub Topics, [https://github.com/topics/pi-agent?l=html](https://github.com/topics/pi-agent?l=html)  
> 41. context-engineering · GitHub Topics, [https://github.com/topics/context-engineering?l=c%23\&o=desc\&s=updated](https://github.com/topics/context-engineering?l=c%23&o=desc&s=updated)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAZCAYAAAAFbs/PAAAAzklEQVR4XmNgGAXkA0kgfg/E/5EwI4oKKOAE4jIg/gTE0UAcB8R3GSAauJHUgQE/EG8H4tNArIAkvpABogED7AHiW0AsjyQmyAAx4DWSGBjoAPEOBoiTYIALiOcCcS6aONgzUxggbiYKSAPxAyDWRBPHCVyA+B8Q86JL4AJVDHjCGRuABRsHugQuANOgiC7BAImsCUC8DVkwnQGioZIB1VmsQDyLAZJEzJDEGWSA+DoDRFMHEItDxZcxQELPFMrHAKFAPA2IuxggITcKYAAAHNwkLxPR9XQAAAAASUVORK5CYII=>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFEAAAAZCAYAAABJhMI3AAADdklEQVR4Xu2YW6iNQRTH/3KJIkpIeTgUUi4PbglFUZR7IZEXhURKREinkKQo10IpHlxTko4odpyOQi4lnhRyiZIXHiSX9bNm2rO/9j72Pjly6vvXv/lmzXeZ+c9aa9beUo4cOXLkyJHj/0V742zjM+PLzBhYa/xg/BmYowyajN/kAqUiIu4i40XjCON8449kPEeCQXKBEPF2sNXJxb0b+qCvcUHSz5HBRrmIF4yzjB+Nm4xd0ptyVEY3uQci4jnj2NLhHNVggPGd8bvxizxsc9QIwhcvJP81GkeWDrdpcDi2yxoDmhurGfvlItYbdxpXl4y2HvoZD2WNfwn75JFVMHYtHfqN5sZahHvyEmdC4FW1zoGy2Dgs6U9X69adHJYFlRdqsyqPtQgsBA9M+6eNHRJbOXRW5fzZw9hbHjKgznhf1aUKnq0VfYwdM7bmRCw3xnVPtSDEuxu/Gscltidyd5+a2CJYIJM9Yjwj967dwRZxw3hAXiJRvI83PpcX6vzymSIXmByceiL1aoNxa2jpgz3GW8Y1xuNhjHkDWvrLjY+Mq1QUAaFYy2HjJeNNeQqJYwUVRTwpT2u75JFZExCvoNIdWaLiQcPORCAqYY/tsXxBAKGmhWvGmCAYIz/tAR74KrQRsbQCiPpAxffQ0scO+C4/CADePzNcDza+D9ekotfGoaHPPNi8Ormw243X5GtNRSTiDoZ7IE7xpygsAepnDxK8inoRIU8FGzuINxxN7iFU8cw7KgpHnisXsuVEZAGFcI1HI0D0FFr62EE6hojrwjXoJN88fpq+UVHgrLcxN6IOsdOxIcZl8vfCpfL0UBV6GedkjQk4XGYYJ8nzXwT9T8aJoY/7bzEON841jg72FKmIeARIRVwhr1WpWUGsXaOIeHvMv7Rx01g8AoP4zMLQz4pIGiEysiLyHN//p+CDqWeQ53YE9peLFPNSDC12+618IfXBlorIu0gRMZznhX78RiURiaSYEibLw35l6NcSzpdVrEjIs61RnZQAD75uvCIXlJrshXGbfLKE93njevmhAOJh1GgcJc91TfIDLC6ag6RBnpNo6YO98tTyVO6ZtJ+DfWDok5IQ6az8Lz2wQX7AHQstB17cFJ7n28yBubAZD+Wlz4lwzz8B+bBSOVJprJwti2ruScHGxZCthGreScpKy7IcOdoIfgHROrylyBSD0AAAAABJRU5ErkJggg==>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFIAAAAZCAYAAACis3k0AAADXklEQVR4Xu2YWaiNURTH/zeUMTOJIqGUqSgp6nrwZkqGRFIUD6RQhgd54EHGpJRESMZIMiTlhCgUylCkKFEKJR6QYf1ae3f2+dx7nHvudXXr+9e/83177fG/115rf0fKkSNHjhw5crQ8tDJOMz41vsrYwArjO+OvwBz14Jbxu1ykVEgEnms8YxxpnGX8mdhzZDBELhJC3ghlA+QC3wnvoI9xdvKeow6skQt52jjV+N641tgurZSjPDrJPREhTxrHlppzVIqBxrfGH8Yv8iOcowpwlPFG4uFN4+hSc4tAjTw5/lfslgu50bjZuKzE2nToYDylpr9CDZf3OSVraG7clV9/xgde1r9NMoeyBU0Arm2NFZKNXh1+qwK7iSem78eMrZOyhqCj/KjVh+YQsq081vNbKeYYr8jn32B0Nn41jkvKHskTz6SkLKKLcafcTj2y/B656N2Mh+WhAi/vH9q0Ce/7Qv1noXyi8ZN849JjX0hsJL/F8n6fG8fQ0NDPeM14zngg1ItCMt5x4zzjbeOWUL5VPu/rxuXGS8aLcg3Ax2B/reJ9umIgYEGluzBfxeTTPSlHWEIA4N7JwKOM2+U7v18uKt7I5PFqFrVOxcnyfjY8AwRh4hF4ayE8Y8PT6DfaojcjBv1Gz+cTNgrJnGMbbiTp19oM+Rr4AMFjU09mTQVV6ZF4Tza5sFg8BzGPhDIWxeTxKsCgeFnX8D5UfolfJJ/gAuML47DwmyI92nExEamQ0cbio+2q3Hvx1vR2kT3aZHBOzyC5V0ZQh41jPbH/lcFWtZA9jdOzhQlIOJONtfoz1mQHjXfRJbFCQF/jy0xZQ4WMAkUbY5YTstY4ITyz0Wz4CHn4oQ516Tv2z1pAuqbGJq6KkRWSSe41npdvAEd5g7G9cZfcywHleHZEbxU9lnbcGArhvZyQxOeFoRykMZLNxOPAYPmx36SiQPUJSbvHxh4q72BNhh3Gz/Kj/yYp58gRKu4bD8rjJ0C8o/KJIsYD44lQv8a4Sp4YtslDCf3OVPGvuw/y5PFNngz4M4W+78k3a708XjOnpfKTdkE+HnMlOVIvnfeTQJ4pw0ZyfCgPX7T57yAMZL8y8AaSAMIRu7LoJW9DvUpjFH3RZ+w7HZMx6hrnb6CPbF85crQg/AYYXcgiR+JTBgAAAABJRU5ErkJggg==>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC4AAAAZCAYAAABOxhwiAAACWUlEQVR4Xu2WTahNURiGX6GIoki5CMVA+UnMriFlwIAJZeBmpPwMKMSEpDuQASliIAMMiIGpdEkZMKCEQn6SgUImJoT38a3t7L3uOeXe2p2j9ltPe+/1s3v3t771rS01atSoUV2aaHaZr2ao2qUx5r75lThjxlVGdFEvzA+FsYul9tnmuhkwy8xzc8tMKo3pqjA4qDB+yow12xQrcCCNIcqbzNz03BMiHS4pjO8xF8xTs7Q8qBdFxN+bL+aOmVLt7l2tMt8Vxrn+N9qvSJPLishPrnbXJlKU/TRqXTM/zQZFOVxU6a1HrxTBWp93jERE+Y2ZpYj+zkrvyLTFLMkb26jYV6M2znLx5ZvTM2WP6K/9O6K9mDfNTFXrQJpnHpoV6bkQ6cC4smaat6oaZ9wMM6HU1lHTFV8+v9SG8SENz3VeWBi4qogu5ZODqV+x/Mz9aFancRvNI3Pe3FVEGuXGCQQVbYd5YPam9o4isldUPcZvKlahPJlIPFEcUGig1fXndwER6XfpWuiE4oN4P3vptMJkbpw5i9P9QvMy3bcVL+BFeVosV5RGIHL8yxwxz9Q6Ob+Zs6m/qPvtjLP84xVGj6q1krlxAoJh2hco/o86imVblzeWxAu2mjl5hyK/UZ+5ne7LxjHJmMfpHh1TGCcwuXH6SNvaVV4lKhGijH5QrMLh9PxJkedE/YbC+D4NN87HrEn3iNJci+6ZQ2a3IncR5vjtpW+lIq8PmtfmpGIvUAj4AP6F2EefzXYmKzbxOXNcMa8WsT/I1bzMobyNavQvJ2RRYvNq1qir+g3CwXGGbac7rgAAAABJRU5ErkJggg==>

[image5]: <data:image/png;base64,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>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA0AAAAbCAYAAACnZAX6AAAAwUlEQVR4Xu2RMQ4BURCGR5CQSBSESFTolM4g0agUKjfQuoZOXGdpEC1xBIUoVRJ8s+8tY0OUmv2SL9k3/87My65IQsIvUljCSjz4RB4neMYNbnEkbshXlrjDlj/ry1cc+HMHc/45pIgnbNsiHHEtLh/boIx77NmiJ8ALznBqA12rQcMWPQHe8YB1G0RNBVv0BHjDYawebtC7f2paiRuog9/I4FxeX01JYxcX4q7Xx6bJn+immrifqk0RWaz6POE/PAC7XRwKxZpQiQAAAABJRU5ErkJggg==>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA0AAAAZCAYAAADqrKTxAAABCUlEQVR4Xu2SsUoDQRCGJ2hAIU2qNAmInSBEyCuYQtKZQsQHEexTiBLSiKWIEAiEYLo8gp2NkCIIttFCFAQr8ZubS9idU4Ot+MEHt//usbuzI/LPjyzhPvbwFie4Fa1w5PEET9NxDo/xZr7iC/bwTOznGYf4FowjSniNFZe38NVlCSvYxZrLded3rLs8oYwDsV0u8FGsAFNsBOsitsUuX8A23mMHn7AZrIs4wgOXaeV017HYfTMMsehDsSJ8iJ0kw7kPYBn7YpWrurkEfQvPJj7jCFfdnKzjHa4FmbbSC+4GWYSedwcfxPrtMv3WZ/gWvayiraNVUsM2yqCdcOXDRcwe9VdspP4VPgGrlSdPcEXDDQAAAABJRU5ErkJggg==>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGAAAAAaCAYAAABIIVmfAAADWklEQVR4Xu2ZWahNYRTHl1BEhoiEB1MikYQMeRBlyJAkUgoPPBhK4YGk5El5MERKoiRDSgnJgyRDCQ9EhkRSHlDiSeH/a52dfb5z77nf/g46sX/1b9/Wumef/X1r+Na+16ykpKSkpKSkKekh9ZM6hY6SP88N6a50Wvosdax2l9Shs9QuNMYyVroZ2KiCk9bATZuMbtJbabvUK/Cl8lH6YZ6sXLtWu+MgcmelmYF9sHQ8sIU8lpZI7XM2Fndd2pOzNQtdpI3SO+lE4Euhr3mXmGcNBGCSdM48EHnmS0sDW8gA6Zj0VFqQs3OvzdIO88xrNti0hdJtabJVJ1AKDQVgn7Q8sHU3Pw9ibzhcuiBNt+qWRQAo+/VWG+AU2Kg+5lX2O1ojm08QqGQCkkpyAEaYtx+ydIV5Jh+VHkjXcr8XC5syUbojXQ18VMtLq21ZMcyVvtqvauJ7dplXKbCOS5WfG2Gv9F7aZt6uYkkOAJm/OzSKqdK30FgANpgz5bw0KGfnZ2zPK/4YJkifrDYhxklXzCtrnbSzypsG5wMBOGzeBWJJDsARaXZoNJ+AXksdQkdBOBeoqkPm98wYaV4ho61+K6HdPJK+S7MCH/ejvY2SLlauqXAvsj91QkoOAH2baSeEkv5gCTcM4LBbKX2RNuTsbPoY6ZTV/w6GABZGj+4d+Hqat6WD5ptXL5CtQSJQkUxFqwNfEZID0NKYyUIOmGddCnx+mnTPfIF5ztiviSnmHOD5WNjW0GG+WNrknNBRBxKCoD6RLlta0FoiKQB8OeNn2GY4RMks2lNR2HCmCg5h2ksGZc20tcziNj6DjWdh4ZQGHOo8J2dBDByqb8wrZmDga5SkAFDSPNCUnI1NY1JhMipyCAGjKFlP9meZxdSSjaKrKrYiDDVvD1RO9mcRrgTkvvmiWTzBWFPxt8ZiS+vvbcHzrDV/Fp4jGiYdXsLor5wFZDylWXRM5Euz1pL/HBnHxvNC1sg7wHjphflhzCT0StpiHtxn0kPzNSzKPvAXYdNb0nWLqIZNlWv2cpOfUmLZb7WzPVdaDZufze2NQkWRveELGNnHnwPaXGyz0d9qX5T+dXiZo+XG6JY0xD/2Z5hhPgL+T/D/Dao8RnSEIm24MMPMZ/2SkpKSkv+LnyrsnWQjfYlEAAAAAElFTkSuQmCC>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAZCAYAAABQDyyRAAABSklEQVR4Xu2UvUoDQRSFr2gjsYsoFmkkjYhIEAsrKwsLwSIgBMHSR5B0ooVFSjtfwNbSH5CAnU0qK7G2Cj6BxnOcRWdvdmZncLPVfvDBcu5MuJk/kYqKinAW4T1s6oKHabgEt+CUqkVzAk916GEbvsIBvIIvcDM1IpJH2NChhw94IWYVCJtg1vodEQGXjysQygx8h8tWtgKH8DqpB8PB7D6GPdiHc1bGb2YjuGvlufAAcflj4Gr1xd3AsZX/sAbbGR7AJ9hT+b6Z5iSvgbHtdDVwBp9hR+WFN5AFJ9zBHV0IoJAG+Ohs6DCQvEPIeorLpBDql5nmZF3MwzNvZXxJ38RcRV5JLwtwVYcRzIr7HbhN6l64R/99uz9hV/5+h9/MvGeKg88l8JAEUBez30ewpmqZcNkfxGxB6fDf8zAe6kJZ8MrdSPrqVEycb8UjSbNnMc/UAAAAAElFTkSuQmCC>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAAAVCAYAAAD2KuiaAAAAq0lEQVR4XmNgGAWjYBSMglFANGAFYl8gDkWXGAkgH4ifAfF8IJZBkxvWQBiIu4G4E8oeMUAdiBcxQGI9GU1uWAJQ/o4A4ltAvAuIGVGlhzcAeR4U06AYB8X8iAOcQPyEYQTmc2wAlBoCgPg4EJszjLCsgAxAngeVBVcZIAEyYoEiA6TuB9UE3GhyIwqAygdQOVEDxHxocqNgFIyCoQ1AVZ0kCZgHom0UDHkAADyREuJT/eX8AAAAAElFTkSuQmCC>

[image11]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFcAAAAWCAYAAAC1zAClAAACOklEQVR4Xu2XT0gVURTGPwnFMNAsEiFwI0EWVJQtWrgSRMSNm4p2bdoE7gqCQIIWLYKohasWLlwUUS7FhUibRBduiiISLChwIVJQVNCf7+vMMPedxnmTEvKe9wc/3syZ++a9d965954BIpFIJBKJVKWZHqWn6R53LaSNnqGN/kIkn110lT5I/ERbKkYA7fQhXaH36RodDAdE/qaVzvsg+UCPBec/6aXgfD99Qafp7iBeF2haNvmgowFWlUV00rc+SN7Rk8mx7qPk9meX/ywdc7AKPhzEa55n9Ffie2ycwIN0zAcdHXSZXkTlfZ7TA8nxXvoZWbJTJmDfYdjFa5Zueg+2+XTBpuoC7QkHJYzQyz7oUFXegSVJ9zkEq9CBYIyquyi5V128ZrnmAwlKygyyiv6If9twXtEfyN6v+6UoqTsiudpIithHj6B8q6TKPQurVi0jj2EJew2bGUIb22aTq7VZlV/Gst/5vzJEH8F2+VF3LUSJrrYenoC1YSlpspW020lsK8vCDdjmWMawO9kWVAnrsH5U/eYbeh75m5qSUfTDxV266IOwz5iDfV7ehqY/YRKWXK3tdcEtH4D1mVfoV7pEp+g3Oo7qU20M9mDgeQJLfIqSeCE4T/tczR71ynWBloSN0PS9DlsyNC6vmj3qPvTAED4IqCrVnulaijqJp8gSqaXje/IaKaAX9iBxEzYDVP3HK0bYg8JLOgur4C+wsWX+wB3PKXoOljgd56Elpg82RptlJBKJ1Cu/AYjXcEO3GD+cAAAAAElFTkSuQmCC>

[image12]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAAAxCAYAAABnGvUlAAADsElEQVR4Xu3dS6h1YxgH8CWUayK5RHxKihQyUhiIJJFkQMwZmGCgZCop5ZIMRC5lQETJrQy+mIiJiYnLgFyKpIRCLs+/tXbfu9/Wds4+ZyNfv1/92+t91j5773NGT+9ln2EAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAf9QRfWE/c3RfAADYrZsqb1QO7+p3d+NN+KgvrOnAypuV3ys/Vs6q3LH0jHnPVh6bcvtUu7ip7Zlqqzxa+bzyRH+jHDWM9z4Yxtc5oPJ6+wQAgJ06dxgbmfiyclVz7+zKu814E26pnNYX15BG6NOulmbzu662yp/D8uzXJZUbmvFW3qv81hfL05U/utr1lfO7GgDA2j5prn+onNmM06xtuuHIrNhuzP38kZWH++KMk4axYVt4sXJoM97KIZUrhuXXiNsqN1de7erxRV8AANiNNCKZwWrHm5SZrbf64uT5ytuV+/objVsrv/TFYdwPd0xfnHFPZW/l4Mr3y7e25dJhbNryd8lj5L1Pr3xYuXCqtX7qCwAAO7Gn8tUwNiLZh5VknCZkTpq66/4mV+576pLM1qVp6mVPW5qo+KxybHOvlWXPuZ/frq8rD1QuH8bf9fjl21t6aXrM65w8XT8+Peb1DpquW/kb7u8HLACAf8kjwziDtZDlvRub8SZcULmzq2UJ9v1mnMbnxGbcyr12j93HlV+n+kNNfZU8b7EE+sowHrJYR2YBI7OE+RxZBo0stf48Xff2Dho2AGBDsmG+3c+VBmRV43TYMDY/q/LtvqcuyQzbYkZq4cnK1dN1Tlr2G/dbma1qm8p4p3JXV5uTxrB97bzXqlmxOdknt1jyTNN5f+W8aZxZv/weczJj2J+8BQBYW2aI+s3xaWayTHlv5ZTu3k6lcWln0yJ7vHLKM3L6M41U5ABEf0I1DWU+10K+ziOHEPL5FzL7NbfPLQcMXmvGWdbNac9nmlqkoWzfI/I1Is8N46nZyF62xV68vM43U23O3IlSAIC1pZk5oaulaUkzlKZok9pmKs1O3icN0XFNfeGFvjDJ12VcMywfkGjtZp9bbGopOAcT1l12BQD4z11UuWy6zhLj3FdhRJqxNGY78VRfWNPLfWGHHhzsXwMA/qfyXwWy3Jr/onBOd2/hjL6wTatOmG5Xlm1Xzdyt49TKtX0RAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAVvsLbt6Ko98fmJ8AAAAASUVORK5CYII=>

[image13]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAAaCAYAAABhJqYYAAAAvUlEQVR4XmNgGAXDEzACsTAQC6BLIIMcIH4OxFZQPkjDciBmgatAAt+AOAZN7C0Qa6KJMXAC8VUgFkES4wDir0BsjCQGBiCB+QwQ98KAOAMWxSAFS4FYH1mQAeKHBjQxsNUgJ4A8BAMg9ikglkESAwOQNSDrbKF8VgaIie9gCpBBNBD/B+JLQLwSiC8C8XEgVkNWBANzGCDBBvK9JAOeyACFISgs16BLYANBDBAnpKNLYAPJQPyUAUssDVIAANpQGtveRk7iAAAAAElFTkSuQmCC>

[image14]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAaCAYAAAC+aNwHAAABD0lEQVR4Xu2SMUtCYRSGX4mioCBoMEEw2or+gJu/IMTJwcmlf5DS3C44Bv2BpiDaL7k5G+6iOKng0OBi78sR78e5XXEKBx944N7zft+538c9wJ5/4ZTm6KGr+/cEz3REl3RKf+gjPaEFehMvjbmkX7BNWui5oF1YnkBde7BQX0rjCSkNPmDBGzbfr0Invii0eUbvfOBQg8gXq7AG9z7YljYd02sfbMMx/aQdeuYycQ6bA+8aDUq0Us8hR/SVDmBXlAv6HS4SD7RPsz4I0OYhzftAqKgFNR+syMByXVVX/hP9Qh2vTg+CuiayCWvQCOoJbhGPqZq90Hc6h/2lFi2uV6ego17RMmw2Sthw5D27wi8+zTJI8BVOgAAAAABJRU5ErkJggg==>

[image15]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAaCAYAAABVX2cEAAABA0lEQVR4XmNgGAXDF4QA8VIgnoWGPZHU1GORxwsmAfF/IGZElwCCeUA8H4j50CWwAV4gPswAMQwdKABxHAN2S7ACTSB+C8Rf0cSdgPgkmhhBEMQAcdVVKJ8ViMuAeBUQS8AUEQOQvRgNxNeh7PdArIOkjigA8+I3IJ4AxOZAfIIBYuAUBhLCCgRgXgRhUIyBQA6U/wSIFaFiRAFYklgExMxQMZABIINA4hFQMYIA5sVPQKyPJmcJxD+B+B+aOE4ACnCQ7aeBWBBNjhOIdzBA5FnQ5LCCtQwQxeuAmAtNDpQ8ehkg8o4MiCDAADAvwAIehrdC5WHeR5Z7BMRyUPlRMAoIAQBI/D4BSBlYLwAAAABJRU5ErkJggg==>

[image16]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABYAAAAaCAYAAACzdqxAAAABRklEQVR4Xu2Tr0sEQRiGP1FB8EREwaDJJgaDVU1mwatX/AsMFsHsBauYbAYxGLRYVPBAMBs8MIrFZDSJP96Hbwdndvc8z2LZBx6WmW9nduadWbOKim4sy0P5IJ/kWlou0DR/D+/kflouwoAzeSWHc7XAtLyWn7KRq5UyJE/kumzLiaTq9Mkd+Shf5GxS7QAracl5+SxnkqqzZD7xm7yRI2m5nBV5LMfkq1xIyzYqD8wXQAx7abmcEMNi1mbg5nfZ5swPaFBO2R9iYBDkV8SkTA58vOcYBrI2Ex+ZHxZsZE/Ysl/GANvmAwJk3JI1892QLxDZuaxn7R/JxwBcN3Ik592on519WA8xnJqvJsAPQhz35h8OsCv6u8Ip38oLORn183u/y9Wob1xemk/cH/UX4LqwXV4MhkNhZdxZPgzxO8H4OlZU/AdflO9DmAJ+dO8AAAAASUVORK5CYII=>

[image17]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABIAAAAaCAYAAAC6nQw6AAAA90lEQVR4Xu2TvQ4BURBGR0dQ6HRCNESi8hAKaom34AkUXkBJRKg8glKi1ChFohGJSiSixjeZ3bt3Z3djW8me5DT7zf2ZO1mihP+nDefwAC/wCJdw6jiCVVMdgwn86I8gC9ck2VBlAXJwS+EbMQ34gFdYVpmPCrzBuw4c8nBHchA/RSRdkqK9DhzsGw/8kYdd1PdHhhrJbbmmozKD3RYvCIMP4E2esKkyg91WQWVMCi5IajYw4489xiRFPP4weEo8La7pqcwQpy0e+wmWdGDzq60WPFP0IYYZyUb8S7ikSR50Bd+waGUBuJAnwJuE+SJ54Lq7ICFB8QXvKTx5AgmiEgAAAABJRU5ErkJggg==>

[image18]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAAAxCAYAAABnGvUlAAADa0lEQVR4Xu3cO6gcZRQA4BNQiCi+GhGFIGkUCQpWPoggFjYR0RSKdiI26VREGxWxUMQiCoJoo4WNViKIWGyRKiliY+OjESFVlBSBBJ//cWa5//13Z+/sZiyu9/vgkJkzj51MdTjnnxsBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/5kr28T/1OVtAgBgU6+U+LmPj0p8UOK1bWdM68tqO4ua49H95rex9RwZv5Y4tHXqju4tcb5NDtgX3XP83cfY4upIiQ/bZCXv82K//Vl9AADgUv1U4uFqP7tgWchkYTOlG0rc0m+/XeKJ6tjFEndV++u6EOMKtmtKfF/t5//zsmp/lVmJX9pk5c8St/XbT8b07w8A2MOyaLmqyc1KPNvkLtUX1faP1fb+6J5hU6+XuC/GFWxZnGYxtYkfYvg5f4vtxV8Wa1O/PwBgj7qpxF9tsjgV3bhySsfaRC+7e2fb5Eg5hnw/uu7cUDFVy3PzvM9LHGiOrZJFZRZ6eW2+s1p27G7uj9WMRQGASeSaq3pd2VwWHw+2yeKREkdXxJDHY3hEOCvxRpscKbte6cZYLJiWeaHEOyWubQ/sILtlWbTNYvuzfhPdGPSOWOzw5fh3PgIGANjYmVgszLLIGFP8rOPrNlHJ38oO1bqeiq5rl4XiM7HzM79U4tE2OdLp/t8cveZ6u/RJbL27/CDhu367NnWXEgDYg5Ytus/1WEPjwhyf5jVDMSRHlrngv3VdrL5uSN7r4+g6axkHo7tPdsGGtL9zf4nHmtwy+bHE3dV+3ie/aq2vzU7lrNpPec0VTQ4AYC33lPij2n8ouoLs6io3pXfbRHQdsq/aZCWLoxynzv0e3VqyLCpbee4DsbWe7dPth//NnSxxfYmnS7xZHcuRZh6vi8rboxt/Zhey9lwsdiVfjm7d3+Eqd6LaBgDYFV5tE9EViO0Xqq353zZL+dHAuVi+Hu756Makc23Bltdk8Zfjy2Wy25fdurk7Y7GIG5Ij3beq/eys1V05AIBdIYuYXAO2juxyjSmYWpsUTPkxwlTeaxMAALvFqvHnMre2iZGy0FvXlKPgZeNfAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGPAPG4Z//0v3KfgAAAAASUVORK5CYII=>

[image19]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAZCAYAAAA4/K6pAAAAyUlEQVR4Xu2TPw4BcRCFR5CQqBQUohGNzglUCpULuAVnUGiVGqVOtpGIahOH0G40LuHfGw+xI5vMqhT7JV8zL2+2+M2KZPwfTTiBi6cBPCZ4hjPWyBrenF5gD+YeTdCFe1h9DUABroSF5cf8iwrcwbGZN2AkXDCKR3HysGiHYCosh8KPpCYULpibuZuTcMHQBl60rEtaNvCiCzawZAMPHXiFfRt40WeLhE+ZGr0uPRz1fWlpqMMDHNjAQxluhbf+EzXh39i2QUYydxtfLkTVCFj/AAAAAElFTkSuQmCC>

[image20]: <data:image/png;base64,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>

[image21]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAZCAYAAAA4/K6pAAAA4UlEQVR4XmNgGAVDC1gD8VcoNkaTIwpcAeL/DBQY8AOI/zGQaYAsEHcxkOkFbSC+ywDRBNL8DYhNUVTgAaxAvAqIpzMgDACFgy+yInwgHIgfALEKAxkGKADxbSDOgPIlgfghAwkGzAfizUDMCeUjG1AOU4QLmDFAFOLCCxFKMQE/EO8BYhkGiK0wrAzEhxkgBmyFq2aAhHQNEnsWEN9CSKOAOQwQA64iC9oA8W8gjmaAmPyeAeIFbCCdAWIASL0CAzRBgWwFxfNHIPYBYkaoYmwApLaEARIG3GhyYMlRQAYAAPwgNriYHq4lAAAAAElFTkSuQmCC>

[image22]: <data:image/png;base64,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>

[image23]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA0AAAAZCAYAAADqrKTxAAAA5ElEQVR4Xu2SvwtBURTHjzBYKaUMJqUMNlEyGUl2UTaDTP4OySAmk8XiPzD4E0zkT5DYDOJ7Or3rvNt7GGx86rOcH++8c+8l+vN9knAG78qxq0IRhD14hCPYgVuSpoOqMwTgAF5gXsUbJE1DFTNU4A0uYUjF+7ALIypmmJN88QSLVs6XGskkZ/E1zOgCL3gnbrzSszHnqvCgDPdwRfJ7MXfamzNsk0x8C5/UAhbsxCt4Wb7MhJ0AabiBTTtRJVm6ZCfADk5h2E5kSe6Gd+JnE4dRkpcwIZ9LdeCJLViHKfrwQH6aB7x4KICnLANNAAAAAElFTkSuQmCC>

[image24]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAAA6CAYAAAAN3QXmAAATDUlEQVR4Xu2cDex3ZVnHL6ZhlqUpK5sGPCiUBailKIwCDcVgmopFrRdQV0oycTItWnOPY2yRr4WGaAbVLF9Y6sDobXBSF76wmRtKq1zWwKYOnQ6doL2cz+77+/yu//U/5/fy/J9/PI98P9u93zn3ebvPfa7rur/3dc7/H2GMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxG/Ggsbyz1H1zLIeN5QfH8uay7e/KuviTsTxsLB8Zy/3Ktt8cy5F9Wduou6MvH2iOHctVY/nfVB63ZY+IXxjLjaXutrE8uNRlPjaW55XCef4t75T4vrHcPZYH9nX686bF5lmeNpZvjeX+dYPZFX5iLD+f1n84LcNFY/mOUgfYPM9YyJ7xncp/xKJePkBd9ZX9hXv4o76MDdc2TK1fOpbXp7pnjuW5ab3yB2P5n7F8d6qb82Ha8JpaOXLJWJ5QKxMnj+VTtXINbh3LB8fyiLqh8F9jOSpaf/16qufeadsUQzTfXRfOxfkz68Y7jvurWlm4diw/Ey12X5fqsae5dv5StNgsaM95aX0Ozv8vtdLcN8DRMZp7xnJa2bYbvHIs70/rdbClfGfafl+AQEq/CJyegSfztf6L8+PYfxOLAQvx8cW+nOEcnIv9/r5s4xwKJAwqR/Q6AsxOeWQsniXXeFY0+1o1EH6jVkRr/2P6MkG93of6pTLUis5lY3lGWqd9ta+nYFBE/C7jnGhtXAaDV7X3+6LNV+g3+k8wSDLIiiEtQx4Ify/adsqXxvKhtP7f/ffT0Qa5J8eCbOtfnajbCfj0P0Z7tv/cf8+OZmu/3NcvH8sbdUC0OHxlX9aETULje6PZ4Bm9XjCR21vq8j0cnpYBQfjYUgef6b88B/w1869juWYsb50oN0Tz7coPRZsYrcPt/bc+c+JSFt+ZO2tF4tfSMkLqP6PZxReiTRQZf6i7q6+zzO+P9mMqtIvYuAzda43dy/oAoaqJI3CNKiornJ+2roJJfJ0QcH/4gzkEYRDHiE/p628ay18sNu8aDLAYXYYAw2xDIF4QIE9IdQcarjnUyhnyjBdwmFUOvAkEEvGGsVw9ln+Pdp0Ten0VbJV/GMuJsTWYcg7OxTLHv7vvS7aIc5w5lpPG8rlenwUb9RJKO4Hg9dK0rmf71FQHF0cb5AhYf9nrCDj0wVzQBgaxOohQhrRPpgasdQQbs/wsqJehwWcZU0GXwamK0d2GNuQBchn0aWaTY1eBgMn9xgCKTxCfuM5ZsXieN/ffLNgyPMscX+YE2MujbSPuEQuV6dD+1P1OX94f9kazZ9rygf6LDeX25awPIoKJDvdEIUuMX7LPFTE92cEviNk/HguB+k/RfELr9GUWaPU8tIW+rvUC4SXbpy3VbrPgyBBvlmXGBffPBIp7Jh79ajRhTYxAlGF3PPMv64AO51dfTZU8uWKZPiF7L1HG5AD74nm/pdfNsUqw0YfYEdd99FjeM5a3j+VV0fqfeyDu0HfqZ/rmr/uyWEewIayPqpUTEDtvrZUx7zfmIIcB8sK0/t5YzxB2ypxgq8EfA8dxd4sLoqWw1+EdZZ2gS3A9EDAwVMetszRYJdiAcylgEWgJEAQQ1T2k7/eiaOdgHwYT+pqgcku0GSHLzP4IaDsBUcZgI+gz2sSr0PwKBz7cfxGVP9uXCaoEv++K+SCzSYaNwaUGMc6b+5pAV2GwkM2eGsufPYH7+2tlYUqwkXmrdbsNs/B1BlW4rqxvcuwqeK1Nv2UYuKYybNgr1IGHzNSTesnP8Oj+W58rNs45eJ7PiTa5oU72T+YoD7CbgJ8NvZBlw5cQHZ+NecHGdbke5V1jOb7X1Vd5tFcgdC6Kra+Gr44mfo9IdXBstKwefpZ9D7G8bDJCRi63N9soz//jaV1QnwUWgqlO0ARx6CnR2sYyWUeWKRLRUz7Os1sX7o9+IgGAcAOyhghyzoNtP7TXiz+ORfZzlWBjO+MpbaY/eQ3M8oujvU6m/4b+K3h2L0nrkAVbtVfgOecJ51Wx3D6nspDVb8whAk5wfq2cAeMhCDyqbtgP1hVsGDTOReC6t9nNgRQnrZmsLNiYEdL/cmREB477/L5OgFNKn8AoOO89sV1sAs+S7TjuE2Nx7pxhq5CR2KQfaCMz9z+M9gwZlF+xZY8FvA78/FjOjUWWiddHZBkEWUFe/+TBCWjTMFMqCONhLL8Yrc8on4vWT3ptUgdpBu88kcEmlwkVhBeD5jKmBJvqDsZgil0NtfIAgW1/KrYLjDnBJr+YGngYeGkrNoJA0kSFDNPfpv1giHYOrs+Arm8T5+wfyIJqwF+XC6PZtAQL7Z8SbIi8nK1iG3bI7ympXhMbIAtVhQQDOvdAW6fI94cd/1lfpk2cL/sX2/N3plWwzZEF1tHRskII6SkkSiE/8z2xeNVb+5zM4tz9ASJJ0H7iq/qaWDNEe+453nHvZHIFz0n2VQXbOdHipkBYyi5z7L4m2rU5D98aZrgn2kRMUiy6K1rMZJnniNDPr2mJT7QbeDa1XypZAIopvzGHAMwINKPjG4tl3FIrdsC6gg2jol6C48po6fJL+jIgPHBA6nQ8GRmuQRYEByDbgRNQR0DnfqljkB7aIfsGamZGL4z2wbpmnRJD/DJjOqOvy4F5Xco61wKupWvQx7SNdt/Qt1cIZhosBP3DgMPrDvpA1xq0w8jX0zLkQMz+zHA1ONB2zSB/IFq7JNjy695lgm1/IVAxuxUMQnwvVAMYEKCArKBsk2BIxuHIaEFcwXAdyNDe1pd5HgivYd/WBn0wd04Cc86mId6YQa9C30PNMSXYmKAweEG1VyA7wGszAvAn+jrnwT+wH+rkVxyLSOG+sFm+6cLe+f3daOKYes6N38gfePZ/Gu07P30TKf9hAMGOWM/HnhDtWNZZJlOW/WHKbzO0k+sJvtWin98bTWRhE/jBEO3+5At54GHw1Gt02fPQf4H98oDL5ANbkK2/LG07kPaPz722LxM39sZ2wcb9Q22j9jtsLM+ORdZJ2dsfG8uPxNZjECr8gQL3gD0hXiu6P/xQcQ0/4fkiArArUbM3Emw8HxXWfz/t89G0DJyXrPkU+DM+xnmJSxJs9MlvxOJbtJrFw0ZyOyvEPvotw0Sq3s8x0a77/FIP9P+cYMvgez8ZbX/aJcHG2wtsjCwab3JyZpQ3HLS/jnlcowosQWY53xP3OPV8M4jFKmyz35hDCAYyHGYVGPSqv/JZFwJCTukKjKgarwTbEO0vxBBngiCBYyB2BE5DwMqz9b2xmDFq4FPAwzGGvsy5WM7Owv7cu5YzOFZ2YDJBOJSWcWKcKYsqBnHEZSXPRuGT0T6+x+mBPtC1hv4L9TgFYu6XQMov59DgQL/n2TPnlONqMGDwJxCwzPnzLHJT+Jbmz6O15X3RBgZEAOKLPuIaEgVwU7T+efpYfqvX6Z5yWyuHp2XtP4UGxiFXxrxgw4ZygHx8rP+NWbWXigSbZtbYMROFTLXXfE5ead0ZzWd4rQMMDvQf4oYBAX56LMf1ZWxbPqRX49y3/C77AyCYEF/0Qd0G+Vj8WrN9lvVXy1N+W+Ec1feBb1qzWB6iDbBviCZG6sDD4H5uLJ7ZsNi0TQwJ2csDYuEDsn/EcZ7MbALPB2FPxozz6Ny5fCW2CgjaiC0MvTCJxE7oG8Ul/Fd9cmxsvy+OB93X1B/xTPkIk9OTotlQ9smKBNscZ5Z1BDfnnQPf1fPPseqOaG9zEBwIm5xpn0N9yfOvAo9+o6+WlQrtUf0ywcY9KIbkZ0X8pC1XR8ui5Uk59iFxmpkTbIxtmStj6x/ozEEmcih1TLaIyeYQgtdTzADWAQMi+NSAQ8kD2ipOiDazzyleQRCpxst1MXoGHwyZLGC99jujBRAKgQynoUxRA80qwZbbVI+tgg20z/X9l2MV/FWyYBI1U8Zz0SwNaIcCOfvyS5kTbHlGlYPgnlgM5DAlgqjTeXYKQQl0z1PnJfMibo2FQBa6x6m2iiEWxxHoFYDp+/qqGYayrmC7DO6BLITA9iRKpqj2UpFgW0beThtZz7ZE1gUY+NlGlot20WdTQX+V6KrbqeeZce26DfKxQCYMG7siFgPsnN9myAhV34drow32F6a6N0XbXzad4bz5Ly6H/ou4o3+y7Yspm5yq2wlDTLe3Pn/6OccU+a5EwFOjTbJz/+VjEF3V15hk5Ekt5PvjXBdHe23IMqK7Ph++H6UdiC/A7iQaj4h5v0RQVFHx6bIOU4JNdgf0k9pEBkuTnFrYj08mqj8jIrP9TRXslePzd2ycYx3BBnOCDcis8twq7Fftfk6wZfAJnrU4KrbG0YzGtQx9SZz87VJvDlIYSGuwYHaSZ8IZZgbrzHDWBaeqmSYctBrvEAtnPTm2to/2ch/H9XUCCIGJoDzEegFylWCjnRrwdezQf6cEG7Mo+un4vr4ntoox7qMGQ5h6fVYFm6419F+ogo3XVvXVag6ClSkRtEyw0d+X1MoVIPTf3pd1XgaVO6N9RzYF4uvSaH2lQJfb+j39F9gnZ2zn2p4ZynoN8BWuQdazQuZLGY3Kqm9LNhVsPNe6P8+DwUDwColXfWSYn5XqxSrRVbdfFi1rjK/mbbLFfCwgjPABBJvsfMpvK7wuqr4ECD3ABmgD57wu2jVl04ojvB5EMGb7H9KyyBk7mLKXqTrx8Nj6LyPWYYjWB1MCI7NMsL0g1Wd0zKOjZTb1mvLuaIIX38BnL9AB0e5vb7S/jHxPtGdC3xLvEC8VnmmOR0CsgaOjCQjOk6E955Y6kL/KPmCZYOOesmBbB+yJUqFNiF5Q7PyVmH+1SnsOhGCj/2/ty5n9EWwIyqkYTNbstbUyWrv05keQfTym1JmDGIIcTsCD5IGSWkdYLHOKC6M554EAQ84igjYQAAgqLBNUPxEte4bDCjIcJ/blD0c7h7Ie7KfZNQFBKfFT+jbOyT3LAQlSOMvN0c4jwXZj387MMGdUFDQQH/Qfr2UQFYgLsafvl+EVml4TVMcR1Nd/W7GpYKP/aB9/+aTMFpzX66dYR7DlYxEHVSQug0B+UVqv5z0/FrN2AhF9x+CsQZ2+0/PPbc2vDhnAEYAMKpCvMcdQ1hVsp6AvyUazj2biDIgf6fW3xPb/gYV95Fcy3Fee8LCdV4XUY5fZhkS1V2BW/eq+TP+9OZoNK4AzQCJc6DN8gH7klRy2jLhkX/xK18PG6D9m5+zLQME1WaZPWVbGhkwKGUvWT47txwqOyT4L1W8rnBtxkcUWbSQ7BEzKuF/5YxZsOYPKM8x+NKRlcXlZn7KXXFcnQIi1z5a6VQwxPWmqsYJnPSfY8iCe96nHiKn7Ap4V1z0q1SFC8TuQ7cjv8XmymlWwibf1X3xB93h2tIna8dF8BrvFZ/gsggzb9bH1n8VmwaY3ObSfe2Oi9LDY/i89lsG5a0KA+/piWq9xDAHNhCdDe+R/U4JNnxWAYgj3wX7cAwKYfsb/GCvoB/UrbCrYEJZkxRivOT/tpV9JVNwUTaTv2bd3g+fHpwUZ9a05hMBxMaCnx/YAOwfpaL5LwuFVSJdvShVsm8BxDD6A8VNYrw5K/SZGKcGGs3C+qfZNDayV7MSCti07lgEwOxXXp4/IcAAOVoMFKDNHQMgBGJGKgMvPSeXoxW77RBADv2bmCBAcn2UGUY7huW8KQVvHMSB/MLYPUJAH8GxL746tfzGnVxYq9OnFZR8Gj3q/KhIeMKRlWCbYgMAom6tgZzX4EyTJNmWmnt/+gN/SXtmn7J66PBioLt/3KrD9IebtlXNN2Xcmv1LKZL+dAps7Na1nYYUdvS6tnxZbn62yZkx88mCH8Kh2QN15aR98C1Em+6fI/ikc83P79t4/hpj+pIRzZ7L4QqSynQkD8aHeh3wlH5PhvuZgwBe81q/+jejX5PJp/Zc+qm2g3NO3ZRDRp8f2mJzJGWgJNiZismEyYWQABWNVfbWbwQb0aQATvczpY/mpvoz4Q1xOZcA1IeAPUIZo4vJDfZmJPWMfyyqIPJIKoBjCq2VNmBHCT+zLgOjM/bWpYMN/GK+nxiZAINc4xnPMMRIs2MxG7ESw7RZZsN0bbDKDNAc3t5d1XsUsEysHCxJs9wYvju39ZozZfxC/iNOKBZvZCGbL/OXUwUSeYa/KIuwGZDmZRZpDm5rthLPK+sEINi/7z6+c/z+h3+g/Y8zOIXtas+58mpC/+TXGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY4wxxhhjjDHGGGOMMcYYY8y3Hf8HXPBQQzKveO8AAAAASUVORK5CYII=>

[image25]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAAZCAYAAADE6YVjAAABVklEQVR4Xu2TvyvFURjGH7GIupFFKVF3kU0pZTBYGViUP+HahJj8DTJJyW63SHeyGGSw2EgZTZQknsd7f5zz+jrOnZS+n3q6Os91nvfHuUBJyV+wTn1QS95IsElt+MMUdVjIjjtP8Y7OisIdLOSE6nFeEdPUMzXljRQvsJAbash5nlHqFlbYsPOSaLZ1WNBqbLWoUGewgAPqOLbTDFAz1B4s5Ci2W+jiJ9ioFLAV22lmYUGLsJDL2P6ii3qjlqk+WEcdLX238TlOPcIWGqKANViA0M60OxWXheZ83vi7H+29hOhydaEwMUI9IPNl6Z/2Ec9Wu3mFXTAP28Eh1Rt8Rx0oNOtljVFX1GRw1uzmGjY2zV7dhizAus0KUQeq0v/4VmCXFAWIX0M0T1Vfo+5h4/Gom1MUB4hmSJWaowYjFxZygZ+rzEFPeJuaQPsxfENGtz8s+b98AvEFP3yO3EVdAAAAAElFTkSuQmCC>

[image26]: <data:image/png;base64,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>

[image27]: <data:image/png;base64,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>