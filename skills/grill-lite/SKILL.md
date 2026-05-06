---
name: "grill-lite"
description: "轻量澄清提问门：在高歧义任务开始前，通过 5-8 个问题快速对齐目标、范围、验收与停点。"
---

# Grill-Lite（轻量澄清门）

## 目标
在需求描述不完整、验收标准不明确时，用最少问题快速对齐，避免返工与误解后再编码。

## 何时调用
- `entry-router` 判断 `ambiguity=high` 时
- 用户需求少于 3 句但要求直接实现
- 目标、范围、验收、停点任一不清晰时
- 显式调用：`$grill-lite`

## 不做
- 不输出实现代码
- 不代替 `requirement-analyst` 的任务拆解
- 不代替 `task-planner` 的排期和依赖规划

## 输入
- `request`：用户原始诉求
- `known_constraints`：已知约束（可选）

## 输出
- `clarified_requirements`
- `assumptions`
- `open_questions`
- `execution_readiness`：`ready | partial | blocked`
- `recommended_next_step`

## 标准问题模板（5-8 题）
- 目标结果：这次改动“完成”的可观察标准是什么？
- 范围边界：明确不做什么？哪些模块禁止改动？
- 优先级：速度、稳定性、可维护性，当前最优先哪一个？
- 风险容忍：可接受的失败模式是什么？不可接受的是什么？
- 验证方式：需要哪些测试或证据来确认完成？
- 兼容约束：是否有版本、环境、接口兼容要求？
- 交付形式：要方案、直接代码、还是分阶段推进？
- 停点确认：在哪个节点需要你确认（如 `Reviewed=Approved`）？

## 执行规则
- 默认最多提问 8 题，避免把澄清阶段做重。
- 若核心信息已足够，提前结束并标记 `execution_readiness=ready`。
- 若用户无法回答全部问题，输出最小假设清单并标记 `partial`。
- 若缺少关键前置条件（权限/环境/数据），标记 `blocked` 并明确缺失项。

## Contract

- `inputs_required`
  - `request`
- `outputs_required`
  - `clarified_requirements`
  - `execution_readiness`
  - `recommended_next_step`
- `evidence_files`
  - 无硬性文件（决策型 skill）

## Fallback

- 当用户拒绝回答澄清问题时，保留 3 条以内最小假设后继续执行，并在结果中显式标注风险。

## Handoff

- 需求已清晰：交回 `entry-router` 继续分级。
- 需拆解任务：交接 `requirement-analyst` -> `task-planner`。
- 仅需快速实现：交接 `pragmatic-coder` -> `verification-before-completion`。
