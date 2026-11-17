# -*- coding: utf-8 -*-
from h import *
import bb

CIRC = bb.Circuit(
    "servo-pot", 22,
    parts=[
        bb.Servo("SV1", "e5", "e6", "e7", 1),
        bb.Pot("POT1", "d12", "d13", "d14", 2),
        bb.Wire("G5", "a5", "t-5", "black", 3, route="straight"), bb.Wire("V6", "a6", "t+6", "red", 3, route="straight"),
        bb.Wire("P12", "a12", "t+12", "red", 3, route="straight"), bb.Wire("P14", "a14", "t-14", "black", 3, route="straight"),
        bb.Wire("SG", "UNO.D9", "a7", "orange", 4), bb.Wire("SA", "UNO.A0", "a13", "green", 4, route="left"),
        bb.Wire("V5", "UNO.5V", "t+1", "red", 5, route="left1"), bb.Wire("G", "UNO.GND", "t-20", "black", 5),
    ],
    steps=[
        ("接上伺服馬達", "SG90 的線尾是<b>三孔母頭插座</b>。把三條<b>公對公杜邦線</b>的一端分別插進插座,另一端插麵包板:<br><b>棕線(GND)</b> → <code>e5</code>、<b>紅線(5V)</b> → <code>e6</code>、<b>橘線(訊號)</b> → <code>e7</code>。<br>圖上的彩色線是 SG90 自己的線與轉接的杜邦線合起來的示意,杜邦線的顏色不必相同;重點是<b>對準棕、紅、橘三個接點</b>。"),
        ("放電位器", "電位器三隻腳插 <code>d12</code>、<code>d13</code>(中間腳)、<code>d14</code>(第 9 篇接過)。旋鈕等一下用來控制角度。"),
        ("四條短線", "① 黑 <code>a5</code> → <code>t-5</code>:伺服 GND 接 − 軌。<br>② 紅 <code>a6</code> → <code>t+6</code>:伺服 5V 接 + 軌。<br>③ 紅 <code>a12</code> → <code>t+12</code>:電位器一端接 + 軌。<br>④ 黑 <code>a14</code> → <code>t-14</code>:電位器另一端接 − 軌。"),
        ("訊號線:9 號腳與 A0", "橘線:Uno <b>9 號腳</b> → <code>a7</code>(伺服的<b>訊號線</b>)。<br>綠線:Uno <b>A0</b> → <code>a13</code>(電位器中間腳)。"),
        ("電源線:5V 與 GND", "紅線:Uno <b>5V</b> → <code>t+1</code>。黑線:Uno 數位腳位排的 <b>GND</b> → <code>t-20</code>。"),
    ],
    chains=[["UNO.5V", "SV1.VCC"], ["UNO.5V", "POT1.1"], ["SV1.GND", "UNO.GND"], ["POT1.2", "UNO.GND"], ["UNO.D9", "SV1.SIG"], ["POT1.W", "UNO.A0"]],
    intro="先<strong>拔掉 USB 線</strong>。SG90 有三條線:<b>棕 = GND、紅 = 5V、橘 = 訊號</b>。訊號線接 9 號腳,電位器接 A0,等一下用旋鈕控制角度。",
    done="伺服:GND、5V、訊號(9 號腳)。電位器:兩端 5V 與 GND,中間腳 A0。檢查:<b>棕、紅、橘不要插錯</b>,尤其紅線(5V)與棕線(GND)不能對調。",
)
CIRCUITS = [CIRC]

S1 = """// 第 12 篇:讓伺服馬達來回掃動
#include <Servo.h>              // 引入內建的 Servo 函式庫

Servo myServo;                  // 建立一個伺服馬達「物件」
const int SERVO_PIN = 9;

void setup() {
  myServo.attach(SERVO_PIN);    // 告訴函式庫:伺服的訊號線接在 9 號腳
}

void loop() {
  for (int angle = 0; angle <= 180; angle += 1) {   // 0 度慢慢轉到 180 度
    myServo.write(angle);                           // 轉到 angle 度
    delay({step});                                  // 給馬達一點時間轉過去
  }
  for (int angle = 180; angle >= 0; angle -= 1) {   // 再轉回來
    myServo.write(angle);
    delay({step});
  }
}
"""
S2 = """// 第 12 篇:指定三個角度
#include <Servo.h>

Servo myServo;
const int SERVO_PIN = 9;

void setup() {
  myServo.attach(SERVO_PIN);
}

void loop() {
  myServo.write(0);       // 轉到 0 度
  delay(1000);            // 停 1 秒
  myServo.write(90);      // 轉到 90 度(中間)
  delay(1000);
  myServo.write(180);     // 轉到 180 度
  delay(1000);
}
"""
S3 = """// 第 12 篇:用旋鈕控制伺服馬達的角度
#include <Servo.h>

Servo myServo;
const int SERVO_PIN = 9;
const int POT_PIN = A0;

void setup() {
  myServo.attach(SERVO_PIN);
}

void loop() {
  int value = analogRead(POT_PIN);                // 0–1023
  int angle = map(value, 0, 1023, 0, 180);        // 換成 0–180 度
  myServo.write(angle);
  delay(15);                                      // 給馬達一點時間
}
"""
FILL = dict(step="15")
SKETCHES = [
    dict(name="servo-sweep", code=S1, fill=FILL, circuit=CIRC, code_pins={"SERVO_PIN": "UNO.D9"}, libs=["Servo"],
         sim=dict(kind="servo", pin="D9", seconds=2.2, expect=[(500, 884), (1000, 1224), (2000, 1915)], tol=40)),
    dict(name="servo-fixed", code=S2, fill=FILL, circuit=CIRC, code_pins={"SERVO_PIN": "UNO.D9"}, libs=["Servo"],
         sim=dict(kind="servo", pin="D9", seconds=3.0, expect=[(500, 544), (1500, 1472), (2500, 2400)], tol=40)),
    dict(name="servo-pot", code=S3, fill=FILL, circuit=CIRC, code_pins={"SERVO_PIN": "UNO.D9"}, libs=["Servo"],
         sim=dict(kind="servo", pin="D9", seconds=1.5, adc=[(0, 1000, 0), (0, 2500, 500), (0, 4000, 1000)], expect=[(300, 905), (800, 1462), (1300, 2018)], tol=40)),
]

servosim = ('<div class="panel" data-servosim><div class="wgrid f2"><div><label>myServo.write( 角度 )</label><input type="range" min="0" max="180" value="90" data-sv="a"></div><div></div></div>'
            '<div class="canvas" style="margin-top:8px"><svg viewBox="0 0 520 190" role="img" aria-label="伺服馬達角度與脈衝寬度" style="min-width:480px;display:block"><defs>' + bb.STYLE + '</defs>'
            '<text x="12" y="60" class="mb" fill="#3D3D3A">訊號</text>'
            '<line x1="50" y1="40" x2="450" y2="40" stroke="#D1CFC5" stroke-dasharray="3 4"/><line x1="50" y1="110" x2="450" y2="110" stroke="#D1CFC5"/>'
            '<polyline class="sv-wave" points="" fill="none" stroke="#D97757" stroke-width="3" stroke-linejoin="round"/>'
            '<text x="250" y="140" class="m" fill="#87867F" text-anchor="middle">一個週期 20 毫秒(每秒 50 次)</text>'
            '<g><path d="M300,130 A100,100 0 0 1 500,130" fill="none" stroke="#D1CFC5" stroke-width="2"/>'
            '<line class="sv-arm" x1="400" y1="130" x2="500" y2="130" stroke="#3D3D3A" stroke-width="7" stroke-linecap="round"/>'
            '<circle cx="400" cy="130" r="10" fill="#4C78A8" stroke="#141413"/></g>'
            '<text x="300" y="150" class="m" fill="#87867F" text-anchor="middle">180°</text><text x="500" y="150" class="m" fill="#87867F" text-anchor="middle">0°</text></svg>'
            '<div class="rc-out sv-out" aria-live="polite"></div></div>')

what = section("what", "伺服馬達:能轉到「指定角度」的馬達",
  '<div class="panel"><h3>它和一般馬達哪裡不同</h3>'
  '<p>一般馬達通電就一直轉。<b>伺服馬達</b>(servo)裡面有位置感測,你告訴它<b>要轉到幾度</b>,它就轉到那個位置並維持住。常用在機器手臂、遙控車轉向、機關。</p>'
  '<p style="margin-bottom:0">SG90 是最常見的小型伺服,<b>轉動範圍約 0–180 度</b>。三條線:<b>棕 = GND、紅 = 5V、橘 = 訊號</b>。</p></div>',
  '<h3 style="margin-top:26px">角度怎麼告訴它:脈衝寬度</h3>',
  '<p>訊號線上<b>每 20 毫秒送一次脈衝</b>,<b>脈衝 HIGH 的長度決定角度</b>:短(約 0.5 毫秒)轉到一端,長(約 2.4 毫秒)轉到另一端。Arduino 的 Servo 函式庫幫你處理,你只要說角度。拖拖看:</p>',
  servosim,
  '<h3 style="margin-top:26px">用電要注意(很重要)</h3>',
  warn("<b>伺服馬達吃電比 LED 多很多。</b>常見的 SG90 資料:<b>無負載動作約 100–250 mA,被卡住(堵轉)時可超過 500 mA</b>(以你的規格為準)。USB 通常最多供應約 500 mA。<b>只動一顆、不帶重物</b>通常可以由 Uno 的 5V 供電;若 Uno 重開機、LED 變暗、馬達抖動,就要改用外接的 4.8–6V 電源(例如 4 顆 AA 電池盒)供電給伺服,並讓外接電源的<b>負極與 Uno 的 GND 接在一起</b>。", "電流"),
  tip("<b>絕對不要用手強行扭轉搖臂,也不要讓它頂住東西持續用力。</b>馬達卡住時電流最大、最容易燒壞。"))

wire = section("wire", "接線:伺服馬達(9 號腳)加電位器(A0)",
  '<p class="sub" style="margin-bottom:14px">伺服的<b>棕、紅、橘</b>三條線分別接 GND、5V、9 號腳;電位器和第 9 篇一樣,接 A0。</p>',
  bb.stepper_html(CIRC),
  '<p class="sk">Uno 轉了 180 度擺放:A0 與 5V 在上緣,要繞過左邊。圖只畫左邊 22 欄,<b>伺服的大小不是按比例畫的</b>。以欄號與 a–j 為準(手機上可以左右滑動圖)。</p>',
  '<h3 style="margin-top:26px">接線表</h3>', bb.wiring_table(CIRC),
  warn("<b>紅線(5V)與棕線(GND)不要接反。</b>接反可能損壞伺服。接線前先拔 USB;三條線的顏色以 SG90 自己的線為準,杜邦線顏色可以不同。", "注意"),
  '<div class="linkbox" id="linkInfo" style="margin-top:12px">點圖上的伺服馬達或電位器,在其他圖也會跟著亮。</div>')

fillsec = section("fill", "先填入掃動的速度",
  fill([("step", "每轉 1 度,等待幾毫秒", True)]),
  '<p class="sk">空白時用範例值 15 毫秒:整個 0→180 度約 2.7 秒。填小一點會更快,但馬達可能追不上。</p>')

def exp(items):
    return table("g2", ["這一行", "它在做什麼"], items)

code1 = section("code1", "程式一:來回掃動(第一次用函式庫)",
  '<div class="panel"><h3>什麼是函式庫</h3><p style="margin-bottom:0"><b>函式庫(library)就是別人寫好的「工具箱」</b>。伺服馬達要精確的脈衝很麻煩,Arduino 附的 <b>Servo</b> 函式庫已經做好,你只要用就行。Servo 是 IDE <b>內建</b>的,不用另外安裝(下一篇會教怎麼安裝別人的函式庫)。</p></div>',
  cmd(S1, cap="伺服馬達來回掃動", cpp=True),
  exp([
    ["<code>#include &lt;Servo.h&gt;</code>", "<b>引入函式庫</b>,寫在程式最上面。也可以用選單 <b>Sketch → Include Library → Servo</b> 讓 IDE 幫你加。"],
    ["<code>Servo myServo;</code>", "<b>建立一個 Servo 物件</b>,取名叫 <code>myServo</code>。把它想成「一顆伺服馬達的遙控器」;有幾顆伺服,就建立幾個。"],
    ["<code>myServo.attach(SERVO_PIN);</code>", "告訴它這顆伺服的訊號線接在哪個腳位。<code>物件名.函式名()</code> 的寫法,代表「叫這個物件做某件事」。"],
    ["<code>myServo.write(angle);</code>", "轉到 <code>angle</code> 度(0–180)。"],
  ]),
  see("搖臂從一端<b>慢慢轉到另一端,再慢慢轉回來</b>,不斷重複。"),
  tip("Servo 函式庫使用了 Uno 的 Timer1,所以<b>用了 Servo 之後,9 號與 10 號腳不能再用 <code>analogWrite</code> 做 PWM</b>(Arduino 官方文件說明)。這也是這篇把伺服接在 9 號腳時要知道的事:第 6 篇的呼吸燈要換到 3、5、6、11 號腳。"))

code2 = section("code2", "程式二:指定角度",
  cmd(S2, cap="轉到 0、90、180 度,各停 1 秒", cpp=True),
  see("搖臂依序轉到 0 度、90 度(正中間)、180 度,各停 1 秒,重複。"),
  warn("<code>write(0)</code> 與 <code>write(180)</code> 是函式庫的範圍,但<b>你手上的 SG90 實際機械範圍可能略小</b>。如果搖臂到端點時<b>發出嗡嗡聲、持續抖動</b>,表示它頂到底了:把範圍縮小一點(例如 10–170)。", "別頂到底"))

code3 = section("code3", "程式三:用旋鈕控制角度",
  cmd(S3, cap="電位器 → map → 伺服角度", cpp=True),
  exp([
    ["<code>analogRead(POT_PIN)</code>", "讀電位器,0–1023(第 9 篇)。"],
    ["<code>map(value, 0, 1023, 0, 180)</code>", "換成 0–180 度。這和上一篇把 0–1023 換成 0–255 是同樣的手法。"],
    ["<code>delay(15);</code>", "讓馬達有時間轉到,也避免一直重送指令。"],
  ]),
  see("<b>旋鈕轉到哪,搖臂就跟著轉到哪</b>。慢慢轉比較平順;快速轉,搖臂會追著跑。"))

try_ = section("try", "改改看",
  table("g3", ["挑戰", "怎麼改", "你會看到"], [
    ["調速度", "程式一的間隔改 5,再改 40", "5:掃得很快;40:很慢。"],
    ["縮小範圍", "程式一把 <code>0</code>、<code>180</code> 改成 <code>30</code>、<code>150</code>", "只在中間 120 度範圍內掃動,不會頂到底。"],
    ["相反方向", "程式三 <code>map(value, 0, 1023, 180, 0)</code>", "旋鈕往同一個方向轉,搖臂方向顛倒。"],
  ]))

gotchas = section("gotchas", "常見卡關",
  details("伺服完全不動",
    ops(["<b>三條線有沒有接對</b>:棕 GND、紅 5V、橘訊號(9 號腳)。", "<b>杜邦線有沒有真的插進伺服的插座</b>(公對公的針腳要插緊)。", "程式裡 <code>attach(9)</code> 與接線的 9 號腳一致。", "USB 有沒有接上、程式有沒有上傳成功。"]), True) +
  details("伺服抖動、Uno 重開機、LED 變暗",
    "<p>電流不夠(伺服啟動與轉動時瞬間電流大)。先拿掉負重;還是不行就用外接的 4.8–6V 電源供電給伺服,並<b>和 Uno 共用 GND</b>。USB 供電的電腦孔不夠力時也會這樣,換一個孔或接有電源的 USB 集線器。</p>") +
  details("轉到端點時發出嗡嗡聲",
    "<p>頂到機械極限了。縮小角度範圍(例如 10–170),不要讓它持續頂著。</p>") +
  details("搖臂轉的角度和我寫的不一樣",
    "<p>正常有誤差。搖臂是用小螺絲鎖在轉軸上,裝的位置本來就可能偏。先 <code>write(90)</code>,再把搖臂拆下來、以你要的「正中間」位置重新裝上。</p>") +
  details("呼吸燈在伺服的專案裡不能用",
    "<p>用了 Servo 函式庫,9、10 號腳的 PWM 會被停用。把呼吸燈換到 3、5、6、11 號腳。</p>"))

SIM = {
  "a1": "<b>不用。</b>先看供電:伺服啟動瞬間電流大,USB 供電不足時 Uno 會重開機、馬達會抖動。",
  "a2": "<b>對。</b>先拿掉負重。還是不穩,改用外接 4.8–6V 電源供電給伺服,並讓它的負極與 Uno 的 GND 接在一起。",
  "a3": "<b>沒有用。</b>伺服的訊號腳不需要電阻,問題在供電。",
}
QUIZ = quiz_cfg([
  ("SG90 的三條線分別是?", ["棕 GND、紅 5V、橘 訊號", "紅 GND、棕 5V、橘 訊號", "橘 GND、紅 訊號、棕 5V"], 0, "棕=GND、紅=電源、橘=訊號。"),
  ("伺服馬達的角度是由什麼決定的?", ["電壓大小", "訊號腳上 HIGH 脈衝的長度", "電流大小"], 1, "每 20 毫秒一次,脈衝越長,角度越大。"),
  ("<code>Servo myServo;</code> 這行做什麼?", ["建立一個 Servo 物件,之後用它控制馬達", "宣告腳位", "設定 baud"], 0, "物件就像一顆伺服的遙控器。"),
  ("伺服抖動、Uno 重開機,最可能的原因?", ["程式寫錯", "電流不夠(供電不足)", "角度太小"], 1, "伺服電流大,USB 供電可能不夠。"),
  ("用了 Servo 函式庫,哪些腳位不能用 analogWrite?", ["3 與 11", "9 與 10", "5 與 6"], 1, "Servo 使用 Timer1,影響 9、10 號腳的 PWM。"),
])
practice = section("practice", "動手演練與延伸閱讀",
  sim("", "情境:伺服一轉動,Uno 就重新開機、馬達抖動", "你應該先?",
      [("a1", "改寫程式"), ("a2", "拿掉負重;還是不行就改用外接電源,並共用 GND"), ("a3", "在訊號線加電阻")]),
  QUIZ_HTML,
  checks(["我知道伺服馬達是「轉到指定角度」,三條線各是什麼。",
          "我能說出脈衝寬度決定角度,Servo 函式庫幫我處理。",
          "我知道 <code>#include</code>、物件、<code>attach</code>、<code>write</code> 各做什麼。",
          "我的伺服能掃動、轉到指定角度,也能用旋鈕控制。",
          "我知道伺服吃電多,不要讓它卡住,不夠力時要外接電源並共用 GND。",
          "我知道 Servo 會停用 9、10 號腳的 PWM。"], "做完之後,對照這張清單"),
  resources([
    ("https://docs.arduino.cc/libraries/servo/", "Servo 函式庫", "Servo library"),
    ("https://docs.arduino.cc/language-reference/en/functions/math/map/", "map()", "Arduino language reference"),
  ], "Arduino 官方文件"))

SPEC = dict(
    dir="arduino",
    file="arduino-servo-guide.html",
    title="伺服馬達 SG90:第一次使用函式庫",
    eyebrow="第 12 篇 · 伺服馬達",
    h1="讓馬達轉到你指定的角度",
    sub="認識 SG90 伺服馬達,第一次使用函式庫與物件,並留意它的用電;最後用旋鈕控制它的角度。",
    tldr="SG90 三條線:<strong>棕 GND、紅 5V、橘 訊號</strong>。<code>#include &lt;Servo.h&gt;</code>、<code>Servo myServo;</code>、<code>myServo.attach(9)</code>、<code>myServo.write(角度)</code>。<strong>伺服吃電多</strong>,不要讓它卡住;不夠力時外接電源並<strong>共用 GND</strong>。",
    toc=[("what", "伺服與用電"), ("wire", "接線"), ("fill", "填入速度"), ("code1", "程式一:掃動"), ("code2", "程式二:指定角度"), ("code3", "程式三:旋鈕控制"),
         ("try", "改改看"), ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
    body="\n\n".join([what, wire, fillsec, code1, code2, code3, try_, gotchas, practice]),
    config=dict(fill=FILL, sim=SIM, quiz=QUIZ, wiring=[bb.wiring_config(CIRC)], parts=bb.parts_info(CIRC)),
    prev=("arduino-ultrasonic-guide.html", "超音波測距 HC-SR04"),
    next=("arduino-dht-guide.html", "溫濕度 DHT11 與安裝函式庫"),
)
