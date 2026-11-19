#include <iostream>
#include <stack>
#include <string>

bool matches(char open, char close) {
    return (open == '(' && close == ')') ||
           (open == '[' && close == ']') ||
           (open == '{' && close == '}');
}

bool isBalanced(const std::string& s) {
    std::stack<char> st;
    for (char c : s) {
        if (c == '(' || c == '[' || c == '{') {
            st.push(c);
        } else if (c == ')' || c == ']' || c == '}') {
            if (st.empty()) {
                return false;
            }
            char open = st.top();
            st.pop();
            if (!matches(open, c)) {
                return false;
            }
        }
    }
    return st.empty();
}

int main() {
    const char* tests[] = {"{[()]}", "([)]", "((())", "())", "a(b)c"};
    for (const char* t : tests) {
        std::cout << t << " -> " << (isBalanced(t) ? "balanced" : "not balanced") << "\n";
    }
}
