#include <iostream>
using namespace std;

int main() {
    cout << 7 / 2 << endl;              //@ 整數 ÷ 整數 = 整數,捨去小數。
    cout << 7.0 / 2 << endl;            //@ 只要有一邊是小數,就會用小數除法。
    double wrong = 7 / 2;               //@ 陷阱:右邊先用整數除法算出 3,才存進 double,所以 wrong 是 3。
    double right = 7 / 2.0;             //@ 把其中一個數寫成 2.0,就得到 3.5。
    cout << wrong << endl;
    cout << right << endl;
    return 0;
}
