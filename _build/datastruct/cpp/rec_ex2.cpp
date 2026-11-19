#include <iostream>

int power(int base, int exp) {
    if (exp == 0) {
        return 1;
    }
    return base * power(base, exp - 1);
}

int main() {
    std::cout << power(2, 3) << " " << power(5, 0) << "\n";
}
