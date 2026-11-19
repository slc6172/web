"""C++ 主題的驗證:靜態檢查 + Playwright(1280 與 390 寬)。CHROME_PATH 可指定瀏覽器。"""
import os, re, sys, glob
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(os.path.dirname(os.path.dirname(HERE)), "public")
CHROME = os.environ.get("CHROME_PATH", "/usr/bin/google-chrome")
files = sorted(glob.glob(PUB + "/clang/*.html"))
errs = []
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "shared"))
import seo   # 站台網址（canonical / og:url）來自 shared/seo.py 的 SITE_URL
from pwutil import stub_analytics   # 攔下 Cloudflare Web Analytics 的請求（選用 beacon，見 seo.ANALYTICS_TOKEN）
ALLOW = ("https://en.cppreference.com/", "https://www.onlinegdb.com/", "https://www.programiz.com/", "http://www.w3.org/2000/svg", seo.SITE_URL + "/", "https://static.cloudflareinsights.com/beacon.min.js")

for f in files:   # 靜態檢查
    t = open(f, encoding="utf-8").read(); n = os.path.basename(f)
    if "localStorage" in t or "sessionStorage" in t: errs.append((n, "storage"))
    for u in re.findall(r"https?://[^\s\"'<>)]+", t):
        if not u.startswith(ALLOW): errs.append((n, "external", u))
    ids = re.findall(r'\sid="([^"]+)"', re.sub(r'<script>.*?</script>', '', t, flags=re.S))
    for i in set(ids):
        if ids.count(i) > 1: errs.append((n, "dup id", i))

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
    for w in (1280, 390):
        for f in files:
            ctx = b.new_context(viewport={"width": w, "height": 900}); stub_analytics(ctx); page = ctx.new_page(); n = os.path.basename(f)
            page.on("pageerror", lambda e, n=n: errs.append((n, "pageerror", str(e))))
            page.on("console", lambda m, n=n: errs.append((n, "console", m.text)) if m.type == "error" else None)
            page.goto("file://" + f); page.wait_for_timeout(250)
            ov = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            print(w, n, "overflow:", ov)
            if ov > 0: errs.append((n, "overflow", ov, w))
            if w == 1280: page.screenshot(path="/tmp/shot_%s.png" % n.replace(".html", ""))
            ctx.close()
    # 功能檢查
    ctx = b.new_context(viewport={"width": 1280, "height": 900}); stub_analytics(ctx); ctx.grant_permissions(["clipboard-read", "clipboard-write"])
    for f in files:
        page = ctx.new_page(); n = os.path.basename(f)
        page.on("pageerror", lambda e, n=n: errs.append((n, "pageerror", str(e))))
        page.goto("file://" + f)
        page.click("#quizAns button >> nth=0"); page.wait_for_timeout(80)
        if not page.locator("#quizFb.show").count(): errs.append((n, "quiz no feedback"))
        page.locator("#checks input").first.check()
        if "1 / " not in page.inner_text("#checkProgress"): errs.append((n, "checks"))
        # 複製按鈕
        btn = page.locator(".code button.copy:visible").first; btn.click(); page.wait_for_timeout(100)
        if "Copied" not in btn.inner_text(): errs.append((n, "copy feedback"))
        clip = page.evaluate("navigator.clipboard.readText()")
        if "main" not in clip and "int" not in clip: errs.append((n, "clipboard content", clip[:40]))
        # 逐行說明
        if page.locator(".ln.has-note:visible").count():
            page.locator(".ln.has-note:visible").first.click()
            if "第" not in page.inner_text(".code-note"): errs.append((n, "line note"))
        # Flow
        if page.locator("[data-flow]").count():
            page.click('[data-a="next"]'); page.click('[data-a="next"]')
            page.check('[data-a="fail"]')
            if not page.locator(".flow-detail.bad").count(): errs.append((n, "flow fail state"))
            if page.locator('[data-a="next"]').is_disabled() is False: errs.append((n, "next not disabled at fail"))
            page.click('[data-a="reset"]')
            if page.locator(".flow-node.on").count() != 1: errs.append((n, "flow reset"))
        # Stepper
        for k in range(page.locator("[data-stepper]").count()):
            st = page.locator("[data-stepper]").nth(k)
            total = int(st.locator(".stp-count").inner_text().split("/")[1])
            for _ in range(total): st.locator('[data-a="next"]').click()
            if not st.locator('[data-a="next"]').is_disabled(): errs.append((n, "stepper end"))
            if not st.locator(".stp-out pre").inner_text().strip() and "assign" in (st.get_attribute("data-stepper") or ""): errs.append((n, "stepper output empty"))
            st.locator('[data-a="reset"]').click()
            if st.locator(".stp-out pre").inner_text().strip(): errs.append((n, "stepper reset"))
        # Calc
        if page.locator("[data-calc=format]").count():
            if "|3.14159|" not in page.inner_text(".calc-out"): errs.append((n, "format default", page.inner_text(".calc-out")))
            page.check("#fF"); page.fill("#fP", "2")
            if "|3.14|" not in page.inner_text(".calc-out"): errs.append((n, "format fixed", page.inner_text(".calc-out")))
        if page.locator("[data-calc=eval]").count():
            page.fill("#eX", "2 + 3 * 4")
            if "結果：14" not in page.inner_text(".ev-out") : errs.append((n, "eval", page.inner_text(".ev-out")))
            page.fill("#eX", "1 / 0")
            if "除以 0" not in page.inner_text(".ev-out"): errs.append((n, "eval div0"))
            page.click('.calc-pre button >> nth=1')
            if "-3" not in page.inner_text(".ev-out"): errs.append((n, "eval preset"))
        if page.locator("[data-calc=loop]").count():
            if "共執行 5 圈" not in page.inner_text(".lp-out"): errs.append((n, "loop default", page.inner_text(".lp-out")[:80]))
            page.click('.calc-pre button >> nth=4')
            if "停不下來" not in page.inner_text(".lp-out"): errs.append((n, "loop infinite"))
        if page.locator("[data-calc=overflow]").count():
            if "-2147483648" not in page.inner_text(".calc-out"): errs.append((n, "calc default", page.inner_text(".calc-out")))
            page.click('.calc-pre button >> nth=3')
            if "4294967295" not in page.inner_text(".calc-out"): errs.append((n, "calc preset", page.inner_text(".calc-out")))
            page.fill("#cV", "abc")
            if "請輸入整數" not in page.inner_text(".calc-out"): errs.append((n, "calc invalid"))
        # Ladder
        for k in range(page.locator("[data-ladder]").count()):
            ld = page.locator("[data-ladder]").nth(k)
            if not ld.locator(".ld-row.yes").count(): errs.append((n, "ladder no yes row"))
            ld.locator(".calc-pre button >> nth=0").click()
            if ld.locator(".ld-row.yes").count() < 1: errs.append((n, "ladder preset"))
            if ld.locator("[data-brk]").count():
                ld.locator("[data-brk]").uncheck()
                if ld.locator(".ld-row.yes").count() < 2: errs.append((n, "switch fallthrough"))
        # Memory / BeforeAfter
        if page.locator("[data-mem]").count():
            m = page.locator("[data-mem]").first
            m.locator('[data-a="read"]').click()
            if not any(x in m.locator(".mem-out").inner_text() for x in ("75", "'l'")): errs.append((n, "mem read", m.locator(".mem-out").inner_text()))
            m.locator("input").first.fill("5"); m.locator('[data-a="read"]').click()
            if "越界" not in m.locator(".mem-out").inner_text() or not m.locator(".mem-cell.ghost.hl").count(): errs.append((n, "mem oob"))
            m.locator("input").first.fill("1"); m.locator('[data-a="write"]').click()
            if m.locator(".mem-v").nth(1).inner_text().strip() not in ("99", "X"): errs.append((n, "mem write"))
        if page.locator("[data-ba]:has([data-op=push])").count():
            bx = page.locator("[data-ba]:has([data-op=push])").first
            bx.locator('[data-op="push"]').click()
            if "= 4" not in bx.locator(".ba-size").inner_text(): errs.append((n, "ba push"))
            for _ in range(5): bx.locator('[data-op="pop"]').click()
            if "（空）" not in bx.locator(".ba-now").inner_text(): errs.append((n, "ba empty"))
            bx.locator('[data-op="pop"]').click()
            if "未定義" not in bx.locator(".ba-hist").inner_text(): errs.append((n, "ba pop empty"))
        # set / map 對照
        for kk in range(page.locator('[data-ba]').count()):
            bz = page.locator('[data-ba]').nth(kk)
            if bz.locator('[data-op="read"]').count():
                bz.locator("input").first.fill("grape"); bz.locator('[data-op="read"]').click()
                if "順手新增" not in bz.locator(".ba-hist").inner_text() or "= 3" not in bz.locator(".ba-size").inner_text(): errs.append((n, "map read trap"))
            elif bz.locator('[data-op="insert"]').count():
                bz.locator("input").first.fill("3"); bz.locator('[data-op="insert"]').click()
                if "不會重複" not in bz.locator(".ba-hist").inner_text(): errs.append((n, "set dup"))
        dup = page.evaluate("(() => { const s = {}, d = []; document.querySelectorAll('[id]').forEach(e => { if (s[e.id]) d.push(e.id); s[e.id] = 1; }); return d; })()")
        if dup: errs.append((n, "runtime dup id", dup))
        # Diagram
        for kk in range(page.locator("[data-diagram]").count()):
            dgm = page.locator("[data-diagram]").nth(kk)
            dgm.locator(".dg-m").first.click()
            if not dgm.locator(".dg-note").inner_text().strip(): errs.append((n, "diagram note"))
            if dgm.locator("[data-t]").count():
                seen = set()
                for t in range(dgm.locator("[data-t]").count()):
                    dgm.locator("[data-t]").nth(t).click(); seen.add(dgm.locator(".dg-res").inner_text().strip()[:1])
                if seen != {"✓", "✗"}: errs.append((n, "diagram tests should show both ok and bad", seen))
                if dgm.locator("[data-tog]").count():
                    dgm.locator("[data-tog]").uncheck(); dgm.locator("[data-t]").nth(1).click()
                    if "（某種聲音）" not in dgm.locator(".dg-res").inner_text(): errs.append((n, "virtual toggle off"))
        # 連結
        for h in page.eval_on_selector_all("a[href]", "els => els.map(e => e.getAttribute('href'))"):
            if h.startswith("http"): continue
            if h.startswith("#"):
                if page.locator(h).count() == 0: errs.append((n, "badanchor", h))
            elif not os.path.exists(os.path.normpath(os.path.join(PUB, "clang", h.split("#")[0]))): errs.append((n, "missing link", h))
        # 每個 details 都能展開
        d = page.locator("details").first; d.locator("summary").click()
        print(n, "ok: quiz/checks/copy/notes/flow/links")
        page.close()
    # 首頁
    page = ctx.new_page(); page.on("pageerror", lambda e: errs.append(("index", "pageerror", str(e))))
    page.goto("file://" + PUB + "/index.html#clang"); page.wait_for_timeout(250)
    print("index clang cards:", page.locator(".card").count(), "done:", page.locator(".card.done").count(), "title:", page.title())
    if page.locator(".card").count() != 18: errs.append(("index", "card count"))
    if "C++" not in page.inner_text("#heroH1"): errs.append(("index", "hero not switched"))
    page.click('#catTabs button[data-cat="github"]'); page.wait_for_timeout(100)
    if "GitHub" not in page.inner_text("#heroH1") or page.locator(".card").count() != 11: errs.append(("index", "github tab broken"))
    page.set_viewport_size({"width": 390, "height": 900})
    ov = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth"); print("index 390 overflow:", ov)
    if ov > 0: errs.append(("index", "overflow390"))
    b.close()
print("ERRORS:", errs)
sys.exit(1 if errs else 0)
