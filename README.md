# leroy-skills-garage

⚪ 口諭（快問快答／微調）
目標：最快解答，不加流程負擔。
通常會用
主對話直接回答（不開 run）
必要時少量只讀：ReadFile、rg
幾乎不會叫：subagent、devflow.py、審核文書
🟢 快奏（小改、單點修復）
目標：快速完成 + 基本驗證。
通常會用
讀查：ReadFile、rg、Glob
修改：ApplyPatch / Write / StrReplace
驗證：Shell（跑小測試）、ReadLints
可選 skill：pragmatic_coder
通常不開：devflow.py、多 subagent 辯論
🟡 常奏（多檔但邊界清楚）
目標：有計畫、有審核，但控制成本。
通常會用
規劃：task-planner skill 或 devflow-planner subagent
證據（可選）：devflow-evidence-explorer subagent（唯讀）
審核（必要時）：devflow-critic subagent（PASS/FAIL）
文書／狀態（若啟用工具化）：python scripts/devflow.py
create-run
write-artifact（plan/review）
update-status
validate-run
仍以精簡為主：通常停在 Reviewed=Approved
🔴 正奏（高風險／跨系統／正式流程）
目標：可靠性、可審計、可追溯優先。
通常會用（全套）
規劃：devflow-planner
蒐證：devflow-evidence-explorer
硬審：devflow-critic
執行與驗證：ApplyPatch/Write + Shell + ReadLints
流程落盤：scripts/devflow.py 全流程
create-run → write-artifact(plan/review/dispatch/delivery/postmortem)
update-status（每次狀態變更）
validate-run
必要時再做人審批/回滾演練
一句話總結
⚪🟢：以「主 agent + 基本讀寫工具」為主。
🟡：加「規劃/審核」但保持輕量。
🔴：才啟用「subagent 分工 + devflow.py 可審計全流程」。
