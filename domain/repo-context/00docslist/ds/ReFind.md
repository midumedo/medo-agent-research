# ReFind · 根目录文档实测

> 快照 `a80175ca0eeb` · 取证 2026-09-25 · 来源 `sources/repos/ReFind/`
> 状态：verified ｜ 覆盖范围：仓库根目录直接子文件 + `docs/`

## 1. 根目录清单一览（1 份，本样本最少）

| 文件 | 字节 | kind | 角色(D) | 一句话 |
|---|---|---|---|---|
| `README.md` | 7225 | facade | D01 | 首行 `# ReFind`；次行是 badge（Agent Memory Leaderboard 排名 + arXiv 链接） |

**没有的**：`AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、`CHANGELOG.md`、`CONTRIBUTING.md`、`SECURITY.md`、`CODE_OF_CONDUCT.md`、`LICENSE`（根目录）、任何 `SKILL.md`。

## 2. 逐文件分析

### 2.1 `README.md`（7225 字节）—— 唯一一份根级文档

首两行：

```
# ReFind
[![Agent Memory Leaderboard — Academic Textual #2](…)](…)
[![arXiv](https://img.shields.io/badge/arXiv-2608.12888-b31b1b.svg)](https://arxiv.org/abs/2608.12888)
```

**它的定位**：这是一份**带排名的论文级项目 README**——第二位是**榜单成绩**，第三位是 **arXiv 编号**。文档的目的是**证明效果**而不是**帮助协作**。

### 2.2 根目录只有 1 份文档意味着什么

- **协作面为零**：没有 CONTRIBUTING 就**没有外部贡献流程**；没有 SECURITY 就**没有漏洞披露渠道**；没有 LICENSE **就没有授权声明**（根目录实测无 `LICENSE` 文件——本样本 17 个有 checkout 的仓里，ReFind 与 `MemoryBear`、`MemOS` 三家根目录无 LICENSE）。
- **agent 面为零**：无任何指令文件、无 skill。

这与 `sources/repos/index.csv` 对该仓的关键词 `no-read-tool;no-skill-artifacts` 一致。

**判据**：本仓是「**代码 + 论文**」形态，不是「**产品 + 社区**」形态。研究结论里任何「仓库文档规范」的建议，对本仓都是**不适用**的——它不需要协作面文档，因为它的交付物是论文成绩。

### 2.3 `docs/` 只有 2 份，且都是**学术交付件**

```
docs/METHOD_CARD.md   (4KB)
docs/SUBMISSION.md    (2KB)
```

由文件名与所在目录（`docs/` 而非 `docs/design/` 或 `docs/adr/`）判断，这两份服务于**评测提交**（leaderboard submission），不是产品文档或设计记录。

→ **`docs/` 的语义随仓而变**：在 `Tianshu-harness` 是「受控类型文档库」，在 `ReFind` 是「评测提交材料」。任何「`docs/` 里放什么」的规则都必须带上仓库类型。

## 3. Agent 面（vibe coding 相关文件管理）

### 3.1 指令分级：**无**

### 3.2 Skills：**0 份**（`find -name SKILL.md` 零命中）

### 3.3 根级 dotdir：**0 个**（`find -maxdepth 1 -type d -name '.*'` 零命中）

**这是 17 个有 checkout 的仓里唯一一个连 `.github/` 都没有的仓。** 对照：`MemoryBear` 有 `.github/`（1 个），`ReFind` 0 个。

→ 「仓库有 `.github/`」也不是普遍事实。

顶层目录：`ReFind`（疑为源码目录）、`app`、`docs`、`scripts`、`tests`。

## 4. 与既有结论的冲突（反证）

| 既有结论 | 本轮实测 | 判定 |
|---|---|---|
| D01 `README.md`「仓库的第一入口，对外介绍项目**是什么、能干什么、怎么跑起来**」 | 本仓 README 的第二个元素是**榜单排名**，第三个是 arXiv 链接 | **边界需补一类受众**：论文/榜单型 README 的首要目的是**证明效果**，与「怎么跑起来」并列存在 |
| D03/D04 把 CONTRIBUTING/SECURITY 记为 `●`（实证，多家命中） | 本仓两者皆无 | 不冲突（实证 ≠ 普遍），但**任何「X 是标配」的措辞都应避免** |
| `index.csv` 关键词 `no-read-tool;no-skill-artifacts` | `find` 零命中 skill；无任何 agent 入口 | 一致 |

## 5. 空白与未取证

- **未读** `README.md` 正文（只取前 3 行）；未读 `docs/METHOD_CARD.md`、`docs/SUBMISSION.md`。
- **未确认** `ReFind/` 子目录（与仓同名的目录）的内容与作用。
- **未核对** 根目录是否真的没有 `LICENSE`（`find` 未在 `index.csv` 收录范围内覆盖全部非 md 文件；本阶段收录范围是 `*.md` + 治理型非 md，故**未系统扫过所有非 md 文件**）。
- **未验证** arXiv 编号对应的是否就是本仓。
- 以上均属「在本次检索范围内未查」。
