"""驗證首頁 format 試驗台的 JS 模擬 == 真的 g++ 輸出。"""
import subprocess, itertools, os, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "shared"))
from pwutil import stub_analytics
HERE=os.path.dirname(os.path.abspath(__file__)); PUB=os.path.join(os.path.dirname(os.path.dirname(HERE)),"public")
vals=["3.14159265","2.71828","1234.5678","0.000123456","100"]
src='''#include <iostream>
#include <iomanip>
#include <sstream>
using namespace std;
int main(){ double v[]={%s}; 
 for(double x: v) for(int p=0;p<=10;p++) for(int f=0;f<2;f++) for(int l=0;l<2;l++) for(int w: {0,6,12}){
  ostringstream os; if(f) os<<fixed; os<<setprecision(p); if(l) os<<left; os<<setw(w)<<x;
  cout<<setprecision(10)<<x<<"|"<<p<<"|"<<f<<"|"<<l<<"|"<<w<<"|"<<os.str()<<"\\n"; } }'''%",".join(vals)
open("/tmp/fmt.cpp","w").write(src)
subprocess.run(["g++","-std=c++17","/tmp/fmt.cpp","-o","/tmp/fmt"],check=True)
rows=[l.rstrip("\n").split("|") for l in subprocess.run(["/tmp/fmt"],capture_output=True,text=True).stdout.splitlines()]
bad=0
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ.get("CHROME_PATH","/usr/bin/google-chrome"),args=["--no-sandbox"]); ctx=b.new_context(); stub_analytics(ctx); pg=ctx.new_page()
    pg.goto("file://"+PUB+"/clang/clang-io-guide.html")
    res=pg.evaluate("rows => rows.map(r => window.CLANG_FMT(parseFloat(r[0]), +r[1], r[2]==='1', +r[4], r[3]==='1'))", rows)
    for r,g in zip(rows,res):
        if g!=r[5]:
            bad+=1
            if bad<8: print("MISMATCH",r,repr(g))
    b.close()
print("cases:",len(rows),"mismatch:",bad); sys.exit(1 if bad else 0)
