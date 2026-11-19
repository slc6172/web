(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var CODE_ADV = [
    "void merge(std::vector<int>& v, std::vector<int>& tmp, int lo, int mid, int hi) {", "    int i = lo;", "    int j = mid + 1;", "    int k = lo;", "    while (i <= mid && j <= hi) {",
    "        if (v[i] <= v[j]) {", "            tmp[k++] = v[i++];", "        } else {", "            tmp[k++] = v[j++];", "        }", "    }", "    while (i <= mid) {", "        tmp[k++] = v[i++];", "    }",
    "    while (j <= hi) {", "        tmp[k++] = v[j++];", "    }", "    for (int p = lo; p <= hi; ++p) {", "        v[p] = tmp[p];", "    }", "}", "",
    "void mergeSort(std::vector<int>& v, std::vector<int>& tmp, int lo, int hi) {", "    if (lo >= hi) {", "        return;", "    }", "    int mid = lo + (hi - lo) / 2;", "    mergeSort(v, tmp, lo, mid);", "    mergeSort(v, tmp, mid + 1, hi);", "    merge(v, tmp, lo, mid, hi);", "}", "",
    "int partition(std::vector<int>& v, int lo, int hi) {", "    int pivot = v[hi];", "    int i = lo;", "    for (int j = lo; j < hi; ++j) {", "        if (v[j] < pivot) {", "            std::swap(v[i], v[j]);", "            ++i;", "        }", "    }",
    "    std::swap(v[i], v[hi]);", "    return i;", "}", "", "void quickSort(std::vector<int>& v, int lo, int hi) {", "    if (lo >= hi) {", "        return;", "    }", "    int p = partition(v, lo, hi);",
    "    quickSort(v, lo, p - 1);", "    quickSort(v, p + 1, hi);", "}"].join("\n");
  var NAMES = { merge: "合併排序", quick: "快速排序" };

  function mergeSorter(input, record) {
    var v = input.slice(), n = v.length, tmp = [], cmp = 0, wr = 0, fr = [], sorted = [], i;
    for (i = 0; i < n; i++) { tmp.push(null); sorted.push(false); }
    function emit(line, msg, o) {
      if (!record) return; o = o || {};
      var vc = [], vt = [], tc = [], tt = [];
      for (var q = 0; q < n; q++) {
        var base = sorted[q] ? "ok" : (o.lo !== undefined && (q < o.lo || q > o.hi) ? "dim" : "");
        vc.push((o.vcls && o.vcls[q]) || base); vt.push((o.vtags && o.vtags[q]) || ""); tc.push((o.tcls && o.tcls[q]) || ""); tt.push("");
      }
      fr.push({ rows: [{ label: "v(要排序的陣列)", vals: v.slice(), cls: vc, tags: vt }, { label: "tmp(合併用的暫存區)", vals: tmp.slice(), cls: tc, tags: tt }], chips: [["比較次數", cmp], ["寫入 tmp", wr]], line: line, msg: msg });
    }
    function merge(lo, mid, hi) {
      var i = lo, j = mid + 1, k = lo, tcls = {};
      emit(30, "左右兩半 <b>[" + lo + ".." + mid + "]</b> 和 <b>[" + (mid + 1) + ".." + hi + "]</b> 都各自排好了,現在把它們合併成一個排好的區段。", { lo: lo, hi: hi });
      function placed() { var c = {}; for (var q = lo; q < k; q++) c[q] = "ok"; c[k - 1] = "new"; return c; }
      while (i <= mid && j <= hi) {
        cmp++; var left = v[i] <= v[j], x = left ? v[i] : v[j]; tmp[k] = x; wr++; var vc = {}; vc[i] = "cur"; vc[j] = "cur"; k++;
        emit(left ? [5, 6, 7] : [5, 6, 9], "比較 v[" + i + "] = " + v[i] + " 和 v[" + j + "] = " + v[j] + ":" + (left ? "左邊 " + v[i] + " ≤ 右邊,取左邊" : "右邊 " + v[j] + " 比較小,取右邊") + ",放進 tmp[" + (k - 1) + "]。", { lo: lo, hi: hi, vcls: vc, tcls: placed() });
        if (left) i++; else j++;
      }
      while (i <= mid) { tmp[k] = v[i]; wr++; var vc2 = {}; vc2[i] = "cur"; k++; emit([12, 13], "右邊已經用完,左邊剩下的 " + v[i] + " 直接放進 tmp[" + (k - 1) + "]。", { lo: lo, hi: hi, vcls: vc2, tcls: placed() }); i++; }
      while (j <= hi) { tmp[k] = v[j]; wr++; var vc3 = {}; vc3[j] = "cur"; k++; emit([15, 16], "左邊已經用完,右邊剩下的 " + v[j] + " 直接放進 tmp[" + (k - 1) + "]。", { lo: lo, hi: hi, vcls: vc3, tcls: placed() }); j++; }
      for (var p = lo; p <= hi; p++) { v[p] = tmp[p]; sorted[p] = true; }
      var tc = {}; for (p = lo; p <= hi; p++) tc[p] = "ok";
      emit([18, 19], "把 tmp[" + lo + ".." + hi + "] 複製回 v:這一段排好了。", { lo: lo, hi: hi, tcls: tc });
      for (p = lo; p <= hi; p++) tmp[p] = null;
    }
    function ms(lo, hi) {
      if (lo >= hi) { sorted[lo] = true; emit([23, 24, 25], "<code>mergeSort(" + lo + ".." + hi + ")</code>:只有 1 個元素,本來就排好了,直接返回。", { lo: lo, hi: hi }); return; }
      var mid = lo + Math.floor((hi - lo) / 2), vt = {}; vt[mid] = "mid";
      emit([23, 27], "<code>mergeSort(" + lo + ".." + hi + ")</code>:有 " + (hi - lo + 1) + " 個元素。<b>分</b>:切成左 [" + lo + ".." + mid + "] 與右 [" + (mid + 1) + ".." + hi + "]。", { lo: lo, hi: hi, vtags: vt });
      ms(lo, mid); ms(mid + 1, hi); merge(lo, mid, hi);
    }
    if (record) emit(23, "合併排序:<b>分</b>(切成一半)再<b>合</b>(把兩個排好的合併)。先一路切到只剩 1 個。", {});
    if (n > 0) ms(0, n - 1);
    emit(31, "排序完成!一共比較 <b>" + cmp + "</b> 次。", {});
    return { frames: fr, result: v, cmp: cmp, swp: wr };
  }

  function quickSorter(input, record) {
    var v = input.slice(), n = v.length, cmp = 0, swp = 0, fr = [], fin = [], i;
    for (i = 0; i < n; i++) fin.push(false);
    function emit(line, msg, o) {
      if (!record) return; o = o || {};
      var c = [], t = [];
      for (var q = 0; q < n; q++) { c.push((o.cls && o.cls[q]) || (fin[q] ? "ok" : (o.lo !== undefined && (q < o.lo || q > o.hi) ? "dim" : ""))); t.push((o.tags && o.tags[q]) || ""); }
      fr.push({ vals: v.slice(), cls: c, tags: t, chips: [["比較次數", cmp], ["交換次數", swp]], line: line, msg: msg });
    }
    function qs(lo, hi) {
      if (lo > hi) return;
      if (lo === hi) { fin[lo] = true; emit([46, 47, 48], "<code>quickSort(" + lo + ".." + hi + ")</code>:只剩 1 個,它一定在正確位置了。", { lo: lo, hi: hi }); return; }
      var pivot = v[hi], i = lo, cls = {}, tags = {};
      function zone(j) { var c = {}; for (var q = lo; q < i; q++) c[q] = "tgt"; c[hi] = "key"; if (j !== undefined) c[j] = "cur"; return c; }
      tags[hi] = "pivot"; cls[hi] = "key";
      emit([46, 34], "<code>quickSort(" + lo + ".." + hi + ")</code>:有 " + (hi - lo + 1) + " 個。挑最後一個 <b>" + pivot + "</b> 當基準(pivot)。目標:把比 pivot 小的換到左邊(藍色)。", { lo: lo, hi: hi, cls: cls, tags: tags });
      for (var j = lo; j < hi; j++) {
        cmp++; var less = v[j] < pivot, tg = {}; tg[hi] = "pivot"; tg[i] = "i"; tg[j] = i === j ? "i,j" : "j";
        emit([36, 37], "比較 v[" + j + "] = " + v[j] + " 和 pivot " + pivot + ":" + (less ? "比較小,要放到左區。" : "不比 pivot 小,留在右區。"), { lo: lo, hi: hi, cls: zone(j), tags: tg });
        if (less) {
          var sw = i !== j; if (sw) { var t = v[i]; v[i] = v[j]; v[j] = t; swp++; } var c2 = zone(); if (sw) { c2[i] = "mv"; c2[j] = "mv"; } i++; tg = {}; tg[hi] = "pivot"; tg[i] = "i";
          emit([38, 39], sw ? "<code>swap(v[" + (i - 1) + "], v[" + j + "])</code>:把小的換到左區邊界,左區多一個,<code>i</code> 往右。" : "v[" + j + "] 剛好就在左區邊界,不用交換,左區多一個,<code>i</code> 往右。", { lo: lo, hi: hi, cls: c2, tags: tg });
        }
      }
      if (i !== hi) { var t2 = v[i]; v[i] = v[hi]; v[hi] = t2; swp++; }
      fin[i] = true; var c3 = {}; c3[i] = "new";
      emit(42, "<code>swap(v[" + i + "], v[" + hi + "])</code>:把 pivot " + pivot + " 換到位置 " + i + "。左邊都比它小,右邊都不比它小,<b>pivot 就定位了,不會再動</b>。", { lo: lo, hi: hi, cls: c3 });
      qs(lo, i - 1); qs(i + 1, hi);
    }
    if (record) emit(46, "快速排序:挑一個基準(pivot),把資料分成「比它小」和「比它大」兩邊,再各自排。", {});
    qs(0, n - 1);
    for (i = 0; i < n; i++) fin[i] = true;
    emit(53, "排序完成!一共比較 <b>" + cmp + "</b> 次,交換 <b>" + swp + "</b> 次。", {});
    return { frames: fr, result: v, cmp: cmp, swp: swp };
  }
  function run(alg, text) {
    if (!NAMES[alg]) return { error: "請選一種排序法。" };
    var p = A.sort.parse(text); if (p.error) return p;
    var r = alg === "merge" ? mergeSorter(p.vals, true) : quickSorter(p.vals, true); r.result = null; return r;
  }
  function stats(alg, arr) { var r = alg === "merge" ? mergeSorter(arr, false) : quickSorter(arr, false); return { cmp: r.cmp, swp: r.swp, sorted: r.result }; }
  A.sortadv = { CODE_ADV: CODE_ADV, NAMES: NAMES, run: run, stats: stats };
  if (typeof module !== "undefined" && module.exports) module.exports = A;
})(typeof window !== "undefined" ? window : globalThis);
