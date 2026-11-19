from ch import *

def errline(id_):
    for l in RES[id_]["err"].splitlines():
        if "error:" in l:
            return l.split("error: ", 1)[1]
def crashline(id_): return RES[id_]["err"].splitlines()[0]
def pg(n):
    f, t = ORDER[n - 1]
    return '<a href="%s">第 %d 篇</a>' % (f, n)
def er(id_, cause, n):
    return ["<code>%s</code>" % e(errline(id_)), cause, pg(n)]

what = section("what", "最後一篇:會除錯,還要做出一個真的程式",
  '<div class="panel"><h3>這一篇做兩件事</h3>'
  '<p><b>第一,除錯</b>:寫程式一定會出錯,高手與新手的差別,是出錯時知道「怎麼找」。這裡有一份把前 17 篇所有錯誤集中起來的速查表,以及一個「用輸出找出邏輯錯誤」的完整示範。</p>'
  '<p><b>第二,專題</b>:把學過的東西組成一支完整的<b>成績管理程式</b>:新增學生、列出、統計、排序、存檔與讀檔。大約 120 行,分五個階段長大,每個階段都能執行。</p>'
  '<p style="margin-bottom:0">專題不教新語法,只是用你學過的東西解決一個真的問題。如果哪段看不懂,就回頭找對應的那一篇。</p></div>',
  '<h3 style="margin-top:26px">專題用到哪些東西</h3>',
  table("g3", ["工具", "學於", "專題用在"], [
    ["<code>struct</code>、<code>vector</code>", f"{pg(14)}、{pg(9)}", "一位學生一筆資料,全部放在 vector"],
    ["函式、傳參考、<code>const</code> 參考", f"{pg(11)}、{pg(12)}", "每個功能一個函式"],
    ["<code>if</code>、<code>switch</code>、迴圈", f"{pg(6)}、{pg(7)}", "選單與重複執行"],
    ["<code>sort</code>", pg(13), "依分數排序"],
    ["<code>ofstream</code>、<code>ifstream</code>、<code>try / catch</code>", pg(16), "存檔、讀檔、略過壞資料"],
    ["<code>cin.clear()</code>、<code>cin.ignore()</code>", pg(4), "輸入錯誤時救回 <code>cin</code>"],
  ]))

debug = section("debug", "除錯:出錯了,怎麼找?",
  '<p class="sub" style="margin-bottom:16px">錯誤分三種,對付的方法不同。</p>',
  table("g3", ["種類", "什麼時候發現", "怎麼辦"], [
    ["編譯錯誤", "按下編譯就失敗", "看<b>第一個</b> <code>error:</code>:檔名、行號、說明。修好再編譯。"],
    ["執行期錯誤", "程式跑到一半當掉", "多半是越界、空指標、除以 0、沒接住的例外。找「當掉前最後印出了什麼」。"],
    ["邏輯錯誤", "程式正常跑完,但<b>結果不對</b>", "最難:編譯器與系統都不會告訴你。要靠「印出變數」比對你預期的與實際的。"],
  ]),
  '<h3 style="margin-top:26px">編譯錯誤速查表</h3>'
  '<p class="sub" style="margin-bottom:12px">下面的訊息都是前面各篇用 g++ 實際編譯出來的(你的訊息引號可能是 <code>\'</code>)。</p>',
  table("g3w", ["訊息(<code>error:</code> 之後)", "常見原因", "回頭看"], [
    er("p02/e1.err", "少了分號", 2), er("p02/e2.err", "沒寫 <code>std::</code>,也沒有 <code>using namespace std;</code>", 2),
    er("p02/e3.err", "忘了 <code>#include</code>", 2), er("p02/e4.err", "大括號沒有成對", 2),
    er("p03/e1.err", "修改了 <code>const</code> 常數", 3), er("p11/e1.err", "函式在使用之前沒有宣告或定義", 11),
    er("p12/e1.err", "修改了 <code>const</code> 參考", 12), er("p13/e1.err", "忘了 <code>#include &lt;algorithm&gt;</code>", 13),
    er("p14/e1.err", "在類別外面存取 <code>private</code> 成員", 14), er("p15/e1.err", "在類別外面存取 <code>protected</code> 成員", 15),
    er("p17/e1.err", "複製了 <code>unique_ptr</code>", 17),
  ]),
  '<h3 style="margin-top:26px">執行期錯誤速查表</h3>',
  table("g3w", ["症狀", "常見原因", "回頭看"], [
    ["程式當掉(例如 Segmentation fault)", "陣列越界、對 <code>nullptr</code> 或懸空指標解參考", f"{pg(9)}、{pg(12)}、{pg(17)}"],
    ["Floating point exception", "整數除以 0 或對 0 取餘數", pg(5)],
    ["<code>%s</code>" % e(crashline("p09/c1.crash")), "用 <code>at()</code> 越界", pg(9)],
    ["<code>%s</code>" % e(crashline("p16/c1.crash")), "例外沒有被 <code>try / catch</code> 接住", pg(16)],
    ["程式停不下來", "無窮迴圈(條件永遠成立、忘了改變迴圈變數)", pg(7)],
    ["程式卡住不動", "在等 <code>cin</code> 輸入", pg(4)],
  ]),
  '<h3 style="margin-top:26px">邏輯錯誤:用輸出找出來</h3>'
  '<p class="why">這個程式要算 5 科成績的平均,明明總和是 395、平均應該是 79,卻印出 63。沒有任何錯誤訊息,怎麼找?</p>',
  code("p18/dbg1"), term("p18/dbg1"),
  '<p style="margin-top:14px"><b>方法:在可疑的地方,把關鍵變數印出來</b>,對照你「預期」的值。新增的除錯行用綠色底標出,看輸出:</p>',
  code("p18/dbg2", prev="p18/dbg1"), term("p18/dbg2"),
  see("第一筆 <code>i=1</code> 就是 <code>v[i]=92</code>:80 從來沒被加進去。原來迴圈從 <code>i = 1</code> 開始,漏掉了索引 0 的元素。這就是第 7、9 篇提過的<b>差一錯誤</b>。"),
  code("p18/dbg3", prev="p18/dbg1"), term("p18/dbg3"),
  '<h3 style="margin-top:26px">五個習慣</h3>',
  table("g2", ["習慣", "說明"], [
    ["1. 讀第一個錯誤", "不要被一大串訊息嚇到,先看最上面那個。"],
    ["2. 一次只改一處", "改完立刻重新編譯、執行。同時改很多處,你就不知道是哪個改動有效。"],
    ["3. 用小輸入重現", "用最小的資料讓錯誤再現,比用一大堆資料好找得多。"],
    ["4. 把變數印出來", "對照「我預期的值」與「實際的值」,第一個不一樣的地方就是線索。"],
    ["5. 縮小範圍", "把可疑的程式碼分段暫時註解掉,看錯誤是不是消失,就能知道問題在哪一段。"],
  ]))

proj_note = lambda: tip("專題的做法就是第 8 篇學過的:<b>從最小、能執行的一版開始,每次只加一個功能</b>。每個階段新增或改過的行,都用綠色底標出來。")

project = section("project", "專題:成績管理小程式", proj_note(), steps(
  step(1, "階段一:新增與列出",
       "先做最小的版本:一位學生一筆資料(<code>struct</code>),放在 <code>vector</code> 裡,有「新增」與「列出」兩個功能,用選單重複執行。橘色是你要輸入的。",
       code("p18/s1"), term("p18/s1")),
  step(2, "階段二:加上統計",
       "新增 <code>showStats</code>:算平均,並找出最高分的人。選單多一個選項。",
       code("p18/s2", prev="p18/s1"), details("看執行結果(橘色是輸入)", term("p18/s2"))),
  step(3, "階段三:依分數排序",
       "用 <code>sort</code>,並自己寫一個比較函式 <code>higherScore</code>,告訴它「分數高的排前面」。",
       code("p18/s3", prev="p18/s2"), details("看執行結果(橘色是輸入)", term("p18/s3")),
       tip("比較函式的回傳值意思是:<b>「a 應該排在 b 前面嗎?」</b>回傳 <code>true</code> 就排前面。")),
  step(4, "階段四:存檔與讀檔",
       "把資料存成 <code>students.txt</code>,下次還讀得回來。讀檔時,每筆資料的分數用 <code>stoi</code> 轉換,格式錯誤的用 <code>try / catch</code> 略過。",
       code("p18/s4", prev="p18/s3"), details("看執行結果(橘色是輸入)", term("p18/s4")),
       see("注意執行結果:存檔後新增了 Bob,列出有 4 人;<b>讀檔</b>之後又回到 3 人,Bob 不見了,因為檔案裡存的是當時的狀態。")),
  step(5, "階段五:完成——讓它不怕亂輸入",
       "最後一版:分數必須是 0 到 100(不合法就重問)、選單輸入非數字時不會當掉、用 <code>switch</code> 讓選單更清楚、用 <code>setw</code> 排整齊。下面是<b>完整的程式</b>(約 120 行)與一次完整的執行:",
       code("p18/s5", prev="p18/s4"), term("p18/s5"),
       see("看這次執行裡的三個錯誤輸入:分數 <code>150</code> 被擋下重問;選單輸入 <code>x</code> 與 <code>9</code>,程式都有禮貌地回應,沒有當掉。<b>這就是一支完整的小程式。</b>"))
))

nxt = section("next", "接下來可以學什麼?",
  '<p class="sub" style="margin-bottom:16px">你已經學完了 C++ 的基礎。下面是一些自然的下一步,依興趣挑一個就好。</p>',
  table("g2", ["方向", "說明"], [
    ["把 <code>Student</code> 改成 <code>class</code>", "分數設為 <code>private</code>,用 setter 檢查範圍(第 14 篇的想法),把「驗證」搬進型態裡。"],
    ["lambda 運算式", "不必另外寫 <code>higherScore</code> 函式,直接把比較寫在 <code>sort</code> 的呼叫裡。"],
    ["多檔案與標頭檔", "把大程式拆成 <code>.h</code> 與 <code>.cpp</code>,分別編譯。"],
    ["建置工具", "例如 Make、CMake:自動管理多個檔案的編譯。"],
    ["更多標準函式庫", "<code>&lt;algorithm&gt;</code>、<code>&lt;string&gt;</code> 還有很多好用的函式,多翻翻 cppreference。"],
    ["除錯器", "用 IDE 或 gdb 單步執行、設中斷點,比印出變數更強。"],
    ["樣板(template)", "寫出能處理任何型態的函式與類別,<code>vector</code> 就是這樣做出來的。"],
  ]),
  tip("<b>最好的學習方式是做專案</b>:挑一個你自己會用到的小工具(記帳、單字卡、待辦清單),一版一版把它做出來。遇到不會的,再回來查。"))

QUIZ = quiz_cfg([
  ("一次出現很多個編譯錯誤,應該先處理哪一個?", ["第一個", "最後一個", "隨便一個"], 0, "後面的錯誤常是第一個造成的連鎖反應。修好第一個再編譯。"),
  ("程式正常跑完,但結果不對,屬於哪一種錯誤?", ["邏輯錯誤", "編譯錯誤", "連結錯誤"], 0, "編譯與執行都沒問題,只是邏輯不是你想要的,最需要靠印出變數來找。"),
  ("用輸出除錯,最重要的做法是?", ["印出關鍵變數,對照預期的值", "把程式整段刪掉重寫", "把所有 cout 都拿掉"], 0, "第一個和預期不同的地方,就是線索。"),
  ("專題裡 <code>addStudent</code> 的參數寫成 <code>vector&lt;Student&gt;&amp;</code>,是為了?", ["把新學生加進呼叫端的 vector", "加快排序", "避免使用 struct"], 0, "傳參考,函式才能修改外面的 vector。"),
  ("<code>cin.clear(); cin.ignore(1000, '\\n');</code> 的作用是?", ["救回失敗的 cin,並丟掉錯誤的輸入", "清除螢幕", "關閉程式"], 0, "輸入型態錯誤時,cin 會進入失敗狀態,要先救回並清掉殘留的輸入。"),
])

practice = section("practice", "動手演練:擴充成績管理程式",
  '<p class="sub" style="margin-bottom:18px">下面三題都是專題的延伸功能。為了好懂,範例用固定的資料示範一個函式;完成之後,把它們放進你的專題裡。</p>',
  exercise(1, "依姓名搜尋", "寫 <code>int findStudent(const vector&lt;Student&gt;&amp; list, const string&amp; name)</code>:找到就回傳索引,找不到回傳 <code>-1</code>。讀入一個名字並印出分數(或「查無此人」)。", "p18/x1"),
  exercise(2, "及格人數", "寫 <code>int countPassed(const vector&lt;Student&gt;&amp; list)</code>,回傳 60 分以上的人數,並印出「及格人數:N / 總人數」。", "p18/x2"),
  exercise(3, "刪除學生", "寫 <code>bool removeStudent(vector&lt;Student&gt;&amp; list, const string&amp; name)</code>:找到就刪除並回傳 <code>true</code>,找不到回傳 <code>false</code>。提示:<code>list.erase(list.begin() + i)</code>。", "p18/x3",
           note="注意第一個參數是<b>非 const 的參考</b>,因為函式要修改 vector;其他兩題只讀,所以用 <code>const</code> 參考。"),
  QUIZ_HTML,
  chk(["我知道編譯錯誤、執行期錯誤、邏輯錯誤三種的差別與處理方法。", "我遇到編譯錯誤時,會先看第一個 <code>error:</code> 的行號與說明。",
       "我會用「印出變數」找出邏輯錯誤。", "我看得懂成績管理程式各個函式在做什麼。",
       "我能自己擴充專題的功能(搜尋、及格人數、刪除)。", "我知道下一步想學什麼,也知道去哪裡查資料。"]),
  links([("https://en.cppreference.com/cpp/algorithm/sort", "cppreference:std::sort", "cppreference.com"),
         ("https://en.cppreference.com/cpp/container/vector/erase", "cppreference:vector::erase", "cppreference.com"),
         ("https://en.cppreference.com/w/", "cppreference:C++ 參考首頁", "cppreference.com")]))

SPEC = spec(
  file="clang-project-guide.html",
  title="除錯與成績管理小專案:把學過的組起來,做出一支會存檔的程式",
  eyebrow="第 18 篇 · 除錯與成績管理小專案",
  h1="把學過的組起來:一支會存檔的成績管理程式",
  sub="先學會怎麼找錯:一份錯誤速查表與一次完整的除錯示範;再用五個階段,做出有新增、統計、排序、存檔與讀檔的成績管理程式。",
  tldr="錯誤分<strong>編譯、執行期、邏輯</strong>三種:編譯錯誤看第一個 <code>error:</code>;邏輯錯誤靠<strong>把關鍵變數印出來</strong>對照預期。專題是約 120 行的成績管理程式,<strong>從最小可執行版開始、一次加一個功能</strong>,最後完成輸入檢查、排序、存檔與讀檔。",
  toc=[("what", "這一篇做什麼"), ("debug", "除錯"), ("project", "專題"), ("next", "接下來"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, debug, project, nxt, practice]),
  config=dict(quiz=QUIZ),
  **nav(18),
)
