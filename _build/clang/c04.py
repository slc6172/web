from ch import *

what = section("what", "輸入輸出就是兩條水管",
  '<div class="panel"><h3>用「水管」來想</h3>'
  '<p>C++ 把輸入輸出看成<b>資料流(stream)</b>:<code>cout</code> 是通往螢幕的水管,<code>&lt;&lt;</code> 的箭頭指向螢幕;<code>cin</code> 是從鍵盤來的水管,<code>&gt;&gt;</code> 的箭頭指向<b>變數</b>。箭頭方向就是資料流動的方向。</p>'
  '<p style="margin-bottom:0">這一篇的重點只有三個:讀進來、印得漂亮、避開讀取時的坑。</p></div>',
  '<h3 style="margin-top:26px">五個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["<code>cout</code>", "標準輸出:把資料送到螢幕。"],
    ["<code>cin</code>", "標準輸入:從鍵盤讀資料,放進變數。"],
    ["<code>&lt;&lt;</code> / <code>&gt;&gt;</code>", "串流運算子。箭頭朝哪邊,資料就往哪邊流。可以接連使用。"],
    ["<code>endl</code>", "換行,並把還沒送出的輸出立刻送出去。"],
    ["緩衝區", "輸入的字會先放在一個暫存區,按 Enter 後才交給程式。許多輸入的坑都跟它有關。"],
  ]))

mapsec = section("map", "全貌:輸入輸出對照表",
  '<p class="sub" style="margin-bottom:16px">想做什麼事,就查這張表。後面的步驟會一個一個實際用到。</p>',
  table("g3b", ["想做的事", "寫法", "說明"], [
    ["印文字或變數", "<code>cout &lt;&lt; x;</code>", "可以是文字、數字、變數。"],
    ["連續印好幾樣", "<code>cout &lt;&lt; a &lt;&lt; \" \" &lt;&lt; b;</code>", "箭頭可以一直接下去。"],
    ["換行", "<code>endl</code> 或 <code>\"\\n\"</code>", "兩者都能換行。<code>endl</code> 還會立刻送出輸出。"],
    ["讀一個值", "<code>cin &gt;&gt; x;</code>", "依 <code>x</code> 的型態讀;遇到空白或換行就停。"],
    ["讀多個值", "<code>cin &gt;&gt; a &gt;&gt; b;</code>", "輸入用空格或換行隔開。"],
    ["讀一整行", "<code>getline(cin, s);</code>", "連空格一起讀,到換行為止。要 <code>#include &lt;string&gt;</code>。"],
    ["固定小數位數", "<code>fixed &lt;&lt; setprecision(2)</code>", "要 <code>#include &lt;iomanip&gt;</code>。"],
    ["對齊寬度", "<code>setw(8)</code>", "下一個輸出至少佔 8 格,只影響緊接著的一個。"],
  ]))

steps_ = section("steps", "照著做:三個步驟", steps(
  step(1, "讀進一個數字",
       "先印提示,再用 <code>cin</code> 讀。橘色的部分是<b>你要自己輸入的</b>,輸入完按 Enter。程式會停在 <code>cin</code> 那一行等你。",
       code("p04/a1"), term("p04/a1"),
       tip("本機:直接在終端機打。線上編譯器:多半要在網頁上的 <b>Input / stdin</b> 欄位<b>事先填好</b>要輸入的內容(每個值之間用空格或換行隔開),再按 Run。")),
  step(2, "一次讀兩個值",
       "<code>cin</code> 可以像 <code>cout</code> 一樣接著用,依序把輸入放進各個變數。輸入時用空格或換行隔開都可以。",
       code("p04/a2"), term("p04/a2"),
       see("輸入 <code>3 5</code>,<code>a</code> 得到 3、<code>b</code> 得到 5,所以印出 <code>3 + 5 = 8</code>。")),
  step(3, "讀小數與整數,並控制輸出格式",
       "<code>cin</code> 會依變數的型態讀取。右邊的步驟加入 <code>&lt;iomanip&gt;</code>,控制小數位數與寬度。新增的行用綠色底標出,點 ⓘ 看說明。",
       code("p04/a3"), term("p04/a3"),
       warn("<code>fixed</code> 與 <code>setprecision</code> 設定一次就會<b>一直有效</b>,所以第二行和之後的小數都固定兩位;但 <code>setw</code> 只管緊接著的那一個。", "注意"))
))

lab = section("lab", "格式化輸出試驗台",
  '<p class="sub" style="margin-bottom:14px">換個數字、改精度與寬度,看輸出怎麼變。這個模擬的結果與真正的 g++ 輸出逐一核對過。先試試加上與拿掉 <code>fixed</code>。</p>',
  calc("format"))

traps = section("traps", "兩個最常見的輸入陷阱",
  '<h3>陷阱 1:<code>cin &gt;&gt;</code> 之後接 <code>getline</code>,名字是空的</h3>'
  '<p class="why">你輸入 <code>18</code> 再按 Enter,輸入緩衝區裡是 <code>18</code> 加一個換行符號。<code>cin &gt;&gt;</code> 只拿走 <code>18</code>,<b>換行留在緩衝區</b>;接著 <code>getline</code> 一讀,馬上遇到那個換行,於是讀到「空的一行」就結束了。</p>',
  code("p04/a4"), term("p04/a4"),
  '<p style="margin-top:14px">修法:在 <code>getline</code> 之前先把剩下的換行丟掉。</p>',
  code("p04/a4fix", prev="p04/a4"), term("p04/a4fix"),
  tip("口訣:<b>先用 <code>cin &gt;&gt;</code> 讀值,後面要接 <code>getline</code>,中間就補一行 <code>cin.ignore(1000, '\\n');</code></b>。"),
  '<h3 style="margin-top:30px">陷阱 2:輸入的型態不對</h3>'
  '<p class="why">程式要整數,你卻輸入 <code>abc</code>。這時 <code>cin</code> 會進入<b>失敗狀態</b>:<code>a</code> 變成 0,而且<b>之後所有的讀取都會被跳過</b>(<code>b</code> 維持原本的 <code>-1</code>)。程式不會當掉,只是默默得到錯的結果。</p>',
  code("p04/a5"), term("p04/a5"),
  see("這也是為什麼要替變數給初始值(第 3 篇):讀取失敗時,至少看得出它沒被讀到。第 6 篇學會 <code>if</code> 之後,就能檢查讀取是否成功。"))

stuck = section("stuck", "初學者最常卡住的三個地方",
  details("程式一直卡著不動",
          "<p>它多半在 <code>cin</code> 那一行等你輸入。看看提示文字,在終端機裡輸入內容再按 Enter。用線上編譯器時,要先在 Input 欄位填好資料。</p>"),
  details("輸出全部擠在同一行",
          "<p>忘了換行。<code>cout</code> 不會自動換行,要自己加 <code>endl</code> 或 <code>\"\\n\"</code>。</p>"),
  details("編譯說找不到 <code>setw</code> 或 <code>setprecision</code>",
          "<p>它們在 <code>&lt;iomanip&gt;</code> 裡,記得加 <code>#include &lt;iomanip&gt;</code>。<code>getline</code> 與 <code>string</code> 則需要 <code>#include &lt;string&gt;</code>。</p>"))

QUIZ = quiz_cfg([
  ("<code>cin &gt;&gt; a &gt;&gt; b;</code>,輸入 <code>3 5</code>,<code>a</code> 與 <code>b</code> 各是?", ["a 是 3、b 是 5", "a 是 35、b 是 0", "只讀到 a"], 0,
   "cin 用空白分隔,依序把值放進各個變數。"),
  ("<code>cout &lt;&lt; fixed &lt;&lt; setprecision(2) &lt;&lt; 3.14159;</code> 印出?", ["3.14", "3.1", "3.14159"], 0,
   "fixed 加 setprecision(2) 代表小數點後固定 2 位。"),
  ("為什麼 <code>cin &gt;&gt; age;</code> 之後接 <code>getline(cin, name);</code>,name 常常是空的?", ["age 後面留下的換行被 getline 讀走了", "getline 只能讀數字", "cin 壞掉了"], 0,
   "cin >> 不會拿走換行,getline 一開始就遇到它,於是讀到空行。"),
  ("哪一組需要 <code>#include &lt;iomanip&gt;</code>?", ["setw 與 setprecision", "cin 與 cout", "endl"], 0,
   "格式化工具 setw、setprecision 在 iomanip;cin、cout、endl 在 iostream。"),
  ("<code>int n; cin &gt;&gt; n;</code>,使用者輸入 <code>abc</code>,接著後面還有其他 <code>cin</code> 讀取,會怎樣?", ["輸入進入失敗狀態,後面的讀取也被跳過", "自動跳過 abc 繼續讀", "程式立刻當掉"], 0,
   "失敗後 cin 不會自己恢復,後面的讀取都不會生效。"),
])

practice = section("practice", "動手演練:讀進來、算一算、印出來",
  '<p class="sub" style="margin-bottom:18px">每題先自己寫,再展開看參考解答。本機請自己輸入範例的內容;線上編譯器請先填入 Input 欄位。</p>',
  exercise(1, "兩數的和與差", "讀入兩個整數,印出它們的和與差。例如輸入 <code>12 30</code>。", "p04/x1"),
  exercise(2, "算總價", "讀入單價(可能有小數)與數量,印出總價,<b>固定顯示兩位小數</b>。例如輸入 <code>19.9 3</code>。", "p04/x2",
           note="別忘了 <code>#include &lt;iomanip&gt;</code>。"),
  exercise(3, "自我介紹", "先讀年齡,再讀一個<b>含空格</b>的全名(例如 <code>Mina Chen</code>),印出「全名,你 N 歲」。小心陷阱 1。", "p04/x3",
           note="年齡之後、<code>getline</code> 之前,補上 <code>cin.ignore(1000, '\\n');</code>。"),
  QUIZ_HTML,
  chk(["我知道 <code>&lt;&lt;</code> 與 <code>&gt;&gt;</code> 的箭頭代表資料流動的方向。", "我能用 <code>cin</code> 一次讀入多個值。",
       "我會用 <code>fixed</code> 與 <code>setprecision</code> 控制小數位數,用 <code>setw</code> 控制寬度。",
       "我知道 <code>cin &gt;&gt;</code> 之後接 <code>getline</code> 要先 <code>cin.ignore</code>。", "我知道輸入型態錯誤時,<code>cin</code> 會進入失敗狀態。",
       "我知道在線上編譯器要先在 Input 欄位填好輸入。"]),
  links([("https://en.cppreference.com/cpp/io/cin", "cppreference:std::cin", "cppreference.com"),
         ("https://en.cppreference.com/cpp/io/manip/setprecision", "cppreference:std::setprecision", "cppreference.com")]))

SPEC = spec(
  file="clang-io-guide.html",
  title="輸入輸出:cout 送出、cin 收進,輸入的坑多半出在換行",
  eyebrow="第 4 篇 · 輸入輸出",
  h1="<code>cout</code> 送出、<code>cin</code> 收進:輸入的坑多半出在換行",
  sub="學會讀取使用者輸入、把輸出排得整齊,並親眼看看兩個初學者最常踩的輸入陷阱,之後就不會再被它們卡住。",
  tldr="<code>cout &lt;&lt;</code> 往螢幕送、<code>cin &gt;&gt;</code> 往變數收,箭頭方向就是資料方向。用 <code>fixed</code>、<code>setprecision</code>、<code>setw</code> 排版。<strong><code>cin &gt;&gt;</code> 後接 <code>getline</code> 要先 <code>cin.ignore</code></strong>;輸入型態錯會讓 <code>cin</code> 進入失敗狀態。",
  toc=[("what", "兩條水管"), ("map", "對照表"), ("steps", "三個步驟"), ("lab", "格式化試驗台"), ("traps", "兩個陷阱"), ("stuck", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, mapsec, steps_, lab, traps, stuck, practice]),
  config=dict(calc=dict(format=dict(kind="format")), quiz=QUIZ),
  **nav(4),
)
