# 變更文件

以專案 AGENTS.md 的等級與狀態規則為準。L2/L3 若要求 change-id，使用既有記錄；無相符記錄才建立 changes/<change-id>/。
- proposal.md：問題、可觀察結果、範圍、驗收。
- design.md：選定方案、受影響 owner、相容性、依賴與回滾。
- tasks.md：執行順序、產物與各步驗證，未做的工作保持未完成。
- run 的 01_plan.md 只引用上述正文；不要複製三份內容。

L2 的預設停點是 Reviewed=Approved；使用者已明確批准繼續時，記錄批准後執行，不重問。規劃檢查和 Runtime 測試是不同證據。正式流轉使用可用的 devflow-marshal。
