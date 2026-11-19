from ch import *

FLOW = {"compile": dict(
    nodes=[
        dict(t="1 寫", s="main.cpp", d="你在文字編輯器(或線上編譯器的編輯區)寫下<b>原始碼</b>。它只是一個純文字檔,副檔名通常是 <code>.cpp</code>。這時電腦還看不懂它。"),
        dict(t="2 編譯", s="g++", d="<b>編譯器</b>先檢查你的文法,沒問題就把整份原始碼翻譯成機器碼。常見的編譯器有 <code>g++</code>、<code>clang++</code>、MSVC。線上編譯器按 Run 時,第 2、3、4 步都會自動幫你做完。"),
        dict(t="3 可執行檔", s="main / main.exe", d="翻譯的成果是一個<b>可執行檔</b>:Linux、macOS 上叫 <code>main</code>,Windows 上叫 <code>main.exe</code>。它已經跟編譯器無關,可以單獨執行。"),
        dict(t="4 執行", s="./main", d="作業系統載入可執行檔,從 <code>main</code> 開始一行一行執行,你就在螢幕上看到<b>輸出</b>。<br>想改程式?回到第 1 步修改原始碼,再重新編譯一次。")],
    failAt=1, failLabel="原始碼有文法錯誤",
    failText="編譯器發現文法錯誤,<b>不會產生可執行檔</b>,所以也不會有第 3、4 步。它會告訴你錯在第幾行。解法永遠一樣:讀錯誤訊息 → 回去改原始碼 → 重新編譯。(第 2 篇會專門教你讀錯誤訊息)")}

what = section("what", "C++ 是「先翻譯、再執行」的語言",
  '<div class="panel"><h3>用「食譜與廚師」來想</h3>'
  '<p>你寫的程式像一份用人類語言寫的<b>食譜</b>,但電腦這位廚師只看得懂機器碼。所以中間需要一位翻譯:<b>編譯器</b>。翻譯一次,就得到一份廚師能直接照做的版本。</p>'
  '<p style="margin-bottom:0">這和 Python 那種「邊讀邊做」的直譯式語言不同。C++ 多了編譯這一步,好處是跑起來很快、而且很多錯誤在執行前就會被揪出來。</p></div>',
  '<h3 style="margin-top:26px">先認識六個名詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["原始碼", "你寫的程式,一個純文字檔,副檔名 <code>.cpp</code>。"],
    ["編譯器", "把原始碼檢查並翻譯成機器碼的工具,例如 <code>g++</code>。"],
    ["編譯", "執行翻譯這個動作。有文法錯誤就會失敗並告訴你錯在哪。"],
    ["可執行檔", "編譯的成果,Windows 上是 <code>.exe</code>,可以直接執行。"],
    ["執行", "讓可執行檔真的跑起來,看到程式的結果。"],
    ["IDE", "整合開發環境:把編輯器、編譯器與「執行」按鈕包在一起的軟體,例如 VS Code 加外掛、Code::Blocks。"],
  ]))

flowsec = section("flow", "全貌:寫、編譯、執行,三步循環",
  '<p class="sub" style="margin-bottom:16px">點任一個方塊,或按「下一步」。勾選右下角的選項,看看編譯失敗時會怎樣。</p>',
  flow("compile"),
  tip("整本教學都是同一個循環:<b>寫一點 → 編譯 → 執行 → 看結果 → 再改</b>。每次只改一點點,出錯時就很容易找到原因。"))

env = section("env", "選一條路:先用線上編譯器,之後再裝本機",
  '<p class="sub" style="margin-bottom:16px">目標只有一個:今天就看到第一行輸出。環境問題是初學者最常放棄的地方,所以建議先走左邊。</p>',
  '<div class="two">'
  '<div class="panel"><h3>路線 A · 線上編譯器(推薦)</h3><p style="color:var(--gray-700)">免安裝,打開網頁就能寫、編譯、執行。</p>'
  + ops(["用瀏覽器開啟任一個線上 C++ 編譯器(本頁最下方有連結)。",
         "確認語言選的是 <b>C++</b>;如果有版本選項,選 <b>C++17</b>。",
         "把程式貼進編輯區,按 <b>Run</b>(或 Execute),看輸出區。",
         "需要輸入資料時(第 4 篇起),通常在網頁上的 Input / stdin 欄位填寫。"]) + '</div>'
  '<div class="panel"><h3>路線 B · 本機安裝 g++(進階)</h3><p style="color:var(--gray-700)">想離線練習、或之後要做大一點的專案時再裝。</p>'
  + ops(["Linux(Debian、Ubuntu):<code>sudo apt install g++</code>。",
         "macOS:在終端機執行 <code>xcode-select --install</code>。之後的 <code>g++</code> 指令實際上是 Apple 的 clang,用法相同。",
         "Windows:最省事是先安裝 WSL(Windows 內建的 Linux 子系統),再照 Linux 的做法;也可以用 MSYS2。",
         "安裝後用 <code>g++ --version</code> 確認有看到版本號。"]) + '</div></div>',
  details("本機要用到的三個指令(看一眼就好)",
          "<p>把程式存成 <code>main.cpp</code>,在同一個資料夾的終端機裡:</p>" +
          cmd("g++ -std=c++17 main.cpp -o main\n./main", cap="Linux / macOS") +
          cmd("g++ -std=c++17 main.cpp -o main.exe\nmain.exe", cap="Windows(PowerShell 請用 .\\main.exe)") +
          "<p style='margin-bottom:0'><code>-std=c++17</code> 指定語言版本,<code>-o</code> 指定可執行檔的名字。本教學全部以 C++17 為準。</p>"))

runsec = section("run", "跟著做:讓第一支程式跑起來", steps(
  step(1, "貼上一支現成的程式",
       "先不用懂內容(第 2 篇會逐行解釋),只要能把它跑起來。",
       ops(["線上編譯器:把下面的程式整段貼進編輯區。", "本機:存成 <code>main.cpp</code>。"]),
       code("p01/hello")),
  step(2, "編譯並執行",
       "線上:按 Run。本機:用上一節的兩行指令。兩種方式都該得到同樣的結果。",
       term("p01/hello", "你會看到(輸出區)"),
       see("輸出區出現 <code>Hello, C++!</code> 這一行。看到它,你就完成了從「寫」到「執行」的完整循環。")),
  step(3, "改一個字,再跑一次",
       "把雙引號裡的內容改成別的字,再編譯、執行一次。這是你第一次「改程式、看結果」。",
       code("p01/x1", prev="p01/hello"), term("p01/x1"),
       tip("每次改完程式,都要<b>重新編譯</b>(線上就是重新按 Run),輸出才會更新。很多人以為沒變,其實是執行到舊的版本。"))
))

stuck = section("stuck", "初學者最常卡住的四個地方",
  details("本機輸入 <code>g++</code> 顯示「找不到指令」或「不是內部或外部命令」",
          "<p>代表 g++ 還沒安裝,或安裝了但沒有加入系統的 PATH。先用 <code>g++ --version</code> 確認;如果只是想先學語法,改用線上編譯器最快。</p>"),
  details("線上編譯器按 Run 後出現奇怪的錯誤",
          "<p>先檢查頁面上選的語言是不是 <b>C++</b>。選成 C 或其他語言,同一段程式會因為語言不同而報一堆看不懂的錯。</p>"),
  details("中文輸出變成亂碼",
          "<p>多半是終端機的編碼不是 UTF-8。Windows 的命令提示字元可以先執行 <code>chcp 65001</code>;或直接改用線上編譯器,它通常沒有這個問題。</p>"),
  details("編譯成功了,但輸出還是舊的",
          "<p>幾乎都是忘了存檔,或是執行到舊的可執行檔。養成「存檔 → 編譯 → 執行」三個動作連著做的習慣。</p>"))

QUIZ = quiz_cfg([
  ("C++ 程式要執行前,必須先做哪一步?", ["編譯:用編譯器翻成機器碼", "把檔案存成 .exe 副檔名", "用瀏覽器開啟它"], 0,
   "電腦只看得懂機器碼,編譯器負責把你寫的原始碼翻譯成可執行檔。"),
  ("編譯時發現文法錯誤,會發生什麼事?", ["仍會產生可執行檔,但執行時會當掉", "不會產生可執行檔,並告訴你錯在哪一行", "編譯器會自動幫你修好"], 1,
   "有文法錯誤就不會有可執行檔。你要依訊息回去修改原始碼,再重新編譯。"),
  ("C++ 原始碼檔案通常用什麼副檔名?", [".cpp", ".exe", ".txt 才能被編譯"], 0,
   ".cpp 是 C++ 原始碼;.exe 是編譯之後的可執行檔(Windows)。"),
  ("初學者想最快看到第一個輸出,建議怎麼做?", ["先花一整天設定好本機環境", "用線上編譯器貼上程式,按 Run", "等學完所有語法再開始"], 1,
   "先看到結果最重要。本機環境可以之後再慢慢設定。"),
])

practice = section("practice", "動手演練:確認你真的跑得起來",
  '<p class="sub" style="margin-bottom:18px">每題先自己做,再展開看參考解答。</p>',
  exercise(1, "多印一行", "在 <code>Hello, C++!</code> 那一行的下面,再加一行,印出「我開始學 C++ 了」。編譯、執行,確認輸出有兩行。", "p01/x3", prev="p01/hello"),
  exercise(2, "故意搞壞它,再修好它",
           "下面這支程式少了一個分號。先在你的環境裡編譯看看,是不是出現類似的訊息;再把它修好。第 2 篇會教你怎麼讀這些訊息。",
           "p01/hello", before=code("p01/e1.err") + errterm("p01/e1.err"),
           note="分號補回來,就恢復正常了。編譯錯誤不可怕,它只是在告訴你「哪裡有問題」。", prev="p01/e1.err"),
  QUIZ_HTML,
  chk(["我說得出「原始碼、編譯器、可執行檔」各是什麼。", "我知道編譯失敗時不會產生可執行檔。", "我選好了一條環境路線(線上編譯器或本機 g++)。",
       "我成功跑出 <code>Hello, C++!</code>。", "我把訊息改成別的文字,並重新編譯看到新輸出。", "我看過一次編譯錯誤訊息,而且沒有被嚇到。"]),
  links([("https://en.cppreference.com/w/cpp", "cppreference:C++ 語言與標準函式庫參考", "cppreference.com"),
         ("https://www.onlinegdb.com/online_c++_compiler", "OnlineGDB:線上 C++ 編譯器", "onlinegdb.com"),
         ("https://www.programiz.com/cpp-programming/online-compiler/", "Programiz:線上 C++ 編譯器", "programiz.com")]))

SPEC = spec(
  file="clang-intro-guide.html",
  title="認識 C++ 與環境:寫、編譯、執行,三步就能讓 C++ 動起來",
  eyebrow="第 1 篇 · 認識 C++ 與環境",
  h1="寫、編譯、執行:三步就能讓 C++ 動起來",
  sub="這一篇不教新語法,只做一件事:讓你的第一支 C++ 程式真的跑起來。選好環境、貼上現成的程式、看到輸出,就完成了第一步。",
  tldr="C++ 程式要先<strong>編譯</strong>成機器看得懂的檔案才能執行:寫 → 編譯 → 執行。新手先用<strong>線上編譯器</strong>,貼上程式按 Run 就能看到結果;想離線練習再安裝 g++。",
  toc=[("what", "C++ 是什麼"), ("flow", "全貌圖"), ("env", "選環境"), ("run", "跟著做"), ("stuck", "常見卡關"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, flowsec, env, runsec, stuck, practice]),
  config=dict(flow=FLOW, quiz=QUIZ),
  **nav(1),
)
