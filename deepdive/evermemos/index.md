# EverMemOS：论文里的 MemScene，代码里的 Cluster

> 对象深拆，2026-09-21。源码 `sources/repos/EverOS`（EverMind-AI/EverOS，commit `5076683ab88d`，2026-09-08），论文 `sources/papers/md/evermemos-a-self-organizing-memory-operating-system-for-structured-long-horizon-reasoning.md`（arXiv 2601.02163，ACL 2026 长文）。
> 状态区分：**代码确实存在** / **文档声称** / **默认启用** / **本项目未验证**。静态读码；GitHub issue #73 原文**未读到**，本文只从代码与配置推断。

## 先修正一个常见假设

很多介绍把它描述成 MongoDB + Elasticsearch + Redis 的堆栈。**本仓库完全没有这三个**。实际是 md-first 三件套：

| 层 | 是什么 | 作用 |
|---|---|---|
| Markdown 文件 | `episodes/`、`atomic_facts/`、`foresights/`、`user.md` 等 | **真值**，一切可由此重建 |
| SQLite（`system.db`） | `memcell` 边界账本、`unprocessed_buffer`、`md_change_state` 队列 | 状态与崩溃恢复 |
| LanceDB（默认）/ Milvus（可选） | episode / fact / foresight / skill / profile 的向量与 BM25 索引 | **派生索引**，可重建 |

这个结构本身值得记：它把"记忆的真值"放在人类可读的文件里，把索引当作可以随时重建的缓存。这是与 mem0（向量库存本体）完全不同的取舍。

## 版本与范围

仓库与论文必须分开记录。范围是 `src/everos/` 下的 `service/`（memorize、search）、`memory/extract/`、`memory/search/`、`infra/persistence/`，以及 `benchmarks/`。未覆盖：外部 PyPI 包 `everalgo` 的算法实现、OME 策略内部。

**一个重要的可读性限制**：边界检测、聚类、agentic 检索的核心算法在外部包 `everalgo.*` 里，本仓库只做编排。也就是说——**EverMemOS 的"核心算法"在开源代码里读不到**。

## 写入路径

`service/memorize.py:memorize()` → `service/_boundary.py:prepare_cells()` → `memory/extract/pipeline/user_memory.py:UserMemoryPipeline.run()`。

1. 按 `session_id` 加锁，归一化格式；
2. `_boundary.py:prepare_cells()` 合并未处理缓冲，调用边界检测切出 `MemCell`，尾部回写缓冲，每个 cell 写一行 SQLite（`memcell_repo.insert_many`）；
3. 每个 cell 生成 episode，追加到 `episodes/episode-<date>.md`；
4. 异步：watchdog 监听 md 变化 → 嵌入 → 同步到向量索引。

`atomic_fact` / `foresight` / `profile` **不在同步路径**，由 OME 策略异步抽取。

## 表示：MemScene 到底在哪里

论文的核心概念之一是 MemScene（场景级聚类）。代码里的情况是：

- `MemCell`【代码确实存在】：SQLite 表存 `memcell_id / session_id / payload_json / timestamp`，本体类型定义在外部包 `everalgo.types`。
- `Profile`【代码确实存在】：`user_profile` 表，字段 `summary / explicit_info_json / implicit_traits_json / profile_timestamp_ms`。
- **MemScene【代码确实：不是一等对象】**：全仓库只有两处提及——`agent_skill.py` 里一个可选的 "MemScene clustering tag" 字段，以及论文同名概念。检索里真正用的是 **`Cluster`**（`everalgo.clustering.Cluster`），策略层 grep "scene/memscene" 零命中。

结论：论文描述的"增量语义聚类 + 场景摘要驱动检索 + 冲突追踪"，在开源实现里**找不到对应结构**。最接近的 cluster 路径只在 `agentic` 方法下使用，而默认方法不是它。

## 检索路径

方法枚举有 `HYBRID`（**默认**）、`LLM_MULTIROUND`、`AGENTIC`、`VECTOR`、`KEYWORD`【默认启用：HYBRID，非 agentic】。

`agentic` 模式（`memory/search/agentic.py:search_episodes_agentic()`）确实同时用了三路：dense 向量、BM25 sparse、跨编码器 rerank（Qwen3-Reranker 风格指令），RRF 融合（`rrf_k=40`）。它是两段的：Round1 用 cluster 域召回后让 LLM 做**充分性判断**，不足则 Round2 用 hybrid 全量重检索，另有 multi-query 改写（3 条）。

默认取回量是**常量写死**的（`DENSE/SPARSE_CANDIDATES=50`、`CLUSTER_TOP_K=10`、`ROUND1_TOP_N=50`、`ROUND1_RERANK_TOP_N=10`、`ROUND2_CAP=40`），没有 env 或配置旋钮。

`agentic` 默认跑不起来：需要配置 rerank（否则 `capabilities.py:64` 直接禁用），而 clustering 在 `default.toml` 里默认关闭。**论文报告 LoCoMo 用的正是 agentic，而开箱默认不是它**——这一点足以解释大部分复现差距。

## 更新与冲突

- 业务记忆**追加式 daily-log**，按 `<date>.md` 追加，无原地覆盖。
- **软失效而非删除**：episode 与 atomic_fact 表都有 `deprecated_by` 列，Reflection 合并后旧行置该值，检索自动排除。
- 真删除只在 cascade 层（md 文件行消失 → 索引行删除）。
- `memcell` 账本不可变，不参与冲突解析。

新事实浮上来的机制是追加 + 时间戳 + 旧条目被 Reflection 标记失效——与 mem0 的"靠文本重新表达"不同，这里有一条显式的失效通道。

## 关于 issue #73（LoCoMo 复现差距）

issue 原文未读到，以下是代码与配置的推断。至少三处**默认配置与论文配置不同**：

1. `benchmarks/configs/locomo.toml` 默认 `methods = "llm_multiround"`，论文用的是 `agentic`（`agentic_scene_rerank`）。
2. benchmark 默认 decider 模型未设时指向 `deepseek/deepseek-v4-flash-0731`，论文发布数字用的是 `qwen3.6-27B`（toml 注释明确要求另设 env 才能复现）。
3. embedding 与 rerank 在 benchmark toml 里未设，代码默认 `None`；论文用的是 Qwen3-Embedding-4B / Qwen3-Reranker-4B。

Backbone 默认 `gpt-4.1-mini` 与论文一致。所以"默认配置 ≠ 论文配置"成立，但"38.38% 是否可作为对等证据"仍不成立——它只跑了 10 段对话中的 1 段。

**顺带解决了一个长期疑问**：LoCoMo 常被引用为 1,540 题，而论文全集是 7,512 题。本仓库的 adapter 说明了来源——`benchmarks/adapters/locomo.py` 读取的文件含 1,986 题，排除对抗类 category 5 的 446 题后正好 1,540 题（282 多跳 + 321 时间 + 96 开放域 + 841 单跳）。题量口径由此可知，但仓库内注释同时出现 1986 与 2432 两个数，具体数据文件口径未验证。

## 覆盖缺口

1. `everalgo` 包内部（边界检测、MaxSim、rerank 融合）不可读。
2. Profile 抽取策略内部——论文声称的"场景摘要驱动 + 冲突追踪"**未验证**是否存在。
3. `default_ome.toml` 中各策略的默认开关未逐行核对。
4. `benchmarks/data/` 为空，未拿到实际评测数据文件。
5. GitHub issue #73 原文未读。
6. Milvus 后端未实际启动验证。

## 为什么值得深拆

它同时提供了两个有价值的对照：**真值放在 Markdown、索引可重建**这一工程选择，以及**论文概念与开源实现的落差**（MemScene 不是一等对象、默认方法不是论文方法、核心算法在闭源包里）。后者是本项目反复强调的"文档承诺 ≠ 代码存在 ≠ 默认启用"最完整的实例。

## 相关

- [记忆横评对照](../../analysis/memory-benchmark-crossreview-2026-09.md)：92.32% 与复现差距的处理。
- [Mem0](../mem0/index.md)：同样是"追加 + 让新事实浮上来"，机制却不同。
- [论文简介卡片](../../analysis/paper-digests-2026-09.md)：2601.02163 的定位与限制。
