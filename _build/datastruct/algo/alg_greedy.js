(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var CODE_GREEDY = "std::vector<int> greedyChange(const std::vector<int>& coins, int amount) {\n    std::vector<int> used;\n    for (int c : coins) {\n        while (amount >= c) {\n            used.push_back(c);\n            amount -= c;\n        }\n    }\n    if (amount != 0) {\n        used.clear();\n    }\n    return used;\n}";
  var CODE_NQ = "bool safe(const std::vector<int>& cols, int row, int c) {\n    for (int r = 0; r < row; ++r) {\n        if (cols[r] == c || std::abs(cols[r] - c) == row - r) {\n            return false;\n        }\n    }\n    return true;\n}\n\nvoid solve(int n, int row, std::vector<int>& cols, std::vector<std::vector<int>>& sols) {\n    if (row == n) {\n        sols.push_back(cols);\n        return;\n    }\n    for (int c = 0; c < n; ++c) {\n        if (safe(cols, row, c)) {\n            cols[row] = c;\n            solve(n, row + 1, cols, sols);\n        }\n    }\n}";
  var SETS = { us: [25, 10, 5, 1], f1: [4, 3, 1], f2: [12, 10, 5, 1], f3: [5, 2] };
  var SETNAMES = { us: "25, 10, 5, 1(美國硬幣)", f1: "4, 3, 1(會失敗)", f2: "12, 10, 5, 1(會失敗)", f3: "5, 2(連解都找不到)" };
  function best(coins, amount) {
    var INF = 1e9, dp = new Array(amount + 1).fill(INF); dp[0] = 0;
    for (var a = 1; a <= amount; a++) coins.forEach(function (c) { if (a >= c && dp[a - c] !== INF && dp[a - c] + 1 < dp[a]) dp[a] = dp[a - c] + 1; });
    return dp[amount] === INF ? -1 : dp[amount];
  }
  function greedyPlain(coins, amount) { var used = []; coins.forEach(function (c) { while (amount >= c) { used.push(c); amount -= c; } }); return amount !== 0 ? [] : used; }
  function greedyRun(setKey, amount) {
    var coins = SETS[setKey];
    if (!coins) return { error: "請選一組硬幣。" };
    if (!(Number.isInteger(amount) && amount >= 1 && amount <= 99)) return { error: "金額請輸入 1 到 99 的整數。" };
    var rest = amount, used = [], fr = [];
    function snap(line, msg, cur, extra) {
      fr.push({ rows: [{ label: "硬幣面額(由大到小)", cells: coins.map(function (c, i) { return { v: c, cls: i === cur ? "cur" : "" }; }), empty: 0 },
        { label: "目前選的硬幣", cells: used.map(function (c) { return { v: c, cls: "new" }; }), empty: 0 }],
        chips: [["剩下金額", rest], ["已用枚數", used.length]].concat(extra || []), line: line, msg: msg });
    }
    snap(2, "要湊 <b>" + amount + "</b>。貪婪的做法:<b>每一步都先拿最大的、拿得下的硬幣</b>,從最大的面額開始,不回頭。", -1);
    coins.forEach(function (c, i) {
      if (rest < c) { snap([3, 4], "面額 " + c + " 比剩下的 " + rest + " 大,拿不下,換下一種。", i); return; }
      while (rest >= c) { rest -= c; used.push(c); snap([4, 6], "剩下的夠拿 " + c + ",拿一枚,剩 <b>" + rest + "</b>。", i); }
    });
    var opt = best(coins, amount), ok = rest === 0, msg, line;
    if (ok) {
      line = 12;
      msg = used.length === opt ? "湊齊了,貪婪用 <b>" + used.length + "</b> 枚。最少也是 " + opt + " 枚,這組硬幣貪婪<b>剛好是對的</b>。" : "湊齊了,貪婪用 <b>" + used.length + "</b> 枚,但最少其實只要 <b>" + opt + "</b> 枚。<b>貪婪失敗</b>:每一步拿最大的,不保證整體最少。";
    } else {
      line = [9, 10];
      msg = opt === -1 ? "最後剩 " + rest + " 湊不下,<code>used.clear()</code>。這個金額用這組硬幣<b>本來就湊不出來</b>。" : "最後剩 " + rest + " 湊不下,貪婪<b>失敗</b>(<code>used.clear()</code>)。但其實可以湊出來,最少 <b>" + opt + "</b> 枚。貪婪拿了不回頭,卡死了。";
    }
    snap(line, msg, -1, [["最少枚數(DP)", opt]]);
    return { frames: fr, used: ok ? used : [], greedyOk: ok, best: opt };
  }
  function idleGreedy() { return { rows: [], chips: [], msg: "選一組硬幣和金額,按「執行」。" }; }

  /* ---- N 皇后回溯 ---- */
  function nqRun(n, mode) {
    if (!(n === 4 || n === 5 || n === 6)) return { error: "N 只能是 4、5 或 6。" };
    if (mode !== "first" && mode !== "all") return { error: "請選一種模式。" };
    var placed = new Array(n).fill(-1), fr = [], st = { tries: 0, backs: 0, sols: 0 }, sols = [], stop = false;
    function snap(line, msg, cls) { fr.push({ N: n, placed: placed.slice(), cls: cls || {}, chips: [["嘗試", st.tries], ["退回", st.backs], ["解", st.sols]], line: line, msg: msg }); }
    function check(row, c) {
      for (var r = 0; r < row; r++) {
        if (placed[r] === c) return { ok: false, by: r, why: "同一欄" };
        if (Math.abs(placed[r] - c) === row - r) return { ok: false, by: r, why: "同一條斜線" };
      }
      return { ok: true };
    }
    function solve(row) {
      var any = 0;
      if (row === n) {
        st.sols++; sols.push(placed.slice());
        var okc = {}; placed.forEach(function (c, r) { okc[r + "," + c] = "ok"; });
        snap([11, 12], "第 " + n + " 列都放好了,<code>sols.push_back(cols)</code>:找到第 <b>" + st.sols + "</b> 組解!" + (mode === "first" ? "(動畫在第一組解停下;程式會繼續找其他組。)" : ""), okc);
        if (mode === "first") stop = true;
        return 1;
      }
      for (var c = 0; c < n && !stop; c++) {
        st.tries++;
        var s = check(row, c), key = row + "," + c, cls = {};
        if (!s.ok) {
          cls[key] = "bad"; cls[s.by + "," + placed[s.by]] = "bad";
          snap([3, 4], "試第 " + (row + 1) + " 列第 " + (c + 1) + " 欄:和第 " + (s.by + 1) + " 列的皇后<b>" + s.why + "</b>,不行。", cls);
          continue;
        }
        placed[row] = c; any++; cls[key] = "cur";
        snap([16, 17], "試第 " + (row + 1) + " 列第 " + (c + 1) + " 欄:和上面的皇后都不衝突,<b>放下</b>,遞迴去第 " + (row + 2) + " 列。", cls);
        var got = solve(row + 1);
        if (stop) return 1;
        placed[row] = -1; st.backs++;
        snap([18, 19], got ? "下面的列試完了,<b>退回</b>:拿起第 " + (row + 1) + " 列的皇后,試下一欄。" : "第 " + (row + 2) + " 列每一欄都衝突:<b>死路</b>。<b>退回</b>,拿起第 " + (row + 1) + " 列的皇后,試下一欄。", {});
      }
      return any;
    }
    snap(undefined, n + " 個皇后要放在 " + n + "×" + n + " 的棋盤上,<b>任兩個都不能同欄、同列、同斜線</b>。一列放一個,從第 1 列開始,試、錯了就退回。", {});
    solve(0);
    if (!stop) snap(undefined, "全部試完了:" + n + " 皇后一共 <b>" + st.sols + "</b> 組解(嘗試了 " + st.tries + " 次,退回 " + st.backs + " 次)。", {});
    return { frames: fr, sols: sols, tries: st.tries };
  }
  function idleNq() { return { N: 4, placed: [-1, -1, -1, -1], cls: {}, chips: [], msg: "選 N 與模式,按「執行」。" }; }
  A.greedy = { CODE_GREEDY: CODE_GREEDY, CODE_NQ: CODE_NQ, SETS: SETS, SETNAMES: SETNAMES, greedyRun: greedyRun, greedyPlain: greedyPlain, best: best, idleGreedy: idleGreedy, nqRun: nqRun, idleNq: idleNq };
  if (typeof module !== "undefined" && module.exports) module.exports = A;
})(typeof window !== "undefined" ? window : globalThis);
