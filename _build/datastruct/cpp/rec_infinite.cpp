// 錯誤示範:少了基底條件。編譯器會警告,執行會一直往下呼叫直到當掉
int badFact(int n) {
    return n * badFact(n - 1);
}
