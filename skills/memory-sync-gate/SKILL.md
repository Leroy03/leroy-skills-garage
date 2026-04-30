---
name: memory-sync-gate
description: 交付與封存前的沉澱門禁，驗證決策與證據是否完整可追溯。
---

# memory-sync-gate

## 何時使用
- Delivered 到 Archived 前。
- 重大改動或正式流程封存前。

## 輸入
- `run_id`
- `delivery_artifacts`
- `evidence_files`

## 輸出
- `memory_summary.md`（必須）
- `decision_log.md`（必須）
- `memory_index.json`（必須）

## 執行步驟
1. 檢查必要沉澱文檔是否存在。
2. 整理決策、改動、驗證證據、風險與回滾。
3. 更新索引並輸出封存所需資料。

## 門禁規則
- 任一必需沉澱檔缺失則 gate fail。

## 命令映射
- 當前由 skill 直接執行檢查，後續可擴充 `devflow.py validate-memory-gate`。

## Contract

- `inputs_required`
  - `run_id`
  - `delivery_artifacts`
  - `evidence_files`
- `outputs_required`
  - `memory_summary.md`
  - `decision_log.md`
  - `memory_index.json`
- `evidence_files`
  - `04_delivery.md`
  - `gate_reports/*.json`

## Fallback

- 若封存資料缺失：輸出 `gate fail` 並附缺失清單，不進入 Archived。

## Handoff

- 通過後交接：`permanent-memory` 或 `DevFlow Marshal` 進行封存狀態流轉。
