# 交接:GitHub 教學站(新對話請先讀這份)

> 本文件只記錄「這個對話裡的決定、使用者偏好與待辦」。專案本身的細節不在此重複,請讀:
> - `HANDOFF.md`:現況、檔案地圖、`_build/` 工具用法、踩過的坑、查證狀態、擴充指南
> - `DESIGN.md`:設計 tokens、共同元件、導覽規範、11 篇大綱、首頁規格
> - `README.md`:給 repo 讀者看的說明
> - `github/github-pr-guide.html`:視覺與結構的原始樣板(使用者提供,手寫)

## 1. 這個對話做了什麼

使用者要一個完整的 GitHub 繁體中文教學站:`index.html`(首頁)加多個子頁,每頁分別用 `/html-effective` 製作,並沿用已完成的 `github-pr-guide.html` 的設計。流程是先用 `/grill-me` 逐輪確認需求,再實作。

結果:`index.html` + `github/` 內 11 篇 + `DESIGN.md` + `README.md` + `HANDOFF.md` 全部完成,並用 Playwright 在 1280 與 390 寬驗證過(無橫向溢出、無 JS 錯誤、連結與錨點正常、無重複 id)。分四批交付,最後一批為 `github-tutorial-final.zip`。

## 2. 使用者已確認的決定(grill-me 結果)

| 項目 | 決定 |
|---|---|
| 讀者起點 | 往前補到「完全沒碰過 git」,往後延伸到進階協作 |
| 主題 | 11 篇、五階段;加入 `.gitignore`、Release 與版本號、安全性(Secrets、Dependabot);小主題已合併(分支與衝突併成一篇,Actions 與 Pages 併成一篇) |
| 進階選讀 | 第 7、10、11 篇 |
| 資料夾 | 子頁統一放 `github/`;未來每個主題一個獨立資料夾 |
| 檔名 | `github-<主題>-guide.html`(保留主題前綴) |
| 首頁 | 資料驅動(`SITE`);多主題標籤頁;現在顯示「GitHub」與一個不可點的「更多主題」;選中標籤同步網址 hash |
| 首頁功能 | 學習路徑、8 條快速入口、篩選、手動勾選已讀進度、TOC、閱讀進度條 |
| 已讀進度 | 只在首頁、手動勾選;`localStorage` 且包 try/catch。子頁不回寫 |
| 樣式共用方式 | 每頁內嵌 CSS,tokens 與元件命名一致,不抽共用 `style.css` |
| 語言 | 繁體中文;按鈕與選單名稱保留 GitHub 英文原文 |
| 導覽 | 每頁頁首「← 回教學首頁」、頁尾「上一篇 / 下一篇」(PR 頁已補上) |
| 雙視角 | 只用在第 5、6、7 篇;其餘單視角分步驟 |
| 製作方式 | 因為在 claude 網頁版沒有子代理,改成在同一對話依序製作,並用自製的 Python 組頁工具(`_build/`) |
| 時效性查證 | 第 7、9、10、11 篇已對照官方文件,查證日期 2026-11-06 |
| 交付 | zip |

## 3. 使用者的環境與偏好

- 語言:繁體中文;時區 Asia/Taipei。
- 部署:repo 在 GitHub,用 GitHub Actions 把 `public/` 推送到 Cloudflare Workers static assets。`deploy.yml` 由使用者自己維護,**不要碰,也不要主動提供協助**(使用者明確說「你不用協助」)。使用者特別說明:自動推上 Cloudflare 的只有 `public/` 底下的東西。
- 使用者是在 claude 網頁版工作,沒有子代理可用;做到一定頁數後會想用 `/handoff` 交接到新對話。
- 使用者偏好:先用 grill-me 式的多輪提問確認範圍,再動手;回覆簡潔,結果導向。

## 4. 目前尚未完成或未驗證的事

1. 第 1、2、3、4、5、8 篇主要依既有知識撰寫,**未逐頁對照官方文件**;第 4 篇的 Developer settings 與 SSH and GPG keys 路徑、第 5 篇的 Projects 介面與 Close as not planned,最值得先複查。
2. 所有頁面的官方文件連結**沒有逐一打開驗證**。
3. 第 11 篇的「Pages 私人 repo 可用性」與「專案網站網址格式」未由官方頁面確認。
4. 第 7 篇各條 Ruleset 規則的確切名稱官方頁面沒列,頁面上寫「以畫面為準」。
5. 首頁快速入口只連到子頁頂端,尚未加 `#錨點`。
6. `README.md` 的「授權」一節留了待補;網站上線網址也沒填。
7. **repo 結構已確定**:只有 `public/` 會被推送到 Cloudflare,所以 `index.html` 與 `github/` 都在 `public/` 底下;文件與 `_build/` 在 repo 根目錄、不部署。壓縮檔的結構就是 repo 根目錄的樣子。
8. `_build/` 的路徑已改成相對於自身位置(假設 `_build/` 與 `public/` 同在根目錄);Chrome 路徑可用環境變數 `CHROME_PATH` 覆寫。`build.py` 輸出目錄(`public/github/`)與 eyebrow 文字(「GitHub 入門 · …」)仍寫死為 GitHub 主題,新增其他主題前需要先改成可由 `SPEC` 指定(建議加 `dir` 與主題名稱欄位)。

## 5. 下一個對話可能的重點

依 `HANDOFF.md` 第 9 節:(A)更新或補強 GitHub 主題、(B)新增其他主題。若使用者沒有指定,先問是哪一種,再用 `/grill-me` 確認主題清單、階段、大綱與互動元件配置。

## 6. 建議使用的技能

| 技能 | 何時用 |
|---|---|
| `grill-me` / `grilling` | 新增主題或大改版前,先逐輪確認範圍與大綱 |
| `html-effective` | 製作每一頁(使用者要求每頁分別使用) |
| `frontend-design` | 首頁或視覺有大改動時參考 |
| `handoff` | 這個對話再做到一定量,又要交接時 |

## 7. 新對話的開場步驟

1. 解壓縮後依序讀:本文件 → `HANDOFF.md` → `DESIGN.md` → `github/github-pr-guide.html`。
2. 讀 `_build/build.py`、`_build/h.py`、`_build/p3.py`,理解組頁方式。
3. 在 repo 根目錄執行 `python3 _build/verify.py` 確認工具可用(需要 `pip install playwright` 與 Chrome;路徑不同時設 `CHROME_PATH`)。
4. 再開始使用者指定的新工作;不要動 `deploy.yml`。

## 8. 檔案清單(壓縮檔內容)

```text
00-SESSION-HANDOFF.md      本文件(不屬於網站,可不放進 repo)
README.md
DESIGN.md
HANDOFF.md
_build/                    組頁與驗證工具(common.js、h.py、build.py、p1–p5、p7–p11、verify.py)
public/                    ← 唯一會被部署的資料夾
  index.html
  github/                  11 篇教學頁
```

沒有敏感資訊(範例資料皆為 `your-name`、`hello-world`、`you@example.com` 等假值)。
