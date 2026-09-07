# DevFlow Marshal Subagent Scope

本仓库目前不提供独立的 `devflow-planner`、`devflow-evidence-explorer`、`devflow-critic` 目录型 skill。
对应职责由现有 skills 组合承担：

## 角色映射

- `planner`：`work-planning`
- `evidence-explorer`：直接查現有檔案及使用搜尋工具
- `critic`：`engineering-review`
- `implementer`／`debugger`／`optimizer`：直接使用可用工具實作與診斷
- `delivery`：`delivery-evidence`
- `archivist`：`project-memory`

## 适用原则

- `⚪/🟢`：直接處理，不預設載入技能鏈
- `🟡`：依專案要求規劃審議，承接既有批准並以直接證據驗收
- `🔴`：由 `devflow-marshal` 治理全流程，并按阶段调用上述 skills

## 说明

- 代理分工僅在環境允許、已授權且有可獨立執行的實質工作時使用，不依本表自動分派
- 在新增独立 skill 前，应优先判断现有 skill 组合是否已足够
