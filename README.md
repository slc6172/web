# C 語言泡泡排序法｜Cloudflare Workers Static Assets

這是一個無框架、無建置步驟的繁體中文單頁教學網站。部署目標是 **Cloudflare Workers Static Assets**，不是 Cloudflare Pages。

## 專案結構

```text
.
├── .github/
│   └── workflows/
│       └── deploy.yml       # 推送至 main 後自動部署
├── public/
│   └── index.html           # 網站本體（HTML、CSS、JavaScript）
├── wrangler.jsonc           # Workers Static Assets 設定
├── .gitignore
└── README.md
```

## 放進 GitHub

1. 在 GitHub 建立一個新的 repository（例如 `c-bubble-sort-tutorial`）。
2. 將本專案內的所有檔案與資料夾放到 repository 根目錄；不要只上傳 `public` 資料夾。
3. 確認預設分支名稱為 `main`。

## 設定 Cloudflare

1. 登入 Cloudflare Dashboard，進入 **Workers & Pages → Overview**，確認使用的是 Workers。
2. 在 Cloudflare 建立一個 API Token，權限採用 **Edit Cloudflare Workers**，並限定在要部署的 Cloudflare 帳戶。
3. 到 GitHub repository 的 **Settings → Secrets and variables → Actions**，新增以下 Repository secrets：
   - `CLOUDFLARE_API_TOKEN`：剛建立的 API Token。
   - `CLOUDFLARE_ACCOUNT_ID`：Cloudflare 帳戶 ID。
4. 將檔案推送至 `main` 分支，或在 GitHub 的 **Actions** 頁籤手動執行 **Deploy to Cloudflare Workers Static Assets**。
5. 工作流程成功後，至 Cloudflare Workers 檢視部署結果與 `workers.dev` 網址。

**安全提醒：** 不要把 API Token 寫進程式碼、`wrangler.jsonc` 或提交到 Git。請只存放在 GitHub Secrets。

## 操作介面配置

在桌面版畫面中，互動動畫（01）與完整 C 程式碼（03）會並排呈現；按「下一步」或自動播放時，完整程式碼中的黃綠色標記會同步移動。向下閱讀左側操作紀錄時，程式碼面板會暫時固定在畫面上方，方便對照。窄螢幕（手機／小平板）會改成上下排列，以維持可讀性。

## 本機預覽（選用）

若本機已安裝 Node.js，可在專案根目錄執行：

```bash
npx wrangler dev
```

首次使用時，Wrangler 可能會提示安裝套件。部署時 GitHub Actions 會呼叫 `wrangler deploy`，並依 `wrangler.jsonc` 將 `public/` 中的靜態檔案發布至 Workers Static Assets。

## 修改網站

編輯 `public/index.html` 後，提交並推送到 `main`，GitHub Actions 就會再次部署。網站使用原生 HTML、CSS 與 JavaScript，沒有 npm build 步驟，也不需要 Pages 專案。
