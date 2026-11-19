# datastruct（C++ 演算法與資料結構）· 製作指南

> 先讀 `../README.md`（總入口）。這份只記錄 datastruct 主題自己的決定、規則與工具。來源規劃文件（`SPEC-datastruct.md`）與進度檔已濃縮於此，不再保留。

## 1. 主題概況

- 17 篇單檔 HTML，在 `public/datastruct/datastruct-<slug>-guide.html`；規格檔 `d01.py … d17.py`（`dNN.py` ＝ 第 NN 篇）；首頁分類 id `datastruct`，標籤「C++ 演算法」，網址 `#datastruct`。
- 讀者：剛學完 C++17、實際寫過的程式很少、沒學過演算法的人。先備：變數、`if`/`for`/`while`、函式、陣列、`vector`、`string`、基本 `struct`；指標、參照、`new`/`delete`、lambda 由第 1 篇「先備速查」與各頁就地的 `.tip` 補。
- 難度：第 1–3 篇入門、4–8 篇基礎、9–14 篇進階；第 1–8 篇是主線，第 15–17 篇（Dijkstra、動態規劃、貪婪回溯與練習）是進階選讀；第 1 篇可略過。每頁最多 3 個新概念。

| n | slug | 標題 | 主互動 |
|---|---|---|---|
| 1 | prereq | 先備速查：指標、參照與 struct | 記憶體格子（變數、參照、指標、`new`） |
| 2 | bigo | 複雜度與 Big‑O | n 滑桿看六種成長曲線；「這段程式是 O(?)」 |
| 3 | array | 陣列與 vector | 中間插入／刪除逐格位移；`push_back` 擴容 |
| 4 | linkedlist | 鏈結串列 | 節點箭頭圖，逐行顯示指標改寫 |
| 5 | stackqueue | 堆疊與佇列 | push/pop、enqueue/dequeue；括號配對 |
| 6 | search | 搜尋：線性與二分 | 並排比較、計比較次數 |
| 7 | recursion | 遞迴 | 呼叫堆疊＋呼叫樹；費氏重複計算標紅 |
| 8 | sortbasic | 基礎排序 | 長條圖，顯示比較與交換次數 |
| 9 | sortadv | 進階排序與 `std::sort` | 分治過程、並排比較 |
| 10 | hash | 雜湊表 | 桶子圖，輸入 key 看雜湊與碰撞 |
| 11 | tree | 二元樹與走訪 | 四種走訪高亮、輸出序列累積 |
| 12 | bst | 二元搜尋樹 | 插入、搜尋、刪除三種情況；退化成鏈 |
| 13 | heap | 堆積與優先佇列 | 陣列與樹並排；上浮、下沉 |
| 14 | graph | 圖的表示與 BFS/DFS | 格子迷宮、鄰接矩陣／表 |
| 15 | dijkstra | 最短路徑：Dijkstra | 距離表逐步更新 |
| 16 | dp | 動態規劃入門 | DP 表逐格填、點格子看依賴 |
| 17 | greedy | 貪婪、回溯與練習路線 | 找零、N 皇后、可篩選的 STL 速查表 |

## 2. 內容規則（已確認，不要再問）

- 每頁骨架：頁首（crumb、eyebrow「C++ 演算法 · 第 N 篇 · 子題」、h1 結論式標題、`.sub`、TL;DR 含先備／時間／難度）→ 直覺（生活比喻＋名詞表）→ 動手玩（主互動，最顯眼處）→ 完整可編譯程式與預期輸出 → 複雜度小表 → 常見錯誤（`details`）→ 動手寫 1–2 題（答案折疊）→ 測驗 → 檢查表 → 連結 → 頁尾 → 上一篇／下一篇。目錄 ≤ 8 項。
- 程式風格：`std::` 明寫（不用 `using namespace std;`）；索引用 `int`，第 3 篇講清楚 `size_t` 後用 `static_cast<int>(v.size())`；鏈結串列與樹用原始指標加 `new`/`delete`，初學階段不引入 `unique_ptr`；找不到回傳 `-1`；範例前期 ≤ 30 行、後期最長約 60 行。
- **所有範例都實際編譯執行**：`g++ -std=c++17 -Wall -Wextra`（g++ 13），零警告；頁面不內嵌編譯器。例外：動手寫題的 `*_starter.cpp`（未完成的題目，可有未使用變數警告、沒有輸出檔）、`linked_wrong.cpp`（可編譯、不執行的錯誤示範）、`rec_infinite.cpp`（沒有 `main`，只拿來看警告）。
- 外部連結只連 `en.cppreference.com` 的 C++ 頁面，一律用**不含 `/w/`** 的最終網址（與 clang 主題相同）；不放其他外部資源。`verify_ds.py` 與 `verify.py` 都會檢查。
- 動畫尊重 `prefers-reduced-motion`；390 寬沒有橫向捲動、動畫在上程式碼在下；Big‑O 只數操作次數，不做瀏覽器計時；子頁不使用 `localStorage`。
- 測驗：`dh.py` 覆寫 `quiz_cfg`，去掉選項與 why 的 HTML 標籤，並依題號固定錯開正解位置（1,2,0,2,1,0 循環）。
- 首頁快速入口的 `n` 是該分類的篇號；`a` 是目標頁的 section id（目前：慢→2#what、指標→1#node、找值→6#what、遞迴→7#play、排序→9#race、vector/map/set→17#stl、迷宮→14#maze、刷題→17#route）。

## 3. 資料夾與工具

```text
_build/datastruct/
├── d01.py … d17.py     各頁規格（SPEC 另有 modules、script、eyebrow_prefix 三個欄位，見下）
├── dh.py               組頁輔助：cpp(name)、out(name)、widget()、try_list()、compile_cmd()、quiz_cfg()、FOOT、EYEBROW
├── algo/               動畫模組：core.js/css（播放器 Algo.widget、C++ 高亮，必載）、繪圖器 cells／mem／list／tree／graph／grid／board／bars／buckets／curves／dpview／stlfilter，演算法 alg_*.js（純函式，產生 frame）
├── cpp/*.cpp           頁面上的所有範例原始碼（實際編譯過）
├── out/*.txt           對應的實測輸出
├── test_algo.js        Node 測試：演算法結果、frame 行號範圍、程式碼面板與 .cpp 一致
├── verify_ds.py        瀏覽器驗證：1280／390 溢出、JS 錯誤、每個 widget 逐步、測驗／檢查表、連結、外部資源
└── reports/link-check.md
```

- `SPEC` 的主題專用欄位：`modules=[…]`（只內嵌 `algo/` 裡列出的模組，`core` 一定內嵌）、`script`（頁面腳本，包成 IIFE 接在模組後）、`eyebrow_prefix`（等同統一版的 `topic`，`build.py` 兩者都吃）。`build.py` 的 `THEMES["datastruct"]` 以 `algo="algo"` 指定模組資料夾。
- 常用指令（repo 根目錄）：
  ```bash
  python3 _build/build.py d03                      # 重組第 3 篇；--all datastruct 重組全部
  node _build/datastruct/test_algo.js              # 演算法與程式碼面板測試
  python3 _build/datastruct/verify_ds.py [slug…]   # 專用瀏覽器驗證（CHROME_PATH 可指定瀏覽器）
  ```
- 新增或修改範例：寫 `cpp/<name>.cpp` → `g++ -std=c++17 -Wall -Wextra` 編譯（零警告）→ 輸出存 `out/<name>.txt` → 頁面用 `cpp("<name>")`、`out("<name>")` 引用。程式碼面板的行號用腳本從 `.cpp` 切出並對照；改 `.cpp` 後重跑 `test_algo.js`。

## 4. 踩過的坑

- **class 名稱會與基底 CSS 衝突**：基底已有 `.bar`、`.cell`、`.cmd`、`.cap`、`.gt`、`.row`。新模組的 class 要加前綴或限定在自己的容器下（如 `.cells .cell`、`.sbar`），並與 `public/github/github-pr-guide.html` 的 `<style>` 比對。
- 表格新欄數要補 CSS（如 `.gt.g4`、`.gt.g5`）；`verify_ds.py` 會檢查可見表格格子 ≥ 50px 寬。`.cmd .cap` 預設全大寫，`core.css` 對 `.algo-code`／`.cmd.out` 關掉。
- **frame 不能共用可變物件**：會繼續被修改的 object／array 要複製進 frame（`Object.assign({}, txt)`），否則前面的步驟會顯示後面才出現的數字；`test_algo.js` 有對應檢查。
- widget 的 stateless 用法：`make` 不回傳 `result`、`init` 回傳 null，每次按「執行」都從頭開始（迷宮、圖表示法、Dijkstra）；固定程式的 widget 用 `form:[]` 後 `.run({})`。
- 二維表在手機上用 `.dpkeep` 包起來，整張表一起橫向捲動。`tree.js` 的 `tree.bst = true` 讓 BST 單一子節點斜向偏移，其餘頁面不設此旗標。
- `common.js` 不洗牌測驗選項、會跳脫選項與 why，所以才有 `quiz_cfg` 覆寫。

## 5. 驗證與查證狀態

- 驗證：`test_algo.js`、`verify_ds.py`、全站 `verify.py` 都要通過。
- 外部連結與事實查證結果見 `reports/link-check.md`。cppreference 官方站會擋自動化存取，所以 30 條連結由使用者在 2026-11-18 於瀏覽器逐條開啟確認（皆正確）；頁尾與首頁 `foot` 的查證日期因此是 2026-11-18。`std::` 函式的說明內容尚未逐句對照官方頁，僅以 g++ 實測的範例行為支持，之後若要補，請記在 `reports/link-check.md` 的事實複查表。
