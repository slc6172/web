from dh import *

what = section("what", "直覺:別把同一件事算很多次",
  '<div class="panel"><h3>第 7 篇的 fib,慢在哪裡?</h3>'
  '<p>遞迴版 <code>fib(30)</code> 會呼叫將近 <b>270 萬次</b>,因為 <code>fib(28)</code>、<code>fib(27)</code> 這些小問題被一再重複計算。<b>動態規劃</b>(dynamic programming,簡稱 DP)的想法很簡單:<b>算過的答案記下來,下次直接查表</b>。</p>'
  '<p style="margin-bottom:0">能用 DP 的問題有兩個特徵:大問題可以拆成<b>小問題</b>,而且<b>很多小問題是重複的</b>。</p></div>',
  cpp("dp_memo"), out("dp_memo", "執行結果:同一個 fib(30)"),
  '<h3 style="margin-top:26px">兩種寫法,想法一樣</h3>',
  table("g3", ["", "由上而下(記憶化)", "由下而上(填表)"], [
    ["做法", "照遞迴的樣子寫,多一個 <code>memo</code> 陣列記答案,查到就直接回傳", "從最小的問題開始,<b>一格一格填表</b>,後面的格子用前面的算"],
    ["上面程式", "<code>fibMemo</code>(<code>memo[n] != -1</code> 就不用再算)", "下面的 <code>fib</code>、<code>climbStairs</code>、<code>knapsack</code>"],
    ["好處", "不用想填表順序", "沒有遞迴,不會 stack overflow,通常更快"],
  ]),
  '<div class="tip"><b class="l">本篇用「填表」</b>因為填表的過程可以一格一格看。想 DP 問題的步驟:① 定義 <code>dp</code> 的意思 ② 寫出「這格怎麼用前面的格子算」 ③ 決定起始值與填表順序 ④ 找出答案在哪一格。</div>')

play = section("play", "動手玩:一格一格填表",
  '<p class="sub" style="margin-bottom:14px">選問題,按「執行」。<b>橘色</b>是正在填的格子,<b>綠色</b>是它依賴的格子(要先填好)。費氏與爬樓梯是一排格子,<b>0/1 背包</b>是一張二維的表(物品:重 1 值 1、重 3 值 4、重 4 值 5、重 5 值 7)。</p>',
  try_list(["先跑費氏 n=8,看每一格是不是只用到前面兩格。", "再跑爬樓梯 n=8:算式一樣,但起始值是 <code>dp[0] = 1</code>,答案不同。", "跑 0/1 背包(容量 7):每一格都在比「不拿」和「拿」哪個價值大。", "把背包容量改成 3、5、10 看看答案怎麼變。"]),
  widget("w-dp", "DP 填表動畫"),
  sim("", "猜猜看:爬樓梯有幾種方法?", "一次可以爬 1 階或 2 階,爬到第 4 階有幾種不同的爬法?",
      [("a1", "4 種"), ("a2", "5 種"), ("a3", "8 種")]),
  '<h3 style="margin-top:26px">點格子看依賴(背包,容量 7)</h3>',
  '<p class="sub" style="margin-bottom:12px">這是填完的背包表。點任何一格,看它是從哪些格子算出來的:每一格最多只依賴<b>上一列的兩格</b>。</p>',
  '<div class="panel"><div id="w-deps"></div></div>')

code = section("code", "完整程式:三個 DP",
  '<p class="sub" style="margin-bottom:14px">三題的骨架一樣:<b>先建 <code>dp</code> 表、填起始值、照順序用前面的格子算出後面的</b>。注意 <code>dp</code> 要用 <code>long long</code>,費氏數列長大得很快。</p>',
  cpp("dp_ops"), out("dp_ops", "執行結果"), compile_cmd(),
  '<div class="tip"><b class="l">背包那一行在做什麼</b><code>dp[i][w]</code> 是「只考慮前 i 個物品、容量 w」的最大價值。物品 i 要嘛<b>不拿</b>(= 上面那格),要嘛<b>拿</b>(= 容量少掉它的重量那格 + 它的價值),取較大的。這就是 0/1 的意思:每個物品只能拿 0 個或 1 個。</div>')

cost = section("cost", "複雜度小表",
  '<p class="sub" style="margin-bottom:14px">DP 的時間大多等於「表有幾格 × 每格要看幾個格子」。</p>',
  table("g3", ["問題", "不用 DP", "DP"], [
    ["fib(n)", "遞迴 <code>O(2ⁿ)</code>(fib(30) 約 270 萬次)", "<code>O(n)</code>"],
    ["爬樓梯", "遞迴 <code>O(2ⁿ)</code>", "<code>O(n)</code>"],
    ["0/1 背包(n 個物品、容量 W)", "試遍所有取捨 <code>O(2ⁿ)</code>", "<code>O(n × W)</code>,表有 (n+1) × (W+1) 格"],
  ]),
  '<p style="margin-top:14px">一句話:<b>DP 用空間換時間</b>,把指數時間變成「表的大小」。</p>')

gotchas = section("gotchas", "初學者最常卡住的四個地方",
  details("起始值忘了填或填錯",
    '<p>填表是從已知的小答案長出來的。費氏的 <code>dp[0]</code>、<code>dp[1]</code>,爬樓梯的 <code>dp[0] = 1</code>,背包的第 0 列,少一個後面全部會錯。vector 要開 <code>n + 2</code> 格,避免 <code>n = 0</code> 或 <code>1</code> 時讀到範圍外。</p>'),
  details("dp 到底代表什麼,自己講不清楚",
    '<p>動手寫之前,先用一句話寫下 <code>dp[i]</code>(或 <code>dp[i][w]</code>)的意思,例如「只考慮前 i 個物品、容量 w 的最大價值」。意思不清楚,關係式一定寫不對。</p>'),
  details("填表順序反了",
    '<p>算某一格時,它依賴的格子必須<b>已經填好</b>。費氏由小到大填;背包一列一列填,因為每格只依賴上一列。順序錯了,讀到的是沒填的 0。</p>'),
  details("背包要用貪婪(挑最划算的)",
    '<p>0/1 背包用「價值除以重量最高的先拿」會得到錯的答案(例如容量不夠放整個物品,但差一點)。這種「拿了不能反悔、也不能拿一半」的問題要靠 DP 比較所有取捨。下一篇會看貪婪什麼時候可以用、什麼時候不行。</p>'))

SIM = {
  "a1": "<b>不是。</b>爬 1 階有 1 種,2 階有 2 種(1+1、2),3 階有 3 種,4 階是 <code>dp[3] + dp[2] = 3 + 2 = 5</code> 種。",
  "a2": "<b>正確!</b>最後一步不是爬 1 階就是爬 2 階:最後爬 1 階,前面有 dp[3] = 3 種;最後爬 2 階,前面有 dp[2] = 2 種。加起來 5 種。動畫跑爬樓梯 n=4 可以驗證。",
  "a3": "<b>不是。</b>8 是 n = 5 的答案(dp[5])。n = 4 是 5 種。",
}
QUIZ = quiz_cfg([
  ("動態規劃主要解決什麼問題?", ["同一個小問題被重複計算很多次", "資料沒有排序", "記憶體不夠用"], 0, "把算過的答案記下來,下次直接查表。"),
  ("填 dp[i] = dp[i-1] + dp[i-2] 之前,一定要先?", ["填好 dp[0]、dp[1] 這些已知的起始值", "把陣列排序", "清空 vector"], 0, "沒有起始值,後面的格子沒有東西可以用。"),
  ("fib(30) 遞迴約呼叫 269 萬次,用 memo 記下答案後約幾次?", ["59 次", "30 次", "一樣多"], 0, "每個 n 只真正計算一次,其餘直接查表(執行結果是 59 次)。"),
  ("0/1 背包的「0/1」是什麼意思?", ["每個物品要嘛拿一個、要嘛不拿", "物品重量只能是 0 或 1", "背包只有兩種大小"], 0, "不能拿一半,也不能拿兩個。"),
  ("n 個物品、容量 W 的 0/1 背包,DP 表大約有幾格?", ["n × W", "2ⁿ", "W²"], 0, "(n+1) × (W+1) 格,所以時間 O(n × W)。"),
])

ex = ('<h3 style="margin-top:30px">動手寫(兩題)</h3>'
  '<div class="panel"><h3>第 1 題:一次爬 1、2 或 3 階</h3><p>把爬樓梯改成一次可以爬 1、2 或 3 階。輸出應該是 <code>7 13 1</code>。</p>' + cpp("dp_ex1_starter") +
  details("參考答案", "<p>最後一步有三種可能,所以 <code>dp[i]</code> 是前三格相加。用內層迴圈走 1~3 步,並檢查 <code>i - step &gt;= 0</code>,就不會讀到負的位置,<code>n = 0</code> 也不用特判。</p>" + cpp("dp_ex1", "完整答案") + out("dp_ex1")) + '</div>'
  '<div class="panel" style="margin-top:14px"><h3>第 2 題:最少硬幣數</h3><p>用最少的硬幣湊出 amount,每種硬幣無限多枚,湊不出來回傳 -1。輸出應該是 <code>2 -1 3</code>。(<code>{1,3,4}</code> 湊 6 最少 2 枚,3 + 3。)</p>' + cpp("dp_ex2_starter") +
  details("參考答案", "<p><code>dp[a]</code> 是湊出金額 a 最少要幾枚。對每種硬幣 c:如果 <code>a &gt;= c</code> 而且 <code>dp[a - c]</code> 湊得出來,就試著用 <code>dp[a - c] + 1</code> 更新。<code>O(amount × 硬幣種類)</code>。下一篇會看到,這題用貪婪(先拿最大的)有時會錯。</p>" + cpp("dp_ex2", "完整答案") + out("dp_ex2")) + '</div>')

practice = section("practice", "動手演練:確認你真的懂了", ex, QUIZ_HTML,
  checks(["我能說出 DP 的兩個特徵:能拆成小問題、小問題會重複。",
          "我能分辨「由上而下記憶化」和「由下而上填表」。",
          "我能先用一句話定義 <code>dp</code> 的意思,再寫關係式。",
          "我知道起始值與填表順序為什麼重要。",
          "我知道 0/1 背包的「不拿 / 拿」兩種選擇,以及 O(n × W) 的由來。"], title="學完之後,對照這張清單"),
  resources([
    ("https://en.cppreference.com/cpp/algorithm/max", "std::max", "cppreference · std::max"),
    ("https://en.cppreference.com/cpp/container/vector", "std::vector", "cppreference · std::vector"),
  ], title="cppreference 參考頁面"))

SCRIPT = r'''
var P = Algo.dp;
function preset(kind, n) { return function (v, c) { c.set("kind", kind); c.set("n", n); c.run(); }; }
Algo.widget("w-dp", {
  form: [{ id: "kind", label: "問題", type: "select", value: "fib", options: Object.keys(P.NAMES).map(function (k) { return [k, P.NAMES[k]]; }) },
         { id: "n", label: "n(背包是容量,1~10)", type: "number", value: 8, min: 1, max: 15 }],
  buttons: [{ label: "費氏 n=8", run: preset("fib", 8) }, { label: "爬樓梯 n=8", run: preset("stairs", 8) }, { label: "背包 容量 7", run: preset("knap", 7) }],
  init: function () { return null; },
  idle: P.idle,
  make: function (v) { return P.run(v.kind, v.n); },
  render: function (f) { return f.rows.length ? '<div class="dpkeep">' + Algo.cellsHtml({ rows: f.rows, chips: f.chips }) + "</div>" : ""; },
  code: P.CODE_DP, code_cap: "三個 DP(亮起來的行 = 目前執行到的地方)"
});
Algo.dpDeps("w-deps", 7);
'''
SPEC = dict(
  file="datastruct-dp-guide.html", dir="datastruct", eyebrow_prefix=EYEBROW, foot=FOOT,
  modules=["cells", "alg_dp", "dpview"], script=SCRIPT,
  title="動態規劃入門:費氏、爬樓梯與 0/1 背包",
  eyebrow="第 16 篇 · 動態規劃(進階選讀)",
  h1="把算過的答案記下來:一格一格填表",
  sub="動態規劃就是「小問題的答案存進表、大問題直接查表」。這一篇用填表動畫看費氏數列、爬樓梯與 0/1 背包,並點格子看每一格依賴誰。",
  tldr="DP 適用於「能拆成小問題、且小問題會重複」。做法是定義 <code>dp</code> 的意思、寫出關係式、填起始值、照順序填表。fib(30) 遞迴約 270 萬次呼叫,DP 只要 30 步。0/1 背包的表有 (n+1) × (W+1) 格,時間 <code>O(n × W)</code>。<br><small>先備:第 3 篇 vector、第 7 篇遞迴與重複計算。預估 20 分鐘。難度:進階(選讀)。</small>",
  toc=[("what", "直覺:記住答案"), ("play", "填表動畫與依賴"), ("code", "完整程式"), ("cost", "複雜度小表"), ("gotchas", "常見錯誤"), ("practice", "動手寫與測驗")],
  body="\n\n".join([what, play, code, cost, gotchas, practice]),
  config=dict(sim=SIM, quiz=QUIZ),
  prev=("datastruct-dijkstra-guide.html", "最短路徑:Dijkstra"),
  next=("datastruct-greedy-guide.html", "貪婪、回溯與練習路線"),
)
