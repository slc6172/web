# -*- coding: utf-8 -*-
from h import *
import bb, a07

HELLO = """// 第 8 篇:第一個 Serial 程式(不需要接任何線)
int count = 0;                 // 計數器

void setup() {
  Serial.begin(9600);          // 開始序列通訊,速度 9600(要和 Serial Monitor 一致)
  Serial.println("Hello, Arduino!");   // 印一行文字,結尾自動換行
}

void loop() {
  Serial.print("count = ");    // 印文字,不換行
  Serial.println(count);       // 印變數的值,並換行
  count = count + 1;           // 加 1
  delay({gap});                // 等一下,不然會刷太快
}
"""
FMT = """// 第 8 篇:數字怎麼印
void setup() {
  Serial.begin(9600);
  int n = 42;
  float x = 3.14159;
  Serial.print("n = ");          Serial.println(n);        // n = 42
  Serial.print("n in BIN = ");   Serial.println(n, BIN);   // 二進位:101010
  Serial.print("n in HEX = ");   Serial.println(n, HEX);   // 十六進位:2A
  Serial.print("x = ");          Serial.println(x);        // 小數,預設印 2 位:3.14
  Serial.print("x (4 digits) = "); Serial.println(x, 4);   // 指定 4 位小數:3.1416
}

void loop() {
}
"""
DBG = """// 第 8 篇:用 Serial 親眼看按鈕的值(接線沿用第 7 篇)
const int BUTTON_PIN = 2;

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  int state = digitalRead(BUTTON_PIN);
  Serial.print("button = ");
  Serial.println(state);       // 沒按印 1,按下印 0
  delay({gap});
}
"""
KEY = """// 第 8 篇:用電腦鍵盤控制 LED(接線沿用第 7 篇)
const int LED_PIN = 8;

void setup() {
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  Serial.println("Type 1 = LED on, 0 = LED off");
}

void loop() {
  if (Serial.available() > 0) {        // 電腦有送資料進來嗎?
    char c = Serial.read();            // 讀進一個字元
    if (c == '1') {
      digitalWrite(LED_PIN, HIGH);
      Serial.println("LED on");
    } else if (c == '0') {
      digitalWrite(LED_PIN, LOW);
      Serial.println("LED off");
    }
  }
}
"""
PLOT = """// 選修:給 Serial Plotter 畫圖(每行印一個數字)
void setup() {
  Serial.begin(9600);
}

void loop() {
  for (int i = 0; i < 100; i++) {
    Serial.println(i);
    delay(20);
  }
}
"""
FILL = dict(gap="500")
C7 = a07.CIRC
SKETCHES = [
    dict(name="ser-hello", code=HELLO, fill=FILL,
         sim=dict(kind="uart", seconds=2.2, expect=["Hello, Arduino!\r\n", "count = 0\r\n", "count = 1\r\n", "count = 2\r\n", "count = 3\r\n"])),
    dict(name="ser-fmt", code=FMT, fill=FILL,
         sim=dict(kind="uart", seconds=0.5, expect=["n = 42\r\n", "n in BIN = 101010\r\n", "n in HEX = 2A\r\n", "x = 3.14\r\n", "x (4 digits) = 3.1416\r\n"])),
    dict(name="ser-debug", code=DBG, fill=FILL, circuit=C7, code_pins={"BUTTON_PIN": "UNO.D2"},
         sim=dict(kind="uart", seconds=1.8, inputs=[("D2", 1, 0), ("D2", 0, 300), ("D2", 1, 1300)],
                  expect=["button = 1\r\n", "button = 0\r\n", "button = 0\r\n", "button = 1\r\n"])),
    dict(name="ser-key", code=KEY, fill=FILL, circuit=C7, code_pins={"LED_PIN": "UNO.D8"},
         sim=dict(kind="uart", seconds=1.6, pin="D8", rx=[(300, 49), (900, 48)],
                  expect=["Type 1 = LED on, 0 = LED off\r\n", "LED on\r\n", "LED off\r\n"], edges=[(1, 300), (0, 900)], tol_ms=5)),
    dict(name="ser-plot", code=PLOT, fill=FILL, sim=dict(kind="uart", seconds=0.3, expect=["0\r\n", "1\r\n", "2\r\n", "3\r\n"])),
]
CIRCUITS = []

baud = ('<div class="panel" data-baudsim data-prog="9600"><div class="wgrid f2"><div><label>程式裡寫的</label><input value="Serial.begin(9600);" readonly></div>'
        '<div><label>Serial Monitor 選的 baud</label><select data-bd="monitor"><option value="9600">9600 baud</option><option value="115200">115200 baud</option><option value="300">300 baud</option></select></div></div>'
        '<div class="bd-screen" role="status"></div><div class="rc-out bd-note" style="margin-top:10px"></div></div>')

what = section("what", "Serial:Arduino 與電腦之間的對話視窗",
  '<div class="panel"><h3>為什麼要學它</h3>'
  '<p>前面的程式做了什麼,你只能從 LED 有沒有亮去<b>猜</b>。<b>Serial</b>(序列通訊)讓 Arduino 能把文字與數字<b>透過 USB 線傳到電腦</b>,顯示在 Arduino IDE 的 Serial Monitor 上。</p>'
  '<p style="margin-bottom:0">它是你<b>除錯最重要的工具</b>:想知道變數是多少、按鈕有沒有讀到、程式跑到哪一步,印出來看就知道。</p></div>',
  warn("<b>0 號腳與 1 號腳(標示 RX、TX)被 Serial 使用。</b>用 Serial 時,不要把任何零件接在這兩個腳位上,否則上傳程式或印資料時會出問題。", "別用 0、1 號腳"))

hello = section("hello", "第一個 Serial 程式:不需要接線",
  '<p class="sub" style="margin-bottom:14px">只要 Uno 接著電腦,不用接任何零件。每秒印一行計數。</p>',
  fill([("gap", "每一行之間的間隔(毫秒)", True)]),
  cmd(HELLO, cap="Hello Serial:印出計數", cpp=True),
  table("g2", ["這一行", "它在做什麼"], [
    ["<code>Serial.begin(9600);</code>", "<b>開始序列通訊</b>,速度是 9600(每秒傳 9600 個位元,叫 <b>baud</b>)。必須寫在 <code>setup()</code> 裡。"],
    ["<code>Serial.println(\"…\");</code>", "印一段文字,<b>結尾自動換行</b>(ln 是 line)。文字要用<b>雙引號</b>括起來。"],
    ["<code>Serial.print(\"count = \");</code>", "印出但<b>不換行</b>,下一次印會接在後面。"],
    ["<code>Serial.println(count);</code>", "印出<b>變數的值</b>(不用雙引號)。引號裡的是文字,沒有引號的是變數名字。"],
  ]),
  '<h3 style="margin-top:24px">開啟 Serial Monitor</h3>',
  steps(
    step(1, "先上傳程式", "和之前一樣:選好板子與連接埠,按 Upload,等到出現上傳完成。"),
    step(2, "打開 Serial Monitor", "它整合在 IDE 裡,不會另外開視窗。",
         ops(["按 IDE <b>右上角的放大鏡圖示(Serial Monitor)</b>,或選單 <b>Tools → Serial Monitor</b>。", "下方的面板會切換成 Serial Monitor。右上角有個下拉選單可以選 <b>baud rate</b>。"])),
    step(3, "把 baud 選成 9600", "Serial Monitor 的速度必須和程式裡 <code>Serial.begin()</code> 的數字一致。",
         ops(["點 baud rate 下拉選單,選 <b>9600 baud</b>。"]),
         see("面板裡出現 <code>Hello, Arduino!</code>,接著每秒一行 <code>count = 0</code>、<code>count = 1</code> …"),
         tip("有時打開 Serial Monitor 會讓 Uno 重新啟動,所以你可能會從頭看到 <code>Hello, Arduino!</code>。這是正常的。")),
  ),
  '<h3 style="margin-top:26px">速度不一致,就會看到亂碼</h3>',
  baud)

fmt = section("fmt", "怎麼印:文字、數字、進位與小數",
  cmd(FMT, cap="各種印法(只在開機時印一次)", cpp=True),
  table("g3", ["你會看到", "寫法", "說明"], [
    ["n = 42", "<code>Serial.println(n);</code>", "整數,直接印"],
    ["101010", "<code>Serial.println(n, BIN);</code>", "第二個參數:<code>BIN</code> 二進位、<code>HEX</code> 十六進位、<code>DEC</code> 十進位"],
    ["3.14", "<code>Serial.println(x);</code>", "小數(float),預設印 <b>2 位</b>小數"],
    ["3.1416", "<code>Serial.println(x, 4);</code>", "第二個參數是要印幾位小數"],
  ]),
  tip("<code>print</code> 不換行、<code>println</code> 換行。想在同一行印好幾樣東西,前面都用 <code>print</code>,最後一個用 <code>println</code>。中文字串也可以印,Serial Monitor 會顯示;但記得用雙引號。"))

debug = section("debug", "用 Serial 除錯:親眼看到按鈕的值",
  '<p class="sub" style="margin-bottom:14px">接線沿用<b>第 7 篇</b>(按鈕接 2 號腳,對角兩腳,另一腳接 GND)。第 7 篇我說「按下去讀到 LOW」,現在你可以自己看。</p>',
  canvas(bb.breadboard_svg(C7).replace(' data-part=', ' data-ref='), []),
  '<p class="sk">這張圖與第 7 篇相同。LED 這一組在這一篇只有最後一個程式會用到。</p>',
  cmd(DBG, cap="印出按鈕的值", cpp=True),
  see("Serial Monitor 每 0.5 秒印一行 <code>button = 1</code>;<b>按住按鈕時</b>變成 <code>button = 0</code>,放開又變回 1。這證實了:<code>INPUT_PULLUP</code> 時,按下 = LOW(0)。"),
  '<h3 style="margin-top:24px">除錯的基本流程</h3>',
  ops(["<b>懷疑</b>:「我覺得按鈕沒被讀到。」", "<b>印出來看</b>:在可疑的地方加 <code>Serial.println(…)</code>,印出變數或狀態。", "<b>比對</b>:印出的值和你預期的一樣嗎?一樣就往下一個地方查;不一樣,問題就在這附近。", "<b>修好後把除錯用的 <code>Serial</code> 拿掉</b>(或留著,但要知道它會讓程式變慢一點點)。"]))

keyin = section("keyin", "反過來:用電腦鍵盤控制 Arduino",
  '<p class="sub" style="margin-bottom:14px">Serial 是雙向的。Arduino 也能<b>收到</b>你在 Serial Monitor 輸入的字。下面用鍵盤控制 8 號腳的 LED(接線同第 7 篇)。</p>',
  cmd(KEY, cap="輸入 1 開燈、輸入 0 關燈", cpp=True),
  table("g2", ["這一行", "它在做什麼"], [
    ["<code>Serial.available() &gt; 0</code>", "電腦有送資料進來、還沒被讀走嗎?有幾個位元組可讀,就回傳幾。"],
    ["<code>char c = Serial.read();</code>", "讀進一個字元,存進 <code>char</code> 變數(放單一字元,用<b>單引號</b>)。"],
    ["<code>c == '1'</code>", "比較是不是字元「1」。注意是單引號 <code>'1'</code>,不是數字 1。"],
    ["<code>else if (c == '0')</code>", "「否則,如果……」:第一個條件不成立時,再檢查另一個條件。"],
  ]),
  steps(step(1, "上傳後打開 Serial Monitor", "baud 選 9600。"),
        step(2, "在上方輸入欄打 1,按 Enter(或旁邊的送出)", "字元會被送到 Arduino。",
             see("8 號腳的 LED 亮起,Serial Monitor 印出 <code>LED on</code>。再輸入 <code>0</code>,LED 熄滅,印出 <code>LED off</code>。"))),
  tip("輸入欄旁邊有個決定「送出時要不要多加換行字元」的下拉選單。本程式只看 <code>'1'</code> 與 <code>'0'</code>,多出來的換行會被忽略,所以選哪個都可以。"))

plot = section("plot", "選修:Serial Plotter 把數字畫成線",
  '<p class="sub" style="margin-bottom:14px">如果每一行只印一個數字,IDE 還能幫你畫成曲線,很適合看感測器的變化(第 9 篇會用到)。</p>',
  cmd(PLOT, cap="印 0 到 99,Serial Plotter 會畫出斜線", cpp=True),
  ops(["上傳後,按右上角 <b>Serial Plotter</b> 圖示(Serial Monitor 旁邊),或選單 <b>Tools → Serial Plotter</b>。", "baud 一樣選 9600。你會看到一條從 0 爬升到 99 的斜線,重複出現。"]))

gotchas = section("gotchas", "常見卡關",
  details("Serial Monitor 一片亂碼",
    "<p>baud 不一致。程式是 <code>Serial.begin(9600)</code>,就把 Serial Monitor 選成 9600。把上面的互動示意玩一遍,你會記得這個畫面。</p>", True) +
  details("什麼都沒有印出來",
    ops(["程式有沒有 <code>Serial.begin(9600);</code>(寫在 <code>setup()</code>)。", "有沒有打開 Serial Monitor,而且選的是<b>正確的連接埠</b>。", "上傳有沒有成功;板子上的 TX 燈在印資料時會閃。", "是不是把零件接在 0 或 1 號腳了。"])) +
  details("文字刷得太快,看不清楚",
    "<p>在 <code>loop()</code> 最後加 <code>delay(500)</code> 之類的等待。也可以按面板右側的<b>暫停自動捲動</b>圖示(Toggle Autoscroll)。</p>") +
  details("上傳時說連接埠被佔用",
    "<p>別的程式正在用這個 COM 埠(例如另一個 IDE 視窗的 Serial Monitor)。關掉它,再重新上傳。</p>") +
  details("輸入 1 沒反應",
    "<p>確認程式比對的是<b>單引號的字元</b> <code>'1'</code>,而不是數字 <code>1</code>;確認 Serial Monitor 的 baud 是 9600;確認 LED 腳位與接線一致。</p>"))

try_ = section("try", "改改看",
  table("g3", ["挑戰", "怎麼改", "你會看到"], [
    ["印更多資訊", "在除錯程式裡,用 <code>if</code> 判斷,只有狀態改變時才印", "不再一直刷屏,只有按下、放開的瞬間才有一行。"],
    ["計算按鈕次數", "第 7 篇的切換程式,加一個 <code>count</code> 變數,每按一次加 1 並印出", "Serial Monitor 顯示你按了幾次。這就是用印出來驗證「彈跳處理有沒有成功」。"],
    ["更多指令", "鍵盤程式再加 <code>'t'</code>:切換亮滅", "你自己決定指令的意思。"],
  ]))

SIM = {
  "a1": "<b>不用。</b>亂碼不是程式錯,是兩邊「講話速度」不一樣。調整 Serial Monitor 的 baud 就好。",
  "a2": "<b>對。</b>把 Serial Monitor 右上角的 baud 選成與 <code>Serial.begin()</code> 相同的數字(例如 9600),亂碼就消失。",
  "a3": "<b>沒有用。</b>換 USB 線不能讓兩邊的速度設定一致。",
}
QUIZ = quiz_cfg([
  ("<code>Serial.print</code> 與 <code>Serial.println</code> 的差別?", ["println 結尾會換行", "print 比較快", "沒有差別"], 0,
   "ln 是 line,印完會換行。"),
  ("程式用 <code>Serial.begin(9600)</code>,Serial Monitor 選 115200,會怎樣?", ["正常顯示", "亂碼", "Arduino 當機"], 1,
   "兩邊速度不一致,就會是亂碼。"),
  ("<code>Serial.println(count);</code> 與 <code>Serial.println(\"count\");</code> 的差別?", ["沒有差別", "前者印變數的值,後者印文字 count", "前者是錯的"], 1,
   "有雙引號是文字,沒有是變數。"),
  ("為什麼用 Serial 時不要把零件接在 0、1 號腳?", ["它們是 Serial 的 RX、TX 腳位", "它們沒有電", "會比較燙"], 0,
   "0、1 號腳被 USB 序列通訊使用。"),
  ("用 Serial 除錯的好處是?", ["讓程式跑得更快", "能看到變數與狀態的實際值", "不需要寫程式"], 1,
   "把內部狀態印出來,才知道程式到底在做什麼。"),
])
practice = section("practice", "動手演練與延伸閱讀",
  sim("", "情境:Serial Monitor 顯示一堆亂碼", "最可能的原因與做法?",
      [("a1", "重新安裝 IDE"), ("a2", "把 Serial Monitor 的 baud 選成和程式一致"), ("a3", "換一條 USB 線")]),
  QUIZ_HTML,
  checks(["我知道 Serial 是 Arduino 與電腦的對話視窗,也是除錯的好工具。",
          "我能用 <code>Serial.begin</code>、<code>print</code>、<code>println</code> 印出文字與變數。",
          "我知道 Serial Monitor 的 baud 要與程式一致。",
          "我親眼用 Serial 看到按鈕按下是 0、放開是 1。",
          "我能用鍵盤輸入 1 與 0 控制 LED。",
          "我知道不要把零件接在 0、1 號腳。"], "做完之後,對照這張清單"),
  resources([
    ("https://docs.arduino.cc/software/ide-v2/tutorials/ide-v2-serial-monitor", "在 IDE 2 使用 Serial Monitor", "Using the Serial Monitor tool"),
    ("https://docs.arduino.cc/language-reference/en/functions/communication/serial/", "Serial 函式總覽", "Arduino language reference"),
    ("https://docs.arduino.cc/language-reference/en/functions/communication/serial/println/", "Serial.println()", "Arduino language reference"),
  ], "Arduino 官方文件"))

SPEC = dict(
    dir="arduino",
    file="arduino-serial-guide.html",
    title="Serial Monitor 與除錯",
    eyebrow="第 8 篇 · Serial Monitor",
    h1="Serial:讓 Arduino 開口說話,也能聽你說話",
    sub="學會把數字和文字從 Arduino 傳到電腦,看清楚程式到底在做什麼;也學會從電腦鍵盤控制 Arduino。這是除錯最重要的工具。",
    tldr="<code>Serial.begin(9600)</code> 開始,<code>Serial.print</code> / <code>println</code> 印出,IDE 右上角放大鏡開 <strong>Serial Monitor</strong>,<strong>baud 要和程式一致</strong>,否則亂碼。用 <code>Serial.available()</code> 與 <code>Serial.read()</code> 接收鍵盤輸入。<strong>不要用 0、1 號腳。</strong>",
    toc=[("what", "什麼是 Serial"), ("hello", "第一個程式"), ("fmt", "怎麼印"), ("debug", "用 Serial 除錯"), ("keyin", "鍵盤控制"),
         ("plot", "Serial Plotter"), ("gotchas", "常見卡關"), ("try", "改改看"), ("practice", "演練與延伸閱讀")],
    body="\n\n".join([what, hello, fmt, debug, keyin, plot, gotchas, try_, practice]),
    config=dict(fill=FILL, sim=SIM, quiz=QUIZ),
    prev=("arduino-button-guide.html", "按鈕:讀取輸入"),
    next=("arduino-analog-guide.html", "類比輸入:電位器"),
)
