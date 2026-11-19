#include <iostream>
#include <queue>
#include <vector>

// 用 BFS 判斷點 a 和點 b 之間有沒有路(連不連通)。adj 是鄰接表。
bool connected(const std::vector<std::vector<int>>& adj, int a, int b) {
    (void)adj;
    (void)a;
    (void)b;
    return false;
}

int main() {
    std::vector<std::vector<int>> adj = {{1}, {0, 2}, {1}, {4}, {3}};   // 0-1-2 一組,3-4 一組
    std::cout << connected(adj, 0, 2) << connected(adj, 0, 4) << connected(adj, 3, 4) << "\n";   // 預期輸出 101
}
