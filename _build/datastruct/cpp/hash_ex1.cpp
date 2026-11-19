#include <iostream>
#include <unordered_set>
#include <vector>

bool hasPairSum(const std::vector<int>& v, int target) {
    std::unordered_set<int> seen;
    for (int x : v) {
        if (seen.count(target - x) > 0) {
            return true;
        }
        seen.insert(x);
    }
    return false;
}

int main() {
    std::vector<int> v = {3, 8, 1, 9};
    std::cout << hasPairSum(v, 10) << " " << hasPairSum(v, 100) << "\n";
}
