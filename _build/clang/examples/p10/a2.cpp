#include <iostream>
#include <string>
using namespace std;

int main() {
    string a = "Hello";
    string b = "C++";
    string c = a + " " + b;                  //@ 用 + 把字串接起來。注意:兩邊至少要有一個是 string 變數,不能是兩個 "文字" 相加。
    c += "!";                                //@ += 在後面接上更多文字。
    cout << c << endl;
    return 0;
}
