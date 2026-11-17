import json
from mh import *

def box(vb, fill, op):
    return '<rect x="%s" y="%s" width="%s" height="%s" fill="%s" opacity="%s"/>' % (vb[0] - 5, vb[1] - 5, vb[2] + 10, vb[3] + 10, fill, op)

def H(code, who="an", pose="stand", expr="neutral", facing="r", x=600, arrows=None, tint=None, cx=600, people=None, props=None):
    z = SZ[code]; vb = vbfor(z[1], z[2], cx)
    d = dict(worldW=1200, people=people or [P(x, 130, who=who, pose=pose, expr=expr, facing=facing)], vb=vb)
    if arrows: d["arrows"] = arrows
    if props: d["props"] = props
    if tint: d["extra"] = box(vb, *tint)
    return d

def G(people, vb, tint=None, **kw):
    d = dict(scene="gate", people=people, vb=vb); d.update(kw)
    if tint: d["extra"] = box(vb, *tint)
    return d

VB2 = vbfor(78, 62, 160); CU = [103, 20, 114, 64]; MSV = [91, 30.5, 138.7, 78]
DARK = ("#141413", .38); SEPIA = ("#E3DACC", .5)
SCENES = [
 dict(id="talk", name="對話", sit="兩個人坐著或站著聊天,沒有特別的情緒起伏。", rule="先交代位置,再用正反打輪流拍說話的人。",
  shots=[dict(f=G([P(120,130,expr="smile"),P(200,130,who="yu",facing="l",expr="smile")],[44,17,231,130]), size="全景(雙人)", angle="平視", move="固定", why="先讓觀眾知道兩人在哪、什麼關係。"),
         dict(f=G([P(225,130,who="yu",facing="f",expr="smile",h=92),P(36,190,facing="b",h=175)],[0,0,320,180]), size="過肩", angle="平視", move="固定", why="站在小安旁邊,看小宇說話。"),
         dict(f=G([P(95,130,facing="f",expr="smile",h=92),P(284,190,who="yu",facing="b",h=175)],[0,0,320,180]), size="過肩", angle="平視", move="固定", why="換邊,看小安回應(記得不要跨過軸線)。")]),
 dict(id="chase", name="追逐", sit="小安拼命往前跑,有人(或時間)在追她。", rule="動作要看清楚,畫面要有速度與不穩定感。",
  shots=[dict(f=H("fs",pose="run",arrows=[A(640,55,720,55,"move")]), size="全景", angle="平視", move="跟拍", why="看清楚整個奔跑的動作,鏡頭跟著跑。"),
         dict(f=H("mcu",pose="run",expr="fear"), size="近景", angle="平視", move="手持", why="拉近到表情,手持的晃動增加慌張。"),
         dict(f=H("ls",pose="run",arrows=[A(650,70,820,70,"move")]), size="遠景", angle="平視", move="固定", why="拉遠,看她跑向哪裡、離目標多遠。")]),
 dict(id="love", name="告白", sit="其中一個人鼓起勇氣說出心裡的話。", rule="慢下來、靠近,把注意力放在表情與反應。",
  shots=[dict(f=G([P(120,130,expr="neutral"),P(200,130,who="yu",facing="l",expr="neutral")],[44,17,231,130]), size="腰上景(雙人)", angle="平視", move="固定", why="先看到兩人面對面的距離。"),
         dict(f=G([P(160,130,expr="puzzled")],CU), size="特寫", angle="平視", move="緩慢推近", why="說的人很緊張,慢慢靠近他的臉。"),
         dict(f=G([P(160,130,who="yu",facing="f",expr="smile")],CU), size="特寫", angle="平視", move="固定", why="切到聽的人,這就是反應鏡頭,答案在他臉上。")]),
 dict(id="fear", name="恐懼", sit="空蕩蕩的走廊,小安覺得有什麼東西在後面。", rule="讓畫面不安、讓觀眾看不到全貌。",
  shots=[dict(f=dict(H("ls",x=420),extra=box(vbfor(300,60,600),*DARK)), size="遠景", angle="平視", move="固定", why="空間很大、人很小,感覺沒人能幫她。"),
         dict(f=dict(H("mcu",expr="fear"),extra=box(vbfor(46.7,52.7,600),*DARK)), size="近景", angle="平視", move="手持", why="靠近她驚慌的臉,晃動讓觀眾跟著不安。"),
         dict(f=dict(H("ecu",expr="fear"),extra=box(vbfor(14,47.5,600),*DARK)), size="大特寫", angle="平視", move="固定", why="只看到眼睛,觀眾也不敢看全貌。")]),
 dict(id="fight", name="衝突", sit="兩個人意見不同,越吵越兇。", rule="縮短距離、加快節奏,讓兩人像在對撞。",
  shots=[dict(f=G([P(120,130,expr="angry"),P(200,130,who="yu",facing="l",expr="angry")],[44,17,231,130]), size="全景(雙人)", angle="平視", move="固定", why="先看見兩人劍拔弩張的距離。"),
         dict(f=G([P(160,130,expr="angry")],MSV), size="近景", angle="平視", move="手持", why="靠近的臉加上晃動,增加衝突感。"),
         dict(f=G([P(160,130,who="yu",facing="f",expr="angry")],MSV), size="近景", angle="平視", move="手持", why="換對方,同樣的拍法,保持對稱。")]),
 dict(id="alone", name="孤獨", sit="小安一個人待在很大的空間裡,沒有人陪她。", rule="讓人物很小、空間很大,畫面保持安靜。",
  shots=[dict(f=H("els",x=600), size="大遠景", angle="平視", move="固定", why="人只是一個小點,孤單最明顯。"),
         dict(f=H("ls",expr="sad",x=600), size="遠景", angle="俯拍", move="緩慢拉開", why="俯拍加慢慢拉開,她越來越小。"),
         dict(f=H("cu",expr="sad"), size="特寫", angle="平視", move="固定", why="最後靠近她的臉,安靜地看她的心情。")]),
 dict(id="memory", name="回憶", sit="小安想起以前的事,畫面進入過去。", rule="用和現在不同的質感,讓觀眾分辨這是過去。",
  shots=[dict(f=G([P(160,130,expr="smile")],CU,tint=SEPIA), size="特寫", angle="平視", move="緩慢推近", why="先靠近她的臉,像進入回憶。"),
         dict(f=dict(props=[N("note",176,60,1)],people=[],vb=[160,52,54,30.4],extra=box([160,52,54,30.4],*SEPIA)), size="大特寫(插入)", angle="平視", move="固定", why="一個物件,把觀眾帶到過去。"),
         dict(f=G([P(120,130,expr="smile"),P(200,130,who="yu",facing="l",expr="smile")],[44,17,231,130],tint=SEPIA), size="全景(雙人)", angle="平視", move="緩慢拉開", why="回憶裡的畫面,慢慢拉開,有懷念的感覺。")]),
 dict(id="reveal", name="揭露", sit="小安發現了一個一直不知道的事實。", rule="先藏、再讓觀眾和角色一起發現。",
  shots=[dict(f=G([P(160,130,expr="puzzled")],MSV), size="腰上景", angle="平視", move="固定", why="先看她的疑惑。"),
         dict(f=G([P(200,130,who="yu",facing="f",pose="phone")],[100,20,190,107],extra=win_frame([100,20,190,107])), size="主觀(POV)", angle="平視", move="搖攝到他身上", why="鏡頭轉過去,觀眾和她一起發現小宇在那裡。"),
         dict(f=G([P(160,130,expr="surprise")],CU), size="特寫", angle="平視", move="固定", why="回到她的臉,看她的驚訝。")]),
]
for s in SCENES:
    for k in s["shots"]:
        k["f"] = dict(k["f"]); k["f"].setdefault("label", s["name"] + ":" + k["size"])

OVERVIEW = table("g3", ["情節", "一句建議", "常用的鏡頭"], [[s["name"], s["rule"], "、".join(k["size"].split("(")[0] for k in s["shots"])] for s in SCENES])

start = section("start", "先問三個問題,再選鏡頭",
  '<p class="sub" style="margin-bottom:10px">' + lv(1, "先讀這段") + '前面學了景別、角度、焦段、運鏡,現在要把它們<b>用起來</b>。遇到一場戲,不知道怎麼拍,就依序問自己:</p>'
  '<div class="panel"><ol style="margin:0;padding-left:22px;line-height:1.9"><li><b>觀眾這一格要感覺到什麼?</b>(緊張、孤單、溫暖、疑惑……)</li><li><b>要讓觀眾看到什麼?</b>(環境、動作、表情、物件)→ 選<b>景別</b>(第 3–6 篇)</li><li><b>要不要加強感受?</b> → 選<b>角度</b>(第 7 篇)與<b>運鏡</b>(第 9–12 篇)</li></ol></div>',
  OVERVIEW,
  tip("下面八種情節的建議,都是<b>常見的起點,不是標準答案</b>。同一場戲有很多拍法;重點是你能說出「為什麼這樣拍」。"))

lab = section("lab", "選一種情節,看建議與理由",
  '<p class="sub" style="margin-bottom:12px">' + lv(2, "自己改") + '點一種情節,看建議的三格鏡頭與理由。先<b>自己想一想</b>你會怎麼拍,再點開比一比。</p>',
  '<div class="panel"><div class="fx" id="scenePick" role="group" aria-label="選擇情節"></div><div class="info" id="sceneInfo" aria-live="polite"></div><div class="sbrow c3" id="sceneShots"></div><div class="verdict" id="sceneRule"></div></div>')

pick = section("pick", "你來選",
  '<p class="sub" style="margin-bottom:8px">' + lv(3, "挑戰") + '讀情境,選最適合的拍法。</p>',
  choose([
    dict(q="孤獨的場景,想讓人物顯得很小。", opts=["大遠景或遠景", "大特寫", "雙人過肩"], ans=0, why="人物小、空間大,孤單最明顯。"),
    dict(q="告白時,想讓觀眾看見聽的人的反應。", opts=["切到聽的人的特寫", "一直拍說話的人", "拍遠景"], ans=0, why="反應鏡頭讓答案出現在臉上。"),
    dict(q="追逐戲,想增加慌張與真實感。", opts=["手持加跟拍", "固定不動的大遠景", "環繞"], ans=0, why="跟拍加手持,觀眾像在一起跑。"),
    dict(q="回憶的畫面,想和現在區隔。", opts=["換一種顏色質感、動作放慢", "跟現在完全一樣", "只用大特寫"], ans=0, why="質感不同,觀眾才知道是過去。")]),
  '<div class="panel" style="margin-top:14px"><h3>' + lv(3, "挑戰") + '</h3><p style="margin:0">選一種你沒看過的情節(例如「驚喜」「道別」),自己畫三格,並在每一格寫下<b>「景別、角度、運鏡、為什麼」</b>。</p></div>')

practice = section("practice", "動手演練與檢查",
  sim("", "情境:小安發現紙條上的字,觀眾也要和她一起「發現」", "最適合的做法?",
      [("a1", "近景加推,再切到紙條的插入鏡頭"), ("a2", "一直拍遠景"), ("a3", "只拍背影")]),
  QUIZ_HTML,
  checks(["我知道選鏡頭先問:觀眾要感覺什麼、要看到什麼。",
          "我能說出至少五種情節各自常用的景別。",
          "我知道這些建議是起點,不是唯一答案。",
          "我能替一格分鏡說出「為什麼這樣拍」。",
          "我已自己畫過一種情節的三格。"]),
  '<h3 style="margin-top:30px">可自查的延伸閱讀</h3>',
  '<div class="panel"><ul style="margin:0;padding-left:20px"><li>看一支短片,挑一個情緒場景,寫下它用了哪些景別、角度、運鏡,再想想為什麼。</li></ul></div>')

SIM = {"a1": "<b>很適合!</b>近景加推帶觀眾靠近她,再用插入鏡頭讓大家看清紙條。", "a2": "<b>不太對。</b>遠景看不到她的表情,觀眾無法「一起發現」。", "a3": "<b>可以,但資訊太少。</b>背影看不到她的反應。"}
QUIZ = quiz_cfg([
  ("選鏡頭時,第一個要問什麼?", ["觀眾這一格要感覺到什麼", "用哪個品牌的器材", "要拍多久"], 0, "先想感受,再選景別、角度與運鏡。"),
  ("想讓觀眾看見聽的人的反應,用?", ["反應鏡頭", "大遠景", "空拍"], 0, "切到聽的人。"),
  ("孤獨的場景常用?", ["遠景或大遠景", "大特寫", "快速環繞"], 0, "人物小、空間大。"),
  ("這些情節的建議是?", ["常見的起點,不是標準答案", "唯一正確答案", "不能改"], 0, "你可以有自己的拍法,但要說得出理由。")])

JS = "<script>\n" + inline_kit() + """
(function () {
  var S = __S__, pick = document.getElementById("scenePick"), info = document.getElementById("sceneInfo"), shots = document.getElementById("sceneShots"), rule = document.getElementById("sceneRule");
  pick.innerHTML = S.map(function (s, i) { return '<button type="button" data-i="' + i + '"' + (i ? "" : ' class="on"') + ">" + s.name + "</button>"; }).join("");
  function show(i) {
    var s = S[i];
    info.innerHTML = "<h4>" + s.name + "</h4><div>" + s.sit + "</div>";
    shots.innerHTML = s.shots.map(function (k, j) {
      return '<figure class="sb"><div class="sb-pic"><span class="sb-n">' + (j + 1) + "</span>" + Kit.shot(k.f) + '</div><figcaption><div><b>鏡頭</b><span>' + k.size + "，" + k.angle + "，" + k.move + "</span></div><div><b>為什麼</b><span>" + k.why + "</span></div></figcaption></figure>";
    }).join("");
    rule.innerHTML = "<b>這場戲的重點:</b>" + s.rule;
    Array.prototype.forEach.call(pick.children, function (b) { b.classList.toggle("on", +b.dataset.i === i); b.setAttribute("aria-pressed", +b.dataset.i === i); });
  }
  pick.addEventListener("click", function (e) { var b = e.target.closest("button"); if (b) show(+b.dataset.i); });
  show(0);
})();
</script>""".replace("__S__", json.dumps(SCENES, ensure_ascii=False)) + CHOOSE_JS

SPEC = defaults(
  file="microfilm-scenes-guide.html",
  title="情節配鏡頭速查:對話、追逐、告白、恐懼、衝突、孤獨、回憶、揭露",
  eyebrow="第 14 篇 · 情節配鏡頭速查",
  h1="情節配鏡頭:不知道怎麼拍時,先問觀眾要感覺什麼",
  sub="把前面學的景別、角度、運鏡全部用起來。八種常見情節,每一種都有三格建議鏡頭與理由,可以點著看,也可以拿來改成自己的拍法。",
  tldr="選鏡頭先問:<strong>觀眾要感覺到什麼</strong>?再決定<strong>景別</strong>(看什麼),最後用<strong>角度與運鏡</strong>加強感受。八種情節的建議是<strong>起點,不是標準答案</strong>;重點是你說得出理由。",
  toc=[("start", "三個問題"), ("lab", "選情節看建議"), ("pick", "你來選"), ("practice", "演練與檢查")],
  body="\n\n".join([start, lab, pick, practice]),
  config=dict(sim=SIM, quiz=QUIZ), js=JS,
  prev=("microfilm-continuity-guide.html", "軸線與連戲"), next=("microfilm-practice-guide.html", "實作:把劇本畫成分鏡"),
)
