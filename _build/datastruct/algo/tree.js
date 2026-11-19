(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var esc = A.esc;
  /* f.tree = { root:id|null, nodes:{ id:{label,l,r,cls} } }  ;  f.chips = [[label,value]] */
  A.treeHtml = function (f) {
    var T = f.tree;
    if (!T || !T.root) return '<div class="memnote">(還沒有內容,按「執行」開始)</div>' + chipsHtml(f);
    var pos = {}, leaf = 0, maxD = 0, SX = 76, SY = 58, X0 = 40, Y0 = 26;
    (function lay(id, d) {
      var n = T.nodes[id]; if (d > maxD) maxD = d;
      var kids = [n.l, n.r].filter(function (k) { return k && T.nodes[k]; });
      if (!kids.length) { pos[id] = { x: leaf++, d: d }; return pos[id].x; }
      var xs = kids.map(function (k) { return lay(k, d + 1); });
      var onlyL = xs.length === 1 && T.bst && n.l && T.nodes[n.l];
      pos[id] = { x: xs.length === 1 ? (T.bst ? xs[0] + (onlyL ? 0.4 : -0.4) : xs[0]) : (xs[0] + xs[1]) / 2, d: d }; return pos[id].x;
    })(T.root, 0);
    var minX = 0, maxX = Math.max(leaf - 1, 0);
    Object.keys(pos).forEach(function (id) { if (pos[id].x < minX) minX = pos[id].x; if (pos[id].x > maxX) maxX = pos[id].x; });
    if (minX < 0) Object.keys(pos).forEach(function (id) { pos[id].x -= minX; });
    var W = Math.max((maxX - minX + 1) * SX + 20, 340), H = (maxD + 1) * SY + 16, s = '<div class="tr"><svg width="' + W + '" height="' + H + '" viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="樹狀示意圖">';
    function px(id) { return X0 + pos[id].x * SX; } function py(id) { return Y0 + pos[id].d * SY; }
    Object.keys(pos).forEach(function (id) {
      var n = T.nodes[id];
      [n.l, n.r].forEach(function (k) { if (k && pos[k]) s += '<line class="ed" x1="' + px(id) + '" y1="' + (py(id) + 13) + '" x2="' + px(k) + '" y2="' + (py(k) - 13) + '"/>'; });
    });
    Object.keys(pos).forEach(function (id) {
      var n = T.nodes[id], w = Math.max(40, String(n.label).length * 7.4 + 16);
      s += '<g class="tn ' + (n.cls || "") + '"><rect x="' + (px(id) - w / 2) + '" y="' + (py(id) - 13) + '" width="' + w + '" height="26" rx="13"/><text x="' + px(id) + '" y="' + (py(id) + 4) + '" text-anchor="middle">' + esc(n.label) + "</text></g>";
    });
    return s + "</svg></div>" + chipsHtml(f);
  };
  function chipsHtml(f) { return f.chips && f.chips.length ? '<div class="kv">' + f.chips.map(function (c) { return "<span>" + esc(c[0]) + " <b>" + esc(c[1]) + "</b></span>"; }).join("") + "</div>" : ""; }
  A.stackHtml = function (f) {
    var st = f.stack || [];
    return '<div class="stk"><span class="lab">呼叫堆疊(右邊是目前執行的)</span>' + (st.length ? st.map(function (x, i) { return '<span class="f' + (i === st.length - 1 ? " top" : "") + '">' + esc(x) + "</span>"; }).join("") : '<span class="lab">(空)</span>') + "</div>";
  };
})(typeof window !== "undefined" ? window : globalThis);
