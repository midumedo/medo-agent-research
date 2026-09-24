# samples · 转换结果的格式样本

用来回答「MinerU 到底返回什么字段」，不必重复跑 API 去读。

## content_list.sample.json

不是原始 dump，而是**字段字典 + 每类一条代表样例 + 读取步骤**：原始 `*_content_list.json` 有 206 条、198 KB，其中 `header`/`page_number`/`ref_text` 占了大半，全量存下只为查字段名并不划算。现在 6 KB，信息更密：

- `field_map`：十种 `type` 各自的完整键列表
- `examples`：每种 `type` 一条真实样例（长值截断到 180 字符）
- `_read`：从解包到取图号的四步
- `_source`：取自哪篇、哪个批次、哪个模型档位
- `_consumed_by`：这些字段谁在用（`convert.py` 的 `parse_visual()` / `name_map()`）

**已在本文件上核对过、也踩过坑的事实**：

- 图注字段**按类型分开**：`image` 用 `image_caption`、`chart` 用 `chart_caption`、`table` 用 `table_caption`。早期代码把 chart 也指向 `image_caption`，于是 chart 图注恒为空——样例保留一份的作用就在这。
- 图注原文夹带 `<sup>`/`<sub>` 标记（`Wit<sup>h</sup>out`），消费前要剥标签。
- 结果 zip 里同时有 `*_content_list.json`（V1，本项目只用这个）与 `*_content_list_v2.json`（按页分组）。
- 正文里偶发控制字节（公式处的 `\x00`），已由 `sanitize_text()` 在写盘前剥掉。

## 为什么不把每篇的都存下来

它是转换的**中间产物**：正文已进 `md/`，图注在 md 里紧贴图片引用，图号在文件名里。留一份是为核对字段名，留二十七份只是把同一结构复制二十七遍。
