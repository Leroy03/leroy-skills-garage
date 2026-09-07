---
name: engineering-review
description: 評審指定程式變更、技術方案或產出，提出可定位且有證據的錯誤與風險。適用明確 review／復核或高風險審查；不把每次編碼都升級為正式評審。
---


# 工程評審

先確認受評範圍、基準版本與使用者要「只評審」還是「評審並修正」。只評審不改原件。

逐項連結主張、實際程式／文件、觸發條件與影響；依最可能破壞行為的路徑追查依賴和測試。優先正確性、狀態所有權、相容性與具體安全邊界。效能結論須有量測或可證明的成本來源。

回報可行動的 findings：嚴重程度、檔案位置、觸發情境、影響、最小修正方向與證據。排除只有風格偏好的建議，不湊缺陷數量或 0–100 分數。沒發現問題時直說，附未覆蓋的範圍；不能因此推論所有行為已通過。

方案／文案復核同樣區分事實、推論、建議；來源不足的結論標記待證，不替作者補造證據。

調查卡住或根因未明時才讀 [診斷與效能](references/diagnosis.md)。涉及完成／發布判定時使用實際驗證紀錄；需要結構化交付證據才使用 delivery-evidence。

## Contract
- inputs_required: target_or_diff、constraints、review_scope。
- outputs_required: findings_with_evidence、coverage_limits、recommended_actions。
- evidence_files: 無固定檔案；引用實際 diff、日誌、測試或來源。
