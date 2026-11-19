from dh import *

what = section("what", "分治法:大問題切一半,各自解決再合起來",
  '<div class="panel"><h3>整理一大疊考卷</h3>'
  '<p><strong>合併排序</strong>:把考卷分成兩半,請兩個人各自排好,最後把兩疊「已排好的」合併。合併很容易:兩疊最上面各看一張,每次取分數較小的那張。</p>'
  '<p style="margin-bottom:0"><strong>快速排序</strong>:隨便抽一張當基準(pivot),把比它低分的放左邊、高分的放右邊,基準就定位了;再對左右兩堆各自重複。</p></div>',
  '<h3 style="margin-top:26px">為什麼會變快?</h3>',
  '<p>基礎排序要花 O(n²),因為每個元素都和很多別的元素比較。分治法每次把問題<b>切成一半</b>,切到底只要約 <b>log₂ n 層</b>;每一層全部元素加起來只做約 n 次工作。所以總共是 <b>n × log n</b>。n = 100 萬時:n² 是 1 兆次,n log n 只有約 2 千萬次。</p>',
  table("g2", ["名詞", "白話說明"], [
    ["分治法", "把問題切成更小的同類問題,各自解決,再把答案合起來。遞迴(第 7 篇)的典型應用。"],
    ["合併(merge)", "把兩個已排序的序列合成一個已排序的序列,只要從頭各看一個,取小的。"],
    ["基準(pivot)", "快速排序挑出來的那一個。分區之後,它的位置就確定了。"],
    ["穩定排序", "值相同的元素,排序後維持原本的先後順序。"],
  ]))

play = section("play", "動手玩:看「分」與「合」,看分區",
  '<p class="sub" style="margin-bottom:14px">選合併排序時,上面是要排的陣列 <code>v</code>,下面是合併時用的暫存區 <code>tmp</code>;選快速排序時,藍色是「已確認比 pivot 小」的區域。灰色淡掉的部分是目前沒在處理的範圍。</p>',
  try_list(["用合併排序,先看它怎麼一路「分」到只剩 1 個,再一層層「合」回來。", "改用快速排序,看 pivot(深色)怎麼被換到最後的位置。", "按「已排序」,分別用兩種排序跑一次:比較次數有什麼不同?"]),
  widget("w-adv", "進階排序動畫"),
  sim("", "猜猜看:這一步會發生什麼?", "快速排序用「最後一個」當 pivot,如果資料<b>已經排好了</b>,會發生什麼事?",
      [("a1", "最快:什麼都不用做"), ("a2", "最慢:每次分區都只切掉 1 個,變成 O(n²)"), ("a3", "和隨機資料一樣")]))

race = section("race", "做實驗:五種排序賽跑",
  '<p class="sub" style="margin-bottom:14px">不播動畫,直接數五種排序在同一份資料上的<b>比較次數</b>。把 n 拉大、換不同的資料排列,看誰輸誰贏。(綠色是最少的。)</p>',
  widget("w-race", "五種排序比較次數"),
  '<p style="margin-top:12px">試試「已排序」搭配快速排序:它從天才變成最慢的。這就是下面「常見錯誤」第一項。</p>')

code = section("code", "完整程式:合併排序與快速排序",
  '<p class="sub" style="margin-bottom:14px">兩個都是遞迴。<code>merge</code> 負責合併,<code>partition</code> 負責分區(回傳 pivot 最後的位置)。</p>',
  cpp("sortadv_ops"), out("sortadv_ops", "執行結果(合併、快速)"), compile_cmd(),
  '<h3 style="margin-top:22px">實測:n = 2000 時的比較次數</h3>',
  '<p>下面這份程式用固定的偽亂數資料,數出四種情況的比較次數(程式碼在你的電腦上也會得到一樣的數字):</p>',
  cpp("sortadv_count", "main.cpp(節錄:各排序前面加了 ++cmp)", copy=False), out("sortadv_count", "執行結果"),
  '<div class="see"><b class="l">你會看到</b>隨機資料時,氣泡排序比了約 200 萬次,合併與快速只要約 2 萬次,差了 100 倍。但快速排序遇到「已排序」的資料,也掉到 200 萬次。</div>')

stl = section("stl", "實務上:std::sort 與 std::stable_sort",
  '<p class="sub" style="margin-bottom:14px"><code>std::sort</code> 是快速排序、堆積排序與插入排序的混合體(introsort):平常像快速排序一樣快,遇到會退化的情況就自動換方法,所以<b>最壞也保證 O(n log n)</b>。需要「相同的值維持原本順序」(穩定)時,用 <code>std::stable_sort</code>(以合併排序為基礎)。</p>',
  cpp("sortadv_std"), out("sortadv_std", "執行結果(分數相同者維持原本的 A、C 與 B、D 順序)"))

cost = section("cost", "複雜度小表",
  table("g4", ["排序法", "時間", "額外空間", "穩定?"], [
    ["合併排序", "永遠 O(n log n)", "O(n)(tmp 暫存區)", "是"],
    ["快速排序", "平均 O(n log n);最壞 O(n²)", "O(log n)(遞迴堆疊)", "否"],
    ["<code>std::sort</code>", "最壞 O(n log n)", "O(log n)", "否"],
    ["<code>std::stable_sort</code>", "O(n log n)", "最多 O(n)", "是"],
  ]))

gotchas = section("gotchas", "初學者最常卡住的三個地方",
  details("快速排序遇到已排序的資料變成 O(n²)",
    '<p>如果每次都用最後一個當 pivot,而資料已經排好,pivot 永遠是最大的,每次分區只切掉 1 個,遞迴深度變成 n。上面實測就是 200 萬次。解法是<b>隨機挑 pivot</b>,或取頭、中、尾三個的中位數。<code>std::sort</code> 已經處理好了。</p>'),
  details("合併排序需要額外的 <code>tmp</code> 空間",
    '<p>合併時不能直接在原陣列裡覆蓋(會蓋掉還沒比較的元素),所以要借一塊同樣大小的暫存區。這是合併排序穩定、永遠 n log n 的代價:空間 O(n)。</p>'),
  details("邊界差一:<code>lo &gt;= hi</code>、<code>mid + 1</code>、<code>p - 1</code>",
    '<p>遞迴的範圍是「閉區間」[lo, hi]。左半是 <code>[lo, mid]</code>,右半是 <code>[mid + 1, hi]</code>;快速排序在 pivot 位置 p 切開後,左邊是 <code>[lo, p - 1]</code>、右邊是 <code>[p + 1, hi]</code>(p 本身已定位)。少了 ±1 會無限遞迴或漏排。</p>'))

SIM = {
  "a1": "<b>不是。</b>資料已排好反而是快速排序的壞情況。用「已排序」按鈕與快速排序跑一次,看每次分區只切掉 1 個。",
  "a2": "<b>正確!</b>pivot 是最大的,所有元素都「比它小」,分區後右邊是空的,問題只少了 1 個,遞迴深度變成 n,總共約 n²/2 次比較。實測 n = 2000 就是 1,999,000 次。",
  "a3": "<b>不是。</b>隨機資料時 pivot 通常落在中間附近,差很多;已排序時反而是最壞情況。",
}
QUIZ = quiz_cfg([
  ("合併排序的時間複雜度是?", ["永遠 O(n log n)", "平均 O(n log n),最壞 O(n²)", "O(n²)"], 0, "每次都切一半、合併是 O(n),和資料內容無關。"),
  ("快速排序的最壞情況是什麼時候?", ["每次 pivot 都剛好是最大或最小,變成 O(n²)", "資料量是奇數", "資料有重複"], 0, "pivot 選得很偏,每次只切掉 1 個。"),
  ("合併排序的 <code>merge</code> 為什麼只要 O(n)?", ["兩半都已排序,各用一個指標從頭比,每個元素只處理一次", "因為用了 std::sort", "因為用了雜湊表"], 0, "兩個指標只會往前,不會回頭。"),
  ("想讓分數相同的人維持原本順序,應該用?", ["<code>std::stable_sort</code>", "<code>std::sort</code>", "兩個一樣"], 0, "stable_sort 保證穩定;sort 不保證。"),
  ("實務上要排序一個 vector,最好?", ["用 <code>std::sort</code>", "自己寫合併排序", "自己寫氣泡排序"], 0, "又快又正確,而且最壞也保證 O(n log n)。"),
])

ex = ('<h3 style="margin-top:30px">動手寫(兩題)</h3>'
  '<div class="panel"><h3>第 1 題:合併兩個已排序的 vector</h3><p>完成 <code>mergeTwo</code>:這就是合併排序裡 <code>merge</code> 的核心。輸出應該是 <code>1 2 3 4 7 9 10</code>。</p>' + cpp("sortadv_ex1_starter") +
  details("參考答案", "<p>兩個指標 i、j 各指著 a 和 b 的最前面,每次取較小的;一邊用完後,另一邊剩下的直接接上去。時間 O(n),n 是兩個加起來的長度。</p>" + cpp("sortadv_ex1", "完整答案") + out("sortadv_ex1")) + '</div>'
  '<div class="panel" style="margin-top:14px"><h3>第 2 題:用 lambda 做「多重條件」排序</h3><p>完成 lambda:分數高的在前;分數相同時,名字小的在前。輸出應該是 <code>Ann Dan Bob Cara</code>。</p>' + cpp("sortadv_ex2_starter") +
  details("參考答案", "<p>先比分數;分數不同就用分數決定順序,分數相同再用名字決定。lambda 回傳「a 是否該排在 b 前面」。</p>" + cpp("sortadv_ex2", "完整答案") + out("sortadv_ex2")) + '</div>')

practice = section("practice", "動手演練:確認你真的懂了", ex, QUIZ_HTML,
  checks(["我能說出分治法的概念:切、各自解決、合起來。",
          "我知道合併排序永遠 O(n log n),但要 O(n) 的額外空間。",
          "我知道快速排序平均 O(n log n),最壞 O(n²),以及什麼時候最壞。",
          "我看得懂 <code>merge</code> 與 <code>partition</code> 在做什麼。",
          "我知道「穩定」是什麼意思,以及何時用 <code>std::stable_sort</code>。",
          "我知道實務上直接用 <code>std::sort</code>。"], title="學完之後,對照這張清單"),
  resources([
    ("https://en.cppreference.com/cpp/algorithm/sort", "std::sort", "cppreference · std::sort"),
    ("https://en.cppreference.com/cpp/algorithm/stable_sort", "std::stable_sort", "cppreference · std::stable_sort"),
  ], title="cppreference 參考頁面"))

SCRIPT = r'''
var S = Algo.sort, V = Algo.sortadv;
function setData(kind) { return function (v, c) { c.set("d", S.make(kind, 8).join(", ")); }; }
Algo.widget("w-adv", {
  form: [{ id: "algo", label: "排序法", type: "select", value: "merge", options: [["merge", "合併排序"], ["quick", "快速排序"]] },
         { id: "d", label: "資料(2–10 個,1–99)", type: "text", value: "38, 27, 43, 3, 9, 82, 10, 15" }],
  buttons: [{ label: "隨機", run: setData("random") }, { label: "反向", run: setData("reverse") }, { label: "已排序", run: setData("sorted") }],
  init: function () { return null; },
  idle: function () { return { vals: [38, 27, 43, 3, 9, 82, 10, 15], cls: [], tags: [], chips: [["比較次數", 0]], msg: "選排序法、設定資料,按「執行」。" }; },
  make: function (v) { return V.run(v.algo, v.d); },
  render: Algo.barsHtml, code: V.CODE_ADV, code_cap: "merge / mergeSort / partition / quickSort(亮起來的行 = 目前執行到的地方)"
});
(function () {
  var root = document.getElementById("w-race"); root.classList.add("cv");
  root.innerHTML = '<div class="cv-top"><label for="w-race-n">資料量 n</label><input id="w-race-n" type="range" min="10" max="2000" step="10" value="500"><span class="cv-n" aria-live="polite"></span></div>' +
    '<div class="algo-form"><div class="algo-f"><label for="w-race-k">資料排列</label><select id="w-race-k"><option value="random">隨機</option><option value="sorted">已排序</option><option value="reverse">反向</option><option value="nearly">幾乎排好</option></select></div><button type="button" class="ghost" id="w-race-go">重新抽樣</button></div>' +
    '<table class="cv-tbl"><thead><tr><th>排序法</th><th>比較次數</th></tr></thead><tbody></tbody></table>';
  var r = root.querySelector("input"), nEl = root.querySelector(".cv-n"), tb = root.querySelector("tbody"), kind = document.getElementById("w-race-k");
  function draw() {
    var n = +r.value, a = S.make(kind.value, n); nEl.textContent = "n = " + n.toLocaleString("en-US");
    var rows = [["氣泡排序", S.stats("bubble", a).cmp], ["選擇排序", S.stats("selection", a).cmp], ["插入排序", S.stats("insertion", a).cmp], ["合併排序", V.stats("merge", a).cmp], ["快速排序(最後一個當 pivot)", V.stats("quick", a).cmp]];
    var mn = Math.min.apply(null, rows.map(function (x) { return x[1]; }));
    tb.innerHTML = rows.map(function (x) { return "<tr><td>" + x[0] + '</td><td style="' + (x[1] === mn ? "color:var(--olive);font-weight:700" : "") + '">' + x[1].toLocaleString("en-US") + "</td></tr>"; }).join("");
  }
  r.addEventListener("input", draw); kind.addEventListener("change", draw); document.getElementById("w-race-go").addEventListener("click", draw); draw();
})();
'''
SPEC = dict(
  file="datastruct-sortadv-guide.html", dir="datastruct", eyebrow_prefix=EYEBROW, foot=FOOT,
  modules=["cells", "bars", "alg_sort", "alg_sortadv", "curves"], script=SCRIPT,
  title="進階排序:合併排序、快速排序與 std::sort",
  eyebrow="第 9 篇 · 進階排序",
  h1="切一半再處理,排序從 O(n²) 降到 O(n log n)",
  sub="合併排序「分了再合」,快速排序「分區再遞迴」。這一篇用動畫看分治法怎麼運作,用實驗看差距有多大,並認識實務上的 std::sort。",
  tldr="<b>合併排序</b>:切一半、各自排好、合併,永遠 <code>O(n log n)</code>,要 <code>O(n)</code> 額外空間。<b>快速排序</b>:挑 pivot 分區再遞迴,平均 <code>O(n log n)</code>,pivot 選很偏時最壞 <code>O(n²)</code>。實務上用 <code>std::sort</code>。<br><small>先備:第 7 篇遞迴、第 8 篇基礎排序。預估 18 分鐘。難度:進階。</small>",
  toc=[("what", "分治法的直覺"), ("play", "分與合"), ("race", "五種排序賽跑"), ("code", "完整程式"), ("stl", "std::sort"), ("cost", "複雜度小表"), ("gotchas", "常見錯誤"), ("practice", "動手寫與測驗")],
  body="\n\n".join([what, play, race, code, stl, cost, gotchas, practice]),
  config=dict(sim=SIM, quiz=QUIZ),
  prev=("datastruct-sortbasic-guide.html", "基礎排序:氣泡、選擇、插入"),
  next=("datastruct-hash-guide.html", "雜湊表"),
)
