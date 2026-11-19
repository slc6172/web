#include <iostream>
using namespace std;

void addOne(int n) {
    n = n + 1;
    cout << "函式裡 n = " << n << endl;
}

int main() {
    int x = 5;
    addOne(x);
    cout << "main 裡 x = " << x << endl;
    return 0;
}
