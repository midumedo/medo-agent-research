=====ITEM 0 [assistant]=====
# AGENTS.md 最佳实践：核心结论与实施指南

**核心结论**：AGENTS.md 是由 Linux 基金会下属 Agentic AI Foundation 托管的跨工具开放标准，旨在为 AI 编程代理提供统一的项目级指令@@REF_11@@。编写高质量 AGENTS.md 的关键在于遵循“地图而非手册”原则，仅包含 Agent 无法从代码中自行推断的“隐形逻辑”（如非标准构建命令、反直觉架构决策），篇幅应严格控制在 100-200 行以内。学术研究证实，人工精心编写的 AGENTS.md 可显著降低输出 Token 消耗（中位数减少 16.58%）和运行时间（中位数减少 28.64%）@@REF_7@@，但自动生成的上下文文件反而会导致任务成功率下降 0.5%-2% 并增加 20%-23% 的推理成本@@REF_4@@。在多工具环境中，应以 AGENTS.md 为唯一事实来源，并为 Claude Code 创建一行 `@AGENTS.md` 导入桥接文件以实现全生态兼容@@REF_3@@。

## 一、内容结构与常见段落

AGENTS.md 没有强制 Schema 或必填字段，采用纯 Markdown 格式，Agent 直接解析文本语义。其定位是“给 AI 看的项目操作手册”，与面向人类的 README.md 互补而非替代@@REF_11@@。

### 推荐核心段落

根据官方规范与生产实践，以下六个板块构成了高信噪比的 AGENTS.md 基础结构：

| 段落名称 | 核心内容要求 | 编写要点 |
| :--- | :--- | :--- |
| **项目概述 (Project Overview)** | 技术栈精确到版本、关键依赖、架构分层简述 | 仅写 Agent 无法从 `package.json` 或目录结构推断的信息；避免冗余描述@@REF_8@@ |
| **构建与测试命令 (Build & Test)** | 安装、构建、测试、Lint 的精确命令及完整 Flag@@REF_12@@ | 放在文件靠前位置；提供单文件级别的检查命令以替代全量构建@@REF_6@@ |
| **代码风格与约定 (Conventions)** | 命名规范、缩进、导入顺序、异常处理模式 | 使用祈使句（“必须”“禁止”）；提供好/坏代码片段对比优于文字描述 |
| **安全与权限边界 (Security)** | 允许自动执行 vs 需确认的操作清单；禁止项（硬编码密钥、跨层依赖） | 采用三级优先级体系（CRITICAL > IMPORTANT > GUIDANCE）@@REF_2@@ |
| **目录约定与禁区 (Structure)** | 关键目录职责、新代码存放位置、禁止编辑的目录 | 仅记录非标准或反直觉的目录约束；标准框架约定无需赘述@@REF_2@@ |
| **PR 与提交规范 (Git Workflows)** | 分支策略、提交信息格式、PR 检查清单@@REF_12@@ | 明确验收标准（测试通过、Lint 通过、Diff 范围）@@REF_6@@ |

### “隐形逻辑”优先原则

ETH Zurich 的研究明确指出，AGENTS.md 应仅包含“非可推断细节”（Non-Inferable Details）@@REF_2@@。以下内容**不应**出现在 AGENTS.md 中：
*   **通用的技术栈描述**：Agent 可通过读取 `package.json`、`Cargo.toml` 等文件自行发现@@REF_8@@。
*   **标准的目录结构说明**：若项目遵循框架默认约定（如 Next.js 的 `app/` 目录），无需重复描述@@REF_2@@。
*   **已有的文档内容**：与 README 或现有文档重复的内容会被视为噪声，稀释模型注意力@@REF_8@@。
*   **抽象的质量要求**：如“写好代码”“注意性能”等无法验证的描述@@REF_13@@。

相反，以下内容具有高 ROI：
*   **非标准工具选型**：如使用 Pixi 而非 pip，或使用内部自研构建工具@@REF_2@@。
*   **反直觉的架构决策**：如“API 客户端不抛异常”或“legacy 模块不可重构但 CI 依赖它”@@REF_8@@。
*   **特定的版本锁定**：防止 Agent 使用训练数据中更常见但不兼容的版本@@REF_2@@。
*   **已知的坑与避坑指南**：如废弃 API、时区处理陷阱等 Agent 反复犯错的问题。

## 二、嵌套与覆盖规则

AGENTS.md 支持多层级配置，核心机制为“就近优先”（Proximity Priority），即距离被编辑文件最近的 AGENTS.md 优先级最高。

### 层级加载与拼接策略

Agent 在处理请求时，按以下顺序构建指令链：
1.  **全局层**：`~/.codex/AGENTS.md`（或其他工具对应的全局路径），定义个人通用偏好。
2.  **项目根目录**：仓库根目录下的 `AGENTS.md`，定义项目级“宪法”。
3.  **子目录层级**：从根目录向当前工作目录逐级查找，每一级的 AGENTS.md 依次追加。
4.  **合并规则**：非冲突配置自动合并（如列表类配置追加）；冲突配置由后出现的（更具体的）覆盖先出现的（更通用的）@@REF_19@@。

### Override 机制与本地定制

OpenAI Codex 原生支持 `AGENTS.override.md` 文件，其优先级高于同级 `AGENTS.md`。当 override 文件存在时，同级 AGENTS.md 被**完全跳过**而非合并@@REF_18@@。此机制适用于：
*   **临时全局覆写**：在 `~/.codex/AGENTS.override.md` 设置临时指导，完成后删除即恢复原配置@@REF_9@@。
*   **子目录特殊规则**：如支付服务目录需要完全不同的测试命令和安全约束@@REF_9@@。
*   **个人定制**：社区惯例将 `AGENTS.override.md` 加入 `.gitignore`，用于存放个人偏好（如 pnpm vs npm）而不影响团队共享配置@@REF_5@@。

需注意，`AGENTS.override.md` 并非 AGENTS.md 官方规范的一部分，而是 Codex 特有的实现；其他工具可能不支持此文件名@@REF_5@@。

### 指令优先级链

完整的优先级从高到低为：
1.  用户聊天中的显式指令（最高优先级，覆盖一切）
2.  最近的 AGENTS.md（子目录）
3.  根目录 AGENTS.md
4.  工具默认配置

README.md 与其他文档与 AGENTS.md 是互补关系，不参与此覆盖链@@REF_5@@。

## 三、长度控制与 Token 成本分析

AGENTS.md 在每次会话启动或每条消息中被加载，直接计入输入 Token 消耗。长度控制不仅是工程规范，更是成本与效果的关键变量。

### 推荐长度阈值

*   **根目录文件**：建议控制在 **100-200 行**以内。超过 150-200 行时应考虑拆分至子目录@@REF_2@@。
*   **Codex 硬限制**：合并后的指令总大小默认上限为 **32 KiB**，超出部分按加载顺序从末尾截断，可通过 `project_doc_max_bytes` 调整@@REF_18@@。
*   **Claude Code 建议**：单文件低于 **200 行**，超过 4 MiB 的文件会被跳过@@REF_1@@。
*   **Cursor 建议**：规则文件低于 **500 行**@@REF_1@@。
*   **Antigravity 硬限制**：单文件 **12,000 字符**@@REF_1@@。

### Token 成本的学术量化

两篇 2026 年的实证研究提供了看似矛盾但实则互补的数据：

| 指标 | Lulla et al. (2026)@@REF_7@@ | Gloaguen et al. (2026)@@REF_4@@ |
| :--- | :--- | :--- |
| **样本规模** | 10 个仓库，124 个 PR | SWE-BENCH + CTXBENCH，多 Agent 多 LLM |
| **上下文类型** | 开发者编写的 AGENTS.md | LLM 生成 vs 开发者编写 |
| **运行时间** | 中位数 **-28.64%** (p<0.05) | 未直接报告 |
| **输出 Token** | 中位数 **-16.58%** (p<0.05) | 未直接报告 |
| **推理成本** | 未直接报告 | **+20%~23%** (LLM生成) / **+19%** (人工) |
| **推理步骤** | 未直接报告 | **+2.45~3.92步** (LLM生成) / **+3.34步** (人工) |
| **任务成功率** | 未量化（人工抽检质量相当） | LLM生成 **-0.5%~-2%**；人工 **+2.4%** (不显著) |

**综合分析**：
*   **AGENTS.md 能显著降低输出侧消耗**：Lulla 的研究表明，提供明确的仓库结构和约定可减少 Agent 的探索性导航和重复请求，从而降低输出 Token 和运行时间@@REF_7@@。
*   **输入侧成本必然增加**：无论内容质量如何，AGENTS.md 本身作为额外上下文都会增加输入 Token 和推理步骤@@REF_4@@。
*   **内容质量决定净收益**：LLM 自动生成的文件因与现有文档冗余，导致“负收益”（成本增加且成功率下降）；人工编写的文件虽增加输入成本，但通过减少无效探索实现了输出侧的更大节省，且成功率有边际提升@@REF_4@@。
*   **Prompt Cache 是关键缓解手段**：缓存读取比标准输入便宜 90%，频繁使用的 AGENTS.md 应确保能被缓存命中@@REF_2@@。

## 四、失效模式与维护方式

### 四大失效模式

1.  **自动生成文件的负效应**：LLM 生成的上下文文件在 5/8 的实验设置中降低了任务成功率，原因是其与 Agent 已能独立发现的文档内容冗余，增加了噪声而非信号@@REF_2@@。
2.  **规则膨胀与矛盾积累**：每次 Agent 犯错就新增规则，但从不删除旧规则，导致文件累积矛盾的补丁和一次性修复，直接对抗有效的上下文工程@@REF_2@@。研究表明，更多规则并不产生更好表现@@REF_2@@。
3.  **长会话中的静默丢失（Lost in the Middle）**：随着上下文增长，Agent 可能忽略中间位置的指令，保留架构决策但丢弃具体约束@@REF_2@@。关键规则应放在文件开头，长任务应开启新会话@@REF_2@@。
4.  **过时结构描述的误导**：记录仓库目录结构的 AGENTS.md 在代码库变更后成为负债，过时的架构概述会增加推理成本并鼓励无效的广泛文件遍历@@REF_2@@。

### 维护最佳实践

*   **从错误中迭代，而非预先堆砌**：仅在观察到可复现的失败后才补充对应约束，避免一次性写入大量推测性规则。
*   **纳入 Git 版本控制**：AGENTS.md 是项目资产，更新应像代码变更一样经过 Review。
*   **CI 自动化防膨胀**：在 CI 中检查 AGENTS.md 行数（如 ≤100 行），超出则阻断并要求迁移内容至 Spec/Wiki/Skill@@REF_15@@。
*   **知识升级流程**：一次问题 → 记录现象 → 判断是否可复现 → 验证解决方式 → 决定进入 Wiki、Skill 还是硬规则。能由 lint/CI/hooks 拦截的规则不要进 AGENTS.md@@REF_15@@。
*   **定期审计与清理**：检查规则是否在多处重复（`grep -rn "规则关键词"`）；移除不再适用的约束；验证 Skill 是否真的被触发@@REF_15@@。
*   **验证生效**：修改 AGENTS.md 后需开启新对话或重启工具，现有对话不会自动应用更新。

## 五、各家工具的兼容差异详解

尽管 AGENTS.md 已被 20+ 工具支持@@REF_3@@，但各工具的读取机制、优先级规则和大小限制存在显著差异。**没有任何两个工具以完全相同的方式读取 AGENTS.md**@@REF_1@@。

### 主流工具兼容性矩阵

| 工具 | 读取的文件 | 嵌套支持 | 大小限制 | 每轮发送 | 特殊行为 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **OpenAI Codex** | `AGENTS.override.md` > `AGENTS.md` > 配置的备选名；每目录最多一个@@REF_1@@ | ✅ 从根到工作目录逐级拼接@@REF_1@@ | **32 KiB** 硬限制（可配）@@REF_1@@ | 每次运行构建一次@@REF_1@@ | Override 文件存在时同级 AGENTS.md 被完全跳过@@REF_9@@ |
| **Cursor** | `.cursor/rules/**/*.mdc` + 根/子目录 `AGENTS.md`@@REF_1@@ | ✅ AGENTS.md 按目录；.mdc 按 glob@@REF_1@@ | 建议 <500 行（非硬限）@@REF_1@@ | 应用于模型上下文开头@@REF_1@@ | Team Rules > Project Rules > User Rules@@REF_1@@ |
| **GitHub Copilot** | `.github/copilot-instructions.md` + `.instructions.md` + `AGENTS.md` + `CLAUDE.md` + `GEMINI.md`@@REF_1@@ | ✅ AGENTS.md 就近胜出@@REF_1@@ | 未文档化@@REF_1@@ | **是**，每条消息@@REF_1@@ | 所有相关指令集均提供，非互斥@@REF_1@@ |
| **Claude Code** | `CLAUDE.md` 系列优先；无 CLAUDE.md 时读 `AGENTS.md`@@REF_1@@ | ✅ 父级启动加载，子级按需加载@@REF_1@@ | 建议 <200 行；>4MiB 跳过@@REF_1@@ | 会话启动加载@@REF_1@@ | v2.1.277+ 支持；可配置为同时读取两者@@REF_1@@；支持 `@path` 导入（最多4层）@@REF_3@@ |
| **Devin Desktop (Windsurf)** | `AGENTS.md` / `agents.md` + `.devin/rules/` + `.windsurf/rules/`@@REF_10@@ | ✅ 根目录=always-on；子目录=glob `<dir>/**`@@REF_10@@ | 未文档化 | 根目录内容每条消息包含@@REF_10@@ | 2026.6.2 Windsurf 退役更名 Devin Desktop@@REF_20@@；Devin Local 通过 CLI 规则系统读取@@REF_10@@ |
| **Cline** | `.clinerules/` + `.cline/rules/` + `.cursorrules` + `.windsurfrules` + `AGENTS.md`@@REF_1@@ | ⚠️ 未文档化为目录遍历；按路径 glob 作用域@@REF_1@@ | 未文档化（警告消耗上下文）@@REF_1@@ | **是**，每条规则每次请求加载（除非条件限定）@@REF_1@@ | 全局规则在 `~/.agents/AGENTS.md`@@REF_16@@；支持 YAML frontmatter 条件激活@@REF_16@@ |
| **Gemini CLI** | 默认 `GEMINI.md`；需在 settings 中配置 `context.fileName` 读 AGENTS.md@@REF_1@@ | ✅ 工作区及父级启动加载 + 即时读取@@REF_1@@ | 未文档化@@REF_1@@ | **是**，每条提示@@REF_1@@ | 托管版已于 2026.6.18 退役@@REF_1@@ |
| **Google Antigravity** | `GEMINI.md` + `AGENTS.md` + `.agents/rules/*.md`@@REF_1@@ | ❓ 未文档化@@REF_1@@ | **12,000 字符**硬限制@@REF_1@@ | 提示扩展时注入@@REF_1@@ | 优先级规则未文档化@@REF_1@@ |
| **Continue** | `.continue/rules/*.md` + config.yaml@@REF_1@@ | ❓ 未文档化@@REF_1@@ | 未文档化@@REF_1@@ | Agent/Chat/Edit 请求适用@@REF_1@@ | **文档未提及 AGENTS.md 支持**@@REF_1@@ |

### 跨工具兼容策略

对于使用多个 AI 编程工具的团队，推荐以下策略@@REF_3@@：

1.  **以 AGENTS.md 为唯一事实来源**：它是覆盖面最广的标准文件，Codex、Cursor、Copilot、Devin/Windsurf、Cline 等均原生支持@@REF_3@@。
2.  **为 Claude Code 创建桥接文件**：在项目根目录创建 `CLAUDE.md`，内容仅为一行 `@AGENTS.md`，利用 Claude Code 的导入功能指向同一份内容@@REF_3@@。或在 v2.1.277+ 中通过 `/config` 设置启用 AGENTS.md 回退读取@@REF_21@@。
3.  **为 Gemini CLI 配置文件名**：在 `.gemini/settings.json` 中设置 `{ "context": { "fileName": "AGENTS.md" } }`@@REF_11@@。
4.  **删除遗留文件**：`.cursorrules` 已被 Cursor 官方标记为 legacy，应迁移至 `.cursor/rules/*.mdc` 或直接由 AGENTS.md 替代@@REF_3@@。
5.  **工具特定规则分离**：需要 glob 作用域、YAML frontmatter 或特定工具功能的规则，放入该工具专属的规则目录（如 `.cursor/rules/`、`.clinerules/`、`.claude/rules/`），AGENTS.md 仅保留跨工具通用的基线指令@@REF_3@@。