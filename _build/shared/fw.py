"""全形標點處理(微電影主題用):把「中文字後面」的半形 , : ; ? ! 與包著中文的 ( ) 換成全形。
只處理頁面文字、aria-label,以及 <script> 內含中文的字串、SVG 的 <title>／<text> 文字;不動 CSS、<pre>、<code>、程式碼與 SVG 的其他部分。
build.py 在 dir != github 時自動呼叫:  html = fw.apply(html)"""
import re

CJK = "\u3400-\u9fff\u3001-\u3003\u300c-\u300f\uff09"   # 中日韓字 + 、。 + 「」『』 + 全形右括號
TAG = "\ue000"
_MAP = {",": "，", ":": "：", ";": "；", "?": "？", "!": "！"}
_PUNC = re.compile("([%s])((?:%s)*)([,:;?!])" % (CJK, TAG))
_LATIN = re.compile("([^\\s\u3400-\u9fff\ue000,:;?!，。：；！？、])([,:;?!])(?=%s*[\u3400-\u9fff])" % TAG)   # 任何非空白、非中文的符號或字母後面接中文
_HAS = re.compile("[\u3400-\u9fff]")


def _text(t):
    """t 是一段不含標籤的文字(標籤已換成 TAG 哨兵字元)。先轉括號,再轉標點(這樣「)」後面的冒號也會轉)。"""
    def par(m):
        inner = m.group(2)
        if _HAS.search(inner) or (m.group(1) and _HAS.search(m.group(1))):
            return m.group(1) + "（" + inner + "）"
        return m.group(0)
    for _ in range(3):  # 巢狀括號:內層轉完,外層才配得到
        t = re.sub("([%s]?)\\(([^()]*)\\)" % "\u3400-\u9fff", par, t)
    for _ in range(2):  # 連續標點如「!」「?」
        t = _PUNC.sub(lambda m: m.group(1) + m.group(2) + _MAP[m.group(3)], t)
    # 英文、數字或右括號後面、接中文的 , : ;(例:Git 與 GitHub,用 clone)
    t = _LATIN.sub(lambda m: m.group(1) + _MAP[m.group(2)], t)
    # 標籤(</code>、</b>、</strong>…)緊接標點、後面是中文:例「<code>loop()</code>,用」「<b>Copy</b>,貼」
    t = re.sub("(%s)([,:;?!])(?=%s|[\u3400-\u9fff]|$)" % (TAG, TAG), lambda m: m.group(1) + _MAP[m.group(2)], t)
    return t


def _flow(seg):
    """處理一段 HTML(不含 script/style/pre/svg):以標籤為界,但跨標籤判斷前一個字。"""
    tags = []
    def keep(m):
        tags.append(m.group(0)); return TAG
    body = re.sub(r"<code\b[^>]*>.*?</code>|<[^>]+>", keep, seg, flags=re.S)   # <code>…</code> 整段不動
    body = _text(body)
    it = iter(tags)
    return re.sub(TAG, lambda m: next(it), body)


def _aria(s):
    return re.sub(r'(aria-label|title|alt)="([^"]*)"', lambda m: '%s="%s"' % (m.group(1), _text(m.group(2))), s)


def _js(code):
    def lit(m):
        q, inner = m.group(1), m.group(2)
        return q + (_flow(inner) if _HAS.search(inner) else inner) + q
    code = re.sub(r"(\")((?:[^\"\\\n]|\\.)*)\"", lambda m: lit(m), code)   # 允許 \n、\" 等跳脫
    code = re.sub(r"(')((?:[^'\\\n]|\\.)*)'", lambda m: lit(m), code)
    code = re.sub(r"(</[a-z0-9]+>)([,:;?!])(?=<[a-z/]|[\u3400-\u9fff])", lambda m: m.group(1) + _MAP[m.group(2)], code)   # 安全網
    return code


def apply(html):
    parts = re.split(r"(<script\b.*?</script>|<style\b.*?</style>|<pre\b.*?</pre>|<svg\b.*?</svg>)", html, flags=re.S)
    out = []
    prev = ""
    for p in parts:
        if prev.startswith("<code") and re.match(r"[,:;?!](?=[\u3400-\u9fff<]|$)", p):   # <code>…</code> 後面緊接的標點
            p = _MAP[p[0]] + p[1:]
        prev = p if p.startswith(("<code", "<pre", "<script", "<style", "<svg")) else ""
        if p.startswith("<script"):
            m = re.match(r"(<script\b[^>]*>)(.*)(</script>)$", p, re.S)
            out.append(m.group(1) + _js(m.group(2)) + m.group(3))
        elif p.startswith(("<style", "<pre", "<code")):
            out.append(p)
        elif p.startswith("<svg"):   # 只轉 <title>(滑過提示)與 <text> 的文字
            p = re.sub(r"(<(title|text)\b[^>]*>)(.*?)(</\2>)", lambda m: m.group(1) + _flow(m.group(3)) + m.group(4), p, flags=re.S)
            out.append(_aria(p))
        else:
            out.append(_aria(_flow(p)))
    return "".join(out)


if __name__ == "__main__":
    t = '<p>小安跑得很快,然後<b>停下來</b>:她看到(第 6 篇)的 pan, tilt 與 16:9!</p><script>var a = "框到身體,但沒有拍到頭"; var b = {x:1, y:2};</script>'
    print(apply(t))
