# GitHub 新手教學站

從第一次 `push` 到團隊協作的 GitHub 繁體中文教學。共 11 篇獨立的單頁教學,每一步都說明為什麼要做、要打什麼、會看到什麼,並附情境演練、測驗與檢查表。

完全沒碰過 git 的人從第 1 篇開始;已經會 `add / commit / push / clone` 的人可以直接跳到需要的那一篇。

## 內容

| 階段 | 篇章 |
|---|---|
| 一、入門 | 1. GitHub 是什麼與第一次推送<br>2. `.gitignore` 與檢視歷史 |
| 二、分支與同步 | 3. 分支、合併與衝突解決<br>4. 遠端與同步(含 SSH / HTTPS 驗證) |
| 三、協作 | 5. Issue 與 Projects<br>6. Pull Request<br>7. Code Review 與團隊規範(進階選讀) |
| 四、版本與救援 | 8. 還原與救援<br>9. Release 與版本號 |
| 五、安全與自動化 | 10. 安全性:Secrets 與 Dependabot(進階選讀)<br>11. GitHub Actions 與 Pages(進階選讀) |

首頁另有「我只想解決某個問題」快速入口(push 被拒絕、合併衝突、commit 錯了、密碼不小心 commit 等),以及可手動勾選的已讀進度。

## 專案結構

```text
public/
├── index.html                      教學首頁(多主題標籤頁,資料驅動)
└── github/
    ├── github-start-guide.html     1  GitHub 是什麼與第一次推送
    ├── github-gitignore-guide.html 2  .gitignore 與檢視歷史
    ├── github-branch-guide.html    3  分支、合併與衝突解決
    ├── github-remote-guide.html    4  遠端與同步
    ├── github-issues-guide.html    5  Issue 與 Projects
    ├── github-pr-guide.html        6  Pull Request
    ├── github-review-guide.html    7  Code Review 與團隊規範
    ├── github-undo-guide.html      8  還原與救援
    ├── github-release-guide.html   9  Release 與版本號
    ├── github-security-guide.html  10 安全性
    └── github-actions-guide.html   11 GitHub Actions 與 Pages
DESIGN.md                           設計規範與各篇內容大綱
```

> 只有 `public/` 會被部署;`DESIGN.md`、`HANDOFF.md`、`_build/`(製作工具)放在 repo 根目錄,不會上線。`public/` 內的 `index.html` 與 `github/` 必須在同一層,首頁與各篇之間才能互相連結。

## 本機預覽

全部是單檔、零依賴的靜態 HTML,不需要建置,也不需要安裝套件。

直接用瀏覽器開啟 `public/index.html` 即可。若想用本機伺服器預覽:

```bash
cd public
python3 -m http.server 8000
# 瀏覽器開啟 http://localhost:8000
```

## 部署

`public/` 資料夾的內容會透過 GitHub Actions(`.github/workflows/deploy.yml`)發佈到 Cloudflare Workers 的靜態資源(static assets)。部署流程與所需的 repository secrets,請參考該 workflow 檔案。

## 新增教學頁或新主題

網站設計為資料驅動,首頁的標籤頁、卡片、篩選與進度都由 `public/index.html` 內的 `SITE` 物件產生。

- **新增一篇教學**:在對應的資料夾新增 HTML 檔,並在 `SITE` 該分類的階段裡加一筆資料(標題、路徑、摘要、難度、預估時間、`status: "done"`)。
- **新增一個主題**(例如另一種工具的教學):在 `public/` 底下新增資料夾,在 `SITE` 新增一個分類,首頁會自動多出一個標籤頁。目前網址 hash(如 `#github`)會記住所選的標籤。
- 每一頁的版面、色彩 tokens、元件與導覽規範,請見 [`DESIGN.md`](DESIGN.md),新頁面請照著做,才能維持一致的風格。

## 設計原則

- **單檔、零依賴**:每頁的 CSS 與 JavaScript 都內嵌,不使用框架、CDN、網路字型或外部圖片,可離線開啟、單獨分享。
- **統一的視覺語言**:象牙白底、陶土橘強調色,serif 標題、sans 內文、mono 指令與標籤。
- **每步都有解釋**:每個步驟都說明為什麼、要打什麼、會看到什麼。
- **可動手練習**:每篇都有測驗、檢查表與情境模擬;依主題加上「填入資料自動換指令」等互動。
- **不依賴瀏覽器儲存**:教學頁本身不使用 `localStorage`;只有首頁的「已讀進度」會使用,若瀏覽器不允許儲存,頁面仍可正常使用。

## 內容說明

- 按鈕與選單名稱以 GitHub 英文介面為準。GitHub 偶爾會調整介面文字與位置,找不到時請用關鍵字對照畫面上相近的按鈕。
- 內容查證日期:2026-11-06。費用、免費額度、方案限制等資訊可能變動,請以 GitHub 官方文件與帳號的 Billing 頁為準。
- 每篇文末附有對應的 [GitHub 官方文件](https://docs.github.com) 連結。

## 授權

請在此補上你選擇的授權條款(例如 MIT)。


## Arduino 主題

`public/arduino/` 放 Arduino 入門主題的頁面(規劃 20 篇)。設計決定與大綱見 `ARDUINO-DESIGN.md`,目前進度與接手步驟見 `ARDUINO-PROGRESS.md`。頁面由 `_build/aNN.py` 產生;接線圖、原理圖由 `_build/bb.py` 從同一份資料產生,並有自動驗證(`arduino_verify.py`、`verify_arduino.py`)。
