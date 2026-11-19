#include <iostream>
using namespace std;

int add(int a, int b);                      //@ 函式宣告(原型):只寫「長相」並以分號結束,告訴編譯器「後面會有一個叫 add 的函式」。

int main() {
    cout << add(2, 3) << endl;              //@ 因為上面已經宣告過,這裡才能呼叫。
    return 0;
}

int add(int a, int b) {                     //@ 真正的內容(定義)可以放在後面。
    return a + b;
}
