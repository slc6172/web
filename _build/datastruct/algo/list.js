(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var esc = A.esc;
  var GAP = 100, NW = 74, NH = 34, X0 = 24, Y = [50, 128];
  /* frame = { nodes:[{id,v,next,slot,row,cls,hot}], tags:[{name,at}], headNull, chips } */
  A.listHtml = function (f) {
    var pos = {}, maxSlot = 0;
    f.nodes.forEach(function (n) { pos[n.id] = { x: X0 + n.slot * GAP + (f.headNull ? 0 : 0), y: Y[n.row] }; if (n.slot > maxSlot) maxSlot = n.slot; });
    var W = Math.max(X0 * 2 + (maxSlot + 1) * GAP + 30, 360), H = 190;
    var s = '<div class="lst"><svg width="' + W + '" height="' + H + '" viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="鏈結串列示意圖">' +
      '<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#3D3D3A"/></marker>' +
      '<marker id="arh" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#D97757"/></marker></defs>';
    if (f.headNull) s += '<text class="tg" x="' + X0 + '" y="' + (Y[0] + 22) + '">head → null(空串列)</text>';
    var tagAt = {};
    (f.tags || []).forEach(function (t) { (tagAt[t.at] = tagAt[t.at] || []).push(t.name); });
    f.nodes.forEach(function (n) {
      var p = pos[n.id], x1 = p.x + NW - 17, y1 = p.y + NH / 2;
      if (n.next && pos[n.next]) {
        var q = pos[n.next], x2 = q.x, y2 = q.y + NH / 2, d;
        if (q.y === p.y && Math.abs(q.x - p.x - GAP) < 2) d = "M" + x1 + "," + y1 + " L" + (x2 - 2) + "," + y2;
        else d = "M" + x1 + "," + y1 + " C" + (x1 + 34) + "," + y1 + " " + (x2 - 34) + "," + y2 + " " + (x2 - 2) + "," + y2;
        s += '<path class="ed' + (n.hot ? " hot" : "") + '" d="' + d + '" marker-end="url(#' + (n.hot ? "arh" : "ar") + ')"/>';
      } else {
        s += '<line class="ed' + (n.hot ? " hot" : "") + '" x1="' + x1 + '" y1="' + y1 + '" x2="' + (x1 + 20) + '" y2="' + y1 + '"/><text class="nl" x="' + (x1 + 24) + '" y="' + (y1 + 4) + '">null</text>';
      }
    });
    f.nodes.forEach(function (n) {
      var p = pos[n.id];
      s += '<g class="nd ' + (n.cls || "") + '"><rect class="box" x="' + p.x + '" y="' + p.y + '" width="' + NW + '" height="' + NH + '" rx="7"/>' +
        '<line x1="' + (p.x + NW - 34) + '" y1="' + p.y + '" x2="' + (p.x + NW - 34) + '" y2="' + (p.y + NH) + '" stroke="#D1CFC5"/>' +
        '<text x="' + (p.x + (NW - 34) / 2) + '" y="' + (p.y + 22) + '" text-anchor="middle">' + esc(n.v) + '</text><circle cx="' + (p.x + NW - 17) + '" cy="' + (p.y + NH / 2) + '" r="4" fill="#3D3D3A"/></g>';
      var names = tagAt[n.id];
      if (names) {
        var down = n.row === 1, ty = down ? p.y + NH + 18 : p.y - 10;
        s += '<text class="tg" x="' + (p.x + 2) + '" y="' + ty + '">' + (down ? "↑ " : "↓ ") + esc(names.join(", ")) + "</text>";
      }
    });
    s += "</svg></div>";
    if (f.chips && f.chips.length) s += '<div class="kv">' + f.chips.map(function (c) { return "<span>" + esc(c[0]) + " <b>" + esc(c[1]) + "</b></span>"; }).join("") + "</div>";
    return s;
  };
})(typeof window !== "undefined" ? window : globalThis);
