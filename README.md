# 自學教學站（Learning Hub）

繁體中文的單頁教學站。每一篇都是獨立、零依賴的單檔 HTML，附演練、測驗與檢查表；首頁用標籤頁整理各主題，可篩選、可勾選已讀進度。

- 上線網址：<https://www.slc6172.workers.dev/>
- 原始碼：<https://github.com/slc6172/CloudflareSupabaseBBS>

| 主題 | 資料夾 | 篇數 | 內容 |
|---|---|---|---|
| GitHub | `public/github/` | 11 | 從第一次 `push` 到團隊協作：分支、PR、還原、Release、安全性、Actions |
| Arduino | `public/arduino/` | 20 | 以 Arduino Uno 從接第一條線到綜合專案，附接線圖、原理圖與程式碼 |
| 微電影分鏡 | `public/microfilm/` | 16 | 給沒拍過影片的人：分鏡圖、景別、角度、運鏡、連戲，到把劇本畫成分鏡 |

## 專案結構

```text
public/                  ← 唯一會被部署的資料夾
├── index.html           首頁（多主題標籤頁，資料都在檔內的 SITE 物件）
├── robots.txt           由 _build/site_files.py 產生
├── sitemap.xml          由 _build/site_files.py 產生（列出所有頁面）
├── _headers             Cloudflare 靜態資源的回應標頭
├── github/              github-<子題>-guide.html
├── arduino/             arduino-<子題>-guide.html
└── microfilm/           microfilm-<子題>-guide.html
_build/                  製作工具與維護指南（不會上線），入口見 _build/README.md
README.md                本文件
```

> 只有 `public/` 會被 GitHub Actions 推送到 Cloudflare Workers static assets。`index.html` 與各主題資料夾必須在同一層，頁面之間才能用相對路徑互相連結。

## 本機預覽

全部是靜態 HTML，不需要建置，也不需要安裝套件。直接用瀏覽器開啟 `public/index.html`，或：

```bash
cd public
python3 -m http.server 8000
# 瀏覽器開啟 http://localhost:8000
```

## 部署

`public/` 的內容由 GitHub Actions 發佈到 Cloudflare Workers 的靜態資源。流程與所需的 secrets 請看 `.github/workflows/` 內的 workflow 檔。

## 設計原則

- **單檔、零依賴**：每頁的 CSS 與 JavaScript 都內嵌，不使用框架、CDN、網路字型或外部圖片，可離線開啟、單獨分享。
- **統一的視覺語言**：象牙白底、陶土橘強調色；serif 標題、sans 內文、mono 指令與標籤。三個主題共用同一組設計 tokens 與元件。
- **每步都有解釋**：說明為什麼要做、要打什麼、會看到什麼，並附測驗與檢查表。
- **可搜尋、可分享、可用鍵盤**：每頁都有 description、canonical、Open Graph、favicon 與 theme-color；每頁開頭有「跳到主要內容」連結；首頁快速入口直接連到頁內對應段落。
- **不依賴瀏覽器儲存**：教學頁本身不使用 `localStorage`（微電影第 15 篇的分鏡編輯器除外）；首頁的「已讀進度」會使用，若瀏覽器不允許儲存，頁面仍可正常使用。

## 維護與擴充

頁面是用 Python 組出來的（`_build/`），不是手寫 HTML。要修改頁面、新增篇章或新增主題，請先讀 [`_build/README.md`](_build/README.md)：裡面有資料夾地圖、常用指令、設計規範、首頁資料格式與驗證清單，並附有「交給新對話的開場白」。

## 內容說明

- GitHub 主題的按鈕與選單名稱以 GitHub 英文介面為準；Arduino 主題以 Arduino IDE 2.x（Windows）與 Uno R3 為準。介面與規格偶爾會變，找不到時請用關鍵字對照畫面上相近的項目。
- 各主題的查證日期寫在每頁頁尾：GitHub 2026-11-06、Arduino 2026-11-07、微電影 2026-11-10。費用、免費額度與零件規格可能變動，請以官方文件與你手上的零件為準。

## 授權

[MIT License](LICENSE)。
