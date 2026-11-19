#include <iostream>
#include <utility>
#include <vector>

void bubbleSort(std::vector<int>& v) {
    int n = static_cast<int>(v.size());
    for (int i = 0; i < n - 1; ++i) {
        for (int j = 0; j < n - 1 - i; ++j) {
            if (v[j] > v[j + 1]) {
                std::swap(v[j], v[j + 1]);
            }
        }
    }
}

int main() {
    std::vector<int> v = {4, 3, 1, 2};
    bubbleSort(v);
    for (int x : v) {
        std::cout << x << " ";
    }
    std::cout << "\n";
}
