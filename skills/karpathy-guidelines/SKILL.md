---
name: "karpathy-guidelines"
description: "Applies anti-overengineering and anti-assumption guardrails. Invoke before coding, debugging, optimization, or review when you need simpler and safer execution."
---

# Karpathy Guidelines（执行护栏）

## 目标
把高频但容易被忽略的执行约束前置，减少乱猜、过度设计、越界修改和“自以为完成”。

## 四条核心原则

### 1. Think Before Coding
- 不要默默假设
- 有歧义时给出 2~3 种解释，不要静默选一种
- 如果更简单的路存在，要明确指出
- 真不清楚就停下并提问

### 2. Simplicity First
- 只做当前问题需要的最小实现
- 不为单次使用抽象
- 不补未来也许会用到的配置化
- 不为不可能场景堆复杂异常处理

### 3. Surgical Changes
- 只改和需求直接相关的代码
- 不顺手重构、整理、改注释、改格式
- 只清理“本次改动造成”的废代码
- 看到旧问题可以指出，但不默认顺手改

### 4. Goal-Driven Execution
- 把任务改写成可验证目标
- 修 Bug：先有复现，再修复，再验证
- 做功能：先定义验收，再实现，再验证
- 做重构：先保护现有行为，再收敛改动

## 何时调用
- 编码前
- Debug 前
- 优化/重构前
- 代码评审前，作为“是否过度工程化”的检查尺

## 输出要求
- `assumptions`
- `simplest_viable_path`
- `scope_guardrails`
- `verification_goal`

## 与本仓库的关系
- `entry-router` 负责决定要不要进流程
- `karpathy-guidelines` 负责确保进入流程后不失控
- `DevFlow Marshal` 负责在 `🟡/🔴` 场景下补治理与门禁

## 调用方式
- `$karpathy-guidelines` + 任务描述
