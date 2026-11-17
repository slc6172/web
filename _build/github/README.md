# GitHub 主題（`public/github/`，11 篇）

先讀上一層的 [`../README.md`](../README.md)（總入口、設計規範、指令）。本文件只記 GitHub 主題特有的事。

## 已確認的決定

- 讀者：從完全沒碰過 git 到進階協作；11 篇、五階段；進階選讀是第 7、10、11 篇。
- 檔名 `github-<子題>-guide.html`；語言繁體中文，按鈕與選單名稱保留 GitHub 英文原文。
- 雙視角（提出者／維護者、作者／審查者）只用在第 5、6、7 篇，其餘單視角分步驟。
- 範例一律用假資料（`hello-world`、`your-name`），不放真實帳號或金鑰；每個指令都附「你會看到」。
- 連結只指向 `docs.github.com`；頁尾固定寫「按鈕名稱以 GitHub 英文介面為準」與查證日期。

## 規格檔

| 檔案 | 頁面 | 備註 |
|---|---|---|
| `p1.py` … `p5.py`、`p7.py` … `p11.py` | 第 1–5、7–11 篇 | 第 6 篇 PR 頁沒有規格檔：它是手寫的原始樣板，也是共用 CSS 的來源 |

範本：單視角看 `p3.py`；雙視角看 `p5.py` / `p7.py`；有「我現在的狀況是…」決策選擇器看 `p8.py`。

## 模板語法

- `.cmd pre` 與帶 `data-tpl` 的元素會把 `{key}` 換成使用者填入的值；可用的 key 由該頁 `config.fill` 決定，沒定義的 `{xxx}` 原樣保留。含 `{{ … }}` 的程式碼（GitHub Actions 語法）不受影響。
- 測驗題的 `q` 欄位用 `innerHTML`（可放 `<code>`）；選項 `a` 是純文字，**不要放 HTML**。

## 踩過的坑

1. **重複的 id**：區塊 `id="stages"` 曾與階段切換的 `id="stages"` 撞名，整段被覆寫。區塊 id 請用 `states` 等不同名字；新增頁面後用 `verify.py` 檢查。
2. **TL;DR 內文強調用 `<strong>`**，不要用 `<b>`。
3. 每個指令都要真的能跑，不要放真實帳號或金鑰。

## 內容查證狀態（更新時優先複查）

GitHub 介面變動快。查證日期 2026-11-06。

| 篇 | 狀態 |
|---|---|
| 7 Code Review | Ruleset 路徑（Settings → Rules → Rulesets → New ruleset → New branch ruleset）與 CODEOWNERS 三個放置位置已對照官方文件；各條規則的確切名稱官方頁面未列出，頁面上寫「以畫面為準」 |
| 9 Release | 按鈕名稱（Draft a new release、Generate release notes、Set as a pre-release、Publish release、Save draft）已對照官方文件 |
| 10 安全性 | push protection 預設行為、Dependabot alerts 設定路徑、`dependabot.yml` 範例、`git filter-repo` 建議與風險、Actions secrets 路徑已對照官方文件 |
| 11 Actions 與 Pages | workflow 範例、Actions 分頁操作、Pages Source 選項、免費額度已對照官方文件；**Pages 在私人 repo 的可用性**與**專案網站網址格式**未由官方頁面確認 |
| 1、2、3、4、5、8 | 主要依既有知識撰寫，**未逐頁對照官方文件**。優先複查：第 4 篇的 Developer settings、SSH and GPG keys 路徑；第 5 篇的 Projects 介面與 Close as not planned 選項 |
| 全部 | 頁尾的官方文件連結未逐一打開驗證 |

更新內容後請同步更新各頁頁尾與首頁 `github.foot` 的查證日期。

## 後續擴充

- 優先順序：複查上表標示「未對照」的篇章 → 第 7 篇補 Ruleset 規則確切名稱 → 第 11 篇補 Pages 私人 repo 與網址格式 → 首頁快速入口加 `#錨點` 直接跳到子頁章節。
- 候選新篇章：`git stash` 與 `rebase`、fork 與 upstream 同步、GitHub CLI（`gh`）、Discussions、倉庫權限與協作者管理、monorepo 與 submodule。新增時在 `SITE.github` 選擇階段或新增階段。

## 已知限制

教學頁沒有搜尋功能，也沒有子頁之間的進度同步；版面只驗證過 1280 與 390 寬；SVG 全貌圖是手寫座標，改文字長度時要自己確認不超出方塊；未做完整的無障礙稽核。
