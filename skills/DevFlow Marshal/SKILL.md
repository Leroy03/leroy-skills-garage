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
- 首动作：若尚未分流，先经 `entry-router` 判断等级；跨模型协作时优先同时给出 `L0-L3` 与 `⚪/🟢/🟡/🔴`；进入治理后仍需先用一句话宣布等级。
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

## 可选脚本（优先级与回退）

- 优先级 1：若当前工作区含 `scripts/devflow.py`，优先使用项目脚本维护 `DEVFLOW_ROOT` 下的 `run.json` / `run.json.audit` 与文书文件名。
- 优先级 2：若工作区缺失项目脚本，允许回退使用全局脚本 `C:/Users/cllin/.codex/scripts/devflow.py`，并在回报中明确标注“使用全局脚本回退模式”。
- 新项目建议：首次启用时将全局脚本复制到项目 `scripts/devflow.py`，再切回优先级 1，以避免跨项目路径耦合。

## 全局 DevFlow 命令（新增）

- 项目初始化：
  - `init-project`：初始化 `devflow.project.yaml` 与模板文书
  - `sync-project`：同步 schema 版本并补齐缺失字段
- 证据与契约：
  - `collect-evidence`：执行测试命令并生成 `test_result.json`
  - `validate-skill-contract`：校验 skill 输出 contract（输入/输出/证据）

## 轻量可观测（新增）

- 事件日志：关键命令追加 `event.jsonl`（start/success/fail、产物路径、失败计数）
- 门禁报告：`validate-run` 与 `validate-skill-contract` 生成 `gate_reports/*.json`（并保留 `gate_report.json` 兼容指针）
- 目标：在不增加流程复杂度前提下，提升可追溯与复盘效率

## Contract

- `inputs_required`
  - `grade_or_level`
  - `run_context`
  - `governance_intent`
- `outputs_required`
  - `run_id`
  - `status`
  - `current_artifacts`
  - `gate_decision`
  - `next_step`
- `evidence_files`
  - `run.json`
  - `run.json.audit`
  - `gate_reports/*.json`

## Fallback

- 若脚本不可用：明确声明并进入逻辑协议模式，不伪造执行结果。
- 若门禁失败：回退到 `Planned` 或上一可执行状态并附返工项。

## Handoff

- 规划阶段：交接 `task-planner`
- 执行与质量阶段：交接 `test-evidence-packager`、`skill-contract-checker`
- 封存阶段：交接 `memory-sync-gate`

说明见仓库根目录 `docs/devflow-run-tooling.md`。当前仓库的职责映射见 `docs/devflow-marshal-subagent-scope.md`。

## 输出压缩

- 长流程只汇报：当前等级、run_id、状态、本轮变更文书、门下省结论、下一步。
- 不重复未变化历史；必要时切换 condensed governance mode。

## 协作原则

- 在治理协议内，始终遵循最小可行改动与可验证交付。
- 流程服务于正确性与交付，不做仪式化膨胀。

## Frontend 路由一致性（与 entry-router 对齐）

- 若交付物是产品 UI（网站、落地页、后台、组件、应用页面、交互界面），优先路由 `frontend-design`。
- 若交付物是演示文稿（多页 slides、演讲稿、Pitch deck、PPT/PPTX 转 HTML、现有 deck 增强），优先路由 `frontend-slides`。
- 若请求同时包含产品 UI 与简报 deck，必须拆分为两个子任务并分别路由执行，避免单 skill 混跑。
- 若用户语义不清，仅提“前端展示”，先澄清最终交付物；若语境为演讲/汇报，默认优先 `frontend-slides`。
