# -*- coding: utf-8 -*-
from h import *
import bb, a14

parts = [bb.Shift595("IC1", 5, 1)]
colors = ["red", "yellow", "green", "blue"]
qcol = [8, 7, 6, 5]                 # LED1..LED4 接 Q4、Q3、Q2、Q1(下排腳位所在的欄)
bases = [14, 20, 26, 32]
for i in range(4):
    c = bases[i]
    parts += [bb.Resistor("R%d" % (i + 1), 220, "h%d" % c, "h%d" % (c + 4), 2), bb.LED("LED%d" % (i + 1), colors[i], "i%d" % (c + 4), "i%d" % (c + 5), 2),
              bb.Wire("K%d" % (i + 1), "j%d" % (c + 5), "b-%d" % (c + 5), "black", 3, route="straight"),
              bb.Wire("Q%d" % (4 - i), "j%d" % qcol[i], "j%d" % c, ["orange", "blue", "green", "purple"][i], 4, route="down%d" % i if i else "down")]
parts += [bb.Wire("P5", "a5", "t+5", "red", 3, route="straight"), bb.Wire("P11", "a11", "t+11", "red", 3, route="straight"),
          bb.Wire("G8", "a8", "t-8", "black", 3, route="straight"), bb.Wire("G12", "j12", "b-12", "black", 3, route="straight"),
          bb.Wire("L", "t-38", "b-38", "green", 3, route="straight"),
          bb.Wire("SER", "UNO.D11", "a7", "blue", 5), bb.Wire("RCLK", "UNO.D12", "a9", "green", 5), bb.Wire("SCK", "UNO.D13", "a10", "yellow", 5),
          bb.Wire("V5", "UNO.5V", "t+1", "red", 6, route="left"), bb.Wire("G", "UNO.GND", "t-34", "black", 6)]
CIRC = bb.Circuit(
    "spi-595", 40, parts=parts,
    steps=[
        ("放 74HC595 晶片", "晶片<b>跨在中間凹槽上</b>,<b>缺口(小圓弧)朝左</b>。上排八隻腳插 <code>e5</code>–<code>e12</code>,下排八隻腳插 <code>f5</code>–<code>f12</code>。<br>腳多又細,<b>垂直、對準孔位再慢慢壓下去</b>,不要用力斜插。左下角那隻是 1 號腳。"),
        ("放四組電阻與 LED", "四組都在<b>下半部</b>:電阻橫放 <code>h14–h18</code>、<code>h20–h24</code>、<code>h26–h30</code>、<code>h32–h36</code>;LED 長腳(+)靠左,分別插 <code>i18/i19</code>、<code>i24/i25</code>、<code>i30/i31</code>、<code>i36/i37</code>(紅、黃、綠、藍)。"),
        ("短線:電源、接地與 LED 負極", "① 紅 <code>a5</code> → <code>t+5</code>:16 腳 VCC 接 5V。② 紅 <code>a11</code> → <code>t+11</code>:10 腳 SRCLR 接 5V(不清除)。<br>③ 黑 <code>a8</code> → <code>t-8</code>:13 腳 OE 接 GND(輸出永遠啟用)。④ 黑 <code>j12</code> → <code>b-12</code>:8 腳 GND 接下方 − 軌。<br>⑤ 四條黑線:<code>j19</code>、<code>j25</code>、<code>j31</code>、<code>j37</code> → <code>b-19</code>、<code>b-25</code>、<code>b-31</code>、<code>b-37</code>:LED 負極接 − 軌。<br>⑥ 綠線 <code>t-38</code> → <code>b-38</code>:上下 − 軌連起來。"),
        ("四條輸出線:晶片輸出 → 各組電阻", "晶片下排的四個輸出,各用一條線(從下方繞過去)接到一組電阻的左端:<br><code>j8</code>(Q4)→ <code>j14</code>、<code>j7</code>(Q3)→ <code>j20</code>、<code>j6</code>(Q2)→ <code>j26</code>、<code>j5</code>(Q1)→ <code>j32</code>。<br>線一條套著一條,<b>不會交叉</b>:最左邊的燈接最右邊的輸出腳是故意的,為了讓線不打結。"),
        ("三條控制線:Uno 11、12、13 號腳", "藍線:Uno <b>11 號腳(MOSI)</b> → <code>a7</code>(14 腳 SER,資料)。<br>綠線:Uno <b>12 號腳</b> → <code>a9</code>(12 腳 RCLK,鎖存)。<br>黃線:Uno <b>13 號腳(SCK)</b> → <code>a10</code>(11 腳 SRCLK,時脈)。"),
        ("電源線:5V 與 GND", "紅線:Uno <b>5V</b> → <code>t+1</code>。黑線:Uno 數位腳位排的 <b>GND</b> → <code>t-34</code>。"),
    ],
    chains=[["UNO.5V", "IC1.VCC"], ["UNO.5V", "IC1.SRCLR"], ["IC1.OE", "UNO.GND"], ["IC1.GND", "UNO.GND"],
            ["UNO.D11", "IC1.SER"], ["UNO.D12", "IC1.RCLK"], ["UNO.D13", "IC1.SRCLK"],
            ["IC1.Q4", "R1", "LED1", "UNO.GND"], ["IC1.Q3", "R2", "LED2", "UNO.GND"], ["IC1.Q2", "R3", "LED3", "UNO.GND"], ["IC1.Q1", "R4", "LED4", "UNO.GND"]],
    intro="先<strong>拔掉 USB 線</strong>。這是目前最複雜的接線,<b>請一步一步照著做,每一步做完對照圖檢查</b>。74HC595 讓你用 <b>3 條線(資料、時脈、鎖存)控制 8 個輸出</b>;這裡接其中 4 個輸出到 4 顆 LED。",
    done="晶片:16 腳 5V、8 腳 GND、10 腳 5V、13 腳 GND;11、12、14 腳分別接 Uno 的 13、12、11 號腳;四個輸出 Q4、Q3、Q2、Q1 各經 220Ω 接一顆 LED。檢查:<b>缺口朝左</b>,16 腳(左上)是 5V。",
)
CIRCUITS = [CIRC]

SCAN = """// 第 17 篇:I2C 掃描器——找出匯流排上所有裝置的位址
#include <Wire.h>

void setup() {
  Serial.begin(9600);
  Wire.begin();                              // 啟動 I2C(Uno 是主控端)
  Serial.println("I2C scanner");
}

void loop() {
  int found = 0;
  for (byte address = 1; address < 127; address++) {   // I2C 位址是 7 位元:1 到 126
    Wire.beginTransmission(address);         // 試著叫這個位址
    byte error = Wire.endTransmission();     // 結束,並取得結果:0 表示有人回應
    if (error == 0) {
      Serial.print("Found device at 0x");
      if (address < 16) {
        Serial.print("0");                   // 補一個 0,讓格式整齊
      }
      Serial.println(address, HEX);
      found++;
    }
  }
  if (found == 0) {
    Serial.println("No I2C device found");
  }
  Serial.println("--- scan done ---");
  delay({gap});
}
"""
SPI1 = """// 第 17 篇:用 SPI 控制 74HC595,讓 4 顆 LED 由左到右依序亮
#include <SPI.h>                    // SPI 函式庫(內建)

const int LATCH_PIN = 12;           // 接 74HC595 的 RCLK(鎖存)
const byte patterns[] = {           // 每個位元組的每一個位元,對應一個輸出腳的亮 / 滅
  0b00010000,                       // 只有 Q4 亮 → 最左邊的 LED1
  0b00001000,                       // 只有 Q3 亮 → LED2
  0b00000100,                       // 只有 Q2 亮 → LED3
  0b00000010                        // 只有 Q1 亮 → LED4
};

void setup() {
  pinMode(LATCH_PIN, OUTPUT);
  SPI.begin();                      // 啟動 SPI(11 號腳 MOSI、13 號腳 SCK 由函式庫接管)
}

void loop() {
  for (int i = 0; i < 4; i++) {
    digitalWrite(LATCH_PIN, LOW);   // 鎖存腳先拉低:準備送資料
    SPI.transfer(patterns[i]);      // 送出 1 個位元組(8 個位元),晶片依序把它們移進去
    digitalWrite(LATCH_PIN, HIGH);  // 鎖存腳拉高:晶片把剛移進去的 8 個位元,一次推到輸出腳
    delay({step});
  }
}
"""
FILL = dict(gap="2000", step="300")
SKETCHES = [
    dict(name="i2c-scan", code=SCAN, fill=FILL, libs=["Wire"],
         sim=dict(kind="uart", seconds=1.2, i2c=[0x27, 0x3C], expect=["Found device at 0x27\r\n", "Found device at 0x3C\r\n", "--- scan done ---\r\n"])),
    dict(name="i2c-none", code=SCAN, fill=FILL, libs=["Wire"], sim=dict(kind="uart", seconds=1.2, expect=["No I2C device found\r\n", "--- scan done ---\r\n"])),
    dict(name="spi-chase", code=SPI1, fill=FILL, circuit=CIRC, code_pins={"LATCH_PIN": "UNO.D12"}, libs=["SPI"],
         sim=dict(kind="spi", seconds=1.4, latch="D12", expect=[16, 8, 4, 2], period_ms=300, tol_ms=3)),
]

bitsim = ('<div class="panel" data-bitsim><div class="wgrid f2"><div><label>送出的位元組(0–255)</label><input data-bs8="n" value="16" inputmode="numeric" autocomplete="off"></div><div></div></div>'
          '<div class="bits">' + "".join('<button type="button" class="bitc" data-b="%d">Q%d<small>1 / 0</small></button>' % (b, b) for b in range(7, -1, -1)) + '</div>'
          '<div class="rc-out bits-out" aria-live="polite"></div></div>')

def pin_table():
    rows = [["1", "Q1", "輸出(LED4)"], ["2", "Q2", "輸出(LED3)"], ["3", "Q3", "輸出(LED2)"], ["4", "Q4", "輸出(LED1)"], ["5–7", "Q5–Q7", "輸出(本篇不用)"], ["8", "GND", "接地"],
            ["9", "Q7'", "串接下一顆用(不用)"], ["10", "SRCLR", "清除(低電位清除)→ 接 5V,不清除"], ["11", "SRCLK", "移位時脈 ← Uno 13 號腳(SCK)"], ["12", "RCLK", "鎖存 ← Uno 12 號腳"],
            ["13", "OE", "輸出啟用(低電位啟用)→ 接 GND,永遠啟用"], ["14", "SER", "資料 ← Uno 11 號腳(MOSI)"], ["15", "Q0", "輸出(本篇不用)"], ["16", "VCC", "電源 → 5V"]]
    return table("g3", ["腳號", "名稱", "怎麼接 / 用途"], rows)

what = section("what", "兩種「用少少的線,溝通很多東西」的方法",
  '<p class="sub" style="margin-bottom:14px">Uno 的腳位不多。如果每一顆 LED、每一個感測器都占一個腳位,很快就不夠用。<b>通訊協定</b>讓你用幾條共用的線,跟很多裝置溝通。第 14 篇的 LCD 用了 I2C,這一篇再認識 SPI。</p>',
  table("g3", ["", "I2C", "SPI"], [
    ["線數", "<b>2 條</b>:SDA(資料)、SCL(時脈)", "<b>3 條 + 每個裝置 1 條選擇線</b>:MOSI(出)、MISO(入)、SCK(時脈)、SS"],
    ["怎麼找到裝置", "每個裝置有<b>位址</b>(例如 0x27),主控端依位址叫人", "用<b>選擇線(SS / 鎖存)</b>叫誰,沒有位址"],
    ["速度", "較慢(常見 100–400 kHz)", "快(可到數 MHz)"],
    ["Uno 上的腳位", "<b>A4 = SDA、A5 = SCL</b>", "<b>11 = MOSI、12 = MISO、13 = SCK、10 = SS</b>"],
    ["常見裝置", "LCD、OLED、許多感測器", "74HC595、SD 卡、LED 矩陣、無線模組"],
  ]),
  tip("這一篇是<b>進階選讀</b>。你不一定會用到,但<b>看得懂這兩種協定</b>,以後遇到新的模組(「它是 I2C 還是 SPI?」)就知道怎麼接、怎麼找函式庫。"))

i2c = section("i2c", "I2C:用位址找到裝置,並寫一個掃描器",
  '<p class="sub" style="margin-bottom:14px">I2C 匯流排上每個裝置都有一個 7 位元的<b>位址</b>。LCD 轉接板常見的位址是 <code>0x27</code> 或 <code>0x3F</code>。<b>不知道裝置位址時,最直接的辦法是掃描:把 1 到 126 的位址都「敲門」一次,有人回應的就是裝置。</b></p>',
  '<p>接線沿用第 14 篇的 LCD(只要接著 Uno 的 SDA、SCL、5V、GND 就好):</p>',
  canvas(bb.breadboard_svg(a14.CIRC).replace(' data-part=', ' data-ref='), []),
  cmd(SCAN, cap="I2C 掃描器", cpp=True),
  table("g2", ["這一行", "它在做什麼"], [
    ["<code>Wire.begin();</code>", "啟動 I2C,Uno 擔任<b>主控端</b>(負責發起溝通)。"],
    ["<code>Wire.beginTransmission(address);</code>", "準備對這個位址的裝置說話,也就是「敲門」。"],
    ["<code>Wire.endTransmission();</code>", "結束並<b>真的送出去</b>。回傳 <b>0 表示對方有回應(ACK)</b>,其他數字表示沒人理(或出錯)。"],
    ["<code>Serial.println(address, HEX);</code>", "以十六進位印出位址(第 8 篇學過)。<code>0x27</code> 的 <code>0x</code> 只是標示這是十六進位。"],
  ]),
  see("Serial Monitor(baud 9600)印出 <code>Found device at 0x27</code>(你的轉接板可能是 <code>0x3F</code>)。沒接任何 I2C 裝置時,印 <code>No I2C device found</code>。"),
  tip("如果之後用「LiquidCrystal I2C」函式庫,<code>LiquidCrystal_I2C lcd(0x27, 16, 2);</code> 裡的位址就填掃描出來的數字。第 14 篇用的 <b>hd44780</b> 函式庫會自己做這件事。"))

spi = section("spi", "SPI:用 3 條線控制 8 個輸出(74HC595)",
  '<div class="panel"><h3>74HC595 在做什麼</h3>'
  '<p>74HC595 是<b>移位暫存器</b>:有一排 8 個「抽屜」(Q0–Q7)。你用 <b>SER 線一個位元一個位元把資料送進去</b>,每送一個位元,SRCLK(時脈)就「敲」一下,所有資料往下移一格。<b>送滿 8 個位元後,RCLK(鎖存)敲一下,8 個位元同時出現在 8 個輸出腳</b>。</p>'
  '<p style="margin-bottom:0">Uno 的 SPI 硬體會自動做送位元與敲時脈這些事,你只要<code>SPI.transfer(一個位元組)</code>。一個位元組有 8 個位元,剛好對應 8 個輸出。</p></div>',
  '<h3 style="margin-top:26px">位元組與輸出:拖拖看</h3>',
  '<p>點下面的格子(或輸入數字),看一個位元組的 8 個位元,對應 Q0–Q7 哪幾個輸出是亮的(1)或滅的(0):</p>', bitsim,
  '<h3 style="margin-top:26px">74HC595 的 16 隻腳</h3>', pin_table())

wire = section("wire", "接線:74HC595 加四顆 LED(最複雜的一次)",
  '<p class="sub" style="margin-bottom:14px">腳位多,但每一步都很單純。<b>一步做完,對照圖與接線表檢查一次,再做下一步。</b>圖很寬,手機上可以左右滑動;也可以先看接線表。</p>',
  bb.stepper_html(CIRC),
  '<p class="sk">圖只畫左邊 40 欄,Uno 轉了 180 度擺放。晶片、電阻、LED 的位置依你手上的實物微調即可,<b>以欄號、列號與接線表為準</b>。</p>',
  '<h3 style="margin-top:26px">接線表</h3>', bb.wiring_table(CIRC),
  warn("<b>缺口朝左,16 腳(左上角)接 5V、8 腳(右下角)接 GND。</b>晶片放反(缺口朝右)會讓電源接到錯的腳,可能立刻損壞。接線前先拔 USB;通電後如果晶片發燙,立刻拔掉。", "注意"),
  '<div class="linkbox" id="linkInfo" style="margin-top:12px">點圖上的晶片、電阻或 LED,看它在其他圖的位置。</div>')

fillsec = section("fill", "先填入你的數值",
  fill([("gap", "I2C 掃描:每次掃描之間等待(毫秒)", True), ("step", "SPI 跑馬燈:每顆燈亮多久(毫秒)", True)]),
  '<p class="sk">空白時用範例值:2000 毫秒、300 毫秒。</p>')

code = section("code", "程式:SPI 跑馬燈",
  cmd(SPI1, cap="SPI 控制 74HC595,4 顆 LED 由左到右", cpp=True),
  table("g2", ["這一行", "它在做什麼"], [
    ["<code>#include &lt;SPI.h&gt;</code>", "SPI 函式庫(Arduino 內建)。"],
    ["<code>0b00010000</code>", "<b>二進位寫法</b>:<code>0b</code> 開頭,後面是 8 個位元。只有 Q4 那個位元是 1,所以只有 Q4 輸出 HIGH,LED1 亮。"],
    ["<code>SPI.begin();</code>", "啟動 SPI。11 號腳(MOSI)與 13 號腳(SCK)從此由 SPI 硬體控制。"],
    ["<code>digitalWrite(LATCH_PIN, LOW);</code>", "鎖存腳拉低:<b>準備接收新資料</b>。"],
    ["<code>SPI.transfer(patterns[i]);</code>", "送出 1 個位元組。8 個位元依序移進晶片(<b>最高位元先送</b>,最後落在 Q7)。"],
    ["<code>digitalWrite(LATCH_PIN, HIGH);</code>", "鎖存腳拉高:<b>8 個位元一次推到輸出腳</b>,LED 才會變化。少了這行,資料只留在晶片裡面、輸出不變。"],
  ]),
  see("四顆 LED <b>由左到右依序亮起</b>(紅 → 黃 → 綠 → 藍),一次只亮一顆,不斷重複。"),
  tip("一個位元組控制 8 個輸出。想讓兩顆同時亮,把對應的位元都設成 1:例如 <code>0b00011000</code> 讓 LED1 與 LED2 一起亮。想接 8 顆 LED,就接滿 Q0–Q7(也可以串接多顆 74HC595,控制幾十個輸出,只用同樣 3 條線)。"))

try_ = section("try", "改改看",
  table("g3", ["挑戰", "怎麼改", "你會看到"], [
    ["四顆全亮", "把 <code>patterns</code> 改成 <code>{0b00011110}</code>(只放一個元素,<code>for</code> 的 4 也改 1)", "四顆 LED 同時亮。"],
    ["來回跑", "<code>patterns</code> 改成 <code>{16, 8, 4, 2, 4, 8}</code>,<code>for</code> 改成 6", "紅 → 黃 → 綠 → 藍 → 綠 → 黃 …"],
    ["用二進位算亮度", "對照上面的互動:換成你想要的位元組", "自己設計任意圖案。"],
  ]))

gotchas = section("gotchas", "常見卡關",
  details("四顆 LED 都不亮",
    ops(["<b>晶片方向</b>:缺口朝左,16 腳接 5V。", "<b>OE(13 腳)必須接 GND</b>:接到 5V 會停用輸出。", "<b>SRCLR(10 腳)必須接 5V</b>:接到 GND 會一直清除。", "VCC、GND 是否接好;<code>b-12</code> 的 GND 線是否真的接到。", "程式有沒有上傳成功,<code>LATCH_PIN</code> 是 12。"]), True) +
  details("燈亮了,但順序亂掉或亮到別顆",
    ops(["輸出線(<code>j8→j14</code> 等)有沒有接到對的欄。", "資料(14 腳)與時脈(11 腳)是不是接反:SER 接 11 號腳、SRCLK 接 13 號腳。", "LED 方向、電阻是否在同一欄。"])) +
  details("燈一直閃、或亮一些怪圖案",
    "<p>鎖存(12 腳)沒接好,或 <code>LATCH_PIN</code> 與接線不一致。也可能是接觸不良,把杜邦線與晶片的腳重新壓緊。</p>") +
  details("掃描器找不到 LCD",
    ops(["LCD 的四條線(第 14 篇)有沒有接對:SDA、SCL 不要接反。", "VCC 要接 5V。", "找不到位址不代表壞掉,先檢查杜邦線有沒有接觸不良。"])) +
  details("編譯錯誤:找不到 SPI.h 或 Wire.h",
    "<p>這兩個都是內建函式庫。確認板子選的是 <b>Arduino Uno</b>。仍然找不到就重新安裝 IDE。</p>"))

SIM = {
  "a1": "<b>不用。</b>四顆都不亮,最常見的是晶片方向或 OE、SRCLR 的接法,不是 IDE 的問題。",
  "a2": "<b>對。</b>先看晶片方向與 16、8 腳的電源;再看 OE(13 腳)是否接 GND、SRCLR(10 腳)是否接 5V;最後確認三條控制線(11、12、13)與程式一致。",
  "a3": "<b>沒有用。</b>LED 的電阻不是這個症狀的原因。",
}
QUIZ = quiz_cfg([
  ("I2C 使用哪兩條線?", ["SDA 與 SCL", "MOSI 與 MISO", "TX 與 RX"], 0, "SDA 傳資料,SCL 是時脈。"),
  ("I2C 掃描器 <code>endTransmission()</code> 回傳 0 代表?", ["對方有回應", "沒人回應", "線斷了"], 0, "0 表示成功送出且對方 ACK。"),
  ("SPI 與 I2C 的主要差別?", ["SPI 沒有位址,用選擇線叫人;I2C 靠位址", "SPI 比較慢", "I2C 需要 4 條以上的線"], 0, "SPI 用選擇線(SS / 鎖存),I2C 用位址。"),
  ("74HC595 要讓 8 個位元同時出現在輸出腳,要做什麼?", ["把 RCLK(鎖存)拉高一下", "把 OE 拉高", "把 SRCLR 拉低"], 0, "鎖存把移進去的資料一次推到輸出。"),
  ("<code>0b00001000</code> 會讓哪個輸出變成 HIGH?", ["Q3", "Q8", "Q0"], 0, "由右到左:第 0 位元是 Q0,這個 1 在第 3 位元,所以是 Q3。"),
])
practice = section("practice", "動手演練與延伸閱讀",
  sim("", "情境:74HC595 接好了,四顆 LED 一顆都不亮", "你應該先?",
      [("a1", "重新安裝 IDE"), ("a2", "檢查晶片方向、16 與 8 腳電源、OE 接 GND、SRCLR 接 5V"), ("a3", "換更大的電阻")]),
  QUIZ_HTML,
  checks(["我能說出 I2C 與 SPI 各用幾條線、怎麼找到裝置。",
          "我會用 I2C 掃描器找出裝置位址。",
          "我知道 74HC595:資料進去、時脈移位、鎖存輸出。",
          "我的晶片方向正確(缺口朝左),四顆 LED 依序亮起。",
          "我知道一個位元組的 8 個位元對應 8 個輸出,會用 <code>0b…</code> 寫位元組。",
          "我知道 SPI 的腳位:11 = MOSI、13 = SCK,10 = SS。"], "做完之後,對照這張清單"),
  resources([
    ("https://docs.arduino.cc/language-reference/en/functions/communication/wire/", "Wire(I2C)", "Arduino language reference"),
    ("https://docs.arduino.cc/language-reference/en/functions/communication/SPI/", "SPI", "Arduino language reference"),
    ("https://docs.arduino.cc/tutorials/communication/guide-to-shift-out/", "移位暫存器入門(shiftOut)", "A guide to shiftOut"),
  ], "Arduino 官方文件"))

SPEC = dict(
    dir="arduino",
    file="arduino-bus-guide.html",
    title="I2C 與 SPI 通訊(進階選讀)",
    eyebrow="第 17 篇 · I2C 與 SPI",
    h1="用少少的線,控制很多東西:I2C 與 SPI",
    sub="用 I2C 掃描器找出裝置位址,再用 SPI 控制 74HC595 移位暫存器,用 3 條線驅動多顆 LED。",
    tldr="<strong>I2C</strong>:SDA、SCL 兩條線,靠<strong>位址</strong>找裝置(Uno:A4、A5)。<strong>SPI</strong>:MOSI、SCK 加選擇線,不用位址。74HC595:<code>SPI.transfer(位元組)</code> 把 8 個位元移進去,<strong>鎖存腳拉高</strong>後一次輸出到 8 個腳。",
    toc=[("what", "I2C 與 SPI"), ("fill", "填入數值"), ("i2c", "I2C 掃描器"), ("spi", "74HC595"), ("wire", "接線"), ("code", "SPI 程式"),
         ("try", "改改看"), ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
    body="\n\n".join([what, fillsec, i2c, spi, wire, code, try_, gotchas, practice]),
    config=dict(fill=FILL, sim=SIM, quiz=QUIZ, wiring=[bb.wiring_config(CIRC)], parts=bb.parts_info(CIRC)),
    prev=("arduino-interrupt-guide.html", "外部中斷 attachInterrupt"),
    next=("arduino-project-guide.html", "綜合專案:倒車雷達"),
)
