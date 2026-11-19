#include <iostream>

long long calls = 0;

int fib(int n) {
    ++calls;
    if (n <= 1) {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}

int main() {
    for (int n : {10, 20, 30}) {
        calls = 0;
        int result = fib(n);
        std::cout << "fib(" << n << ") = " << result << ", calls = " << calls << "\n";
    }
}
