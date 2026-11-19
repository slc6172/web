from dh import *

what = section("what", "排序是把一堆東西整理成有順序",
  '<div class="panel"><h3>三種你本來就會的整理法</h3>'
  '<p><strong>氣泡排序</strong>:一排人由左往右,相鄰兩個比身高,左邊比較高就對調。走一趟,最高的會被一路換到最右邊。</p>'
  '<p><strong>選擇排序</strong>:從還沒排好的人裡找出最矮的,請他站到最前面;再從剩下的找最矮的,站到第二位……</p>'
  '<p style="margin-bottom:0"><strong>插入排序</strong>:像整理手上的撲克牌。左邊那幾張已經排好,每抽一張新的,就把它插進左邊正確的位置。</p></div>',
  '<h3 style="margin-top:26px">為什麼要排序?</h3>',
  '<p>排好序之後,第 6 篇的二分搜尋才能用,重複的資料會相鄰、找最大最小也變得簡單。所以排序是很多演算法的第一步。</p>',
  table("g2", ["名詞", "白話說明"], [
    ["比較", "看兩個元素誰大誰小,是排序最主要的操作。"],
    ["交換 / 搬動", "把元素換位置或往旁邊挪。"],
    ["已排序區", "動畫裡綠色的長條:已經確定在正確位置的元素。"],
  ]))

play = section("play", "動手玩:長條圖逐步排序",
  '<p class="sub" style="margin-bottom:14px">長條越高,數字越大。選一種排序法、設定資料,一步步看它怎麼把長條排成由矮到高。右上的兩個計數器會告訴你它花了多少力氣。</p>',
  try_list(["用「隨機」資料,三種排序各跑一次,看比較次數。", "按「已排序」,再跑氣泡排序和插入排序:發生什麼?", "按「反向」(由大到小),看哪一種最辛苦。", "試試自己輸入資料(2 到 10 個、1 到 99 的數字)。"]),
  widget("w-sort", "排序長條圖動畫"),
  sim("", "猜猜看:這一步會發生什麼?", "資料有 6 個、而且<b>已經排好了</b>(例如 1 2 3 4 5 6),用<b>插入排序</b>要比較幾次?",
      [("a1", "0 次"), ("a2", "5 次"), ("a3", "15 次")]))

exp = section("exp", "做實驗:資料變多會怎樣?",
  '<p class="sub" style="margin-bottom:14px">這裡不播動畫,直接讓三種排序在同一份資料上跑完,數出比較與交換次數。拉大 n,看看數字怎麼成長;換不同的資料排列,看哪一種變快或變慢。</p>',
  widget("w-exp", "排序次數實驗"),
  '<p style="margin-top:12px">你應該會發現:n 變成 2 倍,比較次數大約變成 <b>4 倍</b>,這就是 <code>O(n²)</code>。已排序的資料對氣泡與插入排序很友善(幾乎只要 n − 1 次),但對選擇排序沒有幫助。</p>')

code = section("code", "完整程式:三種排序",
  '<p class="sub" style="margin-bottom:14px">三個函式都「原地」排序:直接改傳進來的 <code>vector</code>,不需要額外的陣列。<code>std::swap(a, b)</code> 會交換兩個值。</p>',
  cpp("sort_basic"), out("sort_basic", "執行結果(三種排序結果相同)"), compile_cmd(),
  '<h3 style="margin-top:22px">實務上:直接用 std::sort</h3>',
  '<p>自己手寫是為了理解。實務上直接用 <code>std::sort</code>:又快、又正確,下一篇會講它為什麼快。第二個參數那個 <code>[](int a, int b) { return a &gt; b; }</code> 是 lambda(第 1 篇),用來告訴它「誰該排在前面」。</p>',
  cpp("sort_std"), out("sort_std"))

cost = section("cost", "複雜度小表",
  table("g4", ["排序法", "比較次數", "交換 / 搬動", "什麼時候特別快"], [
    ["氣泡排序", "最壞 O(n²);已排好 O(n)", "最壞 O(n²)", "資料已排好(有提早結束)"],
    ["選擇排序", "永遠 O(n²)", "最多 n − 1 次", "交換很昂貴時(交換次數最少)"],
    ["插入排序", "最壞 O(n²);已排好 O(n)", "最壞 O(n²)", "資料<b>幾乎排好</b>"],
  ]),
  '<p style="margin-top:14px"><b>空間:</b>三種都只多用幾個變數,是 O(1)。<b>但它們的最壞情況都是 O(n²)</b>:資料一多就撐不住(n = 100 萬時要一兆次)。所以下一篇要學更快的排序。</p>')

gotchas = section("gotchas", "初學者最常卡住的三個地方",
  details("內層迴圈的範圍寫錯,越界讀到 <code>v[n]</code>",
    '<p>比較 <code>v[j]</code> 和 <code>v[j + 1]</code> 時,j 最大只能到 <code>n - 2</code>,否則 <code>v[j + 1]</code> 就超出範圍(第 3 篇的越界)。氣泡排序的 <code>j &lt; n - 1 - i</code> 同時也把「已排好的右邊」排除在外。</p>'),
  details("條件寫 <code>&gt;=</code> 而不是 <code>&gt;</code>",
    '<p>兩個值相等時沒有必要交換。多交換不但浪費時間,還會讓「相等元素的原本順序」被打亂(排序的穩定性)。比較用 <code>&gt;</code>,相等不動。</p>'),
  details("給 <code>std::sort</code> 的比較規則寫成 <code>&lt;=</code>",
    '<p>比較函式要回答「a 是不是<b>嚴格</b>排在 b 前面」,<code>a &lt;= b</code> 對相等的元素也回 true,違反規則,在某些資料上可能導致當掉。想由大到小排,寫 <code>a &gt; b</code>,不是 <code>a &gt;= b</code>。</p>'))

SIM = {
  "a1": "<b>不是。</b>插入排序至少要看每個元素有沒有比左邊的大,第 2 到第 6 個各比 1 次,共 5 次。",
  "a2": "<b>正確!</b>已排好時,每個新拿起的 key 只和左邊最近的那個比 1 次,發現不比它大就停,共 n − 1 = 5 次,而且完全不用搬動。回動畫選「已排序」確認。",
  "a3": "<b>不是。</b>15 次(n(n−1)/2)是資料<b>完全反過來</b>時的最壞情況。",
}
QUIZ = quiz_cfg([
  ("氣泡排序跑完第一輪後,一定會發生什麼?", ["最大的元素到了最右邊", "最小的元素到了最左邊", "全部排好了"], 0, "一輪下來,最大的被一路交換到最右邊。"),
  ("資料已經排好時,選擇排序的比較次數是?", ["仍然是 n(n−1)/2 次", "只有 n − 1 次", "0 次"], 0, "選擇排序每一輪都要把剩下的全部看一遍找最小,不管資料長什麼樣。"),
  ("哪一種排序在資料「幾乎已排好」時特別快?", ["插入排序", "選擇排序", "三種一樣"], 0, "插入排序每個元素只需往左移一點點,接近 O(n)。"),
  ("三種基礎排序的最壞時間複雜度是?", ["O(n²)", "O(n log n)", "O(n)"], 0, "都是雙層迴圈的概念,資料大時會很慢。"),
  ("實務上要排序一個 vector,最好怎麼做?", ["用 <code>std::sort</code>", "自己手寫氣泡排序", "用選擇排序"], 0, "標準函式庫已經提供又快又正確的實作。"),
])

ex = ('<h3 style="margin-top:30px">動手寫(兩題)</h3>'
  '<div class="panel"><h3>第 1 題:補上交換的條件</h3><p>把 <code>if (false)</code> 改成正確的條件,輸出應該是 <code>1 2 3 4</code>。如果想改成<b>由大到小</b>排,條件要怎麼改?</p>' + cpp("sort_ex1_starter") +
  details("參考答案", "<p>左邊比右邊大就交換:<code>v[j] &gt; v[j + 1]</code>。由大到小只要把 <code>&gt;</code> 改成 <code>&lt;</code>。</p>" + cpp("sort_ex1", "完整答案") + out("sort_ex1")) + '</div>'
  '<div class="panel" style="margin-top:14px"><h3>第 2 題:完成插入排序的兩個空格</h3><p>完成 <code>while</code> 的條件,和最後把 key 放回去的那一行。輸出應該是 <code>1 2 3 4</code>。</p>' + cpp("sort_ex2_starter") +
  details("參考答案", "<p>條件:<code>j &gt;= 0 &amp;&amp; v[j] &gt; key</code>(順序不能反,要先確認沒越界)。迴圈結束時 j 指在「第一個不比 key 大」的位置,所以 key 放在 <code>v[j + 1]</code>。</p>" + cpp("sort_ex2", "完整答案") + out("sort_ex2")) + '</div>')

practice = section("practice", "動手演練:確認你真的懂了", ex, QUIZ_HTML,
  checks(["我能用一句話說出氣泡、選擇、插入排序各自怎麼做。",
          "我知道三種基礎排序最壞都是 O(n²)。",
          "我知道氣泡與插入排序在資料已排好時接近 O(n),選擇排序不會。",
          "我看得懂 <code>std::swap</code> 與三個函式的雙層迴圈。",
          "我知道比較用 <code>&gt;</code> 而不是 <code>&gt;=</code>,相等時不需要交換。",
          "我知道實務上用 <code>std::sort</code>,手寫只是為了理解。"], title="學完之後,對照這張清單"),
  resources([
    ("https://en.cppreference.com/cpp/algorithm/sort", "std::sort", "cppreference · std::sort"),
    ("https://en.cppreference.com/cpp/algorithm/swap", "std::swap", "cppreference · std::swap"),
  ], title="cppreference 參考頁面"))

SCRIPT = r'''
var S = Algo.sort;
function setData(kind) { return function (v, c) { c.set("d", S.make(kind, 8).join(", ")); }; }
Algo.widget("w-sort", {
  form: [{ id: "algo", label: "排序法", type: "select", value: "bubble", options: [["bubble", "氣泡排序"], ["selection", "選擇排序"], ["insertion", "插入排序"]] },
         { id: "d", label: "資料(2–10 個,1–99)", type: "text", value: "5, 2, 9, 1, 7, 3, 8, 4" }],
  buttons: [{ label: "隨機", run: setData("random") }, { label: "反向", run: setData("reverse") }, { label: "幾乎排好", run: setData("nearly") }, { label: "已排序", run: setData("sorted") }],
  init: function () { return null; },
  idle: function () { var v = [5, 2, 9, 1, 7, 3, 8, 4]; return { vals: v, cls: [], tags: [], chips: [["比較次數", 0], ["交換次數", 0]], msg: "選排序法、設定資料,按「執行」。長條越高,數字越大。" }; },
  make: function (v) { return S.run(v.algo, v.d); },
  render: Algo.barsHtml, code: S.CODE_SORT, code_cap: "三種排序(亮起來的行 = 目前執行到的地方)"
});
(function () {
  var root = document.getElementById("w-exp"); root.classList.add("cv");
  root.innerHTML = '<div class="cv-top"><label for="w-exp-n">資料量 n</label><input id="w-exp-n" type="range" min="5" max="300" value="50"><span class="cv-n" aria-live="polite"></span></div>' +
    '<div class="algo-form"><div class="algo-f"><label for="w-exp-k">資料排列</label><select id="w-exp-k"><option value="random">隨機</option><option value="sorted">已排序</option><option value="reverse">反向</option><option value="nearly">幾乎排好</option></select></div><button type="button" class="ghost" id="w-exp-go">重新抽樣</button></div>' +
    '<table class="cv-tbl"><thead><tr><th>排序法</th><th>比較次數</th><th>交換 / 搬動</th></tr></thead><tbody></tbody></table><p class="cv-note">n(n−1)/2 = <span id="w-exp-tri"></span>(完全反過來時,氣泡與插入排序的比較次數)。</p>';
  var r = root.querySelector("input"), nEl = root.querySelector(".cv-n"), tb = root.querySelector("tbody"), kind = document.getElementById("w-exp-k");
  function draw() {
    var n = +r.value, a = S.make(kind.value, n); nEl.textContent = "n = " + n; document.getElementById("w-exp-tri").textContent = (n * (n - 1) / 2).toLocaleString("en-US");
    tb.innerHTML = ["bubble", "selection", "insertion"].map(function (alg) { var s = S.stats(alg, a);
      return "<tr><td>" + S.NAMES[alg] + "</td><td>" + s.cmp.toLocaleString("en-US") + "</td><td>" + s.swp.toLocaleString("en-US") + "</td></tr>"; }).join("");
  }
  r.addEventListener("input", draw); kind.addEventListener("change", draw); document.getElementById("w-exp-go").addEventListener("click", draw); draw();
})();
'''
SPEC = dict(
  file="datastruct-sortbasic-guide.html", dir="datastruct", eyebrow_prefix=EYEBROW, foot=FOOT,
  modules=["cells", "bars", "alg_sort", "curves"], script=SCRIPT,
  title="基礎排序:氣泡、選擇與插入",
  eyebrow="第 8 篇 · 基礎排序",
  h1="三種直覺的排序法都是 O(n²),資料一多就撐不住",
  sub="氣泡排序、選擇排序、插入排序,是最容易想到的三種排序。這一篇用長條圖逐步看它們怎麼動,並用實驗數出比較與交換次數。",
  tldr="氣泡:相鄰比較浮到右邊。選擇:挑最小放前面。插入:像整理手牌。三種最壞都是 <code>O(n²)</code>;資料幾乎排好時,氣泡與插入接近 <code>O(n)</code>。實務上用 <code>std::sort</code>。<br><small>先備:第 3 篇 vector、第 2 篇 Big‑O。預估 15 分鐘。難度:基礎。</small>",
  toc=[("what", "直覺:三種整理法"), ("play", "長條圖逐步排序"), ("exp", "做實驗"), ("code", "完整程式"), ("cost", "複雜度小表"), ("gotchas", "常見錯誤"), ("practice", "動手寫與測驗")],
  body="\n\n".join([what, play, exp, code, cost, gotchas, practice]),
  config=dict(sim=SIM, quiz=QUIZ),
  prev=("datastruct-recursion-guide.html", "遞迴"),
  next=("datastruct-sortadv-guide.html", "進階排序:合併、快速與 std::sort"),
)
