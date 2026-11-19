#include <algorithm>
#include <iostream>
#include <vector>

long long fib(int n) {
    std::vector<long long> dp(n + 2);
    dp[0] = 0;
    dp[1] = 1;
    for (int i = 2; i <= n; ++i) {
        dp[i] = dp[i - 1] + dp[i - 2];
    }
    return dp[n];
}

long long climbStairs(int n) {
    std::vector<long long> dp(n + 2);
    dp[0] = 1;
    dp[1] = 1;
    for (int i = 2; i <= n; ++i) {
        dp[i] = dp[i - 1] + dp[i - 2];
    }
    return dp[n];
}

int knapsack(const std::vector<int>& wt, const std::vector<int>& val, int cap) {
    int n = static_cast<int>(wt.size());
    std::vector<std::vector<int>> dp(n + 1, std::vector<int>(cap + 1, 0));
    for (int i = 1; i <= n; ++i) {
        for (int w = 0; w <= cap; ++w) {
            dp[i][w] = dp[i - 1][w];
            if (w >= wt[i - 1]) {
                dp[i][w] = std::max(dp[i][w], dp[i - 1][w - wt[i - 1]] + val[i - 1]);
            }
        }
    }
    return dp[n][cap];
}

int main() {
    std::cout << "fib(10) = " << fib(10) << "\n";
    std::cout << "爬 5 階樓梯有 " << climbStairs(5) << " 種方法\n";
    std::cout << "背包最大價值 = " << knapsack({1, 3, 4, 5}, {1, 4, 5, 7}, 7) << "\n";
}
