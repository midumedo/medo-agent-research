# MinerU：当前脚本使用的接口与结果

维护 [mineru_backend.py](pdf2md/scripts/mineru_backend.py) 或排查转换结果时读。服务端限制和参数以 [官方文档](https://mineru.net/apiManage/docs) 为准；连接失败看 [批次续取与网络诊断](pdf2md/references/mineru-network.md)。

## 上传与查询

1. `POST /api/v4/file-urls/batch` 申请上传地址，脚本每批最多 50 个文件。
2. 请求 `files` 与返回 `file_urls` 按顺序对应；逐个 PUT 本地 PDF，不额外设置 `Content-Type`。
3. `GET /api/v4/extract-results/batch/{batch_id}` 查询；只为 `done` 下载 `full_zip_url`，`failed` 报告 `err_msg`。

JSON API 使用 `MINERU_APIKEY` 作为 Bearer Token；上传和结果下载使用服务端给出的签名地址。日志和材料登记中不保留凭据或签名 URL。

| 参数 | 当前发送方式 |
|---|---|
| `model_version` | 默认 `vlm`，也可选 `pipeline` |
| `language` | 来自 `--lang`，默认 `ch`，英文论文用 `en` |
| `enable_formula / enable_table` | 默认开启，可由对应 `--no-*` 参数关闭 |
| `files[].name / data_id` | 原文件名及本次任务标识 |
| `files[].is_ocr` | 来自 `--ocr`，默认 false，由云端执行 |

结果优先按 `data_id` 匹配，缺失时按 `file_name`。轮询等待的是本次预期文件全部结束，不能把服务端返回的部分条目当作整批。API 支持的其他格式、页范围或回调，不代表当前 CLI 已提供。

## ZIP 如何变成本地材料

- 优先取 `full.md`；没有时接受 ZIP 中唯一的 Markdown，多份则报错。正文沿用服务端结果，不用 Content List 重拼。
- V1 `*_content_list.json` 的 `type / img_path / caption` 提供图片关系；V2 `type + content` 仅补足尚未关联的图片。
- 类型对应 `image→fig`、`chart→chart`、`table→table`、有明确图片路径的公式→`eq`；无法确认归属的图片为 `img`。图注只用于编号，不覆盖类型。
- 全部内容图片保留，包括正文没有引用的裁图；图号重复时加后缀，同一路径只命名一次。无路径公式不足以证明其余孤图都是公式。
- 图片写入平铺 `assets/`，实际 Markdown/HTML 图片引用改为 `../assets/...`；普通路径文字和代码示例不改。正文中的 HTML 表格和公式仍保留原表示。
- `layout.json` 或 Middle JSON 只读取 `_version_name`；没有版本标记时登记请求档位。ZIP 当前不落盘，也没有重放缓存或永久页码映射。

## 结果结构依据

测试使用 [真实 V1 字段样本](tests/fixtures/content_list.sample.json) 中的类型、图注和路径。样本经过截断，来源在 `_source`。测试容器是合成 ZIP，不是完整原始回包。

V2 公式路径依据版本固定的 [输出协议](https://github.com/opendatalab/MinerU/blob/0dfc9460cd9ab693b9af60ae3fbffd7bc111b062/docs/en/reference/output_files.md) 与 [输出源码](https://github.com/opendatalab/MinerU/blob/0dfc9460cd9ab693b9af60ae3fbffd7bc111b062/mineru/backend/vlm/vlm_middle_json_mkcontent.py)；V2 测试数据为合成条目。
