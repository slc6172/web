"""微電影主題的共用:CSS、頁面預設值、小元件。每個 mN.py 開頭:  from mh import *"""
from h import *
from svgkit import *

TOPIC = "微電影分鏡入門"
FOOT = "本頁是觀念與練習教學,不依賴特定器材:用手機、相機、平板都能照著做。不同學校或書籍對鏡頭名稱的叫法可能略有不同。內容整理日期:2026-11-10。"
DIR = "microfilm"

MF_CSS = """
  .sb { margin:0; background:#fff; border:var(--border); border-radius:12px; overflow:hidden; }
  .sb-pic { position:relative; border-bottom:var(--border); background:var(--gray-100); }
  .sb-pic svg { display:block; width:100%; height:auto; aspect-ratio:16/9; }
  .sb-n { position:absolute; left:8px; top:8px; z-index:1; min-width:22px; height:22px; padding:0 6px; border-radius:999px; display:grid; place-items:center; background:var(--slate); color:#fff; font:600 12px var(--mono); }
  .sb figcaption { padding:10px 12px 12px; display:grid; gap:6px; font-size:13.5px; line-height:1.55; color:var(--gray-700); }
  .sb figcaption b { font:600 11px var(--mono); letter-spacing:.06em; color:var(--gray-500); margin-right:8px; }
  .sb .mk { display:inline-grid; place-items:center; width:18px; height:18px; margin-right:6px; border-radius:50%; background:var(--clay); color:#fff; font:600 11px var(--mono); vertical-align:1px; }
  .sb-pic .mk { position:absolute; right:8px; top:8px; width:22px; height:22px; margin:0; z-index:1; }
  .sbrow { display:grid; gap:14px; margin:14px 0; }
  .sbrow.c2 { grid-template-columns:repeat(2,minmax(0,1fr)); }
  .sbrow.c3 { grid-template-columns:repeat(3,minmax(0,1fr)); }
  .sbrow.c4 { grid-template-columns:repeat(4,minmax(0,1fr)); }
  @media (max-width: 920px) { .sbrow.c3, .sbrow.c4 { grid-template-columns:repeat(2,minmax(0,1fr)); } }
  @media (max-width: 520px) { .sbrow.c2, .sbrow.c3, .sbrow.c4 { grid-template-columns:minmax(0,1fr); } }
  .sbone { max-width:520px; margin:14px 0; }
  .lv { display:inline-block; margin-right:8px; padding:2px 10px; border-radius:999px; font:600 11px var(--mono); letter-spacing:.04em; vertical-align:2px; }
  .lv.l1 { background:rgba(120,140,93,.18); color:#5C6E45; }
  .lv.l2 { background:var(--oat); color:var(--gray-700); }
  .lv.l3 { background:rgba(217,119,87,.18); color:var(--clay-d); }
  .shotfig { margin:0; }
  .shotfig svg { display:block; width:100%; height:auto; aspect-ratio:16/9; border:var(--border); border-radius:10px; background:var(--gray-100); }
  .shotfig figcaption { font-size:13px; color:var(--gray-700); margin-top:6px; line-height:1.5; }
  .shotfig.empty svg { background:#fff; border-style:dashed; }
  .arrow-row { display:flex; gap:14px; align-items:flex-end; flex-wrap:wrap; margin:14px 0; }
  .arrow-row .shotfig svg { width:auto; height:150px; }
  .arrow-row .shotfig figcaption { text-align:center; font:600 12px var(--mono); color:var(--gray-700); }
  @media (max-width: 520px) { .arrow-row .shotfig svg { height:110px; } }
  .ar-43 svg { aspect-ratio:4/3; } .ar-11 svg { aspect-ratio:1/1; } .ar-916 svg { aspect-ratio:9/16; }
  .duo { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:14px; }
  @media (max-width: 720px) { .duo { grid-template-columns:minmax(0,1fr); } }
  .duo .box > b { display:block; font:600 11px var(--mono); letter-spacing:.06em; color:var(--gray-500); margin-bottom:6px; }
  .duo svg { display:block; width:100%; height:auto; aspect-ratio:16/9; border:var(--border); border-radius:10px; background:var(--gray-100); }
  .master { touch-action:none; cursor:grab; border-radius:10px; } .master:active { cursor:grabbing; }
  .master:focus-visible { outline:2px solid var(--clay); outline-offset:3px; }
  .rng { display:flex; align-items:center; gap:12px; margin:14px 0 4px; font:12px var(--mono); color:var(--gray-500); }
  .rng input { flex:1; accent-color:var(--clay); }
  .info { margin-top:12px; background:var(--gray-100); border-radius:10px; padding:12px 14px; font-size:14px; line-height:1.65; color:var(--gray-700); }
  .info h4 { margin:0 0 4px; font:500 20px var(--serif); color:var(--slate); } .info h4 small { font:12px var(--mono); color:var(--gray-500); margin-left:8px; }
  .lab { display:grid; grid-template-columns:minmax(0,1.5fr) minmax(0,1fr); gap:16px; align-items:start; }
  @media (max-width: 720px) { .lab { grid-template-columns:minmax(0,1fr); } }
  .lab .stage svg { display:block; width:100%; height:auto; aspect-ratio:16/9; border:var(--border); border-radius:10px; background:var(--gray-100); }
  .lab .grp { margin:0 0 12px; } .lab .grp > b { display:block; font:600 11px var(--mono); letter-spacing:.06em; color:var(--gray-500); margin-bottom:6px; }
  .lab .opts { display:flex; flex-wrap:wrap; gap:6px; }
  .lab .opts button { font:600 13px var(--sans); padding:7px 12px; border:var(--border); border-radius:999px; background:#fff; color:var(--slate); cursor:pointer; }
  .lab .opts button:hover { border-color:var(--clay); }
  .lab .opts button.on { background:var(--slate); color:#fff; border-color:var(--slate); }
  .lab .opts button:focus-visible { outline:2px solid var(--clay); outline-offset:2px; }
  .verdict { margin-top:12px; background:var(--gray-100); border-radius:10px; padding:12px 14px; font-size:14px; line-height:1.6; color:var(--gray-700); }
  .verdict b.ok { color:#5C6E45; } .verdict b.no { color:var(--rust); }
  .later { display:inline-block; margin-left:8px; padding:2px 10px; border-radius:999px; background:var(--oat); color:var(--gray-700); font:600 11px var(--mono); vertical-align:3px; }
  .ctl { display:grid; gap:10px; grid-template-columns:repeat(2,minmax(0,1fr)); margin:12px 0; }
  .ctl label { display:block; font:12px var(--mono); color:var(--gray-500); margin-bottom:4px; }
  .ctl input { width:100%; font:15px var(--sans); padding:9px 12px; border:var(--border); border-radius:8px; background:#fff; color:var(--slate); }
  .ctl input:focus-visible { outline:2px solid var(--clay); outline-offset:1px; }
  @media (max-width: 720px) { .ctl { grid-template-columns:minmax(0,1fr); } }
  .legend-key { display:flex; gap:18px; flex-wrap:wrap; margin:8px 0 0; font-size:13.5px; color:var(--gray-700); }
  .legend-key span { display:inline-flex; align-items:center; gap:8px; }
  .legend-key svg { width:44px; height:14px; }
"""


def lv(n, text):
    names = {1: "Level 1", 2: "Level 2", 3: "Level 3"}
    return '<span class="lv l%d">%s · %s</span>' % (n, names[n], text)


def fig(svg, cap="", cls=""):
    c = "<figcaption>%s</figcaption>" % cap if cap else ""
    return '<figure class="shotfig %s">%s%s</figure>' % (cls, svg, c)


def figrow(*figs, cols=None):
    cols = cols or len(figs)
    return '<div class="sbrow c%d">%s</div>' % (cols, "".join(figs))


def defaults(**kw):
    d = dict(dir=DIR, topic=TOPIC, foot=FOOT, css=MF_CSS)
    d.update(kw)
    return d


# ---------- 共用:景別預設與取景(1200 寬世界,人物 x=600)、選擇題小元件 ----------
MF_CSS += """
  .ch { margin:12px 0; }
  .ch .opts { display:flex; flex-wrap:wrap; gap:6px; }
  .ch .opts button { font:600 13px var(--sans); padding:7px 14px; border:var(--border); border-radius:999px; background:#fff; color:var(--slate); cursor:pointer; }
  .ch .opts button:hover { border-color:var(--clay); }
  .ch .opts button:focus-visible { outline:2px solid var(--clay); outline-offset:2px; }
  .ch .opts button.ok { background:#5C6E45; color:#fff; border-color:#5C6E45; }
  .ch .opts button.no { background:var(--rust); color:#fff; border-color:var(--rust); }
  .ch .res { margin-top:12px; font-size:14px; line-height:1.65; color:var(--gray-700); }
  .ch .res[hidden] { display:none; }
  .ch .res .shotfig { max-width:420px; margin-top:8px; }
"""

CHOOSE_JS = """<script>
Array.prototype.forEach.call(document.querySelectorAll(".ch"), function (c) {
  c.querySelector(".opts").addEventListener("click", function (e) {
    var b = e.target.closest("button"); if (!b) return;
    var a = +c.dataset.ans, i = +b.dataset.i, bs = c.querySelectorAll(".opts button");
    Array.prototype.forEach.call(bs, function (x, j) { x.classList.toggle("ok", j === a); x.classList.toggle("no", j === i && i !== a); x.setAttribute("aria-pressed", j === i); });
    c.querySelector(".vd").innerHTML = i === a ? "<b>答對了!</b>" : "<b>再想想。</b>比較適合的是「" + bs[a].textContent + "」。";
    c.querySelector(".res").hidden = false;
  });
});
</script>"""


def choose(items):
    """選擇題卡片。items: dict(q=題目, opts=[...], ans=正確索引, why=說明, pic=答對後顯示的示意圖 svg(可省), cap=圖說)。"""
    out = []
    for n, it in enumerate(items, 1):
        opts = "".join('<button type="button" data-i="%d">%s</button>' % (j, o) for j, o in enumerate(it["opts"]))
        pic = fig(it["pic"], it.get("cap", "")) if it.get("pic") else ""
        out.append('<div class="panel ch" data-ans="%d"><p style="margin:0 0 10px"><b>%d.</b> %s</p><div class="opts">%s</div>'
                   '<div class="res" hidden><span class="vd"></span> %s%s</div></div>' % (it["ans"], n, it["q"], opts, it["why"], pic))
    return "".join(out)


SZ = {  # 代號: (中文, H, cy)
    "els": ("大遠景", 520, 70), "ls": ("遠景", 300, 60), "fs": ("全景", 140, 82), "mls": ("膝上景", 87, 68.8),
    "ms": ("腰上景", 64.4, 59.8), "mcu": ("近景", 46.7, 52.7), "bust": ("胸上景", 33, 47.2), "cu": ("特寫", 26.7, 44.7), "ecu": ("大特寫", 14, 47.5),
}


def vbfor(H, cy, cx=600):
    w = H * 16 / 9
    return [round(cx - w / 2, 2), round(cy - H / 2, 2), round(w, 2), H]


def V(code, people=None, cx=600, **kw):
    """單人(或自訂 people)在 1200 寬走廊裡,依景別代號取景。"""
    z = SZ[code]
    kw.setdefault("worldW", 1200)
    return shot(people=people or [P(600, 130)], vb=vbfor(z[1], z[2], cx), **kw)


def win_frame(vb, inset=14):
    """窗框遮罩(主觀鏡頭用):在 vb 範圍外圈畫一圈窗框,中間留空。回傳 raw SVG,給 shot(extra=...)。"""
    x, y, w, h = vb
    k = w / 320
    i = inset * k
    return ('<path fill-rule="evenodd" fill="#87867F" d="M%s,%s h%s v%s h%s z M%s,%s h%s v%s h%s z"/>' % (x, y, w, h, -w, x + i, y + i, w - 2 * i, h - 2 * i, -(w - 2 * i))
            + '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#87867F" stroke-width="%s"/>' % (x + w / 2, y, x + w / 2, y + h, 3 * k))


# ================= 第 7–16 篇共用:運鏡起訖圖、動畫小工具、拍攝角度/景深圖 =================
MF_CSS += """
  .mvpair { display:grid; grid-template-columns:minmax(0,1fr) auto minmax(0,1fr); gap:10px; align-items:center; margin:14px 0; }
  .mvpair .mid { font:600 22px var(--mono); color:var(--clay); text-align:center; }
  .mvpair .mid small { display:block; font:600 11px var(--mono); color:var(--gray-500); letter-spacing:.04em; }
  @media (max-width: 520px) { .mvpair { grid-template-columns:minmax(0,1fr); } .mvpair .mid { transform:rotate(90deg); } }
  .anim .stagebox { display:grid; gap:12px; }
  .anim .stagebox.two { grid-template-columns:repeat(2,minmax(0,1fr)); }
  @media (max-width: 720px) { .anim .stagebox.two { grid-template-columns:minmax(0,1fr); } }
  .anim .stage svg { display:block; width:100%; height:auto; aspect-ratio:16/9; border:var(--border); border-radius:10px; background:var(--gray-100); }
  .anim .stage > b { display:block; font:600 11px var(--mono); letter-spacing:.06em; color:var(--gray-500); margin-bottom:6px; }
  .anim .bar2 { display:flex; align-items:center; gap:12px; margin:12px 0 4px; }
  .anim .bar2 input { flex:1; accent-color:var(--clay); }
  .anim button.play { font:600 12px var(--mono); padding:8px 16px; border-radius:999px; border:0; background:var(--slate); color:#fff; cursor:pointer; min-width:84px; }
  .anim button.play:focus-visible { outline:2px solid var(--clay); outline-offset:2px; }
  .anim .note2 { font-size:13px; color:var(--gray-500); margin:6px 0 0; }
  .anim .rm { display:none; font-size:13px; color:var(--gray-500); margin:6px 0 0; }
  .anim.reduced .rm { display:block; } .anim.reduced button.play { display:none; }
  .fx { display:flex; flex-wrap:wrap; gap:6px; margin:10px 0 0; }
  .fx button { font:600 13px var(--sans); padding:7px 12px; border:var(--border); border-radius:999px; background:#fff; color:var(--slate); cursor:pointer; }
  .fx button.on { background:var(--slate); color:#fff; border-color:var(--slate); }
  .fx button:focus-visible { outline:2px solid var(--clay); outline-offset:2px; }
  .feel { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:10px; margin:12px 0; }
  .feel > div { background:#fff; border:var(--border); border-radius:10px; padding:10px 12px; font-size:14px; line-height:1.6; color:var(--gray-700); }
  .feel b { display:block; font:600 11px var(--mono); letter-spacing:.06em; color:var(--gray-500); margin-bottom:2px; }
  @media (max-width: 520px) { .feel { grid-template-columns:minmax(0,1fr); } }
"""


def mvpair(name, cam=None, capA="起點", capB="終點", mid="", **kw):
    """運鏡的「起點 → 終點」兩格(靜態、預先畫好)。name 是 svgkit.move 的運鏡名;cam=dict(kind=,dir=) 在終點格畫橘色箭頭。"""
    a = move(name, 0, label=capA, **kw)
    b = move(name, 1, label=capB, cam=cam, **kw) if cam else move(name, 1, label=capB, **kw)
    return ('<div class="mvpair">' + fig(a, "<b>起點</b> " + capA) + '<div class="mid">→<small>%s</small></div>' % mid + fig(b, "<b>終點</b> " + capB) + "</div>")


def animbox(id_, title, caption="", two=False, hint="按「播放」看動畫,也可以拖動滑桿慢慢看。"):
    """動畫容器。頁面 JS 要註冊 window.ANIMS[id_] = {dur:毫秒, frames:[function(t){return svg}, ...], names:[標題...]}。"""
    return ('<div class="panel anim" data-id="%s"><h3 style="margin-top:0">%s</h3>%s<div class="stagebox%s"></div>'
            '<div class="bar2"><button type="button" class="play">播放</button><input type="range" min="0" max="100" value="0" aria-label="動畫進度"></div>'
            '<p class="note2">%s</p><p class="rm">你的系統設定為「減少動態效果」,所以不會自動播放;拖動滑桿就能手動看每一格。</p></div>'
            % (id_, title, ("<p style='margin:0 0 10px;color:var(--gray-700)'>%s</p>" % caption) if caption else "", " two" if two else "", hint))


ANIM_JS = """<script>
window.ANIMS = window.ANIMS || {};
(function () {
  var reduced = !!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
  Array.prototype.forEach.call(document.querySelectorAll(".anim"), function (box) {
    var def = window.ANIMS[box.dataset.id]; if (!def) return;
    var sb = box.querySelector(".stagebox"), btn = box.querySelector(".play"), rng = box.querySelector("input[type=range]");
    var t = 0, playing = false, last = 0, hold = 0, stages = [];
    if (reduced) box.classList.add("reduced");
    def.frames.forEach(function (f, i) {
      var d = document.createElement("div"); d.className = "stage";
      d.innerHTML = (def.names && def.names[i] ? "<b>" + def.names[i] + "</b>" : "") + '<div class="v"></div>';
      sb.appendChild(d); stages.push(d.querySelector(".v"));
    });
    function draw() { def.frames.forEach(function (f, i) { stages[i].innerHTML = f(Math.min(1, t), box); }); rng.value = Math.round(Math.min(1, t) * 100); if (def.onframe) def.onframe(box, Math.min(1, t)); }
    function tick(ts) {
      if (!playing) return;
      if (!last) last = ts;
      var dt = ts - last; last = ts;
      if (t >= 1) { hold += dt; if (hold > 700) { t = 0; hold = 0; } }
      else t += dt / (def.dur || 3000);
      draw(); requestAnimationFrame(tick);
    }
    function set(p) { playing = p; btn.textContent = p ? "暫停" : "播放"; if (p) { last = 0; if (t >= 1) t = 0; requestAnimationFrame(tick); } }
    btn.addEventListener("click", function () { set(!playing); });
    rng.addEventListener("input", function () { set(false); t = rng.value / 100; draw(); });
    draw();
  });
})();
</script>"""


def fx_buttons(items, active=0):
    """一排切換鈕(給 JS 用):items = [(key, 文字), ...]"""
    return '<div class="fx" role="group">%s</div>' % "".join('<button type="button" data-k="%s"%s>%s</button>' % (k, ' class="on"' if i == active else "", t) for i, (k, t) in enumerate(items))


def feel(*pairs):
    """觀眾的感受:pairs = [(標題, 說明), ...]"""
    return '<div class="feel">%s</div>' % "".join("<div><b>%s</b>%s</div>" % p for p in pairs)


def anim_page(registry_js, extra_js=""):
    """動畫頁的 <script>:內嵌 kit.js → 註冊 window.ANIMS → ANIM_JS(播放器)→ CHOOSE_JS。
    registry_js 例:  ANIMS.pan = {dur:3600, names:["搖攝"], frames:[function(t){ return Kit.moveFrame({name:"pan", t:t, cam:{kind:"pan"}}); }]};"""
    return "<script>\n" + inline_kit() + "\nwindow.ANIMS = window.ANIMS || {};\n" + registry_js + "\n" + extra_js + "\n</script>" + ANIM_JS + CHOOSE_JS


def mvf(name, **kw):
    """registry_js 用:產生 frames 的 JS 函式字串。  mvf('pan', cam={'kind':'pan'})"""
    import json as _j
    return "function(t){ return Kit.moveFrame(Object.assign({name:%s, t:t}, %s)); }" % (_j.dumps(name), _j.dumps(kw, ensure_ascii=False))
