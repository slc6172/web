#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {5, 2, 9, 1, 7, 3};
    std::sort(v.begin(), v.end());                       // 由小到大
    for (int x : v) {
        std::cout << x << " ";
    }
    std::cout << "\n";
    std::sort(v.begin(), v.end(), [](int a, int b) { return a > b; });   // 由大到小
    for (int x : v) {
        std::cout << x << " ";
    }
    std::cout << "\n";
}
