#include <iostream>
#include <utility>
#include <vector>

// 在 bubbleSort 的內層迴圈裡,「該不該交換」的條件是什麼?補上它。
// 如果想改成由大到小排,條件要怎麼改?
void bubbleSort(std::vector<int>& v) {
    int n = static_cast<int>(v.size());
    for (int i = 0; i < n - 1; ++i) {
        for (int j = 0; j < n - 1 - i; ++j) {
            if (false) {                     // 把 false 改成正確的條件
                std::swap(v[j], v[j + 1]);
            }
        }
    }
}

int main() {
    std::vector<int> v = {4, 3, 1, 2};
    bubbleSort(v);
    for (int x : v) {
        std::cout << x << " ";
    }
    std::cout << "\n";                       // 預期輸出 1 2 3 4
}
