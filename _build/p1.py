from h import *

SVG = '''<svg viewBox="0 0 900 250" role="img" aria-label="Git 基本流程:工作資料夾、暫存區、本機 repo、GitHub 之間的 add、commit、push、clone">
      <defs>
        <marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#87867F"/></marker>
        <marker id="ac" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#D97757"/></marker>
        <style>.m{font:12px ui-monospace,Menlo,monospace}.s{font:12px system-ui,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif}.nn{font:600 12px ui-monospace,Menlo,monospace}</style>
      </defs>
      <rect width="900" height="250" fill="#FFFFFF"/>
      <text x="20" y="22" class="s" fill="#87867F">你的電腦</text>
      <text x="730" y="22" class="s" fill="#87867F">GitHub 網站</text>
      <rect x="20" y="36" width="160" height="84" rx="10" fill="#F0EEE6" stroke="#3D3D3A" stroke-width="1.5"/>
      <text x="100" y="72" text-anchor="middle" class="s" fill="#141413">工作資料夾</text>
      <text x="100" y="92" text-anchor="middle" class="s" fill="#3D3D3A">你改檔案的地方</text>
      <rect x="250" y="36" width="160" height="84" rx="10" fill="#F0EEE6" stroke="#3D3D3A" stroke-width="1.5"/>
      <text x="330" y="72" text-anchor="middle" class="s" fill="#141413">暫存區</text>
      <text x="330" y="92" text-anchor="middle" class="s" fill="#3D3D3A">挑好這次要記錄的</text>
      <rect x="480" y="36" width="160" height="84" rx="10" fill="#F0EEE6" stroke="#3D3D3A" stroke-width="1.5"/>
      <text x="560" y="72" text-anchor="middle" class="s" fill="#141413">本機 repo</text>
      <text x="560" y="92" text-anchor="middle" class="s" fill="#3D3D3A">commit 歷史存在這裡</text>
      <rect x="710" y="36" width="170" height="84" rx="10" fill="#E3DACC" stroke="#3D3D3A" stroke-width="2"/>
      <text x="795" y="72" text-anchor="middle" class="m" fill="#141413">origin</text>
      <text x="795" y="92" text-anchor="middle" class="s" fill="#3D3D3A">雲端上的 repo</text>
      <line x1="183" y1="78" x2="246" y2="78" stroke="#87867F" stroke-width="1.5" marker-end="url(#ag)"/>
      <circle cx="214" cy="58" r="11" fill="#D97757"/><text x="214" y="62.5" text-anchor="middle" class="nn" fill="#fff">1</text>
      <text x="196" y="102" class="m" fill="#3D3D3A">add</text>
      <line x1="413" y1="78" x2="476" y2="78" stroke="#87867F" stroke-width="1.5" marker-end="url(#ag)"/>
      <circle cx="444" cy="58" r="11" fill="#D97757"/><text x="444" y="62.5" text-anchor="middle" class="nn" fill="#fff">2</text>
      <text x="418" y="102" class="m" fill="#3D3D3A">commit</text>
      <line x1="643" y1="78" x2="706" y2="78" stroke="#87867F" stroke-width="1.5" marker-end="url(#ag)"/>
      <circle cx="674" cy="58" r="11" fill="#D97757"/><text x="674" y="62.5" text-anchor="middle" class="nn" fill="#fff">3</text>
      <text x="660" y="102" class="m" fill="#3D3D3A">push</text>
      <path d="M795,124 C795,210 100,210 100,124" fill="none" stroke="#D97757" stroke-width="2.5" marker-end="url(#ac)"/>
      <circle cx="447" cy="190" r="12" fill="#D97757"/><text x="447" y="194.5" text-anchor="middle" class="nn" fill="#fff">4</text>
      <text x="468" y="214" class="s" fill="#B85C3E">clone:第一次把雲端 repo 抓下來</text>
    </svg>'''

what = section("what", "Git 和 GitHub 是兩個東西",
  '<div class="panel"><h3>用「遊戲存檔」來想</h3>'
  '<p><b>Git</b> 是裝在你電腦上的工具,像遊戲的存檔系統:每次 <code>commit</code> 就是一個存檔點,隨時能回頭看、回到過去。它不需要網路。</p>'
  '<p style="margin-bottom:0"><b>GitHub</b> 是放 Git 專案的雲端網站:把存檔點備份上去、讓別人看到、一起討論與合作。<b>沒有 GitHub 也能用 Git;有了 GitHub,才能備份與協作。</b>你要學的就是「怎麼把本機的存檔點送上去」。</p></div>',
  '<h3 style="margin-top:26px">七個會一直出現的名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["repo", "一個專案的資料夾,連同它所有的歷史紀錄。"],
    ["commit", "一個存檔點:把某一刻的檔案狀態連同一句說明記下來。"],
    ["暫存區(staging)", "commit 之前的「取景框」。你用 <code>git add</code> 決定這次存檔要包含哪些檔案。"],
    ["remote / origin", "遠端:GitHub 上的那份 repo。<code>origin</code> 是 git 替它取的預設名字。"],
    ["clone", "把 GitHub 上的 repo 整份抓到你的電腦。通常只做一次。"],
    ["push", "把本機新的 commit 送到 GitHub。"],
    ["main", "預設的主要分支名稱。新手階段你只會待在這條分支上。"],
  ]))

mapsec = section("map", "全貌:一次推送只有四個動作",
  '<p class="sub" style="margin-bottom:16px">先看地圖,後面每一步都會回到這張圖。左邊三個方塊在你的電腦,右邊在 GitHub。</p>',
  canvas(SVG, [
    ("1", "<b>add</b>:把改好的檔案放進暫存區。"),
    ("2", "<b>commit</b>:把暫存區的內容存成一個存檔點。"),
    ("3", "<b>push</b>:把存檔點送上 GitHub。"),
    ("4", "<b>clone</b>:一開始把 GitHub 上的 repo 抓到電腦(只做一次)。"),
  ]))

fillsec = section("fill", "先填入你的資料,下面所有指令會自動換成你的版本",
  fill([("name", "顯示名稱", True), ("email", "Email", False), ("me", "你的 GitHub 帳號", False), ("repo", "專案名稱", False)]))

S = steps(
  step(1, "註冊 GitHub 並安裝 Git",
       "GitHub 是網站,Git 是要裝在電腦上的程式,兩個都要有。",
       ops(["到 <code>github.com</code> 按 <b>Sign up</b>,依畫面建立帳號並驗證 email。",
            "安裝 Git:Windows 到 <code>git-scm.com</code> 下載安裝(預設選項即可,會附帶 Git Bash);macOS 在終端機打 <code>xcode-select --install</code>;Ubuntu / Debian 打 <code>sudo apt install git</code>。",
            "開一個終端機(Windows 用 Git Bash),輸入下面指令確認安裝成功。"]),
       cmd("git --version"),
       see("類似 <code>git version 2.45.0</code> 的一行(數字依你的版本而不同)。")),
  step(2, "告訴 Git 你是誰(只做一次)",
       "每個 commit 都會記錄作者。還沒設定的話,第一次 commit 會失敗並顯示 <code>Author identity unknown</code>。",
       cmd('git config --global user.name "{name}"\ngit config --global user.email "{email}"\ngit config --global init.defaultBranch main\ngit config --global --list'),
       see("<code>--list</code> 的輸出裡有你剛設的 <code>user.name</code>、<code>user.email</code> 與 <code>init.defaultBranch=main</code>。"),
       warn("email 要和 GitHub 帳號的 email 一致,commit 才會算在你的帳號底下。想隱藏真實 email,可到 GitHub 的 <b>Settings → Emails</b> 取得 noreply 位址來用。")),
  step(3, "在 GitHub 網頁上建立一個 repo",
       "先有雲端的家,才有東西可以 clone 與 push。",
       ops(["登入 GitHub,按右上角的 <b>+</b> → <b>New repository</b>。",
            "<b>Repository name</b> 填 <code data-tpl>{repo}</code>。",
            "選 <b>Public</b>(公開)或 <b>Private</b>(私人)。練習用哪個都可以。",
            "勾選 <b>Add a README file</b>,讓 repo 一開始不是空的。",
            "按 <b>Create repository</b>。"]),
       see("跳到 <code data-tpl>github.com/{me}/{repo}</code>,頁面列出一個 <code>README.md</code> 檔案。"),
       tip("新手建議勾 README:repo 不是空的,下一步 clone 最簡單。")),
  step(4, "Clone:把 repo 抓到電腦",
       "clone 會把整份 repo 與歷史抓下來,並自動把雲端那份取名 <code>origin</code>,所以你不需要再手動設定遠端。",
       cmd("git clone https://github.com/{me}/{repo}.git\ncd {repo}\ngit status"),
       see("終端機顯示 <code>Cloning into '{repo}'...</code>;<code>git status</code> 顯示 <code>On branch main</code> 與 <code>Your branch is up to date with 'origin/main'</code>。"),
       warn("<code>cd {repo}</code> 之後,後面所有 git 指令都要在這個資料夾裡打。", "檢查")),
  step(5, "新增或修改一個檔案",
       "這是你平常就會做的事:改檔案。Git 此時已經知道有變化,但還沒有記錄。",
       cmd('echo "我的第一次推送" > hello.txt\ngit status'),
       see("<code>Untracked files:</code> 底下列出 <code>hello.txt</code>(通常是紅色)。意思是:這個檔案 git 還不認識。")),
  step(6, "add:放進暫存區",
       "暫存區讓你挑選「這次存檔要包含什麼」。例如你改了五個檔案,卻只想先存其中兩個。",
       cmd("git add hello.txt\ngit status"),
       see("<code>Changes to be committed:</code> 底下出現 <code>new file: hello.txt</code>(通常是綠色)。"),
       tip("<code>git add .</code> 會一次加入全部變更。用之前先看 <code>git status</code>,避免把不該進 repo 的檔案也加進去(見第 2 篇 .gitignore)。")),
  step(7, "commit:存成一個存檔點",
       "<code>-m</code> 後面接這次存檔的說明。寫成「改了什麼」,以後翻歷史才看得懂。",
       cmd('git commit -m "新增 hello.txt"\ngit log --oneline'),
       see("<code>1 file changed, 1 insertion(+)</code>;<code>git log --oneline</code> 最上面一行是 7 個字元的代號加上你的說明。"),
       warn("如果畫面跳進一個文字編輯器(忘了 <code>-m</code>),在 vim 裡按 <code>Esc</code>,輸入 <code>:q!</code> 再按 Enter 離開,然後補上 <code>-m</code> 重打。")),
  step(8, "push:送上 GitHub",
       "到這一步,commit 還只存在你的電腦。push 才會把它送到 GitHub。",
       cmd("git push"),
       ops(["第一次 push 可能要求登入:瀏覽器會跳出授權視窗(Git Credential Manager),照畫面登入即可。",
            "回到 <code data-tpl>github.com/{me}/{repo}</code> 重新整理頁面。"]),
       see("終端機最後幾行有 <code>main -&gt; main</code>;網頁上出現 <code>hello.txt</code>,旁邊顯示你寫的 commit 說明。"),
       warn("登入時不能用 GitHub 密碼。若終端機要求密碼並顯示 <code>Authentication failed</code>,請看下方「常見卡關」與第 4 篇。"))
)

gotchas = section("gotchas", "初學者最常卡住的六個地方",
  details("<code>fatal: not a git repository</code>",
          "<p>你所在的資料夾不是 repo。用 <code>pwd</code>(Windows 的 Git Bash 也可用)確認位置,<code>cd</code> 進 clone 下來的資料夾再試一次。</p>"),
  details("<code>Author identity unknown</code>(commit 失敗)",
          "<p>還沒設定 <code>user.name</code> 與 <code>user.email</code>,回到步驟 2 設定,再重打一次 <code>git commit</code>。</p>"),
  details("push 時要求輸入密碼,卻顯示 <code>Authentication failed</code>",
          "<p>GitHub 已不接受用帳號密碼登入 Git。解法是:使用 Git Credential Manager 的瀏覽器授權,或改用 Personal Access Token 或 SSH 金鑰。設定細節在第 4 篇「遠端與同步」。</p>"),
  details("我的分支叫 <code>master</code>,不是 <code>main</code>",
          "<p>舊版 Git 的預設分支叫 master。步驟 2 已設定新專案預設用 main。現有專案想改名:</p>" +
          cmd("git branch -M main")),
  details("我已經有一個本機專案,想把它放上 GitHub(不是 clone)",
          "<p>先在 GitHub 建一個<b>空的</b> repo(不要勾 README),再在你的專案資料夾裡:</p>" +
          cmd("git init\ngit add .\ngit commit -m \"第一次提交\"\ngit branch -M main\ngit remote add origin https://github.com/{me}/{repo}.git\ngit push -u origin main") +
          "<p>這裡的 <code>git remote add origin</code> 就是 clone 幫你自動做的那一步。</p>"),
  details("中文檔名在 <code>git status</code> 裡變成一串 <code>\\346\\226...</code>",
          "<p>這只是顯示方式,檔案本身沒壞。下面這行讓 git 直接顯示中文檔名:</p>" +
          cmd("git config --global core.quotepath false")))

SIM = {
  "a1": "<b>正確!</b>commit 只是在你的電腦上存檔。要讓 GitHub 上看得到,還要 <code>git push</code>。",
  "a2": "<b>不是。</b>clone 是一開始把雲端 repo 抓下來,而且通常只做一次。你的 commit 沒出現,原因是還沒 push。",
  "a3": "<b>不是。</b>fork 是要貢獻別人的專案才需要(見第 6 篇)。這是你自己的 repo,不需要 fork。"
}
QUIZ = quiz_cfg([
  ("Git 和 GitHub 的關係是?", ["兩個名字不同的同一個東西", "Git 是裝在電腦上的版本控制工具,GitHub 是存放 Git 專案的雲端網站", "Git 是網站,GitHub 是電腦上的程式"], 1,
   "Git 在本機管理版本,GitHub 提供雲端備份與協作。沒有 GitHub 也能用 Git。"),
  ("<code>git add hello.txt</code> 做了什麼?", ["把檔案放進暫存區,準備下一次 commit", "把檔案上傳到 GitHub", "把檔案刪除"], 0,
   "add 只是挑選這次 commit 要包含的內容,不會上傳。"),
  ("commit 完之後,GitHub 網頁上就會看到新檔案嗎?", ["會,commit 會自動上傳", "不會,commit 只存在本機,還要 push", "不會,要重新 clone"], 1,
   "commit 是本機存檔,push 才會把它送到 GitHub。"),
  ("GitHub 上已經有 repo,要把它抓到電腦,該用哪個指令?", ["git init", "git clone", "git commit"], 1,
   "clone 會抓下整份 repo 與歷史,並自動設好 origin。"),
  ("第一次 commit 之前,必須先做什麼設定?", ["設定 <code>user.name</code> 與 <code>user.email</code>".replace("<code>", "").replace("</code>", ""), "安裝 Node.js", "建立 .gitignore"], 0,
   "每個 commit 都會記錄作者,沒設定的話會出現 Author identity unknown。"),
])

practice = section("practice", "動手演練:確認你真的懂了",
  '<p class="sub" style="margin-bottom:18px">先選答案再看原因。目的不是背指令,而是確認你懂資料是怎麼從電腦走到 GitHub 的。</p>',
  sim("", "情境:你 add 並 commit 完,打開 GitHub 網頁卻沒看到新檔案", "最可能漏了哪一步?",
      [("a1", "漏了 <code>git push</code>"), ("a2", "漏了 <code>git clone</code>"), ("a3", "要先 fork")]),
  QUIZ_HTML,
  checks(["我能說出 Git 與 GitHub 的差別。",
          "我已設定 <code>user.name</code> 與 <code>user.email</code>。",
          "我知道 <code>git clone</code> 之後要先 <code>cd</code> 進資料夾。",
          "我能依序說出 add → commit → push 各做什麼。",
          "我 commit 前會先看 <code>git status</code>。",
          "我知道登入 GitHub 不能用密碼,要用授權或 token。"]),
  resources([
    ("https://docs.github.com/en/get-started/start-your-journey/hello-world", "Hello World", "Hello World 入門"),
    ("https://docs.github.com/en/get-started/git-basics/set-up-git", "設定 Git", "Set up Git"),
    ("https://docs.github.com/en/repositories/creating-and-managing-repositories/quickstart-for-repositories", "建立 repo 快速入門", "Quickstart for repositories"),
    ("https://docs.github.com/en/get-started/git-basics/about-remote-repositories", "關於遠端 repo", "About remote repositories"),
  ]))

SPEC = dict(
  file="github-start-guide.html",
  title="GitHub 是什麼與第一次推送:五個指令就夠",
  eyebrow="第 1 篇 · 第一次推送",
  h1="從零到第一次 push:五個指令就夠",
  sub="給完全沒碰過 git 的你。先分清楚 Git 與 GitHub,再用 <code>clone</code>、<code>add</code>、<code>commit</code>、<code>push</code> 把第一個檔案送上 GitHub。每一步都說明為什麼要做、要打什麼、會看到什麼。",
  tldr="Git 在你的電腦上記錄存檔點,GitHub 是把存檔點放上雲端的網站。流程只有四個動作:<strong>clone</strong>(抓下來)→ <strong>add</strong>(挑檔案)→ <strong>commit</strong>(存檔)→ <strong>push</strong>(送上去)。",
  toc=[("what", "Git 和 GitHub"), ("map", "全貌圖"), ("fill", "填入你的資料"), ("steps", "八個步驟"), ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, mapsec, fillsec, section("steps", "照著做:八個步驟", S), gotchas, practice]),
  config=dict(fill=dict(name="Your Name", email="you@example.com", me="your-name", repo="hello-world"), sim=SIM, quiz=QUIZ),
  prev=None,
  next=("github-gitignore-guide.html", ".gitignore 與檢視歷史"),
)
