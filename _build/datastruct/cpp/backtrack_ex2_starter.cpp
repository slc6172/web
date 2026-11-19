#include <iostream>
#include <vector>

// 從 nums 裡挑出一些數字(每個位置最多挑一次,可以一個都不挑),
// 總和剛好等於 target 的挑法有幾種?(位置不同就算不同挑法。)
// 提示:回溯 —— 對每個位置,先「挑」遞迴下去,再「不挑」遞迴下去。
int countSubsets(const std::vector<int>& nums, int target) {
    (void)nums;
    (void)target;
    return -1;
}

int main() {
    std::cout << countSubsets({2, 3, 5, 7}, 10) << " " << countSubsets({1, 1, 1}, 2) << " " << countSubsets({4}, 3) << "\n";   // 預期輸出 2 3 0
}
