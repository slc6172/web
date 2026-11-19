#include <iostream>
#include <queue>
#include <stack>

int main() {
    std::stack<int> st;
    st.push(1);
    st.push(2);
    st.push(3);
    std::cout << "stack top = " << st.top() << "\n";   // 只能看頂端
    st.pop();                                          // pop() 不回傳值
    std::cout << "stack top = " << st.top() << "\n";

    std::queue<int> q;
    q.push(1);
    q.push(2);
    q.push(3);
    std::cout << "queue front = " << q.front() << ", back = " << q.back() << "\n";
    q.pop();                                           // 移除最前面的
    std::cout << "queue front = " << q.front() << ", size = " << q.size() << "\n";
}
