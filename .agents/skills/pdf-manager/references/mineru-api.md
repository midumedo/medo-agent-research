# MinerU 接口与结果约定

用于维护 `scripts/mineru_backend.py` 或排查转换。核对日期：2026-11-02。接口依据为 [MinerU 官方 API 文档](https://mineru.net/apiManage/docs)；下述 ZIP 字段同时依据真实云端摘样和对应 MinerU 3.4.4 源码。在线文档、历史回包和请求的模型档位各自说明不同事实，不互相替代。

## 精准解析上传路径

凭据为 `MINERU_APIKEY`，JSON API 请求发送 `Authorization: Bearer <token>`。不要把 Token 或签名上传 URL 写进参考资料、索引或结果登记块。

1. `POST /api/v4/file-urls/batch` 申请上传地址。
2. 按 `data.file_urls` 与请求 `files` 的顺序一一对应地 PUT 本地 PDF。PUT 不附加 `Content-Type`；上传完成后服务端自动开始解析，不再调用提交任务接口。
3. `GET /api/v4/extract-results/batch/{batch_id}` 查询结果。
4. 仅对 `state=done` 的条目下载 `full_zip_url`；逐篇报告失败或超时。

一次申请最多 50 个上传链接，超过时分批。官方摘录的总表曾写 200 个，但具体上传接口写 50 个，本实现按具体接口限制。签名地址有效期 24 小时。单文件大小上限 200 MB、页数上限 200；超限按服务端错误明确报告，不静默截断 PDF。

### 请求中实际使用的字段

| 位置 | 字段 | 处理 |
|---|---|---|
| 全局 | `model_version` | 显式发送 `vlm`；可按任务选择 `pipeline` |
| 全局 | `language` | 命令行 `--lang` 的值须真正传入请求 |
| 全局 | `enable_formula`、`enable_table` | 默认开启，按所用模型的有效范围处理 |
| 每个 `files` 条目 | `name` | 带 `.pdf` 后缀，服务端返回文件名用于匹配 |
| 每个 `files` 条目 | `data_id` | 自定义任务标识；只在响应确实回传时用于匹配 |
| 每个 `files` 条目 | `is_ocr` | pipeline 的 OCR 设置；不能误当作本地 OCR 能力 |

在线 API 文档把批量上传的 `is_ocr`、`page_ranges` 放在每个文件条目中；历史文档摘录曾简化成全局字段。若继续扩展页范围，应以该接口的当前字段位置为准。`vlm` 下 `enable_formula` 的开关只影响行内公式识别，行间公式仍识别。

### 完成判断

查询响应的业务成功由 `code=0` 表示。逐篇状态位于 `data.extract_result`；只有本次预期文件全部返回且分别进入 `done / failed` 才结束正常轮询。不能把“已经返回的条目全结束”误当作“整批文件全返回”。

`file_name` 是文档明确列出的结果匹配字段；`data_id` 回传可用于优先匹配，但不能成为唯一依赖。`done` 读取 `full_zip_url`，`failed` 报告 `err_msg`；等待超时报告仍未完成的文件与 `batch_id`，允许继续查询而不重新提交。

凭据错误、权限错误、参数错误和每日任务上限不循环重试。网络或服务临时故障须报告阶段与错误；不能把失败当成已有转换件。上传签名 URL 的失败响应也应呈现简短错误信息，避免无条件重传整批。

### CDN 连接故障的局部回退

2026-11-02 的本机实测中，系统代理及 TUN 接管 DNS 后将 CDN 域名解析到 `198.18.0.x`。常规域名下载出现 TLS EOF；保持 VPN 开启、使用实时 DNS 返回的实际 CDN 地址并保留原域名 SNI/Host 时，多个节点都能正常完成 HTTPS 下载。

因此结果下载优先使用原有系统路径；仅 `https://cdn-mineru.openxlab.org.cn` 的连接、TLS 或传输异常触发回退：

1. 依次向 AliDNS、Cloudflare 的 HTTPS JSON DNS 接口查询该域名的 A 记录，只发送域名，不发送结果 URL、签名或 Token。
2. 每个解析器最多尝试两个不同的公网 IPv4 地址，过滤本地、保留与 fake-IP 地址；不持久化或硬编码这些地址。
3. 建立到实际地址的连接，TLS SNI 与 HTTP Host 仍是原 CDN 域名，使用系统默认可信证书和主机名校验。
4. 仍检查下载内容是 ZIP。HTTP 403 等服务器拒绝不走 DNS 回退；所有地址均失败时报告原批次供继续获取，不重新上传解析。

这不修改 VPN、系统代理、hosts 或证书配置，其他站点和 MinerU API 请求继续使用原有网络路径。实现依据为 Python 的 [默认 TLS 上下文与主机名校验](https://docs.python.org/3/library/ssl.html#ssl.create_default_context) 和 [Cloudflare JSON DNS 响应格式](https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-https/make-api-requests/dns-json/)。它解决的是已观察到的访问路径故障，不保证所有网络或 CDN 故障都能恢复。

## ZIP 的消费方式

云端通常使用 `full.md`、`layout.json`、`*_content_list.json` 与 `images/`。实际按 ZIP 成员识别这些文件，允许有外层目录；V2 是可选补充，缺少它不使转换失败。

| 内容 | 消费方式 |
|---|---|
| `full.md` | 正文唯一输入；不从 Content List 重组整篇正文，也不重复追加图注 |
| V1 `*_content_list.json` | 扁平条目；使用 `type / img_path / 各类 caption` 建立主要关系 |
| V2 `*_content_list_v2.json` | 按页组织的 `type + content`；仅补足 V1 尚未关联的图片 |
| `layout.json` / Middle JSON | 已有云端格式中的版本与 backend 字段；缺失时保留请求档位，不编造版本 |
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
