(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var MAXN = 6;
  var CODE_LIST = [
    "struct Node {", "    int val;", "    Node* next;", "};", "", "struct List {", "    Node* head = nullptr;", "};", "",
    "void pushFront(List& list, int value) {", "    Node* node = new Node{value, list.head};", "    list.head = node;", "}", "",
    "void pushBack(List& list, int value) {", "    Node* node = new Node{value, nullptr};", "    if (list.head == nullptr) {", "        list.head = node;", "        return;", "    }",
    "    Node* cur = list.head;", "    while (cur->next != nullptr) {", "        cur = cur->next;", "    }", "    cur->next = node;", "}", "",
    "void insertAfter(Node* prev, int value) {", "    Node* node = new Node{value, prev->next};", "    prev->next = node;", "}", "",
    "void eraseFront(List& list) {", "    Node* old = list.head;", "    list.head = old->next;", "    delete old;", "}", "",
    "void eraseAfter(Node* prev) {", "    Node* old = prev->next;", "    prev->next = old->next;", "    delete old;", "}"].join("\n");
  function isInt(x) { return typeof x === "number" && isFinite(x) && Math.floor(x) === x; }

  function build(vals) {
    var S = { nodes: {}, head: null, tags: {}, hint: {}, cls: {}, hot: {}, writes: 0, visits: 0 };
    vals.forEach(function (v, i) { S.nodes["n" + i] = { v: v, next: i + 1 < vals.length ? "n" + (i + 1) : null }; });
    S.head = vals.length ? "n0" : null; return S;
  }
  function chain(S) { var out = [], id = S.head, seen = {}; while (id && !seen[id]) { seen[id] = 1; out.push(id); id = S.nodes[id].next; } return out; }
  function values(S) { return chain(S).map(function (id) { return S.nodes[id].v; }); }
  function snap(S, line, msg) {
    var ch = chain(S), pos = {}; ch.forEach(function (id, i) { pos[id] = { slot: i, row: 0 }; });
    var nodes = Object.keys(S.nodes).map(function (k) {
      var p = pos[k] || S.hint[k] || { slot: ch.length, row: 1 };
      return { id: k, v: S.nodes[k].v, next: S.nodes[k].next, slot: p.slot, row: p.row, cls: S.cls[k] || "", hot: !!S.hot[k] };
    });
    var tags = []; Object.keys(S.tags).forEach(function (nm) { if (S.tags[nm]) tags.push({ name: nm, at: S.tags[nm] }); });
    if (S.head) tags.push({ name: "head", at: S.head });
    return { nodes: nodes, tags: tags, headNull: S.head === null, chips: [["長度", ch.length], ["改了幾個指標", S.writes], ["走訪節點數", S.visits]], line: line, msg: msg };
  }
  function reset(S) { S.cls = {}; S.hot = {}; }

  function pushFront(vals, v) {
    if (vals.length >= MAXN) return { error: "示範最多 " + MAXN + " 個節點,請先刪除幾個或按 Reset。" };
    if (!isInt(v) || v < 0 || v > 99) return { error: "數值請輸入 0 到 99 的整數。" };
    var S = build(vals), fr = [];
    fr.push(snap(S, 10, "<code>pushFront(list, " + v + ")</code>:要把 " + v + " 放到最前面。"));
    S.nodes.nw = { v: v, next: S.head }; S.hint.nw = { slot: 0, row: 1 }; S.tags.node = "nw"; S.cls.nw = "new"; S.hot.nw = true;
    fr.push(snap(S, 11, "<code>new Node{value, list.head}</code>:做出新節點,它的 next 直接指向目前的第一個節點" + (vals.length ? "" : "(空串列就是 null)") + "。"));
    reset(S); S.head = "nw"; S.writes++; S.writes++; S.tags = {}; S.cls.nw = "new";
    fr.push(snap(S, 12, "<code>list.head = node</code>:head 改指向新節點,完成。只動了 2 個指標,和串列多長無關,是 <b>O(1)</b>。"));
    return { frames: fr, result: values(S) };
  }
  function pushBack(vals, v) {
    if (vals.length >= MAXN) return { error: "示範最多 " + MAXN + " 個節點,請先刪除幾個或按 Reset。" };
    if (!isInt(v) || v < 0 || v > 99) return { error: "數值請輸入 0 到 99 的整數。" };
    var S = build(vals), fr = [], n = vals.length;
    fr.push(snap(S, 15, "<code>pushBack(list, " + v + ")</code>:要接在最後面。串列只記得 head,沒有直接指向最後一個節點的指標。"));
    S.nodes.nw = { v: v, next: null }; S.hint.nw = { slot: n, row: 1 }; S.tags.node = "nw"; S.cls.nw = "new";
    if (n === 0) {
      fr.push(snap(S, [16, 17], "<code>new Node{value, nullptr}</code>:做出新節點。<code>list.head == nullptr</code> 成立,代表是空串列。"));
      reset(S); S.head = "nw"; S.writes++; S.tags = {}; S.cls.nw = "new";
      fr.push(snap(S, [18, 19], "空串列:<code>list.head = node</code>,直接結束(走訪 0 個節點)。"));
      return { frames: fr, result: values(S) };
    }
    fr.push(snap(S, [16, 17], "<code>new Node{value, nullptr}</code>:做出新節點。head 不是 nullptr,串列不是空的,要走到最後一個節點。"));
    reset(S); S.tags = { cur: S.head }; S.visits = 1;
    fr.push(snap(S, 21, "<code>Node* cur = list.head;</code>:cur 從第一個節點出發(走訪 1 個)。"));
    var id = S.head;
    while (S.nodes[id].next) {
      id = S.nodes[id].next; S.tags = { cur: id }; S.visits++; S.cls = {}; S.cls[id] = "cur";
      fr.push(snap(S, [22, 23], "<code>cur-&gt;next</code> 不是 nullptr,<code>cur = cur-&gt;next</code>:往下走一個節點(已走訪 " + S.visits + " 個)。"));
    }
    S.cls = {}; S.nodes[id].next = "nw"; S.hot[id] = true; S.writes++; S.tags = { cur: id }; S.cls.nw = "new";
    fr.push(snap(S, 25, "<code>cur-&gt;next</code> 是 nullptr,cur 就是最後一個節點。<code>cur-&gt;next = node</code>:接上去。一共走訪了 <b>" + n + "</b> 個節點,所以尾插是 <b>O(n)</b>。"));
    return { frames: fr, result: values(S) };
  }
  function insertAfter(vals, k, v) {
    var n = vals.length;
    if (n === 0) return { error: "串列是空的,沒有節點可以插在後面。請先用「頭插」或「尾插」放一個。" };
    if (n >= MAXN) return { error: "示範最多 " + MAXN + " 個節點,請先刪除幾個或按 Reset。" };
    if (!isInt(k) || k < 0 || k >= n) return { error: "要插在第幾個節點後面?請輸入 0 到 " + (n - 1) + "(從 0 開始數)。" };
    if (!isInt(v) || v < 0 || v > 99) return { error: "數值請輸入 0 到 99 的整數。" };
    var S = build(vals), fr = [], pk = "n" + k;
    S.tags = { prev: pk }; S.cls[pk] = "cur";
    fr.push(snap(S, 28, "<code>insertAfter(prev, " + v + ")</code>:prev 指向第 " + k + " 個節點(值 " + vals[k] + "),要插在它後面。串列沒有索引,實際上要先走訪才找得到 prev,這裡假設已經拿到。"));
    S.nodes.nw = { v: v, next: S.nodes[pk].next }; S.hint.nw = { slot: k + 0.5, row: 1 }; S.tags.node = "nw"; S.cls = { nw: "new" }; S.hot = { nw: true };
    fr.push(snap(S, 29, "<code>new Node{value, prev-&gt;next}</code>:新節點的 next 先指向 prev 原本的下一個節點" + (S.nodes[pk].next ? "" : "(這裡是 null)") + "。"));
    reset(S); S.nodes[pk].next = "nw"; S.hot[pk] = true; S.writes += 2; S.cls.nw = "new";
    fr.push(snap(S, 30, "<code>prev-&gt;next = node</code>:最後才把 prev 接到新節點。共改 2 個指標,<b>沒有搬動任何資料</b>,是 O(1)。"));
    return { frames: fr, result: values(S) };
  }
  function eraseFront(vals) {
    if (vals.length === 0) return { error: "串列是空的,沒有東西可以刪。" };
    var S = build(vals), fr = [];
    fr.push(snap(S, 33, "<code>eraseFront(list)</code>:要刪掉第一個節點(值 " + vals[0] + ")。"));
    S.tags = { old: "n0" }; S.cls.n0 = "del";
    fr.push(snap(S, 34, "<code>Node* old = list.head;</code>:先用 old 記住它。等一下 head 會移走,不記住就找不到、也沒辦法 delete。"));
    S.head = S.nodes.n0.next; S.hint.n0 = { slot: 0, row: 1 }; S.writes++;
    fr.push(snap(S, 35, "<code>list.head = old-&gt;next;</code>:head 改指向第二個節點,old 已經不在串列裡了。"));
    delete S.nodes.n0; S.tags = {}; S.cls = {};
    fr.push(snap(S, 36, "<code>delete old;</code>:把舊節點還給系統。只改了 1 個指標,是 <b>O(1)</b>。"));
    return { frames: fr, result: values(S) };
  }
  function eraseAfter(vals, k) {
    var n = vals.length;
    if (n < 2) return { error: "至少要有 2 個節點,才有「某個節點後面」的節點可以刪。" };
    if (!isInt(k) || k < 0 || k > n - 2) return { error: "要刪第幾個節點後面的那個?請輸入 0 到 " + (n - 2) + "。" };
    var S = build(vals), fr = [], pk = "n" + k, ok = "n" + (k + 1);
    S.tags = { prev: pk }; S.cls[pk] = "cur";
    fr.push(snap(S, 39, "<code>eraseAfter(prev)</code>:prev 指向第 " + k + " 個節點,要刪掉它後面的那個(值 " + vals[k + 1] + ")。"));
    S.tags.old = ok; S.cls[ok] = "del";
    fr.push(snap(S, 40, "<code>Node* old = prev-&gt;next;</code>:用 old 記住要刪的節點。"));
    S.nodes[pk].next = S.nodes[ok].next; S.hint[ok] = { slot: k + 1, row: 1 }; S.hot[pk] = true; S.writes++;
    fr.push(snap(S, 41, "<code>prev-&gt;next = old-&gt;next;</code>:讓 prev 直接跳過 old,接到 old 的下一個。old 已經不在串列裡了。"));
    delete S.nodes[ok]; S.tags = {}; S.cls = {}; S.hot = {};
    fr.push(snap(S, 42, "<code>delete old;</code>:把節點還給系統。只改 1 個指標,<b>沒有搬動任何資料</b>。"));
    return { frames: fr, result: values(S) };
  }
  A.list = { MAXN: MAXN, CODE_LIST: CODE_LIST, pushFront: pushFront, pushBack: pushBack, insertAfter: insertAfter, eraseFront: eraseFront, eraseAfter: eraseAfter, idle: function (vals) { return snap(build(vals), undefined, ""); } };
  if (typeof module !== "undefined" && module.exports) module.exports = A;
})(typeof window !== "undefined" ? window : globalThis);
