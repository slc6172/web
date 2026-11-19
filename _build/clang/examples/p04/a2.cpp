#include <iostream>
using namespace std;

int main() {
    int a, b;
    cout << "請輸入兩個整數:";
    cin >> a >> b;                     //@ 一行可以連續讀好幾個值。輸入時用空格或換行隔開都可以。
    cout << a << " + " << b << " = " << a + b << endl;
    return 0;
}
