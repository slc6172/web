#include <iostream>
#include <vector>

int main() {
    std::vector<int> v;                      // 空的 vector
    std::cout << v.size() - 1 << "\n";       // 不是 -1!size() 是無號數
    int n = static_cast<int>(v.size());      // 先轉成 int 再計算
    std::cout << n - 1 << "\n";
}
