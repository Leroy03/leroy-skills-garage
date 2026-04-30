---
name: skill-contract-checker
description: 檢查 skills 執行結果是否符合輸入/輸出/證據 contract。
---

# skill-contract-checker

## 何時使用
- L2/L3 任務 Reviewed 前。
- 多 skill 串接後需驗證交接完整性時。

## 輸入
- `skills_involved`
- `project_root`
- `run_id`（可選）
- `strict_mode`（true/false）

## 輸出
- `contract_report.json`（必須）
- `missing_fields.md`（若 fail）

## Contract

- `inputs_required`
  - `skills_involved`
  - `project_root`
  - `run_id`（L2/L3 建议）
- `outputs_required`
  - `contract_report.json`
  - `gate_reports/validate-skill-contract.json`
- `evidence_files`
  - `contract_report.json`

## 執行步驟
1. 讀取 `devflow.project.yaml` 的 `skill_contract.require_fields`。
2. 逐一檢查每個 skill 的輸出欄位與證據檔。
3. 產生 pass/fail 報告。

## 命令映射
- 主要命令：`validate-skill-contract`
- 參考執行：
  - `python C:/Users/cllin/.codex/scripts/devflow.py validate-skill-contract --project-root <root> --run-id <run_id> --strict`

## Fallback

- 若 contract 文件缺失：先输出缺失清单并阻断进入 `Reviewed`。
- 可选后续能力：增加 `--init-missing` 自动生成模板（当前未实现）。

## Handoff

- `passed`：交接 `verification-before-completion` 或进入状态流转。
- `failed`：回交上游 skill 补齐输入/输出/证据。
