# 盤點精簡 Skills 目錄並新增 `to-devlog`

- **日期**：2026-11-20

## 背景與問題

這批改動起於調整 `git-commit` Skill 後，進一步以 `writing-for-agents` 原則全面盤點整個 `skills/` 目錄。檢查後發現三個問題：

1. **常駐 context load 偏高且累積未用 skill**：原本 14 個 skill 中有 6 個幾乎沒用過或已過時，且其中 5 個設為 `disable-model-invocation: false`，每輪對話都在消耗 context token 與注意力。
2. **既有 skill 存在容易導致 agent 失誤的寫法**：包含小改動被「抽檢」稀釋核對門檻、reference pointer 放在最後一步完成條件之後、安全授權規則被埋在長段落，以及步驟完成條件存在前向依賴。
3. **缺少記錄跨 commit 動機的輕量文件機制**：`git log` 只適合看「改了什麼」，`to-manual` 處理操作流程，ADR（`docs/adr/`）則只留給難逆轉的架構決策，缺少能把單次 session 決策脈絡沉澱下來的通用工作流。

## 關鍵決策與取捨

### 1. 直接刪除 6 個未用／過時 skill，而非轉為手動載入保留
- **決策**：移除 `migrate-to-codex`、`agy-delegate`、`optimize-prompts`、`gh-cli`、`git-report`、`gitlab-cli`，使自動載入（`disable-model-invocation: false`）的 skill 只剩下 `git-commit` 與 `multi-agent-discipline`。
- **放棄的替代方案**：將仍具結構價值的 `git-report` 與記有 `glab` 參數差異的 `gitlab-cli` 改為 `disable-model-invocation: true`（零 context 成本）保留。
- **理由與取捨**：未實際使用的 skill 即使不佔 context，仍會增加維護與認知負擔，並隨 CLI／工具演進逐漸過時；刪除後仍完整保留於 Git 歷史中，沒有不可逆風險。
- **Revisit trigger**：若未來開始固定產出 Git 進度週報，或日常工作回到頻繁操作 GitLab／`glab`，再從 Git 歷史取回或依當下工具重寫。

### 2. 以 `writing-for-agents` 原則收斂其餘 skill，不動狀態良好的檔案
- **決策**：
  - `git-commit`：大型刪除／rename 時改用 `--stat -M`、目錄級 `git add` 與超過 10 檔的彙總提示，但保留「一般改動讀完整 staged diff」避免拉低小 commit 核對門檻；將暫存訊息檔明確限制在 repo 外（如 `/tmp`）並改用單引號範例，避免污染工作樹或觸發 shell 展開；驗證腳本對齊檢查第一行總長 72 字元。
  - `multi-agent-discipline`：壓縮常駐 `description` 中重複的分支描述並刪去無來源比例敘述。
  - `python-src-layout`、`ubuntu-cleanup`、`setup-home-repo`、`ambitious-framing`：將 reference pointer 移回決策點、把安全授權規則拆列凸顯、消除步驟完成條件的前向依賴，並移除手動 skill `description` 中的模型觸發語句。
- **放棄的替代方案**：順手微調 `to-manual` 與 `adhd-mode`。兩者皆已簡潔且無明顯行為缺陷，保持不動以避免無意義變動。

### 3. 新增通用的手動 Skill `to-devlog`
- **決策**：建立 `disable-model-invocation: true` 的 `to-devlog`（置於 `skills/productivity/documentation/to-devlog/`），預設輸出單檔 `docs/devlog/YYYY-MM-DD-<slug>.md`，僅在伴隨附屬檔案時改建同名目錄 `README.md`；優先沿用目標專案既有的 `docs/` 目錄與文件慣例，且不自動執行 commit。
- **放棄的替代方案**：
  - 每次固定建一個子目錄（`docs/devlog/<name>/README.md`）：單純文字記錄多一層目錄嵌套會增加瀏覽摩擦。
  - 命名為 `changelog` 類名稱：容易與給外部使用者看的發版 `CHANGELOG.md` 混淆。
- **理由與取捨**：透過 `grounded`／`unexplained` 分類與詢問 gate 避免 agent 腦補未討論的動機；並刻意保持技術棧無關，使程式碼、腳本、設定或文件型專案都能通用。
- **Revisit trigger**：若後續多數 devlog 都需要固定附帶測試報表或圖表，再評估將資料夾模式改為預設。

## Commits

- `4f7468e` — `refactor(git-commit): refine diff workflow and length validation`
- `0acf768` — `chore(skills): remove unused and obsolete skills`
- `b9df4b3` — `refactor(skills): tighten pointers, criteria, and readability`
- `909bb70` — `feat: add to-devlog skill`

## Follow-ups

- 本機執行 `npx --yes . sync` 時顯示 `~/.agents/skills` 尚未納入 `kim-skills` 管理；若先前曾手動安裝過舊版複本，需執行 `npx --yes . install --all` 納入管理或手動清理已刪除的 6 個 skill 複本。
