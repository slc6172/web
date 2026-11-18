"""單頁快速檢查(比 verify.py 快):python3 _build/microfilm/check.py angle lens [--shot]
每頁:1280/390 寬的橫向溢出、JS 錯誤、重複 id、http 連結、localStorage、題目/選擇題/動畫/滑桿的實際操作。--shot 會存 /tmp/mf_<頁>_<寬>.png(整頁)。"""
import sys, os, re
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared"))
from pwutil import stub_analytics
HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(os.path.dirname(os.path.dirname(HERE)), "public", "microfilm")
CHROME = os.environ.get("CHROME_PATH") or None   # 沒設定就用 Playwright 內建的 Chromium
names = [a for a in sys.argv[1:] if not a.startswith("--")]
shot = "--shot" in sys.argv
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
    for n in names:
        f = os.path.join(PUB, "microfilm-%s-guide.html" % n)
        src = open(f, encoding="utf-8").read()
        ids = re.findall(r'\bid="([^"]+)"', src)
        dup = sorted({i for i in ids if ids.count(i) > 1})
        urls = [u for u in re.findall(r'https?://[^"\'\s<)]+', src) if "w3.org" not in u]
        print("==", n, "lines", src.count("\n"), "KB", len(src.encode()) // 1024, "dupIDs", dup, "http", urls[:3], "localStorage", "localStorage" in src)
        for w in (1280, 390):
            errs = []
            ctx = b.new_context(viewport={"width": w, "height": 900}); stub_analytics(ctx); pg = ctx.new_page()
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.goto("file://" + f); pg.wait_for_timeout(250)
            ov = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            ops = []
            if pg.locator("#quizAns button").count():
                pg.click("#quizAns button >> nth=0"); ops.append("quiz")
            for i in range(pg.locator(".ch").count()):
                pg.locator(".ch .opts button").nth(i * 3).click(); ops.append("ch")
                break
            if pg.locator(".anim .play").count():
                pg.click(".anim .play >> nth=0"); pg.wait_for_timeout(500); ops.append("anim:%s" % pg.locator(".anim input[type=range] >> nth=0").input_value())
            for sel in ("#lab button", ".lab .opts button", ".fx button"):
                c = pg.locator(sel).count()
                if c > 1: pg.locator(sel).nth(1).click(); ops.append("click:" + sel)
            pg.wait_for_timeout(100)
            print(" ", w, "overflow", ov, "ops", ops, "errors", errs)
            if shot: pg.screenshot(path="/tmp/mf_%s_%d.png" % (n, w), full_page=True)
            ctx.close()
    b.close()
