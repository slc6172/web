from ch import *
STP = {}

what = section("what", "運算式:把數字和運算子組合成一個值",
  '<div class="panel"><h3>像數學課的算式,但有幾個「電腦脾氣」</h3>'
  '<p><code>17 / 5</code>、<code>a &gt; b</code>、<code>x += 3</code> 都是<b>運算式</b>:每個運算式算完都會得到一個<b>值</b>。運算子負責運算,被運算的數字或變數叫<b>運算元</b>。</p>'
  '<p style="margin-bottom:0">C++ 的運算和數學幾乎一樣,只有幾個地方要特別小心:<b>整數除法會捨去小數</b>、<b>比較與邏輯的結果是 1 或 0</b>、<b>優先序</b>決定先算哪一個。</p></div>',
  '<h3 style="margin-top:26px">六個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["運算子", "代表一種運算的符號,例如 <code>+</code>、<code>&gt;</code>、<code>&amp;&amp;</code>。"],
    ["運算元", "被運算的對象。<code>3 + 4</code> 裡的 3 與 4。"],
    ["運算式", "運算子與運算元組成、能算出一個值的式子。"],
    ["優先序", "同一個式子裡,哪個運算先做。乘除比加減優先,括號最優先。"],
    ["整數除法", "兩邊都是整數的除法,結果是整數,小數部分被捨去。"],
    ["取餘數 <code>%</code>", "整數相除剩下的餘數,例如 <code>17 % 5</code> 是 2。"],
  ]))

mapsec = section("map", "全貌:五類運算子",
  table("g3b", ["種類", "運算子", "例子與結果"], [
    ["算術", "<code>+ - * / %</code>", "<code>17 / 5</code> 得 <code>3</code>;<code>17 % 5</code> 得 <code>2</code>"],
    ["比較", "<code>== != &lt; &gt; &lt;= &gt;=</code>", "<code>17 &gt; 5</code> 得 <code>1</code>(true);<code>17 == 5</code> 得 <code>0</code>(false)"],
    ["邏輯", "<code>&amp;&amp; || !</code>", "<code>1 &amp;&amp; 0</code> 得 <code>0</code>;<code>!0</code> 得 <code>1</code>"],
    ["複合賦值", "<code>+= -= *= /= %=</code>", "<code>x += 5</code> 就是 <code>x = x + 5</code>"],
    ["遞增遞減", "<code>++ --</code>", "<code>i++</code> 就是 <code>i = i + 1</code>"],
  ]),
  '<h3 style="margin-top:26px">優先序(由先算到後算)</h3>',
  table("g2", ["順序", "運算子"], [
    ["1(最先)", "括號 <code>( )</code>"],
    ["2", "<code>!</code>、負號"],
    ["3", "<code>* / %</code>(同層由左往右)"],
    ["4", "<code>+ -</code>(同層由左往右)"],
    ["5", "<code>&lt; &gt; &lt;= &gt;=</code>"],
    ["6", "<code>== !=</code>"],
    ["7", "<code>&amp;&amp;</code>"],
    ["8(最後)", "<code>||</code>"],
  ]),
  tip("記不住也沒關係:<b>拿不準就加括號</b>。括號不會讓程式變慢,卻能讓你和讀程式的人都不用猜。"))

steps_ = section("steps", "照著做:五個步驟", steps(
  step(1, "五個算術運算",
       "先猜每一行印出什麼,再看輸出。重點在最後兩行:<code>17 / 5</code> 與 <code>17 % 5</code>。",
       code("p05/a1"), term("p05/a1"),
       see("<code>17 / 5</code> 是 <code>3</code>(不是 3.4),<code>17 % 5</code> 是 <code>2</code>。兩者合起來:<code>17 = 5 × 3 + 2</code>。")),
  step(2, "整數除法的陷阱",
       "只要兩邊<b>都是整數</b>,除法就是整數除法。想要小數,至少讓一邊變成小數。",
       code("p05/a2"), term("p05/a2"),
       warn("<code>double wrong = 7 / 2;</code> 得到 3:右邊<b>先</b>用整數除法算完,才存進 <code>double</code>。變數的型態是 double,並不能讓除法自動變成小數除法。", "最常見的錯")),
  step(3, "優先序與括號",
       "先乘除、後加減;括號最優先;同一層由左往右。",
       code("p05/a3"), term("p05/a3")),
  step(4, "比較與邏輯",
       "比較與邏輯運算的結果是 <code>bool</code>,用 <code>cout</code> 印出來是 1 或 0。第 6 篇會把它們用在條件判斷上。",
       code("p05/a4"), term("p05/a4"),
       tip("<b>一個等號是賦值,兩個等號才是比較。</b>這是初學者最常寫錯的地方之一,第 6 篇會再提醒。")),
  step(5, "複合賦值與遞增",
       "<code>x += 5</code> 是 <code>x = x + 5</code> 的簡寫。按「下一步」看 <code>x</code> 的變化。",
       stepper(STP, "compound", "p05/a5", [
         dict(l=4, v={"x": "10"}, n="x 一開始是 10。"),
         dict(l=5, v={"x": "15"}, n="x += 5:x = x + 5,所以 15。"),
         dict(l=6, v={"x": "12"}, n="x -= 3:x = x - 3,所以 12。"),
         dict(l=7, v={"x": "24"}, n="x *= 2:x = x * 2,所以 24。"),
         dict(l=8, v={"x": "4"}, n="x /= 5:x = x / 5,整數除法,24 / 5 = 4(捨去 .8)。"),
         dict(l=9, v={"x": "5"}, n="x++:x 加 1,所以 5。"),
         dict(l=10, v={"x": "5"}, o="5\n", n="印出 5。"),
       ], ["x"], {"x": "int"}),
       "<p>最後一個細節:<code>i++</code> 與 <code>++i</code> 單獨一行時沒有差別,但放在其他運算式裡就不同了。</p>",
       code("p05/a6"), term("p05/a6"),
       tip("剛開始請<b>把 <code>++</code> 單獨寫成一行</b>,不要塞在別的運算式裡,就不會踩到這個差別。"))
))

lab = section("lab", "運算式求值追蹤器",
  '<p class="sub" style="margin-bottom:14px">自己輸入運算式,看 C++ 一步一步怎麼算。橘色標記的是這一步要算的那一小段。這個追蹤器的結果,和真的 g++ 對過上千個隨機運算式,答案一致。先按「<code>-7 / 2</code>」和「<code>-7 % 3</code>」,看看負數的除法與取餘數。</p>',
  calc("eval"))

stuck = section("stuck", "初學者最常卡住的四個地方",
  details("算平均卻得到整數",
          "<p>例如總和 <code>sum = 7</code>、人數 <code>n = 2</code>,<code>double avg = sum / n;</code> 得到 3。修法:讓其中一個變成小數,例如 <code>sum / (double)n</code>,或把 <code>sum</code> 一開始就宣告成 <code>double</code>。</p>"),
  details("<code>=</code> 與 <code>==</code> 搞混",
          "<p><code>a = 5</code> 是把 5 放進 a;<code>a == 5</code> 才是問「a 是不是 5」。寫成單個 <code>=</code> 在多數情況下能編譯,但意思完全不同,而且常常不會報錯。</p>"),
  details("負數的 <code>/</code> 與 <code>%</code> 和我想的不一樣",
          "<p>C++ 的整數除法是<b>朝 0 的方向捨去</b>:<code>-7 / 2</code> 得 <code>-3</code>(不是 -4),<code>-7 % 3</code> 得 <code>-1</code>(正負號跟著左邊的數)。不確定時,到上面的追蹤器試試看。</p>"),
  details("執行時程式突然當掉,訊息像是 Floating point exception",
          "<p>多半是整數<b>除以 0</b>(或對 0 取餘數)。程式執行時才會發生,編譯器不一定攔得到。除法之前先確認除數不是 0。</p>"))

QUIZ = quiz_cfg([
  ("<code>7 / 2</code> 的結果是?", ["3", "3.5", "4"], 0, "兩邊都是整數,是整數除法,小數部分被捨去。"),
  ("<code>7 % 3</code> 的結果是?", ["1", "2", "0"], 0, "7 = 3 × 2 + 1,餘數是 1。"),
  ("<code>2 + 3 * 4</code> 的結果是?", ["14", "20", "24"], 0, "乘法優先:先算 3 * 4 = 12,再加 2 得 14。要先加就要寫 (2 + 3) * 4。"),
  ("<code>int i = 5; cout &lt;&lt; i++;</code> 印出?", ["5", "6", "4"], 0, "i++ 先使用目前的值(5),再加 1;印完之後 i 才是 6。"),
  ("<code>5 &gt; 3 &amp;&amp; 2 &gt; 4</code> 的結果是?", ["0(false)", "1(true)", "編譯錯誤"], 0, "&& 要兩邊都成立才是真;2 > 4 不成立,整個是 0。"),
  ("為什麼 <code>double avg = 7 / 2;</code> 得到 3?", ["7 / 2 先用整數除法算出 3,才存進 double", "double 不能存小數", "編譯器出錯了"], 0, "運算先於存放。右邊是兩個整數,結果就是整數 3。"),
])

practice = section("practice", "動手演練:算一算、驗證一下",
  '<p class="sub" style="margin-bottom:18px">每題先自己寫,再展開看參考解答。寫完可以用上面的追蹤器驗證你的算式。</p>',
  exercise(1, "秒數換算", "把 <code>3725</code> 秒換成「幾時幾分幾秒」。提示:用 <code>/</code> 與 <code>%</code>,一小時是 3600 秒。", "p05/x1",
           note="分鐘要先扣掉整小時:<code>total % 3600 / 60</code>;秒數是 <code>total % 60</code>。"),
  exercise(2, "判斷奇偶", "對 <code>n = 14</code> 與 <code>n = 7</code>,印出「n 是不是偶數」(1 是、0 不是)。提示:偶數除以 2 的餘數是 0。", "p05/x2"),
  exercise(3, "閏年判斷", "閏年的規則:能被 4 整除而且不能被 100 整除,<b>或者</b>能被 400 整除。對 2024、1900、2000 三個年份,印出是不是閏年(1 是、0 不是)。", "p05/x3",
           note="注意括號:<code>(…且…) 或 …</code>。把規則直接翻成 <code>&amp;&amp;</code> 與 <code>||</code> 即可。"),
  QUIZ_HTML,
  chk(["我知道兩個整數相除,結果會捨去小數。", "我會用 <code>%</code> 取餘數,並知道它只能用在整數。", "我知道乘除比加減優先,括號最優先。",
       "我知道比較與邏輯運算的結果是 1(true)或 0(false)。", "我分得出 <code>=</code>(賦值)與 <code>==</code>(比較)。",
       "我知道 <code>x += 5</code> 就是 <code>x = x + 5</code>,而且 <code>++</code> 最好單獨寫一行。"]),
  links([("https://en.cppreference.com/cpp/language/operator_precedence", "cppreference:運算子優先序", "cppreference.com"),
         ("https://en.cppreference.com/cpp/language/operator_arithmetic", "cppreference:算術運算子", "cppreference.com")]))

SPEC = spec(
  file="clang-operators-guide.html",
  title="運算子與運算式:整數除法會捨去小數,% 取餘數是你的好朋友",
  eyebrow="第 5 篇 · 運算子與運算式",
  h1="整數除法會捨去小數,<code>%</code> 取餘數是你的好朋友",
  sub="算術、比較、邏輯三類運算,加上整數除法、取餘數與優先序。最後有一個追蹤器,讓你輸入任何運算式,看 C++ 一步一步怎麼算。",
  tldr="兩個整數相除<strong>結果是整數</strong>(<code>7 / 2</code> 得 3),<code>%</code> 取餘數。乘除先於加減,括號最優先,拿不準就加括號。比較與邏輯的結果是 <strong>1(true)或 0(false)</strong>;<code>=</code> 是賦值,<code>==</code> 才是比較。",
  toc=[("what", "運算式是什麼"), ("map", "運算子總覽"), ("steps", "五個步驟"), ("lab", "求值追蹤器"), ("stuck", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, mapsec, steps_, lab, stuck, practice]),
  config=dict(stepper=STP, calc=dict(eval=dict(kind="eval", presets=["2 + 3 * 4", "-7 / 2", "-7 % 3", "(2 + 3) * 4", "10 - 2 - 3", "5 > 3 && 2 > 4", "!0 + 1", "17 % 5 == 2"])), quiz=QUIZ),
  **nav(5),
)
