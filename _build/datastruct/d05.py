from dh import *

what = section("what", "堆疊是一疊盤子,佇列是排隊買票",
  '<div class="panel"><h3>兩個生活比喻</h3>'
  '<p><strong>堆疊(stack)</strong>像一疊盤子:新盤子只能放在最上面,要拿也只能拿最上面那個。<b>最後放進去的,最先拿出來</b>(後進先出,LIFO)。</p>'
  '<p style="margin-bottom:0"><strong>佇列(queue)</strong>像排隊買票:新來的人排到隊伍最後面,服務永遠從最前面開始。<b>最先排隊的,最先離開</b>(先進先出,FIFO)。</p></div>',
  '<h3 style="margin-top:26px">名詞對照</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["<code>push</code>", "放進去。stack 放在頂端;queue 排到最後面。"],
    ["<code>pop</code>", "拿出來。stack 拿頂端;queue 拿最前面。"],
    ["<code>top</code>(stack)", "只看頂端是誰,不拿走。"],
    ["<code>front</code> / <code>back</code>(queue)", "最前面的人 / 最後面的人。"],
    ["LIFO / FIFO", "Last In First Out(後進先出)/ First In First Out(先進先出)。"],
  ]),
  '<div class="tip"><b class="l">它們的重點是「限制」</b>stack 和 queue 都只讓你碰「一端」或「兩端」,不能隨便存取中間。這個限制讓用法很清楚,操作也都很快(O(1))。')

stack = section("stack", "動手玩:堆疊 push 與 pop",
  '<p class="sub" style="margin-bottom:14px">這個 <code>Stack</code> 是用上一篇學過的 <code>vector</code> 包起來的:push 就是 <code>push_back</code>,pop 就是取尾端再 <code>pop_back</code>。尾端就是頂。</p>',
  try_list(["依序 push 1、2、3(把數值改成 1、2、3,各按一次「push」)。", "按一次「pop」:取出的是哪一個?", "再 pop 兩次,看看順序,然後試著對空 stack 再 pop。"]),
  widget("w-stack", "堆疊動畫"),
  sim("", "猜猜看:這一步會發生什麼?", "依序 push 1、2、3,然後 pop 一次,取出來的是?",
      [("a1", "1"), ("a2", "2"), ("a3", "3")]),
  cpp("sq_stack"), out("sq_stack", "執行結果(後進先出)"))

queue = section("queue", "動手玩:佇列 push 與 pop",
  '<p class="sub" style="margin-bottom:14px">佇列一樣用 <code>vector</code> 包,但多一個 <code>head</code> 記著「最前面是第幾格」。pop 不搬資料,只是把 head 往後移。(這個簡化版不會回收離開的格子;真正的 <code>std::queue</code> 會。)</p>',
  try_list(["依序 push 1、2、3,看 front 與 back 標籤。", "pop 一次:這次取出的是哪一個?和 stack 比較。"]),
  widget("w-queue", "佇列動畫"),
  cpp("sq_queue"), out("sq_queue", "執行結果(先進先出)"),
  '<div class="see"><b class="l">你會看到</b>同樣依序放進 1、2、3:stack 取出 <code>3 2 1</code>,queue 取出 <code>1 2 3</code>。')

stl = section("stl", "實務上:std::stack 與 std::queue",
  '<p class="sub" style="margin-bottom:14px">標準函式庫已經幫你寫好了,直接 <code>#include &lt;stack&gt;</code>、<code>&lt;queue&gt;</code> 就能用。</p>',
  cpp("sq_stl"), out("sq_stl"),
  '<div class="tip"><b class="l">注意:pop() 不會回傳值</b>在 <code>std::stack</code> 與 <code>std::queue</code> 裡,<code>pop()</code> 只負責移除、回傳 <code>void</code>。要先用 <code>top()</code>(或 <code>front()</code>)讀出來,再 <code>pop()</code>。我們自己寫的版本為了簡單,才讓 pop 回傳值。</div>')

bracket = section("bracket", "實戰:用 stack 檢查括號配對",
  '<p class="sub" style="margin-bottom:14px">寫程式時,<code>( [ { } ] )</code> 必須成對、而且不能交叉。想想看:<b>最後打開的括號,一定要最先關上</b>,這正是「後進先出」。</p>',
  try_list(["按「配對正確」預設,看左括號進 stack、右括號配對消掉。", "按「交叉」預設:<code>([)]</code> 在哪一步失敗?", "自己輸入一個字串試試。"]),
  widget("w-bracket", "括號配對動畫"),
  cpp("sq_balance"), out("sq_balance"),
  '<p>流程只有三條:左括號就 <code>push</code>;右括號就看頂端能不能配、配得上就 <code>pop</code>;走完時 stack 要是空的。每個字元只處理一次,時間 O(n)。</p>')

cost = section("cost", "複雜度小表",
  table("g3", ["操作", "時間", "說明"], [
    ["stack:<code>push</code> / <code>pop</code> / <code>top</code>", "O(1)", "只碰頂端,不搬動別的元素。"],
    ["queue:<code>push</code> / <code>pop</code> / <code>front</code>", "O(1)", "只碰兩端。"],
    ["找中間的某個元素", "不支援", "要找就得一個個 pop 出來,這不是它們的用途。"],
    ["括號配對", "O(n)", "每個字元 push 或 pop 一次。"],
  ]),
  '<p style="margin-top:14px"><b>空間:</b>括號配對最壞要把所有左括號放進 stack,所以是 O(n)。</p>')

gotchas = section("gotchas", "初學者最常卡住的三個地方",
  details("對空的 stack 或 queue 取 <code>top()</code> / <code>front()</code> / <code>pop()</code>",
    '<p>這是未定義行為,可能當掉、也可能讀到亂值。習慣先檢查 <code>empty()</code>。</p>' + cpp("sq_empty_pop") + out("sq_empty_pop")),
  details("<code>int x = st.pop();</code> 編不過",
    '<p>因為 <code>std::stack::pop()</code> 回傳 <code>void</code>。正確寫法是 <code>int x = st.top(); st.pop();</code>,兩個步驟。</p>'),
  details("用 vector 當 queue,每次 <code>erase(v.begin())</code> 會很慢",
    '<p>從 vector 最前面刪除要把後面全部往前搬(上一篇的 O(n))。要用 queue 就用 <code>std::queue</code>,或像本篇用 <code>head</code> 索引記錄前端位置。</p>'))

SIM = {
  "a1": "<b>不是。</b>1 是最先放進去的,在最底下。stack 取的是最後放進去的。",
  "a2": "<b>不是。</b>2 在中間,不是頂端。pop 只能取頂端。",
  "a3": "<b>正確!</b>3 最後放進去,在頂端,所以最先出來(後進先出)。",
}
QUIZ = quiz_cfg([
  ("依序 push 1、2、3,再 pop 一次,<b>stack</b> 取出的是?", ["1", "2", "3"], 2, "stack 是後進先出,最後放進去的 3 在頂端。"),
  ("依序 push 1、2、3,再 pop 一次,<b>queue</b> 取出的是?", ["1", "2", "3"], 0, "queue 是先進先出,最先放進去的 1 在最前面。"),
  ("括號配對為什麼適合用 stack?", ["最後打開的括號要最先關上(後進先出)", "因為 stack 比較快", "因為字串要先反過來"], 0, "配對的方向和「後進先出」剛好一致。"),
  ("<code>std::stack</code> 的 <code>pop()</code> 會?", ["移除頂端,但不回傳值", "移除並回傳頂端", "只回傳頂端,不移除"], 0, "要先 top() 讀,再 pop() 移除。"),
  ("字串 <code>([)]</code> 括號配對嗎?", ["不配對:遇到 ) 時頂端是 [", "配對", "不配對:因為括號數量不同"], 0, "括號數量相同,但交叉了:) 出現時頂端是 [,配不起來。"),
])

ex = ('<h3 style="margin-top:30px">動手寫(兩題)</h3>'
  '<div class="panel"><h3>第 1 題:用 stack 反轉字串</h3><p>完成 <code>reverseString</code>。輸出應該是 <code>cba kcats</code>。</p>' + cpp("sq_ex1_starter") +
  details("參考答案", "<p>先全部 push,再一個個取頂端接起來。後進先出,所以順序剛好反過來。</p>" + cpp("sq_ex1", "完整答案") + out("sq_ex1")) + '</div>'
  '<div class="panel" style="margin-top:14px"><h3>第 2 題:只有一種括號時,不用 stack</h3><p>完成 <code>isBalancedParen</code>。輸出應該是 <code>100</code>(依序是三個字串的結果)。想想:為什麼多種括號時就不行了?</p>' + cpp("sq_ex2_starter") +
  details("參考答案", "<p>只有一種括號時,只要記得「目前有幾個沒關的左括號」,一個計數器就夠。多種括號時,還得記得<b>是哪一種</b>、順序是什麼,所以需要 stack。</p>" + cpp("sq_ex2", "完整答案") + out("sq_ex2")) + '</div>')

practice = section("practice", "動手演練:確認你真的懂了", ex, QUIZ_HTML,
  checks(["我能說出 stack 是後進先出、queue 是先進先出,並各舉一個生活例子。",
          "我知道 push、pop、top、front、back 各做什麼。",
          "我知道它們的操作都是 O(1)。",
          "我知道為什麼括號配對要用 stack。",
          "我知道 <code>std::stack::pop()</code> 不回傳值,要先 <code>top()</code>。",
          "我知道對空容器取頂端或 pop 是危險的,要先檢查 <code>empty()</code>。"], title="學完之後,對照這張清單"),
  resources([
    ("https://en.cppreference.com/cpp/container/stack", "std::stack", "cppreference · std::stack"),
    ("https://en.cppreference.com/cpp/container/queue", "std::queue", "cppreference · std::queue"),
  ], title="cppreference 參考頁面"))

SCRIPT = r'''
var S = Algo.sq, R = function (f) { return Algo.cellsHtml(f); };
Algo.widget("w-stack", {
  form: [{ id: "op", label: "操作", type: "select", value: "push", options: [["push", "push 放進去"], ["pop", "pop 取出頂端"]] },
         { id: "v", label: "數值", type: "number", min: 0, max: 99, value: 1, showIf: { op: "push" } }],
  buttons: [{ label: "push", run: function (v, c) { c.set("op", "push"); c.run(); } }, { label: "pop", run: function (v, c) { c.set("op", "pop"); c.run(); } }],
  init: function () { return []; },
  idle: function (b) { return S.stackFrame(b, undefined, b.length ? "stack 現在有 " + b.length + " 個元素。" : "stack 是空的。選 push 放一個數字進去,按「執行」。"); },
  make: function (v, base) { return v.op === "push" ? S.stackPush(base, v.v) : S.stackPop(base); },
  render: R, code: S.CODE_STACK, code_cap: "Stack(亮起來的行 = 目前執行到的地方)"
});
Algo.widget("w-queue", {
  form: [{ id: "op", label: "操作", type: "select", value: "push", options: [["push", "push 排到最後"], ["pop", "pop 最前面離開"]] },
         { id: "v", label: "數值", type: "number", min: 0, max: 99, value: 1, showIf: { op: "push" } }],
  buttons: [{ label: "push", run: function (v, c) { c.set("op", "push"); c.run(); } }, { label: "pop", run: function (v, c) { c.set("op", "pop"); c.run(); } }],
  init: S.queueInit,
  idle: function (b) { return S.queueFrame(b, undefined, b.data.length - b.head ? "隊伍現在有 " + (b.data.length - b.head) + " 人。" : "隊伍是空的。選 push 讓一個人排進來,按「執行」。"); },
  make: function (v, base) { return v.op === "push" ? S.queuePush(base, v.v) : S.queuePop(base); },
  render: R, code: S.CODE_QUEUE, code_cap: "Queue(亮起來的行 = 目前執行到的地方)"
});
function setStr(s) { return function (v, c) { c.set("s", s); c.run(); }; }
Algo.widget("w-bracket", {
  form: [{ id: "s", label: "字串(1–14 字元)", type: "text", value: "{[()]}" }],
  buttons: [{ label: "配對正確", run: setStr("{[()]}") }, { label: "交叉", run: setStr("([)]") }, { label: "少一個", run: setStr("((())") }, { label: "多一個", run: setStr("())") }],
  init: function () { return null; },
  idle: function () { return { rows: [{ label: "字串", cells: [], empty: 0 }], msg: "輸入括號字串,或按下面的預設按鈕。" }; },
  make: function (v) { return S.balance(v.s); },
  render: R, code: S.CODE_BRACKET, code_cap: "isBalanced(亮起來的行 = 目前執行到的地方)"
});
'''
SPEC = dict(
  file="datastruct-stackqueue-guide.html", dir="datastruct", eyebrow_prefix=EYEBROW, foot=FOOT,
  modules=["cells", "alg_sq"], script=SCRIPT,
  title="堆疊與佇列:後進先出與先進先出",
  eyebrow="第 5 篇 · 堆疊與佇列",
  h1="堆疊後進先出,佇列先進先出,兩端的操作都是 O(1)",
  sub="堆疊像一疊盤子,佇列像排隊買票。這一篇用動畫看 push 與 pop,再用 stack 解決經典的括號配對問題。",
  tldr="<code>stack</code> 只碰頂端(後進先出),<code>queue</code> 只碰兩端(先進先出),<code>push</code>/<code>pop</code> 都是 <code>O(1)</code>。括號配對:左括號 push,右括號看頂端配得上就 pop,最後 stack 要是空的。<br><small>先備:第 3 篇的 vector。預估 12 分鐘。難度:基礎。</small>",
  toc=[("what", "直覺:盤子與排隊"), ("stack", "堆疊"), ("queue", "佇列"), ("stl", "std::stack/queue"), ("bracket", "括號配對"), ("cost", "複雜度小表"), ("gotchas", "常見錯誤"), ("practice", "動手寫與測驗")],
  body="\n\n".join([what, stack, queue, stl, bracket, cost, gotchas, practice]),
  config=dict(sim=SIM, quiz=QUIZ),
  prev=("datastruct-linkedlist-guide.html", "鏈結串列"),
  next=("datastruct-search-guide.html", "搜尋:線性與二分"),
)
