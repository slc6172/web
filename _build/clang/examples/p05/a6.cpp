#include <iostream>
using namespace std;

int main() {
    int i = 5;
    cout << i++ << endl;                //@ i++:先用目前的值(印出 5),再把 i 加 1。
    cout << i << endl;
    cout << ++i << endl;                //@ ++i:先加 1(i 變成 7),再用新的值。
    return 0;
}
