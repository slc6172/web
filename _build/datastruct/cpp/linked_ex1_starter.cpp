#include <iostream>

struct Node {
    int val;
    Node* next;
};

// 回傳串列有幾個節點(從 head 一路走到 nullptr)
int length(const Node* head) {
    int count = 0;
    // 在這裡寫迴圈
    (void)head;
    return count;
}

int main() {
    Node c{3, nullptr};
    Node b{2, &c};
    Node a{1, &b};
    std::cout << length(&a) << " " << length(nullptr) << "\n";   // 預期輸出 3 0
}
