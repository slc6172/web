#include <iostream>
#include <string>
#include <vector>
using namespace std;

struct Student {                             //@ 一位學生的資料:名字與分數。
    string name;
    int score;
};

void addStudent(vector<Student>& list) {     //@ 參數用參考(第 12 篇):才能把新學生加進呼叫端的 vector。
    Student s;
    cout << "姓名:";
    cin >> s.name;
    cout << "分數(0-100):";
    cin >> s.score;
    list.push_back(s);
    cout << "已新增 " << s.name << endl;
}

void showAll(const vector<Student>& list) {   //@ const 參考:只讀不改,不複製整個 vector。
    if (list.empty()) {
        cout << "(目前沒有資料)" << endl;
        return;
    }
    for (const Student& s : list) {
        cout << s.name << "  " << s.score << endl;
    }
}

int main() {
    vector<Student> list;
    int choice;
    do {
        cout << "\n1 新增  2 列出  0 離開:";
        cin >> choice;
        if (choice == 1) {
            addStudent(list);
        }         else if (choice == 2) {
            showAll(list);
        }

    } while (choice != 0);
    cout << "再見" << endl;
    return 0;
}
