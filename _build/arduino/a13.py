# -*- coding: utf-8 -*-
from h import *
import bb

CIRC = bb.Circuit(
    "dht-led", 22,
    parts=[
        bb.DHT11("DHT1", "e5", "e6", "e7", 1),
        bb.Resistor("R1", 220, "b13", "b17", 2), bb.LED("LED1", "red", "d17", "d18", 2),
        bb.Wire("V6", "a6", "t+6", "red", 3, route="straight"), bb.Wire("G7", "a7", "t-7", "black", 3, route="straight"),
        bb.Wire("K1", "a18", "t-18", "black", 3, route="straight"),
        bb.Wire("SD", "UNO.D2", "a5", "blue", 4), bb.Wire("S1", "UNO.D8", "a13", "orange", 4),
        bb.Wire("V5", "UNO.5V", "t+1", "red", 5, route="left"), bb.Wire("G", "UNO.GND", "t-20", "black", 5),
    ],
    steps=[
        ("放 DHT11 模組", "三隻針腳插 <code>e5</code>(<b>S / DATA</b>)、<code>e6</code>(<b>+ / VCC</b>)、<code>e7</code>(<b>− / GND</b>)。<br><b>先看你的模組上印的符號再對</b>:S(或 DATA、OUT)是訊號,+(或 VCC)是電源,−(或 GND)是接地。<b>各廠牌的順序不一樣</b>,若和圖不同,以模組上的印刷為準,圖上的孔位照著換。"),
        ("放電阻與 LED", "<b>220Ω 電阻</b>橫放在 <code>b13–b17</code>;<b>紅色 LED</b> 長腳(+)插 <code>d17</code>、短腳(−)插 <code>d18</code>。LED 這一組之後做「高溫警示」。"),
        ("三條短線", "① 紅 <code>a6</code> → <code>t+6</code>:模組電源接 + 軌。<br>② 黑 <code>a7</code> → <code>t-7</code>:模組 GND 接 − 軌。<br>③ 黑 <code>a18</code> → <code>t-18</code>:LED 負極接 − 軌。"),
        ("兩條訊號線:2 號腳與 8 號腳", "藍線:Uno <b>2 號腳</b> → <code>a5</code>(DHT11 的 DATA)。<br>橘線:Uno <b>8 號腳</b> → <code>a13</code>(電阻左端)。"),
        ("電源線:5V 與 GND", "紅線:Uno <b>5V</b> → <code>t+1</code>。黑線:Uno 數位腳位排的 <b>GND</b> → <code>t-20</code>。"),
    ],
    chains=[["UNO.5V", "DHT1.VCC"], ["DHT1.GND", "UNO.GND"], ["UNO.D2", "DHT1.DATA"], ["UNO.D8", "R1", "LED1", "UNO.GND"]],
    intro="先<strong>拔掉 USB 線</strong>。DHT11 三腳模組:<b>S 訊號、+ 電源、− 接地</b>。訊號線接 2 號腳;LED 接 8 號腳,之後做溫度警示。",
    done="DHT11:S → 2 號腳、+ → 5V、− → GND。LED:8 號腳 → 220Ω → LED → GND。檢查:<b>+ 與 − 沒有接反</b>(接反會讓模組發燙損壞)。",
)
CIRCUITS = [CIRC]

D1 = """// 第 13 篇:讀 DHT11 的溫度與濕度
#include <DHT.h>                 // 引入 Adafruit 的 DHT 函式庫(要先用 Library Manager 安裝)

const int DHT_PIN = 2;           // DATA 接在 2 號腳
DHT dht(DHT_PIN, DHT11);         // 建立感測器物件:腳位 2、型號 DHT11

void setup() {
  Serial.begin(9600);
  dht.begin();                   // 啟動感測器
}

void loop() {
  delay({gap});                  // DHT11 很慢:兩次讀取至少隔 1–2 秒
  float h = dht.readHumidity();          // 讀濕度(%)
  float t = dht.readTemperature();       // 讀溫度(攝氏)

  if (isnan(h) || isnan(t)) {            // isnan:不是數字 → 讀取失敗
    Serial.println("讀取失敗,請檢查接線");
    return;                              // 結束這一輪 loop,等下一輪重來
  }

  Serial.print("濕度 = ");
  Serial.print(h);
  Serial.print(" %   溫度 = ");
  Serial.print(t);
  Serial.println(" C");
}
"""
D2 = """// 第 13 篇:高溫警示——溫度超過門檻就亮燈
#include <DHT.h>

const int DHT_PIN = 2;
const int LED_PIN = 8;
const float ALARM_TEMP = {alarm};        // 警示溫度(攝氏)
DHT dht(DHT_PIN, DHT11);

void setup() {
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  dht.begin();
}

void loop() {
  delay({gap});
  float t = dht.readTemperature();
  if (isnan(t)) {
    Serial.println("讀取失敗,請檢查接線");
    return;
  }
  Serial.print("溫度 = ");
  Serial.println(t);
  if (t > ALARM_TEMP) {                  // 超過警示溫度
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
}
"""
FILL = dict(gap="1200", alarm="28")
LIBS = ["DHT-sensor-library", "Adafruit_Sensor"]
SKETCHES = [
    dict(name="dht-read", code=D1, fill=FILL, circuit=CIRC, code_pins={"DHT_PIN": "UNO.D2"}, libs=LIBS,
         sim=dict(kind="uart", seconds=3.0, dht=[("D2", 26, 55)], expect=["濕度 = 55.00 %   溫度 = 26.00 C\r\n", "濕度 = 55.00 %   溫度 = 26.00 C\r\n"])),
    dict(name="dht-fail", code=D1, fill=FILL, circuit=CIRC, code_pins={"DHT_PIN": "UNO.D2"}, libs=LIBS,
         sim=dict(kind="uart", seconds=2.8, expect=["讀取失敗,請檢查接線\r\n", "讀取失敗,請檢查接線\r\n"])),
    dict(name="dht-alarm", code=D2, fill=dict(FILL, alarm="25"), circuit=CIRC, code_pins={"DHT_PIN": "UNO.D2", "LED_PIN": "UNO.D8"}, libs=LIBS,
         sim=dict(kind="uart", seconds=2.8, pin="D8", dht=[("D2", 26, 55)], expect=["溫度 = 26.00\r\n"], edges=[(1, 1205)], tol_ms=60)),
]

def dht_schematic():
    G7, SL, CL = bb.GRAY7, bb.SLATE, bb.CLAY
    o = ['<g class="el" data-part="DHT1" tabindex="0" role="button" aria-label="DHT11 模組,點一下看它在麵包板上的位置">'
         '<rect class="halo" x="108" y="26" width="150" height="150" rx="12" fill="none" stroke="%s" stroke-width="2.5"/>'
         '<rect x="120" y="34" width="126" height="134" rx="8" fill="#F0EEE6" stroke="%s" stroke-width="1.8"/>' % (CL, G7),
         bb._txt(183, 104, "DHT11", "mb", SL), bb._txt(183, 120, "溫濕度模組", "s", bb.GRAY5)]
    for nm, y, side in (("VCC", 62, "L"), ("GND", 142, "L"), ("DATA", 102, "R")):
        o.append(bb._txt(130, y + 4, nm, "m", SL, "start") if side == "L" else bb._txt(236, y + 4, nm, "m", SL, "end"))
    o.append("</g>")
    o.append('<line x1="120" y1="62" x2="78" y2="62" stroke="%s" stroke-width="2"/><line x1="78" y1="62" x2="78" y2="42" stroke="%s" stroke-width="2"/>' % (G7, G7))
    o.append('<line x1="62" y1="42" x2="94" y2="42" stroke="%s" stroke-width="2.4" stroke-linecap="round"/>' % G7 + bb._txt(78, 34, "5V", "mb", bb.RUST))
    o.append('<line x1="120" y1="142" x2="78" y2="142" stroke="%s" stroke-width="2"/><line x1="78" y1="142" x2="78" y2="160" stroke="%s" stroke-width="2"/>' % (G7, G7))
    for k, wd in enumerate((28, 18, 8)):
        o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.2" stroke-linecap="round"/>' % (78 - wd / 2, 160 + k * 7, 78 + wd / 2, 160 + k * 7, G7))
    o.append('<line x1="246" y1="102" x2="300" y2="102" stroke="%s" stroke-width="2"/>' % G7)
    o.append('<rect x="300" y="87" width="80" height="30" rx="8" fill="#F0EEE6" stroke="%s" stroke-width="1.5"/>%s' % (G7, bb._txt(340, 106, "Uno D2", "mb", SL)))
    o.append(bb._txt(270, 94, "資料 ⇄", "m", bb.GRAY5))
    return ('<svg viewBox="0 0 420 200" role="img" aria-label="DHT11 原理圖" style="min-width:420px"><defs>%s</defs><rect width="420" height="200" fill="#FFFFFF"/>%s</svg>' % (bb.STYLE, "".join(o)))

led_circ = bb.Circuit("dht-led8", 22, parts=CIRC.parts, steps=CIRC.steps, chains=[["UNO.D8", "R1", "LED1", "UNO.GND"]])
LED_SCH = bb.schematic_svg(led_circ, mark=())[0]

what = section("what", "DHT11:同時量溫度和濕度",
  '<div class="panel"><h3>認識 DHT11</h3>'
  '<p>DHT11 是便宜的<b>溫濕度感測器</b>:一條訊號線(DATA)就能讀出<b>溫度與濕度</b>。常見規格:溫度 0–50 °C(誤差約 ±2 °C)、濕度 20–80 %(誤差約 ±5 %),<b>讀取速度很慢:兩次讀取至少隔 1–2 秒</b>。電壓 3.3–5.5 V,用 Uno 的 5V 就可以。</p>'
  '<p style="margin-bottom:0">它用一種<b>單線通訊協定</b>:Arduino 先拉低訊號線叫醒它,它再用一連串長短不同的脈衝,把 40 個位元的資料(溫度、濕度、檢查碼)送回來。<b>這段脈衝時序很精細</b>,自己寫很麻煩,所以我們用<b>別人寫好的函式庫</b>。</p></div>',
  tip("這裡的規格是常見資料手冊的數值,<b>以你的模組為準</b>。DHT11 精度有限,適合看趨勢(例如「現在悶不悶」),不適合需要精確數字的場合。要更準可以升級 DHT22 或其他感測器,用法類似。"))

lib = section("lib", "安裝函式庫:用 Library Manager",
  '<p class="sub" style="margin-bottom:14px">上一篇的 <code>Servo</code> 是 IDE 內建的。DHT11 的函式庫<b>不是內建的</b>,要自己安裝。這是你以後用任何感測器都會做的步驟。</p>',
  steps(
    step(1, "打開 Library Manager", "IDE 2 左側邊欄有一排圖示,函式庫管理員是其中一個。",
         ops(["點左側邊欄的<b>函式庫圖示(Library Manager)</b>(由上往下第三個)。", "或用選單 <b>Sketch → Include Library → Manage Libraries…</b>。"])),
    step(2, "搜尋並安裝", "函式庫要找對作者,不然會裝到不相容的版本。",
         ops(["在搜尋欄輸入 <code>DHT sensor library</code>。", "找到<b>作者是 Adafruit</b> 的那一個,按 <b>INSTALL</b>。"])),
    step(3, "安裝相依的函式庫", "有些函式庫需要別的函式庫才能運作,IDE 會問你。",
         ops(["跳出「Install library dependencies」視窗,詢問是否要同時安裝 <b>Adafruit Unified Sensor</b>。", "按 <b>INSTALL ALL</b>(安裝全部)。"]),
         see("等一下,函式庫清單裡這兩個都會標上 <code>INSTALLED</code>。"),
         warn("<b>一定要按 INSTALL ALL。</b>只裝 DHT 本體、不裝相依的 Adafruit Unified Sensor,編譯時會出現找不到 <code>Adafruit_Sensor.h</code> 的錯誤(見常見卡關)。", "別漏掉")),
    step(4, "確認可以使用", "裝好之後,程式最上面加 <code>#include &lt;DHT.h&gt;</code> 就能用。",
         ops(["也可以看內建範例:<b>File → Examples → DHT sensor library → DHTtester</b>。", "之後所有第三方函式庫都是同樣的流程:搜尋、安裝、(裝相依)、<code>#include</code>。"])),
  ))

wire = section("wire", "接線:DHT11(2 號腳)加 LED(8 號腳)",
  bb.stepper_html(CIRC),
  '<p class="sk">Uno 轉了 180 度擺放:5V 在上緣,要繞過左邊;數位腳位(2、8、GND)在下緣。圖只畫左邊 22 欄,<b>模組不是按比例畫的</b>。以欄號與 a–j 為準(手機上可以左右滑動圖)。</p>',
  '<h3 style="margin-top:26px">接線表</h3>', bb.wiring_table(CIRC),
  warn("<b>+ 與 − 不要接反。</b>DHT11 模組接反電源會發燙、損壞。三腳模組的腳位順序因廠牌而異,<b>一定要對照你的模組上印的 S、+、−(或 DATA、VCC、GND)</b>。接線前先拔 USB。", "注意"),
  '<h3 style="margin-top:26px">原理圖</h3>',
  canvas(dht_schematic(), [("", "")][:0] or []),
  '<h3 style="margin-top:18px">LED 那一組</h3>', canvas(LED_SCH, []),
  '<div class="linkbox" id="linkInfo" style="margin-top:12px">點原理圖裡的模組、電阻或 LED,看它在麵包板上是哪一個。</div>',
  tip("三腳版 DHT11 模組<b>已經附有上拉電阻</b>(讓訊號線平常維持 HIGH)。若你買的是<b>四腳的單體</b>,要自己在 DATA 與 VCC 之間接一顆 4.7–10 kΩ 電阻,本篇不涵蓋。"))

fillsec = section("fill", "先填入你的數值",
  fill([("gap", "兩次讀取的間隔(毫秒,至少 1000)", True), ("alarm", "高溫警示的溫度(攝氏,程式二)", True)]),
  '<p class="sk">空白時用範例值:1200、28。程式二的警示溫度,可以設成比現在室溫低一點,等一下才看得到 LED 亮。</p>')

def exp(items):
    return table("g2", ["這一行", "它在做什麼"], items)

code1 = section("code1", "程式一:讀溫度與濕度",
  cmd(D1, cap="DHT11:印出濕度與溫度", cpp=True),
  exp([
    ["<code>#include &lt;DHT.h&gt;</code>", "引入剛安裝的函式庫。沒安裝會出錯。"],
    ["<code>DHT dht(DHT_PIN, DHT11);</code>", "建立一個 <code>DHT</code> 物件,取名 <code>dht</code>。括號是「<b>建立時要給的設定</b>」:接在哪個腳位、感測器型號。"],
    ["<code>dht.begin();</code>", "啟動感測器。"],
    ["<code>dht.readHumidity()</code>、<code>dht.readTemperature()</code>", "讀濕度(%)與溫度(攝氏)。回傳 <code>float</code>。想要華氏,<code>readTemperature(true)</code>。"],
    ["<code>isnan(h) || isnan(t)</code>", "<code>isnan</code> 檢查「這不是個數字」。讀取失敗時函式庫回傳 NaN。<code>||</code> 是「或者」:<b>濕度或溫度任一個失敗</b>就算失敗。"],
    ["<code>return;</code>", "在 <code>loop()</code> 裡提早結束這一輪,回到開頭等下一輪。避免把壞資料印出來。"],
  ]),
  see("Serial Monitor(baud 9600)每 1.2 秒印一行,例如 <code>濕度 = 55.00 %   溫度 = 26.00 C</code>。用手捂住感測器(或對它哈氣),濕度會明顯上升,溫度也會慢慢變。"))

code2 = section("code2", "程式二:高溫警示",
  cmd(D2, cap="溫度超過門檻,LED 亮", cpp=True),
  exp([
    ["<code>const float ALARM_TEMP = 28;</code>", "<code>float</code> 常數,警示溫度。"],
    ["<code>if (t &gt; ALARM_TEMP) { … } else { … }</code>", "溫度<b>高於</b>警示就亮燈,否則熄滅。和第 10 篇的光敏電阻判斷是同樣的結構。"],
  ]),
  see("手捂住感測器讓溫度上升,超過警示溫度時 <b>LED 亮</b>;放開、溫度降下來後熄滅。"),
  tip("和第 10 篇一樣,溫度在門檻附近會讓 LED 來回切換。想避免的話,用<b>兩個門檻(遲滯)</b>。"))

try_ = section("try", "改改看",
  table("g3", ["挑戰", "怎麼改", "你會看到"], [
    ["看華氏", "<code>dht.readTemperature(true)</code>", "數字變成華氏溫度。"],
    ["加上體感指數", "<code>dht.computeHeatIndex(t, h, false)</code>", "函式庫幫你算「感覺溫度」。這是函式庫的另一個功能。"],
    ["濕度警示", "改用 <code>h</code> 判斷,超過 70% 就亮燈", "梅雨季的「太潮濕」提醒。"],
  ]))

gotchas = section("gotchas", "常見卡關",
  details("編譯錯誤:找不到 DHT.h 或 Adafruit_Sensor.h",
    "<p><code>DHT.h: No such file or directory</code> 表示 DHT 函式庫沒裝;<code>Adafruit_Sensor.h</code> 找不到表示<b>相依的函式庫沒裝</b>。回到 Library Manager,搜尋 <code>DHT sensor library</code>,安裝時按 <b>INSTALL ALL</b>;或另外搜尋 <code>Adafruit Unified Sensor</code> 安裝。</p>", True) +
  details("一直印「讀取失敗」",
    ops(["<b>DATA 腳位沒接對</b>:模組的 S 要接 2 號腳。", "<b>電源接錯</b>:+ 接 5V、− 接 GND(對照模組印刷)。", "程式裡 <code>DHT_PIN</code> 與接線的 2 號腳一致,型號選 <code>DHT11</code>。", "<b>讀得太快</b>:兩次讀取至少隔 1 秒;<code>delay</code> 不要設太小。", "模組是四腳單體、沒有上拉電阻。"])) +
  details("數字偶爾跳掉或不準",
    "<p>DHT11 本來就不精確(溫度約 ±2 °C、濕度約 ±5 %),而且對氣流、手的溫度敏感。把它放在不被風吹、不被手碰的地方,看長時間的趨勢。</p>") +
  details("模組發燙",
    "<p><b>立刻拔掉 USB。</b>很可能 + 與 − 接反了。確認腳位之後再通電;壞掉的模組要換新的。</p>") +
  details("LED 不亮",
    "<p>程式二有沒有成功上傳;警示溫度是否低於現在的溫度;LED 方向、8 號腳接線(第 3 篇)。</p>"))

SIM = {
  "a1": "<b>不用。</b>這個錯誤是「沒裝到函式庫」,和 IDE 本身無關。",
  "a2": "<b>對。</b>安裝 DHT 函式庫時,一定要按 INSTALL ALL,同時裝相依的 Adafruit Unified Sensor。漏裝就會出現找不到 <code>Adafruit_Sensor.h</code> 的錯誤。",
  "a3": "<b>沒有用。</b>換 USB 線不會補上缺少的函式庫。",
}
QUIZ = quiz_cfg([
  ("為什麼要用函式庫來讀 DHT11?", ["因為它的通訊時序很精細,自己寫很麻煩", "因為 Arduino 不能讀它", "因為它很貴"], 0, "函式庫把複雜的時序處理好了。"),
  ("安裝第三方函式庫的流程是?", ["Library Manager 搜尋 → INSTALL →(有相依就)INSTALL ALL → #include", "直接 #include 就好", "要重新安裝 IDE"], 0, "搜尋、安裝、裝相依、#include。"),
  ("<code>isnan(t)</code> 為 true 代表?", ["溫度很高", "讀取失敗,t 不是有效數字", "溫度是 0"], 1, "NaN 是「不是數字」,讀取失敗時回傳。"),
  ("DHT11 兩次讀取至少要隔多久?", ["不用等", "約 1–2 秒", "1 分鐘"], 1, "DHT11 很慢,讀太快會失敗。"),
  ("<code>DHT dht(2, DHT11);</code> 的括號裡是?", ["建立物件時的設定(腳位、型號)", "溫度與濕度", "兩個腳位"], 0, "告訴函式庫接在哪個腳位、是哪個型號。"),
])
practice = section("practice", "動手演練與延伸閱讀",
  sim("", "情境:編譯出現找不到 Adafruit_Sensor.h", "你應該先?",
      [("a1", "重新安裝 IDE"), ("a2", "回 Library Manager 把相依的 Adafruit Unified Sensor 一起裝好(INSTALL ALL)"), ("a3", "換 USB 線")]),
  QUIZ_HTML,
  checks(["我知道 DHT11 能量溫度與濕度,而且讀取很慢。",
          "我會用 Library Manager 安裝函式庫,並知道要按 INSTALL ALL。",
          "我能說出建立物件、<code>begin()</code>、<code>read…()</code> 三步。",
          "我的 Serial Monitor 能印出合理的溫度與濕度。",
          "我知道 <code>isnan</code> 與 <code>||</code> 在做什麼。",
          "我的高溫警示:溫度超過門檻,LED 就亮。"], "做完之後,對照這張清單"),
  resources([
    ("https://docs.arduino.cc/software/ide-v2/tutorials/ide-v2-installing-a-library", "在 IDE 2 安裝函式庫", "Installing libraries"),
    ("https://docs.arduino.cc/language-reference/en/functions/digital-io/digitalwrite/", "digitalWrite()", "Arduino language reference"),
  ], "Arduino 官方文件"))

SPEC = dict(
    dir="arduino",
    file="arduino-dht-guide.html",
    title="溫濕度 DHT11:安裝第三方函式庫",
    eyebrow="第 13 篇 · DHT11 與函式庫",
    h1="量溫度與濕度,順便學會安裝別人寫好的函式庫",
    sub="用 Library Manager 安裝 Adafruit 的 DHT 函式庫,讀出溫度與濕度,並做一個高溫警示。",
    tldr="DHT11 一條線讀<strong>溫度與濕度</strong>,兩次讀取至少隔 <strong>1–2 秒</strong>。函式庫不是內建的:<strong>Library Manager 搜尋 DHT sensor library(Adafruit)→ INSTALL → INSTALL ALL</strong>。程式:<code>DHT dht(腳位, DHT11)</code>、<code>begin()</code>、<code>readTemperature()</code>、<code>isnan()</code> 檢查失敗。",
    toc=[("what", "認識 DHT11"), ("lib", "安裝函式庫"), ("wire", "接線"), ("fill", "填入數值"), ("code1", "程式一:讀溫濕度"), ("code2", "程式二:高溫警示"),
         ("try", "改改看"), ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
    body="\n\n".join([what, lib, wire, fillsec, code1, code2, try_, gotchas, practice]),
    config=dict(fill=FILL, sim=SIM, quiz=QUIZ, wiring=[bb.wiring_config(CIRC)], parts=bb.parts_info(CIRC)),
    prev=("arduino-servo-guide.html", "伺服馬達 SG90"),
    next=("arduino-lcd-guide.html", "LCD1602 I2C 顯示"),
)
