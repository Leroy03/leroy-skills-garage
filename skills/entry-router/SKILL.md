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
- `level`：`L0 | L1 | L2 | L3`
- `grade`：`⚪ | 🟢 | 🟡 | 🔴`
- `grade_alias`：`direct | minimal | planned | formal`
- `reasoning`：为什么这样分级
- `recommended_skills`：建议调用链
- `required_checks`：本轮至少要完成的验证或门禁
- `stop_point`：做到哪里就该停下来等确认

## 模型兼容说明
- 对人展示时，保留 `⚪/🟢/🟡/🔴` 与中文层名
- 对模型执行时，优先使用 `L0/L1/L2/L3` 与显式条件判断
- 原因：`Cursor`、`Codex`、`Claude Code` 这类代理更稳定地理解“级别 + 条件”，不太依赖隐喻命名

## 判定轴
- `scope`：只读 | 单文件 | 多文件 | 跨系统
- `risk`：low | medium | high
- `ambiguity`：low | medium | high
- `governance`：none | review_needed | formal_required

## 分级规则

### `L0 / ⚪ 口谕 / direct`
- 适用：解释、问答、文案、极小变更建议
- 默认链路：直接回答，必要时少量只读
- 不启动：文书、run、正式审查

### `L1 / 🟢 快奏 / minimal`
- 适用：单文件、小范围修复、明确实现
- 默认链路：`karpathy-guidelines` -> `knowledge-keeper`（可选） -> `context-builder`（可选） -> `pragmatic-coder` -> `verification-before-completion`
- 停点：验证完成即可

### `L2 / 🟡 常奏 / planned`
- 适用：多文件但边界清楚，有规划/评审需求
- 默认链路：`karpathy-guidelines` -> `solution-designer`（如需） -> `task-planner` -> `context-builder` -> `pragmatic-coder` -> `code-reviewer` / `qa-gatekeeper` -> `verification-before-completion`
- 停点：`Reviewed=Approved`

### `L3 / 🔴 正奏 / formal`
- 适用：正式需求、高风险改动、跨系统、上线/归档/立案
- 默认链路：`DevFlow Marshal` 主导；其余 skills 按阶段调用
- 停点：按治理状态机推进

## 决策规则
- 若 `governance=formal_required`，直接进入 `L3 / 🔴`
- 若任务是纯说明、纯问答、纯建议，进入 `L0 / ⚪`
- 若 `scope=单文件` 且 `risk=low` 且 `ambiguity=low`，进入 `L1 / 🟢`
- 若涉及多文件、需轻规划、需评审或风险中等，进入 `L2 / 🟡`
- 若信息不足且判断卡在 `L1/L2` 之间，默认先按 `L2` 做最小规划

## 轻量优先规则
- 若存在 `L1 / 🟢` 可完成路径，不默认升级到 `L2 / 🟡`
- 若用户明确要求正式流程，直接升级 `L3 / 🔴`
- 若信息不足但风险低，先列最小假设再继续
- 若信息不足且风险高，先补澄清，不直接执行

## 调用方式
- `$entry-router` + 用户需求 +（可选）风险/时限/是否正式
