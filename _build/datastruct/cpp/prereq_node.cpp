#include <iostream>

struct Node {
    int val;
    Node* next;
};

int main() {
    Node* a = new Node{1, nullptr};
    Node* b = new Node{2, nullptr};
    a->next = b;
    std::cout << a->next->val << "\n";
    delete b;
    delete a;
}
