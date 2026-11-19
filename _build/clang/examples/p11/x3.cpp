#include <iostream>
using namespace std;

int power(int base, int exp) {
    int result = 1;
    for (int i = 0; i < exp; i++) {
        result *= base;
    }
    return result;
}

int main() {
    cout << power(2, 10) << endl;
    cout << power(3, 4) << endl;
    return 0;
}
