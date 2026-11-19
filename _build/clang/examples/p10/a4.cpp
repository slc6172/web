#include <iostream>
#include <string>
using namespace std;

int main() {
    string s = "Hello, C++ World";
    cout << s.find("C++") << endl;           //@ find:找到子字串第一次出現的位置(索引)。
    cout << s.substr(7, 3) << endl;          //@ substr(開始位置, 長度):取出一段。這裡從索引 7 取 3 個字元。
    cout << s.substr(7) << endl;             //@ 只給開始位置,就一路取到最後。
    size_t pos = s.find("Java");             //@ size_t 是「表示大小或位置的非負整數」型態。find 的結果就是這個型態。
    if (pos == string::npos) {               //@ 找不到時,find 回傳特殊值 string::npos,要用它來判斷。
        cout << "找不到 Java" << endl;
    }
    return 0;
}
