# 00 台账逐条映射

本表覆盖 `00docslist/index.csv` 的 135 行：133 条 `verified` 实例和 1 条 `claude-code` 的 `absent` 占位（CSV 含表头，故数据行数为 134）。每行保留 00 的原始 `kind` 与旧 `role`，再给出本阶段的 C/T 映射。C/T 不是互斥标签；一条文件记录可以有多个映射。

证据列含义：`I`=台账已核对；`B`=正文/组织方式已在 00 明细或本地快照核读；`R?`=消费者关系待固定版本核验。`role` 为空不表示没有职责，只表示旧 `ds.md` 没有对应条目。

## 判断理由代码

| 代码 | 判断理由 |
|---|---|
| F | 项目门面/语言或平台变体，回答项目是什么及如何进入；可组合 T01。 |
| A | Agent 或协作入口，规定行动约束、辖域或入口路由；可组合 T02。 |
| P | 协作/治理规则，回答参与者如何贡献、报告或处理争议；通常 C02/T05。 |
| R | 变更、版本或发布记录；保存已发生事实，通常 C10/T06。 |
| L | 法律、来源、致谢或贡献归属；C12，生成物可加 T07。 |
| H | 主题能力、环境、接口、错误或操作参考；按正文在 C05/C06 间保留缺口。 |
| S | 系统/领域/原则解释；C03，可能同时 C09。 |
| W | 计划、临时工作状态或路线；C08，是否已成为当前事实需复核。 |
| K | 结构/安全/设计/架构策略等契约或约束；C07，可组合 T03。 |
| M | 机器发现、运行配置或派生同步元数据；在 C13/C14/C05/C07 间按字段职责映射。 |
| X | 外部 PR 或可调用工作流，把规则、步骤和结果检查组织起来；C06/T04/T05。 |
| Z | 无本地 checkout 的负向占位；不创建模型。 |

## 逐条记录

| 仓库 | 路径 | 00 kind | 旧 role | C 模型 | T 模型 | 理由 | 证据 |
|---|---|---|---|---|---|---|---|
| cline | `AGENTS.md` | agent-entry | D09 | C02 | T02 | A | I |
| cline | `CHANGELOG.md` | record | D02 | C10 | T06 | R | I |
| cline | `CODE_OF_CONDUCT.md` | collab-rule | D03 | C02 | T05 | P | I |
| cline | `CONTRIBUTING.md` | collab-rule | D03 | C02,C06 | T05 | P,X | I |
| cline | `README.md` | facade | D01 | C01 | T01 | F | I |
| cline | `SECURITY.md` | collab-rule | D04 | C02,C07 | T03,T05 | P,K | I |
| codex | `AGENTS.md` | agent-entry | D09 | C02,C03 | T02 | A；辖域正文含系统定位，不能只按名称归 C02 | B |
| codex | `CHANGELOG.md` | record | D02 | C10 | T06 | R | I |
| codex | `NOTICE` | legal | D06 | C12 | T01,T07 | L | I |
| codex | `README.md` | facade | D01 | C01 | T01 | F | I |
| codex | `SECURITY.md` | collab-rule | D04 | C02,C07 | T03,T05 | P,K | I |
| deepseek-harness | `AGENTS.md` | agent-entry | D09 | C02,C04 | T02 | A；根入口把架构/文档路由出去 | B |
| deepseek-harness | `BENCHMARK.md` | topic-manual | D36 | C06 | T03,T04 | H；正文是如何跑基准，结果另属 C10 | B |
| deepseek-harness | `BRAND_GUIDELINES.i18n.yaml` | machine | — | C14 | T07 | M；翻译同步 sidecar | B |
| deepseek-harness | `BRAND_GUIDELINES.md` | topic-manual | D36 | C07,C05 | T03,T04 | H,K；主题设计约束 | B |
| deepseek-harness | `BRAND_GUIDELINES.zh.md` | topic-manual | D36 | C07,C05 | T03,T04 | F/H；语言派生正文仍保留原职责 | B |
| deepseek-harness | `CLAUDE.md` | agent-entry | D10 | C02,C04 | T02 | A；与 AGENTS 的复制关系是 T07 线索，不是指针结论 | B |
| deepseek-harness | `CONTRIBUTING.i18n.yaml` | machine | — | C14 | T07 | M | B |
| deepseek-harness | `CONTRIBUTING.md` | collab-rule | D03 | C02,C06 | T05 | P,X | B |
| deepseek-harness | `CONTRIBUTING.zh.md` | collab-rule | D03 | C02,C06 | T05,T07 | P,X；翻译正文 | B |
| deepseek-harness | `README.i18n.yaml` | machine | — | C14 | T07 | M | B |
| deepseek-harness | `README.md` | facade | D01 | C01 | T01 | F | B |
| deepseek-harness | `README.zh.md` | facade | D01 | C01 | T01,T07 | F；语言派生 | B |
| deepseek-harness | `SAFETY.i18n.yaml` | machine | — | C14 | T07 | M | B |
| deepseek-harness | `SAFETY.md` | topic-manual | D35 | C02,C07 | T03,T02 | K；Agent 运行边界 | B |
| deepseek-harness | `SAFETY.zh.md` | topic-manual | D35 | C02,C07 | T03,T07 | K；语言派生正文 | B |
| deepseek-harness | `THIRD_PARTY_NOTICES.md` | legal | D06 | C12 | T07 | L；生成标记建立派生关系 | B |
| EverOS | `ACKNOWLEDGMENTS.md` | legal | D06 | C11,C12 | T01 | L | I |
| EverOS | `CHANGELOG.md` | record | D02 | C10 | T06 | R | I |
| EverOS | `CITATION.md` | legal | D06 | C12 | T01 | L | I |
| EverOS | `CLAUDE.md` | agent-entry | D10 | C02,C04 | T02 | A；唯一入口状态需按正文理解 | I |
| EverOS | `CODE_OF_CONDUCT.md` | collab-rule | D03 | C02 | T05 | P | I |
| EverOS | `CONTRIBUTING.md` | collab-rule | D03 | C02,C06 | T05 | P,X | I |
| EverOS | `NOTICE` | legal | D06 | C12 | T01,T07 | L | I |
| EverOS | `QUICKSTART.md` | semantic | D05 | C01,C06 | T01,T04 | F,H | I |
| EverOS | `README.md` | facade | D01 | C01 | T01 | F | I |
| EverOS | `README.zh-CN.md` | facade | D01 | C01 | T01,T07 | F；语言变体 | I |
| EverOS | `SECURITY.md` | collab-rule | D04 | C02,C07 | T03,T05 | P,K | I |
| gemini-cli | `CONTRIBUTING.md` | collab-rule | D03 | C02,C06 | T05 | P,X | I |
| gemini-cli | `GEMINI.md` | agent-entry | D10 | C02,C04 | T02 | A；入口名是 harness 接口，不是内容类型 | I |
| gemini-cli | `README.md` | facade | D01 | C01 | T01 | F | I |
| gemini-cli | `ROADMAP.md` | topic-manual | D26 | C08 | T06 | W；真实实例反驳旧零命中 | B |
| gemini-cli | `SECURITY.md` | collab-rule | D04 | C02,C07 | T03,T05 | P,K | I |
| goose | `AGENTS.md` | agent-entry | D09 | C02,C04 | T02 | A | I |
| goose | `BUILDING_DOCKER.md` | topic-manual | D36 | C06,C05 | T04 | H | I |
| goose | `BUILDING_LINUX.md` | topic-manual | D36 | C06,C05 | T04 | H | I |
| goose | `CLAUDE.md` | agent-entry | D10 | C02,C04 | T02,T07 | A；指针/适配关系需正文核验 | I |
| goose | `CODE_OF_CONDUCT.md` | collab-rule | D03 | C02 | T05 | P | I |
| goose | `CONTRIBUTING.md` | collab-rule | D03 | C02,C06 | T05 | P,X | I |
| goose | `CUSTOM_DISTROS.md` | topic-manual | D36 | C05,C06 | T01,T04 | H | I |
| goose | `GOVERNANCE.md` | collab-rule | — | C02 | T05 | P；制度与决策权限，不能并入名单 | B |
| goose | `I18N.md` | topic-manual | D36 | C05,C06 | T04 | H；需核正文是参考还是规程 | I |
| goose | `MAINTAINERS.md` | collab-rule | — | C11 | T05 | P；当前维护责任登记 | B |
| goose | `MERGE_FIXES.md` | topic-manual | D36 | C08,C06 | T06,T04 | W；文件自述临时性，不能当稳定主题手册 | B |
| goose | `README.md` | facade | D01 | C01 | T01 | F | I |
| goose | `RELEASE.md` | record | D05 | C06,C10 | T04,T06 | H,R；需按正文区分步骤和结果 | I |
| goose | `RELEASE_CHECKLIST.md` | record | D05 | C06 | T03,T04 | H；检查门槛 | I |
| goose | `RISCV_SETUP.md` | topic-manual | D36 | C05,C06 | T04 | H | I |
| goose | `SECURITY.md` | collab-rule | D04 | C02,C07 | T03,T05 | P,K；若含 Agent 权限段保留双映射 | B |
| mem0 | `AGENTS.md` | agent-entry | D09 | C02,C04 | T02 | A | I |
| mem0 | `CLAUDE.md` | agent-entry | D10 | C02,C04 | T02,T07 | A；复制副本不是天然指针 | I |
| mem0 | `CODE_OF_CONDUCT.md` | collab-rule | D03 | C02 | T05 | P | I |
| mem0 | `CONTRIBUTING.md` | collab-rule | D03 | C02,C06 | T05 | P,X | I |
| mem0 | `LLM.md` | topic-manual | D36 | C05 | T04 | H；主题参考，正文可能含步骤 | I |
| mem0 | `marketplace.json` | machine | — | C13 | T08 | M；插件发现/分发元数据 | B |
| mem0 | `README.md` | facade | D01 | C01 | T01 | F | I |
| mem0 | `SECURITY.md` | collab-rule | D04 | C02,C07 | T03,T05 | P,K | I |
| MemoryBear | `CONTRIBUTING.md` | collab-rule | D03 | C02,C06 | T05 | P,X | I |
| MemoryBear | `README.md` | facade | D01 | C01 | T01 | F | I |
| MemoryBear | `README_CN.md` | facade | D01 | C01 | T01,T07 | F；语言派生但对齐需复核 | B |
| MemOS | `AGENTS.md` | agent-entry | D09 | C02,C04 | T02 | A；正本/消费者声明是关键关系 | B |
| MemOS | `CLAUDE.md` | agent-entry | D10 | C02 | T02,T07 | A；运行时互补分工，不能套指针通则 | B |
| MemOS | `CONTRIBUTING.md` | collab-rule | D03 | C02,C06 | T05 | P,X | I |
| MemOS | `README.md` | facade | D01 | C01 | T01 | F | I |
| MemOS | `README_ZH.md` | facade | D01 | C01 | T01,T07 | F；语言派生 | I |
| memU | `AGENTS.md` | agent-entry | D09 | C02,C04 | T02 | A | I |
| memU | `CHANGELOG.md` | record | D02 | C10 | T06,T07 | R；生成/发布关系需复核 | I |
| memU | `CONTRIBUTING.md` | collab-rule | D03 | C02,C06 | T05 | P,X | I |
| memU | `INSTALL-LATEST.md` | topic-manual | D05 | C06,C05 | T01,T04 | H；frontmatter 可能使其成为 Skill 描述符，不能按名字定型 | B |
| memU | `LICENSE.txt` | legal | D06 | C12 | T01 | L | I |
| memU | `README.md` | facade | D01 | C01 | T01 | F | I |
| memU | `SKILL.md` | topic-manual | D12 | C06 | T04 | X；入口性质需结合 frontmatter/资源 | B |
| minimax-cli | `AGENTS.md` | agent-entry | D09 | C02,C04 | T02 | A | I |
| minimax-cli | `ERRORS.md` | topic-manual | D36 | C05 | T04 | H；面向用户的错误参考 | I |
| minimax-cli | `README.md` | facade | D01 | C01 | T01 | F | I |
| minimax-cli | `README_CN.md` | facade | D01 | C01 | T01,T07 | F；语言派生 | I |
| minimax-cli | `SDK.md` | topic-manual | D36 | C05 | T04 | H；接口参考 | I |
| OpenHands | `AGENTS.md` | agent-entry | D09 | C02,C03 | T02 | A；Repository Notes 含责任边界解释 | B |
| OpenHands | `CHANGELOG.md` | record | D02 | C10 | T06 | R | I |
| OpenHands | `README.md` | facade | D01 | C01 | T01 | F | I |
| OpenHands | `README.windows.md` | facade | D01 | C01,C05 | T01 | F；平台变体不等于语言变体 | I |
| qwen-code | `AGENTS.md` | agent-entry | D09 | C02,C04 | T02 | A | I |
| qwen-code | `CHANGELOG.md` | record | D02 | C10 | T06 | R；体量不改变模型 | I |
| qwen-code | `CLAUDE.md` | agent-entry | D10 | C02,C04 | T02,T07 | A；散文指针关系需保留 | B |
| qwen-code | `CONTRIBUTING.md` | collab-rule | D03 | C02,C06 | T05 | P,X | I |
| qwen-code | `README.md` | facade | D01 | C01 | T01 | F | I |
| qwen-code | `SECURITY.md` | collab-rule | D04 | C02,C07 | T03,T05 | P,K | I |
| Raven | `AGENTS.md` | agent-entry | D09 | C02 | T02 | A；硬约束重心由正文证明 | B |
| Raven | `CHANGELOG.md` | record | D02 | C10 | T06 | R | I |
| Raven | `CLAUDE.md` | agent-entry | D10 | C02 | T02,T07 | A；当前快照为副本关系，不能沿用旧字节判断 | B |
| Raven | `CODE_OF_CONDUCT.md` | collab-rule | D03 | C02 | T05 | P | I |
| Raven | `CONTEXT-MAP.md` | semantic | D16 | C03,C04 | T08 | S；同时解释边界并路由术语 | B |
| Raven | `CONTEXT.md` | semantic | D14 | C03 | T08 | S；领域词义正典 | B |
| Raven | `CONTRIBUTING.md` | collab-rule | D03 | C02,C06 | T05 | P,X | I |
| Raven | `NOTICES.md` | legal | D06 | C12 | T01,T07 | L | I |
| Raven | `README.md` | facade | D01 | C01,C04 | T01 | F；README 也承担进一步导航 | B |
| Raven | `README.zh-CN.md` | facade | D01 | C01,C04 | T01,T07 | F；语言派生 | I |
| Raven | `RELEASING.md` | record | D05 | C06 | T04 | H；发布规程，不因 kind=record 变成历史 | I |
| Raven | `SECURITY.md` | collab-rule | D04 | C02,C07 | T03,T05 | P,K | I |
| ReFind | `README.md` | facade | D01 | C01 | T01 | F | I |
| Tianshu-harness | `.rivet.md` | machine | — | C05,C07 | T03,T04 | M；项目级 harness 命令/运行约定，字段语义以正文为准 | B |
| Tianshu-harness | `AGENTS.md` | agent-entry | D09 | C02,C03,C04 | T02 | A；Architecture Map 反例，不能限定为纯硬约束 | B |
| Tianshu-harness | `CHANGELOG.md` | record | D02 | C10 | T06 | R | I |
| Tianshu-harness | `CLAUDE.md` | agent-entry | D10 | C05,C02 | T02,T07 | A；命令手册与 AGENTS 互补 | B |
| Tianshu-harness | `CODE_OF_CONDUCT.md` | collab-rule | D03 | C02 | T05 | P | I |
| Tianshu-harness | `CONTRIBUTING.md` | collab-rule | D03 | C02,C06 | T05 | P,X | I |
| Tianshu-harness | `CONTRIBUTORS.md` | legal | D06 | C11,C12 | T01 | L | I |
| Tianshu-harness | `CREDITS.md` | legal | D06 | C11,C12 | T01 | L | I |
| Tianshu-harness | `EXTERNAL-PRS.md` | collab-rule | — | C02,C06 | T05 | X；双仓投影、移植、验证、同步形成独立流转任务 | B |
| Tianshu-harness | `README.en.md` | facade | D01 | C01 | T01,T07 | F；语言变体 | I |
| Tianshu-harness | `README.ja.md` | facade | D01 | C01 | T01,T07 | F；语言变体 | I |
| Tianshu-harness | `README.ko.md` | facade | D01 | C01 | T01,T07 | F；语言变体 | I |
| Tianshu-harness | `README.md` | facade | D01 | C01,C04 | T01 | F | I |
| Tianshu-harness | `SECURITY.md` | collab-rule | D04 | C02,C07 | T03,T05 | P,K | I |
| Tianshu-harness | `star.md` | semantic | D17 | C03,C09 | T01,T06 | S；原则/立场与系统解释相连 | B |
| ZCode | `AGENTS.md` | agent-entry | D09 | C02,C04 | T02 | A | I |
| ZCode | `architecture-policy.yaml` | machine | — | C07 | T03 | M；机器可判定模块依赖/所有者/入口约束 | B |
| ZCode | `CONTEXT.md` | semantic | D14 | C03 | T08 | S；功能域术语/边界 | B |
| ZCode | `DESIGN.md` | semantic | — | C07,C05 | T03,T04 | K；面向 Agent 的 UI 设计系统约束，不等同架构或一般 STYLE | B |
| ZCode | `NOTICE.md` | legal | D06 | C12 | T01,T07 | L | I |
| ZCode | `README.en.md` | facade | D01 | C01 | T01,T07 | F；语言派生 | I |
| ZCode | `README.md` | facade | D01 | C01 | T01 | F | I |
| ZCode | `THIRD-PARTY-NOTICES.md` | legal | D06 | C12 | T01,T07 | L；生成法务清单 | I |
| claude-code | — | — | — | — | — | Z；无本地 checkout，仅记录覆盖缺口 | I |

## 映射后的暂定结论

00 的 `kind` 可以帮助快速取样，但它不能解释同一 kind 内的差异：`semantic` 同时出现领域词典、设计系统和立论；`topic-manual` 同时出现规程、能力参考、路线和临时状态；`machine` 同时出现派生 sidecar、插件分发和架构策略。模型应由任务和关系解释这些差异。

本表中的 C/T 是当前可审查的工作映射，不是对运行时消费者的断言。正文核读、加载路径、生成器和效果证据的缺口集中在 [`gaps.md`](gaps.md)。
