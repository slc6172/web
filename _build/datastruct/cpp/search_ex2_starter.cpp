#include <iostream>
#include <vector>

// 在「已排序」的 v 裡,回傳第一個「大於等於 target」的元素的索引;
// 如果每個元素都比 target 小,回傳 v.size()。
int lowerBound(const std::vector<int>& v, int target) {
    int lo = 0;
    int hi = static_cast<int>(v.size());     // 答案可能是 size(),所以 hi 從 size 開始
    // 提示:用 while (lo < hi),mid 的值如果小於 target,答案在右邊;否則 mid 本身也可能是答案
    (void)v;
    (void)target;
    return lo + hi - hi;
}

int main() {
    std::vector<int> v = {1, 3, 3, 5, 8};
    std::cout << lowerBound(v, 3) << " " << lowerBound(v, 4) << " " << lowerBound(v, 9) << " " << lowerBound(v, 0) << "\n";   // 預期輸出 1 3 5 0
}
