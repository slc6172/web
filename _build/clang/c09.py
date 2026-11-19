from ch import *

what = section("what", "陣列:一排有編號的盒子",
  '<div class="panel"><h3>像一排編了號的置物櫃</h3>'
  '<p>要記 5 個人的成績,不會宣告 <code>score1</code>、<code>score2</code>……五個變數。<b>陣列</b>讓你用一個名字,放下一整排同型態的資料,再用<b>編號(索引)</b>取出其中一個。</p>'
  '<p style="margin-bottom:0">最重要的一件事:<b>編號從 0 開始</b>。5 個元素的編號是 0、1、2、3、4,<b>沒有 5</b>。這是 C++ 初學者最常被咬到的地方。</p></div>',
  '<h3 style="margin-top:26px">六個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["元素", "陣列裡的每一格資料。"],
    ["索引(index)", "元素的編號,從 0 開始。寫在方括號裡,例如 <code>scores[2]</code>。"],
    ["長度", "陣列有幾格。宣告時就固定,不能改。"],
    ["越界", "用了不存在的索引,例如長度 5 卻去讀 <code>scores[5]</code>。"],
    ["<code>vector</code>", "可以變長變短的陣列,是日常寫程式時的首選。"],
    ["範圍 <code>for</code>", "<code>for (int x : a)</code>:不用管索引,逐個取出元素。"],
  ]))

mapsec = section("map", "全貌:陣列與 vector,怎麼選",
  table("g3b", ["比較", "陣列 <code>int a[5]</code>", "<code>vector&lt;int&gt; v</code>"], [
    ["長度", "宣告時固定", "可以隨時變長、變短"],
    ["加元素", "不行", "<code>v.push_back(x)</code>"],
    ["取得長度", "自己記(或用 <code>sizeof</code> 計算)", "<code>v.size()</code>"],
    ["取值與改值", "<code>a[i]</code>", "<code>v[i]</code>,或有檢查的 <code>v.at(i)</code>"],
    ["要引入什麼", "不用", "<code>#include &lt;vector&gt;</code>"],
  ]),
  tip("<b>日常寫程式優先用 <code>vector</code></b>:不用事先決定長度、不用自己記長度、還能加減元素。陣列要先學,是因為它是 <code>vector</code> 的基礎,也常出現在別人的程式裡。"))

steps_ = section("steps", "照著做:六個步驟", steps(
  step(1, "宣告陣列,用索引取值",
       "先猜每一行印出什麼。下面的格子可以點著玩:<b>輸入索引,讀取或寫入</b>,也可以故意輸入 5 看看越界。",
       code("p09/a1"), term("p09/a1"),
       '<div style="margin-top:14px"><div data-mem="scores"></div></div>',
       see("長度是 5,合法的索引是 <b>0 到 4</b>。最後一個元素永遠是「長度 − 1」。")),
  step(2, "用迴圈走訪陣列",
       "陣列配迴圈是最常見的組合。<code>i</code> 從 0 跑到「長度 − 1」,用條件 <code>i &lt; 5</code>。",
       code("p09/a2"), term("p09/a2"),
       tip("走訪陣列的條件用 <code>i &lt; 長度</code>,<b>不是</b> <code>i &lt;= 長度</code>。這就是第 7 篇的差一錯誤,在陣列上會變成越界。")),
  step(3, "找出最大值",
       "經典的「擂台」做法:先假設第一個最大,再逐一比較,遇到更大的就換人。",
       code("p09/a3"), term("p09/a3")),
  step(4, "範圍 for:不用管索引",
       "只想「每個元素都處理一遍」,不需要知道是第幾個時,範圍 <code>for</code> 最簡單,也不可能越界。",
       code("p09/a4"), term("p09/a4")),
  step(5, "vector:會自己長大的陣列",
       "按下面的按鈕操作 <code>v</code>,看每個操作前後的內容。注意 <code>push_back</code> 會讓長度加 1,<code>v[i] = x</code> 只改那一格。",
       code("p09/a5"), term("p09/a5"),
       '<div style="margin-top:14px"><div data-ba="v"></div></div>'),
  step(6, "邊讀邊加:不知道有幾個數字",
       "陣列的長度要事先決定,<code>vector</code> 就不用:有幾個,就 <code>push_back</code> 幾個。橘色是你要輸入的。",
       code("p09/a6"), term("p09/a6"),
       "<p>最後補充二維陣列:想成一張表格,用兩個索引取值。</p>",
       code("p09/a7"), term("p09/a7"))
))

oob = section("oob", "越界:C++ 不會替你檢查",
  '<p class="why">用了不存在的索引(越界),C++ 的陣列<b>不會報錯</b>:它直接去存取那個位置的記憶體。可能讀到無關的資料,可能改壞別的變數,也可能一切看起來正常——所以最難找。上面步驟 1 的格子可以親手試試。</p>',
  '<p>想要「越界就明確報錯」,<code>vector</code> 提供了 <code>at()</code>。同樣是取第 10 個元素,對照看看:<code>v[10]</code> 是未定義行為,<code>v.at(10)</code> 則會讓程式立刻停下來並告訴你原因:</p>',
  code("p09/c1.crash"), crash("p09/c1.crash"),
  warn("程式用 <code>at()</code> 越界會「當掉」,這已經比默默出錯好太多:你馬上知道哪裡錯。除錯時可以暫時把 <code>v[i]</code> 換成 <code>v.at(i)</code> 來找問題。(例外處理第 16 篇會學,現在先認得這個訊息。)", "重要"))

stuck = section("stuck", "初學者最常卡住的四個地方",
  details("想用 <code>a[5]</code> 取最後一個元素",
          "<p>長度 5 的陣列,最後一個是 <code>a[4]</code>。可以記成:<b>長度是「幾個」,索引是「第幾個,從 0 起算」</b>。</p>"),
  details("宣告陣列時用變數當長度",
          "<p><code>int n = 5; int a[n];</code> 在標準 C++ 裡不合法(有些編譯器勉強接受,但不要依賴)。長度需要在編譯時就知道。要長度由程式決定,請用 <code>vector</code>。</p>"),
  details("忘了 <code>#include &lt;vector&gt;</code>",
          "<p>編譯器會說 <code>vector</code> 不是 <code>std</code> 的成員或沒有宣告。補上 <code>#include &lt;vector&gt;</code> 就好。</p>"),
  details("陣列沒給初始值,印出奇怪的數字",
          "<p><code>int a[5];</code> 的內容是不確定的舊資料。要全部歸零可以寫 <code>int a[5] = {};</code>;<code>vector&lt;int&gt; v(5);</code> 也會把 5 個元素都設成 0。</p>"))

QUIZ = quiz_cfg([
  ("<code>int a[5]</code> 合法的索引範圍是?", ["0 到 4", "1 到 5", "0 到 5"], 0, "索引從 0 開始,長度 5 的最後一個索引是 4。"),
  ("對長度 5 的陣列讀取 <code>a[5]</code>,會發生什麼事?", ["未定義行為:可能讀到亂資料、也可能當掉", "一定會編譯失敗", "得到 0"], 0, "C++ 陣列不檢查索引,越界是未定義行為,結果沒有保證。"),
  ("要在 <code>vector&lt;int&gt; v</code> 的最後面加一個數字,用?", ["v.push_back(x)", "v[v.size()] = x", "v.add(x)"], 0, "push_back 會讓 vector 自動變長;直接寫 v[v.size()] 是越界。"),
  ("<code>for (int x : v)</code> 的意思是?", ["對 v 裡的每一個元素,依序放進 x", "把 v 複製成 x", "從 x 找 v"], 0, "這是範圍 for,逐個取出元素。"),
  ("想讓越界時「明確報錯而不是默默出錯」,可以用?", ["v.at(i)", "v[i]", "v.size(i)"], 0, "at() 會檢查索引,越界時中止程式並說明原因。"),
])

practice = section("practice", "動手演練:陣列與 vector",
  '<p class="sub" style="margin-bottom:18px">每題先自己寫,再展開看參考解答。</p>',
  exercise(1, "總和、平均與最大值", "陣列 <code>{12, 7, 30, 4, 19, 8}</code>。用一個迴圈同時算出總和、平均與最大值。", "p09/x1",
           note="平均要用 <code>sum / 6.0</code>,才不會被整數除法捨去小數(第 5 篇)。"),
  exercise(2, "反過來印", "把 <code>{1, 2, 3, 4, 5}</code> 由最後一個印到第一個。提示:迴圈從 4 倒數到 0。", "p09/x2"),
  exercise(3, "去除重複", "<code>vector</code> 裡有 <code>{3, 1, 3, 2, 1, 4}</code>。建立另一個 vector,只放「第一次出現」的數字,最後印出 <code>3 1 2 4</code>。提示:對每個數字,先到新的 vector 裡找找看有沒有。", "p09/x3",
           note="內層迴圈用 <code>found</code> 旗標記錄「找到了沒」,找到就 <code>break</code>;沒找到才 <code>push_back</code>。這是巢狀迴圈加旗標的經典寫法。"),
  QUIZ_HTML,
  chk(["我知道陣列的索引從 0 開始,最後一個是「長度 − 1」。", "我會用 <code>for</code> 走訪陣列,條件是 <code>i &lt; 長度</code>。",
       "我知道越界不會有編譯錯誤,而且結果不可預期。", "我會用 <code>vector</code> 的 <code>push_back</code>、<code>size</code>、<code>pop_back</code>。",
       "我會用範圍 <code>for</code> 逐個處理元素。", "我知道除錯時可以用 <code>at()</code> 找出越界。"]),
  links([("https://en.cppreference.com/cpp/container/vector", "cppreference:std::vector", "cppreference.com"),
         ("https://en.cppreference.com/cpp/language/array", "cppreference:陣列", "cppreference.com")]))

SPEC = spec(
  file="clang-array-vector-guide.html",
  title="陣列與 vector:索引從 0 開始,越界不會報錯卻會出事",
  eyebrow="第 9 篇 · 陣列與 vector",
  h1="索引從 0 開始,越界不會報錯卻會出事",
  sub="用一個名字放下一整排資料。從固定長度的陣列,到會自己長大的 <code>vector</code>,並親手體驗什麼叫越界。",
  tldr="陣列用<strong>索引</strong>取值,<strong>從 0 開始</strong>,長度 N 的最後一個是 N−1。<strong>越界不會有編譯錯誤</strong>,結果不可預期。日常優先用 <code>vector</code>:<code>push_back</code> 加元素、<code>size()</code> 取長度,除錯時用 <code>at()</code> 抓越界。",
  toc=[("what", "陣列是什麼"), ("map", "陣列 vs vector"), ("steps", "六個步驟"), ("oob", "越界"), ("stuck", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, mapsec, steps_, oob, stuck, practice]),
  config=dict(memory=dict(scores=dict(name="scores", values=[80, 92, 75, 60, 88], ghost=2)), beforeafter=dict(v=dict(name="v", init=[3, 5, 8])), quiz=QUIZ),
  **nav(9),
)
