# -*- coding: utf-8 -*-
from h import *
import bb

CIRC = bb.Circuit(
    "ldr-night", 22,
    parts=[
        bb.LDR("LDR1", "d5", "d7", 1),
        bb.Resistor("R2", 10000, "b7", "b11", 2), bb.Resistor("R1", 220, "b15", "b19", 2), bb.LED("LED1", "red", "d19", "d20", 2),
        bb.Wire("P", "a5", "t+5", "red", 3, route="straight"), bb.Wire("G10", "a11", "t-11", "black", 3, route="straight"),
        bb.Wire("K1", "a20", "t-20", "black", 3, route="straight"),
        bb.Wire("SA", "UNO.A0", "a7", "green", 4, route="left"), bb.Wire("S1", "UNO.D8", "a15", "orange", 4),
        bb.Wire("V5", "UNO.5V", "t+1", "red", 5, route="left1"), bb.Wire("G", "UNO.GND", "t-22", "black", 5),
    ],
    steps=[
        ("放光敏電阻", "光敏電阻<b>沒有方向</b>,兩隻腳插在 <code>d5</code> 與 <code>d7</code>(隔一欄)。表面有彎曲紋路的那一面朝上,這樣才受得到光。"),
        ("放兩顆電阻與 LED", "<b>10 kΩ 電阻</b>(棕、黑、橙)橫放在 <code>b7–b11</code>;<b>220Ω 電阻</b>放 <code>b15–b19</code>;<b>紅色 LED</b> 長腳(+)插 <code>d19</code>、短腳(−)插 <code>d20</code>。<br>10 kΩ 電阻與光敏電阻在第 7 欄接在一起,這一點就是要量電壓的地方。"),
        ("三條短線", "① 紅色 <code>a5</code> → <code>t+5</code>:光敏電阻一腳接 + 軌(5V)。<br>② 黑色 <code>a11</code> → <code>t-11</code>:10 kΩ 電阻的另一端接 − 軌(GND)。<br>③ 黑色 <code>a20</code> → <code>t-20</code>:LED 負極接 − 軌。"),
        ("兩條訊號線:A0 與 8 號腳", "綠線:Uno <b>A0</b> → <code>a7</code>(光敏電阻與 10 kΩ 電阻相接的那一欄)。<br>橘線:Uno <b>8 號腳</b> → <code>a15</code>(220Ω 電阻左端)。"),
        ("電源線:5V 與 GND", "紅線:Uno <b>5V</b> → <code>t+1</code>。黑線:Uno 數位腳位排的 <b>GND</b> → <code>t-22</code>。"),
    ],
    chains=[["UNO.5V", "LDR1", "UNO.A0"], ["UNO.A0", "R2", "UNO.GND"], ["UNO.D8", "R1", "LED1", "UNO.GND"]],
    intro="先<strong>拔掉 USB 線</strong>。光敏電阻要和一顆 10 kΩ 電阻<b>串聯成分壓電路</b>,A0 量它們中間那一點的電壓。LED 接 8 號腳,天黑時由程式點亮。",
    done="5V → 光敏電阻 → (A0 接在這裡)→ 10 kΩ 電阻 → GND,是分壓電路。檢查:A0 接的是兩顆電阻相接的那一欄,而不是 5V 或 GND 那一欄。",
)
CIRCUITS = [CIRC]

L1 = """// 第 10 篇:先量量看——印出光線的讀值
const int LDR_PIN = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int light = analogRead(LDR_PIN);   // 越亮,數字越大(這個接法)
  Serial.println(light);
  delay({gap});
}
"""
L2 = """// 第 10 篇:小夜燈(天黑就亮)
const int LDR_PIN = A0;
const int LED_PIN = 8;
const int THRESHOLD = {thr};      // 門檻:讀值低於它就算「天黑了」

void setup() {
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  int light = analogRead(LDR_PIN);
  Serial.println(light);
  if (light < THRESHOLD) {          // 比門檻小:暗
    digitalWrite(LED_PIN, HIGH);    // 開燈
  } else {                          // 否則:亮
    digitalWrite(LED_PIN, LOW);     // 關燈
  }
  delay(100);
}
"""
L3 = """// 第 10 篇:加上「遲滯」——兩個門檻,避免在邊界閃爍
const int LDR_PIN = A0;
const int LED_PIN = 8;
const int DARK = {dark};          // 低於這個值,才開燈
const int BRIGHT = {bright};      // 高於這個值,才關燈
bool ledOn = false;               // 記住燈現在是亮或滅

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  int light = analogRead(LDR_PIN);
  if (ledOn == false && light < DARK) {          // 燈是滅的,而且夠暗了 → 開燈
    ledOn = true;
    digitalWrite(LED_PIN, HIGH);
  } else if (ledOn == true && light > BRIGHT) {  // 燈是亮的,而且夠亮了 → 關燈
    ledOn = false;
    digitalWrite(LED_PIN, LOW);
  }
  delay(100);
}
"""
FILL = dict(gap="500", thr="400", dark="300", bright="500")
SKETCHES = [
    dict(name="ldr-read", code=L1, fill=FILL,
         sim=dict(kind="uart", seconds=1.2, adc=[(0, 3911, 0), (0, 978, 500)], expect=["800\r\n", "200\r\n"])),
    dict(name="ldr-night", code=L2, fill=FILL, circuit=CIRC, code_pins={"LED_PIN": "UNO.D8"},
         sim=dict(kind="uart", seconds=1.6, pin="D8", adc=[(0, 3911, 0), (0, 978, 500), (0, 3911, 1000)], expect=["800\r\n", "200\r\n"],
                  edges=[(1, 502), (0, 1003)], tol_ms=30)),
    dict(name="ldr-hyst", code=L3, fill=FILL, circuit=CIRC, code_pins={"LED_PIN": "UNO.D8"},
         sim=dict(kind="adc_edges", pin="D8", seconds=2.4, adc=[(0, 3911, 0), (0, 1711, 500), (0, 1222, 1000), (0, 1711, 1500), (0, 3911, 2000)],
                  expect=[(1, 1000), (0, 2000)], tol_ms=130, note="亮 → 中間值 → 暗 → 中間值 → 亮")),
]

ldrsim = ('<div class="panel" data-ldrsim><div class="wgrid f2"><div><label>環境亮度(0% = 全黑,100% = 很亮)</label><input type="range" min="0" max="100" value="50" data-ldr="v"></div>'
          '<div><label>門檻(analogRead 低於它就開燈)</label><input data-ldr="thr" value="400" inputmode="numeric" autocomplete="off"></div></div>'
          '<div class="pot-bar" aria-hidden="true"><span></span></div>'
          '<div class="rc-out ldr-out" aria-live="polite"></div>'
          '<p style="margin:10px 0 0;font-size:14px;color:var(--gray-700)">LED:<span class="pwm-led" style="margin-left:6px"></span></p></div>')

what = section("what", "光敏電阻:光越亮,電阻越小",
  '<div class="panel"><h3>光敏電阻(LDR)是什麼</h3>'
  '<p>它是一顆<b>電阻值會隨光線改變</b>的電阻:<b>越亮,電阻越小</b>;完全黑暗時,電阻可高達 1 MΩ 以上(常見的 GL5528:光線充足時約數百歐姆到幾 kΩ,10 lux 約 8–20 kΩ)。這些數字是範例值,<b>每顆都有差異,用 Serial 實際量一次最準</b>。</p>'
  '<p style="margin-bottom:0">但 Arduino 只會量<b>電壓</b>,不會量電阻。要把「電阻的變化」變成「電壓的變化」,用上一篇學的<b>分壓</b>。</p></div>',
  '<h3 style="margin-top:26px">分壓:把電阻變化換成電壓變化</h3>',
  '<p>光敏電阻與一顆固定的 10 kΩ 電阻<b>串聯</b>,5V 加在串聯的兩端,中間那一點接 A0。光敏電阻的比例變了,A0 的電壓就跟著變:</p>',
  '<div class="panel"><p style="margin:0">A0 電壓 = 5 V × <b>10 kΩ</b> ÷ (<b>光敏電阻</b> + 10 kΩ)</p></div>',
  table("g3", ["環境", "光敏電阻(範例)", "A0 電壓 / analogRead"], [
    ["很亮", "約 1 kΩ", "約 4.5 V / 約 930"],
    ["室內一般亮度", "約 10 kΩ", "約 2.5 V / 約 511"],
    ["很暗", "約 100 kΩ 以上", "約 0.45 V / 約 93 以下"],
  ]),
  '<p class="sk">上表是用公式算出的範例;你的光敏電阻數值不同,實際讀值也不同,所以要先量再決定門檻。</p>',
  '<h3 style="margin-top:26px">拖曳看看</h3>', ldrsim,
  tip("為什麼固定電阻選 10 kΩ?分壓電路的固定電阻選<b>和光敏電阻「常用範圍」差不多大</b>,A0 電壓的變化範圍才夠大、好分辨。這是常見的經驗做法,不是唯一答案。"))

wire = section("wire", "接線:光敏電阻分壓(A0)加 LED(8 號腳)",
  bb.stepper_html(CIRC),
  '<p class="sk">Uno 轉了 180 度擺放:A0、5V 在上緣,<b>兩條線要繞過 Uno 左邊</b>;數位腳位(8、GND)在下緣。圖只畫左邊 22 欄,以欄號與 a–j 為準(手機上可以左右滑動圖)。</p>',
  '<h3 style="margin-top:26px">接線表</h3>', bb.wiring_table(CIRC),
  warn("<b>A0 的線要接在「光敏電阻與 10 kΩ 電阻相接」的那一欄(第 7 欄)</b>。接在 5V 軌或 GND 軌,讀值會永遠是 1023 或 0。接線前先拔 USB。", "最容易接錯的地方"),
  '<h3 style="margin-top:26px">原理圖</h3>',
  '<p class="sub">三條路:<b>5V → 光敏電阻 → A0</b>、<b>A0 → 10 kΩ → GND</b>(兩個 A0 是同一點),以及 LED 那一組。</p>',
  *[canvas(bb.schematic_svg(CIRC)[0], [(n, '<span class="newsym">新符號</span>' + t) for n, t in bb.schematic_svg(CIRC)[1] if "光敏" in t])],
  '<div class="linkbox" id="linkInfo" style="margin-top:12px">點原理圖裡的光敏電阻、電阻或 LED,看它在麵包板上是哪一個。</div>')

fillsec = section("fill", "先填入你的數值",
  fill([("gap", "校準時,印出數字的間隔(毫秒)", True), ("thr", "小夜燈的門檻(程式二)", True), ("dark", "遲滯:低於這個才開燈(程式三)", True), ("bright", "遲滯:高於這個才關燈(程式三)", True)]),
  '<p class="sk">空白時用範例值:500、400、300、500。<b>先做完程式一的校準,再回來改這裡。</b></p>')

def exp(items):
    return table("g2", ["這一行", "它在做什麼"], items)

code1 = section("code1", "程式一:先量一量,知道你的光是多少",
  cmd(L1, cap="校準用:印出光線讀值", cpp=True),
  steps(step(1, "上傳,打開 Serial Monitor(baud 9600)", "第 8 篇學過。"),
        step(2, "記下兩個數字", "這兩個數字決定程式二的門檻。",
             ops(["在你平常的<b>室內光線</b>下,記下讀值(例如 650)。", "用手<b>完全蓋住光敏電阻</b>(或關燈),記下讀值(例如 120)。"]),
             see("光亮時數字大、蓋住時數字小。你的兩個數字一定和範例不一樣,沒關係。"))),
  tip("<b>門檻怎麼選?</b>取兩個數字的中間值。亮 650、暗 120 → 門檻 ≈ 385,就填 400 左右。"))

code2 = section("code2", "程式二:小夜燈(天黑就亮)",
  cmd(L2, cap="讀值低於門檻,就開燈", cpp=True),
  exp([
    ["<code>const int THRESHOLD = 400;</code>", "<b>門檻</b>:用名字取代數字,之後只要改這一處。"],
    ["<code>if (light &lt; THRESHOLD) { … } else { … }</code>", "讀值<b>小於</b>門檻(暗)就開燈,否則關燈。<code>&lt;</code> 是「小於」。"],
    ["<code>delay(100);</code>", "每 0.1 秒量一次就夠了,不必一直量。"],
  ]),
  see("<b>手蓋住光敏電阻,LED 亮;手移開,LED 滅</b>。若效果相反或沒反應,先看常見卡關。"),
  warn("<b>如果讀值剛好停在門檻附近</b>(例如黃昏,光線慢慢變暗),LED 可能<b>不停閃爍</b>:讀值一下 399、一下 401,一下低於、一下高於。下一個程式解決它。", "會有個問題"))

code3 = section("code3", "程式三:遲滯 —— 兩個門檻,不再閃爍",
  '<p class="sub" style="margin-bottom:14px">做法:<b>開燈</b>與<b>關燈</b>用<b>不同</b>的門檻。低於 <code>DARK</code> 才開燈,要高於 <code>BRIGHT</code> 才關燈,兩者之間<b>維持原狀</b>。這叫<b>遲滯</b>(hysteresis),冷氣、恆溫器也是這樣做。</p>',
  cmd(L3, cap="遲滯:DARK 開燈、BRIGHT 關燈", cpp=True),
  exp([
    ["<code>bool ledOn = false;</code>", "記住燈現在的狀態(第 7 篇學過布林變數)。判斷時要「看狀態」。"],
    ["<code>if (ledOn == false &amp;&amp; light &lt; DARK)</code>", "<code>&amp;&amp;</code> 是「而且」:<b>兩個條件都成立</b>才做。燈是滅的、<b>而且</b>夠暗,才開燈。"],
    ["<code>else if (ledOn == true &amp;&amp; light &gt; BRIGHT)</code>", "否則,燈是亮的、而且夠亮,才關燈。介於兩個門檻之間,兩個條件都不成立,什麼都不做。"],
  ]),
  table("g3", ["讀值", "只有一個門檻(400)", "遲滯(開燈 300、關燈 500)"], [
    ["800(亮)", "滅", "滅"], ["350(黃昏)", "亮", "<b>維持原狀(滅)</b>"], ["250(暗)", "亮", "亮"], ["450(微亮)", "滅", "<b>維持原狀(亮)</b>"], ["800(亮)", "滅", "滅"],
  ]),
  tip("邏輯運算:<code>&amp;&amp;</code> 而且、<code>||</code> 或者、<code>!</code> 不是。例如 <code>if (a &gt; 3 || b == 0)</code> 表示 a 大於 3 <b>或者</b> b 等於 0。"))

try_ = section("try", "改改看",
  table("g3", ["挑戰", "怎麼改", "你會看到"], [
    ["反過來:亮才亮", "程式二把 <code>&lt;</code> 改成 <code>&gt;</code>", "光越強 LED 越亮,蓋住就熄。"],
    ["調靈敏度", "把門檻往亮的方向調(例如 600)", "不用很暗就會開燈。"],
    ["漸亮的夜燈", "第 9 篇的 <code>map</code> 搭配 <code>analogWrite</code>,讓 LED 亮度和環境亮度相反", "天越暗,燈越亮。LED 要改接 9 號腳。"],
  ]))

gotchas = section("gotchas", "常見卡關",
  details("讀值固定在 1023,或固定在 0",
    ops(["<b>A0 沒接在兩顆電阻相接的那一欄</b>:接到 5V 軌 → 永遠 1023;接到 GND 軌 → 永遠 0。", "10 kΩ 電阻沒有接到 GND,或光敏電阻沒有接到 5V:分壓電路斷了,A0 浮接。", "光敏電阻或 10 kΩ 電阻的腳沒插到底。"]), True) +
  details("蓋住和不蓋,讀值差別很小",
    "<p>光敏電阻朝向的光線太均勻,或固定電阻不適合。用手電筒對著它照,再完全蓋住,看範圍有多大。必要時把 10 kΩ 換成 4.7 kΩ 或 22 kΩ 試試(要重新校準門檻)。</p>") +
  details("效果相反(亮的時候 LED 反而亮)",
    "<p>檢查光敏電阻和 10 kΩ 的位置有沒有接反(光敏電阻要接 5V 那一側)。或直接在程式裡把 <code>&lt;</code> 換成 <code>&gt;</code>。</p>") +
  details("LED 在黃昏時閃爍",
    "<p>用程式三(遲滯)。把 <code>DARK</code> 與 <code>BRIGHT</code> 的距離拉大一點,雜訊就不會讓它來回切換。</p>") +
  details("LED 不亮",
    "<p>先檢查 LED 的組(和第 3 篇一樣):長腳方向、同欄、8 號腳、GND。再用程式一確認光線讀值有變化。</p>"))

SIM = {
  "a1": "<b>不用。</b>固定在 1023 表示 A0 一直接近 5 V,這是接線問題。",
  "a2": "<b>對。</b>A0 必須接在光敏電阻和 10 kΩ 電阻<b>相接的那一欄</b>。接在 5V 軌會固定 1023、接在 GND 軌會固定 0。",
  "a3": "<b>沒有用。</b>換更大的 LED 電阻,不影響光線感測的分壓電路。",
}
QUIZ = quiz_cfg([
  ("光敏電阻在光線越亮時,電阻?", ["變大", "變小", "不變"], 1, "光越亮,光敏電阻越小。"),
  ("為什麼要和固定電阻一起接成分壓?", ["Arduino 只能量電壓,要把電阻變化換成電壓變化", "為了省電", "為了讓 LED 更亮"], 0, "ADC 量的是電壓,分壓電路負責轉換。"),
  ("<code>if (a &gt; 3 &amp;&amp; b == 0)</code> 什麼時候成立?", ["a 大於 3 或 b 等於 0", "a 大於 3 而且 b 等於 0", "只要 b 等於 0"], 1, "&amp;&amp; 要兩邊都成立。"),
  ("「遲滯」的目的是?", ["避免讀值在門檻附近來回觸發", "讓程式變快", "節省記憶體"], 0, "用兩個不同的門檻,中間維持原狀,就不會閃爍。"),
  ("決定門檻最好的方法是?", ["隨便猜 512", "用 Serial 量亮與暗的讀值,取中間", "越小越好"], 1, "每顆零件與環境不同,先量再決定。"),
])
practice = section("practice", "動手演練與延伸閱讀",
  sim("", "情境:不論亮或暗,Serial Monitor 的讀值都是 1023", "你應該先?",
      [("a1", "改程式的門檻"), ("a2", "檢查 A0 是否接在光敏電阻與 10 kΩ 電阻相接的那一欄"), ("a3", "換更大的 LED 電阻")]),
  QUIZ_HTML,
  checks(["我知道光敏電阻光越亮,電阻越小。",
          "我能解釋分壓電路怎麼把電阻變化換成電壓變化。",
          "我用 Serial 量出自己亮與暗的讀值,並選出門檻。",
          "我的小夜燈:蓋住就亮、移開就滅。",
          "我知道門檻附近會閃爍,並懂得用兩個門檻(遲滯)解決。",
          "我會用 <code>&amp;&amp;</code> 組合兩個條件。"], "做完之後,對照這張清單"),
  resources([
    ("https://docs.arduino.cc/language-reference/en/functions/analog-io/analogread/", "analogRead()", "Arduino language reference"),
    ("https://docs.arduino.cc/language-reference/en/structure/boolean-operators/logicalAnd/", "&amp;&amp;(邏輯 AND)", "Arduino language reference"),
  ], "Arduino 官方文件"))

SPEC = dict(
    dir="arduino",
    file="arduino-ldr-guide.html",
    title="光敏電阻小夜燈:分壓、門檻與遲滯",
    eyebrow="第 10 篇 · 光敏電阻",
    h1="天黑自動開燈:用光敏電阻做小夜燈",
    sub="用光敏電阻與 10 kΩ 電阻組成分壓電路,讓 Arduino 量光線;再用門檻判斷天黑,並用遲滯解決邊界閃爍。",
    tldr="光敏電阻<strong>越亮電阻越小</strong>。它與 <strong>10 kΩ 串聯分壓</strong>,A0 接在<strong>兩者相接處</strong>。先用 Serial 量亮與暗的讀值,取中間當<strong>門檻</strong>;為避免在門檻附近閃爍,用<strong>兩個門檻(遲滯)</strong>。",
    toc=[("what", "光敏電阻與分壓"), ("wire", "接線"), ("fill", "填入數值"), ("code1", "程式一:校準"), ("code2", "程式二:小夜燈"),
         ("code3", "程式三:遲滯"), ("try", "改改看"), ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
    body="\n\n".join([what, wire, fillsec, code1, code2, code3, try_, gotchas, practice]),
    config=dict(fill=FILL, sim=SIM, quiz=QUIZ, wiring=[bb.wiring_config(CIRC)], parts=bb.parts_info(CIRC)),
    prev=("arduino-analog-guide.html", "類比輸入:電位器"),
    next=("arduino-ultrasonic-guide.html", "超音波測距 HC-SR04"),
)
