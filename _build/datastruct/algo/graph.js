(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var esc = A.esc || function (s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); };
  /* g = { W, H, nodes:[{x,y,t,cls,sub}], edges:[{a,b,w,cls}] } */
  A.graphHtml = function (g) {
    var s = '<div class="gv"><svg viewBox="0 0 ' + g.W + " " + g.H + '" style="max-width:' + g.W + 'px" role="img" aria-label="節點圖">';
    g.edges.forEach(function (e) {
      var a = g.nodes[e.a], b = g.nodes[e.b];
      s += '<line class="ge ' + (e.cls || "") + '" x1="' + a.x + '" y1="' + a.y + '" x2="' + b.x + '" y2="' + b.y + '"/>';
    });
    g.edges.forEach(function (e) {
      if (e.w === undefined || e.w === null) return;
      var a = g.nodes[e.a], b = g.nodes[e.b];
      s += '<text class="gw" x="' + ((a.x + b.x) / 2) + '" y="' + ((a.y + b.y) / 2) + '">' + esc(e.w) + "</text>";
    });
    g.nodes.forEach(function (n) {
      s += '<g class="gn ' + (n.cls || "") + '"><circle cx="' + n.x + '" cy="' + n.y + '" r="17"/><text x="' + n.x + '" y="' + n.y + '">' + esc(n.t) + "</text>";
      if (n.sub !== undefined && n.sub !== null) s += '<text class="gs" x="' + n.x + '" y="' + (n.y - 28) + '">' + esc(n.sub) + "</text>";
      s += "</g>";
    });
    return s + "</svg></div>";
  };
  /* f = { n, m:[[0/1]], hl:[[r,c]] } */
  A.matrixHtml = function (f) {
    var h = '<div class="gcap">鄰接矩陣(列 → 行)</div><table class="gmat"><tr><th></th>';
    for (var j = 0; j < f.n; j++) h += "<th>" + j + "</th>";
    h += "</tr>";
    for (var i = 0; i < f.n; i++) {
      h += "<tr><th>" + i + "</th>";
      for (var k = 0; k < f.n; k++) {
        var hl = (f.hl || []).some(function (p) { return p[0] === i && p[1] === k; });
        h += '<td class="' + (f.m[i][k] ? "on " : "") + (hl ? "hl" : "") + '">' + f.m[i][k] + "</td>";
      }
      h += "</tr>";
    }
    return h + "</table>";
  };
  /* f = { n, adj:[[...]], hl:[[node, idx]] } */
  A.adjHtml = function (f) {
    var h = '<div class="gcap">鄰接表</div><div class="gadj">';
    for (var i = 0; i < f.n; i++) {
      h += '<div class="gr"><span class="gk">' + i + "</span>";
      if (!f.adj[i].length) h += '<span class="ge0">(空)</span>';
      f.adj[i].forEach(function (v, k) {
        var hl = (f.hl || []).some(function (p) { return p[0] === i && p[1] === k; });
        h += (k ? '<span class="ga">→</span>' : "") + '<span class="gi' + (hl ? " hl" : "") + '">' + v + "</span>";
      });
      h += "</div>";
    }
    return h + "</div>";
  };
})(typeof window !== "undefined" ? window : globalThis);
