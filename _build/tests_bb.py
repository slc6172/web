# -*- coding: utf-8 -*-
"""驗證器自我測試:故意做錯的電路必須被抓出來(確保 check() 不是橡皮圖章)。"""
import sys, copy, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bb, a03

def mutate(fn):
    c = copy.deepcopy(a03.CIRC)
    fn(c)
    return c

def errors(c):
    return [m for lv, m in bb.check(c) if lv == "error"]

cases = {
  "LED 插反(長腳接 GND 側)": lambda c: c.part("LED1").pins.update({"A": "d10", "K": "d9"}),
  "橘線插錯欄(a6,沒接到電阻)": lambda c: c.part("W1").pins.update({"b": "a6"}),
  "GND 線插錯欄(a11,沒接到 LED 短腳)": lambda c: c.part("W2").pins.update({"b": "a11"}),
  "橘線誤接 5V(與預期不同)": lambda c: c.part("W1").pins.update({"a": "UNO.5V"}),
  "電阻兩腳插同一欄(被短路)": lambda c: c.part("R1").pins.update({"2": "c5"}),
  "LED 兩腳同欄(被短路)": lambda c: c.part("LED1").pins.update({"K": "e9"}),
  "孔位重複(LED 長腳與電阻右腳同孔)": lambda c: c.part("LED1").pins.update({"A": "b9"}),
  "孔位超出欄數": lambda c: c.part("W2").pins.update({"b": "a40"}),
  "5V 與 GND 同網路(短路)": lambda c: (c.parts.append(bb.Wire("W3", "UNO.5V", "a10", "red", 4))),
}
bad = 0
for name, fn in cases.items():
    errs = errors(mutate(fn))
    print(("OK   抓到" if errs else "FAIL 漏掉"), "—", name, "→", (errs[0][:50] if errs else ""))
    bad += 0 if errs else 1
# 電流過大
c = mutate(lambda c: c.part("R1").meta.update(ohms=47))
lv = [l for l, m in bb.check(c) if "電流" in m]
print(("OK   抓到" if lv and lv[0] != "ok" else "FAIL 漏掉"), "— 電阻 47Ω 電流過大 →", lv)
bad += 0 if lv and lv[0] != "ok" else 1
print("\n自我測試:%s" % ("全部通過" if bad == 0 else "有 %d 項漏抓" % bad))
sys.exit(1 if bad else 0)
