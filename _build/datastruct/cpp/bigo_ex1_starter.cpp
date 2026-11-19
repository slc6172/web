#include <iostream>
#include <vector>

// 這個函式的時間是 O(?)。先想,再展開答案。
int countEven(const std::vector<int>& v) {
    int count = 0;
    for (int x : v) {
        if (x % 2 == 0) {
            ++count;
        }
    }
    return count;
}

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5, 6};
    std::cout << countEven(v) << "\n";
}
