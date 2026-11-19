#include <iostream>
#include <string>
using namespace std;

struct Student {
    string name;
    int score;

    void print() {                           //@ 成員函式:放在型態裡面的函式,專門處理這個型態的資料。
        cout << name << ": " << score << endl;   //@ 在成員函式裡,可以直接使用同一個物件的成員,不用加 s.。
    }
};

int main() {
    Student a;
    a.name = "Mina";
    a.score = 90;
    Student b;
    b.name = "Leo";
    b.score = 75;
    a.print();                               //@ 呼叫成員函式:物件.函式()。印的是 a 自己的資料。
    b.print();
    return 0;
}
