import json
from mh import *

# 景別預設:(代號, 中文, 英文縮寫, H, cy, 拍到哪裡, 常用來)。人物 x=600, 腳底 y=130, 身高 100。
SZ = [
  ("els", "大遠景", "ELS", 520, 70, "人物只是小小一點,環境才是主角。", "交代地點、營造渺小或孤獨的感覺。"),
  ("ls", "遠景", "LS", 300, 60, "看得到整個人,也看得到大片環境。", "交代人在哪裡、和環境的關係。"),
  ("fs", "全景", "FS", 140, 82, "從頭到腳整個人,剛好撐滿畫面。", "看清楚全身的動作與姿勢。"),
  ("mls", "膝上景", "MLS", 87, 68.8, "拍到膝蓋以上。", "走路、互動的動作;同時還看得到表情。"),
  ("ms", "腰上景", "MS", 64.4, 59.8, "拍到腰部以上(也叫中景)。", "對話最常用,動作與表情都照顧到。"),
  ("mcu", "近景", "MCU", 46.7, 52.7, "拍到胸口以上。", "把注意力帶到表情與情緒。"),
  ("bust", "胸上景", "胸像", 33, 47.2, "拍到肩膀以上,頭和肩佔滿畫面。", "更專注在臉,但還保有一點身體語言。"),
  ("cu", "特寫", "CU", 26.7, 44.7, "整張臉。", "強調這一刻的情緒。"),
  ("ecu", "大特寫", "ECU", 14, 47.5, "臉的一小部分(例如眼睛),或物件的細節。", "最強烈的強調;用多了就不稀奇,要省著用。"),
]

def vbfor(H, cy, cx=600):
    w = H * 16 / 9
    return [round(cx - w / 2, 2), round(cy - H / 2, 2), round(w, 2), H]

def view(code, **kw):
    z = next(s for s in SZ if s[0] == code)
    return shot(worldW=1200, people=[P(600, 130)], vb=vbfor(z[3], z[4]), label="%s:%s" % (z[1], z[5]), **kw)

def card(i, code):
    z = next(s for s in SZ if s[0] == code)
    return fig(view(code), "<b>%d. %s</b> <span style=\"font-family:var(--mono);color:var(--gray-500)\">%s</span>" % (i, z[1], z[2]))

why = section("why", "景別 = 人物在畫面裡有多大",
  '<p class="sub" style="margin-bottom:6px">「景別」就是鏡頭離角色多遠:拍得遠,看到整個環境;拍得近,看到臉上的表情。' + lv(1, "跟著做") + '先只記三種:<b>遠、中、近</b>。下面是同一刻的小安,拍成三種大小。</p>',
  figrow(fig(view("ls"), "<b>遠</b>:看到她在哪裡、周圍有什麼。"), fig(view("ms"), "<b>中</b>:看到她在做什麼。"), fig(view("cu"), "<b>近</b>:看到她的表情。"), cols=3),
  details("哪一格最能讓你看清楚小安現在的心情?為什麼?", "通常是<b>近</b>那一格。越靠近,表情越清楚;越遠,越能看到環境與動作。<b>選景別,就是決定「這一格想讓觀眾看什麼」。</b>"),
  tip("同一個人、同一個地方,只是鏡頭離得遠或近,觀眾得到的資訊和感覺就完全不同。這就是分鏡裡「鏡頭」欄位最常寫的內容。"))

ladder = section("ladder", "九種景別,從遠到近",
  '<p class="sub" style="margin-bottom:6px">' + lv(2, "再多認識") + '把「遠中近」再切細,一共九種。同一個人站在同一個位置,只是取景框越縮越小。</p>',
  '<div class="sbrow c3">' + "".join(card(i + 1, z[0]) for i, z in enumerate(SZ)) + "</div>",
  table("g3", ["景別", "拍到哪裡", "常用來"], [["%s <small style=\"font-family:var(--mono);color:var(--gray-500)\">%s</small>" % (z[1], z[2]), z[5], z[6]] for z in SZ]),
  '<div class="warn"><b class="l">叫法會不一樣</b>不同學校、書籍、劇組對這些名稱的叫法略有不同(例如「近景」「中近景」「半身」常被混用)。<b>這個教學站採用上面這張表</b>:以人物身體被「切」在哪裡來定義。你和同學討論時,先說好大家用哪一套就好。</div>')

lab = section("lab", "拖動取景框:自己找出景別",
  '<p class="sub" style="margin-bottom:12px">' + lv(3, "挑戰") + '左邊是一個大場景,小安站在中間。<b>在左圖上拖動取景框</b>(或點一下),用滑桿調大小,右邊就是鏡頭看到的畫面。試著讓它依序變成九種景別。</p>',
  '''<div class="panel">
<div class="duo">
  <div class="box"><b>遠處的大場景(橘框 = 取景框)</b><div class="master" id="master" tabindex="0" role="application" aria-label="大場景。用方向鍵移動取景框,或在畫面上拖動"></div></div>
  <div class="box"><b>鏡頭看到的畫面</b><div id="pre" aria-live="polite"></div></div>
</div>
<div class="rng"><span>框小(近)</span><input type="range" id="size" min="0" max="100" value="46" aria-label="取景框大小"><span>框大(遠)</span></div>
<div class="grp" style="margin-top:10px"><div class="lab"><div class="opts" id="presets" style="grid-column:1/-1"></div></div></div>
<div class="info" id="info" aria-live="polite"></div>
</div>''')

practice = section("practice", "動手演練:選一種景別",
  sim("", "情境:《紙條》第 3 段,小安讀紙條,表情從疑惑變驚訝", "想讓觀眾看清楚她的表情,最適合用哪一種?",
      [("a1", "大遠景:拍整條走廊"), ("a2", "特寫:拍到整張臉"), ("a3", "全景:拍整個人")]),
  '<h3 style="margin-top:22px"><span class="lv l2">Level 2 · 自己改</span> 與 <span class="lv l3">Level 3 · 挑戰</span></h3>',
  '<div class="sbrow c2"><div class="panel"><p style="margin:0">把你第 1 篇畫的那一格,用<b>三種大小(遠、中、近)</b>各畫一次。注意人物在框裡要畫多大。</p></div>'
  '<div class="panel"><p style="margin:0">把《紙條》的六個段落,每段選一個你覺得最適合的景別,寫在紙上。先不用管對不對,第 4、5 篇會告訴你各景別的用法。</p></div></div>',
  QUIZ_HTML,
  checks(["我能說出景別是什麼:鏡頭離角色多遠、人物在畫面裡多大。",
          "我能分出遠、中、近三種。",
          "我能依序說出九種景別的名稱。",
          "我知道景別是用「身體被切在哪裡」來分的。",
          "我知道不同書籍的叫法可能不同,這個站採用本篇的表。",
          "我在實驗室裡讓取景框變成過至少三種景別。"]),
  '<h3 style="margin-top:30px">可自查的延伸閱讀</h3>',
  '<div class="panel"><ul style="margin:0;padding-left:20px"><li>用「景別 遠景 全景 中景 近景 特寫」當關鍵字,看不同來源怎麼定義,並比較和本篇的差異。</li><li>看一支你喜歡的短片,每換一個鏡頭,試著說出它是哪一種景別。</li></ul></div>')

SIM = {
  "a1": "<b>不適合。</b>大遠景把人縮成一個小點,表情完全看不到。它適合交代地點,不適合表現表情。",
  "a2": "<b>正確!</b>特寫讓整張臉佔滿畫面,疑惑和驚訝的細微變化都看得見。",
  "a3": "<b>可以,但不是最好。</b>全景看得到全身動作,表情卻很小。想強調表情,要再靠近。",
}
QUIZ = quiz_cfg([
  ("景別指的是什麼?", ["鏡頭離角色多遠、人物在畫面裡多大", "畫面的顏色", "影片的長度"], 0, "景別就是畫面拍得遠或近。"),
  ("想交代「人在哪裡、周圍有什麼」,比較適合哪一類?", ["特寫", "遠景一類(拍得遠)", "大特寫"], 1, "拍得遠才看得到環境。"),
  ("本站的景別是用什麼來區分的?", ["鏡頭的品牌", "人物身體被畫面切在哪裡(以及人物佔多大)", "影片的長度"], 1, "例如拍到膝蓋以上是膝上景,拍到腰以上是腰上景。"),
  ("下面哪個順序是由遠到近?", ["特寫 → 全景 → 大遠景", "大遠景 → 遠景 → 全景 → … → 特寫 → 大特寫", "全景 → 大特寫 → 遠景"], 1, "九種景別由遠到近:大遠景、遠景、全景、膝上景、腰上景、近景、胸上景、特寫、大特寫。"),
  ("別人跟你說的「近景」和本站的近景範圍不一樣,怎麼辦?", ["他一定講錯了", "先和對方確認用的是哪一套定義", "放棄使用景別"], 1, "名稱沒有唯一標準。討論前先對齊定義,最不會誤會。"),
])

JS = "<script>\n" + inline_kit() + """
(function () {
  var SZ = %s;
  var WORLD = 1200, PX = 600, MV = [120, -210, 960, 540], HMIN = 14, HMAX = 540;
  var st = { cx: 600, cy: 82, H: 140 };
  var master = document.getElementById("master"), pre = document.getElementById("pre"), info = document.getElementById("info");
  var size = document.getElementById("size"), presets = document.getElementById("presets");
  var seen = {};
  function Hof(v) { return HMIN * Math.pow(HMAX / HMIN, v / 100); }
  function Vof(H) { return Math.round(Math.log(H / HMIN) / Math.log(HMAX / HMIN) * 100); }
  function frame() { var w = st.H * 16 / 9; return { x: st.cx - w / 2, y: st.cy - st.H / 2, w: w, h: st.H }; }
  function clamp() {
    var w = st.H * 16 / 9;
    st.cx = Math.min(MV[0] + MV[2] - w / 2, Math.max(MV[0] + w / 2, st.cx));
    st.cy = Math.min(MV[1] + MV[3] - st.H / 2, Math.max(MV[1] + st.H / 2, st.cy));
  }
  var person = [{ x: PX, y: 130, who: "an", facing: "r" }];
  master.innerHTML = Kit.shot({ worldW: WORLD, vb: MV, people: person, label: "大場景:小安站在走廊中間", extra: '<g id="fg"></g>' });
  var fg = master.querySelector("#fg");
  function overlay() {
    var f = frame(), k = MV[2] / 320, X = MV[0], Y = MV[1], W = MV[2], H = MV[3];
    fg.innerHTML = '<path fill-rule="evenodd" fill="#141413" opacity=".5" d="M' + X + "," + Y + " h" + W + " v" + H + " h" + (-W) + " z M" + f.x + "," + f.y + " h" + f.w + " v" + f.h + " h" + (-f.w) + ' z"/>' +
      '<rect x="' + f.x + '" y="' + f.y + '" width="' + f.w + '" height="' + f.h + '" fill="none" stroke="#D97757" stroke-width="' + (2.4 * k) + '"/>';
  }
  function classify() {
    var f = frame(), top = f.y, bot = f.y + f.h, inX = PX >= f.x && PX <= f.x + f.w;
    if (!inX || bot < 34 || top > 130) return null;
    if (st.H < 19) return "ecu";
    if (top <= 34 && bot >= 130) return st.H > 480 ? "els" : (st.H > 213 ? "ls" : "fs");
    if (top > 58) return "nohead";
    if (bot >= 105) return "mls"; if (bot >= 86) return "ms"; if (bot >= 70) return "mcu"; if (bot >= 62) return "bust"; return "cu";
  }
  function render() {
    clamp(); overlay();
    var f = frame();
    pre.innerHTML = Kit.shot({ worldW: WORLD, vb: [f.x, f.y, f.w, f.h], people: person, label: "取景框裡看到的畫面" });
    var c = classify(), z = SZ.filter(function (s) { return s[0] === c; })[0];
    if (z) {
      seen[c] = true;
      info.innerHTML = "<h4>" + z[1] + "<small>" + z[2] + "</small></h4><div><b>拍到哪裡:</b>" + z[5] + "<br><b>常用來:</b>" + z[6] + '</div><div style="margin-top:8px;color:var(--gray-500);font-size:13px">已試過 ' + Object.keys(seen).length + " / 9 種景別</div>";
    } else if (c === "nohead") {
      info.innerHTML = "<h4>框到身體,但沒有拍到頭</h4><div>這個取景框切掉了小安的頭。把框往上移一點,看看表情。</div>";
    } else {
      info.innerHTML = "<h4>沒有框到小安</h4><div>取景框裡沒有人物。把框拖回大場景中間的小安身上。</div>";
    }
    Array.prototype.forEach.call(presets.querySelectorAll("button"), function (b) { b.classList.toggle("on", b.dataset.c === c); b.setAttribute("aria-pressed", b.dataset.c === c); });
    size.value = Vof(st.H);
  }
  presets.innerHTML = SZ.map(function (s, i) { return '<button type="button" data-c="' + s[0] + '">' + (i + 1) + ". " + s[1] + "</button>"; }).join("");
  presets.addEventListener("click", function (e) {
    var b = e.target.closest("button"); if (!b) return;
    var z = SZ.filter(function (s) { return s[0] === b.dataset.c; })[0];
    st.cx = 600; st.cy = z[4]; st.H = z[3]; render();
  });
  size.addEventListener("input", function () { st.H = Hof(+size.value); render(); });
  var drag = null;
  function toWorld(e) {
    var r = master.getBoundingClientRect();
    return { x: MV[0] + (e.clientX - r.left) / r.width * MV[2], y: MV[1] + (e.clientY - r.top) / r.height * MV[3] };
  }
  master.addEventListener("pointerdown", function (e) {
    var p = toWorld(e), f = frame(), inside = p.x >= f.x && p.x <= f.x + f.w && p.y >= f.y && p.y <= f.y + f.h;
    drag = inside ? { dx: st.cx - p.x, dy: st.cy - p.y } : { dx: 0, dy: 0 };
    try { master.setPointerCapture(e.pointerId); } catch (x) {}
    st.cx = p.x + drag.dx; st.cy = p.y + drag.dy; render(); e.preventDefault();
  });
  master.addEventListener("pointermove", function (e) {
    if (!drag) return; var p = toWorld(e); st.cx = p.x + drag.dx; st.cy = p.y + drag.dy; render();
  });
  function end() { drag = null; }
  master.addEventListener("pointerup", end); master.addEventListener("pointercancel", end);
  master.addEventListener("keydown", function (e) {
    var s = Math.max(3, st.H * 0.08), m = { ArrowLeft: [-s, 0], ArrowRight: [s, 0], ArrowUp: [0, -s], ArrowDown: [0, s] }[e.key];
    if (!m) return; st.cx += m[0]; st.cy += m[1]; render(); e.preventDefault();
  });
  render();
})();
</script>""" % json.dumps([list(z) for z in SZ], ensure_ascii=False)

SPEC = defaults(
  file="microfilm-shot-size-guide.html",
  title="景別總覽:大遠景到大特寫",
  eyebrow="第 3 篇 · 景別總覽",
  h1="景別:鏡頭離角色多遠,觀眾就看到多少",
  sub="先記「遠、中、近」三種,再把它們切細成九種,最後在互動實驗室拖動取景框,自己找出每一種景別。",
  tldr="景別就是「人物在畫面裡有多大」。由遠到近九種:<strong>大遠景、遠景、全景、膝上景、腰上景、近景、胸上景、特寫、大特寫</strong>。遠的給環境,近的給表情。選景別,就是決定這一格想讓觀眾看什麼。",
  toc=[("why", "景別是什麼"), ("ladder", "九種景別"), ("lab", "拖動取景框"), ("practice", "演練與延伸閱讀")],
  body="\n\n".join([why, ladder, lab, practice]),
  config=dict(sim=SIM, quiz=QUIZ),
  js=JS,
  prev=("microfilm-composition-guide.html", "畫面與構圖"),
  next=("microfilm-wide-shots-guide.html", "遠景、全景、中景的功能"),
)
