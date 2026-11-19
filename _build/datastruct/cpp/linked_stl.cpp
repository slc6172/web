#include <iostream>
#include <list>

int main() {
    std::list<int> lst = {10, 20, 40};       // 雙向鏈結串列
    lst.push_front(5);                       // 頭插,O(1)
    lst.push_back(50);                       // 尾插,O(1)
    auto it = lst.begin();
    ++it;                                    // 往後走一個節點
    lst.insert(it, 15);                      // 插在 it 前面,O(1)
    lst.erase(lst.begin());                  // 刪掉第一個,O(1)
    for (int x : lst) {
        std::cout << x << " ";
    }
    std::cout << "\n";
}
