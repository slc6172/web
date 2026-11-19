#include <iostream>
#include <vector>

int sum(const std::vector<int>& v) {
    int total = 0;
    for (int x : v) {
        total += x;
    }
    return total;
}

int main() {
    std::vector<int> v = {3, 1, 4, 1, 5};
    std::cout << sum(v) << "\n";
}
