from ch import *

what = section("what", "六個零件,拼成一支程式",
  '<div class="panel"><h3>程式像一份照順序執行的清單</h3>'
  '<p>C++ 會從 <code>main</code> 開始,<b>由上往下、一行一行</b>執行。第一支程式只需要認識下面六個零件,其他都是在它們的基礎上加東西。</p>'
  '<p style="margin-bottom:0">你不需要現在就背起來:接下來四個步驟會讓它們一個一個出現。</p></div>',
  table("g2", ["零件", "作用"], [
    ["<code>#include &lt;iostream&gt;</code>", "引入「輸入輸出」工具箱,才能用 <code>cout</code> 印字。"],
    ["<code>int main()</code>", "程式的入口。每支程式都從這裡開始執行。"],
    ["<code>{ }</code>", "大括號圈出一段程式,必須成對。<code>main</code> 要做的事都寫在裡面。"],
    ["<code>std::cout &lt;&lt; …</code>", "把右邊的東西印到螢幕。<code>&lt;&lt;</code> 像一個箭頭,指向輸出的方向。"],
    ["<code>;</code>", "一個敘述的句點。每個敘述的結尾都要有它。"],
    ["<code>return 0;</code>", "告訴作業系統程式順利結束(0 代表成功)。"],
  ]))

steps_ = section("steps", "照著做:程式一步一步長出來", steps(
  step(1, "最小的 C++ 程式:什麼都不做",
       "先確認環境沒問題。這支程式合法、能編譯,只是沒有叫它印任何東西。",
       code("p02/a1"), term("p02/a1"),
       see("沒有任何錯誤,也沒有輸出。這正是預期的:<code>main</code> 一開始就用 <code>return 0;</code> 結束了。")),
  step(2, "讓它說話:加入 #include 與 cout",
       "印字需要工具箱(<code>#include</code>)和輸出指令(<code>cout</code>)。這一步新增的行會用綠色底標出來。",
       code("p02/a2", prev="p02/a1"), term("p02/a2"),
       warn("要印出的文字要放在<b>雙引號 <code>\"</code></b> 裡。單引號 <code>'</code> 是給單一字元用的,之後會學到。", "注意")),
  step(3, "多印一行,並看懂每一行",
       "想印幾行,就寫幾個 <code>cout</code>。下面這份程式已經幫每一行寫好說明:<b>點有 ⓘ 的那幾行</b>。",
       code("p02/a3", prev="p02/a2"), term("p02/a3"),
       tip("程式是<b>由上往下</b>執行的。把兩個 <code>cout</code> 的順序對調再執行,輸出的順序也會跟著對調。")),
  step(4, "兩個小捷徑:註解與 using namespace std",
       "每次都寫 <code>std::</code> 很麻煩,所以多數初學教材會加一行 <code>using namespace std;</code>,之後就能省略。<b>本教學從下一篇起都這樣寫。</b>",
       code("p02/a4", prev="p02/a3"), term("p02/a4"),
       table("g2", ["新東西", "說明"], [
         ["<code>// …</code>", "註解。從 <code>//</code> 到行尾,編譯器完全忽略,是寫給人看的筆記。"],
         ["<code>using namespace std;</code>", "<code>std</code> 是標準函式庫的「姓氏」。宣告之後,<code>std::cout</code> 可簡寫成 <code>cout</code>。"],
         ["<code>\\n</code>", "跳脫字元,代表換行,放在雙引號裡。效果和 <code>endl</code> 相近。"],
       ]))
))

errors = section("errors", "編譯錯誤長什麼樣:先看第一個,再看行號",
  '<p class="sub" style="margin-bottom:16px">寫程式一定會遇到錯誤。學會讀訊息,錯誤就變成「編譯器在指路」。下面四個是新手最常遇到的,訊息都是真的用 g++ 編譯出來的。</p>',
  '<h3>一則錯誤訊息怎麼讀</h3>',
  table("g2", ["訊息裡的部分", "意思"], [
    ["<code>main.cpp:4:44</code>", "檔名、第 <b>4</b> 行、第 <b>44</b> 個字元的位置。先去那一行附近看。"],
    ["<code>error:</code>", "錯誤,必須修好才能編譯。<code>warning:</code> 是警告,程式能跑但寫法可疑。"],
    ["<code>expected ‘;’ before ‘return’</code>", "說明。這句的白話:「在 return 之前,我預期要有一個分號」。"],
    ["下面兩三行", "把那一行程式印出來,用 <code>^</code> 標出編譯器注意到的位置。"],
  ]),
  tip("一次只修<b>第一個</b>錯誤,然後重新編譯。後面很多錯誤是第一個錯誤連鎖造成的,修好第一個,它們常常一起消失。"),
  details("錯誤 1:漏掉分號", code("p02/e1.err") + errterm("p02/e1.err") +
          "<p>編譯器指向第 4 行的行尾,說「在 <code>return</code> 之前缺了 <code>;</code>」。修法:在 <code>std::endl</code> 後面補上分號。</p>"
          "<p style='margin-bottom:0'>有時報錯的行號是「發現問題的地方」,真正的原因在它的<b>上一行</b>,所以報錯行與前一行都要看。</p>", True),
  details("錯誤 2:沒寫 std::,編譯器不認識 cout", code("p02/e2.err") + errterm("p02/e2.err") +
          "<p>編譯器不認識 <code>cout</code>,還貼心問你「是不是要寫 <code>std::cout</code>」。修法:改成 <code>std::cout</code> 與 <code>std::endl</code>,或在 <code>#include</code> 下面加 <code>using namespace std;</code>。</p>"),
  details("錯誤 3:忘了 #include", code("p02/e3.err") + errterm("p02/e3.err") +
          "<p>這次編譯器直接說出答案:「<code>std::cout</code> 定義在 <code>&lt;iostream&gt;</code>,你是不是忘了 <code>#include &lt;iostream&gt;</code>?」修法:在第一行補上它。</p>"),
  details("錯誤 4:大括號沒有成對", code("p02/e4.err") + errterm("p02/e4.err") +
          "<p><code>main</code> 開頭的 <code>{</code> 沒有對應的 <code>}</code>,編譯器一路讀到檔案結尾還在等。修法:在最後補上 <code>}</code>。大括號建議<b>一打左就馬上打右</b>,再回頭填中間的內容。</p>"))

QUIZ = quiz_cfg([
  ("每個 C++ 程式都從哪裡開始執行?", ["main 函式", "第一行的 #include", "最後的 return 0"], 0,
   "不管程式有多長,執行都從 main 開始。#include 是在編譯前先引入工具箱。"),
  ("漏掉敘述結尾的分號,會發生什麼事?", ["編譯失敗,並指出附近的位置", "程式照常執行", "電腦自動幫你補上"], 0,
   "C++ 用分號分隔敘述,少了它編譯器無法判斷哪裡結束,所以會報錯。"),
  ("<code>std::cout &lt;&lt; \"Hi\";</code> 裡的 <code>&lt;&lt;</code> 是在做什麼?", ["把右邊的內容送到左邊的輸出", "比較兩個數字誰大", "把檔案複製到螢幕上"], 0,
   "<< 像一個箭頭,把右邊的內容送進 cout,也就是螢幕。"),
  ("編譯器一次報了很多個錯誤,最好怎麼處理?", ["從第一個開始修,修完重新編譯", "從最後一個開始修", "全部一起修,最後再編譯"], 0,
   "後面的錯誤常常是第一個錯誤連鎖造成的。修好第一個再編譯,往往一次就消掉一大半。"),
])

practice = section("practice", "動手演練:自己寫、自己修",
  '<p class="sub" style="margin-bottom:18px">每題先自己做,再展開看參考解答。第 3 題要你當一次「除錯員」。</p>',
  exercise(1, "自我介紹", "寫一支程式,印出兩行:第一行「我叫小明」,第二行「我住在台北」(換成你自己的名字與城市)。", "p02/x1"),
  exercise(2, "用星號畫三角形", "用三個 <code>cout</code> 印出三行,組成一個三角形。提示:空格也是字元,要放在雙引號裡。", "p02/x2",
           note="每一行的前面要先印出幾個空格,星號才會置中。多試幾次調整空格數。"),
  exercise(3, "找出兩個錯誤", "下面的程式有兩個錯誤。編譯器的第一個抱怨如下。找出並修好它們——修好第一個之後,可能會出現下一個。",
           "p02/x3fix", before=code("p02/x3.err") + errterm("p02/x3.err"),
           note="第一個是 <code>endl</code> 後面漏了分號;修好後,編譯器才會抱怨第二個:<code>retrun</code> 拼錯了,應該是 <code>return</code>。", prev="p02/x3.err"),
  QUIZ_HTML,
  chk(["我看得懂 <code>#include</code>、<code>main</code>、<code>cout</code>、<code>;</code>、<code>{ }</code>、<code>return 0;</code> 各自的作用。",
       "我知道程式是由上往下一行一行執行。", "我能自己寫出一支會印出兩行文字的程式。",
       "我知道讀錯誤訊息要先看檔名、行號與 <code>error:</code> 之後的說明。", "我遇到多個錯誤時,會先修第一個再重新編譯。",
       "我認得四種常見錯誤:漏分號、沒寫 std::、忘了 #include、大括號沒成對。"]),
  links([("https://en.cppreference.com/cpp/io/cout", "cppreference:std::cout", "cppreference.com"),
         ("https://en.cppreference.com/cpp/language/main_function", "cppreference:main 函式", "cppreference.com")]))

SPEC = spec(
  file="clang-first-program-guide.html",
  title="第一支程式:只有五行有意義的程式,每一行都有用途",
  eyebrow="第 2 篇 · 第一支程式",
  h1="第一支程式只有五行,每一行都有用途",
  sub="從一支什麼都不做的程式開始,一步一步加上 <code>#include</code>、<code>cout</code>、註解,並且故意製造四種常見的編譯錯誤,學會讀懂它們。",
  tldr="每支程式都從 <code>main</code> 開始、<strong>由上往下</strong>執行;用 <code>std::cout &lt;&lt; \"文字\" &lt;&lt; std::endl;</code> 印字,<strong>每個敘述以分號結尾</strong>。編譯錯誤先看第一個:檔名、行號、<code>error:</code> 之後的說明。",
  toc=[("what", "六個零件"), ("steps", "四個步驟"), ("errors", "讀懂編譯錯誤"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, steps_, errors, practice]),
  config=dict(quiz=QUIZ),
  **nav(2),
)
