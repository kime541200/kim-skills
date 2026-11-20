---
name: git-commit
description: 建立 Git commit，或依 staged diff 草擬 commit message。
disable-model-invocation: false
---

# Git Commit

## 1. 確認請求與範圍

先區分「依 staged diff 產生訊息」與「建立 commit」。檢查適用的 repository instructions、近期 commit subjects、`git status --short` 與 `git diff --staged --stat -M`；先用 `--stat -M` 掌握全貌與 rename。

- 只要求訊息：只描述 staged diff，不 staging、不 commit；staged diff 為空時回報無暫存內容並停止，否則跳至步驟 3。
- 要求提交：依使用者指定路徑、已 staged 內容或本次對話可明確識別的修改判定範圍（即使尚無 staged 內容，仍檢查未暫存與未追蹤改動）。需要加入未暫存改動時先看 `git diff --stat -M`，只對有實質內容改動或關鍵未追蹤檔案按需讀取 diff 或內容。
- 範圍不明、混有無關改動或需更動使用者原有 staged 範圍時，展示差異後詢問：變更檔案超過約 10 個時，改以「目錄＋狀態」彙總呈現，僅單獨標出關鍵或疑似敏感檔案（使用者要求時再展開完整清單）。明確授權的範圍不重複索取同意。

完成條件：請求分支與提交範圍明確；訊息草稿分支不改動工作樹或 index。

## 2. 準備提交內容

只 staging 已授權內容，優先用 `git add -- <paths>` 指定檔案，大量檔案時改用已授權的目錄或 pathspec。若同一檔案混有無關改動，僅暫存已授權部分；無法可靠區分時詢問，不整檔加入。使用者明確要求 `git add .` 時才使用該命令。

檢查 staged diff 是否構成可獨立描述與回復的變更。多個無關變更先建議拆分，經同意才調整原有 staged 範圍。

完成條件：最終 staged diff 精確符合授權範圍，未混入無關內容。

## 3. 產生並驗證訊息

遵循專案既有 commit message 慣例；沒有時使用 Conventional Commits：

```text
<type>(<scope>): <subject>

<body>

<footer>
```

Fallback type：`feat`、`fix`、`docs`、`style`、`refactor`、`perf`、`test`、`chore`。scope 可省略。subject 使用主動、祈使語氣，以 50 字元內為目標；第一行總長不超過 72 字元且不以句號結尾。body 說明解決的問題與原因；body/footer 無額外資訊時省略，段落間留空行。

核對最終 staged diff 與訊息是否一致：一般改動讀取完整 `git diff --staged`；大量刪除、rename 或批次檔時，以 `git diff --staged --stat -M` 搭配實質內容修改檔的 diff 核對。使用 fallback 時，將 `<skill-dir>` 解析為本 SKILL.md 所在目錄，以單引號或參數傳遞第一行並執行 `bash "<skill-dir>/scripts/validate_commit_msg.sh" '<first-line>'`（避免 `$`、反引號等 shell 展開）；採專案格式時依其規範驗證。

完成條件：訊息只描述 staged diff 並符合選定格式；草稿請求到此返回訊息。

## 4. 建立並確認 commit

已授權提交時，將訊息寫入 repo 外的暫存檔（如 `/tmp`），執行 `git commit -F <message-file>` 並於完成後清理，不額外詢問訊息確認；使用者要求先審核訊息時才等候同意。commit 失敗時檢查原因，不宣稱成功或繞過 hooks。

成功後檢查最新 commit 與 `git status --short`，回報 commit ID、subject 及剩餘改動。提交授權不包含 push。
