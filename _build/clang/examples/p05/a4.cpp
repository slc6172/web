#include <iostream>
using namespace std;

int main() {
    int a = 17, b = 5;
    cout << (a > b) << endl;                //@ 比較的結果是 bool:true 印成 1,false 印成 0。
    cout << (a == b) << endl;               //@ == 是「相等嗎?」。單個 = 是賦值,不要搞混。
    cout << (a != b) << endl;
    cout << (a > 3 && b < 3) << endl;       //@ && 是「而且」:兩邊都為真才是真。b < 3 不成立,所以是 0。
    cout << (a > 100 || b == 5) << endl;    //@ || 是「或者」:只要有一邊為真就是真。
    cout << !(a > b) << endl;               //@ ! 是「不是」:把真假反過來。
    return 0;
}
