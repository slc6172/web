#include <iostream>

struct Node {
    int val;
    Node* next;
};

Node* findNode(Node* head, int target) {
    for (Node* cur = head; cur != nullptr; cur = cur->next) {
        if (cur->val == target) {
            return cur;
        }
    }
    return nullptr;
}

int main() {
    Node c{30, nullptr};
    Node b{20, &c};
    Node a{10, &b};
    Node* p = findNode(&a, 20);
    std::cout << (p != nullptr ? p->val : -1) << " ";
    p = findNode(&a, 99);
    std::cout << (p != nullptr ? p->val : -1) << "\n";
}
