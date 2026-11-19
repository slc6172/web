#include <iostream>
#include <string>
using namespace std;

int main() {
    string name;
    cout << "全名:";
    cin >> name;                             //@ cin >> 遇到空格就停,所以只讀到第一個單字。
    cout << "你好," << name << endl;
    return 0;
}
