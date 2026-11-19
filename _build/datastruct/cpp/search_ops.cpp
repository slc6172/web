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
    std::vector<int> v = {2, 5, 8, 12, 16, 23, 38, 56, 72, 91};
    std::cout << linearSearch(v, 23) << " " << binarySearch(v, 23) << "\n";
    std::cout << linearSearch(v, 7) << " " << binarySearch(v, 7) << "\n";
}
