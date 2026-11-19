#include <iostream>
using namespace std;

void swapInt(int& a, int& b) {
    int temp = a;
    a = b;
    b = temp;
}

int main() {
    int x = 3, y = 5;
    swapInt(x, y);
    cout << x << " " << y << endl;
    return 0;
}
