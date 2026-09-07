---
name: ubuntu-cleanup
description: "盤點並安全清理 Ubuntu 的快取、暫存檔、舊套件、容器資源與可重建的開發產物。"
disable-model-invocation: true
---

# Ubuntu Cleanup

以「先盤點、再授權、後驗證」清理 Ubuntu。呼叫此 skill 本身只授權唯讀盤點；實際刪除仍以使用者在本次對話中明確同意的項目為限。

## 1. 盤點

先記錄 `df -hT`、`df -ih` 與根檔案系統可用 bytes。使用 `du -x` 由淺入深找出主要占用，避免跨越其他 mount；檢查存在且適用的來源：

- 使用者 cache、Trash、瀏覽器 cache，以及 pip、uv、npm、pnpm 等套件 cache。
- `/tmp`、APT cache、systemd journal、crash dump、停用的 Snap revision。
- Docker/Podman 的 containers、images、volumes、networks 與 builder cache。
- 專案內 `.venv`、`node_modules`、`target`、`build`、`dist`、coverage 與工具 cache。
- 舊版 remote IDE/server、已刪除但仍被程序開啟的檔案，以及異常大的單一檔案。

只執行與現有軟體相符的檢查；command 不存在時記錄並略過。以實際輸出為證據，不從目錄名稱猜測內容。對「舊」資料查閱工具提供的 last-used/active 狀態、檔案時間與目前執行程序；沒有可靠證據或使用者指定的時間門檻時，只列為候選並要求使用者判斷，不宣稱它已經過時。完成條件：主要占用均能歸類，且每個候選都有路徑或資源名稱、大小、影響與可取得的新舊證據。

## 2. 提案與授權

依下列風險分組，先回報預估可回收空間：

- **低風險**：可重新下載的 cache、APT cache、舊 crash dump、停用 Snap revision。
- **可重建**：虛擬環境、依賴目錄、build 產物、舊 IDE server、未使用的 container image。說明重建或重新下載成本。
- **需逐項確認**：Trash（可能包含無其他副本的個人檔案）、個人檔案、下載、模型或 dataset、瀏覽器 profile、應用程式狀態、資料庫、備份、Docker volume，以及執行中的 container。

列出將保留的主要資料，避免「全部清理」的範圍不明。使用者明確授權清理的 exact target 或低風險、可重建分類，可在核實範圍後執行；模型的風險分類本身不代表授權，其餘候選先取得確認。上述「需逐項確認」一律優先於「全部」、「都清掉」或 Docker 等廣泛分類授權：盤點列出 exact resources 與影響後，需有使用者逐項或針對該清單整體的刪除授權；已有對應明確授權時不重複詢問。`dry-run` 存在時先執行並以結果收斂 exact targets。完成條件：每個待刪項目都有本次對話中的明確授權。

## 3. 清理

清理前再次解析並核對 exact targets。優先使用套件管理器或工具本身的 clean/prune/remove 命令；只在沒有合適介面時刪除明確路徑。保護 mount root、家目錄、workspace root 與未展開變數，不以寬泛 glob、未驗證的 command substitution 或遞迴命令決定刪除範圍。

若應用程式正在寫入目標，說明需要關閉的程序；除非使用者已同意中斷，否則保留該項。需要 sudo 密碼而無法非互動完成時，繼續處理其他已授權項目，最後提供 scope 精確的手動命令。完成條件：所有已授權項目均已刪除或明確列出未完成原因，未授權資料保持不變。

## 4. 驗證

重新執行相同的空間與資源查詢。回報實際釋放 bytes/GiB、前後使用率、各分類結果、被關閉或移除的服務，以及任何需要重新下載或重建的內容。對部分失敗逐項核對，不以命令 exit code 代替結果驗證。
