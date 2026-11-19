#include <iostream>
#include <string>
#include <vector>
using namespace std;

struct Student {
    string name;
    int score;
};

int findStudent(const vector<Student>& list, const string& name) {
    for (int i = 0; i < (int)list.size(); i++) {
        if (list[i].name == name) {
            return i;
        }
    }
    return -1;
}

int main() {
    vector<Student> list = {{"Mina", 90}, {"Leo", 75}, {"Amy", 82}};
    string name;
    cout << "要找誰?";
    cin >> name;
    int idx = findStudent(list, name);
    if (idx == -1) {
        cout << "查無此人" << endl;
    } else {
        cout << name << " 的分數是 " << list[idx].score << endl;
    }
    return 0;
}
