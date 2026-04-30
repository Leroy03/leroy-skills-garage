---
name: regression-matrix-builder
description: 依改動範圍建立回歸測試矩陣，確保核心流程與高風險模組被覆蓋。
---

# regression-matrix-builder

## 何時使用
- 多檔改動、跨模組改動。
- 發版前或 Delivered 前需要回歸盤點時。

## 輸入
- `changed_files`
- `impact_scope`
- `risk_level`
- `existing_test_assets`

## 輸出
- `regression_scope.md`（必須）
- `regression_matrix.json`（可選）

## 執行步驟
1. 依 `changed_files` 歸類核心、邊界、相依影響。
2. 建立測試優先級（P0/P1/P2）。
3. 指派對應測試命令與證據要求。
4. 生成回歸矩陣文檔供測試執行。

## 命令映射
- 當前由 skill 直接產文檔，後續可擴充 `devflow.py build-regression-matrix`。
- 交接給 `test-evidence-packager` 執行收證。

## Contract

- `inputs_required`
  - `changed_files`
  - `impact_scope`
  - `risk_level`
  - `existing_test_assets`
- `outputs_required`
  - `regression_scope.md`
  - `regression_matrix.json`（可選）
- `evidence_files`
  - `regression_scope.md`

## Fallback

- 若改動資訊不足：先輸出最小回歸清單並標註待補項。

## Handoff

- 交接：`test-evidence-packager` 執行測試與證據收集。
