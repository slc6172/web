#include <iostream>

int main() {
    int x = 10;
    int y = 5;
    int& r = x;
    int* p = &x;
    *p = 20;
    r = 30;
    p = &y;
    *p = 99;
    std::cout << x << " " << y << "\n";
}
