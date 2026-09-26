# memU · 根目录文档实测

> 快照 `08e1ed4cdf4c` · 取证 2026-09-25 · 来源 `sources/repos/memU/`
> 状态：verified ｜ 覆盖范围：仓库根目录直接子文件 + 根级 SKILL.md

## 1. 根目录清单一览

| 文件 | 字节 | kind | 角色(D) | 一句话 |
|---|---|---|---|---|
| `AGENTS.md` | 3506 | agent-entry | D09 | 首行 `# AGENTS.md`；次节 `## Mission`——极短（3.5KB） |
| `SKILL.md` | 7549 | topic-manual | D12 | **仓库根级 skill**（唯一一例），首行是 YAML frontmatter `---` |
| `INSTALL-LATEST.md` | 5482 | topic-manual | D05 | **实为 skill 描述符**：首行也是 `---`，frontmatter 的 `name: install-memu-latest`（见 §2.2） |
| `README.md` | 11846 | facade | D01 | 门面（banner 图开头） |
| `CHANGELOG.md` | 38514 | record | D02 | Release Please 生成式（`## 2.0.0-beta.0 (2026-07-23)`） |
| `CONTRIBUTING.md` | 7220 | collab-rule | D03 | 贡献指南 |
| `LICENSE.txt` | 10897 | legal | D06 | 扩展名 `.txt`（非无扩展名、非 `.md`） |

## 2. 逐文件分析

### 2.1 `AGENTS.md`（3506 字节）—— 本样本最短的 agent 指令

首行裸 `# AGENTS.md`，次节 `## Mission`。对照 `deepseek-harness`(17805)、`Raven`(22349)、`codex`(22397)——**最短与最长差 6.4 倍**。

**判据**：`AGENTS.md` 这个名字**不承诺规模**。任何「AGENTS.md 应该多长」的讨论都要先说明是在哪个样本上说的。

### 2.2 `INSTALL-LATEST.md` 与 `SKILL.md` —— 两份**带 frontmatter 的 skill 描述符**

`head -1` 实测两份文件的首行**都是 `---`**（YAML frontmatter 起始）。进一步读到：

- `INSTALL-LATEST.md` 的 frontmatter：`name: install-memu-latest` / `description: Install the latest development build of memU-cli from git (main HEAD). Use when the user wants the newest unreleased code — clean any old install…`
- `SKILL.md` 的 frontmatter：`name: install-memu` / `description: Install or uninstall memU for whatever agent you are — identify your host, print its packaged guide, and follow it to wire (or unwire) both seams…`

**这是本阶段最重要的一条「名实不符」发现**：

| 期望（按文件名） | 实际（按首行与 frontmatter） |
|---|---|
| `INSTALL-LATEST.md` = 人类读的「如何安装最新版」 | **agent 读的 skill 描述符**（带 `name` / `description`，供 skill 加载器发现） |

`02docsdefine\ds.md` D05 把 `INSTALL-LATEST` 归入「流程与上手（RELEASING / QUICKSTART / INSTALL-LATEST）」，边界写「QUICKSTART 是 README 的最短路径切片」。**本仓的 `INSTALL-LATEST.md` 不满足这个边界**——它是 skill，不是上手文档。

→ **判据固化**：判断一份 `.md` 是「文档」还是「skill 描述符」，看**首行是不是 `---`（frontmatter）+ 是否含 `name`/`description`**，不看文件名。

### 2.3 `CHANGELOG.md`（38514 字节）—— 生成式

首行后的版本节是 `## 2.0.0-beta.0 (2026-07-23)` —— 带 compare 链接、日期、`### Features` 分组，是 **Release Please / semantic-release 一类工具的产物**。

**形态维度**：`CHANGELOG.md` 至少有 4 种形态（本样本实测）：

| 形态 | 仓 | 证据 |
|---|---|---|
| 人手写（Keep a Changelog） | `EverOS`、`OpenHands`、`Raven` | 首行 `# Changelog` + `All notable changes …` |
| 生成式（工具产出） | `memU`、`cline`（`## [4.1.21]`） | 版本节带 compare 链接 |
| 指针型 | `codex`（330B） | 正文指向 GitHub Releases |
| 目录化 | `Tianshu-harness`（`docs/changelog/` 41 篇日期文件） | 根级 CHANGELOG 只是聚合之一 |
| 膨胀失控 | `qwen-code`（888KB） | 单文件线性增长 |

## 3. Agent 面（vibe coding 相关文件管理）

### 3.1 指令分级：只有 1 份

全仓仅根级 `AGENTS.md`。无 `CLAUDE.md`、无 `GEMINI.md`、无子树同名文件。

### 3.2 Skills：**2 份，都在仓库根**

```
SKILL.md              (7549B)
INSTALL-LATEST.md     (5482B, frontmatter name: install-memu-latest)
```

`find -name SKILL.md` 全仓只命中 1 份（根级 `SKILL.md`）；但按「frontmatter 含 `name`/`description`」的判据，`INSTALL-LATEST.md` 是**第二份 skill 描述符**。

**`02docsdefine` D12 边界写「SKILL 是『可按需加载的流程』；AGENTS 是『常驻的约束』」**——本仓提供了最难判的一例：一份 skill 描述符**不叫 SKILL.md**。

### 3.3 根级 dotdir 只有 `.github`

无 `.agents/`、无 `.claude/`、无 `.cursor/`。但 **skill 确实存在**（根级）。→ 「有 skill」与「有工具目录」在本样本里**不相关**。

## 4. 与既有结论的冲突（反证）

| 既有结论 | 本轮实测 | 判定 |
|---|---|---|
| D05 边界：`INSTALL-LATEST` 属「流程与上手」，是 README 的最短路径切片 | `sources/repos/memU/INSTALL-LATEST.md` 首行 `---`，frontmatter `name: install-memu-latest` + `description: …Use when the user wants…` | **需重判**：在本仓它是 **skill 描述符**，不是上手文档。D05 的边界不足以覆盖 |
| D12 位置：「`skills\<name>\SKILL.md`（也可在包内）；memU 直接放根级」 | 根级确有 `SKILL.md`；**另有**根级 `INSTALL-LATEST.md` 也是 skill 描述符 | **需补**：「文件名不必然是 `SKILL.md`；判据是 frontmatter」 |
| D02 `CHANGELOG` 形态「单文件（+目录变体）」 | 本仓是**生成式**（Release Please 风格） | 形态清单需补「生成式」 |
| `sources/repos/index.csv` 关键词 `memory-cli;root-skill-md` | 一致 | 一致 |

## 5. 空白与未取证

- **未读** `AGENTS.md` 全文（只取首行 + 次节标题）、`SKILL.md` 与 `INSTALL-LATEST.md` 的 frontmatter 之后正文。
- **未确认** `docs/` 目录结构（顶层存在但未展开）。
- **未验证** 这两个根级 skill 描述符由什么加载器读取（仓内无 `.agents/`/`.claude/`）。
- **未核对** `CHANGELOG.md` 是否由 CI 自动提交。
- 以上均属「在本次检索范围内未查」。
