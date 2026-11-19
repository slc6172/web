// 錯誤示範:這份程式可以編譯,但執行會出問題,所以本站不執行它
struct Node {
    int val;
    Node* next;
};

void insertAfterWrong(Node* prev, int value) {
    Node* node = new Node{value, nullptr};
    prev->next = node;                       // 先改了 prev->next ...
    node->next = prev->next;                 // ... 這時 prev->next 已經是 node 自己了!
}
