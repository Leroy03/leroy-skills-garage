---
name: entry-router
description: 舊專案規則點名 entry-router 時的相容入口；將既有 L0–L3 分級對應到新技能，不提供額外執行鏈。
---

# 舊入口相容

只有仍引用此名稱的規則需要本入口。依任務範圍、風險與專案門禁選最輕等級：L0 直接答覆；L1 最小實作與直接驗證；L2 規劃及審議；L3 正式治理。

資訊可由檔案／對話取得就直接查證。grill_required 只有在缺口會影響範圍、重要取捨、授權或驗收且無法合理推定時才為 yes；不預設题数。需要規劃時使用 [work-planning](../work-planning/SKILL.md)，正式治理使用 [devflow-marshal](../devflow-marshal/SKILL.md)。不重複載入通用編碼／搜尋技能。

L2 依專案要求停 Reviewed=Approved；已有使用者明確繼續指令時承接批准執行。規劃批准不代表 Runtime 完成。
