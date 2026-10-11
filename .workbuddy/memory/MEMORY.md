# 会话记忆入口

- 项目入口：[README](../../README.md)
- 对象研究：[Deepdive](../../deepdive/README.md)
- 问题研究：[Analysis](../../analysis/README.md)
- 主题入口：[Domain](../../domain/index.md)
- 2026-09-20 结构调整：[架构研究](../../analysis/knowledge-architecture-2026-09-20.md)、[决定记录](../../dialogue/2026-09-20-focused-research-structure.md)
- 早期经过：[Dialogue](../../dialogue/README.md)

- 运行主题与教材路线：[主题](../../domain/agent-runtime/index.md)、[章节提案](../../analysis/book-design.md)、[版本管理决定](../../dialogue/2026-09-20-runtime-theme-and-git.md)。

- 记忆横评与分类（2026-09-21）：[横评对照](../../analysis/memory-benchmark-crossreview-2026-09.md)、[记忆分类主题](../../domain/memory-taxonomy/index.md)、[候选清单](../../analysis/landscape/memory-object-candidates-2026-09.md)、[决定记录](../../dialogue/2026-09-21-memory-benchmarks-and-layout.md)。

- 论文库（2026-09-24 更新）：`sources/papers/` 按表示形式分 `pdf/ md/ assets/`（`json/` 已取消）；**文件名 = `<id>.<简称>`**（如 `arxiv-2502.12110v11.A-Mem`；`id` 含登记处、编号与版本，是永久身份）。数据查 index.csv（`id, name, keywords, date`），规则与字段读法见 papers/AGENTS.md，历史见 CHANGELOG.md。2026-09-22 的旧方案（标题 slug 作文件名、`index.json`、`json/` 目录、`kinds`/`tags` 分列）已被本次改版取代；[决定记录](../../dialogue/2026-09-22-papers-layout-and-naming.md) 保留当时的理由。

- doc-model 分类（2026-10-05）：`domain/repo-context/01docsclassify` 已推进到 v5，讨论稿在 [v5/Space_Bunny/](../../domain/repo-context/01docsclassify/v5/Space_Bunny/README.md)（README／推导过程／研究报告／命名方案 + 两个可复现实测脚本）。要点：分类改用**六根正交轴**（消费时点／事实类型／执行点／可寻址性／生命周期／变更频率）替代按流程的清单；「哪个文件被加载」是数月可变的产品状态（Claude Code 读 `AGENTS.md` 是 fallback 非 merge），**分类学须按角色引用、不按文件名**。实测基线：上电集 778 tokens、按需层 9856、中文 token 成本高于英文。

- **取证纪律（2026-10-05 确立，补充 00 阶段那条）**：00 阶段是「不递归导致假阴性」，本轮遇到镜像——**残缺快照导致假阳性**。`sources/repos/` 的 checkout 可能不完整（`Tianshu-harness` 的 `docs/docs.json` 自称 1034 篇而磁盘只有 150 篇），用它算死链率会得到 86.6% 这种极有说服力的错误数字。凡用链接存活率、覆盖率等**分母来自被测对象自身**的指标，必须先独立验证分母。另外 `sources/repos/` 下 18 仓**无自身 `.git`**，在其中跑 git 会向上冒到本项目主仓，子仓版本只以 `index.csv` 的 `snapshot` 为准。
