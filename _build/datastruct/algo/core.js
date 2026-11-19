(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  function esc(s){ return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;"); }
  A.esc = esc;

  /* ---------- 極簡 C++ 語法上色(每行一個 <span class="l">,換行字元保留在 span 內,複製時不會掉) ---------- */
  var KW = /^(?:auto|break|case|const|constexpr|continue|default|delete|do|else|enum|false|for|if|namespace|new|nullptr|operator|private|public|return|sizeof|static|static_cast|struct|switch|template|this|true|typedef|using|while|class|void|int|long|short|unsigned|signed|char|bool|float|double)$/;
  var TY = /^(?:vector|string|size_t|cout|cin|cerr|endl|array|list|stack|queue|deque|map|set|unordered_map|unordered_set|priority_queue|pair|sort|swap|min|max|begin|end|int64_t)$/;
  var RE = /(\/\/[^\n]*)|("(?:\\.|[^"\\\n])*")|('(?:\\.|[^'\\\n])+')|(^[ \t]*#[^\n]*)|(\b\d+(?:\.\d+)?\b)|(\b[A-Za-z_]\w*\b)/g;
  function hlInline(line){
    var out = "", last = 0, m; RE.lastIndex = 0;
    while ((m = RE.exec(line))){
      out += esc(line.slice(last, m.index));
      var t = m[0], c = null;
      if (m[1]) c = "c"; else if (m[2] || m[3]) c = "s"; else if (m[4]) c = "p"; else if (m[5]) c = "n";
      else if (KW.test(t)) c = "k"; else if (TY.test(t)) c = "t";
      out += c ? '<span class="x' + c + '">' + esc(t) + "</span>" : esc(t);
      last = RE.lastIndex;
    }
    return out + esc(line.slice(last));
  }
  A.hlCpp = function (code) {
    return code.replace(/\n$/, "").split("\n").map(function (ln) {
      return '<span class="l">' + hlInline(ln) + "\n</span>";
    }).join("");
  };
  A.highlightAll = function () {
    if (typeof document === "undefined") return;
    Array.prototype.forEach.call(document.querySelectorAll("pre[data-cpp]"), function (pre) {
      pre.innerHTML = A.hlCpp(pre.textContent);
    });
  };

  /* ---------- 通用播放器 widget ----------
     o = { form:[{id,label,type:'select'|'number'|'text',options,value,min,max,showIf}], runLabel,
           init():base, idle(base):frame, make(vals, base):{frames,result}|{error},
           render(frame):html, code:string|null, code_cap:string }
     frame = { msg, line:number|[number], ...(由 render 決定其餘欄位) }                                 */
  var SPEEDS = { slow: 1400, mid: 800, fast: 350 };
  A.widget = function (id, o) {
    if (typeof document === "undefined") return null;
    var root = document.getElementById(id); if (!root) return null;
    root.classList.add("algo-w");
    var form = (o.form || []).map(function (f) {
      var inner;
      if (f.type === "select") inner = '<select id="' + id + "-" + f.id + '">' + f.options.map(function (op) {
        return '<option value="' + esc(op[0]) + '"' + (op[0] === f.value ? " selected" : "") + ">" + esc(op[1]) + "</option>"; }).join("") + "</select>";
      else inner = '<input id="' + id + "-" + f.id + '" type="' + (f.type || "text") + '" value="' + esc(f.value === undefined ? "" : f.value) + '"' +
        (f.min !== undefined ? ' min="' + f.min + '"' : "") + (f.max !== undefined ? ' max="' + f.max + '"' : "") + ' autocomplete="off">';
      return '<div class="algo-f" data-f="' + f.id + '"><label for="' + id + "-" + f.id + '">' + esc(f.label) + "</label>" + inner + "</div>";
    }).join("");
    var extra = (o.buttons || []).map(function (b, i) { return '<button type="button" class="ghost" data-x="' + i + '">' + esc(b.label) + "</button>"; }).join("");
    root.innerHTML =
      '<div class="algo-form">' + form + '<button type="button" class="primary" data-a="run">' + esc(o.runLabel || "執行") + "</button>" + extra +
      '<button type="button" class="ghost" data-a="reset">Reset</button></div>' +
      '<div class="algo-main' + (o.code ? "" : " nocode") + '">' +
      '<div class="algo-left" tabindex="0" aria-label="動畫區:按左右方向鍵逐步,空白鍵播放或暫停">' +
        '<div class="algo-stage"></div><div class="algo-msg" aria-live="polite"></div>' +
        '<div class="algo-ctl"><button type="button" class="ghost" data-a="first" title="回到第一步">⏮</button>' +
        '<button type="button" class="ghost" data-a="prev">← 上一步</button>' +
        '<button type="button" class="primary" data-a="next">下一步 →</button>' +
        '<button type="button" class="ghost" data-a="play">▶ 播放</button>' +
        '<select data-a="speed" aria-label="播放速度"><option value="slow">慢</option><option value="mid" selected>中</option><option value="fast">快</option></select>' +
        '<input type="range" data-a="seek" min="0" max="0" value="0" aria-label="步驟"><span class="algo-step"></span></div></div>' +
      (o.code ? '<div class="cmd algo-code"><div class="cap">' + esc(o.code_cap || "程式碼(目前執行的那一行會亮起來)") + "</div><pre>" + A.hlCpp(o.code) + "</pre></div>" : "") +
      "</div>";
    var $ = function (s) { return root.querySelector(s); };
    var stage = $(".algo-stage"), msg = $(".algo-msg"), step = $(".algo-step"), seek = $('[data-a="seek"]'),
        btnPrev = $('[data-a="prev"]'), btnNext = $('[data-a="next"]'), btnPlay = $('[data-a="play"]'), btnFirst = $('[data-a="first"]');
    var lines = o.code ? Array.prototype.slice.call(root.querySelectorAll(".algo-code .l")) : [];
    var base = o.init(), frames = [o.idle(base)], idx = 0, timer = null;

    function vals() {
      var v = {}; (o.form || []).forEach(function (f) {
        var el = document.getElementById(id + "-" + f.id); v[f.id] = f.type === "number" ? (el.value === "" ? NaN : +el.value) : el.value; });
      return v;
    }
    function showIf() {
      var v = vals();
      (o.form || []).forEach(function (f) {
        if (!f.showIf) return;
        var ok = Object.keys(f.showIf).every(function (k) { return [].concat(f.showIf[k]).map(String).indexOf(String(v[k])) !== -1; });
        $('[data-f="' + f.id + '"]').hidden = !ok;
      });
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; } btnPlay.textContent = "▶ 播放"; }
    function show() {
      var f = frames[idx];
      stage.innerHTML = o.render(f);
      msg.className = "algo-msg"; msg.innerHTML = f.msg || "";
      var on = f.line === undefined ? [] : [].concat(f.line);
      lines.forEach(function (l, i) { l.classList.toggle("on", on.indexOf(i + 1) !== -1); });
      if (on.length && lines[on[0] - 1]) { var el = lines[on[0] - 1], pre = el.parentNode;
        if (el.offsetTop < pre.scrollTop || el.offsetTop + el.offsetHeight > pre.scrollTop + pre.clientHeight) pre.scrollTop = Math.max(0, el.offsetTop - pre.clientHeight / 3); }
      var last = frames.length - 1;
      seek.max = last; seek.value = idx; seek.disabled = last === 0;
      step.textContent = last === 0 ? "尚未執行" : "步驟 " + (idx + 1) + " / " + frames.length;
      btnPrev.disabled = idx === 0; btnFirst.disabled = idx === 0;
      btnNext.disabled = idx >= last; btnPlay.disabled = last === 0;
    }
    function go(i) { idx = Math.max(0, Math.min(frames.length - 1, i)); show(); }
    function play() {
      if (timer) { stop(); return; }
      if (idx >= frames.length - 1) go(0);
      btnPlay.textContent = "⏸ 暫停";
      timer = setInterval(function () { if (idx >= frames.length - 1) { stop(); return; } go(idx + 1); if (idx >= frames.length - 1) stop(); },
        SPEEDS[$('[data-a="speed"]').value] || 800);
    }
    function run(v) {
      stop();
      var r = o.make(v, base);
      if (r.error) { msg.className = "algo-msg err"; msg.textContent = r.error; return false; }
      frames = r.frames; base = r.result; go(0); return true;
    }
    function reset() { stop(); base = o.init(); frames = [o.idle(base)]; idx = 0; show(); }

    root.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-a],button[data-x]"); if (!b || !root.contains(b)) return;
      if (b.dataset.x !== undefined) { var bx = o.buttons[+b.dataset.x]; if (bx.run) { bx.run(vals(), { base: base, setBase: function (b) { stop(); base = b; frames = [o.idle(base)]; idx = 0; show(); }, set: function (k, val) { document.getElementById(id + "-" + k).value = val; showIf(); }, run: function () { run(vals()); } }); } return; }
      var a = b.dataset.a;
      if (a === "run") run(vals()); else if (a === "reset") reset();
      else if (a === "next") { stop(); go(idx + 1); } else if (a === "prev") { stop(); go(idx - 1); }
      else if (a === "first") { stop(); go(0); } else if (a === "play") play();
    });
    seek.addEventListener("input", function () { stop(); go(+seek.value); });
    root.addEventListener("change", function (e) { if (e.target.closest(".algo-form")) showIf(); });
    $(".algo-left").addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); stop(); go(idx + 1); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); stop(); go(idx - 1); }
      else if (e.key === " ") { e.preventDefault(); play(); }
    });
    showIf(); show();
    var api = { run: run, reset: reset, go: go, frames: function () { return frames; }, base: function () { return base; } };
    root._algo = api; return api;
  };
  if (typeof document !== "undefined") A.highlightAll();
})(typeof window !== "undefined" ? window : globalThis);
