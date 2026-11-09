from h import *

SVG = '''<svg viewBox="0 0 980 230" role="img" aria-label="檔案的四種狀態:新檔案先比對 .gitignore,符合的被忽略,不符合的是未追蹤,add 後變已暫存,commit 後變已追蹤">
      <defs>
        <marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#87867F"/></marker>
        <style>.m{font:12px ui-monospace,Menlo,monospace}.s{font:12px system-ui,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif}.nn{font:600 12px ui-monospace,Menlo,monospace}</style>
      </defs>
      <rect width="980" height="230" fill="#FFFFFF"/>
      <rect x="20" y="110" width="130" height="64" rx="10" fill="#F0EEE6" stroke="#3D3D3A" stroke-width="1.5"/>
      <text x="85" y="147" text-anchor="middle" class="s" fill="#141413">新檔案</text>
      <rect x="195" y="110" width="170" height="64" rx="10" fill="#E3DACC" stroke="#3D3D3A" stroke-width="2"/>
      <text x="280" y="138" text-anchor="middle" class="m" fill="#141413">.gitignore</text>
      <text x="280" y="158" text-anchor="middle" class="s" fill="#3D3D3A">名字符合規則嗎?</text>
      <rect x="415" y="18" width="150" height="64" rx="10" fill="#F0EEE6" stroke="#B04A3F" stroke-width="1.5"/>
      <text x="490" y="46" text-anchor="middle" class="s" fill="#141413">被忽略</text>
      <text x="490" y="66" text-anchor="middle" class="s" fill="#3D3D3A">status 不會列出</text>
      <rect x="415" y="110" width="150" height="64" rx="10" fill="#F0EEE6" stroke="#3D3D3A" stroke-width="1.5"/>
      <text x="490" y="138" text-anchor="middle" class="s" fill="#141413">未追蹤</text>
      <text x="490" y="158" text-anchor="middle" class="s" fill="#3D3D3A">status 顯示紅色</text>
      <rect x="615" y="110" width="150" height="64" rx="10" fill="#F0EEE6" stroke="#3D3D3A" stroke-width="1.5"/>
      <text x="690" y="138" text-anchor="middle" class="s" fill="#141413">已暫存</text>
      <text x="690" y="158" text-anchor="middle" class="s" fill="#3D3D3A">status 顯示綠色</text>
      <rect x="815" y="110" width="150" height="64" rx="10" fill="#E3DACC" stroke="#3D3D3A" stroke-width="2"/>
      <text x="890" y="138" text-anchor="middle" class="s" fill="#141413">已追蹤</text>
      <text x="890" y="158" text-anchor="middle" class="s" fill="#3D3D3A">寫進歷史</text>
      <line x1="153" y1="142" x2="191" y2="142" stroke="#87867F" stroke-width="1.5" marker-end="url(#ag)"/>
      <circle cx="172" cy="124" r="11" fill="#D97757"/><text x="172" y="128.5" text-anchor="middle" class="nn" fill="#fff">1</text>
      <path d="M280,106 L280,50 L411,50" fill="none" stroke="#B04A3F" stroke-width="1.5" marker-end="url(#ag)"/>
      <text x="292" y="44" class="s" fill="#B04A3F">符合</text>
      <line x1="368" y1="142" x2="411" y2="142" stroke="#87867F" stroke-width="1.5" marker-end="url(#ag)"/>
      <text x="372" y="132" class="s" fill="#3D3D3A">不符合</text>
      <line x1="568" y1="142" x2="611" y2="142" stroke="#87867F" stroke-width="1.5" marker-end="url(#ag)"/>
      <circle cx="590" cy="124" r="11" fill="#D97757"/><text x="590" y="128.5" text-anchor="middle" class="nn" fill="#fff">2</text>
      <text x="576" y="196" class="m" fill="#3D3D3A">add</text>
      <line x1="768" y1="142" x2="811" y2="142" stroke="#87867F" stroke-width="1.5" marker-end="url(#ag)"/>
      <circle cx="790" cy="124" r="11" fill="#D97757"/><text x="790" y="128.5" text-anchor="middle" class="nn" fill="#fff">3</text>
      <text x="768" y="196" class="m" fill="#3D3D3A">commit</text>
    </svg>'''

GITIGNORE = """# 密碼與環境設定
.env
# 記錄檔
*.log
# 套件資料夾
node_modules/
# 系統暫存檔
.DS_Store
Thumbs.db"""

what = section("what", "不是每個檔案都該進 repo",
  '<div class="panel"><h3>用「搬家打包」來想</h3>'
  '<p>你搬家時會挑東西裝箱,不會把垃圾、暫時用的雜物、和裝滿密碼的筆記本一起帶走。<code>.gitignore</code> 就是一張「這些不要打包」的清單,git 看到符合的檔案就當作它不存在。</p>'
  '<p style="margin-bottom:0">越早寫越好:一旦 commit 過,檔案就進了歷史,事後補規則不會讓它消失(見步驟 5)。</p></div>',
  '<h3 style="margin-top:26px">最常見的六類「不該進 repo」</h3>',
  table("g3", ["類型", "例子", "為什麼不該進"], [
    ["密碼與金鑰", "<code>.env</code>、<code>*.pem</code>", "一旦上傳,等於公開。這是新手最危險的錯誤(見第 10 篇)。"],
    ["套件資料夾", "<code>node_modules/</code>、<code>venv/</code>", "體積大、可由設定檔重新安裝,別人 clone 後自己裝就好。"],
    ["建置產物", "<code>dist/</code>、<code>build/</code>", "由原始碼產生,放進去只會讓每次 diff 吵雜。"],
    ["記錄與暫存檔", "<code>*.log</code>、<code>*.tmp</code>", "只對你本機有意義。"],
    ["系統檔案", "<code>.DS_Store</code>、<code>Thumbs.db</code>", "作業系統自動產生,與專案無關。"],
    ["個人編輯器設定", "<code>.idea/</code>、<code>.vscode/</code>", "多半因人而異;團隊若要共用,再刻意提交。"],
  ]))

mapsec = section("map", "全貌:檔案有四種狀態",
  '<p class="sub" style="margin-bottom:16px">新檔案出現時,git 先比對 <code>.gitignore</code>。符合的被忽略;不符合的才進入「未追蹤 → 已暫存 → 已追蹤」這條路。</p>',
  canvas(SVG, [
    ("1", "<b>比對規則</b>:新檔案先過 <code>.gitignore</code> 這一關。"),
    ("2", "<b>add</b>:未追蹤的檔案放進暫存區。"),
    ("3", "<b>commit</b>:暫存的內容寫進歷史,成為已追蹤。"),
    ("!", "<b>被忽略</b>的檔案不在這條路上,<code>git status</code> 看不到它。"),
  ]))

DIFF = ('<div class="diff" role="img" aria-label="notes.txt 的修改範例:新增第二行">'
        '<div class="diff-row"><span class="ln">1</span><span class="mark"> </span><span>我的筆記</span></div>'
        '<div class="diff-row add"><span class="ln">2</span><span class="mark">+</span><span>第二行</span></div></div>')

S = steps(
  step(1, "先製造幾個檔案,認識「未追蹤」",
       "在 git 看過它們之前,所有新檔案都是「未追蹤」。我們故意做幾個「不該進 repo」的檔案來練習。以下在你的 repo 資料夾(第 1 篇 clone 下來的那個)裡執行。",
       cmd('echo "my-secret-key" > .env\necho "debug info" > debug.log\nmkdir node_modules\necho "x" > node_modules/a.js\necho "我的筆記" > notes.txt\ngit status'),
       see("<code>Untracked files:</code> 底下列出 <code>.env</code>、<code>debug.log</code>、<code>node_modules/</code>、<code>notes.txt</code> 四項。這時如果隨手 <code>git add .</code>,密碼檔也會被加進去。")),
  step(2, "建立 .gitignore",
       "把不要的檔案寫成規則。<code>.gitignore</code> 是一個沒有副檔名的純文字檔,放在 repo 最外層,檔名開頭有一個點。",
       ops(["用任何文字編輯器新增檔案,存成 <code>.gitignore</code>(不是 <code>.gitignore.txt</code>)。",
            "貼上下面的內容並存檔。",
            "回到終端機再看一次 <code>git status</code>。"]),
       cmd(GITIGNORE, cap=".gitignore 內容"),
       cmd("git status"),
       see("未追蹤清單只剩 <code>.gitignore</code> 與 <code>notes.txt</code>。<code>.env</code>、<code>debug.log</code>、<code>node_modules/</code> 都消失了:它們被忽略了。"),
       tip("在 GitHub 建立 repo 時,可以勾 <b>Add .gitignore</b> 並選語言範本;GitHub 官方也維護一個範本集 repo(<code>github/gitignore</code>)可參考。")),
  step(3, "看懂規則寫法",
       "規則不多,記住下面這幾種就能應付大部分情況。",
       table("g2", ["寫法", "意思"], [
         ["<code>*.log</code>", "所有 <code>.log</code> 檔,不管在哪個資料夾。<code>*</code> 代表任意字元。"],
         ["<code>node_modules/</code>", "名叫這個名字的資料夾(結尾的 <code>/</code> 表示它是資料夾)。"],
         ["<code>/build</code>", "只限 repo 最外層的 <code>build</code>(開頭的 <code>/</code> 表示從根目錄算起)。"],
         ["<code>docs/*.tmp</code>", "只限 <code>docs</code> 資料夾底下的 <code>.tmp</code> 檔。"],
         ["<code>**/cache</code>", "任何深度的 <code>cache</code>。"],
         ["<code>!keep.log</code>", "例外:即使前面的規則擋住,這個仍要追蹤(<code>!</code> 代表反向)。"],
         ["<code># 註解</code>", "以 <code>#</code> 開頭的行是註解,git 會略過。"],
       ]),
       warn("反向規則 <code>!</code> 有一個限制:如果上層資料夾已經被忽略,資料夾裡的檔案就無法再用 <code>!</code> 放行。放行要連資料夾一起寫。")),
  step(4, "查「為什麼這個檔案被忽略」",
       "規則一多,你會想知道某個檔案到底是被哪一行擋住的。",
       cmd("git check-ignore -v debug.log"),
       see("輸出 <code>.gitignore:3:*.log    debug.log</code>:意思是檔案 <code>.gitignore</code> 的第 3 行規則 <code>*.log</code> 擋住了它。")),
  step(5, "檔案已經 commit 過,再寫規則「沒有用」怎麼辦",
       "<code>.gitignore</code> 只管「還沒被追蹤」的檔案。已經進了歷史的檔案,要先叫 git 停止追蹤(檔案本身不會被刪掉)。",
       cmd('git rm --cached .env\ngit commit -m "停止追蹤 .env"\n# 整個資料夾要加 -r:\n# git rm -r --cached node_modules'),
       see("<code>git rm --cached</code> 顯示 <code>rm '.env'</code>;你的資料夾裡 <code>.env</code> 仍然存在。"),
       warn("這只是「從現在起不再追蹤」。<b>它在過去的 commit 裡仍然存在。</b>如果那是真的密碼或金鑰,請當作已外洩,立刻去服務端更換,並看第 10 篇。", "重要")),
  step(6, "看改了什麼:git diff",
       "commit 之前,先看一眼「這次到底改了什麼」,是避免誤 commit 的好習慣。先讓 <code>notes.txt</code> 成為已追蹤檔案,再修改它。",
       cmd('git add .gitignore notes.txt\ngit commit -m "新增 .gitignore 與筆記"\necho "第二行" >> notes.txt\ngit diff\ngit add notes.txt\ngit diff --staged'),
       DIFF,
       see("第一個 <code>git diff</code> 顯示尚未 add 的變更;<b>綠色 +</b> 是新增、<b>紅色 −</b> 是刪除。<code>add</code> 之後要加 <code>--staged</code> 才看得到暫存區的差異。")),
  step(7, "看歷史:git log",
       "歷史是 commit 串成的清單。學會看它,你就知道專案怎麼走到現在。",
       cmd("git commit -m \"補充第二行\"\ngit log --oneline -n 5\ngit show --stat HEAD\ngit log --oneline -- notes.txt"),
       ops(["<code>git log --oneline -n 5</code>:最近 5 筆,每筆一行。",
            "<code>git show --stat HEAD</code>:最新那筆 commit 改了哪些檔案。",
            "<code>git log --oneline -- notes.txt</code>:只看動過這個檔案的 commit。"]),
       see("每行開頭是 7 個字元的代號(commit 的名字),後面是你寫的說明。最新的在最上面。"),
       tip("<code>git log</code> 太長會進入分頁模式,按 <code>q</code> 離開。"))
)

gotchas = section("gotchas", "初學者最常卡住的四個地方",
  details("我加了規則,檔案還是出現在 <code>git status</code>",
          "<p>依序檢查三件事:</p><ol class='ops'><li>檔案是不是<b>已經被追蹤過</b>?是的話照步驟 5 先 <code>git rm --cached</code>。</li>"
          "<li>檔名是不是 <code>.gitignore.txt</code>?Windows 預設會隱藏副檔名,打開「顯示副檔名」確認。</li>"
          "<li>用 <code>git check-ignore -v 檔名</code> 看有沒有任何規則命中。沒有命中就是規則寫錯了。</li></ol>"),
  details("我想讓全部專案都忽略 <code>.DS_Store</code>,不想每個 repo 都寫",
          "<p>設一份全域忽略清單,只對你自己的電腦有效:</p>" +
          cmd('echo ".DS_Store" >> ~/.gitignore_global\ngit config --global core.excludesfile ~/.gitignore_global') +
          "<p>團隊共用的規則仍然寫在專案裡的 <code>.gitignore</code>。</p>"),
  details("<code>.env</code> 要忽略,但別人需要知道有哪些設定項目",
          "<p>慣例是另外提交一份<b>只有欄位名稱、沒有真實值</b>的範例檔 <code>.env.example</code>,並在 <code>.gitignore</code> 裡放行它:</p>" +
          cmd(".env\n!.env.example") ),
  details("空資料夾沒有出現在 <code>git status</code>",
          "<p>git 只追蹤檔案,不追蹤空資料夾。想保留空資料夾,慣例是在裡面放一個空檔案,常見取名 <code>.gitkeep</code>。</p>" +
          cmd("mkdir logs\necho \"\" > logs/.gitkeep")))

SIM = {
  "s1": "<b>要忽略。</b>套件資料夾體積大,而且可以由設定檔重新安裝。放進 <code>.gitignore</code>:<code>node_modules/</code>。",
  "s2": "<b>不要忽略。</b>README 是專案說明,正是要讓別人看到的內容。",
  "s3": "<b>要忽略,並且還要多做一件事。</b>真實的 <code>.env</code> 放進 <code>.gitignore</code>;另外提交一份只有欄位名稱的 <code>.env.example</code> 讓別人知道要設定什麼。",
  "s4": "<b>要忽略。</b>建置產物可以由原始碼重新產生,放進去只會讓 diff 變得很吵。通常寫成 <code>dist/</code> 或 <code>build/</code>。"
}
QUIZ = quiz_cfg([
  ("<code>.gitignore</code> 能讓「已經 commit 過」的檔案自動變成不追蹤嗎?", ["能,加了規則就會自動消失", "不能,要先用 <code>git rm --cached</code> 停止追蹤".replace("<code>","").replace("</code>",""), "只有重新 clone 才會生效"], 1,
   "規則只對尚未被追蹤的檔案有效。已追蹤的要先 git rm --cached,而且它仍留在過去的歷史裡。"),
  ("規則 <code>*.log</code> 的意思是?", ["只忽略名叫 log 的資料夾", "忽略所有副檔名為 .log 的檔案", "忽略所有檔案"], 1,
   "* 代表任意字元,所以 *.log 會擋住任何資料夾裡的 .log 檔。"),
  ("想查某個檔案是被 <code>.gitignore</code> 的哪一行擋住,用哪個指令?", ["git log", "git check-ignore -v 檔名", "git diff"], 1,
   "check-ignore -v 會顯示命中的檔案、行號與規則。"),
  ("<code>git diff</code>(不加參數)比較的是什麼?", ["已修改但尚未 add 的變更", "最近一次 push 的內容", "暫存區與歷史的差異"], 0,
   "沒加參數時看的是尚未 add 的變更;暫存區的差異要加 --staged。"),
])

practice = section("practice", "動手演練:確認你真的懂了",
  '<p class="sub" style="margin-bottom:18px">先選答案再看原因。重點是培養「這個檔案該不該進 repo」的直覺。</p>',
  sim("", "情境:挑出一個檔案,看看該不該忽略", "下面這些檔案,你想知道哪一個該怎麼處理?",
      [("s1", "<code>node_modules/</code>"), ("s2", "<code>README.md</code>"), ("s3", "<code>.env</code>"), ("s4", "<code>dist/</code>")]),
  QUIZ_HTML,
  checks(["我在第一次 commit 之前就建立了 <code>.gitignore</code>。",
          "我的 <code>.gitignore</code> 擋住了密碼檔、套件資料夾與系統暫存檔。",
          "我 add 之前會先看 <code>git status</code>。",
          "我 commit 之前會先用 <code>git diff</code> 看一遍改了什麼。",
          "我知道已經 commit 的檔案要用 <code>git rm --cached</code> 才會停止追蹤。",
          "我知道密碼一旦 commit 過,就要當作已外洩。"]),
  resources([
    ("https://docs.github.com/en/get-started/git-basics/ignoring-files", "忽略檔案", "Ignoring files"),
    ("https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository", "移除 repo 中的敏感資料", "Removing sensitive data from a repository"),
    ("https://docs.github.com/en/get-started/using-git/about-git", "關於 Git", "About Git"),
  ]))

SPEC = dict(
  file="github-gitignore-guide.html",
  title=".gitignore 與檢視歷史:先寫 .gitignore,再第一次 commit",
  eyebrow="第 2 篇 · .gitignore 與歷史",
  h1="先寫 .gitignore,再第一次 commit",
  sub="新手最早踩到的坑,是把 <code>node_modules</code> 或 <code>.env</code> 一起 commit 上去。這一篇教你用 <code>.gitignore</code> 擋住不該進 repo 的檔案,並用 <code>status</code>、<code>diff</code>、<code>log</code> 看清楚 repo 裡發生了什麼。",
  tldr="不想進 repo 的檔案寫進 <code>.gitignore</code>;但它只管「還沒被追蹤」的檔案。<strong>已經 commit 過的密碼,擋不回來</strong>,要當作外洩處理。commit 前養成 <code>status</code> 與 <code>diff</code> 看一遍的習慣。",
  toc=[("what", "為什麼要忽略"), ("map", "四種狀態"), ("steps", "七個步驟"), ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, mapsec, section("steps", "照著做:七個步驟", S), gotchas, practice]),
  config=dict(fill={}, sim=SIM, quiz=QUIZ),
  prev=("github-start-guide.html", "GitHub 是什麼與第一次推送"),
  next=("github-branch-guide.html", "分支、合併與衝突解決"),
)
