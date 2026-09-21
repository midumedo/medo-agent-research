# Mem0：抽取-更新派的当前形态

> 对象深拆，2026-09-21。源码 `sources/repos/mem0`（mem0ai/mem0，commit `a39a802bbc93`，2026-09-18，打包下载不含 `.git`），论文 `sources/papers/frameworks/2504.19413.md`（arXiv 2504.19413v1）。
> 全部结论区分四种状态：**代码确实存在** / **文档或 README 声称** / **默认启用** / **本项目未验证**。静态读码，没有运行框架。

## 版本与范围

仓库与论文是两件事：论文是 2025-04 的 v1，代码是 2026-09 的主分支。官方 2026 年宣称的"single-pass ADD-only"新算法与论文描述的"抽取 + UPDATE/DELETE 冲突消解"是两个阶段，**本轮确认代码处于前者**。

范围集中在 `mem0/memory/main.py` 的写入与检索路径，以及 `mem0/configs/prompts.py`、`mem0/utils/scoring.py`。未覆盖：向量库各后端实现、图模块（OSS 不存在）、托管平台客户端。

## 整体地图

核心包 `mem0/`，主类 `Memory`（`main.py:487`）与 `AsyncMemory`（`main.py:2172`）并存，公开 API 一致。三个存储同时参与：

| 存储 | 存什么 | 写入时机 |
|---|---|---|
| `vector_store`（默认 Qdrant） | 抽取出的记忆本体，payload 含 `data / hash / created_at / updated_at / attributed_to` | `add()` 同步写入 |
| `db`（SQLite，默认 `~/.mem0/history.db`） | 消息原文与 ADD/UPDATE/DELETE 事件日志 | `add()` 同步写入 |
| `entity_store` | 实体向量（同一向量库的独立 collection，lazy 初始化） | `add()` 末段批量写入 |

## 写入路径

`Memory.add()`（`main.py:760`）→ `_add_to_vector_store()`（`main.py:879`）。默认 `infer=True` 时进入代码里标注为 `=== V3 PHASED BATCH PIPELINE ===` 的管线（`main.py:916`）。

事实抽取只用**一次**模型调用（`main.py:940-961`），提示词是 `ADDITIVE_EXTRACTION_PROMPT`（`configs/prompts.py:468`），首句即 "Your sole operation is ADD"——【代码确实存在】。

**最关键的一点：写入路径没有冲突治理。** 唯一与"已存在"相关的判断是精确哈希去重：

```python
mem_hash = hashlib.md5(text.encode()).hexdigest()
if mem_hash in existing_hashes or mem_hash in seen_hashes:
    logger.debug(f"Skipping duplicate memory (hash match): {text[:50]}")
    continue
```

也就是说，语义等价但措辞不同的新旧事实**不会被消解**，两条都留下。没有失效标记、没有合并、没有基于冲突的删除【代码确实存在：没有】。

`update()`（`main.py:1815`）与 `delete()`（`main.py:1869`）**确实存在且可用**，但它们是外部显式调用的 API，不参与 `add()` 的自动路径。这一点必须说清：把"mem0 有 update/delete"当成"mem0 会自动处理冲突"是误读。

## 新事实怎样浮上来

这是 ADD-only 设计的必然后果，代码里给出的答案比想象中弱：

- `created_at` / `updated_at` 写进了 payload，但**排序不使用时间衰减**——`score_and_rank` 里没有时间项【代码确实存在：无时间衰减】。
- 时间感知排序是平台专属：OSS 调 `search(reference_date=...)` 直接抛错（"Platform-only temporal parameter"，`main.py:1421`）。
- 唯一的机制是**把变化写进事实文本本身**，靠提示词引导（例如"User switched from almond milk to oat milk lattes"，`prompts.py:612-620`），让新事实在语义与关键词上自然胜出。另有 `expiration_date` 硬过期过滤（`main.py:442-451`）在 OSS 可用。

这解释了一个工程后果：**更正依赖于重新抽取出一条能压过旧事实的文本**，而不是依赖于冲突检测。抽取没抽到，旧事实就继续生效。

## 检索路径

`Memory.search()`（`main.py:1379`），默认 `top_k=20`、`threshold=0.1`、`rerank=False`。三路并行后融合（`main.py:1640-1687`）：语义向量（over-fetch 到 `max(top_k*4, 60)`）+ BM25 关键词 + 实体 boost。

融合公式（`utils/scoring.py:60` `score_and_rank`）：

```python
max_possible = 1.0
if has_bm25:   max_possible += 1.0
if has_entity: max_possible += ENTITY_BOOST_WEIGHT   # 0.5
raw_combined = semantic_score + bm25_score + entity_boost
combined = min(raw_combined / max_possible, 1.0)
```

实体 boost 只在相似度 ≥0.5 时生效，权重上限 0.5。Rerank 默认关闭，需配置 `config.reranker` 才有【默认启用：否】。

## 与论文、与文档的差距

| 维度 | 论文 2504.19413（2025） | 本代码（2026-09） | 状态 |
|---|---|---|---|
| 写入语义 | 抽取 + UPDATE/DELETE 冲突消解 | `add()` 为 ADD-only，仅哈希去重 | 代码确实存在；论文描述已过时 |
| `Mem0^g` 图记忆 | 完整知识图（抽取 + 冲突检测） | **OSS 中无图模块** | 文档声称与代码矛盾 |
| 多路检索 | 论文未强调 BM25 / 实体融合 | 语义 + BM25 + 实体融合 | 代码确实存在（2026 新增） |
| 时间推理 | 时间戳文本 | OSS 仅 `expiration_date`；`reference_date` 抛错 | 平台专属 |
| 论文 Table 1/2 的分数与延迟 | J=66.88、p50=0.708s 等 | 源码中**找不到任何对应常量或计算依据** | 代码确实存在：否 |

图记忆值得单独说明：`mem0/AGENTS.md` 声称存在 `graphs/` 目录与四个图后端（Neo4j / Memgraph / Kuzu / Apache AGE），但本提交里该目录不存在、`MemoryConfig` 没有 `graph` 字段、全仓库没有 `enable_graph` 标识符，只在 `exceptions.py` 留了一个 kuzu 依赖缺失的错误桩。**README 与代码在这件事上是矛盾的**，引用"mem0 有图记忆"时必须区分 OSS 与托管平台。

另外，论文遗留的 `DEFAULT_UPDATE_MEMORY_PROMPT` 仍在 `prompts.py:176`，但 `add()` 不再调用它【代码确实存在但非默认路径】——这正是"新旧两个阶段在同一份代码里留下痕迹"的证据。

## 覆盖缺口

1. 图模块究竟是被删除还是只在平台专有仓库——未验证（本地不含 `.git`，无法追溯历史）。
2. Qdrant 默认连接配置未读，纯本地零配置是否可跑存疑。
3. `db`（SQLite）的表结构与 `is_deleted` 是否在检索时用于软失效——未读。
4. Reranker 各 provider 的打分逻辑、异步与同步路径的逐行差异——未读。
5. BM25 能力对哪些向量库后端可用——只知不支持时会退化为纯语义，未逐库确认。

## 为什么值得深拆

它是"抽取-更新派"事实上的默认参照，而且**代码比论文更能说明这个流派当前的实际状态**：写入是一次抽取 + 无冲突治理的追加，智能程度集中在提示词而非存储结构。对本项目最有用的一点是——它把"记忆的更正"问题完整地留给了抽取步骤，这使得它成为检验"抽取错了怎么办"这个具体失败的最小案例。

## 相关

- [记忆横评对照)(../../analysis/memory-benchmark-crossreview-2026-09.md)：Mem0 的自报分数与协议问题。
- [Memory 工程选择)(../../analysis/memory-engineering-selection.md)：保留材料还是提前理解。
- [论文简介卡片)(../../analysis/paper-digests-2026-09.md)：2504.19413 的定位与限制。
