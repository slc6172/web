#include <iostream>
#include <stack>
#include <string>

std::string reverseString(const std::string& s) {
    std::stack<char> st;
    for (char c : s) {
        st.push(c);
    }
    std::string result;
    while (!st.empty()) {
        result += st.top();
        st.pop();
    }
    return result;
}

int main() {
    std::cout << reverseString("abc") << " " << reverseString("stack") << "\n";
}
