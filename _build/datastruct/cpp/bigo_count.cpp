#include <iostream>

int main() {
    int n = 8;
    int single = 0;
    for (int i = 0; i < n; ++i) {
        ++single;                            // 單層迴圈:做 n 次
    }

    int nested = 0;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            ++nested;                        // 雙層迴圈:做 n * n 次
        }
    }

    int halving = 0;
    int m = n;
    while (m > 1) {
        m /= 2;
        ++halving;                           // 每次砍一半:大約 log2(n) 次
    }

    std::cout << single << " " << nested << " " << halving << "\n";
}
