---
name: git-commit
description: 規範 git 提交流程：提交前先檢查遠端主幹有無更新、從最新主幹分出工作分支、提交訊息寫明改動內容與原因。適用使用者要求提交、commit、存檔進版本庫或準備推送時；只查看狀態、diff 或歷史不使用。
---

# Git 提交流程

三條硬性要求，缺一不提交：先檢查更新、不在主幹上提交、提交訊息有詳細說明。任一步失敗就停下回報實際輸出，不跳過、不聲稱已檢查。

## 1. 檢查更新

```text
git status --short --branch
git symbolic-ref --short refs/remotes/origin/HEAD
git fetch origin --prune
git rev-list --left-right --count origin/<主幹>...HEAD
```

- 主幹名稱以 `origin/HEAD` 為準；查不到時依序找 `main`、`master`，仍無法確定就問使用者。
- `rev-list` 輸出為「落後數 領先數」。落後數大於 0 表示主幹有更新，要先在第 2 步納入再提交。
- `fetch` 失敗（離線、無權限）時不當作「沒有更新」；回報後由使用者決定是否仍在本地提交。
- 沒有遠端的倉庫跳過 fetch，以本地主幹為基準，並在回報裡說明沒有做遠端檢查。

## 2. 從主幹分出工作分支

目前在主幹上：

```text
git switch -c <分支名> origin/<主幹>
```

- 未提交的改動會跟著帶到新分支。git 因衝突拒絕切換時，用 `git stash push -u` → 切換 → `git stash pop`；pop 出現衝突就停下回報，不自行取捨內容。
- 本地主幹有尚未推送的提交時先問使用者，不擅自搬移或丟棄。

目前已在工作分支上：

- 沒有落後主幹：直接進第 3 步。
- 落後主幹且分支尚未推送：`git rebase --autostash origin/<主幹>`。
- 落後主幹且分支已推送或與他人共用：`git merge origin/<主幹>`，不改寫已推送的歷史。
- 該分支與本次改動無關時，改從主幹另開新分支。

分支名沿用專案既有慣例；沒有慣例時用 `<類型>/<簡短英文描述>`，例如 `feat/git-commit-skill`、`fix/login-timeout`。類型與提交訊息的類型一致。

## 3. 暫存與檢查

- 按路徑 `git add <檔案>` 只加入本次改動相關的檔案，不用 `git add -A` 把無關改動一起帶入。
- 用 `git diff --staged` 核對暫存內容；發現憑證、金鑰、`.env` 或大型產物就移出並告知使用者。
- 互不相關的改動拆成多次提交，各自有說明。

## 4. 提交訊息

語言與格式先看 `git log -5` 沿用既有習慣；沒有既定習慣時用使用者的語言和以下模板：

```text
<類型>: <一句話摘要，50 字內>

改動內容：
- <改了什麼，具體到模組或行為>
- <...>

改動原因：
<為什麼要改：問題、需求或背景；有議題編號就附上>

影響與驗證：
- <影響範圍、相容性或需要注意的地方>
- <實際做過的驗證及結果；沒有驗證就寫「未驗證」>
```

- 類型：`feat`、`fix`、`docs`、`refactor`、`test`、`chore`、`perf`。
- 「改動內容」和「改動原因」必填。原因從對話和 diff 判斷，判斷不出來就問使用者，不編造。
- 只寫實際發生的事；沒跑過的測試不寫成通過。

多行訊息寫入倉庫外的 UTF-8（無 BOM）暫存檔後提交，避免 shell 引號和編碼問題，提交後刪除暫存檔：

```text
git commit -F <暫存檔路徑>
```

範例：

```text
fix: 修正登入逾時後未清除 session

改動內容：
- auth/session.py 在逾時時同步清除伺服器端 session 紀錄
- 補上逾時情境的單元測試

改動原因：
逾時後 cookie 失效但伺服器端 session 仍保留，舊 token 在 TTL 內可被重放（#128）。

影響與驗證：
- 只影響逾時路徑，正常登出流程不變
- python -m unittest tests.test_session 共 12 項通過
```

## 5. 確認與回報

```text
git log -1 --stat
git status --short --branch
```

回報分支名、commit 雜湊、更新檢查的結果（落後幾個提交、如何處理）及未納入提交的改動。

推送、開 PR、合併回主幹只在使用者已授權時執行。不使用 `--force`、`--no-verify`、`--amend` 已推送的提交；hook 失敗時修正問題後建立新的提交。
