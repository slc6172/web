# datastruct 主題專用的組頁輔助函式(沿用 h.py,再加上 C++ 程式碼、輸出、widget 容器)
import os, re, html as _html
from h import *

HERE = os.path.dirname(os.path.abspath(__file__))
CPP = os.path.join(HERE, "cpp")
OUT = os.path.join(HERE, "out")

def read_cpp(name):
    return open(os.path.join(CPP, name + ".cpp"), encoding="utf-8").read().rstrip("\n")

def read_out(name):
    return open(os.path.join(OUT, name + ".txt"), encoding="utf-8").read().rstrip("\n")

def cpp(name, cap=None, copy=True):
    """顯示 _build/cpp/<name>.cpp(實際編譯過的檔案)。cap 預設為 <name>.cpp 的 main.cpp 說明。"""
    c = '<div class="cap">%s</div>' % (cap or "main.cpp")
    b = '<button type="button" class="copy">Copy</button>' if copy else ""
    return '<div class="cmd">%s<pre data-cpp>%s</pre>%s</div>' % (c, e(read_cpp(name)), b)

def out(name, cap="執行結果"):
    return '<div class="cmd out"><div class="cap">%s</div><pre>%s</pre></div>' % (cap, e(read_out(name)))

def compile_cmd(fname="main.cpp"):
    return ('<div class="cmd"><div class="cap">編譯並執行(g++ 或 clang++ 皆可)</div><pre>g++ -std=c++17 -Wall -Wextra -o main %s\n./main</pre>'
            '<button type="button" class="copy">Copy</button></div>' % fname)

def widget(wid, label):
    return '<div id="%s" role="group" aria-label="%s"></div>' % (wid, label)

def try_list(items):
    return '<ol class="ops">%s</ol>' % "".join("<li>%s</li>" % i for i in items)

FOOT = "範例以 g++ 13、<code>-std=c++17 -Wall -Wextra</code> 實際編譯執行驗證(零警告);動畫為教學示意,資料量固定很小。cppreference 連結已逐條開啟確認。查證日期:2026-11-18。"
EYEBROW = "C++ 演算法"

# 測驗:common.js 不洗牌,且選項與 why 會被跳脫(HTML 標籤會原樣顯示)。
# datastruct 專用版:選項與 why 去掉標籤,並依題號固定錯開正解位置(確定性,每次建置結果相同)。
_POS = [1, 2, 0, 2, 1, 0]
def _plain(t): return _html.unescape(re.sub(r"<[^>]+>", "", t))
def quiz_cfg(items):
    out = []
    for i, (q, a, c, w) in enumerate(items):
        good = a[c]; rest = [x for j, x in enumerate(a) if j != c]
        t = _POS[i % len(_POS)] % len(a)
        arr = rest[:t] + [good] + rest[t:]
        out.append({"q": q, "a": [_plain(x) for x in arr], "c": t, "why": _plain(w)})
    return out
