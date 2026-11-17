"""站台層檔案:把 head 中繼資料、skip link 套到 public/ 底下所有頁面(冪等),並產生
robots.txt、sitemap.xml、_headers。

用法(repo 根目錄):  python3 _build/site_files.py
  - build.py 組出來的頁面本來就會套用;這支負責手寫頁(index.html、github-pr-guide.html)
    與既有頁面的就地補強,並重新產生 sitemap.xml。
  - 新增主題或改了 shared/seo.py 的 SITE_URL 後,重跑一次即可。
"""
import os, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "shared"))
import seo

PUB = os.path.join(os.path.dirname(HERE), "public")


def pages():
    out = ["index.html"]
    for d in sorted(x for x in os.listdir(PUB) if os.path.isdir(os.path.join(PUB, x))):
        out += sorted(d + "/" + os.path.basename(f) for f in glob.glob(os.path.join(PUB, d, "*.html")))
    return out


def main():
    ps = pages()
    n = 0
    for rel in ps:
        p = os.path.join(PUB, rel)
        h = open(p, encoding="utf-8").read()
        new = seo.apply(h, rel)
        if new != h:
            open(p, "w", encoding="utf-8").write(new)
            n += 1
    print("patched", n, "of", len(ps), "pages")

    if seo.SITE_URL:
        urls = "\n".join("  <url><loc>%s</loc></url>" % seo.page_url(r) for r in ps)
        open(os.path.join(PUB, "sitemap.xml"), "w", encoding="utf-8").write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>\n' % urls)
        open(os.path.join(PUB, "robots.txt"), "w", encoding="utf-8").write(
            "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % seo.SITE_URL)
    else:
        print("SITE_URL 為空:略過 sitemap.xml 與 robots.txt 的 Sitemap 行")
        open(os.path.join(PUB, "robots.txt"), "w", encoding="utf-8").write("User-agent: *\nAllow: /\n")

    open(os.path.join(PUB, "_headers"), "w", encoding="utf-8").write(
        "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n"
        "  X-Frame-Options: SAMEORIGIN\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n")
    print("wrote robots.txt, _headers" + (", sitemap.xml (%d urls)" % len(ps) if seo.SITE_URL else ""))


if __name__ == "__main__":
    main()
