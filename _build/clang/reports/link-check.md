# C++ 主題 · 外部連結與事實查證報告

檢查日期：2026-11-17（AI 端嘗試）、2026-11-18（使用者在瀏覽器回報）
方法：在整併對話中用 `web_search` 與 `web_fetch` 嘗試實際開啟。`web_fetch` 只能開啟「已出現在搜尋結果中的網址」，且 `en.cppreference.com` 對自動抓取回應 bot detection（CLIENT_ERROR），所以多數連結**無法取得頁面內容**。shell 無法連外網，不能當證據。

## 一、連結（全站 37 條，18 頁）

| 狀態 | 條數 | 說明 |
|---|---|---|
| 開啟成功 | 1 | `https://www.programiz.com/cpp-programming/online-compiler/`：成功取得頁面內容、無轉址（回傳的 `final_url` 與請求相同；未取得 HTTP 狀態碼），標題為「Online C++ Compiler (Editor)」，有 `main.cpp` 編輯區與 Run 按鈕 |
| 無法驗證 | 36 | 見下 |

### 無法驗證的 36 條

- **`https://www.onlinegdb.com/online_c++_compiler`（第 1 篇，1 條）**：兩次搜尋都沒有出現這個確切網址（只出現 `onlinegdb.com/<專案代碼>` 、`/fork/<代碼>` 與 `/online_c++_formatter` 等其他頁面），`web_fetch` 拒絕開啟。**無法驗證**。
- **`https://en.cppreference.com/w/...`（35 條）**：確切網址不在可開啟範圍；改開搜尋結果中的 `https://en.cppreference.com/cpp/container/vector` 時被 bot detection 擋下。**無法驗證**。
  - 觀察（不是驗證）：搜尋索引中該站的頁面出現的是不含 `/w/` 的形式（例如 `/cpp/container/vector`、`/cpp/header/vector`），與頁面使用的 `/w/cpp/...` 不同；是否為網站改版後的新網址、舊網址是否轉址，**未能確認**。請在瀏覽器實際點幾條；若確實轉到 `/cpp/...`，再決定是否全部改用最終網址（35 條規則一致，可用腳本批次改）。
  - 這 35 條包含：`/w/`（第 18 篇）、`/w/cpp`（第 1 篇）、`algorithm/sort`、`container/map`、`container/vector`、`container/vector/erase`、`error/exception`、`io/basic_fstream`、`io/cin`、`io/cout`、`io/manip/setprecision`、`language/access`、`array`、`class`、`cv`、`derived_class`、`for`、`functions`、`if`、`main_function`、`operator_arithmetic`、`operator_precedence`、`overload_resolution`、`pointer`、`reference`、`switch`、`types`、`virtual`、`while`、`memory/shared_ptr`、`memory/unique_ptr`、`numeric/random`、`numeric/random/mersenne_twister_engine`、`string/basic_string`、`string/basic_string/find`。

## 二、事實複查（會隨版本改變的內容）

| 頁面寫法 | 對照來源 | 結果 |
|---|---|---|
| 範例以 g++ 13、`-std=c++17`、`-Wall -Wextra` 實測，頁面輸出為實際執行結果 | 本機 g++ 13.3.0（Ubuntu 24.04）重跑 `run_examples.py`：181 個範例、問題 0；與頁面使用的 `results.json` 逐筆比對差異 0 | 一致（實測，非官方文件） |
| 逐行追蹤表、格式化試驗台、迴圈追蹤的 JS 模擬 == 真的 g++ | `check_eval.py`、`check_format.py`、`check_loop.py` | 2026-11-17 重跑：運算式 617 筆（另跳過除以 0 等 50 筆）、格式化 660 筆、迴圈 1000 筆，不一致皆為 0 |
| 第 1 篇：`sudo apt install g++`、WSL、MSYS2、VS Code 加外掛、Code::Blocks 的安裝與介面說法 | 未對照官方文件（`web_fetch` 無法開啟，也未取得官方頁面內容） | **無法驗證** |
| 第 1 篇：OnlineGDB／Programiz 的操作（按 Run、Input／stdin 欄位） | Programiz 頁面實際有 `main.cpp`、Run、Output；OnlineGDB 以 `onlinegdb.com` 上其他頁面（搜尋結果取得的範例／fork 頁，非頁面所寫的確切網址）的內容對照：編輯區提示「press "Run" button」、有「Standard Input: Interactive Console」區 | 操作說明一致；OnlineGDB 的確切連結仍無法驗證 |
| 各頁對 cppreference 條目的描述（標準庫、語言規則） | 無法開啟 cppreference；`std::vector` 等僅在鏡像站與搜尋摘要中看到相符內容，鏡像不算官方來源 | **無法驗證**（未逐項對照） |

## 三、結論與後續

- 頁尾與首頁 `foot` **不更新查證日期**：連結與事實兩項沒有全部完成。頁尾維持「安裝步驟與外部網站連結未逐一查證」，日期欄標示為製作日期（2026-11-12）。
- 建議：用瀏覽器逐條開啟 35 條 cppreference 與 OnlineGDB 連結並回報結果（含是否轉址），再更新本表與查證日期。

## 四、2026-11-18 使用者回報與處理

- 使用者在瀏覽器實際點開 #5 `/w/cpp/container/vector`、#10 `/w/cpp/io/cout`：兩者都轉址到不含 `/w/` 的最終網址（`https://en.cppreference.com/cpp/container/vector`、`https://en.cppreference.com/cpp/io/cout`）。
- 使用者另外隨機抽測 36 條連結，回報都可連結（未逐條列出哪些）。這是抽查，不等於逐條驗證。
- 處理：依「被轉址就改用最終網址」，把規格檔中 34 處（33 個不同網址）`en.cppreference.com/w/cpp/…` 改成 `en.cppreference.com/cpp/…`，重組並通過 `verify.py` 與 `verify_clang.py`。除 #5、#10 外，其餘是依同一規則推定，並非逐條確認。
- 保留不動：`https://en.cppreference.com/w/`（第 18 篇）與 `https://en.cppreference.com/w/cpp`（第 1 篇）。這兩條沒有被確認過轉址後的最終網址；舊網址目前可連結（在抽查範圍內），待使用者確認後再決定。
- 使用者說明抽查範圍為十篇，並判斷抽查已足夠（2026-11-18）。頁尾與首頁 `foot` 因此改為「外部連結已於 2026-11-18 抽查（非逐條驗證），安裝步驟未逐一對照官方文件」，並沒有寫成已全部驗證；`查證日期`欄仍不使用。第 1 篇安裝步驟與 cppreference 條目描述仍屬「無法驗證」。

## 五、2026-11-18 第二輪抽測（改寫後的網址）

使用者從已改寫的網址中隨機抽 5 條實際開啟：`/cpp/numeric/random`、`/cpp/language/cv`、`/cpp/container/map`、`/cpp/language/array`、`/cpp/language/class`。結果：全部可開啟、條目與頁面用途相符、沒有再轉址。至此改寫後的網址共 7 條已由使用者實際開啟（含前述 `/cpp/container/vector`、`/cpp/io/cout`），其餘 26 條仍是依規則推定；`/w/` 與 `/w/cpp` 兩條仍未確認最終網址。
