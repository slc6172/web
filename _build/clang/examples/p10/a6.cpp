#include <iostream>
#include <string>
using namespace std;

int main() {
    string name;
    cout << "全名:";
    getline(cin, name);                      //@ getline 讀一整行,包含空格。
    cout << "你好," << name << "(" << name.length() << " 個字元)" << endl;
    return 0;
}
