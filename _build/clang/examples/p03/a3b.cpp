#include <iostream>
using namespace std;

int main() {
    int n = 3.9;                  //@ int 只能存整數,3.9 的小數部分會被直接捨去(不是四捨五入),n 變成 3。
    double d = 3;                 //@ 把整數存進 double 沒問題,d 的值是 3。
    char c = 'A';
    cout << n << endl;
    cout << d << endl;
    cout << c << endl;
    cout << c + 1 << endl;        //@ 字元其實是小整數('A' 的編碼是 65)。c + 1 是整數運算,所以印出 66,不是 B。
    return 0;
}
