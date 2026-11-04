# pdf2md

把搜索发现的论文或已有 PDF 保存为本地全文，供深入阅读、原文核对和后续复用。

本目录包含完整源码与开发材料。[pdf2md/](pdf2md/SKILL.md) 是可直接复制安装的 skill；修改、验证均在本空间完成。

```text
pdf2md/
  SKILL.md                     使用入口
  agents/openai.yaml           展示与调用描述
  scripts/                     下载、转换、读取与资料维护
  references/                  按需读取的校对与网络说明
tests/                         本地行为验证及字段样本
pyrightconfig.json             本地类型检查
experience.md                  设计原则与反例
mineru-implementation.md        接口消费与结果处理
```

## 使用与安装

在本目录运行：

```text
python -B pdf2md/scripts/pdf2md.py --help
python -B pdf2md/scripts/pdf2md.py metadata "<本地 MD 或论文编号>"
uv run --script pdf2md/scripts/pdf_read.py "<PDF>" --pages 1-2
```

下载与转换脚本使用 Python 3.10+ 标准库；PDF 读取脚本声明自己的 PyMuPDF 依赖，由 uv 准备。转换所需凭据和命令用法见 [SKILL.md](pdf2md/SKILL.md)。

安装时复制完整的 `pdf2md/` 到目标 skills 目录，例如 `.agents/skills/pdf2md/`，调用名为 `$pdf2md`。本地研究文档、测试和类型配置留在开发空间。

## 本地维护

按改动范围运行相关测试；调整描述或整理文档时检查格式、链接与命令即可。

```text
python -B -m unittest discover -s tests -p test_download.py
npx pyright --project pyrightconfig.json --pythonpath "<实际解释器>"
```

`test_pdf_read.py` 及其类型检查需要能加载 PyMuPDF 的解释器。测试直接引用本空间的源码，不依赖已安装副本。

设计取舍见 [experience.md](experience.md)；修改接口或资产处理时查 [mineru-implementation.md](mineru-implementation.md)。
