(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var MAXN = 10;
  var CODE_SORT = [
    "void bubbleSort(std::vector<int>& v) {", "    int n = static_cast<int>(v.size());", "    for (int i = 0; i < n - 1; ++i) {", "        bool swapped = false;", "        for (int j = 0; j < n - 1 - i; ++j) {",
    "            if (v[j] > v[j + 1]) {", "                std::swap(v[j], v[j + 1]);", "                swapped = true;", "            }", "        }", "        if (!swapped) {", "            break;", "        }", "    }", "}", "",
    "void selectionSort(std::vector<int>& v) {", "    int n = static_cast<int>(v.size());", "    for (int i = 0; i < n - 1; ++i) {", "        int minIdx = i;", "        for (int j = i + 1; j < n; ++j) {",
    "            if (v[j] < v[minIdx]) {", "                minIdx = j;", "            }", "        }", "        std::swap(v[i], v[minIdx]);", "    }", "}", "",
    "void insertionSort(std::vector<int>& v) {", "    int n = static_cast<int>(v.size());", "    for (int i = 1; i < n; ++i) {", "        int key = v[i];", "        int j = i - 1;",
    "        while (j >= 0 && v[j] > key) {", "            v[j + 1] = v[j];", "            --j;", "        }", "        v[j + 1] = key;", "    }", "}"].join("\n");
  var NAMES = { bubble: "氣泡排序", selection: "選擇排序", insertion: "插入排序" };

  /* 單一實作:record=true 時產生 frame;record=false 只統計(給「實驗」用) */
  function sorter(alg, input, record) {
    var a = input.slice(), n = a.length, cmp = 0, swp = 0, fr = [];
    function emit(line, msg, cls, tags, extra) {
      if (!record) return;
      var c = [], t = [], i; for (i = 0; i < n; i++) { c.push((cls && cls[i]) || ""); t.push((tags && tags[i]) || ""); }
      fr.push({ vals: a.slice(), cls: c, tags: t, chips: [["比較次數", cmp], [alg === "insertion" ? "搬動次數" : "交換次數", swp]].concat(extra || []), line: line, msg: msg });
    }
    function mark(map, from, to, cls) { for (var q = from; q <= to; q++) if (q >= 0 && q < n) map[q] = cls; }
    var o, i, j;
    if (alg === "bubble") {
      emit([2, 3], "氣泡排序:每一輪從左到右,比較相鄰兩個,<b>左邊比右邊大就交換</b>。一輪下來,最大的會「浮」到最右邊。");
      for (i = 0; i < n - 1; i++) {
        var swapped = false;
        for (j = 0; j < n - 1 - i; j++) {
          cmp++; o = {}; mark(o, n - i, n - 1, "ok"); o[j] = "cur"; o[j + 1] = "cur";
          var gt = a[j] > a[j + 1];
          emit([5, 6], "比較 v[" + j + "] = " + a[j] + " 和 v[" + (j + 1) + "] = " + a[j + 1] + (gt ? ":左邊比較大,要交換。" : ":順序正確,不動。"), o);
          if (gt) { var t = a[j]; a[j] = a[j + 1]; a[j + 1] = t; swp++; swapped = true; o = {}; mark(o, n - i, n - 1, "ok"); o[j] = "mv"; o[j + 1] = "mv"; emit([7, 8], "交換:" + a[j + 1] + " 往右移了一格。", o); }
        }
        if (!swapped) { o = {}; mark(o, 0, n - 1, "ok"); emit([11, 12], "這一輪<b>一次都沒有交換</b>,代表已經排好,提早結束(<code>break</code>)。", o); return { frames: fr, result: a, cmp: cmp, swp: swp }; }
      }
    } else if (alg === "selection") {
      emit([18, 19], "選擇排序:每一輪從「還沒排好的部分」挑出<b>最小的</b>,和該部分的第一個交換。");
      for (i = 0; i < n - 1; i++) {
        var mi = i; o = {}; mark(o, 0, i - 1, "ok"); o[i] = "cur"; var tg = {}; tg[i] = "min";
        emit(20, "第 " + i + " 輪:先假設位置 " + i + " 的 " + a[i] + " 是最小的(<code>minIdx = " + i + "</code>)。", o, tg);
        for (j = i + 1; j < n; j++) {
          cmp++; var less = a[j] < a[mi]; o = {}; mark(o, 0, i - 1, "ok"); o[mi] = "min"; o[j] = "cur"; tg = {}; tg[mi] = "min"; tg[j] = "j";
          emit([21, 22], "比較 v[" + j + "] = " + a[j] + " 和目前最小的 v[" + mi + "] = " + a[mi] + (less ? ":更小,要更新最小的位置。" : ":沒有更小。"), o, tg);
          if (less) { mi = j; o = {}; mark(o, 0, i - 1, "ok"); o[mi] = "min"; tg = {}; tg[mi] = "min"; emit(23, "<code>minIdx = " + j + "</code>:新的最小值是 " + a[mi] + "。", o, tg); }
        }
        if (mi !== i) { var t2 = a[i]; a[i] = a[mi]; a[mi] = t2; swp++; }
        o = {}; mark(o, 0, i, "ok"); if (mi !== i) o[mi] = "mv";
        emit(26, mi !== i ? "把最小的 " + a[i] + " 和位置 " + i + " 交換,位置 " + i + " 就排好了。" : "最小的本來就在位置 " + i + ",不用動。位置 " + i + " 排好了。", o);
      }
    } else {
      emit([31, 32], "插入排序:像整理手上的撲克牌。左邊一段已經排好,每次拿下一張,<b>插進左邊正確的位置</b>。");
      for (i = 1; i < n; i++) {
        var key = a[i]; j = i - 1; o = {}; mark(o, 0, i - 1, "ok"); o[i] = "key"; tg = {}; tg[i] = "key";
        emit([33, 34], "拿起 v[" + i + "] = <b>" + key + "</b>(叫它 key),從左邊已排好的部分的最後面往前找位置。", o, tg, [["key", key]]);
        while (j >= 0) {
          cmp++; var big = a[j] > key; o = {}; mark(o, 0, i, "ok"); o[j] = "cur"; o[j + 1] = "key";
          emit(35, "比較 v[" + j + "] = " + a[j] + " 和 key = " + key + (big ? ":比 key 大,要往右讓位。" : ":不比 key 大,位置找到了。"), o, null, [["key", key]]);
          if (!big) break;
          a[j + 1] = a[j]; swp++; o = {}; mark(o, 0, i, "ok"); o[j + 1] = "mv"; emit([36, 37], "<code>v[" + (j + 1) + "] = v[" + j + "]</code>:" + a[j + 1] + " 往右搬一格。", o, null, [["key", key]]);
          j--;
        }
        a[j + 1] = key; o = {}; mark(o, 0, i, "ok"); o[j + 1] = "new";
        emit(39, "<code>v[" + (j + 1) + "] = key</code>:把 " + key + " 放進空出來的位置。左邊 " + (i + 1) + " 個都排好了。", o);
      }
    }
    o = {}; mark(o, 0, n - 1, "ok");
    emit(alg === "bubble" ? 15 : alg === "selection" ? 28 : 41, "排序完成!一共比較 <b>" + cmp + "</b> 次," + (alg === "insertion" ? "搬動" : "交換") + " <b>" + swp + "</b> 次。", o);
    return { frames: fr, result: a, cmp: cmp, swp: swp };
  }
  function parse(text) {
    var parts = String(text).split(/[\s,]+/).filter(function (x) { return x !== ""; });
    if (parts.length < 2 || parts.length > MAXN) return { error: "請輸入 2 到 " + MAXN + " 個數字,用逗號或空白分隔。" };
    var vals = parts.map(Number);
    if (!vals.every(function (x) { return isFinite(x) && Math.floor(x) === x && x >= 1 && x <= 99; })) return { error: "每個數字請是 1 到 99 的整數。" };
    return { vals: vals };
  }
  function run(alg, text) {
    var p = parse(text); if (p.error) return p; if (!NAMES[alg]) return { error: "請選一種排序法。" };
    var r = sorter(alg, p.vals, true); r.result = null; return r;
  }
  function stats(alg, arr) { var r = sorter(alg, arr, false); return { cmp: r.cmp, swp: r.swp, sorted: r.result }; }
  function make(kind, n, rnd) {
    rnd = rnd || Math.random; var a = [], i;
    for (i = 0; i < n; i++) a.push(1 + Math.floor(rnd() * 99));
    if (kind === "sorted" || kind === "reverse" || kind === "nearly") a.sort(function (x, y) { return x - y; });
    if (kind === "reverse") a.reverse();
    if (kind === "nearly") for (i = 0; i + 1 < n; i += Math.max(3, Math.floor(n / 6))) { var t = a[i]; a[i] = a[i + 1]; a[i + 1] = t; }
    return a;
  }
  A.sort = { MAXN: MAXN, CODE_SORT: CODE_SORT, NAMES: NAMES, run: run, stats: stats, parse: parse, make: make };
  if (typeof module !== "undefined" && module.exports) module.exports = A;
})(typeof window !== "undefined" ? window : globalThis);
