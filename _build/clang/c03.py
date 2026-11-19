from ch import *
STP = {}

what = section("what", "變數是貼了標籤的盒子",
  '<div class="panel"><h3>用「貼了標籤的盒子」來想</h3>'
  '<p>程式需要記住東西:你的年齡、一個分數、計算到一半的結果。<b>變數</b>就是一個取了名字的盒子,把資料放進去,之後用名字就能取出來、也能換成別的值。</p>'
  '<p style="margin-bottom:0">每個盒子有固定的<b>型態</b>:它決定盒子裡能放什麼(整數?小數?文字?)、以及盒子有多大。型態一旦決定就不能變,所以選對型態是第一個重點。</p></div>',
  '<h3 style="margin-top:26px">六個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["變數", "有名字的儲存空間,裡面的值可以改變。"],
    ["型態", "規定這個變數能放哪一類資料,例如整數 <code>int</code>。"],
    ["宣告", "告訴編譯器「我要一個什麼型態、叫什麼名字的變數」。"],
    ["初始化", "宣告的同時放入第一個值,例如 <code>int age = 18;</code>。"],
    ["賦值", "把新的值放進已經存在的變數,例如 <code>age = 19;</code>。"],
    ["常數", "宣告時放進值、之後不准再改的變數,用 <code>const</code>。"],
  ]))

types = section("types", "四種最常用的基本型態",
  '<p class="sub" style="margin-bottom:16px">先記這四個,九成的入門程式都用得上。文字(很多個字)要用 <code>string</code>,第 10 篇再學。</p>',
  table("g3", ["型態", "用來裝", "範例"], [
    ["<code>int</code>", "整數(沒有小數點)", "<code>42</code>、<code>-7</code>、<code>0</code>"],
    ["<code>double</code>", "有小數點的數字", "<code>3.14</code>、<code>170.5</code>"],
    ["<code>char</code>", "單一個字元,用<b>單引號</b>", "<code>'A'</code>、<code>'7'</code>"],
    ["<code>bool</code>", "真或假,只有兩種值", "<code>true</code>、<code>false</code>"],
  ]))

steps_ = section("steps", "照著做:五個步驟", steps(
  step(1, "宣告第一個變數",
       "格式是<b>型態 名字 = 值;</b>。下面這行同時做了三件事:決定型態 <code>int</code>、取名字 <code>age</code>、放入第一個值 <code>18</code>。",
       code("p03/a1"), term("p03/a1"),
       tip("變數名稱只能用英文字母、數字、底線,<b>不能用數字開頭</b>,而且大小寫不同(<code>age</code> 與 <code>Age</code> 是兩個變數)。取一個看得出用途的名字,比 <code>a</code>、<code>x</code> 好讀得多。")),
  step(2, "四種基本型態一次看",
       "新增的行用綠色底標出來。點有 ⓘ 的行看說明。",
       code("p03/a2", prev="p03/a1"), term("p03/a2"),
       see("<code>及格:1</code>——<code>bool</code> 用 <code>cout</code> 印出來是 <code>1</code>(true)或 <code>0</code>(false),不是英文字。")),
  step(3, "改變變數的值:賦值",
       "變數的重點就是「值可以換」。按「下一步」,看 <code>age</code> 這個盒子在每一行之後裝了什麼。",
       stepper(STP, "assign", "p03/a3", [
         dict(l=4, v={"age": "18"}, n="宣告 age 並放入 18:盒子出現了。"),
         dict(l=5, v={"age": "18"}, o="18\n", n="印出 age 目前的值:18。"),
         dict(l=6, v={"age": "19"}, n="賦值:盒子裡的 18 被換成 19。這裡不用再寫 int,因為 age 已經宣告過了。"),
         dict(l=7, v={"age": "19"}, o="19\n", n="印出 19。"),
         dict(l=8, v={"age": "20"}, n="先算等號右邊:age + 1 = 20,再把結果放回 age。「=」是「放進去」,不是數學的「相等」。"),
         dict(l=9, v={"age": "20"}, o="20\n", n="印出 20。"),
         dict(l=10, v={"age": "20"}, n="return 0:程式結束。"),
       ], ["age"], {"age": "int"}),
       warn("<code>int age = 18;</code> 是<b>宣告加初始化</b>,只能對同一個名字做一次;後面要改值,只寫 <code>age = 19;</code>。重複寫 <code>int age</code> 會編譯失敗。", "注意")),
  step(4, "型態不同,存的東西就不同",
       "盒子的型態決定了它怎麼處理放進來的值。先猜猜每一行會印什麼,再看輸出。",
       code("p03/a3b"), term("p03/a3b"),
       warn("把 <code>3.9</code> 存進 <code>int</code>,得到 <code>3</code>:小數部分是<b>直接捨去</b>,不是四捨五入。需要小數就用 <code>double</code>。", "注意")),
  step(5, "常數與 auto",
       "<code>const</code> 讓值鎖死,避免不小心改到(例如圓周率);<code>auto</code> 讓編譯器看右邊的值自己決定型態。",
       code("p03/a4"), term("p03/a4"),
       "<p>試著改動常數,看編譯器怎麼說:</p>",
       code("p03/e1.err", prev="p03/a4"), errterm("p03/e1.err"),
       see("<code>assignment of read-only variable ‘PI’</code>:你想改一個唯讀(<code>const</code>)的變數。這個錯誤正是 <code>const</code> 的用意:在編譯時就攔下來。"),
       tip("常數的名稱習慣全部大寫,看到大寫名字就知道「這個不能改」。"))
))

size = section("size", "型態有大小,也有上限:溢位",
  '<p class="sub" style="margin-bottom:16px">盒子的大小用「位元組(byte)」計算。盒子越小,能裝的範圍越小。下面是在常見電腦上的實測。</p>',
  code("p03/s1"), term("p03/s1"),
  table("g3b", ["型態", "大小(位元組)", "能裝多大"], [
    ["<code>char</code>", "1", "單一字元;有號版本約 −128 ~ 127"],
    ["<code>bool</code>", "1", "<code>true</code> / <code>false</code>"],
    ["<code>short</code>", "2", "−32,768 ~ 32,767"],
    ["<code>int</code>", "4", "−2,147,483,648 ~ 2,147,483,647(約 ±21 億)"],
    ["<code>long long</code>", "8", "約 ±9.2 × 10<sup>18</sup>"],
    ["<code>float</code>", "4", "小數,約 7 位有效數字"],
    ["<code>double</code>", "8", "小數,約 15 位有效數字"],
  ]),
  '<p class="mock-cap" style="margin-top:10px">大小可能因電腦與編譯器而不同,以上是最常見的 64 位元環境。</p>',
  '<h3 style="margin-top:26px">親手把盒子「撐爆」看看</h3>'
  '<p class="sub" style="margin-bottom:14px">選一個型態、輸入一個整數,看它存進去之後變成多少。先按預設的「int 最大值 + 1」。</p>',
  calc("overflow"),
  '<h3 style="margin-top:26px">真的在程式裡發生一次</h3>',
  code("p03/o1"), term("p03/o1"),
  warn("<b>有號整數(<code>int</code>)溢位在 C++ 標準裡是「未定義行為」</b>:程式不保證怎麼動。上面的 <code>-2147483648</code> 只是常見電腦上的結果,不能依賴它。實務上的做法是:數字可能很大時,改用 <code>long long</code>。", "重要"))

stuck = section("stuck", "初學者最常卡住的四個地方",
  details("忘了給初始值,印出來是一個奇怪的數字",
          "<p><code>int x;</code> 只宣告、沒給值,裡面裝的是不確定的舊資料,直接使用會得到亂數,甚至每次執行結果不同。<b>宣告時就給初始值</b>是最好的習慣,例如 <code>int x = 0;</code>。</p>"),
  details("單引號與雙引號搞混了",
          "<p>單引號 <code>'A'</code> 是<b>一個字元</b>(<code>char</code>);雙引號 <code>\"A\"</code> 是<b>文字</b>(字串)。它們是不同的東西:<code>char c = \"A\";</code> 會編譯失敗。<code>cout &lt;&lt; \"Hello\"</code> 印的是文字,所以用雙引號。</p>"),
  details("<code>int</code> 存了小數,結果不對",
          "<p>要存小數就用 <code>double</code>。用 <code>int</code> 存 <code>3.9</code> 得到 <code>3</code>,而且編譯器通常不會警告你。</p>"),
  details("變數名稱被編譯器拒絕",
          "<p>檢查三件事:是不是數字開頭、有沒有空格或符號(如 <code>-</code>)、是不是用了 C++ 的保留字(例如 <code>int</code>、<code>return</code>)當名字。</p>"))

QUIZ = quiz_cfg([
  ("<code>int age = 18.9;</code> 之後,<code>age</code> 裡裝的是?", ["18", "19", "18.9"], 0,
   "int 只能存整數,小數部分會被直接捨去,不是四捨五入。"),
  ("哪一個會編譯失敗?", ["const int N = 5; N = 6;", "int n = 5; n = 6;", "double d = 5;"], 0,
   "const 宣告的變數不能再被賦值。其他兩個都合法。"),
  ("<code>char c = 'A'; cout &lt;&lt; c + 1;</code> 會印出?", ["66", "B", "A1"], 0,
   "字元是小整數('A' 的編碼是 65),c + 1 是整數運算,結果是 66。"),
  ("<code>bool ok = true; cout &lt;&lt; ok;</code> 印出?", ["1", "true", "T"], 0,
   "bool 預設印成數字:true 是 1,false 是 0。"),
  ("<code>unsigned int</code> 已經是最大值 4294967295,再加 1 會?", ["繞回 0", "變成 4294967296", "編譯失敗"], 0,
   "unsigned 超過上限會繞回 0,這是 C++ 明確規定的行為。"),
])

practice = section("practice", "動手演練:自己宣告、自己改",
  '<p class="sub" style="margin-bottom:18px">每題先自己寫,再展開看參考解答。記得每次改完都要重新編譯。</p>',
  exercise(1, "我的資料卡", "宣告四個變數:年齡(<code>int</code>)、身高(<code>double</code>)、名字縮寫(<code>char</code>)、是不是學生(<code>bool</code>),用 <code>cout</code> 各印一行,前面加上說明文字。", "p03/x1"),
  exercise(2, "交換兩個變數", "有 <code>a = 3</code>、<code>b = 5</code>。不能直接 <code>a = b; b = a;</code>(想想為什麼),請借助第三個變數,讓兩者的值互換,並印出交換前後。", "p03/x2",
           note="先把 a 的值存到 temp,a 才能被覆蓋;最後把 temp 放進 b。像兩杯飲料要換,中間需要一個空杯。"),
  exercise(3, "圓面積", "用常數 <code>PI = 3.14159</code> 與 <code>double r = 5</code>,算出圓面積(<code>PI * r * r</code>)並印出。", "p03/x3",
           note="<code>cout</code> 預設最多顯示 6 位有效數字,所以結果看起來被「四捨五入」了。第 4 篇會學怎麼控制小數位數。"),
  QUIZ_HTML,
  chk(["我能說出變數、型態、宣告、初始化、賦值的差別。", "我會寫 <code>int</code>、<code>double</code>、<code>char</code>、<code>bool</code> 的宣告並給初始值。",
       "我知道把小數存進 <code>int</code> 會被捨去。", "我知道 <code>const</code> 的值不能再改,改了會編譯失敗。",
       "我知道 <code>int</code> 有上限,超過會出問題,數字很大時要用 <code>long long</code>。", "我分得出單引號 <code>'A'</code> 與雙引號 <code>\"A\"</code> 的不同。"]),
  links([("https://en.cppreference.com/cpp/language/types", "cppreference:基本型態", "cppreference.com"),
         ("https://en.cppreference.com/cpp/language/cv", "cppreference:const 限定詞", "cppreference.com")]))

SPEC = spec(
  file="clang-variables-guide.html",
  title="變數與資料型態:型態決定盒子裝什麼、裝多大",
  eyebrow="第 3 篇 · 變數與資料型態",
  h1="變數是有名字、有型態的盒子,型態決定裝得下什麼、裝多大",
  sub="學會宣告變數、換掉它的值、用 <code>const</code> 鎖住它,並親手把一個盒子「撐爆」,看溢位是怎麼回事。",
  tldr="四個基本型態:<code>int</code> 整數、<code>double</code> 小數、<code>char</code> 字元、<code>bool</code> 真假。宣告時就給初始值,<strong>型態決定能裝的範圍</strong>:<code>int</code> 存小數會被捨去、超過上限會溢位。不想被改的值用 <code>const</code>。",
  toc=[("what", "變數是什麼"), ("types", "四種型態"), ("steps", "五個步驟"), ("size", "大小與溢位"), ("stuck", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, types, steps_, size, stuck, practice]),
  config=dict(stepper=STP, calc=dict(overflow=dict(kind="overflow")), quiz=QUIZ),
  **nav(3),
)
