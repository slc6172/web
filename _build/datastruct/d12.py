from dh import *

what = section("what", "直覺:把二分搜尋做成一棵樹",
  '<div class="panel"><h3>第 6 篇的二分搜尋,每次都先看「正中間」</h3>'
  '<p>在排好序的 <code>1 2 3 4 5 6 7</code> 裡找 5:先看中間的 4,5 比較大就往右半邊,再看 6,比較小就往左……每次砍掉一半。如果把「每次先看的那個數」畫成一棵樹,中間的 4 是根,左右兩邊各自再選中間的數當子節點。這就是一棵<strong>二元搜尋樹</strong>(BST)。</p>'
  '<p style="margin-bottom:0">好處是:二分搜尋要求資料放在陣列裡、而且<b>事先排好序</b>,中間插入一個數得搬動一大堆元素(第 3 篇);樹用<b>指標</b>連起來,插入只要接一條線(第 4 篇),又保留「每次砍一半」的找法。</p></div>',
  '<h3 style="margin-top:26px">唯一的規則,和幾個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["BST 規則", "對<b>每一個</b>節點:左子樹裡的值<b>全部比它小</b>,右子樹裡的值<b>全部比它大</b>(本篇不放重複的值)。"],
    ["搜尋", "比大小:小就往左、大就往右,走到相等就找到了,走到 <code>nullptr</code> 就是沒有。"],
    ["插入", "照搜尋的路走到 <code>nullptr</code>,新節點就放在那裡。新節點一定是葉。"],
    ["後繼(successor)", "比某個值大的值裡<b>最小</b>的那個。在 BST 裡,就是「右子樹一路往左走到底」的節點。刪除時會用到。"],
    ["中序走訪", "第 11 篇的「左 → 根 → 右」,在 BST 上剛好是<b>由小到大</b>。這是檢查 BST 有沒有壞掉的好方法。"],
  ]),
  '<div class="tip"><b class="l">節點長得和第 11 篇一樣</b>還是 <code>struct TreeNode { int val; TreeNode* left; TreeNode* right; };</code>。差別不在長相,而在<b>放進去的位置有規則</b>。</div>')

play = section("play", "動手玩:插入、查詢、刪除,看樹怎麼長",
  '<p class="sub" style="margin-bottom:14px">選操作、輸入 1~99 的數字,按「執行」再用「下一步」逐步看。<b>綠色</b>是走過的路或新節點,<b>橘色</b>是目前比較的節點,<b>虛線紅框</b>是即將被刪掉的節點。下方「中序」那排永遠由小到大。動畫最多放 10 個節點。</p>',
  try_list(["按「平衡範例」,再 <b>search 6</b>:數數看比較了幾次。", "<b>insert 5</b>(放在最底下的葉),看新節點一定長在葉的位置。",
            "<b>erase 1</b>(葉)、<b>erase 2</b>(只剩一個子節點)、<b>erase 4</b>(根,有兩個子節點)各做一次,看三種情況有什麼不同。", "按「排序後插入 1~7」,樹變成一條鏈;再 <b>search 7</b>,比較次數是多少?"]),
  widget("w-bst", "二元搜尋樹動畫"),
  sim("", "猜猜看:會長成什麼形狀?", "把 <code>1, 2, 3, 4, 5, 6, 7</code>(由小到大)依序插入一棵空的 BST,樹會是什麼形狀?",
      [("a1", "矮矮胖胖的平衡樹,高度 3"), ("a2", "一條往右下的鏈,高度 7"), ("a3", "和插入順序無關,永遠是同一個形狀")]),
  '<h3 style="margin-top:26px">刪除有三種情況</h3>',
  '<p class="sub" style="margin-bottom:12px">搜尋與插入都只是「照路走」,刪除才需要想一下:拿掉節點之後,它的子樹要接去哪裡?</p>',
  table("g3", ["情況", "怎麼做", "在程式的哪裡"], [
    ["葉(沒有子節點)", "直接 <code>delete</code>,這個位置變成 <code>nullptr</code>。", "<code>bst_ops.cpp</code> 第 50–54 行(左邊是 nullptr 時,右邊也是 nullptr,回傳的 <code>r</code> 就是 nullptr)"],
    ["只有一個子節點", "<code>delete</code> 它,讓<b>唯一的子節點</b>頂替它的位置,整棵子樹跟著上來。", "第 50–54 行(只有右子)、第 55–59 行(只有左子)"],
    ["有兩個子節點", "不能直接拿掉。找<b>後繼</b>(右子樹最小的),把後繼的<b>值抄過來</b>,再到右子樹把後繼那個節點刪掉(它最多只有右子節點,屬於前兩種情況)。", "第 60–62 行"],
  ]))

code = section("code", "完整程式:插入、搜尋、刪除",
  '<p class="sub" style="margin-bottom:14px">四個函式都是遞迴,而且都長得像 <code>node-&gt;left = f(node-&gt;left, val)</code>:<b>先處理子樹,再把回傳的新根接回來</b>。回傳值就是這棵子樹「現在的根」,所以刪掉子樹的根時,上一層才能接到頂替的節點。</p>',
  cpp("bst_ops"), out("bst_ops", "執行結果(依序:中序與前序、search、四次 erase 後的前序、最後的中序)"), compile_cmd(),
  '<div class="tip"><b class="l">怎麼讀輸出</b>第一組樹是依序插入 <code>5 3 8 1 4 7 9 2 6</code>。<code>erase 2</code> 是葉;<code>erase 7</code> 只有左子 6;<code>erase 3</code> 有兩個子節點,後繼 4 的值蓋過來;<code>erase 5</code> 是根,後繼 6 的值蓋過來。這份程式用 <code>-fsanitize=address</code> 檢查過,沒有洩漏。</div>')

degen = section("degen", "退化:同樣的資料,插入順序決定樹的高度",
  '<p class="sub" style="margin-bottom:14px">BST 的規則只管「大小關係」,完全不管「平不平衡」。資料如果本來就排好序,每個新值都比前面所有的值大,就一直往右接,樹變成一條<b>鏈</b>,其實就是第 4 篇的鏈結串列。</p>',
  cpp("bst_degenerate"), out("bst_degenerate"),
  '<p style="margin-top:14px">7 個值,高度可以是 3,也可以是 7。差距隨 n 放大:100 萬個值,平衡的樹約 20 層,鏈卻有 <b>100 萬</b>層,搜尋從「走 20 步」變成「走 100 萬步」,遞迴還可能 stack overflow(第 7、11 篇)。</p>',
  '<div class="tip"><b class="l">解法:自動平衡</b>AVL 樹、紅黑樹會在插入、刪除之後<b>旋轉</b>子樹,讓高度維持在 <code>O(log n)</code>。旋轉的細節不在本篇範圍;下一節的 <code>std::set</code> 與 <code>std::map</code> 就已經幫你做好了。</div>')

stl = section("stl", "實務上:std::set 與 std::map",
  '<p class="sub" style="margin-bottom:14px">自己寫 BST 是為了弄懂原理。實務上直接用 <code>std::set</code>(只存值)和 <code>std::map</code>(存 key 與 value)。C++ 標準只規定它們的複雜度是 <code>O(log n)</code>,常見實作是自動平衡的<b>紅黑樹</b>,所以不會退化成鏈。</p>',
  cpp("bst_stl"), out("bst_stl", "執行結果"),
  table("g3", ["需求", "選哪個", "時間"], [
    ["要「排好序」走訪,或找「第一個 ≥ x」(<code>lower_bound</code>)", "<code>std::set</code> / <code>std::map</code>", "<code>O(log n)</code>"],
    ["只要「有沒有」或查 key,不在乎順序", "<code>std::unordered_set</code> / <code>unordered_map</code>(第 10 篇)", "平均 <code>O(1)</code>"],
    ["資料放著、偶爾二分搜尋", "排好序的 <code>std::vector</code> + <code>std::binary_search</code>(第 6 篇)", "查詢 <code>O(log n)</code>,插入 <code>O(n)</code>"],
  ]))

cost = section("cost", "複雜度小表",
  '<p class="sub" style="margin-bottom:14px">n 是節點數,h 是樹的高度。搜尋、插入、刪除都是沿著<b>一條從根往下的路</b>走,所以時間是 <code>O(h)</code>。</p>',
  table("g3", ["操作", "樹很平衡(h ≈ log n)", "樹退化成鏈(h = n)"], [
    ["search / insert / erase", "<code>O(log n)</code>", "<code>O(n)</code>"],
    ["中序走訪(印出全部,已排序)", "<code>O(n)</code>", "<code>O(n)</code>"],
    ["遞迴使用的額外空間", "<code>O(log n)</code>", "<code>O(n)</code>"],
  ]),
  '<p style="margin-top:14px">一句話:<b>BST 的速度取決於高度</b>。所以才有各種「讓樹保持矮胖」的平衡樹。</p>')

gotchas = section("gotchas", "初學者最常卡住的四個地方",
  details("刪除兩個子節點時,直接把節點拿掉",
    '<p>只有一個指標位置,卻有兩棵子樹要接,放不下。正確做法是找<b>後繼</b>(右子樹最小的)的值抄過來,再刪掉後繼。用「左子樹最大的」(前驅)也可以,對稱。</p>'),
  details("忘了把回傳值接回去",
    '<p><code>node-&gt;left = insert(node-&gt;left, val);</code> 的 <code>node-&gt;left =</code> 不能省。寫成單獨一行 <code>insert(node-&gt;left, val);</code>,新節點 <code>new</code> 出來卻沒有任何指標指向它,樹沒變、記憶體也洩漏。呼叫端同理:要寫 <code>root = insert(root, v);</code>,否則空樹永遠是空的。</p>'),
  details("忽略重複的值",
    '<p>這份程式遇到相等的值什麼都不做(和 <code>std::set</code> 一樣)。如果需要重複值,要先決定規則:例如多存一個「出現次數」,或統一放右邊(<code>std::multiset</code> 就允許重複)。不決定就寫,搜尋和刪除會出現怪結果。</p>'),
  details("以為 BST 一定很快",
    '<p>資料已經排好序、或幾乎排好序時,依序插入會得到一條鏈,<code>O(log n)</code> 變成 <code>O(n)</code>。實務上用 <code>std::set</code> / <code>std::map</code>,或自己實作平衡樹。</p>'))

SIM = {
  "a1": "<b>不是。</b>BST 只看大小關係,不會自動調整形狀。每個新值都比前面的大,就一直往右接。按動畫的「排序後插入 1~7」看看。",
  "a2": "<b>正確!</b>1 是根,2 比 1 大放右邊,3 比 1、2 都大再往右……變成一條高度 7 的鏈。同樣這 7 個數,先插入 4、2、6、1、3、5、7,高度只有 3。",
  "a3": "<b>不是。</b>形狀取決於插入的順序。<code>4 2 6 1 3 5 7</code> 會長成矮胖的樹(高度 3),<code>1 2 3 4 5 6 7</code> 卻是一條鏈(高度 7)。",
}
QUIZ = quiz_cfg([
  ("二元搜尋樹(BST)的規則是?", ["每個節點的左子節點比右子節點小", "每個節點的左子樹的值都比它小,右子樹的值都比它大", "每一層由左到右排好序"], 1, "規則是對整棵子樹成立,不只是直接的子節點。"),
  ("對 BST 做哪一種走訪,會由小到大走過每個節點?", ["前序", "後序", "中序"], 2, "中序是左 → 根 → 右,正好是由小到大。"),
  ("刪除有兩個子節點的節點,本篇的做法是?", ["把右子樹整棵接到它的父節點", "用後繼(右子樹最小的值)蓋過它的值,再刪掉後繼", "把它和兩棵子樹都刪掉"], 1, "後繼最多只有右子節點,刪起來簡單。"),
  ("想要「自動排好序、插入查詢刪除都是 O(log n)」的 C++ 容器,該用?", ["std::unordered_set", "std::set", "std::vector"], 1, "std::set 通常是紅黑樹,自動平衡;unordered_set 沒有順序。"),
  ("BST 退化成一條鏈時,search 要花多久?", ["O(1)", "O(log n)", "O(n)"], 2, "高度是 n,最壞要從根一路走到最底。"),
])

ex = ('<h3 style="margin-top:30px">動手寫(兩題)</h3>'
  '<p class="sub" style="margin-bottom:12px">兩題都在同一棵樹上測試:根 5,左邊 3(再接 1),右邊 7。</p>'
  '<div class="panel"><h3>第 1 題:用迴圈寫 contains</h3><p>不用遞迴,從根出發,小就往左、大就往右,直到找到或走到 <code>nullptr</code>。輸出應該是 <code>1100</code>。</p>' + cpp("bst_ex1_starter") +
  details("參考答案", "<p>每一步只會走一邊,所以用 <code>while</code> 迴圈就夠了,額外空間只要 <code>O(1)</code>(遞迴版是 <code>O(h)</code>)。</p>" + cpp("bst_ex1", "完整答案") + out("bst_ex1")) + '</div>'
  '<div class="panel" style="margin-top:14px"><h3>第 2 題:把 BST 依序放進 vector</h3><p>用中序走訪把值放進 <code>out</code>。輸出應該是 <code>1 3 5 7</code>(已經排好序)。</p>' + cpp("bst_ex2_starter") +
  details("參考答案", "<p>就是第 11 篇的中序:先左、再把自己放進去、最後右。不用排序,走完就是排好的,時間 <code>O(n)</code>。</p>" + cpp("bst_ex2", "完整答案") + out("bst_ex2")) + '</div>')

practice = section("practice", "動手演練:確認你真的懂了", ex, QUIZ_HTML,
  checks(["我能說出 BST 的規則:左子樹全部比自己小,右子樹全部比自己大。",
          "我能口述 search 與 insert:小往左、大往右,走到 nullptr 就放在那裡。",
          "我能分辨刪除的三種情況,並說出「後繼」是什麼。",
          "我知道 <code>node-&gt;left = insert(...)</code> 的回傳值一定要接回去。",
          "我知道依序插入排好序的資料會退化成鏈,時間變成 O(n)。",
          "我知道實務上用 <code>std::set</code> / <code>std::map</code>,它們自動平衡。"], title="學完之後,對照這張清單"),
  resources([
    ("https://en.cppreference.com/cpp/container/set", "std::set", "cppreference · std::set"),
    ("https://en.cppreference.com/cpp/container/map", "std::map", "cppreference · std::map"),
  ], title="cppreference 參考頁面"))

SCRIPT = r'''
var B = Algo.bst;
function inorderCells(T) {
  var out = [];
  (function go(id) { if (!id) return; var n = T.nodes[id]; go(n.l); out.push({ v: n.label, cls: n.cls === "cur" || n.cls === "new" || n.cls === "del" ? n.cls : "" }); go(n.r); })(T.root);
  return out;
}
function render(f) {
  var h = Algo.treeHtml({ tree: f.tree });
  var cells = inorderCells(f.tree);
  if (cells.length) h += Algo.cellsHtml({ rows: [{ label: "中序(左 → 根 → 右,應該由小到大)", cells: cells, empty: 0 }] });
  return h + Algo.cellsHtml({ cells: [], chips: f.chips });
}
function randomList() {
  var s = {}, a = [];
  while (a.length < 7) { var v = 1 + Math.floor(Math.random() * 99); if (!s[v]) { s[v] = 1; a.push(v); } }
  return a;
}
Algo.widget("w-bst", {
  form: [{ id: "op", label: "操作", type: "select", value: "insert", options: Object.keys(B.NAMES).map(function (k) { return [k, B.NAMES[k]]; }) },
         { id: "val", label: "數字(1–99)", type: "number", value: 5, min: 1, max: 99 }],
  buttons: [
    { label: "平衡範例", run: function (v, c) { c.setBase(B.fromList([4, 2, 6, 1, 3, 5, 7])); } },
    { label: "排序後插入 1~7", run: function (v, c) { c.setBase(B.fromList([1, 2, 3, 4, 5, 6, 7])); } },
    { label: "隨機 7 個", run: function (v, c) { c.setBase(B.fromList(randomList())); } }
  ],
  init: B.init,
  idle: B.idle,
  make: function (v, base) { return B.run(v.op, v.val, base); },
  render: render, code: B.CODE_BST, code_cap: "二元搜尋樹(亮起來的行 = 目前執行到的地方)"
});
'''
SPEC = dict(
  file="datastruct-bst-guide.html", dir="datastruct", eyebrow_prefix=EYEBROW, foot=FOOT,
  modules=["cells", "tree", "alg_bst"], script=SCRIPT,
  title="二元搜尋樹:插入、搜尋、刪除與退化",
  eyebrow="第 12 篇 · 二元搜尋樹",
  h1="小的往左、大的往右:一棵會自己排好序的樹",
  sub="二元搜尋樹把二分搜尋做成指標連起來的樹。這一篇用動畫看插入、搜尋與刪除的三種情況,再看為什麼排序後插入會退化成一條鏈。",
  tldr="BST 規則:左子樹全部比自己小、右子樹全部比自己大,所以搜尋、插入、刪除都是沿著一條路往下走,時間 <code>O(h)</code>(h 是高度)。樹平衡時 <code>O(log n)</code>,退化成鏈時 <code>O(n)</code>。實務上用自動平衡的 <code>std::set</code> / <code>std::map</code>。<br><small>先備:第 6 篇二分搜尋、第 7 篇遞迴、第 11 篇二元樹與中序。預估 18 分鐘。難度:進階。</small>",
  toc=[("what", "直覺:二分搜尋變成樹"), ("play", "插入、查詢、刪除"), ("code", "完整程式"), ("degen", "退化成鏈"), ("stl", "std::set / map"), ("cost", "複雜度小表"), ("gotchas", "常見錯誤"), ("practice", "動手寫與測驗")],
  body="\n\n".join([what, play, code, degen, stl, cost, gotchas, practice]),
  config=dict(sim=SIM, quiz=QUIZ),
  prev=("datastruct-tree-guide.html", "二元樹與走訪"),
  next=("datastruct-heap-guide.html", "堆積與優先佇列"),
)
