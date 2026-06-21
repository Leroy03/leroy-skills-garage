# DevFlow Run Tooling

`scripts/devflow.py` 为 `devflow-marshal` 提供最小可用的 run 管理能力，用于在 `🟡/🔴` 流程下维护状态与文书。

## 支持命令

- `python .\scripts\devflow.py create-run --project <project> --topic <topic>`
- `python .\scripts\devflow.py get-run --run-id <run_id>`
- `Get-Content <file> | python .\scripts\devflow.py write-artifact --run-id <run_id> --artifact <plan|review|dispatch|delivery|postmortem>`
- `python .\scripts\devflow.py update-status --run-id <run_id> --status <status> --actor <actor> --note "<note>"`
- `python .\scripts\devflow.py validate-run --run-id <run_id>`
- `python .\scripts\devflow.py init-change --change-id <change_id>`
- `python .\scripts\devflow.py validate-change --change-id <change_id>`
- `python .\scripts\devflow.py link-change --run-id <run_id> --change-id <change_id>`
- `python .\scripts\devflow.py archive-change --change-id <change_id>`
- `python .\scripts\devflow.py sync-spec-index`
- `python .\scripts\devflow.py validate-workflow --all`
- `python .\scripts\devflow.py doctor-capabilities --strict`
- `python .\scripts\devflow.py resolve-capability --name <capability>`

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
- `L2/L3` repository-backed work 默认先建立 `changes/<change-id>/proposal.md`、`design.md`、`tasks.md`
- run 文书只写治理摘要与 change artifact 引用，不复制完整正文
- 若脚本不可用，应退回逻辑协议模式，并明确说明未执行脚本

## Change-aware 最小路径

```powershell
python .\scripts\devflow.py init-change --change-id 20260609-example
python .\scripts\devflow.py validate-change --change-id 20260609-example
python .\scripts\devflow.py create-run --project leroy-skills-garage --topic example
python .\scripts\devflow.py link-change --run-id <run_id> --change-id 20260609-example
python .\scripts\devflow.py sync-spec-index
```

## Workflow 与 Capability

- workflow recipes 位于 `workflows/*.yaml`，使用 JSON-compatible YAML，不需要 PyYAML。
- capability registry 位于 `capabilities/providers.yaml`。
- `validate-workflow` 检查必填字段、skill 引用、capability 引用与 next workflow 引用。
- `doctor-capabilities` 按顺序探测 provider，并报告实际选择与 fallback。
- `resolve-capability` 返回第一个可用 provider；无法解析时退出码非零。
- doctor 当前只支持 `command`、`path`、`always` 三种只读 probe，不安装依赖、不读取凭据、不执行网络登录。

```powershell
python .\scripts\devflow.py validate-workflow --workflow implement
python .\scripts\devflow.py doctor-capabilities --name repository_search
python .\scripts\devflow.py resolve-capability --name repository_search
```
