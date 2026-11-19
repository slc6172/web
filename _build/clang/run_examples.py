"""編譯並執行 examples/ 底下的每個 .cpp,把結果存到 examples/results.json。
命名:*.err.cpp = 預期編譯失敗(擷取第一個錯誤);其餘必須無警告地編譯成功並正常結束。
可選 <name>.in 提供 stdin。用法:python3 _build/run_examples.py [篇號前綴,如 p02]"""
import os, re, sys, json, subprocess, tempfile, pty, select, termios, time
HERE = os.path.dirname(os.path.abspath(__file__))
EX = os.path.join(HERE, "examples")
FLAGS = ["g++", "-std=c++17", "-Wall", "-Wextra"]
DIAG = re.compile(r"^\S+:\d+:\d+: (error|warning|note|fatal error)")

def first_error(stderr, src):
    lines = stderr.replace(src, "main.cpp").splitlines()
    e = next((i for i, l in enumerate(lines) if re.search(r"(error|fatal error):", l)), None)
    if e is None: return ""
    start = e - 1 if e > 0 and lines[e - 1].startswith("main.cpp: In") else e
    out = lines[start:e + 1]
    for l in lines[e + 1:]:
        if l.startswith("In file included"): break
        m = DIAG.match(l)
        if m:
            if m.group(1) == "note" and "did you forget" in l: out.append(l); continue   # 這種提示對新手很有用
            break
        out.append(l)
    return "\n".join(out[:14]).rstrip()

def run_session(exe, stdin_text, limit=8, cwd=None):
    """用偽終端機執行:程式停下來等輸入時,才送出下一行,並把『輸出』與『你打的字』依序記成 parts。"""
    lines = stdin_text.splitlines(keepends=True)
    pid, fd = pty.fork()
    if pid == 0:
        if cwd: os.chdir(cwd)
        os.execv(exe, [exe])
    attr = termios.tcgetattr(fd); attr[3] &= ~termios.ECHO; termios.tcsetattr(fd, termios.TCSANOW, attr)
    parts, chunk, t0, code, eof = [], b"", time.time(), None, False
    def flush():
        nonlocal chunk
        if chunk: parts.append(["o", chunk.decode("utf-8", "replace").replace("\r\n", "\n")]); chunk = b""
    while time.time() - t0 < limit:
        r, _, _ = select.select([fd], [], [], 0.35)
        if r:
            try: data = os.read(fd, 4096)
            except OSError: break
            if not data: break
            chunk += data
            continue
        done, st = os.waitpid(pid, os.WNOHANG)
        if done: code = os.waitstatus_to_exitcode(st); break
        flush()
        if lines:
            l = lines.pop(0); os.write(fd, l.encode()); parts.append(["i", l])
        elif not eof:
            os.write(fd, b"\x04"); eof = True   # 輸入用完了,送出 Ctrl+D(輸入結束),讓 while (cin >> x) 這類迴圈可以結束
        else:
            break
    flush()
    if code is None:
        for _ in range(30):
            try: done, st = os.waitpid(pid, os.WNOHANG)
            except ChildProcessError: return parts, 0
            if done: return parts, os.waitstatus_to_exitcode(st)
            time.sleep(0.1)
        os.kill(pid, 9); os.waitpid(pid, 0); return parts, None
    return parts, code

def main(prefix=""):
    path = os.path.join(EX, "results.json")
    res = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
    problems = []
    for root, _, files in sorted(os.walk(EX)):
        for f in sorted(files):
            if not f.endswith(".cpp"): continue
            src = os.path.join(root, f)
            id_ = os.path.relpath(src, EX)[:-4]
            if prefix and not id_.startswith(prefix): continue
            expect_fail = ".err" in f
            m_exit = re.search(r"\.exit(\d+)", f); want = int(m_exit.group(1)) if m_exit else 0   # 預期的結束碼
            with tempfile.TemporaryDirectory() as td:
                exe = os.path.join(td, "a.out")
                c = subprocess.run(FLAGS + [src, "-o", exe], capture_output=True, text=True)
                if expect_fail:
                    if c.returncode == 0: problems.append(id_ + ": 預期編譯失敗但成功了"); continue
                    res[id_] = {"ok": False, "err": first_error(c.stderr, src)}
                    continue
                if c.returncode != 0 or c.stderr.strip():
                    problems.append(id_ + ": 編譯失敗或有警告\n" + c.stderr[:600]); continue
                if ".crash" in f:   # 預期執行時異常中止:記錄 stdout 與 stderr 的前幾行
                    r = subprocess.run([exe], capture_output=True, text=True, timeout=5, cwd=td)
                    if r.returncode == 0: problems.append(id_ + ": 預期執行時當掉,但正常結束了"); continue
                    res[id_] = {"ok": False, "crash": True, "out": r.stdout, "err": "\n".join(r.stderr.strip().splitlines()[:3])}
                    continue
                if ".norun" in f:   # 只確認能編譯(例如結果每次不同的程式)
                    res[id_] = {"ok": True, "out": "", "norun": True}; continue
                inp = os.path.splitext(src)[0] + ".in"
                stdin = open(inp, encoding="utf-8").read() if os.path.exists(inp) else ""
                if stdin:
                    parts, code = run_session(exe, stdin, cwd=td)
                    if code != want: problems.append(id_ + ": 結束碼 %s(或逾時)" % code); continue
                    res[id_] = {"ok": True, "out": "".join(t for _, t in parts), "parts": parts, "stdin": stdin}
                    continue
                try:
                    r = subprocess.run([exe], capture_output=True, text=True, timeout=5, cwd=td)
                except subprocess.TimeoutExpired:
                    problems.append(id_ + ": 執行逾時"); continue
                if r.returncode != want: problems.append(id_ + ": 結束碼 %d" % r.returncode); continue
                res[id_] = {"ok": True, "out": r.stdout, "stdin": ""}
    json.dump(res, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    print("examples:", len(res), "problems:", len(problems))
    for p in problems: print(" ✗", p)
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
