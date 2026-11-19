#include <iostream>

struct Node {
    int val;
    Node* next;
};

// 在 list 的某個節點 prev 後面插入 value 之前,要先找到 prev。
// 回傳第一個 val 等於 target 的節點指標;找不到回傳 nullptr。
Node* findNode(Node* head, int target) {
    (void)head;
    (void)target;
    return nullptr;
}

int main() {
    Node c{30, nullptr};
    Node b{20, &c};
    Node a{10, &b};
    Node* p = findNode(&a, 20);
    std::cout << (p != nullptr ? p->val : -1) << " ";
    p = findNode(&a, 99);
    std::cout << (p != nullptr ? p->val : -1) << "\n";                // 預期輸出 20 -1
}
