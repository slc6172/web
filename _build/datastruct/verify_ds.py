"""datastruct 主題驗證:1280 / 390 寬溢出、JS 錯誤、播放器互動、測驗與檢查表、連結。
用法: python3 _build/datastruct/verify_ds.py [檔名片段 ...]   環境變數 CHROME_PATH(預設 /tmp/chromium，沒有就用 Playwright 內建 Chromium)"""
import sys, os, re, glob
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.dirname(HERE)
PUB = os.path.join(os.path.dirname(BUILD), "public")            # 製作檔在 _build/datastruct/，往上兩層才是 repo 根目錄
sys.path.insert(0, os.path.join(BUILD, "shared"))
from pwutil import stub_analytics
import seo
DS = os.path.join(PUB, "datastruct")
CHROME = os.environ.get("CHROME_PATH") or ("/tmp/chromium" if os.path.exists("/tmp/chromium") else None)   # None = Playwright 內建的 Chromium
ARGS = ["--no-sandbox", "--headless=new", "--disable-gpu", "--single-process", "--no-zygote"]
want = sys.argv[1:]
files = sorted(glob.glob(DS + "/datastruct-*-guide.html"))
if want: files = [f for f in files if any(w in f for w in want)]
errs = []; shots = os.path.join(__import__("tempfile").gettempdir(), "datastruct-shots")   # 截圖放暫存資料夾，不進 repo; os.makedirs(shots, exist_ok=True)

def launch(p):
    for i in range(4):
        try: return p.chromium.launch(executable_path=CHROME, args=ARGS)
        except Exception as ex:
            if i == 3: raise
def widgets(page):
    return page.eval_on_selector_all(".algo-w", "els => els.map(e => e.id)")

with sync_playwright() as p:
    for f in files:
        name = os.path.basename(f)
        for w in (1280, 390):
            b = launch(p)
            ctx = b.new_context(viewport={"width": w, "height": 900}); stub_analytics(ctx); page = ctx.new_page(); page.set_default_timeout(5000)
            page.on("pageerror", lambda e, n=name: errs.append((n, "pageerror", str(e))))
            page.on("console", lambda m, n=name: errs.append((n, "console", m.text)) if m.type == "error" else None)
            page.goto("file://" + f); page.wait_for_timeout(250)
            ov = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            print(w, name, "overflow:", ov)
            if ov > 0: errs.append((name, "overflow", w))
            # 每個 widget:執行 → 下一步到底 → 上一步 → 重設,並檢查程式碼行高亮
            for wid in widgets(page):
                sel = "#" + wid
                page.locator(sel).scroll_into_view_if_needed()
                page.click(sel + ' [data-a="run"]'); page.wait_for_timeout(60)
                total = page.evaluate("document.querySelector('%s')._algo.frames().length" % sel)
                hl = 0
                for i in range(total - 1):
                    page.click(sel + ' [data-a="next"]')
                    hl += page.locator(sel + " .algo-code .l.on").count()
                page.click(sel + ' [data-a="prev"]'); page.keyboard.press("Escape")
                page.click(sel + ' [data-a="play"]'); page.wait_for_timeout(120); page.click(sel + ' [data-a="play"]')
                if w == 1280 or True:
                    page.screenshot(path=os.path.join(shots, "%s_%s_%d.png" % (name.replace(".html", ""), wid, w)), clip=None) if False else None
                page.locator(sel).screenshot(path=os.path.join(shots, "%s_%s_%d.png" % (name[:-5], wid, w)))
                page.click(sel + ' [data-a="reset"]')
                print("   widget", wid, "frames:", total, "highlighted-steps:", hl)
                if total < 2: errs.append((name, "widget-no-frames", wid))
            if page.locator(".cv-chart").count():
                page.evaluate("(()=>{const r=document.querySelector('.cv input');r.value=100;r.dispatchEvent(new Event('input'))})()")
                rows = page.locator(".cv tbody tr").count()
                if rows != 6 or "宇宙" not in page.inner_text(".cv tbody"): errs.append((name, "curves", rows))
                else: print("   curves ok (n=100)")
            if w == 1280:
                # 測驗 / 檢查表 / sim / 複製
                page.click("#quizAns button >> nth=1"); page.wait_for_timeout(80)
                if page.locator("#quizFb.show").count() != 1: errs.append((name, "quiz", ""))
                page.locator("#checks input").first.check()
                if "已完成 1" not in page.inner_text("#checkProgress"): errs.append((name, "checks", ""))
                if page.locator("[data-sim]").count():
                    page.click("[data-sim] >> nth=0")
                    if not page.inner_text(".sim-result").strip(): errs.append((name, "sim", ""))
                page.locator(".cmd .copy").first.click(); page.wait_for_timeout(80)
                # 程式碼高亮後 textContent 仍是原始碼(換行不能掉)
                n_lines = page.evaluate("(()=>{const p=document.querySelector('pre[data-cpp]');return [p.textContent.split('\\n').length, p.querySelectorAll('.l').length]})()")
                if abs(n_lines[0] - n_lines[1]) > 1: errs.append((name, "cpp-lines", n_lines))
                # 連結
                hrefs = page.eval_on_selector_all("a[href]", "els => els.map(e => e.getAttribute('href'))")
                for h in hrefs:
                    if h.startswith("http"): continue
                    if h.startswith("#"):
                        if page.locator(h).count() == 0: errs.append((name, "badanchor", h))
                        continue
                    if not os.path.exists(os.path.normpath(os.path.join(DS, h.split("#")[0]))): print("   (連結目標尚未製作)", h)
                # 表格版面:每個 .gt 的每一格至少 50px 寬(class 不存在會塌成一欄)
                narrow = page.evaluate("[...document.querySelectorAll('.gt .cell')].filter(c => (c.getBoundingClientRect().width > 0 && c.getBoundingClientRect().width < 50)).length")
                if narrow: errs.append((name, "table-collapsed", narrow))
                ids = page.eval_on_selector_all("[id]", "els => els.map(e => e.id)")
                dup = sorted({i for i in ids if ids.count(i) > 1})
                if dup: errs.append((name, "dup-id", dup))
            b.close()
        src = open(f, encoding="utf-8").read()
        if "localStorage" in src: errs.append((name, "localStorage", ""))
        ext = [u for u in re.findall(r"https?://[^\"'\s<>)]+", src) if "w3.org" not in u and "cppreference.com" not in u and not (seo.SITE_URL and u.startswith(seo.SITE_URL)) and "cloudflareinsights.com" not in u]
        if ext: errs.append((name, "external", ext))
print("ERRORS:", errs)
sys.exit(1 if errs else 0)
