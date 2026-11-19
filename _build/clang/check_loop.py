"""迴圈追蹤表的 JS 模擬 == 真的 g++ 迴圈。"""
import random, subprocess, os, sys, itertools
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "shared"))
from pwutil import stub_analytics
HERE=os.path.dirname(os.path.abspath(__file__)); PUB=os.path.join(os.path.dirname(os.path.dirname(HERE)),"public")
random.seed(3)
cases=[(s,e,t,o) for s in range(-6,7,2) for e in range(-6,7,3) for t in (-3,-1,0,1,2) for o in ("<","<=",">",">=")]
cases+= [(random.randint(-99,99),random.randint(-99,99),random.randint(-5,5),random.choice(["<","<=",">",">="])) for _ in range(300)]
body="".join('  {long long sum=0; int i=%d, count=0; while (i %s %d) { sum+=i; i+=%d; if(++count>300) break; } std::cout<<count<<" "<<sum<<"\\n";}\n'%(s,o,e,t) for s,e,t,o in cases)
open("/tmp/lp.cpp","w").write("#include <iostream>\nint main(){\n"+body+"}\n")
subprocess.run(["g++","-std=c++17","-w","/tmp/lp.cpp","-o","/tmp/lp"],check=True)
real=[tuple(map(int,l.split())) for l in subprocess.run(["/tmp/lp"],capture_output=True,text=True).stdout.splitlines()]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ.get("CHROME_PATH","/usr/bin/google-chrome"),args=["--no-sandbox"]); ctx=b.new_context(); stub_analytics(ctx); pg=ctx.new_page()
    pg.goto("file://"+PUB+"/clang/clang-loops-guide.html")
    js=pg.evaluate("cs => cs.map(c => { var r = window.CLANG_LOOP(c[0],c[1],c[2],c[3]); return [r.inf ? 301 : r.count, r.inf ? r.rows.reduce((a,x)=>a+x.i,0) : r.sum]; })",[list(c) for c in cases])
    b.close()
bad=[(c,j,r) for c,j,r in zip(cases,js,real) if tuple(j)!=r]
print("cases:",len(cases),"mismatch:",len(bad)); print(bad[:5]); sys.exit(1 if bad else 0)
