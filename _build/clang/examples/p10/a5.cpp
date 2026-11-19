#include <iostream>
#include <string>
using namespace std;

int main() {
    string x = "apple", y = "banana";
    cout << (x == y) << endl;                //@ == 比較兩個字串的內容是否完全相同。
    cout << (x < y) << endl;                 //@ < 依字典順序比較:apple 排在 banana 前面,所以是 1。
    cout << ("A" == string("a")) << endl;    //@ 大小寫不同,就是不同的字元。
    return 0;
}
