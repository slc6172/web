(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var M = 7, MAXK = 14;
  var CODE_HASH = [
    "using Table = std::vector<std::vector<std::string>>;", "",
    "int hashOf(const std::string& key, int m) {", "    int sum = 0;", "    for (char c : key) {", "        sum += c;", "    }", "    return sum % m;", "}", "",
    "bool contains(const Table& t, const std::string& key) {", "    int idx = hashOf(key, static_cast<int>(t.size()));", "    for (const std::string& k : t[idx]) {", "        if (k == key) {", "            return true;", "        }", "    }", "    return false;", "}", "",
    "void insert(Table& t, const std::string& key) {", "    if (contains(t, key)) {", "        return;", "    }", "    int idx = hashOf(key, static_cast<int>(t.size()));", "    t[idx].push_back(key);", "}", "",
    "void erase(Table& t, const std::string& key) {", "    int idx = hashOf(key, static_cast<int>(t.size()));", "    std::vector<std::string>& bucket = t[idx];", "    for (int i = 0; i < static_cast<int>(bucket.size()); ++i) {",
    "        if (bucket[i] == key) {", "            bucket.erase(bucket.begin() + i);", "            return;", "        }", "    }", "}"].join("\n");
  function hashOf(key, m) { var s = 0; for (var i = 0; i < key.length; i++) s += key.charCodeAt(i); return s % m; }
  function calcText(key, m) {
    var parts = key.split("").map(function (c) { return c.charCodeAt(0); }), sum = parts.reduce(function (a, b) { return a + b; }, 0);
    return 'hashOf("' + key + '") = (' + parts.join(" + ") + ") % " + m + " = " + sum + " % " + m + " = " + (sum % m);
  }
  function init() { var t = []; for (var i = 0; i < M; i++) t.push([]); return t; }
  function clone(t) { return t.map(function (c) { return c.slice(); }); }
  function count(t) { return t.reduce(function (a, c) { return a + c.length; }, 0); }
  function check(t, key, forInsert) {
    if (typeof key !== "string" || !/^[A-Za-z0-9]{1,8}$/.test(key)) return "key 請輸入 1 到 8 個英文字母或數字。";
    if (forInsert && count(t) >= MAXK) return "示範最多放 " + MAXK + " 個 key,請按 Reset 重新開始。";
    return null;
  }
  function frame(t, cur, cls, line, msg, o) {
    o = o || {}; var n = count(t), mx = Math.max.apply(null, t.map(function (c) { return c.length; }));
    return { buckets: t.map(function (chain, b) { return chain.map(function (k, i) { return { k: k, cls: (cls && cls[b + ":" + i]) || "" }; }); }), cur: cur, calc: o.calc || "",
      chips: [["元素個數", n], ["負載因子 n/m", (n / M).toFixed(2)], ["最長的鏈", mx], ["比較字串次數", o.cmp || 0]], line: line, msg: msg };
  }
  /* 在 idx 桶子裡逐一比對 key;回傳 {found, frames 已 push 到 fr} */
  function scan(t, idx, key, fr, cmp0, linesCompare, lineFoundRet, lineEnd, calc, okMsgFound) {
    var chain = t[idx], cmp = cmp0, found = -1;
    for (var i = 0; i < chain.length; i++) {
      cmp++; var same = chain[i] === key, c = {}; c[idx + ":" + i] = same ? "ok" : "cur";
      fr.push(frame(t, idx, c, linesCompare, "比較桶子 " + idx + " 的第 " + i + " 個:<code>\"" + chain[i] + "\" == \"" + key + "\"</code>?" + (same ? "<b>相同</b>。" : "不同,看下一個。"), { calc: calc, cmp: cmp }));
      if (same) { found = i; break; }
    }
    return { found: found, cmp: cmp };
  }
  function insert(t0, key) {
    var e = check(t0, key, true); if (e) return { error: e };
    var t = clone(t0), fr = [], idx = hashOf(key, M), calc = calcText(key, M);
    fr.push(frame(t, -1, null, 21, "<code>insert(\"" + key + "\")</code>:要放進雜湊表。第一步,算出它該放哪個桶子。"));
    fr.push(frame(t, idx, null, [4, 8], "<b>雜湊函數</b>:把每個字元的編號加起來,再除以桶子數 " + M + " 取餘數,得到 <b>桶子 " + idx + "</b>。", { calc: calc }));
    var chain = t[idx], r = { found: -1, cmp: 0 };
    if (chain.length === 0) fr.push(frame(t, idx, null, [22, 11], "<code>contains</code>:桶子 " + idx + " 是空的,不可能有重複。", { calc: calc }));
    else {
      r = scan(t, idx, key, fr, 0, [13, 14], 15, 18, calc);
      if (r.found >= 0) { fr[fr.length - 1].msg += "key 已經存在,<code>return</code>,不重複放入。"; fr[fr.length - 1].line = [14, 15, 23]; return { frames: fr, result: t }; }
      fr.push(frame(t, idx, null, [18, 22], "整條鏈都比完了,沒有相同的 key,可以放進去。", { calc: calc, cmp: r.cmp }));
    }
    var collide = chain.length > 0, before = chain.slice(); chain.push(key); var c = {}; c[idx + ":" + (chain.length - 1)] = "new";
    fr.push(frame(t, idx, c, [25, 26], collide ? "<b>碰撞!</b>桶子 " + idx + " 已經有 " + before.map(function (x) { return "<code>" + x + "</code>"; }).join("、") + ",新的 key 接在這條鏈的後面(<b>chaining</b>)。" : "桶子 " + idx + " 是空的,直接放進去。", { calc: calc, cmp: r.cmp }));
    return { frames: fr, result: t };
  }
  function contains(t0, key) {
    var e = check(t0, key, false); if (e) return { error: e };
    var t = clone(t0), fr = [], idx = hashOf(key, M), calc = calcText(key, M);
    fr.push(frame(t, -1, null, 11, "<code>contains(\"" + key + "\")</code>:要查有沒有這個 key。不用從頭找整個表,先算桶子。"));
    fr.push(frame(t, idx, null, [12, 4, 8], "雜湊函數算出 <b>桶子 " + idx + "</b>,只需要去那一個桶子找。", { calc: calc }));
    if (t[idx].length === 0) { fr.push(frame(t, idx, null, 18, "桶子 " + idx + " 是空的,一定沒有。回傳 <b>false</b>。比較了 0 次。", { calc: calc })); return { frames: fr, result: t }; }
    var r = scan(t, idx, key, fr, 0, [13, 14], 15, 18, calc);
    var last = fr[fr.length - 1];
    if (r.found >= 0) { last.line = [14, 15]; last.msg += "回傳 <b>true</b>,一共比較 " + r.cmp + " 次。"; }
    else fr.push(frame(t, idx, null, 18, "這條鏈都比完了,沒有。回傳 <b>false</b>,一共比較 " + r.cmp + " 次。", { calc: calc, cmp: r.cmp }));
    return { frames: fr, result: t };
  }
  function erase(t0, key) {
    var e = check(t0, key, false); if (e) return { error: e };
    var t = clone(t0), fr = [], idx = hashOf(key, M), calc = calcText(key, M);
    fr.push(frame(t, -1, null, 29, "<code>erase(\"" + key + "\")</code>:要刪掉這個 key。先算桶子。"));
    fr.push(frame(t, idx, null, [30, 31], "雜湊函數算出 <b>桶子 " + idx + "</b>。<code>bucket</code> 指向這個桶子裡的那條鏈。", { calc: calc }));
    var r = scan(t, idx, key, fr, 0, [32, 33], 34, 38, calc);
    if (r.found < 0) { fr.push(frame(t, idx, null, 38, "整條鏈都找過了,沒有這個 key,什麼也不做。", { calc: calc, cmp: r.cmp })); return { frames: fr, result: t }; }
    var c = {}; c[idx + ":" + r.found] = "del"; fr.push(frame(t, idx, c, 34, "<code>bucket.erase(...)</code>:把它從鏈裡拿掉。", { calc: calc, cmp: r.cmp }));
    t[idx].splice(r.found, 1);
    fr.push(frame(t, idx, null, 35, "已刪除。平均只要比較鏈上少數幾個,所以是 <b>O(1)</b>。", { calc: calc, cmp: r.cmp }));
    return { frames: fr, result: t };
  }
  function run(op, t, key) { return op === "insert" ? insert(t, key) : op === "contains" ? contains(t, key) : op === "erase" ? erase(t, key) : { error: "請選一個操作。" }; }
  function fill(keys) { var t = init(); keys.forEach(function (k) { if (t[hashOf(k, M)].indexOf(k) < 0) t[hashOf(k, M)].push(k); }); return t; }
  A.hash = { M: M, MAXK: MAXK, CODE_HASH: CODE_HASH, hashOf: hashOf, init: init, run: run, fill: fill, idle: function (t) { return frame(t, -1, null, undefined, ""); } };
  if (typeof module !== "undefined" && module.exports) module.exports = A;
})(typeof window !== "undefined" ? window : globalThis);
