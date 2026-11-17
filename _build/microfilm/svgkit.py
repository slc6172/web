"""微電影主題的繪圖輔助。薄包裝:實際繪圖邏輯只在 kit.js(單一來源),
這裡用 node 預先產生靜態 SVG,所以頁面不依賴 JS 也看得到圖;互動頁另外內嵌 kit.js 即時重畫。

用法:
    from svgkit import *
    shot(people=[P(120, 130, who="an", pose="walk")], label="小安走過走廊")
    shot(scene="gate", zoom=2, cx=200, cy=80, grid=True, people=[...])
    sb(1, shot(...), "小安快步走過走廊。", "全景,固定鏡頭")      # 一格分鏡卡(HTML)
"""
import json, os, subprocess, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "kit.js")
_n = [0]
_cache = {}


def _node(fn, kw):
    _n[0] += 1
    kw = dict(kw)
    kw.setdefault("uid", "k%d" % _n[0])
    key = fn + json.dumps(kw, sort_keys=True, ensure_ascii=False)
    key = hashlib.md5(key.encode()).hexdigest()
    if key in _cache:
        return _cache[key]
    code = ("const K=require(process.argv[1]);const o=JSON.parse(process.argv[2]);"
            "process.stdout.write(K[process.argv[3]](o))")
    r = subprocess.run(["node", "-e", code, KIT, json.dumps(kw, ensure_ascii=False), fn],
                       capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr)
    _cache[key] = r.stdout
    return r.stdout


def P(x, y, h=100, facing="r", pose="stand", who="an", expr="neutral"):
    """一個角色。y 是腳底;h 是身高(世界座標)。who:an=小安 / yu=小宇 / x=路人。"""
    return dict(x=x, y=y, h=h, facing=facing, pose=pose, who=who, expr=expr)


def A(x1, y1, x2, y2, kind="move", label=None):
    """箭頭。kind:move=人物移動(實線)/ cam=鏡頭移動(橘色虛線)。"""
    return dict(x1=x1, y1=y1, x2=x2, y2=y2, kind=kind, label=label)


def N(name, x, y, s=1):
    """道具。name:note(紙條)/ phone。"""
    return dict(name=name, x=x, y=y, s=s)


def shot(**kw):
    return _node("shot", kw)


def inline_kit():
    """互動頁用:回傳要內嵌的 kit.js 原始碼。"""
    return open(KIT, encoding="utf-8").read()


# ---------- 分鏡卡(HTML) ----------
def sb(n, pic, action, cam, dial="", mk=False, ids=None):
    """一格分鏡:編號 + 畫面 + 動作/對白 + 鏡頭說明。pic 是 shot() 的結果。
    mk=True 時在三個欄位前加橘色編號 ①②③(教欄位用);ids=(動作id, 鏡頭id) 讓頁面 JS 即時改字。"""
    m = lambda k: '<i class="mk">%d</i>' % k if mk else ""
    ia, ic = (' id="%s"' % ids[0], ' id="%s"' % ids[1]) if ids else ("", "")
    d = '<div><b>對白</b><span>%s</span></div>' % dial if dial else ""
    return ('<figure class="sb"><div class="sb-pic"><span class="sb-n">%s</span>%s%s</div>'
            '<figcaption><div>%s<b>動作</b><span%s>%s</span></div>%s<div>%s<b>鏡頭</b><span%s>%s</span></div></figcaption></figure>'
            % (n, m(1), pic, m(2), ia, action, d, m(3), ic, cam))


def sbrow(*cards, cols=None):
    cols = cols or len(cards)
    return '<div class="sbrow c%d">%s</div>' % (cols, "".join(cards))


# ---------- 第 7–16 篇新增 ----------
def angle(**kw):
    """拍攝角度圖。angle: eye / high / low / dutch;who: an / yu;expr;hzline=True 畫出地平線。"""
    return _node("angleShot", kw)


def lens(**kw):
    """景深物件圖:D=鏡頭離主角的距離、F=焦距倍率(主角身高 100*F/D)。blur 讓遠近物件模糊。face/pose/expr、zw(牆的距離)、shift、camH、hz。"""
    return _node("lens", kw)


def topdown(**kw):
    """俯視示意圖。people=[dict(x,y,dir,who,name)]、cams=[dict(x,y,tx,ty,ok,name)]、axis=軸線 y、zone='top'|'bottom'。"""
    return _node("topdown", kw)


def move(name, t=0, **kw):
    """運鏡動畫的某一格(t=0..1)。name: pan/tilt/track/follow/orbit/push/pull/rise/zoom/vertigo/handheld/drone/slow/longtake。cam=dict(kind=,dir=) 畫橘色運鏡箭頭。"""
    return _node("moveFrame", dict(kw, name=name, t=t))
