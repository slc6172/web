from h import *

SVG = '''<svg viewBox="0 0 900 230" role="img" aria-label="Issue 的旅程:提出、分類與指派、開分支與 PR、合併後自動關閉">
      <defs>
        <marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#87867F"/></marker>
        <marker id="ao" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#788C5D"/></marker>
        <style>.m{font:12px ui-monospace,Menlo,monospace}.s{font:12px system-ui,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif}.nn{font:600 12px ui-monospace,Menlo,monospace}</style>
      </defs>
      <rect width="900" height="230" fill="#FFFFFF"/>
      <rect x="20" y="40" width="170" height="84" rx="10" fill="#F0EEE6" stroke="#3D3D3A" stroke-width="1.5"/>
      <text x="105" y="76" text-anchor="middle" class="s" fill="#141413">Issue #12</text>
      <text x="105" y="96" text-anchor="middle" class="s" fill="#3D3D3A">有人提出問題或想法</text>
      <rect x="250" y="40" width="190" height="84" rx="10" fill="#F0EEE6" stroke="#3D3D3A" stroke-width="1.5"/>
      <text x="345" y="76" text-anchor="middle" class="s" fill="#141413">分類與指派</text>
      <text x="345" y="96" text-anchor="middle" class="s" fill="#3D3D3A">labels・assignee・Project</text>
      <rect x="500" y="40" width="190" height="84" rx="10" fill="#F0EEE6" stroke="#3D3D3A" stroke-width="1.5"/>
      <text x="595" y="76" text-anchor="middle" class="s" fill="#141413">分支 + Pull Request</text>
      <text x="595" y="96" text-anchor="middle" class="s" fill="#3D3D3A">PR 說明寫 Closes #12</text>
      <rect x="750" y="40" width="130" height="84" rx="10" fill="#E3DACC" stroke="#3D3D3A" stroke-width="2"/>
      <text x="815" y="76" text-anchor="middle" class="s" fill="#141413">Closed</text>
      <text x="815" y="96" text-anchor="middle" class="s" fill="#3D3D3A">自動關閉</text>
      <line x1="193" y1="82" x2="246" y2="82" stroke="#87867F" stroke-width="1.5" marker-end="url(#ag)"/>
      <circle cx="220" cy="62" r="11" fill="#D97757"/><text x="220" y="66.5" text-anchor="middle" class="nn" fill="#fff">1</text>
      <line x1="443" y1="82" x2="496" y2="82" stroke="#87867F" stroke-width="1.5" marker-end="url(#ag)"/>
      <circle cx="470" cy="62" r="11" fill="#D97757"/><text x="470" y="66.5" text-anchor="middle" class="nn" fill="#fff">2</text>
      <line x1="693" y1="82" x2="746" y2="82" stroke="#788C5D" stroke-width="2" marker-end="url(#ao)"/>
      <circle cx="720" cy="62" r="11" fill="#788C5D"/><text x="720" y="66.5" text-anchor="middle" class="nn" fill="#fff">3</text>
      <text x="40" y="172" class="s" fill="#B85C3E">提出者負責:①(寫清楚)</text>
      <text x="270" y="172" class="s" fill="#4B5C39">維護者負責:②(分類、決定、排進計畫)與 ③(合併即關閉)</text>
    </svg>'''

what = section("what", "Issue 是專案的「問題單」",
  '<div class="panel"><h3>用「客服工單」來想</h3>'
  '<p>有人發現 bug、想要新功能、或有疑問,就開一張 <b>Issue</b>(工單)。維護者收到後分類、決定要不要做、指派給誰;做完之後用 Pull Request 把它<b>關掉</b>。討論、決策與進度都留在同一個地方,不會散落在聊天室裡。</p>'
  '<p style="margin-bottom:0">Issue 的品質決定對方要不要追問你。<b>好的 Issue 讓對方不用追問。</b></p></div>',
  '<h3 style="margin-top:26px">七個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["Issue / #編號", "一張問題單。每張有自己的編號,例如 <code>#12</code>,可以在別處用 <code>#12</code> 引用它。"],
    ["label(標籤)", "分類用的貼紙,例如 <code>bug</code>、<code>enhancement</code>、<code>good first issue</code>。"],
    ["assignee(指派)", "這張單由誰負責。"],
    ["milestone(里程碑)", "把一批 Issue 歸到同一個目標,例如「v1.0」,並顯示完成進度。"],
    ["Projects(專案看板)", "把 Issue 與 PR 排成看板或表格,用欄位(如 Status)追蹤進度。"],
    ["Closes #12", "寫在 PR 說明裡的關鍵字。這個 PR 合併進預設分支時,會自動關閉 Issue #12。"],
    ["Close reason", "關閉有不同理由:已完成、不打算做(not planned)、重複(duplicate)。"],
  ]))

mapsec = section("map", "全貌:一張 Issue 從提出到關閉",
  '<p class="sub" style="margin-bottom:16px">提出者主要做第 1 步,維護者主要做第 2、3 步;但任何人都可以在討論中留言幫忙。</p>',
  canvas(SVG, [
    ("1", "<b>提出</b>:寫標題與內文,送出 Issue。<span class=\"role c\">提出者</span>"),
    ("2", "<b>分類與指派</b>:貼標籤、指派、排進里程碑與看板。<span class=\"role o\">維護者</span>"),
    ("3", "<b>解決並關閉</b>:PR 說明寫 <code>Closes #編號</code>,合併後自動關閉。<span class=\"role o\">維護者</span>"),
  ]))

TEMPLATE = """## 發生什麼事
按下「儲存」之後頁面變成空白。

## 重現步驟
1. 打開 設定 頁
2. 修改暱稱
3. 按下「儲存」

## 預期結果
顯示「已儲存」。

## 實際結果
頁面空白,沒有任何訊息。

## 環境
- 瀏覽器:Chrome 126
- 作業系統:macOS 14"""

ISSUE_TPL = """---
name: 回報問題
about: 回報 bug 或使用上的問題
title: "[Bug] "
labels: bug
---

## 發生什麼事

## 重現步驟
1.
2.

## 預期結果

## 實際結果

## 環境
- 瀏覽器 / 版本:
- 作業系統:"""

roles = '''<div class="role-tabs" role="tablist" aria-label="選擇視角">
    <button type="button" role="tab" id="tab-c" aria-controls="panel-c" aria-selected="true" data-role="c" class="on"><span class="rt">視角 A · 6 個步驟</span><b>我是提出者</b><span>我想回報問題或提出想法</span></button>
    <button type="button" role="tab" id="tab-o" aria-controls="panel-o" aria-selected="false" data-role="o" tabindex="-1"><span class="rt">視角 B · 7 個步驟</span><b>我是維護者</b><span>有人對我的專案開了 Issue</span></button>
  </div>'''

SC = steps(
  step(1, "先搜尋,確認不是重複的",
       "多數專案已經有人回報過。先搜尋可以幫你省時間,也不會讓維護者重複處理。",
       ops(["進入專案頁面,點上方的 <b>Issues</b> 分頁。",
            "在搜尋框輸入關鍵字(錯誤訊息的關鍵字最有效)。<b>預設只搜尋 Open</b> 的 Issue,記得也看看 <b>Closed</b>。",
            "找到類似的,就在那張 Issue 底下留言補充你的情況,不要再開新的。"]),
       see("搜尋結果列出符合的 Issue,每張有編號、標題、標籤與留言數。")),
  step(2, "按 New issue,選對範本",
       "如果專案設了範本,會讓你先選類型(回報問題、功能建議……)。範本會把該寫的欄位預先列好。",
       ops(["在 Issues 頁按綠色的 <b>New issue</b>。",
            "若出現範本清單,選最符合的一個,按 <b>Get started</b>。"]),
       see("跳到填寫頁面,可能已經預填了一些標題與段落。"),
       warn("找不到 <b>Issues</b> 分頁?代表這個 repo 沒有開啟 Issue 功能(維護者可以在 repo 的 Settings 裡開關)。這時請看專案 README 有沒有說明聯絡方式。")),
  step(3, "寫一個一眼看懂的標題",
       "維護者每天會看到很多張 Issue,標題是他決定要不要點進來的依據。",
       table("g2", ["不好的標題", "好的標題"], [
         ["壞了", "設定頁按「儲存」後變成空白(Chrome 126,macOS)"],
         ["請修好!!!", "匯出 CSV 時中文變成亂碼"],
         ["有個想法", "建議:搜尋框支援依標籤篩選"],
       ]),
       tip("標題就是結論:說出「什麼東西、在什麼情況下、怎麼了」。")),
  step(4, "內文:讓對方能重現問題",
       "維護者不在你的電腦前。能照著做就看到同樣問題,這張 Issue 就成功了一半。",
       cmd(TEMPLATE, cap="內文範例(回報 bug)"),
       see("重現步驟、預期結果與實際結果分開寫,維護者只需要看一眼就能判斷。"),
       warn("貼錯誤訊息或日誌時,<b>先檢查有沒有密碼、token、個人資料</b>再貼。Issue 預設是公開的。", "隱私")),
  step(5, "附上截圖與日誌",
       "一張圖勝過一百字,但也要挑重點。",
       ops(["截圖可以直接貼上或拖曳到內文框,GitHub 會自動上傳並產生圖片語法。",
            "較長的日誌用程式碼區塊包起來(前後各一行三個反引號 <code>```</code>),或用 <code>&lt;details&gt;</code> 收合,避免整頁被洗版。"]),
       see("預覽分頁裡圖片已顯示,日誌是等寬字型的灰底區塊。")),
  step(6, "送出之後:追蹤與回覆",
       "按 <b>Submit new issue</b> 就完成了。接下來的重點是保持聯繫。",
       ops(["你會收到 email 通知。維護者問問題時,盡快回覆。",
            "被貼上 <code>needs more info</code> 之類的標籤,就是在等你補資料。",
            "被關閉也看一下原因:<b>completed</b> 表示已解決;<b>not planned</b> 或 <b>duplicate</b> 是正常的決定,不是針對你。"]),
       see("Issue 頁面上方狀態是 <b>Open</b>(綠色);解決後變成 <b>Closed</b>(紫色)。"))
)

SO = steps(
  step(1, "收到通知,先判斷這張單的類型",
       "有人開 Issue 時你會收到通知,Issues 分頁的數字也會增加。先讀標題與內文,判斷是 bug、功能建議、提問還是重複。",
       see("Issue 頁右側有 <b>Assignees</b>、<b>Labels</b>、<b>Projects</b>、<b>Milestone</b> 幾個區塊,後面幾步都是在這裡操作。")),
  step(2, "貼標籤",
       "標籤讓你(和志工)之後能篩選。不需要很多,一組簡單的就夠。",
       ops(["點右側 <b>Labels</b> 旁的齒輪,勾選合適的標籤。",
            "常見組合:<code>bug</code>、<code>enhancement</code>、<code>question</code>、<code>documentation</code>、<code>good first issue</code>(適合新手上手)。",
            "缺資料就貼上 <code>needs more info</code> 之類的標籤,並留言說明需要什麼。"]),
       see("標籤出現在 Issue 標題下方與列表上,可以點標籤篩選同類的 Issue。")),
  step(3, "指派負責人與里程碑",
       "沒有人負責的 Issue,通常就不會被做。",
       ops(["<b>Assignees</b> 旁點齒輪,選負責的人(也可以選自己)。",
            "有版本規劃時,在 <b>Milestone</b> 選擇對應的里程碑,例如 <code>v1.0</code>。"]),
       see("右側顯示負責人頭像;里程碑頁面能看到「已關閉 / 總數」的進度條。")),
  step(4, "放進 Projects 看板",
       "Projects 把散落的 Issue 與 PR 排成一個看得見進度的表格或看板。",
       ops(["在 repo 或你的帳號 / 組織頁面進入 <b>Projects</b>,建立一個新的 Project,選 <b>Board</b>(看板)版型。",
            "預設有 <b>Todo</b>、<b>In Progress</b>、<b>Done</b> 三欄,對應內建的 <b>Status</b> 欄位。",
            "回到 Issue,右側 <b>Projects</b> 旁選擇這個 Project;也可以在看板上直接把 Issue 加進來,再拖曳卡片換欄位。"]),
       see("卡片出現在看板的 Todo 欄,拖到 In Progress 後,Issue 的 Status 也跟著更新。"),
       tip("Projects 的介面更新得比較頻繁,實際畫面請以 GitHub 為準。")),
  step(5, "(選用)設定 Issue 範本",
       "範本讓每個人一開始就填對欄位,你就不用一直追問。範本是放在 repo 裡的檔案。",
       cmd(ISSUE_TPL, cap=".github/ISSUE_TEMPLATE/bug-report.md"),
       ops(["在 repo 建立資料夾 <code>.github/ISSUE_TEMPLATE/</code>,把上面的內容存成裡面的 <code>bug-report.md</code>。",
            "commit 並 push 到預設分支(通常是 <code>main</code>)。"]),
       see("之後別人按 <b>New issue</b>,就會先看到「回報問題」這個選項,標題與標籤已預填。")),
  step(6, "用 Pull Request 解決並自動關閉",
       "解決問題的 PR,在說明裡寫關鍵字加編號,合併時就會自動關閉對應的 Issue。",
       cmd("Closes #12\n# 也可以用 Fixes #12 或 Resolves #12", cap="寫在 PR 說明裡"),
       see("PR 頁面右側 <b>Development</b> 會顯示連結的 Issue。合併後,Issue 自動變成 Closed。"),
       warn("自動關閉只有在 PR <b>合併進預設分支</b>時才會發生。合併到其他分支,Issue 不會被關。")),
  step(7, "關閉:選對理由",
       "不是每張 Issue 都要做。清楚地關閉,對提出者也是一種尊重。",
       ops(["Issue 頁底部的 <b>Close issue</b> 旁有下拉選單,選 <b>Close as completed</b>(已完成)、<b>Close as not planned</b>(不打算做),或在重複時選 <b>Close as duplicate</b>。",
            "關閉前先留言說明原因並感謝對方。"]),
       see("Issue 狀態變成紫色或灰色的 <b>Closed</b>,並標示關閉理由。"))
)

body_roles = '''<div role="tabpanel" id="panel-c" aria-labelledby="tab-c" data-panel="c">
    <div class="orient">
      <div class="panel known"><span class="k">你已經會的</span>用瀏覽器操作 GitHub、貼文字與圖片</div>
      <div class="panel new"><span class="k">這次要新學的</span>搜尋重複、寫清楚的標題與重現步驟、保持追蹤</div>
    </div>
    ''' + SC + '''
  </div>
  <div role="tabpanel" id="panel-o" aria-labelledby="tab-o" data-panel="o" hidden>
    <div class="orient">
      <div class="panel known"><span class="k">你已經會的</span>建立 repo、<code>git push</code></div>
      <div class="panel new"><span class="k">這次要新學的</span>標籤、指派、Projects 看板、範本,以及 <code>Closes #編號</code></div>
    </div>
    ''' + SO + '''
  </div>'''

rolesec = section("roles", "選一個視角,照著步驟做",
  '<p class="sub">同一張 Issue,兩個人各做各的事。可以隨時切換視角對照著看。</p>', roles, body_roles)

togethersec = section("together", "同一張 Issue,兩邊在同一個時間點各做什麼",
  '<p class="sub">點選下面的階段,看提出者與維護者分別該做什麼。</p>\n'
  '<div class="stages" id="stages" role="group" aria-label="Issue 的階段"></div>\n'
  '<div class="two">\n<div class="panel"><h3><span class="role c">提出者</span><span id="c-h"></span></h3><ul id="c-list"></ul></div>\n'
  '<div class="panel"><h3><span class="role o">維護者</span><span id="o-h"></span></h3><ul id="o-list"></ul></div>\n</div>\n'
  '<div class="stage-nav"><button type="button" class="ghost" id="prevStage">← 上一階段</button><button type="button" class="ghost" id="nextStage">下一階段 →</button></div>')

STAGES = [
  dict(badge="Open", tone="ok", label="剛開立",
       c=dict(h="按下 Submit new issue", items=["Issue 出現,狀態是 <b>Open</b>。", "再讀一遍:步驟、預期、實際都寫了嗎?有沒有貼到密碼或 token?", "等待回應,不需要重複開單。"]),
       o=dict(h="收到通知", items=["讀標題與內文,判斷是 bug、建議、提問或重複。", "有資料不足,先留言請對方補充。", "重複的,關閉並指向原本那張。"])),
  dict(badge="Triaged", tone="ok", label="已分類",
       c=dict(h="看到標籤與指派", items=["看到 <b>bug</b>、<b>enhancement</b> 等標籤,代表維護者已讀過。", "被貼上 <code>needs more info</code> 就補資料並留言。"]),
       o=dict(h="貼標籤、指派、排進計畫", items=["貼上標籤,指派負責人。", "排進里程碑,或加入 Projects 的 Todo 欄。"])),
  dict(badge="In progress", tone="warn", label="進行中",
       c=dict(h="等待修復", items=["有人在處理時,你不需要做什麼。", "若有 PR 連結到這張 Issue,可以去看看並協助測試。"]),
       o=dict(h="有人開始做", items=["看板上的卡片移到 <b>In Progress</b>。", "負責人開分支、寫 PR,說明裡寫 <code>Closes #編號</code>。"])),
  dict(badge="Closed", tone="done", label="已關閉",
       c=dict(h="確認結果", items=["PR 合併後 Issue 自動關閉,狀態變成 <b>Closed</b>。", "到新版本確認問題真的消失了;沒有就留言,並請對方 Reopen。"]),
       o=dict(h="關閉並感謝", items=["PR 合併進預設分支,Issue 自動關閉;或手動選關閉理由。", "留一句謝謝,對第一次回報的人是很大的鼓勵。"]))
]

gotchas = section("gotchas", "常見卡關",
  details("PR 合併了,Issue 卻沒有自動關閉",
          "<p>依序檢查:</p><ol class='ops'><li>關鍵字是不是寫在 <b>PR 說明</b>(或 commit 訊息)裡,而且格式是 <code>Closes #編號</code>。</li>"
          "<li>PR 是不是合併進<b>預設分支</b>(通常是 <code>main</code>)。</li><li>編號對不對、是不是同一個 repo。</li></ol>"),
  details("一張 Issue 裡塞了好幾件事",
          "<p>拆成多張。每張只處理一件事,才能各自指派、各自關閉,也才好用 <code>Closes #編號</code> 對應 PR。在原本那張留言附上新 Issue 的編號即可。</p>"),
  details("我的 Issue 被標成 duplicate 關掉了",
          "<p>這不是拒絕你。代表已經有同一個問題的 Issue 在處理,討論集中在那一張比較有效率。到那張補上你的情況,並按右側的訂閱追蹤進度。</p>"),
  details("Issues 分頁不見了",
          "<p>代表這個 repo 沒有啟用 Issue。維護者可以在 repo 的 <b>Settings</b> 頁的功能區塊開啟 Issues。</p>"))

SIM = {
  "t1": "<b>太模糊。</b>維護者看不出是什麼東西、在什麼情況下壞了,只能再追問一輪。",
  "t2": "<b>正確!</b>說出了「哪裡、做了什麼、結果怎樣」,還附上環境。維護者不用追問就能開始重現。",
  "t3": "<b>不建議。</b>語氣急躁但沒有任何資訊,對解決問題沒有幫助,也會降低對方的意願。"
}
QUIZ = quiz_cfg([
  ("在 PR 說明寫 <code>Closes #12</code>,會發生什麼事?", ["PR 立刻被關閉", "PR 合併進預設分支時,Issue #12 會自動關閉", "Issue #12 被刪除"], 1,
   "關鍵字連結 PR 與 Issue,合併進預設分支時才會自動關閉。"),
  ("開 Issue 之前最該先做什麼?", ["直接開,越多越好", "先搜尋有沒有人回報過", "先寫 PR"], 1,
   "多數問題已有人回報。搜尋能避免重複,也能直接加入既有討論。"),
  ("哪個是比較好的 Issue 標題?", ["壞了", "設定頁按「儲存」後變成空白(Chrome 126,macOS)", "請修好!!!"], 1,
   "好標題說出什麼東西、在什麼情況下、怎麼了,還包含環境。"),
  ("Issue 用 label(標籤)的主要目的?", ["讓 Issue 看起來比較漂亮", "分類,方便篩選與排優先順序", "自動關閉 Issue"], 1,
   "標籤是分類用的貼紙,可以依標籤篩選同一類的 Issue。"),
  ("貼錯誤日誌到 Issue 之前,必須先確認什麼?", ["日誌夠不夠長", "有沒有包含密碼、token 等敏感資訊", "有沒有用大寫"], 1,
   "Issue 預設公開。貼出去之前先檢查並遮掉敏感資料。"),
])

practice = section("practice", "動手演練:確認你真的懂了",
  '<p class="sub" style="margin-bottom:18px">先選答案再看原因。重點是培養「怎麼寫才不用被追問」的直覺。</p>',
  sim('<span class="role c">提出者</span> ', "情境:你要回報一個 bug", "下面三個標題,哪一個最好?",
      [("t1", "壞了"), ("t2", "設定頁按「儲存」後變成空白(Chrome 126,macOS)"), ("t3", "請修好!!!")]),
  QUIZ_HTML,
  checks(['<span class="role c">提出者</span>我開單前搜尋過,也看了 Closed 的 Issue。',
          '<span class="role c">提出者</span>標題說明了什麼東西、什麼情況、怎麼了。',
          '<span class="role c">提出者</span>內文有重現步驟、預期結果、實際結果與環境。',
          '<span class="role c">提出者</span>貼日誌前我檢查過沒有密碼或 token。',
          '<span class="role o">維護者</span>我會貼標籤並指派負責人,讓每張單有人跟。',
          '<span class="role o">維護者</span>我知道 <code>Closes #編號</code> 要寫在 PR 說明,而且要合併進預設分支。',
          '<span class="role o">維護者</span>我關閉 Issue 時會選對理由,並留言說明與感謝。',
          '<span class="role o">維護者</span>我考慮設定 Issue 範本,減少來回追問。']),
  resources([
    ("https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue", "建立 Issue", "Creating an issue"),
    ("https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels", "管理標籤", "Managing labels"),
    ("https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects", "關於 Projects", "About Projects"),
    ("https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository", "設定 Issue 範本", "Configuring issue templates"),
  ]))

SPEC = dict(
  file="github-issues-guide.html",
  title="Issue 與 Projects:好的 Issue 讓對方不用追問",
  eyebrow="第 5 篇 · Issue 與 Projects",
  h1="好的 Issue 讓對方不用追問",
  sub="Issue 是專案的問題單,Projects 是把它們排成看得見進度的看板。同一張 Issue 分兩個視角講:「提出問題的人(提出者)」和「負責處理的人(維護者)」。",
  tldr="提出者:<strong>先搜尋、標題說清楚、附上重現步驟</strong>。維護者:<strong>貼標籤、指派、排進看板</strong>,用 PR 說明裡的 <code>Closes #編號</code> 在合併時自動關閉。",
  toc=[("what", "Issue 是什麼"), ("map", "全貌圖"), ("roles", "兩種視角的步驟"), ("together", "兩邊同步看"), ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, mapsec, rolesec, togethersec, gotchas, practice]),
  config=dict(fill={}, sim=SIM, quiz=QUIZ, stages=STAGES),
  prev=("github-remote-guide.html", "遠端與同步"),
  next=("github-pr-guide.html", "Pull Request"),
)
