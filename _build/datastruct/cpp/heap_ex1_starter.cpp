#include <iostream>
#include <vector>

// 判斷 h 是不是「最大堆積」:每個節點都 >= 它的左右子節點。
// 提示:位置 i 的左子是 2*i+1,右子是 2*i+2,要先檢查有沒有超出範圍。
bool isMaxHeap(const std::vector<int>& h) {
    (void)h;
    return false;
}

int main() {
    std::cout << isMaxHeap({9, 5, 8, 1, 3, 2}) << isMaxHeap({9, 5, 8, 6, 3, 2}) << isMaxHeap({}) << isMaxHeap({4}) << "\n";   // 預期輸出 1011
}
