# -*- coding: utf-8 -*-
from h import *
import bb

CODE = """// 第 1 篇:讓 Uno 板子上自己的 L 燈閃爍(不需要接任何線)
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);   // LED_BUILTIN 是板子內建 LED 的腳位;Uno 上就是 13 號腳
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);  // 輸出 5V:L 燈亮
  delay({ms});                      // 等 {ms} 毫秒(1000 毫秒 = 1 秒)
  digitalWrite(LED_BUILTIN, LOW);   // 輸出 0V:L 燈滅
  delay({ms});
}
"""
FILL = dict(ms="1000")
SKETCHES = [dict(name="blink-builtin", code=CODE, fill=FILL, sim=dict(seconds=5.2, pin="D13", period_ms=1000, tol_ms=15))]
CIRCUITS = []

uno_svg, uno_legend = bb.uno_overview_svg()

what = section("what", "Arduino 是一台你能自己寫程式的小電腦",
  '<div class="panel"><h3>三句話講完</h3>'
  '<p><b>Arduino Uno 是一塊電路板</b>,中間有一顆晶片(微控制器),你寫的程式就存在裡面。</p>'
  '<p><b>它能做兩件事</b>:讀取外面世界的訊號(按鈕、感測器),以及控制外面的零件(燈、馬達、蜂鳴器)。</p>'
  '<p style="margin-bottom:0"><b>你要學的有兩半</b>:電路(零件怎麼接在板子的腳位上),和程式(板子該怎麼反應)。這個主題會兩邊一起,一次只加一點點。</p></div>',
  '<h3 style="margin-top:26px">認識 Uno 板子</h3>',
  '<p class="sub" style="margin-bottom:14px">先不用背,知道有這些東西就好。之後每次用到,我會再指出來。</p>',
  canvas(uno_svg, uno_legend),
  '<h3 style="margin-top:26px">四條安全守則(整個主題都適用)</h3>',
  ops(["<b>改接線之前,先拔掉 USB。</b>先接好零件,最後才通電。",
       "<b>LED 一定要串電阻。</b>沒有電阻,電流過大會燒掉 LED 或腳位。",
       "<b>只用 USB 供電,電壓是 5 V。</b>初學階段不要接其他電源,也不要把 5V 直接接到 GND(短路)。",
       "<b>不確定就停手。</b>零件發燙、有焦味,立刻拔掉 USB,再檢查接線。"]))

PLAN_ROWS = [
  ["一、起步", "認識板子、安裝 IDE、第一次上傳,再學電與麵包板。", "第 1–2 篇"],
  ["二、輸出", "接 LED、讀電路圖、PWM 呼吸燈與蜂鳴器。", "第 3–6 篇"],
  ["三、輸入", "按鈕、Serial Monitor、電位器、光敏電阻。", "第 7–10 篇"],
  ["四、感測與驅動", "超音波、伺服馬達、溫濕度、LCD。", "第 11–14 篇"],
  ["五、進階", "millis()、中斷、I2C 與 SPI、綜合專案。", "第 15–18 篇"],
  ["六、附錄", "故障排除與速查表。", "第 19–20 篇"],
]
plan = section("plan", "這個主題怎麼學",
  '<p class="sub" style="margin-bottom:14px">每一篇都是「接線 → 程式 → 看到結果」的實作,從最簡單的開始。<b>照順序做最順</b>,後面的篇章會用到前面學過的東西。</p>',
  table("g3", ["階段", "做什麼", "篇章"], PLAN_ROWS),
  tip("難度標籤:<b>入門</b>不需要任何基礎;<b>基礎</b>用到前面學過的觀念;<b>進階</b>會同時用到多個零件;<b>進階選讀</b>不影響主線,可以跳過。"))

BUY_A = [
  ["Arduino Uno R3 + USB-B 線", "原廠或相容板都可以。相容板常用 CH340 晶片,Windows 可能要另外裝驅動(見後面「連接電腦」)。買到 Uno R4 也能跟著做,只是 USB 接頭和 IDE 設定不同。", "1 組 · 第 1 篇起"],
  ["麵包板(830 孔)", "有兩側各兩條電源軌(紅、藍線)的標準款。長麵包板的電源軌有些在中間是斷開的,第 2 篇會教你怎麼確認。", "1 塊 · 第 3 篇起"],
  ["公對公杜邦線", "兩端都是針腳。買 20 條以上的混色包,顏色不影響電路,但分色比較好檢查。", "20 條以上 · 第 3 篇起"],
  ["LED(5 mm)", "紅色 8 顆以上(第 17 篇要 8 顆),綠色、黃色各 2–3 顆。兩腳一長一短。", "紅 8、綠 3、黃 3 · 第 3 篇起"],
  ["電阻 220Ω(1/4 W,±5%)", "給 LED 限流用。四環電阻色環是紅、紅、棕、金。", "12 顆 · 第 3 篇起"],
  ["電阻 10kΩ", "光敏電阻的分壓電路用(第 10 篇);第 7 篇會看到外接電阻的寫法,但只讀不做。色環是棕、黑、橙、金。", "4 顆 · 第 10 篇起"],
  ["按鈕(4 腳 6×6 mm 輕觸開關)", "最常見的小方塊按鈕。", "2–4 個 · 第 7 篇起"],
  ["主動式蜂鳴器(5 V)", "「主動」表示內建振盪電路,通電就會響。有 + 與 − 兩隻腳,+ 較長。", "1 個 · 第 6 篇起"],
  ["電位器 10kΩ(B10K)", "三隻腳、有旋鈕的可變電阻。", "1 個 · 第 9 篇"],
  ["光敏電阻(例如 GL5528)", "表面有彎曲紋路的小圓片,越亮電阻越小。", "1 個 · 第 10 篇"],
]
BUY_B = [
  ["HC-SR04 超音波測距模組", "有兩個圓形探頭、四隻針腳(VCC、Trig、Echo、GND)。", "1 個 · 第 11、18 篇"],
  ["SG90 伺服馬達", "三條線:棕色 GND、紅色 5 V、橘色訊號。插頭是母頭。", "1 個 · 第 12 篇"],
  ["DHT11 溫濕度感測器", "買「三腳模組版」,上面已經附好上拉電阻;四腳單體版要自己另接電阻。", "1 個 · 第 13 篇"],
  ["LCD1602 + I2C 轉接板", "買已經焊好 I2C 背板的版本,背板上只有 GND、VCC、SDA、SCL 四隻針腳。", "1 個 · 第 14、18 篇"],
  ["公對母杜邦線", "伺服馬達的插頭與 LCD 的針腳需要用到。", "10 條 · 第 12、14 篇"],
]
BUY_C = [
  ["74HC595 移位暫存器(DIP-16)", "長方形、16 隻腳,可直接插在麵包板上。", "1 顆 · 第 17 篇"],
  ["(沿用)紅色 LED 8 顆、220Ω 電阻 8 顆", "前面第一批買的數量已經夠用。", "第 17 篇"],
]
parts = section("parts", "零件清單:分三批買,不用一次買齊",
  '<p class="sub" style="margin-bottom:14px">第一批就能做完第 1–10 篇。常見的「Uno 入門套件」通常已經包含大部分零件,買之前對照這張表。<b>規格是常見範例,以你手上的零件為準</b>;不確定的零件,先跳過那一篇,等買齊再回頭做。</p>',
  '<h3>第一批:第 1–10 篇</h3>', table("g3b", ["零件", "規格與購買注意", "數量 · 用到的篇章"], BUY_A),
  '<h3 style="margin-top:24px">第二批:第 11–14 篇</h3>', table("g3b", ["零件", "規格與購買注意", "數量 · 用到的篇章"], BUY_B),
  '<h3 style="margin-top:24px">第三批:第 15–18 篇</h3>', table("g3b", ["零件", "規格與購買注意", "數量 · 用到的篇章"], BUY_C),
  tip("<b>萬用電錶</b>(選買)可以量電阻、檢查線有沒有接通,出問題時很好用,但不是必要的。想玩 <code>tone()</code> 做音階的話,再加一個<b>被動式蜂鳴器</b>(第 6 篇會說明差別)。", "選買"))

install = section("install", "安裝 Arduino IDE(Windows)",
  '<p class="sub" style="margin-bottom:14px">IDE 是你寫程式、檢查、再送進 Uno 的軟體。本主題使用 <b>Arduino IDE 2.x</b>,需要 Windows 10 以上的 64 位元系統。</p>',
  steps(
    step(1, "下載安裝檔", "只從官方下載,避免抓到夾帶其他軟體的安裝檔。",
         ops(["用瀏覽器開 <code>arduino.cc</code> 的 Software 下載頁。", "找到 <b>Arduino IDE 2.x</b>,點 <b>Windows</b> 版本(Win 10 and newer, 64 bits)的安裝檔。", "下載頁可能問你要不要捐款,可以直接按 <b>Just Download</b>。"])),
    step(2, "執行安裝程式", "安裝程式只是一個精靈,一路按下一步即可。",
         ops(["雙擊下載好的 <code>arduino-ide_….exe</code>。", "同意授權條款,安裝選項與安裝位置維持預設,按 <b>Install</b>。", "安裝需要幾分鐘,完成後勾選 <b>Run Arduino IDE</b> 並按 <b>Finish</b>。"])),
    step(3, "第一次開啟", "第一次開啟時 IDE 會做初始設定,不要中途關掉。",
         ops(["第一次開啟時,IDE 會自動安裝 Uno 需要的板子套件(Arduino AVR Boards)與內建函式庫,視網路速度可能要一兩分鐘。", "Windows 防火牆或安全性提示可能跳出幾次,詢問是否允許 IDE 或安裝裝置驅動,<b>允許即可</b>。"]),
         see("看到編輯區裡有預設的 <code>void setup()</code> 與 <code>void loop()</code>。左邊是一排圖示的側邊欄,上方是工具列。")),
  ),
  '<h3 style="margin-top:26px">IDE 畫面導覽</h3>',
  table("g2", ["位置", "有什麼"], [
    ["上方工具列左側", "<b>勾號 Verify</b>:檢查並編譯程式,不會動到板子。<b>右箭頭 Upload</b>:編譯後把程式送進板子。旁邊是<b>板子下拉選單</b>,選板子與連接埠。"],
    ["上方工具列右側", "<b>Serial Plotter</b>(繪圖)與 <b>Serial Monitor</b>(放大鏡圖示)。第 8 篇會用到。"],
    ["左側側邊欄", "由上而下:Sketchbook(你存的程式)、<b>Boards Manager</b>(安裝板子套件)、<b>Library Manager</b>(安裝函式庫)、Debug、Search。"],
    ["下方", "<b>Output</b> 視窗:編譯與上傳的訊息;出錯時會有紅字。"],
  ]),
  tip("IDE 可以切換成中文介面,但<b>本主題的按鈕與選單名稱一律以英文介面為準</b>,對照畫面比較不會迷路,建議保持英文。"))

connect = section("connect", "接上 Uno,確認電腦找得到它",
  step(1, "用 USB 線把 Uno 接到電腦", "先確認電腦與板子之間有一條「能傳資料」的線。",
       ops(["USB-B 那頭(方形)插 Uno,另一頭插電腦。", "Uno 上標示 <code>ON</code> 的小燈會亮,表示有電。"]),
       warn("有些 USB 線只能充電、不能傳資料。如果後面抓不到板子,第一個要懷疑的就是這條線。", "線材")) ,
  step(2, "到「裝置管理員」確認", "這一步確認 Windows 真的認得這塊板子,比在 IDE 裡猜原因快。",
       ops(["在 Windows 搜尋列輸入「裝置管理員」並開啟。", "展開<b>連接埠(COM 和 LPT)</b>。"]),
       see("原廠 Uno 會顯示 <code>Arduino Uno (COM3)</code> 這類名稱,後面的數字依電腦而異。相容板常顯示 <code>USB-SERIAL CH340 (COM4)</code>。這個 COM 數字就是之後在 IDE 選的連接埠。")),
  details("相容板:裝置管理員裡有黃色驚嘆號,或根本沒有連接埠",
    "<p>多半是缺少 CH340 晶片的 USB 驅動。Windows 有時會自動安裝;沒有的話,到晶片廠商 <b>WCH(沁恆)</b>的官網搜尋 <code>CH341SER</code> 驅動,下載後執行安裝,再重新插拔 USB。這一步不是 Arduino 官方文件的內容,請只從 WCH 官網下載。</p>"
    "<p style=\"margin-bottom:0\">裝好後,裝置管理員會出現 <code>USB-SERIAL CH340 (COM數字)</code>。</p>") ,
  details("我的板子是 Uno R4(USB-C)",
    "<p>接線與程式和 R3 完全相同(兩者都是 5V 邏輯、腳位位置相同),但 IDE 需要多一個設定:點左側邊欄的 <b>Boards Manager</b>,搜尋 <code>UNO R4</code>,安裝 <b>Arduino UNO R4 Boards</b> 套件。之後在板子下拉選單選你的 R4 型號(Minima 或 WiFi)。</p>"
    "<p style=\"margin-bottom:0\">本主題的範例都能在 R4 上編譯,但驗證是以 R3 為準;R4 的內建 LED 腳位同樣用 <code>LED_BUILTIN</code> 表示。</p>"))

first = section("first", "第一次上傳:讓板子自己的 L 燈閃起來",
  '<p class="sub" style="margin-bottom:14px">這一步不需要麵包板、不需要任何線,只有 Uno 與電腦。目的是確認「IDE → USB → 板子」整條路是通的,之後有問題就能排除這一段。</p>',
  fill([("ms", "閃爍間隔(毫秒)", True)]),
  steps(
    step(1, "開新草稿碼並貼上程式", "Arduino 稱程式為「草稿碼(sketch)」。",
         ops(["選單 <b>File → New Sketch</b>。", "<code>Ctrl + A</code> 全選預設內容後刪掉。", "按下面程式的 <b>Copy</b>,貼進編輯區。"]),
         cmd(CODE, cap="Arduino 程式(會依上面填的間隔更新)", cpp=True),
         tip("你也可以用內建範例:<b>File → Examples → 01.Basics → Blink</b>,效果相同。")),
    step(2, "選板子與連接埠", "告訴 IDE 要把程式送到哪塊板子。",
         ops(["看工具列,勾號與右箭頭旁有下拉選單。Uno 接好後通常會自動顯示 <b>Arduino Uno</b> 與 COM 埠。", "沒有的話:點下拉選單 → <b>Select other board and port…</b>,或用 <b>Tools → Board → Arduino AVR Boards → Arduino Uno</b> 加上 <b>Tools → Port</b>,選後面標著 <code>(Arduino Uno)</code> 的那個。"])),
    step(3, "驗證,再上傳", "驗證只檢查程式,不動板子。先驗證,出錯時比較好找原因。",
         ops(["按<b>勾號(Verify)</b>,等 Output 視窗跑完,沒有紅字。", "按<b>右箭頭(Upload)</b>。上傳時 Uno 上的 <code>TX</code>、<code>RX</code> 燈會快速閃。"]),
         see("Output 視窗結尾出現上傳完成的提示(Done uploading)。")),
    step(4, "看板子的 L 燈", "上傳完成後,Uno 會立刻執行,不用再按任何東西。",
         see("Uno 上標示 <code>L</code> 的小燈<b>亮 1 秒、滅 1 秒</b>,不斷重複。你的第一個程式成功了!"),
         tip("按一下 Uno 的 RESET 按鈕,程式會從頭再跑一次。程式存在板子裡,拔掉 USB 再插上,它還是會自己開始閃。")),
  ),
  '<h3 style="margin-top:26px">這支程式在做什麼</h3>',
  table("g2", ["這一行", "它在做什麼"], [
    ["<code>void setup() { … }</code>", "開機或按 RESET 後<b>只執行一次</b>,放準備工作。"],
    ["<code>pinMode(LED_BUILTIN, OUTPUT);</code>", "把內建 LED 的腳位設成<b>輸出</b>:由 Arduino 決定這隻腳的電壓。<code>LED_BUILTIN</code> 在 Uno 上就是 13 號腳。"],
    ["<code>void loop() { … }</code>", "<code>setup()</code> 跑完後<b>一直重複</b>執行。"],
    ["<code>digitalWrite(LED_BUILTIN, HIGH);</code>", "輸出 5 V,L 燈亮。<code>HIGH</code> 要全大寫。"],
    ["<code>delay(1000);</code>", "暫停 1000 毫秒(1 秒),這段時間維持現在的狀態。"],
    ["<code>digitalWrite(LED_BUILTIN, LOW);</code>", "輸出 0 V,L 燈滅。"],
  ]),
  '<p class="sk">下一篇開始會自己接線,並把每個關鍵字再講仔細;這一篇先知道「能動」就好。</p>')

gotchas = section("gotchas", "常見卡關",
  details("Port 選單是灰色的,或 IDE 說找不到板子",
    ops(["先確認 Uno 上的 <code>ON</code> 燈有亮。", "換一條 USB 線(有些線只能充電),再換一個 USB 孔。", "到「裝置管理員」看有沒有連接埠;相容板請看前面的 CH340 驅動。", "關掉其他可能佔用連接埠的程式(例如另一個開著的 IDE 或序列埠軟體),重新插拔 USB。"]), True) +
  details("上傳失敗,出現 avrdude 或 stk500 開頭的紅字",
    "<p>這類訊息的意思大多是「IDE 跟板子溝通不上」。依序檢查:板子是否選成 <b>Arduino Uno</b>、連接埠是否選對、USB 線是否能傳資料、同時有沒有別的程式佔用連接埠。這四項都對,才懷疑板子本身。</p>") +
  details("驗證時出現紅字錯誤",
    "<p>第 1 篇的程式是直接貼上的,若出錯通常是貼上時少了一部分(例如最後的 <code>}</code>)。把編輯區清空,重新複製貼上一次。</p>") +
  details("上傳成功但 L 燈不閃",
    "<p>先按一下 RESET。還是不閃的話,檢查程式裡 <code>pinMode</code> 與 <code>digitalWrite</code> 的拼字與大小寫;Arduino 區分大小寫,<code>HIGH</code>、<code>OUTPUT</code> 必須全大寫。</p>"))

SIM = {
  "a1": "<b>不用。</b>這個症狀是電腦找不到板子,跟 IDE 本身無關。重新安裝是最後才考慮的事。",
  "a2": "<b>對。</b>先排除最便宜的原因:換一條能傳資料的 USB 線與另一個 USB 孔,再到「裝置管理員」確認有沒有連接埠。相容板另外要看 CH340 驅動。",
  "a3": "<b>不要。</b>程式還沒送進板子,跟程式內容無關。板子與電腦之間的連線沒通,改程式也不會有用。",
}
QUIZ = quiz_cfg([
  ("為什麼要先做「不接線、只讓 L 燈閃」這個練習?", ["因為 L 燈比外接 LED 亮", "確認 IDE、USB、板子這一整段是通的,之後出問題就能排除這一段", "因為外接 LED 很貴"], 1,
   "先把「電腦到板子」這一段確認通,之後排錯才能縮小範圍。"),
  ("<code>setup()</code> 與 <code>loop()</code> 的差別是?", ["setup 一直重複,loop 只跑一次", "setup 只跑一次,loop 一直重複", "兩個都只跑一次"], 1,
   "setup 開機後只跑一次;loop 跑完會回到開頭不斷重複。"),
  ("你的 Port 選單是灰色的,最先該檢查什麼?", ["重寫程式", "換一條能傳資料的 USB 線、換一個 USB 孔,並看裝置管理員", "重新安裝作業系統"], 1,
   "多半是線材或驅動的問題,先排除最便宜、最容易的原因。"),
  ("改接線之前,第一件事是?", ["先拔掉 USB", "先按 RESET", "先按 Verify"], 0,
   "先拔電再接線,錯接時才不會有電流經過。"),
])

practice = section("practice", "動手演練與延伸閱讀",
  '<p class="sub" style="margin-bottom:18px">先選答案再看原因。重點是「找不到板子時,先查什麼」。</p>',
  sim("", "情境:IDE 的 Port 選單是灰的", "你下一步該怎麼做?",
      [("a1", "重新安裝 Arduino IDE"), ("a2", "換 USB 線與 USB 孔,再看裝置管理員有沒有連接埠"), ("a3", "改寫程式再上傳")]),
  QUIZ_HTML,
  checks(["我知道 Uno 板子上有 USB、RESET、數位腳位、電源腳位、類比腳位與 L 燈。",
          "我已經安裝 Arduino IDE 2.x,並能開啟它。",
          "裝置管理員裡看得到我的 Uno 的 COM 埠。",
          "我成功上傳程式,Uno 的 L 燈每秒閃一次。",
          "我記得安全守則:改接線前先拔 USB、LED 要串電阻。",
          "我已經對照零件清單,知道第一批要買什麼。"], "做完之後,對照這張清單"),
  resources([
    ("https://docs.arduino.cc/software/ide-v2/tutorials/getting-started/ide-v2-downloading-and-installing", "下載與安裝 Arduino IDE 2", "Downloading and installing the Arduino IDE 2"),
    ("https://docs.arduino.cc/software/ide-v2/tutorials/getting-started/ide-v2-uploading-a-sketch", "用 Arduino IDE 2 上傳草稿碼", "How to upload a sketch with the Arduino IDE 2"),
    ("https://docs.arduino.cc/built-in-examples/basics/Blink/", "Blink 內建範例", "Blink (built-in example)"),
    ("https://docs.arduino.cc/tutorials/uno-r4-minima/minima-getting-started", "Uno R4 入門(需安裝板子套件)", "Getting Started with Arduino UNO R4 Minima"),
  ], "Arduino 官方文件"))

SPEC = dict(
    dir="arduino",
    file="arduino-start-guide.html",
    title="認識 Arduino 與第一次上傳",
    eyebrow="第 1 篇 · 認識 Arduino",
    h1="從零開始:認識 Arduino、安裝 IDE,讓板子自己閃一次",
    sub="這一篇不接任何線。先認識 Uno 板子、備好零件、裝好軟體,再讓板子上自己的小燈閃爍,確認電腦到板子這條路是通的。",
    tldr="Uno 是一塊能自己寫程式的小電腦。<strong>分三批買零件</strong>(第一批做完第 1–10 篇),安裝 <strong>Arduino IDE 2</strong>,用 USB 接上板子,貼上 Blink 程式、選好板子與連接埠,按 Upload,L 燈每秒閃一次就成功了。",
    toc=[("what", "Arduino 是什麼"), ("plan", "怎麼學"), ("parts", "零件清單"), ("install", "安裝 IDE"), ("connect", "連接電腦"),
         ("first", "第一次上傳"), ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
    body="\n\n".join([what, plan, parts, install, connect, first, gotchas, practice]),
    config=dict(fill=FILL, sim=SIM, quiz=QUIZ),
    next=("arduino-electric-guide.html", "電與麵包板基礎"),
)
