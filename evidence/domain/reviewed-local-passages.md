# 本地论文摘录：领域审查中已核对的段落

**核对日期：2026-09-20。** 本记录核对的是本地论文 Markdown 转换件中的段落，未联网核验 arXiv 当前版本，未逐页校对 PDF，也未复现实验。下列论文的本地版本号均**未知**；文件名对应 arXiv 标识不等于已锁定 `vN`。PDF 链接用于找回本地原件，不表示本轮检查过排版或提取准确性。

每节分开给原文和我方解释。摘录足以确认“本地所存论文讨论了什么”，不能单独确认被论文转引的系统能力、实验因果或跨领域普遍性。定位使用论文节号、标题和摘录文本，不依赖转换件行号或头部导航卡。

<a id="control-policy"></a>

## 控制策略：谁决定存、取、丢

**来源定位**：*Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers*，arXiv [2603.07670](https://arxiv.org/abs/2603.07670)，§3.3 **Control policy**。[本地正文](../../sources/papers/surveys/2603.07670.md#33-control-policy) · [本地 PDF](../../sources/papers/pdf/2603.07670.pdf)。本地资料版本：未知；本地核对日期：2026-09-20。

**原文摘录**：

> Perhaps the most consequential—and least discussed— dimension is _who decides_ what to store, what to retrieve, and what to discard.

> **Heuristic control** hard-codes rules: top- _k_ retrieval, summarize every _n_ turns, expire records older than _d_ days.

> **Prompted self-control** exposes memory operations as tool calls and lets the LLM decide when to invoke them.

> **Learned control** treats memory operations as policy actions optimized end-to-end.

**我方解释**：这直接否定“综述没人问谁决定，第三条轴由本项目首次加入”的旧说法。该节按控制策略区分机制；它不等价于完整的组织责任和权限模型，也不证明任何一种策略的普遍优势。本项目可继续研究提出、批准、执行和复核操作的边界，但应承认已有视角。

<a id="memory-scope"></a>

## 记忆范围：任务内状态与外部离散表示

**来源定位**：*Memory in the Age of AI Agents*，arXiv [2512.13564](https://arxiv.org/abs/2512.13564)，§2.2 **Agent Memory Systems** 与 §3.1 **Token-level Memory**。[本地 §2.2](../../sources/papers/surveys/2512.13564.md#22-agent-memory-systems) · [本地 §3.1](../../sources/papers/surveys/2512.13564.md#31-token-level-memory) · [本地 PDF](../../sources/papers/pdf/2512.13564.pdf)。本地资料版本：未知；本地核对日期：2026-09-20。

**原文摘录，§2.2**：

> During task execution, new information accumulates and functions as short-term, task-specific memory. Both roles are supported within a single memory container, with temporal distinctions emerging from usage patterns rather than architectural separation.

其中 “Both roles” 指前文的跨任务历史与当前任务中积累的状态。

**原文摘录，§3.1 的 Definition of Token-level Memory**：

> Token-level memory stores information as persistent, discrete units that are externally accessible and inspectable.

**我方解释**：按该论文定义，memory 不只指跨会话长期保存；任务内状态也是讨论对象。token-level 描述表示形式，外部存储描述位置，两者可以同时成立，不能作为互斥选项。这里采用的是一篇论文的定义，不能由此宣称整个领域已统一术语。

<a id="procedural-memory"></a>

## 程序性记忆：已有技能载体与实现讨论

**来源定位 A**：*Memory in the Age of AI Agents*，arXiv [2512.13564](https://arxiv.org/abs/2512.13564)，§4.2.3 **Skill-based Memory**。[本地正文](../../sources/papers/surveys/2512.13564.md#423-skill-based-memory) · [本地 PDF](../../sources/papers/pdf/2512.13564.pdf)。本地资料版本：未知；本地核对日期：2026-09-20。

**原文摘录 A**：

> Skill memory spans a continuum from internal, fine-grained code to externalized, standardized interfaces. The unifying criteria are straightforward: skills must be **callable** by the agent, their outcomes must be verifiable to support learning, and they must compose with other skills to form larger routines.

该节随后分别讨论 **Code Snippets**、**Functions and Scripts**、**APIs** 与 **MCPs**。

**来源定位 B**：*A Survey of Agent Memory in the Second Half: Towards Self-Evolving and Long-Horizon Agents*，arXiv [2602.06052](https://arxiv.org/abs/2602.06052)，§3.2.5 **Procedural Memory**，以 “A notable recent development” 开头的段落。[本地正文](../../sources/papers/surveys/2602.06052.md#325-procedural-memory) · [本地 PDF](../../sources/papers/pdf/2602.06052.pdf)。本地资料版本：未知；本地核对日期：2026-09-20。

**原文摘录 B**：

> Such externalization turns procedural memory from private agent state into portable, human-readable, and versionable infrastructure that can be inspected, shared, and reused across agents and models.

**我方解释**：这些段落足以否定“程序性记忆只被点名，没有实现范式或版本化讨论”的笼统判断。仍可追问哪些实现已被复现、技能如何验证和失效、不同框架如何加载；这些问题并未由这几句摘录解决。论文对所引系统和实证的判断仍需回查原始研究，不能把本地摘录当成系统复现。

<a id="evaluation-protocol"></a>

## 评测协议：预算与判分条件会影响比较

**来源定位**：*Beyond Memory Leaderboards: Evaluating Scientific Memory as Budgeted Context Restoration*，arXiv [2607.16848](https://arxiv.org/abs/2607.16848)，**Abstract**；实验条件见 §6.1 **Experimental setup**，Paim 比较见 **Table 4**。[本地摘要](../../sources/papers/surveys/2607.16848.md#abstract) · [本地 §6.1](../../sources/papers/surveys/2607.16848.md#61-experimental-setup) · [本地 PDF](../../sources/papers/pdf/2607.16848.pdf)。本地资料版本：未知；本地核对日期：2026-09-20。

**原文摘录，Abstract**：

> Our results show that memory leaderboards are not interpretable without the full protocol: ingestion granularity, raw-text preservation, retrieval budget, retrieval modality, rubric audit, and judge choice all affect the outcome.

> For example, on Paim Graphiti wins convincingly but uses 2.6M characters of retrieved context per query, and after controlling for retrieval budget the lead disappears.

**原文摘录，§6.1**：

> We run all memory systems on Paim (81 papers, 66 questions) and on PTr (252 papers, 98 questions).

**我方解释**：本地论文已经专门研究评测协议，所以不能把它列入材料集合后再说“这些材料都没系统回答协议问题”。文中数字是作者在科学论文记忆任务中的报告，单位是检索上下文字符，不能改称 token；本项目未复现。它支持追问比较是否控制预算与协议，不支持“所有评测都不可信”，也不直接给出编码 agent 或跨会话对话的效果结论。
