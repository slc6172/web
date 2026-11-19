(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var CODE_TREE = [
    "struct TreeNode {", "    int val;", "    TreeNode* left;", "    TreeNode* right;", "};", "",
    "void preorder(const TreeNode* node) {", "    if (node == nullptr) {", "        return;", "    }", "    std::cout << node->val << \" \";", "    preorder(node->left);", "    preorder(node->right);", "}", "",
    "void inorder(const TreeNode* node) {", "    if (node == nullptr) {", "        return;", "    }", "    inorder(node->left);", "    std::cout << node->val << \" \";", "    inorder(node->right);", "}", "",
    "void postorder(const TreeNode* node) {", "    if (node == nullptr) {", "        return;", "    }", "    postorder(node->left);", "    postorder(node->right);", "    std::cout << node->val << \" \";", "}", "",
    "void levelOrder(const TreeNode* root) {", "    if (root == nullptr) {", "        return;", "    }", "    std::queue<const TreeNode*> q;", "    q.push(root);", "    while (!q.empty()) {",
    "        const TreeNode* node = q.front();", "        q.pop();", "        std::cout << node->val << \" \";", "        if (node->left != nullptr) {", "            q.push(node->left);", "        }",
    "        if (node->right != nullptr) {", "            q.push(node->right);", "        }", "    }", "}"].join("\n");
  var L = { pre: { fn: "preorder", enter: [7, 8], nul: [8, 9], print: 11, left: 12, right: 13 }, in: { fn: "inorder", enter: [16, 17], nul: [17, 18], left: 20, print: 21, right: 22 },
    post: { fn: "postorder", enter: [25, 26], nul: [26, 27], left: 29, right: 30, print: 31 } };
  var NAMES = { pre: "前序 preorder(根 → 左 → 右)", in: "中序 inorder(左 → 根 → 右)", post: "後序 postorder(左 → 右 → 根)", level: "層序 levelOrder(一層一層,由左到右)" };
  function nd(v, l, r) { return { v: v, l: l || null, r: r || null }; }
  var PRESETS = {
    full: { name: "完全二元樹(7 個節點)", tree: nd(1, nd(2, nd(4), nd(5)), nd(3, nd(6), nd(7))) },
    irregular: { name: "不規則(7 個節點)", tree: nd(1, nd(2, nd(4), nd(5, nd(7), null)), nd(3, null, nd(6))) },
    chain: { name: "鏈狀(4 個節點,最不平衡)", tree: nd(1, null, nd(2, null, nd(3, null, nd(4)))) }
  };
  function build(t) {
    var nodes = {}, root = null;
    (function go(x) { if (!x) return null; var id = "n" + x.v; nodes[id] = { v: x.v, l: go(x.l), r: go(x.r) }; return id; })(t);
    root = t ? "n" + t.v : null; return { root: root, nodes: nodes };
  }
  function expected(mode, t) {
    var out = [];
    if (mode === "level") { var q = [t]; while (q.length) { var x = q.shift(); out.push(x.v); if (x.l) q.push(x.l); if (x.r) q.push(x.r); } return out; }
    (function go(x) { if (!x) return; if (mode === "pre") out.push(x.v); go(x.l); if (mode === "in") out.push(x.v); go(x.r); if (mode === "post") out.push(x.v); })(t); return out;
  }
  function run(mode, key) {
    var P = PRESETS[key]; if (!P) return { error: "請選一棵樹。" }; if (!NAMES[mode]) return { error: "請選一種走訪。" };
    var T = build(P.tree), vis = {}, out = [], stack = [], q = [], inq = {}, fr = [];
    function snap(line, msg, cur) {
      var tn = {}; Object.keys(T.nodes).forEach(function (id) { var n = T.nodes[id]; tn[id] = { label: n.v, l: n.l, r: n.r, cls: id === cur ? "cur" : vis[id] ? "ok" : inq[id] ? "new" : "" }; });
      var f = { tree: { root: T.root, nodes: tn }, out: out.slice(), line: line, msg: msg };
      if (mode === "level") { f.queue = q.map(function (id) { return T.nodes[id].v; }); f.chips = [["已印出", out.length], ["queue 大小", q.length]]; }
      else { f.stack = stack.map(function (id) { return Ls.fn + "(" + T.nodes[id].v + ")"; }); f.chips = [["已印出", out.length], ["目前深度", stack.length]]; }
      fr.push(f);
    }
    var Ls = L[mode] || {};
    function print(id) { vis[id] = true; out.push(T.nodes[id].v); snap(Ls.print, "<code>cout &lt;&lt; node-&gt;val</code>:印出 <b>" + T.nodes[id].v + "</b>。" + (mode === "pre" ? "前序:先處理自己。" : mode === "in" ? "中序:左邊走完了,輪到自己。" : "後序:左右都走完了,最後才處理自己。"), id); }
    function child(id, c, side, lineAfter) {
      if (c === null) { snap(Ls.nul, "節點 " + T.nodes[id].v + " 的" + (side === "left" ? "左" : "右") + "邊是 nullptr:<code>" + Ls.fn + "(nullptr)</code> 馬上返回。", id); return; }
      visit(c);
      snap(lineAfter, (side === "left" ? "左" : "右") + "子樹都走完了,回到節點 <b>" + T.nodes[id].v + "</b>。", id);
    }
    function visit(id) {
      var n = T.nodes[id]; stack.push(id); snap(Ls.enter, "進入 <code>" + Ls.fn + "</code>:目前的節點是 <b>" + n.v + "</b>(不是 nullptr)。", id);
      if (mode === "pre") print(id);
      child(id, n.l, "left", Ls.left); if (mode === "in") print(id);
      child(id, n.r, "right", Ls.right); if (mode === "post") print(id);
      stack.pop();
    }
    if (mode === "level") {
      q.push(T.root); inq[T.root] = true; snap([34, 39], "層序走訪:用 <b>queue</b>(第 5 篇)。先把根節點放進去。", null);
      while (q.length) {
        var id = q.shift(); delete inq[id]; var n = T.nodes[id];
        snap([41, 42], "<code>q.front()</code> 然後 <code>q.pop()</code>:取出最前面的節點 <b>" + n.v + "</b>。", id);
        vis[id] = true; out.push(n.v); snap(43, "印出 <b>" + n.v + "</b>。", id);
        if (n.l) { q.push(n.l); inq[n.l] = true; snap([44, 45], "有左子節點 " + T.nodes[n.l].v + ",放進 queue 的最後面(排隊等著)。", id); }
        if (n.r) { q.push(n.r); inq[n.r] = true; snap([47, 48], "有右子節點 " + T.nodes[n.r].v + ",放進 queue 的最後面。", id); }
      }
      snap(50, "queue 空了,走完了。同一層的節點是一起排隊、一起處理的,所以是<b>一層一層</b>印。", null);
    } else {
      visit(T.root); snap(Ls.right, "最外層返回,走完了。", null);
    }
    fr[fr.length - 1].msg += "輸出順序:<b>" + out.join(" ") + "</b>。";
    return { frames: fr, result: null, out: out };
  }
  function idle(key) {
    var P = PRESETS[key] || PRESETS.full, T = build(P.tree), tn = {};
    Object.keys(T.nodes).forEach(function (id) { var n = T.nodes[id]; tn[id] = { label: n.v, l: n.l, r: n.r, cls: "" }; });
    return { tree: { root: T.root, nodes: tn }, out: [], chips: [["節點數", Object.keys(T.nodes).length]] };
  }
  A.tree = { idle: idle, CODE_TREE: CODE_TREE, PRESETS: PRESETS, NAMES: NAMES, run: run, expected: expected, nd: nd, build: build };
  if (typeof module !== "undefined" && module.exports) module.exports = A;
})(typeof window !== "undefined" ? window : globalThis);
