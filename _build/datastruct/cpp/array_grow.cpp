#include <iostream>
#include <vector>

int main() {
    std::vector<int> v;
    for (int i = 1; i <= 9; ++i) {
        v.push_back(i);
        std::cout << v.size() << " " << v.capacity() << "\n";
    }
}
