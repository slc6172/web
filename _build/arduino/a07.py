# -*- coding: utf-8 -*-
from h import *
import bb

CIRC = bb.Circuit(
    "button-led", 22,
    parts=[
        bb.Button("BTN1", "e5", "f7", "e7", "f5", 1),
        bb.Resistor("R1", 220, "b11", "b15", 2), bb.LED("LED1", "red", "d15", "d16", 2),
        bb.Wire("K1", "a16", "t-16", "black", 3, route="straight"),
        bb.Wire("KB", "j7", "b-7", "black", 3, route="straight"),
        bb.Wire("L", "t-22", "b-22", "green", 3, route="straight"),
        bb.Wire("S2", "UNO.D2", "a5", "blue", 4), bb.Wire("S1", "UNO.D8", "a11", "orange", 4),
        bb.Wire("G", "UNO.GND", "t-20", "black", 5),
    ],
    steps=[
        ("放按鈕", "按鈕<b>跨在中間凹槽上</b>:四隻腳分別插在 <code>e5</code>、<code>e7</code>、<code>f5</code>、<code>f7</code>。<br>接線只用<b>對角</b>的兩隻腳:<code>e5</code> 與 <code>f7</code>(圖上橘光圈)。另外兩隻腳也會插進孔裡,但不接線。按鈕腳是方形排列,插不進時,先把腳扶正再往下壓。"),
        ("放電阻與 LED", "<b>電阻</b>橫放在 <code>b11–b15</code>;<b>紅色 LED</b>長腳(+)插 <code>d15</code>、短腳(−)插 <code>d16</code>。這一組和第 3 篇一樣。"),
        ("三條線:都是 GND 的路", "① 黑色短線 <code>a16</code> → <code>t-16</code>:LED 的負極接到上方 − 軌。<br>② 黑色短線 <code>j7</code> → <code>b-7</code>:按鈕的一腳接到<b>下方</b> − 軌。<br>③ 綠色線 <code>t-22</code> → <code>b-22</code>:把上下兩條 − 軌連起來(按鈕在下半部,LED 在上半部,需要共用 GND)。"),
        ("兩條訊號線:2 號腳與 8 號腳", "藍線:Uno <b>2 號腳</b> → <code>a5</code>(按鈕上腳那一欄)。<br>橘線:Uno <b>8 號腳</b> → <code>a11</code>(電阻左端那一欄)。"),
        ("黑線:Uno GND → − 軌", "黑色杜邦線一端插 Uno 數位腳位排的 <strong>GND</strong>,另一端插 <code>t-20</code>。<br>整條 GND 現在同時供給 LED 與按鈕。"),
    ],
    chains=[["UNO.D8", "R1", "LED1", "UNO.GND"], ["UNO.D2", "BTN1", "UNO.GND"]],
    intro="先<strong>拔掉 USB 線</strong>。這次有兩部分:<b>輸入</b>(按鈕接 2 號腳)與<b>輸出</b>(LED 接 8 號腳)。按鈕不需要電阻:程式會啟用 Uno 內建的上拉電阻。",
    done="按鈕的一腳接 2 號腳,另一腳接 GND;LED 組和第 3 篇相同。上下兩條 − 軌用一條綠線連在一起。檢查:按鈕是用對角的兩腳接線。",
)
CIRCUITS = [CIRC]

A = """// 第 7 篇(寫法一):按住按鈕,LED 才亮
const int BUTTON_PIN = 2;   // 按鈕接在 2 號腳
const int LED_PIN = 8;      // LED 接在 8 號腳

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);  // 輸入模式,並啟用內建上拉電阻
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  int state = digitalRead(BUTTON_PIN);  // 讀取 2 號腳:HIGH(1)或 LOW(0)
  if (state == LOW) {                   // 等於 LOW:按鈕被按下(2 號腳被接到 GND)
    digitalWrite(LED_PIN, HIGH);        // 亮
  } else {                              // 否則:沒按
    digitalWrite(LED_PIN, LOW);         // 滅
  }
}
"""
B = """// 第 7 篇(寫法二):按一下切換 LED(亮 ↔ 滅),並處理彈跳
const int BUTTON_PIN = 2;
const int LED_PIN = 8;
bool ledOn = false;                    // 記住 LED 現在是不是亮著

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  if (digitalRead(BUTTON_PIN) == LOW) {        // 偵測到按下
    ledOn = !ledOn;                            // 反轉:true 變 false,false 變 true
    if (ledOn) {
      digitalWrite(LED_PIN, HIGH);
    } else {
      digitalWrite(LED_PIN, LOW);
    }
    delay({wait});                             // 等彈跳過去
    while (digitalRead(BUTTON_PIN) == LOW) {   // 一直等,直到手放開
    }
    delay({wait});                             // 放開時也會彈跳,再等一下
  }
}
"""
C = """// 實驗:故意不啟用上拉電阻(INPUT),看看浮接會怎樣
const int BUTTON_PIN = 2;
const int LED_PIN = 8;

void setup() {
  pinMode(BUTTON_PIN, INPUT);          // 只是輸入,沒有任何電阻:2 號腳沒按時是「浮接」
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  if (digitalRead(BUTTON_PIN) == LOW) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
}
"""
D = """// 挑戰:按一下,LED 閃三下
const int BUTTON_PIN = 2;
const int LED_PIN = 8;

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  if (digitalRead(BUTTON_PIN) == LOW) {
    for (int i = 0; i < 3; i++) {
      digitalWrite(LED_PIN, HIGH);
      delay(150);
      digitalWrite(LED_PIN, LOW);
      delay(150);
    }
  }
}
"""
FILL = dict(wait="30")
bounce = [("D2", 1, 0), ("D2", 0, 500), ("D2", 1, 502), ("D2", 0, 504), ("D2", 1, 700), ("D2", 0, 702), ("D2", 1, 704),
          ("D2", 0, 1200), ("D2", 1, 1203), ("D2", 0, 1206), ("D2", 1, 1400), ("D2", 0, 1402), ("D2", 1, 1405)]
SKETCHES = [
    dict(name="btn-hold", code=A, fill=FILL, circuit=CIRC, code_pins={"BUTTON_PIN": "UNO.D2", "LED_PIN": "UNO.D8"},
         sim=dict(kind="input", pin="D8", seconds=1.3, inputs=[("D2", 1, 0), ("D2", 0, 500), ("D2", 1, 900)], expect=[(1, 500), (0, 900)], tol_ms=5,
                  note="D2 在 500 ms 按下、900 ms 放開")),
    dict(name="btn-toggle", code=B, fill=FILL, circuit=CIRC, code_pins={"BUTTON_PIN": "UNO.D2", "LED_PIN": "UNO.D8"},
         sim=dict(kind="input", pin="D8", seconds=1.8, inputs=bounce, expect=[(1, 500), (0, 1200)], tol_ms=5,
                  note="兩次按下,每次按下與放開都帶 2–4 ms 的彈跳,LED 仍只切換一次")),
    dict(name="btn-float", code=C, fill=FILL, circuit=CIRC, code_pins={"BUTTON_PIN": "UNO.D2", "LED_PIN": "UNO.D8"}),
    dict(name="btn-three", code=D, fill=FILL, circuit=CIRC, code_pins={"BUTTON_PIN": "UNO.D2", "LED_PIN": "UNO.D8"},
         sim=dict(kind="input", pin="D8", seconds=1.5, inputs=[("D2", 1, 0), ("D2", 0, 500), ("D2", 1, 700)],
                  expect=[(1, 500), (0, 650), (1, 800), (0, 950), (1, 1100), (0, 1250)], tol_ms=5, note="D2 在 500 ms 按下、700 ms 放開")),
]

# 與本頁電路相關的參考原理圖:外接下拉電阻的寫法(只讀、不做)
pd_circ = bb.Circuit("pulldown-ref", 12,
    parts=[bb.Button("BTN1", "e5", "f7", "e7", "f5", 1), bb.Resistor("R1", 10000, "j7", "j10", 1)],
    steps=[("a", "a")], chains=[["UNO.5V", "BTN1", "UNO.D2"], ["UNO.D2", "R1", "UNO.GND"]])
PD_SCH = bb.schematic_svg(pd_circ, mark=())[0]

btnsim = ('<div class="panel" data-btnsim>'
          '<div class="wgrid f2"><div><label>2 號腳的模式</label><select data-bs="mode"><option value="pullup">INPUT_PULLUP(內建上拉電阻)</option><option value="plain">INPUT(沒有任何電阻)</option></select></div>'
          '<div><label>按鈕</label><button type="button" class="primary" data-bs="btn" style="width:100%">目前:放開(點一下按住)</button></div></div>'
          '<div class="canvas" style="margin-top:12px"><svg viewBox="0 0 560 230" role="img" aria-label="按鈕與上拉電阻示意圖" style="min-width:520px">'
          '<defs>' + bb.STYLE + '</defs><rect width="560" height="230" fill="#FFFFFF"/>'
          '<rect x="20" y="16" width="238" height="200" rx="12" fill="#FAF9F5" stroke="#87867F" stroke-dasharray="5 4"/>'
          '<text x="34" y="38" class="sb" fill="#3D3D3A">Uno 內部</text>'
          '<g class="pu"><line x1="100" y1="52" x2="136" y2="52" stroke="#3D3D3A" stroke-width="2.4" stroke-linecap="round"/>'
          '<text x="118" y="46" class="mb" fill="#B04A3F" text-anchor="middle">5V</text><line x1="118" y1="52" x2="118" y2="70" stroke="#3D3D3A" stroke-width="2"/>'
          '<polyline points="118,70 118,76 108,84 128,96 108,108 128,120 118,128 118,134" fill="none" stroke="#3D3D3A" stroke-width="2" stroke-linejoin="round"/>'
          '<text x="140" y="104" class="s" fill="#3D3D3A">上拉電阻</text><text x="140" y="118" class="m" fill="#87867F">約 20–50 kΩ</text>'
          '<line x1="118" y1="134" x2="118" y2="156" stroke="#3D3D3A" stroke-width="2"/></g>'
          '<circle class="bs-node" cx="118" cy="156" r="6" fill="#788C5D"/>'
          '<line x1="118" y1="156" x2="300" y2="156" stroke="#3D3D3A" stroke-width="2"/>'
          '<rect x="226" y="141" width="64" height="30" rx="8" fill="#F0EEE6" stroke="#3D3D3A" stroke-width="1.5"/><text x="258" y="160" class="mb" fill="#141413" text-anchor="middle">D2 腳位</text>'
          '<circle cx="340" cy="156" r="4" fill="#3D3D3A"/><circle cx="410" cy="156" r="4" fill="#3D3D3A"/>'
          '<g class="sw-open"><line x1="340" y1="156" x2="402" y2="128" stroke="#3D3D3A" stroke-width="3" stroke-linecap="round"/></g>'
          '<g class="sw-closed" style="display:none"><line x1="340" y1="156" x2="410" y2="156" stroke="#B04A3F" stroke-width="3.5" stroke-linecap="round"/></g>'
          '<text x="375" y="190" class="s" fill="#3D3D3A" text-anchor="middle">按鈕</text>'
          '<line x1="410" y1="156" x2="480" y2="156" stroke="#3D3D3A" stroke-width="2"/><line x1="480" y1="156" x2="480" y2="176" stroke="#3D3D3A" stroke-width="2"/>'
          '<line x1="464" y1="176" x2="496" y2="176" stroke="#3D3D3A" stroke-width="2.4" stroke-linecap="round"/><line x1="470" y1="183" x2="490" y2="183" stroke="#3D3D3A" stroke-width="2.4" stroke-linecap="round"/><line x1="476" y1="190" x2="484" y2="190" stroke="#3D3D3A" stroke-width="2.4" stroke-linecap="round"/>'
          '<text x="480" y="210" class="s" fill="#87867F" text-anchor="middle">GND</text>'
          '<text class="bs-level mb" x="300" y="56" fill="#788C5D" font-size="15">digitalRead(2) → HIGH(1)</text></svg></div>'
          '<div class="rc-out bs-out" aria-live="polite"></div></div>')

what = section("what", "輸入:讓 Arduino「聽到」外面的世界",
  '<p class="sub" style="margin-bottom:14px">前面幾篇都是輸出(Arduino 控制 LED、蜂鳴器)。這一篇換方向:<b>輸入</b>。按鈕是最簡單的輸入裝置:按下去,Arduino 就能知道。</p>',
  '<div class="panel"><h3>按鈕怎麼運作</h3>'
  '<p>按鈕內部是兩個接點。<b>沒按時是斷開的,按下去就接通</b>,放開又斷開。所以它就是一個「用手控制的線」。</p>'
  '<p style="margin-bottom:0">Arduino 要知道有沒有按,是讀 2 號腳的電壓:<b>HIGH(約 5 V)或 LOW(約 0 V)</b>。問題是:沒按的時候,2 號腳接著什麼?</p></div>',
  '<h3 style="margin-top:26px">浮接,與上拉電阻</h3>',
  '<p class="sub" style="margin-bottom:14px">如果按鈕一端接 2 號腳、另一端接 GND,<b>沒按時 2 號腳什麼都沒接</b>,它會像天線一樣收到雜訊,讀值亂跳(<b>浮接</b>)。解決辦法是讓沒按時有個「預設值」:Uno 內建一顆<b>上拉電阻</b>,可以用程式打開。試試看,切換模式與按鈕:</p>',
  btnsim,
  tip("<b>「上拉」</b>就是沒按時,透過一顆電阻把腳位輕輕拉向 5 V,讀到 HIGH;<b>按下去時按鈕把腳位接到 GND,讀到 LOW</b>。所以用 <code>INPUT_PULLUP</code> 時,<b>按下是 LOW、放開是 HIGH</b>(和直覺相反,但很快會習慣)。"))

sch_svg, sch_legend = bb.schematic_svg(CIRC, mark=("btn",))
wire = section("wire", "接線:一個按鈕(2 號腳)加一個 LED(8 號腳)",
  '<p class="sub" style="margin-bottom:14px">LED 這一組和第 3 篇相同;新的是按鈕:一腳接 2 號腳,另一腳接 GND。按鈕<b>不需要電阻</b>,因為程式會啟用內建上拉電阻。</p>',
  bb.stepper_html(CIRC),
  '<p class="sk">Uno 轉了 180 度擺放,數位腳位排在下緣。圖只畫左邊 22 欄,以欄號與 a–j 為準(手機上可以左右滑動圖)。</p>',
  '<h3 style="margin-top:26px">接線表</h3>', bb.wiring_table(CIRC),
  warn("<b>按鈕要用「對角」的兩隻腳。</b>四腳按鈕的內部,<b>同一側的兩隻腳永遠相通</b>。如果你把接線接在同一側的兩腳,按鈕等於一直按著(或完全按不動),是新手最常見的按鈕錯誤。對角的兩腳,在任何方向下都是「按下才相通」。", "最常見的錯誤"),
  '<h3 style="margin-top:26px">原理圖</h3>',
  canvas(sch_svg, [(n, '<span class="newsym">新符號</span>' + t) for n, t in sch_legend]),
  '<div class="linkbox" id="linkInfo" style="margin-top:12px">點原理圖裡的按鈕或 LED,看它在麵包板上是哪一個。</div>',
  tip("原理圖上有<b>兩個 GND 符號</b>(一個給 LED、一個給按鈕),它們是同一個點,對應到麵包板上就是「用綠色線連起來的上下兩條 − 軌」。"))

fillsec = section("fill", "先填入去彈跳的等待時間",
  fill([("wait", "等待彈跳的時間(毫秒)", True)]),
  '<p class="sk">空白時用範例值 30 毫秒。一般按鈕的彈跳在 1–10 毫秒內,30 毫秒很夠用。</p>')

def exp(items):
    return table("g2", ["這一行", "它在做什麼"], items)

code = section("code", "程式一:按住,LED 才亮",
  cmd(A, cap="按住按鈕,LED 才亮", cpp=True),
  exp([
    ["<code>pinMode(BUTTON_PIN, INPUT_PULLUP);</code>", "把 2 號腳設成<b>輸入</b>,並啟用<b>內建上拉電阻</b>。沒按時讀到 HIGH。"],
    ["<code>int state = digitalRead(BUTTON_PIN);</code>", "讀取 2 號腳的電位,存進整數變數 <code>state</code>(HIGH 是 1、LOW 是 0)。"],
    ["<code>if (state == LOW) { … } else { … }</code>", "<b>條件判斷</b>:如果括號裡成立,做第一個大括號的事;<b>否則</b>做 <code>else</code> 後面的事。"],
    ["<code>==</code>", "<b>兩個等號是「比較是否相等」</b>。一個等號 <code>=</code> 是「放進去(指定)」,兩者不同,新手常搞混。"],
  ]),
  table("g3", ["比較符號", "意思", "例子"], [
    ["<code>==</code>", "等於", "<code>state == LOW</code>"],
    ["<code>!=</code>", "不等於", "<code>state != LOW</code>"],
    ["<code>&lt;</code>、<code>&gt;</code>", "小於、大於", "<code>i &lt; 3</code>"],
    ["<code>&lt;=</code>、<code>&gt;=</code>", "小於等於、大於等於", "<code>b &lt;= 255</code>"],
  ]),
  see("<b>按住</b>按鈕時,LED 亮;<b>放開</b>,LED 熄滅。注意:按下去讀到的是 <code>LOW</code>。"))

code2 = section("code2", "程式二:按一下,切換亮或滅",
  '<p class="sub" style="margin-bottom:14px">想要「按一下亮、再按一下滅」,程式必須<b>記住</b> LED 現在是亮還是滅。這就是變數的用處。</p>',
  cmd(B, cap="按一下切換 LED,並處理彈跳", cpp=True),
  exp([
    ["<code>bool ledOn = false;</code>", "<b>布林變數</b>:只有 <code>true</code>(是)與 <code>false</code>(否)兩種值。拿來記「LED 現在亮不亮」。寫在函式外面,值才會一直保留。"],
    ["<code>ledOn = !ledOn;</code>", "<code>!</code> 是「相反」:true 變 false,false 變 true。每按一次,翻轉一次。"],
    ["<code>delay({wait});</code>", "按下去的瞬間,按鈕的金屬片會<b>彈跳</b>:短短幾毫秒內開開關關好幾次(見下圖)。等一下,讓它穩定。"],
    ["<code>while (digitalRead(BUTTON_PIN) == LOW) { }</code>", "<b>while 迴圈</b>:條件成立就一直重複。大括號裡是空的,表示什麼都不做、只是<b>等到你放手</b>。這樣按住不放也只會切換一次。"],
  ]),
  '<h3 style="margin-top:22px">什麼是彈跳?</h3>',
  canvas(('<svg viewBox="0 0 520 130" role="img" aria-label="按鈕彈跳示意圖" style="min-width:480px"><defs>' + bb.STYLE + '</defs><rect width="520" height="130" fill="#FFFFFF"/>'
          '<text x="14" y="30" class="mb" fill="#3D3D3A">HIGH</text><text x="14" y="104" class="mb" fill="#3D3D3A">LOW</text>'
          '<polyline points="60,24 160,24 160,100 168,100 168,24 176,24 176,100 184,100 184,24 190,24 190,100 440,100 440,24 448,24 448,100 454,100 454,24 500,24" fill="none" stroke="#D97757" stroke-width="3" stroke-linejoin="round"/>'
          '<text x="175" y="124" class="s" fill="#87867F" text-anchor="middle">按下:幾毫秒內彈跳數次</text><text x="447" y="124" class="s" fill="#87867F" text-anchor="middle">放開:也會彈跳</text></svg>'), []),
  '<p style="margin-top:12px">Arduino 一秒能讀幾萬次,彈跳的每一下它都看得到。沒有處理的話,「按一下」可能被當成「按了好幾下」,LED 就會亂切換。<b>去彈跳</b>最簡單的做法就是:偵測到變化後,<b>等一小段時間再繼續</b>。</p>',
  see("每按<b>一下</b>,LED 切換<b>一次</b>(亮 → 滅 → 亮 …),不會亂跳。"),
  warn("這個寫法有個限制:<b>按住按鈕的那段時間,Arduino 被「卡」在 <code>while</code> 裡,做不了別的事</b>(例如讓另一顆燈閃)。第 15 篇的 <code>millis()</code> 會教你不卡住的做法。", "先記著"))

pdsec = section("pd", "別的教學的寫法:外接上拉 / 下拉電阻",
  '<p class="sub" style="margin-bottom:14px">你會在別的教學看到另一種做法:不用 <code>INPUT_PULLUP</code>,改成在按鈕旁<b>外接一顆 10 kΩ 電阻</b>。下面是「下拉」版本的原理圖,<b>只讀不用做</b>:</p>',
  canvas(PD_SCH, []),
  ops(["按鈕一端接 5V,另一端接 2 號腳,2 號腳再經過 10 kΩ 電阻接 GND。", "<b>沒按</b>:2 號腳透過電阻接 GND → 讀 LOW。<b>按下</b>:2 號腳接到 5V → 讀 HIGH(和 <code>INPUT_PULLUP</code> 剛好相反)。", "程式用 <code>pinMode(2, INPUT);</code>(不啟用內建上拉)。"]),
  tip("<code>INPUT_PULLUP</code> 把這顆電阻搬進晶片裡,<b>省零件、省接線</b>,本主題採用它。看到外接電阻的寫法,知道它在做同樣的事就夠了。"))

try_ = section("try", "改改看",
  table("g3", ["挑戰", "怎麼改", "你會看到"], [
    ["反過來", "寫法一裡,把 <code>HIGH</code> 與 <code>LOW</code> 對調(<code>LED_PIN</code> 那兩行)", "沒按時 LED 亮,按住時熄滅。"],
    ["親眼看浮接", "改用下面的「實驗」程式(<code>INPUT</code>)", "沒按時 LED 會不穩定、亂閃,手靠近還會變。這就是浮接。"],
    ["按一下閃三下", "改用下面的「挑戰」程式", "按一下,LED 閃三次,然後停止。"],
  ]),
  details("實驗:INPUT(沒有上拉電阻)",
    cmd(C, cap="實驗:故意浮接", cpp=True) + '<p style="margin:12px 0 0">只有一行差別:<code>INPUT_PULLUP</code> 換成 <code>INPUT</code>。做完實驗記得改回來。</p>'),
  details("挑戰:按一下,LED 閃三下",
    cmd(D, cap="挑戰:按一下閃三下", cpp=True) + '<p style="margin:12px 0 0">用到第 4 篇學的 <code>for</code>。閃的這段時間(0.9 秒),Arduino 讀不到按鈕。</p>'))

gotchas = section("gotchas", "常見卡關",
  details("LED 一直亮著,按了也沒反應",
    ops(["<b>按鈕接在同一側的兩腳</b>:換成<b>對角</b>(<code>e5</code> 與 <code>f7</code>)。", "按鈕<b>沒有跨在中間凹槽上</b>,四隻腳其實在同一半:重新插好,讓它跨過凹槽。", "<b>2 號腳的藍線沒接好</b>,或接到了錯誤的欄。"]), True) +
  details("按了沒有任何反應",
    ops(["<b>GND 沒接上</b>:按鈕下腳的黑色短線(<code>j7</code> → <code>b-7</code>)、上下 − 軌的綠色連接線、Uno GND 到 − 軌的黑線,三處都要有。", "你的麵包板電源軌如果中間斷開,檢查黑色短線與 GND 線是否接在同一半。", "<b>程式裡的腳位</b>(2、8)與接線一致。"])) +
  details("LED 亂閃,或手靠近就變",
    "<p>浮接。檢查程式是不是 <code>INPUT_PULLUP</code>(不是 <code>INPUT</code>),以及按鈕是不是真的接到 2 號腳。</p>") +
  details("按一下,LED 切換好幾次,不穩定",
    "<p>彈跳沒處理好。確認程式用的是寫法二、<code>delay</code> 與 <code>while</code> 都在,等待時間不要設成 0。</p>") +
  details("按鈕的腳插不進去",
    "<p>按鈕的腳是方形排列、容易彎。拿出來看腳有沒有歪,用手指把腳扶正,垂直下壓。別硬插,腳彎了就換一顆。</p>"))

SIM = {
  "a1": "<b>不用。</b>程式也沒錯(<code>INPUT_PULLUP</code> 的邏輯是「按下 = LOW」)。看到一直亮,先檢查按鈕的接法。",
  "a2": "<b>對。</b>一直亮代表 2 號腳永遠是 LOW,多半是按鈕接在<b>同一側的兩腳</b>(永遠相通),或根本沒跨在凹槽上。換成對角的兩腳,並確認有跨過凹槽。",
  "a3": "<b>沒有用。</b>電阻只影響亮度,不影響按鈕有沒有被讀到。",
}
QUIZ = quiz_cfg([
  ("使用 <code>INPUT_PULLUP</code>,按鈕<b>沒按</b>時讀到?", ["LOW", "HIGH", "不一定"], 1,
   "內建上拉電阻把腳位拉到 5 V,沒按讀 HIGH。按下去接到 GND 才讀 LOW。"),
  ("<code>=</code> 與 <code>==</code> 的差別?", ["一樣", "= 是指定(放進去),== 是比較是否相等", "== 是指定,= 是比較"], 1,
   "= 把值放進變數,== 判斷兩邊是否相等。if 裡要用 ==。"),
  ("四腳按鈕為什麼要用「對角」兩腳接線?", ["對角兩腳在任何方向下都是按下才相通", "對角兩腳比較省線", "只是習慣"], 0,
   "同一側的兩腳永遠相通,接錯會變成一直按著。"),
  ("按鈕的「彈跳」是指?", ["按鈕會彈起來", "按下去的瞬間訊號在幾毫秒內開開關關好幾次", "按鈕用久了會壞"], 1,
   "金屬接點碰撞時會抖動,所以要等一下再讀。"),
  ("<code>while (digitalRead(2) == LOW) { }</code> 做什麼?", ["什麼也不做,只是等到按鈕被放開", "讓 LED 閃爍", "讀取兩次"], 0,
   "大括號是空的,迴圈只是一直檢查,直到條件不成立(放開)才往下。"),
])
practice = section("practice", "動手演練與延伸閱讀",
  sim("", "情境:LED 一直亮著,按了也沒反應", "你應該先?",
      [("a1", "重新安裝 IDE"), ("a2", "檢查按鈕是否接在對角兩腳,且有跨在中間凹槽上"), ("a3", "換更大的電阻")]),
  QUIZ_HTML,
  checks(["我知道按鈕沒按是斷開、按下是接通。",
          "我能說出浮接是什麼,以及上拉電阻怎麼解決它。",
          "我知道 <code>INPUT_PULLUP</code> 時,按下是 LOW、放開是 HIGH。",
          "我的按鈕是用對角兩腳接線,並跨在中間凹槽上。",
          "我寫出了「按住才亮」與「按一下切換」兩種程式。",
          "我分得清 <code>=</code> 與 <code>==</code>。",
          "我能解釋什麼是彈跳,以及怎麼簡單處理它。"], "做完之後,對照這張清單"),
  resources([
    ("https://docs.arduino.cc/language-reference/en/functions/digital-io/digitalread/", "digitalRead()", "Arduino language reference"),
    ("https://docs.arduino.cc/language-reference/en/functions/digital-io/pinmode/", "pinMode()(含 INPUT_PULLUP)", "Arduino language reference"),
    ("https://docs.arduino.cc/language-reference/en/structure/control-structure/if/", "if 條件判斷", "Arduino language reference"),
    ("https://docs.arduino.cc/language-reference/en/structure/control-structure/while/", "while 迴圈", "Arduino language reference"),
  ], "Arduino 官方文件"))

SPEC = dict(
    dir="arduino",
    file="arduino-button-guide.html",
    title="按鈕:讀取輸入、上拉電阻與去彈跳",
    eyebrow="第 7 篇 · 按鈕",
    h1="按鈕:讓 Arduino 聽到你的動作",
    sub="第一次做「輸入」:讀按鈕、理解浮接與上拉電阻,寫出按住才亮、按一下切換兩種程式,並處理按鈕的彈跳。",
    tldr="按鈕<strong>一腳接 2 號腳、一腳接 GND</strong>(用<strong>對角</strong>兩腳),程式用 <code>INPUT_PULLUP</code>,<strong>按下讀到 LOW</strong>。<code>if</code> 判斷、<code>==</code> 比較;切換狀態要用變數記住,並用 <code>delay</code> 加 <code>while</code> 處理彈跳。",
    toc=[("what", "輸入與上拉"), ("wire", "接線"), ("fill", "填入等待時間"), ("code", "程式一:按住才亮"), ("code2", "程式二:按一下切換"),
         ("pd", "外接電阻的寫法"), ("try", "改改看"), ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
    body="\n\n".join([what, wire, fillsec, code, code2, pdsec, try_, gotchas, practice]),
    config=dict(fill=FILL, sim=SIM, quiz=QUIZ, wiring=[bb.wiring_config(CIRC)], parts=bb.parts_info(CIRC)),
    prev=("arduino-pwm-guide.html", "PWM 呼吸燈與蜂鳴器"),
    next=("arduino-serial-guide.html", "Serial Monitor 與除錯"),
)
