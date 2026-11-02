# 译本库

本目录保存五篇 agent memory 综述的中文译本、逐篇译法摘记与合并后的术语总表。译本均由 DeepSeek-V4.1-Flash 于 2026-11-02 生成，源文件为 `../md/` 下的同名英文机器转换件。

## 总规则

1. **关键术语保留英文原形，中文承担叙述、连接与论证。** `memory`、`agent memory`、`context`、`prompt`、`retrieval`、`consolidation`、`KV cache` 等词在译文中保持英文；中文用于句法连接、解释与评价性表述。
2. **译本不替代原文。** 引用具体数字、表格单元格、公式、指标口径或参考文献时，必须回到 `../pdf/` 下的同名 PDF 核对，不能只依据译本或机器转换文本。
3. **摘记不是术语表。** 每份 `*.zh.notes.md` 记录该篇的定译、备选、句例与存疑；跨篇的统一口径见 [术语总表.md](术语总表.md)。

## 五篇索引

| 简写 | 译本文件 | 对应英文源 md | 主题一句话 | 行数 / 字符数 | 摘记文件 | 质量状态 / 已知源文缺陷摘要 |
| :--- | :--- | :--- | :--- | ---: | :--- | :--- |
| **MemMech** | `arxiv-2404.13501.Survey.Memory Mechanism.zh.md` | `arxiv-2404.13501.Survey.Memory Mechanism.md` | LLM-based agent 的 memory 是什么、为什么需要、如何实现与评估，以及应用与未来方向。 | 888 / 91,228 | `arxiv-2404.13501.Survey.Memory Mechanism.zh.notes.md` | 未记录结构性缺陷。源文用 `episode memory` 而非 `episodic memory`，另有 `spacial tasks` 疑为 `spatial` 拼写问题；译本均按原样保留，未擅改。 |
| **Rethink** | `arxiv-2505.00675.Survey.Rethinking Memory.zh.md` | `arxiv-2505.00675.Survey.Rethinking Memory.md` | 以 parametric / contextual 两种表示与六种原子操作重划 agent memory，并映射到 long-term memory、long-context、parametric 修改与 multi-source 四个主题。 | 1,389 / 187,576 | `arxiv-2505.00675.Survey.Rethinking Memory.zh.notes.md` | 未记录结构性缺陷。术语采用“名词保留英文、动词用中文”的分工，导致部分句子中英混排偏密；`integration` 与 `consolidation` 的动词都落为「整合」，需靠英文原形区分。 |
| **AgeMem** | `arxiv-2512.13564.Survey.Age of Agent Memory.zh.md` | `arxiv-2512.13564.Survey.Age of Agent Memory.md` | 从 forms、functions、dynamics 三个视角重审 agent memory，并汇总 benchmark 与开源框架。 | 2,271 / 314,291 | `arxiv-2512.13564.Survey.Age of Agent Memory.zh.notes.md` | 已知源文表格缺陷较多：Table 1 表头作 `Memory Structure` 而正文分类应为 `Memory Form`；Table 3 的 FOT 行 `memory attention KV` 单元格原意不明；Table 4 的 MemVerse 行内容错位；Table 8 的 `SWE-Bench Verified` 行后缺 `</tr>`；§1 末段有分页断句。译本按源文照录、未静默纠正，较源文少 19 行（合并断句与空行差异，非删节）。 |
| **AgentMem** | `arxiv-2602.06052.Survey.Agent Memory.zh.md` | `arxiv-2602.06052.Survey.Agent Memory.md` | 以 memory substrate、cognitive mechanism、memory subject 三维统一 foundation agent memory，并讨论单/多 agent 操作、学习策略与评测。 | 1,716 / 245,950 | `arxiv-2602.06052.Survey.Agent Memory.zh.notes.md` | 未记录结构性缺陷。源文 §7.2 附近有残字「确」，译本已修正；源文 `weight-based` / `state-based` 与译文 `weight memory` / `state memory` 形成混合形；`memory trace` 与 `engram` 合并后各保留一次，弱化了原措辞。 |
| **AutoMem** | `arxiv-2603.07670.Survey.Autonomous Memory.zh.md` | `arxiv-2603.07670.Survey.Autonomous Memory.md` | 把 agent memory 形式化为 write–manage–read 循环，提出 temporal scope、representational substrate、control policy 三维分类与五个机制族，并讨论评测与工程现实。 | 593 / 45,665 | `arxiv-2603.07670.Survey.Autonomous Memory.zh.notes.md` | 未记录结构性缺陷。源文 `expartner` 为粘连拼写，译本按语义拆为「前伴侣」；`precis` 的体裁义与 `modest` 的程度义在译文中有所折损。参考文献 64 个段落中有 1 段是 51 号 AutoGen 条目的折行残片，实际条目为 63。 |

字符数按文件全部字符计（含空白、Markdown 标记与英文原形），不是汉字字数。

## 校验

计数方法：标题为 `^#{1,6}` 行数；参考文献为 `## References` / `## 参考文献` 之后的条目数（编号条目按 `[n]` 计，无编号条目按空行分隔的段落计）；表格为 `<table>` 出现次数；图片引用为 `![...]` 出现次数。源文与译本在同一方法下逐项对照。

| 简写 | 标题数（译 / 源） | 参考文献（译 / 源） | 表格（译 / 源） | 图片引用（译 / 源） | 与历史记录核对 | 结论 |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **MemMech** | 55 / 55 | 174 / 174 | 4 / 4 | 5 / 5 | 与 55 / 174 / 4 / 5 一致 | 通过 |
| **Rethink** | 34 / 34 | 382 / 382 | 19 / 19 | 35 / 35 | 与 34 / 382 / 19 / 35 一致 | 通过 |
| **AgeMem** | 103 / 103 | 503 / 503 | 9 / 9 | 15 / 15 | 摘记只记「与源文一致」，未留具体数字；本次补计为 103 / 503 / 9 / 15 | 通过（补计） |
| **AgentMem** | 75 / 75 | 561 / 561 | 6 / 6 | 11 / 11 | 历史记录参考文献为「—」；本次补计为 561 | 通过（补计） |
| **AutoMem** | 63 / 63 | 63 / 63 | 2 / 2 | 0 / 0 | 与 63 / 63 / 2 / 0 一致 | 通过（源文 64 段含 1 段折行残片） |

补充说明：

- 行数差异：MemMech 888 / 891、Rethink 1,389 / 1,409、AgeMem 2,271 / 2,290、AgentMem 1,716 / 1,707、AutoMem 593 / 595（译 / 源）。这些差异来自断行、空行与段落合并，未见整节缺失；AgeMem 的 −19 与其摘记记录一致。
- AutoMem 源文 `## References` 之后有 64 个非空段落，其中第 52 段 `applications via multi-agent conversation...` 是第 51 段 AutoGen 条目的折行残片，不是独立文献；按完整条目计为 63，与译本 63 条一致。
- 以上校验只核对计数，不等于逐条核对内容；具体数字与表格仍须回 PDF。

## 推荐阅读顺序

1. **AutoMem**（593 行，最短）。先读这篇建立问题框架：为什么固定 context window 不够、write–manage–read 循环是什么、五类机制如何分工。它的批评性判断最集中，适合先读。
2. **MemMech**（888 行）。再读这篇补齐经典分类：memory sources、textual / parametric forms、writing / management / reading 三类操作，以及直接 / 间接评估。它是最早的体系化综述，术语最保守。
3. **Rethink**（1,389 行）。接着读操作视角：六种原子操作与四个主题。读这篇时要同时打开摘记，否则 `retrieval`、`consolidation`、`integration` 的名词/动词分工容易看漏。
4. **AgentMem**（1,716 行）。然后读三维统一框架与评测部分；这篇的 `memory substrate / cognitive mechanism / memory subject` 是理解后两篇分类差异的钥匙。
5. **AgeMem**（2,271 行，最长）。最后读这篇的最新全景，把它当作查证手册：forms / functions / dynamics、benchmark 表与框架表适合按需回查，不必一次顺读。

如果只读一篇，先读 **MemMech**；如果只读一篇最新的，读 **AgeMem**；如果关心“记忆操作如何设计”，读 **Rethink**。

## 用法

- **先查术语总表，再读译本。** [术语总表.md](术语总表.md) 给出英文原形、是否保留、一句界定、出处与跨篇差异；遇到同一词在不同篇含义不同时，先看该表的「跨篇冲突」节。
- **摘记配合译本查。** 摘记记录的是“为什么这样译、备选是什么、哪里存疑”。Rethink 摘记的位置编号明确指译本行号；其余摘记多用章节号或原文位置，查的时候以译本小节标题为准。
- **`../单词本.md` 仍是阅读工具。** 它按阅读场景组织术语、句法与符号，不是术语表合并产物；需要跨篇术语口径时以本目录的术语总表为准。
- **引用回 PDF。** 译本用于理解和检索，不作为引用底本；数字、表格、公式与参考文献条目回到 `../pdf/` 核对。

## 文件角色

| 文件 | 角色 |
| :--- | :--- |
| `*.zh.md` | 五篇中文译本，只读底稿，不因术语统一而回改正文 |
| `*.zh.notes.md` | 逐篇译法摘记：定译、备选、句例、存疑 |
| `术语总表.md` | 五份摘记的术语合并、分族、冲突与存疑清单 |
| `README.md` | 本目录索引、总规则、阅读顺序与计数校验 |
