#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>

bool safe(const std::vector<int>& cols, int row, int c) {
    for (int r = 0; r < row; ++r) {
        if (cols[r] == c || std::abs(cols[r] - c) == row - r) {
            return false;
        }
    }
    return true;
}

void solve(int n, int row, std::vector<int>& cols, std::vector<std::vector<int>>& sols) {
    if (row == n) {
        sols.push_back(cols);
        return;
    }
    for (int c = 0; c < n; ++c) {
        if (safe(cols, row, c)) {
            cols[row] = c;
            solve(n, row + 1, cols, sols);
        }
    }
}

int main() {
    for (int n = 4; n <= 8; ++n) {
        std::vector<int> cols(n, -1);
        std::vector<std::vector<int>> sols;
        solve(n, 0, cols, sols);
        std::cout << n << " 皇后:" << sols.size() << " 組解\n";
        if (n == 4) {
            for (int c : sols[0]) {
                std::cout << std::string(c, '.') << "Q" << std::string(n - c - 1, '.') << "\n";
            }
        }
    }
}
