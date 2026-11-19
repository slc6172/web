#include <iostream>
#include <vector>

// 爬樓梯變化:一次可以爬 1、2 或 3 階,爬到第 n 階有幾種方法?(n >= 0)
// 提示:dp[i] = dp[i-1] + dp[i-2] + dp[i-3];要小心 i < 3 時不能讀到負的位置。
long long ways(int n) {
    (void)n;
    return 0;
}

int main() {
    std::cout << ways(4) << " " << ways(5) << " " << ways(0) << "\n";   // 預期輸出 7 13 1
}
