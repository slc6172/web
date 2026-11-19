#include <algorithm>
#include <iostream>
#include <vector>

const int INF = 1000000000;

int coinChange(const std::vector<int>& coins, int amount) {
    std::vector<int> dp(amount + 1, INF);
    dp[0] = 0;
    for (int a = 1; a <= amount; ++a) {
        for (int c : coins) {
            if (a >= c && dp[a - c] != INF) {
                dp[a] = std::min(dp[a], dp[a - c] + 1);
            }
        }
    }
    return dp[amount] == INF ? -1 : dp[amount];
}

int main() {
    std::cout << coinChange({1, 3, 4}, 6) << " " << coinChange({2}, 3) << " " << coinChange({1, 2, 5}, 11) << "\n";
}
