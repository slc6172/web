#include <iostream>

struct Node {
    int val;
    Node* next;
};

int main() {
    Node* p = nullptr;                       // 先明確寫成 nullptr:不指向任何東西
    if (p != nullptr) {
        std::cout << p->val << "\n";
    } else {
        std::cout << "p is null\n";          // 使用前先檢查,避免當掉
    }
}
