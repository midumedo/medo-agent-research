# 文档实例定义

每条记录对应 00 中一个实际文件路径，分别定义。路径列表来自台账，定义内容来自对应实例正文；没有正文证据时明确标为待核读，不从文件名推断。简称用于阅读和交叉引用，不代替完整路径。

本文件的证据主体是固定本地 checkout 的静态正文。除明确列出消费者代码的条目外，不能据此断言 Agent 自动发现、读取、注入或执行；没有针对任务的实验时，也不能声称文档改善了正确性、成本或其他行为效果。Raven 的 `CONTEXT.md` 等超长文件只做代表性章节核读，相关定义保持暂定。

## 状态口径

- **正文已核读**：可引用固定本地样本中的具体行。
- **正文待核读**：目前只有 00 的存在性记录，不足以定义职责。
- **消费者已核对/待核对**：只描述具体版本中程序是否读取、解析或投递此实例，不由正文声明替代。
- **效果未测**：没有直接任务实验时，不声称定义或文档提升了 Agent 行为。

## 定义条目

条目按仓库和路径逐个记录。相似文件也保留独立条目，并说明其具体差异；不存在的路径不创建定义。

## cline

### 云端开发环境指令（cloud-workspace-instructions） · `cline/AGENTS.md`

- **定义**：针对 Cline monorepo 云端开发环境，规定各组件构建、启动、测试及持久 VM 状态使用方式的工程说明。
- **回答**：云端 Agent 在这个仓库里怎样操作各子项目，环境前提和已知失败边界是什么？
- **成立内容**：环境条件、按组件区分的操作步骤、验证方法和已知边界须保持对应。
- **边界与演化**：不同于面向所有贡献者的贡献指南；VM、工具链或子项目命令变化时更新。正文并不单独证明运行时加载。
- **证据**：[原文 L1-L32](../../../sources/repos/cline/AGENTS.md#L1)。

### 版本变更记录（release-changelog） · `cline/CHANGELOG.md`

- **定义**：按版本记录 Cline 已发布的新功能、变更和修复，支持用户判断升级影响及维护者核对发布内容。
- **回答**：这个版本已经改变了什么？
- **成立内容**：版本与日期、变化类别及其用户可感知影响需要对应。
- **边界与演化**：不同于 README 对当前能力的说明；新版本追加记录，旧条目按历史理解。发布条目和版本策略改变时更新。
- **证据**：[原文 L1-L22](../../../sources/repos/cline/CHANGELOG.md#L1)。

### 社区行为准则（community-code-of-conduct） · `cline/CODE_OF_CONDUCT.md`

- **定义**：规定 Cline 社区参与空间中的行为边界、报告渠道及违规处理责任。
- **回答**：参与者应遵循什么行为标准，发生问题时如何报告和处理？
- **成立内容**：适用空间、行为标准、报告方式与维护者处置职责。
- **边界与演化**：不同于 CONTRIBUTING 的代码贡献步骤；社区空间、报告渠道或采用版本变化时更新。
- **证据**：[原文 L1-L10、L34-L76](../../../sources/repos/cline/CODE_OF_CONDUCT.md#L1)。

### 外部贡献指南（contributor-guide） · `cline/CONTRIBUTING.md`

- **定义**：指导外部贡献者通过 issue、开发环境、拉取请求、测试和提交要求参与 Cline 项目，并转介安全报告。
- **回答**：我如何提出、实现、验证并提交一项贡献？
- **成立内容**：贡献类型、准入/评审条件、开发步骤、验证要求和适用规范之间的衔接。
- **边界与演化**：与云端 Agent 环境指令和社区行为准则相邻但不同；工作流、命令、目标分支和政策变化时更新。
- **证据**：[原文 L1-L23、L32-L65、L126-L207](../../../sources/repos/cline/CONTRIBUTING.md#L1)。

### 产品介绍与导航（product-overview） · `cline/README.md`

- **定义**：面向用户及潜在贡献者介绍 Cline 产品、能力和安装入口，并把读者路由到子项目与其他资料。
- **回答**：Cline 是什么、如何开始使用、进一步信息在哪里？
- **成立内容**：产品和组件身份、能力概要、进入路径及资料导航。
- **边界与演化**：不是逐步安装手册或开发者规约；产品、发行渠道、安装平台和文档入口变化时更新。
- **证据**：[原文 L5-L9、L44-L132、L134-L185、L229-L235](../../../sources/repos/cline/README.md#L5)。

### 漏洞报告政策（vulnerability-disclosure-policy） · `cline/SECURITY.md`

- **定义**：声明 Cline 支持的版本、私密漏洞报告渠道、报告信息和公开披露前的保密要求。
- **回答**：如何报告 Cline 漏洞，哪些版本与披露步骤适用？
- **成立内容**：支持范围、私密入口、报告材料及协调披露要求。
- **边界与演化**：不同于产品风险/安全使用说明；支持版本或披露入口变化时更新。
- **证据**：[原文 L1-L25](../../../sources/repos/cline/SECURITY.md#L1)。

## codex

### 仓库工程指令（repository-engineering-instructions） · `codex/AGENTS.md`

- **定义**：限定 `codex-rs` Rust 子目录的工程约束与审查/测试指南，覆盖 Rust 惯例、构建、架构、API 和上下文限制。
- **回答**：在 codex-rs 子树中怎样修改、定位依赖并验证 Rust 改动？
- **成立内容**：适用子树、Rust 约定、模块/API 边界、验证方式及限制。
- **边界与演化**：不面向整个 Codex 产品仓库；不同于 README 的产品/安装介绍。Rust 子树结构和规则变化时更新。自动发现/加载未核实。
- **证据**：[原文 L1-L3、L5-L32、L33-L83、L85-L132、L260-L320](../../../sources/repos/codex/AGENTS.md#L1)。

### 未发布变更提示（unreleased-changes-pointer） · `codex/CHANGELOG.md`

- **定义**：把完整已发布版本历史委托给 GitHub Releases，并在仓库内保留当前 Unreleased 变更入口的短记录。
- **回答**：当前有哪些尚未发布的变更，正式历史在哪里？
- **成立内容**：未发布条目与正式历史入口需要区分。
- **边界与演化**：不同于包含逐版本详情的传统 changelog；发布后调整 Unreleased 内容并维持外部链接。
- **证据**：[原文 L1-L5](../../../sources/repos/codex/CHANGELOG.md#L1)。

### 产品版权与第三方归属声明（copyright-and-attribution-notice） · `codex/NOTICE`

- **定义**：声明 Codex 产品版权，并标明纳入的 Ratatui 派生代码及相应归属信息。
- **回答**：产品及特定第三方代码的权利归属是什么？
- **成立内容**：作品、权利人和被纳入第三方材料之间的归属关系。
- **边界与演化**：不能代替 LICENSE 的完整授权条款；版权或第三方代码来源变化时更新。
- **证据**：[原文 L1-L6](../../../sources/repos/codex/NOTICE#L1)。

### 产品入口与版本选择（product-overview） · `codex/README.md`

- **定义**：区分 Codex CLI、IDE、桌面端与云版，并给出安装、认证和继续阅读的入口。
- **回答**：Codex 有哪些产品形态，我应使用哪个并如何开始？
- **成立内容**：产品形态、能力边界、选择路径和安装/认证入口。
- **边界与演化**：不等同于某一发行形态的详细手册；产品形态、安装和登录渠道变化时更新。
- **证据**：[原文 L1-L8、L12-L81](../../../sources/repos/codex/README.md#L1)。

### 漏洞报告入口（vulnerability-reporting-entry） · `codex/SECURITY.md`

- **定义**：提供 Codex 漏洞报告渠道，并把产品安全控制说明委托给另一安全资料。
- **回答**：如何私下报告漏洞，产品安全边界说明在哪里？
- **成立内容**：报告入口与被引用的安全控制资料之间的路由关系。
- **边界与演化**：此实例本身主要是披露入口，不等于完整产品威胁模型；接收渠道或链接变化时更新。
- **证据**：[原文 L1-L17](../../../sources/repos/codex/SECURITY.md#L1)；外部漏洞接收流程未独立核验。

## deepseek-harness

### 仓库 Agent 工作指南（repository-agent-guide） · `deepseek-harness/AGENTS.md`

- **定义**：说明 Agent 在 DeepSeek Harness 仓库的稳定工作规则、首要阅读路由及验证要求。
- **回答**：开始修改前应先取得哪些架构/子树说明，并怎样完成受约束的变更？
- **成立内容**：适用规则、到更细说明的路由、执行约束和检查要求之间的关系。
- **边界与演化**：与本实例的 CLAUDE 正文相同，但仍是独立路径实例；子树规则、命令和架构入口变化时更新。
- **证据**：[原文 L1-L12、L112-L119、L164-L178](../../../sources/repos/deepseek-harness/AGENTS.md#L1)。正文不证明哪个运行时读取它。

### Claude 命名的规则副本（claude-named-rule-copy） · `deepseek-harness/CLAUDE.md`

- **定义**：以 Claude 命名入口形式保存与同仓 AGENTS 相同工程规则的完整正文副本。
- **回答**：从 Claude 命名的路径取得时，本仓规则文本是什么？
- **成立内容**：当前快照中它与 AGENTS 正文逐字相同，但两者是两个普通文件；持续一致需要维护者同步。
- **边界与演化**：不是一行指针，也不是文件系统 symlink；本地文件属性无 LinkType/Target。改动规则时应核对副本关系，实际 Claude loader 是否读取未核。
- **证据**：[原文 L1-L12](../../../sources/repos/deepseek-harness/CLAUDE.md#L1)；本地文件为 17,805 字节并与 AGENTS 比较一致，`Get-Item` 显示普通文件。

### 基准任务运行入口（benchmark-run-pointer） · `deepseek-harness/BENCHMARK.md`

- **定义**：提供按指定 Python SDK 指南运行一个 jsonrpc-agent 最小变体的入口，并要求隔离 workspace/session。
- **回答**：如何运行这一个基准任务并避免会话/工作区互相污染？
- **成立内容**：任务标识、SDK 操作入口和隔离条件。
- **边界与演化**：不构成完整基准协议；本文件没有定义数据集、指标和评分。SDK 命令或隔离条件变化时更新。
- **证据**：[原文 L1-L3](../../../sources/repos/deepseek-harness/BENCHMARK.md#L1)。

### 品牌与商标使用政策（brand-use-policy） · `deepseek-harness/BRAND_GUIDELINES.md`

- **定义**：规定生态插件和衍生项目如何描述与 DeepSeek Harness 的关系、使用名称及展示品牌素材。
- **回答**：第三方如何宣传或命名与项目相关的产品而不误示官方关系？
- **成立内容**：允许的描述、误导性暗示的限制和相关处理方式。
- **边界与演化**：不等同 README 的项目介绍或 LICENSE 的版权授权；商标/品牌政策变化时更新。
- **证据**：[原文 L1-L12](../../../sources/repos/deepseek-harness/BRAND_GUIDELINES.md#L1)。

### 中文品牌与商标使用政策（brand-use-policy-zh） · `deepseek-harness/BRAND_GUIDELINES.zh.md`

- **定义**：以中文说明第三方对 DeepSeek Harness 品牌、名称和关联关系的使用边界。
- **回答**：中文生态参与者如何准确描述与项目的关系并使用品牌材料？
- **成立内容**：中文语境下的允许描述、限制和适用对象。
- **边界与演化**：作为独立中文实例定义，不预设其与英文版语义完全等价；政策或中文表述变化时核对更新。
- **证据**：[原文 L1-L12](../../../sources/repos/deepseek-harness/BRAND_GUIDELINES.zh.md#L1)。

### 品牌指南双语配对记录（brand-translation-pairing） · `deepseek-harness/BRAND_GUIDELINES.i18n.yaml`

- **定义**：登记品牌指南英文/中文章节的配对键与摘要值，供文档同步校验流程定位变化。
- **回答**：两种语言哪些章节应配对，编辑后需要重录哪些配对摘要？
- **成立内容**：章节标识与每种语言对应值的关联。
- **边界与演化**：不是品牌规则或翻译正文；章节结构、正文或校验算法变化时重建。摘要匹配不证明翻译质量。
- **证据**：[原文 L1-L7](../../../sources/repos/deepseek-harness/BRAND_GUIDELINES.i18n.yaml#L1)。

### 外部参与和贡献政策（community-contribution-policy） · `deepseek-harness/CONTRIBUTING.md`

- **定义**：说明社区参与形式、当前外部 PR 接收状态及替代参与渠道。
- **回答**：外部参与者现在可以通过什么方式参与，哪些提交路径暂不开放？
- **成立内容**：接收状态、可参与途径及项目对社区衍生工作的定位。
- **边界与演化**：此实例明确暂不接受外部 PR；不等于代码仓内部实施流程。社区渠道和接收政策变化时更新。
- **证据**：[原文 L1-L21](../../../sources/repos/deepseek-harness/CONTRIBUTING.md#L1)。

### 中文外部参与政策（community-contribution-policy-zh） · `deepseek-harness/CONTRIBUTING.zh.md`

- **定义**：以中文说明社区可参与的事项、外部 PR 接收状态和替代参与方式。
- **回答**：中文读者当前能怎样参与 DeepSeek Harness 社区？
- **成立内容**：接收政策与可行参与渠道之间的对应。
- **边界与演化**：此实例正文同样声明暂不接收外部 PR；独立于英文实例，不以英文文本替代中文核读。政策/渠道变化时更新。
- **证据**：[原文 L1-L21](../../../sources/repos/deepseek-harness/CONTRIBUTING.zh.md#L1)。

### 贡献政策双语配对记录（contribution-translation-pairing） · `deepseek-harness/CONTRIBUTING.i18n.yaml`

- **定义**：记录英文与中文贡献政策各章节的配对摘要，供仓库的翻译配对校验流程使用。
- **回答**：维护贡献政策双语版本时，章节对应关系和摘要如何登记？
- **成立内容**：章节键与 en/zh 摘要关联。
- **边界与演化**：不是贡献政策内容，也不判断政策在两种语言中的语义等价；章节或校验算法变化时重建。
- **证据**：[原文 L1-L7](../../../sources/repos/deepseek-harness/CONTRIBUTING.i18n.yaml#L1)。脚本有消费者，但本条记录当前有效性未独立执行验证。

### 项目介绍与运行入口（project-overview-and-entry） · `deepseek-harness/README.md`

- **定义**：英文用户入口，说明 DeepSeek Harness 的身份、预览/安全状态、安装运行路径及支持、开发、许可资料的去向。
- **回答**：这个项目是什么，如何运行，重要风险与后续资料在哪里？
- **成立内容**：项目身份、运行入口、风险提示和分层导航共同构成用户进入路径。
- **边界与演化**：详细规则归 AGENTS，风险边界由 SAFETY 展开；项目状态、安装、能力和外链变化时更新。
- **证据**：[原文 L1-L15、L17-L59、L61-L77](../../../sources/repos/deepseek-harness/README.md#L1)。

### 中文项目入口（project-overview-and-entry-zh） · `deepseek-harness/README.zh.md`

- **定义**：面向中文读者介绍项目并给出运行、支持和开发资料入口。
- **回答**：中文用户如何认识、开始使用并继续查找本项目资料？
- **成立内容**：中文身份说明、运行入口与本地化支持路径。
- **边界与演化**：正文的社群渠道与英文版不同，不应只按翻译副本维护；项目事实或中文渠道变化时单独核对。
- **证据**：[原文 L1-L15、L19-L50、L70-L98](../../../sources/repos/deepseek-harness/README.zh.md#L1)。

### 项目介绍双语配对记录（readme-translation-pairing） · `deepseek-harness/README.i18n.yaml`

- **定义**：登记 README 英文与中文章节的配对键和摘要，供配对检查识别需同步的内容段。
- **回答**：README 哪些英中章节对应，修改后需更新哪些配对记录？
- **成立内容**：章节路径及其语言侧摘要，并连接到文档 gate 的验证流程。
- **边界与演化**：不是用户介绍内容或翻译质量证明；正文结构、语言片段或验证算法变化时重建。
- **证据**：[原文 L1-L23](../../../sources/repos/deepseek-harness/README.i18n.yaml#L1)；`verify-translation-pairing` 有仓内消费者。

### 英文产品安全告知（product-safety-notice） · `deepseek-harness/SAFETY.md`

- **定义**：告知运行者软件的实验状态、Agent/插件/网络风险、沙箱局限、最低风险控制及担保边界。
- **回答**：运行此产品前，应怎样理解风险、采取哪些措施，哪些控制不能保证安全？
- **成立内容**：风险来源、控制局限、使用建议和责任声明。
- **边界与演化**：不同于漏洞私密报告流程；能力、权限、隔离边界或责任声明变化时更新。
- **证据**：[原文 L1-L27](../../../sources/repos/deepseek-harness/SAFETY.md#L1)。

### 中文产品安全告知（product-safety-notice-zh） · `deepseek-harness/SAFETY.zh.md`

- **定义**：面向中文运行者说明产品实验状态、能力风险、沙箱局限及使用预防建议。
- **回答**：中文使用者应如何降低本地运行风险，哪些风险无法由沙箱消除？
- **成立内容**：风险源、控制限制和行动建议之间的关系。
- **边界与演化**：独立于英文实例，不能假定“dedicated environment”等限定完整等价；能力或责任边界变化时核对更新。
- **证据**：[原文 L1-L27](../../../sources/repos/deepseek-harness/SAFETY.zh.md#L1)。

### 安全告知双语配对记录（safety-translation-pairing） · `deepseek-harness/SAFETY.i18n.yaml`

- **定义**：登记 Safety 英文/中文章节的对应关系与摘要，供文档 gate 检查双语配对状态。
- **回答**：安全告知哪些英中章节对应，正文变化后应更新哪些状态记录？
- **成立内容**：章节键、两种语言对应值及校验工具使用关系。
- **边界与演化**：不承载风险政策本身，也不证明两种语言的安全建议完整等义；章节或检查算法变化时更新。
- **证据**：[原文 L1-L19](../../../sources/repos/deepseek-harness/SAFETY.i18n.yaml#L1)；仓内验证脚本读取 sidecar。

## Tianshu-harness

### 项目级操作约定（project-agent-operating-instructions） · `Tianshu-harness/.rivet.md`

- **定义**：面向项目编码工作的操作上下文，组合命令、审批档位、测试要求、代码约定、复杂规格核验和语义消歧。
- **回答**：在 Tianshu 项目中怎样启动、验证、处理复杂任务并澄清关键词义？
- **成立内容**：命令、规则、验证策略与判断分支需相互对应。
- **边界与演化**：与 AGENTS 架构地图、CLAUDE 构建/架构提示相邻且有混合；随命令、策略和约定变化更新。README 自称其自动注入，但加载实现未核实。
- **证据**：[原文 L1-L70](../../../sources/repos/Tianshu-harness/.rivet.md#L1)；自动注入是 README 自述。

### 仓库架构与能力地图（repository-architecture-map） · `Tianshu-harness/AGENTS.md`

- **定义**：为开发者/Agent 提供 Tianshu 组件、运行数据位置、能力边界和排查入口的仓库地图，并混合部分执行约束。
- **回答**：系统由哪些部分组成，数据在哪，遇到特定问题从何处定位？
- **成立内容**：能力与路径、状态位置和排查步骤之间需可对应。
- **边界与演化**：正文自称 Architecture Map；与 CLAUDE 的工程提示和 `.rivet.md` 操作约定不同但可组合。目录、数据位置或规则变化时更新。
- **证据**：[原文 L1-L14、L16-L39、L91-L186](../../../sources/repos/Tianshu-harness/AGENTS.md#L1)。不据此断言运行时读取。

### 日期化产品变更记录（dated-product-change-log） · `Tianshu-harness/CHANGELOG.md`

- **定义**：按日期记录 Tianshu 已发生的产品变化、修复、症状及实施处置。
- **回答**：某次变化是什么、解决什么现象、影响哪项行为？
- **成立内容**：日期、事件、受影响行为和处置之间的联系。
- **边界与演化**：不同于 CONTRIBUTOR 署名/PR 台账和未来计划；新变更追加，旧条目保留历史。
- **证据**：[原文 L1-L56](../../../sources/repos/Tianshu-harness/CHANGELOG.md#L1)。静态条目未经版本历史交叉核验。

### 社区参与行为准则（community-code-of-conduct） · `Tianshu-harness/CODE_OF_CONDUCT.md`

- **定义**：规定 Tianshu 社区可接受的参与行为、报告路径及维护者处置方式。
- **回答**：社区成员应如何参与、违规时通过什么渠道处理？
- **成立内容**：行为标准、适用空间和报告/执行渠道。
- **边界与演化**：不同于 SECURITY 的产品安全/漏洞流程和 CONTRIBUTING 的代码协作步骤；采用版本或渠道改变时更新。
- **证据**：[原文 L1-L22](../../../sources/repos/Tianshu-harness/CODE_OF_CONDUCT.md#L1)。

### 贡献者与维护者操作手册（contribution-and-maintainer-guide） · `Tianshu-harness/CONTRIBUTING.md`

- **定义**：规定 Tianshu 中代码/文档贡献的可改范围、权限审查、PR 验证、双仓收编及署名流程。
- **回答**：哪些内容可由谁修改，如何提交/审查，外部 PR 如何进入主仓？
- **成立内容**：贡献区域与审查权限、步骤、验证和署名规则的连接。
- **边界与演化**：同时面向贡献者和维护者；外部 PR 专页展开双仓流程，CoC 处理社区行为。边界、同步或记账规则变化时更新。
- **证据**：[原文 L1-L29、L56-L134](../../../sources/repos/Tianshu-harness/CONTRIBUTING.md#L1)。

### 贡献者经历与 PR 摘要（contributor-history） · `Tianshu-harness/CONTRIBUTORS.md`

- **定义**：按人员汇总 Tianshu 贡献者的可读贡献摘要并链接关联 PR，同时说明对账/生成约定。
- **回答**：哪些人贡献过什么，相关 PR 在哪里？
- **成立内容**：人员、贡献摘要和 PR 证据之间的关系。
- **边界与演化**：不同于逐笔面板记账的 CREDITS；新贡献或摘要校正时更新，并遵循文中只增不删的人工说明约定。
- **证据**：[原文 L1-L35](../../../sources/repos/Tianshu-harness/CONTRIBUTORS.md#L1)。

### 外部 PR 署名账目（pull-request-credit-ledger） · `Tianshu-harness/CREDITS.md`

- **定义**：按已移植外部 PR 追加作者登录名、邮箱和条目，使 GitHub Contributors 面板能按作者身份计入。
- **回答**：某个已移植 PR 的作者是否完成面板记账？
- **成立内容**：作者身份、PR 状态和贡献计数所需邮箱之间的对应。
- **边界与演化**：不同于 CONTRIBUTORS 的人级贡献叙述及 EXTERNAL-PRS 的操作流程；每笔 PR 记账时按文中规则追加。
- **证据**：[原文 L1-L35](../../../sources/repos/Tianshu-harness/CREDITS.md#L1)。

### 双仓外部 PR 收编流程（external-pr-intake-and-sync） · `Tianshu-harness/EXTERNAL-PRS.md`

- **定义**：规定公开仓是 dev 主仓投影时，外部 PR 如何移植、适配、验证、同步、关闭并保留署名。
- **回答**：外部 PR 关闭是否代表拒绝，贡献如何进入公开仓并保留作者归属？
- **成立内容**：双仓关系、流转步骤、关闭标签含义和署名账目需要连成一条路径。
- **边界与演化**：是 CONTRIBUTING 中双仓场景的专项流程；不等于一般贡献指南或最终署名名单。同步拓扑/credit 规则变化时更新。
- **证据**：[原文 L1-L48](../../../sources/repos/Tianshu-harness/EXTERNAL-PRS.md#L1)。

### 中文产品介绍与论证入口（product-overview-zh） · `Tianshu-harness/README.md`

- **定义**：中文用户产品入口，说明交付问题、产品定位/能力主张，并连接安装、权限、模型和深入材料。
- **回答**：Tianshu 是什么、为什么采用这种产品方向、如何开始？
- **成立内容**：问题定位、能力/价值解释与可操作入口相连；指标应有独立证据。
- **边界与演化**：与其他语种 README 是独立实例；产品能力、兼容、安装和指标变化时更新。
- **证据**：[原文 L38-L55、L79-L149、L213-L267](../../../sources/repos/Tianshu-harness/README.md#L38)。

### 英文产品比较与上手入口（product-overview-en） · `Tianshu-harness/README.en.md`

- **定义**：英文读者的产品解释和上手入口，包含产品功能、市场比较、工程指标和 Quick Start。
- **回答**：英文读者怎样理解 Tianshu、它与比较对象的差异以及如何试用？
- **成立内容**：能力说明、比较基准和运行入口相互对应。
- **边界与演化**：独立于中文实例；比较事实、指标、安装和英文链接变化时核验更新，不能假设语义完全对齐。
- **证据**：[原文 L34-L54、L68-L151](../../../sources/repos/Tianshu-harness/README.en.md#L34)。

### 日文产品与公开资料入口（product-overview-ja） · `Tianshu-harness/README.ja.md`

- **定义**：日文用户的产品说明和上手入口，包含能力、理由、指标、Quick Start 及独有的公开声明/A-B 报告链接。
- **回答**：日文读者怎样了解产品并进入安装/证据资料？
- **成立内容**：日文定位、功能和独有外链须维持准确关联。
- **边界与演化**：不是英文或中文文件的自动等价翻译；外链、指标、本地化描述或命令变化时独立更新。
- **证据**：[原文 L12-L25、L38-L46、L71-L164](../../../sources/repos/Tianshu-harness/README.ja.md#L12)。

### 韩文产品与公开资料入口（product-overview-ko） · `Tianshu-harness/README.ko.md`

- **定义**：韩文用户的产品说明和上手入口，解释内核、能力、工程指标和快速开始，并链接公开声明/实验报告。
- **回答**：韩文读者怎样理解并开始使用产品？
- **成立内容**：本地化能力说明、实证/宣传材料链接和运行路径相连接。
- **边界与演化**：与日文/中文 README 是独立实例；本地化文字、安装入口和指标变化时单独更新。
- **证据**：[原文 L12-L25、L38-L46、L71-L164](../../../sources/repos/Tianshu-harness/README.ko.md#L12)。

### 产品安全与漏洞响应说明（product-security-and-disclosure） · `Tianshu-harness/SECURITY.md`

- **定义**：结合漏洞报告流程、受支持版本、运行时防线和仓库数据/指令信任边界的安全说明。
- **回答**：漏洞如何报告、哪些版本受支持，产品如何处理不可信输入和运行风险？
- **成立内容**：披露渠道/版本范围与安全控制、信任边界声明之间的对应。
- **边界与演化**：兼有漏洞政策和产品安全承诺，不等同 CODE_OF_CONDUCT 或仓内 AGENTS 规则；实现和版本变化时复核自述。
- **证据**：[原文 L1-L35](../../../sources/repos/Tianshu-harness/SECURITY.md#L1)。正文只能证明承诺，不证明实现效果。

### 项目理念与设计公理（project-thesis-ja） · `Tianshu-harness/star.md`

- **定义**：以星域叙事组织 Tianshu 的共同公理、伙伴身份、角色和协作关系。
- **回答**：项目为何采用这些协作价值，角色和伙伴关系如何被理解？
- **成立内容**：共享公理与逐个角色/职责之间的联系。
- **边界与演化**：不是可执行命令、架构事实或运行时配置；与 README 的产品主张及 AGENTS/CLAUDE 的工程说明相邻。理念/角色变化时更新。
- **证据**：[原文 L1-L46](../../../sources/repos/Tianshu-harness/star.md#L1)。实际运行时是否读取或执行其叙述未证实。

## EverOS

### 思想来源与依赖致谢（influences-and-acknowledgments） · `EverOS/ACKNOWLEDGMENTS.md`

- **定义**：把 EverOS 的设计影响、相关来源、技术依赖和社区贡献者联系起来的致谢材料。
- **回答**：哪些来源影响了哪些设计，项目使用了什么依赖，并感谢了谁？
- **成立内容**：来源/影响与项目设计事项之间的对应，以及依赖/人员信息。
- **边界与演化**：不同于 NOTICE 的法律归属和许可例外，也不同于纯贡献者名册；来源、依赖或贡献变化时更新。
- **证据**：[原文 L10-L42、L46-L75、L79-L130](../../../sources/repos/EverOS/ACKNOWLEDGMENTS.md#L10)。

### 版本变更记录（release-changelog） · `EverOS/CHANGELOG.md`

- **定义**：按 SemVer 版本记录 EverOS 的代码、行为、文档变动及升级影响。
- **回答**：各版本已发生哪些变化，升级者需要注意什么？
- **成立内容**：版本/日期、变化类别、用户影响与必要升级动作之间的对应。
- **边界与演化**：不同于 README 的当前能力和 release 流程；每次发布追加，维护版本与比较链接。
- **证据**：[原文 L1-L26、L32-L44、L1212-L1221](../../../sources/repos/EverOS/CHANGELOG.md#L1)。底部比较链接与最新版本存在不一致疑点，需重新核对。

### 学术与软件引用说明（citation-instructions） · `EverOS/CITATION.md`

- **定义**：为学术/出版场景提供引用 EverOS 论文或软件的格式信息。
- **回答**：发表材料中应怎样引用该项目及其版本？
- **成立内容**：区分论文与软件引用，并提供相应作者、版本、URL 和许可信息。
- **边界与演化**：不同于 ACKNOWLEDGMENTS 的思想来源致谢；论文、版本、URL 或许可信息变化时更新。
- **证据**：[原文 L5-L18、L30-L57](../../../sources/repos/EverOS/CITATION.md#L5)。论文条目仍为 coming soon。

### Claude Code 工程上下文（claude-project-context） · `EverOS/CLAUDE.md`

- **定义**：为 Claude Code/维护者提供 EverOS 架构、命令、工程约束、分层依赖、运行时专属规则和仓库同步边界。
- **回答**：在 Claude 环境中如何理解仓库、运行工程操作并找到适用规则？
- **成立内容**：项目布局/事实、操作命令和工具专属适配之间的关系。
- **边界与演化**：该实例是完整工程指南，不能按 CLAUDE 名称认作指针；规则、分支、存储或 Claude 约定变化时更新。自动加载未核。
- **证据**：[原文 L16-L46、L48-L92](../../../sources/repos/EverOS/CLAUDE.md#L16)。

### 社区行为与处分准则（community-code-of-conduct） · `EverOS/CODE_OF_CONDUCT.md`

- **定义**：规定 EverOS 社区行为规范、适用空间、报告渠道和分级处置方式。
- **回答**：社区参与者应遵守哪些行为标准，违规时怎样报告和处置？
- **成立内容**：行为标准、适用范围、报告主体及处分机制。
- **边界与演化**：不同于 CONTRIBUTING 的交付步骤和 SECURITY 的漏洞披露；社区规则、联系信息或公约版本变化时更新。
- **证据**：[原文 L9-L41、L43-L77](../../../sources/repos/EverOS/CODE_OF_CONDUCT.md#L9)。

### 外部贡献与核心维护手册（contribution-and-maintainer-guide） · `EverOS/CONTRIBUTING.md`

- **定义**：同时面向外部贡献者和核心维护者，说明准入、issue/PR、安全分流、工程分支、开发、CI、风格和测试要求。
- **回答**：外部贡献如何进入项目，维护者如何在约定分支上开发和验证？
- **成立内容**：外部贡献路径与仅核心团队适用的内部工程步骤需明确区分。
- **边界与演化**：不是单纯用户指南；分支模型、开发命令、审查和贡献政策变化时更新。
- **证据**：[原文 L6-L23、L24-L63、L73-L96、L98-L156](../../../sources/repos/EverOS/CONTRIBUTING.md#L6)。

### 项目许可与第三方例外声明（project-license-notice） · `EverOS/NOTICE`

- **定义**：说明 EverOS 项目整体版权/主许可证，并标出特定第三方资产的来源、用途和适用许可例外。
- **回答**：项目总体许可是什么，哪些特定资产不由该许可覆盖？
- **成立内容**：项目许可范围与文件/用途级第三方例外之间的对应。
- **边界与演化**：不取代 LICENSE 全文；依赖、打包资产或许可证变化时更新。
- **证据**：[原文 L1-L16、L19-L56](../../../sources/repos/EverOS/NOTICE#L1)。

### 最小 API 首次运行路径（quickstart-guide） · `EverOS/QUICKSTART.md`

- **定义**：引导新用户从 API key、安装和初始化走到真实服务请求及健康检查的最短可运行流程。
- **回答**：用最低配置怎样跑通第一次 API 操作并确认结果？
- **成立内容**：前置条件、命令/配置、请求步骤、预期结果和功能边界不可断开。
- **边界与演化**：比 README 的整体介绍聚焦；API、服务依赖、默认配置或验证方式改变时更新。
- **证据**：[原文 L3-L45、L68-L113、L145-L211](../../../sources/repos/EverOS/QUICKSTART.md#L3)。

### 英文产品入口与使用综述（product-overview-en） · `EverOS/README.md`

- **定义**：英文用户入口，组合 EverOS 定位、功能/生态、Quick Start、用例、文档、社区和许可导航。
- **回答**：EverOS 是什么、当前提供什么、如何开始并继续查找信息？
- **成立内容**：项目主张、可用路径和深入资料导航之间的关系。
- **边界与演化**：含有比纯门面更多的操作/比较内容；与 Quickstart 的单一路径区分。产品边界、安装、功能和外链变化时更新。
- **证据**：[原文 L37-L86、L90-L312、L664-L793](../../../sources/repos/EverOS/README.md#L37)。宣传性对比未独立核实。

### 中文产品入口与使用综述（product-overview-zh） · `EverOS/README.zh-CN.md`

- **定义**：中文用户的 EverOS 产品介绍和操作/资料入口，功能与用例结构对应英文入口。
- **回答**：中文读者怎样理解产品并找到适用的开始路径？
- **成立内容**：中文产品事实、术语、操作链接与英文并行资料需各自准确。
- **边界与演化**：本实例独立于英文 README；本轮核了章节结构与关键主体，不做逐句等价确认。
- **证据**：[原文 L37-L86、L90-L313、L663-L795](../../../sources/repos/EverOS/README.zh-CN.md#L37)。中段示例细节未逐行检查。

### 安全报告与本地数据风险说明（security-disclosure-and-risk） · `EverOS/SECURITY.md`

- **定义**：说明 EverOS 支持版本、私密漏洞入口/响应预期，以及 local-first API、文档信任、凭证和明文存储风险。
- **回答**：漏洞如何提交，部署中的数据和信任边界有哪些风险？
- **成立内容**：版本范围、披露流程与实际威胁边界相连接。
- **边界与演化**：混合漏洞政策与产品风险说明；支持线、披露时限/渠道或威胁模型变化时更新。
- **证据**：[原文 L3-L11、L13-L38、L40-L60](../../../sources/repos/EverOS/SECURITY.md#L3)。

## gemini-cli

### 外部贡献与工程手册（contribution-and-engineering-guide） · `gemini-cli/CONTRIBUTING.md`

- **定义**：面向 Gemini CLI 外部贡献者及工程团队，组合 CLA、issue/PR 评审、构建测试、沙箱与文档写作要求。
- **回答**：贡献如何获准、实现、审查和验证？
- **成立内容**：准入和审批、开发步骤、测试约定与文档约束之间的流程关系。
- **边界与演化**：不同于 GEMINI.md 的 Agent 开发上下文和 ROADMAP 的发展方向；工具链/审批/测试变化时更新。
- **证据**：[原文 L17-L101、L117-L169、L197-L357、L418-L569](../../../sources/repos/gemini-cli/CONTRIBUTING.md#L17)。

### Gemini Agent 仓库上下文（agent-repository-context） · `gemini-cli/GEMINI.md`

- **定义**：向 Gemini CLI 中协作的编码 Agent 提供仓库事实、开发命令、按改动选择测试和代码/文档约定。
- **回答**：Agent 在此仓库开发时应先了解什么并如何验证改动？
- **成立内容**：仓库结构/事实与命令、测试选择、文档操作要求之间的联系。
- **边界与演化**：不是终端用户产品介绍或人的贡献入门；工具、结构和测试策略变化时更新。自动读取未核。
- **证据**：[原文 L1-L29、L31-L96](../../../sources/repos/gemini-cli/GEMINI.md#L1)。

### 产品介绍与用户上手入口（product-overview） · `gemini-cli/README.md`

- **定义**：介绍 Gemini CLI 的产品形态、安装/发布渠道、认证、功能、示例和帮助资料。
- **回答**：产品提供什么、如何安装认证并执行典型任务？
- **成立内容**：产品能力、前置账户/模型条件、用户命令和后续文档导航。
- **边界与演化**：不等同于 GEMINI.md 的工程约束；模型、配额、认证、命令和链接变化时核对更新。
- **证据**：[原文 L1-L28、L30-L108、L146-L214、L214-L412](../../../sources/repos/gemini-cli/README.md#L1)。时效性产品主张需独立核实。

### 非承诺性发展路线说明（nonbinding-roadmap） · `gemini-cli/ROADMAP.md`

- **定义**：公开 Gemini CLI 当前的发展方向、原则、优先主题及社区提出建议的路径，并声明不构成交付承诺。
- **回答**：项目当前关注哪些方向，怎样影响优先级，哪些事项并非交付保证？
- **成立内容**：方向/原则与实时 issue 跟踪的关系，以及交付时间的不确定性说明。
- **边界与演化**：不同于 CHANGELOG 的已发生变化或 README 的当前能力；优先方向/治理方式变化时更新。
- **证据**：[原文 L1-L28、L30-L113](../../../sources/repos/gemini-cli/ROADMAP.md#L1)。

### Google 漏洞报告入口（security-reporting-entry） · `gemini-cli/SECURITY.md`

- **定义**：向安全研究者提供 Google Gemini CLI 的漏洞报告入口、协调渠道和预期响应时间。
- **回答**：研究者应在哪里提交漏洞，期望何种响应？
- **成立内容**：唯一/首选报告入口、协调方和响应预期。
- **边界与演化**：不是一般 issue 或贡献流程；入口域名和承诺变化时更新，实际处理流程未外部核验。
- **证据**：[原文 L1-L9](../../../sources/repos/gemini-cli/SECURITY.md#L1)。

## MemoryBear

### 中文贡献指南（contributor-guide-zh） · `MemoryBear/CONTRIBUTING.md`

- **定义**：以中文规定 MemoryBear 从 issue、feature branch、commit 到 develop PR 的简化贡献路径及格式/测试提示。
- **回答**：贡献者怎样提交改动并进行本地检查？
- **成立内容**：渠道、步骤、提交命名和本地验证要求。
- **边界与演化**：README 面向使用者；简短行为要求不构成完整 CoC。分支、命令和技术栈变化时更新。
- **证据**：[原文 L1-L20、L21-L48、L50-L74](../../../sources/repos/MemoryBear/CONTRIBUTING.md#L1)。

### 英文项目入口与部署手册（product-overview-and-deployment） · `MemoryBear/README.md`

- **定义**：英文主入口，组合 MemoryBear 产品主张、论文、能力/架构/指标、Docker 与手工部署配置及社区入口。
- **回答**：产品是什么、宣称提供什么能力，怎样部署和配置？
- **成立内容**：概念主张必须与架构/能力说明连接，部署部分需保持前置条件、变量和启动步骤完整。
- **边界与演化**：比简短项目门面更像混合介绍+安装手册；与独立中文版逐项核对。架构、配置、指标和链接变化时更新。
- **证据**：[原文 L5-L37、L39-L58、L62-L465、L485-L504](../../../sources/repos/MemoryBear/README.md#L5)。性能与“类脑”结论仅证明该文件如此声称。

### 中文项目入口与部署手册（product-overview-and-deployment-zh） · `MemoryBear/README_CN.md`

- **定义**：中文主入口，介绍 MemoryBear 的愿景、论文、能力和架构，并提供中文 Docker/手工启动配置路径。
- **回答**：中文用户如何理解并实际部署配置该系统？
- **成立内容**：中文产品术语、论文/指标声明与配置步骤需在本实例中自洽。
- **边界与演化**：独立于英文实例，不能默认内容相等；本实例含自己的图像资源 ID，部署/指标/本地化变化时单独核对。
- **证据**：[原文 L5-L35、L37-L56、L60-L468、L488-L507](../../../sources/repos/MemoryBear/README_CN.md#L5)。本轮未做逐句中英 diff。

## goose

### 仓库编码 Agent 工作规则（repository-agent-work-rules） · `goose/AGENTS.md`

- **定义**：规定 goose 编码 Agent 在 issue 准入、仓库结构、开发工具和验证方面的项目内约束。
- **回答**：开始 issue 工作前需要满足哪些条件，如何在仓库中实施和检查？
- **成立内容**：issue 状态/Ready 门槛、工作区与技术约定、适用例外和验证要求。
- **边界与演化**：与外部贡献指南重叠但更直接面向 Agent；工作流、技术栈和迁移状态变化时更新。
- **证据**：[原文 L1-L28、L39-L43、L81-L137](../../../sources/repos/goose/AGENTS.md#L1)。

### Docker 构建与运行指南（docker-build-run-guide） · `goose/BUILDING_DOCKER.md`

- **定义**：为 Docker 使用者和维护者说明 Goose CLI 容器的获取/构建、运行配置、卷和 CI 相关事项及故障处理。
- **回答**：如何构建/启动 Docker 版本并传入 provider、数据和配置？
- **成立内容**：环境前提、命令、镜像属性、挂载配置和故障路径。
- **边界与演化**：不同于原生 Linux Desktop 构建或一般用户教学；Dockerfile、运行环境和发行机制变化时更新。
- **证据**：[原文 L1-L24、L26-L64、L134-L173、L175-L257、L290-L322](../../../sources/repos/goose/BUILDING_DOCKER.md#L1)。示例版本/标签未核当前有效性。

### Linux 原生构建指南（linux-native-build-guide） · `goose/BUILDING_LINUX.md`

- **定义**：按 Linux 发行版说明从源码构建 Goose CLI/Desktop、打包及排障的技术指南。
- **回答**：在目标 Linux 发行版上需安装什么、按什么顺序构建并如何处理错误？
- **成立内容**：发行版依赖、构建顺序、产物和故障处理相互对应。
- **边界与演化**：不等同 Docker 构建指南；正文的 Termux 段实际指 CLI，含跨平台内容，不能简单视为纯 Desktop。依赖、工具链和平台支持变化时更新。
- **证据**：[原文 L1-L56、L58-L185、L211-L218](../../../sources/repos/goose/BUILDING_LINUX.md#L1)。

### Claude 规则导入指针（claude-instruction-pointer） · `goose/CLAUDE.md`

- **定义**：一行 `@AGENTS.md`，将 Claude Code 的仓库规则委托给 AGENTS 正本。
- **回答**：Claude Code 应取得哪份仓库规则？
- **成立内容**：引用目标必须存在，并由消费者按该语法解析。
- **边界与演化**：不是独立规则正文；目标路径或 Claude include 约定变化时更新。本文件存在不能单独证明加载行为。
- **证据**：[原文 L1](../../../sources/repos/goose/CLAUDE.md#L1)。

### 社区行为准则（community-code-of-conduct） · `goose/CODE_OF_CONDUCT.md`

- **定义**：规定 Goose 社区的可接受/受限行为、报告、调查和处置程序。
- **回答**：何种行为适当，发生违规时谁接收报告并如何处理？
- **成立内容**：行为边界、适用范围、报告角色、调查和修复/制裁步骤。
- **边界与演化**：与 SECURITY 中的 Agent 风险和漏洞报告不同；社区空间或处理角色变化时更新。
- **证据**：[原文 L2-L22、L25-L42、L45-L83](../../../sources/repos/goose/CODE_OF_CONDUCT.md#L2)。

### 外部贡献与 AI 协作指南（contribution-and-ai-collaboration-guide） · `goose/CONTRIBUTING.md`

- **定义**：指导 goose 社区贡献从问题登记、设计、Ready、实现 PR 到验证的流程，并说明项目特有 AI 协作要求。
- **回答**：问题如何变成可验证的贡献，Agent 和人分别承担什么责任？
- **成立内容**：issue 状态、实现准入、PR 条件、AI 使用/审阅责任和开发环境。
- **边界与演化**：外部贡献路径为主，同时混合环境手册和 AI 建议；与 AGENTS 的 Agent 操作边界、GOVERNANCE 的权责制度相邻。工作板/工具/协作政策变化时更新。
- **证据**：[原文 L1-L49、L55-L108、L121-L206、L298-L361](../../../sources/repos/goose/CONTRIBUTING.md#L1)。

### 派生发行定制指南（custom-distribution-guide） · `goose/CUSTOM_DISTROS.md`

- **定义**：指导组织或派生发行者预置模型、工具、UI、provider、recipe 和子 Agent，并处理分发约束。
- **回答**：如何针对组织需求定制并发布 goose 派生版本？
- **成立内容**：可定制面、操作方式、示例、许可/遥测和上游跟进要求。
- **边界与演化**：不是基础产品介绍或通用 recipe 教程；扩展机制和分发限制变化时更新。具体 API 示例可能随版本过期。
- **证据**：[原文 L1-L43、L56-L105、L106-L807](../../../sources/repos/goose/CUSTOM_DISTROS.md#L1)。

### 技术治理与许可政策说明（technical-governance-policy） · `goose/GOVERNANCE.md`

- **定义**：描述 goose 的治理角色、决策/争议路径、维护者产生退出方式，并包含项目许可政策说明。
- **回答**：项目如何决策和处理争议，谁承担治理职责，贡献涉及什么权利政策？
- **成立内容**：角色权责、治理流程、变更程序和适用政策条款。
- **边界与演化**：不是 MAINTAINERS 的当前名单或 CONTRIBUTING 的操作流程；正文还委托现任名单给 MAINTAINERS。治理或 LF Projects 政策变化时更新。
- **证据**：[原文 L1-L5、L14-L46、L48-L140、L142-L199](../../../sources/repos/goose/GOVERNANCE.md#L1)。

### 桌面界面国际化工程指南（desktop-i18n-engineering-guide） · `goose/I18N.md`

- **定义**：说明 Goose Desktop UI 的国际化实现、message 标记/抽取/catalog 同步、格式化、新语言和测试步骤。
- **回答**：开发者如何改动或新增 UI 语言支持并验证结果？
- **成立内容**：实现组件、消息 ID/格式、资源与生成步骤和测试之间的关系。
- **边界与演化**：不是面向翻译人员的文案风格指南；react-intl、工具链或目录结构变化时更新。
- **证据**：[原文 L1-L79、L81-L179](../../../sources/repos/goose/I18N.md#L1)。

### 当前维护者名册（current-maintainer-roster） · `goose/MAINTAINERS.md`

- **定义**：列出 goose 当前 Core Maintainers 与 Maintainers 的账号。
- **回答**：当前哪些账号被列为维护者？
- **成立内容**：人员与角色类别的当前对应。
- **边界与演化**：不定义治理权限或任命方式，那些内容在 GOVERNANCE；成员变化时更新。名单的时效性未由本文件自证。
- **证据**：[原文 L1-L18](../../../sources/repos/goose/MAINTAINERS.md#L1)。

### 特定分支合并修复记录（branch-merge-repair-log） · `goose/MERGE_FIXES.md`

- **定义**：记录 `unroll-agent-loop` 分支相对 main 的合并故障、逐项修复、验证状态和剩余工作。
- **回答**：该特定合并丢失/破坏了什么，修复到哪，尚余哪些事项？
- **成立内容**：分支基线、状态、问题证据、修复和未完工作需连在一起。
- **边界与演化**：临时工作记录，不是稳定主题手册；文件自述合并前删除。分支/测试状态改变时更新或移除。
- **证据**：[原文 L1-L35、L38-L53、L55-L196](../../../sources/repos/goose/MERGE_FIXES.md#L1)。当前分支状态未核。

### 产品定位与用户入口（product-overview） · `goose/README.md`

- **定义**：介绍 goose 产品、适用方向、下载/安装入口、帮助资料和社区位置。
- **回答**：goose 是什么、适合什么用途、如何开始和继续查找？
- **成立内容**：身份/能力、起步路径和用户导航。
- **边界与演化**：比定制指南或构建手册更偏产品入口；产品能力、发行和支持链接变化时更新。
- **证据**：[原文 L1-L18、L23-L50、L59-L63](../../../sources/repos/goose/README.md#L1)。

### 自动化版本发布流程（automated-release-procedure） · `goose/RELEASE.md`

- **定义**：规定 goose minor/patch 版本的自动发布触发条件、分支/PR、QA、修复和打标签顺序。
- **回答**：何时以及按什么步骤执行一次自动化版本发布？
- **成立内容**：自动化触发与 PR、release 分支、QA 和 tag 之间的依赖。
- **边界与演化**：不同于单个 release candidate 的人工检查清单；workflow 或 QA 流程变化时更新。文中星期频率需与 workflow 实际核验。
- **证据**：[原文 L1-L27、L29-L50](../../../sources/repos/goose/RELEASE.md#L1)。

### 发布候选风险与人工验证清单（release-candidate-test-checklist） · `goose/RELEASE_CHECKLIST.md`

- **定义**：指导针对一个 release candidate 生成风险报告、运行自测并完成按变更范围制定的人工测试。
- **回答**：发布候选上架前要产出什么风险判断并完成哪些验证？
- **成立内容**：候选 PR、自动报告、自测 recipe 和人工测试计划的执行顺序。
- **边界与演化**：不是自动发版/分支流程；release recipe 或审查要求改变时更新。
- **证据**：[原文 L1-L23](../../../sources/repos/goose/RELEASE_CHECKLIST.md#L1)。recipe 现存性未核。

### RISC-V 构建实验与限制（riscv-experimental-build-guide） · `goose/RISCV_SETUP.md`

- **定义**：记录在 RISC-V 上构建 Goose CLI 的实验性依赖适配、补丁、构建命令和已知限制。
- **回答**：如何尝试构建，哪些依赖障碍尚未解决，结果有何风险？
- **成立内容**：目标环境、上游版本、补丁、构建验证和不支持状态之间的联系。
- **边界与演化**：不是稳定支持的 Linux 通用指南；依赖或官方架构支持改变时重做/退休。
- **证据**：[原文 L1-L49、L58-L94、L96-L175、L177-L285](../../../sources/repos/goose/RISCV_SETUP.md#L1)。

### Agent 风险提示与漏洞报告入口（agent-risk-and-vulnerability-reporting） · `goose/SECURITY.md`

- **定义**：向 goose 运行者说明本地执行/不可信输入风险、可采取的缓解措施和私密漏洞报告路径。
- **回答**：Agent 使用带来什么风险，用户如何降低风险并向项目报告漏洞？
- **成立内容**：风险机制、用户控制措施与漏洞入口。
- **边界与演化**：兼有产品使用风险和漏洞披露入口，不是完整安全政策或 CODE_OF_CONDUCT；能力、prompt injection 风险或渠道变化时更新。
- **证据**：[原文 L1-L15](../../../sources/repos/goose/SECURITY.md#L1)。

## deepseek-harness（续）

### 第三方许可披露清单（third-party-license-disclosure） · `deepseek-harness/THIRD_PARTY_NOTICES.md`

- **定义**：自动生成随包第三方许可披露清单，覆盖直接依赖、可选平台载荷、bundled Python distributions 和 vendored source。
- **回答**：发行物中有哪些第三方材料及对应的来源、范围和许可声明需要向接收者披露？
- **成立内容**：依赖类别、来源/范围、声明文本和生成输入应保持可追溯。
- **边界与演化**：不同于项目自身 LICENSE；锁文件、vendor、打包载荷或许可变化后重生成。正文存在不证明清单与当前依赖仍一致。
- **证据**：[原文 L4-L30、L150-L172、L175-L289](../../../sources/repos/deepseek-harness/THIRD_PARTY_NOTICES.md#L4)。未运行生成一致性检查。

## MemOS

### 多运行时项目事实与 Agent 工程规约（multi-runtime-agent-guide） · `MemOS/AGENTS.md`

- **定义**：作为 Claude/Codex/Cursor/Copilot 多运行时共用的项目事实与工程规约，说明目录、命令、API/Provider、扩展方式、行为边界和验证要求。
- **回答**：Agent 改动某模块前应读取哪些事实/规则，并怎样验证？
- **成立内容**：单一事实源、按任务定位路径、行动限制与受影响测试之间的对应。
- **边界与演化**：CLAUDE 只承载 Claude 专属适配，README 面向产品用户；模块、依赖、API、测试或限制变化时更新。自动加载仅为文档声明。
- **证据**：[原文 L1-L16、L18-L66、L79-L114、L124-L155](../../../sources/repos/MemOS/AGENTS.md#L1)。

### Claude 子代理与知识入口适配（claude-runtime-adapter） · `MemOS/CLAUDE.md`

- **定义**：规定 Claude Code 专用子代理的只读/读写边界，并指向 API contract 知识入口。
- **回答**：Claude 环境中可使用哪些子代理，各自有什么访问边界？
- **成立内容**：代理角色/权限与需读取的 API 知识之间的映射。
- **边界与演化**：不重复 AGENTS 的跨运行时项目事实；子代理或文档入口变化时更新。
- **证据**：[原文 L1-L23](../../../sources/repos/MemOS/CLAUDE.md#L1)。

### 外部贡献与维护协作流程（contribution-workflow） · `MemOS/CONTRIBUTING.md`

- **定义**：指导 MemOS 外部贡献者与维护者处理 issue/PR、环境和后端选择、分支、测试、文档、社区及许可要求。
- **回答**：一项贡献从提出到合并应经过哪些门槛、操作和验证？
- **成立内容**：贡献类型、issue/PR 条件、技术栈环境、验证、review 和后续文档责任。
- **边界与演化**：与 AGENTS 的 Agent 行为约束和 CLAUDE 适配相邻；工作流、分支、后端、命令或联系渠道变化时更新。
- **证据**：[原文 L1-L82、L107-L213、L217-L297、L300-L450](../../../sources/repos/MemOS/CONTRIBUTING.md#L1)。

### 英文产品入口与接入教程（product-overview-and-onboarding） · `MemOS/README.md`

- **定义**：介绍 MemOS 价值/能力、集成和基准主张，并串联 Cloud/Self-host/Plugin 等接入路径、社区、引用和许可信息。
- **回答**：MemOS 提供什么，使用者应选择哪种接入方式并如何开始？
- **成立内容**：产品边界、接入方式、对应操作和选择条件。
- **边界与演化**：比 README 门面更深入，含多种接入教程；性能数字是文件自述，不是效果证据。API、安装、插件和基准声明变化时更新。
- **证据**：[原文 L41-L120、L131-L214、L305-L344](../../../sources/repos/MemOS/README.md#L41)。

### 中文产品入口与接入手册（product-overview-and-onboarding-zh） · `MemOS/README_ZH.md`

- **定义**：中文用户的产品入口与接入说明，覆盖部署路径、配置和引用。
- **回答**：中文用户如何理解并选择 MemOS 的接入方式？
- **成立内容**：本地化产品事实、术语、部署路径和配置。
- **边界与演化**：与英文 README 是独立实例，逐句等价未核；配置、功能、配额或数据变化时两侧分别核对。
- **证据**：[原文 L41-L124、L134-L219、L314-L353](../../../sources/repos/MemOS/README_ZH.md#L41)。

## memU

### MemoryService 工程约束与上下文地图（memoryservice-engineering-guide） · `memU/AGENTS.md`

- **定义**：为 AI coding agent 定义 memU 服务入口不变量、存储后端契约、scope/retrieval 配置、目录地图和测试完成条件。
- **回答**：改动服务/后端/检索逻辑时应维护哪些不变量并跑哪些验证？
- **成立内容**：任务改动、受影响层/后端和 parity 测试之间的关系。
- **边界与演化**：不同于安装 Skill 或最新开发版操作规程；架构入口、后端或约束变化时更新。自动注入未核。
- **证据**：[原文 L1-L16、L17-L47、L49-L77](../../../sources/repos/memU/AGENTS.md#L1)。

### 按版本记录的项目变更历史（release-changelog） · `memU/CHANGELOG.md`

- **定义**：按发布日期/版本记载 memU 功能、修复、文档及 breaking changes。
- **回答**：在某个版本发生了什么，哪些行为或迁移条件变化？
- **成立内容**：版本、日期、变更类别和提交/影响线索之间的对应。
- **边界与演化**：不同于 README 的现状或 ADR 的选择理由；发布时追加，保持版本和比较链接可用。
- **证据**：[原文 L1-L30、L51-L103、L103-L185、L240-L281](../../../sources/repos/memU/CHANGELOG.md#L1)。

### 贡献者开发与提交指南（contributor-development-guide） · `memU/CONTRIBUTING.md`

- **定义**：规定 memU 贡献渠道、uv 环境、代码质量/测试、issue/PR/commit/review、安全和社区要求。
- **回答**：人类贡献者怎样搭建环境、完成检查并提交可审查改动？
- **成立内容**：环境命令、代码检查、issue/PR 条件和 review 之间的衔接。
- **边界与演化**：不同于 AGENTS 的 AI Agent 工程约束和 README 的产品入口；工具、测试、分支和优先级变化时更新。
- **证据**：[原文 L1-L18、L20-L131、L157-L238](../../../sources/repos/memU/CONTRIBUTING.md#L1)。

### 安装最新版的 Agent 操作规程（latest-development-install-procedure） · `memU/INSTALL-LATEST.md`

- **定义**：给执行安装任务的 Agent 提供升级最新 `main` 开发版的路由规程，包括卸载旧包、持久安装、验证 commit、选择 host adapter 和执行后续 guide。
- **回答**：怎样确保实际运行的是最新开发版，并保留用户配置/记忆？
- **成立内容**：旧安装处理、Git 安装、持久 PATH、commit 验证和 host adapter 顺序。
- **边界与演化**：本文件名看似通用安装指南，frontmatter 与正文明确它是面向 Agent 的最新开发版任务；包名、host、验证 gate 或路径变化时更新。
- **证据**：[原文 L1-L31、L33-L60、L62-L136](../../../sources/repos/memU/INSTALL-LATEST.md#L1)。未实际执行。

### Apache 2.0 许可全文（apache-license-text） · `memU/LICENSE.txt`

- **定义**：为 memU 提供 Apache License 2.0 的授权、专利、再分发、贡献、商标、免责声明和责任限制条款，并标明版权主体。
- **回答**：使用者可以如何使用/修改/分发该作品，适用哪些权利义务？
- **成立内容**：标准许可条款与当前版权主体。
- **边界与演化**：法律授权文本，不是项目使用说明或 NOTICE；许可版本/版权信息变化时更新。
- **证据**：[原文 L1-L23、L67-L194](../../../sources/repos/memU/LICENSE.txt#L1)。

### 产品入口与集成开发说明（product-overview-and-integrations） · `memU/README.md`

- **定义**：说明 memU 作为跨 session/agent/device 共享 wiki 的项目定位，列出支持 host、技能、安装/卸载、配置、后端和集成路径。
- **回答**：产品是什么、适用于何种 host，用户/集成者如何接入？
- **成立内容**：能力与支持矩阵、安装/路由入口、配置和集成方式。
- **边界与演化**：Skill 是实际安装路由；INSTALL-LATEST 聚焦最新开发版本。支持状态明确可能变化，需按产品变动更新。
- **证据**：[原文 L23-L77、L79-L143、L145-L206](../../../sources/repos/memU/README.md#L23)。

### Agent 安装/卸载任务技能（install-uninstall-agent-skill） · `memU/SKILL.md`

- **定义**：把用户交办的安装/卸载任务路由到 host 识别、初始化、专用 guide、验证 gate 和固定完成报告的可执行协议。
- **回答**：Agent 应如何选择对应 host 流程、完成安装/卸载并确认结果？
- **成立内容**：任务触发、upgrade/host 路由、每阶段检查、后端唯一性及完成/卸载保留规则。
- **边界与演化**：不同于产品介绍和“最新版开发版”专门规程；子命令、host 列表或验证报告变化时更新。是否自动加载未核。
- **证据**：[原文 L1-L41、L43-L131、L154-L170](../../../sources/repos/memU/SKILL.md#L1)。

## OpenHands

### Agent Canvas 前端仓库开发规则（frontend-contribution-rules） · `OpenHands/AGENTS.md`

- **定义**：规定 OpenHands Agent Canvas 前端仓库的所有权边界、依赖方向、状态迁移、技能选择、测试/规格和发布约束。
- **回答**：改动应落在哪个仓库/组件，需要哪些专题规则和验证？
- **成立内容**：模块所有权、依赖/API 兼容约束、改动触发的测试与发布要求。
- **边界与演化**：比 README 更偏内部协作规则；具体专题步骤由 Skill 补充。仓库分工、依赖和发布机制变化时更新。
- **证据**：[原文 L1-L23、L25-L71](../../../sources/repos/OpenHands/AGENTS.md#L1)。运行时自动加载为文档自述。

### Agent Canvas 版本变更记录（release-changelog） · `OpenHands/CHANGELOG.md`

- **定义**：按 Keep a Changelog/SemVer 方式记录 Agent Canvas 的 Unreleased 与已发布 npm 包变化。
- **回答**：发布包增加了什么、入口和构建行为如何变化？
- **成立内容**：版本状态、变化条目、npm exports/构建和发布信息。
- **边界与演化**：不同于 README 的现状和安装入口；发布后追加，包导出或 OIDC 发布流程变化时更新。
- **证据**：[原文 L1-L29](../../../sources/repos/OpenHands/CHANGELOG.md#L1)。

### Agent Canvas 产品与自托管入口（product-overview-and-self-hosting） · `OpenHands/README.md`

- **定义**：介绍 Agent Canvas 的功能、可连接的 Agent/backend、自托管选项、架构边界及文档导航。
- **回答**：用户如何理解系统、选择部署方式并辨认与其他仓库的责任边界？
- **成立内容**：产品身份、后端能力、部署前提和跨仓架构/导航。
- **边界与演化**：Windows 页面只补平台专属启动步骤，AGENTS 规定贡献者约束；镜像、端口、后端和架构变化时更新。
- **证据**：[原文 L5-L12、L33-L48、L50-L122、L124-L158](../../../sources/repos/OpenHands/README.md#L5)。

### Windows Docker 平台启动步骤（windows-docker-start-guide） · `OpenHands/README.windows.md`

- **定义**：为 Windows PowerShell 用户补充 Agent Canvas Docker sandbox 的平台专属前置、路径挂载、端口和项目目录权限。
- **回答**：在 Windows 上怎样完成该项目的 Docker 启动路径？
- **成立内容**：Windows/PowerShell 前提、挂载语义、端口和主 README 的衔接。
- **边界与演化**：不是单纯 README 语言变体；PowerShell、Docker 镜像、路径和入口变化时更新。
- **证据**：[原文 L1-L29](../../../sources/repos/OpenHands/README.windows.md#L1)。

## ReFind

### 竞赛记忆检索系统说明与 API 契约（retrieval-system-and-api-reference） · `ReFind/README.md`

- **定义**：ReFind 唯一的产品、方法、部署和 API 说明；界定原始 chunk/session/conversation 数据关系、检索流程、配置模式、保留条件及请求/响应契约。
- **回答**：竞赛平台或开发者如何正确部署、调用并理解本系统返回的检索证据？
- **成立内容**：数据写入→索引→规划/检索→evidence-only response 的关系，以及配置对运行模式的影响。
- **边界与演化**：同页混合项目介绍、方法、部署和 API；METHOD_CARD/提交表单承载专题资料。API、配置、保留策略和竞赛规则变化时更新。排行榜/论文主张未独立验证。
- **证据**：[原文 L1-L9、L33-L57、L59-L167](../../../sources/repos/ReFind/README.md#L1)。

## mem0

### 多语言仓库工程指令副本（repository-agent-guide-copy） · `mem0/AGENTS.md`

- **定义**：为 mem0 多语言 monorepo 中的代码 Agent 提供总体约束、子包工具链/目录导航、仓库事实、贡献门槛和验证路径。
- **回答**：改动某个 package 前应读取哪些局部规则，哪些全仓或子包检查适用？
- **成立内容**：总规则、子目录责任/工具链、例外和 PR/test 要求可互相定位。
- **边界与演化**：与本仓 CLAUDE.md 正文逐行相同，是独立复制载体而非指针；根规则变化时同步副本或改变其载体关系。运行时加载/优先级未知。
- **证据**：[原文 L1-L22、L24-L55、L72-L97、L99-L175](../../../sources/repos/mem0/AGENTS.md#L1)。

### Claude 命名工程指令副本（claude-repository-agent-guide-copy） · `mem0/CLAUDE.md`

- **定义**：以 Claude 命名的独立文件保存与 AGENTS 相同的 175 行工程规则、目录地图和治理约束。
- **回答**：Claude 场景对应的仓库工程规则正文是什么？
- **成立内容**：副本内容需与 AGENTS 的规则/地图一致；若继续复制，应有同步关系。
- **边界与演化**：不是 `@AGENTS.md` 单行 include 或 symlink；规则变化需同步两份，除非改为指针。实际 host 选择/优先级未核。
- **证据**：[原文 L1-L22、L24-L55、L72-L97、L99-L175](../../../sources/repos/mem0/CLAUDE.md#L1)，并与 AGENTS 全文逐行比较确认相同。

### 社区行为与 AI 贡献诚信规则（community-and-ai-contribution-conduct） · `mem0/CODE_OF_CONDUCT.md`

- **定义**：规定社区行为，并要求披露、验证 AI 生成贡献和不伪造证据，包含 issue/PR/review 中的执行与调查程序。
- **回答**：社区参与和 AI 辅助贡献中哪些行为可接受，违规由谁处理？
- **成立内容**：通用行为标准、Contribution Conduct、适用范围、报告/调查责任与处置。
- **边界与演化**：混合一般 CoC 与项目特有 AI 贡献规则；CONTRIBUTING 提供步骤并引用/执行其中规则。社区渠道、管理者或处置级别变化时更新。
- **证据**：[原文 L1-L38、L39-L82、L84-L175](../../../sources/repos/mem0/CODE_OF_CONDUCT.md#L1)。

### 多语言贡献者与包级操作指南（contributor-and-package-guide） · `mem0/CONTRIBUTING.md`

- **定义**：指导 mem0 外部贡献者从 issue/CLA 到 Python/TypeScript 环境开发、PR、发布和 review，并按包选择命令。
- **回答**：贡献者如何在目标技术栈完成一个符合仓库门槛的交付？
- **成立内容**：行为准则约束、issue/accepted/CLA 门槛、目录/技术栈、命令、PR/release 条件和安全转介。
- **边界与演化**：与 AGENTS 的 Agent 约束和 CODE_OF_CONDUCT 的行为执行相邻；package、工作流、工具链或 release 变化时更新。
- **证据**：[原文 L1-L35、L67-L141、L143-L256](../../../sources/repos/mem0/CONTRIBUTING.md#L1)。

### Mem0 SDK 使用参考手册（sdk-and-integration-reference） · `mem0/LLM.md`

- **定义**：为模型/Agent 和集成开发者汇集 Mem0 SDK quickstart、托管/自托管 API、配置/provider、高级能力、示例、实践与排错。
- **回答**：如何选择接口并用 SDK 构建和维护记忆流程？
- **成立内容**：API、配置、适用条件、完整示例和排错路径。
- **边界与演化**：比 README 更长、更偏 SDK 查询；API/provider/默认值变化时更新。未找到仓内自动消费声明，不声称注入。
- **证据**：[原文 L1-L254、L255-L693、L695-L1323](../../../sources/repos/mem0/LLM.md#L1)。文件内性能数字与 README 存在不同口径，均仅作自述。

### Claude 插件市场注册清单（plugin-marketplace-manifest） · `mem0/marketplace.json`

- **定义**：登记 mem0 插件市场名称、展示属性、插件来源目录、安装/认证策略、类别和版本。
- **回答**：市场应展示并从哪里取得哪个插件，安装/认证时机是什么？
- **成立内容**：marketplace 与 plugin 项目、来源路径、选择/安装策略及展示字段。
- **边界与演化**：不是插件实现目录或 `.claude-plugin/plugin.json` 本体清单；插件身份、来源、策略和版本变化时同步。
- **证据**：[原文 L1-L19](../../../sources/repos/mem0/marketplace.json#L1)。JSON 内容直接可见；实际市场消费者未运行核验。

### Mem0 产品和集成入口（product-overview-and-integration-entry） · `mem0/README.md`

- **定义**：介绍 Mem0 产品/研究主张，提供托管与自托管选择、快速开始、Agent skills、社区和引用入口。
- **回答**：Mem0 提供什么，如何选接入方式，并让 coding agent 使用其能力？
- **成立内容**：定位/产品边界、必要命令/配置、限制条件、详细文档和证据出处。
- **边界与演化**：与 LLM.md 的长 SDK 参考及 CONTRIBUTING 的开发参与流程不同；安装、SDK、Skills 和证据链接变化时更新。性能声明不得外推到未涵盖范围。
- **证据**：[原文 L45-L69、L71-L120、L131-L192、L194-L269](../../../sources/repos/mem0/README.md#L45)。

### 漏洞披露与响应政策（vulnerability-disclosure-policy） · `mem0/SECURITY.md`

- **定义**：规定私密漏洞报告渠道、禁止公开披露的处理方式、所需复现信息、响应时限、协调公开与支持版本。
- **回答**：如何安全提交漏洞报告并协作完成修复披露？
- **成立内容**：私密入口、复现证据、响应/协调时限和支持版本策略。
- **边界与演化**：不同于 CODE_OF_CONDUCT 的社区行为规则；联系方式、SLA 或支持版本变化时更新。正文不证明实际响应效果。
- **证据**：[原文 L1-L19、L21-L54](../../../sources/repos/mem0/SECURITY.md#L1)。

## Tianshu-harness（续）

### Claude 工程提示与架构参考（claude-engineering-context） · `Tianshu-harness/CLAUDE.md`

- **定义**：为 Claude Code 提供 Tianshu 命令/测试入口、架构/运行时说明、代码约束和已知失败经验。
- **回答**：Claude 场景下如何验证改动并理解会影响哪些真实运行路径？
- **成立内容**：命令、架构调用链、条件装配和具体约束/失效案例互相连接。
- **边界与演化**：与 AGENTS 的地图和 `.rivet.md` 的项目操作约定有重叠；本实例包含更长的运行时架构解释。hook、依赖、命令或约束变化时更新。
- **证据**：[原文 L1-L14、L16-L49、L51-L90](../../../sources/repos/Tianshu-harness/CLAUDE.md#L1)。自动加载未核。

## ZCode

### ZCode 工程 Agent 工作约束（agent-engineering-rules） · `ZCode/AGENTS.md`

- **定义**：为 ZCode 开发 Agent 规定证据优先、spec-before-code、仓库操作、实现验证、UI/平台和远程协议约束。
- **回答**：在此仓如何先调查/设计、实施改动并按边界验证？
- **成立内容**：原则、仓库命令/包图、具体验证路径和进程/API 边界。
- **边界与演化**：与 DESIGN 的 UI 视觉规范及架构策略数据相邻但粒度不同；仓库流程、协议、身份/日志语义变化时更新。
- **证据**：[原文 L1-L36、L38-L82](../../../sources/repos/ZCode/AGENTS.md#L1)。

### 模块架构策略数据（machine-checked-architecture-policy） · `ZCode/architecture-policy.yaml`

- **定义**：以机器可解析字段声明模块根、管理状态、依赖、公共入口、层次、owner 和架构限制。
- **回答**：架构检查应对哪些模块关系和全局阈值施加约束？
- **成立内容**：模块到路径/依赖/入口/owner 的关系及全局规则、例外。
- **边界与演化**：不同于 AGENTS 的操作规程和 ARCHITECTURE 的人读解释；随模块路径、依赖、管理阶段或阈值更新。此实例有脚本直接读取/解析和执行检查的代码消费者。
- **证据**：[原文 L1-L67](../../../sources/repos/ZCode/architecture-policy.yaml#L1)；消费者见 [`policy.mjs`](../../../sources/repos/ZCode/scripts/architecture/policy.mjs#L125) 与 [`index.mjs`](../../../sources/repos/ZCode/scripts/architecture/index.mjs#L81)。

### 插件商店领域术语词典（plugin-store-domain-glossary） · `ZCode/CONTEXT.md`

- **定义**：定义 ZCode 插件商店 UI/服务共用的市场来源、页面区段、目录元数据、插件清单和生命周期状态。
- **回答**：讨论插件商店需求或实现时，这些产品对象、字段和状态分别指什么？
- **成立内容**：术语定义、避免混淆词和相邻对象边界。
- **边界与演化**：限定于 Plugin Store，不是全仓架构词典；与 AGENTS 的模块地图不同。商店信息架构、字段和生命周期变化时更新。
- **证据**：[原文 L1-L3、L7-L80](../../../sources/repos/ZCode/CONTEXT.md#L1)。

### UI 设计系统约束（ui-design-system-rules） · `ZCode/DESIGN.md`

- **定义**：为生成或修改 ZCode UI 提供可判定的视觉/交互规则，涵盖 token、字体、颜色、组件、布局、响应式、无障碍和多语言。
- **回答**：新增或修改 UI 时，哪些视觉和交互选择符合产品设计系统？
- **成立内容**：token 与角色/状态、组件关系、平台例外和明确例外条件。
- **边界与演化**：不是架构解释或组件 API 目录；可由规程引用，但规则结果与检查步骤不同。UI token、组件基线和平台行为变化时更新。AGENTS 引用它，UI 自动检查消费者未证实。
- **证据**：[原文 L1-L18、L20-L81、L165-L218](../../../sources/repos/ZCode/DESIGN.md#L1)。

### 产品运行与数据安全告知（product-data-and-runtime-notice） · `ZCode/NOTICE.md`

- **定义**：说明不同运行形态下 AI 输出/执行风险、能力数据流、接收方、持久化/日志/凭据和许可边界。
- **回答**：使用某个入口/功能时，什么可能执行、发送、保存，取消后哪些数据仍不可撤回？
- **成立内容**：触发条件、数据范围、接收端、运行形态差异和限制须一起解释。
- **边界与演化**：不是漏洞披露入口；与第三方版权清单不同。入口、联网/存储行为、权限和发行物许可变化时重核。
- **证据**：[原文 L1-L30、L32-L70](../../../sources/repos/ZCode/NOTICE.md#L1)。

### 英文开发与发行指南（developer-build-and-release-guide-en） · `ZCode/README.en.md`

- **定义**：面向英文开发者说明 ZCode 组件结构、初始化、桌面/Web/CLI 使用、配置和打包步骤。
- **回答**：英文开发者如何准备、运行、修改和构建仓库？
- **成立内容**：环境版本、命令、运行形态、配置与发行步骤相连。
- **边界与演化**：与中文版 README 为独立实例，不默认逐项等价；命令、运行方式和发行步骤变化时更新。
- **证据**：[原文 L14-L35、L44-L135](../../../sources/repos/ZCode/README.en.md#L14)。

### 中文开发与远程运行指南（developer-build-and-remote-guide-zh） · `ZCode/README.md`

- **定义**：中文开发入口，说明工具要求、初始化、桌面/Web/CLI 开发、配置和包输出，并提供远程 SSH/WSL 资源准备流程。
- **回答**：中文开发者如何准备本地或远程环境并验证多运行模式？
- **成立内容**：版本/命令、远端资源与安全默认、运行/打包路径之间的对应。
- **边界与演化**：与英文实例交叉但不是同一文本；远程资源或命令变化时独立更新。
- **证据**：[原文 L16-L44、L46-L82、L84-L223](../../../sources/repos/ZCode/README.md#L16)。

### 第三方依赖许可披露清单（generated-third-party-license-notices） · `ZCode/THIRD-PARTY-NOTICES.md`

- **定义**：脚本生成发行依赖、复制源码/素材、native/WASM 和修改包的第三方版权与许可材料集合。
- **回答**：发行物包含哪些需保留的第三方声明，其来源和范围是什么？
- **成立内容**：发行组件范围、原始声明/条款与出处之间的关系，并说明保守并集及证据缺口。
- **边界与演化**：不同于 NOTICE 的用户运行/数据告知和项目 LICENSE；依赖图或复制资产变化时重生成。
- **证据**：[原文 L1-L35、L2421-L2493](../../../sources/repos/ZCode/THIRD-PARTY-NOTICES.md#L1)。声明为生成物，本轮未重跑生成器。

## qwen-code

### Qwen Code 工程 Agent 交付规约（agent-coding-and-delivery-rules） · `qwen-code/AGENTS.md`

- **定义**：规定 Agent 在 Qwen Code 仓库的简化原则、模块/PR门槛、包级检查、编程和设计约定及交付审查。
- **回答**：Agent 应凭什么证据、按什么流程和边界改动并报告？
- **成立内容**：适用规则、架构/目录、实施、验证和交付步骤的关系。
- **边界与演化**：与 CONTRIBUTING 的人的贡献流程重叠；具体门槛需与当前仓库事实复核。命令、架构或审查规则变化时更新。
- **证据**：[原文 L3-L48、L50-L179、L207-L350](../../../sources/repos/qwen-code/AGENTS.md#L3)。

### 自动生成的稳定版发布记录（generated-stable-release-notes） · `qwen-code/CHANGELOG.md`

- **定义**：从 GitHub Releases 生成的稳定版演进记录，列版本 highlights、breaking changes、分类变更和贡献者。
- **回答**：某个 stable 版本公开发布了什么变化或破坏性变更？
- **成立内容**：稳定版本、变化分类和发行内容的对应。
- **边界与演化**：明确不收 nightly/preview，且不得手改；新 stable release 时重新生成。
- **证据**：[原文 L1-L48、L141 起](../../../sources/repos/qwen-code/CHANGELOG.md#L1)。

### Claude Code 规则来源指针（claude-coding-rules-pointer） · `qwen-code/CLAUDE.md`

- **定义**：要求 Claude Code 先取得 AGENTS.md，并声明其是编码规范、构建/测试和审查要求的唯一事实源。
- **回答**：Claude Code 应从哪里取得仓库规则？
- **成立内容**：入口指向与权威范围声明。
- **边界与演化**：自身不包含具体规则；AGENTS 路径或职责变化时更新。本文件不证明消费者按自述加载。
- **证据**：[原文 L1-L5](../../../sources/repos/qwen-code/CLAUDE.md#L1)。

### 贡献与开发操作指南（contributor-development-guide） · `qwen-code/CONTRIBUTING.md`

- **定义**：指导贡献者完成 PR 审查/Issue 关联、provider 审批、环境准备、构建测试、文档预览和发布。
- **回答**：如何准备并提交一个可审查、可验证的贡献？
- **成立内容**：准入、工作准备、验证、PR 和文档产物之间的路径。
- **边界与演化**：与 AGENTS 有流程重叠；sandbox 部分存在 TBD，不能据此认定准则完整。依赖/命令/流程变化时更新。
- **证据**：[原文 L5-L84、L85-L177、L211-L255、L318-L332](../../../sources/repos/qwen-code/CONTRIBUTING.md#L5)。

### 产品介绍与使用入口（product-overview-and-quickstart） · `qwen-code/README.md`

- **定义**：介绍 Qwen Code 能力、集成、安装和命令，并提供使用示例、配置、Agent setup、隐私与评测入口。
- **回答**：产品是什么、如何安装认证并开始使用，支持哪些接口？
- **成立内容**：产品定位、安装/命令和能力/限制导航相连。
- **边界与演化**：混合定位、操作入口和版本化评测主张；评测数字需随方法/数据一同核查。支持界面、安装和认证变化时更新。
- **证据**：[原文 L10-L82、L91-L135、L137-L214](../../../sources/repos/qwen-code/README.md#L10)。

### Aliyun 安全漏洞报告入口（security-vulnerability-report-entry） · `qwen-code/SECURITY.md`

- **定义**：引导安全漏洞通过 Aliyun 私有门户报告，并把普通 bug/非安全问题排除在该入口之外。
- **回答**：发现漏洞应去哪里报告，哪些问题适用于该渠道？
- **成立内容**：报告门户与安全/普通问题范围区分。
- **边界与演化**：几乎只承担路由，不含支持版本、响应时限或完整安全模型；门户或范围变化时更新。
- **证据**：[原文 L1-L9](../../../sources/repos/qwen-code/SECURITY.md#L1)。

## minimax-cli

### MiniMax CLI Agent 工程开发规约（cli-agent-engineering-rules） · `minimax-cli/AGENTS.md`

- **定义**：规定 CLI 代码 Agent 的 Bun/TypeScript 命令、风格、错误/配置/输出/测试/Git、blind review 和源码布局要求。
- **回答**：怎样在 CLI 中实现新命令/API 并完成相应验证？
- **成立内容**：源码注册模式、开发约定和测试路径之间的对应。
- **边界与演化**：与 ERRORS 的用户可见错误目录及 README 的命令使用说明不同；脚本、registry 或错误/API 模式变化时更新。
- **证据**：[原文 L1-L80、L89-L153、L155-L211](../../../sources/repos/minimax-cli/AGENTS.md#L1)。

### 用户可见错误目录（cli-error-message-reference） · `minimax-cli/ERRORS.md`

- **定义**：按 `mmx` 子命令映射参数、认证、网络和文件场景下 CLI 将显示的错误消息。
- **回答**：某命令在给定失败条件下会报告什么文本？
- **成立内容**：命令/前置条件→失败场景→用户可见消息。
- **边界与演化**：不是根因排障指南或 Agent 异常处理规约；错误场景/文案变化时与实现、测试同步。
- **证据**：[原文 L1-L69、L73-L206](../../../sources/repos/minimax-cli/ERRORS.md#L1)。

### 英文 CLI 产品与命令入口（cli-product-and-command-guide-en） · `minimax-cli/README.md`

- **定义**：介绍官方 MiniMax CLI、支持的能力、Skill/终端安装、Token Plan、认证、命令示例和配置。
- **回答**：使用者如何安装认证并通过 `mmx` 调用平台功能？
- **成立内容**：产品身份、地区/账户前提、安装/认证和按功能的 CLI 操作。
- **边界与演化**：是 CLI 使用说明，不是 SDK 类型参考；命令、接口、区域和认证条件变化时更新。
- **证据**：[原文 L1-L62、L64-L215](../../../sources/repos/minimax-cli/README.md#L1)。

### 中文 CLI 产品与操作指南（cli-product-and-command-guide-zh） · `minimax-cli/README_CN.md`

- **定义**：以中文介绍 MiniMax CLI 功能、区域、Skill/全局安装、认证和命令参考。
- **回答**：中文使用者如何安装并用 `mmx` 调用平台能力？
- **成立内容**：中文能力说明、地区前提、认证/操作和 update/贡献入口。
- **边界与演化**：与英文实例题材相同但独立可读，不默认完全同步；区域、模型、命令和安装变化时分别核对。
- **证据**：[原文 L1-L62、L64-L202](../../../sources/repos/minimax-cli/README_CN.md#L1)。

### TypeScript SDK 调用手册（typescript-sdk-reference） · `minimax-cli/SDK.md`

- **定义**：说明 TypeScript SDK 的初始化、认证/区域及文本、图像、视频、语音、搜索、额度和 Base URL 调用示例。
- **回答**：如何在 TypeScript 程序中调用 API 并处理同步/异步结果？
- **成立内容**：初始化参数、各模块入参/返回处理和 SSE 错误路径。
- **边界与演化**：不同于通过 `mmx` 命令操作的 README；示例本身不是当前 SDK 行为的独立验证。导出和响应语义变化时更新。
- **证据**：[原文 L1-L22、L24-L80、L100-L194](../../../sources/repos/minimax-cli/SDK.md#L1)。

## Raven

### Raven 仓库硬约束（repository-hard-constraints） · `Raven/AGENTS.md`

- **定义**：面向各种 AI 编码协助规定 Raven 源码/交付硬约束，包括语言、分支/提交/PR、依赖、测试、术语和资产限制。
- **回答**：Agent 在本仓修改和交付代码时必须满足什么？
- **成立内容**：约束、门槛、流程和例外关系。
- **边界与演化**：与外部 CONTRIBUTING 重叠但本实例自述只放硬约束；允许少量 Claude 专门步骤。CI、依赖或交付流程变化时更新。
- **证据**：[原文 L1-L17、L21-L76、L114-L146、L148-L413](../../../sources/repos/Raven/AGENTS.md#L1)。

### Raven 仓库规则正文副本（repository-rule-copy） · `Raven/CLAUDE.md`

- **定义**：在 CLAUDE.md 路径保存与 AGENTS.md 逐行相同的硬约束全文。
- **回答**：从该兼容路径读取时，Raven 仓库规则正文是什么？
- **成立内容**：当前实例是同内容普通文件副本，需与 AGENTS 维持一致。
- **边界与演化**：不是轻量指针；规则变动时核对副本同步。Claude 消费者如何读取未核。
- **证据**：[原文 L1 起](../../../sources/repos/Raven/CLAUDE.md#L1)；与 AGENTS 文本比较无差异。

### 当前与待发布变化记录（release-changelog） · `Raven/CHANGELOG.md`

- **定义**：以 Unreleased 和版本分类记录 Raven 的新增、变化、修复、移除与 breaking changes，并包含迁移提示。
- **回答**：当前待发布及各发行版改变了什么？
- **成立内容**：版本状态、事件类别、原因/影响和迁移注意相连。
- **边界与演化**：历史记录，不是当前操作规范；新变化追加并保留版本史。版本/行为演进时更新，条目主张未与 Git/release 核对。
- **证据**：[原文 L1-L15、L35-L140](../../../sources/repos/Raven/CHANGELOG.md#L1)。

### 技术社区行为规范（technical-community-conduct） · `Raven/CODE_OF_CONDUCT.md`

- **定义**：规定 Raven 技术讨论/贡献互动的行为边界、治理措施和报告渠道。
- **回答**：社区参与者应如何互动，违规时通过何渠道处理？
- **成立内容**：期望/禁止行为、适用范围、执行/报告路径。
- **边界与演化**：与漏洞报告 SECURITY 和贡献步骤 CONTRIBUTING 分流；治理权力或联系方式变化时更新。
- **证据**：[原文 L1-L20](../../../sources/repos/Raven/CODE_OF_CONDUCT.md#L1)。

### Raven 领域上下文路由图（domain-context-routing-map） · `Raven/CONTEXT-MAP.md`

- **定义**：列出 Runtime/TUI/Web/ACP 等领域上下文及通信关系，并把架构词汇路由至具体说明。
- **回答**：改动前应该读取哪个领域上下文，组件边界怎样区分？
- **成立内容**：领域/模块、通信关系与对应上下文路径。
- **边界与演化**：是路由与边界总览，不替代 CONTEXT 的详细术语定义；模块拓扑或文档路径变化时更新。
- **证据**：[原文 L1-L25](../../../sources/repos/Raven/CONTEXT-MAP.md#L1)；AGENTS 规定命名时使用它，但自动加载未证实。

### Raven Runtime 领域词汇与架构不变量（runtime-domain-glossary） · `Raven/CONTEXT.md`

- **定义**：为 Raven Runtime 及相邻子域定义术语、字段/状态关系和常见混淆词，并关联实现位置。
- **回答**：实现/设计讨论中的对象、字段、生命周期和架构关系在当前代码中是什么意思？
- **成立内容**：定义、避免混用边界、关系和实现依据。
- **边界与演化**：不是 CONTEXT-MAP 的路由；内容大量绑定代码语义，代码变化需同步。此文超过 2,500 行，本轮抽读多个区段，未逐项反查源码，定义保持暂定。
- **证据**：[原文 L1-L68、L682-L735、L934-L986、L2022-L2085、L2520-L2555](../../../sources/repos/Raven/CONTEXT.md#L1)。

### Raven 外部贡献者开发指南（contributor-development-guide） · `Raven/CONTRIBUTING.md`

- **定义**：给 Raven 贡献者提供最低开发准备、验证工具/命令、PR 质量要求和安全报告分流。
- **回答**：怎样准备环境并提交可审查、包含必要验证材料的变更？
- **成立内容**：依赖/检查命令与 PR、测试、文档和验证材料要求相连接。
- **边界与演化**：与 AGENTS 的 Agent 硬约束重叠但读者和粒度不同；CLAUDE 是兼容入口。流程、命令、Make 目标或渠道变化时更新。
- **证据**：[原文 L1-L55](../../../sources/repos/Raven/CONTRIBUTING.md#L1)。

### 上游来源、派生范围与许可路由（upstream-attribution-and-license-map） · `Raven/NOTICES.md`

- **定义**：声明 Raven 所含上游来源、版权/许可、引入和修改范围，并区分不随发行的外部工具。
- **回答**：哪些内容是派生/vendored、来源和许可在哪里，哪些只是运行外部依赖？
- **成立内容**：上游来源→引入形式/范围/改动→许可依据，并区分打包与非打包。
- **边界与演化**：不同于根 LICENSE 的项目整体许可和 CHANGELOG 的代码事件；依赖来源/版本/范围变化时更新。
- **证据**：[原文 L1-L25、L27-L85](../../../sources/repos/Raven/NOTICES.md#L1)。

### 英文产品入口与安装导航（product-overview-en） · `Raven/README.md`

- **定义**：介绍 Raven 宿主式多 Agent 协调器、内置 Agent、连接/安装/运行路径、界面和资料入口。
- **回答**：Raven 是什么、能做什么，英文读者如何安装体验？
- **成立内容**：产品身份/能力、安装入口、架构和后续文档导航。
- **边界与演化**：混合宣传性基准和产品自述，不能据其证明指标；与详细 docs-site/RELEASING 不同。版本、安装和能力变化时更新。
- **证据**：[原文 L12-L110、L208-L327](../../../sources/repos/Raven/README.md#L12)。

### 中文产品与 WebUI 安装入口（product-overview-zh） · `Raven/README.zh-CN.md`

- **定义**：面向中文读者介绍 Raven、多 Agent 角色、自演化案例、连接/安装/核心系统和 WebUI。
- **回答**：中文用户如何理解产品并完成安装/体验？
- **成立内容**：中文定位、运行路径、功能说明和本地化操作细节。
- **边界与演化**：和英文 README 是独立正文；中文安装部分有 wheel/容器等专有解释，不能作为纯副本。安装/功能/生态或指标变化时单独核对。
- **证据**：[原文 L12-L110、L207-L309](../../../sources/repos/Raven/README.zh-CN.md#L12)。

### Raven 版本切割与发布操作流程（release-procedure） · `Raven/RELEASING.md`

- **定义**：指导维护者按版本源、tag、release note、CI draft、人工发布、预发布和安装约束完成 Raven 发布。
- **回答**：怎样从合并后的代码状态得到可公开安装的 release？
- **成立内容**：版本来源→tag→CI 制品/draft→人工编辑发布→latest/installer 的顺序与约束。
- **边界与演化**：是未来可执行流程，不是 CHANGELOG 的既往事实；CI、包、安装器或版本政策变化时更新。
- **证据**：[原文 L5-L13、L21-L68、L79-L97](../../../sources/repos/Raven/RELEASING.md#L5)。

### Raven 漏洞报告与支持分支说明（vulnerability-disclosure-policy） · `Raven/SECURITY.md`

- **定义**：说明漏洞私密报告渠道、所需材料、当前支持版本/分支及响应范围。
- **回答**：漏洞去哪里报告，需要什么证据，哪些分支获得安全修复？
- **成立内容**：报告入口、材料要求和支持范围相联。
- **边界与演化**：不定义完整产品安全保证；与 CODE_OF_CONDUCT 的社区行为投诉区分。渠道或支持分支状态变化时更新。
- **证据**：[原文 L3-L25](../../../sources/repos/Raven/SECURITY.md#L3)。
