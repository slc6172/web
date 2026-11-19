(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var esc = A.esc;
  /* f = { vals, cls, tags, chips }  或  { rows:[{label,vals,cls,tags}], chips };vals 內的 null 代表空槽 */
  function row(f, vals, cls, tags, mx, sm) {
    return '<div class="bars' + (sm ? " sm" : "") + '">' + vals.map(function (v, i) {
      var empty = v === null || v === undefined;
      return '<div class="sbar ' + ((cls && cls[i]) || "") + (empty ? " empty" : "") + '"><span class="t">' + esc((tags && tags[i]) || "") + '</span><div class="col" style="height:' + (empty ? 10 : (14 + Math.round(v / mx * (sm ? 78 : 138)))) + 'px"></div><span class="v">' + (empty ? "" : esc(v)) + "</span></div>";
    }).join("") + "</div>";
  }
  A.barsHtml = function (f) {
    var h = "", all;
    if (f.rows) {
      all = [].concat.apply([], f.rows.map(function (r) { return r.vals; })).filter(function (x) { return x !== null && x !== undefined; });
      var mx2 = Math.max.apply(null, all.concat([1]));
      f.rows.forEach(function (r) { h += '<div class="rowlab">' + esc(r.label) + "</div>" + row(f, r.vals, r.cls, r.tags, mx2, true); });
    } else { var vals = f.vals || []; h = row(f, vals, f.cls, f.tags, Math.max.apply(null, vals.concat([1])), false); }
    if (f.chips && f.chips.length) h += '<div class="kv">' + f.chips.map(function (c) { return "<span>" + esc(c[0]) + " <b>" + esc(c[1]) + "</b></span>"; }).join("") + "</div>";
    return h;
  };
})(typeof window !== "undefined" ? window : globalThis);
