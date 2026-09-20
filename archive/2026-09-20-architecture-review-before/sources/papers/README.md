# papers/

《Memory 与上下文工程》教材的一手资料库。PDF 下载后解析成 Markdown 存本地，分析直接在文件上做，不联网现查。

## 目录

| 路径 | 内容 |
|---|---|
| `surveys/` | 已解析的综述，每篇头部带导航卡 |
| `pdf/` | 原始 PDF |
| `meta.json` | 标题 / 作者 / 日期 / 摘要 |
| `nav.json` | 每篇的导航卡数据（改这里 → 重跑解析即生效） |
| `_scripts/` | 下载与解析脚本 |
| `logs/` | 运行日志 |

## 三条命令

```
# 1. 加编号到 watchlist.txt，然后下载
<python> _scripts\download_arxiv.py --all

# 2. 解析为 Markdown（默认输出到 surveys/）
C:\Users\37071\.workbuddy\binaries\python\envs\default\Scripts\python.exe _scripts\pdf2md.py

# 3. 加了新分类时
... pdf2md.py --out engineering   # 输出到 papers/engineering/
```

解析用 `pymupdf4llm`，装在隔离 venv，不污染系统环境。

## 下一步

看 [surveys/README.md](surveys/README.md)。它按渐进披露组织：读完第 0 层就能走，需要更多再往下。
