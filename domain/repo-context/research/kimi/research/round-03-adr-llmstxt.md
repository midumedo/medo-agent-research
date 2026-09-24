# Round 03 检索笔记：ADR 决策记录 与 llms.txt

## ADR（Architecture Decision Records）
- 起源：Michael Nygard 2011 博客。动机原话："Large documents are never kept up to date... small, modular documents have at least a chance at being updated." —— 即「大文档必然过期」是 ADR 模式存在的理由。
- 核心规则：
  - 一决策一文件，3 分钟可读；Nygard 五段式（Title/Status/Context/Decision/Consequences）；MADR 扩展（YAML frontmatter、Decision Drivers、Considered Options 含"do nothing"、Confirmation 节）。
  - **Accepted 后不可变**；反转 = 写新 ADR 并标记旧的 Superseded（双向指针）；编号单调、零填充、绝不复用。
  - 生命周期：Proposed → Accepted → Deprecated/Superseded；Proposed 阶段可自由编辑。
  - 存与代码同 repo（docs/adr/），ThoughtWorks 2016 Tech Radar 即推荐：获得 Git 不可变性、grep 可发现、PR 评审流。
  - 0000 号 meta-ADR：记录「本仓库使用 ADR」这一决策本身。
  - 治理健康指标：grep -r 'docs/adr/' src/ 若为零结果，说明实践在静默失败（代码未引用 ADR）。
  - Tessl 规则：flip conditions（可观测、具体的重开条件）必填——"if requirements change" 这类不可证伪的条件是坏的；review trigger 让 ADR 可自我监控。
- 与 README 提纲的对应：这正是「文档-证据/记录分离模式」的成熟先例：ARCHITECTURE.md（现状快照） vs records/ARCHITECTURE/（每决策一文件、编号排序）≈ ADR 实践。提纲中 `0001-use-rust-core.md` 的命名猜想与社区惯例 `NNNN-kebab-title.md` 完全一致。

## llms.txt
- Jeremy Howard（Answer.AI/fast.ai）2024-09-03 提出；动机：FastHTML 晚于训练截止，编码助手无法获取其文档。
- 结构：/llms.txt = 策展索引（H1 + blockquote 摘要 + H2 分节链接列表，20-50 行为宜）；/llms-full.txt = 全文拼接；页面级 .md 后缀约定。
- 定位区分：robots.txt 管访问控制，sitemap.xml 是全量机器索引，llms.txt 是**人工策展**——"Site authors know best"。
- 采用现状（2026）：top 1000 站点仅 0.3%（Rankability）；~30 万域名研究 10.13%（SE Ranking）；无主流 AI 厂商承诺消费；Google 公开表示怀疑（类比 keywords meta）。实际主要读者是编码 agent（Claude Code 等）而非搜索爬虫。
- 对 INDEX.md 设计的启示：索引文件应「策展而非穷举」；索引价值=作者的筛选判断；索引本身会过期（stale llms.txt 被视为负债——"adds another place for inconsistency to hide"）。

## 来源登记
- S21: https://hidekazu-konishi.com/entry/architecture_decision_records_templates_and_operations.html
- S22: https://tessl.io/registry/testland/tool-selection-decision-record/1.10.14
- S23: https://hld.handbook.academy/curriculum/interview-framework/design-doc-authoring/
- S24: https://getwyrd.dev/adr/0001-record-architecture-decisions.html
- S25: https://www.reattend.com/blog/engineering-managers-guide-to-architecture-decision-records
- S26: https://llmstxt.org/ （经 PyPI llms-txt 页转述）
- S27: https://zylos.ai/research/2026-07-09-agentic-web-access-standards-llms-txt-crawler-authentication/
- S28: https://patrickstox.com/ai-search/optimization/llms-txt/
- S29: https://reputationresolutions.com/news-insights/what-is-llms-txt
- S30: https://jorijn.com/en/blog/geo-is-still-seo-ai-search-llms-txt-small-business-websites/
