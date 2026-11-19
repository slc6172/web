#include <iostream>
#include <vector>

// 把兩個「已排序」的 vector 合併成一個新的、也是已排序的 vector。
// 這就是合併排序裡 merge 的核心:兩個指標 i、j 各指著 a 和 b 的最前面,每次取較小的。
std::vector<int> mergeTwo(const std::vector<int>& a, const std::vector<int>& b) {
    std::vector<int> result;
    (void)a;
    (void)b;
    return result;
}

int main() {
    std::vector<int> r = mergeTwo({1, 4, 7}, {2, 3, 9, 10});
    for (int x : r) {
        std::cout << x << " ";
    }
    std::cout << "\n";                       // 預期輸出 1 2 3 4 7 9 10
}
