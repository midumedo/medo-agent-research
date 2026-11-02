# 第 1 章 品类边界：decision model 与 LLM 结构化输出、专训分类器、规则引擎的三角分工

## 本章论点

decision model 既不是"更快的 LLM"，也不是"更聪明的分类器"。它是一个**标签空间在推理时由请求定义、类型安全与概率校准由权重保证**的第三类组件。它的边界不是营销话术画出来的，而是由四条不可协商的约束推出来的：**不生成 token、不提供定制权重、只吃文本、只对输入计费**。本章的任务是把这条线画准，并明确指出哪些需求应当直接判出局。

用三句话把它说白：① **它是什么**——你给它一段状态文本，加一组选项已经预先声明好的问题，它直接返回答案与概率，不生成任何文字；② **它与 LLM 的差别**——因为不产出文本，它更快、更便宜，也不会格式出错（它根本没有"格式"可错）；③ **它与分类器的差别**——换一套标签不用重训，把新标签写进请求就行。下面三节分别展开这三条边界。

## 1. 三个原语：语义差异与业务映射

decision model 的表达力被三个原语锁死，先认清"拿不到什么"比认清"能做什么"更重要。

**Choice** 回答"是这几个里的哪一个"，最多 255 个选项，返回 `choice`、覆盖全部选项且和为 1 的 `probabilities`、以及描述分布尖锐程度的 `confidence`（0–1）。它**拿不到程度**——官方明确 Choice 不适合有内在顺序的判断，那类需求应改用 Score（[Choice 原语](https://docs.typesafe.ai/primitives/choice)）。业务映射：工单路由、文档分类。

**Score** 回答"落在哪个档位"，接受 **2–10 个有序等级**，返回的是**概率加权均值**，因此**可以落在两档之间**（如 1.43）（[Score 原语](https://docs.typesafe.ai/primitives/score)）。它拿不到两样东西：一是未在等级中体现的维度；二是"分布形状"——score 同为 1.0，可能是概率全压在一档，也可能是首尾各半，必须同读 `probabilities` 与 `confidence`。业务映射：严重度、优先级、阈值判断。

**Noul** 回答"这个命题成立吗"，返回 0–1 的为真概率，**没有独立 `confidence` 字段**（[Primitives 总览](https://docs.typesafe.ai/primitives)）。它拿不到选项间比较，也不表达程度——官方特别强调 0.5 只意味着"是/否概率相等"，不意味着"中等水平"。业务映射：是否含 PII、是否要求退款。

一个容易被忽略的机制细节：**同一请求内各问题的答案相互独立**，一个问题的答案不会成为另一问题的隐藏上下文，因此增删问题不影响其他问题的结果；问题 `id` 不发给模型，完整问法必须写进 `instructions`（[Primitives 总览](https://docs.typesafe.ai/primitives)）。各问题之间因此**不做联合推理**——官方把这条写成设计原则："控制流、确定性规则、副作用留在代码里"（[How to build with System One](https://docs.typesafe.ai/concepts/how-to-build-with-system-one)）。跨问题的组合只能写在代码里。

## 2. 非生成式机制与 RLCD 的后果

Jev 一次前向、并行输出全部答案，不生成任何 token。训练目标上，官方把自己与 LLM 对照得很清楚：LLM 用 RLHF/RLVR 优化"人类偏好的文字"或"可程序验证的奖励"，而 Jev 用 **RLCD（Reinforcement Learning for Calibrated Decisions）** 优化"校准过的决策"——官方原文的措辞就是 "training method we call Reinforcement Learning for Calibrated Decisions (RLCD)"，其对照表中 LLM 一栏为 RLHF/RLVR、System One 一栏为 RLCD（[发布博客](https://typesafe.ai/blog/introducing-system-one-models-and-jev)）。需说明：ML 文献里 RLCD 另有通行展开（对比蒸馏），本文一律按 TypeSafe 官方定义使用。

后果有两条，都是选型者最容易误判的地方：

**第一，它不能写报告。** 官方文档直陈：System One 模型"不写回复、不产出代码、不生成关于自身推理的解释"（[System One 概念页](https://docs.typesafe.ai/concepts/system-one)）。任何"顺便让它总结一下""让它给个人话理由"的需求，都超出了品类定义，不是调参能解决的。

**第二，它不该被要求解释理由。** 这是本章最需要提前说清的一点——很多团队第一反应是"它为什么不告诉我为什么这么判"。原因是结构性的：解释必须由生成 token 产生，而 RLCD 优化的是概率校准而非理由质量。**本文认为**，即便在 schema 里加一个"理由"字段，那个字段也只能是 Choice/Score/Noul 三者之一的又一种被分类输出——官方 primitives 只允许这三种答案形态（[Primitives 总览](https://docs.typesafe.ai/primitives)）——因此它不具备因果解释力。可解释性在这里必须来自外部结构：**把大判断拆成原子问题（暴露判断）、读概率与 confidence（暴露不确定）、把阈值与组合写在代码里（暴露规则）**——这正是官方推荐的工作流（[How to build with System One](https://docs.typesafe.ai/concepts/how-to-build-with-system-one)）。需要"理由"的场景，本质上是需要 LLM 的场景，应交给第 6 章讨论的编排层。

## 3. 边界一：与传统专训分类器——不是替代，是补位

Cloudflare 发布 Clef 时给的对照表常被误读：CLINC150+OOS 上 macro-F1，Clef 97.43、**Jev 89.27**、小模型 **Laya 仅 3.19**（[Cloudflare 博客](https://blog.cloudflare.com/clef-decision-models/)）。

**3.19 不是"模型差"，而是"它在没训过的标签集上必然崩"。** 表里的 Laya 就是 Convai 开源的那份权重（列标题直接指向其 HuggingFace 仓库），而它在同一张表上 10 项指标**全线处于随机水平或更低**（BFCL 38.13、API-Bank 11.41、家电类目 0.00）（[Cloudflare 博客](https://blog.cloudflare.com/clef-decision-models/)）。这不是孤例，Laya 自己的模型卡就承认：基座检查点在 typed-decisions 基准上零样本仅 **0.362**，低于多数类基线 **0.461**、仅略高于随机 **0.318**，并直陈"Laya 是一个便于专门化的快速基座，**不是零样本决策引擎**"（[Laya 模型卡](https://huggingface.co/convaiinnovations/laya)）。厂商自己都把这条线划得很清楚：**专训分类器的能力来自微调，不来自零样本**。

机制上也有确切解释，而且它比"标签空间不匹配"更具体：其 option-marker 打分器让所有选项**共享一个固定 token 预算**（英文 192、多语 256），于是 77 个选项每个只剩 3–4 个 token，"文本变得不可区分"——Banking77 上准确率仅 0.425。也就是说**选项越多、每个选项能分到的表征越少**，这是专训分类器的结构性弱点（以上数字见 [Laya 模型卡](https://huggingface.co/convaiinnovations/laya)）。

这一条要划清边界：它是 Laya 打分器的特定预算限制，**不是"选项多就不可解"**——同一张表上 Jev 的 89.27 也是在同样 151 个候选上拿到的。但也不能反过来当作 Jev 的能力证明：255 是 Choice 的**契约上限**，不是质量承诺。官方说明"对更高基数的选项，我们采用两阶段系统——先独立打分，再做显式选择，因此偶有变慢"（[发布博客](https://typesafe.ai/blog/introducing-system-one-models-and-jev)）；**本文认为，这意味着连厂商自己都把 255 当作需要变通的上限，而不是可直接依赖的能力，也意味着高基数在这个品类里不是免费的**：选项数要么换成延迟，要么换成准确率，要么换成拆题工作量——Jev 用两阶段打分，Laya 用调大 option 预算或拆两级层次化 Choice，各家其实是同一个思路。公开可核的 Jev 高基数实测只有 CLINC150+OOS 这**一个点**（150 个域内意图加 1 个域外类，共 **151 个候选**；89.27 是单点汇总，没有随选项数变化的劣化曲线），**151 到 255 之间没有任何公开数据**，托管 Jev 在高基数选项上的真实阈值未公开。

延迟那一列要打折读，但原因不是“同一厂商给了两套设置”，而是**同一个模型被两个独立测量方各测了一次**。5.8ms 是 Cloudflare 在 Clef 对照表里测得的 Laya 中位延迟；39.5ms 是 Convai 自己在 Tesla T4 上测的单问题延迟（多语版 32.8ms）。Cloudflare 未披露该第三方模型的硬件、量化与 batch——**本文不替它归因**：批处理摊薄、更快的硬件都只是可能，既无法证实也无法否证，因此不写成结论。可以确定的只有一点：**这两个数不同源，不能相除**。

唯一可作量级参考的是 Laya 模型卡给出的 **6–8 倍**（Jev p50 236–276ms），但它的基准是 **T4 单问题**，且区间两端各对了一个检查点：236÷39.5≈6.0 取英文数，276÷32.8≈8.4 取多语数，取整规则未说明；对照表另给 7.8×，是 32.8ms 除 Jev 中值 256ms 所得。**因此这个倍数不可反算 Jev 延迟**——若硬乘，6×5.8≈35ms 与 8×39.5≈316ms 相差近 9 倍，两个估计都站不住。它取代了 90 倍这个不成立的算法，但它出自 Laya 一方、方向对其有利，模型卡亦自陈那两个 Jev 数“第三方已发布、**从未在此测量**（无 TypeSafe API 访问），样本量与提示词亦不同”（[Laya 模型卡](https://huggingface.co/convaiinnovations/laya)），所以本身也不是严格同环境对比。

结论只取方向：**专训小模型有数倍级延迟优势，代价是只能判自己训过的标签**——一个用专用化换速度，一个用通用性换零样本。

分界线由此清晰：

- **该训分类器**：标注数据充足、标签集稳定、延迟极敏感、单一租户单一领域。Cloudflare 的说法是，自建分类器要划算是需要长期积累的标注数据的，换来的是更准更快；而微调本身是"牺牲通用性能换取领域精度"的交易（[Cloudflare 博客](https://blog.cloudflare.com/clef-decision-models/)）。
- **该用 decision model**：标签会变、冷启动无标注、长尾类别、多租户各自一套标签体系——即"需要换标签而不重训"的那一维。

## 4. 边界二：与 LLM + structured output——差在延迟、成本与类型安全

精度不是本章的举证点：Jev 与 LLM 的准确率差异**按任务族分化**（有的族持平，有的族仍落后），完整的任务族拆解与结论统一放第 2 章。本章只保留原语定义与工程账，不引用任何准确率数字，以免把"原语定义"与"实测表现"混在一处。真正的分野在工程账上，而这笔账**最容易被算错**。

Vals AI 的实测是本章最值得记住的一个数：**要求 LLM 输出概率而非裸标签，会让成本上升 29%（GPT-6 Luna）到 101%（GPT-5.6 Sol）**，12 个系统里 11 个涨价，唯一例外是 Gemini 4 Argon 的 −3%；Jev 的输出本身就是分布，零额外成本（[Vals AI 评测](https://vals.ai/blogs/independent-evaluation-of-jev)）。只比 "$/Mtok 单价"的选型表会系统性低估 LLM 一侧的成本，还会漏掉两笔：LLM 输出 token 单价通常是输入的 5 倍（[发布博客](https://typesafe.ai/blog/introducing-system-one-models-and-jev)），以及 schema 校验失败后的重试。

延迟结构同样不同构：Vals 实测同一长文档上问 1 到 64 个判断，Jev 从 0.10s 到 0.12s 几乎不动，而 GPT-6 Astra 到 38s、Gemini 4 Argon 到 65s；32 个判断时 Jev 中位延迟比 Astra 低 194 倍（[Vals AI 评测](https://vals.ai/blogs/independent-evaluation-of-jev)）。类型安全上，Jev 的 schema 匹配是结构保证——官方原话是"这用一个反例就能推翻，但它在数学上不可能"（[发布博客](https://typesafe.ai/blog/introducing-system-one-models-and-jev)），而 LLM 一侧在评测中出现了缺答案的情况，Jev 零格式错误（[Vals AI 评测](https://vals.ai/blogs/independent-evaluation-of-jev)）。

## 5. 边界三：与规则引擎——它是规则引擎的输入层，不是替代品

官方在发布博客的用例表里给自己的定位就是 **"AI-Powered Workflows / smart if-statements"**：把结构化输出当作模糊决策规则插进普通软件，"在**手写逻辑太脆**的地方做分类、路由、打分、抽取或分支"（[发布博客](https://typesafe.ai/blog/introducing-system-one-models-and-jev)）。

什么算"太脆"？给三条可操作的判据：**规则条目随表述变体爆炸**（同一意思十种说法就要写十条）、**输入本身是自然语言而非结构化字段**、**判断依赖常识而非可枚举条件**。反过来，三类东西**绝不该交给它**：金额计算、权限/授权判定、合规硬门槛。Vercel 的工程指南把这条写成一句口号："把分类与授权分开"——Jev 能判断"客户是否要求退款"，但**是否批准退款取决于它看不到的账户状态、政策与权限**，必须在代码里做第二道检查；它记录的是意图，不是批准（[Vercel 指南](https://vercel.com/kb/guide/typesafe-jev-and-ai-sdk)）。官方文档的措辞是同一件事：控制流、确定性规则、副作用留在代码里（[How to build with System One](https://docs.typesafe.ai/concepts/how-to-build-with-system-one)）。

所以正确的理解是：**它把自然语言压成布尔/枚举/档位，再交给规则引擎**。概率是路由信号，不是判决。

## 6. 不可协商的硬约束（已核对官方 models 页，Jev 1.14）

| 约束 | 具体内容 |
|---|---|
| 无定制权重 | 不用客户数据微调、不做 LoRA，"同一份权重服务每一个账户"，只能靠 `state`/`instructions`/`criteria` 塑形 |
| 仅文本 | 只接受字符串、JSON 对象、文本数组；音频与视频不支持 |
| 语言 | 英语为主要训练语言、准确率最高；CJK 等"能处理但不等同"，官方要求自行测试 |
| 上下文 | 64k/请求、32k/问题；加 `TypeSafe-Danger-Zone-Long-Context: true` 头后两者**均升至 262k**（[models 页 · Long context](https://docs.typesafe.ai/models#long-context)）；**同价**（超出 64k 的部分仍按 $0.042/Mtok 计），但**更慢更不准** |
| 计价 | $0.042/Mtok 输入（$42/Btok），**输出免费**；长上下文同价 |
| 版本 | Jev 1.14（`jev-1.14.0`，2026-10-14 起），`jev-latest` 与 `jev-preview` 当前都指向它 |

（以上均见 [官方 models 页](https://docs.typesafe.ai/models)。三处需要以官方为准的细节：其一，Vercel 指南把 32k 说成"`state` 占 32k"，官方定义是 per-question context，即 `state` + 任一问题合计 32k——写 schema 时按后者算；其二，长上下文的口径官方原文是 "With the header, the per-request context and the per-question context are both 262k tokens"，并明确 "Long context costs the same per token as any other request. It is slower and less accurate than staying within the default limits"；其三，**两档相等时，per-request 一项自动成为唯一有效约束，per-question 不再起约束作用**——这解释了为什么 64k/32k 这种 2 倍关系会在加头后并到同一个数。）

## 7. 硬约束的排除效应（本章最重要的输出）

硬约束的价值不在于"知道它有限制"，而在于**据此判定出局**。先划清适用对象：**以下"出局"针对的是"选用托管的 Jev"这一决策，不是针对 decision model 这个品类**——托管版闭源、共享权重、仅接受文本；品类里存在开源自托管实现（Laya / Clef），权重可微调、模态可扩展，本节结论对它们不适用。如果你要的是可定制权重，那条路存在，但它在选型之前就要走完，且不再享有本文讨论的任何托管形态优势。在此前提下，三类需求应当直接判定为**出局，而非"调优后可用"**：

1. **需要领域定制权重的场景。** 官方明确不微调、不做 LoRA、全账户共享同一份权重。如果你的准确率瓶颈在于领域词汇或领域边界**无法用文字在 `state`/`criteria` 里描述清楚**，那它不是"再调调 prompt"能解决的，而是权重层面的缺口。
2. **需要图像/音视频输入的场景。** 官方明确"不支持（yet）"（[System One 概念页](https://docs.typesafe.ai/concepts/system-one)）。品类内已有带视觉编码器的实现，替代路径与选型对比见第 3 章。
3. **需要 CJK 母语级语义判断的场景。** 官方只承诺"能处理但不等同"，并要求自测；**本章未找到任何公开的第三方 CJK 基准或评测**，因此这一维度**公开信息不足**——缺的是非英语语种上的独立准确率/校准数据。在没有自测数据前，不应把它放进中文为主的生产判断链路。

还有一条隐含代价必须写出来：**共享权重意味着全行业共用一套失败模式，你的 badcase 不会因为你反馈而改善。** 这不是推测，第 2 章会给出第三方独立评测在 LegalBench 切片上的实测（本章不重复数字）：那类失败模式属于所有账户共有，你既不能靠反馈修掉它，也不能靠微调绕开它。顺带澄清一个容易混淆的点：这**与 Score 原语"返回概率加权均值"的语义无关**——加权均值是 Score 的定义（§1），LegalBench 垫底是推理链能力的缺口，两者没有因果关系。你能做的只有两件事：在代码里检测它（低 confidence 路由人工），或用 `state`/问题分解绕开它。**可调的是输入与阈值，不可调的是权重与模态**——这是**托管 Jev** 的边界，不是品类的边界；这就是"调优"与"出局"的分界线。

## 8. 成本与延迟的真实结构

输出免费 + 输入计费，构成一个很硬的不对称：**多问几个问题几乎不涨价，`state` 越长越贵。** 官方也承认长上下文"同价但更慢更不准"，且不同 state 长度下准确率会抖动（[models 页](https://docs.typesafe.ai/models)）。Vercel 据此给出的建议是"只传决策依赖的字段"（[Vercel 指南](https://vercel.com/kb/guide/typesafe-jev-and-ai-sdk)）。

结构性含义有三条（具体 schema 规则留给第 6 章）：

- **决策密度应当最大化**：一个 `state` 上问满所有需要的问题，因为拆请求等于重复支付同一份 `state` 的钱。
- **`state` 是唯一成本项，也是准确率的敌人**：省钱与降噪在这里同向，都指向剪裁。
- **成本优势随"每 state 问题数"放大**：单文档单问题的场景，Jev 的价格优势远不如"高频、短 state、多问题"的形态显著。

## 小结与判据

decision model 的适用区间由四个条件共同定义：**判断能写成一道"知识渊博的人几秒内答完"的单选题**（可原子化，[Vercel 指南](https://vercel.com/kb/guide/typesafe-jev-and-ai-sdk)）、**标签会变或尚无标注数据**（否则专训分类器更快更准）、**输入是文本且语言以英文为主**（否则触达模态与语种硬约束）、**判决之后的动作能用代码兜住**（金额、权限、合规不得下放）。四者缺一，即出局或换工具。

> **一句话判据**：如果这道判断"标签会变、只有文本、答案能写成单选或档位、且错了也只是走人工复核而不是直接放款/放权"，它在适用区间内；如果它需要"领域定制权重、看图听音、或中文母语级语义"，请直接判出局，不要进入调优流程。（本条针对托管 Jev；品类内可自托管、可微调的实现见第 3 章，边界不同。）
