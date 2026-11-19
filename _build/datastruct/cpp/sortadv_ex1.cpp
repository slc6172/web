#include <iostream>
#include <vector>

std::vector<int> mergeTwo(const std::vector<int>& a, const std::vector<int>& b) {
    std::vector<int> result;
    int na = static_cast<int>(a.size());
    int nb = static_cast<int>(b.size());
    int i = 0;
    int j = 0;
    while (i < na && j < nb) {
        if (a[i] <= b[j]) {
            result.push_back(a[i++]);
        } else {
            result.push_back(b[j++]);
        }
    }
    while (i < na) {
        result.push_back(a[i++]);
    }
    while (j < nb) {
        result.push_back(b[j++]);
    }
    return result;
}

int main() {
    std::vector<int> r = mergeTwo({1, 4, 7}, {2, 3, 9, 10});
    for (int x : r) {
        std::cout << x << " ";
    }
    std::cout << "\n";
}
