(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  /* f = { N, placed:[col or -1 per row], cls:{"r,c":"cur|bad|ok"} } */
  A.boardHtml = function (f) {
    var size = f.N <= 5 ? 48 : 42;
    var h = '<div class="qb" role="img" aria-label="' + f.N + ' 乘 ' + f.N + ' 棋盤" style="grid-template-columns:repeat(' + f.N + ',' + size + 'px)">';
    for (var r = 0; r < f.N; r++) for (var c = 0; c < f.N; c++) {
      var k = r + "," + c, q = f.placed[r] === c, cls = f.cls[k] || "";
      h += '<div class="qs ' + ((r + c) % 2 ? "d " : "") + cls + '">' + (q ? "♛" : cls === "bad" ? "×" : "") + "</div>";
    }
    return h + "</div>";
  };
})(typeof window !== "undefined" ? window : globalThis);
