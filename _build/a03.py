# -*- coding: utf-8 -*-
from h import *
import bb

# ------------------------------------------------------------------ 電路(唯一資料來源)
CIRC = bb.Circuit(
    "led-blink", 16,
    parts=[
        bb.Resistor("R1", 220, "b5", "b9", 1),
        bb.LED("LED1", "red", "d9", "d10", 2),
        bb.Wire("W1", "UNO.D8", "a5", "orange", 3),
        bb.Wire("W2", "UNO.GND", "a10", "black", 4),
    ],
    steps=[
        ("放電阻", "電阻插在 <code>b5</code> 與 <code>b9</code>,橫跨 5 欄。<br>電阻沒有方向,哪隻腳插哪邊都可以,腳要插到底。"
                  "這顆是 220Ω(色環:紅、紅、棕、金)。它會串在 LED 前面,負責限制電流。"),
        ("放 LED", "<strong>長腳(+)</strong>插 <code>d9</code>,<strong>短腳(−)</strong>插 <code>d10</code>。<br>"
                  "<code>d9</code> 和電阻右腳 <code>b9</code> 在同一欄(第 9 欄),<code>a–e</code> 五個孔在內部相通,所以電阻的右腳已經接到 LED 的長腳。"
                  "兩腳等長時,看 LED 外殼邊緣:有平邊的那一側是負極(−)。"),
        ("橘線:Uno 8 號腳 → a5", "橘色杜邦線一端插 Uno 的 <strong>8 號腳</strong>,另一端插麵包板 <code>a5</code>。<br>"
                  "<code>a5</code> 和電阻左腳 <code>b5</code> 在同一欄,所以 8 號腳現在接到電阻。"),
        ("黑線:Uno GND → a10", "黑色杜邦線一端插 Uno 數位腳位排上的 <strong>GND</strong>(在 13 號腳旁邊),另一端插 <code>a10</code>。<br>"
                  "<code>a10</code> 和 LED 短腳 <code>d10</code> 在同一欄,所以 LED 的負極接回了 GND,電路繞成一圈。"),
    ],
    chain=["UNO.D8", "R1", "LED1", "UNO.GND"],
    code_pins={"LED_PIN": "UNO.D8"},
    intro="先<strong>拔掉 USB 線</strong>,接線時不要通電。圖上方是 Uno,下方是麵包板,Uno 的數位腳位排朝向麵包板。按「下一步」,一次放一個零件;目前這一步要插的零件會有橘色光圈。",
    done="8 號腳 → 電阻 → LED 長腳(+),LED 短腳(−)→ GND,電流有一條完整的圈。這個圈缺任何一環,LED 都不會亮。接好後先別急著接 USB,對照下面的接線表再檢查一次。",
)

I_MA = (bb.UNO_VCC - bb.LED_C["red"][3]) / 220.0 * 1000.0
assert abs(I_MA - 13.6) < 0.1

# ------------------------------------------------------------------ 程式(頁面上顯示的就是被編譯驗證的這一份)
CODE = """// 第 3 篇:外接 LED 閃爍
const int LED_PIN = {pin};   // LED 接在哪個腳位(用名字代替數字,之後好改)

void setup() {
  pinMode(LED_PIN, OUTPUT);  // 把這個腳位設成「輸出」:Arduino 要送電壓出去
}

void loop() {
  digitalWrite(LED_PIN, HIGH);  // 輸出 5V:LED 亮
  delay({ms});                  // 等待 {ms} 毫秒(1000 毫秒 = 1 秒)
  digitalWrite(LED_PIN, LOW);   // 輸出 0V:LED 滅
  delay({ms});                  // 再等一次
}
"""
FILL = dict(pin="8", ms="1000")
SKETCHES = [dict(name="led-blink", code=CODE, fill=FILL, circuit=CIRC,
                 sim=dict(seconds=5.2, pin="D8", period_ms=1000, tol_ms=15))]
CIRCUITS = [CIRC]

# ------------------------------------------------------------------ 內容
what = section("what", "LED 有方向,而且一定要配一顆電阻",
  '<div class="panel"><h3>兩個規則,先記住</h3>'
  '<p><b>LED 有方向。</b>LED(發光二極體)只讓電流從<b>長腳(正極,+)</b>流向<b>短腳(負極,−)</b>。插反了不會亮;所以接線時永遠先確認長腳在哪一側。</p>'
  '<p style="margin-bottom:0"><b>LED 一定要串一顆電阻。</b>LED 自己幾乎不會限制電流,Uno 的腳位輸出 5V 時,沒有電阻的話電流會大到可能燒掉 LED,甚至傷到腳位。電阻就像水管上的閥門,把電流壓在安全範圍。</p></div>',
  '<div class="spec">'
  '<div><div class="k">這個電路的電流</div><div class="v">≈ %.1f mA</div></div>'
  '<div><div class="k">Uno 每腳建議上限</div><div class="v">20 mA</div></div>'
  '<div><div class="k">每腳絕對上限(不可超過)</div><div class="v">40 mA</div></div></div>' % I_MA,
  '<p class="sub" style="margin-top:14px;margin-bottom:0">算法:電流 = (電源電壓 − LED 壓降)÷ 電阻 = (5 − 2.0)÷ 220 ≈ 0.0136 A。紅色 LED 的順向壓降約 2 V,這是常見的範例值,實際請以你的 LED 規格為準;第 2 篇會把這個公式講清楚。</p>')

parts = section("parts", "準備這五樣東西",
  table("g3", ["零件", "數量", "怎麼認"], [
    ["Arduino Uno R3 + USB 線", "1", "USB 線是方形(Type-B)那一頭接 Uno。Uno R4 的接線與程式完全相同,只是 USB 接頭和 IDE 設定不同,第 1 篇有說明。"],
    ["麵包板", "1", "任何尺寸都可以,本篇只用最左邊的 10 欄。"],
    ["紅色 LED(5 mm)", "1", "兩隻腳<b>一長一短</b>:長腳是 +,短腳是 −。"],
    ["220Ω 電阻", "1", "四環電阻的色環是<b>紅、紅、棕、金</b>。五環電阻的 220Ω 是紅、紅、黑、黑、棕,認不準就用電錶量。"],
    ["公對公杜邦線", "2", "兩端都是針腳的那種。顏色不影響電路,本篇用橘色與黑色,方便你對照圖。"],
  ]),
  warn("手邊沒有 220Ω 時,330Ω 也可以用(LED 會稍微暗一點,電流約 9 mA)。<b>不要用小於 150Ω 的電阻</b>:電流會逼近 Uno 每腳 20 mA 的建議上限。", "電阻可以換,但別換太小"))

wire = section("wire", "接線:先麵包板、後 Arduino,一次一步",
  '<p class="sub" style="margin-bottom:14px">麵包板的規則只有一條:<b>同一欄(同一個數字)的 <code>a–e</code> 五個孔,內部是相通的;<code>f–j</code> 是另一組</b>。所以把兩個零件的腳插在同一欄,它們就接在一起了。</p>',
  bb.stepper_html(CIRC),
  '<div class="linkbox" style="margin-top:12px">點圖上的任何零件,它會亮起橘色光圈,而且在下一節的原理圖裡也會跟著亮。</div>',
  '<p class="sk">圖中的 Uno 轉了 180 度擺放:<b>數位腳位排(0–13、GND)在下緣</b>,朝向麵包板;電源與類比腳位在上緣。圖只畫出麵包板最左邊 16 欄,你的麵包板更長,以欄號與 a–j 為準(手機上可以左右滑動圖);各廠牌字母與數字印刷的位置可能不同,但「同欄 5 孔相通」的規則一樣。</p>',
  '<h3 style="margin-top:26px">接線表(跟著圖對一遍)</h3>',
  bb.wiring_table(CIRC),
  warn("<b>接線時 USB 要拔掉。</b>先在麵包板上放好零件,最後才接 Arduino 的線;確認沒問題才插 USB。這樣萬一線插錯,不會有電流經過。"))

sch_svg, sch_legend = bb.schematic_svg(CIRC)
sch = section("sch", "原理圖:同一個電路的另一種畫法",
  '<p class="sub" style="margin-bottom:16px">原理圖不管零件長什麼樣子,只畫「誰接到誰」,是電子電路共通的語言。上面的接線圖是「照著插」,原理圖是「看懂它」。以後每次出現新符號,我都會標上<span class="newsym">新符號</span>。</p>',
  canvas(sch_svg, [(n, '<span class="newsym">新符號</span>' + t) for n, t in sch_legend]),
  '<div class="linkbox" id="linkInfo" style="margin-top:12px">點原理圖裡的電阻、LED(或上面接線圖裡的零件),看它在另一張圖裡是哪個東西。</div>',
  '<p style="margin-top:14px">兩張圖說的是同一件事:<b>8 號腳 → 電阻 → LED 的 A(正極)→ LED 的 K(負極)→ GND</b>。電流只會順著這個方向流,所以 LED 的方向很重要。</p>')

fillsec = section("fill", "先填入你的腳位與間隔,下面的程式會自動換成你的版本",
  fill([("pin", "LED 接的腳位(2–13)", True), ("ms", "閃爍間隔(毫秒)", True)]),
  '<p class="sk">空白時用範例值(8 號腳、1000 毫秒)。如果你把腳位改成別的數字,<b>橘色那條線也要改插 Uno 對應的腳</b>,接線和程式必須一致。不要用 0 和 1 號腳,它們留給 USB 通訊使用。</p>')

S = steps(
  step(1, "對照檢查接線,然後接上 USB",
       "動手前最後一次檢查。接線錯誤是 LED 不亮最常見的原因,比程式錯更常見。",
       ops(["電阻:<code>b5</code> ↔ <code>b9</code>。",
            "LED:長腳在 <code>d9</code>、短腳在 <code>d10</code>(長腳靠近電阻那一側)。",
            "橘線:Uno 8 號腳 ↔ <code>a5</code>;黑線:Uno GND ↔ <code>a10</code>。",
            "沒有兩隻零件腳或兩條導線擠在同一個孔,也沒有任何金屬腳碰在一起。"]),
       "<p>確認後,用 USB 線把 Uno 接到電腦。Uno 的電源燈(標示 ON 的小燈)會亮。此時 LED 還不會閃,因為程式還沒寫進去。</p>"),
  step(2, "開新草稿碼,貼上程式",
       "Arduino 把程式叫做「草稿碼(sketch)」。我們要從空白的開始。",
       ops(["打開 Arduino IDE。選單 <b>File → New Sketch</b>。",
            "編輯區裡有預設的 <code>setup()</code> 與 <code>loop()</code>,用 <code>Ctrl + A</code> 全選後刪掉。",
            "按下面程式右上角的 <b>Copy</b>,貼進編輯區(<code>Ctrl + V</code>)。"]),
       cmd(CODE, cap="Arduino 程式(會依你上面填的值更新)", cpp=True),
       tip("程式裡 <code>//</code> 後面是註解,給人看的,Arduino 不會執行。貼上時有沒有註解都可以。")),
  step(3, "選擇板子與連接埠",
       "IDE 要知道你用的是哪一種板子、接在電腦的哪個埠,才知道把程式送到哪裡。",
       ops(["看視窗上方工具列,<b>勾號(Verify)與右箭頭(Upload)旁邊有一個下拉選單</b>。Uno 接好後,通常會自動顯示 <b>Arduino Uno</b> 與一個 COM 埠,例如 <code>COM3</code>。",
            "如果沒有自動出現:點下拉選單,選 <b>Select other board and port…</b>,或用選單 <b>Tools → Board → Arduino AVR Boards → Arduino Uno</b>,再用 <b>Tools → Port</b> 選後面標有 <code>(Arduino Uno)</code> 的那個 COM 埠。"]),
       see("下拉選單顯示 <code>Arduino Uno</code>,連接埠旁邊寫著 <code>COM 數字</code>。"),
       warn("Port 選單是灰的或找不到 Uno:先換一條 USB 線(有些線只能充電,不能傳資料),再換一個 USB 孔。相容板如果仍抓不到,可能需要裝 CH340 驅動,第 1 篇與第 19 篇會詳細說明。")),
  step(4, "先驗證,再上傳",
       "「驗證」只檢查程式有沒有寫錯、能不能編譯,不會動到板子。養成先驗證的習慣,出錯時比較好找原因。",
       ops(["按工具列左邊的<b>勾號(Verify)</b>,等下方輸出視窗跑完,沒有紅字錯誤就可以。",
            "按旁邊的<b>右箭頭(Upload)</b>。IDE 會再編譯一次,然後把程式送進 Uno。上傳期間,Uno 上的 TX、RX 小燈會快速閃爍。"]),
       see("輸出視窗結尾出現上傳完成的提示(Done uploading)。")),
  step(5, "看 LED 閃爍",
       "上傳完成後,Uno 會立刻開始執行程式,不需要再按任何東西。",
       see("麵包板上的紅色 LED <b>亮 1 秒、滅 1 秒</b>,不斷重複。Uno 板子上自己的 L 燈<b>不會</b>閃,因為它接在 13 號腳,而我們用的是 8 號腳。"),
       tip("把 USB 拔掉再插上,或按 Uno 上的 Reset 小按鈕,程式會從頭再跑一次。程式存在 Uno 裡,拔掉電源也不會消失。"),
       warn("LED 完全不亮?先不要急著改程式,到下面「常見卡關」照順序檢查,九成是接線的問題。")))

CODE_TABLE = table("g2", ["這一行", "它在做什麼"], [
  ["<code>const int LED_PIN = 8;</code>", "宣告一個叫 <code>LED_PIN</code> 的<b>整數常數</b>,值是 8。用名字代替數字,以後換腳位只要改這一行。<code>const</code> 表示它不會被改變。行尾的分號 <code>;</code> 不能少。"],
  ["<code>void setup() { … }</code>", "<b>開機或按 Reset 後,只執行一次</b>。放「準備工作」。大括號 <code>{ }</code> 圈住這個區塊的內容。"],
  ["<code>pinMode(LED_PIN, OUTPUT);</code>", "設定腳位的模式。<code>OUTPUT</code> 表示輸出:由 Arduino 決定這隻腳的電壓。忘了這行,LED 會很暗(見常見卡關)。"],
  ["<code>void loop() { … }</code>", "<code>setup()</code> 跑完之後,<b>一直重複執行</b>,直到斷電。"],
  ["<code>digitalWrite(LED_PIN, HIGH);</code>", "輸出<b>高電位(5V)</b>。電流從 8 號腳出發,經過電阻、LED,流回 GND,LED 亮。<code>HIGH</code> 要全大寫。"],
  ["<code>delay(1000);</code>", "<b>暫停 1000 毫秒</b>(1 秒)。這段時間程式什麼都不做,LED 維持現在的狀態。"],
  ["<code>digitalWrite(LED_PIN, LOW);</code>", "輸出<b>低電位(0V)</b>。LED 兩端沒有電壓差,所以熄滅。"],
])
code = section("code", "逐行看懂這支程式", CODE_TABLE,
  '<p style="margin-top:14px"><b>執行順序</b>:開機 → <code>setup()</code> 一次 → <code>loop()</code> 從上到下 → 跑到最後一行,回到 <code>loop()</code> 第一行 → 一直重複。LED 就是在這個圈裡被不斷開、關。</p>')

try_ = section("try", "改改看:三個小挑戰",
  '<p class="sub" style="margin-bottom:14px">只改數字,不改接線。每次改完按 Upload,看 LED 的變化。</p>',
  table("g3", ["挑戰", "怎麼改", "你會看到"], [
    ["快閃", "把兩個 <code>delay</code> 都改成 <code>200</code>", "LED 一秒閃約 2.5 次。"],
    ["心跳", "第一個 <code>delay</code> 改 <code>100</code>,第二個改 <code>900</code>", "短短亮一下,然後暗很久,像心跳或警示燈。"],
    ["快到看不出", "兩個 <code>delay</code> 都改成 <code>10</code>", "LED 看起來是一直亮著(只是比較暗),因為眼睛跟不上這麼快的閃爍。這是下一篇 PWM 呼吸燈的原理。"],
  ]),
  tip("<code>delay</code> 的單位是毫秒,不要寫成 <code>delay(1.5)</code> 之類的小數:它只接受整數。想要 1.5 秒就寫 <code>delay(1500)</code>。"))

gotchas = section("gotchas", "常見卡關(照順序檢查)",
  details("LED 完全不亮",
    "<p>九成是接線。由最常見的開始檢查:</p>" +
    ops(["<b>LED 插反了</b>:長腳(+)要在靠近電阻、也就是 <code>d9</code> 的那一側。拔出來,轉 180 度再插回去。",
         "<b>零件沒有插在同一欄</b>:電阻右腳與 LED 長腳必須同一欄(第 9 欄),橘線與電阻左腳同一欄(第 5 欄)。",
         "<b>GND 線沒接好</b>:黑線的另一端要插在 LED 短腳同一欄(第 10 欄)。",
         "<b>腳位和程式不一致</b>:橘線插的是 8 號腳,程式裡 <code>LED_PIN</code> 就必須是 8。",
         "<b>程式其實沒有上傳成功</b>:看輸出視窗有沒有上傳完成的提示。"]), True) +
  details("LED 亮了,但很暗、而且一直不閃",
    "<p>如果程式裡<b>少了 <code>pinMode(LED_PIN, OUTPUT);</code></b>,腳位預設是輸入。這時呼叫 <code>digitalWrite(…, HIGH)</code> 只會開啟內部的上拉電阻,LED 會微微地亮,看起來像很暗。補上 <code>pinMode</code> 就恢復正常。</p>") +
  details("LED 亮得很暗,但程式沒問題",
    "<p>先看電阻色環。<b>紅、紅、棕</b>是 220Ω;<b>紅、紅、黃</b>是 220kΩ(多了一千倍),電流小到幾乎不亮。把電阻拿起來對照色環,或用第 2 篇的色環計算機。</p>") +
  details("驗證時出現紅字錯誤",
    "<p>IDE 會在輸出視窗指出是第幾行。新手最常見的三種:</p>" +
    table("g2", ["訊息大意", "原因"], [
      ["<code>expected ';' before …</code>", "上一行結尾少了分號 <code>;</code>。"],
      ["<code>'digitalwrite' was not declared in this scope</code>", "大小寫打錯。Arduino 區分大小寫,正確是 <code>digitalWrite</code>,<code>HIGH</code>、<code>OUTPUT</code> 也要全大寫。"],
      ["<code>expected '}' at end of input</code>", "大括號 <code>{ }</code> 沒有成對。每個 <code>{</code> 都要有對應的 <code>}</code>。"],
    ])) +
  details("上傳失敗,或 Port 選單是灰的",
    "<p>先換一條 USB 線(有些線只能充電),再換一個 USB 孔,然後重新打開 IDE。相容板抓不到 COM 埠,多半要裝 CH340 驅動;第 1 篇的安裝章節與第 19 篇的決策選擇器會一步一步帶你排查。</p>") +
  details("我想把 LED 換到別的腳位",
    "<p>兩邊要一起改:<b>接線</b>(橘線從 Uno 8 號腳換到新腳位,另一端不動)與<b>程式</b>(上面填入表單裡的腳位數字)。只改其中一邊,LED 不會亮。</p>"))

SIM = {
  "a1": "<b>不用。</b>IDE 沒有問題才能上傳成功,重新安裝是最後一步,不是第一步。先檢查你最容易出錯的地方。",
  "a2": "<b>對。</b>LED 方向是最常見的錯誤:長腳要靠近電阻(+),短腳那一欄要有黑線接到 GND。接著再檢查零件有沒有插在同一欄、橘線是不是 8 號腳。",
  "a3": "<b>千萬不要。</b>電阻是用來保護 LED 與腳位的,拿掉之後電流可能超過 Uno 每腳 40 mA 的上限,損壞 LED 或腳位。LED 不亮的原因要找出來,不是把保護拿掉。",
}
QUIZ = quiz_cfg([
  ("紅色 LED 的長腳應該接在哪一側?", ["靠近電阻、訊號端(正極 +)那一側", "靠近 GND 的那一側", "哪一側都可以"], 0,
   "長腳是正極(+),電流從這裡進去,由短腳(−)流向 GND。"),
  ("為什麼 LED 前面要串一顆電阻?", ["讓 LED 更亮", "限制電流,避免燒壞 LED 或腳位", "讓程式跑得更快"], 1,
   "LED 自己不限流,電阻把電流限制在安全範圍(這個電路約 13.6 mA)。"),
  ("<code>pinMode(8, OUTPUT);</code> 在做什麼?", ["讓 8 號腳輸出 5V", "把 8 號腳設成輸出模式,之後才能用 digitalWrite 控制它", "讀取 8 號腳的電壓"], 1,
   "pinMode 只設定模式;真正輸出電壓的是之後的 digitalWrite。"),
  ("<code>delay(500);</code> 會讓程式暫停多久?", ["500 秒", "0.5 秒", "5 秒"], 1,
   "delay 的單位是毫秒,500 毫秒 = 0.5 秒。"),
  ("麵包板同一欄的 <code>a、b、c、d、e</code> 五個孔是什麼關係?", ["彼此不相通", "內部相通,等於接在一起", "只有 a 和 e 相通"], 1,
   "同一欄 a–e 內部相通;f–j 另一組。這是用麵包板接線的基本規則。"),
])

practice = section("practice", "動手演練:確認你真的懂了",
  '<p class="sub" style="margin-bottom:18px">先選答案再看原因。目的是練習「LED 不亮時先查哪裡」,而不是背指令。</p>',
  sim("", "情境:程式上傳成功了,但 LED 完全不亮", "你下一步應該怎麼做?",
      [("a1", "重新安裝 Arduino IDE"), ("a2", "檢查 LED 的長短腳方向與各條線有沒有插在同一欄"), ("a3", "把電阻拿掉,讓電流大一點")]),
  QUIZ_HTML,
  checks(["我接線前先拔掉了 USB,確認後才接上。",
          "我知道 LED 長腳是正極(+),要靠近電阻、訊號端那一側。",
          "我知道電阻的作用是限制電流,不能省。",
          "我知道麵包板同一欄 <code>a–e</code> 內部相通。",
          "我看得懂 <code>setup()</code> 只跑一次、<code>loop()</code> 一直重複。",
          "我知道換腳位時,接線與程式兩邊都要改。",
          "我能在原理圖上指出電阻、LED、GND 三個符號。"], "做完之後,對照這張清單"),
  resources([
    ("https://docs.arduino.cc/built-in-examples/basics/Blink/", "Blink 內建範例", "Blink (built-in example)"),
    ("https://docs.arduino.cc/language-reference/en/functions/digital-io/digitalwrite/", "digitalWrite()", "Arduino language reference"),
    ("https://docs.arduino.cc/language-reference/en/functions/digital-io/pinmode/", "pinMode()", "Arduino language reference"),
    ("https://docs.arduino.cc/language-reference/en/functions/time/delay/", "delay()", "Arduino language reference"),
    ("https://support.arduino.cc/hc/en-us/articles/4733418441116-Upload-a-sketch-in-Arduino-IDE", "在 Arduino IDE 上傳草稿碼", "Upload a sketch in Arduino IDE"),
  ], "Arduino 官方文件"))

SPEC = dict(
    dir="arduino",
    file="arduino-led-guide.html",
    title="外接 LED 閃爍:第一次接線與第一個程式",
    eyebrow="第 3 篇 · 外接 LED",
    h1="用一顆電阻和一顆 LED,讓你自己接的燈閃起來",
    sub="第一次把線接在麵包板上,第一次寫控制外部零件的程式。每一步先說明為什麼,再告訴你插哪個孔、會看到什麼。",
    tldr="<strong>先拔掉 USB,再接線</strong>:Uno 8 號腳 → 220Ω 電阻 → LED 長腳(+),LED 短腳(−)→ GND。程式用 <code>pinMode</code> 把 8 號腳設為輸出,再用 <code>digitalWrite</code> 與 <code>delay</code> 讓它每秒開關一次。",
    toc=[("what", "LED 與電阻"), ("parts", "零件"), ("wire", "接線"), ("sch", "原理圖"), ("fill", "填入你的資料"),
         ("steps", "五個步驟"), ("code", "逐行看程式"), ("try", "改改看"), ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
    body="\n\n".join([what, parts, wire, sch, fillsec, section("steps", "照著做:五個步驟", S), code, try_, gotchas, practice]),
    config=dict(fill=FILL, sim=SIM, quiz=QUIZ,
                wiring=[bb.wiring_config(CIRC)], parts=bb.parts_info(CIRC)),
    prev=("arduino-electric-guide.html", "電與麵包板基礎"),
    next=("arduino-loop-guide.html", "變數、for 與陣列:跑馬燈"),
)
