(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var MAXN = 10, MAXCAP = 16;

  /* 程式碼面板文字:必須與 cpp/array_edit.cpp、cpp/array_grow.cpp 的對應片段一致(test_algo.js 會檢查) */
  var CODE_EDIT = [
    "void insertAt(std::vector<int>& v, int pos, int value) {",
    "    v.push_back(0);                      // 先在尾端多開一格",
    "    int last = static_cast<int>(v.size()) - 1;",
    "    for (int i = last; i > pos; --i) {",
    "        v[i] = v[i - 1];                 // 把前一格搬過來",
    "    }",
    "    v[pos] = value;                      // 空位放進新值",
    "}",
    "",
    "void eraseAt(std::vector<int>& v, int pos) {",
    "    int n = static_cast<int>(v.size());",
    "    for (int i = pos; i + 1 < n; ++i) {",
    "        v[i] = v[i + 1];                 // 把後一格搬過來",
    "    }",
    "    v.pop_back();                        // 丟掉最後一格",
    "}"].join("\n");
  var CODE_GROW = [
    "std::vector<int> v;",
    "for (int i = 1; i <= 9; ++i) {",
    "    v.push_back(i);",
    "    std::cout << v.size() << \" \" << v.capacity() << \"\\n\";",
    "}"].join("\n");

  function mk(arr, over) { return arr.map(function (v, i) { return { v: v, cls: (over && over[i]) || "" }; }); }
  function isInt(x) { return typeof x === "number" && isFinite(x) && Math.floor(x) === x; }

  /* ---- 在 pos 插入 value ---- */
  function insert(arr, pos, val) {
    var n = arr.length;
    if (n >= MAXN) return { error: "示範最多放 " + MAXN + " 個元素,請先按 Reset 或刪掉幾個。" };
    if (!isInt(pos) || pos < 0 || pos > n) return { error: "位置必須是 0 到 " + n + " 的整數(目前有 " + n + " 個元素)。" };
    if (!isInt(val) || val < 0 || val > 99) return { error: "數值請輸入 0 到 99 的整數。" };
    var a = arr.slice(), moves = 0, fr = [];
    function chips() { return [["元素個數", a.length], ["搬動次數", moves]]; }
    fr.push({ cells: mk(a), chips: chips(), line: 1, msg: "現在有 " + n + " 個元素,要在位置 <b>" + pos + "</b> 插入 <b>" + val + "</b>。" });
    a.push(0);
    var o = {}; o[n] = "new";
    fr.push({ cells: mk(a, o), chips: chips(), line: [2, 3], msg: "<code>push_back(0)</code>:先在尾端多開一格(裡面暫時是 0,等一下會被蓋掉)。" });
    for (var i = n; i > pos; i--) {
      a[i] = a[i - 1]; moves++;
      o = {}; o[i] = "mv mvr"; o[i - 1] = "cur";
      fr.push({ cells: mk(a, o), chips: chips(), line: [4, 5],
        msg: "<code>v[" + i + "] = v[" + (i - 1) + "]</code>:把 " + a[i] + " 從位置 " + (i - 1) + " 搬到位置 " + i + "。這是第 " + moves + " 次搬動。" });
    }
    a[pos] = val; o = {}; o[pos] = "new";
    fr.push({ cells: mk(a, o), chips: chips(), line: 7,
      msg: "<code>v[" + pos + "] = " + val + "</code>:空位放進新值。" + (moves === 0 ? "插在尾端,<b>完全不用搬動</b>。" : "一共搬動了 <b>" + moves + "</b> 次。") });
    return { frames: fr, result: a };
  }

  /* ---- 刪除 pos ---- */
  function erase(arr, pos) {
    var n = arr.length;
    if (n === 0) return { error: "vector 是空的,沒有東西可以刪。" };
    if (!isInt(pos) || pos < 0 || pos >= n) return { error: "位置必須是 0 到 " + (n - 1) + " 的整數。" };
    var a = arr.slice(), moves = 0, fr = [], o = {};
    function chips() { return [["元素個數", a.length], ["搬動次數", moves]]; }
    o[pos] = "del";
    fr.push({ cells: mk(a, o), chips: chips(), line: 10, msg: "要刪除位置 <b>" + pos + "</b> 的 " + a[pos] + "。刪掉之後,後面的元素都要往前補位。" });
    for (var i = pos; i + 1 < n; i++) {
      a[i] = a[i + 1]; moves++;
      o = {}; o[i] = "mv mvl"; o[i + 1] = "cur";
      fr.push({ cells: mk(a, o), chips: chips(), line: [12, 13],
        msg: "<code>v[" + i + "] = v[" + (i + 1) + "]</code>:把 " + a[i] + " 從位置 " + (i + 1) + " 搬到位置 " + i + "。這是第 " + moves + " 次搬動。" });
    }
    a.pop();
    fr.push({ cells: mk(a), chips: chips(), line: 15,
      msg: "<code>pop_back()</code>:丟掉最後一格。" + (moves === 0 ? "刪的是最後一個,<b>完全不用搬動</b>。" : "一共搬動了 <b>" + moves + "</b> 次。越靠前面的位置,要搬的越多。") });
    return { frames: fr, result: a };
  }

  /* ---- push_back 與擴容(模型:容量不夠就換成 2 倍大的新空間並搬家,與 g++ 的 libstdc++ 行為相同) ---- */
  function growInit() { return { vals: [], cap: 0, grows: 0, copies: 0, next: 1 }; }
  function push(base, count) {
    if (!isInt(count) || count < 1 || count > 9) return { error: "一次請輸入 1 到 9 次。" };
    if (base.vals.length + count > MAXCAP) return { error: "示範最多放 " + MAXCAP + " 個元素,請按 Reset 重新開始。" };
    var b = { vals: base.vals.slice(), cap: base.cap, grows: base.grows, copies: base.copies, next: base.next }, fr = [];
    function chips() { return [["size", b.vals.length], ["capacity", b.cap], ["擴容次數", b.grows], ["累計複製", b.copies]]; }
    function one(cells, empty, over) { return { cells: mk(cells, over), empty: empty, chips: chips() }; }
    for (var k = 0; k < count; k++) {
      var x = b.next++, f;
      if (b.vals.length < b.cap) {
        f = one(b.vals, b.cap - b.vals.length); f.line = 3;
        f.msg = "<code>push_back(" + x + ")</code>:size=" + b.vals.length + "、capacity=" + b.cap + ",還有空位,直接放進去。";
        fr.push(f);
      } else {
        var nc = b.cap === 0 ? 1 : b.cap * 2, old = b.vals.slice();
        f = one(b.vals, 0); f.line = 3;
        f.msg = "<code>push_back(" + x + ")</code>:size=" + old.length + "、capacity=" + b.cap + ",<b>已經滿了</b>,需要擴容。";
        if (old.length === 0) f.msg = "<code>push_back(" + x + ")</code>:一開始 capacity=0,一個位置都沒有,要先要一塊空間。";
        fr.push(f);
        fr.push({ rows: [{ label: "舊空間(容量 " + b.cap + ")", cells: mk(old, { 0: "" }), empty: 0 }, { label: "新空間(容量 " + nc + ")", cells: [], empty: nc }],
          chips: chips(), line: 3, msg: "向系統要一塊容量 <b>" + nc + "</b> 的新空間(通常是原本的 2 倍)。" });
        for (var j = 0; j < old.length; j++) {
          b.copies++;
          var oo = {}; oo[j] = "cur";
          fr.push({ rows: [{ label: "舊空間(容量 " + b.cap + ")", cells: mk(old, oo), empty: 0 }, { label: "新空間(容量 " + nc + ")", cells: mk(old.slice(0, j + 1), (function (q) { var r = {}; r[q] = "mv"; return r; })(j)), empty: nc - j - 1 }],
            chips: chips(), line: 3, msg: "把位置 " + j + " 的 " + old[j] + " 複製到新空間(累計複製 " + b.copies + " 次)。" });
        }
        b.cap = nc; b.grows++;
        fr.push(Object.assign(one(old, nc - old.length), { line: 3, msg: "舊空間釋放掉,之後只用新空間。擴容一次,就要搬一次家。" }));
        b.vals.push(x);
        var no = {}; no[b.vals.length - 1] = "new";
        fr.push(Object.assign(one(b.vals, b.cap - b.vals.length, no), { line: 3, msg: "新值 " + x + " 放進新空間。" }));
        fr.push(Object.assign(one(b.vals, b.cap - b.vals.length), { line: 4, msg: "印出 <code>" + b.vals.length + " " + b.cap + "</code>(size 和 capacity)。" }));
        continue;
      }
      b.vals.push(x);
      var o2 = {}; o2[b.vals.length - 1] = "new";
      fr.push(Object.assign(one(b.vals, b.cap - b.vals.length, o2), { line: 3, msg: "新值 " + x + " 放進去,size 變成 " + b.vals.length + "。" }));
      fr.push(Object.assign(one(b.vals, b.cap - b.vals.length), { line: 4, msg: "印出 <code>" + b.vals.length + " " + b.cap + "</code>(size 和 capacity)。" }));
    }
    return { frames: fr, result: b };
  }

  A.vec = { mk: mk, MAXN: MAXN, MAXCAP: MAXCAP, CODE_EDIT: CODE_EDIT, CODE_GROW: CODE_GROW, insert: insert, erase: erase, growInit: growInit, push: push };
  if (typeof module !== "undefined" && module.exports) module.exports = A;
})(typeof window !== "undefined" ? window : globalThis);
