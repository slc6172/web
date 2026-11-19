"""統一組頁工具:把各頁的 SPEC(_build/<主題>/<檔名>.py)組成單檔 HTML,寫到 public/<主題>/。

用法(在 repo 根目錄):
    python3 _build/build.py p3            # github 第 3 篇
    python3 _build/build.py a05 a06       # arduino,可一次多個
    python3 _build/build.py m7
    python3 _build/build.py --all github  # 重建某主題全部頁面(也可寫 arduino / microfilm / all)
    python3 _build/build.py --out /tmp/x m1   # 改寫到別的資料夾(只用來比對,不動 public/)

規格檔放哪個主題,由檔名開頭決定:p* = github、a* = arduino、m* = microfilm、c* = clang、d* = datastruct。
新增主題時,在下方 THEMES 加一筆設定即可(見 _build/README.md)。
"""
import re, json, sys, os, importlib, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PUBLIC = os.path.join(ROOT, "public")          # 會被部署的網站根目錄
SHARED = os.path.join(HERE, "shared")

# ---------- 共用樣式:從已完成的 PR 頁讀取(所有主題的頁面都沿用這份 CSS) ----------
_pr = open(os.path.join(PUBLIC, "github", "github-pr-guide.html"), encoding="utf-8").read()
CSS = re.search(r"<style>(.*?)</style>", _pr, re.S).group(1)
EXTRA = """
  .fill.f4 { grid-template-columns:repeat(4,minmax(0,1fr)); }
  .fill.f3 { grid-template-columns:repeat(3,minmax(0,1fr)); }
  .fill.f2 { grid-template-columns:repeat(2,minmax(0,1fr)); }
  @media (max-width: 920px) { .fill.f4, .fill.f3 { grid-template-columns:repeat(2,minmax(0,1fr)); } }
  @media (max-width: 520px) { .fill.f4, .fill.f3, .fill.f2 { grid-template-columns:minmax(0,1fr); } }
  .badge.bad { background:rgba(176,74,63,.15); color:var(--rust); }
  .dec-out { background:var(--gray-100); border-radius:10px; padding:12px 14px; font-size:14px; color:var(--gray-700); margin-top:12px; }
"""


def _read(*parts):
    return open(os.path.join(*parts), encoding="utf-8").read()


COMMON_JS = _read(SHARED, "common.js")

# 站台層設定(description / canonical / og / skip link)在 shared/seo.py;SPEC 可用 desc 欄位覆寫 description。

# ---------- 各主題設定 ----------
# prefix : 規格檔名開頭(用來找到檔案在哪個資料夾)
# topic  : 頁首 eyebrow 前綴(SPEC 沒寫 topic 時使用)
# foot   : 頁尾文字(SPEC 沒寫 foot 時使用)
# css/js : 只有這個主題才內嵌的額外樣式與腳本(放在 _build/<主題>/ 底下的檔案名)
# fw     : True = 組完後把頁面文字轉成全形標點(shared/fw.py)
# uniq_svg : True = 重複使用同一張圖時,重新編號 SVG marker id,避免重複 id
THEMES = {
    "github": dict(
        prefix="p", topic="GitHub 入門",
        foot="本頁按鈕名稱以 GitHub 英文介面為準;GitHub 偶爾會微調介面文字與位置,找不到時請用關鍵字對照畫面上相近的按鈕。查證日期:2026-11-06。",
        css=None, js=None, fw=True, uniq_svg=False),
    "arduino": dict(
        prefix="a", topic="Arduino 入門",
        foot="本主題以 Arduino IDE 2.x(Windows)與 Arduino Uno R3 為準。零件規格與電路數值是常見範例,請以你手上零件的規格為準;每次改接線前,先拔掉 USB。查證日期:2026-11-07。",
        css="arduino.css", js="arduino.js", fw=True, uniq_svg=False),
    "microfilm": dict(
        prefix="m", topic="微電影分鏡入門",
        foot="", css=None, js=None, fw=True, uniq_svg=True),   # topic / foot / css 由 microfilm/mh.py 的 defaults() 提供
    "clang": dict(
        prefix="c", topic="C++ 入門", foot="",
        css="clang.css", js="clang.js", fw=True, uniq_svg=False),   # foot 由 clang/ch.py 的 FOOT 提供（每頁 SPEC 都帶 topic / foot）
    "datastruct": dict(
        prefix="d", topic="C++ 演算法", foot="",
        css=None, js=None, fw=True, uniq_svg=False, algo="algo"),   # foot 由 datastruct/dh.py 的 FOOT 提供（每頁 SPEC 都帶）；algo/ 是動畫模組，SPEC 的 modules 列出要內嵌哪些
}


def algo_bundle(theme, T, mods):
    """datastruct 的動畫模組：core 一定內嵌，其餘只內嵌 SPEC["modules"] 列出的。回傳 (css, js)。"""
    css, js = "", ""
    d = os.path.join(HERE, theme, T["algo"])
    for m in ["core"] + [x for x in mods if x != "core"]:
        c, j = os.path.join(d, m + ".css"), os.path.join(d, m + ".js")
        if os.path.exists(c):
            css += open(c, encoding="utf-8").read()
        if os.path.exists(j):
            js += "\n/* ---- %s ---- */\n" % m + open(j, encoding="utf-8").read()
        elif m != "core":
            raise SystemExit("找不到模組: " + j)
    return css, js


def uniq_svg(html):
    """同一張圖(例如 shot() 的結果)在頁面中重複使用時,每個 <svg> 內的 marker id 重新編號。"""
    n = [0]

    def one(m):
        n[0] += 1
        return re.sub(r"\b(mv|cm)k\d+", lambda mm: "%sk%d" % (mm.group(1), n[0]), m.group(0))
    return re.sub(r"<svg\b.*?</svg>", one, html, flags=re.S)


def build(s, out_root=PUBLIC):
    d = s.get("dir", "github")
    if d not in THEMES:
        raise SystemExit("SPEC 的 dir=%r 不在 THEMES 裡,請先在 build.py 新增這個主題" % d)
    T = THEMES[d]
    topic = s.get("topic", s.get("eyebrow_prefix", T["topic"]))   # eyebrow_prefix：datastruct 規格檔的舊欄位名
    foot = s.get("foot", T["foot"])
    a_css, a_js = algo_bundle(d, T, s.get("modules", [])) if T.get("algo") and (s.get("modules") or s.get("algo")) else ("", "")
    css = CSS + EXTRA + a_css + (_read(HERE, d, T["css"]) if T["css"] else "") + s.get("css", "")
    js = COMMON_JS + ("\n" + _read(HERE, d, T["js"]) if T["js"] else "")
    toc = "\n".join('  <a href="#%s">%d. %s</a>' % (i, n + 1, t) for n, (i, t) in enumerate(s["toc"]))

    def pg(kind, label, ent):
        href, title = ent
        if os.path.exists(os.path.join(PUBLIC, d, href)):
            return '  <a class="%s" href="%s"><small>%s</small><b>%s</b></a>\n' % (kind, href, label, title)
        return '  <span class="%s off" aria-disabled="true"><small>%s · 製作中</small><b>%s</b></span>\n' % (kind, label, title)
    pager = ""
    if s.get("prev"):
        pager += pg("prev", "上一篇", s["prev"])
    if s.get("next"):
        pager += pg("next", "下一篇", s["next"])

    extra_js = (s["js"] + "\n") if s.get("js") else ""   # 頁面專屬 <script>(可省略)
    if a_js:       # datastruct：動畫模組與頁面腳本（SPEC["script"]，包成 IIFE）接在 common.js 之後
        extra_js += "<script>\n" + a_js + "\n</script>\n"
    if s.get("script"):
        extra_js += "<script>\n(function(){\n\"use strict\";\n" + s["script"] + "\n})();\n</script>\n"
    html = f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{s["title"]}</title>
<style>{css}</style>
</head>
<body>
<div class="progress" aria-hidden="true"><span id="readBar"></span></div>
<div class="page">

<header>
  <nav class="crumb" aria-label="站內導覽"><a href="../index.html#{d}">← 回教學首頁</a></nav>
  <div class="eyebrow">{topic} · {s["eyebrow"]}</div>
  <h1>{s["h1"]}</h1>
  <p class="sub">{s["sub"]}</p>
  <div class="tldr"><b>TL;DR</b> {s["tldr"]}</div>
</header>

<div class="layout">
<nav class="toc" aria-label="本頁目錄">
  <div class="label">On this page</div>
{toc}
</nav>

<main>
{s["body"]}
</main>
</div>

<p class="foot" style="margin-top:28px">{foot}</p>

<nav class="pager" aria-label="上一篇與下一篇">
{pager}</nav>
</div>

<script>window.PAGE = {json.dumps(s["config"], ensure_ascii=False)};</script>{s.get("pre_js", "")}
<script>
{js}
</script>
{extra_js}</body>
</html>
"""
    outdir = os.path.join(out_root, d)
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, s["file"])
    if T["fw"]:
        import fw
        html = fw.apply(html)
    if T["uniq_svg"]:
        html = uniq_svg(html)
    import seo
    html = seo.apply(html, d + "/" + s["file"], s.get("desc"))
    open(out, "w", encoding="utf-8").write(html)
    print("wrote", out, html.count("\n"), "lines")


def find_spec_module(name):
    """依檔名找到 _build/<主題>/<name>.py,並把該主題資料夾加進 import 路徑。"""
    for theme, T in THEMES.items():
        if os.path.exists(os.path.join(HERE, theme, name + ".py")):
            sys.path.insert(0, os.path.join(HERE, theme))
            return importlib.import_module(name)
    raise SystemExit("找不到規格檔 %s.py(應放在 _build/<主題>/)" % name)


def theme_specs(theme):
    T = THEMES[theme]
    pat = re.compile(r"^%s\d+$" % T["prefix"])
    names = [os.path.basename(f)[:-3] for f in glob.glob(os.path.join(HERE, theme, "*.py"))]
    return sorted((n for n in names if pat.match(n)), key=lambda n: int(n[len(T["prefix"]):]))


if __name__ == "__main__":
    sys.path.insert(0, SHARED)
    args = sys.argv[1:]
    out_root = PUBLIC
    if "--out" in args:
        i = args.index("--out")
        out_root = os.path.abspath(args[i + 1])
        del args[i:i + 2]
    names = []
    if "--all" in args:
        i = args.index("--all")
        which = args[i + 1] if i + 1 < len(args) else "all"
        for t in (THEMES if which == "all" else [which]):
            names += theme_specs(t)
    else:
        names = args
    if not names:
        raise SystemExit(__doc__)
    for name in names:
        build(find_spec_module(name).SPEC, out_root)
