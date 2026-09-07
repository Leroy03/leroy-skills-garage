# 測試證據

1. 讀取專案規則與 devflow.project.yaml，確認命令適用本次範圍。執行器若預設會跑 Runtime 或覆寫別人的根目錄報告，改以明確命令和本次 run 目錄收證，不為適應工具改專案設定。
2. 記錄命令、cwd、開始／結束時間、exit_code、耗時與 stdout/stderr；保留失敗。非零退出不等於測試失敗的場景應解釋工具語義，不能改造原始記錄。
3. [test_result schema](../schemas/test_result.schema.json) 是既有格式。JSON 額外記錄 change_id、run_id、Git HEAD；工作樹不乾淨時附 dirty_manifest_sha256。證據按 run 保存，避免覆寫其他工作。
4. 現有 devflow.py 支援 collect-evidence 時可復用，先查看 --help 與 --output 語義。以專案腳本為先；全域備援路徑從 CODEX_HOME 或使用者目錄解析，不寫死他人的帳號路徑。
5. 不因測試技能被載入就安裝依賴。必要新增／升級須有變更說明、直接驗證和回滾。若工具不可用，選可用的等價直接驗證並記錄限制。

契約紀錄記載「實際提供了哪些輸入／輸出／證據」。devflow-marshal 的 contract 檢查若只驗欄位及檔案存在，不能宣稱已驗證內容正確；還需檢查命令結果與驗收覆蓋。
