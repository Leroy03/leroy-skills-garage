---
name: "delivery-tracker"
description: "Tracks single delivery readiness with checklist, verification path, and rollback plan. Invoke when准备交付或发布前核对。"
---

# Delivery Tracker (Merged Policy)

## Role Boundary

- 负责：单次交付的清单化跟踪、验收路径、回滚步骤。
- 不负责：端到端研发流程编排（交给 `dev-flow-orchestrator`）。

## Invoke When

- 用户要求“交付清单/上线前检查/回滚准备”
- 需要对当前迭代做最终交付确认

## Required Output

- `delivery_checklist`
- `verification_path`
- `rollback_plan`
- `signoff_status`

## Rule

- 缺少验证证据不得标记完成。
- 回滚触发条件必须明确可执行。
