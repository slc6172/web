#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    map<string, int> scores = {{"Mina", 90}, {"Leo", 75}, {"Amy", 82}};
    string name;
    cout << "查詢誰?";
    cin >> name;
    if (scores.count(name) == 1) {
        cout << name << " 的成績是 " << scores[name] << endl;
    } else {
        cout << "查無此人" << endl;
    }
    return 0;
}
