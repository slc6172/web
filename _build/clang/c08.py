from ch import *

what = section("what", "這一篇不教新語法,只把學過的組起來",
  '<div class="panel"><h3>用前七篇,做兩個完整的程式</h3>'
  '<p>會一個一個語法,和做出一支完整的程式是兩回事。這一篇你會做出<b>九九乘法表</b>和<b>猜數字遊戲</b>,全部只用前面學過的東西。唯一的新東西是產生亂數的 <code>&lt;random&gt;</code>,先當成黑盒子用就好。</p>'
  '<p style="margin-bottom:0">做法是<b>由簡單到完整,一版一版長大</b>:每一版都能執行,每一版只多一點點。這也是寫真正的程式時最穩的方式。</p></div>',
  '<h3 style="margin-top:26px">複習地圖:這一篇用到哪些東西</h3>',
  table("g3", ["工具", "學於", "這一篇用在"], [
    ["變數與型態", "第 3 篇", "記住答案、猜測與次數"],
    ["<code>cin</code> / <code>cout</code>、<code>setw</code>", "第 4 篇", "讀入猜測、整齊印出乘法表"],
    ["<code>%</code> 與運算", "第 5 篇", "把亂數換算成 1 到 100"],
    ["<code>if / else if / else</code>", "第 6 篇", "判斷太大、太小、答對"],
    ["<code>for</code> / <code>while</code> / <code>break</code>", "第 7 篇", "巢狀迴圈印表、重複猜到對為止"],
  ]))

mult = section("mult", "作品一:九九乘法表", steps(
  step(1, "先印一個數字的乘法表",
       "先解決最小的問題:用一個 <code>for</code> 印出 3 的乘法表。",
       code("p08/m1"), term("p08/m1")),
  step(2, "加上外層迴圈,印出整張表",
       "把「3」換成會變的 <code>i</code>,外面再包一層迴圈,就得到完整的 9 × 9。用 <code>setw(4)</code> 讓數字對齊。",
       code("p08/m2"), term("p08/m2"),
       tip("這就是<b>巢狀迴圈</b>:外層 9 圈,內層每圈跑 9 遍,共 81 次。要印不同的表格,只要改內層的條件。")),
  step(3, "改成傳統的九九乘法表",
       "只改一個地方:內層的條件由 <code>j &lt;= 9</code> 改成 <code>j &lt;= i</code>,並改變輸出的格式。新增或改過的行用綠色底標出。",
       code("p08/m3", prev="p08/m2"), term("p08/m3"))
))

guess = section("guess", "作品二:猜數字遊戲",
  '<p class="sub" style="margin-bottom:16px">電腦想一個 1 到 100 的數字,你來猜,它告訴你「太大」或「太小」。我們分五版完成,每版都能執行。橘色是你要輸入的。</p>',
  steps(
  step(1, "最簡單的版本:猜一次",
       "先把答案寫死成 42(測試時答案固定,才知道程式對不對)。只問一次,先把「比較並回應」做對。",
       code("p08/g1"), term("p08/g1")),
  step(2, "猜到對為止",
       "加上 <code>while</code>:沒猜中就一直問。新增的行用綠色底標出。",
       code("p08/g2", prev="p08/g1"), term("p08/g2"),
       warn("如果有人輸入的不是數字(例如 <code>abc</code>),<code>cin</code> 會進入失敗狀態(第 4 篇),<code>guess</code> 永遠不變,這個迴圈就會停不下來。目前先假設輸入的都是數字,之後的篇章會學到更穩的處理方式。", "已知的限制")),
  step(3, "限制次數、記錄次數",
       "加上 <code>tries</code> 計數,最多猜 7 次。猜中時用 <code>break</code> 離開;迴圈結束後,如果還沒猜中,就公布答案。",
       code("p08/g3", prev="p08/g2"), term("p08/g3")),
  step(4, "把答案換成亂數",
       "答案不能每次都是 42。這裡先用<b>固定種子</b>的亂數產生器,每次執行答案都一樣,除錯很方便。下面這次的答案剛好是 13。",
       code("p08/g4", prev="p08/g3"), term("p08/g4"),
       tip("你可能注意到,上面是 6 次猜中。<b>每次猜中間的數字</b>(50、25、12……),每次都能排除一半的可能,所以 1 到 100 最多 7 次一定猜得到。這個想法叫「二分搜尋」。")),
  step(5, "最後一步:真正的隨機",
       "程式都正確之後,只要改一行,把固定種子換成 <code>random_device</code>,答案就每次不同了。",
       code("p08/g5.norun", prev="p08/g4"),
       see("這一版每次的答案都不同,所以沒有固定的輸出可以展示。自己編譯執行,多玩幾次吧!"))
))

stuck = section("stuck", "初學者最常卡住的四個地方",
  details("迴圈停不下來",
          "<p>檢查迴圈裡有沒有「讓條件改變」的動作:猜數字的迴圈要在<b>迴圈裡面</b>讀入 <code>guess</code>。如果輸入了非數字,<code>cin</code> 失敗後 <code>guess</code> 不再改變,也會造成同樣的結果。</p>"),
  details("每次執行,答案都一樣",
          "<p>這是固定種子(<code>mt19937 gen(2024)</code>)的預期行為。想要每次不同,把括號裡改成 <code>random_device{}()</code>。</p>"),
  details("乘法表的數字沒有對齊",
          "<p>忘了 <code>setw</code>,或是 <code>setw</code> 的寬度比最大的數字還小。9 × 9 = 81 有兩位數,所以至少要 <code>setw(3)</code> 才有空隙,<code>setw(4)</code> 更好看。</p>"),
  details("不知道從哪裡開始寫比較大的程式",
          "<p>照這一篇的做法:<b>先做最小的、能執行的一版</b>,確認正確,再加一個功能,再確認。每次只改一點點,出錯時就只需要檢查剛剛改的那幾行。</p>"))

QUIZ = quiz_cfg([
  ("<code>gen() % 100 + 1</code> 產生的數字範圍是?", ["1 到 100", "0 到 100", "1 到 99"], 0, "% 100 得到 0 到 99,再加 1 就是 1 到 100。"),
  ("為什麼先把答案寫死成 42,最後才換成亂數?", ["測試時結果固定,才知道程式對不對", "亂數比較慢", "編譯器要求這樣"], 0, "答案固定,每次輸入的結果就能預期;程式都正確了再換成亂數。"),
  ("猜對時,用什麼立刻離開 <code>while</code> 迴圈?", ["break", "continue", "return 1"], 0, "break 立刻結束整個迴圈。"),
  ("<code>mt19937 gen(2024);</code> 之後,每次執行程式,產生的亂數會?", ["每次都一樣", "每次都不同", "越來越大"], 0, "種子固定,產生的序列就固定。想要不同,種子要不同。"),
  ("乘法表的內層條件從 <code>j &lt;= 9</code> 改成 <code>j &lt;= i</code>,會怎樣?", ["第 i 列只印 i 個,變成三角形", "整張表印兩次", "編譯失敗"], 0, "內層圈數跟著外層的 i 變,第 i 列就只有 i 個。"),
])

practice = section("practice", "動手演練:延伸這兩個作品",
  '<p class="sub" style="margin-bottom:18px">每題先自己寫,再展開看參考解答。</p>',
  exercise(1, "指定數字的乘法表", "讓使用者輸入一個數字 <code>n</code>,印出 n 的乘法表(例如輸入 7)。", "p08/x1"),
  exercise(2, "加上範圍檢查的猜數字", "先讓使用者輸入最大範圍,答案固定為 7。如果猜的數字不在 1 到範圍之間,印出「超出範圍了」;猜中時,印出總共猜了幾次。", "p08/x2",
           note="先檢查範圍,再用 <code>else if</code> 比較大小。注意迴圈條件仍然是 <code>guess != answer</code>。"),
  exercise(3, "數字統計", "不斷讀入正整數,輸入 0 結束。最後印出共輸入幾個數字、最大的是哪一個。", "p08/x3",
           note="用一個變數 <code>maxValue</code> 記住目前最大的數字,每讀入一個就比較一次。這種「邊讀邊記錄」的做法非常常見。"),
  QUIZ_HTML,
  chk(["我能用巢狀迴圈印出整齊的九九乘法表。", "我知道寫比較大的程式要「先做最小的能執行版本,再一次加一點」。",
       "我能用 <code>while</code> 加 <code>break</code> 做出會重複猜的遊戲。", "我知道固定種子的亂數每次結果相同,方便除錯。",
       "我知道輸入非數字會讓 <code>cin</code> 失敗,可能造成無窮迴圈。", "我完成了至少一題延伸練習。"]),
  links([("https://en.cppreference.com/cpp/numeric/random", "cppreference:亂數函式庫", "cppreference.com"),
         ("https://en.cppreference.com/cpp/numeric/random/mersenne_twister_engine", "cppreference:mt19937", "cppreference.com")]))

SPEC = spec(
  file="clang-practice1-guide.html",
  title="綜合演練一:用前七篇的語法做出乘法表與猜數字",
  eyebrow="第 8 篇 · 綜合演練一",
  h1="用前七篇的語法,就能做出兩個完整的小遊戲",
  sub="不學新語法,只把變數、輸入輸出、運算、條件與迴圈組合起來:一版一版做出九九乘法表和猜數字遊戲。",
  tldr="大程式要<strong>從最小的、能執行的一版開始,每次只加一點</strong>。九九乘法表是巢狀迴圈加 <code>setw</code>;猜數字是 <code>while</code>、<code>if</code> 與 <code>break</code>。測試時先固定答案,正確了再換成亂數。",
  toc=[("what", "複習地圖"), ("mult", "乘法表"), ("guess", "猜數字"), ("stuck", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, mult, guess, stuck, practice]),
  config=dict(quiz=QUIZ),
  **nav(8),
)
