#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

std::string mostCommon(const std::vector<std::string>& words) {
    std::unordered_map<std::string, int> count;
    for (const std::string& w : words) {
        ++count[w];
    }
    std::string best;
    int bestCount = 0;
    for (const auto& entry : count) {
        if (entry.second > bestCount) {
            bestCount = entry.second;
            best = entry.first;
        }
    }
    return best;
}

int main() {
    std::vector<std::string> w = {"cat", "dog", "cat", "bird", "dog", "cat"};
    std::cout << mostCommon(w) << "\n";
}
