#include <iostream>
#include <string>
#include <vector>
using namespace std;

struct Student {
    string name;
    int score;
};

int main() {
    vector<Student> list = {{"Mina", 90}, {"Leo", 75}, {"Amy", 82}};   //@ 物件也可以放進 vector。每一組大括號是一個 Student。
    int sum = 0;
    for (Student s : list) {
        cout << s.name << ": " << s.score << endl;
        sum += s.score;
    }
    cout << "平均:" << sum / 3.0 << endl;
    return 0;
}
