# 文档结构与 AI 指令：本次核对的外部资料

访问日期：2026-09-20。下面是已实际抓取页面中的短摘录及其支持范围，供 [本轮架构研究](../../analysis/knowledge-architecture-2026-09-20.md) 引用。它们是产品说明与文档设计建议，不是本项目目录效率或模型表现的实验结果。动态页面以后可能变化，本记录不声称固定了完整网页版本。

<a id="skills"></a>

## OpenAI 官方文档：技能的按需加载

请求 `https://developers.openai.com/codex/skills` 时，实际跳转至 [Build skills](https://learn.chatgpt.com/docs/build-skills)。

原文短摘录：

> “Skills use progressive disclosure to manage context efficiently.”

> “Implicit invocation: ChatGPT or Codex can choose a skill when your task matches the skill description.”

页面说明，ChatGPT 和 Codex 先获得技能名称及描述，选择使用技能时再读取完整 `SKILL.md`。

支持：描述会参与隐式选择，技能正文按需读取。因此把“所有文档新建、修订或迁移”写成用途，覆盖范围很广。但本项目没有收集触发日志，不能据此证明实际调用频率，或声称技能本身降低智能。

<a id="agents"></a>

## OpenAI 官方文档：项目指令

请求 `https://developers.openai.com/codex/guides/agents-md` 时，实际跳转至 [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)。

原文短摘录：

> “Codex builds an instruction chain when it starts (once per run; in the TUI this usually means once per launched session).”

> “Codex concatenates files from the root down, joining them with blank lines.”

支持：AGENTS 是用于提供项目指令的机制。把少量行动边界和按需阅读路由放在项目入口是合理用法。本文没有验证用户环境中的运行时加载轨迹，不能从官方机制直接推断本轮每次调用实际读了多少 token。

<a id="needs"></a>

## Diátaxis：按使用需要组织，而非填满框架

Daniele Procida，[Diátaxis](https://diataxis.fr/)：

> “documentation should itself be organised around the structures of those needs.”

[Diátaxis as a guide to work](https://diataxis.fr/how-to-use-diataxis/)：

> “the structure it proposes is not intended to be a plan”

> “It certainly does not mean that you should create empty structures for tutorials/howto guides/reference/explanation with nothing in them.”

支持：用文档结构检查不同阅读需要，避免为了展示结构创建空栏目。这里不直接采用该框架的四种文档类型；研究材料与产品文档的需要不同。

<a id="explanation"></a>

## Diátaxis：解释的价值在于建立关系

[Explanation](https://diataxis.fr/explanation/)：

> “For the user, explanation joins things together.”

> “Keep explanation closely bounded”

支持：主题综合应提供联系和解释，并有明确范围。这不等于删掉理解所必需的条件，也不规定综合必须有多少来源或多少页。

<a id="decisions"></a>

## Michael Nygard：保留被替代决定的理由

[Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)，2011-11-15。

> “Each record describes a set of forces and a single decision in response to those forces.”

> “If a decision is reversed, we will keep the old one around, but mark it as superseded.”

支持：历史记录保留当时约束和选择，改变后标明替代关系。它不要求本项目所有普通修改都建立 ADR，不要求历史决定与现行原则分别占一个根目录，也不能推出长文一定不会维护。
