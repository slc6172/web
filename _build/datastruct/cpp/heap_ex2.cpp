#include <functional>
#include <iostream>
#include <queue>
#include <vector>

int kthLargest(const std::vector<int>& nums, int k) {
    std::priority_queue<int, std::vector<int>, std::greater<int>> minHeap;
    for (int x : nums) {
        minHeap.push(x);
        if (static_cast<int>(minHeap.size()) > k) {
            minHeap.pop();
        }
    }
    return minHeap.top();
}

int main() {
    std::cout << kthLargest({3, 2, 1, 5, 6, 4}, 2) << " " << kthLargest({3, 2, 3, 1, 2, 4, 5, 5, 6}, 4) << "\n";
}
