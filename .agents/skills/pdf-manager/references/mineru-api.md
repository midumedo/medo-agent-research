# MinerU 常用接口与结果处理

本文是本 skill 的操作与实现摘要，用于调整转换参数、排查结果或维护 [mineru_backend.py](../scripts/mineru_backend.py)。接口关键字段核对日期：2026-11-02。

- **完整接口资料**：[官方文档本地副本](minerU.api.md)，查完整参数、错误码、语言列表和其他接口。本副本包含导语与汇总，不保证与源站实时同步。
- **网络故障**：[连接诊断与批次续取](mineru-network.md)，区分失败阶段、自动回退和实测结论。
- **结果结构**：本文后半段与 [真实字段样本](samples/content_list.sample.json)，说明本 skill 怎样消费 ZIP；API 参数表不能代替结果结构证据。

接口有疑点时，核对 [官方源站](https://mineru.net/apiManage/docs) 的对应具体接口，而非套用总表或其他接口的参数。以下明确区分官方约定与本 skill 的选择；修改实现时同步维护摘要，不把实现选择写成服务端限制。

## 精准解析上传路径

凭据为 `MINERU_APIKEY`，JSON API 请求发送 `Authorization: Bearer <token>`。不要把 Token 或签名上传 URL 写进参考资料、索引或结果登记块。

1. `POST /api/v4/file-urls/batch` 申请上传地址。
2. 按 `data.file_urls` 与请求 `files` 的顺序一一对应地 PUT 本地 PDF。PUT 不附加 `Content-Type`；上传完成后服务端自动开始解析，不再调用提交任务接口。
3. `GET /api/v4/extract-results/batch/{batch_id}` 查询结果。
4. 仅对 `state=done` 的条目下载 `full_zip_url`；逐篇报告失败或超时。

官方“本地文件批量上传解析”说明单次最多 50 个链接、上传链接有效期 24 小时，单文件不超过 200 MB、200 页。本 skill 按 50 个分批，超限交由服务端明确报错，不截断 PDF。24 小时指上传链接，不能据此推断结果 ZIP 链接的寿命。

本地副本的模式总表写批量 200 个，具体接口写 50 个；保留原文差异，当前实现采用具体接口值。轻量接口的概述与错误示例也有页数差异，本 skill 不调用该接口，不用这些数值定义当前行为。

### 请求中实际使用的字段

| 位置 | 字段 | 官方约定与本 skill 选择 |
|---|---|---|
| 全局 | `model_version` | 官方副本默认 `pipeline`；本 skill 显式默认 `vlm`，CLI 可选 `pipeline` |
| 全局 | `language` | 发送 `--lang` 的值；脚本默认 `ch`，英文可用 `en` |
| 全局 | `enable_formula`、`enable_table` | 两种模型均可传入，脚本默认开启；`vlm` 的公式开关只影响行内公式，行间公式仍识别 |
| 每个 `files` 条目 | `name` | 带 `.pdf` 后缀，服务端返回文件名用于匹配 |
| 每个 `files` 条目 | `data_id` | 自定义任务标识；只在响应确实回传时用于匹配 |
| 每个 `files` 条目 | `is_ocr` | 官方说明 `pipeline`、`vlm` 有效；本 skill 由 `--ocr` 控制，默认 false |

官方副本将这两个文件级参数写成 `file.is_ocr`、`file.page_ranges`，对应请求 JSON 的 `files[]` 条目。本 skill 尚未暴露页范围、回调或额外格式等选项；不要因官方 API 支持就假定 CLI 也支持。这里的 OCR 由云端执行。

### 完成判断

查询响应的业务成功由 `code=0` 表示。逐篇状态位于 `data.extract_result`；只有本次预期文件全部返回且分别进入 `done / failed` 才结束正常轮询。不能把“已经返回的条目全结束”误当作“整批文件全返回”。

`file_name` 是文档明确列出的结果匹配字段；`data_id` 回传可用于优先匹配，但不能成为唯一依赖。`done` 读取 `full_zip_url`，`failed` 报告 `err_msg`。查询中断、等待超时或结果下载失败时保留 `batch_id`，用原文件及原文件名运行 `convert --batch-id <批次>`；这是重新查询并整包下载，不是字节级断点续传。`--timeout` 控制轮询等待，不能作为整个命令的总时限。

凭据错误、权限错误、参数错误和每日任务上限不循环重试。网络或服务临时故障须报告阶段与错误；不能把失败当成已有转换件。上传签名 URL 的失败响应也应呈现简短错误信息，避免无条件重传整批。

结果 CDN 的连接回退范围、重试上限和失败后的操作见 [连接诊断与批次续取](mineru-network.md)。API 拒绝、文件上传失败和结果下载失败应分别处理，不能统称为 VPN 问题。

## ZIP 的消费方式

云端通常使用 `full.md`、`layout.json`、`*_content_list.json` 与 `images/`。实际按 ZIP 成员识别这些文件，允许有外层目录；V2 是可选补充，缺少它不使转换失败。

| 内容 | 消费方式 |
|---|---|
| `full.md` | 优先使用；缺失时接受 ZIP 中唯一的 Markdown，多份则报错。不从 Content List 重组正文或重复追加图注 |
| V1 `*_content_list.json` | 扁平条目；使用 `type / img_path / 各类 caption` 建立主要关系 |
| V2 `*_content_list_v2.json` | 按页组织的 `type + content`；仅补足 V1 尚未关联的图片 |
| `layout.json` / Middle JSON | 当前读取 `_version_name` 标记解析器版本；缺失时用请求档位，不把 `vlm` 等档位当服务端版本 |
| `images/` | 完整保留内容图片，即使正文以 HTML 表格或 LaTeX 表达而没有引用裁图 |

### 分类与命名

| 原始类型 | 主要字段 | 本地分类 |
|---|---|---|
| `image` | `img_path`、`image_caption` | `fig` |
| `chart` | `img_path`、`chart_caption` | `chart` |
| `table` | `img_path`、`table_caption`、HTML `table_body` | `table` |
| 明确关联图片的 `equation` / V2 `equation_interline` | V1 图片路径或 V2 `content.image_source.path` | `eq` |
| 存在字节但没有可靠类型关联 | ZIP 中的内容图片 | `img` |

类型决定分类；图注只用于提取编号。`chart_caption` 即使写着 `Figure 4`，分类仍为 `chart`。有编号使用原编号，无编号使用同类型顺序号；一个图号对应多个图片时添加后缀，如 `fig1-2`。同一路径只命名一次，重复引用复用该结果。

V1 中无 `img_path` 的公式条目不足以证明剩余图片全是公式；先尝试 V2 的明确路径，仍不能对应时使用 `img`。不以块数量或全篇类型集合猜测逐图片归属。

图片保存至平铺 `assets/`，MD 中已有 Markdown、HTML 图片及引用式链接改为 `../assets/...`；带空格等字符的路径正确编码。映射仅在本次转换中使用，不生成每篇 manifest、页码映射或永久关联表。文本表格与裁图分别保存，正文仍保留服务端原有的文本表示。

转换、改名与完整性检查共用 `scripts/pdf_markdown.py` 识别实际链接；正文中的普通路径文字、围栏代码和行内代码保持原样，不当作资源引用。空正文不能因为补上登记块就成为成功转换。写入前检查资产前缀是否被另一份资料占用，避免同一来源身份的不同文件互相覆盖图片。

## 可复用证据

[content_list.sample.json](samples/content_list.sample.json) 是一次真实云端 V1 结果的字段字典与代表条目，来源标识和批次保存在 `_source` 中。它经过压缩和长值截断，不是可直接当作完整回包使用的 dump；其中没有公式条目，也不覆盖所有解析器版本。

样本中的 `_read`、`_consumed_by` 保留采集时的旧脚本说明；当前 V2 补充策略与入口以本参考和 skill 内脚本为准。离线测试读取样本中的真实类型、图注和路径字段，将其放入合成 ZIP 验证消费逻辑，不把合成容器宣称为原始回包。

V2 的公式路径补充还依据 MinerU 3.4.4 的 [输出协议说明](https://github.com/opendatalab/MinerU/blob/0dfc9460cd9ab693b9af60ae3fbffd7bc111b062/docs/en/reference/output_files.md) 与 [VLM 内容输出源码](https://github.com/opendatalab/MinerU/blob/0dfc9460cd9ab693b9af60ae3fbffd7bc111b062/mineru/backend/vlm/vlm_middle_json_mkcontent.py)。测试里自行构造的 V2 条目只能标为合成测试数据，不能称为另一次真实回包。

API 契约不证明识别内容准确；字节完整提取也不等于原 PDF 已经视觉核验。
