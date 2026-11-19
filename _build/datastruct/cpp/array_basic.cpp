#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {10, 20, 30};   // 建立,一開始有 3 個元素
    v.push_back(40);                     // 在尾端加一個
    std::cout << "size = " << v.size() << "\n";
    std::cout << "v[0] = " << v[0] << "\n";

    int total = 0;
    for (int i = 0; i < static_cast<int>(v.size()); ++i) {
        total += v[i];                   // 用索引逐一讀取
    }
    std::cout << "total = " << total << "\n";

    for (int x : v) {                    // range-for:不需要索引時更簡潔
        std::cout << x << " ";
    }
    std::cout << "\n";
}
