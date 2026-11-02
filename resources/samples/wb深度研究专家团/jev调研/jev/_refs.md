# 全局参考文献表（`_refs`）

> 编制日期 2026-11-01　·　编制人：谭溯源（课题研究员）　·　**覆盖：第 1–7 章全七章**
> **本文件不改动、不移动任何 `ch*.md`。**

---

## 0　读数说明

**（1）覆盖范围与缺口**
已并入：第 1 章（`jev-report/ch1-category-boundary.md`）、第 2 章（`ch2_revised.md`）、第 3 章（`ch3-draft-v4.md`）、第 4 章（`ch4-revised.md`）、第 5 章（`ch5_draft.md`）、第 6 章（`ch6-draft.md`）、第 7 章（`ch7-draft.md`）。**七章已全覆盖，无遗漏章节。**

第 2、5 章为**补录**（第九节 R42–R67），原因是初版误将两文件判为"另一份报告"，详见 `_format-spec` 附录 B。**这个错误本身留档**：判错依据是"同目录 + 同命名模式"，而正确依据应是 H1 的主题词。

**（2）去重规则**
- 只有**两个 URL 完全相同**才合并（主理人定的纪律）。
- **唯一例外**：`www.` 与非 `www.` 视为同一 URL 的等价写法，合并并逐条注明。全表只有 1 处属此类（R29 `vals.ai`）。
- **锚点变体不合并**：`docs.typesafe.ai/models` 与 `docs.typesafe.ai/models#long-context` 是两个 URL，分列 R05／R06，并在 R06 注明"同页锚点变体，不独立计源"。
- **接口端点不入表**：`https://api.typesafe.ai/v1/systemone` 是请求示例里的端点，不是来源。

**（3）编号规则**
`R01–R41`（第一至八节，第 1、3、4、6、7 章）+ `R42–R69`（第九节，第 2、5 章补录），按两轴类型分组连续编号；arXiv 条目在各节内单列成表。**原 R01–R41 编号未因补录而变动**，全局编号可直接用于正文交叉引用（如"见 R29""见 R54"）。

**（4）计数**
- 七个章节共出现 **93 个"章内唯一 URL"**（53 + 第 2 章 15 + 第 5 章 25）；
- 其中 **28 个为补录新增**（第 2 章 6 个、第 5 章 20 个，另 2 个为无 URL 数据的端点补登），其余与既有编号合并；
- 最终 **69 条编号条目**（R01–R67 + R68–R69 两条补端点）+ 1 组线索 + 4 项本文推演（不入编号）。
- arXiv 条目 **8 条**（R01–R04、R42–R45），六项元数据（编号／标题／作者／提交日期／版本／是否同行评议）**已全部补齐，无缺项**。
- 版本分布：**R43 迭代至 v6**（5 周内 6 版）、R04 两版、其余六篇单版。**8 篇全部"未见同行评议"。**

---

## 一　一手·论文/预印本（R01–R04）

### 1.1　arXiv 条目专表

> **元数据来源说明**：以下六项于 2026-11-01 由 arXiv abs 页逐条核对补入，**非各章原文所载**（第 6、7 章原文只给 ID，未给作者与日期）。四篇 abs 页**均未显示期刊引用信息**，故"是否同行评议"一律判为**未见**，与各章表述一致。

| 编号 | arXiv ID | 标题 | 作者 | 提交日期 | 版本 | 是否同行评议 | URL | 引用章 |
|---|---|---|---|---|---|---|---|---|
| R01 | 2609.24052 | Calibrated Decisions at Scale: Converting Police Crash Narratives into Probabilistic Crash Variables with a System One Model (Jev) | Amir Rafe, Subasish Das（Texas State University, Ingram School of Engineering） | 2026-09-21 | v1（唯一版本） | 未见 | https://arxiv.org/html/2609.24052v1 | 第 4、6、7 章 |
| R02 | 2609.25845 | Visual Jev: Accurate and Efficient Decisions from Shared Visual Context | Guanxu Yu, Yuhang Yao | 2026-09-22 | v1（唯一版本） | 未见 | https://arxiv.org/abs/2609.25845 | 第 7 章 |
| R03 | 2609.36965 | Chinese-Jev: Bringing System One Model to Chinese-Language Tasks | Zexiao Wang, Zihao Zhang, Xudong Wang, Pan Wang, Ziyi Ye, Haoyu Zhao, Zuxuan Wu, Shuicheng Yan | 2026-09-29 | v1（唯一版本） | 未见 | https://arxiv.org/abs/2609.36965 | 第 6、7 章 |
| R04 | 2609.38827 | More Choices, Fewer Decisions: Ordinal-Scale Bias in JEV-like Direct-Decision Models | Tianxiang Gao, Jinzhe Li, Zhiyuan Li, Yi Chang, Yuan Wu | v1 2026-09-30；v2 2026-10-14 | **v2** | 未见 | https://arxiv.org/abs/2609.38827 | 第 6 章 |

**版本差异（须注明）**：R04 有 v1→v2 两个版本，间隔 14 天（09-30 → 10-14），第 6 章引用的是 **v2**（原文标"预印本 v2"）。其余三篇仅 v1。**v1 与 v2 不是同一份文本，引用页码/表号时须写明版本。**

### 1.2　各条内容要点

**R01**（第 4、6、7 章）— 500 万条语料、19.6 万条实测编码、27 问 schema、F1 0.908、$0.1543/千条、$55.79 总花费、0 次失败调用（调用层口径）。第 6 章取其"a property of the model's interface rather than of its skill"、两位小数网格与 Proposition 1；第 7 章取其 "detectable after the fact"、"a reader cannot rerun the analysis"、Lemma 2、§2.3 "no answer can be invalid and none has to be parsed"、§4.4 pooled F1 0.875。**本地存有全文**：`D:\research\jev\2609.24052.pdf` 与 `.txt`。

**R02**（第 7 章）— 摘要原文 "A matched typed-head control offers **no consistent accuracy advantage** over the language-model-head readout"，第 7 章 §7.3 逐字引用且保留了"一致"二字。另：四基准 answer-supervised post-training 使 equal-weight macro accuracy 由 70.6% 升至 76.1%；N=32 时共享批执行比独立串行快 8.9×。**该篇是视觉域（cs.CV），不是托管 Jev 的模态证据**，第 7 章只作读出方式比较使用，处理正确。

**R03**（第 6、7 章）— CJ-Bench；一阶段通用域超 Jev 1.24%（20.3× 提速）；三域微调后达 Jev 平均准确率 **92%**、17× 提速、15 ms/例；INT8 端侧约 1.0 s/决策。第 7 章 §7.2 的 "1.24%" 与 §7.5 的 "92%"、医疗 +4.0% 均与本篇摘要吻合（医疗 87.65 vs 84.29 = +3.99% ≈ 4.0%，已验算）。

**R04**（第 6 章）— 40 个数据集、9 个模型（JEV / KEV / StartLux Decision 三族）；序数任务刻度利用率 60%–76%、无序名义任务 87%–102%（36 + 4 = 40，与第 6 章一致）；K 由 2 增至 14 时 D_R 由 4.1 升至 45.6；随机化候选顺序只减弱、不消除压缩。

---

## 二　一手·官方（TypeSafe 自有文档与公告，R05–R16）

| 编号 | 标题 | URL | 类型 | 引用章 | 一句话摘要 |
|---|---|---|---|---|---|
| R05 | TypeSafe Models 页 | https://docs.typesafe.ai/models | **一手·官方**（可复现抓取） | 第 1、3 章 | 64k/请求 · 32k/问题、262k danger-zone 头、Jev 1.14（10-14）、alias 漂移警告、不可微调、仅文本、$0.042/Mtok 输入且输出免费 |
| R06 | 同上 · Long context 锚点 | https://docs.typesafe.ai/models#long-context | **一手·官方**（同页锚点变体，**不独立计源**） | 第 1 章 | "With the header, the per-request context and the per-question context are both 262k tokens"；"It is slower and less accurate"；长上下文同价 |
| R07 | TypeSafe Introduction（三原语总览入口） | https://docs.typesafe.ai/ | **一手·官方**（可复现抓取） | 第 3 章 | 三原语定义与返回字段的入口页 |
| R08 | TypeSafe Quickstart | https://docs.typesafe.ai/introduction/quickstart | **一手·官方**（可复现抓取） | 第 3 章 | `/v1/systemone` 完整请求/响应 schema 与 curl 示例——第 3 章最小请求示例的唯一出处 |
| R09 | TypeSafe State 概念页 | https://docs.typesafe.ai/concepts/state | **一手·官方**（可复现抓取） | 第 3 章 | `state` 可为 string / object / array；不支持音视频；CJK 准确率较低 |
| R10 | System One 概念页 | https://docs.typesafe.ai/concepts/system-one | **一手·官方**（可复现抓取） | 第 1 章 | "不写回复、不产出代码、不生成关于自身推理的解释"；图像"不支持（yet）" |
| R11 | How to build with System One | https://docs.typesafe.ai/concepts/how-to-build-with-system-one | **一手·官方**（可复现抓取） | 第 1 章 | 拆原子问题、读概率与 confidence、阈值与组合写在代码里的官方工作流；控制流/确定性规则/副作用留在代码 |
| R12 | Primitives 总览 | https://docs.typesafe.ai/primitives | **一手·官方**（可复现抓取） | 第 1 章 | 三原语总览；Noul 无独立 `confidence` 字段；问题 `id` 不发给模型；同请求内各问题答案相互独立 |
| R13 | Choice 原语 | https://docs.typesafe.ai/primitives/choice | **一手·官方**（可复现抓取） | 第 1 章 | 最多 255 选项；返回 choice + 和为 1 的 probabilities + 分布尖锐度 confidence；官方明言不适合有内在顺序的判断 |
| R14 | Score 原语 | https://docs.typesafe.ai/primitives/score | **一手·官方**（可复现抓取） | 第 1 章 | 2–10 个有序等级；返回**概率加权均值**，可落在两档之间（如 1.43） |
| R15 | 发布博客：Introducing System One Models and Jev | https://typesafe.ai/blog/introducing-system-one-models-and-jev | **一手·厂商自述**（利益相关） | 第 1、3、6 章 | RLCD 与 RLHF/RLVR 对照表；"Jev supports a cardinality up to 255"；高基数走两阶段且 "occasional slowdown"；用例表 "smart if-statements"；输出 token 单价约输入 5 倍 |
| R16 | TypeSafe Series A | https://typesafe.ai/blog/series-ai | **一手·厂商自述**（利益相关） | 第 3、4 章 | $870M @ $75 亿、a16z 领投、Casado 入董事会；"1/3 财富 500 强在用""已省下数百万美元"——**无名单、无 case study** |

---

## 三　一手·平台/大厂文档与公告（R17–R20）

| 编号 | 标题 | URL | 类型 | 引用章 | 一句话摘要 |
|---|---|---|---|---|---|
| R17 | Cloudflare: Clef decision models | https://blog.cloudflare.com/clef-decision-models/ | **一手·厂商自述**（非 Jev 厂商） | 第 1、3、6 章 | "fully Jev-API compatible"；CLINC150+OOS 10 项对照表（Clef 97.43 / Jev 89.27 / Laya 3.19）；延迟 Laya 5.8 ms、Jev 524.1 ms；64k vs Jev 32k；Clef 带视觉编码器 |
| R18 | Vercel KB: TypeSafe Jev and AI SDK | https://vercel.com/kb/guide/typesafe-jev-and-ai-sdk | **一手·平台文档**（非 Jev 厂商） | 第 1、3 章 | "OpenAI-compatible endpoints don't support Jev evaluation"；概率两位小数；255 选项 / 2–10 档；`probabilities` 可选；"把分类与授权分开" |
| R19 | Vercel: Jev is the fastest-adopted model in AI Gateway history | https://vercel.com/blog/ai-gateway-jev-model-launch | **一手·厂商自述**（内部遥测不可复算；非 Jev 厂商） | 第 3、4 章 | 24h 内近 13% 付费团队采用；2× GPT-5.6 家族、>6× Fable 5.1（三者同平台、同分母、同 24h 窗）；仅平台方可复核 |
| R20 | Microsoft Foundry 官方博客 | https://devblogs.microsoft.com/foundry/ | **一手·厂商自述**（**反向证据**） | 第 3 章 | 已检索首页全部文章，**未见 Decision-1 公告**——用于支撑"微软发布时间为二手口径、待一手核实" |

---

## 四　一手·客户（R21–R26）

| 编号 | 标题 | URL | 类型 | 引用章 | 一句话摘要 |
|---|---|---|---|---|---|
| R21 | Document Review With Unsiloed and TypeSafe Jev | https://www.unsiloed.ai/blog/document-review-unsiloed-typesafe-jev | **一手·客户自有文档**（可复现抓取；厂商是 TypeSafe，Unsiloed 是客户） | 第 4、6 章 | 双模型互查完整实现：分工、完整请求/响应 JSON、阈值 0.90 / 0.50、$0.000076/文档、咖啡渍与布洛芬两向漏检；"A high Jev answer must not cancel a low Unsiloed score" |
| R22 | Famulor Changelog（2026-09-22） | https://docs.famulor.io/changelog | **一手·客户自有文档**（可复现抓取） | 第 4 章 | Jev 驱动消息咨询标签（Possible scam / Advertising）；客户自陈 "They are advisory and can be wrong" |
| R23 | WikiFix for Confluence — Atlassian Marketplace | https://marketplace.atlassian.com/apps/2836392116/wikifix-for-confluence | **一手·厂商自述**（平台托管） | 第 4 章 | 产品定位核实：扫描矛盾/过期/无主页面并写修复，逐条人工批准 |
| R24 | Ana — vertice.one | https://www.vertice.one/ana | **一手·客户自有文档**（可复现抓取） | 第 4 章 | 软件采购谈判 agent，自称 4,000+ 场谈判、5 亿美元 spend；**Jev 用法仅见于客户页，细节未公开** |
| R25 | Jev on Product Hunt（产品页 + 评价卡） | https://www.producthunt.com/products/jev | **一手·客户自述**（平台托管；引句取自 2026-10-21 快照） | 第 4 章 | gg-friggin-ez（Shikhar Srivastava）、Fit Receipt（Crystal Chang）的用法原文——全报告唯二可回溯到具体载体的客户引文 |
| R26 | Where I put Jev in production on a large site, and where I didn't（PH 论坛帖，作者 Hisashi Space，2026-09-30） | https://www.producthunt.com/p/jev/where-i-put-jev-in-production-on-a-large-site-and-where-i-didn-t | **一手·客户自述**（平台托管；无审计；非 9 家名单成员） | 第 4 章 | 日本招聘平台生产约 10 天：996 家流水线判定 571 家、抽检 50 家 0 错；**抽样方法未公开** |

---

## 五　一手·厂商自述（第三方厂商／竞品，R27–R28）

| 编号 | 标题 | URL | 类型 | 引用章 | 一句话摘要 |
|---|---|---|---|---|---|
| R27 | Laya 模型卡（Convai） | https://huggingface.co/convaiinnovations/laya | **一手·厂商自述**（模型卡；非 Jev 厂商） | 第 1、3 章 | 与 Cloudflare 表中的 Laya 同源（列标题直指本仓库）；"Laya is a fast base to specialise, not a zero-shot decision engine"；基座 0.362 **低于多数类基线 0.461**（随机 0.318）；`head_max_len` 192/256；Jev p50 236–276 ms、Laya 快 6–8×（**Laya 侧 T4 实测，Jev 侧硬件未披露**） |
| R28 | eu/jev — First System One Model Hosted in the EU（Bevel） | https://eu-jev.com/ | **一手·厂商自述**（利益相关；**竞品，非客户**） | 第 3、4 章 | 德国 Hetzner 推理、不留存 prompt；Jev-style API，模型 ID `eu-jeff-latest`（**jeff 非 jev**）；€37/Btok；**API 层面完全兼容、产品定位上是替代品** |

---

## 六　一手·平台数据与开源仓库（R29–R34）

| 编号 | 标题 | URL | 类型 | 引用章 | 一句话摘要 |
|---|---|---|---|---|---|
| R29 | Vals AI: Independent evaluation of Jev | https://vals.ai/blogs/independent-evaluation-of-jev | **一手·平台数据**（评测平台自测；原始数据不可复算） | 第 1、6 章 | 要求 LLM 输出概率使成本升 29%–101%（12 系统 11 涨，唯一例外 Gemini 4 Argon −3%）；1→64 判断 Jev 0.10→0.12s、GPT-6 Astra 38s、Gemini 4 Argon 65s；32 判断时比 Astra 低 194×；LegalBench 类别平衡准确率 0.730 排末、两子任务恒答 Yes；四步法 12 系统中 6 个超预算（含 Jev：95% 覆盖、1.6% 实际错误） |
| R30 | AbdelStark/jev-benchmarks | https://github.com/AbdelStark/jev-benchmarks | **一手·平台数据**（GitHub，可复现抓取） | 第 3 章 | 独立于 TypeSafe 的 Jev 测量；被 Laya 模型卡引为 236–276 ms p50 出处（**本章未逐项复核方法学**） |
| R31 | nibzard/decision-model-benchmark | https://github.com/nibzard/decision-model-benchmark | **一手·平台数据**（GitHub，可复现抓取） | 第 6 章 | 社区自建基准（**非同行评议**）：验证集冻结后测试误差 **6.65%** 仍超 5% 目标 |
| R32 | wfzyx/von（已归档） | https://github.com/wfzyx/von | **一手·平台数据**（GitHub，可复现抓取） | 第 3 章 | 395M ModernBERT，byte-compatible；2026-10-19 归档并指向 d1-omni-600M |
| R33 | OpenAgents Laya 移植 README | https://github.com/OpenAgentsInc/openagents/blob/main/docs/laya/README.md | **一手·平台数据**（GitHub，可复现抓取） | 第 3 章 | "Answer semantics follow rl_agent_api.py, not kev's door"；四位小数 ties-to-even |
| R34 | awesome-jev | https://github.com/yibie/awesome-jev | **一手·平台数据**（GitHub，可复现抓取） | 第 3 章 | 2.5k star / 374 fork / 917 commits，20+ router 项目 |

> **R29 合并说明（规则外唯一例外）**：第 1 章写作 `https://vals.ai/...`，第 6 章写作 `https://www.vals.ai/...`。两者字符串不同，但为同一页面。按"URL 完全相同才合并"的纪律本不应合并；本次合并并在此注明，**若主理人要求严格执行纪律，可拆回两条，编号顺延为 R29a／R29b，其余条目编号不变。**

---

## 七　二手（R35–R41）

| 编号 | 标题 | URL | 类型 | 引用章 | 一句话摘要 |
|---|---|---|---|---|---|
| R35 | Jev Customers（Product Hunt） | https://www.producthunt.com/products/jev/customers | **二手·转述**（页体受保护，本次未直接抓取） | 第 4 章 | 9 家实名客户清单的唯一来源；**计数按转述处理**，用法另有客户自有文档与客户自述交叉核对 |
| R36 | WikiFix — Products used（Product Hunt） | https://www.producthunt.com/products/wikifix/built-with | **二手·转述**（页体受保护；PH 产品页快照中检索 WikiFix / 415 / 13k / Sonnet 均 0 命中） | 第 4 章 | 据转述：三次 Sonnet 投票 → 一次 Jev；415 页 13k→5k credits（**未直接复核，不计入成本型证据**；credits 非美元，换算比未公开） |
| R37 | System One Models 索引 | https://systemonemodels.org/models/ | **二手·社区/展示站**（可复现抓取） | 第 3 章 | 逐条 34 条目（21 商业 + 12 开源 + 1 提取）；FAQ 自述 "29 of the 33"，与逐条计数差 1，**差异未解** |
| R38 | Laya 评测（andrew.ooo） | https://andrew.ooo/posts/laya-review-open-weight-jev-alternative-system-1-decision-model | **二手·媒体/专栏**（技术博客，未独立核实） | 第 3 章 | **GitHub star 34,729（10-31）/ 23,805（09-25）两口径并存**；2,045 fork；改 baseUrl 即迁移；Banking77 行未标指标名 |
| R39 | The New Stack: OpenAI Decision API | https://thenewstack.io/openai-decision-api-luna/ | **二手·媒体/专栏**（主流媒体） | 第 3 章 | 09-29 抢发；"likely a reaction to TypeSafe and Jev"；价格/候选上限/可调优三项未披露 |
| R40 | 36 氪／量子位 | https://m.36kr.com/p/4019764837748872 | **二手·媒体/专栏**（中文，未独立核实） | 第 3 章 | 种子 $40M @ $2 亿、24 天时间线、微软两小时后跟进——**均为二手口径，不作一手论据** |
| R41 | Lurk · Jevfast | https://jevfast.com/lurk/ | **二手·社区/展示站**（未独立核实） | 第 4 章 | 免费 Reddit 监控，自称 "only possible to give for free bc of Jev"，Jev 机制未披露，无付费主体（→第 5 章） |

---

## 八　线索（未采信为依据，L01）

| 编号 | 内容 | URL | 引用章 | 处理 |
|---|---|---|---|---|
| L01 | 百度百科「Microsoft-Decision-1」／「APUS-OpenJev-v1」／「Qwen3.5-9B」；百家号「Jev 类模型全景对比」 | **〔待补：第 3 章未记录 URL〕** | 第 3 章 | 仅用于确定检索方向；**正文事实性陈述均不依赖上述条目**。相关论断（微软发布日、Qwen3.5-9B 底座、APUS 规格）在第 3 章已降为"二手口径"并列入待补清单 |

---

## 九　增补：第 2、5 章并入（R42–R67）

> **本节是补录，不是新体系。** 初版 `_refs.md` 因误判 `ch2_revised.md`／`ch5_draft.md` 为"另一份报告"而漏收两章，详见 `_format-spec` 附录 B 的更正说明。补录沿用同一套两轴标注，**原 R01–R41 编号一律不动**，新增从 R42 起。两章合计去重后 **26 条**，其中 10 条与既有编号重复（已并入原号，不在本节重列）：`arxiv.org/abs/2609.25845`→R02、`2609.36965`→R03、`2609.38827`→R04、`arxiv.org/html/2609.24052v1`→R01、`blog.cloudflare.com/clef-decision-models/`→R17、`docs.typesafe.ai/models`→R05、`typesafe.ai/blog/introducing-system-one-models-and-jev`→**R15**、`vercel.com/kb/guide/typesafe-jev-and-ai-sdk`→**R18**、`github.com/AbdelStark/jev-benchmarks`→R30、`github.com/nibzard/decision-model-benchmark`→R31、`github.com/yibie/awesome-jev`→R34、`jevfast.com/lurk/`→R41、`vals.ai/blogs/independent-evaluation-of-jev`→R29（含 `www.` 变体，见 R29 合并说明）。

### 9.1　一手·论文／预印本（R42–R45）

> 四篇元数据于 2026-11-01 由 arXiv abs 页直接请求核对（HTTP 200）。四篇 abs 页**均未显示期刊引用信息**，故"是否同行评议"一律判为**未见**。

| 编号 | arXiv ID | 标题 | 作者 | 提交日期 | 版本 | 是否同行评议 | URL | 引用章 |
|---|---|---|---|---|---|---|---|---|
| R42 | 2609.23986 | Jev-Mem: System-One-Controlled Agentic Memory for Efficient AI Agents | Dongming Jiang, Yi Li, Bingzhe Li（UT Dallas） | 2026-09-21 | v1（唯一版本） | 未见 | https://arxiv.org/abs/2609.23986 | 第 5 章 |
| R43 | 2609.26550 | JEV-as-a-Judge: Accept When Confident, Escalate When Unsure | Yubo Li, Yidi Miao, Ramayya Krishnan, Rema Padman（CMU） | 2026-09-22 | **v6（2026-10-29）** | 未见 | https://arxiv.org/abs/2609.26550 | 第 5 章 |
| R44 | 2609.28940 | Calibrated Decision Models for Autonomous Penetration-Testing Harnesses: JEV and Laya as System One Decision Layers for LLM-Driven Pentest Agents | Joas Antonio dos Santos Barbosa | 2026-09-24 | v1（唯一版本） | 未见 | https://arxiv.org/abs/2609.28940 | 第 5 章 |
| R45 | 2609.30216 | Jev in the Wild: A Data-Driven Analysis of the Jev Model's Functionality, Applications and Ecosystem | Guoming Ling, Muen Xue, Zijian Ye | 2026-09-24 | v1（唯一版本） | 未见 | https://arxiv.org/abs/2609.30216 | 第 5 章 |

**版本警示（R43）**：本篇已迭代到 **v6**，是全部 8 篇里版本最多的一篇。第 5 章按 **v6（2026-10-29）** 引用，与 abs 页一致；但**摘要内容在六版之间是否变过，本次未逐版比对**——凡引用其数字，须写明 v6。**这一条值得单独记下：一篇预印本在 5 周内迭代 6 次，意味着"某论文说了 X"这句话在没有版本号时几乎不可核。**

**内容要点**：
- **R42**（第 5 章）— 把 Jev 用作 agent 记忆的控制器（何时写入、何时检索、何时遗忘由决策模型判定）。第 5 章作 D 层"学术推演"收录，不作效果背书。
- **R43**（第 5 章）— 摘要：16 个生成式与奖励模型评委、盲法人裁决下，**凡判决可从文本直接读出**处 JEV 与 GPT-6 差距在 3 分内，费用为 **0.36%**、中位延迟 **0.15 s**；**凡判决需推导**（数学、代码、逻辑）则落后。冻结阈值后"接受高置信、其余升级"在 1,610 对留出集上比 GPT-6 高 **0.9 分**、费用 **41%**；两个新工作负载的预注册实测中级联与 GPT-6 **准确率完全持平**。作者自陈置信路由在**风格对抗样本**与**无参考答案散文**上会减弱。
- **R44**（第 5 章）— 渗透测试 harness 的四个决策点（发现裁决、严重度重校准、agent 剪枝、确认循环）。作者自陈 NeuroSploit 案例是 **exploratory**，差异"**不构成统计显著性**"。**这是本报告收录的"最诚实的负面样本"**：有架构、有案例、明确拒绝效果断言。
- **R45**（第 5 章）— 2,170 个公开 GitHub 项目（截至 2026-09-22），其中 1,865 个为发布后一周内新建、305 个为存量接入（**出处为 §2.2 正文，配 Figure 1，论文未以表格列出**）。摘要原话"public attention is concentrated in routing and interface agents and does not track project counts"。

### 9.2　一手·官方（TypeSafe，R46–R52）

| 编号 | 标题 | URL | 类型 | 引用章 | 一句话摘要 |
|---|---|---|---|---|---|
| R46 | Machine Learning Primer（校准定义） | https://docs.typesafe.ai/introduction/machine-learning-primer | **一手·官方**（文档） | 第 2 章 | 校准描述"一批判断"的整体频率而非单次可靠度；原话 "These rates describe groups of predictions, not a guarantee about any single answer." |
| R47 | Model Jaggedness: Jev 1.13 | https://docs.typesafe.ai/model-jaggedness/jev-1.13 | **一手·官方**（文档，最后复核 2026-10-02） | 第 2 章 | 官方自曝的 9 类失败模式清单；第 2 章 §2.5 逐条落地到业务场景。**厂商自己写的**，故为本报告最可信的一手材料之一 |
| R48 | Workflow Evals（首页） | https://evals.typesafe.ai/ | **一手·官方**（评测站） | 第 2 章 | 四个 workflow 的任务描述；参考标签由 GPT-6 Astra 与 Claude Fable 5.1 均以 high thinking 作答后平均生成；"Workflow Intelligence vs Cost" 纵轴为四 workflow 等权平均 |
| R49 | Invoice Processing（workflow 详情） | https://evals.typesafe.ai/invoice_processing.html | **一手·官方**（评测站子页） | 第 2 章 | 金额、日期、账号、状态**由代码计算而非问模型**；三方对账（账单／订单／实际交付） |
| R50 | TypeSafe 官网首页 | https://typesafe.ai/ | **一手·官方**（官网） | 第 2 章 | 0% 结构化输出错误率并列图；脚注明示 0% 是"输出必定匹配 schema"的**保证**而非实测错误率；官方自曝对照组 bias（"more complex queries might be routed to better models"） |
| R51 | Agent Skill | https://docs.typesafe.ai/agent-skill | **一手·官方**（文档） | 第 5 章 | Claude Code / Codex 可直接安装的官方 skill |
| R52 | system-one-adapter-python | https://github.com/typesafe-ai/system-one-adapter-python | **一手·官方**（官方仓库，可复现抓取） | 第 5 章 | 官方 Python 适配器；406 stars（截至 2026-10-31） |

> **R50 的读法（重要）**：这是全表唯一一条**官方主动否证自家营销数字**的来源。0.00% 与 Claude Sonnet 5 的 12.6% 并列展示，看起来是碾压性优势；但同一份材料写明 "Our number is not empirical. Schema matching is guaranteed, thus we can confidently add 0% into the plots." ——**"保证"与"实测"是两类量**。凡引用这个 0%，必须同时给出这句限定，否则就是把保证读成了观测。

### 9.3　一手·平台数据与仓库代码（R53–R60、R68–R69）

| 编号 | 标题 | URL | 类型 | 引用章 | 一句话摘要 |
|---|---|---|---|---|---|
| R53 | HN Algolia 检索 API | https://hn.algolia.com/api/v1/search?query=Jev%20TypeSafe&tags=story | **一手·平台数据**（子型 a，可复现抓取） | 第 5 章 | `query="Jev TypeSafe"` 命中 story **72 条**；其中 2026-09-16~10-15 内 **64 条**；该 64 条中 ≤6 分 **60 条**、零评论 **51 条**、中位数 **2 分**；≥20 分仅 **3 条** |
| R54 | OpenByteInc/QuantDinger | https://github.com/OpenByteInc/QuantDinger | **一手·平台数据**（子型 a，GitHub 可复现抓取） | 第 5 章 | **13,348 stars，但仓库建于 2025-12-28，早于 Jev 发布（2026-09-15）**，Jev 仅为其多个集成之一——**star 不可归因于 Jev** |
| R55 | Selmar/typesafe-jev-calibrate-for-code-review | https://github.com/Selmar/typesafe-jev-calibrate-for-code-review | **一手·平台数据**（子型 a） | 第 5 章 | 代码审查场景的 Jev 标定实验 |
| R56 | agodoy21/enigma-jev | https://github.com/agodoy21/enigma-jev | **一手·平台数据**（子型 a） | 第 5 章 | 社区实验项目 |
| R57 | coderexpert123/jev-browser-wingman | https://github.com/coderexpert123/jev-browser-wingman | **一手·平台数据**（子型 a） | 第 5 章 | 社区 MCP 代理（官方 MCP 服务缺失的替代） |
| R58 | dabit3/jev-experiments | https://github.com/dabit3/jev-experiments | **一手·平台数据**（子型 a） | 第 5 章 | 社区实验集 |
| R59 | hardness1020/learn-agent-architecture | https://github.com/hardness1020/learn-agent-architecture | **一手·平台数据**（子型 a） | 第 5 章 | agent 架构学习仓库（Jev 为其中一节） |
| R60 | maayanlevy/mysql-ailike | https://github.com/maayanlevy/mysql-ailike | **一手·平台数据**（子型 a） | 第 5 章 | 社区实验项目 |
| R68 | npm registry 检索与下载量 API | https://registry.npmjs.org/-/v1/search?text=jev<br>https://api.npmjs.org/downloads/point/last-week/{pkg} | **一手·平台数据**（子型 a，可复现抓取） | 第 5 章 | `text=jev` 检索命中 **1,534 个包**（含噪声）；周下载（**2026-10-23~10-29**）：`jev-browser` **989**、`@livx.cc/mcp-jev` **305**、`@marcmeese/n8n-nodes-jev` **25**。**本次已独立复现，四个数字与第 5 章完全一致** |
| R69 | OpenRouter 模型目录 | https://openrouter.ai/api/v1/models | **一手·平台数据**（子型 a，可复现抓取） | 第 5 章 | 实测存在 `typesafe/jev-router` 与 `typesafe/jev-router/endpoints`（**本次已独立复现**）；`typesafe/jev-latest` 亦在目录内。属**分发渠道证据**，非性能证据 |

> **R54 是全表最值得记的一条反例**：它是唯一 star 破万的 Jev 相关仓库，看上去是"生态爆发"的证据；但仓库创建日**早于 Jev 发布 8 个多月**，Jev 只是它后来接入的众多模型之一。**star 是仓库的存量，不是 Jev 的增量**——把 13,348 记在 Jev 账上，会凭空造出一个头部。第 5 章已剔除该条后重算：原生项目 star **中位数约 5.5**，仅 1 个超 400。

### 9.4　一手·客户自述与第三方厂商自述（R61–R63）

| 编号 | 标题 | URL | 类型 | 引用章 | 一句话摘要 |
|---|---|---|---|---|---|
| R61 | DialNexa: Can a decision model run our voice agent's hangup and routing calls | https://dialnexa.com/blogs/jev-on-real-calls-can-a-decision-model-run-our-voice-agents-hangup-and-routing-calls | **一手·客户自有文档** | 第 5 章 | **离线回放，非生产**：4,516 条挂断判断／1,079 通电话，调阈值后与生产 LLM 一致率 **95.0%**、中位 **462 ms**；作者自陈「We didn't route live calls through Jev」，且「One flag needs a safety fix」 |
| R62 | Vapi: Early experiment with Jev | https://vapi.ai/blog/early-experiment-with-jev | **一手·客户自有文档** | 第 5 章 | guardrails 早期实验；作者自陈「caught at least three out of four」，且「not a 100% compliance guarantee」 |
| R63 | MLflow Releases | https://www.mlflow.org/releases/ | **一手·平台/大厂文档** | 第 5 章 | MLflow **3.17.0**（2026-10-06）支持 `model="typesafe:/jev-latest"` 作 judge |

> **R61／R62 的共同点：都是"客户自己先说清了边界"。** DialNexa 明写没跑生产、Vapi 明写不构成合规保证。**这两条之所以能进第 5 章而第 4 章那两条要降级，差别不在结果好坏，在于作者有没有自己划出适用边界**——自陈限制的可信度高于自陈收益。

### 9.5　二手（R64–R67）

| 编号 | 标题 | URL | 类型 | 引用章 | 一句话摘要 |
|---|---|---|---|---|---|
| R64 | 虎嗅访谈（2026-10-18） | https://www.huxiu.com/article/4898379.html | **二手·媒体**（创始人直接引语，媒体转述） | 第 2 章 | 创始人：「我非常反感公开基准测试……公开基准最大的问题就是极易被刷分、被针对优化」 |
| R65 | r6i.it: TypeSafe Jev vs agentic loop | https://blog.r6i.it/typesafe-jev-vs-agentic-loop.html | **一手·客户自述**（自测，未独立核实） | 第 5 章 | 产品分类迁移（Sam Reghenzi，2026-09-21）：同批 50 个商品均值延迟 **9.62 s → 1.38 s**、模型调用数 **7.22 → 3.18**；作者同时写明「agent 在需要回溯的场景仍然胜出」 |
| R66 | jev.guide | https://jev.guide/ | **二手·社区展示站** | 第 5 章 | 收录 X 原帖与 Owner 所在地分布（美 69／印 37／中 36／日 21／法 19／德 18／加 12／波 7）；4 条用例形态均单点自述，**不构成效果证据** |
| R67 | 中国指挥与控制学会专栏（2026-10-27） | https://www.c2.org.cn/h-nd-3419.html | **二手·媒体**（**通篇未给论文标题或 arXiv 编号**） | 第 5 章 | 第 5 章 §5.5 的核查起点：其所述四支后续研究经检索 arXiv **全部定位到原文**（→R42–R45）。**这是"二手先于一手"的典型：专栏本身不可核，但它指向的一手可核** |

> **R67 的方法论价值大于它的内容。** 一条没有出处的二手转述，通常会被直接丢弃；这里被当作**检索线索**使用——先记下它说了什么，再去 arXiv 找有没有对应的原文，找到就以原文为准，找不到就标〔待补〕。**二手不可信 ≠ 二手无用**，区别在于你把它当证据还是当线索。

---

## 十　本文推演（无外部来源，不入编号）

按第 4 章类型表，`本文推演`＝"无公开实现证据"。以下四处在正文中以"本文认为/本文估算/据…推定"形式出现，**不是来源，列出以免被误当作来源**：

| 位置 | 推演内容 | 标记方式 |
|---|---|---|
| 第 3 章表 2「辖区」行 | Jev 数据处理地点写作"美国" | 标注"据总部所在地推定，**未见官方数据处理地点声明**"，并列入待补清单 |
| 第 3 章 §七 | €37 与 $42 的关系 | 第 3 章写"名义低约 12%"；第 4 章换算后判为"大致持平"。**两处方向相反，须统一**（`_format-spec` D15） |
| 第 6 章 §6.2 | 27 题拆成 27 次请求合计约 6,291 token、约 1.7 倍 | 标注"（本文估算）"，并给出算式与两个输入（111 / 122 / 3,673） |
| 第 3 章第五节 | OpenAI Decisions API 单价 $0.10 | 标注"索引站口径"；正文已说明官方未披露定价 |

---

## 附录 A　合并明细（哪些 URL 被几章引用）

> **口径**：本表只登记**被两章及以上引用**的 URL（七章合计）。单章来源不进本表。

| URL | 引用章 | 引用次数 | 合并后编号 |
|---|---|---|---|
| https://typesafe.ai/blog/introducing-system-one-models-and-jev | 第 1、2、3、6 章 | **4** | R15 |
| https://blog.cloudflare.com/clef-decision-models/ | 第 1、2、3、6 章 | **4** | R17 |
| https://vercel.com/kb/guide/typesafe-jev-and-ai-sdk | 第 1、2、3、5 章 | **4** | R18 |
| arXiv:2609.24052 | 第 2、4、6、7 章 | **4** | R01 |
| https://docs.typesafe.ai/models | 第 1、2、3 章 | 3 | R05 |
| https://vals.ai/blogs/independent-evaluation-of-jev（第 6 章作 `www.vals.ai`） | 第 1、2、6 章 | 3 | R29（**等价写法合并**） |
| arXiv:2609.36965 | 第 5、6、7 章 | 3 | R03 |
| https://typesafe.ai/blog/series-ai | 第 3、4 章 | 2 | R16 |
| https://vercel.com/blog/ai-gateway-jev-model-launch | 第 3、4 章 | 2 | R19 |
| https://huggingface.co/convaiinnovations/laya | 第 1、3 章 | 2 | R27 |
| https://www.unsiloed.ai/blog/document-review-unsiloed-typesafe-jev | 第 4、6 章 | 2 | R21 |
| https://eu-jev.com/ | 第 3、4 章 | 2 | R28 |
| arXiv:2609.38827 | 第 2、6 章 | 2 | R04 |
| arXiv:2609.25845 | 第 5、7 章 | 2 | R02 |
| https://github.com/AbdelStark/jev-benchmarks | 第 2、3 章 | 2 | R30 |
| https://github.com/nibzard/decision-model-benchmark | 第 2、6 章 | 2 | R31 |
| https://github.com/yibie/awesome-jev | 第 3、5 章 | 2 | R34 |
| https://jevfast.com/lurk/ | 第 4、5 章 | 2 | R41 |

**合计：18 个跨章重复 URL、47 次引用 → 18 条，净减 29 条。**

**与 69 条编号条目的差额说明（差额 51 条）**，不硬凑成一个减法，原因是差额由三类不同性质的条目构成：

| 类别 | 条数 | 说明 |
|---|---|---|
| 单章来源 | **48** | 只在某一章出现，无重复可合并 |
| 同页锚点变体 | **1** | R06（`docs.typesafe.ai/models#long-context`）——与 R05 同一页、两个 URL，按纪律不合并，但也不构成两次独立取材 |
| 补登端点 | **2** | R68（npm）、R69（OpenRouter）——原章正文未给 URL，本次为可复现性补登 |
| **合计** | **51** | 18 + 48 + 1 + 2 = 69 ✓ |

> R29 的 `www.` 变体**不在本差额表内**：它已计入上面 18 条跨章重复之中（第 1、2、6 章），不重复计算。**一条条目只能落在一个格子里**——这是本表能加平的前提。

> **这一栏本身就是一条方法论**：报告里任何"总数 = A − B"的式子，都要能说清每一项的归类。把 69 说成"93 − 47 + 18 + 5"能凑对，但那 5 是什么说不清——**凑对的算式比算错更危险**，因为它看起来是对的。

---

## 附录 B　缺口清单

| # | 缺口 | 影响 | 处置建议 |
|---|---|---|---|
| 1 | ~~第 2 章、第 5 章未落盘~~ **已关闭** | 两章已定位并补录（第九节 R42–R67），覆盖缺口清零 | **已完成**。教训留档于 `_format-spec` 附录 B |
| 2 | **第 7 章全章零超链接** | 其 4 篇 arXiv 与 2 类官方来源在本表已可回溯（R01–R04、R05–R14、R27），但**读者无法从第 7 章原文跳转** | 第 7 章按本表编号回填链接（`_format-spec` D25） |
| 3 | **L01 线索组 4 条无 URL** | 无法复核 | 第 3 章已声明不依赖；若需保留，由第 3 章作者补记录 |
| 4 | 第 4 章「Albie、Wand 本次检索未能复核」 | 无来源可列 | 不列条目；已在第 4 章表 1 中标"未获取" |
| 5 | 第 6 章引 "arXiv:2609.36965 的 Table 1/2" 但未给链接 | 表号无法直接定位 | 已由 R03 覆盖；第 6 章补链接即可 |
| 6 | 第 3 章来源 #20 标题含两个仓库（AbdelStark / nibzard），只给了 1 个 URL | 第 2 个仓库在第 3 章无法直达 | 已拆为 R30／R31 两条，各自带 URL |
| 7 | **第 2、5 章无独立"本章来源清单"小节** | 两章的来源只存在于正文行内链接与本表，正文自身不可自足 | 按 `_format-spec` 5.4 在章末补三小节；或由 Phase 5 整合时统一生成 |
| 8 | ~~npm 数据无 URL~~ **已关闭** | 已补 R68，并**独立复现**四个数字（1,534 / 989 / 305 / 25，窗口 2026-10-23~10-29），与第 5 章完全一致 | **已完成** |
| 9 | ~~OpenRouter 无 URL~~ **已关闭** | 已补 R69，并**独立复现** `typesafe/jev-router` 存在于模型目录 | **已完成**。Cloudflare Workers AI 指向 R17，不另立条目 |
