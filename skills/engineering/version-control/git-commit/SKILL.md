---
name: git-commit
description: 安全地建立 Git commit，或依 staged diff 草擬 commit message。
disable-model-invocation: false
---

# Git Commit

## 1. 確認請求與範圍

先區分「依 staged diff 產生訊息」與「建立 commit」。檢查適用的 repository instructions、近期 commit subjects、`git status --short` 與 `git diff --staged`。

- 只要求訊息：只描述 staged diff，不 staging、不 commit；staged diff 為空時回報無暫存內容並停止。
- 要求提交：依使用者指定檔案、已 staged 內容或本次對話可明確識別的修改判定範圍。需要加入未暫存改動時讀取 diff；未追蹤檔案需直接讀取內容，不能只靠 `git diff`。
- 範圍不明、混有無關改動或需更動使用者原有 staged 範圍時，展示具體差異後詢問。明確授權的範圍不重複索取同意。

完成條件：請求分支與提交範圍明確；訊息草稿分支不改動工作樹或 index。

## 2. 準備提交內容

只 staging 已授權內容，優先用 `git add -- <files>` 指定檔案。若同一檔案混有無關改動，僅暫存已授權部分；無法可靠區分時詢問，不整檔加入。使用者明確要求 `git add .` 時才使用該命令。

檢查 staged diff 是否構成可獨立描述與回復的變更。多個無關變更先建議拆分，經同意才調整原有 staged 範圍。未 staged 不代表無可提交內容。

完成條件：最終 staged diff 精確符合授權範圍，未混入無關內容。

## 3. 產生並驗證訊息

遵循專案既有 commit message 慣例；沒有時使用 Conventional Commits：

```text
<type>(<scope>): <subject>

<body>

<footer>
```

Fallback type：`feat`、`fix`、`docs`、`style`、`refactor`、`perf`、`test`、`chore`。scope 可省略。subject 使用主動、祈使語氣，以 50 字元內為目標，不超過 72 字元且不以句號結尾。body 說明解決的問題與原因；body/footer 無額外資訊時省略，段落間留空行。

以最終 `git diff --staged` 核對訊息。使用 fallback 時，將 `<skill-dir>` 解析為本 SKILL.md 所在目錄，安全傳入 subject 並執行 `bash "<skill-dir>/scripts/validate_commit_msg.sh" "<subject>"`；採專案格式時依其規範驗證。動態訊息使用安全引號或參數傳遞，避免 shell 展開。

完成條件：訊息只描述 staged diff 並符合選定格式；草稿請求到此返回訊息。

## 4. 建立並確認 commit

已授權提交時，將訊息寫入暫存檔，執行 `git commit -F <message-file>`，不額外詢問訊息確認；使用者要求先審核訊息時才等候同意。commit 失敗時檢查原因，不宣稱成功或繞過 hooks。

成功後檢查最新 commit 與 `git status --short`，回報 commit ID、subject 及剩餘改動。提交授權不包含 push。
