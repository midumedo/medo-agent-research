# Harness 机制研究记录与复核材料

作者：Codex / GPT-6 · 日期：2026-09-26

对应正文：[Repo-context 如何真正进入模型](../harness-mechanisms.md)

这是当次研究记录，不是新增的项目规则。事实分成固定源码静态检查、官方网页观测、本地小型输出观测三种；本轮未运行 Codex、Gemini CLI 或 Tianshu 的 Agent 会话，未进行模型实验。没有读取本机用户配置、密钥或个人记忆。

## 范围与实际推进

先读取根与 `domain/`、`domain/repo-context/`、`sources/`、`sources/repos/` 的约定，随后读 `CONVENTIONS.md`、`STYLE.md`，以既有 `04how-agent-read-file/` 作为待验证线索。选择 Codex、Gemini CLI、Tianshu-harness，是为了覆盖 shell 读取、带 JIT 的专用读取、结构感知裁剪三种差异，并非代表市场份额或产品质量排名。

实际顺序为：确认本地路径和版本 → 查项目指令发现与预算 → 查模型可见工具及其下游结果处理 → 查技能发现/正文注入 → 对照旧判断 → 运行一次不调用模型的列投影 → 写结论与本记录。所有命令在 `D:\workspace\memory` 的 PowerShell 中执行。以下记录保留足够的命令重建取证过程，不保留几十份重复全文输出。

## 证据索引

### H01 版本与本地文件核对

本地版本来源是 [`sources/repos/_commits.json`](../../../../sources/repos/_commits.json) 与 [`index.csv`](../../../../sources/repos/index.csv)。它们是 tar 快照登记，不是 checkout 内的 Git 历史。

| 对象 | 本轮使用 commit | 登记的获取日期 | 本轮额外核对 |
|---|---|---|---|
| openai/codex | `75e0e0aad97a86138b8b1ec87d9b544b4a35ecbf` | 2026-09-25 | `codex-rs/core/src/agents_md.rs` 对固定 commit raw 内容，统一 CRLF/LF 后相等 |
| google-gemini/gemini-cli | `bedef96ef42905bd84a86dbec021c706168e7e2f` | 2026-09-24 | 账本仅存 12 位；GitHub commit API 解析出完整 SHA；`packages/core/src/tools/read-file.ts` 比对相等 |
| huiliyi37/Tianshu-harness | `79c10d30ba4fff8aaccfed30410d75050cecb451` | 2026-09-25 | `src/prompt/project-instructions.ts` 比对相等 |

实际查询：

```powershell
$rows = Import-Csv sources/repos/index.csv
$rows | Where-Object { $_.id -in @('codex','gemini-cli','Tianshu-harness') } | ConvertTo-Json
$meta = Get-Content sources/repos/_commits.json -Raw | ConvertFrom-Json
$meta.codex
$meta.'gemini-cli'
$meta.'Tianshu-harness'
Invoke-RestMethod -Uri 'https://api.github.com/repos/google-gemini/gemini-cli/commits/bedef96ef429'
```

Gemini API 返回的 commit 时间为 `2026-09-24T21:49:16Z`。这用于解析已有短 SHA，不是更新快照。代表文件比对的实际核心操作如下，对表中三组参数逐一执行，结果均为 `True`：

```powershell
$remote = (Invoke-WebRequest -Uri ('https://raw.githubusercontent.com/'+$t.repo+'/'+$t.sha+'/'+$t.file) -UseBasicParsing).Content
if ($remote -is [byte[]]) { $remote = [System.Text.Encoding]::UTF8.GetString($remote) }
$local = Get-Content -LiteralPath $t.local -Raw
$remote.Replace("`r`n","`n") -eq $local.Replace("`r`n","`n")
```

边界：这是代表文件的内容核对，不能声称完整仓库每个文件都做了哈希验证。访问日期均为 2026-09-26。

### H02 Codex 祖先发现与每层择一

源码：[`agents_md.rs:189–295`](https://github.com/openai/codex/blob/75e0e0aad97a86138b8b1ec87d9b544b4a35ecbf/codex-rs/core/src/agents_md.rs#L189)。祖先目录从 root 到 cwd；无发现的项目根时只查当前目录。每层按 override、默认文件、fallback 顺序，找到文件即返回该层候选。因此“每层多个名字同时相加”不符合该实现。

定位命令：

```powershell
rg --no-ignore -n 'AGENTS.override.md|candidate_filenames|search_dirs' sources/repos/codex/codex-rs/core/src/agents_md.rs
```

### H03 Codex 项目指令累计预算

源码：[`agents_md.rs:58–115`](https://github.com/openai/codex/blob/75e0e0aad97a86138b8b1ec87d9b544b4a35ecbf/codex-rs/core/src/agents_md.rs#L58)、[`agents_md.rs:125–179`](https://github.com/openai/codex/blob/75e0e0aad97a86138b8b1ec87d9b544b4a35ecbf/codex-rs/core/src/agents_md.rs#L125)、[`config_toml.rs:74–81`](https://github.com/openai/codex/blob/75e0e0aad97a86138b8b1ec87d9b544b4a35ecbf/codex-rs/config/src/config_toml.rs#L74)。

静态检查：先设 `remaining = config.project_doc_max_bytes`，跨 turn environments 递减；环境内逐文件读取完整字节后 `data.truncate(remaining as usize)`，非空内容进入 entries 后减掉使用量。默认为 `32 * 1024`。用户/线程指令不在这个项目文件循环里。

这个证据只证明预算控制与路径顺序。本文的 40 KiB 拆分算例是源码逻辑推演，没有运行模型或集成测试。

### H04 Codex 缓存与注入

源码：[`agents_md_manager.rs:79–139`](https://github.com/openai/codex/blob/75e0e0aad97a86138b8b1ec87d9b544b4a35ecbf/codex-rs/core/src/agents_md_manager.rs#L79)、[`agents_md.rs:386–418`](https://github.com/openai/codex/blob/75e0e0aad97a86138b8b1ec87d9b544b4a35ecbf/codex-rs/core/src/agents_md.rs#L386)、[`context/world_state/agents_md.rs:26–76`](https://github.com/openai/codex/blob/75e0e0aad97a86138b8b1ec87d9b544b4a35ecbf/codex-rs/core/src/context/world_state/agents_md.rs#L26)、[`session/world_state.rs:163`](https://github.com/openai/codex/blob/75e0e0aad97a86138b8b1ec87d9b544b4a35ecbf/codex-rs/core/src/session/world_state.rs#L163)。

静态检查：缓存重建条件含环境 selection 与项目 trust 变化；相同快照的 world-state diff 可以不发新片段，不同快照构成替换/移除文本。不能从这里推断所有宿主的热更新行为，更不能把磁盘每次修改都视作立刻更新模型输入。

### H05 Codex shell 工具面

源码：[`tools/spec_plan.rs:1079–1116`](https://github.com/openai/codex/blob/75e0e0aad97a86138b8b1ec87d9b544b4a35ecbf/codex-rs/core/src/tools/spec_plan.rs#L1079)、[`handlers/shell_spec.rs:35–113`](https://github.com/openai/codex/blob/75e0e0aad97a86138b8b1ec87d9b544b4a35ecbf/codex-rs/core/src/tools/handlers/shell_spec.rs#L35)、[`unified_exec/mod.rs:79`](https://github.com/openai/codex/blob/75e0e0aad97a86138b8b1ec87d9b544b4a35ecbf/codex-rs/core/src/unified_exec/mod.rs#L79)。

有环境、shell feature 启用且模型未禁用 shell 时，core 注册执行工具；统一执行可注册 `write_stdin`。schema 中有命令、工作目录、`max_output_tokens`，默认输出预算 10,000。检索 core 工具目录，未发现内建通用文件读工具的注册；命中包含 MCP 文件工具测试和 `read_mcp_resource`，不能据此宣称整个产品只能 shell。

实际负向检索范围：

```powershell
rg --no-ignore -n 'name: "read_file"|name: "read"|tool_name.*read|ToolName::plain\("read' sources/repos/codex/codex-rs/core/src/tools --glob '*.rs'
```

### H06 Codex 技能分来源加载

源码：[`ext/skills/src/tools/mod.rs:55–96`](https://github.com/openai/codex/blob/75e0e0aad97a86138b8b1ec87d9b544b4a35ecbf/codex-rs/ext/skills/src/tools/mod.rs#L55)、[`tools/read.rs:34–67`](https://github.com/openai/codex/blob/75e0e0aad97a86138b8b1ec87d9b544b4a35ecbf/codex-rs/ext/skills/src/tools/read.rs#L34)、[`host_prompt.rs:69–96`](https://github.com/openai/codex/blob/75e0e0aad97a86138b8b1ec87d9b544b4a35ecbf/codex-rs/ext/skills/src/host_prompt.rs#L69)、[`session/turn.rs:1054–1090`](https://github.com/openai/codex/blob/75e0e0aad97a86138b8b1ec87d9b544b4a35ecbf/codex-rs/core/src/session/turn.rs#L1054)。

存在有条件的 `skills` namespace list/read，read 接受 package/resource/cursor 并返回 next_cursor。显式提及 host skill 的路径可构建 contextual-user 片段。agent-plugin skill 的正文经过 `truncate_main_prompt_contents`，其上限常量在 [`render.rs:19`](https://github.com/openai/codex/blob/75e0e0aad97a86138b8b1ec87d9b544b4a35ecbf/codex-rs/ext/skills/src/render.rs#L19) 为 8,000 字节；不能把它扩大成所有技能正文统一上限。`tools/read.rs:155–158` 说明分页可复用快照，续页不自动反映文件更改。

发现阶段读取内容解析元数据的入口见 [`loader/environment.rs:60–78`](https://github.com/openai/codex/blob/75e0e0aad97a86138b8b1ec87d9b544b4a35ecbf/codex-rs/ext/skills/src/loader/environment.rs#L60)。这区分了“程序读过”与“模型收到正文”。

### H07 Codex 隐式检测的真实含义

源码：[`skills/src/invocation.rs:12–71`](https://github.com/openai/codex/blob/75e0e0aad97a86138b8b1ec87d9b544b4a35ecbf/codex-rs/skills/src/invocation.rs#L12)、[`invocation.rs:111–143`](https://github.com/openai/codex/blob/75e0e0aad97a86138b8b1ec87d9b544b4a35ecbf/codex-rs/skills/src/invocation.rs#L111)。函数 tokenize shell command，识别 script runner 或 `ParsedCommand::Read` 路径，再查技能索引；不在此处将用户任务描述和 skill 描述做语义匹配。

模型的描述匹配提示另在 [`ext/skills/src/catalog_prompt.rs`](https://github.com/openai/codex/blob/75e0e0aad97a86138b8b1ec87d9b544b4a35ecbf/codex-rs/ext/skills/src/catalog_prompt.rs)。源码中的提示是研究对象，不是本轮的额外工作指令。

### H08 Gemini 初始化与 import

源码：[`context/memoryContextManager.ts:38–95`](https://github.com/google-gemini/gemini-cli/blob/bedef96ef42905bd84a86dbec021c706168e7e2f/packages/core/src/context/memoryContextManager.ts#L38)、[`utils/memoryDiscovery.ts:209–241`](https://github.com/google-gemini/gemini-cli/blob/bedef96ef42905bd84a86dbec021c706168e7e2f/packages/core/src/utils/memoryDiscovery.ts#L209)、[`memoryDiscovery.ts:405–430`](https://github.com/google-gemini/gemini-cli/blob/bedef96ef42905bd84a86dbec021c706168e7e2f/packages/core/src/utils/memoryDiscovery.ts#L405)、[`memoryImportProcessor.ts:190–216`](https://github.com/google-gemini/gemini-cli/blob/bedef96ef42905bd84a86dbec021c706168e7e2f/packages/core/src/utils/memoryImportProcessor.ts#L190)。

初始化发现 global/extension/project/private-project 路径，去重后读取；正文处理 import；该调用默认 tree import，状态中最大深度为 5。workspace root 向上查到项目边界，未找到边界时以 root 为界。初始化结果经 [`config.ts:2564–2573`](https://github.com/google-gemini/gemini-cli/blob/bedef96ef42905bd84a86dbec021c706168e7e2f/packages/core/src/config/config.ts#L2564) 与 [`prompts/snippets.ts:524–575`](https://github.com/google-gemini/gemini-cli/blob/bedef96ef42905bd84a86dbec021c706168e7e2f/packages/core/src/prompts/snippets.ts#L524) 构成上下文段。此处只检查公开源码里的路径表达，未访问本机实际私有文件。

### H09 Gemini JIT 与已加载状态

源码：[`tools/read-file.ts:194–202`](https://github.com/google-gemini/gemini-cli/blob/bedef96ef42905bd84a86dbec021c706168e7e2f/packages/core/src/tools/read-file.ts#L194)、[`tools/jit-context.ts:18–60`](https://github.com/google-gemini/gemini-cli/blob/bedef96ef42905bd84a86dbec021c706168e7e2f/packages/core/src/tools/jit-context.ts#L18)、[`memoryDiscovery.ts:512–647`](https://github.com/google-gemini/gemini-cli/blob/bedef96ef42905bd84a86dbec021c706168e7e2f/packages/core/src/utils/memoryDiscovery.ts#L512)、[`memoryContextManager.ts:141–171`](https://github.com/google-gemini/gemini-cli/blob/bedef96ef42905bd84a86dbec021c706168e7e2f/packages/core/src/context/memoryContextManager.ts#L141)。

JIT 有 trusted folder/root 条件；从访问文件的父目录向上找；按文件身份排除先前已加载项，记录新加载项，连接正文返回。调用方把结果附加到工具 LLM content。负向检索 `shell.ts` 未命中 `discoverJitContext`，这只限制在该工具实现与此次搜索。

### H10 Gemini read_file 的两种截断

源码：[`tools/read-file.ts:52–67`](https://github.com/google-gemini/gemini-cli/blob/bedef96ef42905bd84a86dbec021c706168e7e2f/packages/core/src/tools/read-file.ts#L52)、[`utils/fileUtils.ts:522–528`](https://github.com/google-gemini/gemini-cli/blob/bedef96ef42905bd84a86dbec021c706168e7e2f/packages/core/src/utils/fileUtils.ts#L522)、[`fileUtils.ts:557–597`](https://github.com/google-gemini/gemini-cli/blob/bedef96ef42905bd84a86dbec021c706168e7e2f/packages/core/src/utils/fileUtils.ts#L557)、[`utils/constants.ts:10–12`](https://github.com/google-gemini/gemini-cli/blob/bedef96ef42905bd84a86dbec021c706168e7e2f/packages/core/src/utils/constants.ts#L10)。

文本 schema 是 file_path/start_line/end_line，行号从 1 开始、end 含边界；默认 2,000 行，显式 end 没有再次按 2,000 截选区；每行长于 2,000 字符另行截短。文件有 20 MB 大小门。这里按源码常量原单位记录，不换算 token。

### H11 Gemini 多文件与工具结果裁剪

源码：[`tools/read-many-files.ts:235–263`](https://github.com/google-gemini/gemini-cli/blob/bedef96ef42905bd84a86dbec021c706168e7e2f/packages/core/src/tools/read-many-files.ts#L235)、[`read-many-files.ts:323–328`](https://github.com/google-gemini/gemini-cli/blob/bedef96ef42905bd84a86dbec021c706168e7e2f/packages/core/src/tools/read-many-files.ts#L323)、[`read-many-files.ts:377–440`](https://github.com/google-gemini/gemini-cli/blob/bedef96ef42905bd84a86dbec021c706168e7e2f/packages/core/src/tools/read-many-files.ts#L377)、[`scheduler/tool-executor.ts:340–405`](https://github.com/google-gemini/gemini-cli/blob/bedef96ef42905bd84a86dbec021c706168e7e2f/packages/core/src/scheduler/tool-executor.ts#L340)。

多文件先按 ignore/access 过滤，逐文件调用同一 reader，不传行区间；每文件包装为结果 part，涉及目录另做 JIT。scheduler 上限常量为 `64 * 1024` 字节，对单 string 或数组各文本 part 裁剪；不是数组总和限制。工具成功路径在 `tool-executor.ts:484–485` 调用该裁剪函数。

shell 可配置摘要见 [`tools/shell.ts:1100–1132`](https://github.com/google-gemini/gemini-cli/blob/bedef96ef42905bd84a86dbec021c706168e7e2f/packages/core/src/tools/shell.ts#L1100)。未展开所有压缩/历史重写路径，因此本记录不声称逐 part 预算就是最终请求级预算。

### H12 Gemini skill 加载与激活

源码：[`skills/skillLoader.ts:164–186`](https://github.com/google-gemini/gemini-cli/blob/bedef96ef42905bd84a86dbec021c706168e7e2f/packages/core/src/skills/skillLoader.ts#L164)、[`prompts/snippets.ts:314–333`](https://github.com/google-gemini/gemini-cli/blob/bedef96ef42905bd84a86dbec021c706168e7e2f/packages/core/src/prompts/snippets.ts#L314)、[`tools/activate-skill.ts:130–153`](https://github.com/google-gemini/gemini-cli/blob/bedef96ef42905bd84a86dbec021c706168e7e2f/packages/core/src/tools/activate-skill.ts#L130)。

loader 读完整文件解析 metadata 与 body；提示只列 name/description/location；activation 标记技能、扩展 workspace 可读目录并把 body 与资源树返回。这是模型可见层面的延迟展开，不是“直到激活才首次读盘”。后续输出仍经过公共工具路径。

### H13 Tianshu 本目录两文件读取

源码：[`prompt/volatile.ts:426–472`](https://github.com/huiliyi37/Tianshu-harness/blob/79c10d30ba4fff8aaccfed30410d75050cecb451/src/prompt/volatile.ts#L426)、[`volatile.ts:1110–1128`](https://github.com/huiliyi37/Tianshu-harness/blob/79c10d30ba4fff8aaccfed30410d75050cecb451/src/prompt/volatile.ts#L1110)。

该 loader 在信任条件通过后读 cwd 下 `AGENTS.md` 和 `.rivet.md`，按顺序连接；缓存 TTL 30 秒。调用方可直接提供 `ctx.rivetMd`，也可存在 frozen-prefix 生命周期影响，故不能由这个 TTL 推出会话内所有更新延迟恰为 30 秒。没有据此宣称全仓库其他路径都不支持更深目录。

### H14 Tianshu 按节选择与真实预算

源码：[`prompt/project-instructions.ts:20–107`](https://github.com/huiliyi37/Tianshu-harness/blob/79c10d30ba4fff8aaccfed30410d75050cecb451/src/prompt/project-instructions.ts#L20)、[`project-instructions.ts:118–179`](https://github.com/huiliyi37/Tianshu-harness/blob/79c10d30ba4fff8aaccfed30410d75050cecb451/src/prompt/project-instructions.ts#L118)、[`prompt/block-policy.ts:12–35`](https://github.com/huiliyi37/Tianshu-harness/blob/79c10d30ba4fff8aaccfed30410d75050cecb451/src/prompt/block-policy.ts#L12)、[`context/payload-diagnostic.ts:45–55`](https://github.com/huiliyi37/Tianshu-harness/blob/79c10d30ba4fff8aaccfed30410d75050cecb451/src/context/payload-diagnostic.ts#L45)。

结构分类、优先选择和恢复原顺序均为实现体行为；每节按转义后长度计费。standard cap 是 8,000 字符，subagent 覆盖为 4,000；6,000 是建议候选条件。源码注释中描述的历史事故、31% 转义膨胀和探针覆盖率没有被本轮复现，不作为本项目观测。

### H15 Tianshu read_file 的状态和分摊

源码：[`tools/read-file.ts:538–648`](https://github.com/huiliyi37/Tianshu-harness/blob/79c10d30ba4fff8aaccfed30410d75050cecb451/src/tools/read-file.ts#L538)、[`read-file.ts:743–758`](https://github.com/huiliyi37/Tianshu-harness/blob/79c10d30ba4fff8aaccfed30410d75050cecb451/src/tools/read-file.ts#L743)、[`read-file.ts:844–883`](https://github.com/huiliyi37/Tianshu-harness/blob/79c10d30ba4fff8aaccfed30410d75050cecb451/src/tools/read-file.ts#L844)、[`read-file.ts:1049–1082`](https://github.com/huiliyi37/Tianshu-harness/blob/79c10d30ba4fff8aaccfed30410d75050cecb451/src/tools/read-file.ts#L1049)。

此路径明确拒绝 gitignored 文件，focus 与显式范围是不同分支；大文件可成 partial view。多文件取前 5 个，并把总体 cap 的 max/head/tail 各自均分。启用 read-ref 后，未变的重复读取可返回引用；已经返回引用而再次请求时可以退回内容。没有把可配置分支写成始终启用。

### H16 Tianshu skill 目录与重新注入

源码：[`skills/skill-loader.ts:241–293`](https://github.com/huiliyi37/Tianshu-harness/blob/79c10d30ba4fff8aaccfed30410d75050cecb451/src/skills/skill-loader.ts#L241)、[`skill-loader.ts:324–342`](https://github.com/huiliyi37/Tianshu-harness/blob/79c10d30ba4fff8aaccfed30410d75050cecb451/src/skills/skill-loader.ts#L324)、[`tools/skill.ts:64–90`](https://github.com/huiliyi37/Tianshu-harness/blob/79c10d30ba4fff8aaccfed30410d75050cecb451/src/tools/skill.ts#L64)、[`prompt/engine.ts:589`](https://github.com/huiliyi37/Tianshu-harness/blob/79c10d30ba4fff8aaccfed30410d75050cecb451/src/prompt/engine.ts#L589)。

发现块缺省描述预算 1,500 字符，单描述截到 200；触发正则命中者优先。装不下时跳过候选并留下遗漏数。`skill` 返回正文/附属文件名；调用记录可让 dynamic appendix 重建正文，complete 回调结束此状态。正文返回处无局部截断，不能推出下游也无裁剪。

### H17 官方文档表述差异

2026-09-26 实际以 HTTP 读取以下官方页面并查关键字符串：

- [AGENTS guide](https://developers.openai.com/codex/guides/agents-md)：包含 combined size 达到 `project_doc_max_bytes` 即停止增加文件的说明。
- [Advanced configuration](https://developers.openai.com/codex/config-advanced)：参数说明使用 each `AGENTS.md` file 的措辞。

两页都不是固定 commit 文档；本轮不猜测谁更新较晚。H03 的固定代码给出本次采用的解释。实际命令：

```powershell
$r = Invoke-WebRequest -Uri 'https://developers.openai.com/codex/guides/agents-md' -UseBasicParsing
[regex]::Matches($r.Content,'.{0,200}project_doc_max_bytes.{0,300}') | ForEach-Object {$_.Value}
$r = Invoke-WebRequest -Uri 'https://developers.openai.com/codex/config-advanced' -UseBasicParsing
[regex]::Matches($r.Content,'.{0,300}project_doc_max_bytes.{0,350}') | ForEach-Object {$_.Value}
```

研究通信中曾两次把待查线索误写成“已核验”，随即明确撤回；上面的结论只依据随后实际执行且成功的 HTTP 结果。首次记录 `BaseResponse.ResponseUri.AbsoluteUri` 返回 null，所以本文不声称成功记录了重定向终点。没有为消除文档措辞差异而反复抓取。

### H18 本地 CSV 列投影观测

目的：检验“没有专用 read 列参数就做不到列投影”是否成立。对象为项目现有 `sources/repos/index.csv` 的三条 harness 行。观测不是模型实验，也没有修改该文件。

实际命令：

```powershell
$rows = Import-Csv sources/repos/index.csv | Where-Object {$_.id -in @('codex','gemini-cli','Tianshu-harness')}
$full = ($rows | ConvertTo-Csv -NoTypeInformation) -join "`n"
$projected = ($rows | Select-Object id,snapshot | ConvertTo-Csv -NoTypeInformation) -join "`n"
[System.Text.Encoding]::UTF8.GetByteCount($full)
[System.Text.Encoding]::UTF8.GetByteCount($projected)
$projected
```

返回六列统一序列化 509 字节、两列 99 字节；投影内容为 id 与 snapshot。两个数均含列名和换行，分母都是相同的 3 条数据行。它证明当前工具/解释器可以先解析 CSV 再只输出指定列；它不证明所有机器装有同样解释器，也未测 token、可靠性、延迟或端到端成本。

## 失败查询与判断修正

| 实际遇到的情况 | 修正与适用边界 |
|---|---|
| 旧线索指向 Codex `core/src/project_doc.rs`、`tools/spec.rs`、`core/src/codex.rs`；路径不存在 | 先 `rg --files --no-ignore` 查当前树，入口已是 `agents_md.rs`、`spec_plan.rs`、`session/turn.rs`；不把旧路径空命中当机制不存在 |
| 初次 `rg` 对被忽略的 source checkout 搜不到目标 | 改用显式路径加 `--no-ignore`；负向结果必须记录忽略规则与范围 |
| 把 Gemini MemoryContextManager 猜在 utils/ 下，报文件不存在 | 文件发现命中 `context/memoryContextManager.ts` 后重读；没有靠相似名字补猜 |
| Tianshu `prompt/frozen.ts` 不存在 | 实际前缀代码在 `prompt/volatile.ts` 与 `prompt/block-policy.ts`；文件名不等于功能分类 |
| 多条大范围源码读回被工具输出截断 | 改为按已发现函数的行区间读回；正文引用取自后续可见片段，不依赖被截断部分 |
| 旧稿称 Codex skill 不是工具 | 缩小为 host 路径的一种方式；当前固定源码存在 executor/cloud 的条件式 list/read |
| 旧稿把隐式 skill invocation 解释成任务描述匹配 | 实现检查的是 shell 中读取/脚本路径；模型按描述选择属于另一机制 |
| 旧稿认为自动拼接意味着拆分零成本 | 发现累计预算与包装开销；拆分收益取决于选择集合变化 |
| 旧稿把无列 schema 推到必须整行支付 | H18 给出已有 shell+CSV 解析器反例；新增专用工具不是唯一可行路径 |
| 把 Tianshu 6,000 看成真实截断上限 | 找到渲染 policy，区分诊断 6,000、standard 8,000、subagent 4,000；未据此推模型性能阈值 |
| 只读 Gemini 三个常量可能误报 2,000 行硬上限 | 继续追到显式 end 分支和 scheduler，分开缺省选区、长行截短、下游 byte cap |

本轮没有覆盖全部旧稿结论，不以这里未讨论的部分表示认可；旧稿仍保持历史原貌。

## 可复用复核步骤

1. **固定对象**：记录 repo、commit、宿主/功能开关；确认文件实际可读。若只有 schema 或文档而无实现，将证据等级写明。
2. **找入口而非猜目录**：先查符号或文件名，再从注册器追到 handler；负向搜索必须注明目录、扩展名、ignore 策略。
3. **分别追三种内容**：自动项目指令、主动工具读取、skill；同名文件在这三条路径可有不同预算。
4. **列明选择条件**：cwd、根边界、候选文件优先级、信任条件、用户点名、provider 可用性。源文件不进入候选集时，优化其文风无助于该路径。
5. **追完整返回链**：底层读盘 → 行/字节选择 → 渲染包装 → scheduler/历史裁剪 → 注入位置。限额必须附单位与层次，查清 per-file、per-part、per-call 或累计范围。
6. **检查状态寿命**：什么集合记录“已读”，什么键触发刷新，是否用文件身份、mtime 或固定快照；压缩后的恢复另做观测。
7. **把反例作为测试材料**：同样正文单/多文件、长行、多字节字符、大小不均的批量文件、已加载后改写、默认与显式范围。这是建议的后续检查集，不是本轮已跑实验。
8. **先测最终输入，再测行为**：机制实验保存工具参数和最终输入片段；模型实验固定任务、模型、配置和 seed（若支持），保存成功率、证据覆盖、补读和计费。不能拿运行时字节差替代行为或 token 结果。

常用定位模板（本轮实际使用这一模式）：

```powershell
rg --files --no-ignore sources/repos/<repo>/<source-root>
rg --no-ignore -n '目标符号|调用方|预算常量' sources/repos/<repo>/<source-root> --glob '*.ts'
$p = '已发现的源文件'
$a = Get-Content $p
$a[($start-1)..($end-1)] | ForEach-Object -Begin {$n=$start} -Process {'{0}: {1}' -f $n++,$_}
```

停止条件是能为正在写的机制判断定位完整必要路径，并把未核对处标明；不是把仓库读完。后续若版本变化，应重新运行上述定位，保留本记录所用 commit，不在旧 SHA 下悄悄换成新实现。
