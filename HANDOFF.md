# HANDOFF:GitHub 教學站的後續擴充

> 給接手的人(或新對話的 Claude)。先讀完本文件,再讀 `DESIGN.md`(設計規範與各篇大綱),就能接著做。
> 狀態截至 2026-11-06:11 篇 GitHub 教學與首頁全部完成,已通過瀏覽器驗證。

## 1. 現況一句話

靜態教學站:`index.html`(多主題標籤頁首頁)+ `github/` 內 11 篇單檔 HTML。每頁零依賴、內嵌 CSS 與 JS。**只有 `public/` 底下的東西會被 GitHub Actions 推送到 Cloudflare Workers static assets**,所以 `index.html` 與主題資料夾都必須在 `public/` 裡;文件與 `_build/` 放 repo 根目錄、不會被部署。`deploy.yml` 由使用者自行維護,不在本文件範圍,也不要動它。

## 2. 檔案地圖

```text
DESIGN.md                          設計規範、元件清單、各篇大綱(權威文件)
README.md                          repo 說明
HANDOFF.md                         本文件
_build/                            製作工具(見第 4 節;不部署)
public/                            ← 唯一會被部署的資料夾
  index.html                       首頁。資料在檔案內的 SITE 物件
  github/
  github-start-guide.html          1  第一次推送
  github-gitignore-guide.html      2  .gitignore 與歷史
  github-branch-guide.html         3  分支、合併、衝突
  github-remote-guide.html         4  遠端與同步、登入驗證
  github-issues-guide.html         5  Issue 與 Projects      [雙視角]
  github-pr-guide.html             6  Pull Request           [雙視角,原始樣板,手寫]
  github-review-guide.html         7  Code Review 與規範     [雙視角,進階選讀]
  github-undo-guide.html           8  還原與救援(含決策選擇器)
  github-release-guide.html        9  Release 與版本號
  github-security-guide.html       10 安全性                 [進階選讀]
  github-actions-guide.html        11 Actions 與 Pages       [進階選讀]
```

`index.html` 與主題資料夾必須同層(都在 `public/` 下),頁面間用相對路徑連結。

## 3. 設計不變量(改任何一頁前先記住)

- **單檔、零依賴**:不用框架、CDN、網路字型、外部圖片;不發網路請求。連結只允許指向 `docs.github.com` 官方文件。
- **教學頁不使用 `localStorage`**。唯一例外是 `index.html` 的「已讀進度」,且一律包在 try/catch,失敗時退回記憶體。
- **色彩 tokens 逐字一致**(`:root` 變數,見 `DESIGN.md` 第 2 節)。所有頁面的 CSS 都是從 `github-pr-guide.html` 複製而來,不要各頁自行微調。
- **字型分工**:serif 給 h1/h2/h3 與大數字,sans 給內文,mono 給 eyebrow、標籤、chip、程式碼。
- **每頁固定元件**:頁首「← 回教學首頁」、TL;DR、TOC、全貌圖(SVG)、步驟(為什麼/要打什麼/你會看到)、常見卡關(`details`)、測驗、檢查表、官方文件連結、頁尾「上一篇 / 下一篇」、「按鈕名稱以 GitHub 英文介面為準」與查證日期。
- **語言**:繁體中文;按鈕與選單名稱保留 GitHub 英文原文。
- **檔名**:`<主題>-<子題>-guide.html`,放在 `<主題>/` 資料夾。
- TL;DR 裡強調用 `<strong>`,不要用 `<b>`(CSS 會把 `.tldr b` 當標籤樣式,變成大寫等寬字)。

## 4. 製作工具 `_build/`

頁面不是手寫 HTML,而是用 Python 組出來(PR 頁例外,是原始手寫檔)。

| 檔案 | 作用 |
|---|---|
| `common.js` | 所有頁面共用的互動:填入資料換指令、複製按鈕、閱讀進度條、TOC 高亮、情境模擬、測驗、檢查表、視角切換(`data-role` / `data-panel`)、階段切換(`#stages`)、決策選擇器(`#decideBtns`) |
| `h.py` | HTML 輔助函式:`cmd`、`step`、`steps`、`details`、`table`、`section`、`fill`、`sim`、`checks`、`resources`、`canvas`、`quiz_cfg` 等 |
| `build.py` | 讀取 `github-pr-guide.html` 的 CSS 與 `common.js`,依頁面 `SPEC` 組成完整 HTML,寫到 `github/` |
| `p1.py` … `p11.py`(缺 `p6.py`) | 各頁內容,每個檔案匯出一個 `SPEC` |
| `verify.py` | Playwright 驗證:1280 與 390 寬無橫向溢出、無 JS 錯誤、首頁篩選與進度、各頁測驗與檢查表與互動 |

### 新增或修改一頁

1. 複製最接近的 `pN.py`(單視角看 `p3.py`;雙視角看 `p5.py` / `p7.py`;有決策選擇器看 `p8.py`),改 `SPEC`。
2. 執行 `python3 build.py pN`(不含 `.py`)。
3. 到 `index.html` 的 `SITE` 加一筆(或把 `status` 改成 `"done"`)。
4. 執行 `verify.py`,並用瀏覽器實際看一次。

`SPEC` 欄位:`file`、`title`、`eyebrow`、`h1`、`sub`、`tldr`、`toc`、`body`、`config`(`fill`、`sim`、`quiz`,可選 `stages`、`decide`)、`prev`、`next`(皆為 `(檔名, 標題)` 或 `None`)。

### 使用前必須改的地方

- `build.py` 與 `verify.py` 以自身位置推算路徑:假設 `_build/` 與 `public/` 同在 repo 根目錄。只要維持這個相對位置,不需要改路徑。
- `verify.py` 預設用 `/usr/bin/google-chrome`;換環境時設環境變數 `CHROME_PATH`。需要 `pip install playwright`。
- 執行方式:在 repo 根目錄 `python3 _build/build.py p3`、`python3 _build/verify.py`。
- **改共用樣式要改 `github-pr-guide.html`**(CSS 來源),再重新 build 全部頁面;`build.py` 的 `EXTRA` 變數放後來補的小型樣式。

## 5. 頁面與首頁的資料約定

### 首頁 `SITE`

```js
{ id:"github", label:"GitHub", stages:[
    { name:"一、入門", pages:[
        { n:1, title:"…", href:"github/github-start-guide.html", status:"done",
          level:"入門", mins:12, elective:false, summary:"…" } ]}
  ],
  quick:[ { t:"push 被拒絕(403 / rejected)", n:4 } ]
}
```

- `status:"planned"` 的卡片不可點,快速入口也會自動變成不可點。
- 標籤列自動多一個停用的「更多主題」佔位;`#github` 這類網址 hash 對應分類 `id`。
- 已讀進度的 key 是 `gh-guide-read`,每筆是 `<分類id>:<篇號>`。**改篇號會讓使用者既有進度對錯位置**,盡量不要重排 `n`。

### 模板語法

- `.cmd pre` 與帶 `data-tpl` 的元素會把 `{key}` 換成使用者填入的值;可用的 key 由該頁 `config.fill` 決定。沒有定義的 `{xxx}` 會原樣保留。
- 程式碼區若含 `{{ … }}`(GitHub Actions 語法)不受影響,因為它含空白與句點,不符合 key 規則。
- 測驗題的 `q` 欄位用 `innerHTML` 顯示,可以放 `<code>`;選項 `a` 是純文字,**不要放 HTML**。

## 6. 踩過的坑

1. **重複的 id**:區塊 `id="stages"` 與階段切換的 `id="stages"` 撞名,`getElementById` 先拿到區塊,整段被覆寫,按鈕消失。區塊 id 請用 `states` 等不同名字。新增頁面後檢查是否有重複 id(見第 8 節)。
2. **CSS 繼承**:`.tldr b` 在 PR 頁樣式裡是標籤樣式,TL;DR 內文強調要用 `<strong>`。
3. **選項不可含 HTML**:測驗選項用 `textContent`,放 `<code>` 會被當成文字顯示。
4. **語言細節**:全站用「全形標點」與繁體中文;`go` 標籤等 mono 文字保持英文。
5. **步驟裡的指令要真的能跑**:每個範例都用假資料(`hello-world`、`your-name`),不要放真實帳號或金鑰。

## 7. 內容查證狀態(更新時優先複查)

GitHub 介面與功能變動快。以下為查證情況:

| 篇 | 狀態 |
|---|---|
| 7 Code Review | Ruleset 路徑(Settings → Rules → Rulesets → New ruleset → New branch ruleset)與 CODEOWNERS 三個放置位置,已對照官方文件。各條規則的確切名稱官方頁面未列出,頁面上寫「以畫面為準」 |
| 9 Release | 按鈕名稱(Draft a new release、Generate release notes、Set as a pre-release、Publish release、Save draft)已對照官方文件 |
| 10 安全性 | push protection 預設行為、Dependabot alerts 的設定路徑、`dependabot.yml` 範例、`git filter-repo` 建議與風險、Actions secrets 路徑,已對照官方文件 |
| 11 Actions 與 Pages | workflow 範例、Actions 分頁操作、Pages Source 選項、免費額度,已對照官方文件。**Pages 在私人 repo 的可用性** 與 **專案網站網址格式** 未由官方頁面確認 |
| 1、2、3、4、5、8 | 主要依既有知識撰寫,**未逐頁對照官方文件**。第 4 篇的 Developer settings、SSH and GPG keys 路徑,第 5 篇的 Projects 介面與 Close as not planned 選項,建議優先複查 |
| 全部 | 頁尾的官方文件連結**未逐一打開驗證** |

查證日期寫在每頁頁尾與首頁頁尾(2026-11-06)。更新內容後請同步更新日期。

## 8. 驗證清單(每次改動後)

- 執行 `verify.py`:全部頁面 1280 與 390 寬 `overflow: 0`、`ERRORS: []`。
- 確認沒有重複 id、沒有失效的相對連結或 `#錨點`。
- 搜尋 `http://` 與 `https://`:只應出現在 `docs.github.com` 連結與 SVG `xmlns`。
- 確認教學頁沒有 `localStorage`(只有 `index.html` 可以有)。
- 用瀏覽器實際點過:複製按鈕、測驗、檢查表、模擬、(有的話)視角切換與階段切換。

## 9. 後續擴充指南

### A. 更新 GitHub 主題

- GitHub 改了介面名稱或路徑:修改對應 `pN.py` 的步驟文字與官方連結,重新 `build.py pN`,更新頁尾查證日期。
- 要補的內容(優先順序建議):
  1. 複查第 7 節標示「未對照」的篇章。
  2. 第 7 篇補上各條 Ruleset 規則的確切名稱(對照「Available rules for rulesets」文件)。
  3. 第 11 篇補上 Pages 私人 repo 與網址格式的官方說明。
  4. 首頁快速入口加上 `#錨點`,直接跳到子頁的對應章節(目前只連到頁面頂端)。
  5. 加入子頁的「已讀」回寫(目前是首頁手動勾選;子頁互不依賴,若要做需注意子頁不得使用 `localStorage`,或改成回首頁勾選)。
- 想新增 GitHub 主題的篇章(候選):`git stash` 與 `rebase`、fork 與 upstream 同步、GitHub CLI(`gh`)、Discussions、倉庫權限與協作者管理、monorepo 與 submodule。新增時在 `SITE` 選擇階段,或新增階段。

### B. 新增其他主題(例如 Docker、Linux 指令)

1. 在 `public/` 底下新增資料夾,例如 `docker/`。
2. 檔名用 `docker-<子題>-guide.html`;新增 `_build` 的 `pN.py`,並把 `build.py` 輸出目錄改成可依 `SPEC` 指定(目前寫死輸出到 `public/github/`;建議在 `SPEC` 加 `dir` 欄位)。
3. 在 `index.html` 的 `SITE` 新增一個分類(`id`、`label`、`stages`、`quick`)。標籤頁、卡片、篩選、進度、網址 hash 會自動出現,**不需要改首頁的任何程式碼**。
4. 每個主題頁的 eyebrow 要改成該主題名稱(目前模板固定寫「GitHub 入門 · …」,見 `build.py`)。
5. 首頁文案與路徑圖目前偏 GitHub 風格,新主題上線時重新檢視 hero 與頁尾的措辭。
6. 沿用 `DESIGN.md` 的骨架,在 `DESIGN.md` 新增該主題的站台結構與各篇大綱。

### C. 要請 Claude 接手時,可以這樣交代

> 請先讀 `HANDOFF.md` 與 `DESIGN.md`,再讀 `github/github-pr-guide.html`(樣板)與 `_build/` 的 `build.py`、`h.py`、`p3.py`。我要新增 `<主題>`,每頁分別用 `/html-effective` 製作並依循既有設計。動手前先用 `/grill-me` 和我確認範圍與大綱。

## 10. 已知限制

- 教學頁沒有搜尋功能,也沒有子頁之間的進度同步。
- 版面針對 1280 與 390 寬驗證過,中間寬度(平板)沒有逐頁檢查。
- 所有 SVG 全貌圖是手寫座標,改文字長度時要自己確認不會超出方塊。
- 目前未做無障礙的完整稽核(有 `:focus-visible`、`aria-label`、可鍵盤操作的主要功能,但沒有用螢幕閱讀器測過)。
- 沒有自動化 CI 測試;`verify.py` 需要手動執行。
