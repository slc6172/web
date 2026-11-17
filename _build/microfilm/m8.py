import json
from mh import *

W1 = lens(D=1.3, F=1.3, label="廣角:小安一樣大,背後看到很多東西,盆栽變大、後面的人變小")
W2 = lens(D=2.6, F=2.6, blur=.35, label="標準:接近眼睛平常看到的樣子")
W3 = lens(D=5.5, F=5.5, blur=1, label="望遠:小安一樣大,背景看起來被拉近,而且變模糊")
SHARP = lens(D=3.2, F=3.2, blur=0, label="景深深:前後都清楚")
SOFT = lens(D=3.2, F=3.2, blur=1.2, label="景深淺:只有小安清楚,前後都模糊")
HALL = lens(D=1.3, F=1.3, face="r", pose="walk", yu=False, near=False, zw=6, label="廣角:走廊看起來又深又長")
GATE = lens(D=5.5, F=5.5, blur=1.2, who="yu", pose="phone", near=False, label="望遠加淺景深:小宇孤零零地站在模糊的背景前")
FEEL = [  # 代號, 中文, 看到的範圍, 遠近感, 背景, 適合
  ("wide", "廣角", "看到的範圍很寬,背景東西很多。", "近的東西變大、遠的東西變小,空間顯得又深又長。", "通常整個畫面都很清楚。", "交代環境、讓空間有深度、動作很大的場面。"),
  ("std", "標準", "和眼睛平常看到的差不多。", "遠近比例自然,不誇張。", "背景有一點點柔。", "一般敘事、對話。不知道選什麼時,先用它。"),
  ("tele", "望遠", "看到的範圍窄,只拍到一小塊。", "遠近被「壓」在一起,背景看起來離人很近。", "通常背景更容易模糊。", "想讓人物從背景中跳出來、營造孤立或專注的感覺。"),
]

start = section("start", "焦段:鏡頭「看」得寬還是窄?",
  '<p class="sub" style="margin-bottom:10px">' + lv(1, "跟著做") + '第 3 篇用「離多遠」決定景別。這一篇換一種方式:<b>人物拍得一樣大,但鏡頭看得寬或窄</b>。看得寬叫<b>廣角</b>,看得窄叫<b>望遠</b>,中間是<b>標準</b>。這一篇只看畫面怎麼變,不用記任何數字。</p>',
  figrow(fig(W1, "<b>廣角</b>:前面的盆栽變大,後面的小宇變小,背景很清楚。"), fig(W2, "<b>標準</b>:和平常用眼睛看差不多。"), fig(W3, "<b>望遠</b>:小宇看起來離小安很近,背景變模糊。"), cols=3),
  details("先看畫面:這三張的哪裡不一樣?(動動腦再打開)", "<b>小安一樣大</b>,但:① 左邊的盆栽,廣角時最大、望遠時最小。② 後面的小宇,廣角時最小、望遠時最大。③ 背景的櫃子,廣角時又小又多,望遠時又大又少,而且變模糊。這就是焦段改變的是「<b>遠近感</b>」和「<b>背景</b>」。"),
  table("g3", ["", "廣角", "望遠"], [
    ["看到的範圍", "寬,東西多", "窄,東西少"],
    ["遠近感", "拉開,空間深", "壓縮,前後靠近"],
    ["背景", "通常很清楚", "通常比較模糊"]]))

lab = section("lab", "互動實驗室:拉滑桿,從廣角變望遠",
  '<p class="sub" style="margin-bottom:12px">' + lv(2, "自己改") + '拉動滑桿。小安的大小不會變,<b>注意盆栽、小宇、背景櫃子</b>怎麼變。再按「背景模糊」開關,看看差別。</p>',
  '''<div class="panel"><div class="lab">
  <div class="stage" id="stage" aria-live="polite"></div>
  <div>
    <div class="grp"><b>快速選一個</b><div class="opts" id="presets"><button type="button" data-t="0">廣角</button><button type="button" data-t="35">標準</button><button type="button" data-t="100">望遠</button></div></div>
    <div class="grp"><b>背景模糊</b><div class="opts" id="blurOpts"><button type="button" data-b="1" class="on">開</button><button type="button" data-b="0">關</button></div></div>
  </div></div>
  <div class="rng"><span>廣角(看得寬)</span><input type="range" id="tw" min="0" max="100" value="0" aria-label="焦段:廣角到望遠"><span>望遠(看得窄)</span></div>
  <div class="info" id="info" aria-live="polite"></div></div>''')

dof = section("dof", "景深:前後多大範圍是清楚的",
  '<p>' + lv(2, "再多認識") + '「景深」就是畫面裡<b>前後有多深的範圍是清楚的</b>。範圍很大叫「深景深」,範圍很小、只有主角清楚叫「淺景深」。</p>',
  figrow(fig(SHARP, "<b>深景深</b>:前面、中間、後面都清楚。適合想讓觀眾看見環境。"), fig(SOFT, "<b>淺景深</b>:只有小安清楚,前後糊掉。觀眾的眼睛會被帶到她身上。"), cols=2),
  '<div class="panel"><h3>想要淺景深(背景模糊),常見的幾個方向</h3><ul style="margin:0;padding-left:20px"><li>讓人物<b>離背景遠一點</b>(背景越遠越容易糊)。</li><li>讓鏡頭<b>靠近人物</b>一點。</li><li>用比較偏<b>望遠</b>的看法。</li></ul></div>',
  tip("淺景深很好看,但也有代價:<b>背景的資訊變少</b>。想讓觀眾知道「這是哪裡」時,不要糊掉環境。"))

story = section("story", "《紙條》裡怎麼用",
  '<p>廣角和望遠沒有誰比較好,要看<b>這一格想說什麼</b>。</p>',
  figrow(sb(1, HALL, "放學後,小安快步走過走廊。", "全景,<b>廣角</b>。走廊顯得又深又長,更空蕩。"), sb(2, GATE, "校門口,小宇低頭看手機等人。", "近景,<b>望遠、淺景深</b>。背景糊掉,他顯得更孤單。"), cols=2),
  '<div class="warn"><b class="l">提醒</b><b>廣角靠得很近拍臉,臉會被拉得變形</b>(鼻子變大、臉變奇怪),拍人物特寫通常會選不那麼廣的看法。</div>')

pick = section("pick", "你來選焦段",
  '<p class="sub" style="margin-bottom:8px">' + lv(2, "自己改") + '讀情境,選最適合的看法。</p>',
  choose([
    dict(q="想讓走廊看起來又深又長,讓人覺得空蕩蕩。", opts=["廣角", "望遠", "都可以"], ans=0, why="廣角會拉開遠近感,空間顯得更深。", pic=HALL, cap="廣角"),
    dict(q="想讓小宇從背景裡「跳出來」,背景模糊不搶戲。", opts=["廣角、背景全清楚", "望遠加淺景深", "標準、深景深"], ans=1, why="望遠加淺景深,背景糊掉,觀眾只看人。", pic=GATE, cap="望遠加淺景深"),
    dict(q="想讓觀眾清楚看到「這是校門口、旁邊有哪些東西」。", opts=["深景深", "淺景深", "背景全部糊掉"], ans=0, why="深景深讓前後都清楚,環境資訊最多。", pic=SHARP, cap="深景深"),
    dict(q="一般兩人聊天,沒有特別要強調什麼,先選哪個?", opts=["標準", "很誇張的廣角", "很誇張的望遠"], ans=0, why="標準最自然,不容易出問題。", pic=W2, cap="標準")]),
  '<div class="panel" style="margin-top:14px"><h3>' + lv(3, "挑戰") + '</h3><p style="margin:0">把《紙條》第 4 段(小宇等人)畫成<b>兩格</b>:一格廣角、背景清楚,一格望遠、背景模糊。比一比,哪一格更像「他等得很孤單」?</p></div>')

practice = section("practice", "動手演練與檢查",
  sim("", "情境:你想讓觀眾覺得小安在空蕩蕩的學校裡,整個人好小", "你會選哪種看法?",
      [("a1", "廣角:空間又深又長,人顯得小"), ("a2", "望遠加淺景深:背景全糊"), ("a3", "大特寫:只拍眼睛")]),
  QUIZ_HTML,
  checks(["我知道焦段是鏡頭「看得寬或窄」,不是離多遠。",
          "我能說出廣角、標準、望遠各自的遠近感。",
          "我知道廣角常讓空間顯得深,望遠常把前後「壓」在一起。",
          "我知道景深是前後多大範圍是清楚的。",
          "我知道淺景深能讓主角跳出來,但背景資訊會變少。",
          "我已把同一格用廣角和望遠各畫一次。"]),
  '<h3 style="margin-top:30px">可自查的延伸閱讀</h3>',
  '<div class="panel"><ul style="margin:0;padding-left:20px"><li>用你手邊的任何相機,在同一個位置拍同一個人,一次看得寬、一次看得窄,比較背景。</li><li>用「廣角 望遠 透視壓縮 景深」當關鍵字,看不同來源怎麼說明。</li></ul></div>')

SIM = {"a1": "<b>正確!</b>廣角讓空間顯得又深又長,人物在裡面就顯得很小。", "a2": "<b>不太對。</b>背景全糊,空間感反而不見了,觀眾看不出「空蕩蕩的學校」。", "a3": "<b>不適合。</b>大特寫只看到眼睛,看不到環境,無法表現「整個人好小」。"}
QUIZ = quiz_cfg([
  ("焦段改變的是什麼?", ["鏡頭看得寬還是窄", "畫面的顏色", "影片的長度"], 0, "廣角看得寬,望遠看得窄。"),
  ("「望遠」常帶來的效果是?", ["前後距離被壓縮、背景比較模糊", "空間被拉得很深", "人物變得很小"], 0, "望遠把前後壓在一起,背景通常比較模糊。"),
  ("「景深」指的是?", ["畫面的明暗", "前後多大範圍是清楚的", "鏡頭的顏色"], 1, "範圍大是深景深,範圍小是淺景深。"),
  ("想讓背景模糊、人物跳出來,常見的方向是?", ["讓人物離背景遠一點、靠近一點拍", "讓人物貼著牆", "把畫面調暗"], 0, "背景離得越遠越容易糊,靠近拍也有幫助。"),
  ("廣角靠很近拍臉,常會怎樣?", ["臉被拉得變形", "臉變得很清楚", "背景消失"], 0, "近距離廣角會讓臉變形,所以拍臉通常不選太廣。")])

JS = "<script>\n" + inline_kit() + """
(function () {
  var FEEL = __FEEL__, stage = document.getElementById("stage"), info = document.getElementById("info"), tw = document.getElementById("tw");
  var presets = document.getElementById("presets"), blurOpts = document.getElementById("blurOpts"), st = { t: 0, b: 1 };
  function kind(t) { return t < 18 ? 0 : t < 62 ? 1 : 2; }
  function render() {
    var t = st.t / 100, D = 1.3 + 4.2 * t, f = FEEL[kind(st.t)];
    stage.innerHTML = Kit.lens({ D: D, F: D, blur: st.b ? t * 1.1 : 0, label: f[1] + ":" + f[3] });
    info.innerHTML = "<h4>" + f[1] + "</h4><div><b>看到的範圍:</b>" + f[2] + "<br><b>遠近感:</b>" + f[3] + "<br><b>背景:</b>" + f[4] + "<br><b>適合:</b>" + f[5] + "</div>";
    tw.value = st.t;
    Array.prototype.forEach.call(blurOpts.children, function (b) { b.classList.toggle("on", +b.dataset.b === st.b); b.setAttribute("aria-pressed", +b.dataset.b === st.b); });
    Array.prototype.forEach.call(presets.children, function (b) { var on = kind(st.t) === kind(+b.dataset.t); b.classList.toggle("on", on); b.setAttribute("aria-pressed", on); });
  }
  tw.addEventListener("input", function () { st.t = +tw.value; render(); });
  presets.addEventListener("click", function (e) { var b = e.target.closest("button"); if (b) { st.t = +b.dataset.t; render(); } });
  blurOpts.addEventListener("click", function (e) { var b = e.target.closest("button"); if (b) { st.b = +b.dataset.b; render(); } });
  render();
})();
</script>""".replace("__FEEL__", json.dumps([list(f) for f in FEEL], ensure_ascii=False)) + CHOOSE_JS

SPEC = defaults(
  file="microfilm-lens-guide.html",
  title="焦段與景深:廣角、標準、望遠的透視與背景模糊",
  eyebrow="第 8 篇 · 焦段與景深",
  h1="焦段與景深:同樣大的人,背景卻可以完全不同",
  sub="這一篇不用記數字,只看畫面:廣角把空間拉開,望遠把前後壓緊;景深決定背景是清楚還是模糊。拉滑桿就能親眼看見。",
  tldr="<strong>廣角</strong>看得寬、空間深;<strong>望遠</strong>看得窄、前後被壓縮、背景常模糊;<strong>標準</strong>最自然。<strong>景深</strong>是前後多大範圍清楚:淺景深讓主角跳出來,深景深讓環境看得清。",
  toc=[("start", "廣角與望遠"), ("lab", "互動實驗室"), ("dof", "景深"), ("story", "《紙條》裡怎麼用"), ("pick", "你來選焦段"), ("practice", "演練與檢查")],
  body="\n\n".join([start, lab, dof, story, pick, practice]),
  config=dict(sim=SIM, quiz=QUIZ), js=JS,
  prev=("microfilm-angle-guide.html", "拍攝角度"), next=("microfilm-pan-tilt-guide.html", "固定與搖攝"),
)
