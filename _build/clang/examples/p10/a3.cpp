#include <iostream>
#include <string>
using namespace std;

int main() {
    string s = "Hello";
    cout << s[0] << endl;                    //@ 用索引取出一個字元,從 0 開始,和陣列一樣。
    cout << s[s.length() - 1] << endl;       //@ 最後一個字元的索引是「長度 − 1」。
    s[0] = 'J';                              //@ 改一個字元,要用單引號('J' 是 char)。
    cout << s << endl;
    int n = s.length();                      //@ 先把長度存進 int 變數,迴圈比較起來最單純。
    for (int i = 0; i < n; i++) {
        cout << i << ":" << s[i] << " ";
    }
    cout << endl;
    return 0;
}
