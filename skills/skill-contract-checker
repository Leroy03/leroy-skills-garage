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

## 執行步驟
1. 讀取 `devflow.project.yaml` 的 `skill_contract.require_fields`。
2. 逐一檢查每個 skill 的輸出欄位與證據檔。
3. 產生 pass/fail 報告。

## 命令映射
- 主要命令：`validate-skill-contract`
- 參考執行：
  - `python C:/Users/cllin/.codex/scripts/devflow.py validate-skill-contract --project-root <root> --run-id <run_id> --strict`
