# codex · 根目录文档实测

> 快照 `75e0e0aad97a` · 取证 2026-09-25 · 来源 `sources/repos/codex/`
> 状态：verified ｜ 覆盖范围：仓库根目录直接子文件 + `docs/` 存根 + `.codex/skills/`

## 1. 根目录清单一览

| 文件 | 字节 | kind | 角色(D) | 一句话 |
|---|---|---|---|---|
| `AGENTS.md` | 22397 | agent-entry | D09 | 首行 `# Rust/codex-rs`，只管 Rust 子树的约定 |
| `README.md` | 3334 | facade | D01 | 门面，3.3KB（本样本最小的 README 之一） |
| `SECURITY.md` | 923 | collab-rule | D04 | 漏洞上报 |
| `CHANGELOG.md` | 330 | record | D02 | **指针文件**：正文指向 GitHub releases 页（见 §2.2） |
| `NOTICE` | 242 | legal | D06 | 无扩展名（对比 `NOTICE.md`） |

根级没有任何 `CLAUDE.md` / `GEMINI.md` / `CONTRIBUTING.md` / `CODE_OF_CONDUCT.md`。

## 2. 逐文件分析

### 2.1 `AGENTS.md`（22397 字节）

- **取到的原文**：L1 `# Rust/codex-rs`（`L1` 见 `index.csv`）；L2 起 `In the codex-rs folder where the rust code lives:` / `- Crate names are prefixed with \`codex-\` …`
- **它回答什么**：**只回答 codex-rs 子树**怎么写 Rust。文件放在仓库根，标题却写着子树名——`AGENTS.md` 的**辖域（根 / 子树）与落点（根目录）不一致**。
- **推论**：`AGENTS.md` 的辖域不能由路径推断。要判断一份 `AGENTS.md` 管谁，必须读它的**标题与首段**，或看同目录是否有更内层的覆盖文件。
- **对照**：`codex-rs/tui/src/bottom_pane/AGENTS.md` 是第二份，落在真正对应的子树里。

### 2.2 `CHANGELOG.md`（330 字节）—— 指针型变更记录

全文 6 行，首行：

```
The changelog can be found on the [releases page](https://github.com/openai/codex/releases).
## Unreleased
- Fix missing command lifecycle events when unified exec cannot create a process …
```

**形态**：`CHANGELOG.md` 这个名字保留了，但**记录本体在别处**（GitHub Releases）。文件里只留「未发布」段。这是 D02「CHANGELOG 单文件」的一个**未收录变体**：**指针型**。

### 2.3 `docs/` 是存根目录，不是文档库

| 文件 | 字节 | 内容 |
|---|---|---|
| `docs/license.md` | 84 | 仅 `## License` 标题 + 一句 |
| `docs/skills.md` | 115 | 仅 `# Skills` 标题 |
| `docs/sandbox.md` | 150 | 仅 `## Sandbox & approvals` 标题 |
| `docs/slash_commands.md` | 145 | 仅 `# Slash commands` 标题 |
| `docs/open-source-fund.md` | 340 | 一段 |

（另有 `agents_md.md` 126B、`exec.md` 146B、`execpolicy.md` 138B、`getting-started.md` 177B、`example-config.md` 134B、`config.md` 726B、`contributing.md` 3KB、`install.md` 3KB 等，`repo_map` 实测 15 份。）

**判据**：**文件存在 ≠ 内容存在**。15 份 `docs/*.md` 里多数是「标题 + 一句」，正文在官网。任何按「文件数」统计文档规模的做法在这里会严重虚高。

## 3. Agent 面（vibe coding 相关文件管理）

### 3.1 指令分级：根 + 1

```
AGENTS.md                                    ← 实为 codex-rs 子树约定
codex-rs/tui/src/bottom_pane/AGENTS.md       ← 更内层
```

无 `CLAUDE.md`、无 `GEMINI.md`。根级 dotdir：`.cargo`、`.codex`、`.github`、`.vscode`。

### 3.2 Skills：17 份，两处性质完全不同

| 位置 | 数量 | 性质 |
|---|---|---|
| `.codex/skills/` | 11 | **仓库自用的开发工作流**（`babysit-pr`、`code-review*`、`remote-tests`、`test-tui`、`update-v8-version` …） |
| `codex-rs/skills/src/assets/samples/` | 6 | **随产品分发的示例 skill**（`imagegen`、`openai-docs`、`plugin-creator`、`review-agent`、`skill-creator`、`skill-installer`） |

`code-review` 被拆成 5 个并列 skill（`code-review` / `-breaking-changes` / `-change-size` / `-context` / `-testing`）——**用多文件而非单文件长文**承载一个复杂工作流。这与 `deepseek-harness` 的单文件 `dsh-code-review`（9KB）是两种相反的组织方式。

### 3.3 `docs/skills.md` 的存在暗示

存根式 `docs/skills.md` 说明本仓把「skill 能力」当成**对外产品特性**在官网叙述，而 `.codex/skills/` 是**对内工作流**。同一名词两种受众，文件分置两处。

## 4. 与既有结论的冲突（反证）

| 既有结论 | 本轮实测 | 判定 |
|---|---|---|
| `sources/repos/index.csv` 对 codex 的关键词含 `read-tool-absent;exec-command-as-reader;skills-loader` | 根级无 `CLAUDE.md`/`GEMINI.md`；`AGENTS.md` 存在 | 无冲突 |
| D02：`CHANGELOG` 记「对外变化」，形态「单文件（+目录变体）」 | codex 的 `CHANGELOG.md` 是**指针型**（330B，正文在 Releases） | **形态清单不全**：除「单文件 / 目录」外还有「指针型」 |
| D09 边界：AGENTS.md 面向「仓库内的 AI Agent」 | `AGENTS.md` 标题为 `# Rust/codex-rs`，辖域 ≠ 落点 | **需补边界说明**：AGENTS.md 的辖域要读内容判断 |

## 5. 空白与未取证

- **未读** `docs/contributing.md`(3KB) 与 `docs/install.md`(3KB) 的正文——它们与存根不同，可能有实体内容。
- **未核对** `docs/` 其余 4 份（`authentication.md`、`sandbox.md` 之外的）的完整清单。
- **未验证** `.codex/skills/` 的加载器实现（`index.csv` 关键词记为 `skills-loader`，本轮未读源码）。
- **未确认** `NOTICE`（无扩展名）与 `.gitignore` 的追踪关系。
- 以上均属「在本次检索范围内未查」。
