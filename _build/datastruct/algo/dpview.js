(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  /* 背包的最終表,每一格都能點:自己標橘色,依賴的格子標綠色 */
  A.dpDeps = function (id, cap) {
    var root = document.getElementById(id), P = A.dp, T = P.table(cap), n = P.WT.length;
    var h = '<div class="dpwrap"><table class="dpt"><tr><th></th>';
    for (var w = 0; w <= cap; w++) h += "<th>w=" + w + "</th>";
    h += "</tr>";
    for (var a = 0; a <= n; a++) {
      h += '<tr><th class="rl">' + (a === 0 ? "沒有物品" : "物品 " + a + "(重 " + P.WT[a - 1] + ",值 " + P.VAL[a - 1] + ")") + "</th>";
      for (w = 0; w <= cap; w++) h += '<td><button type="button" data-a="' + a + '" data-w="' + w + '" aria-label="dp[' + a + '][' + w + '] = ' + T[a][w] + '">' + T[a][w] + "</button></td>";
      h += "</tr>";
    }
    h += '</table></div><div class="dpinfo" aria-live="polite">點任一格,看它是怎麼算出來的。<b>橘色</b>是你點的格子,<b>綠色</b>是它依賴的格子。</div>';
    root.innerHTML = h;
    var info = root.querySelector(".dpinfo");
    root.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-a]"); if (!b) return;
      root.querySelectorAll("button").forEach(function (x) { x.classList.remove("cur", "dep"); });
      var a = +b.getAttribute("data-a"), w = +b.getAttribute("data-w"), d = P.deps(cap, a, w);
      b.classList.add("cur");
      d.cells.forEach(function (p) { var t = root.querySelector('button[data-a="' + p[0] + '"][data-w="' + p[1] + '"]'); if (t) t.classList.add("dep"); });
      info.textContent = d.text;
    });
  };
})(typeof window !== "undefined" ? window : globalThis);
