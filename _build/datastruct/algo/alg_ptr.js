(function (G) {
  "use strict";
  var A = G.Algo = G.Algo || {};
  var CODE_PTR = [
    "int main() {", "    int x = 10;", "    int y = 5;", "    int& r = x;", "    int* p = &x;", "    *p = 20;", "    r = 30;", "    p = &y;", "    *p = 99;",
    "    std::cout << x << \" \" << y << \"\\n\";", "}"].join("\n");
  var CODE_NODE = [
    "struct Node {", "    int val;", "    Node* next;", "};", "", "int main() {",
    "    Node* a = new Node{1, nullptr};", "    Node* b = new Node{2, nullptr};", "    a->next = b;",
    "    std::cout << a->next->val << \"\\n\";", "    delete b;", "    delete a;", "}"].join("\n");

  function framesPtr() {
    var AD = { x: "0x1000", y: "0x1004", p: "0x1008" };
    var S = { x: null, y: null, r: false, p: null }, fr = [];
    function vars(chg, tgt) {
      var out = [];
      if (S.x !== null) out.push({ n: "x", t: "int", addr: AD.x, v: S.x, cls: (chg === "x" ? "chg " : "") + (tgt === "x" ? "tgt" : "") });
      if (S.y !== null) out.push({ n: "y", t: "int", addr: AD.y, v: S.y, cls: (chg === "y" ? "chg " : "") + (tgt === "y" ? "tgt" : "") });
      if (S.r) out.push({ n: "r", t: "int&", ref: "x", v: S.x, cls: chg === "r" ? "chg" : "" });
      if (S.p) out.push({ n: "p", t: "int*", addr: AD.p, v: AD[S.p], to: S.p, cls: chg === "p" ? "chg" : "" });
      return out;
    }
    function snap(line, msg, chg) { fr.push({ vars: vars(chg, S.p), line: line, msg: msg }); }
    snap(1, "程式從 <code>main</code> 開始。每個變數都會在記憶體佔一格,每一格有自己的<b>地址</b>。");
    S.x = 10; snap(2, "<code>int x = 10;</code>:x 佔一格(地址 0x1000),裡面放 10。", "x");
    S.y = 5; snap(3, "<code>int y = 5;</code>:y 佔另一格(地址 0x1004),裡面放 5。", "y");
    S.r = true; snap(4, "<code>int&amp; r = x;</code>:<b>參照</b> r 是 x 的另一個名字。它不是新的格子,用 r 就是在用 x。", "r");
    S.p = "x"; snap(5, "<code>int* p = &amp;x;</code>:<b>指標</b> p 自己也佔一格,裡面存的是 x 的<b>地址</b>(0x1000)。我們說「p 指向 x」。", "p");
    S.x = 20; snap(6, "<code>*p = 20;</code>:<code>*p</code> 是「走到 p 指的那格」,所以 x 變成 20。", "x");
    S.x = 30; snap(7, "<code>r = 30;</code>:改 r 就是改 x,x 變成 30。", "x");
    S.p = "y"; snap(8, "<code>p = &amp;y;</code>:p 裡存的地址換成 y 的(0x1004),現在 p 指向 y。x 沒有動。", "p");
    S.y = 99; snap(9, "<code>*p = 99;</code>:p 現在指向 y,所以 y 變成 99。", "y");
    snap(10, "印出 <code>" + S.x + " " + S.y + "</code>。");
    return fr;
  }

  function framesNode() {
    var fr = [], A1 = "0x2000", B1 = "0x2010";
    var st = { a: null, b: null, n1: null, n2: null };
    function snapV(line, msg, o) {
      o = o || {};
      var vars = [];
      if (st.a) vars.push({ n: "a", t: "Node*", addr: "0x1000", v: A1, to: "節點 1", cls: o.va || "" });
      if (st.b) vars.push({ n: "b", t: "Node*", addr: "0x1008", v: B1, to: "節點 2", cls: o.vb || "" });
      var heap = [];
      if (st.n1) heap.push({ addr: A1, val: st.n1.val, next: st.n1.next, cls: st.n1.freed ? "freed" : (o.n1 || "") });
      if (st.n2) heap.push({ addr: B1, val: st.n2.val, next: st.n2.next, cls: st.n2.freed ? "freed" : (o.n2 || "") });
      fr.push({ vars: vars, heap: heap, line: line, msg: msg });
    }
    snapV(6, "程式從 <code>main</code> 開始。這次要用 <code>new</code> 在 heap 上做出兩個節點。");
    st.a = true; st.n1 = { val: 1, next: "null" }; snapV(7, "<code>new Node{1, nullptr}</code>:在 heap 要一塊空間,放 val=1、next=null,回傳它的地址 0x2000,存進指標 a。", { va: "new", n1: "new" });
    st.b = true; st.n2 = { val: 2, next: "null" }; snapV(8, "同樣做出第二個節點(地址 0x2010),由 b 指著。", { vb: "new", n2: "new" });
    st.n1.next = B1; snapV(9, "<code>a-&gt;next = b;</code>:<code>a-&gt;</code> 是「走到 a 指的節點,再取裡面的成員」。把節點 1 的 next 改成 b 的地址,兩個節點就接起來了。", { n1: "chg", n2: "tgt" });
    snapV(10, "<code>a-&gt;next-&gt;val</code>:先走到節點 1,取它的 next(0x2010),再走到那個節點取 val,得到 <b>2</b>。", { n2: "tgt" });
    st.n2.freed = true; snapV(11, "<code>delete b;</code>:把節點 2 還給系統。b 這個變數本身還在,但它指的格子已經不能再用了。", { vb: "chg" });
    st.n1.freed = true; snapV(12, "<code>delete a;</code>:節點 1 也還給系統。<b>new 幾次,就要 delete 幾次</b>,否則會記憶體洩漏。", { va: "chg" });
    snapV(13, "<code>main</code> 結束。");
    return fr;
  }
  A.ptr = { CODE_PTR: CODE_PTR, CODE_NODE: CODE_NODE, framesPtr: framesPtr, framesNode: framesNode };
  if (typeof module !== "undefined" && module.exports) module.exports = A;
})(typeof window !== "undefined" ? window : globalThis);
