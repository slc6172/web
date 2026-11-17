from mh import *

# ---------- 圖 ----------
B1 = shot(people=[P(120, 130, pose="walk")], arrows=[A(155, 58, 235, 58, "move")], label="小安背著書包快步走過走廊,黑色實線箭頭指向右邊")
B2 = shot(people=[P(130, 130)], props=[N("note", 176, 60)], label="小安停在置物櫃前,櫃門夾著一張紙條")
B3 = shot(people=[P(130, 130, pose="read", expr="surprise")], label="小安拿著紙條讀,表情驚訝")
B4 = shot(scene="gate", people=[P(200, 130, who="yu", facing="f", pose="phone")], label="小宇在校門口低頭看手機")
B5 = shot(people=[P(110, 130, pose="run")], arrows=[A(150, 58, 240, 58, "move")], label="小安跑向畫面右邊")
B6 = shot(scene="gate", people=[P(120, 130, expr="smile"), P(215, 130, who="yu", facing="l", expr="smile")], props=[N("note", 150, 66)], label="兩人在校門口面對面,笑了")

def beat(n, svg, t): return fig(svg, "<b>%d</b> %s" % (n, t))

what = section("what", "分鏡圖就是先畫好的「拍攝地圖」",
  '<div class="panel"><h3>用漫畫來想</h3>'
  '<p><b>分鏡圖</b>(storyboard)是在拍影片<b>之前</b>,先用一格一格的小圖,把影片會長什麼樣子畫出來。就像漫畫的分格:每一格是一個鏡頭,連起來就是整部影片的拍攝地圖。</p>'
  '<p style="margin-bottom:0"><b>你不需要會畫畫。</b>圓圈當頭、方塊當身體的火柴人就夠了。分鏡的重點是讓別人看懂「這一格要拍什麼」,不是比誰畫得漂亮。</p></div>',
  '<h3 style="margin-top:26px">先認識四個詞</h3>',
  table("g2", ["名詞", "白話說明"], [
    ["劇本", "故事的文字版:誰、在哪裡、做什麼、說什麼。"],
    ["鏡頭(shot)", "攝影機從開始錄到停止,拍到的一段連續畫面。"],
    ["格(panel)", "分鏡圖裡的一個小框,通常對應一個鏡頭。"],
    ["分鏡圖(storyboard)", "把劇本一格一格畫出來的圖,也叫分鏡表。"],
  ]),
  '<h3 style="margin-top:26px">本站的示範劇本:《紙條》</h3>',
  '<p class="sub" style="margin-bottom:6px">接下來每一篇都用同一個很短的故事當例子:兩位同學、兩個地方、六個小段落。先看一遍,有印象就好。</p>',
  figrow(
    beat(1, B1, "放學鐘響,走廊空蕩,小安背著書包快步走。"),
    beat(2, B2, "她停在置物櫃前,看見櫃門縫夾著一張紙條。"),
    beat(3, B3, "她讀紙條,表情從疑惑變驚訝。"),
    beat(4, B4, "窗外,小宇在校門口低頭看手機等人。"),
    beat(5, B5, "小安衝下樓。"),
    beat(6, B6, "兩人在校門口面對面,小安遞出紙條,兩人笑了。"), cols=3))

why = section("why", "為什麼拍之前要先畫?",
  '<p class="sub" style="margin-bottom:14px">因為在紙上改一格只要幾秒鐘,到了現場才發現不對,可能要重拍整段。</p>',
  table("g2", ["好處", "會發生什麼事"], [
    ["改起來很便宜", "發現第 4 格看不清楚小宇的表情?橡皮擦一擦重畫,比現場重拍省很多時間。"],
    ["大家看同一張圖", "導演、攝影、演員不用靠嘴巴猜「你說的那個鏡頭是什麼樣子」。"],
    ["不容易漏拍", "拍的時候照格子一格一格檢查,拍完一格就打勾。"],
  ]))

CARD = sb(1, B1, "小安背著書包,快步走過空蕩蕩的走廊。", "拍到整個人和走廊,鏡頭不動。", mk=True)
one = section("one", "一格分鏡,只有三個欄位",
  '<p class="sub" style="margin-bottom:6px">先記住這張卡片。這個主題裡每一格分鏡,都長這樣。</p>',
  '<div class="sbone">' + CARD + '</div>',
  '<ol class="legend" style="list-style:none">'
  '<li><span class="n">1</span><span><b>畫面</b>:這個鏡頭拍到什麼?人物站哪裡、背景有什麼。(圖左上角的黑圈是這一格的編號。)</span></li>'
  '<li><span class="n">2</span><span><b>動作</b>:人物做了什麼。有台詞就另外寫一行「對白」。</span></li>'
  '<li><span class="n">3</span><span><b>鏡頭</b>:鏡頭怎麼拍。現在先用白話寫「拍多近、鏡頭動不動」就好,專業名稱之後每一篇學一點。</span></li>'
  '</ol>',
  tip("每一格都記得寫編號,討論時才能說「看第 3 格」。"),
  '<h3 style="margin-top:26px">玩玩看:改改文字,卡片會跟著變</h3>',
  '<div class="panel"><div class="ctl">'
  '<div><label for="f-act">動作</label><input id="f-act" autocomplete="off" spellcheck="false" placeholder="例如:小安停下腳步,看向櫃子。"></div>'
  '<div><label for="f-cam">鏡頭</label><input id="f-cam" autocomplete="off" spellcheck="false" placeholder="例如:拍到整個人,鏡頭不動。"></div></div>'
  '<div class="sbone" style="margin-bottom:0">' + sb(1, B1, "小安背著書包,快步走過空蕩蕩的走廊。", "拍到整個人和走廊,鏡頭不動。", ids=("o-act", "o-cam")) + '</div></div>')

read = section("read", "讀一讀:《紙條》前三格",
  '<p class="sub" style="margin-bottom:6px">先不用畫。像讀漫畫一樣,看這三格說了什麼故事。想好答案再打開檢查。</p>',
  sbrow(
    sb(1, B1, "小安背著書包,快步走過走廊。", "拍到整個人和走廊,鏡頭不動。"),
    sb(2, B2, "小安停下腳步,看見櫃門夾著紙條。", "拍到整個人和置物櫃,鏡頭不動。"),
    sb(3, B3, "小安拿著紙條讀,表情變驚訝。", "鏡頭不動。", dial="(小聲)這是…給我的?"), cols=3),
  details("第 2 格比第 1 格多了什麼?為什麼要畫出來?", "多了一張<b>紙條</b>。它是整個故事的關鍵,觀眾得先看到它,後面才看得懂小安為什麼驚訝。"),
  details("第 3 格的小安和第 2 格有什麼不同?", "表情從平靜變成<b>驚訝</b>,而且手上拿著紙條在讀。不用旁白,觀眾從畫面就知道「紙條的內容讓她吃驚」。"),
  details("只看這三格,你猜得到接下來會怎麼發展嗎?", "沒有標準答案。你猜得出來,就代表這三格分鏡<b>有效</b>:它讓看的人跟得上故事。"))

EMPTY = shot(scene="none", label="一個空的橫向長方形框,代表鏡頭看得到的範圍")
DRAW2 = shot(scene="blank", people=[P(160, 130)], label="框裡畫了一個簡單的人物與地面線")
draw = section("draw", "動手畫第 1 格:三步就完成",
  '<p class="sub" style="margin-bottom:10px">拿一張白紙和一支筆(或在手機、平板的畫圖軟體裡)。這一篇只要你完成 Level 1;有信心再挑戰後面兩關。</p>',
  '<p><span class="lv l1">Level 1 · 跟著做</span> 照下面三步,畫出《紙條》的第 1 格。</p>',
  steps(
    step(1, "畫一個框,寫上編號",
         "框就是鏡頭看得到的範圍,框外的東西不會被拍到。",
         ops(["畫一個<b>橫向</b>的長方形,長寬比大約 16:9(跟手機橫拍的畫面差不多)。", "在框的左上角寫「1」。"]),
         '<div class="sbone">' + fig(EMPTY, "", "empty") + "</div>",
         see("一個空框。你之後畫的所有東西,都要放在框裡面。")),
    step(2, "在框裡畫出畫面",
         "「畫面」欄位用圖來說話:誰在哪裡、背景有什麼。",
         ops(["畫一條地面線。", "圓圈當頭、方塊當身體,畫一個人站在框裡。", "背景只畫最重要的一兩樣,例如幾個置物櫃就夠。"]),
         '<div class="sbone">' + fig(DRAW2) + "</div>",
         tip("火柴人完全可以。不確定怎麼畫,就先畫形狀,不要畫細節。")),
    step(3, "在框下面填「動作」與「鏡頭」",
         "只有圖,別人不知道人物在做什麼、鏡頭要怎麼拍;補上兩行字就完整了。",
         ops(["寫「動作:小安背著書包,快步走過走廊。」", "寫「鏡頭:拍到整個人和走廊,鏡頭不動。」"]),
         '<div class="sbone">' + sb(1, B1, "小安背著書包,快步走過走廊。", "拍到整個人和走廊,鏡頭不動。") + "</div>",
         see("一格完整的分鏡:有編號、有畫面、有兩行說明。你的版本和它不一樣也沒關係。"))),
  '<div class="sbrow c2" style="margin-top:22px">'
  '<div class="panel"><h3>' + lv(2, "自己改") + '</h3><p style="margin-bottom:0">選一件你今天做過的小事(例如拿起手機、打開門),用同樣的三步畫成一格。換成自己的題材,才會知道哪些地方不確定。</p></div>'
  '<div class="panel"><h3>' + lv(3, "挑戰") + '</h3><p style="margin-bottom:0">把上面那件小事拆成連續的 <b>3 格</b>(例如:伸手、拿起、看螢幕),請朋友只看圖說出發生了什麼。他說對,就代表你的分鏡有效。</p></div></div>')

K_MOVE = '<svg viewBox="0 0 44 14" aria-hidden="true"><line x1="3" y1="7" x2="35" y2="7" stroke="#3D3D3A" stroke-width="2.4" stroke-linecap="round"/><path d="M33,2 L42,7 L33,12 z" fill="#3D3D3A"/></svg>'
K_CAM = '<svg viewBox="0 0 44 14" aria-hidden="true"><line x1="3" y1="7" x2="35" y2="7" stroke="#D97757" stroke-width="3.4" stroke-linecap="round" stroke-dasharray="6 4"/><path d="M33,2 L42,7 L33,12 z" fill="#D97757"/></svg>'
CAMF = shot(people=[P(110, 130)], arrows=[A(60, 22, 250, 22, "cam")], label="橘色虛線箭頭橫過畫面,代表鏡頭往右移動")
arrows = section("arrows", "兩種箭頭,先學這兩種就夠",
  '<p class="sub" style="margin-bottom:10px">分鏡裡的箭頭,用來告訴別人「什麼東西在動」。它可能是人在動,也可能是鏡頭在動,這兩件事要分清楚。</p>',
  figrow(
    fig(B1, "<b>黑色實線</b>:人物移動。小安從左往右走,<b>鏡頭不動</b>,所以背景不會變。"),
    fig(CAMF, "<b>橘色虛線</b>:鏡頭移動。鏡頭往右移動,小安站著不動,但畫面裡的景會慢慢換。"), cols=2),
  '<div class="legend-key"><span>' + K_MOVE + '人物移動</span><span>' + K_CAM + '鏡頭移動</span></div>',
  tip("箭頭畫在框裡面,指向哪邊,就是往哪邊動(以看畫面的人的左右為準)。推、拉、搖等更細的鏡頭符號,之後各篇會一個一個加進來。"))

practice = section("practice", "動手演練:確認你看得懂分鏡",
  '<div class="sbone">' + fig(B5, "") + '</div>',
  sim("", "情境:你在分鏡裡看到一條黑色實線箭頭,從小安指向右邊", "這是什麼意思?",
      [("a1", "小安往右跑"), ("a2", "鏡頭往右移動"), ("a3", "小安在看右邊")]),
  QUIZ_HTML,
  checks(["我能用一句話說出分鏡圖是什麼。",
          "我知道一格分鏡有三個欄位:畫面、動作、鏡頭。",
          "我分得出黑色實線(人物移動)和橘色虛線(鏡頭移動)。",
          "我知道分鏡不用畫得漂亮,火柴人也可以。",
          "我已經在紙上畫出自己的第 1 格。"]),
  '<h3 style="margin-top:30px">可自查的延伸閱讀</h3>',
  '<div class="panel"><ul style="margin:0;padding-left:20px">'
  '<li>用「分鏡表 範本」或「storyboard template」當關鍵字搜尋,看看別人的分鏡表有哪些欄位。</li>'
  '<li>挑一支你喜歡的短片,每看到畫面換了就暫停,畫出前 5 格。你會發現專業影片的鏡頭其實換得很快。</li></ul></div>')

SIM = {
  "a1": "<b>正確!</b>黑色實線是<b>人物移動</b>:小安往右跑。鏡頭沒有動。",
  "a2": "<b>不是。</b>鏡頭移動要用<b>橘色虛線</b>。黑色實線是人物移動。",
  "a3": "<b>不是。</b>這條箭頭表示小安的身體在移動,不是視線。視線方向之後第 2 篇會學怎麼表示。",
}
QUIZ = quiz_cfg([
  ("一格分鏡通常包含哪三個部分?", ["畫面、動作、鏡頭說明", "標題、作者、日期", "顏色、字體、背景音樂"], 0, "畫面說明拍到什麼,動作說明人物做什麼,鏡頭說明怎麼拍。"),
  ("分鏡圖裡的橘色虛線箭頭代表什麼?", ["人物移動", "鏡頭移動", "對白的順序"], 1, "橘色虛線是鏡頭移動;黑色實線才是人物移動。"),
  ("為什麼拍攝前要先畫分鏡?", ["因為老師規定要交", "在紙上發現並修改問題,比現場重拍便宜得多", "因為分鏡畫得好,影片就一定好看"], 1, "分鏡的價值在於先發現問題,不是為了交作業,也不能保證成品好看。"),
  ("畫分鏡一定要畫得很漂亮嗎?", ["要,不然別人看不懂", "不用,火柴人也行,重點是讓別人看懂這一格要拍什麼", "要用彩色筆才算數"], 1, "分鏡是溝通工具,看得懂比畫得好看重要。"),
])

JS = """<script>
(function () {
  var a = document.getElementById("f-act"), c = document.getElementById("f-cam");
  var oa = document.getElementById("o-act"), oc = document.getElementById("o-cam");
  var da = oa.textContent, dc = oc.textContent;
  function up() { oa.textContent = a.value.trim() || da; oc.textContent = c.value.trim() || dc; }
  a.addEventListener("input", up); c.addEventListener("input", up);
})();
</script>"""

SPEC = defaults(
  file="microfilm-storyboard-guide.html",
  title="分鏡圖是什麼、格式與符號:一格只有三個欄位",
  eyebrow="第 1 篇 · 分鏡圖是什麼",
  h1="分鏡圖是什麼:拍之前先畫好的「拍攝地圖」",
  sub="給從來沒拍過影片的你。先弄懂分鏡圖是什麼、一格長什麼樣子,再親手畫出第 1 格。這一篇只要三個欄位和兩種箭頭,其他的之後每一篇再加一點。",
  tldr="分鏡圖是「一格一個鏡頭」的拍攝計畫。每一格只有三個欄位:<strong>畫面、動作、鏡頭</strong>。箭頭先學兩種:<strong>黑色實線</strong>是人物移動,<strong>橘色虛線</strong>是鏡頭移動。不用畫得漂亮,火柴人就行。",
  toc=[("what", "分鏡圖是什麼"), ("why", "為什麼要先畫"), ("one", "一格的三個欄位"), ("read", "讀前三格"), ("draw", "畫第 1 格"), ("arrows", "兩種箭頭"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([what, why, one, read, draw, arrows, practice]),
  config=dict(sim=SIM, quiz=QUIZ),
  js=JS,
  prev=None,
  next=("microfilm-composition-guide.html", "畫面與構圖:比例、三分法、頭上空間、視線空間"),
)
