#include <iostream>
#include <string>
#include <vector>
using namespace std;

struct Student {
    string name;
    int score;
};

int countPassed(const vector<Student>& list) {
    int count = 0;
    for (const Student& s : list) {
        if (s.score >= 60) {
            count++;
        }
    }
    return count;
}

int main() {
    vector<Student> list = {{"Mina", 90}, {"Leo", 55}, {"Amy", 82}, {"Bob", 48}};
    cout << "及格人數:" << countPassed(list) << " / " << list.size() << endl;
    return 0;
}
