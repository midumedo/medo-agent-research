# claude-code · 根目录文档实测（absent）

> 快照 —（无）· 取证 2026-09-25 · 来源 `sources/repos/claude-code/`（**不存在**）
> 状态：**absent** ｜ 覆盖范围：无

## 1. 根目录清单一览

**无**。本仓在 `sources/repos/` 下**没有本地 checkout**，因此没有可枚举的根目录文件。

## 2. 为什么是 absent 而不是「忘了收」

两条独立证据：

**(a) `sources/repos/index.csv` 的行本身**：

| 列 | 值 |
|---|---|
| `id` | `claude-code` |
| `repo` | `anthropic/claude-code` |
| `kind` | `harness` |
| `keywords` | `npm-wrapper-27k;prebuilt-binary;contract-only;no-impl-published;no-local-snapshot` |
| `completeness` | **`binary`** |
| `snapshot` | **空**（18 行里唯一没有 sha 的一行） |

**(b) 目录不存在（本轮实测）**：`ls -d sources/repos/claude-code` → `ls: cannot access 'claude-code': No such file or directory`（退出码 2，是本环境的**预期负结果**，不是执行失败）。

`keywords` 里的 `no-local-snapshot` 与 `snapshot` 列为空互相印证——**这是账本里被显式登记的状态，不是遗漏**。

## 3. 为什么仍然要在本阶段留一行

**因为它证明了一件事**：18 行的账本里，**只有 17 行能做根目录文件级实测**。

- 若 `ds/` 只写 17 份而不写这一份，下游会看到「17 个仓的明细」而**无法区分**「漏了一个」与「有一个不可测」。
- `index.csv` 里那一行 `status=absent` 也承担同样的职责：**缺什么必须显式，不能靠数数发现**。

这与 `STYLE.md` 的一条要求同源：*「覆盖范围、未读部分与未运行路径应可见，不能把『没有找到』说成『整个对象不存在』。」*

## 4. 本仓的可获得信息（不作根目录断言）

以下不是本阶段的实测结论，只是**账本已记录的状态**，供下游按需取用：

- **闭源形态**：`binary`（预编译二进制）+ `npm-wrapper-27k`（27KB 的 npm 包装层）。
- **契约可见、实现不可见**：`contract-only;no-impl-published`——接口/契约有公开描述，实现未发布。
- 因此本仓**无法参与**「根目录文档实测」这项研究：没有 checkout，就没有 `find`、没有行哈希、没有 `cmp`。

**待验证假设（不得引用）**：本仓若将来产出 checkout，其根目录形态是否与其它 harness 同型（`AGENTS.md` + `README.md`）——**本轮无法取证**。

## 5. 空白与未取证

- **未取证**：本仓的任何根目录文件（无 checkout）。
- **未取证**：`binary` 与 `source` / `source-partial` / `app-only` 之外是否还有其它 `completeness` 取值（本阶段只见到这 4 种）。
- **未验证**：`anthropic/claude-code` 上游是否确实不发布实现源码（`index.csv` 的关键词是**既有账本的记录**，本轮未独立复核）。
- 以上均属「在本次检索范围内未查」。
