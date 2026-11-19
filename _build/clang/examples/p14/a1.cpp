#include <iostream>
#include <string>
using namespace std;

struct Student {                             //@ struct:把幾個相關的資料打包成一個新型態。大括號結尾要有分號!
    string name;                             //@ 成員變數(也叫欄位):這個型態裡的每一項資料。
    int score;
};

int main() {
    Student s;                               //@ 用新型態宣告一個變數,叫做「物件」。
    s.name = "Mina";                         //@ 用點 . 存取物件的成員。
    s.score = 90;
    cout << s.name << ": " << s.score << endl;
    return 0;
}
