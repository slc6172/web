from ch import *

what = section("what", "讓資料活得比程式更久,並優雅地處理出錯",
  '<div class="panel"><h3>兩個新能力</h3>'
  '<p><b>檔案輸入輸出</b>:程式結束,變數就消失了。想把資料留下來(成績、設定、紀錄),就要存進<b>檔案</b>,下次再讀回來。用法和 <code>cout</code> / <code>cin</code> 幾乎一樣,只是把「螢幕、鍵盤」換成「檔案」。</p>'
  '<p><b>例外處理</b>:檔案打不開、轉換失敗、除以零……程式難免遇到出錯。<code>try / catch</code> 讓你先「試試看」,出錯時乾淨地處理,而不是讓整個程式當掉。</p>'
  '<p style="margin-bottom:0" class="foot"><b>進階選讀</b>:這一篇不影響前面的主線,學完第 15 篇後再讀也可以。</p></div>',
  '<h3 style="margin-top:26px">六個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["<code>ofstream</code>", "輸出檔案串流:把資料「寫進」檔案(o = output)。"],
    ["<code>ifstream</code>", "輸入檔案串流:從檔案「讀出」資料(i = input)。"],
    ["<code>is_open()</code>", "檔案有沒有成功打開。"],
    ["例外", "程式執行中遇到的錯誤事件,可以被丟出(<code>throw</code>)與接住(<code>catch</code>)。"],
    ["<code>try</code> / <code>catch</code>", "<code>try</code> 裡面試著做;出現例外就跳到 <code>catch</code> 處理。"],
    ["<code>e.what()</code>", "例外附帶的錯誤說明文字。"],
  ]),
  tip("<b>線上編譯器的提醒</b>:有些線上編譯器不保留檔案,或限制能讀寫的位置。本篇的範例都是「同一支程式先寫、再讀回來」,不依賴檔案事先存在,所以大多數環境都能跑。如果你的線上編譯器不行,可以改用本機的 g++ 練習。"))

steps_ = section("steps", "照著做:七個步驟", steps(
  step(1, "寫入檔案,再讀回來",
       "用 <code>ofstream</code> 寫、<code>ifstream</code> 讀。<code>&lt;&lt;</code> 與 <code>getline</code> 都是你熟悉的語法。點 ⓘ 看說明。",
       code("p16/a1"), term("p16/a1"),
       see("寫進檔案的 <code>Hello</code> 與 <code>C++ 檔案</code>,被程式一行一行讀回來,再印到螢幕。")),
  step(2, "永遠先檢查:檔案打得開嗎?",
       "檔案不存在、沒有權限時會打不開。讀取之前先用 <code>is_open()</code> 確認。",
       code("p16/a2.exit1"), term("p16/a2.exit1"),
       tip("<code>main</code> 回傳 <code>0</code> 代表正常結束,非 <code>0</code> 代表有問題。這是作業系統與其他程式判斷你的程式有沒有成功的依據。")),
  step(3, "用 >> 一個一個讀數字",
       "檔案裡有一串用空格隔開的數字,用 <code>in &gt;&gt; n</code> 讀,讀完自然結束。",
       code("p16/a3"), term("p16/a3")),
  step(4, "附加模式:不要清掉舊內容",
       "預設的 <code>ofstream</code> 會把檔案<b>清空重寫</b>。想接著寫在後面,加上 <code>ios::app</code>。",
       code("p16/a4"), term("p16/a4"),
       warn("用錯模式會把舊資料蓋掉,而且無法復原。寫檔案前,先想清楚是要「重寫」還是「附加」。", "注意")),
  step(5, "try / catch:接住錯誤",
       "<code>stoi</code> 把文字轉成整數。轉不了的時候,不是回傳錯誤碼,而是<b>丟出例外</b>。用 <code>try / catch</code> 接住:",
       code("p16/a5"), term("p16/a5"),
       see("丟出例外後,<code>try</code> 裡剩下的程式會被跳過,直接進入 <code>catch</code>;處理完,程式<b>從 catch 之後繼續往下</b>執行。"),
       "<p>如果不接住,程式會直接異常中止:</p>",
       code("p16/c1.crash"), crash("p16/c1.crash")),
  step(6, "自己丟例外",
       "自己寫的函式發現狀況不對時,可以用 <code>throw</code> 丟出例外,把「怎麼處理」交給呼叫的人決定。",
       code("p16/a6"), term("p16/a6")),
  step(7, "整合:遇到壞資料,略過它繼續",
       "檔案裡混進一行壞資料(<code>abc</code>)。把每行的轉換放進 <code>try / catch</code>,壞資料被略過,好資料照樣算進去。",
       code("p16/a7"), term("p16/a7"),
       tip("這就是例外處理的價值:<b>錯誤被限制在一小塊範圍裡處理掉,不會讓整個程式停擺</b>。"))
))

stuck = section("stuck", "初學者最常卡住的四個地方",
  details("寫入的檔案找不到",
          "<p>相對路徑(例如 <code>\"notes.txt\"</code>)是相對於<b>程式執行時所在的資料夾</b>,不一定是原始碼所在的資料夾。到你執行程式的那個資料夾找找看。</p>"),
  details("讀不到資料,<code>is_open()</code> 是 false",
          "<p>檢查檔名拼對沒、大小寫、副檔名(Windows 有時會隱藏 <code>.txt</code>),以及檔案是不是在程式執行的資料夾。</p>"),
  details("寫入後,檔案是空的或內容不完整",
          "<p>沒有 <code>close()</code>,內容可能還留在暫存區沒真正寫進去。寫完呼叫 <code>close()</code>;程式正常結束時也會自動關閉,但養成手動關的習慣比較安全。</p>"),
  details("<code>catch</code> 沒有接到我丟出的例外",
          "<p><code>catch</code> 的型態要符合丟出的例外型態。<code>catch (const exception&amp; e)</code> 能接住標準函式庫丟出的大部分例外(包含 <code>runtime_error</code>、<code>invalid_argument</code>)。</p>"))

QUIZ = quiz_cfg([
  ("要把資料寫進檔案,用哪個型態?", ["ofstream", "ifstream", "cout"], 0, "ofstream 是輸出檔案串流(o = output);ifstream 是讀取。"),
  ("預設的 <code>ofstream</code> 開啟已存在的檔案,會?", ["清空原內容後重寫", "接在原內容後面", "報錯"], 0, "要接在後面,需要加 ios::app。"),
  ("<code>try</code> 裡面某一行丟出例外後,接下來會?", ["跳過 try 剩下的部分,執行 catch", "繼續執行 try 的下一行", "程式立刻結束"], 0, "例外一旦丟出,try 裡剩下的程式不會被執行。"),
  ("<code>stoi(\"abc\")</code> 沒有被 try / catch 包住,會?", ["程式異常中止", "回傳 0", "回傳 -1"], 0, "沒人接住的例外會讓程式異常中止。"),
  ("讀檔之前,最好先做什麼?", ["用 is_open() 檢查檔案是否成功開啟", "先 close()", "先 sort()"], 0, "檔案可能不存在或沒有權限,先確認才不會讀到空資料。"),
])

practice = section("practice", "動手演練:存檔、讀檔、不怕出錯",
  '<p class="sub" style="margin-bottom:18px">每題先自己寫,再展開看參考解答。</p>',
  exercise(1, "名單存檔再編號讀出", "把 Mina、Leo、Amy 三個名字寫進 <code>names.txt</code>(一行一個),再讀回來,印出時加上編號 <code>1. Mina</code>。", "p16/x1"),
  exercise(2, "計算檔案裡的數字", "把 <code>5 15 25 35</code> 寫進檔案,再讀出,算出個數、總和與平均。", "p16/x2",
           note="平均要避免整數除法:<code>(double)sum / count</code>(把 sum 暫時當成 double,是第 5 篇平均問題的另一種解法)。"),
  exercise(3, "安全的轉換", "從鍵盤讀入一串文字(例如 <code>12 x5 7</code>),能轉成整數的就印出它的兩倍,轉不了的印出「不是整數,略過」。", "p16/x3",
           note="<code>while (cin &gt;&gt; token)</code> 一個一個讀(第 13 篇),每個放進 <code>try / catch</code>。"),
  QUIZ_HTML,
  chk(["我會用 <code>ofstream</code> 寫檔、<code>ifstream</code> 讀檔。", "我知道讀檔前要用 <code>is_open()</code> 檢查。",
       "我分得出「清空重寫」與 <code>ios::app</code> 附加模式。", "我會用 <code>try / catch</code> 接住例外,並知道丟出例外後 try 剩下的部分會被跳過。",
       "我會用 <code>throw</code> 在自己的函式裡丟出例外。", "我知道相對路徑是相對於程式執行時的資料夾。"]),
  links([("https://en.cppreference.com/cpp/io/basic_fstream", "cppreference:檔案串流", "cppreference.com"),
         ("https://en.cppreference.com/cpp/error/exception", "cppreference:std::exception", "cppreference.com")]))

SPEC = spec(
  file="clang-file-exception-guide.html",
  title="檔案 I/O 與例外處理:檔案可能開不了,所以讀寫前一定要檢查",
  eyebrow="第 16 篇 · 檔案 I/O 與例外處理〔進階選讀〕",
  h1="檔案可能開不了,所以讀寫前一定要檢查",
  sub="讓資料存進檔案、下次再讀回來,並用 <code>try / catch</code> 處理出錯。這一篇是進階選讀,最後的小專案會用到它。",
  tldr="<code>ofstream</code> 寫檔、<code>ifstream</code> 讀檔,用法和 <code>cout</code> / <code>cin</code> 幾乎一樣;<strong>讀檔前先檢查 <code>is_open()</code></strong>,預設寫入會清空舊內容,要接著寫用 <code>ios::app</code>。出錯時用 <strong><code>try / catch</code></strong> 接住例外,沒人接的例外會讓程式異常中止。",
  toc=[("what", "兩個新能力"), ("steps", "七個步驟"), ("stuck", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, steps_, stuck, practice]),
  config=dict(quiz=QUIZ),
  **nav(16),
)
