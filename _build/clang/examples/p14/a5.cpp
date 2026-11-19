#include <iostream>
#include <string>
using namespace std;

class Student {
private:
    string name;
    int score;
public:
    Student(string n, int s) {
        name = n;
        score = 0;
        setScore(s);                         //@ 建構子也可以重複使用 setScore 的檢查。
    }
    void setScore(int s) {                   //@ setter:修改 score 的唯一入口。
        if (s >= 0 && s <= 100) {
            score = s;
        } else {
            cout << "分數 " << s << " 不合法,保持原本的 " << score << endl;
        }
    }
    int getScore() {                         //@ getter:讓外面能讀取。
        return score;
    }
    string getName() {
        return name;
    }
};

int main() {
    Student a("Mina", 90);
    a.setScore(120);
    cout << a.getName() << ": " << a.getScore() << endl;
    return 0;
}
