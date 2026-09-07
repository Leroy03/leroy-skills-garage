---
name: hatch-pet
description: 建立、修復與封裝 Codex v2 動畫寵物，包含 9 個標準動畫狀態、16 個注視方向及圖集 QA。適用新寵物或既有寵物修復；一般插畫使用 imagegen。
---

# Hatch Pet

保留使用者提供的角色身份、風格與已批准動畫。名稱或簡介缺省時可合理推定；已有輸入從適用階段接續，不重做整套。

## 共用契約
- 先讀 [v2 封裝契約](references/codex-pet-contract.md)；標準行語義與幀數查 [動畫行](references/animation-rows.md)。新寵物最終必須 8×11、1536×2288、192×208 cells、透明背景及 spriteVersionNumber: 2。
- 8×9 僅為中間產物。000 是向上，不是 neutral；兩個 look rows 必須各來自一張連貫 8 幀來源，不混貼單獨修復格。
- 視覺生成使用已安裝 imagegen 的入口與可用工具；不把整理／維護技能當成生成請求。确定性組裝使用保留的 scripts。
- 執行腳本前用 load_workspace_dependencies 取得 bundled Python/Pillow 路徑。SKILL_DIR 指向本技能根目錄；範例為 shell 語法，Windows 使用原生 PowerShell 或參數陣列，不直接貼 Bash 語法。

## 按階段讀取
1. 輸入、身份、透明度與構型決策：讀 [準備](references/preparation.md)。僅有品牌名稱且確需查資料時，再讀 [品牌探索](references/brand-discovery.md)。
2. 標準動畫生成、切幀與中間圖集：讀 [製作流程](references/production.md)。
3. 製作／修復 16 方向：讀 [方向製作與 QA](references/look-directions.md)。保留三份獨立盲評、cardinal 硬門禁、intermediate warning 的有標籤連貫性審查；warning 不自動等於重生整套。
4. 需要圖像生成或盲評代理时讀 [視覺工作者](references/visual-workers.md)，在可用且已授權的環境內執行；不得偽造不存在的獨立評審。
5. 修復及最後封裝：讀 [修復與驗收](references/repair-and-acceptance.md) 和 [QA 清單](references/qa-rubric.md)。缺必要 QA 時回報 partial，不安裝未通過成品。

## 最終組裝順序
由未做最終去色的來源重建時，先用 scripts/assemble_extended_atlas.py 組成 v2，再且只對最終圖集執行一次 scripts/despill_chroma_edges.py；標準中間圖集不提前做最終去色。既有成品修復先遵守修復參考文件的來源保全分支，不能把已去色 atlas 再套同一步骤。修復後按受影響範圍重跑驗證、方向與連貫性檢查。

重複失敗且沒有改善時更換可驗證策略；保留已通過資產，時間預估不授權降低 QA。只回報已完成階段、產物與未通過項，不強制固定進度話術。清理只限本次工作且可回復的中間檔，不預設刪除原始生成圖或使用者來源。
