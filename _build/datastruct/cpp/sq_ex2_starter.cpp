#include <iostream>
#include <string>

// 只有一種括號 ( ) 時,不需要 stack,一個計數器就夠了。
// 遇到 ( 加 1,遇到 ) 減 1;中途變成負數,或最後不是 0,都不配對。
bool isBalancedParen(const std::string& s) {
    (void)s;
    return false;
}

int main() {
    std::cout << isBalancedParen("(())") << isBalancedParen("(()") << isBalancedParen("())(") << "\n";   // 預期輸出 100
}
