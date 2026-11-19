#include <iostream>
using namespace std;

class Animal {
public:
    void speak() {
        cout << "(某種聲音)" << endl;
    }
};

class Dog : public Animal {
public:
    void speak() {                           //@ 子類別自己寫了一個同名的 speak。
        cout << "汪汪!" << endl;
    }
};

int main() {
    Dog d;
    d.speak();
    Animal* a = &d;                          //@ 用「Animal 指標」指著一隻 Dog。這是合法的:狗也是一種動物。
    a->speak();                              //@ -> 是「透過指標呼叫成員」,等於 (*a).speak()。
    return 0;
}
