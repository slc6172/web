from dh import *

what = section("what", "猜數字遊戲:每次猜中間,一次砍掉一半",
  '<div class="panel"><h3>兩種找法</h3>'
  '<p>朋友心裡想 1 到 100 的一個數字。<strong>笨方法</strong>:從 1 開始一個個猜,最壞要猜 100 次。<strong>聰明方法</strong>:每次猜中間值 50,朋友只要說「大了」或「小了」,你就能一次排除一半,頂多 7 次就猜中。</p>'
  '<p style="margin-bottom:0">前者是<b>線性搜尋</b>,後者是<b>二分搜尋</b>。聰明方法有個前提:數字有大小順序,也就是資料要<strong>已排序</strong>。</p></div>',
  '<h3 style="margin-top:26px">名詞對照</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["線性搜尋", "從頭到尾一個個比對。不要求排序,時間 <code>O(n)</code>。"],
    ["二分搜尋", "每次看中間,決定留左半或右半。要求已排序,時間 <code>O(log n)</code>。"],
    ["<code>lo</code> / <code>hi</code> / <code>mid</code>", "目前還可能有答案的範圍左端、右端與中間。"],
    ["回傳 <code>-1</code>", "本站的約定:找不到就回傳 -1;找到就回傳索引。"],
  ]))

play = section("play", "動手玩:線性與二分搜尋逐步比較",
  '<p class="sub" style="margin-bottom:14px">資料是一個已排序的陣列。選一種搜尋法、設一個目標,逐步看它怎麼找。右上角的「比較次數」是這一篇的重點。</p>',
  try_list(["先用<b>線性搜尋</b>找 58,記下比較次數。", "再用<b>二分搜尋</b>找同一個 58,比較次數差多少?", "按「目標:不存在」,看兩種方法怎麼判斷找不到。", "按「重新產生資料」,多試幾次。"]),
  widget("w-search", "搜尋動畫"),
  sim("", "猜猜看:這一步會發生什麼?", "已排序的 1000 筆資料,二分搜尋<b>最壞情況</b>要比幾次?",
      [("a1", "約 10 次"), ("a2", "約 500 次"), ("a3", "1000 次")]),
  '<h3 style="margin-top:22px">資料量變大時,差距有多誇張</h3>',
  widget("w-worst", "最壞比較次數計算"))

code = section("code", "完整程式:兩種搜尋",
  '<p class="sub" style="margin-bottom:14px">兩個函式都回傳「找到的索引」,找不到回傳 -1。</p>',
  cpp("search_ops"), out("search_ops", "執行結果(找 23 與找 7)"),
  table("g2", ["看不懂的地方", "說明"], [
    ["<code>lo &lt;= hi</code>", "範圍裡還有至少一個元素時才繼續。lo 超過 hi,表示範圍空了,沒找到。"],
    ["<code>mid = lo + (hi - lo) / 2</code>", "取中間。不直接寫 <code>(lo + hi) / 2</code>,是因為資料量很大時 <code>lo + hi</code> 可能超出 int 範圍。"],
    ["<code>lo = mid + 1</code> / <code>hi = mid - 1</code>", "已經看過 mid 了,所以新範圍要<b>跳過 mid</b>。少了 ±1 可能卡住不動。"],
  ]))

stl = section("stl", "實務上:std::find 與 std::binary_search",
  '<p class="sub" style="margin-bottom:14px">標準函式庫都有現成的,放在 <code>&lt;algorithm&gt;</code>。回傳的是「迭代器」(指向元素的位置),減去 <code>v.begin()</code> 就是索引。</p>',
  cpp("search_stl"), out("search_stl"),
  table("g2", ["函式", "用途"], [
    ["<code>std::find</code>", "線性搜尋,不要求排序;找不到回傳 <code>v.end()</code>。"],
    ["<code>std::binary_search</code>", "二分搜尋,只回答「有沒有」(true/false);要求已排序。"],
    ["<code>std::lower_bound</code>", "二分搜尋,回傳第一個「大於等於目標」的位置。動手寫第 2 題就是它。"],
  ]))

cost = section("cost", "複雜度小表",
  table("g3", ["方法", "時間", "空間"], [
    ["線性搜尋", "最壞 O(n)", "O(1)"],
    ["二分搜尋", "最壞 O(log n)", "O(1)(迴圈版)"],
    ["先排序再二分", "排序要 O(n log n)", "資料要找很多次時才划算(第 9 篇)"],
  ]),
  '<p style="margin-top:14px">二分搜尋每次砍一半,n = 1,000,000 也只需要約 20 次。但如果資料只找一次、又還沒排序,直接線性搜尋反而最划算(排序本身比找一次貴)。</p>')

gotchas = section("gotchas", "初學者最常卡住的三個地方",
  details("對沒排序的資料用二分搜尋,結果是錯的",
    '<p>二分搜尋靠「中間比目標大,所以目標在左邊」這個推論,資料沒排序就不成立。下面的陣列裡明明有 1(索引 3),二分搜尋卻回傳 -1:</p>' + cpp("search_unsorted", "main.cpp(節錄 main 之前相同)", copy=False) + out("search_unsorted", "執行結果(二分、線性)")),
  details("寫成 <code>lo = mid</code>,程式卡住不動",
    '<p>如果範圍剩兩個元素,<code>mid</code> 會等於 <code>lo</code>。這時寫 <code>lo = mid</code> 範圍完全沒縮小,迴圈永遠不結束。記得 <code>lo = mid + 1</code>、<code>hi = mid - 1</code>。</p>'),
  details("<code>(lo + hi) / 2</code> 為什麼有人說不好?",
    '<p>當 lo 和 hi 都很大(接近 int 上限的一半以上)時,相加會溢位變成負數。<code>lo + (hi - lo) / 2</code> 不會。小資料看不出差別,但這是好習慣。</p>'))

SIM = {
  "a1": "<b>正確!</b>1000 → 500 → 250 → …,大約砍 10 次就剩 1 個(⌊log₂1000⌋ + 1 = 10)。拉動下面的計算器看更大的 n。",
  "a2": "<b>不是。</b>500 是「砍一次」之後剩下的數量,不是比較次數。二分搜尋每次都砍一半,所以次數是 log₂ n。",
  "a3": "<b>不是。</b>1000 次是線性搜尋最壞的情況。二分搜尋每次可以排除一半,遠少於 1000 次。",
}
QUIZ = quiz_cfg([
  ("二分搜尋<b>一定要</b>滿足的前提是?", ["資料已排序", "資料沒有重複", "資料量是 2 的次方"], 0, "靠大小關係排除一半,沒排序就不成立。"),
  ("已排序的 1,000,000 筆資料,二分搜尋最壞大約比幾次?", ["約 20 次", "約 1000 次", "約 500,000 次"], 0, "log₂(1,000,000) ≈ 20。"),
  ("<code>v[mid] &lt; target</code> 成立時,下一步是?", ["<code>lo = mid + 1</code>", "<code>hi = mid - 1</code>", "<code>lo = mid</code>"], 0, "mid 比目標小,目標只可能在右邊,而且 mid 本身看過了,所以從 mid + 1 開始。"),
  ("在<b>沒排序</b>的資料裡找一個值,最適合用?", ["線性搜尋", "二分搜尋", "兩個都不行"], 0, "沒排序時只能一個個找。要用二分搜尋得先排序。"),
  ("<code>std::lower_bound</code> 回傳什麼?", ["第一個大於等於目標的位置", "目標的索引(找不到回傳 -1)", "是否找到(true/false)"], 0, "它回傳迭代器,指向第一個不小於目標的元素。"),
])

ex = ('<h3 style="margin-top:30px">動手寫(兩題)</h3>'
  '<div class="panel"><h3>第 1 題:補上縮小範圍的那一行</h3><p>這份二分搜尋少了「目標在左半邊」的處理。補上一行,輸出要是 <code>5 -1</code>。</p>' + cpp("search_ex1_starter") +
  details("參考答案", "<p>目標在左邊,右端要縮到 mid 的前一個:<code>hi = mid - 1;</code>。</p>" + cpp("search_ex1", "完整答案") + out("search_ex1")) + '</div>'
  '<div class="panel" style="margin-top:14px"><h3>第 2 題:寫出 lowerBound</h3><p>完成 <code>lowerBound</code>:回傳第一個「大於等於 target」的索引,都比 target 小就回傳 <code>v.size()</code>。輸出應該是 <code>1 3 5 0</code>。</p>' + cpp("search_ex2_starter") +
  details("參考答案", "<p>這一版的範圍是 <code>[lo, hi)</code>(hi 取不到)。mid 小於 target,答案在右邊,<code>lo = mid + 1</code>;否則 mid 本身可能就是答案,<code>hi = mid</code>。範圍縮到空,lo 就是答案。時間 O(log n)。</p>" + cpp("search_ex2", "完整答案") + out("search_ex2")) + '</div>')

practice = section("practice", "動手演練:確認你真的懂了", ex, QUIZ_HTML,
  checks(["我知道線性搜尋是 O(n),二分搜尋是 O(log n)。",
          "我知道二分搜尋要求資料已排序。",
          "我看得懂 lo、hi、mid 怎麼隨著比較結果縮小範圍。",
          "我知道為什麼要寫 <code>mid + 1</code> 與 <code>mid - 1</code>。",
          "我知道 <code>std::find</code>、<code>std::binary_search</code>、<code>std::lower_bound</code> 各做什麼。",
          "我能判斷:資料只找一次且沒排序時,直接線性搜尋就好。"], title="學完之後,對照這張清單"),
  resources([
    ("https://en.cppreference.com/cpp/algorithm/find", "std::find", "cppreference · std::find"),
    ("https://en.cppreference.com/cpp/algorithm/binary_search", "std::binary_search", "cppreference · std::binary_search"),
    ("https://en.cppreference.com/cpp/algorithm/lower_bound", "std::lower_bound", "cppreference · std::lower_bound"),
  ], title="cppreference 參考頁面"))

SCRIPT = r'''
var S = Algo.search;
Algo.widget("w-search", {
  form: [{ id: "algo", label: "搜尋法", type: "select", value: "linear", options: [["linear", "線性搜尋"], ["binary", "二分搜尋"]] },
         { id: "t", label: "目標", type: "number", min: 0, max: 99, value: 58 }],
  buttons: [
    { label: "重新產生資料", run: function (v, c) { c.setBase(S.randomSorted(15)); } },
    { label: "目標:存在", run: function (v, c) { c.set("t", c.base[Math.floor(Math.random() * c.base.length)]); } },
    { label: "目標:不存在", run: function (v, c) { var t; do { t = 1 + Math.floor(Math.random() * 99); } while (c.base.indexOf(t) !== -1); c.set("t", t); } }
  ],
  init: function () { return [3, 8, 15, 22, 29, 34, 41, 47, 53, 58, 64, 71, 79, 86, 93]; },
  idle: function (b) { return { cells: b.map(function (v) { return { v: v, cls: "" }; }), chips: [["資料個數", b.length]], msg: "資料已經排好序。選搜尋法、設目標,按「執行」。" }; },
  make: function (v, base) { return v.algo === "linear" ? S.linear(base, v.t) : S.binary(base, v.t); },
  render: Algo.cellsHtml, code: S.CODE_SEARCH, code_cap: "兩個搜尋函式(亮起來的行 = 目前執行到的地方)"
});
(function () {
  var root = document.getElementById("w-worst"); root.classList.add("cv");
  root.innerHTML = '<div class="cv-top"><label for="w-worst-k">資料量 n = 2 的 k 次方</label><input id="w-worst-k" type="range" min="1" max="30" value="10"><span class="cv-n" aria-live="polite"></span></div>' +
    '<table class="cv-tbl"><thead><tr><th>方法</th><th>最壞要比幾次</th></tr></thead><tbody></tbody></table><p class="cv-note">二分搜尋的次數 = ⌊log₂ n⌋ + 1。</p>';
  var r = root.querySelector("input"), nEl = root.querySelector(".cv-n"), tb = root.querySelector("tbody");
  function draw() {
    var k = +r.value, n = Math.pow(2, k), w = S.worst(n);
    nEl.textContent = "n = " + n.toLocaleString("en-US");
    tb.innerHTML = "<tr><td>線性搜尋</td><td>" + w.linear.toLocaleString("en-US") + "</td></tr><tr><td>二分搜尋</td><td>" + w.binary + "</td></tr><tr><td>差距</td><td>約 " + Math.round(w.linear / w.binary).toLocaleString("en-US") + " 倍</td></tr>";
  }
  r.addEventListener("input", draw); draw();
})();
'''
SPEC = dict(
  file="datastruct-search-guide.html", dir="datastruct", eyebrow_prefix=EYEBROW, foot=FOOT,
  modules=["cells", "alg_search", "curves"], script=SCRIPT,
  title="搜尋:從頭找到尾,與每次砍一半",
  eyebrow="第 6 篇 · 搜尋",
  h1="已排序的資料,每次砍一半就能找得又快又準",
  sub="線性搜尋一個個比,二分搜尋每次排除一半。這一篇用動畫並排看兩種方法的比較次數,體會 O(n) 和 O(log n) 的差距。",
  tldr="線性搜尋 <code>O(n)</code>,不要求排序;二分搜尋 <code>O(log n)</code>,<b>要求已排序</b>,靠 <code>lo</code>/<code>hi</code>/<code>mid</code> 每次砍掉一半。n = 1,000,000 時,最壞只要比約 20 次。<br><small>先備:第 2 篇 Big‑O、第 3 篇 vector。預估 12 分鐘。難度:基礎。</small>",
  toc=[("what", "直覺:猜數字"), ("play", "逐步比較"), ("code", "完整程式"), ("stl", "STL"), ("cost", "複雜度小表"), ("gotchas", "常見錯誤"), ("practice", "動手寫與測驗")],
  body="\n\n".join([what, play, code, stl, cost, gotchas, practice]),
  config=dict(sim=SIM, quiz=QUIZ),
  prev=("datastruct-stackqueue-guide.html", "堆疊與佇列"),
  next=("datastruct-recursion-guide.html", "遞迴"),
)
