#include <iostream>
using namespace std;

int maxOf(int a, int b) {
    return a > b ? a : b;
}

int maxOf3(int a, int b, int c) {
    return maxOf(maxOf(a, b), c);
}

int main() {
    cout << maxOf3(7, 19, 4) << endl;
    cout << maxOf3(-5, -2, -9) << endl;
    return 0;
}
