#include <iostream>
#include <vector>

int countGreater(const std::vector<int>& v, int x) {
    // 回傳 v 裡「大於 x」的元素有幾個
    return 0;
}

int main() {
    std::vector<int> v = {3, 1, 4, 1, 5, 9, 2, 6};
    std::cout << countGreater(v, 3) << "\n";   // 預期輸出 4
    std::cout << countGreater(v, 9) << "\n";   // 預期輸出 0
}
