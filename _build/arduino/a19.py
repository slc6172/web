# -*- coding: utf-8 -*-
from h import *
import bb

def L(n, t):
    return '<a href="arduino-%s-guide.html">第 %d 篇</a>' % (t, n)

P = {1: L(1, "start"), 2: L(2, "electric"), 3: L(3, "led"), 4: L(4, "loop"), 5: L(5, "schematic"), 6: L(6, "pwm"), 7: L(7, "button"), 8: L(8, "serial"), 9: L(9, "analog"),
     10: L(10, "ldr"), 11: L(11, "ultrasonic"), 12: L(12, "servo"), 13: L(13, "dht"), 14: L(14, "lcd"), 15: L(15, "millis"), 16: L(16, "interrupt"), 17: L(17, "bus"), 18: L(18, "project")}

DECIDE = [
  dict(label="IDE 的 Port 選單是灰的 / 找不到連接埠", risk="低",
       cmd="1. 確認 Uno 的 ON 燈有亮\n2. 換一條能傳資料的 USB 線,再換一個 USB 孔\n3. Windows 開「裝置管理員」→「連接埠(COM 和 LPT)」,看有沒有 Arduino Uno 或 USB-SERIAL CH340\n4. 相容板:安裝 CH340 驅動後重新插拔\n5. 關掉其他佔用連接埠的程式,重新插拔 USB",
       why="多半是 USB 線(只能充電)或驅動。詳見 %s(連接電腦)。" % P[1]),
  dict(label="上傳失敗(avrdude / stk500 開頭的紅字)", risk="低",
       cmd="1. 確認板子選 Arduino Uno、連接埠選對\n2. 換 USB 線、換 USB 孔\n3. 關掉可能佔用連接埠的程式(另一個 IDE 視窗、序列埠軟體)\n4. 拔掉接在 0、1 號腳的零件(它們與 USB 通訊共用)\n5. 重新插拔 USB,再上傳一次",
       why="這類訊息多半表示「IDE 跟板子溝通不上」。詳見 %s、%s。" % (P[1], P[3])),
  dict(label="編譯錯誤:expected ';' / was not declared in this scope", risk="低",
       cmd="1. 看輸出視窗第一條紅字的行號,從那一行與上一行找起\n2. 行尾少了分號 ; 嗎?\n3. { } 或 ( ) 有沒有成對?\n4. 大小寫:digitalWrite、HIGH、OUTPUT、Serial\n5. 變數有沒有先宣告?拼字有沒有打錯?",
       why="先修第一條錯誤,後面的紅字常是它連帶出來的。詳見 %s、%s。" % (P[3], P[4])),
  dict(label="編譯錯誤:找不到 xxx.h(函式庫)", risk="低",
       cmd="1. 開 Library Manager,搜尋函式庫名稱並 INSTALL\n2. 安裝時跳出相依視窗,按 INSTALL ALL\n3. DHT:還要有 Adafruit Unified Sensor;LCD:hd44780\n4. 裝好後重新驗證",
       why="Servo、Wire、SPI 是內建的;DHT、hd44780 要自己裝。詳見 %s、%s。" % (P[13], P[14])),
  dict(label="外接 LED 不亮", risk="中",
       cmd="1. 先拔 USB\n2. LED 方向:長腳(+)靠電阻、靠訊號那一側\n3. 電阻右腳與 LED 長腳在同一欄;LED 短腳那一欄有線接到 GND\n4. 程式的 LED_PIN 與訊號線插的腳位一致\n5. 有 pinMode(LED_PIN, OUTPUT) 嗎?上傳成功了嗎?",
       why="九成是接線。LED 一定要串電阻,不要為了讓它亮就拿掉。詳見 %s。" % P[3]),
  dict(label="零件發燙、冒煙或有焦味", risk="高",
       cmd="立刻拔掉 USB!\n1. 等零件冷卻\n2. 檢查 5V 與 GND 有沒有碰在一起(短路)\n3. 模組的 VCC、GND 有沒有接反(超音波、DHT11、LCD、SG90)\n4. LED 有沒有少了電阻\n5. 逐一拔掉零件再通電,找出元兇;燒壞的零件要換新",
       why="發燙幾乎都是短路或電源接反。詳見 %s、%s。" % (P[2], P[11])),
  dict(label="Uno 一直重新開機,或整個板子沒反應", risk="高",
       cmd="1. 拔掉 USB\n2. 檢查有沒有短路(5V 碰到 GND)\n3. 伺服馬達是不是吃太多電:拿掉負重,或改外接電源並共用 GND\n4. 一次接回一組零件,看是哪一組造成的\n5. 換一個 USB 孔、或用有電源的 USB 集線器",
       why="電流不夠或短路。詳見 %s、%s、%s。" % (P[12], P[18], P[2])),
  dict(label="按鈕一直是按下,或完全沒反應", risk="低",
       cmd="1. 按鈕用「對角」兩隻腳接線,並跨在中間凹槽上\n2. 一腳接訊號腳(例如 2 號腳),另一腳接 GND\n3. 程式用 pinMode(腳位, INPUT_PULLUP);按下讀到 LOW\n4. 用 Serial.println(digitalRead(...)) 親眼看",
       why="同一側的兩腳永遠相通。詳見 %s。" % P[7]),
  dict(label="按一下,程式觸發很多次", risk="低",
       cmd="1. 這是按鈕彈跳\n2. 簡單做法:偵測到變化後 delay(30),再等放開\n3. 不能 delay 的程式:用 millis() 的時間差(第 15 篇)\n4. 中斷:每一次電位變化都記時間,並用 CHANGE",
       why="詳見 %s、%s、%s。" % (P[7], P[15], P[16])),
  dict(label="Serial Monitor 亂碼或空白", risk="低",
       cmd="1. baud 選成和程式一致(Serial.begin(9600) → 9600)\n2. 程式有 Serial.begin(),且寫在 setup()\n3. 打開了 Serial Monitor,選對連接埠\n4. 不要把零件接在 0、1 號腳",
       why="詳見 %s。" % P[8]),
  dict(label="analogRead 固定是 0 或 1023,或亂跳", risk="低",
       cmd="1. 電位器:兩端接 5V 與 GND,中間腳接 A0\n2. 光敏電阻:A0 接在光敏電阻與 10kΩ 相接的那一欄\n3. A0 沒接任何東西會浮接、亂跳\n4. 用 Serial 印出數字,慢慢轉旋鈕 / 遮光看變化",
       why="詳見 %s、%s。" % (P[9], P[10])),
  dict(label="超音波一直顯示 out of range", risk="低",
       cmd="1. Trig 接 9 號腳(輸出)、Echo 接 10 號腳(輸入),沒有接反\n2. VCC 接 5V、GND 接 GND(對照模組上印的字)\n3. 前方要有硬的平面,不要太斜、太軟\n4. 程式的 TRIG_PIN、ECHO_PIN 與接線一致",
       why="詳見 %s。" % P[11]),
  dict(label="伺服馬達不動,或一動就抖、Uno 重開機", risk="中",
       cmd="1. 棕 GND、紅 5V、橘訊號(9 號腳),不要接反\n2. 程式有 #include <Servo.h>、attach(9)\n3. 抖動或重開機:拿掉負重;還是不行就改外接 4.8–6V 電源,與 Uno 共用 GND\n4. 不要讓搖臂頂到底或被卡住",
       why="伺服吃電多。詳見 %s。" % P[12]),
  dict(label="DHT11 一直讀取失敗", risk="低",
       cmd="1. S(DATA)接 2 號腳、+ 接 5V、− 接 GND(對照模組印刷)\n2. 函式庫與 Adafruit Unified Sensor 都裝了\n3. 兩次讀取至少隔 1–2 秒\n4. 程式型號是 DHT11,腳位與接線一致",
       why="詳見 %s。" % P[13]),
  dict(label="LCD 背光亮但沒字,或只有一排白色方塊", risk="低",
       cmd="1. 用小螺絲起子慢慢轉轉接板上的藍色對比旋鈕\n2. 四條線:VCC 5V、GND、SDA、SCL(沒有接反)\n3. L 燈一直閃:LCD 沒被找到,檢查接線\n4. 用 I2C 掃描器(第 17 篇)確認位址",
       why="對比沒調好是最常見的原因。詳見 %s、%s。" % (P[14], P[17])),
  dict(label="74HC595 的 LED 不亮或亂亮", risk="低",
       cmd="1. 晶片缺口朝左,16 腳(左上)5V、8 腳(右下)GND\n2. OE(13 腳)接 GND、SRCLR(10 腳)接 5V\n3. SER 接 11 號腳、SRCLK 接 13 號腳、RCLK 接 12 號腳\n4. 程式裡 LATCH_PIN 是 12,且 SPI.transfer 之後有把鎖存拉高",
       why="詳見 %s。" % P[17]),
  dict(label="按鈕有時候漏掉,或程式一做別的事就卡住", risk="低",
       cmd="1. 找出 loop() 裡的 delay()\n2. 改用 millis() 的時間差,每個工作快速檢查「該不該做」\n3. 變數用 unsigned long,比較用減法\n4. 真的不能漏的快速事件,用外部中斷(2、3 號腳)",
       why="詳見 %s、%s。" % (P[15], P[16])),
  dict(label="程式上傳成功,但行為還是舊的", risk="低",
       cmd="1. 確認上傳的是現在這個視窗(多個 IDE 視窗時很容易搞混)\n2. 輸出視窗有出現上傳完成嗎?\n3. 按一下 Uno 的 RESET\n4. 改一個明顯的地方(例如 delay 時間)再上傳,確認有變化",
       why="先確定「新程式真的進去了」,再找邏輯錯誤。詳見 %s。" % P[3]),
]

decidesec = section("decide", "我現在遇到的是…",
  '<p class="sub" style="margin-bottom:14px">選一個症狀,看該怎麼檢查。「風險」指<b>繼續通電可能損壞零件的程度</b>:標「高」的請先拔掉 USB。</p>',
  '<div class="panel"><div class="sim-buttons" id="decideBtns" role="group" aria-label="選擇你的症狀"></div>'
  '<div class="sim-result dec-out" id="decideOut" aria-live="polite">選一個症狀,看看該怎麼做。</div></div>')

method = section("method", "通用除錯:六個步驟",
  ops(["<b>停手、斷電。</b>先拔掉 USB,別在通電狀態下亂插拔。", "<b>縮小範圍。</b>一次只測一組零件;把能拿掉的都先拿掉。", "<b>確認「電腦 → 板子」這一段是通的。</b>上傳第 1 篇的 Blink,L 燈會閃,代表 IDE、USB、板子都沒問題。",
       "<b>從簡單到複雜驗證。</b>先量電壓與接線(對照圖與接線表),再看程式;程式用 Serial 印出變數。", "<b>一次只改一個地方。</b>改了再試,才知道是哪個改動有用。", "<b>有線索就記下來。</b>症狀、你做了什麼、結果,下次或問別人時很有用。"]),
  tip("<b>最強的除錯習慣:分段驗證。</b>接線與程式一次只加一樣,確認能動才加下一樣。第 18 篇的綜合專案就是這樣做出來的。"))

errors = section("errors", "常見編譯錯誤訊息對照",
  table("g3", ["訊息大意", "通常是", "怎麼處理"], [
    ["<code>expected ';' before …</code>", "上一行少了分號", "在上一行結尾補 <code>;</code>"],
    ["<code>'xxx' was not declared in this scope</code>", "拼字或大小寫錯、變數沒宣告", "對照拼字;<code>digitalWrite</code> 不是 <code>digitalwrite</code>"],
    ["<code>expected '}' at end of input</code>", "大括號沒有成對", "補上缺的 <code>}</code>"],
    ["<code>xxx.h: No such file or directory</code>", "函式庫沒安裝", "Library Manager 搜尋並安裝(裝相依)"],
    ["<code>stray '\\' in program</code> / <code>stray '\\343' …</code>", "程式碼裡混進了全形符號(中文標點、全形括號)", "把程式碼裡的全形 <code>( ) ; ,</code> 改成半形;註解裡的中文沒關係"],
    ["<code>avrdude: stk500_getsync() not in sync</code>", "IDE 跟板子溝通不上", "檢查板子、連接埠、USB 線、有沒有佔用"],
    ["<code>… multiple definition</code> / <code>redefinition</code>", "同一個東西定義了兩次", "刪掉重複的變數或函式"],
  ]),
  tip("<b>永遠先看第一條紅字,而且從它指出的行號與上一行開始找。</b>後面的錯誤常是被第一個錯連累出來的。"))

hw = section("hw", "硬體檢查清單(通電之前)",
  checks(["USB 拔掉了。", "所有零件的腳都插到底,沒有歪掉。", "LED 的長腳(+)與電阻、訊號同一側;每顆 LED 都有串電阻。", "5V 與 GND 沒有碰在一起;沒有零件被自己的導線短路。",
          "模組(超音波、DHT11、LCD、SG90)的 VCC 與 GND 沒有接反,對照模組上印的字。", "麵包板同一欄 a–e 相通;兩隻腳不要插在同一欄。", "你的麵包板電源軌中間有沒有斷開;上下電源軌需要時用線連起來。", "接線與程式的腳位一致。"], "通電之前,逐項檢查"))

SIM = {
  "a1": "<b>對。</b>把問題拆小:拔掉其他零件,只留一組,對照圖與接線表檢查,再用簡單的程式確認。重寫一般只會浪費時間。",
  "a2": "<b>不一定。</b>多數問題不在 IDE。先排除接線與電源,再考慮其他。",
}
QUIZ = quiz_cfg([
  ("零件發燙、有焦味,第一步?", ["立刻拔掉 USB", "繼續觀察", "換更大的電阻"], 0, "先斷電,再找原因,避免零件損壞擴大。"),
  ("編譯出現很多錯誤,先看哪一條?", ["第一條,從它的行號與上一行找起", "最後一條", "任意一條"], 0, "後面的錯誤常是第一個錯誤連累的。"),
  ("確認「IDE、USB、板子」這一段是通的,最好的測試是?", ["上傳 Blink,看 L 燈有沒有閃", "重新安裝作業系統", "換電腦"], 0, "這是最簡單、不用接線的測試。"),
  ("為什麼要「一次只改一個地方」?", ["才知道是哪個改動有用", "比較快", "沒有理由"], 0, "同時改很多處,就分不清誰有用。"),
  ("程式裡混進全形的括號,會出現什麼?", ["stray 開頭的編譯錯誤", "沒有影響", "LED 變亮"], 0, "程式碼必須用半形符號。"),
])
practice = section("practice", "演練與延伸閱讀",
  sim("", "情境:你的專案沒反應,你不知道從哪裡開始", "最好的第一步是?",
      [("a1", "拔電,把問題拆小,一次只測一組零件"), ("a2", "重新安裝 Arduino IDE")]),
  QUIZ_HTML,
  resources([
    ("https://support.arduino.cc/hc/en-us/articles/4733418441116-Upload-a-sketch-in-Arduino-IDE", "在 Arduino IDE 上傳草稿碼", "Upload a sketch in Arduino IDE"),
    ("https://docs.arduino.cc/software/ide-v2/tutorials/ide-v2-serial-monitor", "在 IDE 2 使用 Serial Monitor", "Using the Serial Monitor tool"),
    ("https://docs.arduino.cc/software/ide-v2/tutorials/ide-v2-installing-a-library", "在 IDE 2 安裝函式庫", "Installing libraries"),
  ], "Arduino 官方文件"))

SPEC = dict(
    dir="arduino",
    file="arduino-troubleshoot-guide.html",
    title="故障排除總整理",
    eyebrow="附錄 · 故障排除",
    h1="出問題了?從症狀找到該查哪裡",
    sub="整個主題最常遇到的狀況集中在這一頁:選你的症狀,看檢查順序,再跳到對應的篇章。",
    tldr="先<strong>斷電</strong>、再<strong>縮小範圍</strong>:上傳 Blink 確認「IDE → USB → 板子」是通的,然後一次只測一組零件。編譯錯誤<strong>先看第一條紅字</strong>。零件發燙<strong>立刻拔 USB</strong>。",
    toc=[("decide", "選你的症狀"), ("method", "通用六步"), ("errors", "編譯錯誤對照"), ("hw", "硬體檢查清單"), ("practice", "演練與延伸閱讀")],
    body="\n\n".join([decidesec, method, errors, hw, practice]),
    config=dict(fill={}, sim=SIM, quiz=QUIZ, decide=DECIDE),
    prev=("arduino-project-guide.html", "綜合專案:倒車雷達"),
    next=("arduino-reference-guide.html", "語法與電路符號速查"),
)
