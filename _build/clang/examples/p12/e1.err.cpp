#include <iostream>
using namespace std;

void show(const int& n) {
    n = 5;
    cout << n << endl;
}

int main() {
    int x = 1;
    show(x);
    return 0;
}
