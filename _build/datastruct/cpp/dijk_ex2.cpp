#include <iostream>
#include <vector>

const int INF = 1000000000;

bool relax(std::vector<int>& dist, int du, int v, int w) {
    if (du + w < dist[v]) {
        dist[v] = du + w;
        return true;
    }
    return false;
}

int main() {
    std::vector<int> dist = {0, INF, 9};
    std::cout << relax(dist, 0, 1, 7) << " " << dist[1] << " " << relax(dist, 7, 2, 5) << " " << dist[2] << " " << relax(dist, 7, 2, 2) << " " << dist[2] << "\n";
}
