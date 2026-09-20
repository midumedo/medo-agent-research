# domain/ · 主题综合

这里按领域主题组织连贯的综合认识，解释概念、机制、选择条件与分歧之间的关系。主题可以接近未来一章或一组章节的尺度，但不绑定教材顺序，也不要求所有结论已经得到实验验证。

## 已有主题

### [Agent 的持续运行：Harness、Context 与 Memory](agent-runtime/index.md)

首个暂定综合，2026-09-20。沿一次持续任务解释目标、状态、一次调用的输入、工具行动、反馈、记忆更新与恢复如何连接。依据包括已有问题研究、官方工程文档和明确标注的构造案例；尚无本项目的完整实现复现或模型行为实验。

- [状态与上下文](agent-runtime/state-and-context.md)：系统拥有的信息、一次调用可见的信息与外部世界怎样区分。
- [记忆生命周期](agent-runtime/memory-lifecycle.md)：形成、读取、修正、失效和跨任务复用怎样贯穿运行。
- [失效定位](agent-runtime/failure-modes.md)：从错误行动反查信息、模型能力、执行与恢复问题。

上述补充属于同一个研究主题，可以独立深入，也共同支撑主文。它们不预设为教材第二、三、四章。未来教学组织见 [章节设计提案](../analysis/book-design.md)。

## 研究依据与后续修订

[概念草稿](../analysis/concepts-and-boundaries.md)、[留存分析](../analysis/context-retention.md)、[研究议程](../analysis/research-agenda.md)和[对象探索](../deepdive/README.md)继续维护各自问题与材料。新的实现或反例可以改写本主题；不为保住流程图而把所有系统归入固定阶段。具体归属见 [CONVENTIONS](../CONVENTIONS.md)。
