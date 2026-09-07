# 設計與審議

來源為使用者目錄下 `.codex/AGENTS.md`、`.codex/skills` 的 9 個非系統技能、協作協定、契約模板及精簡注入入口；不複製系統／插件技能、快取或認證狀態。

保留 entry-router/grill-lite 相容名稱，採全局薄入口；其餘舊職責由 work-planning、engineering-review、delivery-evidence、project-memory、devflow-marshal 承接，一般編碼與搜尋直接使用工具。加入全局既有 hatch-pet/quarkclouddrive。

套件／路由只列現存技能，工作流使用合併後技能；驗證器取消全技能強制 Contract/Fallback/Handoff，改查必要 frontmatter、名稱與資源連結。契約門禁依專案與特定工作要求維持。

審議結論：Reviewed=Approved。已查來源、呼叫者與全局相容策略；採直接同步，沒有新增依賴。既有重疊編輯由此次同步取代並先備份；不相關外部靈感及歷史 change 改動留在工作樹，不納入提交。

回滾：提交後使用 git revert；提交前快照在 `C:/Users/ADMINI~1/AppData/Local/Temp/leroy-skills-before-sync-20260907-202651`，含原工作樹與 working-tree.patch。
