(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var CODE_DIJK = "struct Edge {\n    int to;\n    int w;\n};\n\nusing Graph = std::vector<std::vector<Edge>>;\nusing Item = std::pair<int, int>;\nconst int INF = 1000000000;\n\nvoid dijkstra(const Graph& g, int src, std::vector<int>& dist, std::vector<int>& prev) {\n    dist.assign(g.size(), INF);\n    prev.assign(g.size(), -1);\n    std::priority_queue<Item, std::vector<Item>, std::greater<Item>> pq;\n    dist[src] = 0;\n    pq.push({0, src});\n    while (!pq.empty()) {\n        Item top = pq.top();\n        pq.pop();\n        int d = top.first;\n        int u = top.second;\n        if (d > dist[u]) {\n            continue;\n        }\n        for (const Edge& e : g[u]) {\n            if (d + e.w < dist[e.to]) {\n                dist[e.to] = d + e.w;\n                prev[e.to] = u;\n                pq.push({dist[e.to], e.to});\n            }\n        }\n    }\n}";
  var INF = 1000000000;
  var PRESETS = {
    classic: { n: 6, pos: [[40, 112], [108, 50], [108, 172], [214, 50], [276, 112], [214, 172]],
      edges: [[0, 1, 7], [0, 2, 9], [0, 5, 14], [1, 2, 10], [1, 3, 15], [2, 3, 11], [2, 5, 2], [3, 4, 6], [4, 5, 9]] },
    detour: { n: 5, pos: [[36, 112], [128, 52], [128, 172], [218, 112], [290, 112]],
      edges: [[0, 1, 10], [0, 2, 3], [2, 1, 4], [1, 3, 2], [2, 3, 8], [3, 4, 7]] }
  };
  function randomGraph(rnd) {
    rnd = rnd || Math.random;
    var n = 6, pos = PRESETS.classic.pos, edges = [], have = {};
    function add(a, b) { var k = Math.min(a, b) + "-" + Math.max(a, b); if (a === b || have[k]) return false; have[k] = 1; edges.push([a, b, 1 + Math.floor(rnd() * 9)]); return true; }
    for (var i = 1; i < n; i++) add(i, Math.floor(rnd() * i));
    for (var t = 0, extra = 2 + Math.floor(rnd() * 3); t < 40 && extra > 0; t++) if (add(Math.floor(rnd() * n), Math.floor(rnd() * n))) extra--;
    return { n: n, pos: pos, edges: edges };
  }
  function adjOf(P) { var g = []; for (var i = 0; i < P.n; i++) g.push([]); P.edges.forEach(function (e) { g[e[0]].push({ to: e[1], w: e[2] }); g[e[1]].push({ to: e[0], w: e[2] }); }); return g; }
  var inf = function (d) { return d >= INF ? "∞" : d; };
  function run(P, src) {
    if (!(Number.isInteger(src) && src >= 0 && src < P.n)) return { error: "起點請輸入 0 到 " + (P.n - 1) + " 的整數。" };
    var g = adjOf(P), n = P.n, dist = new Array(n).fill(INF), prev = new Array(n).fill(-1), done = {}, pq = [], fr = [], st = { upd: 0, pops: 0 };
    function snap(line, msg, o) {
      o = o || {};
      var nodes = P.pos.map(function (p, i) { return { x: p[0], y: p[1], t: String(i), sub: dist[i] >= INF ? "∞" : dist[i], cls: o.cur === i ? "cur" : o.upd === i ? "new" : done[i] ? "ok" : "" }; });
      var edges = P.edges.map(function (e, j) { var onTree = prev[e[1]] === e[0] || prev[e[0]] === e[1]; return { a: e[0], b: e[1], w: e[2], cls: o.edge === j ? "cur" : onTree ? "ok" : "" }; });
      var sorted = pq.slice().sort(function (a, b) { return a[0] - b[0] || a[1] - b[1]; });
      fr.push({ g: { W: 320, H: 214, nodes: nodes, edges: edges },
        dist: dist.map(function (d, i) { return { v: inf(d), cls: o.upd === i ? "new" : o.cur === i ? "cur" : done[i] ? "ok" : "" }; }),
        prev: prev.map(function (p, i) { return { v: p < 0 ? "-" : p, cls: o.upd === i ? "new" : "" }; }),
        pq: sorted.map(function (x, i) { return { v: x[0] + "," + x[1], cls: i === 0 ? "new" : "" }; }),
        chips: [["已確定", Object.keys(done).length + "/" + n], ["pq 大小", pq.length], ["更新次數", st.upd]], line: line, msg: msg });
    }
    dist[src] = 0; pq.push([0, src]);
    snap([11, 15], "<code>dist</code> 全部設成 ∞(還沒走到),起點 <b>" + src + "</b> 設成 0,把 <code>(0, " + src + ")</code> 放進優先佇列。pq 每次會先給出「距離最小」的那一筆。", { cur: src });
    while (pq.length) {
      var bi = 0; for (var i = 1; i < pq.length; i++) if (pq[i][0] < pq[bi][0] || (pq[i][0] === pq[bi][0] && pq[i][1] < pq[bi][1])) bi = i;
      var top = pq.splice(bi, 1)[0], d = top[0], u = top[1]; st.pops++;
      if (d > dist[u]) {
        snap([21, 23], "取出 <code>(" + d + ", " + u + ")</code>:但 <code>dist[" + u + "]</code> 已經是 " + dist[u] + " 了,這是<b>過時的舊紀錄</b>(後來找到更短的路),直接丟掉。", { cur: u });
        continue;
      }
      done[u] = true;
      snap([17, 18], "取出 <code>(" + d + ", " + u + ")</code>:pq 裡距離最小的。點 <b>" + u + "</b> 的最短距離就是 <b>" + d + "</b>,<b>確定了</b>(之後不會再變短)。", { cur: u });
      g[u].forEach(function (e) {
        var j = -1; P.edges.forEach(function (x, k) { if ((x[0] === u && x[1] === e.to) || (x[1] === u && x[0] === e.to)) j = k; });
        if (d + e.w < dist[e.to]) {
          var old = dist[e.to]; dist[e.to] = d + e.w; prev[e.to] = u; pq.push([dist[e.to], e.to]); st.upd++;
          snap([24, 28], "看邊 " + u + "→" + e.to + "(權重 " + e.w + "):<code>" + d + " + " + e.w + " = " + (d + e.w) + "</code> 比 <code>dist[" + e.to + "]</code> = " + inf(old) + " <b>更短</b>,更新(<b>鬆弛</b>成功),記下從 " + u + " 來,並放進 pq。", { cur: u, edge: j, upd: e.to });
        } else {
          snap([24, 25], "看邊 " + u + "→" + e.to + "(權重 " + e.w + "):<code>" + d + " + " + e.w + " = " + (d + e.w) + "</code>,沒有比 <code>dist[" + e.to + "]</code> = " + inf(dist[e.to]) + " 更短,不更新。", { cur: u, edge: j });
        }
      });
    }
    snap(undefined, "pq 空了,結束。<b>綠色的邊</b>是每個點「最短路上最後走的那一條」(<code>prev</code>),合起來就是最短路徑樹。點上方的數字是起點到它的最短距離。", {});
    return { frames: fr, dist: dist, prev: prev, pops: st.pops };
  }
  function idle() {
    var P = PRESETS.classic;
    return { g: { W: 320, H: 214, nodes: P.pos.map(function (p, i) { return { x: p[0], y: p[1], t: String(i), sub: "?" }; }), edges: P.edges.map(function (e) { return { a: e[0], b: e[1], w: e[2] }; }) },
      dist: [], prev: [], pq: [], chips: [], msg: "選一張圖和起點,按「執行」。邊上的數字是權重(路有多長)。" };
  }
  A.dijk = { CODE_DIJK: CODE_DIJK, INF: INF, PRESETS: PRESETS, randomGraph: randomGraph, run: run, idle: idle };
  if (typeof module !== "undefined" && module.exports) module.exports = A;
})(typeof window !== "undefined" ? window : globalThis);
