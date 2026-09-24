# Round 04 检索笔记：Diátaxis 分类学 与 文档漂移治理

## Diátaxis（Daniele Procida）
- 四象限 = 两轴（实践/理论 × 学习/工作）：Tutorials（学习向）、How-to（任务向）、Reference（信息向）、Explanation（理解向）。
- 铁律：一份文档只服务一个目的，混型是文档失败的主因；边界严格（Reference 不含教学叙述，Tutorial 不含参考表）。
- 采用：Cloudflare（称其 docs 改版"北极星"）、Canonical/Ubuntu 全线、Django、Python 官方文档。
- **与 AI agent 的对齐**（byteiota 2026-08）：agent 推理是意图驱动的——执行任务要 how-to，核验字段要 reference，做计划要 explanation；Diátaxis 按人类读者意图设计，恰好同构。已有 agent skill 强制四象限不混（keithpatton/diataxis-agent-skill）。
- 对 README 提纲的映射：Diátaxis 是按「内容功能」分类的正交轴，可与提纲的「时态/层级」轴组合（如 ARCHITECTURE=Explanation，AGENTS=How-to+Reference，ADR=Explanation 的时态化切片）。

## 文档漂移（documentation drift）治理
- 定义：代码变、文档不变 → 文档开始"说谎"。非代码变更（配置、workflow、模板、feature flag）也会造成漂移，path filter 会漏。
- 根因判断：**漂移本质是所有权问题+流程问题**，不是技术问题。单一专家依赖、孤儿文档是典型失败模式。
- 解法谱系：
  1. 明确 owner 矩阵（按文档类型指派 lead+reviewer，与自然专长对齐）；
  2. docs-as-code：纯文本+PR 评审+CI 测试+自动发布——"the build won't go green until we do"；
  3. CI 卡点：Vale/alex 文风 lint、死链检查、Spectral 校验 OpenAPI 与实现一致、自定义规则（引用的文件路径是否存在、文档端点 vs 代码路由 diff——"文档幽灵"与"未文档化表面"）；
  4. AI 漂移检测工作流：PR 合并后把 diff+现有文档交给 Claude Code（anthropics/claude-code-action@v1），漂移则自动开后续 PR；需 loop guard 防 bot 循环、prompt-injection 缓解；
  5. 面向用户的变更文档与代码同 PR；内部重构可不同步。
- 节奏建议：高影响文档周审、全面月审；API 文档影响外部用户需最严。
- 效果度量：onboarding 时间、支持工单量、time-to-first-integration，修复漂移后 3 个月内普遍改善 20-40%。
- 对 agent 的新意义：AI 工具把文档当 ground truth，陈旧文档的代价从"误导人"升级为"误导所有 agent 会话"。

## 来源登记
- S31: https://diataxis.fr/ （经多处转述）
- S32: https://byteiota.com/diataxis-the-documentation-framework-ai-agents-need/
- S33: https://handbook.eng.kempnerinstitute.harvard.edu/s2_swe_for_research/documentation_and_readibility.html
- S34: https://www.mintlify.com/library/documentation-linting
- S35: https://decryptd.co/the-docs-as-code-drift-problem-why-your-documentation
- S36: https://blog.vibecoder.me/documentation-rot-keeping-docs-in-sync
- S37: https://understandingdata.com/posts/doc-drift-detection-ci/
- S38: https://sourcegraph.com/blog/documentation-as-code
- S39: https://www.docsie.io/blog/glossary/documentation-drift/
