# Claude Code · 上下文经济学：50 倍价差与两处地雷

> 数据来源：官方 pricing / extended-thinking 文档（一手，2026-09-20）。
> cache write 价格官方未在该页列出，本文不涉及。标 [推断] 处为推论。

---

## 一、先纠正一个前提：把 AGENTS.md 当成上下文主体是错的

常见的估算是：system prompt + AGENTS.md + 记忆文件，加起来几千到几万 token，占不了多少。

**估数量级没错，判断谁是主体错了。** 上下文的实际大头是另外两样：

- **工具输出** —— 一次 Read 大文件 thousands token；官方自己举的例子是 10,000 行日志
- **对话历史重放** —— 每轮请求都把完整对话再发一遍，每次工具调用还要带上该批结果

这也解释了上一份拆解里那个观察：官方给的所有减负手段，**绝大部分是对付工具输出和历史重放的**（Hook 在工具结果进入前过滤、Subagent 隔离大输出、code intelligence 减少 Tool Read 次数），对付 AGENTS.md 的只有"保持 200 行以内"这一条。

> 供给端（指令文件）小，但它不是主要矛盾。别把注意力放错了地方。

---

## 二、价格结构：三个数字撑起全部推理

| 模型 | Input | Output | Cache read |
|---|---|---|---|
| Opus 5 | $5 / MTok | $25 | $0.50 |
| Sonnet 5 | $2 / MTok | $10 | $0.20 |
| Haiku 4.5 | $1 / MTok | $5 | $0.10 |

恒定的比例关系：

```
output    = 5   × input
cache读   = 0.1 × input
∴ thinking : cached-input = 50 : 1
```

**直接回答那个问题：思考算钱，按 output 计，单价是 input 的 5 倍，且计入该轮 max_tokens。**

---

## 三、你的结论对，但理由反了

原推理是「输入总共才几万 token，所以比思考划算」。

**真相不是因为它小，是因为它能被缓存。**

同一份 3000 token 的 AGENTS.md，跑一场 50 轮的会话：

| 情形 | 计算 | Sonnet 5 成本 |
|---|---|---|
| 完全不缓存 | 50 轮 × 3000 = 150k input | **$0.30** |
| 命中缓存 | 150k × 0.1 | **$0.03** |

差 **10 倍**。而一次 8000 token 的思考：

```
8000 × $10/MTok = $0.08
```

**一次思考，比一整场会话里那份常驻文件的缓存成本还贵 2.7 倍。**

> 所以正确的表述是：
> **常驻内容贵不贵，取决于它能不能命中缓存，而不是它有多长。**
> 不缓存的话，它是按轮次计息的债；缓存了，它接近免费。

这也顺带解释了为什么上一份拆解里所有的优化手段都指向"保持前缀稳定"——它们守护的其实是同一个东西。

---

## 四、但别滑向另一个极端：不能因此无限加输入

两条反制：

1. **稀释**。官方要求 AGENTS.md ≤ 200 行——如果"越多越好"成立，就不会有这个数字。超过之后代价不是成本，是注意力稀释，且无报错。
2. **思考有时反而更省 whole-path。** 让它多想一点，可能少调五次工具，每次工具结果几千 token，而且那些结果之后每轮都要带着重放。

> 所以真正要比的是**整条路径的总成本**（含 tool call 次数、工具输出大小、后续每轮重放），**不是单价**。

```
路径 A（写清楚入口在哪）：1 次 Read + 短思考
路径 B（自己探索）：      5 次 Read + 长思考，且这 5 次的输出会跟随会话一路重放
```

A 便宜得多——**尽管 AGENTS.md 那段话在每一轮都要付费**。因为它命中缓存后，那份费用近乎为零。

**判据**：写到**边际信息量归零**为止（200 行可理解为官方的经验拐点），而不是写到预算用完为止。

---

## 五、地雷一：Opus 上，思考会被征收两次

官方原文：

> "Claude Opus 4.5 and models numbered 4.6 and higher keep prior turns' thinking blocks in context and **bill them as input**, where Claude Sonnet 4.5, Claude Haiku 4.5, and earlier models stripped them"

翻译：**同一段思考，先按 output 计一次费，之后每轮再按 input 计一次**——因为它留在了上下文里。

连带后果是一条链式反应，这条我认为是今天最值得记住的：

```
Opus 上开满思考
  → thinking blocks 留存在上下文并按 input 反复计费
  → 上下文涨得更快
  → 更早触发 auto-compact
  → 压缩是静默丢失（见《卸荷优先于压缩》）
  → 你为了「想得更周全」付出的代价，包括了「更早忘记之前约定过什么」
```

**追求更强的推理，间接买到了更高的失忆风险。** 这个 trade-off 在任何文档里都没有被提示过。

（另一个隐藏杀手：你的 thinking blocks 若被保留，它们很可能是压缩时被优先牺牲的内容——推理由焉Нет 只能推一次，用完即弃。）

---

## 六、地雷二：思考和缓存是结构性冲突的

官方三条硬约束：

1. **改 `budget_tokens` 会炸掉缓存断点** —— *"because the budget value is rendered into the prompt"*
2. **不能做缓存预热** —— *"extended thinking cannot be combined with `max_tokens: 0`"*
3. 官方建议 —— *"pick a budget and hold it stable for the life of a cached conversation"*

**推论：为了省钱而动态调 thinking 预算，是自相矛盾的做法。**
第一次请求就把前缀炸了，破前缀那一下的损失可能远超你省下的思考费用。

> 这又是一个「看似局部决策、实则全局影响」的现场——thinking budget 写在 prompt 里，于是它成了前缀的一部分。

---

## 七、两家在分歧处暴露了设计取向

同一道题：**怎么才能在对话途中调整推理强度，又不破坏缓存前缀？**

| | Claude | OpenAI |
|---|---|---|
| 思考如何计费 | output 价，计入 max_tokens | output 价 —— *"billed as output tokens"* |
| 是否占上下文 | 占 | 占 —— *"occupy space in the model's context window"* |
| 早期思考进不进下一轮 | Opus 4.5 / 4.6+ **保留并按 input 计费**；Sonnet 4.5 / Haiku 4.5 及更早**剥离** | GPT-5.6 之前**不渲染**；GPT-5.6 **默认渲染**，可用 `reasoning.context` 控制（`current_turn` / `all_turns`） |
| 途中调强度还想保住缓存 | **做不到。** 预算渲染在 prompt 里，改即破前缀 | **有解法**：保留 request-level 的 `reasoning.effort` 不变，改用 conversation-level 的 `configuration_update` —— *"This preserves the original prompt prefix for prompt caching"* |

OpenAI 那条路更宽容，但代价是引入了一整套新概念：`reasoning.context`、`previous_response_id`、`encrypted_content` 回传。**更多旋钮 = 更多可由你搞错的地方。**

**而且两家共同踩了一脚**：OpenAI 明确写着 *"Do not combine configuration updates with automatic compaction or automatic truncation"*，`/responses/compact` 甚至会拒绝含 update 的历史。

> **「运行时可调推理强度」与「自动压缩」互不兼容，两边各自踩到。
> 这种共性通常意味着它是本质困难，不是某家的实现瑕疵。**

---

## 八、拿去撞主线：第一原理可能要从「预算」升级成「负债」

我们原来的第一原理：**Context 是预算，不是仓库。**

这次算完账会发现它不够准。预算是一次性的容量约束，**它描述不出"每件东西进来之后还在持续收费"这件事**。

更贴切的表述可能是：

> **Context 不是预算，是一份按轮次计息的负债。**

三种不同性质的持有：

| 内容类型 | 性质 | 计息方式 |
|---|---|---|
| 未命中缓存的常驻项 | 高利贷 | 每轮全额重付（5×、50× 的差距由此而来） |
| 命中缓存的常驻项 | 付息极低的债券 | 0.1×／轮，**但要求字节级稳定** —— 改一个空格，前缀断裂，利率瞬间跳回高利贷 |
| 思考 | 当期费用 | 一次性 5×，但在 Opus 上会转成后续负债 |

这个视角比"预算"更有解释力。它能自然推导出为什么必须重视前缀稳定性、为什么卸荷优于压缩、为什么会存在 200 行这类限制。

**预算观默认"放进去就结束"，负债观提醒你"它在后面每一轮都在收利息"。**

（待 Codex / 开源侧交叉验证后再决定是否写进主线。）
