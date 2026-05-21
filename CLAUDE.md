# CLAUDE.md

本文件提供 Claude/Codex 在本倉庫的最小可執行指引。請先讀 `AGENTS.md`（日常短版），再按需展開到各 `skills/*/SKILL.md`。

## 快速路由

1. 先調 `entry-router`；若 `grill_required=yes`，必先 `grill-lite` 再判定 `L0/L1/L2/L3`。
2. 依分級選鏈路，不要直接跳重流程。
3. 任務完成前必過 `verification-before-completion`（`L0` 除外）。

## 分級速記

- `L0 / ⚪`：問答與輕建議，直接回覆。
- `L1 / 🟢`：單檔低風險，最小改動 + 驗證。
- `L2 / 🟡`：多檔/中風險，需規劃與證據，停於 `Reviewed=Approved`。
- `L3 / 🔴`：正式/歸檔/立案/跨系統高風險，走 `DevFlow Marshal`。

## 常用技能組合

- 功能實作：`grill-lite`（驗收不清時） -> `requirement-analyst` -> `task-planner` -> `pragmatic-coder` -> `verification-before-completion`
- 問題排查：`context-builder` -> `bug-hunter` -> `verification-before-completion`
- 交付前：`test-evidence-packager` -> `qa-gatekeeper`（必要時） -> `delivery-tracker`
- 封存沉澱：`context-archiver` / `permanent-memory` / `memory-sync-gate`（依場景擇一或串接）

## 個人流程缺口補位（必讀）

- **澄清先行**：要改代碼且驗收/邊界不清 -> `grill-lite`（5-8 題），再進實作鏈路。
- **Spike 先行**：方案未定或成本未知時，先輸出 `timebox/options/recommendation/stop`。
- **依賴變更門禁**：新增或升級依賴時，至少補 changelog、直接驗證、回滾說明。
- **記憶分層**：單次摘要用 `context-archiver`，長期事實用 `permanent-memory`，封存前門禁用 `memory-sync-gate`。

## 同步規則

若本文件與 `AGENTS.md` 規則衝突，以更嚴格者優先，並在下次更新時消除差異。
