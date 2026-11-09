from h import *

SVG = '''<svg viewBox="0 0 900 250" role="img" aria-label="GitHub Actions:push 事件觸發 workflow,在 runner 上依序執行 checkout、安裝、測試,成功後可部署到 GitHub Pages">
      <defs>
        <marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#87867F"/></marker>
        <marker id="ao" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#788C5D"/></marker>
        <style>.m{font:12px ui-monospace,Menlo,monospace}.s{font:12px system-ui,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif}.nn{font:600 12px ui-monospace,Menlo,monospace}</style>
      </defs>
      <rect width="900" height="250" fill="#FFFFFF"/>
      <rect x="20" y="40" width="150" height="84" rx="10" fill="#F0EEE6" stroke="#3D3D3A" stroke-width="1.5"/>
      <text x="95" y="74" text-anchor="middle" class="m" fill="#141413">on: push</text><text x="95" y="96" text-anchor="middle" class="s" fill="#3D3D3A">事件發生</text>
      <rect x="215" y="40" width="440" height="84" rx="10" fill="#F0EEE6" stroke="#3D3D3A" stroke-width="1.5"/>
      <text x="435" y="62" text-anchor="middle" class="s" fill="#87867F">job:在 GitHub 提供的虛擬機(runner)上跑</text>
      <rect x="230" y="72" width="120" height="40" rx="8" fill="#fff" stroke="#87867F" stroke-width="1"/><text x="290" y="97" text-anchor="middle" class="m" fill="#141413">checkout</text>
      <rect x="365" y="72" width="120" height="40" rx="8" fill="#fff" stroke="#87867F" stroke-width="1"/><text x="425" y="97" text-anchor="middle" class="m" fill="#141413">安裝套件</text>
      <rect x="500" y="72" width="140" height="40" rx="8" fill="#fff" stroke="#87867F" stroke-width="1"/><text x="570" y="97" text-anchor="middle" class="m" fill="#141413">跑測試</text>
      <rect x="700" y="40" width="180" height="84" rx="10" fill="#E3DACC" stroke="#3D3D3A" stroke-width="2"/>
      <text x="790" y="74" text-anchor="middle" class="s" fill="#141413">結果 / 部署</text><text x="790" y="96" text-anchor="middle" class="s" fill="#3D3D3A">綠勾、或 GitHub Pages</text>
      <line x1="173" y1="82" x2="211" y2="82" stroke="#87867F" stroke-width="1.5" marker-end="url(#ag)"/>
      <circle cx="192" cy="62" r="11" fill="#D97757"/><text x="192" y="66.5" text-anchor="middle" class="nn" fill="#fff">1</text>
      <circle cx="435" cy="26" r="0" fill="none"/>
      <circle cx="357" cy="30" r="11" fill="#D97757"/><text x="357" y="34.5" text-anchor="middle" class="nn" fill="#fff">2</text>
      <line x1="658" y1="82" x2="696" y2="82" stroke="#788C5D" stroke-width="2" marker-end="url(#ao)"/>
      <circle cx="677" cy="62" r="11" fill="#788C5D"/><text x="677" y="66.5" text-anchor="middle" class="nn" fill="#fff">3</text>
      <text x="40" y="172" class="s" fill="#3D3D3A">workflow 是放在 repo 裡的一個 YAML 檔:.github/workflows/xxx.yml</text>
    </svg>'''

what = section("what", "把重複的事交給機器",
  '<div class="panel"><h3>用「自動化工廠的流水線」來想</h3>'
  '<p>每次 push 之後,你都想跑一次測試、檢查格式、打包、發佈。這些事每次都一樣,<b>GitHub Actions</b> 就是讓 GitHub 在特定事件(push、開 PR、打 tag)發生時,依你寫的腳本自動幫你做,結果會顯示在 PR 的 Checks 上(第 7 篇看到的綠勾、紅叉就是它)。</p>'
  '<p style="margin-bottom:0"><b>GitHub Pages</b> 則是把 repo 裡的靜態網頁(HTML、CSS、JS)變成一個公開網站,可以直接從分支發佈,也可以用 Actions 建置後發佈。</p></div>',
  '<h3 style="margin-top:26px">七個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["workflow", "一份自動化流程,寫在 <code>.github/workflows/</code> 底下的 <code>.yml</code> 檔。"],
    ["event(<code>on</code>)", "觸發條件,例如 <code>push</code>、<code>pull_request</code>。"],
    ["job", "一組在同一台機器上依序執行的步驟。多個 job 預設同時進行。"],
    ["runner", "跑 job 的機器。<code>ubuntu-latest</code> 是 GitHub 提供的 Linux 虛擬機。"],
    ["step", "job 裡的一個動作:跑一個指令(<code>run</code>)或使用別人寫好的 action(<code>uses</code>)。"],
    ["action", "可重複使用的步驟,例如 <code>actions/checkout</code> 把 repo 下載到 runner。"],
    ["GitHub Pages", "把 repo 的靜態檔案發佈成網站的服務。"],
  ]))

mapsec = section("map", "全貌:事件觸發,runner 依序做事",
  '<p class="sub" style="margin-bottom:16px">一個 workflow 的生命週期:事件 → 一台乾淨的機器依序跑步驟 → 結果顯示在 GitHub 上。</p>',
  canvas(SVG, [
    ("1", "<b>事件</b>:你 push、開 PR,或其他設定的時機。"),
    ("2", "<b>步驟</b>:機器是全新的,所以第一步一定是 checkout,把你的程式碼拿下來。"),
    ("3", "<b>結果</b>:成功是綠勾、失敗是紅叉;也可以接著部署到 Pages。"),
  ]))

fillsec = section("fill", "先填入你的資料,下面的指令會自動換成你的版本",
  fill([("me", "你的 GitHub 帳號", False), ("repo", "專案名稱", False), ("branch", "主要分支", False)]))

WF = """name: CI
on:
  push:
    branches: [ {branch} ]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: 取得程式碼
        uses: actions/checkout@v4
      - name: 顯示檔案
        run: ls -la
      - name: 跑測試
        run: echo "在這裡放你的測試指令,例如 npm test"
"""

S = steps(
  step(1, "建立第一個 workflow 檔",
       "workflow 就是 repo 裡的一個檔案,放在固定位置 GitHub 才找得到。",
       cmd("mkdir -p .github/workflows"),
       ops(["用編輯器新增檔案 <code>.github/workflows/ci.yml</code>。",
            "貼上下面的內容。YAML 對縮排很敏感:<b>用空白,不要用 Tab</b>,每層縮排 2 個空白。"]),
       cmd(WF, cap=".github/workflows/ci.yml"),
       ops(["<code>name</code>:這個 workflow 在 Actions 頁顯示的名字。",
            "<code>on</code>:什麼時候跑。這裡是 push 到 <code data-tpl>{branch}</code>,以及任何 PR。",
            "<code>jobs → test → runs-on</code>:有一個叫 test 的 job,跑在 Ubuntu 上。",
            "<code>steps</code>:依序做的事。<code>uses</code> 是用別人寫好的 action;<code>run</code> 是執行指令。"]),
       tip("<code>actions/checkout@v4</code> 的 <code>@v4</code> 是 action 的版本。官方文件的範例可能使用更新的主版本,新增時以當時文件為準。")),
  step(2, "commit 並 push,觸發第一次執行",
       "workflow 一進到預設分支(或對應的分支),下一次符合事件就會跑。",
       cmd('git add .github/workflows/ci.yml\ngit commit -m "新增 CI workflow"\ngit push'),
       see("push 成功後,不需要任何手動動作。GitHub 會自動開始執行。")),
  step(3, "在 Actions 分頁看結果",
       "每次執行都有完整的日誌。失敗了,就是從這裡找原因。",
       ops(["到 repo 頁面,點上方的 <b>Actions</b> 分頁。",
            "左側列出 workflow 名稱(<b>CI</b>),點進去,再點最新的一次執行。",
            "左側 <b>Jobs</b> 底下點 <b>test</b>,可以展開每一步的日誌。"]),
       see("執行中是黃色圓點,成功是綠色勾勾,失敗是紅色叉叉。每個 step 可以展開看輸出。"),
       warn("紅叉時,點進失敗的那一步看紅色錯誤訊息。九成是縮排錯誤、指令打錯,或測試真的沒過。")),
  step(4, "讓 PR 也會自動檢查",
       "上面的 <code>on</code> 已經包含 <code>pull_request</code>,所以每個 PR 都會自動跑。",
       ops(["開一個 PR(見第 6 篇)。",
            "PR 頁面下方的合併區塊會出現 <b>Checks</b>:顯示 CI 是通過或失敗。",
            "搭配第 7 篇的規則集,可以設定「CI 通過才能合併」。"]),
       see("合併區塊列出 <b>CI / test</b>,通過時是綠勾。")),
  step(5, "用 secrets 保存金鑰",
       "測試或部署需要金鑰時,放在 Actions secrets,不要寫進 workflow 檔(見第 10 篇)。",
       ops(["repo 的 <b>Settings</b> → 側邊欄 <b>Secrets and variables</b> → <b>Actions</b>。",
            "<b>Secrets</b> 分頁按 <b>New repository secret</b>,填名稱與值,按 <b>Add secret</b>。",
            "在 workflow 的 step 裡用環境變數傳入。"]),
       cmd("      - name: 使用 secret\n        env:\n          API_KEY: ${{ secrets.API_KEY }}\n        run: ./deploy.sh"),
       see("日誌裡 secret 的值會被遮成 <code>***</code>。"),
       warn("來自 fork 的 PR 預設拿不到 secrets,這是為了安全,不是壞掉。")),
  step(6, "啟用 GitHub Pages(從分支發佈)",
       "最簡單的發佈方式:把網頁檔案放在某個分支,讓 Pages 直接發佈。",
       ops(["確認 repo 根目錄(或 <code>/docs</code> 資料夾)有 <code>index.html</code>,並已 push。",
            "repo 的 <b>Settings</b> → 側邊欄 <b>Code, planning, and automation</b> 區塊的 <b>Pages</b>。",
            "<b>Build and deployment</b> → <b>Source</b> 選 <b>Deploy from a branch</b>。",
            "<b>Branch</b> 選 <code data-tpl>{branch}</code>,資料夾選 <b>/ (root)</b> 或 <b>/docs</b>,按 <b>Save</b>。"]),
       see("稍等一兩分鐘,Pages 設定頁上方會出現 <b>Your site is live at …</b> 與網址。專案網站網址通常是 <code data-tpl>https://{me}.github.io/{repo}/</code>。"),
       warn("Pages 能不能用在私人 repo,依你的方案而定;公開 repo 一般可以直接使用。找不到選項時,以官方文件與你帳號實際的畫面為準。")),
  step(7, "(進階)用 Actions 建置後發佈 Pages",
       "網站需要先建置(例如用工具把 Markdown 轉成 HTML)時,改成讓 Actions 建置並部署。",
       ops(["Pages 設定頁 <b>Source</b> 選 <b>GitHub Actions</b>。",
            "GitHub 會建議幾種現成的 workflow 範本,選一個符合你工具的,或用現有的 workflow。",
            "之後每次 push,Actions 會建置並更新網站。"]),
       see("Actions 分頁出現部署的執行紀錄;完成後網站內容更新。"),
       tip("純 HTML 的靜態網站,不需要建置,步驟 6 就夠了。"))
)

gotchas = section("gotchas", "常見卡關",
  details("workflow 沒有跑",
          "<p>依序檢查:</p><ol class='ops'><li>檔案位置是不是 <code>.github/workflows/xxx.yml</code>(資料夾名稱與副檔名都要對)。</li><li><code>on</code> 的事件和分支是否符合你的操作(例如設定 push 到 <code>main</code>,你卻 push 到別的分支)。</li><li>YAML 縮排有沒有錯。到 Actions 分頁,常常會直接顯示語法錯誤。</li></ol>"),
  details("Actions 日誌說 <code>Permission denied</code> 或需要權限",
          "<p>預設的 token 權限有限。需要寫入(例如推送、開 Release)時,在 workflow 加上 <code>permissions:</code> 區塊,只給需要的最小權限。</p>" + cmd("permissions:\n  contents: read")),
  details("Pages 顯示 404",
          "<p>檢查三件事:<code>index.html</code> 是否在你選的分支與資料夾的最外層;檔名是否完全是小寫的 <code>index.html</code>;是否等了一兩分鐘讓部署完成。也可以在 Actions 分頁看有沒有 Pages 的部署紀錄。</p>"),
  details("網站樣式或圖片壞掉,但 HTML 有出來",
          "<p>專案網站的網址帶有 repo 名稱(<code data-tpl>/{repo}/</code>),所以資源路徑要用<b>相對路徑</b>(<code>style.css</code>),而不是以 <code>/</code> 開頭的絕對路徑(<code>/style.css</code>)。</p>"),
  details("要付費嗎?",
          "<p>公開 repo 使用 GitHub 提供的標準 runner 一般是免費的;私人 repo 的免費額度依方案而定(個人免費方案每月有一定額度的使用量,Linux 計費最便宜,Windows 與 macOS 較貴)。額度與價格會調整,請以 GitHub 帳號的 Billing 頁與官方文件為準。</p>"))

SIM = {
  "w1": "<b>檢查檔案位置與觸發條件。</b>檔案必須在 <code>.github/workflows/</code>,<code>on</code> 的事件與分支要符合你的操作。Actions 分頁可能會顯示語法錯誤。",
  "w2": "<b>看日誌找出失敗的那一步。</b>點進失敗的 step 看紅色錯誤訊息;多數是縮排、指令打錯,或測試真的沒過。",
  "w3": "<b>檢查來源與資料夾。</b>確認 Source 選對、分支與資料夾對、<code>index.html</code> 在最外層,並等一兩分鐘。",
  "w4": "<b>把資源路徑改成相對路徑。</b>專案網站的網址帶 repo 名稱,以 <code>/</code> 開頭的路徑會指到網域根目錄而找不到檔案。"
}
QUIZ = quiz_cfg([
  ("workflow 檔案放在哪裡才會被 GitHub 執行?", ["任意位置", ".github/workflows/ 資料夾底下的 .yml 檔", "README.md 裡"], 1,
   "位置固定,GitHub 才找得到。"),
  ("為什麼大多數 workflow 的第一步是 <code>actions/checkout</code>?", ["讓機器顯示日誌", "runner 是全新的機器,要先把你的程式碼下載下來", "為了登入 GitHub"], 1,
   "每次 job 都在乾淨的機器上跑,什麼都沒有。"),
  ("<code>on: [push]</code> 代表?", ["每天自動執行", "有人 push 時觸發", "只有手動執行"], 1,
   "on 定義觸發的事件。"),
  ("CI 需要部署金鑰,應該?", ["寫在 workflow 裡", "存成 Actions secret,用 secrets 內容取用", "放在 README"], 1,
   "secrets 不會出現在 repo 內容與日誌中。"),
  ("Pages 網站樣式跑掉,最可能的原因?", ["瀏覽器壞了", "資源用了 / 開頭的絕對路徑,專案網站網址帶 repo 名稱", "Pages 不支援 CSS"], 1,
   "專案網站的根是 /repo/,絕對路徑會指到網域根目錄。"),
])

practice = section("practice", "動手演練:確認你真的懂了",
  '<p class="sub" style="margin-bottom:18px">先選答案再看原因。重點是遇到問題時知道先看哪裡。</p>',
  sim("", "情境:選一個你遇到的狀況", "你想知道要先檢查什麼?",
      [("w1", "workflow 完全沒有執行"), ("w2", "Actions 顯示紅叉"), ("w3", "Pages 顯示 404"), ("w4", "網站出來了但樣式全跑掉")]),
  QUIZ_HTML,
  checks(["我知道 workflow 要放在 <code>.github/workflows/</code>。",
          "我的 YAML 用空白縮排,沒有用 Tab。",
          "我知道每個 job 的第一步通常是 checkout。",
          "我能到 Actions 分頁看日誌找失敗的原因。",
          "我的金鑰存在 Actions secrets,不在 workflow 檔裡。",
          "我知道專案網站的資源要用相對路徑。",
          "我了解免費額度會調整,會到帳號的 Billing 頁確認。"]),
  resources([
    ("https://docs.github.com/en/actions/get-started/quickstart", "Actions 快速入門", "Quickstart for GitHub Actions"),
    ("https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions", "在 Actions 使用 secrets", "Using secrets in GitHub Actions"),
    ("https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site", "設定 Pages 的發佈來源", "Configuring a publishing source for your GitHub Pages site"),
    ("https://docs.github.com/en/billing/concepts/product-billing/github-actions", "Actions 計費", "GitHub Actions billing"),
  ]))

SPEC = dict(
  file="github-actions-guide.html",
  title="GitHub Actions 與 Pages:自動跑測試、發佈網站",
  eyebrow="第 11 篇 · Actions 與 Pages(進階選讀)",
  h1="寫一個 YAML,讓 GitHub 自動幫你測試與發佈網站",
  sub="從最小的 workflow 開始:push 之後自動 checkout 與跑指令,在 Actions 分頁看日誌,再用 GitHub Pages 把靜態網頁變成公開網站。",
  tldr="workflow 是 <code>.github/workflows/</code> 裡的 YAML:<strong>事件(on)→ job → step</strong>,第一步通常是 <code>actions/checkout</code>。結果看 Actions 分頁;金鑰放 secrets;網站用 <b>Settings → Pages</b> 從分支或 Actions 發佈。",
  toc=[("what", "Actions 與 Pages"), ("map", "全貌圖"), ("fill", "填入你的資料"), ("steps", "七個步驟"), ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, mapsec, fillsec, section("steps", "照著做:七個步驟", S), gotchas, practice]),
  config=dict(fill=dict(me="your-name", repo="hello-world", branch="main"), sim=SIM, quiz=QUIZ),
  prev=("github-security-guide.html", "安全性:Secrets 與 Dependabot"),
  next=None,
)
