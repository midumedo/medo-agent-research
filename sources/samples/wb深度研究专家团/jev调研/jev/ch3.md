# 第 3 章 选型地图：34 个竞品、`/v1/systemone` 契约标准化与厂商锁定风险

> 数据采集日期：2026-10-31。价格、延迟、上下文随版本变动，引用请复核。

## 论点：你要决策的不是"选哪一家"

Jev 发布后 24 天内，**至少四家、至多六家**大厂相继推出同类产品（口径见第一节），开源自托管模型从 1 个增至 12 个（口径见第二节）。面对这个格局，架构决策者最容易犯的错误是把问题设成"Jev、Clef、Decision-1 该选哪个"——但本章的结论是：**真正的决策对象是"要不要采纳 decision model 这个品类"，以及"抽象层切在哪一层"。** 因为 `POST /v1/systemone` 的 `state` + typed questions 结构，已经在事实上成为这个品类的标准契约；换底座在多数情况下只改 base URL。

### 路线 0：不引入 decision model（对照组）

在讨论"选哪一家"之前，必须先有"一家都不选"这一项，否则全章会滑回厂商比较。**默认选项是 LLM + structured output**（提示模型输出 JSON，再由代码解析）。用本章判据检验——**它是否输出"预声明答案空间上的校准概率"**——答案是**否**：LLM 生成的是 token 序列，结构由解析器事后约束，概率不在答案空间上定义，且 schema 合规与语义正确是两件事。

**所以它不属本品类，但它是本品类存在的理由**：这条路线的问题（解析脆弱、无可用置信度、成本与延迟高）正是 decision model 要解决的。**它的适用条件、失效边界与详细对比见第 1 章 §4，本章不重复论证**——本章只需记住一点：**路线 0 永远可用，所以任何 decision model 的采纳都必须证明自己比"什么都不换"更好，而不只是比别家模型更好。**

## 一、24 天：大厂陆续下场的时间线

TypeSafe AI 于 2026-09-15 发布 Jev（$0.042/Mtok 输入、输出 token 免费），并在 2026-10-14 迭代到 1.14（[官方 Models 页](https://docs.typesafe.ai/models)）。

**本节计数口径**：「24 天」= 2026-09-15（Jev 发布）至 10-09，共 24 日。「大厂」指 OpenAI、Microsoft、Cloudflare、Perplexity、Liquid AI、Together AI 六家，**不含 TypeSafe 自身**。其中 Cloudflare（10-01）、OpenAI（09-29 预告）、Liquid AI（09-29 托管）、Microsoft（10-09）**四家日期可核实**；Perplexity 与 Together AI 的日期〔待补〕。**故本节结论应读作「至少四家可核实、至多六家」，而非「六家全部可核实」。**

此后 24 天内：

**表 1 · 七家厂商决策模型产品对照（含 TypeSafe 自身；六家挑战者中四家日期可核实）**

本表只列**产品身份**（谁、何时、什么底座、什么许可、是否兼容契约）；**价格、延迟、上下文、模态、辖区等采购维度统一见第五节表 2**，两表不重复列同一指标。

| 厂商 | 产品家族 | 首发 | 底座 | 许可 | 兼容 Jev API |
|---|---|---|---|---|---|
| TypeSafe AI | Jev 1.13 → 1.14 | 09-15、10-14 | 未公开 | 闭源托管 | 基准 |
| Together AI | Tev1-4B-experimental | 〔待补：09-23 未核实〕 | Qwen3.5-4B 微调 | 〔待补：未核实〕 | 〔待补：疑仅 Choice〕 |
| Liquid AI | d1 / d1-ultra / d1-3B / d1-omni-600M | 09-29 托管；10-07/08 开源 | 自研 LFM | LFM Open License〔待补：条款未核〕 | 〔待补〕 |
| OpenAI | Decisions API | 09-29 预告、10-06 公测 | GPT-6 Luna | 闭源 | **否**（Predicate/Choice/Score） |
| Cloudflare | Clef / Clef-flash / Clef-omni / Clairic | 10-01、10-09、10-19 | Qwen3.8-27B / Qwen3.5-9B / 30B-MoE(A3B) | **Apache-2.0** | **是（"fully Jev-API compatible"）** |
| Microsoft | Microsoft-Decision-1 | 〔待补：10-09 仅二手〕 | Qwen3.5-9B 后训练〔待补〕 | 闭源 | 否 |
| Perplexity | pplx-decider v1.2-27b / flash | 〔待补：10 月初，日期未定〕 | Qwen3.8-27B / 4B | Apache-2.0 | 〔待补〕 |

来源：[systemonemodels.org/models](https://systemonemodels.org/models/)、[Cloudflare 官方博客](https://blog.cloudflare.com/clef-decision-models/)、[The New Stack](https://thenewstack.io/openai-decision-api-luna/)。

**来源强度说明**：本表凡未标"官方称"的数字，均为索引站或二手口径。Microsoft-Decision-1 的发布日与底座**未能取得微软一手公告**——已检索微软 Foundry 官方博客、Azure 博客与 Learn 文档，均未见对应文章。OpenAI Decisions API 的 $0.10 亦来自索引站，其**单价、单请求候选答案上限、能否用自有数据调优三项官方均未披露**。

三点值得单列。**第一**，OpenAI 在 DevDay 前一天（09-29）抢发，The New Stack 直接写 "likely a reaction to TypeSafe and Jev"——这是"决策模型"作为独立品类被最大玩家承认的时刻。但请注意上表三个"未披露"：**一个契约要成为标准，不能只标准化请求形状，还要标准化"能力边界是否可声明"**。**第二**，Cloudflare 把 Jev 放上 10 项 benchmark 逐项对照，并写明 "our model has a 64k context window (compared to Jev's 32k)"——**上下文长度是 Jev 当前的结构性短板**。**第三**，若二手口径的 10-09 成立，微软的发布时点紧接 TypeSafe 融资公告（同为 10-09）之后，二者同日、先后顺序据二手转述——**微软一手公告未取得，故此条不作「24 天内跟进」的论据**。可独立成立的是底座：据二手口径为阿里 Qwen3.5-9B 后训练，**若成立，则说明这个品类的进入门槛已降到"买底座 + 后训练"**。

## 二、34 个模型与开源成熟度的光谱

**本节计数口径**：systemonemodels.org 当前页面**逐条清点为 34 个条目 = 商业托管 21 + 开源自托管 12 + 提取 1**（逐条名单见文末附录，可自行反算）。**含**已弃用的 Von（计入开源 12 之中）、**含**同时上 OpenRouter 的 Kev；**不含**社区展示站、单篇博客与未上架的项目。站点 FAQ 自述"29 of the 33 models here"，**与逐条清点差 1，差异未解，本文不采用该数**，只采用可逐条反算的 34。
另有 10-22 的二手盘点记录为"27 个决策模型 + 1 个提取模型"（二手转述，未复核），若该口径成立，则 9 天内净增 6 个——**这个增长率本身就是选型地图最重要的信息：你写的适配器在明年会面对更多后端，而不是更少。**

光谱两端：

- **成熟端：Laya**（Convai Innovations，2026-09-18 创建，Apache-2.0）。**GitHub star 34,729（截至 2026-10-31）**；一周内被第三方移植到 **Core ML / MLX / GGUF / ONNX / LiteRT 五个运行时**（[架构说明](https://systemonemodels.ai/blog/laya-architecture-explained)）；`laya-serve` 暴露 `POST /v1/systemone`，"existing Jev clients only need a new baseUrl"（[评测](https://andrew.ooo/posts/laya-review-open-weight-jev-alternative-system-1-decision-model)）。**但它的成熟度恰好也标出了这个品类的真实门槛**——模型卡原文：*"Laya is a fast base to specialise, not a zero-shot decision engine."*（[模型卡](https://huggingface.co/convaiinnovations/laya)）
  - 〔星数口径注〕上数为 GitHub star，非 HuggingFace likes、非下载量。**同一来源内部存在两个口径**：TL;DR 段与 Quick Reference 表记 **23,805 star / 2,045 fork（截至 2026-09-25）**，而 "Repository facts, checked Oct 31, 2026" 区块记 **34,729 star（+503/7 天）**。本章取 10-31 口径；若需与 9 月数据并列，请注明两个日期。
- **淘汰端：Von**（wfzyx，395M ModernBERT，Apache-2.0）。README 顶部已挂归档通知："Von is no longer maintained… For new projects, use LiquidAI/d1-omni-600M"，最后一次提交 2026-10-19 就是加这条通知（[wfzyx/von](https://github.com/wfzyx/von)）。它曾是 byte-compatible 的 `/v1/systemone` drop-in 服务。

中间还有 APUS-OpenJev-v1、Kev、CLM、H2O-Lightning、OpenThai-SystemOne 等。其中 APUS-OpenJev-v1 据二手转述提供 4B/9B/35B-A3B 三档权重（Apache-2.0）与 MIT 工具链，**未取得一手仓库或模型卡核实，故正文不引用其任何性能数字**。

**一个必要的口径澄清**：本节"34 个模型"是**品类规模**的分母，不是"Jev 可替换集合"的分母。34 个条目里 12 个是开源自托管——它们天然可微调、可换权重、可自部署，这与托管 Jev 的硬约束（不改权重、全账户共享、仅文本、无自托管）不是同一回事。**把两个分母混用会推出错误结论**：看到 12 个可微调的开源实现，就以为"微调需求已有着落"，实际上你换掉的是**整个托管形态**，而不只是换一个供应商。对架构决策者的含义是：**"要不要自托管"是独立于"选哪家"的前置决策，它比供应商选择更早、也更难回退。**

**核心判断：「有开源实现」不等于「可生产替换」。** 五条区分标准：(1) 是否持续维护（Von 反例）；(2) 是否实现完整三原语——只实现 Choice 的实现即功能子集（**本章未逐一核实各家原语覆盖，此条为判据，非对各家的结论**）；(3) 是否有可复现评测；(4) 概率是否校准；(5) 是否有社区。

第 4 条最易忽略，且这里有一个指标陷阱值得单独说明。Laya 自测的校准数据是：**mean ECE 0.466（开箱）→ 0.081（按 question type × 选项数重拟合温度后）**。需强调，**这个 ECE 与第 2 章引用的 Jev 声明核验 ECE 0.011 不可直接比较**——数据集、题目类型与统计口径都不同；量级差异本身就说明"ECE"高度依赖评测集，跨报告引用会失真。至于常被引用的 Banking77 数字（Laya 0.425 对 Jev 0.870），**原文未标注指标名称**，从上下文看是分类得分（最可能为准确率）而非校准误差，且两侧标签集不同（Jev 72 类 vs Laya 77 类），原文将差距归因于"选项共享一个很小的 token 预算"。**它不是 ECE，不能放进校准语境**——读者若把它当成校准指标，会得出"Jev 校准极差"的完全错误结论。

至于"可生产替换"的真正门槛，最硬的证据来自模型卡自己的数字。typed-decisions 基准（2,000 个判断、四个工作流）上：基座英文 checkpoint **0.362**、基座多语 checkpoint **0.342**、**随机基线 0.318**、**多数类基线 0.461**、微调专用 checkpoint **0.766**。关键不是"接近随机"，而是**基座检查点低于多数类基线**——模型卡原文："The base checkpoints sit below the majority-class baseline here — the capability on this benchmark comes from fine-tuning." 也就是说，**不做微调时，一个只会猜多数类的笨办法比它更准**。同一页还给了教师自一致上限 0.735 与 Jev 公开值 0.727 作参照。

这直接决定选型判断：**开箱即用与可生产之间，隔着一个数据标注项目**（模型卡给的微调成本是 M 系列 Mac 上 15–20 分钟 LoRA）。所以"Apache-2.0 + 421M + 33ms"这组参数的真实含义不是"免费的 Jev"，而是"**一个很便宜的自建起点**"。

### 关于 Cloudflare 对照表中的 Laya

Cloudflare 三个表格中 Laya 列标题均指向 `https://huggingface.co/convaiinnovations/laya`，与 Convai 发布的权重仓库**是同一地址**，故为同一模型。但两处数字不可直接引用：

1. **5.8 ms 中位延迟不可与 Convai 自测对比。** Cloudflare 全文未披露第三方模型的硬件、量化与 batch 设置（唯一的环境说明只解释 Clef 自身的 Workers AI 边缘 GPU 优势）；Convai 自测是 Tesla T4 上的 32.8–39.5 ms。**本文认为这更可能是硬件代差，而非两个模型。**
2. **macro-F1 3.19 不是"专训分类器性能差"的证据，但原因比"标签空间不匹配"更具体。** 模型卡给出确切机制：option-marker 打分器让**所有选项共享一个固定 token 预算**（英文 `head_max_len = 192`、多语 256），77 个选项的 Banking77 上每个标签只剩 `(256 - 16) // 77 ≈ 3–4` 个 token，"causing text to become indistinguishable"，准确率随之塌到 0.425。叠加"基座检查点低于多数类基线"，解释了 Cloudflare 表里全线近随机的形态。

**这个机制对选型者比"性能差"有用得多**：它说明高基数 Choice 是这类小参数编码器的结构性弱点，缓解手段是工程性的——调大 `head_max_len`（至 512/1024/2048/8192），或拆成两级粗到细的层次化 Choice。**这也呼应第四节"原子问题在代码里组合"：不只是为了准确率，也是为了绕开逐选项 token 预算。**

另需注意：Cloudflare 原文**未描述 Laya 的架构与训练方式**，也未使用 zero-shot/few-shot 措辞。故"ModernBERT-large 421M 编码器 + 决策头"须引用 Laya 模型卡，不能挂在 Cloudflare 名下。

## 三、`/v1/systemone`：一个已经标准化的封闭 schema

契约不是自由文本接口，而是一个**封闭的类型化 schema**（[TypeSafe Quickstart](https://docs.typesafe.ai/introduction/quickstart)）：

```bash
POST https://api.typesafe.ai/v1/systemone
Authorization: Bearer $TYPESAFE_API_KEY
{
  "state": "客户工单原文…",
  "model": "jev-latest",
  "questions": {
    "department": {"type":"choice","instructions":"哪个团队处理",
                   "criteria":{"billing":"付款问题","technical":"技术问题"}},
    "frustration": {"type":"score","instructions":"愤怒程度",
                    "criteria":["平静","不满","愤怒"]},
    "is_urgent":  {"type":"noul","instructions":"是否紧急"}
  }
}
```

响应按同一批 question id 回填：`choice` → 选中项 + `probabilities` + `confidence`；`score` → 档位期望值 + `legend` + `probabilities` + `confidence`；`noul` → 单个 0–1 概率（**不返回 confidence**）；另有 `usage`。注意 `questions` 是**以 id 为键的对象，不是数组**——这既让它可被静态类型化，也让它容易被标准化。

标准化已有硬证据，但**必须按可核范围计数**：**大厂中目前只有 Cloudflare 一家**明确宣称 "fully Jev-API compatible… you can make the swap extremely easily"（[Cloudflare 博客](https://blog.cloudflare.com/clef-decision-models/)）；**另有一家小型竞品**（Bevel 的 `eu/jev`）同样实现了 `POST /v1/systemone` + 三原语 + Bearer 鉴权（[eu-jev.com](https://eu-jev.com)）；**开源侧可核的是 4 个**——Laya（`laya-serve` 暴露同一端点，只需改 base URL）、Von（宣称 byte-compatible，已归档）、Kev、CLM，四者均有各自仓库或文档明确写出实现 `/v1/systemone`。另有 APUS-OpenJev-v1 据二手转述实现同一契约，**未获一手核实，且不在下节 12 个开源模型之列**。

**这里有一个必须说清的计数陷阱**：第二节的"12"是**开源自托管模型的总数**，不是"12 个都兼容"——**已核实兼容的是 4 个**。两者是不同的集合，不能互相顶替。

**其余大厂多为部分兼容或未公开**：OpenAI 用 Predicate/Choice/Score 而非三原语；Microsoft、Perplexity、Liquid AI 的兼容性〔待补〕；Together 疑似仅支持 Choice。**本文不把"兼容"扩写成"对齐"**——「实现同一契约」与「可零成本替换」是两个不同强度的判断，前者有证据，后者只对 Cloudflare、Laya、Von、eu/jev 四例成立。

**所以准确的说法是：一个接口在 6 周内被 1 家大厂 + 1 家小型竞品 + 4 个可核的开源项目实现（另有 1 个开源项目为二手口径）。** 这个数字比"3 家大厂 + 12 个开源"小得多，但它是可逐一点名的；而它已经足以支撑本章的结论——**契约成为标准的标志不是"多少大厂宣称兼容"，而是"改 base URL 就能换供应商"这件事已经有人做到。**

**这个扩散速度是可解释的**：`/v1/systemone` 是封闭 schema——无自由文本、无流式、无 tool-call、无多轮状态，只有 `state` + 固定三原语的 typed questions，适配成本极低。**本文认为，正因为它的表达能力被刻意收窄，它才容易被标准化**；这也意味着凡需要多轮推理或自由输出的场景，它天然不适用（与第 1 章的品类边界一致）。

## 四、抽象层建议与三道缝隙

**建议：可以且应当按契约做抽象层**——一个 `DecisionModel` interface（`evaluate(state, questions) → answers`）+ 多 provider 适配器。迁移成本近似一次配置变更，锁定风险显著低于常规模型采购。

但有三道缝隙必须提前设计：

**1. OpenAI 兼容端点不支持评估调用。** Vercel 原文："AI Gateway exposes evaluation through the AI SDK, rather than its compatibility endpoints… OpenAI-compatible endpoints don't support Jev evaluation"（[Vercel KB](https://vercel.com/kb/guide/typesafe-jev-and-ai-sdk)）。抽象层**不能**只做 OpenAI-compatible shim。

**2. 同一原语有三个名字。** TypeSafe 叫 `noul`，OpenAI 叫 `Predicate`，Vercel evaluation API 映射为 `boolean`/`probability`。映射错了不会报错，只会静默返回错误语义。

**3. `confidence`、`score` 与"版本"三重语义漂移。**
- 官方示例中 `frustration` 返回 `score: 0.67` 而 `confidence: 0.5`——`score` 是档位上的**概率加权期望**，不是 argmax；`confidence` 是分布集中度（0 = 均匀，1 = 全集中），不是"选中项概率"。
- Vercel 注明概率四舍五入到两位小数（分布可能合计 0.99），且 `probabilities` 在各 provider 中是**可选字段**，必须防御性读取。
- 社区实现更细：Laya 的移植版 README 明确写 "Answer semantics follow rl_agent_api.py, not kev's door"，采用**四位小数 ties-to-even**——与 Jev 的两位小数不同。
- **最强的一条来自厂商自己的文档**：alias `jev-latest` 随版本移动，"its answers can change without any change to your code… If you have tuned confidence thresholds against one version, send that version's ID instead of the alias"（[Models 页](https://docs.typesafe.ai/models)）。而 Jev 从 1.13 到 1.14 只用了 **29 天**。**这意味着即使你只用一个供应商、一行代码不改，阈值也会失效。**

**所以本章的核心结论是：抽象层要防的是「语义漂移」，不是「接口变更」。** 接口变更立刻抛错，好处理；语义漂移会安静地让你的阈值失效。防御手段：把"契约测试"写进 CI——固定一组 (state, questions) 黄金样本，对每个 provider 断言字段存在性、概率归一性、`score` 与 `probabilities` 的一致性、`confidence` 单调性；**并且锁定版本化 model ID 而非 alias**。

## 五、横向选型矩阵

**表 2 · 选型维度矩阵**（采集 2026-10-31；本表承担全部采购维度，与表 1 无重复列）

| 维度 | Jev | Clef 家族 | Decision-1 | Decisions API | d1 家族 | pplx-decider |
|---|---|---|---|---|---|---|
| 单价（$/Mtok 输入） | 0.042 | 0.15–0.24 | 0.042 | 0.10〔索引站〕 | 0.02–0.042 | 0.01–0.02 |
| 延迟 p50（ms） | 官方 70–500 / CF 实测 524.1 / 第三方 236–276 | 38.8–209.3 | 85–125 | 150 | 最低 8 | **无一手数据，不参与比较** |
| 上下文 | 64k/请求 · 32k/问题 · 262k 长上下文 | 64k / 24.5k | 〔待补〕 | 未披露 | 〔待补〕 | 〔待补〕 |
| 模态 | 仅文本 | 文 + 图 + 音视频 | 仅文本 | 文 + 图 | 文 + 图 + 音视频 | 仅文本 |
| 许可 | 闭源 | **Apache-2.0** | 闭源 | 闭源 | LFM Open License〔条款待补〕 | Apache-2.0 |
| 自托管 | 否 | 是 | 否 | 否 | 是 | 是 |
| 可微调 | **否**（全账户共享权重） | 是（开源权重） | 〔待补〕 | 未披露 | 是 | 是 |
| 兼容 Jev API | 基准 | **是** | 否 | 否 | 〔待补〕 | 〔待补〕 |
| 企业级承诺 | ZDR / No-Training / 1/3 Fortune 500 | Cloudflare 生态 | Foundry + OpenRouter | Azure 生态 | 边缘部署 | — |
| **辖区（数据处理地点）** | 美国〔据总部所在地推定，**未见官方数据处理地点声明**〕 | 未明示 | 未明示 | 未明示 | 未明示 | 未明示 |

**关于「辖区」这一行的限定**（单独列出，不与"企业级承诺"混读）：本行记录的是**数据处理地点与厂商自述的驻留安排**，属**事实层**描述，**不是合规认证**。数据在某一司法辖区内处理，不等于该服务满足该辖区的全部法律义务（例如 GDPR 下自动化决策的告知与异议权）；本章不替任何供应商把"驻留"升格为"合规"，也不做法律判断。

**读法**：**只按单价**选，pplx-decider 最低（$0.01–0.02）；**按"单价 × 延迟"选，只有 d1 两项都有数**——pplx-decider 的延迟在任何一手源里都没有，**不参与这项比较，也不能被写成"最快的之一"**。按"许可 + 可自托管 + 可微调 + 兼容契约"选，Clef 家族与 Laya 是唯一四项全中的组合。

**关于 Jev 的延迟区间**：70–500 ms 应读作「**下限占优、上限最宽**」——最快时它与表中最快者处于同一量级，最慢时它是表中上限最高的一家。这是**区间宽度**问题，不是"最慢"。把它读成"Jev 最慢"，与把它读成"Jev 最快"，同样不准确。

Jev 的位置需要说准：**它在每一项上都不是最优，但也不是最差**。单价 $0.042 **低于** OpenAI Decisions API（$0.10，**索引站口径，官方未披露定价，故此项为指示性对比**）与 Clef（$0.15–0.24），**高于** pplx-decider（$0.01–0.02）与 d1（$0.02–0.042），落在中位；延迟与上下文同样处于中位区间；**模态（仅文本）是唯一明确的短板**——Clef 带视觉编码器、d1-omni 与 Clef-omni 支持音视频，Jev 官方明确"does not accept audio or video"。

所以它的差异化不在任何单项指标，而在**生态深度**（Vercel AI Gateway 上线 24 小时内近 13% 付费团队采用，网关史上最快，[Vercel 博客](https://vercel.com/blog/ai-gateway-jev-model-launch)）与**企业级承诺**（ZDR、No Training、约三分之一《财富》500 强接入）。对选型者的实际含义是：**如果你只需要一个"够快、够便宜、文本、托管"的默认选项，Jev 是合理的；如果你的场景有图像、音视频、超长上下文、或必须自托管/可微调，它就不是候选，而不是"差一点的候选"。**

注意"可微调 = 否"这一行的战略含义：**Jev 用"不改权重、只改请求"换取全账户一致的校准，代价是无法为你的域做适配**。当标签空间偏离其训练分布时，唯一出路是拆原子问题 + 在代码里组合——这不是缺陷，但它把"模型选型"变成了"提示工程选型"。

## 六、邻近范式的边界

品类边界模糊时采购清单会被灌水。**唯一判断标准**：该模型是否输出"**在调用方预先声明的答案空间上的校准概率**"。

- **reward model / guardrail**——答案空间由模型方预设，**不是竞品**。边界个案：Respan Span-01/02 因实现了 Choice/Noul/Score 而被索引站收录。
- **router 模型**——答案空间可声明，**功能上是竞品子集**；awesome-jev 中 20+ 个 router 项目说明这是最高频用例。
- **embedding + head**（GLiNER2.5-Decide，340M 编码器，Apache-2.0）——架构同源，但训练目标是抽取而非校准决策，**近亲不是同类**。
- **「System One」概念溢出**——部分项目借用该术语做 computer use 等任务（如 CUA-S1），输出空间与校准目标不同，属**概念邻居**。〔待补：此类项目的完整清单未逐一核实〕

## 七、供应商可持续性与竞争结构

可核验事实：种子轮 $40M @ $2 亿（09-15，二手媒体口径）；A 轮 **$870M @ $75 亿**，a16z 领投，红杉、DCVC 跟投，Martin Casado 入董事会（10-09，[官方博客](https://typesafe.ai/blog/series-ai)）。同期竞争事实：Convai 在 Jev 发布后 3 天（09-18）推出 Apache-2.0 的 Laya。

**竞争结构判断**：多家大厂在 24 天内下场（口径见第一节）+ 12 个开源自托管模型（口径见第二节；**其中 4 个已核实实现同一契约**），说明**护城河在品牌与生态，不在技术**——底座可以买，配方可以复现。「完全兼容 Jev API」因此是双刃剑：既是标准制定者的分发优势，也是**被零成本替换的风险敞口**。

**辖区是一条不依赖模型质量的差异化轴。** Bevel 的 `eu/jev` 宣称数据在德国处理且不存储，请求直达德国服务器、不经代理或 CDN，并复刻 `/v1/systemone` 契约，模型名仿作 `eu-jeff-latest`（[eu-jev.com](https://eu-jev.com)）。**这意味着美国闭源厂商无法靠"发个更强的模型"回应数据驻留要求；对选型者而言，这一维往往比其他维度更早触发否决。**

**"Jev 先发优势可持续性"评估框架**（框架，不给结论），五个可观测变量：

1. **权重是否开放**——闭源保留议价权，但放弃生态扩散与域适配。
2. **是否有独占能力**——当前在模态（仅文本）与上下文（32k/问题）上落后；长上下文 262k 的 danger-zone 头是差异化的一半。
3. **生态绑定深度**——SDK、Agent Skill、Gateway 集成、awesome-jev **GitHub star 2.5k / 374 fork**（非 HF likes 或下载量）。
4. **企业级功能**——ZDR、No Training、SLA、私有部署，这是开源复现最难对齐的一层。
5. **接口契约兼容是否构成真实护城河**——`eu/jev` 这类供应商兼容的是 `/v1/systemone` 接口而非模型本体。**接口兼容降低迁移成本，因此它既是替代威胁，也说明这条赛道的进入壁垒主要在模型质量之外。**

## 小结与可行动建议

**现在就把 decision model 抽象成一个 interface（`evaluate(state, questions) → {answers, confidence, probabilities}`），后端做成可插拔适配器；同时把"契约测试"作为一等公民写进 CI，并在配置里锁定版本化 model ID 而非 alias——因为你真正要防的不是接口被改，而是同一个字段名（以及同一个 alias）在不同厂商、不同版本那里意味着不同的东西。** 这样无论 12 个月后是 Jev、Clef 还是一家尚未出现的厂商胜出，你的迁移成本都是一次配置变更，而不是一次重构。

---

## 附录：34 个模型清单（供反算，不含属性）

**商业托管（21）**：elephant-1（Baseten）· mammoth-1（Baseten）· d1-ultra（Liquid AI）· Span-02（Respan）· SubQ Snap（Subquadratic）· Clef-omni（Cloudflare）· Microsoft-Decision-1（Microsoft）· Celeris-1 Decision（Celeris）· Clef / Clef-flash（Cloudflare）· pplx-decider（Perplexity）· GLiDE（Fastino Labs）· Mercury Decide（Inception）· d1（Liquid AI）· OpenAI Decisions API（OpenAI）· Kai（Hanzo AI）· Drex（Nace.AI）· Span-01（Respan）· Tev1（Together AI）· Decider 1（meraGPT）· Solar Decide（Upstage）· Jev（TypeSafe AI）

**开源自托管（12）**：H2O-Lightning-31B · Jeffan-31b-1710 · Quyet-1.0-Large · Torchcast Decision 27B · H2O-Lightning-4B · Strands-Decider 2B · GLiNER2.5-Decide · **CLM（CLM-8B）✔** · Surogate Rune 26B-A4B · **Laya ✔** · **Von（已弃用）✔** · **Kev ✔**（0.8B/4B/9B/27B，亦上 OpenRouter）

**提取模型（1）**：Clairic（Cloudflare）

合计 **21 + 12 + 1 = 34**。本清单只列名称与归属，不列属性，用途是让读者能自行清点核对；属性见 [systemonemodels.org/models](https://systemonemodels.org/models/)。**站点 FAQ 自述的"33"未采用，差异未解**（见第二节口径说明）。

**✔ = 有各自仓库或文档明确写出实现 `/v1/systemone`，共 4 个**（CLM、Laya、Von、Kev）。**其余 8 个开源模型未见兼容性声明，不等于"不兼容"，只等于"未核实"。** 另：第三节提到的 APUS-OpenJev-v1 **不在本 12 个之列**，其兼容性为二手口径。

> **两个数字不要混用**：**12** = 开源自托管模型总数；**4** = 已核实实现同一契约的开源项目数。凡引用"12"，指的是前者。

---

## 本章来源清单

| # | 标题 | URL | 类型 | 一句话摘要 |
|---|---|---|---|---|
| 1 | TypeSafe Models 页 | https://docs.typesafe.ai/models | 厂商一手文档 | 64k/请求 · 32k/问题、262k danger-zone 头、Jev 1.14（10-14）、alias 漂移警告、不可微调、仅文本 |
| 2 | TypeSafe Quickstart | https://docs.typesafe.ai/introduction/quickstart | 厂商一手文档 | `/v1/systemone` 完整请求/响应 schema 与 curl 示例 |
| 3 | TypeSafe Introduction | https://docs.typesafe.ai/ | 厂商一手文档 | 三原语定义（Choice/Score/Noul）与返回字段 |
| 4 | TypeSafe State 概念页 | https://docs.typesafe.ai/concepts/state | 厂商一手文档 | state 可为 string/object/array；不支持音视频；CJK 准确率较低 |
| 5 | TypeSafe 发布博客 | https://typesafe.ai/blog/introducing-system-one-models-and-jev | 厂商一手 | "Jev supports a cardinality up to 255"、高基数走两阶段且"occasional slowdown"、用例表含 "smart if-statements" |
| 6 | TypeSafe Series A | https://typesafe.ai/blog/series-ai | 厂商一手 | $870M @ $75 亿，a16z 领投，Casado 入董事会 |
| 7 | Laya 模型卡 | https://huggingface.co/convaiinnovations/laya | 厂商一手（模型卡） | "fast base to specialise, not a zero-shot decision engine"；基座 0.362 < 多数类基线 0.461；Jev p50 236–276 ms、Laya 快 6–8×（**Laya 侧 T4 实测，Jev 侧硬件未披露、模型卡自陈"never measured here"**）；`head_max_len` 192/256；Banking77 逐选项 3–4 token |
| 8 | Cloudflare: Clef decision models | https://blog.cloudflare.com/clef-decision-models/ | 大厂一手 | "fully Jev-API compatible"、64k vs Jev 32k、10 项对照表、Jev 524.1 ms、Laya 5.8 ms |
| 9 | Vercel KB: Jev and AI SDK | https://vercel.com/kb/guide/typesafe-jev-and-ai-sdk | 平台一手文档 | "OpenAI-compatible endpoints don't support Jev evaluation"、两位小数、255 选项 / 2–10 档、`probabilities` 可选 |
| 10 | Vercel: Jev fastest-adopted model | https://vercel.com/blog/ai-gateway-jev-model-launch | 平台一手 | 24h 内近 13% 付费团队，网关史上最快 |
| 11 | The New Stack: OpenAI Decision API | https://thenewstack.io/openai-decision-api-luna/ | 主流媒体 | 09-29 抢发、"likely a reaction to TypeSafe and Jev"、价格/候选上限/可调优三项未披露 |
| 12 | System One Models 索引 | https://systemonemodels.org/models/ | 社区索引 | 逐条 34 条目（21/12/1），FAQ 自述"29 of the 33" |
| 13 | wfzyx/von（已归档） | https://github.com/wfzyx/von | 开源仓库 | 395M ModernBERT，byte-compatible，10-19 归档并指向 d1-omni-600M |
| 14 | Laya 评测（andrew.ooo） | https://andrew.ooo/posts/laya-review-open-weight-jev-alternative-system-1-decision-model | 技术博客 | **GitHub star 34,729（10-31）/ 23,805（09-25）两口径并存**、2,045 fork、改 baseUrl 即迁移、Banking77 行未标指标名 |
| 15 | Laya 架构说明 | https://systemonemodels.ai/blog/laya-architecture-explained | 社区技术站 | 三 checkpoint、ECE 0.466→0.081、"within a week it had been ported to Core ML, MLX, GGUF, ONNX and LiteRT"（五运行时的唯一出处）、LoRA 微调 15–20 分钟 |
| 16 | OpenAgents Laya 移植 README | https://github.com/OpenAgentsInc/openagents/blob/main/docs/laya/README.md | 开源仓库 | "Answer semantics follow rl_agent_api.py, not kev's door"、四位小数 ties-to-even |
| 17 | awesome-jev | https://github.com/yibie/awesome-jev | 社区索引 | 2.5k 星 / 374 fork / 917 commits，20+ router 项目 |
| 18 | 36氪/量子位 | https://m.36kr.com/p/4019764837748872 | 二手媒体（中文） | 种子 $40M/$2 亿、24 天时间线、微软两小时后跟进 |
| 19 | 微软 Foundry 官方博客 | https://devblogs.microsoft.com/foundry/ | 大厂一手（**反向证据**） | 已检索首页全部文章，**未见 Decision-1 公告**，用于支撑"待一手核实" |
| 20 | AbdelStark/jev-benchmarks；nibzard/decision-model-benchmark | https://github.com/AbdelStark/jev-benchmarks | 第三方基准仓库 | 独立于 TypeSafe 的 Jev 测量；被 Laya 模型卡引为 236–276 ms p50 出处（未逐项复核） |
| 21 | eu/jev（Bevel） | https://eu-jev.com/ | 竞品官网（一手） | 德国 Hetzner 托管、数据不存储；`POST /v1/systemone` 三原语 + Bearer；模型 ID `eu-jeff-latest`（**jeff 非 jev**）；标价 €37/Btok，与 Jev $42 **币种不同、名义低约 12%**；"Same price as Typesafe's Jev" 是**供应商说法，不可写成事实等同** |

**线索（未采信为依据，仅用于确定检索方向）**：百度百科 Microsoft-Decision-1、百度百科 APUS-OpenJev-v1、百度百科 Qwen3.5-9B、百家号 Jev 类模型全景对比。正文事实性陈述均不依赖上述条目。

---

## 仍缺一手来源的论断清单

| 论断 | 位置 | 缺什么 | 处理 |
|---|---|---|---|
| Microsoft-Decision-1 发布日 2026-10-09 | 表 1、第一节 | 微软一手公告（Foundry/Azure/Learn 均已检索未见） | 表 1 标〔待补〕，正文标"二手口径" |
| Microsoft-Decision-1 底座为 Qwen3.5-9B 后训练 | 表 1、第一节 | 微软一手公告 | 表 1 标〔待补〕，正文标"二手口径" |
| Together Tev1 发布日期 09-23 及"仅 Choice"限制 | 表 1 | 一手模型卡/文档 | 表 1 标〔待补〕 |
| Perplexity pplx-decider 确切发布日 | 表 1 | 一手公告 | 标〔待补：10 月初，日期未定〕 |
| LFM Open License 具体条款（含营收门槛） | 表 1、表 2 | 许可原文 | 标〔条款待补〕，正文未引营收门槛 |
| APUS-OpenJev-v1 的规格与许可 | 第二节 | 一手仓库/模型卡 | 正文已降为"据二手转述"，不引用性能数字 |
| OpenAI Decisions API 单价 $0.10 | 表 1、表 2 | 官方定价页 | 标"索引站口径"，正文已说明三项未披露 |
| d1 家族、pplx-decider 是否兼容 `/v1/systemone` | 表 1、表 2 | 各家文档 | 标〔待补〕，未断言 |
| 「System One」概念溢出项目的完整清单 | 第六节 | 系统检索 | 标〔待补〕，仅举例未穷举 |
| 两个第三方基准仓库的具体方法学 | 来源 #20 | 未展开核 | 标注"未逐项复核" |
| Laya 的 GitHub star 数（同一来源两个口径） | 第二节、来源 #14 | 无缺——**但同一来源自相矛盾** | 取 10-31 的 34,729，同处注明 09-25 的 23,805 与两个日期 |
| Jev 的数据处理地点（辖区栏"美国"） | 表 2 | TypeSafe 官方数据处理地点声明（仅有总部所在地的二手信息） | 表 2 标"据总部所在地推定，未见官方声明" |

**〔待补〕标记的连带约束（本章已执行）**：凡正文出现〔待补〕的句子，**该句不得同时承载断言性结论**；凡结论依赖待补数字的，一律降为条件句。本次已连带降级三处：① 第一节「24 天内全部下场」→ 降为「至少四家可核实、至多六家」；② 第一节「微软在两小时后跟进」→ 降为「若二手口径成立，则同日；不作 24 天跟进的论据」；③ 第二节「疑仅 Choice 的实现即功能子集」→ 降为「本章未逐一核实，此条为判据而非结论」。另将第五节「Jev 单价低于 OpenAI」标注为指示性对比（因 OpenAI 定价未官方披露）。

---

## 写作口径备注（供审稿与终校核对）

1. **所有比较句先确认"两个数是不是同一类量"，再谈是否同环境。** 本章已按此规则自查，正文现存三处倍/百分比表述：**OpenAI 称 150 ms 对 1.6 秒约 10 倍**（同模型同厂商同 API 族，唯一 apples-to-apples，已标"OpenAI 称"）、**6–8× 优于 90×**（已注明"仍非严格同环境"、Jev 侧硬件未披露）、**€37 名义低于 $42 约 12%**（已注明币种不同、且"同价"为供应商说法）。**已从正文移除**的表述：「估值 37.5 倍/融资 22 倍」——该倍数的基数是二手媒体口径的种子轮估值，不宜作为可核事实呈现；正文改为直接给两轮绝对值（$40M @ $2 亿 → $870M @ $75 亿）。
2. **凡用"低于多数类基线"否证，必须同句给出随机基线。** 第二节已同句给出 0.318（随机）与 0.461（多数类）。
3. **不使用"Jev 快两个数量级"。** Cloudflare 表中 Laya 5.8 ms 对 Jev 524.1 ms 的比值无意义（两套硬件、第三方测量条件未披露）；可用最强表述是模型卡的 6–8×，且注明 Jev 侧硬件未披露。
4. **Laya 模型卡内部不一致的处理**：正文含**两个不同**的基座数——**英文基座 0.362**、**多语基座 0.342**（两者并列出现，勿混读）。模型卡对**多语**基座给出两个值：typed-decisions 表格记 **0.342**、Honest Limits 正文记 **0.352**。本章只取表格口径的 0.342，**不引用 0.352、不加脚注**（按主理人裁定：保持单一口径与可追溯）。
5. **255 的定性**：厂商自述支持上限 255，但同句自承高基数走"两阶段"且"会偶尔变慢"，且无任何 255 选项上的质量数据。故为"**需要变通才能达到的上限**"，非"可直接依赖的能力"；博客未说明超过 255 时的处理方式，本章不写"255 是硬上限"。
6. **Bevel 的定性**：API 契约层面完全兼容 Jev，产品定位上是替代品而非分销渠道——**兼容的是接口，替代的是供应商**，官网未提任何与 TypeSafe 的授权关系。
7. **「辖区」栏不是合规认证**：仅记录数据处理地点与厂商自述的驻留安排，本章不做法律判断。
8. **计数断言必须带口径，且口径须可反算。** 本章两处计数均已给出口径（第一节「24 天/大厂」、第二节「34 个条目」），并说明含哪些、排除哪些、哪几家日期可核实。**凡给不出口径的计数，一律改用不可反算表述**（如"多家""30 余个"）。
9. **统计量必须带单位与平台。** star / like / 下载量三者含义不同，本章统一写作「GitHub star」并附日期；凡同一来源存在多口径，取最新并同处注明另一口径与日期。
10. **〔待补〕不得与断言共句。** 数字待补则结论一并降为条件句；否则待补标记只保护了数字、没保护推理。
11. **结论句里的数字，必须等于前文点名的个数。** 凡出现"X 个……"而前文只列了 Y 个名字，读者会当场数，数出来是 Y。本章已修三处此类问题：**12 → 4**（把"开源自托管模型总数"误当成"兼容项目数"，两个集合不同）、**3 家大厂 → 1 家**（把"兼容"与"对齐"混用）、**"美国" → 据总部推定**（把推定当声明）。**报数与点名不一致时，先怀疑集合搞错了，再怀疑数字错了。**
