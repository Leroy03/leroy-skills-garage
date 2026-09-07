---
name: devflow-marshal
description: 執行專案指定的 L2/L3 審議、run 狀態、證據契約與封存門禁。適用正式治理、立案、走流程、發布或封存控制；日常問答和小修不啟動狀態機。
---


# DevFlow 治理

先讀專案 AGENTS.md 的等級、停點與既有 change/run。L0 直接答覆；L1 最小修改與直接驗證；L2 規劃／審議後停 Reviewed=Approved，除非使用者已明確批准繼續；L3 按專案完整狀態機。不要因一句日常「整理」或多個檔案就自動升為正式流程。

實作前需要審议的任務，先確認目標可驗收、範圍、依賴、風險／回滾、產物順序與最小方案，記錄 PASS/FAIL。既有批准可承接，不要求重複確認。規劃批准不證明 Runtime 完成。

依當前階段讀取：
- 建立／推進 run：讀 [狀態與工具](references/state-and-tools.md)。
- Reviewed／交付前契約、封存：讀 [契約與封存](references/contracts-and-archive.md)。

不必為角色名稱建立多個代理。需要獨立審查且環境允許時，可委派有界的評審；保留產物與來源。通用搜尋與工具選擇使用當前可用能力，不強制不存在的 provider registry。

## Contract
- inputs_required: level、project_rules、change_id、run_context。
- outputs_required: run_id、change_id、status、gate_decision、artifact_links、next_step。
- evidence_files: 專案要求的 run.json、run.json.audit、規劃文件及 gate reports；不能用空模板冒充執行證據。
