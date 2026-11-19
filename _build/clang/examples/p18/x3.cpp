#include <iostream>
#include <string>
#include <vector>
using namespace std;

struct Student {
    string name;
    int score;
};

bool removeStudent(vector<Student>& list, const string& name) {
    for (int i = 0; i < (int)list.size(); i++) {
        if (list[i].name == name) {
            list.erase(list.begin() + i);
            return true;
        }
    }
    return false;
}

int main() {
    vector<Student> list = {{"Mina", 90}, {"Leo", 75}, {"Amy", 82}};
    cout << (removeStudent(list, "Leo") ? "已刪除 Leo" : "找不到 Leo") << endl;
    cout << (removeStudent(list, "Bob") ? "已刪除 Bob" : "找不到 Bob") << endl;
    for (const Student& s : list) {
        cout << s.name << " " << s.score << endl;
    }
    return 0;
}
