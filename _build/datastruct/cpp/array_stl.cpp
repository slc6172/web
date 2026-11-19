#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {10, 20, 30, 40, 50};
    v.insert(v.begin() + 2, 99);         // 在位置 2 插入 99
    v.erase(v.begin());                  // 刪掉位置 0
    for (int x : v) {
        std::cout << x << " ";
    }
    std::cout << "\n";
}
