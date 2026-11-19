from dh import *

what = section("what", "雜湊表:用「號碼牌」一步找到東西",
  '<div class="panel"><h3>想像衣帽間</h3>'
  '<p>你把外套交給櫃台,拿到一張號碼牌 <b>37</b>。要取回時,不用把整間衣帽間的外套一件件翻過去,直接走到 37 號掛勾就好。</p>'
  '<p style="margin-bottom:0">雜湊表就是這樣:用一個<strong>雜湊函數</strong>把 key(例如字串 <code>"cat"</code>)變成一個<b>桶子編號</b>,資料就放在那個桶子裡。找的時候再算一次編號,<b>直接走到那個桶子</b>,不必從頭找。</p></div>',
  '<h3 style="margin-top:26px">五個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["key / value", "key 是用來找的名字(<code>\"cat\"</code>),value 是附帶的資料(例如出現次數)。本篇動畫只放 key。"],
    ["雜湊函數", "把 key 算成桶子編號的規則。同一個 key 每次算出來都要一樣。"],
    ["桶子(bucket)", "雜湊表裡的格子,編號 0 到 m − 1。"],
    ["碰撞(collision)", "兩個不同的 key 算出同一個桶子編號。一定會發生(key 比桶子多)。"],
    ["chaining", "解決碰撞的一種方式:每個桶子放一條「鏈」,碰撞的 key 都接在同一個桶子裡。"],
    ["負載因子", "元素個數 ÷ 桶子數。越大,每條鏈越長,越慢。"],
  ]))

play = section("play", "動手玩:雜湊、碰撞與 chaining",
  '<p class="sub" style="margin-bottom:14px">這個迷你雜湊表有 7 個桶子,雜湊函數是「<b>所有字元的編號加起來,再 % 7</b>」(簡單,但不好,等一下就知道為什麼)。黑色那一行是雜湊值的計算過程。</p>',
  try_list(["按「放入 5 個範例」,觀察 <code>cat</code>、<code>act</code>、<code>bird</code> 擠在同一個桶子。", "查詢(contains)<code>act</code>:要比較幾次?再查詢一個不存在的,例如 <code>tac</code>。", "再自己放進 <code>tac</code>(<code>cat</code> 的字母換個順序),看它放哪裡。", "刪除(erase)<code>cat</code>,看鏈怎麼變。"]),
  widget("w-hash", "雜湊表動畫"),
  sim("", "猜猜看:這一步會發生什麼?", "雜湊函數是「字元編號加總 % 7」。<code>cat</code> 和 <code>act</code> 的字母一樣、只是順序不同,它們會放進?",
      [("a1", "不同的桶子"), ("a2", "同一個桶子(發生碰撞)"), ("a3", "放不進去")]))

code = section("code", "完整程式:自己做一個雜湊表",
  '<p class="sub" style="margin-bottom:14px"><code>using Table = ...</code> 是替一個很長的型別取別名:它就是「桶子的陣列,每個桶子是一個字串的 vector」。<code>main</code> 會放進動畫裡那五個 key。</p>',
  cpp("hash_ops"), out("hash_ops", "執行結果(桶子內容,再加兩行查詢結果)"), compile_cmd(),
  '<div class="see"><b class="l">你會看到</b>桶子 4 裡有 <code>cat act bird</code>,桶子 6 裡有 <code>dog god</code>:碰撞真的發生了。最後兩行是 contains 的結果(1 是找到,0 是沒找到)。</div>')

stl = section("stl", "實務上:std::unordered_map 與 unordered_set",
  '<p class="sub" style="margin-bottom:14px">標準函式庫已經提供雜湊表:<code>std::unordered_map&lt;key, value&gt;</code>(有 value)與 <code>std::unordered_set&lt;key&gt;</code>(只有 key)。它會自動擴大桶子,讓負載因子不會太高。</p>',
  cpp("hash_stl"), out("hash_stl"),
  table("g2", ["寫法", "意思"], [
    ["<code>count[w]</code>", "取 w 的 value;<b>如果沒有就新增</b>一個(value 為 0)。"],
    ["<code>count.find(w)</code>", "找 w,找不到回傳 <code>count.end()</code>。不會新增。"],
    ["<code>count.count(w)</code>", "w 出現幾次(對 map 來說是 0 或 1)。常用來判斷有沒有。"],
    ["<code>count.erase(w)</code>", "刪除 w。"],
  ]))

cost = section("cost", "複雜度小表",
  table("g3", ["操作", "平均", "最壞"], [
    ["插入 / 查詢 / 刪除", "<b>O(1)</b>:算桶子,再比較鏈上少數幾個", "O(n):所有 key 擠進同一個桶子"],
    ["空間", "O(n)", "O(n)"],
    ["和 <code>std::map</code> 比", "<code>std::map</code>(第 12 篇的樹)是 O(log n),但 key 是排好序的", "—"],
  ]),
  '<p style="margin-top:14px"><b>平均 O(1) 的條件:</b>雜湊函數要把 key 分散得均勻,而且負載因子別太大。這也是為什麼<code>std::unordered_map</code> 會在太擠時自動擴大桶子並重新放(rehash)。</p>')

gotchas = section("gotchas", "初學者最常卡住的三個地方",
  details("用 <code>m[key]</code> 查詢,結果不小心新增了 key",
    '<p><code>operator[]</code> 找不到時會「幫你建立」。只想看有沒有時,用 <code>find</code> 或 <code>count</code>:</p>' + cpp("hash_bracket") + out("hash_bracket")),
  details("雜湊函數太差:全部擠進同一個桶子",
    '<p>我們的「字元加總」就很差:<code>cat</code>、<code>act</code>、<code>tac</code> 這些字母相同的字一定碰撞。好的雜湊函數會讓順序不同、內容稍有差異的 key 都分散開。標準函式庫對 <code>std::string</code>、<code>int</code> 等型別已經提供了好的雜湊函數。</p>'),
  details("依賴 <code>unordered_map</code> 的走訪順序",
    '<p>雜湊表<b>沒有順序</b>。用 range-for 走訪時,順序取決於內部實作,不同編譯器、甚至擴容之後都可能不同。需要有序的結果時,用 <code>std::map</code>,或先把結果排序。</p>'))

SIM = {
  "a1": "<b>不是。</b>加總不管順序:c + a + t = a + c + t,所以算出同樣的值。回動畫先放 <code>cat</code>,再放 <code>act</code>,看它們落在哪個桶子。",
  "a2": "<b>正確!</b>字母一樣、順序不同,加總結果一模一樣,所以放進同一個桶子,發生碰撞。這也說明了「加總」是個不太好的雜湊函數。",
  "a3": "<b>不是。</b>碰撞不是錯誤,只要用 chaining,同一個桶子可以放好幾個 key(接成一條鏈)。",
}
QUIZ = quiz_cfg([
  ("雜湊表的插入、查詢、刪除,平均時間是?", ["O(1)", "O(log n)", "O(n)"], 0, "算出桶子後直接走過去,只要比較鏈上少數幾個。"),
  ("什麼叫「碰撞」?", ["兩個不同的 key 算出同一個桶子編號", "雜湊函數算不出結果", "桶子滿了放不下"], 0, "碰撞是正常現象,用 chaining 等方式處理。"),
  ("雜湊表最壞情況什麼時候發生?", ["所有 key 都擠進同一個桶子,變成 O(n)", "key 是字串的時候", "桶子數是質數的時候"], 0, "雜湊函數很差或被刻意攻擊時,鏈會變得很長。"),
  ("只想知道某個 key 有沒有在 <code>unordered_map</code> 裡,又不想新增,該用?", ["<code>count</code> 或 <code>find</code>", "<code>m[key]</code>", "<code>m.erase(key)</code>"], 0, "<code>m[key]</code> 找不到會自動新增。"),
  ("<code>unordered_map</code> 走訪時,元素的順序是?", ["沒有保證,不要依賴", "插入的順序", "key 由小到大"], 0, "要有序請用 <code>std::map</code>。"),
])

ex = ('<h3 style="margin-top:30px">動手寫(兩題)</h3>'
  '<div class="panel"><h3>第 1 題:把第 2 篇的 O(n²) 改成 O(n)</h3><p>第 2 篇的 <code>hasPairSum</code> 用雙層迴圈。這次用 <code>unordered_set</code> 記住看過的數字。輸出應該是 <code>1 0</code>。</p>' + cpp("hash_ex1_starter") +
  details("參考答案", "<p>對每個 x,看 <code>target - x</code> 以前有沒有出現過;有就找到了,沒有就把 x 記起來。每個元素只處理一次,查詢是平均 O(1),所以整體 O(n)。</p>" + cpp("hash_ex1", "完整答案") + out("hash_ex1")) + '</div>'
  '<div class="panel" style="margin-top:14px"><h3>第 2 題:找出出現次數最多的單字</h3><p>完成 <code>mostCommon</code>。輸出應該是 <code>cat</code>。</p>' + cpp("hash_ex2_starter") +
  details("參考答案", "<p>先用 <code>unordered_map</code> 數每個單字出現的次數(<code>++count[w]</code>),再走訪找最大的。注意:走訪順序沒有保證,所以題目假設最多的只有一個。</p>" + cpp("hash_ex2", "完整答案") + out("hash_ex2")) + '</div>')

practice = section("practice", "動手演練:確認你真的懂了", ex, QUIZ_HTML,
  checks(["我能說出雜湊函數、桶子、碰撞、chaining 各是什麼。",
          "我知道雜湊表的插入、查詢、刪除平均是 O(1),最壞是 O(n)。",
          "我知道負載因子越大,鏈越長,越慢。",
          "我知道 <code>m[key]</code> 找不到會新增,只查詢要用 <code>find</code> 或 <code>count</code>。",
          "我知道雜湊表沒有順序,要有序用 <code>std::map</code>。",
          "我能用 <code>unordered_set</code> 把「找配對」從 O(n²) 降到 O(n)。"], title="學完之後,對照這張清單"),
  resources([
    ("https://en.cppreference.com/cpp/container/unordered_map", "std::unordered_map", "cppreference · std::unordered_map"),
    ("https://en.cppreference.com/cpp/container/unordered_set", "std::unordered_set", "cppreference · std::unordered_set"),
  ], title="cppreference 參考頁面"))

SCRIPT = r'''
var H = Algo.hash;
Algo.widget("w-hash", {
  form: [{ id: "op", label: "操作", type: "select", value: "insert", options: [["insert", "insert 放入"], ["contains", "contains 查詢"], ["erase", "erase 刪除"]] },
         { id: "key", label: "key(1–8 個英數字)", type: "text", value: "cat" }],
  buttons: [
    { label: "放入 5 個範例", run: function (v, c) { c.setBase(H.fill(["cat", "act", "dog", "god", "bird"])); } },
    { label: "查詢 act", run: function (v, c) { c.set("op", "contains"); c.set("key", "act"); c.run(); } },
    { label: "放入 tac", run: function (v, c) { c.set("op", "insert"); c.set("key", "tac"); c.run(); } }
  ],
  init: H.init,
  idle: function (t) { var f = H.idle(t); f.msg = "7 個桶子(編號 0–6),目前還沒有 key。選操作、輸入 key,按「執行」。"; return f; },
  make: function (v, base) { return H.run(v.op, base, v.key.trim()); },
  render: Algo.bucketsHtml, code: H.CODE_HASH, code_cap: "迷你雜湊表(亮起來的行 = 目前執行到的地方)"
});
'''
SPEC = dict(
  file="datastruct-hash-guide.html", dir="datastruct", eyebrow_prefix=EYEBROW, foot=FOOT,
  modules=["cells", "buckets", "alg_hash"], script=SCRIPT,
  title="雜湊表:用號碼牌一步找到資料",
  eyebrow="第 10 篇 · 雜湊表",
  h1="雜湊表把 key 算成桶子編號,平均一步就找到",
  sub="雜湊函數把 key 變成桶子編號,查詢直接走到那個桶子。這一篇用桶子動畫看雜湊值怎麼算、碰撞怎麼處理,再認識 std::unordered_map。",
  tldr="雜湊函數把 key 算成桶子編號;不同 key 算出同一個桶子叫<b>碰撞</b>,用 chaining 接成一條鏈。插入、查詢、刪除<b>平均 O(1)</b>,最壞 O(n)。實務上用 <code>std::unordered_map</code> 與 <code>unordered_set</code>。<br><small>先備:第 3 篇 vector、第 4 篇鏈的概念、第 6 篇搜尋。預估 15 分鐘。難度:進階。</small>",
  toc=[("what", "直覺:號碼牌"), ("play", "雜湊與碰撞"), ("code", "完整程式"), ("stl", "std::unordered_map"), ("cost", "複雜度小表"), ("gotchas", "常見錯誤"), ("practice", "動手寫與測驗")],
  body="\n\n".join([what, play, code, stl, cost, gotchas, practice]),
  config=dict(sim=SIM, quiz=QUIZ),
  prev=("datastruct-sortadv-guide.html", "進階排序:合併、快速與 std::sort"),
  next=("datastruct-tree-guide.html", "二元樹與走訪"),
)
