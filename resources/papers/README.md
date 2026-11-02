# 论文库

这里保存外部论文原件、机器转换全文及定位它们的索引。清单在 [index.csv](index.csv)，本库约定在 [AGENTS.md](AGENTS.md)，历史在 [CHANGELOG.md](CHANGELOG.md)。下载、命名、转换、改名和检查使用 [pdf-manager skill](../../.agents/skills/pdf-manager/SKILL.md)。

## 一篇论文由什么组成

本库沿用 `<id>.<类型>.<简称>`，例如 `arxiv-2502.12110v11.Project.A-Mem`。`id` 包含来源编号及已知版本；名称供人和 Agent 辨认。

| 位置 | 内容 |
|---|---|
| `pdf/<名>.pdf` | PDF 原件 |
| `md/<名>.md` | 机器转换正文，顶部 front matter 登记摘要、关键词、来源与解析器 |
| `assets/<id>-*` | 平铺资产，分类为 `fig / chart / table / eq / img` |
| `index.csv` | 四列 `id, name, keywords, revised`；保留暂未下载的资料记录 |

PDF、MD、资产目录按本库 Git 规则不追踪；索引与文档随仓库保留。

## 找、读与补齐

先读索引的编号、名称、关键词和修订日筛选资料；需要判断一篇讲什么，再读 MD 顶部的摘要；论证与比数字时读正文并回到同名 PDF 核对。

在仓库根运行：

```text
python .agents/skills/pdf-manager/scripts/pdf_manager.py metadata 2504.19413v1 --root resources/papers
python .agents/skills/pdf-manager/scripts/pdf_manager.py check 2504.19413v1 --root resources/papers
```

新收录资料可先由脚本获取摘要，Agent 再决定类型与简称；本库已有名称默认保留。类型参考 `Survey / Bench / Project / Model / Method / Analysis`，可按实际材料扩展。转换使用 MinerU v4 精准解析，脚本只需 Python 标准库与 `MINERU_APIKEY`。

转换成功表示所选产物完成写出与引用检查，不表示 PDF 已视觉核验。缺失来源信息留空，不补猜；`check` 能检查 MD 引用的图片，不能仅凭正文检查未被引用的全部表格或公式裁图。
