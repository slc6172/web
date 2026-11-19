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
    void speak() override {
        cout << "汪汪!" << endl;
    }
};

class Cat : public Animal {
public:
    void speak() override {
        cout << "喵喵!" << endl;
    }
};

int main() {
    Dog d;
    Cat c;
    Animal* zoo[2] = {&d, &c};               //@ 一個 Animal 指標的陣列,裝著不同種類的動物。
    for (Animal* a : zoo) {
        a->speak();                          //@ 同一行程式、同一個呼叫,依每隻動物真正的種類,做不同的事。
    }
    return 0;
}
