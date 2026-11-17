# -*- coding: utf-8 -*-
from h import *
import bb

parts = [bb.Button("BTN1", "e5", "f7", "e7", "f5", 1),
         bb.Resistor("R1", 220, "b11", "b15", 2), bb.LED("LED1", "red", "d15", "d16", 2),
         bb.Resistor("R2", 220, "b19", "b23", 2), bb.LED("LED2", "yellow", "d23", "d24", 2),
         bb.Wire("K1", "a16", "t-16", "black", 3, route="straight"), bb.Wire("K2", "a24", "t-24", "black", 3, route="straight"),
         bb.Wire("KB", "j7", "b-7", "black", 3, route="straight"), bb.Wire("L", "t-26", "b-26", "green", 3, route="straight"),
         bb.Wire("S2", "UNO.D2", "a5", "blue", 4), bb.Wire("S1", "UNO.D8", "a11", "orange", 4), bb.Wire("S3", "UNO.D9", "a19", "purple", 4),
         bb.Wire("G", "UNO.GND", "t-20", "black", 5)]
CIRC = bb.Circuit(
    "millis-demo", 26, parts=parts,
    steps=[
        ("放按鈕", "和第 7 篇一樣:按鈕跨在中間凹槽上,<b>對角</b>兩腳 <code>e5</code>、<code>f7</code> 接線(另外兩腳 <code>e7</code>、<code>f5</code> 只是插著)。"),
        ("放兩組電阻與 LED", "<b>第一組</b>:電阻 <code>b11–b15</code>、<b>紅色 LED</b> 長腳 <code>d15</code>、短腳 <code>d16</code>(自動閃爍用)。<br><b>第二組</b>:電阻 <code>b19–b23</code>、<b>黃色 LED</b> 長腳 <code>d23</code>、短腳 <code>d24</code>(按鈕控制用)。"),
        ("四條黑 / 綠短線", "① <code>a16</code> → <code>t-16</code>、② <code>a24</code> → <code>t-24</code>:兩顆 LED 負極接 − 軌。<br>③ <code>j7</code> → <code>b-7</code>:按鈕下腳接下方 − 軌。<br>④ 綠線 <code>t-26</code> → <code>b-26</code>:上下 − 軌連起來(第 7 篇學過)。"),
        ("三條訊號線:2、8、9 號腳", "藍線:Uno <b>2 號腳</b> → <code>a5</code>(按鈕)。<br>橘線:Uno <b>8 號腳</b> → <code>a11</code>(紅燈,自動閃)。<br>紫線:Uno <b>9 號腳</b> → <code>a19</code>(黃燈,按鈕控制)。"),
        ("GND 線", "黑線:Uno 數位腳位排的 <b>GND</b> → <code>t-20</code>。"),
    ],
    chains=[["UNO.D8", "R1", "LED1", "UNO.GND"], ["UNO.D9", "R2", "LED2", "UNO.GND"], ["UNO.D2", "BTN1", "UNO.GND"]],
    intro="先<strong>拔掉 USB 線</strong>。這次要讓<b>兩件事同時進行</b>:紅燈自己一直閃,同時黃燈由按鈕控制。接法就是把第 7 篇與第 6 篇的兩組合在一起。",
    done="按鈕 → 2 號腳;紅 LED → 8 號腳;黃 LED → 9 號腳;共用 GND。檢查:兩顆 LED 長腳都朝向自己的電阻。",
)
CIRCUITS = [CIRC]

A = """// 第 15 篇(寫法一):不用 delay 讓 LED 閃爍
const int LED_PIN = 8;
const unsigned long INTERVAL = {interval};   // 每隔幾毫秒切換一次
unsigned long previousMillis = 0;            // 上一次切換是什麼時候
bool ledOn = false;

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  unsigned long currentMillis = millis();                  // 現在是開機後的第幾毫秒
  if (currentMillis - previousMillis >= INTERVAL) {        // 距離上次,已經過了足夠的時間嗎?
    previousMillis = currentMillis;                        // 記下這次的時間
    ledOn = !ledOn;                                        // 切換狀態
    if (ledOn) {
      digitalWrite(LED_PIN, HIGH);
    } else {
      digitalWrite(LED_PIN, LOW);
    }
  }
  // 這裡沒有 delay:loop() 會飛快地一直重複,有空就去做別的事
}
"""
B = """// 第 15 篇(寫法二):兩件事同時進行——LED1 自己閃,按鈕控制 LED2
const int BUTTON_PIN = 2;
const int LED1_PIN = 8;
const int LED2_PIN = 9;

const unsigned long BLINK_INTERVAL = {interval};
unsigned long previousMillis = 0;
bool led1On = false;

const unsigned long DEBOUNCE = 30;      // 去彈跳時間(毫秒)
int lastReading = HIGH;                 // 上一次讀到的按鈕狀態
int buttonState = HIGH;                 // 穩定後的按鈕狀態
unsigned long lastChange = 0;           // 按鈕讀值上次變化的時間
bool led2On = false;

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED1_PIN, OUTPUT);
  pinMode(LED2_PIN, OUTPUT);
}

void loop() {
  unsigned long now = millis();

  // ---- 工作 1:LED1 每 BLINK_INTERVAL 毫秒切換一次 ----
  if (now - previousMillis >= BLINK_INTERVAL) {
    previousMillis = now;
    led1On = !led1On;
    if (led1On) {
      digitalWrite(LED1_PIN, HIGH);
    } else {
      digitalWrite(LED1_PIN, LOW);
    }
  }

  // ---- 工作 2:按鈕按一下,LED2 切換(不卡住的去彈跳)----
  int reading = digitalRead(BUTTON_PIN);
  if (reading != lastReading) {          // 讀值變了:重新計時,先別相信它
    lastChange = now;
  }
  if (now - lastChange > DEBOUNCE) {     // 讀值已經穩定超過 30 毫秒
    if (reading != buttonState) {        // 而且和上次確認的狀態不同
      buttonState = reading;
      if (buttonState == LOW) {          // 變成 LOW:按下
        led2On = !led2On;
        if (led2On) {
          digitalWrite(LED2_PIN, HIGH);
        } else {
          digitalWrite(LED2_PIN, LOW);
        }
      }
    }
  }
  lastReading = reading;
}
"""
C = """// 對照組:用 delay() 寫的同一件事(會漏掉按鈕!)
const int BUTTON_PIN = 2;
const int LED1_PIN = 8;
const int LED2_PIN = 9;
bool led2On = false;

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED1_PIN, OUTPUT);
  pinMode(LED2_PIN, OUTPUT);
}

void loop() {
  digitalWrite(LED1_PIN, HIGH);
  delay(500);                        // 睡 0.5 秒:這段時間完全看不到按鈕
  digitalWrite(LED1_PIN, LOW);
  delay(500);                        // 再睡 0.5 秒
  if (digitalRead(BUTTON_PIN) == LOW) {   // 每 1 秒才看一次按鈕
    led2On = !led2On;
    if (led2On) {
      digitalWrite(LED2_PIN, HIGH);
    } else {
      digitalWrite(LED2_PIN, LOW);
    }
  }
}
"""
FILL = dict(interval="500")
bounce = [("D2", 1, 0), ("D2", 0, 700), ("D2", 1, 702), ("D2", 0, 704), ("D2", 1, 900), ("D2", 0, 902), ("D2", 1, 905)]
SKETCHES = [
    dict(name="millis-blink", code=A, fill=FILL, circuit=CIRC, code_pins={"LED_PIN": "UNO.D8"},
         sim=dict(kind="toggle", pin="D8", seconds=3.2, period_ms=500, tol_ms=3)) if False else
    dict(name="millis-blink", code=A, fill=FILL, circuit=CIRC, code_pins={"LED_PIN": "UNO.D8"},
         sim=dict(kind="dual", pins=["D8", "D9"], seconds=3.2, inputs=[("D2", 1, 0)], toggle=("D8", 500, 3), note="只量紅燈")),
    dict(name="millis-two-tasks", code=B, fill=FILL, circuit=CIRC, code_pins={"BUTTON_PIN": "UNO.D2", "LED1_PIN": "UNO.D8", "LED2_PIN": "UNO.D9"},
         sim=dict(kind="dual", pins=["D8", "D9"], seconds=3.2, inputs=bounce, toggle=("D8", 500, 3), edges=[("D9", [(1, 734)], 5)],
                  note="紅燈每 500 ms 切換,同時在 700–900 ms 按一下(帶彈跳)按鈕")),
    dict(name="delay-misses", code=C, fill=FILL, circuit=CIRC, code_pins={"BUTTON_PIN": "UNO.D2", "LED1_PIN": "UNO.D8", "LED2_PIN": "UNO.D9"},
         sim=dict(kind="dual", pins=["D8", "D9"], seconds=2.4, inputs=[("D2", 1, 0), ("D2", 0, 1200), ("D2", 1, 1300)], toggle=None, edges=[("D9", [], 5)],
                  note="在 delay 期間(1200–1300 ms)按一下按鈕:黃燈完全沒反應")),
]

dsim = ('<div class="panel" data-delaysim><div class="wgrid f2"><div><button type="button" class="primary" data-ds="tap" style="width:100%">按一下按鈕(0.3 秒)</button></div><div><button type="button" class="ghost" data-ds="reset" style="width:100%">重來</button></div></div>'
        '<div class="ds-grid"><div><b>delay() 版</b><br>紅燈(LED1)<span class="led ds-d1"></span>黃燈(LED2)<span class="led ds-d2"></span></div>'
        '<div><b>millis() 版</b><br>紅燈(LED1)<span class="led ds-m1"></span>黃燈(LED2)<span class="led ds-m2"></span></div></div>'
        '<div class="rc-out ds-log" aria-live="polite" style="margin-top:12px"></div></div>')

what = section("what", "delay() 的問題:它在睡覺,什麼都不做",
  '<p class="sub" style="margin-bottom:14px">到目前為止,我們用 <code>delay()</code> 等時間。但 <code>delay(500)</code> 的意思是:<b>Arduino 整整睡 0.5 秒,期間什麼都不看、什麼都不做</b>,包括按鈕。想要「LED 一直閃,同時還能按按鈕」,用 <code>delay()</code> 就會漏掉按鈕。</p>',
  '<h3 style="margin-top:6px">先親眼看一次</h3>',
  '<p>下面並排兩個版本:<b>delay() 版</b>(每 1 秒才看一次按鈕)與 <b>millis() 版</b>(隨時都在看)。<b>點「按一下按鈕」</b>,看黃燈的反應。可以多點幾次、點在不同時間:</p>',
  dsim,
  tip("這就是為什麼 <code>delay()</code> 只適合「同時只做一件事」的簡單程式。一旦要「<b>同時做好幾件事</b>」(閃燈、讀按鈕、量距離、更新螢幕……),就要換成 <code>millis()</code> 的寫法。第 18 篇的綜合專案就靠它。"))

mill = section("mill", "millis():看一眼時鐘,而不是站著等",
  '<div class="panel"><h3>比喻:煮泡麵</h3>'
  '<p><b>delay(180000)</b> 像是站在爐子前面盯著鍋子三分鐘,什麼都不能做。<b>millis()</b> 像是記下現在幾點,然後<b>去忙別的事,時不時看一眼時鐘</b>:「現在離我下鍋已經過 3 分鐘了嗎?」到了才關火。</p></div>',
  '<p style="margin-top:14px"><b><code>millis()</code></b> 回傳「<b>從開機到現在,過了幾毫秒</b>」,型態是 <code>unsigned long</code>(只有正數、很大的整數)。這個數字一直往上跑。</p>',
  '<h3 style="margin-top:22px">固定的寫法</h3>',
  '<div class="panel"><pre style="margin:0;font:13px/1.7 var(--mono);white-space:pre-wrap">unsigned long now = millis();\nif (now - previousMillis >= INTERVAL) {   // 距離上次已過 INTERVAL 毫秒?\n  previousMillis = now;                   // 記下這次的時間\n  // 在這裡做你要定時做的事\n}</pre></div>',
  ops(["<b>每一件定時的事,各用一個 <code>previousMillis</code> 變數</b>記「上次是什麼時候」。", "判斷用<b>減法</b>:<code>現在 − 上次 ≥ 間隔</code>,不要用 <code>現在 ≥ 上次 + 間隔</code>。", "整個 <code>loop()</code> 裡<b>不要有 delay()</b>。"]),
  table("g2", ["為什麼用減法", "說明"], [
    ["<code>unsigned long</code> 會「繞一圈」", "它最大約 42.9 億,毫秒數跑到上限(約 <b>49.7 天</b>)會歸零重新開始。"],
    ["減法剛好不受影響", "無號整數相減,<b>即使中間歸零,算出的「過了多久」仍然正確</b>。用加法比較就會在那一刻出錯。"],
  ]),
  warn("<b>不要把 <code>millis()</code> 的結果放進 <code>int</code>。</code>int</code> 最大只能放 32767,約 32 秒就溢位,程式會莫名其妙壞掉。一定要用 <code>unsigned long</code>。".replace("</code>int</code>", "<code>int</code>"), "型態要對"))

wire = section("wire", "接線:按鈕(2)、紅 LED(8)、黃 LED(9)",
  '<p class="sub" style="margin-bottom:14px">把第 7 篇的按鈕、第 3 篇的 LED 合在一起,多加一顆黃燈。</p>',
  bb.stepper_html(CIRC),
  '<p class="sk">Uno 轉了 180 度擺放,數位腳位排在下緣。圖只畫左邊 26 欄,以欄號與 a–j 為準(手機上可以左右滑動圖)。</p>',
  '<h3 style="margin-top:26px">接線表</h3>', bb.wiring_table(CIRC),
  warn("按鈕一樣要用<b>對角的兩隻腳</b>,並跨在中間凹槽上(第 7 篇)。兩顆 LED 的長腳都朝向自己的電阻。接線前先拔 USB。", "提醒"),
  '<div class="linkbox" id="linkInfo" style="margin-top:12px">點圖上的零件,看它在其他圖的位置。</div>')

fillsec = section("fill", "先填入紅燈閃爍的間隔",
  fill([("interval", "紅燈每隔幾毫秒切換一次", True)]),
  '<p class="sk">空白時用範例值 500 毫秒(閃一次完整的亮滅是 1 秒)。</p>')

def exp(items):
    return table("g2", ["這一行", "它在做什麼"], items)

code1 = section("code1", "寫法一:不用 delay 讓 LED 閃",
  cmd(A, cap="millis() 版 Blink", cpp=True),
  exp([
    ["<code>unsigned long previousMillis = 0;</code>", "記「上次切換是什麼時候」。<b>寫在函式外面</b>,值才會一直保留。"],
    ["<code>unsigned long currentMillis = millis();</code>", "看一眼時鐘:現在是開機後第幾毫秒。"],
    ["<code>currentMillis - previousMillis &gt;= INTERVAL</code>", "距離上次已經過了 500 毫秒嗎?"],
    ["<code>previousMillis = currentMillis;</code>", "到了:把「上次」更新成現在。"],
    ["<code>ledOn = !ledOn;</code>", "切換狀態(第 7 篇學過 <code>!</code>)。"],
  ]),
  see("紅燈每 0.5 秒切換一次(亮 0.5 秒、滅 0.5 秒),和 delay 版看起來一樣。差別在<b>程式沒有在睡覺</b>。"))

code2 = section("code2", "寫法二:兩件事同時進行",
  cmd(B, cap="紅燈自己閃、按鈕控制黃燈", cpp=True),
  exp([
    ["<code>// ---- 工作 1 ---- / // ---- 工作 2 ----</code>", "把 <code>loop()</code> 分成幾個<b>互不干擾的工作</b>。每一個工作快速檢查一下「該不該做」,不該做就立刻跳過。"],
    ["<code>if (reading != lastReading) { lastChange = now; }</code>", "按鈕讀值一變,就記下時間。"],
    ["<code>if (now - lastChange &gt; DEBOUNCE)</code>", "讀值<b>穩定超過 30 毫秒</b>,才相信它。這是第 7 篇去彈跳的「不卡住」版本:不再用 <code>delay</code>,而是用時間差判斷。"],
    ["<code>buttonState</code> 與 <code>lastReading</code>", "<code>lastReading</code> 是上次讀到的,<code>buttonState</code> 是穩定後確認的狀態。兩者分開,才能分辨「真的按下」與「抖動」。"],
  ]),
  see("<b>紅燈照樣每 0.5 秒一次規律地閃,同時按一下按鈕,黃燈立刻切換</b>,不論你什麼時候按,都不會漏。按住不放也不影響紅燈。"),
  '<h3 style="margin-top:22px">對照:同樣的事用 delay 寫</h3>',
  details("看看 delay 版(它會漏掉按鈕)", cmd(C, cap="對照組:delay 版", cpp=True) + '<p style="margin:12px 0 0">這支程式每一輪 <code>loop()</code> 要 1 秒,而且<b>只在最後才看一次按鈕</b>。你在紅燈閃的任何時刻短按按鈕,它多半「醒來」時你已經放開,<b>按鈕就被漏掉了</b>(上面的互動示範可以看到)。</p>'))

try_ = section("try", "改改看",
  table("g3", ["挑戰", "怎麼改", "你會看到"], [
    ["三個節奏", "再加一顆 LED(或用蜂鳴器),用第三組 <code>previousMillis</code>,間隔 800 毫秒", "兩個燈各自以不同節奏閃,互不干擾。"],
    ["改閃爍速度", "「紅燈間隔」改成 100,再改成 1000", "按鈕反應速度完全不受影響。"],
    ["按住加速", "按鈕按住時把 <code>BLINK_INTERVAL</code> 變成 100,放開變回 500", "按住紅燈閃得快,放開恢復。"],
  ]))

gotchas = section("gotchas", "常見卡關",
  details("LED 完全不閃,或閃爍的間隔不對",
    ops(["<code>previousMillis</code> 是不是<b>寫在函式外面</b>(放進 <code>loop()</code> 裡每輪都會重設成 0)。", "變數是不是 <code>unsigned long</code>,不是 <code>int</code>。", "比較用的是<b>減法</b>。", "有沒有不小心留下 <code>delay()</code>。"]), True) +
  details("按鈕有時候沒反應",
    "<p>檢查 <code>loop()</code> 裡有沒有任何地方還在用 <code>delay()</code>,或是某個工作花太久(例如一次印很多 Serial 資料)。<b>每一輪 <code>loop()</code> 都要很快跑完</b>。</p>") +
  details("按一下,黃燈切換了兩次(又變回去)",
    "<p>去彈跳沒做好。確認 <code>DEBOUNCE</code> 不是 0,而且判斷的是<b>穩定之後</b>的狀態。</p>") +
  details("跑了很久之後怪怪的",
    "<p>如果你的 <code>millis()</code> 結果用了 <code>int</code> 或 <code>long</code>(有號),大約 32 秒或 24 天後會溢位出問題。改成 <code>unsigned long</code>,並用減法比較。</p>"))

SIM = {
  "a1": "<b>對。</b>delay 期間 Arduino 在睡覺,看不到按鈕。要同時做多件事,改用 millis() 計時,讓 <code>loop()</code> 一直跑、隨時檢查按鈕。",
  "a2": "<b>不對。</b>把 delay 縮短只是讓漏掉的機率變低,還是會漏,而且閃爍的節奏也變了。根本辦法是不要睡覺。",
  "a3": "<b>沒有用。</b>換更大的電阻不影響程式的時序。",
}
QUIZ = quiz_cfg([
  ("<code>delay(500)</code> 期間,Arduino 在做什麼?", ["什麼都不做(也看不到按鈕)", "繼續讀按鈕", "進入省電模式"], 0, "delay 就是睡覺等時間。"),
  ("<code>millis()</code> 回傳的是?", ["從開機到現在經過的毫秒數", "現在的時間(幾點幾分)", "電壓"], 0, "開機後經過的毫秒數。"),
  ("為什麼用 <code>現在 − 上次 ≥ 間隔</code>(減法)?", ["寫起來比較短", "即使 millis() 歸零繞一圈,算出的「經過多久」仍然正確", "因為加法不能用"], 1, "無號整數的減法能抵銷歸零造成的影響。"),
  ("儲存 <code>millis()</code> 結果的變數應該用?", ["int", "unsigned long", "bool"], 1, "int 太小,約 32 秒就溢位。"),
  ("要同時做好幾件事,<code>loop()</code> 的原則是?", ["每個工作快速檢查「該不該做」,不要 delay", "每個工作都 delay 一下", "用 while 迴圈卡住等"], 0, "讓 loop() 飛快地跑,各個工作按自己的計時器行動。"),
])
practice = section("practice", "動手演練與延伸閱讀",
  sim("", "情境:你要「LED 一直閃,同時按鈕隨時有反應」。用 delay 寫的版本,按鈕常常漏掉", "你應該?",
      [("a1", "改用 millis() 計時,不要用 delay"), ("a2", "把 delay 縮短到 10 毫秒"), ("a3", "換更大的電阻")]),
  QUIZ_HTML,
  checks(["我知道 <code>delay()</code> 期間 Arduino 什麼都看不到。",
          "我能解釋 <code>millis()</code> 與「現在 − 上次 ≥ 間隔」的寫法。",
          "我知道要用 <code>unsigned long</code>,以及為什麼用減法。",
          "我的紅燈用 millis 自己閃,同時按鈕能控制黃燈,不漏。",
          "我能把 <code>loop()</code> 拆成幾個獨立的小工作。",
          "我用「去彈跳不卡住」的寫法處理按鈕。"], "做完之後,對照這張清單"),
  resources([
    ("https://docs.arduino.cc/language-reference/en/functions/time/millis/", "millis()", "Arduino language reference"),
    ("https://docs.arduino.cc/built-in-examples/digital/BlinkWithoutDelay/", "BlinkWithoutDelay 內建範例", "Blink without delay"),
  ], "Arduino 官方文件"))

SPEC = dict(
    dir="arduino",
    file="arduino-millis-guide.html",
    title="millis():不卡住的計時",
    eyebrow="第 15 篇 · millis()",
    h1="讓 Arduino 同時做好幾件事:不要睡覺,改看時鐘",
    sub="delay() 讓 Arduino 睡覺,會漏掉按鈕。學會 millis():不卡住的計時,讓閃燈、按鈕與別的工作各自按自己的節奏進行。",
    tldr="<code>delay()</code> 期間什麼都看不到。<strong><code>millis()</code> 回傳開機後的毫秒數</strong>。固定寫法:<code>if (現在 - 上次 &gt;= 間隔) { 上次 = 現在; … }</code>,變數用 <strong><code>unsigned long</code></strong>,<strong>loop() 裡不要 delay()</strong>。每件定時的事各用一個「上次」變數。",
    toc=[("what", "delay 的問題"), ("mill", "millis 的原理"), ("wire", "接線"), ("fill", "填入間隔"), ("code1", "寫法一:閃燈"), ("code2", "寫法二:兩件事"),
         ("try", "改改看"), ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
    body="\n\n".join([what, mill, wire, fillsec, code1, code2, try_, gotchas, practice]),
    config=dict(fill=FILL, sim=SIM, quiz=QUIZ, wiring=[bb.wiring_config(CIRC)], parts=bb.parts_info(CIRC)),
    prev=("arduino-lcd-guide.html", "LCD1602 I2C 顯示"),
    next=("arduino-interrupt-guide.html", "外部中斷 attachInterrupt"),
)
