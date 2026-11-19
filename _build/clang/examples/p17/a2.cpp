#include <iostream>
using namespace std;

int main() {
    int* p = new int(1);
    cout << *p << endl;
    p = new int(2);
    cout << *p << endl;
    delete p;
    return 0;
}
