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
