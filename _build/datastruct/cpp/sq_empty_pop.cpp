#include <iostream>
#include <stack>

int main() {
    std::stack<int> st;
    if (!st.empty()) {                       // 先檢查,再 top() / pop()
        std::cout << st.top() << "\n";
        st.pop();
    } else {
        std::cout << "stack is empty\n";
    }
}
