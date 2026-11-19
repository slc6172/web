from ch import *
STP = {}

# 追蹤:int sum = 0; for (int i = 1; i <= 4; i++) sum += i;  (行號為 0 起算,對應 p07/a2)
def sum_trace():
    st = [dict(l=4, v={"sum": "0"}, n="sum 一開始是 0。")]
    sm, i = 0, 1
    st.append(dict(l=5, v={"i": "1", "sum": "0"}, n="迴圈開始:先做起點 i = 1,再檢查 i <= 4,成立,進入主體。"))
    while i <= 4:
        sm += i
        st.append(dict(l=6, v={"i": str(i), "sum": str(sm)}, n="主體:sum += %d,sum 變成 %d。" % (i, sm)))
        i += 1
        if i <= 4:
            st.append(dict(l=5, v={"i": str(i), "sum": str(sm)}, n="這一圈結束:i++ 讓 i 變成 %d,再檢查 i <= 4,成立,再來一圈。" % i))
        else:
            st.append(dict(l=5, v={"i": str(i), "sum": str(sm)}, n="i++ 讓 i 變成 5,檢查 i <= 4,不成立,離開迴圈。"))
    st.append(dict(l=8, v={"sum": str(sm)}, o="%d\n" % sm, n="印出 sum。注意 i 的盒子不見了:它是在 for 裡宣告的,只在迴圈裡有效。"))
    return st

what = section("what", "迴圈:讓同一件事重複做",
  '<div class="panel"><h3>像跑操場,跑到指定圈數就停</h3>'
  '<p>要印 100 次「你好」,不會真的寫 100 行。<b>迴圈</b>讓同一段程式重複執行,直到<b>條件不成立</b>為止。每重複一次叫一「圈」(iteration)。</p>'
  '<p style="margin-bottom:0">所有迴圈都有三個要素:<b>起點</b>、<b>繼續的條件</b>、<b>每圈後的變化</b>。少了其中任何一個,就可能停不下來。</p></div>',
  '<h3 style="margin-top:26px">六個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["迴圈", "重複執行一段程式的結構。"],
    ["迴圈變數", "控制迴圈的變數,常叫 <code>i</code>。"],
    ["迴圈主體", "大括號裡每圈都會做的事。"],
    ["<code>break</code>", "立刻離開整個迴圈。"],
    ["<code>continue</code>", "跳過這一圈剩下的內容,直接進入下一圈。"],
    ["巢狀迴圈", "迴圈裡面還有迴圈。"],
  ]))

mapsec = section("map", "全貌:三種迴圈怎麼選",
  table("g3b", ["迴圈", "什麼時候用", "特點"], [
    ["<code>for</code>", "知道要跑幾圈", "起點、條件、變化都寫在同一行,最不容易漏。"],
    ["<code>while</code>", "不知道要跑幾圈,只知道「什麼時候停」", "每圈開始前先檢查,可能一圈都不跑。"],
    ["<code>do-while</code>", "至少要做一次,例如先輸入再檢查", "每圈結束後才檢查,所以至少執行一次。"],
  ]),
  tip("三種迴圈能互相改寫。初學時的簡單原則:<b>數得出圈數就用 <code>for</code>,數不出就用 <code>while</code></b>。"))

steps_ = section("steps", "照著做:六個步驟", steps(
  step(1, "for:數著圈數跑",
       "<code>for</code> 的括號裡有三部分,用分號隔開。點 ⓘ 看每一部分的作用。",
       code("p07/a1"), term("p07/a1"),
       see("<code>i</code> 從 1 開始,每圈結束後 <code>i++</code>,只要 <code>i &lt;= 5</code> 就繼續,所以印出 1 到 5。")),
  step(2, "用迴圈累加",
       "把 1 加到 4。按「下一步」,一格一格看 <code>i</code> 與 <code>sum</code> 的變化,特別注意<b>檢查條件那一步</b>。",
       stepper(STP, "sumloop", "p07/a2", sum_trace(), ["i", "sum"], {"i": "int", "sum": "int"}),
       tip("累加的固定寫法:<b>先把累加變數設成 0,再在迴圈裡一直加上去</b>。累加變數要放在迴圈外面宣告,否則每圈都會重新歸零。")),
  step(3, "while:不知道要跑幾圈",
       "使用者想輸入幾個數字都可以,輸入 0 才結束。橘色是你要輸入的。",
       code("p07/a3"), term("p07/a3"),
       warn("<code>while</code> 的主體裡<b>一定要有讓條件改變的動作</b>(這裡是 <code>cin &gt;&gt; n</code>)。忘了的話,條件永遠成立,迴圈會停不下來。", "注意")),
  step(4, "do-while:至少做一次",
       "先要求輸入,再檢查輸入合不合理,不合理就再問。這種「先做再檢查」最適合 <code>do-while</code>。",
       code("p07/a4"), term("p07/a4")),
  step(5, "break 與 continue",
       "<code>continue</code> 略過這一圈剩下的部分;<code>break</code> 直接結束整個迴圈。先猜會印出什麼。",
       code("p07/a5"), term("p07/a5"),
       see("偶數被 <code>continue</code> 略過;<code>i</code> 到 9 時 <code>i &gt; 7</code> 成立,<code>break</code> 結束迴圈,所以只印到 7。")),
  step(6, "巢狀迴圈:迴圈裡的迴圈",
       "外層控制列,內層控制欄。<b>外層跑一圈,內層就從頭完整跑一遍。</b>",
       code("p07/a6"), term("p07/a6"),
       tip("巢狀迴圈的總次數是「外層圈數 × 內層圈數」:這裡是 3 × 3 = 9 次。")),
))

lab = section("lab", "迴圈追蹤表:自己改改看",
  '<p class="sub" style="margin-bottom:14px">改起點、終點和每圈的變化,看會跑幾圈。<b>試試這三個按鈕</b>:「少一圈」(<code>&lt;</code> 與 <code>&lt;=</code> 的差別,也就是差一錯誤)、「停不下來」(無窮迴圈長什麼樣)、「一圈都不跑」。這個模擬和真的 g++ 對過數百組設定,結果一致。</p>',
  calc("loop"))

pitfall = section("pitfall", "兩個一定會遇到的錯誤",
  '<h3>差一錯誤(off-by-one)</h3>'
  '<p class="why">要跑 5 圈,到底寫 <code>&lt; 5</code> 還是 <code>&lt;= 5</code>?差一個等號,多一圈或少一圈。從 0 開始數時用 <code>&lt;</code>,從 1 開始數時用 <code>&lt;=</code>。</p>',
  code("p07/a7"), term("p07/a7"),
  '<h3 style="margin-top:28px">無窮迴圈</h3>'
  '<p class="why">條件永遠成立,迴圈永遠不會結束。例如 <code>for (int i = 1; i &lt;= 5; i--)</code>:i 越減越小,永遠 <code>&lt;= 5</code>。上面的追蹤表按「停不下來」就能看到。</p>'
  + tip("程式停不下來時,在終端機按 <b>Ctrl + C</b> 強制中止。線上編譯器則是按它的 Stop 按鈕。"))

stuck = section("stuck", "初學者最常卡住的三個地方",
  details("迴圈跑完後,想用 <code>i</code> 卻編譯失敗",
          "<p>在 <code>for (int i = …)</code> 裡宣告的 <code>i</code> 只在迴圈裡有效,離開就消失了(第 2 步的追蹤表可以看到)。要在迴圈外使用,就把 <code>int i;</code> 宣告在迴圈外面。</p>"),
  details("累加的結果永遠是最後一個數字",
          "<p>多半是把 <code>sum</code> 的宣告放進迴圈裡了,每圈都重新歸零。或是寫成 <code>sum = i</code> 而不是 <code>sum += i</code>。</p>"),
  details("<code>for</code> 的括號後面多寫了分號",
          "<p><code>for (int i = 1; i &lt;= 5; i++);</code> 後面的分號讓迴圈主體變成「什麼都不做」,大括號的內容只會在迴圈結束後執行一次。<code>while</code> 也一樣,只有 <code>do-while</code> 結尾才需要分號。</p>"))

QUIZ = quiz_cfg([
  ("<code>for (int i = 0; i &lt; 5; i++)</code> 主體會執行幾次?", ["5 次", "4 次", "6 次"], 0, "i 依序是 0、1、2、3、4,共 5 圈;i = 5 時條件不成立,離開。"),
  ("<code>do-while</code> 與 <code>while</code> 最大的差別是?", ["do-while 至少會執行一次", "do-while 比較快", "do-while 不能用 break"], 0, "do-while 先做主體,再檢查條件。"),
  ("<code>continue</code> 的作用是?", ["跳過這一圈剩下的內容,進入下一圈", "結束整個迴圈", "回到程式開頭"], 0, "continue 只影響這一圈;結束整個迴圈的是 break。"),
  ("下面哪個迴圈會停不下來?", ["<code>for (int i = 1; i &lt;= 5; i--)</code>", "<code>for (int i = 1; i &lt;= 5; i++)</code>", "<code>for (int i = 5; i &gt; 0; i--)</code>"], 0, "i 越減越小,永遠 <= 5。"),
  ("外層迴圈 3 圈、內層迴圈 4 圈,內層主體總共執行幾次?", ["12 次", "7 次", "4 次"], 0, "外層每一圈,內層都完整跑 4 圈,共 3 × 4 = 12。"),
])

practice = section("practice", "動手演練:讓電腦替你重複",
  '<p class="sub" style="margin-bottom:18px">每題先自己寫,再展開看參考解答。</p>',
  exercise(1, "1 加到 100", "用 <code>for</code> 算出 1 + 2 + … + 100。(據說高斯小時候一下子就算出來了:答案是 5050。)", "p07/x1"),
  exercise(2, "星號三角形", "印出四列:第 1 列 1 個星號,第 2 列 2 個,依此類推到 4 個。提示:巢狀迴圈,內層的圈數跟著外層的 <code>i</code> 變。", "p07/x2",
           note="內層的條件是 <code>j &lt;= i</code>,所以第 i 列剛好印 i 個星號;每列結束再印一個換行。"),
  exercise(3, "質數判斷", "讀入一個大於 1 的整數 <code>n</code>,判斷它是不是質數。提示:從 2 試到 <code>n - 1</code>,只要有一個能整除就不是質數,可以用 <code>break</code> 提早結束。", "p07/x3",
           note="可以再輸入 21、2、97 試試。進階想法:其實只需要試到 √n,有興趣可以自己改改看。"),
  QUIZ_HTML,
  chk(["我知道 <code>for</code> 括號裡的三個部分各是什麼。", "我會用迴圈做累加,並知道累加變數要放在迴圈外面。",
       "我能分辨什麼時候用 <code>for</code>、<code>while</code>、<code>do-while</code>。", "我知道 <code>break</code> 與 <code>continue</code> 的差別。",
       "我會預防差一錯誤與無窮迴圈。", "我能算出巢狀迴圈主體的總次數。"]),
  links([("https://en.cppreference.com/cpp/language/for", "cppreference:for 迴圈", "cppreference.com"),
         ("https://en.cppreference.com/cpp/language/while", "cppreference:while 迴圈", "cppreference.com")]))

SPEC = spec(
  file="clang-loops-guide.html",
  title="迴圈:把同一件事做 N 次,小心差一錯誤",
  eyebrow="第 7 篇 · 迴圈",
  h1="迴圈就是把同一件事做 N 次,小心差一錯誤",
  sub="學會 <code>for</code>、<code>while</code>、<code>do-while</code>、<code>break</code>、<code>continue</code> 與巢狀迴圈,並用追蹤表親眼看每一圈的變數怎麼變。",
  tldr="迴圈需要<strong>起點、條件、每圈的變化</strong>。數得出圈數用 <code>for</code>,數不出用 <code>while</code>,至少做一次用 <code>do-while</code>。<code>break</code> 離開整個迴圈,<code>continue</code> 只跳過這一圈。兩大錯誤:<strong>差一錯誤</strong>與<strong>無窮迴圈</strong>。",
  toc=[("what", "迴圈是什麼"), ("map", "三種迴圈"), ("steps", "六個步驟"), ("lab", "追蹤表"), ("pitfall", "兩個錯誤"), ("stuck", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, mapsec, steps_, lab, pitfall, stuck, practice]),
  config=dict(stepper=STP, calc=dict(loop=dict(kind="loop", presets=[
      ["1 到 5", 1, "<=", 5, 1], ["少一圈(i < 5)", 1, "<", 5, 1], ["每次加 2", 1, "<=", 10, 2], ["倒數 10 到 1", 10, ">=", 1, -1],
      ["停不下來", 1, "<=", 5, -1], ["一圈都不跑", 6, "<=", 5, 1]])), quiz=QUIZ),
  **nav(7),
)
