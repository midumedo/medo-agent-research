# 第 4 章　已验证的生产落地：实名客户、Unsiloed 双模型互查与 500 万条学术部署

> 本章只回答一个问题：**有没有人真的靠 Jev 跑起来了，跑成了什么形态，收益是成本型还是质量型。**
> 证据门槛：只收**有第三方可核验的规模证据或付费主体**的用法；无规模证据的 POC 归第 5 章。

## 论点

「用起来了」这件事是真的，但**证据密度极不均匀**：9 家实名客户里只有少数能追溯到客户自有文档，其余停留在厂商与客户共同策划的展示页；真正同时给出规模、基线、成本与失败数的只有两个案例——Unsiloed 的双模型互查与一篇 500 万条语料的学术部署。本章的结论因此分两层：**落地形态已被验证，收益性质则多数是成本型而非质量型。**

## 一、实名客户：先做减法，再做核对

[Product Hunt 的 Jev 客户页](https://www.producthunt.com/products/jev/customers)列出 9 家实名产品与创始人署名引言。需要说明的是，该页本次受 Cloudflare 保护无法直接抓取，本节改以**客户自有文档 + [Product Hunt 产品页](https://www.producthunt.com/products/jev)的使用评价卡**交叉核对，核对结果与二手转述有出入。

**Famulor**：团队自有的 [changelog](https://docs.famulor.io/changelog)（2026-09-22）写明「Jev, TypeSafe AI's decision model, now powers Famulor's advisory message labels」——给来信消息打 `Possible scam`、`Advertising` 等**咨询性标签**，与 Milian copilot 分工。同一份文档主动写明「They are advisory and can be wrong」，用户可在 History 驳回、管理员可整体关闭。**这是本章唯一由客户自己写进产品文档、且自带免责声明的用例**；但它不是「实时语音通话中做结构化判断」，而是消息标签——二手转述在这里需要修正。

**WikiFix for Confluence**：产品定位由 [Atlassian Marketplace 页面](https://marketplace.atlassian.com/apps/2836392116/wikifix-for-confluence)核实（扫描 Confluence、找出互相矛盾/过期/无主的页面并写修复，逐条人工批准）。其[使用评价卡](https://www.producthunt.com/products/wikifix/built-with)原话：「That audit used to take three votes from Claude Sonnet. Jev does it in one call and returns a calibrated probability we set a threshold on. Scanning the same 415-page handbook dropped from 13k credits to 5k.」——**省的是 credits，不是准确率**。

**gg-friggin-ez**（Shikhar Srivastava）与 **Fit Receipt**（Crystal Chang）的引言见产品页评价卡。前者替代 OpenAI omni-moderation，专治「obfuscated text, romanized Indic, and the usual game chat evasion tricks」，Jev 输出 toxicity/profanity/severity/language/obfuscation 的校准分，再由确定性阈值映射为 `ALLOW / SUSPICIOUS_REVIEW / AUTO_CENSOR / AUTO_BAN`；后者「When confidence is below 0.7, we show "trade-off still to confirm" instead of pretending to be sure」。

**两处必须纠正的判断**：其一，**Bevel 不是客户，而是竞品**。其[官网 eu-jev.com](https://eu-jev.com/)标题即「First System One Model Hosted in the EU」，署名 by Bevel；正文写明「Your request goes straight to our Hetzner server in Germany… No proxy, CDN, or external model API sits in between」「Prompts and answers are processed in Germany and are not stored」，接口为「Jev-style API requests」，模型 ID 设为 **`eu-jeff-latest`**（拼作 jeff，非 jev）、`POST /v1/systemone` + Bearer 鉴权，三原语同端点。价格页宣称「Same price as Typesafe's Jev」，但标价 **€37/十亿输入 token**（$5 起用，输出免费），与 Jev 的 $42 币种不同、名义低约 12%——**「同价」是 Bevel 的说法，不能写成事实等同**。定位上它是**API 契约兼容、产品上替代**的供应商（兼容的是接口，替代的是供应商），应归第 3 章竞品。需注意：官网承诺的是「processed in Germany and are not stored」，这是**数据处理地点**的承诺，**不等于合规认证**——本文不替它升格为法律结论。（本文认为：这也是「类 Jev」赛道第一条不依赖模型质量的差异化轴——美国闭源厂商无法靠「发个更强的模型」回应数据驻留要求。）其二，**lurk 只有社区展示站记录**（[jevfast.com](https://jevfast.com/lurk/)，自称「only possible to give for free bc of Jev」，Jev 的判断机制未披露），无付费主体、无规模证据，按本章判据归第 5 章。**Albie、Wand 本次检索未能复核**；**Ana by Vertice** 的产品定位可由[官方页](https://www.vertice.one/ana)核实（软件采购谈判 agent，自称 4,000+ 场谈判、5 亿美元 spend），但 Jev 用法仅见于客户页。

### 表 1　实名客户核对表（9 家 → 有效 5 家 + 1 家证伪）

| 客户 | 产品定位 | Jev 用法 | 证据性质 | 收益类型 |
|---|---|---|---|---|
| Famulor | 德国 AI 语音/消息 agent 平台 | 消息咨询标签（诈骗/广告） | 客户自有 changelog，一手可核验 | 成本型（未公布数字） |
| WikiFix for Confluence | Confluence 知识库维护 App | 替代三次 Sonnet 投票做 QC，一次调用+阈值 | PH 评价卡（转引，页体受保护） | **成本型**：13k→5k credits / 415 页 |
| gg-friggin-ez | 实时聊天审核 | 校准分 + 确定性阈值四档处置 | PH 评价卡，客户署名 | 成本型为主，质量型未量化 |
| Fit Receipt | 电商适配/推荐 agent | 封闭问题判断 + 0.7 以下降级 + receipt | PH 评价卡，客户署名 | **质量型**（诚实度，非准确率） |
| Ana by Vertice | 软件采购谈判 agent | 仅客户页记载，细节未公开 | 仅 PH 客户页，本次未复核 | 未知 |
| Albie / Wand | 未获取 | 未获取 | 未能复核 | 未知 |
| lurk | Reddit 话题监控（免费） | 机制未披露 | 社区展示站，无付费主体 | 不计入（→第 5 章） |
| Bevel（eu-jev.com） | 欧盟托管、API 契约兼容 Jev 的**替代供应商** | — | 一手官网，可复核 | **证伪：非客户**（→第 3 章） |

## 二、Unsiloed：双模型互查，全报告证据密度最高的单个案例

Unsiloed 的[工程博客](https://www.unsiloed.ai/blog/document-review-unsiloed-typesafe-jev)把分工写得很清楚：**Unsiloed 负责「读得对不对」，Jev 负责「读出来的东西合不合理」**。前者每个字段返回 `extraction_score` 与 `grounding_score` 及 bbox 引证；后者看不到图像、也看不到 Unsiloed 的分数，只接收抽取结果与上下文。

**prompt 结构**：`state` 由三段构成——检查范围指令（"Check for obvious quantity, unit or frequency errors. Dose means amount taken each time, not supply quantity. Do not assess patient-specific safety or propose corrections."）、`careContext`（成人门诊用药核对，52 岁）、`medications[]`（含 id/medicine/dose/frequency/route/instructions）。`questions` 里每行一个 `noul`，并自带 `criteria.true/false` 两段文案；**问题 key 不下发给模型**，靠 `row_id` 对齐。六行共用一次请求，问题彼此独立。

**阈值**：读数分 < 0.90 或合理性分 < 0.50 即送审，且「A high Jev answer must not cancel a low Unsiloed score」——两个理由同时保留。

**成本**：6 问 1,812 输入 token，按 $42/十亿输入 token 计 **$0.000076/文档**，10 万份约 **$7.61**（仅 Jev 侧，不含抽取与人工）。

**关键失败案例**：咖啡渍遮住的一行，Unsiloed 读作「1 tablet」、extraction 0.74 / grounding 0.76 被标记，而 **Jev 给 0.94**——它看不到污渍；反向的布洛芬行「10 tablets, three times daily」双分 0.99，**Jev 给 0.04**。原文的判词是「Each check flags a review need the other misses」。这说明双模型互查的价值不在提高准确率，而在**把「哪一行需要人看」的排序做对**——也是第 6 章「共识≠正确」的原型。

## 三、规模证据的可信度分级：同一件事，差一个量级

**平台一手观测**：[Vercel 官方博客](https://vercel.com/blog/ai-gateway-jev-model-launch)（2026-09-18）称 Jev 上线 24 小时内「nearly 13% of paid teams were using it」，是 GPT-5.6 家族的 2 倍、Fable 5.1 的 6 倍以上，18 小时破 10%，为 AI Gateway 史上最快；文末自带限定：「the next test is whether that early adoption lasts」。**分母明确、口径单一、平台可复核**。

**公司自述**：[TypeSafe 融资公告](https://typesafe.ai/blog/series-ai)（2026-10-09，8.7 亿美元、75 亿美元估值、a16z 领投）称「A third of the Fortune 500 are getting their Jev on」「We've saved customers millions of dollars in production already」——**无客户名单、无 case study、无「在用」的口径定义**。

同一件事的两个数字，可信度差一个量级。且 Vercel 的 13% 度量的是**采用速度**，不是效果。

## 四、500 万条：唯一同时具备规模、基线、成本与零失败的第三方证据

Texas State University 的 Rafe 与 Das 在 [arXiv:2609.24052](https://arxiv.org/html/2609.24052v1)（2026-09-21）把德州 2017–2025 年 **5,018,080 条**警方事故叙述编码为概率化事故变量。schema 共 27 问（16 个存在性、8 个分类、3 个序数，其中 7 个门控，τ=0.5），设计规则包括「一题一判断」「presence 先于 detail」「每个分类题必带 no-match」「命名实体从封闭集选」「数字预分桶」。

结果：对人工标签 **F1 = 0.908**；对照两个前沿生成模型，原文只给了一句「One frontier model gains 0.059 and the other is indistinguishable from it」（**未点名厂商与型号**），并强调「Calibration varies by model rather than by paradigm」。运行侧：中位延迟 0.20 s、p90 0.33 s、持续 44 req/s、**0 failed calls**；平均 3,673 输入 token/条，其中约 3,451 来自 schema 本身——**成本由问题数（122 token/问）主导，而非文本长度**。花费：**$0.154/千条**，全语料外推 **$774**，全部模型调用合计 **$55.79**。

需要打折的是「零失败」：论文自陈 typed 模型在结构上不可能产生类型错误，所以这是**接口层的零失败**，不是判断层的零错误。

## 五、已被验证的四类落地形态

### 表 2　落地形态归纳

| 形态 | 代表 | 共同前置条件 | 复制难度 |
|---|---|---|---|
| ① 结构化判断嵌入既有流程 | Famulor 消息标签、Ana 采购谈判 | 流程里已存在一个「窄判断」卡点 | 中：需改造既有链路 |
| ② 替代多次 LLM 投票做 QC | WikiFix（三次 Sonnet → 一次 Jev） | 已有可接受的基线判定 + 阈值可调 | **最低**：阈值 + 抽样验收即可 |
| ③ 置信度驱动 UI 降级 | Fit Receipt（<0.7 显示待确认） | 产品愿意公开承认不确定 | 低，但需要产品决策 |
| ④ 高一致性批量标注 | 学术 500 万条 | 需人工标注集做基线 + schema 是研究工作量 | **最高** |

三类共同前置条件可归纳为：**答案空间明确、有人工兜底、错误可发现或可承受**。②最易复制，因为它把「质量」外包给了阈值与抽样；④门槛最高，因为 schema 本身就是研究成果。

## 六、收益性质的诚实标注

- **成本型**：WikiFix（credits 13k→5k）、gg-friggin-ez（每条消息都跑，替代更贵模型）、Unsiloed（$0.000076/文档）。
- **采用速度**：Vercel 的 13%——不是效果。
- **诚实度**：Fit Receipt 的 0.7 待确认是**对模型不确定性的让步**，不是增益。
- **可核验的效果数字**：只有 Unsiloed（两向漏检的结构性说明 + 单文档成本）与学术部署（F1 0.908 对前沿模型、$0.154/千条）。

**「用起来了」不等于「效果更好」。**

## 七、本章的负空间

这 9 家里，**没有一家公开错误率、延迟 SLA 或事故记录**；唯一主动写「can be wrong」的是 Famulor。客户页由厂商与客户共同策划，存在**选择性披露**。产品页上唯一一条自称的生产数字来自一条评价卡（日本招聘平台，Jev 在生产约 10 天，996 家公司中判定 571 家，抽检 50 家 0 错）——单人自述、无审计、样本未公开。因此「9 家实名客户」证明的是**有人愿意署名**，**不证明「跑得稳」**。

## 小结

Jev 已经跨过「有没有人用」这道线：形态清楚、分工清楚、成本可算到小数点后六位。但它还没有跨过「跑得稳不稳」这道线——那需要错误率、SLA 与事故记录，而这些目前一条都没有公开。**选型决策者应当把本章当作「形态可行性证据」，而不是「可靠性证据」。**

---

## 本章新增来源清单

| # | 标题 | URL | 类型 | 一句话摘要 |
|---|---|---|---|---|
| 1 | Document Review With Unsiloed and TypeSafe Jev | https://www.unsiloed.ai/blog/document-review-unsiloed-typesafe-jev | 客户工程博客 | 双模型互查完整实现：分工、prompt、阈值、$0.000076/文档、咖啡渍与布洛芬两向漏检 |
| 2 | Estimating Crash Narratives with a Typed Decision Model (arXiv:2609.24052) | https://arxiv.org/html/2609.24052v1 | 学术预印本 | 500 万条德州事故叙述，27 问 schema，F1 0.908，$0.154/千条，0 失败调用 |
| 3 | Jev is the fastest-adopted model in AI Gateway history | https://vercel.com/blog/ai-gateway-jev-model-launch | 平台一手观测 | 24h 内近 13% 付费团队采用，2× GPT-5.6 家族、>6× Fable 5.1 |
| 4 | TypeSafe A raises Series AI | https://typesafe.ai/blog/series-ai | 厂商公告 | 「1/3 财富 500 强在用」「已省下数百万美元」，无名单无 case study |
| 5 | Jev on Product Hunt（产品页 + 评价卡） | https://www.producthunt.com/products/jev | 平台社区 | gg-friggin-ez、Fit Receipt 等客户署名的用法原文 |
| 6 | Jev Customers（Product Hunt） | https://www.producthunt.com/products/jev/customers | 平台客户页 | 9 家实名客户清单来源；本次受 Cloudflare 保护未能直接复核 |
| 7 | Famulor Changelog（2026-09-22） | https://docs.famulor.io/changelog | 客户自有文档 | Jev 驱动消息咨询标签，官方自陈「advisory and can be wrong」 |
| 8 | WikiFix for Confluence — Atlassian Marketplace | https://marketplace.atlassian.com/apps/2836392116/wikifix-for-confluence | 平台商品页 | 产品定位核实：扫描矛盾/过期/无主页面并写修复 |
| 9 | WikiFix — Products used（Product Hunt） | https://www.producthunt.com/products/wikifix/built-with | 平台评价卡 | 「three votes from Claude Sonnet」→ 一次 Jev；415 页 13k→5k credits |
| 10 | eu/jev — First System One Model Hosted in the EU | https://eu-jev.com/ | 竞品官网（一手） | Bevel 出品；德国 Hetzner 推理、不留存 prompt；Jev-style API，模型 ID `eu-jeff-latest`；€37/Btok，自称「同价」 |
| 11 | Ana — vertice.one | https://www.vertice.one/ana | 客户产品页 | 软件采购谈判 agent，自称 4,000+ 场谈判、5 亿美元 spend |
| 12 | Lurk · Jevfast | https://jevfast.com/lurk/ | 社区展示站 | 免费 Reddit 监控，Jev 机制未披露，无付费主体（→第 5 章） |
