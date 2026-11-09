# -*- coding: utf-8 -*-
"""bb.py — Arduino 教學主題專用:麵包板接線圖 + 電路原理圖 + 接線電氣檢查。

核心想法:一個電路只在資料裡寫「一次」——零件插在哪個孔、導線連哪裡、預期的電路連線(chain)。
  * 麵包板 SVG、文字接線表、原理圖,全部由同一份資料產生,不會互相矛盾。
  * check() 依麵包板規則(同欄 a–e 相通、f–j 相通、電源軌整條相通)算出實際連線,
    再和預期電路比對,並檢查短路、孔位重複、LED 電流等。
孔位命名:面包板孔 'e10'(列 a–j + 欄號)、電源軌 't+5' / 't-5' / 'b+5' / 'b-5'(位置號碼)、
          Uno 腳位 'UNO.D8' / 'UNO.5V' / 'UNO.GND'。
"""
import re
from h import table, e

P = 18                       # 孔距(px)
UNO_VCC = 5.0                # Uno 數位腳位 HIGH 的電壓(V)

# ---------------------------------------------------------------- 顏色(實體零件的顏色,非介面色)
BAND = {0: "#141413", 1: "#8B5A3C", 2: "#B04A3F", 3: "#D97757", 4: "#E1B93B",
        5: "#788C5D", 6: "#5B7FA6", 7: "#7A5C8F", 8: "#87867F", 9: "#FFFFFF"}
BAND_NAME = ["黑", "棕", "紅", "橙", "黃", "綠", "藍", "紫", "灰", "白"]
GOLD, SILVER = "#C9A227", "#BFBFBF"
WIRE = {"red": "#B04A3F", "black": "#141413", "orange": "#D97757", "green": "#788C5D",
        "blue": "#5B7FA6", "yellow": "#E1B93B", "white": "#FFFFFF", "purple": "#7A5C8F"}
WIRE_ZH = {"red": "紅", "black": "黑", "orange": "橘", "green": "綠", "blue": "藍",
           "yellow": "黃", "white": "白", "purple": "紫"}
LED_C = {"red": ("#F2C9C3", "#B04A3F", "紅", 2.0), "green": ("#D7E3C6", "#788C5D", "綠", 2.2),
         "yellow": ("#F6E7B0", "#B8962E", "黃", 2.1), "blue": ("#CFDDEB", "#5B7FA6", "藍", 3.0),
         "white": ("#FFFFFF", "#87867F", "白", 3.0)}


def bands(ohms):
    """色環:回傳 [第1環, 第2環, 乘數, 誤差] 的顏色代碼(4 環電阻,誤差 ±5% 金色)。"""
    v, mult = ohms, 0
    while v >= 100:
        v /= 10.0
        mult += 1
    while v < 10 and mult > -2:
        v *= 10
        mult -= 1
    v = int(round(v))
    return [v // 10, v % 10, mult if mult >= 0 else "gold"]


def fmt_ohm(o):
    if o >= 1e6:
        return ("%g" % (o / 1e6)) + "MΩ"
    if o >= 1e3:
        return ("%g" % (o / 1e3)) + "kΩ"
    return "%g" % o + "Ω"


# ---------------------------------------------------------------- 孔位解析
RE_HOLE = re.compile(r"^([a-j])(\d{1,2})$")
RE_RAIL = re.compile(r"^([tb][+-])(\d{1,2})$")


def kind_of(h):
    if h.startswith("UNO."):
        return "uno"
    if RE_HOLE.match(h):
        return "hole"
    if RE_RAIL.match(h):
        return "rail"
    return "bad"


# ---------------------------------------------------------------- Uno 腳位排(畫面上轉 180°,數位腳位在下緣、對著麵包板)
DIG = ["D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", None, "D8", "D9", "D10", "D11", "D12", "D13",
       "GND", "AREF", "SDA", "SCL"]
PWR = ["A5", "A4", "A3", "A2", "A1", "A0", None, "VIN", "GND2", "GND3", "5V", "3V3", "RESET", "IOREF", "NC"]
PWM = {"D3", "D5", "D6", "D9", "D10", "D11"}
GND_ALIASES = {"UNO.GND", "UNO.GND2", "UNO.GND3"}


def pin_label(p):
    if p.startswith("D") and p[1:].isdigit():
        return ("~" if p in PWM else "") + p[1:]
    if p.startswith("GND"):
        return "GND"
    return p


class Layout:
    def __init__(s, ncols=20):
        s.n = ncols
        s.UX, s.UY, s.UW, s.UH = 40, 34, 436, 112
        s.bx = 40
        s.by = s.UY + s.UH + 60
        s.x0 = s.bx + 34
        y = s.by + 22
        s.rail_y = {"t+": y, "t-": y + P}
        y += 2 * P + 14
        s.row_y = {}
        for r in "abcde":
            s.row_y[r] = y
            y += P
        y += 14
        for r in "fghij":
            s.row_y[r] = y
            y += P
        y += 8
        s.rail_y["b+"] = y
        s.rail_y["b-"] = y + P
        s.bottom = y + P + 20
        s.bw = 34 + ncols * P + 18
        s.W = max(s.UX + s.UW + 46, s.bx + s.bw + 20)
        s.H = s.bottom + 18
        s.uno_xy = {}
        xd = s.UX + 24
        for i, p in enumerate(DIG):
            if p:
                s.uno_xy["UNO." + p] = (xd + i * P, s.UY + s.UH - 14)
        xp = s.UX + 54
        for i, p in enumerate(PWR):
            if p:
                s.uno_xy["UNO." + p] = (xp + i * P, s.UY + 14)

    def xy(s, h):
        if h in s.uno_xy:
            return s.uno_xy[h]
        m = RE_HOLE.match(h)
        if m:
            return (s.x0 + (int(m.group(2)) - 1) * P, s.row_y[m.group(1)])
        m = RE_RAIL.match(h)
        if m:
            return (s.x0 + (int(m.group(2)) - 1) * P, s.rail_y[m.group(1)])
        raise ValueError("未知孔位:%s" % h)


# ---------------------------------------------------------------- 零件資料
class Part:
    def __init__(s, kind, ref, pins, step, **meta):
        s.kind, s.ref, s.pins, s.step, s.meta = kind, ref, pins, step, meta


def Resistor(ref, ohms, h1, h2, step):
    return Part("R", ref, {"1": h1, "2": h2}, step, ohms=ohms)


def LED(ref, color, anode, cathode, step):
    return Part("LED", ref, {"A": anode, "K": cathode}, step, color=color)


def LDR(ref, p1, p2, step):
    """光敏電阻(沒有方向的兩腳元件)。"""
    return Part("LDR", ref, {"1": p1, "2": p2}, step)


def Pot(ref, p1, w, p2, step):
    """電位器(三腳):p1、p2 是兩個外側腳,w 是中間的滑動腳(wiper)。"""
    return Part("POT", ref, {"1": p1, "W": w, "2": p2}, step)


def Button(ref, p1, p2, x1, x2, step):
    """4 腳按鈕:p1、p2 是接線用的「對角」兩腳(不論按鈕怎麼轉,對角兩腳一定是按下才相通);
    x1、x2 是另外兩隻腳,只佔位、不接線(不列入連線)。"""
    return Part("BTN", ref, {"1": p1, "2": p2, "x1": x1, "x2": x2}, step)


def Buzzer(ref, kind, plus, minus, step):
    """蜂鳴器。kind: 'active'(主動)或 'passive'(被動)。長腳 / + 標記是 P。"""
    return Part("BZ", ref, {"P": plus, "N": minus}, step, btype=kind)


def Wire(ref, a, b, color, step, route="auto"):
    return Part("W", ref, {"a": a, "b": b}, step, color=color, route=route)


class Circuit:
    def __init__(s, cid, ncols, parts, steps, chain=None, code_pins=None, intro="", done="", chains=None):
        """steps: [(標題, 說明HTML)],第 i 項對應零件的 step == i+1。
        chain: 預期電路,例如 ['UNO.D8','R1','LED1','UNO.GND'](由訊號端串到 GND)。
        code_pins: 程式裡的腳位常數名稱 → 預期 Uno 腳位,例如 {'LED_PIN':'UNO.D8'}。"""
        s.chains = chains or [chain]
        s.id, s.ncols, s.parts, s.steps, s.chain = cid, ncols, parts, steps, s.chains[0]
        s.code_pins = code_pins or {}
        s.intro, s.done = intro, done

    def part(s, ref):
        for p in s.parts:
            if p.ref == ref:
                return p
        raise KeyError(ref)


# ---------------------------------------------------------------- 預期連線(由 chain 推出)
IN_OUT = {"R": ("1", "2"), "LED": ("A", "K"), "BZ": ("P", "N"), "BTN": ("1", "2"), "LDR": ("1", "2")}


def chain_nets(circ):
    """把串聯鏈轉成「網路」清單,每個網路是一組腳位名稱的 frozenset。多條鏈共用的端點(如 GND)會合併。"""
    d = DSU()
    seen = set()
    for chain in circ.chains:
        toks = []
        for t in chain:
            if t.startswith("UNO."):
                n = "UNO.GND" if t in GND_ALIASES else t
                toks.append((n, n))
            elif "." in t:                      # 零件腳位端點,例如 POT1.W
                toks.append((t, t))
            else:
                k = circ.part(t).kind
                toks.append((t + "." + IN_OUT[k][0], t + "." + IN_OUT[k][1]))
        for i in range(len(toks) - 1):
            d.u(toks[i][1], toks[i + 1][0])
            seen.update([toks[i][1], toks[i + 1][0]])
    groups = {}
    for m in seen:
        groups.setdefault(d.f(m), set()).add(m)
    return {frozenset(g) for g in groups.values() if len(g) >= 2}


# ---------------------------------------------------------------- 實際連線(依麵包板規則計算)
class DSU:
    def __init__(s):
        s.p = {}

    def f(s, x):
        s.p.setdefault(x, x)
        while s.p[x] != x:
            s.p[x] = s.p[s.p[x]]
            x = s.p[x]
        return x

    def u(s, a, b):
        s.p[s.f(a)] = s.f(b)


def node_of(h):
    """孔位 → 導電節點:同欄同半邊(a–e / f–j)相通;電源軌整條相通;Uno GND 腳全部相通。"""
    if h.startswith("UNO."):
        return "UNO.GND" if h in GND_ALIASES else h
    m = RE_HOLE.match(h)
    if m:
        return ("strip", int(m.group(2)), "top" if m.group(1) in "abcde" else "bot")
    m = RE_RAIL.match(h)
    return ("rail", m.group(1))


def actual_nets(circ):
    d = DSU()
    for p in circ.parts:
        if p.kind == "W":
            d.u(node_of(p.pins["a"]), node_of(p.pins["b"]))
    members = {}
    for p in circ.parts:
        if p.kind == "W":
            continue
        for pin, h in p.pins.items():
            if pin.startswith("x"):
                continue
            members.setdefault(d.f(node_of(h)), set()).add("%s.%s" % (p.ref, pin))
    for p in circ.parts:
        if p.kind == "W":
            for h in p.pins.values():
                if h.startswith("UNO."):
                    members.setdefault(d.f(node_of(h)), set()).add(node_of(h))
    nets = set()
    for k, m in members.items():
        if len(m) >= 2:
            nets.add(frozenset(m))
    return nets, members


# ---------------------------------------------------------------- 檢查
def check(circ):
    """回傳 [(級別, 訊息)];級別為 'ok' / 'warn' / 'error'。"""
    out = []
    lay = Layout(circ.ncols)

    def add(level, msg):
        out.append((level, msg))

    # 1. 孔位合法、在畫出來的欄數之內
    bad = []
    for p in circ.parts:
        for h in p.pins.values():
            k = kind_of(h)
            if k == "bad":
                bad.append(h)
            elif k == "uno" and h not in lay.uno_xy:
                bad.append(h)
            elif k in ("hole", "rail"):
                col = int(re.search(r"(\d+)$", h).group(1))
                if not (1 <= col <= circ.ncols):
                    bad.append(h)
    add("error" if bad else "ok", "所有孔位都存在且在圖上的 %d 欄之內" % circ.ncols if not bad else "不存在的孔位:%s" % bad)

    # 2. 同一個孔不能插兩個東西
    used, dup = {}, []
    for p in circ.parts:
        for pin, h in p.pins.items():
            if kind_of(h) in ("hole", "rail"):
                if h in used:
                    dup.append("%s(%s 與 %s.%s)" % (h, used[h], p.ref, pin))
                used[h] = "%s.%s" % (p.ref, pin)
    add("error" if dup else "ok", "沒有任何一個孔被兩個零件腳或導線共用" if not dup else "孔位重複:%s" % dup)

    # 3. 實際連線 == 預期電路
    nets, members = actual_nets(circ)
    expect = chain_nets(circ)
    if nets == expect:
        add("ok", "依麵包板規則算出的實際連線,與原理圖的預期電路完全一致(%d 條連線)" % len(expect))
    else:
        add("error", "實際連線與預期不同。多出:%s;缺少:%s" % (
            [sorted(x) for x in nets - expect], [sorted(x) for x in expect - nets]))

    # 4. 零件兩腳不可被短路
    for p in circ.parts:
        if p.kind in ("R", "LED", "BZ", "BTN", "LDR"):
            pins = [k for k in p.pins if not k.startswith("x")]
            a, b = ["%s.%s" % (p.ref, x) for x in pins]
            if any(a in n and b in n for n in nets):
                add("error", "%s 的兩隻腳被接在同一條線上(被短路)" % p.ref)
    add("ok" if not any(l == "error" and "短路" in m for l, m in out) else "error", "沒有零件被自己的導線短路")

    # 5. Uno 腳位之間不可短路(同一網路不得有兩個不同的 Uno 腳位)
    shorts = []
    for k, m in members.items():
        unos = {x for x in m if x.startswith("UNO.")}
        if len(unos) > 1:
            shorts.append(sorted(unos))
    add("error" if shorts else "ok", "沒有任何兩個不同的 Uno 腳位被接在一起(5V 與 GND 沒有短路)" if not shorts else "Uno 腳位短路:%s" % shorts)

    # 6. 腳位電流(每條串聯鏈,訊號端為數位 / 類比腳位或 5V)
    for chain in circ.chains:
        src = chain[0]
        if not (src.startswith("UNO.D") or src.startswith("UNO.A") or src == "UNO.5V"):
            continue
        r_tot, vf, leds = 0.0, 0.0, 0
        for t in chain[1:-1]:
            pt = circ.part(t)
            if pt.kind == "R":
                r_tot += pt.meta["ohms"]
            elif pt.kind == "LED":
                vf += LED_C[pt.meta["color"]][3]
                leds += 1
        if leds and r_tot > 0:
            i_ma = (UNO_VCC - vf) / r_tot * 1000.0
            lvl = "ok" if 3 <= i_ma <= 20 else ("warn" if i_ma < 3 or i_ma <= 40 else "error")
            add(lvl, "%s 腳位電流估算 ≈ %.1f mA(Vcc %.0f V、LED 順向壓降 %.1f V、串聯電阻 %s);Uno 建議每腳 ≤ 20 mA、絕對上限 40 mA"
                % (src[4:], i_ma, UNO_VCC, vf, fmt_ohm(r_tot)))
    return out


# ================================================================ 繪圖
STYLE = ('<style>.m{font:9px ui-monospace,Menlo,Consolas,monospace}.mb{font:600 10px ui-monospace,Menlo,Consolas,monospace}'
         '.s{font:11px system-ui,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif}'
         '.sb{font:600 11px system-ui,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif}</style>')
GRAY5, GRAY7, GRAY3, GRAY1 = "#87867F", "#3D3D3A", "#D1CFC5", "#F0EEE6"
CLAY, OLIVE, RUST, SLATE = "#D97757", "#788C5D", "#B04A3F", "#141413"


def _txt(x, y, s, cls="m", fill=GRAY5, anchor="middle"):
    return '<text x="%.1f" y="%.1f" class="%s" fill="%s" text-anchor="%s">%s</text>' % (x, y, cls, fill, anchor, e(s))


def uno_zh(h):
    n = h[4:]
    if n.startswith("D") and n[1:].isdigit():
        return "Uno 數位腳位 %s(板上標示 %s)" % (n[1:], pin_label(n))
    if n.startswith("GND"):
        return "Uno 的 GND 腳"
    if n == "5V":
        return "Uno 的 5V 腳"
    if n == "3V3":
        return "Uno 的 3.3V 腳"
    return "Uno 的 %s 腳" % n


def board_svg(lay, uno=True):
    """Uno 與麵包板的底圖(永遠顯示)。"""
    o = []
    UX, UY, UW, UH = lay.UX, lay.UY, lay.UW, lay.UH
    if uno:
        o.append(_uno_board(lay))
    o.append(_breadboard(lay))
    return "".join(o)


def _uno_board(lay):
    o = []
    UX, UY, UW, UH = lay.UX, lay.UY, lay.UW, lay.UH
    o.append('<rect x="%d" y="%d" width="34" height="46" rx="4" fill="%s" stroke="%s" stroke-width="1.5"/>' % (UX + UW - 4, UY + 22, GRAY3, GRAY5))
    o.append(_txt(UX + UW + 13, UY + 49, "USB", "m", GRAY7))
    o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s" stroke="%s" stroke-width="1.5"/>' % (UX, UY, UW, UH, GRAY7, SLATE))
    o.append('<rect x="%d" y="%d" width="86" height="30" rx="3" fill="%s"/>' % (UX + 150, UY + 41, SLATE))
    o.append(_txt(UX + 193, UY + 60, "ATmega328P", "m", GRAY3))
    o.append(_txt(UX + 300, UY + 61, "ARDUINO UNO", "mb", GRAY1))
    o.append(_txt(UX + 60, UY + 30, "POWER / ANALOG IN", "m", GRAY3, "start") if False else "")
    for name, (x, y) in lay.uno_xy.items():
        p = name[4:]
        top = y < UY + UH / 2
        o.append('<rect x="%.1f" y="%.1f" width="8" height="8" rx="1.5" fill="%s" stroke="%s" stroke-width="1"/>' % (x - 4, y - 4, SLATE, GOLD))
        lab = pin_label(p)
        if len(lab) <= 3:
            o.append(_txt(x, y + (17 if top else -9), lab, "m", GRAY1))
        else:   # 長標籤改成直式,避免互相重疊
            ty = y + 9 if top else y - 8
            o.append('<text transform="translate(%.1f %.1f) rotate(-90)" font-size="8" font-family="ui-monospace,Menlo,Consolas,monospace" fill="%s" text-anchor="%s">%s</text>'
                     % (x + 3, ty, GRAY1, "end" if top else "start", lab))
    o.append(_txt(UX + 24, UY + UH - 40, "DIGITAL 數位腳位(~ = 可輸出 PWM)", "m", GRAY3, "start"))
    o.append(_txt(UX + 6, UY + 38, "ANALOG IN", "m", GRAY3, "start") if False else "")
    return "".join(o)


def _breadboard(lay):
    o = []
    bx, by, bw = lay.bx, lay.by, lay.bw
    o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s" stroke="%s" stroke-width="1.5"/>' % (bx, by, bw, lay.bottom - by, GRAY1, GRAY3))
    ye, yf = lay.row_y["e"], lay.row_y["f"]
    o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s"/>' % (bx + 22, ye + 12, bw - 44, yf - ye - 24, GRAY3))
    xa, xz = lay.x0 - 12, lay.x0 + (lay.n - 1) * P + 12
    for rname, color in (("t+", RUST), ("t-", GRAY7), ("b+", RUST), ("b-", GRAY7)):
        y = lay.rail_y[rname]
        yl = y - 9 if rname in ("t+", "b+") else y + 9
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.5"/>' % (xa, yl, xz, yl, color))
        o.append(_txt(bx + 14, y + 3.5, "+" if rname.endswith("+") else "−", "mb", color))
    holes = []
    for r in "abcdefghij":
        for c in range(1, lay.n + 1):
            x, y = lay.xy("%s%d" % (r, c))
            holes.append('<rect x="%.1f" y="%.1f" width="7" height="7" rx="1.2"/>' % (x - 3.5, y - 3.5))
    for rname in ("t+", "t-", "b+", "b-"):
        for c in range(1, lay.n + 1):
            x, y = lay.xy("%s%d" % (rname, c))
            holes.append('<rect x="%.1f" y="%.1f" width="7" height="7" rx="1.2"/>' % (x - 3.5, y - 3.5))
    o.append('<g fill="#FFFFFF" stroke="%s" stroke-width=".8">%s</g>' % (GRAY3, "".join(holes)))
    for r in "abcdefghij":
        o.append(_txt(bx + 24, lay.row_y[r] + 3, r, "m", GRAY5))
    ych = (ye + yf) / 2.0 + 3
    for c in range(1, lay.n + 1):
        o.append('<text x="%.1f" y="%.1f" font-size="8.5" font-family="ui-monospace,Menlo,Consolas,monospace" fill="%s" text-anchor="middle">%d</text>'
                 % (lay.x0 + (c - 1) * P, ych, GRAY7, c))
    return "".join(o)


def _wire_path(lay, p):
    a, b = p.pins["a"], p.pins["b"]
    x1, y1 = lay.xy(a)
    x2, y2 = lay.xy(b)
    route = p.meta.get("route", "auto")
    if route.startswith("left"):
        k = int(route[4:] or 0)       # 車道:0 最內側,1、2 … 往外,避免互相重疊
        return "M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f" % (
            x1, y1, x1, lay.UY - 18 - 8 * k, lay.UX - 22 - 10 * k, lay.UY - 18 - 8 * k, lay.UX - 22 - 10 * k, lay.by - 14 + 8 * k,
            x2, lay.by - 14 + 8 * k, x2, y2)
    if route == "right":
        xr = lay.bx + lay.bw + 12
        return "M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f" % (
            x1, y1, x1, lay.UY + lay.UH + 26, xr, lay.UY + lay.UH + 26, xr, y2, x2, y2)
    if route == "straight":
        return "M%.1f,%.1f L%.1f,%.1f" % (x1, y1, x2, y2)
    if a.startswith("UNO.") != b.startswith("UNO."):
        if b.startswith("UNO."):
            x1, y1, x2, y2 = x2, y2, x1, y1
        dy = max(30, (y2 - y1) / 2.0)
        return "M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (x1, y1, x1, y1 + dy, x2, y2 - dy, x2, y2)
    return "M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (x1, y1, x1, y1 - 30, x2, y2 - 30, x2, y2)


def _ring(x, y):
    return '<circle cx="%.1f" cy="%.1f" r="8.5" fill="none" stroke="%s" stroke-width="2.5"/>' % (x, y, CLAY)


def part_svg(lay, p):
    """一個零件(或導線)的 SVG 群組,帶 data-step、data-part,供步驟播放與原理圖連動使用。"""
    ref = p.ref
    if p.kind == "W":
        d = _wire_path(lay, p)
        col = WIRE[p.meta["color"]]
        x1, y1 = lay.xy(p.pins["a"])
        x2, y2 = lay.xy(p.pins["b"])
        title = "%s色杜邦線 %s:%s ↔ %s" % (WIRE_ZH[p.meta["color"]], ref, p.pins["a"], p.pins["b"])
        inner = ('<path d="%s" fill="none" stroke="%s" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>'
                 '<path d="%s" fill="none" stroke="%s" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>'
                 '<circle cx="%.1f" cy="%.1f" r="4" fill="%s" stroke="%s" stroke-width="1.5"/>'
                 '<circle cx="%.1f" cy="%.1f" r="4" fill="%s" stroke="%s" stroke-width="1.5"/>') % (d, SLATE, d, col, x1, y1, col, SLATE, x2, y2, col, SLATE)
        halo = '<path d="%s" fill="none" stroke="%s" stroke-width="13" stroke-linecap="round" stroke-linejoin="round" opacity=".35"/>' % (d, CLAY)
        halo += "".join(_ring(*lay.xy(h)) for h in p.pins.values() if not h.startswith("UNO."))
        halo += "".join('<circle cx="%.1f" cy="%.1f" r="9" fill="none" stroke="%s" stroke-width="2.5"/>' % (lay.xy(h) + (CLAY,)) for h in p.pins.values() if h.startswith("UNO."))
    elif p.kind == "POT":
        pts = {k: lay.xy(h) for k, h in p.pins.items()}
        xs = [q[0] for q in pts.values()]
        yy = pts["W"][1]
        cx = pts["W"][0]
        inner = ('<rect x="%.1f" y="%.1f" width="%.1f" height="30" rx="5" fill="%s" stroke="%s" stroke-width="1.5"/>'
                 '<circle cx="%.1f" cy="%.1f" r="12" fill="#87867F" stroke="%s" stroke-width="1.5"/>'
                 '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3" stroke-linecap="round"/>'
                 % (min(xs) - 10, yy - 15, max(xs) - min(xs) + 20, "#2B6CB0" if False else GRAY7, SLATE, cx, yy, SLATE, cx, yy, cx + 7, yy - 9, "#F0EEE6"))
        inner += "".join('<circle cx="%.1f" cy="%.1f" r="2.6" fill="#E1B93B"/>' % q for q in pts.values())
        inner += _txt(cx, yy + 30, "10kΩ 電位器", "m", GRAY7)
        halo = '<rect x="%.1f" y="%.1f" width="%.1f" height="38" rx="9" fill="none" stroke="%s" stroke-width="2.5"/>' % (min(xs) - 14, yy - 19, max(xs) - min(xs) + 28, CLAY)
        halo += "".join(_ring(*q) for q in pts.values())
        title = "電位器 %s:三隻腳插在 %s(外側)、%s(中間,滑動腳)、%s(外側)" % (ref, p.pins["1"], p.pins["W"], p.pins["2"])
    elif p.kind == "BTN":
        pts = {k: lay.xy(h) for k, h in p.pins.items()}
        xs = [q[0] for q in pts.values()]
        ys = [q[1] for q in pts.values()]
        x0, x1_, y0, y1_ = min(xs) - 9, max(xs) + 9, min(ys) - 9, max(ys) + 9
        cx, cy = (x0 + x1_) / 2.0, (y0 + y1_) / 2.0
        inner = ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="5" fill="%s" stroke="%s" stroke-width="1.5"/>'
                 '<circle cx="%.1f" cy="%.1f" r="10" fill="#87867F" stroke="%s" stroke-width="1.5"/><circle cx="%.1f" cy="%.1f" r="6" fill="#D1CFC5"/>'
                 % (x0, y0, x1_ - x0, y1_ - y0, GRAY7, SLATE, cx, cy, SLATE, cx, cy))
        inner += "".join('<circle cx="%.1f" cy="%.1f" r="2.6" fill="%s"/>' % (x, y, "#E1B93B") for x, y in pts.values())
        inner += _txt(cx, y1_ + 15, "按鈕", "m", GRAY7)
        halo = '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="8" fill="none" stroke="%s" stroke-width="2.5"/>' % (x0 - 5, y0 - 5, x1_ - x0 + 10, y1_ - y0 + 10, CLAY)
        halo += _ring(*pts["1"]) + _ring(*pts["2"])
        title = "按鈕 %s:對角的兩隻腳插在 %s 與 %s(另外兩隻腳 %s、%s 也插進孔裡,但不接線)" % (ref, p.pins["1"], p.pins["2"], p.pins["x1"], p.pins["x2"])
    else:
        (xa, ya) = lay.xy(list(p.pins.values())[0])
        (xb, yb) = lay.xy(list(p.pins.values())[1])
        import math
        cx, cy = (xa + xb) / 2.0, (ya + yb) / 2.0
        ang = math.degrees(math.atan2(yb - ya, xb - xa))
        L = math.hypot(xb - xa, yb - ya)
        if p.kind == "R":
            bl = L - 14
            ohms = p.meta["ohms"]
            b = bands(ohms)
            cols = [BAND[b[0]], BAND[b[1]], BAND[b[2]] if b[2] != "gold" else GOLD, GOLD]
            body = ('<line x1="%.1f" y1="0" x2="%.1f" y2="0" stroke="%s" stroke-width="2.2" stroke-linecap="round"/>'
                    '<rect x="%.1f" y="-6" width="%.1f" height="12" rx="5" fill="#E3DACC" stroke="%s" stroke-width="1.2"/>') % (-L / 2, L / 2, GRAY5, -bl / 2, bl, GRAY5)
            for i, c in enumerate(cols):
                bx_ = -bl / 2 + 7 + i * 6 if i < 3 else bl / 2 - 9
                body += '<rect x="%.1f" y="-6" width="3" height="12" fill="%s"%s/>' % (bx_, c, ' stroke="#87867F" stroke-width=".4"' if c == "#FFFFFF" else "")
            body += '<circle cx="%.1f" cy="0" r="2.4" fill="%s"/><circle cx="%.1f" cy="0" r="2.4" fill="%s"/>' % (-L / 2, GRAY7, L / 2, GRAY7)
            inner = '<g transform="translate(%.1f %.1f) rotate(%.1f)">%s</g>' % (cx, cy, ang, body)
            if abs(xb - xa) < abs(yb - ya):
                inner += _txt(cx - 13, cy + 3, fmt_ohm(ohms), "m", GRAY7, "end")
            else:
                inner += _txt(cx, cy + 20, fmt_ohm(ohms), "m", GRAY7)
            halo = '<g transform="translate(%.1f %.1f) rotate(%.1f)"><rect x="%.1f" y="-12" width="%.1f" height="24" rx="8" fill="none" stroke="%s" stroke-width="2.5"/></g>' % (cx, cy, ang, -bl / 2 - 6, bl + 12, CLAY)
            halo += _ring(xa, ya) + _ring(xb, yb)
            title = "電阻 %s(%s):插在 %s 與 %s" % (ref, fmt_ohm(ohms), p.pins["1"], p.pins["2"])
        elif p.kind == "LDR":
            body = ('<line x1="%.1f" y1="0" x2="%.1f" y2="0" stroke="%s" stroke-width="2.2" stroke-linecap="round"/>'
                    '<circle cx="0" cy="0" r="14" fill="#D9C7A0" stroke="%s" stroke-width="1.5"/>'
                    '<polyline points="-9,-5 -4,-1 -9,3 -4,7 1,3 -4,-1 1,-5 6,-1 1,3 6,7 9,4" fill="none" stroke="%s" stroke-width="1.3" stroke-linejoin="round"/>') % (-L / 2, L / 2, GRAY5, GRAY7, GRAY7)
            body += '<circle cx="%.1f" cy="0" r="2.4" fill="%s"/><circle cx="%.1f" cy="0" r="2.4" fill="%s"/>' % (-L / 2, GRAY7, L / 2, GRAY7)
            inner = '<g transform="translate(%.1f %.1f) rotate(%.1f)">%s</g>' % (cx, cy, ang, body)
            inner += _txt(cx, cy + 27, "光敏電阻", "m", GRAY7)
            halo = '<circle cx="%.1f" cy="%.1f" r="21" fill="none" stroke="%s" stroke-width="2.5"/>' % (cx, cy, CLAY)
            halo += _ring(xa, ya) + _ring(xb, yb)
            title = "光敏電阻 %s:兩腳插在 %s 與 %s(沒有方向)" % (ref, p.pins["1"], p.pins["2"])
        elif p.kind == "BZ":
            body = ('<circle cx="0" cy="0" r="15" fill="%s" stroke="%s" stroke-width="1.5"/>'
                    '<circle cx="0" cy="0" r="3.5" fill="%s"/>'
                    '<text x="%.1f" y="4" class="mb" fill="#FFFFFF" text-anchor="middle">+</text>') % (SLATE, GRAY7, GRAY5, -8)
            body += '<circle cx="%.1f" cy="0" r="2.4" fill="%s"/><circle cx="%.1f" cy="0" r="2.4" fill="%s"/>' % (-L / 2, GRAY5, L / 2, GRAY5)
            body += '<text x="%.1f" y="-15" class="mb" fill="%s" text-anchor="middle">+</text><text x="%.1f" y="-15" class="mb" fill="%s" text-anchor="middle">−</text>' % (-L / 2, RUST, L / 2, GRAY7)
            inner = '<g transform="translate(%.1f %.1f) rotate(%.1f)">%s</g>' % (cx, cy, ang, body)
            halo = '<circle cx="%.1f" cy="%.1f" r="22" fill="none" stroke="%s" stroke-width="2.5"/>' % (cx, cy, CLAY)
            halo += _ring(xa, ya) + _ring(xb, yb)
            title = "%s式蜂鳴器 %s:+ 腳(長腳)插在 %s,− 腳插在 %s" % ("主動" if p.meta["btype"] == "active" else "被動", ref, p.pins["P"], p.pins["N"])
        else:  # LED
            fill, stroke, zh, _vf = LED_C[p.meta["color"]]
            r = 11
            body = ('<circle cx="0" cy="0" r="%d" fill="%s" stroke="%s" stroke-width="1.8"/>'
                    '<line x1="%d" y1="-7.5" x2="%d" y2="7.5" stroke="%s" stroke-width="2.4" stroke-linecap="round"/>') % (r, fill, stroke, 8, 8, stroke)
            body += '<circle cx="%.1f" cy="0" r="2.4" fill="%s"/><circle cx="%.1f" cy="0" r="2.4" fill="%s"/>' % (-L / 2, GRAY7, L / 2, GRAY7)
            body += '<text x="%.1f" y="-15" class="mb" fill="%s" text-anchor="middle">+</text><text x="%.1f" y="-15" class="mb" fill="%s" text-anchor="middle">−</text>' % (-L / 2, RUST, L / 2, GRAY7)
            inner = '<g transform="translate(%.1f %.1f) rotate(%.1f)">%s</g>' % (cx, cy, ang, body)
            halo = '<circle cx="%.1f" cy="%.1f" r="%d" fill="none" stroke="%s" stroke-width="2.5"/>' % (cx, cy, r + 8, CLAY)
            halo += _ring(xa, ya) + _ring(xb, yb)
            title = "%s色 LED %s:長腳(+)插在 %s,短腳(−)插在 %s" % (zh, ref, p.pins["A"], p.pins["K"])
    return ('<g class="el" data-step="%d" data-part="%s"><title>%s</title><g class="halo">%s</g>%s</g>'
            % (p.step, ref, e(title), halo, inner))


def breadboard_svg(circ):
    lay = Layout(circ.ncols)
    body = board_svg(lay) + "".join(part_svg(lay, p) for p in circ.parts)
    label = "%s 的接線圖:Uno 與麵包板,共 %d 步" % (circ.id, len(circ.steps))
    return ('<svg viewBox="0 0 %d %d" role="img" aria-label="%s" style="min-width:560px">\n<defs>%s</defs>\n'
            '<rect width="%d" height="%d" fill="#FFFFFF"/>\n%s\n</svg>' % (lay.W, lay.H, e(label), STYLE, lay.W, lay.H, body))


def stepper_html(circ):
    """可一步一步播放的接線圖:上一步/下一步、步驟按鈕、說明框。說明文字放在 window.PAGE.wiring。"""
    n = len(circ.steps)
    dots = "".join('<button type="button" class="wdot" data-w="%d" aria-label="第 %d 步">%d</button>' % (i, i, i) for i in range(1, n + 1))
    return ('<div class="panel wiring" data-wiring="%s">\n'
            '<div class="canvas">%s</div>\n'
            '<div class="wnav"><button type="button" class="ghost" data-w="prev">← 上一步</button>'
            '<span class="wdots" role="group" aria-label="跳到步驟">%s</span>'
            '<button type="button" class="primary" data-w="next">下一步 →</button>'
            '<button type="button" class="ghost" data-w="all">看完整接線</button>'
            '<button type="button" class="ghost" data-w="reset">Reset</button></div>\n'
            '<div class="wcap" aria-live="polite"></div>\n</div>' % (circ.id, breadboard_svg(circ), dots))


def wiring_config(circ):
    """給 common 腳本用:每一步的標題與說明。"""
    return {"id": circ.id, "intro": circ.intro, "done": circ.done, "steps": [{"t": t, "x": x} for t, x in circ.steps]}


def part_zh(p):
    if p.kind == "R":
        return "電阻 %s(%s)" % (p.ref, fmt_ohm(p.meta["ohms"]))
    if p.kind == "LED":
        return "%s色 LED(%s)" % (LED_C[p.meta["color"]][2], p.ref)
    if p.kind == "BZ":
        return "%s式蜂鳴器(%s)" % ("主動" if p.meta["btype"] == "active" else "被動", p.ref)
    if p.kind == "BTN":
        return "按鈕(%s)" % p.ref
    if p.kind == "POT":
        return "電位器(%s)" % p.ref
    if p.kind == "LDR":
        return "光敏電阻(%s)" % p.ref
    return "%s色杜邦線 %s" % (WIRE_ZH[p.meta["color"]], p.ref)


def where_zh(p):
    if p.kind == "R":
        return "兩腳分別插在 <code>%s</code> 與 <code>%s</code>(電阻沒有方向,兩腳可對調)" % (p.pins["1"], p.pins["2"])
    if p.kind == "LED":
        return "<strong>長腳(+)</strong>插 <code>%s</code>,<strong>短腳(−)</strong>插 <code>%s</code>" % (p.pins["A"], p.pins["K"])
    if p.kind == "BZ":
        return "<strong>+ 腳(外殼有 + 標記、通常較長)</strong>插 <code>%s</code>,<strong>− 腳</strong>插 <code>%s</code>" % (p.pins["P"], p.pins["N"])
    if p.kind == "LDR":
        return "兩腳分別插 <code>%s</code> 與 <code>%s</code>(光敏電阻沒有方向,兩腳可對調)" % (p.pins["1"], p.pins["2"])
    if p.kind == "POT":
        return "三隻腳依序插 <code>%s</code>(外側)、<code>%s</code>(<b>中間腳</b>)、<code>%s</code>(外側)" % (p.pins["1"], p.pins["W"], p.pins["2"])
    if p.kind == "BTN":
        return "跨在中間凹槽上,<b>對角</b>的兩隻腳插 <code>%s</code> 與 <code>%s</code>;另外兩隻腳會插進 <code>%s</code>、<code>%s</code>,<b>不接線</b>" % (p.pins["1"], p.pins["2"], p.pins["x1"], p.pins["x2"])
    a, b = p.pins["a"], p.pins["b"]

    def end(h):
        return uno_zh(h) if h.startswith("UNO.") else "麵包板 <code>%s</code>" % h
    return "一端插 %s,另一端插 %s" % (end(a), end(b))


def wiring_table(circ):
    rows = []
    for p in sorted(circ.parts, key=lambda q: q.step):
        rows.append([str(p.step), part_zh(p), where_zh(p)])
    return table("g3w", ["步驟", "零件", "插在哪裡"], rows)


# ---------------------------------------------------------------- 原理圖(串聯鏈)
def _zigzag(x, y, w=80, h=14, n=6):
    pts = ["%.1f,%.1f" % (x, y)]
    step = w / float(n + 1)
    pts.append("%.1f,%.1f" % (x + step * 0.5, y))
    for i in range(n):
        pts.append("%.1f,%.1f" % (x + step * (i + 1), y + (-h if i % 2 == 0 else h)))
    pts.append("%.1f,%.1f" % (x + w - step * 0.5, y))
    pts.append("%.1f,%.1f" % (x + w, y))
    return '<polyline points="%s" fill="none" stroke="%s" stroke-width="2" stroke-linejoin="round"/>' % (" ".join(pts), GRAY7)


def schematic_svg(circ, mark=("gnd", "res", "led", "bz", "btn", "ldr")):
    """依 chains 畫水平串聯的原理圖(每條鏈一列)。回傳 (svg, 符號圖例 [(編號, 說明)])。"""
    o, legend = [], []
    kinds = {}

    def marker(n, mx, my):
        return ('<circle cx="%.1f" cy="%.1f" r="10" fill="%s"/><text x="%.1f" y="%.1f" class="mb" fill="#FFFFFF" text-anchor="middle">%d</text>'
                % (mx, my, CLAY, mx, my + 3.5, n))

    def note(kind, mx, my, text):
        if kind in mark and kind not in kinds:
            kinds[kind] = len(kinds) + 1
            legend.append((str(kinds[kind]), text))
            o.append(marker(kinds[kind], mx, my))

    maxx = 0
    for ci, chain in enumerate(circ.chains):
        y = 74 + ci * 118
        cur = 22
        for i, t in enumerate(chain):
            if t.startswith("UNO.") and i == 0:
                name = t[4:]
                o.append('<rect x="%d" y="%d" width="74" height="30" rx="8" fill="#F0EEE6" stroke="%s" stroke-width="1.5"/>' % (cur, y - 15, GRAY7))
                o.append(_txt(cur + 37, y + 4, "Uno " + name, "mb", SLATE))
                if ci == 0:
                    o.append(_txt(cur + 37, y + 30, "(5 V 電源從這裡出來)" if name == "5V" else "(訊號從這裡出來)", "s", GRAY5))
                cur += 74
                o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (cur, y, cur + 40, y, GRAY7))
                cur += 40
            elif t.startswith("UNO.") and i == len(chain) - 1 and not t.startswith("UNO.GND"):
                o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (cur, y, cur + 40, y, GRAY7))
                cur += 40
                o.append('<rect x="%d" y="%d" width="74" height="30" rx="8" fill="#F0EEE6" stroke="%s" stroke-width="1.5"/>' % (cur, y - 15, GRAY7))
                o.append(_txt(cur + 37, y + 4, "Uno " + t[4:], "mb", SLATE))
                cur += 74
            elif t.startswith("UNO.") and i == len(chain) - 1:
                o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (cur, y, cur + 40, y, GRAY7))
                cur += 40
                gx = cur
                o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (gx, y, gx, y + 34, GRAY7))
                for k, wd in enumerate((26, 17, 8)):
                    yy = y + 34 + k * 7
                    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.2" stroke-linecap="round"/>' % (gx - wd / 2, yy, gx + wd / 2, yy, GRAY7))
                o.append(_txt(gx, y + 66, "GND(接地,0 V)", "s", GRAY5))
                note("gnd", gx + 30, y + 40, "<b>接地 GND</b>:電路的 0 V 參考點。三條漸短的橫線是它的符號;<b>圖上出現幾次,就代表那幾處接到同一個 GND</b>。")
                cur = gx
            else:
                pt = circ.part(t)
                if pt.kind == "R":
                    o.append('<g class="el" data-part="%s" tabindex="0" role="button" aria-label="電阻 %s,點一下看它在麵包板上的位置">' % (t, t))
                    o.append('<rect x="%d" y="%d" width="90" height="46" rx="8" fill="#FFFFFF" opacity="0.001"/>' % (cur, y - 23))
                    o.append('<rect class="halo" x="%d" y="%d" width="92" height="48" rx="10" fill="none" stroke="%s" stroke-width="2.5"/>' % (cur - 1, y - 24, CLAY))
                    o.append(_zigzag(cur + 4, y, 82, 13, 6))
                    o.append(_txt(cur + 45, y + 34, "%s  %s" % (t, fmt_ohm(pt.meta["ohms"])), "mb", SLATE))
                    o.append("</g>")
                    note("res", cur + 45, y - 34, "<b>電阻</b>:鋸齒線。串在 LED 旁邊,把電流限制在安全範圍。有些教科書把電阻畫成長方形,意思相同。")
                    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (cur, y, cur + 4, y, GRAY7))
                    cur += 90
                    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (cur - 4, y, cur + 36, y, GRAY7))
                    cur += 36
                elif pt.kind == "LDR":
                    o.append('<g class="el" data-part="%s" tabindex="0" role="button" aria-label="光敏電阻 %s,點一下看它在麵包板上的位置">' % (t, t))
                    o.append('<rect class="halo" x="%d" y="%d" width="92" height="68" rx="10" fill="none" stroke="%s" stroke-width="2.5"/>' % (cur - 1, y - 40, CLAY))
                    o.append('<rect x="%d" y="%d" width="92" height="68" rx="10" fill="#FFFFFF" opacity="0.001"/>' % (cur - 1, y - 40))
                    o.append(_zigzag(cur + 4, y, 82, 13, 6))
                    for dx in (0, 14):
                        o.append('<path d="M%d,%d l9,9 m-5,0 l5,0 l0,-5" fill="none" stroke="%s" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" transform="rotate(0)"/>' % (cur + 28 + dx, y - 38, RUST))
                    o.append(_txt(cur + 45, y + 34, "%s  光敏電阻" % t, "mb", SLATE))
                    o.append("</g>")
                    note("ldr", cur + 45, y - 52, "<b>光敏電阻(LDR)</b>:電阻加兩個<b>指向它的箭頭</b>(光)。光越亮,電阻越小。")
                    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (cur, y, cur + 4, y, GRAY7))
                    cur += 90
                    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (cur - 4, y, cur + 36, y, GRAY7))
                    cur += 36
                elif pt.kind == "BTN":
                    o.append('<g class="el" data-part="%s" tabindex="0" role="button" aria-label="按鈕 %s,點一下看它在麵包板上的位置">' % (t, t))
                    o.append('<rect class="halo" x="%d" y="%d" width="86" height="62" rx="10" fill="none" stroke="%s" stroke-width="2.5"/>' % (cur - 8, y - 36, CLAY))
                    o.append('<rect x="%d" y="%d" width="86" height="62" rx="10" fill="#FFFFFF" opacity="0.001"/>' % (cur - 8, y - 36))
                    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (cur, y, cur + 18, y, GRAY7))
                    o.append('<circle cx="%d" cy="%d" r="3.5" fill="%s"/><circle cx="%d" cy="%d" r="3.5" fill="%s"/>' % (cur + 18, y, GRAY7, cur + 54, y, GRAY7))
                    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (cur + 54, y, cur + 72, y, GRAY7))
                    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.4" stroke-linecap="round"/>' % (cur + 12, y - 22, cur + 60, y - 22, GRAY7))
                    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/><line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (cur + 36, y - 22, cur + 36, y - 31, GRAY7, cur + 36, y - 22, cur + 36, y - 14, GRAY7))
                    o.append(_txt(cur + 36, y + 34, "%s  按鈕" % t, "mb", SLATE))
                    o.append("</g>")
                    note("btn", cur + 36, y - 46, "<b>按鈕(開關)</b>:兩個接點,上方有一條可以壓下去的橫槓。<b>沒按時,兩個接點是斷開的;按下去,橫槓把兩個接點接通。</b>")
                    cur += 72
                    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (cur, y, cur + 40, y, GRAY7))
                    cur += 40
                elif pt.kind == "BZ":
                    o.append('<g class="el" data-part="%s" tabindex="0" role="button" aria-label="蜂鳴器 %s,點一下看它在麵包板上的位置">' % (t, t))
                    o.append('<rect class="halo" x="%d" y="%d" width="76" height="60" rx="10" fill="none" stroke="%s" stroke-width="2.5"/>' % (cur - 8, y - 30, CLAY))
                    o.append('<rect x="%d" y="%d" width="76" height="60" rx="10" fill="#FFFFFF" opacity="0.001"/>' % (cur - 8, y - 30))
                    o.append('<circle cx="%d" cy="%d" r="20" fill="#FFFFFF" stroke="%s" stroke-width="2"/>' % (cur + 30, y, GRAY7))
                    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (cur, y, cur + 10, y, GRAY7))
                    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (cur + 50, y, cur + 60, y, GRAY7))
                    o.append(_txt(cur + 20, y + 5, "+", "mb", RUST))
                    for k in (0, 1):
                        o.append('<path d="M%d,%d q5,%d 0,%d" fill="none" stroke="%s" stroke-width="1.6" stroke-linecap="round"/>' % (cur + 33 + k * 7, y - 9, 9, 18, GRAY7))
                    o.append(_txt(cur + 30, y + 44, "%s  蜂鳴器" % t, "mb", SLATE))
                    o.append("</g>")
                    note("bz", cur + 30, y - 38, "<b>蜂鳴器</b>:圓圈加 + 號與聲波弧線。+ 號那一側是正極(長腳),要接靠近電源 / 訊號的一邊。")
                    cur += 60
                    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (cur, y, cur + 40, y, GRAY7))
                    cur += 40
                elif pt.kind == "LED":
                    fill, stroke, zh, _vf = LED_C[pt.meta["color"]]
                    o.append('<g class="el" data-part="%s" tabindex="0" role="button" aria-label="LED %s,點一下看它在麵包板上的位置">' % (t, t))
                    o.append('<rect class="halo" x="%d" y="%d" width="76" height="56" rx="10" fill="none" stroke="%s" stroke-width="2.5"/>' % (cur - 8, y - 28, CLAY))
                    o.append('<rect x="%d" y="%d" width="76" height="56" rx="10" fill="#FFFFFF" opacity="0.001"/>' % (cur - 8, y - 28))
                    o.append('<polygon points="%d,%d %d,%d %d,%d" fill="%s" stroke="%s" stroke-width="2" stroke-linejoin="round"/>' % (cur, y - 18, cur, y + 18, cur + 34, y, fill, GRAY7))
                    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.6" stroke-linecap="round"/>' % (cur + 36, y - 18, cur + 36, y + 18, GRAY7))
                    for dx in (0, 11):
                        o.append('<path d="M%d,%d l9,-9 m-5,0 l5,0 l0,5" fill="none" stroke="%s" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>' % (cur + 26 + dx, y - 22, stroke))
                    o.append(_txt(cur + 4, y + 36, "A(+)", "m", RUST, "middle"))
                    o.append(_txt(cur + 36, y + 36, "K(−)", "m", GRAY7, "middle"))
                    o.append(_txt(cur + 18, y + 52, "%s  %s色" % (t, zh), "mb", SLATE))
                    o.append("</g>")
                    note("led", cur + 18, y - 38, "<b>LED(發光二極體)</b>:三角形加一條槓。三角形的底是<b>正極 A(長腳)</b>,槓那一側是<b>負極 K(短腳)</b>;電流只能從三角形往槓的方向流。旁邊兩個小箭頭表示「會發光」。")
                    cur += 36
                    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>' % (cur, y, cur + 40, y, GRAY7))
                    cur += 40
        maxx = max(maxx, cur)
    W = maxx + 70
    H = 74 + (len(circ.chains) - 1) * 118 + 90
    svg = ('<svg viewBox="0 0 %d %d" role="img" aria-label="原理圖:%s" style="min-width:520px">\n<defs>%s</defs>\n<rect width="%d" height="%d" fill="#FFFFFF"/>\n%s\n</svg>'
           % (W, H, e(" / ".join(" → ".join(c) for c in circ.chains)), STYLE, W, H, "".join(o)))
    legend.sort(key=lambda x: int(x[0]))
    return svg, legend


def parts_info(circ):
    """原理圖與麵包板連動時顯示的說明。"""
    info = {}
    for p in circ.parts:
        if p.kind == "R":
            info[p.ref] = "<b>電阻 %s(%s)</b>:原理圖上是鋸齒線;麵包板上是 <code>%s</code>–<code>%s</code> 之間那顆有色環的小圓柱(色環 %s)。" % (
                p.ref, fmt_ohm(p.meta["ohms"]), p.pins["1"], p.pins["2"], "、".join(_band_names(p.meta["ohms"])))
        elif p.kind == "LED":
            info[p.ref] = "<b>%s色 LED(%s)</b>:原理圖上是三角形加一條槓;麵包板上是插在 <code>%s</code>(長腳 +)與 <code>%s</code>(短腳 −)的小圓頭燈。" % (
                LED_C[p.meta["color"]][2], p.ref, p.pins["A"], p.pins["K"])
        elif p.kind == "LDR":
            info[p.ref] = "<b>光敏電阻(%s)</b>:原理圖上是電阻加兩個指向它的箭頭(光);麵包板上是表面有彎曲紋路的小圓片,插在 <code>%s</code> 與 <code>%s</code>。" % (p.ref, p.pins["1"], p.pins["2"])
        elif p.kind == "POT":
            info[p.ref] = "<b>電位器(%s)</b>:原理圖上是電阻加一個指向中間的箭頭(滑動腳);麵包板上是有旋鈕的三腳元件,中間腳插 <code>%s</code>。" % (p.ref, p.pins["W"])
        elif p.kind == "BTN":
            info[p.ref] = "<b>按鈕(%s)</b>:原理圖上是兩個接點加上方一條橫槓;麵包板上是跨在凹槽上的小方塊,接線用 <code>%s</code> 與 <code>%s</code> 這對角兩腳。" % (p.ref, p.pins["1"], p.pins["2"])
        elif p.kind == "BZ":
            info[p.ref] = "<b>%s</b>:原理圖上是圓圈加 + 號與聲波弧線;麵包板上是黑色圓柱形蜂鳴器,+ 腳插 <code>%s</code>、− 腳插 <code>%s</code>。" % (part_zh(p), p.pins["P"], p.pins["N"])
        else:
            info[p.ref] = "<b>%s</b>:原理圖上就是一條線,代表「這兩點接在一起」;麵包板上是這條 %s色杜邦線。" % (part_zh(p), WIRE_ZH[p.meta["color"]])
    return info


def _band_names(ohms):
    b = bands(ohms)
    return [BAND_NAME[b[0]], BAND_NAME[b[1]], BAND_NAME[b[2]] if b[2] != "gold" else "金", "金(±5%)"]


# ================================================================ Uno 板子導覽圖(不轉向,USB 在左)
def uno_overview_svg():
    """回傳 (svg, 圖例)。第 1 篇用:認識 Uno 板子上的各個部位。"""
    o = []
    X0, Y0, W, H = 40, 34, 520, 196
    o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s" stroke="%s" stroke-width="1.5"/>' % (X0, Y0, W, H, GRAY7, SLATE))
    o.append('<rect x="14" y="%d" width="64" height="58" rx="4" fill="%s" stroke="%s" stroke-width="1.5"/>' % (Y0 + 40, GRAY3, GRAY5))
    o.append(_txt(46, Y0 + 74, "USB-B", "m", GRAY7))
    o.append('<rect x="14" y="%d" width="56" height="52" rx="4" fill="%s" stroke="%s" stroke-width="1.5"/>' % (Y0 + 128, SLATE, GRAY5))
    o.append(_txt(42, Y0 + 158, "DC 電源孔", "m", GRAY3))
    # Reset 鈕
    o.append('<circle cx="116" cy="%d" r="10" fill="%s" stroke="%s" stroke-width="2"/>' % (Y0 + 52, RUST, SLATE))
    o.append(_txt(116, Y0 + 78, "RESET", "m", GRAY1))
    # 上排:數位腳位(實體順序,USB 在左)
    top = ["SCL", "SDA", "AREF", "GND", "13", "12", "~11", "~10", "~9", "8", None, "7", "~6", "~5", "4", "~3", "2", "TX1", "RX0"]
    xs = 150
    for i, lab in enumerate(top):
        if lab is None:
            continue
        x = xs + i * P
        o.append('<rect x="%.1f" y="%d" width="8" height="8" rx="1.5" fill="%s" stroke="%s"/>' % (x - 4, Y0 + 8, SLATE, GOLD))
        if len(lab) > 3:
            o.append('<text transform="translate(%.1f %d) rotate(-90)" font-size="8" font-family="ui-monospace,Menlo,Consolas,monospace" fill="%s" text-anchor="end">%s</text>' % (x + 3, Y0 + 44, GRAY1, lab))
        else:
            o.append(_txt(x, Y0 + 30, lab, "m", GRAY1))
    # 下排:電源 + 類比
    bot = ["", "IOREF", "RESET", "3.3V", "5V", "GND", "GND", "VIN", None, "A0", "A1", "A2", "A3", "A4", "A5"]
    xb = 230
    for i, lab in enumerate(bot):
        if lab is None or lab == "":
            continue
        x = xb + i * P
        o.append('<rect x="%.1f" y="%d" width="8" height="8" rx="1.5" fill="%s" stroke="%s"/>' % (x - 4, Y0 + H - 16, SLATE, GOLD))
        if len(lab) > 3:
            o.append('<text transform="translate(%.1f %d) rotate(-90)" font-size="8" font-family="ui-monospace,Menlo,Consolas,monospace" fill="%s" text-anchor="start">%s</text>' % (x + 3, Y0 + H - 22, GRAY1, lab))
        else:
            o.append(_txt(x, Y0 + H - 24, lab, "m", GRAY1))
    # ATmega328P、LED
    o.append('<rect x="390" y="%d" width="86" height="34" rx="3" fill="%s"/>' % (Y0 + 88, SLATE))
    o.append(_txt(433, Y0 + 109, "ATmega328P", "m", GRAY3))
    o.append(_txt(300, Y0 + 100, "ARDUINO UNO", "mb", GRAY1))
    for lab, x, col in (("L", xs + 4 * P, "#E1B93B"), ("TX", xs + 17 * P - 36, "#E1B93B"), ("RX", xs + 17 * P - 12, "#E1B93B")):
        pass
    for lab, x in (("L", xs + 4 * P - 9), ("TX", 262), ("RX", 286)):
        o.append('<rect x="%d" y="%d" width="12" height="7" rx="1.5" fill="#E1B93B" stroke="%s"/>' % (x, Y0 + 62, SLATE))
        o.append(_txt(x + 6, Y0 + 80, lab, "m", GRAY1))
    o.append('<rect x="%d" y="%d" width="12" height="7" rx="1.5" fill="%s" stroke="%s"/>' % (470, Y0 + 150, OLIVE, SLATE))
    o.append(_txt(486, Y0 + 157, "ON", "m", GRAY1, "start"))

    def mk(n, x, y):
        return ('<circle cx="%d" cy="%d" r="10" fill="%s"/><text x="%d" y="%d" class="mb" fill="#FFFFFF" text-anchor="middle">%d</text>' % (x, y, CLAY, x, y + 3.5, n))
    o.append(mk(1, 30, 52))
    o.append(mk(2, 90, 72))
    o.append(mk(3, 360, 16))
    o.append(mk(4, 330, 252))
    o.append(mk(5, 478 - 10, 252))
    o.append(mk(6, 433, 156))
    o.append(mk(7, 192, 100))
    o.append(mk(8, 30, 232))
    legend = [
        ("1", "<b>USB-B 接頭</b>:接電腦。同時負責供電、上傳程式、傳資料回電腦。"),
        ("2", "<b>RESET 按鈕</b>:按一下,程式從頭再跑一次。"),
        ("3", "<b>數位腳位 0–13</b>:可以輸出 0 V / 5 V,也可以讀取高低電位。前面有 <code>~</code> 的腳位可輸出 PWM(第 6 篇)。旁邊的 GND 是接地腳。"),
        ("4", "<b>電源腳位</b>:<code>5V</code> 與 <code>3.3V</code> 是輸出電源,<code>GND</code> 是接地(0 V)。<code>VIN</code> 是外部電源輸入。"),
        ("5", "<b>類比輸入 A0–A5</b>:讀取 0–5 V 之間的電壓大小(第 9 篇)。"),
        ("6", "<b>ATmega328P 晶片</b>:Uno 的大腦,你寫的程式就存在裡面。"),
        ("7", "<b>小燈</b>:<code>L</code> 接在 13 號腳(程式能控制);<code>TX</code>、<code>RX</code> 在傳資料時閃;右下 <code>ON</code> 表示有電。"),
        ("8", "<b>DC 電源孔</b>:接 7–12 V 的外部電源。只用 USB 時用不到。"),
    ]
    svg = ('<svg viewBox="0 0 600 270" role="img" aria-label="Arduino Uno 板子各部位導覽圖" style="min-width:520px">\n<defs>%s</defs>\n<rect width="600" height="270" fill="#FFFFFF"/>\n%s\n</svg>'
           % (STYLE, "".join(o)))
    return svg, legend


# ================================================================ 麵包板內部連線探索圖(第 2 篇)
def explorer_svg(n=20):
    """可點孔位、看哪些孔相通的麵包板。孔位帶 data-net(整條電源軌)與 data-net2(電源軌中間斷開)。"""
    lay = Layout(n)
    y0 = lay.by - 6
    h = lay.bottom - y0 + 6
    base = _breadboard(lay)
    cells = []
    for r in "abcdefghij":
        for c in range(1, n + 1):
            x, y = lay.xy("%s%d" % (r, c))
            net = "s%d%s" % (c, "t" if r in "abcde" else "b")
            cells.append('<rect class="bh" x="%.1f" y="%.1f" width="16" height="16" data-h="%s%d" data-net="%s" data-net2="%s"/>' % (x - 8, y - 8, r, c, net, net))
    for rn in ("t+", "t-", "b+", "b-"):
        for c in range(1, n + 1):
            x, y = lay.xy("%s%d" % (rn, c))
            side = "L" if c <= n // 2 else "R"
            cells.append('<rect class="bh" x="%.1f" y="%.1f" width="16" height="16" data-h="%s%d" data-net="r%s" data-net2="r%s%s"/>' % (x - 8, y - 8, rn, c, rn, rn, side))
    label = "可以點擊的麵包板:點任一個孔,看哪些孔在內部相通"
    return ('<svg viewBox="0 %d %d %d" role="group" aria-label="%s" style="min-width:520px">\n<defs>%s</defs>\n<rect y="%d" width="%d" height="%d" fill="#FFFFFF"/>\n%s\n%s\n</svg>'
            % (y0, lay.bw + 60, h, label, STYLE, y0, lay.bw + 60, h, base, "".join(cells)))
