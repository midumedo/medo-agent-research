# samples · 转换结果的格式样本

用来回答「MinerU 到底返回什么字段」，不必重复跑 API 去读。

## content_list.sample.json

取自 `mem0-building-production-ready-ai-agents-with-scalable-long-term-memory-v1` 的一次**真实**转换（2026-09-24，`model_version=vlm`，batch `70168b43-1ec1-401a-a60e-d29b0f4b57e9`），是结果 zip 里 `*_content_list.json`（Content List V1）的原文。

**已在本文件上逐字段核对过的事实**（不是推断）：

- 顶层是扁平的 `list`，共 206 条；`type` 分布为 `text` 94、`header` 43、`ref_text` 30、`page_number` 23、`code` 5、`image` 3、`page_footnote` 3、`table` 2、`chart` 2、`aside_text` 1。
- `image` 条目的键：`bbox, content, image_caption, image_footnote, img_path, page_idx, type`。图注字段就是 **`image_caption`**，类型是 `list[str]`；路径字段是 `img_path`。
- `table` 条目的键：`bbox, img_path, page_idx, table_body, table_caption, table_footnote, type`。
- 图注原文**夹带 `<sup>`/`<sub>` 标记**，例：`Wit<sup>h</sup>out pe<sup>r</sup>s<sup>i</sup>s<sup>t</sup>e<sup>nt</sup>`。消费前应剥标签（`mineru_cloud.clean_caption()` 负责这件事）。
- 结果 zip 里同时存在 `*_content_list.json`（V1，本文件）与 `*_content_list_v2.json`（V2，按页分组）。本项目只用 V1。

## 为什么不把每篇的 content_list 都存下来

它是转换的**中间产物**：图注已经用进了 `assets/` 的图片文件名与 md（图注文本紧贴图片引用），正文已经落进 `md/`。留一份样本是为了核对字段名，留二十七份只是把同一份结构复制二十七遍。
