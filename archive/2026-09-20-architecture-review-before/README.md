# Memory 与上下文工程

面向已了解 LLM 与 Agent 的进阶读者。

**实质**：构建一套 agent 领域的认知体系，再把它编译成不同形态的产物。认知层（`domain/`）是本体，教材与手册是它的投影——产物会过时、会重写，认知层不会。

---

## 30 秒

- **在做什么**：建立对 agent 记忆与上下文运作机制的认知体系
- **到哪了**：认知层骨架已建，机制库待建；教材与手册是后期产物，现在不写
- **从哪看起**：`domain/index.md`

---

## 怎么逛这个仓库

**第一次来（5 分钟）**
1. 本页
2. `domain/index.md` —— 我们用什么坐标系看这个领域
3. `THESIS.md` —— 我们要赌的那条主线，以及它最可疑的那一段

**想看我们拆过什么（10 分钟）**

`analysis/claude-code/` 目前两篇：

- `context-management-offload.md` —— 官方给的所有减负手段都不是「压得更好」，而是「别让它进来」
- `context-economics-two-traps.md` —— 50 倍价差；以及 Opus 上「追求更强推理 = 间接买到更高失忆风险」

**想看论文原料**

`sources/papers/surveys/README.md` —— 它自己有五层渐进披露，读完第 0 层就能走。

**想看我们聊过什么（含被否掉的选项）**

`dialogue/` —— 按问题记，死路也留着。

---

## 目录

| 目录 | 装什么 |
|---|---|
| `domain/` | **认知层 · 一号资产**：坐标系 / 系统定位 / 分歧 / 机制库 |
| `sources/` | 别人写的：论文、第三方仓库、调研报告 |
| `analysis/` | 我们对外部系统的完整拆解 |
| `evidence/` | 支撑具体论断的原始摘录，与文档同名配对 |
| `dialogue/` | 交流记录：问了什么、怎么推演、否掉了什么 |
| `notes/` | 已拍板的决定 |
| `book/` `manual/` | 后期产物，现在不写 |
| `archive/` | 会话快照 |

分水岭：**`sources/` 是外部世界，其余都是我们的产出。**

---

## 目标与边界（原始定义）

- 重点方向：harness 工程、上下文工程、memory
- 定位：面向已了解 LLM 与 Agent 的**进阶**教材，重点在**工程化**与**记忆的深度讲解**
- 教学法：**先找到共性，把核心思路讲透，然后再在各点深入**
- 不做什么：不做入门科普，不做框架罗列

**待补的研究对象**（原清单，尚未拆解）：

- 纯记忆框架：mem0 / zep / everOS / memgit
- 自带记忆的 harness：codex / claude-code / hermes / openclaw / manus / pi agent / gemini / kimi code / minimax code / tianshu
- 框架层：langchain 及 langmem、openviking 的记忆库

---

## 规则在哪

| 要什么 | 去哪 |
|---|---|
| **这个项目是怎么设计的、为什么这么定** | [ARCHITECTURE.md](ARCHITECTURE.md) |
| 改文件、放东西、往认知层加条目 | `project-maintenance` skill |
| 目录结构与命名 | `CONVENTIONS.md` |
| 教材什么该写、什么不该写 | `TRADEOFFS.md` |
| AI 常驻指令 | `AGENTS.md` |

人读本页，AI 读 `AGENTS.md`。要审查设计读 `ARCHITECTURE.md`。
