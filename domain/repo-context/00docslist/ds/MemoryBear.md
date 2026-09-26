# MemoryBear · 根目录文档实测

> 快照 `c32b937f1ed0` · 取证 2026-09-25 · 来源 `sources/repos/MemoryBear/`
> 状态：verified ｜ 覆盖范围：仓库根目录直接子文件
> **本仓是本样本里唯一「没有 agent 入口文件」的仓。**

## 1. 根目录清单一览（3 份，本样本最少）

| 文件 | 字节 | kind | 角色(D) | 一句话 |
|---|---|---|---|---|
| `README.md` | 21718 | facade | D01 | 英文门面（hero banner 开头） |
| `README_CN.md` | 20049 | facade | D01 | 中文门面。**下划线式 `_CN`** |
| `CONTRIBUTING.md` | 1738 | collab-rule | D03 | 1.7KB，中文正文（`感谢你对 MemoryBear 的关注！…`） |

**没有的**：`AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、`CHANGELOG.md`、`SECURITY.md`、`LICENSE`（根目录）、`CODE_OF_CONDUCT.md`。

## 2. 逐文件分析

### 2.1 唯一一家「无 agent 入口」

`sources/repos/index.csv` 对本仓的 `keywords` 记 `load-skill-tools;no-root-manifest;monorepo`；跨会话记忆里另有一条独立复核结论：**MemoryBear 有 0 个 `SKILL.md`，却有 `load_skill_tools`**。

本轮 `find` 独立复核：

- `find MemoryBear -name 'AGENTS.md' -o -name 'CLAUDE.md' -o -name 'GEMINI.md'` → **零命中**
- `find MemoryBear -name 'SKILL.md'` → **零命中**
- 根级 dotdir 只有 `.github/`

**这是一个重要反例**：它同时推翻了两个容易默认成立的假设——

1. **「AI 时代的仓都有 AGENTS.md」≠ 成立**。18 仓里有 1 仓（5.6%）完全没有。
2. **「有 skill 加载能力 ⇒ 有 SKILL.md 文件」≠ 成立**。本仓有加载工具、无 skill 文件——**能力与内容是两件事**（这条已记在跨会话记忆里，本轮独立复核一致）。

**判据固化**：判断一个仓「有没有接入 agent」，不能只看 `AGENTS.md`/`SKILL.md` 是否存在；存在性只能证明存在，缺失需要看它是不是**从别处配置**（如 `README` 内的说明、或 harness 侧配置）。

### 2.2 `CONTRIBUTING.md` 是**中文正文**

首行 `# Contributing to MemoryBear`（英文标题），次行 `感谢你对 MemoryBear 的关注！我们欢迎任何形式的贡献。`（中文正文）。

**类型与语言的错配**：标题英文、正文中文。对照 `ZCode/AGENTS.md`（全中文，含标题）、`Tianshu-harness/CODE_OF_CONDUCT.md`（中英同文件并存，各一段）。→ **语言不是文件级属性**，同一文件内可混排，且标题与正文可以不同语言。

### 2.3 两份 README 用**不同的** hero 图

`head -1` 实测：

- `README.md`：`<img width="2346" height="1310" alt="MemoryBear Hero Banner" src="…/2c0a3f72-…" />`
- `README_CN.md`：`<img width="2346" height="1310" alt="MemoryBear Hero Banner" src="…/77f3e31a-…" />`

**资源 ID 不同**（`2c0a3f72` vs `77f3e31a`）。→ 两份不是「同一份的翻译」，而是**各自维护**的两份文档（与 `EverOS` 的 61 字节差、`ZCode` 的 12% 差同型）。**语言变体不承诺内容对齐。**

## 3. Agent 面（vibe coding 相关文件管理）

### 3.1 指令分级：**无**

### 3.2 Skills：**0 份**

### 3.3 根级 dotdir：只有 `.github`

顶层目录（`find -maxdepth 1 -type d` 实测）：`.github`、`MemoryBear`、`api`、`assests`（**拼写如此，非 `assets`**）、`e2b-infra`、`gateway-service`、`identity-service`、`mem-knowledge`、`packages`、`sandbox`、`web`。

**这是一个 monorepo**（多个 service 并列），却**没有子树级 agent 指令**。→ 「monorepo ⇒ 需要分级 AGENTS.md」也不是必然；`mem0`（monorepo + 11 组对）与 `MemoryBear`（monorepo + 0 份）是两个端点。

**另注**：目录名 `assests` 是 `assets` 的拼写错误且已固化在仓库顶层——这类**顶层命名漂移**会直接影响任何按名字导航的 agent。

## 4. 与既有结论的冲突（反证）

| 既有结论 | 本轮实测 | 判定 |
|---|---|---|
| 隐含默认：「样本仓都有 agent 入口」 | 本仓 0 份 `AGENTS.md`/`CLAUDE.md`/`GEMINI.md` | **反例成立**。任何「某某命名已全行业收敛」的结论都必须排除本仓 |
| `02docsdefine` D37/D38（`MEMORY.md`/`USER.md`）：样本零命中，属草案 | 本仓根目录亦无 | 一致 |
| 跨会话记忆：「MemoryBear 0 个 SKILL.md 却有 load_skill_tools」 | `find -name SKILL.md` 零命中 | **一致**（独立复核通过） |
| `index.csv` 关键词 `no-root-manifest` | 根目录无 `package.json`/`pyproject.toml` | 一致 |

## 5. 空白与未取证

- **未读** `README.md`/`README_CN.md` 正文（21KB / 20KB，只取首行）。
- **未核对** `CONTRIBUTING.md` 全文（1.7KB，只取前 2 行）。
- **未验证** `load_skill_tools` 的实现在哪个包、读什么路径（本仓无 `SKILL.md`，加载目标不明）。
- **未展开** 各 service 子目录，无法排除「子树里另有 `AGENTS.md`」的可能（`find` 是整树搜索且零命中，但**未打印检索深度与文件数**，见 `README.md` 的 `absent` 纪律）。
- 以上均属「在本次检索范围内未查」。
