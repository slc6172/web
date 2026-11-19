(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var CODE_REC = [
    "int fact(int n) {", "    if (n <= 1) {", "        return 1;", "    }", "    return n * fact(n - 1);", "}", "",
    "int fib(int n) {", "    if (n <= 1) {", "        return n;", "    }", "    return fib(n - 1) + fib(n - 2);", "}"].join("\n");
  var LIM = { fact: [1, 8], fib: [1, 6] };
  function isInt(x) { return typeof x === "number" && isFinite(x) && Math.floor(x) === x; }
  function fibCalls(n) { var a = 1, b = 1; if (n <= 1) return 1; for (var i = 2; i <= n; i++) { var c = a + b + 1; a = b; b = c; } return b; }
  function run(fn, n) {
    if (!LIM[fn]) return { error: "請選 fact 或 fib。" };
    if (!isInt(n) || n < LIM[fn][0] || n > LIM[fn][1]) return { error: fn + " 的 n 請輸入 " + LIM[fn][0] + " 到 " + LIM[fn][1] + " 的整數(再大,圖就看不清楚了)。" };
    var nodes = {}, cnt = 0, stack = [], fr = [], calls = 0, seen = {}, dups = 0, rootId = null;
    function lab(id) { var nd = nodes[id]; return nd.name + "(" + nd.n + ")" + (nd.val !== undefined ? "=" + nd.val : ""); }
    function snap(line, msg, cur) {
      var tn = {};
      Object.keys(nodes).forEach(function (id) {
        var nd = nodes[id], cls = nd.val !== undefined ? "ok" : ""; if (id === cur) cls = "cur"; if (nd.dup) cls += " dup";
        tn[id] = { label: lab(id), l: nd.l, r: nd.r, cls: cls };
      });
      var chips = [["呼叫次數", calls], ["目前深度", stack.length]]; if (fn === "fib") chips.push(["重複計算的呼叫", dups]);
      fr.push({ tree: { root: rootId, nodes: tn }, stack: stack.map(lab), chips: chips, line: line, msg: msg });
    }
    function call(nv, parent, side) {
      var id = "c" + (cnt++), nd = { name: fn, n: nv, l: null, r: null, val: undefined, dup: false }; calls++;
      if (fn === "fib") { if (seen[nv]) { nd.dup = true; dups++; } seen[nv] = 1; }
      nodes[id] = nd; if (parent) nodes[parent][side] = id; else rootId = id;
      stack.push(id);
      snap(fn === "fact" ? [1, 2] : [8, 9], "進入 <code>" + fn + "(" + nv + ")</code>。" + (nv <= 1 ? "n ≤ 1,是<b>基底條件</b>。" : "n &gt; 1,還不是基底條件,要繼續呼叫。") + (nd.dup ? "<b>這個呼叫之前已經算過了(虛線框)。</b>" : ""), id);
      var val;
      if (nv <= 1) { val = fn === "fact" ? 1 : nv; nd.val = val; snap(fn === "fact" ? 3 : 10, "基底條件:直接回傳 <b>" + val + "</b>,不再呼叫自己。", id); }
      else if (fn === "fact") { var r = call(nv - 1, id, "l"); val = nv * r; nd.val = val; snap(5, "<code>fact(" + (nv - 1) + ")</code> 回傳了 " + r + ",所以 <code>fact(" + nv + ")</code> = " + nv + " × " + r + " = <b>" + val + "</b>。", id); }
      else {
        var a = call(nv - 1, id, "l"); snap(12, "<code>fib(" + (nv - 1) + ")</code> 回來了(= " + a + "),接著算 <code>fib(" + (nv - 2) + ")</code>。", id);
        var b = call(nv - 2, id, "r"); val = a + b; nd.val = val; snap(12, "<code>fib(" + (nv - 1) + ") + fib(" + (nv - 2) + ")</code> = " + a + " + " + b + " = <b>" + val + "</b>。", id);
      }
      stack.pop(); return val;
    }
    var value = call(n, null, null);
    snap(fn === "fact" ? 5 : 12, "最外層的 <code>" + fn + "(" + n + ")</code> 回傳 <b>" + value + "</b>。一共呼叫了 <b>" + calls + "</b> 次函式" + (fn === "fib" ? ",其中 " + dups + " 次是重複算已經算過的" : "") + "。", null);
    return { frames: fr, result: null, value: value, calls: calls, dups: dups };
  }
  A.rec = { CODE_REC: CODE_REC, LIM: LIM, run: run, fibCalls: fibCalls };
  if (typeof module !== "undefined" && module.exports) module.exports = A;
})(typeof window !== "undefined" ? window : globalThis);
