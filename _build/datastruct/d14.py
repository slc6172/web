from dh import *

what = section("what", "直覺:圖就是「點」加上「連線」",
  '<div class="panel"><h3>地圖、社群網路、迷宮,都是圖</h3>'
  '<p>城市是<b>點</b>,道路是<b>邊</b>;朋友是點,「互相認識」是邊;迷宮裡每個空格是點,相鄰的空格之間有邊。第 11 篇的樹其實是一種特別的圖(沒有繞圈的路、全部連在一起)。圖比樹自由:一個點可以連任意多個點,還可以繞回來形成<b>環</b>。</p>'
  '<p style="margin-bottom:0">圖要回答的常見問題:<b>從 A 走得到 B 嗎?最少要走幾步?</b>這一篇學兩件事:圖怎麼<b>存</b>進程式,以及兩種走遍整張圖的方法 <b>BFS</b> 與 <b>DFS</b>。</p></div>',
  '<h3 style="margin-top:26px">幾個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["點(vertex / node)與邊(edge)", "圖由點和連接兩點的邊組成。本篇的點用 <code>0, 1, 2…</code> 編號。"],
    ["無向 / 有向", "無向圖:邊沒有方向,A-B 就是 B-A(好友關係)。有向圖:邊有方向,A→B 不代表 B→A(單行道、追蹤)。本篇用無向圖。"],
    ["相鄰、度數", "有邊直接連著的兩個點互為<b>鄰居</b>。一個點的鄰居數叫<b>度數</b>(degree)。"],
    ["路徑、連通", "沿著邊從 A 走到 B 的一串點叫路徑。任兩點之間都有路徑,就說這張圖<b>連通</b>。"],
    ["環", "沿著邊走了一圈又回到出發點。有環的圖,走訪時一定要記錄「來過了」,否則會一直繞圈。"],
  ]))

repr_ = section("repr", "圖怎麼存:鄰接矩陣與鄰接表",
  '<p class="sub" style="margin-bottom:14px">輸入邊的清單(例如 <code>0-1 0-2 1-3</code>,點編號 0~6),按「執行」,看<b>同一張圖</b>怎麼同時存成兩種樣子。每條邊會拆成四個小步驟,逐行看程式碼改了什麼。</p>',
  try_list(["直接按「執行」,看 <code>0-1</code> 這條邊為什麼要記<b>兩次</b>(矩陣對稱、兩個 list 各加一筆)。", "按「星狀圖」:點 0 連很多點,矩陣大部分是 0,鄰接表很短。", "按「四點全連」:每兩點都有邊,矩陣填滿,兩種存法用的空間差不多。"]),
  widget("w-repr", "圖的表示法動畫"),
  '<h3 style="margin-top:26px">兩種存法的比較</h3>',
  table("g3", ["", "鄰接矩陣", "鄰接表"], [
    ["怎麼存", "<code>V × V</code> 的二維陣列,<code>m[a][b] = 1</code> 表示有邊", "每個點一個 <code>vector</code>,放它的鄰居"],
    ["空間", "<code>O(V²)</code>,不管有幾條邊", "<code>O(V + E)</code>,邊少就省"],
    ["a、b 之間有沒有邊?", "<code>O(1)</code>,直接看格子", "<code>O(度數)</code>,要掃 a 的 list"],
    ["列出 a 的所有鄰居", "<code>O(V)</code>,要掃整列", "<code>O(度數)</code>,list 就是答案"],
    ["適合", "點很少、或邊幾乎全有", "邊很少(大多數實際的圖),BFS / DFS 都用它"],
  ]),
  cpp("graph_repr"), out("graph_repr", "執行結果"), compile_cmd(),
  '<div class="tip"><b class="l">有向圖只記一半</b>有向的邊 <code>a→b</code> 只要 <code>matrix[a][b] = 1</code> 與 <code>adj[a].push_back(b)</code>,不用記回頭那一半。</div>')

maze = section("maze", "走遍整張圖:BFS 與 DFS 走迷宮",
  '<p class="sub" style="margin-bottom:14px">迷宮是最好懂的圖:每個空格是點,上下左右的空格互為鄰居。<b>BFS</b>(廣度優先)用 <b>queue</b>,一圈一圈往外擴;<b>DFS</b>(深度優先)用 <b>stack</b>,一直往前鑽,走不通才退回來。同一個迷宮,兩種走法的樣子完全不同。</p>',
  try_list(["選「有牆的迷宮」,分別按「BFS 跑一次」與「DFS 跑一次」,比較最後的步數。", "選「空地」跑 DFS:明明直走就到,它卻繞了一大圈,為什麼?(提示:看每一步新放進 stack 的格子,最後放的先出來。)", "選「沒有出口」跑 BFS:queue 空了就知道走不到。", "按「隨機迷宮」多試幾次,BFS 的步數是不是永遠 ≤ DFS?"]),
  widget("w-maze", "迷宮 BFS / DFS 動畫"),
  sim("", "猜猜看:DFS 找到的路一定最短嗎?", "DFS 先找到了終點,它走的那條路是最短的嗎?",
      [("a1", "是,先到的一定最短"), ("a2", "不一定,DFS 只保證找得到,不保證最短"), ("a3", "一定是最長的")]),
  table("g3", ["", "BFS(廣度優先)", "DFS(深度優先)"], [
    ["資料結構", "<code>queue</code>(先進先出)", "<code>stack</code>(後進先出)"],
    ["走法", "一圈一圈往外擴,先走近的", "一路往前鑽,走不通再退回"],
    ["無權重圖的最短路", "<b>保證</b>最短(第一次到就是最短)", "不保證"],
    ["適合", "最少步數、最少轉乘", "有沒有路、走完所有可能(例如第 17 篇的回溯)"],
  ]),
  '<div class="tip"><b class="l">本篇的 DFS 為什麼不用遞迴?</b>DFS 也能寫成遞迴(呼叫堆疊就是那個 stack,第 7 篇)。這裡明確用 <code>std::stack</code>,才看得到「放進去的格子」,也避免格子很多時遞迴太深 stack overflow。</div>')

code = section("code", "完整程式:bfs 與 dfs",
  '<p class="sub" style="margin-bottom:14px">兩個函式的骨架幾乎一樣:取出一個格子、看四個方向、把能走又沒到過的放進去。<b>差別只在 <code>queue</code> 換成 <code>stack</code></b>。方向順序是上、下、左、右(<code>DR</code> / <code>DC</code> 兩個陣列)。</p>',
  cpp("maze_search"), out("maze_search", "執行結果(三個迷宮:空地、有牆的、沒有出口)"), compile_cmd(),
  '<div class="tip"><b class="l">怎麼讀輸出</b>空地裡 BFS 是 10 步(往右 6、往下 4);DFS 走了 34 步,因為每次都先處理最後放進 stack 的方向,會蛇行掃過整片空地才碰到終點。第三個迷宮被牆隔開,兩個函式都回傳 <code>-1</code>。</div>')

cost = section("cost", "複雜度小表",
  '<p class="sub" style="margin-bottom:14px">V 是點數,E 是邊數。BFS 和 DFS 每個點最多放進去處理一次、每條邊最多看兩次。</p>',
  table("g3", ["情況", "時間", "額外空間"], [
    ["鄰接表上的 BFS / DFS", "<code>O(V + E)</code>", "<code>O(V)</code>(queue / stack / 已拜訪表)"],
    ["鄰接矩陣上的 BFS / DFS", "<code>O(V²)</code>(找鄰居要掃整列)", "<code>O(V)</code>"],
    ["R × C 的格子迷宮", "<code>O(R × C)</code>(每格最多 4 個鄰居)", "<code>O(R × C)</code>"],
  ]),
  '<p style="margin-top:14px">一句話:<b>走遍整張圖,每個點、每條邊只碰常數次</b>,所以和圖的大小成正比。</p>')

gotchas = section("gotchas", "初學者最常卡住的四個地方",
  details("沒有記錄「走過了」",
    '<p>圖有環時,不記錄已拜訪的點會一直繞圈,程式永遠不會結束(或 queue / stack 爆掉)。BFS 用 <code>dist</code>(<code>-1</code> 代表沒到過)、DFS 用 <code>seen</code>,都是這個用途。</p>'),
  details("BFS 要在「放進 queue 時」就標記",
    '<p>本篇 BFS 在放進 queue 的當下就設好 <code>dist</code>。如果等到取出才標記,同一個格子可能被好幾個鄰居重複放進去,浪費時間,距離也容易寫錯。</p>'),
  details("DFS 的順序和直覺相反",
    '<p>stack 是後進先出,所以<b>最後放進去的方向最先走</b>。方向陣列寫成上、下、左、右,DFS 就會先往右走。換個方向順序,走到的路就不一樣,這很正常。</p>'),
  details("邊界檢查在讀格子之後",
    '<p>要先確定 <code>0 &lt;= r &lt; 列數</code> 且 <code>0 &lt;= c &lt; 行數</code>,才能讀 <code>g[r][c]</code>。<code>isOpen</code> 把檢查包在同一個函式裡,而且 <code>&amp;&amp;</code> 會短路,前面不成立就不會去讀。</p>'))

SIM = {
  "a1": "<b>不是。</b>DFS 看到終點就停,但它走的路可能繞了很大一圈。空地的例子裡,BFS 是 10 步,DFS 卻走了 34 步。",
  "a2": "<b>正確!</b>DFS 只保證「有路就找得到」。要最少步數(無權重)得用 BFS:它一圈一圈往外擴,第一次碰到終點時走的就是最短的路。",
  "a3": "<b>不是。</b>DFS 的路可能很長也可能剛好很短,取決於方向順序與迷宮的樣子,沒有固定結論。",
}
QUIZ = quiz_cfg([
  ("無向圖的邊 0-1,在鄰接矩陣裡要怎麼記?", ["只設 matrix[0][1]", "matrix[0][1] 和 matrix[1][0] 都設成 1", "只設 matrix[1][0]"], 1, "無向圖兩個方向都要記,矩陣是對稱的。"),
  ("點很多、邊很少的圖(例如社群網路),通常用哪種存法?", ["鄰接矩陣", "鄰接表", "把二維陣列填滿"], 1, "鄰接表空間是 O(V+E),邊少時比 O(V²) 的矩陣省很多。"),
  ("沒有權重的迷宮,要找「最少步數」,該用?", ["DFS(stack)", "BFS(queue)", "先排序再二分搜尋"], 1, "BFS 一圈一圈往外擴,第一次到終點就是最短。"),
  ("走圖時如果不記錄已經到過的點,遇到有環的圖會?", ["自動跳過重複的點", "可能一直繞圈走不完", "走得更快"], 1, "必須用 dist 或 seen 記錄來過的點。"),
  ("用鄰接表時,BFS / DFS 走遍整張圖的時間是?", ["O(V + E)", "O(log V)", "一定是 O(V²)"], 0, "每個點處理一次、每條邊看常數次。"),
])

ex = ('<h3 style="margin-top:30px">動手寫(兩題)</h3>'
  '<div class="panel"><h3>第 1 題:度數最大的點</h3><p>鄰接表裡,哪個點的鄰居最多?有多個時回傳編號最小的。輸出應該是 <code>1</code>。</p>' + cpp("graph_ex1_starter") +
  details("參考答案", "<p>鄰接表裡,點 <code>i</code> 的度數就是 <code>adj[i].size()</code>。只在「嚴格大於」目前最佳時更新,就會留下編號最小的。<code>O(V)</code>。</p>" + cpp("graph_ex1", "完整答案") + out("graph_ex1")) + '</div>'
  '<div class="panel" style="margin-top:14px"><h3>第 2 題:兩點連不連通</h3><p>用 BFS 判斷點 a 到點 b 有沒有路。輸出應該是 <code>101</code>。</p>' + cpp("graph_ex2_starter") +
  details("參考答案", "<p>和迷宮的 bfs 同一個骨架:<code>seen</code> 記錄來過的點、<code>queue</code> 放待處理的點,取出的點等於 b 就回傳 true;queue 空了還沒遇到就是 false。<code>O(V + E)</code>。</p>" + cpp("graph_ex2", "完整答案") + out("graph_ex2")) + '</div>')

practice = section("practice", "動手演練:確認你真的懂了", ex, QUIZ_HTML,
  checks(["我能說出點、邊、度數、路徑、連通、環是什麼意思。",
          "我能說出鄰接矩陣與鄰接表各自怎麼存,以及什麼時候選哪個。",
          "我知道無向圖的邊要記兩次。",
          "我能說出 BFS 用 queue、DFS 用 stack,以及 BFS 才保證(無權重)最短路。",
          "我知道走圖一定要記錄已拜訪的點,否則有環會無窮迴圈。"], title="學完之後,對照這張清單"),
  resources([
    ("https://en.cppreference.com/cpp/container/queue", "std::queue", "cppreference · std::queue"),
    ("https://en.cppreference.com/cpp/container/stack", "std::stack", "cppreference · std::stack"),
  ], title="cppreference 參考頁面"))

SCRIPT = r'''
var Gr = Algo.graph;
function renderRepr(f) {
  if (!f.g) return '<div class="memnote">' + f.msg + "</div>";
  return Algo.graphHtml(f.g) + '<div class="gtri"><div class="gcol">' + Algo.matrixHtml(f.matrix) + '</div><div class="gcol">' + Algo.adjHtml(f.adj) + "</div></div>" + Algo.cellsHtml({ cells: [], chips: f.chips });
}
function reprPreset(text) { return function (v, c) { c.set("edges", text); c.run(); }; }
Algo.widget("w-repr", {
  form: [{ id: "edges", label: "邊(點編號 0~6,最多 9 條)", type: "text", value: "0-1 0-2 1-3 2-3 3-4" }],
  buttons: [{ label: "星狀圖", run: reprPreset("0-1 0-2 0-3 0-4") }, { label: "路徑圖", run: reprPreset("0-1 1-2 2-3 3-4") }, { label: "四點全連", run: reprPreset("0-1 0-2 0-3 1-2 1-3 2-3") }],
  init: function () { return null; },
  idle: function () { return { msg: "輸入邊的清單,按「執行」。" }; },
  make: function (v) { return Gr.reprRun(v.edges); },
  render: renderRepr, code: Gr.CODE_REPR, code_cap: "addEdge(亮起來的行 = 目前執行到的地方)"
});
function renderMaze(f) {
  var h = Algo.gridHtml(f.grid);
  if (f.list.label) h += Algo.cellsHtml({ rows: [{ label: f.list.label, cells: f.list.items, empty: 0 }] });
  return h + Algo.cellsHtml({ cells: [], chips: f.chips });
}
function mazeOf(name) { return name === "random" ? Gr.randomMaze() : Gr.MAZES[name]; }
function runMode(mode) { return function (v, c) { c.set("mode", mode); c.run(); }; }
Algo.widget("w-maze", {
  form: [{ id: "mode", label: "演算法", type: "select", value: "bfs", options: [["bfs", "BFS(queue)"], ["dfs", "DFS(stack)"]] },
         { id: "maze", label: "迷宮", type: "select", value: "walls", options: [["walls", "有牆的迷宮"], ["open", "空地"], ["noexit", "沒有出口"], ["random", "隨機迷宮"]] }],
  buttons: [{ label: "BFS 跑一次", run: runMode("bfs") }, { label: "DFS 跑一次", run: runMode("dfs") },
            { label: "隨機迷宮", run: function (v, c) { c.set("maze", "random"); c.run(); } }],
  init: function () { return null; },
  idle: Gr.idleMaze,
  make: function (v) { return Gr.gridRun(v.mode, mazeOf(v.maze)); },
  render: renderMaze, code: Gr.CODE_MAZE, code_cap: "bfs 與 dfs(亮起來的行 = 目前執行到的地方)"
});
'''
SPEC = dict(
  file="datastruct-graph-guide.html", dir="datastruct", eyebrow_prefix=EYEBROW, foot=FOOT,
  modules=["cells", "grid", "graph", "alg_graph"], script=SCRIPT,
  title="圖的表示與 BFS / DFS:走迷宮",
  eyebrow="第 14 篇 · 圖的表示與 BFS/DFS",
  h1="點加連線:怎麼存一張圖、怎麼走遍它",
  sub="這一篇看圖怎麼存成鄰接矩陣與鄰接表,再用迷宮動畫比較 BFS(queue)與 DFS(stack):一個一圈圈往外擴,一個一路往前鑽。",
  tldr="圖 = 點 + 邊。存法有<b>鄰接矩陣</b>(<code>O(V²)</code>)與<b>鄰接表</b>(<code>O(V+E)</code>,邊少時用)。<b>BFS</b> 用 queue,一圈圈往外擴,無權重時保證最短路;<b>DFS</b> 用 stack,一路往前鑽。走圖一定要記錄已拜訪的點,時間 <code>O(V+E)</code>。<br><small>先備:第 3 篇 vector、第 5 篇 stack 與 queue、第 7 篇遞迴。預估 20 分鐘。難度:進階。</small>",
  toc=[("what", "直覺與名詞"), ("repr", "鄰接矩陣與鄰接表"), ("maze", "BFS 與 DFS 走迷宮"), ("code", "完整程式"), ("cost", "複雜度小表"), ("gotchas", "常見錯誤"), ("practice", "動手寫與測驗")],
  body="\n\n".join([what, repr_, maze, code, cost, gotchas, practice]),
  config=dict(sim=SIM, quiz=QUIZ),
  prev=("datastruct-heap-guide.html", "堆積與優先佇列"),
  next=("datastruct-dijkstra-guide.html", "最短路徑:Dijkstra"),
)
