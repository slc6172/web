#include <algorithm>
#include <fstream>
#include <iomanip>
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

int readScore() {                            //@ 專門負責「讀一個合法分數」的函式:不合法就一直問。
    int score;
    while (true) {                           //@ while (true):永遠成立的條件,靠迴圈裡的 return 離開。
        cout << "分數(0-100):";
        if (cin >> score && score >= 0 && score <= 100) {   //@ 讀取成功,而且範圍正確,才算數。
            return score;
        }
        cout << "請輸入 0 到 100 的整數" << endl;
        cin.clear();                         //@ 把 cin 從失敗狀態救回來(第 4 篇的陷阱)。
        cin.ignore(1000, '\n');              //@ 丟掉這一行剩下的錯誤輸入。
    }
}

void addStudent(vector<Student>& list) {
    Student s;
    cout << "姓名:";
    cin >> s.name;
    s.score = readScore();
    list.push_back(s);
    cout << "已新增 " << s.name << endl;
}

void showAll(const vector<Student>& list) {
    if (list.empty()) {
        cout << "(目前沒有資料)" << endl;
        return;
    }
    for (const Student& s : list) {
        cout << left << setw(8) << s.name << right << setw(4) << s.score << endl;   //@ left / right 與 setw(第 4 篇)讓名字與分數整齊對齊。
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

void saveToFile(const vector<Student>& list, const string& filename) {
    ofstream out(filename);
    if (!out.is_open()) {                    //@ 第 16 篇:寫檔前先確認檔案能開。
        cout << "無法寫入檔案" << endl;
        return;
    }
    for (const Student& s : list) {
        out << s.name << " " << s.score << endl;
    }
    cout << "已儲存 " << list.size() << " 筆" << endl;
}

void loadFromFile(vector<Student>& list, const string& filename) {
    ifstream in(filename);
    if (!in.is_open()) {
        cout << "找不到檔案 " << filename << endl;
        return;
    }
    vector<Student> loaded;
    string name, scoreText;
    while (in >> name >> scoreText) {
        try {
            loaded.push_back({name, stoi(scoreText)});   //@ stoi 轉換失敗會丟出例外,被下面的 catch 接住。
        } catch (const exception& e) {
            cout << "略過格式錯誤的資料:" << name << " " << scoreText << endl;
        }
    }
    list = loaded;
    cout << "已讀入 " << list.size() << " 筆" << endl;
}

int main() {
    vector<Student> list;
    const string fileName = "students.txt";
    int choice = -1;
    while (choice != 0) {
        cout << "\n1 新增  2 列出  3 統計  4 排序  5 存檔  6 讀檔  0 離開\n選擇:";
        if (!(cin >> choice)) {              //@ 使用者輸入的不是數字:救回 cin,告訴他,再問一次。
            cout << "請輸入數字" << endl;
            cin.clear();
            cin.ignore(1000, '\n');
            choice = -1;
            continue;                        //@ continue:跳過這一圈剩下的部分,直接回到迴圈開頭(第 7 篇)。
        }
        switch (choice) {                    //@ 選項多的時候,switch 比一長串 if 清楚(第 6 篇)。
            case 1: addStudent(list); break;
            case 2: showAll(list); break;
            case 3: showStats(list); break;
            case 4:
                sort(list.begin(), list.end(), higherScore);
                cout << "已依分數由高到低排序" << endl;
                break;
            case 5: saveToFile(list, fileName); break;
            case 6: loadFromFile(list, fileName); break;
            case 0: cout << "再見" << endl; break;
            default: cout << "沒有這個選項" << endl;
        }
    }
    return 0;
}
