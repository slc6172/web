# -*- coding: utf-8 -*-
import copy, re
from h import *
import bb, a03

# ---------------------------------------------------------------- 練習用電路(正確版與故意做錯的版本)
def variant(base, cid, fn):
    c = copy.deepcopy(base)
    c.id = cid
    fn(c)
    return c

def plain(svg):
    """練習用的圖不要連動高亮:移除 data-part。"""
    return re.sub(r' data-part="[^"]*"', "", svg)

EX1_OK = variant(a03.CIRC, "ex1-ok", lambda c: None)
EX1_REV = variant(a03.CIRC, "ex1-rev", lambda c: c.part("LED1").pins.update({"A": "d10", "K": "d9"}))
EX1_COL = variant(a03.CIRC, "ex1-col", lambda c: c.part("W1").pins.update({"b": "a6"}))

two = bb.Circuit(
    "ex2-ok", 14,
    parts=[bb.Resistor("R1", 220, "b3", "b7", 1), bb.LED("LED1", "red", "d7", "d8", 2), bb.Wire("S1", "UNO.D8", "a3", "orange", 3),
           bb.Wire("K1", "a8", "t-8", "black", 3, route="straight"),
           bb.Resistor("R2", 220, "b9", "b13", 1), bb.LED("LED2", "green", "d13", "d14", 2), bb.Wire("S2", "UNO.D9", "a9", "blue", 3),
           bb.Wire("K2", "a14", "t-14", "black", 3, route="straight"), bb.Wire("G", "UNO.GND", "t-11", "black", 4)],
    steps=[("a", "a")] * 4,
    chains=[["UNO.D8", "R1", "LED1", "UNO.GND"], ["UNO.D9", "R2", "LED2", "UNO.GND"]])
EX2_OK = two
EX2_REV = variant(two, "ex2-rev", lambda c: c.part("LED2").pins.update({"A": "d14", "K": "d13"}))
EX2_NC = variant(two, "ex2-nc", lambda c: c.part("S2").pins.update({"b": "a10"}))
EX2_SCH = bb.schematic_svg(two, mark=())[0]

swap = bb.Circuit(
    "ex3", 12,
    parts=[bb.LED("LED1", "red", "d5", "d6", 1), bb.Resistor("R1", 220, "b6", "b10", 2), bb.Wire("S1", "UNO.D8", "a5", "orange", 3),
           bb.Wire("G", "UNO.GND", "a10", "black", 4)],
    steps=[("a", "a")] * 4,
    chain=["UNO.D8", "LED1", "R1", "UNO.GND"])
EX3_SCH_Y = bb.schematic_svg(swap, mark=())[0]
EX3_SCH_X = bb.schematic_svg(a03.CIRC, mark=())[0]

# 練習本身必須成立:正確版全部通過檢查;錯誤版一定被抓出來
def errs(c):
    return [m for lv, m in bb.check(c) if lv == "error"]
for ok in (EX1_OK, EX2_OK, swap):
    assert not errs(ok), (ok.id, errs(ok))
for bad in (EX1_REV, EX1_COL, EX2_REV, EX2_NC):
    assert errs(bad), bad.id
CIRCUITS = [EX1_OK, EX2_OK, swap]
SKETCHES = []

# ---------------------------------------------------------------- 符號總表
def symbol_sheet():
    G7, SL, CL = bb.GRAY7, bb.SLATE, bb.CLAY
    o = []
    def cell(i):
        return 20 + (i % 4) * 160, 20 + (i // 4) * 120
    def cap(i, t):
        x, y = cell(i)
        o.append(bb._txt(x + 60, y + 92, t, "sb", SL))
    # 0 電阻
    x, y = cell(0); o.append(bb._zigzag(x, y + 34, 120, 13, 6)); cap(0, "電阻")
    # 1 LED
    x, y = cell(1)
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (x, y + 34, x + 30, y + 34, G7))
    o.append('<polygon points="%d,%d %d,%d %d,%d" fill="#F2C9C3" stroke="%s" stroke-width="2" stroke-linejoin="round"/>' % (x + 30, y + 16, x + 30, y + 52, x + 66, y + 34, G7))
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.6" stroke-linecap="round"/>' % (x + 68, y + 16, x + 68, y + 52, G7))
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (x + 68, y + 34, x + 100, y + 34, G7))
    for dx in (0, 11):
        o.append('<path d="M%d,%d l9,-9 m-5,0 l5,0 l0,5" fill="none" stroke="%s" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>' % (x + 58 + dx, y + 12, bb.RUST))
    cap(1, "LED(發光二極體)")
    # 2 GND
    x, y = cell(2)
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (x + 50, y + 4, x + 50, y + 36, G7))
    for k, wd in enumerate((36, 24, 12)):
        yy = y + 36 + k * 8
        o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.4" stroke-linecap="round"/>' % (x + 50 - wd / 2, yy, x + 50 + wd / 2, yy, G7))
    cap(2, "GND 接地(0 V)")
    # 3 5V
    x, y = cell(3)
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.4" stroke-linecap="round"/>' % (x + 32, y + 14, x + 68, y + 14, G7))
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (x + 50, y + 14, x + 50, y + 56, G7))
    o.append(bb._txt(x + 50, y + 8, "5V", "mb", bb.RUST))
    cap(3, "電源 5V")
    # 4 腳位標籤
    x, y = cell(4)
    o.append('<rect x="%d" y="%d" width="64" height="30" rx="8" fill="#F0EEE6" stroke="%s" stroke-width="1.5"/>' % (x + 18, y + 18, G7))
    o.append(bb._txt(x + 50, y + 38, "Uno D8", "mb", SL))
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (x + 82, y + 33, x + 112, y + 33, G7))
    cap(4, "Uno 的腳位")
    # 5 導線
    x, y = cell(5)
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (x, y + 34, x + 110, y + 34, G7))
    cap(5, "導線(同一點)")
    # 6 交叉有點
    x, y = cell(6)
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/><line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (x + 10, y + 34, x + 100, y + 34, G7, x + 55, y + 6, x + 55, y + 62, G7))
    o.append('<circle cx="%d" cy="%d" r="5" fill="%s"/>' % (x + 55, y + 34, G7))
    cap(6, "交叉有圓點:接在一起")
    # 7 交叉無點
    x, y = cell(7)
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/><line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (x + 10, y + 34, x + 100, y + 34, G7, x + 55, y + 6, x + 55, y + 62, G7))
    cap(7, "交叉沒圓點:沒有接")
    return ('<svg viewBox="0 0 660 250" role="img" aria-label="本站用過的原理圖符號" style="min-width:520px"><defs>%s</defs><rect width="660" height="250" fill="#FFFFFF"/>%s</svg>'
            % (bb.STYLE, "".join(o)))

# ---------------------------------------------------------------- 內容
def canvas1(svg):
    return canvas(svg, [])

def opt_block(label, svg):
    return '<h3 style="margin:22px 0 8px">%s</h3>' % label + canvas1(plain(svg))

why = section("why", "原理圖是電路的共通語言",
  '<div class="panel"><h3>為什麼一定要學看原理圖</h3>'
  '<p>接線圖(麵包板圖)畫的是「零件<b>插在哪裡</b>」,同一個電路,每個人的擺法都不一樣。<b>原理圖只畫「誰接到誰」</b>,同一個電路永遠只有一張。</p>'
  '<p style="margin-bottom:0">網路上的教學、零件的資料表(datasheet)、書本,給你的幾乎都是原理圖。看得懂它,你就能自己把陌生的電路接到麵包板上,不必每次都等別人畫好接線圖。</p></div>',
  tip("原理圖<b>不代表零件在麵包板上的位置</b>。它只保證:圖上接在一起的點,實際也要接在一起;沒有連線的點,不能碰在一起。"))

symbols = section("symbols", "目前用過的符號",
  '<p class="sub" style="margin-bottom:14px">前幾篇已經看過這些。下面把它們集中在一張表,並多加兩個新的:<b>線的交叉</b>。</p>',
  canvas1(symbol_sheet()),
  '<h3 style="margin-top:26px">線交叉的規則</h3>',
  ops(["<b>交叉處有一個實心圓點</b>:兩條線在這裡接在一起,是同一個點。",
       "<b>交叉處沒有圓點</b>:只是畫圖時剛好交叉,<b>沒有接在一起</b>。",
       "線的「丁字路口」(一條線從中間接出去)一定會有圓點。"]),
  warn("看陌生的圖時,先看交叉處有沒有圓點,再決定線有沒有接在一起。看錯一個圓點,整個電路的意思就變了。", "新規則"))

rules = section("read", "怎麼讀一張原理圖:三步",
  steps(
    step(1, "找起點與終點", "電流需要出發點與回家的路。",
         ops(["起點通常是<b>電源(5V)或 Uno 的腳位(D8)</b>。", "終點通常是 <b>GND</b>。"])),
    step(2, "沿著線走,一個零件一個零件對照", "用手指順著線從起點走到終點。",
         ops(["每經過一個零件,就在麵包板上找出那個零件。", "順序是:D8 → 電阻 → LED → GND。這也是電流走的順序。"]),
         canvas1(bb.schematic_svg(a03.CIRC, mark=())[0])),
    step(3, "檢查方向", "LED 這類零件有方向,要看它的符號。",
         ops(["LED 的三角形<b>尖端指向電流流去的方向</b>(往 GND 那一邊),槓那一側是短腳(−)。", "麵包板上,長腳(+)就要接在靠近電阻、靠近 D8 的那一側。"])),
  ))

pa = section("pa", "練習一:原理圖 → 麵包板(找出接對的那一張)",
  '<p class="sub" style="margin-bottom:14px">下面這張原理圖,是第 3 篇的 LED 電路。三張麵包板接線圖只有一張是對的,另外兩張各有一處接錯。</p>',
  '<h3 style="margin:14px 0 8px">原理圖</h3>', canvas1(bb.schematic_svg(a03.CIRC, mark=())[0]),
  opt_block("接線圖 A", bb.breadboard_svg(EX1_REV)), opt_block("接線圖 B", bb.breadboard_svg(EX1_OK)), opt_block("接線圖 C", bb.breadboard_svg(EX1_COL)),
  sim("", "哪一張接線圖和原理圖相符?", "選一個答案。", [("p1a", "A"), ("p1b", "B"), ("p1c", "C")]))

pb = section("pb", "練習二:兩顆 LED、共用 GND",
  '<p class="sub" style="margin-bottom:14px">這張原理圖有兩條路:D8 接紅燈、D9 接綠燈,兩條路的 GND 是同一個。找出接對的接線圖。</p>',
  '<h3 style="margin:14px 0 8px">原理圖</h3>', canvas1(EX2_SCH),
  opt_block("接線圖 A", bb.breadboard_svg(EX2_NC)), opt_block("接線圖 B", bb.breadboard_svg(EX2_REV)), opt_block("接線圖 C", bb.breadboard_svg(EX2_OK)),
  sim("", "哪一張接線圖和原理圖相符?", "選一個答案。", [("p2a", "A"), ("p2b", "B"), ("p2c", "C")]))

pc = section("pc", "練習三:麵包板 → 原理圖",
  '<p class="sub" style="margin-bottom:14px">反過來:先看接線圖,找出對應的原理圖。這次電阻與 LED 的<b>順序</b>和之前不同。</p>',
  '<h3 style="margin:14px 0 8px">接線圖</h3>', canvas1(plain(bb.breadboard_svg(swap))),
  opt_block("原理圖 X", EX3_SCH_X), opt_block("原理圖 Y", EX3_SCH_Y),
  sim("", "哪一張原理圖和接線圖相符?", "選一個答案。", [("p3x", "X"), ("p3y", "Y")]),
  tip("電阻在 LED 前面還是後面,<b>電流都一樣大</b>(串聯電路各處電流相同),LED 都一樣亮。只是「接線圖看起來的樣子」與「原理圖的順序」要對得上。本站習慣把電阻放在訊號端這邊。"))

gotchas = section("gotchas", "常見迷思",
  details("原理圖上零件的位置,就是麵包板上零件的位置?",
    "<p>不是。原理圖為了好讀,排版與麵包板毫無關係。只看「誰連到誰」。</p>", True) +
  details("原理圖上兩條線交叉,就是接在一起?",
    "<p>只有交叉處有<b>實心圓點</b>才算接在一起。沒有圓點,只是剛好交叉。</p>") +
  details("圖上畫了三個 GND,是不是要接三條線?",
    "<p>不用。圖上每個 GND 符號都是同一個點。麵包板上可以共用一條 − 軌,再用<b>一條線</b>回到 Uno 的 GND(第 4 篇就是這樣)。</p>"))

SIM = {
  "p1a": "<b>不對。</b>A 圖的 LED 插反了:長腳(+)在 <code>d10</code>,靠近 GND 那側;原理圖要求長腳靠近電阻。",
  "p1b": "<b>對!</b>B 圖:D8 → 電阻 → LED 長腳(+),短腳(−)→ GND,每一處都和原理圖一致。",
  "p1c": "<b>不對。</b>C 圖的橘色線插在 <code>a6</code>,但電阻的左腳在第 5 欄,D8 沒有接到電阻,電路在這裡斷了。",
  "p2a": "<b>不對。</b>A 圖的藍線插在 <code>a10</code>,但第二組電阻在第 9 欄,D9 沒有接到電阻,綠燈那條路是斷的。",
  "p2b": "<b>不對。</b>B 圖的綠色 LED 插反了(長腳在 <code>d14</code>,靠近 GND 的一側)。原理圖要求長腳靠近電阻。",
  "p2c": "<b>對!</b>C 圖兩條路都完整、方向正確,兩顆 LED 的負極共用同一條 − 軌回到 GND。",
  "p3x": "<b>不對。</b>X 圖是「電阻 → LED」的順序;但接線圖裡,D8 先接到 LED 的長腳(<code>d5</code>),電阻在 LED 後面(<code>b6–b10</code>)接到 GND。",
  "p3y": "<b>對!</b>Y 圖的順序是 D8 → LED → 電阻 → GND,與接線圖一致。電阻在 LED 前或後,電流相同,LED 都一樣亮。",
}
QUIZ = quiz_cfg([
  ("原理圖上兩條線交叉、交叉處<b>沒有</b>圓點,代表?", ["兩條線接在一起", "只是畫圖時交叉,沒有接在一起", "電路短路"], 1,
   "實心圓點才代表連接。"),
  ("LED 符號中,三角形的尖端指向?", ["電流流去的方向(負極一側)", "正極一側", "沒有意義"], 0,
   "三角形尖端指向電流方向,槓是負極(短腳)。"),
  ("原理圖上的 GND 符號出現三次,代表?", ["三個不同的點", "同一個點(接在同一個 0 V)", "要接三條線回 Uno"], 1,
   "每個 GND 符號都是同一個點。"),
  ("原理圖會告訴你什麼?", ["零件在麵包板上的位置", "誰接到誰,以及零件的方向", "要買哪個牌子"], 1,
   "原理圖只管連接關係,不管位置。"),
  ("串聯電路裡,電阻放在 LED 前面或後面,電流大小?", ["前面比較大", "後面比較大", "一樣"], 2,
   "串聯各處電流相同,所以位置不影響 LED 亮度。"),
])
practice = section("practice", "測驗、檢查表與延伸閱讀",
  QUIZ_HTML,
  checks(["我能說出電阻、LED、GND、5V 與腳位標籤的符號。",
          "我知道交叉有圓點才算接在一起。",
          "我會用三步讀圖:找起點終點、沿線對照零件、檢查方向。",
          "我能在三張接線圖裡找出和原理圖相符的那一張。",
          "我知道原理圖不代表零件在麵包板上的位置。"], "做完之後,對照這張清單"),
  resources([
    ("https://www.arduino.cc/en/Tutorial/Blink", "Blink 教學(附電路圖與原理圖)", "Blink · circuit and schematic"),
    ("https://docs.arduino.cc/built-in-examples/basics/Blink/", "Blink 內建範例", "Blink (built-in example)"),
  ], "Arduino 官方文件"))

SPEC = dict(
    dir="arduino",
    file="arduino-schematic-guide.html",
    title="讀懂電路圖:原理圖與麵包板互相對照",
    eyebrow="第 5 篇 · 讀懂電路圖",
    h1="讀懂電路圖:看得懂,就能照著任何人的電路接",
    sub="原理圖只畫「誰接到誰」。這一篇集中練習原理圖和麵包板接線圖的互相對照,練到看得懂為止。",
    tldr="讀圖三步:<strong>找起點與終點 → 沿線對照零件 → 檢查方向</strong>。交叉處<strong>有圓點才連接</strong>;多個 GND 符號是<strong>同一個點</strong>;原理圖不代表零件位置。下面有三個對照練習。",
    toc=[("why", "為什麼學"), ("symbols", "符號"), ("read", "三步讀圖"), ("pa", "練習一"), ("pb", "練習二"), ("pc", "練習三"),
         ("gotchas", "常見迷思"), ("practice", "測驗與延伸閱讀")],
    body="\n\n".join([why, symbols, rules, pa, pb, pc, gotchas, practice]),
    config=dict(sim=SIM, quiz=QUIZ),
    prev=("arduino-loop-guide.html", "變數、for 與陣列:跑馬燈"),
    next=("arduino-pwm-guide.html", "PWM 呼吸燈與蜂鳴器"),
)
