#include <iostream>
#include <string>

bool isBalancedParen(const std::string& s) {
    int depth = 0;
    for (char c : s) {
        if (c == '(') {
            ++depth;
        } else if (c == ')') {
            --depth;
            if (depth < 0) {
                return false;
            }
        }
    }
    return depth == 0;
}

int main() {
    std::cout << isBalancedParen("(())") << isBalancedParen("(()") << isBalancedParen("())(") << "\n";
}
