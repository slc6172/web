from dh import *

what = section("what", "樹:一層一層往下分岔的資料",
  '<div class="panel"><h3>像家族圖,或電腦的資料夾</h3>'
  '<p>資料夾裡有子資料夾,子資料夾裡又有子資料夾……這就是<strong>樹</strong>。最上面只有一個起點(<b>根</b>),每個節點往下連到它的<b>子節點</b>。</p>'
  '<p style="margin-bottom:0">這一篇的<strong>二元樹</strong>規定:每個節點<b>最多兩個</b>子節點,分別叫「左」和「右」。你在第 4 篇學的鏈結串列,其實就是「每個節點只有一個子節點」的樹。</p></div>',
  '<h3 style="margin-top:26px">名詞對照</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["根(root)", "最上面的節點,沒有父節點。"],
    ["葉(leaf)", "沒有任何子節點的節點。"],
    ["父 / 子", "一個節點往下連到的,是它的子;反過來是父。"],
    ["子樹", "某個節點和它底下的全部。<b>一棵樹 = 根 + 左子樹 + 右子樹</b>,這正是遞迴的形狀。"],
    ["高度", "從根到最遠的葉,最長的那條路上有幾個節點。"],
    ["走訪(traversal)", "把每個節點恰好看過一遍的方式,順序有好幾種。"],
  ]),
  '<div class="tip"><b class="l">節點長這樣</b>跟第 4 篇的鏈結串列節點很像:<code>struct TreeNode { int val; TreeNode* left; TreeNode* right; };</code>,多了一個指標。沒有子節點時,指標是 <code>nullptr</code>。</div>')

play = section("play", "動手玩:四種走訪,看順序怎麼來",
  '<p class="sub" style="margin-bottom:14px">選一棵樹、一種走訪法,按「下一步」。橘色是目前所在的節點,綠色是已經印出來的。上面的「呼叫堆疊」(前、中、後序)或 queue(層序)會顯示目前的狀態。</p>',
  try_list(["用<b>完全二元樹</b>跑前序、中序、後序:同一棵樹,印出來的順序差在哪?", "看遞迴版的 <code>nullptr</code> 返回:每個葉的左右兩邊都會呼叫一次。", "跑<b>層序</b>,看 queue 怎麼讓同一層的節點「一起排隊」。", "換成<b>鏈狀</b>的樹,看呼叫堆疊最深能到多深。"]),
  widget("w-tree", "二元樹走訪動畫"),
  sim("", "猜猜看:這一步會發生什麼?", "對完全二元樹做<b>後序</b>走訪(左 → 右 → 根),根節點 1 會在什麼時候印出來?",
      [("a1", "第一個"), ("a2", "正中間"), ("a3", "最後一個")]),
  '<h3 style="margin-top:26px">四種走訪,差在「什麼時候處理自己」</h3>',
  table("g3", ["走訪", "順序(完全二元樹的結果)", "常見用途"], [
    ["前序", "根 → 左 → 右:<code>1 2 4 5 3 6 7</code>", "複製一棵樹、把樹存成文字。"],
    ["中序", "左 → 根 → 右:<code>4 2 5 1 6 3 7</code>", "在二元搜尋樹(第 12 篇)上,會依大小排好的順序走過每個節點。"],
    ["後序", "左 → 右 → 根:<code>4 5 2 6 7 3 1</code>", "刪除整棵樹(先刪子,再刪自己)、算子樹的結果。"],
    ["層序", "一層一層:<code>1 2 3 4 5 6 7</code>", "找最近的節點、按層處理。用 queue,第 14 篇的廣度優先搜尋也是同一個想法。"],
  ]))

code = section("code", "完整程式:四種走訪",
  '<p class="sub" style="margin-bottom:14px">前、中、後序的程式碼<b>幾乎一模一樣</b>,只差印出那一行放在哪裡:遞迴呼叫左子樹之前(前序)、兩個呼叫之間(中序)、之後(後序)。層序則不用遞迴,改用 queue。</p>',
  cpp("tree_traverse"), out("tree_traverse", "執行結果(依序:前序、中序、後序、層序)"), compile_cmd(),
  '<div class="tip"><b class="l">最後的 destroy 是後序</b>釋放整棵樹時,要先 <code>delete</code> 左右子樹,最後才 <code>delete</code> 自己。如果先刪自己,就再也找不到子樹了(和第 4 篇鏈結串列的 <code>old</code> 一樣的道理)。這份程式用 <code>-fsanitize=address</code> 檢查過,沒有洩漏。</div>')

cost = section("cost", "複雜度小表",
  '<p class="sub" style="margin-bottom:14px">n 是節點數,h 是樹的高度。</p>',
  table("g3", ["走訪", "時間", "額外空間"], [
    ["前序 / 中序 / 後序", "O(n):每個節點恰好處理一次", "O(h):遞迴呼叫堆疊的深度"],
    ["層序", "O(n)", "O(w):queue 最多裝一層的節點(w 是最寬的一層)"],
    ["樹很平衡時", "—", "h 約等於 log n,很省"],
    ["樹退化成鏈時", "—", "h 等於 n,遞迴很深"],
  ]),
  '<p style="margin-top:14px">注意 h 的角色:<b>同樣 n 個節點,樹長得「矮胖」還是「又高又瘦」,會影響很多操作的速度</b>。下一篇的二元搜尋樹會看到這個差別。</p>')

gotchas = section("gotchas", "初學者最常卡住的三個地方",
  details("忘了先檢查 <code>nullptr</code>",
    '<p>遞迴走訪的第一件事一定是 <code>if (node == nullptr) return;</code>。少了它,走到葉子的子節點(<code>nullptr</code>)就會去讀 <code>node-&gt;val</code>,程式當掉。這就是遞迴的基底條件(第 7 篇)。</p>'),
  details("分不清前序、中序、後序",
    '<p>只看「<b>根在什麼時候被處理</b>」:根在最前面 → 前序;根在左右之間 → 中序;根在最後 → 後序。左一定在右前面,三種都是。</p>'),
  details("樹很深時遞迴會爆掉",
    '<p>鏈狀的樹有 n 層,遞迴走訪就是 n 層呼叫堆疊(第 7 篇)。節點數幾萬以上、又很不平衡時,可能 stack overflow。這是平衡樹很重要的原因之一。</p>'))

SIM = {
  "a1": "<b>不是。</b>後序是「左 → 右 → 根」,根要等左右子樹都走完才處理。回動畫選後序,看根 1 什麼時候被印。",
  "a2": "<b>不是。</b>根被夾在左右子樹中間的是<b>中序</b>(左 → 根 → 右)。後序要等左右兩邊都走完,根才輪到。",
  "a3": "<b>正確!</b>後序要先走完左子樹和右子樹,最後才處理根,所以 1 是最後一個:<code>4 5 2 6 7 3 1</code>。",
}
QUIZ = quiz_cfg([
  ("前序走訪的順序是?", ["根 → 左 → 右", "左 → 根 → 右", "左 → 右 → 根"], 0, "前序:根最先。"),
  ("層序走訪用什麼資料結構輔助?", ["queue", "stack", "雜湊表"], 0, "先進先出,讓同一層的節點依序排隊處理。"),
  ("要釋放(delete)整棵樹,應該用哪種順序?", ["後序:先刪左右子樹,最後才刪自己", "前序:先刪自己再刪子樹", "隨便"], 0, "先刪自己就找不到子樹了。"),
  ("二元樹的每個節點最多有幾個子節點?", ["2 個", "1 個", "任意多個"], 0, "「二元」就是最多左、右兩個。"),
  ("遞迴走訪一棵有 n 個節點的樹,時間是?", ["O(n)", "O(log n)", "O(n²)"], 0, "每個節點恰好被走訪一次。"),
])

ex = ('<h3 style="margin-top:30px">動手寫(兩題)</h3>'
  '<p class="sub" style="margin-bottom:12px">兩題都用「一棵樹 = 根 + 左子樹 + 右子樹」的遞迴想法。</p>'
  '<div class="panel"><h3>第 1 題:數節點個數</h3><p>完成 <code>countNodes</code>。輸出應該是 <code>3 0</code>。</p>' + cpp("tree_ex1_starter") +
  details("參考答案", "<p>基底條件:空的樹有 0 個節點。否則 = 1(自己)+ 左子樹節點數 + 右子樹節點數。</p>" + cpp("tree_ex1", "完整答案") + out("tree_ex1")) + '</div>'
  '<div class="panel" style="margin-top:14px"><h3>第 2 題:算樹的高度</h3><p>完成 <code>height</code>:最長路徑上的節點數。輸出應該是 <code>3 1 0</code>。</p>' + cpp("tree_ex2_starter") +
  details("參考答案", "<p>空的樹高度 0;否則高度 = 1 + 左右兩邊較高的那個。用 <code>std::max</code> 取較大值。時間 O(n)。</p>" + cpp("tree_ex2", "完整答案") + out("tree_ex2")) + '</div>')

practice = section("practice", "動手演練:確認你真的懂了", ex, QUIZ_HTML,
  checks(["我能說出根、葉、子樹、高度各是什麼。",
          "我知道二元樹的節點最多有左、右兩個子節點。",
          "我能分辨前序、中序、後序:看根在什麼時候被處理。",
          "我知道層序走訪要用 queue,一層一層處理。",
          "我知道走訪是 O(n),遞迴的空間取決於樹的高度。",
          "我知道刪除整棵樹要用後序(先子樹,再自己)。"], title="學完之後,對照這張清單"))

SCRIPT = r'''
var T = Algo.tree;
function render(f) {
  var h = "";
  if (f.stack) h += Algo.stackHtml(f);
  if (f.queue) h += Algo.cellsHtml({ rows: [{ label: "queue(左邊是最前面)", cells: f.queue.map(function (v) { return { v: v, cls: "" }; }), empty: 0 }] });
  h += Algo.treeHtml({ tree: f.tree });
  h += Algo.cellsHtml({ rows: [{ label: "輸出順序(已經印出的結果)", cells: f.out.map(function (v) { return { v: v, cls: "ok" }; }), empty: 0 }], chips: f.chips });
  return h;
}
function mode(m) { return function (v, c) { c.set("mode", m); c.run(); }; }
Algo.widget("w-tree", {
  form: [{ id: "tree", label: "樹", type: "select", value: "full", options: Object.keys(T.PRESETS).map(function (k) { return [k, T.PRESETS[k].name]; }) },
         { id: "mode", label: "走訪法", type: "select", value: "pre", options: Object.keys(T.NAMES).map(function (k) { return [k, T.NAMES[k]]; }) }],
  buttons: [{ label: "前序", run: mode("pre") }, { label: "中序", run: mode("in") }, { label: "後序", run: mode("post") }, { label: "層序", run: mode("level") }],
  init: function () { return null; },
  idle: function () { var f = T.idle("full"); f.msg = "選一棵樹與走訪法,按「執行」。這棵是完全二元樹,節點上的數字是編號。"; return f; },
  make: function (v) { return T.run(v.mode, v.tree); },
  render: render, code: T.CODE_TREE, code_cap: "四種走訪(亮起來的行 = 目前執行到的地方)"
});
'''
SPEC = dict(
  file="datastruct-tree-guide.html", dir="datastruct", eyebrow_prefix=EYEBROW, foot=FOOT,
  modules=["cells", "tree", "alg_tree"], script=SCRIPT,
  title="二元樹與走訪:前序、中序、後序與層序",
  eyebrow="第 11 篇 · 二元樹與走訪",
  h1="同一棵樹,換個「處理自己」的時機,走訪順序就不同",
  sub="二元樹的每個節點最多有左右兩個子節點。這一篇用動畫看前序、中序、後序(遞迴)與層序(queue)如何走過每個節點。",
  tldr="一棵樹 = 根 + 左子樹 + 右子樹,所以走訪用遞迴最自然。前序、中序、後序只差「印出自己」那一行的位置;層序改用 queue 一層層走。走訪都是 <code>O(n)</code>。<br><small>先備:第 4 篇節點與指標、第 5 篇 queue、第 7 篇遞迴。預估 15 分鐘。難度:進階。</small>",
  toc=[("what", "直覺:家族圖"), ("play", "四種走訪"), ("code", "完整程式"), ("cost", "複雜度小表"), ("gotchas", "常見錯誤"), ("practice", "動手寫與測驗")],
  body="\n\n".join([what, play, code, cost, gotchas, practice]),
  config=dict(sim=SIM, quiz=QUIZ),
  prev=("datastruct-hash-guide.html", "雜湊表"),
  next=("datastruct-bst-guide.html", "二元搜尋樹"),
)
