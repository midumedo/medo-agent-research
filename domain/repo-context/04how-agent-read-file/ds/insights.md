# 见解 · read 能力与文档治理

> **本文件是判断，不是证据。** 事实与可复现锚点在 `ds/read-tool-and-skill-loading.md`；这里的每一条都按
> 「观察 → 推断 → 反例 → 待验证」写，且**不可单独引用**——引用时必须回 `ds/read-tool-and-skill-loading.md` 找锚点。
> 分工写在两处：`ds/read-tool-and-skill-loading.md` 可独立成立；本文件只有与它合起来才成立。

---

## 见解 1：默认加载文件的稳态形态是「薄常驻 + 厚按需」，而不是「一份很全的 AGENTS.md」

**观察。** Tianshu-harness 把这件事量化到了常量：`LARGE_VOLATILE_PAYLOAD_CHARS = 12_000`
（`sources/repos/Tianshu-harness/src/context/payload-diagnostic.ts:27`），并对
`project-instructions` 段单独设 6000 字符阈值（`:49-54`），超限时给出的建议原文就是
"split project instructions into always-on core plus task-routed details"。同一个仓库的
项目模板测试断言模板应当只有 **30–120 行**，且注明"是通用版而不是完整的天枢 AGENTS.md"
（`src/bootstrap/__tests__/project-templates.test.ts:57`）。另一侧的 codex 干脆把指令做成
多来源列表按目录层级拼接（`codex-rs/app-server-protocol/src/protocol/common.rs:3229-3233`）。

**推断。** 两个独立实现都在往同一个方向走：常驻部分尽量薄、与每次会话都相关；其余按任务
路由。差别只在「怎么把外置部分拿回来」——codex 靠自动拼接多文件，单文件注入型 harness
靠模型的按需读取。**「一份大 AGENTS.md」是默认状态，不是稳态。**

**反例。** 这条不普适。若某个 harness 既不做多文件拼接、read 工具又只有整文件读
（本阶段的 9 个对象里没有这样的，但完全可能存在），那么拆分会让外置内容**无法被取回**，
此时「一份大文件」反而是更优解。判据是 harness 的两件事，不是文件长度本身。

**待验证。** 6000 / 1200 / 800 这些数字是**项目自设的 guardrail**，不是实测的悬崖。
`payload-diagnostic.ts` 的输出是「候选 + 理由 + 建议」，落在诊断面板里等人判断，**没有强制
裁剪**。把它们当成通用定律是误读。

---

## 见解 2：账本能有多宽，由「read 工具能不能做列投影」决定，与人的阅读习惯无关

**观察。** 本阶段取证的 **9 个对象**（codex、Tianshu-harness、deepseek-harness、Raven、
gemini-cli、qwen-code、cline、ZCode、claude-code）里，**没有一个** read 工具的入参含列选择。
最接近的三个也都不算：Tianshu-harness 的 `focus` 由启发式决定选什么；`read_section` 的粒度是
**节**不是列；gemini-cli `read_many_files` 的 `include`/`exclude` 是**文件级 glob**
（`sources/repos/gemini-cli/packages/core/src/tools/read-many-files.ts:58-70`）。

**推断。** 「把补充内容加到 CSV 后面」这个想法在**文档格式层**是无解的——只要工具按整行读，
加宽一列就是每次读都付那一列的成本。所以 `sources/papers/AGENTS.md` 的「`index.csv` 不加
摘要列」不是保守，是被工具面约束出来的正确解。反过来也成立：**帐本的宽度应当由工具能力决定**，
短枚举（`completeness` 这类 ≤ 12 字符的值）可以加，叙事性内容必须外置。

**反例。** 如果哪天某个 harness 提供了列投影工具（或 `read` 的 `limit` 语义扩展成字段级），
整条结论翻转。这不是理论假设——本阶段就验证过两个方向的近似物都在被尝试（`focus` 与
`read_section`），只是都还没做到确定性的列投影。另有一条隐含前提：文档里的 `grep -n`
按行定位在本项目可用，但**并非所有 harness 都给 shell**，届时「外置 + 行过滤」这条退路也会断。

**待验证。** 「用 `grep` 行过滤替代列投影」的实际成本没有实测。理论上它要求模型先想出
正确的过滤模式，而列投影是工具保证的确定行为——这两者的可靠性差距有多大，需要实验。

---

## 见解 3：「仓库藏了东西」应当是一等字段，但它必须能被机械复核

**观察。** 三个形态各异的样本：ZCode 的 `.gitignore:8-13` 排除了 `bundled-agents/`、
`bundled-tools/`、`prebuilds/`，而 README 声称包含运行时源码；OpenHands 的公开仓库顶层没有
`pyproject.toml`、没有 `openhands/` 包，只有 Web/Electron 前端；Claude Code 的 npm 包是
27KB 的启动包装器加一个预编译 `claude.exe`，读工具只以类型契约（`FileReadInput`）存在。

**推断。** 三者是同一个风险的不同表现形式：**「这个上游有仓库」会被自动读成「它的实现可以
被核对」**。引用纪律因此需要一条前置判据——`sources/repos/index.csv` 的 `completeness` 列
就是这条判据。它比许可证更该进账本（许可证不影响研究可用性，实现是否可读影响）。

**反例。** 不是所有「缺」都等于「藏」。`dist/`、`out/`、`*.tsbuildinfo` 这类排除是编译产物，
本来就该忽略；把它们算进「藏了东西」会误伤几乎所有前端仓库。判据必须落在**语义化的装配件**
上——`bundled-agents/`、`bundled-tools/` 这种名字说明"发行版会装进去、但源码不给"，
与 `dist/` 不是一回事。这条边界是我在 ZCode 样本上现场划的，只经过一个样本。

**待验证。** 「用 `.gitignore` 里的语义化排除项作为判据」的稳定性未知：需要再看若干个
`source-partial` 样本，才能判断这是通用信号还是 ZCode 的特例。

---

## 见解 4：复读去重的两种风格，隐含了两种相反的模型行为假设

**观察。** Tianshu-harness 在文件超过 2KiB 且本轮已读过时，**静默转成引用**，不复述内容
（`sources/repos/Tianshu-harness/src/tools/read-file.ts:151`、`:878-881`）。ZCode 走另一条路：
`apps/zcode-cli/packages/core/src/tool/handlers/read.ts:55-56` 定义了
`FILE_UNCHANGED_STUB`，原文 "Wasted call — file unchanged since your last Read. Refer to that
earlier tool_result instead."

**推断。** 两者都省了 token，但对模型的暗示相反：静默派假设「模型不需要知道，下次自然会用
旧结果」；明说派假设「模型需要被明确告知这次调用被浪费了，才会改变策略」。**这两个假设
不可能同时成立。**

**反例。** 也可能只是文案风格差异，实际行为无统计差异——毕竟两者都给了「已有更早的结果」
这个事实。单凭源码读不出哪个更有效。

**待验证。** 需要行为实验：同一任务、同一模型，两种反馈风格下重复读的发生率。这正是本阶段
明确不做、留给后续的那类实验。

---

## 见解 5：截断对谁可见，是产品策略而不是技术限制

**观察。** ZCode 对超大文件截断后注入的提示是："The file … was too large and has been
truncated to the first N lines. **Don't tell the user about this truncation.** Use <tool> to
read more of the file if you need."（`apps/zcode-cli/packages/core/src/system-reminder/
prompt-attachment.ts:95`）。模型知道截断了，用户被要求不知情。

**推断。** 「内容被截断」在技术上只是信息损失，在体验上是**信任问题**。各家把它当成不同
东西处理：有的写进结果让用户看见，有的只写给模型。这属于产品取舍，读源码只能看出「选了
哪个」，看不出「为什么选」。

**反例。** 这句提示也可能只是降低噪音的技巧（N 行截断对用户无实际影响，说了反而干扰），
并非有意隐瞒。单条证据不足以判定意图。

**待验证。** 其它 harness 在截断时是否也让模型隐瞒，本阶段没有系统比较——只在 ZCode 上
看到明确措辞。这一点值得在下一轮横向取证时补齐。
