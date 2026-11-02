# PDF→MD 标签噪声：诊断与处置计划

> 范围：`resources/papers` 中 MinerU v4 转换件。初稿只做分析与计划；2026-11-02 增补两次重转验证、一次替代抽取实验；同日收窄定案：**MinerU 为唯一底稿，PyMuPDF 只作字符真值**。2026-11-03 范围修正：目标从「修这一篇」改为「把修复能力做进 `pdf-manager` skill」，最终形态见 §10（实验产物只落在 `.rivet_scratch/`，未入库存档）。
> 样本：`arxiv-2504.19413v1.Project.Mem0.md`（重症），另抽查 LongMemEval、Memory Mechanism、Memory OS、Memory Workloads、Scientific Memory、MemoryArena，并做全库 27 篇盘点。

## 0. 结论

**推荐路线（2026-11-02 二次修订，2026-11-03 定交付形态）：MinerU 产物是唯一底稿；只把 PyMuPDF 纯文本当作字符真值，做同段词级替换。表格、公式、代码围栏、算法块、图片与图片路径一律原样不动。这套能力做进 `pdf-manager` skill，而不是修单篇——形态与改动清单见 §10。**

五条依据：

1. **重转已被证伪。** `vlm` 与 `pipeline` 产出同构噪声（表格外 `<sub>` 6837 / 6922，落点重合 91.4%），重转不修（§4）。
2. **本地工具只该补字符，不该补结构。** PyMuPDF 纯文本 5/5 命中原文、0 标签、0.047 s、离线纯 CPU（§8）。
3. **`pymupdf4llm` 降级为实验记录。** 它的价值在表格与标题结构，而本轮明确不修结构；引入它会带来第二套排版、第二套行号，反而扩大引用与 diff 风险。
4. **词级替换可逐行审阅。** 补丁只改同一段落内的词，不动换行；产出的 diff 按行可读（§9.3–§9.5）。
5. **规模可控。** 4,659 个受损词里 4,362（93.6%）满足形式条件、可自动修；真上标白名单 6 条保留（另 1 条形式损坏待确认）；297 个词（70 行）需要 AI 裁决，按每包 20 条约 15 包（§9.6）。

| 路线 | 预期收益 | 代价 |
|---|---|---|
| **skill 能力：体检默认开 + 修复默认关（推荐，§10）** | 任意新转换件写盘前就知道脏不脏、能自动修多少；93.6% 受损词可自动修；真上标不误伤；结构哈希不变 | 一个新模块 + 一个 reference + 一组测试；PyMuPDF 为运行时可选依赖 |
| 词级补丁的一次性脚本（§9） | 同上，但只服务当前一篇 | 无复用；规则散落在临时脚本里 |
| 两版合并且采用 `pymupdf4llm` 结构（已否决） | 结构更规整 | 行号与段落重排，diff 不可读；表格、公式需重建，引用需重核 |
| 重转（已否决） | 无 | 密度未变；`pipeline` 还把公式 103→131 段 |

**决策门槛**：`sub+sup` 残留 ≤50（6 条真上标白名单另计）、表格/公式/代码块/图片路径哈希 100% 不变、净改行数 ≤90（当前受影响 85 行）、5 处已知字符损坏全部经 PDF 逐字证实后修复。

**能力层门槛（§10）**：`convert` 默认只多一行体检输出；`audit` 只读；`repair` 不带 `--apply` 时 `md/` 的 SHA 与 mtime 不变；缺 PyMuPDF 时 `repair` 退出码 2 且给安装提示、`audit` 仍可用；回归语料三篇（Mem0 / MemoryArena / Memory Workloads）中后两篇改动为 0。

---

## 1. 现象量化

### 1.1 全库分布：一篇独占

对 `resources/papers/md/` 全部 27 篇按 `<sub>`/`<sup>` 计数（表格内单独统计）：

| 文件 | 类型 | 字符数 | `<sub>` | `<sup>` | 密度（个/千字） | 表格块 |
|---|---|---:|---:|---:|---:|---:|
| [Mem0](file:///d:/workspace/memory/resources/papers/md/arxiv-2504.19413v1.Project.Mem0.md) | Project | 160,453 | 6,837 | 873 | **48.05** | 2 |
| MemoryArena | Bench | 100,509 | 40 | 44 | 0.84 | 9 |
| Scientific Memory | Bench | 119,247 | 48 | 9 | 0.48 | 16 |
| LongMemEval | Bench | 103,830 | 4 | 17 | 0.20 | 13 |
| Memory Mechanism | Survey | 148,602 | 1 | 16 | 0.11 | 4 |
| Memory OS | Project | 40,478 | 3 | 0 | 0.07 | 4 |
| Memory Workloads | Analysis | 61,792 | 0 | 0 | 0 | 3 |
| 其余 20 篇 | — | 47k–472k | 0–4 | 0–94 | ≤0.26 | 2–26 |

全库合计 `<sub>` 6,956、`<sup>` 1,304。Mem0 一篇分别占 98.3% 与 67.0%。**把 Mem0 排除后，整个库的 `<sub>` 只有 119 个**，其中还包含真实下标与数学 fallback。

表格内计数（用 `<table>…</table>` 整体屏蔽后统计）：

| 范围 | `<sub>` 表内 | `<sup>` 表内 |
|---|---:|---:|
| Mem0 | 0 | 0 |
| 全库 27 篇 | 0 | 0 |

全库标签词表也很小：`td` 21,547、`sub` 6,956、`tr` 3,545、`sup` 1,304、`table` 268，另有 `<div class="mineru-algorithm">` 16 个、`<think>` 26 个、`<answer>` 15 个、`<plan>` 10 个、`<title>` 8 个等。这些非表格标签多是**正文内容**（提示词模板、JSON schema、算法块），不是噪声，见 §6。

### 1.2 Mem0 内部分层

| 区域 | 字符数 | `<sub>` | `<sup>` | 合计 | 占比 |
|---|---:|---:|---:|---:|---:|
| 正文段落（含标题） | 112,890 | 5,306 | 783 | 6,089 | 79.0% |
| 参考文献 | 33,401 | 1,269 | 31 | 1,300 | 16.9% |
| 图注/表注 | 6,611 | 262 | 59 | 321 | 4.2% |
| 表格 | 5,398 | 0 | 0 | 0 | 0% |
| 公式（`$…$` / `$$…$$`） | — | 0 | 0 | 0 | 0% |
| front matter | 2,153 | 0 | 0 | 0 | 0% |

- 85/379 行含标签；以空白切分的 10,321 个 token 中，**4,651 个（45.1%）token 内含标签**。
- 标签内容类型：`sub` 纯字母 5,137、混合 1,511、纯符号 189；`sup` 纯字母 837、纯数字 5、混合 23、纯符号 8。
- **1,166 个（15.1%）标签内部含空格**（如 `<sub>responses, ye</sub>`），这种跨词、跨标点的内容不可能是真实上下标格式。
- 103 段行内公式中，公式内部标签数 **0**；公式整体保持 LaTeX（`$\mathtt { M e m O } ^ { g }$`、`$\left( m _ { t - 1 } , m _ { t } \right)$`）。

按相邻字符的上下文分类：

| 上下文 | 正文 | 参考文献 | 图注 | 合计 | 占比 |
|---|---:|---:|---:|---:|---:|
| 词内（左邻字母、右邻字母） | 3,375 | 708 | 183 | 4,266 | 55.3% |
| 半边界（仅一侧邻字母） | 2,550 | 567 | 123 | 3,240 | 42.0% |
| 独立（两侧均非字母） | 164 | 25 | 15 | 204 | 2.6% |

「词内」是最可判定的噪声；「半边界」混入了真实的脚注/变体标记（如 `Mem0<sup>g</sup>`、`Neo4j<sup>1</sup>`）；「独立」应默认不动。

### 1.3 具体误判样本

| 位置 | 原文片段 | 判定 | 说明 |
|---|---|---|---|
| [L19](file:///d:/workspace/memory/resources/papers/md/arxiv-2504.19413v1.Project.Mem0.md#L19) | `Lar<sub>g</sub>e Lan<sub>g</sub>ua<sub>g</sub>e` | 噪声 | 去标签即得 Language；单词被切成 2–4 段 |
| L19 | `<sub>responses, ye</sub>t` | 噪声 | 标签跨词并包含逗号，跨度 14 字符 |
| L19 | `2<sup>6</sup>%` | 噪声 | 原文是 “26%”，模型把数字切成上标 |
| [L21](file:///d:/workspace/memory/resources/papers/md/arxiv-2504.19413v1.Project.Mem0.md#L21) | `<sup>h</sup>ttps://mem0.ai/researc<sup>h</sup>` | 噪声 | URL 也被切碎 |
| [L25](file:///d:/workspace/memory/resources/papers/md/arxiv-2504.19413v1.Project.Mem0.md#L25) | `Human memory is afoundation of intelligence` | 字符损坏 | 丢空格，去标签无法修复 |
| L25 | `AI <sub>s s</sub>t<sub>ems canno</sub>t` | 噪声 + 字符损坏 | 去标签得到 “AI s stems cannot”，仍有杂字母与空格 |
| [L28](file:///d:/workspace/memory/resources/papers/md/arxiv-2504.19413v1.Project.Mem0.md#L28) | 图注 `Wit<sup>h</sup>out pe<sup>r</sup>s<sup>i</sup>s<sup>t</sup>e<sup>nt</sup> …` | 噪声 | 图注同样被切碎 |
| [L44](file:///d:/workspace/memory/resources/papers/md/arxiv-2504.19413v1.Project.Mem0.md#L44) | 公式后紧跟 `<sub>, w</sub>h<sub>ere</sub>` | 噪声 | 公式本体正常，噪声贴在公式边界 |
| [L56](file:///d:/workspace/memory/resources/papers/md/arxiv-2504.19413v1.Project.Mem0.md#L56) | `## 2.2. Mem0<sup>g</sup>` | **真实上标** | Mem0 的图变体记号，必须保留 |
| [L74](file:///d:/workspace/memory/resources/papers/md/arxiv-2504.19413v1.Project.Mem0.md#L74) | `Neo4j<sup>1</sup>` | **真实脚注** | 数字上标是脚注，不能合并成 Neo4j1 |
| [L108](file:///d:/workspace/memory/resources/papers/md/arxiv-2504.19413v1.Project.Mem0.md#L108) | 13 行 × 160 单元格的 HTML 表格 | 结构 | 表内 0 个 `<sub>`/`<sup>` |
| [L132](file:///d:/workspace/memory/resources/papers/md/arxiv-2504.19413v1.Project.Mem0.md#L132) | 24 行 × 155 单元格的 HTML 表格 | 结构 | 表内 0 个 `<sub>`/`<sup>` |
| [L161](file:///d:/workspace/memory/resources/papers/md/arxiv-2504.19413v1.Project.Mem0.md#L161) | `Mem0 ra <sup>h</sup> construct<sup>i</sup>on com <sup>l</sup>etes` | 字符损坏 | PDF 第 14 页为 “graph construction completes”；**丢了 g、p 等字母** |
| [L167](file:///d:/workspace/memory/resources/papers/md/arxiv-2504.19413v1.Project.Mem0.md#L167) | 结论段 | 噪声 | 单行 226 个标签 |
| [L179](file:///d:/workspace/memory/resources/papers/md/arxiv-2504.19413v1.Project.Mem0.md#L179) | `A<sub>n</sub>th<sub>rop</sub>i<sub>c.</sub> M<sub>o</sub>d<sub>e</sub>l …` | 噪声 | 参考文献作者名被切碎 |
| [L185](file:///d:/workspace/memory/resources/papers/md/arxiv-2504.19413v1.Project.Mem0.md#L185) | `P<sub>ra</sub>t<sub>ee</sub>k Chhik<sub>ara,</sub>` | 噪声 | 作者名跨词切分 |
| [L373](file:///d:/workspace/memory/resources/papers/md/arxiv-2504.19413v1.Project.Mem0.md#L373) / [L377](file:///d:/workspace/memory/resources/papers/md/arxiv-2504.19413v1.Project.Mem0.md#L377) | ReadAgent / MemGPT 段落 | 噪声 | 行内 230 级标签；附录同样严重 |

反例（低噪声文件中的真实标签）：

- MemoryArena [L13](file:///d:/workspace/memory/resources/papers/md/arxiv-2602.16313v2.Bench.MemoryArena.md#L13)：作者单位标记 `Zexue He <sup>*</sup> <sup>1</sup>`，真实上标。
- Scientific Memory [L17](file:///d:/workspace/memory/resources/papers/md/arxiv-2607.16848.Bench.Scientific Memory.md#L17)：`St<sub>.</sub> P<sub>e</sub>t<sub>ers</sub>b<sub>urg</sub>`，同样是噪声，但密度低（0.48/千字），说明缺陷是同一机制的低频表现，而非 Mem0 独有。

### 1.4 中间产物与可追溯性

- `resources/papers/.rivet_scratch/` **存在但为空**（0 个条目）。
- `resources/papers` 下没有任何 `.zip` / `.json` 中间产物；转换完成后 ZIP 即被丢弃。
- [`parse_archive`](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/mineru_backend.py#L360-L453) 只把 `full.md` 读成 `body`；`content_list.json` / `content_list_v2.json` 仅用于图片分类，`layout.json` 仅用于读 `_version_name`，三者都不保留。
- 因此**事后无法用中间产物对照「解析器结构」与「后续转换」**。但代码路径本身已经排除后者：`body` 从 `full.md` 原样读出（[L377](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/mineru_backend.py#L377)），随后只做两件事——图片链接改写与去掉控制字符（[L439](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/mineru_backend.py#L439)）；[`write_conversion`](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/pdf_library.py#L359-L383) 只前置 front matter。**本仓库不可能生成 `<sub>`。**

---

## 2. 成因分层

### 2.1 不是 PDF 版式

用 PyMuPDF 读取 Mem0 PDF 第 1–3 页的字符级坐标：

- 每一行内所有字符的 `origin.y` **极差 0.00**；每行只有一种字号（如正文 9.89–10.06，标题 19.85）。
- 抽查的 36 行（3 页 × 12 行）全部如此；没有任何真正的基线偏移或字号切换。
- 第 1 页摘要文本层是连续的：“Large Language Models (LLMs) have demonstrated remarkable prowess in generating contextually coherent …” 是**单个 span**。

结论：PDF 里没有可被忠实转写的上下标版式。**标签不是版式识别结果。**

### 2.2 不是本仓库的转换阶段

见 §1.4：`body` 原样取自 MinerU 的 `full.md`，本仓库只改链接与去控制字符。标签必然存在于 MinerU 返回的 Markdown 里。

### 2.3 机制判断

现有证据指向 **MinerU v4 `vlm` 的 Markdown 生成/解码不稳定**，而不是某个确定性的版式特征：

- 标签落点任意：55.3% 在词内，42.0% 在词边界，2.6% 独立；15.1% 的标签内容自带空格或逗号。这些分布不符合任何真实排版规则。
- 同类 PDF 的其它 26 篇几乎干净（≤0.84/千字），说明这不是全库普遍的格式问题；但 2026-11-02 的重转实验进一步排除了「一次性失稳」这一解释（见本节末修订）。
- 标签与空格/字母损坏同时出现（`afoundation`、`se ara t e`、`ra h`、`ofering`、`eficien`），说明故障发生在「文本→Markdown token 序列」这一层，而不是字符定位层。

需要保留的限定：由于原始 ZIP 未留存，无法进一步区分「模型生成了标签 token」与「服务端后处理插入了标签」。但无论哪种，**都不是 PDF 版式，也不是本仓库代码**。

**2026-11-02 修订：上一段的「解码不稳定」判断已被重转实验推翻。** 同一 PDF 用 `vlm` 重转，正文与旧件等价；改用 `pipeline` 重转，噪声同样出现（`<sub>` 6922、落点重合 91.4%）。因此这是 **MinerU 对这份 PDF 的确定性缺陷**，跨后端稳定复现，与「一次解码轨迹的失稳」无关。可区分性只能到「MinerU 内部文本→Markdown 阶段」这一层，无法再细分。

### 2.4 哪些可判定，哪些本质有歧义

可判定（结构上就能判断）：

- 词内字母片段：左右都是字母，去标签后得到完整词。4,266 个（55.3%）。
- 标签内含空格/逗号且跨词：`<sub>responses, ye</sub>` 这类不可能是真实上下标。1,166 个。
- 标签内容为连字符/符号且去掉标签不改变字符：如 `<sub>-</sub>`，189 个 `sub` 纯符号中的大部分。

半可判定（需要词表或白名单）：

- 词首/词尾片段：`<sub>p</sub>rowess`、`generat<sub>ing</sub>` 可合并；但 `Mem0<sup>g</sup>`、`Neo4j<sup>1</sup>` 必须保留。二者在结构上同为「半边界」。
- 纯数字上标：可能是 `26%` 的噪声，也可能是脚注。Mem0 里 5 个纯数字 `sup`，其中 `Neo4j<sup>1</sup>` 真实，`2<sup>6</sup>%` 噪声。

本质有歧义（规则不应硬修）：

- 真实数学下标/上标（`$x_i$` 已走 LaTeX；但 MemoryArena [L586](file:///d:/workspace/memory/resources/papers/md/arxiv-2602.16313v2.Bench.MemoryArena.md#L586) 出现 `<sup>d+k</sup>`、`<sub>ε2</sub>` 这类 HTML 化数学）。
- 作者单位、脚注、变体记号。
- 提示词/schema 里的 `<think>`、`<title>`、`<integer from 1-10>`、`<key>:<value>` 等——它们本来就是尖括号内容。

### 2.5 补充发现：字符损坏不可由标签规则修复

在 PDF 中逐条检索、在 MD 中逐条对照：

| MD 片段 | PDF 原文 | PDF 位置 | 去标签后是否恢复 |
|---|---|---|---|
| `ra <sup>h</sup> construct<sup>i</sup>on com <sup>l</sup>etes` | graph construction completes | p.14 | 否，仍缺 g、p |
| `ofering`（由 `of<sub>er</sub>i<sub>ng</sub>` 去标签） | offering | p.1 | 否，仍少一个 f |
| `eficien…` | efficient | p.1 | 否，仍少一个 f |
| `afoundation` | a foundation | p.1 | 否，缺空格 |
| `se ara t e sessions` | separate sessions | p.2 | 否，字母间多空格 |

这决定了：**后处理最多把“可读性”恢复到 60–80%，无法把文本恢复为原文。** 要恢复原文，只能重转，或做 PDF 文本层对齐（成本更高、且 PDF 文本层本身也可能有读取顺序问题）。

---

## 3. 方案对比

| 路线 | 适用条件 | 代价 | 主要失效场景 | 结论 |
|---|---|---|---|---|
| A. 表格块之外归一化（HTML 感知） | 需要就地修，且标签遍布全文 | 需要块级扫描与屏蔽；要处理 `<div class="mineru-algorithm">`、代码块、提示词 | 若只按标签名处理 `sub/sup`，风险可控；若泛化到所有尖括号会毁掉提示词/schema | 技术上可行，但当前只服务 1 篇，不值得常驻 |
| B. 按上下文判定 `sub/sup` | 词内片段多、且有词表 | 需词典/词表；词边界规则需白名单 | 专名、术语、变体记号、脚注数字误判；总是被切碎的词永远进不了文档词表 | 可作为一次性修复；不能作为默认管线 |
| C. 换更稳的表示（LaTeX / Unicode / 标准 MD 表） | 表示层本身就是问题 | 表格转标准 MD 会丢失 `rowspan/colspan`；Unicode 下标破坏原文可检索性 | 本库表格大量合并单元格（Mem0 两张表都有 `rowspan/colspan`） | 表格保持 HTML；公式已 LaTeX；Unicode 方案收益极低，否决 |
| D. 重转 / 调 MinerU 参数 | 缺陷来自解析器，且源 PDF 可复现 | 1 次 API 调用；需核对新产物的表、公式、图片 | 新版本解析器与 3.4.4 行为不同；`pipeline` 可能降低公式质量 | **首选**：成本最低，且能修复字符损坏 |
| E. 完全后处理 vs 管线内规范化阶段 | 缺陷反复出现 | 后处理一次性便宜；管线层需测试、配置、白名单维护 | 后处理不可复用；管线层现在过度设计 | 现在选一次性；未来复发再上管线层 |

### A. 保留原始产物，只在表格块之外归一化

做法：先按块切分（front matter、HTML 表格、`<div class="mineru-algorithm">`、围栏代码、`$$…$$`、行内 `$…$`、普通段落），只对普通段落做标签处理。

- 优点：表格天然免疫；实现比全篇正则安全。
- 代价：块扫描要正确处理一行内闭合的 `<table>…</table>`（Mem0 的两张表都在单行内），以及跨行 `$$` 块；一旦切分错误，表格会被当正文处理。
- 失效：如果把「尖括号」当成通用噪声，会删掉 `<think>`/`<title>`/`<integer>`；因此必须**只处理 `sub` 与 `sup` 两种标签名**。
- 结论：作为一次性修复的骨架可以，但不单独成为路线。

### B. 按上下文判定 `sub/sup`

可落地的规则分层：

1. 词内（左右皆字母）→ 合并，前提是合并结果命中词典或文档内未受污染词表。
2. 词首/词尾 → 合并，但要求命中词典；否则进入人工清单。
3. 标签内容含空格且跨词 → 合并，同样要求结果命中词典。
4. 纯数字/纯符号/独立标签 → 默认不动。
5. 白名单：`Mem0<sup>g</sup>`、`Neo4j<sup>1</sup>`、单位/脚注上下文 → 保留。
6. 公式区间 → 一律不动。

量化上限（用文档内未受污染词表做闭包测试）：

- 4,651 个含标签 token 中，**3,110 个（66.9%）**去标签后的形态在文档别处以完整形式出现过。
- 这些 token 覆盖 **4,744/7,710 个标签（61.5%）**。
- 剩余 1,530 个 token 包含：`eficiency`、`sophisticated` 这类“在本文中从未完整出现过”的词，以及 `p95`、`a` 等短词。没有外部词典时无法可靠修复。

失效场景：专名（`Chhikara`）、变体记号、脚注数字、数学符号；以及去标签后仍不成立的碎片（`s stems`、`No- tably`）。**这条路无法触及丢失的字母与空格。**

### C. 转换到更稳的表示

- **公式**：现状已经是 LaTeX，`$…$`/`$$…$$` 内部 0 标签，没有转换必要。
- **表格**：Mem0 的两张表都含 `rowspan`/`colspan`（L108、L132），标准 Markdown 表格无法表达合并单元格；转成标准 MD 表会**直接丢结构**。保持 HTML table 是正确选择。
- **下标数字用 Unicode**：本库真实数字上标只有极少数（Mem0 仅 `Neo4j<sup>1</sup>` 与若干噪声数字），收益接近 0；还会破坏精确搜索与复制。
- 结论：表示层不需要改；问题在文本层。

### D. 调整 MinerU 参数 / 换产物形态后重转

可比较的三组参数：

1. 同模型 `vlm` 重转（`--force`）：验证是否为一次性解码失稳。
2. `--model-version pipeline`：非 VLM 的版面/OCR 管线，通常不会生成这种内联样式标签，但公式与复杂表格可能退化。
3. `--lang en`（当前 CLI 默认 `ch`）：语言提示可能影响分词与空格恢复，收益不确定。

成本：每次 1 个文件、1 次调用；无源文件改动；PDF、id、版本不变。收益上限最高，因为能同时修复标签、丢字母、丢空格。

风险：新产物与 `parser: mineru-cloud 3.4.4` 不再一致（front matter 会记录新版本）；MD 行号变化；资产命名/裁图可能变化（当前 7 个资产、5 处引用）。

### E. 完全后处理 vs 管线内规范化阶段

- 一次性后处理：适合「只修 Mem0」；脚本可放在 `analysis/` 或临时目录，不进管线；无需长期维护。
- 管线内阶段：只有在检测器表明「多篇、反复出现」时才值得。它需要：块级屏蔽、词表、白名单、单元测试、失败回退，以及不能改变图片链接与 front matter 的约束。
- 当前 1/27 的发病率不支持后者。**先一次性，后观察。**

---

## 4. 推荐路线与分阶段计划

### Phase 0 · 基线固化（本轮已完成）

- 产出本文件中的计数、行号与 PDF 对照。
- 不新增脚本、不改 MD、不重转。
- 可选的后续动作（下一轮再做）：在 `check` 中加一个**只读**指标，输出「表格外 `sub+sup` 密度」，阈值 2/千字；超过即打印文件名与行号，不改文件。挂接点见 [`check_document`](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/pdf_library.py#L343-L356)。

### Phase 1 · 只重转 Mem0（首选验证）

动作：

```text
python .agents/skills/pdf-manager/scripts/pdf_manager.py convert \
  resources/papers/pdf/arxiv-2504.19413v1.Project.Mem0.pdf \
  --root resources/papers --force --lang en
```

- 只处理这一篇；不碰其它 26 篇。
- 若需要保留证据，后续可加一个只读的“保留原始 ZIP”选项；本轮不改代码，因此先以新 MD 与 PDF 对照为准。

判定（全部满足才验收）：

| 检查 | 门槛 |
|---|---|
| 表格外 `<sub>`+`<sup>` 密度 | < 1/千字（当前 48.05） |
| 两张表 | 与旧 MD 逐字节一致，或仅空白差异；行/列/`rowspan`/`colspan` 不变 |
| 103 段行内公式 | 逐字节一致 |
| 5 处已知字符损坏 | 全部恢复（`graph construction`、`offering`、`efficient`、`a foundation`、`separate sessions`） |
| 资产 | `check` 无缺失；7 个资产仍在，5 处引用可解析 |
| front matter | `id`、`source`、`abstract` 不变；`parser` 如实记录新版本 |

若通过：结束。后续只需在 `CHANGELOG.md` 追加一条「重转 Mem0 及原因」（本轮不写）。

**执行结果（2026-11-02，未通过）**：`vlm --force --lang en`（batch `4c1d18e9`）产出与旧件逐字节等价——2 张表、103 段行内公式、7 个资产同哈希，仅图引用 `chart2`→`chart4`（两者同哈希）与提示词块 11 处空行；表格外 `<sub>` 6837 / `<sup>` 873 不变，密度仍 50.42/千字；5 处字符损坏全部未恢复。新产物还把 front matter 改成全字段加引号并新增 `title`，与全库其余 26 篇风格不一致。已恢复旧 MD、删除重复的 `chart4`，并在 `CHANGELOG.md` 追加记录。

### Phase 2 · 若仍不达标，比较 `pipeline`

在**临时 root** 中重转同一 PDF，避免覆盖现有产物：

```text
python .agents/skills/pdf-manager/scripts/pdf_manager.py convert \
  <同一 PDF> --root <临时目录> --force --model-version pipeline --lang en
```

比较维度：标签密度、表格结构、公式保真、字符损坏、图片资产。选择「标签最低且表格/公式不退化」的版本。若 `pipeline` 的表格或公式明显退化，则放弃 D 路线，进入 Phase 3。

**执行结果（2026-11-02，未通过）**：`pipeline`（batch `78dc3d25`，临时 root）表格外 `<sub>` 6922 / `<sup>` 874，密度 50.54/千字，与 `vlm` 的标签落点重合 91.4%；行内公式由 103 段变为 131 段（结构更碎），5 处字符损坏同样未恢复。结论：D 路线整体否决，不再以重转为修复手段。

### Phase 3 · 一次性修复（仅当重转不可用或仍失败）

只对目标文件生成**副本**，不原地改：

1. **屏蔽区**：front matter；`<table>…</table>`（单行与跨行都要处理）；`<div class="mineru-algorithm">…</div>`；围栏代码；`$$…$$`；行内 `$…$`；图片行（行首 `![`）；标题行首的 `#`。全部按源文结构标记定位。
2. **只处理两种标签**：`<sub>`、`<sup>`。其它尖括号标签一律不动。
3. **合并规则**：词内优先；合并结果必须命中词典/文档词表；含空格内容同样处理；纯数字/符号/独立标签不动。
4. **白名单**：`Mem0<sup>g</sup>`、`Neo4j<sup>1</sup>`、作者单位上标、脚注数字。
5. **不变量**：只允许删除标签与片段间空格；除规则 R5（无标签字符损坏，须 PDF 逐字证实）外，不允许增删字母；换行数必须相等。
6. **残余清单**：所有未自动处理的标签输出「行号 + 原文 + 原因」，人工对照 PDF。
7. **表格/公式回归**：修复前后对每个表格块与每段公式取哈希，必须完全相同。

若 Phase 3 执行，请预期：按收窄后的规则（§9.3）标签可消掉约 **93.6%**；`ra h`、`ofering`、`afoundation` 这类字符损坏仅在有 PDF 逐字证据时才补，无法证实的仍留原样，引用时仍需回 PDF 核对。

**2026-11-02 收窄修订**：Phase 3 的判据由「文档内未受污染词表」单条，改为「词表 + PyMuPDF 同句逐字命中」双条件；不再引入 `pymupdf4llm` 作为第二版结构来源。具体规则与规模见 §9.3、§9.6。

### Phase 4 · 只有复发才上管线层

触发条件：未来检测器在 **≥2 篇不同文件**上超过 2/千字，或同一来源反复出现。

设计要点：

- 位置：`parse_archive` 之后、`write_conversion` 之前，对 `parsed["body"]` 做纯文本规范化。
- 结构：块扫描 + 保护区间 + 仅 `sub/sup` + 词表白名单。
- 测试：用 Mem0 作重症样本、LongMemEval 作表格样本、MemoryArena 作真实上标样本、Agentic Memory 作提示词样本。
- 失败策略：任何不确定的标签保留原样并计数，不猜。

### 自动修 vs 人工复核的边界

| 类别 | 处理 |
|---|---|
| 词内字母片段，合并后命中词典/文档词表 | 自动 |
| 标签含空格且合并在词表内 | 自动 |
| `<sub>-</sub>` 等纯符号，删除标签不改变字符 | 自动 |
| 词首/词尾片段但词表未命中 | 人工 |
| 独立标签（204 个，2.6%） | 人工 |
| 纯数字/纯符号 `sup`（除已确认脚注） | 人工 |
| `Mem0<sup>g</sup>`、`Neo4j<sup>1</sup>`、作者单位 | 保留，不修 |
| 公式内、代码内、算法块内、提示词内 | 永不处理 |

### 如何避免改坏表格

1. 先切块再处理，不在全文字符串上跑跨块正则。
2. 表格块哈希前后必须相同（字节级）；行数、单元格数、`rowspan/colspan` 数量作为附加断言。
3. 只处理 `sub/sup` 标签名，不碰 `table/tr/td/div/think/...`。
4. 若切块器遇到不闭合的 `<table>`，整文件放弃自动修复，转人工。

---

## 5. 验收指标

| 指标 | 定义 | 当前基线 | 目标 |
|---|---|---|---|
| 标签误报率（核心） | 表格外 `sub+sup` 密度（个/千字） | Mem0 48.05；全库次高 0.84 | < 1.0；跨库阈值 2.0 只命中 1/27 |
| 表格结构保持率 | 表格块 SHA-256 相同 | Mem0 2/2 | 100%；全库回归时 268/268 |
| 公式保持率 | `$…$` / `$$…$$` 段字节相同 | Mem0 103 段 | 100% |
| 断词粘连修复数 | 含标签 token 去标签后命中词表 | 4,362/4,659 词（93.6%） | 自动修 ≥93%；保守 ≥4,000 |
| 真上标保留率 | 白名单逐条匹配次数 | 6 条（5 × `Mem0<sup>g</sup>`、1 × `Neo4j<sup>1</sup>`）+ 1 条形式损坏 | 100%，一条不少 |
| 字符不变量 | 除 R5 外，去标签后字母序列不变；换行数相等 | — | 0 个非证据增删；行数恒等 |
| 需人工/AI 复核残留 | 规则 R6 的词 | 297 词（295 token）/ 70 行 | ≤20 条/包、≤12,000 字/包、共 ≤15 包 |
| 字符损坏修复 | 5 处已定位损坏 | 5/5 破损 | 5/5 经 PDF 逐字证实后修复；未能证实的不改 |
| 资产完整性 | `check` 缺失图片数 | 0 | 0；7 个资产保留 |

> §9.5 是执行时的操作版指标；本表是跨文件、跨路线的总账口径。

测量口径：

- 密度 = `(count(<sub>) + count(<sup>)) / 去表格后的字符数 × 1000`
- 词表命中 = 去标签后的 token（去标点、小写）是否出现在「文档未受污染词表 ∪ PyMuPDF 词表」中
- 表格块 = 从 `<table` 到 `</table>` 的整段字节；逐块哈希

---

## 6. 风险与边界

### 不该用规则硬修的内容

- **真实上下标**：`Mem0<sup>g</sup>`（[L56](file:///d:/workspace/memory/resources/papers/md/arxiv-2504.19413v1.Project.Mem0.md#L56)、L70、L122、L149、L291）、`Neo4j<sup>1</sup>`（L74）、MemoryArena 作者单位（[L13](file:///d:/workspace/memory/resources/papers/md/arxiv-2602.16313v2.Bench.MemoryArena.md#L13)）。
- **数学**：`<sup>d+k</sup>`、`<sub>ε2</sub>` 这类 HTML 化数学（MemoryArena L586），以及所有 `$…$` 内部内容。
- **正文里的尖括号契约**：`<think>`（Agentic Memory [L451](file:///d:/workspace/memory/resources/papers/md/arxiv-2601.01885v3.Method.Agentic Memory.md#L451)–L469）、`<title>`（Million-Token Memory L2416 起）、`<integer from 1-10>`（MemoryBench L711）、`<key>: <value>`（AMA L716）。这些是作者的提示词/schema，删掉会改变论文内容。
- **算法块**：`<div class="mineru-algorithm">`（A-Mem L498/L515/L529、EverMemOS L379/L463/L503、AMA L513、MemoryArena L523）是结构，不是噪声。

### 重转带来的版本与引用一致性

- PDF、`id`、`source` 不变 → **引用身份安全**；引用应指向 PDF 与图表，不应指向 MD 行号。
- MD 行号会变：当前分析稿引用的是 Table 2 的数值（如 Mem0 66.88%），不是 MD 行号，因此不受影响；但若有文稿按行号定位，需要重定位。
- `parser` 字段会从 `mineru-cloud 3.4.4` 变成当前服务版本；这意味着旧 MD 不再能由记录的解析器版本复现，应在 `CHANGELOG.md` 记录。
- 资产命名由图注编号推导；重转后可能出现裁图差异或未引用资产变化，必须跑 `check`。
- `md-zh/` 有 6 篇中文译本，其中**没有 Mem0**；若未来重转已有译本的论文，译本会立刻变成“旧 MD 的译本”，需要明确是否重译。
- 库规则：已有转换件不会因线上新版本自动换版；本次只对明确指定的 Mem0 使用 `--force`，不扩大范围。

### 其他边界

- 不删除正文、不“顺手润色”、不修改表格、不把 HTML 表格转成 Markdown 表格。
- 不在本轮改动任何现有 MD；本文件只是计划。
- 后处理脚本若将来落地，应产出「变更差异 + 残余清单」，而不是静默改写。

---

## 7. 附：复现口径

- 标签统计：对 `resources/papers/md/*.md` 逐文件计数 `<(sub|sup)>`；表格内计数先以 `<table…</table>` 整体屏蔽。
- 区域划分：front matter（首个 `---` 块）、HTML 表格块、`$$` 块、`References` 之后为参考文献、`Figure/Table/Algorithm` 开头为图注，其余为正文。
- 上下文分类：标签开标签前一字符、闭标签后一字符是否为字母。
- PDF 版式核对：PyMuPDF `page.get_text("rawdict")`，逐行统计字符 `origin.y` 极差与字号；第 1–3 页抽样 36 行，极差均为 0.00。
- 字符损坏核对：`page.search_for()` 在 PDF 中检索 `graph construction completes`、`offering a compelling`、`efficient LLM-driven`、`a foundation of intelligence`、`separate sessions`；PDF 均能命中，MD 均破损。
- 词表闭包：同文件「不含标签的空白 token」构成未受污染词表（Mem0 为 1,322 个词），对含标签 token 去标签后查表。

## 8. 替代抽取实验（2026-11-02）

产物只落在 `resources/papers/.rivet_scratch/alt-extract-20261102/`，未入库。项目 `.venv` 无依赖声明；系统 Python 3.13 自带 PyMuPDF 1.28.2 与 pymupdf4llm，pdfplumber 0.11.10 用临时环境。marker / docling 未安装，需 torch（GB 级）与权重下载，按「环境里可用才加一条」的条件未跑。

```text
python C:\Users\37071\AppData\Local\Temp\alt_extract_pymupdf.py
uv run --with pdfplumber python C:\Users\37071\AppData\Local\Temp\alt_extract_pdfplumber.py
```

| 维度 | MinerU `vlm` | PyMuPDF 纯文本 | `pymupdf4llm` | `pdfplumber` |
|---|---|---|---|---|
| 字符数 | 160,453（含 7,710 个标签） | 70,061 | 72,204 | 仅表格 811 B |
| `<sub>` / `<sup>` | 6,837 / 873 | 0 / 0 | 0 / 50（全部真实上标） | — |
| 5 处字符损坏 | **0/5 恢复** | **5/5** | 4/5（`a foundation` 被斜体标记包裹，文字完整） | — |
| 两张表 | HTML，`<td>` 160 / 155，`rowspan`/`colspan` 保留 | `find_tables` 2 张，但小数点与 `±` 被打散 | 2 张，14 / 25 行，**带小数数值覆盖 100%** | 1 张，3×3，列组被合并、数值丢失 |
| 数学 | 103 段行内公式，LaTeX | 纯文本扁平（`Mem0g`） | `Mem0`<sup>_g_</sup>，无 `$` | — |
| 标题层级 | `#` / `##` 两级 | 无 | `#` / `###` / `####`，4.1、4.2 漏检 | — |
| 代码 / 提示词 | 5 个 `txt` 代码围栏 | 无围栏 | 44 个无语言围栏，提示词正文在 | — |
| 参考文献 | 1,300 个标签落在该区 | 完整文本 | `-` 列表 | — |
| 耗时 | 云端（分钟级） | 0.047 s（页）/ 0.493 s（块） | 11.9 s | 0.925 s |
| 依赖 | API key + 网络 | 104 MB wheel，纯 CPU，离线 | 同左 + 1 MB | uv 临时环境，不入项目 |

同一位置的三个版本：

```text
[MinerU]      ...ra <sup>h</sup> construct<sup>i</sup>on com <sup>l</sup>etes <sup>i</sup>n un<sup>d</sup>er a m<sup>i</sup>nute...
[PyMuPDF]     ...Mem0 graph construction completes in under a minute even...
[pymupdf4llm] ...graph construction completes in under a minute even...
```

```text
[MinerU]      | 38.72 | 27.13 | 67.13 ± 0.65 |
[pymupdf4llm] |**38.72**|**27.13**|**67.13 ± 0.65**|
[find_tables]  3872 2713 6713±065 . . . .
```

可判定结论：

- **文本修复的参照**：PyMuPDF 纯文本最强——5/5 命中、零标签、0.05 s；但没有结构，只能当字符级真值。
- **表格校验源**：`pymupdf4llm` 是唯一同时保住行列结构与数值的本地产物（130 + 110 个带小数数值 100% 覆盖，`Mem0` 行可逐格对齐）；`find_tables` 与 `pdfplumber` 只能做局部交叉验算。
- **数学**：三者都不产生 LaTeX；MinerU 独有，必须原样保留，任何自动合并都要绕开公式。
- **不能替代 MinerU 的部分**：标题层级、代码语言标记、公式、图片裁图。因此本地工具只补「文本 + 表格」这半，另一半仍靠原转换件。
- **不值得**：单独用一个本地工具重做整篇转换。`pdfplumber` 在 Mem0 上只找到 1 张 3×3 的表，且丢失数值，可直接排除。

**定位调整（2026-11-02 收窄）**：本节 `pymupdf4llm` 的表格/结构结论只作实验记录，不进入方案。§9 只用 PyMuPDF 纯文本作字符真值，因为本轮不修结构。

## 9. 收窄后的修复方案：MinerU 底稿 + PyMuPDF 字符真值

> 本节是**算法层**设计（按一次性脚本的粒度写清规则与规模）。它如何变成 skill 的常驻能力，见 §10；两节冲突时以 §10 为准。

### 9.1 边界：不动什么，不修什么

**一律不动**。脚本按源文里**显式的结构标记**定位这些区间，整段跳过，字节级保留：

| 对象 | 源文中的定位标记 | 为什么不能碰 |
|---|---|---|
| front matter | 文件首 `---` … `---` | 登记块；键名与顺序由库规则约束（`pdf_library.render_markdown`） |
| HTML 表格 | `<table>` … `</table>` | 2 块；表内 `<sub>/<sup>` 计数为 0，本来无噪声；表结构由 `rowspan`/`colspan` 承担 |
| 独立公式 | `$$` … `$$` | LaTeX 记号，任何替换都会破坏语义 |
| 行内公式 | 行内成对的 `$…$` | 103 段；实测内部标签 0 |
| 代码围栏 | 行首三个反引号（到下一个同级围栏） | 5 个 `txt` 块，含提示词模板原文 |
| 算法块 | `<div class="mineru-algorithm">` … `</div>` | 伪码，非自然语言 |
| 图片行与路径 | 行首 `![` | `../assets/…` 是库约定，改一个字符即断图 |
| 标题标记 | 行首的 `#` 与紧随的空格 | 层级不得变；**标题文字本身允许参与 R1–R5**（如 `## 2.2. Mem0<sup>g</sup>`，其标签属于白名单） |

**已知但不处理**。这些是结构问题，本轮明确出界，只写进残余清单，不猜：

- 跨行断句 / 断词：一个词被换行切开，标签落在两行之间。
- 页眉页脚混入正文段落。
- 表格插入段落中间、段落被 HTML 块截断。
- 图注与正文的顺序错位。
- **上游已丢失的真上标**：PDF 文本层 45 处 `Mem0g`，MD 只剩 19 处 LaTeX `\mathtt{M e m O}^{g}` 与 5 处 `<sup>g</sup>`，其余约 20 处在正文已被吃掉，只剩 `Mem0`。无从判定该不该有上标，补写即为臆造，不做。
- PDF 无文本层（扫描件）：整篇只做屏蔽与报表。

**修复单位**（贯穿全节的唯一硬约束）：

1. 只替换**同一行内**的连续字符片段；不跨行、不重排、不增删换行。
2. 替换片段两端落在词边界或标点边界上，绝不切开字母。
3. 断言 `body.count("\n")` 前后相等；任何改变行数的操作直接拒绝并报错。
4. diff 按行输出，每行差异只显示被替换的几个字符与左右各 20 字上下文。

补充一个事实依据：该 MD 的段落基本一行一段（379 行对应 23 页），所以「同段」与「同行」几乎等价；脚本取「同行」为硬边界，比「同段」更严，等价于把「不重写段落」变成可断言的条件。

### 9.2 依赖：只留 PyMuPDF 纯文本

| 项 | 取值 | 依据 |
|---|---|---|
| 库 | PyMuPDF 1.28.2 | 系统 Python 3.13 已带；**不写入** `pyproject.toml` |
| 体积 / 算力 | 104 MB wheel，纯 CPU，离线 | §8 实测 |
| 耗时 | 0.047 s（按页）/ 0.493 s（按块） | 全文 23 页 |

只作三种用途，都不采它的结构：

- **句子定位**：`page.search_for()` 检索整句，得到页号与包围盒。
- **整词检索**：在 `get_text("text")` 上做带边界的词匹配，判断候选词是否「逐字存在」。
- **行→句锚定**：把该 MD 行去掉标签后，与 PDF 全文做词级对齐（`SequenceMatcher(autojunk=False)` + 长词锚），只回答「这一行对应 PDF 哪一句」，不采用 PDF 的换行与段落。

`pymupdf4llm`、`pdfplumber`、`find_tables` 全部退出方案：本轮不修表格与标题层级，它们的产物会引入第二个行号空间，使 diff 与引用对不上。§8 的结论保留为实验记录。

### 9.3 判定规则清单

| 编号 | 触发条件 | 判定条件 | 动作 |
|---|---|---|---|
| **R0** | 落在 §9.1 任一屏蔽区间内 | — | 跳过，记 `skipped`，计数进报表 |
| **R1** | `sub/sup` 两侧都是字母，去标签后与前后字母连成完整词（`Lar<sub>g</sub>e`） | ①合并词在该行锚定的 PDF 句里**逐字**命中；②该词在文档词表 ∪ 英文词表成立 | 合并，删除标签本身 |
| **R2** | 只有一侧是字母（`<sub>p</sub>rowess`、`generat<sub>ing</sub>`） | 同 R1 的两条；任一条不成立则落 R6 | 合并 |
| **R3** | 词尾、内容为数字或单个字母、前接专名或实体（`Mem0<sup>g</sup>`、`Neo4j<sup>1</sup>`），或位于数学上下文 | 命中白名单 | **不修**；计数前后必须相等 |
| **R4** | 标签内容为标点或纯符号，删标签不改变字母序列（`<sub>-</sub>`、`<sup>’</sup>`） | 合并后的字符序列与 PDF 同句一致 | 只删标签，不补任何字符 |
| **R5** | 无标签但字符损坏（`afoundation`、`ofering`、`eficienc`） | ①同句内、替换跨度 ≤6 字符；②替换后在 PDF 文本中**逐字可查**；③替换结果是词表内的词 | 替换该词 |
| **R6** | 其余（两版都说不清的畸形片段，如 `ara</sub>t<sub>e`、`<sub>s</sub>i<sub>ng</sub>l<sub>e-</sub>h<sub>op,<`） | 不猜 | 不改，出 AI 包 |

几条必须写进脚本的附注：

- **R1/R2 的两条是「且」不是「或」。** 只靠词表会把 `Mem0g` 当成待合并的坏词；只靠 PDF 命中会放过 PDF 自身也印错的情况（本期未见，规则仍要设防）。
- **OOV ≠ 损坏。** 65 个无标签 OOV（≥4 字母，如 `Enai`）多数是参考文献人名与术语，在 PDF 里逐字可查，属正常词，不动。只有「PDF 里查不到、且同句存在相似度 ≥0.9 的 PDF 词」才进 R5。
- **白名单按文件生成、随补丁清单存档，不写死在脚本里。** Mem0 的完整白名单只有 6 条：
  - `Mem0<sup>g</sup>` ×5（正文 L56、L70、L149、L291 等）——Mem0 的图变体记号；
  - `Neo4j<sup>1</sup>` ×1（L74）——脚注编号；
  - 另有 1 条**形式损坏的真上标**：L72 `Mem0<sup>g i</sup>mp…`，内容带空格但去标签后仍是 `Mem0g`，按 R1 合并会正确，但必须**保留上标形式**，单列交 AI 确认一次。
- **`Mem0<sup>’</sup>` ×3、`OpenAI<sup>’</sup>` ×1** 是撇号被误标成上标，内容非字母数字，走 R4 只删标签，不是真上标。
- R5 的 5 个已知点：`ra <sup>h</sup> construct<sup>i</sup>on com <sup>l</sup>etes`（p.14）、`ofering`（p.1）、`eficien…`（p.1）、`afoundation`（p.1）、`se ara t e`（p.2），PDF 均可逐字命中。

### 9.4 脚本草案（只设计，不执行）

落点：`resources/papers/.rivet_scratch/repair/`。**本轮一行都不跑，也不碰库内 `md/`。**

```text
resources/papers/.rivet_scratch/repair/
  locate.py     # 结构标记状态机 → protected.json
  align.py      # 行 → PDF 句锚定   → anchors.json
  decide.py     # 规则 R0–R6        → patches.json
  emit.py       # 应用（只对副本）+ diff + 统计 + AI 包
  rules.toml    # 白名单、词表路径、开关
  out/
    protected.json  anchors.json  patches.json
    patches.diff    stats.json    ai-packs/p01.txt …
```

数据流：

```text
md  ──┐
      ├─ locate.py → protected.json   （行号, 起止偏移, 区间类型）
pdf ──┤
      ├─ align.py  → anchors.json     （MD 行 ↔ PDF 页 / 句 / 字符偏移）
      ├─ decide.py → patches.json     （每条带规则编号与证据）
      └─ emit.py   → patches.diff / stats.json / ai-packs/*.txt
```

补丁条目（一条一个替换，自解释、可人工核对）：

```json
{"file": "md/arxiv-2504.19413v1.Project.Mem0.md",
 "line": 19, "start": 3, "end": 14,
 "original": "Lar<sub>g</sub>e",
 "replacement": "Large",
 "rule": "R1",
 "evidence": {"pdf_page": 1,
              "sentence": "Large Language Models (LLMs) have demonstrated remarkable prowess",
              "match": "verbatim"},
 "vocab": ["large"],
 "confidence": 0.99}
```

**怎么保证只碰正文文字**——四道闸，全部是可断言条件，不靠文本猜测：

1. **按标记切分，不按内容推断。** `locate.py` 是逐行状态机，只认五种显式标记：

   ```text
   front matter : 首个 "---" 到下一个 "---"          → 整段屏蔽
   table        : "<table"         → 直到 "</table>"    → 整段屏蔽
   fence        : 行首 "```"        → 直到同级 "```"      → 整段屏蔽
   math         : "$$" 配平；行内 "\$[^$]+\$" 逐段屏蔽
   algorithm    : "<div class=\"mineru-algorithm\">" → 直到 "</div>"
   image        : 行首 "!["
   ```

   没有任何一步依赖「这看起来像表格」之类的判断。

2. **补丁必须落在单个未屏蔽区间内。** 每条补丁记录 `(line, start, end)`，应用前断言该区间不与 `protected.json` 的任何区间相交、且不跨越行尾。

3. **行数不变量。** 应用前后 `body.count("\n")` 必须相等；不等则整批作废。这一条直接排除「重写段落」「重排换行」的一切可能。

4. **结构哈希与白名单计数不变量。** 每个表格块、每段公式、每个代码围栏、每条图片引用的字节串 SHA 前后相同；白名单 6 条的匹配次数前后相同。任一不符，拒绝写入。

`emit.py` 的默认行为是 **dry-run**：只打印 diff 与统计，不写文件。要写也只能写 `--out` 指定的副本路径，且拒绝解析到 `resources/papers/md/` 下。

dry-run 输出形态：

```text
L19  - Lar<sub>g</sub>e Lan<sub>g</sub>ua<sub>g</sub>e
     + Large Language
     证据: p.1 "Large Language Models (LLMs) have demonstrated ..."
L25  - Human memory is afoundation of intelligence
     + Human memory is a foundation of intelligence
     证据: p.1 "Human memory is a foundation of intelligence"
统计: R1 4,201 · R2 161 · R4 3 · R5 5 · R6 297 · 跳过区间 9
净改 83 行 · −79,354 字符 · 残留标签 483（待 AI）
```

### 9.5 验收指标

| 指标 | 阈值 | 基线 / 现状 | 量法 |
|---|---|---|---|
| 真上标保留率 | **100%** | 白名单 6 条 + 1 条损坏形式 | 逐条匹配次数前后相等 |
| 词表命中率 | ≥99% | 4,362 / 4,659 = 93.6% 形式可判 | 修后逐词查英文词表 ∪ 文档词表 |
| 表格哈希 | 100% 不变 | 2 块 | 区间字节 SHA256 |
| 公式哈希 | 100% 不变 | 103 段 | 同上 |
| 代码围栏哈希 | 100% 不变 | 5 个 | 同上 |
| 图片引用与路径 | 100% 不变 | 7 个资产 | 字符串全等 |
| 净改动行数 | ≤90 | 受影响 85 行 | 去重后的补丁行号 |
| 净改动字符数 | 报告值，不设上限 | 标签总长 84,810，预估 −79,000 左右 | 前后长度差 |
| 残留标签 | ≤50（白名单除外） | 7,710 | 计数 |
| AI 包数 / 单包预算 | ≤15 包；≤20 条 / ≤12,000 字 | 12–15 包 | 包清单 |

净改动字符数几乎等于标签自身的长度（`<sub>` + `</sub>` 或 `<sup>` + `</sup>` 各 11 字符 × 7,710 ≈ 84,810），字母层面的增删只来自 R5 的少量替换。这条指标的作用是防止「以为在修词、实际在重写段落」——一旦净改字符数远超 8 万，说明有非词级改动混进来了。

### 9.6 Mem0 收窄后的规模

| 项 | 数量 | 说明 |
|---|---:|---|
| `<sub>` / `<sup>` | 6,837 / 873 | 表格外；表内 0 |
| 含标签 token | 4,651 | 空白切分，占 10,321 个 token 的 45.1% |
| 受损词 | 4,659 | 以词为单位计 |
| **R1/R2 自动可修** | **4,362（93.6%）** | 去标签后每词均命中词表 |
| 保守区间 | 3,800–4,200 | 再叠 PDF 逐字命中过滤，预计损耗 4–12% |
| **真上标白名单** | **6** | 5 × `Mem0<sup>g</sup>`、1 × `Neo4j<sup>1</sup>` |
| 真上标（形式损坏） | 1 | L72 `Mem0<sup>g i</sup>mp…`，确认后保留 |
| **R5 已知损坏** | **5** | `afoundation`、`ofering`、`eficien…`、`graph construction completes`、`separate sessions` |
| R6 → AI | 297 词 / 295 token / **70 行** | 平均 4.2 词/行 |
| AI 包 | 12–15 | 20 条/包，按段落聚合 |
| 受影响行 | 85 / 379 | 页均 3.7 行 |
| 无标签 OOV | 65 | 多数是人名/术语，PDF 可逐字查，不动 |
| 上游丢失的真上标 | ~20 | PDF 45 处 `Mem0g`，MD 保留 19 LaTeX + 5 sup；不处理 |

一句话概括：**动 4,362 条、保留 6 条、升级 297 条、剩约 483 个标签等 AI 裁决后归零**。AI 的实际阅读量是 70 行原文 + 70 段 PDF 邻句，按每包 20 条切成 12–15 包；单包约 9,000 字，在 12,000 字预算内。

### 9.7 一次性脚本，还是固化成管线层

**一次性脚本（当前推荐）**，需同时成立：受污染文件 ≤2；标签家族只有 `sub/sup`；白名单可按文件枚举；规则仍可能微调。

**升级为管线层**（满足任一）：

- 30 天内 ≥3 篇新转换件出现同类噪声（当前是 27 篇里 1 篇重症）；
- 出现 `sub/sup` 之外的正文级标签污染（如 `<div>`、`<think>` 被批量误写进正文）；
- 同一份 PDF 被下游反复消费（翻译、抽取、问答），每次临时修的成本高于固化；
- 规则连续两次运行无需人工调整（说明已稳定，固化才有意义）。

挂载点：先在 `check_document`（[pdf_library.py#L343-L356](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/pdf_library.py#L343-L356)）加**只读**密度报表，积累一个月；确有复发再写 `parse_archive`（[mineru_backend.py#L360-L453](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/mineru_backend.py#L360-L453)）之后、`write_conversion` 之前的补丁层，且必须带 Mem0 / MemoryArena / Scientific Memory 三份回归样本（后两份分别是低密度噪声与真实下标的对照）。

---

## 10. skill 级改造方案（2026-11-03 最终形态）

> **这是 skill 改造方案，不是单文件修补方案。** 目标不是把 Mem0 修干净，而是让 `pdf-manager` 在**任何**新转换件上都能回答两个问题：「这篇脏不脏」「脏的部分哪些可以自动修」。单篇修补只是这条能力的一次调用实例。

### 10.1 用户视角：四个命令，两个默认

```text
python "<脚本>" convert "a/pdf/xx.pdf"                     # 转换 + 体检（只读）
python "<脚本>" convert "a/pdf/xx.pdf" --repair            # 转换 + 自动修可判定项（显式）
python "<脚本>" audit   "a/md/xx.md"                       # 单独体检，只读
python "<脚本>" repair  "a/md/xx.md" --out "D:\tmp\repair" # 阶段一：出补丁计划 + AI 小包
python "<脚本>" repair  "a/md/xx.md" --plan "D:\tmp\repair\patches.json" \
                                --verdicts "D:\tmp\repair\verdicts.json" --apply
```

| 动作 | 默认 | 写什么 | 失败时 |
|---|---|---|---|
| `convert` | **体检开、修复关** | 只写原有的 md / assets / index | 体检异常被捕获，只记 `quality.error`，不影响转换与批处理 |
| `audit` | 只读 | 什么都不写（stdout / `--json`） | 退出码 0；发现问题不是命令失败 |
| `repair`（阶段一） | 只出计划 | 只写 `--out` 目录，**必须在库外或 `.rivet_scratch/` 下** | 缺 PyMuPDF → 退出码 2 并给安装命令 |
| `repair --apply` | 需显式两件套 | 只写该文档自己的 `md/` 文件，原子替换 | 路径不在 `md/` 下 → 拒绝；冲突条目跳过并报告 |
| `convert --all` | 禁止同时 `--repair` | — | 直接报错，一篇都不转 |

体检在 `convert` 里只加一行输出，不改既有行：

```text
[arxiv-2504.19413v1.Project.Mem0] -> .../md/arxiv-2504.19413v1.Project.Mem0.md；7 张分类资产；mineru-cloud vlm
[arxiv-2504.19413v1.Project.Mem0] 体检：表格外 sub+sup 48.05/千字 · 1,166 处跨词标签 · 真上标 6 · 可自动修 4,362 词 · 建议 `repair`
```

### 10.2 管线位置：`parse_archive` 之后、`write_conversion` 之前

选定位置：在 [`convert_documents`](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/pdf_manager.py#L224-L295) 的循环里，`parse_archive`（[L270](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/pdf_manager.py#L270-L272)）之后、`write_conversion`（[L284](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/pdf_manager.py#L284)）之前，对 `parsed["body"]` 的副本做变换。

四条理由：

1. **只有一次写盘。** [`write_conversion`](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/pdf_library.py#L359-L384) 是 `md/` 的唯一写入口。修复在内存里完成后交给它，不可能出现「修了一半的文件」。
2. **行号没有偏移。** 此时 body 尚未前置 front matter，补丁里的行号就是正文行号；若放到 `write_conversion` 之后，行号必须减去 front matter 的行数，还要重新读盘解析，等于把已经算对的坐标再还原一次。
3. **不与资产校验打架。** `write_conversion` 用 `parsed["body"]` 检查「正文引用的图片是否都在结果包里」（[L374-L378](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/pdf_library.py#L374-L378)）。图片行被设为保护区间，引用字符串一字节不变，校验照旧通过。
4. **失败即零写入。** 修复抛异常时 `write_conversion` 还没被调用，磁盘上什么都没有发生；这正是「可回滚」最便宜的实现。

不选另外两个位置：

- **不选 `parse_archive` 内部**：这是网络/解析层，输入是 ZIP bytes，手里没有本地 PDF 路径；把 PyMuPDF 依赖塞进去，会让「只想解析」的调用也被迫承担 104 MB 依赖。
- **不选 `write_conversion` 之后单独一步**：需要第二次写盘 + 二次读盘，回滚从「一步」变成「两步有中间态」，而收益只是代码位置看起来更分层。

**原子性与回滚**。现状必须说清楚：`atomic_text` / `atomic_bytes`（[pdf_library.py#L110-L130](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/pdf_library.py#L110-L130)）是「临时文件 + `os.replace`」，**单文件原子**；但 md、逐张 assets、index.csv 是三次独立替换，跨文件并不构成事务。修复不新增写目标，所以不改变这个事实，也不该假装它已经事务化。

在此前提下做三点加固（都落在 `write_conversion` 内部，签名不变）：

1. **写盘前快照**：`previous = doc.md.read_bytes() if doc.md.is_file() else None`；同时记录 `created = [name for name in assets if not (root/"assets"/name).exists()]`。
2. **异常回滚**：`try: 写 assets → 写 md → 更新索引 except: 用 previous 原样写回 md（若为 None 则删除）；删除 `created` 中本次新建、且旧 md 未引用的资产；重新抛出`。旧 md 引用过的资产不删——它们可能是上一轮转换留下的有效文件。
3. **索引降级**：`update_existing_index` 只补 keywords，失败记为 warning 而不回滚 md；索引本就不是交付物，且它自己也是 `atomic_text` 整表替换。

补丁报告一律不落库内：走 stdout，或由 `--out` 指向库外。

### 10.3 触发：体检默认开，修复默认关

体检函数 `audit_body(body, pdf_path=None) -> dict`，只读、纯函数：

```json
{"density": 48.05,
 "tags": {"sub": 6837, "sup": 873},
 "blocks_over_threshold": 9,
 "worst_block": {"line": 167, "per_kchars": 213.0},
 "true_sups": {"Mem0<sup>g</sup>": 5, "Neo4j<sup>1</sup>": 1, "Mem0<sup>g i</sup>": 1},
 "known_corruptions": {"afoundation": true, "ofering": true, "eficienc": true},
 "pdf_text": {"available": true, "engine": "pymupdf 1.28.2"}}
```

- **阈值**：块级 ≥2 个标签/千字（依据 §1.1：全库 26 篇正常件最高 0.84/千字，2 是 2.4 倍余量）。全篇密度只做汇总，不参与触发——长文档会稀释局部重症。
- **默认值的三条理由**：
  1. 全库 1/27 命中，默认改文件等于让 4% 的文件改变 96% 的行为；
  2. 库规则本来就写着「已有转换件不因线上新版本自动换版」，默认改写与之相悖；
  3. 体检成本是纯正则计数（毫秒级），缺 PyMuPDF 也能跑；修复才需要文本层。
- **批处理不被卡住**：`convert --all` 逐篇体检，`audit_body` 内部异常一律 catch 成 `"error": "..."` 字符串，`errors` 计数不加；单篇脏或单篇体检失败都不影响其余 26 篇的转换与退出码。
- **批处理禁止自动修**：`--all` 与 `--repair` 互斥（`LibraryError`），避免一次对 27 篇做 4,000 级的字符替换。

### 10.4 两阶段接口：脚本出包 → Agent 裁决 → 脚本应用

skill 不调外部 API、不要 key，所以把「需要判断」的部分外化成文件，让当前 Agent 会话自己读包、写裁决。

**阶段一** `repair --out DIR`（只产文件，不碰 md）：

| 产物 | 内容 |
|---|---|
| `DIR/patches.json` | 全部自动判定项：`id`、`line`、`start`、`end`、`expect`、`replacement`、`rule`、`evidence` |
| `DIR/verdicts.template.json` | 只含 R6 项，`action` 预填 `"keep"`，待 Agent 填 `merge`/`replace` |
| `DIR/ai-packs/p01.md` | 每包 ≤20 条、≤12,000 字；每条 = 行号 + 原文片段 + PDF 邻句 |
| `DIR/stats.json` | 分规则计数、净改行数、净改字符数、残留标签、白名单计数 |

**阶段二** `repair --plan … --verdicts … --apply`：

- 输入：上面两件套；`--verdicts` 可缺省。
- 按 `expect` 校验：偏移处仍是原文 → 应用；原文已不在 → 记 `already-applied` 跳过；位置在但内容不同 → 记 `conflict`，该条不改。
- **幂等**：阶段一的 id 是 `p0001…`，按 `(行号, 偏移)` 排序生成，无时间戳、无随机数，同一输入跑两次字节相同。阶段二对已修文件再跑一次，结果是 `0 applied / N already-applied`，md 字节不变，退出码 0。
- **裁决缺失的降级**：缺 `--verdicts`、或某 id 不在裁决表里 → 一律 `keep`（保留原样），计入 `unresolved` 清单。**不猜**，也不把「没有裁决」当成「同意修改」。
- **写入闸**：`--apply` 只接受解析到「该文档自己的 `md/` 文件」的目标；指向 `assets/`、`pdf/`、库外路径、或经软链逃逸的路径，一律非零退出且不写。

### 10.5 依赖取舍：可选依赖 + 显式降级

| 方案 | 具体影响 | 判定 |
|---|---|---|
| 强制依赖 | `convert` / `download --convert` 全部要求 PyMuPDF；只做下载、索引、元数据的用户被迫多装 104 MB；skill 首页「Python 标准库即可」的承诺破功 | 否 |
| **可选依赖 + 降级** | 缺库时 `audit` 仍能出标签密度（纯正则），`repair` 明确拒绝并给安装命令，退出码 2；`convert` 体检降级为「只有密度，无真上标/损坏项」 | **采用** |
| 零依赖替代 | 标准库解不开 PDF 内容流、CMap 与对象表；MinerU 的 `content_list.json` 转换后不保留；pdfminer 同样是第三方包 | 不存在 |

- 检测：`probe_pdf_text()` 用 `importlib.util.find_spec("fitz")` 探测，返回 `{"available": bool, "engine": "pymupdf x.y.z", "reason": str}`；结果随体检一起进 stdout，用户看得见当前引擎。
- 报错文案（可直接照抄）：`缺少 PDF 文本层依赖：PyMuPDF（约 104 MB，纯 CPU 离线）。执行 python -m pip install pymupdf 后重试；只做体检可用 audit。`
- 不写进 `pyproject.toml` / `uv.lock`：skill 设计为可整体拷贝到任意机器，项目依赖保持为空。需要临时用时显式 `uv run --with pymupdf python "<脚本>" repair …`。

### 10.6 文件级改动清单

| 文件 | 改动 | 为什么在这里 | 对现有行为的影响 |
|---|---|---|---|
| `scripts/pdf_repair.py`（新增，约 550 行） | 函数：`locate_protected(body)`、`iter_tag_words(line)`、`align_line_to_pdf(line, page_text)`、`classify(...)`、`build_plan(body, pdf)`、`render_packs(plan)`、`apply_verdicts(plan, verdicts)`、`audit_body(body, pdf=None)`、`probe_pdf_text()` | 职责分层：`pdf_library` 管存储、`mineru_backend` 管网络与解析、`pdf_repair` 管纯文本变换。三者互不 import 循环 | 无（新文件） |
| `scripts/pdf_manager.py` · `add_conversion_options`（[L301-L309](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/pdf_manager.py#L301-L309)） | 加 `--repair`、`--no-audit` | 转换参数集中在这一个函数，`convert` 与 `download --convert` 两个入口共享 | 默认值即体检开、修复关；不加参数时命令行完全兼容 |
| `scripts/pdf_manager.py` · `convert_documents`（[L224-L295](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/pdf_manager.py#L224-L295)，插在 [L284](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/pdf_manager.py#L284) 前） | 三步：`audit_body` → 若 `--repair` 则 `build_plan` + 自动项 `apply_verdicts` → 打印体检测 | 此处 body 是内存对象、PDF 路径在手、尚未写盘 | 既有 `-> ...` 行不动，只多一行 `体检：…` |
| `scripts/pdf_manager.py` · `make_parser`（[L312-L345](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/pdf_manager.py#L312-L345)） | 新增 `audit`、`repair` 两个 subparser；`repair` 的 `--out / --plan / --verdicts / --apply` 互斥组 | 命令解析的唯一位置 | 旧命令没变；`--all --repair` 在此处直接报错 |
| `scripts/pdf_manager.py` · `main()`（[L387](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/pdf_manager.py#L387-L444)） | dispatch 加两个分支，新增 `audit_command`、`repair_command` | 与现有 `index_command` / `check_command` 同构 | 无 |
| `scripts/pdf_library.py` · `write_conversion`（[L359-L384](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/pdf_library.py#L359-L384)） | 加写盘前快照与异常回滚（约 +12 行），**签名不变** | 它是唯一写 `md/` 的地方，回滚只能在这里做 | 正常路径行为完全一致；仅异常路径多一次还原 |
| `scripts/pdf_library.py` · `check_document`（[L343-L356](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/pdf_library.py#L343-L356)） | 加关键字参数 `audit=None`，返回字典追加 `"quality": audit` | `check` 是用户查看单篇状态的入口，体检结果应能从这里取到 | 默认 None，`check` 的现有输出与退出逻辑不变 |
| `scripts/mineru_backend.py` | **零改动** | 它的输入是 ZIP bytes，没有 PDF 路径；文本层依赖不属于解析层 | 无 |
| `references/tag-noise.md`（新增） | R0–R6 全文、白名单策略、`patches.json` / `verdicts.json` / AI 包字段说明、已知但不处理的清单 | SKILL.md 保持入口级长度，细节按现有惯例放 `references/` | 无（新文件） |
| `SKILL.md` · 「根据现状选操作」表 | 加两行：怀疑文本脏 → `audit`；确认要修 → `repair --out` | 用户第一眼是这张表 | 表格变长，旧行不变 |
| `SKILL.md` · 「转换与继续处理」 | 加三句：转换默认体检、修复需显式、`--all` 禁止修复；并指向 `references/tag-noise.md` | 这是转换行为的说明位置 | 纯追加 |
| `SKILL.md` · front matter `description` | **不改** | 改它会影响 skill 的路由与触发面，收益不抵风险 | 无 |
| `tests/test_repair.py`（新增） | 见 §10.7 | 与现有 `tests/test_library.py` 并列 | 无 |
| `resources/papers/CHANGELOG.md` | 落地后追加一条「工具 · PDF 管理 · 体检与可选修复」 | 库日志的既有写法 | 本轮不写（没有代码） |
| `pyproject.toml` / `uv.lock` | **不改** | 依赖保持为空，PyMuPDF 走运行时可选 | 无 |

**向后兼容的四条硬承诺**：

1. 现有 27 篇 MD 一字节不动：体检只读；`--repair` 只作用于本次转换的内存产物；旧 MD 只有显式 `repair --apply` 才会写。
2. 旧命令输出不变：`convert` 的人工行不改格式，体检另起一行；JSON 只增键。
3. `check` 返回值新增 `quality` 键且默认 `None`，现有调用方无感。
4. 资产命名、索引四列、front matter 渲染规则全部不动。

### 10.7 验收与测试

**脚本内置自检**（任一失败即非零退出、不写盘）：

| 自检 | 断言 |
|---|---|
| 行数恒等 | `body.count("\n")` 前后相等 |
| 保护区块哈希 | 每段 `<table>`、`$$`、围栏、算法块、图片行的字节 SHA 不变 |
| 白名单计数 | 每条真上标出现次数前后相等（Mem0 为 6 条） |
| 幂等（plan） | 同输入两次 `build_plan`，`patches.json` 字节相同 |
| 幂等（apply） | 对已修文件再 apply，`0 applied`，md 字节不变，退出码 0 |
| dry-run 默认 | 无 `--apply` 时 `md/` 的 SHA 与 mtime 均不变 |
| 写入路径闸 | `--apply` 指向 `assets/`、`pdf/`、库外或软链逃逸 → 非零退出且不写 |
| 依赖缺失 | 屏蔽 `fitz` 后：`repair` 退出码 2 且给安装提示；`audit` 仍输出密度 |
| 批处理闸 | `convert --all --repair` → 立即报错，不发起任何转换 |

**回归语料**（全部用库里现有文件，不新增材料）：

| 文件 | 角色 | 期望 |
|---|---|---|
| [Mem0](file:///d:/workspace/memory/resources/papers/md/arxiv-2504.19413v1.Project.Mem0.md) | 重症 | 体检 48.05/千字、1,166 处跨词标签；plan 4,362 自动项 + 297 AI 词（70 行）；白名单 6 条不变；行数 379 不变 |
| [MemoryArena](file:///d:/workspace/memory/resources/papers/md/arxiv-2602.16313v2.Bench.MemoryArena.md) | 轻度噪声 + 真实上标 | 体检 ≤0.84/千字；真实 `<sup>*</sup> <sup>1</sup>`、`<sup>d+k</sup>` 零误伤；plan 极少或为空 |
| [Memory Workloads](file:///d:/workspace/memory/resources/papers/md/arxiv-2606.06448.Analysis.Memory%20Workloads.md) | 干净件（0 标签） | 体检 0；plan 空；apply 后 md SHA 不变 |
| [Scientific Memory](file:///d:/workspace/memory/resources/papers/md/arxiv-2607.16848.Bench.Scientific%20Memory.md)（可选） | 低密度噪声 + 真实下标 | 体检 0.48/千字；R1 少量命中；行数与保护区块不变 |

测试类名：`LocateProtectedTests`、`RuleMergeTests`、`WhitelistTests`、`IdempotencyTests`、`ApplyPathGuardTests`、`AuditTests`、`RegressionCorpusTests`（后两者读上述现有文件，文件缺失则 skip，不让 CI 依赖论文库）。

### 10.8 判定：值不值得进 skill，以什么形态

**值得，但只能以「能力」形态进入，不能以「默认行为」形态进入。**

- **形态**：体检默认开、修复默认关、`--apply` 再一道显式。三层闸的语义是——能力随时可用，但任何一次改动 4,000 级字符的动作都必须有人点头。
- **成本**：一个约 550 行的新模块、一个 reference 文档、一组测试；不改任何现有函数签名（`write_conversion` 只加内部回滚）。收益：任何新转换件在写盘前就拿到「脏不脏、能自动修多少」。
- **为什么不做成默认修复**：1/27 的命中率意味着 96% 的转换件根本走不到这条路径，默认修复只会增加每次转换的失败面，而收益为零。
- **升级为「修复默认开」的条件**（满足任一，且必须有数据）：
  1. 30 天内新增转换件 ≥2 篇命中块级阈值；
  2. 同一 MinerU 版本连续 3 次转换复现同类噪声；
  3. 自动修在回归语料上连续两次零误伤（正常件零改动、白名单计数不变）。
- **降级/下线**：若 MinerU 侧修好，体检保留（成本近似 0，还能防未来回归），`repair` 子命令可整体移除。

---

## 11. `mineru.cache` 中间缓存：评估与最小形态

**结论：加，但只加最小形态——只存 `raw.zip` + `manifest.json`，写入默认开（仅 `convert` 路径）、读取默认关（`--from-cache` 显式），配一个 `gc`。不存解包产物。**

三个理由：

1. **缓存的价值不是省流量，是「可重放」。** 本轮 `audit` / `repair` 需要的是 `parsed` 的产物，而 `parsed` 只有两条来源：云端重新解析，或把当时的 ZIP 再解一遍。ZIP 一丢，任何重跑都必须重新上云。
2. **ZIP 已经是服务端产物的最小完整单位。** 解包出来的 `full.md`、`content_list*.json`、`layout.json`、`middle.json`、图片，全部能从它确定性再生；单独落盘只会制造第二份真相。
3. **只有 ZIP 层能躲开命名耦合。** 解析结果里的图片名带 `<prefix>-fig3.jpg`，prefix 由当前文件名推导。若缓存「解析结果」，一次 `rename` 就全部失效；缓存 ZIP 则与名称无关。

### 11.1 现状核实：ZIP 在链路里活多久

完整生命周期（全部为代码事实）：

| 步 | 位置 | 发生什么 |
|---|---|---|
| 1 | [`convert_files`](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/mineru_backend.py#L267-L290) | 组装 jobs，向 MinerU 提交解析；参数 `model_version` / `language` / `is_ocr` / `enable_formula` / `enable_table` 从这里发出（[L283-L290](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/mineru_backend.py#L283-L290)） |
| 2 | [`_batch_results`](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/mineru_backend.py#L246-L264) | `state == "done"` 时从 `full_zip_url` 下载，写进 `result["zip_bytes"]`（[L257](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/mineru_backend.py#L257)） |
| 3 | [`_download_zip`](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/mineru_backend.py#L192-L208) | `response.read()` 拿全部 bytes，`is_zipfile` 校验后**原样返回**；整个过程不落盘（[L195-L208](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/mineru_backend.py#L195-L208)） |
| 4 | [`parse_archive`](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/mineru_backend.py#L360-L453) | `ZipFile(BytesIO(payload))`（[L367](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/mineru_backend.py#L367)），随后只读三样东西：`full.md`（[L377](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/mineru_backend.py#L377)）、`content_list.json` / `content_list_v2.json`（[L394-L395](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/mineru_backend.py#L394-L395)）、图片成员（[L396-L403](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/mineru_backend.py#L396-L403)、[L442](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/mineru_backend.py#L442)）；`layout.json` 或 `*_middle.json` **也只用来正则抓 `_version_name`**（[L444-L451](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/mineru_backend.py#L444-L451)） |
| 5 | `parse_archive` 返回 | 只回 `body` / `assets` / `parser` / `warnings`（[L452-L453](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/mineru_backend.py#L452-L453)）。**ZIP 本身不在返回值里** |
| 6 | [`convert_documents`](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/pdf_manager.py#L269-L287) | `result` 是循环内的局部变量；`write_conversion` 之后没有任何人再引用 `result["zip_bytes"]`，函数返回即被回收 |
| 7 | [`write_conversion`](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/pdf_library.py#L359-L384) | 逐张 `atomic_bytes` 写 assets（[L379-L382](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/pdf_library.py#L379-L382)），再 `atomic_text` 写 md（[L383](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/pdf_library.py#L383)） |

因此现在被丢掉的东西，按证据分三类：

- **整个 raw zip**：唯一完整副本，丢掉后无法复原。
- **zip 内被读取但未保留的结构文件**：`content_list.json`、`content_list_v2.json`、`layout.json` / `*_middle.json`（后者只被正则读过一次 `_version_name`）。注意 `middle.json` 里含逐块 bbox 与 span 信息，是**唯一能还原 MinerU 版面判断的物证**，现在读完就扔。
- **zip 内未被读取的成员**：例如服务端可能附带的原件 PDF、未被打包进正文的裁图（`IMAGES` 以外的成员）。这一点不确定，因为 ZIP 被立刻丢弃，事后无法核对——这本身也是保留缓存的理由。

两点需要更正之前的表述：

- **`.rivet_scratch/` 不是「天然为空」，而是「链路从不写它」。** 对整个 skill 目录 grep `rivet_scratch` 为零命中——`pdf_library` / `mineru_backend` / `pdf_manager` 都没有写它的代码。2026-11-02 早间实测 0 条目（§1.4），现在里面只有本次实验的 7 个文件（约 233 KB），属人工产物，不是链路副产物。
- **服务端有缓存，但与本地无关。** [minerU.api.md#L157-L158](file:///d:/workspace/memory/.agents/skills/pdf-manager/references/minerU.api.md#L157-L158) 记录 `no_cache` 与 `cache_tolerance`（默认 900 秒），那是按 **URL 内容** 的服务端缓存；`full_zip_url` 是短期签名链接，既不能当本地缓存，也不能用来重放。

### 11.2 缓存键与失效

```text
key = sha256(pdf_bytes)[:12]
    + model_version            # vlm | pipeline
    + parameters_lang/ocr/formula/table 的有序摘要
    + cache_schema             # 常量，随缓存格式升级而变
```

关于「skill 版本要不要进键」：**不直接把 `skill_version` 放进键，而是用一个语义明确的 `cache_schema` 常量代替。** 原因是第一性的——缓存的内容是「服务端给了什么」，它只受「服务端版本」和「请求参数」影响；skill 的补丁版本（改文案、改一处打印）与 ZIP 内容无关。若把 `skill_version` 放进键，每次改 skill 都会让 27 篇缓存全部作废，而收益为零。反之，一旦缓存**格式**（manifest 字段、目录布局、键算法）变化，就必须升 `cache_schema`，旧条目自然 miss。`skill_version` 只写进 manifest 供排查，不参与命中。

刻意**不放进键**的东西：

| 不放进键 | 为什么 |
|---|---|
| 文件名 / stem | 改名不应导致缓存失效。ZIP 里没有资产名，命名发生在 `parse_archive` 内部 |
| `prefix` | 同上；prefix 由 stem 推导，属下游命名 |
| 时间戳 | 同内容同参数的条目应当命中，与时间无关 |

刻意**必须放进键**的东西，以及对应失效方式：

| 变化 | 键是否变 | 结果 |
|---|---|---|
| PDF 被替换（同文件名不同内容） | 变（`pdf_sha` 不同） | 新条目；旧条目留在磁盘，由 `gc` 处理。**这是最重要的一条**：按文件名做键会让「换了 PDF 却复用旧结果」变成静默错误 |
| 解析器升级（`vlm` → 新模型，或 `_version_name` 变） | 变（`model_version` 或 `cache_schema` 提升） | 新条目；旧条目不再命中 |
| 参数改动（`--lang`、`--ocr`、`--no-formula`、`--no-table`） | 变（参数摘要进键） | 两个条目并存，不覆盖。同一 PDF 用 `en` 和 `ch` 转两次本来就应该有两份结果 |
| 改名 `rename` | 不变 | 命中，资产名由新 prefix 重新生成——这正是不缓存解析结果的原因 |
| 同一 PDF 多个历史版本 | 按 `pdf_sha` 分开 | 并存；`gc --keep-per-pdf 2` 保留最新的两条 |

### 11.3 截留点与写读路径

**截留点：`parse_archive` 成功返回之后、`write_conversion` 之前**（即 [pdf_manager.py#L284](file:///d:/workspace/memory/.agents/skills/pdf-manager/scripts/pdf_manager.py#L284) 之前）。理由：

- **不缓坏包**：`parse_archive` 失败（空正文、图片缺失、ZIP 结构不对）时不写缓存，保证缓存里每一份都是「曾被成功解析过」的包。
- **不改网络层职责**：`mineru_backend` 是纯取回+纯解析，不在其中写盘；写缓存属于编排层（`convert_documents`）的事。
- **不越过写盘点**：一旦 `write_conversion` 抛出，本次转换失败，此时不写缓存可以把「缓存与 md 不一致」的概率压到 0。

目录与条目：

```text
<root>/.mineru-cache/
  index.json                    # 所有条目的轻量索引（键 → 目录名、大小、last_used_at）
  <key>/raw.zip                 # 服务端原样包
  <key>/manifest.json           # 见下
```

选 `<root>/.mineru-cache/`（即 `resources/papers/.mineru-cache/`）而不是仓库顶层的 `mineru.cache/`：`root` 是「这一批资料」的边界，`--root` 已经决定了所有路径；缓存随 root 走，换一个资料库不会串用；仓库顶层也不会凭空多出一个与 `resources/` 平级的运行时目录。

`manifest.json` 字段：

```json
{"cache_schema": 1,
 "key": "3fa2c81b7d40-vlm-en-fft",
 "pdf_sha256": "…", "pdf_name": "arxiv-2504.19413v1.Project.Mem0.pdf",
 "zip_sha256": "…", "zip_bytes": 1310720,
 "model_version": "vlm", "parameters": {"lang": "en", "ocr": false,
   "formula": true, "table": true},
 "parser": "mineru-cloud 3.4.4",
 "batch_id": "4c1d18e9", "created_at": "2026-11-02T09:12:44+08:00",
 "source": "cloud", "skill_version": "0.1.0"}
```

写入用现有的 `atomic_bytes`（tempfile + `os.replace`），条目目录名即键，天然幂等：重复写同一键只是覆盖同一份内容。

与现有约定的共处：

- **`.gitignore`**：需要新增一行 `/resources/papers/.mineru-cache/`。现状的 `.gitignore` 只排除了 `pdf/`、`md/`、`assets/`、`logs/`（[.gitignore](file:///d:/workspace/memory/.gitignore)），`.rivet_scratch/` 也没被忽略（`git status` 里是 `??`）。所以「放进 `.rivet_scratch/`」会让每次转换都冒出一堆未跟踪文件，不合适。
- **`CHANGELOG.md`**：缓存是运行时派生物，不逐条记。只在「引入缓存能力」「键格式升级」「目录迁移」时记一条；这与该文件「记多了什么、改了什么，不重复索引数据」的定位一致。
- **`check` 不读缓存**：缓存不是资料，`check_document` 的完成度判断仍只看 `pdf` / `md` / `assets`。

### 11.4 收益量化（基于现有 27 篇实测）

先给磁盘实测量（本次统计）：

| 项 | 数量 | 总量 | 单位 |
|---|---:|---:|---:|
| PDF | 27 | 86.3 MB | 均 3.2 MB |
| MD | 27 | 3.51 MB | 均 133 KB |
| assets（719 个图） | 719 | 51.5 MB | 均 73 KB |
| Mem0 单篇 | — | PDF 1.09 MB / MD 157 KB / 7 张资产 0.58 MB | — |

`raw.zip` 的量级估算（ZIP 内同一批 JPEG 基本不可再压，所以按「图片 + 正文 + JSON」粗算）：

| 假说 | 算式 | 全库 | Mem0 |
|---|---|---:|---:|
| 下界（JSON 0.2–0.5 MB/篇） | 51.5 + 3.5 + 27×0.2–0.5 | **60–70 MB** | 0.9–1.3 MB |
| 上界（`middle.json` 2–3 MB/篇） | 51.5 + 3.5 + 27×2–3 | **110–135 MB** | 2.9–4.0 MB |
| 若 ZIP 还打包原件 PDF | 上式 + 86.3 | **146–221 MB** | +1.09 |

时间差（本地实测 + 合理推算）：

| 动作 | 本地 | 云端 |
|---|---|---|
| 体检（纯正则，[实测]） | **0.002 s / 篇** | — |
| PyMuPDF 全文 23 页（[实测]） | **0.144 s** | — |
| 5 个短语 × 23 页 `search_for`（[实测]） | **0.125 s** | — |
| 解 ZIP + `parse_archive` 重放（估） | 0.1–0.5 s | — |
| `repair` 出计划（4,362 条 + 85 行对齐，估） | 2–8 s | — |
| 完整转换（提交 + 轮询，`timeout` 默认 1800 s） | — | 分钟级，批量更久 |

结论：**重放比重新转换快 2–3 个数量级**，但绝对值上，本地重放也就「秒级」。所以缓存省下的不是「一次修复的时间」，而是**反复调规则时的迭代成本**：每改一次阈值或白名单，没有 ZIP 就要重新上云一次，有 ZIP 则是秒级重跑几十次。

**代价也算清楚**：最多 221 MB 磁盘、约 120 行代码、一个 `.gitignore` 行、一个 manifest schema。以「一次重转就要几分钟、还可能排到队列后面」来看，这个代价是合理的。

### 11.5 风险与硬规矩

| 风险 | 会发生什么 | 硬规矩 |
|---|---|---|
| 陈旧缓存被当真相 | 用旧 ZIP 生成新 md，且没人发现 | 读缓存前校验 `manifest.zip_sha256` 与文件实算一致、`pdf_sha256` 与当前 PDF 一致；任一不符 → **拒绝该条目并告警**，不静默降级为「用旧的」 |
| 键漏了版本 | 解析器升级后仍命中旧结果 | `cache_schema` 常量 + `model_version` + 参数摘要三者强制进键；格式一改就升 schema，旧键自然 miss |
| 磁盘无界增长 | 长时间迭代后目录膨胀 | `gc --max-size`（默认 300 MB）+ `--keep-per-pdf`（默认 2 条）+ LRU 按 `last_used_at`；`gc` 只删缓存，不碰 `md/`、`assets/`、`pdf/` |
| 缓存与 `md/` 不一致 | 缓存说一套、md 是另一套 | **缓存永不写回 `md/`**。缓存只喂 `convert` 的 `parsed`；`repair` 的输入是 md + PDF 文本层，与缓存无关 |
| 不同步/并发写入 | 半截 ZIP | 复用 `atomic_bytes`；条目目录以键命名，写入幂等 |
| 跨机器 / 协作不可移植 | 换机后命中不到 | 缓存不入库、不进 git、manifest 标 `source: cloud`；换机自然 miss，这是预期行为而不是故障 |
| 缓存被误当「资料」引用 | 有人把缓存当证据 | `SKILL.md` 与 `references` 写明：缓存是派生物，引用仍指向 PDF 与 `md/` |

还有一条容易被忽略的：**缓存不能成为 `convert` 的默认输入。** 默认转换必须打云端，否则「缓存里有什么，就永远转出什么」，解析器升级永远生效不了。所以 `--from-cache` 必须显式，且路径上要打印一行 `[stem] 命中缓存 <key>`，让用户知道这次没有真的转。

### 11.6 与体检 / 修复的依赖顺序

**缓存 → 体检 → 修复** 是错误顺序；正确的关系是 **体检 → 修复 → 缓存（可选）**。

| 能力 | 需要什么 | 与缓存的关系 |
|---|---|---|
| `audit` | 只有 md 文本 | **零依赖**。实测 0.002 s/篇，不需要 ZIP，也不需要 PyMuPDF |
| `repair` | md + PDF 文本层 | 不需要 ZIP。两阶段**默认只读本地**，绝不触发云端；缺 PyMuPDF 就拒绝，而不是偷偷去转 |
| `cache` | 一次成功解析的 ZIP | 只服务 `convert` 的重放，不参与修复判定 |

理由：`repair` 的输入是「MinerU 的文本 + PDF 的字符真值」，这两样都在本地；缓存解决的是「没有 ZIP 时无法重跑 parse」的问题，而当前场景（1/27、重转已证伪）并没有这个需求——重跑 parse 只是为了改规则时快速看结果。

**唯一需要缓存的场合**：反复调 §9.3 的规则或白名单。此时秒级重放 vs 分钟级重上云，差别是「一天能试 20 次」还是「一天试 2 次」。

### 11.7 最终判断

**加。最小可行形态就是「只存 raw.zip + manifest.json」。**

- **够不够**：够。ZIP 是服务端产物的最小完整单位，`content_list*.json` / `middle.json` / 图片 / `full.md` 全部可从它确定性再生；单存解析结果反而把 `prefix` 与算法版本绑死（改名即失效、规则一改全废）。
- **升级为「完整缓存」（单独解包中间 JSON 与图片原件）的条件**，三条都不成立就不做：
  1. ZIP 解压成为瓶颈（实测重放在 0.5 s 内，未达）；
  2. 需要跨机器共享同一份解析结果且网络不可用；
  3. 需要拿中间 JSON 做内容级对账（当前 §9 只做字符级对账，不需要）。
- **落地成本**：约 120 行（`write_entry` / `read_entry` / `gc`）+ 3 个参数（`--from-cache`、`--no-cache-write`、`gc --max-size`）+ 1 行 `.gitignore` + 1 个 manifest schema。相对 §10 的改造，这是个小增量。
- **前置条件**：先落 §10 的 `audit`。因为 `audit` 零依赖、能立刻回答「这篇脏不脏」；缓存只有在确认「需要反复重放」之后才有价值。反过来说，如果 §10 的 `repair` 最终证明规则稳定、不再迭代，那么缓存可以不做——这正是把它排在最后的原因。
