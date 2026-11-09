# -*- coding: utf-8 -*-
"""verify_arduino.py — Arduino 頁面與首頁的瀏覽器驗證(Playwright)。用法: python3 verify_arduino.py"""
import os, re, sys, glob
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(os.path.dirname(HERE), "public")
BASE = "file://" + PUB + "/"
CHROME = os.environ.get("CHROME_PATH", "/opt/google/chrome/chrome")
pages = sorted(os.path.basename(f) for f in glob.glob(PUB + "/arduino/arduino-*-guide.html"))
errs, fails = [], []

def check(cond, msg):
    print(("  ok  " if cond else "  FAIL"), msg)
    if not cond:
        fails.append(msg)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
    for w in (1280, 390):
        for pg in pages:
            ctx = b.new_context(viewport={"width": w, "height": 900})
            page = ctx.new_page()
            page.on("pageerror", lambda e, pg=pg: errs.append((pg, str(e))))
            page.on("console", lambda m, pg=pg: errs.append((pg, m.text)) if m.type == "error" else None)
            page.goto(BASE + "arduino/" + pg); page.wait_for_timeout(300)
            ov = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            check(ov <= 0, "%s @%d 沒有橫向溢出(overflow=%d)" % (pg, w, ov))
            if w == 390:
                page.screenshot(path=os.path.join(HERE, "shots", "m_" + pg.replace(".html", ".png")), full_page=False)
            ctx.close()
    # ---- 功能檢查(每頁) ----
    for pg in pages:
        print("\n[%s]" % pg)
        ctx = b.new_context(viewport={"width": 1280, "height": 900}); page = ctx.new_page()
        page.on("pageerror", lambda e, pg=pg: errs.append((pg, str(e))))
        page.on("console", lambda m, pg=pg: errs.append((pg, m.text)) if m.type == "error" else None)
        page.goto(BASE + "arduino/" + pg); page.wait_for_timeout(300)
        ids = page.eval_on_selector_all("[id]", "els => els.map(e => e.id)")
        check(len(ids) == len(set(ids)), "沒有重複的 id")
        # 外部連結只能指向 Arduino 官方
        hrefs = page.eval_on_selector_all("a[href]", "els => els.map(e => e.getAttribute('href'))")
        for h in hrefs:
            if h.startswith("http"):
                check(re.match(r"https://(docs|support)\.arduino\.cc/", h) is not None or h.startswith("https://www.arduino.cc/"), "外部連結為 Arduino 官方:" + h[:70])
            elif h.startswith("#"):
                check(page.locator(h).count() > 0, "錨點存在:" + h)
            else:
                ok = os.path.exists(os.path.normpath(os.path.join(PUB, "arduino", h.split("#")[0])))
                check(ok, "內部連結存在:" + h)
        # 零元件:沒有外部資源
        html = open(os.path.join(PUB, "arduino", pg), encoding="utf-8").read()
        check("localStorage" not in html and "sessionStorage" not in html, "沒有使用 localStorage/sessionStorage")
        check(not re.search(r'<(script|link|img)[^>]+(src|href)="https?://', html), "沒有外部 script/link/img")
        # 測驗
        page.click("#quizAns button >> nth=1"); check(page.locator("#quizFb.show").count() == 1, "測驗作答後顯示回饋")
        page.locator("#checks input").first.check(); check("已完成 1 /" in page.inner_text("#checkProgress"), "檢查表可勾選")
        # 情境
        if page.locator("[data-sim]").count():
            page.click("[data-sim] >> nth=1"); check(len(page.inner_text(".sim-result")) > 10, "情境模擬可點選")
        # 填入
        if page.locator("input[data-k]").count():
            inp = page.locator("input[data-k]").first
            k = inp.get_attribute("data-k")
            allcode = lambda: "\n".join(page.locator(".cmd pre[data-tpl]").all_inner_texts())
            before = allcode()
            inp.fill("9")
            after = allcode()
            check(before != after and "9" in after, "填入欄位 %s=9 後,程式碼隨之更新" % k)
            page.click("#resetBtn"); check(allcode() == before, "Reset 後程式碼還原")
        # 接線播放
        for box in page.locator("[data-wiring]").all():
            n = box.locator(".wdot").count()
            check(box.locator(".wcap").inner_text().strip() != "", "接線播放:開始前有說明文字")
            for i in range(1, n + 1):
                box.locator('[data-w="next"]').click()
                cur = box.locator(".el.cur").count()
                fut = box.locator(".el.future").count()
                check(cur >= 1, "第 %d 步:目前零件有光圈(cur=%d、尚未放入=%d)" % (i, cur, fut))
            box.locator('[data-w="next"]').click()
            check(box.locator(".el.future").count() == 0 and box.locator(".el.cur").count() == 0, "完成後所有零件都已放入")
            box.locator('[data-w="reset"]').click()
            check(box.locator(".el.future").count() == box.locator(".el").count(), "Reset 後全部回到未放入")
            box.locator('[data-w="all"]').click()
        # 麵包板探索圖
        if page.locator("[data-bbx]").count():
            page.locator('[data-bbx] .bh[data-h="e7"]').click()
            on = page.locator("[data-bbx] .bh.on").count()
            check(on == 5, "麵包板探索:點 e7,同欄 a–e 共 5 個孔亮起(%d)" % on)
            page.locator('[data-bbx] .bh[data-h="t+3"]').click()
            n_full = page.locator("[data-bbx] .bh.on").count()
            page.locator(".bbx-split").check()
            n_split = page.locator("[data-bbx] .bh.on").count()
            check(n_full > n_split > 0, "電源軌:整條 %d 個孔;勾選『中間斷開』後只剩一半 %d 個" % (n_full, n_split))
        # 色環計算機
        if page.locator("[data-rcalc]").count():
            page.fill('[data-rc="val"]', "10k")
            txt = page.inner_text(".rc-out")
            check("棕、黑、橙" in txt and "10 kΩ" in txt, "色環計算機:10k → 棕黑橙")
            page.fill('[data-rc="val"]', "4.7k")
            check("黃、紫、紅" in page.inner_text(".rc-out"), "色環計算機:4.7k → 黃紫紅")
            page.select_option('[data-rc="b1"]', "3"); page.select_option('[data-rc="b2"]', "3"); page.select_option('[data-rc="b3"]', "1")
            check("330" in page.inner_text(".rc-out"), "色環計算機:橙橙棕 → 330 Ω")
        if page.locator("[data-ledcalc]").count():
            page.select_option('[data-lc="vf"]', "2.0"); page.fill('[data-lc="ma"]', "10")
            check("300 Ω" in page.inner_text(".lc-out") and "330" in page.inner_text(".lc-out"), "LED 計算機:紅 LED 10 mA → 300 Ω → 取 330 Ω")
            page.fill('[data-lc="ma"]', "30")
            check("超過" in page.inner_text(".lc-out"), "LED 計算機:30 mA 會警告超過 20 mA")
        # 按鈕與上拉示意
        if page.locator("[data-btnsim]").count():
            check("HIGH(1)" in page.text_content(".bs-level"), "按鈕示意:預設(上拉、放開)讀 HIGH")
            page.click('[data-bs="btn"]'); check("LOW(0)" in page.text_content(".bs-level"), "按鈕示意:按下讀 LOW")
            page.select_option('[data-bs="mode"]', "plain"); page.click('[data-bs="btn"]')
            check("不確定" in page.text_content(".bs-level"), "按鈕示意:INPUT 模式放開 → 浮接(不確定)")
        # 鮑率亂碼示意
        if page.locator("[data-baudsim]").count():
            check("Hello" in page.text_content(".bd-screen"), "鮑率示意:一致時文字正常")
            page.select_option('[data-bd="monitor"]', "115200")
            check("Hello" not in page.text_content(".bd-screen") and "亂碼" in page.inner_text(".bd-note"), "鮑率示意:不一致時變亂碼")
        # 電位器分壓示意
        if page.locator("[data-potsim]").count():
            page.fill('[data-pot="v"]', "50")
            txt = page.inner_text(".pot-out")
            check("2.50 V" in txt and "5.0 kΩ" in txt, "電位器示意:旋鈕 50% → 2.50 V、上下段各 5.0 kΩ")
            page.fill('[data-pot="v"]', "100")
            check("1023" in page.inner_text(".pot-out"), "電位器示意:旋鈕 100% → analogRead = 1023")
        # 光敏電阻分壓示意
        if page.locator("[data-ldrsim]").count():
            page.fill('[data-ldr="v"]', "0")
            check("LED 亮" in page.inner_text(".ldr-out"), "光敏電阻示意:全黑 → 低於門檻 → LED 亮")
            page.fill('[data-ldr="v"]', "100")
            check("LED 滅" in page.inner_text(".ldr-out"), "光敏電阻示意:很亮 → LED 滅")
        # PWM 示意
        if page.locator("[data-pwmbox]").count():
            page.fill('[data-pwm="num"]', "128")
            check("50%" in page.inner_text("[data-pwmbox] .rc-out") and page.locator(".pwm-wave").get_attribute("points") != "", "PWM 示意:analogWrite 128 → 50%、波形已繪出")
            page.fill('[data-pwm="num"]', "0")
            check("全滅" in page.inner_text("[data-pwmbox] .rc-out"), "PWM 示意:0 → 全滅")
        # 原理圖連動
        sch = page.locator('#sch .el[data-part]')
        if sch.count():
            ref = sch.first.get_attribute("data-part")
            sch.first.click()
            hl = page.locator('.el.hl[data-part="%s"]' % ref).count()
            check(hl >= 2, "點原理圖零件 %s,原理圖與麵包板同時高亮(%d 處)" % (ref, hl))
            check("麵包板" in page.locator(".linkbox").last.inner_text(), "連動說明框顯示對應說明")
            sch.first.focus(); page.keyboard.press("Enter")
            check(page.locator(".el.hl").count() == 0, "再按一次(鍵盤 Enter)取消高亮")
        ctx.close()
    # ---- 首頁 ----
    print("\n[index.html]")
    ctx = b.new_context(viewport={"width": 1280, "height": 900}); page = ctx.new_page()
    page.on("pageerror", lambda e: errs.append(("index", str(e))))
    page.goto(BASE + "index.html"); page.wait_for_timeout(200)
    gh_h1 = page.inner_text("#heroH1")
    check(page.locator(".card").count() == 11, "預設 GitHub 分頁有 11 張卡")
    page.click('#catTabs button[data-cat="arduino"]'); page.wait_for_timeout(100)
    check("Arduino" in page.inner_text("#heroH1"), "切到 Arduino:標題換成 Arduino 版本")
    check("Arduino" in page.inner_text("#siteFoot") and "GitHub" not in page.inner_text("#siteFoot"), "切到 Arduino:頁尾換成 Arduino 版本")
    check(page.locator(".card").count() == 20, "Arduino 分頁有 20 張卡(%d)" % page.locator(".card").count())
    check(page.locator(".card.done").count() == len([x for x in pages]), "已完成卡片數 = 已建置頁面數(%d)" % len(pages))
    check(page.locator("#pathStrip button").count() == 6, "學習路徑有 6 個階段")
    check(page.locator("a.q, .q.off").count() == 8, "快速入口 8 條;可點 %d 條" % page.locator("a.q").count())
    page.click('#filters button[data-f="elective"]'); check(page.locator(".card").count() == 2, "進階選讀篩選 = 2 篇")
    page.click('#catTabs button[data-cat="github"]'); page.wait_for_timeout(100)
    check(page.inner_text("#heroH1") == gh_h1 and page.locator(".card").count() == 11, "切回 GitHub:標題與 11 張卡恢復")
    page.goto(BASE + "index.html#arduino"); page.wait_for_timeout(200)
    check("Arduino" in page.inner_text("#heroH1"), "網址 #arduino 直接開 Arduino 分頁")
    page.locator('input[data-r="arduino:3"]').check(); check("已讀 1 / 20" in page.inner_text("#progTxt"), "Arduino 進度獨立計算(已讀 1 / 20)")
    page.screenshot(path=os.path.join(HERE, "shots", "index_arduino.png"))
    ctx.close()
    b.close()
print("\nJS/console 錯誤:", errs)
print("失敗項目:", fails if fails else "無")
sys.exit(1 if (errs or fails) else 0)
