#include <iostream>
using namespace std;

int main() {
    int x = 10;
    int* p = &x;
    cout << *p << endl;
    *p = 20;
    cout << x << endl;
    cout << (p == &x) << endl;
    return 0;
}
