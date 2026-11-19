#include <iostream>

// 回傳 base 的 exp 次方(exp 是 0 或正整數)。用遞迴寫:
// base^exp = base * base^(exp - 1),而 base^0 = 1
int power(int base, int exp) {
    (void)base;
    (void)exp;
    return 0;
}

int main() {
    std::cout << power(2, 3) << " " << power(5, 0) << "\n";   // 預期輸出 8 1
}
