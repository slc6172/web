#include <iostream>
#include <stdexcept>
#include <vector>

int main() {
    std::vector<int> v = {10, 20, 30};
    try {
        std::cout << v.at(10) << "\n";       // at() 會檢查範圍,越界就丟例外
    } catch (const std::out_of_range&) {
        std::cout << "out of range\n";
    }
}
