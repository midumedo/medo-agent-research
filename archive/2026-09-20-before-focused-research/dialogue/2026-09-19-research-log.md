# 历史研究日志 · 2026-09-19

> 此记录从旧会话记忆迁出，保留当时的推演与判断。它不是现行规则或已核实事实；当前认识见 [领域入口](../domain/index.md)，本轮更正见 [项目审查](../analysis/project-review-2026-09-20.md)。下方历史内容保持原文。

---

# 2026-09-19

## 《Memory 与上下文工程》教材立项：目标文件深度调研与分析

- 输入：`D:\workspace\memory\目标.md`（用户的研究方向与教材目标清单）
- 产出：`D:\workspace\memory\目标-深度调研与分析报告.md`

### 用户目标要点
- 研究方向：harness 工程、上下文工程、memory
- 想写一本面向已懂 LLM/Agent 读者的**进阶教材**，重点工程化 + 记忆深度讲解
- 教学法主张：先找共性、讲透核心思路，再各点深入

### 本轮关键发现（后续写作的事实底座）
1. **纠错（重要）**：`memgit` 是真实独立项目 —— memgit.dev / github.com/code4161/memgit，"Git for AI Memory"，本地优先、SHA-256 内容寻址、TOON 明文格式、MCP。核心机制：8 类记忆类型 + 3 级优先级、supersede 取代而非覆盖、checkpoint、core seed/sync/heal 自我维护、eval 用冻结集测召回稳定性。此前工作区内的调研（20260919-201314-e52b6696）判定"不存在/是 Letta Context Repositories 别称"，是错的。另有 xbasset/memgit、subho004/mem-git-agent 需区分。
2. **everOS = EverMemOS**（evermind.ai），核心抽象 MemCell = (Episode, AtomicFacts, Foresight, Metadata)，含独有的"前瞻记忆"。LoCoMo 92.32%，横评中唯一超过 Full-context。
3. **tianshu = 天枢**（huiliyi37/Tianshu-harness，TS，原代号 Rivet），CVM 认知虚拟机 + Stigmergy 信息素自衰减记忆 + 前缀缓存引擎（95–99%）。≠ DeepSeek 官方 harness（dsh）。
4. **Pi** 已 10 万+ star，被 OpenClaw、MiniMax Code 用作底层 SDK —— 清单里的产品不是平级，有依赖层次。
5. **Letta** 主分支 2026-08-15 移除 V1 API server（约 36.7 万行），代码现集中在 `letta-code`，引用源码需指向新仓库。
6. **Claude Code 压缩阈值**：不是固定百分比，而是 `有效窗口 = 窗口 − min(最大输出, 20000)`，`阈值 = 有效窗口 − 13000`；200K → 167K（占有效窗口 ~92.8%，占完整窗口 ~83.5%）。流传的"92%"分母是有效窗口。
7. **评测系统性不可信**：LoCoMo 审计 1540 题 99 处错误（理论上限 ~93.6%）；judge 接受 62.81% 的错误但沾边答案；厂商口径 vs 第三方复现差距可达 20 分（mem0 93.4% vs 73.8%）；基准规模能塞进上下文窗口。新一代：LoCoMo-Refined、LongMemEval-V2（LAFS 准确率+延迟联合评分）、BEAM（1M/10M，设计上不饱和）。

### 提炼出的教材主线（共性骨架）
- 第一原理：**Context 是预算，不是仓库**（成本 4×/7×/25K vs 7K；效果 lost-in-the-middle；延迟 115K→1.6K）
- 六段循环：产生 → 写入 → 治理 → 召回 → 注入 →（旁路：压缩 / 隔离）
- 四层金字塔：常驻 / 热 / 温 / 冷；**分水岭是"谁决定什么在常驻层"**（系统 / Agent / 人显式 schema / 后台笔记）
- 差异化章节机会：**程序性记忆（技能库）**被 47 作者 taxonomy 点名为"基准影响最大、生产工具最少"的一层，而 Hermes / Pi / Letta / Codex 都已工程化实现（Voyager 技能库带来 15.3× 提速）
- 另一个差异化章节：**缓存友好设计**（Pi 99.93% 命中率、成本差 50×；可归纳为 6 条设计纪律）

### 待办
- [ ] 建立一手核实清单（官方 README + 关键源码本地存档）
- [ ] 补空白：Kimi Code / ZCode / MiniMax Code 上下文机制、DeepSeek 官方 dsh 源码级机制
- [ ] 确定配套代码技术栈（TS 或 Python）

---

## 第二轮（用户要求放慢节奏，先做综述）

用户反馈：不要一次性全给；先调研综述，看综述都写了哪些；**不要源码堆砌**（要看源码读者自己问 AI 即可）；要的是"有 AI 味儿、适用于 AI 时代的教材"，不是传统厚教材。要求先把论文 PDF 解析成 Markdown 本地化复用。

### 已建成：refs/ 论文管线
- `refs/download_arxiv.py`：按 watchlist.txt 批量下载 PDF + 抓 abs 页元数据 → `refs/pdf/`、`refs/meta.json`
- `refs/pdf2md.py`：pymupdf4llm 批量转 Markdown → `refs/md/`，带 YAML 头（标题/作者/日期/链接）
- `refs/综述索引.md`：七篇综述的核实结果、对原表 4 处修正、阅读顺序、复用命令
- 解析器装在隔离 venv：`C:\Users\37071\.workbuddy\binaries\python\envs\default`（pymupdf4llm 1.28.2）

### 七篇综述核实结果（全部下载+解析成功）
| 编号 | 真实标题 | v1 | 分类轴 |
|---|---|---|---|
| 2404.13501 | A Survey on the Memory Mechanism of LLM based Agents | 2024-04-21 | 来源 × 形式 × 操作 |
| 2505.00675 | Rethinking Memory in LLM based Agents: Representations, Operations, and Emerging Topics | 2025-05-01 | parametric/contextual + 六大操作 |
| 2512.13564 | Memory in the Age of AI Agents（48 作者） | 2025-12-15 | Forms × Functions × Dynamics |
| 2602.06052 | A Survey of Agent Memory in the Second Half: Towards Self-Evolving and Long-Horizon Agents（60 作者） | 2026-01-14 | Substrate × Cognitive × Subject |
| 2603.07670 | Memory for Autonomous LLM Agents（**单作者** Du Pengfei） | 2026-03-08 | write-manage-read + 三维 taxonomy |
| 2606.06448 | Agent Memory: Characterization and System Implications（**短文** 415 行） | 2026-06-04 | 系统四轴 + phase profiling |
| 2607.16848 | Beyond Memory Leaderboards（我补充） | 2026-07-18 | 评测协议视角 |

### 对用户原表的修正
1. 2602.06052 标题不是「Rethinking Memory Mechanisms of Foundation Agents...」，v1 是 2026-01-14 不是 Feb
2. 2603.07670 是单作者，非「美国团队」；有价值的在 §7 Engineering Realities、§8 Positioning Relative to Prior Surveys
3. 2404.13501 主干是 来源×形式×操作，长短期只在「认知心理学」一节出现
4. 2505.00675 六操作是 Consolidation/Updating/Indexing/Forgetting/Retrieval/**Condensation**（用户漏了 Indexing 与 Condensation）

### 下一步（等用户确认）
按索引里的顺序逐篇精读，先 2512.13564 立边界 → 2603.07670 建回路，边读边抽"共性骨架"的证据，而不是一次性写完教材。

---

## 第三轮：重构为 papers/ 知识库 + 渐进披露 README

用户要求：建立专门的 papers 文件夹，下面分 综述/，写 README 介绍论文，**符合渐进披露原则**。

- 已把 `refs/` 整体迁移为 `papers/`：`综述/`（md）、`pdf/`、`meta.json`、`nav.json`、`watchlist.txt`、`_scripts/`、`logs/`；`refs/` 已移除
- 新增 `papers/nav.json`：每篇论文的导航卡数据（一句话定位 / 分类轴 / 必读 / 可跳过 / 盲区 / 对应教材章节），由 `pdf2md.py` 渲染进每篇 md 头部
- `pdf2md.py` 重写：BASE 改为上级目录、支持 `--out <分类>`、渲染导航卡
- `papers/README.md`（L0 入口）+ `papers/综述/README.md`（5 层渐进披露：15分钟最短路径 → 一览表含"什么时候跳过" → 三条路径 → 逐篇卡片 → 按问题索引 → **七篇集体盲区**）
- 第 5 层"集体盲区"是教材的立身之地：缓存友好性、Harness 作为记忆系统、常驻层预算、程序性记忆工程范式、记忆与版本控制、评测协议问题
