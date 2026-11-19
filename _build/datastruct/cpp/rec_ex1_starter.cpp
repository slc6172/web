#include <iostream>

// 回傳 1 + 2 + ... + n
int sumTo(int n) {
    // 在這裡補上基底條件:n 是 0 的時候,總和是多少?
    return n + sumTo(n - 1);
}

int main() {
    std::cout << sumTo(5) << " " << sumTo(0) << "\n";   // 預期輸出 15 0
}
