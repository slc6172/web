#include <iostream>
#include <unordered_set>
#include <vector>

// 回傳 v 裡有沒有「兩個不同位置的元素相加等於 target」。
// 第 2 篇的雙層迴圈寫法是 O(n²);用 unordered_set 記住「看過的數字」,可以做到 O(n)。
// 提示:對每個 x,看 target - x 是不是已經在 seen 裡。
bool hasPairSum(const std::vector<int>& v, int target) {
    std::unordered_set<int> seen;
    (void)v;
    (void)target;
    return false;
}

int main() {
    std::vector<int> v = {3, 8, 1, 9};
    std::cout << hasPairSum(v, 10) << " " << hasPairSum(v, 100) << "\n";   // 預期輸出 1 0
}
