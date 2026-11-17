import json
from mh import *

EYE = angle(angle="eye", hzline=True, label="平視:鏡頭和眼睛一樣高,地平線穿過角色的眼睛")
HIGH = angle(angle="high", hzline=True, label="俯拍:鏡頭比眼睛高,從上往下看,地平線很高")
LOW = angle(angle="low", hzline=True, label="仰拍:鏡頭比眼睛低,從下往上看,地平線很低")
DUTCH = angle(angle="dutch", expr="fear", label="荷蘭角:整個畫面歪了一邊")
YU_HIGH = angle(angle="high", who="yu", pose="phone", label="俯拍:從樓上往下看低頭看手機的小宇")
AN_LOW = angle(angle="low", who="an", expr="smile", label="仰拍:小安下定決心,看起來很有力量")
AN_DUTCH = angle(angle="dutch", who="an", expr="surprise", label="荷蘭角:小安讀完紙條,整個人愣住")
AN_EYE = angle(angle="eye", who="an", expr="smile", label="平視:兩人面對面,感覺平等")

ANG = [  # key, 中文, 英文, 感覺, 適合, 《紙條》
  ("eye", "平視", "eye level", "平等、自然,像和角色面對面站著。是最常用、最安全的預設角度。", "對話、一般敘事。不確定時,先用平視。", "第 6 段,兩人面對面聊天。"),
  ("high", "俯拍", "high angle", "角色看起來渺小、無助、被看輕,觀眾像在上面看著他。", "角色迷路、失落、被壓力包圍;想讓觀眾看見全貌。", "窗外的小宇低頭看手機,從樓上往下看,他顯得有點孤單。"),
  ("low", "仰拍", "low angle", "角色看起來高大、有力量、有威嚴;有時也會帶來壓迫感。", "角色下定決心、登場、對峙,或讓人害怕的角色。", "小安決定衝下樓的那一刻,她看起來很有決心。"),
  ("dutch", "荷蘭角", "dutch angle", "畫面歪斜,讓人不安、緊張、失去平衡。", "慌亂、恐懼、腦中一片混亂;少量使用才有效。", "小安讀完紙條,愣住的那一瞬間。"),
]

start = section("start", "角度:鏡頭比眼睛高,還是比眼睛低?",
  '<p class="sub" style="margin-bottom:10px">' + lv(1, "跟著做") + '前面學的是鏡頭「離多遠」。這一篇學鏡頭「放多高」。先只記三種:<b>平視、俯拍、仰拍</b>。同一個小安,三種高度,給觀眾的感覺完全不同。</p>',
  figrow(fig(EYE, "<b>平視</b>:和眼睛一樣高。"), fig(HIGH, "<b>俯拍</b>:鏡頭在上面,往下看。"), fig(LOW, "<b>仰拍</b>:鏡頭在下面,往上看。"), cols=3),
  tip("看圖找一個小祕訣:橘色虛線是<b>地平線</b>,它在哪裡,<b>鏡頭就在那個高度</b>。平視時地平線剛好穿過眼睛;俯拍時地平線跑到上面;仰拍時跑到下面。"),
  table("g3", ["角度", "鏡頭位置", "觀眾的感覺"], [
    ["平視", "和角色的眼睛一樣高", "平等、自然"],
    ["俯拍", "比眼睛高,往下拍", "渺小、無助"],
    ["仰拍", "比眼睛低,往上拍", "強大、有威嚴"]]))

lab = section("lab", "互動實驗室:切換角度,看角色的感覺怎麼變",
  '<p class="sub" style="margin-bottom:12px">' + lv(2, "自己改") + '選一個角度、選一個角色,看看右邊的說明。每一種都試一次,再回頭想:你會把哪個角度用在你的故事裡?</p>',
  '''<div class="panel"><div class="lab">
  <div class="stage" id="stage" aria-live="polite"></div>
  <div>
    <div class="grp"><b>角度</b><div class="opts" id="angOpts"></div></div>
    <div class="grp"><b>角色</b><div class="opts" id="whoOpts"><button type="button" data-w="an" class="on">小安</button><button type="button" data-w="yu">小宇</button></div></div>
    <div class="grp"><b>地平線</b><div class="opts" id="hzOpts"><button type="button" data-h="1" class="on">顯示</button><button type="button" data-h="0">隱藏</button></div></div>
  </div></div>
  <div class="info" id="info" aria-live="polite"></div>
  <div class="legend-key" id="seen"></div></div>''')

dutch = section("dutch", "荷蘭角:故意把畫面歪一邊",
  '<p>' + lv(3, "挑戰") + '前三種都是「高低」。荷蘭角不一樣:<b>鏡頭歪了,地平線不再水平</b>,牆和櫃子也跟著傾斜。觀眾會下意識覺得「哪裡怪怪的」。</p>',
  '<div class="sbone">' + fig(DUTCH, "<b>荷蘭角</b>:小安嚇到了,畫面也跟著失去平衡。") + '</div>',
  '<div class="warn"><b class="l">少用</b>荷蘭角很顯眼,<b>用多了會讓觀眾頭暈</b>,也不容易再有效果。一部短片裡用一兩次,留給最不安的那一刻。</div>',
  '<p>《紙條》裡可以用在哪?挑一個「小安腦中一片混亂」的瞬間,畫成下面這樣:</p>',
  figrow(sb(1, AN_EYE, "小安走到置物櫃前。", "腰上景,<b>平視</b>。先用最普通的角度。"), sb(2, AN_DUTCH, "她讀完紙條,愣住了。", "近景,<b>荷蘭角</b>。畫面歪了,觀眾感覺到她的震驚。"), cols=2))

story = section("story", "《紙條》裡的三個角度",
  '<p>同一個故事裡,<b>大部分鏡頭都用平視</b>;只有想特別強調的那一格,才換角度。換了,觀眾就會注意到。</p>',
  figrow(sb(1, YU_HIGH, "窗外,小宇在校門口低頭看手機等人。", "近景,<b>俯拍</b>。從樓上往下看,他有點孤單。"), sb(2, AN_LOW, "小安下定決心,轉身衝下樓。", "近景,<b>仰拍</b>。她看起來很有決心。"), sb(3, AN_EYE, "兩人在校門口面對面,笑了。", "腰上景,<b>平視</b>。回到平等的角度。"), cols=3),
  tip("分鏡的「鏡頭」欄這樣寫:<b>近景,俯拍</b>。景別在前,角度在後;平視是預設,沒有特別要求就可以不寫。"),
  '<div class="warn"><b class="l">不是固定公式</b>俯拍不一定代表弱、仰拍不一定代表強。要看前後的畫面和劇情,角度只是在「幫忙說」這件事。</div>')

pick = section("pick", "你來選角度",
  '<p class="sub" style="margin-bottom:8px">' + lv(2, "自己改") + '讀情境,選最適合的角度。</p>',
  choose([
    dict(q="想讓觀眾覺得小宇一個人站在那裡,有點孤單、很渺小。", opts=["俯拍", "仰拍", "平視"], ans=0, why="鏡頭放高、往下拍,角色會顯得渺小。", pic=YU_HIGH, cap="俯拍"),
    dict(q="想讓小安下定決心的那一刻,看起來很有力量。", opts=["俯拍", "仰拍", "荷蘭角"], ans=1, why="鏡頭放低、往上拍,角色會顯得高大有力。", pic=AN_LOW, cap="仰拍"),
    dict(q="兩人面對面輕鬆聊天,沒有特別要強調什麼。", opts=["平視", "荷蘭角", "仰拍"], ans=0, why="平視最自然、最平等,是對話的預設。", pic=AN_EYE, cap="平視"),
    dict(q="小安讀完紙條,腦中一片混亂,想讓觀眾感覺到不安。", opts=["平視", "荷蘭角", "俯拍"], ans=1, why="畫面歪斜會讓人不安,但要少用。", pic=AN_DUTCH, cap="荷蘭角")]),
  '<div class="panel" style="margin-top:14px"><h3>' + lv(3, "挑戰") + '</h3><p style="margin:0">把<b>同一個動作</b>(小安走到置物櫃前)畫成三格:平視、俯拍、仰拍。比一比,哪一格最像「她有點害怕」?哪一格最像「她很有自信」?</p></div>')

practice = section("practice", "動手演練與檢查",
  sim("", "情境:想讓觀眾覺得角色「被壓力壓得喘不過氣」", "最可能選哪一種角度?",
      [("a1", "仰拍:從下往上看"), ("a2", "俯拍:從上往下看,角色顯得渺小"), ("a3", "平視:和眼睛一樣高")]),
  QUIZ_HTML,
  checks(["我知道角度是鏡頭放得比眼睛高還是低。",
          "我能用「地平線」判斷鏡頭是平視、俯拍還是仰拍。",
          "我能說出三種角度各自給人的感覺。",
          "我知道荷蘭角要少用,留給最不安的瞬間。",
          "我知道大部分鏡頭用平視,想強調時才換角度。",
          "我已把同一個動作用三種角度畫過。"]),
  '<h3 style="margin-top:30px">可自查的延伸閱讀</h3>',
  '<div class="panel"><ul style="margin:0;padding-left:20px"><li>找一部你看過的短片,留意哪一格是俯拍或仰拍,想想導演想讓你怎麼看那個角色。</li><li>用「平視 俯拍 仰拍 荷蘭角」當關鍵字,比較不同來源怎麼解釋它們的心理效果。</li></ul></div>')

SIM = {"a1": "<b>方向反了。</b>仰拍會讓角色顯得高大有力,比較像「他很強」。", "a2": "<b>正確!</b>俯拍讓角色在畫面裡顯得小,像被上面的東西壓著。", "a3": "<b>可以,但效果比較弱。</b>平視很自然,不太會特別傳達「被壓住」的感覺。"}
QUIZ = quiz_cfg([
  ("橘色地平線在畫面很低(接近下緣),代表鏡頭是?", ["俯拍", "仰拍", "平視"], 1, "地平線的位置就是鏡頭的高度。低,代表鏡頭在下面往上看。"),
  ("想讓角色看起來渺小、無助,常用?", ["俯拍", "仰拍", "荷蘭角"], 0, "俯拍讓角色顯得小。"),
  ("荷蘭角的特徵是?", ["鏡頭拉得很遠", "畫面歪斜、地平線不水平", "角色變得很高大"], 1, "畫面歪斜會讓人不安。"),
  ("一般對話場景,最安全的預設角度是?", ["平視", "俯拍", "荷蘭角"], 0, "平視最自然、最平等。"),
  ("為什麼荷蘭角要少用?", ["因為很難畫", "用多了觀眾會頭暈,效果也變弱", "因為它不好看"], 1, "越少用,用的那一格越有力。")])

JS = "<script>\n" + inline_kit() + """
(function () {
  var ANG = __ANG__, st = { a: "eye", w: "an", h: 1 }, seen = {};
  var stage = document.getElementById("stage"), info = document.getElementById("info"), seenEl = document.getElementById("seen");
  var angOpts = document.getElementById("angOpts"), whoOpts = document.getElementById("whoOpts"), hzOpts = document.getElementById("hzOpts");
  angOpts.innerHTML = ANG.map(function (a, i) { return '<button type="button" data-a="' + a[0] + '"' + (i ? "" : ' class="on"') + ">" + a[1] + "</button>"; }).join("");
  function render() {
    var a = ANG.filter(function (x) { return x[0] === st.a; })[0]; seen[st.a] = true;
    stage.innerHTML = Kit.angleShot({ angle: st.a, who: st.w, hzline: !!st.h, expr: st.a === "dutch" ? "fear" : st.a === "eye" ? "smile" : "neutral", label: a[1] + ":" + a[3] });
    info.innerHTML = "<h4>" + a[1] + "<small>" + a[2] + "</small></h4><div><b>觀眾的感覺:</b>" + a[3] + "<br><b>適合用在:</b>" + a[4] + "<br><b>《紙條》:</b>" + a[5] + "</div>";
    seenEl.textContent = "已試過 " + Object.keys(seen).length + " / 4 種角度";
    Array.prototype.forEach.call(angOpts.children, function (b) { b.classList.toggle("on", b.dataset.a === st.a); b.setAttribute("aria-pressed", b.dataset.a === st.a); });
    Array.prototype.forEach.call(whoOpts.children, function (b) { b.classList.toggle("on", b.dataset.w === st.w); b.setAttribute("aria-pressed", b.dataset.w === st.w); });
    Array.prototype.forEach.call(hzOpts.children, function (b) { b.classList.toggle("on", +b.dataset.h === st.h); b.setAttribute("aria-pressed", +b.dataset.h === st.h); });
  }
  angOpts.addEventListener("click", function (e) { var b = e.target.closest("button"); if (b) { st.a = b.dataset.a; render(); } });
  whoOpts.addEventListener("click", function (e) { var b = e.target.closest("button"); if (b) { st.w = b.dataset.w; render(); } });
  hzOpts.addEventListener("click", function (e) { var b = e.target.closest("button"); if (b) { st.h = +b.dataset.h; render(); } });
  render();
})();
</script>""".replace("__ANG__", json.dumps([list(a) for a in ANG], ensure_ascii=False)) + CHOOSE_JS

SPEC = defaults(
  file="microfilm-angle-guide.html",
  title="拍攝角度:平視、俯拍、仰拍、荷蘭角的心理效果",
  eyebrow="第 7 篇 · 拍攝角度",
  h1="角度:鏡頭放得高或低,角色的感覺就不一樣",
  sub="先記平視、俯拍、仰拍三種,再認識故意把畫面歪一邊的荷蘭角,最後在互動實驗室切換角度,親眼看角色的感覺怎麼改變。",
  tldr="<strong>平視</strong>最自然,是預設;<strong>俯拍</strong>讓角色渺小、無助;<strong>仰拍</strong>讓角色強大、有威嚴;<strong>荷蘭角</strong>讓人不安,要少用。看<strong>地平線</strong>就知道鏡頭在哪個高度。",
  toc=[("start", "三種角度"), ("lab", "互動實驗室"), ("dutch", "荷蘭角"), ("story", "《紙條》裡的角度"), ("pick", "你來選角度"), ("practice", "演練與檢查")],
  body="\n\n".join([start, lab, dutch, story, pick, practice]),
  config=dict(sim=SIM, quiz=QUIZ), js=JS,
  prev=("microfilm-relation-shots-guide.html", "關係鏡頭"), next=("microfilm-lens-guide.html", "焦段與景深"),
)
