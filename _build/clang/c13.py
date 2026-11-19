from ch import *

what = section("what", "容器:幫你整理資料的現成工具",
  '<div class="panel"><h3>三種收納盒,各有脾氣</h3>'
  '<p><b><code>vector</code></b> 像一排有編號的格子,依放入順序排列,可以重複。<b><code>set</code></b> 像一份<b>不重複的名單</b>,自動排好順序。<b><code>map</code></b> 像一本<b>字典</b>:用「鍵」查「值」,鍵不重複,也自動依鍵排好順序。</p>'
  '<p style="margin-bottom:0">它們和 <code>sort</code>、<code>find</code> 這些演算法,都屬於 C++ 的<b>標準樣板函式庫(STL)</b>。有了它們,查找、去重、排序都不用自己寫迴圈。</p></div>',
  '<h3 style="margin-top:26px">五個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["STL", "C++ 內建的一套容器(<code>vector</code>、<code>map</code>、<code>set</code>……)與演算法(<code>sort</code>、<code>find</code>……)。"],
    ["鍵 / 值", "<code>map</code> 的一組資料:用「鍵」找到對應的「值」。"],
    ["<code>pair</code>", "一組成對的資料。<code>map</code> 走訪時,每個元素是一個 pair:<code>kv.first</code> 是鍵,<code>kv.second</code> 是值。"],
    ["<code>begin()</code> / <code>end()</code>", "容器的起點與終點,用來告訴演算法「處理整個容器」。先照抄。"],
    ["演算法", "對容器做事的現成函式,放在 <code>&lt;algorithm&gt;</code>。"],
  ]))

mapsec = section("map", "全貌:什麼時候用哪一個",
  table("g3b", ["容器", "特色", "什麼時候用"], [
    ["<code>vector</code>", "依序、可重複、用索引取值", "一串資料,順序重要;最常用,預設選它"],
    ["<code>set</code>", "不重複、自動排序", "去重、檢查「有沒有出現過」"],
    ["<code>map</code>", "鍵不重複、鍵值對應、依鍵排序", "計次數、用名字查資料(字典)"],
  ]),
  tip("<b>先問自己:我需要「用什麼去查什麼」嗎?</b>需要就用 <code>map</code>;只是要「有沒有」就用 <code>set</code>;其他情況,用 <code>vector</code>。"))

steps_ = section("steps", "照著做:五個步驟", steps(
  step(1, "map:用鍵查值",
       "<code>map&lt;string, int&gt;</code> 的意思是「鍵是 string、值是 int」。用 <code>[鍵]</code> 放入、修改、讀取。",
       code("p13/a1"), term("p13/a1"),
       "<p>下面的 <code>m</code> 是一個 <code>map&lt;string, int&gt;</code>。<b>試著用不存在的鍵按「[key](讀取)」</b>,看看會發生什麼:</p>",
       '<div style="margin:12px 0"><div data-ba="m"></div></div>',
       code("p13/a1b"), term("p13/a1b"),
       warn("用 <code>[]</code> 讀一個<b>不存在的鍵</b>,會順手把這個鍵新增進去。只想「查詢有沒有」時,用 <code>count()</code>,它不會改動 map。", "map 最大的陷阱")),
  step(2, "實用範例:字數統計",
       "<code>freq[w]++</code> 是 <code>map</code> 最經典的用法:每出現一次,對應的次數加 1。橘色是輸入的句子。",
       code("p13/a2"), term("p13/a2"),
       tip("自己在終端機試的話,輸入完要按 <b>Ctrl + D</b>(Windows 是 <b>Ctrl + Z</b> 再按 Enter)告訴程式「輸入結束了」。線上編譯器把句子填在 Input 欄位就會自動結束。")),
  step(3, "set:不重複的集合",
       "把重複的值丟進 <code>set</code>,只會留一份,而且自動由小到大。下面的 <code>s</code> 是一個 <code>set&lt;int&gt;</code>,<b>放進一個已經有的數字</b>看看。",
       code("p13/a3"), term("p13/a3"),
       '<div style="margin-top:12px"><div data-ba="s"></div></div>'),
  step(4, "sort:排序",
       "不用自己寫排序迴圈,<code>sort</code> 一行解決。要由大到小,多加 <code>greater&lt;int&gt;()</code>。",
       code("p13/a4"), term("p13/a4"),
       "<p>忘了引入 <code>&lt;algorithm&gt;</code> 的話,會是這樣:</p>",
       code("p13/e1.err"), errterm("p13/e1.err")),
  step(5, "find 與 count:在容器裡找東西",
       "<code>find</code> 找到會回傳指向它的位置,找不到回傳 <code>end()</code>。<code>it - v.begin()</code> 就是它的索引。",
       code("p13/a5"), term("p13/a5"))
))

stuck = section("stuck", "初學者最常卡住的四個地方",
  details("<code>map</code> 的 <code>size()</code> 莫名變大了",
          "<p>多半是用 <code>[]</code> 讀了不存在的鍵,順手新增了一筆。只想查詢時用 <code>count(鍵)</code> 或 <code>find</code>。</p>"),
  details("<code>set</code> 裡的順序和放進去的順序不同",
          "<p><code>set</code> 與 <code>map</code> 會自動依大小(字串依字典順序)排好,不會記得放入的先後。要保留放入順序,用 <code>vector</code>。</p>"),
  details("編譯說 <code>sort</code> 或 <code>map</code> 沒有宣告",
          "<p>忘了引入標頭檔:<code>sort</code>、<code>find</code>、<code>count</code> 要 <code>#include &lt;algorithm&gt;</code>;<code>map</code> 要 <code>&lt;map&gt;</code>;<code>set</code> 要 <code>&lt;set&gt;</code>。</p>"),
  details("<code>for (auto&amp; kv : m)</code> 看不懂",
          "<p>拆開看:<code>m</code> 是 map,每個元素是一組鍵值(<code>pair</code>)。<code>auto</code> 讓編譯器決定型態,<code>&amp;</code> 是第 12 篇的參考(不複製)。<code>kv.first</code> 是鍵,<code>kv.second</code> 是值。先照著這個樣子用就好。</p>"))

QUIZ = quiz_cfg([
  ("要統計每個單字出現幾次,最適合用哪個容器?", ["map<string, int>", "set<string>", "vector<int>"], 0, "用單字(鍵)查次數(值),正是 map 的用途。"),
  ("<code>set&lt;int&gt; s = {3, 1, 2, 3, 1};</code>,<code>s.size()</code> 是?", ["3", "5", "2"], 0, "set 不重複:只剩 1、2、3 三個。"),
  ("用 <code>m[\"grape\"]</code> 讀取 map 裡不存在的鍵,會?", ["新增這個鍵,值為 0", "回傳錯誤", "什麼都不做"], 0, "[] 讀取不存在的鍵會順手新增。想只查詢請用 count()。"),
  ("<code>sort(v.begin(), v.end())</code> 的結果是?", ["由小到大排序", "由大到小排序", "隨機排列"], 0, "預設由小到大。要由大到小,多給 greater<int>()。"),
  ("<code>find</code> 在容器裡找不到時,回傳?", ["end()", "-1", "0"], 0, "找不到時回傳 end(),要和 end() 比較才知道有沒有找到。"),
])

practice = section("practice", "動手演練:用現成工具解問題",
  '<p class="sub" style="margin-bottom:18px">每題先自己寫,再展開看參考解答。</p>',
  exercise(1, "單字統計", "讀入一句話(輸入 <code>to be or not to be</code>),統計每個單字出現的次數,依字母順序印出。", "p13/x1",
           note="<code>map</code> 本來就依鍵排序,所以輸出自然是字母順序。"),
  exercise(2, "去除重複並排序", "<code>vector</code> 裡有 <code>{5, 3, 5, 1, 3, 9}</code>,用 <code>set</code> 去除重複,並由小到大印出。(對照第 9 篇練習 3:現在不用巢狀迴圈了!)", "p13/x2"),
  exercise(3, "查成績", "建立 <code>map</code>:Mina 90、Leo 75、Amy 82。讀入一個名字,有就印出成績,沒有就印出「查無此人」。用 <code>count</code> 檢查,別用 <code>[]</code>。", "p13/x3",
           before="<p style='margin-bottom:6px'>輸入不存在的名字會是這樣:</p>" + code("p13/x3b", prev="p13/x3") + term("p13/x3b")),
  QUIZ_HTML,
  chk(["我知道 <code>vector</code>、<code>set</code>、<code>map</code> 各適合什麼情況。", "我會用 <code>map</code> 放入、修改與走訪(<code>kv.first</code>、<code>kv.second</code>)。",
       "我知道用 <code>[]</code> 讀不存在的鍵會順手新增,查詢要用 <code>count</code>。", "我知道 <code>set</code> 會自動去重並排序。",
       "我會用 <code>sort(v.begin(), v.end())</code> 排序。", "我會用 <code>find</code> 與 <code>count</code>,並知道要引入 <code>&lt;algorithm&gt;</code>。"]),
  links([("https://en.cppreference.com/cpp/container/map", "cppreference:std::map", "cppreference.com"),
         ("https://en.cppreference.com/cpp/algorithm/sort", "cppreference:std::sort", "cppreference.com")]))

SPEC = spec(
  file="clang-stl-guide.html",
  title="STL:map、set、sort 讓你不用自己寫查找與排序",
  eyebrow="第 13 篇 · STL:map、set、sort",
  h1="<code>map</code>、<code>set</code>、<code>sort</code> 讓你不用自己寫查找與排序",
  sub="認識 C++ 內建的兩個好用容器和兩個常用演算法,並用操作前後對照,看清楚每個操作到底改動了什麼。",
  tldr="<code>map</code> 用<strong>鍵查值</strong>,<code>set</code> 保存<strong>不重複的元素</strong>,兩者都自動排序;<code>sort</code> 排序、<code>find</code> 查找。<strong><code>map</code> 用 <code>[]</code> 讀不存在的鍵會順手新增</strong>,只想查詢請用 <code>count</code>。",
  toc=[("what", "容器是什麼"), ("map", "怎麼選"), ("steps", "五個步驟"), ("stuck", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, mapsec, steps_, stuck, practice]),
  config=dict(beforeafter=dict(
      m=dict(kind="map", name="m", init={"apple": 7, "banana": 3}),
      s=dict(kind="set", name="s", init=[1, 3, 5])), quiz=QUIZ),
  **nav(13),
)
