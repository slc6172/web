from h import *

SVG = '''<svg viewBox="0 0 900 250" role="img" aria-label="密碼外洩的處理順序:先撤銷或更換金鑰,再清理歷史,最後開啟預防機制">
      <defs>
        <marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#87867F"/></marker>
        <style>.s{font:12px system-ui,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif}.nn{font:600 12px ui-monospace,Menlo,monospace}</style>
      </defs>
      <rect width="900" height="250" fill="#FFFFFF"/>
      <rect x="20" y="40" width="230" height="110" rx="10" fill="#FBF1EC" stroke="#B04A3F" stroke-width="2"/>
      <text x="135" y="76" text-anchor="middle" class="s" fill="#B04A3F">① 撤銷 / 更換</text>
      <text x="135" y="98" text-anchor="middle" class="s" fill="#141413">到服務商讓舊金鑰失效</text>
      <text x="135" y="118" text-anchor="middle" class="s" fill="#3D3D3A">這一步最重要、最先做</text>
      <rect x="335" y="40" width="230" height="110" rx="10" fill="#F0EEE6" stroke="#3D3D3A" stroke-width="1.5"/>
      <text x="450" y="76" text-anchor="middle" class="s" fill="#141413">② 清理歷史(選做)</text>
      <text x="450" y="98" text-anchor="middle" class="s" fill="#3D3D3A">git filter-repo 改寫歷史</text>
      <text x="450" y="118" text-anchor="middle" class="s" fill="#3D3D3A">降低被看到的機會</text>
      <rect x="650" y="40" width="230" height="110" rx="10" fill="#EEF2E8" stroke="#788C5D" stroke-width="1.5"/>
      <text x="765" y="76" text-anchor="middle" class="s" fill="#4B5C39">③ 開啟預防</text>
      <text x="765" y="98" text-anchor="middle" class="s" fill="#141413">.gitignore・push protection</text>
      <text x="765" y="118" text-anchor="middle" class="s" fill="#3D3D3A">Secret scanning・Dependabot</text>
      <line x1="253" y1="95" x2="331" y2="95" stroke="#87867F" stroke-width="1.5" marker-end="url(#ag)"/>
      <line x1="568" y1="95" x2="646" y2="95" stroke="#87867F" stroke-width="1.5" marker-end="url(#ag)"/>
      <circle cx="292" cy="75" r="11" fill="#D97757"/><text x="292" y="79.5" text-anchor="middle" class="nn" fill="#fff">1</text>
      <circle cx="607" cy="75" r="11" fill="#D97757"/><text x="607" y="79.5" text-anchor="middle" class="nn" fill="#fff">2</text>
      <text x="40" y="196" class="s" fill="#B85C3E">一旦 push,就當作已經外洩:機器人會在幾分鐘內掃描公開 repo。順序不能顛倒,先讓舊金鑰失效。</text>
    </svg>'''

what = section("what", "密碼一旦 push,就當作外洩",
  '<div class="panel"><h3>用「家裡鑰匙」來想</h3>'
  '<p>你把鑰匙放在公開的地方,就算幾分鐘後拿回來,也無法確定有沒有被人複製。所以正確做法不是「把鑰匙藏好」,而是<b>把鎖換掉</b>。Secret(密碼、API 金鑰、token、私鑰)也一樣:push 過,就必須先在服務端讓它失效。</p>'
  '<p style="margin-bottom:0">本篇分三層:<b>預防</b>(不讓它進 repo)、<b>偵測</b>(Secret scanning、push protection)、<b>善後</b>(撤銷、清理)。再加上 Dependabot,處理相依套件的漏洞。</p></div>',
  '<h3 style="margin-top:26px">六個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["secret", "不能公開的憑證:密碼、API key、token、私鑰、資料庫連線字串。"],
    ["Secret scanning", "GitHub 掃描 repo 內容,發現看起來像憑證的字串就提出警示。"],
    ["Push protection", "在你 push 的當下就攔截含 secret 的 commit,讓它根本進不了 repo。"],
    ["Dependabot alerts", "你用的套件有已知漏洞時發出警示。"],
    ["Dependabot security updates", "發現漏洞時,自動開 PR 把套件升到安全版本。"],
    ["Dependabot version updates", "依你設定的頻率,自動開 PR 升級套件版本。"],
  ]))

mapsec = section("map", "全貌:先讓舊金鑰失效,再談清理",
  '<p class="sub" style="margin-bottom:16px">順序很重要。很多人先忙著清歷史,卻忘了金鑰早就被抄走。</p>',
  canvas(SVG, [
    ("1", "<b>撤銷 / 更換</b>:到服務商後台讓舊金鑰失效,換新的。"),
    ("2", "<b>清理歷史</b>:改寫歷史把它移除。這只是補強,不能取代第 1 步。"),
    ("3", "<b>開啟預防</b>:<code>.gitignore</code>、push protection、Secret scanning、Dependabot。"),
  ]))

S = steps(
  step(1, "預防:不要讓 secret 進入 repo",
       "最好的處理是它從來沒有進過 repo。",
       ops(["把 secret 放在 <code>.env</code>,並寫進 <code>.gitignore</code>(見第 2 篇)。",
            "程式從環境變數讀取,不要把字串寫死在程式碼裡。",
            "另外提交一份只有欄位名稱的 <code>.env.example</code>,讓別人知道要設定什麼。"]),
       cmd("# .gitignore\n.env\n!.env.example\n\n# 程式裡改成讀環境變數(Node.js 範例)\nconst key = process.env.API_KEY;", cap="預防範例"),
       see("<code>git status</code> 看不到 <code>.env</code>,表示它被忽略了。")),
  step(2, "發現已經 commit(甚至 push)了:先別慌,照順序",
       "不要先刪檔案、不要先 revert,那都無法讓已外洩的金鑰失效。",
       ops(["<b>立刻到該服務的後台撤銷 / 更換這把金鑰</b>(例如雲端服務的 API keys 頁、資料庫的密碼設定、GitHub 的 Personal access tokens 頁)。",
            "確認新金鑰已設定好,舊金鑰真的失效了。",
            "檢查服務的使用紀錄,看有沒有不明的使用。有的話,視情況通知相關人員。"]),
       warn("<code>git revert</code> 與刪除檔案只會新增一個 commit,舊的 commit 仍然留著密碼。<b>只有撤銷才有用。</b>", "重要")),
  step(3, "(選做)清理歷史",
       "撤銷之後,舊金鑰已經沒用,清理歷史只是讓它不要繼續被看到。官方文件建議用 <code>git filter-repo</code>(較新的版本才有 <code>--sensitive-data-removal</code> 這個選項,請查閱工具說明)。",
       ops(["先把 repo 重新 clone 一份乾淨的副本來操作,避免弄壞原本的工作資料夾。",
            "依你的情況選一種做法:整個檔案從歷史移除,或用文字檔列出要替換的字串。",
            "檢查結果沒問題,再強制推送到 GitHub。"]),
       cmd("# 安裝:pip install git-filter-repo\n# 範例:把 .env 從所有歷史移除\ngit filter-repo --invert-paths --path .env\n\n# 範例:把檔案裡列出的字串替換掉(replacements.txt 每行一條規則)\n# git filter-repo --replace-text replacements.txt\n\n# 清理完,強制推送(會改寫整個雲端歷史)\n# git push --force --mirror origin"),
       warn("這會<b>改寫所有 commit 代號</b>、移除簽章,進行中的 PR 可能受影響。其他人手上的 clone 與 fork 仍然保有舊資料,你要通知他們重新 clone,並且不要用舊 clone 再 push 回來。GitHub 上的快取檢視與 PR 參照,需要另外聯絡 GitHub Support 才會清除。強制推送前務必先和團隊確認。", "風險")),
  step(4, "開啟 Secret scanning 與 push protection",
       "讓 GitHub 在 push 的當下就幫你擋。",
       ops(["個人帳號的 push protection,在 GitHub.com 上預設就是開啟的,會擋住你把 secret 推到公開 repo。",
            "repo 層級的 push protection 預設是關閉的,要由 repo 管理者(或組織擁有者)開啟。入口在 repo 的 <b>Settings</b> → 側邊欄 <b>Security and quality</b> 區塊的 <b>Advanced Security</b>。",
            "不同 repo 類型與方案可用的功能不同(例如部分功能屬於 GitHub Secret Protection),請依你頁面上實際出現的選項為準。"]),
       see("push 含有 secret 的 commit 時,終端機顯示 push 被拒絕,並說明是哪個檔案、哪一行。"),
       tip("被擋時的正確做法:移除 secret、改用環境變數、重新 commit。不要選「略過」,除非你確認那是誤報或測試用資料。略過會留下紀錄並通知管理者。")),
  step(5, "開啟 Dependabot alerts",
       "你的程式用了別人的套件。套件有漏洞,你的程式也受影響。Dependabot 幫你看。",
       ops(["進入 repo 的 <b>Settings</b>。",
            "側邊欄 <b>Security and quality</b> 區塊 → <b>Advanced Security</b>。",
            "在 <b>Dependabot alerts</b> 右邊按 <b>Enable</b>。"]),
       see("repo 的 <b>Security</b> 分頁出現 Dependabot 的警示清單(沒有漏洞時是空的)。"),
       warn("設定頁的區塊名稱與位置會調整,若看不到,請用設定頁上方的搜尋,或以官方文件為準。")),
  step(6, "讓 Dependabot 自動開 PR 升級套件",
       "有警示後,可以讓它直接開 PR 把套件升級到修好的版本;也可以設定定期檢查更新。",
       cmd('# .github/dependabot.yml\nversion: 2\nupdates:\n  - package-ecosystem: "npm"   # 依你用的套件管理員:npm、pip、maven …\n    directory: "/"              # 設定檔(如 package.json)所在的位置\n    schedule:\n      interval: "weekly"        # 每週檢查一次', cap=".github/dependabot.yml(版本更新)"),
       ops(["把上面內容存成 <code>.github/dependabot.yml</code>,依你的專案改 <code>package-ecosystem</code>。",
            "commit 並 push 到預設分支。",
            "之後 Dependabot 依排程開 PR,你像審查一般 PR 一樣看過、確認測試通過再合併(見第 7 篇)。"]),
       see("repo 的 <b>Pull requests</b> 出現由 <code>dependabot[bot]</code> 開的 PR,說明裡寫了升級的版本與變更內容。")),
  step(7, "在 GitHub Actions 裡用 secrets,不要寫死",
       "CI 需要部署金鑰時,放在 Actions secrets,不要寫進 workflow 檔。",
       ops(["repo 的 <b>Settings</b> → 側邊欄 <b>Secrets and variables</b> → <b>Actions</b>。",
            "在 <b>Secrets</b> 分頁按 <b>New repository secret</b>,填名稱與值,按 <b>Add secret</b>。",
            "workflow 裡用 <code>${{ secrets.名稱 }}</code> 取用(詳見第 11 篇)。"]),
       cmd("steps:\n  - name: Deploy\n    env:\n      API_KEY: ${{ secrets.API_KEY }}   # 值不會出現在日誌\n    run: ./deploy.sh", cap="workflow 片段"),
       see("secret 儲存後只能覆蓋或刪除,看不到原本的值;日誌裡出現的值會被遮成 <code>***</code>。"))
)

gotchas = section("gotchas", "常見卡關",
  details("我 commit 了密碼,但還沒 push",
          "<p>好消息:還沒離開你的電腦。用第 8 篇的方式把那個 commit 拆掉(<code>git reset --soft HEAD~1</code>),把 secret 移出去再重新 commit。仍建議更換金鑰,以防萬一曾經被別的工具(如雲端同步)看到。</p>"),
  details("我的 repo 是私人的,還需要撤銷嗎?",
          "<p>需要。私人 repo 仍然有協作者、CI 與整合服務能看到,而且 repo 之後可能被改成公開或被 fork。金鑰外洩的處理標準不因 repo 公開與否而不同。</p>"),
  details("push 被 push protection 擋住,但我確定是誤報",
          "<p>終端機訊息會提供略過的連結與選項(例如「是測試用資料」「是誤報」)。選擇後可以再 push,但這會留下紀錄並通知管理者。能改成不像金鑰的測試資料就改。</p>"),
  details("Dependabot 開了太多 PR",
          "<p>在 <code>dependabot.yml</code> 把 <code>interval</code> 改成 <code>monthly</code>,或設定 <code>open-pull-requests-limit</code> 限制同時開啟的數量,並把相關更新設定成分組。</p>"),
  details("我不知道自己有沒有把 secret commit 過",
          "<p>可以搜尋歷史:<code>git log -S\"可疑字串\" --oneline</code> 會列出新增或移除過這個字串的 commit。也可以到 repo 的 Security 分頁看 Secret scanning 有沒有警示。</p>"))

SIM = {
  "s1": "<b>第一步:到服務後台撤銷這把金鑰並更換。</b>刪檔案、revert、甚至清歷史都不能讓已外洩的金鑰失效。只有撤銷才有用。",
  "s2": "<b>先撤銷,再用 <code>git filter-repo</code> 清歷史。</b>清歷史只是補強,而且需要強制推送與通知所有人重新 clone。順序不能顛倒。",
  "s3": "<b>用 Actions secrets。</b>在 Settings 的 Secrets and variables → Actions 新增,workflow 用 <code>${{ secrets.名稱 }}</code> 取用。不要寫在 workflow 檔裡。",
  "s4": "<b>先移除並改用環境變數,再 commit。</b>不要選略過。若真的是誤報或測試資料,才用被擋時提供的略過選項,並知道這會通知管理者。"
}
QUIZ = quiz_cfg([
  ("你不小心把 API key push 到公開 repo,第一步該做什麼?", ["刪掉檔案再 push", "到服務後台撤銷並更換這把金鑰", "等一下看看有沒有人用"], 1,
   "刪檔案與 revert 都不會讓已外洩的金鑰失效,只有撤銷才有用。"),
  ("<code>git revert</code> 能讓已 commit 的密碼從歷史裡消失嗎?", ["能", "不能,舊 commit 還在", "只有私人 repo 能"], 1,
   "revert 只是新增一個反向 commit,舊的仍留在歷史。"),
  ("Push protection 的作用是?", ["在 push 的當下攔截含 secret 的 commit", "自動刪除 secret", "加密整個 repo"], 0,
   "它讓 secret 根本進不了 repo,比事後處理便宜得多。"),
  ("Dependabot alerts 是做什麼的?", ["套件有已知漏洞時發出警示", "自動合併所有 PR", "掃描你的密碼"], 0,
   "它比對你使用的套件版本,有已知漏洞時通知你。"),
  ("在 Actions workflow 裡需要 API key,該怎麼做?", ["寫進 workflow 檔", "放在 Settings 的 Actions secrets,用 secrets 內容取用", "貼在 README"], 1,
   "secrets 不會出現在 repo 內容與日誌中。"),
])

practice = section("practice", "動手演練:確認你真的懂了",
  '<p class="sub" style="margin-bottom:18px">先選答案再看原因。重點是養成「先撤銷」的反射。</p>',
  sim("", "情境:選一個你遇到的狀況", "你想知道下一步該怎麼做?",
      [("s1", "密碼 push 到公開 repo 了"), ("s2", "金鑰已撤銷,想清掉歷史"), ("s3", "CI 需要部署金鑰"), ("s4", "push 被 push protection 擋住")]),
  QUIZ_HTML,
  checks(["我知道 push 過的 secret 就當作外洩。",
          "遇到外洩,我第一步是撤銷與更換金鑰,不是刪檔案。",
          "我的 <code>.gitignore</code> 擋住了 <code>.env</code>,並提供 <code>.env.example</code>。",
          "我知道 <code>git revert</code> 無法讓舊 commit 裡的密碼消失。",
          "我已開啟(或知道在哪裡開啟)push protection 與 Secret scanning。",
          "我為專案開啟了 Dependabot alerts,並設好 <code>dependabot.yml</code>。",
          "CI 用的金鑰放在 Actions secrets,而不是寫在 workflow 檔。"]),
  resources([
    ("https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository", "移除 repo 中的敏感資料", "Removing sensitive data from a repository"),
    ("https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection", "關於 push protection", "About push protection"),
    ("https://docs.github.com/en/code-security/dependabot/dependabot-alerts/configuring-dependabot-alerts", "設定 Dependabot alerts", "Configuring Dependabot alerts"),
    ("https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuring-dependabot-version-updates", "設定 Dependabot 版本更新", "Configuring Dependabot version updates"),
    ("https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions", "在 Actions 使用 secrets", "Using secrets in GitHub Actions"),
  ]))

SPEC = dict(
  file="github-security-guide.html",
  title="安全性:Secrets 與 Dependabot:密碼一旦 push 就當作外洩",
  eyebrow="第 10 篇 · 安全性(進階選讀)",
  h1="密碼一旦 push 就當作外洩:先撤銷,再清理",
  sub="三層防線:不讓 secret 進 repo(預防)、進了就擋下(偵測)、進了就補救(善後)。最後再看 Dependabot 怎麼幫你盯住相依套件的漏洞。",
  tldr="<strong>先到服務後台撤銷並更換金鑰</strong>,這一步永遠最先做;刪檔案、revert、清歷史都無法讓已外洩的金鑰失效。平常用 <code>.gitignore</code>、環境變數、push protection 預防,用 Dependabot 盯住套件漏洞。",
  toc=[("what", "為什麼要撤銷"), ("map", "全貌圖"), ("steps", "七個步驟"), ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, mapsec, section("steps", "照著做:七個步驟", S), gotchas, practice]),
  config=dict(fill={}, sim=SIM, quiz=QUIZ),
  prev=("github-release-guide.html", "Release 與版本號"),
  next=("github-actions-guide.html", "GitHub Actions 與 Pages"),
)
