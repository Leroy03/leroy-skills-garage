---
name: "entry-router"
description: "Routes incoming work to the lightest valid workflow. Invoke at the start of non-trivial tasks to classify ⚪/🟢/🟡/🔴 and select the right skills."
---

# Entry Router（入口分流）

## 目标
在任务一开始就判断复杂度、风险与所需流程，避免一上来就走重流程，也避免复杂任务被轻率处理。

## 灵感来源
- 借鉴 `superpowers` 的“先选 workflow，再调 skill”
- 结合本仓库 `DevFlow Marshal` 的 `⚪/🟢/🟡/🔴` 分级
- 吸收 `karpathy` 风格的“先澄清、先降复杂度、先定义验收”

## 何时调用
- 所有非纯闲聊、非一次性问答任务的首个技能
- 用户说“帮我做/修/实现/评审/优化/排查/走流程”时
- 显式调用：`$entry-router`

## 输入
- request：用户诉求
- context：已知限制、风险、时间要求（可选）

## 输出
- `grade`：`⚪ | 🟢 | 🟡 | 🔴`
- `reasoning`：为什么这样分级
- `recommended_skills`：建议调用链
- `required_checks`：本轮至少要完成的验证或门禁
- `stop_point`：做到哪里就该停下来等确认

## 分级规则

### `⚪ 口谕`
- 适用：解释、问答、文案、极小变更建议
- 默认链路：直接回答，必要时少量只读
- 不启动：文书、run、正式审查

### `🟢 快奏`
- 适用：单文件、小范围修复、明确实现
- 默认链路：`karpathy-guidelines` -> `knowledge-keeper`（可选） -> `context-builder`（可选） -> `pragmatic-coder` -> `verification-before-completion`
- 停点：验证完成即可

### `🟡 常奏`
- 适用：多文件但边界清楚，有规划/评审需求
- 默认链路：`karpathy-guidelines` -> `solution-designer`（如需） -> `task-planner` -> `context-builder` -> `pragmatic-coder` -> `code-reviewer` / `qa-gatekeeper` -> `verification-before-completion`
- 停点：`Reviewed=Approved`

### `🔴 正奏`
- 适用：正式需求、高风险改动、跨系统、上线/归档/立案
- 默认链路：`DevFlow Marshal` 主导；其余 skills 按阶段调用
- 停点：按治理状态机推进

## 轻量优先规则
- 若存在 `🟢` 可完成路径，不默认升级到 `🟡`
- 若用户明确要求正式流程，直接升级 `🔴`
- 若信息不足但风险低，先列最小假设再继续
- 若信息不足且风险高，先补澄清，不直接执行

## 调用方式
- `$entry-router` + 用户需求 +（可选）风险/时限/是否正式
