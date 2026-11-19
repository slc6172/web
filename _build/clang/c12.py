from ch import *
STP = {}

def C(id, names, v, t="int", a="", p=None):
    d = dict(id=id, names=names if isinstance(names, list) else [names], v=str(v), t=t, a=a)
    if p: d["p"] = p
    return d

# a1:指標(行號 0 起算)
X = lambda v: C("x", "x", v, a="0x1000")
P = C("p", "p", "0x1000", "int*", "0x1008", "x")
T1 = [
 dict(l=4, m=[X(10)], n="宣告 x = 10。x 是一個格子,住在某個位址(這裡示意為 0x1000)。"),
 dict(l=5, m=[X(10), P], n="int* p = &x:&x 是「x 的位址」。p 是一個指標,它裡面存的就是這個位址,所以畫一條箭頭指向 x。"),
 dict(l=6, m=[X(10), P], o="10\n", n="*p:順著箭頭,取出 p 指向的那個格子的值:10。"),
 dict(l=7, m=[X(20), P], n="*p = 20:順著箭頭,改到 x 本人。x 變成 20。"),
 dict(l=8, m=[X(20), P], o="20\n", n="直接印 x,也是 20:因為 *p 和 x 就是同一個格子。"),
 dict(l=9, m=[X(20), P], o="1\n", n="p == &x:p 裡存的位址就是 x 的位址,所以成立,印出 1。"),
]
# a2:參考
T2 = [
 dict(l=4, m=[C("x", "x", 10, a="0x1000")], n="宣告 x = 10。"),
 dict(l=5, m=[C("x", ["x", "r"], 10, a="0x1000")], n="int& r = x:r 是 x 的「別名」。沒有新的格子,只是同一個格子多了一個名字。"),
 dict(l=6, m=[C("x", ["x", "r"], 30, a="0x1000")], n="r = 30:改 r,就是改 x(它們是同一個格子)。"),
 dict(l=7, m=[C("x", ["x", "r"], 30, a="0x1000")], o="30\n", n="印 x:30。"),
 dict(l=8, m=[C("x", ["x", "r"], 30, a="0x1000")], o="30\n", n="印 r:也是 30。"),
]
# a3:傳參考
def xy(x, y, alias=False, temp=None):
    cs = [C("x", ["x", "a"] if alias else ["x"], x, a="0x1000"), C("y", ["y", "b"] if alias else ["y"], y, a="0x1004")]
    if temp is not None: cs.append(C("t", ["temp"], temp, a="0x0FF0"))
    return cs
T3 = [
 dict(l=10, m=xy(3, 5), n="main 裡有兩個變數:x = 3、y = 5。"),
 dict(l=11, m=xy(3, 5, True), n="呼叫 swapInt(x, y):參數是參考(int&),所以 a 就是 x 的別名、b 就是 y 的別名。沒有複製!"),
 dict(l=4, m=xy(3, 5, True, 3), n="int temp = a:temp 是函式自己的新格子,先把 a(也就是 x)的值 3 存起來。"),
 dict(l=5, m=xy(5, 5, True, 3), n="a = b:把 b 的值 5 放進 a。因為 a 就是 x,所以 x 變成 5。"),
 dict(l=6, m=xy(5, 3, True, 3), n="b = temp:把 3 放進 b,y 變成 3。"),
 dict(l=7, m=xy(5, 3), n="函式結束:temp 消失,a 與 b 這兩個別名也不再使用。x 與 y 已經被換過來了。"),
 dict(l=12, m=xy(5, 3), o="5 3\n", n="印出 x 和 y:5 3。和第 11 篇的 addOne 對照:傳參考就能改到外面。"),
]
# a5:指標與陣列
A = lambda v0, v1, v2: [C("a0", "a[0]", v0, a="0x2000"), C("a1", "a[1]", v1, a="0x2004"), C("a2", "a[2]", v2, a="0x2008")]
def pa(t): return C("p", "p", {"a0": "0x2000", "a1": "0x2004"}[t], "int*", "0x2010", t)
T5 = [
 dict(l=4, m=A(10, 20, 30), n="陣列 a 是三個相鄰的格子,位址每次差 4(一個 int 的大小)。"),
 dict(l=5, m=A(10, 20, 30) + [pa("a0")], n="int* p = a:陣列的名字在這裡代表「第一個元素的位址」,所以 p 指向 a[0]。"),
 dict(l=6, m=A(10, 20, 30) + [pa("a0")], o="10\n", n="*p 是 a[0] 的值:10。"),
 dict(l=7, m=A(10, 20, 30) + [pa("a1")], n="p = p + 1:指標往後移「一個元素」(不是一個位元組),現在指向 a[1]。"),
 dict(l=8, m=A(10, 20, 30) + [pa("a1")], o="20\n", n="*p 是 a[1] 的值:20。"),
 dict(l=9, m=A(10, 20, 30) + [pa("a1")], o="30\n", n="p[1] 等於 *(p + 1):從 p 現在的位置,再往後一格,也就是 a[2]:30。"),
 dict(l=10, m=A(10, 20, 30) + [pa("a1")], o="30\n", n="直接印 a[2],也是 30。陣列和指標關係很近:a[i] 其實就是 *(a + i)。"),
]

what = section("what", "兩個「間接」的工具:參考與指標",
  '<div class="panel"><h3>用「房子與門牌」來想</h3>'
  '<p>每個變數都是記憶體裡的一個「房子」(格子),每間房子有自己的<b>位址</b>(門牌)。</p>'
  '<p><b>參考</b>是房子的<b>另一個名字</b>(別名):叫哪個名字,都是進同一間房子。<b>指標</b>是一張<b>寫著門牌號碼的紙條</b>:你要拿著紙條,「順著」去找那間房子。</p>'
  '<p style="margin-bottom:0">兩者的目的都一樣:<b>不複製,直接讓別人使用原本的那個格子</b>。這一篇的動畫會帶你一格一格地看。</p></div>',
  '<h3 style="margin-top:26px">七個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["位址", "變數在記憶體裡的「門牌號碼」。"],
    ["取址 <code>&amp;x</code>", "取得 x 的位址。"],
    ["指標 <code>int* p</code>", "一個專門存「某個 int 的位址」的變數。"],
    ["解參考 <code>*p</code>", "順著指標去找它指的格子,存取那裡的值。"],
    ["參考 <code>int&amp; r</code>", "某個變數的別名,宣告時就要綁定一個對象,之後不能改綁別人。"],
    ["<code>nullptr</code>", "「不指向任何東西」的指標。不能對它解參考。"],
    ["<code>const</code> 參考", "只能看、不能改的參考。"],
  ]))

mapsec = section("map", "全貌:&amp; 與 * 在不同位置有不同意思",
  '<p class="sub" style="margin-bottom:14px">這是最容易搞混的地方。看<b>它出現在宣告裡,還是運算式裡</b>。</p>',
  table("g3b", ["寫法", "出現的位置", "意思"], [
    ["<code>int&amp; r = x;</code>", "宣告", "r 是 x 的<b>參考</b>(別名)。"],
    ["<code>&amp;x</code>", "運算式", "取 x 的<b>位址</b>。"],
    ["<code>int* p = &amp;x;</code>", "宣告", "p 是<b>指標</b>,存 x 的位址。"],
    ["<code>*p</code>", "運算式", "<b>解參考</b>:p 指向的那個格子。"],
    ["<code>a * b</code>", "兩個運算元之間", "乘法。"],
  ]),
  tip("口訣:<b>宣告時的 <code>&amp;</code> 是參考,運算式裡的 <code>&amp;</code> 是取位址;宣告時的 <code>*</code> 是指標,運算式裡的 <code>*</code> 是「順著去找」</b>。"))

steps_ = section("steps", "照著做:七個步驟", steps(
  step(1, "指標:存著位址的變數",
       "按「下一步」,看記憶體格子與箭頭。<b>指標是虛線格子</b>,它裡面的值是一個位址,箭頭指向它指的格子。",
       stepper(STP, "ptr", "p12/a1", T1),
       details("要自己試的話:完整程式碼(可複製)", code("p12/a1") + term("p12/a1")),
       see("<b><code>*p</code> 與 <code>x</code> 是同一個格子</b>:改 <code>*p</code>,x 就跟著變。")),
  step(2, "參考:別名",
       "參考不是新的格子,只是同一個格子的<b>第二個名字</b>(看格子上同時有 <code>x / r</code>)。",
       stepper(STP, "ref", "p12/a2", T2),
       details("要自己試的話:完整程式碼(可複製)", code("p12/a2") + term("p12/a2"))),
  step(3, "傳參考:讓函式改到外面的變數",
       "還記得第 11 篇「傳值」不能改到外面嗎?把參數寫成 <code>int&amp;</code>,函式裡的 <code>a</code>、<code>b</code> 就成了外面 <code>x</code>、<code>y</code> 的別名。",
       stepper(STP, "swap", "p12/a3", T3),
       details("要自己試的話:完整程式碼(可複製)", code("p12/a3") + term("p12/a3")),
       tip("兩個變數互換,需要借助第三個格子 <code>temp</code>,這個做法在第 3 篇練習 2 學過。現在包成函式,而且能真的換到外面了。")),
  step(4, "const 參考:只看、不複製",
       "字串或 <code>vector</code> 很大時,傳值要複製一整份,很浪費。<b>傳 <code>const</code> 參考</b>:不複製,而且保證不會改到它。",
       code("p12/a4"), term("p12/a4"),
       "<p>想在 <code>const</code> 參考裡修改,編譯器會擋下來:</p>",
       code("p12/e1.err"), errterm("p12/e1.err"),
       tip("經驗法則:<b>函式不需要修改的大型參數,用 <code>const 型態&amp;</code>;需要修改外面的變數,用 <code>型態&amp;</code>;小的值(<code>int</code>、<code>double</code>)直接傳值就好</b>。")),
  step(5, "指標與陣列",
       "陣列是相鄰的格子,陣列名字代表第一個格子的位址。看指標怎麼在陣列上「走」。",
       stepper(STP, "arr", "p12/a5", T5),
       details("要自己試的話:完整程式碼(可複製)", code("p12/a5") + term("p12/a5"))),
  step(6, "nullptr:還沒有對象的指標",
       "指標在還沒有指向任何東西時,要設成 <code>nullptr</code>,使用前先檢查。",
       code("p12/a6"), term("p12/a6"),
       warn("對 <code>nullptr</code> 或沒初始化的指標使用 <code>*p</code>,程式會當掉(或更糟:默默改到別人的資料)。<b>宣告指標就要立刻給值</b>。", "最危險的錯")),
  step(7, "指標當參數:認得就好",
       "舊程式或 C 語言裡,常用「傳指標」達成和傳參考一樣的事。呼叫時要加 <code>&amp;</code> 取位址。新寫的程式優先用參考,比較簡單、也比較安全。",
       code("p12/a7"), term("p12/a7"))
))

stuck = section("stuck", "初學者最常卡住的四個地方",
  details("<code>&amp;</code> 和 <code>*</code> 到底什麼時候是什麼意思",
          "<p>看上面「全貌」的表:<b>在宣告(型態後面)是參考與指標,在運算式裡是取位址與解參考</b>。一開始看不懂很正常,多看幾次動畫就會慢慢有感覺。</p>"),
  details("函式回傳區域變數的參考或指標",
          "<p>區域變數在函式結束時就消失了。回傳指向它的參考或指標,等於指著一間已經拆掉的房子(懸空),使用時結果不可預期。目前的原則:<b>不要回傳區域變數的參考或指標</b>。</p>"),
  details("指標宣告了卻沒有給值",
          "<p><code>int* p;</code> 裡面是不確定的亂數位址。用 <code>*p</code> 就是去存取一個不屬於你的地方。要嘛馬上指向某個變數,要嘛設成 <code>nullptr</code>。</p>"),
  details("<code>int* a, b;</code> 結果 b 不是指標",
          "<p>只有 <code>a</code> 是指標,<code>b</code> 是普通的 <code>int</code>。每個變數都要自己的 <code>*</code>:<code>int *a, *b;</code>。初學時建議一行只宣告一個變數。</p>"))

QUIZ = quiz_cfg([
  ("<code>int x = 5; int* p = &amp;x; *p = 9;</code> 之後,<code>x</code> 是?", ["9", "5", "p 的位址"], 0, "*p 就是 x 這個格子,改 *p 就是改 x。"),
  ("<code>int&amp; r = x;</code> 中的 <code>r</code> 是?", ["x 的別名", "x 的複製", "x 的位址"], 0, "參考不是新的格子,只是同一個格子的另一個名字。"),
  ("想讓函式修改呼叫端的整數變數,最簡單的寫法是?", ["參數寫成 int&", "參數寫成 const int", "把函式改成 void"], 0, "傳參考讓函式拿到的是原變數的別名,不是影本。"),
  ("對 <code>nullptr</code> 解參考(<code>*p</code>)會?", ["讓程式當掉或產生未定義行為", "得到 0", "編譯失敗"], 0, "空指標不指向任何格子,不能使用。使用前先檢查。"),
  ("傳一個很大的 <code>vector</code> 給只需要「讀取」它的函式,最好用?", ["const vector&lt;int&gt;&amp;", "vector&lt;int&gt;(傳值)", "int*"], 0, "const 參考不複製,又保證不會改到。"),
])

practice = section("practice", "動手演練:參考與指標",
  '<p class="sub" style="margin-bottom:18px">每題先自己寫,再展開看參考解答。</p>',
  exercise(1, "交換兩個字串", "把 <code>swapInt</code> 改成 <code>swapStr</code>,交換兩個 <code>string</code>。印出交換後的結果。", "p12/x1"),
  exercise(2, "指標版與參考版", "寫兩個函式:<code>incByPtr(int* p)</code> 與 <code>incByRef(int&amp; r)</code>,都讓變數加 1。對 <code>x = 5</code> 各呼叫一次,印出 6 與 7。", "p12/x2",
           note="比較兩種呼叫方式:指標版要寫 <code>incByPtr(&amp;x)</code>,參考版直接 <code>incByRef(x)</code>。"),
  exercise(3, "一次傳回兩個結果", "函式只能 <code>return</code> 一個值,但可以用參考參數「傳回」更多。寫 <code>minMax(v, mn, mx)</code>,找出 <code>{7, 3, 9, 1, 5}</code> 的最小與最大。", "p12/x3",
           note="<code>v</code> 用 <code>const vector&lt;int&gt;&amp;</code>(只看不改),<code>mn</code> 與 <code>mx</code> 用 <code>int&amp;</code>(要把結果寫回去)。"),
  QUIZ_HTML,
  chk(["我知道每個變數都有位址,<code>&amp;x</code> 是取位址。", "我知道指標存的是位址,<code>*p</code> 是順著去找那個格子。",
       "我知道參考是別名,不是新的格子。", "我能用傳參考寫出 <code>swap</code>。", "我知道大型參數用 <code>const</code> 參考傳。",
       "我知道指標要初始化、不用時設 <code>nullptr</code>,而且不能對它解參考。"]),
  links([("https://en.cppreference.com/cpp/language/pointer", "cppreference:指標", "cppreference.com"),
         ("https://en.cppreference.com/cpp/language/reference", "cppreference:參考", "cppreference.com")]))

SPEC = spec(
  file="clang-ref-pointer-guide.html",
  title="參考與指標:指標是存著位址的變數,參考是別人的別名",
  eyebrow="第 12 篇 · 參考與指標",
  h1="指標是存著別人位址的變數,參考是別人的別名",
  sub="用記憶體格子和箭頭的動畫,一步一步看懂位址、指標、參考與傳參考,也看清楚為什麼傳參考能讓函式改到外面的變數。",
  tldr="每個變數都有<strong>位址</strong>。<strong>參考</strong>是同一個格子的別名;<strong>指標</strong>是存著位址的變數,<code>*p</code> 順著去找那個格子。想讓函式改到外面的變數,參數用 <code>int&amp;</code>;大型資料只看不改,用 <code>const</code> 參考。指標要初始化,不能對 <code>nullptr</code> 解參考。",
  toc=[("what", "兩個間接工具"), ("map", "& 與 * 的意思"), ("steps", "七個步驟"), ("stuck", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, mapsec, steps_, stuck, practice]),
  config=dict(stepper=STP, quiz=QUIZ),
  **nav(12),
)
