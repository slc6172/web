(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var esc = A.esc;
  /* frame = { vars:[{n,t,addr,v,to,ref,cls}], heap:[{addr,val,next,cls}], msg, line } */
  A.memHtml = function (f) {
    var vars = (f.vars || []).map(function (x) {
      return '<div class="mv ' + (x.ref ? "ref " : "") + (x.cls || "") + '"><b>' + esc(x.n) + '</b><i>' + esc(x.t) + (x.addr ? " · " + esc(x.addr) : " · 與 " + esc(x.ref) + " 同一格") + '</i><span class="v">' + esc(x.v) + "</span>" +
        (x.to ? '<span class="to">→ 指向 ' + esc(x.to) + "</span>" : "") + "</div>";
    }).join("") || '<div class="memnote">(還沒有任何變數)</div>';
    var h = '<div class="mem' + (f.heap ? " two" : "") + '"><div class="col"><div class="rowlab">變數(stack)</div>' + vars + "</div>";
    if (f.heap) h += '<div class="col"><div class="rowlab">new 出來的節點(heap)</div>' + (f.heap.map(function (n) {
      return '<div class="mn ' + (n.cls || "") + '"><i>' + esc(n.addr) + "</i><span>val " + esc(n.val) + "</span><span>next " + esc(n.next) + "</span></div>";
    }).join("") || '<div class="memnote">(還沒有 new 任何東西)</div>') + "</div>";
    return h + "</div>" + '<div class="memnote">地址是示意數字,實際執行時由系統決定。</div>';
  };
})(typeof window !== "undefined" ? window : globalThis);
