---
name: "ai-output-auditor"
description: "Audits AI output for correctness, consistency, and risk. Invoke when需要对方案/代码/文案结果做事实与风险审校。"
---

# AI Output Auditor (Merged Policy)

## Role Boundary

- 负责：正确性、一致性、风险审校；指出证据不足点。
- 不负责：测试覆盖矩阵与发布门禁（交给 `qa-gatekeeper`）。

## Invoke When

- AI 已生成方案/代码/文档，需要审计
- 用户强调“校对、复核、风险检查”

## Required Output

- `audit_summary`
- `issues`（严重级别 + 证据）
- `fix_suggestions`
- `confidence`

## Audit Focus

- 事实错误与逻辑矛盾
- 与项目约束不一致
- 安全/合规/可维护性风险

## Contract

- `inputs_required`
  - `target_output`
  - `reference_constraints`
  - `expected_quality_bar`
- `outputs_required`
  - `audit_summary`
  - `issues`
  - `fix_suggestions`
  - `confidence`
- `evidence_files`
  - 无硬性文件（审校型 skill）

## Fallback

- 若参考依据不足：明确标注低置信度与待补材料，不给绝对结论。

## Handoff

- 发现问题：回交对应生产 skill（如 `solution-designer`、`pragmatic-coder`）。
- 无阻断问题：交接 `verification-before-completion`。
