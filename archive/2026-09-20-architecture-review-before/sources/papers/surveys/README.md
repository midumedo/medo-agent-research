# 综述 · 阅读入口

七篇 Agent Memory 综述，已下载并解析为 Markdown。每一层都先给「要不要继续往下」的判断依据——**读完第 0 层就可以走**。

---

## 第 0 层 · 如果只有 15 分钟

读 **[2512.13564.md](2512.13564.md) 的 §2.3**（Comparing Agent Memory with Other Key Concepts）。

理由：48 位作者花了一整节专门划清 agent memory 与 **LLM memory、RAG、context engineering** 的边界。这不是术语洁癖——如果这一步没立住，后面所有"记忆系统"的讨论都会退化成"高级一点的 RAG"。我们教材的序章"记忆不是什么"就靠这一节。

---

## 第 1 层 · 七篇一览，以及**什么时候可以不读**

| 编号 | 一句话 | 它回答什么 | 篇幅代价 | 什么时候跳过它 |
|---|---|---|---|---|
| **2512.13564** | 48 位作者的共识尝试，三轴建立共同语言 | 记忆到底分几种？边界在哪？ | 2997 行，密度高 | 几乎不该跳过 |
| **2603.07670** | write–manage–read 闭环 + 五族机制 | 记忆系统有哪些实现路线？ | 643 行，最省时 | 若只要分类体系，可只看 §3 |
| **2602.06052** | "下半场"：长程自主 Agent，程序性记忆是重点 | 技能怎么沉淀？多 Agent 怎么共享？ | 2238 行，密度不均 | 不做程序性记忆 / 多 Agent 可跳过 |
| **2505.00675** | 表示形态 + 六个原子操作 | 记忆的生命周期有哪些动作？ | 1836 行 | 只要"六操作"清单，读 §2.4 即可 |
| **2606.06448** | 系统负载实测：三相开销归因 + 10 条建议 | 记忆到底贵在写还是读？ | **415 行**，短文 | 不做工程底座可跳过 |
| **2404.13501** | 奠基之作，来源 × 形式 × 操作 | 术语从哪来？早期怎么分？ | 1063 行 | 时间紧可跳过；想写历史脉络再看 |
| **2607.16848** | 评测协议批判：脱离预算的榜单不可解读 | 那些分数能不能信？ | 914 行 | 不写评测章可跳过 |

---

## 第 2 层 · 三条路径，按目的选一条

**路径 A · 立教材的概念骨架**（推荐先走这条）
1. 2512.13564 §2.3 → 划边界
2. 2603.07670 §2–§3 → 建回路与 taxonomy
3. 2603.07670 §8 → 看它对其它综述的定位，确认分工
4. 2505.00675 §2.4 → 补六个原子操作

**路径 B · 做工程底座 / Harness**
1. 2606.06448 全文 → 三相开销归因、10 条建议
2. 2603.07670 §7 Engineering Realities → 写路径过滤、矛盾处理、延迟预算、隐私
3. 2602.06052 §4–§5 → 操作机制与学习式策略

**路径 C · 评测与方法论**
1. 2607.16848 全文 → 协议如何决定结论
2. 2606.06448 §4 → 实测对照
3. 2404.13501 §6 → 旧评测观（对照看它怎么过时）

---

## 第 3 层 · 逐篇卡片

> 同样的卡片已写进每篇 md 的头部（"## 导航卡"），可直接 grep 直达。改 `nav.json` 后重跑 `pdf2md.py --force` 即生效。

### 2512.13564 · Memory in the Age of AI Agents（2025-12，48 人）
- **分类轴**：Forms（token-level / parametric / latent）× Functions（factual / experiential / working）× Dynamics（formation / evolution / retrieval）
- **必读**：§2.3 概念边界、§3 Form、§4 Functions、§5 Dynamics 定义段、§6 资源与框架汇总
- **可跳过**：§7 前沿展望（五个方向各一小节，点到即止）
- **盲区**：程序性记忆只在 taxonomy 表里出现，工程实现几乎没写；完全没有系统开销与缓存视角
- **回答什么问题**：记忆和 RAG、长上下文的边界在哪？记忆该分成几类？

### 2603.07670 · Memory for Autonomous LLM Agents（2026-03，单作者 Du Pengfei）
- **分类轴**：write–manage–read 闭环；三维 taxonomy（temporal scope / substrate / control policy）；五族机制
- **必读**：§2 问题形式化、§3 三维 taxonomy、**§7 Engineering Realities**、**§8 对其它综述的定位**
- **可跳过**：§6 五个应用领域的罗列
- **盲区**：单作者，覆盖靠引用而非实测；没有系统 profiling
- **回答什么问题**：记忆系统有哪些实现路线？工程落地有哪些现实约束？

### 2602.06052 · A Survey of Agent Memory in the Second Half（2026-01，60 人）
- **分类轴**：Substrate（internal / external）× Cognitive（sensory / working / episodic / semantic / procedural）× Subject（user-centric / agent-centric）
- **必读**：§3 的 Subject 轴与 procedural 部分、§4 操作机制、§5 Learning Policy、多 Agent 记忆路由与可移植技能生态
- **可跳过**：各认知类型小节（与其他综述重复度高）、§8 应用
- **盲区**：没有系统开销量化；60 位作者导致部分章节像拼接
- **回答什么问题**：程序性记忆怎么工程化？多 Agent 怎么共享记忆？

### 2505.00675 · Rethinking Memory in LLM based Agents（2025-05，8 人）
- **分类轴**：表示（parametric vs contextual）× 六操作（Consolidation / Updating / Indexing / Forgetting / Retrieval / Condensation）
- **必读**：§2.1 表示、**§2.4 六操作**、**§5 The Cognitive Gap between Biological and Agent Memory**（少见的反类比反思，适合拿来批判"人脑隐喻"）
- **可跳过**：§3 四个 topic 的文献罗列、§4 产品清单（时效性差）
- **盲区**：不谈系统开销、Harness、缓存；六操作之间没给调度与触发条件的工程讨论
- **回答什么问题**：记忆生命周期有哪些原子操作？人脑隐喻靠不靠谱？

### 2606.06448 · Agent Memory: Characterization and System Implications（2026-06，9 人）
- **分类轴**：系统四轴；phase-aware profiling 归因到 construction / retrieval / generation
- **必读**：§3 profiling harness、**§4 实测归因**、§5 的 10 条建议（construction scheduling / capability floors / amortization / freshness-latency / fleet-scale）
- **可跳过**：§2 四轴 taxonomy（不是它的贡献点）
- **盲区**：是短文（约 6–8 页），无体系性分类；只测 10 套系统；不涉及缓存友好
- **回答什么问题**：记忆系统贵在写还是贵在读？开销在三相之间怎么分布？

### 2404.13501 · A Survey on the Memory Mechanism of LLM based Agents（2024-04，9 人）
- **分类轴**：来源（inside-trial / cross-trial / external）× 形式（textual / parametric）× 操作（writing / management / reading）
- **必读**：§3.2 / §3.3 窄定义与宽定义、§4.1 认知心理学视角、§5.2.3 textual 与 parametric 优劣对比
- **可跳过**：§7 应用场景罗列、§6 评测（已被 2607.16848 部分推翻）
- **盲区**：2024 年 4 月，mem0 / Zep / Letta / OpenViking 之后的生态完全没有；无程序性记忆、无 Harness、无缓存
- **回答什么问题**：这套术语从哪来？早期怎么分类？（历史脉络，不是现状）

### 2607.16848 · Beyond Memory Leaderboards（2026-07，3 人）
- **分类轴**：不论分类，论评测协议（ingestion granularity / raw-text preservation / retrieval budget / modality / rubric / judge）
- **必读**：§2 的十种机制家族梳理（意外的好评测地图）、budget 控制前后的对比、multi-judge 与人类对齐校准、它对评测目标的重定义
- **可跳过**：Theoria 自身的方法细节
- **盲区**：只做科学论文领域的记忆，不覆盖对话式记忆与编码 Agent 场景
- **回答什么问题**：榜单分数能不能信？评测协议怎么决定结论？

---

## 第 4 层 · 按问题索引（不是按论文索引）

| 我想回答的问题 | 去哪 |
|---|---|
| 记忆和 RAG / 长上下文的边界在哪？ | 2512.13564 §2.3 |
| 记忆该分成几类？有共识吗？ | 2512.13564 §3–§4（Forms × Functions）；2602.06052 §3（含 Subject 轴） |
| 记忆有哪些原子操作？ | 2505.00675 §2.4（六操作）；2404.13501 §5.3（写/管/读） |
| 程序性记忆（技能沉淀）怎么工程化？ | 2602.06052 §3 procedural + §5；2603.07670 §4 反思族 |
| 记忆系统到底贵在写还是读？ | 2606.06448 §4 |
| 记忆管理能不能学出来（RL）？ | 2602.06052 §5 Learning Policy；2603.07670 §4 学习式管理 |
| 多 Agent 怎么共享 / 路由记忆？ | 2602.06052 多 Agent 部分 |
| 榜单分数能不能信？ | 2607.16848 全文 |
| 人脑隐喻靠不靠谱？ | **2505.00675 §5**（少见的反思） |
| 有哪些开源框架和基准可用？ | 2512.13564 §6（最全的一手汇总） |

---

## 第 5 层 · 这七篇**集体**没解决的问题

这是我们教材的空白带，也是立身之地。以下六条在七篇综述里都找不到系统回答：

1. **缓存友好性**——没有一篇讨论 prefix caching、cache_edits、冻结前缀。而这是生产上最省钱的一维（实测差 50 倍）。
2. **Harness 作为记忆系统**——Claude Code / Pi / OpenClaw / Hermes 的压缩与隔离工程实践在综述里几乎缺席，它们被当作"应用"而非"记忆系统的一种形态"。
3. **常驻层预算**——Hermes 3,575 字符、OpenClaw 20,000 字符这类硬上限在综述里找不到，但它是决定记忆系统行为的最强约束。
4. **程序性记忆的工程范式**——被反复点名"最重要、最缺工具"，却没人给实现范式。
5. **记忆与版本控制**——memgit、Letta Context Repositories 这类"记忆可 diff / 可回滚"的思路完全未被综述收录。
6. **评测协议问题**——2607.16848 刚提出，尚未进入任何综述正文，主流综述仍在引用那些不可复现的分数。
