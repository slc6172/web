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
        score = s;
    }
    char grade() {
        if (score >= 90) {
            return 'A';
        } else if (score >= 70) {
            return 'B';
        }
        return 'C';
    }
    void print() {
        cout << name << " " << score << " 等級 " << grade() << endl;
    }
};

int main() {
    Student a("Mina", 92);
    Student b("Leo", 75);
    Student c("Amy", 58);
    a.print();
    b.print();
    c.print();
    return 0;
}
