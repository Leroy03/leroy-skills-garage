# 契約與封存

先讀 devflow.project.yaml 或專案等價設定，確認實際 required fields 與 evidence，不把全域範本當所有專案的強制規格。

若使用現有 validate-skill-contract：run/skill_contract/<skill-name>.json 記錄 inputs_required、outputs_required、evidence_files，填入實際值和路徑；--skill 可重複指定。證據相對路徑通常相對 run，使用前核對工具實作或說明。
```text
PYTHON SCRIPT validate-skill-contract --project-root ROOT --run-id RUN --skill NAME --strict
```
此命令可能只檢查欄位與檔案存在，還須人工／獨立檢查驗收及真實測試結果。空欄位模板、過時結果或未執行命令不構成 PASS。使用 delivery-evidence 整理測試結果，讓 change/run/HEAD/dirty manifest 可追溯。

封存前核對交付、重要決策、驗證、殘餘風險和回滾的來源。若專案要求 memory_summary.md、decision_log.md、memory_index.json 或 changes/<change-id>/delivery.md、archive.md，逐一驗證；未要求時引用既有紀錄即可。長期記憶只收穩定結論，不複製完整規劃正文。必要證據缺失不得進 Archived。
