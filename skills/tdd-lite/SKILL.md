---
name: "tdd-lite"
description: "Applies lightweight test-first or test-near workflow for risky changes. Invoke when core logic changes need protection without pulling the full process heavier."
---

# TDD Lite（轻量测试先行）

## 目标
在不把流程全面做重的前提下，为高风险改动补上最小测试保护，尤其适合核心逻辑、回归代价高、容易重复出错的场景。

## 设计原则
- 不强制所有任务先写测试
- 只在“测试能明显降低回归风险”时启用
- 优先沿用现有测试框架，不引入新脚手架
- 测试只保护本次要改的行为，不扩张覆盖野心

## 何时调用
- 修复可复现 Bug，且需要防止同类问题再次出现
- 修改核心业务逻辑，回归代价高
- 重构前需要先锁定既有行为
- 用户明确要求 TDD 或先补测试

## 不建议调用
- 文案、配置、一次性脚本、低风险小修
- 改动极小且已有足够人工验证证据
- 测试成本明显高于风险，且任务处于 `⚪`

## 推荐模式

### 模式 A：Test First
- 先写一个会失败的最小测试
- 再做最小修复
- 最后让测试通过并补最小回归说明

### 模式 B：Test Near
- 先明确验收与边界
- 先做最小改动
- 立刻补一条最值钱的保护测试

## 输出
- `test_strategy`
- `target_behaviors`
- `new_or_updated_tests`
- `evidence`
- `residual_risks`

## 分级对齐
- `🟢`：仅在核心逻辑或重复性 Bug 时推荐
- `🟡`：优先考虑用于核心路径与回归保护
- `🔴`：若涉及关键链路，建议纳入门禁证据

## 协作关系
- 与 `karpathy-guidelines` 配合，避免“为了 TDD 而 TDD”
- 与 `pragmatic-coder` 配合，控制实现范围
- 与 `verification-before-completion` 配合，形成证据闭环

## 调用方式
- `$tdd-lite` + 改动目标 + 风险说明 + 当前可用测试框架
