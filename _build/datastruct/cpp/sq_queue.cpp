#include <iostream>
#include <vector>

struct Queue {
    std::vector<int> data;
    int head = 0;                            // 隊伍最前面在 data 的哪個位置

    void push(int x) {
        data.push_back(x);
    }

    int pop() {
        return data[head++];
    }

    bool empty() const {
        return head == static_cast<int>(data.size());
    }
};

int main() {
    Queue q;
    q.push(1);
    q.push(2);
    q.push(3);
    while (!q.empty()) {
        std::cout << q.pop() << " ";
    }
    std::cout << "\n";
}
