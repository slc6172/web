#include <iostream>
using namespace std;

int main() {
    int a = 3;
    int b = 5;
    cout << "交換前:a=" << a << " b=" << b << endl;
    int temp = a;
    a = b;
    b = temp;
    cout << "交換後:a=" << a << " b=" << b << endl;
    return 0;
}
