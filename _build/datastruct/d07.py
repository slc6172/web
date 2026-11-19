from dh import *

what = section("what", "遞迴:把大問題變成「同樣形狀的小問題」",
  '<div class="panel"><h3>想像一組俄羅斯娃娃</h3>'
  '<p>要數有幾個娃娃:打開最外面一個,剩下的是「一組比較小的娃娃」,而數它的方法跟原本一樣。一直打開,直到打開後裡面是空的,就知道數完了。</p>'
  '<p style="margin-bottom:0">寫成程式就是:<strong>函式在裡面呼叫自己</strong>,每次處理的問題都比上一次小,小到不能再小時停下來。</p></div>',
  '<h3 style="margin-top:26px">寫遞迴只要記住三件事</h3>',
  table("g2", ["要素", "說明"], [
    ["基底條件", "問題小到可以直接回答的時候(例如 <code>n == 0</code>)。<b>沒有它就會無限呼叫下去。</b>"],
    ["縮小問題", "每次呼叫自己時,參數要更靠近基底條件(例如 <code>n - 1</code>)。"],
    ["相信子呼叫", "寫的時候假設 <code>f(n - 1)</code> 已經算對了,你只負責「用它的答案算出 <code>f(n)</code>」。"],
  ]),
  '<p style="margin-top:18px">先看最簡單的例子,倒數計時:</p>',
  cpp("rec_countdown"), out("rec_countdown"),
  '<div class="see"><b class="l">你會看到</b><code>countdown(3)</code> 印 3,呼叫 <code>countdown(2)</code>,印 2,呼叫 <code>countdown(1)</code>,印 1,呼叫 <code>countdown(0)</code>,碰到基底條件印出 liftoff 後一路返回。</div>')

play = section("play", "動手玩:看呼叫堆疊與呼叫樹",
  '<p class="sub" style="margin-bottom:14px">每呼叫一次函式,上方的<b>呼叫堆疊</b>就多一層(和第 5 篇的 stack 一樣,後進先出);下方的<b>呼叫樹</b>記錄誰呼叫了誰。節點旁邊的「=數字」是它回傳的結果。</p>',
  try_list(["選 <code>fact</code>、n = 4:看呼叫一路往下到基底條件,再一路往回乘出答案。", "選 <code>fib</code>、n = 4,再改成 n = 6:樹長成什麼樣?", "注意虛線框的節點:它們是「已經算過的 fib(k) 又被重新算一遍」。"]),
  widget("w-rec", "遞迴呼叫動畫"),
  sim("", "猜猜看:這一步會發生什麼?", "<code>fact(4)</code> 一共會呼叫 <code>fact</code> 這個函式幾次(包含最外層那次)?",
      [("a1", "3 次"), ("a2", "4 次"), ("a3", "24 次")]))

code = section("code", "完整程式:階乘與費氏數列",
  '<p class="sub" style="margin-bottom:14px"><code>fact(n)</code> = n × (n − 1) × … × 1;<code>fib(n)</code> 每一項是前兩項的和(0, 1, 1, 2, 3, 5, 8…)。兩個函式都符合「三要素」。</p>',
  cpp("rec_basic"), out("rec_basic", "執行結果(fact(5)、fib(6))"),
  '<p>記得這個順序:<code>fact(5)</code> 先往下呼叫到 <code>fact(1)</code>(基底條件),<b>回傳時才開始乘</b>。每一層都在等下一層的答案,所以呼叫堆疊上同時有很多層。</p>')

why = section("why", "為什麼 fib 會慢?重複計算",
  '<p class="sub" style="margin-bottom:14px">回頭看 <code>fib(6)</code> 的呼叫樹:<code>fib(3)</code> 出現了好幾次,每次都從頭算。n 一大,重複的次數爆炸成長。下面是用真正的程式數出來的呼叫次數:</p>',
  cpp("rec_fibcount"), out("rec_fibcount", "執行結果(呼叫次數)"),
  '<div class="warn"><b class="l">n 每加 10,次數約變成 120 倍</b>這是<b>指數成長</b>(大約 O(1.6ⁿ),常簡化說成 O(2ⁿ))。n = 50 時,你的電腦可能算好幾個小時。第 16 篇「動態規劃」會教你把算過的結果記下來,讓 <code>fib</code> 變成 O(n)。</div>')

bs = section("bs", "遞迴的第二個例子:二分搜尋",
  '<p class="sub" style="margin-bottom:14px">上一篇的二分搜尋也能寫成遞迴:每次只留下一半,「在剩下一半裡搜尋」就是一個一模一樣、但更小的問題。這裡有<b>兩個基底條件</b>:範圍空了(沒找到)、找到了。</p>',
  cpp("rec_binsearch"), out("rec_binsearch"))

cost = section("cost", "複雜度小表:時間與呼叫堆疊",
  '<p class="sub" style="margin-bottom:14px">遞迴的「空間」要把<b>呼叫堆疊的深度</b>算進去:每一層都佔一點記憶體。</p>',
  table("g3", ["函式", "時間", "空間(堆疊深度)"], [
    ["<code>fact(n)</code>", "O(n)", "O(n):最深有 n 層"],
    ["<code>fib(n)</code>(上面的寫法)", "指數,約 O(2ⁿ)", "O(n):最深是從 n 一路減到 1"],
    ["遞迴二分搜尋", "O(log n)", "O(log n):每層砍一半"],
  ]))

gotchas = section("gotchas", "初學者最常卡住的三個地方",
  details("忘了寫基底條件:無限遞迴",
    '<p>少了基底條件,函式永遠不會停,一直呼叫下去,直到呼叫堆疊用光、程式當掉。連編譯器都看得出來,會警告你:</p>' + cpp("rec_infinite", "錯誤示範(不要執行)", copy=False) + out("rec_infinite", "g++ -Wall 的警告(實際輸出)")),
  details("遞迴太深:呼叫堆疊爆掉(stack overflow)",
    '<p>每一層呼叫都要佔一小塊記憶體。一般電腦大約幾萬到幾十萬層就會用完,所以 <code>sumTo(1000000)</code> 這種寫法很可能直接當掉。層數可能很深的時候,改用迴圈。</p>'),
  details("遞迴一定比迴圈好嗎?",
    '<p>不一定。像 <code>fact</code> 用迴圈寫更省空間。遞迴的優勢是:遇到「問題裡面有同樣形狀的小問題」時(樹的走訪、排列組合、分治法),寫起來特別自然。後面的二元樹、合併排序、回溯都會用到。</p>'))

SIM = {
  "a1": "<b>不是。</b>要數到 <code>fact(1)</code> 才是基底條件:fact(4)、fact(3)、fact(2)、fact(1) 共 4 次。回到動畫選 fact、n = 4 數一數。",
  "a2": "<b>正確!</b>fact(4) 呼叫 fact(3),fact(3) 呼叫 fact(2),fact(2) 呼叫 fact(1),共 4 次。一般來說 fact(n) 會呼叫 n 次,所以時間是 O(n)。",
  "a3": "<b>不是。</b>24 是 fact(4) 的<b>答案</b>(4×3×2×1),不是呼叫次數。",
}
QUIZ = quiz_cfg([
  ("遞迴函式一定要有什麼,才不會無限呼叫下去?", ["基底條件", "迴圈", "全域變數"], 0, "基底條件是「不再呼叫自己」的出口。"),
  ("<code>fact(4)</code> 一共會呼叫 <code>fact</code> 幾次?", ["3 次", "4 次", "24 次"], 1, "fact(4)、fact(3)、fact(2)、fact(1) 共 4 次。"),
  ("遞迴太深可能導致什麼?", ["呼叫堆疊用光,程式當掉", "硬碟變滿", "網路斷線"], 0, "每層呼叫都佔呼叫堆疊的空間。"),
  ("未加優化的 <code>fib(30)</code> 為什麼很慢?", ["同樣的子問題被重複計算很多次", "因為 fib 的公式很複雜", "因為 int 太小"], 0, "例如 fib(3) 在樹裡出現很多次,每次都從頭算。"),
  ("下面哪一項<b>不是</b>遞迴三要素?", ["一定要用 vector 存資料", "基底條件", "每次呼叫讓問題變小"], 0, "遞迴和用什麼容器無關。"),
])

ex = ('<h3 style="margin-top:30px">動手寫(兩題)</h3>'
  '<div class="panel"><h3>第 1 題:補上基底條件</h3><p><code>sumTo(n)</code> 要回傳 1 + 2 + … + n。目前缺基底條件,執行會當掉。補上它,輸出應該是 <code>15 0</code>。</p>' + cpp("rec_ex1_starter") +
  details("參考答案", "<p>n 等於 0 的時候總和是 0,直接回傳。其他情況用 <code>n + sumTo(n - 1)</code>。</p>" + cpp("rec_ex1", "完整答案") + out("rec_ex1")) + '</div>'
  '<div class="panel" style="margin-top:14px"><h3>第 2 題:用遞迴寫 power</h3><p>完成 <code>power(base, exp)</code>。輸出應該是 <code>8 1</code>。想想三要素:基底條件是什麼?怎麼縮小問題?</p>' + cpp("rec_ex2_starter") +
  details("參考答案", "<p>基底條件:<code>exp == 0</code> 時回傳 1。縮小問題:<code>base × power(base, exp - 1)</code>。時間是 O(exp)。</p>" + cpp("rec_ex2", "完整答案") + out("rec_ex2")) + '</div>')

practice = section("practice", "動手演練:確認你真的懂了", ex, QUIZ_HTML,
  checks(["我能說出遞迴三要素:基底條件、縮小問題、相信子呼叫。",
          "我看得懂 fact 與 fib 的呼叫堆疊和呼叫樹。",
          "我知道忘記基底條件會無限遞迴,編譯器甚至會警告。",
          "我知道遞迴太深會讓呼叫堆疊爆掉。",
          "我知道 fib 慢的原因是重複計算,之後會用動態規劃解決。",
          "我能把「二分搜尋」寫成遞迴,並找出它的兩個基底條件。"], title="學完之後,對照這張清單"))

SCRIPT = r'''
var R = Algo.rec;
function render(f) { return Algo.stackHtml(f) + Algo.treeHtml(f); }
Algo.widget("w-rec", {
  form: [{ id: "fn", label: "函式", type: "select", value: "fact", options: [["fact", "fact(n) 階乘"], ["fib", "fib(n) 費氏數列"]] },
         { id: "n", label: "n", type: "number", min: 1, max: 8, value: 4 }],
  buttons: [
    { label: "fact(4)", run: function (v, c) { c.set("fn", "fact"); c.set("n", 4); c.run(); } },
    { label: "fib(4)", run: function (v, c) { c.set("fn", "fib"); c.set("n", 4); c.run(); } },
    { label: "fib(6)", run: function (v, c) { c.set("fn", "fib"); c.set("n", 6); c.run(); } }
  ],
  init: function () { return null; },
  idle: function () { return { tree: null, stack: [], chips: [], msg: "選函式與 n,按「執行」。fact 的 n 最大 8,fib 的 n 最大 6(再大樹就太寬了)。" }; },
  make: function (v) { return R.run(v.fn, v.n); },
  render: render, code: R.CODE_REC, code_cap: "fact 與 fib(亮起來的行 = 目前執行到的地方)"
});
'''
SPEC = dict(
  file="datastruct-recursion-guide.html", dir="datastruct", eyebrow_prefix=EYEBROW, foot=FOOT,
  modules=["cells", "tree", "alg_rec"], script=SCRIPT,
  title="遞迴:函式呼叫自己,直到碰到基底條件",
  eyebrow="第 7 篇 · 遞迴",
  h1="遞迴就是把問題縮小,直到小到能直接回答",
  sub="函式在裡面呼叫自己。這一篇用呼叫堆疊與呼叫樹的動畫,看階乘與費氏數列怎麼一層層展開、再一層層回來,也看為什麼天真的 fib 會慢。",
  tldr="遞迴三要素:<b>基底條件</b>(何時停)、<b>縮小問題</b>、<b>相信子呼叫</b>。每次呼叫佔呼叫堆疊一層,太深會爆;天真的 <code>fib</code> 因為重複計算是指數時間。<br><small>先備:第 5 篇堆疊的概念。預估 15 分鐘。難度:基礎。</small>",
  toc=[("what", "直覺與三要素"), ("play", "呼叫堆疊與呼叫樹"), ("code", "完整程式"), ("why", "fib 為什麼慢"), ("bs", "遞迴二分搜尋"), ("cost", "複雜度小表"), ("gotchas", "常見錯誤"), ("practice", "動手寫與測驗")],
  body="\n\n".join([what, play, code, why, bs, cost, gotchas, practice]),
  config=dict(sim=SIM, quiz=QUIZ),
  prev=("datastruct-search-guide.html", "搜尋:線性與二分"),
  next=("datastruct-sortbasic-guide.html", "基礎排序:氣泡、選擇、插入"),
)
