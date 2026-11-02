# 第 5 章 探索与缺口：社区实验、学术推演与尚未长出的工具链

## 5.1 论点：Jev 生态的真实形状是「高密度试错、低密度验证」

本章的收录判据只有一条：**有信号（代码 / 论文 / 热度），但没有规模证据**。这条判据把本章与第 4 章分开——第 4 章收有第三方可核验规模证据或付费主体的用法，本章收「有人在试、有人写了论文、但没人证明它扛得住规模」的部分。

截至 2026-10-31 的观测给出一个反直觉的组合：代码密度极高、学术跟进极快、声量极大，但三者都还没转化为可核验的规模证据。规模最大的量化研究本身就说明了这一点——[Jev in the Wild](https://arxiv.org/abs/2609.30216) 统计 **2,170 个公开 GitHub 项目（截至 2026-09-22）**，其中 **1,865 个为发布后一周内新建、305 个为存量仓库接入**（出处：论文 **§2.2 Growth Trends 正文**，配 Figure 1；该拆分仅见于正文叙述，论文未以表格列出）。这是对「扩散速度」的测量，不是对「生产可靠性」的测量。

## 5.2 B 层：有代码、有细节、但无人证明能扛规模的试点

GitHub 仓库均已核实存在性与维护状态（GitHub API，**截至 2026-10-31**）；非仓库条目以「—」表示。

| 仓库 / 项目 | 来源类型 | 用途 | Stars | 最后推送 | 状态判断 |
|---|---|---|---|---|---|
| [OpenByteInc/QuantDinger](https://github.com/OpenByteInc/QuantDinger) | 一手·仓库代码 | AI 交易系统，Jev 作**交易前决策门控** | 13,348 | 2026-10-31 | 活跃；但仓库建于 2025-12-28，**早于 Jev**，Jev 仅为其多个集成之一 |
| [yibie/awesome-jev](https://github.com/yibie/awesome-jev) | 一手·仓库代码 | 主索引（日更 evidence sweep） | 2,516 | 2026-10-31 | 活跃；374 forks / 917 commits / **679 条条目**（571 项目 + 108 讨论） |
| [hardness1020/learn-agent-architecture](https://github.com/hardness1020/learn-agent-architecture) | 一手·仓库代码 | 中文教程，第 22 章把 Jev 接成「图工程的决策边」 | 1,188 | 2026-10-21 | 活跃；仓库建于 2026-06-23，Jev 为后续增补章节 |
| [dabit3/jev-experiments](https://github.com/dabit3/jev-experiments) | 一手·仓库代码 | Nader Dabit 的延迟导向 demo 集 | 412 | 2026-09-21 | **已停更**（发布后 4 天） |
| [coderexpert123/jev-browser-wingman](https://github.com/coderexpert123/jev-browser-wingman) | 一手·仓库代码 | MCP 代理，把浏览器点击交给 Jev | 7 | 2026-10-31 | 活跃但极小 |
| [maayanlevy/mysql-ailike](https://github.com/maayanlevy/mysql-ailike) | 一手·仓库代码 | MySQL 插件，按语义过滤行 | 4 | 2026-09-20 | 已停更（1 天） |
| [Selmar/typesafe-jev-calibrate-for-code-review](https://github.com/Selmar/typesafe-jev-calibrate-for-code-review) | 一手·仓库代码 | 把 Jev 校准成代码审查员 | 3 | 2026-09-23 | 已停更（2 天） |
| [agodoy21/enigma-jev](https://github.com/agodoy21/enigma-jev) | 一手·仓库代码 | Jev 当 Bletchley Park 分析员破 Enigma | 3 | 2026-09-30 | 已停更 |
| lurk（[社区展示站](https://jevfast.com/lurk/)） | 二手·社区/展示站（未独立核实） | 扫描 Reddit 帖做分类，自称「only possible to give for free bc of Jev」 | — | — | 判断机制未披露，无公开仓库 |
| [DialNexa](https://dialnexa.com/blogs/jev-on-real-calls-can-a-decision-model-run-our-voice-agents-hangup-and-routing-calls) | 一手·客户自有文档 | 语音 agent 挂断 / 路由判断 | — | 2026-10 | **离线回放，非生产**：回放 4,516 条挂断判断 / 1,079 通电话，调阈值后与生产 LLM 一致率 95.0%、中位 462 ms；作者自陈「We didn't route live calls through Jev」，且「One flag needs a safety fix」 |
| [Vapi](https://vapi.ai/blog/early-experiment-with-jev) | 一手·客户自有文档 | guardrails 早期实验 | — | 2026-10 | 实验性；作者自陈「caught at least three out of four」，且「not a 100% compliance guarantee」 |

> **本表 11 条均无第三方可核验的规模或精度证据**：代码可读、可克隆、可运行，不等于效果可验。

另有博客侧单点实验：[r6i.it 的产品分类迁移](https://blog.r6i.it/typesafe-jev-vs-agentic-loop.html)（Sam Reghenzi，2026-09-21）把 agentic 分类循环换成 Jev，同一批 50 个商品上均值延迟 9.62 s → 1.38 s、模型调用数 7.22 → 3.18；作者同时写明「agent 在需要回溯的场景仍然胜出」。

**分析**：八条 GitHub 条目里，Jev 原生项目的 star **中位数约 5.5**，只有一个超过 400；而唯一破万的 QuantDinger 仓库建于 **2025-12-28，早于 Jev 发布（2026-09-15）**，Jev 只是它的多个集成之一——**它的 13,348 stars 不能归因于 Jev**。去掉这条不可归因的头部后，真实分布是**长尾极长、头部缺失**：绝大多数是发布后一到两周内的一次性探索，仓库存活但停更。这一点有论文背书，非本文自测——2609.30216 摘要原话：「public attention is **concentrated in routing and interface agents and does not track project counts**」（声量集中于路由与界面 agent，且不随项目数变化）。三条非仓库条目更进一步——连代码都不公开、只有自述，DialNexa 还明确否认做过生产路由。

## 5.3 C 层：社区活跃度数据（只报数，不做推论）

| 指标 | 数值 | 抓取口径 |
|---|---|---|
| HN 命中 story 总数 | **72 条** | [Algolia API](https://hn.algolia.com/api/v1/search?query=Jev%20TypeSafe&tags=story)，`query="Jev TypeSafe"` |
| 其中落在 2026-09-16 ~ 10-15 | **64 条** | 同上 |
| 该 64 条中 ≤6 分 / 零评论 / 中位数 | **60 条 / 51 条 / 2 分** | 同上 |
| ≥20 分的帖子 | **3 条**：Jev 1.14.0 官方发布帖 335 分 / 122 评论（10-14）、CUA-S1 95 分 / 10 评论（间接相关）、Unsiloed 48 分 / 7 评论 | 同上 |
| 窗口外发布帖 | 1,989 分 / 520 评论（09-15） | 同上 |
| jev.guide 国家分布 | 美 69 / 印 37 / 中 36 / 日 21 / 法 19 / 德 18 / 加 12 / 波 7 | [jev.guide](https://jev.guide/)，按公开 Owner 所在地 |
| npm `jev` 检索命中 | 1,534 个包（含噪声） | registry.npmjs.org |
| Jev 适配器周下载量 | `jev-browser` 989 / `@livx.cc/mcp-jev` 305 / `@marcmeese/n8n-nodes-jev` **25** | api.npmjs.org |

**这些数字的含义见第 7 章，本章不展开。**

## 5.4 C 层：具体用例形态（价值在「形态提示」，不在「效果背书」）

以下四条均来自 [jev.guide](https://jev.guide/) 收录的 X 原帖，**均为单点自述，不构成效果证据**：

- **Lightpanda Agent 用 Jev 识别登录框**（2026-10-29 收录）——把「这是不是登录表单」变成一次 Noul 判断。
- **Browser Use + Jev 做浏览器 agent**（Gregor Zunic）：搜航班 7 秒、成本 $0.0039。
- **Jev 做上下文压缩**：给每次工具调用打分、丢掉无关内容，绕开摘要提示；社区实现为 `fast-jev-compaction`。
- **12.8 秒评完 100 分钟面试、成本 $0.005**：Pass/Hold 分类 + 专业技能与沟通动机打分 + 重大顾虑片段定位。

形态提示一致：Jev 被放在**「原本会调用一次 LLM 做小判断」的位置**，而非替代 LLM 做生成。

## 5.5 D 层：四支后续研究——原文回溯结果

这是本章最重要的核实工作。这四条此前只见于[中国指挥与控制学会专栏](https://www.c2.org.cn/h-nd-3419.html)（2026-10-27）与百家号 AI 生成版，**该专栏通篇未给出任何论文标题或 arXiv 编号**，因此初看无法验证。经检索 arXiv，**四条全部定位到原文**：

| 线索 | 是否定位 | arXiv 编号 | 判定 |
|---|---|---|---|
| JevMem（UT Dallas） | ✅ | [2609.23986](https://arxiv.org/abs/2609.23986) *Jev-Mem: System-One-Controlled Agentic Memory for Efficient AI Agents*，Dongming Jiang / Yi Li / Bingzhe Li，2026-09-21 | arXiv 一手，预印本 |
| JEV-as-a-Judge（CMU） | ✅ | [2609.26550](https://arxiv.org/abs/2609.26550) v6 *JEV-as-a-Judge: Accept When Confident, Escalate When Unsure*，Yubo Li / Yidi Miao / Ramayya Krishnan / Rema Padman，2026-09-22（v6 2026-10-29） | arXiv 一手，预印本 |
| Visual-Jev | ✅ | [2609.25845](https://arxiv.org/abs/2609.25845) *Visual Jev: Accurate and Efficient Decisions from Shared Visual Context*，Guanxu Yu / Yuhang Yao，2026-09-22 | arXiv 一手，预印本 |
| Chinese-Jev（复旦 / 新国立） | ✅ | [2609.36965](https://arxiv.org/abs/2609.36965) *Chinese-Jev: Bringing System One Model to Chinese-Language Tasks*，Zexiao Wang 等（含 Zuxuan Wu、Shuicheng Yan），2026-09-29 | arXiv 一手，预印本 |

> **核验方式说明**：上表四条与本章引用的 2609.30216、2609.28940 均以**直接请求 arXiv abs 页返回 HTTP 200** 为准，标题、作者、日期、摘要与表内容均可读。此处特别说明，是因为检索过程中曾出现「arXiv 站内搜索与 API 因限流返回零结果」的情形——**「我搜不到」与「它不存在」是两件不同的事**，本章的证据判据（见 5.9）正建立在这一区分之上。

**四条的原文数字**：

- **Jev-Mem**：LoCoMo 上 LLM-as-a-Judge 得分 **0.777**（较最强基线 +11.0%），记忆构建时间降至 **158 s**（较最快竞品 **6.6×**），平均查询延迟 **0.93 s**（**−36.7%**）。
- **JEV-as-a-Judge**：对比 **16 种**生成式与奖励模型裁判、带盲法人审。凡「判决可直接从文本读出」的任务，Jev 与 GPT-6 差距 **≤3 个百分点**，费用为其 **0.36%**，中位延迟 **0.15 s**；凡「判决必须推导」的任务（数学、代码、逻辑）明显落后。预先冻结阈值后，在 **1,610 组留出样本**上级联准确率较 GPT-6 高 **0.9 个百分点**、费用为其 **41%**；但作者明确写道：**置信路由在风格对抗样本与无参考散文上会失效**。
- **Visual Jev**：等权宏平均准确率 **70.6% → 76.1%**；**N=32 问/图**时共享批处理比独立串行**快 8.9×**，比已批处理但重算前缀的基线仍**快 3.4×**，代价是更高峰值显存。**关键限定**：它让「共享视觉上下文」这一模态变得可行，**不是给 Jev 加视觉**——Jev 仍是纯文本决策模型，视觉侧是另一组件（第 3 章「模态是 Jev 唯一明确短板」由此不受影响）；该系统从底座 LM head 读候选概率，与 TypeSafe 架构无关，**不可读作「Jev 已支持图像」**。且匹配 typed-head 对照组相对 LM-head 读出**无一致准确率优势**——收益来自共享上下文与批处理，而非「类型化决策头」本身，故本条只宜作**工程效率证据**。这与第 1 章 §4 的边界主张一致：该品类的价值在延迟、成本与类型安全，不在精度；**无一致准确率优势恰是这一判断的第三方旁证**。
- **Chinese-Jev**：编码器-only 轻量底座，先以 **1,000 万条**通用中文决策样本训练、再分医疗/法律/金融微调；一阶段后通用域准确率超闭源 Jev **1.24%**，加速 **20.3×**（**该倍数口径见摘要原文，本文不代为解释**）。

**⚠️ 一处必须纠正的转述（三层）**：专栏称 Chinese-Jev 在 CJ-Bench 上 69.20% vs Jev 68.35%——**68.35 实为 Jev 的法律单项**，非通用域；查论文 Table 2，领域微调后专业域平均仅 **70.82%**（低于 Jev 的 **77.01%**），平均 **ECE 12.08%**（高于 Jev 的 **5.57%**）。摘要所称「+4.0%」仅医疗单项成立（84.29 → 87.65）。**故专栏数字不予采用，本章以 arXiv Table 2 为准。**

值得单独指出的是 **ECE 12.08% vs 5.57%**：领域微调把准确率拉近了，却把校准打坏了。自建模型能追上准确率，但追不上校准——这一条留给第 7 章作反证。

**回溯的连带结论**：既然四条全部命中，该专栏应从「单点不可信转述」**上调为「可靠的二手综述」**——机构归属与结论方向均准确。但仍不能作一手引用：自身不提供可追溯标识，且在 Chinese-Jev 上确有选择性转述。

**另一支前沿**：[arXiv:2609.28940](https://arxiv.org/abs/2609.28940)（Joas Antonio dos Santos Barbosa，2026-09-24）把 Jev 与开源 Laya 作为 System One 决策层嵌入自主渗透测试 harness，定义四个决策点（发现裁决、严重度重校准、agent 剪枝、确认循环）。作者自己写明：NeuroSploit 案例是 **exploratory**，差异「**不构成统计显著性**」。这篇是本章判据的最佳范例——有架构、有案例、明确拒绝效果断言。

## 5.6 生态集成现状（一手核实）

| 渠道 | 证据 | 状态 |
|---|---|---|
| [Vercel AI SDK](https://vercel.com/kb/guide/typesafe-jev-and-ai-sdk) | `experimental_evaluate` + `gateway.evaluationModel('typesafe-ai/jev')`，Vercel KB，2026-09-19 | 官方文档级 |
| [MLflow 3.17.0](https://www.mlflow.org/releases/) | `model="typesafe:/jev-latest"` 作 judge，2026-10-06 | 官方文档级 |
| OpenRouter | `/api/v1/models` 实测存在 `typesafe/jev-router` | 分发渠道 |
| Cloudflare Workers AI | Clef 系列，API 兼容 Jev | 第三方托管 |
| 官方 SDK | Python + JS/TS；[system-one-adapter-python](https://github.com/typesafe-ai/system-one-adapter-python)（406 stars） | 官方 |
| 官方 Agent Skill | [docs.typesafe.ai/agent-skill](https://docs.typesafe.ai/agent-skill)（Claude Code / Codex 直接安装） | 官方 |
| 社区 MCP 代理 | [jev-browser-wingman](https://github.com/coderexpert123/jev-browser-wingman) | 社区 |

## 5.7 生态缺口清单（只列，不给方案）

| 缺口 | 影响面 | 粗估工作量（本文估算） |
|---|---|---|
| n8n **官方**节点缺失，仅有社区 `@marcmeese/n8n-nodes-jev` v0.0.2（2026-10-06 发布，周下载 25，德语文案，挂在个人仓库） | 需自建 | 2–3 人日 |
| Dify / LlamaIndex / Flowise **未见一手集成证据**（已重搜，结论为「未见」，非「不支持」） | 需自建 | 3–5 人日 / 平台 |
| OpenAI 兼容端点不支持评估调用 | 需绕行 | 1–2 人日 |
| 各家 `confidence` 语义与 `Score` 档位实现不一致 | 需绕行 | 0.5–1 人日 / 系统 |
| 除 MLflow 外的评估平台（LangSmith / Weave / Braintrust）未见支持 | 需自建 | 3–5 人日 |
| 官方 MCP 服务缺失，仅社区代理 | 需绕行 | 1–2 人日 |
| 无官方本地 / 离线推理路径 | 需绕行 | 需第三方底座 |

## 5.8 结构性空白场景（**本文推演，无公开实现证据**）

- 多轮对话中的**逐步决策**（每轮做一次结构化判断而非整体重答）——**本文推演，无公开实现证据**
- **长文档流式过滤**（边读边丢，而非读完再摘要）——**本文推演，无公开实现证据**
- agent loop 内的**廉价 critic**（每步都质疑而不只终局裁判）——**本文推演，无公开实现证据**
- **会话级意图漂移检测**——**本文推演，无公开实现证据**

**需与第 4 章区分**：第 4 章的 Unsiloed 双模型互查案例（**一手·客户自有文档**；咖啡渍遮住剂量，Unsiloed 读作「1 tablet」、`extraction_score` 0.74 / `grounding_score` 0.76 被标记，Jev 对同一行合理性判 `noul` = 0.94——它看不到污渍；反向的布洛芬行双分 0.99 而 Jev 给 0.04，原文判词「Each check flags a review need the other misses.」）是**单点已实现**，证明机制存在；本节四条推演讨论的是该机制能否被**工程化复现与规模化**。两者证据等级不同，不可互相替代。**凡两者冲突，以第 4 章为准——已实现的单点优先于未实现的推演。**

## 5.9 小结：如何区分「有人在试」「有人在写论文」「工具链还不存在」

1. **有人在试** = 仓库可访问，但看三个数：star、最后推送时间、是否早于 2026-09-15。Jev 原生项目 star 中位数在个位数、多在两周内停更，属「试过」而非「在用」。
2. **有人在写论文** = 能定位到 arXiv 编号或 OpenReview，且论文**自己**声明了局限。本章四篇全为预印本、无同行评议。
3. **工具链还不存在** = 官方文档搜不到、npm / PyPI 上只有个人 scope 的 0.0.x 包、周下载两位数。缺口表中 n8n、Dify、LlamaIndex、Flowise 均在这一档。

**本章不给补法。所有绕行方案、自建路径与优先级排序留给第 6 章。**
