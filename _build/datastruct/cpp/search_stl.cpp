#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {2, 5, 8, 12, 16, 23, 38, 56, 72, 91};
    auto it = std::find(v.begin(), v.end(), 23);                       // 線性搜尋
    std::cout << (it != v.end() ? it - v.begin() : -1) << "\n";
    std::cout << std::binary_search(v.begin(), v.end(), 23) << "\n";   // 二分搜尋:有沒有
    auto lb = std::lower_bound(v.begin(), v.end(), 20);                // 第一個 >= 20 的位置
    std::cout << lb - v.begin() << " " << *lb << "\n";
}
