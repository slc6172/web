(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var esc = A.esc || function (s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); };
  /* g = { R, C, wall:[[bool]], cls:{"r,c":"seen|fr|cur"}, txt:{"r,c":text}, S:[r,c], G:[r,c] } */
  A.gridHtml = function (g) {
    var size = g.C <= 7 ? 42 : 34;
    var h = '<div class="maze" style="grid-template-columns:repeat(' + g.C + ',minmax(0,' + size + 'px));max-width:' + (g.C * (size + 4)) + 'px">';
    for (var r = 0; r < g.R; r++) for (var c = 0; c < g.C; c++) {
      var k = r + "," + c, cls = g.wall[r][c] ? "wall" : (g.cls[k] || ""), t = "";
      if (g.S[0] === r && g.S[1] === c) { cls += " mS"; t = "S"; }
      else if (g.G[0] === r && g.G[1] === c) { cls += " mG"; t = "G"; }
      else if (!g.wall[r][c] && g.txt[k] !== undefined) t = g.txt[k];
      h += '<div class="mz ' + cls + '">' + esc(t) + "</div>";
    }
    return h + "</div>" + '<div class="mazelegend"><span><i class="wall"></i>牆</span><span><i class="fr"></i>在 queue / stack 裡</span><span><i class="cur"></i>目前這格</span><span><i class="seen"></i>已處理</span></div>';
  };
})(typeof window !== "undefined" ? window : globalThis);
