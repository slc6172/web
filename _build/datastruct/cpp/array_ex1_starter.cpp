#include <iostream>
#include <vector>

int sum(const std::vector<int>& v) {
    int total = 0;
    for (int x : v) {
        // 在這裡加一行,把 x 加進 total
    }
    return total;
}

int main() {
    std::vector<int> v = {3, 1, 4, 1, 5};
    std::cout << sum(v) << "\n";         // 預期輸出 14
}
