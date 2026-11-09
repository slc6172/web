import re, json, sys, importlib
import os
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(os.path.dirname(HERE), "public")   # 網站根目錄(會被部署的 public/)
pr = open(BASE + "/github/github-pr-guide.html", encoding="utf-8").read()
CSS = re.search(r"<style>(.*?)</style>", pr, re.S).group(1)
EXTRA = """
  .fill.f4 { grid-template-columns:repeat(4,minmax(0,1fr)); }
  .fill.f3 { grid-template-columns:repeat(3,minmax(0,1fr)); }
  .fill.f2 { grid-template-columns:repeat(2,minmax(0,1fr)); }
  @media (max-width: 920px) { .fill.f4, .fill.f3 { grid-template-columns:repeat(2,minmax(0,1fr)); } }
  @media (max-width: 520px) { .fill.f4, .fill.f3, .fill.f2 { grid-template-columns:minmax(0,1fr); } }
  .badge.bad { background:rgba(176,74,63,.15); color:var(--rust); }
  .dec-out { background:var(--gray-100); border-radius:10px; padding:12px 14px; font-size:14px; color:var(--gray-700); margin-top:12px; }
"""
JS = open(HERE + "/common.js", encoding="utf-8").read()
A_CSS = open(HERE + "/arduino.css", encoding="utf-8").read()
A_JS = open(HERE + "/arduino.js", encoding="utf-8").read()
GH_FOOT = "本頁按鈕名稱以 GitHub 英文介面為準;GitHub 偶爾會微調介面文字與位置,找不到時請用關鍵字對照畫面上相近的按鈕。查證日期:2026-11-06。"
AR_FOOT = "本主題以 Arduino IDE 2.x(Windows)與 Arduino Uno R3 為準。零件規格與電路數值是常見範例,請以你手上零件的規格為準;每次改接線前,先拔掉 USB。查證日期:2026-11-07。"

def build(s):
    d = s.get("dir", "github")
    ar = d == "arduino"
    topic = s.get("topic", "Arduino 入門" if ar else "GitHub 入門")
    foot = s.get("foot", AR_FOOT if ar else GH_FOOT)
    css = CSS + EXTRA + (A_CSS if ar else "")
    js = JS + ("\n" + A_JS if ar else "")
    toc = "\n".join('  <a href="#%s">%d. %s</a>' % (i, n + 1, t) for n, (i, t) in enumerate(s["toc"]))

    def pg(kind, label, ent):
        href, title = ent
        if os.path.exists(os.path.join(BASE, d, href)):
            return '  <a class="%s" href="%s"><small>%s</small><b>%s</b></a>\n' % (kind, href, label, title)
        return '  <span class="%s off" aria-disabled="true"><small>%s · 製作中</small><b>%s</b></span>\n' % (kind, label, title)
    pager = ""
    if s.get("prev"):
        pager += pg("prev", "上一篇", s["prev"])
    if s.get("next"):
        pager += pg("next", "下一篇", s["next"])
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

<script>window.PAGE = {json.dumps(s["config"], ensure_ascii=False)};</script>
<script>
{js}
</script>
</body>
</html>
"""
    os.makedirs(os.path.join(BASE, d), exist_ok=True)
    out = os.path.join(BASE, d, s["file"])
    open(out, "w", encoding="utf-8").write(html)
    print("wrote", out, html.count("\n"), "lines")

if __name__ == "__main__":
    sys.path.insert(0, HERE)
    for name in sys.argv[1:]:
        build(importlib.import_module(name).SPEC)
