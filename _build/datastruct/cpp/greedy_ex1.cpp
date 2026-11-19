#include <algorithm>
#include <iostream>
#include <utility>
#include <vector>

int maxActivities(std::vector<std::pair<int, int>> acts) {
    std::sort(acts.begin(), acts.end(), [](const std::pair<int, int>& a, const std::pair<int, int>& b) {
        return a.second < b.second;
    });
    int count = 0;
    int lastEnd = -1;
    for (const auto& a : acts) {
        if (a.first >= lastEnd) {
            ++count;
            lastEnd = a.second;
        }
    }
    return count;
}

int main() {
    std::cout << maxActivities({{1, 3}, {2, 4}, {3, 5}, {0, 6}, {5, 7}, {8, 9}, {5, 9}}) << "\n";
}
