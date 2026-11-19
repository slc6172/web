#include <iostream>
#include <vector>

struct Stack {
    std::vector<int> data;

    void push(int x) {
        data.push_back(x);
    }

    int pop() {
        int x = data.back();
        data.pop_back();
        return x;
    }

    bool empty() const {
        return data.empty();
    }
};

int main() {
    Stack st;
    st.push(1);
    st.push(2);
    st.push(3);
    while (!st.empty()) {
        std::cout << st.pop() << " ";
    }
    std::cout << "\n";
}
