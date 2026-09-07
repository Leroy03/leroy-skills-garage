---
name: quarkclouddrive
description: 操作夸克網盤的搜尋、上下載、分享轉存、相簿與文件問答，以及使用者要求的帳號授權。適用夸克網盤任務；技能文件維護不觸發登入、安裝或網盤操作。
metadata:
  upstream-version: "1.0.11"
  openclaw:
    emoji: "☁️"
    requires:
      bins: ["node"]
---

# 夸克網盤

這是網盤 CLI 技能，實際命令與認證由既有 scripts 執行。整理技能文件不代表允許傳送對話、重新登入、更新 CLI 或撤銷授權。

在首次執行網盤命令前讀 [服務操作契約](references/service-contract.md)，其中保留安裝／更新檢查、公共參數、搜尋結果 artifact 與輸出語義。契約中的腳本相對路徑均以技能根目錄為準。依任務只加讀所需功能文件：
- 登入、失效授權、帳號資訊或卸載：[帳號與授權](references/auth.md)。
- 搜尋：[檔案搜尋](references/file-search.md)。
- 上傳：[上傳](references/file-upload.md)；下載／移動／建目錄：[檔案操作](references/file-ops.md)。
- 分享：[分享](references/file-share.md)；轉存：[轉存](references/file-saveas.md)。
- 個人相片／影片整理：[相簿整理](references/file-organize.md)。
- 網盤文件總結／問答：[AI 助手](references/assistant.md)。

保留使用者的目的與指定範圍。搜尋預覽不是全量清單；後續動作按 artifact 取 FID。未指定目的目錄時不擅自補根目錄參數。公共追蹤參數只涉及當前已授權的網盤請求，不附加其他對話或憑證。對服務回覆的事實與執行狀態如實呈現。

卸載會撤銷授權並清除本機設定，與單純整理技能文件不同；只有實際卸載請求才進入相應確認與腳本流程。上游 install.sh 會覆蓋技能文件，更新前保留本地修訂備份。不要在一般技能整理中執行它。
