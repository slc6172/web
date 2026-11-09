# -*- coding: utf-8 -*-
from h import *
import bb

CIRC = bb.Circuit(
    "pot-led", 22,
    parts=[
        bb.Pot("POT1", "d5", "d6", "d7", 1),
        bb.Resistor("R1", 220, "b11", "b15", 2), bb.LED("LED1", "red", "d15", "d16", 2),
        bb.Wire("P1", "a5", "t+5", "red", 3, route="straight"), bb.Wire("P2", "a7", "t-7", "black", 3, route="straight"),
        bb.Wire("K1", "a16", "t-16", "black", 3, route="straight"),
        bb.Wire("SA", "UNO.A0", "a6", "green", 4, route="left"), bb.Wire("S1", "UNO.D9", "a11", "blue", 4),
        bb.Wire("V5", "UNO.5V", "t+1", "red", 5, route="left1"), bb.Wire("G", "UNO.GND", "t-20", "black", 5),
    ],
    steps=[
        ("放電位器", "電位器有<b>三隻腳</b>,排成一排:<code>d5</code>(左外側)、<code>d6</code>(<b>中間腳,滑動腳</b>)、<code>d7</code>(右外側)。<br>旋鈕朝向你,腳垂直下壓到底。"),
        ("放電阻與 LED", "<b>電阻</b>橫放在 <code>b11–b15</code>;<b>紅色 LED</b>長腳(+)插 <code>d15</code>、短腳(−)插 <code>d16</code>。LED 要接在有 <code>~</code> 的 <b>9 號腳</b>。"),
        ("三條短線:電位器兩端與 LED 負極", "① 紅色短線 <code>a5</code> → <code>t+5</code>:電位器左外側腳接 + 軌(5V)。<br>② 黑色短線 <code>a7</code> → <code>t-7</code>:右外側腳接 − 軌(GND)。<br>③ 黑色短線 <code>a16</code> → <code>t-16</code>:LED 負極接 − 軌。"),
        ("兩條訊號線:A0 與 9 號腳", "綠線:Uno <b>A0</b>(電源腳位排,Uno 上緣)→ <code>a6</code>,也就是電位器的<b>中間腳</b>。<br>藍線:Uno <b>9 號腳</b> → <code>a11</code>(電阻左端)。<br>A0 是「類比輸入」腳位,能讀 0–5 V 之間的電壓大小。"),
        ("電源線:5V 與 GND", "紅線:Uno <b>5V</b> → <code>t+1</code>(+ 軌)。<br>黑線:Uno 數位腳位排的 <b>GND</b> → <code>t-20</code>(− 軌)。"),
    ],
    chains=[["UNO.5V", "POT1.1"], ["POT1.W", "UNO.A0"], ["POT1.2", "UNO.GND"], ["UNO.D9", "R1", "LED1", "UNO.GND"]],
    intro="先<strong>拔掉 USB 線</strong>。這次的重點是電位器:它的<b>兩個外側腳</b>接 5V 與 GND,<b>中間腳</b>接 Uno 的 A0。LED 接 9 號腳(PWM),之後旋鈕要控制它的亮度。",
    done="電位器兩端分別接 5V 與 GND,中間腳接 A0;LED 組接 9 號腳。5V 與 GND 兩條線絕對不能互碰。檢查:電位器的三隻腳在三個不同的欄。",
)
CIRCUITS = [CIRC]

P1 = """// 第 9 篇:讀電位器,印出數值(0–1023)
const int POT_PIN = A0;        // 電位器的中間腳接在 A0

void setup() {
  Serial.begin(9600);
}

void loop() {
  int value = analogRead(POT_PIN);   // 讀取 A0 的電壓:0 V → 0,5 V → 1023
  Serial.println(value);
  delay({gap});
}
"""
P2 = """// 第 9 篇:旋鈕控制 LED 亮度
const int POT_PIN = A0;
const int LED_PIN = 9;          // 要用有 ~ 的腳位

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  int value = analogRead(POT_PIN);                  // 0–1023
  int brightness = map(value, 0, 1023, 0, 255);     // 換算成 0–255
  analogWrite(LED_PIN, brightness);                 // 用 PWM 輸出
}
"""
P3 = """// 第 9 篇:把數值換算成電壓,同時印出兩者
const int POT_PIN = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int value = analogRead(POT_PIN);
  float volts = value * 5.0 / 1023.0;    // 換算成伏特(5.0 要寫成小數,結果才會有小數)
  Serial.print("value = ");
  Serial.print(value);
  Serial.print("  voltage = ");
  Serial.println(volts);
  delay({gap});
}
"""
P4 = """// 挑戰:旋鈕控制閃爍速度
const int POT_PIN = A0;
const int LED_PIN = 9;

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  int wait = analogRead(POT_PIN);   // 0–1023 毫秒
  digitalWrite(LED_PIN, HIGH);
  delay(wait);
  digitalWrite(LED_PIN, LOW);
  delay(wait);
}
"""
FILL = dict(gap="500")
SKETCHES = [
    dict(name="pot-read", code=P1, fill=FILL, circuit=CIRC, code_pins={"LED_PIN": "UNO.D9"} if False else {},
         sim=dict(kind="uart", seconds=1.7, adc=[(0, 0, 0), (0, 2500, 400), (0, 5000, 1100)], expect=["0\r\n", "511\r\n", "1023\r\n"])),
    dict(name="pot-led", code=P2, fill=FILL, circuit=CIRC, code_pins={"LED_PIN": "UNO.D9"},
         sim=dict(kind="adc_pwm", seconds=1.5, adc=[(0, 1000, 0), (0, 2500, 500), (0, 4000, 1000)], addr=0x88, note="1000、2500、4000 mV",
                  expect=[(300, 51), (800, 127), (1300, 203)], tol=3)),
    dict(name="pot-volts", code=P3, fill=FILL,
         sim=dict(kind="uart", seconds=1.2, adc=[(0, 2500, 0)], expect=["value = 511  voltage = 2.50\r\n"])),
    dict(name="pot-speed", code=P4, fill=FILL, circuit=CIRC, code_pins={"LED_PIN": "UNO.D9"},
         sim=dict(kind="adc_toggle", pin="D9", seconds=3.3, adc=[(0, 2000, 0)], period_ms=409, tol_ms=15, note="2000 mV → wait = 409")),
]

# ---------------------------------------------------------------- 原理圖(電位器分壓 + LED)
def pot_schematic():
    G7, CL, SL = bb.GRAY7, bb.CLAY, bb.SLATE
    o = []
    o.append('<g class="el" data-part="POT1" tabindex="0" role="button" aria-label="電位器 POT1,點一下看它在麵包板上的位置">'
             '<rect class="halo" x="72" y="48" width="170" height="104" rx="10" fill="none" stroke="%s" stroke-width="2.5"/>'
             '<rect x="72" y="48" width="170" height="104" rx="10" fill="#FFFFFF" opacity="0.001"/>' % CL)
    # 5V
    o.append('<line x1="100" y1="22" x2="136" y2="22" stroke="%s" stroke-width="2.4" stroke-linecap="round"/><text x="118" y="16" class="mb" fill="%s" text-anchor="middle">5V</text>' % (G7, bb.RUST))
    o.append('<line x1="118" y1="22" x2="118" y2="54" stroke="%s" stroke-width="2"/>' % G7)
    o.append('<polyline points="118,54 118,60 106,66 130,78 106,90 130,102 106,114 130,126 118,132 118,140" fill="none" stroke="%s" stroke-width="2" stroke-linejoin="round"/>' % G7)
    # 滑動腳箭頭
    o.append('<line x1="210" y1="96" x2="136" y2="96" stroke="%s" stroke-width="2"/><polygon points="136,96 146,90 146,102" fill="%s"/>' % (G7, G7))
    o.append('<text x="214" y="86" class="m" fill="%s">W 滑動腳</text>' % bb.GRAY5)
    o.append('<text x="30" y="100" class="mb" fill="%s">POT1</text><text x="30" y="114" class="m" fill="%s">10kΩ</text>' % (SL, bb.GRAY5))
    o.append('</g>')
    o.append('<line x1="210" y1="96" x2="290" y2="96" stroke="%s" stroke-width="2"/>' % G7)
    o.append('<rect x="290" y="81" width="80" height="30" rx="8" fill="#F0EEE6" stroke="%s" stroke-width="1.5"/><text x="330" y="100" class="mb" fill="%s" text-anchor="middle">Uno A0</text>' % (G7, SL))
    o.append('<line x1="118" y1="140" x2="118" y2="168" stroke="%s" stroke-width="2"/>' % G7)
    for k, wd in enumerate((30, 20, 10)):
        yy = 168 + k * 7
        o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.2" stroke-linecap="round"/>' % (118 - wd / 2, yy, 118 + wd / 2, yy, G7))
    o.append('<text x="118" y="200" class="s" fill="%s" text-anchor="middle">GND</text>' % bb.GRAY5)
    o.append('<circle cx="372" cy="118" r="0" fill="none"/>')
    note = '<circle cx="46" cy="60" r="10" fill="%s"/><text x="46" y="63.5" class="mb" fill="#FFFFFF" text-anchor="middle">1</text>' % CL
    return ('<svg viewBox="0 0 420 220" role="img" aria-label="電位器分壓原理圖" style="min-width:420px"><defs>%s</defs><rect width="420" height="220" fill="#FFFFFF"/>%s%s</svg>'
            % (bb.STYLE, "".join(o), note))

led_only = bb.Circuit("led9", 22, parts=CIRC.parts, steps=CIRC.steps, chains=[["UNO.D9", "R1", "LED1", "UNO.GND"]])
LED_SCH, LED_LEG = bb.schematic_svg(led_only, mark=())

potsim = ('<div class="panel" data-potsim><div class="wgrid f2"><div><label>旋鈕轉到(0% = 全部轉向 GND 端,100% = 轉向 5V 端)</label><input type="range" min="0" max="100" value="50" data-pot="v"></div>'
          '<div><label>LED 亮度(map 之後)</label><span class="pwm-led" style="margin:6px 0 0"></span></div></div>'
          '<div class="pot-bar" aria-hidden="true"><span></span></div>'
          '<div class="rc-out pot-out" aria-live="polite"></div></div>')

what = section("what", "類比輸入:讀「多少」,不只是「有沒有」",
  '<p class="sub" style="margin-bottom:14px">按鈕只有兩種狀態:HIGH 或 LOW。但現實世界的很多東西是「連續」的:旋鈕轉了多少、光有多亮、溫度多高。Arduino 用<b>類比輸入</b>來讀這些。</p>',
  '<div class="panel"><h3>三個關鍵</h3>'
  '<ul style="margin:0;padding-left:20px"><li><b>類比輸入腳位 A0–A5</b>:可以量 0–5 V 之間<b>任意大小</b>的電壓。</li>'
  '<li><b>ADC(類比數位轉換器)</b>把電壓換成數字:<b>0 V → 0,5 V → 1023</b>(共 1024 級,即 10 位元)。每一級約 4.9 mV。</li>'
  '<li><b><code>analogRead(A0)</code></b>:讀出 A0 的數字,0–1023。</li></ul></div>',
  '<h3 style="margin-top:26px">電位器:能轉動的可變電阻</h3>',
  '<p>電位器有<b>三隻腳</b>。兩個外側腳之間是一整條固定的電阻(這顆是 10 kΩ),<b>中間腳</b>(滑動腳)隨旋鈕在這條電阻上移動。旋鈕轉到哪裡,中間腳就把這條電阻<b>分成上下兩段</b>:</p>',
  '<p><b>分壓:</b>兩端接 5V 與 GND 時,中間腳的電壓 = 5 V × (下段電阻 ÷ 總電阻)。旋鈕轉一圈,中間腳就從 0 V 平順地變到 5 V。拖拖看:</p>',
  potsim,
  tip("A0 腳位量的是「中間腳的電壓」,所以<b>中間腳必須接 A0</b>。兩個外側腳一個接 5V、一個接 GND,哪邊接哪邊只會影響旋轉方向,不會影響能不能用。"))

sch_svg, _ = bb.schematic_svg(CIRC, mark=()) if False else (None, None)
wire = section("wire", "接線:電位器(A0)加 LED(9 號腳)",
  '<p class="sub" style="margin-bottom:14px">電位器兩端接 5V 與 GND,中間腳接 A0;LED 接 9 號腳(有 <code>~</code>,能做 PWM)。</p>',
  bb.stepper_html(CIRC),
  '<p class="sk">Uno 轉了 180 度擺放:電源腳位與類比腳位(A0–A5、5V…)在上緣,數位腳位在下緣。<b>A0 與 5V 兩條線要繞過 Uno 的左邊</b>,才接得到麵包板。圖只畫左邊 22 欄,以欄號與 a–j 為準(手機上可以左右滑動圖)。</p>',
  '<h3 style="margin-top:26px">接線表</h3>', bb.wiring_table(CIRC),
  warn("<b>5V 與 GND 兩條線不能碰在一起。</b>電位器兩個外側腳分別接 + 軌與 − 軌,中間腳接 A0;<b>不要把中間腳接到外側的欄</b>。接線前先拔 USB。", "注意"),
  '<h3 style="margin-top:26px">原理圖</h3>',
  '<p class="sub">電位器的符號是<b>電阻加一個指向它中間的箭頭</b>(滑動腳),分成上下兩段。</p>',
  canvas(pot_schematic(), [("1", '<span class="newsym">新符號</span><b>電位器</b>:鋸齒電阻加一個箭頭。上端接 5V、下端接 GND,箭頭那條線(中間腳)接 Uno 的 A0。')]),
  '<div class="linkbox" id="linkInfo" style="margin-top:12px">點電位器,看它在麵包板上是哪一個。</div>',
  '<h3 style="margin-top:18px">LED 這一組(和之前一樣)</h3>',
  canvas(LED_SCH, []))

fillsec = section("fill", "先填入印數字的間隔",
  fill([("gap", "每一行之間的間隔(毫秒)", True)]),
  '<p class="sk">空白時用範例值 500 毫秒。</p>')

def exp(items):
    return table("g2", ["這一行", "它在做什麼"], items)

code1 = section("code1", "程式一:讀電位器,印出數字",
  cmd(P1, cap="讀 A0,印出 0–1023", cpp=True),
  exp([
    ["<code>const int POT_PIN = A0;</code>", "A0 是類比腳位的名字,可以直接當數字用。"],
    ["<code>analogRead(POT_PIN)</code>", "讀出電壓並轉成數字:<b>0–1023</b>。<b>不需要 <code>pinMode</code></b>,類比輸入腳位預設就是輸入。"],
  ]),
  steps(step(1, "上傳,打開 Serial Monitor(baud 9600)", "第 8 篇學過。"),
        step(2, "慢慢轉動旋鈕", "看數字變化。", see("轉到一端約 <b>0</b>,另一端約 <b>1023</b>,中間約 <b>512</b>。旋轉越慢,數字變化越平順。"))),
  '<h3 style="margin-top:22px">換算成電壓</h3>',
  cmd(P3, cap="同時印出數值與電壓", cpp=True),
  exp([
    ["<code>float volts = value * 5.0 / 1023.0;</code>", "數值 ÷ 1023 再乘 5,就是電壓。<code>float</code> 是帶小數的變數;<b>5.0 與 1023.0 要寫小數點</b>,否則整數除法會把小數吃掉。"],
    ["<code>Serial.print(...)</code> 連續幾次", "前面都用 <code>print</code>(不換行),最後一個用 <code>println</code>,同一行就印出數值和電壓。"],
  ]),
  tip("打開 <b>Serial Plotter</b>(第 8 篇)看程式一,旋鈕的變化會畫成一條曲線。"))

code2 = section("code2", "程式二:旋鈕控制 LED 亮度",
  cmd(P2, cap="電位器 → map() → analogWrite", cpp=True),
  exp([
    ["<code>int value = analogRead(POT_PIN);</code>", "讀出 0–1023。"],
    ["<code>map(value, 0, 1023, 0, 255)</code>", "<b>把一個範圍的數字,對應到另一個範圍</b>。這裡把 0–1023 換成 0–255(<code>analogWrite</code> 能接受的範圍)。"],
    ["<code>analogWrite(LED_PIN, brightness);</code>", "用 PWM 輸出亮度(第 6 篇)。"],
  ]),
  table("g3", ["map 的五個參數", "意思", "這裡的值"], [
    ["第 1 個", "要換算的數字", "<code>value</code>"], ["第 2、3 個", "原本的範圍(最小、最大)", "<code>0, 1023</code>"], ["第 4、5 個", "想換成的範圍(最小、最大)", "<code>0, 255</code>"],
  ]),
  see("<b>旋鈕轉到一端,LED 全暗;轉到另一端,LED 全亮</b>,中間漸漸變化。如果方向和你想的相反,把電位器兩個外側腳對調(或把 <code>map</code> 後面的 <code>0, 255</code> 改成 <code>255, 0</code>)。"),
  warn("<code>map()</code> 只處理<b>整數</b>,結果會直接捨去小數,而且<b>不會</b>限制數字不超出範圍。輸入的數字要在原本範圍內。", "注意"))

try_ = section("try", "改改看",
  table("g3", ["挑戰", "怎麼改", "你會看到"], [
    ["反方向", "<code>map(value, 0, 1023, 255, 0)</code>", "旋鈕轉向另一端時 LED 才變亮。"],
    ["控制閃爍速度", "改用下面的挑戰程式", "旋鈕轉到最小,LED 飛快閃;轉到最大,每次約 1 秒。"],
    ["只用一半範圍", "<code>map(value, 0, 1023, 0, 100)</code>", "LED 永遠不會全亮,最亮只有約 40%。"],
  ]),
  details("挑戰:旋鈕控制閃爍速度",
    cmd(P4, cap="挑戰:旋鈕決定 delay 多久", cpp=True) + '<p style="margin:12px 0 0">不需要 <code>map</code>:0–1023 剛好可以直接當成 0–1023 毫秒的 <code>delay</code>。轉到 0 時 <code>delay(0)</code> 閃得很快,肉眼看起來像一直亮。</p>'))

gotchas = section("gotchas", "常見卡關",
  details("數字固定是 0,或固定是 1023",
    ops(["<b>中間腳沒接到 A0</b>,或接到了外側欄。三隻腳要在三個不同的欄,A0 的線接在中間那一欄。", "<b>兩個外側腳都接 5V,或都接 GND</b>:一端接 5V、另一端接 GND。", "電位器的腳沒插到底。"]), True) +
  details("數字亂跳,不隨旋鈕變化",
    "<p>A0 沒接任何東西(<b>浮接</b>)時,讀到的是雜訊。檢查中間腳的綠線是否真的接在電位器中間腳的那一欄。</p>") +
  details("數字有變化,但 LED 亮度沒有漸變",
    "<p>LED 沒接在有 <code>~</code> 的腳位(第 6 篇)。確認接 9 號腳,而且程式的 <code>LED_PIN</code> 是 9。</p>") +
  details("旋轉方向和我想的相反",
    "<p>不是錯誤:兩個外側腳對調,方向就會顛倒。或在程式裡把 <code>map</code> 的輸出範圍反過來。</p>") +
  details("數字最大只到 1000 多,或最小不是 0",
    "<p>正常。電位器與 ADC 都有一點誤差,範圍可能是 3–1020。不需要為此煩惱。</p>"))

SIM = {
  "a1": "<b>不用。</b>固定在 0 表示 A0 一直接近 0 V,這是接線問題,不是程式問題。",
  "a2": "<b>對。</b>先檢查<b>中間腳</b>:A0 的線必須接在電位器的中間腳所在的欄,兩個外側腳一端接 5V、一端接 GND。接錯的話,A0 會固定在 0 或 5 V。",
  "a3": "<b>沒有用。</b>電阻不影響電位器中間腳的分壓結果。",
}
QUIZ = quiz_cfg([
  ("<code>analogRead(A0)</code> 回傳的範圍是?", ["0–255", "0–1023", "0–5"], 1,
   "10 位元 ADC,0 V 對應 0,5 V 對應 1023。"),
  ("電位器的哪一隻腳接 A0?", ["左外側腳", "中間腳(滑動腳)", "右外側腳"], 1,
   "中間腳的電壓隨旋鈕改變,A0 量的就是它。"),
  ("<code>map(512, 0, 1023, 0, 255)</code> 大約等於?", ["127", "255", "512"], 0,
   "512 約在 0–1023 的一半,換成 0–255 就約 127。"),
  ("要把 analogRead 的值換成電壓(伏特),可以?", ["value * 5.0 / 1023.0", "value / 5", "value * 255"], 0,
   "電壓 = 數值 ÷ 1023 × 5。記得用小數 5.0。"),
  ("為什麼 <code>analogRead</code> 不需要 <code>pinMode</code>?", ["類比輸入腳位預設就是輸入", "它不是輸入", "因為 A0 不是腳位"], 0,
   "A0–A5 預設為輸入,可直接讀。"),
])
practice = section("practice", "動手演練與延伸閱讀",
  sim("", "情境:Serial Monitor 的數字一直是 0,轉旋鈕也沒變", "你應該先?",
      [("a1", "改寫程式"), ("a2", "檢查電位器中間腳是否接到 A0,外側腳是否一端 5V、一端 GND"), ("a3", "換更大的電阻")]),
  QUIZ_HTML,
  checks(["我能說出 analogRead 會回傳 0–1023,0 V 是 0、5 V 是 1023。",
          "我知道電位器三隻腳各自接哪裡:兩端 5V 與 GND,中間腳 A0。",
          "我能解釋電位器為什麼能「分壓」。",
          "我的 Serial Monitor 數字會隨旋鈕平順變化。",
          "我的旋鈕能控制 LED 亮度,並知道 <code>map()</code> 做什麼。",
          "我知道 A0 不接東西會讀到雜訊(浮接)。"], "做完之後,對照這張清單"),
  resources([
    ("https://docs.arduino.cc/language-reference/en/functions/analog-io/analogread/", "analogRead()", "Arduino language reference"),
    ("https://docs.arduino.cc/language-reference/en/functions/math/map/", "map()", "Arduino language reference"),
    ("https://docs.arduino.cc/language-reference/en/functions/analog-io/analogwrite/", "analogWrite()", "Arduino language reference"),
  ], "Arduino 官方文件"))

SPEC = dict(
    dir="arduino",
    file="arduino-analog-guide.html",
    title="類比輸入:電位器、分壓與 map()",
    eyebrow="第 9 篇 · 類比輸入",
    h1="轉動旋鈕,讓 Arduino 讀到「多少」",
    sub="學會讀類比電壓:電位器的兩端接 5V 與 GND、中間腳接 A0,用 analogRead 得到 0–1023,再用 map 換成亮度。",
    tldr="<code>analogRead(A0)</code> 把 0–5 V 換成 <strong>0–1023</strong>。電位器<strong>兩端接 5V 與 GND、中間腳接 A0</strong>,中間腳的電壓就是「分壓」。<code>map(值, 0, 1023, 0, 255)</code> 把範圍換成 <code>analogWrite</code> 能用的 0–255。",
    toc=[("what", "類比與分壓"), ("wire", "接線"), ("fill", "填入間隔"), ("code1", "程式一:讀與印"), ("code2", "程式二:控制亮度"),
         ("try", "改改看"), ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
    body="\n\n".join([what, wire, fillsec, code1, code2, try_, gotchas, practice]),
    config=dict(fill=FILL, sim=SIM, quiz=QUIZ, wiring=[bb.wiring_config(CIRC)], parts=bb.parts_info(CIRC)),
    prev=("arduino-serial-guide.html", "Serial Monitor 與除錯"),
    next=("arduino-ldr-guide.html", "光敏電阻小夜燈"),
)
