(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var CODE_COUNT = [
    "int main() {", "    int n = 8;", "    int single = 0;", "    for (int i = 0; i < n; ++i) {",
    "        ++single;                            // 單層迴圈:做 n 次", "    }", "",
    "    int nested = 0;", "    for (int i = 0; i < n; ++i) {", "        for (int j = 0; j < n; ++j) {",
    "            ++nested;                        // 雙層迴圈:做 n * n 次", "        }", "    }", "",
    "    int halving = 0;", "    int m = n;", "    while (m > 1) {", "        m /= 2;",
    "        ++halving;                           // 每次砍一半:大約 log2(n) 次", "    }", "",
    "    std::cout << single << \" \" << nested << \" \" << halving << \"\\n\";", "}"].join("\n");
  var LIM = { a: [1, 16], b: [1, 8], c: [1, 64] };
  function isInt(x) { return typeof x === "number" && isFinite(x) && Math.floor(x) === x; }
  function count(prog, n) {
    if (!LIM[prog]) return { error: "請選一種程式。" };
    if (!isInt(n) || n < LIM[prog][0] || n > LIM[prog][1]) return { error: "這種程式的 n 請輸入 " + LIM[prog][0] + " 到 " + LIM[prog][1] + " 的整數(要看得清楚,所以限制小一點)。" };
    var fr = [], k = 0, i, j;
    function cell(v, cls) { return { v: v, cls: cls || "" }; }
    if (prog === "a") {
      var row = []; for (i = 0; i < n; i++) row.push(cell(i));
      fr.push({ cells: row.map(function (c) { return cell(c.v); }), chips: [["n", n], ["操作次數", 0]], line: 4, msg: "單層迴圈:i 從 0 跑到 " + (n - 1) + ",每圈做一次 <code>++single</code>。" });
      for (i = 0; i < n; i++) {
        k++;
        fr.push({ cells: row.map(function (c, q) { return cell(c.v, q < i ? "ok" : q === i ? "cur" : ""); }), chips: [["n", n], ["操作次數", k]], line: [4, 5], msg: "i = " + i + ":操作次數變成 <b>" + k + "</b>。" });
      }
      fr.push({ cells: row.map(function (c) { return cell(c.v, "ok"); }), chips: [["n", n], ["操作次數", k]], line: 6, msg: "迴圈結束,一共 <b>" + k + "</b> 次 = n。" });
    } else if (prog === "b") {
      function grid(ci, cj) {
        var rows = [];
        for (var r = 0; r < n; r++) { var cs = []; for (var c = 0; c < n; c++) cs.push(cell(r * n + c + 1 <= k ? "✓" : "", (r === ci && c === cj) ? "cur" : (r * n + c + 1 <= k ? "ok" : ""))); rows.push({ label: "i = " + r, cells: cs, empty: 0 }); }
        return rows;
      }
      fr.push({ rows: grid(-1, -1), chips: [["n", n], ["操作次數", 0]], line: 9, msg: "雙層迴圈:外層 i 跑 n 圈,<b>每一圈</b>裡面的 j 又跑 n 圈。每個格子代表一次 <code>++nested</code>。" });
      for (i = 0; i < n; i++) for (j = 0; j < n; j++) {
        k++;
        fr.push({ rows: grid(i, j), chips: [["n", n], ["操作次數", k]], line: [9, 10, 11], msg: "i = " + i + "、j = " + j + ":操作次數 <b>" + k + "</b>。" + (j === n - 1 ? "這一列滿了,換下一個 i。" : "") });
      }
      fr.push({ rows: grid(-1, -1), chips: [["n", n], ["操作次數", k]], line: 13, msg: "結束,一共 <b>" + k + "</b> 次 = n × n = " + n + "²。n 變 2 倍,次數就變 4 倍。" });
    } else {
      var m = n, seq = [cell(m, "cur")];
      fr.push({ cells: seq.map(function (c) { return cell(c.v, c.cls); }), chips: [["m", m], ["操作次數", 0]], line: 16, msg: "每次把 m 砍一半,直到 m 不大於 1。目前 m = " + m + "。" });
      while (m > 1) {
        m = Math.floor(m / 2); k++;
        seq.forEach(function (c) { c.cls = "ok"; }); seq.push(cell(m, "cur"));
        fr.push({ cells: seq.map(function (c) { return cell(c.v, c.cls); }), chips: [["m", m], ["操作次數", k]], line: [17, 18, 19], msg: "<code>m /= 2</code>:m 變成 " + m + ",操作次數 <b>" + k + "</b>。" });
      }
      fr.push({ cells: seq.map(function (c) { return cell(c.v, "ok"); }), chips: [["m", m], ["操作次數", k]], line: 20, msg: "m 縮到 1,一共砍了 <b>" + k + "</b> 次,約等於 log₂(" + n + ")。n 變 2 倍,才多砍 1 次。" });
    }
    return { frames: fr, result: { prog: prog, n: n, ops: k } };
  }
  A.count = { CODE_COUNT: CODE_COUNT, LIM: LIM, count: count };
  if (typeof module !== "undefined" && module.exports) module.exports = A;
})(typeof window !== "undefined" ? window : globalThis);
