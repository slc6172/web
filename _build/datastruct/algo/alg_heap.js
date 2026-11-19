(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var CODE_HEAP = "void siftUp(std::vector<int>& h, int i) {\n    while (i > 0) {\n        int parent = (i - 1) / 2;\n        if (h[parent] >= h[i]) {\n            break;\n        }\n        std::swap(h[parent], h[i]);\n        i = parent;\n    }\n}\n\nvoid push(std::vector<int>& h, int val) {\n    h.push_back(val);\n    siftUp(h, static_cast<int>(h.size()) - 1);\n}\n\nvoid siftDown(std::vector<int>& h, int i) {\n    int n = static_cast<int>(h.size());\n    while (true) {\n        int largest = i;\n        int left = 2 * i + 1;\n        int right = 2 * i + 2;\n        if (left < n && h[left] > h[largest]) {\n            largest = left;\n        }\n        if (right < n && h[right] > h[largest]) {\n            largest = right;\n        }\n        if (largest == i) {\n            break;\n        }\n        std::swap(h[i], h[largest]);\n        i = largest;\n    }\n}\n\nint pop(std::vector<int>& h) {\n    int top = h[0];\n    h[0] = h.back();\n    h.pop_back();\n    if (!h.empty()) {\n        siftDown(h, 0);\n    }\n    return top;\n}";
  var MAXN = 10, LO = 1, HI = 99;
  var NAMES = { push: "push 放入", pop: "pop 取出最大" };
  function init() { return []; }
  function isHeap(a) { for (var i = 0; i < a.length; i++) { var l = 2 * i + 1, r = 2 * i + 2; if ((l < a.length && a[l] > a[i]) || (r < a.length && a[r] > a[i])) return false; } return true; }
  /* 靜默建堆積(不出 frame):照 siftUp 一個一個 push */
  function fromList(list) {
    var h = [];
    list.forEach(function (v) { h.push(v); var i = h.length - 1; while (i > 0) { var p = (i - 1) >> 1; if (h[p] >= h[i]) break; var t = h[p]; h[p] = h[i]; h[i] = t; i = p; } });
    return h;
  }
  function toFrame(arr, cls, line, msg, st) {
    var nodes = {};
    arr.forEach(function (v, i) { nodes["i" + i] = { label: v, l: 2 * i + 1 < arr.length ? "i" + (2 * i + 1) : null, r: 2 * i + 2 < arr.length ? "i" + (2 * i + 2) : null, cls: cls[i] || "" }; });
    return { arr: arr.slice(), tree: { root: arr.length ? "i0" : null, nodes: nodes },
      cells: arr.map(function (v, i) { return { v: v, cls: cls[i] || "" }; }), line: line, msg: msg,
      chips: [["大小", arr.length], ["比較次數", st.cmp], ["交換次數", st.swp]] };
  }
  function idle(base) {
    var f = toFrame(base, {}, undefined, "", { cmp: 0, swp: 0 });
    f.chips = f.chips.slice(0, 1);
    f.msg = base.length ? "目前最大的是 <b>" + base[0] + "</b>(就在根,位置 0)。選一個操作,按「執行」。" : "堆積是空的。先 push 幾個數字,或按「範例」。";
    return f;
  }
  function run(op, val, base) {
    if (!NAMES[op]) return { error: "請選一個操作。" };
    var h = base.slice(), st = { cmp: 0, swp: 0 }, fr = [];
    function X(a, ca, b, cb) { var o = {}; if (a !== undefined) o[a] = ca; if (b !== undefined) o[b] = cb; return o; }
    function snap(line, msg, cls) { fr.push(toFrame(h, cls || {}, line, msg, st)); }
    var endMsg = function () { return "陣列現在是 <b>" + (h.join(" ") || "(空)") + "</b>。"; };
    if (op === "push") {
      if (!(Number.isInteger(val) && val >= LO && val <= HI)) return { error: "請輸入 " + LO + " 到 " + HI + " 的整數。" };
      if (h.length >= MAXN) return { error: "動畫最多放 " + MAXN + " 個數字,請先 pop 一些,或按 Reset。" };
      h.push(val); var i = h.length - 1;
      snap(13, "<code>push_back(" + val + ")</code>:先放在陣列最後面,位置 " + i + "。對應到樹,就是最底層最左邊的空位(完全二元樹一格一格填)。", X(i, "new"));
      while (i > 0) {
        var p = (i - 1) >> 1; st.cmp++;
        if (h[p] >= h[i]) {
          snap([3, 5], "父節點在位置 (" + i + "-1)/2 = " + p + ",值 " + h[p] + " ≥ " + h[i] + ":不用再上去了,<code>break</code>。", X(i, "cur", p, "new"));
          snap(undefined, "完成。" + endMsg() + "每個節點都不小於它的子節點,這就是最大堆積。", {});
          return { frames: fr, result: h };
        }
        snap([3, 4], "父節點在位置 (" + i + "-1)/2 = " + p + ",值 " + h[p] + " &lt; " + h[i] + ":新來的比較大,要跟父節點換。", X(i, "cur", p, "new"));
        var t = h[p]; h[p] = h[i]; h[i] = t; st.swp++;
        snap([7, 8], "<code>swap</code>:換上去了,現在它在位置 <b>" + p + "</b>(<code>i = parent</code>)。", X(p, "cur", i, "new"));
        i = p;
      }
      snap(2, "<code>i == 0</code>:已經到根了,不能再往上(<code>while (i &gt; 0)</code> 結束)。", X(0, "cur"));
      snap(undefined, "完成。" + endMsg() + "新的數字是最大的,現在是根。", {});
      return { frames: fr, result: h };
    }
    if (!h.length) return { error: "堆積是空的,沒有東西可以 pop。先 push 幾個數字。" };
    var top = h[0], last = h.length - 1;
    snap(38, "<code>int top = h[0]</code>:最大的值永遠在根(位置 0),先記下來:<b>" + top + "</b>。", X(0, "del"));
    if (last === 0) {
      snap([39, 40], "只剩一個,<code>pop_back</code> 之後堆積變空。", X(0, "del")); h.pop();
      snap(undefined, "完成。pop 回傳 <b>" + top + "</b>。堆積現在是空的。", {});
      return { frames: fr, result: h, popped: top };
    }
    var lv = h[last]; h[0] = lv;
    snap(39, "<code>h[0] = h.back()</code>:直接拿掉根會留下一個洞,所以把<b>最後一個</b>(" + lv + ")搬到根。陣列短一格比挖掉中間輕鬆得多。", X(0, "cur", last, "del"));
    h.pop();
    snap(40, "<code>pop_back()</code>:最後那格刪掉。現在樹的形狀恢復成完全二元樹,但根(" + lv + ")可能太小,不一定符合規則。", X(0, "cur"));
    var i2 = 0, n = h.length;
    snap(42, "<code>siftDown(h, 0)</code>:讓根<b>往下沉</b>,直到比兩個子節點都大。", X(0, "cur"));
    while (true) {
      var largest = i2, l = 2 * i2 + 1, r = 2 * i2 + 2;
      if (l < n) { st.cmp++; if (h[l] > h[largest]) largest = l; }
      snap([23, 24], l < n ? "看左子(位置 " + l + ",值 " + h[l] + ")" + (h[l] > h[i2] ? ":比 " + h[i2] + " 大,<code>largest = left</code>。" : ":沒有比 " + h[i2] + " 大。") : "左子的位置 " + l + " ≥ 大小 " + n + ":沒有左子。", l < n ? X(i2, "cur", l, "new") : X(i2, "cur"));
      if (r < n) { st.cmp++; if (h[r] > h[largest]) largest = r; }
      snap([26, 27], r < n ? "看右子(位置 " + r + ",值 " + h[r] + ")" + (largest === r ? ":比目前最大的還大,<code>largest = right</code>。" : ":沒有比目前最大的大。") : "右子的位置 " + r + " ≥ 大小 " + n + ":沒有右子。", r < n ? X(i2, "cur", r, "new") : X(i2, "cur"));
      if (largest === i2) {
        snap([29, 30], "<code>largest == i</code>:<b>" + h[i2] + "</b> 比它的子節點都大(或沒有子節點),停止下沉。", X(i2, "cur"));
        break;
      }
      var t2 = h[i2]; h[i2] = h[largest]; h[largest] = t2; st.swp++;
      snap([32, 33], "<code>swap</code>:跟較大的子節點(位置 " + largest + ")交換,現在它在位置 <b>" + largest + "</b>(<code>i = largest</code>)。", X(largest, "cur", i2, "new"));
      i2 = largest;
    }
    snap(44, "<code>return top</code>:pop 回傳 <b>" + top + "</b>。" + endMsg(), {});
    return { frames: fr, result: h, popped: top };
  }
  A.heap = { CODE_HEAP: CODE_HEAP, NAMES: NAMES, MAXN: MAXN, LO: LO, HI: HI, init: init, fromList: fromList, run: run, idle: idle, isHeap: isHeap };
  if (typeof module !== "undefined" && module.exports) module.exports = A;
})(typeof window !== "undefined" ? window : globalThis);
