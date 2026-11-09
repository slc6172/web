# -*- coding: utf-8 -*-
from h import *
import bb

CIRC = bb.Circuit(
    "pwm-buzzer", 22,
    parts=[
        bb.Resistor("R2", 220, "b5", "b9", 1), bb.Resistor("R1", 220, "b15", "b19", 1),
        bb.Buzzer("BZ1", "active", "d9", "d12", 2), bb.LED("LED1", "red", "d19", "d20", 2),
        bb.Wire("K2", "a12", "t-12", "black", 3, route="straight"), bb.Wire("K1", "a20", "t-20", "black", 3, route="straight"),
        bb.Wire("S2", "UNO.D8", "a5", "orange", 4), bb.Wire("S1", "UNO.D9", "a15", "blue", 4),
        bb.Wire("G", "UNO.GND", "t-22", "black", 5),
    ],
    steps=[
        ("放兩顆電阻", "兩顆 220Ω 電阻都橫放在 <b>b 列</b>:左邊 <code>b5–b9</code>(給蜂鳴器),右邊 <code>b15–b19</code>(給 LED)。"),
        ("放蜂鳴器與 LED", "<b>蜂鳴器</b>:<b>+ 腳</b>(外殼有 + 標記、通常較長)插 <code>d9</code>,<b>− 腳</b>插 <code>d12</code>(兩腳相隔 3 欄)。<br><b>紅色 LED</b>:長腳(+)插 <code>d19</code>,短腳(−)插 <code>d20</code>。"),
        ("兩條黑色短線:負極 → − 軌", "<code>a12</code> → <code>t-12</code>(蜂鳴器 − 腳),<code>a20</code> → <code>t-20</code>(LED 短腳)。兩個負極都接到 − 軌。"),
        ("兩條訊號線", "橘線:Uno <b>8 號腳</b> → <code>a5</code>(蜂鳴器那一組)。<br>藍線:Uno <b>9 號腳</b> → <code>a15</code>(LED 那一組)。<br><b>9 號腳旁邊有一個 <code>~</code></b>,表示它能輸出 PWM。"),
        ("黑線:Uno GND → − 軌", "黑色杜邦線一端插 Uno 數位腳位排的 <strong>GND</strong>,另一端插 <code>t-22</code>。"),
    ],
    chains=[["UNO.D9", "R1", "LED1", "UNO.GND"], ["UNO.D8", "R2", "BZ1", "UNO.GND"]],
    intro="先<strong>拔掉 USB 線</strong>。這次有兩組電路:<b>8 號腳 → 電阻 → 蜂鳴器</b>,以及 <b>9 號腳 → 電阻 → LED</b>。LED 一定要接在有 <code>~</code> 的腳位(9 號),才能做出漸亮漸暗。",
    done="兩條獨立的路,負極共用同一條 − 軌回 GND。蜂鳴器串了一顆 220Ω 電阻,把電流壓低、聲音也比較不刺耳。檢查:蜂鳴器 + 腳朝向電阻那一側。",
)
CIRCUITS = [CIRC]

FADE = """// 第 6 篇:呼吸燈(PWM)
const int LED_PIN = 9;       // 必須是有 ~ 的腳位(3、5、6、9、10、11)

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  for (int b = 0; b <= 255; b += 5) {   // 由暗到亮:0、5、10 … 255
    analogWrite(LED_PIN, b);            // 輸出 PWM,b 是亮度(0–255)
    delay({fade});
  }
  for (int b = 255; b >= 0; b -= 5) {   // 由亮到暗:255、250 … 0
    analogWrite(LED_PIN, b);
    delay({fade});
  }
}
"""
BEEP = """// 第 6 篇:蜂鳴器「嗶嗶嗶」,停一下,再重複
const int BUZZER_PIN = 8;

void setup() {
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop() {
  for (int i = 0; i < 3; i++) {          // 嗶 3 聲
    digitalWrite(BUZZER_PIN, HIGH);      // 通電:主動式蜂鳴器就會響
    delay(100);
    digitalWrite(BUZZER_PIN, LOW);       // 斷電:停止
    delay(100);
  }
  delay({pause});                        // 停一下再重複
}
"""
TONE = """// 選修:被動式蜂鳴器,用 tone() 指定音高(主動式蜂鳴器請不要用)
const int BUZZER_PIN = 8;

void setup() {
}

void loop() {
  tone(BUZZER_PIN, 440);   // 輸出 440 Hz 的聲音(國際標準音 A)
  delay(500);
  noTone(BUZZER_PIN);      // 停止
  delay(500);
}
"""
SOS = """// 挑戰:SOS 求救訊號(三短、三長、三短)
const int BUZZER_PIN = 8;

void beep(int ms) {                      // 自己定義的函式:響 ms 毫秒,再停 100 毫秒
  digitalWrite(BUZZER_PIN, HIGH);
  delay(ms);
  digitalWrite(BUZZER_PIN, LOW);
  delay(100);
}

void setup() {
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop() {
  for (int i = 0; i < 3; i++) { beep(100); }   // 三短
  for (int i = 0; i < 3; i++) { beep(300); }   // 三長
  for (int i = 0; i < 3; i++) { beep(100); }   // 三短
  delay({pause});
}
"""
FILL = dict(fade="20", pause="1000")
SKETCHES = [
    dict(name="pwm-fade", code=FADE, fill=FILL, circuit=CIRC, code_pins={"LED_PIN": "UNO.D9"},
         sim=dict(kind="ocr", pin="D9", addr=0x88, seconds=2.3, up_ms=1040, tol_ms=60)),
    dict(name="pwm-beep", code=BEEP, fill=FILL, circuit=CIRC, code_pins={"BUZZER_PIN": "UNO.D8"},
         sim=dict(kind="pattern", pin="D8", seconds=3.5, seq=[(1, 100), (0, 100), (1, 100), (0, 100), (1, 100), (0, 1100)], tol_ms=5)),
    dict(name="pwm-tone", code=TONE, fill=FILL, circuit=CIRC, code_pins={"BUZZER_PIN": "UNO.D8"},
         sim=dict(kind="freq", pin="D8", seconds=1.2, window_ms=500, hz=440, tol_pct=3)),
    dict(name="pwm-sos", code=SOS, fill=FILL, circuit=CIRC, code_pins={"BUZZER_PIN": "UNO.D8"}),
]

pwm_widget = ('<div class="panel" data-pwmbox data-pin="9">'
              '<div class="wgrid f2"><div><label>拖曳:analogWrite 的值(0–255)</label><input type="range" min="0" max="255" value="128" data-pwm="v"></div>'
              '<div><label>或直接輸入數字</label><input data-pwm="num" value="128" inputmode="numeric" autocomplete="off"></div></div>'
              '<svg class="pwm-svg" viewBox="0 0 520 150" role="img" aria-label="PWM 波形示意">'
              '<line x1="50" y1="30" x2="500" y2="30" stroke="#D1CFC5" stroke-dasharray="3 4"/><line x1="50" y1="120" x2="500" y2="120" stroke="#D1CFC5"/>'
              '<text x="42" y="34" font-size="11" fill="#87867F" text-anchor="end" font-family="ui-monospace,Menlo,Consolas,monospace">5 V</text>'
              '<text x="42" y="124" font-size="11" fill="#87867F" text-anchor="end" font-family="ui-monospace,Menlo,Consolas,monospace">0 V</text>'
              '<polyline class="pwm-wave" points="" fill="none" stroke="#D97757" stroke-width="3" stroke-linejoin="round"/>'
              '<line x1="50" y1="140" x2="160" y2="140" stroke="#87867F"/><line x1="50" y1="135" x2="50" y2="145" stroke="#87867F"/><line x1="160" y1="135" x2="160" y2="145" stroke="#87867F"/>'
              '<text x="105" y="136" font-size="11" fill="#87867F" text-anchor="middle" font-family="system-ui,sans-serif">一個週期(約 2 毫秒)</text></svg>'
              '<div class="rc-out pwm-out" aria-live="polite" style="margin-top:8px"></div>'
              '<p style="margin:10px 0 0;font-size:14px;color:var(--gray-700)">LED 的亮度感覺:<span class="pwm-led"></span></p></div>')

what = section("what", "數位腳位只有「開」和「關」,怎麼做出「半亮」?",
  '<p class="sub" style="margin-bottom:14px">到目前為止,LED 只有亮或滅。要讓它漸漸變亮、變暗,需要「中間值」。Arduino 的做法叫 <b>PWM</b>(脈衝寬度調變):<b>每秒開關幾百次,調整「開」佔多少比例</b>。</p>',
  '<div class="panel"><h3>三個關鍵</h3>'
  '<ul style="margin:0;padding-left:20px"><li><b>閃得夠快,眼睛看不出來</b>:Uno 的 PWM 每秒約開關 490 次(5、6 號腳約 980 次),眼睛只看到平均亮度。</li>'
  '<li><b>工作週期(duty cycle)</b>:一個週期裡「開」的時間占比。占 50% = 約一半亮。</li>'
  '<li><b><code>analogWrite(腳位, 值)</code></b>:值 0–255。0 是一直關,255 是一直開,128 約 50%。</li></ul></div>',
  '<h3 style="margin-top:26px">拖曳看看</h3>', pwm_widget,
  tip("只有<b>有 <code>~</code> 標記的腳位</b>能做 PWM:Uno 上是 <b>3、5、6、9、10、11</b>。其他腳位也能呼叫 <code>analogWrite</code>,但只會變成「值 &lt; 128 就關、≥ 128 就開」,沒有中間值。"))

sch_svg, sch_legend = bb.schematic_svg(CIRC, mark=("bz",))
wire = section("wire", "接線:一個 LED(9 號腳)加一個蜂鳴器(8 號腳)",
  '<p class="sub" style="margin-bottom:14px">兩組電路各自獨立,負極共用 − 軌。LED 一定要接 <b>9 號腳</b>(有 <code>~</code>)。</p>',
  bb.stepper_html(CIRC),
  '<p class="sk">Uno 轉了 180 度擺放,數位腳位排在下緣。圖只畫左邊 22 欄,以欄號與 a–j 為準(手機上可以左右滑動圖)。</p>',
  '<h3 style="margin-top:26px">接線表</h3>', bb.wiring_table(CIRC),
  warn("<b>蜂鳴器有方向:</b>+ 腳要接靠電阻的一邊。接反了不會壞,但可能不響。接線前先拔 USB。", "注意方向"),
  '<h3 style="margin-top:26px">蜂鳴器的原理圖符號</h3>',
  canvas(sch_svg, [(n, '<span class="newsym">新符號</span>' + t) for n, t in sch_legend]),
  '<div class="linkbox" id="linkInfo" style="margin-top:12px">點原理圖裡的蜂鳴器或電阻,看它在麵包板上是哪一個。</div>')

buzz = section("buzz", "主動式與被動式蜂鳴器,差在哪裡?",
  table("g3", ["", "主動式(Active)", "被動式(Passive)"], [
    ["內部", "<b>有</b>振盪電路", "<b>沒有</b>,只是一個會震動的喇叭"],
    ["怎麼讓它響", "只要<b>通電</b>就響(<code>digitalWrite(HIGH)</code>)", "要送<b>變化的頻率</b>給它(<code>tone(腳位, 頻率)</code>)"],
    ["聲音", "只有<b>一種固定音高</b>", "<b>可以換音高</b>,能唱出音階"],
    ["怎麼分辨", "背面通常封著黑色膠;直接接 5V 會響", "背面常看得到綠色電路板;直接接 5V 只會「喀」一聲"],
  ]),
  warn("<b>主動式蜂鳴器請不要用 <code>tone()</code>。</b>它自己會振盪,收到變化的訊號會變成雜音。本篇主線用主動式;<code>tone()</code> 放在選修,需要被動式蜂鳴器。", "別混用"),
  tip("小型 5 V 蜂鳴器的電流常在 10–30 mA 之間,接近 Uno 每腳 20 mA 的建議上限。本篇在蜂鳴器前串了 220Ω 電阻當保險,聲音會小一點,但比較安全。<b>以你手上蜂鳴器的規格為準</b>,電流大的蜂鳴器需要電晶體驅動,本主題不涵蓋。"))

fillsec = section("fill", "先填入你想要的速度與間隔",
  fill([("fade", "漸亮漸暗每一步的間隔(毫秒)", True), ("pause", "蜂鳴器兩輪之間的停頓(毫秒)", True)]),
  '<p class="sk">空白時用範例值:20 毫秒、1000 毫秒。</p>')

def exp(items):
    return table("g2", ["這一行", "它在做什麼"], items)

code = section("code", "程式一:呼吸燈",
  cmd(FADE, cap="呼吸燈(接在 9 號腳的 LED)", cpp=True),
  exp([
    ["<code>const int LED_PIN = 9;</code>", "LED 接的腳位,<b>必須是有 <code>~</code> 的腳位</b>。"],
    ["<code>for (int b = 0; b &lt;= 255; b += 5)</code>", "<code>b</code> 從 0 開始,每圈加 5,到 255 為止。<code>b += 5</code> 是 <code>b = b + 5</code> 的簡寫。"],
    ["<code>analogWrite(LED_PIN, b);</code>", "輸出 PWM,亮度是 <code>b</code>。<b>不需要</b>寫 <code>digitalWrite</code>。"],
    ["<code>for (int b = 255; b &gt;= 0; b -= 5)</code>", "反過來:從 255 每圈減 5,減到 0。<code>b -= 5</code> 是 <code>b = b - 5</code>。"],
  ]),
  see("紅色 LED 在約 1 秒內<b>由暗漸亮</b>,再用約 1 秒<b>由亮漸暗</b>,不斷重複,像呼吸一樣。"),
  tip("<code>pinMode</code> 還是要寫:<code>analogWrite</code> 不會幫你把腳位設成輸出。名字叫 analog(類比),但它輸出的其實是 PWM 的快速開關,不是真正的類比電壓。"))

code2 = section("code2", "程式二:蜂鳴器「嗶嗶嗶」",
  cmd(BEEP, cap="蜂鳴器:嗶 3 聲、停一下、重複", cpp=True),
  exp([
    ["<code>digitalWrite(BUZZER_PIN, HIGH);</code>", "輸出 5 V,主動式蜂鳴器通電就響。"],
    ["<code>delay(100);</code>", "響 100 毫秒(0.1 秒)。"],
    ["<code>digitalWrite(BUZZER_PIN, LOW);</code>", "斷電,停止。再 <code>delay(100)</code> 是兩聲之間的空檔。"],
    ["<code>for (int i = 0; i &lt; 3; i++)</code>", "把「響、停」做 3 次(第 4 篇學過的 for)。"],
    ["<code>delay({pause});</code>", "3 聲之後停一下,再回到 <code>loop()</code> 開頭。"],
  ]),
  see("蜂鳴器發出「嗶、嗶、嗶」三聲短音,停一秒,再重複。"),
  details("選修:被動式蜂鳴器與 tone()",
    '<p>如果你有<b>被動式蜂鳴器</b>,接線和上面完全一樣(換下主動式即可)。<code>tone(腳位, 頻率)</code> 會讓腳位以指定頻率快速開關,不需要自己寫迴圈。</p>' +
    cmd(TONE, cap="tone():送 440 Hz 的聲音 0.5 秒", cpp=True) +
    exp([["<code>tone(BUZZER_PIN, 440);</code>", "持續輸出 440 次/秒的方波,蜂鳴器發出對應音高。程式不會停在這一行,會繼續往下跑。"],
         ["<code>noTone(BUZZER_PIN);</code>", "停止發聲。"]]) +
    '<p style="margin-top:12px;margin-bottom:0">頻率越高音越高:262 Hz 是 Do,294 Hz 是 Re,330 Hz 是 Mi。改 <code>440</code> 試試。</p>'))

try_ = section("try", "改改看",
  table("g3", ["挑戰", "怎麼改", "你會看到"], [
    ["呼吸變慢", "「每一步的間隔」改 40", "漸亮漸暗各約 2 秒。"],
    ["換腳位", "把 LED 的藍線改插 10 號腳,程式 <code>LED_PIN</code> 改 10", "效果相同:10 號腳也有 <code>~</code>。"],
    ["非 PWM 腳位", "把 LED 的藍線改插 <b>8 號腳</b>(沒有 ~),程式不變", "不再漸變,只是突然亮、突然滅。這就是 PWM 腳位的差別。"],
    ["SOS", "改用下面的 SOS 程式", "三短、三長、三短的求救訊號。"],
  ]),
  details("SOS 程式(自己定義函式 beep)",
    cmd(SOS, cap="挑戰:SOS", cpp=True) +
    exp([["<code>void beep(int ms) { … }</code>", "自己定義的函式:響 <code>ms</code> 毫秒再停 100 毫秒。以後想響多久,只要寫 <code>beep(…)</code>。"],
         ["<code>beep(100);</code> 與 <code>beep(300);</code>", "短音 100 毫秒,長音 300 毫秒。"]])))

gotchas = section("gotchas", "常見卡關",
  details("LED 不會漸變,只是一直亮或突然亮暗",
    "<p>LED 沒接在有 <code>~</code> 的腳位。<code>analogWrite</code> 在非 PWM 腳位上只會「值 &lt; 128 關、≥ 128 開」。把訊號線改插 9、10 或 11 號腳,並同步修改程式。</p>", True) +
  details("蜂鳴器完全不響",
    ops(["<b>蜂鳴器是不是主動式</b>:被動式用 <code>digitalWrite(HIGH)</code> 只會喀一聲,要用 <code>tone()</code>。", "<b>+ 腳方向</b>:長腳(或標 + 的那隻)靠電阻那側。", "兩隻腳有沒有插在<b>不同欄</b>,且 − 腳那一欄有黑色短線接到 − 軌。", "程式腳位(8)與訊號線插的腳位一致。"])) +
  details("蜂鳴器一直響不停",
    "<p>多半是蜂鳴器接到了 5V 而不是 8 號腳,或程式沒有上傳成功(還跑著上一個程式)。重新檢查訊號線,重新上傳。</p>") +
  details("聲音很小",
    "<p>正常:串了 220Ω 電阻,電流變小。想要大聲一點,可以換小一點的電阻(例如 100Ω),<b>但要確認蜂鳴器規格的電流不超過 20 mA</b>。</p>") +
  details("LED 呼吸時閃爍、不順",
    "<p>檢查 <code>delay</code> 值是不是太大(超過 40 毫秒就看得到一格一格變亮),或太小(小於 5 毫秒就變化得太快看不出來)。</p>"))

SIM = {
  "a1": "<b>不用。</b>8 號腳沒有 PWM 功能,所以 <code>analogWrite</code> 只會輸出全亮或全滅,跟 IDE 設定無關。",
  "a2": "<b>對。</b>把訊號線改插到有 <code>~</code> 的腳位(9、10、11 都可以),程式裡的 <code>LED_PIN</code> 也要改成同一個數字。",
  "a3": "<b>沒有用。</b>電阻影響的是整體亮度,不能讓沒有 PWM 的腳位出現中間亮度。",
}
QUIZ = quiz_cfg([
  ("<code>analogWrite(9, 128);</code> 大約代表?", ["全亮", "約 50% 的工作週期", "全滅"], 1,
   "128 約是 255 的一半,工作週期約 50%,平均電壓約 2.5 V。"),
  ("Uno 上哪些腳位可以輸出 PWM?", ["所有數位腳位", "有 ~ 標記的:3、5、6、9、10、11", "只有 13 號腳"], 1,
   "只有有 ~ 標記的腳位才有 PWM 硬體功能。"),
  ("主動式蜂鳴器要發聲,最簡單的做法是?", ["digitalWrite(HIGH) 通電", "一定要 tone()", "analogWrite(0)"], 0,
   "主動式有內建振盪電路,通電就響,音高固定。"),
  ("<code>b -= 5</code> 的意思是?", ["b = 5", "b = b - 5", "b 比 5 小"], 1,
   "-= 是「減去再存回去」,等於 b = b - 5。"),
  ("PWM 讓 LED 看起來半亮,是因為?", ["電壓真的變成 2.5 V", "開關得太快,眼睛只看到平均亮度", "LED 壞了"], 1,
   "PWM 輸出的仍是 0 或 5 V,只是比例不同。"),
])
practice = section("practice", "動手演練與延伸閱讀",
  sim("", "情境:你的 LED 只會一下全亮、一下全滅,不會漸變", "最可能的原因與做法是?",
      [("a1", "重新安裝 Arduino IDE"), ("a2", "LED 沒接在有 ~ 的腳位,改插 9、10 或 11 號腳並同步改程式"), ("a3", "換更大的電阻")]),
  QUIZ_HTML,
  checks(["我能說出 PWM 是「很快地開關,調整開的比例」。",
          "我知道有 ~ 的腳位才能做 PWM,以及是哪幾個腳位。",
          "我的呼吸燈會漸亮、漸暗。",
          "我分得出主動式與被動式蜂鳴器,知道主動式用 digitalWrite。",
          "我的蜂鳴器能「嗶嗶嗶」三聲。",
          "我知道蜂鳴器也有方向(+ 腳),並且前面串了電阻。"], "做完之後,對照這張清單"),
  resources([
    ("https://docs.arduino.cc/language-reference/en/functions/analog-io/analogwrite/", "analogWrite()", "Arduino language reference"),
    ("https://docs.arduino.cc/language-reference/en/functions/advanced-io/tone/", "tone()", "Arduino language reference"),
    ("https://docs.arduino.cc/language-reference/en/functions/digital-io/digitalwrite/", "digitalWrite()", "Arduino language reference"),
  ], "Arduino 官方文件"))

SPEC = dict(
    dir="arduino",
    file="arduino-pwm-guide.html",
    title="PWM 呼吸燈與蜂鳴器",
    eyebrow="第 6 篇 · PWM 與蜂鳴器",
    h1="讓燈漸漸變亮變暗,再讓蜂鳴器開口說話",
    sub="學會 PWM:不用真的變電壓,也能控制亮度。再接一顆蜂鳴器,認識主動式與被動式的差別。",
    tldr="<b>PWM = 很快地開關,調整開的比例</b>。<code>analogWrite(腳位, 0–255)</code> 只能用在有 <code>~</code> 的腳位(3、5、6、9、10、11)。<b>主動式蜂鳴器通電就響</b>,被動式要用 <code>tone()</code> 給頻率。",
    toc=[("what", "什麼是 PWM"), ("wire", "接線"), ("buzz", "兩種蜂鳴器"), ("fill", "填入你的資料"), ("code", "程式一:呼吸燈"),
         ("code2", "程式二:蜂鳴器"), ("try", "改改看"), ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
    body="\n\n".join([what, wire, buzz, fillsec, code, code2, try_, gotchas, practice]),
    config=dict(fill=FILL, sim=SIM, quiz=QUIZ, wiring=[bb.wiring_config(CIRC)], parts=bb.parts_info(CIRC)),
    prev=("arduino-schematic-guide.html", "讀懂電路圖"),
    next=("arduino-button-guide.html", "按鈕:讀取輸入"),
)
