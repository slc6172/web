from ch import *

what = section("what", "字串:一串排好的字元",
  '<div class="panel"><h3>字串就是「字元的陣列」,但更好用</h3>'
  '<p>第 9 篇學過陣列:一排編號的格子。<b>字串</b>也是:每一格放一個字元(<code>char</code>),可以用索引取得。差別是 <code>std::string</code> 替你包好了很多功能:取長度、接在一起、搜尋、擷取、比較。</p>'
  '<p style="margin-bottom:0">所以這一篇的重點是:<b>一個字元用單引號,一段文字用雙引號</b>;<b>字串的索引也從 0 開始</b>;<b>常用操作都是「字串名稱.功能()」</b>。</p></div>',
  '<h3 style="margin-top:26px">五個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["<code>string</code>", "放一段文字的型態,要 <code>#include &lt;string&gt;</code>。"],
    ["字元 <code>char</code>", "單一個字,用單引號,例如 <code>'A'</code>。"],
    ["子字串", "字串中連續的一小段。"],
    ["<code>string::npos</code>", "「找不到」的特殊值,<code>find</code> 找不到時回傳它。"],
    ["C 風格字串", "舊式寫法:<code>char</code> 陣列加結束記號 <code>'\\0'</code>。看得懂就好,平常用 <code>string</code>。"],
  ]))

mapsec = section("map", "全貌:常用操作對照表",
  table("g3b", ["想做的事", "寫法", "結果(以 <code>s = \"Hello\"</code>)"], [
    ["有幾個字元", "<code>s.length()</code> 或 <code>s.size()</code>", "<code>5</code>"],
    ["接在一起", "<code>s + \" C++\"</code>、<code>s += \"!\"</code>", "<code>Hello C++</code>、<code>Hello!</code>"],
    ["取第 i 個字元", "<code>s[i]</code>", "<code>s[1]</code> 是 <code>'e'</code>"],
    ["找子字串", "<code>s.find(\"ll\")</code>", "<code>2</code>(找不到是 <code>string::npos</code>)"],
    ["擷取一段", "<code>s.substr(1, 3)</code>", "<code>ell</code>"],
    ["比較", "<code>==</code>、<code>&lt;</code>", "依內容與字典順序比"],
    ["讀一整行", "<code>getline(cin, s)</code>", "含空格"],
  ]))

steps_ = section("steps", "照著做:七個步驟", steps(
  step(1, "宣告字串,取長度",
       "字串用雙引號。<code>length()</code> 與 <code>size()</code> 都是取長度,效果相同。",
       code("p10/a1"), term("p10/a1")),
  step(2, "用 + 接字串",
       "把幾個字串接成一個,<code>+=</code> 可以接在後面。",
       code("p10/a2", prev="p10/a1"), term("p10/a2"),
       warn("<code>\"Hello\" + \"C++\"</code>(兩個文字直接相加)不合法。<b>至少要有一邊是 <code>string</code> 變數</b>,例如 <code>a + \" \" + b</code>。", "注意")),
  step(3, "用索引取字元、改字元",
       "字串的索引和陣列一樣,<b>從 0 開始</b>。下面的格子是字串 <code>s = \"Hello\"</code>,點著玩;再看程式。",
       '<div style="margin-bottom:12px"><div data-mem="hello"></div></div>',
       code("p10/a3"), term("p10/a3"),
       tip("取出或修改<b>一個字元</b>用單引號 <code>'J'</code>;<b>一段文字</b>用雙引號 <code>\"Jello\"</code>。")),
  step(4, "找子字串、擷取一段",
       "<code>find</code> 回傳位置,<code>substr</code> 取出一段。找不到時要檢查 <code>string::npos</code>。",
       code("p10/a4"), term("p10/a4")),
  step(5, "比較字串",
       "<code>==</code> 比較內容是否相同,<code>&lt;</code> 依字典順序比。大小寫不同的字母,就是不同的字元。",
       code("p10/a5"), term("p10/a5")),
  step(6, "讀入整行文字",
       "<code>cin &gt;&gt;</code> 遇到空格就停,<code>getline</code> 讀整行。橘色是你要輸入的。",
       code("p10/a6"), term("p10/a6"),
       "<p>同樣輸入 <code>Mina Chen</code>,如果用 <code>cin &gt;&gt;</code>:</p>",
       code("p10/a6b", prev="p10/a6"), term("p10/a6b"),
       tip("<code>cin &gt;&gt;</code> 之後要接 <code>getline</code>,記得先 <code>cin.ignore</code>(第 4 篇的陷阱)。")),
  step(7, "中文字的長度",
       "試試看中文:",
       code("p10/a7"), term("p10/a7"),
       warn("<code>length()</code> 算的是<b>位元組</b>,不是「字」。UTF-8 編碼下,一個中文字通常佔 3 個位元組。所以處理中文時,用索引逐字拆開會把一個字切碎,英文與數字則沒有這個問題。這一篇的練習以英文為主。", "中文的特別提醒"))
))

cstr = section("cstr", "C 風格字串:看得懂就好",
  '<p class="sub" style="margin-bottom:14px">更早的 C 語言沒有 <code>string</code>。它的字串是<b>字元陣列</b>,最後多放一個看不見的結束記號 <code>\'\\0\'</code>。你會在別人的舊程式、或某些函式的參數裡看到它。</p>',
  '<div data-mem="cstr"></div>',
  code("p10/a8"), term("p10/a8"),
  tip("實務原則:<b>自己寫的程式一律用 <code>std::string</code></b>。看到 <code>char[]</code> 或 <code>char*</code>,就是 C 風格字串,知道最後有個 <code>'\\0'</code> 就夠了。"))

stuck = section("stuck", "初學者最常卡住的四個地方",
  details("<code>\"Hello\" + \"World\"</code> 編譯失敗",
          "<p>兩個雙引號的文字相加,在 C++ 裡不是字串相加。把其中一個寫成 <code>string</code> 變數,或寫 <code>string(\"Hello\") + \"World\"</code>。</p>"),
  details("<code>for (int i = 0; i &lt; s.length(); i++)</code> 出現警告",
          "<p>編譯器(開啟警告時)會提醒:<code>length()</code> 回傳的是非負的 <code>size_t</code>,而 <code>i</code> 是有號的 <code>int</code>,比較時型態不同。簡單做法:先 <code>int n = s.length();</code> 再用 <code>i &lt; n</code>。</p>"),
  details("倒著走訪時,迴圈停不下來",
          "<p>如果寫 <code>for (size_t i = s.length() - 1; i &gt;= 0; i--)</code>,<code>size_t</code> 是非負的,<code>i &gt;= 0</code> 永遠成立,<code>i</code> 減到 0 後會繞回極大的數。倒著走用 <code>int i</code>。</p>"),
  details("<code>find</code> 的結果拿來當索引卻出事",
          "<p>找不到時 <code>find</code> 回傳 <code>string::npos</code>(一個很大的數),不是 -1。用它當索引會越界。使用前先確認 <code>!= string::npos</code>。</p>"))

QUIZ = quiz_cfg([
  ("<code>string s = \"Hello\";</code>,<code>s[1]</code> 是?", ["'e'", "'H'", "'l'"], 0, "索引從 0 開始,s[0] 是 'H',s[1] 是 'e'。"),
  ("哪一個會編譯失敗?", ["<code>\"Hello\" + \"C++\"</code>", "<code>string(\"Hello\") + \"C++\"</code>", "<code>string a = \"x\"; a + \"y\"</code>"], 0, "兩個雙引號的文字不能直接用 + 相加,至少要有一邊是 string。"),
  ("<code>s.find(\"abc\")</code> 找不到時,回傳什麼?", ["string::npos", "-1", "0"], 0, "找不到時回傳特殊值 string::npos,要用它來判斷。"),
  ("要讀入含空格的一整行,用?", ["getline(cin, s)", "cin >> s", "cin.line(s)"], 0, "cin >> 遇到空格就停;getline 讀到換行。"),
  ("<code>string t = \"你好\"; t.length()</code> 在 UTF-8 下通常是?", ["6", "2", "4"], 0, "length 算位元組,一個中文字通常佔 3 個位元組。"),
])

practice = section("practice", "動手演練:處理文字",
  '<p class="sub" style="margin-bottom:18px">每題先自己寫,再展開看參考解答。</p>',
  exercise(1, "數母音", "字串 <code>\"programming language\"</code>,數出裡面有幾個母音字母(a、e、i、o、u)。提示:範圍 <code>for</code> 逐個字元,用 <code>||</code> 合併條件。", "p10/x1"),
  exercise(2, "回文判斷", "回文是正著讀、反著讀都一樣的字,例如 <code>level</code>。判斷 <code>\"level\"</code> 與 <code>\"hello\"</code>。提示:比較第 i 個與倒數第 i 個字元,只需要比到一半。", "p10/x2",
           note="任何一組不相同,就設 <code>same = false</code> 並 <code>break</code>。第 7 篇練習 3 的旗標做法。"),
  exercise(3, "字串反轉", "把 <code>\"Hello\"</code> 反過來,存成新字串 <code>r</code> 再印出(應該是 <code>olleH</code>)。提示:迴圈由最後一個字元倒數到第一個,用 <code>+=</code> 加進去。", "p10/x3"),
  QUIZ_HTML,
  chk(["我知道字元用單引號、文字用雙引號。", "我會用 <code>length()</code>、<code>+</code>、<code>[]</code>、<code>find</code>、<code>substr</code>。",
       "我知道 <code>find</code> 找不到時要用 <code>string::npos</code> 判斷。", "我分得出 <code>cin &gt;&gt;</code> 與 <code>getline</code> 的差別。",
       "我知道中文字在 UTF-8 下 <code>length()</code> 會算成位元組。", "我看得懂 C 風格字串結尾有個 <code>'\\0'</code>。"]),
  links([("https://en.cppreference.com/cpp/string/basic_string", "cppreference:std::string", "cppreference.com"),
         ("https://en.cppreference.com/cpp/string/basic_string/find", "cppreference:string::find", "cppreference.com")]))

SPEC = spec(
  file="clang-string-guide.html",
  title="字串:用 std::string 處理文字,C 字串只需要認得",
  eyebrow="第 10 篇 · 字串",
  h1="用 <code>std::string</code> 處理文字,C 字串只需要認得",
  sub="學會文字處理的基本功:長度、串接、取字元、搜尋、擷取、比較與讀入一整行,並認識舊式 C 字串。",
  tldr="<code>string</code> 的索引也<strong>從 0 開始</strong>;<strong>一個字元用單引號,一段文字用雙引號</strong>。常用:<code>length()</code>、<code>+</code>、<code>find</code>(找不到是 <code>string::npos</code>)、<code>substr</code>、<code>getline</code>。中文字 <code>length()</code> 算的是位元組。",
  toc=[("what", "字串是什麼"), ("map", "操作對照表"), ("steps", "七個步驟"), ("cstr", "C 風格字串"), ("stuck", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, mapsec, steps_, cstr, stuck, practice]),
  config=dict(memory=dict(
      hello=dict(name="s", chars=True, values=["H", "e", "l", "l", "o"], ghost=2),
      cstr=dict(name="word", chars=True, values=["H", "i", "!", "\\0"], ghost=1)), quiz=QUIZ),
  **nav(10),
)
