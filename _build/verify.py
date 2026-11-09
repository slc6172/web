import sys, os
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(os.path.dirname(HERE), "public")
BASE = "file://" + PUB + "/"
CHROME = os.environ.get("CHROME_PATH", "/usr/bin/google-chrome")
pages = ["index.html"] + ["github/github-%s-guide.html" % x for x in ("start","gitignore","branch","remote","issues","pr","review","undo","release","security","actions")]
errs = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
    for w in (1280, 390):
        for pg in pages:
            ctx = b.new_context(viewport={"width": w, "height": 900})
            page = ctx.new_page()
            page.on("pageerror", lambda e, pg=pg: errs.append((pg, "pageerror", str(e))))
            page.on("console", lambda m, pg=pg: errs.append((pg, "console", m.text)) if m.type == "error" else None)
            page.goto(BASE + pg)
            page.wait_for_timeout(300)
            ov = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            print(w, pg, "overflow:", ov)
            if w == 1280:
                page.screenshot(path=os.path.join(HERE, "shot_%s.png") % os.path.basename(pg).replace(".html", ""), full_page=False)
            ctx.close()
    # functional checks
    ctx = b.new_context(viewport={"width": 1280, "height": 900}); page = ctx.new_page()
    page.on("pageerror", lambda e: errs.append(("func", "pageerror", str(e))))
    page.goto(BASE + "index.html")
    print("cards:", page.locator(".card").count(), "done:", page.locator(".card.done").count())
    page.click('#filters button[data-f="done"]'); print("done filter:", page.locator(".card").count())
    page.click('#filters button[data-f="all"]')
    page.click('#pathStrip button[data-i="2"]'); print("stage 3 cards:", page.locator(".card").count())
    page.click('#pathStrip button[data-i="2"]')
    page.locator('input[data-r="github:1"]').check(); print("prog:", page.inner_text("#progTxt"))
    print("quick links:", page.locator("a.q").count(), "disabled:", page.locator(".q.off").count())
    page.click("a.q >> nth=0"); page.wait_for_timeout(300); print("quick ->", page.url.split("/")[-1])
    for pg in [p for p in pages[1:] if 'github-pr-' not in p]:
        page.goto(BASE + pg)
        page.click("#quizAns button >> nth=1"); page.wait_for_timeout(100)
        print(pg, "quiz fb:", page.locator("#quizFb.show").count(), "checks:", page.locator("#checks input").count())
        page.locator("#checks input").first.check(); print(" ", page.inner_text("#checkProgress"))
        if page.locator("#stages").count() and not page.locator("#tab-o").count():
            page.click("#nextStage"); print("  stage:", page.inner_text("#c-h"))
        if page.locator("#in-me").count():
            page.fill("#in-me", "alice"); print("  tpl:", page.locator(".cmd pre").nth(1).inner_text().splitlines()[0])
        if page.locator("#decideBtns button").count():
            page.click("#decideBtns button >> nth=5"); print("  decide:", page.inner_text("#decideOut")[:40].replace("\n"," "))
        if page.locator("#tab-o").count():
            page.click("#tab-o"); print("  role o visible:", page.locator("#panel-o").is_visible(), "c hidden:", not page.locator("#panel-c").is_visible())
            page.click("#nextStage"); print("  stage:", page.inner_text("#c-h"))
        if page.locator("[data-sim]").count():
            page.click("[data-sim] >> nth=0"); print("  sim:", page.inner_text(".sim-result")[:20])
        # link check
        import re
        hrefs = page.eval_on_selector_all("a[href]", "els => els.map(e => e.getAttribute('href'))")
        for h in hrefs:
            if h.startswith("http") or h.startswith("#"):
                if h.startswith("#") and page.locator(h).count() == 0: errs.append((pg, "badanchor", h))
                continue
            if not os.path.exists(os.path.normpath(os.path.join(PUB, "github", h))): print("  MISSING LINK:", h)
    b.close()
print("ERRORS:", errs)
