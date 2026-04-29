---
name: "daily-qa-work-summary"
description: "Summarizes today's Q&A and completed work in numbered-title format with sub-bullet logs. Invoke when user asks for daily recap, worklog, or handoff summary."
---

# Daily Q&A Work Summary

## Description

将当天对话与执行工作整理成可复盘、可交接的总结，输出格式固定为“编号标题 + 子条列日志”。

## Usage Scenario

- 用户说“总结今天问答”
- 用户说“整理今天做了什么”
- 需要日报、交接记录、复盘纪要

## Instructions

1. 先汇总当天会话中的用户问题与已完成动作。
2. 过滤掉无关寒暄，保留可执行信息与结果证据。
3. 输出时必须使用“编号标题 + 子条列日志”结构。
4. 标题使用任务化命名，不强制固定栏目名称。
5. 每个编号标题后空一行，再写 `-` 子条列日志。
6. 子条列要写“已完成动作 + 结果”，避免空泛描述。
7. 若当天有代码改动，必须补充“变更文件”与“验证动作”。
8. 输出末尾追加一句：`后续我就按这个“编号标题 + 子条列日志”格式给你输出。`

## Output Template

```markdown
1. 工具文档贴合项目能力

   - 已重写 vector-search 文档，入参/出参与实际代码一致
   - 已明确工具边界与调用场景
   - 已按你要求收敛文档策略并移除不需要的分支文档

2. 单句混合“板块+证券”方案讨论

   - 已给出分流思路：一句话拆 token 后双通道处理
   - 板块语义走向量检索，证券代码走精确解析
   - 已形成可直接落地的最小规则集（含识别模式）

后续我就按这个“编号标题 + 子条列日志”格式给你输出。
```

## Quality Bar

- 结论必须可追溯到当天对话事实。
- 不编造未执行的动作。
- 优先写“结果 + 影响”，其次再写过程。
