#include <iostream>
#include <vector>

int main() {
    auto pi = 3.14;                          // auto:讓編譯器推斷型別(這裡是 double)
    std::vector<int> v = {1, 2, 3};
    auto square = [](int n) { return n * n; };   // lambda:沒有名字的小函式
    for (auto& e : v) {                      // auto& 拿到本尊,改 e 就是改 v 裡的元素
        e = square(e);
    }
    for (int e : v) {
        std::cout << e << " ";
    }
    std::cout << pi << "\n";
}
