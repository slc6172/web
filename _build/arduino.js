/* Arduino 主題專用互動:接線步驟播放、原理圖與麵包板連動。只有 dir=arduino 的頁面會內嵌。 */
(function () {
  "use strict";
  var CFG = window.PAGE || {};

  /* ---------- 表格:手機版直式堆疊時,每格補上欄名 ---------- */
  Array.prototype.forEach.call(document.querySelectorAll(".gt"), function (t) {
    var rows = t.querySelectorAll(".row");
    if (rows.length < 2) return;
    var heads = Array.prototype.map.call(rows[0].children, function (c) { return c.textContent; });
    for (var i = 1; i < rows.length; i++)
      Array.prototype.forEach.call(rows[i].children, function (c, k) { if (k > 0 && heads[k]) c.setAttribute("data-h", heads[k]); });
  });

  /* ---------- 接線步驟播放 ---------- */
  var WIRES = CFG.wiring || [];
  Array.prototype.forEach.call(document.querySelectorAll("[data-wiring]"), function (box) {
    var id = box.getAttribute("data-wiring"), conf = null;
    WIRES.forEach(function (w) { if (w.id === id) conf = w; });
    if (!conf) return;
    var n = conf.steps.length, cur = 0;                 // cur: 0=還沒開始, 1..n=第幾步, n+1=全部完成
    var els = Array.prototype.slice.call(box.querySelectorAll(".el"));
    var cap = box.querySelector(".wcap");
    var dots = Array.prototype.slice.call(box.querySelectorAll(".wdot"));
    var bPrev = box.querySelector('[data-w="prev"]'), bNext = box.querySelector('[data-w="next"]');
    function render() {
      els.forEach(function (el) {
        var s = +el.getAttribute("data-step");
        el.classList.toggle("future", cur <= n && s > cur);
        el.classList.toggle("cur", s === cur);
      });
      dots.forEach(function (d) {
        var i = +d.getAttribute("data-w");
        d.classList.toggle("on", i === cur);
        d.classList.toggle("done", i < cur);
        d.setAttribute("aria-pressed", i === cur ? "true" : "false");
      });
      if (cur === 0) cap.innerHTML = '<b class="t">開始前</b>' + (conf.intro || "");
      else if (cur <= n) cap.innerHTML = '<b class="t">第 ' + cur + " 步:" + conf.steps[cur - 1].t + "</b>" + conf.steps[cur - 1].x;
      else cap.innerHTML = '<b class="t">完整接線</b>' + (conf.done || "");
      bPrev.disabled = cur === 0;
      bNext.disabled = cur > n;
    }
    box.addEventListener("click", function (e) {
      var b = e.target.closest("[data-w]");
      if (!b) return;
      var k = b.getAttribute("data-w");
      if (k === "prev") { if (cur > 0) cur = cur > n ? n : cur - 1; }
      else if (k === "next") { if (cur <= n) cur++; }
      else if (k === "all") cur = n + 1;
      else if (k === "reset") cur = 0;
      else cur = +k;
      render();
    });
    box.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight" && cur <= n) { cur++; render(); e.preventDefault(); }
      else if (e.key === "ArrowLeft" && cur > 0) { cur = cur > n ? n : cur - 1; render(); e.preventDefault(); }
    });
    render();
  });


  /* ---------- 麵包板內部連線探索圖 ---------- */
  Array.prototype.forEach.call(document.querySelectorAll("[data-bbx]"), function (box) {
    var cells = Array.prototype.slice.call(box.querySelectorAll(".bh"));
    var info = box.querySelector(".bbx-info"), split = box.querySelector(".bbx-split");
    var sel = null, DEF = info.innerHTML;
    function net(c) { return c.getAttribute(split && split.checked ? "data-net2" : "data-net"); }
    function paint() {
      if (!sel) { cells.forEach(function (c) { c.classList.remove("on", "sel"); }); info.innerHTML = DEF; return; }
      var k = net(sel), mates = [];
      cells.forEach(function (c) {
        var on = net(c) === k;
        c.classList.toggle("on", on); c.classList.toggle("sel", c === sel);
        if (on && c !== sel) mates.push(c.getAttribute("data-h"));
      });
      var h = sel.getAttribute("data-h"), txt;
      if (/^[tb]/.test(h)) {
        txt = "你點的是 <code>" + h + "</code>,它屬於電源軌。<b>同一條軌上共 " + (mates.length + 1) + " 個孔彼此相通</b>" +
              (split && split.checked ? "(這片麵包板的電源軌在中間斷開,左半與右半不相通)。" : "。") + "把 5V 接到 + 軌、GND 接到 − 軌,之後整排孔都能取用。";
      } else {
        txt = "你點的是 <code>" + h + "</code>,它和 <code>" + mates.join("、") + "</code> 在內部相通(同一欄的 " + (/[a-e]/.test(h[0]) ? "a–e" : "f–j") + ")。" +
              "把兩個零件的腳插在這 " + (mates.length + 1) + " 個孔裡,它們就接在一起了。";
      }
      info.innerHTML = txt;
    }
    box.addEventListener("click", function (e) {
      var c = e.target.closest(".bh");
      if (!c) return;
      sel = sel === c ? null : c; paint();
    });
    if (split) split.addEventListener("change", paint);
  });

  /* ---------- 電阻色環計算機 ---------- */
  var COL = [["黑", "#141413"], ["棕", "#8B5A3C"], ["紅", "#B04A3F"], ["橙", "#D97757"], ["黃", "#E1B93B"], ["綠", "#788C5D"], ["藍", "#5B7FA6"], ["紫", "#7A5C8F"], ["灰", "#87867F"], ["白", "#FFFFFF"]];
  var MUL = [[0, "黑 ×1", "#141413"], [1, "棕 ×10", "#8B5A3C"], [2, "紅 ×100", "#B04A3F"], [3, "橙 ×1k", "#D97757"], [4, "黃 ×10k", "#E1B93B"], [5, "綠 ×100k", "#788C5D"], [6, "藍 ×1M", "#5B7FA6"], [-1, "金 ×0.1", "#C9A227"], [-2, "銀 ×0.01", "#BFBFBF"]];
  function fmtOhm(v) {
    if (v >= 1e6) return +(v / 1e6).toFixed(2) + " MΩ";
    if (v >= 1e3) return +(v / 1e3).toFixed(2) + " kΩ";
    return +v.toFixed(2) + " Ω";
  }
  function parseOhm(s) {
    var m = /^\s*(\d+(?:\.\d+)?)\s*([kKmM]?)\s*[ΩΩohmOHM]*\s*$/.exec(s || "");
    if (!m) return NaN;
    var v = parseFloat(m[1]), u = m[2];
    return u === "k" || u === "K" ? v * 1e3 : (u === "M" || u === "m" ? v * 1e6 : v);
  }
  Array.prototype.forEach.call(document.querySelectorAll("[data-rcalc]"), function (box) {
    var s1 = box.querySelector('[data-rc="b1"]'), s2 = box.querySelector('[data-rc="b2"]'), s3 = box.querySelector('[data-rc="b3"]');
    var inp = box.querySelector('[data-rc="val"]'), out = box.querySelector(".rc-out");
    var r1 = box.querySelector(".rc1"), r2 = box.querySelector(".rc2"), r3 = box.querySelector(".rc3");
    COL.forEach(function (c, i) { if (i > 0) s1.add(new Option(c[0] + " " + i, i)); });
    COL.forEach(function (c, i) { s2.add(new Option(c[0] + " " + i, i)); });
    MUL.forEach(function (m) { s3.add(new Option(m[1], m[0])); });
    function mulColor(e) { for (var i = 0; i < MUL.length; i++) if (MUL[i][0] === e) return MUL[i][2]; return "#141413"; }
    function showBands() {
      r1.setAttribute("fill", COL[+s1.value][1]); r2.setAttribute("fill", COL[+s2.value][1]); r3.setAttribute("fill", mulColor(+s3.value));
    }
    function fromSelects() {
      var v = (+s1.value * 10 + +s2.value) * Math.pow(10, +s3.value);
      inp.value = fmtOhm(v).replace(" ", "").replace("Ω", "");
      var mc = MUL.filter(function (m) { return m[0] === +s3.value; })[0][1].split(" ")[0];
      out.innerHTML = "<b>" + COL[+s1.value][0] + "、" + COL[+s2.value][0] + "、" + mc + "、金</b> = " + (+s1.value * 10 + +s2.value) + " × " + (+s3.value >= 0 ? Math.pow(10, +s3.value) : Math.pow(10, +s3.value)) + " = <b>" + fmtOhm(v) + "</b>(誤差 ±5%)";
      showBands();
    }
    function fromInput() {
      var v = parseOhm(inp.value);
      if (!(v >= 1)) { out.innerHTML = "請輸入數字,例如 <code>220</code>、<code>4.7k</code>、<code>10k</code>。"; return; }
      var e = Math.floor(Math.log10(v)) - 1, m = Math.round(v / Math.pow(10, e));
      if (m === 100) { m = 10; e += 1; }
      if (e < -2 || e > 6 || m < 10) { out.innerHTML = "這個值超出 4 環電阻的範圍。"; return; }
      if (e < 0) { e = e; }
      s1.value = Math.floor(m / 10); s2.value = m % 10; s3.value = e;
      var exact = Math.abs(m * Math.pow(10, e) - v) < 1e-9;
      fromSelects();
      if (!exact) out.innerHTML += "<br>(你輸入的值不能用 4 環精確表示,已顯示最接近的 " + fmtOhm(m * Math.pow(10, e)) + ")";
    }
    [s1, s2, s3].forEach(function (s) { s.addEventListener("change", fromSelects); });
    inp.addEventListener("input", fromInput);
    s1.value = 2; s2.value = 2; s3.value = 1; fromSelects();
  });

  /* ---------- LED 限流電阻計算機 ---------- */
  var E12 = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82];
  function nextE12(r) {
    var d = Math.pow(10, Math.floor(Math.log10(r)) - 1);
    for (var k = 0; k < 4; k++) for (var i = 0; i < E12.length; i++) { var v = E12[i] * d * Math.pow(10, k); if (v >= r - 1e-9) return v; }
    return r;
  }
  Array.prototype.forEach.call(document.querySelectorAll("[data-ledcalc]"), function (box) {
    var vf = box.querySelector('[data-lc="vf"]'), ma = box.querySelector('[data-lc="ma"]'), out = box.querySelector(".lc-out");
    function calc() {
      var v = parseFloat(vf.value), i = parseFloat(ma.value);
      if (!(i > 0)) { out.innerHTML = "請輸入大於 0 的電流(毫安)。"; return; }
      var r = (5 - v) / (i / 1000), std = nextE12(r), real = (5 - v) / std * 1000;
      var msg = "電阻上要承擔的電壓 = 5 − " + v + " = <b>" + (5 - v).toFixed(1) + " V</b><br>" +
                "理論電阻 R = " + (5 - v).toFixed(1) + " ÷ " + (i / 1000) + " A = <b>" + Math.round(r) + " Ω</b><br>" +
                "取不小於它的標準值 → <b>" + fmtOhm(std) + "</b>,實際電流約 <b>" + real.toFixed(1) + " mA</b>";
      if (real > 20) msg += "<br><span class=\"calc-bad\">超過 Uno 每腳建議上限 20 mA,請選更大的電阻或降低目標電流。</span>";
      else if (real < 1) msg += "<br>電流太小,LED 可能幾乎看不出來在亮。";
      out.innerHTML = msg;
    }
    vf.addEventListener("change", calc); ma.addEventListener("input", calc); calc();
  });


  /* ---------- PWM 示意 ---------- */
  Array.prototype.forEach.call(document.querySelectorAll("[data-pwmbox]"), function (box) {
    var rng = box.querySelector('[data-pwm="v"]'), num = box.querySelector('[data-pwm="num"]');
    var wave = box.querySelector(".pwm-wave"), out = box.querySelector(".pwm-out"), led = box.querySelector(".pwm-led");
    var pin = box.getAttribute("data-pin") || "9";
    function draw(v) {
      var d = v / 255, P = 110, x0 = 50, pts = [], i;
      for (i = 0; i < 4; i++) {
        var x = x0 + i * P, hi = d * P;
        if (d <= 0) { pts.push(x + "," + 120, (x + P) + "," + 120); }
        else if (d >= 1) { pts.push(x + "," + 30, (x + P) + "," + 30); }
        else { pts.push(x + "," + 120, x + "," + 30, (x + hi) + "," + 30, (x + hi) + "," + 120, (x + P) + "," + 120); }
      }
      wave.setAttribute("points", pts.join(" "));
      led.style.background = "rgba(176,74,63," + (0.08 + 0.92 * d).toFixed(2) + ")";
      out.innerHTML = "<code>analogWrite(" + pin + ", " + v + ");</code> → 一個週期裡有 <b>" + Math.round(d * 100) + "%</b> 的時間是 5 V,其餘是 0 V → 平均電壓約 <b>" + (5 * d).toFixed(2) + " V</b>。" +
        (v === 0 ? "(0 等於一直輸出 LOW,LED 全滅。)" : (v === 255 ? "(255 等於一直輸出 HIGH,LED 全亮。)" : "LED 因為閃得太快,看起來是「半亮」。"));
    }
    function set(v) { v = Math.max(0, Math.min(255, Math.round(+v || 0))); rng.value = v; num.value = v; draw(v); }
    rng.addEventListener("input", function () { set(rng.value); });
    num.addEventListener("input", function () { if (num.value !== "") set(num.value); });
    set(rng.value);
  });


  /* ---------- 按鈕與上拉電阻示意 ---------- */
  Array.prototype.forEach.call(document.querySelectorAll("[data-btnsim]"), function (box) {
    var mode = box.querySelector('[data-bs="mode"]'), btn = box.querySelector('[data-bs="btn"]');
    var open = box.querySelector(".sw-open"), closed = box.querySelector(".sw-closed"), pu = box.querySelector(".pu");
    var lvl = box.querySelector(".bs-level"), out = box.querySelector(".bs-out"), node = box.querySelector(".bs-node");
    var pressed = false;
    function render() {
      var pull = mode.value === "pullup", read, txt, col;
      open.style.display = pressed ? "none" : "block";
      closed.style.display = pressed ? "block" : "none";
      pu.style.opacity = pull ? "1" : "0.18";
      btn.textContent = pressed ? "目前:按住中(點一下放開)" : "目前:放開(點一下按住)";
      btn.setAttribute("aria-pressed", pressed ? "true" : "false");
      if (pull && !pressed) { read = "HIGH(1)"; col = "#788C5D"; txt = "<b>沒按</b>:5 V 經過內建上拉電阻到達 2 號腳。D2 沒有別的去處,幾乎沒有電流,電壓留在約 5 V → <code>digitalRead(2)</code> = <b>HIGH(1)</b>。"; }
      else if (pull && pressed) { read = "LOW(0)"; col = "#B04A3F"; txt = "<b>按下</b>:按鈕把 2 號腳接到 GND。上拉電阻只讓一點點電流通過(5 V ÷ 約 20–50 kΩ,約 0.1–0.25 mA),2 號腳電壓被拉到約 0 V → <code>digitalRead(2)</code> = <b>LOW(0)</b>。"; }
      else if (!pull && !pressed) { read = "不確定"; col = "#87867F"; txt = "<b>沒按</b>:2 號腳什麼都沒接,像一根天線,會收到周圍的雜訊,讀到的值<b>在 HIGH 與 LOW 之間亂跳</b>。這叫<b>浮接</b>,是新手最常踩的坑。"; }
      else { read = "LOW(0)"; col = "#B04A3F"; txt = "<b>按下</b>:2 號腳接到 GND → LOW。但<b>放開的瞬間又回到浮接</b>,讀值不穩,所以這樣的接法不能用。"; }
      lvl.textContent = "digitalRead(2) → " + read;
      lvl.setAttribute("fill", col);
      node.setAttribute("fill", col);
      out.innerHTML = txt;
    }
    btn.addEventListener("click", function () { pressed = !pressed; render(); });
    mode.addEventListener("change", render);
    render();
  });


  /* ---------- 鮑率不一致 → 亂碼 示意 ---------- */
  Array.prototype.forEach.call(document.querySelectorAll("[data-baudsim]"), function (box) {
    var sel = box.querySelector('[data-bd="monitor"]'), scr = box.querySelector(".bd-screen"), note = box.querySelector(".bd-note");
    var prog = box.getAttribute("data-prog") || "9600";
    var GARBLE = { lower: "\u00ff\u00ff\u00e0\u00e0 \u00fe\u00fe\ufffd\ufffd\ufffd\ufffd\n\u00ff\u00fc\ufffd\ufffd\u00ff\u00ff \u00e0\ufffd\ufffd", higher: "\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\n\ufffd\ufffd\ufffd \ufffd\ufffd\ufffd\ufffd\ufffd\ufffd" };
    function render() {
      var m = +sel.value, p = +prog;
      if (m === p) { scr.textContent = "Hello, Arduino!\ncount = 0\ncount = 1\ncount = 2"; scr.style.color = "#3D3D3A"; note.innerHTML = "<b>兩邊都是 " + p + "。</b>文字正常顯示。"; }
      else { scr.textContent = m < p ? GARBLE.lower : GARBLE.higher; scr.style.color = "#B04A3F"; note.innerHTML = "程式用 <code>Serial.begin(" + p + ")</code>,Serial Monitor 卻選 <b>" + m + "</b>:雙方講話速度不同,對方聽到的是亂碼。<b>把 Serial Monitor 右上角的 baud 選成和程式一樣。</b>"; }
    }
    sel.addEventListener("change", render); render();
  });


  /* ---------- 電位器分壓示意 ---------- */
  Array.prototype.forEach.call(document.querySelectorAll("[data-potsim]"), function (box) {
    var rng = box.querySelector('[data-pot="v"]'), out = box.querySelector(".pot-out"), bar = box.querySelector(".pot-bar span"), led = box.querySelector(".pwm-led");
    function render() {
      var pos = +rng.value, x = pos / 100;
      var rt = 10 * (1 - x), rb = 10 * x, v = 5 * x, adc = Math.round(x * 1023), mapped = Math.floor(adc * 255 / 1023);
      bar.style.width = pos + "%";
      led.style.background = "rgba(176,74,63," + (0.08 + 0.92 * mapped / 255).toFixed(2) + ")";
      out.innerHTML = "旋鈕轉到 <b>" + pos + "%</b>:<br>" +
        "上段電阻(5V 到中間腳)= <b>" + rt.toFixed(1) + " kΩ</b>,下段電阻(中間腳到 GND)= <b>" + rb.toFixed(1) + " kΩ</b>(加起來永遠是 10 kΩ)<br>" +
        "中間腳(接 A0)電壓 = 5 V × " + rb.toFixed(1) + " ÷ 10 = <b>" + v.toFixed(2) + " V</b><br>" +
        "<code>analogRead(A0)</code> ≈ <b>" + adc + "</b>(0–1023)<br>" +
        "<code>map(值, 0, 1023, 0, 255)</code> ≈ <b>" + mapped + "</b> → LED 亮度";
    }
    rng.addEventListener("input", render); render();
  });


  /* ---------- 光敏電阻分壓示意 ---------- */
  Array.prototype.forEach.call(document.querySelectorAll("[data-ldrsim]"), function (box) {
    var rng = box.querySelector('[data-ldr="v"]'), thr = box.querySelector('[data-ldr="thr"]'), out = box.querySelector(".ldr-out"), bar = box.querySelector(".pot-bar span"), led = box.querySelector(".pwm-led");
    function fmt(v) { return v >= 1e6 ? (v / 1e6).toFixed(2) + " MΩ" : (v >= 1e3 ? (v / 1e3).toFixed(1) + " kΩ" : Math.round(v) + " Ω"); }
    function render() {
      var x = +rng.value / 100, r = 1e6 * Math.pow(1e-3, x), v = 5 * 10000 / (r + 10000), adc = Math.round(v / 5 * 1023), t = parseInt(thr.value, 10);
      bar.style.width = (adc / 1023 * 100) + "%";
      var on = !isNaN(t) && adc < t;
      led.style.background = on ? "rgba(176,74,63,1)" : "rgba(176,74,63,.08)";
      out.innerHTML = "環境亮度 <b>" + Math.round(x * 100) + "%</b>:光敏電阻約 <b>" + fmt(r) + "</b>(範例值)<br>" +
        "A0 電壓 = 5 V × 10 kΩ ÷ (光敏電阻 + 10 kΩ) = <b>" + v.toFixed(2) + " V</b> → <code>analogRead(A0)</code> ≈ <b>" + adc + "</b><br>" +
        "門檻 " + (isNaN(t) ? "?" : t) + ":<b>" + (on ? "讀值低於門檻 → 天黑,LED 亮" : "讀值不低於門檻 → 夠亮,LED 滅") + "</b>";
    }
    rng.addEventListener("input", render); thr.addEventListener("input", render); render();
  });

  /* ---------- 原理圖 ↔ 麵包板 連動 ---------- */
  var PARTS = CFG.parts || {};
  var infos = Array.prototype.slice.call(document.querySelectorAll(".linkbox"));
  infos.forEach(function (b) { b._def = b.innerHTML; });
  var sel = "";
  function hl(ref) {
    sel = sel === ref ? "" : ref;
    Array.prototype.forEach.call(document.querySelectorAll("[data-part]"), function (el) {
      el.classList.toggle("hl", sel !== "" && el.getAttribute("data-part") === sel);
    });
    infos.forEach(function (b) { b.innerHTML = sel ? (PARTS[sel] || "") : b._def; });
  }
  document.addEventListener("click", function (e) {
    var el = e.target.closest("[data-part]");
    if (el) hl(el.getAttribute("data-part"));
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Enter" && e.key !== " ") return;
    var el = e.target.closest && e.target.closest("[data-part]");
    if (el) { e.preventDefault(); hl(el.getAttribute("data-part")); }
  });
})();
