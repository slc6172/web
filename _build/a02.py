# -*- coding: utf-8 -*-
from h import *
import bb

CIRC = bb.Circuit(
    "led-5v", 14,
    parts=[
        bb.Resistor("R1", 220, "t+6", "b6", 1),
        bb.LED("LED1", "red", "d6", "d7", 2),
        bb.Wire("W3", "a7", "t-7", "black", 3, route="straight"),
        bb.Wire("W1", "UNO.5V", "t+1", "red", 4, route="left"),
        bb.Wire("W2", "UNO.GND", "t-3", "black", 5),
    ],
    steps=[
        ("放電阻", "電阻一腳插在<b>上方紅線那排</b>的 <code>t+6</code>(+ 電源軌),另一腳插 <code>b6</code>(第 6 欄)。<br>電阻沒有方向。它橫跨在電源軌與第 6 欄之間,會蓋住中間的 <code>t-6</code> 與 <code>a6</code>,那兩個孔不要用。"),
        ("放 LED", "<strong>長腳(+)</strong>插 <code>d6</code>,<strong>短腳(−)</strong>插 <code>d7</code>。<br>"
                  "<code>d6</code> 和電阻的 <code>b6</code> 在同一欄(第 6 欄,a–e 相通),所以電阻已經接到 LED 的長腳。"),
        ("黑色短線:LED 負極 → − 軌", "黑色短線一端插 <code>a7</code>(和 LED 短腳同一欄),另一端插上方<b>藍線那排</b>的 <code>t-7</code>(− 電源軌)。<br>這樣 LED 的負極就接到了 − 軌。"),
        ("紅線:Uno 5V → + 軌", "紅色杜邦線一端插 Uno <b>電源腳位排</b>(Uno 上緣)的 <strong>5V</strong>,另一端插 <code>t+1</code>。<br>整條 + 軌現在都是 5 V,電阻上端因此有電。"),
        ("黑線:Uno GND → − 軌", "黑色杜邦線一端插 Uno 數位腳位排的 <strong>GND</strong>(13 號腳旁邊),另一端插 <code>t-3</code>。<br>整條 − 軌現在都是 GND(0 V),電路繞成完整的一圈。"),
    ],
    chain=["UNO.5V", "R1", "LED1", "UNO.GND"],
    intro="先<strong>拔掉 USB 線</strong>。這次我們不用數位腳位,而是直接把 Uno 的 <b>5V</b> 與 <b>GND</b> 接到麵包板上下方的電源軌,再從電源軌取電。按「下一步」,一次放一個零件。",
    done="5V → 電阻 → LED 長腳(+),LED 短腳(−)→ GND,是一個完整的圈。接好後,對照下面的接線表檢查一次,再接上 USB。",
)
CIRCUITS = [CIRC]
SKETCHES = []
I_MA = (bb.UNO_VCC - bb.LED_C["red"][3]) / 220.0 * 1000.0


def colors(ohm):
    b = bb.bands(ohm)
    return "、".join([bb.BAND_NAME[b[0]], bb.BAND_NAME[b[1]], bb.BAND_NAME[b[2]] if b[2] != "gold" else "金", "金"])


what = section("what", "電的三個量:電壓、電流、電阻",
  '<p class="sub" style="margin-bottom:14px">把電想成水管裡的水,三個量就很好懂:</p>',
  table("g3", ["名稱", "水管比喻", "單位與常見數字"], [
    ["電壓 V", "水壓:推動水流動的力量。", "伏特(V)。Uno 的電源是 <b>5 V</b>。"],
    ["電流 I", "水流量:每秒流過多少水。", "安培(A),LED 電路常用<b>毫安(mA)</b>。1 A = 1000 mA。"],
    ["電阻 R", "水管的窄處:越窄,水流得越少。", "歐姆(Ω)。本主題常用 220 Ω、10 kΩ(1 kΩ = 1000 Ω)。"],
  ]),
  '<div class="panel" style="margin-top:18px"><h3>電路要「繞成一整圈」才有電流</h3>'
  '<p>電流從電源的一端出發,經過零件,回到電源的另一端。<b>圈中任何一處斷掉,電流就停了。</b>所以 LED 不亮,多半是圈沒有接完整。</p>'
  '<ul style="margin:0;padding-left:20px"><li><b>開路</b>:圈斷了(線沒插好、零件腳鬆脫),沒有電流,零件不工作。</li>'
  '<li><b>短路</b>:電流找到一條<b>幾乎沒有阻力</b>的捷徑(例如 5V 直接接 GND),電流會大到讓線材與板子發燙、損壞。</li></ul></div>',
  '<div class="panel" style="margin-top:14px"><h3>GND 是什麼?</h3>'
  '<p style="margin-bottom:0">GND(接地)是電路的 <b>0 V 參考點</b>。電壓永遠是「兩點之間的差」:5V 腳比 GND 高 5 V,電流就想從 5V 流向 GND。所以一個完整的電路,一定有一條線接到 GND 當作「回家的路」。</p></div>',
  warn("<b>永遠不要把 5V 直接用導線接到 GND</b>,中間沒有任何零件。這就是短路。Uno 的 USB 有保護,但仍可能讓板子或電腦的 USB 孔受損。", "短路"))

ohm_rows = [[fmt, "%s" % colors(v), use] for fmt, v, use in
            (("220 Ω", 220, "LED 限流(本主題最常用)"), ("330 Ω", 330, "LED 限流,稍暗一點"),
             ("1 kΩ", 1000, "小電流、保護用"), ("4.7 kΩ", 4700, "感測器上拉(第 13 篇)"), ("10 kΩ", 10000, "按鈕、光敏電阻(第 7、10 篇)"))]
ohm = section("ohm", "歐姆定律:知道兩個量,就能算出第三個",
  '<div class="panel"><h3>V = I × R</h3>'
  '<p style="margin-bottom:0">電壓 = 電流 × 電阻。改寫成 <b>I = V ÷ R</b>(電流)、<b>R = V ÷ I</b>(電阻)。電壓不變時,<b>電阻越大,電流越小</b>。</p></div>',
  '<h3 style="margin-top:26px">LED 電路怎麼算:一個完整的例子</h3>',
  ops(["LED 點亮時,自己會「吃掉」一小段電壓,叫<b>順向壓降</b>,紅色 LED 約 <b>2.0 V</b>(官方 Blink 範例寫紅色約 1.8–2.2 V)。",
       "電源 5 V 減去 LED 的 2.0 V,剩下 <b>3.0 V</b> 由電阻承擔。",
       "想要電流約 10 mA(0.01 A):R = 3.0 ÷ 0.01 = <b>300 Ω</b>。",
       "電阻有標準值(300 Ω 不常見),取<b>不小於計算值</b>的標準值:330 Ω。實際電流 = 3.0 ÷ 330 ≈ <b>9.1 mA</b>。",
       "本主題用 <b>220 Ω</b>:3.0 ÷ 220 ≈ <b>%.1f mA</b>,亮度夠、也在 Uno 每腳 20 mA 的建議上限之內。" % I_MA]),
  '<h3 style="margin-top:26px">自己算算看</h3>',
  '<div class="panel" data-ledcalc><div class="wgrid f2">'
  '<div><label>LED 顏色(順向壓降 Vf)</label><select data-lc="vf"><option value="2.0">紅色 2.0 V</option><option value="2.1">黃色 2.1 V</option><option value="2.2">綠色 2.2 V</option><option value="3.0">藍色或白色 3.0 V</option></select></div>'
  '<div><label>想要的電流(mA)</label><input data-lc="ma" value="10" inputmode="decimal" autocomplete="off"></div></div>'
  '<div class="lc-out" aria-live="polite"></div></div>',
  '<p class="sk">這裡的壓降是常見範例值,實際請以你的 LED 規格為準。官方 Blink 範例也提到:5V 板子搭配 LED,電阻到約 1 kΩ 都還看得見亮度。</p>',
  tip("常見電阻只有<b>標準值</b>(E12 系列:10、12、15、18、22、27、33、39、47、56、68、82 再乘上 10 的次方)。買 <b>220 Ω、330 Ω、1 kΩ、10 kΩ</b> 就夠做完這個主題。"))

rcode = section("rcode", "看懂電阻上的色環",
  '<p class="sub" style="margin-bottom:14px">電阻身上的彩色環就是它的數值。下面的計算機兩個方向都能用:選顏色看數值,或輸入數值看顏色。</p>',
  '<div class="panel" data-rcalc>'
  '<svg class="rc-svg" viewBox="0 0 320 70" role="img" aria-label="電阻色環示意圖">'
  '<line x1="8" y1="35" x2="312" y2="35" stroke="#87867F" stroke-width="4" stroke-linecap="round"/>'
  '<rect x="60" y="12" width="200" height="46" rx="20" fill="#E3DACC" stroke="#87867F" stroke-width="1.5"/>'
  '<rect class="rc1" x="92" y="12" width="16" height="46" fill="#B04A3F"/>'
  '<rect class="rc2" x="124" y="12" width="16" height="46" fill="#B04A3F"/>'
  '<rect class="rc3" x="156" y="12" width="16" height="46" fill="#8B5A3C"/>'
  '<rect x="222" y="12" width="16" height="46" fill="#C9A227"/></svg>'
  '<div class="wgrid f4"><div><label>第 1 環(十位數)</label><select data-rc="b1"></select></div>'
  '<div><label>第 2 環(個位數)</label><select data-rc="b2"></select></div>'
  '<div><label>第 3 環(乘數)</label><select data-rc="b3"></select></div>'
  '<div><label>電阻值(可直接輸入)</label><input data-rc="val" value="220" autocomplete="off" spellcheck="false"></div></div>'
  '<div class="rc-out" aria-live="polite"></div></div>',
  '<h3 style="margin-top:26px">本主題用到的電阻</h3>',
  table("g3", ["電阻值", "色環(四環,最後一環金色 = ±5%)", "用途"], ohm_rows),
  '<h3 style="margin-top:26px">怎麼讀</h3>',
  ops(["把電阻放好,<b>金色(或銀色)那一環放在右邊</b>,從左邊開始讀。",
       "前兩環是數字,第三環是乘數(後面補幾個 0),第四環是誤差(金色 = ±5%)。",
       "<b>五環電阻</b>:前三環是數字,第四環乘數,第五環誤差(棕色 = ±1%)。例如 220 Ω 的五環是紅、紅、黑、黑、棕。",
       "還是看不清楚,就用<b>萬用電錶</b>量。量電阻時,電阻要先從電路上拿下來。"]))

board_widget = ('<div class="panel" data-bbx><div class="canvas">%s</div>'
                '<div class="bbx-bar"><label><input type="checkbox" class="bbx-split"> 我的麵包板電源軌在中間是斷開的</label></div>'
                '<div class="bbx-info">點上面任何一個孔,看哪些孔在內部相通。</div></div>' % bb.explorer_svg(20))
board = section("board", "麵包板:內部藏著的連線",
  '<p class="sub" style="margin-bottom:14px">麵包板上的小孔不是各自獨立的,底下有金屬片把某些孔連在一起。<b>這就是不用焊接也能接電路的祕密。</b>試試看:</p>',
  board_widget,
  '<h3 style="margin-top:26px">三條規則</h3>',
  ops(["<b>同一欄(同一個數字)的 <code>a–e</code> 五個孔彼此相通</b>;<code>f–j</code> 是另一組五個孔。兩組之間不相通。",
       "<b>中間的凹槽</b>把上下兩組分開。IC(例如第 17 篇的 74HC595)會跨在凹槽上,左右兩排腳各落在不同組。",
       "<b>最外側的長條(電源軌)整條相通</b>,通常上面一條標紅線(+)、下面一條標藍線(−),拿來接 5V 與 GND。"]),
  '<h3 style="margin-top:26px">兩個零件怎麼「接在一起」?</h3>',
  '<p>把兩隻腳插進<b>同一欄的 a–e(或 f–j)</b>,它們就連起來了。要接遠一點的,用杜邦線從這一欄拉到另一欄。</p>',
  warn("<b>同一個零件的兩隻腳,不要插在同一欄。</b>那樣兩腳被金屬片連在一起,等於零件被短路,不會有任何作用。"),
  tip("很多長麵包板的電源軌<b>在中間是斷開的</b>(左半與右半不相通)。拿到麵包板先用上面的探索圖勾選看看差別,再用電錶或一個 LED 實測:兩半都要接電源,或把零件放在有接電的那一半。"))

sch_svg, sch_legend = bb.schematic_svg(CIRC)
build = section("build", "實作:不用寫程式、插上 USB 就會亮的電路",
  '<p class="sub" style="margin-bottom:14px">這個電路沒有程式:Uno 只是當<b>電源</b>用。目的是練習用電源軌接線,並親眼看到「完整的圈才有電流」。</p>',
  bb.stepper_html(CIRC),
  '<div class="linkbox" style="margin-top:12px">點圖上的零件,它會亮起橘色光圈,而且在下方的原理圖也會跟著亮。</div>',
  '<p class="sk">Uno 轉了 180 度擺放:電源腳位(5V、GND…)在上緣,數位腳位排在下緣。圖只畫左邊 14 欄,你的麵包板更長,以欄號與 a–j 為準。</p>',
  '<h3 style="margin-top:26px">接線表</h3>', bb.wiring_table(CIRC),
  warn("先確認 <b>USB 拔掉</b>、紅線只插 <b>5V</b>、黑線只插 <b>GND</b>,再接上 USB。5V 與 GND 兩條線絕對不能互相碰到。"),
  see("接上 USB 後,LED <b>一直亮著,不會閃</b>,因為 5V 一直都在,沒有程式控制它。電流約 %.1f mA。" % I_MA),
  '<h3 style="margin-top:26px">動手試試:把圈弄斷,再接回去</h3>',
  table("g3", ["你做的事", "會看到", "代表什麼"], [
    ["拔掉黑色 GND 線(Uno 那端)", "LED 熄滅", "圈斷了(<b>開路</b>),沒有回家的路,電流停止。"],
    ["重新插回 GND", "LED 又亮", "圈接上,電流回來。"],
    ["把 LED 轉 180 度(長短腳對調)", "LED 不亮", "LED 有方向,反過來電流不通。"],
  ]),
  '<h3 style="margin-top:26px">對應的原理圖</h3>',
  canvas(sch_svg, [(n, '<span class="newsym">新符號</span>' + t) for n, t in sch_legend if n]),
  '<div class="linkbox" id="linkInfo" style="margin-top:12px">點原理圖裡的電阻或 LED,看它在麵包板上是哪個零件。</div>',
  '<p style="margin-top:14px">下一篇會把 5V 換成 Uno 的 <b>8 號腳</b>:同樣的電路,但「有沒有電」變成由程式決定,LED 就能閃。</p>')

gotchas = section("gotchas", "常見卡關",
  details("LED 不亮",
    ops(["<b>USB 有沒有接上</b>,Uno 上的 <code>ON</code> 燈有沒有亮。",
         "<b>LED 方向</b>:長腳(+)要在靠電阻、接 5V 的那側;短腳(−)才往 GND。",
         "<b>紅線是否插在 5V</b>(Uno 電源排,不是 3.3V、也不是 VIN),<b>黑線是否插在 GND</b>。",
         "<b>零件是否在同一欄</b>:電阻下端與 LED 長腳同在第 6 欄;LED 短腳與黑色短線同在第 7 欄。",
         "<b>你的麵包板電源軌是否中間斷開</b>:若紅線插在左半,電阻卻插在右半,右半沒有電。把零件移到左半,或用跳線把兩半接起來。"]), True) +
  details("LED 很暗",
    "<p>電阻太大。對照色環:<b>紅、紅、棕</b>是 220 Ω;<b>紅、紅、黃</b>是 220 kΩ(大 1000 倍)。用上面的色環計算機確認。</p>") +
  details("零件很燙,或聞到燒焦味",
    "<p><b>立刻拔掉 USB。</b>多半是 5V 與 GND 被短路,或 LED 少了電阻。等零件冷卻後,逐條檢查接線再通電。</p>"))

SIM = {
  "a1": "<b>不行。</b>LED 自己幾乎沒有電阻,5V 直接加上去,電流會超過 LED 能承受的量,LED 很快就會壞,也可能傷到板子。「亮了」不代表安全。",
  "a2": "<b>對。</b>先拔掉 USB 再加電阻。電阻是用來限制電流的保護,一定要有。算法就是歐姆定律:R = (5 − 2.0) ÷ 想要的電流。",
  "a3": "<b>沒有用。</b>電流大小由電壓與電阻決定,換 USB 孔不會改變 LED 與 5V 之間沒有限流電阻這件事。",
}
QUIZ = quiz_cfg([
  ("歐姆定律的式子是?", ["V = I × R", "V = I ÷ R", "R = V × I"], 0,
   "電壓 = 電流 × 電阻,所以 I = V ÷ R、R = V ÷ I。"),
  ("5 V 電源、LED 壓降 2 V,要讓電流約 10 mA,電阻大約要?", ["30 Ω", "300 Ω", "3000 Ω"], 1,
   "電阻承擔 3 V,R = 3 ÷ 0.01 = 300 Ω,取接近且不小於它的標準值 330 Ω。"),
  ("色環「棕、黑、橙、金」是多少歐姆?", ["10 kΩ", "100 Ω", "13 Ω"], 0,
   "1、0,再乘 1000(橙色),= 10000 Ω = 10 kΩ。金色是 ±5% 的誤差環。"),
  ("麵包板同一欄 a–e 五個孔的關係?", ["各自獨立", "內部相通", "只有 a 與 e 相通"], 1,
   "同一欄 a–e 相通,f–j 是另一組。"),
  ("LED 的電路少接了 GND 那條線,會怎樣?", ["LED 會特別亮", "電流沒有回路,LED 不亮(開路)", "LED 會閃爍"], 1,
   "電流必須繞成完整的圈。圈斷了就是開路,沒有電流。"),
])
practice = section("practice", "動手演練與延伸閱讀",
  '<p class="sub" style="margin-bottom:18px">練習判斷「這樣可以嗎」。理解原因比背數字重要。</p>',
  sim("", "情境:你把 LED 直接接在 5V 與 GND 之間,它亮了", "你應該?",
      [("a1", "可以,反正亮了"), ("a2", "先拔掉 USB,串上一顆電阻"), ("a3", "換一個 USB 孔")]),
  QUIZ_HTML,
  checks(["我能用水管比喻說出電壓、電流、電阻各是什麼。",
          "我知道電路要繞成完整的圈,斷了叫開路,捷徑叫短路。",
          "我會用 V = I × R 算出 LED 要用的電阻。",
          "我能讀懂四環電阻的色環,至少認得 220 Ω 與 10 kΩ。",
          "我知道麵包板同一欄 a–e 相通、電源軌整條相通。",
          "我檢查過我的麵包板電源軌中間有沒有斷開。",
          "我完成了 5V → 電阻 → LED → GND 的電路,LED 會亮。"], "做完之後,對照這張清單"),
  resources([
    ("https://www.arduino.cc/en/Tutorial/Blink", "Blink 教學(含電阻選擇說明)", "Blink · why the resistor matters"),
    ("https://docs.arduino.cc/built-in-examples/basics/Blink/", "Blink 內建範例", "Blink (built-in example)"),
  ], "Arduino 官方文件"))

SPEC = dict(
    dir="arduino",
    file="arduino-electric-guide.html",
    title="電與麵包板基礎",
    eyebrow="第 2 篇 · 電與麵包板",
    h1="電是什麼?把它想成水管,再接出第一個會亮的電路",
    sub="不需要數學基礎。先用水管比喻抓住電壓、電流、電阻,再認識麵包板內部怎麼連,最後接一個不用寫程式、插上 USB 就會亮的電路。",
    tldr="<b>電壓是推力、電流是流量、電阻是阻力</b>,關係是 <code>V = I × R</code>。電流要繞成<strong>完整的一圈</strong>才會流動。麵包板<strong>同一欄 a–e 相通</strong>、電源軌整條相通。LED 的電阻用 <code>R = (5 − 壓降) ÷ 電流</code> 算,本主題用 220 Ω。",
    toc=[("what", "電壓電流電阻"), ("ohm", "歐姆定律"), ("rcode", "色環"), ("board", "麵包板內部"), ("build", "第一個電路"),
         ("gotchas", "常見卡關"), ("practice", "演練與延伸閱讀")],
    body="\n\n".join([what, ohm, rcode, board, build, gotchas, practice]),
    config=dict(sim=SIM, quiz=QUIZ, wiring=[bb.wiring_config(CIRC)], parts=bb.parts_info(CIRC)),
    prev=("arduino-start-guide.html", "認識 Arduino 與第一次上傳"),
    next=("arduino-led-guide.html", "外接 LED 閃爍:第一次接線"),
)
