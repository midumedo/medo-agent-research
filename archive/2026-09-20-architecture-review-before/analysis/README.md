# analysis/ · 我们对外部系统的拆解

这里装的是**完整推演**——一次拆解从头到尾的论证过程。

结论在 `understanding/`，支撑某条论断的摘录在 `evidence/`，原始材料在 `sources/`。**三层不互相复制。**

---

## 只有 5 分钟

读 [claude-code/context-management-offload.md](claude-code/context-management-offload.md)。

它是目前唯一撞出结构性结论的一篇：**官方给的所有减负手段，没有一条是在说「怎么压得更好」**——前六条都是让信息别进来，只有压缩是在信息已进入后做减法，而且排在清单最后。

---

## 已拆的

| 文件 | 一句话 | 撞出了什么 |
|---|---|---|
| [claude-code/context-management-offload.md](claude-code/context-management-offload.md) | 卸荷 vs 压缩：官方减负清单的真实结构 | **卸荷不属于六段循环任何一段** → 骨架可能是守门机制（默认拒绝），不是流水线（默认放行） |
| [claude-code/context-economics-two-traps.md](claude-code/context-economics-two-traps.md) | 50 倍价差与两处地雷 | 第一原理从「Context 是预算」升级为「**是按轮次计息的负债**」 |

两篇都出自 Claude Code。它是主锚点——六段循环每一段在它身上都有落点。

---

## 想拆新的

先看 `THESIS.md` 的「已知最可疑的一段」，找能撞它的角度。**别拆没有撞击目标的系统**——那只会产出一份没有判断力的说明书。

拆解的形状是三段式：头（来源与可信度）/ 中（判断优先于陈述）/ 尾（拿去撞主线）。细节见 `project-maintenance` skill。

拆完之后：结论进 `understanding/systems.md`，摘录进 `evidence/understanding/`，**这里不回头改。**
