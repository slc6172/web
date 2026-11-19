#include <iostream>

void addOne(int& n) {
    ++n;
}

int main() {
    int x = 5;
    addOne(x);
    std::cout << x << "\n";
}
