---
name: grill-with-docs
description: 手工触发：对一个计划或设计做 relentless 追问，同时把定下来的术语和决定写进项目文档。当用户说"grill with docs / 对着文档拷问这个计划 / stress-test against the docs / 把这份计划问清楚并留下记录"时使用。不会由模型自动触发。
agent_created: true
---

# grill-with-docs

一个计划 → 一路追问到没有隐含假设 → 顺手把术语和决定写进项目文档。

Call the Skill tool with "grilling"，然后 Call the Skill tool with "domain-modeling"。两个都要调用：`grilling` 提供追问，`domain-modeling` 提供落笔。只跑追问不写文档，或只写文档不追问，都不是这个 skill。

## 前提

需要用户手动触发（说 "grill with docs" 之类）。对话开始前先做 `domain-modeling` 的 Step 0：读本项目的 AGENTS.md、CONVENTIONS.md、STYLE.md，确认术语和决定该写到哪。**这一步在问第一个问题之前完成**，否则追问会往一个不存在或错误的位置写东西。

本项目已知落点：术语进 `analysis/concepts-and-boundaries.md`，决定进 `dialogue/`（日期+主题命名）。若 `domain-modeling` 里的落点表与 CONVENTIONS 不一致，以 CONVENTIONS 为准。

## 会话形状

1. 用户说出计划。粗糙没关系。
2. 扫项目的术语与决定文档，索引现有用词。
3. 选一条分支，一次问一轮，每题引用文档作为依据："你的计划用了'记忆'，但项目里它指跨决策步骤保留、更新并能影响后续行为的状态及管理机制，你指的是这个还是别的？"
4. 用户回答的同时，术语定下来就 inline 写进项目既有的术语位置；够格的决定写进项目既有的决定位置。
5. 前沿空了、用户确认共识，结束。

副作用通常比计划本身更值钱：每次会话结束，项目的术语和决定记录都比一小时前更准一点。

## 什么时候别用

- 没有文档、也没有既有约定的全新项目 → 用 `grilling` 单跑，别硬写文档。
- 文档本身含糊或自相矛盾 → 先修文档，否则追问会空转。
- 一个很小的改动 → 二十个问题拷问一处文案改动是噪音。

## 注意

本 skill 是项目级安装，只对本项目可见。它描述的是**方法**（怎么发现约定、怎么追问），不存本项目的规则正本——规则正本在 CONVENTIONS.md。两者冲突时改本文件，不改 CONVENTIONS。

---

基于 Matt Pocock 的 `grill-with-docs`（mattpocock/skills, MIT）。原版是 7 行壳，只委派给 `grilling` 与 `domain-modeling`；本版保留该结构，并补上原版缺失的"先定位项目约定"前提与本项目落点指针。
