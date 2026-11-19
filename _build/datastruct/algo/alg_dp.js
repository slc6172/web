(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var CODE_DP = "long long fib(int n) {\n    std::vector<long long> dp(n + 2);\n    dp[0] = 0;\n    dp[1] = 1;\n    for (int i = 2; i <= n; ++i) {\n        dp[i] = dp[i - 1] + dp[i - 2];\n    }\n    return dp[n];\n}\n\nlong long climbStairs(int n) {\n    std::vector<long long> dp(n + 2);\n    dp[0] = 1;\n    dp[1] = 1;\n    for (int i = 2; i <= n; ++i) {\n        dp[i] = dp[i - 1] + dp[i - 2];\n    }\n    return dp[n];\n}\n\nint knapsack(const std::vector<int>& wt, const std::vector<int>& val, int cap) {\n    int n = static_cast<int>(wt.size());\n    std::vector<std::vector<int>> dp(n + 1, std::vector<int>(cap + 1, 0));\n    for (int i = 1; i <= n; ++i) {\n        for (int w = 0; w <= cap; ++w) {\n            dp[i][w] = dp[i - 1][w];\n            if (w >= wt[i - 1]) {\n                dp[i][w] = std::max(dp[i][w], dp[i - 1][w - wt[i - 1]] + val[i - 1]);\n            }\n        }\n    }\n    return dp[n][cap];\n}";
  var WT = [1, 3, 4, 5], VAL = [1, 4, 5, 7];
  var NAMES = { fib: "費氏數列 fib(n)", stairs: "爬樓梯(1 或 2 階)", knap: "0/1 背包" };
  function cellsOf(v, cls) { return v.map(function (x, i) { return x === null ? { v: 0, cls: "empty" } : { v: x, cls: cls[i] || "" }; }); }
  function runLine(kind, n) {
    if (!(Number.isInteger(n) && n >= 2 && n <= 15)) return { error: "n 請輸入 2 到 15 的整數。" };
    var isF = kind === "fib", dp = new Array(n + 1).fill(null), fr = [], adds = 0;
    var L = isF ? { init: [2, 4], loop: [5, 6], ret: 8 } : { init: [12, 14], loop: [15, 16], ret: 18 };
    function snap(line, msg, cls) { fr.push({ rows: [{ label: "dp[i](格子下的數字是 i)", cells: cellsOf(dp, cls || {}), empty: 0 }], chips: [["已填", dp.filter(function (x) { return x !== null; }).length + "/" + (n + 1)], ["加法次數", adds]], line: line, msg: msg }); }
    dp[0] = isF ? 0 : 1; dp[1] = 1;
    snap(L.init, isF ? "先填已知的:<code>dp[0] = 0</code>、<code>dp[1] = 1</code>。其他格子都要靠前面的格子算出來。" : "先填已知的:爬到第 0 階有 1 種(不動)、第 1 階有 1 種。其他格子都要靠前面的格子算出來。", { 0: "cur", 1: "cur" });
    for (var i = 2; i <= n; i++) {
      dp[i] = dp[i - 1] + dp[i - 2]; adds++;
      snap(L.loop, "<code>dp[" + i + "] = dp[" + (i - 1) + "] + dp[" + (i - 2) + "]</code> = " + dp[i - 1] + " + " + dp[i - 2] + " = <b>" + dp[i] + "</b>。" + (isF ? "" : "(最後一步若是爬 1 階,前面有 dp[" + (i - 1) + "] 種;若是爬 2 階,前面有 dp[" + (i - 2) + "] 種。)"), (function () { var o = {}; o[i] = "cur"; o[i - 1] = "new"; o[i - 2] = "new"; return o; })());
    }
    snap(L.ret, "<code>return dp[" + n + "]</code> = <b>" + dp[n] + "</b>。每一格只算一次,一共只做了 " + adds + " 次加法。", (function () { var o = {}; o[n] = "cur"; return o; })());
    return { frames: fr, answer: dp[n], dp: dp };
  }
  function table(cap) {
    var n = WT.length, dp = [];
    for (var i = 0; i <= n; i++) { dp.push(new Array(cap + 1).fill(0)); }
    for (var a = 1; a <= n; a++) for (var w = 0; w <= cap; w++) { dp[a][w] = dp[a - 1][w]; if (w >= WT[a - 1]) dp[a][w] = Math.max(dp[a][w], dp[a - 1][w - WT[a - 1]] + VAL[a - 1]); }
    return dp;
  }
  function runKnap(cap) {
    if (!(Number.isInteger(cap) && cap >= 1 && cap <= 10)) return { error: "背包容量請輸入 1 到 10 的整數。" };
    var n = WT.length, T = [], fr = [], filled = 0, total = (n + 1) * (cap + 1);
    for (var i = 0; i <= n; i++) T.push(new Array(cap + 1).fill(null));
    function snap(line, msg, cls) {
      var rows = T.map(function (row, a) { return { label: a === 0 ? "沒有物品" : "前 " + a + " 個物品(最後一個:重 " + WT[a - 1] + ",值 " + VAL[a - 1] + ")", cells: row.map(function (x, w) { var k = a + "," + w; return x === null ? { v: 0, cls: "empty" } : { v: x, cls: cls[k] || "" }; }), empty: 0 }; });
      fr.push({ rows: rows, chips: [["已填", filled + "/" + total]], line: line, msg: msg });
    }
    for (var w0 = 0; w0 <= cap; w0++) { T[0][w0] = 0; filled++; }
    snap(23, "第 0 列:<b>沒有物品</b>,不管背包多大,價值都是 0。格子下的數字是<b>背包容量</b> w,每一列多考慮一個物品。", {});
    for (var a = 1; a <= n; a++) for (var w = 0; w <= cap; w++) {
      var wt = WT[a - 1], vl = VAL[a - 1], skip = T[a - 1][w], cls = {};
      cls[a + "," + w] = "cur"; cls[(a - 1) + "," + w] = "new";
      if (w < wt) {
        T[a][w] = skip; filled++;
        snap([26, 27], "物品 " + a + "(重 " + wt + ")放不進容量 " + w + ":<code>dp[" + a + "][" + w + "] = dp[" + (a - 1) + "][" + w + "]</code> = <b>" + skip + "</b>(只能不拿)。", cls);
      } else {
        var take = T[a - 1][w - wt] + vl; cls[(a - 1) + "," + (w - wt)] = "new";
        T[a][w] = Math.max(skip, take); filled++;
        snap([26, 28], "容量 " + w + ",考慮物品 " + a + "(重 " + wt + ",值 " + vl + "):<b>不拿</b> = dp[" + (a - 1) + "][" + w + "] = " + skip + ";<b>拿</b> = dp[" + (a - 1) + "][" + (w - wt) + "] + " + vl + " = " + take + "。取較大的:<b>" + T[a][w] + "</b>。", cls);
      }
    }
    var fin = {}; fin[n + "," + cap] = "cur";
    snap(32, "<code>return dp[" + n + "][" + cap + "]</code> = <b>" + T[n][cap] + "</b>:容量 " + cap + " 的背包,最多能裝價值 " + T[n][cap] + "。", fin);
    return { frames: fr, answer: T[n][cap], table: T };
  }
  function run(kind, n) {
    if (!NAMES[kind]) return { error: "請選一個問題。" };
    return kind === "knap" ? runKnap(n) : runLine(kind, n);
  }
  function idle() { return { rows: [], chips: [], msg: "選一個問題,按「執行」。費氏與爬樓梯填一排格子,背包填一張二維的表。" }; }
  /* 點格子看依賴:dp[i][w] 依賴哪些格子 */
  function deps(cap, a, w) {
    var T = table(cap);
    if (a === 0) return { cells: [], text: "第 0 列:沒有物品,價值一定是 0,不依賴別的格子。" };
    var wt = WT[a - 1], vl = VAL[a - 1], skip = T[a - 1][w];
    if (w < wt) return { cells: [[a - 1, w]], text: "dp[" + a + "][" + w + "]:物品 " + a + "(重 " + wt + ")放不進容量 " + w + ",只能不拿,直接抄上面那格 dp[" + (a - 1) + "][" + w + "] = " + skip + "。" };
    var take = T[a - 1][w - wt] + vl;
    return { cells: [[a - 1, w], [a - 1, w - wt]], text: "dp[" + a + "][" + w + "] = max(不拿 dp[" + (a - 1) + "][" + w + "] = " + skip + ",拿 dp[" + (a - 1) + "][" + (w - wt) + "] + " + vl + " = " + take + ") = " + T[a][w] + "。它依賴上一列的兩格。" };
  }
  A.dp = { CODE_DP: CODE_DP, NAMES: NAMES, WT: WT, VAL: VAL, run: run, idle: idle, table: table, deps: deps };
  if (typeof module !== "undefined" && module.exports) module.exports = A;
})(typeof window !== "undefined" ? window : globalThis);
