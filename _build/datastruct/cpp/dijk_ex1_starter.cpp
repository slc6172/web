#include <iostream>
#include <vector>

// prev[v] 是「走到 v 之前的那個點」,起點的 prev 是 -1。
// 請回傳從起點到 target 的路徑(由起點到 target 的順序)。
std::vector<int> buildPath(const std::vector<int>& prev, int target) {
    (void)prev;
    (void)target;
    return {};
}

int main() {
    std::vector<int> prev = {-1, 0, 0, 2, 3};   // 路:0 -> 2 -> 3 -> 4
    for (int v : buildPath(prev, 4)) {
        std::cout << v << " ";
    }
    std::cout << "\n";   // 預期輸出 0 2 3 4
}
