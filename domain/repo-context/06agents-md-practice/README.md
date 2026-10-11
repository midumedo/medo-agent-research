# 06 · AGENTS.md 的写法：最佳实践及其证据强度

> 属于 `domain\repo-context\` 研究，阶段 **06agents-md-practice**
> 相关材料：[初步研究计划](../初步研究计划.md)（早期研究纲领）、[research/kimi round-01](../research/kimi/research/round-01-agents-md.md)（标准史与生态兼容矩阵）、[文档参考资料](../01docsclassify/v9/README.md)（文档职责、读取和维护的解释）
> 产出者：qwen（AI 生成，见 [本主题 AGENTS.md](../AGENTS.md) 的命名约定）

## 这一阶段回答什么

前面的阶段问的是「仓库里有哪些 .md」「它们该怎么分类」「harness 用什么工具读」。这一阶段问一个更窄、更工程化的问题：**根目录那份 AGENTS.md 具体该怎么写**——写什么、不写什么、多长、怎么嵌套、怎么维护、跨工具怎么兼容。

选它作为独立阶段有两个理由。一是它是本项目自己正在用的制品（根 [AGENTS.md](../../../AGENTS.md) 就是协作者入口），写法结论可以直接反过来审查本项目。二是它是 `repo-context` 里少数**有实证研究可引**的对象：2026 年出现两篇 arXiv 论文测它的成本与成功率影响，不必全靠博客经验谈。

## 目录结构

| 文件 | 内容 |
|---|---|
| `README.md`（本文件） | 范围、与已有阶段的关系、证据边界、下一步 |
| `qwen/agents-md-best-practices.md` | 主研究稿：六章正文（标准定位／内容结构／嵌套与优先级／长度与 token 成本／失效模式与维护／跨工具兼容），含 6 张对照表、126 处溯源链接、21 条参考文献 |
| `qwen/insights.md` | **判断层**：六条见解，逐条「观察→推断→反例／待验证」。不可单独引用，引用必须回主研究稿找锚点 |
| `qwen/run-20261004/` | 本轮检索的原始资料层：`source_text.md`（清洗后资料正文）、`cited_urls.md`（来源清单）、`outline.md`（大纲与引用白名单）、`run_meta.json`（规模统计）。原始目录名为 `20261004-072241-da482b58`，为可读性改名为 `run-20261004`，`run_meta.json` 内的路径字段未同步 |

事实层与判断层分家的理由同 [04how-agent-read-file](../04how-agent-read-file/README.md)：主研究稿每句都能指到来源链接，`insights.md` 每条都带反例与待验证项——混在一份文档里，读者无法区分哪句可核对。

## 与其他阶段的关系（有意重叠）

[research/kimi round-01](../research/kimi/research/round-01-agents-md.md) 已有一张 2026 年中口径的工具兼容矩阵（8 款工具）和标准史（2025-08-20 发布、2025-12-09 捐赠给 Linux 基金会 AAIF、60,000+ 项目采用）。本轮的兼容矩阵是 9 款工具，字段更细（嵌套支持、大小限制、每轮发送时机、特殊行为）。**两张表不合并、不互相覆盖**：来源不同、口径不同、检索时间不同，并列保留才能看出哪些条目稳定、哪些是单源。

具体分歧已记录在 `qwen/insights.md` 第 5 条：round-01 记 Claude Code「不读 AGENTS.md（可用 @AGENTS.md import 或 symlink 桥接）」，本轮资料记 Claude Code「无 CLAUDE.md 时读 AGENTS.md，v2.1.277+ 支持」。这两条可能是时间差（版本演进）而非矛盾，但未核实版本号与日期。

与[文档模型参考](../01docsclassify/v9/文档模型.codex.md)的关系：该文解释协作入口、当前要求和其他信息职责怎样组合；本专题考察具体 AGENTS 写法。本轮工具发送时机的数据只描述所查样本，不能单独推出通用的常驻规则。

## 证据边界（引用前必读）

本轮资料的证据层级严重不均，这是本子主题最大的限制。21 个来源的构成：

| 层级 | 数量 | 来源 |
|---|---|---|
| 官方标准站 | 1 | `agents.md` |
| 工具官方文档 | 2 | `docs.devin.ai`、`docs.cline.bot` |
| arXiv 论文（**二手转述，未读原文**） | 2 | 2602.11988（Gloaguen）、2601.20404（Lulla） |
| 商业厂商指南／社区博客／内容聚合页 | 16 | augmentcode、digitalapplied、getunblocked、dev.to、掘金、火山引擎、w3cschool、CSDN、博客园、wsisp、神马、skills-hub |

按本轮当时的根级约定「重复转引同一来源不算独立证据」，本轮存在两处**单点依赖**：augmentcode 一篇商业指南撑起第 2.2、4.1、4.3、5.1 节的关键论断；digitalapplied 一篇博客撑起第 6.1 节整张工具矩阵。主研究稿中凡依赖这两处的数字，在 `insights.md` 里逐条标了待核实。

另外，主研究稿中「ETH Zurich 的研究指出」这一表述来自 augmentcode 的转述，本轮未取得该研究原文，论文标题、作者、年份均未知。

**适用性限定**：两篇 arXiv 研究测的都是编码代理在真实代码仓库上的表现（PR、SWE-BENCH）。本项目 `memory` 是纯文档仓库，代理的主要动作是读写 Markdown 而非改代码，「减少探索性导航」的收益机制未必成立。成本数字不得直接外推到本项目。

## 本项目自查结果

根 [AGENTS.md](../../../AGENTS.md) 实测 **23 行 / 844 字符 / 1890 UTF-8 字节**（2026-10-04，PowerShell 计数），远低于资料建议的 100-200 行，也远低于 Codex 的 32 KiB 上限。

结构上它是**导航型**（按任务指向 CONVENTIONS / STYLE / ARCHITECTURE / TRADEOFFS 及各子树 AGENTS.md），不是**指令型**（不含构建、测试、Lint 命令）。按本轮的「非可推断细节」判据，导航型是高价值内容——「哪个文件在什么条件下读」无法从代码推断，且本项目的职责文件分工本身是非标准的。缺构建/测试命令段落对纯文档仓库可能无碍，但仓库内确有可执行脚本（`sources/papers/_scripts/pipeline.py`、`domain/repo-context/05read-pdf-vs-html/measure_read_cost.py`），代理要复跑时无处可查。这条已记入 `insights.md` 第 6 条。

## 下一步

1. **取两篇 arXiv 原文入库**（`sources/papers/`，按该目录 AGENTS 的命名与入库流程）：2601.20404、2602.11988。核对编号真实性、样本构成、中位数口径，以及 Lulla 的「人工抽检质量相当」是与哪一组相比。
2. **向官方文档核实硬限制**：Codex 的 32 KiB 与 `project_doc_max_bytes`、截断方向；Antigravity 的 12,000 字符；Claude Code 的 4 MiB 与 v2.1.277。当前来源全是二手。
3. **实测本项目自己的加载行为**：这是 2026-10-04 的建议，当时列出的目录状态现已变化，`01docsclassify/AGENTS.md` 也已删除。若继续该实验，应先按届时实际存在的指令文件重新取样，再判断是否需要隔离设计。
4. **与 round-01 的 Claude Code 分歧对账**：确认 v2.1.277 的发布日期，判断两条记录是版本演进而非矛盾。

## 不做的事

- 不把 16 个博客／商业指南来源的经验数字当作已核实事实；`insights.md` 标了待核实的条目，下游不得引用。
- 不把两篇 arXiv 的成本百分比外推到文档型仓库或非编码任务。
- 不据本轮资料声称 `.cursorrules` 已废弃——资料说的是 Cursor 官方标记为 legacy，这是产品状态描述，不等于该文件在所有工具中失效。
- 不合并 round-01 与本轮的两张兼容矩阵；口径不同，合并会抹掉时间差信息。
