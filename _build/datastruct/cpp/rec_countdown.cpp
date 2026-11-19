#include <iostream>

void countdown(int n) {
    if (n == 0) {
        std::cout << "liftoff\n";             // 基底條件:不再呼叫自己
        return;
    }
    std::cout << n << " ";
    countdown(n - 1);                        // 呼叫自己,但問題變小了
}

int main() {
    countdown(3);
}
