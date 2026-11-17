from h import *

SVG = '''<svg viewBox="0 0 900 250" role="img" aria-label="Git 的四個位置與還原指令:工作資料夾、暫存區、本機歷史、GitHub,以及 restore、restore --staged、reset、revert 各自作用的位置">
      <defs>
        <marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#87867F"/></marker>
        <marker id="ac" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#D97757"/></marker>
        <style>.m{font:12px ui-monospace,Menlo,monospace}.s{font:12px system-ui,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif}.nn{font:600 12px ui-monospace,Menlo,monospace}</style>
      </defs>
      <rect width="900" height="250" fill="#FFFFFF"/>
      <rect x="20" y="40" width="170" height="80" rx="10" fill="#F0EEE6" stroke="#3D3D3A" stroke-width="1.5"/>
      <text x="105" y="76" text-anchor="middle" class="s" fill="#141413">工作資料夾</text><text x="105" y="96" text-anchor="middle" class="s" fill="#3D3D3A">你正在改的檔案</text>
      <rect x="250" y="40" width="170" height="80" rx="10" fill="#F0EEE6" stroke="#3D3D3A" stroke-width="1.5"/>
      <text x="335" y="76" text-anchor="middle" class="s" fill="#141413">暫存區</text><text x="335" y="96" text-anchor="middle" class="s" fill="#3D3D3A">已 add 的內容</text>
      <rect x="480" y="40" width="170" height="80" rx="10" fill="#F0EEE6" stroke="#3D3D3A" stroke-width="1.5"/>
      <text x="565" y="76" text-anchor="middle" class="s" fill="#141413">本機歷史</text><text x="565" y="96" text-anchor="middle" class="s" fill="#3D3D3A">已 commit 的存檔點</text>
      <rect x="710" y="40" width="170" height="80" rx="10" fill="#E3DACC" stroke="#3D3D3A" stroke-width="2"/>
      <text x="795" y="76" text-anchor="middle" class="s" fill="#141413">GitHub</text><text x="795" y="96" text-anchor="middle" class="s" fill="#3D3D3A">已 push,別人看得到</text>
      <path d="M335,44 C335,0 105,0 105,36" fill="none" stroke="#D97757" stroke-width="2" marker-end="url(#ac)"/>
      <circle cx="220" cy="12" r="11" fill="#D97757"/><text x="220" y="16.5" text-anchor="middle" class="nn" fill="#fff">1</text>
      <path d="M565,44 C565,0 335,0 335,36" fill="none" stroke="#D97757" stroke-width="2" marker-end="url(#ac)"/>
      <circle cx="450" cy="12" r="11" fill="#D97757"/><text x="450" y="16.5" text-anchor="middle" class="nn" fill="#fff">2</text>
      <path d="M565,124 C565,175 335,175 335,124" fill="none" stroke="#B85C3E" stroke-width="2" marker-end="url(#ac)"/>
      <circle cx="450" cy="160" r="11" fill="#B85C3E"/><text x="450" y="164.5" text-anchor="middle" class="nn" fill="#fff">3</text>
      <path d="M795,124 C795,205 565,205 565,124" fill="none" stroke="#788C5D" stroke-width="2" marker-end="url(#ag)"/>
      <circle cx="680" cy="190" r="11" fill="#788C5D"/><text x="680" y="194.5" text-anchor="middle" class="nn" fill="#fff">4</text>
      <text x="40" y="150" class="m" fill="#3D3D3A">① restore  ② restore --staged</text>
      <text x="40" y="172" class="m" fill="#3D3D3A">③ reset(動歷史,只用在還沒 push 的)</text>
      <text x="40" y="194" class="m" fill="#4B5C39">④ revert(新增一個「反向 commit」,已 push 也安全)</text>
    </svg>'''

what = section("what", "多數錯誤都能救,關鍵是先判斷「走到哪一步了」",
  '<div class="panel"><h3>用「寫文章」來想</h3>'
  '<p>你有一份稿子:改到一半的草稿(工作資料夾)、挑好要交的段落(暫存區)、已經存檔的版本(本機歷史)、已經寄給別人的版本(GitHub)。想「收回」一個錯誤,要看它現在<b>在哪一層</b>:越往右,動它的影響越大。</p>'
  '<p style="margin-bottom:0">原則只有一句:<b>還沒 push 的,可以改寫歷史;已經 push 的,用新增反向 commit 的方式收回。</b></p></div>',
  '<h3 style="margin-top:26px">六個還原指令一覽</h3>',
  table("g3", ["指令", "作用", "安全程度"], [
    ["<code>git restore 檔案</code>", "丟掉工作資料夾裡尚未 add 的修改,檔案回到上次 commit 的樣子。", "<b>不可逆</b>:修改不會留在任何地方"],
    ["<code>git restore --staged 檔案</code>", "把檔案從暫存區拿回來,修改仍保留在工作資料夾。", "安全"],
    ["<code>git commit --amend</code>", "修改<b>最近一次</b> commit 的訊息或內容。", "只用在還沒 push 的 commit"],
    ["<code>git revert 代號</code>", "新增一個 commit,內容與指定的 commit 相反。", "<b>安全</b>:不改歷史,已 push 也可以"],
    ["<code>git reset --soft / --mixed / --hard 代號</code>", "把目前分支移回指定的 commit。三種差別在是否保留修改。", "--hard 會丟掉修改;已 push 不要用"],
    ["<code>git reflog</code>", "顯示 HEAD 的移動紀錄,找回「消失」的 commit。", "安全(只讀)"],
  ]))

mapsec = section("map", "全貌:每個指令作用在哪一層",
  '<p class="sub" style="margin-bottom:16px">看圖選指令:你的錯誤在哪一層,就用作用在那一層的指令。</p>',
  canvas(SVG, [
    ("1", "<b>restore</b>:工作資料夾回到暫存區(或上次 commit)的樣子。"),
    ("2", "<b>restore --staged</b>:從暫存區退回工作資料夾,修改保留。"),
    ("3", "<b>reset</b>:本機歷史往回退。只用在還沒 push 的。"),
    ("4", "<b>revert</b>:新增反向 commit,不改歷史。已 push 的用它。"),
  ]))

decidesec = section("decide", "我現在的狀況是…",
  '<p class="sub" style="margin-bottom:14px">選一個最接近你的狀況,看建議的指令、風險與原因。每個指令都有 Copy 按鈕。</p>'
  '<div class="panel"><div class="sim-buttons" id="decideBtns" role="group" aria-label="選擇你的狀況"></div>'
  '<div class="sim-result dec-out" id="decideOut" aria-live="polite">選一個狀況,看看該怎麼做。</div></div>')

DECIDE = [
  dict(label="改了檔案,還沒 add,想丟掉這些修改", risk="高", cmd="git restore 檔名",
       why="修改會被直接丟掉,<b>無法復原</b>。執行前先 <code>git diff 檔名</code> 確認真的不要了;不確定就先 <code>git stash</code> 暫存起來。"),
  dict(label="已經 add,但想拿回來、不要放進這次 commit", risk="低", cmd="git restore --staged 檔名",
       why="檔案只是離開暫存區,修改內容還在工作資料夾裡,什麼都沒有丟。"),
  dict(label="剛 commit,訊息寫錯了(還沒 push)", risk="低", cmd='git commit --amend -m "正確的訊息"',
       why="會取代最近一次 commit。<b>只能用在還沒 push 的 commit</b>,因為它會改寫歷史。"),
  dict(label="剛 commit,漏加了一個檔案(還沒 push)", risk="低", cmd="git add 漏掉的檔案\ngit commit --amend --no-edit",
       why="把漏掉的檔案併進上一個 commit,訊息不變。同樣只用在還沒 push 的 commit。"),
  dict(label="commit 了,還沒 push,想退回去重做(保留修改)", risk="中", cmd="git reset --soft HEAD~1",
       why="把最近一次 commit 拆掉,內容留在暫存區。想連暫存也拿掉、只留修改在工作資料夾,改用 <code>--mixed</code>(預設)。"),
  dict(label="commit 了,還沒 push,想整個丟掉", risk="高", cmd="git reset --hard HEAD~1",
       why="<b>最近一次 commit 與所有修改都會消失</b>。先 <code>git status</code> 確認沒有其他想保留的未存修改;萬一後悔,見最下面的 reflog。"),
  dict(label="已經 push 了,想收回那個 commit", risk="低", cmd="git revert 代號\ngit push",
       why="新增一個反向 commit,不改歷史,別人 pull 之後也不會出問題。<b>已 push 的一律用 revert</b>,不要 reset 再強推。"),
  dict(label="reset --hard 之後後悔了,想找回 commit", risk="低", cmd="git reflog\ngit reset --hard 代號",
       why="reflog 會列出 HEAD 走過的每一步,找出「消失」之前的代號,再 reset 回去。reflog 只存在你的電腦,而且通常只保留一段時間。"),
]

S = steps(
  step(1, "動手前:先看清楚現況",
       "還原的第一步永遠是看狀態,不是下指令。你要知道錯誤在哪一層。",
       cmd("git status\ngit log --oneline -n 5\ngit diff"),
       see("<code>status</code> 告訴你哪些檔案已修改或已 add;<code>log</code> 看最近的 commit;<code>diff</code> 看未 add 的內容。"),
       tip("不確定時,先建一個備份分支:<code>git branch backup</code>。出了狀況還能回來,而且完全不影響目前工作。")),
  step(2, "丟掉未 add 的修改:restore",
       "改壞了,想回到上次 commit 的樣子。",
       cmd("git restore notes.txt\ngit status"),
       see("<code>notes.txt</code> 回到上次 commit 的內容,不再列在 <code>Changes not staged</code>。"),
       warn("這個動作<b>不可逆</b>:被丟掉的修改沒有任何地方可以找回。不確定就先 <code>git stash</code>。", "危險")),
  step(3, "取消暫存:restore --staged",
       "add 錯檔案時用。修改留在工作資料夾,只是不放進這次 commit。",
       cmd("git add secret.txt\ngit restore --staged secret.txt\ngit status"),
       see("<code>secret.txt</code> 從 <code>Changes to be committed</code> 移到 <code>Untracked files</code> 或 <code>Changes not staged</code>。")),
  step(4, "改最近一次 commit:amend",
       "訊息打錯、少加一個檔案,都可以修最近一次 commit。",
       cmd('git commit --amend -m "新增 notes.txt 並補上說明"'),
       see("<code>git log --oneline</code> 最上面那筆的代號變了(因為它是一個新的 commit),舊的那筆被取代。"),
       warn("amend 會改寫歷史。<b>已經 push 的 commit 不要 amend</b>,否則和別人的歷史對不上。", "只用在還沒 push")),
  step(5, "已經 push:revert",
       "歷史已經被別人看到了,就不要改歷史。revert 另外再做一個「反向」的 commit,把錯誤抵銷掉。",
       cmd("git log --oneline -n 3\n# 假設要收回的 commit 代號是 a1b2c3d\ngit revert a1b2c3d\ngit push"),
       see("出現一個新的 commit,訊息是 <code>Revert \"…\"</code>;檔案內容回到那個 commit 之前的樣子。若 revert 時出現衝突,和第 3 篇的做法一樣解決後 <code>git revert --continue</code>。")),
  step(6, "還沒 push:reset 三種模式",
       "把目前分支移回較早的 commit。三種模式差別只在「對暫存區和工作資料夾怎麼處理」。",
       table("g3", ["模式", "暫存區", "工作資料夾"], [
         ["<code>--soft</code>", "保留(內容仍是已 add)", "保留"],
         ["<code>--mixed</code>(預設)", "清空", "保留(修改仍在,只是回到未 add)"],
         ["<code>--hard</code>", "清空", "<b>全部丟掉</b>"],
       ]),
       cmd("git reset --soft HEAD~1    # 拆掉最後一個 commit,內容留在暫存區\ngit reset HEAD~1           # 預設 mixed:內容留在工作資料夾\ngit reset --hard HEAD~1    # 全部丟掉(小心)"),
       see("<code>HEAD~1</code> 的意思是「往前一個 commit」。<code>git log --oneline</code> 少了最後一筆。")),
  step(7, "救回「消失」的 commit:reflog",
       "reset --hard、刪錯分支之後,commit 其實還在,只是沒有名字指到它。reflog 記下了 HEAD 的每一次移動。",
       cmd("git reflog\n# 找到出事之前的那一行,例如 e5f6a7b HEAD@{2}\ngit reset --hard e5f6a7b"),
       see("reflog 每一行有代號、動作(commit、reset、checkout…)與說明。回到那個代號,你的 commit 又回來了。"),
       tip("reflog 只存在你的電腦,而且過一段時間(預設數十天)會被清理。出事後越早處理越好。"))
)

gotchas = section("gotchas", "常見卡關",
  details("我想改很久以前的某個 commit",
          "<p>這需要 interactive rebase,風險比較高,而且只適用於還沒 push 的歷史。新手階段建議用 <code>git revert</code> 另外新增一個修正的 commit,更安全。</p>"),
  details("push 被拒絕,是不是該 <code>--force</code>?",
          "<p>幾乎都不要。被拒絕通常是因為雲端有你沒有的 commit,<code>--force</code> 會洗掉別人的工作。先 <code>git pull</code>,見第 4 篇。真的必須強制時用 <code>--force-with-lease</code>,並先和團隊確認。</p>"),
  details("我把密碼 commit 上去了,revert 就可以嗎?",
          "<p><b>不行。</b>revert 只是新增一個反向 commit,舊的 commit 與密碼仍在歷史裡。請當作已外洩:先到服務端更換金鑰,再看第 10 篇處理歷史。</p>"),
  details("<code>git reset</code> 之後工作資料夾的檔案不見了",
          "<p>如果用了 <code>--hard</code>,未 commit 的修改已經丟了;已 commit 的內容可以用 <code>git reflog</code> 找回。下次用 <code>--hard</code> 前先 <code>git status</code>,或先 <code>git branch backup</code>。</p>"),
  details("我不小心在 main 上 commit,想改放到新分支",
          "<p>先用 <code>git branch 新分支</code> 把 commit 存到新分支,再把 main 退回去:</p>" + cmd("git branch fix-typo\ngit reset --hard origin/main\ngit switch fix-typo") +
          "<p>前提是這些 commit 還沒 push,而且 main 上沒有其他想保留的未存修改。</p>"))

SIM = {
  "u1": "<b>用 revert。</b>已 push 的歷史別人可能已經拿到,不能改寫。<code>git revert</code> 新增反向 commit,最安全。",
  "u2": "<b>用 amend。</b>還沒 push,可以直接修最近一次 commit:<code>git commit --amend -m \"新訊息\"</code>。",
  "u3": "<b>用 restore --staged。</b>只是離開暫存區,修改內容還在工作資料夾,不會丟東西。",
  "u4": "<b>用 reflog 找回。</b>commit 沒有真的消失,<code>git reflog</code> 找到代號,再 <code>git reset --hard 代號</code>。"
}
QUIZ = quiz_cfg([
  ("已經 push 的 commit 想收回,應該用?", ["git reset --hard 再 push --force", "git revert", "刪掉 repo"], 1,
   "revert 不改歷史,別人 pull 之後也不會出問題。"),
  ("<code>git restore 檔名</code> 的特點是?", ["可以隨時復原", "丟掉未 add 的修改,而且不可逆", "會刪除整個檔案"], 1,
   "被丟掉的修改沒有任何地方可以找回,執行前要確定。"),
  ("<code>git reset --mixed</code>(預設)對修改的影響是?", ["全部丟掉", "修改保留在工作資料夾,暫存區清空", "修改保留在暫存區"], 1,
   "mixed 回到未 add 的狀態,修改仍在。"),
  ("<code>reset --hard</code> 之後 commit 消失了,怎麼辦?", ["沒救了", "用 git reflog 找出代號,再 reset 回去", "重新 clone"], 1,
   "commit 還在,只是沒有名字指到它。reflog 記錄了 HEAD 的移動。"),
  ("不確定哪個還原指令安全時,最好先做什麼?", ["直接用 --hard 試試", "建立一個 backup 分支再操作", "刪掉 .git"], 1,
   "建立分支只是多一個名字,不影響任何東西,出事還能回來。"),
])

practice = section("practice", "動手演練:確認你真的懂了",
  '<p class="sub" style="margin-bottom:18px">先選答案再看原因。重點是培養「先判斷在哪一層」的直覺。</p>',
  sim("", "情境:選一個你遇到的狀況", "你想知道用哪個還原指令?",
      [("u1", "commit 已經 push 了,想收回"), ("u2", "剛 commit,訊息寫錯(還沒 push)"), ("u3", "add 錯了一個檔案"), ("u4", "<code>reset --hard</code> 之後後悔了")]),
  QUIZ_HTML,
  checks(["還原之前我會先看 <code>git status</code> 與 <code>git log</code>。",
          "我知道 <code>restore</code> 丟掉的修改無法復原,所以用之前先 <code>git diff</code>。",
          "我只對還沒 push 的 commit 使用 amend 與 reset。",
          "已 push 的 commit 我會用 <code>git revert</code>。",
          "我知道 <code>reset --hard</code> 前先 <code>git status</code>,或先建 backup 分支。",
          "我知道 commit 消失時可以用 <code>git reflog</code> 找回。",
          "我知道 revert 不能讓已外洩的密碼消失。"]),
  resources([
    ("https://docs.github.com/en/get-started/using-git/about-git", "關於 Git", "About Git"),
    ("https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/reverting-a-pull-request", "從網頁還原一個 PR", "Reverting a pull request"),
    ("https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository", "移除 repo 中的敏感資料", "Removing sensitive data from a repository"),
  ]))

SPEC = dict(
  file="github-undo-guide.html",
  title="還原與救援:先判斷狀況,再選指令",
  eyebrow="第 8 篇 · 還原與救援",
  h1="先判斷狀況,再選指令:多數錯誤都能救",
  sub="改錯、add 錯、commit 錯、push 錯,各有不同的收回方式。這一篇先教你判斷錯誤走到哪一層,再配上對應的指令,最後教你用 <code>reflog</code> 救回「消失」的 commit。",
  tldr="<strong>還沒 push 可以改寫歷史</strong>(restore / amend / reset);<strong>已經 push 就用 revert</strong> 新增反向 commit。用 <code>--hard</code> 之前先看 <code>git status</code>;真的搞丟了,<code>git reflog</code> 通常救得回來。",
  toc=[("what", "為什麼要先判斷"), ("map", "全貌圖"), ("decide", "我現在的狀況"), ("steps", "七個步驟"), ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, mapsec, decidesec, section("steps", "照著做:七個步驟", S), gotchas, practice]),
  config=dict(fill={}, sim=SIM, quiz=QUIZ, decide=DECIDE),
  prev=("github-review-guide.html", "Code Review 與團隊規範"),
  next=("github-release-guide.html", "Release 與版本號"),
)
