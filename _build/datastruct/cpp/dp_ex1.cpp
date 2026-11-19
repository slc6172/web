#include <iostream>
#include <vector>

long long ways(int n) {
    std::vector<long long> dp(n + 3, 0);
    dp[0] = 1;
    for (int i = 1; i <= n; ++i) {
        for (int step = 1; step <= 3; ++step) {
            if (i - step >= 0) {
                dp[i] += dp[i - step];
            }
        }
    }
    return dp[n];
}

int main() {
    std::cout << ways(4) << " " << ways(5) << " " << ways(0) << "\n";
}
