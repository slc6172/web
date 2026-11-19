"""站台層設定:每頁 <head> 的 description / canonical / Open Graph / favicon / theme-color,
以及 skip link 與 <main id="main">。可重複套用(冪等)。

build.py 組頁後呼叫 apply();手寫頁(首頁、github-pr-guide.html)由 _build/site_files.py 套用。
站台網址只在這裡設定一次。留空時略過 canonical、og:url 與 sitemap。
"""
import re, html as _h, urllib.parse

SITE_URL = "https://www.slc6172.workers.dev"   # 不含結尾斜線;留空 = 略過 canonical / og:url / sitemap
CLEAN_URLS = True                               # Cloudflare 會把 /x.html 轉成 /x(已實測),canonical 與 sitemap 用無 .html 版本
ANALYTICS_TOKEN = ""                            # 選用:Cloudflare Web Analytics 的 token;留空 = 不輸出任何外部資源(預設)
SITE_NAME = "自學教學站"
THEME_COLOR = "#FAF9F5"
INDEX_DESC = "繁體中文的單頁自學教學站：GitHub、Arduino、微電影分鏡、C++。每篇都有演練、測驗與檢查表，可離線開啟。"

SKIP_CSS = """
  .skip { position:absolute; left:12px; top:-60px; z-index:100; background:var(--slate); color:var(--ivory);
          padding:10px 16px; border-radius:8px; font-size:14px; text-decoration:none; }
  .skip:focus { top:12px; outline:2px solid var(--clay); outline-offset:2px; }
  main:focus { outline:none; }
"""
_FAVICON_SVG = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'>"
                "<rect width='32' height='32' rx='8' fill='#FAF9F5'/><circle cx='16' cy='16' r='8' fill='#D97757'/></svg>")
FAVICON = "data:image/svg+xml," + urllib.parse.quote(_FAVICON_SVG, safe="/:=' ")
FAVICON = FAVICON.replace(" ", "%20")


def page_url(rel):
    """rel 例如 'github/github-pr-guide.html';首頁為 'index.html'。"""
    if not SITE_URL:
        return ""
    if rel == "index.html":
        return SITE_URL + "/"
    return SITE_URL + "/" + (rel[:-5] if CLEAN_URLS and rel.endswith(".html") else rel)


def _text(s):
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", _h.unescape(s)).strip()


def _fw(t):
    import fw
    return fw._text(t)


def derive_desc(html, limit=90):
    m = re.search(r'<div class="tldr">(.*?)</div>', html, re.S)
    t = _text(m.group(1)) if m else ""
    t = _fw(re.sub(r"^TL;DR\s*", "", t))
    if len(t) <= limit:
        return t
    cut = t[:limit]
    i = cut.rfind("。")
    if i < 30:
        i = max(cut.rfind("。"), cut.rfind("；"))
    return cut[:i + 1] if i > 30 else cut.rstrip("，、：") + "…"


def _esc(s):
    return _h.escape(s, quote=True)


_BEACON_RE = re.compile(r'\n?<script defer src="https://static\.cloudflareinsights\.com/beacon\.min\.js"[^>]*></script>')


def _beacon():
    return ('<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
            "data-cf-beacon='{\"token\": \"%s\"}'></script>" % ANALYTICS_TOKEN)


def apply(html, rel, desc=None):
    title = _text(re.search(r"<title>(.*?)</title>", html, re.S).group(1))
    if rel == "index.html":
        desc = desc or INDEX_DESC
    else:
        desc = desc or derive_desc(html)
    # 先清掉舊的站台層 meta(讓 description 改了之後可以重跑)
    html = re.sub(r'\n<(?:meta name="(?:description|theme-color|twitter:card)"|meta property="og:[a-z_]+"|link rel="(?:icon|canonical)")[^>]*>', "", html)
    if True:
        url = page_url(rel)
        tags = ['<meta name="description" content="%s">' % _esc(desc),
                '<meta name="theme-color" content="%s">' % THEME_COLOR,
                '<link rel="icon" href="%s">' % FAVICON]
        if url:
            tags.append('<link rel="canonical" href="%s">' % _esc(url))
        tags += ['<meta property="og:type" content="website">',
                 '<meta property="og:locale" content="zh_TW">',
                 '<meta property="og:site_name" content="%s">' % SITE_NAME,
                 '<meta property="og:title" content="%s">' % _esc(title),
                 '<meta property="og:description" content="%s">' % _esc(desc)]
        if url:
            tags.append('<meta property="og:url" content="%s">' % _esc(url))
        tags.append('<meta name="twitter:card" content="summary">')
        html = re.sub(r"(</title>)", lambda m: m.group(1) + "\n" + "\n".join(tags), html, count=1)
    if ".skip {" not in html:
        html = html.replace("</style>", SKIP_CSS + "</style>", 1)
    if 'class="skip"' not in html:
        html = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + '\n<a class="skip" href="#main">跳到主要內容</a>', html, count=1)
    if 'id="main"' not in html:
        html = html.replace("<main>", '<main id="main" tabindex="-1">', 1)
    html = _BEACON_RE.sub("", html)          # 先清掉舊的,token 改了或移除後重跑即可更新
    if ANALYTICS_TOKEN:
        html = html.replace("</body>", _beacon() + "\n</body>", 1)
    return html
