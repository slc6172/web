#include <algorithm>
#include <iostream>
#include <vector>

std::vector<int> buildPath(const std::vector<int>& prev, int target) {
    std::vector<int> path;
    for (int v = target; v != -1; v = prev[v]) {
        path.push_back(v);
    }
    std::reverse(path.begin(), path.end());
    return path;
}

int main() {
    std::vector<int> prev = {-1, 0, 0, 2, 3};
    for (int v : buildPath(prev, 4)) {
        std::cout << v << " ";
    }
    std::cout << "\n";
}
