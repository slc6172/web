# -*- coding: utf-8 -*-
from h import *
import bb

def L(n, t):
    return '<a href="arduino-%s-guide.html">%d</a>' % (t, n)
PG = {1: "start", 2: "electric", 3: "led", 4: "loop", 5: "schematic", 6: "pwm", 7: "button", 8: "serial", 9: "analog", 10: "ldr", 11: "ultrasonic", 12: "servo",
      13: "dht", 14: "lcd", 15: "millis", 16: "interrupt", 17: "bus", 18: "project", 19: "troubleshoot", 20: "reference"}
def pg(*ns):
    return "、".join(L(n, PG[n]) for n in ns)

def syntax_table(rows):
    return table("g3", ["寫法", "意思", "篇章"], [[a, b, pg(*c)] for a, b, c in rows])

G7, SL, CL, RU, G5 = bb.GRAY7, bb.SLATE, bb.CLAY, bb.RUST, bb.GRAY5

def symbol_sheet():
    o = []
    def cell(i):
        return 16 + (i % 4) * 160, 14 + (i // 4) * 118
    def cap(i, t):
        x, y = cell(i)
        o.append(bb._txt(x + 66, y + 96, t, "sb", SL))
    def ln(x1, y1, x2, y2, w=2):
        return '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (x1, y1, x2, y2, G7, w)
    # 0 電阻
    x, y = cell(0); o.append(bb._zigzag(x, y + 36, 130, 13, 6)); cap(0, "電阻")
    # 1 LED
    x, y = cell(1)
    o += [ln(x, y + 36, x + 36, y + 36), '<polygon points="%d,%d %d,%d %d,%d" fill="#F2C9C3" stroke="%s" stroke-width="2" stroke-linejoin="round"/>' % (x + 36, y + 18, x + 36, y + 54, x + 72, y + 36, G7),
          ln(x + 74, y + 18, x + 74, y + 54, 2.6), ln(x + 74, y + 36, x + 120, y + 36)]
    o.append('<path d="M%d,%d l9,-9 m-5,0 l5,0 l0,5 M%d,%d l9,-9 m-5,0 l5,0 l0,5" fill="none" stroke="%s" stroke-width="1.6" stroke-linecap="round"/>' % (x + 62, y + 14, x + 74, y + 14, RU)); cap(1, "LED")
    # 2 GND
    x, y = cell(2)
    o.append(ln(x + 66, y + 6, x + 66, y + 38))
    for k, wd in enumerate((40, 26, 12)):
        o.append(ln(x + 66 - wd // 2, y + 38 + k * 8, x + 66 + wd // 2, y + 38 + k * 8, 2.4))
    cap(2, "GND")
    # 3 5V
    x, y = cell(3)
    o += [ln(x + 46, y + 16, x + 86, y + 16, 2.4), ln(x + 66, y + 16, x + 66, y + 60), bb._txt(x + 66, y + 9, "5V", "mb", RU)]; cap(3, "電源 5V")
    # 4 按鈕
    x, y = cell(4)
    o += [ln(x + 6, y + 48, x + 34, y + 48), '<circle cx="%d" cy="%d" r="3.5" fill="%s"/><circle cx="%d" cy="%d" r="3.5" fill="%s"/>' % (x + 34, y + 48, G7, x + 98, y + 48, G7),
          ln(x + 98, y + 48, x + 126, y + 48), ln(x + 26, y + 26, x + 106, y + 26, 2.4), ln(x + 66, y + 26, x + 66, y + 14), ln(x + 66, y + 26, x + 66, y + 36)]; cap(4, "按鈕")
    # 5 電位器
    x, y = cell(5)
    o.append('<polyline points="%d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d %d,%d" fill="none" stroke="%s" stroke-width="2" stroke-linejoin="round"/>' % (
        x + 66, y + 2, x + 66, y + 8, x + 56, y + 16, x + 76, y + 28, x + 56, y + 40, x + 76, y + 52, x + 56, y + 62, x + 66, y + 68, x + 66, y + 74, G7))
    o.append(ln(x + 120, y + 38, x + 82, y + 38) + '<polygon points="%d,%d %d,%d %d,%d" fill="%s"/>' % (x + 80, y + 38, x + 90, y + 33, x + 90, y + 43, G7)); cap(5, "電位器")
    # 6 光敏電阻
    x, y = cell(6)
    o.append(bb._zigzag(x, y + 44, 130, 13, 6))
    o.append('<path d="M%d,%d l9,9 m-5,0 l5,0 l0,-5 M%d,%d l9,9 m-5,0 l5,0 l0,-5" fill="none" stroke="%s" stroke-width="1.6" stroke-linecap="round"/>' % (x + 40, y + 6, x + 56, y + 6, RU)); cap(6, "光敏電阻")
    # 7 蜂鳴器
    x, y = cell(7)
    o += [ln(x + 6, y + 40, x + 36, y + 40), ln(x + 96, y + 40, x + 126, y + 40), '<circle cx="%d" cy="%d" r="24" fill="#FFFFFF" stroke="%s" stroke-width="2"/>' % (x + 66, y + 40, G7), bb._txt(x + 52, y + 46, "+", "mb", RU),
          '<path d="M%d,%d q6,10 0,20 M%d,%d q6,10 0,20" fill="none" stroke="%s" stroke-width="1.6" stroke-linecap="round"/>' % (x + 76, y + 30, x + 84, y + 30, G7)]; cap(7, "蜂鳴器")
    # 8 模組方框
    x, y = cell(8)
    o += ['<rect x="%d" y="%d" width="86" height="64" rx="8" fill="#F0EEE6" stroke="%s" stroke-width="1.8"/>' % (x + 24, y + 10, G7), bb._txt(x + 67, y + 46, "模組", "mb", SL),
          ln(x + 6, y + 26, x + 24, y + 26), ln(x + 6, y + 58, x + 24, y + 58), ln(x + 110, y + 26, x + 128, y + 26), ln(x + 110, y + 58, x + 128, y + 58)]; cap(8, "模組 / 晶片方框")
    # 9 腳位標籤
    x, y = cell(9)
    o += ['<rect x="%d" y="%d" width="70" height="30" rx="8" fill="#F0EEE6" stroke="%s" stroke-width="1.5"/>' % (x + 10, y + 24, G7), bb._txt(x + 45, y + 44, "Uno D8", "mb", SL), ln(x + 80, y + 39, x + 122, y + 39)]; cap(9, "Uno 的腳位")
    # 10 交叉有點
    x, y = cell(10)
    o += [ln(x + 10, y + 40, x + 120, y + 40), ln(x + 66, y + 8, x + 66, y + 72), '<circle cx="%d" cy="%d" r="5" fill="%s"/>' % (x + 66, y + 40, G7)]; cap(10, "交叉有圓點:接在一起")
    # 11 交叉無點
    x, y = cell(11)
    o += [ln(x + 10, y + 40, x + 120, y + 40), ln(x + 66, y + 8, x + 66, y + 72)]; cap(11, "交叉沒圓點:沒有接")
    return ('<svg viewBox="0 0 660 360" role="img" aria-label="電路符號速查" style="min-width:540px"><defs>%s</defs><rect width="660" height="360" fill="#FFFFFF"/>%s</svg>' % (bb.STYLE, "".join(o)))

struct = section("struct", "程式結構、變數與運算",
  syntax_table([
    ["<code>void setup() { … }</code>", "開機後只跑一次", (3,)],
    ["<code>void loop() { … }</code>", "不斷重複", (3,)],
    ["<code>// 註解</code>", "給人看的說明,不會執行", (3,)],
    ["<code>int x = 5;</code>", "整數變數(約 ±32767)", (4,)],
    ["<code>long</code> / <code>unsigned long</code>", "較大的整數;<code>millis()</code> 用 <code>unsigned long</code>", (11, 15)],
    ["<code>float x = 3.14;</code>", "小數", (9,)],
    ["<code>bool b = true;</code>", "布林:<code>true</code> / <code>false</code>", (7,)],
    ["<code>char c = 'A';</code>", "單一字元(單引號)", (8,)],
    ["<code>const int PIN = 8;</code>", "常數,不會被改", (3, 4)],
    ["<code>volatile</code>", "會被中斷改的共用變數", (16,)],
    ["<code>int a[] = {8, 9, 10};</code> / <code>a[0]</code>", "陣列;編號從 0 開始", (4,)],
    ["<code>0b00010000</code>、<code>0x1F</code>", "二進位、十六進位數字", (17,)],
    ["<code>+ - * /</code>、<code>x++</code>、<code>x += 5</code>", "運算;加 1;加上再存回", (4, 6)],
    ["<code>== != &lt; &gt; &lt;= &gt;=</code>", "比較(<code>==</code> 是比較,<code>=</code> 是指定)", (7,)],
    ["<code>&amp;&amp;</code> <code>||</code> <code>!</code>", "而且、或者、不是", (10, 7)],
  ]))

flow = section("flow", "控制結構與函式",
  syntax_table([
    ["<code>if (…) { … } else { … }</code>", "條件判斷", (7,)],
    ["<code>else if (…)</code>", "再一個條件", (8, 10)],
    ["<code>for (int i = 0; i &lt; n; i++) { … }</code>", "重複 n 次", (4,)],
    ["<code>while (條件) { … }</code>", "條件成立就一直重複", (7,)],
    ["<code>返回型態 名稱(參數) { … return 值; }</code>", "自己定義的函式", (6, 11)],
    ["<code>return;</code>", "提早結束這一輪(或函式)", (13,)],
    ["<code>map(x, a, b, c, d)</code>", "把範圍 a–b 換成 c–d(整數)", (9,)],
    ["<code>constrain(x, 下限, 上限)</code>", "限制範圍", (11,)],
    ["<code>isnan(x)</code>", "是不是「不是數字」", (13,)],
  ]))

io = section("io", "輸入輸出、時間與通訊",
  syntax_table([
    ["<code>pinMode(腳位, OUTPUT / INPUT / INPUT_PULLUP)</code>", "設定腳位模式", (3, 7)],
    ["<code>digitalWrite(腳位, HIGH / LOW)</code>", "輸出 5 V / 0 V", (3,)],
    ["<code>digitalRead(腳位)</code>", "讀 HIGH(1)或 LOW(0)", (7,)],
    ["<code>analogWrite(腳位, 0–255)</code>", "PWM,只有 ~ 腳位(3、5、6、9、10、11)", (6,)],
    ["<code>analogRead(A0)</code>", "讀 0–5 V,回傳 0–1023", (9,)],
    ["<code>delay(毫秒)</code> / <code>delayMicroseconds(微秒)</code>", "暫停(整個程式睡覺)", (3, 11)],
    ["<code>millis()</code>", "開機後的毫秒數(不睡覺的計時)", (15,)],
    ["<code>pulseIn(腳位, HIGH, 逾時微秒)</code>", "量脈衝長度", (11,)],
    ["<code>tone(腳位, 頻率)</code> / <code>noTone(腳位)</code>", "被動蜂鳴器發聲", (6,)],
    ["<code>Serial.begin(9600)</code>", "啟動序列通訊", (8,)],
    ["<code>Serial.print() / println()</code>", "印出(println 換行)", (8,)],
    ["<code>Serial.available()</code> / <code>Serial.read()</code>", "接收電腦送來的字元", (8,)],
    ["<code>attachInterrupt(digitalPinToInterrupt(腳位), 函式, 模式)</code>", "外部中斷(2、3 號腳)", (16,)],
    ["<code>noInterrupts()</code> / <code>interrupts()</code>", "暫時關閉 / 打開中斷", (16,)],
    ["<code>Wire.begin()</code>、<code>beginTransmission()</code>、<code>endTransmission()</code>", "I2C", (17,)],
    ["<code>SPI.begin()</code>、<code>SPI.transfer(位元組)</code>", "SPI", (17,)],
    ["<code>#include &lt;Servo.h&gt;</code>、<code>Servo s;</code>、<code>s.attach(9)</code>、<code>s.write(角度)</code>", "伺服馬達", (12,)],
    ["<code>DHT dht(腳位, DHT11);</code>、<code>dht.begin()</code>、<code>dht.readTemperature()</code>", "DHT11(Adafruit 函式庫)", (13,)],
    ["<code>lcd.begin(16, 2)</code>、<code>lcd.setCursor(欄, 列)</code>、<code>lcd.print()</code>", "LCD1602(hd44780)", (14,)],
  ]))

pins = section("pins", "Uno 腳位速查",
  table("g3", ["功能", "腳位", "備註 / 篇章"], [
    ["數位輸入輸出", "0–13", "<b>0、1 號腳</b>與 USB 序列通訊共用,有用 Serial 時不要接零件"],
    ["PWM(analogWrite)", "<b>3、5、6、9、10、11</b>(板上標 <code>~</code>)", "第 6 篇;Servo 函式庫會停用 9、10 的 PWM(第 12 篇)"],
    ["類比輸入", "A0–A5", "第 9 篇;也可以當數位腳位用"],
    ["外部中斷", "<b>2、3</b>", "第 16 篇"],
    ["I2C", "<b>A4 = SDA、A5 = SCL</b>(靠近 AREF 處另有同訊號的 SDA、SCL)", "第 14、17 篇"],
    ["SPI", "<b>11 = MOSI、12 = MISO、13 = SCK、10 = SS</b>", "第 17 篇"],
    ["內建 LED", "13(<code>LED_BUILTIN</code>)", "第 1 篇"],
    ["電源", "5V、3.3V、GND、VIN", "每個數位腳位建議 ≤ 20 mA、絕對上限 40 mA(第 2 篇)"],
  ]))

parts = section("parts", "零件接法速查",
  table("g3", ["零件", "怎麼接", "篇章"], [
    ["LED", "長腳(+)靠電阻、訊號腳;短腳(−)接 GND;<b>一定串 220Ω 電阻</b>", pg(3)],
    ["按鈕", "對角兩腳,跨凹槽;一腳接訊號腳,一腳接 GND;程式 <code>INPUT_PULLUP</code>,按下為 LOW", pg(7)],
    ["蜂鳴器(主動)", "+ 腳經 220Ω 接訊號腳,− 腳接 GND;<code>digitalWrite</code> 通電就響", pg(6)],
    ["電位器", "兩端接 5V 與 GND,中間腳接 A0", pg(9)],
    ["光敏電阻", "與 10kΩ 串聯成分壓,A0 接在兩者之間", pg(10)],
    ["HC-SR04", "VCC→5V、GND→GND、Trig→輸出腳、Echo→輸入腳", pg(11)],
    ["SG90 伺服", "棕 GND、紅 5V、橘訊號;吃電多", pg(12)],
    ["DHT11(3 腳)", "S→訊號腳、+→5V、−→GND(對照印刷)", pg(13)],
    ["LCD1602 I2C", "VCC→5V、GND→GND、SDA→A4/SDA、SCL→A5/SCL;先調對比", pg(14)],
    ["74HC595", "缺口朝左;16→5V、8→GND、10→5V、13→GND;SER→11、SRCLK→13、RCLK→12", pg(17)],
  ]))

symbols = section("symbols", "電路符號速查",
  canvas(symbol_sheet(), []),
  tip("看陌生的圖,先找<b>電源(5V)與 GND</b>,再沿著線,一個零件一個零件對照;<b>交叉處有圓點才是接在一起</b>。第 5 篇有完整練習。"))

units = section("units", "常用單位與數字",
  table("g3", ["項目", "換算", "備註"], [
    ["電壓 / 電流 / 電阻", "V、A(1 A = 1000 mA)、Ω(1 kΩ = 1000 Ω)", "V = I × R(第 2 篇)"],
    ["時間", "1 秒 = 1000 毫秒 = 1,000,000 微秒", "<code>delay</code> 毫秒、<code>delayMicroseconds</code> 微秒"],
    ["analogRead", "0–1023 對應 0–5 V,約 4.9 mV 一級", "第 9 篇"],
    ["analogWrite", "0–255 對應 0–100% 工作週期", "第 6 篇"],
    ["超音波", "距離(cm)= 時間(µs)× 0.0343 ÷ 2", "第 11 篇"],
    ["LED 電阻", "R = (5 − Vf) ÷ I,取不小於的標準值", "紅色 Vf 約 2 V,220Ω 約 13.6 mA"],
  ]))

QUIZ = quiz_cfg([
  ("哪些腳位能做 PWM(analogWrite)?", ["3、5、6、9、10、11", "0–13 全部", "只有 13"], 0, "有 ~ 標記的腳位。"),
  ("Uno 外部中斷腳位是?", ["2 與 3", "10 與 11", "A4 與 A5"], 0, "只有 2、3 號腳。"),
  ("I2C 的 SDA、SCL 在 Uno 上是?", ["A4、A5", "2、3", "11、13"], 0, "A4 = SDA、A5 = SCL。"),
  ("按下 <code>INPUT_PULLUP</code> 的按鈕,<code>digitalRead</code> 讀到?", ["LOW", "HIGH", "0.5"], 0, "按下接到 GND,讀 LOW。"),
  ("要在 <code>loop()</code> 同時做好幾件事,用?", ["millis() 的時間差", "delay()", "while(1)"], 0, "delay 會讓程式睡覺。"),
])
practice = section("practice", "測驗與延伸閱讀",
  QUIZ_HTML,
  resources([
    ("https://docs.arduino.cc/language-reference/", "Arduino 語言參考", "Language reference"),
    ("https://docs.arduino.cc/hardware/uno-rev3/", "Arduino Uno Rev3 說明", "Arduino UNO Rev3"),
  ], "Arduino 官方文件"))

SPEC = dict(
    dir="arduino",
    file="arduino-reference-guide.html",
    title="語法與電路符號速查",
    eyebrow="附錄 · 速查",
    h1="一頁查完:語法、腳位、零件接法與電路符號",
    sub="本主題用過的 Arduino 語法、Uno 腳位、各零件的接法與電路符號,都集中在這一頁。每一列都標了出處,點篇號可以跳回去看完整說明。",
    tldr="這是查詢用的附錄,不必照順序讀。想快速回想<strong>某個語法怎麼寫</strong>、<strong>哪個腳位能做什麼</strong>、<strong>零件怎麼接</strong>、<strong>符號長什麼樣</strong>,都在這裡;篇號是連結,點了就跳到完整說明。",
    toc=[("struct", "結構與變數"), ("flow", "控制與函式"), ("io", "輸入輸出與通訊"), ("pins", "腳位速查"), ("parts", "零件接法"), ("symbols", "電路符號"), ("units", "單位換算"), ("practice", "測驗與延伸閱讀")],
    body="\n\n".join([struct, flow, io, pins, parts, symbols, units, practice]),
    config=dict(fill={}, quiz=QUIZ),
    prev=("arduino-troubleshoot-guide.html", "故障排除總整理"),
)
