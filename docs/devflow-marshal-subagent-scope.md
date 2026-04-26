# DevFlow Marshal Subagent Scope

本仓库目前不提供独立的 `devflow-planner`、`devflow-evidence-explorer`、`devflow-critic` 目录型 skill。
对应职责由现有 skills 组合承担：

## 角色映射

- `planner`：`solution-designer` + `task-planner`
- `evidence-explorer`：`knowledge-keeper` + `context-builder`
- `critic`：`code-reviewer` + `qa-gatekeeper` + `ai-output-auditor`
- `implementer`：`pragmatic-coder`
- `debugger`：`bug-hunter`
- `optimizer`：`code-optimizer`
- `delivery`：`delivery-tracker`
- `archivist`：`context-archiver` + `permanent-memory`

## 适用原则

- `⚪/🟢`：通常只需调用单个执行型 skill，必要时辅以 `context-builder`
- `🟡`：推荐先规划，再补上下文，执行后进入 review / QA gate
- `🔴`：由 `devflow-marshal` 治理全流程，并按阶段调用上述 skills

## 说明

- 如果后续确实要拆出独立 subagent，可沿用此职责边界
- 在新增独立 skill 前，应优先判断现有 skill 组合是否已足够
