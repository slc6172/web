#include <iostream>
#include <queue>
#include <vector>

bool connected(const std::vector<std::vector<int>>& adj, int a, int b) {
    std::vector<bool> seen(adj.size(), false);
    std::queue<int> q;
    seen[a] = true;
    q.push(a);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        if (u == b) {
            return true;
        }
        for (int v : adj[u]) {
            if (!seen[v]) {
                seen[v] = true;
                q.push(v);
            }
        }
    }
    return false;
}

int main() {
    std::vector<std::vector<int>> adj = {{1}, {0, 2}, {1}, {4}, {3}};
    std::cout << connected(adj, 0, 2) << connected(adj, 0, 4) << connected(adj, 3, 4) << "\n";
}
