#include <iostream>
#include <vector>

int go(const std::vector<int>& nums, int idx, int remain) {
    if (idx == static_cast<int>(nums.size())) {
        return remain == 0 ? 1 : 0;
    }
    int take = go(nums, idx + 1, remain - nums[idx]);
    int skip = go(nums, idx + 1, remain);
    return take + skip;
}

int countSubsets(const std::vector<int>& nums, int target) {
    return go(nums, 0, target);
}

int main() {
    std::cout << countSubsets({2, 3, 5, 7}, 10) << " " << countSubsets({1, 1, 1}, 2) << " " << countSubsets({4}, 3) << "\n";
}
