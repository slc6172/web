#include <iostream>

struct Node {
    int val;
    Node* next;
};

struct List {
    Node* head = nullptr;
};

void pushFront(List& list, int value) {
    Node* node = new Node{value, list.head};
    list.head = node;
}

void pushBack(List& list, int value) {
    Node* node = new Node{value, nullptr};
    if (list.head == nullptr) {
        list.head = node;
        return;
    }
    Node* cur = list.head;
    while (cur->next != nullptr) {
        cur = cur->next;
    }
    cur->next = node;
}

void insertAfter(Node* prev, int value) {
    Node* node = new Node{value, prev->next};
    prev->next = node;
}

void eraseFront(List& list) {
    Node* old = list.head;
    list.head = old->next;
    delete old;
}

void eraseAfter(Node* prev) {
    Node* old = prev->next;
    prev->next = old->next;
    delete old;
}

void print(const List& list) {
    for (Node* cur = list.head; cur != nullptr; cur = cur->next) {
        std::cout << cur->val << " -> ";
    }
    std::cout << "null\n";
}

void clear(List& list) {
    while (list.head != nullptr) {
        eraseFront(list);
    }
}

int main() {
    List list;
    pushFront(list, 20);
    pushFront(list, 10);
    pushBack(list, 40);
    insertAfter(list.head->next, 30);        // 插在 20 後面
    print(list);
    eraseFront(list);
    eraseAfter(list.head);                   // 刪掉 20 後面的 30
    print(list);
    clear(list);                             // 全部 delete,避免洩漏
}
