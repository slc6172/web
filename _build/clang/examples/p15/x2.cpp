#include <iostream>
using namespace std;

class Animal {
public:
    virtual void speak() {
        cout << "(某種聲音)" << endl;
    }
};

class Dog : public Animal {
public:
    void speak() override { cout << "汪汪!" << endl; }
};

class Cat : public Animal {
public:
    void speak() override { cout << "喵喵!" << endl; }
};

class Cow : public Animal {
public:
    void speak() override { cout << "哞~" << endl; }
};

int main() {
    Dog d;
    Cat c;
    Cow w;
    Animal* zoo[3] = {&d, &c, &w};
    for (Animal* a : zoo) {
        a->speak();
    }
    return 0;
}
