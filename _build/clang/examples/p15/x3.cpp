#include <iostream>
#include <string>
using namespace std;

class Person {
protected:
    string name;
    int age;
public:
    Person(string n, int a) {
        name = n;
        age = a;
    }
    void introduce() {
        cout << "我是 " << name << ",今年 " << age << " 歲" << endl;
    }
};

class Student : public Person {
private:
    string school;
public:
    Student(string n, int a, string s) : Person(n, a) {
        school = s;
    }
    void introduce() {
        Person::introduce();
        cout << "就讀 " << school << endl;
    }
};

int main() {
    Student s("Mina", 20, "台北大學");
    s.introduce();
    return 0;
}
