"""首頁 SITE 維護:把某主題的指定篇號 status 改成 done / planned,並讓首頁文字維持全形標點。
用法(在 repo 根目錄):
    python3 _build/update_index.py microfilm done 7 8 9
    python3 _build/update_index.py github planned 12
    python3 _build/update_index.py            # 只做全形標點整理(不改狀態)
只改 public/index.html;新增整個主題分類(id / label / hero / stages / quick)請直接編輯 SITE,見 _build/README.md。"""
import re, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "shared"))
import fw

P = os.path.join(os.path.dirname(HERE), "public", "index.html")
s = open(P, encoding="utf-8").read()
args = sys.argv[1:]
if len(args) >= 3 and args[1] in ("done", "planned"):
    theme, status, nums = args[0], args[1], args[2:]
    a = s.index('{ id:"%s"' % theme)
    m = re.search(r'\n    \{ id:"|\n  \];', s[a + 1:])
    b = a + 1 + m.start()
    blk = s[a:b]
    for n in nums:
        blk, k = re.subn(r'(\{ n:%s,[^}]*?status:")\w+(")' % n, r"\g<1>%s\g<2>" % status, blk, flags=re.S)
        if not k:
            raise SystemExit("找不到 %s 第 %s 篇" % (theme, n))
    s = s[:a] + blk + s[b:]
elif args:
    raise SystemExit(__doc__)
s = fw.apply(s)
open(P, "w", encoding="utf-8").write(s)
print("done:", len(re.findall(r'status:"done"', s)), "planned:", len(re.findall(r'status:"planned"', s)))
