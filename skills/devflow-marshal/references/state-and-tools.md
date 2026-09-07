# 狀態與工具

專案規則優先。通常狀態為 Draft → Planned → Reviewed；審議失敗記錄 Rejected 並返工。正式執行依序 Dispatched → Running → Delivered → Archived。L2 未獲繼續指令時停在 Reviewed=Approved；已批准執行的 L2 記錄批准與執行結果，是否升級狀態依專案協定。

每次狀態變更都寫 run.json.audit。change_id 是需求記錄，run_id 是執行證據實例，兩者需互相引用。狀態欄位通過不代表測試通過。

工具順序：專案 scripts/devflow.py → 存在時使用 CODEX_HOME/scripts/devflow.py（CODEX_HOME 未設定則使用目前使用者的 .codex）→ 明示無工具的邏輯記錄。先執行 --help 確認子命令；不可假設所有版本都有 init-change、link-change 或 capability doctor。不要為了技能工作升級專案固定版本。

已確認的基本命令模式（PYTHON/SCRIPT/RUN 代表實際解析的路徑或值）：
```text
PYTHON SCRIPT create-run --project PROJECT --topic TOPIC
PYTHON SCRIPT get-run --run-id RUN
PYTHON SCRIPT write-artifact --run-id RUN --artifact plan
PYTHON SCRIPT update-status --run-id RUN --status Planned --actor codex --note NOTE
PYTHON SCRIPT validate-run --run-id RUN --strict-level standard
```
write-artifact 的正文用 UTF-8 stdin 傳入。artifact 可用值先以 --help 確認；常見 plan/review/dispatch/delivery/postmortem 對應 01–05 文件。

有 capabilities/providers.yaml 或 workflows 時才讀取相關註冊表及可用 doctor 命令；缺少選用 provider 就採可用替代。只有確實必要且沒有替代的能力才構成阻塞。不自動安裝、查看憑證或發出認證探測。
