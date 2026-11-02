# Tasks

- [x] Task 1: 合并四段草稿为唯一交付文件
  - [x] SubTask 1.1: 按 part1 → part2 → part3 → part4 顺序拼接
  - [x] SubTask 1.2: 写入 `resources/papers/单词本.md`（UTF-8）
- [x] Task 2: 逐条校验英文原句归属
  - [x] SubTask 2.1: 抽查含符号的原句（φ、α、π_θ、M_t^form、Pass^k）
  - [x] SubTask 2.2: 确认每条引句在其标注的文件中存在（118 个引句片段，0 缺失）
- [x] Task 3: 统计条目数
  - [x] SubTask 3.1: 术语 86 条（13/15/16/14/14/14）、句法 25 条、符号 30 行、读表 8 小节、冲突 9 条
- [x] Task 4: 清理临时目录
  - [x] SubTask 4.1: 删除 `.tmp_wordbook/`（spec.md、tasks.md、part1–part4、verify.ps1）
- [x] Task 5: 确认未改动其它文件

# Task Dependencies
- Task 2 depends on Task 1
- Task 3 depends on Task 1
- Task 4 depends on Task 1、Task 2
