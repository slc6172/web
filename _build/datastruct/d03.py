from dh import *

what = section("what", "vector 就是一排編號的置物櫃",
  '<div class="panel"><h3>用「一排緊貼的置物櫃」來想</h3>'
  '<p>想像走廊上有一排<strong>緊貼在一起</strong>的置物櫃,編號從 <b>0</b> 開始。要拿 5 號櫃的東西,你不用從 0 號開始一個個找,直接走到 5 號就好,這叫<strong>隨機存取</strong>,一步到位。</p>'
  '<p style="margin-bottom:0">但如果想在 2 號和 3 號之間「再擠進一個新櫃子」,右邊每一個櫃子裡的東西,都得先往後搬一格。<strong>讀取很快、中間插入很貴</strong>,這就是這一篇要看懂的事。</p></div>',
  '<h3 style="margin-top:26px">五個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["元素(element)", "vector 裡存的每一筆資料,例如 <code>{10, 20, 30}</code> 有 3 個元素。"],
    ["索引(index)", "元素的編號,<b>從 0 開始</b>。<code>v[0]</code> 是第一個,最後一個是 <code>v[size - 1]</code>。"],
    ["size", "目前實際放了幾個元素。"],
    ["capacity", "目前向系統「租下」的格子數。永遠 ≥ size;容量用完了才需要換更大的空間。"],
    ["連續記憶體", "元素在記憶體中一個緊接一個排好。這讓 <code>v[i]</code> 能直接算出位置,也是「搬家」成本的來源。"],
  ]),
  '<div class="tip"><b class="l">原生陣列呢?</b>你也許看過 <code>int a[5];</code>。它同樣是連續記憶體、同樣用索引讀取,但<b>大小在寫程式時就固定</b>,不能 <code>push_back</code>。這一篇的觀念兩者通用;實務上我們優先用 <code>std::vector</code>。</div>')

basic = section("basic", "先認識 vector 的幾個寫法",
  '<p class="sub" style="margin-bottom:14px">這份程式用到本篇會出現的全部基本語法。先看一遍,不用背。</p>',
  cpp("array_basic"), out("array_basic"), compile_cmd(),
  table("g2", ["寫法", "意思"], [
    ["<code>std::vector&lt;int&gt; v = {10, 20, 30};</code>", "建立一個放 <code>int</code> 的 vector,一開始有 3 個元素。尖括號裡是元素的型別。"],
    ["<code>v.push_back(40);</code>", "在尾端加一個元素。vector 會自己長大,不用先決定大小。"],
    ["<code>v.size()</code>", "目前有幾個元素。"],
    ["<code>v[0]</code>", "用索引讀取(或修改)元素。"],
    ["<code>for (int x : v)</code>", "range-for:依序把每個元素拿出來給 <code>x</code>,不需要索引時最簡潔。"],
  ]),
  '<div class="tip"><b class="l">為什麼寫 static_cast&lt;int&gt;(v.size())?</b><code>v.size()</code> 的型別是<b>無號整數</b>(<code>size_t</code>),不能是負數。拿它和 <code>int</code> 比較、相減,很容易出怪事(見下方「常見錯誤」)。本站一律先轉成 <code>int</code> 再用,讓初學階段少踩坑。</div>')

play = section("play", "動手玩:在中間插入、從前面刪除",
  '<p class="sub" style="margin-bottom:14px">畫面上是一個 vector,下方的程式碼就是我們自己寫的 <code>insertAt</code> 與 <code>eraseAt</code>。每按一次「下一步」,就執行一小步,亮起來的行就是目前執行到的地方。</p>',
  try_list(["按「最前面插入」:看有幾個元素被搬動(橘色格子)。", "按「尾端插入」:這次要搬幾個?", "按「刪除最前面」,再按「刪除最後面」,比較搬動次數。", "插入太多次後再按一次,看看會出現什麼提示。"]),
  widget("w-edit", "vector 插入與刪除動畫"),
  sim("", "猜猜看:這一步會發生什麼?", "vector 現在有 5 個元素 <code>{10, 20, 30, 40, 50}</code>,在<b>位置 0(最前面)</b>插入一個新值,要搬動幾個既有元素?",
      [("a1", "0 個"), ("a2", "1 個"), ("a3", "5 個")]),
  '<p style="margin-top:14px">結論:搬動次數 = <b>插入位置之後有幾個元素</b>。插在最前面要搬全部 n 個,插在尾端要搬 0 個。刪除也一樣,位置越靠前,後面要補位的元素越多。</p>')

grow = section("grow", "動手玩:vector 怎麼自己長大",
  '<p class="sub" style="margin-bottom:14px"><code>push_back</code> 看起來永遠成功,但 vector 的格子是<b>租來的</b>。租的格子用完了,它就要換一塊更大的、把舊資料全部搬過去。</p>',
  try_list(["按幾次「push_back」,觀察 capacity 如何變化。", "看到「已經滿了」時,注意舊空間與新空間兩列,以及累計複製的次數。", "按「連續 9 次」,對照下方真實程式的輸出。"]),
  widget("w-grow", "vector 擴容動畫"),
  cpp("array_grow"), out("array_grow", "執行結果(size  capacity)"),
  '<div class="see"><b class="l">你會看到</b>capacity 依序是 1、2、4、4、8、8、8、8、16,每次滿了就變成 2 倍。這是 g++ 的做法;不同編譯器的倍數可能不同(例如 MSVC 是 1.5 倍),但「滿了就換更大的空間並搬家」是一樣的。</div>',
  '<div class="tip"><b class="l">知道要放多少時,先 reserve</b>如果事先知道大概會放 100 個,<code>v.reserve(100)</code> 一次租好,就不會在途中反覆搬家。</div>',
  cpp("array_reserve"), out("array_reserve"))

code = section("code", "完整程式:自己寫一次插入與刪除",
  '<p class="sub" style="margin-bottom:14px">這就是動畫裡用的那兩個函式,加上 <code>main</code> 與印出的小函式。你可以複製到自己的電腦編譯執行。</p>',
  cpp("array_edit"), out("array_edit"),
  '<p>重點在 <code>for</code> 迴圈:<code>insertAt</code> 從<b>後面往前</b>搬(不然會把還沒搬的資料蓋掉),<code>eraseAt</code> 從<b>前面往後</b>搬。順序反過來,結果就會錯。</p>',
  '<h3 style="margin-top:22px">實務上:直接用 STL</h3>',
  '<p>你不需要每次都自己寫迴圈。<code>std::vector</code> 已經提供 <code>insert</code> 與 <code>erase</code>,做的事和我們寫的一樣(一樣要搬動元素,一樣是 O(n))。<code>v.begin()</code> 是「指向第一個元素的位置」,<code>v.begin() + 2</code> 就是位置 2。</p>',
  cpp("array_stl"), out("array_stl"))

cost = section("cost", "複雜度小表:哪些操作快、哪些慢",
  '<p class="sub" style="margin-bottom:14px">n 代表元素個數。O(1) 是「不管多少元素,都是固定幾步」;O(n) 是「元素越多,步數成正比」。(第 2 篇有完整說明。)</p>',
  table("g3", ["操作", "時間", "為什麼"], [
    ["<code>v[i]</code> 讀取 / 修改", "O(1)", "位置算得出來,一步到位。"],
    ["<code>push_back</code>", "平均 O(1)", "大多數時候直接放進空位;只有容量滿了才搬家(那一次是 O(n))。"],
    ["<code>pop_back</code>", "O(1)", "只是把 size 減 1,不用搬任何東西。"],
    ["在中間 <code>insert</code>", "O(n)", "插入位置之後的元素全部往後搬一格。"],
    ["在中間 <code>erase</code>", "O(n)", "刪除位置之後的元素全部往前補一格。"],
    ["在最前面插入 / 刪除", "O(n)", "最糟:全部 n 個元素都要搬。"],
    ["找某個值(沒排序)", "O(n)", "只能從頭一個一個看。第 6 篇會學更快的方法。"],
  ]),
  '<p style="margin-top:14px"><b>空間:</b>O(n)。capacity 可能比 size 大(最多約 2 倍),這是用空間換「<code>push_back</code> 很少搬家」的代價。</p>')

gotchas = section("gotchas", "初學者最常卡住的三個地方",
  details("<code>v.size() - 1</code> 在空 vector 上變成超大的數字",
    '<p>因為 <code>size()</code> 是無號整數,<code>0 - 1</code> 不會變成 -1,而是「繞回」最大值。如果拿它當迴圈上限,迴圈會跑到天荒地老。</p>' + cpp("array_sizet") + out("array_sizet", "執行結果(第一行就是那個超大數字)") +
    '<p>解法:先 <code>static_cast&lt;int&gt;(v.size())</code>,再計算。</p>'),
  details("<code>v[10]</code> 越界,程式卻沒有報錯",
    '<p><code>v[i]</code> <b>不會檢查範圍</b>。越界讀寫是未定義行為:可能剛好沒事、可能讀到亂值、也可能當掉,而且每次不一定一樣,最難除錯。</p>'
    '<p>想要有保護,用 <code>v.at(i)</code>:越界時會丟出 <code>std::out_of_range</code> 例外,錯誤變得看得見。</p>' + cpp("array_oob") + out("array_oob")),
  details("我 <code>push_back</code> 了很多次,程式變慢了",
    '<p>很可能是反覆擴容搬家。如果事先知道大概的數量,用 <code>reserve</code>(見上方「擴容」那一節)一次租好。另外,如果你常在最前面或中間插入,vector 本來就不適合,下一篇的鏈結串列是另一種取捨。</p>'))

SIM = {
  "a1": "<b>不是。</b>位置 0 之後的每個元素,都要先往後搬一格,才能空出位置 0。回到動畫按「最前面插入」確認。",
  "a2": "<b>不是。</b>只搬 1 個的話,其他元素會被蓋掉。每個元素都要往後移一格。",
  "a3": "<b>正確!</b>5 個元素全部都要往後搬一格,搬動次數 = 插入位置之後的元素個數 = 5。這就是在最前面插入是 O(n) 的原因。",
}
QUIZ = quiz_cfg([
  ("vector 有 5 個元素,在最前面(位置 0)插入一個新值,要搬動幾個既有元素?", ["0 個", "1 個", "5 個"], 2,
   "位置 0 之後的 5 個元素都要往後搬一格。搬動次數等於插入位置之後的元素個數。"),
  ("下面哪個操作「不需要」搬動任何既有元素(假設容量夠)?", ["在位置 0 插入", "刪除位置 2", "在尾端 push_back"], 2,
   "尾端後面沒有元素,所以不用搬。其他兩個都要讓後面的元素補位或讓位。"),
  ("capacity 依序是 1、2、4、8。第幾次 push_back 會讓 capacity 從 4 變成 8?", ["第 4 次", "第 5 次", "第 8 次"], 1,
   "前 4 次放滿 4 格(size = capacity = 4),第 5 次沒有空位,才需要擴容成 8。"),
  ("為什麼空 vector 的 <code>v.size() - 1</code> 會得到超大數字?", ["size() 是無號整數,0 - 1 會繞回最大值", "vector 壞掉了", "編譯器的 bug"], 0,
   "無號整數不能是負的,減過頭會從最大值繞回來。所以先轉成 int 再算。"),
  ("讀取 <code>v[i]</code> 的時間成本是?", ["O(1)", "O(n)", "O(n²)"], 0,
   "連續記憶體讓位置可以直接算出來,不用從頭找,一步到位。"),
])

ex = ('<h3 style="margin-top:30px">動手寫(兩題)</h3>'
  '<p class="sub" style="margin-bottom:12px">先自己在電腦上寫寫看,再展開參考答案。兩題的起始程式都能編譯,只是答案還不對。</p>'
  '<div class="panel"><h3>第 1 題:把 x 加進 total(補一行)</h3><p>下面的 <code>sum</code> 應該回傳所有元素的總和,但迴圈裡少了一行。補上它,輸出要是 14。</p>' +
  cpp("array_ex1_starter") +
  details("參考答案", "<p>迴圈裡加上這一行就好:<code>total += x;</code></p>" + cpp("array_ex1", "完整答案") + out("array_ex1")) + '</div>'
  '<div class="panel" style="margin-top:14px"><h3>第 2 題:數有幾個大於 x(完整寫出函式)</h3><p>完成 <code>countGreater</code>:回傳 v 裡「大於 x」的元素個數。範例的輸出應該是 4 和 0。</p>' +
  cpp("array_ex2_starter") +
  details("參考答案", "<p>用一個計數器,走訪每個元素,大於 x 就加 1。時間是 O(n),因為每個元素都看一次。</p>" + cpp("array_ex2", "完整答案") + out("array_ex2")) + '</div>')

practice = section("practice", "動手演練:確認你真的懂了",
  ex, QUIZ_HTML,
  checks(["我知道 vector 的元素是連續擺放的,所以 <code>v[i]</code> 一步就到。",
          "我知道索引從 0 開始,最後一個元素是 <code>v[size - 1]</code>。",
          "我能說出為什麼在最前面插入要搬動所有元素。",
          "我知道 size 與 capacity 的差別,也知道容量滿了會換新空間並搬家。",
          "我看得懂 <code>insertAt</code> 與 <code>eraseAt</code>,知道為什麼搬動方向不同。",
          "我知道 <code>v[i]</code> 越界不會報錯,想檢查可以用 <code>at()</code>。"],
         title="學完之後,對照這張清單"),
  resources([
    ("https://en.cppreference.com/cpp/container/vector", "std::vector", "cppreference · std::vector"),
    ("https://en.cppreference.com/cpp/container/vector/insert", "vector::insert", "cppreference · std::vector::insert"),
    ("https://en.cppreference.com/cpp/container/vector/erase", "vector::erase", "cppreference · std::vector::erase"),
    ("https://en.cppreference.com/cpp/container/vector/capacity", "vector::capacity", "cppreference · std::vector::capacity"),
    ("https://en.cppreference.com/cpp/container/vector/reserve", "vector::reserve", "cppreference · std::vector::reserve"),
  ], title="cppreference 參考頁面"))

SCRIPT = r'''
var V = Algo.vec;
function idleEdit(b){ return { cells: V.mk(b), chips: [["元素個數", b.length], ["搬動次數", 0]], msg: "選好操作與位置,按「執行」。也可以直接按下面的快捷按鈕。" }; }
Algo.widget("w-edit", {
  form: [
    { id: "op", label: "操作", type: "select", value: "insert", options: [["insert", "在位置插入"], ["erase", "刪除位置"]] },
    { id: "pos", label: "位置", type: "number", min: 0, max: 10, value: 0 },
    { id: "val", label: "數值", type: "number", min: 0, max: 99, value: 99, showIf: { op: "insert" } }
  ],
  buttons: [
    { label: "最前面插入", run: function (v, c) { c.set("op", "insert"); c.set("pos", 0); c.run(); } },
    { label: "尾端插入", run: function (v, c) { c.set("op", "insert"); c.set("pos", c.base.length); c.run(); } },
    { label: "刪除最前面", run: function (v, c) { c.set("op", "erase"); c.set("pos", 0); c.run(); } },
    { label: "刪除最後面", run: function (v, c) { c.set("op", "erase"); c.set("pos", Math.max(0, c.base.length - 1)); c.run(); } }
  ],
  init: function () { return [10, 20, 30, 40, 50]; },
  idle: idleEdit,
  make: function (v, base) { return v.op === "insert" ? V.insert(base, v.pos, v.val) : V.erase(base, v.pos); },
  render: Algo.cellsHtml, code: V.CODE_EDIT, code_cap: "insertAt / eraseAt(亮起來的行 = 目前執行到的地方)"
});
Algo.widget("w-grow", {
  form: [{ id: "count", label: "連續 push_back 幾次", type: "number", min: 1, max: 9, value: 1 }],
  runLabel: "push_back",
  buttons: [{ label: "連續 9 次", run: function (v, c) { c.set("count", 9); c.run(); } }],
  init: V.growInit,
  idle: function (b) { return { cells: V.mk(b.vals), empty: b.cap - b.vals.length, chips: [["size", b.vals.length], ["capacity", b.cap], ["擴容次數", b.grows], ["累計複製", b.copies]],
                               msg: "vector 一開始是空的(size 0、capacity 0)。按「push_back」放進第一個元素。" }; },
  make: function (v, base) { return V.push(base, v.count); },
  render: Algo.cellsHtml, code: V.CODE_GROW, code_cap: "對應的程式(亮起來的行 = 目前執行到的地方)"
});
'''

SPEC = dict(
  file="datastruct-array-guide.html", dir="datastruct", eyebrow_prefix=EYEBROW, foot=FOOT,
  modules=["cells", "alg_array"], script=SCRIPT,
  title="陣列與 vector:讀取很快,中間插入要搬家",
  eyebrow="第 3 篇 · 陣列與 vector",
  h1="vector 讀取很快,但在中間插入要搬家",
  sub="vector 是學完 C++ 之後最常用的容器。這一篇用動畫看它裡面怎麼擺資料、為什麼在最前面插入很慢,以及它怎麼自己長大。",
  tldr="vector 把元素<strong>連續</strong>放在一起,所以用索引讀取一步就到(O(1))。但在中間插入或刪除,後面的元素都要搬一格(O(n));尾端 <code>push_back</code> 通常很快,只有容量滿了才要換新空間搬家。<br><small>先備:會用 <code>vector</code>、<code>push_back</code> 與 <code>for</code>。預估 12 分鐘。難度:入門。</small>",
  toc=[("what", "直覺:置物櫃"), ("basic", "先認識 vector"), ("play", "插入與刪除"), ("grow", "自己長大"), ("code", "完整程式"), ("cost", "複雜度小表"), ("gotchas", "常見錯誤"), ("practice", "動手寫與測驗")],
  body="\n\n".join([what, basic, play, grow, code, cost, gotchas, practice]),
  config=dict(sim=SIM, quiz=QUIZ),
  prev=("datastruct-bigo-guide.html", "複雜度與 Big‑O"),
  next=("datastruct-linkedlist-guide.html", "鏈結串列"),
)
