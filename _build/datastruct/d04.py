from dh import *

what = section("what", "鏈結串列是一條「下一站在哪」的接力",
  '<div class="panel"><h3>用「尋寶遊戲的紙條」來想</h3>'
  '<p>每個節點是一張紙條,上面寫著<strong>寶藏(資料)</strong>和<strong>下一張紙條放在哪裡</strong>。你手上只有第一張(<code>head</code>),要看第 5 張,就得從第 1 張一路照著「下一站」走過去。</p>'
  '<p style="margin-bottom:0">紙條可以散落在記憶體各處,不必緊貼。所以<b>插入、刪除只要改「下一站」的指向,不用搬動任何資料</b>;代價是沒有索引,不能一步跳到第 i 個。這正好和上一篇的 vector 相反。</p></div>',
  '<h3 style="margin-top:26px">五個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["節點(node)", "一張紙條:放一筆資料 <code>val</code>,加上指向下一個節點的 <code>next</code>。"],
    ["<code>next</code>", "指向下一個節點的指標(上一篇的指標)。"],
    ["<code>head</code>", "指向第一個節點的指標。串列只靠它找到整串資料,弄丟它就找不到了。"],
    ["<code>nullptr</code>", "最後一個節點的 <code>next</code>,表示「後面沒有了」。空串列是 <code>head == nullptr</code>。"],
    ["走訪(traverse)", "從 head 開始,沿著 next 一個個往下走,直到遇到 nullptr。"],
  ]),
  '<div class="tip"><b class="l">這一篇是「單向」的</b>每個節點只知道下一個。還有「雙向」鏈結串列,節點多存一個指向前一個的指標,<code>std::list</code> 就是雙向的(見下方 STL 一節)。</div>')

play = section("play", "動手玩:插入與刪除只改指標",
  '<p class="sub" style="margin-bottom:14px">下面的圖是一條鏈結串列,每個方框左邊是資料、右邊的圓點是 next 指標。按「執行」後,一步一步看每一行程式怎麼改指標。右上角的數字會告訴你改了幾個指標、走訪了幾個節點。</p>',
  try_list(["按「頭插」:改了幾個指標?再按「尾插」,走訪了幾個節點?", "按「中間插入」(第 0 個節點後面):看新節點先接哪裡、後接哪裡。", "按「刪頭」,看被刪的節點變成虛線框後才消失。", "重複幾次頭插到滿(6 個),看看會出現什麼提示。"]),
  widget("w-list", "鏈結串列插入刪除動畫"),
  sim("", "猜猜看:這一步會發生什麼?", "串列有 5 個節點,在<b>最前面</b>插入一個新節點,要改幾個指標?(對照上一篇:vector 要搬動 5 個元素)",
      [("a1", "5 個,每個節點都要動"), ("a2", "2 個:新節點的 next 與 head"), ("a3", "0 個")]),
  '<p style="margin-top:14px">注意:這裡的「O(1)」有一個前提——<b>你已經拿到要操作的位置</b>(頭插是 head;<code>insertAfter</code> 是 prev)。如果要「在第 k 個之後插入」,光是找到第 k 個就要走訪 k 步。')

code = section("code", "完整程式:五個基本操作",
  '<p class="sub" style="margin-bottom:14px">這就是動畫裡用的函式,加上印出與清除。<code>clear</code> 會把每個節點 <code>delete</code> 掉,讓程式沒有記憶體洩漏。</p>',
  cpp("linked_ops"), out("linked_ops"), compile_cmd(),
  '<h3 style="margin-top:22px">三個要記住的小規則</h3>',
  table("g2", ["規則", "原因"], [
    ["插入:先設新節點的 <code>next</code>,最後才改 <code>prev-&gt;next</code>", "一旦先改了 prev->next,就弄丟了原本的下一個節點(見下方「常見錯誤」)。"],
    ["刪除:先用 <code>old</code> 記住要刪的節點", "指標改走之後,就再也找不到它,沒辦法 delete,會洩漏。"],
    ["每個 <code>new</code> 對應一個 <code>delete</code>", "所以最後用 <code>clear</code> 把整串清掉。"],
  ]))

compare = section("compare", "和 vector 比:各有各的強項",
  '<p class="sub" style="margin-bottom:14px">n 是元素個數。「已拿到位置」表示你手上已經有 prev(或 head)。</p>',
  table("g3", ["操作", "vector", "鏈結串列(本篇的單向版)"], [
    ["讀第 i 個元素", "<b>O(1)</b>,索引直接算", "O(n),從 head 一個個走"],
    ["在最前面插入", "O(n),全部搬一格", "<b>O(1)</b>,改 2 個指標"],
    ["在最後面插入", "平均 O(1)", "O(n),要先走到最後(有存 tail 指標的版本是 O(1))"],
    ["已拿到位置後,中間插入 / 刪除", "O(n),後面要搬動", "<b>O(1)</b>,改 1~2 個指標"],
    ["記憶體", "連續一整塊", "每個節點分開放,另外多存一個指標"],
  ]),
  '<div class="tip"><b class="l">實務上怎麼選?</b>大多數時候 <code>std::vector</code> 就夠好,甚至更快:連續的記憶體對 CPU 快取比較友善,而鏈結串列的節點散在各處。鏈結串列的價值在於它讓你<b>理解「用指標串起資料」</b>,後面的樹、圖、雜湊表都是同一個想法。</div>')

stl = section("stl", "實務上:std::list",
  '<p class="sub" style="margin-bottom:14px"><code>std::list</code> 是雙向鏈結串列,已經幫你寫好 <code>push_front</code>、<code>push_back</code>、<code>insert</code>、<code>erase</code>,也不用自己 delete。<code>it</code> 是「迭代器」,可以先當成「指向某個節點的位置」。</p>',
  cpp("linked_stl"), out("linked_stl"),
  '<p>因為是雙向的,頭尾插入都是 O(1)。但它一樣沒有索引,<code>lst[3]</code> 是不能用的。只想要單向、更省空間時,有 <code>std::forward_list</code>。</p>')

gotchas = section("gotchas", "初學者最常卡住的三個地方",
  details("插入時順序寫反:先改 <code>prev-&gt;next</code>,再設 <code>node-&gt;next</code>",
    '<p>下面這段可以編譯,但是會出問題:第一行改完之後,<code>prev-&gt;next</code> 已經是 <code>node</code> 自己,原本的下一個節點就弄丟了,而且 <code>node-&gt;next</code> 變成指向自己。</p>' + cpp("linked_wrong", "錯誤示範(不要執行)", copy=False) +
    '<p>口訣:<b>先接後面,再接前面</b>。先讓新節點指向後面的人,最後才讓前面的人指向新節點。</p>'),
  details("走訪時沒檢查 nullptr,<code>cur-&gt;next</code> 當掉",
    '<p>如果 <code>cur</code> 本身已經是 <code>nullptr</code>,再寫 <code>cur-&gt;next</code> 就是對空指標取成員,程式會當掉。迴圈條件要寫對:走訪全部用 <code>cur != nullptr</code>;要停在最後一個節點用 <code>cur-&gt;next != nullptr</code>(而且要先確認串列不是空的)。</p>'),
  details("刪掉節點後記憶體洩漏,或 head 弄丟了",
    '<p>刪除第一個節點時,如果直接 <code>list.head = list.head-&gt;next;</code> 而沒有先記住舊的 head,舊節點就再也 delete 不到了。如果更慘,先 <code>delete</code> 了節點才去讀 <code>old-&gt;next</code>,那是在用已經還給系統的記憶體。順序是:記住 → 改指標 → delete。</p>'))

SIM = {
  "a1": "<b>不是。</b>鏈結串列不用搬動資料。回動畫按「頭插」,右上角看「改了幾個指標」。",
  "a2": "<b>正確!</b>新節點的 next 指向原本的第一個節點,再把 head 改指向新節點,只改 2 個指標,不管串列多長都一樣,是 O(1)。vector 要搬 5 個元素,是 O(n)。",
  "a3": "<b>不是。</b>至少要讓新節點接上串列,並讓 head 指向它,所以要改 2 個指標。",
}
QUIZ = quiz_cfg([
  ("在 5 個節點的單向串列最前面插入新節點,要改幾個指標?", ["5 個", "2 個(新節點的 next 與 head)", "0 個"], 1,
   "新節點的 next 指向原本的第一個節點,head 改指向新節點。和串列多長無關。"),
  ("為什麼鏈結串列「讀第 i 個元素」是 O(n)?", ["沒有索引,只能從 head 一個個往下走", "因為節點很大", "因為必須先排序"], 0,
   "節點散在記憶體各處,位置不能用算的,只能沿著 next 一個個找。"),
  ("刪除節點時,為什麼要先用 <code>old</code> 記住它?", ["指標改走之後就找不到它,沒辦法 delete,會記憶體洩漏", "語法規定要這樣", "為了讓程式變慢"], 0,
   "先記住,才能在改完指標之後 delete 它。"),
  ("在 prev 後面插入新節點,正確順序是?", ["先設新節點的 next 指向 prev 原本的下一個,最後才改 prev-&gt;next", "先改 prev-&gt;next,再設新節點的 next", "順序無所謂"], 0,
   "先改 prev->next 會弄丟原本的下一個節點。口訣:先接後面,再接前面。"),
  ("單向串列最後一個節點的 <code>next</code> 應該是?", ["nullptr", "指向 head", "隨便一個值"], 0,
   "nullptr 表示後面沒有節點了,走訪時就靠它判斷結束。"),
])

ex = ('<h3 style="margin-top:30px">動手寫(兩題)</h3>'
  '<p class="sub" style="margin-bottom:12px">兩題都是「走訪」:從 head 沿著 next 走到 nullptr。</p>'
  '<div class="panel"><h3>第 1 題:數節點個數</h3><p>完成 <code>length</code>,回傳串列有幾個節點。輸出應該是 <code>3 0</code>(最後的 0 是空串列)。</p>' + cpp("linked_ex1_starter") +
  details("參考答案", "<p>用 <code>cur</code> 從 head 出發,只要不是 nullptr 就計數並往下走。時間是 O(n)。</p>" + cpp("linked_ex1", "完整答案") + out("linked_ex1")) + '</div>'
  '<div class="panel" style="margin-top:14px"><h3>第 2 題:找出第一個值等於 target 的節點</h3><p>完成 <code>findNode</code>,找不到回傳 <code>nullptr</code>。輸出應該是 <code>20 -1</code>。(這就是「插入之前要先找 prev」的那一步。)</p>' + cpp("linked_ex2_starter") +
  details("參考答案", "<p>一樣是走訪,每到一個節點就比較 val,相等就回傳它;走完都沒有就回傳 nullptr。</p>" + cpp("linked_ex2", "完整答案") + out("linked_ex2")) + '</div>')

practice = section("practice", "動手演練:確認你真的懂了", ex, QUIZ_HTML,
  checks(["我能說出節點、next、head、nullptr 各是什麼。",
          "我知道在最前面插入只要改 2 個指標,所以是 O(1)。",
          "我知道為什麼讀第 i 個元素是 O(n):要從 head 一個個走。",
          "我記得插入的口訣:先接後面,再接前面。",
          "我知道刪除前要先用 <code>old</code> 記住節點,最後才 <code>delete</code>。",
          "我能比較 vector 與鏈結串列各自擅長什麼,也知道實務上多半用 vector。"], title="學完之後,對照這張清單"),
  resources([
    ("https://en.cppreference.com/cpp/container/list", "std::list", "cppreference · std::list(雙向鏈結串列)"),
    ("https://en.cppreference.com/cpp/container/forward_list", "std::forward_list", "cppreference · std::forward_list(單向鏈結串列)"),
  ], title="cppreference 參考頁面"))

SCRIPT = r'''
var L = Algo.list;
Algo.widget("w-list", {
  form: [
    { id: "op", label: "操作", type: "select", value: "pushFront", options: [["pushFront", "頭插 pushFront"], ["pushBack", "尾插 pushBack"], ["insertAfter", "在第 k 個節點後插入"], ["eraseFront", "刪頭 eraseFront"], ["eraseAfter", "刪第 k 個節點後面的"]] },
    { id: "k", label: "k(從 0 數)", type: "number", min: 0, max: 5, value: 0, showIf: { op: ["insertAfter", "eraseAfter"] } },
    { id: "v", label: "數值", type: "number", min: 0, max: 99, value: 99, showIf: { op: ["pushFront", "pushBack", "insertAfter"] } }
  ],
  buttons: [
    { label: "頭插", run: function (v, c) { c.set("op", "pushFront"); c.run(); } },
    { label: "尾插", run: function (v, c) { c.set("op", "pushBack"); c.run(); } },
    { label: "中間插入", run: function (v, c) { c.set("op", "insertAfter"); c.set("k", 0); c.run(); } },
    { label: "刪頭", run: function (v, c) { c.set("op", "eraseFront"); c.run(); } }
  ],
  init: function () { return [10, 20, 30]; },
  idle: function (b) { var f = L.idle(b); f.msg = "串列現在是 " + (b.length ? b.join(" → ") + " → null" : "空的") + "。選一個操作,按「執行」。"; return f; },
  make: function (v, base) {
    switch (v.op) {
      case "pushFront": return L.pushFront(base, v.v);
      case "pushBack": return L.pushBack(base, v.v);
      case "insertAfter": return L.insertAfter(base, v.k, v.v);
      case "eraseFront": return L.eraseFront(base);
      default: return L.eraseAfter(base, v.k);
    }
  },
  render: Algo.listHtml, code: L.CODE_LIST, code_cap: "程式碼(亮起來的行 = 目前執行到的地方)"
});
'''
SPEC = dict(
  file="datastruct-linkedlist-guide.html", dir="datastruct", eyebrow_prefix=EYEBROW, foot=FOOT,
  modules=["cells", "list", "alg_list"], script=SCRIPT,
  title="鏈結串列:插入刪除只改指標,不搬資料",
  eyebrow="第 4 篇 · 鏈結串列",
  h1="鏈結串列的插入刪除只改指標,代價是不能直接跳到第 i 個",
  sub="每個節點存一筆資料和「下一個在哪」。這一篇用節點箭頭圖,逐行看指標怎麼改,再和上一篇的 vector 比較取捨。",
  tldr="節點用 <code>next</code> 串起來,頭插只改 2 個指標,是 <code>O(1)</code>;但沒有索引,讀第 i 個要從 head 走 <code>O(n)</code>。插入口訣:<b>先接後面,再接前面</b>;每個 <code>new</code> 都要有對應的 <code>delete</code>。<br><small>先備:第 1 篇的指標與 <code>new</code>/<code>delete</code>、第 3 篇的 vector。預估 15 分鐘。難度:基礎。</small>",
  toc=[("what", "直覺:接力紙條"), ("play", "插入與刪除"), ("code", "完整程式"), ("compare", "和 vector 比"), ("stl", "std::list"), ("gotchas", "常見錯誤"), ("practice", "動手寫與測驗")],
  body="\n\n".join([what, play, code, compare, stl, gotchas, practice]),
  config=dict(sim=SIM, quiz=QUIZ),
  prev=("datastruct-array-guide.html", "陣列與 vector"),
  next=("datastruct-stackqueue-guide.html", "堆疊與佇列"),
)
