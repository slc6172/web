#include <iostream>
#include <vector>

int countGreater(const std::vector<int>& v, int x) {
    int count = 0;
    for (int y : v) {
        if (y > x) {
            ++count;
        }
    }
    return count;
}

int main() {
    std::vector<int> v = {3, 1, 4, 1, 5, 9, 2, 6};
    std::cout << countGreater(v, 3) << "\n";
    std::cout << countGreater(v, 9) << "\n";
}
