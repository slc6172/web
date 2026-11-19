#include <iostream>
#include <vector>

bool hasPairSum(const std::vector<int>& v, int target) {
    int n = static_cast<int>(v.size());
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (v[i] + v[j] == target) {
                return true;
            }
        }
    }
    return false;
}

int main() {
    std::vector<int> v = {3, 8, 1, 9};
    std::cout << hasPairSum(v, 10) << " " << hasPairSum(v, 100) << "\n";
}
