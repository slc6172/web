(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var MAXN = 20;
  var CODE_SEARCH = [
    "int linearSearch(const std::vector<int>& v, int target) {", "    for (int i = 0; i < static_cast<int>(v.size()); ++i) {", "        if (v[i] == target) {", "            return i;", "        }", "    }", "    return -1;", "}", "",
    "int binarySearch(const std::vector<int>& v, int target) {", "    int lo = 0;", "    int hi = static_cast<int>(v.size()) - 1;", "    while (lo <= hi) {", "        int mid = lo + (hi - lo) / 2;",
    "        if (v[mid] == target) {", "            return mid;", "        } else if (v[mid] < target) {", "            lo = mid + 1;", "        } else {", "            hi = mid - 1;", "        }", "    }", "    return -1;", "}"].join("\n");
  function isInt(x) { return typeof x === "number" && isFinite(x) && Math.floor(x) === x; }
  function check(arr, target) {
    if (!arr.length) return "資料是空的,請按「重新產生資料」。";
    if (!isInt(target) || target < 0 || target > 99) return "目標請輸入 0 到 99 的整數。";
    return null;
  }
  function randomSorted(n, rnd) {
    rnd = rnd || Math.random; var set = {}, out = [];
    while (out.length < n) { var x = 1 + Math.floor(rnd() * 99); if (!set[x]) { set[x] = 1; out.push(x); } }
    return out.sort(function (a, b) { return a - b; });
  }
  function cells(a, over, tags) { return a.map(function (v, i) { var c = { v: v, cls: (over && over[i]) || "" }; if (tags && tags[i]) c.t = tags[i].join("/"); return c; }); }
  function linear(arr, target) {
    var e = check(arr, target); if (e) return { error: e };
    var fr = [], k = 0, over = {}, n = arr.length;
    fr.push({ cells: cells(arr), chips: [["比較次數", 0]], line: 2, msg: "線性搜尋:從第 0 個開始,一個個和目標 <b>" + target + "</b> 比。" });
    for (var i = 0; i < n; i++) {
      k++; var o = {}; for (var q = 0; q < i; q++) o[q] = "dim"; o[i] = "cur";
      if (arr[i] === target) {
        o[i] = "new"; fr.push({ cells: cells(arr, o), chips: [["比較次數", k]], line: [3, 4], msg: "v[" + i + "] = " + arr[i] + " 等於目標,<b>找到了</b>!回傳 " + i + "。一共比了 <b>" + k + "</b> 次。" });
        return { frames: fr, result: arr, found: i, comparisons: k };
      }
      fr.push({ cells: cells(arr, o), chips: [["比較次數", k]], line: [2, 3], msg: "v[" + i + "] = " + arr[i] + " ≠ " + target + ",看下一個。" });
    }
    var all = {}; for (var j = 0; j < n; j++) all[j] = "dim";
    fr.push({ cells: cells(arr, all), chips: [["比較次數", k]], line: 7, msg: "全部都看過了,沒有 " + target + "。回傳 -1。一共比了 <b>" + k + "</b> 次。" });
    return { frames: fr, result: arr, found: -1, comparisons: k };
  }
  function binary(arr, target) {
    var e = check(arr, target); if (e) return { error: e };
    var fr = [], k = 0, lo = 0, hi = arr.length - 1;
    function view(mid, line, msg, cls) {
      var over = {}, tags = {}; for (var i = 0; i < arr.length; i++) if (i < lo || i > hi) over[i] = "dim";
      function tag(i, nm) { if (i >= 0 && i < arr.length) (tags[i] = tags[i] || []).push(nm); }
      tag(lo, "lo"); if (mid !== null) tag(mid, "mid"); tag(hi, "hi");
      if (mid !== null) over[mid] = cls || "cur";
      fr.push({ cells: cells(arr, over, tags), chips: [["比較次數", k], ["範圍大小", Math.max(0, hi - lo + 1)]], line: line, msg: msg });
    }
    view(null, [11, 12], "二分搜尋要求資料<b>已排序</b>。lo = 0、hi = " + hi + ":目標如果存在,一定在 lo 到 hi 之間。");
    while (lo <= hi) {
      var mid = lo + Math.floor((hi - lo) / 2); k++;
      if (arr[mid] === target) {
        view(mid, [14, 15, 16], "mid = " + mid + ",v[mid] = " + arr[mid] + " 等於目標,<b>找到了</b>!回傳 " + mid + "。一共比了 <b>" + k + "</b> 次。", "new");
        return { frames: fr, result: arr, found: mid, comparisons: k };
      }
      if (arr[mid] < target) {
        view(mid, [14, 15], "mid = " + mid + ",v[mid] = " + arr[mid] + " <b>小於</b> " + target + ":目標只可能在右邊。");
        lo = mid + 1; view(null, 18, "<code>lo = mid + 1</code>:左半邊整個丟掉。範圍縮成 " + Math.max(0, hi - lo + 1) + " 個。");
      } else {
        view(mid, [14, 15], "mid = " + mid + ",v[mid] = " + arr[mid] + " <b>大於</b> " + target + ":目標只可能在左邊。");
        hi = mid - 1; view(null, 20, "<code>hi = mid - 1</code>:右半邊整個丟掉。範圍縮成 " + Math.max(0, hi - lo + 1) + " 個。");
      }
    }
    view(null, 23, "lo &gt; hi,範圍已經空了,沒有 " + target + "。回傳 -1。一共比了 <b>" + k + "</b> 次。");
    return { frames: fr, result: arr, found: -1, comparisons: k };
  }
  function worst(n) { return { linear: n, binary: n < 1 ? 0 : Math.floor(Math.log2(n)) + 1 }; }
  A.search = { MAXN: MAXN, CODE_SEARCH: CODE_SEARCH, randomSorted: randomSorted, linear: linear, binary: binary, worst: worst };
  if (typeof module !== "undefined" && module.exports) module.exports = A;
})(typeof window !== "undefined" ? window : globalThis);
