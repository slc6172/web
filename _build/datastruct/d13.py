from dh import *

what = section("what", "直覺:每次都要「馬上拿到最大(或最小)的那個」",
  '<div class="panel"><h3>醫院急診:不是先來先看,是最嚴重的先看</h3>'
  '<p>第 5 篇的 queue 是先進先出。但有些場合要的是「<b>優先順序最高的先出來</b>」:急診、作業系統排程、遊戲裡最近的敵人、下一篇的最短路徑。這種資料結構叫<b>優先佇列</b>(priority queue),最常見的實作是<b>堆積</b>(heap)。</p>'
  '<p style="margin-bottom:0">用排序好的陣列也能做到,但插入要搬動元素(<code>O(n)</code>)。堆積只保證<b>最大的在最上面</b>,不要求其他位置排好,換來 push 與 pop 都只要 <code>O(log n)</code>。</p></div>',
  '<h3 style="margin-top:26px">兩個重點:規則,以及用陣列存</h3>',
  table("g2", ["重點", "說明"], [
    ["最大堆積的規則", "每個節點的值都<b>不小於</b>它的左右子節點。所以最大的值一定在根。(最小堆積反過來。)"],
    ["形狀:完全二元樹", "一層一層填滿,最後一層從左填到右,中間不留洞。"],
    ["用陣列存,不用指標", "從位置 0 開始,一層一層排進陣列。位置 <code>i</code> 的<b>父節點</b>在 <code>(i-1)/2</code>,<b>左子</b>在 <code>2*i+1</code>,<b>右子</b>在 <code>2*i+2</code>。例:位置 1 的父是 0,子是 3 與 4。"],
    ["上浮 / 下沉", "push 把新值放最後再<b>上浮</b>(sift up);pop 把最後一個搬到根再<b>下沉</b>(sift down)。"],
  ]),
  '<div class="tip"><b class="l">為什麼不是排好序?</b>堆積只比較「父與子」,兄弟之間(例如左子和右子)沒有大小關係。這是它比排序陣列便宜的原因。</div>')

play = section("play", "動手玩:同一份資料,陣列與樹並排看",
  '<p class="sub" style="margin-bottom:14px">上面是樹,下面是同一份資料的陣列(格子下的數字是位置 <code>i</code>)。<b>橘色</b>是正在移動的值,<b>綠色</b>是比較的對象,<b>虛線紅框</b>是即將被拿掉的。最多放 10 個數字。</p>',
  try_list(["按「範例」,再 <b>push 10</b>:看它一路上浮到根,陣列和樹同步變化。", "<b>push 4</b>:父節點比它大,第一次比較就停。", "連按幾次 <b>pop 取出最大</b>:取出的順序是不是由大到小?", "按「遞增放入 1~7」(每個新值都比前面大):每個 push 都要上浮到根,看比較與交換次數。"]),
  widget("w-heap", "堆積動畫(陣列與樹並排)"),
  sim("", "猜猜看:堆積的陣列有排好序嗎?", "push 了 <code>5, 3, 8, 1, 9, 2</code>,陣列是 <code>9 8 5 1 3 2</code>。這個陣列是由大到小排好序的嗎?",
      [("a1", "是,堆積就是排好序的陣列"), ("a2", "不是,只保證每個節點不小於它的子節點"), ("a3", "不是,只有最後一個位置是最大的")]))

code = section("code", "完整程式:上浮與下沉",
  '<p class="sub" style="margin-bottom:14px">整個堆積就是一個 <code>vector&lt;int&gt;</code>。兩個核心動作都是「<b>和父(或子)比較,不對就交換,換到對為止</b>」,每次最多走過樹的高度那麼多層。</p>',
  cpp("heap_ops"), out("heap_ops", "執行結果(push 逐步的陣列、兩次 pop、最後依序取出)"), compile_cmd(),
  '<div class="tip"><b class="l">pop 為什麼要搬最後一個到根?</b>直接把根拿掉會留下一個洞,而且陣列要整排往前搬(<code>O(n)</code>)。改成把最後一個搬到根、刪掉最後一格,陣列一次就縮短;再讓根往下沉到對的位置。</div>')

stl = section("stl", "實務上:std::priority_queue",
  '<p class="sub" style="margin-bottom:14px"><code>std::priority_queue</code> 就是把上面的做法包好:用 <code>vector</code> 存,<code>push</code> / <code>pop</code> 為 <code>O(log n)</code>,<code>top</code> 為 <code>O(1)</code>。注意<b>預設是最大堆積</b>。</p>',
  cpp("heap_stl"), out("heap_stl", "執行結果"),
  table("g3", ["想要", "寫法", "top() 是"], [
    ["最大的先出來", "<code>priority_queue&lt;int&gt;</code>", "最大值"],
    ["最小的先出來", "<code>priority_queue&lt;int, vector&lt;int&gt;, greater&lt;int&gt;&gt;</code>", "最小值"],
    ["依 pair 的第一個值排", "<code>priority_queue&lt;pair&lt;int,int&gt;&gt;</code>(第一個相同再比第二個)", "第一個值最大的 pair"],
  ]))

cost = section("cost", "複雜度小表",
  '<p class="sub" style="margin-bottom:14px">n 個元素的完全二元樹高度約 <code>log₂n</code>,上浮與下沉最多走一整條「根到葉」的路。</p>',
  table("g3", ["操作", "時間", "為什麼"], [
    ["top(看最大的)", "<code>O(1)</code>", "就是位置 0"],
    ["push", "<code>O(log n)</code>", "最多上浮到根,走過高度那麼多層"],
    ["pop", "<code>O(log n)</code>", "最多下沉到葉"],
    ["放進 n 個數字", "<code>O(n log n)</code>", "n 次 push(用 <code>make_heap</code> 一次建好可以到 <code>O(n)</code>)"],
    ["依序 pop 完(堆積排序)", "<code>O(n log n)</code>", "n 次 pop"],
  ]),
  '<p style="margin-top:14px">對照第 9 篇:堆積排序就是「全部 push 進去,再一個一個 pop」,取出的順序自然排好,時間 <code>O(n log n)</code>。</p>')

gotchas = section("gotchas", "初學者最常卡住的四個地方",
  details("以為 priority_queue 預設是最小堆積",
    '<p>預設 <code>std::less</code>,<code>top()</code> 是<b>最大</b>的。想要最小的,要寫 <code>priority_queue&lt;int, vector&lt;int&gt;, greater&lt;int&gt;&gt;</code>。比較函式的方向和直覺相反,第一次寫幾乎都會搞反。</p>'),
  details("pop() 會回傳值?",
    '<p><code>std::priority_queue::pop()</code> 回傳 <code>void</code>:要先 <code>top()</code> 拿值,再 <code>pop()</code> 刪掉。(本篇自己寫的 <code>pop</code> 為了教學直接回傳最大值,STL 不是這樣。)</p>'),
  details("對空的堆積 top() 或 pop()",
    '<p>空的 <code>priority_queue</code> 呼叫 <code>top()</code> 或 <code>pop()</code> 是未定義行為(可能直接當掉)。先檢查 <code>!pq.empty()</code>。</p>'),
  details("把堆積的陣列當成排好序的",
    '<p>堆積內部的順序只保證父不小於子。直接印陣列看起來「大概由大到小」,但並沒有排好。要排好序,得一個一個 <code>pop</code>。<code>priority_queue</code> 也不能走訪,只能看 top。</p>'))

SIM = {
  "a1": "<b>不是。</b>堆積只比較父與子。例如陣列 <code>9 8 5 1 3 2</code> 裡,位置 4 的 3 比位置 3 的 1 大,兄弟之間沒有規定。",
  "a2": "<b>正確!</b>每個節點不小於子節點,最大的在根,但整個陣列不一定排好序(<code>9 8 5 1 3 2</code> 剛好大致遞減,換個順序放入就不一定了)。",
  "a3": "<b>不是。</b>最大的在<b>根(位置 0)</b>,最後的位置通常是比較小的葉。",
}
QUIZ = quiz_cfg([
  ("陣列從位置 0 開始存堆積,位置 i 的左子節點在?", ["2*i + 1", "2*i", "i + 1"], 0, "左子 2*i+1,右子 2*i+2,父節點 (i-1)/2。"),
  ("最大堆積中,最大的值在哪裡?", ["根(位置 0)", "最後一個位置", "隨便一個葉"], 0, "規則是每個節點都不小於子節點,所以根最大。"),
  ("push 一個新值,做法是?", ["從根往下沉", "放在陣列最後面,再往上浮", "把整個陣列重新排序"], 1, "放最後(最底層最左空位),再和父節點比較上浮。"),
  ("std::priority_queue<int> 預設 top() 回傳?", ["最小的", "最大的", "最先放進去的"], 1, "預設是最大堆積;要最小的得加 greater。"),
  ("堆積的 pop 時間複雜度?", ["O(1)", "O(log n)", "O(n)"], 1, "最多下沉樹的高度那麼多層。"),
])

ex = ('<h3 style="margin-top:30px">動手寫(兩題)</h3>'
  '<div class="panel"><h3>第 1 題:isMaxHeap</h3><p>檢查一個 vector 是不是最大堆積(每個節點都不小於它的子節點)。輸出應該是 <code>1011</code>。</p>' + cpp("heap_ex1_starter") +
  details("參考答案", "<p>逐一檢查每個位置 i:左子 <code>2*i+1</code>、右子 <code>2*i+2</code> 只有在範圍內才比較。<code>O(n)</code>。</p>" + cpp("heap_ex1", "完整答案") + out("heap_ex1")) + '</div>'
  '<div class="panel" style="margin-top:14px"><h3>第 2 題:第 k 大</h3><p>只用一個「最小堆積」,大小不超過 k,回傳 nums 裡第 k 大的值。輸出應該是 <code>5 4</code>。</p>' + cpp("heap_ex2_starter") +
  details("參考答案", "<p>堆積只保留目前最大的 k 個數,超過就 pop 掉最小的,最後 top 就是第 k 大。時間 <code>O(n log k)</code>,比整個排序更省(尤其 k 很小時)。</p>" + cpp("heap_ex2", "完整答案") + out("heap_ex2")) + '</div>')

practice = section("practice", "動手演練:確認你真的懂了", ex, QUIZ_HTML,
  checks(["我能說出最大堆積的規則,以及最大的值在哪裡。",
          "我能用 <code>2*i+1</code>、<code>2*i+2</code>、<code>(i-1)/2</code> 算出父子位置。",
          "我能口述 push(上浮)與 pop(搬最後一個到根再下沉)。",
          "我知道 <code>priority_queue</code> 預設是最大堆積,要最小堆積得加 <code>greater</code>。",
          "我知道堆積的陣列不是排好序的,只保證父不小於子。"], title="學完之後,對照這張清單"),
  resources([
    ("https://en.cppreference.com/cpp/container/priority_queue", "std::priority_queue", "cppreference · std::priority_queue"),
    ("https://en.cppreference.com/cpp/algorithm/make_heap", "std::make_heap", "cppreference · std::make_heap"),
  ], title="cppreference 參考頁面"))

SCRIPT = r'''
var H = Algo.heap;
function render(f) {
  return Algo.treeHtml({ tree: f.tree }) + Algo.cellsHtml({ rows: [{ label: "陣列(格子下的數字是位置 i)", cells: f.cells, empty: 0 }], chips: f.chips });
}
function randomList() {
  var a = []; for (var i = 0; i < 7; i++) a.push(1 + Math.floor(Math.random() * 99)); return a;
}
Algo.widget("w-heap", {
  form: [{ id: "op", label: "操作", type: "select", value: "push", options: Object.keys(H.NAMES).map(function (k) { return [k, H.NAMES[k]]; }) },
         { id: "val", label: "數字(1–99,pop 不用填)", type: "number", value: 10, min: 1, max: 99 }],
  buttons: [
    { label: "範例", run: function (v, c) { c.setBase(H.fromList([5, 3, 8, 1, 9, 2])); } },
    { label: "遞增放入 1~7", run: function (v, c) { c.setBase(H.fromList([1, 2, 3, 4, 5, 6, 7])); } },
    { label: "隨機 7 個", run: function (v, c) { c.setBase(H.fromList(randomList())); } }
  ],
  init: H.init, idle: H.idle,
  make: function (v, base) { return H.run(v.op, v.val, base); },
  render: render, code: H.CODE_HEAP, code_cap: "堆積(亮起來的行 = 目前執行到的地方)"
});
'''
SPEC = dict(
  file="datastruct-heap-guide.html", dir="datastruct", eyebrow_prefix=EYEBROW, foot=FOOT,
  modules=["cells", "tree", "alg_heap"], script=SCRIPT,
  title="堆積與優先佇列:上浮、下沉與 priority_queue",
  eyebrow="第 13 篇 · 堆積與優先佇列",
  h1="每次都先拿最大的:用陣列存的一棵樹",
  sub="堆積讓你「馬上拿到最大(或最小)的」,push 與 pop 都是 O(log n)。這一篇用陣列與樹並排的動畫看上浮與下沉,再用 std::priority_queue。",
  tldr="堆積是完全二元樹,用陣列存:位置 <code>i</code> 的父在 <code>(i-1)/2</code>、左子 <code>2i+1</code>、右子 <code>2i+2</code>。最大堆積的根最大;push 放最後再<b>上浮</b>,pop 把最後一個搬到根再<b>下沉</b>,都是 <code>O(log n)</code>。<code>std::priority_queue</code> 預設是最大堆積。<br><small>先備:第 3 篇 vector、第 5 篇 queue、第 11 篇二元樹。預估 18 分鐘。難度:進階。</small>",
  toc=[("what", "直覺與陣列存法"), ("play", "上浮與下沉"), ("code", "完整程式"), ("stl", "priority_queue"), ("cost", "複雜度小表"), ("gotchas", "常見錯誤"), ("practice", "動手寫與測驗")],
  body="\n\n".join([what, play, code, stl, cost, gotchas, practice]),
  config=dict(sim=SIM, quiz=QUIZ),
  prev=("datastruct-bst-guide.html", "二元搜尋樹"),
  next=("datastruct-graph-guide.html", "圖的表示與 BFS/DFS"),
)
