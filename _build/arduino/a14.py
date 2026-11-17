# -*- coding: utf-8 -*-
from h import *
import bb

CIRC = bb.Circuit(
    "lcd-i2c", 22,
    parts=[
        bb.LCD("LCD1", 1),
        bb.Wire("V5", "UNO.5V", "MOD.VCC", "red", 2, route="left"), bb.Wire("G", "UNO.GND", "MOD.GND", "black", 2),
        bb.Wire("SDA", "UNO.SDA", "MOD.SDA", "blue", 3), bb.Wire("SCL", "UNO.SCL", "MOD.SCL", "yellow", 3),
    ],
    steps=[
        ("擺好 LCD", "LCD 模組<b>不用插麵包板</b>:平放在桌上,<b>背面朝上</b>,就能看到黏在背面的黑色 I2C 轉接板與四隻針腳。<br>轉接板上印著 <b>VCC、GND、SDA、SCL</b>(<b>順序依廠牌而異</b>,以你的轉接板上的字為準,圖上的順序只是示意)。"),
        ("電源線:5V 與 GND", "用<b>公對母杜邦線</b>(母頭那端插轉接板的針腳):<br>紅線:轉接板 <b>VCC</b> ← Uno <b>5V</b>(電源腳位排,Uno 上緣,要繞過左邊)。<br>黑線:轉接板 <b>GND</b> ← Uno 數位腳位排的 <b>GND</b>。"),
        ("訊號線:SDA 與 SCL", "藍線:轉接板 <b>SDA</b> ← Uno <b>SDA</b>(數位腳位排,靠近 AREF 那兩個之一;和 A4 是同一個訊號)。<br>黃線:轉接板 <b>SCL</b> ← Uno <b>SCL</b>(同上,和 A5 是同一個訊號)。<br>I2C 只用這兩條線:<b>SDA 傳資料,SCL 是節拍</b>。"),
    ],
    chains=[["UNO.5V", "LCD1.VCC"], ["LCD1.GND", "UNO.GND"], ["LCD1.SDA", "UNO.SDA"], ["LCD1.SCL", "UNO.SCL"]],
    intro="先<strong>拔掉 USB 線</strong>。LCD1602 加了 I2C 轉接板之後,只剩<b>四條線</b>:VCC、GND、SDA、SCL。這次<b>不用麵包板</b>,用公對母杜邦線直接從 Uno 接到轉接板的針腳。",
    done="四條線:5V → VCC、GND → GND、SDA → SDA、SCL → SCL。檢查:<b>SDA 與 SCL 沒有接反</b>,VCC 接的是 5V(不是 3.3V,否則背光會很暗)。",
    mode="direct",
)
CIRCUITS = [CIRC]

L1 = """// 第 14 篇:LCD1602 顯示文字
#include <Wire.h>
#include <hd44780.h>                         // 函式庫 hd44780(要先用 Library Manager 安裝)
#include <hd44780ioClass/hd44780_I2Cexp.h>   // 這個類別能自動找出 I2C 位址

hd44780_I2Cexp lcd;                          // 建立 LCD 物件

void setup() {
  int status = lcd.begin(16, 2);             // 16 欄、2 列。回傳 0 表示成功
  if (status) {                              // 不是 0:找不到 LCD
    hd44780::fatalError(status);             // 用板子上的 L 燈閃爍代表錯誤,並停在這裡
  }
  lcd.print("Hello, Arduino!");              // 第一行(游標一開始在左上角)
  lcd.setCursor(0, 1);                       // 游標移到第 0 欄、第 1 列(也就是第二行開頭)
  lcd.print("LCD1602 I2C");
}

void loop() {
}
"""
L2 = """// 第 14 篇:會動的數字
#include <Wire.h>
#include <hd44780.h>
#include <hd44780ioClass/hd44780_I2Cexp.h>

hd44780_I2Cexp lcd;
int count = 0;

void setup() {
  int status = lcd.begin(16, 2);
  if (status) {
    hd44780::fatalError(status);
  }
  lcd.print("Counter");
}

void loop() {
  lcd.setCursor(0, 1);              // 每次都回到第二行開頭
  lcd.print("count: ");
  lcd.print(count);                 // print 也能印數字
  lcd.print("   ");                 // 多印幾個空白,把上一次殘留的字蓋掉
  count = count + 1;
  delay({gap});
}
"""
L3 = """// 另一個常見的函式庫:LiquidCrystal I2C(很多教學用它)
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);   // I2C 位址 0x27(有些模組是 0x3F)、16 欄、2 列

void setup() {
  lcd.begin();                        // 較舊的版本要寫成 lcd.init();
  lcd.backlight();                    // 打開背光
  lcd.print("Hello, Arduino!");
  lcd.setCursor(0, 1);
  lcd.print("LiquidCrystal I2C");
}

void loop() {
}
"""
FILL = dict(gap="500")
SKETCHES = [
    dict(name="lcd-hello", code=L1, fill=FILL, libs=["Wire", "hd44780"]),
    dict(name="lcd-count", code=L2, fill=FILL, libs=["Wire", "hd44780"]),
    dict(name="lcd-alt", code=L3, fill=FILL, libs=["Wire", "LiquidCrystal_I2C"]),
]

def lcd_schematic():
    G7, SL, CL = bb.GRAY7, bb.SLATE, bb.CLAY
    o = ['<g class="el" data-part="LCD1" tabindex="0" role="button" aria-label="LCD 模組,點一下看它在實物上是哪一個">'
         '<rect class="halo" x="108" y="26" width="160" height="168" rx="12" fill="none" stroke="%s" stroke-width="2.5"/>'
         '<rect x="120" y="34" width="136" height="152" rx="8" fill="#F0EEE6" stroke="%s" stroke-width="1.8"/>' % (CL, G7),
         bb._txt(188, 104, "LCD1602", "mb", SL), bb._txt(188, 120, "I2C 轉接板", "s", bb.GRAY5)]
    for nm, y, side in (("VCC", 60, "L"), ("GND", 160, "L"), ("SDA", 84, "R"), ("SCL", 140, "R")):
        o.append(bb._txt(130, y + 4, nm, "m", SL, "start") if side == "L" else bb._txt(246, y + 4, nm, "m", SL, "end"))
    o.append("</g>")
    o.append('<line x1="120" y1="60" x2="78" y2="60" stroke="%s" stroke-width="2"/><line x1="78" y1="60" x2="78" y2="40" stroke="%s" stroke-width="2"/>' % (G7, G7))
    o.append('<line x1="62" y1="40" x2="94" y2="40" stroke="%s" stroke-width="2.4" stroke-linecap="round"/>' % G7 + bb._txt(78, 32, "5V", "mb", bb.RUST))
    o.append('<line x1="120" y1="160" x2="78" y2="160" stroke="%s" stroke-width="2"/><line x1="78" y1="160" x2="78" y2="176" stroke="%s" stroke-width="2"/>' % (G7, G7))
    for k, wd in enumerate((28, 18, 8)):
        o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.2" stroke-linecap="round"/>' % (78 - wd / 2, 176 + k * 7, 78 + wd / 2, 176 + k * 7, G7))
    for nm, y, lab in (("SDA", 84, "Uno SDA(A4)"), ("SCL", 140, "Uno SCL(A5)")):
        o.append('<line x1="256" y1="%d" x2="300" y2="%d" stroke="%s" stroke-width="2"/>' % (y, y, G7))
        o.append('<rect x="300" y="%d" width="112" height="30" rx="8" fill="#F0EEE6" stroke="%s" stroke-width="1.5"/>%s' % (y - 15, G7, bb._txt(356, y + 4, lab, "mb", SL)))
    o.append(bb._txt(278, 76, "⇄", "mb", bb.GRAY5) + bb._txt(278, 132, "→", "mb", bb.GRAY5))
    return ('<svg viewBox="0 0 440 220" role="img" aria-label="LCD I2C 原理圖" style="min-width:440px"><defs>%s</defs><rect width="440" height="220" fill="#FFFFFF"/>%s</svg>' % (bb.STYLE, "".join(o)))

lcdsim = ('<div class="panel" data-lcdsim><div class="wgrid f2"><div><label>第一行(最多 16 個英文字母 / 數字)</label><input data-lcd="l1" value="Hello, Arduino!" autocomplete="off" spellcheck="false"></div>'
          '<div><label>第二行</label><input data-lcd="l2" value="LCD1602 I2C" autocomplete="off" spellcheck="false"></div></div>'
          '<div class="lcd-screen" style="margin-top:12px" aria-live="polite"></div><div class="lcd-code"></div></div>')

what = section("what", "LCD1602:Arduino 的小螢幕",
  '<div class="panel"><h3>認識 LCD1602</h3>'
  '<p><b>LCD1602 能顯示 2 行、每行 16 個字元</b>(共 32 個字),是最常見的字元型液晶。它本身有 16 隻接腳,接起來很麻煩;所以我們買<b>已經焊好 I2C 轉接板</b>的版本,<b>只要四條線</b>。</p>'
  '<p style="margin-bottom:0">不只能顯示英文字母和數字,但<b>預設不能顯示中文</b>。這一篇只顯示英文與數字。</p></div>',
  '<h3 style="margin-top:26px">I2C:用兩條線說話</h3>',
  '<p><b>I2C</b>(讀作 I-squared-C)是一種只用<b>兩條線</b>就能和多個裝置溝通的方式:<b>SDA</b> 傳資料、<b>SCL</b> 是節拍(時脈)。一條 I2C「匯流排」上可以掛很多裝置,每個裝置有自己的<b>位址</b>,Arduino 叫誰,誰才回應。Uno 上 <b>A4 是 SDA、A5 是 SCL</b>(數位腳位排靠近 AREF 處也有一組同樣訊號的 SDA、SCL)。第 17 篇會更深入。</p>',
  tip("LCD 的液晶模組是 <b>5 V</b> 供電。接 Uno 的 5V 腳就好,不要接 3.3V,否則背光會很暗、字也看不清楚。"))

lib = section("lib", "安裝函式庫:hd44780",
  '<p class="sub" style="margin-bottom:14px">和第 13 篇一樣,用 Library Manager 安裝。這次我選 <b>hd44780</b> 函式庫(作者 Bill Perry):它能<b>自動找出轉接板的 I2C 位址</b>,不用猜 <code>0x27</code> 還是 <code>0x3F</code>,新手最容易卡關的地方它幫你處理掉了。</p>',
  ops(["點左側 <b>Library Manager</b>,搜尋 <code>hd44780</code>。", "找到 <b>hd44780(Bill Perry)</b>,按 <b>INSTALL</b>。", "如果跳出相依視窗,按 <b>INSTALL ALL</b>。", "裝好後可看範例:<b>File → Examples → hd44780 → ioClass → hd44780_I2Cexp → HelloWorld</b>。"]),
  tip("很多網路教學用的是 <b>LiquidCrystal I2C</b> 這個函式庫(要手動填 I2C 位址)。它也能用,本篇最後有它的寫法。<b>但同名的函式庫有好幾個版本,初始化函式有的叫 <code>init()</code>、有的叫 <code>begin()</code></b>:看到編譯錯誤找不到其中一個,換成另一個試試。"))

wire = section("wire", "接線:四條線,不用麵包板",
  bb.stepper_html(CIRC),
  '<p class="sk">LCD 的實物比圖大(約 8 公分寬);圖只是示意。<b>5V 的線要繞過 Uno 的左邊</b>。以轉接板上印的針腳名稱為準(手機上可以左右滑動圖)。</p>',
  '<h3 style="margin-top:26px">接線表</h3>', bb.wiring_table(CIRC),
  warn("<b>轉接板針腳的順序因廠牌而異</b>(有的是 GND、VCC、SDA、SCL,有的是 VCC、GND、SDA、SCL)。<b>一律對照你的轉接板上印的字接線</b>,不要照圖上的位置接。VCC 與 GND 接反會損壞轉接板。接線前先拔 USB。", "注意"),
  '<h3 style="margin-top:26px">原理圖</h3>', canvas(lcd_schematic(), []),
  '<div class="linkbox" id="linkInfo" style="margin-top:12px">點原理圖裡的 LCD 方框,看它在實物上是哪一個。</div>')

contrast = section("contrast", "接上之後的第一件事:調對比",
  '<p class="sub" style="margin-bottom:14px">轉接板上有一個<b>藍色的小旋鈕(對比旋鈕,其實是一顆微調電阻)</b>。對比調錯時,<b>畫面會是「整排白色方塊」或「完全空白」</b>,即使程式與接線都對。</p>',
  ops(["上傳程式一,讓背光亮起。", "用小<b>十字或一字螺絲起子</b>,<b>慢慢</b>轉那顆藍色旋鈕,一邊看螢幕。", "轉到<b>白色方塊消失、字清楚出現</b>就停。"]),
  see("對比正確時,第一行是 <code>Hello, Arduino!</code>,第二行是 <code>LCD1602 I2C</code>。"),
  tip("這是 LCD 最常見的「明明都對卻沒字」原因,幾乎每個人都會遇到一次。"))

fillsec = section("fill", "先填入計數的間隔",
  fill([("gap", "程式二:每次加 1 之間的間隔(毫秒)", True)]),
  '<p class="sk">空白時用範例值 500 毫秒。</p>')

def exp(items):
    return table("g2", ["這一行", "它在做什麼"], items)

code1 = section("code1", "程式一:顯示兩行字",
  '<p class="sub" style="margin-bottom:14px">先在這裡預覽:輸入文字,看看螢幕與對應的程式碼:</p>', lcdsim,
  cmd(L1, cap="LCD1602:顯示 Hello 與第二行", cpp=True),
  exp([
    ["<code>hd44780_I2Cexp lcd;</code>", "建立 LCD 物件。<code>I2Cexp</code> 表示「透過 I2C 轉接板、自動偵測」。"],
    ["<code>lcd.begin(16, 2)</code>", "啟動 LCD:16 欄、2 列。<b>回傳 0 表示成功</b>,不是 0 表示出錯(找不到)。"],
    ["<code>hd44780::fatalError(status);</code>", "出錯時,用 Uno 的 L 燈閃爍來報告,並停住。看到 L 燈在閃,就是 LCD 沒找到(檢查接線)。"],
    ["<code>lcd.print(\"…\")</code>", "在游標位置印出文字。和 <code>Serial.print</code> 用法一樣,可以印文字、數字。"],
    ["<code>lcd.setCursor(0, 1);</code>", "把游標移到<b>第 0 欄、第 1 列</b>。<b>欄、列都是從 0 開始</b>:第一行是 0、第二行是 1。"],
  ]),
  see("調好對比後,第一行顯示 <code>Hello, Arduino!</code>,第二行顯示 <code>LCD1602 I2C</code>。"))

code2 = section("code2", "程式二:會動的數字",
  cmd(L2, cap="LCD:每 0.5 秒加 1", cpp=True),
  exp([
    ["<code>lcd.setCursor(0, 1);</code>", "每次都先回到第二行開頭,才不會越寫越右。"],
    ["<code>lcd.print(count);</code>", "印出變數的值,例如 <code>12</code>。"],
    ["<code>lcd.print(\"   \");</code>", "多印三個空白。數字由 <code>10</code> 變成 <code>9</code> 這種情況(位數變少)時,把上一次殘留的字蓋掉。"],
  ]),
  see("第二行顯示 <code>count: 0</code>、<code>count: 1</code>… 不斷增加。"),
  table("g3", ["函式", "作用", "例子"], [
    ["<code>lcd.print(x)</code>", "在游標處印出文字或數字", "<code>lcd.print(\"Hi\");</code>"],
    ["<code>lcd.setCursor(欄, 列)</code>", "移動游標(從 0 算起)", "<code>lcd.setCursor(5, 1);</code>"],
    ["<code>lcd.clear()</code>", "清除整個螢幕(游標回左上角)", "<code>lcd.clear();</code>"],
    ["<code>lcd.noBacklight()</code> / <code>lcd.backlight()</code>", "關閉 / 打開背光", "<code>lcd.noBacklight();</code>"],
  ]))

alt = section("alt", "別的教學用的函式庫:LiquidCrystal I2C",
  cmd(L3, cap="LiquidCrystal I2C 版本", cpp=True),
  ops(["<b>位址要自己填</b>:<code>0x27</code> 或 <code>0x3F</code>。不確定就用第 17 篇的 I2C 掃描程式查。", "<b>初始化</b>依版本不同:<code>lcd.begin()</code> 或 <code>lcd.init()</code>。", "<b>打開背光</b>:<code>lcd.backlight()</code>。後面的 <code>setCursor</code>、<code>print</code> 和上面完全一樣。"]))

try_ = section("try", "改改看",
  table("g3", ["挑戰", "怎麼改", "你會看到"], [
    ["顯示自己的名字", "把 <code>Hello, Arduino!</code> 換成你的英文名字", "螢幕顯示你的名字。"],
    ["第二行靠右", "<code>lcd.setCursor(8, 1);</code>", "文字從第 9 個位置開始。"],
    ["閃爍的背光", "在 <code>loop()</code> 加 <code>lcd.noBacklight(); delay(500); lcd.backlight(); delay(500);</code>", "背光一閃一閃。"],
    ["接上第 13 篇的 DHT11", "把溫度、濕度顯示在 LCD 上(第 18 篇綜合專案會用到類似做法)", "不用開電腦也能看溫濕度。"],
  ]))

gotchas = section("gotchas", "常見卡關",
  details("背光亮,但螢幕只有一排白色方塊,或完全空白",
    "<p><b>對比沒調好。</b>用小螺絲起子慢慢轉轉接板上的藍色旋鈕,直到字出現。這是最常見的原因,先做這個。</p>", True) +
  details("L 燈一直規律地閃(程式停在 fatalError)",
    ops(["<b>找不到 LCD</b>:檢查四條線。<b>SDA 與 SCL 沒有接反</b>、VCC 是 5V、GND 有接。", "杜邦線的母頭有沒有插緊轉接板的針腳。", "你的轉接板針腳順序,是否和接線一致(對照上面印的字)。"])) +
  details("編譯錯誤:找不到 hd44780.h",
    "<p>函式庫沒裝。回 Library Manager,搜尋 <code>hd44780</code>,安裝作者 Bill Perry 的那一個。</p>") +
  details("完全沒反應,背光也不亮",
    "<p>VCC 與 GND 沒有接好。用另一條杜邦線、或換一組針腳確認。USB 有沒有接上、<code>ON</code> 燈有沒有亮。</p>") +
  details("顯示亂碼、或字母怪怪的",
    "<p>電壓不足或接觸不良,檢查 VCC 是否為 5V。也要確認顯示的是英文與數字,預設的 LCD 不能直接顯示中文。</p>"))

SIM = {
  "a1": "<b>不用。</b>背光亮但沒字,幾乎一定是<b>對比沒調好</b>。程式不用動。",
  "a2": "<b>對。</b>慢慢轉轉接板上的藍色對比旋鈕,直到白色方塊消失、字出現。這是 LCD 最常見的「沒字」原因。",
  "a3": "<b>沒有用。</b>換 USB 線不影響螢幕的對比。",
}
QUIZ = quiz_cfg([
  ("I2C 用哪兩條訊號線?", ["SDA 與 SCL", "TX 與 RX", "VCC 與 GND"], 0, "SDA 傳資料,SCL 是時脈。"),
  ("Uno 上 I2C 的 SDA 與 SCL 在哪兩個腳位?", ["A4 與 A5", "2 與 3", "0 與 1"], 0, "A4 = SDA、A5 = SCL。"),
  ("<code>lcd.setCursor(0, 1)</code> 把游標移到?", ["第二行的開頭", "第一行的開頭", "第 1 欄第 0 列"], 0, "欄與列都從 0 開始:列 1 是第二行。"),
  ("背光亮、但螢幕只有一排白色方塊,最可能的原因是?", ["對比沒調好", "程式寫錯", "Uno 壞了"], 0, "調轉接板上的藍色旋鈕。"),
  ("為什麼數字變少位數時要多印空白?", ["把上一次殘留的字蓋掉", "讓背光更亮", "節省記憶體"], 0, "LCD 不會自動清除舊字。"),
])
practice = section("practice", "動手演練與延伸閱讀",
  sim("", "情境:背光亮著,螢幕上只有一排白色方塊", "你應該先?",
      [("a1", "改寫程式"), ("a2", "用螺絲起子慢慢轉轉接板上的藍色對比旋鈕"), ("a3", "換 USB 線")]),
  QUIZ_HTML,
  checks(["我知道 LCD1602 是 2 行 16 字,I2C 只用 SDA、SCL 兩條線。",
          "我用 Library Manager 安裝了 hd44780 函式庫。",
          "我的四條線依轉接板上印的字接好(VCC、GND、SDA、SCL)。",
          "我調好了對比,螢幕顯示出文字。",
          "我會用 <code>setCursor</code>(從 0 算起)與 <code>print</code>。",
          "我知道要多印空白把殘留的字蓋掉。"], "做完之後,對照這張清單"),
  resources([
    ("https://docs.arduino.cc/software/ide-v2/tutorials/ide-v2-installing-a-library", "在 IDE 2 安裝函式庫", "Installing libraries"),
    ("https://docs.arduino.cc/language-reference/en/functions/communication/wire/", "Wire 函式庫(I2C)", "Arduino language reference"),
  ], "Arduino 官方文件"))

SPEC = dict(
    dir="arduino",
    file="arduino-lcd-guide.html",
    title="LCD1602 I2C 顯示:四條線的小螢幕",
    eyebrow="第 14 篇 · LCD1602 I2C",
    h1="四條線,讓 Arduino 有一個小螢幕",
    sub="用 I2C 轉接板的 LCD1602 顯示文字與數字。認識 I2C 的 SDA、SCL,安裝 hd44780 函式庫,並學會調對比。",
    tldr="I2C LCD <strong>四條線:VCC、GND、SDA、SCL</strong>(不用麵包板)。安裝 <strong>hd44780</strong> 函式庫,<code>lcd.begin(16, 2)</code>、<code>lcd.print()</code>、<code>lcd.setCursor(欄, 列)</code>(從 0 算起)。<strong>沒字先調轉接板上的藍色對比旋鈕</strong>。",
    toc=[("what", "LCD 與 I2C"), ("lib", "安裝函式庫"), ("wire", "接線"), ("contrast", "調對比"), ("fill", "填入數值"), ("code1", "程式一:顯示文字"),
         ("code2", "程式二:會動的數字"), ("alt", "另一個函式庫"), ("try", "改改看"), ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
    body="\n\n".join([what, lib, wire, contrast, fillsec, code1, code2, alt, try_, gotchas, practice]),
    config=dict(fill=FILL, sim=SIM, quiz=QUIZ, wiring=[bb.wiring_config(CIRC)], parts=bb.parts_info(CIRC)),
    prev=("arduino-dht-guide.html", "溫濕度 DHT11 與安裝函式庫"),
    next=("arduino-millis-guide.html", "millis():不卡住的計時"),
)
