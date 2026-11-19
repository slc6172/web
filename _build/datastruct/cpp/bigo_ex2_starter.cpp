#include <iostream>
#include <vector>

// 回傳 v 裡有沒有「兩個不同位置的元素相加等於 target」。
// 先用最直覺的寫法完成它,再回答:時間是 O(?)
bool hasPairSum(const std::vector<int>& v, int target) {
    (void)v;
    (void)target;
    return false;
}

int main() {
    std::vector<int> v = {3, 8, 1, 9};
    std::cout << hasPairSum(v, 10) << " " << hasPairSum(v, 100) << "\n";   // 預期輸出 1 0
}
