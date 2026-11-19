#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

struct Student {                             //@ 一位學生的資料:名字與分數。
    string name;
    int score;
};

bool higherScore(const Student& a, const Student& b) {   //@ 告訴 sort「怎麼比」:分數高的排前面。回傳 true 表示 a 應該排在 b 前面。
    return a.score > b.score;
}

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

void showStats(const vector<Student>& list) {
    if (list.empty()) {
        cout << "(目前沒有資料)" << endl;
        return;
    }
    int sum = 0;
    const Student* best = &list[0];          //@ 用指標記住目前最高分的那位學生(第 12 篇)。
    for (const Student& s : list) {
        sum += s.score;
        if (s.score > best->score) {
            best = &s;
        }
    }
    cout << "共 " << list.size() << " 人,平均 " << (double)sum / list.size() << endl;
    cout << "最高分:" << best->name << " " << best->score << endl;
}

int main() {
    vector<Student> list;
    int choice;
    do {
        cout << "\n1 新增  2 列出  3 統計  4 排序  0 離開:";
        cin >> choice;
        if (choice == 1) {
            addStudent(list);
        }         else if (choice == 2) {
            showAll(list);
        }         else if (choice == 3) {
            showStats(list);
        }         else if (choice == 4) {
            sort(list.begin(), list.end(), higherScore);
            cout << "已依分數由高到低排序" << endl;
        }

    } while (choice != 0);
    cout << "再見" << endl;
    return 0;
}
