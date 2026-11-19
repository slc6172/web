#include <iostream>
#include <string>
using namespace std;

int main() {
    int age;
    string name;
    cout << "年齡:";
    cin >> age;
    cout << "名字:";
    getline(cin, name);                //@ getline 讀取「一整行」直到換行為止(可含空格)。
    cout << "你好 " << name << ",年齡 " << age << endl;
    return 0;
}
