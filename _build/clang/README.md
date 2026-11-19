# C++ 主題（clang）製作說明

18 篇、5 個階段，輸出到 `public/clang/clang-<子題>-guide.html`；首頁分類 id 是 `clang`、標籤「C++」（`clang` 也是編譯器名稱，但已決定沿用）。共用規範見 `_build/README.md`；本文件只記這個主題的決定、規則與工具。

## 已確認的決定

- 對象：完全沒寫過程式的人。每篇都能跟著打：程式碼逐步長大，新增行用 olive 底色標出，每步固定三塊「為什麼這樣寫、預期輸出（實測）、試著改改看」。刻意放編譯錯誤範例並教讀訊息。
- 跑程式的方式：**主推免安裝的線上編譯器**，本機 `g++`／VS Code 當進階選項。統一 **C++17**（`g++ -std=c++17 main.cpp -o main`），不教 C++20 以後的語法。
- 篇章分級：1 至 7 入門、8 至 13 基礎、14 至 18 進階；第 16（檔案與例外）、17（動態記憶體）為「進階選讀」，首頁 `pathNote` 有說明。每篇約 20 至 35 分鐘，第 18 篇 45 分鐘。
- 教學順序：第 2 篇先用 `std::cout` 並解釋 `std::`，再引入 `using namespace std;`，**第 3 篇起一律用 `using namespace std;`**；先教 `vector` 再談原生陣列細節；函式只教傳值，傳參考放第 12 篇；第 8 篇不教新語法；隨機數用 `<random>`（不教 `rand()`），猜數字先用固定種子 `mt19937 gen(2024)`，最後一版才換 `random_device`（`*.norun.cpp`，不展示輸出）。
- 不做：頁面內真的編譯或執行 C++、自由輸入任意 C++ 的假執行、模板與多執行緒、Makefile／CMake、第三方函式庫、英文版。
- 第 16 篇的檔案範例：線上編譯器通常不保留檔案，頁面已說明限制，範例都設計成「同一支程式先寫、再讀回來」，不行時建議改用本機 g++。
- 外部連結白名單：只有 `en.cppreference.com`、`www.onlinegdb.com`、`www.programiz.com`（`verify_clang.py` 的 `ALLOW`）。其餘一律不放。
- 頁面 eyebrow：`C++ 入門 · <主題>`；頁尾文字寫在 `ch.py` 的 `FOOT`，每頁 SPEC 都帶 `topic`／`foot`。

## 檔案

| 檔案 | 用途 |
|---|---|
| `c01.py` … `c18.py` | 各頁規格（`from ch import *`，用 `spec(...)` 建立，`nav(n)` 決定上下篇） |
| `ch.py` | 組頁輔助：`code(id, prev=)`、`term`、`errterm`、`run`、`exercise`、`flow`、`chk`、`links`、`stepper` 等；程式碼與輸出一律來自 `examples/`，頁面不手抄 |
| `clang.css`、`clang.js` | 主題專用樣式與互動引擎（登記在 `build.py` 的 `THEMES["clang"]`）：`flow`、`stepper`（變數盒子／呼叫堆疊／記憶體格子加箭頭）、`calc`（overflow、format、eval、loop）、`ladder`、`memory`、`beforeafter`、`diagram`。依賴 `shared/common.js` 提供的 `window.PAGE_UTIL` |
| `examples/pNN/` | 範例 `.cpp`；命名：`*.err.cpp` 預期編譯失敗（擷取第一個錯誤）、`*.crash.cpp` 預期執行時中止、`*.exitN.cpp` 預期結束碼 N、`*.norun.cpp` 只編譯不執行；`<名稱>.in` 提供 stdin；行尾 `//@ 說明` 變成可點選的逐行說明 |
| `examples/results.json` | `run_examples.py` 的輸出快取，頁面引用它 |
| `run_examples.py` | 以 `g++ -std=c++17 -Wall -Wextra` 編譯並執行全部範例（有警告也算失敗），更新 `results.json` |
| `check_format.py`、`check_eval.py`、`check_loop.py` | 交叉驗證：JS 模擬（格式化、運算式求值、迴圈追蹤）必須等於真的 g++ 結果；改了對應引擎後必須重跑 |
| `verify_clang.py` | 主題專用瀏覽器驗證（1280／390 寬、互動、靜態檢查）；外部網址白名單含選用的 Analytics beacon |

## 指令（repo 根目錄）

```bash
python3 _build/build.py --all clang           # 重組全部 C++ 頁面
python3 _build/build.py c07                   # 只重組第 7 篇（上下篇連結要靠重組相鄰頁更新）
python3 _build/clang/run_examples.py [pNN]    # 重跑範例並更新 results.json
python3 _build/clang/check_eval.py            # 另有 check_format.py、check_loop.py
CHROME_PATH=<chrome> python3 _build/clang/verify_clang.py
```

需要 `g++`（本機實測用 13.x）與 Playwright 的 Chromium。`verify_clang.py` 與三支 `check_*.py` 都已套用 `shared/pwutil.py` 的 `stub_analytics`（`seo.py` 填了 `ANALYTICS_TOKEN` 時才需要，沒填也無害）；新寫的 Playwright 腳本照做。SPEC 裡的 `kit` 欄位是舊版 build 的遺跡，統一版 `build.py` 忽略它，主題樣式與腳本改由 `THEMES` 的 `css`／`js` 載入。

## 內容規則

- 範例輸出必須是實測結果；故意寫錯的範例要確實編譯失敗。
- 不使用 `localStorage`；全形標點由 `build.py`（`fw=True`）處理。
- 測驗題 `q` 用 innerHTML、選項 `a` 為純文字；TL;DR 強調用 `<strong>`；區塊 id 不可與互動元件 id（例如 `stages`）撞名。
- 初學者最容易放棄的是第 1 篇的環境與第 12 篇的指標：第 1 篇先給線上編譯器路徑，第 12 篇必須用記憶體格子圖。

## 查證狀態

見 `reports/link-check.md`：範例與輸出已用 g++ 13.3 重跑核對；外部連結只有使用者在瀏覽器抽查（cppreference 已改用不含 `/w/` 的最終網址，格式為 `https://en.cppreference.com/cpp/...`），**尚未逐條驗證**，頁尾如實寫「外部連結已於 2026-11-18 抽查（非逐條驗證）、安裝步驟未逐一對照官方文件」；使用者（2026-11-18，抽查十篇）判斷抽查已足夠。
