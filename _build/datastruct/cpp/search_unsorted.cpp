#include <iostream>
#include <vector>

int linearSearch(const std::vector<int>& v, int target) {
    for (int i = 0; i < static_cast<int>(v.size()); ++i) {
        if (v[i] == target) {
            return i;
        }
    }
    return -1;
}

int binarySearch(const std::vector<int>& v, int target) {
    int lo = 0;
    int hi = static_cast<int>(v.size()) - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (v[mid] == target) {
            return mid;
        } else if (v[mid] < target) {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    return -1;
}

int main() {
    std::vector<int> v = {5, 2, 9, 1, 7};    // 沒有排序!
    std::cout << binarySearch(v, 1) << " " << linearSearch(v, 1) << "\n";
}
