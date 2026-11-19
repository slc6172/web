(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var CURVES = [
    { k: "c1", name: "O(1)", color: "#87867F", f: function () { return 1; } },
    { k: "log", name: "O(log n)", color: "#788C5D", f: function (n) { return Math.log2(n); } },
    { k: "n", name: "O(n)", color: "#3D3D3A", f: function (n) { return n; } },
    { k: "nlogn", name: "O(n log n)", color: "#D97757", f: function (n) { return n * Math.log2(n); } },
    { k: "n2", name: "O(n²)", color: "#B04A3F", f: function (n) { return n * n; } },
    { k: "exp", name: "O(2ⁿ)", color: "#141413", dash: "6 4", f: function (n) { return Math.pow(2, n); } }
  ];
  function counts(n) { var o = {}; CURVES.forEach(function (c) { o[c.k] = c.f(n); }); return o; }
  function fmtNum(x) {
    if (x < 1e6) return (Math.round(x * 10) / 10).toLocaleString("en-US");
    var e = Math.floor(Math.log10(x)), m = x / Math.pow(10, e);
    return (Math.round(m * 100) / 100) + "×10<sup>" + e + "</sup>";
  }
  /* 假設每次操作 1 微秒(僅為方便感受大小的示意假設,不是實測) */
  function fmtTime(us) {
    var YEAR = 3.156e13;
    if (us < 1000) return (us < 10 ? Math.round(us * 10) / 10 : Math.round(us)) + " 微秒";
    if (us < 1e6) return Math.round(us / 1000) + " 毫秒";
    if (us < 6e7) return Math.round(us / 1e6 * 10) / 10 + " 秒";
    if (us < 3.6e9) return Math.round(us / 6e7) + " 分鐘";
    if (us < 8.64e10) return Math.round(us / 3.6e9) + " 小時";
    if (us < YEAR) return Math.round(us / 8.64e10) + " 天";
    var y = us / YEAR;
    if (y > 1.38e10) return "超過宇宙年齡(約 138 億年)";
    return y < 1e6 ? Math.round(y).toLocaleString("en-US") + " 年" : fmtNum(y) + " 年";
  }
  function chart(N) {
    var W = 520, H = 250, L = 36, R = 12, T = 12, B = 28, pw = W - L - R, ph = H - T - B;
    N = Math.max(N, 2); var ymax = Math.max(N * 2, 10);
    var sx = function (n) { return L + (n - 1) / (N - 1) * pw; }, sy = function (y) { return T + ph - Math.min(y, ymax) / ymax * ph; };
    var s = '<svg viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="六種成長曲線的比較圖,橫軸是 n,縱軸是操作次數">';
    s += '<rect x="' + L + '" y="' + T + '" width="' + pw + '" height="' + ph + '" fill="#fff" stroke="#D1CFC5"/>';
    [0, .5, 1].forEach(function (t) { var y = T + ph - t * ph; s += '<line x1="' + L + '" x2="' + (W - R) + '" y1="' + y + '" y2="' + y + '" stroke="#F0EEE6"/><text x="' + (L - 4) + '" y="' + (y + 4) + '" text-anchor="end">' + Math.round(t * ymax) + "</text>"; });
    s += '<text x="' + L + '" y="' + (H - 8) + '">n = 1</text><text x="' + (W - R) + '" y="' + (H - 8) + '" text-anchor="end">n = ' + N + "</text>";
    CURVES.forEach(function (c) {
      var d = "", out = false;
      for (var n = 1; n <= N; n++) {
        var y = c.f(n); if (c.k === "log" && n === 1) y = 0;
        if (y > ymax) { d += (d ? "L" : "M") + sx(n).toFixed(1) + "," + sy(ymax).toFixed(1); out = true; break; }
        d += (d ? "L" : "M") + sx(n).toFixed(1) + "," + sy(y).toFixed(1);
      }
      s += '<path d="' + d + '" fill="none" stroke="' + c.color + '" stroke-width="2"' + (c.dash ? ' stroke-dasharray="' + c.dash + '"' : "") + "/>";
    });
    return s + '<text x="' + (L + 6) + '" y="' + (T + 12) + '">超出圖表上緣的線會停在頂端</text></svg>';
  }
  A.curves = { CURVES: CURVES, counts: counts, fmtNum: fmtNum, fmtTime: fmtTime };
  A.curvesInit = function (id) {
    if (typeof document === "undefined") return;
    var root = document.getElementById(id); if (!root) return;
    root.classList.add("cv");
    root.innerHTML = '<div class="cv-top"><label for="' + id + '-n">資料量 n</label><input id="' + id + '-n" type="range" min="1" max="100" value="10"><span class="cv-n" aria-live="polite"></span></div>' +
      '<div class="cv-main"><div class="cv-chart"></div><div><table class="cv-tbl"><thead><tr><th>成長</th><th>操作次數</th><th>若每次 1 微秒</th></tr></thead><tbody></tbody></table></div></div>' +
      '<p class="cv-note">「每次 1 微秒」只是方便感受大小的假設,不是實測;真實時間要看電腦與程式。</p>';
    var rng = root.querySelector("input"), nEl = root.querySelector(".cv-n"), ch = root.querySelector(".cv-chart"), tb = root.querySelector("tbody");
    function draw() {
      var n = +rng.value, c = counts(n); nEl.textContent = "n = " + n; ch.innerHTML = chart(n);
      tb.innerHTML = CURVES.map(function (cv) {
        var v = cv.k === "log" && n === 1 ? 0 : c[cv.k];
        return '<tr><td><span class="sw" style="background:' + cv.color + '"></span>' + cv.name + "</td><td>" + fmtNum(v) + "</td><td>" + fmtTime(v) + "</td></tr>";
      }).join("");
    }
    rng.addEventListener("input", draw); draw();
    root._cv = { set: function (n) { rng.value = n; draw(); } };
  };
  if (typeof module !== "undefined" && module.exports) module.exports = A;
})(typeof window !== "undefined" ? window : globalThis);
