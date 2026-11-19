(function () {
  "use strict";
  var U = window.PAGE_UTIL || {}, CFG = window.PAGE || {};
  function esc(s){ return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;"); }

  /* ---------- 程式碼區塊:複製 + 點選逐行說明 ---------- */
  Array.prototype.forEach.call(document.querySelectorAll(".code"), function (box) {
    var pre = box.querySelector("pre"), btn = box.querySelector("button.copy");
    var note = box.nextElementSibling && box.nextElementSibling.classList.contains("code-note") ? box.nextElementSibling : null;
    var lines = Array.prototype.slice.call(pre.querySelectorAll(".ln"));
    if (btn) btn.addEventListener("click", function () {
      U.copyText(lines.map(function (l) { return l.textContent; }).join("\n") + "\n", btn);
    });
    if (!note) return;
    function show(l) {
      lines.forEach(function (x) { x.classList.toggle("sel", x === l); });
      note.innerHTML = "<b>第 " + (lines.indexOf(l) + 1) + " 行</b>";
      note.appendChild(document.createTextNode(l.dataset.note));
    }
    lines.forEach(function (l) {
      if (!l.dataset.note) return;
      l.addEventListener("click", function () { show(l); });
      l.addEventListener("keydown", function (ev) { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); show(l); } });
    });
  });

  /* ---------- Flow 引擎:節點依序播放,可選擇讓某一步失敗 ---------- */
  var FL = CFG.flow || {};
  Array.prototype.forEach.call(document.querySelectorAll("[data-flow]"), function (el) {
    var f = FL[el.dataset.flow]; if (!f) return;
    var i = 0, fail = false, n = f.nodes.length, hasFail = typeof f.failAt === "number";
    el.classList.add("flow");
    el.innerHTML = '<div class="flow-row" role="group" aria-label="流程"></div><div class="flow-detail" aria-live="polite"></div>' +
      '<div class="flow-ctl"><button type="button" class="ghost" data-a="prev">← 上一步</button><button type="button" class="primary" data-a="next">下一步 →</button>' +
      '<button type="button" class="ghost" data-a="reset">Reset</button>' +
      (hasFail ? '<label><input type="checkbox" data-a="fail">假設' + esc(f.failLabel || "這一步出錯") + '</label>' : "") + "</div>";
    var row = el.querySelector(".flow-row"), det = el.querySelector(".flow-detail");
    var bPrev = el.querySelector('[data-a="prev"]'), bNext = el.querySelector('[data-a="next"]');
    function limit(){ return fail ? f.failAt : n - 1; }
    function render() {
      if (i > limit()) i = limit();
      row.innerHTML = f.nodes.map(function (nd, k) {
        var cls = "";
        if (fail && k > f.failAt) cls = "skip";
        else if (fail && k === f.failAt && i >= k) cls = "fail";
        else if (k < i) cls = "done"; else if (k === i) cls = "on";
        return (k ? '<span class="flow-arrow" aria-hidden="true">→</span>' : "") +
          '<button type="button" class="flow-node ' + cls + '" data-k="' + k + '"><b>' + nd.t + "</b><small>" + nd.s + "</small></button>";
      }).join("");
      var bad = fail && i === f.failAt;
      det.classList.toggle("bad", bad);
      det.innerHTML = bad ? f.failText : f.nodes[i].d;
      bPrev.disabled = i === 0; bNext.disabled = i >= limit();
    }
    row.addEventListener("click", function (ev) { var b = ev.target.closest("[data-k]"); if (b){ i = +b.dataset.k; render(); } });
    el.addEventListener("click", function (ev) {
      var a = ev.target.closest("[data-a]"); if (!a) return;
      if (a.dataset.a === "prev" && i > 0) i--;
      else if (a.dataset.a === "next" && i < limit()) i++;
      else if (a.dataset.a === "reset"){ i = 0; fail = false; var c = el.querySelector('[data-a="fail"]'); if (c) c.checked = false; }
      else if (a.dataset.a === "fail"){ fail = a.checked; }
      render();
    });
    render();
  });


  /* 記憶體格子:cells = [{id, names[], v, t, a, p(指向的格子 id)}];箭頭由 SVG 依格子位置畫出 */
  function drawMem(box, cells) {
    box.innerHTML = '<div class="mm-wrap"><svg class="mm-svg" aria-hidden="true"></svg><div class="mm-row"></div></div><div class="stp-base">位址為示意,實際數字每台電腦、每次執行都不同</div>';
    var wrap = box.querySelector(".mm-wrap"), row = box.querySelector(".mm-row"), svg = box.querySelector(".mm-svg");
    row.innerHTML = cells.map(function (c) {
      return '<div class="mm-cell' + (c.p ? " ptr" : "") + '" data-id="' + esc(c.id) + '"><div class="mm-n">' + c.names.map(esc).join(" / ") + '</div><div class="mm-v">' + esc(c.v) + '</div><div class="mm-t">' + esc((c.t || "") + (c.a ? " @" + c.a : "")) + "</div></div>";
    }).join("");
    var W = row.scrollWidth, H = 54, p = "";
    svg.setAttribute("width", W); svg.setAttribute("height", H); svg.setAttribute("viewBox", "0 0 " + W + " " + H);
    cells.forEach(function (c) {
      if (!c.p) return;
      var a = row.querySelector('[data-id="' + c.id + '"]'), b = row.querySelector('[data-id="' + c.p + '"]'); if (!a || !b) return;
      var x1 = a.offsetLeft + a.offsetWidth / 2, x2 = b.offsetLeft + b.offsetWidth / 2, y = H;
      p += '<path d="M' + x1 + " " + y + " C" + x1 + " " + (y - 46) + " " + x2 + " " + (y - 46) + " " + x2 + " " + (y - 9) + '" fill="none" stroke="#D97757" stroke-width="2"/>' +
        '<path d="M' + (x2 - 5) + " " + (y - 9) + " L" + (x2 + 5) + " " + (y - 9) + " L" + x2 + " " + (y - 1) + ' Z" fill="#D97757"/>';
    });
    svg.innerHTML = p;
  }


  /* stack / heap 兩區的記憶體圖:cells 帶 r:"heap" 的畫在下方;leak=洩漏、free=已歸還、dangling=懸空箭頭(虛線) */
  function drawMem2(box, cells) {
    function cell(c) {
      return '<div class="mm-cell' + (c.p ? " ptr" : "") + (c.free ? " freed" : "") + (c.leak ? " leak" : "") + '" data-id="' + esc(c.id) + '"><div class="mm-n">' + c.names.map(esc).join(" / ") + '</div><div class="mm-v">' + esc(c.free ? "已歸還" : c.v) + '</div><div class="mm-t">' + esc((c.t || "") + (c.a ? " @" + c.a : "")) + (c.leak ? " · 洩漏" : "") + "</div></div>";
    }
    var st = cells.filter(function (c) { return c.r !== "heap"; }), hp = cells.filter(function (c) { return c.r === "heap"; });
    box.innerHTML = '<div class="mm-wrap2"><svg class="mm-svg2" aria-hidden="true"></svg>' +
      '<div class="mm-reg"><b>stack(函式結束自動收回)</b><div class="mm-row">' + st.map(cell).join("") + '</div></div>' +
      '<div class="mm-reg heap"><b>heap(用 new 要的,要自己還)</b><div class="mm-row">' + (hp.length ? hp.map(cell).join("") : '<span class="mm-empty">(目前沒有)</span>') + "</div></div></div>";
    var wrap = box.querySelector(".mm-wrap2"), svg = box.querySelector(".mm-svg2"), w = wrap.getBoundingClientRect(), p = "";
    svg.setAttribute("width", w.width); svg.setAttribute("height", w.height); svg.setAttribute("viewBox", "0 0 " + w.width + " " + w.height);
    cells.forEach(function (c) {
      if (!c.p) return;
      var a = wrap.querySelector('[data-id="' + c.id + '"]'), b = wrap.querySelector('[data-id="' + c.p + '"]'); if (!a || !b) return;
      var ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect(), x1 = ra.left + ra.width / 2 - w.left, y1 = ra.bottom - w.top, x2 = rb.left + rb.width / 2 - w.left, y2 = rb.top - w.top;
      var col = c.dangling ? "#B04A3F" : "#D97757", dash = c.dangling ? ' stroke-dasharray="5 4"' : "";
      p += '<path d="M' + x1 + " " + y1 + " C" + x1 + " " + (y1 + 34) + " " + x2 + " " + (y2 - 34) + " " + x2 + " " + (y2 - 9) + '" fill="none" stroke="' + col + '" stroke-width="2"' + dash + "/>" +
        '<path d="M' + (x2 - 5) + " " + (y2 - 9) + " L" + (x2 + 5) + " " + (y2 - 9) + " L" + x2 + " " + (y2 - 1) + ' Z" fill="' + col + '"/>';
    });
    svg.innerHTML = p;
  }

  /* ---------- Stepper 引擎:逐行執行,顯示變數盒子與輸出 ---------- */
  var ST = CFG.stepper || {};
  Array.prototype.forEach.call(document.querySelectorAll("[data-stepper]"), function (el) {
    var f = ST[el.dataset.stepper]; if (!f) return;
    var steps = f.steps, i = -1, lines = Array.prototype.slice.call(el.querySelectorAll(".ln"));
    var vars = el.querySelector(".stp-vars"), outp = el.querySelector(".stp-out pre"), note = el.querySelector(".stp-note"), cnt = el.querySelector(".stp-count");
    var bPrev = el.querySelector('[data-a="prev"]'), bNext = el.querySelector('[data-a="next"]');
    function render() {
      lines.forEach(function (l, k) { l.classList.toggle("cur", i >= 0 && steps[i].l === k); });
      if (i >= 0 && steps[i].m) {   // 記憶體格子與箭頭模式
        vars.className = "stp-vars mem"; if (steps[i].m.some(function (c) { return c.r; })) drawMem2(vars, steps[i].m); else drawMem(vars, steps[i].m);
      } else if (i < 0 && f.mem) { vars.className = "stp-vars mem"; vars.innerHTML = '<div class="stp-base">記憶體(還沒開始)</div>';
      } else if (i >= 0 && steps[i].f) {   // 呼叫堆疊模式:最上面是目前正在執行的函式
        vars.className = "stp-vars frames";
        vars.innerHTML = steps[i].f.slice().reverse().map(function (fr, k) {
          return '<div class="stp-frame' + (k === 0 ? " top" : "") + '"><div class="stp-fh">' + esc(fr.t) + (fr.r ? ' <span class="stp-ret">回傳 ' + esc(fr.r) + "</span>" : "") + "</div><div class=\"stp-fv\">" +
            Object.keys(fr.v).map(function (nm) { return "<span><small>" + esc(nm) + "</small><b>" + esc(fr.v[nm]) + "</b></span>"; }).join("") + "</div></div>";
        }).join("") + '<div class="stp-base">呼叫堆疊(上面是最新呼叫)</div>';
      } else if (f.frames) { vars.className = "stp-vars frames"; vars.innerHTML = '<div class="stp-base">呼叫堆疊(還沒開始)</div>'; }
      else {
      vars.className = "stp-vars";
      var cur = i >= 0 ? steps[i].v : {}, prv = i > 0 ? steps[i - 1].v : {};
      vars.innerHTML = f.names.map(function (nm) {
        var has = Object.prototype.hasOwnProperty.call(cur, nm);
        return '<div class="stp-var' + (has ? (cur[nm] !== prv[nm] ? " chg" : "") : " none") + '"><small>' + esc((f.types && f.types[nm] ? f.types[nm] + " " : "") + nm) + "</small><b>" + (has ? esc(cur[nm]) : "—") + "</b></div>";
      }).join("");
      }
      outp.textContent = steps.slice(0, i + 1).map(function (s) { return s.o || ""; }).join("");
      note.textContent = i >= 0 ? (steps[i].n || "") : "按「下一步」,程式會一行一行執行。";
      cnt.textContent = (i + 1) + " / " + steps.length;
      bPrev.disabled = i < 0; bNext.disabled = i >= steps.length - 1;
    }
    el.addEventListener("click", function (ev) {
      var a = ev.target.closest("[data-a]"); if (!a) return;
      if (a.dataset.a === "next" && i < steps.length - 1) i++;
      else if (a.dataset.a === "prev" && i >= 0) i--;
      else if (a.dataset.a === "reset") i = -1;
      render();
    });
    render();
  });

  /* ---------- Calc 引擎(overflow):輸入整數,看存進某個型態之後變成多少 ---------- */
  var CA = CFG.calc || {};
  var TYPES = [["char", 8, true], ["short", 16, true], ["int", 32, true], ["long long", 64, true], ["unsigned char", 8, false], ["unsigned int", 32, false]];
  Array.prototype.forEach.call(document.querySelectorAll("[data-calc]"), function (el) {
    var f = CA[el.dataset.calc]; if (!f || f.kind !== "overflow" || typeof BigInt === "undefined") return;
    el.classList.add("calc");
    el.innerHTML = '<div class="calc-row"><div><label for="cT">型態</label><select id="cT">' + TYPES.map(function (t, k) { return '<option value="' + k + '"' + (k === 2 ? " selected" : "") + ">" + t[0] + "</option>"; }).join("") +
      '</select></div><div><label for="cV">要存進去的整數</label><input id="cV" inputmode="numeric" value="2147483648" autocomplete="off"></div><button type="button" class="ghost" data-a="reset">Reset</button></div>' +
      '<div class="calc-pre"></div><div class="calc-out" aria-live="polite"></div><p class="calc-foot">這裡示範「把超出範圍的數字存進變數」的常見結果:會像時鐘一樣繞一圈。<code>char</code> 是否有號由平台決定,這裡以常見的有號版本計算。</p>';
    var sel = el.querySelector("#cT"), inp = el.querySelector("#cV"), out = el.querySelector(".calc-out"), pre = el.querySelector(".calc-pre");
    var PRESETS = [["int 最大值", 2, "2147483647"], ["int 最大值 + 1", 2, "2147483648"], ["200 存進 char", 0, "200"], ["−1 存進 unsigned int", 5, "-1"]];
    pre.innerHTML = PRESETS.map(function (p, k) { return '<button type="button" class="ghost" data-p="' + k + '">' + p[0] + "</button>"; }).join("");
    function render() {
      var t = TYPES[+sel.value], bits = BigInt(t[1]), s = inp.value.trim();
      var ONE = BigInt(1), lo = t[2] ? -(ONE << (bits - ONE)) : BigInt(0), hi = t[2] ? (ONE << (bits - ONE)) - ONE : (ONE << bits) - ONE;
      var rng = "<b>" + t[0] + "</b> 能存的範圍:<code>" + lo + " ~ " + hi + "</code>(" + t[1] + " 位元)";
      if (!/^-?\d{1,25}$/.test(s)) { out.innerHTML = rng + "<br>請輸入整數(最多 25 位)。"; return; }
      var v = BigInt(s), w = t[2] ? BigInt.asIntN(t[1], v) : BigInt.asUintN(t[1], v), fits = v >= lo && v <= hi;
      out.innerHTML = rng + '<br>你輸入 <code>' + v + "</code>,存進去之後是 <b><code>" + w + "</code></b> " +
        (fits ? '<span class="badge ok">在範圍內</span>' : '<span class="badge warn">超出範圍,繞了一圈</span>');
    }
    el.addEventListener("input", render);
    el.addEventListener("click", function (ev) {
      var b = ev.target.closest("button"); if (!b) return;
      if (b.dataset.p !== undefined) { var p = PRESETS[+b.dataset.p]; sel.value = p[1]; inp.value = p[2]; }
      else if (b.dataset.a === "reset") { sel.value = 2; inp.value = "2147483648"; }
      render();
    });
    render();
  });

  /* ---------- Calc 引擎(format):模擬 cout 的 fixed / setprecision / setw / left ---------- */
  function gfmt(x, P) {
    if (P === 0) P = 1; if (x === 0) return "0";
    var m = x.toExponential(P - 1).split("e"), X = parseInt(m[1], 10);
    if (X < -4 || X >= P) {
      var mant = m[0].indexOf(".") >= 0 ? m[0].replace(/0+$/, "").replace(/\.$/, "") : m[0], a = Math.abs(X);
      return mant + "e" + (X < 0 ? "-" : "+") + (a < 10 ? "0" + a : a);
    }
    var f = x.toFixed(Math.max(0, P - 1 - X));
    return f.indexOf(".") >= 0 ? f.replace(/0+$/, "").replace(/\.$/, "") : f;
  }
  function cfmt(x, p, fixed, w, left) {
    var s = fixed ? x.toFixed(p) : gfmt(x, p);
    while (s.length < w) s = left ? s + " " : " " + s;
    return s;
  }
  window.CLANG_FMT = cfmt;
  Array.prototype.forEach.call(document.querySelectorAll("[data-calc]"), function (el) {
    var f = CA[el.dataset.calc]; if (!f || f.kind !== "format") return;
    var VALS = ["3.14159265", "2.71828", "1234.5678", "0.000123456", "100"];
    el.classList.add("calc");
    el.innerHTML = '<div class="calc-row"><div><label for="fV">要輸出的數字</label><select id="fV">' + VALS.map(function (v) { return "<option>" + v + "</option>"; }).join("") + "</select></div>" +
      '<div><label for="fP">setprecision</label><input id="fP" type="number" min="0" max="10" value="6" style="width:84px"></div>' +
      '<div><label for="fW">setw</label><input id="fW" type="number" min="0" max="16" value="0" style="width:84px"></div>' +
      '<label class="calc-chk"><input id="fF" type="checkbox">fixed</label><label class="calc-chk"><input id="fL" type="checkbox">left</label><button type="button" class="ghost" data-a="reset">Reset</button></div>' +
      '<div class="calc-out" aria-live="polite"></div><p class="calc-foot">不加 <code>fixed</code> 時,<code>setprecision(n)</code> 代表「總共 n 位有效數字」;加了 <code>fixed</code> 就變成「小數點後 n 位」。<code>setw</code> 只影響緊接著的那一個輸出。</p>';
    var $v = el.querySelector("#fV"), $p = el.querySelector("#fP"), $w = el.querySelector("#fW"), $f = el.querySelector("#fF"), $l = el.querySelector("#fL"), out = el.querySelector(".calc-out");
    function clamp(n, lo, hi) { n = parseInt(n, 10); return isNaN(n) ? lo : Math.max(lo, Math.min(hi, n)); }
    function render() {
      var p = clamp($p.value, 0, 10), w = clamp($w.value, 0, 16), fx = $f.checked, lf = $l.checked;
      var code = "cout &lt;&lt; " + (fx ? "fixed &lt;&lt; " : "") + "setprecision(" + p + ") &lt;&lt; " + (lf ? "left &lt;&lt; " : "") + (w ? "setw(" + w + ") &lt;&lt; " : "") + $v.value + ";";
      out.innerHTML = "<code>" + code + "</code><br>輸出(<code>|</code> 是邊界記號):<pre class=\"calc-pre2\">|" + esc(cfmt(parseFloat($v.value), p, fx, w, lf)) + "|</pre>";
    }
    el.addEventListener("input", render);
    el.addEventListener("click", function (ev) { var b = ev.target.closest('[data-a="reset"]'); if (!b) return; $v.selectedIndex = 0; $p.value = 6; $w.value = 0; $f.checked = false; $l.checked = false; render(); });
    render();
  });

  /* ---------- 運算式求值追蹤器:依 C++ 優先序,一次只算一個運算 ---------- */
  var LEVELS = [["*", "/", "%"], ["+", "-"], ["<", ">", "<=", ">="], ["==", "!="], ["&&"], ["||"]];
  function show(toks, a, b) {
    var out = "";
    toks.forEach(function (t, k) {
      var s = t.n !== undefined ? String(t.n) : t.o, p = toks[k - 1];
      if (k === a) s = "<mark>" + s; if (k === b) s += "</mark>";
      out += (k === 0 || (p && (p.u || p.o === "(")) || t.o === ")" ? "" : " ") + s;
    });
    return out;
  }
  function evalSteps(src) {
    var s = src.replace(/\s+/g, ""), toks = [], i = 0, m, re = /^(\d+|<=|>=|==|!=|&&|\|\||[-+*\/%<>!()])/;
    if (!s) return { err: "請輸入一個運算式。" };
    if (/\+\+|--/.test(src)) return { err: "這裡不支援 ++ 與 --(它們只能用在變數上)。要連續兩個負號,請中間加空格或括號。" };
    while (i < s.length) {
      m = re.exec(s.slice(i));
      if (!m) return { err: "看不懂「" + s[i] + "」。這裡只支援整數與 + - * / % < > <= >= == != && || ! ( )" };
      i += m[0].length; toks.push(/^\d/.test(m[0]) ? { n: parseInt(m[0], 10) } : { o: m[0] });
    }
    toks.forEach(function (t, k) {
      if (t.o === "!") t.u = true;
      if (t.o === "-") { var p = toks[k - 1]; if (!p || (p.o && p.o !== ")")) t.u = true; }
    });
    var steps = [], guard = 0;
    while (guard++ < 200) {
      if (toks.length === 1 && toks[0].n !== undefined) return { ok: true, value: toks[0].n, steps: steps };
      var open = -1, close = -1, k;
      for (k = 0; k < toks.length; k++) { if (toks[k].o === "(") open = k; else if (toks[k].o === ")") { close = k; break; } }
      if (close > -1 && open < 0 || close < 0 && open > -1) return { err: "括號沒有成對。", steps: steps };
      var lo = close > -1 ? open + 1 : 0, hi = close > -1 ? close : toks.length;
      if (close > -1 && hi - lo === 1 && toks[lo].n !== undefined) {
        steps.push({ h: show(toks, open, close), t: "括號裡只剩一個數字,把括號拿掉。" }); toks.splice(close, 1); toks.splice(open, 1); continue;
      }
      var done = false;
      for (k = hi - 2; k >= lo && !done; k--) {   // 單元運算子:! 與負號
        if (toks[k].u && toks[k + 1].n !== undefined) {
          var x = toks[k + 1].n, v = toks[k].o === "!" ? (x ? 0 : 1) : 0 - x;
          steps.push({ h: show(toks, k, k + 1), t: toks[k].o === "!" ? "! 把真假反過來:" + (x ? "非 0 是真" : "0 是假") + ",所以得到 " + v + "。" : "負號:得到 " + v + "。" });
          toks.splice(k, 2, { n: v }); done = true;
        }
      }
      for (var L = 0; L < LEVELS.length && !done; L++) {
        for (k = lo + 1; k < hi - 1 && !done; k++) {
          var t = toks[k];
          if (!t.o || t.u || LEVELS[L].indexOf(t.o) < 0 || toks[k - 1].n === undefined || toks[k + 1].n === undefined) continue;
          var l = toks[k - 1].n, r = toks[k + 1].n, v2, note = "";
          switch (t.o) {
            case "*": v2 = l * r; note = "乘法。"; break;
            case "/": if (r === 0) return { err: "除以 0:這在 C++ 裡不能算(整數除以 0 會讓程式當掉)。", steps: steps }; v2 = Math.trunc(l / r); note = (l % r !== 0) ? "整數除法:小數部分直接捨去,不是四捨五入。" : "整除,沒有餘數。"; break;
            case "%": if (r === 0) return { err: "對 0 取餘數:這在 C++ 裡不能算。", steps: steps }; v2 = l % r; note = "取餘數:結果的正負號跟著左邊的數。"; break;
            case "+": v2 = l + r; note = "加法。"; break;
            case "-": v2 = l - r; note = "減法。"; break;
            case "<": v2 = l < r ? 1 : 0; note = "比較的結果:成立是 1(true),不成立是 0(false)。"; break;
            case ">": v2 = l > r ? 1 : 0; note = "比較的結果:成立是 1(true),不成立是 0(false)。"; break;
            case "<=": v2 = l <= r ? 1 : 0; note = "比較的結果:成立是 1(true),不成立是 0(false)。"; break;
            case ">=": v2 = l >= r ? 1 : 0; note = "比較的結果:成立是 1(true),不成立是 0(false)。"; break;
            case "==": v2 = l === r ? 1 : 0; note = "是否相等:成立是 1,不成立是 0。"; break;
            case "!=": v2 = l !== r ? 1 : 0; note = "是否不相等:成立是 1,不成立是 0。"; break;
            case "&&": v2 = (l && r) ? 1 : 0; note = "而且:兩邊都不是 0 才是 1。"; break;
            case "||": v2 = (l || r) ? 1 : 0; note = "或者:只要有一邊不是 0 就是 1。"; break;
          }
          v2 = v2 + 0;   // 避免出現 -0
          if (Math.abs(v2) > 2147483647) note += "(注意:超出 int 的範圍,真實程式會溢位。)";
          steps.push({ h: show(toks, k - 1, k + 1), t: l + " " + t.o + " " + r + " = " + v2 + "。" + note });
          toks.splice(k - 1, 3, { n: v2 }); done = true;
        }
      }
      if (!done) return { err: "運算式不完整或寫法不對,例如少了數字或運算子。", steps: steps };
    }
    return { err: "運算式太長了。" };
  }
  window.CLANG_EVAL = evalSteps;
  Array.prototype.forEach.call(document.querySelectorAll("[data-calc]"), function (el) {
    var f = CA[el.dataset.calc]; if (!f || f.kind !== "eval") return;
    var P = f.presets || [];
    el.classList.add("calc");
    el.innerHTML = '<div class="calc-row"><div style="flex:1 1 260px"><label for="eX">輸入一個整數運算式</label><input id="eX" value="' + esc(P[0] || "2 + 3 * 4") + '" autocomplete="off" spellcheck="false" style="width:100%"></div><button type="button" class="ghost" data-a="reset">Reset</button></div>' +
      '<div class="calc-pre">' + P.map(function (p, k) { return '<button type="button" class="ghost" data-p="' + k + '">' + esc(p) + "</button>"; }).join("") + '</div><div class="calc-out ev-out" aria-live="polite"></div>' +
      '<p class="calc-foot">支援整數與 <code>+ - * / % &lt; &gt; &lt;= &gt;= == != &amp;&amp; || ! ( )</code>。比較與邏輯運算的結果用 1(true)與 0(false)表示,和 C++ 印出來的一樣。</p>';
    var inp = el.querySelector("#eX"), out = el.querySelector(".ev-out");
    function render() {
      var r = evalSteps(inp.value), h = "";
      if (r.steps && r.steps.length) h += "<ol class=\"ev-steps\">" + r.steps.map(function (s) { return "<li><code>" + s.h + "</code><span>" + esc(s.t) + "</span></li>"; }).join("") + "</ol>";
      h += r.err ? '<div class="ev-res bad">' + esc(r.err) + "</div>" : '<div class="ev-res">結果:<b><code>' + r.value + "</code></b></div>";
      out.innerHTML = h;
    }
    el.addEventListener("input", render);
    el.addEventListener("click", function (ev) {
      var b = ev.target.closest("button"); if (!b) return;
      if (b.dataset.p !== undefined) inp.value = P[+b.dataset.p]; else if (b.dataset.a === "reset") inp.value = P[0] || "";
      render();
    });
    render();
  });

  /* ---------- Ladder 引擎:if / else if / else 與 switch 的選分支追蹤 ---------- */
  var LD = CFG.ladder || {};
  Array.prototype.forEach.call(document.querySelectorAll("[data-ladder]"), function (el) {
    var f = LD[el.dataset.ladder]; if (!f) return;
    var sw = f.mode === "switch", id = el.dataset.ladder;
    el.classList.add("calc");
    el.innerHTML = '<div class="calc-row"><div><label for="l' + id + '">' + esc(f.label) + '</label><input id="l' + id + '" type="number" step="1" value="' + f.value + '" style="width:120px"></div>' +
      (sw ? '<label class="calc-chk"><input type="checkbox" data-brk checked>每個 case 結尾都有 break</label>' : "") + '<button type="button" class="ghost" data-a="reset">Reset</button></div>' +
      '<div class="calc-pre">' + (f.presets || []).map(function (p) { return '<button type="button" class="ghost" data-p="' + p + '">' + esc(f.label) + " = " + p + "</button>"; }).join("") + '</div>' +
      '<div class="ld-rows"></div><div class="calc-out ld-sum" aria-live="polite"></div>';
    var inp = el.querySelector("input[type=number]"), rows = el.querySelector(".ld-rows"), sum = el.querySelector(".ld-sum"), brk = el.querySelector("[data-brk]");
    function render() {
      var raw = inp.value.trim(), v = parseInt(raw, 10), html = "", s = "";
      if (!/^-?\d+$/.test(raw) || isNaN(v)) { rows.innerHTML = ""; sum.textContent = "請輸入一個整數。"; return; }
      var n = f.rows.length, st = [], tag = [], i, m = -1;
      if (!sw) {
        var matched = false, log = [];
        for (i = 0; i < n; i++) {
          if (matched) { st.push("skip"); tag.push("(不再檢查)"); continue; }
          var r = window.CLANG_EVAL(f.rows[i].c.replace(new RegExp("\\b" + f.label + "\\b", "g"), "(" + v + ")"));
          if (r.ok && r.value) { st.push("yes"); tag.push("成立 → 執行"); matched = true; log.push(f.rows[i].c + " 成立"); }
          else { st.push("no"); tag.push("不成立 ↓"); log.push(f.rows[i].c + " 不成立"); }
        }
        st.push(matched ? "skip" : "yes"); tag.push(matched ? "(不執行)" : "前面都不成立 → 執行");
        s = "依序檢查:" + log.join(";") + "。" + (matched ? "只有第一個成立的分支會執行,後面的分支完全不會被檢查。" : "所有條件都不成立,執行最後的 else。");
      } else {
        for (i = 0; i < n; i++) if (String(f.rows[i].c) === String(v)) { m = i; break; }
        if (m < 0) m = n;
        var go = brk.checked ? [m] : null, ran = [];
        for (i = 0; i <= n; i++) {
          var run = brk.checked ? i === m : i >= m;
          st.push(run ? "yes" : "skip"); tag.push(run ? "執行" : (i < m ? "(跳過)" : "(沒有執行)"));
          if (run) ran.push(i === n ? "default" : "case " + f.rows[i].c);
        }
        s = "switch 依值直接跳到 " + (m === n ? "default" : "case " + f.rows[m].c) + "。執行:" + ran.join(" → ") + "。" +
          (brk.checked ? "遇到 break 就跳出,後面的 case 不會執行。" : "沒有 break,所以會一路「穿透」往下做,直到 switch 結束。");
      }
      for (i = 0; i <= n; i++) {
        var head = sw ? (i < n ? "case " + f.rows[i].c + ":" : "default:") : (i === 0 ? "if (" + f.rows[0].c + ")" : i < n ? "else if (" + f.rows[i].c + ")" : "else");
        html += '<div class="ld-row ' + st[i] + '"><div class="ld-c"><code>' + esc(head) + '</code><small>' + esc(tag[i]) + '</small></div><div class="ld-a">' + esc(i < n ? f.rows[i].a : f.other) + (sw && brk.checked && i < n ? "<br>break;" : "") + "</div></div>";
      }
      rows.innerHTML = html; sum.textContent = s;
    }
    el.addEventListener("input", render);
    el.addEventListener("click", function (ev) {
      var b = ev.target.closest("button"); if (!b) return;
      if (b.dataset.p !== undefined) inp.value = b.dataset.p; else if (b.dataset.a === "reset") { inp.value = f.value; if (brk) brk.checked = true; }
      render();
    });
    render();
  });

  /* ---------- Loop 追蹤表:for (int i = S; i OP E; i += STEP) { sum += i; } ---------- */
  var CMP = { "<": function (a, b) { return a < b; }, "<=": function (a, b) { return a <= b; }, ">": function (a, b) { return a > b; }, ">=": function (a, b) { return a >= b; } };
  function loopSim(s, e, st, op) {
    var i = s, sum = 0, rows = [], inf = false;
    while (CMP[op](i, e)) {
      sum += i; rows.push({ k: rows.length + 1, i: i, sum: sum });
      i += st;
      if (rows.length > 300) { inf = true; break; }
    }
    return { rows: rows, count: rows.length, sum: sum, inf: inf, last: i };
  }
  window.CLANG_LOOP = loopSim;
  Array.prototype.forEach.call(document.querySelectorAll("[data-calc]"), function (el) {
    var f = CA[el.dataset.calc]; if (!f || f.kind !== "loop") return;
    var P = f.presets;
    el.classList.add("calc");
    el.innerHTML = '<div class="calc-row"><div><label for="lS">起點 i =</label><input id="lS" type="number" value="1" style="width:84px"></div>' +
      '<div><label for="lO">條件 i …</label><select id="lO"><option>&lt;=</option><option>&lt;</option><option>&gt;=</option><option>&gt;</option></select></div>' +
      '<div><label for="lE">終點</label><input id="lE" type="number" value="5" style="width:84px"></div>' +
      '<div><label for="lT">每圈 i +=</label><input id="lT" type="number" value="1" style="width:84px"></div><button type="button" class="ghost" data-a="reset">Reset</button></div>' +
      '<div class="calc-pre">' + P.map(function (p, k) { return '<button type="button" class="ghost" data-p="' + k + '">' + esc(p[0]) + "</button>"; }).join("") + '</div><div class="calc-out lp-out" aria-live="polite"></div>' +
      '<p class="calc-foot">每一圈的主體都是 <code>sum += i;</code>。數字限制在 −99 到 99,超過 300 圈會判定為停不下來。</p>';
    var $S = el.querySelector("#lS"), $O = el.querySelector("#lO"), $E = el.querySelector("#lE"), $T = el.querySelector("#lT"), out = el.querySelector(".lp-out");
    function num(x) { var n = parseInt(x.value, 10); return isNaN(n) ? 0 : Math.max(-99, Math.min(99, n)); }
    function render() {
      var s = num($S), e = num($E), t = num($T), op = $O.value, r = loopSim(s, e, t, op);
      var h = "<code>for (int i = " + s + "; i " + esc(op) + " " + e + "; i += " + t + ") { sum += i; }</code>";
      if (r.count) {
        var shown = r.rows.slice(0, 15);
        h += '<div class="tbl-wrap"><table class="lp-tbl"><thead><tr><th>第幾圈</th><th>進入時 i</th><th>加完後 sum</th></tr></thead><tbody>' +
          shown.map(function (x) { return "<tr><td>" + x.k + "</td><td>" + x.i + "</td><td>" + x.sum + "</td></tr>"; }).join("") +
          (r.count > 15 ? '<tr><td colspan="3">⋯(後面省略)</td></tr>' : "") + "</tbody></table></div>";
      }
      h += r.inf ? '<div class="ev-res bad">這個迴圈<b>停不下來</b>:i 一直離終點越來越遠,條件永遠成立。(超過 300 圈,這裡強制停止。)</div>'
        : r.count === 0 ? '<div class="ev-res bad">一圈都沒有執行:第一次檢查條件就不成立,sum 維持 0。</div>'
        : '<div class="ev-res">共執行 <b>' + r.count + "</b> 圈,結束時 <code>sum = " + r.sum + "</code>,最後 <code>i = " + r.last + "</code>(它讓條件不成立,所以迴圈停了)。</div>";
      out.innerHTML = h;
    }
    el.addEventListener("input", render);
    el.addEventListener("click", function (ev) {
      var b = ev.target.closest("button"); if (!b) return;
      if (b.dataset.p !== undefined) { var p = P[+b.dataset.p]; $S.value = p[1]; $O.value = p[2]; $E.value = p[3]; $T.value = p[4]; }
      else if (b.dataset.a === "reset") { var q = P[0]; $S.value = q[1]; $O.value = q[2]; $E.value = q[3]; $T.value = q[4]; }
      render();
    });
    render();
  });

  /* ---------- Memory 引擎(array):一排有索引的格子,讀、寫,以及越界 ---------- */
  var MM = CFG.memory || {};
  Array.prototype.forEach.call(document.querySelectorAll("[data-mem]"), function (el) {
    var f = MM[el.dataset.mem]; if (!f) return;
    var vals = f.values.slice(), n = vals.length, ghost = f.ghost || 2, hl = -1, msg = "";
    var nm = f.name;
    el.classList.add("calc");
    el.innerHTML = '<div class="mem-row" role="group" aria-label="' + esc(nm) + ' 的格子"></div>' +
      '<div class="calc-row" style="margin-top:12px"><div><label for="mI' + el.dataset.mem + '">索引 i</label><input id="mI' + el.dataset.mem + '" type="number" step="1" value="2" style="width:84px"></div>' +
      '<div><label for="mV' + el.dataset.mem + '">要寫入的' + (f.chars ? "字元" : "值") + '</label><input id="mV' + el.dataset.mem + '" ' + (f.chars ? 'type="text" maxlength="1" value="X"' : 'type="number" step="1" value="99"') + ' style="width:96px"></div>' +
      '<button type="button" class="primary" data-a="read">讀取 ' + esc(nm) + '[i]</button><button type="button" class="primary" data-a="write">寫入 ' + esc(nm) + '[i] = 值</button><button type="button" class="ghost" data-a="reset">Reset</button></div>' +
      '<div class="calc-out mem-out" aria-live="polite"></div>';
    var row = el.querySelector(".mem-row"), out = el.querySelector(".mem-out"), $i = el.querySelector("input"), $v = el.querySelectorAll("input")[1];
    function draw() {
      var h = "";
      for (var k = 0; k < n + ghost; k++) {
        var g = k >= n;
        h += '<div class="mem-cell' + (g ? " ghost" : "") + (k === hl ? " hl" : "") + '"><div class="mem-v">' + (g ? "?" : vals[k]) + '</div><div class="mem-i">' + (g ? "[" + k + "] 界外" : "[" + k + "]") + "</div></div>";
      }
      row.innerHTML = h; out.innerHTML = msg || "輸入索引,按「讀取」或「寫入」。試試索引 " + n + " 或 −1。";
    }
    function idx() { var s = $i.value.trim(); return /^-?\d+$/.test(s) ? parseInt(s, 10) : null; }
    el.addEventListener("click", function (ev) {
      var b = ev.target.closest("button"); if (!b) return; var i = idx(), a = b.dataset.a;
      if (a === "reset") { vals = f.values.slice(); hl = -1; msg = ""; $i.value = 2; $v.value = f.chars ? "X" : 99; draw(); return; }
      if (i === null) { msg = "請輸入整數索引。"; hl = -1; draw(); return; }
      var inr = i >= 0 && i < n;
      if (a === "read") {
        hl = inr ? i : (i >= n && i < n + ghost ? i : -1);
        msg = inr ? "<code>" + esc(nm) + "[" + i + "]</code> 的值是 <b>" + (f.chars ? "'" + esc(vals[i]) + "'" : vals[i]) + "</b>" + (f.chars && vals[i] === "\\0" ? "(結束記號,字串到這裡結束)" : "") + "。" :
          '<b class="bad">越界!</b><code>' + esc(nm) + "[" + i + "]</code> 在陣列範圍(0 到 " + (n - 1) + ")之外。C++ 不會替你檢查:它會去讀那個位置上剛好有的任何資料,結果沒有保證(未定義行為)。";
      } else {
        var v = f.chars ? $v.value : parseInt($v.value, 10); if (f.chars ? v.length !== 1 : isNaN(v)) { msg = f.chars ? "請輸入剛好一個字元。" : "請輸入要寫入的整數。"; draw(); return; }
        if (inr) { vals[i] = f.chars ? v : v; hl = i; msg = "已執行 <code>" + esc(nm) + "[" + i + "] = " + (f.chars ? "'" + esc(v) + "'" : v) + ";</code>。"; }
        else { hl = -1; msg = '<b class="bad">危險!</b>寫入 <code>' + esc(nm) + "[" + i + "]</code> 會改到陣列以外、不屬於它的記憶體,可能默默弄壞別的變數,也可能讓程式當掉。這裡不會真的寫入。"; }
      }
      draw();
    });
    draw();
  });

  /* ---------- BeforeAfter 引擎(vector):每個操作前後的內容對照 ---------- */
  var BA = CFG.beforeafter || {};
  Array.prototype.forEach.call(document.querySelectorAll("[data-ba]"), function (el) {
    var f = BA[el.dataset.ba]; if (!f || (f.kind && f.kind !== "vector")) return;
    var cur = f.init.slice(), hist = [], nm = f.name, id = el.dataset.ba;
    el.classList.add("calc");
    el.innerHTML = '<div class="calc-row"><div><label for="bV' + id + '">值 x</label><input id="bV' + id + '" type="number" step="1" value="10" style="width:84px"></div>' +
      '<div><label for="bI' + id + '">索引 i</label><input id="bI' + id + '" type="number" step="1" value="0" style="width:84px"></div></div>' +
      '<div class="calc-pre"><button type="button" class="primary" data-op="push">' + esc(nm) + '.push_back(x)</button><button type="button" class="primary" data-op="pop">' + esc(nm) + '.pop_back()</button>' +
      '<button type="button" class="primary" data-op="set">' + esc(nm) + '[i] = x</button><button type="button" class="primary" data-op="clear">' + esc(nm) + '.clear()</button><button type="button" class="ghost" data-op="reset">Reset</button></div>' +
      '<div class="ba-now"></div><div class="ba-hist" aria-live="polite"></div>';
    var $x = el.querySelector("#bV" + id), $i = el.querySelector("#bI" + id), now = el.querySelector(".ba-now"), hist$ = el.querySelector(".ba-hist");
    function cells(a, cls) { return '<span class="ba-cells ' + (cls || "") + '">' + (a.length ? a.map(function (x) { return "<i>" + x + "</i>"; }).join("") : "<em>(空)</em>") + "</span>"; }
    function draw() {
      now.innerHTML = "<code>" + esc(nm) + "</code> 現在:" + cells(cur) + ' <span class="ba-size"><code>' + esc(nm) + ".size()</code> = <b>" + cur.length + "</b></span>";
      hist$.innerHTML = hist.slice(-6).reverse().map(function (h) {
        return '<div class="ba-row"><code>' + esc(h.code) + "</code><div>" + cells(h.before, "old") + " → " + cells(h.after) + "</div>" + (h.note ? "<small>" + esc(h.note) + "</small>" : "") + "</div>";
      }).join("");
    }
    el.addEventListener("click", function (ev) {
      var b = ev.target.closest("[data-op]"); if (!b) return;
      var op = b.dataset.op, x = parseInt($x.value, 10), i = parseInt($i.value, 10), before = cur.slice(), code, note = "";
      if (op === "reset") { cur = f.init.slice(); hist = []; draw(); return; }
      if (op === "push") { if (isNaN(x)) return; cur.push(x); code = nm + ".push_back(" + x + ");"; note = "加到最後面,長度加 1。"; }
      else if (op === "pop") { code = nm + ".pop_back();"; if (!cur.length) { note = "已經是空的了:對空的 vector 呼叫 pop_back 是未定義行為,這裡不會執行。"; hist.push({ code: code, before: before, after: cur.slice(), note: note }); draw(); return; } cur.pop(); note = "移除最後一個,長度減 1。"; }
      else if (op === "set") { if (isNaN(x) || isNaN(i)) return; code = nm + "[" + i + "] = " + x + ";"; if (i < 0 || i >= cur.length) { note = "索引 " + i + " 超出範圍(0 到 " + (cur.length - 1) + "):這是越界,這裡不會執行。"; hist.push({ code: code, before: before, after: cur.slice(), note: note }); draw(); return; } cur[i] = x; note = "只改那一格,長度不變。"; }
      else if (op === "clear") { cur = []; code = nm + ".clear();"; note = "全部移除,長度變 0。"; }
      hist.push({ code: code, before: before, after: cur.slice(), note: note }); draw();
    });
    draw();
  });

  /* ---------- BeforeAfter 引擎(set / map):自動排序、不重複、[] 會順手新增 ---------- */
  Array.prototype.forEach.call(document.querySelectorAll("[data-ba]"), function (el) {
    var f = BA[el.dataset.ba]; if (!f || (f.kind !== "set" && f.kind !== "map")) return;
    var isMap = f.kind === "map", nm = f.name, id = el.dataset.ba, hist = [];
    var cur = isMap ? JSON.parse(JSON.stringify(f.init)) : f.init.slice();
    function sorted(c) { return isMap ? Object.keys(c).sort().map(function (k) { return k + ": " + c[k]; }) : c.slice().sort(function (a, b) { return a - b; }); }
    el.classList.add("calc");
    el.innerHTML = (isMap
      ? '<div class="calc-row"><div><label for="bK' + id + '">鍵 key</label><input id="bK' + id + '" value="kiwi" style="width:120px" autocomplete="off"></div><div><label for="bV' + id + '">值 value</label><input id="bV' + id + '" type="number" value="4" style="width:84px"></div></div>' +
        '<div class="calc-pre"><button type="button" class="primary" data-op="put">' + esc(nm) + '[key] = value</button><button type="button" class="primary" data-op="read">' + esc(nm) + '[key](讀取)</button><button type="button" class="primary" data-op="erase">' + esc(nm) + '.erase(key)</button><button type="button" class="primary" data-op="count">' + esc(nm) + '.count(key)</button><button type="button" class="ghost" data-op="reset">Reset</button></div>'
      : '<div class="calc-row"><div><label for="bV' + id + '">值 x</label><input id="bV' + id + '" type="number" value="2" style="width:84px"></div></div>' +
        '<div class="calc-pre"><button type="button" class="primary" data-op="insert">' + esc(nm) + '.insert(x)</button><button type="button" class="primary" data-op="erase">' + esc(nm) + '.erase(x)</button><button type="button" class="primary" data-op="count">' + esc(nm) + '.count(x)</button><button type="button" class="ghost" data-op="reset">Reset</button></div>') +
      '<div class="ba-now"></div><div class="ba-hist" aria-live="polite"></div>';
    var $k = el.querySelector("#bK" + id), $v = el.querySelector("#bV" + id), now = el.querySelector(".ba-now"), hist$ = el.querySelector(".ba-hist");
    function cells(a, cls) { return '<span class="ba-cells ' + (cls || "") + '">' + (a.length ? a.map(function (x) { return "<i>" + esc(x) + "</i>"; }).join("") : "<em>(空)</em>") + "</span>"; }
    function size() { return isMap ? Object.keys(cur).length : cur.length; }
    function draw() {
      now.innerHTML = "<code>" + esc(nm) + "</code> 現在(自動由小到大排好):" + cells(sorted(cur)) + ' <span class="ba-size"><code>' + esc(nm) + ".size()</code> = <b>" + size() + "</b></span>";
      hist$.innerHTML = hist.slice(-6).reverse().map(function (h) {
        return '<div class="ba-row"><code>' + esc(h.code) + "</code><div>" + cells(h.before, "old") + " → " + cells(h.after) + "</div><small>" + esc(h.note) + "</small></div>";
      }).join("");
    }
    el.addEventListener("click", function (ev) {
      var b = ev.target.closest("[data-op]"); if (!b) return; var op = b.dataset.op;
      if (op === "reset") { cur = isMap ? JSON.parse(JSON.stringify(f.init)) : f.init.slice(); hist = []; draw(); return; }
      var before = sorted(cur), code, note, v = parseInt($v.value, 10), key = isMap ? $k.value.trim() : null;
      if (isMap) { if (!key || /\s/.test(key)) { now.insertAdjacentHTML("beforeend", ""); return; } if (isNaN(v) && op === "put") return; }
      else if (isNaN(v)) return;
      if (!isMap) {
        var has = cur.indexOf(v) >= 0;
        if (op === "insert") { code = nm + ".insert(" + v + ");"; if (has) note = v + " 已經在裡面了:set 不會重複,所以什麼都沒變。"; else { cur.push(v); note = "加入 " + v + ",並自動排在正確的位置。"; } }
        else if (op === "erase") { code = nm + ".erase(" + v + ");"; if (has) { cur.splice(cur.indexOf(v), 1); note = "移除了 " + v + "。"; } else note = "裡面沒有 " + v + ",沒有任何改變(不會出錯)。"; }
        else { code = nm + ".count(" + v + ");"; note = "回傳 " + (has ? 1 : 0) + "(" + (has ? "有" : "沒有") + "),只是查詢,內容不變。"; }
      } else {
        var k = JSON.stringify(key), has2 = Object.prototype.hasOwnProperty.call(cur, key);
        if (op === "put") { code = nm + "[" + k + "] = " + v + ";"; note = has2 ? "鍵已存在,把值更新成 " + v + "。" : "鍵不存在,新增一筆。"; cur[key] = v; }
        else if (op === "read") { code = "cout << " + nm + "[" + k + "];"; if (has2) note = "印出 " + cur[key] + "。"; else { cur[key] = 0; note = "印出 0。陷阱:鍵不存在,[] 讀取時會「順手新增」這個鍵(值為 0),所以 map 變大了!"; } }
        else if (op === "erase") { code = nm + ".erase(" + k + ");"; if (has2) { delete cur[key]; note = "移除了這一筆。"; } else note = "沒有這個鍵,沒有任何改變。"; }
        else { code = nm + ".count(" + k + ");"; note = "回傳 " + (has2 ? 1 : 0) + ",只是查詢,不會改動 map。"; }
      }
      hist.push({ code: code, before: before, after: sorted(cur), note: note }); draw();
    });
    draw();
  });

  /* ---------- Diagram 引擎:類別方塊圖、存取權限測試、繼承箭頭 ---------- */
  var DG = CFG.diagram || {};
  Array.prototype.forEach.call(document.querySelectorAll("[data-diagram]"), function (el) {
    var f = DG[el.dataset.diagram]; if (!f) return;
    var on = f.toggle ? !!f.toggle.on : true, VIS = { pub: "+", pri: "-", pro: "#" };
    function mem(b, m, kind) {
      var id = b.id + "." + m.n;
      return '<button type="button" class="dg-m ' + m.v + '" data-m="' + esc(id) + '" data-note="' + esc(m.note || "") + '"><span class="dg-v">' + VIS[m.v] + "</span> " + esc(kind === "f" ? m.t + " " + m.n : m.t + " " + m.n) + "</button>";
    }
    el.classList.add("dg");
    el.innerHTML = '<div class="dg-canvas"><svg class="dg-svg" aria-hidden="true"></svg><div class="dg-rows">' +
      f.rows.map(function (row) {
        return '<div class="dg-row">' + row.map(function (bid) {
          var b = f.boxes[bid]; b.id = bid;
          return '<div class="dg-box" data-b="' + esc(bid) + '"><div class="dg-name">' + esc(b.name) + (b.sub ? "<small>" + esc(b.sub) + "</small>" : "") + "</div>" +
            '<div class="dg-sec">' + (b.fields || []).map(function (m) { return mem(b, m, "f"); }).join("") + "</div>" +
            '<div class="dg-sec">' + (b.methods || []).map(function (m) { return mem(b, m, "m"); }).join("") + "</div></div>";
        }).join("") + "</div>";
      }).join("") + "</div></div>" +
      '<div class="dg-legend"><span><b>+</b> public(外面能用)</span><span><b>−</b> private(只有類別自己能用)</span>' + (f.boxes && JSON.stringify(f.boxes).indexOf('"pro"') > 0 ? "<span><b>#</b> protected(自己與子類別)</span>" : "") + "</div>" +
      '<div class="dg-note" aria-live="polite">點方塊裡的成員,看它的說明。</div>' +
      (f.toggle ? '<label class="calc-chk" style="margin:12px 0 0 !important"><input type="checkbox" data-tog ' + (on ? "checked" : "") + ">" + esc(f.toggle.label) + "</label>" : "") +
      (f.tests ? '<div class="dg-tests-h">' + esc(f.testsTitle || "試試看:執行這些程式碼") + '</div><div class="calc-pre">' + f.tests.map(function (t, k) { return '<button type="button" class="ghost" data-t="' + k + '"><code>' + esc(t.code) + "</code></button>"; }).join("") + '</div><div class="dg-res" aria-live="polite"></div>' : "");
    var canvas = el.querySelector(".dg-canvas"), svg = el.querySelector(".dg-svg"), note = el.querySelector(".dg-note"), res = el.querySelector(".dg-res");
    function arrows() {
      var c = canvas.getBoundingClientRect(), p = "";
      svg.setAttribute("width", c.width); svg.setAttribute("height", c.height);
      (f.arrows || []).forEach(function (a) {
        var from = el.querySelector('[data-b="' + a.from + '"]'), to = el.querySelector('[data-b="' + a.to + '"]'); if (!from || !to) return;
        var r1 = from.getBoundingClientRect(), r2 = to.getBoundingClientRect(), x1 = r1.left + r1.width / 2 - c.left, y1 = r1.top - c.top, x2 = r2.left + r2.width / 2 - c.left, y2 = r2.bottom - c.top;
        p += '<path d="M' + x1 + " " + y1 + " L" + x2 + " " + (y2 + 12) + '" stroke="#3D3D3A" stroke-width="1.6" fill="none"/>' +
          '<path d="M' + x2 + " " + y2 + " L" + (x2 - 7) + " " + (y2 + 12) + " L" + (x2 + 7) + " " + (y2 + 12) + ' Z" fill="#fff" stroke="#3D3D3A" stroke-width="1.6"/>';
      });
      svg.innerHTML = p;
    }
    function pick(t) { return t.on !== undefined || t.off !== undefined ? (on ? t.on : t.off) : t; }
    el.addEventListener("click", function (ev) {
      var m = ev.target.closest(".dg-m"), t = ev.target.closest("[data-t]");
      if (m) {
        Array.prototype.forEach.call(el.querySelectorAll(".dg-m"), function (x) { x.classList.toggle("sel", x === m); });
        note.textContent = m.dataset.note || "(沒有額外說明)";
      }
      if (t) {
        var d = pick(f.tests[+t.dataset.t]);
        Array.prototype.forEach.call(el.querySelectorAll(".dg-m"), function (x) { x.classList.toggle("hit", x.dataset.m === d.hl); x.classList.toggle("badhit", x.dataset.m === d.hl && !d.ok); });
        res.className = "dg-res " + (d.ok ? "ok" : "bad");
        res.innerHTML = (d.ok ? "✓ " : "✗ ") + d.msg;
      }
    });
    var tg = el.querySelector("[data-tog]");
    if (tg) tg.addEventListener("change", function () { on = tg.checked; res.className = "dg-res"; res.textContent = "已切換,請重新按一次上面的程式碼。"; });
    window.addEventListener("resize", arrows); arrows(); setTimeout(arrows, 60);
  });
})();
