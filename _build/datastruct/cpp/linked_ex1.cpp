#include <iostream>

struct Node {
    int val;
    Node* next;
};

int length(const Node* head) {
    int count = 0;
    for (const Node* cur = head; cur != nullptr; cur = cur->next) {
        ++count;
    }
    return count;
}

int main() {
    Node c{3, nullptr};
    Node b{2, &c};
    Node a{1, &b};
    std::cout << length(&a) << " " << length(nullptr) << "\n";
}
