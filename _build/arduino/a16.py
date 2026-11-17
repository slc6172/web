# -*- coding: utf-8 -*-
from h import *
import bb, a07

C7 = a07.CIRC

T1 = """// 第 16 篇:用外部中斷讀按鈕——即使 loop() 正在睡覺,按鈕也不會漏
const int BUTTON_PIN = 2;               // 只有 2 與 3 號腳能用外部中斷(Uno)
const int LED_PIN = 8;
volatile bool ledOn = false;            // 在中斷函式與主程式之間共用的變數,要加 volatile
volatile unsigned long lastEdge = 0;    // 上一次「電位變化」的時間(包含彈跳)

void onChange() {                       // 中斷服務函式(ISR):按鈕電位一變化,就「插隊」執行這裡
  unsigned long now = millis();
  if (now - lastEdge > {lock}) {        // 距離上一次變化夠久了,才相信這一次
    if (digitalRead(BUTTON_PIN) == LOW) {   // 讀到 LOW:這是「按下」
      ledOn = !ledOn;
      if (ledOn) {
        digitalWrite(LED_PIN, HIGH);
      } else {
        digitalWrite(LED_PIN, LOW);
      }
    }
  }
  lastEdge = now;                       // 每一次變化都要記下時間,包括彈跳那幾下
}

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), onChange, CHANGE);   // 腳位電位一變化(按下或放開),就執行 onChange
}

void loop() {
  Serial.println("working...");        // 假裝在做一件很花時間的事
  delay(2000);                         // 睡 2 秒:換成以前的寫法,這段時間按鈕會被漏掉
}
"""
T2 = """// 第 16 篇:數按鈕被按了幾次(安全地讀共用變數)
const int BUTTON_PIN = 2;
volatile unsigned int pressCount = 0;   // 中斷裡會改它
volatile unsigned long lastEdge = 0;

void onChange() {
  unsigned long now = millis();
  if (now - lastEdge > {lock}) {
    if (digitalRead(BUTTON_PIN) == LOW) {   // 按下才算
      pressCount++;                          // ++ 等於 pressCount = pressCount + 1
    }
  }
  lastEdge = now;                            // 每一次變化都記時間
}

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), onChange, CHANGE);
}

void loop() {
  noInterrupts();                        // 暫時關掉中斷
  unsigned int copy = pressCount;        // 趁沒人插隊,把值完整複製出來
  interrupts();                          // 再打開中斷
  Serial.print("count = ");
  Serial.println(copy);
  delay(1000);
}
"""
FILL = dict(lock="50")
bounce1 = [("D2", 1, 0), ("D2", 0, 500), ("D2", 1, 502), ("D2", 0, 504), ("D2", 1, 700), ("D2", 0, 702), ("D2", 1, 705),
           ("D2", 0, 1500), ("D2", 1, 1503), ("D2", 0, 1506), ("D2", 1, 1700)]
SKETCHES = [
    dict(name="int-toggle", code=T1, fill=FILL, circuit=C7, code_pins={"BUTTON_PIN": "UNO.D2", "LED_PIN": "UNO.D8"},
         sim=dict(kind="dual", pins=["D8", "D9"], seconds=2.0, inputs=bounce1, toggle=None, edges=[("D8", [(1, 500), (0, 1500)], 5)],
                  note="loop() 正在 delay(2000) 睡覺時,在 500 ms 與 1500 ms 按按鈕(都帶彈跳)")),
    dict(name="int-count", code=T2, fill=FILL, circuit=C7, code_pins={"BUTTON_PIN": "UNO.D2"},
         sim=dict(kind="uart", seconds=2.2, inputs=[("D2", 1, 0), ("D2", 0, 300), ("D2", 1, 303), ("D2", 0, 306), ("D2", 1, 400), ("D2", 0, 402), ("D2", 1, 405), ("D2", 0, 600), ("D2", 1, 700), ("D2", 0, 702), ("D2", 1, 706), ("D2", 0, 1500), ("D2", 1, 1600)],
                  expect=["count = 0\r\n", "count = 2\r\n", "count = 3\r\n"])),
]

what = section("what", "中斷:讓按鈕「插隊」",
  '<div class="panel"><h3>兩種「等人來」的方法</h3>'
  '<p><b>輪詢(polling)</b>:像你<b>每隔幾分鐘就去開門看看有沒有人來</b>。第 7、15 篇都是這樣:<code>loop()</code> 一直跑,不停讀按鈕。缺點:如果程式正忙(或在 <code>delay</code>),就會漏掉。</p>'
  '<p style="margin-bottom:0"><b>中斷(interrupt)</b>:像裝了<b>門鈴</b>。你專心做事,門鈴一響,你<b>馬上放下手邊的事去開門</b>,開完再回來接著做。Arduino 的晶片有這個硬體功能:事件發生的瞬間,自動暫停主程式,先去執行你指定的函式。</p></div>',
  tip("這一篇是<b>進階選讀</b>。第 15 篇的 <code>millis()</code> 已經能解決大部分「同時做好幾件事」的需求。中斷適合<b>不能漏掉的快速事件</b>(例如轉速感測器的脈衝、急停按鈕),新手專案多半用不到。"),
  '<h3 style="margin-top:26px">Uno 的外部中斷腳位</h3>',
  table("g3", ["腳位", "中斷編號", "用法"], [
    ["<b>2</b> 號腳", "INT0", "<code>attachInterrupt(digitalPinToInterrupt(2), 函式, 模式)</code>"],
    ["<b>3</b> 號腳", "INT1", "<code>attachInterrupt(digitalPinToInterrupt(3), 函式, 模式)</code>"],
  ]),
  '<p class="sk">Uno R3 只有 2 與 3 號腳支援外部中斷。這也是為什麼前幾篇的按鈕接 2 號腳。</p>',
  '<h3 style="margin-top:26px">四種觸發模式</h3>',
  table("g2", ["模式", "什麼時候觸發"], [
    ["<code>FALLING</code>", "腳位<b>從 HIGH 掉到 LOW</b> 的那一瞬間(<code>INPUT_PULLUP</code> 時就是<b>按下</b>)。<b>注意:</b>放開時的彈跳也可能含有這種變化,按鈕用它要小心"],
    ["<code>RISING</code>", "腳位從 LOW 升到 HIGH 的瞬間(放開)"],
    ["<code>CHANGE</code>", "只要電位有變化(按下與放開都觸發),進去後自己用 <code>digitalRead</code> 判斷。<b>本篇用它</b>"],
    ["<code>LOW</code>", "腳位<b>維持</b> LOW 的期間,一直觸發"],
  ]))

wire = section("wire", "接線:和第 7 篇完全一樣",
  '<p class="sub" style="margin-bottom:14px">按鈕接 2 號腳(用對角的兩腳,跨凹槽,下腳接 GND),LED 接 8 號腳。<b>不用重接,第 7 篇的電路直接拿來用</b>;還沒接的話,照第 7 篇的步驟接。</p>',
  canvas(bb.breadboard_svg(C7).replace(' data-part=', ' data-ref='), []),
  '<p class="sk">這張圖和第 7 篇相同(第 7 篇有逐步接線與接線表)。</p>')

fillsec = section("fill", "先填入去彈跳的鎖定時間",
  fill([("lock", "多少毫秒內的重複觸發當作彈跳", True)]),
  '<p class="sk">空白時用範例值 50 毫秒。</p>')

def exp(items):
    return table("g2", ["這一行", "它在做什麼"], items)

code1 = section("code1", "程式一:按一下,LED 切換(loop 在睡覺也不漏)",
  cmd(T1, cap="外部中斷:按鈕插隊", cpp=True),
  exp([
    ["<code>void onChange() { … }</code>", "<b>中斷服務函式(ISR)</b>:中斷發生時被自動呼叫的函式。<b>沒有回傳值、沒有參數</b>。你不會在程式裡自己呼叫它。"],
    ["<code>attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), onChange, CHANGE);</code>", "<b>註冊</b>:告訴 Arduino「2 號腳的電位只要有變化,就去執行 <code>onChange</code>」。<code>digitalPinToInterrupt()</code> 把腳位編號換成中斷編號。"],
    ["<code>volatile bool ledOn</code>", "<b>volatile</b> 提醒編譯器:這個變數<b>隨時可能被中斷改掉</b>,每次都要老實去讀,別偷懶用舊的值。<b>主程式與中斷共用的變數一定要加。</b>"],
    ["<code>now - lastEdge &gt; 50</code>", "按鈕彈跳會連續觸發好幾次中斷。<b>距離上一次電位變化不到 50 毫秒的,都當作彈跳忽略</b>(第 15 篇的時間差技巧,放進中斷裡)。"],
    ["<code>if (digitalRead(BUTTON_PIN) == LOW)</code>", "用 <code>CHANGE</code> 時,按下與放開都會進來,所以要<b>讀腳位現在的電位</b>:LOW 才是「按下」。"],
    ["<code>lastEdge = now;</code>", "<b>每一次</b>電位變化都記下時間,連彈跳的那幾下也要記。這樣放開時的彈跳,也會因為「離上一次變化太近」而被忽略。"],
  ]),
  see("Serial Monitor 每 2 秒印一行 <code>working...</code>,但<b>按下按鈕,LED 立刻切換</b>,不用等 <code>delay(2000)</code> 結束。"),
  warn("把第 7 篇的「輪詢」寫法放在這種「睡 2 秒」的 <code>loop()</code> 裡,多半會漏掉按鈕。中斷讓它在 2 秒睡眠中也能即時反應。", "對照"))

rules = section("rules", "中斷函式的守則:越短越好",
  '<p class="sub" style="margin-bottom:14px">中斷函式會<b>打斷主程式</b>,所以要遵守這些規則:</p>',
  table("g2", ["規則", "原因"], [
    ["<b>越短越快越好</b>,做完立刻回去", "在中斷期間,主程式與其他中斷都被擋住。"],
    ["<b>不要用 <code>delay()</code></b>", "中斷裡 <code>delay()</code> 不會正常運作。要等時間,改用旗標讓主程式處理。"],
    ["<b>不要用 <code>Serial.print</code></b>", "傳送資料可能花很久,或在中斷中卡住。要印,就在主程式裡印。"],
    ["<b><code>millis()</code> 在中斷裡不會增加</b>", "可以讀,但數字在這次中斷期間不會前進。"],
    ["<b>共用變數加 <code>volatile</code></b>", "否則編譯器可能把它的值存在暫存器,主程式看不到中斷改的新值。"],
    ["<b>函式不能有參數與回傳值</b>", "中斷由硬體呼叫,沒有人傳參數給它、也沒有人接回傳值。"],
  ]),
  tip("<b>最好的做法:中斷函式裡只做「記下發生過」</b>(例如把旗標設成 true、計數加 1),真正花時間的事交給主程式的 <code>loop()</code> 去做。程式一在中斷裡直接 <code>digitalWrite</code> 是因為這件事夠快、夠簡單。"))

code2 = section("code2", "程式二:數按鈕被按了幾次(安全地讀共用變數)",
  cmd(T2, cap="中斷計數,並安全地讀取", cpp=True),
  exp([
    ["<code>pressCount++;</code>", "計數加 1,寫在中斷裡很快。"],
    ["<code>noInterrupts();</code> … <code>interrupts();</code>", "<b>暫時關掉、再打開中斷</b>。夾在中間的幾行,保證不會被中斷插隊。"],
    ["<code>unsigned int copy = pressCount;</code>", "為什麼要這樣?<code>unsigned int</code> 在 Uno 上是 <b>2 個位元組</b>,CPU 要分兩次才能讀完。如果讀到一半中斷剛好改了它,就會讀到<b>前半是舊的、後半是新的</b>的怪數字。先關掉中斷、一次複製完整、再打開,就安全了。"],
  ]),
  see("每秒印一行 <code>count = N</code>。每按一下按鈕,N 就加 1(按得再快、再抖,也只算一次)。"),
  tip("這種「<b>複製出來再用</b>」的技巧,是中斷程式最重要的習慣:<b>只在關掉中斷的短短一瞬間碰共用變數</b>。"))

try_ = section("try", "改改看",
  table("g3", ["挑戰", "怎麼改", "你會看到"], [
    ["改成放開才切換", "把函式裡的 <code>== LOW</code> 改成 <code>== HIGH</code>", "放開的瞬間才切換 LED。"],
    ["試試 FALLING(看看為什麼不用它)", "把註冊那行的 <code>CHANGE</code> 改成 <code>FALLING</code>,並把「上一次變化」的記錄改成只在按下時更新", "按住一小段時間再放開,<b>有時放開時 LED 會多切換一次</b>:放開時的彈跳含有「掉到 LOW」的瞬間,被當成又按了一次。所以用 <code>CHANGE</code> 並記下每次變化比較可靠。"],
    ["比較:不用中斷", "把程式二的 <code>delay(1000)</code> 改成 <code>delay(3000)</code>,再試著改成「輪詢」寫法", "輪詢寫法會漏數,中斷寫法依然準確。"],
  ]))

gotchas = section("gotchas", "常見卡關",
  details("按鈕沒反應",
    ops(["按鈕有沒有接在 <b>2 或 3 號腳</b>(Uno R3 只有這兩個能用外部中斷)。", "<code>attachInterrupt</code> 有沒有寫在 <code>setup()</code>、腳位轉換用 <code>digitalPinToInterrupt()</code>。", "按鈕是否用對角兩腳、並接 GND(第 7 篇)。"]), True) +
  details("按一下,中斷觸發了好幾次",
    "<p>彈跳。確認有做去彈跳(程式裡用 <code>millis()</code> 的時間差鎖定),鎖定時間不要是 0。</p>") +
  details("計數的數字偶爾跳掉",
    "<p>讀共用變數時沒關閉中斷(多位元組變數),或忘了加 <code>volatile</code>。照程式二的寫法複製出來再用。</p>") +
  details("在中斷函式裡印 Serial 或用 delay,結果當掉或卡住",
    "<p>中斷函式裡不要用 <code>Serial.print</code> 與 <code>delay</code>。改成設一個 <code>volatile</code> 旗標,在 <code>loop()</code> 裡檢查並處理。</p>"))

SIM = {
  "a1": "<b>不用。</b>按鈕的 <code>loop()</code> 正在 <code>delay(2000)</code> 睡覺,輪詢寫法看不到。改用外部中斷,按下時 Arduino 會立刻打斷睡眠執行你的函式。",
  "a2": "<b>對。</b>外部中斷讓按鈕「插隊」。要注意:按鈕必須接 2 或 3 號腳,而且中斷函式要短、共用變數要加 <code>volatile</code>。",
  "a3": "<b>沒有用。</b>電阻不影響這個問題。",
}
SIM_Q = "你的 loop() 在 delay(2000) 時常常漏掉按鈕,又不想改成 millis() 的寫法。比較適合的做法是?"
QUIZ = quiz_cfg([
  ("Uno R3 上哪兩個腳位能用外部中斷?", ["2 與 3", "8 與 9", "A0 與 A1"], 0, "只有 2 與 3 號腳。"),
  ("主程式與中斷函式共用的變數要加什麼?", ["volatile", "const", "static"], 0, "volatile 告訴編譯器它隨時可能被改。"),
  ("中斷函式裡可以做什麼?", ["快速的小事,例如旗標或計數", "delay(1000)", "印很多 Serial 資料"], 0, "越短越快越好;不要 delay、不要 Serial.print。"),
  ("為什麼讀多位元組的共用變數要先 <code>noInterrupts()</code>?", ["避免讀到一半被中斷改掉,得到前後不一致的值", "讓程式跑更快", "省電"], 0, "CPU 要分兩次讀 2 個位元組。"),
  ("<code>FALLING</code> 模式搭配 <code>INPUT_PULLUP</code> 的按鈕,何時觸發?", ["按下的瞬間", "放開的瞬間", "一直觸發"], 0, "按下時腳位從 HIGH 掉到 LOW。"),
])
practice = section("practice", "動手演練與延伸閱讀",
  sim("", SIM_Q, "你應該?",
      [("a1", "繼續用輪詢,把 delay 縮短"), ("a2", "用外部中斷(按鈕接 2 或 3 號腳)讓它插隊"), ("a3", "換更大的電阻")]),
  QUIZ_HTML,
  checks(["我能用「門鈴」說明中斷和輪詢的差別。",
          "我知道 Uno R3 只有 2、3 號腳能做外部中斷。",
          "我會寫 <code>attachInterrupt(digitalPinToInterrupt(腳位), 函式, 模式)</code>。",
          "我知道中斷函式要短,不能 <code>delay</code>、不要 <code>Serial.print</code>。",
          "我知道共用變數要加 <code>volatile</code>,讀多位元組要先 <code>noInterrupts()</code>。",
          "我的按鈕在 loop() 睡覺時也能即時反應。"], "做完之後,對照這張清單"),
  resources([
    ("https://docs.arduino.cc/language-reference/en/functions/external-interrupts/attachInterrupt/", "attachInterrupt()", "Arduino language reference"),
    ("https://docs.arduino.cc/language-reference/en/variables/variable-scope-qualifiers/volatile/", "volatile", "Arduino language reference"),
  ], "Arduino 官方文件"))

SPEC = dict(
    dir="arduino",
    file="arduino-interrupt-guide.html",
    title="外部中斷 attachInterrupt(進階選讀)",
    eyebrow="第 16 篇 · 外部中斷",
    h1="讓按鈕「插隊」:外部中斷",
    sub="輪詢是不停去開門看,中斷是裝門鈴。學會 attachInterrupt,讓按鈕在 Arduino 忙碌或睡覺時也不漏。",
    tldr="<strong>只有 2、3 號腳</strong>能做外部中斷:<code>attachInterrupt(digitalPinToInterrupt(2), 函式, CHANGE)</code>。中斷函式<strong>要短、不要 delay 與 Serial.print</strong>;和主程式共用的變數要加 <strong>volatile</strong>,讀多位元組變數先 <code>noInterrupts()</code>。",
    toc=[("what", "中斷是什麼"), ("wire", "接線"), ("fill", "填入數值"), ("code1", "程式一:LED 切換"), ("rules", "中斷守則"), ("code2", "程式二:計數"),
         ("try", "改改看"), ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
    body="\n\n".join([what, wire, fillsec, code1, rules, code2, try_, gotchas, practice]),
    config=dict(fill=FILL, sim=SIM, quiz=QUIZ),
    prev=("arduino-millis-guide.html", "millis():不卡住的計時"),
    next=("arduino-bus-guide.html", "I2C 與 SPI 通訊"),
)
