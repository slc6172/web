(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var HEAD = ["名稱", "標頭", "特性", "常見操作時間", "本系列"];
  /* cfg = { cats:[...], rows:[[名稱, 標頭, 類別, 特性, 時間, 篇章]], filters, q, table, count }(後四個是元素 id) */
  A.stlFilter = function (cfg) {
    var cat = cfg.cats[0], qEl = document.getElementById(cfg.q), tb = document.getElementById(cfg.table), cnt = document.getElementById(cfg.count), fb = document.getElementById(cfg.filters);
    function plain(s) { return s.replace(/<[^>]+>/g, "").replace(/&lt;/g, "<").replace(/&gt;/g, ">").toLowerCase(); }
    function draw() {
      var q = qEl.value.trim().toLowerCase(), n = 0;
      var h = '<div class="row">' + HEAD.map(function (x) { return '<div class="cell head">' + x + "</div>"; }).join("") + "</div>";
      cfg.rows.forEach(function (r) {
        if (cat !== cfg.cats[0] && r[2] !== cat) return;
        if (q && plain(r.join(" ")).indexOf(q) < 0) return;
        n++; h += '<div class="row"><div class="cell term"><code>' + r[0] + '</code></div><div class="cell"><code>' + r[1] + '</code></div><div class="cell">' + r[3] + '</div><div class="cell">' + r[4] + '</div><div class="cell">' + r[5] + "</div></div>";
      });
      if (!n) h += '<div class="row" style="grid-template-columns:1fr"><div class="cell">沒有符合的項目,換個關鍵字或類別試試。</div></div>';
      tb.innerHTML = h; cnt.textContent = "共 " + n + " 項";
    }
    fb.innerHTML = cfg.cats.map(function (c) { return '<button type="button" class="fbtn" aria-pressed="' + (c === cat) + '" data-cat="' + c + '">' + c + "</button>"; }).join("");
    fb.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-cat]"); if (!b) return;
      cat = b.getAttribute("data-cat");
      fb.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      draw();
    });
    qEl.addEventListener("input", draw);
    draw();
  };
})(typeof window !== "undefined" ? window : globalThis);
