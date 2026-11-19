(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var esc = A.esc || function (s) { return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"); };
  function row(cells, empty) {
    var h = '<div class="cells">';
    (cells || []).forEach(function (c, i) {
      h += '<div class="cell ' + (c.cls || "") + '"><span class="t">' + esc(c.t || "") + '</span><div class="b">' +
        (c.v === null || c.v === undefined ? "" : esc(c.v)) + '</div><span class="i">' + i + "</span></div>";
    });
    var n = (cells || []).length;
    for (var e = 0; e < (empty || 0); e++) h += '<div class="cell empty"><span class="t"></span><div class="b">0</div><span class="i">' + (n + e) + "</span></div>";
    return h + "</div>";
  }
  /* frame = { cells:[{v,cls,t}], empty:n, chips:[[label,value]] }  或  { rows:[{label,cells,empty}], chips } */
  A.cellsHtml = function (f) {
    var h = "";
    if (f.rows) f.rows.forEach(function (r) { h += (r.label ? '<div class="rowlab">' + esc(r.label) + "</div>" : "") + row(r.cells, r.empty); });
    else h = row(f.cells, f.empty);
    if (f.chips && f.chips.length) h += '<div class="kv">' + f.chips.map(function (c) { return "<span>" + esc(c[0]) + " <b>" + esc(c[1]) + "</b></span>"; }).join("") + "</div>";
    return h;
  };
})(typeof window !== "undefined" ? window : globalThis);
