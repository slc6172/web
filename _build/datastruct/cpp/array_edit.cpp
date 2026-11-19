#include <iostream>
#include <vector>

void insertAt(std::vector<int>& v, int pos, int value) {
    v.push_back(0);                      // 先在尾端多開一格
    int last = static_cast<int>(v.size()) - 1;
    for (int i = last; i > pos; --i) {
        v[i] = v[i - 1];                 // 把前一格搬過來
    }
    v[pos] = value;                      // 空位放進新值
}

void eraseAt(std::vector<int>& v, int pos) {
    int n = static_cast<int>(v.size());
    for (int i = pos; i + 1 < n; ++i) {
        v[i] = v[i + 1];                 // 把後一格搬過來
    }
    v.pop_back();                        // 丟掉最後一格
}

void print(const std::vector<int>& v) {
    for (int x : v) {
        std::cout << x << " ";
    }
    std::cout << "\n";
}

int main() {
    std::vector<int> v = {10, 20, 30, 40, 50};
    insertAt(v, 2, 99);
    print(v);                            // 插在位置 2
    eraseAt(v, 0);
    print(v);                            // 刪掉最前面
    insertAt(v, static_cast<int>(v.size()), 7);
    print(v);                            // 插在尾端
}
