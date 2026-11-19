from ch import *

what = section("what", "條件判斷讓程式在路口選路",
  '<div class="panel"><h3>像走路遇到岔路</h3>'
  '<p>到目前為止,程式都是從上到下<b>一路走到底</b>。條件判斷讓它在路口先看一個<b>條件</b>,依成立或不成立,走不同的路。這就是「分支」。</p>'
  '<p style="margin-bottom:0">條件就是第 5 篇的比較與邏輯運算式。C++ 的規則很簡單:<b>結果是 0 就是假,不是 0 就是真</b>。</p></div>',
  '<h3 style="margin-top:26px">五個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["條件", "放在小括號裡、算出來是真或假的運算式,例如 <code>age &gt;= 18</code>。"],
    ["分支", "程式可能走的其中一條路。"],
    ["<code>if / else if / else</code>", "依序檢查條件,執行<b>第一個成立</b>的分支。"],
    ["<code>switch</code>", "依一個整數或字元的值,直接跳到對應的 <code>case</code>。"],
    ["巢狀", "條件裡面再放條件。"],
  ]))

steps_ = section("steps", "照著做:五個步驟", steps(
  step(1, "if 與 else:二選一",
       "<code>if</code> 後面的條件成立,就做第一段;不成立,做 <code>else</code> 那一段。橘色是你要輸入的。",
       code("p06/a1"), term("p06/a1"),
       warn("條件的小括號後面<b>不要加分號</b>:<code>if (age &gt;= 18);</code> 會讓 <code>if</code> 變成「什麼都不做」,後面的大括號永遠會執行。", "最常見的錯"),
       tip("即使裡面只有一行,也<b>養成加大括號的習慣</b>。以後再加第二行時,才不會出錯。")),
  step(2, "else if:多選一",
       "超過兩種情況,就用 <code>else if</code> 接著問。下面先看程式,再用追蹤器觀察:<b>輸入不同的分數,看哪一個分支被執行</b>。",
       code("p06/a2", prev="p06/a1"), term("p06/a2"),
       '<div style="margin-top:14px">' + '<div data-ladder="grade"></div>' + '</div>',
       see("<b>只有第一個成立的分支會執行</b>。輸入 95 時,後面的 <code>score &gt;= 80</code> 雖然也成立,卻根本不會被檢查。所以<b>條件的順序很重要</b>:要從最嚴格的開始寫。")),
  step(3, "switch:依值跳轉",
       "當條件是「某個整數或字元等於幾」時,<code>switch</code> 比一長串 <code>else if</code> 清楚。下面的追蹤器可以<b>取消 break</b>,看「穿透」是什麼。",
       code("p06/a3"), term("p06/a3"),
       '<div style="margin-top:14px"><div data-ladder="menu"></div></div>',
       "<p>真的把 <code>break</code> 全部拿掉的程式長這樣(輸入 2,和上面追蹤器取消勾選的結果一樣):</p>",
       code("p06/a4", prev="p06/a3"), term("p06/a4"),
       warn("漏寫 <code>break</code> 是 <code>switch</code> 最常見的錯。除非你<b>刻意</b>要穿透(而且寫上註解說明),否則每個 <code>case</code> 結尾都要有 <code>break</code>。", "注意")),
  step(4, "巢狀:條件裡面再放條件",
       "先判斷年齡,成年的人再判斷是不是學生。只有外層成立,才會走進去檢查內層。",
       code("p06/a5"), term("p06/a5"),
       tip("巢狀超過兩三層就很難讀。如果發現自己縮排越來越深,考慮改用 <code>&amp;&amp;</code> 合併條件,或拆開處理。")),
  step(5, "三元運算子:二選一取值",
       "只是要在兩個值中挑一個時,可以用 <code>條件 ? 值1 : 值2</code> 代替整段 <code>if / else</code>。",
       code("p06/a6"), term("p06/a6"),
       tip("三元運算子適合簡短的二選一。需要做很多事,還是用 <code>if</code> 比較清楚。"))
))

stuck = section("stuck", "初學者最常卡住的四個地方",
  details("<code>if (x = 5)</code> 永遠成立",
          "<p>單個 <code>=</code> 是賦值:它把 5 放進 x,然後整個式子的值是 5(不是 0),所以條件永遠為真,而且 x 還被改掉了。要比較請寫 <code>==</code>。許多編譯器開啟警告選項(例如 <code>-Wall</code>)時會提醒你。</p>"),
  details("成績 95 分卻得到 C",
          "<p>檢查順序反了。若先寫 <code>if (score &gt;= 60)</code>,95 分馬上成立,後面的 <code>&gt;= 90</code> 就沒有機會被檢查。<b>範圍型條件要從最嚴格的開始寫</b>。</p>"),
  details("<code>switch</code> 裡用了小數或文字",
          "<p><code>switch</code> 括號裡只能是整數或字元(<code>int</code>、<code>char</code> 等),不能用 <code>double</code> 或字串。需要比較那些,就用 <code>if / else if</code>。</p>"),
  details("<code>case</code> 裡宣告變數,編譯失敗",
          "<p>在 <code>case</code> 下面直接宣告變數常會編譯失敗。把該 <code>case</code> 的內容用大括號 <code>{ }</code> 包起來即可。目前先避免在 <code>case</code> 裡宣告變數。</p>"))

QUIZ = quiz_cfg([
  ("<code>if (score &gt;= 90) … else if (score &gt;= 80) …</code>,score 是 95,哪些分支會被執行?", ["只有第一個", "兩個都會", "兩個都不會"], 0,
   "只有第一個成立的分支會執行;後面的 else if 不會被檢查。"),
  ("條件 <code>if (x)</code> 在什麼情況下成立?", ["x 不是 0", "x 大於 0", "x 等於 1"], 0,
   "C++ 規定 0 是假、不是 0 都是真,所以 -3 也成立。"),
  ("<code>switch</code> 的 case 結尾沒有 <code>break</code>,會發生什麼事?", ["繼續執行下一個 case(穿透)", "編譯失敗", "程式立刻結束"], 0,
   "沒有 break 就不會跳出 switch,而是一路往下執行。"),
  ("哪一個寫法在多數情況下<b>能編譯卻意思錯誤</b>?", ["<code>if (a = 5)</code>", "<code>if (a == 5)</code>", "<code>if (a &gt;= 5)</code>"], 0,
   "單個 = 是賦值,會把 5 放進 a,而且整個條件永遠為真。"),
  ("<code>int m = (a &gt; b) ? a : b;</code> 的作用是?", ["把 a 與 b 中較大的存進 m", "把 a 和 b 相加", "比較 a 與 b 並印出結果"], 0,
   "條件成立時取 a,不成立時取 b,也就是取較大的那個。"),
])

practice = section("practice", "動手演練:讓程式自己做決定",
  '<p class="sub" style="margin-bottom:18px">每題先自己寫,再展開看參考解答。可以自己換不同的輸入值測試每個分支。</p>',
  exercise(1, "判斷奇偶", "讀入一個整數,印出它是奇數還是偶數。提示:第 5 篇學過 <code>n % 2</code>。", "p06/x1"),
  exercise(2, "成績等級", "讀入分數,依序印出 A(90 以上)、B(70 以上)、C(60 以上)、D(其餘)。<b>如果分數不在 0 到 100 之間,要印出錯誤訊息</b>。", "p06/x2",
           note="先檢查不合法的輸入,再從最嚴格的條件往下寫。多試幾個分數:100、70、69、-5。"),
  exercise(3, "簡易計算機", "讀入「數字 運算子 數字」,例如 <code>12 + 30</code>。用 <code>switch</code> 依運算子(<code>char</code>)計算並印出結果;不認識的運算子印出「不支援的運算子」。", "p06/x3",
           note="<code>case</code> 後面的字元要用單引號:<code>case '+':</code>。"),
  QUIZ_HTML,
  chk(["我知道 0 是假、不是 0 都是真。", "我會寫 <code>if / else if / else</code>,而且知道只有第一個成立的分支會執行。",
       "我知道範圍型條件要從最嚴格的開始寫。", "我會用 <code>switch</code>,並知道每個 <code>case</code> 要有 <code>break</code>。",
       "我知道 <code>=</code> 與 <code>==</code> 的差別。", "我知道三元運算子 <code>?:</code> 可以用來二選一取值。"]),
  links([("https://en.cppreference.com/cpp/language/if", "cppreference:if 敘述", "cppreference.com"),
         ("https://en.cppreference.com/cpp/language/switch", "cppreference:switch 敘述", "cppreference.com")]))

SPEC = spec(
  file="clang-conditions-guide.html",
  title="條件判斷:if 決定走哪條路,switch 適合一長串選項",
  eyebrow="第 6 篇 · 條件判斷",
  h1="<code>if</code> 決定走哪條路,<code>switch</code> 適合一長串選項",
  sub="讓程式依情況做不同的事:<code>if / else if / else</code>、<code>switch</code>、巢狀條件與三元運算子,並用追蹤器看清楚到底是哪個分支被執行。",
  tldr="<code>if / else if / else</code> 依序檢查條件,<strong>只執行第一個成立的分支</strong>,所以範圍條件要從最嚴格的開始寫。<code>switch</code> 依值跳轉,每個 <code>case</code> 結尾要 <code>break</code>。<strong>條件裡用 <code>==</code>,不是 <code>=</code></strong>。",
  toc=[("what", "路口與分支"), ("steps", "五個步驟"), ("stuck", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, steps_, stuck, practice]),
  config=dict(ladder=dict(
    grade=dict(label="score", value=85, presets=[95, 85, 70, 59], rows=[dict(c="score >= 90", a='cout << "A";'), dict(c="score >= 80", a='cout << "B";'), dict(c="score >= 60", a='cout << "C";')], other='cout << "不及格";'),
    menu=dict(label="choice", mode="switch", value=2, presets=[1, 2, 3, 9], rows=[dict(c=1, a='cout << "查詢中";'), dict(c=2, a='cout << "新增中";'), dict(c=3, a='cout << "再見";')], other='cout << "沒有這個選項";')), quiz=QUIZ),
  **nav(6),
)
