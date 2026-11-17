from mh import *

def hall(**kw):
    kw.setdefault("people", [P(160, 130)])
    return shot(**kw)

R169 = hall(vb=[0, 0, 320, 180], label="16:9 的橫向畫面,小安站在走廊中間")
R43 = hall(vb=[40, 0, 240, 180], label="4:3 的畫面,左右比 16:9 窄")
R11 = hall(vb=[70, 0, 180, 180], label="1:1 的正方形畫面")
R916 = hall(vb=[109.4, 0, 101.2, 180], label="9:16 的直向畫面,只拍得到小安和一小段走廊")
C_BAD = shot(people=[P(262, 130, pose="stand")], vb=[0, 0, 320, 180], label="小安貼著右邊緣站,面向右邊,看起來快被畫面切掉")
C_GOOD = shot(people=[P(107, 130)], vb=[0, 0, 320, 180], label="小安站在左邊三分之一的位置,面向右邊,前面有空間")
G0 = shot(people=[P(160, 130)], label="只有畫面,沒有格線")
G1 = shot(people=[P(160, 130)], grid=True, label="畫面加上三分線:橫豎各兩條,共四個交叉點")
G2 = shot(people=[P(107, 130)], grid=True, label="小安站在左邊的三分線上")
H1 = shot(people=[P(160, 130)], vb=[0, 32, 320, 180], headroom=True, label="頭上空間太少:頭頂幾乎貼到畫面上緣")
H2 = shot(people=[P(160, 130)], vb=[0, 16, 320, 180], headroom=True, label="頭上空間剛好")
H3 = shot(people=[P(160, 130)], vb=[0, -30, 320, 180], headroom=True, label="頭上空間太多:人物像被壓在畫面下面")
L1 = shot(people=[P(213, 130)], vb=[0, 16, 320, 180], lookroom=True, label="面向右邊卻站在右邊:視線空間太少")
L2 = shot(people=[P(107, 130)], vb=[0, 16, 320, 180], lookroom=True, label="面向右邊,站在左邊:視線空間夠")

why = section("why", "構圖就是決定「東西放在畫面哪裡」",
  '<p class="sub" style="margin-bottom:6px">同一個人、同一個走廊,放的位置不同,觀眾的感覺就不同。先看兩格:一樣是小安面向右邊,哪一格比較舒服?</p>',
  figrow(fig(C_BAD, "<b>A</b>:貼著右邊緣,又看向右邊。感覺她快要撞出畫面。"), fig(C_GOOD, "<b>B</b>:站在左邊,看向右邊。她前面有空間,感覺比較自然。"), cols=2),
  '<p>你的直覺大概選 B。這一篇就是把這種「直覺」變成幾個你能自己檢查的小規則。<b>先學兩個</b>(比例、三分法),<span class="later">再進一步</span>再學兩個(頭上空間、視線空間)。</p>')

ratio = section("ratio", "規則 1:先決定畫面的比例",
  '<p>' + lv(1, "跟著做") + '畫面的形狀叫<b>比例</b>(寬比高)。常見的有四種,同一個場景放進去,看到的範圍差很多。</p>',
  '<div class="arrow-row">' + fig(R169, "16:9") + fig(R43, "4:3", "ar-43") + fig(R11, "1:1", "ar-11") + fig(R916, "9:16", "ar-916") + '</div>',
  table("g2", ["比例", "常見用途"], [["16:9 橫向", "電腦、電視、影片網站最常見。"], ["4:3", "比較方,老電影與照片常用。"], ["1:1 正方形", "社群貼文常用。"], ["9:16 直向", "手機短影音常用。"]]),
  tip("上面四張是<b>同一個場景、同樣的高度</b>。比例不同,左右(或上下)看得到的範圍就不同。"),
  '<div class="panel"><p style="margin:0"><b>怎麼選?</b>想想「作品要在哪裡看」。微電影多半在電腦或電視上看,用 <b>16:9 橫向</b>最保險。<b>整部片的比例要統一</b>,不要一下橫一下直。本站的示範圖都是 16:9。</p></div>')

STEPS = steps(
  step(1, "畫一個 16:9 的框", "框決定了你能放東西的範圍。", ops(["畫一個橫向長方形(第 1 篇學過)。"]), '<div class="sbone">' + fig(G0, "", "") + "</div>"),
  step(2, "把框切成九等份", "橫的兩條線、直的兩條線,把畫面平均切成三份。", ops(["用尺或目測,畫<b>兩條直線</b>把寬分成三等份。", "再畫<b>兩條橫線</b>把高分成三等份。"]),
       '<div class="sbone">' + fig(G1, "") + "</div>", see("四條線,產生四個交叉點。這就是<b>三分線</b>。")),
  step(3, "把主角放在線上或交叉點附近", "放在線上比放在正中間更自然,也讓旁邊留下空間。", ops(["把小安畫在<b>左邊那條直線</b>上。"]),
       '<div class="sbone">' + fig(G2, "") + "</div>", tip("正中間不是錯,它會讓畫面很穩定、很正式,只是容易呆板。三分法是「好用的起點」,不是法律。")))

thirds = section("thirds", "規則 2:三分法",
  '<p>' + lv(1, "跟著做") + '把畫面橫豎各切成三等份,<b>重要的東西放在線上或交叉點附近</b>,畫面通常更舒服。</p>', STEPS)

more = section("more", "再進一步:頭上空間與視線空間",
  '<p class="sub" style="margin-bottom:6px"><span class="lv l2">Level 2 · 自己改</span>前面兩個規則會了,再加兩個。它們都是「留白」:該留的地方要留夠。</p>',
  '<h3>頭上空間:頭頂到畫面上緣,大約留一個拳頭</h3>',
  figrow(fig(H1, "<b>太少</b>:頭快被切掉,有點壓迫。"), fig(H2, "<b>剛好</b>:大約畫面高度的十分之一。"), fig(H3, "<b>太多</b>:人物縮在畫面下面,感覺小而無力。"), cols=3),
  '<h3 style="margin-top:22px">視線空間:角色看(或走)向哪裡,哪裡就要留空間</h3>',
  figrow(fig(L1, "<b>太少</b>:面向右邊卻貼著右邊緣,像快撞牆。"), fig(L2, "<b>夠</b>:前面有空間,觀眾的視線也跟著往那邊走。"), cols=2),
  tip("兩個規則其實是同一個想法:<b>讓角色「前面」和「上面」有呼吸的空間</b>。故意打破也可以(例如想營造壓迫、被困住的感覺),但要「是你決定的」,不是「忘了」。"))

lab = section("lab", "構圖實驗室:自己動手調",
  '<p class="sub" style="margin-bottom:12px"><span class="lv l3">Level 3 · 挑戰</span>調整下面的選項,讓三個檢查都變成綠色。可以打開或關掉輔助層來比較。</p>',
  '''<div class="panel"><div class="lab">
<div class="stage" id="labStage" aria-live="polite"></div>
<div>
  <div class="grp"><b>人物位置</b><div class="opts" data-k="pos"><button type="button" data-v="107">左邊三分線</button><button type="button" data-v="160">正中間</button><button type="button" data-v="213">右邊三分線</button></div></div>
  <div class="grp"><b>面向</b><div class="opts" data-k="face"><button type="button" data-v="l">向左</button><button type="button" data-v="r">向右</button></div></div>
  <div class="grp"><b>頭上空間</b><div class="opts" data-k="head"><button type="button" data-v="32">太少</button><button type="button" data-v="16">剛好</button><button type="button" data-v="-30">太多</button></div></div>
  <div class="grp"><b>輔助層</b><div class="opts" id="layers"><button type="button" data-t="grid">三分線</button><button type="button" data-t="hr">頭上空間</button><button type="button" data-t="lr">視線空間</button></div></div>
</div></div>
<div class="verdict" id="labVerdict" aria-live="polite"></div></div>''')

practice = section("practice", "動手演練:確認你看得懂構圖",
  sim("", "情境:小安面向左邊,你把她放在畫面左邊的三分線上", "這個構圖有什麼問題?",
      [("a1", "沒問題,三分法就是放在三分線"), ("a2", "視線空間太少:她看向左邊,左邊卻只剩一點空間"), ("a3", "頭上空間不夠")]),
  '<h3 style="margin-top:22px"><span class="lv l2">Level 2 · 自己改</span> 與 <span class="lv l3">Level 3 · 挑戰</span></h3>',
  '<div class="sbrow c2"><div class="panel"><p style="margin:0">打開你在第 1 篇畫的第 1 格,畫上三分線。把人物移到線上,並檢查他的「前面」和「上面」有沒有留空間。</p></div>'
  '<div class="panel"><p style="margin:0">用同一個動作畫<b>三種構圖</b>:中間、左三分線、右三分線。拿給朋友看,問他覺得哪一格最舒服、為什麼。</p></div></div>',
  QUIZ_HTML,
  checks(["我知道 16:9、9:16 各適合在哪裡看,而且整部片比例要統一。",
          "我能畫出三分線(橫豎各兩條),並指出四個交叉點。",
          "我知道主角放在線上比放在正中間更自然,但正中間也不是錯。",
          "我知道頭上空間大約留畫面高度的十分之一。",
          "我知道角色看向哪裡,哪裡就要留視線空間。",
          "我能在自己的分鏡格裡檢查這四件事。"]),
  '<h3 style="margin-top:30px">可自查的延伸閱讀</h3>',
  '<div class="panel"><ul style="margin:0;padding-left:20px"><li>用「三分法 構圖」或「rule of thirds」當關鍵字,看更多靜態照片的例子。</li><li>暫停一支你喜歡的短片,在螢幕上想像畫三分線,看主角站在哪裡。</li></ul></div>')

SIM = {
  "a1": "<b>不完全對。</b>位置在三分線沒問題,但她<b>面向左邊</b>,左邊卻只剩約三分之一的空間,視線空間太少。要讓她面向右邊,或把她移到右邊三分線。",
  "a2": "<b>正確!</b>角色看向哪裡,哪裡就要留空間。她面向左邊站在左邊,視線空間太少;移到右邊三分線就舒服了。",
  "a3": "<b>不是。</b>題目沒有說頭上空間有問題。這題的重點是她面向左邊、站在左邊。",
}
QUIZ = quiz_cfg([
  ("要在電腦和電視上看的微電影,最保險的比例是?", ["9:16", "16:9", "1:1"], 1, "電腦、電視是橫向螢幕,16:9 最常見。直向 9:16 多用在手機短影音。"),
  ("三分法是把畫面怎麼切?", ["橫豎各切成三等份,共四條線", "切成三個大小不同的區塊", "只切一條中線"], 0, "橫豎各兩條線,把畫面平均切成九格,產生四個交叉點。"),
  ("角色面向右邊,最好把他放在哪裡?", ["右邊緣", "畫面左邊,讓右邊有空間", "一定要正中間"], 1, "視線空間:角色看向的那一側要留空間。"),
  ("頭上空間大約該留多少?", ["越多越好", "完全不留", "大約畫面高度的十分之一"], 2, "太少有壓迫感,太多讓人物顯得小而無力。"),
  ("什麼時候可以故意不遵守這些構圖規則?", ["不行,這是規定", "你想營造特別的感覺(例如壓迫),而且是有意識的決定", "只要懶得調整就可以"], 1, "規則是好用的起點。有意識地打破,才是創作;忘記才是失誤。"),
])

JS = "<script>\n" + inline_kit() + """
(function () {
  var st = { pos: 213, face: "r", head: 16, grid: true, hr: true, lr: true };
  var stage = document.getElementById("labStage"), vd = document.getElementById("labVerdict");
  function render() {
    var p = { x: st.pos, y: 130, facing: st.face, who: "an" };
    stage.innerHTML = Kit.shot({ people: [p], vb: [0, st.head, 320, 180], grid: st.grid, headroom: st.hr, lookroom: st.lr, label: "可調整的構圖實驗畫面" });
    var hx = Kit.faceX(p), room = st.face === "r" ? 320 - hx : hx, ht = Kit.headTop(p) - st.head;
    var lookOk = room >= 150, headOk = ht >= 8 && ht <= 30, posOk = st.pos !== 160;
    var rows = [
      posOk ? '<b class="ok">位置:在三分線上</b>,自然舒服。' : '<b>位置:正中間</b>,穩定正式,但容易呆板。(不算錯)',
      lookOk ? '<b class="ok">視線空間:夠</b>,角色前面有空間可以看。' : '<b class="no">視線空間:太少</b>,角色好像快撞到畫面邊緣。',
      headOk ? '<b class="ok">頭上空間:剛好</b>。' : (ht < 8 ? '<b class="no">頭上空間:太少</b>,頭頂快被切掉。' : '<b class="no">頭上空間:太多</b>,人物縮在畫面下面。')
    ];
    vd.innerHTML = rows.join("<br>") + (posOk && lookOk && headOk ? '<br><b class="ok">三項都達標!這就是一個很穩的構圖。</b>' : "");
  }
  function sync() {
    Array.prototype.forEach.call(document.querySelectorAll(".lab .opts[data-k]"), function (g) {
      Array.prototype.forEach.call(g.querySelectorAll("button"), function (b) {
        var on = String(st[g.dataset.k]) === b.dataset.v; b.classList.toggle("on", on); b.setAttribute("aria-pressed", on);
      });
    });
    Array.prototype.forEach.call(document.querySelectorAll("#layers button"), function (b) {
      var on = st[b.dataset.t]; b.classList.toggle("on", on); b.setAttribute("aria-pressed", on);
    });
  }
  Array.prototype.forEach.call(document.querySelectorAll(".lab .opts[data-k]"), function (g) {
    g.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      var k = g.dataset.k, v = b.dataset.v; st[k] = (k === "face") ? v : +v; sync(); render();
    });
  });
  document.getElementById("layers").addEventListener("click", function (e) {
    var b = e.target.closest("button"); if (!b) return; st[b.dataset.t] = !st[b.dataset.t]; sync(); render();
  });
  sync(); render();
})();
</script>"""

SPEC = defaults(
  file="microfilm-composition-guide.html",
  title="畫面與構圖:比例、三分法、頭上空間、視線空間",
  eyebrow="第 2 篇 · 畫面與構圖",
  h1="構圖:先學比例和三分法,再學「留空間」",
  sub="同一個人、同一個走廊,放的位置不同,感覺就不同。先學兩個最好用的規則,再加兩個「留白」的小規則,最後在互動實驗室裡自己調。",
  tldr="<strong>比例</strong>先定好(微電影多用 16:9 橫向)→ <strong>三分法</strong>把主角放在線上 → 頭上留約十分之一的<strong>頭上空間</strong> → 角色看向哪,哪裡就留<strong>視線空間</strong>。規則是好用的起點,有意識才能打破。",
  toc=[("why", "為什麼要構圖"), ("ratio", "比例"), ("thirds", "三分法"), ("more", "頭上與視線空間"), ("lab", "構圖實驗室"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([why, ratio, thirds, more, lab, practice]),
  config=dict(sim=SIM, quiz=QUIZ),
  js=JS,
  prev=("microfilm-storyboard-guide.html", "分鏡圖是什麼、格式與符號"),
  next=("microfilm-shot-size-guide.html", "景別總覽:大遠景到大特寫"),
)
