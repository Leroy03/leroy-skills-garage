# DevFlow Run Tooling

`scripts/devflow.py` 为 `devflow-marshal` 提供最小可用的 run 管理能力，用于在 `🟡/🔴` 流程下维护状态与文书。

## 支持命令

- `python .\scripts\devflow.py create-run --project <project> --topic <topic>`
- `python .\scripts\devflow.py get-run --run-id <run_id>`
- `Get-Content <file> | python .\scripts\devflow.py write-artifact --run-id <run_id> --artifact <plan|review|dispatch|delivery|postmortem>`
- `python .\scripts\devflow.py update-status --run-id <run_id> --status <status> --actor <actor> --note "<note>"`
- `python .\scripts\devflow.py validate-run --run-id <run_id>`

## 默认目录

- 若未设置 `DEVFLOW_ROOT`，默认输出到 `.\devflow\`
- 每个 run 目录包含：
  - `run.json`
  - `run.json.audit`
  - `01_plan.md`
  - `02_review.md`
  - `03_dispatch.md`
  - `04_delivery.md`
  - `05_postmortem.md`

## 使用建议

- `🟡` 只要求最小文书：`run.json`、`run.json.audit`、`01_plan.md`、`02_review.md`
- `🔴` 使用全套文书并完整流转状态机
- 若脚本不可用，应退回逻辑协议模式，并明确说明未执行脚本
