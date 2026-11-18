"""全站瀏覽器驗證(Playwright):首頁 + 所有主題的所有頁面。
用法(在 repo 根目錄):  python3 _build/verify.py
需要:pip install playwright && playwright install chromium;或設定 CHROME_PATH 指向 Chrome。
檢查:1280 / 390 寬無橫向溢出、無 JS 錯誤;首頁每個分頁籤的卡片數、篩選、進度、快速入口;
      每頁「← 回教學首頁」回到對的分頁籤;測驗、檢查表、各頁互動(有才測)、相對連結與 #錨點。
各主題另有更深入的專用驗證:arduino/verify_arduino.py、microfilm/check.py。"""
import sys, os, re, glob, tempfile
from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "shared"))
from pwutil import stub_analytics   # 攔下 Cloudflare Web Analytics 的請求,避免 file:// 驗證時的 CORS console error

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(os.path.dirname(HERE), "public")
BASE = "file://" + PUB + "/"
CHROME = os.environ.get("CHROME_PATH") or None          # 沒設定就用 Playwright 內建的 Chromium
SHOTS = os.path.join(tempfile.gettempdir(), "learning-hub-shots")
os.makedirs(SHOTS, exist_ok=True)

THEMES = [d for d in ("github", "arduino", "microfilm") if os.path.isdir(os.path.join(PUB, d))]
THEMES += sorted(d for d in os.listdir(PUB) if os.path.isdir(os.path.join(PUB, d)) and d not in THEMES)
pages = ["index.html"]
for t in THEMES:
    pages += sorted(t + "/" + os.path.basename(f) for f in glob.glob(os.path.join(PUB, t, "*.html")))

errs = []

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
    for w in (1280, 390):
        for pg in pages:
            ctx = b.new_context(viewport={"width": w, "height": 900})
            stub_analytics(ctx)
            page = ctx.new_page()
            page.on("pageerror", lambda e, pg=pg: errs.append((pg, "pageerror", str(e))))
            page.on("console", lambda m, pg=pg: errs.append((pg, "console", m.text)) if m.type == "error" else None)
            page.goto(BASE + pg)
            page.wait_for_timeout(300)
            ov = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            if ov > 0:
                errs.append((pg, "overflow@%d" % w, ov))
            print(w, pg, "overflow:", ov)
            if w == 1280:
                page.screenshot(path=os.path.join(SHOTS, os.path.basename(pg).replace(".html", ".png")), full_page=False)
            ctx.close()

    # ---- 首頁功能 ----
    ctx = b.new_context(viewport={"width": 1280, "height": 900}); stub_analytics(ctx); page = ctx.new_page()
    page.on("pageerror", lambda e: errs.append(("index", "pageerror", str(e))))
    page.goto(BASE + "index.html")
    tabs = page.eval_on_selector_all("#catTabs button[data-cat]", "els => els.map(e => e.dataset.cat)")
    print("tabs:", tabs)
    for t in tabs:
        page.click('#catTabs button[data-cat="%s"]' % t)
        n_cards = page.locator(".card").count()
        n_files = len(glob.glob(os.path.join(PUB, t, "*.html")))
        print(t, "cards:", n_cards, "files:", n_files, "done:", page.locator(".card.done").count())
        if n_cards != n_files:
            errs.append(("index", "cards != files for " + t, (n_cards, n_files)))
        page.click('#filters button[data-f="done"]'); done_n = page.locator(".card").count()
        page.click('#filters button[data-f="all"]')
        page.click('#pathStrip button[data-i="1"]'); stage_n = page.locator(".card").count()
        page.click('#pathStrip button[data-i="1"]')
        page.locator('input[data-r="%s:1"]' % t).check()
        print("  done filter:", done_n, "| stage 2 cards:", stage_n, "| prog:", page.inner_text("#progTxt"))
        page.locator('input[data-r="%s:1"]' % t).uncheck()
        print("  quick links:", page.locator("a.q").count(), "disabled:", page.locator(".q.off").count())
        # 快速入口的連結都存在
        for h in page.eval_on_selector_all("a.q", "els => els.map(e => e.getAttribute('href'))"):
            if not os.path.exists(os.path.join(PUB, h.split("#")[0])):
                errs.append(("index", "quick link missing", h))

    # ---- 每頁「回教學首頁」回到自己的分頁籤 ----
    for t in THEMES:
        first = sorted(glob.glob(os.path.join(PUB, t, "*.html")))[0]
        page.goto("file://" + first)
        page.click(".crumb a"); page.wait_for_timeout(200)
        sel = page.eval_on_selector('#catTabs button[aria-selected="true"]', "e => e.dataset.cat")
        print("crumb from", t, "-> tab:", sel)
        if sel != t:
            errs.append((t, "crumb lands on wrong tab", sel))
    for pg in [x for x in pages[1:]]:
        s = open(os.path.join(PUB, pg), encoding="utf-8").read()
        want = "../index.html#" + pg.split("/")[0]
        if 'href="%s"' % want not in s:
            errs.append((pg, "crumb href not", want))

    # ---- 各頁通用互動與連結 ----
    for pg in [x for x in pages[1:] if "github-pr-" not in x]:
        page.goto(BASE + pg)
        if page.locator("#quizAns button").count() > 1:
            page.click("#quizAns button >> nth=1"); page.wait_for_timeout(100)
        print(pg, "quiz fb:", page.locator("#quizFb.show").count(), "checks:", page.locator("#checks input").count())
        if page.locator("#checks input").count():
            page.locator("#checks input").first.check()
        if page.locator("#stages").count() and page.locator("#nextStage").count() and not page.locator("#tab-o").count():
            page.click("#nextStage")
        if page.locator("#in-me").count():
            page.fill("#in-me", "alice")
        if page.locator("#decideBtns button").count() > 5:
            page.click("#decideBtns button >> nth=5")
        if page.locator("#tab-o").count():
            page.click("#tab-o"); page.click("#nextStage")
        if page.locator("[data-sim]").count():
            page.click("[data-sim] >> nth=0")
        hrefs = page.eval_on_selector_all("a[href]", "els => els.map(e => e.getAttribute('href'))")
        for h in hrefs:
            if h.startswith("http") or h.startswith("#"):
                if h.startswith("#") and len(h) > 1 and page.locator(h).count() == 0:
                    errs.append((pg, "badanchor", h))
                continue
            if not os.path.exists(os.path.normpath(os.path.join(PUB, os.path.dirname(pg), h.split("#")[0]))):
                errs.append((pg, "MISSING LINK", h))
    b.close()

# ---------- 站台層靜態檢查(不需瀏覽器):head 中繼資料、skip link、sitemap、quick 錨點 ----------
def static_checks():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "shared"))
    import seo
    import json
    seen_t, seen_d = {}, {}
    for pg in pages:
        h = open(os.path.join(PUB, pg), encoding="utf-8").read()
        for name, pat in (("description", r'<meta name="description" content="[^"]{20,}"'),
                          ("canonical", r'<link rel="canonical" href="https?://'),
                          ("og:title", r'<meta property="og:title"'), ("og:description", r'<meta property="og:description"'),
                          ("og:url", r'<meta property="og:url"'), ("favicon", r'<link rel="icon"'),
                          ("theme-color", r'<meta name="theme-color"'),
                          ("skip link", r'<a class="skip" href="#main"'), ("main#main", r'<main id="main"')):
            if not re.search(pat, h):
                errs.append((pg, "缺少 " + name, ""))
        t = re.search(r"<title>(.*?)</title>", h, re.S).group(1)
        d = re.search(r'<meta name="description" content="([^"]*)"', h)
        d = d.group(1) if d else ""
        if t in seen_t: errs.append((pg, "title 與 %s 重複" % seen_t[t], t))
        if d and d in seen_d: errs.append((pg, "description 與 %s 重複" % seen_d[d], ""))
        seen_t[t] = seen_t.get(t, pg); seen_d[d] = seen_d.get(d, pg)
    sm = os.path.join(PUB, "sitemap.xml")
    for f in ("robots.txt", "_headers", "sitemap.xml"):
        if not os.path.exists(os.path.join(PUB, f)):
            errs.append((f, "public/ 缺少檔案", ""))
    if os.path.exists(sm):
        locs = re.findall(r"<loc>(.*?)</loc>", open(sm, encoding="utf-8").read())
        want = set(re.sub(r"^https?://[^/]+/?", "", u) or "index.html" for u in locs)
        want = set(w[:-0] if False else w for w in want)
        have = set(pages)
        norm = lambda x: x if x.endswith(".html") else (x + ".html" if x else "index.html")
        if set(map(norm, want)) != have:
            errs.append(("sitemap.xml", "與 public/ 頁面不符", sorted(set(map(norm, want)) ^ have)))
    # 外部資源白名單:唯一允許的是選用的 Cloudflare Web Analytics beacon(canonical 不算資源)
    ok_ext = "https://static.cloudflareinsights.com/beacon.min.js"
    for pg in pages:
        h = open(os.path.join(PUB, pg), encoding="utf-8").read()
        for m in re.finditer(r'<(?:script|img|iframe|source|video|audio)\b[^>]*\ssrc=["\'](https?:)?//[^"\']+["\']|<link\b(?![^>]*rel=["\']canonical["\'])[^>]*\shref=["\'](https?:)?//[^"\']+["\']', h):
            if ok_ext not in m.group(0):
                errs.append((pg, "不允許的外部資源", m.group(0)[:100]))
    # 部署設定:wrangler.jsonc 與 SITE_URL、CLEAN_URLS 一致,workflow 與 .gitignore 存在
    root = os.path.dirname(PUB)
    wr = os.path.join(root, "wrangler.jsonc")
    if os.path.exists(wr):
        w = open(wr, encoding="utf-8").read()
        nm = re.search(r'"name"\s*:\s*"([^"]+)"', w)
        if not re.search(r'"directory"\s*:\s*"\./?public/?"', w):
            errs.append(("wrangler.jsonc", "assets.directory 不是 ./public", ""))
        if nm and seo.SITE_URL and not re.match(r"https://%s\." % re.escape(nm.group(1)), seo.SITE_URL):
            errs.append(("wrangler.jsonc", "name 與 seo.SITE_URL 的主機名稱不符", "%s vs %s" % (nm.group(1), seo.SITE_URL)))
        if "html_handling" in w:
            errs.append(("wrangler.jsonc", "有設定 html_handling:請確認 seo.CLEAN_URLS 是否仍適用", ""))
    for f in (".github/workflows/deploy.yml", ".gitignore", "wrangler.jsonc"):
        if not os.path.exists(os.path.join(root, f)):
            errs.append((f, "專案根目錄缺少部署相關檔案(打包時要保留)", ""))
    # quick 錨點:SITE 裡每個 a 都要存在於目標頁
    idx = open(os.path.join(PUB, "index.html"), encoding="utf-8").read()
    for cid in re.findall(r'id:"(\w+)", label', idx):
        seg = idx[idx.find('id:"%s", label' % cid):]
        nxt = re.search(r'\n    \{ id:"', seg[5:]); seg = seg[:nxt.start() + 5] if nxt else seg
        hrefs = dict((int(n), hf) for n, hf in re.findall(r'n:(\d+), title:"[^"]*", href:"([^"]+)"', seg))
        qm = re.search(r"quick:\[(.*?)\n\s*\]", seg, re.S)
        for n, a in re.findall(r'n:(\d+)(?:, a:"([^"]*)")? \}', qm.group(1) if qm else ""):
            if not a:
                errs.append(("index", "quick 沒有 a 錨點", "%s #%s" % (cid, n))); continue
            tp = os.path.join(PUB, hrefs.get(int(n), ""))
            if not os.path.isfile(tp) or 'id="%s"' % a not in open(tp, encoding="utf-8").read():
                errs.append(("index", "quick 錨點不存在", "%s #%s → #%s" % (cid, n, a)))


static_checks()
print("站台層靜態檢查完成")
print("截圖放在:", SHOTS)
print("ERRORS:", errs)
sys.exit(1 if errs else 0)
