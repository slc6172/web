#include <iostream>
#include <string>
using namespace std;

class Animal {                               //@ 基底類別(父類別):放所有動物共同的東西。
protected:                                   //@ protected:外面不能碰,但「子類別」可以使用。
    string name;
public:
    Animal(string n) {
        name = n;
    }
    string getName() {
        return name;
    }
};

class Dog : public Animal {                  //@ 冒號加 public Animal:Dog「繼承」Animal,自動擁有 name 與 getName()。
public:
    Dog(string n) : Animal(n) {}             //@ 冒號後面:先呼叫基底類別的建構子,把名字交給它。
    void bark() {
        cout << name << ": 汪汪!" << endl;   //@ 子類別可以直接使用 protected 的 name。
    }
};

int main() {
    Dog d("Rex");
    cout << d.getName() << endl;             //@ getName 是從 Animal 繼承來的,Dog 沒有自己寫,卻能呼叫。
    d.bark();
    return 0;
}
