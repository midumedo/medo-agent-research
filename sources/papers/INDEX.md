# INDEX · 论文库数据在哪、怎么查

**清单不在这里。** 数据在 [index.json](index.json)，每篇论文一条记录；本页只说明字段与查询方式。规则见 [AGENTS.md](AGENTS.md)，历史见 [CHANGELOG.md](CHANGELOG.md)。

- 文件名是标题的 slug，用来路由 `pdf/`、`md/`、`json/`、`assets/`；`id`（`<registry>-<native-id>`）才是永久身份。
- 收录不等于核实；字段缺失为 `null`，不推测。

## 字段

| 组 | 字段 | 说明 |
|---|---|---|
| 身份 | `stem` | 文件名词干，路由键，冻结 |
| | `id` | `<registry>-<native-id>`，永久身份 |
| | `registry` `native_id` `alt_ids` | 登记处与编号 |
| 语义 | `title` `slug_year` `authors` | 标题取原文 |
| | `kinds` | 多值：survey / benchmark / framework / … |
| | `tags` | 多值自由标签 |
| | `note` | 给未来引用者的一句话提醒 |
| 定位 | `source_url` | 来源页面 |
| 状态 | `has_pdf` `has_md` `has_json` `has_assets` | 各表示形式是否齐备 |
| 溯源 | `version` `pdf_sha256` `parser` `converted_at` `retrieved_at` `visual_verification` | 版本与指纹 |
| | `added` | 入库日期 |

`kinds` 与 `tags` 在 SQL 视图里展开为 `paper_kinds(stem, kind)` 与 `paper_tags(stem, tag)`。

## 查

```text
<python> _scripts/index_query.py                              # 概览与缺口
<python> _scripts/index_query.py --sql "SELECT stem, id, version FROM papers WHERE has_json = 0"
<python> _scripts/index_query.py --sql "SELECT p.stem, p.title FROM papers p
                                        JOIN paper_kinds k ON p.stem = k.stem
                                        WHERE k.kind = 'benchmark' AND p.has_md = 1"
<python> _scripts/index_query.py --sql "SELECT stem, note FROM papers WHERE note != ''"
<python> _scripts/index_query.py --emit index.sql             # 导出可在外部 sqlite 载入的 .sql
```

SQL 是查询语言，JSON 是存储；不在版本库里放二进制 `.db`。

## 重建与校验

```text
<python> _scripts/build_index.py          # 从文件与 provenance 重建
<python> _scripts/build_index.py --check  # index.json 与文件不一致就报错
```

`kinds`、`tags`、`note` 是人工判断，重建时会从旧记录带回来，不会被覆盖。
