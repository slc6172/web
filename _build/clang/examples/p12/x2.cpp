#include <iostream>
using namespace std;

void incByPtr(int* p) {
    *p = *p + 1;
}

void incByRef(int& r) {
    r = r + 1;
}

int main() {
    int x = 5;
    incByPtr(&x);
    cout << x << endl;
    incByRef(x);
    cout << x << endl;
    return 0;
}
