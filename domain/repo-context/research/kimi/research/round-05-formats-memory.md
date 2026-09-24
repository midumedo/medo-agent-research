# Round 05 检索笔记：格式选择（md/yaml/json/csv）与记忆文件实践

## LLM 数据格式实证（improvingagents.com，3 模型 × 1000 题）
- **Markdown token 效率最高**：比 JSON 少 34-38%，比 YAML 少约 10-12%；XML 最差（比 MD 多 80% token）。
- **YAML 准确率最高**（GPT-5 Nano 62.1%、Gemini 2.5 Flash Lite 51.9% 嵌套数据问答）；JSON 表现差；XML 最差。
- 结论：默认 YAML 或 Markdown，避免 JSON/XML 给 LLM 读；格式选择可致 54% 的准确率差。
- 腾讯工蜂 CLI 实践佐证：同信息 Markdown 比 JSON 省约 40% token 且理解准确率不降反升；YAML frontmatter 承载元数据 + Markdown 正文承载自由文本 = 贴合模型阅读惯性的标准模式（Cursor .mdc、SKILL.md、copilot instructions 都是这个模式）。
- 表格数据：CSV/Zen Grid token 最少，但 CSV 丢类型（无法区分 null/空串/布尔，不能嵌套）；Markdown 表格有对齐 padding 开销。
- TOON/MINT 等新格式：省 19-47% token，但需自定义解析器、生态不成熟——repo 文档场景不推荐。

## 对 README 提纲问题「index.md 是否选 csv」的回答素材
- 若 index 的主要操作是高频追加子项且消费方是脚本 → CSV/JSONL 合理（追加友好、token 少）。
- 若消费方是 LLM 且需要类型/嵌套 → YAML frontmatter + Markdown 表，或纯 Markdown 列表。
- agent 生态的事实标准：元数据一律 YAML frontmatter，正文一律 Markdown——「配置给工具读、叙述给模型读」的分层。

## MEMORY.md / USER.md 等个性化记忆文件
- Claude Code auto memory：用户纠正自动写入 MEMORY.md（~/.claude/projects/<project>/memory/），会话开始加载；`#` 快捷写入。
- OpenClaw 模型（taxonomy 参考）：
  - MEMORY.md = 长期记忆（架构、偏好、约束）；memory/YYYY-MM-DD.md = 每日会话日志（临时、过程性）。
  - SOUL.md=核心人格指令、IDENTITY.md=名字与呈现、USER.md=用户偏好、TOOLS.md=工具说明。
  - 实践规则：MEMORY.md < 2000 词；**每月审查**；不写机密；记录教训时带日期；只记可行动的。
- Deep Agents (LangChain)：memory 参数加载 AGENTS.md 进 system prompt + memory_guidelines 教 agent 何时自更新（用户纠正时 FIRST action 是更新记忆）。
- MEMORY.md 规模化失败（dev.to 2026-02）：本地文件注入适合简单场景，规模化后转向带 importance score/语义检索的记忆系统（MemoClaw、agentmemory 等 MCP 服务）；教训："If memory is locked behind an API you can't see, it's not your memory"（可读可迁移是底线）。
- 记忆之战（labgrimoire）：主文件 < 100 行，细节拆到 @import 目标或 rules 目录——与 Anthropic 200 行建议同向。
- Shopify CEO Tobi Lutke 公开抱怨 AGENTS.md vs CLAUDE.md 分裂 → symlink 方案流行。

## 来源登记
- S40: https://www.improvingagents.com/blog/best-nested-data-format/
- S41: https://arxiv.org/html/2604.05865v1 （Zen Grid token 效率对比）
- S42: https://www.cnblogs.com/studyzy/p/20068897 （腾讯工蜂 CLI 为 agent 设计的决策）
- S43: https://alterlab.io/blog/optimizing-ai-data-pipelines-json-vs-markdown-vs-text
- S44: https://dev.to/anajuliabit/the-memorymd-problem-why-local-files-fail-at-scale-58ae
- S45: https://learnopenclaw.org/workspace-memory.html
- S46: https://clawsindex.com/memory/memory/
- S47: https://docs.bswen.com/blog/2026-03-20-memory-agents-md/
- S48: https://labgrimoire.com/blog/ai-cli-memory-systems-compared/
- S49: https://segmentfault.com/a/1190000047546151 （中文社区 agentic memory 实践）
- S50: https://explainx.ai/blog/what-is-claude-md-persistent-memory-claude-code
