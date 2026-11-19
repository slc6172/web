#include <iostream>
#include <string>
using namespace std;

int main() {
    int age;
    string name;
    cout << "年齡:";
    cin >> age;
    cin.ignore(1000, '\n');            //@ 丟掉 age 後面留在輸入裡的換行(最多略過 1000 個字元,直到遇到換行)。
    cout << "名字:";
    getline(cin, name);
    cout << "你好 " << name << ",年齡 " << age << endl;
    return 0;
}
