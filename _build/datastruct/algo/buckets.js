(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var esc = A.esc;
  /* f = { buckets:[[{k,cls}]], cur:index|-1, calc:string, chips } */
  A.bucketsHtml = function (f) {
    var h = f.calc ? '<div class="calc">' + esc(f.calc) + "</div>" : "";
    h += '<div class="hb">' + f.buckets.map(function (chain, b) {
      return '<div class="hrow' + (f.cur === b ? " cur" : "") + '"><span class="ix">' + b + '</span><div class="chain">' +
        (chain.length ? chain.map(function (c, i) { return (i ? '<span class="ar">→</span>' : "") + '<span class="k ' + (c.cls || "") + '">' + esc(c.k) + "</span>"; }).join("") + '<span class="ar">→ null</span>' : '<span class="empty">(空)</span>') + "</div></div>";
    }).join("") + "</div>";
    if (f.chips && f.chips.length) h += '<div class="kv">' + f.chips.map(function (c) { return "<span>" + esc(c[0]) + " <b>" + esc(c[1]) + "</b></span>"; }).join("") + "</div>";
    return h;
  };
})(typeof window !== "undefined" ? window : globalThis);
