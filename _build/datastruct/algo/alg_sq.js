(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var MAXS = 8, MAXQ = 10;
  var CODE_STACK = [
    "struct Stack {", "    std::vector<int> data;", "", "    void push(int x) {", "        data.push_back(x);", "    }", "",
    "    int pop() {", "        int x = data.back();", "        data.pop_back();", "        return x;", "    }", "",
    "    bool empty() const {", "        return data.empty();", "    }", "};"].join("\n");
  var CODE_QUEUE = [
    "struct Queue {", "    std::vector<int> data;", "    int head = 0;                            // 隊伍最前面在 data 的哪個位置", "",
    "    void push(int x) {", "        data.push_back(x);", "    }", "", "    int pop() {", "        return data[head++];", "    }", "",
    "    bool empty() const {", "        return head == static_cast<int>(data.size());", "    }", "};"].join("\n");
  var CODE_BRACKET = [
    "bool matches(char open, char close) {", "    return (open == '(' && close == ')') ||", "           (open == '[' && close == ']') ||", "           (open == '{' && close == '}');", "}", "",
    "bool isBalanced(const std::string& s) {", "    std::stack<char> st;", "    for (char c : s) {", "        if (c == '(' || c == '[' || c == '{') {", "            st.push(c);",
    "        } else if (c == ')' || c == ']' || c == '}') {", "            if (st.empty()) {", "                return false;", "            }", "            char open = st.top();",
    "            st.pop();", "            if (!matches(open, c)) {", "                return false;", "            }", "        }", "    }", "    return st.empty();", "}"].join("\n");
  function isInt(x) { return typeof x === "number" && isFinite(x) && Math.floor(x) === x; }
  function cs(arr, over, tags) { return arr.map(function (v, i) { var c = { v: v, cls: (over && over[i]) || "" }; if (tags && tags[i]) c.t = tags[i]; return c; }); }

  /* ---- stack(base = 陣列,右邊是頂) ---- */
  function stackFrame(a, line, msg, over, extra) {
    var tags = {}; if (a.length) tags[a.length - 1] = "top";
    return { rows: [{ label: "stack(左邊是底,右邊是頂)", cells: cs(a, over, tags), empty: 0 }], chips: [["大小", a.length]].concat(extra || []), line: line, msg: msg };
  }
  function stackPush(a, v) {
    if (a.length >= MAXS) return { error: "示範最多放 " + MAXS + " 個,請先 pop 幾個或按 Reset。" };
    if (!isInt(v) || v < 0 || v > 99) return { error: "數值請輸入 0 到 99 的整數。" };
    var b = a.slice(), fr = [stackFrame(b, 4, "<code>push(" + v + ")</code>:要放到最上面(頂端)。")];
    b.push(v); var o = {}; o[b.length - 1] = "new";
    fr.push(stackFrame(b, 5, "<code>data.push_back(" + v + ")</code>:放進尾端。尾端就是 stack 的頂。", o));
    return { frames: fr, result: b };
  }
  function stackPop(a) {
    if (a.length === 0) return { error: "stack 是空的,不能 pop(對空 stack 取頂端是未定義行為,見常見錯誤)。" };
    var b = a.slice(), t = b.length - 1, x = b[t], o = {}, fr = [stackFrame(b, 8, "<code>pop()</code>:要取走最上面(最後放進去)的那一個。")];
    o[t] = "cur"; fr.push(stackFrame(b, 9, "<code>int x = data.back()</code>:先記下頂端的值 <b>" + x + "</b>。", o));
    b.pop(); fr.push(stackFrame(b, 10, "<code>data.pop_back()</code>:把頂端移除。"));
    fr.push(stackFrame(b, 11, "<code>return x</code>:回傳 " + x + "。後進先出:最後放進去的最先出來。", null, [["取出", x]]));
    return { frames: fr, result: b };
  }

  /* ---- queue(base = {data, head}) ---- */
  function queueFrame(q, line, msg, over, extra) {
    var tags = {}, n = q.data.length;
    if (q.head < n) { tags[q.head] = "front"; tags[n - 1] = tags[n - 1] ? "front/back" : "back"; }
    var over2 = {}; for (var i = 0; i < q.head; i++) over2[i] = "dim"; if (over) for (var k in over) over2[k] = over[k];
    return { rows: [{ label: "queue(淡色 = 已經離開隊伍)", cells: cs(q.data, over2, tags), empty: 0 }], chips: [["隊伍長度", n - q.head], ["head", q.head]].concat(extra || []), line: line, msg: msg };
  }
  function queueInit() { return { data: [], head: 0 }; }
  function queuePush(q, v) {
    if (q.data.length >= MAXQ) return { error: "這個簡化版不會回收已離開的格子,示範最多 " + MAXQ + " 格,請按 Reset。(真正的 std::queue 會回收。)" };
    if (!isInt(v) || v < 0 || v > 99) return { error: "數值請輸入 0 到 99 的整數。" };
    var b = { data: q.data.slice(), head: q.head }, fr = [queueFrame(b, 5, "<code>push(" + v + ")</code>:新來的人要排到隊伍最後面。")];
    b.data.push(v); var o = {}; o[b.data.length - 1] = "new";
    fr.push(queueFrame(b, 6, "<code>data.push_back(" + v + ")</code>:放在尾端。尾端就是隊伍的最後面(back)。", o));
    return { frames: fr, result: b };
  }
  function queuePop(q) {
    if (q.head >= q.data.length) return { error: "隊伍是空的,不能 pop。" };
    var b = { data: q.data.slice(), head: q.head }, x = b.data[b.head], o = {}, fr = [queueFrame(b, 9, "<code>pop()</code>:要讓最前面(最先排隊)的人離開。")];
    o[b.head] = "cur"; b.head++;
    fr.push(queueFrame(b, 10, "<code>return data[head++]</code>:取出最前面的 <b>" + x + "</b>,head 往後移一格。先進先出:最先排隊的最先離開。", o, [["取出", x]]));
    return { frames: fr, result: b };
  }

  /* ---- 括號配對 ---- */
  function balance(s) {
    if (typeof s !== "string" || s.length < 1 || s.length > 14) return { error: "請輸入 1 到 14 個字元。" };
    if (!/^[()\[\]{}a-zA-Z0-9]+$/.test(s)) return { error: "只能輸入括號 ( ) [ ] { } 和英數字。" };
    var chars = s.split(""), st = [], fr = [], MATCH = { ")": "(", "]": "[", "}": "{" };
    function f(line, msg, ci, over, result) {
      var o = {}; for (var i = 0; i < chars.length; i++) o[i] = i < ci ? "ok" : ""; if (ci >= 0 && ci < chars.length) o[ci] = "cur"; if (over) for (var k in over) o[k] = over[k];
      return { rows: [{ label: "字串", cells: cs(chars, o), empty: 0 }, { label: "stack(右邊是頂)", cells: cs(st, null, st.length ? (function () { var t = {}; t[st.length - 1] = "top"; return t; })() : null), empty: 0 }],
        chips: [["stack 大小", st.length]].concat(result ? [["結果", result]] : []), line: line, msg: msg };
    }
    fr.push(f(8, "要檢查字串 <code>" + s.replace(/&/g, "&amp;").replace(/</g, "&lt;") + "</code> 的括號有沒有正確配對。從左到右一個字元一個字元看,stack 一開始是空的。", 0));
    for (var i = 0; i < chars.length; i++) {
      var c = chars[i];
      if (c === "(" || c === "[" || c === "{") {
        st.push(c); fr.push(f([10, 11], "<code>" + c + "</code> 是左括號:<code>push</code> 進 stack,等著之後有人來配對。", i, { [i]: "new" }));
      } else if (c === ")" || c === "]" || c === "}") {
        if (!st.length) { fr.push(f([12, 13, 14], "<code>" + c + "</code> 是右括號,但 stack 是空的,沒有左括號可以配。<b>不配對</b>。", i, { [i]: "del" }, "不配對")); return { frames: fr, result: false }; }
        var open = st[st.length - 1];
        fr.push(f([12, 16], "<code>" + c + "</code> 是右括號:看 stack 頂端是 <code>" + open + "</code>。", i));
        st.pop();
        if (open !== MATCH[c]) { fr.push(f([17, 18, 19], "<code>pop</code> 出 <code>" + open + "</code>,但 <code>" + open + "</code> 和 <code>" + c + "</code> <b>配不起來</b>。不配對。", i, { [i]: "del" }, "不配對")); return { frames: fr, result: false }; }
        fr.push(f(17, "<code>pop</code> 出 <code>" + open + "</code>,和 <code>" + c + "</code> 配對成功,一起消掉。", i, { [i]: "mv" }));
      } else {
        fr.push(f(9, "<code>" + c + "</code> 不是括號,跳過。", i));
      }
    }
    var okk = st.length === 0;
    fr.push(f(23, okk ? "字串走完,stack 是空的:所有左括號都找到配對。<b>配對正確</b>。" : "字串走完,stack 裡還剩 " + st.length + " 個左括號沒人配。<b>不配對</b>。", chars.length, null, okk ? "配對正確" : "不配對"));
    return { frames: fr, result: okk };
  }
  A.sq = { MAXS: MAXS, MAXQ: MAXQ, CODE_STACK: CODE_STACK, CODE_QUEUE: CODE_QUEUE, CODE_BRACKET: CODE_BRACKET, stackFrame: stackFrame, queueFrame: queueFrame,
    stackPush: stackPush, stackPop: stackPop, queueInit: queueInit, queuePush: queuePush, queuePop: queuePop, balance: balance };
  if (typeof module !== "undefined" && module.exports) module.exports = A;
})(typeof window !== "undefined" ? window : globalThis);
