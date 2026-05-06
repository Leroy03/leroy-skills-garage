---
name: "dev-flow-orchestrator"
description: "Designs end-to-end development workflow from requirement to post-release. Invoke when需要全流程编排或跨阶段协同。"
---

# Dev Flow Orchestrator (Merged Policy)

## Role Boundary

- 负责：需求->方案->开发->测试->发布->复盘 的全流程编排。
- 不负责：单次交付清单细节（交给 `delivery-tracker`）。

## Invoke When

- 用户要求“端到端流程/跨团队协同/全链路计划”
- 任务涉及多个阶段、多个角色、多个依赖

## Required Output

- `workflow_map`（阶段、责任、输入输出）
- `stage_gates`
- `handoff_contracts`
- `escalation_and_rollback`

## Rule

- 每个阶段必须有明确完成条件。
- 每个移交点必须有产物定义与责任人。


## Contract

- `inputs_required`
  - 目标与范围
  - 涉及阶段、角色、依赖与风险
  - 预期交付与成功标准
- `outputs_required`
  - `workflow_map`
  - `stage_gates`
  - `handoff_contracts`
  - `escalation_and_rollback`
- `evidence_files`
  - `01_plan.md`（L2/L3）
  - `03_dispatch.md`（L3）

## Fallback

- 范围不清时，先输出阶段假设与待确认问题，不直接进入执行编排。
- 若治理要求不足，回交 `entry-router` 重新分级。

## Handoff

- L2 默认交接到 `task-planner` 与 `context-builder`。
- L3 默认交接到 `DevFlow Marshal` 按状态机推进。
