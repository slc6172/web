#include <iostream>
#include <string>
using namespace std;

int main() {
    string t = "你好";
    cout << t << endl;
    cout << t.length() << endl;              //@ 中文字在 UTF-8 裡通常佔 3 個位元組,所以 2 個字的 length() 是 6,不是 2。
    return 0;
}
