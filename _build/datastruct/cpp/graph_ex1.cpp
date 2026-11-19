#include <iostream>
#include <vector>

int maxDegreeNode(const std::vector<std::vector<int>>& adj) {
    int best = -1;
    for (int i = 0; i < static_cast<int>(adj.size()); ++i) {
        if (best == -1 || adj[i].size() > adj[best].size()) {
            best = i;
        }
    }
    return best;
}

int main() {
    std::vector<std::vector<int>> adj = {{1, 2}, {0, 2, 3}, {0, 1, 3}, {1, 2, 4}, {3}};
    std::cout << maxDegreeNode(adj) << "\n";
}
