#include <iostream>
#include <vector>

int search(const std::vector<int>& v, int target, int lo, int hi) {
    if (lo > hi) {
        return -1;                           // 基底條件 1:範圍空了
    }
    int mid = lo + (hi - lo) / 2;
    if (v[mid] == target) {
        return mid;                          // 基底條件 2:找到了
    }
    if (v[mid] < target) {
        return search(v, target, mid + 1, hi);   // 只剩右半邊
    }
    return search(v, target, lo, mid - 1);       // 只剩左半邊
}

int main() {
    std::vector<int> v = {2, 5, 8, 12, 16, 23, 38, 56, 72, 91};
    int n = static_cast<int>(v.size());
    std::cout << search(v, 23, 0, n - 1) << " " << search(v, 7, 0, n - 1) << "\n";
}
