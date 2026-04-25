---
name: devflow-marshal
description: >-
  DevFlow Marshal governance skill for software delivery.
  Enforces four-level triage (⚪/🟢/🟡/🔴), state machine, review gates,
  and artifact discipline with minimal viable process.
  Use when user asks workflow governance, 走流程, 立案, 正式, 归档,
  run tracking, or formal review/dispatch/delivery/postmortem control.
---

# DevFlow Marshal（技能入口）

主协议文件：`inject/devflow-marshal-context.md`

## 使用规则

- 触发条件：用户提到流程治理、分级流转、立案/归档、门下省审查、run 管理，或显式 @`devflow-marshal`。
- 首动作：每个请求先分级（`⚪/🟢/🟡/🔴`），并先用一句话宣布等级。
- 强制升级：用户若说 `正式/归档/立案/走流程`，必须按 `🔴`。
- 用户异议：若用户对等级有异议，立即上调，不争辩。

## 协议对齐

- `⚪/🟢`：直接处理，默认不要求文书。
- `🟡`：最小文书路径，且在 `Reviewed=Approved` 停止，除非用户明确说 `继续` 或 `归档`。
- `🔴`：全路径文书与状态机流转。

## 硬约束

- `🟡/🔴` 未通过门下省硬审（PASS）前，不得进入执行。
- run 的每次状态变化必须写入 `run.json.audit`。
- 若脚本系统不可用，必须明示并进入逻辑协议模式；不得伪造“已执行脚本”。

## 可选脚本（本仓库）

若当前工作区含 `scripts/devflow.py`，优先用它维护 `DEVFLOW_ROOT` 下的 `run.json` / `run.json.audit` 与文书文件名；说明见仓库根目录 `docs/devflow-run-tooling.md`。当前仓库的职责映射见 `docs/devflow-marshal-subagent-scope.md`。

## 输出压缩

- 长流程只汇报：当前等级、run_id、状态、本轮变更文书、门下省结论、下一步。
- 不重复未变化历史；必要时切换 condensed governance mode。

## 协作原则

- 在治理协议内，始终遵循最小可行改动与可验证交付。
- 流程服务于正确性与交付，不做仪式化膨胀。
