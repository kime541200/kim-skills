---
name: python-src-layout
description: "設計新 Python 套件的 src-layout，或依明確要求遷移既有專案，並驗證安裝、CLI 與測試。"
disable-model-invocation: true
---

# Python src-layout

適用於新可安裝 Python 套件的佈局設計，或使用者明確要求的既有專案佈局遷移。新套件優先採 src-layout；既有專案的一般修改沿用原結構，不因偵測到 flat-layout 自動搬移或擴大工作。

## 1. 檢查專案

讀取 pyproject.toml、build backend、套件與 CLI entry points、測試及 CI 的安裝方式。沿用既有工具與依賴；區分單次腳本、應用程式與需打包的套件。src-layout 是佈局選擇，並非所有 Python 檔案都必須放在 src 下。

完成條件：佈局變更在授權範圍內，且已識別受影響的安裝、import、CLI 與測試路徑。

## 2. 初始化或遷移

典型結構：

```text
pyproject.toml
src/
  my_package/
    __init__.py
    main.py
tests/
  test_main.py
```

只建立需求所需的檔案。遷移時搬移生產套件、調整現有 backend 的套件發現與 package data 設定，並更新受影響的 entry points 與 import 路徑。

setuptools 的常見設定：

```toml
[tool.setuptools.packages.find]
where = ["src"]
```

Hatch 的常見設定：

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/my_package"]
```

只套用專案正在使用的 backend 設定，按目前版本文件與既有用法核對。使用專案既有安裝流程更新環境；例如 uv 環境可使用 `uv pip install -e .`。

## 3. 執行與驗證

- 上述含 main.py 的範例使用 `python -m my_package.main`。只有已定義 `__main__.py` 時才用 `python -m my_package`；已安裝的 console entry point 優先沿用。
- 開發測試可使用 editable install。`pythonpath = ["src"]` 只適用於明確選擇直接測試原始碼的流程，不把它當作安裝或打包驗證。
- 驗證遷移的打包行為時，建置產物並在隔離環境安裝，從原始碼樹外執行必要 import／CLI smoke checks 與適用測試，避免 PYTHONPATH 指向 src 掩蓋缺漏。
- 沿用既有 pytest import mode 與 tests 套件結構；只有實際 import 問題才調整，不一律移除 tests/__init__.py。
- 不預設加入 sys.path hack；使用者明確要求免安裝執行時，再評估直接原始碼路線。

完成條件：授權的佈局變更完成，相關安裝、import、CLI 與測試可運作；檢查通過後不因一般小修改反覆做整套打包驗證。

佈局取捨與直接執行特例見 `references/src-layout-vs-flat-layout.rst`。
