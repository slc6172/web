#include <iostream>
#include <string>                            //@ 使用 string 要引入 <string>。
using namespace std;

int main() {
    string s = "Hello";                      //@ string:裝一段文字的型態。文字要用雙引號。
    cout << s << endl;
    cout << s.length() << endl;              //@ length():有幾個字元。s.size() 的結果完全一樣。
    return 0;
}
