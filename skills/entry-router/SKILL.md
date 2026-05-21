---
name: "entry-router"
description: "Routes incoming work to the lightest valid workflow. At non-trivial tasks, run grill-lite when unclear, then classify ⚪/🟢/🟡/🔴 and select skills."
---

# Entry Router（入口分流）

## 目标
在任务一开始就判断复杂度、风险与所需流程，避免一上来就走重流程，也避免复杂任务被轻率处理。

## 灵感来源
- 借鉴 `superpowers` 的“先选 workflow，再调 skill”
- 结合本仓库 `DevFlow Marshal` 的 `⚪/🟢/🟡/🔴` 分级
- 吸收 `karpathy` 风格的“先澄清、先降复杂度、先定义验收”

## 何时调用
- 所有非纯闲聊、非一次性问答任务的首个技能
- 用户说“帮我做/修/实现/评审/优化/排查/走流程”时
- 显式调用：`$entry-router`

## 输入
- request：用户诉求
- context：已知限制、风险、时间要求（可选）

## 输出
- `level`：`L0 | L1 | L2 | L3`
- `grade`：`⚪ | 🟢 | 🟡 | 🔴`
- `grade_alias`：`direct | minimal | planned | formal`
- `reasoning`：为什么这样分级
- `recommended_skills`：建议调用链
- `required_checks`：本轮至少要完成的验证或门禁
- `stop_point`：做到哪里就该停下来等确认
- `execution_mode`：`plan_only | execute_after_gate | formal_state_machine`
- `execution_budget`：`tiny | normal | extended`
- `grill_required`：`yes | no`（是否必须先走 `grill-lite`）

## Contract

- `inputs_required`
  - `request`
  - `context`（可选）
- `outputs_required`
  - `level`
  - `grade`
  - `recommended_skills`
  - `required_checks`
  - `stop_point`
  - `grill_required`
- `evidence_files`
  - 无硬性文件（决策型 skill）

## 模型兼容说明
- 对人展示时，保留 `⚪/🟢/🟡/🔴` 与中文层名
- 对模型执行时，优先使用 `L0/L1/L2/L3` 与显式条件判断
- 原因：`Cursor`、`Codex`、`Claude Code` 这类代理更稳定地理解“级别 + 条件”，不太依赖隐喻命名

## 判定轴
- `scope`：只读 | 单文件 | 多文件 | 跨系统
- `risk`：low | medium | high
- `ambiguity`：low | medium | high
- `governance`：none | review_needed | formal_required
- `execution_budget`：tiny | normal | extended
- `agent_budget`：0 | 1 | parallel
- `data_sensitivity`：normal | sensitive
- `destructive_risk`：none | reversible | irreversible

## Step 0：澄清门（优先于分级）

**凡进入本 skill，先按下列规则判断是否 `grill_required=yes`；满足任一即必须先调 `grill-lite`，再回来做 L0-L3 分级。**

### 必触发 `grill-lite`（默认 yes）

- 用户要求实现/修复/重构/优化/新增功能，但未给出可观察验收标准
- 需求含模糊词：`大概`、`尽量`、`看看`、`类似`、`优化一下`、`改好一点`
- `ambiguity` 为 `medium` 或 `high`（默认倾向 `medium`，不要因“写得长”就判 `low`）
- 多文件或跨模块，且未说明 in/out 边界
- 新功能或行为变更，用户未说明「不做什么」
- 用户说「你看着办」「按最佳实践」

### 可跳过 `grill-lite`（`grill_required=no`）

- `L0` 纯问答、解释、对比方案（无改代码）
- 明确单点修复：已给文件路径 + 现象 + 期望结果 + 验证方式
- 用户显式说「不要问，直接做」且风险为 low

### 输出要求

- `grill_required=yes` 时，`recommended_skills` **第一项必须是** `grill-lite`
- 澄清后若 `execution_readiness=blocked`，停止实现，只回报缺失项
- 澄清后若 `partial`，在 `reasoning` 中列出假设清单再继续

## 分级规则

### `L0 / ⚪ 口谕 / direct`
- 适用：解释、问答、文案、极小变更建议
- 默认链路：直接回答，必要时少量只读
- 不启动：文书、run、正式审查

### `L1 / 🟢 快奏 / minimal`
- 适用：单文件、小范围修复、明确实现
- 默认链路：`karpathy-guidelines` -> `knowledge-keeper`（可选） -> `context-builder`（可选） -> `pragmatic-coder` -> `verification-before-completion`
- 个人效率规则：当任务为明确单文件、低风险、低歧义时，可跳过 `karpathy-guidelines`，但不得跳过 `verification-before-completion`
- 停点：验证完成即可

### `L2 / 🟡 常奏 / planned`
- 适用：多文件但边界清楚，有规划/评审需求
- 默认链路：`grill-lite`（若 `grill_required=yes`） -> `karpathy-guidelines` -> `solution-designer`（如需） -> `task-planner` -> `context-builder`（可选） -> `pragmatic-coder` -> `test-evidence-packager` -> `skill-contract-checker` -> `verification-before-completion`
- 测试与证据：默认加入 `test-evidence-packager`，并要求输出 `test_result.json`
- 风险触发：仅在高风险、发布前或跨系统联调时追加 `qa-gatekeeper` 与 `code-reviewer`
- 停点：`Reviewed=Approved`

### `L3 / 🔴 正奏 / formal`
- 适用：正式需求、高风险改动、跨系统、上线/归档/立案
- 默认链路：`DevFlow Marshal` 主导；其余 skills 按阶段调用
- 治理校验：默认加入 `skill-contract-checker` 与 `memory-sync-gate`
- 停点：按治理状态机推进

## 决策规则
- 若 `governance=formal_required`，直接进入 `L3 / 🔴`
- 若任务是纯说明、纯问答、纯建议，进入 `L0 / ⚪`
- 若 `scope=单文件` 且 `risk=low` 且 `ambiguity=low`，进入 `L1 / 🟢`
- 若涉及多文件、需轻规划、需评审或风险中等，进入 `L2 / 🟡`
- 若用户只要求方案/评估/拆解，`execution_mode=plan_only`
- 若用户明确要求实现、修复或做完，`execution_mode=execute_after_gate`
- 若信息不足且判断卡在 `L1/L2` 之间，默认先按 `L2` 做最小规划
- 若信息不足且用户要求改代码，优先 `grill_required=yes`，不要静默假设后直接实现

## 轻量优先规则
- 若存在 `L1 / 🟢` 可完成路径，不默认升级到 `L2 / 🟡`
- 若用户明确要求正式流程，直接升级 `L3 / 🔴`
- 若信息不足但风险低，先列最小假设再继续
- 若信息不足且风险高，先补澄清，不直接执行
- 若任务为 trivial（明显一行修复、纯文案、无行为改动），可直接按 L1 最小链路执行
- 若任务存在明显不确定性（方案未定/成本未知/依赖未知），先走 Spike 决策再进入实现链路

## 调用方式
- `$entry-router` + 用户需求 +（可选）风险/时限/是否正式

## Fallback

- 信息不足且要改代码时：先 `grill-lite`；仍不足再在 `L1/L2` 间取 `L2` 并标注最小假设。
- 用户对分级有异议时，立即上调，不争辩。

## Handoff

- `L1`：`pragmatic-coder` -> `verification-before-completion`
- `L2`：`task-planner` -> `test-evidence-packager` -> `skill-contract-checker`
- `L3`：`DevFlow Marshal` 主导治理

## 与 DevFlow 命令的衔接（新增）

- 当进入 `L2/L3` 时，建议将关键检查映射到全局 `devflow.py`：
  - `test-evidence-packager` -> `collect-evidence`
  - `skill-contract-checker` -> `validate-skill-contract`
- 输出中建议明确：
  - `required_checks` 是否包含 `test_result.json`
  - `execution_mode` 是 `plan_only` 还是 `execute_after_gate`
  - `stop_point` 前是否必须通过门禁校验

## Spike 调研补位（个人流程缺口）

当需求不清、方案分歧或预估成本不稳定时，先进入轻量 Spike（默认 30-90 分钟）：

- `timebox`：本轮调研时限
- `options`：2-3 个可行方案（含约束）
- `recommendation`：推荐路径与理由
- `stop`：是否进入实现（yes/no）

若 `stop=no`，保持 `execution_mode=plan_only`；若 `stop=yes`，回到分级规则继续执行。

## 依赖变更最小门禁（个人流程缺口）

只要涉及新增/升级依赖，`required_checks` 至少追加：

- `changelog_checked`：已阅读关键变更说明
- `direct_verification`：已执行直接相关验证
- `rollback_note`：已记录回滚方案或降级路径

若改动涉及安全、权限、金流或发布关键链路，自动追加 `code-reviewer` 与 `qa-gatekeeper`。

## Frontend 专项分流

当需求涉及“前端设计/页面产出”时，先按交付物类型分流，避免误用技能：

- 若交付物是**产品界面**（网站、落地页、后台、组件、应用页面、交互界面），路由到 `frontend-design`。
- 若交付物是**演示文稿**（多页 slides、演讲稿、Pitch deck、PPT/PPTX 转 HTML、现有 slide deck 增强），路由到 `frontend-slides`。
- 若需求同时包含两类交付物（例如“先做官网，再做汇报简报”），拆分为两个子任务并分别路由：
  - 子任务 A：`frontend-design`
  - 子任务 B：`frontend-slides`

若用户只说“做一个前端展示”且语义不清，先反问一次确认最终交付物是“产品 UI”还是“简报 deck”；若用户强调“用于演讲/汇报”，默认优先 `frontend-slides`。
