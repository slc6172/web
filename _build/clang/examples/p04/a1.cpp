#include <iostream>
using namespace std;

int main() {
    int age;                           //@ 先宣告一個空盒子,等著接收輸入。
    cout << "請輸入年齡:";             //@ 先用 cout 印出提示,讓使用者知道要輸入什麼。這行沒有 endl,游標會停在冒號後面。
    cin >> age;                        //@ cin 是「鍵盤輸入」,>> 的箭頭指向變數:把使用者打的數字放進 age。程式會在這裡停下來等。
    cout << "你今年 " << age << " 歲" << endl;
    return 0;
}
