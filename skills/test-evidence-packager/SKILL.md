---
name: test-evidence-packager
description: 全域測試證據打包器。執行專案測試命令並產生標準 test_result.json。
---

# test-evidence-packager

## 何時使用
- L2/L3 任務需提交測試證據時。
- Reviewed 前、Delivered 前需要統一測試輸出格式時。

## 輸入
- `project_root`
- `run_id`（可選）
- `level`（L2/L3）
- `test_scope`（unit/integration/e2e/custom）

## 輸出
- `test_result.json`（必須）
- `regression_scope.md`（若流程要求）
- `coverage_summary.json`（若啟用 coverage）

## Contract

- `inputs_required`
  - `project_root`
  - `level`
  - `run_id`（L2/L3 建议）
- `outputs_required`
  - `test_result.json`
  - `dependency_actions`（记录自动安装行为）
- `evidence_files`
  - `test_result.json`

## 執行步驟
1. 讀取 `devflow.project.yaml` 的 `testing.commands`。
2. 在虛擬環境中執行命令（若未建立，先建立並安裝必要依賴）。
3. 收集 `exit_code`、耗時、`stdout/stderr` 摘要。
4. 產出標準化 `test_result.json`。

## 命令映射
- 主要命令：`collect-evidence`
- 參考執行：
  - `python C:/Users/cllin/.codex/scripts/devflow.py collect-evidence --project-root <root> --run-id <run_id> --level <level>`

## Fallback

- 若缺少测试框架依赖：可启用 `--auto-install-missing` 并使用白名单安装。
- 若命令执行失败：保留失败证据并回交 `pragmatic-coder`。

## Handoff

- 默认交接到：`skill-contract-checker`
