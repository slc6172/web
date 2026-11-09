# -*- coding: utf-8 -*-
from h import *
import bb

parts = []
steps_ = []
for k, (B, col, pin, sig) in enumerate([(3, "red", "D8", "orange"), (9, "yellow", "D9", "blue"), (15, "green", "D10", "purple")], 1):
    parts += [bb.Resistor("R%d" % k, 220, "b%d" % B, "b%d" % (B + 4), 1),
              bb.LED("LED%d" % k, col, "d%d" % (B + 4), "d%d" % (B + 5), 2),
              bb.Wire("K%d" % k, "a%d" % (B + 5), "t-%d" % (B + 5), "black", 3, route="straight"),
              bb.Wire("S%d" % k, "UNO.%s" % pin, "a%d" % B, sig, 4)]
parts.append(bb.Wire("G", "UNO.GND", "t-22", "black", 5))
CIRC = bb.Circuit(
    "led-chase", 22, parts=parts,
    steps=[
        ("放三顆電阻", "三顆 220Ω 電阻都橫放在 <b>b 列</b>,各跨 4 欄:<code>b3–b7</code>、<code>b9–b13</code>、<code>b15–b19</code>。<br>三組之間各空出一欄,避免腳碰在一起。"),
        ("放三顆 LED", "<strong>長腳(+)</strong>靠左、<strong>短腳(−)</strong>靠右,都在 <b>d 列</b>:紅 <code>d7、d8</code>,黃 <code>d13、d14</code>,綠 <code>d19、d20</code>。<br>每顆 LED 的長腳與自己那顆電阻的右腳同欄(第 7、13、19 欄)。"),
        ("三條黑色短線:LED 負極 → − 軌", "三條黑色短線,一端插 LED 短腳那一欄的 <b>a 列</b>(<code>a8</code>、<code>a14</code>、<code>a20</code>),另一端插上方藍線那排的 <code>t-8</code>、<code>t-14</code>、<code>t-20</code>。<br>三顆 LED 的負極都接到同一條 − 軌,<b>共用 GND</b>。"),
        ("三條訊號線:8、9、10 號腳", "橘線:Uno 8 號腳 → <code>a3</code>;藍線:Uno 9 號腳 → <code>a9</code>;紫線:Uno 10 號腳 → <code>a15</code>。<br>每條線接到自己那顆電阻的左端欄(第 3、9、15 欄)。顏色只是方便你分辨。"),
        ("黑線:Uno GND → − 軌", "黑色杜邦線一端插 Uno 數位腳位排的 <strong>GND</strong>,另一端插 <code>t-22</code>。<br>只要<b>一條線</b>,就能把整條 − 軌接回 Uno 的 GND。"),
    ],
    chains=[["UNO.D8", "R1", "LED1", "UNO.GND"], ["UNO.D9", "R2", "LED2", "UNO.GND"], ["UNO.D10", "R3", "LED3", "UNO.GND"]],
    intro="先<strong>拔掉 USB 線</strong>。這次有三組一模一樣的「電阻 + LED」,分別接到 8、9、10 號腳;三顆 LED 的負極集中接到 − 軌,再用一條線回到 GND。按「下一步」,一次放一種零件。",
    done="三條獨立的路(8、9、10 號腳各一條),最後都回到同一個 GND。檢查:每條路都完整;每顆 LED 長腳朝向電阻。",
)
CIRCUITS = [CIRC]

V1 = """// 第 4 篇(寫法一):三顆燈,每顆都寫一遍
void setup() {
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
}

void loop() {
  digitalWrite(8, HIGH);   // 第一顆亮
  delay({ms});
  digitalWrite(8, LOW);    // 第一顆滅

  digitalWrite(9, HIGH);   // 第二顆亮
  delay({ms});
  digitalWrite(9, LOW);

  digitalWrite(10, HIGH);  // 第三顆亮
  delay({ms});
  digitalWrite(10, LOW);
}
"""
V2 = """// 第 4 篇(寫法二):用變數替腳位取名字
const int RED_PIN = 8;       // 常數:值不會變
const int YELLOW_PIN = 9;
const int GREEN_PIN = 10;
int waitMs = {ms};           // 變數:之後可以改它的值

void setup() {
  pinMode(RED_PIN, OUTPUT);
  pinMode(YELLOW_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
}

void loop() {
  digitalWrite(RED_PIN, HIGH);
  delay(waitMs);
  digitalWrite(RED_PIN, LOW);

  digitalWrite(YELLOW_PIN, HIGH);
  delay(waitMs);
  digitalWrite(YELLOW_PIN, LOW);

  digitalWrite(GREEN_PIN, HIGH);
  delay(waitMs);
  digitalWrite(GREEN_PIN, LOW);
}
"""
V3 = """// 第 4 篇(寫法三):陣列 + for 迴圈
const int ledPins[] = {8, 9, 10};   // 陣列:把三個腳位放在一排
const int LED_COUNT = 3;            // 一共幾顆燈
int waitMs = {ms};

void setup() {
  for (int i = 0; i < LED_COUNT; i++) {
    pinMode(ledPins[i], OUTPUT);    // 對每一顆燈做一次
  }
}

void loop() {
  for (int i = 0; i < LED_COUNT; i++) {
    digitalWrite(ledPins[i], HIGH);  // 第 i 顆亮
    delay(waitMs);
    digitalWrite(ledPins[i], LOW);   // 第 i 顆滅
  }
}
"""
V4 = """// 挑戰:來回跑(像霹靂遊俠的車頭燈)
const int ledPins[] = {8, 9, 10};
const int LED_COUNT = 3;
int waitMs = {ms};

void blinkOne(int i) {               // 自己定義一個函式:亮第 i 顆再熄滅
  digitalWrite(ledPins[i], HIGH);
  delay(waitMs);
  digitalWrite(ledPins[i], LOW);
}

void setup() {
  for (int i = 0; i < LED_COUNT; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
}

void loop() {
  for (int i = 0; i < LED_COUNT; i++) {               // 往右:0 → 1 → 2
    blinkOne(i);
  }
  for (int i = LED_COUNT - 2; i > 0; i--) {           // 往左:1(頭尾不重複)
    blinkOne(i);
  }
}
"""
FILL = dict(ms="300")
chase = dict(kind="chase", seconds=3.5, pins=["D8", "D9", "D10"], ms=300, tol_ms=15)
SKETCHES = [
    dict(name="chase-v1", code=V1, fill=FILL, circuit=CIRC, code_pins={}, sim=chase),
    dict(name="chase-v2", code=V2, fill=FILL, circuit=CIRC, code_pins={"RED_PIN": "UNO.D8", "YELLOW_PIN": "UNO.D9", "GREEN_PIN": "UNO.D10"}, sim=chase),
    dict(name="chase-v3", code=V3, fill=FILL, circuit=CIRC, code_pins={"ledPins": ["UNO.D8", "UNO.D9", "UNO.D10"]}, sim=chase),
    dict(name="chase-v4", code=V4, fill=FILL, circuit=CIRC, code_pins={"ledPins": ["UNO.D8", "UNO.D9", "UNO.D10"]}),
]
I_MA = (bb.UNO_VCC - bb.LED_C["red"][3]) / 220.0 * 1000.0

what = section("what", "三顆燈都想閃:每顆都寫一遍太累了",
  '<p class="sub" style="margin-bottom:14px">上一篇一顆 LED 只要幾行。三顆就要把同樣的事情寫三遍;十顆呢?這一篇學三個工具,讓程式變短、也變好改:</p>',
  table("g3", ["工具", "像什麼", "解決什麼問題"], [
    ["變數與常數", "給一個值取名字,貼在盒子上。", "程式裡到處都是 <code>8</code>、<code>300</code>,看不懂、也不好改。取名字後只改一處。"],
    ["陣列", "一排有編號的盒子。", "三個腳位放在一起管理,不用取三個不同的名字。"],
    ["for 迴圈", "「對每一個,做一次」。", "同樣的動作要重複做,不用複製貼上。"],
  ]),
  tip("這一篇的程式有<b>四個版本</b>(寫法一到三,再加一個挑戰),<b>做出來的效果完全相同</b>。差別只在於程式碼的長短與好不好改,你會親眼看到它們怎麼一步步變短。"))

sch_svg, sch_legend = bb.schematic_svg(CIRC, mark=("gnd",))
wire = section("wire", "接線:三組「電阻 + LED」,共用一條 GND",
  '<p class="sub" style="margin-bottom:14px">每一組的接法和上一篇完全一樣(訊號腳 → 電阻 → LED → GND),只是做三次。新的做法是:<b>三顆 LED 的負極都接到同一條電源軌</b>,再用一條線回到 Uno 的 GND,不必拉三條。</p>',
  bb.stepper_html(CIRC),
  '<p class="sk">圖只畫左邊 22 欄,你的麵包板更長,以欄號與 a–j 為準(手機上可以左右滑動圖)。如果你的麵包板電源軌中間是斷開的(第 2 篇),黑色短線與 GND 線要接在<b>同一半</b>:上面圖中 <code>t-8</code>、<code>t-14</code>、<code>t-20</code>、<code>t-22</code> 都在同一條軌上,請確認它們彼此相通。</p>',
  '<h3 style="margin-top:26px">接線表</h3>', bb.wiring_table(CIRC),
  warn("先拔 USB,先接麵包板上的零件,最後才接 Uno 的線。三顆 LED 的<b>長腳都朝左</b>(靠近電阻那側),很容易有一顆插反。"),
  '<h3 style="margin-top:26px">原理圖:三個 GND 符號,是同一個 GND</h3>',
  canvas(sch_svg, [(n, '<span class="newsym">新觀念</span>' + t) for n, t in sch_legend]),
  '<div class="linkbox" id="linkInfo" style="margin-top:12px">點原理圖裡的零件,看它在麵包板上是哪一個。</div>',
  '<p style="margin-top:14px">在原理圖上,三條路各畫一個 GND 符號,但那只是為了圖好畫。<b>圖上每一個 GND 符號都是同一個點</b>,對應到麵包板上就是那條共用的 − 軌。</p>')

fillsec = section("fill", "先填入你想要的速度",
  fill([("ms", "每顆燈亮的時間(毫秒)", True)]),
  '<p class="sk">空白時用範例值 300 毫秒,三顆跑一輪是 0.9 秒。填大一點會變慢,填小一點會變快。</p>')

def exp(items):
    return table("g2", ["這一行", "它在做什麼"], items)

code = section("code", "四個版本的程式,效果完全相同",
  '<h3>寫法一:最直接,但很長</h3>',
  cmd(V1, cap="寫法一:每顆燈都寫一遍", cpp=True),
  '<p>能動,但每多一顆燈就要複製三行。而且腳位數字 <code>8</code>、<code>9</code>、<code>10</code> 散在好幾處,想換腳位要一個一個改,很容易漏。</p>',
  '<h3 style="margin-top:28px">寫法二:用變數替腳位取名字</h3>',
  cmd(V2, cap="寫法二:變數與常數", cpp=True),
  exp([
    ["<code>const int RED_PIN = 8;</code>", "宣告<b>常數</b>:<code>int</code> 是型態(整數),<code>RED_PIN</code> 是名字,<code>8</code> 是值。<code>const</code> 表示它不會被改。之後用 <code>RED_PIN</code> 就等於用 8。"],
    ["<code>int waitMs = 300;</code>", "宣告<b>變數</b>(沒有 <code>const</code>):值可以在程式裡被改。這裡存「每顆燈亮多久」。"],
    ["<code>delay(waitMs);</code>", "用變數代替數字。想調速度,只改最上面那一行。"],
  ]),
  tip("取名字的規則:用<b>英文字母開頭</b>,只用英文、數字與底線 <code>_</code>,<b>不能有空格</b>,而且<b>大小寫不同就是不同名字</b>(<code>waitMs</code> 與 <code>waitms</code> 是兩個東西)。"),
  '<h3 style="margin-top:28px">寫法三:陣列 + for 迴圈</h3>',
  cmd(V3, cap="寫法三:陣列與 for 迴圈", cpp=True),
  exp([
    ["<code>const int ledPins[] = {8, 9, 10};</code>", "<b>陣列</b>:一排有編號的盒子。方括號 <code>[]</code> 表示這是陣列,大括號裡是內容。"],
    ["<code>ledPins[0]</code>、<code>ledPins[1]</code>、<code>ledPins[2]</code>", "取出第幾格的值。<b>編號從 0 開始</b>:<code>ledPins[0]</code> 是 8,<code>ledPins[1]</code> 是 9,<code>ledPins[2]</code> 是 10。"],
    ["<code>for (int i = 0; i &lt; LED_COUNT; i++) { … }</code>", "<b>for 迴圈</b>:把大括號裡的事重複做。括號裡三段用分號隔開,見下表。"],
    ["<code>ledPins[i]</code>", "每一圈 <code>i</code> 不同,取到的腳位就不同。同一行程式,三顆燈各做一次。"],
  ]),
  '<h3 style="margin-top:22px">for 括號裡的三段</h3>',
  table("g3", ["寫法", "意思", "什麼時候做"], [
    ["<code>int i = 0</code>", "<b>起點</b>:建立計數器 <code>i</code>,從 0 開始。", "進迴圈前,只做一次"],
    ["<code>i &lt; LED_COUNT</code>", "<b>條件</b>:<code>i</code> 小於 3 才繼續。", "每一圈開始前檢查,不成立就結束"],
    ["<code>i++</code>", "<b>每圈做完</b>:<code>i</code> 加 1(等於 <code>i = i + 1</code>)。", "每一圈結束時"],
  ]),
  '<h3 style="margin-top:22px">跑一遍會怎樣(LED_COUNT = 3)</h3>',
  table("g3", ["第幾圈", "i 的值與腳位", "動作"], [
    ["第 1 圈", "<code>i = 0</code> → <code>ledPins[0]</code> = 8", "紅燈亮、等待、熄滅"],
    ["第 2 圈", "<code>i = 1</code> → <code>ledPins[1]</code> = 9", "黃燈亮、等待、熄滅"],
    ["第 3 圈", "<code>i = 2</code> → <code>ledPins[2]</code> = 10", "綠燈亮、等待、熄滅"],
    ["結束", "<code>i = 3</code>,條件 3 &lt; 3 不成立", "離開迴圈;<code>loop()</code> 從頭再來"],
  ]),
  see("三顆燈<b>由左到右依序亮起</b>,一次只亮一顆,一輪 0.9 秒,不斷重複。紅 → 黃 → 綠 → 紅 …"),
  tip("三個版本會做出一模一樣的效果。要多一顆燈,寫法三只需要加一個腳位到陣列、並把 <code>LED_COUNT</code> 改成 4;寫法一要再複製三行,還得記得 <code>setup()</code> 也要加。"))

try_ = section("try", "改改看",
  table("g3", ["挑戰", "怎麼改", "你會看到"], [
    ["調速度", "把上面「每顆燈亮的時間」改成 100,再改成 1000", "100:很快地連續跑;1000:很慢,每顆燈亮 1 秒。"],
    ["反方向", "寫法三的陣列改成 <code>{10, 9, 8}</code>", "由右到左跑。程式只改一處,接線完全不動。"],
    ["來回跑", "改用下面的「來回跑」程式", "紅 → 黃 → 綠 → 黃 → 紅 …,像車頭燈左右掃動。"],
  ]),
  details("來回跑的程式與說明",
    cmd(V4, cap="挑戰:來回跑", cpp=True) +
    exp([
      ["<code>void blinkOne(int i) { … }</code>", "<b>自己定義的函式</b>:把「亮第 i 顆再熄滅」這件事取名叫 <code>blinkOne</code>。括號裡的 <code>int i</code> 是它收到的資料(第幾顆)。"],
      ["<code>blinkOne(i);</code>", "呼叫它。要做這件事就寫名字,不用重寫三行。"],
      ["<code>for (int i = LED_COUNT - 2; i &gt; 0; i--)</code>", "從倒數第二顆往回數到第 1 顆(<code>i--</code> 是每圈減 1),頭尾那兩顆不重複亮,動作才順。"],
    ])))

gotchas = section("gotchas", "常見卡關",
  details("只有某一顆燈不亮,另外兩顆正常",
    "<p>程式對三顆燈是一樣的做法,所以問題幾乎一定在那一列的接線。依序檢查那一組:</p>" +
    ops(["LED 的<b>長腳在不在靠電阻的那一側</b>(插反最常見)。", "電阻右腳與 LED 長腳是否在<b>同一欄</b>。", "LED 短腳那一欄的黑色短線,是否真的接到 − 軌。", "訊號線是否插在<b>正確的腳位</b>(8、9、10),且插在電阻左端那一欄。"]), True) +
  details("三顆燈全不亮",
    "<p>先檢查共用的部分:Uno 的 GND 線有沒有接到 − 軌、− 軌有沒有中間斷開、USB 有沒有接上、程式有沒有成功上傳。三條路共用同一條 GND,這條線沒接就全部不亮。</p>") +
  details("燈亮的順序和我想的不一樣",
    "<p>順序由陣列決定:<code>{8, 9, 10}</code> 是先 8、再 9、再 10。如果實際位置的順序不同,檢查哪條訊號線接到哪一組,或直接調整陣列裡數字的順序。</p>") +
  details("迴圈寫成 <code>i &lt;= LED_COUNT</code>,結果怪怪的",
    "<p><code>i &lt;= 3</code> 會多跑一圈,取到 <code>ledPins[3]</code>。但陣列只有 0、1、2 三格,第 3 格不存在,Arduino <b>不會報錯</b>,而是讀到記憶體裡的別的東西,可能去控制一個你沒接任何東西的腳位。記住:<b>n 個元素,編號是 0 到 n−1</b>,條件寫 <code>i &lt; n</code>。</p>") +
  details("驗證出現紅字錯誤",
    "<p>新手最常見:陣列漏了 <code>[]</code>、大括號 <code>{ }</code> 沒成對、<code>for</code> 括號裡的分號寫成逗號、少了結尾分號。IDE 會指出行號,從那一行與上一行找起。</p>"))

SIM = {
  "a1": "<b>不用。</b>三顆燈共用同一段程式,另外兩顆正常,表示程式沒有問題。重寫只會浪費時間。",
  "a2": "<b>對。</b>程式一視同仁,異常只出現在黃色那一列,就只查那一列:LED 方向、電阻與 LED 是否同欄、黑色短線是否接到 − 軌、訊號線是否插在 9 號腳。",
  "a3": "<b>沒有用。</b>USB 線影響的是整塊板子,不會只讓其中一顆 LED 不亮。",
}
QUIZ = quiz_cfg([
  ("<code>const int ledPins[] = {8, 9, 10};</code>,<code>ledPins[1]</code> 是多少?", ["8", "9", "10"], 1,
   "編號從 0 開始:[0] 是 8,[1] 是 9,[2] 是 10。"),
  ("<code>for (int i = 0; i &lt; 3; i++)</code> 會執行幾圈?", ["2 圈", "3 圈", "4 圈"], 1,
   "i 依序是 0、1、2,到 3 時條件不成立,共 3 圈。"),
  ("陣列有 3 個元素,取 <code>ledPins[3]</code> 會怎樣?", ["取到第三個元素", "超出範圍,讀到不屬於陣列的記憶體,且 Arduino 不會警告你", "自動回到第一個元素"], 1,
   "有效編號只有 0、1、2。超出範圍是常見的錯誤。"),
  ("<code>const</code> 的意思是?", ["這個值之後不會被改變", "這個值一定是 0", "這個變數是陣列"], 0,
   "const 表示常數,宣告之後不能再改。"),
  ("為什麼原理圖上有三個 GND 符號,卻只接一條線回 Uno 的 GND?", ["三個 GND 是三個不同的點", "圖上每個 GND 符號都是同一個點,對應麵包板上共用的 − 軌", "其實需要三條線,只是省略不畫"], 1,
   "GND 符號代表「接到同一個 0 V」。畫三個只是為了圖好畫。"),
])
practice = section("practice", "動手演練與延伸閱讀",
  sim("", "情境:三顆燈只有黃色那顆不亮", "你應該先?",
      [("a1", "整個程式重寫一遍"), ("a2", "只檢查黃色那一列的接線"), ("a3", "換一條 USB 線")]),
  QUIZ_HTML,
  checks(["三顆 LED 的長腳都在靠電阻那一側。",
          "我知道三顆 LED 的負極共用一條 − 軌,再用一條線回 GND。",
          "我能說出變數、陣列、for 迴圈各解決什麼問題。",
          "我知道陣列編號從 0 開始,條件要寫 <code>i &lt; 數量</code>。",
          "我完成了寫法一到三,並確認效果相同。",
          "我看得懂原理圖上多個 GND 符號代表同一點。"], "做完之後,對照這張清單"),
  resources([
    ("https://docs.arduino.cc/language-reference/en/structure/control-structure/for/", "for 迴圈", "Arduino language reference"),
    ("https://docs.arduino.cc/language-reference/en/variables/data-types/array/", "陣列 array", "Arduino language reference"),
    ("https://docs.arduino.cc/language-reference/en/functions/digital-io/digitalwrite/", "digitalWrite()", "Arduino language reference"),
  ], "Arduino 官方文件"))

SPEC = dict(
    dir="arduino",
    file="arduino-loop-guide.html",
    title="變數、for 與陣列:三顆 LED 跑馬燈",
    eyebrow="第 4 篇 · 跑馬燈",
    h1="接三顆 LED,用變數、陣列和 for 讓程式變短",
    sub="三組一模一樣的電路,先用最笨的寫法讓它動,再一步步改成變數、陣列加 for 迴圈。效果相同,程式越來越短、越好改。",
    tldr="三顆 LED 的負極共用一條 − 軌,正極各經過 220Ω 電阻接到 8、9、10 號腳。程式寫三次:<strong>直接寫、用變數命名、陣列加 for</strong>。陣列編號<strong>從 0 開始</strong>,迴圈條件寫 <code>i &lt; 數量</code>。",
    toc=[("what", "為什麼要學"), ("wire", "接線"), ("fill", "填入速度"), ("code", "四個版本程式"), ("try", "改改看"), ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
    body="\n\n".join([what, wire, fillsec, code, try_, gotchas, practice]),
    config=dict(fill=FILL, sim=SIM, quiz=QUIZ, wiring=[bb.wiring_config(CIRC)], parts=bb.parts_info(CIRC)),
    prev=("arduino-led-guide.html", "外接 LED 閃爍:第一次接線"),
    next=("arduino-schematic-guide.html", "讀懂電路圖"),
)
