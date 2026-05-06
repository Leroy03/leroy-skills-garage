# AGENTS.md（個人日常短版）

目標：先做對，再做快；在最小流程下保持可驗證交付。

## 執行順序
1. 遵循即時指令與限制。
2. 先走 `entry-router` 分級（L0/L1/L2/L3）。
3. 依分級選 skill，避免過度流程化。

## 分級速記
- `L0 / ⚪`：問答/建議，直接回覆。
- `L1 / 🟢`：單檔低風險，最小改動 + 驗證。
- `L2 / 🟡`：多檔或中風險，要規劃與證據，停於 `Reviewed=Approved`。
- `L3 / 🔴`：正式/立案/歸檔/高風險跨系統，交 `DevFlow Marshal`。

## 常用鏈路
- 實作：`requirement-analyst` -> `task-planner` -> `pragmatic-coder` -> `verification-before-completion`
- 排查：`context-builder` -> `bug-hunter` -> `verification-before-completion`
- 發版前：`test-evidence-packager` -> `qa-gatekeeper`（必要時） -> `delivery-tracker`

## 個人缺口補位
- Spike 先行：需求不清先產出 `timebox/options/recommendation/stop`。
- 依賴門禁：新增/升級依賴需 changelog、直接驗證、回滾說明。
- 記憶分層：`context-archiver`（單次）/`permanent-memory`（長期）/`memory-sync-gate`（封存前）。

## 不可省
- 除 `L0` 外，宣告完成前必有驗證證據與 `completion_decision`。
- `AGENTS.md` 與 `CLAUDE.md` 規則需同步，衝突取較嚴者。

## 三省六部速記
- `🟡/🔴`：中書（規劃）-> 門下（審議）-> 尚書（統籌）再執行；`🟡` 停 `Reviewed=Approved`，`🔴` 走完整狀態機。
- 六部按職能分派：分流/上下文、實作/優化、驗證/門禁、交付/沉澱；避免所有任務都走重治理。
