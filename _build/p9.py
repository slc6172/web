from h import *

SVG = '''<svg viewBox="0 0 900 230" role="img" aria-label="版本號 MAJOR.MINOR.PATCH 各自代表的意義,以及從 tag 到 Release 的流程">
      <defs>
        <marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#87867F"/></marker>
        <style>.m{font:600 28px ui-monospace,Menlo,monospace}.mm{font:12px ui-monospace,Menlo,monospace}.s{font:12px system-ui,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif}.nn{font:600 12px ui-monospace,Menlo,monospace}</style>
      </defs>
      <rect width="900" height="230" fill="#FFFFFF"/>
      <text x="20" y="26" class="s" fill="#87867F">版本號 v2.4.1 的三個數字</text>
      <rect x="20" y="40" width="180" height="90" rx="10" fill="#FBF1EC" stroke="#B04A3F" stroke-width="1.5"/>
      <text x="110" y="82" text-anchor="middle" class="m" fill="#141413">2</text>
      <text x="110" y="104" text-anchor="middle" class="s" fill="#B04A3F">MAJOR:不相容的改動</text>
      <text x="110" y="121" text-anchor="middle" class="s" fill="#3D3D3A">舊用法可能壞掉</text>
      <rect x="220" y="40" width="180" height="90" rx="10" fill="#F0EEE6" stroke="#3D3D3A" stroke-width="1.5"/>
      <text x="310" y="82" text-anchor="middle" class="m" fill="#141413">4</text>
      <text x="310" y="104" text-anchor="middle" class="s" fill="#3D3D3A">MINOR:新增功能</text>
      <text x="310" y="121" text-anchor="middle" class="s" fill="#3D3D3A">舊用法照常能用</text>
      <rect x="420" y="40" width="180" height="90" rx="10" fill="#EEF2E8" stroke="#788C5D" stroke-width="1.5"/>
      <text x="510" y="82" text-anchor="middle" class="m" fill="#141413">1</text>
      <text x="510" y="104" text-anchor="middle" class="s" fill="#4B5C39">PATCH:修 bug</text>
      <text x="510" y="121" text-anchor="middle" class="s" fill="#3D3D3A">不改任何行為</text>
      <text x="40" y="168" class="s" fill="#B85C3E">升 MAJOR,後面兩個歸零(2.4.1 → 3.0.0);升 MINOR,PATCH 歸零(2.4.1 → 2.5.0)</text>
      <rect x="640" y="40" width="240" height="90" rx="10" fill="#E3DACC" stroke="#3D3D3A" stroke-width="2"/>
      <text x="760" y="76" text-anchor="middle" class="mm" fill="#141413">tag v2.4.1</text>
      <text x="760" y="98" text-anchor="middle" class="s" fill="#3D3D3A">指向某個 commit 的書籤</text>
      <text x="760" y="116" text-anchor="middle" class="s" fill="#3D3D3A">+ Release:說明與附件</text>
      <circle cx="620" cy="85" r="0" fill="none"/>
      <line x1="604" y1="85" x2="636" y2="85" stroke="#87867F" stroke-width="1.5" marker-end="url(#ag)"/>
    </svg>'''

what = section("what", "版本號是對使用者的承諾",
  '<div class="panel"><h3>用「書的版次」來想</h3>'
  '<p>書出了新版,封面會寫第幾版,讀者才知道自己手上的是不是最新、改了什麼。軟體也一樣:<b>tag</b> 是在某個 commit 上貼的書籤(<code>v1.2.0</code>),<b>Release</b> 則是在這個書籤旁邊附上更新說明與可下載的檔案。</p>'
  '<p style="margin-bottom:0">使用者看到版本號,就能判斷「升級會不會壞掉我的東西」。所以<b>版本號要照規則升</b>。</p></div>',
  '<h3 style="margin-top:26px">五個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["tag", "貼在某個 commit 上的固定標記,通常用版本號命名,例如 <code>v1.2.0</code>。"],
    ["lightweight / annotated tag", "輕量 tag 只是名字;<b>annotated tag</b>(<code>-a</code>)還附有作者、日期與說明,建議用這種。"],
    ["SemVer(語意化版本)", "<code>MAJOR.MINOR.PATCH</code> 的命名規則,見下圖。"],
    ["Release", "GitHub 上一頁正式的發佈,連結到一個 tag,可附說明與檔案。"],
    ["Pre-release", "標示為預覽版:還不穩定,不是給所有人用的。"],
  ]))

mapsec = section("map", "全貌:三個數字,各代表一種承諾",
  '<p class="sub" style="margin-bottom:16px">版本號 <code>v2.4.1</code> 拆開來看。右邊是它在 GitHub 上的樣子:tag 加上 Release。</p>',
  canvas(SVG, [
    ("2", "<b>MAJOR</b>:有不相容的改動。使用者升級前必須看說明。"),
    ("4", "<b>MINOR</b>:新增功能,舊功能照舊。"),
    ("1", "<b>PATCH</b>:只修 bug,行為不變。"),
  ]))

fillsec = section("fill", "先填入你的資料,下面的指令會自動換成你的版本",
  fill([("me", "你的 GitHub 帳號", False), ("repo", "專案名稱", False), ("ver", "版本號(含 v)", False)]))

S = steps(
  step(1, "先決定這次是哪一種升級",
       "版本號不是亂取的。問自己:這次改動,會不會讓<b>舊的用法壞掉</b>?",
       table("g3", ["這次改了…", "升哪一位", "例子"], [
         ["修 bug、文字更正,行為不變", "PATCH", "<code>1.2.3 → 1.2.4</code>"],
         ["新增功能,舊功能照常可用", "MINOR(PATCH 歸零)", "<code>1.2.4 → 1.3.0</code>"],
         ["改了既有用法、移除功能", "MAJOR(其餘歸零)", "<code>1.3.0 → 2.0.0</code>"],
         ["還在開發、尚未穩定", "<code>0.x.y</code>,或加上 <code>-beta.1</code> 這類後綴", "<code>0.9.0</code>、<code>1.0.0-rc.1</code>"],
       ]),
       tip("第一次正式發佈通常從 <code>v1.0.0</code> 開始;還不穩定就先用 <code>v0.1.0</code>。")),
  step(2, "確認要發佈的內容已經在 main 上",
       "tag 會貼在目前所在的那個 commit。貼錯位置,版本號就對不上內容。",
       cmd("git switch main\ngit pull\ngit status\ngit log --oneline -n 3"),
       see("<code>git status</code> 顯示 <code>nothing to commit, working tree clean</code> 與 <code>up to date with 'origin/main'</code>。"),
       warn("沒有 clean 或沒有 pull 到最新,就先處理,不然 tag 會貼在不是你想發佈的 commit 上。")),
  step(3, "建立 annotated tag",
       "<code>-a</code> 表示 annotated,<code>-m</code> 是這個版本的簡短說明。",
       cmd('git tag -a {ver} -m "Release {ver}"\ngit tag\ngit show {ver} --stat'),
       see("<code>git tag</code> 列出所有 tag,其中有 <code data-tpl>{ver}</code>;<code>git show</code> 顯示 tag 的資訊與它指向的 commit。"),
       tip("貼錯了想刪掉(還沒 push):<code>git tag -d {ver}</code>。")),
  step(4, "把 tag 推上 GitHub",
       "<b>tag 不會隨著 <code>git push</code> 一起上去</b>,要另外送。",
       cmd("git push origin {ver}\n# 一次推送全部本機 tag:\n# git push origin --tags"),
       see("終端機顯示 <code>* [new tag]  {ver} -&gt; {ver}</code>。在 GitHub 的 repo 頁面,切換分支選單旁的 <b>Tags</b> 可以看到它。")),
  step(5, "在網頁上建立 Release",
       "tag 只是標記。Release 才是給使用者看的發佈頁。",
       ops(["在 repo 首頁,右側 <b>Releases</b> 區塊點 <b>Releases</b>(或用網址 <code data-tpl>github.com/{me}/{repo}/releases</code>)。",
            "按 <b>Draft a new release</b>(若是第一次,也可能顯示 <b>Create a new release</b>)。",
            "<b>Choose a tag</b> 下拉選擇剛推上去的 <code data-tpl>{ver}</code>。",
            "<b>Release title</b> 填 <code data-tpl>{ver}</code> 或帶一點說明的標題。"]),
       see("頁面進入編輯狀態,左上顯示你選的 tag,下方是一個說明編輯框。")),
  step(6, "寫 Release notes(可用自動產生)",
       "說明要寫給使用者看:新增什麼、修了什麼、需要注意什麼。",
       ops(["在 <b>Describe this release</b> 裡,按 <b>Generate release notes</b>,GitHub 會依合併過的 PR 自動列出清單與貢獻者。",
            "<b>Previous tag</b> 選上一個版本,清單才會是「這次與上次之間」的差異。",
            "自動產生的內容可以再編輯。有不相容的改動,務必在最前面寫出來。"]),
       cmd("## 新增\n- 搜尋支援依標籤篩選 (#34)\n\n## 修正\n- 修正匯出 CSV 時中文亂碼 (#36)\n\n## 注意\n- 設定檔欄位 `theme` 更名為 `colorTheme`,請參考遷移說明", cap="Release notes 範例"),
       see("說明框出現依 PR 整理的條列;預覽分頁可看到最後的樣子。")),
  step(7, "選發佈類型、附檔案、發佈",
       "Release 有三種常見狀態,依成熟度選。",
       ops(["有要附上的安裝檔或壓縮檔,拖曳到 <b>Attach binaries</b> 的區域。",
            "還不穩定:勾 <b>Set as a pre-release</b>,標成預覽版。",
            "正式版:勾 <b>Set as the latest release</b>(不勾的話,GitHub 依版本號決定哪個是最新)。",
            "還沒寫完:按 <b>Save draft</b> 存成草稿,只有管理者看得到。",
            "準備好了,按 <b>Publish release</b>。"]),
       see("Release 頁面公開,綠色標籤 <b>Latest</b> 或橘色標籤 <b>Pre-release</b>。repo 首頁右側 Releases 區塊顯示最新版本號。"),
       warn("GitHub 會自動附上「原始碼的壓縮檔」(Source code .zip / .tar.gz),不需要自己上傳。若要附編譯好的檔案,才需要在步驟中附檔。", "提醒"))
)

STAGES = [
  dict(badge="Draft", tone="warn", label="草稿",
       c=dict(h="只有你看得到", items=["可以反覆修改說明、換附件。", "按 <b>Save draft</b> 存起來,晚點再發佈。"]),
       o=dict(h="還沒公開", items=["使用者與訂閱的人不會收到通知。", "適合先貼上、請同事看一次說明。"])),
  dict(badge="Pre-release", tone="warn", label="預覽版",
       c=dict(h="勾 This is a pre-release", items=["tag 常用 <code>v1.0.0-rc.1</code>、<code>v1.0.0-beta.2</code>。", "公開但標示「預覽」,不會被標成 Latest。"]),
       o=dict(h="蒐集回饋", items=["請願意試用的人測試,回報的問題開成 Issue。", "確認穩定了,再發正式版。"])),
  dict(badge="Latest", tone="done", label="正式版",
       c=dict(h="發佈", items=["按 <b>Publish release</b>,標上 Latest。", "訂閱 release 通知的人會收到通知。"]),
       o=dict(h="對外承諾", items=["說明裡把不相容的改動寫在最前面。", "版本號一旦發佈就不要改;有錯就發新的 PATCH。"]))
]

stagesec = section("states", "發佈的三種狀態",
  '<p class="sub">點選下面的狀態,左邊看你怎麼做,右邊看對使用者有什麼意義。</p>\n'
  '<div class="stages" id="stages" role="group" aria-label="Release 的狀態"></div>\n'
  '<div class="two">\n<div class="panel"><h3>你怎麼做:<span id="c-h"></span></h3><ul id="c-list"></ul></div>\n'
  '<div class="panel"><h3>對使用者意味著:<span id="o-h"></span></h3><ul id="o-list"></ul></div>\n</div>\n'
  '<div class="stage-nav"><button type="button" class="ghost" id="prevStage">← 上一階段</button><button type="button" class="ghost" id="nextStage">下一階段 →</button></div>')

gotchas = section("gotchas", "常見卡關",
  details("Release 的 Choose a tag 下拉選單找不到我的 tag",
          "<p>多半是 tag 還沒推到 GitHub。用 <code>git push origin 版本號</code> 推上去,重新整理頁面。也可以直接在下拉裡輸入新的版本號並選 <b>Create new tag</b>,這時要再選 <b>Target</b> 是哪個分支。</p>"),
  details("tag 貼錯 commit 了",
          "<p>如果還沒推上去,<code>git tag -d 版本號</code> 刪掉重打。已經推上去,但還沒對外宣布,先在 GitHub 刪掉那個 Release 與 tag,再重打。已經被人用了,就別動它,發一個新的 PATCH。</p>" +
          cmd("git tag -d {ver}\ngit push origin --delete {ver}")),
  details("發佈後發現有 bug",
          "<p>不要改已發佈的版本。修好之後發一個新的 PATCH 版(例如 <code>v1.2.4</code>),說明裡簡短交代修了什麼。</p>"),
  details("我應該用 <code>v1.0.0</code> 還是 <code>1.0.0</code>?",
          "<p>兩者都可以。多數專案加前綴 <code>v</code>。重點是<b>全專案保持一致</b>,工具與腳本才不會出錯。</p>"),
  details("可以讓 GitHub 自動發 Release 嗎?",
          "<p>可以,用 GitHub Actions 在推上 tag 時自動建立 Release 並附上建置好的檔案,見第 11 篇。</p>"))

SIM = {
  "v1": "<b>PATCH:<code>2.4.1 → 2.4.2</code>。</b>只修 bug、行為不變,只升最後一位。",
  "v2": "<b>MINOR:<code>2.4.1 → 2.5.0</code>。</b>新增功能但舊用法照常,升中間位,PATCH 歸零。",
  "v3": "<b>MAJOR:<code>2.4.1 → 3.0.0</code>。</b>改了既有用法會讓舊程式壞掉,升第一位,其餘歸零,並在說明裡寫清楚遷移方式。"
}
QUIZ = quiz_cfg([
  ("新增了一個功能,舊功能完全照常運作。版本號從 2.4.1 該升到?", ["2.4.2", "2.5.0", "3.0.0"], 1,
   "新增功能升 MINOR,PATCH 歸零。"),
  ("<code>git push</code> 之後,tag 會自動上去嗎?", ["會", "不會,要另外 git push origin 版本號", "只有 annotated tag 會"], 1,
   "tag 要另外推送,或用 --tags 一次推全部。"),
  ("Release 與 tag 的關係是?", ["完全一樣", "Release 是建立在 tag 上的發佈頁,可附說明與檔案", "Release 只能手動刪除"], 1,
   "tag 是標記,Release 是給使用者看的發佈頁。"),
  ("發佈 <code>v1.2.3</code> 後發現 bug,正確做法是?", ["修改 v1.2.3 的內容重新發佈", "修好後發 v1.2.4", "刪掉專案"], 1,
   "已發佈的版本不要變動,用新的 PATCH 版。"),
  ("版本還不穩定,想先給願意試用的人,應該?", ["直接發正式版", "勾選 This is a pre-release", "不要發佈"], 1,
   "Pre-release 公開但標示為預覽版,適合蒐集回饋。"),
])

practice = section("practice", "動手演練:確認你真的懂了",
  '<p class="sub" style="margin-bottom:18px">先選答案再看原因。重點是練習看到改動就知道升哪一位。</p>',
  sim("", "情境:目前版本是 <code>2.4.1</code>", "這次改了什麼?你想知道新版本號要怎麼升?",
      [("v1", "只修了一個 bug"), ("v2", "新增一個功能,舊功能照常"), ("v3", "改了設定檔格式,舊設定會失效")]),
  QUIZ_HTML,
  checks(["我知道 PATCH、MINOR、MAJOR 各代表什麼。",
          "發佈前我先確認 main 是最新且 clean。",
          "我用 annotated tag(<code>-a</code>)並記得 <code>git push origin 版本號</code>。",
          "Release notes 把不相容的改動寫在最前面。",
          "還不穩定的版本我會勾 pre-release。",
          "我知道已發佈的版本不改,有錯就發新的 PATCH。"]),
  resources([
    ("https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository", "管理 Release", "Managing releases in a repository"),
    ("https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes", "自動產生 Release notes", "Automatically generated release notes"),
    ("https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases", "關於 Release", "About releases"),
  ]))

SPEC = dict(
  file="github-release-guide.html",
  title="Release 與版本號:版本號是對使用者的承諾",
  eyebrow="第 9 篇 · Release 與版本號",
  h1="版本號是對使用者的承諾:用 tag 與 Release 發佈",
  sub="把做好的成果正式交給使用者:決定版本號、貼上 tag、在 GitHub 上建立有說明與附件的 Release。重點是學會看改動內容決定該升哪一位。",
  tldr="版本號 <code>MAJOR.MINOR.PATCH</code>:<strong>壞掉舊用法升 MAJOR、新增功能升 MINOR、只修 bug 升 PATCH</strong>。流程是 <code>git tag -a</code> → <code>git push origin 版本號</code> → 在網頁 <b>Draft a new release</b>。",
  toc=[("what", "tag 與 Release"), ("map", "全貌圖"), ("fill", "填入你的資料"), ("steps", "七個步驟"), ("states", "三種發佈狀態"), ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, mapsec, fillsec, section("steps", "照著做:七個步驟", S), stagesec, gotchas, practice]),
  config=dict(fill=dict(me="your-name", repo="hello-world", ver="v1.0.0"), sim=SIM, quiz=QUIZ, stages=STAGES),
  prev=("github-undo-guide.html", "還原與救援"),
  next=("github-security-guide.html", "安全性:Secrets 與 Dependabot"),
)
