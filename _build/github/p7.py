from h import *

SVG = '''<svg viewBox="0 0 900 250" role="img" aria-label="Code Review 流程:送審、自動檢查、審查留言、作者修改後再審,通過規則後合併">
      <defs>
        <marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#87867F"/></marker>
        <marker id="ac" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#D97757"/></marker>
        <style>.m{font:12px ui-monospace,Menlo,monospace}.s{font:12px system-ui,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif}.nn{font:600 12px ui-monospace,Menlo,monospace}</style>
      </defs>
      <rect width="900" height="250" fill="#FFFFFF"/>
      <rect x="20" y="40" width="150" height="80" rx="10" fill="#F0EEE6" stroke="#3D3D3A" stroke-width="1.5"/>
      <text x="95" y="76" text-anchor="middle" class="s" fill="#141413">送審</text><text x="95" y="96" text-anchor="middle" class="s" fill="#3D3D3A">作者開 PR</text>
      <rect x="215" y="40" width="150" height="80" rx="10" fill="#F0EEE6" stroke="#3D3D3A" stroke-width="1.5"/>
      <text x="290" y="76" text-anchor="middle" class="s" fill="#141413">自動檢查</text><text x="290" y="96" text-anchor="middle" class="s" fill="#3D3D3A">Checks 綠勾 / 紅叉</text>
      <rect x="410" y="40" width="150" height="80" rx="10" fill="#F0EEE6" stroke="#3D3D3A" stroke-width="1.5"/>
      <text x="485" y="76" text-anchor="middle" class="s" fill="#141413">審查</text><text x="485" y="96" text-anchor="middle" class="s" fill="#3D3D3A">留言 + 結論</text>
      <rect x="605" y="40" width="130" height="80" rx="10" fill="#F0EEE6" stroke="#3D3D3A" stroke-width="1.5"/>
      <text x="670" y="76" text-anchor="middle" class="s" fill="#141413">修改</text><text x="670" y="96" text-anchor="middle" class="s" fill="#3D3D3A">作者 push</text>
      <rect x="770" y="40" width="110" height="80" rx="10" fill="#E3DACC" stroke="#3D3D3A" stroke-width="2"/>
      <text x="825" y="76" text-anchor="middle" class="s" fill="#141413">合併</text><text x="825" y="96" text-anchor="middle" class="s" fill="#3D3D3A">規則放行</text>
      <line x1="173" y1="80" x2="211" y2="80" stroke="#87867F" stroke-width="1.5" marker-end="url(#ag)"/>
      <line x1="368" y1="80" x2="406" y2="80" stroke="#87867F" stroke-width="1.5" marker-end="url(#ag)"/>
      <line x1="563" y1="80" x2="601" y2="80" stroke="#87867F" stroke-width="1.5" marker-end="url(#ag)"/>
      <path d="M670,44 C670,-5 485,-5 485,36" fill="none" stroke="#D97757" stroke-width="2" marker-end="url(#ac)"/>
      <circle cx="577" cy="20" r="11" fill="#D97757"/><text x="577" y="24.5" text-anchor="middle" class="nn" fill="#fff">1</text>
      <path d="M485,124 C485,185 825,185 825,124" fill="none" stroke="#788C5D" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#ag)"/>
      <circle cx="655" cy="170" r="11" fill="#788C5D"/><text x="655" y="174.5" text-anchor="middle" class="nn" fill="#fff">2</text>
      <text x="40" y="212" class="s" fill="#B85C3E">① 需要修改就在「審查 ↔ 修改」之間來回,直到沒有未解決的意見</text>
      <text x="40" y="234" class="s" fill="#4B5C39">② 通過後,還要符合規則(必要核准數、Checks、Code Owner)才能按 Merge</text>
    </svg>'''

what = section("what", "Code Review:讓第二雙眼睛看過再合併",
  '<div class="panel"><h3>用「出書前的校對」來想</h3>'
  '<p>作者再仔細也會有盲點。Code Review 就是請另一個人在合併前看一遍:找 bug、問疑問、提改善,也讓專案知識不被單一個人壟斷。它的目的不是挑錯,而是<b>讓合併進 main 的東西更可靠</b>。</p>'
  '<p style="margin-bottom:0">好的 review 靠兩件事:<b>小而專一的 PR</b>,與<b>具體而友善的意見</b>。團隊規範(規則集、Code Owner、PR 範本)則讓這件事不靠自覺也能執行。</p></div>',
  '<h3 style="margin-top:26px">七個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["Review", "對一個 PR 送出的整體評語,結論有 Comment / Approve / Request changes 三種。"],
    ["Suggestion", "留言時直接寫出建議的新內容,作者按一下就能採用。"],
    ["Resolve conversation", "某則討論處理完畢後標記為已解決。"],
    ["Required approvals", "規則要求的最少核准人數。沒達到,Merge 按鈕不會放行。"],
    ["Code Owner", "某些檔案的指定負責人。這些檔案被改動時,會自動請他審查。"],
    ["Ruleset / Branch protection", "保護重要分支的規則,例如必須經過 PR、必須通過檢查、禁止強制推送。"],
    ["PR template", "開 PR 時自動預填的說明範本。"],
  ]))

mapsec = section("map", "全貌:審查是一個來回的迴圈",
  '<p class="sub" style="margin-bottom:16px">先看地圖。作者與審查者在中間來回,直到規則放行。</p>',
  canvas(SVG, [
    ("1", "<b>審查 ↔ 修改</b>:審查者留意見,作者改完 push,PR 自動更新。<span class=\"role c\">作者</span><span class=\"role o\">審查者</span>"),
    ("2", "<b>規則放行</b>:核准數、Checks、Code Owner 都滿足,才能 Merge。<span class=\"role o\">審查者</span>"),
  ]))

roles = '''<div class="role-tabs" role="tablist" aria-label="選擇視角">
    <button type="button" role="tab" id="tab-c" aria-controls="panel-c" aria-selected="true" data-role="c" class="on"><span class="rt">視角 A · 6 個步驟</span><b>我是作者</b><span>我的 PR 要被別人審</span></button>
    <button type="button" role="tab" id="tab-o" aria-controls="panel-o" aria-selected="false" data-role="o" tabindex="-1"><span class="rt">視角 B · 6 個步驟</span><b>我是審查者</b><span>我被請來審別人的 PR</span></button>
  </div>'''

PRT = """## 這個 PR 做了什麼
(一兩句話)

## 為什麼
(背景或對應的 Issue,例如 Closes #12)

## 怎麼確認
(測試方式、截圖)

## 想請你特別看
(例如:第 40 行的邊界條件是否合理)"""

SC = steps(
  step(1, "把 PR 縮小",
       "審查品質和 PR 大小成反比。一個 PR 只做一件事,審查者才有力氣看仔細。",
       ops(["一個 PR 解一個問題。順便重構、順便改格式,請另開 PR。",
            "改動超過幾百行,考慮拆成幾個依序合併的小 PR。",
            "拆不開時,在說明裡寫「建議閱讀順序」。"]),
       tip("好用的自問:「審查者能在 15 分鐘內讀完並理解嗎?」")),
  step(2, "送審之前先自己審一遍",
       "多數低級問題,作者自己看 Files changed 就能發現。這能大幅減少來回次數。",
       ops(["開 PR 後先點 <b>Files changed</b>,像審查者一樣從頭看。",
            "找:誤加的檔案、遺留的除錯輸出、註解掉的程式碼、密碼或 token。",
            "在你覺得不直覺的地方,自己先留一則註解說明為什麼。"]),
       warn("發現密碼或 token 被 commit 進去,請看第 10 篇,不要只是刪掉再 push。", "重要")),
  step(3, "寫一份讓審查者好上手的說明",
       "說明是審查者的導讀。沒寫清楚,他只能自己猜你的意圖。",
       cmd(PRT, cap="PR 說明範本(團隊可存成 PR template)"),
       ops(["還沒做完就先開 <b>Draft pull request</b>,草稿不會被當成可以合併。",
            "準備好了,在 PR 頁面按 <b>Ready for review</b>。"]),
       see("PR 頁面狀態從灰色的 Draft 變成 Open,審查者會收到通知。")),
  step(4, "收到意見:回覆、修改、標記解決",
       "每一則意見都需要一個回應。同意就改,不同意就禮貌地說明理由。",
       ops(["對方用了 suggestion:在該則留言按 <b>Commit suggestion</b> 一鍵採用。",
            "需要自己改:在同一個分支修改、commit、<code>git push</code>,PR 會自動更新。",
            "處理完那則討論,按 <b>Resolve conversation</b>;不同意就留言說明,讓對方決定是否解決。"]),
       cmd('git add .\ngit commit -m "依 review 調整命名"\ngit push'),
       see("新 commit 出現在 PR 時間軸,被處理的討論折疊成「Resolved」。")),
  step(5, "重新請求審查",
       "你改完了,但審查者不知道。主動通知他。",
       ops(["在 PR 右側 <b>Reviewers</b> 旁,點對方名字旁的重新整理圖示(Re-request review)。",
            "或留言一句「已更新,麻煩再看一下」,並點名 <code>@對方</code>。"]),
       see("審查者再次收到通知,審查狀態回到等待中。")),
  step(6, "合併前最後確認",
       "按 Merge 之前,把清單走一遍。",
       ops(["所有討論都已 Resolve,Checks 是綠勾。",
            "沒有衝突;有的話先回到第 3 篇的方式在本機解決。",
            "符合規則要求的核准數(有 Code Owner 時,包含他的核准)。",
            "合併後,若 PR 頁有 <b>Delete branch</b> 就按下去清掉。"]),
       see("Merge 按鈕可點(綠色)。被規則擋住時,按鈕灰掉,並列出還缺什麼。"))
)

SO = steps(
  step(1, "先讀說明和 Checks,再看程式碼",
       "知道作者想解決什麼,才能判斷做法對不對。Checks 紅叉時,先請作者處理,不必急著逐行看。",
       ops(["讀標題、說明與連結的 Issue。",
            "往下看 <b>Checks</b>:綠勾通過、紅叉失敗。",
            "想不通目的時,先留言問,而不是自己猜。"])),
  step(2, "按好的順序讀 diff",
       "從大到小:先看「做了什麼」,再看「怎麼做」。",
       ops(["先看測試檔案:它們說明了作者想保證的行為。",
            "再看對外的介面、設定、資料結構,最後才是實作細節。",
            "看完一個檔案,在 Files changed 右上角勾 <b>Viewed</b> 做記號。"]),
       tip("心裡問這幾件事:對嗎?看得懂嗎?會不會壞掉別的地方?有測試嗎?有沒有敏感資訊?")),
  step(3, "留言要具體,而且分輕重",
       "讓作者一眼看出「哪些非改不可」。把行號、原因和建議寫在同一則留言裡。",
       table("g3b", ["類型", "怎麼寫", "範例"], [
         ["必改", "說明問題與原因", "這裡沒處理 <code>null</code>,使用者沒填時會當掉。"],
         ["建議", "加上 nit: 前綴,表示可改可不改", "nit: <code>d</code> 可以改叫 <code>days</code>,比較好讀。"],
         ["疑問", "用問句,不要預設對方錯", "這個延遲設 500ms 是有什麼考量嗎?"],
         ["稱讚", "具體說好在哪", "這個拆法很清楚,測試也好讀。"],
       ]),
       ops(["在行號旁的 <b>+</b> 留言;簡單修改用 <b>Add a suggestion</b>(±)直接寫出新內容。",
            "多則意見先用 <b>Start a review</b> / <b>Add review comment</b> 累積,最後一次送出,避免作者被一則一則通知轟炸。"])),
  step(4, "送出你的結論",
       "看完後,正式告訴作者你的結論。",
       ops(["Files changed 頁右上角按 <b>Review changes</b>,寫一段總結。",
            "三選一:<b>Comment</b>(只是留言)、<b>Approve</b>(我同意)、<b>Request changes</b>(有必改的問題),按 <b>Submit review</b>。"]),
       warn("只有真的有「必改」的問題才用 Request changes。只是偏好或 nit,用 Comment 或直接 Approve 並附註。")),
  step(5, "作者更新後,再看一次",
       "不必重讀全部,看「上次之後改了什麼」就好。",
       ops(["收到更新通知後,點 PR 的 <b>Commits</b> 或 <b>Files changed</b>,只看新的 commit。",
            "意見處理好了,幫忙或請作者按 <b>Resolve conversation</b>,並改成 <b>Approve</b>。"]),
       see("審查狀態從 <b>Changes requested</b> 變成綠色的 <b>Approved</b>。")),
  step(6, "什麼時候不該按 Approve",
       "Approve 代表你對這次改動負一份責任。",
       ops(["你<b>沒有真的看過</b>。只按 LGTM(Looks Good To Me)而沒看,比不審查更糟,因為會給人錯誤的安心。",
            "還有疑問沒獲得回答。",
            "超出你能判斷的範圍時,說出來並請更適合的人看。"]),
       see("對方會明白你看了哪些部分、哪些沒把握,而不是被一個空洞的 Approve 帶過去。"))
)

body_roles = '''<div role="tabpanel" id="panel-c" aria-labelledby="tab-c" data-panel="c">
    <div class="orient">
      <div class="panel known"><span class="k">你已經會的</span>開 PR(第 6 篇)、在同一分支再 push</div>
      <div class="panel new"><span class="k">這次要新學的</span>怎麼讓 PR 好審、怎麼回應意見、重新請求審查</div>
    </div>
    ''' + SC + '''
  </div>
  <div role="tabpanel" id="panel-o" aria-labelledby="tab-o" data-panel="o" hidden>
    <div class="orient">
      <div class="panel known"><span class="k">你已經會的</span>閱讀 Files changed、送出 Review(第 6 篇)</div>
      <div class="panel new"><span class="k">這次要新學的</span>讀 diff 的順序、留言分輕重、什麼時候不該 Approve</div>
    </div>
    ''' + SO + '''
  </div>'''

rolesec = section("roles", "選一個視角,照著步驟做",
  '<p class="sub">同一個 PR,兩個人各做各的事。可以隨時切換視角對照著看。</p>', roles, body_roles)

CODEOWNERS = """# 每一行:檔案樣式 + 負責人(@帳號 或 @組織/團隊)
# 最後一個符合的規則優先
*           @your-name
/docs/      @doc-team
*.js        @frontend-team"""

teamsec = section("team", "團隊規範:讓 review 不靠自覺也能執行",
  '<p class="sub" style="margin-bottom:16px">下面四步通常由 repo 的管理者設定。規則功能的可用範圍依方案與 repo 類型而定(私人 repo 可能需要付費方案),實際畫面以 GitHub 為準。</p>',
  steps(
    step(1, "放一份 PR 範本",
         "每個 PR 一開始就有說明的骨架,作者不用每次自己想要寫什麼。",
         ops(["在 repo 建立檔案 <code>.github/pull_request_template.md</code>,內容用步驟 3 的範本。",
              "commit 並 push 到預設分支。"]),
         see("之後有人開 PR,說明欄自動出現你的範本。")),
    step(2, "設定 CODEOWNERS",
         "指定「這些檔案由誰負責」。有人改到時,GitHub 會自動請他審查。",
         cmd(CODEOWNERS, cap="CODEOWNERS(可放在 .github/、根目錄或 docs/)"),
         ops(["把檔案放在 <code>.github/CODEOWNERS</code>、repo 根目錄或 <code>docs/CODEOWNERS</code> 其中之一(GitHub 依這個順序找第一個)。",
              "每行是「檔案樣式 + 一個或多個負責人」,最後一個符合的規則優先。"]),
         see("PR 的 Reviewers 欄自動出現對應的負責人。")),
    step(3, "建立 Ruleset 保護 main",
         "把「必須經過審查才能合併」寫成規則,而不是靠大家自覺。Ruleset 是較新的做法,同一個分支可以同時套用多組規則;舊的 Branch protection rule 仍可使用,但官方文件把 ruleset 當作替代方案。",
         ops(["在 repo 頁面進 <b>Settings</b>,左側找到 <b>Rules → Rulesets</b>。",
              "按 <b>New ruleset → New branch ruleset</b>,取個名字,例如 <code>protect-main</code>。",
              "<b>Enforcement status</b> 選 <b>Active</b>(啟用)。",
              "目標分支選預設分支(<b>Include default branch</b>)。",
              "勾選要的規則,常見四項:要求經過 PR 才能合併、設定必要的核准人數、要求 Code Owner 核准、要求狀態檢查(Checks)通過;另外建議勾禁止強制推送。",
              "按 <b>Create</b>。"]),
         see("規則集出現在 Rulesets 清單,狀態是 Active。"),
         warn("規則的確切名稱與選項順序會隨 GitHub 更新而調整,請以畫面上的字為準;設定前建議先在練習用的 repo 試一次。")),
    step(4, "驗證:開一個測試 PR",
         "規則有沒有生效,實際試一次最準。",
         ops(["開一個測試 PR,在還沒有核准時看 <b>Merge</b> 按鈕。",
              "規則生效時,按鈕被擋住,並列出還缺什麼(核准、Checks、Code Owner)。",
              "也試試直接 <code>git push origin main</code>,應該被拒絕。"]),
         see("按鈕灰色,畫面寫著需要至少一位核准;直接 push 到 main 顯示被規則拒絕。")),
  ))

togethersec = section("together", "同一個 PR,兩邊在同一個時間點各做什麼",
  '<p class="sub">點選下面的階段,看作者與審查者分別該做什麼。</p>\n'
  '<div class="stages" id="stages" role="group" aria-label="Review 的階段"></div>\n'
  '<div class="two">\n<div class="panel"><h3><span class="role c">作者</span><span id="c-h"></span></h3><ul id="c-list"></ul></div>\n'
  '<div class="panel"><h3><span class="role o">審查者</span><span id="o-h"></span></h3><ul id="o-list"></ul></div>\n</div>\n'
  '<div class="stage-nav"><button type="button" class="ghost" id="prevStage">← 上一階段</button><button type="button" class="ghost" id="nextStage">下一階段 →</button></div>')

STAGES = [
  dict(badge="Ready", tone="ok", label="送審",
       c=dict(h="按下 Ready for review", items=["確認 Files changed 自己看過、說明寫清楚。", "Checks 紅叉先自己處理,不要讓審查者替你除錯。"]),
       o=dict(h="收到審查請求", items=["讀說明與 Checks。", "判斷範圍:能審就審,超出能力就說出來。"])),
  dict(badge="Review", tone="ok", label="審查中",
       c=dict(h="等待意見", items=["等待期間不要再塞新功能進同一個 PR。", "收到問題盡快回,不確定就問。"]),
       o=dict(h="逐檔閱讀並留言", items=["先看測試、再看介面、最後看實作。", "累積成一次 review 再送出,分清必改與建議。"])),
  dict(badge="Changes requested", tone="warn", label="要求修改",
       c=dict(h="回去修改", items=["同一分支修改、commit、push。", "每則意見都回應,處理完 Resolve,最後重新請求審查。"]),
       o=dict(h="等待更新", items=["不需要做什麼,等作者更新。", "收到通知後只看新的 commit。"])),
  dict(badge="Approved", tone="done", label="通過並合併",
       c=dict(h="確認規則放行", items=["核准數、Checks、Code Owner 都滿足,Merge 按鈕才會亮。", "合併後清理分支,並在 PR 留一句謝謝。"]),
       o=dict(h="Approve", items=["確認自己真的看過再按 Approve。", "有權限的人按 Merge;選合併方式見第 6 篇。"]))
]

gotchas = section("gotchas", "常見卡關",
  details("Merge 按鈕是灰的,不知道缺什麼",
          "<p>往下捲到 PR 頁最底的合併區塊,GitHub 會列出每個還沒滿足的條件:需要幾個核准、哪個 Check 沒過、哪位 Code Owner 還沒審、還有未解決的討論。逐項處理即可。</p>"),
  details("審查者很久沒回",
          "<p>先確認是否真的被請求了(<b>Reviewers</b> 欄有沒有他)。隔一兩天留言禮貌提醒,或請團隊裡另一位審查者;不要自己繞過規則。</p>"),
  details("意見互相衝突,不知道聽誰的",
          "<p>把兩種意見和你的取捨寫在留言裡,點名雙方,請他們在 PR 上直接討論。團隊有決策慣例就照做。」</p>".replace("」","")),
  details("審查者說我的 PR 太大了",
          "<p>這是最常見也最合理的意見。把 PR 拆成幾個依序合併的小 PR,每個只做一件事。拆開之後,review 的速度與品質都會上升。</p>"),
  details("我是 repo 擁有者,可以略過規則嗎",
          "<p>管理者通常能繞過規則(可在規則集裡設定誰能 bypass),但最好養成「自己也走流程」的習慣。很多團隊會把管理者也納入規則。</p>"))

SIM = {
  "m1": "<b>不建議。</b>Request changes 是「必改才能合併」。這只是命名偏好,會讓作者覺得被卡住。",
  "m2": "<b>正確!</b>用 Comment(或 Approve 並附註)搭配 <code>nit:</code> 前綴,說明這是可改可不改的小建議,並簡單說原因。",
  "m3": "<b>不建議。</b>沒說任何話的 Approve 看不出你看過什麼。至少留一則簡短的留言,說明你確認了哪些部分。"
}
QUIZ = quiz_cfg([
  ("審查者看到一個只是偏好的命名問題,最好怎麼處理?", ["Request changes,要求一定要改", "用 Comment 並加 nit: 前綴,說明可改可不改", "直接關閉 PR"], 1,
   "分清必改與建議,才不會讓作者無謂地被卡住。"),
  ("PR 規則要求「Code Owner 核准」是什麼意思?", ["所有人都必須核准", "被改動的檔案如果有指定負責人,要由他核准才能合併", "只有作者可以合併"], 1,
   "CODEOWNERS 指定檔案負責人;規則開啟後,他的核准是放行條件之一。"),
  ("作者依意見修改後,應該?", ["重新開一個新的 PR", "在同一個分支 push,PR 會自動更新,並重新請求審查", "刪掉舊分支"], 1,
   "PR 追蹤的是分支,不需要重開。"),
  ("Merge 按鈕被灰掉,最好的第一步是?", ["改用 git push 直接推 main", "往下看合併區塊列出的未滿足條件", "找管理者關掉規則"], 1,
   "GitHub 會明確列出缺少的核准、Checks 或 Code Owner。"),
  ("什麼時候不該按 Approve?", ["PR 太長", "你沒有真的看過,或還有疑問沒解答", "作者是新手"], 1,
   "Approve 代表你負了一份責任,沒看就按比不審查更糟。"),
])

practice = section("practice", "動手演練:確認你真的懂了",
  '<p class="sub" style="margin-bottom:18px">先選答案再看原因。重點是練習怎麼把意見說得清楚又友善。</p>',
  sim('<span class="role o">審查者</span> ', "情境:你發現一個變數取名不夠好,但不影響功能", "你想留下意見,該怎麼做?",
      [("m1", "選 Request changes,要求一定要改"), ("m2", "用 Comment,加 <code>nit:</code> 說明可改可不改"), ("m3", "什麼都不說,直接 Approve")]),
  QUIZ_HTML,
  checks(['<span class="role c">作者</span>我的 PR 只做一件事,而且夠小。',
          '<span class="role c">作者</span>送審前我自己看過一遍 Files changed。',
          '<span class="role c">作者</span>每則意見我都回應過,改完會重新請求審查。',
          '<span class="role c">作者</span>說明寫了做什麼、為什麼、怎麼確認。',
          '<span class="role o">審查者</span>我先讀說明與 Checks,再看程式碼。',
          '<span class="role o">審查者</span>我的意見具體,而且分清必改與建議。',
          '<span class="role o">審查者</span>只有真的看過才 Approve。',
          '團隊已用規則集保護 main,並設定 CODEOWNERS 與 PR 範本。']),
  resources([
    ("https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/reviewing-proposed-changes-in-a-pull-request", "審查 PR 的修改", "Reviewing proposed changes in a pull request"),
    ("https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository", "建立 Ruleset", "Creating rulesets for a repository"),
    ("https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches", "關於受保護分支", "About protected branches"),
    ("https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners", "關於 Code Owners", "About code owners"),
  ]))

SPEC = dict(
  file="github-review-guide.html",
  title="Code Review 與團隊規範:讓合併進 main 的東西更可靠",
  eyebrow="第 7 篇 · Code Review(進階選讀)",
  h1="小而專一的 PR 加具體友善的意見,review 才有效",
  sub="這是第 6 篇 Pull Request 的延伸。同一個 PR 分兩個視角講:「被審查的人(作者)」和「審查別人的人(審查者)」,最後再說團隊怎麼用規則集、CODEOWNERS 與 PR 範本把流程固定下來。",
  tldr="作者:<strong>PR 要小、先自審、說明寫清楚、每則意見都回應</strong>。審查者:<strong>先讀說明與 Checks、按順序看 diff、意見分必改與建議</strong>。團隊:用 Ruleset 與 CODEOWNERS,讓審查變成規則而不是自覺。",
  toc=[("what", "Review 是什麼"), ("map", "全貌圖"), ("roles", "兩種視角的步驟"), ("team", "團隊規範"), ("together", "兩邊同步看"), ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, mapsec, rolesec, teamsec, togethersec, gotchas, practice]),
  config=dict(fill={}, sim=SIM, quiz=QUIZ, stages=STAGES),
  prev=("github-pr-guide.html", "Pull Request"),
  next=("github-undo-guide.html", "還原與救援"),
)
