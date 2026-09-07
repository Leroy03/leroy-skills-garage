# 現行路由契約調整

- workflow-composition：不再要求先讀 entry-router；仍遵循專案審議與 change 門禁。
- capability-routing：由選定 workflow 宣告能力需求，必要時使用既有 CLI 選擇 provider；刪除 capability-router 技能的強制依賴。
- 一般任務直接使用工具。工作流、能力 CLI 與正式狀態機的資料格式維持相容。
