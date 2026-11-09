# -*- coding: utf-8 -*-
"""打包目前的 repo 成 zip(容器會重置,每完成一頁就打包一次)。用法: python3 package.py p01
同時重新產生 ARDUINO-PROGRESS.md 裡的頁面狀態表(依 public/index.html 的 status)。"""
import os, re, sys, shutil, zipfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
label = sys.argv[1] if len(sys.argv) > 1 else "latest"

# 1) 更新進度表
idx = open(os.path.join(ROOT, "public", "index.html"), encoding="utf-8").read()
arduino = idx[idx.index('{ id:"arduino"'):]
rows = re.findall(r'\{ n:(\d+), title:"([^"]+)", href:"arduino/([^"]+)", status:"(\w+)"', arduino)
lines = ["| # | 標題 | 檔案 | 狀態 |", "|---|---|---|---|"]
for n, t, f, st in rows:
    lines.append("| %s | %s | `%s` | %s |" % (n, t, f, "✅ 完成" if st == "done" else "⬜ 規劃中"))
done = sum(1 for r in rows if r[3] == "done")
block = "<!-- STATUS:START -->\n完成 %d / %d 篇(依 `public/index.html` 自動產生)\n\n%s\n<!-- STATUS:END -->" % (done, len(rows), "\n".join(lines))
pp = os.path.join(ROOT, "ARDUINO-PROGRESS.md")
s = open(pp, encoding="utf-8").read()
if "<!-- STATUS:START -->" in s:
    s = re.sub(r"<!-- STATUS:START -->.*?<!-- STATUS:END -->", block, s, flags=re.S)
else:
    s = s.replace("## 狀態", "## 頁面狀態\n" + block + "\n\n## 基礎建設", 1)
open(pp, "w", encoding="utf-8").write(s)

# 2) 打包
tmp = "/tmp/pkg"
shutil.rmtree(tmp, ignore_errors=True)
dst = os.path.join(tmp, "github-tutorial-repo")
shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns("__pycache__", "shots", "simpin", ".git", ".github"))
os.makedirs("/mnt/user-data/outputs", exist_ok=True)
out = "/mnt/user-data/outputs/arduino-site-after-%s.zip" % label
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for dp, dn, fn in os.walk(tmp):
        for f in fn:
            fp = os.path.join(dp, f)
            z.write(fp, os.path.relpath(fp, tmp))
print("打包完成:%s(%d KB),完成 %d / %d 篇" % (out, os.path.getsize(out) // 1024, done, len(rows)))
