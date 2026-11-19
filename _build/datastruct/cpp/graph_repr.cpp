#include <iostream>
#include <utility>
#include <vector>

using Table = std::vector<std::vector<int>>;

void addEdge(Table& matrix, Table& adj, int a, int b) {
    matrix[a][b] = 1;
    matrix[b][a] = 1;
    adj[a].push_back(b);
    adj[b].push_back(a);
}

int main() {
    const int n = 5;
    std::vector<std::pair<int, int>> edges = {{0, 1}, {0, 2}, {1, 3}, {2, 3}, {3, 4}};
    Table matrix(n, std::vector<int>(n, 0));
    Table adj(n);
    for (const auto& e : edges) {
        addEdge(matrix, adj, e.first, e.second);
    }
    std::cout << "鄰接矩陣:\n";
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            std::cout << matrix[i][j] << " ";
        }
        std::cout << "\n";
    }
    std::cout << "鄰接表:\n";
    for (int i = 0; i < n; ++i) {
        std::cout << i << ":";
        for (int v : adj[i]) {
            std::cout << " " << v;
        }
        std::cout << "\n";
    }
    std::cout << "點 3 的度數: " << adj[3].size() << "\n";
}
