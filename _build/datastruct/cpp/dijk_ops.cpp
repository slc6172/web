#include <functional>
#include <iostream>
#include <queue>
#include <utility>
#include <vector>

struct Edge {
    int to;
    int w;
};

using Graph = std::vector<std::vector<Edge>>;
using Item = std::pair<int, int>;
const int INF = 1000000000;

void dijkstra(const Graph& g, int src, std::vector<int>& dist, std::vector<int>& prev) {
    dist.assign(g.size(), INF);
    prev.assign(g.size(), -1);
    std::priority_queue<Item, std::vector<Item>, std::greater<Item>> pq;
    dist[src] = 0;
    pq.push({0, src});
    while (!pq.empty()) {
        Item top = pq.top();
        pq.pop();
        int d = top.first;
        int u = top.second;
        if (d > dist[u]) {
            continue;
        }
        for (const Edge& e : g[u]) {
            if (d + e.w < dist[e.to]) {
                dist[e.to] = d + e.w;
                prev[e.to] = u;
                pq.push({dist[e.to], e.to});
            }
        }
    }
}

void addEdge(Graph& g, int a, int b, int w) {
    g[a].push_back({b, w});
    g[b].push_back({a, w});
}

void report(const Graph& g, int src, int target) {
    std::vector<int> dist;
    std::vector<int> prev;
    dijkstra(g, src, dist, prev);
    std::cout << "dist:";
    for (int d : dist) {
        std::cout << " " << d;
    }
    std::cout << "\n";
    std::vector<int> path;
    for (int v = target; v != -1; v = prev[v]) {
        path.push_back(v);
    }
    std::cout << "到 " << target << " 的路(" << dist[target] << "):";
    for (int i = static_cast<int>(path.size()) - 1; i >= 0; --i) {
        std::cout << " " << path[i];
    }
    std::cout << "\n";
}

int main() {
    Graph a(6);
    addEdge(a, 0, 1, 7);
    addEdge(a, 0, 2, 9);
    addEdge(a, 0, 5, 14);
    addEdge(a, 1, 2, 10);
    addEdge(a, 1, 3, 15);
    addEdge(a, 2, 3, 11);
    addEdge(a, 2, 5, 2);
    addEdge(a, 3, 4, 6);
    addEdge(a, 4, 5, 9);
    report(a, 0, 4);
    Graph b(5);
    addEdge(b, 0, 1, 10);
    addEdge(b, 0, 2, 3);
    addEdge(b, 2, 1, 4);
    addEdge(b, 1, 3, 2);
    addEdge(b, 2, 3, 8);
    addEdge(b, 3, 4, 7);
    report(b, 0, 4);
}
