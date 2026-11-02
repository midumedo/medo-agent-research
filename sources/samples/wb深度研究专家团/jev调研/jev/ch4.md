# 第 4 章　已验证的生产落地：实名客户、Unsiloed 双模型互查与 500 万条学术部署

> 本章只回答一个问题：**有没有人真的靠 Jev 跑起来了，跑成了什么形态，收益是成本型还是质量型。**
> 证据门槛：只收**有第三方可核验的规模证据或付费主体**的用法；无规模证据的 POC 归第 5 章。

## 论点

「用起来了」这件事是真的，但**证据密度极不均匀**：9 家实名客户里**只有 Famulor 1 家**能追溯到客户自有文档（changelog），**其余 2 家（gg-friggin-ez、Fit Receipt）的用法有可复核的 PH 评价卡；WikiFix 的用法与收益、Ana 的用法均只有转述**。而真正同时给出规模、基线、成本与运行统计的只有两个案例——Unsiloed 的双模型互查与一篇在 500 万条语料上做的学术部署。本章的结论因此分两层：**落地形态已被验证，收益性质则多数是成本型而非质量型。**

## 一、实名客户：先做减法，再做核对

据转述，[Product Hunt 的 Jev 客户页](https://www.producthunt.com/products/jev/customers)列出 9 家实名产品与创始人署名引言——**该页本次受 Cloudflare 保护无法直接抓取，本章读到的是他人对它的转述（二手·转述），不是原文**。因此本节不引用该页的措辞，改以**客户自有文档 + [Product Hunt 产品页](https://www.producthunt.com/products/jev)的客户自述评价卡**交叉核对，核对结果与转述有出入。

**这里有两层证据，强度不同，不能混着用**：**「用法」这一层**，凡能核到的每一家都另有**一手·客户自有文档**或**一手·客户自述**支撑，可逐条读原文；**「9 这个计数」这一层**，本次只能依赖那个受 Cloudflare 保护、未能直接抓取的页面（**二手·转述**）。换言之，本章可以替读者核对「某家用 Jev 干了什么」，但不能替读者核对「是不是正好 9 家」。下文凡涉及名单计数，均按转述处理。

**Famulor**：团队自有的 [changelog](https://docs.famulor.io/changelog)（2026-09-22）写明「Jev, TypeSafe AI's decision model, now powers Famulor's advisory message labels」——给来信消息打 `Possible scam`、`Advertising` 等**咨询性标签**，与 Milian copilot 分工。同一份文档主动写明「They are advisory and can be wrong」，用户可在 History 驳回、管理员可整体关闭。**这是本章唯一由客户自己写进产品文档、且自带免责声明的用例**；但它不是「实时语音通话中做结构化判断」，而是消息标签——二手转述在这里需要修正。

**WikiFix for Confluence**：产品定位由 [Atlassian Marketplace 页面](https://marketplace.atlassian.com/apps/2836392116/wikifix-for-confluence)核实（扫描 Confluence、找出互相矛盾/过期/无主的页面并写修复，逐条人工批准）——**这一层可复核**。但其 Jev 用法与收益，本次**无法回溯到任何我们实际读过的页面**：`/products/wikifix/built-with` 直接请求返回 Cloudflare 挑战页（"Just a moment…"，正文零内容），而在本次抓取成功的 PH 产品页快照（2026-10-21）中全文检索 `WikiFix` / `415` / `13k` / `Sonnet` **均 0 命中**。因此下面这句只能作**转述**处理、不加引号：据转述，该团队原先的审计要三次 Claude Sonnet 投票，改用 Jev 后一次调用即返回可设阈值的校准概率，同一份 415 页手册从 13k credits 降到 5k——**即便这对数字成立，它度量的是调用量，不是准确率**。

**转述里的数字只能当线索，不能当证据**：13k→5k 未直接复核，且 **credits 是 WikiFix 平台的计量单位、美元换算比未公开**——所以既不能换算成金额（更不能读成「省了 1.3 万美元」），也**不能据此推算「每页多少 credits」或「降幅约百分之多少」**，那些都是二次推算，在源头不可核的前提下不成立。**本条不计入本章的成本型收益证据。**

**gg-friggin-ez**（Shikhar Srivastava）与 **Fit Receipt**（Crystal Chang）的引言取自 [Product Hunt 产品页](https://www.producthunt.com/products/jev)——**这是本章唯一两条能自证到具体载体的客户引文**：该页本次抓取成功，快照内嵌时间戳 2026-10-21，引句逐字可核（与上文 WikiFix 那条形成对照，后者无法回溯到任何读过的页面）。前者替代 OpenAI omni-moderation，专治「obfuscated text, romanized Indic, and the usual game chat evasion tricks」，Jev 输出 toxicity/profanity/severity/language/obfuscation 的校准分，再由确定性阈值映射为 `ALLOW / SUSPICIOUS_REVIEW / AUTO_CENSOR / AUTO_BAN`；后者「When confidence is below 0.7, we show "trade-off still to confirm" instead of pretending to be sure」。

**两处必须纠正的判断**：其一，**Bevel 不是客户，而是竞品**。其[官网 eu-jev.com](https://eu-jev.com/)标题即「First System One Model Hosted in the EU」，署名 by Bevel；正文写明「Your request goes straight to our Hetzner server in Germany… No proxy, CDN, or external model API sits in between」「Prompts and answers are processed in Germany and are not stored」，接口为「Jev-style API requests」，模型 ID 设为 **`eu-jeff-latest`**（拼作 jeff，非 jev）、`POST /v1/systemone` + Bearer 鉴权，三原语同端点。价格页宣称「Same price as Typesafe's Jev」，但标价 **€37/十亿输入 token**（$5 起用，输出免费），与 Jev 的 $42 币种不同、名义低约 12%；按 1 EUR ≈ 1.14 USD 估算，€37 约合 $42，**两者大致持平**——「名义低 12%」是币种不同造成的数字错觉，不是真实价差。本文不做汇率时点考证，只作量级判断。**「同价」是 Bevel 的说法，本章既不写成事实等同（汇率时点未核），也不反过来读成「Bevel 更便宜」。**定位上它是**API 契约兼容、产品上替代**的供应商（兼容的是接口，替代的是供应商），应归第 3 章竞品。需注意：官网承诺的是「processed in Germany and are not stored」，这是**数据处理地点**的承诺，**不等于合规认证**——本文不替它升格为法律结论。

其二，**lurk 只有社区展示站记录**（[jevfast.com](https://jevfast.com/lurk/)，自称「only possible to give for free bc of Jev」，Jev 的判断机制未披露），无付费主体、无规模证据，按本章判据归第 5 章。**Albie、Wand 本次检索未能复核**；**Ana by Vertice** 的产品定位可由[官方页](https://www.vertice.one/ana)核实（软件采购谈判 agent，自称 4,000+ 场谈判、5 亿美元 spend），但 Jev 用法仅见于客户页。

### 表 1　实名客户核对表（9 家 → 有效 5 家 / 未复核 2 家 / 不计入 1 家 / 证伪 1 家；有效 5 家中仅 3 家可自证）

| 客户 | 产品定位 | Jev 用法 | 证据性质 | 收益类型 |
|---|---|---|---|---|
| Famulor | 德国 AI 语音/消息 agent 平台 | 消息咨询标签（诈骗/广告） | 一手·客户自有文档（可复现抓取） | 成本型（未公布数字） |
| WikiFix for Confluence | Confluence 知识库维护 App | 据转述：三次 Sonnet 投票 → 一次 Jev + 阈值 | **二手·转述**（页体受保护，本次未能直接读取） | 转述线索，**不计入证据**：13k→5k credits / 415 页（未直接复核；美元值未公开） |
| gg-friggin-ez | 实时聊天审核 | 校准分 + 确定性阈值四档处置 | 一手·客户自述（平台托管；引句取自 2026-10-21 快照，可复核） | 成本型为主，质量型未量化 |
| Fit Receipt | 电商适配/推荐 agent | 封闭问题判断 + 0.7 以下降级 + receipt | 一手·客户自述（平台托管；引句取自 2026-10-21 快照，可复核） | **质量型（诚实度）／属让步非增益** |
| Ana by Vertice | 软件采购谈判 agent | 仅客户页记载，细节未公开 | 二手·转述（页体受保护） | 未知 |
| Albie / Wand | 未获取 | 未获取 | 未获取，未能复核 | 未知 |
| lurk | Reddit 话题监控（免费） | 机制未披露 | 二手·社区/展示站（未独立核实） | 不计入（→第 5 章） |
| Bevel（eu-jev.com） | 欧盟托管、API 契约兼容 Jev 的**替代供应商** | — | 一手·厂商自述（利益相关；竞品） | **证伪：非客户**（→第 3 章） |

**表 1 的读法**：这里的「有效」要再分三层——**3 家可自证**（Famulor 有客户自有 changelog；gg-friggin-ez 与 Fit Receipt 有可回溯到 2026-10-21 快照的逐字引文）+ **1 家仅产品定位可核**（WikiFix：Marketplace 页可核，但用法与收益均为转述）+ **1 家仅客户页转述**（Ana，本次未复核）。**这 5 家里没有一家给出可直接采用的量化收益**：Famulor 明确未公布数字，gg-friggin-ez 未量化，Fit Receipt 是产品规则而非结果，WikiFix 那对 credits 数字来自转述、未能直接复核，Ana 完全未知。**这是证据可得性的计数，不是效果的计数——这 9 家里没有任何一家提供了质量增益的量化证据。**

## 二、Unsiloed：双模型互查，全报告证据密度最高的单个案例

Unsiloed 的[工程博客](https://www.unsiloed.ai/blog/document-review-unsiloed-typesafe-jev)把分工写得很清楚：**Unsiloed 负责「读得对不对」，Jev 负责「读出来的东西合不合理」**。前者每个字段返回 `extraction_score` 与 `grounding_score` 及 bbox 引证；后者看不到图像、也看不到 Unsiloed 的分数，只接收抽取结果与上下文。

**prompt 结构**：`state` 由三段构成——检查范围指令（"Check for obvious quantity, unit or frequency errors. Dose means amount taken each time, not supply quantity. Do not assess patient-specific safety or propose corrections."）、`careContext`（成人门诊用药核对，52 岁）、`medications[]`（含 id/medicine/dose/frequency/route/instructions）。`questions` 里每行一个 `noul`，并自带 `criteria.true/false` 两段文案；**问题 key 不下发给模型**，靠 `row_id` 对齐。六行共用一次请求，问题彼此独立。

**把咖啡渍那一行摊开看**（字段与取值据博客原文，长句以 `…` 省略；完整请求见博客附带的 `jev-request.json`）：

```jsonc
// ① 抽取侧：Unsiloed 已保存响应，row-5 = 被咖啡渍遮住剂量的那一行（原图 1200×1500）
{ "value": "1 tablet",
  "score": { "grounding_score": 0.76, "extraction_score": 0.74 },
  "citation": { "page": 1, "bbox": [582, 975, 649, 994], "page_width": 1200, "page_height": 1500 } }

// ② 判断侧：同一行送 Jev（六行共用一次请求，此处只留 row-5），POST https://api.typesafe.ai/v1/systemone
{ "model": "jev-1.13.0",
  "state": { "context": "Check for obvious quantity, unit or frequency errors. … Do not assess patient-specific safety or propose corrections.",
             "careContext": "Adult outpatient medication reconciliation, age 52",
             "medications": [{ "id": "row-5", "medicine": "Cetirizine 10 mg tablet", "dose": "1 tablet",
                               "frequency": "Once daily as needed", "route": "Oral", "instructions": "For allergy symptoms." }] },
  "questions": { "row-5": { "type": "noul",
      "instructions": { "question": "Is the extracted dose and frequency plausible on its face …", "row_id": "row-5" },
      "criteria": { "true": "Plausible on its face; no obvious quantity, unit or frequency error.",
                    "false": "Clearly implausible; warrants review of the original prescription." } } } }

// ③ 响应：answers["row-5"]
{ "type": "noul", "noul": 0.94 }
```

**同一行，两个分数并列**：Unsiloed `extraction 0.74 / grounding 0.76` ↔ Jev `noul 0.94`。Jev 说「这条剂量看起来合理」（94% 概率为真），但它看不到咖啡渍——**0.94 高不代表「读对了」，只代表「没有理由怀疑」**。这正是双模型互查的结构性理由：两个分数回答的是两个不同问题，不能互相抵消。

**阈值**：读数分 < 0.90 或合理性分 < 0.50 即送审，且「A high Jev answer must not cancel a low Unsiloed score」——两个理由同时保留。

**成本**：6 问 1,812 输入 token，按 $42/十亿输入 token 计 **$0.000076/文档**，10 万份约 **$7.61**（仅 Jev 侧，不含抽取与人工）。

**关键失败案例**：咖啡渍遮住的一行，Unsiloed 读作「1 tablet」、extraction 0.74 / grounding 0.76 被标记，而 **Jev 给 0.94**——它看不到污渍；反向的布洛芬行「10 tablets, three times daily」双分 0.99，**Jev 给 0.04**。原文的判词是「Each check flags a review need the other misses」。这说明双模型互查的价值不在提高准确率，而在**把「哪一行需要人看」的排序做对**——也是第 6 章「共识≠正确」的原型。该案例证明机制存在；截至目前，尚无公开证据显示该机制被工程化复现或规模化（见第 5 章 5.8）。

## 三、规模证据的可信度分级：同一件事，不在同一层级

**平台一手观测**：[Vercel 官方博客](https://vercel.com/blog/ai-gateway-jev-model-launch)（2026-09-18）称 Jev 上线 24 小时内「nearly 13% of paid teams were using it」。原文对倍数的完整表述是「By hour 24, nearly 13% of paid teams were using it. That's 2x the GPT-5.6 family and more than 6x Fable 5.1's share」——**三者同为同一平台、同一分母（AI Gateway 的付费团队）、同一时间窗（上线后 24 小时内使用该模型的团队占比）**；并以「Every other recent model launch remained below 7% after a full day」交叉印证（13 ÷ 7 ≈ 1.9，与 2× 自洽）。Jev 在 18 小时破 10%，平台称其为 AI Gateway 史上最快；文末自带限定：「the next test is whether that early adoption lasts」。**分母明确、口径单一、但仅平台方可复核**——外部读者无法复算 Vercel 的内部遥测，这既是它的强项（分母唯一、不是自述）也是它的边界（不可独立复算）。

**公司自述**：[TypeSafe 融资公告](https://typesafe.ai/blog/series-ai)（2026-10-09）称「A third of the Fortune 500 are getting their Jev on」「We've saved customers millions of dollars in production already」——**无客户名单、无 case study、无「在用」的口径定义**，属公司自述，本章只作口径判断，不作证据。

同一件事的两个数字，可信度不在同一层级。且 Vercel 的 13% 度量的是**采用速度**，不是效果。

## 四、500 万条语料、19.6 万条实测：唯一同时具备规模、基线、成本与运行统计的第三方证据

Texas State University 的 Rafe 与 Das 在 [arXiv:2609.24052](https://arxiv.org/html/2609.24052v1)（2026-09-21）把德州 2017–2025 年的警方事故叙述编码为概率化事故变量。schema 共 27 问（16 个存在性、8 个分类、3 个序数，其中 7 个门控，τ=0.5），设计规则包括「一题一判断」「presence 先于 detail」「每个分类题必带 no-match」「命名实体从封闭集选」「数字预分桶」。

**先把规模口径说清（这是全章最容易读错的地方）**：**5,018,080 条是语料规模，不是实际编码量**——论文两次强调全语料「the corpus itself was not coded」。因此本章能替它担保的实测规模是 **约 19.6 万条**，500 万条是外推的适用面。**规模口径还要再分三层**（否则会与第 2 章对照表里的「240 万次答案」读成打架）：分析语料 **5,018,080** 条；第一阶段以 10 个 presence 问题跑 **500,000** 条随机帧、**499,500** 条返回答案；第二阶段以完整 27 问编码 **195,857** 条，其中 **150,000** 条构成随机层（论文称其为所有总体估计的推断基础；论文 4.1 节称其为 195,857 条中的「150,000 of them」，3.2 节又称其「from the first-stage sample」，**两处表述的层级不同，本章不替它选定**；按 4.1 节口径推算，余 **45,857** 条为富集层），**论文明确富集层从不与随机层合并**用于患病率估计。**240 万次答案即随机层 150,000 条 × 16 个 presence 变量**（乘数口径为本文按算术反推，论文未明示）。两阶段答案合计约 **1,028 万**（499,500×10 + 195,857×27），**这个数论文同样未给，本章仅用于说明量级**。

结果：对人工标签（2,416 条可用判断）**F1 = 0.908**；对照两个前沿生成模型，原文只给了一句「One frontier model gains 0.059 and the other is indistinguishable from it」（**未点名厂商与型号**，即前沿模型比 typed 模型高 0.059），并强调「Calibration varies by model rather than by paradigm」。运行侧：中位延迟 0.20 s、p90 0.33 s、持续 44 req/s、**0 failed calls**（**是调用层口径，不是编码零错误，详见本节末**）；平均 3,673 输入 token/条，可干净地拆成两块：**27 题 schema 项约 3,562**（Table 2 直接拟合在 27 题处的单一截距，已吸收 schema 全部开销）+ **叙事文本约 111**（按 0.236 token/字符 反推约 470 字符；中位 378 字符的叙事只贡献约 89）。**3,562 + 111 = 3,673，加得平**；均值高于中位是长尾叙事所致（p95 为 935 字符），不是模型不稳定。论文未再把 3,562 内部拆细。

**成本由问题数主导，而非文本长度**：每多一题边际成本恒为 **122 token**（拟合 β，R²=0.987，7 个题数点、420 次调用）；同一模型在 27 题给出 α=171 + 122×27 ≈ 3,465 的 schema 项，与直接拟合的 3,562 是同一件事的两种参数化。折算成「每问成本」应读作 **约 122–128 token/问**（122 为纯边际，128 = 3,451 ÷ 27 为含截距均值），**差异来自截距口径，不是题面长度浮动**。中位叙事只贡献约 89 token——这就是「schema 规模而非文本长度决定成本」这句话的数据基础。

**花费（五个数字、三组口径，必须分开读，否则会误以为算错）**：

| 数字 | 口径 | 覆盖范围 |
|---|---|---|
| **$0.1543/千条** | 实测单价（Table 2 报 0.1543，正文舍入写作 $0.154） | 第二阶段实编 195,857 条，实际支出 $30.22 |
| 分项合计 **$55.48** | 论文列出的三项分项之和 | 初筛 $25.23 + 编码 $30.22 + 成本模型拟合扫描 $0.03 |
| **未披露差项（非独立支出）$0.31** | 占总额 0.56%，用于闭合论文自报总额与三项已计价支出之差 | **不计入任何单位成本或外推**；来源论文未披露，见下方推算 |
| **$55.79** | **论文报告的全部模型调用总额**（评测样本，非全语料） | 上三项 + 未披露差项；**不含**对照的前沿模型调用（原文称该组成本未被计量） |
| **$774** | **按 $0.1543/千条 对 5,018,080 条线性外推的全语料成本** | 估算值：0.1543 × 5,018.08 ≈ $774.3；全语料并未编码 |

**这张表加得平**：25.23 + 30.22 + 0.03 + 0.31 = **$55.79**。$0.31 的来源论文未披露；唯一在数值上对得上的，是论文另一处提到的一次未计价复跑——分类规则修订后「the full schema was re-run on a fixed sample of 2,000 narratives before and after the change」，2,000 × $0.1543/千条 ≈ **$0.309**。但「before and after」若各跑一次则为 $0.62，就对不上了。**因此本章把它标为「未披露差项」，不替论文补账。**

也就是说，**$55.79 与 $774 不在同一口径上**：前者是「这次实验真的花了多少」，后者是「如果整库都跑要花多少」。两者不能互相验算，也不能并列成「花了 $55.79 就省了 $774」这类叙述。

**「失败」这个词还要再拆一层口径**（前面的「0 failed calls」不能直接读成「零失败」）。论文报告的是 **0 次失败调用**（"0 failed calls"），与中位延迟 0.20 s、P90 0.33 s、44 req/s 并列在同一组运行统计里——**它证明的是吞吐稳定性，不是判断正确性**。

而且「零失败」只在调用层成立：第一阶段 500,000 条中 **499,500 条返回答案，500 条未返回，论文未解释**；第二阶段才报告 0 failed calls。**同一篇论文两个阶段对「失败」的记法不同，说明该指标没有统一定义。**

编码层错误则是存在的：论文在人工复核不一致处自陈这些是 **model errors**，并给出「若把被排除的那一对也算作模型错误，pooled F1 降至 **0.875**」——**0.875 是论文自己给的敏感性下界**，它比 F1 0.908 更能说明**准确率的稳健区间**，且是论文自陈，不是本文推算。另需注意 §2.3 明写「returns no free text, so no answer can be invalid and none has to be parsed」——**「解析零失败」在这个接口下是结构性事实，不是实测结论**。

**时序上值得记一笔**：arXiv v1 投稿于 2026-09-21，距 Jev 公开发布（2026-09-15）仅 **6 天**；而论文实测调用约 69.6 万次（499,500 + 195,857 + 420），按 44 req/s 折算仅约 4.4 小时纯机时——**机器时间不是瓶颈，拿到模型与定价才是**。这提示作者很可能握有早期访问权限（论文未披露与 TypeSafe 的合作性质）。这一点值得留意，因为它同时解释了本章的两个现象：为什么这篇论文能**先于任何商业客户**给出基线数字、运行统计与单价；以及为什么它的**失败统计只覆盖调用层、不覆盖判断层**——一个结构上不可能产生解析错误的接口，其「零失败」天然只能说明吞吐。

## 五、已被验证的四类落地形态

### 表 2　落地形态归纳

| 形态 | 代表 | 共同前置条件 | 复制难度 |
|---|---|---|---|
| ① 结构化判断嵌入既有流程 | Famulor 消息咨询标签（**单案例**；Ana by Vertice 待核实，若成立可归此类） | 流程里已存在一个「窄判断」卡点 | 中：需改造既有链路 |
| ② 替代多次 LLM 投票做 QC | WikiFix（三次 Sonnet → 一次 Jev）（**依据为转述，未直接复核**） | 已有可接受的基线判定 + 阈值可调 | **最低**：阈值 + 抽样验收即可 |
| ③ 置信度驱动 UI 降级 | Fit Receipt（<0.7 显示待确认）（**单案例支撑**） | 产品愿意公开承认不确定 | 低，但需要产品决策 |
| ④ 高一致性批量标注 | 学术 19.6 万条实测（语料 500 万条） | 需人工标注集做基线 + schema 是研究工作量 | **最高** |

**四类**共同前置条件可归纳为：**答案空间明确、有人工兜底、错误可发现或可承受**。逐类对照：① 的卡点是流程里**本来就存在一个窄判断**，答案空间天然封闭，人工兜底就是原岗位的人；② 的卡点是**已有可接受的基线判定且阈值可调**，人工兜底被换成抽样验收；③ 的卡点是**产品愿意公开承认不确定**，错误之所以「可发现」是因为 UI 直接把「待确认」显示给用户；④ 的卡点是**有人工标注集做基线**，schema 本身就是研究成果，人工兜底由标注集承担。

复制难度上，②最低，因为它把「质量」外包给了阈值与抽样（**②的可复制性判断同样带转述折价：本报告没有读到该团队的一手实现说明**）；④门槛最高，因为 schema 本身就是研究成果。③的难度不在工程而在产品决策，且目前**只有 Fit Receipt 一个案例支撑**——保留这一类的理由不是样本量，而是它的前置条件「产品愿意公开承认不确定」是一个真实且独立于其他三类的门槛：技术团队可以独自完成 ①②④，③必须由产品负责人签字。

## 六、收益性质的诚实标注

- **成本型**：gg-friggin-ez（每条消息都跑，替代 OpenAI omni-moderation）、Unsiloed（$0.000076/文档）、学术部署（$0.1543/千条）。**其中只有 gg-friggin-ez 有替代方案对照，且是定性对照、无数字**——原文只说通用生成式 LLM「can be too slow and expensive to run on every live-chat message」，未给价格；Unsiloed 与学术部署都只有绝对单价，没有「替代方案要花多少」的同口径对照（论文自陈对照的前沿模型「cost was not metered by that harness」）。因此本章只能把它们读成「**单位成本低且可预算**」，不能读成「比替代方案省 X%」。**WikiFix 的 13k→5k credits 属转述、未直接复核，不计入本条。**
- **采用速度**：Vercel 的 13%——不是效果。
- **诚实度**：Fit Receipt 的 0.7 待确认是**对模型不确定性的让步**，不是增益。
- **可核验的准确率/质量数字**：只有 Unsiloed 与学术部署提供了这一口径——Unsiloed 给的是「两向漏检」的结构性说明（咖啡渍行 Jev 0.94 而 Unsiloed 0.74/0.76；布洛芬行 Jev 0.04 而 Unsiloed 0.99/0.99），学术部署给的是 F1 0.908 对人工标签（论文另给敏感性下界 **0.875**）、以及前沿模型 +0.059 的差值。**其余可核验数字均为成本口径（Unsiloed $0.000076/文档、学术 $0.1543/千条）或采用口径（Vercel 13%）；Fit Receipt 的 0.7 是产品规则，不是结果；WikiFix 的 13k→5k 属转述、未直接复核，不列入。**

**本章没有一个客户提供了质量增益的量化证据。** 所有可核数字要么是成本、要么是采用、要么是产品规则；唯一带准确率口径的 F1 0.908 来自一篇作者很可能握有早期访问权限的学术论文，不是客户生产环境。

**「用起来了」不等于「效果更好」。**

## 七、本章的负空间

这 9 家里，**没有一家公开错误率、延迟 SLA 或事故记录**；唯一主动写「can be wrong」的是 Famulor。**该类客户页通常**由厂商与客户共同策划，存在**选择性披露**。

产品页上唯一一条自称的生产数字来自一条论坛帖（[《Where I put Jev in production on a large site, and where I didn't》](https://www.producthunt.com/p/jev/where-i-put-jev-in-production-on-a-large-site-and-where-i-didn-t)，作者 Hisashi Space，2026-09-30）：「I run a large job marketplace in Japan, and Jev has been in production on it for about 10 days」——首轮 996 家公司中判定 571 家（原文「Code settles most of them, and only the leftovers go to Jev, with just the two names (about 200 tokens)」）、**抽检 50 家 0 错**。这里要先分清归属：**571/996 是整条流水线（代码判掉大部分 + 残余交 Jev）的判定量，不是 Jev 单独判了 571 家**——Jev 只处理代码判不掉的残余。三点还需说明：**其一，该帖作者不在上述 9 家实名客户名单内**，这是与 9 家并列的另一条独立证据，不能读成「第 9 家客户」；**其二，单人自述、无第三方审计**，抽检方法与抽样规则均未公开；**其三，本次已补上直达原帖的链接**，但「可核验」到此为止——能核验的是**确实有人这样说过**，不能核验 571/996 与 0 错本身。

因此「9 家实名客户」证明的是**有人愿意署名**，**不证明「跑得稳」**。

## 小结

Jev 已经跨过「有没有人用」这道线：形态清楚、分工清楚、成本可算到小数点后六位。但它还没有跨过「跑得稳不稳」这道线——那需要**客户生产环境**的错误率、SLA 与事故记录，而本章 9 家客户里一条都没有公开。全章唯一的错误率线索来自那篇学术部署，且是论文自陈的敏感性下界（pooled F1 0.875），不是客户生产数据；它同时说明**「0 次失败调用」只覆盖调用层，不覆盖判断层**。**选型决策者应当把本章当作「形态可行性证据」，而不是「可靠性证据」。**

本章的证据分布本身就是结论：**能自证到具体载体的客户引文 2 条、客户自有文档 1 份、转述 2 家、可复核的第三方量化 1 篇、仅平台方可复核的遥测 1 条、Jev 厂商自述 1 条。** 一家都没有的是：**客户自己公布的前后对比成本，和质量增益的量化证据。**

---

## 本章新增来源清单

**来源标注规范（全报告通用，仅在本章首次出现处印一次，其余章只标不解释）**：类型标注分两轴——**轴 1「谁在说」定主分类，轴 2「怎么核」写在括号里，不改变主分类**。把两者混成一个标签，会出现「客户本人署名却被归为二手」这类错位。

| 主分类（轴 1） | 含义 |
|---|---|
| 一手·客户自有文档 | 客户自己写进产品文档、changelog、工程博客 |
| 一手·客户自述 | 客户本人在平台（评价卡、论坛）讲自己的使用 |
| 一手·厂商自述 | 厂商/竞品自己说（含官网、公告、遥测） |
| 一手·论文/预印本 | 学术来源，须附版本与同行评议状态 |
| 一手·平台数据 | 可复现抓取的接口数据（npm / GitHub / arXiv abs） |
| 二手·转述 | 我们没读到原文，靠他人转述 |
| 二手·社区/展示站 | 聚合站、展示站，非当事人也非媒体 |
| 二手·媒体/专栏 | 须标是否独立核实 |
| 本文推演 | 无公开实现证据 |

轴 2 括注只用这几个用语：可复现抓取 / 平台托管 / 页体受保护 / 内部遥测不可复算 / 无审计 / 利益相关。

| # | 标题 | URL | 类型 | 一句话摘要 |
|---|---|---|---|---|
| 1 | Document Review With Unsiloed and TypeSafe Jev | https://www.unsiloed.ai/blog/document-review-unsiloed-typesafe-jev | **一手·客户自有文档**（可复现抓取；厂商是 TypeSafe，Unsiloed 是客户） | 双模型互查完整实现：分工、完整请求/响应 JSON、阈值、$0.000076/文档、咖啡渍与布洛芬两向漏检 |
| 2 | Calibrated Decisions at Scale: Converting Police Crash Narratives into Probabilistic Crash Variables with a System One Model (Jev)（arXiv:2609.24052） | https://arxiv.org/html/2609.24052v1 | **一手·论文/预印本**（v1，2026-09-21，未见同行评议） | 500 万条语料、19.6 万条实测编码，27 问 schema，F1 0.908，$0.1543/千条，$55.79 总花费（分项和 $55.48 + 非独立支出差项 $0.31），**0 次失败调用**（调用层口径，非编码零错误；见正文） |
| 3 | Jev is the fastest-adopted model in AI Gateway history | https://vercel.com/blog/ai-gateway-jev-model-launch | **一手·厂商自述**（内部遥测不可复算；非 Jev 厂商） | 24h 内近 13% 付费团队采用，2× GPT-5.6 家族、>6× Fable 5.1（三者同平台、同分母、同 24h 窗）；仅平台方可复核 |
| 4 | TypeSafe A raises Series AI | https://typesafe.ai/blog/series-ai | **一手·厂商自述**（利益相关） | 「1/3 财富 500 强在用」「已省下数百万美元」，无名单无 case study |
| 5 | Jev on Product Hunt（产品页 + 评价卡） | https://www.producthunt.com/products/jev | **一手·客户自述**（平台托管；引句取自本次抓取的 2026-10-21 快照，可复核） | gg-friggin-ez（Shikhar Srivastava）、Fit Receipt（Crystal Chang）的用法原文——本章唯二可回溯到具体载体的客户引文；亦收录日本招聘平台帖（见 #13） |
| 6 | Jev Customers（Product Hunt） | https://www.producthunt.com/products/jev/customers | **二手·转述**（页体受保护，本次未直接抓取） | 9 家实名客户清单来源；**计数按转述处理**，用法另有客户自有文档与客户自述交叉核对 |
| 7 | Famulor Changelog（2026-09-22） | https://docs.famulor.io/changelog | **一手·客户自有文档**（可复现抓取） | Jev 驱动消息咨询标签，官方自陈「advisory and can be wrong」 |
| 8 | WikiFix for Confluence — Atlassian Marketplace | https://marketplace.atlassian.com/apps/2836392116/wikifix-for-confluence | **一手·厂商自述**（平台托管） | 产品定位核实：扫描矛盾/过期/无主页面并写修复 |
| 9 | WikiFix — Products used（Product Hunt） | https://www.producthunt.com/products/wikifix/built-with | **二手·转述**（页体受保护，本次未能直接读取；本次抓取的 PH 产品页快照中检索 WikiFix / 415 / 13k / Sonnet 均 0 命中） | 据转述：三次 Sonnet 投票 → 一次 Jev；415 页 13k→5k credits（**未直接复核，不计入成本型证据**；credits 非美元，换算比未公开） |
| 10 | eu/jev — First System One Model Hosted in the EU | https://eu-jev.com/ | **一手·厂商自述**（利益相关；竞品） | Bevel 出品；德国 Hetzner 推理、不留存 prompt；Jev-style API，模型 ID `eu-jeff-latest`；€37/Btok，自称「同价」 |
| 11 | Ana — vertice.one | https://www.vertice.one/ana | **一手·客户自有文档**（客户官网产品定位；可复现抓取） | 软件采购谈判 agent，自称 4,000+ 场谈判、5 亿美元 spend |
| 12 | Lurk · Jevfast | https://jevfast.com/lurk/ | **二手·社区/展示站**（未独立核实） | 免费 Reddit 监控，Jev 机制未披露，无付费主体（→第 5 章） |
| 13 | Where I put Jev in production on a large site, and where I didn't（Product Hunt 论坛帖，作者 Hisashi Space，2026-09-30） | https://www.producthunt.com/p/jev/where-i-put-jev-in-production-on-a-large-site-and-where-i-didn-t | **一手·客户自述**（平台托管；无审计；非 9 家名单成员） | 日本招聘平台生产约 10 天：996 家流水线判定 571 家、抽检 50 家 0 错；抽样未公开 |
