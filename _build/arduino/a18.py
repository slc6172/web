# -*- coding: utf-8 -*-
from h import *
import bb

CIRC = bb.Circuit(
    "parking-sensor", 30, mode="both",
    parts=[
        bb.HCSR04("HC1", "e5", "e6", "e7", "e8", 1),
        bb.Resistor("R2", 220, "b13", "b17", 2), bb.Buzzer("BZ1", "active", "d17", "d20", 2),
        bb.Resistor("R1", 220, "b22", "b26", 2), bb.LED("LED1", "red", "d26", "d27", 2),
        bb.LCD("LCD1", 3),
        bb.Wire("P", "a5", "t+5", "red", 4, route="straight"), bb.Wire("G8", "a8", "t-8", "black", 4, route="straight"),
        bb.Wire("K2", "a20", "t-20", "black", 4, route="straight"), bb.Wire("K1", "a27", "t-27", "black", 4, route="straight"),
        bb.Wire("LP", "t+30", "b+30", "red", 4, route="straight"), bb.Wire("LG", "t-29", "b-29", "black", 4, route="straight"),
        bb.Wire("LV", "MOD.VCC", "b+24", "red", 4, route="vs"), bb.Wire("LGND", "MOD.GND", "b-25", "black", 4, route="vs"),
        bb.Wire("T", "UNO.D9", "a6", "blue", 5), bb.Wire("E", "UNO.D10", "a7", "green", 5), bb.Wire("B", "UNO.D12", "a13", "orange", 5),
        bb.Wire("LD", "UNO.D13", "a22", "purple", 5),
        bb.Wire("SDA", "UNO.SDA", "MOD.SDA", "blue", 5, route="right"), bb.Wire("SCL", "UNO.SCL", "MOD.SCL", "yellow", 5, route="right1"),
        bb.Wire("V5", "UNO.5V", "t+1", "red", 6, route="left"), bb.Wire("G", "UNO.GND", "t-24", "black", 6),
    ],
    steps=[
        ("放超音波模組(第 11 篇)", "四隻針腳插 <code>e5</code>(VCC)、<code>e6</code>(Trig)、<code>e7</code>(Echo)、<code>e8</code>(GND),<b>先看模組上印的字再對</b>。"),
        ("放蜂鳴器與 LED(第 6、3 篇)", "<b>蜂鳴器組</b>:電阻 <code>b13–b17</code>、蜂鳴器 + 腳 <code>d17</code>、− 腳 <code>d20</code>。<br><b>LED 組</b>:電阻 <code>b22–b26</code>、紅 LED 長腳 <code>d26</code>、短腳 <code>d27</code>。"),
        ("擺好 LCD(第 14 篇)", "LCD 放在麵包板下方,<b>背面朝上、不插麵包板</b>。轉接板的四隻針腳要接母頭杜邦線(<b>先看轉接板上印的字</b>,順序依廠牌而異)。"),
        ("短線與電源軌連接", "① 紅 <code>a5</code> → <code>t+5</code>、黑 <code>a8</code> → <code>t-8</code>(模組電源)。<br>② 黑 <code>a20</code> → <code>t-20</code>、黑 <code>a27</code> → <code>t-27</code>(蜂鳴器與 LED 負極)。<br>③ 紅 <code>t+30</code> → <code>b+30</code>、黑 <code>t-29</code> → <code>b-29</code>:把<b>上下電源軌連起來</b>,下方的軌才有電。<br>④ LCD 的 <b>VCC</b> → <code>b+24</code>,<b>GND</b> → <code>b-25</code>(從下方電源軌取電,Uno 只有一個 5V 腳,不夠直接接這麼多)。"),
        ("訊號線", "藍 Uno <b>9</b> → <code>a6</code>(Trig)、綠 Uno <b>10</b> → <code>a7</code>(Echo)、橘 Uno <b>12</b> → <code>a13</code>(蜂鳴器)、紫 Uno <b>13</b> → <code>a22</code>(LED)。<br>LCD:藍 Uno <b>SDA</b> → LCD <b>SDA</b>、黃 Uno <b>SCL</b> → LCD <b>SCL</b>(兩條線繞過麵包板右側)。"),
        ("電源線:5V 與 GND", "紅線:Uno <b>5V</b> → <code>t+1</code>。黑線:Uno 數位腳位排的 <b>GND</b> → <code>t-24</code>。"),
    ],
    chains=[["UNO.5V", "HC1.VCC"], ["HC1.TRIG", "UNO.D9"], ["HC1.ECHO", "UNO.D10"], ["HC1.GND", "UNO.GND"],
            ["UNO.D12", "R2", "BZ1", "UNO.GND"], ["UNO.D13", "R1", "LED1", "UNO.GND"],
            ["UNO.5V", "LCD1.VCC"], ["LCD1.GND", "UNO.GND"], ["LCD1.SDA", "UNO.SDA"], ["LCD1.SCL", "UNO.SCL"]],
    intro="先<strong>拔掉 USB 線</strong>。這一篇把前面學過的合在一起:<b>超音波量距離、LCD 顯示、蜂鳴器與 LED 警示</b>。接線全是你接過的,只是放在同一塊板子上;<b>一步一步來,每步檢查</b>。",
    done="超音波 Trig 9、Echo 10;蜂鳴器 12;LED 13;LCD 走 SDA、SCL;所有電源與 GND 都接到共用的電源軌。檢查:<b>上下兩條電源軌有用兩條線連起來</b>。",
)
CIRCUITS = [CIRC]

CODE = """// 第 18 篇:倒車雷達——用 millis() 同時做好幾件事
#include <Wire.h>
#include <hd44780.h>
#include <hd44780ioClass/hd44780_I2Cexp.h>

hd44780_I2Cexp lcd;

const int TRIG_PIN = 9;
const int ECHO_PIN = 10;
const int BUZZER_PIN = 12;
const int LED_PIN = 13;

const float FAR_CM = {far};                         // 超過這個距離就安靜
const float NEAR_CM = {near};                       // 小於這個距離,LED 亮
const unsigned long MEASURE_INTERVAL = 100;         // 每 100 毫秒量一次距離
const unsigned long LCD_INTERVAL = 250;             // 每 250 毫秒更新一次螢幕

unsigned long lastMeasure = 0;
unsigned long lastLcd = 0;
unsigned long lastBeep = 0;
float distanceCm = -1;                              // 最新的距離;-1 代表量不到
bool beepOn = false;

float readDistanceCm() {                            // 第 11 篇的量距離函式
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
  pinMode(LED_PIN, OUTPUT);
  int status = lcd.begin(16, 2);
  if (status) {
    hd44780::fatalError(status);
  }
  lcd.print("Parking Sensor");
}

void loop() {
  unsigned long now = millis();

  // ---- 工作 1:定時量距離 ----
  if (now - lastMeasure >= MEASURE_INTERVAL) {
    lastMeasure = now;
    distanceCm = readDistanceCm();
  }

  // ---- 工作 2:定時更新螢幕 ----
  if (now - lastLcd >= LCD_INTERVAL) {
    lastLcd = now;
    lcd.setCursor(0, 1);
    if (distanceCm < 0) {
      lcd.print("out of range    ");
    } else {
      lcd.print(distanceCm, 1);
      lcd.print(" cm       ");                      // 多印空白,蓋掉殘留的字
    }
  }

  // ---- 工作 3:蜂鳴器,越近越密(不用 delay)----
  if (distanceCm > 0 && distanceCm < FAR_CM) {
    int gap = map((int)distanceCm, 5, (int)FAR_CM, 50, 500);
    gap = constrain(gap, 50, 500);
    unsigned long interval = beepOn ? 30 : gap;     // 響 30 毫秒,停 gap 毫秒
    if (now - lastBeep >= interval) {
      lastBeep = now;
      beepOn = !beepOn;
      if (beepOn) {
        digitalWrite(BUZZER_PIN, HIGH);
      } else {
        digitalWrite(BUZZER_PIN, LOW);
      }
    }
  } else {
    beepOn = false;
    digitalWrite(BUZZER_PIN, LOW);
  }

  // ---- 工作 4:太近就亮 LED ----
  if (distanceCm > 0 && distanceCm < NEAR_CM) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
}
"""
SIM_CODE = (CODE.replace("#include <hd44780.h>\n#include <hd44780ioClass/hd44780_I2Cexp.h>\n", "")
            .replace("hd44780_I2Cexp lcd;", "struct FakeLCD { int begin(int, int) { return 0; } void setCursor(int, int) {} void print(const char *) {} void print(float, int) {} } lcd;")
            .replace("    hd44780::fatalError(status);\n", ""))
FILL = dict(far="60", near="25")
pulses = []
t = 1.0
while t < 1400:
    pulses += [("D10", 1, round(t, 3)), ("D10", 0, round(t + 1.1666, 4))]
    t += 10.0
SKETCHES = [
    dict(name="parking", code=CODE, fill=FILL, circuit=CIRC, libs=["Wire", "hd44780"],
         code_pins={"TRIG_PIN": "UNO.D9", "ECHO_PIN": "UNO.D10", "BUZZER_PIN": "UNO.D12", "LED_PIN": "UNO.D13"},
         sim_code=SIM_CODE, sim_libs=["Wire"],
         sim=dict(kind="dual", pins=["D12", "D13"], seconds=0.85, inputs=[("D10", 0, 0)] + pulses,
                  toggle=None, edges=[("D13", [(1, 102)], 6), ("D12", [(1, 165), (0, 195), (1, 359), (0, 388), (1, 553), (0, 583), (1, 747), (0, 776)], 8)], note="每 10 ms 一個約 20 cm 的回波(LED 該亮、蜂鳴器依距離嗶)")),
]

what = section("what", "把學過的合在一起:倒車雷達",
  '<div class="panel"><h3>要做的東西</h3>'
  '<p>一個<b>會用聲音、燈光與螢幕告訴你距離</b>的倒車雷達:超音波量距離,LCD 顯示幾公分,蜂鳴器<b>越近嗶得越快</b>,太近時 LED 亮起。</p>'
  '<p style="margin-bottom:0">每個零件你都做過了,這一篇的新東西只有一個:<b>把好幾件事排進同一個 <code>loop()</code>,各自按自己的節奏進行</b>(第 15 篇的 <code>millis()</code>)。</p></div>',
  '<h3 style="margin-top:26px">用到哪幾篇學過的東西</h3>',
  table("g3", ["零件 / 觀念", "出自", "在這個專案的角色"], [
    ["HC-SR04 超音波、<code>pulseIn</code>", "第 11 篇", "量到前方物體的距離"],
    ["LCD1602 I2C、<code>hd44780</code>", "第 14 篇", "顯示距離"],
    ["蜂鳴器、<code>map</code> / <code>constrain</code>", "第 6、9、11 篇", "越近嗶得越密"],
    ["LED", "第 3 篇", "太近時亮燈"],
    ["<code>millis()</code> 與狀態變數", "第 15 篇", "讓四件事同時進行,不卡住"],
    ["自己定義的函式 <code>readDistanceCm()</code>", "第 11 篇", "把量距離包起來,主程式好讀"],
  ]),
  '<h3 style="margin-top:26px">距離與反應</h3>',
  table("g3", ["距離", "蜂鳴器", "LED"], [
    ["超過 60 公分,或量不到", "安靜", "滅"],
    ["25–60 公分", "慢慢嗶(間隔最多 0.5 秒)", "滅"],
    ["5–25 公分", "越近越密(間隔最短 50 毫秒)", "<b>亮</b>"],
  ]),
  tip("<b>先確認每個零件單獨能動</b>(第 11、14 篇)再合在一起。這是做大專案最重要的習慣:一次只加一樣,出問題才知道是誰。"))

wire = section("wire", "接線:這次是全部合在一起",
  '<p class="sub" style="margin-bottom:14px">每一組你都接過。新增的只有:<b>LCD 的電源取自下方電源軌</b>(Uno 只有一個 5V 腳),所以上下電源軌要用兩條線連起來。圖很寬,手機上可以左右滑動。</p>',
  bb.stepper_html(CIRC),
  '<p class="sk">Uno 轉了 180 度擺放。LCD 與超音波模組<b>不是按比例畫的</b>。以接線表與模組上印的針腳名稱為準。</p>',
  '<h3 style="margin-top:26px">接線表</h3>', bb.wiring_table(CIRC),
  warn("<b>VCC 與 GND 不能接反</b>(超音波、LCD 都會損壞);<b>SDA、SCL 不要接反</b>。每加一組,先通電檢查有沒有發燙,再加下一組。接線前先拔 USB。", "注意"),
  '<div class="linkbox" id="linkInfo" style="margin-top:12px">點圖上的零件,看它在其他圖的位置。</div>')

fillsec = section("fill", "先填入你的距離設定",
  fill([("far", "幾公分以內才開始嗶", True), ("near", "幾公分以內 LED 亮", True)]),
  '<p class="sk">空白時用範例值:60 公分、25 公分。</p>')

def exp(items):
    return table("g2", ["這一段", "它在做什麼"], items)

code = section("code", "完整程式",
  cmd(CODE, cap="倒車雷達:四個工作共用一個 loop", cpp=True),
  '<h3 style="margin-top:22px">怎麼讀這支程式</h3>',
  exp([
    ["最上面的 <code>const</code> 與變數", "把「設定」集中在一起:腳位、距離門檻、時間間隔。以後要調整,只改這裡。每個定時的工作各有一個 <code>lastXxx</code> 記上次的時間。"],
    ["<code>readDistanceCm()</code>", "第 11 篇的量距離函式,原封不動搬過來。"],
    ["<code>setup()</code>", "設定腳位,啟動 LCD(<code>begin</code> 失敗就用 L 燈閃爍報錯並停住),印出標題。"],
    ["工作 1:定時量距離", "每 100 毫秒量一次,把結果放進 <code>distanceCm</code>。<b>量測結果存起來,其他工作只讀這個變數</b>,不各自重新量。"],
    ["工作 2:定時更新螢幕", "每 250 毫秒更新第二行。LCD 更新比較慢,不用太頻繁,也不影響其他工作。"],
    ["工作 3:蜂鳴器", "用 <code>beepOn</code> 記「現在是在響還是在停」:響 30 毫秒,停的時間依距離而定。<b>用時間差決定何時切換</b>,沒有 <code>delay</code>。"],
    ["工作 4:LED", "太近就亮,否則滅。"],
  ]),
  see("手(或一本書)由遠而近靠近超音波:<b>LCD 顯示的距離變小,蜂鳴器由慢變快,小於 25 公分時紅 LED 亮起</b>;離開或超出範圍,全部安靜,LCD 顯示 <code>out of range</code>。"),
  tip("這種寫法叫<b>協同工作(cooperative multitasking)</b>:沒有誰是老大,每個工作都快速檢查一下「該不該動」,不該動就立刻讓出去。<code>loop()</code> 每一圈都很短,所以每件事都很即時。"))

tune = section("tune", "調整與除錯",
  table("g3", ["想要", "改什麼", "說明"], [
    ["更早開始嗶", "「幾公分以內才開始嗶」調大(例如 100)", "超音波有效範圍到約 400 公分,但近距離最準"],
    ["嗶聲更急促", "<code>map</code> 的 <code>50, 500</code> 改成 <code>30, 300</code>", "最短與最長的間隔"],
    ["螢幕更新更快", "<code>LCD_INTERVAL</code> 調小", "LCD 更新太快,字會閃"],
    ["數字更穩", "加上平均(連續量 3 次取平均)", "超音波偶爾會跳一下;這是進階的小改良"],
    ["加第二個 LED", "再加 <code>NEAR_CM</code> 與 <code>FAR_CM</code> 之間的黃燈", "做成「綠、黃、紅」三段警示"],
  ]),
  '<h3 style="margin-top:22px">怎麼分段除錯</h3>',
  ops(["<b>先看 Serial</b>:暫時在工作 1 後面加一行 <code>Serial.println(distanceCm);</code>(第 8 篇),看量到的距離對不對。", "<b>再看輸出</b>:距離對了,蜂鳴器與 LED 還不對,就是工作 3、4 的邏輯;距離不對,回去查超音波接線(第 11 篇)。", "<b>LCD 沒字</b>:調對比旋鈕(第 14 篇)。<b>L 燈一直閃</b>:LCD 沒找到,檢查 SDA、SCL 與電源。"]))

gotchas = section("gotchas", "常見卡關",
  details("整個系統沒反應,或 Uno 一直重開機",
    "<p>電流不夠或短路。立刻拔掉 USB,檢查 5V 與 GND 有沒有碰在一起;<b>上下電源軌是否用兩條線連好</b>;逐一拔掉模組,找出是哪一組造成的。</p>", True) +
  details("LCD 完全不亮或 L 燈在閃",
    "<p>LCD 的電源取自下方電源軌:確認 <code>t+30→b+30</code> 與 <code>t-29→b-29</code> 兩條連接線有接,以及 LCD 的 VCC、GND 有插到 <code>b+24</code>、<code>b-25</code>。</p>") +
  details("蜂鳴器一直響或很不規則",
    "<p>檢查 <code>loop()</code> 裡有沒有誤用 <code>delay()</code>;距離變數是否正確。也可能是超音波讀值亂跳,先用 Serial 看一下距離。</p>") +
  details("距離一直是 out of range",
    "<p>回到第 11 篇:Trig、Echo 腳位,VCC、GND,以及前方要有硬平面。這一篇的超音波接法和第 11 篇相同。</p>") +
  details("改了程式之後燈亂閃",
    "<p>檢查每個工作的 <code>lastXxx = now;</code> 有沒有寫(漏了就會每一圈都觸發),以及比較用的是減法、變數是 <code>unsigned long</code>。</p>"))

SIM = {
  "a1": "<b>不要全部重寫。</b>先找出是哪一組出問題:一次拿掉一組(只留超音波 + Serial),各個零件單獨測試。",
  "a2": "<b>對。</b>大專案要「分段驗證」:先確認超音波的距離(用 Serial),再確認蜂鳴器與 LED 的邏輯,最後看 LCD。出問題時就知道是哪一段。",
  "a3": "<b>沒有用。</b>換 USB 線不能分辨是哪一個零件出問題。",
}
QUIZ = quiz_cfg([
  ("為什麼這個專案不用 <code>delay()</code>?", ["讓量距離、顯示、蜂鳴器能同時進行,互不卡住", "因為 delay 會讓 LCD 壞掉", "因為 delay 太貴"], 0, "delay 會讓整個程式睡覺。"),
  ("每個定時工作需要什麼?", ["一個記「上次時間」的 unsigned long 變數", "一個 delay", "一個 Serial"], 0, "用時間差決定何時再做。"),
  ("為什麼量測結果存進 <code>distanceCm</code> 變數?", ["其他工作共用,不用各自重新量", "為了讓程式變慢", "因為函式不能回傳值"], 0, "量一次,大家用。"),
  ("LCD 更新間隔(250 ms)比量測間隔(100 ms)長,有什麼好處?", ["不讓慢速的 LCD 拖累其他工作,也避免畫面閃", "讓 LCD 比較省電", "沒有好處"], 0, "每個工作的節奏可以不同。"),
  ("接線時上下兩條電源軌要用兩條線連起來,是為了?", ["讓下方電源軌也有 5V 與 GND,供應 LCD", "讓麵包板更美觀", "沒有用"], 0, "麵包板上下的電源軌彼此不相通。"),
])
practice = section("practice", "動手演練與延伸閱讀",
  sim("", "情境:全部接好後,什麼都沒反應,Uno 還一直重新開機", "你應該先?",
      [("a1", "把程式全部重寫"), ("a2", "拔掉 USB,一次接回一組,每次檢查有沒有發燙或重開機"), ("a3", "換 USB 線")]),
  QUIZ_HTML,
  checks(["我的超音波、蜂鳴器、LED、LCD 單獨都能運作。",
          "我把它們接在同一塊板子上,接線依表檢查過。",
          "我的 LCD 顯示距離,距離越近,數字越小。",
          "我的蜂鳴器越近嗶得越快,小於門檻時 LED 亮。",
          "我能說出每個「工作」怎麼用 <code>millis()</code> 計時、為什麼不用 <code>delay()</code>。",
          "遇到問題,我會「分段驗證」:先看距離,再看輸出,再看螢幕。"], "做完之後,對照這張清單"),
  resources([
    ("https://docs.arduino.cc/language-reference/en/functions/time/millis/", "millis()", "Arduino language reference"),
    ("https://docs.arduino.cc/language-reference/en/functions/math/constrain/", "constrain()", "Arduino language reference"),
    ("https://docs.arduino.cc/language-reference/en/functions/advanced-io/pulseIn/", "pulseIn()", "Arduino language reference"),
  ], "Arduino 官方文件"))

SPEC = dict(
    dir="arduino",
    file="arduino-project-guide.html",
    title="綜合專案:倒車雷達",
    eyebrow="第 18 篇 · 綜合專案",
    h1="把學到的全部合起來:做一個倒車雷達",
    sub="超音波量距離、LCD 顯示、蜂鳴器越近越密、LED 警示。四件事用 millis() 排進同一個 loop,互不卡住。",
    tldr="<strong>量測、顯示、蜂鳴器、LED 四個工作</strong>各自用 <code>millis()</code> 的時間差決定何時動,<strong>loop() 裡不用 delay()</strong>。量測結果存進變數,大家共用。接線:超音波 9/10、蜂鳴器 12、LED 13、LCD 走 SDA/SCL;<strong>上下電源軌要連起來</strong>。",
    toc=[("what", "專案概覽"), ("wire", "接線"), ("fill", "填入設定"), ("code", "完整程式"), ("tune", "調整與除錯"), ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
    body="\n\n".join([what, wire, fillsec, code, tune, gotchas, practice]),
    config=dict(fill=FILL, sim=SIM, quiz=QUIZ, wiring=[bb.wiring_config(CIRC)], parts=bb.parts_info(CIRC)),
    prev=("arduino-bus-guide.html", "I2C 與 SPI 通訊"),
    next=("arduino-troubleshoot-guide.html", "故障排除總整理"),
)
