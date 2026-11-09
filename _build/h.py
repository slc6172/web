import html as _h

def e(s): return _h.escape(s, quote=False)

def cmd(text, cap=None, copy=True, cpp=False):
    c = '<div class="cap">%s</div>' % cap if cap else ""
    b = '<button type="button" class="copy">Copy</button>' if copy else ""
    return '<div class="cmd">%s<pre data-tpl%s>%s</pre>%s</div>' % (c, " data-cpp" if cpp else "", e(text), b)

def see(t):  return '<div class="see"><b class="l">你會看到</b>%s</div>' % t
def warn(t, l="注意"): return '<div class="warn"><b class="l">%s</b>%s</div>' % (l, t)
def tip(t, l="小技巧"): return '<div class="tip"><b class="l">%s</b>%s</div>' % (l, t)

def ops(items): return '<ol class="ops">%s</ol>' % "".join("<li>%s</li>" % i for i in items)

def step(n, title, why, *parts):
    return ('<div class="step"><div class="num">%d</div><div>\n<h3>%s</h3>\n<p class="why">%s</p>\n%s\n</div></div>'
            % (n, title, why, "\n".join(parts)))

def steps(*s): return '<div class="steps">\n%s\n</div>' % "\n".join(s)

def details(summary, body, open_=False):
    return '<details%s><summary>%s</summary><div class="body">%s</div></details>' % (" open" if open_ else "", summary, body)

def table(cls, head, rows):
    r = '<div class="row">%s</div>' % "".join('<div class="cell head">%s</div>' % x for x in head)
    for row in rows:
        cells = ""
        for i, x in enumerate(row):
            cells += '<div class="cell%s">%s</div>' % (" term" if i == 0 else "", x)
        r += '<div class="row">%s</div>' % cells
    return '<div class="table-wrap"><div class="gt %s">%s</div></div>' % (cls, r)

def section(id_, title, *parts):
    return '<section id="%s">\n  <h2>%s</h2>\n  <hr class="rule">\n%s\n</section>' % (id_, title, "\n".join(parts))

def fill(fields):
    # fields: (key, label, ns)
    n = len(fields)
    cells = "".join(
        '<div><label for="in-%s">%s</label><input id="in-%s" data-k="%s"%s autocomplete="off" spellcheck="false"></div>'
        % (k, l, k, k, ' data-ns="1"' if ns else "") for k, l, ns in fields)
    return ('<div class="panel"><div class="fill f%d">%s</div>'
            '<div class="fill-foot"><button type="button" class="ghost" id="resetBtn">Reset</button>'
            '<span>空白時顯示範例值;<span class="slot">橘底</span>文字就是會被替換的部分。</span></div></div>' % (n, cells))

def sim(role_html, title, question, buttons):
    b = "".join('<button type="button" data-sim="%s">%s</button>' % (k, t) for k, t in buttons)
    return ('<div class="panel sim" data-simgroup>\n<h3>%s%s</h3>\n<p style="margin:6px 0 0;color:var(--gray-700)">%s</p>\n'
            '<div class="sim-buttons" role="group" aria-label="選擇做法">%s</div>\n'
            '<div class="sim-result" aria-live="polite">選一個做法,看看對不對。</div>\n</div>' % (role_html, title, question, b))

QUIZ_HTML = """<div class="panel" id="quiz">
    <div class="quiz-top"><h3 style="margin:0">快速測驗</h3><span class="count" id="quizCount">1 / 1</span></div>
    <div class="question" id="quizQ"></div>
    <div class="answers" id="quizAns"></div>
    <div class="feedback" id="quizFb" aria-live="polite"></div>
    <div class="quiz-foot"><span id="quizScore">答對 0 題</span><button type="button" class="primary" id="quizNext" disabled>下一題 →</button></div>
  </div>"""

def checks(items, title="開做之前,對照這張清單"):
    li = "".join('<label class="check-item"><input type="checkbox"><span>%s</span></label>' % i for i in items)
    return ('<h3 style="margin-top:30px">%s</h3>\n<div class="panel">\n<div class="checks" id="checks">%s</div>\n'
            '<div class="check-progress" id="checkProgress">已完成 0 / %d 項</div>\n<div class="bar"><span id="checkBar"></span></div>\n</div>' % (title, li, len(items)))

def resources(items, title="GitHub 官方文件"):
    a = "".join('<a class="resource" href="%s" target="_blank" rel="noopener"><b>%s</b><small>%s</small></a>' % i for i in items)
    return '<h3 style="margin-top:30px">%s</h3>\n<div class="resources">%s</div>' % (title, a)

def canvas(svg, legend):
    li = "".join('<li><span class="n">%s</span><span>%s</span></li>' % (n, t) for n, t in legend)
    return '<div class="canvas">%s</div>\n<ol class="legend" style="list-style:none">%s</ol>' % (svg, li)

def quiz_cfg(items):
    return [{"q": q, "a": a, "c": c, "why": w} for q, a, c, w in items]
