#include <functional>
#include <iostream>
#include <queue>
#include <vector>

int main() {
    std::priority_queue<int> maxHeap;                  // 預設:最大的在最上面
    for (int v : {5, 3, 8, 1, 9, 2}) {
        maxHeap.push(v);
    }
    std::cout << maxHeap.top() << " size=" << maxHeap.size() << "\n";
    while (!maxHeap.empty()) {
        std::cout << maxHeap.top() << " ";
        maxHeap.pop();
    }
    std::cout << "\n";

    std::priority_queue<int, std::vector<int>, std::greater<int>> minHeap;   // 最小的在最上面
    for (int v : {5, 3, 8, 1, 9, 2}) {
        minHeap.push(v);
    }
    while (!minHeap.empty()) {
        std::cout << minHeap.top() << " ";
        minHeap.pop();
    }
    std::cout << "\n";
}
