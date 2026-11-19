#include <iostream>
#include <vector>

// 鄰接表 adj 裡,「度數最大」的點是哪一個?(度數 = 相鄰的點數;有多個時回傳編號最小的)
int maxDegreeNode(const std::vector<std::vector<int>>& adj) {
    (void)adj;
    return -1;
}

int main() {
    std::vector<std::vector<int>> adj = {{1, 2}, {0, 2, 3}, {0, 1, 3}, {1, 2, 4}, {3}};
    std::cout << maxDegreeNode(adj) << "\n";   // 預期輸出 1
}
