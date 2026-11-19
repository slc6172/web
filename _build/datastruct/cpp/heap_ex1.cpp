#include <iostream>
#include <vector>

bool isMaxHeap(const std::vector<int>& h) {
    int n = static_cast<int>(h.size());
    for (int i = 0; i < n; ++i) {
        int left = 2 * i + 1;
        int right = 2 * i + 2;
        if (left < n && h[left] > h[i]) {
            return false;
        }
        if (right < n && h[right] > h[i]) {
            return false;
        }
    }
    return true;
}

int main() {
    std::cout << isMaxHeap({9, 5, 8, 1, 3, 2}) << isMaxHeap({9, 5, 8, 6, 3, 2}) << isMaxHeap({}) << isMaxHeap({4}) << "\n";
}
