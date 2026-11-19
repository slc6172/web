#include <iostream>
#include <vector>

const int INF = 1000000000;

// 用最少的硬幣湊出 amount;湊不出來回傳 -1。每種硬幣可以用無限多枚。
// 提示:dp[a] = 湊出金額 a 最少要幾枚;dp[a] = min(dp[a - c] + 1),對每種硬幣 c(a >= c 且 dp[a - c] 不是 INF)。
int coinChange(const std::vector<int>& coins, int amount) {
    (void)coins;
    (void)amount;
    return -2;
}

int main() {
    std::cout << coinChange({1, 3, 4}, 6) << " " << coinChange({2}, 3) << " " << coinChange({1, 2, 5}, 11) << "\n";   // 預期輸出 2 -1 3
}
