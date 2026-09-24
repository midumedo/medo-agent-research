---
name: mineru-pdf-convert
description: 把 sources/papers 里的论文 PDF 转成高保真 Markdown 与图片。需要保留表格、公式、多栏排版的论文正文，或要核对具体数字时使用。走 MinerU 云端 API（读环境变量 MINERU_APIKEY，每天有免费页数额度）。项目级安装。触发词：MinerU 转换、高保真 PDF 解析、重转论文、表格公式核对、mineru_cloud、转换图片。
agent_created: true
---

# 用 MinerU 转换论文 PDF

## 走哪条路

只有一条：`_scripts/mineru_cloud.py`（MinerU 云端 API）。

早期的本地 `pymupdf4llm` 路径（`pdf2md.py`）已删除：它虽快，但对表格、公式、多栏损失大，而且会把 `pymupdf`/`pymupdf-layout`/`onnxruntime` 一串重依赖拖进环境，与「工具链零第三方依赖」冲突。

## 云端 API

不需要装模型。凭据是环境变量 **`MINERU_APIKEY`**（Windows 用户变量）。

```text
cd D:/workspace/memory/sources/papers
uv run python _scripts/mineru_cloud.py <文件名 | id | arXiv编号 | 标题>
uv run python _scripts/mineru_cloud.py <tokenA> <tokenB>       # 一次批量提交，省每日任务数
uv run python _scripts/mineru_cloud.py --model-version pipeline <token>
uv run python _scripts/mineru_cloud.py --force <token>         # 覆盖已有转换
uv run python _scripts/mineru_cloud.py --no-images <token>     # 只登记，不写图片字节
```

参数是**文件名**（`<id>.<名称>`）、`id`（`arxiv-2504.19413`）、arXiv 编号或标题，脚本都能查到；不给参数就转换 `pdf/` 下全部。

- `--model-version`：`vlm`（默认，最准）或 `pipeline`（快）。
- 多个 token **一次提交**：每天有任务数量上限，批量能省额度。
- 已存在的非空 `md/` 不会覆盖，除非 `--force`。
- 拿不到 `MINERU_APIKEY` 时脚本先回退读 Windows 用户环境变量（注册表），再失败才报错；当前终端看不到该变量时重开终端即可。

**限制**：单文件 ≤ 200 MB、≤ 200 页；账号每天 1000 页优先额度，超出仍可跑但优先级低。报错 `-60018` 是每日任务数到顶——改为批量提交或次日再跑。

**产物**：`md/<文件名>.md`（front matter 登记块 + 转换正文）与平铺的 `assets/<id>-<kind><n>.<ext>`。**不写 `json/`、不写 manifest、不写 provenance**：结构化输出只在转换时读一次用来抽图注，随即丢弃。

## 登记块只有一份

md 顶部是 YAML front matter（`stem` / `id` / `keywords` / `abstract` / `revised` / `source` / `parser`），其后**直接**是 MinerU 的正文。没有第二个头块——早先版本曾在 front matter 之后另写一段「解析器 / 转换时间 / 本地 PDF SHA256 / 图片」，它与 front matter 登记同一件事却已漂移（`parser` 版本号都不一致），2026-09-25 随本次收敛移除。

写盘由 `write_document()` 负责：**文本先构建、后开文件**。`open(path, "w")` 一调用就截断，而 `front_matter()` 靠读旧文件来保留 `abstract` / `revised` / `source`——顺序颠倒会把这三个字段洗成空（实测发生过）。因此 `--force` 重转是安全的：这三项会被保留。

登记块里**没有转换时间**：版本已唯一确定解析行为，"什么时候转的"由 git 承载。

## 图片怎么命名

MinerU 结果 zip 里的 `images/` 会被改写引用为 `../assets/<新文件名>`，让引用与 md 的位置解耦；每种图都有名字，平铺在 `assets/`：

| 图片来源 | 命名 |
|---|---|
| content_list 有 `img_path`、图注带编号 | `<id>-fig<N>` / `<id>-table<N>` / `<id>-chart<N>` |
| content_list 有 `img_path`、图注无编号 | `<id>-<kind><顺序号>` |
| 无 `img_path`，且这些条目全是 `equation` | `<id>-eq<N>` |
| 无 `img_path`，但类型混了 / content_list 完全没提 | `<id>-img<N>` |

没有 manifest：图注在 md 里紧贴图片引用，图号在文件名里，字节在 assets/。完整表格与判据见 `sources/papers/AGENTS.md`。

## 本地服务：已移除

曾有一个 `mineru_client.py` 对接本地 MinerU 服务，从未被使用过——它需要本地装模型（一串重依赖，与「工具链零第三方依赖」直接冲突），而云端 API 够用。2026-09-24 删除；确实需要本地解析时**再写**，不必预置。

## 版本：只在 zip 里，别处都没有

MinerU 的版本号**不在 API 响应里**——提交返回只有 `code/msg/trace_id/data{batch_id,file_urls}`，轮询返回只有 `data{batch_id,extract_result[{data_id,file_name,state,err_msg}]}`；`*_model.json` 里也没有。这三处都实测过。

它在 **zip 内 `layout.json`（MiddleJson）的末尾**：

    "_backend": "hybrid", "_effort": "medium", "_ocr_enable": false, "_version_name": "3.4.4"

所以解包后调 `mineru_version(zf)` 取 `_version_name` 与 `_backend`，写进 md 的 `parser: mineru-cloud 3.4.4`。**读不到就退回请求的档位**（`mineru-cloud vlm`），不编版本号。注意 `--model-version` 是我们**请求**的档位、`_backend` 是服务端**实际**用的，两者未必同名——以服务端回报的为准。

## 收尾

转换完跑一次 `_scripts/build_index.py` 刷新 `index.csv`，并在 `CHANGELOG.md` 追加一行。

## 边界

- 转换成功 **不等于** 已对 PDF 做视觉核验；引用具体数字前仍要回 `pdf/` 定位原文核对。
- 云端不会悄悄回退到别的解析器：失败就是失败，不会把未转换当成已转换。
- `id` 永不改；名称可变。命名与索引规则见 `sources/papers/AGENTS.md`。
