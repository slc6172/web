from h import *

SVG = '''<svg viewBox="0 0 900 250" role="img" aria-label="遠端同步:GitHub 的 origin 透過 fetch 更新本機的 origin/main,再 merge 進你的 main;push 則把 main 送回 GitHub">
      <defs>
        <marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#87867F"/></marker>
        <marker id="ac" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#D97757"/></marker>
        <style>.m{font:12px ui-monospace,Menlo,monospace}.s{font:12px system-ui,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif}.nn{font:600 12px ui-monospace,Menlo,monospace}</style>
      </defs>
      <rect width="900" height="250" fill="#FFFFFF"/>
      <text x="20" y="22" class="s" fill="#87867F">GitHub 網站</text>
      <text x="360" y="22" class="s" fill="#87867F">你的電腦</text>
      <rect x="20" y="36" width="230" height="84" rx="10" fill="#E3DACC" stroke="#3D3D3A" stroke-width="2"/>
      <text x="135" y="68" text-anchor="middle" class="m" fill="#141413">origin 的 main</text>
      <text x="135" y="90" text-anchor="middle" class="s" fill="#3D3D3A">雲端上的最新進度</text>
      <rect x="335" y="36" width="230" height="84" rx="10" fill="#F0EEE6" stroke="#3D3D3A" stroke-width="1.5"/>
      <text x="450" y="68" text-anchor="middle" class="m" fill="#141413">origin/main</text>
      <text x="450" y="90" text-anchor="middle" class="s" fill="#3D3D3A">本機記著的「雲端進度」</text>
      <rect x="650" y="36" width="230" height="84" rx="10" fill="#F0EEE6" stroke="#3D3D3A" stroke-width="1.5"/>
      <text x="765" y="68" text-anchor="middle" class="m" fill="#141413">你的 main</text>
      <text x="765" y="90" text-anchor="middle" class="s" fill="#3D3D3A">你實際工作的分支</text>
      <line x1="253" y1="78" x2="331" y2="78" stroke="#87867F" stroke-width="1.5" marker-end="url(#ag)"/>
      <circle cx="292" cy="58" r="11" fill="#D97757"/><text x="292" y="62.5" text-anchor="middle" class="nn" fill="#fff">1</text>
      <text x="268" y="102" class="m" fill="#3D3D3A">fetch</text>
      <line x1="568" y1="78" x2="646" y2="78" stroke="#87867F" stroke-width="1.5" marker-end="url(#ag)"/>
      <circle cx="607" cy="58" r="11" fill="#D97757"/><text x="607" y="62.5" text-anchor="middle" class="nn" fill="#fff">2</text>
      <text x="580" y="102" class="m" fill="#3D3D3A">merge</text>
      <path d="M765,124 C765,205 135,205 135,124" fill="none" stroke="#D97757" stroke-width="2.5" marker-end="url(#ac)"/>
      <circle cx="450" cy="190" r="12" fill="#D97757"/><text x="450" y="194.5" text-anchor="middle" class="nn" fill="#fff">3</text>
      <text x="470" y="216" class="s" fill="#B85C3E">push:把你的 main 送回雲端</text>
      <rect x="335" y="140" width="230" height="26" rx="13" fill="#FBF1EC" stroke="#D97757" stroke-width="1"/>
      <text x="450" y="157" text-anchor="middle" class="s" fill="#B85C3E">pull = ① fetch + ② merge</text>
    </svg>'''

what = section("what", "origin 是你的雲端副本",
  '<div class="panel"><h3>用「雲端共用文件」來想</h3>'
  '<p>你的電腦上有一份工作副本,GitHub 上有一份雲端版本。兩份要靠三個動作保持一致:<b>fetch</b>(只是看看雲端有什麼新東西)、<b>pull</b>(看,而且直接併進來)、<b>push</b>(把你的新進度送上去)。</p>'
  '<p style="margin-bottom:0">另一個重點是<b>登入</b>:GitHub 不收帳號密碼,要用瀏覽器授權、Personal Access Token(PAT)或 SSH 金鑰三者之一。</p></div>',
  '<h3 style="margin-top:26px">五個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["remote", "遠端:別的地方的那份 repo。<code>git remote -v</code> 可以列出來。"],
    ["origin", "你 clone 時,git 替來源取的預設名字。"],
    ["origin/main", "你的電腦記下來的「上次看雲端時,它的 main 長怎樣」。要 fetch 才會更新。"],
    ["fetch / pull", "fetch 只更新 <code>origin/main</code>,不動你的檔案;pull 是 fetch 再加 merge,會動你的檔案。"],
    ["PAT / SSH", "兩種證明身分的方式:一串像密碼的 token,或一對金鑰(私鑰留在你電腦,公鑰交給 GitHub)。"],
  ]))

mapsec = section("map", "全貌:一個本機分支背後有三個位置",
  '<p class="sub" style="margin-bottom:16px">看懂「origin/main」是中間那一格,就看懂了 fetch 與 pull 的差別。</p>',
  canvas(SVG, [
    ("1", "<b>fetch</b>:把雲端的新進度抓到 <code>origin/main</code>(不動你的檔案)。"),
    ("2", "<b>merge</b>:把 <code>origin/main</code> 併進你的 <code>main</code>。"),
    ("3", "<b>push</b>:把你的 <code>main</code> 送到雲端。"),
    ("=", "<b>pull</b> 就是 1 加 2 一次做完。"),
  ]))

fillsec = section("fill", "先填入你的資料,下面的指令會自動換成你的版本",
  fill([("me", "你的 GitHub 帳號", False), ("repo", "專案名稱", False), ("email", "Email", False)]))

S = steps(
  step(1, "看目前的遠端是哪裡",
       "連不上或登入錯,第一件事就是看遠端網址指到哪。",
       cmd("git remote -v"),
       see("四行輸出:<code>origin</code> 的 <code>(fetch)</code> 與 <code>(push)</code> 各一行,網址是 <code data-tpl>https://github.com/{me}/{repo}.git</code> 或 <code data-tpl>git@github.com:{me}/{repo}.git</code>。前者是 HTTPS,後者是 SSH。")),
  step(2, "fetch:先看雲端有什麼新東西",
       "fetch 很安全,它只是把雲端的新進度抓下來放在 <code>origin/main</code>,不會改動你正在編輯的檔案。",
       cmd("git fetch\ngit status\ngit log --oneline main..origin/main"),
       see("<code>git status</code> 可能顯示 <code>Your branch is behind 'origin/main' by 2 commits</code>;最後一個指令列出「雲端有、你還沒有」的 commit。沒有新東西時什麼都不會顯示。")),
  step(3, "pull:把雲端的新進度併進來",
       "pull 等於 fetch 加 merge。建議先設定一次,讓行為單純可預期。",
       cmd("git config --global pull.rebase false\ngit pull"),
       see("<code>Fast-forward</code> 與更新的檔案清單;已經是最新時顯示 <code>Already up to date.</code>。"),
       tip("<code>pull.rebase false</code> 代表用 merge 來整合,是新手最容易理解的方式。第一次 pull 遇到 <code>divergent branches</code> 提示,就是因為這個選項還沒設。")),
  step(4, "push:把你的 commit 送上去",
       "新分支第一次 push 要加 <code>-u</code>,讓 git 記住它對應雲端哪個分支,以後只要打 <code>git push</code>。",
       cmd("git push\n# 新分支的第一次:\n# git push -u origin 分支名稱"),
       see("最後幾行有 <code>main -&gt; main</code>。")),
  step(5, "登入方式 A:瀏覽器授權或 Personal Access Token(HTTPS)",
       "網址是 <code>https://</code> 開頭時用這一條。多數新版 Git(Windows、macOS 的標準安裝)附帶 Git Credential Manager,第一次 push 會跳出瀏覽器請你登入並授權,完成後自動記住,這是最省事的做法。",
       ops(["若沒有跳出瀏覽器、而是要求輸入密碼,就要改用 token:到 GitHub 右上角頭像 → <b>Settings</b> → 最底下 <b>Developer settings</b> → <b>Personal access tokens</b>。",
            "建立一個 <b>Fine-grained token</b>:只選你要用的 repo,權限 <b>Contents</b> 設為 <b>Read and write</b>,設定到期日,按 <b>Generate token</b>。",
            "把 token 複製起來(只會顯示一次)。下次終端機問 <b>Password</b> 時,貼上 token 當密碼;<b>Username</b> 填你的帳號。"]),
       warn("token 等於密碼。不要貼在聊天、不要寫進程式碼、不要 commit 進 repo(見第 10 篇)。設到期日,不用時就到同一頁撤銷。", "安全")),
  step(6, "登入方式 B:SSH 金鑰",
       "網址是 <code>git@github.com:</code> 開頭時用這一條。你會產生一對金鑰:<b>私鑰</b>留在你電腦,<b>公鑰</b>交給 GitHub。之後不用再輸入任何密碼。",
       cmd('ssh-keygen -t ed25519 -C "{email}"\n# 一路按 Enter 接受預設值(可設 passphrase)\neval "$(ssh-agent -s)"\nssh-add ~/.ssh/id_ed25519\ncat ~/.ssh/id_ed25519.pub'),
       ops(["複製最後一個指令印出的整行內容(<code>ssh-ed25519 …</code> 開頭)。",
            "GitHub 右上角頭像 → <b>Settings</b> → <b>SSH and GPG keys</b> → <b>New SSH key</b>。",
            "Title 取個辨識用的名字(例如 my-laptop),Key 貼上剛才複製的內容,按 <b>Add SSH key</b>。",
            "回終端機測試連線。"]),
       cmd("ssh -T git@github.com"),
       see("第一次會問是否信任主機,輸入 <code>yes</code>。成功時顯示 <code>Hi 你的帳號! You've successfully authenticated, but GitHub does not provide shell access.</code>。這就是成功,不是錯誤。"),
       warn("只能貼 <code>.pub</code> 結尾的<b>公鑰</b>。沒有 <code>.pub</code> 的那個檔案是私鑰,絕對不能分享、貼上或 commit。", "重要")),
  step(7, "把既有 repo 的網址換成 SSH(或換回 HTTPS)",
       "clone 時用的是哪種網址,就會繼續用那種。想換,只要改 origin 的網址。",
       cmd("git remote set-url origin git@github.com:{me}/{repo}.git\ngit remote -v\n# 換回 HTTPS:\n# git remote set-url origin https://github.com/{me}/{repo}.git"),
       see("<code>git remote -v</code> 顯示的網址已經是新的那一種。"))
)

gotchas = section("gotchas", "初學者最常卡住的六個地方",
  details("<code>! [rejected] main -&gt; main (fetch first)</code> 或 <code>non-fast-forward</code>",
          "<p>雲端有你這邊沒有的新 commit,git 不讓你直接蓋過去。先把雲端的併進來,再 push:</p>" + cmd("git pull\ngit push") +
          "<p>如果 pull 時出現衝突,照第 3 篇的方式解決,再 push。不要用 <code>--force</code> 硬蓋,那會洗掉別人的 commit。</p>"),
  details("<code>remote: Permission to … denied to 某個帳號</code>(403)",
          "<p>你現在登入的是「某個帳號」,它對這個 repo 沒有寫入權限。常見原因:電腦裡存了另一個帳號的登入資訊,或 clone 的是別人的 repo。</p>"
          "<p>先看 <code>git remote -v</code> 是不是你自己的 repo。若是別人的專案,請走 fork 流程(見第 6 篇)。若存了舊帳號的憑證,在 Windows 到「認證管理員」、macOS 到「鑰匙圈存取」刪掉 github.com 的項目,下次 push 重新登入。</p>"),
  details("<code>Permission denied (publickey)</code>",
          "<p>SSH 沒有認出你的金鑰。依序檢查:</p><ol class='ops'><li>公鑰有沒有貼到 GitHub 的 SSH and GPG keys。</li><li><code>ssh-add -l</code> 有沒有列出你的金鑰;沒有就重做步驟 6 的 <code>ssh-add</code>。</li><li>用 <code>ssh -T git@github.com</code> 單獨測試。</li></ol>"),
  details("<code>Authentication failed</code> 或一直要求密碼",
          "<p>GitHub 不再接受帳號密碼登入 Git。改用步驟 5(瀏覽器授權或 token)或步驟 6(SSH)。貼上 token 時畫面不會顯示字元,這是正常的。</p>"),
  details("<code>fatal: refusing to merge unrelated histories</code>",
          "<p>兩邊的歷史完全沒有共同祖先,常見於「本機 <code>git init</code>、GitHub 上又勾了 README」的情況。確定要把兩邊接起來才加參數:</p>" + cmd("git pull origin main --allow-unrelated-histories")),
  details("第一次 pull 出現 <code>hint: You have divergent branches</code>",
          "<p>git 要你選一種整合方式。依步驟 3 設定 <code>pull.rebase false</code>,再重打 <code>git pull</code>。</p>"))

SIM = {
  "r1": "<b>先 <code>git pull</code> 再 <code>git push</code>。</b>雲端有你還沒有的 commit,把它併進來之後才能送上去。不要用 <code>--force</code>。",
  "r2": "<b>先檢查身分與網址。</b>看 <code>git remote -v</code> 是不是你自己的 repo;再看目前登入的是不是正確帳號,必要時清掉舊憑證重新登入。如果是別人的專案,要走 fork。",
  "r3": "<b>檢查 SSH 金鑰。</b>確認公鑰已加到 GitHub、用 <code>ssh-add</code> 載入了私鑰,再用 <code>ssh -T git@github.com</code> 測試。",
  "r4": "<b>改用瀏覽器授權或 token,或換成 SSH。</b>GitHub 不接受用帳號密碼登入 Git。"
}
QUIZ = quiz_cfg([
  ("<code>git fetch</code> 與 <code>git pull</code> 最大的差別是?", ["沒有差別", "fetch 只更新 origin/main,不動你的檔案;pull 還會把它併進你的分支", "fetch 會上傳,pull 會下載"], 1,
   "pull = fetch + merge。想先看看雲端有什麼,用 fetch 最安全。"),
  ("<code>git push</code> 顯示 <code>rejected (fetch first)</code>,正確做法是?", ["加 --force 強制蓋過", "先 git pull 把雲端新進度併進來,再 push", "刪掉 repo 重新 clone"], 1,
   "強推會洗掉別人的 commit;先整合再送是標準做法。"),
  ("SSH 金鑰要貼到 GitHub 的是哪一把?", ["私鑰(沒有 .pub 的那個)", "公鑰(.pub 結尾)", "兩把都要貼"], 1,
   "私鑰永遠留在你電腦;只有公鑰交給 GitHub。"),
  ("<code>git remote -v</code> 看到 <code>git@github.com:…</code> 開頭的網址,代表?", ["這個 remote 用 SSH 連線", "這個 remote 用 HTTPS 連線", "這個 repo 是私人的"], 0,
   "git@github.com: 開頭是 SSH;https:// 開頭是 HTTPS。"),
  ("<code>ssh -T git@github.com</code> 顯示 “successfully authenticated, but GitHub does not provide shell access”,代表?", ["連線成功,身分驗證通過", "連線失敗", "你的金鑰過期了"], 0,
   "這句話就是成功訊息:GitHub 認得你,只是不提供終端機登入。"),
])

practice = section("practice", "動手演練:確認你真的懂了",
  '<p class="sub" style="margin-bottom:18px">看到錯誤訊息時,先判斷是「同步」問題還是「登入」問題,下一步就清楚了。</p>',
  sim("", "情境:選一個你遇到的錯誤訊息", "你想知道第一步該怎麼處理?",
      [("r1", "<code>rejected (fetch first)</code>"), ("r2", "<code>Permission to … denied to 某帳號</code>"), ("r3", "<code>Permission denied (publickey)</code>"), ("r4", "要求輸入密碼後 <code>Authentication failed</code>")]),
  QUIZ_HTML,
  checks(["我知道 <code>origin/main</code> 是「本機記著的雲端進度」。",
          "我 push 被拒絕時,會先 pull 再 push,而不是 <code>--force</code>。",
          "我知道登入 GitHub 不能用密碼,要用瀏覽器授權、token 或 SSH。",
          "我的 token 有設到期日,而且沒有存進任何 repo。",
          "我只把 <code>.pub</code> 公鑰貼給 GitHub,從不分享私鑰。",
          "遇到 403 我會先看 <code>git remote -v</code> 與目前登入的帳號。"]),
  resources([
    ("https://docs.github.com/en/get-started/git-basics/about-remote-repositories", "關於遠端 repo", "About remote repositories"),
    ("https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent", "產生 SSH 金鑰並加入 ssh-agent", "Generating a new SSH key"),
    ("https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens", "管理 Personal Access Token", "Managing your personal access tokens"),
    ("https://docs.github.com/en/get-started/git-basics/getting-changes-from-a-remote-repository", "從遠端取得變更", "Getting changes from a remote repository"),
  ]))

SPEC = dict(
  file="github-remote-guide.html",
  title="遠端與同步:fetch、pull、push 與登入驗證",
  eyebrow="第 4 篇 · 遠端與同步",
  h1="origin 是你的雲端副本,fetch 看、pull 拿、push 送",
  sub="push 被拒絕、要求密碼、403、Permission denied,幾乎都出在「同步」或「登入」。這一篇把兩件事一次講清楚:怎麼和雲端保持一致,以及怎麼用瀏覽器授權、token 或 SSH 證明你是你。",
  tldr="<code>fetch</code> 只更新 <code>origin/main</code>(安全),<code>pull</code> = fetch + merge,<code>push</code> 送你的進度。登入不能用密碼:用<strong>瀏覽器授權、Personal Access Token 或 SSH 金鑰</strong>。被拒絕時先 <code>pull</code>,不要 <code>--force</code>。",
  toc=[("what", "遠端與驗證"), ("map", "全貌圖"), ("fill", "填入你的資料"), ("steps", "七個步驟"), ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, mapsec, fillsec, section("steps", "照著做:七個步驟", S), gotchas, practice]),
  config=dict(fill=dict(me="your-name", repo="hello-world", email="you@example.com"), sim=SIM, quiz=QUIZ),
  prev=("github-branch-guide.html", "分支、合併與衝突解決"),
  next=("github-issues-guide.html", "Issue 與 Projects"),
)
