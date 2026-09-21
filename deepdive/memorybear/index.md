# MemoryBear：图优先、带遗忘曲线的商用记忆引擎

> 对象深拆，2026-09-21。源码 `sources/repos/MemoryBear`（SuanmoSuanyangTechnology/MemoryBear，即"红熊 AI / RedBear AI"，commit `c32b937f1ed0`，2026-09-16，打包下载不含 `.git`，3101 个文件）。
> 状态区分：**代码确实存在** / **文档或 README 声称** / **默认启用** / **本项目未验证**。仓库是全栈（后端 + 前端 + 沙箱 + 多个兄弟服务），本文只读了后端 `api/app`，静态读码未运行。

## 版本与范围

范围：`api/app/core/memory/`（pipelines / storage_services / read_services / models / enums）及其外层 controller / service / repository。**未读**：前端 `web/`、兄弟服务 `mem-knowledge`、`gateway-service`、`identity-service`、`packages/`、部署 `e2b-infra` 与 `sandbox/`。

相关 arXiv 有两篇（2603.22306 多模态情感记忆、2604.07017 A-MBER 基准），本地未入库，本文只在代码里找间接线索。

## 整体架构

多底座，且**四个底座全部是外部依赖**（README 要求另行拉镜像，docker-compose 里不含它们）：

| 底座 | 角色 |
|---|---|
| Neo4j（默认存储） | 知识图全量：实体、关系、陈述句、分块、对话 |
| PostgreSQL | 用户/租户/配置/审计/遗忘日志 |
| Redis | 缓存 + Celery broker/backend |
| Elasticsearch | provider 存在；默认 NEO4J 路径下检索在 Neo4j 内完成 |

`StorageType = NEO4J | RAG`，默认 `NEO4J`【默认启用】。ES 在实时检索中的真实占比**未验证**。

## 写入路径

`controllers/memory_controller.py:48` `POST /write` → `WritePipeline.run`，流程是：剪枝(LLM) → 分块 → 萃取(LLM 编排器) → 建图 + 去重 → 写 Neo4j → 聚类(Celery) → 摘要。

抽取由 `NewExtractionOrchestrator` 编排两个步骤：`StatementTemporalExtractionStep`（陈述句 + 时间）与 `TripletExtractionStep`（实体/关系三元组），都通过 `llm_client.call_structured` 拿结构化 JSON。提示词是 jinja2 模板。模型来自配置，**不硬编码**。

记忆类型不是我们原先猜的 profile/event/relation，实际是：

- `MemoryDisplayType`：`profile / fact / entity / summary / file / unknown`
- 陈述句类型：`FACT / OPINION / PREDICTION / SUGGESTION`
- 实体画像字段：`core_facts / traits / relations / goals / interests / beliefs_or_stances / anchors / events`
- 三元组谓词 13 类：`ALIAS_OF / IS_A / LOCATED_IN / OWNS / PREFERS` 等

## "时序知识图谱"这个猜测成立吗

**部分成立，需要修正。**

成立的部分：节点与边确实带时间字段并落库——`StatementNode` 有 `valid_at / invalid_at / dialog_at / created_at`，`EntityEntityEdge` 同样有 `valid_at / invalid_at`，`graph_saver.py` 写入时带上。还有专门的 `TemporalInfo`（STATIC / DYNAMIC / ATEMPORAL）。这是一套真的"有效时间"语义，与 Graphiti 的双时间模型在同一思路上。

需要修正的部分：`Neo4jStorageStrategy.TIMELINE` **只是一个枚举**，全仓库找不到任何按它分支的实现。所以"时序"体现在节点字段上，而不是一条独立的时序存储策略。

冲突与过期：关系是带有效期的，检索侧可按当前时间过滤（具体是否默认启用**未验证**）；逻辑冲突检测走反思引擎，检测后**置 `unresolved_flag` 标记待人工复核，不自动覆盖**——这与多数系统"直接覆盖或并存"都不同。

## 遗忘：ACT-R 幂律曲线

这是它对外宣传的特色之一，**代码里确实有实现**（`forgetting_engine/actr_calculator.py:30`）：

```python
exponent = -self.forgetting_rate * time_since_last / bla_sum
activation = self.offset + (1 - self.offset) * math.exp(exponent)
```

`ForgetService`（`forget_service.py:34`）做**软删除**（置 `delete_at`，可恢复），受 `memory_limit` 配额驱动：核心池（Chunk / Statement / ExtractedEntity）与辅助池按 `created_at` 与 ACT-R 激活值排序淘汰，写审计日志。调度由 Celery 周期任务 `scan_forget_candidates` → `do_forget_for_user` 完成。

是否出厂默认开启取决于 `memory_limit > 0`，**未验证**出厂值。

## 自反思

`reflection_engine/self_reflexion.py` 提供 `ReflectionBaseline.TIME / FACT / HYBRID`、`ReflectionRange.PARTIAL/ALL`、`iteration_period`（默认 `"3"` 小时）。但 `enabled: bool = False`——**默认关闭**【默认启用：否】。周期扫描任务 `scan_layer2_reflection` 存在，实际是否运行取决于配置。

注意这与 README 的"每日反思"措辞不一致：代码默认周期是 3 小时且默认关闭，以配置为准。

## 检索路径

`core/memory/src/search.py` 的 `run_hybrid_search` 按 `search_type` 并发跑 keyword（图遍历/全文）、embedding（向量），另有 temporal 变体。融合分两阶段：

```python
content_score = alpha * bm25_norm + (1 - alpha) * emb_norm      # 初筛，取 Top-K*3
memory_strength = importance * (1 + activation_val * activation_boost_factor)
```

即**内容相关性初筛，再用 ACT-R 激活值（含时间衰减）重排**。这与"遗忘曲线"共用同一套激活值——记忆强度既决定淘汰顺序，也决定检索排序，是这个系统里少见的一致性设计。

`apply_reranker_placeholder` 看起来是占位/未实装；`use_llm_rerank` 与 `use_forgetting_rerank` 默认 `False`。

## 可运行性

四个底座 + LLM/embedding API key 全都要，**没有纯本地可跑路径**。

一个需要修正的说法：外部资料称它依赖自研模型 OpenBear / CodeBear，**代码里 grep 不到这两个名字**。模型是可插拔 provider（OpenAI 兼容 / DashScope / Bedrock），唯一红熊自有的是 `SPEEDBEAR_BASE_URL`，用于密钥解析与租户绑定，不参与记忆算法。所以"因依赖自研模型而不可复现"这个说法**在本仓库里没有代码支撑**。

## 覆盖缺口

1. `TIMELINE` 存储策略是否真有独立代码路径——未确认。
2. 检索时是否默认按 `valid_at / invalid_at` 过滤——字段已落库，过滤逻辑未读。
3. ES 在实时检索中的占比、RAG 存储路径是否线上默认——未验证。
4. 遗忘与反思的出厂默认值（配置种子/迁移）——未核实。
5. 前端与兄弟服务、沙箱——未读。
6. 两篇 arXiv 与代码的对应关系——只有间接线索（`extract_emotion`、`PerceptualNode`），未坐实。

## 为什么值得深拆

它是本轮唯一**真正实现遗忘曲线**的对象——多数系统的"时间"只用于排序或失效标记，MemoryBear 把记忆强度做成了贯穿淘汰与检索的同一个量。同时它也是唯一用图承载有效时间语义、且对冲突采取"标记待人工复核"而非自动处理的系统。这两点都提供了别处看不到的机制样本。

## 相关

- [记忆分类：情景与语义](../../domain/memory-taxonomy/cognitive-classes.md)：陈述句 + 三元组属于哪一层。
- [Memory 工程选择](../../analysis/memory-engineering-selection.md)：写入成本与淘汰策略。
- [候选对象清单](../../analysis/landscape/memory-object-candidates-2026-09.md)：用户此前"MemoryBear 应属时序图派"的猜测及其修正。
