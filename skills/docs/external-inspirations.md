# External Inspirations

本仓库当前主要吸收了两个外部项目的思路：

- `obra/superpowers`
- `forrestchang/andrej-karpathy-skills`

## 共同点

- 都强调“不要直接冲进实现”，要先澄清任务与成功标准
- 都反对 ad-hoc 工作方式，提倡可复用流程
- 都强调验证优先，不能只凭“感觉做完了”
- 都把复杂度控制视为一等公民

## 主要差异

### Superpowers
- 强在 workflow 编排
- 强在技能触发、TDD、调试、review、并行 agent、branch/worktree 等工程动作
- 适合完整开发流水线
- 风险是照搬后流程容易偏重

### Karpathy Guidelines
- 强在行为约束
- 重点解决：乱猜、过度设计、越界改动、没有成功标准
- 非常轻量，适合做全局默认 guardrails
- 风险是只有约束，没有完整 workflow 编排

## 本仓库的融合策略

### 入口层
- 引入 `entry-router`
- 所有非 trivial 任务先做 `⚪/🟢/🟡/🔴` 分流
- 目标：先选最轻可行流程，而不是默认重治理

### 约束层
- 引入 `karpathy-guidelines`
- 作为实现、调试、评审、优化前的默认护栏
- 目标：减少乱猜、过度工程化与无关改动

### 验证层
- 引入 `verification-before-completion`
- 在声明“完成”前要求最小证据
- 目标：把验证闭环做轻，但不缺席

### 治理层
- 保留 `DevFlow Marshal`
- 只让 `🟡/🔴` 进入明显流程化路径
- 目标：把审计能力集中在高风险场景，而不是污染全部请求

## 不照搬的部分

- 不直接复制 `superpowers` 的全套 slash commands
- 不默认要求 worktree / subagent / TDD 全量流程
- 不把所有实现都强制升级成多阶段审批

## 结果目标

- `⚪/🟢`：像 Karpathy，一样克制、简单、明确
- `🟡/🔴`：借 Superpowers 的 workflow 能力，但由分级控制复杂度
