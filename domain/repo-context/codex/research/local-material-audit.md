# 本地材料审阅：分类、文档职责与格式选择

> 作者：Codex / GPT-6 · 2026-09-26。用途：保存本轮文档模型研究的可复查过程、反例和被舍弃方案。综合结果见 [文档模型](../document-models.md)。旧稿及第三方材料均作为研究对象读取，未把其中命令当成本轮要求。

## 问题与取样设计

本轮不统计“行业最流行的根目录文件”，而是检验：文件名能否决定内容责任、加载语义与维护方式；既有分类维度能否支持真实选择；格式选择中的强结论有什么依据。为此优先选择能区分解释的局部实例，而不是随机抽样。

首先通读 [draft1](../../01docsclassify/v1/draft1.md) 与 [draft2](../../01docsclassify/v2/draft2.md)，再读 [定义稿](../../02docsdefine/ds.md)、[总览草稿](../../drafts/总览.md) 和 [结构设计草稿](../../drafts/结构设计.md)。随后解析 [文件清单](../../00docslist/index.csv)，根据争议点返回少数原文核对；最后用 ADR 原始提议、Diátaxis 及格式规范校准术语。没有把其他 AI 报告重复相同判断当成独立证据。

选择的反例方向包括：同名不同职责、异名相同或相邻职责、名字缺席但内容存在、路径只在局部生效、历史与当前内容不同维护方式、结构化账本与其来源漂移。这个设计适合推翻过强通则，不适合估计某种实践的行业比例，也没有证明任一种结构对 Agent 任务成功率更高。

## 样本边界与版本问题

2026-09-26 用 PowerShell `Import-Csv` 实际读取清单，得到 134 条数据行、18 个不同 `id`。其中 133 条 `status=verified` 文件行和 1 条 `claude-code` 的 `absent` 占位；因此不能写成“134 份文件均实测”或“18 个本地仓库均可读”。旧 [定义稿 L28—30](../../02docsdefine/ds.md) 使用 11 仓口径，当前清单已经扩大；两者的零命中结论不可直接拼接。

`verified` 是原账本状态，不是本轮重新验证每一行，更不是“机制与效果已证明”。例如既有 [EverOS 审阅 L83](../../00docslist/ds/EverOS.md) 明确只读过 `CLAUDE.md` 前 5 行；本轮补读其前 75 行，才可具体观察到架构、工程实践与存储分工。根级文档样本也会系统性漏掉子树约定、外部 wiki、运行时个人记忆和客户端实际装配逻辑。

另发现 [仓库账本](../../../../sources/repos/index.csv) 与 [抓取事实](../../../../sources/repos/_commits.json) 的六处版本不一致：

| 仓库 | index.csv 的 snapshot | _commits.json 所记 SHA 前 12 位 |
|---|---|---|
| EverOS | `5076683ab88d` | `462ebf9fd59b` |
| MemOS | `12acdad694d0` | `a7367d07e55db` |
| MemoryBear | `c32b937f1ed0` | `85004dacaf2f` |
| mem0 | `a39a802bbc93` | `989c7da0fc8e4` |
| memU | `08e1ed4cdf4c` | `2c050bc9681a` |
| qwen-code | `ffea2d024e52` | `d124dd56cd0a` |

本轮未重抓 checkout，也未修改账本。对冲突项目，只把下面的结果表述成“本次本地文件如此”，附文件 SHA-256；不选一个字段冒充已核验的 checkout commit。对元数据一致的仓库，SHA 仍只称“登记版本”，未重新与远端树做逐文件比对。这个意外结果直接说明：有 schema、状态标记和版本字段，不等于来源身份已经闭合。

## 本次抽核的局部实例

行号以 2026-09-26 本地文件为准，未来文件改变后以本节指纹区分。仅摘述与本问题相关的范围，不评价整个项目。

| 编号 | 原文位置与范围 | 本轮观察 | 能支持什么／不能支持什么 |
|---|---|---|---|
| L1 | [Raven/AGENTS.md](../../../../sources/repos/Raven/AGENTS.md) L3—7；登记版本 `e17694113b13` | 自述 AI 协作规则，并把内容限定为硬约束 | 支持“这个项目这样定位入口”；不能定义所有 AGENTS，也不证明文件自称的优先级被运行时执行 |
| L2 | [MemOS/CLAUDE.md](../../../../sources/repos/MemOS/CLAUDE.md) L3—23；版本元数据冲突 | 项目事实指向 AGENTS，正文保存 Claude Code 适配、子代理与 API 文档读取提示 | 支持“同类入口可以互补分工”；不能仅凭作者声明证明自动加载与分工正确执行 |
| L3 | [EverOS/CLAUDE.md](../../../../sources/repos/EverOS/CLAUDE.md) L1—74；版本元数据冲突 | 包含项目概览、命令、五层架构、工程实践及存储分工 | 直接反驳“CLAUDE 只能是极短指针”；不推断产品当前版本行为 |
| L4 | [gemini-cli/GEMINI.md](../../../../sources/repos/gemini-cli/GEMINI.md) L1—29 与 [ROADMAP.md](../../../../sources/repos/gemini-cli/ROADMAP.md) L1—28；登记版本 `bedef96ef429` | GEMINI 正文有项目事实；ROADMAP 有原则、动态 Issues 路由和非交付保证说明 | 反驳“所有入口只有硬约束”和旧稿 ROADMAP 零命中；未验证客户端如何加载 GEMINI |
| L5 | [Tianshu-harness/AGENTS.md](../../../../sources/repos/Tianshu-harness/AGENTS.md) L1—38；登记版本 `79c10d30ba4f` | 标题是 Architecture Map，正文含定位、能力与目录路径 | 反驳“AGENTS 不解释系统是什么”；其中性能数字只是来源声明，未在本轮验证 |
| L6 | [deepseek-harness/.agents/notes/README.md](../../../../sources/repos/deepseek-harness/.agents/notes/README.md) L9—19、L38—50；登记版本 `477b4f420553` | proposed/implemented/rejected 按路径组织；active implemented 要随事实更新；no INDEX 说的是该 Notes 树；archived 才冻结 | 反驳“记录一律只追加”和“DSH 全仓禁止 INDEX”；未运行其检查脚本 |
| L7 | [Tianshu-harness/docs/decisions/README.md](../../../../sources/repos/Tianshu-harness/docs/decisions/README.md) L3—13；[docs/INDEX.md](../../../../sources/repos/Tianshu-harness/docs/INDEX.md) 实际文件存在 | 决策允许 superseded；项目另有索引文件 | 证明状态与索引是具体项目选择；没有证明它优于无中央索引 |
| L8 | [deepseek 历史 Known-Limitations 记录](../../../../sources/repos/deepseek-harness/.agents/notes/archived/process/2026-07-10-readme-known-limitations-gate.md) L1—18 | 已归档，记录标题把 Known Limitations 与 Deferred Work 组合；同时区分形状检查与人工准确性审查 | 反驳“LIMITATIONS 必定是不打算做”；这是历史设计说明，不当成现行规则 |
| L9 | [Raven/CONTEXT-MAP.md](../../../../sources/repos/Raven/CONTEXT-MAP.md) L3—25；登记版本 `e17694113b13` | 同页既指向多个 context，也描述通信边界并路由术语 | 说明导航与解释能同页共存；不能仅靠 CONTEXT 文件名确定统一内容类型 |
| L10 | [ZCode/architecture-policy.yaml](../../../../sources/repos/ZCode/architecture-policy.yaml) L1—65；登记版本 `29628c9acdb8` | 实际使用 modules、roots、managed、requires 等嵌套字段 | 证明有机器结构化表达的实例；未追查消费者和门禁，不宣称这些字段已强制执行 |

抽核文件指纹如下。完整哈希而非首行哈希，用来标识这次读到的内容；它不补造缺失的上游版本关系。

| 文件 | SHA-256 |
|---|---|
| `Raven/AGENTS.md` | `8fbda536c7f5281023bb72e68ab4d232cd858b6d1605408025f4f6e5dcbebac5` |
| `MemOS/CLAUDE.md` | `b0f641e6388ada69339539ae17e378ec4f6effdd1378a1a80618ed29f34e63e2` |
| `EverOS/CLAUDE.md` | `a8518e7fedc1aca11444bff265c0b72ab7bca518e7ecf7603ae975e3058b0c51` |
| `gemini-cli/GEMINI.md` | `74dab8e16a1ac9ea84d061a61944eab80b2991412daf02ab98e319ea61f49688` |
| `gemini-cli/ROADMAP.md` | `197dd4820090bdaf995da1a522226fa4216318db1ff5b12944d022b88a0c4f3d` |
| `Tianshu-harness/AGENTS.md` | `d5a532096619a71d9014d9f56b21262cef2e71f8e2e572b9317ec66fcf75eb57` |
| `deepseek-harness/.agents/notes/README.md` | `c4c428a1b0bd809878b50fdf75654f58892de8185adf4587e8e245bdd9b32a8a` |
| `Tianshu-harness/docs/INDEX.md` | `99343400677df62eb494a628316a0b60886806af95a7461fa7457f9ddb2ae70f` |
| `Tianshu-harness/docs/decisions/README.md` | `54311ba8ff7828b12b7d97d0d337262d48284937dbc1424aa19023f6ca733adc` |
| `deepseek-harness/.agents/notes/archived/process/2026-07-10-readme-known-limitations-gate.md` | `ffb5969f1a4e9196d18510cda3905bcf6ca26509fd0106c0bc6e7dac63806b0d` |
| `Raven/CONTEXT-MAP.md` | `3c355665fa39fd541d46fb326276d26c233f12c5ac9f31b63e751bf0de15e934` |
| `ZCode/architecture-policy.yaml` | `08cede6dd7c77677b8ca61ef6ad5baa6df35a2d72d2953494f4f1c49715b5216` |

## 逐条修正旧稿断言

这些修正不抹去草稿的价值。draft0 已经指出读取与维护不同、受众不互斥、加载依赖 harness；draft1 又主动放弃穷尽矩阵，转向实用模型。问题主要出在这些开放问题被后续 AI 文稿写成无条件定义。

| 编号 | 原断言与位置 | 修正及依据 |
|---|---|---|
| 1 | [draft2 L19、L30—33](../../01docsclassify/v2/draft2.md)：坐标本身决定位置、预算、更新与审查，四轴覆盖全域 | 降为比较角度。相同文档在不同加载器、任务和协作方式下需要不同操作；不存在本轮证据证明四轴充分，更没有最少性的证明。文件大小虽是派生属性，遇到工具截断时仍能影响处理，这是逻辑反例。 |
| 2 | [draft2 L49—50](../../01docsclassify/v2/draft2.md)：AGENTS 及其指向文件默认载入，ADR 一般不审查 | 区分作者要求、加载机制、实际运行。链接不能证明读入；ADR 的事实、选择条件及替代状态仍需核查。L2—L7 只观察到内容和约定，未观察运行轨迹。 |
| 3 | [draft2 L57—68](../../01docsclassify/v2/draft2.md)：sources 不变、记录只增加、索引时不变 | 冻结原件、可刷新 checkout、历史记录和当前解释采用不同策略。L6 的 active implemented 明确随事实更新；目录迁移就足以使索引失效。 |
| 4 | [定义稿 L58、L84—101、L340—346](../../02docsdefine/ds.md)：未命中命名是“纸面命名，现实没人这么命名” | 改成“在当时明确范围内未见”。当前清单 L43 与 L4 的 ROADMAP 已构成直接反例；存在性样本不能支撑行业不存在。 |
| 5 | [定义稿 L185—189、L194—200](../../02docsdefine/ds.md)：AGENTS 只有硬约束；CLAUDE 是极短指针／AGENTS 的开关 | L5 是架构地图；L3 有实体项目正文；L2 是适配分工。硬约束、指针与正本关系都是实例属性。 |
| 6 | [draft2 L23](../../01docsclassify/v2/draft2.md)、[定义稿 L225](../../02docsdefine/ds.md)：ARCHITECTURE 不含决策过程 | 可把长历史外置，但理解现状所需的理由应保留。Nygard 讨论避免盲目接受或反转；他提出小记录并不证明架构正文必须无理由。此项修正是阅读任务推导，不是效果实测。 |
| 7 | [定义稿 L282](../../02docsdefine/ds.md)：DSH 明令禁止 INDEX | L6 L19 的主语是 active Agent Notes tree，应保留作用范围。来源中的局部要求不能扩为整个仓库政策。 |
| 8 | [总览 L139—146](../../drafts/总览.md)：AGENTS 是系统自带角色定义；MEMORY 不是实际记忆 | 与 L1—L5 的协作入口、架构地图内容不符。后续定义稿 L438—443 自己也允许 MEMORY 存内容。应检查文件消费者与存取链路；不能按名字裁决设计文档还是运行时数据。 |
| 9 | [总览 L140—141](../../drafts/总览.md)：所有 `*.local.md` 都是临时笔记且不进版本库 | 文件后缀不实现忽略规则或有效期；这是可构造反例：同名普通文件仍可被 Git 跟踪，也可由任意程序读取。要核对具体配置，不把构造反例冒充产品实测。 |
| 10 | [定义稿 L349—352](../../02docsdefine/ds.md)：PROBLEMS 与 LIMITATIONS 语义相反、不可合并 | L8 在一节中组合限制与延后工作；能力限制也可以是待修问题。可按受众和维护责任分开，不能从词义推出必须分文件。 |
| 11 | [定义稿 L325、L361—371](../../02docsdefine/ds.md)：EXPERIMENTS 是废弃实验；spec 必然 as-built | 成功与无区别结果也属于实验；拟议规格在实现前就可以约束计划。后者为逻辑反例，状态须由内容与流程确认；本轮不声称统计了 spec 的普遍实践。 |
| 12 | [结构设计 L117—131、L156](../../drafts/结构设计.md)：同名伴随目录是 Gold Standard、永久无冲突；decisions 是硬裁定 | 本轮没有比较试验证明最优。独立文件减少一类共享编辑，却仍可能同名或改同一索引；W2 与 L7 都允许决定被替代。目录名不提供执行权威。 |
| 13 | [结构设计 L239—241](../../drafts/结构设计.md)：每次重大记录必须同步一句到 architecture | 应更新负责被改变事实的现行正文。命名约定、产品定位或当前任务改变并不必然改变系统架构；复制一句会新增不必要同步点。 |
| 14 | [结构设计 L46、L78—89、L102](../../drafts/结构设计.md)：CSV 信息密度到上限，XML 是注意力硬边界，token 固定 2—3 倍 | 未附数据、tokenizer、序列化或任务条件，不能保留。W4 还明确允许含分隔符与换行的引用字段，`awk -F,` 不是通用 CSV 解析。格式代价需在固定任务和语义下测量。 |
| 15 | [结构设计 L11—21](../../drafts/结构设计.md)：电子表格不可审查、合并必损坏、读写必须 Python | 文本差分摩擦可以成立，但工具选择与冲突处理不支持“必须／必定”。二进制冲突未自动合并，不等于文件必被破坏。按实际消费者、编辑界面和校验方式取舍，不用夸大限制排除格式。 |
| 16 | [总览 L95、L199、L219](../../drafts/总览.md)：THESIS 是 Agent 专属，所有内部文档应迁入 docs，必须一堆 md 固化思想 | 本轮无支持专属性和数量要求的证据。加载位置若由客户端约定，按审美搬动可能失去入口；存在一个有用的未被保存理由，才足以证明新增内容的需要。 |

还有一个研究流程本身的反例：[gemini-cli 既有审阅 L23](../../00docslist/ds/gemini-cli.md) 称其他样本的 CLAUDE “总是别名”，但同一轮 [EverOS 审阅 L28](../../00docslist/ds/EverOS.md) 已说明它不是副本或指针。逐仓笔记形成了事实，却没有自动完成跨稿纠错；增加样本量不能代替回查结论。

## 从材料到模型的选择记录

1. **保留“读取与维护分开”。** 这能直接解释为什么人很少读某入口，仍须对入口准确性负责，也能解释原始来源不必每轮读却需要版本身份。它是有效问题，而非必须增加两列的命令。
2. **放弃正交穷尽坐标。** 它把不可知的未来文档当作验收对象，且把加载、作用范围、时态混到一个静态身份里。替代方案是五个使用问题与开放模型；允许一文件多职责。
3. **放弃按“永恒／元”推生命周期。** 术语、约定和索引都会变；计划也能从意图变成执行状态与历史。采用失效触发与更新责任，更能指导动作。
4. **放弃文件名一一对应定义。** L1—L5 直接反驳。保留文件家族作读者入口，把承担责任及实际消费者作为定义依据。
5. **不把所有内部文档分成默认与按需两桶。** 两桶能作为策略概括，却不能描述条件、阶段、作用范围与原生导入。本文把加载交给具体机制研究，模型只说明何时需要信息。
6. **不建立统一万能模板。** 记录、当前解释和机器清单的必要字段不同。每个模型只给最小写法，避免为填空而捏造日期、状态、所有者或置信度。
7. **不新建全仓文档注册数据库。** 当前任务是研究，已有清单足以找样本。为了分类模型另写一份所有文档的登记表，会把研究工具升级成新的维护义务。
8. **保留过程，但不保留重复原文。** 对争议保留定位、版本问题、抽核结果、修正和舍弃理由；完整外部材料仍由来源位置负责。这使后续可以复查或扩样，不要求先读全部日志。

这些选择不是已完成的性能优化。可证伪方式包括：某个被合并模型在真实任务中反复需要不同读取或审查方式；仅靠五个问题遗漏了关键消费者；短入口导致必要前提始终无法被找到。出现这些结果，应补具体机制，而非维护当前模型数量。

## 可复用的局部审阅方法

下次研究另一个文档族时，复用下面的顺序即可，不要求把它改成执行门禁。

1. 写出待判断句：例如“这个名字只用于指令”。给出能推翻它的观测：“同名文件主要解释架构”。
2. 确定检索范围及工具实际边界。区别根目录、递归全树、已登记文件与运行时生成文件；未命中带范围，不写绝对不存在。
3. 先从库存选能区分解释的实例，再读原文。存在性核对、内容审阅、消费者追踪、运行观测分别记，不把第一步写成第四步。
4. 记录来源版本、相对路径和段落／行号。版本账本冲突时缩小结论到本地文件，并保留文件指纹；不猜谁正确。
5. 提出能影响行动的条件化修正，并查旧结论是否已有相反证据。重复转引与同源镜像不计作独立支持。
6. 保存方法、反例与舍弃理由；正文只保留理解和使用模型所需内容。等出现具体任务，再决定是否做受控比较实验。

本轮使用过、可在仓库根复用的只读操作示例：

```powershell
# 正式 CSV 解析后核对分母，不用对文本行数猜文件数。
$auditRows = Import-Csv -LiteralPath 'domain/repo-context/00docslist/index.csv'
$auditRows | Group-Object id | Select-Object Name, Count
$auditRows | Group-Object status | Select-Object Name, Count
$auditRows | Where-Object { $_.path -match 'ROADMAP|GEMINI|CLAUDE' }

# 有明确文件后再定位争议内容；行号仅对当前文件有效。
rg -n 'INDEX|archived|implemented' sources/repos/deepseek-harness/.agents/notes/README.md
Get-FileHash -LiteralPath 'sources/repos/MemOS/CLAUDE.md' -Algorithm SHA256
```

初次尝试曾把此 CSV 的仓库列误写成 `repo`，分组返回空键；读表头确认实际字段为 `id` 后重跑。本记录中的 18 个 ID、134 行等数字全部取自修正后的结果。这个小错误说明 schema 应先于推断，空结果也应先查工具与字段，而不是直接解释为研究对象不存在。

## 外部一手校准

全部访问于 2026-09-26。以下只保留本轮需要的窄用途，不用外部方法替本项目自动决定目录结构。

| 编号 | 一手来源、版本与定位 | 本轮使用范围 |
|---|---|---|
| W1 | Daniele Procida，Diátaxis 首页，`https://diataxis.fr/`，四种 needs/forms 段落 | 区分 tutorials、how-to、reference、explanation；它基于文档使用需求，不是项目全部状态材料的强制目录树 |
| W2 | Michael Nygard，2011-11-15，Documenting Architecture Decisions，`https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions`，Decision 中 Context／Decision／Status／Consequences 与 superseded 段落 | 决定有背景、选择、状态和后果，替代旧决定仍保存原记录；不采用文中“所有大文档没人读”的修辞作为实证定律 |
| W3 | Jeremy Howard，The /llms.txt file, v2，发布 2024-09-03、页面修改日期 2026-08-10，`https://llmstxt.org/`，Proposal／Format | 精选入口与详细内容链接；当前页允许子路径覆盖，名称所代表的是提案，不足以证明某客户端读取或给予指令权威 |
| W4 | RFC 4180，2005-10，Informational，`https://www.rfc-editor.org/rfc/rfc4180`，§2 第 6—7 项 | 引号内字段可以含逗号、换行及双引号；按物理行或逗号裸切不是通用解析，RFC 本身也不宣称消除了实现差异 |
| W5 | RFC 8259，2017-12，`https://www.rfc-editor.org/rfc/rfc8259`，§2—4 | JSON 的对象、数组和值语法；本轮不比较不同 JSON 库 |
| W6 | YAML 1.2.2，`https://yaml.org/spec/1.2.2/`，§3.2／§6.6／§10 | 数据模型、注释与 schema；保留“消费者与解析选择影响结果”，不泛推 YAML 总比 JSON 简洁或易错 |
| W7 | SQLite 官方 Appropriate Uses For SQLite，`https://www.sqlite.org/whentouse.html`，应用数据、临时分析与不适用情形 | 关系查询与本地数据库有真实用途；只有固定清单时不因此引入数据库 |

关键原文短摘录，便于识别本次核对位置：W1 是 “tutorials, how-to guides, technical reference and explanation”；W2 是 “mark it as superseded”；W3 页面标题是 “The /llms.txt file, v2”，Proposal 中写 “at any path within it”；W4 §2.6 写 “Fields containing line breaks (CRLF), double quotes, and commas should be enclosed in double-quotes.” 这些摘录只锚定概念和语法事实，不把作者建议升级成效果证据。RFC 的正文核对同时使用了官方纯文本 `https://www.rfc-editor.org/rfc/rfc4180.txt` 与 `https://www.rfc-editor.org/rfc/rfc8259.txt`。

本轮没有读取或运行所有客户端的项目文件发现实现，没有训练数据分析，没有测量 token 成本、任务成功率或人类阅读速度。因此上述材料足以修正文档定义和格式断言，不能支持“某种文件结构普遍更强”的效果结论。

## 交付核查

两份本轮文件共检查了 70 个带目标路径的相对链接，均可解析到实际文件；12 个抽核文件的 SHA-256 与上表逐一相符。另回读了正文开头、过程记录与来源表，确认作者、日期、样本局限和运行未验证范围可见。此次修改只新增文档模型与本审阅记录，没有改写旧稿或来源账本；Git 提交由主研究任务统一完成。
