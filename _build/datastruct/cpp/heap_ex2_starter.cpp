#include <functional>
#include <iostream>
#include <queue>
#include <vector>

// 回傳 nums 裡「第 k 大」的值(k 從 1 開始,保證 1 <= k <= nums.size())。
// 提示:用一個「最小堆積」只留下目前最大的 k 個數;堆積超過 k 個就 pop 掉最小的。
int kthLargest(const std::vector<int>& nums, int k) {
    (void)nums;
    (void)k;
    return 0;
}

int main() {
    std::cout << kthLargest({3, 2, 1, 5, 6, 4}, 2) << " " << kthLargest({3, 2, 3, 1, 2, 4, 5, 5, 6}, 4) << "\n";   // 預期輸出 5 4
}
