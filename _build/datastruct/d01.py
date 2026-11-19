from dh import *

what = section("what", "後面三分之二的主題,都靠指標把資料串起來",
  '<div class="panel"><h3>這一篇可以略過嗎?</h3>'
  '<p>如果你已經能說清楚 <code>int* p = &amp;x;</code> 和 <code>int&amp; r = x;</code> 的差別,也寫過 <code>new</code>/<code>delete</code>,可以直接跳到第 2 篇。</p>'
  '<p style="margin-bottom:0">否則花 10 分鐘看完。鏈結串列、樹、圖的節點全都是「用指標指向下一個節點」,在這裡先把指標弄懂,後面會輕鬆很多。</p></div>',
  '<h3 style="margin-top:26px">這一篇要認識的名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["地址", "每個變數在記憶體裡都佔一格,每一格有編號,就是地址。"],
    ["參照 <code>int&amp; r = x;</code>", "替 x 取另一個名字。用 r 就是在用 x,沒有新的格子。"],
    ["指標 <code>int* p = &amp;x;</code>", "一個變數,裡面存的是「別人的地址」。說「p 指向 x」。"],
    ["解參考 <code>*p</code>", "走到 p 指的那一格,讀或改裡面的值。"],
    ["<code>-&gt;</code>", "指標專用的箭頭:<code>p-&gt;val</code> 等於 <code>(*p).val</code>,走到節點再取成員。"],
    ["<code>nullptr</code>", "表示「不指向任何東西」。鏈結串列的最後一個節點,next 就是 nullptr。"],
  ]),
  '<div class="tip"><b class="l">&amp; 和 * 會看錯,因為位置不同意思就不同</b><code>int&amp; r</code>(宣告時)是參照,<code>&amp;x</code>(運算時)是「取 x 的地址」;<code>int* p</code>(宣告時)是指標,<code>*p</code>(運算時)是「走到 p 指的那格」。看它前面有沒有型別。</div>')

mem = section("mem", "動手玩:變數、參照與指標",
  '<p class="sub" style="margin-bottom:14px">下面逐行執行一段小程式。左邊是記憶體裡的變數,右邊是程式碼。看 <code>x</code>、<code>r</code>、<code>p</code> 三者怎麼互相影響。</p>',
  try_list(["到第 4 步,注意 r 是虛線框:它和 x 是同一格。", "到第 5 步,看 p 裡存的是地址,不是 10。", "第 6、7 步分別用指標和參照改 x,看 x 的變化。", "第 8 步 p 改指 y,x 是不是還是 30?"]),
  widget("w-ptr", "指標與參照動畫"),
  sim("", "猜猜看:這一步會發生什麼?", "<code>int x = 10; int* p = &amp;x; *p = 20;</code> 執行完,x 是多少?",
      [("a1", "還是 10"), ("a2", "20"), ("a3", "p 的地址")]),
  cpp("prereq_ptr"), out("prereq_ptr"))

node = section("node", "動手玩:struct、new 與 ->",
  '<p class="sub" style="margin-bottom:14px">鏈結串列的節點就是一個 <code>struct</code>:裡面放資料,再放一個指向下一個節點的指標。這裡先用兩個節點練習 <code>new</code>、<code>-&gt;</code> 與 <code>delete</code>。</p>',
  try_list(["第 2 步:new 在右邊 heap 做出節點,左邊的 a 存它的地址。", "第 4 步:改 next,兩個節點就接起來了。", "第 6、7 步:delete 之後節點變成虛線框,表示已還給系統。"]),
  widget("w-node", "struct 與 new 動畫"),
  cpp("prereq_node"), out("prereq_node"),
  '<div class="tip"><b class="l">兩個新寫法</b><code>Node{1, nullptr}</code> 是依欄位順序一次填好 val 和 next。<code>new</code> 在 heap 要一塊空間並回傳地址;用 <code>new</code> 要來的,用完一定要 <code>delete</code>。</div>')

syntax = section("syntax", "兩個之後會常看到的寫法:auto 與 lambda",
  '<p class="sub" style="margin-bottom:14px"><code>auto</code> 讓編譯器幫你推斷型別;lambda 是「沒有名字的小函式」,排序時常拿來寫比較規則(第 8、9 篇)。</p>',
  cpp("prereq_syntax"), out("prereq_syntax"),
  table("g2", ["寫法", "意思"], [
    ["<code>auto pi = 3.14;</code>", "pi 的型別由右邊決定(<code>double</code>)。"],
    ["<code>[](int n) { return n * n; }</code>", "lambda:<code>[]</code> 開頭,後面接參數和函式本體。可以存進 <code>auto</code> 變數,像一般函式一樣呼叫。"],
    ["<code>for (auto&amp; e : v)</code>", "<code>auto&amp;</code> 拿到元素<b>本尊</b>(參照),改 e 就是改 v;去掉 <code>&amp;</code> 只是拿到複製品。"],
  ]))

run = section("run", "怎麼編譯並執行本站的範例",
  '<p class="sub" style="margin-bottom:14px">本站每一段完整程式都能複製到自己的電腦上跑。你只需要一個 C++ 編譯器(g++ 或 clang++)。</p>',
  table("g2", ["步驟", "做法"], [
    ["1. 安裝編譯器", "Linux 用套件管理員安裝 <code>g++</code>;macOS 在終端機執行 <code>xcode-select --install</code>;Windows 可以用 WSL,或安裝 MinGW-w64 / MSYS2。裝好後 <code>g++ --version</code> 能顯示版本就成功。"],
    ["2. 存檔", "把程式碼貼進 <code>main.cpp</code>(存成 UTF-8)。"],
    ["3. 編譯", "執行下面的指令。沒有訊息就是成功,同資料夾會多出 <code>main</code>(Windows 是 <code>main.exe</code>)。"],
    ["4. 執行", "<code>./main</code>(Windows 是 <code>main.exe</code>)。"],
  ]),
  compile_cmd(),
  table("g2", ["選項", "作用"], [
    ["<code>-std=c++17</code>", "使用 C++17 規則。"],
    ["<code>-Wall -Wextra</code>", "打開常見警告。看到警告別忽略,它多半在指出真的問題。"],
    ["<code>-fsanitize=address,undefined -g</code>", "選用。執行時抓越界、忘記 delete 等錯誤並指出行號,學指標時很有用(本站帶指標的範例都用它檢查過)。"],
  ]))

gotchas = section("gotchas", "初學者最常卡住的三個地方",
  details("指標沒有初始化,或指到 nullptr 還去用",
    '<p><code>int* p;</code> 只宣告、沒給值,裡面是亂數地址(野指標),用了會當掉或改壞別的資料。習慣寫成 <code>int* p = nullptr;</code>,並在用 <code>-&gt;</code> 或 <code>*</code> 之前先檢查它不是 nullptr。</p>' + cpp("prereq_null") + out("prereq_null")),
  details("<code>new</code> 了卻忘記 <code>delete</code>(記憶體洩漏)",
    '<p>少了 <code>delete</code>,那塊空間要到程式結束才會被回收。小程式看不出來,但程式跑很久或 new 很多次就會越吃越多。規則很簡單:<b>每個 new 對應一個 delete</b>。用 <code>-fsanitize=address</code> 編譯執行,它會在結束時報告洩漏。</p>'),
  details("<code>delete</code> 之後又去用、或 delete 兩次",
    '<p>delete 之後,那個指標還存著舊地址,但那塊空間已經不屬於你。再讀寫或再 delete 一次,都是未定義行為。習慣上 delete 之後不要再碰它;需要時可以順手把指標設成 <code>nullptr</code>。</p>'))

SIM = {
  "a1": "<b>不是。</b><code>*p = 20</code> 是走到 p 指的那一格(也就是 x)並寫入 20,所以 x 變了。回動畫第 6 步確認。",
  "a2": "<b>正確!</b>p 指向 x,<code>*p = 20</code> 就是直接改 x 這一格的內容。",
  "a3": "<b>不是。</b>p 裡存的是 x 的地址,但 <code>*p</code> 是走到那個地址去,取到的是 x 本身的值。",
}
QUIZ = quiz_cfg([
  ("<code>int x = 10; int* p = &amp;x; *p = 20;</code> 之後,x 是多少?", ["10", "20", "p 的地址"], 1,
   "<code>*p</code> 是走到 p 指的那一格,也就是 x,所以寫入 20 就改到 x。"),
  ("參照 <code>int&amp; r = x;</code> 和指標 <code>int* p = &amp;x;</code> 最大的差別是?", ["參照只是 x 的另一個名字,不能改成指別人;指標是自己的變數,存地址,可以改指向", "參照比指標快", "沒有差別"], 0,
   "參照一經綁定就永遠是同一個變數的別名;指標是獨立的變數,存的地址可以改。"),
  ("<code>a-&gt;next</code> 等於哪一個?", ["(*a).next", "*(a.next)", "&amp;a.next"], 0,
   "<code>-&gt;</code> 是 <code>(*a).</code> 的簡寫:先走到 a 指的節點,再取成員。"),
  ("用 <code>new</code> 做出來的節點,用完要怎麼處理?", ["用 delete 還給系統,new 幾次就 delete 幾次", "不用處理,程式會自己清", "再 new 一次覆蓋"], 0,
   "new 要來的空間不會自動歸還,忘了 delete 就是記憶體洩漏。"),
  ("<code>Node* p = nullptr;</code> 之後直接寫 <code>p-&gt;val</code> 會?", ["未定義行為,通常會當掉", "得到 0", "編譯錯誤"], 0,
   "nullptr 不指向任何東西,走過去讀資料是非法的。使用前要先檢查。"),
])

ex = ('<h3 style="margin-top:30px">動手寫(兩題)</h3>'
  '<p class="sub" style="margin-bottom:12px">先在自己的電腦上試試,再展開參考答案。</p>'
  '<div class="panel"><h3>第 1 題:用參照改呼叫者的變數(補一行)</h3><p><code>addOne</code> 要讓呼叫者的 x 加 1。補上那一行,輸出應該是 6。</p>' + cpp("prereq_ex1_starter") +
  details("參考答案", "<p>因為參數 <code>n</code> 是參照,它就是 x 本尊,所以 <code>++n;</code> 就會改到 x。</p>" + cpp("prereq_ex1", "完整答案") + out("prereq_ex1")) + '</div>'
  '<div class="panel" style="margin-top:14px"><h3>第 2 題:交換兩個變數(完整寫出函式)</h3><p>完成 <code>swapInt</code>,讓 a 和 b 的值對調。輸出應該是 <code>7 3</code>。提示:需要一個暫存變數。</p>' + cpp("prereq_ex2_starter") +
  details("參考答案", "<p>先把 a 暫存起來,再把 b 放進 a,最後把暫存的放進 b。因為參數是參照,對調的是呼叫者的變數。</p>" + cpp("prereq_ex2", "完整答案") + out("prereq_ex2")) + '</div>')

practice = section("practice", "動手演練:確認你真的懂了", ex, QUIZ_HTML,
  checks(["我能分辨 <code>int&amp; r</code>、<code>&amp;x</code>、<code>int* p</code>、<code>*p</code> 各是什麼意思。",
          "我知道參照是別名,指標存的是地址,指標可以改指向。",
          "我看得懂 <code>a-&gt;next</code>,知道它是走到節點再取成員。",
          "我知道 <code>new</code> 要配對 <code>delete</code>,delete 之後不再使用。",
          "我習慣把沒指向東西的指標寫成 <code>nullptr</code>,使用前先檢查。",
          "我能自己編譯並執行一份 .cpp,看得懂警告訊息。"], title="學完之後,對照這張清單"),
  resources([
    ("https://en.cppreference.com/cpp/language/pointer", "指標", "cppreference · Pointer declaration"),
    ("https://en.cppreference.com/cpp/language/reference", "參照", "cppreference · Reference declaration"),
    ("https://en.cppreference.com/cpp/language/lambda", "lambda", "cppreference · Lambda expressions"),
    ("https://en.cppreference.com/cpp/language/new", "new 運算式", "cppreference · new expression"),
  ], title="cppreference 參考頁面"))

SCRIPT = r'''
var fixed = function (id, frames, code, cap) {
  var w = Algo.widget(id, { form: [], runLabel: "從頭開始", init: function () { return null; },
    idle: function () { return frames[0]; }, make: function () { return { frames: frames, result: null }; },
    render: Algo.memHtml, code: code, code_cap: cap });
  w.run({});
};
fixed("w-ptr", Algo.ptr.framesPtr(), Algo.ptr.CODE_PTR, "程式碼(亮起來的行 = 目前執行到的地方)");
fixed("w-node", Algo.ptr.framesNode(), Algo.ptr.CODE_NODE, "程式碼(亮起來的行 = 目前執行到的地方)");
'''
SPEC = dict(
  file="datastruct-prereq-guide.html", dir="datastruct", eyebrow_prefix=EYEBROW, foot=FOOT,
  modules=["mem", "alg_ptr"], script=SCRIPT,
  title="先備速查:指標、參照與 struct",
  eyebrow="第 1 篇 · 先備速查",
  h1="指標只是「存別人地址的變數」,先搞懂它再往下學",
  sub="鏈結串列、樹、圖都靠指標串起節點。這一篇用動畫把變數、參照、指標、struct 與 new/delete 講清楚,並教你怎麼編譯執行本站的範例。已經熟的人可以略過。",
  tldr="<b>參照</b>是別名,<b>指標</b>是存地址的變數;<code>*p</code> 走到它指的那格,<code>p-&gt;x</code> 走到節點再取成員;<code>new</code> 要配對 <code>delete</code>。<br><small>先備:學過 C++17 基本語法。預估 10 分鐘。難度:入門(可略過)。</small>",
  toc=[("what", "為什麼要先備"), ("mem", "變數、參照與指標"), ("node", "struct 與 new"), ("syntax", "auto 與 lambda"), ("run", "編譯與執行"), ("gotchas", "常見錯誤"), ("practice", "動手寫與測驗")],
  body="\n\n".join([what, mem, node, syntax, run, gotchas, practice]),
  config=dict(sim=SIM, quiz=QUIZ),
  prev=None,
  next=("datastruct-bigo-guide.html", "複雜度與 Big‑O"),
)
