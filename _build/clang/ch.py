"""C++ 主題的組頁輔助函式(建立在 h.py 之上)。頁面只寫資料與文字,程式碼與輸出一律來自 examples/。"""
import os, re, json, difflib, html as _h
from h import *

HERE = os.path.dirname(os.path.abspath(__file__))
EX = os.path.join(HERE, "examples")
_rp = os.path.join(EX, "results.json")
RES = json.load(open(_rp, encoding="utf-8")) if os.path.exists(_rp) else {}

TOPIC = "C++ 入門"
FOOT = ("範例程式皆以 g++ 13、<code>-std=c++17</code> 實測,頁面上的輸出就是實際執行的結果(編譯錯誤訊息的引號在你的環境可能是 <code>'</code>)。"
        "外部網站連結已於 2026-11-18 抽查(非逐條驗證);安裝步驟未逐一對照官方文件;若連結失效,請搜尋「C++ online compiler」。製作日期:2026-11-12。")

def spec(**kw):
    d = dict(dir="clang", kit="clang", topic=TOPIC, foot=FOOT)
    d.update(kw)
    return d

# ---------- 語法上色(只用 token 色) ----------
KW = set("int double float char bool void return if else for while do switch case break continue const auto struct class "
         "public private protected virtual override new delete nullptr true false using namespace".split())
TOK = re.compile(r'(//.*$)|("(?:\\.|[^"\\])*"?)|(\'(?:\\.|[^\'\\])*\'?)|(#\s*include\s*<[^>]*>)|(\b[A-Za-z_]\w*\b)')
def hl(line):
    out, last = [], 0
    for m in TOK.finditer(line):
        out.append(e(line[last:m.start()]))
        t = m.group(0)
        if m.group(1): out.append('<span class="c">%s</span>' % e(t))
        elif m.group(2) or m.group(3): out.append('<span class="s">%s</span>' % e(t))
        elif m.group(4): out.append('<span class="p">%s</span>' % e(t))
        elif t in KW: out.append('<span class="k">%s</span>' % t)
        else: out.append(e(t))
        last = m.end()
    out.append(e(line[last:]))
    return "".join(out)

NOTE = re.compile(r"\s*//@\s?(.*)$")
def parse(id_):
    """回傳 [(程式碼, 說明或 None)]。'//@ 說明' 不會顯示在程式碼裡,而是變成可點選的逐行說明。"""
    rows = []
    for raw in open(os.path.join(EX, id_ + ".cpp"), encoding="utf-8").read().rstrip("\n").split("\n"):
        m = NOTE.search(raw)
        rows.append((raw[:m.start()] if m else raw, m.group(1) if m else None))
    return rows

def code(id_, prev=None, cap="main.cpp"):
    rows = parse(id_)
    add = set()
    if prev:
        a, b = [r[0] for r in parse(prev)], [r[0] for r in rows]
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
            if tag in ("insert", "replace"): add.update(range(j1, j2))
    notes = any(n for _, n in rows)
    lines = ""
    for i, (c, n) in enumerate(rows):
        cls = "ln" + (" add" if i in add else "") + (" has-note" if n else "")
        extra = ' data-note="%s" tabindex="0" role="button"' % _h.escape(n, quote=True) if n else ""
        lines += '<span class="%s"%s>%s</span>' % (cls, extra, hl(c))
    legend = " · <em>綠色底 = 這一步新增或改過的行</em>" if prev else ""
    hint = " · 點有 ⓘ 的行看說明" if notes else ""
    box = ('<div class="code%s"><div class="cap">%s%s%s</div><pre>%s</pre><button type="button" class="copy">Copy</button></div>'
           % (" has-notes" if notes else "", cap, legend, hint, lines))
    if notes: box += '<div class="code-note" aria-live="polite">點程式碼中有 ⓘ 的那一行,這裡會說明它在做什麼。</div>'
    return box

def term(id_, cap=None):
    r = RES[id_]
    parts = r.get("parts")
    if parts and any(k == "i" for k, _ in parts):
        cap = cap or "執行結果(橘色是你要輸入的部分)"
        body = "".join(('<span class="in">%s</span>%s' % (e(t.rstrip("\n")), "\n" * (len(t) - len(t.rstrip("\n"))))) if k == "i" else e(t) for k, t in parts).rstrip("\n")
    else:
        cap = cap or "執行結果"
        out = r["out"].rstrip("\n")
        body = e(out) if out else '<span class="none">(沒有任何輸出——程式執行了,只是沒有叫它印東西)</span>'
    return '<div class="term"><div class="cap">%s</div><pre>%s</pre></div>' % (cap, body)

def errterm(id_, cap="編譯器的回應(g++)"):
    return '<div class="term err"><div class="cap">%s</div><pre>%s</pre></div>' % (cap, e(RES[id_]["err"]))

def run(id_, prev=None, cap="main.cpp"):
    """程式碼 + 實測輸出"""
    return code(id_, prev, cap) + term(id_)

def exercise(n, title, prompt, sol, before="", note="", prev=None):
    sol_html = code(sol, prev) + term(sol) + (("<p style='margin-top:8px'>%s</p>" % note) if note else "")
    return details("練習 %d:%s" % (n, title),
                   "<p>%s</p>%s%s" % (prompt, before, details("看參考解答(先自己寫再看)", sol_html)))

def check_trace(steps, ex):
    """追蹤表的輸出必須和實測輸出完全一致,否則建置失敗。"""
    got = "".join(s.get("o", "") for s in steps)
    if got != RES[ex]["out"]: raise SystemExit("追蹤與實測輸出不符 %s:\n%r\n%r" % (ex, got, RES[ex]["out"]))

def stepper(store, id_, ex, steps, names=None, types=None):
    """逐行追蹤。steps: [{l:行(0 起算), v:{變數:值}, o:輸出, n:說明}];names 決定變數盒子的順序。"""
    check_trace(steps, ex)
    store[id_] = dict(steps=steps, names=names or [], types=types or {}, frames=any("f" in s for s in steps), mem=any("m" in s for s in steps))
    lines = "".join('<span class="ln">%s</span>' % hl(c) for c, _ in parse(ex))
    return ('<div class="stp" data-stepper="%s"><div class="stp-grid">'
            '<div class="code"><div class="cap">main.cpp · 橘色 = 正在執行的行</div><pre>%s</pre></div>'
            '<div class="stp-side"><div class="stp-vars"></div><div class="term stp-out"><div class="cap">輸出</div><pre></pre></div></div></div>'
            '<div class="stp-note" aria-live="polite"></div>'
            '<div class="flow-ctl"><button type="button" class="ghost" data-a="prev">← 上一步</button><button type="button" class="primary" data-a="next">下一步 →</button>'
            '<button type="button" class="ghost" data-a="reset">Reset</button><span class="stp-count"></span></div></div>' % (id_, lines))

def mem(id_): return '<div data-mem="%s"></div>' % id_
def ba(id_): return '<div data-ba="%s"></div>' % id_
def crash(id_): return term(id_, "程式輸出(中止之前)") + errterm(id_, "程式異常中止(執行時錯誤,g++ 的訊息)")

def diagram(id_): return '<div data-diagram="%s"></div>' % id_

def calc(id_): return '<div data-calc="%s"></div>' % id_

def flow(id_): return '<div data-flow="%s"></div>' % id_

def chk(items):
    li = "".join('<label class="check-item"><input type="checkbox"><span>%s</span></label>' % i for i in items)
    return ('<h3 style="margin-top:30px">學完之後,對照這張清單</h3>\n<div class="panel">\n<div class="checks" id="checks">%s</div>\n'
            '<div class="check-progress" id="checkProgress">已完成 0 / %d 項</div>\n<div class="bar"><span id="checkBar"></span></div>\n</div>' % (li, len(items)))

def links(items, title="延伸閱讀(外部連結)"):
    a = "".join('<a class="resource" href="%s" target="_blank" rel="noopener"><b>%s</b><small>%s</small></a>' % i for i in items)
    return '<h3 style="margin-top:30px">%s</h3>\n<div class="resources">%s</div>' % (title, a)

# ---------- 全站篇章順序(上一篇/下一篇自動依「檔案是否已存在」決定)----------
ORDER = [
 ("clang-intro-guide.html", "認識 C++ 與環境"), ("clang-first-program-guide.html", "第一支程式"),
 ("clang-variables-guide.html", "變數與資料型態"), ("clang-io-guide.html", "輸入輸出"),
 ("clang-operators-guide.html", "運算子與運算式"), ("clang-conditions-guide.html", "條件判斷"),
 ("clang-loops-guide.html", "迴圈"), ("clang-practice1-guide.html", "綜合演練一:乘法表與猜數字"),
 ("clang-array-vector-guide.html", "陣列與 vector"), ("clang-string-guide.html", "字串"),
 ("clang-functions-guide.html", "函式"), ("clang-ref-pointer-guide.html", "參考與指標"),
 ("clang-stl-guide.html", "STL:map、set、sort"), ("clang-class-guide.html", "struct 與 class"),
 ("clang-oop-guide.html", "封裝、繼承、多型"), ("clang-file-exception-guide.html", "檔案 I/O 與例外處理"),
 ("clang-memory-guide.html", "動態記憶體與智慧指標"), ("clang-project-guide.html", "除錯與成績管理小專案"),
]
def nav(n):
    """n 為篇號(1 起算)。回傳 dict(prev=..., next=...),下一篇檔案還沒做出來就省略。"""
    out = {"prev": ORDER[n - 2] if n > 1 else None, "next": None}
    if n < len(ORDER) and os.path.exists(os.path.join(HERE, "..", "public", "clang", ORDER[n][0])):
        out["next"] = ORDER[n]
    return out
