from h import *

def node(x, y, label, fill="#F0EEE6", stroke="#3D3D3A"):
    return ('<circle cx="%d" cy="%d" r="15" fill="%s" stroke="%s" stroke-width="1.5"/>'
            '<text x="%d" y="%d" text-anchor="middle" class="m" fill="#141413">%s</text>' % (x, y, fill, stroke, x, y + 4, label))

SVG = '''<svg viewBox="0 0 900 250" role="img" aria-label="分支與合併:main 上有 C1、C2、C3,從 C2 分出 feature 分支提交 F1、F2,最後合併回 main 成為 M">
      <defs>
        <marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#87867F"/></marker>
        <style>.m{font:12px ui-monospace,Menlo,monospace}.s{font:12px system-ui,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif}.nn{font:600 12px ui-monospace,Menlo,monospace}</style>
      </defs>
      <rect width="900" height="250" fill="#FFFFFF"/>
      <text x="20" y="28" class="m" fill="#87867F">main</text>
      <text x="20" y="196" class="m" fill="#87867F">feature</text>
      <line x1="95" y1="80" x2="215" y2="80" stroke="#87867F" stroke-width="1.5"/>
      <line x1="245" y1="80" x2="505" y2="80" stroke="#87867F" stroke-width="1.5"/>
      <line x1="535" y1="80" x2="675" y2="80" stroke="#87867F" stroke-width="1.5"/>
      <path d="M240,92 C270,170 290,170 316,170" fill="none" stroke="#D97757" stroke-width="2" marker-end="url(#ag)"/>
      <line x1="347" y1="170" x2="413" y2="170" stroke="#D97757" stroke-width="2"/>
      <path d="M446,170 C560,170 620,170 690,92" fill="none" stroke="#788C5D" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#ag)"/>
      ''' + node(80, 80, "C1") + node(230, 80, "C2") + node(520, 80, "C3") + node(690, 80, "M", "#E3DACC") + \
      node(332, 170, "F1", "#FBF1EC", "#D97757") + node(430, 170, "F2", "#FBF1EC", "#D97757") + '''
      <circle cx="262" cy="130" r="11" fill="#D97757"/><text x="262" y="134.5" text-anchor="middle" class="nn" fill="#fff">1</text>
      <circle cx="382" cy="150" r="11" fill="#D97757"/><text x="382" y="154.5" text-anchor="middle" class="nn" fill="#fff">2</text>
      <circle cx="380" cy="60" r="11" fill="#D97757"/><text x="380" y="64.5" text-anchor="middle" class="nn" fill="#fff">3</text>
      <circle cx="600" cy="140" r="11" fill="#788C5D"/><text x="600" y="144.5" text-anchor="middle" class="nn" fill="#fff">4</text>
      <text x="470" y="226" class="s" fill="#4B5C39">merge:把 feature 的成果合進 main,產生合併 commit M</text>
    </svg>'''

what = section("what", "分支讓你放心地試",
  '<div class="panel"><h3>用「草稿本」來想</h3>'
  '<p><code>main</code> 是已經定稿的正本。想試新點子,就另外開一本<b>草稿本(分支)</b>:在上面隨便改、隨便 commit,正本完全不受影響。滿意了,再把草稿<b>合併(merge)</b>回正本;不滿意,整本丟掉就好。</p>'
  '<p style="margin-bottom:0">所以:<b>一件事一個分支</b>。這也是第 6 篇 Pull Request 的基礎。</p></div>',
  '<h3 style="margin-top:26px">六個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["branch(分支)", "一條獨立的 commit 時間線。建立分支很便宜,幾乎瞬間完成。"],
    ["HEAD", "「你現在站的位置」。<code>git status</code> 第一行 <code>On branch …</code> 就是在告訴你它在哪。"],
    ["switch", "切換到另一條分支。檔案會跟著變成那條分支的樣子。"],
    ["merge(合併)", "把另一條分支的 commit 整合進目前所在的分支。"],
    ["fast-forward", "主線沒有新進度時,merge 只是把指標往前推,不產生新的合併 commit。"],
    ["conflict(衝突)", "兩條分支改了同一個地方,git 無法自己決定留誰的,需要你來選。"],
  ]))

mapsec = section("map", "全貌:分出去、做事、合回來",
  '<p class="sub" style="margin-bottom:16px">圖中每個圓是一個 commit。上方是 <code>main</code>,下方是從 C2 分出去的 <code>feature</code>。</p>',
  canvas(SVG, [
    ("1", "<b>開分支</b>:從 C2 分出一條新線。"),
    ("2", "<b>在分支上 commit</b>:F1、F2 只存在 feature 上。"),
    ("3", "<b>main 也往前走</b>:別人(或你)在 main 又加了 C3。"),
    ("4", "<b>merge</b>:feature 合進 main,產生合併 commit M。"),
  ]))

fillsec = section("fill", "先填入你的分支名稱,下面的指令會自動換成你的版本",
  fill([("branch", "分支名稱", False)]))

CONFLICT = "<<<<<<< HEAD\n標題:主線再改一次\n=======\n標題:分支版本\n>>>>>>> feature-title"

S = steps(
  step(1, "先確認你站在哪條分支",
       "動手前先看位置,是避免「改錯地方」的第一個習慣。以下在你練習用的 repo 資料夾裡執行。",
       cmd("git status\ngit branch"),
       see("<code>On branch main</code>;<code>git branch</code> 列出所有本機分支,目前所在的前面有 <code>*</code>。")),
  step(2, "建立並切換到新分支",
       "取一個看得出在做什麼的短名字,不要有空白,用 <code>-</code> 連接。",
       cmd("git switch -c {branch}\ngit branch"),
       see("<code>Switched to a new branch '{branch}'</code>;<code>git branch</code> 的 <code>*</code> 移到了新分支上。"),
       tip("<code>switch -c</code> 的 <code>c</code> 是 create:建立並切過去。只想切換既有分支時不加 <code>-c</code>。舊版 git(低於 2.23)請用 <code>git checkout -b {branch}</code>。")),
  step(3, "在分支上改檔案、commit",
       "跟平常一模一樣。差別只在:這些 commit 現在只屬於這條分支。",
       cmd('echo "新功能草稿" > feature.txt\ngit add feature.txt\ngit commit -m "新增 feature.txt"\ngit log --oneline -n 3'),
       see("log 最上面是你剛剛的 commit,後面括號裡寫著 <code>HEAD -&gt; {branch}</code>。")),
  step(4, "切回 main,看見「草稿」不見了",
       "切換分支時,資料夾裡的檔案會跟著換成那條分支的樣子。這是理解分支最直觀的一步。",
       cmd("git switch main\nls"),
       see("資料夾裡沒有 <code>feature.txt</code>(Windows 的 Git Bash 用 <code>ls</code>,PowerShell 用 <code>dir</code>)。它沒有消失,只是存在另一條分支上。再切回去就會出現。")),
  step(5, "merge:把分支合進 main",
       "合併的方向很重要:<b>你站在誰身上,就是誰接收別人的成果</b>。要把 feature 合進 main,就要先站在 main。",
       cmd("git switch main\ngit merge {branch}\ngit log --oneline -n 3"),
       see("因為 main 在分出去之後沒有新進度,出現 <code>Fast-forward</code>,<code>feature.txt</code> 出現在 main。log 裡看不到額外的合併 commit。"),
       tip("如果 main 之後也有新 commit(像全貌圖那樣),merge 會產生一個新的合併 commit,並請你確認訊息:直接存檔離開即可。")),
  step(6, "故意製造一次衝突(練習用)",
       "與其等衝突自己找上門,不如先在安全的地方遇到它一次。下面讓兩條分支改<b>同一個檔案的同一行</b>。",
       cmd('git switch main\necho "標題:主線版本" > title.txt\ngit add title.txt\ngit commit -m "main: 新增 title.txt"\ngit switch -c feature-title\necho "標題:分支版本" > title.txt\ngit add title.txt\ngit commit -m "分支: 改標題"\ngit switch main\necho "標題:主線再改一次" > title.txt\ngit add title.txt\ngit commit -m "main: 再改標題"\ngit merge feature-title'),
       see("<code>CONFLICT (content): Merge conflict in title.txt</code>,並顯示 <code>Automatic merge failed; fix conflicts and then commit the result.</code>。<code>git status</code> 會列出 <code>both modified: title.txt</code>。"),
       tip("這不是壞掉,是 git 在問你:「兩邊都改了這行,你要哪個?」")),
  step(7, "看懂標記、決定內容、完成合併",
       "git 把兩邊的內容都放進檔案,用三種標記隔開。你的工作是:留下最終要的內容,並<b>把三種標記行整行刪掉</b>。",
       cmd(CONFLICT, cap="打開 title.txt 會看到"),
       table("g2", ["標記", "意思"], [
         ["<code>&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD</code>", "從這行到 <code>=======</code> 是「你現在所在分支」(這裡是 main)的內容。"],
         ["<code>=======</code>", "分隔線。"],
         ["<code>&gt;&gt;&gt;&gt;&gt;&gt;&gt; feature-title</code>", "從分隔線到這行是「要合進來的分支」的內容。"],
       ]),
       ops(["用編輯器打開 <code>title.txt</code>,改成你要的最終內容,例如只留一行 <code>標題:合併後的版本</code>。確認沒有任何 <code>&lt;&lt;&lt;&lt;&lt;&lt;&lt;</code>、<code>=======</code>、<code>&gt;&gt;&gt;&gt;&gt;&gt;&gt;</code> 殘留。",
            "存檔後,告訴 git 這個檔案解決了,並完成合併。"]),
       cmd('git add title.txt\ngit commit -m "解決 title.txt 的衝突"\ngit log --oneline --graph -n 6'),
       see("<code>git log --graph</code> 顯示兩條線匯合成一個合併 commit。"),
       warn("標記行一定要刪乾淨。留下 <code>&lt;&lt;&lt;&lt;&lt;&lt;&lt;</code> 就 commit,等於把標記當成檔案內容提交了。")),
  step(8, "刪掉用完的分支",
       "合併完成後,草稿本可以丟了。刪除分支只是刪掉那個名字,commit 已經在 main 裡了。",
       cmd("git branch -d {branch}\ngit branch -d feature-title\ngit branch"),
       see("<code>Deleted branch {branch}</code>;<code>git branch</code> 只剩 <code>main</code>。"))
)

gotchas = section("gotchas", "初學者最常卡住的五個地方",
  details("切換分支時顯示 <code>Your local changes would be overwritten</code>",
          "<p>你有尚未 commit 的修改,而且和目標分支會衝到。二選一:</p><ol class='ops'><li>先 <code>commit</code> 把它存起來。</li><li>還不想 commit,就暫時收起來:</li></ol>" +
          cmd("git stash\ngit switch 目標分支\n# 回來之後再拿出來\ngit stash pop")),
  details("衝突解到一半,想全部放棄",
          "<p>合併還沒完成時,可以整個退回合併前的狀態,什麼都不會損失:</p>" + cmd("git merge --abort")),
  details("<code>git branch -d</code> 說 “not fully merged”",
          "<p>git 認為這條分支還有 commit 沒進到目前分支。如果你確認內容已經合併(例如在 GitHub 上用 Squash and merge,commit 被壓成新的一個,git 認不出來),可以強制刪除:</p>" +
          cmd("git branch -D {branch}")),
  details("我不知道自己現在在哪條分支",
          "<p>打 <code>git status</code>,第一行就是答案。也可以用 <code>git branch</code>,有 <code>*</code> 的那條。</p>"),
  details("我在 main 上 commit 了本來該在分支做的事",
          "<p>commit 還在,先在目前位置開一個分支把它存起來。把 main 拉回與遠端一致的做法,在第 6 篇 Pull Request 的常見卡關有完整步驟。</p>" +
          cmd("git branch {branch}")))

SIM = {
  "a1": "<b>正確!</b><code>&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD</code> 到 <code>=======</code> 之間,是你「現在所在分支」的版本。合併時你站在哪條分支,HEAD 就是哪條。",
  "a2": "<b>不是。</b>分隔線下方、<code>&gt;&gt;&gt;&gt;&gt;&gt;&gt;</code> 之前,才是「要合進來的分支」的內容。",
  "a3": "<b>不是。</b>這兩段來自兩條不同的分支,不可能都是你這邊的。想清楚該留哪一段,或兩段都改寫成新的內容。"
}
QUIZ = quiz_cfg([
  ("要把 feature 分支合進 main,應該先做什麼?", ["切換到 main,再執行 git merge feature", "切換到 feature,再執行 git merge main", "直接刪掉 feature"], 0,
   "你站在誰身上,誰就接收別人的成果。要合進 main,就要先站在 main。"),
  ("Fast-forward 合併代表什麼?", ["發生了衝突", "main 沒有新進度,git 只把指標往前推,不產生合併 commit", "合併失敗"], 1,
   "分出去之後 main 沒有新 commit,所以只需要把 main 往前推到 feature 的位置。"),
  ("衝突標記 <code>=======</code> 的作用是?".replace("<code>","").replace("</code>",""), ["分隔兩邊的內容", "表示檔案結束", "表示已經解決"], 0,
   "它把「目前分支」與「要合進來的分支」的兩段內容隔開。"),
  ("解決衝突後,要做哪兩件事才算完成?", ["只要存檔就好", "git add 該檔案,然後 git commit", "重新 clone"], 1,
   "add 告訴 git 這個檔案已經解決,commit 完成這次合併。"),
  ("合併到一半想放棄,應該用?", ["git merge --abort", "git reset --hard HEAD~10", "刪掉整個資料夾"], 0,
   "--abort 會安全地退回合併前的狀態。"),
])

practice = section("practice", "動手演練:確認你真的懂了",
  '<p class="sub" style="margin-bottom:18px">先選答案再看原因。目的是看懂衝突標記,而不是背指令。</p>',
  sim("", "情境:你在 main 上執行 <code>git merge feature-title</code>,出現衝突", "檔案裡 <code>&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD</code> 與 <code>=======</code> 之間的內容,是誰的?",
      [("a1", "我現在所在分支(main)的版本"), ("a2", "feature-title 的版本"), ("a3", "兩邊都是我的")]),
  QUIZ_HTML,
  checks(["我動手前會先看 <code>git status</code> 確認所在分支。",
          "我一件事開一個分支,而不是直接在 main 上改。",
          "我知道 merge 要先站在「接收的那條分支」。",
          "我看得懂 <code>&lt;&lt;&lt;&lt;&lt;&lt;&lt;</code>、<code>=======</code>、<code>&gt;&gt;&gt;&gt;&gt;&gt;&gt;</code> 各代表哪邊。",
          "解決衝突後我會把三種標記整行刪乾淨。",
          "我知道合併到一半可以用 <code>git merge --abort</code> 放棄。"]),
  resources([
    ("https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-using-the-command-line", "用指令列解決合併衝突", "Resolving a merge conflict using the command line"),
    ("https://docs.github.com/en/get-started/using-git/about-git", "關於 Git", "About Git"),
  ]))

SPEC = dict(
  file="github-branch-guide.html",
  title="分支、合併與衝突解決:一件事一個分支",
  eyebrow="第 3 篇 · 分支與合併",
  h1="一件事一個分支,衝突只是 git 在問你留誰的",
  sub="分支讓你在不弄髒 <code>main</code> 的情況下放心嘗試。這一篇從開分支、合併,一路練到親手製造並解決一次衝突,讓你下次遇到時不再慌張。",
  tldr="用 <code>git switch -c</code> 開分支、在上面 commit、切回 <code>main</code> 用 <code>git merge</code> 合進來。兩邊改了同一行就會衝突:<strong>打開檔案留下要的內容、刪掉三種標記、add 再 commit</strong>。",
  toc=[("what", "分支是什麼"), ("map", "全貌圖"), ("fill", "填入你的資料"), ("steps", "八個步驟"), ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, mapsec, fillsec, section("steps", "照著做:八個步驟", S), gotchas, practice]),
  config=dict(fill=dict(branch="add-feature"), sim=SIM, quiz=QUIZ),
  prev=("github-gitignore-guide.html", ".gitignore 與檢視歷史"),
  next=("github-remote-guide.html", "遠端與同步"),
)
