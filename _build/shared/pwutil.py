"""Playwright 驗證用的共用小工具(verify.py、arduino/verify_arduino.py、microfilm/check.py 都用)。"""
import re

# Cloudflare Web Analytics(選用,見 seo.py 的 ANALYTICS_TOKEN)的網域:static.cloudflareinsights.com 與 cloudflareinsights.com
_ANALYTICS = re.compile(r"^https?://([^/]*\.)?cloudflareinsights\.com/")


def stub_analytics(ctx):
    """離線驗證用 file:// 開頁(origin 為 null),Cloudflare Web Analytics 的 beacon 會對
    cloudflareinsights.com 發 CORS 請求而被擋、噴 console error,使 workflow 失敗。驗證不需要
    真的送資料,所以把這個網域(含子網域)的請求直接用空回應攔下來。每個 new_context() 後都要呼叫。"""
    ctx.route(
        _ANALYTICS,
        lambda route: route.fulfill(
            status=200,
            content_type="application/javascript",
            headers={"Access-Control-Allow-Origin": "*"},
            body="",
        ),
    )
