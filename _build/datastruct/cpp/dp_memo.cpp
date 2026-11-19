#include <iostream>
#include <vector>

long long calls = 0;

long long fibSlow(int n) {
    ++calls;
    if (n < 2) {
        return n;
    }
    return fibSlow(n - 1) + fibSlow(n - 2);
}

long long fibMemo(int n, std::vector<long long>& memo) {
    ++calls;
    if (n < 2) {
        return n;
    }
    if (memo[n] != -1) {
        return memo[n];
    }
    memo[n] = fibMemo(n - 1, memo) + fibMemo(n - 2, memo);
    return memo[n];
}

int main() {
    const int n = 30;
    calls = 0;
    long long a = fibSlow(n);
    std::cout << "沒有記憶:fib(" << n << ") = " << a << ",呼叫 " << calls << " 次\n";
    calls = 0;
    std::vector<long long> memo(n + 1, -1);
    long long b = fibMemo(n, memo);
    std::cout << "有記憶:  fib(" << n << ") = " << b << ",呼叫 " << calls << " 次\n";
}
