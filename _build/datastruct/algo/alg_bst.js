(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var CODE_BST = "struct TreeNode {\n    int val;\n    TreeNode* left;\n    TreeNode* right;\n};\n\nTreeNode* insert(TreeNode* node, int val) {\n    if (node == nullptr) {\n        return new TreeNode{val, nullptr, nullptr};\n    }\n    if (val < node->val) {\n        node->left = insert(node->left, val);\n    } else if (val > node->val) {\n        node->right = insert(node->right, val);\n    }\n    return node;\n}\n\nbool search(const TreeNode* node, int val) {\n    if (node == nullptr) {\n        return false;\n    }\n    if (val == node->val) {\n        return true;\n    }\n    if (val < node->val) {\n        return search(node->left, val);\n    }\n    return search(node->right, val);\n}\n\nTreeNode* minNode(TreeNode* node) {\n    while (node->left != nullptr) {\n        node = node->left;\n    }\n    return node;\n}\n\nTreeNode* erase(TreeNode* node, int val) {\n    if (node == nullptr) {\n        return nullptr;\n    }\n    if (val < node->val) {\n        node->left = erase(node->left, val);\n    } else if (val > node->val) {\n        node->right = erase(node->right, val);\n    } else {\n        if (node->left == nullptr) {\n            TreeNode* r = node->right;\n            delete node;\n            return r;\n        }\n        if (node->right == nullptr) {\n            TreeNode* l = node->left;\n            delete node;\n            return l;\n        }\n        TreeNode* succ = minNode(node->right);\n        node->val = succ->val;\n        node->right = erase(node->right, succ->val);\n    }\n    return node;\n}";
  var MAXN = 10, LO = 1, HI = 99;
  var NAMES = { insert: "insert 放入", search: "search 查詢", erase: "erase 刪除" };
  function mk(id, v) { return { id: id, v: v, l: null, r: null }; }
  function clone(n) { return n ? { id: n.id, v: n.v, l: clone(n.l), r: clone(n.r) } : null; }
  function count(n) { return n ? 1 + count(n.l) + count(n.r) : 0; }
  function height(n) { return n ? 1 + Math.max(height(n.l), height(n.r)) : 0; }
  function inorder(n, o) { o = o || []; if (n) { inorder(n.l, o); o.push(n.v); inorder(n.r, o); } return o; }
  function preorder(n, o) { o = o || []; if (n) { o.push(n.v); preorder(n.l, o); preorder(n.r, o); } return o; }
  /* 含 null 的前序,用來檢查「結構」完全相同 */
  function shape(n) { return n ? "(" + n.v + " " + shape(n.l) + " " + shape(n.r) + ")" : "."; }
  function init() { return { root: null, next: 1 }; }
  function has(n, v) { while (n) { if (v === n.v) return true; n = v < n.v ? n.l : n.r; } return false; }
  /* 靜默建樹(不出 frame):依序插入,重複的略過 */
  function fromList(list) {
    var b = init();
    list.forEach(function (v) {
      var node = mk("b" + b.next, v), cur = b.root, par = null;
      while (cur) { if (v === cur.v) return; par = cur; cur = v < cur.v ? cur.l : cur.r; }
      b.next++; if (par) { if (v < par.v) par.l = node; else par.r = node; } else b.root = node;
    });
    return b;
  }
  function toFrame(root, cls, line, msg, cmps) {
    var nodes = {};
    (function go(n) { if (!n) return; nodes[n.id] = { label: n.v, l: n.l ? n.l.id : null, r: n.r ? n.r.id : null, cls: cls[n.id] || "" }; go(n.l); go(n.r); })(root);
    return { tree: { root: root ? root.id : null, nodes: nodes, bst: true }, line: line, msg: msg,
      chips: [["節點數", count(root)], ["高度", height(root)], ["比較次數", cmps]] };
  }
  function idle(base) {
    var f = toFrame(base.root, {}, undefined, "", 0);
    f.msg = base.root ? "選一個操作、輸入 1~99 的數字,按「執行」。目前中序(由小到大)是:<b>" + inorder(base.root).join(" ") + "</b>。"
      : "樹是空的。先用「insert 放入」放幾個數字,或按「平衡範例」。";
    f.chips = f.chips.slice(0, 2); return f;
  }
  function run(op, val, base) {
    if (!NAMES[op]) return { error: "請選一個操作。" };
    if (!(Number.isInteger(val) && val >= LO && val <= HI)) return { error: "請輸入 " + LO + " 到 " + HI + " 的整數。" };
    var T = { root: clone(base.root) }, next = base.next, fr = [], path = {}, cmps = 0, n0 = count(T.root);
    function cls(extra) { var c = {}; Object.keys(path).forEach(function (k) { c[k] = "ok"; }); Object.keys(extra || {}).forEach(function (k) { c[k] = extra[k]; }); return c; }
    function snap(line, msg, extra) { fr.push(toFrame(T.root, cls(extra), line, msg, cmps)); }
    function X(id, c) { var o = {}; o[id] = c; return o; }
    function two(a, ac, b, bc) { var o = {}; o[a] = ac; o[b] = bc; return o; }
    var msgEnd = function () { return "中序(由小到大)是 <b>" + (inorder(T.root).join(" ") || "(空)") + "</b>。"; };

    if (op === "insert") {
      if (has(T.root, val)) return { error: val + " 已經在樹裡了。這份程式遇到相等的值什麼都不做(set 的規則:不放重複值)。" };
      if (n0 >= MAXN) return { error: "動畫最多放 " + MAXN + " 個節點,請先用 erase 刪掉一些,或按 Reset。" };
      var cur = T.root, par = null, side = null;
      snap(7, T.root ? "<code>insert(root, " + val + ")</code>:從根開始,一路比大小往下找位置。" : "樹是空的(<code>root == nullptr</code>),馬上就會走到 nullptr。", {});
      while (cur) {
        cmps++; path[cur.id] = true;
        if (val < cur.v) { snap([11, 12], "<b>" + val + "</b> &lt; " + cur.v + ":往<b>左</b>走(<code>node-&gt;left = insert(node-&gt;left, val)</code>)。", X(cur.id, "cur")); par = cur; side = "l"; cur = cur.l; }
        else { snap([13, 14], "<b>" + val + "</b> &gt; " + cur.v + ":往<b>右</b>走(<code>node-&gt;right = insert(node-&gt;right, val)</code>)。", X(cur.id, "cur")); par = cur; side = "r"; cur = cur.r; }
      }
      var nn = mk("b" + next, val); next++;
      if (par) par[side] = nn; else T.root = nn;
      snap([8, 9], "走到 <code>nullptr</code>:這裡就是 <b>" + val + "</b> 的位置。<code>new TreeNode{val, nullptr, nullptr}</code> 放在這裡。", X(nn.id, "new"));
      snap(16, "<code>return node</code>:一路回傳,其他節點都沒動。新節點永遠是<b>葉</b>。" + msgEnd(), X(nn.id, "new"));
      return { frames: fr, result: { root: T.root, next: next } };
    }

    if (op === "search") {
      var c = T.root, found = false;
      snap(19, T.root ? "<code>search(root, " + val + ")</code>:從根開始。" : "樹是空的,<code>search</code> 一開始就遇到 nullptr。", {});
      while (true) {
        if (!c) { snap([20, 21], "走到 <code>nullptr</code>:沒有路可走了,<code>return false</code>。<b>" + val + "</b> 不在這棵樹裡。", {}); break; }
        cmps++; path[c.id] = true;
        if (val === c.v) { snap([23, 24], "<b>" + val + "</b> == " + c.v + ":找到了,<code>return true</code>。一共比較了 <b>" + cmps + "</b> 次。", X(c.id, "new")); found = true; break; }
        if (val < c.v) { snap([26, 27], "<b>" + val + "</b> &lt; " + c.v + ":往<b>左</b>子樹找(<code>return search(node-&gt;left, val)</code>)。", X(c.id, "cur")); c = c.l; }
        else { snap(29, "<b>" + val + "</b> &gt; " + c.v + ":往<b>右</b>子樹找(<code>return search(node-&gt;right, val)</code>)。", X(c.id, "cur")); c = c.r; }
      }
      return { frames: fr, result: { root: T.root, next: next }, found: found };
    }

    /* erase:照 C++ 遞迴的順序出 frame */
    var twoTop = false;
    function er(node, v) {
      if (!node) { snap([40, 41], "走到 <code>nullptr</code>:這棵樹裡沒有 <b>" + v + "</b>,什麼都不用刪(<code>return nullptr</code>)。", {}); return null; }
      cmps++; path[node.id] = true;
      if (v < node.v) {
        snap([43, 44], "<b>" + v + "</b> &lt; " + node.v + ":要刪的在<b>左</b>子樹(<code>node-&gt;left = erase(node-&gt;left, val)</code>)。", X(node.id, "cur"));
        var oldL = node.l, rl = er(oldL, v);
        if (rl !== oldL) { node.l = rl; snap(44, "子樹的根換人了:<code>node-&gt;left</code> 重新接上回傳值。", X(node.id, "cur")); }
        return node;
      }
      if (v > node.v) {
        snap([45, 46], "<b>" + v + "</b> &gt; " + node.v + ":要刪的在<b>右</b>子樹(<code>node-&gt;right = erase(node-&gt;right, val)</code>)。", X(node.id, "cur"));
        var oldR = node.r, rr = er(oldR, v);
        if (rr !== oldR) { node.r = rr; snap(46, "子樹的根換人了:<code>node-&gt;right</code> 重新接上回傳值。", X(node.id, "cur")); }
        return node;
      }
      if (!node.l) {
        snap(47, "找到了:<b>" + node.v + "</b>。先看它有幾個子節點:<b>" + (node.r ? "只有右子節點" : "沒有子節點(葉)") + "</b>。", X(node.id, "del"));
        snap([48, 49], "<code>node-&gt;left == nullptr</code>:先把右子節點記成 <code>r</code>(" + (node.r ? "子樹的根是 " + node.r.v : "<code>nullptr</code>") + ")。", node.r ? two(node.id, "del", node.r.id, "new") : X(node.id, "del"));
        snap([50, 51], "<code>delete node</code>,然後 <code>return r</code>:讓 " + (node.r ? "<b>" + node.r.v + "</b> 的子樹頂替它的位置" : "這個位置變成空的") + "。", node.r ? two(node.id, "del", node.r.id, "new") : X(node.id, "del"));
        return node.r;
      }
      if (!node.r) {
        snap(47, "找到了:<b>" + node.v + "</b>。它<b>只有左子節點</b>。", X(node.id, "del"));
        snap([53, 54], "<code>node-&gt;right == nullptr</code>:先把左子節點記成 <code>l</code>(子樹的根是 " + node.l.v + ")。", two(node.id, "del", node.l.id, "new"));
        snap([55, 56], "<code>delete node</code>,然後 <code>return l</code>:讓 <b>" + node.l.v + "</b> 的子樹頂替它的位置。", two(node.id, "del", node.l.id, "new"));
        return node.l;
      }
      /* 兩個子節點 */
      twoTop = true;
      snap(47, "找到了:<b>" + node.v + "</b>。它有<b>左右兩個子節點</b>,不能直接拿掉,否則會斷成兩棵樹。", X(node.id, "cur"));
      var s = node.r;
      snap(58, "<code>succ = minNode(node-&gt;right)</code>:找<b>後繼</b>(比 " + node.v + " 大的值裡最小的)。從右子節點 " + s.v + " 開始。", two(node.id, "cur", s.id, "new"));
      while (s.l) { snap([33, 34], s.v + " 還有左子節點 " + s.l.v + ":往左走(右子樹裡越往左越小)。", two(node.id, "cur", s.id, "new")); s = s.l; }
      snap(36, s.v + " 沒有左子節點了:後繼就是 <b>" + s.v + "</b>(右子樹裡最小的值)。", two(node.id, "cur", s.id, "new"));
      var ov = node.v; node.v = s.v;
      snap(59, "<code>node-&gt;val = succ-&gt;val</code>:把後繼的值 <b>" + s.v + "</b> 抄過來,原本的 " + ov + " 被蓋掉。現在樹上有兩個 " + s.v + ",下一步把下面那個刪掉。", two(node.id, "cur", s.id, "del"));
      var sv = s.v;
      snap(60, "<code>node-&gt;right = erase(node-&gt;right, " + sv + ")</code>:在右子樹裡刪掉值 " + sv + "(後繼最多只有右子節點,屬於簡單的情況)。", two(node.id, "cur", s.id, "del"));
      var oldR2 = node.r, r2 = er(oldR2, sv);
      if (r2 !== oldR2) { node.r = r2; snap(60, "子樹的根換人了:<code>node-&gt;right</code> 重新接上回傳值。", X(node.id, "cur")); }
      return node;
    }
    snap(39, T.root ? "<code>erase(root, " + val + ")</code>:先照 search 的方式找到它。" : "樹是空的,<code>erase</code> 一開始就遇到 nullptr。", {});
    var oldRoot = T.root, nr = er(oldRoot, val);
    if (nr !== oldRoot) { T.root = nr; snap(undefined, "沒有上一層了:呼叫端的 <code>root = erase(root, val)</code> 接上回傳值,根換人了。", {}); }
    var removed = count(T.root) < n0;
    path = {};
    snap(twoTop ? 62 : undefined, (removed ? "完成,<b>" + val + "</b> 刪掉了。一共比較 <b>" + cmps + "</b> 次。" : "完成,樹沒有改變。") + msgEnd(), {});
    return { frames: fr, result: { root: T.root, next: next }, removed: removed };
  }
  A.bst = { CODE_BST: CODE_BST, NAMES: NAMES, MAXN: MAXN, LO: LO, HI: HI, init: init, fromList: fromList, run: run, idle: idle,
    inorder: function (b) { return inorder(b.root); }, preorder: function (b) { return preorder(b.root); }, shape: function (b) { return shape(b.root); },
    count: function (b) { return count(b.root); }, height: function (b) { return height(b.root); }, clone: function (b) { return { root: clone(b.root), next: b.next }; } };
  if (typeof module !== "undefined" && module.exports) module.exports = A;
})(typeof window !== "undefined" ? window : globalThis);
