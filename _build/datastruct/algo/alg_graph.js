(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var CODE_MAZE = "struct Point {\n    int r;\n    int c;\n};\n\nstruct Step {\n    Point p;\n    int steps;\n};\n\nconst int DR[4] = {-1, 1, 0, 0};\nconst int DC[4] = {0, 0, -1, 1};\n\nbool isOpen(const std::vector<std::string>& g, int r, int c) {\n    return r >= 0 && r < static_cast<int>(g.size()) && c >= 0 && c < static_cast<int>(g[0].size()) && g[r][c] != '#';\n}\n\nint bfs(const std::vector<std::string>& g, Point s, Point t) {\n    std::vector<std::vector<int>> dist(g.size(), std::vector<int>(g[0].size(), -1));\n    std::queue<Point> q;\n    dist[s.r][s.c] = 0;\n    q.push(s);\n    while (!q.empty()) {\n        Point cur = q.front();\n        q.pop();\n        if (cur.r == t.r && cur.c == t.c) {\n            return dist[cur.r][cur.c];\n        }\n        for (int d = 0; d < 4; ++d) {\n            int nr = cur.r + DR[d];\n            int nc = cur.c + DC[d];\n            if (isOpen(g, nr, nc) && dist[nr][nc] == -1) {\n                dist[nr][nc] = dist[cur.r][cur.c] + 1;\n                q.push({nr, nc});\n            }\n        }\n    }\n    return -1;\n}\n\nint dfs(const std::vector<std::string>& g, Point s, Point t) {\n    std::vector<std::vector<bool>> seen(g.size(), std::vector<bool>(g[0].size(), false));\n    std::stack<Step> st;\n    st.push({s, 0});\n    while (!st.empty()) {\n        Step cur = st.top();\n        st.pop();\n        if (seen[cur.p.r][cur.p.c]) {\n            continue;\n        }\n        seen[cur.p.r][cur.p.c] = true;\n        if (cur.p.r == t.r && cur.p.c == t.c) {\n            return cur.steps;\n        }\n        for (int d = 0; d < 4; ++d) {\n            int nr = cur.p.r + DR[d];\n            int nc = cur.p.c + DC[d];\n            if (isOpen(g, nr, nc) && !seen[nr][nc]) {\n                st.push({{nr, nc}, cur.steps + 1});\n            }\n        }\n    }\n    return -1;\n}";
  var CODE_REPR = "using Table = std::vector<std::vector<int>>;\n\nvoid addEdge(Table& matrix, Table& adj, int a, int b) {\n    matrix[a][b] = 1;\n    matrix[b][a] = 1;\n    adj[a].push_back(b);\n    adj[b].push_back(a);\n}";
  var DR = [-1, 1, 0, 0], DC = [0, 0, -1, 1];
  var MAZES = {
    open: ["S......", ".......", ".......", ".......", "......G"],
    walls: ["S....##", ".##....", ".#.....", "#..##..", "......G"],
    noexit: ["S.#....", ".#.###.", ".#...#.", ".###.#.", "....#.G"]
  };
  function parseMaze(rows) {
    var M = { R: rows.length, C: rows[0].length, wall: [], S: null, G: null };
    for (var r = 0; r < M.R; r++) { M.wall.push([]); for (var c = 0; c < M.C; c++) { var ch = rows[r][c]; M.wall[r].push(ch === "#"); if (ch === "S") M.S = [r, c]; if (ch === "G") M.G = [r, c]; } }
    return M;
  }
  function isOpen(M, r, c) { return r >= 0 && r < M.R && c >= 0 && c < M.C && !M.wall[r][c]; }
  function randomMaze(rnd) {
    rnd = rnd || Math.random;
    for (var t = 0; t < 300; t++) {
      var rows = [];
      for (var r = 0; r < 5; r++) { var s = ""; for (var c = 0; c < 7; c++) s += (r === 0 && c === 0) ? "S" : (r === 4 && c === 6) ? "G" : (rnd() < 0.3 ? "#" : "."); rows.push(s); }
      if (searchPlain("bfs", parseMaze(rows)).steps > 0) return rows;
    }
    return MAZES.walls.slice();
  }
  function key(r, c) { return r + "," + c; }
  /* 沒有 frame 的版本,給測試與隨機迷宮用 */
  function searchPlain(mode, M) {
    var seen = {}, n = 0;
    if (mode === "bfs") {
      var dist = {}, q = [M.S]; dist[key(M.S[0], M.S[1])] = 0;
      while (q.length) { var cur = q.shift(); n++; var dc = dist[key(cur[0], cur[1])]; if (cur[0] === M.G[0] && cur[1] === M.G[1]) return { steps: dc, visited: n };
        for (var d = 0; d < 4; d++) { var nr = cur[0] + DR[d], nc = cur[1] + DC[d]; if (isOpen(M, nr, nc) && dist[key(nr, nc)] === undefined) { dist[key(nr, nc)] = dc + 1; q.push([nr, nc]); } } }
      return { steps: -1, visited: n };
    }
    var st = [{ r: M.S[0], c: M.S[1], s: 0 }];
    while (st.length) { var t = st.pop(); if (seen[key(t.r, t.c)]) continue; seen[key(t.r, t.c)] = true; n++; if (t.r === M.G[0] && t.c === M.G[1]) return { steps: t.s, visited: n };
      for (var e = 0; e < 4; e++) { var a = t.r + DR[e], b = t.c + DC[e]; if (isOpen(M, a, b) && !seen[key(a, b)]) st.push({ r: a, c: b, s: t.s + 1 }); } }
    return { steps: -1, visited: n };
  }
  function pt(p) { return p[0] + "," + p[1]; }
  function gridRun(mode, rows) {
    var M = parseMaze(rows), isB = mode === "bfs", fr = [];
    var seen = {}, txt = {}, queue = [], steps = {}, order = 0, cur = null;
    function frame(line, msg, extraCls, chips) {
      var cls = {};
      queue.forEach(function (e) { var k = key(e.r, e.c); if (!seen[k]) cls[k] = "fr"; });
      Object.keys(seen).forEach(function (k) { cls[k] = "seen"; });
      if (cur) cls[key(cur[0], cur[1])] = "cur";
      var items = queue.map(function (e) { return { v: e.r + "," + e.c, cls: "" }; });
      if (items.length) items[isB ? 0 : items.length - 1].cls = "new";
      fr.push({ grid: { R: M.R, C: M.C, wall: M.wall, cls: cls, txt: Object.assign({}, txt), S: M.S, G: M.G },
        list: { label: isB ? "queue(左邊先出去,格子是 行,列)" : "stack(右邊是 top,先出去,格子是 行,列)", items: items }, chips: chips, line: line, msg: msg });
    }
    function chipsNow(extra) { return [[isB ? "已處理" : "已走訪", Object.keys(seen).length], [isB ? "queue 大小" : "stack 大小", queue.length]].concat(extra || []); }
    var S0 = { r: M.S[0], c: M.S[1], s: 0 };
    queue.push(S0); if (isB) txt[key(S0.r, S0.c)] = 0;
    frame(isB ? [21, 22] : 44, isB ? "起點距離設成 0,放進 queue。BFS 用 <b>queue</b>:先放進去的先處理,所以會<b>一圈一圈</b>往外擴。" : "起點放進 stack。DFS 用 <b>stack</b>:最後放進去的先處理,所以會<b>一直往前鑽</b>,走不通才退回來。", {}, chipsNow());
    while (queue.length) {
      var e = isB ? queue.shift() : queue.pop();
      var k = key(e.r, e.c);
      if (!isB && seen[k]) {
        cur = [e.r, e.c]; var save = seen[k]; delete seen[k];
        frame([46, 49], "取出 (" + k + "):這格已經走過了(同一格可能被不同的路重複放進 stack),直接丟掉。", {}, chipsNow());
        seen[k] = save; cur = null; continue;
      }
      seen[k] = true; cur = [e.r, e.c];
      if (!isB) { order++; txt[k] = order; }
      var here = isB ? txt[k] : e.s;
      if (e.r === M.G[0] && e.c === M.G[1]) {
        var res = isB ? "最短步數 = <b>" + here + "</b>。" : "這次走到的路是 <b>" + here + "</b> 步(不一定是最短)。";
        frame(isB ? [24, 27] : [46, 53], "取出 (" + k + ") 就是<b>終點</b>,<code>return</code>。" + res, {}, chipsNow([[isB ? "最短步數" : "這條路的步數", here]]));
        return { frames: fr, steps: here, visited: Object.keys(seen).length };
      }
      frame(isB ? [24, 25] : [46, 51], isB ? "取出 queue 最前面的 (" + k + "),它的距離是 " + here + "。" : "取出 stack 最上面的 (" + k + "),還沒走過,標記為第 <b>" + order + "</b> 個走訪(從起點走了 " + e.s + " 步)。", {}, chipsNow());
      var added = [];
      for (var d = 0; d < 4; d++) {
        var nr = e.r + DR[d], nc = e.c + DC[d], nk = key(nr, nc);
        if (!isOpen(M, nr, nc)) continue;
        if (isB) { if (txt[nk] === undefined) { txt[nk] = here + 1; queue.push({ r: nr, c: nc, s: here + 1 }); added.push(nk); } }
        else if (!seen[nk]) { queue.push({ r: nr, c: nc, s: e.s + 1 }); added.push(nk); }
      }
      var lst = added.map(function (x) { return "(" + x + ")"; }).join(" "), em;
      if (added.length) em = "依序看上、下、左、右,把" + (isB ? "還沒到過的空格放進 queue:" + lst + "。距離都是 " + (here + 1) + "。" : "還沒走過的空格放進 stack:" + lst + "。最後放進去的 (" + added[added.length - 1] + ") 會最先被取出。");
      else em = "依序看上、下、左、右,沒有可以放進去的格子" + (isB ? "。" : ",下一步會退回 stack 裡更早放進去的格子。");
      frame(isB ? [29, 34] : [55, 59], em, {}, chipsNow());
    }
    cur = null;
    frame(isB ? 38 : 63, (isB ? "queue" : "stack") + " 空了,還是沒走到終點:<b>這個迷宮沒有出口</b>(<code>return -1</code>)。", {}, chipsNow([["結果", -1]]));
    return { frames: fr, steps: -1, visited: Object.keys(seen).length };
  }
  function idleMaze() {
    var M = parseMaze(MAZES.walls);
    return { grid: { R: M.R, C: M.C, wall: M.wall, cls: {}, txt: {}, S: M.S, G: M.G }, list: { label: "", items: [] }, chips: [], msg: "選演算法與迷宮,按「執行」。S 是起點,G 是終點。" };
  }

  /* ---- 圖的表示:一條邊一條邊加進去 ---- */
  function parseEdges(str) {
    var toks = String(str).split(/[\s,;]+/).filter(Boolean);
    if (!toks.length) return { error: "請輸入至少一條邊,例如 0-1 0-2 1-3。" };
    var edges = [], seen = {}, n = 0;
    for (var i = 0; i < toks.length; i++) {
      var m = /^(\d)-(\d)$/.exec(toks[i]);
      if (!m) return { error: "「" + toks[i] + "」格式不對,請寫成 0-1(兩個 0~6 的數字,中間一個減號)。" };
      var a = +m[1], b = +m[2];
      if (a > 6 || b > 6) return { error: "點的編號只能是 0 到 6。" };
      if (a === b) return { error: "「" + toks[i] + "」是自己連到自己,這裡不放自環。" };
      var kk = Math.min(a, b) + "-" + Math.max(a, b);
      if (seen[kk]) return { error: "邊 " + kk + " 重複了(無向圖:" + a + "-" + b + " 和 " + b + "-" + a + " 是同一條)。" };
      seen[kk] = 1; edges.push([a, b]); n = Math.max(n, a + 1, b + 1);
    }
    if (edges.length > 9) return { error: "最多 9 條邊。" };
    return { n: Math.max(n, 2), edges: edges };
  }
  function layout(n) {
    var nodes = [], W = 240, H = 210, cx = 120, cy = 105, R = 80;
    for (var i = 0; i < n; i++) { var ang = -Math.PI / 2 + 2 * Math.PI * i / n; nodes.push({ x: Math.round(cx + R * Math.cos(ang)), y: Math.round(cy + R * Math.sin(ang)), t: String(i), cls: "" }); }
    return { W: W, H: H, nodes: nodes };
  }
  function reprRun(str) {
    var p = parseEdges(str); if (p.error) return { error: p.error };
    var n = p.n, m = [], adj = [], fr = [], shown = [], L = layout(n);
    for (var i = 0; i < n; i++) { m.push(new Array(n).fill(0)); adj.push([]); }
    function items() { var c = 0; adj.forEach(function (l) { c += l.length; }); return c; }
    function frame(line, msg, hlM, hlA, curEdge, curNodes) {
      var nodes = L.nodes.map(function (x, i) { return { x: x.x, y: x.y, t: x.t, cls: curNodes && curNodes.indexOf(i) >= 0 ? "cur" : "" }; });
      fr.push({ g: { W: L.W, H: L.H, nodes: nodes, edges: shown.map(function (e, j) { return { a: e[0], b: e[1], cls: curEdge === j ? "cur" : "" }; }) },
        matrix: { n: n, m: m.map(function (r) { return r.slice(); }), hl: hlM || [] }, adj: { n: n, adj: adj.map(function (l) { return l.slice(); }), hl: hlA || [] },
        chips: [["點", n], ["邊", shown.length], ["矩陣格數", n * n], ["表格項目", items()]], line: line, msg: msg });
    }
    frame(undefined, n + " 個點、還沒有邊:矩陣全是 0,每個點的 list 都是空的。接下來一條邊一條邊加(無向圖:<b>兩個方向都要記</b>)。");
    p.edges.forEach(function (e, j) {
      var a = e[0], b = e[1]; shown.push(e);
      m[a][b] = 1; frame(4, "加邊 " + a + "-" + b + ":<code>matrix[" + a + "][" + b + "] = 1</code>,矩陣第 " + a + " 列第 " + b + " 行設成 1。", [[a, b]], [], j, [a, b]);
      m[b][a] = 1; frame(5, "無向圖要對稱:<code>matrix[" + b + "][" + a + "] = 1</code>。", [[a, b], [b, a]], [], j, [a, b]);
      adj[a].push(b); frame(6, "鄰接表:<code>adj[" + a + "].push_back(" + b + ")</code>,在 " + a + " 的 list 後面接上 " + b + "。", [], [[a, adj[a].length - 1]], j, [a, b]);
      adj[b].push(a); frame(7, "<code>adj[" + b + "].push_back(" + a + ")</code>。這條邊加完了。", [], [[a, adj[a].length - 1], [b, adj[b].length - 1]], j, [a, b]);
    });
    frame(undefined, "完成:" + shown.length + " 條邊。矩陣用了 " + n * n + " 格(不管有幾條邊),鄰接表只用 " + items() + " 個項目(每條邊 2 個)。邊很少的圖,鄰接表省很多空間。");
    return { frames: fr, n: n, edges: p.edges, matrix: m, adj: adj };
  }
  A.graph = { CODE_MAZE: CODE_MAZE, CODE_REPR: CODE_REPR, MAZES: MAZES, parseMaze: parseMaze, randomMaze: randomMaze, searchPlain: searchPlain, gridRun: gridRun, idleMaze: idleMaze,
    parseEdges: parseEdges, reprRun: reprRun, layout: layout };
  if (typeof module !== "undefined" && module.exports) module.exports = A;
})(typeof window !== "undefined" ? window : globalThis);
