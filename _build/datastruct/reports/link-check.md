# datastruct · 外部連結與事實查證

- 檢查日期：2026-11-18
- 方法：先以 web_fetch／web_search 嘗試（被擋）；再由使用者在瀏覽器逐條開啟。shell 沒有外網，不能當證據。

## 結果摘要

- 外部連結共 30 條，**全部是 `en.cppreference.com`**，網址都是不含 `/w/` 的最終形式（來源專案的 35 處 `/w/` 連結已改掉，依據 clang 主題的既有規則與搜尋結果中 `vector` 頁的官方網址）。
- 2026-11-18 自動化查證失敗：官方站擋 web_fetch（bot detection），其餘頁面也沒出現在搜尋結果裡。
- **2026-11-18 由使用者在瀏覽器逐條開啟，30 條都正確**（能開啟、是官方頁、沒有被轉址到別的網址）。下表狀態以此為準。

## 連結清單

| 網址 | 出現在 | 狀態 |
|---|---|---|
| `https://en.cppreference.com/cpp/language/pointer` | d01 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/language/reference` | d01 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/language/lambda` | d01 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/language/new` | d01 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/container/vector/push_back` | d02 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/container/vector` | d03、d16 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/container/vector/insert` | d03 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/container/vector/erase` | d03 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/container/vector/capacity` | d03 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/container/vector/reserve` | d03 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/container/list` | d04 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/container/forward_list` | d04 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/container/stack` | d05、d14 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/container/queue` | d05、d14 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/algorithm/find` | d06 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/algorithm/binary_search` | d06 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/algorithm/lower_bound` | d06 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/algorithm/sort` | d08、d09 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/algorithm/swap` | d08 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/algorithm/stable_sort` | d09 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/container/unordered_map` | d10 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/container/unordered_set` | d10 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/container/set` | d12 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/container/map` | d12 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/container/priority_queue` | d13、d15 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/algorithm/make_heap` | d13 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/utility/functional/greater` | d15 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/algorithm/max` | d16 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/container` | d17 | 使用者於 2026-11-18 開啟確認 |
| `https://en.cppreference.com/cpp/algorithm` | d17 | 使用者於 2026-11-18 開啟確認 |

## 事實複查

| 項目 | 頁面寫法 | 對照結果 | 是否一致 |
|---|---|---|---|
| 編譯指令與旗標 | `g++ -std=c++17 -Wall -Wextra -o main main.cpp` | 2026-11-18 以 g++ 13.3.0（Ubuntu 24.04）實際編譯 | 一致 |
| 範例輸出 | 117 個 `cpp/*.cpp` 對應 `out/*.txt` | 全部重新編譯執行：輸出與頁面一致，**零警告**（`*_starter.cpp` 有未使用變數警告，屬刻意）；`linked_wrong.cpp` 無 `main`、`rec_infinite.cpp` 為刻意的錯誤示範 | 一致 |
| `rec_infinite` 警告 | `warning: infinite recursion detected [-Winfinite-recursion]` | g++ 13.3 實際輸出相同 | 一致 |
| 演算法動畫 | frame 數、最終結果、程式碼行號 | `node _build/datastruct/test_algo.js`：380916 項檢查通過 | 一致 |
| `std::` 函式行為（`lower_bound`、`priority_queue`、`std::greater`、`make_heap`、`stable_sort` 等）| 各頁的說明 | 連結已確認可開啟，但**說明內容尚未逐句對照官方頁**；僅以 g++ 實測的範例行為支持 | 部分驗證 |
| `vector` 擴容 1→2→4→8 | 第 3 篇 | g++（libstdc++）實測輸出；這是實作細節，標準沒有規定倍數 | 實測一致 |

沒有價格、額度或介面按鈕名稱類的時效性內容。
