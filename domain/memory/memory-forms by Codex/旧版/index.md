# Memory forms：当前任务与结论入口

> 索引作者：Codex；纯 AI 生成的研究工作稿。可确认基于 GPT-6，具体子型号未知。整理日期：2026-11-02。

<a id="current-task"></a>
## 本次 forms 基础研究的当前任务说明

本次工作为后续 token memory 研究整理可直接继承的概念、机制结论与使用条件。用户已确认主研 token，保留 token / parametric / latent 三形态，并先分“参数记忆 / 外部记忆”、再在外部中区分 token / latent。本轮按问题吸收 forms2、05、06 的有效认识，裁定关键推理，保留证据与真正未决问题，不继续增加互相替代的稿件或争论哪套分类最根本。

本轮完成边界是明确“现在采用什么、为什么、什么仍需实验”，不自动启动下一阶段的维度研究或实验。具体工作定义与分析安排是本轮工作默认，不代表用户新批准了相应命题或后续任务。以下说明仅适用于本次 forms 基础研究；后续用户新指令优先。历史提示词与意图片段只用于追溯，不承接为当前执行指令。

<a id="current-decisions"></a>
## 六条可以直接使用的结论

下表压缩当前裁定，具体定义、条件、证据与反例由主文承担。研究入口属于已确认约定；表中的分析与机制裁定属于本轮研究判断，可由新证据修订。

| 当前采用的结论 | 知识状态与论证入口 |
|---|---|
| 默认以跨 LLM 请求为保留边界；当前可用 memory 还须有现存机制与允许路径来读取或恢复并消费历史信息。context、cache 可以参与这种关系，增加备份不会自动取消记忆资格。 | 本轮操作性定义与分析裁定；[工作边界](<讨论前提 by Codex.md#working-boundary>) · [因果说明](<讨论前提 by Codex.md#causal-model>)。 |
| 固定目标模型实现与接口约定后，LoRA 增量属于参数侧，作为前缀激活读取的 soft prompt 属于 latent；写入用了梯度不独自决定 form。 | 约定下的机制裁定；[形态判例](<讨论前提 by Codex.md#form-decisions>)。 |
| Token 留存符号工件，供目标 LLM 经输入使用；原文、检索索引、派生 KV 是不同实例，索引不自动等于注入模型的 latent 内容。 | 机制与实例裁定；[Token 的保留与使用](<讨论前提 by Codex.md#token-retention-use>) · [实例与使用路径](<讨论前提 by Codex.md#instances-and-use-paths>)。 |
| 选择、更新、作用域、治理等是有用的功能检查项；具体任务可以要求它们，不能把全部功能一律列为 memory 成立门槛。 | 本轮分析裁定；[功能要求](<讨论前提 by Codex.md#functional-requirements>)。 |
| 完整系统可以通过保留、更新并使用外部状态发生适应；未改主体权重或移除笔记后失效，不能单独判定完整系统“没有学习”。 | 系统边界下的裁定，泛化效果另测；[外部状态与适应](<讨论前提 by Codex.md#external-adaptation>)。 |
| 同质量、同负载下，KV 复用的累计重算节省须超过新增的保存、装载、重建与管理成本才值得采用；它仍有后续注意力成本，其他 latent 路径也不能统一称为免 prefill。 | 机制裁定，净收益依负载；[KV 复用裁定](<讨论前提 by Codex.md#kv-reuse-decision>)。 |

<a id="empirical-questions"></a>
## 三组待实证问题

- **能力与泛化：** 特定模型、任务与外部状态方案能保持什么、迁移什么、泛化到哪里，需要分别测量。状态被更新不自动证明泛化，保持外部依赖也不自动否定完整系统的适应。
- **成本与容量：** 净节省、干扰发生的条件、各方案的可行预算和混合收益，需要同任务、同质量、同资源口径比较。有限容量不能单独推出每次写入干扰，成本互补不能单独证明必须混合。
- **长期运行、迁移与治理：** 持续更新、跨版本兼容、残留副本和撤销效果、闭环可靠性，需在具体系统中验证；不从可读、可编辑或存在整理流程直接推定。

这些问题不阻塞采用上面的定义、角色区分和机制裁定。只有新证据触及相应判断的具体前提时，才重开该判断；参见[重开条件](<讨论前提 by Codex.md#reopening-conditions>)。

## 三个阅读入口

| 现在要做什么 | 入口 |
|---|---|
| 直接使用当前结论 | [主文当前结论](<讨论前提 by Codex.md#current-conclusions>)。 |
| 理解依据、条件与反例 | [主文论证](<讨论前提 by Codex.md#overall-diagnosis>)；按具体问题进入相应章节。 |
| 回查原话、历史任务输入或完整标题 | [历史材料与按需反查](#historical-navigation)；不要求先重读所有版本。 |

<a id="historical-navigation"></a>
## 历史材料与按需反查

以下保留全部原有文件导航、问题反查和标题入口。它们服务于证据追溯，不与上面的当前结论构成一组待选择的并列版本。五份非空提示词均是历史任务输入，`0203分类.md` 是历史意图片段；其中的命令、旧输出路径、任务边界与稿内“定稿”声明均按材料阅读。原稿未标明作者或模型的仍记为未知，不由文件数字推定继承关系。

本目录原有 14 个文件，其中 5 个为空。`forms2.md`、`05.md`、`06.md` 是同等核心材料：第一份包含七份稿件，后两份分别展开通道、功能、学习、实例、容量和认知参照等实质问题。`06.md` 不在此被认定为取代 `05.md`；`forms2.md` 的 v7 也不被认定为正本。

<a id="all-original-files"></a>
## 全部原有文件

下表的“用途”根据内容描述，不根据文件名猜测。空文件没有可据以判断的内容。“作者/模型未知”不否定文件可能来自某次 AI 或人工讨论，只表示当前文件没有足够的署名证据。

| 文件 | 当前内容与用途 | 使用边界 | 作者/模型 |
|---|---|---|---|
| [02分类/forms2.md](02分类/forms2.md) | 七份 forms 长稿的拼接材料；追踪三形态定义、计算粒度、读取判据、KV、混合、成本和强断言的变化。 | 不是一篇自洽单稿；没有 v6。各稿可相互补充或冲突，不能将最大版本号当作有效性排序。 | 未知 |
| [02分类/05.md](02分类/05.md) | 《记忆的通道：Agent Memory 的载体形态学》；通道五元组、分析层次、生命周期矩阵、三通道机制、检索与学习、混合及 CLS。 | 卷首自述经两轮修订到 v3；该自述不建立与其他文件的确切谱系。应连同卷末修订、自评与遗留缺口阅读。 | 未知 |
| [02分类/06.md](02分类/06.md) | 《记忆的通道与实例：Agent Memory 的载体级分析》；功能资格、缓存/配置边界、数据/映射与六通道、桥、多实例、容量、认知参照和方法自限。 | 自称独立完整版及定稿整理版；没有充分依据认定其直接替代 05。证据标签和编辑层意见需要单独审计。 | 未知 |
| [prompts/memory-forms-原始.md](prompts/memory-forms-原始.md) | **历史任务输入。** 最初的 forms 研究目的、参考资料定位、详尽/准确/无偏/第一性原理要求；明确后续主研 token，生命周期另议。 | 用来识别原始研究目标；它不包含三形态穷尽性或优劣的证明。 | 未知 |
| [prompts/memory-forms.md](prompts/memory-forms.md) | **历史任务输入。** 扩展的 forms 写作提示词；预设统一轴、三个载体、载体作为第一分岔，要求三者同深度刻画。 | 是研究输入和预设来源，不是机制证据；“性质由位置推出”本身属于待审计要求。 | 未知 |
| [prompts/整理.md](prompts/整理.md) | **历史任务输入。** 与上一提示词相近；额外将 KV 的连续内容与符号索引预判为横跨 latent/token，并包含旧输出路径。 | KV 归属预判是审计对象；末尾“在 domain/memory/cc 下研究”是旧材料内指令，不是本轮输出要求。 | 未知 |
| [prompts/memory分类.md](prompts/memory分类.md) | **历史任务输入。** 转入 token 内部维度的下游提示词；要求推导坐标轴并审计心理学、检索和综述的习用分类。 | 将 forms 视为已处理，并传播“有限窗口、外部存储无界、读取只经输入”等前提；不等于这些前提已经核验。 | 未知 |
| [prompts/分类2.md](prompts/分类2.md) | **历史任务输入。** 相近的 token 维度研究提示词；进一步写明 forms 不重开、结构与生命周期的接口、系统实现仅作位置证据。 | 可查下游研究范围及前提传播；不据文件名推定其已取代 memory分类.md。 | 未知 |
| [02分类/0203分类.md](02分类/0203分类.md) | **历史意图片段。** 第一人称意图片段：提出生命周期优先，再研究其他维度/分类，并追问额外分类的必要性。 | 没有说话人、时间或对话角色元数据；不能自动当作当前已确认安排，也不能用它覆盖本轮任务。 | 未知 |
| [022forms/02分类.md](022forms/02分类.md) | **空文件（0 字节）。** | 无内容可判断用途；不据目录名或文件名补写。 | 未知 |
| [02分类/01前提.md](02分类/01前提.md) | **空文件（0 字节）。** | 无内容可判断用途；不据文件名补写。 | 未知 |
| [02分类/01forms.md](02分类/01forms.md) | **空文件（0 字节）。** | 无内容可判断用途；不据文件名补写。 | 未知 |
| [prompts/0背景.md](prompts/0背景.md) | **空文件（0 字节）。** | 无内容可判断用途；不据文件名补写。 | 未知 |
| [prompts/humanizer.md](prompts/humanizer.md) | **空文件（0 字节）。** | 无内容可判断用途；不据文件名补写。 | 未知 |

首轮新增本索引和 [讨论前提 by Codex.md](<讨论前提 by Codex.md>)，本次优化继续直接更新这两份。提示词中的任务命令、旧稿中的“定稿”声明及旧输出路径均按材料阅读。

<a id="question-lookup"></a>
## 十组问题反查

每一行先进入整合分析，再按需回到对应原稿。下列定位只说明“哪里讨论了此问题”，不表示接受该处全部结论。

| 问题 | 本轮整合分析 | 原始材料入口 |
|---|---|---|
| 研究目的、分类用途与成功标准 | [进入分析](<讨论前提 by Codex.md#purpose-and-presuppositions>) | [原始目标](<D:/workspace/memory/domain/memory/mine/prompts/memory-forms-原始.md:2>) · [v1 不可通约/取材](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:140>) · [05 §10 用途与限度](<D:/workspace/memory/domain/memory/mine/02分类/05.md:172>) · [06 §11 框架比较](<D:/workspace/memory/domain/memory/mine/02分类/06.md:292>) |
| 第一性起点：无状态、持久状态、前向计算与事件边界 | [进入分析](<讨论前提 by Codex.md#computational-starting-point>) | [v5 请求边界](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:941>) · [v7 单次前向](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1198>) · [05 §1 信息通道](<D:/workspace/memory/domain/memory/mine/02分类/05.md:16>) · [06 §1 无状态起点](<D:/workspace/memory/domain/memory/mine/02分类/06.md:40>) |
| 缓存与记忆、context、config、知识资产、经验的边界 | [进入分析](<讨论前提 by Codex.md#memory-boundaries>) | [v5 缓存同构](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1101>) · [v7 治理检测器](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1213>) · [05 §2 层次判据](<D:/workspace/memory/domain/memory/mine/02分类/05.md:34>) · [06 §2 功能与资格](<D:/workspace/memory/domain/memory/mine/02分类/06.md:55>) |
| Forms、通道与层级：三形态、五元组、数据/映射和六通道 | [进入分析](<讨论前提 by Codex.md#forms-and-channels>) | [v4 状态与读取接口](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:734>) · [05 五元组](<D:/workspace/memory/domain/memory/mine/02分类/05.md:17>) · [06 §3 枚举](<D:/workspace/memory/domain/memory/mine/02分类/06.md:67>) · [06 §11.3 双框架比较](<D:/workspace/memory/domain/memory/mine/02分类/06.md:297>) |
| 多实例、内容/索引、生成器/产物、转换与使用路径 | [进入分析](<讨论前提 by Codex.md#instances-and-use-paths>) | [v4 LoRA/soft prompt](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:801>) · [v5 KV内容与索引](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1078>) · [05 三层结构](<D:/workspace/memory/domain/memory/mine/02分类/05.md:35>) · [06 §6 桥与实例](<D:/workspace/memory/domain/memory/mine/02分类/06.md:178>) |
| 功能需求与生命周期：持久化、使用、选择、更新、作用域、治理 | [进入分析](<讨论前提 by Codex.md#functions-and-lifecycle>) | [v7 操作轴](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1209>) · [05 §3 生命周期矩阵](<D:/workspace/memory/domain/memory/mine/02分类/05.md:47>) · [06 六项功能](<D:/workspace/memory/domain/memory/mine/02分类/06.md:56>) · [生命周期优先意图片段](<D:/workspace/memory/domain/memory/mine/02分类/0203分类.md:1>) |
| 学习、记忆与能力：三种定义、移除笔记、泛化及系统边界 | [进入分析](<讨论前提 by Codex.md#learning-and-capability>) | [v7 理解深度/能力断言](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1251>) · [v7 记忆与能力](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1274>) · [05 §7 三种学习定义](<D:/workspace/memory/domain/memory/mine/02分类/05.md:130>) · [06 表达能力争议](<D:/workspace/memory/domain/memory/mine/02分类/06.md:114>) |
| 成本、容量与混合分工：资源基线、干扰、加性/竞争性及必然性 | [进入分析](<讨论前提 by Codex.md#cost-capacity-and-hybrid>) | [v7 混合必然性](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1357>) · [05 §8 成本与混合](<D:/workspace/memory/domain/memory/mine/02分类/05.md:147>) · [06 §7 容量与经济学](<D:/workspace/memory/domain/memory/mine/02分类/06.md:206>) · [06 §8 对照表](<D:/workspace/memory/domain/memory/mine/02分类/06.md:231>) |
| 认知参照与巩固：CLS、ACT-R、机制对应和持续闭环 | [进入分析](<讨论前提 by Codex.md#cognitive-reference>) | [v7 三条前史](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1196>) · [05 §9 CLS启发](<D:/workspace/memory/domain/memory/mine/02分类/05.md:164>) · [06 §9 认知参照](<D:/workspace/memory/domain/memory/mine/02分类/06.md:262>) · [06 巩固与缺口](<D:/workspace/memory/domain/memory/mine/02分类/06.md:277>) |
| 证据、反例与结论强度：已验证、定理、自评、证伪及验证债务 | [进入分析](<讨论前提 by Codex.md#evidence-and-strength>) | [v7 断言地位](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1382>) · [v7 引用核验自述](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1417>) · [05 修订附录](<D:/workspace/memory/domain/memory/mine/02分类/05.md:235>) · [06 证伪汇总](<D:/workspace/memory/domain/memory/mine/02分类/06.md:309>) · [06 验证债务](<D:/workspace/memory/domain/memory/mine/02分类/06.md:366>) |

<a id="case-lookup"></a>
## 具体判例反查

| 想查的具体争议 | 原文位置 | 连到哪组问题 |
|---|---|---|
| LoRA 是外挂文件，是否就是外部记忆？soft prompt 可训练，是否就是参数记忆？ | [v4 决定性判例](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:801>) · [v4 软提示归属](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:841>) · [06 桥上居民](<D:/workspace/memory/domain/memory/mine/02分类/06.md:181>) | [进入分析](<讨论前提 by Codex.md#forms-and-channels>) |
| 参数写入是否必需梯度？闭式编辑与梯度流程怎样区分？ | [v5 两种写入谱系](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1025>) · [v7 定义](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1260>) · [05 参数异质性](<D:/workspace/memory/domain/memory/mine/02分类/05.md:83>) | [进入分析](<讨论前提 by Codex.md#forms-and-channels>) |
| 请求内 KV 是否算记忆？会话边界有没有本体地位？ | [v5 请求选择](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:941>) · [v5 临界点](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1101>) · [v7 请求内记忆](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1291>) · [06 权威副本判据](<D:/workspace/memory/domain/memory/mine/02分类/06.md:61>) | [进入分析](<讨论前提 by Codex.md#memory-boundaries>) |
| 向量索引是否 latent 内容？MLA 是否失去源 token 对应？ | [v5 索引排除](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:982>) · [v5 双重结构](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1082>) · [v5 MLA等参照](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1095>) | [进入分析](<讨论前提 by Codex.md#instances-and-use-paths>) |
| token 自然产生激活，是否所有 token 系统都算混合？生成器训练是否等于写入当前内容？ | [v3 两类混合](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:648>) · [v5 生成器与产物](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1062>) · [v7 自动副本](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1315>) · [06 双分析单位](<D:/workspace/memory/domain/memory/mine/02分类/06.md:68>) | [进入分析](<讨论前提 by Codex.md#instances-and-use-paths>) |
| 因果定位能否推出最佳编辑位置？可检视能否推出可归因/可删除？ | [v5 定位争议](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1014>) · [v5 检视与地址性](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1037>) · [05 定位与AlphaEdit](<D:/workspace/memory/domain/memory/mine/02分类/05.md:94>) | [进入分析](<讨论前提 by Codex.md#evidence-and-strength>) |
| 免 prefill、读免费、持续存储成本分别适用于什么实现？ | [v4 latent不同注入点](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:850>) · [v5 参数成本](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1033>) · [v5 latent读取](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1051>) · [06 token完整账单](<D:/workspace/memory/domain/memory/mine/02分类/06.md:103>) | [进入分析](<讨论前提 by Codex.md#cost-capacity-and-hybrid>) |
| 记忆污染、提示注入、共享缓存侧信道与单租户风险怎样区分？ | [v7 token攻击面](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1255>) · [v7 latent条件攻击面](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1302>) · [06 失败与攻击总表](<D:/workspace/memory/domain/memory/mine/02分类/06.md:281>) | [进入分析](<讨论前提 by Codex.md#evidence-and-strength>) |

<a id="forms-navigation"></a>
## forms2：七份稿件内部导航

原文共 1423 行。下表把实质内容与其后的空行/分隔线分开标明；不存在未列出的第八份稿件。各小表的“行范围”按下一个同级或更高级标题之前划定，可能含段末分隔线；起始行跳转直接定位原文标题。

| 稿件 | 实质内容行范围 | 其后空行/分隔行 | 导航 |
|---|---|---|---|
| v1：记忆的载体：token、parametric 与 latent（修订稿） | 1–158 | 159–165 | [本页导航](#forms-v1) |
| 载体：Agent Memory 的第一分岔（无版本号） | 166–272 | 273–278 | [本页导航](#forms-unnumbered) |
| v2：记忆的载体：token、parametric 与 latent（重构版） | 279–495 | 496–499 | [本页导航](#forms-v2) |
| v3：记忆的载体：token、parametric 与 latent | 500–702 | 703–708 | [本页导航](#forms-v3) |
| v4：Agent Memory 的载体：token、parametric、latent | 709–917 | 918–923 | [本页导航](#forms-v4) |
| v5：记忆的载体：token、parametric 与 latent | 924–1179 | 1180–1187 | [本页导航](#forms-v5) |
| v7：记忆的载体：token、parametric 与 latent | 1188–1423 | 无 | [本页导航](#forms-v7) |

<a id="forms-v1"></a>
### v1：修订稿

9–153 行为正文；155–158 行是编辑注；2–7 行为本轮修订自述。

| 主节入口 | 行范围 | 节内入口 |
|---|---|---|
| [§1 引言：冻结的前提](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:9>) | 9–22 | [1.1 冻结](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:10>) · [1.2 判据：什么构成记忆](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:15>) · [1.3 记忆系统的算子分解](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:19>) |
| [§2 三个物理位置](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:23>) | 23–37 | [2.1 前向计算的信息解剖](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:24>) · [2.2 穷尽性命题](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:30>) · [2.3 归类判据：以读取时刻为准](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:33>) |
| [§3 token 载体](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:38>) | 38–57 | [3.1 定义与机制](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:39>) · [3.2 设计自由度：token 内部分化的必然性与悬置](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:43>) · [3.3 成本结构与性质](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:51>) · [3.4 失败的可见性](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:54>) |
| [§4 parametric 载体](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:58>) | 58–78 | [4.1 定义与机制](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:59>) · [4.2 与预训练的关系，及写入的机制基础](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:62>) · [4.3 写入通道：重开被冻结关闭的梯度](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:65>) · [4.4 成本结构与性质](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:67>) · [4.5 记忆与推理的不可分离性](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:73>) · [4.6 失败模式](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:76>) |
| [§5 latent 载体](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:79>) | 79–99 | [5.1 KV cache 的机制回顾](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:80>) · [5.2 定义与注入点](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:83>) · [5.3 记忆临界点](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:87>) · [5.4 存储成本：算例](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:91>) · [5.5 性质](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:97>) |
| [§6 边界与判例](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:100>) | 100–114 | [6.1 裸上下文窗口：token 内容跑在 latent 载体上](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:101>) · [6.2 判例表](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:103>) |
| [§7 载体的对比](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:115>) | 115–143 | [7.1 总表（经审计）](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:116>) · [7.2 三种经济学](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:138>) · [7.3 不可通约性](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:140>) |
| [§8 范围与取材](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:144>) | 144–158 | [8.1 分类实在性的证据](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:145>) · [8.2 门槛与最优的诚实区分](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:149>) · [8.3 声明](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:151>) |

<a id="forms-unnumbered"></a>
### 无版本号稿：载体作为第一分岔

注意167–169行的两轴推导与253–268行的KV判例。

| 主节入口 | 行范围 | 节内入口 |
|---|---|---|
| [引言：从计算结构到载体问题](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:167>) | 167–171 | 本节无下一层标题 |
| [判定框架：四个维度](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:172>) | 172–179 | 本节无下一层标题 |
| [Token 载体](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:180>) | 180–197 | [定义来源与计算定位](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:181>) · [状态存放](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:183>) · [读取机制](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:185>) · [写入与检视](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:187>) · [性质与代价](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:189>) · [边界判定](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:195>) |
| [Parametric 载体](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:198>) | 198–217 | [定义来源与计算定位](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:199>) · [状态存放](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:201>) · [读取机制](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:203>) · [写入机制](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:205>) · [可检视性](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:207>) · [性质与代价](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:209>) · [边界判定与一个有争议的点](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:214>) |
| [Latent 载体](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:218>) | 218–237 | [定义来源与计算定位](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:219>) · [状态存放](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:221>) · [读取机制](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:223>) · [写入机制](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:225>) · [可检视性](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:227>) · [性质与代价](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:229>) · [边界判定](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:235>) |
| [三载体对照](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:238>) | 238–252 | 本节无下一层标题 |
| [KV Cache：latent 与 token 之间的边界案例](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:253>) | 253–269 | [计算结构](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:255>) · [为何骑在边界上](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:257>) · [判定](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:264>) |
| [结语：载体作为第一分岔](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:270>) | 270–272 | 本节无下一层标题 |

<a id="forms-v2"></a>
### v2：重构版

280行是修订自述；471行起的断言降格清单及485行起的补全清单是认识论审计入口。

| 主节入口 | 行范围 | 节内入口 |
|---|---|---|
| [§0 方法论前言：第一性立场与边界声明](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:282>) | 282–295 | [0.1 为什么从"冻结"出发——以及为什么这是有条件的](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:283>) · [0.2 记忆研究的三条前史——避免领域诞生神话](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:286>) · [0.3 粒度声明与判据边界](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:292>) |
| [§1 判据与算子分解](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:296>) | 296–311 | [1.1 记忆判据及其超集问题](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:297>) · [1.2 算子分解及其边界](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:303>) · [1.3 主体性维度：本框架刻意缺席的一根轴](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:308>) |
| [§2 三类载体的结构性论证](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:312>) | 312–329 | [2.1 前向计算的信息解剖](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:313>) · [2.2 穷尽性的认识论地位](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:319>) · [2.3 归类判据：以读取时刻为准](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:324>) · [2.4 完整性与混合的张力](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:327>) |
| [§3 token 载体](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:330>) | 330–359 | [3.1 定义与机制](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:331>) · [3.2 token 内部分化：载体属性 vs 分类粒度](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:334>) · [3.3 成本结构与性质](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:348>) · [3.4 失败的可见性](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:356>) |
| [§4 parametric 载体](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:360>) | 360–384 | [4.1 定义与机制](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:361>) · [4.2 与预训练的关系，及定位发现的争议状态](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:364>) · [4.3 写入通道：重开被冻结关闭的梯度](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:372>) · [4.4 成本结构与"买断制"的适用域](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:375>) · [4.5 记忆与能力的不可分离性——及其对预训练知识地位的张力](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:378>) · [4.6 失败模式](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:382>) |
| [§5 latent 载体](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:385>) | 385–410 | [5.1 KV cache 的机制回顾](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:386>) · [5.2 定义与注入点](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:389>) · [5.3 记忆临界点：工程裁量而非本体跃迁](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:392>) · [5.4 存储成本：算例的形态对称性](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:395>) · [5.5 性质：时间维度的对称宽容](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:406>) |
| [§6 边界与判例](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:411>) | 411–427 | [6.1 裸上下文窗口：token 内容跑在 latent 载体上](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:412>) · [6.2 判例表](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:415>) |
| [§7 载体的对比](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:428>) | 428–458 | [7.1 总表（经二次审计）](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:429>) · [7.2 三种经济学（修正版）](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:448>) · [7.3 可通约性：从绝对到相对](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:451>) |
| [§8 范围与取材](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:459>) | 459–470 | [8.1 分类实在性的证据与选择偏倚](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:460>) · [8.2 门槛与最优的诚实区分](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:464>) · [8.3 聚焦声明的诚实化](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:466>) |
| [附录 A：框架定理降格清单](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:471>) | 471–484 | 本节无下一层标题 |
| [附录 B：维度补全清单](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:485>) | 485–495 | 本节无下一层标题 |

<a id="forms-v3"></a>
### v3：操作轴移出、混合与控制变量

501行是结构改动自述，702行是重构说明；两者与独立正文分开阅读。

| 主节入口 | 行范围 | 节内入口 |
|---|---|---|
| [§0 方法论前言：立场与边界](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:503>) | 503–512 | [0.1 冻结作为条件前提](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:504>) · [0.2 三条前史](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:507>) · [0.3 粒度声明](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:509>) |
| [§1 记忆判据与本章边界](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:513>) | 513–525 | [1.1 记忆判据及其附加条件](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:514>) · [1.2 载体轴与操作轴的解耦](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:521>) |
| [§2 三类载体的结构性论证](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:526>) | 526–543 | [2.1 前向计算的信息解剖](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:527>) · [2.2 穷尽性命题及其前提](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:533>) · [2.3 归类判据：以读取时刻为准](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:538>) · [2.4 穷尽性不蕴含互斥性](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:541>) |
| [§3 token 载体](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:544>) | 544–567 | [3.1 定义与机制](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:545>) · [3.2 内部分化：自由度的两个来源](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:548>) · [3.3 成本结构与性质](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:561>) · [3.4 失败的可见性与攻击面](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:564>) |
| [§4 parametric 载体（对照载体）](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:568>) | 568–587 | [4.1 定义与机制](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:569>) · [4.2 与预训练的关系、地址性程度谱](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:572>) · [4.3 写入通道：重开梯度](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:578>) · [4.4 成本结构与“买断制”的适用域](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:580>) · [4.5 记忆与能力的不可分离性](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:582>) · [4.6 失败模式](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:585>) |
| [§5 latent 载体（对照载体）](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:588>) | 588–609 | [5.1 KV cache 的机制回顾](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:589>) · [5.2 定义与注入点](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:592>) · [5.3 记忆临界点：工程裁量](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:595>) · [5.4 存储成本：形态对称的算例](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:597>) · [5.5 性质](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:605>) |
| [§6 边界与判例](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:610>) | 610–624 | [6.1 裸上下文窗口：token 内容跑在 latent 载体上](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:611>) · [6.2 判例表](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:613>) |
| [§7 载体的对比](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:625>) | 625–657 | [7.1 总表](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:626>) · [7.2 三种经济学](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:643>) · [7.3 可通约性](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:645>) · [7.4 混合形态：补充说明](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:648>) |
| [§8 范围与取材](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:658>) | 658–671 | [8.1 分类实在性的证据与偏倚声明](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:659>) · [8.2 门槛与最优的区分](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:663>) · [8.3 聚焦声明](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:665>) |
| [附录 A：断言地位清单](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:672>) | 672–686 | 本节无下一层标题 |
| [附录 B：后续章节接口](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:687>) | 687–702 | 本节无下一层标题 |

<a id="forms-v4"></a>
### v4：目标LLM、状态本体与读取接口

对齐目标LLM的分析单位、LoRA/soft prompt读取角色、外挂参数及会话内KV边界。

| 主节入口 | 行范围 | 节内入口 |
|---|---|---|
| [0. 本文的地位、范围与用法](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:710>) | 710–715 | 本节无下一层标题 |
| [1. 计算图与位置推导](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:716>) | 716–742 | [1.1 前向计算的解剖](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:717>) · [1.2 持久状态的两个必要条件](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:723>) · [1.3 接口枚举：为什么恰好三个位置](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:727>) · [1.4 判定规则：状态本体 + 读取接口](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:734>) · [1.5 三个位置，不是三个互斥格子](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:740>) |
| [2. Token 载体](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:743>) | 743–782 | [2.1 定义与来源](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:744>) · [2.2 什么算，什么不算](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:747>) · [2.3 状态存放](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:764>) · [2.4 写入机制](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:766>) · [2.5 读取机制](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:768>) · [2.6 性质与代价（由位置推出）](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:770>) · [2.7 边缘情形](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:778>) |
| [3. Parametric 载体](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:783>) | 783–820 | [3.1 定义与来源](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:784>) · [3.2 什么算，什么不算](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:787>) · [3.3 状态存放](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:802>) · [3.4 写入机制](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:804>) · [3.5 读取机制与内部结构](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:806>) · [3.6 性质与代价（由位置推出）](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:808>) · [3.7 边缘情形](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:816>) |
| [4. Latent 载体](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:821>) | 821–867 | [4.1 定义与来源](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:822>) · [4.2 什么算，什么不算（含软提示归属论证）](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:825>) · [4.3 状态存放](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:842>) · [4.4 写入机制](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:844>) · [4.5 读取机制：注入点枚举](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:850>) · [4.6 性质与代价（由位置推出）](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:855>) · [4.7 边缘情形](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:863>) |
| [5. KV Cache：专项说明](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:868>) | 868–880 | [5.1 机制](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:869>) · [5.2 归属：三位置之外的边界情形](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:871>) · [5.3 三种命运](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:874>) · [5.4 文献中的界定分歧（如实记录）](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:878>) |
| [6. 多载体系统（补充）](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:881>) | 881–897 | [6.1 并存的结构性原因](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:882>) · [6.2 代表性组合（载体成分标注）](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:884>) · [6.3 载体间转化（最小声明，不展开）](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:891>) |
| [7. 三载体对比总表](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:898>) | 898–909 | 本节无下一层标题 |
| [8. 开放问题与分类争议（显式标注）](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:910>) | 910–917 | 本节无下一层标题 |

<a id="forms-v5"></a>
### v5：请求边界、前向/控制/执行区分

925行是性质说明；1179行是文档自查。请求边界、非梯度参数写入及内容/索引是重点入口。

| 主节入口 | 行范围 | 节内入口 |
|---|---|---|
| [§0 导言：载体问题](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:927>) | 927–931 | 本节无下一层标题 |
| [§1 计算结构：状态位置的枚举](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:932>) | 932–975 | [1.1 术语与前向计算的信息解剖](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:933>) · [1.2 计算事件的边界：请求](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:941>) · [1.3 记忆判据与前向判据](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:947>) · [1.4 位置枚举与穷尽性](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:956>) · [1.5 定义锚定、归类判据与两轴解耦](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:966>) |
| [§2 token 载体](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:976>) | 976–1008 | [2.1 定义来源](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:977>) · [2.2 状态存放](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:980>) · [2.3 读取机制](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:983>) · [2.4 写入机制](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:995>) · [2.5 性质与代价（由机制推导）](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:998>) · [2.6 失败模式](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1006>) |
| [§3 parametric 载体](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1009>) | 1009–1043 | [3.1 定义来源](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1010>) · [3.2 状态存放：编码方式与其证据](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1014>) · [3.3 读取机制](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1020>) · [3.4 写入机制](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1025>) · [3.5 性质与代价](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1033>) · [3.6 失败模式](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1041>) |
| [§4 latent 载体](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1044>) | 1044–1077 | [4.1 定义来源](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1045>) · [4.2 状态存放](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1049>) · [4.3 读取机制：注入点与计算细节](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1051>) · [4.4 写入机制](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1057>) · [4.5 性质与代价](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1064>) · [4.6 失败模式](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1072>) |
| [§5 KV cache：内容与索引的分离](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1078>) | 1078–1104 | [5.1 机制回顾](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1080>) · [5.2 双重结构](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1082>) · [5.3 判定与索引维度](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1087>) · [5.4 反向参照物](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1095>) · [5.5 记忆临界点与缓存同构](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1101>) |
| [§6 判例总集](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1105>) | 1105–1133 | 本节无下一层标题 |
| [§7 三载体的对照](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1134>) | 1134–1172 | [7.1 总表](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1135>) · [7.2 三行展开](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1154>) · [7.3 载体间的转化（最小点明）](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1158>) · [7.4 描述性分布：证据与偏倚](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1160>) · [7.5 无共识点清单](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1164>) |
| [§8 范围、判别力边界与遗留接口](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1173>) | 1173–1179 | 本节无下一层标题 |

<a id="forms-v7"></a>
### v7：新增治理、机制/内容判据与核验分档

1189行和1423行是整合/定稿自述；“定稿”不设定本轮有效性排序。

| 主节入口 | 行范围 | 节内入口 |
|---|---|---|
| [§0 方法论前言：立场与边界](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1191>) | 1191–1201 | [0.1 冻结作为条件前提](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1192>) · [0.2 三条前史](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1196>) · [0.3 粒度声明](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1198>) |
| [§1 记忆判据与本章边界](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1202>) | 1202–1216 | [1.1 记忆判据及其附加条件](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1203>) · [1.2 载体轴与操作轴的解耦](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1209>) · [1.3 治理检测器：记忆的操作性校验](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1213>) |
| [§2 三类载体的结构性论证](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1217>) | 1217–1235 | [2.1 前向计算的信息解剖](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1218>) · [2.2 穷尽性命题及其前提](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1224>) · [2.3 归类判据：以读取时刻为准，及一处判据分歧](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1229>) · [2.4 穷尽性不蕴含互斥性](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1233>) |
| [§3 token 载体](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1236>) | 1236–1258 | [3.1 定义与机制](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1237>) · [3.2 内部分化：自由度的两个来源与多轴结构](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1240>) · [3.3 成本结构、性质与结构性限制](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1251>) · [3.4 失败可见性与攻击面](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1255>) |
| [§4 parametric 载体（对照载体）](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1259>) | 1259–1279 | [4.1 定义与机制](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1260>) · [4.2 层级关系、写入形态与地址性程度谱](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1263>) · [4.3 写入通道：重开梯度](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1270>) · [4.4 成本结构与“买断制”的适用域](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1272>) · [4.5 记忆与能力的不可分离性](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1274>) · [4.6 失败模式](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1277>) |
| [§5 latent 载体（对照载体）](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1280>) | 1280–1313 | [5.1 KV cache 的机制回顾与语义升格](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1281>) · [5.2 定义与注入点](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1288>) · [5.3 生命周期与记忆地位](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1291>) · [5.4 存储成本：形态对称的算例](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1294>) · [5.5 性质：含条件攻击面](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1302>) · [5.6 内部谱系的存在性](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1307>) |
| [§6 边界与判例](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1314>) | 1314–1331 | [6.1 裸上下文窗口：token 内容跑在 latent 载体上](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1315>) · [6.2 判例表](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1317>) |
| [§7 载体的对比](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1332>) | 1332–1366 | [7.1 总表](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1333>) · [7.2 三种经济学](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1352>) · [7.3 可通约性](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1354>) · [7.4 混合形态：成本互补性、两种混合与控制变量](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1357>) |
| [§8 范围与取材](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1367>) | 1367–1381 | [8.1 分类实在性的证据与偏倚声明](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1368>) · [8.2 门槛与最优的区分](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1372>) · [8.3 聚焦声明](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1374>) |
| [附录 A：断言地位清单](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1382>) | 1382–1402 | 本节无下一层标题 |
| [附录 B：后续章节接口](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1403>) | 1403–1416 | 本节无下一层标题 |
| [附录 C：引用核验状态](<D:/workspace/memory/domain/memory/mine/02分类/forms2.md:1417>) | 1417–1423 | 本节无下一层标题 |

<a id="five-navigation"></a>
## 05：通道、生命周期、学习与 CLS

全文 273 行。第1–7行为卷首编辑层；第8–234行为正文标题、正文与参考文献；第235–273行为卷末修订附录。文件自述的 v1→v2→v3 只作为来历材料，不据此补造其他原稿或认定与 forms2 的具体对应。
卷首入口：[编辑说明](<D:/workspace/memory/domain/memory/mine/02分类/05.md:1>)（1–7）；正文标题：[记忆的通道](<D:/workspace/memory/domain/memory/mine/02分类/05.md:8>)（8）；卷末入口：[修订附录](<D:/workspace/memory/domain/memory/mine/02分类/05.md:235>)（235–273）。

| 主节入口 | 行范围 | 节内入口 |
|---|---|---|
| [0. 导言](<D:/workspace/memory/domain/memory/mine/02分类/05.md:9>) | 9–15 | 本节无下一层标题 |
| [1. 第一性原理：信息通道与计算边界](<D:/workspace/memory/domain/memory/mine/02分类/05.md:16>) | 16–33 | [1.1 信息通道的形式定义](<D:/workspace/memory/domain/memory/mine/02分类/05.md:17>) · [1.2 通道框架相对"三位置"框架的增益](<D:/workspace/memory/domain/memory/mine/02分类/05.md:26>) · [1.3 枚举的诚实表述](<D:/workspace/memory/domain/memory/mine/02分类/05.md:31>) |
| [2. 分析单位的显式分层](<D:/workspace/memory/domain/memory/mine/02分类/05.md:34>) | 34–46 | [2.1 三层结构](<D:/workspace/memory/domain/memory/mine/02分类/05.md:35>) · [2.2 分层判据](<D:/workspace/memory/domain/memory/mine/02分类/05.md:39>) · [2.3 控制面的正面处理](<D:/workspace/memory/domain/memory/mine/02分类/05.md:43>) |
| [3. 生命周期 × 通道矩阵](<D:/workspace/memory/domain/memory/mine/02分类/05.md:47>) | 47–58 | 本节无下一层标题 |
| [4. Token 通道：外部符号记忆](<D:/workspace/memory/domain/memory/mine/02分类/05.md:59>) | 59–78 | [4.1 机制](<D:/workspace/memory/domain/memory/mine/02分类/05.md:60>) · [4.2 成本结构](<D:/workspace/memory/domain/memory/mine/02分类/05.md:63>) · [4.3 优势](<D:/workspace/memory/domain/memory/mine/02分类/05.md:67>) · [4.4 能力上限的机制刻画与外推边界](<D:/workspace/memory/domain/memory/mine/02分类/05.md:71>) · [4.5 失败模式与攻击面](<D:/workspace/memory/domain/memory/mine/02分类/05.md:74>) |
| [5. Parametric 通道：权重记忆](<D:/workspace/memory/domain/memory/mine/02分类/05.md:79>) | 79–103 | [5.1 机制](<D:/workspace/memory/domain/memory/mine/02分类/05.md:80>) · [5.2 内部异质性的显式分拆](<D:/workspace/memory/domain/memory/mine/02分类/05.md:83>) · [5.3 定位争议与 AlphaEdit 争论链](<D:/workspace/memory/domain/memory/mine/02分类/05.md:94>) · [5.4 成本与适用域](<D:/workspace/memory/domain/memory/mine/02分类/05.md:98>) · [5.5 失败模式](<D:/workspace/memory/domain/memory/mine/02分类/05.md:101>) |
| [6. Latent 通道：持久张量记忆](<D:/workspace/memory/domain/memory/mine/02分类/05.md:104>) | 104–129 | [6.1 机制](<D:/workspace/memory/domain/memory/mine/02分类/05.md:105>) · [6.2 存储成本的量化](<D:/workspace/memory/domain/memory/mine/02分类/05.md:111>) · [6.3 读取成本的准确表述](<D:/workspace/memory/domain/memory/mine/02分类/05.md:116>) · [6.4 最新工程前沿：两项改变通道边界的工作](<D:/workspace/memory/domain/memory/mine/02分类/05.md:120>) · [6.5 多模态输入的归属](<D:/workspace/memory/domain/memory/mine/02分类/05.md:125>) · [6.6 失败模式](<D:/workspace/memory/domain/memory/mine/02分类/05.md:127>) |
| [7. 检索是否构成学习：正面处理](<D:/workspace/memory/domain/memory/mine/02分类/05.md:130>) | 130–146 | [7.1 Xu（2026）主张及其强度](<D:/workspace/memory/domain/memory/mine/02分类/05.md:132>) · [7.2 三种"学习"定义下的分解](<D:/workspace/memory/domain/memory/mine/02分类/05.md:137>) · [7.3 T-Mem 的启示：检索可能需要形态级创新](<D:/workspace/memory/domain/memory/mine/02分类/05.md:144>) |
| [8. 成本经济学的交汇点与混合必然性](<D:/workspace/memory/domain/memory/mine/02分类/05.md:147>) | 147–163 | [8.1 三条交汇点及其物理解释](<D:/workspace/memory/domain/memory/mine/02分类/05.md:148>) · [8.2 "混合必然性"的论证补全](<D:/workspace/memory/domain/memory/mine/02分类/05.md:152>) |
| [9. CLS 类比的角色：从参照系到启发源](<D:/workspace/memory/domain/memory/mine/02分类/05.md:164>) | 164–171 | 本节无下一层标题 |
| [10. 框架的适用范围与结语](<D:/workspace/memory/domain/memory/mine/02分类/05.md:172>) | 172–189 | [10.1 该框架能做什么](<D:/workspace/memory/domain/memory/mine/02分类/05.md:173>) · [10.2 该框架不能做什么](<D:/workspace/memory/domain/memory/mine/02分类/05.md:178>) · [10.3 已知盲区](<D:/workspace/memory/domain/memory/mine/02分类/05.md:182>) · [10.4 结语](<D:/workspace/memory/domain/memory/mine/02分类/05.md:186>) |
| [参考文献](<D:/workspace/memory/domain/memory/mine/02分类/05.md:190>) | 190–234 | 本节无下一层标题 |
| [A. 修订日志（v1 → v2 → v3 关键变更）](<D:/workspace/memory/domain/memory/mine/02分类/05.md:236>) | 236–254 | 本节无下一层标题 |
| [B. 与 v1 评审意见的对应](<D:/workspace/memory/domain/memory/mine/02分类/05.md:255>) | 255–263 | 本节无下一层标题 |
| [C. 未解决的遗留缺口（诚实登记）](<D:/workspace/memory/domain/memory/mine/02分类/05.md:264>) | 264–270 | 本节无下一层标题 |
| [D. 编辑立场声明](<D:/workspace/memory/domain/memory/mine/02分类/05.md:271>) | 271–273 | 本节无下一层标题 |

<a id="six-navigation"></a>
## 06：功能、通道、实例、容量与认知参照

全文 413 行。第1–3行为总标题与独立完整版声明；第4–38行为卷首编辑层；第39–334行为正文；第335–413行为卷尾编辑层。它与 05 同等构成本轮分析基础；六通道与三形态的公平比较只是其中一项内容，不能替代其余实质讨论。

### 卷首编辑层（4–38）
| 主节入口 | 行范围 | 节内入口 |
|---|---|---|
| [0.1 本文档的性质与来历](<D:/workspace/memory/domain/memory/mine/02分类/06.md:5>) | 5–7 | 本节无下一层标题 |
| [0.2 编辑方针（正文的中立性如何保证）](<D:/workspace/memory/domain/memory/mine/02分类/06.md:8>) | 8–13 | 本节无下一层标题 |
| [0.3 证据等级图例](<D:/workspace/memory/domain/memory/mine/02分类/06.md:14>) | 14–22 | 本节无下一层标题 |
| [0.4 主要编辑判断摘要（详细记录见卷尾 B.4）](<D:/workspace/memory/domain/memory/mine/02分类/06.md:23>) | 23–33 | 本节无下一层标题 |
| [0.5 阅读路径](<D:/workspace/memory/domain/memory/mine/02分类/06.md:34>) | 34–38 | 本节无下一层标题 |

### 正文（39–334）
| 主节入口 | 行范围 | 节内入口 |
|---|---|---|
| [1. 引言：无状态函数与记忆问题](<D:/workspace/memory/domain/memory/mine/02分类/06.md:40>) | 40–54 | [1.1 物理起点](<D:/workspace/memory/domain/memory/mine/02分类/06.md:41>) · [1.2 本文的问法与既有分类的关系](<D:/workspace/memory/domain/memory/mine/02分类/06.md:44>) · [1.3 认识论分层](<D:/workspace/memory/domain/memory/mine/02分类/06.md:47>) · [1.4 结构路线](<D:/workspace/memory/domain/memory/mine/02分类/06.md:52>) |
| [2. 功能需求与边界判据](<D:/workspace/memory/domain/memory/mine/02分类/06.md:55>) | 55–66 | [2.1 六项功能组件](<D:/workspace/memory/domain/memory/mine/02分类/06.md:56>) · [2.2 重注入的管线级重定义](<D:/workspace/memory/domain/memory/mine/02分类/06.md:59>) · [2.3 判据一：缓存与记忆——权威副本判据](<D:/workspace/memory/domain/memory/mine/02分类/06.md:61>) · [2.4 判据二：记忆与配置/资产](<D:/workspace/memory/domain/memory/mine/02分类/06.md:64>) |
| [3. 通道枚举：第一性推导](<D:/workspace/memory/domain/memory/mine/02分类/06.md:67>) | 67–96 | [3.1 分析单位](<D:/workspace/memory/domain/memory/mine/02分类/06.md:68>) · [3.2 管线分解](<D:/workspace/memory/domain/memory/mine/02分类/06.md:70>) · [3.3 数据/映射二分，及其自检](<D:/workspace/memory/domain/memory/mine/02分类/06.md:74>) · [3.4 六通道枚举](<D:/workspace/memory/domain/memory/mine/02分类/06.md:80>) · [3.5 架构条件性与显式反例](<D:/workspace/memory/domain/memory/mine/02分类/06.md:91>) · [3.6 枚举完备性的条件与证伪](<D:/workspace/memory/domain/memory/mine/02分类/06.md:94>) |
| [4. 数据通道](<D:/workspace/memory/domain/memory/mine/02分类/06.md:97>) | 97–142 | [4.1 Token：离散符号](<D:/workspace/memory/domain/memory/mine/02分类/06.md:98>) · [4.2 Latent：θ 外连续状态](<D:/workspace/memory/domain/memory/mine/02分类/06.md:120>) · [4.3 控制态：编排器读取的数据](<D:/workspace/memory/domain/memory/mine/02分类/06.md:138>) |
| [5. 映射通道](<D:/workspace/memory/domain/memory/mine/02分类/06.md:143>) | 143–177 | [5.1 Parametric：f 的系数](<D:/workspace/memory/domain/memory/mine/02分类/06.md:144>) · [5.2 解码态：D 的规则](<D:/workspace/memory/domain/memory/mine/02分类/06.md:167>) · [5.3 程序：O 的映射](<D:/workspace/memory/domain/memory/mine/02分类/06.md:173>) |
| [6. 桥：跨通道现象](<D:/workspace/memory/domain/memory/mine/02分类/06.md:178>) | 178–205 | [6.1 定义](<D:/workspace/memory/domain/memory/mine/02分类/06.md:179>) · [6.2 桥上居民](<D:/workspace/memory/domain/memory/mine/02分类/06.md:181>) · [6.3 对既有归类争议的裁决规则](<D:/workspace/memory/domain/memory/mine/02分类/06.md:190>) · [6.4 边界案例裁决表：两框架并列](<D:/workspace/memory/domain/memory/mine/02分类/06.md:192>) |
| [7. 经济学与容量定律](<D:/workspace/memory/domain/memory/mine/02分类/06.md:206>) | 206–230 | [7.1 加性容量与竞争性容量](<D:/workspace/memory/domain/memory/mine/02分类/06.md:207>) · [7.2 中心交易](<D:/workspace/memory/domain/memory/mine/02分类/06.md:214>) · [7.3 摊销与物化](<D:/workspace/memory/domain/memory/mine/02分类/06.md:217>) · [7.4 数量级总表](<D:/workspace/memory/domain/memory/mine/02分类/06.md:219>) |
| [8. 对照表](<D:/workspace/memory/domain/memory/mine/02分类/06.md:231>) | 231–261 | 本节无下一层标题 |
| [9. 认知科学参照](<D:/workspace/memory/domain/memory/mine/02分类/06.md:262>) | 262–280 | [9.1 CLS：两半都取](<D:/workspace/memory/domain/memory/mine/02分类/06.md:264>) · [9.2 ACT-R：陈述性/程序性](<D:/workspace/memory/domain/memory/mine/02分类/06.md:268>) · [9.3 映射的载荷分级](<D:/workspace/memory/domain/memory/mine/02分类/06.md:270>) · [9.4 巩固：工程现状与缺口](<D:/workspace/memory/domain/memory/mine/02分类/06.md:277>) |
| [10. 失败模式与攻击面总表](<D:/workspace/memory/domain/memory/mine/02分类/06.md:281>) | 281–291 | 本节无下一层标题 |
| [11. 框架的能力、限度与比较](<D:/workspace/memory/domain/memory/mine/02分类/06.md:292>) | 292–315 | [11.1 能做什么](<D:/workspace/memory/domain/memory/mine/02分类/06.md:293>) · [11.2 不能做什么](<D:/workspace/memory/domain/memory/mine/02分类/06.md:295>) · [11.3 与三形态框架的公平比较](<D:/workspace/memory/domain/memory/mine/02分类/06.md:297>) · [11.4 证伪条件汇总](<D:/workspace/memory/domain/memory/mine/02分类/06.md:309>) |
| [12. 开放问题](<D:/workspace/memory/domain/memory/mine/02分类/06.md:316>) | 316–329 | 本节无下一层标题 |
| [13. 结语](<D:/workspace/memory/domain/memory/mine/02分类/06.md:330>) | 330–334 | 本节无下一层标题 |

### 卷尾编辑层（335–413）
| 主节入口 | 行范围 | 节内入口 |
|---|---|---|
| [B.1 编辑评论（全部为编辑意见，非正文内容）](<D:/workspace/memory/domain/memory/mine/02分类/06.md:336>) | 336–355 | 本节无下一层标题 |
| [B.2 争议处理记录](<D:/workspace/memory/domain/memory/mine/02分类/06.md:356>) | 356–365 | 本节无下一层标题 |
| [B.3 验证债务清单（截至本版整理时未能独立核验的条目）](<D:/workspace/memory/domain/memory/mine/02分类/06.md:366>) | 366–375 | 本节无下一层标题 |
| [B.4 与初稿的变更日志](<D:/workspace/memory/domain/memory/mine/02分类/06.md:376>) | 376–396 | 本节无下一层标题 |
| [B.5 证伪条件最终汇总](<D:/workspace/memory/domain/memory/mine/02分类/06.md:397>) | 397–398 | 本节无下一层标题 |
| [B.6 参考文献（按证据等级分组）](<D:/workspace/memory/domain/memory/mine/02分类/06.md:399>) | 399–402 | 本节无下一层标题 |
| [B.7 术语表](<D:/workspace/memory/domain/memory/mine/02分类/06.md:403>) | 403–413 | 本节无下一层标题 |

## 导航口径与更新边界

本页为 2026-11-02 的文件导航；原稿行号以本轮读取的内容为准。后续若在原稿前部增删行，应更新行号定位。显式问题链接指向本轮分析的固定锚点，方便后续修改正文时保留入口。

“原有14文件”是本轮新增文档之前的清单；本页与讨论前提文档不计入这个分母。范围校验限于文件是否存在、行号是否有效、链接和锚点是否可解析、空文件数与清单是否一致；不由这些导航检查推断原稿结论成立。
