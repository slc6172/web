from dh import *

what = section("what", "直覺:邊有「長短」,最少步數不等於最短",
  '<div class="panel"><h3>三站直達 vs 轉兩次車,哪個比較快?</h3>'
  '<p>第 14 篇的 BFS 數的是<b>步數</b>:每走一條邊算 1。但真實的路有長短:公里數、分鐘、車資。給每條邊一個數字,叫<b>權重</b>(weight)。這時「最少步數」不一定是「總長最短」:一條邊權重 10 的直達路,可能比兩條權重 3 和 4 的路還長。</p>'
  '<p style="margin-bottom:0"><b>Dijkstra 演算法</b>(讀作「迪克斯特拉」)找的就是:從一個起點出發,到每個點的<b>總權重最小</b>的路。想法是貪心:每次從「還沒確定的點」裡挑目前距離最小的,把它的最短距離<b>確定</b>下來,再用它去更新鄰居。</p></div>',
  '<h3 style="margin-top:26px">幾個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["權重(weight)", "邊上的數字,代表走這條邊的代價(距離、時間、費用)。本篇權重都是<b>正數</b>。"],
    ["<code>dist[v]</code>", "到目前為止,從起點走到 v 找到的最短距離。一開始起點是 0,其他是 ∞(還沒走到)。"],
    ["鬆弛(relax)", "看一條邊 u→v:如果「走到 u 的距離 + 邊的權重」比目前記的 <code>dist[v]</code> 更短,就更新。就像把繃緊的繩子放鬆一點。"],
    ["確定(finalized)", "從 pq 取出、距離最小的點,它的 <code>dist</code> 之後不會再變短。"],
    ["<code>prev[v]</code>", "最短路上 v 的前一個點。從終點一路往回找,就能還原整條路。"],
    ["優先佇列", "第 13 篇的堆積。放 <code>(距離, 點)</code>,每次先拿距離最小的。"],
  ]))

play = section("play", "動手玩:看距離一步步被更新",
  '<p class="sub" style="margin-bottom:14px">選一張圖和起點,按「執行」。點上方的數字是目前的 <code>dist</code>(∞ 表示還沒走到)。<b>綠框</b>是已確定的點,<b>橘色</b>是目前處理的點,<b>淺綠</b>是剛被更新的點;綠色的邊是最短路徑樹。</p>',
  try_list(["先看「繞路更近」:起點 0 到 1 有一條權重 10 的直達邊,但最後 <code>dist[1]</code> 是多少?走哪條路?", "「經典範例」裡找「過時的舊紀錄」(訊息裡會寫):為什麼 pq 裡會有同一個點的兩筆?", "看 dist 表的變化:每個點的值是不是只會<b>變小</b>、不會變大?", "按「隨機圖」換幾張圖,試試不同起點。"]),
  widget("w-dijk", "Dijkstra 動畫(圖、距離表、優先佇列)"),
  sim("", "猜猜看:最短距離是多少?", "在「繞路更近」那張圖,起點 0 到點 1 有一條直達的邊,權重 10;另外還有 0→2(權重 3)與 2→1(權重 4)。起點 0 到點 1 的最短距離是?",
      [("a1", "10,直達最近"), ("a2", "7,繞過點 2 比較短"), ("a3", "3,因為 0→2 只要 3")]),
  '<h3 style="margin-top:26px">為什麼「每次拿最小的」就是對的?</h3>',
  '<p>假設 pq 現在給出距離最小的點 <code>u</code>,距離 <code>d</code>。如果還有更短的路到 u,那條路必須先經過某個<b>還沒確定</b>的點;但那些點的距離都 <b>≥ d</b>(因為 d 是最小的),再加上一條<b>非負</b>的邊,只會更長,不可能比 d 短。所以 u 的距離確定了。這個論證<b>依賴權重不能是負的</b>。</p>')

code = section("code", "完整程式:Dijkstra",
  '<p class="sub" style="margin-bottom:14px">骨架和 BFS 很像:一個容器放待處理的點,取出一個、看它的鄰居。差別是容器換成<b>優先佇列</b>(最小堆積,所以 <code>greater</code>),而且多了「鬆弛」那一步。<code>dist</code> 是答案,<code>prev</code> 用來還原路徑。</p>',
  cpp("dijk_ops"), out("dijk_ops", "執行結果(兩張圖:各印 dist 與到點 4 的路)"), compile_cmd(),
  '<div class="tip"><b class="l">為什麼有 <code>if (d &gt; dist[u]) continue;</code></b>STL 的 <code>priority_queue</code> 不能「修改」裡面已有的值。所以每次鬆弛成功就<b>再放一筆新的</b>,舊的留著。取出時如果發現距離比 <code>dist</code> 記的大,就是過時的紀錄,丟掉。</div>')

cost = section("cost", "複雜度小表",
  '<p class="sub" style="margin-bottom:14px">V 是點數,E 是邊數。每條邊最多讓 pq 多一筆,pq 的 push / pop 各是 <code>O(log)</code>。</p>',
  table("g3", ["演算法", "時間", "適用"], [
    ["BFS", "<code>O(V + E)</code>", "沒有權重(或權重都一樣)"],
    ["Dijkstra(priority_queue)", "<code>O((V + E) log V)</code>", "權重<b>非負</b>"],
    ["Bellman-Ford(本篇不教)", "<code>O(V × E)</code>", "可以有負權重,比較慢"],
  ]))

gotchas = section("gotchas", "初學者最常卡住的四個地方",
  details("邊的權重是負的",
    '<p>Dijkstra 的「確定了就不會變」靠的是非負權重。有負權重的邊時,之後可能出現更短的路,答案會錯。遇到負權重要改用 Bellman-Ford 之類的演算法。</p>'),
  details("INF 加權重溢位",
    '<p>如果寫成 <code>dist[u] + w</code> 而 <code>dist[u]</code> 還是 INF,<code>INF + w</code> 可能超過 <code>int</code> 範圍。本篇只對<b>從 pq 取出、一定走得到</b>的點做加法,所以安全。INF 也不要設成 <code>INT_MAX</code>。</p>'),
  details("pq 用成最大堆積",
    '<p><code>priority_queue</code> 預設最大的先出來(第 13 篇)。Dijkstra 要最小的,必須用 <code>greater</code>。寫錯時程式能跑,但答案是錯的。</p>'),
  details("無向圖的邊只加一次",
    '<p>無向圖的邊要兩個方向都放進鄰接表(<code>addEdge</code> 做了兩次 <code>push_back</code>)。只加一次,有些點會「走不回來」。</p>'))

SIM = {
  "a1": "<b>不是。</b>直達的邊權重是 10,但 0→2→1 只要 3 + 4 = 7。邊少不代表總長短,這正是 BFS 在有權重的圖上不夠用的原因。",
  "a2": "<b>正確!</b>0→2 是 3、2→1 是 4,合起來 7,比直達的 10 短。動畫最後 <code>dist[1]</code> 就是 7,<code>prev[1]</code> 是 2。",
  "a3": "<b>不是。</b>3 是到點 <b>2</b> 的距離。到點 1 還要再走 2→1(權重 4),所以是 7。",
}
QUIZ = quiz_cfg([
  ("邊有權重時,為什麼不能直接用 BFS 找總長最短的路?", ["BFS 找的是步數最少,不是總權重最小", "BFS 一定比較慢", "BFS 不能用在圖上"], 0, "BFS 把每條邊都當 1,不管權重。"),
  ("Dijkstra 每次從優先佇列取出什麼?", ["距離最小的點", "最先放進去的點", "編號最小的點"], 0, "pq 是最小堆積,取出目前距離最小的。"),
  ("「鬆弛」(relax)是指?", ["發現經過 u 走到 v 比目前記的更短,就更新 dist[v]", "把邊刪掉", "把整個 pq 清空"], 0, "d + w < dist[v] 時更新。"),
  ("Dijkstra 不能正確處理哪種圖?", ["有環的圖", "有負權重邊的圖", "無向圖"], 1, "「確定了就不會變」依賴權重非負。"),
  ("用 priority_queue 實作的 Dijkstra,時間複雜度是?", ["O(V + E)", "O((V + E) log V)", "O(V³)"], 1, "每條邊最多讓 pq 多一筆,push / pop 是 O(log)。"),
])

ex = ('<h3 style="margin-top:30px">動手寫(兩題)</h3>'
  '<div class="panel"><h3>第 1 題:還原最短路徑</h3><p>給 <code>prev</code>,回傳從起點到 target 的路徑。輸出應該是 <code>0 2 3 4</code>。</p>' + cpp("dijk_ex1_starter") +
  details("參考答案", "<p>從 target 沿著 <code>prev</code> 一路往回找,直到 <code>-1</code>(起點的 prev),這樣得到的是反過來的路徑,最後 <code>reverse</code>。</p>" + cpp("dijk_ex1", "完整答案") + out("dijk_ex1")) + '</div>'
  '<div class="panel" style="margin-top:14px"><h3>第 2 題:寫出「鬆弛」</h3><p>實作 <code>relax</code>。輸出應該是 <code>1 7 0 9 0 9</code>。注意最後一次 7 + 2 = 9 和原本一樣長,<b>不算更短</b>,不更新。</p>' + cpp("dijk_ex2_starter") +
  details("參考答案", "<p>只有「嚴格小於」才更新。用 <code>&lt;=</code> 的話,相等時也會更新並重複放進 pq,答案沒錯但做了白工。</p>" + cpp("dijk_ex2", "完整答案") + out("dijk_ex2")) + '</div>')

practice = section("practice", "動手演練:確認你真的懂了", ex, QUIZ_HTML,
  checks(["我知道有權重時「最少步數」不等於「總長最短」。",
          "我能說出 <code>dist</code>、<code>prev</code>、鬆弛、確定各是什麼意思。",
          "我能口述流程:取出 pq 裡距離最小的點、確定它、用它鬆弛每個鄰居。",
          "我知道 Dijkstra 的權重必須非負,以及 pq 要用最小堆積(<code>greater</code>)。",
          "我知道複雜度是 <code>O((V + E) log V)</code>。"], title="學完之後,對照這張清單"),
  resources([
    ("https://en.cppreference.com/cpp/container/priority_queue", "std::priority_queue", "cppreference · std::priority_queue"),
    ("https://en.cppreference.com/cpp/utility/functional/greater", "std::greater", "cppreference · std::greater"),
  ], title="cppreference 參考頁面"))

SCRIPT = r'''
var D = Algo.dijk;
function render(f) {
  var h = Algo.graphHtml(f.g);
  if (!f.dist.length) return h;
  return h + Algo.cellsHtml({ rows: [
    { label: "dist[i](∞ = 還沒走到)", cells: f.dist, empty: 0 },
    { label: "prev[i](最短路上,i 的前一個點)", cells: f.prev, empty: 0 },
    { label: "優先佇列 pq:(距離,點),最小的在左邊", cells: f.pq, empty: 0 }], chips: f.chips });
}
function preset(name) { return function (v, c) { c.set("graph", name); c.run(); }; }
Algo.widget("w-dijk", {
  form: [{ id: "graph", label: "圖", type: "select", value: "classic", options: [["classic", "經典範例(6 點)"], ["detour", "繞路更近(5 點)"], ["random", "隨機圖(6 點)"]] },
         { id: "src", label: "起點(0 開始)", type: "number", value: 0, min: 0, max: 5 }],
  buttons: [{ label: "經典範例", run: preset("classic") }, { label: "繞路更近", run: preset("detour") }, { label: "隨機圖", run: preset("random") }],
  init: function () { return null; },
  idle: D.idle,
  make: function (v) { return D.run(v.graph === "random" ? D.randomGraph() : D.PRESETS[v.graph], v.src); },
  render: render, code: D.CODE_DIJK, code_cap: "dijkstra(亮起來的行 = 目前執行到的地方)"
});
'''
SPEC = dict(
  file="datastruct-dijkstra-guide.html", dir="datastruct", eyebrow_prefix=EYEBROW, foot=FOOT,
  modules=["cells", "graph", "alg_dijk"], script=SCRIPT,
  title="最短路徑:Dijkstra 演算法",
  eyebrow="第 15 篇 · Dijkstra(進階選讀)",
  h1="邊有長短:每次確定「目前最近」的那個點",
  sub="BFS 數的是步數;邊有權重時要用 Dijkstra。這一篇用動畫看距離表一步步被更新,理解「鬆弛」與優先佇列怎麼配合。",
  tldr="Dijkstra 從起點出發,每次從優先佇列取出<b>距離最小</b>的點,把它的距離<b>確定</b>,再用它去<b>鬆弛</b>鄰居(<code>d + w &lt; dist[v]</code> 就更新)。權重必須<b>非負</b>,時間 <code>O((V + E) log V)</code>。<br><small>先備:第 13 篇堆積與 priority_queue、第 14 篇圖與 BFS。預估 18 分鐘。難度:進階(選讀)。</small>",
  toc=[("what", "直覺與名詞"), ("play", "距離表怎麼更新"), ("code", "完整程式"), ("cost", "複雜度小表"), ("gotchas", "常見錯誤"), ("practice", "動手寫與測驗")],
  body="\n\n".join([what, play, code, cost, gotchas, practice]),
  config=dict(sim=SIM, quiz=QUIZ),
  prev=("datastruct-graph-guide.html", "圖的表示與 BFS/DFS"),
  next=("datastruct-dp-guide.html", "動態規劃"),
)
