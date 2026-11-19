#include <iostream>
#include <vector>

int lowerBound(const std::vector<int>& v, int target) {
    int lo = 0;
    int hi = static_cast<int>(v.size());
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (v[mid] < target) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return lo;
}

int main() {
    std::vector<int> v = {1, 3, 3, 5, 8};
    std::cout << lowerBound(v, 3) << " " << lowerBound(v, 4) << " " << lowerBound(v, 9) << " " << lowerBound(v, 0) << "\n";
}
