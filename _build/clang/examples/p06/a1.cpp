#include <iostream>
using namespace std;

int main() {
    int age;
    cout << "年齡:";
    cin >> age;
    if (age >= 18) {                     //@ if 後面的小括號放「條件」,條件成立(結果不是 0)才會執行後面大括號裡的內容。
        cout << "成年" << endl;
    } else {                             //@ else:條件不成立時,改做這一段。
        cout << "未成年" << endl;
    }
    return 0;
}
