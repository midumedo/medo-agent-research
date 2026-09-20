<a id="correction-2026-09-20"></a>

> **更正 · 2026-09-20：以下旧记录已撤回作为外部证据的资格。** 旧记录把文档排列顺序、我方解释与未经核实的产品行为混在一起；它不能证明“官方默认采用自己认为较差的策略”。本轮未联网核验官方文档，原始 URL、版本与完整快照仍缺失。
>
> **当前判断**：清单顺序不构成优劣排序；设置项存在不证明自动选择不可能；“绝大多数用户不配置”没有观测依据。前置减负与压缩应按任务效用、全路径成本和恢复能力有条件比较，见[修订后的分析](../../analysis/claude-code/context-management-offload.md)。
>
> 下文保留原样，仅用于追溯已发生的推断错误，不得摘成已确认事实。[更正前快照](../../archive/2026-09-20-architecture-review-before/evidence/domain/claude-code-default-strategy.md)可恢复旧版。

本次更正撤销的是原记录的证明力，不是宣称相反的产品行为已被证实。后续取得官方原文或实际观察时，应形成新的证据记录。

---


# 证据：默认策略恰好是官方自己认为较差的那条

支撑 `domain/systems.md` 中 Claude Code 那一行。

---

## 一、官方减负清单的顺序

来源：官方 Reduce token usage 文档（一手）。按文档原序列出：

| 手段 | 作用点在哪个环节 |
|---|---|
| PreToolUse Hook 预处理工具输出 | 工具结果**进入之前** |
| Subagent 委托 | 独立上下文 |
| MCP 工具定义延迟加载 | 系统提示 |
| Skill 按需加载 | 指令 |
| code intelligence 插件 | 检索精度 |
| AGENTS.md 保持精简 | 常驻层 |
| **auto-compact / `/compact`** | **已经进来之后** |

压缩排在最末，而且是唯一作用于「信息已经进入上下文之后」的手段。其余六条都是让信息别进来。

## 二、官方对压缩成本的表述

> *"compacting a large context is itself a large request"*

压缩之前，得先把整段待压缩内容再读一遍。卸荷不付这笔钱。

## 三、旋钮默认是空的

官方给了四级压缩控制粒度：

```
自动触发     auto-compact window 达到阈值
手动触发     /compact
带焦点       /compact Focus on code samples and API usage
永久定制     AGENTS.md 里写 `# Compact instructions`
```

后两级的存在等于公开承认「什么值得留下来」不可判定。但旋钮默认是空的——绝大多数用户不会去写
`# Compact instructions`，于是拿到的就是那套谁也没定制过的通用策略。

**结论**：默认行为（自动压缩）恰好是官方自己排在清单最后、且明确说它成本高的那个策略；
而它认为更好的策略（卸荷）需要用户先跨过一道配置门槛。

---

完整推演见 `analysis/claude-code/context-management-offload.md`。
