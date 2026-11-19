from ch import *
STP = {}

def H(id, v, a, **kw): return dict(id=id, names=["(無名)"], v=str(v), t="int", a=a, r="heap", **kw)
def S(v, **kw): return dict(id="p", names=["p"], v=v, t="int*", a="0x1000", **kw)

T1 = [
 dict(l=4, m=[S("0x9000", p="h1"), H("h1", 42, "0x9000")], n="new int(42):向系統在 heap 要一塊空間放 42,並把「位址」交給 p。heap 上的東西沒有名字,只能靠指標找到它。"),
 dict(l=5, m=[S("0x9000", p="h1"), H("h1", 42, "0x9000")], o="42\n", n="*p:順著箭頭取值,42。"),
 dict(l=6, m=[S("0x9000", p="h1"), H("h1", 7, "0x9000")], n="*p = 7:改的是 heap 上那一塊。"),
 dict(l=7, m=[S("0x9000", p="h1"), H("h1", 7, "0x9000")], o="7\n", n="印出 7。"),
 dict(l=8, m=[S("0x9000", p="h1", dangling=True), H("h1", 7, "0x9000", free=True)], n="delete p:把那塊空間還給系統。但 p 裡的位址還在——它變成「懸空指標」,指著一塊已經不屬於你的地方,之後絕對不能再用 *p。"),
 dict(l=9, m=[S("nullptr")], n="p = nullptr:把用不到的指標設成空,避免誤用。這一輪的借與還完整結束。"),
]
T2 = [
 dict(l=4, m=[S("0x9000", p="h1"), H("h1", 1, "0x9000")], n="new int(1):heap 上有了第一塊,p 指向它。"),
 dict(l=5, m=[S("0x9000", p="h1"), H("h1", 1, "0x9000")], o="1\n", n="印出 1。"),
 dict(l=6, m=[S("0x9100", p="h2"), H("h1", 1, "0x9000", leak=True), H("h2", 2, "0x9100")], n="又 new 了一塊,p 改指向新的。舊的那塊(1)現在沒有任何指標記得它的位址——沒有人能再歸還它。這就是記憶體洩漏。"),
 dict(l=7, m=[S("0x9100", p="h2"), H("h1", 1, "0x9000", leak=True), H("h2", 2, "0x9100")], o="2\n", n="印出 2。"),
 dict(l=8, m=[S("0x9100", p="h2", dangling=True), H("h1", 1, "0x9000", leak=True), H("h2", 2, "0x9100", free=True)], n="delete p 只歸還了 p 現在指的那塊(2)。h1 永遠還不回去了,一直佔著空間,直到程式結束。"),
]

what = section("what", "借了就要還:heap 與智慧指標",
  '<div class="panel"><h3>用「租倉庫」來想</h3>'
  '<p>目前你宣告的變數,都放在 <b>stack</b>:函式一結束,系統就<b>自動收回</b>,像便利貼用完就撕掉。但有時資料要活得比函式更久,或大小要到執行時才知道,就需要向系統在 <b>heap</b> 要空間:<code>new</code> 像是<b>租一個倉庫</b>,用完要用 <code>delete</code> <b>退租</b>。</p>'
  '<p>人會忘記退租(記憶體洩漏),也會退租後還拿著鑰匙亂開(懸空指標)。所以現代 C++ 的做法是:<b>交給智慧指標</b>,它在離開範圍時<b>自動退租</b>。</p>'
  '<p style="margin-bottom:0" class="foot"><b>進階選讀</b>:不影響前面的主線。最重要的結論只有一句:<b>能不用 <code>new</code> 就不用,要用就用智慧指標。</b></p></div>',
  '<h3 style="margin-top:26px">七個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["stack", "區域變數住的地方,函式結束自動收回。"],
    ["heap", "手動要、手動還的空間,用 <code>new</code> 取得。"],
    ["<code>new</code> / <code>delete</code>", "取得與歸還 heap 空間。<code>new</code> 回傳位址,要用指標接住。"],
    ["記憶體洩漏", "要了空間卻沒歸還,而且再也沒有指標能找到它。"],
    ["懸空指標", "指著已經歸還(或已經消失)的位置的指標。"],
    ["<code>unique_ptr</code>", "智慧指標:<b>獨佔</b>一個物件,離開範圍時自動歸還,不能複製。"],
    ["<code>shared_ptr</code>", "智慧指標:可以多個擁有者<b>共享</b>,最後一個離開時才歸還。"],
  ]))

steps_ = section("steps", "照著做:六個步驟", steps(
  step(1, "new 與 delete:借與還",
       "按「下一步」,看 stack 與 heap 兩個區域。<b>指標在 stack,它指向的東西在 heap</b>。注意 <code>delete</code> 之後那條虛線箭頭。",
       stepper(STP, "newdel", "p17/a1", T1),
       details("要自己試的話:完整程式碼(可複製)", code("p17/a1") + term("p17/a1")),
       warn("<code>delete</code> 之後 <code>p</code> 還握著舊的位址(懸空指標)。習慣上緊接著 <code>p = nullptr;</code>。對已經 <code>delete</code> 的指標再用 <code>*p</code> 或再 <code>delete</code> 一次,都會出大事。", "重要")),
  step(2, "記憶體洩漏長什麼樣",
       "只要 <code>new</code> 出來的東西,在你還沒 <code>delete</code> 之前就失去了所有指標,它就洩漏了。看下面哪一塊變成紅色:",
       stepper(STP, "leak", "p17/a2", T2),
       details("要自己試的話:完整程式碼(可複製)", code("p17/a2") + term("p17/a2")),
       see("洩漏不會讓程式立刻出錯,輸出看起來一切正常。但長時間執行的程式(伺服器、遊戲)會越吃越多記憶體,最後用光。")),
  step(3, "unique_ptr:自動歸還",
       "<code>make_unique</code> 幫你 <code>new</code>,<code>unique_ptr</code> 在離開範圍時自動 <code>delete</code>。你不需要(也不應該)自己寫 <code>delete</code>。",
       code("p17/a3"), term("p17/a3")),
  step(4, "親眼看見自動歸還",
       "下面的 <code>Resource</code> 在建立與銷毀時各印一行訊息(解構子 <code>~Resource</code>),讓我們看到「什麼時候被歸還」。",
       code("p17/a4"), term("p17/a4"),
       see("「釋放資源」出現在「離開區塊之後」<b>之前</b>:離開內層區塊的那一刻,<code>unique_ptr</code> 就自動處理了。")),
  step(5, "對照:忘了 delete 的後果",
       "同樣的程式,改用原始的 <code>new</code>,而且忘了 <code>delete</code>:",
       code("p17/a5"), term("p17/a5"),
       warn("輸出裡<b>沒有</b>「釋放資源」。解構子根本沒被執行,資源就這樣洩漏了。用 <code>unique_ptr</code> 完全不會有這個問題。", "洩漏的證據")),
  step(6, "shared_ptr:多個擁有者",
       "有時候真的需要多個地方共同擁有一個物件。<code>shared_ptr</code> 記錄「有幾個人還在用」(<code>use_count()</code>),最後一個放手時才歸還。",
       code("p17/a6"), term("p17/a6"),
       "<p><code>unique_ptr</code> 的重點是「獨佔」,所以<b>不能複製</b>:</p>",
       code("p17/e1.err"), errterm("p17/e1.err"),
       tip("<b>預設選 <code>unique_ptr</code>;確定需要共享時才用 <code>shared_ptr</code></b>。大部分時候,直接用普通的區域變數與 <code>vector</code> 就夠了,完全不需要 <code>new</code>。"))
))

stuck = section("stuck", "初學者最常卡住的四個地方",
  details("什麼時候真的需要 <code>new</code> 或智慧指標",
          "<p>多數情況下,<b>普通的區域變數與 <code>vector</code>、<code>string</code></b> 就夠了,它們內部已經替你管理好記憶體。只有在「物件要活得比函式久」、「用基底類別指標操作子類別物件(多型)」等情況才需要。</p>"),
  details("<code>new[]</code> 要用 <code>delete[]</code>",
          "<p><code>int* a = new int[10];</code> 必須用 <code>delete[] a;</code> 歸還(有方括號)。用錯會出問題。更簡單的做法:根本不要用 <code>new[]</code>,改用 <code>vector&lt;int&gt;</code>。</p>"),
  details("<code>unique_ptr</code> 不能複製,怎麼傳給函式",
          "<p>要轉移所有權用 <code>std::move</code>,或把函式參數寫成「參考」。這屬於比較進階的內容,先知道「不能直接複製」即可。</p>"),
  details("基底類別的指標指向子類別物件,delete 後子類別的清理沒執行",
          "<p>基底類別的解構子要加 <code>virtual</code>(第 15 篇提過)。用 <code>unique_ptr&lt;Animal&gt;</code> 管理時也一樣要加,下面的練習 2 就會用到。</p>"))

QUIZ = quiz_cfg([
  ("<code>int* p = new int(5);</code> 之後,程式結束前一定要做什麼?", ["delete p(或改用智慧指標)", "什麼都不用做", "把 p 設成 0"], 0, "new 要的 heap 空間要自己歸還;或乾脆交給智慧指標。"),
  ("什麼叫記憶體洩漏?", ["要了 heap 空間卻沒歸還,而且沒有指標能再找到它", "變數太多", "程式跑太慢"], 0, "洩漏的空間會一直被佔著,直到程式結束。"),
  ("<code>delete p;</code> 之後,<code>p</code> 變成?", ["懸空指標(應設成 nullptr)", "自動變成 nullptr", "指向新的空間"], 0, "delete 不會改 p 的值,p 還握著舊位址,不能再使用。"),
  ("<code>unique_ptr</code> 的特色是?", ["獨佔所有權,不能複製,離開範圍時自動歸還", "可以任意複製", "需要手動 delete"], 0, "獨佔所有權,由它負責最後的歸還。"),
  ("需要讓多個地方共同擁有同一個物件,用?", ["shared_ptr", "unique_ptr", "int*"], 0, "shared_ptr 計算擁有者數量,最後一個放手時才歸還。"),
])

practice = section("practice", "動手演練:把借與還交給智慧指標",
  '<p class="sub" style="margin-bottom:18px">每題先自己寫,再展開看參考解答。</p>',
  exercise(1, "提早離開也不會洩漏", "寫一個函式 <code>work(bool fail)</code>:建立 <code>unique_ptr&lt;Resource&gt;</code>,如果 <code>fail</code> 為真就印出訊息並提早 <code>return</code>。分別呼叫 <code>work(true)</code> 與 <code>work(false)</code>,觀察「釋放資源」是不是都有印出。", "p17/x1",
           note="不管從哪一條路離開函式,<code>unique_ptr</code> 都會自動歸還。如果是原始的 <code>new</code>,你得在每個出口都記得 <code>delete</code>。"),
  exercise(2, "智慧指標加多型", "用 <code>vector&lt;unique_ptr&lt;Animal&gt;&gt;</code> 放入 <code>Dog</code> 與 <code>Cat</code>(用 <code>make_unique</code> 與 <code>push_back</code>),迴圈呼叫 <code>speak()</code>。<code>Animal</code> 的解構子要加 <code>virtual</code>。", "p17/x2",
           note="走訪時用 <code>auto&amp;</code>(參考),因為 <code>unique_ptr</code> 不能複製。這是第 15 篇多型加上本篇的組合。"),
  exercise(3, "數一數擁有者", "建立 <code>shared_ptr&lt;int&gt; a</code>,印出 <code>use_count()</code>;複製兩次(<code>b</code>、<code>c</code>)再印;<code>b.reset()</code> 後再印一次。預期是 1、3、2。", "p17/x3"),
  QUIZ_HTML,
  chk(["我知道 stack 自動收回、heap 要自己還。", "我會用 <code>new</code> / <code>delete</code>,並知道 delete 後要把指標設成 <code>nullptr</code>。",
       "我能認出記憶體洩漏與懸空指標。", "我會用 <code>make_unique</code> 與 <code>unique_ptr</code>,知道它不能複製。",
       "我知道 <code>shared_ptr</code> 用 <code>use_count</code> 記錄擁有者數量。", "我知道能不用 <code>new</code> 就不用,要用就用智慧指標。"]),
  links([("https://en.cppreference.com/cpp/memory/unique_ptr", "cppreference:std::unique_ptr", "cppreference.com"),
         ("https://en.cppreference.com/cpp/memory/shared_ptr", "cppreference:std::shared_ptr", "cppreference.com")]))

SPEC = spec(
  file="clang-memory-guide.html",
  title="動態記憶體與智慧指標:new 出來的就要還,智慧指標替你還",
  eyebrow="第 17 篇 · 動態記憶體與智慧指標〔進階選讀〕",
  h1="<code>new</code> 出來的就要還,智慧指標替你還",
  sub="用 stack 與 heap 的動畫,看懂借與還、記憶體洩漏與懸空指標,並學會用 <code>unique_ptr</code> 讓歸還自動發生。",
  tldr="用 <code>new</code> 向 heap 要的空間,要自己 <code>delete</code>;忘了就是<strong>記憶體洩漏</strong>,<code>delete</code> 後還用就是<strong>懸空指標</strong>。現代做法:<strong>能不用 <code>new</code> 就不用,要用就用 <code>unique_ptr</code>(獨佔、自動歸還)</strong>,需要共享才用 <code>shared_ptr</code>。",
  toc=[("what", "stack 與 heap"), ("steps", "六個步驟"), ("stuck", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, steps_, stuck, practice]),
  config=dict(stepper=STP, quiz=QUIZ),
  **nav(17),
)
