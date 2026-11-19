from ch import *

ERR_PRIV = RES["p14/e1.err"]["err"].splitlines()[1].split("error: ")[1]

what = section("what", "把相關的資料與操作,打包成自己的型態",
  '<div class="panel"><h3>內建的型態不夠用了</h3>'
  '<p><code>int</code>、<code>string</code> 只能表示單一個資料。但「一位學生」同時有名字、分數、學號……用好幾個分開的變數很零散。<b>struct</b> 與 <b>class</b> 讓你把相關的資料打包成<b>一個新的型態</b>,再用這個型態宣告出「物件」。</p>'
  '<p style="margin-bottom:0"><b>class</b> 更進一步:還能把「操作這些資料的函式」放在一起,並且用 <code>private</code> 把不想讓外面亂改的資料<b>保護</b>起來。</p></div>',
  '<h3 style="margin-top:26px">七個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["型態(類別)", "你自己設計的「資料藍圖」,例如 <code>Student</code>。"],
    ["物件", "照藍圖做出來的實體,例如 <code>Student a;</code> 的 <code>a</code>。"],
    ["成員變數", "型態裡的每一項資料,也叫欄位。"],
    ["成員函式", "型態裡的函式,專門處理這個型態的資料。"],
    ["建構子", "建立物件時自動執行的特殊函式,用來設定初始值。"],
    ["<code>public</code> / <code>private</code>", "公開(外面能用)與私有(只有自己能用)。"],
    ["getter / setter", "讀取與修改私有成員的公開函式。"],
  ]))

mapsec = section("map", "全貌:struct 與 class 差在哪",
  table("g3b", ["比較", "<code>struct</code>", "<code>class</code>"], [
    ["能放成員變數與成員函式", "可以", "可以"],
    ["沒特別寫時,成員預設是", "<code>public</code>", "<code>private</code>"],
    ["慣用在", "單純把資料打包(例如座標、一筆紀錄)", "有行為、要保護資料的物件(例如帳戶)"],
  ]),
  tip("<b>兩者幾乎一樣,只差預設的存取權限</b>。簡單的原則:資料很單純就用 <code>struct</code>;需要保護內部資料、控制怎麼被修改,就用 <code>class</code>。"))

steps_ = section("steps", "照著做:六個步驟", steps(
  step(1, "struct:把資料打包",
       "先設計一個 <code>Student</code> 型態,再用它做出物件。用<b>點 <code>.</code></b> 存取物件的成員。",
       code("p14/a1"), term("p14/a1"),
       warn("<code>struct</code> 的大括號後面要有<b>分號</b> <code>};</code>。漏掉的話,編譯器會報一堆讓人摸不著頭腦的錯。", "最常見的錯")),
  step(2, "加上成員函式",
       "把「印出自己」這個動作也放進型態裡。呼叫時寫 <code>物件.函式()</code>,印出的就是那個物件自己的資料。新增的行用綠色底標出。",
       code("p14/a2", prev="p14/a1"), term("p14/a2")),
  step(3, "class:用 private 保護資料",
       "銀行帳戶的餘額,不能讓外面隨便改。把它放在 <code>private</code>,只提供 <code>deposit</code>(存入)與 <code>getBalance</code>(查詢)兩個公開入口。<b>點下面方塊裡的成員</b>看說明,再<b>按下面的程式碼</b>,看哪些能用、哪些會被擋下。",
       code("p14/a3"), term("p14/a3"),
       '<div style="margin-top:14px"><div data-diagram="acct"></div></div>',
       "<p>真的在程式裡直接改 <code>balance</code>,編譯器會這樣擋下來:</p>",
       code("p14/e1.err"), errterm("p14/e1.err"),
       see("<code>is private within this context</code>:這是 private 成員,在類別外面不能碰。")),
  step(4, "建構子:建立物件時就設好初始值",
       "每次都要先宣告、再一個一個設定很麻煩,而且可能忘記。<b>建構子</b>讓你在建立物件的同時就把值放進去。",
       code("p14/a4"), term("p14/a4"),
       tip("建構子的名字和類別<b>一模一樣</b>,而且<b>沒有回傳型態</b>(連 <code>void</code> 也不寫)。")),
  step(5, "getter 與 setter:讓修改有把關",
       "分數不該小於 0 或大於 100。把 <code>score</code> 設成 <code>private</code>,所有修改都經過 <code>setScore</code>,就能統一檢查。",
       code("p14/a5"), term("p14/a5"),
       see("這就是<b>封裝</b>的好處:規則寫在一個地方,外面的人想亂改也改不了。下一篇會再深入談。")),
  step(6, "物件放進 vector",
       "物件和 <code>int</code>、<code>string</code> 一樣可以放進 <code>vector</code>,用迴圈處理。",
       code("p14/a6"), term("p14/a6"))
))

stuck = section("stuck", "初學者最常卡住的四個地方",
  details("編譯錯誤:<code>is private within this context</code>",
          "<p>在類別外面存取了 <code>private</code> 成員。改用公開的成員函式(例如 getter),或確認這個成員真的需要公開。</p>"),
  details("<code>struct</code> 或 <code>class</code> 結尾忘了分號",
          "<p>型態定義的右大括號後面要有 <code>;</code>。這是少數「大括號後面還要分號」的地方,漏掉時錯誤訊息常常出現在下面幾行,看起來和它無關。</p>"),
  details("建構子寫了參數,卻用 <code>Student s;</code> 宣告物件",
          "<p>一旦自己寫了需要參數的建構子,編譯器就不會再提供「不用參數」的版本。建立物件時要給參數:<code>Student s(\"Mina\", 90);</code>。</p>"),
  details("成員函式裡能直接用成員變數,為什麼外面不行",
          "<p>在成員函式裡,成員變數就在「自己家」,可以直接用。在外面(例如 <code>main</code>)要透過物件加點 <code>a.name</code>,而且還要這個成員是 <code>public</code>。</p>"))

QUIZ = quiz_cfg([
  ("<code>class</code> 裡沒有特別寫存取權限的成員,預設是?", ["private", "public", "protected"], 0, "class 預設 private;struct 預設 public,這是兩者唯一的差別。"),
  ("<code>BankAccount acc; acc.balance = 100;</code>,而 balance 是 private,會?", ["編譯失敗", "正常執行", "得到 0"], 0, "在類別外面不能直接存取 private 成員,編譯器會擋下來。"),
  ("建構子的特徵是?", ["名字和類別相同,且沒有回傳型態", "名字叫 init,回傳 void", "必須有參數"], 0, "建構子與類別同名、不寫回傳型態,建立物件時自動執行。"),
  ("把成員變數設為 private,再用 setter 修改,最大的好處是?", ["可以統一檢查,避免被改成不合理的值", "執行速度更快", "不需要建構子"], 0, "所有修改都經過同一個入口,規則寫一次就能保護資料。"),
  ("<code>a.print()</code> 印出的是誰的資料?", ["物件 a 自己的", "最後建立的物件的", "所有物件的"], 0, "成員函式處理的是呼叫它的那個物件自己的成員。"),
])

practice = section("practice", "動手演練:設計自己的型態",
  '<p class="sub" style="margin-bottom:18px">每題先自己寫,再展開看參考解答。</p>',
  exercise(1, "座標點", "用 <code>struct Point</code>(<code>x</code>、<code>y</code>)表示平面上的點,寫函式算兩點之間的「曼哈頓距離」(<code>|x1−x2| + |y1−y2|</code>)。<code>abs</code> 在 <code>&lt;cstdlib&gt;</code>。", "p14/x1"),
  exercise(2, "會評等級的學生", "設計 <code>class Student</code>:名字、分數(都 private),建構子,以及 <code>grade()</code>(90 以上 A、70 以上 B,其餘 C)與 <code>print()</code>。建立三位學生印出。", "p14/x2"),
  exercise(3, "不能透支的帳戶", "在 <code>BankAccount</code> 加上 <code>bool withdraw(int amount)</code>:金額合理且餘額足夠才扣款並回傳 <code>true</code>,否則回傳 <code>false</code>。", "p14/x3",
           note="回傳 <code>bool</code> 讓呼叫的人知道有沒有成功,這是設計成員函式很常見的手法。"),
  QUIZ_HTML,
  chk(["我知道 struct 與 class 能把資料與函式打包成新型態。", "我分得出型態(藍圖)與物件(實體)。",
       "我知道 class 的預設是 private,struct 的預設是 public。", "我會寫建構子,並知道它沒有回傳型態。",
       "我知道用 private 加 getter / setter 可以保護資料。", "我能把物件放進 <code>vector</code> 並用迴圈處理。"]),
  links([("https://en.cppreference.com/cpp/language/class", "cppreference:class 與 struct", "cppreference.com"),
         ("https://en.cppreference.com/cpp/language/access", "cppreference:存取權限", "cppreference.com")]))

SPEC = spec(
  file="clang-class-guide.html",
  title="struct 與 class:class 把資料與操作綁在一起,private 保護內部",
  eyebrow="第 14 篇 · struct 與 class",
  h1="<code>class</code> 把資料與操作綁在一起,<code>private</code> 保護內部",
  sub="設計自己的型態:成員變數、成員函式、建構子與存取權限,並看看被 <code>private</code> 擋下來的程式碼長什麼樣。",
  tldr="<code>struct</code> / <code>class</code> 把<strong>相關的資料與函式打包成新型態</strong>,用它做出物件。兩者只差預設權限:<strong>struct 預設 public,class 預設 private</strong>。用 <code>private</code> 保護資料,透過公開的成員函式(getter / setter)存取,並用建構子設定初始值。",
  toc=[("what", "為什麼要自己設計型態"), ("map", "struct vs class"), ("steps", "六個步驟"), ("stuck", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, mapsec, steps_, stuck, practice]),
  config=dict(diagram=dict(acct=dict(
      rows=[["acct"]],
      boxes=dict(acct=dict(name="BankAccount", fields=[dict(t="int", n="balance", v="pri", note="餘額。private:只有 BankAccount 自己的成員函式能讀寫它。")],
                           methods=[dict(t="void", n="deposit(int amount)", v="pub", note="存入。公開入口,內部會檢查金額必須大於 0。"),
                                    dict(t="int", n="getBalance()", v="pub", note="查詢餘額。公開入口,只讀,不能藉它修改餘額。")])),
      testsTitle="試試看:在 main 裡執行這些程式碼",
      tests=[dict(code="acc.deposit(500);", ok=True, msg="可以。deposit 是 public,而且它自己知道怎麼安全地更新 balance。", hl="acct.deposit(int amount)"),
             dict(code="acc.getBalance();", ok=True, msg="可以。getBalance 是 public,回傳目前的餘額。", hl="acct.getBalance()"),
             dict(code="acc.balance = 1000000;", ok=False, msg="編譯失敗:<code>" + ERR_PRIV.replace("<", "&lt;") + "</code>。balance 是 private,在類別外面不能直接改。", hl="acct.balance"),
             dict(code="cout << acc.balance;", ok=False, msg="編譯失敗:同樣是 <code>" + ERR_PRIV.replace("<", "&lt;") + "</code>。private 連「讀」都不行,要讀就透過 getBalance()。", hl="acct.balance")])), quiz=QUIZ),
  **nav(14),
)
