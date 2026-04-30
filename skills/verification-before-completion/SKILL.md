---
name: "verification-before-completion"
description: "Requires evidence before declaring work done. Invoke after implementation, bugfix, or optimization and before claiming completion or delivery."
---

# Verification Before Completion（完成前验证）

## 目标
在“看起来完成了”和“有证据证明完成了”之间加一道轻量但刚性的检查，减少误报完成。

## 灵感来源
- 借鉴 `superpowers` 的 evidence-first / verify-before-claim
- 与本仓库 `qa-gatekeeper`、`delivery-tracker` 形成轻重分层

## 何时调用
- `pragmatic-coder` 改完代码后
- `bug-hunter` 给出修复后
- `code-optimizer` 完成最小优化后
- 提交交付、结束任务、声称“已完成”之前

## 不做
- 不代替完整测试策略
- 不代替发布门禁
- 不替代正式 Code Review

## 最小检查清单
- 改动目标是否有明确验收
- 是否执行了至少一个直接相关验证
- 是否检查了最可能受影响的回归路径
- 是否区分“已验证事实”和“尚未验证假设”

## 输出
- `verification_steps`
- `evidence`
- `residual_risks`
- `completion_decision`：pass | partial | fail

## Contract

- `inputs_required`
  - `change_summary`
  - `validation_results`
  - `expected_acceptance`
- `outputs_required`
  - `verification_steps`
  - `evidence`
  - `residual_risks`
  - `completion_decision`
- `evidence_files`
  - `test_result.json`（L2/L3）
  - `contract_report.json`（L2/L3）

## Fallback

- 若证据不足：输出 `partial`，并明确缺失项与补证步骤。
- 若验证失败：输出 `fail`，并回交 `pragmatic-coder` 修复。

## Handoff

- `pass`：可交付或进入下一治理状态。
- `partial/fail`：回交 `pragmatic-coder`，必要时触发 `qa-gatekeeper`。

## 分级对齐
- `⚪/🟢`：至少给出最小验证证据
- `🟡`：验证结果要能支持进入 `Reviewed`
- `🔴`：验证证据应纳入交付文书

## 调用方式
- `$verification-before-completion` + 改动说明 + 验证结果
