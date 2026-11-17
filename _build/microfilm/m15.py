import json
from mh import *

PAGE_CSS = """
  .strip { display:flex; gap:10px; overflow-x:auto; padding:4px 2px 12px; margin:0 0 10px; }
  .th { flex:0 0 150px; border:var(--border); border-radius:10px; background:#fff; padding:0; cursor:pointer; position:relative; overflow:hidden; text-align:left; font-family:var(--sans); }
  .th.on { border-color:var(--clay); outline:2px solid var(--clay); outline-offset:1px; }
  .th:focus-visible { outline:2px solid var(--clay); outline-offset:2px; }
  .th svg { display:block; width:100%; height:auto; aspect-ratio:16/9; background:var(--gray-100); }
  .th .n { position:absolute; left:6px; top:6px; min-width:20px; height:20px; padding:0 5px; border-radius:999px; background:var(--slate); color:#fff; font:600 11px var(--mono); display:grid; place-items:center; }
  .th small { display:block; padding:5px 8px 6px; font:11px var(--mono); color:var(--gray-500); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  .ed-btns { display:flex; flex-wrap:wrap; gap:8px; margin:0 0 12px; }
  .ed-btns button { font:600 12px var(--mono); padding:8px 14px; border-radius:999px; border:var(--border); background:transparent; color:var(--gray-700); cursor:pointer; }
  .ed-btns button:hover { border-color:var(--clay); color:var(--clay-d); }
  .ed-btns button.primary { background:var(--slate); color:#fff; border-color:var(--slate); }
  .ed-btns button.primary.ok { background:var(--olive); border-color:var(--olive); }
  .ed-btns button.armed { border-color:var(--rust); color:var(--rust); }
  .ed-btns button:focus-visible { outline:2px solid var(--clay); outline-offset:2px; }
  .ctl select, .ctl textarea { width:100%; font:15px var(--sans); padding:8px 10px; border:var(--border); border-radius:8px; background:#fff; color:var(--slate); }
  .ctl textarea { min-height:64px; resize:vertical; }
  .ctl select:focus-visible, .ctl textarea:focus-visible { outline:2px solid var(--clay); outline-offset:1px; }
  .ctl .wide { grid-column:1/-1; }
  .out { width:100%; border-collapse:collapse; font-size:13.5px; line-height:1.55; }
  .out th, .out td { border:1px solid var(--gray-300); padding:7px 9px; text-align:left; vertical-align:top; }
  .out th { background:var(--gray-100); font:600 11px var(--mono); letter-spacing:.06em; color:var(--gray-500); }
  #edlab { grid-template-columns:minmax(0,1.3fr) minmax(0,1fr); }
  @media (max-width: 720px) { #edlab { grid-template-columns:minmax(0,1fr); } }
  .why { margin-top:10px; background:rgba(217,119,87,.1); border-radius:10px; padding:10px 12px; font-size:14px; color:var(--gray-700); }
  .why[hidden] { display:none; }
"""

SEG = ["放學鐘響,走廊空蕩,小安背著書包快步走。", "她停在置物櫃前,看見櫃門縫夾著一張紙條。", "她讀紙條,表情從疑惑變驚訝。", "窗外,小宇在校門口低頭看手機等人。", "小安衝下樓。", "兩人在校門口面對面,小安遞出紙條,兩人笑了。"]
def R(text, **k):
    d = dict(text=text, dial="", scene="hallway", subj="an", size="ms", expr="neutral", pose="stand", face="r", move="none", mdir="r", parrow=False, angle="平視", note="")
    d.update(k); return d
REF = [
  R(SEG[0], size="fs", pose="walk", move="track", parrow=True, why="全景看清楚「走」的動作;橫移讓背景一直滑過去,有空蕩蕩又趕時間的感覺。"),
  R(SEG[1], subj="note", size="ecu", why="大特寫插入:讓觀眾看清楚那張紙條,這是重要物件。"),
  R(SEG[2], size="mcu", pose="read", expr="puzzled", move="push", why="近景加推:慢慢靠近她,表情從疑惑變驚訝,觀眾一起屏息。"),
  R(SEG[3], scene="gate", subj="yu", size="mcu", pose="phone", angle="俯拍", why="從樓上看下去(俯拍),小宇顯得有點孤單;這也是小安看到的畫面(POV)。"),
  R(SEG[4], size="fs", pose="run", move="follow", parrow=True, why="全景加跟拍:看清楚跑的動作,鏡頭追著她。"),
  R(SEG[5], scene="gate", subj="both", size="ms", expr="smile", why="腰上景雙人:兩人面對面,表情與手勢都看得到。要拍更多格,可加過肩與反應鏡頭(第 13 篇)。"),
]
DEF = [R(t) for t in SEG]

start = section("start", "任務:把《紙條》畫成分鏡表",
  '<p class="sub" style="margin-bottom:10px">' + lv(1, "跟著做") + '這一篇不教新觀念,而是<b>把前面學的全部用起來</b>。你要把《紙條》的六個段落,畫成一張完整的分鏡表。工作方式:<b>選一格 → 選景別、角色、運鏡 → 寫下動作</b>,畫面會自動畫出來。</p>',
  table("g3", ["要決定的事", "在哪一篇學過", "問自己"], [
    ["景別(拍多近)", "第 3–5 篇", "這一格要讓觀眾看到環境、動作,還是表情?"],
    ["特殊鏡頭(插入、POV 等)", "第 6 篇", "有沒有重要物件?是不是誰的視線?"],
    ["角度", "第 7 篇", "要不要用俯拍或仰拍加強感覺?(寫在文字裡)"],
    ["運鏡", "第 9–12 篇", "鏡頭要不要動?為什麼?"],
    ["連戲", "第 13 篇", "人物的左右位置有沒有保持一致?"]]),
  tip("先照<b>「簡單的」</b>做:每段先畫一格。畫完六格,再回頭想要不要多加幾格(例如過肩、反應)。<b>沒有唯一正確答案</b>,重點是你說得出理由。"))

ed = section("ed", "分鏡編輯器",
  '<p class="sub" style="margin-bottom:12px">' + lv(2, "自己改") + '編輯器裡已經放了《紙條》的六段文字,每一格先用預設畫面。點上方的縮圖選一格,在右邊改設定。卡住時可以按「套用參考答案」看一種拍法,再自己改。</p>',
  '''<div class="panel">
  <div class="ed-btns" role="group" aria-label="編輯器功能">
    <button type="button" id="bAdd">＋ 新增一格</button>
    <button type="button" id="bDel">刪除這格</button>
    <button type="button" id="bUp">← 前移</button>
    <button type="button" id="bDown">後移 →</button>
    <button type="button" id="bRef">套用參考答案</button>
    <button type="button" id="bReset">重設成《紙條》六段</button>
    <button type="button" id="bClear">清空</button>
  </div>
  <div class="strip" id="strip" role="list" aria-label="分鏡縮圖"></div>
  <div class="lab" id="edlab">
    <div><div class="stage" id="stage" aria-live="polite"></div><div class="verdict" id="auto"></div><div class="why" id="why" hidden></div></div>
    <div class="ctl" id="ctl">
      <div class="wide"><label for="f-text">動作(這一格發生什麼事)</label><textarea id="f-text" data-k="text"></textarea></div>
      <div class="wide"><label for="f-dial">對白(沒有就留空)</label><input id="f-dial" data-k="dial" autocomplete="off"></div>
      <div><label for="f-scene">場景</label><select id="f-scene" data-k="scene"></select></div>
      <div><label for="f-subj">畫面裡有誰</label><select id="f-subj" data-k="subj"></select></div>
      <div><label for="f-size">景別</label><select id="f-size" data-k="size"></select></div>
      <div><label for="f-angle">角度(只寫在文字裡)</label><select id="f-angle" data-k="angle"></select></div>
      <div><label for="f-expr">表情</label><select id="f-expr" data-k="expr"></select></div>
      <div><label for="f-pose">姿勢</label><select id="f-pose" data-k="pose"></select></div>
      <div><label for="f-face">人物朝向</label><select id="f-face" data-k="face"><option value="r">朝右</option><option value="l">朝左</option></select></div>
      <div><label for="f-parrow">人物移動箭頭(黑色)</label><select id="f-parrow" data-k="parrow"><option value="0">不畫</option><option value="1">畫</option></select></div>
      <div><label for="f-move">運鏡(橘色箭頭)</label><select id="f-move" data-k="move"></select></div>
      <div><label for="f-mdir">運鏡方向</label><select id="f-mdir" data-k="mdir"></select></div>
      <div class="wide"><label for="f-note">補充說明(選填)</label><input id="f-note" data-k="note" autocomplete="off"></div>
    </div>
  </div></div>''',
  '<p style="margin-top:12px;color:var(--gray-500);font-size:13px">這一頁會把你的分鏡存在<b>這台裝置的瀏覽器</b>裡,下次回來還在;如果瀏覽器不允許儲存,畫面仍可使用,只是關掉頁面就會消失。要保存或交作業,請用下面的「複製分鏡表」。</p>')

out = section("out", "分鏡表:複製帶走",
  '<p class="sub" style="margin-bottom:12px">' + lv(2, "自己改") + '下面是你目前的分鏡表。按「複製分鏡表」,貼到文件、筆記或聊天裡就能分享。(格式是 Markdown 表格,貼到大部分筆記軟體都會變成表格。)</p>',
  '<div class="panel"><div class="ed-btns"><button type="button" class="primary" id="bCopy">複製分鏡表</button></div><div class="table-wrap" style="overflow-x:auto"><table class="out" id="outTbl"></table></div></div>')

review = section("review", "檢查你的分鏡",
  '<p>' + lv(3, "挑戰") + '畫完以後,用這份清單<b>自己檢查一遍</b>。每一項都和前面的某一篇有關,不確定時就回去看。</p>',
  '<div class="panel"><ul style="margin:0;padding-left:20px;line-height:1.9"><li>每一格的<b>景別</b>,我說得出為什麼選它。(第 3–5 篇)</li><li>需要看清楚的<b>重要物件</b>,有用插入鏡頭。(第 6 篇)</li><li>運鏡的格子,我知道<b>鏡頭為什麼要動</b>。沒理由就改成固定。(第 9–12 篇)</li><li>連續兩格<b>不太像</b>,不會剪起來跳。(第 13 篇)</li><li>如果有對話,兩人的<b>左右位置保持一致</b>。(第 13 篇)</li></ul></div>',
  '<div class="panel" style="margin-top:14px"><h3>' + lv(3, "挑戰") + '</h3><p style="margin:0">把「動作」那一欄<b>改成你自己的故事</b>(新增格數、刪掉不要的),重新畫一份分鏡表。你現在就是導演了。</p></div>')

practice = section("practice", "快速測驗與檢查",
  QUIZ_HTML,
  checks(["我已把《紙條》的六段各畫成至少一格。",
          "每一格我都寫了「動作」,需要時也寫了對白。",
          "每一格的景別我都說得出理由。",
          "我檢查過人物的左右位置沒有亂掉。",
          "我複製了分鏡表,並存在自己找得到的地方。",
          "我試著把動作改成自己的故事。"]),
  '<h3 style="margin-top:30px">可自查的延伸閱讀</h3>',
  '<div class="panel"><ul style="margin:0;padding-left:20px"><li>下一篇會把分鏡變成「拍攝前的鏡頭清單」,並整理新手最常見的錯誤。</li></ul></div>')

QUIZ = quiz_cfg([
  ("畫分鏡時,最先決定什麼?", ["這一格要讓觀眾看到或感覺到什麼", "用什麼顏色", "拍幾秒"], 0, "先想目的,再選景別、運鏡。"),
  ("同一場對話,兩人的左右位置要?", ["保持一致", "每格對調", "隨便"], 0, "這是第 13 篇的連戲。"),
  ("鏡頭要不要動?", ["有理由才動,沒理由就固定", "越多越好", "一定要動"], 0, "動的鏡頭要留給需要的時刻。"),
  ("分鏡表怎麼保存最保險?", ["複製分鏡表,存在自己的文件", "只留在瀏覽器", "不用存"], 0, "瀏覽器的存檔只在這台裝置。")])

SZJ = {k: [v[0], v[1], v[2]] for k, v in SZ.items()}
JS = "<script>\n" + inline_kit() + """
(function () {
  var SZ = __SZ__, DEF = __DEF__, REF = __REF__;
  var SIZES = ["els","ls","fs","mls","ms","mcu","bust","cu","ecu"];
  var L = { scene:[["hallway","走廊"],["gate","校門口"]], subj:[["an","小安"],["yu","小宇"],["both","兩個人"],["note","紙條(插入)"]],
    expr:[["neutral","平靜"],["smile","微笑"],["puzzled","疑惑"],["surprise","驚訝"],["sad","難過"],["angry","生氣"],["fear","害怕"]],
    pose:[["stand","站著"],["walk","走路"],["run","跑步"],["read","讀紙條"],["phone","看手機"]],
    move:[["none","固定"],["pan","搖攝"],["tilt","俯仰"],["push","推"],["pull","拉"],["track","橫移"],["follow","跟拍"],["orbit","環繞"],["rise","升降"]],
    angle:[["平視","平視"],["俯拍","俯拍"],["仰拍","仰拍"],["荷蘭角","荷蘭角"]] };
  var S = { p: null, i: 0 }, KEY = "mf-practice-v1", mem = null;
  function clone(x) { return JSON.parse(JSON.stringify(x)); }
  function load() { try { var r = window.localStorage.getItem(KEY); if (r) { var a = JSON.parse(r); if (Array.isArray(a) && a.length) return a; } } catch (e) {} return mem; }
  function save() { mem = clone(S.p); try { window.localStorage.setItem(KEY, JSON.stringify(S.p)); } catch (e) {} }
  function blank() { return { text:"", dial:"", scene:"hallway", subj:"an", size:"ms", expr:"neutral", pose:"stand", face:"r", move:"none", mdir:"r", parrow:false, angle:"平視", note:"" }; }
  function nm(list, v) { for (var i = 0; i < list.length; i++) if (list[i][0] === v) return list[i][1]; return v; }
  function dirName(p) { if (p.move === "none" || p.move === "push" || p.move === "pull" || p.move === "orbit") return ""; return p.move === "tilt" || p.move === "rise" ? (p.mdir === "d" ? "(向下)" : "(向上)") : (p.mdir === "l" ? "(向左)" : "(向右)"); }
  function label(p) { var s = SZ[p.size][0] + (p.subj === "both" ? "(雙人)" : p.subj === "note" ? "(插入)" : ""); return s + "，" + p.angle + "，" + nm(L.move, p.move) + dirName(p); }
  function frame(p) {
    var gate = p.scene === "gate", W = gate ? 320 : 1200, cx = gate ? 160 : 600, o = { scene: p.scene, worldW: W, people: [], label: label(p) }, vb, w, H, z = SZ[p.size];
    if (p.subj === "note") { o.props = [{ name: "note", x: cx - 11, y: 100, s: 1 }]; H = 40; vb = [cx - H * 8 / 9, 114 - H / 2, H * 16 / 9, H]; }
    else { H = z[1]; w = H * 16 / 9; vb = [cx - w / 2, z[2] - H / 2, w, H]; }
    o.vb = vb;
    if (p.subj === "both") o.people = [{ x: cx - 40, y: 130, h: 100, facing: "r", who: "an", pose: p.pose, expr: p.expr }, { x: cx + 40, y: 130, h: 100, facing: "l", who: "yu", pose: p.pose, expr: p.expr }];
    else if (p.subj !== "note") o.people = [{ x: cx, y: 130, h: 100, facing: p.face, who: p.subj, pose: p.pose, expr: p.expr }];
    if (p.parrow && p.subj !== "note") { var d = p.face === "l" ? -1 : 1; o.arrows = [{ x1: cx + d * vb[2] * .1, y1: vb[1] + vb[3] * .2, x2: cx + d * vb[2] * .34, y2: vb[1] + vb[3] * .2, kind: "move", label: null }]; }
    if (p.move !== "none") o.cam = { kind: p.move, dir: p.move === "tilt" || p.move === "rise" ? (p.mdir === "d" ? "d" : "u") : (p.mdir === "l" ? "l" : "r") };
    return Kit.shot(o);
  }
  var strip = document.getElementById("strip"), stage = document.getElementById("stage"), auto = document.getElementById("auto"), why = document.getElementById("why");
  function fill(id, list) { var el = document.getElementById(id); el.innerHTML = list.map(function (x) { return '<option value="' + x[0] + '">' + x[1] + "</option>"; }).join(""); }
  fill("f-scene", L.scene); fill("f-subj", L.subj); fill("f-expr", L.expr); fill("f-pose", L.pose); fill("f-move", L.move); fill("f-angle", L.angle);
  fill("f-size", SIZES.map(function (c) { return [c, SZ[c][0]]; }));
  function mdirFill(p) { var el = document.getElementById("f-mdir"), v = (p.move === "tilt" || p.move === "rise") ? [["u","向上"],["d","向下"]] : [["r","向右"],["l","向左"]]; fill("f-mdir", v); el.disabled = (p.move === "none" || p.move === "push" || p.move === "pull" || p.move === "orbit"); if (!v.some(function (x) { return x[0] === p.mdir; })) p.mdir = v[0][0]; el.value = p.mdir; }
  function sync() {
    var p = S.p[S.i];
    document.querySelectorAll("#ctl [data-k]").forEach(function (el) {
      var k = el.dataset.k; if (k === "mdir") return;
      el.value = k === "parrow" ? (p.parrow ? "1" : "0") : p[k];
    });
    mdirFill(p);
    document.getElementById("f-face").disabled = (p.subj === "both" || p.subj === "note");
    document.getElementById("f-pose").disabled = (p.subj === "note");
    document.getElementById("f-expr").disabled = (p.subj === "note");
  }
  function strips() {
    strip.innerHTML = S.p.map(function (p, i) { return '<button type="button" class="th' + (i === S.i ? " on" : "") + '" data-i="' + i + '" role="listitem" aria-label="第 ' + (i + 1) + ' 格"><span class="n">' + (i + 1) + "</span>" + frame(p) + "<small>" + label(p) + "</small></button>"; }).join("");
  }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function table() {
    var rows = S.p.map(function (p, i) { return "<tr><td>" + (i + 1) + "</td><td>" + label(p) + "</td><td>" + esc(p.text) + "</td><td>" + esc(p.dial) + "</td><td>" + esc(p.note) + "</td></tr>"; }).join("");
    document.getElementById("outTbl").innerHTML = "<tr><th>格</th><th>鏡頭(景別，角度，運鏡)</th><th>動作</th><th>對白</th><th>補充</th></tr>" + rows;
  }
  function md() {
    function c(s) { return String(s || "").replace(/\\|/g, "／").replace(/\\n/g, " "); }
    return "| 格 | 鏡頭（景別，角度，運鏡） | 動作 | 對白 | 補充 |\\n|---|---|---|---|---|\\n" + S.p.map(function (p, i) { return "| " + (i + 1) + " | " + c(label(p)) + " | " + c(p.text) + " | " + c(p.dial) + " | " + c(p.note) + " |"; }).join("\\n");
  }
  function view() {
    var p = S.p[S.i];
    stage.innerHTML = frame(p);
    auto.innerHTML = "<b>第 " + (S.i + 1) + " 格的鏡頭欄會寫:</b>" + label(p) + '<br><span style="color:var(--gray-500);font-size:13px">角度只會寫在文字裡,預覽畫面不會跟著傾斜或升高。</span>';
    why.hidden = !p.why; if (p.why) why.innerHTML = "<b>參考答案的理由:</b>" + esc(p.why) + "(這只是其中一種拍法,不是唯一答案。)";
    strips(); table(); sync();
  }
  function commit() { save(); view(); }
  document.getElementById("ctl").addEventListener("input", function (e) {
    var el = e.target, k = el.dataset.k; if (!k) return; var p = S.p[S.i]; delete p.why;
    p[k] = k === "parrow" ? el.value === "1" : el.value;
    if (k === "subj" && p.subj === "note") p.size = "ecu";
    commit();
  });
  strip.addEventListener("click", function (e) { var b = e.target.closest(".th"); if (b) { S.i = +b.dataset.i; view(); } });
  var armedTimer = {};
  function arm(btn, fn, textArmed) {
    var orig = btn.textContent;
    btn.addEventListener("click", function () {
      if (btn.classList.contains("armed")) { btn.classList.remove("armed"); btn.textContent = orig; clearTimeout(armedTimer[btn.id]); fn(); return; }
      btn.classList.add("armed"); btn.textContent = textArmed;
      armedTimer[btn.id] = setTimeout(function () { btn.classList.remove("armed"); btn.textContent = orig; }, 3000);
    });
  }
  document.getElementById("bAdd").addEventListener("click", function () { if (S.p.length >= 16) return; S.p.splice(S.i + 1, 0, blank()); S.i++; commit(); });
  document.getElementById("bUp").addEventListener("click", function () { if (S.i > 0) { var t = S.p[S.i]; S.p[S.i] = S.p[S.i - 1]; S.p[S.i - 1] = t; S.i--; commit(); } });
  document.getElementById("bDown").addEventListener("click", function () { if (S.i < S.p.length - 1) { var t = S.p[S.i]; S.p[S.i] = S.p[S.i + 1]; S.p[S.i + 1] = t; S.i++; commit(); } });
  arm(document.getElementById("bDel"), function () { if (S.p.length > 1) { S.p.splice(S.i, 1); S.i = Math.max(0, S.i - 1); } else S.p = [blank()]; commit(); }, "再按一次確認刪除");
  arm(document.getElementById("bRef"), function () { S.p = clone(REF); S.i = 0; commit(); }, "會取代目前內容,再按一次");
  arm(document.getElementById("bReset"), function () { S.p = clone(DEF); S.i = 0; commit(); }, "會取代目前內容,再按一次");
  arm(document.getElementById("bClear"), function () { S.p = [blank()]; S.i = 0; commit(); }, "全部清掉,再按一次");
  var cb = document.getElementById("bCopy");
  cb.addEventListener("click", function () {
    var t = md(); function done() { cb.classList.add("ok"); cb.textContent = "已複製!"; setTimeout(function () { cb.classList.remove("ok"); cb.textContent = "複製分鏡表"; }, 1200); }
    function fb() { var ta = document.createElement("textarea"); ta.value = t; ta.style.position = "fixed"; ta.style.opacity = "0"; document.body.appendChild(ta); ta.select(); try { document.execCommand("copy"); } catch (e) {} document.body.removeChild(ta); done(); }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(done, fb); else fb();
  });
  S.p = load() || clone(DEF); view();
})();
</script>""".replace("__SZ__", json.dumps(SZJ, ensure_ascii=False)).replace("__DEF__", json.dumps(DEF, ensure_ascii=False)).replace("__REF__", json.dumps(REF, ensure_ascii=False))

SPEC = defaults(
  file="microfilm-practice-guide.html",
  title="實作:把《紙條》劇本畫成分鏡表(分鏡編輯器)",
  eyebrow="第 15 篇 · 實作:把劇本畫成分鏡",
  h1="實作:把《紙條》畫成一份完整的分鏡表",
  sub="不學新東西,把前面學的全部用起來。用分鏡編輯器選景別、角色、運鏡,畫面自動畫出來,最後複製分鏡表帶走,也可以改成自己的故事。",
  tldr="選一格 → 選<strong>景別、角色、運鏡</strong> → 寫<strong>動作與對白</strong>,六段《紙條》各先畫一格。卡住就按<strong>套用參考答案</strong>看一種拍法再自己改。完成後<strong>複製分鏡表</strong>;想挑戰就改成自己的故事。",
  toc=[("start", "任務"), ("ed", "分鏡編輯器"), ("out", "複製分鏡表"), ("review", "自我檢查"), ("practice", "測驗與檢查")],
  body="\n\n".join([start, ed, out, review, practice]),
  config=dict(sim={}, quiz=QUIZ), js=JS + CHOOSE_JS, css=MF_CSS + PAGE_CSS,
  prev=("microfilm-scenes-guide.html", "情節配鏡頭速查"), next=("microfilm-prep-guide.html", "拍攝前準備"),
)
