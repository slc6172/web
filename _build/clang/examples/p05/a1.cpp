#include <iostream>
using namespace std;

int main() {
    int a = 17, b = 5;                  //@ 一行可以同時宣告好幾個同型態的變數,用逗號隔開。
    cout << a + b << endl;
    cout << a - b << endl;
    cout << a * b << endl;              //@ 乘號是 *,不是 x。
    cout << a / b << endl;              //@ 兩個整數相除,結果還是整數:17 / 5 = 3 餘 2,小數部分直接捨去。
    cout << a % b << endl;              //@ % 是取餘數:17 除以 5 的餘數是 2。只能用在整數。
    return 0;
}
