# Round 02 检索笔记：CLAUDE.md 记忆体系与 context rot

## Claude Code 记忆层级（官方文档口径，v2.1.x）
- 加载顺序（拼接，非覆盖）：Managed Policy → 用户级 rules → 用户 memory → 项目 rules → 项目 CLAUDE.md → CLAUDE.local.md（最后）。
- 官方明示："All discovered files are concatenated into context rather than overriding each other"；规则冲突时模型可能任选一个——无确定性优先级。
- CLAUDE.md 以 user message 形式注入，不是 system prompt，"no guarantee of strict compliance"。
- 子目录 CLAUDE.md 按需加载（读到该目录文件时）；`.claude/rules/*.md` 支持 paths frontmatter 按 glob 作用域加载——这才是真正省上下文的机制。
- `@path` import：最多 4 跳递归；**import 不省上下文**（加载时内联展开），只是源码组织手段。
- **官方建议：每个 CLAUDE.md < 200 行**；/doctor (v2.1.206+) 可检查并提出精简建议。
- Auto memory：默认开启，agent 自动把用户纠正写入 MEMORY.md。
- 内容外迁对照表：多步流程→skill；目录/文件类型规则→.claude/rules（paths 作用域）；长参考资料→skill 的 references/；个人偏好→auto memory。

## 实证研究
- arXiv 2606.15828（AGENTS.md 坏味道/-smells 研究，14 篇文献+PR 分析）：
  - Context Bloat 是最高频坏味道（10/14 文献提及）；某 PR 把配置从 598 行砍到 149 行，理由：现代 LLM 在 ~150-200 行配置下表现更好。
  - Skill Leakage：低频/高情境指令不该放 AGENTS.md，应放 skill 文件按需加载。
- arXiv 2511.12884：对真实项目 agent context file 的实证（规模、可读性 FRE、结构层级）——首批系统性分析。
- alexdunlop.com 证据综述：
  - "IMPORTANT/YOU MUST" 强调措辞**无证据**提升遵从度；一项研究发现即使故意矛盾的指令对遵从率也无可测影响 → 强调措辞是民间传说。
  - CLAUDE.local.md 未废弃；Claude Code 运行时不读 AGENTS.md（issue anthropics/claude-code#6235）。

## Context rot（上下文衰减）
- Chroma 2025 研究：18 个前沿模型全部随输入变长而退化（lost-in-the-middle、注意力稀释、干扰项）。
- 经验法则：~50% 填充后模型偏向近期 token；~75% 后急剧下降；按填充百分比而非绝对 token 做预算（HumanLayer 目标 40-60%）。
- LongMemEval：短(~300 token) vs 长(~113k token) 提示间 30-60% 性能差。
- 对策谱系：JIT 检索（Claude Code 式 grep+按需读文件）、子 agent 隔离窗口、file-based memory 跨会话、intentional compaction、skill 按需加载。
- 关键类比：编码 agent 对代码库早已用「迭代式程序化多跳检索」而非全量塞入——文档治理应遵循同一逻辑（小常驻索引 + 按需展开）。

## 来源登记
- S11: https://github.com/luongnv89/claude-howto/blob/main/02-memory/README.md （Claude Code memory 官方文档梳理）
- S12: https://arxiv.org/pdf/2606.15828 （AGENTS.md smells）
- S13: https://arxiv.org/pdf/2511.12884 （agent context files 实证）
- S14: https://www.alexdunlop.com/writing/claude-md-best-practices
- S15: https://claudecertificationguide.com/learn/3-claude-code-config/3-1-claude-md-hierarchy
- S16: https://www.fundesk.io/context-engineering-techniques-ai-coding-agents-2026
- S17: https://www.mindstudio.ai/blog/context-rot-ai-coding-agents-explained
- S18: https://vibecoding.app/blog/context-engineering-for-coding-agents
- S19: https://tabulareditor.com/blog/managing-context-for-ai-agents
- S20: https://milvus.io/ko/blog/keeping-ai-agents-grounded-context-engineering-strategies-that-prevent-context-rot-using-milvus.md
