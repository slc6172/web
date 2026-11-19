/* Node 測試:algo 純函式的最終結果、frame 的程式碼行號範圍,並檢查程式碼面板文字與 cpp/ 原始檔一致 */
const fs = require("fs"), path = require("path"), assert = require("assert");
globalThis.window = undefined;
const dir = path.join(__dirname, "algo");
const only = process.argv.slice(2);
require(path.join(dir, "core.js"));
fs.readdirSync(dir).filter(f => /^alg_.*\.js$/.test(f)).forEach(f => require(path.join(dir, f)));
const A = globalThis.Algo;
let n = 0; const ok = (c, m) => { assert(c, m); n++; };
const nlines = s => s.split("\n").length;
function checkFrames(fr, code, tag) {
  const L = nlines(code);
  fr.forEach((f, i) => [].concat(f.line === undefined ? [] : f.line).forEach(x => ok(x >= 1 && x <= L, tag + " frame " + i + " line " + x + " 超出 1.." + L)));
}
function codeInFile(code, file) {
  const src = fs.readFileSync(path.join(__dirname, "cpp", file), "utf8").split("\n").map(s => s.trimEnd());
  let at = 0;
  code.split("\n").forEach(line => { if (!line.trim()) return; const j = src.findIndex((s, k) => k >= at && s === line.trimEnd()); ok(j >= 0, file + " 找不到程式碼行: " + line); at = j + 1; });
}

/* ---- array / vector ---- */
if (A.vec) {
  codeInFile(A.vec.CODE_EDIT, "array_edit.cpp");
  codeInFile(A.vec.CODE_GROW.split("\n").map(s => "    " + s).join("\n").replace(/^ {4}/, "    "), "array_grow.cpp");
  let seed = 7; const rnd = m => (seed = (seed * 1103515245 + 12345) & 0x7fffffff) % m;
  for (let t = 0; t < 300; t++) {
    const len = rnd(10), arr = Array.from({ length: len }, () => rnd(100)), val = rnd(100);
    const pos = rnd(len + 1), r = A.vec.insert(arr, pos, val), exp = arr.slice(); exp.splice(pos, 0, val);
    ok(JSON.stringify(r.result) === JSON.stringify(exp), "insert 結果");
    ok(r.frames[r.frames.length - 1].chips[1][1] === len - pos, "insert 搬動次數 = n - pos");
    checkFrames(r.frames, A.vec.CODE_EDIT, "insert");
    if (len > 0) {
      const p2 = rnd(len), e = A.vec.erase(arr, p2), ex = arr.slice(); ex.splice(p2, 1);
      ok(JSON.stringify(e.result) === JSON.stringify(ex), "erase 結果");
      ok(e.frames[e.frames.length - 1].chips[1][1] === len - 1 - p2, "erase 搬動次數 = n - 1 - pos");
      checkFrames(e.frames, A.vec.CODE_EDIT, "erase");
    }
  }
  ok(A.vec.insert(new Array(10).fill(1), 0, 1).error, "滿了要報錯"); ok(A.vec.insert([1], 5, 1).error, "越界報錯");
  ok(A.vec.insert([1], 0, 100).error, "數值範圍"); ok(A.vec.erase([], 0).error, "空 vector 刪除報錯");
  let b = A.vec.growInit(), caps = [];
  for (let i = 0; i < 9; i++) { const r = A.vec.push(b, 1); checkFrames(r.frames, A.vec.CODE_GROW, "grow"); b = r.result; caps.push(b.cap); }
  ok(JSON.stringify(caps) === "[1,2,4,4,8,8,8,8,16]", "capacity 序列與 g++ 實際輸出一致: " + caps);
  ok(b.grows === 5 && b.copies === 15, "擴容 5 次、累計複製 15 次: " + b.grows + "," + b.copies);
  const g = fs.readFileSync(path.join(__dirname, "out", "array_grow.txt"), "utf8").trim().split("\n").map(l => +l.split(" ")[1]);
  ok(JSON.stringify(g) === JSON.stringify(caps), "與 g++ 實測 capacity 序列相同");
  ok(A.vec.push(A.vec.growInit(), 17).error && A.vec.push(b, 9).error, "超出上限報錯");
}

/* ---- pointer / node ---- */
if (A.ptr) {
  codeInFile(A.ptr.CODE_PTR, "prereq_ptr.cpp"); codeInFile(A.ptr.CODE_NODE, "prereq_node.cpp");
  const fp = A.ptr.framesPtr(); checkFrames(fp, A.ptr.CODE_PTR, "ptr");
  const last = fp[fp.length - 1].vars; ok(last[0].v === 30 && last[1].v === 99 && last[3].to === "y", "ptr 最終狀態 x=30 y=99 p→y");
  ok(fs.readFileSync(path.join(__dirname, "out", "prereq_ptr.txt"), "utf8").trim() === "30 99", "與實際輸出一致");
  const fn = A.ptr.framesNode(); checkFrames(fn, A.ptr.CODE_NODE, "node");
  ok(fn[fn.length - 1].heap.every(h => h.cls === "freed"), "兩個節點最後都 delete");
}

/* ---- count / curves ---- */
if (A.count) {
  codeInFile(A.count.CODE_COUNT, "bigo_count.cpp");
  for (let n = 1; n <= 8; n++) {
    ["a", "b", "c"].forEach(p => { const r = A.count.count(p, n); checkFrames(r.frames, A.count.CODE_COUNT, "count" + p);
      const exp = p === "a" ? n : p === "b" ? n * n : Math.floor(Math.log2(n)); ok(r.result.ops === exp, "count " + p + " n=" + n + " ops=" + r.result.ops); });
  }
  ok(A.count.count("c", 64).result.ops === 6, "halving 64 → 6"); ok(A.count.count("b", 9).error && A.count.count("a", 0).error, "限制報錯");
  ok(fs.readFileSync(path.join(__dirname, "out", "bigo_count.txt"), "utf8").trim() === "8 64 3", "與 g++ 輸出一致(n=8)");
  const c8 = [A.count.count("a", 8).result.ops, A.count.count("b", 8).result.ops, A.count.count("c", 8).result.ops].join(" "); ok(c8 === "8 64 3", "n=8 的三個次數");
}
if (A.curves) {
  const c = A.curves.counts(10); ok(c.n === 10 && c.n2 === 100 && c.exp === 1024 && Math.abs(c.log - 3.3219) < 1e-3, "counts(10)");
  ok(A.curves.fmtTime(1e6) === "1 秒" || A.curves.fmtTime(1e6).indexOf("秒") > 0, "fmtTime 秒"); ok(A.curves.fmtTime(Math.pow(2, 100)).indexOf("宇宙") > 0, "2^100 微秒超過宇宙年齡");
  ok(A.curves.fmtNum(1.27e30).indexOf("10<sup>30") > 0, "fmtNum 科學記號");
}

/* ---- linked list ---- */
if (A.list) {
  codeInFile(A.list.CODE_LIST, "linked_ops.cpp");
  let seed = 11; const rnd = m => (seed = (seed * 1103515245 + 12345) & 0x7fffffff) % m, J = JSON.stringify;
  for (let t = 0; t < 400; t++) {
    const len = rnd(6), arr = Array.from({ length: len }, () => rnd(100)), v = rnd(100);
    let r = A.list.pushFront(arr, v);
    if (len < 6) { ok(J(r.result) === J([v].concat(arr)), "pushFront"); checkFrames(r.frames, A.list.CODE_LIST, "pushFront"); ok(r.frames[r.frames.length - 1].chips[1][1] === 2, "pushFront 改 2 個指標");
      r = A.list.pushBack(arr, v); ok(J(r.result) === J(arr.concat([v])), "pushBack"); checkFrames(r.frames, A.list.CODE_LIST, "pushBack"); ok(r.frames[r.frames.length - 1].chips[2][1] === len, "pushBack 走訪 n 個"); }
    if (len >= 1 && len < 6) { const k = rnd(len); r = A.list.insertAfter(arr, k, v); const e = arr.slice(); e.splice(k + 1, 0, v); ok(J(r.result) === J(e), "insertAfter"); checkFrames(r.frames, A.list.CODE_LIST, "insertAfter"); }
    if (len >= 1) { r = A.list.eraseFront(arr); ok(J(r.result) === J(arr.slice(1)), "eraseFront"); checkFrames(r.frames, A.list.CODE_LIST, "eraseFront"); }
    if (len >= 2) { const k = rnd(len - 1); r = A.list.eraseAfter(arr, k); const e = arr.slice(); e.splice(k + 1, 1); ok(J(r.result) === J(e), "eraseAfter"); checkFrames(r.frames, A.list.CODE_LIST, "eraseAfter");
      r.frames.forEach(f => f.nodes.forEach(nd => ok(typeof nd.slot === "number" && (nd.row === 0 || nd.row === 1), "節點位置"))); }
  }
  ok(A.list.pushFront(new Array(6).fill(1), 1).error && A.list.eraseFront([]).error && A.list.insertAfter([], 0, 1).error && A.list.eraseAfter([1], 0).error && A.list.insertAfter([1, 2], 5, 1).error, "錯誤輸入報錯");
}

/* ---- stack / queue / bracket ---- */
if (A.sq) {
  codeInFile(A.sq.CODE_STACK, "sq_stack.cpp"); codeInFile(A.sq.CODE_QUEUE, "sq_queue.cpp"); codeInFile(A.sq.CODE_BRACKET, "sq_balance.cpp");
  let seed = 5; const rnd = m => (seed = (seed * 1103515245 + 12345) & 0x7fffffff) % m, J = JSON.stringify;
  let st = [], ref = [];
  for (let t = 0; t < 300; t++) {
    if (rnd(2) && st.length < A.sq.MAXS) { const v = rnd(100), r = A.sq.stackPush(st, v); st = r.result; ref.push(v); checkFrames(r.frames, A.sq.CODE_STACK, "push"); }
    else if (st.length) { const r = A.sq.stackPop(st); ok(r.frames[r.frames.length - 1].chips.some(c => c[1] === ref[ref.length - 1]), "pop 取出的是最後放進去的"); ref.pop(); st = r.result; checkFrames(r.frames, A.sq.CODE_STACK, "pop"); }
    ok(J(st) === J(ref), "stack 內容");
  }
  let q = A.sq.queueInit(), qref = [], pushed = 0;
  for (let t = 0; t < 300; t++) {
    if (rnd(2) && q.data.length < A.sq.MAXQ) { const v = rnd(100), r = A.sq.queuePush(q, v); q = r.result; qref.push(v); checkFrames(r.frames, A.sq.CODE_QUEUE, "qpush"); }
    else if (q.head < q.data.length) { const r = A.sq.queuePop(q); ok(r.frames[r.frames.length - 1].chips.some(c => c[1] === qref[0]), "queue 取出最先放進去的"); qref.shift(); q = r.result; checkFrames(r.frames, A.sq.CODE_QUEUE, "qpop"); }
    ok(J(q.data.slice(q.head)) === J(qref), "queue 內容");
  }
  const exp = s => { const m = { ")": "(", "]": "[", "}": "{" }, k = []; for (const c of s) { if ("([{".includes(c)) k.push(c); else if (m[c]) { if (k.pop() !== m[c]) return false; } } return k.length === 0; };
  const out = fs.readFileSync(path.join(__dirname, "out", "sq_balance.txt"), "utf8").trim().split("\n");
  ["{[()]}", "([)]", "((())", "())", "a(b)c", "", "((", "]", "{[}]", "a1b2"].forEach(s => { if (!s) return; const r = A.sq.balance(s); ok(r.result === exp(s), "balance " + s); checkFrames(r.frames, A.sq.CODE_BRACKET, "balance " + s); });
  ["{[()]}", "([)]", "((())", "())", "a(b)c"].forEach((s, i) => ok(out[i] === s + " -> " + (A.sq.balance(s).result ? "balanced" : "not balanced"), "與 g++ 輸出一致 " + s));
  ok(A.sq.balance("").error && A.sq.balance("a b").error && A.sq.stackPop([]).error && A.sq.queuePop(A.sq.queueInit()).error, "錯誤輸入");
}

/* ---- search ---- */
if (A.search) {
  codeInFile(A.search.CODE_SEARCH, "search_ops.cpp");
  let seed = 3; const r01 = () => ((seed = (seed * 1103515245 + 12345) & 0x7fffffff) % 10000) / 10000;
  for (let t = 0; t < 300; t++) {
    const n = 1 + Math.floor(r01() * 15), arr = A.search.randomSorted(n, r01), tg = Math.floor(r01() * 100);
    ok(arr.every((x, i) => i === 0 || arr[i - 1] < x), "已排序且不重複");
    const L = A.search.linear(arr, tg), B = A.search.binary(arr, tg), idx = arr.indexOf(tg);
    ok(L.found === idx && B.found === idx, "找到的索引正確 " + arr + " t=" + tg);
    checkFrames(L.frames, A.search.CODE_SEARCH, "linear"); checkFrames(B.frames, A.search.CODE_SEARCH, "binary");
    ok(B.comparisons <= Math.floor(Math.log2(n)) + 1, "二分最多 floor(log2 n)+1 次");
    ok(L.comparisons === (idx === -1 ? n : idx + 1), "線性比較次數");
  }
  const v = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91], o = fs.readFileSync(path.join(__dirname, "out", "search_ops.txt"), "utf8").trim().split("\n");
  ok(o[0] === A.search.linear(v, 23).found + " " + A.search.binary(v, 23).found && o[1] === A.search.linear(v, 7).found + " " + A.search.binary(v, 7).found, "與 g++ 輸出一致");
  ok(A.search.worst(1000000).binary === 20 && A.search.worst(1024).binary === 11 && A.search.worst(1).binary === 1, "worst");
  ok(A.search.linear([], 1).error && A.search.binary([1], 200).error, "錯誤輸入");
}

/* ---- recursion ---- */
if (A.rec) {
  codeInFile(A.rec.CODE_REC, "rec_basic.cpp");
  const F = n => n <= 1 ? 1 : n * F(n - 1), Fb = n => n <= 1 ? n : Fb(n - 1) + Fb(n - 2);
  for (let n = 1; n <= 8; n++) { const r = A.rec.run("fact", n); ok(r.value === F(n) && r.calls === n, "fact " + n); checkFrames(r.frames, A.rec.CODE_REC, "fact"); }
  for (let n = 1; n <= 6; n++) {
    const r = A.rec.run("fib", n); ok(r.value === Fb(n), "fib " + n); ok(r.calls === A.rec.fibCalls(n), "fib 呼叫次數 " + n + ": " + r.calls); checkFrames(r.frames, A.rec.CODE_REC, "fib");
    ok(r.dups === r.calls - (n <= 1 ? 1 : n + 1), "重複呼叫 = 總呼叫 - 不同的 n 個數(" + n + ")");
    r.frames.forEach(f => { ok(f.tree.root !== null && f.stack.length >= 0, "frame 結構"); });
  }
  const o = fs.readFileSync(path.join(__dirname, "out", "rec_fibcount.txt"), "utf8").trim().split("\n");
  [10, 20, 30].forEach((n, i) => ok(o[i] === "fib(" + n + ") = " + Fb(n) + ", calls = " + A.rec.fibCalls(n), "與 g++ 輸出一致 fib(" + n + ")"));
  ok(fs.readFileSync(path.join(__dirname, "out", "rec_basic.txt"), "utf8").trim() === F(5) + " " + Fb(6), "rec_basic 輸出");
  ok(A.rec.run("fib", 7).error && A.rec.run("fact", 0).error && A.rec.run("x", 3).error, "錯誤輸入");
}

/* ---- sort(basic) ---- */
if (A.sort) {
  codeInFile(A.sort.CODE_SORT, "sort_basic.cpp");
  let seed = 9; const r01 = () => ((seed = (seed * 1103515245 + 12345) & 0x7fffffff) % 10000) / 10000, J = JSON.stringify;
  ["bubble", "selection", "insertion"].forEach(alg => {
    for (let t = 0; t < 200; t++) {
      const n = 2 + Math.floor(r01() * 9), kind = ["random", "sorted", "reverse", "nearly"][t % 4], arr = A.sort.make(kind, n, r01);
      const r = A.sort.run(alg, arr.join(","));
      ok(J(r.frames[r.frames.length - 1].vals) === J(arr.slice().sort((a, b) => a - b)), alg + " 結果排序正確 " + arr);
      checkFrames(r.frames, A.sort.CODE_SORT, alg);
      const st = A.sort.stats(alg, arr); ok(st.cmp === r.cmp && st.swp === r.swp && J(st.sorted) === J(arr.slice().sort((a, b) => a - b)), "stats 與 frames 一致");
      r.frames.forEach(f => ok(f.vals.length === n && f.cls.length === n && f.tags.length === n, "frame 長度"));
    }
    const n = 8, sorted = [1, 2, 3, 4, 5, 6, 7, 8], rev = [8, 7, 6, 5, 4, 3, 2, 1], tri = n * (n - 1) / 2;
    const s1 = A.sort.stats(alg, sorted), s2 = A.sort.stats(alg, rev);
    if (alg === "bubble") { ok(s1.cmp === n - 1 && s1.swp === 0, "bubble 已排序:n-1 次比較、0 交換(提早結束)"); ok(s2.cmp === tri && s2.swp === tri, "bubble 反向:n(n-1)/2"); }
    if (alg === "selection") { ok(s1.cmp === tri && s2.cmp === tri, "selection 比較永遠 n(n-1)/2"); ok(s1.swp === 0 && s2.swp === n / 2, "selection 交換次數"); }
    if (alg === "insertion") { ok(s1.cmp === n - 1 && s1.swp === 0, "insertion 已排序:n-1 次比較"); ok(s2.cmp === tri && s2.swp === tri, "insertion 反向:n(n-1)/2"); }
  });
  const out = fs.readFileSync(path.join(__dirname, "out", "sort_basic.txt"), "utf8").trim().split("\n");
  ["bubble", "selection", "insertion"].forEach((alg, i) => ok(out[i].trim() === A.sort.run(alg, "5,2,9,1,7,3").frames.slice(-1)[0].vals.join(" "), "與 g++ 輸出一致 " + alg));
  ok(A.sort.run("bubble", "5").error && A.sort.run("bubble", "1,2,300").error && A.sort.run("x", "3,2,1").error && A.sort.run("bubble", "1,2,3,4,5,6,7,8,9,10,11").error, "錯誤輸入");
}

/* ---- sort(advanced) ---- */
if (A.sortadv) {
  codeInFile(A.sortadv.CODE_ADV, "sortadv_ops.cpp");
  let seed = 21; const r01 = () => ((seed = (seed * 1103515245 + 12345) & 0x7fffffff) % 10000) / 10000, J = JSON.stringify;
  ["merge", "quick"].forEach(alg => {
    for (let t = 0; t < 250; t++) {
      const n = 2 + Math.floor(r01() * 9), arr = A.sort.make(["random", "sorted", "reverse", "nearly"][t % 4], n, r01), r = A.sortadv.run(alg, arr.join(","));
      const last = r.frames[r.frames.length - 1], fin = last.vals || last.rows[0].vals;
      ok(J(fin) === J(arr.slice().sort((a, b) => a - b)), alg + " 結果排序正確 " + arr);
      checkFrames(r.frames, A.sortadv.CODE_ADV, alg);
      const st = A.sortadv.stats(alg, arr); ok(st.cmp === r.cmp && J(st.sorted) === J(arr.slice().sort((a, b) => a - b)), "stats 一致");
    }
  });
  /* 與 g++ 實測的比較次數一致(同一組偽亂數) */
  const mk = (n, sorted) => { const v = []; let x = 12345; for (let i = 0; i < n; i++) { x = (Math.imul(x, 1103515245) + 12345) >>> 0; v.push(sorted ? i : (x >>> 16) % 10000); } return v; };
  const o = fs.readFileSync(path.join(__dirname, "out", "sortadv_count.txt"), "utf8").trim().split("\n").map(l => +l.split(":")[1]);
  ok(A.sortadv.stats("merge", mk(2000, false)).cmp === o[1], "merge 比較次數與 g++ 一致 " + o[1]);
  ok(A.sortadv.stats("quick", mk(2000, false)).cmp === o[2], "quick 隨機 比較次數與 g++ 一致 " + o[2]);
  ok(A.sortadv.stats("quick", mk(2000, true)).cmp === o[3], "quick 已排序 比較次數與 g++ 一致 " + o[3] + " (= n(n-1)/2)");
  ok(o[0] === 2000 * 1999 / 2, "bubble 無提早結束版 = n(n-1)/2");
  const so = fs.readFileSync(path.join(__dirname, "out", "sortadv_ops.txt"), "utf8").trim().split("\n");
  ok(so[0].trim() === J([38, 27, 43, 3, 9, 82, 10].slice().sort((a, b) => a - b)).replace(/[\[\]]/g, "").split(",").join(" "), "與 g++ 輸出一致");
  ok(A.sortadv.run("merge", "5").error && A.sortadv.run("x", "3,1").error, "錯誤輸入");
}

/* ---- hash ---- */
if (A.hash) {
  codeInFile(A.hash.CODE_HASH, "hash_ops.cpp");
  const H = A.hash, J = JSON.stringify;
  const g = H.fill(["cat", "act", "dog", "god", "bird"]);
  const o = fs.readFileSync(path.join(__dirname, "out", "hash_ops.txt"), "utf8").trim().split("\n");
  g.forEach((chain, b) => ok(o[b] === b + ":" + chain.map(k => " " + k).join(""), "與 g++ 輸出一致 桶子 " + b));
  ok(H.hashOf("cat", 7) === 4 && H.hashOf("act", 7) === 4 && H.hashOf("bird", 7) === 4 && H.hashOf("dog", 7) === 6, "雜湊值");
  let seed = 4; const rnd = m => (seed = (seed * 1103515245 + 12345) & 0x7fffffff) % m;
  const words = ["cat", "act", "tac", "dog", "god", "bird", "a", "b", "xyz", "Zz9"];
  let t = H.init(), ref = new Set();
  for (let i = 0; i < 400; i++) {
    const w = words[rnd(words.length)], op = ["insert", "contains", "erase"][rnd(3)];
    const r = H.run(op, t, w);
    if (r.error) { ok(op === "insert" && ref.size >= H.MAXK, "只有滿了才會報錯"); t = H.init(); ref = new Set(); continue; }
    checkFrames(r.frames, H.CODE_HASH, op);
    if (op === "insert") ref.add(w); if (op === "erase") ref.delete(w);
    t = r.result;
    ok(t.every((chain, b) => chain.every(k => H.hashOf(k, 7) === b)), "每個 key 都在正確的桶子");
    ok([].concat(...t).sort().join() === [...ref].sort().join(), "內容與 Set 一致");
    const c = H.run("contains", t, w); ok(c.frames[c.frames.length - 1].msg.includes(ref.has(w) ? "true" : "false"), "contains 結果 " + w);
  }
  ok(H.run("insert", H.init(), "a b").error && H.run("insert", H.init(), "").error && H.run("insert", H.init(), "abcdefghi").error && H.run("x", H.init(), "a").error, "錯誤輸入");
  ok(fs.readFileSync(path.join(__dirname, "out", "hash_ops.txt"), "utf8").trim().split("\n").slice(7).join("|") === "10|01", "contains/erase 結果");
}

/* ---- tree traversal ---- */
if (A.tree) {
  codeInFile(A.tree.CODE_TREE, "tree_traverse.cpp");
  const T = A.tree, J = JSON.stringify;
  const o = fs.readFileSync(path.join(__dirname, "out", "tree_traverse.txt"), "utf8").trim().split("\n");
  ["pre", "in", "post", "level"].forEach((m, i) => ok(o[i].trim() === T.run(m, "full").out.join(" "), "與 g++ 輸出一致 " + m));
  Object.keys(T.PRESETS).forEach(k => ["pre", "in", "post", "level"].forEach(m => {
    const r = T.run(m, k); ok(J(r.out) === J(T.expected(m, T.PRESETS[k].tree)), k + " " + m + " 順序正確"); checkFrames(r.frames, T.CODE_TREE, k + m);
    r.frames.forEach(f => ok(f.tree.root && f.out.length <= r.out.length, "frame"));
  }));
  ok(T.run("pre", "x").error && T.run("x", "full").error, "錯誤輸入");
}
/* ---- BST ---- */
if (A.bst) {
  const B = A.bst, J = JSON.stringify;
  codeInFile(B.CODE_BST, "bst_ops.cpp"); ok(nlines(B.CODE_BST) === 63, "程式碼面板 63 行");
  /* 與 g++ 實際輸出逐行比對 */
  const o = fs.readFileSync(path.join(__dirname, "out", "bst_ops.txt"), "utf8").trim().split("\n");
  let b = B.fromList([5, 3, 8, 1, 4, 7, 9, 2, 6]);
  ok(o[0].replace("inorder:", "").trim() === B.inorder(b).join(" "), "inorder 與 g++ 一致");
  ok(o[1].replace("preorder:", "").trim() === B.preorder(b).join(" "), "preorder 與 g++ 一致");
  let k = 3;
  [2, 7, 3, 5].forEach(v => {
    const r = B.run("erase", v, b); b = r.result; checkFrames(r.frames, B.CODE_BST, "erase" + v);
    ok(o[k++].split(":")[1].trim() === B.preorder(b).join(" "), "erase " + v + " 的 preorder 與 g++ 一致");
  });
  ok(o[7].replace("inorder:", "").trim() === B.inorder(b).join(" "), "最後 inorder 與 g++ 一致");
  /* 退化:高度 3 對 7 */
  const dg = fs.readFileSync(path.join(__dirname, "out", "bst_degenerate.txt"), "utf8").trim().split("\n");
  ok(dg[0].endsWith("height " + B.height(B.fromList([4, 2, 6, 1, 3, 5, 7]))) && dg[1].endsWith("height " + B.height(B.fromList([1, 2, 3, 4, 5, 6, 7]))), "高度與 g++ 一致");
  /* 隨機:與獨立的參考實作比對結構 */
  const RI = (t, v) => { if (!t) return [v, null, null]; if (v < t[0]) t[1] = RI(t[1], v); else if (v > t[0]) t[2] = RI(t[2], v); return t; };
  const RM = t => { while (t[1]) t = t[1]; return t; };
  const RE = (t, v) => { if (!t) return null; if (v < t[0]) t[1] = RE(t[1], v); else if (v > t[0]) t[2] = RE(t[2], v); else { if (!t[1]) return t[2]; if (!t[2]) return t[1]; const s = RM(t[2]); t[0] = s[0]; t[2] = RE(t[2], s[0]); } return t; };
  const RS = t => t ? "(" + t[0] + " " + RS(t[1]) + " " + RS(t[2]) + ")" : ".";
  let seed = 11; const rnd = m => (seed = (seed * 1103515245 + 12345) & 0x7fffffff) % m;
  let ref = null, t = B.init(), errs = 0, ids = 0;
  for (let i = 0; i < 1500; i++) {
    const op = ["insert", "insert", "search", "erase", "erase"][rnd(5)], v = 1 + rnd(20);
    const r = B.run(op, v, t);
    if (r.error) { ok(op === "insert", "只有 insert 會報錯"); errs++; if (B.count(t) >= B.MAXN) { ref = null; t = B.init(); } continue; }
    checkFrames(r.frames, B.CODE_BST, op);
    r.frames.forEach(f => ok(f.tree && f.chips.length === 3, "frame 結構"));
    if (op === "insert") ref = RI(ref, v); if (op === "erase") ref = RE(ref, v);
    t = r.result;
    ok(B.shape(t) === RS(ref), op + " " + v + " 結構與參考實作相同: " + B.shape(t) + " vs " + RS(ref));
    const io = B.inorder(t); ok(io.every((x, j) => j === 0 || io[j - 1] < x), "中序嚴格遞增");
    if (op === "search") ok(r.found === io.includes(v) && r.frames[r.frames.length - 1].msg.includes(r.found ? "找到了" : "不在這棵樹裡"), "search 結果");
    ok(B.count(t) <= B.MAXN, "節點數上限");
    const ids2 = []; (function g(n) { if (n) { ids2.push(n.id); g(n.l); g(n.r); } })(t.root); ok(new Set(ids2).size === ids2.length, "id 唯一");
  }
  ok(errs > 0, "有測到重複或滿了的錯誤");
  ok(B.run("insert", 5, B.fromList([5])).error && B.run("insert", 0, B.init()).error && B.run("insert", 1.5, B.init()).error && B.run("insert", NaN, B.init()).error && B.run("x", 1, B.init()).error, "錯誤輸入");
  ok(B.run("insert", 11, B.fromList([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])).error, "滿了要報錯");
  /* 三種刪除情況各至少有一次,兩子節點的 frame 會經過「抄值」那一行 */
  const base = B.fromList([4, 2, 6, 1, 3, 5, 7]);
  ok(B.run("erase", 1, base).frames.some(f => [].concat(f.line).includes(50)), "葉:delete 行");
  ok(B.run("erase", 2, B.fromList([4, 2, 1])).frames.some(f => [].concat(f.line).includes(55)), "只有左子:delete 行");
  const e2 = B.run("erase", 4, base); ok([59, 60, 62].every(L => e2.frames.some(f => [].concat(f.line).includes(L))), "兩子節點經過 59/60/62");
  ok(B.preorder(e2.result).join(" ") === "5 2 1 3 6 7", "刪根 4:後繼 5 頂上來");
  ok(B.run("erase", 99, base).removed === false && B.preorder(B.run("erase", 99, base).result).join() === B.preorder(base).join(), "刪不存在的值,樹不變");
}
/* ---- heap ---- */
if (A.heap) {
  const H = A.heap;
  codeInFile(H.CODE_HEAP, "heap_ops.cpp");
  const o = fs.readFileSync(path.join(__dirname, "out", "heap_ops.txt"), "utf8").trim().split("\n");
  let h = H.init();
  [5, 3, 8, 1, 9, 2].forEach((v, i) => { const r = H.run("push", v, h); h = r.result; checkFrames(r.frames, H.CODE_HEAP, "push"); ok(o[i].split(":")[1].trim() === h.join(" "), "push " + v + " 與 g++ 一致"); });
  [[6, 9], [7, 8]].forEach(([k, top]) => { const r = H.run("pop", 0, h); h = r.result; ok(r.popped === top && o[k].split(":")[1].trim() === h.join(" "), "pop 與 g++ 一致"); checkFrames(r.frames, H.CODE_HEAP, "pop"); });
  const rest = []; while (h.length) { const r = H.run("pop", 0, h); rest.push(r.popped); h = r.result; }
  ok(o[8].split(":")[1].trim() === rest.join(" "), "依序取出與 g++ 一致");
  ok(H.fromList([5, 3, 8, 1, 9, 2]).join(" ") === "9 8 5 1 3 2", "fromList 與 push 結果一致");
  let seed = 5; const rnd = m => (seed = (seed * 1103515245 + 12345) & 0x7fffffff) % m;
  let ref = []; h = H.init();
  for (let i = 0; i < 1500; i++) {
    const op = rnd(5) < 3 ? "push" : "pop", v = 1 + rnd(30), r = H.run(op, v, h);
    if (r.error) { ok((op === "push" && h.length >= H.MAXN) || (op === "pop" && h.length === 0), "只有滿了或空了才報錯"); continue; }
    checkFrames(r.frames, H.CODE_HEAP, op); r.frames.forEach(f => ok(f.tree && f.cells.length === f.arr.length && f.chips.length >= 1, "frame 結構"));
    if (op === "push") ref.push(v); else { const m = Math.max(...ref); ok(r.popped === m, "pop 是最大值"); ref.splice(ref.indexOf(m), 1); }
    h = r.result; ok(H.isHeap(h), "堆積性質"); ok(h.slice().sort((a, b) => a - b).join() === ref.slice().sort((a, b) => a - b).join(), "內容與參考一致");
  }
  ok(H.run("push", 0, []).error && H.run("push", 1.5, []).error && H.run("pop", 0, []).error && H.run("x", 1, []).error && H.run("push", 1, new Array(10).fill(1)).error, "錯誤輸入");
}
/* ---- graph(迷宮 BFS/DFS、圖的表示) ---- */
if (A.graph) {
  const Gr = A.graph;
  codeInFile(Gr.CODE_MAZE, "maze_search.cpp"); ok(nlines(Gr.CODE_MAZE) === 64, "迷宮程式碼 64 行");
  codeInFile(Gr.CODE_REPR, "graph_repr.cpp"); ok(nlines(Gr.CODE_REPR) === 8, "表示法程式碼 8 行");
  const o = fs.readFileSync(path.join(__dirname, "out", "maze_search.txt"), "utf8").trim().split("\n");
  ["open", "walls", "noexit"].forEach((name, i) => {
    const b = Gr.gridRun("bfs", Gr.MAZES[name]), d = Gr.gridRun("dfs", Gr.MAZES[name]);
    ok(o[i] === "BFS 最短步數 " + b.steps + ",DFS 走到的步數 " + d.steps, name + " 與 g++ 一致:" + o[i]);
    checkFrames(b.frames, Gr.CODE_MAZE, "bfs " + name); checkFrames(d.frames, Gr.CODE_MAZE, "dfs " + name);
    ok(b.steps === Gr.searchPlain("bfs", Gr.parseMaze(Gr.MAZES[name])).steps && d.steps === Gr.searchPlain("dfs", Gr.parseMaze(Gr.MAZES[name])).steps, name + " 與無 frame 版本一致");
  });
  let seed = 9; const rnd = () => (seed = (seed * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff;
  for (let i = 0; i < 400; i++) {
    const rows = i % 4 === 0 ? Gr.randomMaze(rnd) : Array.from({ length: 5 }, (_, r) => Array.from({ length: 7 }, (_, c) => r === 0 && c === 0 ? "S" : r === 4 && c === 6 ? "G" : rnd() < 0.35 ? "#" : ".").join(""));
    const M = Gr.parseMaze(rows);
    /* 獨立的參考:用距離表算最短路 */
    const ref = (() => { const d = Array.from({ length: 5 }, () => Array(7).fill(-1)); d[0][0] = 0; let ch = true; while (ch) { ch = false; for (let r = 0; r < 5; r++) for (let c = 0; c < 7; c++) if (d[r][c] >= 0) [[1, 0], [-1, 0], [0, 1], [0, -1]].forEach(([a, b]) => { const x = r + a, y = c + b; if (x >= 0 && x < 5 && y >= 0 && y < 7 && rows[x][y] !== "#" && (d[x][y] < 0 || d[x][y] > d[r][c] + 1)) { d[x][y] = d[r][c] + 1; ch = true; } }); } return d[4][6]; })();
    const b = Gr.gridRun("bfs", rows), d = Gr.gridRun("dfs", rows);
    ok(b.steps === ref, "BFS 是最短步數 " + ref + " vs " + b.steps + "\n" + rows.join("\n"));
    ok((d.steps === -1) === (ref === -1) && (ref === -1 || d.steps >= ref), "DFS 找得到與否一致,且不比最短短");
    checkFrames(b.frames, Gr.CODE_MAZE, "bfs"); checkFrames(d.frames, Gr.CODE_MAZE, "dfs");
    [b, d].forEach(r => r.frames.forEach(f => ok(f.grid && f.list && f.chips, "frame 結構")));
    [b, d].forEach(r => { let prev = 0; r.frames.forEach((f, j) => { const k = Object.keys(f.grid.txt).length; ok(k >= prev && k - prev <= 4, "每個 frame 自己的數字快照,不能被後面的 frame 改到"); prev = k; }); ok(Object.keys(r.frames[0].grid.txt).length <= 1, "第一個 frame 只有起點"); });
  }
  ok(Gr.randomMaze(rnd).length === 5 && Gr.searchPlain("bfs", Gr.parseMaze(Gr.randomMaze(rnd))).steps > 0, "隨機迷宮一定有解");
  /* 表示法:與 g++ 輸出比對 */
  const og = fs.readFileSync(path.join(__dirname, "out", "graph_repr.txt"), "utf8").trim().split("\n");
  const r = Gr.reprRun("0-1 0-2 1-3 2-3 3-4"); ok(!r.error, "表示法執行"); checkFrames(r.frames, Gr.CODE_REPR, "repr");
  ok(r.frames.length === 1 + 5 * 4 + 1, "每條邊 4 個 frame");
  ok(r.matrix.map(x => x.join(" ") + " ").join("|") === og.slice(1, 6).join("|"), "鄰接矩陣與 g++ 一致");
  ok(r.adj.map((l, i) => i + ":" + l.map(v => " " + v).join("")).join("|") === og.slice(7, 12).join("|"), "鄰接表與 g++ 一致");
  ["", "0-0", "0-1 1-0", "a-b", "0-9", "0-1 0-1", "0-1 0-2 0-3 0-4 0-5 0-6 1-2 1-3 1-4 1-5"].forEach(t => ok(Gr.reprRun(t).error, "錯誤輸入: " + t));
  const big = Gr.reprRun("0-1, 1-2; 2-6"); ok(!big.error && big.n === 7, "分隔符號與 7 個點");
}
/* ---- dijkstra ---- */
if (A.dijk) {
  const D = A.dijk;
  codeInFile(D.CODE_DIJK, "dijk_ops.cpp"); ok(nlines(D.CODE_DIJK) === 32, "Dijkstra 程式碼 32 行");
  const o = fs.readFileSync(path.join(__dirname, "out", "dijk_ops.txt"), "utf8").trim().split("\n");
  const pathOf = (prev, t) => { const p = []; for (let v = t; v !== -1; v = prev[v]) p.push(v); return p.reverse(); };
  [["classic", 0, 4, 0], ["detour", 0, 4, 2]].forEach(([name, src, t, k]) => {
    const r = D.run(D.PRESETS[name], src); checkFrames(r.frames, D.CODE_DIJK, name);
    ok(o[k] === "dist: " + r.dist.join(" "), name + " dist 與 g++ 一致");
    ok(o[k + 1] === "到 " + t + " 的路(" + r.dist[t] + "): " + pathOf(r.prev, t).join(" "), name + " 路徑與 g++ 一致");
  });
  /* 參考:Bellman-Ford,完全不同的做法 */
  const bf = (P, src) => { const d = new Array(P.n).fill(D.INF); d[src] = 0; for (let i = 0; i < P.n; i++) P.edges.forEach(([a, b, w]) => { if (d[a] + w < d[b]) d[b] = d[a] + w; if (d[b] + w < d[a]) d[a] = d[b] + w; }); return d; };
  let seed = 21; const rnd = () => (seed = (seed * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff;
  for (let i = 0; i < 600; i++) {
    const P = D.randomGraph(rnd), src = Math.floor(rnd() * P.n), r = D.run(P, src);
    checkFrames(r.frames, D.CODE_DIJK, "random");
    ok(r.dist.join() === bf(P, src).join(), "Dijkstra 與 Bellman-Ford 一致");
    r.dist.forEach((d, v) => { if (v !== src) { const p = r.prev[v], w = P.edges.find(e => (e[0] === p && e[1] === v) || (e[1] === p && e[0] === v))[2]; ok(r.dist[p] + w === d, "prev 的路長度等於 dist"); } });
    r.frames.forEach(f => ok(f.g && f.dist.length === P.n && f.prev.length === P.n && f.chips.length === 3, "frame 結構"));
    let prevUpd = 0; r.frames.forEach(f => { const u = f.chips[2][1]; ok(u >= prevUpd, "更新次數只增不減"); prevUpd = u; });
    ok(r.frames[r.frames.length - 1].dist.every((c, v) => c.v === r.dist[v]), "最後一個 frame 是最終距離");
  }
  ok(D.run(D.PRESETS.classic, 6).error && D.run(D.PRESETS.classic, -1).error && D.run(D.PRESETS.classic, 1.5).error && D.run(D.PRESETS.detour, NaN).error, "錯誤的起點");
  ok(D.run(D.PRESETS.classic, 0).frames.some(f => f.msg.includes("過時")), "classic 圖會出現過時的舊紀錄");
}
/* ---- dp ---- */
if (A.dp) {
  const P = A.dp;
  codeInFile(P.CODE_DP, "dp_ops.cpp"); ok(nlines(P.CODE_DP) === 33, "DP 程式碼 33 行");
  const o = fs.readFileSync(path.join(__dirname, "out", "dp_ops.txt"), "utf8").trim().split("\n");
  const f10 = P.run("fib", 10), s5 = P.run("stairs", 5), k7 = P.run("knap", 7);
  ok(o[0] === "fib(10) = " + f10.answer && o[1] === "爬 5 階樓梯有 " + s5.answer + " 種方法" && o[2] === "背包最大價值 = " + k7.answer, "與 g++ 輸出一致");
  [f10, s5, k7].forEach(r => checkFrames(r.frames, P.CODE_DP, "dp"));
  const fibRef = n => { let a = 0, b = 1; for (let i = 0; i < n; i++) [a, b] = [b, a + b]; return a; };
  for (let n = 2; n <= 15; n++) { ok(P.run("fib", n).answer === fibRef(n), "fib " + n); ok(P.run("stairs", n).answer === fibRef(n + 1), "stairs " + n); checkFrames(P.run("fib", n).frames, P.CODE_DP, "fib"); checkFrames(P.run("stairs", n).frames, P.CODE_DP, "stairs"); }
  /* 背包:用枚舉所有子集當參考 */
  for (let cap = 1; cap <= 10; cap++) {
    let best = 0; for (let m = 0; m < 16; m++) { let w = 0, v = 0; for (let i = 0; i < 4; i++) if (m >> i & 1) { w += P.WT[i]; v += P.VAL[i]; } if (w <= cap && v > best) best = v; }
    const r = P.run("knap", cap); ok(r.answer === best, "背包容量 " + cap + ":" + r.answer + " vs " + best); checkFrames(r.frames, P.CODE_DP, "knap");
    ok(r.frames.length === 1 + 4 * (cap + 1) + 1, "背包 frame 數");
    r.frames.forEach(f => { ok(f.rows.length === 5 && f.rows.every(x => x.cells.length === cap + 1), "表格大小"); });
    ok(r.frames[0].rows[1].cells.every(c => c.cls === "empty"), "第一個 frame 之後的列還沒填(不能被後面的 frame 改到)");
    const T = P.table(cap); for (let a = 0; a <= 4; a++) for (let w = 0; w <= cap; w++) { const d = P.deps(cap, a, w); ok(d.cells.every(([x, y]) => x === a - 1 && y >= 0 && y <= w), "依賴在上一列、容量不更大"); }
  }
  ok(P.run("fib", 1).error && P.run("fib", 16).error && P.run("knap", 0).error && P.run("knap", 11).error && P.run("x", 5).error && P.run("fib", 2.5).error, "錯誤輸入");
}
/* ---- greedy / N 皇后 ---- */
if (A.greedy) {
  const Q = A.greedy;
  codeInFile(Q.CODE_GREEDY, "greedy_change.cpp"); ok(nlines(Q.CODE_GREEDY) === 13, "貪婪程式碼 13 行");
  codeInFile(Q.CODE_NQ, "nqueens.cpp"); ok(nlines(Q.CODE_NQ) === 21, "N 皇后程式碼 21 行");
  const og = fs.readFileSync(path.join(__dirname, "out", "greedy_change.txt"), "utf8").trim().split("\n");
  [["us", 63, 0], ["f1", 6, 1], ["f2", 15, 2]].forEach(([k, amt, i]) => {
    const r = Q.greedyRun(k, amt); checkFrames(r.frames, Q.CODE_GREEDY, "greedy " + k);
    ok(og[i] === "金額 " + amt + ",貪婪用 " + r.used.length + " 枚:" + r.used.map(x => " " + x).join("") + ";最少其實要 " + r.best + " 枚", "與 g++ 一致:" + og[i]);
  });
  /* 最少枚數用「窮舉所有組合」當參考 */
  const brute = (coins, a) => { let bestN = -1; const go = (i, rest, n) => { if (rest === 0) { if (bestN < 0 || n < bestN) bestN = n; return; } if (i === coins.length || rest < 0 || (bestN >= 0 && n >= bestN)) return; go(i, rest - coins[i], n + 1); go(i + 1, rest, n); }; go(0, a, 0); return bestN; };
  Object.keys(Q.SETS).forEach(k => { for (let a = 1; a <= 40; a++) { const r = Q.greedyRun(k, a); ok(r.best === brute(Q.SETS[k], a), "最少枚數 " + k + " " + a); ok(r.greedyOk === (Q.greedyPlain(Q.SETS[k], a).length > 0), "貪婪成功與否"); if (r.greedyOk) ok(r.used.length >= r.best && r.used.reduce((x, y) => x + y, 0) === a, "貪婪的和正確且不比最少少"); checkFrames(r.frames, Q.CODE_GREEDY, "greedy"); r.frames.forEach(f => ok(f.rows.length === 2 && f.chips.length >= 2, "frame 結構")); } });
  ok(Q.greedyRun("f1", 6).greedyOk && Q.greedyRun("f1", 6).used.length === 3 && Q.greedyRun("f1", 6).best === 2, "1,3,4 湊 6:貪婪 3 枚 vs 最少 2 枚");
  ok(!Q.greedyRun("f3", 6).greedyOk && Q.greedyRun("f3", 6).best === 3, "5,2 湊 6:貪婪找不到,但其實 3 枚");
  ok(Q.greedyRun("f3", 3).best === -1, "5,2 湊 3:真的湊不出");
  ok(Q.greedyRun("zz", 5).error && Q.greedyRun("us", 0).error && Q.greedyRun("us", 100).error && Q.greedyRun("us", 2.5).error, "錯誤輸入");
  /* N 皇后 */
  const on = fs.readFileSync(path.join(__dirname, "out", "nqueens.txt"), "utf8").trim().split("\n");
  const expect = { 4: 2, 5: 10, 6: 4 };
  [4, 5, 6].forEach(n => {
    const r = Q.nqRun(n, "all"); checkFrames(r.frames, Q.CODE_NQ, "nq" + n);
    ok(r.sols.length === expect[n], n + " 皇后解的數量");
    ok(on.includes(n + " 皇后:" + r.sols.length + " 組解"), n + " 皇后與 g++ 一致");
    r.sols.forEach(s => { for (let a = 0; a < n; a++) for (let b = a + 1; b < n; b++) ok(s[a] !== s[b] && Math.abs(s[a] - s[b]) !== b - a, "解沒有衝突"); });
    r.frames.forEach(f => ok(f.placed.length === n && f.N === n && f.chips.length === 3, "frame 結構"));
    const first = Q.nqRun(n, "first"); ok(first.sols.length === 1 && first.sols[0].join() === r.sols[0].join(), "第一組解相同");
    ok(first.frames.length < r.frames.length, "只看第一組解的 frame 比較少"); checkFrames(first.frames, Q.CODE_NQ, "nq first");
  });
  const q4 = Q.nqRun(4, "first").sols[0]; ok(["1,3,0,2"].includes(q4.join()) && on.slice(1, 5).join("|") === q4.map(c => ".".repeat(c) + "Q" + ".".repeat(4 - c - 1)).join("|"), "N=4 第一組解與 g++ 印出的棋盤一致");
  ok(Q.nqRun(3, "all").error && Q.nqRun(7, "all").error && Q.nqRun(4, "x").error, "錯誤輸入");
  /* 每個 frame 的 placed 是自己的快照 */
  const fr4 = Q.nqRun(4, "all").frames; ok(fr4[0].placed.every(c => c === -1), "第一個 frame 還沒放任何皇后");
}
/* ---- 高亮:textContent 還原為原始碼 ---- */
const sample = "int main() {\n    // hi\n    return 0;\n}\n";
const html = A.hlCpp(sample);
ok(html.replace(/<[^>]+>/g, "").replace(/&lt;/g,"<").replace(/&gt;/g,">").replace(/&amp;/g,"&") === sample.replace(/\n$/, "") + "\n", "hlCpp 保留換行");
console.log("test_algo: " + n + " 項檢查通過");
