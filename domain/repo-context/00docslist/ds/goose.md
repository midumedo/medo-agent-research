# goose · 根目录文档实测

> 快照 `61830521ad31` · 取证 2026-09-25 · 来源 `sources/repos/goose/`
> 状态：verified ｜ 覆盖范围：仓库根目录直接子文件 + `documentation/` 二级 + copilot/llms 入口

## 1. 根目录清单一览（16 份，本样本最多）

| 文件 | 字节 | kind | 角色(D) | 一句话 |
|---|---|---|---|---|
| `AGENTS.md` | 6581 | agent-entry | D09 | 首行 `# AGENTS Instructions`，次节 `## Contribution Workflow` |
| `CLAUDE.md` | **11** | agent-entry | D10 | 全文单行 `@AGENTS.md`——**import 指针** |
| `README.md` | 3449 | facade | D01 | 极短门面（3.4KB，四行 tagline + logo） |
| `CONTRIBUTING.md` | 16647 | collab-rule | D03 | 明写「code is only one way to contribute」 |
| `CODE_OF_CONDUCT.md` | 8513 | collab-rule | D03 | **Contributor Covenant 3.0**（3.0，非 2.1） |
| `SECURITY.md` | 2551 | collab-rule | D04 | 首行是 `> [!CAUTION]`，说明 agent 在本机的权限风险 |
| `GOVERNANCE.md` | 10503 | collab-rule | — | 技术治理结构（「轻量治理模型」） |
| `MAINTAINERS.md` | 772 | collab-rule | — | 核心维护者名单 |
| `RELEASE.md` | 2378 | record | D05 | 发版流程（GitHub Actions + tag 触发） |
| `RELEASE_CHECKLIST.md` | 1046 | record | D05 | 发版人工测试清单 |
| `BUILDING_DOCKER.md` | 7273 | topic-manual | D36 | Docker 构建指南 |
| `BUILDING_LINUX.md` | 5678 | topic-manual | D36 | Linux 桌面构建指南 |
| `CUSTOM_DISTROS.md` | 28327 | topic-manual | D36 | 白标/定制发行版指南 |
| `I18N.md` | 6158 | topic-manual | D36 | 桌面端 i18n 基础设施 |
| `RISCV_SETUP.md` | 8342 | topic-manual | D36 | RISC-V 构建（含 `> [!WARNING]`） |
| `MERGE_FIXES.md` | 10620 | topic-manual | D36 | **临时工作稿**，自述「Delete this file before the branch merges」 |

## 2. 逐文件分析

### 2.1 `CLAUDE.md`（11 字节）—— 最省的一种别名策略

全文（无换行符结尾）：

```
@AGENTS.md
```

**与同类对比**：`deepseek-harness`/`Raven`/`mem0` 用**整份复制**（17–22KB ×2），`qwen-code` 用**散文指针**（350B），`MemOS` 用**互补分工**（1.2KB），`goose` 用**语言内建的 import 语法**（11B）。

`documentation/CLAUDE.md` 也是同一行 `@AGENTS.md` → 该策略**在两级一致套用**。

### 2.2 `SECURITY.md` 的首行

首行是 GitHub alert 语法 `> [!CAUTION]`，正文警告「goose is a developer agent with access to a variety of systems that perform actions on behalf of the user on their local machine」。

**与 `Tianshu-harness` 分工对照**：`deepseek-harness` 把「Agent 运行安全」单独拆成 `SAFETY.md`（D35），`goose` 把它**并进 `SECURITY.md`**（对外的漏洞上报政策文件）。→ 同一关切，两种归口，`02docsdefine` D04/D35 的边界说明应记录这种合并。

### 2.3 `MERGE_FIXES.md`（10620 字节）—— 反面样本

首行 `# Merge fixes for \`unroll-agent-loop\``，次行 `Working notes for repairing what the merges with \`origin/main\` lost. Delete this file before the branch merges.`

**它为什么值得记一条**：
- 文件**自己声明**它是临时的、合并前应删；
- 却**长期留在仓库根**，且已有 10.6KB；
- 打开仓库第一眼就会看到它（根目录、大写命名、与 README/AGENTS 同级）。

→ 这是「**过程性文档与常驻文档混在根目录**」的具体代价。任何「根目录只放常驻文档」的规则都必须有一条**过程稿的临时落点**，否则临时稿会占用最显眼的位置。（对照 `Tianshu-harness` 的解法：把工具运行时草稿区隔离到 `.rivet/plans/`、`.cursor/plans/`、`.zcode/plans/`。）

## 3. Agent 面（vibe coding 相关文件管理）

### 3.1 指令分级：根 + `documentation/`

```
AGENTS.md
CLAUDE.md                  → @AGENTS.md
documentation/AGENTS.md
documentation/CLAUDE.md    → @AGENTS.md
```

`documentation/` 子树同时有 `AGENTS.md` 与 `CLAUDE.md`，**且 `CLAUDE.md` 也是 `@AGENTS.md`**。

### 3.2 根级 dotdir 5 个

`.blox`（品牌/发布？）、`.cargo`、`.devcontainer`、`.github`、`.intersect`。无 `.agents/`、无 `.claude/`、无 `.cursor/`。

### 3.3 copilot 指令与 `llms.txt` 两个入口**都存在**

| 文件 | 位置 |
|---|---|
| `copilot-instructions.md` | `.github/copilot-instructions.md` |
| `llms.txt` | `documentation/static/llms.txt` |

**这条推翻了本阶段早期的一个假阴性**：会话开始时用 `grep` 目录检索搜 `llms.txt` / `copilot-instructions` 得到「未找到匹配」，实为检索方式错误（`grep` 目录检索不递归）。已写进 `README.md` 的「假阴性陷阱」。

**含义**：`llms.txt` 在本样本里**不是零命中**——它出现在 `goose`（`documentation/static/`）与 `mem0`（`docs/llms.txt`）。放在**文档站的静态目录**下，说明其受众是**站点抓取器/外部消费者**，而非仓内 agent。这与 `AGENTS.md`（仓内 agent）是两个不同受众。

### 3.4 Skills：只有 1 份

`evals/harbor/.agents/skills/compare-tasks` —— 本样本**最少**（对照 qwen-code 43、mem0 56）。goose 的 skill 机制在 `index.csv` 里记为 `skill-md-via-plugin`（经插件发布），仓内不囤积。

## 4. 与既有结论的冲突（反证）

| 既有结论 | 本轮实测 | 判定 |
|---|---|---|
| 早期假阴性：`llms.txt` / `copilot-instructions` 在本样本「未找到匹配」 | `sources/repos/goose/.github/copilot-instructions.md`、`sources/repos/goose/documentation/static/llms.txt`、`sources/repos/mem0/docs/llms.txt`、`sources/repos/cline/.github/copilot-instructions.md` 均存在 | **旧论断作废**。这是本轮方法级反证的来源 |
| D04 vs D35：SECURITY 是「漏洞上报政策」，SAFETY 是「Agent 行为安全边界」，二者不同 | 本仓把 agent 安全边界写在 `SECURITY.md` 内（首行 `> [!CAUTION]`） | **边界需补**「可合并」这一可能；不能断言两者必然分置 |
| D06 `CONTRIBUTORS` / `ACKNOWLEDGMENTS` 是「致谢名单」 | 本仓用 `MAINTAINERS.md`（维护者）——**职责不同的第四个名字** | **新增命名**，未覆盖 |

## 5. 空白与未取证

- **未读** `MERGE_FIXES.md` 正文（只取首 2 行）；未核它是否已被删除/仍在增长。
- **未读** `GOVERNANCE.md`、`CUSTOM_DISTROS.md`（28KB 最大）正文。
- **未核对** `.github/copilot-instructions.md` 与 `AGENTS.md` 的内容关系（是否重复）。
- **未验证** `documentation/static/llms.txt` 的生成方式（手工 vs 脚本）。
- **未确认** `.blox`、`.intersect` 两个 dotdir 的用途。
- 以上均属「在本次检索范围内未查」。
