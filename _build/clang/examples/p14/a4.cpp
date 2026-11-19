#include <iostream>
#include <string>
using namespace std;

class Student {
private:
    string name;
    int score;
public:
    Student(string n, int s) {               //@ 建構子:名字和類別相同、沒有回傳型態。建立物件時會自動執行,用來設定初始值。
        name = n;
        score = s;
    }
    void print() {
        cout << name << ": " << score << endl;
    }
};

int main() {
    Student a("Mina", 90);                   //@ 建立物件時,括號裡的值會交給建構子。
    Student b("Leo", 75);
    a.print();
    b.print();
    return 0;
}
