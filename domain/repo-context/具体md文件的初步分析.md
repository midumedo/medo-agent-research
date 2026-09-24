# 具体md文件的初步分析
草稿！

### 1. THESIS.md 【项目立论/核心主张文档】⭐Agent项目最重要
> 直译：**论题、立论文档**
普通后端几乎没有这个文件；**LLM‑Agent项目专属产物**。
写：
- 本项目的**底层假设**：我们认为Agent应该是什么样子；反对哪些流行思路。
- 哲学层面的设计立场：比如“我们不做无限长的ReAct循环”、“记忆层独立于LLM，不要塞进system prompt”；
- 本项目要证明的命题：**这一套harness架构为什么是可行的**；
- 哪些现有框架(LangGraph、AutoGPT)的痛点本项目试图解决。

> 用途：团队后期做重构的时候先回来看THESIS，防止做着做着架构跑偏。
> 很多时候架构漂移就是大家忘记最初立论。
> 👉 kimi‑code tianshu‑harness 内部就有类似THESIS的思想文档。

### 2. ARCHITECTURE.md（架构）
技术架构，模块划分、数据流图、高层组件；接口之间怎么调用；目录src模块职责。
> 和THESIS区别：
> - THESIS：**为什么这么设计（why），立场、假设**
> - ARCHITECTURE：**长什么样（what/how），模块与数据流**

### 3. TRADEOFFS.md【权衡取舍文档】⭐非常关键
> AI项目到处都是取舍！不要只写最终方案，**把放弃的方案也要写下来**。
记录每一次重要决策的利弊：
示例条目：
```
# 决策1：记忆是否存入Redis
✅ 方案A：Redis持久化
    pros：性能好；支持多进程共享记忆
    cons：运维重；本地开发需要启动redis
❌ 放弃方案B：本地sqlite文件记忆
    pros：开箱即用无依赖
    cons：多进程冲突；大数据检索慢
Decision：选择A；接受运维代价
```
**价值：防止以后新人又重新踩坑，反复把之前否决过的方案拿出来讨论；重构的时候知道当初为什么这么选。**
> 普通业务项目很少维护TRADEOFFS；但是Agent/LLM框架强烈建议维护。

### 4. CONVENTIONS.md 项目开发规约
- 代码风格、命名；
- Prompt片段怎么管理；
- Agent skill的编写规范；
- 日志规范；
- 内部markdown文档自身的写作规范；
> 相当于本项目内部的“开发手册”。

### 5. AGENTS.md / AGENTS.local.md
专门针对agent定义：
- AGENTS.md：**官方内置agent角色定义，系统自带的agent；角色、system prompt概要、能力清单**
- AGENTS.local.md：**本地开发时，开发者自己临时写的实验agent，不要提交git！一般写进.gitignore**
> local后缀惯例：所有 `*.local.md` = 本机临时笔记，不进版本库；本机调试记录，草稿。

### 6. MEMORY.md
关于本项目的记忆

### 7. USER.md
站在用户视角：用户模型；用户会话、用户偏好；用户状态；权限；用户侧约束；Agent如何感知用户。

### 8. INDEX.md
**根文档索引页**。相当于本项目内部文档的首页目录。
列出所有内部md文档链接：
```
# 项目内部文档索引
- THESIS.md 核心立论
- ARCHITECTURE.md 架构
- TRADEOFFS.md 取舍记录
- AGENTS.md Agent角色
```
> 适合vscode workspace打开，点索引跳转全部设计笔记；相当于简易内部wiki首页。

### 9. CHANGELOG.md
版本变更，Keep‑a‑changelog格式，对外。

### 10. SECURITY.md
安全策略；漏洞上报方式；Agent风险提示（prompt注入风险、工具调用越权风险）。
> Agent项目这里尤其重要：说明工具调用沙箱、权限隔离。

---

# ✨【补充：你还应该新增哪些md文件？AI Agent项目建议补充】
> 基于Moonshot kimi‑code harness、还有很多开源agent框架实践总结

1. **DECISIONS.md / ADRs (Architecture Decision Record)**
> ADR架构决策记录。
TRADEOFFS偏向权衡清单；ADR是一条条正式架构决策记录；很多项目直接用 `adr/` 文件夹放一堆adr‑001‑xxx.md。
> 如果项目不大，可以直接在根目录`DECISIONS.md`；大项目单独adr目录。

2. **PROBLEMS.md（现存问题 / debt 技术债务）**
记录当前架构已知缺陷、待解决痛点、技术债务。不要只放在github issue；根目录文档记录高层问题。
> 比如：“当前记忆压缩策略会丢失细节；后续需要做分层摘要”。
> 重构的时候优先看这个文件。

3. **EXPERIMENTS.md**
开发过程做过的各种废弃实验；试过哪些方向最后砍掉；实验结论。
> 和tradeoffs有重叠，更偏向原型实验结果。

4. **LIMITATIONS.md（项目局限性）【对外+内部】**
明确写明本Agent框架固有的局限；哪些问题本框架不打算解决；不要让使用者产生不切实际预期。
> AI项目非常需要这个：比如“本框架不支持多agent并行；长会话超过32k上下文性能下降明显”。

5. **ROADMAP.md 路线图**
短期、中期、长期版本规划。

6. **NOTES/ 文件夹（不要全部堆根目录！）**
> 当根目录md越来越多之后，根目录会爆炸！
> 演进方案：根目录只保留核心：README, BRIEF, CHANGELOG, SECURITY；
> **所有内部开发者文档全部移动到 `docs/` 或者 `design/` 子文件夹！**
```
docs/design/
    THESIS.md
    ARCHITECTURE.md
    TRADEOFFS.md
    DECISIONS.md
    AGENTS.md
    MEMORY.md
    INDEX.md
```
> 很多新手agent项目直接把十几份md堆在项目根目录，github根页密密麻麻一堆md，观感很差。
> 区分：
> - 根目录：对外文档（少数）
> - `docs/design/`：全部内部开发者设计笔记（大量）

# AGENTS.md
你会有“感觉它啥都要干”的困惑，本质上是因为很多开源项目和网上的教程**把 `AGENTS.md` 当成了垃圾桶**——架构、业务逻辑、编码风格、环境配置全都往里塞。

如果职责已经分出去了（业务/架构在 `ARCHITECTURE.md`，历史决策在 `docs/adr/`，格式排版交给了 Linter），那么 **`AGENTS.md` 的核心职责其实只剩一个：当好一个“操作员的操作守则与执行沙盒”。**

一句话概括它的定位：**它不解释“系统是什么”（What/Why），只规定“作为执行者，你必须怎么做、如何自检、绝不能碰什么”（How/Verification/Boundaries）。**

---

### 一、 它必须负责的 4 件事（不可替代）

#### 1. 确定性的“工具链与命令”（Command Runbook）

LLM 不是通过“猜”来跑代码的。没有这一节，Agent 遇到测试会瞎猜是 `npm test`、`yarn test`、`pnpm test` 还是 `pytest -s`。

* **开发指令**：`pnpm dev`
* **单测指令**：`pnpm test:run <file-path>`（教它如何只跑单文件，避免每次改两行跑整个套件耗死 Token）
* **类型检查**：`pnpm typecheck`
* **格式化/Lint**：`pnpm lint:fix`

#### 2. “完成定义”与自检闭环（Definition of Done, DoD）

人类不盯着它时，Agent 最大的坏毛病是：**改完代码立刻交卷，压根不知道自己的改动导致编译断裂或逻辑崩溃。**
你必须在 `AGENTS.md` 里给它戴上紧箍咒：

> **在向我汇报任务完成前，你必须按顺序执行：**
> 1. 运行相关文件的单元测试，确保无断言失败。
> 2. 运行类型检查（如 `tsc --noEmit`），确保零类型错误。
> 3. 运行代码检查（如 `ruff check`）。
> 如果报错，必须自行修复并再次验证；若无法解决，必须在回复中如实说明报错日志。
> 
> 

#### 3. 破坏性操作的“安全红线”（Negative Constraints / Guardrails）

人类开发有常识，Agent 没有。你需要显式剥夺它自作主张的权力：

* ❌ **严禁操作**：`git push`、修改或提交 `.env*`、未经允许执行清空库表的 SQL（如 `DROP`、`TRUNCATE`）。
* ❌ **自作聪明型重构**：严禁“顺手”重构没有要求的外部模块，或者随意修改公共接口签名。
* ❌ **包管理约束**：禁止自行添加未经授权的大型第三方依赖库。

#### 4. 上下文按需检索指引（Context Routing）

既然职责分出去了，它需要知道**去哪里查什么**（充当调度指引）：

* 遇到系统架构或模块调用边界不清楚？$\to$ **去读 `ARCHITECTURE.md**`
* 遇到奇怪的构建报错或依赖冲突？$\to$ **去查 `docs/troubleshooting/**`
* 想要推翻当前设计或质疑选型？$\to$ **先查 `docs/adr/**`

---

### 二、 它绝对不应该包含的内容（必须剥离）

| 常见错误内容 | 为什么不要写进 `AGENTS.md` | 正确的归宿 |
| --- | --- | --- |
| **详细业务背景、产品定位** | 每次对话注入大量废话，降低 LLM 遵循指令的注意力 | `README.md` / `THISIS.md` |
| **缩进、空格、单双引号、Import 排序** | LLM 经常记不住，且浪费 Token | 交给 `.prettierrc`、`biome.json`、`ruff.toml` |
| **模块拓扑、分层架构、数据流图** | 这是系统模型，改动低频，混在一起会导致职责混乱 | `ARCHITECTURE.md` |
| **某个历史选型的推导与对比细节** | 只有重构时才有用，日常修改完全不需要常驻上下文 | `docs/adr/` |
| **个人本地路径或私有端口** | 提交后会污染团队成员的环境 | `.agents.local.md`（加入 `.gitignore`） |

---

### 三、 一个精简干练的 `AGENTS.md` 真实范例

不需要洋洋洒洒几千字，通常 **30–50 行** 就足够强悍：

```markdown
# Agent Operational Guidelines

## 1. Commands
- Run single test: `pnpm vitest run <path/to/test>`
- Type check: `pnpm typecheck`
- Lint fix: `pnpm lint:fix`

## 2. Guardrails (Strict)
- NEVER commit secrets, `.env` files, or modify credentials.
- NEVER execute destructive database commands (DROP, TRUNCATE, ALTER TABLE without approval).
- DO NOT refactor unrelated files outside the scope of the prompt.
- DO NOT add new dependencies without explicit permission.

## 3. Definition of Done (DoD)
Before claiming a task is complete, you MUST:
1. Run typecheck and ensure 0 errors.
2. Run tests relevant to modified files and ensure they pass.
3. Apply lint auto-fix.
If any step fails, fix it before reporting back.

## 4. Context Lookup
- System layers & architectural rules: Read `ARCHITECTURE.md`
- Strange build/runtime errors: Search `docs/troubleshooting/`
- Why a design choice was made: Check `docs/adr/`

```

---

### 总结

* **`ARCHITECTURE.md`** 是系统的**蓝图**（它长什么样）。
* **`docs/`** 是项目的**档案室**（过去发生了什么、踩过什么坑）。
* **`AGENTS.md`** 是给进场的施工工人发的**安全施工守则**（戴安全帽、拿什么扳手、干完活怎么自验、哪里严禁踩雷）。

职责分出去后，它非但不会变臃肿，反而变得极其轻量、锋利且不可替代。