#include <algorithm>
#include <iostream>
#include <vector>

std::vector<int> greedyChange(const std::vector<int>& coins, int amount) {
    std::vector<int> used;
    for (int c : coins) {
        while (amount >= c) {
            used.push_back(c);
            amount -= c;
        }
    }
    if (amount != 0) {
        used.clear();
    }
    return used;
}

int bestCount(const std::vector<int>& coins, int amount) {
    const int INF = 1000000000;
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

void show(const std::vector<int>& coins, int amount) {
    std::vector<int> used = greedyChange(coins, amount);
    std::cout << "金額 " << amount << ",貪婪用 " << used.size() << " 枚:";
    for (int c : used) {
        std::cout << " " << c;
    }
    std::cout << ";最少其實要 " << bestCount(coins, amount) << " 枚\n";
}

int main() {
    show({25, 10, 5, 1}, 63);
    show({4, 3, 1}, 6);
    show({12, 10, 5, 1}, 15);
}
