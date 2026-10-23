# AGENTS.md 最佳实践

**为 AI 编程代理编写项目根目录指令文件的内容结构、优先级机制、成本证据、失效模式与跨工具兼容策略**

**报告日期：2026年10月4日**

## 摘要

AGENTS.md 由 Linux 基金会下属 Agentic AI Foundation 托管，是纯 Markdown、无 Schema、无必填字段的跨工具开放标准，写法质量决定成败，没有校验层可兜底。内容取舍的唯一判据是「代理能否自行推断」：通用技术栈描述、标准目录结构、与既有文档重复的内容和抽象质量要求都是噪声；非标准工具选型、反直觉架构决策、版本锁定与已知的坑才有价值。嵌套遵循就近优先，逐级追加、冲突时更具体者覆盖；`AGENTS.override.md` 是完全跳过而非合并，且属 Codex 特有实现，不在官方规范内。完整优先级链为：用户显式指令 > 子目录文件 > 根目录文件 > 工具默认配置。

成本证据呈两侧分化：Lulla et al. (2026) 在 10 个仓库、124 个 PR 上测得运行时间中位数 -28.64%、输出 Token 中位数 -16.58%（p<0.05）；Gloaguen et al. (2026) 测得 LLM 生成文件使成功率下降 0.5%-2%、推理成本上升 20%-23%，人工编写成本上升 19%、成功率 +2.4%（不显著）。前者降的是输出侧，后者增的是输入侧，净收益由内容质量决定；缓存读取比标准输入便宜 90% 是主要缓解手段。四类失效模式中，规则膨胀与静默丢失分别指向「不要每次犯错就加规则」和「关键规则放开头、长任务开新会话」。跨工具方面，没有任何两个工具以完全相同的方式读取它：Gemini CLI 需显式配置文件名，Continue 文档未提及支持，Claude Code 以 AGENTS.md 为回退项。多工具环境应以 AGENTS.md 为唯一事实来源，用一行 `@AGENTS.md` 桥接 Claude Code，并把工具特定规则分离到各自专属目录。

## 1. 标准身份与定位：AGENTS.md 是给代理读的操作手册，不是给人的 README

### 1.1 它由谁托管、约束力有多强

AGENTS.md 是由 Linux 基金会下属 Agentic AI Foundation 托管的跨工具开放标准，目标是为 AI 编程代理提供统一的项目级指令[agents.md](https://agents.md/)。这个身份带来两个直接影响本报告后续全部结论的性质。

第一，它是跨工具标准而非某家产品的私有配置文件。这意味着一份写好的根目录指令文件可以同时被多家代理读取，也让「以 AGENTS.md 为唯一事实来源」成为可行的工程策略，而不只是理想化的建议。

第二，它采用纯 Markdown 格式，没有强制 Schema，也没有必填字段，代理解析的是文本语义本身[agents.md](https://agents.md/)。这一点常被低估：因为没有校验器，写错了不会报错。字段拼错、命令写漏 flag、约束描述含糊，都不会在提交时被任何工具拦下——它们只在代理实际执行任务时以错误行为的形式暴露出来。换句话说，AGENTS.md 的正确性完全依赖写法本身的质量，这是「最佳实践」这个说法在这个对象上有实质内容的原因：不存在一个可以自动兜底的格式层。

同一份文件的定位是「给 AI 看的项目操作手册」，与面向人类的 README.md 互补而非替代[agents.md](https://agents.md/)。它不试图成为项目文档的全集，而是承担一个窄得多、也硬得多的职责：告诉代理在这个仓库里怎么把事情做对。

### 1.2 定位差异：README 给人看，AGENTS.md 给代理看

两份文件回答的是不同的问题。README.md 面向新接触项目的人，承担项目介绍、快速上手与基本描述；AGENTS.md 面向要动手改代码的代理，承担构建与测试命令、反直觉的约定、以及明确的禁忌项。

这个区分不是修辞上的分工，它决定了内容取舍的判据。README 里合理的「本项目是一个基于 X 框架的 Y 系统」这类介绍性文字，放进 AGENTS.md 就是纯消耗——代理不需要被介绍，它需要被指示。反过来，README 里通常不会写的「测试必须带某个特定 flag 才能跑通」「这个目录禁止编辑」，恰恰是 AGENTS.md 里价值密度最高的内容。

需要单独澄清的一点是覆盖关系：README.md 与其他文档和 AGENTS.md 是互补关系，不参与指令覆盖链[wsisp.com](https://www.wsisp.com/helps/91061.html)。也就是说，即便 README 与 AGENTS.md 在某个说法上不一致，代理也不会因为「README 更权威」或「README 更新更近」而改变行为——只有 AGENTS.md 系列文件和用户在对话中的显式指令构成覆盖链。这一点在多份文档并存、更新节奏不同的仓库里尤其重要：把行为约束写进 README 是无效的治理动作。

## 2. 内容结构：只写代理推断不出来的东西

### 2.1 六个高信噪比段落

由于没有 Schema，段落划分完全靠约定。官方规范与生产实践收敛出六个板块，构成高信噪比的基础结构。其中构建与测试命令应放在文件靠前位置，并提供单文件级别的检查命令以替代全量构建[volcengine.com](https://developer.volcengine.com/articles/7549123386920665130)——这条位置要求有明确的机制依据：代理在长上下文中更容易保留靠前位置的指令（详见第 5 章的静默丢失问题）。

**表1：AGENTS.md 的六个推荐段落**

| 段落名称 | 核心内容要求 | 编写要点 |
| :--- | :--- | :--- |
| 项目概述 | 技术栈精确到版本、依赖、架构分层简述 | 仅写代理无法从 `package.json` 或目录结构推断的信息；避免冗余描述[dev.to](https://dev.to/aileenvl/stop-burning-tokens-on-redundant-context-why-your-agentsmd-is-failing-3cpn) |
| 构建与测试命令 | 安装、构建、测试、Lint 的精确命令及完整 Flag[掘金](https://juejin.cn/post/7569532841870540826) | 放在文件靠前位置；提供单文件级别的检查命令以替代全量构建[volcengine.com](https://developer.volcengine.com/articles/7549123386920665130) |
| 代码风格与约定 | 命名规范、缩进、导入顺序、异常处理模式 | 使用祈使句（「必须」「禁止」）；提供好/坏代码片段对比优于文字描述 |
| 安全与权限边界 | 允许自动执行与需确认的操作清单；禁止项（硬编码密钥、跨层依赖） | 采用三级优先级体系（CRITICAL > IMPORTANT > GUIDANCE）[augmentcode.com](https://www.augmentcode.com/guides/how-to-build-agents-md) |
| 目录约定与禁区 | 目录职责、新代码存放位置、禁止编辑的目录 | 仅记录非标准或反直觉的目录约束；标准框架约定无需赘述[augmentcode.com](https://www.augmentcode.com/guides/how-to-build-agents-md) |
| PR 与提交规范 | 分支策略、提交信息格式、PR 检查清单[掘金](https://juejin.cn/post/7569532841870540826) | 明确验收标准（测试通过、Lint 通过、Diff 范围）[volcengine.com](https://developer.volcengine.com/articles/7549123386920665130) |

表格中有两处写法值得单独说明。一是代码风格段落建议「提供好/坏代码片段对比优于文字描述」，理由在于代理的模仿能力强于对抽象形容词的执行力——一段被标记为「不要这样写」的真实代码，比三句描述性规范更能约束生成结果。二是安全段落采用三级优先级体系（CRITICAL > IMPORTANT > GUIDANCE）[augmentcode.com](https://www.augmentcode.com/guides/how-to-build-agents-md)，这实际上是在没有 Schema 的条件下，用文本约定人为重建了一套优先级语义，让代理在冲突时有裁量依据。

### 2.2 隐形逻辑优先：什么不该写、什么 ROI 最高

六个段落是骨架，但骨架里填什么由一条判据决定：ETH Zurich 的研究明确指出，AGENTS.md 应仅包含「非可推断细节」（Non-Inferable Details）[augmentcode.com](https://www.augmentcode.com/guides/how-to-build-agents-md)。判据是一个反事实问题——如果这一行删掉，代理能否通过读代码自己发现同样的信息？能发现的就是噪声，不能发现的才值得占位。

**表2：不应写入与应当写入的内容对照**

| 方向 | 内容 | 判定理由 |
| :--- | :--- | :--- |
| 不应写入 | 通用的技术栈描述 | 代理可通过读取 `package.json`、`Cargo.toml` 自行发现[dev.to](https://dev.to/aileenvl/stop-burning-tokens-on-redundant-context-why-your-agentsmd-is-failing-3cpn) |
| 不应写入 | 标准的目录结构说明 | 若项目遵循框架默认约定（如 Next.js 的 `app/` 目录），无需重复描述[augmentcode.com](https://www.augmentcode.com/guides/how-to-build-agents-md) |
| 不应写入 | 已有的文档内容 | 与 README 或现有文档重复的内容会被视为噪声，稀释模型注意力[dev.to](https://dev.to/aileenvl/stop-burning-tokens-on-redundant-context-why-your-agentsmd-is-failing-3cpn) |
| 不应写入 | 抽象的质量要求 | 「写好代码」「注意性能」这类描述无法验证[博客园](https://www.cnblogs.com/mliu/p/20089537) |
| 应当写入 | 非标准工具选型 | 如使用 Pixi 而非 pip，或使用内部自研构建工具[augmentcode.com](https://www.augmentcode.com/guides/how-to-build-agents-md) |
| 应当写入 | 反直觉的架构决策 | 如「API 客户端不抛异常」或「legacy 模块不可重构但 CI 依赖它」[dev.to](https://dev.to/aileenvl/stop-burning-tokens-on-redundant-context-why-your-agentsmd-is-failing-3cpn) |
| 应当写入 | 特定的版本锁定 | 防止代理使用训练数据中更常见但不兼容的版本[augmentcode.com](https://www.augmentcode.com/guides/how-to-build-agents-md) |
| 应当写入 | 已知的坑与避坑指南 | 如废弃 API、时区处理陷阱这类代理反复犯错的问题 |

这张表的两列有一个共同的深层逻辑：代理的先验来自训练数据，而训练数据反映的是社区中的通行做法。因此凡是「通行做法」的内容，代理本来就会做对，写进文件是浪费；凡是「本仓库偏离通行做法」的内容，代理默认会做错，写进文件才产生价值。版本锁定这一项是此逻辑最锋利的例子——代理会倾向于使用它在训练数据中见得最多的版本，而不是本仓库实际锁定的版本，这个偏差只能靠显式声明纠正。

「不可验证」这条排除标准同样值得展开。抽象质量要求之所以是噪声，不只是因为它信息量低，而是因为它无法被执行也无法被检查：写了「注意性能」之后，没有任何一步可以判定代理是否遵守了它。这类条目占用的行数与真正可执行的约束完全等价，却换不来任何行为改变。

综合起来就是「地图而非手册」原则：AGENTS.md 标出代理自己找不到的路，而不是把整个地形抄一遍。这一原则同时也是第 4 章成本分析的落脚点——篇幅之所以是硬约束而非风格偏好，正是因为它按 token 计费。

## 3. 嵌套、覆盖与优先级链

### 3.1 层级加载与就近优先

AGENTS.md 支持多层级配置，核心机制为「就近优先」（Proximity Priority）：距离被编辑文件最近的 AGENTS.md 优先级最高。代理处理请求时按四层顺序构建指令链。

第一层是全局层，如 `~/.codex/AGENTS.md`（或其他工具对应的全局路径），定义个人通用偏好。第二层是项目根目录下的 `AGENTS.md`，定义项目级约束。第三层是子目录层级，从根目录向当前工作目录逐级查找，每一级的 AGENTS.md 依次追加。第四层是合并规则：非冲突配置自动合并（如列表类配置追加）；冲突配置由后出现的、更具体的那一份覆盖先出现的、更通用的那一份[掘金](https://juejin.cn/post/7556911205156749322)。

需要区分「拼接」与「覆盖」这两种行为。逐级追加意味着子目录文件不会让根目录文件失效，两者叠加生效；只有在真正冲突时，就近的那一份才胜出。这个设计让 monorepo 可以用一份根文件承载全仓库通用约束，再在个别子目录里只写差异，而不必复制整份内容。

### 3.2 Override 机制与其工具特异性

OpenAI Codex 原生支持 `AGENTS.override.md`，其优先级高于同级 `AGENTS.md`。语义上有一个容易被忽略的细节：当 override 文件存在时，同级 AGENTS.md 被完全跳过，而非合并[神马](https://page.sm.cn/blm/midpage-317/index?h=iknow.v6_2.quark.cn&id=28_d818afb69400326b370ba870388e171a)。这与 3.1 中的逐级追加机制性质不同——override 是替换，不是叠加。

该机制适用于三类场景。一是临时全局覆写：在 `~/.codex/AGENTS.override.md` 设置临时指导，完成后删除即恢复原配置[w3cschool.cn](https://www.w3cschool.cn/aicodingguide/codex-agents-md.html)。二是子目录特殊规则：如支付服务目录需要完全不同的测试命令和安全约束[w3cschool.cn](https://www.w3cschool.cn/aicodingguide/codex-agents-md.html)。三是个人定制：社区惯例将 `AGENTS.override.md` 加入 `.gitignore`，用于存放个人偏好（如 pnpm 与 npm 的选择）而不影响团队共享配置[wsisp.com](https://www.wsisp.com/helps/91061.html)。

必须标注边界：`AGENTS.override.md` 并非 AGENTS.md 官方规范的一部分，而是 Codex 特有的实现；其他工具可能不支持此文件名[wsisp.com](https://www.wsisp.com/helps/91061.html)。因此在跨工具仓库里依赖 override 机制会产生只对一家生效的配置，团队其余成员的代理读到的仍是原文件。把它写进治理规范前，应先确认团队实际使用的工具集合。

### 3.3 完整优先级链

把嵌套规则与用户指令合起来，完整的优先级从高到低为四级：用户在聊天中的显式指令（覆盖一切）、最近的子目录 AGENTS.md、根目录 AGENTS.md、工具默认配置。

第一级的含义需要说清楚：文件里写的内容永远可以被对话中的指令临时推翻，这是设计意图而非漏洞——它让代理在探索性任务中不必被既有约束锁死。但反过来，这也意味着任何指望「写进文件就一定被执行」的强约束，其保证强度受限于代理对文件内容的注意力，而不受文件本身保护。真正需要不可绕过的约束（如禁止操作某目录），更可靠的落点是 CI、hooks 或权限配置，而非指令文件——第 5 章的知识升级流程会把这一点变成明确判据。

README.md 与其他文档不参与此覆盖链[wsisp.com](https://www.wsisp.com/helps/91061.html)，因此这条四级链是 AGENTS.md 家族内部加上用户指令与工具默认值的封闭体系。

## 4. 长度控制与 token 成本的实证量化

### 4.1 各工具的长度阈值与硬限制

AGENTS.md 在每次会话启动或每条消息中被加载，直接计入输入 token 消耗，因此长度控制是成本与效果变量，而不只是排版偏好。根目录文件建议控制在 100-200 行以内；超过 150-200 行时应考虑拆分至子目录[augmentcode.com](https://www.augmentcode.com/guides/how-to-build-agents-md)。

各工具的限制性质不同，需要区分「建议值」与「硬限制」——前者超出只是浪费，后者超出会触发截断或跳过，行为会静默改变。

**表3：各工具对指令文件的长度限制**

| 工具 | 限制 | 性质 |
| :--- | :--- | :--- |
| OpenAI Codex | 合并后的指令总大小默认上限 32 KiB，超出部分按加载顺序从末尾截断，可通过 `project_doc_max_bytes` 调整[神马](https://page.sm.cn/blm/midpage-317/index?h=iknow.v6_2.quark.cn&id=28_d818afb69400326b370ba870388e171a) | 硬限制（可配置） |
| Google Antigravity | 单文件 12,000 字符[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 硬限制 |
| Claude Code | 单文件建议低于 200 行，超过 4 MiB 的文件会被跳过[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 行数为建议，4 MiB 为硬限制 |
| Cursor | 规则文件建议低于 500 行[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 建议值 |

Codex 的 32 KiB 上限特别值得注意，因为它约束的是**合并后**的总大小——第 3 章的逐级追加机制会把全局层、根目录与各子目录文件拼在一起，单份文件不超限不代表合并结果不超限。而「从末尾截断」意味着超限时代价落在最后加载的那一份上，通常是最近、最具体的子目录文件，也就是针对性最强的内容反而最先丢失。

### 4.2 两篇实证研究的成本数据

关于「写 AGENTS.md 是否划算」，两篇 2026 年的实证研究给出了方向相反的结论。它们测的其实不是同一件事。

**表4：两篇实证研究的口径与测量结果对照**

| 指标 | Lulla et al. (2026)[arXiv](https://arxiv.org/pdf/2601.20404.pdf) | Gloaguen et al. (2026)[arXiv](https://arxiv.org/pdf/2602.11988.pdf) |
| :--- | :--- | :--- |
| 样本规模 | 10 个仓库，124 个 PR | SWE-BENCH + CTXBENCH，多 Agent 多 LLM |
| 上下文类型 | 开发者编写的 AGENTS.md | LLM 生成与开发者编写两组对照 |
| 运行时间 | 中位数 -28.64% (p<0.05) | 未直接报告 |
| 输出 Token | 中位数 -16.58% (p<0.05) | 未直接报告 |
| 推理成本 | 未直接报告 | LLM 生成 +20%~23%，人工编写 +19% |
| 推理步骤 | 未直接报告 | LLM 生成 +2.45~3.92 步，人工编写 +3.34 步 |
| 任务成功率 | 未量化（人工抽检质量相当） | LLM 生成 -0.5%~-2%，人工编写 +2.4%（不显著） |

两组数字都带着各自的限定条件，引用时不能剥离。Lulla 的 -28.64% 与 -16.58% 是**中位数**变化，样本为 10 个仓库、124 个 PR，显著性标注 p<0.05，且只覆盖开发者编写的文件；该研究对任务成功率未做量化，只有人工抽检显示质量相当[arXiv](https://arxiv.org/pdf/2601.20404.pdf)。Gloaguen 的百分比变化基于 SWE-BENCH 与 CTXBENCH 两套基准、多 Agent 多 LLM 设置，其中人工编写带来的 +2.4% 成功率提升被明确标注为**不显著**[arXiv](https://arxiv.org/pdf/2602.11988.pdf)。

### 4.3 综合判断：净收益由内容质量决定

两项研究看似矛盾，实则测量了成本结构的不同侧。AGENTS.md 能显著降低的是**输出侧**消耗：Lulla 的研究表明，提供明确的仓库结构和约定可减少代理的探索性导航和重复请求，从而降低输出 Token 和运行时间[arXiv](https://arxiv.org/pdf/2601.20404.pdf)。而**输入侧**成本必然增加：无论内容质量如何，AGENTS.md 本身作为额外上下文都会增加输入 Token 和推理步骤[arXiv](https://arxiv.org/pdf/2602.11988.pdf)。

把两侧合起来，净收益由内容质量决定。LLM 自动生成的文件因与现有文档冗余，导致负收益——成本增加且成功率下降；人工编写的文件虽增加输入成本，但通过减少无效探索实现了输出侧的更大节省，成功率也有边际提升[arXiv](https://arxiv.org/pdf/2602.11988.pdf)。这与第 2 章的「非可推断细节」判据严丝合缝：自动生成之所以是负收益，恰恰因为它生成的正是代理本来就能自己发现的那些内容——付了输入成本，换不到探索节省。

输入侧成本还有一个明确的缓解手段：缓存读取比标准输入便宜 90%，频繁使用的 AGENTS.md 应确保能被缓存命中[augmentcode.com](https://www.augmentcode.com/guides/how-to-build-agents-md)。这给出一条与「写短一点」不同的优化路径——文件内容稳定、加载位置固定，才更容易命中缓存；频繁改动指令文件会同时付出直接 token 成本与缓存失效成本。

需要标注这两组数字的适用边界：它们测量的是「有无/何种来源的指令文件」对成本的影响，都没有给出「多少行是最优」的剂量-反应曲线。因此 100-200 行的建议阈值来自工程实践与工具限制，而非这两项研究的实测最优点。

## 5. 失效模式与维护方式

### 5.1 四类失效模式

**表5：四类失效模式的成因与后果**

| 失效模式 | 成因 | 可观测后果 |
| :--- | :--- | :--- |
| 自动生成文件的负效应 | 生成内容与代理已能独立发现的文档冗余 | 在 8 个实验设置中的 5 个降低任务成功率，增加噪声而非信号[augmentcode.com](https://www.augmentcode.com/guides/how-to-build-agents-md) |
| 规则膨胀与矛盾积累 | 每次代理犯错就新增规则，但从不删除旧规则 | 文件累积矛盾的补丁和一次性修复；更多规则并不产生更好表现[augmentcode.com](https://www.augmentcode.com/guides/how-to-build-agents-md) |
| 长会话中的静默丢失 | 上下文增长导致中间位置指令被忽略 | 保留架构决策但丢弃具体约束[augmentcode.com](https://www.augmentcode.com/guides/how-to-build-agents-md) |
| 过时结构描述的误导 | 代码库变更后目录结构描述未同步 | 成为负债，增加推理成本并鼓励无效的广泛文件遍历[augmentcode.com](https://www.augmentcode.com/guides/how-to-build-agents-md) |

四类失效中有两类值得展开，因为它们的机制指向不同的对策。

规则膨胀是**主动**对抗上下文工程的行为模式：每次失败就加一条规则，是最自然的应激反应，但它单调增加文件长度、从不减少，且新规则常与旧规则形成局部矛盾。「更多规则并不产生更好表现」[augmentcode.com](https://www.augmentcode.com/guides/how-to-build-agents-md) 这个结论直接否定了「把文件写全一点更安全」的直觉——超过某个点之后，增加条目是在降低而非提高遵循率。

静默丢失（Lost in the Middle）解释了为什么第 2 章要求构建命令放在文件靠前位置：随着上下文增长，代理可能忽略中间位置的指令，保留架构决策但丢弃具体约束[augmentcode.com](https://www.augmentcode.com/guides/how-to-build-agents-md)。对策有两条——关键规则放在文件开头，长任务应开启新会话[augmentcode.com](https://www.augmentcode.com/guides/how-to-build-agents-md)。这条机制也解释了表 3 中 Codex「从末尾截断」为何格外有害：超限被截掉的内容与因位置靠后而被忽略的内容，恰好是同一批。

过时结构描述这一类的特殊性在于：它是**时间**造成的失效，写法再正确也会随代码演进而腐坏。这与前 2 章讨论的「怎么写」是不同维度的问题，只能靠维护流程解决。

### 5.2 维护流程与知识升级判据

维护的起点是抑制写入冲动：仅在观察到可复现的失败后才补充对应约束，避免一次性写入大量推测性规则。这与 5.1 的膨胀模式正好相反——从错误中迭代，而非预先堆砌。

AGENTS.md 应纳入 Git 版本控制，作为项目资产，其更新应像代码变更一样经过 Review。这一步把指令文件从「随手改的说明」提升为「受控制品」，也让 5.1 中的矛盾积累变得可追溯。

防膨胀可以自动化：在 CI 中检查 AGENTS.md 行数（如不超过 100 行），超出则阻断并要求把内容迁移至 Spec、Wiki 或 Skill[掘金](https://juejin.cn/post/7685944661652602914)。

更重要的是知识升级流程，它给出「一条经验该落到哪里」的判据：一次问题 → 记录现象 → 判断是否可复现 → 验证解决方式 → 决定进入 Wiki、Skill 还是硬规则。其中有一条排除规则格外锋利：**能由 lint、CI 或 hooks 拦截的规则不要进 AGENTS.md**[掘金](https://juejin.cn/post/7685944661652602914)。这条判据与第 3.3 节的推论一致——指令文件是软约束，可被用户对话指令覆盖，也受注意力衰减影响；凡是能被机器强制执行的约束，放到强制执行的位置才真正可靠。指令文件应当保留的是那些无法被机器检查、只能靠代理理解与判断的内容。

配套的定期审计动作包括：检查规则是否在多处重复（可用 `grep -rn "规则关键词"`）、移除不再适用的约束、验证 Skill 是否真的被触发[掘金](https://juejin.cn/post/7685944661652602914)。最后一项尤其容易被跳过——配置了 Skill 不等于它被加载过，这与第 4.2 节「人工编写才有效」的结论共同指向同一个方法要求：治理动作需要可观测的验证环节，而不是写完就算生效。

还有一条操作层面的事实：修改 AGENTS.md 后需开启新对话或重启工具，现有对话不会自动应用更新。这意味着调试指令文件时，若不重开会话就观察行为，得到的是旧配置的结果，容易误判修改无效。

## 6. 跨工具兼容差异与桥接策略

### 6.1 没有任何两个工具以完全相同的方式读取 AGENTS.md

尽管 AGENTS.md 已被 20+ 工具支持[getunblocked.com](https://getunblocked.com/blog/claude-md-vs-agents-md-vs-cursor-rules/)，各工具在读取哪些文件、是否支持嵌套、大小限制、每轮是否发送、以及特殊行为上都有差异。资料给出的总判断很直接：**没有任何两个工具以完全相同的方式读取 AGENTS.md**[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what)。

**表6：九款工具读取指令文件的差异对照**

| 工具 | 读取的文件 | 嵌套支持 | 大小限制 | 每轮发送 |
| :--- | :--- | :--- | :--- | :--- |
| OpenAI Codex | `AGENTS.override.md` > `AGENTS.md` > 配置的备选名；每目录最多一个[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 支持，从根到工作目录逐级拼接[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 32 KiB 硬限制（可配）[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 每次运行构建一次[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) |
| Cursor | `.cursor/rules/**/*.mdc` 加根目录与子目录 `AGENTS.md`[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 支持，AGENTS.md 按目录、.mdc 按 glob[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 建议低于 500 行（非硬限）[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 应用于模型上下文开头[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) |
| GitHub Copilot | `.github/copilot-instructions.md`、`.instructions.md`、`AGENTS.md`、`CLAUDE.md`、`GEMINI.md`[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 支持，AGENTS.md 就近胜出[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 未文档化[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 是，每条消息[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) |
| Claude Code | `CLAUDE.md` 系列优先；无 CLAUDE.md 时读 `AGENTS.md`[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 支持，父级启动加载、子级按需加载[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 建议低于 200 行；超过 4 MiB 跳过[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 会话启动加载[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) |
| Devin Desktop (原 Windsurf) | `AGENTS.md` / `agents.md` 加 `.devin/rules/`、`.windsurf/rules/`[devin.ai](https://docs.devin.ai/desktop/cascade/agents-md) | 支持，根目录为 always-on、子目录按 glob `<dir>/**`[devin.ai](https://docs.devin.ai/desktop/cascade/agents-md) | 未文档化 | 根目录内容每条消息包含[devin.ai](https://docs.devin.ai/desktop/cascade/agents-md) |
| Cline | `.clinerules/`、`.cline/rules/`、`.cursorrules`、`.windsurfrules`、`AGENTS.md`[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 未文档化为目录遍历；按路径 glob 作用域[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 未文档化（警告消耗上下文）[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 是，每条规则每次请求加载（除非条件限定）[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) |
| Gemini CLI | 默认 `GEMINI.md`；需在 settings 中配置 `context.fileName` 才读 AGENTS.md[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 支持，工作区及父级启动加载加即时读取[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 未文档化[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 是，每条提示[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) |
| Google Antigravity | `GEMINI.md`、`AGENTS.md`、`.agents/rules/*.md`[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 未文档化[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 12,000 字符硬限制[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 提示扩展时注入[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) |
| Continue | `.continue/rules/*.md` 加 config.yaml[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 未文档化[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | 未文档化[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) | Agent/Chat/Edit 请求适用[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) |

表中「未文档化」出现多次，这本身是重要信息：它不等于「没有限制」或「不支持」，只代表该行为在工具官方文档中没有记载。跨工具仓库若要依赖某项具体行为，需要自行实测，不能从沉默中推断结论。

三处容易踩空的差异值得单独点出。第一，Gemini CLI 默认读 `GEMINI.md`，需要显式配置才会读 AGENTS.md[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what)——不配置则文件根本不生效。第二，Continue 的文档未提及 AGENTS.md 支持[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what)，把它纳入「20+ 工具支持」的统计里做假设是危险的。第三，Claude Code 是 `CLAUDE.md` 系列优先，无 CLAUDE.md 时才读 `AGENTS.md`[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what)，即 AGENTS.md 在这里是**回退项**而非首选；该行为自 v2.1.277 起支持，也可配置为同时读取两者[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what)。

另有一项与产品演进相关的信息：Windsurf 于 2026.6.2 退役并更名为 Devin Desktop[skills-hub.ai](https://skills-hub.ai/blog/devin-desktop-acp-2026)，Devin Local 通过 CLI 规则系统读取[devin.ai](https://docs.devin.ai/desktop/cascade/agents-md)；Gemini CLI 的托管版已于 2026.6.18 退役[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what)。兼容矩阵是时变的，引用时应带日期。

### 6.2 多工具环境下的兼容策略

对使用多个 AI 编程工具的团队，推荐五条策略[getunblocked.com](https://getunblocked.com/blog/claude-md-vs-agents-md-vs-cursor-rules/)。

第一，以 AGENTS.md 为唯一事实来源。它是覆盖面最广的标准文件，Codex、Cursor、Copilot、Devin/Windsurf、Cline 均原生支持[getunblocked.com](https://getunblocked.com/blog/claude-md-vs-agents-md-vs-cursor-rules/)。

第二，为 Claude Code 创建桥接文件：在项目根目录创建 `CLAUDE.md`，内容仅为一行 `@AGENTS.md`，利用 Claude Code 的导入功能指向同一份内容[getunblocked.com](https://getunblocked.com/blog/claude-md-vs-agents-md-vs-cursor-rules/)；该导入机制最多支持 4 层[getunblocked.com](https://getunblocked.com/blog/claude-md-vs-agents-md-vs-cursor-rules/)。另一条路径是在 v2.1.277 及以后版本中通过 `/config` 设置启用 AGENTS.md 回退读取[CSDN](https://blog.csdn.net/2401_88139521/article/details/166133383)。

第三，为 Gemini CLI 配置文件名：在 `.gemini/settings.json` 中设置 `{ "context": { "fileName": "AGENTS.md" } }`[agents.md](https://agents.md/)。

第四，删除遗留文件：`.cursorrules` 已被 Cursor 官方标记为 legacy，应迁移至 `.cursor/rules/*.mdc` 或直接由 AGENTS.md 替代[getunblocked.com](https://getunblocked.com/blog/claude-md-vs-agents-md-vs-cursor-rules/)。

第五，工具特定规则分离：需要 glob 作用域、YAML frontmatter 或特定工具功能的规则，放入该工具专属的规则目录（如 `.cursor/rules/`、`.clinerules/`、`.claude/rules/`），AGENTS.md 仅保留跨工具通用的基线指令[getunblocked.com](https://getunblocked.com/blog/claude-md-vs-agents-md-vs-cursor-rules/)。

第五条与第 2 章的判据形成呼应，也给出这套策略的内在结构：AGENTS.md 承载**跨工具通用**且**代理无法自行推断**的基线，工具专属能力（glob 作用域、frontmatter 条件激活——Cline 支持 YAML frontmatter 条件激活，其全局规则位于 `~/.agents/AGENTS.md`[cline.bot](https://docs.cline.bot/customization/cline-rules)）留在各自目录。Cursor 另有自己的优先级规则：Team Rules > Project Rules > User Rules[digitalapplied.com](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what)。这样分层之后，AGENTS.md 才能保持短、稳定、易于命中缓存——即第 4 章那条 90% 成本差的前提条件。

## 核心参考文献

[Evaluating agents. md: Are repo…](https://arxiv.org/pdf/2602.11988.pdf) · [On the Impact of AGENTS. md Fil…](https://arxiv.org/pdf/2601.20404.pdf) · [Which AI Coding Tools Read Whic…](https://www.digitalapplied.com/blog/coding-agent-instruction-files-which-tool-reads-what) · [How to Build Your AGENTS.md: Th…](https://www.augmentcode.com/guides/how-to-build-agents-md) · [CLAUDE.md vs AGENTS.md vs Curso…](https://getunblocked.com/blog/claude-md-vs-agents-md-vs-cursor-rules/) · [AGENTS.md官方标准解读 - 网硕互…](https://www.wsisp.com/helps/91061.html) · [\[实用指南与最佳实践\] 用 AGENTS.…](https://developer.volcengine.com/articles/7549123386920665130) · [Stop Burning Tokens on Redundan…](https://dev.to/aileenvl/stop-burning-tokens-on-redundant-context-why-your-agentsmd-is-failing-3cpn) · [Codex 项目说明书 AGENTS.md：把…](https://www.w3cschool.cn/aicodingguide/codex-agents-md.html) · [AGENTS.md](https://docs.devin.ai/desktop/cascade/agents-md) · [AGENTS.md](https://agents.md/) · [AGENTS.md转载 使用单一的 Markdo…](https://juejin.cn/post/7569532841870540826) · [Code Agent不听话？一个文件让它…](https://www.cnblogs.com/mliu/p/20089537) · [Codex AGENTS.md 完整配置指南：…](https://juejin.cn/post/7672244196402085951) · [别再堆 AGENTS.md 了：前端团队的…](https://juejin.cn/post/7685944661652602914) · [Rules](https://docs.cline.bot/customization/cline-rules) · [23-AGENTS.md高级用法-CSDN博客](https://blog.csdn.net/davy800405/article/details/162570879) · [OpenAI Codex CLI 的 `AGENTS.md`…](https://page.sm.cn/blm/midpage-317/index?h=iknow.v6_2.quark.cn&id=28_d818afb69400326b370ba870388e171a) · [告别配置地狱：AGENTS.md如何统一…](https://juejin.cn/post/7556911205156749322) · [Windsurf Is Now Devin Desktop:…](https://skills-hub.ai/blog/devin-desktop-acp-2026) · [Claude Code 2.1.277 开始读 AGEN…](https://blog.csdn.net/2401_88139521/article/details/166133383)
