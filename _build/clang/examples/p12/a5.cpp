#include <iostream>
using namespace std;

int main() {
    int a[3] = {10, 20, 30};
    int* p = a;
    cout << *p << endl;
    p = p + 1;
    cout << *p << endl;
    cout << p[1] << endl;
    cout << a[2] << endl;
    return 0;
}
