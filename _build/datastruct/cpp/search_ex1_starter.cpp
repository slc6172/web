#include <iostream>
#include <vector>

int binarySearch(const std::vector<int>& v, int target) {
    int lo = 0;
    int hi = static_cast<int>(v.size()) - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (v[mid] == target) {
            return mid;
        } else if (v[mid] < target) {
            lo = mid + 1;
        } else {
            // 目標在左半邊:在這裡補一行,縮小範圍
            // (如果執行後卡住不動,就是少了這一行,按 Ctrl+C 結束)
        }
    }
    return -1;
}

int main() {
    std::vector<int> v = {2, 5, 8, 12, 16, 23, 38, 56, 72, 91};
    std::cout << binarySearch(v, 23) << " " << binarySearch(v, 7) << "\n";   // 預期輸出 5 -1
}
