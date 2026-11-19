"""把「另一份專案」裡新做的主題整併進本專案。

另一份專案 = 含 public/index.html 的 zip 或資料夾（通常是 github 主題 + 一個新主題）。
本程式只做機械的部分；需要判斷的部分（THEMES 設定、主題 README、文件濃縮）見 _build/README.md 第 11 節。

用法（在 repo 根目錄）：
    python3 _build/merge_theme.py NEW.zip --dry-run        # 只分析、不寫入：看會整併什麼、有哪些風險
    python3 _build/merge_theme.py NEW.zip                  # 整併（自動偵測本專案沒有的主題）
    python3 _build/merge_theme.py NEW.zip --theme docker   # 指定主題 id
    python3 _build/merge_theme.py NEW.zip --verify --zip /tmp/upload.zip   # 整併後跑全站驗證並打包上傳用 zip

自動完成：
  1. 複製 public/<主題>/ 全部頁面（已存在則停下，除非 --force）
  2. 把來源首頁 SITE 裡的該主題分類，轉成本專案首頁的格式，插入 SITE 最後（在「更多主題」之前）
  3. 每頁「← 回教學首頁」改成 ../index.html#<主題>；頁面與首頁全部轉全形標點（shared/fw.py）
  4. 檢查：設計 tokens 是否與 github 樣板一致、localStorage、外部連結、站內連結與 prev/next
  5. 把來源的製作檔放進 _build/<主題>/；與共用檔同名但內容不同的，放進 _build/<主題>/_incoming/ 等人工合併
  6. 在 build.py 的 THEMES 加一筆待確認的設定；更新根目錄 README.md 與 _build/README.md 的主題表與資料夾地圖
  7. 不帶入 HANDOFF、DESIGN、進度檔等過程文件（主題相關的規劃檔放進 _incoming/ 供濃縮成主題 README）
"""
import argparse, glob, json, os, re, shutil, subprocess, sys, tempfile, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "shared"))
import fw  # noqa: E402

SHARED_NAMES = {"build.py", "common.js", "h.py", "fw.py", "verify.py", "update_index.py", "merge_theme.py"}
SKIP_DOCS = {"README.md", "HANDOFF.md", "DESIGN.md", "00-SESSION-HANDOFF.md"}
JUNK = re.compile(r"(__pycache__|\.pyc$|^shot_.*\.png$|\.png$|^simpin$|\.DS_Store)")
TOKENS = ["--ivory", "--white", "--slate", "--clay", "--clay-d", "--oat", "--olive", "--rust",
          "--gray-100", "--gray-300", "--gray-500", "--gray-700"]
notes = []   # 最後印出的「請人工確認」清單


def warn(msg):
    notes.append(msg)
    print("  ⚠", msg)


def find_root(path):
    for dp, dn, fn in os.walk(path):
        if os.path.exists(os.path.join(dp, "public", "index.html")):
            return dp
    raise SystemExit("找不到 public/index.html：這不是教學站專案")


def read(p):
    return open(p, encoding="utf-8").read()


def write(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(s)


def site_block(index_html):
    m = re.search(r"var SITE = (\[[\s\S]*?\n  \]);", index_html)
    if not m:
        raise SystemExit("首頁找不到 `var SITE = [...]`")
    return m


def load_site(index_html):
    """用 node 求值 SITE（首頁資料是 JS 物件字面值）。"""
    js = "const S=eval(require('fs').readFileSync(0,'utf8'));process.stdout.write(JSON.stringify(S))"
    r = subprocess.run(["node", "-e", js], input=site_block(index_html).group(1), capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("node 解析 SITE 失敗：" + r.stderr[:300])
    return json.loads(r.stdout)


def j(x):
    return json.dumps(x, ensure_ascii=False)


def category_js(c):
    """轉成本專案首頁 SITE 的寫法（欄位名 foot、tldr 不含 TL;DR 標籤）。"""
    h = c.get("hero")
    if not h:
        warn("來源的 %s 分類沒有 hero，首頁切換到該分頁時會缺少標題文字，請補上" % c["id"])
        h = {"h1": c["label"], "sub": "", "tldr": ""}
    tldr = re.sub(r'^<b class="l">TL;DR</b>\s*', "", h.get("tldr", ""))
    foot = c.get("foot", c.get("footNote", ""))
    L = ['    { id:%s, label:%s,' % (j(c["id"]), j(c["label"])),
         '      hero:{ h1:%s,' % j(h["h1"]),
         '        sub:%s,' % j(h.get("sub", "")),
         '        tldr:%s },' % j(tldr),
         '      pathTitle:%s,' % j(c.get("pathTitle", "學習路徑")),
         '      pathNote:%s,' % j(c.get("pathNote", "")),
         '      foot:%s,' % j(foot),
         '      stages:[']
    st = []
    for sg in c["stages"]:
        pg = []
        for q in sg["pages"]:
            pg.append('        { n:%d, title:%s, href:%s, status:%s, level:%s, mins:%d, elective:%s,\n          summary:%s }' % (
                q["n"], j(q["title"]), j(q["href"]), j(q.get("status", "done")), j(q.get("level", "基礎")),
                q.get("mins", 10), "true" if q.get("elective") else "false", j(q.get("summary", ""))))
        st.append('      { name:%s, pages:[\n%s\n      ]}' % (j(sg["name"]), ",\n".join(pg)))
    L.append(",\n".join(st))
    L.append('    ],')
    L.append('    quick:[')
    L.append(",\n".join('      { t:%s, n:%d%s }' % (j(q["t"]), q["n"], (', a:%s' % j(q["a"])) if q.get("a") else "")
                        for q in c.get("quick", [])))
    miss = [q["t"] for q in c.get("quick", []) if not q.get("a")]
    if miss:
        notes.append("首頁 quick 有 %d 項沒有 a（錨點），要補成目標頁的 section id：%s" % (len(miss), "、".join(miss)))
    L.append('    ]}')
    return "\n".join(L)


def root_tokens(html):
    m = re.search(r":root\s*\{(.*?)\}", html, re.S)
    if not m:
        return {}
    d = dict(re.findall(r"(--[a-z0-9-]+)\s*:\s*([^;]+);", m.group(1)))
    return {k: v.strip().upper() for k, v in d.items() if k in TOKENS}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="另一份專案的 zip 或資料夾")
    ap.add_argument("--theme", help="要整併的主題 id（預設：自動偵測本專案沒有的主題）")
    ap.add_argument("--target", default=os.path.dirname(HERE), help="本專案根目錄（預設：本檔所在 repo）")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="主題資料夾已存在時覆蓋")
    ap.add_argument("--verify", action="store_true", help="整併後執行 _build/verify.py（需要 playwright）")
    ap.add_argument("--zip", help="整併後打包成上傳用 zip（不含暫存與編譯產物）")
    a = ap.parse_args()

    T = os.path.abspath(a.target)
    tmp = None
    src = a.source
    if os.path.isfile(src) and src.endswith(".zip"):
        tmp = tempfile.mkdtemp(prefix="newtheme-")
        zipfile.ZipFile(src).extractall(tmp)
        src = tmp
    S = find_root(src)
    print("來源專案：", S, "\n本專案：  ", T)

    t_index = read(os.path.join(T, "public", "index.html"))
    s_index = read(os.path.join(S, "public", "index.html"))
    t_site, s_site = load_site(t_index), load_site(s_index)
    have = [c["id"] for c in t_site]
    cands = [c for c in s_site if c["id"] not in have]
    if a.theme:
        cands = [c for c in s_site if c["id"] == a.theme]
        if not cands:
            raise SystemExit("來源首頁沒有 id=%s 的分類（來源有：%s）" % (a.theme, [c["id"] for c in s_site]))
    if not cands:
        raise SystemExit("來源沒有本專案缺少的主題（本專案已有：%s）" % have)
    if len(cands) > 1:
        raise SystemExit("來源有多個新主題 %s，請用 --theme 一次指定一個" % [c["id"] for c in cands])
    cat = cands[0]
    tid = cat["id"]
    n_pages = sum(len(s["pages"]) for s in cat["stages"])
    print("\n要整併的主題：%s（%s），%d 篇，%d 個階段" % (tid, cat["label"], n_pages, len(cat["stages"])))

    s_pub = os.path.join(S, "public", tid)
    t_pub = os.path.join(T, "public", tid)
    if not os.path.isdir(s_pub):
        raise SystemExit("來源沒有 public/%s/" % tid)
    if os.path.exists(t_pub) and not a.force:
        raise SystemExit("本專案已有 public/%s/，若要覆蓋請加 --force" % tid)
    files = sorted(glob.glob(os.path.join(s_pub, "*.html")))
    print("頁面檔：%d 個" % len(files))

    # ---- 分析 ----
    print("\n檢查：")
    ref = root_tokens(read(os.path.join(T, "public", "github", "github-pr-guide.html")))
    names = {os.path.basename(f) for f in files}
    for q in [p for s in cat["stages"] for p in s["pages"]]:
        if q["href"].split("/")[0] != tid or q["href"].split("/")[-1] not in names:
            warn("SITE 的 %s 第 %d 篇指向不存在的檔案：%s" % (tid, q["n"], q["href"]))
    ls_pages, http_pages, bad_tokens = [], [], []
    for f in files:
        h = read(f)
        d = {k: v for k, v in root_tokens(h).items() if ref.get(k) != v}
        if d:
            bad_tokens.append((os.path.basename(f), d))
        if "localStorage" in h:
            ls_pages.append(os.path.basename(f))
        urls = [u for u in re.findall(r'https?://[^"\'\s<)]+', h) if "w3.org" not in u]
        if urls:
            http_pages.append((os.path.basename(f), urls[0]))
        for ref_href in re.findall(r'<a class="(?:prev|next)" href="([^"#]+)"', h):
            if ref_href not in names:
                warn("%s 的上一篇／下一篇指向不存在的 %s" % (os.path.basename(f), ref_href))
    # 前後頁鏈：第一頁沒有 prev、最後一頁沒有 next，其餘都要有（來源若用「檔案存在才顯示」產生 next，常整排缺漏）
    _pv, _nx = {}, {}
    for f in files:
        h = read(f)
        for kind, dst in (("prev", _pv), ("next", _nx)):
            mm = re.search(r'<a class="%s" href="([^"#]+)"' % kind, h)
            if mm:
                dst[os.path.basename(f)] = mm.group(1)
    if len(files) > 1:
        _no_prev = [n for n in names if n not in _pv]
        _no_next = [n for n in names if n not in _nx]
        if len(_no_prev) != 1 or len(_no_next) != 1:
            warn("上一篇／下一篇沒接成一條鏈：沒有上一篇的頁面 %s、沒有下一篇的頁面 %s（應各只有一頁）；請改規格檔，只依篇章順序決定 prev／next" % (_no_prev, _no_next))
    if bad_tokens:
        warn("設計 tokens 與 github 樣板不同的頁面 %d 個，例如 %s：%s（風格可能不一致）" % (len(bad_tokens), bad_tokens[0][0], bad_tokens[0][1]))
    else:
        print("  ✓ 所有頁面的設計 tokens 與 github 樣板一致")
    if ls_pages:
        warn("使用 localStorage 的頁面：%s（規範只允許首頁與少數例外，請確認有 try/catch 並寫進主題 README）" % ls_pages)
    if http_pages:
        warn("含外部連結的頁面 %d 個，例如 %s → %s（請確認符合主題的連結規則）" % (len(http_pages), http_pages[0][0], http_pages[0][1]))

    # 製作檔分類
    s_build = os.path.join(S, "_build")
    t_theme_dirs = [d for d in glob.glob(os.path.join(T, "_build", "*")) if os.path.isdir(d)]
    plan_copy, plan_incoming, plan_skip = [], [], []
    if os.path.isdir(s_build):
        for dp, dn, fn in os.walk(s_build):
            dn[:] = [d for d in dn if not JUNK.search(d)]
            for f in fn:
                if JUNK.search(f):
                    continue
                p = os.path.join(dp, f)
                rel = os.path.relpath(p, s_build)
                same = False
                for d in t_theme_dirs:
                    q = os.path.join(d, rel)
                    if os.path.exists(q) and open(q, "rb").read() == open(p, "rb").read():
                        same = True
                if os.path.exists(os.path.join(T, "_build", rel)) and open(os.path.join(T, "_build", rel), "rb").read() == open(p, "rb").read():
                    same = True
                if same:
                    plan_skip.append(rel)
                elif os.path.basename(rel) in SHARED_NAMES:
                    plan_incoming.append(rel)
                elif re.match(r"p\d+\.py$", rel):          # github 規格檔但內容不同：人工比對
                    plan_incoming.append(rel)
                else:
                    plan_copy.append(rel)
    docs = [f for f in glob.glob(os.path.join(S, "*.md")) if os.path.basename(f) not in SKIP_DOCS]
    theme_docs = [f for f in docs if tid.lower() in os.path.basename(f).lower() or tid.lower() in read(f)[:400].lower()]
    ignored_docs = [os.path.basename(f) for f in glob.glob(os.path.join(S, "*.md")) if f not in theme_docs]
    print("\n製作檔：直接帶入 %d 個、與共用檔衝突需人工合併 %d 個、與本專案相同略過 %d 個" % (len(plan_copy), len(plan_incoming), len(plan_skip)))
    if plan_incoming:
        print("  需人工合併（會附 .diff 供比對；多半只是來源版本較舊）：", plan_incoming)
    print("不帶入的文件：", ignored_docs, "｜轉成 _incoming 供濃縮的主題文件：", [os.path.basename(f) for f in theme_docs])

    if a.dry_run:
        print("\n（--dry-run：沒有寫入任何檔案）")
        return

    # ---- 寫入 ----
    print("\n整併中…")
    if os.path.exists(t_pub):
        shutil.rmtree(t_pub)
    os.makedirs(t_pub)
    for f in os.listdir(s_pub):
        p = os.path.join(s_pub, f)
        if os.path.isfile(p) and not JUNK.search(f):
            shutil.copy(p, os.path.join(t_pub, f))
    crumb = re.compile(r'(<nav class="crumb"[^>]*><a href=")\.\./index\.html(?:#[\w-]*)?(")')
    changed = 0
    for f in sorted(glob.glob(os.path.join(t_pub, "*.html"))):
        s = read(f)
        s2, n = crumb.subn(r"\g<1>../index.html#%s\2" % tid, s)
        if n != 1:
            warn("%s 找不到唯一的「回教學首頁」連結（找到 %d 個）" % (os.path.basename(f), n))
        s2 = fw.apply(s2)
        changed += s2 != s
        write(f, s2)
    print("  頁面 %d 個（已改回首頁連結並轉全形標點，其中 %d 個內容有變動）" % (len(files), changed))

    m = site_block(t_index)
    start = m.start(1)
    end = t_index.index("\n  ];", start)
    new_index = t_index[:end] + ",\n" + category_js(cat) + t_index[end:]
    new_index = fw.apply(new_index)
    write(os.path.join(T, "public", "index.html"), new_index)
    print("  首頁 SITE 已新增 %s（%d 篇），並整理為全形標點" % (tid, n_pages))

    bt = os.path.join(T, "_build", tid)
    for rel in plan_copy:
        os.makedirs(os.path.dirname(os.path.join(bt, rel)), exist_ok=True)
        shutil.copy(os.path.join(s_build, rel), os.path.join(bt, rel))
    for rel in plan_incoming:
        dst = os.path.join(bt, "_incoming", rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(s_build, rel), dst)
        mine = [q for q in (os.path.join(T, "_build", "shared", os.path.basename(rel)), os.path.join(T, "_build", rel),
                            os.path.join(T, "_build", "github", os.path.basename(rel))) if os.path.exists(q)]
        if mine:   # 附上與本專案版本的差異，方便判斷來源有沒有本專案缺少的新功能
            import difflib
            d = difflib.unified_diff(read(mine[0]).splitlines(), read(os.path.join(s_build, rel)).splitlines(),
                                     "本專案/" + os.path.basename(rel), "來源/" + rel, lineterm="")
            write(dst + ".diff", "\n".join(d) + "\n")
    for f in theme_docs:
        dst = os.path.join(bt, "_incoming", os.path.basename(f))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(f, dst)
    for rel in plan_copy:
        if rel.endswith(".py"):
            t = read(os.path.join(bt, rel))
            if re.search(r"dirname\(HERE\)", t) and "public" in t:
                warn("_build/%s/%s 以 `dirname(HERE)` 推算 public/ 路徑；它現在在子資料夾裡，需改成往上兩層（os.path.dirname 多包一層）" % (tid, rel))
    print("  製作檔 → _build/%s/（%d 個）%s" % (tid, len(plan_copy), "；衝突與主題文件 → _incoming/" if plan_incoming or theme_docs else ""))

    # 規格檔字首猜測
    prefixes = {}
    for rel in plan_copy:
        mm = re.match(r"([a-z]+)\d+\.py$", os.path.basename(rel))
        if mm and "/" not in rel.replace("\\", "/"):
            prefixes[mm.group(1)] = prefixes.get(mm.group(1), 0) + 1
    used = set(re.findall(r'prefix="(\w+)"', read(os.path.join(T, "_build", "build.py"))))
    prefix = None
    for k, _ in sorted(prefixes.items(), key=lambda kv: -kv[1]):
        if k not in used:
            prefix = k
            break
    if not prefix:
        prefix = "x"
        warn("猜不到規格檔字首（或與既有主題衝突），THEMES 暫用 prefix=\"x\"，請改成實際字首")
    bp = os.path.join(T, "_build", "build.py")
    b = read(bp)
    sb = os.path.join(s_build, "build.py")
    uniq = os.path.exists(sb) and "def uniq_svg" in read(sb)      # 來源有 SVG id 重新編號就沿用
    if '"%s": dict(' % tid not in b:
        i = b.index("THEMES = {")
        j2 = b.index("\n}\n", i)
        stub = ('    "%s": dict(\n        prefix="%s", topic=%s, foot="", css=None, js=None, fw=True, uniq_svg=%s),'
                '   # TODO(merge_theme)：確認 topic / foot / css / js\n') % (tid, prefix, j(cat["label"] + "入門"), uniq)
        b = b[:j2 + 1] + stub + b[j2 + 1:]
        write(bp, b)
    warn("build.py 的 THEMES 已加入 %s 的暫定設定，請對照來源 build.py 確認 topic / foot / css / js / uniq_svg，並把來源的特殊處理合併進 build()" % tid)

    # README：根目錄主題表與結構、_build 資料夾地圖
    rp = os.path.join(T, "README.md")
    r = read(rp)
    row = "| %s | `public/%s/` | %d | %s |" % (cat["label"], tid, n_pages, (cat.get("hero") or {}).get("h1", ""))
    lines = r.split("\n")
    idx = [k for k, l in enumerate(lines) if l.startswith("| ") and "public/" in l]
    if idx and ("public/%s/" % tid) not in r:
        lines.insert(idx[-1] + 1, row)
    r = "\n".join(lines)
    r = tree_add(r, "public/", "%s/" % tid, "%s-<子題>-guide.html" % tid)
    write(rp, r)
    bp2 = os.path.join(T, "_build", "README.md")
    br = read(bp2)
    br = tree_add(br, "_build/", "%s/" % tid, "%s1 … ；README.md" % prefix)
    br = re.sub(r"(由檔名開頭決定：[^。]*?)(。)", lambda mm: mm.group(1) + "、`%s*` = %s" % (prefix, tid) + mm.group(2), br, count=1) if ("`%s*`" % prefix) not in br else br
    write(bp2, br)
    stub_readme = os.path.join(bt, "README.md")
    if not os.path.exists(stub_readme):
        write(stub_readme, "# %s 主題（`public/%s/`，%d 篇）\n\n先讀上一層的 [`../README.md`](../README.md)。\n\n"
              "> TODO(merge_theme)：把 `_incoming/` 裡的規劃文件濃縮成本主題的決定、內容規則、專用工具與驗證方式，然後刪除 `_incoming/`。\n"
              % (cat["label"], tid, n_pages))
    warn("README.md 的查證日期說明、設計原則、_build/README.md 的 SPEC 欄位與 THEMES 說明，請依新主題內容檢查是否需要補充")
    print("  README.md 與 _build/README.md 已加入主題列與資料夾地圖")

    if a.verify:
        print("\n執行全站驗證…")
        subprocess.call([sys.executable, os.path.join(T, "_build", "verify.py")])
    if a.zip:
        for dp, dn, fn in os.walk(T):
            for d in list(dn):
                if d == "__pycache__":
                    shutil.rmtree(os.path.join(dp, d)); dn.remove(d)
        with zipfile.ZipFile(a.zip, "w", zipfile.ZIP_DEFLATED) as z:
            for dp, dn, fn in os.walk(T):
                dn[:] = [d for d in dn if d not in (".git", "__pycache__", "_incoming")]
                for f in fn:
                    if JUNK.search(f):
                        continue
                    p = os.path.join(dp, f)
                    z.write(p, os.path.relpath(p, T))
        print("已打包（不含 _incoming、暫存與編譯產物）：", a.zip)

    print("\n=== 請人工確認（%d 項）===" % len(notes))
    for k, n in enumerate(notes, 1):
        print("%d. %s" % (k, n))
    print("\n接著：照 _build/README.md 第 11 節完成「判斷型」步驟，最後跑 python3 _build/verify.py。")
    if tmp:
        shutil.rmtree(tmp, ignore_errors=True)


def tree_add(text, anchor, name, comment):
    """README 裡以 ├── / └── 畫的目錄樹：找到以 anchor 開頭的那一行，在該區塊最後新增一項。"""
    lines = text.split("\n")
    first = next((k for k, l in enumerate(lines) if l.startswith(anchor)), None)
    if first is None:
        return text
    last = None
    for k in range(first + 1, len(lines)):
        if lines[k].startswith("```") or not lines[k].strip():
            break
        if lines[k].startswith("└── "):
            last = k
    if last is None or any(l.startswith(("├── " + name, "└── " + name)) for l in lines[first:]):
        return text
    lines[last] = "├── " + lines[last][4:]
    lines.insert(last + 1, "└── " + name.ljust(21) + comment)
    return "\n".join(lines)


if __name__ == "__main__":
    main()
