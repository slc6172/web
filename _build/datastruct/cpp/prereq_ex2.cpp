#include <iostream>

void swapInt(int& a, int& b) {
    int tmp = a;
    a = b;
    b = tmp;
}

int main() {
    int a = 3, b = 7;
    swapInt(a, b);
    std::cout << a << " " << b << "\n";
}
