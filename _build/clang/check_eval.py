"""隨機運算式:JS 追蹤器的結果 == 真的 g++ 算出的結果。"""
import random, subprocess, os, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "shared"))
from pwutil import stub_analytics
HERE=os.path.dirname(os.path.abspath(__file__)); PUB=os.path.join(os.path.dirname(os.path.dirname(HERE)),"public")
random.seed(7)
OPS=["+","-","*","/","%","<",">","<=",">=","==","!=","&&","||"]
def gen(d=0):
    if d>=3 or random.random()<0.3:
        return str(random.randint(0,9))
    r=random.random()
    if r<0.12: return "!"+gen(d+1) if random.random()<.5 else "- "+gen(d+1)
    a=gen(d+1); b=gen(d+1); e=a+" "+random.choice(OPS)+" "+b
    return "("+e+")" if random.random()<0.35 else e
fixed=["7 / 2","7 % 3","-7 / 2","-7 % 3","2 + 3 * 4","(2 + 3) * 4","10 - 2 - 3","5 > 3 && 2 > 4","1 < 2 < 3","3 > 2 > 1","!0 + 1","- -3","2 * -3","8 / 2 * 4","8 % 3 * 2","1 || 0 && 0","(1 || 0) && 0","!1 || 1","5 == 5 == 1"]
exprs=fixed+[gen() for _ in range(900)]
exprs=[e for e in dict.fromkeys(exprs)]
res=pw=None
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ.get("CHROME_PATH","/usr/bin/google-chrome"),args=["--no-sandbox"]); ctx=b.new_context(); stub_analytics(ctx); pg=ctx.new_page()
    pg.goto("file://"+PUB+"/clang/clang-operators-guide.html")
    js=pg.evaluate("es => es.map(e => { var r = window.CLANG_EVAL(e); return r.ok ? r.value : null; })",exprs)
    b.close()
ok=[(e,v) for e,v in zip(exprs,js) if v is not None]
src="#include <iostream>\nint main(){\n"+"".join('  std::cout << (%s) << "\\n";\n'%e for e,_ in ok)+"}\n"
open("/tmp/ev.cpp","w").write(src)
c=subprocess.run(["g++","-std=c++17","-w","/tmp/ev.cpp","-o","/tmp/ev"],capture_output=True,text=True)
if c.returncode: print(c.stderr[:800]); sys.exit(2)
out=subprocess.run(["/tmp/ev"],capture_output=True,text=True).stdout.split()
bad=[(e,v,o) for (e,v),o in zip(ok,out) if str(v)!=o]
print("expressions:",len(ok),"skipped(div0 etc):",len(exprs)-len(ok),"mismatch:",len(bad)); print(bad[:6]); sys.exit(1 if bad else 0)
