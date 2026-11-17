# -*- coding: utf-8 -*-
from h import *
import bb

CIRC = bb.Circuit(
    "sonar", 22,
    parts=[
        bb.HCSR04("HC1", "e5", "e6", "e7", "e8", 1),
        bb.Resistor("R2", 220, "b13", "b17", 2), bb.Buzzer("BZ1", "active", "d17", "d20", 2),
        bb.Wire("P", "a5", "t+5", "red", 3, route="straight"), bb.Wire("G8", "a8", "t-8", "black", 3, route="straight"),
        bb.Wire("K2", "a20", "t-20", "black", 3, route="straight"),
        bb.Wire("T", "UNO.D9", "a6", "blue", 4), bb.Wire("E", "UNO.D10", "a7", "green", 4), bb.Wire("S3", "UNO.D12", "a13", "orange", 4),
        bb.Wire("V5", "UNO.5V", "t+1", "red", 5, route="left"), bb.Wire("G", "UNO.GND", "t-22", "black", 5),
    ],
    steps=[
        ("放超音波模組", "模組的<b>四隻針腳</b>插在 <code>e5</code>、<code>e6</code>、<code>e7</code>、<code>e8</code>(依序是 <b>VCC、Trig、Echo、GND</b>,請看模組上印的字)。<br>針腳朝下插,<b>兩個圓形探頭朝外</b>(圖上藍色本體畫在下方,實際上它會懸在麵包板外側或上方,不要壓到導線)。"),
        ("放電阻與蜂鳴器", "<b>220Ω 電阻</b>橫放在 <code>b13–b17</code>;<b>主動式蜂鳴器</b> <b>+ 腳</b>插 <code>d17</code>、<b>− 腳</b>插 <code>d20</code>(第 6 篇接過)。"),
        ("三條短線", "① 紅色 <code>a5</code> → <code>t+5</code>:模組 VCC 接 + 軌(5V)。<br>② 黑色 <code>a8</code> → <code>t-8</code>:模組 GND 接 − 軌。<br>③ 黑色 <code>a20</code> → <code>t-20</code>:蜂鳴器負極接 − 軌。"),
        ("三條訊號線:9、10、12 號腳", "藍線:Uno <b>9 號腳</b> → <code>a6</code>(<b>Trig</b>,Arduino 輸出脈衝給模組)。<br>綠線:Uno <b>10 號腳</b> → <code>a7</code>(<b>Echo</b>,模組把回波時間送回 Arduino)。<br>橘線:Uno <b>12 號腳</b> → <code>a13</code>(蜂鳴器那一組)。"),
        ("電源線:5V 與 GND", "紅線:Uno <b>5V</b> → <code>t+1</code>。黑線:Uno 數位腳位排的 <b>GND</b> → <code>t-22</code>。"),
    ],
    chains=[["UNO.5V", "HC1.VCC"], ["HC1.TRIG", "UNO.D9"], ["HC1.ECHO", "UNO.D10"], ["HC1.GND", "UNO.GND"], ["UNO.D12", "R2", "BZ1", "UNO.GND"]],
    intro="先<strong>拔掉 USB 線</strong>。HC-SR04 超音波模組有四隻腳:<b>VCC、Trig、Echo、GND</b>。VCC 與 GND 供電,Trig 由 Arduino 送出觸發脈衝,Echo 回報聲音來回的時間。蜂鳴器沿用第 6 篇的接法,改接 12 號腳。",
    done="模組:VCC → 5V、GND → GND、Trig → 9 號腳、Echo → 10 號腳。蜂鳴器:12 號腳 → 220Ω → 蜂鳴器 + 腳,− 腳 → GND。檢查:Trig 與 Echo 沒有接反,VCC 沒有接到 GND。",
)
CIRCUITS = [CIRC]

U1 = """// 第 11 篇:量距離,印在 Serial Monitor
const int TRIG_PIN = 9;      // Trig:Arduino 送出觸發脈衝
const int ECHO_PIN = 10;     // Echo:接收回波時間

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  digitalWrite(TRIG_PIN, LOW);       // 先確保是 LOW,等 2 微秒
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);      // 送出 10 微秒的 HIGH,告訴模組「開始量」
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 30000);   // 量 Echo 維持 HIGH 的時間(微秒),最多等 30 毫秒

  if (duration == 0) {               // 0 表示等不到回波
    Serial.println("out of range");
  } else {
    float distance = duration * 0.0343 / 2;         // 聲速 0.0343 公分/微秒;來回要除以 2
    Serial.print(distance, 1);
    Serial.println(" cm");
  }
  delay({gap});
}
"""
U2 = """// 第 11 篇:倒車雷達雛形——越近,嗶得越快
const int TRIG_PIN = 9;
const int ECHO_PIN = 10;
const int BUZZER_PIN = 12;

float readDistanceCm() {              // 自己定義的函式:量一次距離,回傳公分;量不到回傳 -1
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long duration = pulseIn(ECHO_PIN, HIGH, 30000);
  if (duration == 0) {
    return -1;
  }
  return duration * 0.0343 / 2;
}

void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop() {
  float d = readDistanceCm();
  if (d > 0 && d < {far}) {                         // 在範圍內才響
    int gap = map((int)d, 5, {far}, 50, 500);       // 距離 5 → 間隔 50 毫秒;距離 {far} → 間隔 500 毫秒
    gap = constrain(gap, 50, 500);                  // 限制在 50–500 之間
    digitalWrite(BUZZER_PIN, HIGH);
    delay(30);                                      // 嗶 30 毫秒
    digitalWrite(BUZZER_PIN, LOW);
    delay(gap);
  } else {
    delay(100);                                     // 太遠或量不到:不響
  }
}
"""
FILL = dict(gap="500", far="60")
pulses = []
t = 1.0
while t < 1500:
    pulses += [("D10", 1, round(t, 3)), ("D10", 0, round(t + 1.1666, 4))]
    t += 20.0
SKETCHES = [
    dict(name="sonar-read", code=U1, fill=FILL, circuit=CIRC, code_pins={"TRIG_PIN": "UNO.D9", "ECHO_PIN": "UNO.D10"},
         sim=dict(kind="uart", seconds=1.3, inputs=[("D10", 0, 0), ("D10", 1, 1.0), ("D10", 0, 2.1666), ("D10", 1, 520.0), ("D10", 0, 520.5832)],
                  expect=["19.8 cm\r\n", "9.9 cm\r\n", "out of range\r\n"])),
    dict(name="sonar-radar", code=U2, fill=FILL, circuit=CIRC, code_pins={"TRIG_PIN": "UNO.D9", "ECHO_PIN": "UNO.D10", "BUZZER_PIN": "UNO.D12"},
         sim=dict(kind="highlow", pin="D12", seconds=1.2, inputs=[("D10", 0, 0)] + pulses, high=(27, 35), low=(150, 260), count=3,
                  note="每 20 ms 一個約 20 cm 的回波")),
]

# ---------------------------------------------------------------- 圖
def timing_svg():
    G7 = bb.GRAY7
    return ('<svg viewBox="0 0 560 190" role="img" aria-label="HC-SR04 量測時序" style="min-width:520px"><defs>' + bb.STYLE + '</defs><rect width="560" height="190" fill="#FFFFFF"/>'
            '<text x="12" y="38" class="mb" fill="#3D3D3A">Trig</text><polyline points="70,48 70,48 110,48 110,28 128,28 128,48 540,48" fill="none" stroke="#D97757" stroke-width="3" stroke-linejoin="round"/>'
            '<text x="119" y="20" class="m" fill="#87867F" text-anchor="middle">10 微秒</text>'
            '<text x="12" y="98" class="mb" fill="#3D3D3A">聲波</text><polyline points="70,108 130,108 134,92 138,124 142,92 146,124 150,92 154,124 158,92 162,124 166,92 170,124 174,92 178,124 182,92 186,124 190,92 194,124 198,108 540,108" fill="none" stroke="#87867F" stroke-width="2"/>'
            '<text x="165" y="146" class="m" fill="#87867F" text-anchor="middle">模組送出 8 個 40 kHz 超音波</text>'
            '<text x="12" y="168" class="mb" fill="#3D3D3A">Echo</text><polyline points="70,178 200,178 200,158 400,158 400,178 540,178" fill="none" stroke="#788C5D" stroke-width="3" stroke-linejoin="round"/>'
            '<line x1="200" y1="186" x2="400" y2="186" stroke="#87867F"/><text x="300" y="150" class="sb" fill="#3D3D3A" text-anchor="middle">Echo 維持 HIGH 的時間 = 聲音來回的時間</text></svg>')

def hc_schematic():
    G7, SL, CL = bb.GRAY7, bb.SLATE, bb.CLAY
    o = ['<g class="el" data-part="HC1" tabindex="0" role="button" aria-label="超音波模組 HC1,點一下看它在麵包板上的位置">'
         '<rect class="halo" x="108" y="26" width="160" height="164" rx="12" fill="none" stroke="%s" stroke-width="2.5"/>'
         '<rect x="120" y="34" width="136" height="148" rx="8" fill="#F0EEE6" stroke="%s" stroke-width="1.8"/>' % (CL, G7),
         bb._txt(188, 112, "HC-SR04", "mb", SL), bb._txt(188, 128, "超音波模組", "s", bb.GRAY5)]
    for nm, y, side in (("VCC", 62, "L"), ("GND", 154, "L"), ("Trig", 74, "R"), ("Echo", 142, "R")):
        if side == "L":
            o.append(bb._txt(130, y + 4, nm, "m", SL, "start"))
        else:
            o.append(bb._txt(246, y + 4, nm, "m", SL, "end"))
    o.append("</g>")
    o.append('<line x1="120" y1="62" x2="78" y2="62" stroke="%s" stroke-width="2"/><line x1="78" y1="62" x2="78" y2="42" stroke="%s" stroke-width="2"/>' % (G7, G7))
    o.append('<line x1="62" y1="42" x2="94" y2="42" stroke="%s" stroke-width="2.4" stroke-linecap="round"/>' % G7 + bb._txt(78, 34, "5V", "mb", bb.RUST))
    o.append('<line x1="120" y1="154" x2="78" y2="154" stroke="%s" stroke-width="2"/><line x1="78" y1="154" x2="78" y2="172" stroke="%s" stroke-width="2"/>' % (G7, G7))
    for k, wd in enumerate((28, 18, 8)):
        o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.2" stroke-linecap="round"/>' % (78 - wd / 2, 172 + k * 7, 78 + wd / 2, 172 + k * 7, G7))
    for nm, y, lab in (("Trig", 74, "Uno D9"), ("Echo", 142, "Uno D10")):
        o.append('<line x1="256" y1="%d" x2="300" y2="%d" stroke="%s" stroke-width="2"/>' % (y, y, G7))
        o.append('<rect x="300" y="%d" width="80" height="30" rx="8" fill="#F0EEE6" stroke="%s" stroke-width="1.5"/>%s' % (y - 15, G7, bb._txt(340, y + 4, lab, "mb", SL)))
    o.append(bb._txt(278, 62, "輸出 →", "m", bb.GRAY5) + bb._txt(278, 130, "← 輸入", "m", bb.GRAY5))
    o.append('<circle cx="40" cy="106" r="10" fill="%s"/><text x="40" y="109.5" class="mb" fill="#FFFFFF" text-anchor="middle">1</text>' % CL)
    return ('<svg viewBox="0 0 420 210" role="img" aria-label="HC-SR04 原理圖" style="min-width:420px"><defs>%s</defs><rect width="420" height="210" fill="#FFFFFF"/>%s</svg>' % (bb.STYLE, "".join(o)))

bz_circ = bb.Circuit("sonar-bz", 22, parts=CIRC.parts, steps=CIRC.steps, chains=[["UNO.D12", "R2", "BZ1", "UNO.GND"]])
BZ_SCH, BZ_LEG = bb.schematic_svg(bz_circ, mark=())

sonicsim = ('<div class="panel" data-sonicsim><div class="wgrid f2"><div><label>物體距離(公分)</label><input type="range" min="2" max="400" value="20" data-so="d"></div><div></div></div>'
            '<div class="pot-bar" aria-hidden="true"><span></span></div><div class="rc-out so-out" aria-live="polite"></div></div>')

what = section("what", "用聲音量距離:像蝙蝠一樣",
  '<div class="panel"><h3>HC-SR04 怎麼量</h3>'
  '<ol style="margin:0;padding-left:20px"><li><b>Arduino 在 Trig 腳送出一個 10 微秒的 HIGH 脈衝</b>,告訴模組「開始量」。</li>'
  '<li>模組發出 8 個 40 kHz 的超音波(人耳聽不到),碰到物體會反彈回來。</li>'
  '<li><b>模組把 Echo 腳拉成 HIGH,直到收到回波才放下。</b>HIGH 持續的時間,就是聲音<b>來回</b>的時間。</li>'
  '<li>Arduino 用 <code>pulseIn()</code> 量這段 HIGH 有多長,再用聲速換算成距離。</li></ol></div>',
  canvas(timing_svg(), []),
  '<h3 style="margin-top:26px">從時間換算成距離</h3>',
  '<div class="panel"><p style="margin:0">聲速約 343 公尺/秒 = <b>0.0343 公分/微秒</b>。聲音<b>來回</b>走了兩倍距離,所以:<br><b>距離(公分)= 時間(微秒)× 0.0343 ÷ 2</b>(也可簡化成 ÷ 58)</p></div>',
  '<p style="margin-top:14px">拖拖看,距離和回波時間的關係:</p>', sonicsim,
  table("g2", ["規格(HC-SR04 常見資料手冊)", "數值"], [
    ["工作電壓", "5 V,工作電流約 15 mA"], ["量測範圍", "約 2–400 公分,精度約 0.3 公分"], ["量測角度", "約 15 度的錐形範圍"], ["觸發訊號", "Trig 送 10 微秒的 TTL 脈衝"], ["量測間隔", "建議兩次量測至少隔 60 毫秒"],
  ]),
  tip("這些是常見資料手冊的數值,<b>以你手上的模組為準</b>。表面柔軟(衣服、沙發)、太斜、或太小的物體,聲音反射不好,量到的值可能不準或量不到。"))

wire = section("wire", "接線:超音波(9、10 號腳)加蜂鳴器(12 號腳)",
  '<p class="sub" style="margin-bottom:14px">模組四隻腳:VCC 接 5V、GND 接 GND、<b>Trig 接 9 號腳(輸出)</b>、<b>Echo 接 10 號腳(輸入)</b>。蜂鳴器和第 6 篇一樣,串 220Ω 電阻。</p>',
  bb.stepper_html(CIRC),
  '<p class="sk">Uno 轉了 180 度擺放,5V 在上緣,要繞過左邊。圖只畫左邊 22 欄,<b>模組尺寸不是按比例畫的</b>,實物比圖大。以欄號與 a–j 為準(手機上可以左右滑動圖)。</p>',
  '<h3 style="margin-top:26px">接線表</h3>', bb.wiring_table(CIRC),
  warn("<b>VCC 與 GND 不能接反。</b>接反會讓模組發燙損壞。接線前先拔 USB,並對照模組上印的 VCC、Trig、Echo、GND 文字,不要只靠位置猜。", "注意"),
  '<h3 style="margin-top:26px">原理圖</h3>',
  '<p class="sub">HC-SR04 在原理圖上是一個方框,四邊標明腳位;<b>Trig 是輸出(Arduino → 模組),Echo 是輸入(模組 → Arduino)</b>。</p>',
  canvas(hc_schematic(), [("1", '<span class="newsym">新符號</span><b>模組方框</b>:電路圖裡常用方框代表一個整合好的模組或晶片,只畫出它的接腳,不畫內部。')]),
  '<h3 style="margin-top:18px">蜂鳴器那一組</h3>',
  canvas(BZ_SCH, []),
  '<div class="linkbox" id="linkInfo" style="margin-top:12px">點原理圖裡的模組、電阻或蜂鳴器,看它在麵包板上是哪一個。</div>')

fillsec = section("fill", "先填入你的數值",
  fill([("gap", "程式一:兩次量測的間隔(毫秒)", True), ("far", "程式二:幾公分以內才響", True)]),
  '<p class="sk">空白時用範例值:500 毫秒、60 公分。</p>')

def exp(items):
    return table("g2", ["這一行", "它在做什麼"], items)

code1 = section("code1", "程式一:量距離並印出來",
  cmd(U1, cap="HC-SR04:印出距離", cpp=True),
  exp([
    ["<code>delayMicroseconds(10);</code>", "暫停 10 <b>微秒</b>(1 毫秒 = 1000 微秒)。<code>delay</code> 的單位是毫秒,<code>delayMicroseconds</code> 是微秒,不要弄混。"],
    ["<code>pulseIn(ECHO_PIN, HIGH, 30000)</code>", "<b>量脈衝長度</b>:等 Echo 變成 HIGH,量它維持多久(微秒)。第三個參數是<b>最多等 30000 微秒</b>(30 毫秒),等不到就回傳 0,不會卡死。"],
    ["<code>long duration</code>", "<code>long</code> 是能放<b>更大整數</b>的變數(比 <code>int</code> 大很多)。時間的微秒數可能超過 <code>int</code> 的上限,所以用 <code>long</code>。"],
    ["<code>duration * 0.0343 / 2</code>", "換算成公分。有小數點的 0.0343,結果就會是 <code>float</code>。"],
    ["<code>Serial.print(distance, 1);</code>", "第二個參數 1 表示印<b>小數點後 1 位</b>(第 8 篇學過)。"],
  ]),
  see("Serial Monitor(baud 9600)每 0.5 秒印一行距離,例如 <code>23.4 cm</code>。拿手或書本在模組前面前後移動,數字跟著變。前面沒有東西或太遠時,印 <code>out of range</code>。"),
  tip("先用一本書(硬、平面)正對模組當目標,用尺量實際距離,和 Serial Monitor 比對。誤差在 1 公分左右是正常的。"))

code2 = section("code2", "程式二:倒車雷達雛形",
  '<p class="sub" style="margin-bottom:14px">把量距離包成一個<b>自己定義的函式</b> <code>readDistanceCm()</code>,主程式就很好讀。距離越近,蜂鳴器嗶得越快。</p>',
  cmd(U2, cap="越近越密集的嗶聲", cpp=True),
  exp([
    ["<code>float readDistanceCm() { … }</code>", "<b>會回傳值的函式</b>:前面的 <code>float</code> 是回傳的資料型態。函式裡用 <code>return</code> 把結果交出去。量不到就回傳 -1。"],
    ["<code>map((int)d, 5, {far}, 50, 500)</code>", "把「距離 5–{far} 公分」對應成「間隔 50–500 毫秒」。<code>(int)d</code> 把小數轉成整數(<code>map</code> 只收整數,第 9 篇提過)。"],
    ["<code>constrain(gap, 50, 500);</code>", "<b>限制範圍</b>:小於 50 就當 50,大於 500 就當 500。避免距離不到 5 公分時間隔變負數。"],
    ["<code>d &gt; 0 &amp;&amp; d &lt; {far}</code>", "量得到(&gt; 0),<b>而且</b>在範圍內才響(第 10 篇學過 <code>&amp;&amp;</code>)。"],
  ]),
  see("手從遠處靠近:<b>先是慢慢嗶、嗶、嗶,越近越密,最後幾乎連成一片</b>;拿開或超出範圍,就安靜。"),
  warn("這段程式每次量測與 <code>delay</code> 時,Arduino 都在等。第 15 篇的 <code>millis()</code> 會教你不卡住的做法,讓第 18 篇的綜合專案可以同時顯示距離。", "先記著"))

try_ = section("try", "改改看",
  table("g3", ["挑戰", "怎麼改", "你會看到"], [
    ["改靈敏度", "「幾公分以內才響」改 30", "只有很近時才響。"],
    ["距離顯示更精確", "程式一的 <code>Serial.print(distance, 1)</code> 改 <code>2</code>", "小數點後兩位,數字跳動更明顯(但不代表更準)。"],
    ["用 LED 代替蜂鳴器", "把蜂鳴器換成第 3 篇的 LED(接 12 號腳),程式不用改", "越近閃越快。"],
  ]))

gotchas = section("gotchas", "常見卡關",
  details("一直印 out of range(量不到)",
    ops(["<b>Trig 與 Echo 接反</b>:Trig 要接 9 號腳(輸出),Echo 接 10 號腳。", "<b>VCC 或 GND 沒接好</b>:模組沒電就沒有回波。用手摸模組是否微熱(小心別壓到針腳)。", "<b>前面沒有東西、或東西太斜、太軟</b>:換成一本書正對模組。", "程式與接線的腳位不一致。"]), True) +
  details("距離一直是固定的怪數字",
    "<p>可能是 Echo 腳浮接,或針腳沒插好。用力按一下模組、確認四隻針腳都在孔裡,再重新上傳。</p>") +
  details("數字亂跳很大",
    "<p>聲音可能反射到旁邊的牆或桌面。把目標放在正前方、周圍淨空;也可以連續量幾次取平均(之後的進階做法)。</p>") +
  details("蜂鳴器一直響或完全不響",
    "<p>檢查蜂鳴器的 + 腳方向與 12 號腳的橘線;程式二的 <code>BUZZER_PIN</code> 要是 12;蜂鳴器是<b>主動式</b>。</p>") +
  details("Serial Monitor 空白",
    "<p>baud 要選 9600(第 8 篇);有沒有開 Serial Monitor;程式一有 <code>Serial.begin(9600)</code>,程式二沒有(它只用蜂鳴器)。</p>"))

SIM = {
  "a1": "<b>不用。</b>固定量不到,通常是接線或腳位的問題,和 IDE 無關。",
  "a2": "<b>對。</b>先確認 Trig 在 9 號腳、Echo 在 10 號腳,VCC 接 5V、GND 接 GND;再把一本書正對模組,距離約 20 公分試試。",
  "a3": "<b>沒有用。</b>蜂鳴器的電阻不影響距離量測。",
}
QUIZ = quiz_cfg([
  ("HC-SR04 的 Trig 腳功能是?", ["接收回波時間", "接收 Arduino 的觸發脈衝,開始量測", "供電"], 1, "Trig 由 Arduino 輸出 10 微秒脈衝,觸發量測。"),
  ("Echo 腳 HIGH 的時間代表?", ["聲音來回的時間", "單程時間", "溫度"], 0, "HIGH 的長度 = 聲音發出去再回來的總時間。"),
  ("回波時間 1166 微秒,距離約?", ["20 公分", "40 公分", "2 公分"], 0, "1166 × 0.0343 ÷ 2 ≈ 20。"),
  ("為什麼要除以 2?", ["聲速太快", "量到的是來回,距離只要單程", "模組有兩個探頭"], 1, "聲音走到物體再回來,是兩倍距離。"),
  ("<code>pulseIn(ECHO_PIN, HIGH, 30000)</code> 的第三個參數是?", ["最多等待的時間(微秒),超過就回傳 0", "要量幾次", "距離上限"], 0, "避免沒有回波時程式永遠等下去。"),
])
practice = section("practice", "動手演練與延伸閱讀",
  sim("", "情境:Serial Monitor 一直印 out of range", "你應該先?",
      [("a1", "重新安裝 IDE"), ("a2", "確認 Trig 接 9、Echo 接 10、VCC 接 5V、GND 接 GND,並把書擋在前方"), ("a3", "換蜂鳴器的電阻")]),
  QUIZ_HTML,
  checks(["我能說出 HC-SR04 量距離的四個步驟。",
          "我知道 Trig 是輸出、Echo 是輸入,並且接線沒有接反。",
          "我能解釋距離 = 時間 × 0.0343 ÷ 2。",
          "我的 Serial Monitor 能印出合理的距離。",
          "我知道 <code>pulseIn</code>、<code>delayMicroseconds</code>、<code>long</code> 各是什麼。",
          "我的倒車雷達:越近,嗶得越快。"], "做完之後,對照這張清單"),
  resources([
    ("https://docs.arduino.cc/language-reference/en/functions/advanced-io/pulseIn/", "pulseIn()", "Arduino language reference"),
    ("https://docs.arduino.cc/language-reference/en/functions/time/delayMicroseconds/", "delayMicroseconds()", "Arduino language reference"),
    ("https://docs.arduino.cc/language-reference/en/functions/math/constrain/", "constrain()", "Arduino language reference"),
  ], "Arduino 官方文件"))

SPEC = dict(
    dir="arduino",
    file="arduino-ultrasonic-guide.html",
    title="超音波測距 HC-SR04:倒車雷達雛形",
    eyebrow="第 11 篇 · 超音波",
    h1="用聲音量距離:越近,蜂鳴器嗶得越快",
    sub="認識 HC-SR04:Trig 送出脈衝、Echo 回報時間,用 pulseIn 量時間再換算成公分;最後做出越近越快的倒車雷達雛形。",
    tldr="<strong>Trig 送 10 微秒脈衝 → Echo 的 HIGH 長度 = 聲音來回時間</strong>。<code>pulseIn()</code> 量時間,<code>距離(cm) = 時間(µs) × 0.0343 ÷ 2</code>。把量測包成自己的函式,用 <code>map</code> 與 <code>constrain</code> 決定嗶聲間隔。",
    toc=[("what", "運作原理"), ("wire", "接線"), ("fill", "填入數值"), ("code1", "程式一:量與印"), ("code2", "程式二:倒車雷達"), ("try", "改改看"), ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
    body="\n\n".join([what, wire, fillsec, code1, code2, try_, gotchas, practice]),
    config=dict(fill=FILL, sim=SIM, quiz=QUIZ, wiring=[bb.wiring_config(CIRC)], parts=bb.parts_info(CIRC)),
    prev=("arduino-ldr-guide.html", "光敏電阻小夜燈"),
    next=("arduino-servo-guide.html", "伺服馬達 SG90"),
)
