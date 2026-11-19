#include <algorithm>
#include <iostream>
#include <utility>
#include <vector>

// 一間會議室,每個活動是 (開始, 結束)。最多能安排幾個「時間不重疊」的活動?
// (一個活動的結束時間 == 下一個的開始時間,不算重疊。)
// 提示:貪婪 —— 依「結束時間」由小到大排序,能接上的就選(開始時間 >= 上一個選的結束時間)。
int maxActivities(std::vector<std::pair<int, int>> acts) {
    (void)acts;
    return 0;
}

int main() {
    std::cout << maxActivities({{1, 3}, {2, 4}, {3, 5}, {0, 6}, {5, 7}, {8, 9}, {5, 9}}) << "\n";   // 預期輸出 4
}
