from dh import *

greedy = section("greedy", "貪婪:每一步都拿「當下最好」的,不回頭",
  '<div class="panel"><h3>找零:先拿最大的硬幣</h3>'
  '<p>找 63 元,店員會先拿 25 元、再 25 元、再 10 元……每一步都拿「拿得下的最大面額」。這就是<b>貪婪演算法</b>(greedy):<b>每一步都選當下看起來最好的,選了就不反悔</b>。程式短、速度快,但<b>不保證答案最好</b>。</p>'
  '<p style="margin-bottom:0">下面的動畫讓你試試同一個貪婪程式在不同硬幣組合下的結果:有的組合剛好對,有的會輸給第 16 篇的 DP。</p></div>',
  try_list(["先跑「美國硬幣」湊 63:貪婪用 6 枚,最少也是 6 枚,對了。", "改選「4, 3, 1」湊 6:貪婪拿 4+1+1 = 3 枚,但 3+3 只要 2 枚。", "選「5, 2」湊 6:貪婪拿了 5 之後剩 1 湊不下,卡住;其實 2+2+2 就可以。", "自己換金額多試幾次,看什麼時候貪婪會失敗。"]),
  widget("w-greedy", "貪婪找零動畫"),
  cpp("greedy_change"), out("greedy_change", "執行結果(貪婪的結果與 DP 算出的最少枚數對照)"), compile_cmd(),
  '<h3 style="margin-top:26px">貪婪什麼時候可以用?</h3>',
  table("g3", ["問題", "貪婪的做法", "對不對"], [
    ["活動安排(最多不重疊活動)", "依<b>結束時間</b>排序,能接就選", "對(可以證明),下面練習題"],
    ["找零:25、10、5、1", "先拿最大面額", "對"],
    ["找零:任意面額(如 4、3、1)", "先拿最大面額", "<b>不一定</b>(動畫看得到)"],
    ["最短路徑(正權重)", "每次確定目前最近的點", "對:第 15 篇的 Dijkstra 本身就是貪婪"],
    ["0/1 背包", "挑價值除以重量最高的", "<b>不對</b>,要用第 16 篇的 DP"],
  ]),
  '<div class="tip"><b class="l">怎麼判斷?</b>貪婪要「證明」才能放心用:要說明「這一步選最好的,不會害後面的選擇變差」。想不出證明、或很容易找到反例時,改用 DP 或回溯。</div>')

backtrack = section("backtrack", "回溯:試、錯了就退回、再試別的",
  '<div class="panel"><h3>N 皇后:在 N×N 的棋盤放 N 個皇后,互相吃不到</h3>'
  '<p>皇后會吃同欄、同列、同斜線的棋子。做法:<b>一列放一個</b>,從第 1 列開始,一欄一欄試。能放就放下、去下一列;<b>下一列每一欄都不行,就退回來</b>,把這一列的皇后拿起來換下一欄。這種「走不通就退回上一步、換另一個選擇」的方法叫<b>回溯</b>(backtracking)。</p>'
  '<p style="margin-bottom:0">回溯其實就是第 7 篇的遞迴加上「撤銷選擇」。和第 14 篇的 DFS 是同一個「一路鑽、走不通退回」的想法。</p></div>',
  try_list(["先看 N=4、「只看第一組解」,數數看嘗試了幾次、退回了幾次。", "切到「全部解」:N=4 只有 2 組解。", "改 N=6、「全部解」,拉到最後看總共嘗試多少次、有幾組解(答案是 4 組)。", "留意「×」的格子:和哪個皇后衝突(同欄或同斜線)。"]),
  widget("w-nq", "N 皇后回溯動畫"),
  cpp("nqueens"), out("nqueens", "執行結果(N = 4 到 8 的解的組數,以及 4 皇后的第一組解)"), compile_cmd(),
  '<div class="tip"><b class="l">為什麼不是試完所有擺法?</b>8 個皇后隨便放有上千萬種擺法;一列放一個、而且<b>一發現衝突就不往下走</b>(這叫<b>剪枝</b>),大部分擺法根本不用試。</div>')

stl = section("stl", "STL 速查表:vector、map、set 到底選哪個?",
  '<p class="sub" style="margin-bottom:14px">先看常見需求,再用下面的表篩選、搜尋容器與演算法。「本系列」欄是這個網站講過它的那一篇。</p>',
  table("g2", ["我需要", "選這個"], [
    ["一般的清單,不確定選什麼", "<code>vector</code>(預設首選)"],
    ["用 key 找 value,不在乎順序", "<code>unordered_map</code>(平均 <code>O(1)</code>)"],
    ["key 要排序、或要找「第一個 ≥ x」", "<code>map</code> / <code>set</code>(<code>O(log n)</code>)"],
    ["去掉重複、判斷有沒有", "<code>unordered_set</code>(要排序就用 <code>set</code>)"],
    ["先進先出 / 後進先出", "<code>queue</code> / <code>stack</code>"],
    ["每次拿最大(或最小)的", "<code>priority_queue</code>"],
    ["頭尾都要快速增刪", "<code>deque</code>"],
  ]),
  '<div class="filterbar" role="group" aria-label="篩選類別" id="stl-filters"></div>'
  '<input id="stl-q" class="filterq" type="search" placeholder="搜尋名稱、標頭、特性…(例如 sort、log、queue)" aria-label="搜尋 STL 速查表">'
  '<div id="stl-count" class="filtercount" aria-live="polite"></div>'
  '<div class="table-wrap"><div class="gt g5" id="stl-table"></div></div>')

route = section("route", "學完之後:刷題路線",
  '<p class="sub" style="margin-bottom:14px">每個階段先挑 2~3 題。題名可以直接在 LeetCode 等練習平台搜尋(這裡不附連結,連結容易失效)。</p>',
  table("g3", ["階段(對應本系列)", "練習題(題名)", "練的是什麼"], [
    ["1. 熱身(第 3~5、10 篇)", "Two Sum、Valid Parentheses、Reverse Linked List、Best Time to Buy and Sell Stock", "vector、map、stack、鏈結串列的基本功"],
    ["2. 搜尋與排序(第 6、8、9 篇)", "Binary Search、Sort Colors、Merge Intervals", "二分搜尋的邊界、排序後再處理"],
    ["3. 遞迴與樹(第 7、11、12 篇)", "Maximum Depth of Binary Tree、Invert Binary Tree、Validate Binary Search Tree", "遞迴思考、樹的走訪、BST 規則"],
    ["4. 堆積與圖(第 13~15 篇)", "Kth Largest Element in an Array、Number of Islands、Shortest Path in Binary Matrix、Network Delay Time", "priority_queue、BFS / DFS、Dijkstra"],
    ["5. DP、貪婪、回溯(第 16、17 篇)", "Climbing Stairs、Coin Change、Jump Game、Subsets、N-Queens", "填表、貪婪、試與退回"],
  ]),
  '<div class="tip"><b class="l">每題的固定流程</b>① 先花 15~20 分鐘自己想,不要馬上看答案 ② 先寫暴力解,說得出它的複雜度 ③ 想「這題像本系列的哪一篇」 ④ 寫完用自己的話解釋為什麼對、時間與空間各是多少 ⑤ 隔幾天不看筆記再寫一次。</div>')

gotchas = section("gotchas", "初學者最常卡住的四個地方",
  details("貪婪沒想過反例就直接用",
    '<p>貪婪的程式短又快,很容易「看起來對」。先用小例子找反例(像 <code>{4,3,1}</code> 湊 6);找得到反例就換 DP。找不到也要能說出「為什麼這一步選最好不會害到後面」。</p>'),
  details("回溯忘了撤銷選擇",
    '<p>遞迴回來之後,要把剛才做的選擇<b>還原</b>:放了皇后要拿起來、<code>push_back</code> 的要 <code>pop_back</code>、設成 <code>true</code> 的 <code>visited</code> 要設回 <code>false</code>。忘了還原,下一個選擇會在「髒掉」的狀態上試,答案錯得很奇怪。</p>'),
  details("沒有剪枝,速度爆炸",
    '<p>回溯本質是「試所有可能」,不剪枝就是指數時間。好的回溯在<b>確定走不通</b>的那一刻就退回(像 <code>safe</code> 一發現衝突就不放),而不是放滿再檢查。</p>'),
  details("容器選錯",
    '<p>常見的:在 <code>vector</code> 中間頻繁插入刪除(<code>O(n)</code>)、需要排序走訪卻用 <code>unordered_map</code>、只要判斷有沒有卻用 <code>vector</code> 一個一個找。先看上面「我需要」那張表。</p>'))

SIM = {}
QUIZ = quiz_cfg([
  ("貪婪演算法的特徵是?", ["每一步都選當下最好的,而且不回頭", "把所有可能都試一遍", "把算過的答案記在表裡"], 0, "不回頭,所以快,但不保證整體最好。"),
  ("硬幣 {4, 3, 1} 湊 6,貪婪會拿?", ["4、1、1,共 3 枚", "3、3,共 2 枚", "湊不出來"], 0, "先拿最大的 4,剩 2,再拿兩個 1。最少其實是 3 + 3。"),
  ("回溯法的重點是?", ["走不通就退回上一步,換另一個選擇", "一路往前不回頭", "先排序再二分搜尋"], 0, "試、錯了就撤銷選擇、再試別的。"),
  ("N 皇后「一列只放一個」的好處是?", ["保證不會有兩個皇后同一列,大幅縮小要試的範圍", "讓程式碼變短而已", "棋盤規定一定要這樣"], 0, "同列衝突不用檢查,而且只剩下欄與斜線要判斷。"),
  ("想要「依 key 排序,還能找第一個 ≥ x」的容器?", ["std::map 或 std::set", "std::unordered_map", "std::vector 搭配 find"], 0, "map / set 是有序的,可以用 lower_bound,時間 O(log n)。"),
])

ex = ('<h3 style="margin-top:30px">動手寫(兩題)</h3>'
  '<div class="panel"><h3>第 1 題:活動安排(貪婪)</h3><p>最多能安排幾個時間不重疊的活動?輸出應該是 <code>4</code>。</p>' + cpp("greedy_ex1_starter") +
  details("參考答案", "<p>依<b>結束時間</b>排序,從最早結束的開始選,能接上(開始時間 ≥ 上一個選的結束時間)就選。早點結束,留給後面的時間最多。時間 <code>O(n log n)</code>(排序)。</p>" + cpp("greedy_ex1", "完整答案") + out("greedy_ex1")) + '</div>'
  '<div class="panel" style="margin-top:14px"><h3>第 2 題:有幾種挑法湊出總和(回溯)</h3><p>輸出應該是 <code>2 3 0</code>。<code>{2,3,5,7}</code> 湊 10 有 3+7、2+3+5 兩種。</p>' + cpp("backtrack_ex2_starter") +
  details("參考答案", "<p>每個位置兩種選擇:<b>挑</b>(剩下的目標減掉它)與<b>不挑</b>,都遞迴下去。走到最後一個位置時,剩下目標剛好是 0 才算一種。時間 <code>O(2ⁿ)</code>。因為用函式參數傳 <code>remain</code>,不需要手動撤銷選擇。</p>" + cpp("backtrack_ex2", "完整答案") + out("backtrack_ex2")) + '</div>')

practice = section("practice", "動手演練:確認你真的懂了", ex, QUIZ_HTML,
  checks(["我能說出貪婪的做法,以及它為什麼不保證最好(舉得出反例)。",
          "我能用「試、錯了退回、再試」說明回溯,並說出為什麼要撤銷選擇、要剪枝。",
          "我能依需求選 vector、map、set、unordered_map、queue、priority_queue。",
          "我知道刷題的流程:先自己想、先暴力解、想像哪一篇、用自己的話解釋。"], title="學完之後,對照這張清單"),
  resources([
    ("https://en.cppreference.com/cpp/container", "C++ 容器總覽", "cppreference · Containers library"),
    ("https://en.cppreference.com/cpp/algorithm", "C++ 演算法總覽", "cppreference · Algorithms library"),
  ], title="cppreference 參考頁面"))

SCRIPT = r'''
var Q = Algo.greedy;
function gPreset(set, amount) { return function (v, c) { c.set("set", set); c.set("amount", amount); c.run(); }; }
Algo.widget("w-greedy", {
  form: [{ id: "set", label: "硬幣面額", type: "select", value: "us", options: Object.keys(Q.SETNAMES).map(function (k) { return [k, Q.SETNAMES[k]]; }) },
         { id: "amount", label: "要湊的金額(1–99)", type: "number", value: 63, min: 1, max: 99 }],
  buttons: [{ label: "美國硬幣 63", run: gPreset("us", 63) }, { label: "4,3,1 湊 6", run: gPreset("f1", 6) }, { label: "5,2 湊 6", run: gPreset("f3", 6) }],
  init: function () { return null; },
  idle: Q.idleGreedy,
  make: function (v) { return Q.greedyRun(v.set, v.amount); },
  render: function (f) { return f.rows.length ? Algo.cellsHtml({ rows: f.rows, chips: f.chips }) : ""; },
  code: Q.CODE_GREEDY, code_cap: "greedyChange(亮起來的行 = 目前執行到的地方)"
});
function nPreset(n, mode) { return function (v, c) { c.set("n", String(n)); c.set("mode", mode); c.run(); }; }
Algo.widget("w-nq", {
  form: [{ id: "n", label: "N(棋盤大小)", type: "select", value: "4", options: [["4", "4"], ["5", "5"], ["6", "6"]] },
         { id: "mode", label: "模式", type: "select", value: "first", options: [["first", "只看第一組解"], ["all", "全部解"]] }],
  buttons: [{ label: "4 皇后 第一組", run: nPreset(4, "first") }, { label: "4 皇后 全部", run: nPreset(4, "all") }, { label: "6 皇后 全部", run: nPreset(6, "all") }],
  init: function () { return null; },
  idle: Q.idleNq,
  make: function (v) { return Q.nqRun(parseInt(v.n, 10), v.mode); },
  render: function (f) { return Algo.boardHtml(f) + Algo.cellsHtml({ cells: [], chips: f.chips }); },
  code: Q.CODE_NQ, code_cap: "safe 與 solve(亮起來的行 = 目前執行到的地方)"
});

/* ---- STL 速查表(篩選 + 搜尋) ---- */
var CATS = ["全部", "序列容器", "容器介面卡", "有序關聯", "雜湊容器", "演算法"];
var ROWS = [
  ["vector", "&lt;vector&gt;", "序列容器", "連續的動態陣列,預設首選。", "[i] <code>O(1)</code>;尾端 push_back 均攤 <code>O(1)</code>;中間插入刪除 <code>O(n)</code>", "第 3 篇"],
  ["array", "&lt;array&gt;", "序列容器", "大小固定的陣列(編譯時決定)。", "[i] <code>O(1)</code>", "第 3 篇"],
  ["string", "&lt;string&gt;", "序列容器", "字元序列,用法像 vector&lt;char&gt;。", "[i] <code>O(1)</code>;尾端附加均攤 <code>O(1)</code>", "第 3 篇"],
  ["list", "&lt;list&gt;", "序列容器", "雙向鏈結串列,不能用 [i]。", "已知位置插入刪除 <code>O(1)</code>;找第 k 個 <code>O(n)</code>", "第 4 篇"],
  ["forward_list", "&lt;forward_list&gt;", "序列容器", "單向鏈結串列,更省記憶體。", "已知位置之後插入 <code>O(1)</code>", "第 4 篇"],
  ["deque", "&lt;deque&gt;", "序列容器", "頭尾都能快速增刪,支援 [i]。", "頭尾增刪 <code>O(1)</code>;[i] <code>O(1)</code>", "第 5 篇"],
  ["stack", "&lt;stack&gt;", "容器介面卡", "後進先出,只能操作最上面。", "push / pop / top <code>O(1)</code>", "第 5 篇"],
  ["queue", "&lt;queue&gt;", "容器介面卡", "先進先出,從尾放、從頭取。", "push / pop / front <code>O(1)</code>", "第 5 篇"],
  ["priority_queue", "&lt;queue&gt;", "容器介面卡", "每次取出最大(預設)的;最小堆積要加 greater。", "push / pop <code>O(log n)</code>;top <code>O(1)</code>", "第 13 篇"],
  ["set", "&lt;set&gt;", "有序關聯", "不重複、自動排序(通常是紅黑樹)。", "插入 / 查詢 / 刪除 <code>O(log n)</code>", "第 12 篇"],
  ["map", "&lt;map&gt;", "有序關聯", "key → value,依 key 排序。", "插入 / 查詢 / 刪除 <code>O(log n)</code>", "第 12 篇"],
  ["multiset / multimap", "&lt;set&gt; / &lt;map&gt;", "有序關聯", "允許重複的 set / map。", "<code>O(log n)</code>", "第 12 篇"],
  ["unordered_set", "&lt;unordered_set&gt;", "雜湊容器", "不重複、不排序,雜湊表。", "平均 <code>O(1)</code>,最壞 <code>O(n)</code>", "第 10 篇"],
  ["unordered_map", "&lt;unordered_map&gt;", "雜湊容器", "key → value,雜湊表,不排序。", "平均 <code>O(1)</code>,最壞 <code>O(n)</code>", "第 10 篇"],
  ["sort", "&lt;algorithm&gt;", "演算法", "排序一段範圍(不穩定,通常是 introsort)。", "<code>O(n log n)</code>", "第 8、9 篇"],
  ["stable_sort", "&lt;algorithm&gt;", "演算法", "穩定排序:相等的元素保持原本的先後。", "<code>O(n log n)</code>", "第 9 篇"],
  ["binary_search / lower_bound / upper_bound", "&lt;algorithm&gt;", "演算法", "在<b>已排序</b>的範圍二分搜尋;lower_bound 回傳第一個 ≥ x 的位置。", "<code>O(log n)</code>(隨機存取迭代器)", "第 6 篇"],
  ["find / count", "&lt;algorithm&gt;", "演算法", "線性找值、數出現次數。", "<code>O(n)</code>", "第 2、6 篇"],
  ["reverse / swap", "&lt;algorithm&gt; / &lt;utility&gt;", "演算法", "反轉一段範圍、交換兩個值。", "reverse <code>O(n)</code>;swap <code>O(1)</code>", "第 3 篇"],
  ["min_element / max_element", "&lt;algorithm&gt;", "演算法", "回傳最小 / 最大元素的迭代器。", "<code>O(n)</code>", "第 2 篇"],
  ["make_heap / push_heap / pop_heap", "&lt;algorithm&gt;", "演算法", "在 vector 上直接做堆積(最大堆積)。", "make_heap <code>O(n)</code>;push / pop <code>O(log n)</code>", "第 13 篇"],
  ["next_permutation", "&lt;algorithm&gt;", "演算法", "依字典序產生下一個排列,用來列舉全部排列。", "<code>O(n)</code> / 次", "第 17 篇"],
  ["accumulate", "&lt;numeric&gt;", "演算法", "把一段範圍加總(也可自訂運算)。", "<code>O(n)</code>", "第 2 篇"]
];
Algo.stlFilter({ cats: CATS, rows: ROWS, filters: "stl-filters", q: "stl-q", table: "stl-table", count: "stl-count" });
'''
SPEC = dict(
  file="datastruct-greedy-guide.html", dir="datastruct", eyebrow_prefix=EYEBROW, foot=FOOT,
  modules=["cells", "board", "alg_greedy", "stlfilter"], script=SCRIPT,
  title="貪婪、回溯與練習路線",
  eyebrow="第 17 篇 · 貪婪、回溯與練習路線(進階選讀)",
  h1="不回頭的貪婪、會退回的回溯,以及接下來怎麼練",
  sub="貪婪每一步選當下最好的,快但不一定對;回溯試了走不通就退回再試。這一篇用找零與 N 皇后動畫看兩者,最後附上可篩選的 STL 速查表與刷題路線。",
  tldr="<b>貪婪</b>:每一步選當下最好的、不回頭,快,但要有證明或找不到反例才能用(找零 {4,3,1} 會失敗)。<b>回溯</b>:試、走不通就撤銷選擇退回、再試別的,要剪枝。學完全系列後,用速查表選容器,照路線刷題。<br><small>先備:第 7 篇遞迴、第 14 篇 DFS、第 16 篇 DP。預估 22 分鐘。難度:進階(選讀)。</small>",
  toc=[("greedy", "貪婪找零"), ("backtrack", "回溯與 N 皇后"), ("stl", "STL 速查表"), ("route", "刷題路線"), ("gotchas", "常見錯誤"), ("practice", "動手寫與測驗")],
  body="\n\n".join([greedy, backtrack, stl, route, gotchas, practice]),
  config=dict(sim=SIM, quiz=QUIZ),
  prev=("datastruct-dp-guide.html", "動態規劃"),
  next=None,
)
