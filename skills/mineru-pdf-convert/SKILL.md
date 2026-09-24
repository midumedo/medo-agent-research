---
name: mineru-pdf-convert
description: 把 sources/papers 里的论文 PDF 转成高保真 Markdown、JSON 与图片清单。需要保留表格、公式、多栏排版的论文正文，或现有 pymupdf4llm 转换不足以核对具体数字时使用。默认走 MinerU 云端 API（读环境变量 MINERU_APIKEY，每天有免费页数额度），本地 MinerU 服务是备选。项目级安装。触发词：MinerU 转换、高保真 PDF 解析、重转论文、表格公式核对、mineru_cloud、转换图片。
agent_created: true
---

# 用 MinerU 转换论文 PDF

## 走哪条路

| 需要什么 | 用什么 |
|---|---|
| 表格、公式、多栏正文保真；或要核对具体数字 | **MinerU**（本 skill） |
| 只要全文快速检索、看章节结构 | `_scripts/pdf2md.py`（`pymupdf4llm`，本地，快但对这些内容损失大） |

同一篇可以先跑快的拿全文，遇到关键表格或数字再用 MinerU 重转核对；`provenance.json` 保留最近一次转换记录，历史由 Git 追溯。

## 云端 API（默认）

不需要装模型。凭据是环境变量 **`MINERU_APIKEY`**（Windows 用户变量）。

```text
cd D:/workspace/memory/sources/papers
<python> _scripts/mineru_cloud.py mem0-building-production-ready-ai-agents-with-scalable-long-term-memory
<python> _scripts/mineru_cloud.py <词干A> <词干B>            # 一次批量提交，省每日任务数
<python> _scripts/mineru_cloud.py --model-version pipeline <词干>
<python> _scripts/mineru_cloud.py --force <词干>             # 覆盖已有转换
<python> _scripts/mineru_cloud.py --keep-images <词干>       # 连图片字节一起落盘
```

参数是**词干**（标题 slug）、`id`（`arxiv-2504.19413`）、arXiv 编号或标题，脚本都能查到；不给参数就转换 `pdf/` 下全部。

- `--model-version`：`vlm`（默认，最准）或 `pipeline`（快）。
- 多个词干**一次提交**：每天有任务数量上限，批量能省额度。
- 已存在的非空 `md/` 不会覆盖，除非 `--force`。
- 拿不到 `MINERU_APIKEY` 时脚本先回退读 Windows 用户环境变量（注册表），再失败才报错；当前终端看不到该变量时重开终端即可。

**限制**：单文件 ≤ 200 MB、≤ 200 页；账号每天 1000 页优先额度，超出仍可跑但优先级低。报错 `-60018` 是每日任务数到顶——改为批量提交或次日再跑。

**产物**：`md/<词干>.md`、`json/<词干>.json`（content_list，可定位表格与公式）、`assets/<词干>/manifest.json`；`provenance.json` 写入 `parser=mineru-cloud`、batch_id、`pdf_sha256`、`body_sha256`、`visual_verification=false`。

## 图片：默认只留清单

转换结果里的图片是**从已提交的 PDF 派生的**，所以脚本默认只写清单、不写字节：

- `assets/<词干>/manifest.json` 始终写入：每个图片的文件名、字节数、SHA256，外加从 content_list 抽出的**图注**（`figures`）。要找「Figure 3 说了什么」先查图注，不必先取回图片。
- md 里的 `![](images/x.jpg)` 会被改写成 `](../assets/<词干>/x.jpg)`，引用与 md 的位置解耦。
- 真的要看图：`--keep-images`。字节不进 Git（见 `.gitignore`），随时能按同一 API 与版本再生成，清单可用来验证重新生成的结果一致。

## 本地服务：已移除

曾有一个 `mineru_client.py` 对接本地 MinerU 服务，从未被使用过——它需要本地装模型（一串重依赖，与「工具链零第三方依赖」直接冲突），而云端 API 够用。2026-09-24 删除；确实需要本地解析时**再写**，不必预置。

## 版本：只在 zip 里，别处都没有

MinerU 的版本号**不在 API 响应里**——提交返回只有 `code/msg/trace_id/data{batch_id,file_urls}`，轮询返回只有 `data{batch_id,extract_result[{data_id,file_name,state,err_msg}]}`；`*_model.json` 里也没有。这三处都实测过。

它在 **zip 内 `layout.json`（MiddleJson）的末尾**：

    "_backend": "hybrid", "_effort": "medium", "_ocr_enable": false, "_version_name": "3.4.4"

所以解包后调 `mineru_version(zf)` 取 `_version_name` 与 `_backend`，写进 md 的 `parser: mineru-cloud 3.4.4`。**读不到就退回请求的档位**（`mineru-cloud vlm`），不编版本号。注意 `--model-version` 是我们**请求**的档位、`_backend` 是服务端**实际**用的，两者未必同名——以服务端回报的为准。

登记块因此**不再有 `converted_at`**：版本已唯一确定解析行为，"什么时候转的"由 git 承载。

## 收尾

转换完跑一次 `_scripts/build_index.py` 刷新 `index.json`，并在 `CHANGELOG.md` 追加一行。

## 边界

- 转换成功 **不等于** 已对 PDF 做视觉核验；引用具体数字前仍要回 `pdf/` 定位原文核对。
- 云端与本地都不会悄悄回退到别的解析器：失败就是失败，不会把未转换当成已转换。
- PDF 与 `provenance.json` 记录的 SHA256 不一致时脚本会停下来——那是先调查来源变化，不是覆盖。
- 词干永不改名；命名与索引规则见 `sources/papers/AGENTS.md`。
