from dh import *

what = section("what", "不用計時,改成「數步驟」",
  '<div class="panel"><h3>為什麼不直接量幾秒?</h3>'
  '<p>同一段程式,換一台電腦、換一個編譯選項,秒數就不一樣。我們想知道的是更根本的問題:<strong>資料變多的時候,程式會慢多少?</strong></p>'
  '<p style="margin-bottom:0">所以改成「數操作次數」:資料量 n 變成 2 倍、10 倍時,操作次數怎麼成長?這個成長的樣子,用 <b>Big‑O</b> 記號來描述。</p></div>',
  '<h3 style="margin-top:26px">五個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["n(輸入規模)", "資料的量,例如 vector 的元素個數。"],
    ["操作次數", "程式主要的步驟做了幾次,例如比較、搬動、加法。"],
    ["時間複雜度", "操作次數如何隨 n 成長。"],
    ["空間複雜度", "額外用的記憶體如何隨 n 成長。"],
    ["Big‑O,<code>O(…)</code>", "描述成長趨勢的記號。<code>O(n)</code> 唸作「order n」,意思是「大致和 n 成正比」。"],
  ]))

count = section("count", "動手玩:數一數操作次數",
  '<p class="sub" style="margin-bottom:14px">選一種迴圈、調整 n,一步一步看操作次數怎麼累積。程式碼裡寫 <code>n = 8</code>;改 n 時,把它想成改那一行。</p>',
  try_list(["選「單層迴圈」,n = 5:次數和 n 的關係?", "選「雙層迴圈」,n = 4,再改成 n = 8:次數變成幾倍?", "選「每次砍一半」,n = 16 再改成 n = 32:多了幾次?"]),
  widget("w-count", "操作次數動畫"),
  cpp("bigo_count"), out("bigo_count", "執行結果(n = 8:單層、雙層、砍一半)"),
  '<div class="see"><b class="l">你會看到</b>n = 8 時是 8、64、3。單層是 n,雙層是 n × n,每次砍一半只要 log₂ n 次(8 → 4 → 2 → 1,共 3 次)。</div>')

curves = section("curves", "拖拉 n,看六種成長的差距",
  '<p class="sub" style="margin-bottom:14px">這是最常見的六種成長。把 n 從小拉到大,看哪幾條線衝上天、哪幾條幾乎貼地。</p>',
  sim("", "猜猜看:這一步會發生什麼?", "資料量 n 從 100 變成 200,<b>O(n)</b> 和 <b>O(n²)</b> 的操作次數分別變成幾倍?",
      [("a1", "都變成 2 倍"), ("a2", "O(n) 變 2 倍,O(n²) 變 4 倍"), ("a3", "O(n) 變 2 倍,O(n²) 變 8 倍")]),
  widget("w-curves", "成長曲線比較"),
  '<h3 style="margin-top:26px">六個常見等級,之後都會遇到</h3>',
  table("g3", ["等級", "名稱", "你會在哪裡遇到"], [
    ["<code>O(1)</code>", "常數", "用索引讀 <code>v[i]</code>(第 3 篇)、<code>push_back</code> 多數時候。"],
    ["<code>O(log n)</code>", "對數", "二分搜尋(第 6 篇)、平衡的樹(第 11–13 篇)。"],
    ["<code>O(n)</code>", "線性", "從頭到尾掃一遍:線性搜尋、加總、在 vector 中間插入。"],
    ["<code>O(n log n)</code>", "線性對數", "好的排序法:合併排序、快速排序(第 9 篇)。"],
    ["<code>O(n²)</code>", "平方", "雙層迴圈:氣泡、選擇、插入排序(第 8 篇)。"],
    ["<code>O(2ⁿ)</code>", "指數", "把所有子集、所有組合都試一遍(遞迴、回溯,第 7、17 篇)。n 稍大就算不完。"],
  ]))

rules = section("rules", "三條化簡規則",
  '<p class="sub" style="margin-bottom:14px">數出來的次數常常是 <code>3n² + 5n + 2</code> 這種樣子。Big‑O 只關心「n 很大時,誰最大」,所以這樣化簡:</p>',
  table("g3", ["規則", "例子", "原因"], [
    ["只留成長最快的那一項", "<code>n² + n</code> → <code>O(n²)</code>", "n = 1000 時,n² 是 100 萬,n 只有 1000,可以忽略。"],
    ["去掉前面的係數", "<code>3n</code> → <code>O(n)</code>", "係數取決於電腦與寫法;我們看的是成長的形狀。"],
    ["不同的輸入用不同的字母", "掃 a 個再掃 b 個 → <code>O(a + b)</code>", "兩個 vector 的大小互不相干,不要都寫成 n。"],
  ]),
  '<div class="tip"><b class="l">一個接一個,還是一個套一個?</b>兩個迴圈<b>一個接一個</b>(各 n 次)是 n + n = 2n,仍是 <code>O(n)</code>;<b>一個套在另一個裡面</b>是 n × n,變成 <code>O(n²)</code>。看迴圈怎麼擺,比看有幾個更重要。</div>',
  '<h3 style="margin-top:22px">空間複雜度</h3>',
  '<p>同樣的算法,看「額外」用了多少記憶體。只多用幾個變數是 <code>O(1)</code>;另外複製一份長度 n 的 vector 是 <code>O(n)</code>。後面學到遞迴、雜湊表時,空間也會成為取捨的一部分。</p>')

gotchas = section("gotchas", "初學者最常卡住的三個地方",
  details("O(n) 一定比 O(n²) 快嗎?",
    '<p>n 很大時是的,n 很小時不一定。Big‑O 省略了係數,所以 n = 5 時,一個寫得很囉嗦的 O(n) 可能輸給寫得簡潔的 O(n²)。它回答的是「資料變大時,誰撐得住」。</p>'),
  details("兩段程式都是 O(n),速度就一樣嗎?",
    '<p>不一定。Big‑O 只描述成長的形狀,不管每一步多貴。都是 O(n) 的兩段程式,一個每圈做 1 次加法、一個每圈做 100 次運算,實際速度差很多。想比較真實速度,要實際量測。</p>'),
  details("<code>O(n + n)</code> 為什麼會寫成 <code>O(n)</code>?",
    '<p>去掉係數的規則:2n 和 n 成長的形狀一樣,都是「資料多一倍,時間多一倍」。所以寫成 <code>O(n)</code>。</p>'))

SIM = {
  "a1": "<b>不是。</b>只有 O(n) 是 2 倍。O(n²) 是 n 乘以 n,兩邊都變 2 倍,乘起來是 4 倍。",
  "a2": "<b>正確!</b>O(n) 跟著 n 變 2 倍;O(n²) = n × n,所以 (2n)² = 4n²,變 4 倍。拉動下面的滑桿,看 n = 100 與 n = 200 的數字。",
  "a3": "<b>不是。</b>變成 8 倍是 n³ 才會發生。n² 在 n 變 2 倍時是 2 × 2 = 4 倍。",
}
QUIZ = quiz_cfg([
  ("資料量 n 變成 2 倍時,<code>O(n²)</code> 的操作次數大約變成幾倍?", ["2 倍", "4 倍", "不變"], 1,
   "(2n)² = 4n²,所以是 4 倍。n 變 10 倍,次數會變 100 倍。"),
  ("下面哪一種寫法是 <code>O(n²)</code>?", ["一個 for 迴圈跑 n 次,裡面做固定幾步", "一個 for 迴圈跑 n 次,裡面又有一個 for 迴圈跑 n 次", "兩個 for 迴圈一個接一個,各跑 n 次"], 1,
   "套在裡面的迴圈,每一圈外層都要完整跑一次,所以是 n × n。一個接一個只是 n + n。"),
  ("<code>3n + 5</code> 化簡成 Big‑O 是?", ["O(n)", "O(3n)", "O(n + 5)"], 0,
   "去掉係數 3 和常數 5,只留成長形狀:O(n)。"),
  ("二分搜尋每次砍掉一半,時間是?", ["O(n)", "O(log n)", "O(1)"], 1,
   "n 一直除以 2,到剩 1 只需要約 log₂ n 次。"),
  ("n = 1,000,000 時,下面哪個操作次數最多?", ["O(n log n)", "O(n²)", "O(n)"], 1,
   "n² 是一兆次,n log n 約 2 千萬次,n 只有一百萬次。"),
])

ex = ('<h3 style="margin-top:30px">動手寫(兩題)</h3>'
  '<p class="sub" style="margin-bottom:12px">這一篇的動手題偏「判斷」。</p>'
  '<div class="panel"><h3>第 1 題:判斷時間複雜度</h3><p>下面的 <code>countEven</code> 時間是 O(?)?想好再看答案。</p>' + cpp("bigo_ex1_starter") +
  details("參考答案", "<p><b>O(n)</b>:迴圈每個元素看一次,每次做固定的幾步(取餘數、比較、可能加 1),總共 n 圈。</p>" + out("bigo_ex1", "執行結果")) + '</div>'
  '<div class="panel" style="margin-top:14px"><h3>第 2 題:寫出函式,再判斷複雜度</h3><p>完成 <code>hasPairSum</code>(最直覺的寫法就好),輸出要是 <code>1 0</code>。然後想想:它是 O(?)?</p>' + cpp("bigo_ex2_starter") +
  details("參考答案", "<p>檢查所有兩兩配對:外層 i 跑 n 圈,內層 j 從 i + 1 跑到尾,大約 n²/2 次,去掉係數是 <b>O(n²)</b>。第 10 篇學雜湊表之後,可以改成 O(n)。</p>" + cpp("bigo_ex2", "完整答案") + out("bigo_ex2")) + '</div>')

practice = section("practice", "動手演練:確認你真的懂了", ex, QUIZ_HTML,
  checks(["我知道 Big‑O 描述的是「n 變大時操作次數怎麼成長」,不是秒數。",
          "我能說出 O(1)、O(log n)、O(n)、O(n log n)、O(n²)、O(2ⁿ) 的大小順序。",
          "我會用三條規則化簡,例如 <code>3n² + 5n</code> → <code>O(n²)</code>。",
          "我能分辨兩個迴圈是「一個接一個」(O(n))還是「一個套一個」(O(n²))。",
          "我知道 n 變 2 倍時,O(n²) 會變成 4 倍。",
          "我知道 O(n) 不一定在任何情況都比 O(n²) 快,小 n 時要看常數。"], title="學完之後,對照這張清單"),
  resources([
    ("https://en.cppreference.com/cpp/container/vector/push_back", "vector::push_back", "cppreference · 頁面裡有 Complexity 一節,看標準怎麼寫"),
  ], title="cppreference 參考頁面"))

SCRIPT = r'''
Algo.widget("w-count", {
  form: [
    { id: "prog", label: "程式", type: "select", value: "a", options: [["a", "單層迴圈"], ["b", "雙層迴圈"], ["c", "每次砍一半"]] },
    { id: "n", label: "n", type: "number", min: 1, max: 64, value: 5 }
  ],
  runLabel: "執行",
  init: function () { return null; },
  idle: function () { return { cells: [], msg: "選一種程式、設定 n,按「執行」。單層與雙層的 n 請用小一點的數字,才看得清楚。" }; },
  make: function (v) { return Algo.count.count(v.prog, v.n); },
  render: Algo.cellsHtml, code: Algo.count.CODE_COUNT, code_cap: "程式碼(亮起來的行 = 目前執行到的地方)"
});
Algo.curvesInit("w-curves");
'''
SPEC = dict(
  file="datastruct-bigo-guide.html", dir="datastruct", eyebrow_prefix=EYEBROW, foot=FOOT,
  modules=["cells", "alg_count", "curves"], script=SCRIPT,
  title="複雜度與 Big‑O:用操作次數看程式會不會撐不住",
  eyebrow="第 2 篇 · 複雜度與 Big‑O",
  h1="資料變多時會慢多少?數操作次數就知道",
  sub="Big‑O 不量秒數,而是看操作次數隨資料量 n 怎麼成長。這一篇用動畫數一數,再拖動滑桿看六種成長的差距。",
  tldr="單層迴圈 <code>O(n)</code>,雙層迴圈 <code>O(n²)</code>,每次砍一半 <code>O(log n)</code>。化簡只留成長最快的一項、去掉係數。n 變 2 倍時,<code>O(n²)</code> 會慢 4 倍,<code>O(2ⁿ)</code> 很快就算不完。<br><small>先備:會寫 <code>for</code> 迴圈。預估 10 分鐘。難度:入門。</small>",
  toc=[("what", "不量秒,改數步驟"), ("count", "數一數"), ("curves", "六種成長"), ("rules", "化簡規則"), ("gotchas", "常見誤解"), ("practice", "動手寫與測驗")],
  body="\n\n".join([what, count, curves, rules, gotchas, practice]),
  config=dict(sim=SIM, quiz=QUIZ),
  prev=("datastruct-prereq-guide.html", "先備速查:指標、參照與 struct"),
  next=("datastruct-array-guide.html", "陣列與 vector"),
)
