# memU：把判断留在 Agent 侧的极简记忆服务

> 对象深拆，2026-09-21。源码 `sources/repos/memU`（NevaMind-AI/memU，commit `08e1ed4cdf4c`，2026-09-10，打包下载不含 `.git`）。memU 无论文，因此本文以代码为准，并专门记录 README/CHANGELOG 与代码不同步的地方。
> 状态区分：**代码确实存在** / **文档或 README 声称** / **默认启用** / **本项目未验证**。静态读码，未运行。

## 版本与范围

memU 在 2026 年内重构过一次：README 从"三层记忆树 + RAG/LLM 双检索"改写为"Personal memory, stored as Wiki"，代码也相应地重命名了核心概念。**引用 memU 的任何机制描述都必须带上日期**，这是本文最想留下的提醒。

范围集中在 `src/memu/app/`（service、agentic、settings）、`src/memu/database/models.py`、`src/memu/vector.py`。未覆盖：`hosts/` 下各宿主适配的细节、postgres/pgvector 路径。

## 整体地图

核心只有三个类（`database/models.py`）：

| 类 | 是什么 | 对应旧说法 |
|---|---|---|
| `Resource` | 仅有 `url / caption / embedding` | 旧 Resource Layer（多模态原始仓库） |
| `RecallFile` | 一份 Markdown 正文，带 `track`（`memory` / `skill`） | 旧 MemoryCategory Layer（聚合文本单元） |
| `RecallFileSegment` | 嵌入与检索的最小单元 | 旧 MemoryItem Layer（离散记忆单元） |

旧的 `MemoryItem` / `MemoryCategory` 类名在代码中已不存在（ADR 0006，2026-06-30 改名为 `RecallEntry`/`RecallFile`，`RecallEntry` 之后也消失了）。**"三层"在代码里收敛成了两张表 + 一个 track 字段。**

服务入口 `MemoryService`（`app/service.py:24`，约 96 行）+ `AgenticMixin`（`app/agentic.py:150`，约 669 行）+ `cosine_topk`（`vector.py:23`）。README 说的"核心逻辑只有 500 行"，实测这三个文件约 842 行——来源是 CHANGELOG 里 "pitch memU as a 500-line memory system (#488)" 的营销口径，**不是度量**【文档声称】。

## 写入路径：服务里没有 LLM 抽取

`commit_results`（`agentic.py:343`）是唯一写入入口，注释自己写着 "it runs no ingest/preprocess/LLM steps — just create-or-update straight into storage"。全仓库 grep 不到 `chat.completions`、`LLMGateway`，`env.py:173` 直接写 "There is no LLM in memU"【代码确实存在】。

那抽取是谁做的？**外部 coding agent。** `hosts/bridging/pipeline.py` 的 `prepare()` 把会话切片成 job 文件，`commit()` 读回 agent 落盘的 Markdown 再入库；中间那一步由外部 agent 执行 `instructions.py` 里的模板（`MEMORY_JOB_TEMPLATE` / `SKILL_JOB_TEMPLATE`，开头是 "You are the self-evolve pass…"）【代码确实存在，但执行者不在本仓库】。

这是一个真正不同的架构选择：**memU 把"什么值得记"的判断整个委托出去，自己只负责存、嵌、检索。** 它使 memU 极轻，也让记忆质量完全取决于调用方的 agent——而这部分逻辑不在仓库里，本项目未验证。

写入是幂等 upsert：新文件 `get_or_create`，旧文件更新 content；`_plan_segments` 做 drop-and-add diff，未变文本不重嵌。

## 检索路径

唯一机制 `progressive_retrieve`（`agentic.py:187`），查询嵌入一次后顺序三步：

1. `_recall_segments`：在 `RecallFileSegment` 上按余弦取 `file.top_k`（默认 5）；
2. `_collect_files`：把命中段 roll-up 到所属 `RecallFile`（取段最高分，**不再排序**）；
3. `_recall_resources`：`track="workspace"` 的 `Resource` 按余弦取 `resource.top_k`（默认 5）。

全程无模型、无路由、无充分性判断。另有 `list_all_recall_files`（`agentic.py:159`）纯枚举整库 wiki，不需要嵌入。

旧 README 提到的"LLM 直接读文件"这条检索，在当前代码里对应的是**外部 agent 拿到返回的 `path` 后自己读磁盘**（`retrieval.py:_shape_for_agent`），不在服务内。`hosts/codex/INSTALL.md:306` 仍保留着对已移除路径的指称——文档与代码不同步的一处实证。

## 更新、合并与失效

- **无合并**：多个条目不会自动合并，是否 patch 由外部 agent 在指令模板里决定。
- **无 consolidation、无自动演化**：代码里没有合并或重聚类函数。
- **无失效与衰减**：`models.py` 没有 `salience` / `reinforcement` / `expiry` 字段。旧 1.4.0 CHANGELOG 声称的 "salience-aware memory with reinforcement tracking" 在当前代码中已不存在【文档声称，代码已移除】。
- ADR 0006 自己记录了缺口：skill track 是 append/merge-only，源文件删除时 skill 不随之收缩（provenance gap，deferred）。

所以 memU 的记忆是"追加 + 幂等更新 + 段重建"，**演化完全靠 agent 手动 patch**。

## 存储与可运行性

存储三后端：`inmemory`（默认）/ `sqlite` / `postgres`，CLI 默认 `sqlite://~/.memu/memu.sqlite3`。向量索引在无 pgvector 时暴力扫描。

嵌入五个 provider（openai 默认 `text-embedding-3-small`、jina、voyage、doubao、openrouter），**全部远程**——存储可以完全本地，但嵌入必须联网且有 key，因此端到端不可离线【代码确实存在】。

## 覆盖缺口

1. 多模态原始仓库：当前 `Resource` 无 blob 字段，多模态嵌入仅 Doubao 且未被默认写入路径调用；旧 README 的"多模态原始仓库"在当前代码中**未验证存在**（推断已剥离）。
2. ADR 0007（三条独立 memory line + Node/Edge + BM25 混合 + graph）状态为 Proposed，代码里没有 `memu.lines` 包，仍是纯余弦、无 BM25、无图。**README 的架构方向领先于代码。**
3. 外部 agent 的抽取行为不在本仓库，memU 不保证其幂等与质量——未验证。
4. postgres/pgvector 路径未验证（测试按 inmemory + sqlite 跑）。
5. 2.0.0-beta.0 CHANGELOG 列出的 `llm`/`vlm` gateway、`preprocess`、`blob` 在当前 `src` 下均无对应包。

## 为什么值得深拆

它代表与 mem0 完全相反的一端：**mem0 把智能放进服务（抽取），memU 把智能留给调用方**。两者在"谁来判定什么值得记"这个根本问题上给出了相反答案，而 memU 的极简使这个分歧变得可检查：如果记忆质量差，问题清晰地落在调用方 agent 身上，而不是落在框架内部某个不可见的抽取步骤上。

同时它也是一个诚实的反面教材：**当 README 与代码不同步时，只有读代码才知道系统真正在做什么**——本文档记录的三处不一致（500 行、LLM 路由检索、salience）都是这种检查的产物。

## 相关

- [Mem0](../mem0/index.md)：同一个问题的相反答案。
- [Memory 工程选择](../../analysis/memory-engineering-selection.md)：谁决定存、取、弃。
- [记忆分类：程序性记忆](../../domain/memory-taxonomy/cognitive-classes.md)：memU 的 skill track 落在哪一层。
