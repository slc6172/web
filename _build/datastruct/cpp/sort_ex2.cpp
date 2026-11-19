#include <iostream>
#include <vector>

void insertionSort(std::vector<int>& v) {
    int n = static_cast<int>(v.size());
    for (int i = 1; i < n; ++i) {
        int key = v[i];
        int j = i - 1;
        while (j >= 0 && v[j] > key) {
            v[j + 1] = v[j];
            --j;
        }
        v[j + 1] = key;
    }
}

int main() {
    std::vector<int> v = {4, 3, 1, 2};
    insertionSort(v);
    for (int x : v) {
        std::cout << x << " ";
    }
    std::cout << "\n";
}
