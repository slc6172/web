# _build · 製作與維護指南

> 給接手的人，或新對話的 Claude：**要修改頁面、新增篇章或新增主題前，先讀完這份**；動到某個主題時，再讀該主題資料夾裡的 `README.md`。
> `_build/` 不會被部署；只有 `public/` 會上線。部署相關檔案（`.github/workflows/deploy.yml`、`wrangler.jsonc`、`.gitignore`）由專案擁有者自行維護，**不要改它們**；部署流程與網址規則寫在根目錄 `README.md` 的「部署」。`deploy.yml` 會先檢查 `public/` 是否為 `site_files.py` 的最新輸出、再跑 `verify.py`，通過才 `wrangler deploy`，不建置頁面；所以改完頁面要先在本機跑 `site_files.py` 與 `verify.py` 並 commit `public/`，再 push，否則部署會失敗。

## 1. 一句話

`public/` 裡的每一頁都是單檔 HTML，由 `_build/<主題>/` 裡的規格檔（`SPEC`）經 `_build/build.py` 組出來，首頁 `public/index.html` 的 `SITE` 物件列出所有主題與篇章。**每一頁都用 `/html-effective` 的原則製作**，三個主題共用同一組設計 tokens 與元件，看起來必須是同一個家族。

## 2. 資料夾地圖

```text
_build/
├── README.md            本文件（總入口）
├── build.py             統一組頁工具；檔內 THEMES 登記每個主題的差異
├── verify.py            全站瀏覽器驗證（Playwright）
├── update_index.py      改首頁某主題的 status，並整理首頁全形標點
├── site_files.py        站台層：把 head 中繼資料與 skip link 就地套到 public/ 全部頁面，並產生 robots.txt、sitemap.xml、_headers
├── merge_theme.py       把另一份專案裡新做的主題整併進來（見第 11 節）
├── shared/              所有主題共用
│   ├── common.js        每頁內嵌的共用互動（複製、測驗、檢查表、模擬、視角/階段切換…）
│   ├── h.py             HTML 輔助函式（cmd、step、table、fill、sim、checks、resources…）
│   ├── fw.py            全形標點轉換
│   ├── pwutil.py        Playwright 驗證共用：stub_analytics（攔下 Cloudflare Web Analytics 的請求）
│   └── seo.py           站台層設定：SITE_URL、description／canonical／Open Graph／favicon／theme-color、skip link
├── github/              p1 … p11（沒有 p6：PR 頁是手寫的原始樣板）；README.md、reports/link-check.md
├── arduino/             a01 … a20、bb.py（接線圖）、arduino.css/.js、驗證工具、tools/、reports/；README.md
└── microfilm/           m1 … m16、mh.py、svgkit.py、kit.js（繪圖積木）、check.py；README.md
```

規格檔放在哪個主題資料夾，由檔名開頭決定：`p*` = github、`a*` = arduino、`m*` = microfilm。

## 3. 常用指令（都在 repo 根目錄執行）

```bash
python3 _build/build.py p3                 # 重組 github 第 3 篇 → public/github/
python3 _build/build.py a05 a06            # 一次多個；可混用不同主題
python3 _build/build.py --all microfilm    # 重組某主題全部頁面（github / arduino / microfilm / all）
python3 _build/build.py --out /tmp/x m1    # 改寫到別的資料夾，不動 public/（拿來比對）

python3 _build/update_index.py microfilm done 7 8   # 首頁把微電影第 7、8 篇改成 done
python3 _build/site_files.py               # 補齊全站 head／skip link，重新產生 sitemap.xml、robots.txt、_headers（新增主題或改 SITE_URL 後必跑）
python3 _build/merge_theme.py NEW.zip --dry-run   # 先看另一份專案的新主題會怎麼整併（第 11 節）
python3 _build/verify.py                   # 全站驗證；先 pip install playwright && playwright install chromium
                                           # 或設 CHROME_PATH 指向 Chrome
python3 _build/microfilm/check.py angle lens --shot # 微電影單頁快速檢查
python3 _build/arduino/verify_arduino.py   # Arduino 專用驗證（互動、首頁）
python3 _build/arduino/arduino_verify.py a03 # Arduino 電路與程式驗證（需要 tools/setup_env.sh 的環境）
```

微電影的繪圖需要 `node`；其他主題只需要 Python 3。

**發佈流程**（`deploy.yml` 會在雲端重跑第 2、3 步，任一步失敗就不部署）：

1. 改規格檔 → `build.py` 重組頁面（改首頁就直接改 `public/index.html`）。
2. `python3 _build/site_files.py`：補齊 head／skip link／全形標點，更新 sitemap。
3. `python3 _build/verify.py`：全站驗證要 `ERRORS: []`。
4. commit（含 `public/`）並 push 到 `main` → GitHub Actions 部署到 Cloudflare Workers。

專案根目錄另有 `wrangler.jsonc`、`.github/workflows/deploy.yml`、`.gitignore`、`LICENSE`，由擁有者維護，工具不會改動，打包上傳用 zip 時要保留。

## 4. SPEC 欄位（規格檔 `SPEC = {...}`）

| 欄位 | 說明 |
|---|---|
| `file` | 輸出檔名，例如 `github-start-guide.html` |
| `dir` | 主題資料夾：`github`（可省略）、`arduino`、`microfilm`。決定輸出位置、頁首「回教學首頁」連結（`../index.html#<dir>`）與樣式設定 |
| `title` `eyebrow` `h1` `sub` `tldr` | 頁首文字。`tldr` 裡的強調用 `<strong>`，不要用 `<b>`（CSS 會把 `.tldr b` 當成標籤樣式） |
| `toc` | 左欄目錄，`[(id, 標題), …]`，8 項以內 |
| `body` | 主體 HTML |
| `config` | 寫進 `window.PAGE`：`fill`、`sim`、`quiz`，可選 `stages`、`decide` 等 |
| `prev` `next` | `(檔名, 標題)` 或 `None`；檔案還不存在時會顯示「製作中」的虛線卡片 |
| `topic` `foot` | 頁首 eyebrow 前綴、頁尾文字；省略時用 `build.py` 裡該主題的預設值 |
| `desc` | 選填。`<meta name="description">` 與 `og:description`；省略時由 `tldr` 純文字取約 90 字（含全形化）。每頁不得與其他頁重複 |
| `css` `js` `pre_js` | 頁面專屬的額外樣式、`<script>`（接在 `common.js` 之後）、`window.PAGE` 之後插入的 script |

新增一頁的最短流程：複製同主題最接近的規格檔 → 改內容 → `build.py <檔名>` → 在首頁 `SITE` 新增或把 `status` 改成 `"done"` → `python3 _build/site_files.py`（更新 sitemap）→ `verify.py` → 用瀏覽器實際看一次。

## 5. 首頁 `SITE`（`public/index.html`）

首頁的標籤頁、路徑圖、快速入口、卡片、篩選、進度都由 `SITE` 產生，**新增主題或篇章不需要改首頁的程式碼**。

```js
{ id:"github", label:"GitHub",
  hero:{ h1:"…", sub:"…", tldr:"…" },          // tldr 不含 "TL;DR" 字樣（標籤已在 HTML 裡）
  pathTitle:"…", pathNote:"…", foot:"…",        // 切換標籤時會自動換字
  stages:[ { name:"一、入門", pages:[
    { n:1, title:"…", href:"github/github-start-guide.html", status:"done",
      level:"入門", mins:12, elective:false, summary:"…" } ]} ],
  quick:[ { t:"push 被拒絕（403 / rejected）", n:4, a:"gotchas" } ] }
```

- 標籤順序就是 `SITE` 的順序（目前 github → arduino → microfilm）；最後會自動多一個停用的「更多主題」佔位。網址 `#<id>` 對應分類，每頁的「← 回教學首頁」也靠它回到自己的標籤頁。
- `quick` 的 `a` 是目標頁內的 section id（必須存在於該頁），快速入口會連到 `頁面#a`；每一項都要有 `a`，`verify.py` 會檢查。
- `status:"planned"` 的卡片不可點，快速入口也會自動變成不可點。
- 已讀進度的 key 是 `gh-guide-read`，每筆是 `<分類id>:<篇號>`。**不要重排 `n`**，否則使用者既有的進度會對錯位置。`quick` 的 `n` 指的是該分類的篇號。
- 等級名稱（`level`）目前有：入門、基礎、協作、進階、附錄、實作。

## 6. 設計規範（所有主題一致）

**硬規則**
- 單檔、零依賴：CSS 在 `<style>`、JS 在 `<script>`；不用框架、CDN、網路字型、外部圖片，不發網路請求；圖像用內嵌 SVG 或 CSS。**唯一的選用例外**是 Cloudflare Web Analytics：`shared/seo.py` 的 `ANALYTICS_TOKEN` 非空時，`seo.apply()` 會在每頁 `</body>` 前輸出 `https://static.cloudflareinsights.com/beacon.min.js`（留空則完全不輸出）。要開關只改這一處再跑 `site_files.py`，**不要手貼到頁面或規格檔**（重組會被洗掉）。若日後在 `_headers` 加 CSP，要放行 `static.cloudflareinsights.com` 與 `cloudflareinsights.com`。
- 一律 `<!doctype html>` + `lang="zh-Hant"` + charset + viewport，`<title>` 要具體。
- 顏色只用 `:root` 變數（SVG 屬性可寫字面色碼，但必須取自同一組 token）。
- **`localStorage` 只有兩個例外**：首頁的「已讀進度」、微電影第 15 篇的分鏡編輯器；一律包 try/catch，失敗時退回記憶體變數，頁面不得壞掉。其他頁面不使用。
- 外部連結：GitHub 主題只連 `docs.github.com`；Arduino 主題只連 `docs.arduino.cc`、`support.arduino.cc`、`www.arduino.cc`；微電影主題不放未驗證的外部連結。

**Tokens（每頁 `:root` 逐字相同）**

```css
--ivory:#FAF9F5; --white:#FFFFFF; --slate:#141413;
--clay:#D97757; --clay-d:#B85C3E; --oat:#E3DACC; --olive:#788C5D; --rust:#B04A3F;
--gray-100:#F0EEE6; --gray-300:#D1CFC5; --gray-500:#87867F; --gray-700:#3D3D3A;
--border: 1.5px solid var(--gray-300);
```

語意色：clay＝焦點／注意／選中；olive＝成功／完成；rust＝危險／失敗；oat＝中性強調；slate＝墨色。字型：h1/h2/h3 與大數字用 serif（weight 500），內文 sans 15px／行高 1.65，eyebrow、標籤、chip、程式碼用 mono。圓角：面板 12、內層 8–10、膠囊 999；邊框 1.5px；不用漸層；陰影只用在「浮起」狀態。容器 `.page` 最大 1100px，`.layout` 為 190px 目錄＋內容，≤920px 折成單欄；斷點 920、720。

**站台層（由 `shared/seo.py` 統一輸出，規格檔不要手寫）**：每頁 `<head>` 有 description、canonical、`og:*`、`twitter:card`、內嵌 SVG favicon（data URI，零外部資源）、`theme-color`；`<body>` 第一個元素是 skip link（`.skip` → `#main`），`<main id="main" tabindex="-1">`。站台網址 `SITE_URL` 只在 `seo.py` 設定一處（目前 `https://www.slc6172.workers.dev`，必須與 `wrangler.jsonc` 的 `name` 加帳號子網域一致，`verify.py` 會檢查名稱部分）；留空時略過 canonical、`og:url` 與 sitemap。Workers Static Assets 預設會把 `/x.html` 轉成 `/x`（`wrangler.jsonc` 沒有設定 `html_handling`，已實測），所以 `CLEAN_URLS = True`：canonical、`og:url` 與 sitemap 都用沒有 `.html` 的網址，站內相對連結仍寫 `.html`（兩種都能開）。目前不放 og:image（維持零外部資源）。手寫頁（首頁、`github-pr-guide.html`）由 `site_files.py` 就地套用。

**固定元件與導覽**：頁首 `crumb`（← 回教學首頁，連到 `../index.html#<主題>`）→ eyebrow → h1（標題就是結論）→ `.sub` → `.tldr`；左欄 `nav.toc`；每頁必備複製按鈕、閱讀進度條、TOC 高亮、`details` 常見卡關、測驗（3–6 題）、檢查表；頁尾 `.foot` → `.pager`（上一篇／下一篇，第一頁沒有上一篇、最後一頁沒有下一篇）。**所有共用 CSS 都是從 `public/github/github-pr-guide.html` 的 `<style>` 讀來的**（`build.py` 啟動時讀取），要改共用樣式就改那一頁，再重組各頁；後來補的小型樣式放在 `build.py` 的 `EXTRA`。

**標點**：全站一律全形標點（，。；：（）！？）。三個主題在 `build.py` 的 `THEMES` 都設 `fw=True`，組頁時自動呼叫 `shared/fw.py` 轉換：只轉頁面文字、aria-label 與含中文的 JS 字串，不動 CSS、`<pre>`、`<code>`、程式碼與 SVG；中文後面的 `, : ; ? !`、包著中文的 `( )`、以及「英文／數字／`)` 後面接中文」的 `, : ;` 都會轉。首頁用 `update_index.py` 維護（會自動套用）。寫規格檔時直接寫全形也可以。補充規則（`fw.py`）：標籤（`</code>`、`</b>`…）後面緊接的 `, : ; ? !`、任何非中文字元後面接中文的 `, : ; ? !`、JS 字串（含 `\n` 跳脫）與 SVG 的 `<title>`／`<text>` 都會轉。**例外（刻意保留）**：只含英文的括號，例如 `(Windows)`、`R1(220Ω)`；程式碼（`<pre>`、`<code>`）內部；範例文字故意寫的半形。`site_files.py` 會對全站再套一次，所以手寫頁也會一致。**跨 JS 字串拆開的括號**（一個字串放 `(`、下一個放 `)`）轉不到，請在原始碼直接寫全形。

## 7. 重組頁面時要知道的事

- 重組出來的頁面**功能相同，但不一定與線上現有的檔案逐位元相同**：github 與微電影的頁面是在不同時期、用不同版本的 `common.js` / `kit.js` 組出來的，重組會換成目前最新版（只多了不影響其他頁的功能，例如 C++ 註解上色、空拍動畫）。Arduino 的 20 頁重組後與現有檔案逐位元相同。
- 只改某一頁時，只重組那一頁即可；不需要為了「統一版本」重組全部。
- `--out` 可以先組到暫存資料夾再比對，確認沒問題再覆蓋。
- `github/p6` 不存在：第 6 篇 PR 頁是手寫的原始樣板，也是共用 CSS 的來源，**不要用 build 覆蓋它**。

## 8. 新增一個主題

1. 建 `public/<主題>/`，檔名 `<主題>-<子題>-guide.html`。
2. 建 `_build/<主題>/`，放規格檔（用一個還沒被用過的字母開頭，如 `d01.py`）與一份 `README.md`（記錄該主題已確認的決定、內容規則、專用工具與驗證方式）。規格檔裡寫 `dir="<主題>"`。
3. 在 `build.py` 的 `THEMES` 新增一筆：`prefix`、`topic`（eyebrow 前綴）、`foot`（頁尾）、`css`／`js`（主題專用檔，沒有就 `None`）、`fw`（是否自動全形標點）、`uniq_svg`。
4. 在 `index.html` 的 `SITE` 新增分類（`id`、`label`、`hero`、`pathTitle`、`pathNote`、`foot`、`stages`、`quick`），首頁會自動多一個標籤頁。
5. 跑 `build.py`、`verify.py`；`verify.py` 會自動涵蓋 `public/` 底下的新資料夾，並檢查卡片數與檔案數相符、回首頁連結落在正確的標籤頁。
6. 更新根目錄 `README.md` 的主題表與本文件的資料夾地圖。
7. 首頁新分類的每個 `quick` 項目都要有 `a` 錨點；跑 `python3 _build/site_files.py` 更新 sitemap。

## 9. 每次改動後的驗證清單

- `python3 _build/verify.py`：每頁 1280 與 390 寬 `overflow: 0`、`ERRORS: []`。
- 沒有重複 id、沒有失效的相對連結或 `#錨點`（`verify.py` 會檢查）。
- 搜尋 `http://`、`https://`：只應出現在官方文件連結、SVG `xmlns`、`<head>` 的 canonical／`og:url`，以及選用的 Analytics beacon。`verify.py` 會檢查外部資源白名單：除了 canonical 與該 beacon，任何外部 `<script>`／`<link>`／`<img>`／`<iframe>` 來源都算錯誤。
- **寫 Playwright 驗證腳本時**，每個 `new_context()` 後都要呼叫 `shared/pwutil.py` 的 `stub_analytics(ctx)`：驗證用 `file://` 開頁（origin 為 null），beacon 的請求會被 CORS 擋下並產生 console error，導致 workflow 失敗；stub 會把 `cloudflareinsights.com` 與其子網域的請求用空回應攔下，不影響頁面本身。`verify.py`、`arduino/verify_arduino.py`、`microfilm/check.py` 都已套用。
- 子頁沒有 `localStorage`（第 6 節的例外除外）。
- `verify.py` 的站台層與部署檢查（`wrangler.jsonc` 的 `name` 要與 `SITE_URL` 一致、部署相關檔案要存在）：每頁 meta／canonical／og／favicon／theme-color／skip link／`main#main`、title 與 description 不重複、`sitemap.xml` 與 `public/` 頁面相符、`quick` 每個錨點都存在。
- **外部連結要實際開啟**（WebFetch 或瀏覽器；shell 通常連不到外網，不能當證據）：結果寫進 `_build/<主題>/reports/link-check.md`（日期、方法、每條狀態）；被轉址的改成最終網址；只拿到頁面外殼的算「無法驗證」，不能寫成已驗證。介面名稱、指令、規格、額度逐項對照官方文件，查證日期在這些做完之後才更新。
- 用瀏覽器實際點過：複製按鈕、測驗、檢查表、模擬與該頁特有的互動；窄螢幕也看一次。
- 頁尾的查證日期與首頁 `foot` 同步更新；時效性內容（介面名稱、規格、價格、額度）先對照官方文件再寫。

## 10. 交給新對話的開場白

> 這是一個由 `/html-effective` 製作的多主題教學站（github、arduino、microfilm）。請先讀 `README.md` 與 `_build/README.md`，再讀 `_build/<主題>/README.md`、`public/github/github-pr-guide.html`（樣板）、該主題最接近的規格檔與 `_build/build.py`。我要【修改某一頁／新增某一篇／新增一個主題】，每一頁都分別用 `/html-effective` 製作並維持既有風格。已記錄在各 README 的決定不要再問我；遇到文件沒涵蓋的新決定，動手前先問我。不要改 `.github/workflows/`、`wrangler.jsonc`、`.gitignore`。

上傳給新對話時，附上整個 repo 的 zip（或至少 `public/index.html`、`_build/` 與要改的頁面）即可；文件已經涵蓋原本分散在各份交接檔的內容。

## 11. 整併「另一份專案」裡新做的主題

情境：別的對話做了一份專案（含 `github` 主題當風格參考，再加一個新主題），要把新主題整併進本專案。流程是「程式做機械的部分，人（或 Claude）做判斷的部分」。

**第一步：交給程式（`merge_theme.py`）**

```bash
python3 _build/merge_theme.py NEW.zip --dry-run          # 只分析不寫入：會整併哪個主題、有哪些風險
python3 _build/merge_theme.py NEW.zip                    # 整併（自動找出本專案沒有的主題；有多個時加 --theme <id>）
python3 _build/merge_theme.py NEW.zip --verify --zip /tmp/learning-hub-github-upload.zip   # 順便全站驗證並打包上傳用 zip
```

程式會自動：複製 `public/<主題>/`；把來源首頁 SITE 的該分類轉成本專案的格式並插到最後；每頁「回教學首頁」改成 `#<主題>`；頁面與首頁轉全形標點；檢查設計 tokens 是否與 github 樣板一致、`localStorage`、外部連結與 prev/next；把製作檔放進 `_build/<主題>/`；在 `build.py` 加一筆暫定 THEMES；更新根目錄 README 與本文件的主題表、資料夾地圖。**來源的 github 主題只當風格參考，不會帶入；HANDOFF、DESIGN、進度檔等過程文件不會帶入。**最後會印出「請人工確認」清單。

**第二步：判斷型工作（程式做不到，要逐項處理）**

1. `build.py` 的 `THEMES` 暫定設定：對照來源的 `build.py`，確認 `topic`、`foot`、`css`／`js`（主題專用檔）、`fw`、`uniq_svg`，並把來源 `build()` 裡的特殊處理合併進統一版。
2. `_build/<主題>/_incoming/`：與共用檔同名但內容不同的檔案（各附 `.diff`）。多半只是來源版本較舊，丟掉即可；若來源含本專案 `shared/` 沒有的新函式或功能，合併進 `shared/`，並確認舊主題的組頁結果沒有被改壞（`build.py --all <主題> --out /tmp/x` 比對）。
3. 把 `_incoming/` 裡的規劃文件濃縮成 `_build/<主題>/README.md`（已確認的決定、內容規則、專用工具與驗證方式），完成後刪掉 `_incoming/`。
4. 製作檔若自己推算路徑（`dirname(HERE)` 之類），要改成往上兩層；專用驗證腳本跑一次確認可用。
5. 根目錄 `README.md`：主題表的說明欄、查證日期、設計原則裡與新主題有關的句子；若新主題有 `localStorage` 等例外，也要寫進本文件第 6 節。
6. 首頁 `foot` 與各頁頁尾的查證文字是否適用新主題。
7. **站台層品質關卡**：①外部連結逐條實際開啟並寫 `_build/<主題>/reports/link-check.md`，事實逐項對照官方文件，之後才更新查證日期；②每頁有 `desc`（或可由 `tldr` 衍生）、title 與 description 不與他頁重複，跑 `site_files.py` 更新 sitemap；③首頁新分類每個 `quick` 項都有 `a` 錨點；④根目錄 `README.md` 與本文件同步。`SITE_URL` 空白時要問人，不要編造。

**第三步：驗證與打包**：`python3 _build/verify.py`（全站）→ 主題專用驗證 → 確認沒有殘留的過程文件與暫存檔 → 用 `--zip` 打包（不含 `_incoming`、`__pycache__`、編譯產物）。

**交給新對話的提示詞**：完整版在專案外的 `merge-theme-prompt.md`（同時上傳目前的 learning-hub zip 與新專案 zip）；精簡版如下，兩者要同步。

> 我有一份現行的教學站專案（learning-hub，已含 github 等主題）和另一份新專案 `NEW.zip`（含 github 主題當風格參考，外加一個新主題）。請把新主題整併進現行專案。
> 先讀 `README.md`、`_build/README.md`（特別是第 11 節），確認 `_build/shared/seo.py` 與 `_build/site_files.py` 存在（缺就先停下來告訴我）。然後依序：①先跑 `merge_theme.py --dry-run` 並把結果與風險告訴我；②我確認後再正式整併；③完成第 11 節「第二步」的每一項（含第 7 項站台層品質關卡）；④跑 `site_files.py`、全站驗證與主題專用驗證；⑤用 `--zip` 打包上傳用 zip，確認裡面沒有 HANDOFF、DESIGN、進度檔、截圖或暫存檔，且**保留**根目錄的 `.github/`、`wrangler.jsonc`、`.gitignore`、`LICENSE`。
> 原則：只動新主題與首頁、文件，不改既有主題的頁面內容（`<head>`、skip link、sitemap 這類站台層輸出除外）；全站全形標點；每一頁維持與 github 相同的風格與元件；沒實際開啟過的連結不要宣稱已驗證；不要碰 `.github/workflows/`、`wrangler.jsonc`、`.gitignore`。遇到文件沒涵蓋的決定，動手前先問我。
