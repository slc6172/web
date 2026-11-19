#include <iostream>
#include <stack>
#include <string>

// 用 stack 把字串反過來:"abc" → "cba"
std::string reverseString(const std::string& s) {
    std::stack<char> st;
    // 1. 把每個字元 push 進去
    // 2. 一個個 pop 出來接成新字串
    (void)s;
    return "";
}

int main() {
    std::cout << reverseString("abc") << " " << reverseString("stack") << "\n";   // 預期輸出 cba kcats
}
