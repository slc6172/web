# -*- coding: utf-8 -*-
"""arduino_verify.py — Arduino 主題的三層驗證:接線電氣檢查、程式與接線一致、編譯 + simavr 模擬。
用法: python3 arduino_verify.py a03 a04 ...   (不帶參數 = 驗證全部已存在的 aNN.py)
輸出: 終端摘要 + reports/arduino-verify-report.md
"""
import sys, os, re, glob, subprocess, importlib, datetime, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bb

CORE = "/tmp/ArduinoCore-avr"
OBJ = "/tmp/avrcore_obj"
SIMPIN = os.path.join(HERE, "tools", "simpin")
CFLAGS = ["-mmcu=atmega328p", "-DF_CPU=16000000UL", "-DARDUINO=10819", "-DARDUINO_AVR_UNO", "-DARDUINO_ARCH_AVR",
          "-Os", "-ffunction-sections", "-fdata-sections", "-Wall", "-Wno-unused-variable"]


def sh(cmd, **kw):
    return subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True, **kw)


def ensure_env():
    if not (shutil.which("avr-gcc") and os.path.isdir(CORE) and os.path.exists(SIMPIN)):
        print("環境未就緒,執行 tools/setup_env.sh …")
        r = sh(["sh", os.path.join(HERE, "tools", "setup_env.sh")])
        if r.returncode != 0:
            print(r.stdout, r.stderr)
            sys.exit("環境建立失敗")


def core_objects():
    os.makedirs(OBJ, exist_ok=True)
    inc = ["-I%s/cores/arduino" % CORE, "-I%s/variants/standard" % CORE]
    objs = []
    for f in sorted(glob.glob(CORE + "/cores/arduino/*.c") + glob.glob(CORE + "/cores/arduino/*.cpp") + glob.glob(CORE + "/cores/arduino/*.S")):
        o = os.path.join(OBJ, os.path.basename(f) + ".o")
        objs.append(o)
        if os.path.exists(o):
            continue
        if f.endswith(".c"):
            r = sh(["avr-gcc"] + CFLAGS + inc + ["-c", f, "-o", o])
        elif f.endswith(".S"):
            r = sh(["avr-gcc"] + CFLAGS + inc + ["-x", "assembler-with-cpp", "-c", f, "-o", o])
        else:
            r = sh(["avr-g++"] + CFLAGS + inc + ["-std=gnu++11", "-fno-exceptions", "-c", f, "-o", o])
        if r.returncode != 0:
            sys.exit("核心編譯失敗:%s\n%s" % (f, r.stderr[:600]))
    return objs, inc


def fill_code(code, fill):
    return re.sub(r"\{([A-Za-z0-9_]+)\}", lambda m: fill.get(m.group(1), m.group(0)), code)


def compile_sketch(name, code, libs=()):
    objs, inc = core_objects()
    wd = os.path.join("/tmp", "avrbuild", name)
    os.makedirs(wd, exist_ok=True)
    src = os.path.join(wd, name + ".cpp")
    open(src, "w", encoding="utf-8").write("#include <Arduino.h>\n" + code)
    extra_inc, extra_src = [], []
    for lib in libs:
        base = CORE + "/libraries/" + lib + "/src"
        if not os.path.isdir(base):
            base = "/tmp/avrlibs/" + lib + ("/src" if os.path.isdir("/tmp/avrlibs/%s/src" % lib) else "")
        extra_inc.append("-I" + base)
        extra_src += glob.glob(base + "/*.cpp") + glob.glob(base + "/utility/*.c") + glob.glob(base + "/utility/*.cpp")
    outs = []
    for f in [src] + extra_src:
        o = os.path.join(wd, os.path.basename(f) + ".o")
        r = sh(["avr-g++"] + CFLAGS + inc + extra_inc + ["-std=gnu++11", "-fno-exceptions", "-c", f, "-o", o])
        if r.returncode != 0:
            return False, r.stderr[:800], None
        outs.append(o)
    elf = os.path.join(wd, name + ".elf")
    r = sh(["avr-gcc", "-mmcu=atmega328p", "-Wl,--gc-sections"] + outs + objs + ["-lm", "-o", elf])
    if r.returncode != 0:
        return False, r.stderr[:800], None
    sz = sh(["avr-size", elf]).stdout.strip().splitlines()[-1].split()
    flash, ram = int(sz[0]) + int(sz[1]), int(sz[1]) + int(sz[2])
    return True, "Flash %d / 32256 bytes(%d%%)、SRAM %d / 2048 bytes(%d%%)" % (flash, flash * 100 // 32256, ram, ram * 100 // 2048), elf


def uno_to_port(pin):   # 'D8' -> 'B0'
    n = int(pin[1:])
    if pin[0] == "D":
        return ("D%d" % n) if n <= 7 else ("B%d" % (n - 8))
    return "C%d" % n


def simulate(elf, pin, seconds):
    r = sh([SIMPIN, elf, str(seconds), uno_to_port(pin)], timeout=120)
    ev = []
    for line in r.stdout.splitlines():
        if line.startswith("PIN "):
            _, _, t, lv = line.split()
            ev.append((float(t), int(lv)))
    return ev


def check_toggle(ev, period, tol):
    if len(ev) < 4:
        return False, "只觀察到 %d 次電位變化" % len(ev)
    ev = ev[1:]                                     # 第一筆是腳位初始化
    ev = [e for i, e in enumerate(ev) if i == 0 or e[1] != ev[i - 1][1]]
    gaps = [round(ev[i + 1][0] - ev[i][0], 2) for i in range(len(ev) - 1)]
    ok = all(abs(g - period) <= tol for g in gaps)
    lv = [e[1] for e in ev]
    alt = all(lv[i] != lv[i + 1] for i in range(len(lv) - 1))
    return ok and alt, "電位交替翻轉 %d 次,間隔 %s ms(預期 %d ± %d)" % (len(ev), "、".join("%.1f" % g for g in gaps[:4]) + (" …" if len(gaps) > 4 else ""), period, tol)


def simulate_multi(elf, pins, seconds):
    r = sh([SIMPIN, elf, str(seconds)] + [uno_to_port(p) for p in pins], timeout=120)
    ev = {p: [] for p in pins}
    names = {uno_to_port(p): p for p in pins}
    for line in r.stdout.splitlines():
        if line.startswith("PIN "):
            _, n, t, lv = line.split()
            ev[names[n]].append((float(t), int(lv)))
    return ev


def check_chase(ev, pins, ms, tol):
    """流水燈:第 k 顆在 k*ms + n*(顆數*ms) 亮起,每次亮 ms 毫秒。"""
    n = len(pins)
    msgs, ok = [], True
    rises0 = [t for t, l in ev[pins[0]][1:] if l == 1]
    if not rises0:
        return False, "第一顆沒有亮起"
    t0 = rises0[0]
    for k, p in enumerate(pins):
        seq = ev[p][1:]
        rises = [t for t, l in seq if l == 1]
        falls = [t for t, l in seq if l == 0]
        if len(rises) < 2 or not falls:
            return False, "%s 的亮滅次數不足" % p
        for j, t in enumerate(rises[:3]):
            want = t0 + k * ms + j * n * ms
            if abs(t - want) > tol:
                ok = False
                msgs.append("%s 第 %d 次亮起 %.0f ms(預期 %.0f)" % (p, j + 1, t, want))
        dur = [round(f - r, 1) for r, f in zip(rises, falls) if f > r]
        if not all(abs(d - ms) <= tol for d in dur[:3]):
            ok = False
            msgs.append("%s 亮的長度 %s ms(預期 %d)" % (p, dur[:3], ms))
    return ok, ("、".join(msgs) if msgs else "%d 顆依序亮起,每顆亮 %d ms,輪一圈 %d ms,誤差 ≤ %d ms" % (n, ms, n * ms, tol))


def simulate_in(elf, pin, seconds, inputs):
    """inputs: [(輸入腳位如 'D2', 電位 0/1, 毫秒), ...] 模擬按鈕等外部輸入;回傳輸出腳位的電位變化。"""
    args = [SIMPIN, elf, str(seconds), uno_to_port(pin)] + ["IN@%s=%d@%s" % (uno_to_port(p), lv, t) for p, lv, t in inputs]
    r = sh(args, timeout=120)
    ev = []
    for line in r.stdout.splitlines():
        if line.startswith("PIN "):
            _, _, t, lv = line.split()
            ev.append((float(t), int(lv)))
    return ev


def check_edges(ev, expect, tol):
    """輸出腳位的電位變化是否依序等於 expect=[(電位, 毫秒), ...](忽略初始化的前 50 ms)。"""
    got = [(l, t) for t, l in ev if t > 50]
    ok = len(got) == len(expect) and all(g[0] == e[0] and abs(g[1] - e[1]) <= tol for g, e in zip(got, expect))
    return ok, "輸出腳位的變化:%s(預期 %s,誤差 ≤ %d ms)" % (["%d@%.0f" % (l, t) for l, t in got], ["%d@%d" % e for e in expect], tol)


def simulate_uart(elf, seconds, pin=None, inputs=(), rx=(), adc=()):
    """回傳 (序列埠輸出文字, 輸出腳位電位變化)。inputs: [(腳位, 電位, ms)];rx: [(ms, 位元組)]。"""
    args = [SIMPIN, elf, str(seconds)] + ([uno_to_port(pin)] if pin else [])
    args += ["IN@%s=%d@%s" % (uno_to_port(p), lv, t) for p, lv, t in inputs] + ["RX@%s=%d" % (t, b) for t, b in rx] + ["ADC@%d=%d@%s" % a for a in adc]
    r = sh(args, timeout=120)
    data, ev = bytearray(), []
    for line in r.stdout.splitlines():
        if line.startswith("UART "):
            data.append(int(line.split()[1]))
        elif line.startswith("PIN "):
            _, _, t, lv = line.split()
            ev.append((float(t), int(lv)))
    return data.decode("utf-8", "replace"), ev


def check_uart(text, expect):
    """expect:依序必須出現的字串清單。"""
    pos, missing = 0, []
    for e_ in expect:
        i = text.find(e_, pos)
        if i < 0:
            missing.append(e_)
        else:
            pos = i + len(e_)
    return (not missing), ("序列埠輸出依序包含 %s" % [x.replace("\r\n", "↵") for x in expect] if not missing else "缺少 %s;實際輸出:%r" % (missing, text[:120]))


def simulate_adc(elf, seconds, adc, pin=None, reg=None):
    """adc: [(通道, 毫伏, ms)];pin: 觀察輸出腳位;reg: 取樣 OCR 暫存器位址。回傳 (腳位事件, 暫存器取樣)。"""
    args = [SIMPIN, elf, str(seconds)] + ([uno_to_port(pin)] if pin else []) + ["ADC@%d=%d@%s" % a for a in adc] + (["REG@%x" % reg] if reg else [])
    r = sh(args, timeout=120)
    ev, regs = [], []
    for line in r.stdout.splitlines():
        if line.startswith("PIN "):
            _, _, t, lv = line.split()
            ev.append((float(t), int(lv)))
        elif line.startswith("REG "):
            _, _, t, val = line.split()
            regs.append((float(t), int(val)))
    return ev, regs


def check_reg_at(regs, expect, tol):
    """expect:[(時間 ms, 暫存器值)];在該時間點(±10 ms 取樣)的值要接近。"""
    bad, got = [], []
    for t, want in expect:
        val = min(regs, key=lambda s: abs(s[0] - t))[1]
        got.append((t, val))
        if abs(val - want) > tol:
            bad.append((t, val, want))
    return (not bad), "在 %s 取得的 PWM 暫存器值 %s(預期 %s,誤差 ≤ %d)" % ([g[0] for g in got], [g[1] for g in got], [e_[1] for e_ in expect], tol)


def simulate_reg(elf, addr, seconds):
    r = sh([SIMPIN, elf, str(seconds), "REG@%x" % addr], timeout=120)
    out = []
    for line in r.stdout.splitlines():
        if line.startswith("REG "):
            _, a, t, val = line.split()
            out.append((float(t), int(val)))
    return out


def check_ocr(samples, up_ms, tol):
    """analogWrite 的值寫在 OCR 暫存器:確認它 0 → 255 → 0 依時間變化。
    註:Arduino 核心對 analogWrite(pin, 255) 直接輸出 HIGH、不寫 OCR,所以暫存器最大值會是 250(255 的前一階)。"""
    vals = [v for _, v in samples]
    top = max(vals)
    t_top = next(t for t, v in samples if v == top)
    mid = min(samples, key=lambda s: abs(s[0] - up_ms / 2.0))[1]
    low = min(v for t, v in samples if abs(t - 2 * up_ms) <= 80)
    ok = top >= 250 and abs(t_top - up_ms) <= tol and 110 <= mid <= 150 and vals[0] <= 5 and low <= 10
    return ok, "OCR 暫存器:最大值 %d 出現在 %.0f ms(預期 %d ± %d;255 會被核心改成直接輸出 HIGH)、上升段中點 %d(預期約 128)、一輪結束時降到 %d" % (top, t_top, up_ms, tol, mid, low)


def check_pwm(ev, seconds, up_ms, tol):
    """呼吸燈:每 40 ms 一個視窗算工作週期;最亮的時間點 ≈ up_ms,且上升段中間約 50%。"""
    seq = ev[1:]
    win, duties = 40.0, []
    t = 0.0
    level, last = 0, 0.0
    i = 0
    while t + win <= seconds * 1000:
        high = 0.0
        cur_t, lv = t, level
        while i < len(seq) and seq[i][0] < t + win:
            if lv:
                high += seq[i][0] - cur_t
            cur_t, lv = seq[i][0], seq[i][1]
            i += 1
        if lv:
            high += t + win - cur_t
        level = lv
        duties.append(high / win)
        t += win
    peak = max(range(len(duties)), key=lambda k: duties[k])
    tpk = peak * win
    mid = duties[int((up_ms / 2) / win)]
    ok = duties[peak] > 0.9 and abs(tpk - up_ms) <= tol and 0.35 < mid < 0.65 and duties[0] < 0.15
    return ok, "最亮在 %.0f ms(預期 %d ± %d)、峰值工作週期 %.0f%%、上升段中點 %.0f%%、起點 %.0f%%" % (tpk, up_ms, tol, duties[peak] * 100, mid * 100, duties[0] * 100)


def check_pattern(ev, seq, tol, cycles=2):
    """依序比對電位持續時間。seq = [(電位, 持續毫秒), ...],重複 cycles 輪。"""
    ev = ev[1:]
    gaps = [(ev[i][1], ev[i + 1][0] - ev[i][0]) for i in range(len(ev) - 1)]
    want = list(seq) * cycles
    if len(gaps) < len(want):
        return False, "只觀察到 %d 段,預期至少 %d 段" % (len(gaps), len(want))
    bad = [(i, g, w) for i, (g, w) in enumerate(zip(gaps, want)) if g[0] != w[0] or abs(g[1] - w[1]) > tol]
    return (not bad), ("前 %d 段電位與時間都符合(誤差 ≤ %d ms)" % (len(want), tol) if not bad else "不符合:%s" % bad[:3])


def check_freq(ev, window_ms, hz, tol_pct):
    rises = [t for t, l in ev[1:] if l == 1 and t <= window_ms]
    n = len(rises)
    want = hz * window_ms / 1000.0
    ok = abs(n - want) <= want * tol_pct / 100.0
    return ok, "前 %d ms 內有 %d 個脈衝(預期約 %d,即 %d Hz)" % (window_ms, n, want, hz)


def code_arrays(code):
    out = {}
    for m in re.finditer(r"const\s+(?:int|byte|uint8_t)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\[\s*\d*\s*\]\s*=\s*\{([^}]*)\}", code):
        out[m.group(1)] = [int(x) for x in re.findall(r"\d+", m.group(2))]
    return out


def code_pins(code):
    out = {}
    for m in re.finditer(r"const\s+(?:int|byte|uint8_t)\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(\d+)\s*;", code):
        out[m.group(1)] = int(m.group(2))
    return out


def verify_module(name, report):
    m = importlib.import_module(name)
    ok_all = True
    report.append("## %s — %s\n" % (name, m.SPEC["title"]))
    for c in getattr(m, "CIRCUITS", []):
        report.append("### 接線:`%s`\n" % c.id)
        for lv, msg in bb.check(c):
            mark = {"ok": "✅", "warn": "⚠️", "error": "❌"}[lv]
            report.append("- %s %s" % (mark, msg))
            if lv == "error":
                ok_all = False
        report.append("")
    for sk in getattr(m, "SKETCHES", []):
        report.append("### 程式:`%s`\n" % sk["name"])
        code = fill_code(sk["code"], sk["fill"])
        left = re.findall(r"\{[A-Za-z0-9_]+\}", code)
        if left:
            report.append("- ❌ 還有未填入的佔位符:%s" % left)
            ok_all = False
        circ = sk.get("circuit")
        cpins = sk.get("code_pins", circ.code_pins if circ is not None else {})
        if circ is not None and cpins:
            consts, arrs = code_pins(code), code_arrays(code)
            for const, unopin in cpins.items():
                if isinstance(unopin, (list, tuple)):
                    want = [int(u.split("D")[-1]) for u in unopin]
                    got = arrs.get(const)
                else:
                    want = int(unopin.split("D")[-1]) if ".D" in unopin else None
                    got = consts.get(const)
                good = got is not None and got == want
                report.append("- %s 程式 `%s = %s` ↔ 接線 `%s`" % ("✅" if good else "❌", const, got, unopin))
                ok_all &= good
        ok, msg, elf = compile_sketch(sk["name"], code, sk.get("libs", ()))
        report.append("- %s 編譯(avr-gcc + 官方 ArduinoCore-avr):%s" % ("✅" if ok else "❌", msg))
        if not ok:
            ok_all = False
            continue
        s = sk.get("sim")
        if s and s.get("kind") == "chase":
            ev = simulate_multi(elf, s["pins"], s["seconds"])
            good, msg2 = check_chase(ev, s["pins"], s["ms"], s["tol_ms"])
            report.append("- %s 模擬(simavr,%.1f 秒):%s ── %s" % ("✅" if good else "❌", s["seconds"], "、".join(s["pins"]), msg2))
            ok_all &= good
        elif s and s.get("kind") == "adc_pwm":
            ev, regs = simulate_adc(elf, s["seconds"], s["adc"], reg=s["addr"])
            good, msg2 = check_reg_at(regs, s["expect"], s["tol"])
            report.append("- %s 模擬(simavr,%.1f 秒,注入類比電壓 %s):%s" % ("✅" if good else "❌", s["seconds"], s["note"], msg2))
            ok_all &= good
        elif s and s.get("kind") == "adc_edges":
            ev, regs = simulate_adc(elf, s["seconds"], s["adc"], pin=s["pin"])
            good, msg2 = check_edges(ev, s["expect"], s["tol_ms"])
            report.append("- %s 模擬(simavr,%.1f 秒,注入類比電壓 %s):%s" % ("✅" if good else "❌", s["seconds"], s["note"], msg2))
            ok_all &= good
        elif s and s.get("kind") == "adc_toggle":
            ev, regs = simulate_adc(elf, s["seconds"], s["adc"], pin=s["pin"])
            good, msg2 = check_toggle(ev, s["period_ms"], s["tol_ms"])
            report.append("- %s 模擬(simavr,%.1f 秒,注入類比電壓 %s):%s 腳 %s" % ("✅" if good else "❌", s["seconds"], s["note"], s["pin"], msg2))
            ok_all &= good
        elif s and s.get("kind") == "uart":
            text, ev = simulate_uart(elf, s["seconds"], s.get("pin"), s.get("inputs", ()), s.get("rx", ()), s.get("adc", ()))
            good, msg2 = check_uart(text, s["expect"])
            if good and s.get("edges"):
                g2, m2 = check_edges(ev, s["edges"], s.get("tol_ms", 5))
                good, msg2 = g2, msg2 + ";" + m2
            report.append("- %s 模擬(simavr,%.1f 秒,UART):%s" % ("✅" if good else "❌", s["seconds"], msg2))
            ok_all &= good
        elif s and s.get("kind") == "input":
            ev = simulate_in(elf, s["pin"], s["seconds"], s["inputs"])
            good, msg2 = check_edges(ev, s["expect"], s["tol_ms"])
            report.append("- %s 模擬(simavr,%.1f 秒,注入按鈕輸入 %s):%s" % ("✅" if good else "❌", s["seconds"], s["note"], msg2))
            ok_all &= good
        elif s and s.get("kind") == "ocr":
            samples = simulate_reg(elf, s["addr"], s["seconds"])
            good, msg2 = check_ocr(samples, s["up_ms"], s["tol_ms"])
            report.append("- %s 模擬(simavr,%.1f 秒,取樣 PWM 暫存器 OCR 0x%X,對應 %s):%s" % ("✅" if good else "❌", s["seconds"], s["addr"], s["pin"], msg2))
            ok_all &= good
        elif s and s.get("kind") in ("pwm", "pattern", "freq"):
            ev = simulate(elf, s["pin"], s["seconds"])
            if s["kind"] == "pwm":
                good, msg2 = check_pwm(ev, s["seconds"], s["up_ms"], s["tol_ms"])
            elif s["kind"] == "pattern":
                good, msg2 = check_pattern(ev, s["seq"], s["tol_ms"])
            else:
                good, msg2 = check_freq(ev, s["window_ms"], s["hz"], s["tol_pct"])
            report.append("- %s 模擬(simavr,%.1f 秒):%s 腳 ── %s" % ("✅" if good else "❌", s["seconds"], s["pin"], msg2))
            ok_all &= good
        elif s:
            ev = simulate(elf, s["pin"], s["seconds"])
            good, msg2 = check_toggle(ev, s["period_ms"], s["tol_ms"])
            report.append("- %s 模擬(simavr,%.1f 秒):%s 腳 %s" % ("✅" if good else "❌", s["seconds"], s["pin"], msg2))
            ok_all &= good
        report.append("")
    return ok_all


def main(names):
    ensure_env()
    if not names:
        names = sorted(os.path.basename(f)[:-3] for f in glob.glob(HERE + "/a[0-9][0-9].py"))
    report = ["# Arduino 主題驗證報告\n", "產生時間:%s\n" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
              "驗證項目:① 麵包板規則算出的實際連線 = 原理圖預期電路;② 程式腳位 = 接線腳位;③ 程式實際編譯;④ simavr 模擬腳位行為。",
              "**驗證不到的**:實體零件的個別差異(模組腳位順序、LCD 對比度、I2C 位址)、IDE 畫面。這些以官方文件為準並在頁面寫成「先確認再接」。\n"]
    allok = True
    for n in names:
        allok &= verify_module(n, report)
    os.makedirs(os.path.join(HERE, "reports"), exist_ok=True)
    out = os.path.join(HERE, "reports", "arduino-verify-report.md")
    open(out, "w", encoding="utf-8").write("\n".join(report) + "\n")
    print("\n".join(report))
    print("\n=> %s" % ("全部通過" if allok else "有失敗項目"))
    sys.exit(0 if allok else 1)


if __name__ == "__main__":
    main(sys.argv[1:])
