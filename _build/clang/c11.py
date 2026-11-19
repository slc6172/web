from ch import *
STP = {}

def fr(*frames): return [dict(t=t, v=v, **({"r": r} if r else {})) for t, v, r in frames]

# a4 的呼叫堆疊(行號 0 起算)
T4 = [
 dict(l=9, f=fr(("main()", {"x": "5"}, None)), n="main 開始執行,宣告 x = 5。"),
 dict(l=10, f=fr(("main()", {"x": "5"}, None), ("addOne(n)", {"n": "5"}, None)), n="呼叫 addOne(x):把 x 的值 5「複製」一份給新的盒子 n。堆疊上多了一個框。"),
 dict(l=4, f=fr(("main()", {"x": "5"}, None), ("addOne(n)", {"n": "6"}, None)), n="n = n + 1:只改了 n 這份影本,變成 6。main 的 x 還是 5。"),
 dict(l=5, f=fr(("main()", {"x": "5"}, None), ("addOne(n)", {"n": "6"}, None)), o="函式裡 n = 6\n", n="印出函式裡的 n。"),
 dict(l=6, f=fr(("main()", {"x": "5"}, None)), n="函式結束:addOne 的框(連同 n)整個消失,回到 main。"),
 dict(l=11, f=fr(("main()", {"x": "5"}, None)), o="main 裡 x = 5\n", n="x 完全沒變。這就是「傳值」:函式拿到的是影本。"),
]

def fact_trace():
    st, frames = [], [("main()", {}, None)]
    st.append(dict(l=11, f=fr(*frames), n="main 呼叫 factorial(4)。"))
    def rec(n, depth):
        frames.append(("factorial(%d)" % n, {"n": str(n)}, None))
        st.append(dict(l=3, f=fr(*frames), n="進入 factorial(%d):堆疊多了一個框。" % n))
        if n <= 1:
            st.append(dict(l=5, f=fr(*(frames[:-1] + [("factorial(%d)" % n, {"n": str(n)}, "1")])), n="n <= 1 成立,直接回傳 1。這個條件叫「終止條件」,沒有它會一直呼叫下去。"))
            frames.pop(); return 1
        st.append(dict(l=7, f=fr(*frames), n="n = %d,不是 1,所以要先算 factorial(%d) 才能相乘。" % (n, n - 1)))
        sub = rec(n - 1, depth + 1)
        val = n * sub
        st.append(dict(l=7, f=fr(*(frames[:-1] + [("factorial(%d)" % n, {"n": str(n)}, str(val))])), n="拿到 factorial(%d) = %d,計算 %d × %d = %d,回傳。" % (n - 1, sub, n, sub, val)))
        frames.pop(); return val
    v = rec(4, 0)
    st.append(dict(l=11, f=fr(("main()", {}, None)), o="%d\n" % v, n="全部回傳完畢,main 印出 %d。" % v))
    return st

what = section("what", "函式:把一件事打包起來,取個名字",
  '<div class="panel"><h3>像一台小機器:丟進去材料,拿出成品</h3>'
  '<p>你已經會用 <code>cout</code>、<code>length()</code>、<code>find()</code> 這些別人寫好的功能。<b>函式</b>就是讓你自己做出這樣的工具:把一件事寫一次、取個名字,之後想用就「呼叫」它,丟進去的資料叫<b>參數</b>,算出來送回去的叫<b>回傳值</b>。</p>'
  '<p style="margin-bottom:0">用函式有三個好處:<b>不用重複寫</b>、<b>程式切成小塊比較好懂</b>、<b>出錯時比較好找</b>。</p></div>',
  '<h3 style="margin-top:26px">七個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["定義", "寫出函式的內容:回傳型態、名字、參數、大括號裡做什麼。"],
    ["呼叫", "使用它:<code>square(5)</code>。"],
    ["參數", "函式收進來的資料。呼叫時傳進去的值叫「引數」。"],
    ["回傳值", "用 <code>return</code> 送回去的結果;沒有回傳的函式,型態寫 <code>void</code>。"],
    ["區域變數", "在函式裡宣告的變數,只在這個函式裡有效,結束就消失。"],
    ["多載", "同名但參數不同的函式,編譯器依你傳的資料自動挑。"],
    ["遞迴", "函式呼叫它自己。這一篇只預告。"],
  ]))

mapsec = section("map", "全貌:一個函式的長相",
  '<div class="panel"><pre style="margin:0;font:13.5px/1.9 var(--mono);overflow-x:auto">'
  '<b style="color:var(--clay-d)">int</b> <b>add</b>(<b style="color:var(--olive)">int a, int b</b>) {\n'
  '    return a + b;\n}'
  '</pre><p style="margin:10px 0 0;font-size:13.5px"><b style="color:var(--clay-d)">回傳型態</b>(送回去的是什麼) · <b>名字</b> · <b style="color:var(--olive)">參數清單</b>(收進來的是什麼) · 大括號裡是內容</p></div>',
  tip("取名字的原則:<b>用動詞、看名字就知道做什麼</b>,例如 <code>isPrime</code>、<code>printLine</code>、<code>maxOf</code>。"))

steps_ = section("steps", "照著做:七個步驟", steps(
  step(1, "定義第一個函式,並呼叫它",
       "點 ⓘ 看每一部分。先看函式怎麼寫,再看 <code>main</code> 怎麼用它。",
       code("p11/a1"), term("p11/a1")),
  step(2, "多個參數與多個 return",
       "參數可以有好幾個。函式的回傳值就是一個值,可以直接放進別的運算式,甚至當成另一個函式的參數。",
       code("p11/a2"), term("p11/a2"),
       see("<code>add(10, maxOf(2, 6))</code>:先算 <code>maxOf(2, 6)</code> 得 6,再算 <code>add(10, 6)</code> 得 16。")),
  step(3, "void:只做事、不回傳",
       "有些函式只是「做一件事」(例如印出訊息),不需要回傳值,回傳型態就寫 <code>void</code>。",
       code("p11/a3"), term("p11/a3")),
  step(4, "傳值:函式拿到的是影本",
       "這是函式最重要的概念。按「下一步」,看右邊的<b>呼叫堆疊</b>:每呼叫一次函式,就多一個框;函式結束,框就消失。",
       stepper(STP, "byval", "p11/a4", T4),
       details("要自己試的話:完整程式碼(可複製)", code("p11/a4") + term("p11/a4")),
       warn("在 <code>addOne</code> 裡修改 <code>n</code>,<b>不會</b>改到 <code>main</code> 的 <code>x</code>。如果想讓函式真的修改外面的變數,要用「參考」——下一篇會學。", "重要")),
  step(5, "先宣告,後定義",
       "C++ 是由上往下讀的。<code>main</code> 在前、函式在後時,要先用「函式宣告」告訴編譯器它的長相。先看沒有宣告會怎樣:",
       code("p11/e1.err"), errterm("p11/e1.err"),
       "<p>加上宣告(一行、分號結尾,不含內容)就解決了:</p>",
       code("p11/a5", prev="p11/e1.err"), term("p11/a5"),
       tip("簡單的原則:<b>把函式的定義放在 <code>main</code> 之前</b>,就不需要宣告。程式越來越大時,才會用到宣告。")),
  step(6, "預設參數與多載",
       "<b>預設參數</b>讓某個參數可以省略;<b>多載</b>讓同名的函式處理不同型態。新增的行用綠色底標出。",
       code("p11/a6"), term("p11/a6")),
  step(7, "遞迴預告:函式呼叫自己",
       "函式也可以呼叫它自己,這叫<b>遞迴</b>。這裡只讓你看「呼叫堆疊」是怎麼一層一層疊起來、又一層一層收回去的。階乘 <code>4! = 4 × 3 × 2 × 1</code>。",
       stepper(STP, "fact", "p11/a7", fact_trace()),
       details("要自己試的話:完整程式碼(可複製)", code("p11/a7") + term("p11/a7")),
       tip("遞迴一定要有<b>終止條件</b>(這裡是 <code>n &lt;= 1</code>),否則會一直呼叫下去、把堆疊用光。目前先知道它存在,不需要會寫。"))
))

stuck = section("stuck", "初學者最常卡住的四個地方",
  details("編譯錯誤:<code>was not declared in this scope</code>",
          "<p>呼叫的函式在更下面才定義,而且沒有先宣告。把函式定義移到 <code>main</code> 前面,或在前面加一行函式宣告。</p>"),
  details("函式改了參數,外面的變數沒變",
          "<p>這是傳值的正常行為:函式拿到的是影本。想改到外面,用參考(第 12 篇),或讓函式 <code>return</code> 新的值再由外面接住:<code>x = addOne(x);</code>。</p>"),
  details("忘了 <code>return</code>,結果是奇怪的數字",
          "<p>回傳型態不是 <code>void</code> 的函式,每一條路徑都必須 <code>return</code>。漏掉的話,編譯器(開啟警告時)會提醒你,執行結果也是不確定的。</p>"),
  details("在函式裡用了別的函式的變數",
          "<p>每個函式的變數是各自獨立的。<code>main</code> 裡的 <code>x</code>,在別的函式裡看不到,要用參數傳進去。</p>"))

QUIZ = quiz_cfg([
  ("<code>int square(int n)</code> 的回傳型態是?", ["int", "n", "square"], 0, "最前面的型態是回傳型態:這個函式會送回一個 int。"),
  ("函式裡修改了參數 <code>n</code>(傳值),會影響呼叫端的原變數嗎?", ["不會,函式拿到的是影本", "會", "只有 void 函式會"], 0, "傳值是複製一份給函式;函式結束後那份影本就消失了。"),
  ("不需要回傳任何值的函式,回傳型態寫?", ["void", "null", "0"], 0, "void 表示沒有回傳值。"),
  ("<code>main</code> 在函式 <code>add</code> 之前,又想呼叫 <code>add</code>,需要?", ["先寫 add 的函式宣告", "把 add 改成 void", "不需要任何東西"], 0, "編譯器由上往下讀,呼叫之前要先看過宣告或定義。"),
  ("遞迴函式一定要有什麼?", ["終止條件", "兩個以上的參數", "void 回傳型態"], 0, "沒有終止條件,函式會一直呼叫自己,直到堆疊用光。"),
])

practice = section("practice", "動手演練:自己寫函式",
  '<p class="sub" style="margin-bottom:18px">每題先自己寫,再展開看參考解答。</p>',
  exercise(1, "三個數的最大值", "寫一個函式 <code>maxOf3(a, b, c)</code>,回傳三個整數中最大的。提示:用第 2 步的 <code>maxOf</code> 組合出來。", "p11/x1"),
  exercise(2, "質數函式", "寫一個函式 <code>bool isPrime(int n)</code>,然後在 <code>main</code> 用迴圈找出 1 到 20 之間所有質數。", "p11/x2",
           note="函式裡一發現能整除,就可以<b>立刻 <code>return false</code></b>,不需要旗標變數(第 7 篇練習 3 的寫法可以簡化了)。"),
  exercise(3, "次方函式", "寫一個函式 <code>power(base, exp)</code>,用迴圈算出 base 的 exp 次方,不要用內建函式。印出 <code>power(2, 10)</code> 與 <code>power(3, 4)</code>。", "p11/x3"),
  QUIZ_HTML,
  chk(["我能看懂函式的回傳型態、名字與參數清單。", "我知道傳值是複製一份,函式裡改參數不會改到外面。",
       "我會用 <code>void</code> 寫「只做事」的函式。", "我知道函式要先宣告或定義,才能被呼叫。",
       "我知道預設參數與多載是什麼。", "我知道遞迴要有終止條件(只需要知道,不需要會寫)。"]),
  links([("https://en.cppreference.com/cpp/language/functions", "cppreference:函式", "cppreference.com"),
         ("https://en.cppreference.com/cpp/language/overload_resolution", "cppreference:多載解析", "cppreference.com")]))

SPEC = spec(
  file="clang-functions-guide.html",
  title="函式:把一件事打包起來,傳值傳的是影本",
  eyebrow="第 11 篇 · 函式",
  h1="函式把一件事打包起來,傳值傳的是影本",
  sub="學會定義與呼叫函式、參數與回傳值,並用呼叫堆疊的動畫,看懂為什麼函式裡改參數不會改到外面。",
  tldr="函式 = <strong>回傳型態 名字(參數) { … }</strong>,用 <code>return</code> 送回結果。預設是<strong>傳值:函式拿到的是影本</strong>,改了不影響外面。函式要先宣告或定義才能呼叫。多載與預設參數讓同名函式更彈性;遞迴先預告。",
  toc=[("what", "函式是什麼"), ("map", "函式的長相"), ("steps", "七個步驟"), ("stuck", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, mapsec, steps_, stuck, practice]),
  config=dict(stepper=STP, quiz=QUIZ),
  **nav(11),
)
