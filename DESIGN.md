# GitHub 教學站 · 設計規範與內容大綱

> 本文件是整個教學站的「單一依據」。每一頁都用 `/html-effective` 製作,並以 `github/github-pr-guide.html`(已完成)為樣板。
> 查證日期:2026-11-06。介面名稱以 GitHub 英文介面為準。

## 0. 站台結構

只有 `public/` 會被 GitHub Actions 推送到 Cloudflare Workers static assets,所以網站檔案都放在 `public/` 底下;文件與製作工具放在 repo 根目錄,不會被部署。

```
public/                         ← 會被部署的網站根目錄
  index.html                    首頁(多主題標籤頁,資料驅動)
  github/
    github-start-guide.html       1  GitHub 是什麼與第一次推送
    github-gitignore-guide.html   2  .gitignore 與檢視歷史
    github-branch-guide.html      3  分支、合併與衝突解決
    github-remote-guide.html      4  遠端與同步(含 SSH / HTTPS 驗證)
    github-issues-guide.html      5  Issue 與 Projects            [雙視角]
    github-pr-guide.html          6  Pull Request                 [雙視角,已完成]
    github-review-guide.html      7  Code Review 與團隊規範       [雙視角,進階選讀]
    github-undo-guide.html        8  還原與救援
    github-release-guide.html     9  Release 與版本號
    github-security-guide.html    10 安全性:Secrets 與 Dependabot [進階選讀]
    github-actions-guide.html     11 GitHub Actions 與 Pages       [進階選讀]
DESIGN.md / README.md / HANDOFF.md / _build/   (根目錄,不部署)
```

未來新增主題:在 `public/` 新增資料夾(如 `docker/`),檔名沿用 `<主題>-<子題>-guide.html`,並在 `index.html` 的 `SITE` 資料中新增一個分類。

## 1. 硬規則(沿用 html-effective)

- 單檔、零依賴:CSS 在 `<style>`、JS 在 `<script>`,不用 CDN、網路字型、外部圖片;不發網路請求。
- 原生 JS,IIFE 包起來;狀態用變數,以 `render()` 重畫。
- 一律 `<!doctype html>` + `lang="zh-Hant"` + charset + viewport;`<title>` 要具體。
- 全頁只用 `:root` 變數取色(SVG 屬性可寫字面色碼,但必須取自同一組 token)。
- 例外(使用者指定):`index.html` 的「已讀進度」使用 `localStorage`,**一律包 try/catch**,讀寫失敗時退回記憶體變數,頁面不得因此壞掉。子頁不使用 `localStorage`。

## 2. 設計 Tokens(逐字複製到每頁 `:root`)

```css
:root {
  --ivory:#FAF9F5; --white:#FFFFFF; --slate:#141413;
  --clay:#D97757; --clay-d:#B85C3E; --oat:#E3DACC; --olive:#788C5D; --rust:#B04A3F;
  --gray-100:#F0EEE6; --gray-300:#D1CFC5; --gray-500:#87867F; --gray-700:#3D3D3A;
  --serif: ui-serif, Georgia, "Times New Roman", "Noto Serif TC", "Songti TC", "PMingLiU", serif;
  --sans:  system-ui, -apple-system, "Segoe UI", Roboto, "PingFang TC", "Noto Sans TC", "Microsoft JhengHei", Helvetica, Arial, sans-serif;
  --mono:  ui-monospace, "SF Mono", Menlo, Monaco, Consolas, monospace;
  --border: 1.5px solid var(--gray-300);
}
```

語意色:clay = 焦點/注意/選中;olive = 成功/完成/新增;rust = 危險/失敗/刪除;oat = 中性強調;slate = 墨色與深色底。

字型分工:h1/h2/h3 與大數字用 serif weight 500;內文 sans 15px / 行高 1.65;eyebrow、標籤、chip、程式碼用 mono。
圓角:面板 12、內層 8–10、膠囊 999。邊框 1.5px,不用漸層,不用陰影(除浮起狀態)。
容器:`.page` 最大寬 1100px;`.layout` 為 `190px + 內容` 兩欄,≤920px 折成單欄。斷點:920、720。

## 3. 共同元件(class 名稱固定,照 `github-pr-guide.html` 複製 CSS)

| 元件 | class | 用途 |
|---|---|---|
| 頁首 | `.eyebrow` `h1` `.sub` `.tldr` | eyebrow 格式:`GitHub 入門 · <主題>` |
| 目錄 | `nav.toc`(sticky,含 scroll-spy) | 左欄 8 項以內 |
| 閱讀進度條 | `.progress > span#readBar` | 固定頂端 3px clay |
| 區塊 | `main > section` + `h2` + `hr.rule` | 每節一個 id |
| 面板 | `.panel` | 白底、邊框、圓角 12 |
| 名詞表 / 對照表 | `.table-wrap > .gt.g2 / .g3 / .g3b` | 寬表可橫向捲動 |
| 指令區 | `.cmd > pre[data-tpl] + button.copy` | 深色底,`{me}` 等佔位符會被「填入資料」替換 |
| 步驟 | `.steps > .step`(`.num` + `h3` + `.why` + `.ops` + 提示框) | 每步:為什麼、要打什麼、會看到什麼 |
| 提示框 | `.see`(olive)`.warn`(rust)`.tip`(clay) | 「你會看到」「注意/檢查」「小技巧」 |
| 全貌圖 | `.canvas > svg` + `ol.legend` | 內嵌 SVG,編號圓點對應圖例 |
| 折疊 | `details > summary + .body` | 常見卡關 |
| 階段切換 | `.stages` + `.two` | 兩欄對照 |
| 情境模擬 | `.panel.sim` + `.sim-buttons` + `.sim-result` | 選做法看結果 |
| 測驗 | `#quiz`(3–6 題,答後出解釋) | 每頁都有 |
| 檢查表 | `.checks` + `.bar` | 每頁都有 |
| 角色標籤 | `.role.c` / `.role.o` | 雙視角頁使用 |
| 資源連結 | `.resources > a.resource` | 只連 docs.github.com 官方文件 |

填入資料區(`.fill`):各頁自選需要的欄位,沿用 `data-k` 與 `{key}` 佔位符機制,空白時顯示範例值,橘底 `.slot` 標示可替換處。

## 4. 固定導覽(每頁必備,含 PR 頁)

頁首最上方(`header` 內、`.eyebrow` 之前):

```html
<nav class="crumb" aria-label="站內導覽"><a href="../index.html">← 回教學首頁</a></nav>
```

頁尾(`</main>` 之後、`.foot` 之後):

```html
<nav class="pager" aria-label="上一篇與下一篇">
  <a class="prev" href="github-XXX-guide.html"><small>上一篇</small><b>標題</b></a>
  <a class="next" href="github-YYY-guide.html"><small>下一篇</small><b>標題</b></a>
</nav>
```

第 1 頁沒有上一篇、第 11 頁沒有下一篇(省略該側,不放空連結)。
`.crumb` 與 `.pager` 的 CSS 固定如下:

```css
.crumb { margin:0 0 18px; font:12px var(--mono); }
.crumb a { color:var(--gray-500); text-decoration:none; }
.crumb a:hover { color:var(--clay); }
.pager { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:14px; margin-top:40px; }
.pager a { display:block; padding:14px 18px; border:var(--border); border-radius:12px; background:#fff; color:var(--slate); text-decoration:none; }
.pager a:hover { border-color:var(--clay); }
.pager small { display:block; font:11px var(--mono); letter-spacing:.08em; text-transform:uppercase; color:var(--gray-500); }
.pager b { font:500 17px/1.4 var(--serif); }
.pager .next { text-align:right; grid-column:2; }
.pager .prev { grid-column:1; }
@media (max-width:720px){ .pager{grid-template-columns:minmax(0,1fr);} .pager .next,.pager .prev{grid-column:1;text-align:left;} }
```

## 5. 每頁骨架

1. 頁首:crumb → eyebrow → h1(標題就是結論)→ `.sub` → `.tldr`
2. `.layout`:左 `nav.toc`,右 `main`
3. 主體順序:概念(比喻 + 名詞表)→ 全貌圖(SVG)→(視主題)填入資料 → 分步驟 → 常見卡關(`details`)→ 演練(情境/測驗/檢查表)→ 官方文件連結
4. 頁尾:`.foot`(「按鈕名稱以 GitHub 英文介面為準;查證日期 2026-11-06」)→ `.pager`

每頁元件分級:
- 必備:複製按鈕、閱讀進度條、TOC 高亮、`details` 常見卡關、測驗、檢查表。
- 視主題:填入資料(1、4、6、9、11)、情境模擬(3、7、8、10)、階段切換(5、6、9)、雙視角(5、6、7)。
- 第 8 頁額外加「我現在的狀況是…」決策選擇器。

篇幅:單視角 500–800 行;測驗 3–6 題;5–8 個步驟或概念區塊。

寫法:標題是結論;每個指令都附「你會看到」;範例用真實可執行的指令與假資料(如 `hello-world`),示意資料不假裝是真實數據;不使用任何網路請求。

## 6. 各頁大綱

### 第 1 頁 · github-start-guide.html · GitHub 是什麼與第一次推送
- 結論標題:「從零到第一次 push:五個指令就夠」
- 概念:Git(本機版本控制)vs GitHub(雲端託管與協作)、repo、commit、remote
- 全貌圖:工作資料夾 → 暫存區 → 本機 repo → GitHub(add / commit / push / clone 四個箭頭)
- 填入資料:帳號、專案名稱、commit 訊息
- 步驟:註冊與安裝 Git → 設定 `user.name` / `user.email` → 在 GitHub 建立 repo → `git init`(或 clone)→ add → commit → 設定 remote 並 push → 在網頁確認
- 卡關:`not a git repository`、push 要求登入、`main` 與 `master` 分支名稱、中文檔名亂碼
- 元件:填入資料、測驗、檢查表

### 第 2 頁 · github-gitignore-guide.html · .gitignore 與檢視歷史
- 結論標題:「先寫 .gitignore,再第一次 commit」
- 概念:追蹤 / 未追蹤 / 被忽略三種狀態;哪些檔案不該進 repo(`node_modules`、`.env`、建置產物、系統暫存檔)
- 全貌圖:檔案三態流程
- 步驟:建立 `.gitignore` → 常見規則寫法(`*.log`、`dir/`、`!keep.txt`)→ 已被追蹤的檔案用 `git rm --cached` → `git status` / `git diff` / `git log --oneline` 看歷史
- 卡關:加了規則卻沒作用、`.env` 已經 commit(指向第 10 頁)
- 元件:情境模擬(這個檔案該不該忽略?)、測驗、檢查表

### 第 3 頁 · github-branch-guide.html · 分支、合併與衝突解決
- 結論標題:「一件事一個分支,衝突只是 git 在問你留誰的」
- 全貌圖:main 與 feature 分支的提交線
- 步驟:`git branch` / `switch -c` → 在分支提交 → `merge`(fast-forward 與 merge commit)→ 製造並看懂衝突標記 → 解決並 commit → 刪除分支
- 卡關:切換分支時有未提交修改、衝突解到一半想放棄(`git merge --abort`)
- 元件:情境模擬(衝突標記該留哪段)、測驗、檢查表

### 第 4 頁 · github-remote-guide.html · 遠端與同步
- 結論標題:「origin 是你的雲端副本,fetch 看、pull 拿、push 送」
- 全貌圖:本機、origin、upstream 與 fetch / pull / push
- 填入資料:帳號、專案名稱
- 步驟:`remote -v` / `add` / `set-url` → fetch 與 pull 的差別 → push 與 `-u` → HTTPS(Personal Access Token)與 SSH 金鑰設定 → 測試連線(`ssh -T git@github.com`)
- 卡關:403 / `rejected (non-fast-forward)` / `Permission denied (publickey)`
- 元件:填入資料、對照表、測驗、檢查表

### 第 5 頁 · github-issues-guide.html · Issue 與 Projects(雙視角:提出者 / 維護者)
- 結論標題:「好的 Issue 讓對方不用追問」
- 全貌圖:Issue → 標籤與指派 → 分支與 PR(`Closes #編號`)→ 關閉
- 提出者:搜尋是否重複、寫標題與重現步驟、使用 issue 範本
- 維護者:分類(labels)、指派(assignees)、里程碑(milestone)、Projects 看板、`Closes #n` 自動關閉
- 元件:雙視角分頁、階段切換、測驗、檢查表

### 第 6 頁 · github-pr-guide.html · Pull Request(已完成,只補導覽)

### 第 7 頁 · github-review-guide.html · Code Review 與團隊規範(雙視角:作者 / 審查者,進階選讀)
- 查證:分支保護規則與 rulesets 的現行畫面名稱後再寫
- 作者:縮小 PR、自我審查、回覆與 resolve
- 審查者:怎麼讀 diff、留言語氣、Approve / Request changes
- 團隊規範:branch protection / rulesets、必要審查人數、`CODEOWNERS`、PR 範本
- 元件:雙視角、情境模擬、測驗、檢查表

### 第 8 頁 · github-undo-guide.html · 還原與救援
- 結論標題:「先判斷狀況,再選指令:多數錯誤都能救」
- 決策選擇器:「我現在的狀況是…」(改錯檔未 add / 已 add 未 commit / 已 commit 未 push / 已 push)→ 輸出建議指令與風險等級
- 步驟:`restore` → `restore --staged` → `commit --amend` → `revert`(公開歷史安全)→ `reset --soft/--mixed/--hard` → `reflog` 救回
- 卡關:`reset --hard` 前先 `git status`、已 push 的歷史不要強推
- 元件:決策選擇器、情境模擬、測驗、檢查表

### 第 9 頁 · github-release-guide.html · Release 與版本號
- 結論標題:「版本號是對使用者的承諾」
- 概念:tag、SemVer(MAJOR.MINOR.PATCH)、Release notes
- 填入資料:版本號、專案名稱
- 步驟:決定版本號 → `git tag -a` → `git push origin <tag>` → 在網頁 Draft a new release → 自動產生 notes → 附加檔案 → 發佈
- 元件:填入資料、階段切換(草稿 → 預發佈 → 正式)、測驗、檢查表

### 第 10 頁 · github-security-guide.html · 安全性:Secrets 與 Dependabot(進階選讀)
- 查證:Secret scanning、push protection、Dependabot alerts / security updates / version updates 現行設定路徑
- 結論標題:「密碼一旦 push 就當作外洩:先撤銷,再清理」
- 步驟:什麼是 secret → 預防(`.gitignore`、環境變數)→ 不小心 commit 了(先到服務端撤銷或更換金鑰,再清理歷史)→ 開啟 Secret scanning 與 push protection → 開啟 Dependabot alerts 與更新 PR → Actions secrets 的使用
- 元件:情境模擬、測驗、檢查表

### 第 11 頁 · github-actions-guide.html · GitHub Actions 與 Pages(進階選讀)
- 查證:Actions 免費額度與 Pages 部署方式後再寫,查不到的標「待確認」
- 填入資料:專案名稱、分支
- 步驟:workflow YAML 結構(`on` / `jobs` / `steps`)→ 第一個 CI(checkout + 跑測試)→ 看 Actions 分頁與日誌 → 用 secrets → 啟用 GitHub Pages(從分支或 Actions 部署)→ 自訂網域概念
- 元件:填入資料、YAML 複製區、測驗、檢查表

## 7. 首頁(index.html)規格

資料驅動:`SITE` 物件 → 分類(tab)→ 階段 → 教學頁。

```js
var SITE = [
  { id:"github", label:"GitHub", stages:[
    { name:"一、入門", pages:[
      { n:1, title:"…", href:"github/github-start-guide.html", summary:"…",
        level:"入門", mins:12, status:"done", elective:false }
    ]}
  ]}
];
```

- 標籤列:現在有「GitHub」與一個不可點的「更多主題」佔位;選中標籤同步到網址 hash(`#github`),載入時讀取。
- 內容:Hero + TL;DR → 學習路徑圖(SVG,五階段)→「我只想解決某個問題」8 條 → 篩選(全部 / 入門 / 協作 / 進階選讀)→ 卡片網格 → 已讀進度(手動勾選,`localStorage` + try/catch 降級)。
- 卡片:狀態徽章(已完成 / 規劃中)、難度、預估分鐘、進階選讀標記。`status:"planned"` 的卡片不可點(`aria-disabled`)。
- 8 條快速入口:push 被拒絕 → 4;合併衝突 → 3;commit 錯了 → 8;密碼 commit 了 → 10;不想讓檔案進 repo → 2;幫別人修錯字 → 6;發佈版本 → 9;自動跑測試或發佈網站 → 11。每條可帶 `#錨點`(子頁完成後補上)。

## 8. 交付前檢查

- 搜尋 `http://`、`https://`:只應出現在 SVG `xmlns` 與 docs.github.com 文件連結(`rel="noopener"`)。
- 子頁沒有 `localStorage`;`index.html` 的 `localStorage` 都在 try/catch 內。
- 所有 `href`(含 `#錨點`)都指向存在的檔案與 id;上一篇/下一篇鏈完整。
- 1280 與 390 寬各驗一次:`document.documentElement.scrollWidth <= clientWidth`。
- 主要互動都真的點過,console 無錯誤。
- 共用 tokens 與 PR 頁逐字一致。

## 9. 製作進度與交接

| 頁 | 狀態 |
|---|---|
| index.html | 已完成;每完成一篇,把 SITE 裡該篇 status 改成 "done" |
| 6 PR | 已搬入 github/ 並補導覽 |
| 1、2 | 已完成(第一批) |
| 3、4、5 | 已完成(第二批) |
| 7、8、9 | 已完成(第三批) |
| 10、11 | 已完成(第四批),全站驗證通過 |

每批完成後使用 `/handoff` 交接。新對話需要:本文件、`github/github-pr-guide.html`(樣板)、已完成頁面清單。


## 10. 製作工具(不在交付 zip 內)

`_build/` 內有 `common.js`(共用互動:填入資料、複製、TOC、模擬、測驗、檢查表、雙視角、階段切換)、`h.py`(HTML 輔助函式)、`build.py`(組頁,CSS 從 `github/github-pr-guide.html` 讀取)、`pN.py`(各頁內容)、`verify.py`(Playwright 驗證)。新增一頁:寫 `pN.py` 的 `SPEC`,執行 `python3 build.py pN`。
