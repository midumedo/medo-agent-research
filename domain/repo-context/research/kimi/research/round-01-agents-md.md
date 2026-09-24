# Round 01 检索笔记：AGENTS.md 标准与生态

## 核心事实
- AGENTS.md：2025-08-20 公开发布，由 OpenAI Codex、Amp、Jules(Google)、Cursor、Factory 协作产生；2025-12-09 捐赠给 Linux 基金会 Agentic AI Foundation (AAIF)。
- 采用量：60,000+ 开源项目（官方口径，2026 年仍为此数）；OpenAI 主 monorepo 有 88 个嵌套 AGENTS.md。
- 特点：纯 Markdown、无 schema、无必填字段；嵌套时「最近文件优先」(closest file wins)；用户对话指令覆盖文件内容。
- 定位：「README for agents」——README 给人看（quick start、项目描述），AGENTS.md 给 agent（构建/测试命令、反直觉约定、禁忌）。
- 社区基准称：有详细 AGENTS.md 的项目 agent 生成 bug 少 35-55%（agentsindex.ai，待核）。

## 工具兼容矩阵（2026 年中口径）
| 工具 | 原生文件 | 读 AGENTS.md |
|---|---|---|
| Codex CLI | AGENTS.md | 原生；层级+override（AGENTS.override.md），32 KiB 上限 |
| Cursor | .cursor/rules/*.mdc | 原生（根+子目录自动发现） |
| GitHub Copilot | .github/copilot-instructions.md | 原生；VS Code 默认开（chat.useAgentsMdFile） |
| Claude Code | CLAUDE.md | 不读（可用 @AGENTS.md import 或 symlink 桥接） |
| Gemini CLI | GEMINI.md | 可配置 fileName |
| Aider | CONVENTIONS.md | 手动 --read / .aider.conf.yml read: |
| Devin Desktop(原Windsurf) | .devin/rules/ | 原生 |
| Zed | .rules | 优先级列表中靠后 |

## 关键研究发现
1. arXiv 论文（2604.21090）将 AGENTS.md 视为「治理制品」(governance artefact)，指出社区存在三种角色混用：
   (1) 治理正文全部内联；(2) 纯指针，重定向到 CLAUDE.md/CONTRIBUTING.md；(3) 混合。
   结论：这是「制品分类缺口」(artefact classification gap)，规范本身未收敛。引用 open issue agentsmd/agents.md#66（redirect 问题未解决）。
2. TechSpokes 规范版提出五条基于 LLM 行为观察的设计原则：
   - 部分加载常见 → 高优先级信息放前面
   - 隐式上下文失败 → 显式声明
   - 扁平结构解析更可靠 → 避免深层嵌套列表
   - 显式前置阅读清单减少错误
   - 邻近性重要 → 指令靠近工作目录
3. augmentcode：GitHub 对 2,500+ 文件分析收敛出 6 个核心段落：精确版本的技术栈、带完整 flag 的可执行命令、编码约定（反直觉的最值钱）、等。
4. ASDLC 模板含 Judgment Boundaries（NEVER/ASK/ALWAYS 三段式）与 Context Map。
5. aihero.dev：AGENTS.md 位于对话历史顶部、系统提示之下；过大的文件是维护噩梦+token 成本。

## 来源登记
- S1: https://agents.md/ （官方站）
- S2: arXiv 2604.21090 AGENTS.md as governance artefact
- S3: https://www.augmentcode.com/guides/how-to-build-agents-md
- S4: https://asdlc.io/practices/agents-md-spec/
- S5: https://www.aihero.dev/a-complete-guide-to-agents-md
- S6: https://blakecrosley.com/blog/agents-md-patterns
- S7: https://github.com/TechSpokes/agency-specifications-files-agents-md/blob/main/SPECIFICATION.md
- S8: https://tomrochette.com/agents/agents-md/
- S9: https://www.morphllm.com/agents-md-guide
- S10: https://agentsindex.ai/alternatives/openapi-specification
