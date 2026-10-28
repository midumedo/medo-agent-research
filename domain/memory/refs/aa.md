**Towards a Systems Foundation for Agentic Skills（arXiv:2608.29596，Google，2026-08）**
这篇提出了**agentic skills 的统一六元组形式化** $s = (\mathcal{A}, \mathcal{I}, \mathcal{C}, \mathcal{T}, \pi, \mathcal{E})$——activation condition / procedural instructions / constraints / tools / execution policy / state transitions L9-L10】。它定义了区分 skill 与相邻概念（prompt、atomic tool、workflow、episodic memory）的三条判据：封装模块化、late-binding 动态调用、程序性状态变换 L11-L12】。**它实际上是 procedural memory 这一支的独立深化**——当 procedural memory 从记忆分类学中独立出来成为“技能系统”这个一等研究对象时，记忆综述的覆盖范围就需要重新审视。
**Microsoft AI Memory Research Group 的系列产出（2606–2608）**
这个组在 2026 年下半年集中产出了多篇相关论文：**TriggerBench**（2606，prospective memory——前瞻记忆的专项基准）、**MESA**（2608，task-adaptive multi-structure evidence selection）、**SkillHEX**（2608，假设驱动的自主探索与利用）、**"Beyond Semantic Organization: Memory as Execution State Management"**（2606）。这个系列代表了一个明确的工业视角：**记忆研究正在从“语义组织”转向“执行状态管理”**——后者是十篇综述中只有 Du（write-manage-read 循环）部分覆盖的维度。
**Memory as Metabolism: A Design for Companion Knowledge Systems（arXiv:2604.12034，2026-04）**
这篇提出了一个三层治理框架：interaction/workflow（collect, annotate, organize, revisit）、representation/retrieval（storage format, object types, retrieval index）、retention/governance（decay, gravity, consolidation, audit）。它的独特定位是**针对 companion 场景的窄领域治理设计**——专门处理单用户知识 wiki 中的 entrenchment 失败模式。
---
## 第二部分：为什么 2606–2610 没有新的全景综述——结构原因
这个现象不是检索遗漏，而是有结构性原因的。
**第一，全景分类的空间已经被填满。** Hu et al.（forms/functions/dynamics）、Zhang et al.（substrate/cognitive mechanism/subject）、Du（temporal scope/substrate/control policy）、Tian et al.（演化三阶段）、Always-On（治理六轴）、Li & Chen（安全二维表）——这六个框架已经把“表示/访问/演化/控制/治理”五个正交问题的组合基本穷尽。**提出第 N 个分类法的边际价值已经趋近于零**。
**第二，评测方法学成为了新的瓶颈。** MERIT 的发现——“架构在单事实召回上不可区分”和“最准确的记忆比最高效的贵 2.7–3.9 倍”——直接暴露了**现有分类学讨论的空洞性**。当架构选择对实际效果的影响远小于评测配置的影响时，分类学讨论的优先级自然让位于评测方法学。
**第三，治理从“前沿方向”升级为“独立研究领域”。** Always-On（2606.30306）的 435 篇文献编码已经明确指出回滚机制只有 27/435 的覆盖率。2606–2610 的产出（PLACE、Memory as Metabolism、MemArchitect）正在填补这个空白——**这是一个从“识别缺口”到“填补缺口”的转折期，而不是提出新分类框架的窗口**。
**第四，垂直领域正在分化。** Agentic skills（2608.29596）、prospective memory（TriggerBench）、multi-agent shared memory（Wu et al.）、companion systems（Memory as Metabolism）——这些窄领域深化正在把“agent memory”这个统一话题拆解为多个独立子领域。**下一个综述级别的工作更可能出现在“子领域内部”而非“全景”**。
---
## 第三部分：增量更新到统一框架
把 2606–2610 的新发现放进之前的五问题框架，可以看到明显的增量：
### 3.1 覆盖矩阵的更新
| 综述/论文 | 表示 | 访问 | 演化 | 控制 | 治理 | 新增维度 |
|----------|------|------|------|------|------|---------|
| **MERIT（2609.05441）** | ❌ | ✅（重定义） | ❌ | ❌ | ❌ | **成本有效性** |
| **PLACE（2610.25179）** | ❌ | ❌ | ❌ | ❌ | ✅（write/read 分离） | **write vs read 两侧治理** |
| **Agentic Skills（2608.29596）** | ✅（程序性） | ✅（late-binding） | ✅（lifecycle） | ❌ | ✅（安全） | **六元组形式化** |
| **Anatomy（2602.19320）** | ✅ | ✅ | ❌ | ❌ | ❌ | **评测可靠性** |
| **Multi-agent Memory（Wu et al.）** | 部分 | 部分 | 部分 | ❌ | 部分 | **多智能体共享** |
| **Memory as Metabolism（2604.12034）** | ❌ | ❌ | ✅ | ❌ | ✅ | **companion 场景** |
| **Microsoft 系列（2606-2608）** | 部分 | ✅ | ❌ | ❌ | ❌ | **执行状态管理** |
### 3.2 五个问题之外正在出现的新维度
**成本有效性**——MERIT 的发现直接引入了一个被十篇综述完全忽略的维度：**记忆系统的经济性不是工程细节，而是与准确性平行的设计目标**。当一个记忆系统比另一个贵 3 倍但只好 5% 时，这个 trade-off 本身需要被分类学讨论。
**Write vs Read 的治理分离**——PLACE 把治理问题分解为两个正交的控制点，这个分解比 Always-On 的六轴更精细。**“状态是否正确存储”与“已存储状态是否有资格影响当前查询”是两个独立的失败模式，需要不同的机制**。
**执行状态 vs 语义状态**——Microsoft 系列和 Agentic Skills 论文都在指向同一个区分：**记忆系统存储的不仅是语义事实，还有执行状态（当前任务进度、已完成的步骤、下一步应该做什么）**。这个区分在十篇综述中只有 Du 的 write-manage-read 循环部分覆盖。
**Prospective memory（前瞻记忆）**——TriggerBench 引入了一个认知科学中重要但 agent memory 综述几乎未覆盖的类型：**记住未来要做的事**。这与 retrospective memory（记住过去发生了什么）是正交的。
---
## 第四部分：追踪建议的更新
基于 2606–2610 的产出结构变化，追踪策略需要调整：
**第一，放弃“等待下一个全景综述”的预期。** 2512–2606 那一批已经完成了分类学布局，下一个综述级别的工作更可能出现在子领域内部或跨框架整合方向。
**第二，重点关注三个正在快速演化的方向**：
- **评测方法学**（MERIT 代表的新范式）——这个方向直接影响所有架构讨论的有效性
- **治理算子级设计**（PLACE 代表的精细化方向）——从“识别治理缺口”到“设计具体算子”的转折
- **技能系统作为独立领域**（Agentic Skills 论文代表的分化方向）——procedural memory 正在脱离记忆分类学成为独立研究对象
**第三，Microsoft AI Memory Research Group 值得单独追踪。** 这个组在 2026 年下半年的产出密度（MESA、SkillHEX、TriggerBench、"Beyond Semantic Organization"）代表了一个明确的工业视角：**记忆研究的重心正在从语义组织转向执行状态管理**——这个转变十篇综述都没有明确预测。
---
## 关于检索覆盖的诚实说明
我必须坦率承认检索的边界：**2606–2610 窗口内的论文，我的检索深度可能不如 2512–2606 那批**。arXiv 检索存在结构性滞后，且 2610（10 月）的论文可能尚未完整索引。我找到的 PLACE（2610.25179，10 月 18 日）是检索窗口内最新的，但**可能不是 10 月的全部产出**。
如果你需要确认是否还有遗漏，最直接的验证方式是：**在 arXiv 搜索框输入 `agent memory survey` 并按提交日期降序，把 `cs.AI, cs.CL, cs.LG` 三个分类各过一遍最近三个月的条目**。另外三个持续更新的 GitHub 仓库（Shichun-Liu/Agent-Memory-Paper-List、FeishuLuo/Evolving-LLM-Agent-Memory-Survey、AgentMemoryWorld/Awesome-Agent-Memory）的最近一个月 add 是感知新论文的最高效方式——它们通常比任何单次检索都更快捕捉到新产出。
**这个领域在 2026 年下半年的变化速度确实很快——但变化的方向不是“更多综述”，而是“综述之外的产出结构变化”。** 这个判断本身，可能比一份新的综述清单更有价值。